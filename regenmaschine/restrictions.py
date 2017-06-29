"""
File: restrictions.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api


class Restrictions(api.BaseAPI):
    """ An object to return retstrictions """

    def current(self):
        """ Returns all current restrictions """
        return self._get('restrictions/currently').body

    def hourly(self):
        """ Returns all hourly restrictions """
        return self._get('restrictions/hourly').body

    def raindelay(self):
        """ Returns all restrictions due to rain """
        return self._get('restrictions/raindelay').body

    def universal(self):
        """ Returns all global restrictions """
        return self._get('restrictions/global').body
