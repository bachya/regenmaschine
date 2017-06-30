"""
File: watering.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,invalid-name

import pytest


@pytest.fixture(scope='session')
def watering_log_response_200():
    """ Fixture to return a basic log """
    return {
        "waterLog": {
            "days": [{
                "date": "2017-06-29",
                "realDuration": 3756,
                "dayTimestamp": 1498716000,
                "userDuration": 3923
            }]
        }
    }


@pytest.fixture(scope='session')
def watering_logdate_response_200():
    """ Fixture to return log over a series of days """
    return {
        "waterLog": {
            "days": [{
                "date": "2017-06-27",
                "realDuration": 3923,
                "dayTimestamp": 1498543200,
                "userDuration": 3923
            }, {
                "date": "2017-06-28",
                "realDuration": 3923,
                "dayTimestamp": 1498629600,
                "userDuration": 3923
            }]
        }
    }


@pytest.fixture(scope='session')
def watering_logdatedetails_response_200():
    """ Fixture to return log with details over a series of days """
    return {
        "waterLog": {
            "days": [{
                "date":
                "2017-06-27",
                "dateTimestamp":
                1498543200,
                "programs": [{
                    "id":
                    1,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-27 06:00:01",
                            "startTimestamp": 1498564801,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 1243
                        }]
                    }, {
                        "uid":
                        2,
                        "flag":
                        0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-27 06:20:44",
                            "startTimestamp": 1498566044,
                            "userDuration": 2680,
                            "machineDuration": 2680,
                            "realDuration": 2680
                        }]
                    }]
                }, {
                    "id":
                    0,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-27 14:37:30",
                            "startTimestamp": 1498595850,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 2
                        }]
                    }]
                }]
            }, {
                "date":
                "2017-06-28",
                "dateTimestamp":
                1498629600,
                "programs": [{
                    "id":
                    1,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-28 06:00:02",
                            "startTimestamp": 1498651202,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 1243
                        }]
                    }, {
                        "uid":
                        2,
                        "flag":
                        0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-28 06:20:46",
                            "startTimestamp": 1498652446,
                            "userDuration": 2680,
                            "machineDuration": 2680,
                            "realDuration": 2680
                        }]
                    }]
                }, {
                    "id":
                    0,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-28 21:06:09",
                            "startTimestamp": 1498705569,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 22
                        }]
                    }]
                }, {
                    "id":
                    0,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-28 21:07:48",
                            "startTimestamp": 1498705668,
                            "userDuration": 60,
                            "machineDuration": 60,
                            "realDuration": 44
                        }]
                    }]
                }, {
                    "id":
                    0,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-28 21:20:12",
                            "startTimestamp": 1498706412,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 14
                        }]
                    }]
                }, {
                    "id":
                    0,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-28 21:21:27",
                            "startTimestamp": 1498706487,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 10
                        }]
                    }]
                }]
            }]
        }
    }


@pytest.fixture(scope='session')
def watering_logdetails_response_200():
    """ Fixture to return a log with details """
    return {
        "waterLog": {
            "days": [{
                "date":
                "2017-06-29",
                "dateTimestamp":
                1498716000,
                "programs": [{
                    "id":
                    1,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-29 06:00:02",
                            "startTimestamp": 1498737602,
                            "userDuration": 1243,
                            "machineDuration": 1187,
                            "realDuration": 1187
                        }]
                    }, {
                        "uid":
                        2,
                        "flag":
                        0,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-29 06:19:49",
                            "startTimestamp": 1498738789,
                            "userDuration": 2680,
                            "machineDuration": 2569,
                            "realDuration": 2569
                        }]
                    }]
                }, {
                    "id":
                    0,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-29 09:43:32",
                            "startTimestamp": 1498751012,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 19
                        }]
                    }]
                }, {
                    "id":
                    0,
                    "zones": [{
                        "uid":
                        1,
                        "flag":
                        1,
                        "cycles": [{
                            "id": 1,
                            "startTime": "2017-06-29 17:41:32",
                            "startTimestamp": 1498779692,
                            "userDuration": 1243,
                            "machineDuration": 1243,
                            "realDuration": 14
                        }]
                    }]
                }]
            }]
        }
    }


@pytest.fixture(scope='session')
def watering_queue_response_200():
    """ Fixture to return current watering queue """
    return {
        "queue": [{
            "availableWater": 0,
            "realDuration": 0,
            "running": True,
            "uid": None,
            "restriction": False,
            "manual": True,
            "pid": 1,
            "flag": 0,
            "machineDuration": 1243,
            "userDuration": 1243,
            "zid": 1,
            "userStartTime": "2017-06-29 17:41:00",
            "cycles": 1,
            "hwZid": 1,
            "remaining": 1233,
            "realStartTime": "2017-06-29 17:41:32",
            "cycle": 1
        }, {
            "availableWater": 0,
            "realDuration": 0,
            "running": False,
            "uid": None,
            "restriction": False,
            "manual": True,
            "pid": 1,
            "flag": 0,
            "machineDuration": 2680,
            "userDuration": 2680,
            "zid": 2,
            "userStartTime": "2017-06-29 17:41:00",
            "cycles": 1,
            "hwZid": 2,
            "remaining": 2680,
            "realStartTime": None,
            "cycle": 1
        }]
    }


@pytest.fixture(scope='session')
def watering_runs_response_200():
    """ Fixture to return runs over a series of days """
    return {
        "pastValues": [{
            "pid": 1,
            "dateTimestamp": 1498543200,
            "dateTime": "2017-06-27 00:00:00",
            "used": True,
            "et0": 7.6932501378577709,
            "qpf": 0
        }, {
            "pid": 1,
            "dateTimestamp": 1498629600,
            "dateTime": "2017-06-28 00:00:00",
            "used": True,
            "et0": 6.7601515522765934,
            "qpf": 0
        }, {
            "pid": 1,
            "dateTimestamp": 1498716000,
            "dateTime": "2017-06-29 00:00:00",
            "used": True,
            "et0": 6.371602632254194,
            "qpf": 0.25
        }]
    }
