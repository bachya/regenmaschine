"""Define tests for the client object."""
# pylint: disable=protected-access
import asyncio
from datetime import datetime, timedelta

import aiohttp
import asynctest
import pytest

from regenmaschine import Client
from regenmaschine.errors import RequestError, TokenExpiredError

from .common import (
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
    load_fixture,
)


@pytest.mark.asyncio
async def test_legacy_login(authenticated_local_client):
    """Test loading a local client through the legacy method."""
    async with authenticated_local_client:
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False)
            controller = next(iter(client.controllers.values()))

            assert controller._access_token == TEST_ACCESS_TOKEN
            assert controller.api_version == TEST_API_VERSION
            assert controller.hardware_version == TEST_HW_VERSION
            assert controller.mac == TEST_MAC
            assert controller.name == TEST_NAME
            assert controller.software_version == TEST_SW_VERSION


@pytest.mark.asyncio
async def test_load_local(authenticated_local_client):
    """Test loading a local client."""
    async with authenticated_local_client:
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
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
async def test_load_local_skip(aresponses, authenticated_local_client):
    """Test skipping the loading of a local client if it's already loaded."""
    authenticated_local_client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/auth/login",
        "post",
        aresponses.Response(text=load_fixture("auth_login_response.json"), status=200),
    )
    authenticated_local_client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/provision/wifi",
        "get",
        aresponses.Response(
            text=load_fixture("provision_wifi_response.json"), status=200
        ),
    )

    async with authenticated_local_client:
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, True)
            controller = client.controllers[TEST_MAC]

            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, True)
            assert len(client.controllers) == 1
            assert client.controllers[TEST_MAC] == controller


@pytest.mark.asyncio
async def test_load_local_failure(aresponses):
    """Test loading a local client and receiving a fail response."""
    aresponses.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/auth/login",
        "post",
        aresponses.Response(
            text=load_fixture("unauthenticated_response.json"), status=401
        ),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)


@pytest.mark.asyncio
async def test_load_remote(authenticated_remote_client, event_loop):
    """Test loading a remote client."""
    async with authenticated_remote_client:
        async with aiohttp.ClientSession(loop=event_loop) as session:
            client = Client(session=session)
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
async def test_load_remote_skip(aresponses, authenticated_remote_client):
    """Test skipping the loading of a remote client if it's already loaded."""
    authenticated_remote_client.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(
            text=load_fixture("remote_auth_login_1_response.json"), status=200
        ),
    )
    authenticated_remote_client.add(
        "my.rainmachine.com",
        "/devices/get-sprinklers",
        "post",
        aresponses.Response(
            text=load_fixture("remote_sprinklers_response.json"), status=200
        ),
    )

    async with authenticated_remote_client:
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD, True)
            controller = client.controllers[TEST_MAC]

            await client.load_remote(TEST_EMAIL, TEST_PASSWORD, True)
            assert len(client.controllers) == 1
            assert client.controllers[TEST_MAC] == controller


@pytest.mark.asyncio
async def test_load_remote_failure(aresponses):
    """Test loading a remote client and receiving a fail response."""
    aresponses.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(
            text=load_fixture("unauthenticated_response.json"), status=401
        ),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)


@pytest.mark.asyncio
async def test_remote_error_known(aresponses):
    """Test that remote error handling works."""
    aresponses.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(
            text=load_fixture("remote_error_known_response.json"), status=200
        ),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)


@pytest.mark.asyncio
async def test_remote_error_http_body(aresponses):
    """Test that remote error handling works."""
    aresponses.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(
            text=load_fixture("remote_error_http_body_response.json"), status=200
        ),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)


@pytest.mark.asyncio
async def test_remote_error_unknown(aresponses):
    """Test that remote error handling works."""
    aresponses.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(
            text=load_fixture("remote_error_unknown_response.json"), status=200
        ),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)


@pytest.mark.asyncio
async def test_request_timeout(authenticated_local_client):  # noqa: D202
    """Test whether the client properly raises an error on timeout."""

    async def long_running_login(*args, **kwargs):  # pylint: disable=unused-argument
        """Define a method that takes 0.5 seconds to execute."""
        await asyncio.sleep(0.5)

    with asynctest.mock.patch.object(
        aiohttp.ClientResponse, "json", long_running_login
    ):
        async with authenticated_local_client:
            async with aiohttp.ClientSession() as session:
                with pytest.raises(RequestError):
                    client = Client(session=session, request_timeout=0.1)
                    await client.load_local(
                        TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False
                    )


@pytest.mark.asyncio
async def test_token_expired_exception(authenticated_local_client):
    """Test that the appropriate error is thrown when a token expires."""
    async with authenticated_local_client:
        with pytest.raises(TokenExpiredError):
            async with aiohttp.ClientSession() as session:
                client = Client(session=session)
                await client.load_local(
                    TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False
                )
                controller = next(iter(client.controllers.values()))

                controller._access_token_expiration = datetime.now() - timedelta(
                    hours=1
                )
                await controller._request("get", "random/endpoint")
