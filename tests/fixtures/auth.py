"""
File: auth_fixtures.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name

import pytest


@pytest.fixture(scope='session')
def local_auth(local_cookies, local_url):
    """ Fixture to return a good credentials dict """
    return {
        'access_token': '12345',
        'api_endpoint': 'auth/login',
        'api_url': local_url,
        'checksum': '12345',
        'cookies': local_cookies,
        'data': {
            'pwd': '12345',
            'remember': 1
        },
        'expiration': 'Thu, 23 Jun 2022 00:35:34 GMT',
        'expires_in': 157679999,
        'session': None,
        'sprinkler_id': None,
        'status_code': 0,
        'timeout': 10,
        'url': local_url,
        'verify_ssl': False,
    }


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
def remote_auth_response_200(sprinkler_id):
    """ Fixture to return a successful remote response """
    return {
        "access_token": "12345",
        "errorType": 0,
        "sprinklerId": sprinkler_id
    }


@pytest.fixture(scope='session')
def remote_auth_response_400():
    """ Fixture to return an unsuccessful remote response """
    return {"errorType": 1}


@pytest.fixture(scope='session')
def remote_cookies():
    """ Fixture to return a local cookie jar """
    return {'connect.sid': '12345'}


@pytest.fixture(scope='session')
def remote_auth(remote_cookies, remote_url, sprinkler_id):
    """ Fixture to return a good credentials dict """
    return {
        'access_token': '12345',
        'api_endpoint': 'login/auth',
        'api_url': '{}/s/{}/api/4'.format(remote_url, sprinkler_id),
        'checksum': None,
        'cookies': remote_cookies,
        'data': {
            'user': {
                'email': 'user@host.com',
                'pwd': '12345',
                'remember': 1
            }
        },
        'expiration': None,
        'expires_in': None,
        'session': None,
        'sprinkler_id': sprinkler_id,
        'status_code': None,
        'timeout': 10,
        'url': remote_url,
        'verify_ssl': True,
    }
