"""Define tests for api endpoints."""
import aiohttp
import pytest

from regenmaschine import Client

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_api_versions(aresponses, authenticated_local_client):
    """Test getting API, hardware, and software versions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/apiVer",
            "get",
            aresponses.Response(
                text=load_fixture("api_version_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False)
            controller = next(iter(client.controllers.values()))

            data = await controller.api.versions()
            assert data["apiVer"] == "4.5.0"
            assert data["hwVer"] == 3
            assert data["swVer"] == "4.0.925"


@pytest.mark.asyncio
async def test_api_versions_no_explicit_session(aresponses, authenticated_local_client):
    """Test no explicit ClientSession."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/apiVer",
            "get",
            aresponses.Response(
                text=load_fixture("api_version_response.json"), status=200
            ),
        )

        client = Client()
        await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False)
        controller = next(iter(client.controllers.values()))

        data = await controller.api.versions()
        assert data["apiVer"] == "4.5.0"
        assert data["hwVer"] == 3
        assert data["swVer"] == "4.0.925"
