"""
file: test_programs.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=no-self-use,too-few-public-methods,redefined-outer-name
# pylint: disable=wildcard-import,unused-wildcard-import

import json

import requests_mock

import regenmaschine as rm
from tests.fixtures import *


def test_local_programs_all(local_cookies, local_url, local_auth_response_200,
                            programs_all_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/program'.format(local_url),
            text=json.dumps(programs_all_response_200),
            cookies=local_cookies)

        auth = rm.LocalAuthenticator('192.168.1.100', '12345')
        client = rm.Client(auth)
        assert client.programs.all() == programs_all_response_200


def test_local_programs_running(local_cookies, local_url,
                                local_auth_response_200,
                                programs_running_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/watering/program'.format(local_url),
            text=json.dumps(programs_running_response_200),
            cookies=local_cookies)

        auth = rm.LocalAuthenticator('192.168.1.100', '12345')
        client = rm.Client(auth)
        assert client.programs.running() == programs_running_response_200
