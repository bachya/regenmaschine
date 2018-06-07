"""Define tests for parser endpoints."""
# pylint: disable=redefined-outer-name

import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT


@pytest.fixture(scope='module')
def fixture_current():
    """Return a /parser response."""
    return {
        "parsers": [{
            "lastRun": "2018-04-30 11:52:33",
            "lastKnownError": "",
            "hasForecast": True,
            "uid": 11,
            "hasHistorical": False,
            "description": "North America weather forecast",
            "enabled": True,
            "custom": False,
            "isRunning": False,
            "name": "NOAA Parser"
        }]
    }


@pytest.mark.asyncio
async def test_endpoints(aresponses, fixture_current, event_loop):
    """Test retrieving current diagnostics."""
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/parser',
                   'get',
                   aresponses.Response(
                       text=json.dumps(fixture_current), status=200))

    # pylint: disable=protected-access
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        client._authenticated = True
        client._access_token = '12345'

        data = await client.parsers.current()
        assert len(data) == 1
        assert data[0]['name'] == 'NOAA Parser'
