"""
File: diagnostics.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api


class Diagnostics(api.BaseAPI):
    """ An object to return device diagnostic information """

    def current(self):
        """ Returns all current/up-to-date diagnostic information """
        return self._get('diag').body

    def log(self):
        """ Returns the entire device log """
        return self._get('diag/log').body
