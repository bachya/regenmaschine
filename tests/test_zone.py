"""Define tests for program endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT


@pytest.fixture(scope='module')
def fixture_all():
    """Return a /zone/properties response."""
    return {
        "zones": [{
            "uid": 1,
            "name": "Landscaping",
            "valveid": 1,
            "ETcoef": 0.80000000000000004,
            "active": True,
            "type": 4,
            "internet": True,
            "savings": 100,
            "slope": 1,
            "sun": 1,
            "soil": 5,
            "group_id": 4,
            "history": True,
            "master": False,
            "before": 0,
            "after": 0,
            "waterSense": {
                "fieldCapacity": 0.17000000000000001,
                "rootDepth": 229,
                "minRuntime": -1,
                "appEfficiency": 0.75,
                "isTallPlant": True,
                "permWilting": 0.029999999999999999,
                "allowedSurfaceAcc": 8.3800000000000008,
                "maxAllowedDepletion": 0.5,
                "precipitationRate": 25.399999999999999,
                "currentFieldCapacity": 16.030000000000001,
                "area": 92.900001525878906,
                "referenceTime": 1243,
                "detailedMonthsKc": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                "flowrate": None,
                "soilIntakeRate": 10.16
            },
            "customSoilPreset": None,
            "customVegetationPreset": None,
            "customSprinklerPreset": None
        }]
    }


@pytest.fixture(scope='module')
def fixture_get():
    """Return a /zone/<ID>/properties response."""
    return {
        "uid": 1,
        "name": "Landscaping",
        "valveid": 1,
        "ETcoef": 0.80000000000000004,
        "active": True,
        "type": 4,
        "internet": True,
        "savings": 100,
        "slope": 1,
        "sun": 1,
        "soil": 5,
        "group_id": 4,
        "history": True,
        "master": False,
        "before": 0,
        "after": 0,
        "waterSense": {
            "fieldCapacity": 0.17000000000000001,
            "rootDepth": 229,
            "minRuntime": -1,
            "appEfficiency": 0.75,
            "isTallPlant": True,
            "permWilting": 0.029999999999999999,
            "allowedSurfaceAcc": 8.3800000000000008,
            "maxAllowedDepletion": 0.5,
            "precipitationRate": 25.399999999999999,
            "currentFieldCapacity": 16.030000000000001,
            "area": 92.900001525878906,
            "referenceTime": 1243,
            "detailedMonthsKc": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            "flowrate": None,
            "soilIntakeRate": 10.16
        },
        "customSoilPreset": None,
        "customVegetationPreset": None,
        "customSprinklerPreset": None
    }


@pytest.fixture(scope='module')
def fixture_start_stop():
    """Return a response for /program/<ID>/start and /program/<ID>/stop."""
    return {"statusCode": 0, "message": "OK"}


@pytest.mark.asyncio
async def test_endpoints(aresponses, fixture_all, fixture_get,
                         fixture_start_stop, event_loop):
    """Test all endpoints."""
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/zone/properties', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_all), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/zone/1/properties', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_get), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/zone/1/start', 'post',
                   aresponses.Response(
                       text=json.dumps(fixture_start_stop), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/zone/1/stop', 'post',
                   aresponses.Response(
                       text=json.dumps(fixture_start_stop), status=200))

    # pylint: disable=protected-access
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TEST_HOST, websession, port=TEST_PORT, ssl=False)
        client._authenticated = True
        client._access_token = '12345'

        data = await client.zones.all(details=True)
        assert len(data) == 1
        assert data[0]['name'] == 'Landscaping'

        data = await client.zones.get(1, details=True)
        assert data['name'] == 'Landscaping'

        data = await client.zones.start(1, 60)
        assert data['message'] == 'OK'

        data = await client.zones.stop(1)
        assert data['message'] == 'OK'
