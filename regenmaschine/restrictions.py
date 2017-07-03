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
        return self.get('restrictions/currently').object.json()

    def hourly(self):
        """ Returns all hourly restrictions """
        return self.get('restrictions/hourly').object.json()

    def raindelay(self):
        """ Returns all restrictions due to rain """
        return self.get('restrictions/raindelay').object.json()

    def universal(self):
        """ Returns all global restrictions """
        return self.get('restrictions/global').object.json()
