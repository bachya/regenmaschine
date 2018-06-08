"""Define tests for restriction endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT


@pytest.fixture(scope='module')
def fixture_current():
    """Return a /restrictions/currently response."""
    return {
        "hourly": False,
        "freeze": False,
        "month": False,
        "weekDay": False,
        "rainDelay": False,
        "rainDelayCounter": -1,
        "rainSensor": False
    }


@pytest.fixture(scope='module')
def fixture_hourly():
    """Return a /restrictions/hourly response."""
    return {
        "hourlyRestrictions": []
    }


@pytest.fixture(scope='module')
def fixture_raindelay():
    """Return a /restrictions/raindelay response."""
    return {
        "delayCounter": -1
    }


@pytest.fixture(scope='module')
def fixture_universal():
    """Return a /restrictions/global response."""
    return {
        "hotDaysExtraWatering": False,
        "freezeProtectEnabled": True,
        "freezeProtectTemp": 2,
        "noWaterInWeekDays": "0000000",
        "noWaterInMonths": "000000000000",
        "rainDelayStartTime": 1524854551,
        "rainDelayDuration": 0
    }


@pytest.mark.asyncio
async def test_endpoints(aresponses, fixture_current, fixture_hourly,
                         fixture_raindelay, fixture_universal, event_loop):
    """Test all endpoints."""
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/restrictions/currently', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_current), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/restrictions/hourly', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_hourly), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/restrictions/raindelay', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_raindelay), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/restrictions/global', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_universal), status=200))

    # pylint: disable=protected-access
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        client._authenticated = True
        client._access_token = '12345'

        data = await client.restrictions.current()
        assert data['hourly'] is False

        data = await client.restrictions.hourly()
        assert not data

        data = await client.restrictions.raindelay()
        assert data['delayCounter'] == -1

        data = await client.restrictions.universal()
        assert data['freezeProtectTemp'] == 2
