"""Define fixtures related to the "zone" endpoint."""
import pytest


@pytest.fixture()
def zone_id_properties_json():
    """Return a /zone/<ID>/properties response."""
    return {
        "uid": 1,
        "name": "Landscaping",
        "valveid": 1,
        "ETcoef": 0.80000000000000004,
        "active": True,
        "type": 4,
        "internet": True,
        "savings": 100,
        "slope": 1,
        "sun": 1,
        "soil": 5,
        "group_id": 4,
        "history": True,
        "master": False,
        "before": 0,
        "after": 0,
        "waterSense": {
            "fieldCapacity": 0.17000000000000001,
            "rootDepth": 229,
            "minRuntime": -1,
            "appEfficiency": 0.75,
            "isTallPlant": True,
            "permWilting": 0.029999999999999999,
            "allowedSurfaceAcc": 8.3800000000000008,
            "maxAllowedDepletion": 0.5,
            "precipitationRate": 25.399999999999999,
            "currentFieldCapacity": 16.030000000000001,
            "area": 92.900001525878906,
            "referenceTime": 1243,
            "detailedMonthsKc": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            "flowrate": None,
            "soilIntakeRate": 10.16,
        },
        "customSoilPreset": None,
        "customVegetationPreset": None,
        "customSprinklerPreset": None,
    }


@pytest.fixture()
def zone_post_json():
    """Return a /zone (POST) response."""
    return {"statusCode": 0, "message": "OK"}


@pytest.fixture()
def zone_properties_json():
    """Return a /zone/properties response."""
    return {
        "zones": [
            {
                "uid": 1,
                "name": "Landscaping",
                "valveid": 1,
                "ETcoef": 0.80000000000000004,
                "active": True,
                "type": 4,
                "internet": True,
                "savings": 100,
                "slope": 1,
                "sun": 1,
                "soil": 5,
                "group_id": 4,
                "history": True,
                "master": False,
                "before": 0,
                "after": 0,
                "waterSense": {
                    "fieldCapacity": 0.17000000000000001,
                    "rootDepth": 229,
                    "minRuntime": -1,
                    "appEfficiency": 0.75,
                    "isTallPlant": True,
                    "permWilting": 0.029999999999999999,
                    "allowedSurfaceAcc": 8.3800000000000008,
                    "maxAllowedDepletion": 0.5,
                    "precipitationRate": 25.399999999999999,
                    "currentFieldCapacity": 16.030000000000001,
                    "area": 92.900001525878906,
                    "referenceTime": 1243,
                    "detailedMonthsKc": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                    "flowrate": None,
                    "soilIntakeRate": 10.16,
                },
                "customSoilPreset": None,
                "customVegetationPreset": None,
                "customSprinklerPreset": None,
            },
            {
                "uid": 2,
                "name": "Flower Bed",
                "valveid": 1,
                "ETcoef": 0.80000000000000004,
                "active": False,
                "type": 4,
                "internet": True,
                "savings": 100,
                "slope": 1,
                "sun": 1,
                "soil": 5,
                "group_id": 4,
                "history": True,
                "master": False,
                "before": 0,
                "after": 0,
                "waterSense": {
                    "fieldCapacity": 0.17000000000000001,
                    "rootDepth": 229,
                    "minRuntime": -1,
                    "appEfficiency": 0.75,
                    "isTallPlant": True,
                    "permWilting": 0.029999999999999999,
                    "allowedSurfaceAcc": 8.3800000000000008,
                    "maxAllowedDepletion": 0.5,
                    "precipitationRate": 25.399999999999999,
                    "currentFieldCapacity": 16.030000000000001,
                    "area": 92.900001525878906,
                    "referenceTime": 1243,
                    "detailedMonthsKc": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                    "flowrate": None,
                    "soilIntakeRate": 10.16,
                },
                "customSoilPreset": None,
                "customVegetationPreset": None,
                "customSprinklerPreset": None,
            },
        ]
    }


@pytest.fixture()
def zone_start_stop_json():
    """Return a response for /zone/<ID>/start and /zone/<ID>/stop."""
    return {"statusCode": 0, "message": "OK"}
