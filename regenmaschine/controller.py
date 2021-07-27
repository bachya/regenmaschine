"""Define a RainMachine controller class."""
# pylint: disable=too-few-public-methods,too-many-instance-attributes
from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Dict, Optional

from regenmaschine.api import API
from regenmaschine.diagnostics import Diagnostics
from regenmaschine.parser import Parser
from regenmaschine.program import Program
from regenmaschine.provision import Provision
from regenmaschine.restriction import Restriction
from regenmaschine.stats import Stats
from regenmaschine.watering import Watering
from regenmaschine.zone import Zone

URL_BASE_LOCAL: str = "https://{0}:{1}/api/4"
URL_BASE_REMOTE: str = "https://api.rainmachine.com/{0}/api/4"


class Controller:  # pylint: disable=too-many-instance-attributes
    """Define the controller."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._access_token: Optional[str] = None
        self._access_token_expiration: Optional[datetime] = None
        self._client_request = request
        self._host: str = ""
        self._ssl = True
        self.api_version: str = ""
        self.hardware_version: int = 0
        self.mac: str = ""
        self.name: str = ""
        self.software_version: str = ""

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
        self, method: str, endpoint: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Wrap the generic request method to add access token, etc."""
        return await self._client_request(
            method,
            f"{self._host}/{endpoint}",
            access_token=self._access_token,
            access_token_expiration=self._access_token_expiration,
            ssl=self._ssl,
            **kwargs,
        )


class LocalController(Controller):
    """Define a controller accessed over the LAN."""

    def __init__(  # pylint: disable=too-many-arguments
        self, request: Callable[..., Awaitable[dict]], host: str, port: int, ssl: bool
    ) -> None:
        """Initialize."""
        super().__init__(request)

        self._host = URL_BASE_LOCAL.format(host, port)
        self._ssl = ssl

    async def login(self, password: str) -> None:
        """Authenticate against the device (locally)."""
        auth_resp = await self._client_request(
            "post", f"{self._host}/auth/login", json={"pwd": password, "remember": 1}
        )

        self._access_token: str = auth_resp["access_token"]
        self._access_token_expiration: datetime = datetime.now() + timedelta(
            seconds=int(auth_resp["expires_in"]) - 10
        )


class RemoteController(Controller):
    """Define a controller accessed over RainMachine's cloud."""

    async def login(
        self, stage_1_access_token: str, sprinkler_id: str, password: str
    ) -> None:
        """Authenticate against the device (remotely)."""
        auth_resp: dict = await self._client_request(
            "post",
            "https://my.rainmachine.com/devices/login-sprinkler",
            access_token=stage_1_access_token,
            json={"sprinklerId": sprinkler_id, "pwd": password},
        )

        self._access_token = auth_resp["access_token"]
        self._host = URL_BASE_REMOTE.format(sprinkler_id)
