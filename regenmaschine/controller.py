"""Define a RainMachine controller class."""
# pylint: disable=too-few-public-methods,too-many-instance-attributes
from datetime import datetime, timedelta
from typing import Awaitable, Callable, Optional

from aiohttp import ClientSession

from regenmaschine.api import API
from regenmaschine.diagnostics import Diagnostics
from regenmaschine.parser import Parser
from regenmaschine.program import Program
from regenmaschine.provision import Provision
from regenmaschine.restriction import Restriction
from regenmaschine.stats import Stats
from regenmaschine.watering import Watering
from regenmaschine.zone import Zone

URL_BASE_LOCAL = "https://{0}:{1}/api/4"
URL_BASE_REMOTE = "https://api.rainmachine.com/{0}/api/4"


class Controller:  # pylint: disable=too-many-instance-attributes
    """Define the controller."""

    def __init__(
        self, request: Callable[..., Awaitable[dict]], websession: ClientSession
    ) -> None:
        """Initialize."""
        self._access_token = None  # type: Optional[str]
        self._access_token_expiration = None  # type: Optional[datetime]
        self._client_request = request
        self._host = None  # type: Optional[str]
        self._ssl = True
        self._websession = websession
        self.api_version = None  # type: Optional[str]
        self.hardware_version = None  # type: Optional[int]
        self.mac = None
        self.name = None  # type: Optional[str]
        self.software_version = None  # type: Optional[str]

        # API endpoints:
        self.api = API(self._request)
        self.diagnostics = Diagnostics(self._request)
        self.parsers = Parser(self._request)
        self.programs = Program(self._request)
        self.provisioning = Provision(self._request)
        self.restrictions = Restriction(self._request)
        self.stats = Stats(self._request)
        self.watering = Watering(self._request)
        self.zones = Zone(self._request)

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        headers: dict = None,
        params: dict = None,
        json: dict = None,
        ssl: bool = True
    ) -> dict:
        """Wrap the generic request method to add access token, etc."""
        return await self._client_request(
            method,
            "{0}/{1}".format(self._host, endpoint),
            access_token=self._access_token,
            access_token_expiration=self._access_token_expiration,
            headers=headers,
            params=params,
            json=json,
            ssl=ssl,
        )


class LocalController(Controller):
    """Define a controller accessed over the LAN."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        request: Callable[..., Awaitable[dict]],
        host: str,
        port: int,
        ssl: bool,
        websession: ClientSession,
    ) -> None:
        """Initialize."""
        super().__init__(request, websession)

        self._host = URL_BASE_LOCAL.format(host, port)
        self._ssl = ssl

    async def login(self, password):
        """Authenticate against the device (locally)."""
        auth_resp = await self._client_request(
            "post",
            "{0}/auth/login".format(self._host),
            json={"pwd": password, "remember": 1},
        )

        self._access_token = auth_resp["access_token"]
        self._access_token_expiration = datetime.now() + timedelta(
            seconds=int(auth_resp["expires_in"]) - 10
        )


class RemoteController(Controller):
    """Define a controller accessed over RainMachine's cloud."""

    async def login(
        self, stage_1_access_token: str, sprinkler_id: str, password: str
    ) -> None:
        """Authenticate against the device (remotely)."""
        auth_resp = await self._client_request(
            "post",
            "https://my.rainmachine.com/devices/login-sprinkler",
            access_token=stage_1_access_token,
            json={"sprinklerId": sprinkler_id, "pwd": password},
        )

        self._access_token = auth_resp["access_token"]
        self._host = URL_BASE_REMOTE.format(sprinkler_id)
