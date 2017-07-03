"""
File: stats.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import maya

import regenmaschine.api as api


class Stats(api.BaseAPI):
    """ An object to return stats """

    def on_date(self, date):
        """ Returns stats for a particular date """
        parser = maya.when(date)
        return self.get('dailystats/{}'.format(parser.datetime().strftime(
            '%Y-%m-%d'))).object.json()

    def upcoming(self, include_details=False):
        """ Returns expected stats for the next 7 days (w/ optional details)"""
        if include_details:
            return self.get('dailystats/details').object.json()

        return self.get('dailystats').object.json()
