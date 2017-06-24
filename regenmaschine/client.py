"""
File: client.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

API_URL_LOCAL = 'https://{}:8080/api/4'
API_URL_REMOTE = 'https://my.rainmachine.com/s/{}/api/4/'

__all__ = ['Client']


class Client():
    """ A client to interact with the bulk of the RainMachine API """

    def __init__(self, credentials):
        """ Initialize! """
        self.url = credentials['api_url']
        # self.access_token = access_token
        # self.session = session
        # self.timeout = timeout
        api_args = {}
