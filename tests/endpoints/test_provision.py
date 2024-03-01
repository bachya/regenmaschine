"""Define tests for program endpoints."""

import json
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from tests.common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_endpoints(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    provision_name_response: dict[str, Any],
    provision_wifi_response: dict[str, Any],
) -> None:
    """Test getting all provisioning data.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        provision_name_response: An API response payload.
        provision_wifi_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/provision",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("provision_response.json")), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/provision/name",
            "get",
            response=aiohttp.web_response.json_response(
                provision_name_response, status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/provision/wifi",
            "get",
            response=aiohttp.web_response.json_response(
                provision_wifi_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            name = await controller.provisioning.device_name
            assert name == "My House"

            data = await controller.provisioning.settings()
            assert data["system"]["databasePath"] == "/rainmachine-app/DB/Default"
            assert data["location"]["stationName"] == "MY STATION"

    aresponses.assert_plan_strictly_followed()
