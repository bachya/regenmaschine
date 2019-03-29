"""Define a client to interact with a RainMachine unit."""
import asyncio
from datetime import datetime
from typing import Dict

import async_timeout
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from regenmaschine.controller import Controller, LocalController
from regenmaschine.errors import RequestError, TokenExpiredError

DEFAULT_LOCAL_PORT = 8080
DEFAULT_TIMEOUT = 10


class Client:  # pylint: disable=too-few-public-methods
    """Define the client."""

    def __init__(
            self,
            websession: ClientSession,
            request_timeout: int = DEFAULT_TIMEOUT) -> None:
        """Initialize."""
        self._websession = websession
        self.controllers = {}  # type: Dict[str, Controller]
        self.request_timeout = request_timeout

    async def load_local(  # pylint: disable=too-many-arguments
            self,
            host: str,
            password: str,
            port: int = DEFAULT_LOCAL_PORT,
            ssl: bool = True) -> None:
        """Create a local client."""
        controller = LocalController(
            self._request, host, port, ssl, self._websession)
        await controller.login(password)
        self.controllers[controller.mac] = controller  # type: ignore

    async def _request(
            self,
            method: str,
            url: str,
            *,
            access_token: str = None,
            access_token_expiration: datetime = None,
            headers: dict = None,
            params: dict = None,
            json: dict = None,
            ssl: bool = True) -> dict:
        """Make a request against the RainMachine device."""
        if (access_token_expiration
                and datetime.now() >= access_token_expiration):
            raise TokenExpiredError('Long-lived access token has expired')

        if not headers:
            headers = {}
        headers.update({'Content-Type': 'application/json'})

        if not params:
            params = {}
        if access_token:
            params.update({'access_token': access_token})

        try:
            async with async_timeout.timeout(self.request_timeout):
                async with self._websession.request(
                        method, url, headers=headers, params=params, json=json,
                        ssl=ssl) as resp:
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
        request_timeout: int = DEFAULT_TIMEOUT) -> Controller:
    """Authenticate against a RainMachine device."""
    print('regenmaschine.client.login() is deprecated; see documentation!')
    client = Client(websession, request_timeout)
    await client.load_local(host, password, port, ssl)
    return next(iter(client.controllers.values()))
