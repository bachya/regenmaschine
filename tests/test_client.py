"""Define tests for the client object."""
import asyncio
from typing import Tuple

import aiohttp
import aresponses
import pytest

from regenmaschine import Client, scan
from regenmaschine.discovery import DEFAULT_TIMEOUT
from regenmaschine.errors import DiscoveryFailedError

TEST_HOST = '192.168.1.100'
TEST_MAC = 'ab:cd:ef:12:34:56'
TEST_NAME = 'My House'
TEST_PORT = 8081
TEST_URL = 'https://{0}:{1}'.format(TEST_HOST, TEST_PORT)


async def endpoint_receive_data(data: bytes) -> Tuple[bytes, Tuple[str, int]]:
    """Stub a simple return from UDP discovery."""
    return data, (TEST_HOST, TEST_PORT)


async def endpoint_timeout() -> None:
    """Stub a simple return from UDP discovery."""
    return await asyncio.sleep(DEFAULT_TIMEOUT + 1)


async def test_manual() -> None:
    """Test the manual creation of a client."""
    async with aiohttp.ClientSession() as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        assert client.host == TEST_HOST
        assert client.port == TEST_PORT
        assert client.ssl is False


async def test_discovery_success(event_loop, mocker):
    """Test the creation of a client via discovery."""
    mock_endpoint_send = mocker.patch('regenmaschine.udp.LocalEndpoint.send')
    mock_endpoint_send.return_value = None
    mock_endpoint_recv = mocker.patch(
        'regenmaschine.udp.LocalEndpoint.receive')
    mock_endpoint_recv.return_value = endpoint_receive_data(
        '||{0}||{1}||{2}||{3}||{4}||'.format('SPRINKLER', TEST_MAC, TEST_NAME,
                                             TEST_URL, 1).encode())

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await scan(websession)
        assert client.host == TEST_HOST
        assert client.mac == TEST_MAC
        assert client.name == TEST_NAME
        assert client.port == TEST_PORT


async def test_discovery_failure_type(event_loop, mocker):
    """Test discovery failing to find a valid sprinkler (amid others)."""
    mock_endpoint_send = mocker.patch('regenmaschine.udp.LocalEndpoint.send')
    mock_endpoint_send.return_value = None
    mock_endpoint_recv = mocker.patch(
        'regenmaschine.udp.LocalEndpoint.receive')
    mock_endpoint_recv.return_value = endpoint_receive_data(
        '||{0}||{1}||{2}||{3}||{4}||'.format('PONY', TEST_MAC, TEST_NAME,
                                             TEST_URL, 1).encode())

    with pytest.raises(DiscoveryFailedError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            await scan(websession)


async def test_discovery_failure_timeout(event_loop, mocker):
    """Test discovery timing out."""
    mock_endpoint_send = mocker.patch('regenmaschine.udp.LocalEndpoint.send')
    mock_endpoint_send.return_value = None
    mock_endpoint_recv = mocker.patch(
        'regenmaschine.udp.LocalEndpoint.receive')
    mock_endpoint_recv.return_value = endpoint_timeout()

    with pytest.raises(DiscoveryFailedError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            await scan(websession)
