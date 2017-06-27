"""
File: auth.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import json

import regenmaschine.api as api

API_LOCAL_BASE = 'https://{}:8080/api/4'
API_REMOTE_BASE = 'https://my.rainmachine.com'

__all__ = ['Authenticator', 'InvalidAuthenticator']


class InvalidAuthenticator(Exception):
    """ Generic auth error """
    pass

# pylint: disable=too-many-instance-attributes
class Authenticator(api.BaseAPI):
    """ Generic authentication object """

    def __init__(self, url, session=None):
        """ Initialize! """
        self.api_endpoint = None
        self.api_url = None
        self.checksum = None
        self.data = None
        self.expiration = None
        self.expires_in = None
        self.session = session
        self.sprinkler_id = None
        self.status_code = None
        self.url = url
        super(Authenticator, self).__init__(self.url, session=self.session)

    def authenticate(self):
        """ Retrieves access token (and related info) from the API """
        response = self._post(self.api_endpoint, data=json.dumps(self.data))
        self.access_token = response.body.get('access_token')
        self.api_url = self.url if response.body.get(
            'sprinklerId') is None else '{}/s/{}/api/4'.format(
                self.url, response.body.get('sprinklerId'))
        self.checksum = response.body.get('checksum')
        self.cookies = response.cookies.get_dict()
        self.expiration = response.body.get('expiration')
        self.expires_in = response.body.get('expires_in')
        self.sprinkler_id = response.body.get('sprinklerId')
        self.status_code = response.body.get('statusCode')

    @classmethod
    def create_local(cls, ip_address, password, session=None):
        """ Creates a local authenticator"""
        klass = cls(API_LOCAL_BASE.format(ip_address), session)
        klass.api_endpoint = 'auth/login'
        klass.data = {'pwd': password, 'remember': 1}
        klass.verify_ssl = False
        klass.authenticate()
        return klass

    @classmethod
    def create_remote(cls, email, password, session=None):
        """ Creates a local authenticator"""
        klass = cls(API_REMOTE_BASE, session)
        klass.api_endpoint = 'login/auth'
        klass.data = {'user': {'email': email, 'pwd': password, 'remember': 1}}
        klass.authenticate()
        return klass

    def dump(self):
        """ Return a nice dict representation of the Authenticator """
        return self.__dict__

    def dumps(self):
        """ Return a string version of the Authenticator (for easy caching) """
        return json.dumps(self.__dict__)

    @classmethod
    def load(cls, auth_dict):
        """ Creates an Authenticator from a dict """
        try:
            klass = cls(auth_dict['url'])
            for k, v in auth_dict.items():  # pylint: disable=invalid-name
                setattr(klass, k, v)
            return klass
        except KeyError:
            raise InvalidAuthenticator('Invalid Authenticator data')

    @classmethod
    def loads(cls, auth_str):
        """ Creates an Authenticator from a string """
        try:
            auth_dict = json.loads(auth_str)
            return cls.load(auth_dict)
        except json.decoder.JSONDecodeError:
            raise InvalidAuthenticator('Invalid Authenticator data')
