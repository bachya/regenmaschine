"""Define a client to interact with a RainMachine unit."""
# pylint: disable=import-error,too-few-public-methods
# pylint: disable=too-many-instance-attributes,unused-import
from datetime import datetime, timedelta
from typing import Union  # noqa

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from .errors import RequestError, TokenExpiredError
from .diagnostics import Diagnostics
from .parser import Parser
from .program import Program
from .provision import Provision
from .restriction import Restriction
from .stats import Stats
from .watering import Watering
from .zone import Zone

API_URL_SCAFFOLD = 'https://{0}:{1}/api/4'


class Client:
    """Define the client."""

    def __init__(
            self, host: str, websession: ClientSession, port: int,
            ssl: bool) -> None:
        """Initialize."""
        self._access_token = None
        self._access_token_expiration = None  # type: Union[None, datetime]
        self._host = host
        self._port = port
        self._ssl = ssl
        self._websession = websession
        self.mac = None
        self.name = None  # type: Union[None, str]

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

        try:
            async with self._websession.request(method, '{0}/{1}'.format(
                    API_URL_SCAFFOLD.format(self._host, self._port),
                    endpoint), headers=headers, params=params, json=json,
                                                ssl=self._ssl) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
                return data
        except ClientError as err:
            raise RequestError(
                'Error requesting data from {}: {}'.format(self._host, err))

    async def authenticate(self, password: str):
        """Instantiate a client with a password."""
        data = await self._request(
            'post', 'auth/login', json={
                'pwd': password,
                'remember': 1
            })

        self._access_token = data['access_token']
        self._access_token_expiration = (
            datetime.now() + timedelta(seconds=int(data['expires_in']) - 10))

        wifi_data = await self.provisioning.wifi()
        self.mac = wifi_data['macAddress']
        self.name = await self.provisioning.device_name


async def login(
        host: str,
        password: str,
        websession: ClientSession,
        *,
        port: int = 8080,
        ssl: bool = True) -> Client:
    """Authenticate against a RainMachine device."""
    client = Client(host, websession, port, ssl)
    await client.authenticate(password)
    return client
