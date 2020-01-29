"""Define tests for api endpoints."""
import aiohttp
import pytest

from regenmaschine import login

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

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.api.versions()
            assert data["apiVer"] == "4.5.0"
            assert data["hwVer"] == 3
            assert data["swVer"] == "4.0.925"
