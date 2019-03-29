"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import
import asyncio
import json
from datetime import datetime, timedelta

import aiohttp
import asynctest
import pytest

from regenmaschine import Client, login
from regenmaschine.errors import RequestError, TokenExpiredError

from tests.const import (
    TEST_ACCESS_TOKEN, TEST_API_VERSION, TEST_EMAIL, TEST_HOST,
    TEST_HW_VERSION, TEST_MAC, TEST_NAME, TEST_PASSWORD, TEST_PORT,
    TEST_SW_VERSION)
from tests.fixtures import (
    authenticated_client, auth_login_json, unauthenticated_json)
from tests.fixtures.api import apiver_json
from tests.fixtures.provision import provision_name_json, provision_wifi_json


@pytest.mark.asyncio
async def test_legacy_login(authenticated_client, event_loop):
    """Test loading a local client through the legacy method."""
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
async def test_load_local(authenticated_client, event_loop):
    """Test loading a local client."""
    async with authenticated_client:
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)

            assert len(client.controllers) == 1

            controller = client.controllers[TEST_MAC]
            assert controller._access_token == TEST_ACCESS_TOKEN
            assert controller.api_version == TEST_API_VERSION
            assert controller.hardware_version == TEST_HW_VERSION
            assert controller.mac == TEST_MAC
            assert controller.name == TEST_NAME
            assert controller.software_version == TEST_SW_VERSION


@pytest.mark.asyncio
async def test_load_local_skip(
        aresponses, auth_login_json, provision_wifi_json, authenticated_client,
        event_loop):
    """Test skipping the loading of a local client if it's already loaded."""
    authenticated_client.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/auth/login', 'post',
        aresponses.Response(text=json.dumps(auth_login_json), status=200))
    authenticated_client.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision/wifi', 'get',
        aresponses.Response(text=json.dumps(provision_wifi_json), status=200))

    async with authenticated_client:
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)
            controller = client.controllers[TEST_MAC]

            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)
            assert len(client.controllers) == 1
            assert client.controllers[TEST_MAC] == controller


@pytest.mark.asyncio
async def test_load_local_failure(
        aresponses, unauthenticated_json, event_loop):
    """Test loading a local client and receiving some sort of fail response."""
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/auth/login', 'post',
        aresponses.Response(text=json.dumps(unauthenticated_json), status=401))

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)

@pytest.mark.asyncio
async def test_load_remote(authenticated_client, event_loop):
    """Test loading a remote client."""
    async with authenticated_client:
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)

            assert len(client.controllers) == 1

            controller = client.controllers[TEST_MAC]
            assert controller._access_token == TEST_ACCESS_TOKEN
            assert controller.api_version == TEST_API_VERSION
            assert controller.hardware_version == TEST_HW_VERSION
            assert controller.mac == TEST_MAC
            assert controller.name == TEST_NAME
            assert controller.software_version == TEST_SW_VERSION



@pytest.mark.asyncio
async def test_token_expired_exception(authenticated_client, event_loop):
    """Test that the appropriate error is thrown when a token expires."""
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
    """Test whether the client properly raises an error on timeout."""

    async def long_running_login(*args, **kwargs):
        """Define a method that takes 0.5 seconds to execute."""
        await asyncio.sleep(0.5)

    mock_login = mocker.patch('regenmaschine.login')
    mock_login.return_value = long_running_login

    with asynctest.mock.patch.object(aiohttp.ClientResponse, 'json',
                                     long_running_login):
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
