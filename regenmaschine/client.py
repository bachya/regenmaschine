"""Define a client to interact with a RainMachine hub."""
import datetime

from aiohttp import ClientSession, client_exceptions

from .errors import ExpiredTokenError, RequestError, UnauthenticatedError
from .diagnostics import Diagnostics
from .parser import Parser
from .program import Program
from .provision import Provision
from .restriction import Restriction
from .stats import Stats
from .watering import Watering
from .zone import Zone

API_VERSION = '4'


class Client(object):  # pylint: disable=too-many-instance-attributes
    """Define the client."""

    def __init__(self,
                 host: str,
                 websession: ClientSession,
                 *,
                 mac: str = None,
                 name: str = None,
                 port: int = 8080,
                 ssl: bool = True) -> None:
        """Initialize."""
        self._access_token = None
        self._access_token_expiration = None  # type: datetime.datetime
        self._authenticated = False
        self.host = host
        self.mac = mac
        self.name = name
        self.port = port
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

    async def authenticate(self, passwd: str) -> None:
        """Authenticate against the RainMachine device."""
        json = {'pwd': passwd, 'remember': 1}
        data = await self.request('post', 'auth/login', json=json, auth=False)
        self._authenticated = True
        self._access_token = data['access_token']
        self._access_token_expiration = (
            datetime.datetime.now() +
            datetime.timedelta(seconds=data['expires_in']))

    async def request(self,
                      method: str,
                      endpoint: str,
                      *,
                      headers: dict = None,
                      params: dict = None,
                      json: dict = None,
                      auth: bool = True) -> dict:
        """Make a request against the RainMachine device."""
        url = 'https://{0}:{1}/api/{2}/{3}'.format(self.host, self.port,
                                                   API_VERSION, endpoint)

        if auth and not self._authenticated:
            raise UnauthenticatedError('You must authenticate first!')

        if auth and datetime.datetime.now() > self._access_token_expiration:
            raise ExpiredTokenError('Your token is expired; re-authenticate!')

        if not headers:
            headers = {}
        headers.update({'Content-Type': 'application/json'})

        if not params:
            params = {}
        if auth:
            params.update({'access_token': self._access_token})

        try:
            async with self.websession.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=json,
                    ssl=self.ssl) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
                return data
        except client_exceptions.ClientError as err:
            raise RequestError('Error requesting data from {}: {}'.format(
                self.host, err)) from None
