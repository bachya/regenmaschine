"""Define tests for restriction endpoints."""

import datetime
import json
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from tests.common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.fixture(name="watering_pause_response")
def watering_pause_response_fixture() -> dict[str, Any]:
    """Return an API response that contains watering pause data.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("watering_pause_response.json"))
    )


@pytest.mark.asyncio
async def test_watering_log_details(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting watering log details.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")

        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            f"/api/4/watering/log/details/{today_str}/2",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("watering_log_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.watering.log(today, 2, details=True)
            assert len(data) == 2

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_watering_pause(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    watering_pause_response: dict[str, Any],
) -> None:
    """Test pausing and unpausing watering.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        watering_pause_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/pauseall",
            "post",
            response=aiohttp.web_response.json_response(
                watering_pause_response, status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/pauseall",
            "post",
            response=aiohttp.web_response.json_response(
                watering_pause_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.watering.pause_all(30)
            assert data["message"] == "OK"

            with pytest.raises(ValueError):
                data = await controller.watering.pause_all(60 * 60 * 24)

            data = await controller.watering.unpause_all()
            assert data["message"] == "OK"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_watering_queue(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting the watering queue.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/queue",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("watering_queue_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.watering.queue()
            assert not data

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_watering_past(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test gettinng info on past watering runs.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")

        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            f"/api/4/watering/past/{today_str}/2",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("watering_past_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.watering.runs(today, 2)
            assert len(data) == 8

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_watering_stop(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test stopping all watering activities.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/stopall",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("watering_stopall_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.watering.stop_all()
            assert data["message"] == "OK"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_watering_flowmeter(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting flowmeter values.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/flowmeter",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("watering_flowmeter_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.watering.flowmeter()
            assert data["flowMeterWateringClicks"] == 4000

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_post_watering_flowmeter(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting flowmeter values.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/flowmeter",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("watering_flowmeter_post_response.json")),
                status=200,
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.watering.post_flowmeter(value=200, units="litre")
            assert data["statusCode"] == 0

    aresponses.assert_plan_strictly_followed()
