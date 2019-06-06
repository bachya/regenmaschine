"""Define fixtures related to the "watering" endpoint."""
import pytest


@pytest.fixture()
def watering_log_json():
    """Return a /watering/log/details/<DATE>/<DAYS> response."""
    return {
        "waterLog": {
            "days": [
                {
                    "date": "2018-06-01",
                    "dateTimestamp": 1527832800,
                    "programs": [
                        {
                            "id": 1,
                            "zones": [
                                {
                                    "uid": 1,
                                    "flag": 0,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-01 06:00:02",
                                            "startTimestamp": 1527854402,
                                            "userDuration": 1243,
                                            "machineDuration": 1243,
                                            "realDuration": 1243,
                                        }
                                    ],
                                },
                                {
                                    "uid": 2,
                                    "flag": 0,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-01 06:20:45",
                                            "startTimestamp": 1527855645,
                                            "userDuration": 2680,
                                            "machineDuration": 2680,
                                            "realDuration": 2680,
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "id": 2,
                            "zones": [
                                {
                                    "uid": 1,
                                    "flag": 0,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-01 22:00:01",
                                            "startTimestamp": 1527912001,
                                            "userDuration": 1243,
                                            "machineDuration": 1243,
                                            "realDuration": 1243,
                                        }
                                    ],
                                },
                                {
                                    "uid": 2,
                                    "flag": 0,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-01 22:20:44",
                                            "startTimestamp": 1527913244,
                                            "userDuration": 2680,
                                            "machineDuration": 2680,
                                            "realDuration": 2680,
                                        }
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    "date": "2018-06-02",
                    "dateTimestamp": 1527919200,
                    "programs": [
                        {
                            "id": 1,
                            "zones": [
                                {
                                    "uid": 1,
                                    "flag": 0,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-02 06:00:01",
                                            "startTimestamp": 1527940801,
                                            "userDuration": 1243,
                                            "machineDuration": 1217,
                                            "realDuration": 1217,
                                        }
                                    ],
                                },
                                {
                                    "uid": 2,
                                    "flag": 0,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-02 06:20:18",
                                            "startTimestamp": 1527942018,
                                            "userDuration": 2680,
                                            "machineDuration": 2624,
                                            "realDuration": 2624,
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "id": 0,
                            "zones": [
                                {
                                    "uid": 1,
                                    "flag": 1,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-02 20:58:54",
                                            "startTimestamp": 1527994734,
                                            "userDuration": 1243,
                                            "machineDuration": 1243,
                                            "realDuration": 6,
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "id": 0,
                            "zones": [
                                {
                                    "uid": 1,
                                    "flag": 1,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-02 21:00:40",
                                            "startTimestamp": 1527994840,
                                            "userDuration": 1243,
                                            "machineDuration": 1243,
                                            "realDuration": 3,
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "id": 0,
                            "zones": [
                                {
                                    "uid": 1,
                                    "flag": 1,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-02 21:20:03",
                                            "startTimestamp": 1527996003,
                                            "userDuration": 1243,
                                            "machineDuration": 1243,
                                            "realDuration": 3,
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "id": 0,
                            "zones": [
                                {
                                    "uid": 1,
                                    "flag": 1,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-02 21:40:41",
                                            "startTimestamp": 1527997241,
                                            "userDuration": 3,
                                            "machineDuration": 3,
                                            "realDuration": 2,
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "id": 2,
                            "zones": [
                                {
                                    "uid": 1,
                                    "flag": 0,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-02 22:00:02",
                                            "startTimestamp": 1527998402,
                                            "userDuration": 1243,
                                            "machineDuration": 1180,
                                            "realDuration": 1180,
                                        }
                                    ],
                                },
                                {
                                    "uid": 2,
                                    "flag": 0,
                                    "cycles": [
                                        {
                                            "id": 1,
                                            "startTime": "2018-06-02 22:19:42",
                                            "startTimestamp": 1527999582,
                                            "userDuration": 2680,
                                            "machineDuration": 2545,
                                            "realDuration": 2545,
                                        }
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ]
        }
    }


@pytest.fixture()
def watering_past_json():
    """Return a /watering/past/<DATE>/<DAYS> response."""
    return {
        "pastValues": [
            {
                "pid": 3,
                "dateTimestamp": 1528005600,
                "dateTime": "2018-06-03 00:00:00",
                "used": False,
                "et0": 6.0254171309381261,
                "qpf": 0,
            },
            {
                "pid": 4,
                "dateTimestamp": 1528005600,
                "dateTime": "2018-06-03 00:00:00",
                "used": False,
                "et0": 6.0254171309381261,
                "qpf": 0,
            },
            {
                "pid": 3,
                "dateTimestamp": 1528092000,
                "dateTime": "2018-06-04 00:00:00",
                "used": False,
                "et0": 7.1343372845726805,
                "qpf": 0,
            },
            {
                "pid": 4,
                "dateTimestamp": 1528092000,
                "dateTime": "2018-06-04 00:00:00",
                "used": False,
                "et0": 7.1343372845726805,
                "qpf": 0,
            },
            {
                "pid": 1,
                "dateTimestamp": 1528005600,
                "dateTime": "2018-06-03 00:00:00",
                "used": True,
                "et0": 6.0106859434539972,
                "qpf": 0.13,
            },
            {
                "pid": 2,
                "dateTimestamp": 1528005600,
                "dateTime": "2018-06-03 00:00:00",
                "used": True,
                "et0": 5.6123523873214118,
                "qpf": 0,
            },
            {
                "pid": 1,
                "dateTimestamp": 1528092000,
                "dateTime": "2018-06-04 00:00:00",
                "used": True,
                "et0": 7.2596885196807355,
                "qpf": 0,
            },
            {
                "pid": 2,
                "dateTimestamp": 1528092000,
                "dateTime": "2018-06-04 00:00:00",
                "used": False,
                "et0": 7.3563610137518314,
                "qpf": 0,
            },
        ]
    }


@pytest.fixture()
def watering_pause_json():
    """Return a /watering/pauseall response."""
    return {"statusCode": 0, "message": "OK"}


@pytest.fixture()
def watering_queue_json():
    """Return a /watering/queue response."""
    return {"queue": []}


@pytest.fixture()
def watering_stopall_json():
    """Return a /watering/stopall response."""
    return {"statusCode": 0, "message": "OK"}
