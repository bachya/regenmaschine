"""Define tests for restriction endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import datetime
import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT


@pytest.fixture(scope='module')
def fixture_log():
    """Return a /watering/log/details/<DATE>/<DAYS> response."""
    return {
        "waterLog": {
            "days": [{
                "date":
                    "2018-06-01",
                "dateTimestamp":
                    1527832800,
                "programs": [{
                    "id":
                        1,
                    "zones": [{
                        "uid":
                            1,
                        "flag":
                            0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-01 06:00:02",
                            "startTimestamp": 1527854402,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 1243
                        }]
                    }, {
                        "uid":
                            2,
                        "flag":
                            0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-01 06:20:45",
                            "startTimestamp": 1527855645,
                            "userDuration": 2680,
                            "machineDuration": 2680,
                            "realDuration": 2680
                        }]
                    }]
                }, {
                    "id":
                        2,
                    "zones": [{
                        "uid":
                            1,
                        "flag":
                            0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-01 22:00:01",
                            "startTimestamp": 1527912001,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 1243
                        }]
                    }, {
                        "uid":
                            2,
                        "flag":
                            0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-01 22:20:44",
                            "startTimestamp": 1527913244,
                            "userDuration": 2680,
                            "machineDuration": 2680,
                            "realDuration": 2680
                        }]
                    }]
                }]
            }, {
                "date":
                    "2018-06-02",
                "dateTimestamp":
                    1527919200,
                "programs": [{
                    "id":
                        1,
                    "zones": [{
                        "uid":
                            1,
                        "flag":
                            0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-02 06:00:01",
                            "startTimestamp": 1527940801,
                            "userDuration": 1243,
                            "machineDuration": 1217,
                            "realDuration": 1217
                        }]
                    }, {
                        "uid":
                            2,
                        "flag":
                            0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-02 06:20:18",
                            "startTimestamp": 1527942018,
                            "userDuration": 2680,
                            "machineDuration": 2624,
                            "realDuration": 2624
                        }]
                    }]
                }, {
                    "id":
                        0,
                    "zones": [{
                        "uid":
                            1,
                        "flag":
                            1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-02 20:58:54",
                            "startTimestamp": 1527994734,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 6
                        }]
                    }]
                }, {
                    "id":
                        0,
                    "zones": [{
                        "uid":
                            1,
                        "flag":
                            1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-02 21:00:40",
                            "startTimestamp": 1527994840,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 3
                        }]
                    }]
                }, {
                    "id":
                        0,
                    "zones": [{
                        "uid":
                            1,
                        "flag":
                            1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-02 21:20:03",
                            "startTimestamp": 1527996003,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 3
                        }]
                    }]
                }, {
                    "id":
                        0,
                    "zones": [{
                        "uid":
                            1,
                        "flag":
                            1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-02 21:40:41",
                            "startTimestamp": 1527997241,
                            "userDuration": 3,
                            "machineDuration": 3,
                            "realDuration": 2
                        }]
                    }]
                }, {
                    "id":
                        2,
                    "zones": [{
                        "uid":
                            1,
                        "flag":
                            0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-02 22:00:02",
                            "startTimestamp": 1527998402,
                            "userDuration": 1243,
                            "machineDuration": 1180,
                            "realDuration": 1180
                        }]
                    }, {
                        "uid":
                            2,
                        "flag":
                            0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2018-06-02 22:19:42",
                            "startTimestamp": 1527999582,
                            "userDuration": 2680,
                            "machineDuration": 2545,
                            "realDuration": 2545
                        }]
                    }]
                }]
            }]
        }
    }


@pytest.fixture(scope='module')
def fixture_queue():
    """Return a /watering/queue response."""
    return {"queue": []}


@pytest.fixture(scope='module')
def fixture_runs():
    """Return a /watering/past/<DATE>/<DAYS> response."""
    return {
        "pastValues": [{
            "pid": 3,
            "dateTimestamp": 1528005600,
            "dateTime": "2018-06-03 00:00:00",
            "used": False,
            "et0": 6.0254171309381261,
            "qpf": 0
        }, {
            "pid": 4,
            "dateTimestamp": 1528005600,
            "dateTime": "2018-06-03 00:00:00",
            "used": False,
            "et0": 6.0254171309381261,
            "qpf": 0
        }, {
            "pid": 3,
            "dateTimestamp": 1528092000,
            "dateTime": "2018-06-04 00:00:00",
            "used": False,
            "et0": 7.1343372845726805,
            "qpf": 0
        }, {
            "pid": 4,
            "dateTimestamp": 1528092000,
            "dateTime": "2018-06-04 00:00:00",
            "used": False,
            "et0": 7.1343372845726805,
            "qpf": 0
        }, {
            "pid": 1,
            "dateTimestamp": 1528005600,
            "dateTime": "2018-06-03 00:00:00",
            "used": True,
            "et0": 6.0106859434539972,
            "qpf": 0.13
        }, {
            "pid": 2,
            "dateTimestamp": 1528005600,
            "dateTime": "2018-06-03 00:00:00",
            "used": True,
            "et0": 5.6123523873214118,
            "qpf": 0
        }, {
            "pid": 1,
            "dateTimestamp": 1528092000,
            "dateTime": "2018-06-04 00:00:00",
            "used": True,
            "et0": 7.2596885196807355,
            "qpf": 0
        }, {
            "pid": 2,
            "dateTimestamp": 1528092000,
            "dateTime": "2018-06-04 00:00:00",
            "used": False,
            "et0": 7.3563610137518314,
            "qpf": 0
        }]
    }


@pytest.fixture(scope='module')
def fixture_stop_all():
    """Return a /watering/stopall response."""
    return {"statusCode": 0, "message": "OK"}


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, fixture_log, fixture_queue, fixture_runs, fixture_stop_all,
        event_loop):
    """Test all endpoints."""
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT),
        '/api/4/watering/log/details/{0}/{1}'.format(today_str, 2), 'get',
        aresponses.Response(text=json.dumps(fixture_log), status=200))
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/queue', 'get',
        aresponses.Response(text=json.dumps(fixture_queue), status=200))
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT),
        '/api/4/watering/past/{0}/{1}'.format(today_str, 2), 'get',
        aresponses.Response(text=json.dumps(fixture_runs), status=200))
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/stopall',
        'post',
        aresponses.Response(text=json.dumps(fixture_stop_all), status=200))

    # pylint: disable=protected-access
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        client._authenticated = True
        client.access_token = '12345'

        data = await client.watering.log(today, 2, details=True)
        assert len(data) == 2

        data = await client.watering.queue()
        assert not data

        data = await client.watering.runs(today, 2)
        assert len(data) == 8

        data = await client.watering.stop_all()
        assert data['message'] == 'OK'
