# -*- coding: utf-8 -*-
"""
File: api.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

import json

import requests

DEFAULT_TIMEOUT = 10

__all__ = ['BaseAPI']


class Response(object):  # pylint: disable=too-few-public-methods
    """
    A class lovingly borred from Slacker (https://github.com/os/slacker)
    """

    def __init__(self, requests_response_object):
        """ Initialize! """
        self.body = requests_response_object.json()
        self.error = None
        self.raw = requests_response_object.text
        self.request_url = requests_response_object.request.url
        self.successful = requests_response_object.ok

    def __str__(self):
        """ Defines how this class should be printed """
        return json.dumps(self.body)


class BaseAPI(object):
    """ Base class for interacting with the RainMachine API """

    def __init__(self,
                 url,
                 access_token=None,
                 session=None,
                 timeout=DEFAULT_TIMEOUT):
        """ Initialize! """
        self.url = url
        self.access_token = access_token
        self.timeout = timeout
        self.session = session

    def _request(self, method, api_endpoint, **kwargs):
        """ Generic request method """
        kwargs.setdefault('headers', {})['Content-Type'] = 'application/json'
        if self.access_token:
            kwargs.setdefault('params', {})['access_token'] = self.access_token

        _response = method('{}/{}'.format(self.url, api_endpoint), **kwargs)
        _response.raise_for_status()
        response = Response(_response)

        # The remote API is odd: it returns error codes in the body somewhat
        # correctly, but always seems to return a status of 200. If that
        # happens, catch it and set the correct code based on the API docs
        # before moving on:
        remote_error_code = response.body.get('errorType')
        if remote_error_code and remote_error_code != 0:
            response.successful = False
            if remote_error_code == 2:
                response.error = '401 Client Error: Unauthorized'
            elif remote_error_code == 4:
                response.error = '501 Client Error: Not Implemented'
            elif remote_error_code == 5:
                response.error = '404 Client Error: Not Found'
            elif remote_error_code == 6:
                response.error = '500 Client Error: Internal Server Error'
            elif remote_error_code == 10:
                response.error = '503 Client Error: Service Unavailable'
            else:
                response.error = '400 Client Error: Bad Request'

        if not response.successful:
            raise requests.exceptions.HTTPError(
                '{} for url: {}'.format(response.error, response.request_url))

        return response

    def _session_get(self, url, params=None, **kwargs):
        """ Session-based GET request """
        kwargs.setdefault('allow_redirects', True)
        return self.session.request(
            method='get', url=url, params=params, **kwargs)

    def _session_post(self, url, data=None, **kwargs):
        """ Session-based GET request """
        kwargs.setdefault('allow_redirects', True)
        return self.session.request(
            method='post', url=url, data=data, **kwargs)

    def get(self, api_endpoint, **kwargs):
        """ Generic GET request """
        return self._request(self._session_get if self.session else
                             requests.get, api_endpoint, **kwargs)

    def post(self, api_endpoint, **kwargs):
        """ Generic GET request """
        return self._request(self._session_post if self.session else
                             requests.post, api_endpoint, **kwargs)
