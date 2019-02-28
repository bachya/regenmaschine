"""Define tests for program endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments
import json

import aiohttp
import pytest

from regenmaschine import login

from .const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from .fixtures import authenticated_client, auth_login_json
from .fixtures.api import apiver_json
from .fixtures.provision import *


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, authenticated_client, event_loop, provision_json,
        provision_name_json, provision_wifi_json):
    """Test getting all provisioning data."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision', 'get',
            aresponses.Response(text=json.dumps(provision_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision/name',
            'get',
            aresponses.Response(
                text=json.dumps(provision_name_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision/wifi',
            'get',
            aresponses.Response(
                text=json.dumps(provision_wifi_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            name = await client.provisioning.device_name
            assert name == 'My House'

            data = await client.provisioning.settings()
            assert data['system'][
                'databasePath'] == '/rainmachine-app/DB/Default'
            assert data['location']['stationName'] == 'MY STATION'
