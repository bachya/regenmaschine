"""
File: client.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.api as api
import regenmaschine.diagnostics as diagnostics
import regenmaschine.program as program
import regenmaschine.parser as parser
import regenmaschine.provision as provision
import regenmaschine.restrictions as restrictions
import regenmaschine.stats as stats
import regenmaschine.watering as watering
import regenmaschine.zone as zone


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class Client(object):
    """ A client to interact with the bulk of the RainMachine API """

    def __init__(self, auth, timeout=api.DEFAULT_TIMEOUT):
        """ Initialize! """
        self.auth = auth
        kwargs = {
            'url': auth.api_url,
            'access_token': auth.access_token,
            'cookies': auth.cookies,
            'session': auth.session,
            'timeout': timeout,
            'using_remote_api': auth.using_remote_api,
            'verify_ssl': auth.verify_ssl
        }

        self.diagnostics = diagnostics.Diagnostics(**kwargs)
        self.parsers = parser.Parsers(**kwargs)
        self.programs = program.Programs(**kwargs)
        self.provision = provision.Provision(**kwargs)
        self.restrictions = restrictions.Restrictions(**kwargs)
        self.stats = stats.Stats(**kwargs)
        self.watering = watering.Watering(**kwargs)
        self.zones = zone.Zones(**kwargs)
