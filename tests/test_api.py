"""
file: test_api.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=no-self-use,too-few-public-methods,redefined-outer-name
# pylint: disable=wildcard-import,unused-wildcard-import

import json

import pytest
import requests_mock

import regenmaschine as rm
from tests.fixtures.auth import *
from tests.fixtures.misc import *
from tests.fixtures.program import *


def test_bad_api_call(local_url):
    """ Tests a bad API call (and that it raises an exception) """
    with requests_mock.Mocker() as mock:
        mock.post('{}/auth/login'.format(local_url), status_code=404)

        with pytest.raises(rm.exceptions.HTTPError) as exc_info:
            rm.Authenticator.create_local('192.168.1.100', '12345')
            assert '404' in str(exc_info)


def test_cookies(local_auth_response_200, local_cookies, local_url,
                 programs_all_response_200):
    """ Tests connection pooling with a session """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/program'.format(local_url),
            text=json.dumps(programs_all_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth)
        assert client.programs.all() == programs_all_response_200
        assert client.programs.cookies == local_cookies
