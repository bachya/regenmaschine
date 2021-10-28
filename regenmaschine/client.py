"""Define a client to interact with a RainMachine unit."""
import asyncio
from datetime import datetime
import logging
from typing import Any, Dict, Optional, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError, ServerDisconnectedError
import async_timeout

from regenmaschine.controller import Controller, LocalController, RemoteController
from regenmaschine.errors import RequestError, TokenExpiredError, raise_remote_error

_LOGGER: logging.Logger = logging.getLogger(__name__)

DEFAULT_LOCAL_PORT: int = 8080
DEFAULT_TIMEOUT: int = 30


def _raise_for_remote_status(url: str, data: Dict[str, Any]) -> None:
    """Raise an error from the remote API if necessary."""
    if data.get("errorType") and data["errorType"] > 0:
        raise_remote_error(data["errorType"])

    if data.get("statusCode") and data["statusCode"] != 200:
        raise RequestError(
            f"Error requesting data from {url}: {data['statusCode']} {data['message']}"
        )


class Client:
    """Define the client."""

    def __init__(
        self,
        *,
        session: Optional[ClientSession] = None,
        request_timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize."""
        self._request_timeout = request_timeout
        self._session = session
        self.controllers: Dict[str, Controller] = {}

    async def _request(
        self,
        method: str,
        url: str,
        *,
        access_token: Optional[str] = None,
        access_token_expiration: Optional[datetime] = None,
        ssl: bool = True,
        **kwargs: Dict[str, Any],
    ) -> dict:
        """Make a request against the RainMachine device."""
        if access_token_expiration and datetime.now() >= access_token_expiration:
            raise TokenExpiredError("Long-lived access token has expired")

        kwargs.setdefault("headers", {})
        kwargs["headers"]["Content-Type"] = "application/json"

        kwargs.setdefault("params", {})
        if access_token:
            kwargs["params"]["access_token"] = access_token

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        assert session

        try:
            # Only try 2x for ServerDisconnectedError to comply with the RFC
            # https://datatracker.ietf.org/doc/html/rfc2616#section-8.1.4
            for attempt in range(2):
                try:
                    return await self._request_with_session(
                        session, method, url, ssl, **kwargs
                    )
                except ServerDisconnectedError as err:
                    # The HTTP/1.1 spec allows the device to close the connection
                    # at any time. aiohttp raises ServerDisconnectedError to let us
                    # decide what to do. In this case we want to retry as it likely
                    # means the connection was stale and the server closed it on us.
                    if attempt == 0:
                        continue
                    raise RequestError(
                        f"Error requesting data from {url} ({err}))"
                    ) from err

        finally:
            if not use_running_session:
                await session.close()

        assert False, "unreachable"  # https://github.com/python/mypy/issues/8964

    async def _request_with_session(
        self,
        session: ClientSession,
        method: str,
        url: str,
        ssl: bool,
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Make a request with a session."""
        try:
            async with async_timeout.timeout(self._request_timeout), session.request(
                method, url, ssl=ssl, **kwargs
            ) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
                _raise_for_remote_status(url, data)
        except ServerDisconnectedError:
            raise
        except ClientError as err:
            if "401" in str(err):
                raise TokenExpiredError("Long-lived access token has expired") from err
            raise RequestError(f"Error requesting data from {url}") from err
        except asyncio.TimeoutError as err:
            raise RequestError(f"Error requesting data from {url} ({err}))") from err

        _LOGGER.debug("Data received for %s: %s", url, data)
        return cast(Dict[str, Any], data)

    async def load_local(  # pylint: disable=too-many-arguments
        self,
        host: str,
        password: str,
        port: int = DEFAULT_LOCAL_PORT,
        ssl: bool = True,
        skip_existing: bool = True,
    ) -> None:
        """Create a local client."""
        controller: LocalController = LocalController(self._request, host, port, ssl)
        await controller.login(password)

        wifi_data = await controller.provisioning.wifi()
        if skip_existing and wifi_data["macAddress"] in self.controllers:
            return

        version_data = await controller.api.versions()
        controller.api_version = version_data["apiVer"]
        controller.hardware_version = version_data["hwVer"]
        controller.mac = wifi_data["macAddress"]
        controller.name = await controller.provisioning.device_name
        controller.software_version = version_data["swVer"]

        self.controllers[controller.mac] = controller

    async def load_remote(
        self, email: str, password: str, skip_existing: bool = True
    ) -> None:
        """Create a remote client."""
        auth_resp = await self._request(
            "post",
            "https://my.rainmachine.com/login/auth",
            json={"user": {"email": email, "pwd": password, "remember": 1}},
        )

        access_token: str = auth_resp["access_token"]

        sprinklers_resp = await self._request(
            "post",
            "https://my.rainmachine.com/devices/get-sprinklers",
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
            controller.hardware_version = version_data["hwVer"]
            controller.mac = sprinkler["mac"]
            controller.name = sprinkler["name"]
            controller.software_version = version_data["swVer"]

            self.controllers[sprinkler["mac"]] = controller
