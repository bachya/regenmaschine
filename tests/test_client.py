"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import
import json
from datetime import datetime, timedelta

import aiohttp
import pytest

from regenmaschine import Client
from regenmaschine.errors import RequestError, TokenExpiredError

from .const import (
    TEST_ACCESS_TOKEN, TEST_HOST, TEST_MAC, TEST_NAME, TEST_PASSWORD,
    TEST_PORT)
from .fixtures import (
    authenticated_client, auth_login_json, auth_totp_json,
    unauthenticated_json)
from .fixtures.provisioning import (
    provisioning_name_json, provisioning_wifi_json)


@pytest.mark.asyncio
async def test_authentication_success(authenticated_client, event_loop):
    """Test successfully retrieving a long-lived access token."""
    async with authenticated_client:
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await Client.authenticate_via_password(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            assert client.access_token == TEST_ACCESS_TOKEN
            assert client.name == TEST_NAME
            assert client.mac == TEST_MAC


@pytest.mark.asyncio
async def test_authentication_failure(
        aresponses, unauthenticated_json, event_loop):
    """Test authenticating the device."""
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/auth/login', 'post',
        aresponses.Response(text=json.dumps(unauthenticated_json), status=401))

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            await Client.authenticate_via_password(
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
                client = await Client.authenticate_via_password(
                    TEST_HOST,
                    TEST_PASSWORD,
                    websession,
                    port=TEST_PORT,
                    ssl=False)

                client.access_token_expiration = datetime.now() - timedelta(
                    hours=1)
                await client.request('get', 'random/endpoint')
