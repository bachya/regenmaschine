"""
File: parser.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,invalid-name

import pytest


@pytest.fixture(scope='session')
def provision_name_response_200():
    """ Fixture to return all device information """
    return {"name": "Home"}


@pytest.fixture(scope='session')
def provision_settings_response_200():
    """ Fixture to return all device information """
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
            "hardwareVersion": 2,
            "touchLongPressTimeout": 3,
            "showRestrictionsOnLed": False,
            "parserDataSizeInDays": 6,
            "programListShowInactive": True,
            "parserHistorySize": 365,
            "allowAlexaDiscovery": True,
            "minLEDBrightness": 0,
            "minWateringDurationThreshold": 0,
            "localValveCount": 8,
            "touchAuthAPSeconds": 60,
            "useCommandLineArguments": False,
            "databasePath": "/rainmachine-app/DB/Default",
            "touchCyclePrograms": True,
            "zoneListShowInactive": True,
            "rainSensorRainStart": None,
            "zoneDuration": [300, 300, 300, 300, 300, 300, 300, 300],
            "rainSensorIsNormallyClosed": True,
            "useCorrectionForPast": True,
            "useMasterValve": False,
            "runParsersBeforePrograms": True,
            "maxWateringCoef": 2,
            "mixerHistorySize": 365
        },
        "location": {
            "elevation": 1593.45141602,
            "doyDownloaded": True,
            "zip": None,
            "windSensitivity": 0.5,
            "krs": 0.16,
            "stationID": 9172,
            "stationSource": "station",
            "et0Average": 6.578,
            "latitude": 12.1212121,
            "state": "Default",
            "stationName": "MY-STATION",
            "wsDays": 2,
            "stationDownloaded": True,
            "address": "Default",
            "rainSensitivity": 0.8,
            "timezone": "America/Pacific",
            "longitude": -999.999999,
            "name": "1234 Main Street, Los Angeles 11111, CA United States"
        }
    }


@pytest.fixture(scope='session')
def provision_wifi_response_200():
    """ Fixture to return all device information """
    return {
        "macAddress": "00:00:00:00:00:00",
        "ssid": "My Wifi",
        "netmaskAddress": "255.255.255.0",
        "hasClientLink": True,
        "mode": "managed",
        "interface": "wlan0",
        "lastWIFICheckTimestamp": 1499577959,
        "ipAddress": "192.168.1.100"
    }
