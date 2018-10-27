"""Define tests for restriction endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import datetime
import json

import aiohttp
import pytest

from regenmaschine import login

from .const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from .fixtures import authenticated_client, auth_login_json
from .fixtures.provision import provision_name_json, provision_wifi_json
from .fixtures.watering import *


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, authenticated_client, event_loop, watering_log_json,
        watering_past_json, watering_queue_json, watering_stopall_json):
    """Test all endpoints."""
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/watering/log/details/{0}/{1}'.format(today_str, 2), 'get',
            aresponses.Response(
                text=json.dumps(watering_log_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/queue',
            'get',
            aresponses.Response(
                text=json.dumps(watering_queue_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/watering/past/{0}/{1}'.format(today_str, 2), 'get',
            aresponses.Response(
                text=json.dumps(watering_past_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/stopall',
            'post',
            aresponses.Response(
                text=json.dumps(watering_stopall_json), status=200))

        # pylint: disable=protected-access
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.watering.log(today, 2, details=True)
            assert len(data) == 2

            data = await client.watering.queue()
            assert not data

            data = await client.watering.runs(today, 2)
            assert len(data) == 8

            data = await client.watering.stop_all()
            assert data['message'] == 'OK'
