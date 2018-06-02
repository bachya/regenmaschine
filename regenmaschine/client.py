"""Define a client to interact with a RainMachine hub."""
import datetime

from aiohttp import ClientSession, client_exceptions

from .errors import RequestError
from .program import Program

API_VERSION = '4'


class Client(object):  # pylint: disable=too-many-instance-attributes
    """Define the client."""

    def __init__(self,
                 host: str,
                 websession: ClientSession,
                 *,
                 port: int = 8080,
                 ssl: bool = True) -> None:
        """Initialize."""
        self._access_token = None
        self._access_token_expiration = None  # type: datetime
        self._authenticated = False
        self.host = host
        self.port = port
        self.ssl = ssl
        self.websession = websession

        self.diagnostics = None
        self.parsers = None
        self.programs = None  # type: Program
        self.provision = None
        self.restrictions = None
        self.stats = None
        self.watering = None
        self.zones = None

    async def authenticate(self, passwd: str) -> None:
        """Authenticate against the RainMachine device."""
        json = {'pwd': passwd, 'remember': 1}
        data = await self.request('post', 'auth/login', json=json)
        self._access_token = data['access_token']
        self._access_token_expiration = (
            datetime.datetime.now() +
            datetime.timedelta(seconds=data['expires_in']))

        self.programs = Program(self.request)

    async def request(self, method: str, endpoint: str, *,
                      json: dict = None) -> dict:
        """Make a request against the RainMachine device."""
        url = 'https://{0}:{1}/api/{2}/{3}'.format(self.host, self.port,
                                                   API_VERSION, endpoint)

        try:
            headers = {'Content-Type': 'application/json'}
            async with self.websession.request(
                    method, url, headers=headers, json=json,
                    ssl=self.ssl) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
                return data
        except client_exceptions.ClientError as err:
            raise RequestError('Error requesting data from {}: {}'.format(
                self.host, err)) from None
