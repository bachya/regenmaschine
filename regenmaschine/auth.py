"""
File: auth.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import json

import regenmaschine.api as api
import regenmaschine.client as cli

API_LOCAL_BASE = 'https://{}:8080/api/4'
API_REMOTE_BASE = 'https://my.rainmachine.com'

__all__ = ['Authenticator', 'LocalAuthenticator', 'RemoteAuthenticator']


class Authenticator(api.BaseAPI):
    """ Generic authentication object """

    def __init__(self, url):
        """ Initialize! """
        self.api_endpoint = None
        self.credentials = None
        self.data = None
        self.url = url
        super(Authenticator, self).__init__(self.url)

    def _get_credentials(self, verify_ssl=True):
        """ Retrieves access token (and related info) from the API """
        response = self.post(
            self.api_endpoint, data=json.dumps(self.data), verify=verify_ssl)
        return {
            'access_token':
            response.body.get('access_token'),
            'api_url':
            self.url if response.body.get('sprinklerId') is None else
            '{}/s/{}/api/4'.format(self.url, response.body.get('sprinklerId')),
            'checksum':
            response.body.get('checksum'),
            'expires_in':
            response.body.get('expires_in'),
            'expiration':
            response.body.get('expiration'),
            'sprinkler_id':
            response.body.get('sprinklerId'),
            'status_code':
            response.body.get('statusCode'),
            'verify_ssl':
            verify_ssl
        }

    def create_client(self):
        """ Create a client with the correct info """
        return cli.Client(self.credentials)

    def dump(self):
        """ Return a nice dict representation of the Authenticator """
        return self.credentials

    def dumps(self):
        """ Return a string version of the Authenticator (for easy caching) """
        return json.dumps(self.credentials)

    @classmethod
    def load(cls, json_dict):
        """ Creates an Authenticator from a dict """
        klass = cls('http://www.whatever.com')
        klass.credentials = json_dict
        return klass

    @classmethod
    def loads(cls, json_str):
        """ Creates an Authenticator from a string """
        klass = cls('http://www.whatever.com')
        klass.credentials = json.loads(json_str)
        return klass


class LocalAuthenticator(Authenticator):
    """ Authentication object the local device """

    def __init__(self, ip, password):
        """ Initialize! """
        super(LocalAuthenticator, self).__init__(API_LOCAL_BASE.format(ip))
        self.api_endpoint = 'auth/login'
        self.data = {'pwd': password, 'remember': 1}
        self.credentials = self._get_credentials(verify_ssl=False)


class RemoteAuthenticator(Authenticator):
    """ Authentication object the local device """

    def __init__(self, email, password):
        """ Initialize! """
        super(RemoteAuthenticator, self).__init__(API_REMOTE_BASE)
        self.api_endpoint = 'login/auth'
        self.data = {'user': {'email': email, 'pwd': password, 'remember': 1}}
        self.credentials = self._get_credentials()
