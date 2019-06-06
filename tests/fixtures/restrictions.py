"""Define fixtures related to the "restrictions" endpoint."""
import pytest


@pytest.fixture()
def restrictions_currently_json():
    """Return a /restrictions/currently response."""
    return {
        "hourly": False,
        "freeze": False,
        "month": False,
        "weekDay": False,
        "rainDelay": False,
        "rainDelayCounter": -1,
        "rainSensor": False,
    }


@pytest.fixture()
def restrictions_global_json():
    """Return a /restrictions/global response."""
    return {
        "hotDaysExtraWatering": False,
        "freezeProtectEnabled": True,
        "freezeProtectTemp": 2,
        "noWaterInWeekDays": "0000000",
        "noWaterInMonths": "000000000000",
        "rainDelayStartTime": 1524854551,
        "rainDelayDuration": 0,
    }


@pytest.fixture()
def restrictions_hourly_json():
    """Return a /restrictions/hourly response."""
    return {"hourlyRestrictions": []}


@pytest.fixture()
def restrictions_raindelay_json():
    """Return a /restrictions/raindelay response."""
    return {"delayCounter": -1}
