"""
File: provision.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api


class Provision(api.BaseAPI):  # pylint: disable=too-few-public-methods
    """ An object to return device information """

    def device_name(self):
        """ Returns the device name """
        return self.get('provision/name').object.json()

    def settings(self):
        """ Returns all device settings """
        return self.get('provision').object.json()

    def wifi(self):
        """ Returns all device settings """
        return self.get('provision/wifi').object.json()
