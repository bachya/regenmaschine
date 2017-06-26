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

import regenmaschine.auth as rma
from tests.fixtures import *


def test_local_programs_get(local_cookies, local_url, local_auth_response_200,
                            programs_get_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/program'.format(local_url),
            text=json.dumps(programs_get_response_200),
            cookies=local_cookies)
        auth = rma.LocalAuthenticator('192.168.1.100', '12345')
        client = auth.create_client()
        assert client.programs.all() == programs_get_response_200
