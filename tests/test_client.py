"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import
import json

import aiohttp
import pytest

from regenmaschine import Client
from regenmaschine.errors import RainMachineError, UnauthenticatedError

from .const import TEST_HOST, TEST_MAC, TEST_NAME, TEST_PASSWORD, TEST_PORT
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


async def test_create():
    """Test the manual creation of a client."""
    async with aiohttp.ClientSession() as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        assert client.host == TEST_HOST
        assert client.port == TEST_PORT
        assert client.ssl is False


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

    with pytest.raises(RainMachineError):
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
