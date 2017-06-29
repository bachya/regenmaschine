"""
file: test_diagnostics.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=no-self-use,too-few-public-methods,redefined-outer-name
# pylint: disable=wildcard-import,unused-wildcard-import,invalid-name

import json

import requests_mock

import regenmaschine as rm
from tests.fixtures.auth import *
from tests.fixtures.diagnostics import *
from tests.fixtures.misc import *


def test_all_operations(diagnostics_current_response_200,
                        diagnostics_log_response_200, local_cookies, local_url,
                        local_auth_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/diag'.format(local_url),
            text=json.dumps(diagnostics_current_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/diag/log'.format(local_url),
            text=json.dumps(diagnostics_log_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth).diagnostics
        assert client.current() == diagnostics_current_response_200
        assert client.log() == diagnostics_log_response_200
