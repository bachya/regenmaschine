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
        self.parent = super(Programs, self)
        self.parent.__init__(*args, **kwargs)

    @api.broken_remote_api
    def _broken_remote_api_test(self):  # pylint: disable=no-self-use
        """ Pure test method to test the broken_remote_api decorator """
        return {'status': 'ok'}

    def all(self):
        """ Returns all programs """
        return self.parent.get('program').object.json()

    def get(self, program_id):  # pylint: disable=arguments-differ
        """ Returns information for a specific program """
        return self.parent.get('program/{}'.format(program_id)).object.json()

    def next(self):
        """ Returns the next run date/time for all programs """
        return self.parent.get('program/nextrun').object.json()

    def running(self):
        """ Returns all running programs """
        return self.parent.get('watering/program').object.json()

    @api.broken_remote_api
    def start(self, program_id):
        """ Starts a program """
        return self.parent.post(
            'program/{}/start'.format(program_id)).object.json()

    @api.broken_remote_api
    def stop(self, program_id):
        """ Stops a program """
        return self.parent.post(
            'program/{}/stop'.format(program_id)).object.json()
