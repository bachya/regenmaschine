'''
File: zones.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
'''

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,invalid-name

import pytest


@pytest.fixture(scope='session')
def diagnostics_current_response_200():
    ''' Fixture to return local device diagnostic info '''
    return {
        'hasWifi': True,
        'uptime': '18 days, 16:16:48',
        'uptimeSeconds': 1613808,
        'memUsage': 16188,
        'networkStatus': True,
        'bootCompleted': True,
        'lastCheckTimestamp': 1498597977,
        'wizardHasRun': True,
        'standaloneMode': False,
        'cpuUsage': 0.0,
        'lastCheck': '2017-06-27 15:12:57',
        'softwareVersion': '4.0.900',
        'internetStatus': True,
        'locationStatus': True,
        'timeStatus': True,
        'wifiMode': 'managed',
        'gatewayAddress': '192.168.1.1',
        'cloudStatus': 0,
        'weatherStatus': True
    }


@pytest.fixture(scope='session')
def diagnostics_log_response_200():
    ''' Fixture to return a log snippet '''
    return {
        'log': '--------------------------- GENERAL RAINMACHINE LOG --------'
    }
