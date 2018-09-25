"""Define the ability to discover RainMachine devices on the network."""
# pylint: disable=import-error, unused-import

import asyncio
import logging
from typing import List, Tuple  # noqa
from urllib.parse import urlparse

from aiohttp import ClientSession

from .client import Client
from .errors import DiscoveryFailedError
from .udp import open_local_endpoint

_LOGGER = logging.getLogger(__name__)

DEFAULT_BROADCAST_ADDRESS = '192.168.1.255'
DEFAULT_BROADCAST_PORT = 15800
DEFAULT_RECEIVE_PORT = 15900
DEFAULT_TIMEOUT = 5


async def scan(websession: ClientSession) -> Client:
    """Scan the local network for any RainMachine instances."""
    local = await open_local_endpoint('0.0.0.0', DEFAULT_RECEIVE_PORT)
    local.send(
        b'RainMachine Discovery',
        (DEFAULT_BROADCAST_ADDRESS, DEFAULT_BROADCAST_PORT))

    try:
        data, _ = await asyncio.wait_for(
            local.receive(), timeout=DEFAULT_TIMEOUT)
        local.close()

        data_parts = list(
            filter(None, data.decode().split('|')))  # type: List[Tuple]

        kind, mac, name, url, _ = data_parts
        if kind != 'SPRINKLER':
            raise DiscoveryFailedError('No valid RainMachine units found')

        scheme, netloc, _, _, _, _ = urlparse(url)  # type: ignore
        host, port = netloc.split(':')
        return Client(  # type: ignore
            host,
            websession,
            mac=mac,
            name=name,
            port=int(port),
            ssl=bool(scheme == 'https'))
    except asyncio.TimeoutError:
        raise DiscoveryFailedError('No valid RainMachine units found')
