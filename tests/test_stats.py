"""Define tests for stat endpoints."""
from datetime import date

import aiohttp
import pytest

from regenmaschine import login

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

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.stats.on_date(today)
            assert data["percentage"] == 100

            data = await client.stats.upcoming(details=True)
            assert len(data[0]["programs"]) == 4
