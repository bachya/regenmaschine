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

    def __init__(self, *args, **kwargs):
        """ Initialize! """
        self.parent = super(Zones, self)
        self.parent.__init__(*args, **kwargs)

    def all(self, properties=False):
        """ Returns all zones (optionally showing advanced properties) """
        if properties:
            return self.parent.get('zone/properties').object.json()

        return self.parent.get('zone').object.json()

    # pylint: disable=arguments-differ
    def get(self, zone_id, properties=False):
        """ Returns information for a specific zone """
        if properties:
            return self.parent.get(
                'zone/{}/properties'.format(zone_id)).object.json()

        return self.parent.get('zone/{}'.format(zone_id)).object.json()

    def simulate(self, zone_data):
        """
        Simulates a zone activity (based on advanced zone properties)
        """
        return self.parent.post('zone/simulate', json=zone_data).object.json()

    def start(self, zone_id, seconds):
        """ Starts a zone for a specific number of seconds """
        return self.parent.post(
            'zone/{}/start'.format(zone_id), json={'time':
                                                   seconds}).object.json()

    def stop(self, zone_id):
        """ Stops a zone """
        return self.parent.post('zone/{}/stop'.format(zone_id)).object.json()
