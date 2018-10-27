"""Define tests for restriction endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments
import json

import aiohttp
import pytest

from regenmaschine import login

from .const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from .fixtures import authenticated_client, auth_login_json
from .fixtures.provision import provision_name_json, provision_wifi_json
from .fixtures.restrictions import *


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, authenticated_client, event_loop,
        restrictions_currently_json, restrictions_global_json,
        restrictions_hourly_json, restrictions_raindelay_json):
    """Test all endpoints."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/restrictions/currently', 'get',
            aresponses.Response(
                text=json.dumps(restrictions_currently_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/restrictions/global', 'get',
            aresponses.Response(
                text=json.dumps(restrictions_global_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/restrictions/hourly', 'get',
            aresponses.Response(
                text=json.dumps(restrictions_hourly_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/restrictions/raindelay', 'get',
            aresponses.Response(
                text=json.dumps(restrictions_raindelay_json), status=200))

        # pylint: disable=protected-access
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.restrictions.current()
            assert data['hourly'] is False

            data = await client.restrictions.hourly()
            assert not data

            data = await client.restrictions.raindelay()
            assert data['delayCounter'] == -1

            data = await client.restrictions.universal()
            assert data['freezeProtectTemp'] == 2
