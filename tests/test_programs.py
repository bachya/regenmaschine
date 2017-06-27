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


def test_local_all(local_cookies, local_url, local_auth_response_200,
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


def test_local_get(local_cookies, local_url, local_auth_response_200,
                   programs_get_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/program/1'.format(local_url),
            text=json.dumps(programs_get_response_200),
            cookies=local_cookies)

        auth = rm.LocalAuthenticator('192.168.1.100', '12345')
        client = rm.Client(auth)
        assert client.programs.get(1) == programs_get_response_200


def test_local_nextrun(local_cookies, local_url, local_auth_response_200,
                       local_nextrun_response_200):
    """ Tests getting the program list """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/program/nextrun'.format(local_url),
            text=json.dumps(local_nextrun_response_200),
            cookies=local_cookies)

        auth = rm.LocalAuthenticator('192.168.1.100', '12345')
        client = rm.Client(auth)
        assert client.programs.next() == local_nextrun_response_200


def test_local_running(local_cookies, local_url, local_auth_response_200,
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


def test_local_start_stop(client_general_response_200, local_auth_response_200,
                          local_cookies, local_url):
    """ Tests general GET requests """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.post(
            '{}/program/1/delete'.format(local_url),
            text=json.dumps(client_general_response_200),
            cookies=local_cookies)
        mock.post(
            '{}/program/1/start'.format(local_url),
            text=json.dumps(client_general_response_200),
            cookies=local_cookies)
        mock.post(
            '{}/program/1/stop'.format(local_url),
            text=json.dumps(client_general_response_200),
            cookies=local_cookies)

        auth = rm.LocalAuthenticator('192.168.1.100', '12345')
        client = rm.Client(auth)
        assert client.programs.start(1) == client_general_response_200
        assert client.programs.stop(1) == client_general_response_200
