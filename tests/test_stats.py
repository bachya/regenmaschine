"""Define tests for stat endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import datetime
import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT


@pytest.fixture(scope='module')
def fixture_on_date():
    """Return a /dailystats/<DATE> response."""
    return {
        "id": 0,
        "day": "2018-06-04",
        "mint": 12.779999999999999,
        "maxt": 33.329999999999998,
        "icon": 2,
        "percentage": 100,
        "wateringFlag": 0,
        "vibration": [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        "simulatedPercentage": 100,
        "simulatedVibration": [100, 100, 100, 100, 100, 100, 100, 100, 100]
    }


@pytest.fixture(scope='module')
def fixture_upcoming():
    """Return a /dailystats/details response."""
    return {
        "DailyStatsDetails": [{
            "dayTimestamp":
                1528092000,
            "day":
                "2018-06-04",
            "mint":
                12.779999999999999,
            "maxt":
                33.329999999999998,
            "icon":
                2,
            "programs": [{
                "id":
                    1,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    2,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    3,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    4,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }],
            "simulatedPrograms": [{
                "id":
                    1,
                "zones": [{
                    "id": 2,
                    "scheduledWateringTime": 300,
                    "computedWateringTime": 300,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100
                }]
            }]
        }, {
            "dayTimestamp":
                1528178400,
            "day":
                "2018-06-05",
            "mint":
                13.890000000000001,
            "maxt":
                34.439999999999998,
            "icon":
                3,
            "programs": [{
                "id":
                    1,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    2,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    3,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    4,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }],
            "simulatedPrograms": [{
                "id":
                    1,
                "zones": [{
                    "id": 2,
                    "scheduledWateringTime": 300,
                    "computedWateringTime": 300,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100
                }]
            }]
        }, {
            "dayTimestamp":
                1528264800,
            "day":
                "2018-06-06",
            "mint":
                14.44,
            "maxt":
                32.780000000000001,
            "icon":
                3,
            "programs": [{
                "id":
                    1,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    2,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }],
            "simulatedPrograms": [{
                "id":
                    1,
                "zones": [{
                    "id": 2,
                    "scheduledWateringTime": 300,
                    "computedWateringTime": 300,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100
                }]
            }]
        }, {
            "dayTimestamp":
                1528351200,
            "day":
                "2018-06-07",
            "mint":
                13.890000000000001,
            "maxt":
                33.890000000000001,
            "icon":
                3,
            "programs": [{
                "id":
                    1,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    2,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }],
            "simulatedPrograms": [{
                "id":
                    1,
                "zones": [{
                    "id": 2,
                    "scheduledWateringTime": 300,
                    "computedWateringTime": 300,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100
                }]
            }]
        }, {
            "dayTimestamp":
                1528437600,
            "day":
                "2018-06-08",
            "mint":
                13.890000000000001,
            "maxt":
                34.439999999999998,
            "icon":
                3,
            "programs": [{
                "id":
                    1,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    2,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }],
            "simulatedPrograms": [{
                "id":
                    1,
                "zones": [{
                    "id": 2,
                    "scheduledWateringTime": 300,
                    "computedWateringTime": 300,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100
                }]
            }]
        }, {
            "dayTimestamp":
                1528524000,
            "day":
                "2018-06-09",
            "mint":
                14.44,
            "maxt":
                33.890000000000001,
            "icon":
                3,
            "programs": [{
                "id":
                    1,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }, {
                "id":
                    2,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1243,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2680,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100,
                    "wateringFlag": 0
                }]
            }],
            "simulatedPrograms": [{
                "id":
                    1,
                "zones": [{
                    "id": 2,
                    "scheduledWateringTime": 300,
                    "computedWateringTime": 300,
                    "availableWater": 0,
                    "coefficient": 1.0,
                    "percentage": 100
                }]
            }]
        }, {
            "dayTimestamp": 1528610400,
            "day": "2018-06-10",
            "mint": None,
            "maxt": None,
            "icon": None,
            "programs": [],
            "simulatedPrograms": []
        }]
    }


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, fixture_on_date, fixture_upcoming, event_loop):
    """Test all endpoints."""
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT),
        '/api/4/dailystats/{0}'.format(today_str), 'get',
        aresponses.Response(text=json.dumps(fixture_on_date), status=200))
    aresponses.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/dailystats/details',
        'get',
        aresponses.Response(text=json.dumps(fixture_upcoming), status=200))

    # pylint: disable=protected-access
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        client._authenticated = True
        client._access_token = '12345'

        data = await client.stats.on_date(today)
        assert data['percentage'] == 100

        data = await client.stats.upcoming(details=True)
        assert len(data[0]['programs']) == 4
