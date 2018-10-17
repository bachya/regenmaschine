"""Define a client to interact with a RainMachine unit."""
# pylint: disable=import-error, unused-import
from datetime import datetime, timedelta
from typing import Type, TypeVar, Union  # noqa

from aiohttp import ClientSession, client_exceptions

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

ClientType = TypeVar('ClientType', bound='Client')


class Client:  # pylint: disable=too-many-instance-attributes
    """Define the client."""

    def __init__(
            self, host: str, websession: ClientSession, port: int,
            ssl: bool) -> None:
        """Initialize."""
        self.access_token = None
        self.access_token_expiration = None  # type: Union[None, datetime]
        self.authenticated = False
        self.host = host
        self.mac = None
        self.name = None  # type: Union[None, str]
        self.port = port
        self.refresh_token = None
        self.ssl = ssl
        self.websession = websession

        self.diagnostics = Diagnostics(self.request)
        self.parsers = Parser(self.request)
        self.programs = Program(self.request)
        self.provisioning = Provision(self.request)
        self.restrictions = Restriction(self.request)
        self.stats = Stats(self.request)
        self.watering = Watering(self.request)
        self.zones = Zone(self.request)

    @classmethod
    async def authenticate_via_password(
            cls: Type[ClientType],
            host: str,
            password: str,
            websession: ClientSession,
            *,
            port: int = 8080,
            ssl: bool = True):
        """Instantiate a client with a password."""
        klass = cls(host, websession, port, ssl)
        data = await klass.request(
            'post', 'auth/login', json={
                'pwd': password,
                'remember': 1
            })

        klass.authenticated = True
        klass.access_token = data['access_token']
        klass.access_token_expiration = (
            datetime.now() + timedelta(seconds=int(data['expires_in']) - 10))

        if not (klass.name or klass.mac):
            wifi_data = await klass.provisioning.wifi()
            klass.mac = wifi_data['macAddress']
            klass.name = await klass.provisioning.device_name

        return klass

    async def request(
            self,
            method: str,
            endpoint: str,
            *,
            headers: dict = None,
            params: dict = None,
            json: dict = None) -> dict:
        """Make a request against the RainMachine device."""
        if (self.access_token_expiration
                and datetime.now() >= self.access_token_expiration):
            raise TokenExpiredError('Long-lived access token has expired')

        if not headers:
            headers = {}
        headers.update({'Content-Type': 'application/json'})

        if not params:
            params = {}

        if self.access_token:
            params.update({'access_token': self.access_token})

        try:
            async with self.websession.request(method, '{0}/{1}'.format(
                    API_URL_SCAFFOLD.format(self.host, self.port),
                    endpoint), headers=headers, params=params, json=json,
                                               ssl=self.ssl) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
                return data
        except client_exceptions.ClientError as err:
            raise RequestError(
                'Error requesting data from {}: {}'.format(self.host, err))
