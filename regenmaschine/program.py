"""
File: program.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api


class Program(object):
    """ A wrapper class to define a RainMachine program """

    def __init__(self):
        """ Initialize! """
        pass


class Programs(api.BaseAPI):
    """ An object to list, interact with, etc. programs """

    def dump(self):
        """ Returns raw JSON of all program information """
        return self.get('program').body
