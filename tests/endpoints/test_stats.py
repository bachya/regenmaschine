"""Define tests for stat endpoints."""

import json
from datetime import date

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from tests.common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_stats(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting states (with or without details).

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        today = date.today()
        today_str = today.strftime("%Y-%m-%d")

        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            f"/api/4/dailystats/{today_str}",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("dailystats_date_response.json")), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/dailystats/details",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("dailystats_details_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            on_date_data = await controller.stats.on_date(today)
            assert on_date_data["percentage"] == 100

            upcoming_data = await controller.stats.upcoming(details=True)
            assert len(upcoming_data[0]["programs"]) == 4

    aresponses.assert_plan_strictly_followed()
