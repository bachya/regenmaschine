"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import
import asyncio
import json
from datetime import datetime, timedelta

import aiohttp
import asynctest
import pytest

from regenmaschine import login
from regenmaschine.errors import RequestError, TokenExpiredError

from .const import (
    TEST_ACCESS_TOKEN, TEST_API_VERSION, TEST_HOST, TEST_HW_VERSION, TEST_MAC,
    TEST_NAME, TEST_PASSWORD, TEST_PORT, TEST_SW_VERSION)
from .fixtures import (
    authenticated_client, auth_login_json, unauthenticated_json)
from .fixtures.api import apiver_json
from .fixtures.provision import provision_name_json, provision_wifi_json


@pytest.mark.asyncio
async def test_authentication_success(authenticated_client, event_loop):
    """Test successfully retrieving a long-lived access token."""
    async with authenticated_client:
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            assert client._access_token == TEST_ACCESS_TOKEN
            assert client.api_version == TEST_API_VERSION
            assert client.hardware_version == TEST_HW_VERSION
            assert client.mac == TEST_MAC
            assert client.name == TEST_NAME
            assert client.software_version == TEST_SW_VERSION


@pytest.mark.asyncio
async def test_authentication_failure(
        aresponses, unauthenticated_json, event_loop):
    """Test authenticating the device."""
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/auth/login', 'post',
        aresponses.Response(text=json.dumps(unauthenticated_json), status=401))

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)


@pytest.mark.asyncio
async def test_token_expired_exception(authenticated_client, event_loop):
    """Test authenticating the device."""
    async with authenticated_client:
        with pytest.raises(TokenExpiredError):
            async with aiohttp.ClientSession(loop=event_loop) as websession:
                client = await login(
                    TEST_HOST,
                    TEST_PASSWORD,
                    websession,
                    port=TEST_PORT,
                    ssl=False)

                client._access_token_expiration = datetime.now() - timedelta(
                    hours=1)
                await client._request('get', 'random/endpoint')


@pytest.mark.asyncio
async def test_request_timeout(authenticated_client, event_loop, mocker):
    """Test authenticating the device."""

    async def long_running_login(*args, **kwargs):
        """Define a method that takes 20 seconds to execute."""
        await asyncio.sleep(0.5)

    mock_login = mocker.patch('regenmaschine.login')
    mock_login.return_value = long_running_login

    with asynctest.mock.patch.object(aiohttp.ClientResponse,
                                     'json', long_running_login):
        async with authenticated_client:
            async with aiohttp.ClientSession(loop=event_loop) as websession:
                with pytest.raises(RequestError):
                    await login(
                        TEST_HOST,
                        TEST_PASSWORD,
                        websession,
                        port=TEST_PORT,
                        ssl=False,
                        request_timeout=0.1)
