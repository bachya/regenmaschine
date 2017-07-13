"""
File: exceptions.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""


class BrokenAPICall(Exception):
    """ This API call doesn't work on both local _and_ remote APIs """
    pass


class HTTPError(Exception):
    """ Some sort of HTTP error occurred """
    pass


class InvalidAuthenticator(Exception):
    """ Could not create an Authenticator from the provided data """
    pass
