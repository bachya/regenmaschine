"""
File: exceptions.py
Author: yourname
Email: yourname@email.com
Github: https://github.com/yourname
Description:
    """


class BrokenAPICall(Exception):
    """ This API call doesn't work on both local _and_ remote APIs """
    pass


class InvalidAuthenticator(Exception):
    """ Could not create an Authenticator from the provided data """
    pass
