"""Define tests for diagnostics endpoints."""
# pylint: disable=redefined-outer-name

import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT


@pytest.fixture(scope='module')
def fixture_diag():
    """Return a /diag response."""
    return {
        "hasWifi": True,
        "uptime": "14 days, 8:45:19",
        "uptimeSeconds": 1241119,
        "memUsage": 18220,
        "networkStatus": True,
        "bootCompleted": True,
        "lastCheckTimestamp": 1527997722,
        "wizardHasRun": True,
        "standaloneMode": False,
        "cpuUsage": 0.0,
        "lastCheck": "2018-06-02 21:48:42",
        "softwareVersion": "4.0.925",
        "internetStatus": True,
        "locationStatus": True,
        "timeStatus": True,
        "wifiMode": None,
        "gatewayAddress": "192.168.1.1",
        "cloudStatus": 0,
        "weatherStatus": True
    }


@pytest.fixture(scope='module')
def fixture_diag_log():
    """Return a /diag/log response."""
    return {"log": "----"}


@pytest.mark.asyncio
async def test_endpoints(aresponses, fixture_diag, fixture_diag_log,
                         event_loop):
    """Test all endpoints."""
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/diag',
                   'get',
                   aresponses.Response(
                       text=json.dumps(fixture_diag), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/diag/log',
                   'get',
                   aresponses.Response(
                       text=json.dumps(fixture_diag_log), status=200))

    # pylint: disable=protected-access
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        client._authenticated = True
        client._access_token = '12345'

        data = await client.diagnostics.current()
        assert data['memUsage'] == 18220

        data = await client.diagnostics.log()
        assert data == '----'
