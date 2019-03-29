"""Define a client to interact with a RainMachine unit."""
# pylint: disable=protected-access,too-few-public-methods
# pylint: disable=too-many-instance-attributes
import asyncio
from datetime import datetime, timedelta
from typing import Optional  # pylint: disable=unused-import

import async_timeout
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from regenmaschine.api import API
from regenmaschine.errors import RequestError, TokenExpiredError
from regenmaschine.diagnostics import Diagnostics
from regenmaschine.parser import Parser
from regenmaschine.program import Program
from regenmaschine.provision import Provision
from regenmaschine.restriction import Restriction
from regenmaschine.stats import Stats
from regenmaschine.watering import Watering
from regenmaschine.zone import Zone

DEFAULT_LOCAL_PORT = 8080
DEFAULT_TIMEOUT = 10


class Client:
    """Define the client."""

    def __init__(
            self, websession: ClientSession, request_timeout: int) -> None:
        """Initialize."""
        self._access_token = None
        self._access_token_expiration = None  # type: Optional[datetime]
        self._request_timeout = request_timeout
        self._ssl = True
        self._url_base = None  # type: Optional[str]
        self._websession = websession
        self.api_version = None  # type: Optional[str]
        self.hardware_version = None  # type: Optional[int]
        self.mac = None
        self.name = None  # type: Optional[str]
        self.software_version = None  # type: Optional[str]

        self.api = API(self._request)
        self.diagnostics = Diagnostics(self._request)
        self.parsers = Parser(self._request)
        self.programs = Program(self._request)
        self.provisioning = Provision(self._request)
        self.restrictions = Restriction(self._request)
        self.stats = Stats(self._request)
        self.watering = Watering(self._request)
        self.zones = Zone(self._request)

    @classmethod
    async def create_local(  # pylint: disable=too-many-arguments
            cls,
            host: str,
            password: str,
            websession: ClientSession,
            port: int = DEFAULT_LOCAL_PORT,
            ssl: bool = True,
            request_timeout: int = DEFAULT_TIMEOUT) -> 'Client':
        """Create a local client."""
        klass = cls(websession, request_timeout)
        klass._url_base = 'https://{0}:{1}/api/4'.format(host, port)
        klass._ssl = ssl

        auth_resp = await klass._request(
            'post', 'auth/login', json={
                'pwd': password,
                'remember': 1
            })
        klass._access_token = auth_resp['access_token']
        klass._access_token_expiration = (
            datetime.now() +
            timedelta(seconds=int(auth_resp['expires_in']) - 10))

        wifi_data = await klass.provisioning.wifi()
        klass.mac = wifi_data['macAddress']
        klass.name = await klass.provisioning.device_name

        version_data = await klass.api.versions()
        klass.api_version = version_data['apiVer']
        klass.hardware_version = version_data['hwVer']
        klass.software_version = version_data['swVer']

        return klass

    async def _request(
            self,
            method: str,
            endpoint: str,
            *,
            headers: dict = None,
            params: dict = None,
            json: dict = None) -> dict:
        """Make a request against the RainMachine device."""
        if (self._access_token_expiration
                and datetime.now() >= self._access_token_expiration):
            raise TokenExpiredError('Long-lived access token has expired')

        if not headers:
            headers = {}
        headers.update({'Content-Type': 'application/json'})

        if not params:
            params = {}
        if self._access_token:
            params.update({'access_token': self._access_token})

        url = '{0}/{1}'.format(self._url_base, endpoint)

        try:
            async with async_timeout.timeout(self._request_timeout):
                async with self._websession.request(
                        method, url, headers=headers, params=params, json=json,
                        ssl=self._ssl) as resp:
                    resp.raise_for_status()
                    data = await resp.json(content_type=None)
        except ClientError as err:
            raise RequestError(
                'Error requesting data from {0}: {1}'.format(url, err))
        except asyncio.TimeoutError:
            raise RequestError('Timeout during request: {0}'.format(url))

        return data


async def login(
        host: str,
        password: str,
        websession: ClientSession,
        *,
        port: int = 8080,
        ssl: bool = True,
        request_timeout: int = DEFAULT_TIMEOUT) -> Client:
    """Authenticate against a RainMachine device."""
    print('regenmaschine.client.login() is deprecated; see documentation!')
    client = await Client.create_local(
        host, password, websession, port, ssl, request_timeout)
    return client
