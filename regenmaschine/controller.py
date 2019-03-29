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

URL_BASE_LOCAL = 'https://{0}:{1}/api/4'


class Controller:
    """Define the controller."""

    def __init__(  # pylint: disable=too-many-arguments
            self, request: Callable[..., Awaitable[dict]], host: str,
            port: int, ssl: bool, websession: ClientSession) -> None:
        """Initialize."""
        self._access_token = None  # type: Optional[str]
        self._access_token_expiration = None  # type: Optional[datetime]
        self._client_request = request
        self._port = port
        self._ssl = ssl
        self._websession = websession
        self.api_version = None  # type: Optional[str]
        self.hardware_version = None  # type: Optional[int]
        self.host = host
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
            ssl: bool = True) -> dict:
        """Wrap the generic request method to add access token, etc."""
        return await self._client_request(
            method,
            '{0}/{1}'.format(
                URL_BASE_LOCAL.format(self.host, self._port), endpoint),
            access_token=self._access_token,
            access_token_expiration=self._access_token_expiration,
            headers=headers,
            params=params,
            json=json,
            ssl=ssl)

    async def _save_device_info(self):
        """Save various device properties."""
        wifi_data = await self.provisioning.wifi()
        self.mac = wifi_data['macAddress']
        self.name = await self.provisioning.device_name

        version_data = await self.api.versions()
        self.api_version = version_data['apiVer']
        self.hardware_version = version_data['hwVer']
        self.software_version = version_data['swVer']


class LocalController(Controller):  # pylint: disable=too-few-public-methods
    """Define a controller accessed over the LAN."""

    async def login(self, password):
        """Perform post-creation initialization of the object."""
        auth_resp = await self._client_request(
            'post',
            'https://{0}:{1}/api/4/auth/login'.format(self.host, self._port),
            json={
                'pwd': password,
                'remember': 1
            })

        self._access_token = auth_resp['access_token']
        self._access_token_expiration = datetime.now() + timedelta(
            seconds=int(auth_resp['expires_in']) - 10)

        await self._save_device_info()
