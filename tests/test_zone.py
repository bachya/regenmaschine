"""Define tests for program endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import json

import aiohttp
import pytest

from regenmaschine import login

from .const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from .fixtures import authenticated_client, auth_login_json
from .fixtures.api import apiver_json
from .fixtures.provision import provision_name_json, provision_wifi_json
from .fixtures.zone import *


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, authenticated_client, event_loop, zone_id_properties_json,
        zone_properties_json, zone_start_stop_json):
    """Test all endpoints."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/properties',
            'get',
            aresponses.Response(
                text=json.dumps(zone_properties_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/1/properties',
            'get',
            aresponses.Response(
                text=json.dumps(zone_id_properties_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/1/start',
            'post',
            aresponses.Response(
                text=json.dumps(zone_start_stop_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/1/stop',
            'post',
            aresponses.Response(
                text=json.dumps(zone_start_stop_json), status=200))

        # pylint: disable=protected-access
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.zones.all(details=True)
            assert len(data) == 1
            assert data[0]['name'] == 'Landscaping'

            data = await client.zones.get(1, details=True)
            assert data['name'] == 'Landscaping'

            data = await client.zones.start(1, 60)
            assert data['message'] == 'OK'

            data = await client.zones.stop(1)
            assert data['message'] == 'OK'
