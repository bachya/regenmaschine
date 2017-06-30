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
from tests.fixtures.watering import *


def test_all_operations(
        client_general_response_200, local_cookies, local_url,
        local_auth_response_200, watering_log_response_200,
        watering_logdate_response_200, watering_logdatedetails_response_200,
        watering_logdetails_response_200, watering_queue_response_200,
        watering_runs_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/watering/log'.format(local_url),
            text=json.dumps(watering_log_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/watering/log/2017-06-29/2'.format(local_url),
            text=json.dumps(watering_logdate_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/watering/log/details'.format(local_url),
            text=json.dumps(watering_logdetails_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/watering/log/details/2017-06-29/2'.format(local_url),
            text=json.dumps(watering_logdatedetails_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/watering/queue'.format(local_url),
            text=json.dumps(watering_queue_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/watering/past/2017-06-29/2'.format(local_url),
            text=json.dumps(watering_runs_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/watering/stopall'.format(local_url),
            text=json.dumps(client_general_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth).watering
        assert client.log() == watering_log_response_200
        assert client.log('2017-06-29', 2) == watering_logdate_response_200
        assert client.log('6/29/2017', 2) == watering_logdate_response_200
        assert client.log(details=True) == watering_logdetails_response_200
        assert client.log(
            '2017-06-29', 2,
            details=True) == watering_logdatedetails_response_200
        assert client.log(
            '6/29/2017', 2,
            details=True) == watering_logdatedetails_response_200
        assert client.queue() == watering_queue_response_200
        assert client.runs('2017-06-29', 2) == watering_runs_response_200
        assert client.runs('6/29/2017', 2) == watering_runs_response_200
        assert client.stop_all() == client_general_response_200
