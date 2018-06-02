"""
File: parser.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import maya

import regenmaschine.api as api


class Watering(api.BaseAPI):
    """ An alternate object to deal with any watering-related activities """

    def log(self, date=None, num_of_days=None, details=False):
        """ Returns the current watering log """
        if details:
            api_route = 'watering/log/details'
        else:
            api_route = 'watering/log'

        if date and num_of_days:
            parser = maya.when(date)
            date = parser.datetime().strftime('%Y-%m-%d')
            api_route = '{}/{}/{}'.format(api_route, date, num_of_days)

        return self.get(api_route).object.json()

    def queue(self):
        """ Returns the queue of active watering activities """
        return self.get('watering/queue').object.json()

    def runs(self, date, num_of_days):
        """ Similar to log, but returns et0 and qpf info, as well """
        parser = maya.when(date)
        date = parser.datetime().strftime('%Y-%m-%d')
        return self.get(
            'watering/past/{}/{}'.format(date, num_of_days)).object.json()

    def stop_all(self):
        """ Stops all programs and zones from running """
        return self.post('watering/stopall').object.json()
