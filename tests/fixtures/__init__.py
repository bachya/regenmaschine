"""Define global fixtures."""
import json

import aresponses
import pytest

from ..const import TEST_ACCESS_TOKEN, TEST_HOST, TEST_PORT, TEST_TOTP_CODE
from .provision import provision_name_json, provision_wifi_json


@pytest.fixture()
def authenticated_client(
        auth_login_json, event_loop, provision_name_json,
        provision_wifi_json):
    """Return an aresponses server relating to an authenticated client."""
    client = aresponses.ResponsesMockServer(loop=event_loop)
    client.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/auth/login', 'post',
        aresponses.Response(text=json.dumps(auth_login_json), status=200))
    client.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision/name', 'get',
        aresponses.Response(
            text=json.dumps(provision_name_json), status=200))
    client.add(
        '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/provision/wifi', 'get',
        aresponses.Response(
            text=json.dumps(provision_wifi_json), status=200))

    return client


@pytest.fixture()
def auth_login_json():
    """Return a /auth/login response."""
    return {
        "access_token": TEST_ACCESS_TOKEN,
        "checksum": "98765",
        "expires_in": 157680000,
        "expiration": "Tue, 06 Jun 2023 02:17:46 GMT",
        "statusCode": 0
    }


@pytest.fixture()
def auth_totp_json():
    """Return a /auth/totp response."""
    return {"totp": TEST_TOTP_CODE}


@pytest.fixture()
def unauthenticated_json():
    """Return a failed authentication response."""
    return {"statusCode": 2, "message": "Not Authenticated !"}
