"""
File: api.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import logging

import requests
import requests.packages.urllib3 as rurllib3

import regenmaschine.exceptions as exceptions
import regenmaschine.remote_status_codes as rsc

DEFAULT_TIMEOUT = 10
LOGGER = logging.getLogger(__name__)


class Response(object):  # pylint: disable=too-few-public-methods
    """ A simple wrapper for a Requests response object """

    def __init__(self, requests_response_object):
        """ Initialize! """
        self.object = requests_response_object

    def raise_for_status(self):
        """ Encapsulation that works with local and remote errors """

        # First, check for HTTP exceptions from the local API (which seems
        # to utilize HTTP response codes correctly):
        try:
            self.object.raise_for_status()
        except requests.exceptions.HTTPError as exc_info:
            raise exceptions.HTTPError(str(exc_info))

        # The remote API is odd: it returns error codes in the body correctly,
        # but always seems to return a status of 200. If that happens, catch it
        # and set the correct code based on the API docs before moving on:
        remote_error_code = self.object.json().get('errorType')
        if remote_error_code and remote_error_code != 0:
            if remote_error_code in rsc.CODES.keys():
                error_message = rsc.CODES[remote_error_code]
            else:
                error_message = rsc.CODES[99]

            raise exceptions.HTTPError('{} for url: {}'.format(
                error_message, self.object.request.url))


class BaseAPI(object):  # pylint: disable=too-few-public-methods
    """ Base class for interacting with the RainMachine API """

    def __init__(  # pylint: disable=too-many-arguments
            self,
            url,
            using_remote_api,
            access_token=None,
            cookies=None,
            session=None,
            timeout=DEFAULT_TIMEOUT,
            verify_ssl=True):
        """ Initialize! """
        self.url = url
        self.access_token = access_token
        self.cookies = cookies
        self.timeout = timeout
        self.session = session
        self.using_remote_api = using_remote_api
        self.verify_ssl = verify_ssl

    def request(self, method_type, api_endpoint, **kwargs):
        """ Generic request method """
        kwargs.setdefault('headers', {})['Content-Type'] = 'application/json'
        if self.access_token:
            kwargs.setdefault('params', {})['access_token'] = self.access_token

        if not self.verify_ssl:
            # RainMachine uses a self-signed certificate for the local device;
            # unless it is replaced with a signed one, SSL warnings will stop
            # requests from completing, so we offer the ability to shut that
            # behavior off:
            rurllib3.disable_warnings(
                rurllib3.exceptions.InsecureRequestWarning)

        url = '{}/{}'.format(self.url, api_endpoint)
        method = getattr(self.session
                         if self.session else requests, method_type)
        resp = method(
            url,
            cookies=requests.cookies.cookiejar_from_dict(self.cookies),
            verify=self.verify_ssl,
            **kwargs)

        # The Requests object is great, but we need a little extra sugar when
        # checking for errors from the remote API, so we use a custom wrapper:
        response = Response(resp)
        response.raise_for_status()
        return response

    def get(self, api_endpoint, **kwargs):
        """ Generic GET request (prefixed to avoid future name collisions) """
        return self.request('get', api_endpoint, **kwargs)

    def post(self, api_endpoint, **kwargs):
        """ Generic POST request (prefixed to avoid future name collisions) """
        return self.request('post', api_endpoint, **kwargs)


def broken_remote_api(function):
    """ Decorator to define API calls that are broken in the remote API """

    def decorator(self, *args, **kwargs):
        """ Decorate! """
        if self.using_remote_api:
            raise exceptions.BrokenAPICall(
                '{}() currently broken in remote API'.format(
                    function.__name__))
        else:
            return function(self, *args, **kwargs)

    return decorator
