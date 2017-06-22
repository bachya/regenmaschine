"""
File: test_auth.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=no-self-use,too-few-public-methods

import json

import pytest
import requests
import requests_mock

import regenmaschine.auth as rma


class TestCredentialsObject(object):
    """ Tests for the Credentials object """

    @classmethod
    @pytest.fixture(scope='class')
    def valid_local_response(cls):
        """ Fixture to return a valid local response """
        return {
            'access_token': '12345',
            'checksum': '67890',
            'expiration': 'Mon, 20 Jun 2022 19:17:48 GMT',
            'expires_in': 157680000,
            'statusCode': 0
        }

    def test_load_credentials_obj(self, valid_local_response):
        """ Tests loading of raw data into a Credentials object """
        creds = rma.Credentials(json.dumps(valid_local_response))
        assert creds.access_token == valid_local_response['access_token']
        assert creds.checksum == valid_local_response['checksum']
        assert creds.expiration == valid_local_response['expiration']
        assert creds.expires_in == valid_local_response['expires_in']
        assert creds.sprinkler_id is None
        assert creds.status_code == 0


class TestLocalCredentials(object):
    """ Class for testing local credentials """

    def test_local_creds_200(self):
        """ Tests successful credentials from local device """
        with requests_mock.Mocker() as mock:
            expected_response_body = {
                'access_token': '12345',
                'checksum': '67890',
                'expiration': 'Mon, 20 Jun 2022 19:17:48 GMT',
                'expires_in': 157680000,
                'statusCode': 0
            }
            mock.post(
                'https://192.168.1.117:8080/api/4/auth/login',
                text=json.dumps(expected_response_body))

            creds = rma.get_local_credentials('192.168.1.117', '12345')
            assert creds.access_token == expected_response_body['access_token']
            assert creds.checksum == expected_response_body['checksum']
            assert creds.expiration == expected_response_body['expiration']
            assert creds.expires_in == expected_response_body['expires_in']
            assert creds.sprinkler_id is None

    def test_local_creds_404(self):
        """ Tests failed credentials from local device """
        url = 'https://192.168.1.117:8080/api/4/auth/login'
        with requests_mock.Mocker() as mock:
            mock.post(
                url,
                exc=requests.exceptions.HTTPError(
                    '404 Client Error: Not Found in url: {}'.format(url)))

            with pytest.raises(requests.exceptions.HTTPError) as exc_info:
                rma.get_local_credentials('192.168.1.117', '12345')
                assert '404 Client Error: Not Found' in str(exc_info)


class TestRemoteCredentials(object):
    """ Class for testing remote credentials """

    def test_remote_creds_401(self):
        """ Tests failed credentials from remote API """
        # url = 'https://my.rainmachine.com/login/auth'
        # with requests_mock.Mocker() as mock:
        #     mock.post(
        #         url,
        #         exc=requests.exceptions.HTTPError(
        #             '401 Client Error: Unauthorized in url: {}'.format(url)))

        #     with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        #         rma.get_remote_credentials('user@host.com', '12345')
        #         assert '401 Client Error: Unauthorized' in str(exc_info)

    def test_remote_credentials_success(self):
        """ Tests retrieving credentials from the remote API """
        with requests_mock.Mocker() as mock:
            expected_response_body = {
                "access_token": "12345",
                "errorType": 0,
                "sprinklerId": "C3aysvee"
            }
            mock.post(
                'https://my.rainmachine.com/login/auth',
                text=json.dumps(expected_response_body))

            creds = rma.get_remote_credentials('user@host.com', '12345')
            assert creds.access_token == expected_response_body['access_token']
            assert creds.checksum is None
            assert creds.expiration is None
            assert creds.expires_in is None
            assert creds.sprinkler_id == expected_response_body['sprinklerId']
