"""
File: restrictions.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,invalid-name

import pytest


@pytest.fixture(scope='session')
def restrictions_current_response_200():
    """ Fixture to return any current restrictions """
    return {
        'hourly': False,
        'freeze': False,
        'month': False,
        'weekDay': False,
        'rainDelay': False,
        'rainDelayCounter': -1,
        'rainSensor': False
    }


@pytest.fixture(scope='session')
def restrictions_global_response_200():
    """ Fixture to return any global restrictions """
    return {
        'hotDaysExtraWatering': False,
        'freezeProtectEnabled': False,
        'freezeProtectTemp': 2,
        'noWaterInWeekDays': '0000000',
        'noWaterInMonths': '000000000000',
        'rainDelayStartTime': 1497017186,
        'rainDelayDuration': 0
    }


@pytest.fixture(scope='session')
def restrictions_hourly_response_200():
    """ Fixture to return hourly restrictions """
    return {'hourlyRestrictions': []}


@pytest.fixture(scope='session')
def restrictions_raindelay_response_200():
    """ Fixture to return hourly restrictions """
    return {'delayCounter': -1}
