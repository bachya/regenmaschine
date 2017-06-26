"""
File: program.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api


class Programs(api.BaseAPI):  # pylint: disable=too-few-public-methods
    """ An object to list, interact with, etc. programs """

    def get(self):
        """ Returns raw JSON of all program information """
        return self._get('program').body
