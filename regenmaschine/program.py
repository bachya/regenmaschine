"""
File: program.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api


class Programs(api.BaseAPI):
    """ An object to list, interact with, etc. programs """

    def all(self):
        """ Returns all programs """
        return self._get('program').body

    def get(self, program_id):
        """ Returns information for a specific program """
        return self._get('program/{}'.format(program_id)).body

    def next(self):
        """ Returns the next run date/time for all programs """
        return self._get('program/nextrun').body

    def running(self):
        """ Returns all running programs """
        return self._get('watering/program').body

    def start(self, program_id):
        """ Starts a program """
        return self._post('program/{}/start'.format(program_id)).body

    def stop(self, program_id):
        """ Stops a program """
        return self._post('program/{}/stop'.format(program_id)).body
