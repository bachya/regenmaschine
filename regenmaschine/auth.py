"""
File: auth.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import json

import regenmaschine.api as api
import regenmaschine.exceptions as exceptions

API_LOCAL_BASE = 'https://{}:8080/api/4'
API_REMOTE_BASE = 'https://my.rainmachine.com'


# pylint: disable=too-many-instance-attributes
class Authenticator(api.BaseAPI):
    """ Generic authentication object """

    def __init__(self, url, using_remote_api, session=None):
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
        self.using_remote_api = using_remote_api
        super(Authenticator, self).__init__(
            self.url, self.using_remote_api, session=self.session)

    def authenticate(self):
        """ Retrieves access token (and related info) from the API """
        response = self.post(self.api_endpoint, json=self.data)
        data = response.object.json()
        self.access_token = data.get('access_token')
        self.api_url = self.url if data.get(
            'sprinklerId') is None else '{}/s/{}/api/4'.format(
                self.url, data.get('sprinklerId'))
        self.checksum = data.get('checksum')
        self.cookies = response.object.cookies.get_dict()
        self.expiration = data.get('expiration')
        self.expires_in = data.get('expires_in')
        self.sprinkler_id = data.get('sprinklerId')
        self.status_code = data.get('statusCode')

    @classmethod
    def create_local(cls, ip_address, password, session=None):
        """ Creates a local authenticator"""
        klass = cls(API_LOCAL_BASE.format(ip_address), False, session)
        klass.api_endpoint = 'auth/login'
        klass.data = {'pwd': password, 'remember': 1}
        klass.verify_ssl = False
        klass.authenticate()
        return klass

    @classmethod
    def create_remote(cls, email, password, session=None):
        """ Creates a local authenticator"""
        klass = cls(API_REMOTE_BASE, True, session)
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
            klass = cls(auth_dict['url'], auth_dict['using_remote_api'])
            for k, v in auth_dict.items():  # pylint: disable=invalid-name
                setattr(klass, k, v)
            return klass
        except KeyError:
            raise exceptions.InvalidAuthenticator('Invalid Authenticator data')

    @classmethod
    def loads(cls, auth_str):
        """ Creates an Authenticator from a string """
        try:
            auth_dict = json.loads(auth_str)
            return cls.load(auth_dict)
        except ValueError:
            raise exceptions.InvalidAuthenticator('Invalid Authenticator data')
