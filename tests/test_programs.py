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
from tests.fixtures.auth import *
from tests.fixtures.misc import *
from tests.fixtures.program import *


# pylint: disable=too-many-arguments
def test_all_operations(client_general_response_200, local_cookies, local_url,
                        local_auth_response_200, programs_all_response_200,
                        programs_get_response_200,
                        programs_nextrun_response_200,
                        programs_running_response_200):
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
        mock.get(
            '{}/program/nextrun'.format(local_url),
            text=json.dumps(programs_nextrun_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/program/1'.format(local_url),
            text=json.dumps(programs_get_response_200),
            cookies=local_cookies)
        mock.post(
            '{}/program/1/start'.format(local_url),
            text=json.dumps(client_general_response_200),
            cookies=local_cookies)
        mock.post(
            '{}/program/1/stop'.format(local_url),
            text=json.dumps(client_general_response_200),
            cookies=local_cookies)
        mock.get(
            '{}/watering/program'.format(local_url),
            text=json.dumps(programs_running_response_200),
            cookies=local_cookies)

        auth = rm.Authenticator.create_local('192.168.1.100', '12345')
        client = rm.Client(auth).programs
        assert client.all() == programs_all_response_200
        assert client.get(1) == programs_get_response_200
        assert client.next() == programs_nextrun_response_200
        assert client.running() == programs_running_response_200
        assert client.start(1) == client_general_response_200
        assert client.stop(1) == client_general_response_200


# pylint: disable=protected-access
def test_remote_api_broken(local_auth_response_200, local_url,
                           remote_auth_response_200, remote_url, sprinkler_id):
    """ Tests the broken_remote_api decorator """
    with requests_mock.Mocker() as mock:
        mock.post(
            '{}/login/auth'.format(remote_url),
            text=json.dumps(remote_auth_response_200),
            cookies=remote_cookies)
        mock.post(
            '{}/auth/login'.format(local_url),
            text=json.dumps(local_auth_response_200),
            cookies=local_cookies)
        mock.post(
            '{}/s/{}/api/4/program/1/start'.format(remote_url, sprinkler_id),
            exc=rm.api.BrokenAPICall('start() currently broken in remote API'))

        auth_local = rm.Authenticator.create_local('192.168.1.100', '12345')
        auth_remote = rm.Authenticator.create_remote('user@host.com', '12345')

        with pytest.raises(rm.api.BrokenAPICall) as exc_info:
            client = rm.Client(auth_remote)
            client.programs._broken_remote_api_test()
            assert 'currently broken in remote API' in str(exc_info)

        client = rm.Client(auth_local)
        assert client.programs._broken_remote_api_test() == {'status': 'ok'}
