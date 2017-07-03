"""
File: parser.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api


class Parsers(api.BaseAPI):  # pylint: disable=too-few-public-methods
    """ An object to return information on weather parsers """

    def current(self):
        """ Returns all current parsers """
        return self.get('parser').object.json()
