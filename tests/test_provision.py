"""Define tests for program endpoints."""
import aiohttp
import pytest

from regenmaschine import Client

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_endpoints(aresponses, authenticated_local_client):
    """Test getting all provisioning data."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/provision",
            "get",
            aresponses.Response(
                text=load_fixture("provision_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/provision/name",
            "get",
            aresponses.Response(
                text=load_fixture("provision_name_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/provision/wifi",
            "get",
            aresponses.Response(
                text=load_fixture("provision_wifi_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False)
            controller = next(iter(client.controllers.values()))

            name = await controller.provisioning.device_name
            assert name == "My House"

            data = await controller.provisioning.settings()
            assert data["system"]["databasePath"] == "/rainmachine-app/DB/Default"
            assert data["location"]["stationName"] == "MY STATION"
