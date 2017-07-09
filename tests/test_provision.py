"""
file: test_parser.py
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
from tests.fixtures.provision import *


def test_all_operations(local_cookies, local_url, local_auth_response_200,
                        provision_name_response_200,
                        provision_settings_response_200,
                        provision_wifi_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/provision'.format(local_url),
            text=json.dumps(provision_settings_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/provision/name'.format(local_url),
            text=json.dumps(provision_name_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/provision/wifi'.format(local_url),
            text=json.dumps(provision_wifi_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth).provision
        assert client.device_name() == provision_name_response_200
        assert client.settings() == provision_settings_response_200
        assert client.wifi() == provision_wifi_response_200
