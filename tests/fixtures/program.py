"""
File: fixtures.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name

import pytest


@pytest.fixture(scope='session')
def programs_nextrun_response_200():
    """ Fixture to return a successful local response """
    return {'nextRuns': [{'pid': 1, 'startTime': '06:00'}]}


@pytest.fixture(scope='session')
def programs_all_response_200(programs_get_response_200):
    """ Fixture to return a good set of /program data """
    return {'programs': [programs_get_response_200]}


@pytest.fixture(scope='session')
def programs_get_response_200():
    """ Fixture to return info on a single program """
    return {
        'uid':
        1,
        'name':
        'Default Watering Schedule',
        'active':
        True,
        'startTime':
        '06:00',
        'cycles':
        0,
        'soak':
        0,
        'cs_on':
        False,
        'delay':
        0,
        'delay_on':
        False,
        'status':
        0,
        'startTimeParams': {
            'offsetSign': 0,
            'type': 0,
            'offsetMinutes': 0
        },
        'frequency': {
            'type': 0,
            'param': '0'
        },
        'coef':
        0.0,
        'ignoreInternetWeather':
        False,
        'futureField1':
        0,
        'freq_modified':
        0,
        'useWaterSense':
        False,
        'nextRun':
        '2017-06-26',
        'startDate':
        '2017-05-29',
        'endDate':
        None,
        'yearlyRecurring':
        True,
        'simulationExpired':
        False,
        'wateringTimes': [{
            'id': 1,
            'order': 1,
            'name': 'Backyard Landscaping',
            'duration': 0,
            'active': True,
            'userPercentage': 1.0,
            'minRuntimeCoef': 1
        }, {
            'id': 2,
            'order': 2,
            'name': 'Planter Box',
            'duration': 0,
            'active': True,
            'userPercentage': 1.0,
            'minRuntimeCoef': 1
        }, {
            'id': 3,
            'order': 3,
            'name': 'Zone 3',
            'duration': 0,
            'active': False,
            'userPercentage': 1.0,
            'minRuntimeCoef': 1
        }, {
            'id': 4,
            'order': 4,
            'name': 'Zone 4',
            'duration': 0,
            'active': False,
            'userPercentage': 1.0,
            'minRuntimeCoef': 1
        }, {
            'id': 5,
            'order': 5,
            'name': 'Zone 5',
            'duration': 0,
            'active': False,
            'userPercentage': 1.0,
            'minRuntimeCoef': 1
        }, {
            'id': 6,
            'order': 6,
            'name': 'Zone 6',
            'duration': 0,
            'active': False,
            'userPercentage': 1.0,
            'minRuntimeCoef': 1
        }, {
            'id': 7,
            'order': 7,
            'name': 'Zone 7',
            'duration': 0,
            'active': False,
            'userPercentage': 1.0,
            'minRuntimeCoef': 1
        }, {
            'id': 8,
            'order': 8,
            'name': 'Zone 8',
            'duration': 0,
            'active': False,
            'userPercentage': 1.0,
            'minRuntimeCoef': 1
        }]
    }


@pytest.fixture(scope='session')
def programs_running_response_200():
    """ Fixture to return running programs """
    return {
        'programs': [{
            'uid': 1,
            'name': 'Default Watering Schedule',
            'manual': True,
            'userStartTime': '2017-06-26 16:12:00',
            'realStartTime': '2017-06-26 16:12:55',
            'status': 1
        }]
    }
