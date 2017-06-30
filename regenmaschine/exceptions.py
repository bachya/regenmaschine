"""
File: exceptions.py
Author: yourname
Email: yourname@email.com
Github: https://github.com/yourname
Description:
    """


class BrokenAPICall(Exception):
    """ Exception for when RainMachine's API is broken """
    pass


class InvalidAuthenticator(Exception):
    """ Generic auth error """
    pass
