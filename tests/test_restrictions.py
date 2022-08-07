"""Define tests for restriction endpoints."""
import aiohttp
import pytest

from regenmaschine import Client

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_set_restrictions_global(aresponses, authenticated_local_client):
    """Test setting global restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/global",
            "post",
            aresponses.Response(
                text=load_fixture("restrictions_global_set_response.json"), status=200
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


@pytest.mark.asyncio
async def test_restrictions_hourly(aresponses, authenticated_local_client):
    """Test getting any hourly restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/hourly",
            "get",
            aresponses.Response(
                text=load_fixture("restrictions_hourly_response.json"), status=200
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


@pytest.mark.asyncio
async def test_restrictions_raindelay(aresponses, authenticated_local_client):
    """Test getting any rain delay-related restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/raindelay",
            "get",
            aresponses.Response(
                text=load_fixture("restrictions_raindelay_response.json"), status=200
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


@pytest.mark.asyncio
async def test_restrictions_current(aresponses, authenticated_local_client):
    """Test getting any current restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/currently",
            "get",
            aresponses.Response(
                text=load_fixture("restrictions_currently_response.json"), status=200
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


@pytest.mark.asyncio
async def test_restrictions_global(aresponses, authenticated_local_client):
    """Test getting any global restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/global",
            "get",
            aresponses.Response(
                text=load_fixture("restrictions_global_response.json"), status=200
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


@pytest.mark.asyncio
async def test_restrictions_hourly(aresponses, authenticated_local_client):
    """Test getting any hourly restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/hourly",
            "get",
            aresponses.Response(
                text=load_fixture("restrictions_hourly_response.json"), status=200
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


@pytest.mark.asyncio
async def test_restrictions_raindelay(aresponses, authenticated_local_client):
    """Test getting any rain delay-related restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/raindelay",
            "get",
            aresponses.Response(
                text=load_fixture("restrictions_raindelay_response.json"), status=200
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
