"""
File: stats.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,invalid-name

import pytest


@pytest.fixture(scope='session')
def stats_details_response_200():
    """ Fixture to return detailed stats """
    return {
        "DailyStatsDetails": [{
            "dayTimestamp":
            1498543200,
            "day":
            "2017-06-27",
            "mint":
            14,
            "maxt":
            34.56,
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
            1498629600,
            "day":
            "2017-06-28",
            "mint":
            14,
            "maxt":
            30.84,
            "icon":
            1,
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
            1498716000,
            "day":
            "2017-06-29",
            "mint":
            12.45,
            "maxt":
            26.45,
            "icon":
            3,
            "programs": [{
                "id":
                1,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1073,
                    "availableWater": 0,
                    "coefficient": 0.86,
                    "percentage": 86.290000000000012,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2313,
                    "availableWater": 0,
                    "coefficient": 0.86,
                    "percentage": 86.290000000000012,
                    "wateringFlag": 0
                }]
            }],
            "simulatedPrograms": [{
                "id":
                1,
                "zones": [{
                    "id": 2,
                    "scheduledWateringTime": 300,
                    "computedWateringTime": 259,
                    "availableWater": 0,
                    "coefficient": 0.86,
                    "percentage": 86.290000000000012
                }]
            }]
        }, {
            "dayTimestamp":
            1498802400,
            "day":
            "2017-06-30",
            "mint":
            11.56,
            "maxt":
            25.06,
            "icon":
            12,
            "programs": [{
                "id":
                1,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 713,
                    "availableWater": 0,
                    "coefficient": 0.56999999999999988,
                    "percentage": 57.35,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 1622,
                    "availableWater": 0,
                    "coefficient": 0.61,
                    "percentage": 60.52,
                    "wateringFlag": 0
                }]
            }],
            "simulatedPrograms": [{
                "id":
                1,
                "zones": [{
                    "id": 2,
                    "scheduledWateringTime": 300,
                    "computedWateringTime": 182,
                    "availableWater": 0,
                    "coefficient": 0.61,
                    "percentage": 60.52
                }]
            }]
        }, {
            "dayTimestamp":
            1498888800,
            "day":
            "2017-07-01",
            "mint":
            13.11,
            "maxt":
            28.22,
            "icon":
            1,
            "programs": [{
                "id":
                1,
                "zones": [{
                    "id": 1,
                    "scheduledWateringTime": 1243,
                    "computedWateringTime": 1125,
                    "availableWater": 0,
                    "coefficient": 0.91,
                    "percentage": 90.540000000000012,
                    "wateringFlag": 0
                }, {
                    "id": 2,
                    "scheduledWateringTime": 2680,
                    "computedWateringTime": 2426,
                    "availableWater": 0,
                    "coefficient": 0.91,
                    "percentage": 90.540000000000012,
                    "wateringFlag": 0
                }]
            }],
            "simulatedPrograms": [{
                "id":
                1,
                "zones": [{
                    "id": 2,
                    "scheduledWateringTime": 300,
                    "computedWateringTime": 272,
                    "availableWater": 0,
                    "coefficient": 0.91,
                    "percentage": 90.540000000000012
                }]
            }]
        }, {
            "dayTimestamp":
            1498975200,
            "day":
            "2017-07-02",
            "mint":
            14.22,
            "maxt":
            31.84,
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
            1499061600,
            "day":
            "2017-07-03",
            "mint":
            16,
            "maxt":
            31,
            "icon":
            1,
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
        }]
    }


@pytest.fixture(scope='session')
def stats_ondate_response_200():
    """ Fixture to return stats for a given date """
    return {
        "id": 0,
        "day": "2017-06-27",
        "mint": 14,
        "maxt": 34.56,
        "icon": 3,
        "percentage": 100,
        "wateringFlag": 0,
        "vibration": [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        "simulatedPercentage": 100,
        "simulatedVibration":
        [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    }


@pytest.fixture(scope='session')
def stats_upcoming_response_200():
    """ Fixture to return stats for a given date """
    return {
        "DailyStats": [{
            "id":
            0,
            "day":
            "2017-06-27",
            "mint":
            14,
            "maxt":
            34.56,
            "icon":
            3,
            "percentage":
            100,
            "wateringFlag":
            0,
            "vibration": [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
            "simulatedPercentage":
            100,
            "simulatedVibration":
            [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        }, {
            "id":
            1,
            "day":
            "2017-06-28",
            "mint":
            14,
            "maxt":
            30.84,
            "icon":
            1,
            "percentage":
            100,
            "wateringFlag":
            0,
            "vibration": [99, 96, 97, 98, 99, 98, 98, 95, 100, 100],
            "simulatedPercentage":
            100,
            "simulatedVibration": [99, 96, 97, 98, 99, 98, 98, 95, 100, 100]
        }, {
            "id":
            2,
            "day":
            "2017-06-29",
            "mint":
            12.45,
            "maxt":
            26.45,
            "icon":
            3,
            "percentage":
            86.31,
            "wateringFlag":
            0,
            "vibration": [98, 97, 98, 96, 98, 97, 92, 93, 93, 86],
            "simulatedPercentage":
            86.33,
            "simulatedVibration": [98, 97, 98, 96, 98, 97, 92, 93, 93, 86]
        }, {
            "id":
            3,
            "day":
            "2017-06-30",
            "mint":
            11.56,
            "maxt":
            25.06,
            "icon":
            12,
            "percentage":
            59.52,
            "wateringFlag":
            0,
            "vibration": [92, 94, 47, 65, 87, 86, 63, 61, 60, 60],
            "simulatedPercentage":
            60.67,
            "simulatedVibration": [92, 94, 48, 66, 87, 86, 64, 62, 60, 61]
        }, {
            "id":
            4,
            "day":
            "2017-07-01",
            "mint":
            13.11,
            "maxt":
            28.22,
            "icon":
            1,
            "percentage":
            90.52,
            "wateringFlag":
            0,
            "vibration": [100, 100, 92, 90, 94, 92, 89, 85, 90, 91],
            "simulatedPercentage":
            90.67,
            "simulatedVibration": [100, 100, 92, 90, 94, 92, 89, 85, 90, 91]
        }, {
            "id": 5,
            "day": "2017-07-02",
            "mint": 14.22,
            "maxt": 31.84,
            "icon": 3,
            "percentage": 100,
            "wateringFlag": 0,
            "vibration": [89, 100, 95, 98, 100, 100],
            "simulatedPercentage": 100,
            "simulatedVibration": [90, 100, 95, 98, 100, 100]
        }, {
            "id": 6,
            "day": "2017-07-03",
            "mint": 16,
            "maxt": 31,
            "icon": 1,
            "percentage": 100,
            "wateringFlag": 0,
            "vibration": [100, 100],
            "simulatedPercentage": 100,
            "simulatedVibration": [100, 100]
        }]
    }
