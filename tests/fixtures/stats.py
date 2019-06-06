"""Define fixtures related to the "dailystats" endpoint."""
import pytest


@pytest.fixture()
def dailystats_date_json():
    """Return a /dailystats/<DATE> response."""
    return {
        "id": 0,
        "day": "2018-06-04",
        "mint": 12.779999999999999,
        "maxt": 33.329999999999998,
        "icon": 2,
        "percentage": 100,
        "wateringFlag": 0,
        "vibration": [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        "simulatedPercentage": 100,
        "simulatedVibration": [100, 100, 100, 100, 100, 100, 100, 100, 100],
    }


@pytest.fixture()
def dailystats_details_json():
    """Return a /dailystats/details response."""
    return {
        "DailyStatsDetails": [
            {
                "dayTimestamp": 1528092000,
                "day": "2018-06-04",
                "mint": 12.779999999999999,
                "maxt": 33.329999999999998,
                "icon": 2,
                "programs": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                    {
                        "id": 3,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            }
                        ],
                    },
                    {
                        "id": 4,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            }
                        ],
                    },
                ],
                "simulatedPrograms": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 2,
                                "scheduledWateringTime": 300,
                                "computedWateringTime": 300,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                            }
                        ],
                    }
                ],
            },
            {
                "dayTimestamp": 1528178400,
                "day": "2018-06-05",
                "mint": 13.890000000000001,
                "maxt": 34.439999999999998,
                "icon": 3,
                "programs": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                    {
                        "id": 3,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            }
                        ],
                    },
                    {
                        "id": 4,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            }
                        ],
                    },
                ],
                "simulatedPrograms": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 2,
                                "scheduledWateringTime": 300,
                                "computedWateringTime": 300,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                            }
                        ],
                    }
                ],
            },
            {
                "dayTimestamp": 1528264800,
                "day": "2018-06-06",
                "mint": 14.44,
                "maxt": 32.780000000000001,
                "icon": 3,
                "programs": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                ],
                "simulatedPrograms": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 2,
                                "scheduledWateringTime": 300,
                                "computedWateringTime": 300,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                            }
                        ],
                    }
                ],
            },
            {
                "dayTimestamp": 1528351200,
                "day": "2018-06-07",
                "mint": 13.890000000000001,
                "maxt": 33.890000000000001,
                "icon": 3,
                "programs": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                ],
                "simulatedPrograms": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 2,
                                "scheduledWateringTime": 300,
                                "computedWateringTime": 300,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                            }
                        ],
                    }
                ],
            },
            {
                "dayTimestamp": 1528437600,
                "day": "2018-06-08",
                "mint": 13.890000000000001,
                "maxt": 34.439999999999998,
                "icon": 3,
                "programs": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                ],
                "simulatedPrograms": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 2,
                                "scheduledWateringTime": 300,
                                "computedWateringTime": 300,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                            }
                        ],
                    }
                ],
            },
            {
                "dayTimestamp": 1528524000,
                "day": "2018-06-09",
                "mint": 14.44,
                "maxt": 33.890000000000001,
                "icon": 3,
                "programs": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "zones": [
                            {
                                "id": 1,
                                "scheduledWateringTime": 1243,
                                "computedWateringTime": 1243,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                            {
                                "id": 2,
                                "scheduledWateringTime": 2680,
                                "computedWateringTime": 2680,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                                "wateringFlag": 0,
                            },
                        ],
                    },
                ],
                "simulatedPrograms": [
                    {
                        "id": 1,
                        "zones": [
                            {
                                "id": 2,
                                "scheduledWateringTime": 300,
                                "computedWateringTime": 300,
                                "availableWater": 0,
                                "coefficient": 1.0,
                                "percentage": 100,
                            }
                        ],
                    }
                ],
            },
            {
                "dayTimestamp": 1528610400,
                "day": "2018-06-10",
                "mint": None,
                "maxt": None,
                "icon": None,
                "programs": [],
                "simulatedPrograms": [],
            },
        ]
    }
