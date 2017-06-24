"""
file: test_auth.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=no-self-use,too-few-public-methods,redefined-outer-name

import json

import pytest
import requests
import requests_mock

import regenmaschine.auth as rma
import regenmaschine.remote_status_codes as rsc


@pytest.fixture(scope='module')
def correct_local_url():
    """ Fixture to return a valid local API URL """
    return 'https://192.168.1.100:8080/api/4'


@pytest.fixture(scope='class')
def successful_local_response():
    """ Fixture to return a successful local response """
    return {
        'access_token': '12345',
        'checksum': '12345',
        'expires_in': 157679999,
        'expiration': 'Thu, 23 Jun 2022 00:35:34 GMT',
        'statusCode': 0
    }


class TestAuthenticator(object):
    """ Class for testing a generic Authenticator object """

    @pytest.fixture(scope='class')
    def good_credentials(self, correct_local_url):
        """ Fixture to return a good credentials dict """
        return {
            'access_token': '12345',
            'api_url': correct_local_url,
            'checksum': '12345',
            'expires_in': 157679999,
            'expiration': 'Thu, 23 Jun 2022 00:35:34 GMT',
            'sprinkler_id': None,
            'status_code': 0,
            'verify_ssl': False
        }

    def test_dump(self, correct_local_url, good_credentials,
                  successful_local_response):
        """ Tests successfully dumping credentials to a dict """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/auth/login'.format(correct_local_url),
                text=json.dumps(successful_local_response))

            auth = rma.LocalAuthenticator('192.168.1.100', '12345')
            assert auth.dump() == good_credentials

    def test_dumps(self, correct_local_url, good_credentials,
                   successful_local_response):
        """ Tests successfully dumping credentials to a string """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/auth/login'.format(correct_local_url),
                text=json.dumps(successful_local_response))

            auth = rma.LocalAuthenticator('192.168.1.100', '12345')
            assert auth.dumps() == json.dumps(good_credentials)

    def test_load(self, good_credentials):
        """ Test successfully loading credentials via a dict """
        auth = rma.Authenticator.load(good_credentials)
        assert auth.dump() == good_credentials

    def test_loads(self, good_credentials):
        """ Test successfully loading credentials via a string """
        auth = rma.Authenticator.loads(json.dumps(good_credentials))
        assert auth.dump() == good_credentials


class TestLocalCredentials(object):
    """ Class for testing local credentials """

    def test_local_creds_200(self, successful_local_response,
                             correct_local_url):
        """ Tests successful credentials from local device """
        with requests_mock.Mocker() as mock:
            mock.post(
                '{}/auth/login'.format(correct_local_url),
                text=json.dumps(successful_local_response))

            auth = rma.LocalAuthenticator('192.168.1.100', '12345')
            assert auth.credentials[
                'access_token'] == successful_local_response['access_token']
            assert auth.credentials['api_url'] == correct_local_url
            assert auth.credentials['checksum'] == successful_local_response[
                'checksum']
            assert auth.credentials['expiration'] == successful_local_response[
                'expiration']
            assert auth.credentials['expires_in'] == successful_local_response[
                'expires_in']
            assert auth.credentials['sprinkler_id'] is None
            assert auth.credentials['status_code'] == 0
            assert auth.credentials['verify_ssl'] is False

    def test_local_creds_404(self):
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

    @pytest.fixture(scope='class')
    def correct_remote_url(self):
        """ Fixture to return a valid remote API URL """
        return 'https://my.rainmachine.com'

    @pytest.fixture(scope='class')
    def successful_remote_response(self):
        """ Fixture to return a successful remote response """
        return {
            "access_token": "12345",
            "errorType": 0,
            "sprinklerId": "C3aysvee"
        }

    @pytest.fixture(scope='class')
    def unsuccessful_remote_response(self):
        """ Fixture to return an unsuccessful remote response """
        return {"errorType": 1}

    def _test_remote_creds_failure(self, remote_error_code):
        """ Tests some sort of failure from remote API """
        expected_response = {"errorType": remote_error_code}
        with requests_mock.Mocker() as mock:
            mock.post(
                'https://my.rainmachine.com/login/auth',
                text=json.dumps(expected_response))

            with pytest.raises(requests.exceptions.HTTPError) as exc_info:
                rma.RemoteAuthenticator('user@host.com',
                                        '12345').get_credentials()
                assert rsc.CODES[remote_error_code] in str(exc_info)

    def test_remote_creds_200(self, correct_remote_url,
                              successful_remote_response):
        """ Tests retrieving credentials from the remote API """
        with requests_mock.Mocker() as mock:
            mock.post(
                'https://my.rainmachine.com/login/auth',
                text=json.dumps(successful_remote_response))

            auth = rma.RemoteAuthenticator('user@host.com', '12345')
            assert auth.credentials[
                'access_token'] == successful_remote_response['access_token']
            assert auth.credentials['api_url'] == '{}/s/{}/api/4'.format(
                correct_remote_url, auth.credentials['sprinkler_id'])
            assert auth.credentials['checksum'] is None
            assert auth.credentials['expiration'] is None
            assert auth.credentials['expires_in'] is None
            assert auth.credentials[
                'sprinkler_id'] == successful_remote_response['sprinklerId']
            assert auth.credentials['status_code'] is None
            assert auth.credentials['verify_ssl'] is True

    def test_remote_creds_401(self):
        """ Tests failed credentials from remote API """
        self._test_remote_creds_failure(2)

    def test_remote_creds_501(self):
        """ Tests failed credentials from remote API """
        self._test_remote_creds_failure(4)

    def test_remote_creds_404(self):
        """ Tests failed credentials from remote API """
        self._test_remote_creds_failure(5)

    def test_remote_creds_500(self):
        """ Tests failed credentials from remote API """
        self._test_remote_creds_failure(6)

    def test_remote_creds_503(self):
        """ Tests failed credentials from remote API """
        self._test_remote_creds_failure(10)

    def test_remote_creds_400(self):
        """ Tests failed credentials from remote API """
        self._test_remote_creds_failure(42)
