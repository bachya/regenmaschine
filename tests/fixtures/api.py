"""Define fixtures related to the "api" endpoint."""
import pytest


@pytest.fixture()
def apiver_json():
    """Return a /apiVer response."""
    return {"apiVer": "4.5.0", "hwVer": 3, "swVer": "4.0.925"}
