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
from tests.fixtures.stats import *


def test_all_operations(local_cookies, local_url, local_auth_response_200,
                        stats_details_response_200, stats_ondate_response_200,
                        stats_upcoming_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/dailystats/2017-06-29'.format(local_url),
            text=json.dumps(stats_ondate_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/dailystats'.format(local_url),
            text=json.dumps(stats_upcoming_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/dailystats/details'.format(local_url),
            text=json.dumps(stats_details_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth).stats
        assert client.on_date('2017-06-29') == stats_ondate_response_200
        assert client.on_date('6/29/2017') == stats_ondate_response_200
        assert client.upcoming() == stats_upcoming_response_200
        assert client.upcoming(True) == stats_details_response_200
