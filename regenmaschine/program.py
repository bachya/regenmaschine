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

    def __init__(self, *args, **kwargs):
        """ Initialize! """
        self.caller = super(Programs, self)
        super(Programs, self).__init__(*args, **kwargs)

    @api.broken_remote_api
    def _broken_remote_api_test(self):  #pylint: disable=no-self-use
        """ Pure test method to test the broken_remote_api decorator """
        return {'status': 'ok'}

    @staticmethod
    def _build_start_stop_endpoint(program_id, action):
        """ To make Code Climate happy... """
        return 'program/{}/{}'.format(program_id, action)

    def all(self):
        """ Returns all programs """
        return self.caller.get('program').body

    def get(self, program_id):  # pylint: disable=arguments-differ
        """ Returns information for a specific program """
        return self.caller.get('program/{}'.format(program_id)).body

    def next(self):
        """ Returns the next run date/time for all programs """
        return self.caller.get('program/nextrun').body

    def running(self):
        """ Returns all running programs """
        return self.caller.get('watering/program').body

    @api.broken_remote_api
    def start(self, program_id):
        """ Starts a program """
        return self.caller.post(
            self._build_start_stop_endpoint(program_id, 'start')).body

    @api.broken_remote_api
    def stop(self, program_id):
        """ Stops a program """
        return self.caller.post(
            self._build_start_stop_endpoint(program_id, 'stop')).body
