"""Define fixtures related to the "parser" endpoint."""
import pytest


@pytest.fixture(scope="module")
def parser_json():
    """Return a /parser response."""
    return {
        "parsers": [
            {
                "lastRun": "2018-04-30 11:52:33",
                "lastKnownError": "",
                "hasForecast": True,
                "uid": 11,
                "hasHistorical": False,
                "description": "North America weather forecast",
                "enabled": True,
                "custom": False,
                "isRunning": False,
                "name": "NOAA Parser",
            }
        ]
    }
