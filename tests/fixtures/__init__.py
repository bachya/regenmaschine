"""Define global fixtures."""
import json

import aresponses
import pytest

from ..const import (
    TEST_ACCESS_TOKEN,
    TEST_HOST,
    TEST_MAC,
    TEST_NAME,
    TEST_PORT,
    TEST_SPRINKLER_ID,
    TEST_TOTP_CODE,
)
from .api import apiver_json
from .provision import provision_name_json, provision_wifi_json


@pytest.fixture()
def authenticated_local_client(
    apiver_json, auth_login_json, event_loop, provision_name_json, provision_wifi_json
):
    """Return an aresponses server for an authenticated local client."""
    client = aresponses.ResponsesMockServer(loop=event_loop)
    client.add(
        "{0}:{1}".format(TEST_HOST, TEST_PORT),
        "/api/4/auth/login",
        "post",
        aresponses.Response(text=json.dumps(auth_login_json), status=200),
    )
    client.add(
        "{0}:{1}".format(TEST_HOST, TEST_PORT),
        "/api/4/provision/name",
        "get",
        aresponses.Response(text=json.dumps(provision_name_json), status=200),
    )
    client.add(
        "{0}:{1}".format(TEST_HOST, TEST_PORT),
        "/api/4/provision/wifi",
        "get",
        aresponses.Response(text=json.dumps(provision_wifi_json), status=200),
    )
    client.add(
        "{0}:{1}".format(TEST_HOST, TEST_PORT),
        "/api/4/apiVer",
        "get",
        aresponses.Response(text=json.dumps(apiver_json), status=200),
    )

    return client


@pytest.fixture()
def authenticated_remote_client(
    apiver_json,
    event_loop,
    remote_auth_login_1_json,
    remote_auth_login_2_json,
    remote_sprinklers_json,
):
    """Return an aresponses server for an authenticated remote client."""
    client = aresponses.ResponsesMockServer(loop=event_loop)
    client.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(text=json.dumps(remote_auth_login_1_json), status=200),
    )
    client.add(
        "my.rainmachine.com",
        "/devices/get-sprinklers",
        "post",
        aresponses.Response(text=json.dumps(remote_sprinklers_json), status=200),
    )
    client.add(
        "my.rainmachine.com",
        "/devices/login-sprinkler",
        "post",
        aresponses.Response(text=json.dumps(remote_auth_login_2_json), status=200),
    )
    client.add(
        "api.rainmachine.com",
        "/{0}/api/4/apiVer".format(TEST_SPRINKLER_ID),
        "get",
        aresponses.Response(text=json.dumps(apiver_json), status=200),
    )

    return client


@pytest.fixture()
def auth_login_json():
    """Return a /auth/login response."""
    return {
        "access_token": TEST_ACCESS_TOKEN,
        "checksum": "98765",
        "expires_in": 157680000,
        "expiration": "Tue, 06 Jun 2023 02:17:46 GMT",
        "statusCode": 0,
    }


@pytest.fixture()
def auth_totp_json():
    """Return a /auth/totp response."""
    return {"totp": TEST_TOTP_CODE}


@pytest.fixture()
def remote_auth_login_1_json():
    """Return a /login/auth (remote) response."""
    return {"access_token": TEST_ACCESS_TOKEN, "errorType": -1}


@pytest.fixture()
def remote_auth_login_2_json():
    """Return a /devices/login-sprinkler (remote) response."""
    return {
        "access_token": TEST_ACCESS_TOKEN,
        "errorType": 0,
        "sprinklerId": TEST_SPRINKLER_ID,
    }


@pytest.fixture()
def remote_error_known():
    """Return a remote "error" code."""
    return {"errorType": 1}


@pytest.fixture()
def remote_error_http_body():
    """Return a remote "error" code."""
    return {"statusCode": 400, "error": 400, "message": "Bad Request"}


@pytest.fixture()
def remote_error_unknown():
    """Return a remote "error" code."""
    return {"errorType": 999}


@pytest.fixture()
def remote_sprinklers_json():
    """Return a /devices/get-sprinklers (remote) response."""
    return {
        "errorType": 0,
        "sprinklers": [
            {
                "sprinklerId": TEST_SPRINKLER_ID,
                "sprinklerUrl": "https://api.rainmachine.com/{0}/".format(
                    TEST_SPRINKLER_ID
                ),
                "mac": TEST_MAC,
                "name": TEST_NAME,
                "type": "SPK3",
                "swVer": "4.0.974",
            }
        ],
    }


@pytest.fixture()
def unauthenticated_json():
    """Return a failed authentication response."""
    return {"statusCode": 2, "message": "Not Authenticated !"}
