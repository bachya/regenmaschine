"""Define fixtures related to the "diagnostics" endpoint."""
import pytest


@pytest.fixture()
def diag_json():
    """Return a /diag response."""
    return {
        "hasWifi": True,
        "uptime": "14 days, 8:45:19",
        "uptimeSeconds": 1241119,
        "memUsage": 18220,
        "networkStatus": True,
        "bootCompleted": True,
        "lastCheckTimestamp": 1527997722,
        "wizardHasRun": True,
        "standaloneMode": False,
        "cpuUsage": 0.0,
        "lastCheck": "2018-06-02 21:48:42",
        "softwareVersion": "4.0.925",
        "internetStatus": True,
        "locationStatus": True,
        "timeStatus": True,
        "wifiMode": None,
        "gatewayAddress": "192.168.1.1",
        "cloudStatus": 0,
        "weatherStatus": True,
    }


@pytest.fixture()
def diag_log_json():
    """Return a /diag/log response."""
    return {"log": "----"}
