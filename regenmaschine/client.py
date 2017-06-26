"""
File: client.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api
import regenmaschine.program as program


class Client(object):  # pylint: disable=too-few-public-methods
    """ A client to interact with the bulk of the RainMachine API """

    def __init__(self, auth, timeout=api.DEFAULT_TIMEOUT):
        """ Initialize! """
        self.auth = auth
        kwargs = {
            'url': auth.api_url,
            'access_token': auth.access_token,
            'cookies': auth.cookies,
            'session': auth.session,
            'timeout': timeout,
            'verify_ssl': auth.verify_ssl
        }

        self.programs = program.Programs(**kwargs)
