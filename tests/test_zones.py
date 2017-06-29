"""
file: test_zones.py
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
from tests.fixtures.auth import *
from tests.fixtures.misc import *
from tests.fixtures.zone import *


def test_local_all(local_cookies, local_url, local_auth_response_200,
                   zones_all_response_200, zones_all_advanced_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/zone'.format(local_url),
            text=json.dumps(zones_all_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/zone/properties'.format(local_url),
            text=json.dumps(zones_all_advanced_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth)
        assert client.zones.all() == zones_all_response_200
        assert client.zones.all(
            advanced_properties=True) == zones_all_advanced_response_200


def test_local_get(local_cookies, local_url, local_auth_response_200,
                   zones_get_response_200, zones_get_advanced_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/zone/1'.format(local_url),
            text=json.dumps(zones_get_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/zone/1/properties'.format(local_url),
            text=json.dumps(zones_get_advanced_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth)
        assert client.zones.get(1) == zones_get_response_200
        assert client.zones.get(
            1, advanced_properties=True) == zones_get_advanced_response_200

def test_local_start_stop(client_general_response_200, local_auth_response_200,
                          local_cookies, local_url):
    """ Tests general GET requests """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.post(
            '{}/zone/1/start'.format(local_url),
            text=json.dumps(client_general_response_200),
            cookies=local_cookies)
        mock.post(
            '{}/zone/1/stop'.format(local_url),
            text=json.dumps(client_general_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth)
        assert client.zones.start(1, 60) == client_general_response_200
        assert client.zones.stop(1) == client_general_response_200
