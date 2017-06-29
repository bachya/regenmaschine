"""
File: parser.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,invalid-name

import pytest


# pylint: disable=line-too-long
@pytest.fixture(scope='session')
def parser_current_response_200():
    """ Fixture to return information on the current parser(s) """
    return {
        "parsers": [{
            "lastRun":
            None,
            "lastKnownError":
            "",
            "hasForecast":
            False,
            "uid":
            7,
            "hasHistorical":
            True,
            "description":
            "Florida Automated Weather Network observations",
            "enabled":
            False,
            "custom":
            False,
            "params": {
                "station": 480,
                "useHourly": False
            },
            "isRunning":
            False,
            "name":
            "FAWN Parser"
        }, {
            "lastRun":
            None,
            "lastKnownError":
            "",
            "hasForecast":
            False,
            "uid":
            8,
            "hasHistorical":
            True,
            "description":
            "Personal Weather Station direct data download in pws format",
            "enabled":
            False,
            "custom":
            False,
            "params": {
                "urlPath": "http://weather-display.com/windy/clientraw.txt",
                "maxAllowedDistance": 100000
            },
            "isRunning":
            False,
            "name":
            "PWS Parser"
        }, {
            "lastRun":
            None,
            "lastKnownError":
            "",
            "hasForecast":
            False,
            "uid":
            1,
            "hasHistorical":
            True,
            "description":
            "Weather observations from NetAtmo personal weather station",
            "enabled":
            False,
            "custom":
            False,
            "params": {
                "username": "",
                "useSpecifiedModules": False,
                "_availableModules": [],
                "specificModules": "",
                "password": ""
            },
            "isRunning":
            False,
            "name":
            "Netatmo Parser"
        }, {
            "lastRun":
            None,
            "lastKnownError":
            "",
            "hasForecast":
            False,
            "uid":
            3,
            "hasHistorical":
            True,
            "description":
            "California Irrigation Management Information System weather stations",
            "enabled":
            False,
            "custom":
            False,
            "params": {
                "appKey": None,
                "customStation": True,
                "station": 2,
                "historicDays": 5
            },
            "isRunning":
            False,
            "name":
            "CIMIS Parser"
        }, {
            "lastRun":
            "2017-06-27 11:53:01",
            "lastKnownError":
            "",
            "hasForecast":
            True,
            "uid":
            2,
            "hasHistorical":
            True,
            "description":
            "Global weather service with personal weather station access from Weather Underground",
            "enabled":
            True,
            "custom":
            False,
            "params": {
                "useSolarRadiation":
                False,
                "apiKey":
                "477a5ecd9c2b825e",
                "useCustomStation":
                True,
                "_nearbyStationsIDList": [
                    "KCOAUROR53(0km; lat=39.69, lon=-104.77)",
                    "KCOAUROR53(0km; lat=39.69, lon=-104.77)",
                    "KCOAUROR87(0km; lat=39.7, lon=-104.78)",
                    "KCOAUROR70(1km; lat=39.7, lon=-104.78)",
                    "KCOAUROR79(2km; lat=39.67, lon=-104.76)",
                    "KCOAUROR128(2km; lat=39.7, lon=-104.8)",
                    "KCOHUTCH2(3km; lat=39.67, lon=-104.76)",
                    "KCOAUROR108(3km; lat=39.66, lon=-104.77)",
                    "KCOAUROR33(3km; lat=39.67, lon=-104.79)",
                    "KCOAUROR43(3km; lat=39.66, lon=-104.78)",
                    "KCOAUROR112(3km; lat=39.68, lon=-104.73)",
                    "KCOAUROR92(3km; lat=39.67, lon=-104.8)",
                    "KCOAUROR131(3km; lat=39.68, lon=-104.81)",
                    "KCOAUROR172(4km; lat=39.66, lon=-104.8)",
                    "KCOAUROR130(4km; lat=39.67, lon=-104.82)",
                    "KCOAUROR47(4km; lat=39.66, lon=-104.81)",
                    "KCOAUROR14(5km; lat=39.67, lon=-104.82)",
                    "KCOAUROR147(5km; lat=39.64, lon=-104.77)",
                    "KCOAUROR59(5km; lat=39.65, lon=-104.8)",
                    "KCOAUROR39(5km; lat=39.64, lon=-104.79)",
                    "KCOAUROR89(6km; lat=39.69, lon=-104.84)",
                    "KCOAUROR100(6km; lat=39.72, lon=-104.83)",
                    "KCOAUROR98(6km; lat=39.75, lon=-104.8)",
                    "KCOAUROR169(6km; lat=39.71, lon=-104.84)",
                    "KCOAUROR74(6km; lat=39.66, lon=-104.84)",
                    "KCOAUROR123(6km; lat=39.66, lon=-104.84)",
                    "KCOAUROR71(7km; lat=39.64, lon=-104.82)"
                ],
                "_airportStationsIDList": [
                    "KBKF(16km; lat=39.7, lon=-104.75)",
                    "KAPA(26km; lat=39.57, lon=-104.85)",
                    "KDEN(20km; lat=39.86, lon=-104.67)",
                    "KFTG(30km; lat=39.79, lon=-104.54)"
                ],
                "customStationName":
                "KCOAUROR53"
            },
            "isRunning":
            False,
            "name":
            "WUnderground Parser"
        }, {
            "lastRun":
            None,
            "lastKnownError":
            "",
            "hasForecast":
            True,
            "uid":
            4,
            "hasHistorical":
            False,
            "description":
            "Global weather service from https://darksky.net (forecast.io)",
            "enabled":
            False,
            "custom":
            False,
            "params": {
                "appKey": None
            },
            "isRunning":
            False,
            "name":
            "ForecastIO Parser"
        }, {
            "lastRun":
            None,
            "lastKnownError":
            "",
            "hasForecast":
            True,
            "uid":
            9,
            "hasHistorical":
            False,
            "description":
            "Global weather service from Norwegian Meteorological Institute http://met.no",
            "enabled":
            False,
            "custom":
            False,
            "isRunning":
            False,
            "name":
            "METNO Parser"
        }, {
            "lastRun":
            None,
            "lastKnownError":
            "",
            "hasForecast":
            True,
            "uid":
            5,
            "hasHistorical":
            True,
            "description":
            "RainMachine Weather Rules with WUnderground instant data. This feature is in early development do not enable unless you know what you are doing.",
            "enabled":
            False,
            "custom":
            False,
            "params": {
                "apiKey":
                "",
                "rules":
                "[\n                {\n                  \"variable\": \"temperature\",\n                  \"operator\": \">\",\n                  \"value\": 36,\n                  \"action\": \"log\",\n                  \"params\": {\"msg\": \"Temperature over 36 degrees\"}\n                }\n              ]",
                "stationName":
                "",
                "_observations": {},
                "_actions": ["log"]
            },
            "isRunning":
            False,
            "name":
            "Weather Rules Parser"
        }, {
            "lastRun":
            "2017-06-27 11:53:01",
            "lastKnownError":
            "",
            "hasForecast":
            True,
            "uid":
            6,
            "hasHistorical":
            False,
            "description":
            "North America weather forecast from National Oceanic and Atmospheric Administration",
            "enabled":
            True,
            "custom":
            False,
            "isRunning":
            False,
            "name":
            "NOAA Parser"
        }]
    }
