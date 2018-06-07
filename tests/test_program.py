"""Define tests for program endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT


@pytest.fixture(scope='module')
def fixture_all():
    """Return a /program response."""
    return {
        "programs": [{
            "uid": 1,
            "name": "Morning",
            "active": True,
            "startTime": "06:00",
            "cycles": 0,
            "soak": 0,
            "cs_on": False,
            "delay": 0,
            "delay_on": False,
            "status": 0,
            "startTimeParams": {
                "offsetSign": 0,
                "type": 0,
                "offsetMinutes": 0
            },
            "frequency": {
                "type": 0,
                "param": "0"
            },
            "coef": 0.0,
            "ignoreInternetWeather": False,
            "futureField1": 0,
            "freq_modified": 0,
            "useWaterSense": False,
            "nextRun": "2018-06-04",
            "startDate": "2018-04-28",
            "endDate": None,
            "yearlyRecurring": True,
            "simulationExpired": False,
            "wateringTimes": [{
                "id": 1,
                "order": -1,
                "name": "Landscaping",
                "duration": 0,
                "active": True,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 2,
                "order": -1,
                "name": "Flower Box",
                "duration": 0,
                "active": True,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 3,
                "order": -1,
                "name": "TEST",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 4,
                "order": -1,
                "name": "Zone 4",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 5,
                "order": -1,
                "name": "Zone 5",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 6,
                "order": -1,
                "name": "Zone 6",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 7,
                "order": -1,
                "name": "Zone 7",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 8,
                "order": -1,
                "name": "Zone 8",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 9,
                "order": -1,
                "name": "Zone 9",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 10,
                "order": -1,
                "name": "Zone 10",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 11,
                "order": -1,
                "name": "Zone 11",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 12,
                "order": -1,
                "name": "Zone 12",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }]
        }]
    }


@pytest.fixture(scope='module')
def fixture_get():
    """Return a program/<ID> response."""
    return {
        "uid": 1,
        "name": "Morning",
        "active": True,
        "startTime": "06:00",
        "cycles": 0,
        "soak": 0,
        "cs_on": False,
        "delay": 0,
        "delay_on": False,
        "status": 0,
        "startTimeParams": {
            "offsetSign": 0,
            "type": 0,
            "offsetMinutes": 0
        },
        "frequency": {
            "type": 0,
            "param": "0"
        },
        "coef": 0.0,
        "ignoreInternetWeather": False,
        "futureField1": 0,
        "freq_modified": 0,
        "useWaterSense": False,
        "nextRun": "2018-04-27",
        "endDate": "1969-12-31",
        "simulationExpired": False,
        "yearlyRecurring": True,
        "wateringTimes": [{
            "id": 1,
            "name": "Landscaping",
            "duration": 0,
            "active": True,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 2,
            "name": "Flower Box",
            "duration": 0,
            "active": True,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 3,
            "name": "Zone 3",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 4,
            "name": "Zone 4",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 5,
            "name": "Zone 5",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 6,
            "name": "Zone 6",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 7,
            "name": "Zone 7",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 8,
            "name": "Zone 8",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 9,
            "name": "Zone 9",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 10,
            "name": "Zone 10",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 11,
            "name": "Zone 11",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }, {
            "id": 12,
            "name": "Zone 12",
            "duration": 0,
            "active": False,
            "userPercentage": 1.0,
            "order": -1
        }]
    }


@pytest.fixture(scope='module')
def fixture_next_runs():
    """Return a /program/nextrun response."""
    return {
        "nextRuns": [{
            "pid": 1,
            "startTime": "06:00"
        }, {
            "pid": 2,
            "startTime": "22:00"
        }]
    }


@pytest.fixture(scope='module')
def fixture_running():
    """Return a /watering/program response."""
    return {
        "programs": [{
            "uid": 2,
            "name": "Evening",
            "manual": False,
            "userStartTime": "2018-06-02 22:00:00",
            "realStartTime": "2018-06-02 22:00:02",
            "status": 1
        }]
    }


@pytest.fixture(scope='module')
def fixture_start_stop():
    """Return a response for /program/<ID>/start and /program/<ID>/stop."""
    return {"statusCode": 0, "message": "OK"}


@pytest.mark.asyncio
async def test_endpoints(aresponses, fixture_all, fixture_get,
                         fixture_next_runs, fixture_running,
                         fixture_start_stop, event_loop):
    """Test retrieving all programs."""
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program',
                   'get',
                   aresponses.Response(
                       text=json.dumps(fixture_all), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program/1',
                   'get',
                   aresponses.Response(
                       text=json.dumps(fixture_get), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/program/nextrun', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_next_runs), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/watering/program', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_running), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/program/1/start', 'post',
                   aresponses.Response(
                       text=json.dumps(fixture_start_stop), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/program/1/stop', 'post',
                   aresponses.Response(
                       text=json.dumps(fixture_start_stop), status=200))

    # pylint: disable=protected-access
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        client._authenticated = True
        client._access_token = '12345'

        data = await client.programs.all()
        assert len(data) == 1
        assert data[0]['name'] == 'Morning'

        data = await client.programs.get(1)
        assert data['name'] == 'Morning'

        data = await client.programs.next()
        assert len(data) == 2

        data = await client.programs.running()
        assert len(data) == 1
        assert data[0]['name'] == 'Evening'

        data = await client.programs.start(1)
        assert data['message'] == 'OK'

        data = await client.programs.stop(1)
        assert data['message'] == 'OK'
