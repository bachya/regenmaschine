"""Define a client to interact with a RainMachine unit."""
import asyncio
from datetime import datetime
import logging
from typing import Dict, Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
import async_timeout

from regenmaschine.controller import Controller, LocalController, RemoteController
from regenmaschine.errors import RequestError, TokenExpiredError, raise_remote_error

_LOGGER: logging.Logger = logging.getLogger(__name__)

DEFAULT_LOCAL_PORT: int = 8080
DEFAULT_TIMEOUT: int = 30


def _raise_for_remote_status(url: str, data: dict) -> None:
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
        self._session: ClientSession = session
        self.controllers: Dict[str, Controller] = {}
        self.request_timeout: int = request_timeout

    async def load_local(  # pylint: disable=too-many-arguments
        self,
        host: str,
        password: str,
        port: int = DEFAULT_LOCAL_PORT,
        ssl: bool = True,
        skip_existing: bool = True,
    ) -> None:
        """Create a local client."""
        controller: LocalController = LocalController(self.request, host, port, ssl)
        await controller.login(password)

        wifi_data: dict = await controller.provisioning.wifi()
        if skip_existing and wifi_data["macAddress"] in self.controllers:
            return

        version_data: dict = await controller.api.versions()
        controller.api_version = version_data["apiVer"]
        controller.hardware_version = version_data["hwVer"]
        controller.mac = wifi_data["macAddress"]
        controller.name = await controller.provisioning.device_name
        controller.software_version = version_data["swVer"]

        self.controllers[controller.mac] = controller  # type: ignore

    async def load_remote(
        self, email: str, password: str, skip_existing: bool = True
    ) -> None:
        """Create a remote client."""
        auth_resp: dict = await self.request(
            "post",
            "https://my.rainmachine.com/login/auth",
            json={"user": {"email": email, "pwd": password, "remember": 1}},
        )

        access_token: str = auth_resp["access_token"]

        sprinklers_resp: dict = await self.request(
            "post",
            "https://my.rainmachine.com/devices/get-sprinklers",
            access_token=access_token,
            json={"user": {"email": email, "pwd": password, "remember": 1}},
        )

        for sprinkler in sprinklers_resp["sprinklers"]:
            if skip_existing and sprinkler["mac"] in self.controllers:
                continue

            controller: RemoteController = RemoteController(self.request)
            await controller.login(access_token, sprinkler["sprinklerId"], password)

            version_data: dict = await controller.api.versions()
            controller.api_version = version_data["apiVer"]
            controller.hardware_version = version_data["hwVer"]
            controller.mac = sprinkler["mac"]
            controller.name = sprinkler["name"]
            controller.software_version = version_data["swVer"]

            self.controllers[sprinkler["mac"]] = controller

    async def request(
        self,
        method: str,
        url: str,
        *,
        access_token: Optional[str] = None,
        access_token_expiration: Optional[datetime] = None,
        ssl: bool = True,
        **kwargs,
    ) -> dict:
        """Make a request against the RainMachine device."""
        if access_token_expiration and datetime.now() >= access_token_expiration:
            raise TokenExpiredError("Long-lived access token has expired")

        kwargs.setdefault("headers", {})
        kwargs["headers"]["Connection"] = "close"
        kwargs["headers"]["Content-Type"] = "application/json"

        kwargs.setdefault("params", {})
        if access_token:
            kwargs["params"]["access_token"] = access_token

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with async_timeout.timeout(self.request_timeout):
                async with session.request(method, url, ssl=ssl, **kwargs) as resp:
                    resp.raise_for_status()
                    data = await resp.json(content_type=None)
                    _raise_for_remote_status(url, data)
        except ClientError as err:
            if "401" in str(err):
                raise TokenExpiredError("Long-lived access token has expired") from err
            raise RequestError(f"Error requesting data from {url}") from err
        except asyncio.TimeoutError as err:
            raise RequestError(f"Timeout during request: {url}") from err
        finally:
            if not use_running_session:
                await session.close()

        return data
