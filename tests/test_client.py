"""Define tests for the client object."""
# pylint: disable=protected-access
import asyncio
import json
from datetime import datetime, timedelta
from typing import Any
from unittest.mock import Mock, patch

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from regenmaschine.errors import (
    RainMachineError,
    RequestError,
    TokenExpiredError,
    UnknownAPICallError,
)
from tests.common import (
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
async def test_legacy_login(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test loading a local controller through the legacy method.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client, aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False)
        controller = next(iter(client.controllers.values()))

        assert controller._access_token == TEST_ACCESS_TOKEN
        assert controller.api_version == TEST_API_VERSION
        assert controller.hardware_version == TEST_HW_VERSION
        assert controller.mac == TEST_MAC
        assert controller.name == TEST_NAME
        assert controller.software_version == TEST_SW_VERSION

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_load_local(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test loading a local controller.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client, aiohttp.ClientSession() as session:
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

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
@pytest.mark.parametrize("provision_name_response", [{"name": "89"}])
async def test_load_local_string_name(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test loading a local controller whose name (per the API) is not a string.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client, aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)

        assert len(client.controllers) == 1

        controller = client.controllers[TEST_MAC]
        assert isinstance(controller.name, str)
        assert controller.name == "89"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_load_local_skip(
    aresponses: ResponsesMockServer,
    auth_login_response: dict[str, Any],
    authenticated_local_client: ResponsesMockServer,
    provision_wifi_response: dict[str, Any],
) -> None:
    """Test skipping the loading of a local controller if it's already loaded.

    Args:
        aresponses: An aresponses server.
        auth_login_response: An API response payload.
        authenticated_local_client: A mock local controller.
        provision_wifi_response: An API response payload.
    """
    authenticated_local_client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/auth/login",
        "post",
        response=aiohttp.web_response.json_response(auth_login_response, status=200),
    )
    authenticated_local_client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/provision/wifi",
        "get",
        response=aiohttp.web_response.json_response(
            provision_wifi_response, status=200
        ),
    )

    async with authenticated_local_client, aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, True)
        controller = client.controllers[TEST_MAC]

        await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, True)
        assert len(client.controllers) == 1
        assert client.controllers[TEST_MAC] == controller

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_load_local_http_error(aresponses: ResponsesMockServer) -> None:
    """Test loading a local controller and receiving a fail response.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/auth/login",
        "post",
        aresponses.Response(text=None, status=500),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exc",
    [
        aiohttp.client_exceptions.ClientConnectorError(Mock(), Mock()),
        asyncio.TimeoutError(),
        json.decoder.JSONDecodeError("Not valid", "", 0),
    ],
)
async def test_load_local_other_errors(exc: type[Exception]) -> None:
    """Test loading a local controller and encountering a non-HTTP issue."""
    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        with patch.object(client._session, "request", side_effect=exc), pytest.raises(
            RequestError
        ):
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)


@pytest.mark.asyncio
async def test_load_remote(
    aresponses: ResponsesMockServer, authenticated_remote_client: ResponsesMockServer
) -> None:
    """Test loading a remote client.

    Args:
        aresponses: An aresponses server.
        authenticated_remote_client: A mock local controller.
    """
    async with authenticated_remote_client, aiohttp.ClientSession() as session:
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

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_load_remote_skip(
    aresponses: ResponsesMockServer,
    authenticated_remote_client: ResponsesMockServer,
    remote_auth_login_1_response: dict[str, Any],
    remote_sprinklers_response: dict[str, Any],
) -> None:
    """Test skipping the loading of a remote client if it's already loaded.

    Args:
        aresponses: An aresponses server.
        authenticated_remote_client: A mock local controller.
        remote_auth_login_1_response: An API response payload.
        remote_sprinklers_response: An API response payload.
    """
    authenticated_remote_client.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        response=aiohttp.web_response.json_response(
            remote_auth_login_1_response, status=200
        ),
    )
    authenticated_remote_client.add(
        "my.rainmachine.com",
        "/devices/get-sprinklers",
        "post",
        response=aiohttp.web_response.json_response(
            remote_sprinklers_response, status=200
        ),
    )

    async with authenticated_remote_client, aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.load_remote(TEST_EMAIL, TEST_PASSWORD, True)
        controller = client.controllers[TEST_MAC]

        await client.load_remote(TEST_EMAIL, TEST_PASSWORD, True)
        assert len(client.controllers) == 1
        assert client.controllers[TEST_MAC] == controller

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_fixture_filename,exc",
    [
        ("remote_error_http_body_response.json", RequestError),
        ("remote_error_known_response.json", RequestError),
        ("remote_error_unknown_response.json", RequestError),
        ("unauthenticated_response.json", TokenExpiredError),
    ],
)
async def test_load_remote_errors(
    aresponses: ResponsesMockServer,
    exc: type[RainMachineError],
    response_fixture_filename: str,
) -> None:
    """Test various remote errors.

    Args:
        aresponses: An aresponses server.
        exc: A RainMachineError subclass.
        response_fixture_filename: A filename string.
    """
    aresponses.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture(response_fixture_filename)), status=200
        ),
    )

    with pytest.raises(exc):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_remote(TEST_EMAIL, TEST_PASSWORD)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_request_timeout(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test whether the client properly raises an error on timeout.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    with patch.object(
        aiohttp.ClientResponse, "json", side_effect=asyncio.TimeoutError
    ):
        async with authenticated_local_client, aiohttp.ClientSession() as session:
            with pytest.raises(RequestError):
                client = Client(session=session, request_timeout=0)
                await client.load_local(
                    TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
                )

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_request_unknown_api_call(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test that an unknown API call is handled.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("unknown_api_call_response.json")), status=400
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            with pytest.raises(UnknownAPICallError):
                _ = await controller.zones.all()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_request_unparseable_response(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test a response that can't be parsed as JSON.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone",
            "get",
            aresponses.Response(text="404 Not Found", status=404),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            with pytest.raises(RequestError):
                _ = await controller.zones.all()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_token_expired_explicit_exception(
    aresponses: ResponsesMockServer,
) -> None:
    """Test that the appropriate error is thrown when a token expires explicitly.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/auth/login",
        "post",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture("unauthenticated_response.json")), status=400
        ),
    )

    with pytest.raises(TokenExpiredError):
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, TEST_PORT, False)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_token_expired_implicit_exception(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test that the appropriate error is thrown when a token expires implicitly.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    with pytest.raises(TokenExpiredError):
        async with authenticated_local_client, aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            controller._access_token_expiration = datetime.now() - timedelta(hours=1)
            await controller.request("get", "random/endpoint")

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_retry_only_once_on_server_disconnected(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test we retry on server disconnected.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/raindelay",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("restrictions_raindelay_response.json")),
                status=400,
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))
            patcher = None

            # pylint: disable=unused-argument
            def _raise_and_stop_patch(  # type: ignore[no-untyped-def]
                *args, **kwargs
            ) -> None:
                nonlocal patcher
                if patcher:
                    patcher.stop()  # type: ignore[unreachable]
                    raise aiohttp.ServerDisconnectedError

            patcher = patch.object(
                session, "request", side_effect=_raise_and_stop_patch
            )
            patcher.start()

            data = await controller.restrictions.raindelay()
            assert data["delayCounter"] == -1

            with pytest.raises(RequestError), patch.object(
                session, "request", side_effect=aiohttp.ServerDisconnectedError
            ):
                await controller.restrictions.raindelay()

    aresponses.assert_plan_strictly_followed()
