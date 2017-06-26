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
def local_auth_response_200():
    """ Fixture to return a successful local response """
    return {
        'access_token': '12345',
        'checksum': '12345',
        'expires_in': 157679999,
        'expiration': 'Thu, 23 Jun 2022 00:35:34 GMT',
        'statusCode': 0
    }


@pytest.fixture(scope='session')
def local_cookies():
    """ Fixture to return a local cookie jar """
    return {'access_token': '12345'}


@pytest.fixture(scope='session')
def local_credentials(local_cookies, local_url):
    """ Fixture to return a good credentials dict """
    return {
        'access_token': '12345',
        'api_url': local_url,
        'checksum': '12345',
        'cookies': local_cookies,
        'expires_in': 157679999,
        'expiration': 'Thu, 23 Jun 2022 00:35:34 GMT',
        'sprinkler_id': None,
        'status_code': 0,
        'verify_ssl': False
    }


@pytest.fixture(scope='session')
def local_url():
    """ Fixture to return a valid local API URL """
    return 'https://192.168.1.100:8080/api/4'


@pytest.fixture(scope='session')
def programs_get_response_200():
    """ Fixture to return a good set of /program data """
    return {
        "programs": [{
            "uid":
            1,
            "name":
            "Default Watering Schedule",
            "active":
            True,
            "startTime":
            "06:00",
            "cycles":
            0,
            "soak":
            0,
            "cs_on":
            False,
            "delay":
            0,
            "delay_on":
            False,
            "status":
            0,
            "startTimeParams": {
                "offsetSign": 0,
                "type": 0,
                "offsetMinutes": 0
            },
            "frequency": {
                "type": 0,
                "param": "0"
            },
            "coef":
            0.0,
            "ignoreInternetWeather":
            False,
            "futureField1":
            0,
            "freq_modified":
            0,
            "useWaterSense":
            False,
            "nextRun":
            "2017-06-26",
            "startDate":
            "2017-05-29",
            "endDate":
            None,
            "yearlyRecurring":
            True,
            "simulationExpired":
            False,
            "wateringTimes": [{
                "id": 1,
                "order": 1,
                "name": "Backyard Landscaping",
                "duration": 0,
                "active": True,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 2,
                "order": 2,
                "name": "Planter Box",
                "duration": 0,
                "active": True,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 3,
                "order": 3,
                "name": "Zone 3",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 4,
                "order": 4,
                "name": "Zone 4",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 5,
                "order": 5,
                "name": "Zone 5",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 6,
                "order": 6,
                "name": "Zone 6",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 7,
                "order": 7,
                "name": "Zone 7",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }, {
                "id": 8,
                "order": 8,
                "name": "Zone 8",
                "duration": 0,
                "active": False,
                "userPercentage": 1.0,
                "minRuntimeCoef": 1
            }]
        }]
    }


@pytest.fixture(scope='session')
def remote_auth_response_200():
    """ Fixture to return a successful remote response """
    return {"access_token": "12345", "errorType": 0, "sprinklerId": "C3aysvee"}


@pytest.fixture(scope='session')
def remote_auth_response_400():
    """ Fixture to return an unsuccessful remote response """
    return {"errorType": 1}


@pytest.fixture(scope='session')
def remote_cookies():
    """ Fixture to return a local cookie jar """
    return {'connect.sid': '12345'}


@pytest.fixture(scope='session')
def remote_credentials(remote_cookies, remote_url, sprinkler_id):
    """ Fixture to return a good credentials dict """
    return {
        'access_token': '12345',
        'api_url': '{}/s/{}/api/4'.format(remote_url, sprinkler_id),
        'checksum': None,
        'cookies': remote_cookies,
        'expires_in': None,
        'expiration': None,
        'sprinkler_id': sprinkler_id,
        'status_code': None,
        'verify_ssl': True
    }


@pytest.fixture(scope='session')
def remote_url():
    """ Fixture to return a valid remote API URL """
    return 'https://my.rainmachine.com'


@pytest.fixture(scope='session')
def sprinkler_id():
    """ Fixture to return a sprinkler ID """
    return 'C3aysvee'
