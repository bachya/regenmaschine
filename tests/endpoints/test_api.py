"""Define tests for api endpoints."""
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from tests.common import TEST_HOST, TEST_PASSWORD, TEST_PORT


@pytest.mark.asyncio
async def test_api_versions(
    aresponses: ResponsesMockServer,
    api_version_response: dict[str, Any],
    authenticated_local_client: ResponsesMockServer,
) -> None:
    """Test getting API, hardware, and software versions.

    Args:
        aresponses: An aresponses server.
        api_version_response: An API response payload.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/apiVer",
            "get",
            response=aiohttp.web_response.json_response(
                api_version_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.api.versions()
            assert data["apiVer"] == "4.5.0"
            assert data["hwVer"] == 3
            assert data["swVer"] == "4.0.925"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_api_versions_no_explicit_session(
    aresponses: ResponsesMockServer,
    api_version_response: dict[str, Any],
    authenticated_local_client: ResponsesMockServer,
) -> None:
    """Test no explicit ClientSession.

    Args:
        aresponses: An aresponses server.
        api_version_response: An API response payload.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/apiVer",
            "get",
            response=aiohttp.web_response.json_response(
                api_version_response, status=200
            ),
        )

        client = Client()
        await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False)
        controller = next(iter(client.controllers.values()))

        data = await controller.api.versions()
        assert data["apiVer"] == "4.5.0"
        assert data["hwVer"] == 3
        assert data["swVer"] == "4.0.925"

    aresponses.assert_plan_strictly_followed()
