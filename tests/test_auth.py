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
import requests_mock

import regenmaschine as rm
import regenmaschine.remote_status_codes as rsc
from tests.fixtures.auth import *
from tests.fixtures.misc import *


class TestAuthenticator(object):
    """ Class for testing a generic Authenticator object """

    def test_dump(self, local_url, local_cookies, local_auth,
                  local_auth_response_200):
        """ Tests successfully dumping credentials to a dict """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/auth/login'.format(local_url),
                text=json.dumps(local_auth_response_200),
                cookies=local_cookies)

            auth = rm.Authenticator.create_local('192.168.1.100', '12345')
            assert auth.dump() == local_auth

    def test_dumps(self, local_cookies, local_auth, local_auth_response_200,
                   local_url):
        """ Tests successfully dumping credentials to a string """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/auth/login'.format(local_url),
                text=json.dumps(local_auth_response_200),
                cookies=local_cookies)

            auth = rm.Authenticator.create_local('192.168.1.100', '12345')
            assert json.loads(auth.dumps()) == json.loads(
                json.dumps(local_auth))

    def test_load(self, local_auth):
        """ Test successfully loading credentials via a dict """
        auth = rm.Authenticator.load(local_auth)
        assert auth.dump() == local_auth

        with pytest.raises(rm.exceptions.InvalidAuthenticator):
            bad_local_auth = {}
            auth = rm.Authenticator.load(bad_local_auth)

    def test_loads(self, local_auth):
        """ Test successfully loading credentials via a string """
        auth = rm.Authenticator.loads(json.dumps(local_auth))
        assert auth.dump() == local_auth

        with pytest.raises(rm.exceptions.InvalidAuthenticator):
            bad_local_auth = "This can't possibly work!"
            auth = rm.Authenticator.loads(bad_local_auth)


class TestLocalAuthenticator(object):
    """ Class for testing local credentials """

    def test_local_200(self, local_cookies, local_auth,
                       local_auth_response_200, local_url):
        """ Tests successful credentials from local device """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/auth/login'.format(local_url),
                text=json.dumps(local_auth_response_200),
                cookies=local_cookies)

            auth = rm.Authenticator.create_local('192.168.1.100', '12345')
            assert auth.dump() == local_auth

    def test_local_404(self):
        """ Tests failed credentials from local device """
        url = 'https://192.168.1.100:8080/api/4/auth/login'
        with requests_mock.Mocker() as mock:
            mock.post(
                url,
                exc=rm.exceptions.HTTPError(
                    '404 Client Error: Not Found in url: {}'.format(url)))

            with pytest.raises(rm.exceptions.HTTPError) as exc_info:
                rm.Authenticator.create_local('192.168.1.100', '12345')
                assert '404 Client Error: Not Found' in str(exc_info)

    def test_local_different_port(self, local_auth_response_200):
        """ Tests setting a different port for local connections """
        url = 'https://192.168.1.100:80/api/4/auth/login'
        with requests_mock.Mocker() as mock:
            mock.post(url, text=json.dumps(local_auth_response_200))

            auth = rm.Authenticator.create_local(
                '192.168.1.100', '12345', port=80)
            assert ':80/' in auth.url

    def test_local_http_https(self, local_auth_response_200):
        """ Tests setting a different port for local connections """
        http_url = 'http://192.168.1.100:80/api/4/auth/login'
        https_url = 'https://192.168.1.100:8080/api/4/auth/login'
        with requests_mock.Mocker() as mock:
            mock.post(http_url, text=json.dumps(local_auth_response_200))
            mock.post(https_url, text=json.dumps(local_auth_response_200))

            http_auth = rm.Authenticator.create_local(
                '192.168.1.100', '12345', port=80, https=False)
            https_auth = rm.Authenticator.create_local(
                '192.168.1.100', '12345', port=8080, https=True)
            assert 'http://' in http_auth.url
            assert 'https://' in https_auth.url


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

            with pytest.raises(rm.exceptions.HTTPError) as exc_info:
                rm.Authenticator.create_remote('user@host.com', '12345')
                assert rsc.CODES[remote_error_code] in str(exc_info)

    def test_remote_200(self, remote_cookies, remote_auth_response_200,
                        remote_auth, remote_url):
        """ Tests retrieving credentials from the remote API """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/login/auth'.format(remote_url),
                text=json.dumps(remote_auth_response_200),
                cookies=remote_cookies)

            auth = rm.Authenticator.create_remote('user@host.com', '12345')
            assert auth.dump() == remote_auth

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
