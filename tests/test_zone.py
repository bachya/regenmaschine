"""Define tests for program endpoints."""
import aiohttp
import pytest

from regenmaschine import Client

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_zone_enable_disable(aresponses, authenticated_local_client):
    """Test enabling a zone."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/properties",
            "post",
            aresponses.Response(
                text=load_fixture("zone_post_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/properties",
            "post",
            aresponses.Response(
                text=load_fixture("zone_post_response.json"), status=200
            ),
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "zone_fixture_filename", ["zone_response.json", "zone_response_gen1.json"]
)
async def test_zone_get(aresponses, authenticated_local_client, zone_fixture_filename):
    """Test getting info on all zones."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone",
            "get",
            aresponses.Response(text=load_fixture(zone_fixture_filename), status=200),
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "zone_fixture_filename", ["zone_response.json", "zone_response_gen1.json"]
)
async def test_zone_get_detail(
    aresponses, authenticated_local_client, zone_fixture_filename
):
    """Test getting all zones with details."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone",
            "get",
            aresponses.Response(text=load_fixture(zone_fixture_filename), status=200),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/properties",
            "get",
            aresponses.Response(
                text=load_fixture("zone_properties_response.json"), status=200
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


@pytest.mark.asyncio
async def test_zone_get_by_id(aresponses, authenticated_local_client):
    """Test getting properties on a specific zone by ID."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1",
            "get",
            aresponses.Response(text=load_fixture("zone_id_response.json"), status=200),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.zones.get(1)
            assert data["name"] == "Landscaping"


@pytest.mark.asyncio
async def test_zone_get_by_id_details(aresponses, authenticated_local_client):
    """Test getting advanced properties on a specific zone by ID."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1",
            "get",
            aresponses.Response(text=load_fixture("zone_id_response.json"), status=200),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/properties",
            "get",
            aresponses.Response(
                text=load_fixture("zone_id_properties_response.json"), status=200
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


@pytest.mark.asyncio
async def test_zone_start_stop(aresponses, authenticated_local_client):
    """Test starting and stopping a zone."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/start",
            "post",
            aresponses.Response(
                text=load_fixture("zone_start_stop_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/stop",
            "post",
            aresponses.Response(
                text=load_fixture("zone_start_stop_response.json"), status=200
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
