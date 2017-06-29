"""
File: zones.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name

import pytest


@pytest.fixture(scope='session')
def zones_all_response_200(zones_get_response_200):
    """ Fixture to return info on all zones """
    return {"zones": [zones_get_response_200]}


@pytest.fixture(scope='session')
def zones_all_advanced_response_200(zones_get_advanced_response_200):
    """ Fixture to return info on all zones """
    return {"zones": [zones_get_advanced_response_200]}


@pytest.fixture(scope='session')
def zones_get_response_200():
    """ Fixture to return info on a single zone """
    return {
        "uid": 1,
        "name": "Backyard Landscaping",
        "state": 0,
        "active": True,
        "userDuration": 0,
        "machineDuration": 0,
        "remaining": 0,
        "cycle": 0,
        "noOfCycles": 0,
        "restriction": False,
        "type": 4,
        "master": False,
        "waterSense": False
    }


@pytest.fixture(scope='session')
def zones_get_advanced_response_200():
    """ Fixture to return info on a single zone """
    return {
        "uid": 1,
        "name": "Backyard Landscaping",
        "valveid": 1,
        "ETcoef": 0.8,
        "active": True,
        "type": 4,
        "internet": True,
        "savings": 100,
        "slope": 1,
        "sun": 1,
        "soil": 1,
        "group_id": 4,
        "history": True,
        "master": False,
        "before": 0,
        "after": 0,
        "waterSense": {
            "fieldCapacity":
            0.3,
            "rootDepth":
            229,
            "minRuntime":
            -1,
            "appEfficiency":
            0.75,
            "isTallPlant":
            True,
            "permWilting":
            0.03,
            "allowedSurfaceAcc":
            6.6,
            "maxAllowedDepletion":
            0.5,
            "precipitationRate":
            25.4,
            "currentFieldCapacity":
            30.92,
            "area":
            92.9,
            "referenceTime":
            1243,
            "detailedMonthsKc":
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            "flowrate":
            None,
            "soilIntakeRate":
            5.08
        }
    }
