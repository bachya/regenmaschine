# -*- coding: utf-8 -*-
"""
File: auth.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

import json

from .api import BaseAPI

BASE_URL_LOCAL = 'https://{}:8080/api/4'
BASE_URL_REMOTE = 'https://my.rainmachine.com'

__all__ = ['get_local_access_token', 'get_remote_access_token', 'Credentials']


class Credentials(object):  # pylint: disable=too-few-public-methods
    """ Normalization object to hold credential info """

    def __init__(self, credentials):
        """ Initialize! """
        if isinstance(credentials, str):
            credentials = json.loads(credentials)

        self.access_token = credentials['access_token']
        self.checksum = credentials.get('checksum')
        self.expiration = credentials.get('expiration')
        self.expires_in = credentials.get('expires_in')
        self.sprinkler_id = credentials.get('sprinklerId')

    def __str__(self):
        """ Defines how this class should be printed """
        return json.dumps(self.__dict__)


class Authenticator(BaseAPI):
    """ Generic authentication object """

    def __init__(self, url, verify_ssl=True):
        """ Initialize! """
        self.url = url
        self.verify_ssl = verify_ssl
        self.api_endpoint = None
        self.data = None
        super(Authenticator, self).__init__(self.url)

    def get_access_token(self):
        """ Retrieves access token (and related info) from the API """
        response = self.post(
            self.api_endpoint,
            data=json.dumps(self.data),
            verify=self.verify_ssl)
        return Credentials(response.body)


class LocalAuthenticator(Authenticator):
    """ Authentication object the local device """

    def __init__(self, ip, password):
        """ Initialize! """
        super(LocalAuthenticator, self).__init__(
            BASE_URL_LOCAL.format(ip), verify_ssl=False)
        self.api_endpoint = 'auth/login'
        self.data = {'pwd': password, 'remember': 1}


class RemoteAuthenticator(Authenticator):
    """ Authentication object the local device """

    def __init__(self, email, password):
        """ Initialize! """
        super(RemoteAuthenticator, self).__init__(BASE_URL_REMOTE)
        self.api_endpoint = 'login/auth'
        self.data = {'user': {'email': email, 'pwd': password, 'remember': 1}}


def get_local_access_token(ip_address, password):
    """ Convenience method to get an access token from the local device """
    return LocalAuthenticator(ip_address, password).get_access_token()


def get_remote_access_token(email, password):
    """ Convenience method to get an access token from the remote API """
    return RemoteAuthenticator(email, password).get_access_token()
