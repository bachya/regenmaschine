"""Define tests for program endpoints."""
import aiohttp
import pytest

from regenmaschine import login

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

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            resp = await client.zones.enable(1)
            assert resp["message"] == "OK"

            resp = await client.zones.disable(1)
            assert resp["message"] == "OK"


@pytest.mark.asyncio
async def test_zone_get(aresponses, authenticated_local_client):
    """Test getting info on all zones."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/properties",
            "get",
            aresponses.Response(
                text=load_fixture("zone_properties_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.zones.all(details=True, include_inactive=True)
            assert len(data) == 2
            assert data[0]["name"] == "Landscaping"


@pytest.mark.asyncio
async def test_zone_get_active(aresponses, authenticated_local_client):
    """Test getting info on active zones."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/properties",
            "get",
            aresponses.Response(
                text=load_fixture("zone_properties_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.zones.all(details=True)
            assert len(data) == 1
            assert data[0]["name"] == "Landscaping"


@pytest.mark.asyncio
async def test_zone_get_by_id(aresponses, authenticated_local_client):
    """Test getting properties on a specific zone by ID."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/zone/1/properties",
            "get",
            aresponses.Response(
                text=load_fixture("zone_id_properties_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.zones.get(1, details=True)
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

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.zones.start(1, 60)
            assert data["message"] == "OK"

            data = await client.zones.stop(1)
            assert data["message"] == "OK"
