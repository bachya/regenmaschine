"""
file: test_diagnostics.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,wildcard-import,unused-wildcard-import
# pylint: disable=invalid-name,too-many-arguments

import json

import requests_mock

import regenmaschine as rm
from tests.fixtures.auth import *
from tests.fixtures.misc import *
from tests.fixtures.restrictions import *


def test_all_operations(
        restrictions_current_response_200, restrictions_global_response_200,
        restrictions_hourly_response_200, restrictions_raindelay_response_200,
        local_cookies, local_url, local_auth_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/restrictions/currently'.format(local_url),
            text=json.dumps(restrictions_current_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/restrictions/global'.format(local_url),
            text=json.dumps(restrictions_global_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/restrictions/hourly'.format(local_url),
            text=json.dumps(restrictions_hourly_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/restrictions/raindelay'.format(local_url),
            text=json.dumps(restrictions_raindelay_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth).restrictions
        assert client.current() == restrictions_current_response_200
        assert client.hourly() == restrictions_hourly_response_200
        assert client.raindelay() == restrictions_raindelay_response_200
        assert client.universal() == restrictions_global_response_200
