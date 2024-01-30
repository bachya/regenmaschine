"""Define a client to interact with a RainMachine unit."""
from __future__ import annotations

import asyncio
import json
import ssl
from datetime import datetime
from typing import Any, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientOSError, ServerDisconnectedError
from yarl import URL

from .const import LOGGER
from .controller import Controller, LocalController, RemoteController
from .errors import RequestError, TokenExpiredError, raise_for_error

DEFAULT_LOCAL_PORT = 8080
DEFAULT_TIMEOUT = 30


class Client:
    """Define the client."""

    def __init__(
        self,
        *,
        request_timeout: int = DEFAULT_TIMEOUT,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize.

        Args:
            request_timeout: The number of seconds before a request times out.
            session: An optional aiohttp ClientSession.
        """
        self._request_timeout = request_timeout
        self._session = session

        self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

        # The local API on Gen 1 controllers uses outdated RSA ciphers (and there isn't
        # any indication that they'll be updated). Python 3.10+ enforces minimum TLS
        # standards that the Gen 1 can't support, so to keep compatibility, we loosen
        # things up:
        #   1. We set a minimum TLS version of SSLv3
        #   2. We utilize the "DEFAULT" cipher suite (which includes old RSA ciphers).
        #   3. We don't validate the hostname.
        #   4. We allow self-signed certificates.
        #   5. We allow legacy server connections.
        self._ssl_context.minimum_version = ssl.TLSVersion.SSLv3
        self._ssl_context.set_ciphers("DEFAULT:@SECLEVEL=0")
        self._ssl_context.check_hostname = False
        self._ssl_context.verify_mode = ssl.CERT_NONE
        self._ssl_context.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0x4)

        self.controllers: dict[str, Controller] = {}

    async def _request(  # pylint: disable=too-many-arguments
        self,
        method: str,
        url: URL,
        *,
        access_token: str | None = None,
        access_token_expiration: datetime | None = None,
        use_ssl: bool = True,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: An HTTP method.
            url: An API URL.
            access_token: An optional API access token.
            access_token_expiration: An optional API token expiration datetime.
            use_ssl: Whether to use SSL/TLS on the request.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.

        Raises:
            AssertionError: To handle mypy strangeness.
            RequestError: Raised upon an underlying HTTP error.
            TokenExpiredError: Raised upon an expired access token
        """
        if access_token_expiration and datetime.now() >= access_token_expiration:
            raise TokenExpiredError("Long-lived access token has expired")

        kwargs.setdefault("headers", {})
        kwargs["headers"]["Content-Type"] = "application/json"

        kwargs.setdefault("params", {})
        if access_token:
            kwargs["params"]["access_token"] = access_token

        if use_running_session := self._session and not self._session.closed:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            # Only try 2x for ServerDisconnectedError to comply with the RFC:
            # https://datatracker.ietf.org/doc/html/rfc2616#section-8.1.4
            for attempt in range(2):
                try:
                    return await self._request_with_session(
                        session, method, url, use_ssl, **kwargs
                    )
                except ServerDisconnectedError as err:
                    # The HTTP/1.1 spec allows the device to close the connection
                    # at any time. aiohttp raises ServerDisconnectedError to let us
                    # decide what to do. In this case we want to retry as it likely
                    # means the connection was stale and the server closed it on us:
                    if attempt == 0:
                        continue
                    raise RequestError(
                        f"Error requesting data from {url}: {err}"
                    ) from err

        finally:
            if not use_running_session:
                await session.close()

        raise AssertionError  # https://github.com/python/mypy/issues/8964

    async def _request_with_session(
        self,
        session: ClientSession,
        method: str,
        url: URL,
        use_ssl: bool,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Make a request with a session.

        Args:
            session: An aiohttp ClientSession.
            method: An HTTP method.
            url: An API URL.
            use_ssl: Whether to use SSL/TLS on the request.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.

        Raises:
            RequestError: Raised upon an underlying HTTP error.
        """
        try:
            async with session.request(
                method,
                url,
                ssl=self._ssl_context if use_ssl else None,
                timeout=self._request_timeout,
                **kwargs,
            ) as resp:
                data = await resp.json(content_type=None)
        except json.decoder.JSONDecodeError as err:
            raise RequestError("Unable to parse response as JSON") from err
        except ClientOSError as err:
            raise RequestError(
                f"Connection error while requesting data from {url}"
            ) from err
        except asyncio.TimeoutError as err:
            raise RequestError(f"Timed out while requesting data from {url}") from err

        LOGGER.debug("Data received for %s: %s", url, data)
        raise_for_error(resp, data)

        return cast(dict[str, Any], data)

    async def load_local(  # pylint: disable=too-many-arguments
        self,
        host: str,
        password: str,
        port: int = DEFAULT_LOCAL_PORT,
        use_ssl: bool = True,
        skip_existing: bool = True,
    ) -> None:
        """Create a local client.

        Args:
            host: The IP address or hostname of the controller.
            password: The controller password.
            port: The port that serves the controller's API.
            use_ssl: Whether to use SSL/TLS on the request.
            skip_existing: Don't load the controller if it's already loaded.
        """
        controller = LocalController(self._request, host, port, use_ssl)
        await controller.login(password)

        wifi_data = await controller.provisioning.wifi()
        if skip_existing and wifi_data["macAddress"] in self.controllers:
            return

        version_data = await controller.api.versions()
        controller.api_version = version_data["apiVer"]
        controller.hardware_version = str(version_data["hwVer"])
        controller.mac = wifi_data["macAddress"]
        controller.software_version = version_data["swVer"]

        name = await controller.provisioning.device_name
        controller.name = str(name)

        self.controllers[controller.mac] = controller

    async def load_remote(
        self, email: str, password: str, skip_existing: bool = True
    ) -> None:
        """Create a remote client.

        Args:
            email: A RainMachine account email address.
            password: The account password.
            skip_existing: Don't load the controller if it's already loaded.
        """
        auth_resp = await self._request(
            "post",
            URL("https://my.rainmachine.com/login/auth"),
            json={"user": {"email": email, "pwd": password, "remember": 1}},
        )

        access_token: str = auth_resp["access_token"]

        sprinklers_resp = await self._request(
            "post",
            URL("https://my.rainmachine.com/devices/get-sprinklers"),
            access_token=access_token,
            json={"user": {"email": email, "pwd": password, "remember": 1}},
        )

        for sprinkler in sprinklers_resp["sprinklers"]:
            if skip_existing and sprinkler["mac"] in self.controllers:
                continue

            controller: RemoteController = RemoteController(self._request)
            await controller.login(access_token, sprinkler["sprinklerId"], password)

            version_data = await controller.api.versions()
            controller.api_version = version_data["apiVer"]
            controller.hardware_version = str(version_data["hwVer"])
            controller.mac = sprinkler["mac"]
            controller.name = str(sprinkler["name"])
            controller.software_version = version_data["swVer"]

            self.controllers[sprinkler["mac"]] = controller
