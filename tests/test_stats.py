"""Define tests for stat endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments
from datetime import date
import json

import aiohttp
import pytest

from regenmaschine import login

from tests.const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from tests.fixtures import auth_login_json, authenticated_local_client
from tests.fixtures.api import apiver_json
from tests.fixtures.provision import provision_name_json, provision_wifi_json
from tests.fixtures.stats import *


@pytest.mark.asyncio
async def test_stats(
    aresponses,
    authenticated_local_client,
    dailystats_date_json,
    dailystats_details_json,
    event_loop,
):
    """Test getting states (with or without details)."""
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            f"/api/4/dailystats/{today_str}",
            "get",
            aresponses.Response(text=json.dumps(dailystats_date_json), status=200),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/dailystats/details",
            "get",
            aresponses.Response(text=json.dumps(dailystats_details_json), status=200),
        )

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.stats.on_date(today)
            assert data["percentage"] == 100

            data = await client.stats.upcoming(details=True)
            assert len(data[0]["programs"]) == 4
