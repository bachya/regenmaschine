"""Define tests for program endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT


@pytest.fixture(scope='session')
def fixture_device_name():
    """Return a /provision/name response."""
    return {"name": "My House"}


@pytest.fixture(scope='module')
def fixture_settings():
    """Return a /provision response."""
    return {
        "system": {
            "httpEnabled": True,
            "rainSensorSnoozeDuration": 0,
            "uiUnitsMetric": False,
            "programZonesShowInactive": False,
            "programSingleSchedule": False,
            "standaloneMode": False,
            "masterValveAfter": 0,
            "touchSleepTimeout": 10,
            "selfTest": False,
            "useSoftwareRainSensor": False,
            "defaultZoneWateringDuration": 300,
            "maxLEDBrightness": 40,
            "simulatorHistorySize": 0,
            "vibration": False,
            "masterValveBefore": 0,
            "touchProgramToRun": None,
            "useRainSensor": False,
            "wizardHasRun": True,
            "waterLogHistorySize": 365,
            "netName": "Home",
            "softwareRainSensorMinQPF": 5,
            "touchAdvanced": False,
            "useBonjourService": True,
            "hardwareVersion": 3,
            "touchLongPressTimeout": 3,
            "showRestrictionsOnLed": False,
            "parserDataSizeInDays": 6,
            "programListShowInactive": True,
            "parserHistorySize": 365,
            "allowAlexaDiscovery": False,
            "automaticUpdates": True,
            "minLEDBrightness": 0,
            "minWateringDurationThreshold": 0,
            "localValveCount": 12,
            "touchAuthAPSeconds": 60,
            "useCommandLineArguments": False,
            "databasePath": "/rainmachine-app/DB/Default",
            "touchCyclePrograms": True,
            "zoneListShowInactive": True,
            "rainSensorRainStart": None,
            "zoneDuration": [
                300,
                300,
                300,
                300,
                300,
                300,
                300,
                300,
                300,
                300,
                300,
                300
            ],
            "rainSensorIsNormallyClosed": True,
            "useCorrectionForPast": True,
            "useMasterValve": False,
            "runParsersBeforePrograms": True,
            "maxWateringCoef": 2,
            "mixerHistorySize": 365
        },
        "location": {
            "elevation": 1593.4514160199999,
            "doyDownloaded": True,
            "zip": None,
            "windSensitivity": 0.5,
            "krs": 0.16,
            "stationID": 9172,
            "stationSource": "station",
            "et0Average": 6.5780000000000003,
            "latitude": 21.037234682342,
            "state": "Default",
            "stationName": "MY STATION",
            "wsDays": 2,
            "stationDownloaded": True,
            "address": "Default",
            "rainSensitivity": 0.80000000000000004,
            "timezone": "America/Los Angeles",
            "longitude": -87.12872612,
            "name": "123 Main Street, Boston, MA 01234"
        }
    }


@pytest.fixture(scope='session')
def fixture_wifi():
    """Return a /provision/wifi response."""
    return {
        "macAddress": "ab:cd:ef:12:34:56",
        "ssid": None,
        "netmaskAddress": None,
        "hasClientLink": False,
        "mode": None,
        "interface": "wlan0",
        "lastWIFICheckTimestamp": 1525126177,
        "ipAddress": "192.168.1.100"
    }


@pytest.mark.asyncio
async def test_endpoints(aresponses, fixture_device_name, fixture_settings,
                         fixture_wifi, event_loop):
    """Test retrieving all programs."""
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/provision', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_settings), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/provision/name', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_device_name), status=200))
    aresponses.add('{0}:{1}'.format(TEST_HOST, TEST_PORT),
                   '/api/4/provision/wifi', 'get',
                   aresponses.Response(
                       text=json.dumps(fixture_wifi), status=200))

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
