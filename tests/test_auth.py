"""
file: test_auth.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=no-self-use,too-few-public-methods,redefined-outer-name
# pylint: disable=wildcard-import,unused-wildcard-import

import json

import pytest
import requests
import requests_mock

import regenmaschine.auth as rma
import regenmaschine.remote_status_codes as rsc
from tests.fixtures import *


class TestAuthenticator(object):
    """ Class for testing a generic Authenticator object """

    def test_dump(self, local_url, local_cookies,
                  local_credentials, local_auth_response_200):
        """ Tests successfully dumping credentials to a dict """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/auth/login'.format(local_url),
                text=json.dumps(local_auth_response_200),
                cookies=local_cookies)

            auth = rma.LocalAuthenticator('192.168.1.100', '12345')
            assert auth.dump() == local_credentials

    def test_dumps(self, local_cookies, local_credentials,
                   local_auth_response_200, local_url):
        """ Tests successfully dumping credentials to a string """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/auth/login'.format(local_url),
                text=json.dumps(local_auth_response_200),
                cookies=local_cookies)

            auth = rma.LocalAuthenticator('192.168.1.100', '12345')
            assert auth.dumps() == json.dumps(local_credentials)

    def test_load(self, local_credentials):
        """ Test successfully loading credentials via a dict """
        auth = rma.Authenticator.load(local_credentials)
        assert auth.dump() == local_credentials

    def test_loads(self, local_credentials):
        """ Test successfully loading credentials via a string """
        auth = rma.Authenticator.loads(json.dumps(local_credentials))
        assert auth.dump() == local_credentials


class TestLocalAuthenticator(object):
    """ Class for testing local credentials """

    def test_local_200(self, local_cookies, local_credentials,
                       local_auth_response_200, local_url):
        """ Tests successful credentials from local device """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/auth/login'.format(local_url),
                text=json.dumps(local_auth_response_200),
                cookies=local_cookies)

            auth = rma.LocalAuthenticator('192.168.1.100', '12345')
            assert auth.credentials == local_credentials

    def test_local_404(self):
        """ Tests failed credentials from local device """
        url = 'https://192.168.1.100:8080/api/4/auth/login'
        with requests_mock.Mocker() as mock:
            mock.post(
                url,
                exc=requests.exceptions.HTTPError(
                    '404 Client Error: Not Found in url: {}'.format(url)))

            with pytest.raises(requests.exceptions.HTTPError) as exc_info:
                rma.LocalAuthenticator('192.168.1.100', '12345')
                assert '404 Client Error: Not Found' in str(exc_info)


class TestRemoteCredentials(object):
    """ Class for testing remote credentials """

    def _test_remote_failure(self, remote_error_code):
        """ Tests some sort of failure from remote API """
        expected_response = {"errorType": remote_error_code}
        with requests_mock.Mocker() as mock:
            mock.post(
                'https://my.rainmachine.com/login/auth',
                text=json.dumps(expected_response),
                cookies=local_cookies)

            with pytest.raises(requests.exceptions.HTTPError) as exc_info:
                rma.RemoteAuthenticator('user@host.com',
                                        '12345').get_credentials()
                assert rsc.CODES[remote_error_code] in str(exc_info)

    def test_remote_200(self, remote_cookies,
                        remote_auth_response_200, remote_credentials,
                        remote_url):
        """ Tests retrieving credentials from the remote API """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/login/auth'.format(remote_url),
                text=json.dumps(remote_auth_response_200),
                cookies=remote_cookies)

            auth = rma.RemoteAuthenticator('user@host.com', '12345')
            assert auth.credentials == remote_credentials

    def test_remote_401(self):
        """ Tests failed credentials from remote API """
        self._test_remote_failure(2)

    def test_remote_501(self):
        """ Tests failed credentials from remote API """
        self._test_remote_failure(4)

    def test_remote_404(self):
        """ Tests failed credentials from remote API """
        self._test_remote_failure(5)

    def test_remote_500(self):
        """ Tests failed credentials from remote API """
        self._test_remote_failure(6)

    def test_remote_503(self):
        """ Tests failed credentials from remote API """
        self._test_remote_failure(10)

    def test_remote_400(self):
        """ Tests failed credentials from remote API """
        self._test_remote_failure(42)
