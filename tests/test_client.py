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
    TEST_ACCESS_TOKEN,
    TEST_API_VERSION,
    TEST_EMAIL,
    TEST_HOST,
    TEST_HW_VERSION,
    TEST_MAC,
    TEST_NAME,
    TEST_PASSWORD,
    TEST_PORT,
    TEST_SW_VERSION,
)
from tests.fixtures import (
    authenticated_local_client,
    authenticated_remote_client,
    auth_login_json,
    remote_auth_login_1_json,
    remote_auth_login_2_json,
    remote_error_known,
    remote_error_http_body,
    remote_error_unknown,
    remote_sprinklers_json,
    unauthenticated_json,
)
from tests.fixtures.api import apiver_json
from tests.fixtures.provision import provision_name_json, provision_wifi_json


@pytest.mark.asyncio
async def test_legacy_login(authenticated_local_client, event_loop):
    """Test loading a local client through the legacy method."""
    async with authenticated_local_client:
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            assert client._access_token == TEST_ACCESS_TOKEN
            assert client.api_version == TEST_API_VERSION
            assert client.hardware_version == TEST_HW_VERSION
            assert client.mac == TEST_MAC
            assert client.name == TEST_NAME
            assert client.software_version == TEST_SW_VERSION


@pytest.mark.asyncio
async def test_load_local(authenticated_local_client, event_loop):
    """Test loading a local client."""
    async with authenticated_local_client:
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
    aresponses,
    auth_login_json,
    provision_wifi_json,
    authenticated_local_client,
    event_loop,
):
    """Test skipping the loading of a local client if it's already loaded."""
    authenticated_local_client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/auth/login",
        "post",
        aresponses.Response(text=json.dumps(auth_login_json), status=200),
    )
    authenticated_local_client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/provision/wifi",
        "get",
        aresponses.Response(text=json.dumps(provision_wifi_json), status=200),
    )

    async with authenticated_local_client:
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, True)
            controller = client.controllers[TEST_MAC]

            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, True)
            assert len(client.controllers) == 1
            assert client.controllers[TEST_MAC] == controller


@pytest.mark.asyncio
async def test_load_local_failure(aresponses, unauthenticated_json, event_loop):
    """Test loading a local client and receiving a fail response."""
    aresponses.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/auth/login",
        "post",
        aresponses.Response(text=json.dumps(unauthenticated_json), status=401),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)


@pytest.mark.asyncio
async def test_load_remote(authenticated_remote_client, event_loop):
    """Test loading a remote client."""
    async with authenticated_remote_client:
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
async def test_load_remote_skip(
    aresponses,
    authenticated_remote_client,
    remote_auth_login_1_json,
    remote_sprinklers_json,
    event_loop,
):
    """Test skipping the loading of a remote client if it's already loaded."""
    authenticated_remote_client.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(text=json.dumps(remote_auth_login_1_json), status=200),
    )
    authenticated_remote_client.add(
        "my.rainmachine.com",
        "/devices/get-sprinklers",
        "post",
        aresponses.Response(text=json.dumps(remote_sprinklers_json), status=200),
    )

    async with authenticated_remote_client:
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD, True)
            controller = client.controllers[TEST_MAC]

            await client.load_remote(TEST_EMAIL, TEST_PASSWORD, True)
            assert len(client.controllers) == 1
            assert client.controllers[TEST_MAC] == controller


@pytest.mark.asyncio
async def test_load_remote_failure(aresponses, unauthenticated_json, event_loop):
    """Test loading a remote client and receiving a fail response."""
    aresponses.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(text=json.dumps(unauthenticated_json), status=401),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)


@pytest.mark.asyncio
async def test_remote_error_known(aresponses, event_loop, remote_error_known):
    """Test that remote error handling works."""
    aresponses.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(text=json.dumps(remote_error_known), status=200),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)


@pytest.mark.asyncio
async def test_remote_error_http_body(aresponses, event_loop, remote_error_http_body):
    """Test that remote error handling works."""
    aresponses.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(text=json.dumps(remote_error_http_body), status=200),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)


@pytest.mark.asyncio
async def test_remote_error_unknown(aresponses, event_loop, remote_error_unknown):
    """Test that remote error handling works."""
    aresponses.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(text=json.dumps(remote_error_unknown), status=200),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)


@pytest.mark.asyncio
async def test_request_timeout(authenticated_local_client, event_loop, mocker):
    """Test whether the client properly raises an error on timeout."""

    async def long_running_login(*args, **kwargs):
        """Define a method that takes 0.5 seconds to execute."""
        await asyncio.sleep(0.5)

    mock_login = mocker.patch("regenmaschine.login")
    mock_login.return_value = long_running_login

    with asynctest.mock.patch.object(
        aiohttp.ClientResponse, "json", long_running_login
    ):
        async with authenticated_local_client:
            async with aiohttp.ClientSession(loop=event_loop) as websession:
                with pytest.raises(RequestError):
                    await login(
                        TEST_HOST,
                        TEST_PASSWORD,
                        websession,
                        port=TEST_PORT,
                        ssl=False,
                        request_timeout=0.1,
                    )


@pytest.mark.asyncio
async def test_token_expired_exception(authenticated_local_client, event_loop):
    """Test that the appropriate error is thrown when a token expires."""
    async with authenticated_local_client:
        with pytest.raises(TokenExpiredError):
            async with aiohttp.ClientSession(loop=event_loop) as websession:
                client = await login(
                    TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
                )

                client._access_token_expiration = datetime.now() - timedelta(hours=1)
                await client._request("get", "random/endpoint")
