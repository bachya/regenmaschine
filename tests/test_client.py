"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import

import asyncio
import json

import aiohttp
import pytest

from regenmaschine import Client, scan
from regenmaschine.discovery import DEFAULT_TIMEOUT
from regenmaschine.errors import (
    DiscoveryFailedError, RequestError, UnauthenticatedError)

from .const import (
    TEST_HOST, TEST_MAC, TEST_NAME, TEST_PASSWORD, TEST_PORT, TEST_URL)
from .test_provisioning import fixture_device_name, fixture_wifi  # noqa


@pytest.fixture(scope='module')
def authentication_failure():
    """Return a failed authentication response."""
    return {"statusCode": 2, "message": "Not Authenticated !"}


@pytest.fixture(scope='module')
def authentication_success():
    """Return a successful authentication response."""
    return {
        "access_token": "12345",
        "checksum": "98765",
        "expires_in": 157680000,
        "expiration": "Tue, 06 Jun 2023 02:17:46 GMT",
        "statusCode": 0
    }


async def endpoint_receive_data(data):
    """Stub a simple return from UDP discovery."""
    return data, (TEST_HOST, TEST_PORT)


async def endpoint_timeout():
    """Stub a simple return from UDP discovery."""
    return await asyncio.sleep(DEFAULT_TIMEOUT + 1)


async def test_create():
    """Test the manual creation of a client."""
    async with aiohttp.ClientSession() as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        assert client.host == TEST_HOST
        assert client.port == TEST_PORT
        assert client.ssl is False


@pytest.mark.asyncio
async def test_discovery_success(event_loop, mocker):
    """Test the creation of a client via discovery."""
    mock_endpoint_send = mocker.patch('regenmaschine.udp.LocalEndpoint.send')
    mock_endpoint_send.return_value = None
    mock_endpoint_recv = mocker.patch(
        'regenmaschine.udp.LocalEndpoint.receive')
    mock_endpoint_recv.return_value = endpoint_receive_data(
        '||{0}||{1}||{2}||{3}||{4}||'.format(
            'SPRINKLER', TEST_MAC, TEST_NAME, TEST_URL, 1).encode())

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await scan(websession)
        assert client.host == TEST_HOST
        assert client.mac == TEST_MAC
        assert client.name == TEST_NAME
        assert client.port == TEST_PORT


@pytest.mark.asyncio
async def test_discovery_failure_type(event_loop, mocker):
    """Test discovery failing to find a valid sprinkler (amid others)."""
    mock_endpoint_send = mocker.patch('regenmaschine.udp.LocalEndpoint.send')
    mock_endpoint_send.return_value = None
    mock_endpoint_recv = mocker.patch(
        'regenmaschine.udp.LocalEndpoint.receive')
    mock_endpoint_recv.return_value = endpoint_receive_data(
        '||{0}||{1}||{2}||{3}||{4}||'.format(
            'PONY', TEST_MAC, TEST_NAME, TEST_URL, 1).encode())

    with pytest.raises(DiscoveryFailedError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            await scan(websession)


@pytest.mark.asyncio
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


@pytest.mark.asyncio  # noqa
async def test_authentication_success(
        aresponses, authentication_success, fixture_device_name, event_loop,
        fixture_wifi):
    """Test authenticating the device."""
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/auth/login', 'post',
        aresponses.Response(
            text=json.dumps(authentication_success), status=200))
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision/name', 'get',
        aresponses.Response(text=json.dumps(fixture_device_name), status=200))
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision/wifi', 'get',
        aresponses.Response(text=json.dumps(fixture_wifi), status=200))

    # pylint: disable=protected-access
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        await client.authenticate(TEST_PASSWORD)
        assert client._access_token == '12345'
        assert client.name == TEST_NAME
        assert client.mac == TEST_MAC


@pytest.mark.asyncio
async def test_authentication_failure(
        aresponses, authentication_failure, event_loop):
    """Test authenticating the device."""
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/auth/login', 'post',
        aresponses.Response(
            text=json.dumps(authentication_failure), status=401))

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
            await client.authenticate(TEST_PASSWORD)


@pytest.mark.asyncio
async def test_unauthenticated_request(event_loop):
    """Test authenticating the device."""
    with pytest.raises(UnauthenticatedError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
            await client.request('get', '/bad_endpoint')
