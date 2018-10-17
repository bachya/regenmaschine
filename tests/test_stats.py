"""Define tests for stat endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments
import json
from datetime import date

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from .fixtures import authenticated_client, auth_login_json
from .fixtures.provision import provision_name_json, provision_wifi_json
from .fixtures.stats import *


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, authenticated_client, dailystats_date_json,
        dailystats_details_json, event_loop):
    """Test all endpoints."""
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')

    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/dailystats/{0}'.format(today_str), 'get',
            aresponses.Response(
                text=json.dumps(dailystats_date_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/dailystats/details', 'get',
            aresponses.Response(
                text=json.dumps(dailystats_details_json), status=200))

        # pylint: disable=protected-access
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await Client.authenticate_via_password(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.stats.on_date(today)
            assert data['percentage'] == 100

            data = await client.stats.upcoming(details=True)
            assert len(data[0]['programs']) == 4
