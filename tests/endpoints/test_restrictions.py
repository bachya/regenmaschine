"""Define tests for restriction endpoints."""

import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from regenmaschine.errors import UnknownAPICallError
from tests.common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_restrictions_hourly(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting any hourly restrictions.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/hourly",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("restrictions_hourly_response.json")),
                status=200,
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.restrictions.hourly()
            assert not data

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_restrictions_hourly_gen1(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test that getting hourly restrictions fails on a Gen1 controller.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            # Simulate this controller being a 1st generation controller:
            controller.hardware_version = "1"

            with pytest.raises(UnknownAPICallError):
                _ = await controller.restrictions.hourly()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_restrictions_current(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting any current restrictions.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/currently",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("restrictions_currently_response.json")),
                status=200,
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.restrictions.current()
            assert data["hourly"] is False

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_restrictions_global(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting any global restrictions.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/global",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("restrictions_global_response.json")),
                status=200,
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.restrictions.universal()
            assert data["freezeProtectTemp"] == 2

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_restrictions_raindelay(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting any rain delay-related restrictions.

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
                status=200,
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.restrictions.raindelay()
            assert data["delayCounter"] == -1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_set_restrictions_global(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test setting global restrictions.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/global",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("restrictions_global_set_response.json")),
                status=200,
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            await controller.restrictions.set_universal(
                {"hotDaysExtraWatering": False, "freezeProtectEnabled": True}
            )

    aresponses.assert_plan_strictly_followed()
