"""Define tests for program endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, fixture_device_name, fixture_settings, fixture_wifi,
        event_loop):
    """Test all endpoints."""
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision', 'get',
        aresponses.Response(text=json.dumps(fixture_settings), status=200))
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision/name', 'get',
        aresponses.Response(text=json.dumps(fixture_device_name), status=200))
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision/wifi', 'get',
        aresponses.Response(text=json.dumps(fixture_wifi), status=200))

    # pylint: disable=protected-access
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        client._authenticated = True
        client._access_token = '12345'

        name = await client.provisioning.device_name
        assert name == 'My House'

        data = await client.provisioning.settings()
        assert data['system']['databasePath'] == '/rainmachine-app/DB/Default'
        assert data['location']['stationName'] == 'MY STATION'
