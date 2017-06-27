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
def client_general_response_200():
    """ Fixture to return a valid response for most operations """
    return {"statusCode": 0, "message": "OK"}


@pytest.fixture(scope='session')
def local_url():
    """ Fixture to return a valid local API URL """
    return 'https://192.168.1.100:8080/api/4'


@pytest.fixture(scope='session')
def remote_url():
    """ Fixture to return a valid remote API URL """
    return 'https://my.rainmachine.com'


@pytest.fixture(scope='session')
def sprinkler_id():
    """ Fixture to return a sprinkler ID """
    return 'C3aysvee'
