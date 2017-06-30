"""
File: zone.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api


class Zones(api.BaseAPI):
    """ An object to list, interact with, etc. zones """

    def all(self, advanced_properties=False):
        """ Returns all zones (optionally showing advanced properties) """
        if advanced_properties:
            return self._get('zone/properties').body

        return self._get('zone').body

    def get(self, zone_id, advanced_properties=False):
        """ Returns information for a specific zone """
        if advanced_properties:
            return self._get('zone/{}/properties'.format(zone_id)).body

        return self._get('zone/{}'.format(zone_id)).body

    def simulate(self, zone_data):
        """
        Simulates a zone activity (based on advanced zone properties)
        """
        return self._post('zone/simulate', data=zone_data).body

    def start(self, zone_id, seconds):
        """ Starts a zone for a specific number of seconds """
        return self._post(
            'zone/{}/start'.format(zone_id), data={'time': seconds}).body

    def stop(self, zone_id):
        """ Stops a zone """
        return self._post('zone/{}/stop'.format(zone_id)).body
