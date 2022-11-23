"""Define tests for program endpoints."""
import json
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from tests.common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.fixture(name="zone_id_response")
def zone_id_response_fixture() -> dict[str, Any]:
    """Return an API response that contains zone ID data.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("zone_id_response.json")))


@pytest.fixture(name="zone_post_response")
def zone_post_response_fixture() -> dict[str, Any]:
    """Return an API response that contains zone post data.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("zone_post_response.json")))


@pytest.fixture(name="zone_start_stop_response")
def zone_start_stop_response_fixture() -> dict[str, Any]:
    """Return an API response that contains zone start/stop data.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("zone_start_stop_response.json"))
    )


@pytest.mark.asyncio
async def test_zone_enable_disable(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    zone_post_response: dict[str, Any],
) -> None:
    """Test enabling a zone.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        zone_post_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/properties",
            "post",
            response=aiohttp.web_response.json_response(zone_post_response, status=200),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/properties",
            "post",
            response=aiohttp.web_response.json_response(zone_post_response, status=200),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            resp = await controller.zones.enable(1)
            assert resp["message"] == "OK"

            resp = await controller.zones.disable(1)
            assert resp["message"] == "OK"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "zone_fixture_filename", ["zone_response.json", "zone_response_gen1.json"]
)
async def test_zone_get(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    zone_fixture_filename: str,
) -> None:
    """Test getting info on all zones.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        zone_fixture_filename: A fixture filename.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture(zone_fixture_filename)), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            zones = await controller.zones.all(include_inactive=True)
            assert len(zones) == 12
            assert zones[1]["name"] == "Landscaping"
            assert zones[1]["active"] is True

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "zone_fixture_filename", ["zone_response.json", "zone_response_gen1.json"]
)
async def test_zone_get_detail(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    zone_fixture_filename: str,
) -> None:
    """Test getting all zones with details.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        zone_fixture_filename: A fixture filename.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture(zone_fixture_filename)), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/properties",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("zone_properties_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            zones = await controller.zones.all(details=True)
            assert len(zones) == 2
            assert zones[1]["name"] == "Landscaping"
            assert zones[1]["active"] is True
            assert zones[1]["ETcoef"] == 0.80000000000000004

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_zone_get_by_id(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    zone_id_response: dict[str, Any],
) -> None:
    """Test getting properties on a specific zone by ID.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        zone_id_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1",
            "get",
            response=aiohttp.web_response.json_response(zone_id_response, status=200),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.zones.get(1)
            assert data["name"] == "Landscaping"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_zone_get_by_id_details(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    zone_id_response: dict[str, Any],
) -> None:
    """Test getting advanced properties on a specific zone by ID.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        zone_id_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1",
            "get",
            response=aiohttp.web_response.json_response(zone_id_response, status=200),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/properties",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("zone_id_properties_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.zones.get(1, details=True)
            assert data["name"] == "Landscaping"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_zone_running(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting all running zones.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/zone",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("watering_zone_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.zones.running()
            assert len(data) == 12
            assert data[0]["name"] == "Zone 1"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_zone_start_stop(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    zone_start_stop_response: dict[str, Any],
) -> None:
    """Test starting and stopping a zone.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        zone_start_stop_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/start",
            "post",
            response=aiohttp.web_response.json_response(
                zone_start_stop_response, status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/stop",
            "post",
            response=aiohttp.web_response.json_response(
                zone_start_stop_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.zones.start(1, 60)
            assert data["message"] == "OK"

            data = await controller.zones.stop(1)
            assert data["message"] == "OK"

    aresponses.assert_plan_strictly_followed()
