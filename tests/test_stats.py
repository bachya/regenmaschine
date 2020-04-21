"""Define tests for stat endpoints."""
from datetime import date

import aiohttp
import pytest

from regenmaschine import Client

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_stats(aresponses, authenticated_local_client):
    """Test getting states (with or without details)."""
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            f"/api/4/dailystats/{today_str}",
            "get",
            aresponses.Response(
                text=load_fixture("dailystats_date_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/dailystats/details",
            "get",
            aresponses.Response(
                text=load_fixture("dailystats_details_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False)
            controller = next(iter(client.controllers.values()))

            data = await controller.stats.on_date(today)
            assert data["percentage"] == 100

            data = await controller.stats.upcoming(details=True)
            assert len(data[0]["programs"]) == 4
