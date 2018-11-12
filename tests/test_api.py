"""Define tests for api endpoints."""
# pylint: disable=redefined-outer-name

import json

import aiohttp
import aresponses
import pytest

from regenmaschine import login

from .const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from .fixtures import authenticated_client, auth_login_json
from .fixtures.api import apiver_json
from .fixtures.provision import provision_name_json, provision_wifi_json


@pytest.mark.asyncio
async def test_endpoints(
        apiver_json, aresponses, authenticated_client, event_loop):
    """Test all endpoints."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/apiVer', 'get',
            aresponses.Response(text=json.dumps(apiver_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.api.versions()
            assert data['apiVer'] == '4.5.0'
            assert data['hwVer'] == 3
            assert data['swVer'] == '4.0.925'
