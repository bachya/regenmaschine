"""Define fixtures available for all tests."""
import json
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from .common import TEST_HOST, TEST_PORT, TEST_SPRINKLER_ID, load_fixture


@pytest.fixture(name="api_version_response")
def api_version_response_fixture() -> dict[str, Any]:
    """Return an API response that contains versions.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("api_version_response.json")))


@pytest.fixture(name="auth_login_response")
def auth_login_response_fixture() -> dict[str, Any]:
    """Return an API response that contains authentication info.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("auth_login_response.json")))


@pytest.fixture(name="authenticated_local_client")
def authenticated_local_client_fixture(
    api_version_response: dict[str, Any],
    auth_login_response: dict[str, Any],
    provision_name_response: dict[str, Any],
    provision_wifi_response: dict[str, Any],
) -> ResponsesMockServer:
    """Return an aresponses server for an authenticated local client.

    Args:
        api_version_response: An API response payload.
        auth_login_response: An API response payload.
        provision_name_response: An API response payload.
        provision_wifi_response: An API response payload.

    Returns:
        A mocked local API connect.
    """
    client = ResponsesMockServer()
    client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/auth/login",
        "post",
        response=aiohttp.web_response.json_response(auth_login_response, status=200),
    )
    client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/provision/name",
        "get",
        response=aiohttp.web_response.json_response(
            provision_name_response, status=200
        ),
    )
    client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/provision/wifi",
        "get",
        response=aiohttp.web_response.json_response(
            provision_wifi_response, status=200
        ),
    )
    client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/apiVer",
        "get",
        response=aiohttp.web_response.json_response(api_version_response, status=200),
    )
    return client


@pytest.fixture(name="authenticated_remote_client")
def authenticated_remote_client_fixture(
    api_version_response: dict[str, Any],
    remote_auth_login_1_response: dict[str, Any],
    remote_sprinklers_response: dict[str, Any],
) -> ResponsesMockServer:
    """Return an aresponses server for an authenticated remote client.

    Args:
        api_version_response: An API response payload.
        remote_auth_login_1_response: An API response payload.
        remote_sprinklers_response: An API response payload.

    Returns:
        A mocked remote API connect.
    """
    client = ResponsesMockServer()
    client.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        response=aiohttp.web_response.json_response(
            remote_auth_login_1_response, status=200
        ),
    )
    client.add(
        "my.rainmachine.com",
        "/devices/get-sprinklers",
        "post",
        response=aiohttp.web_response.json_response(
            remote_sprinklers_response, status=200
        ),
    )
    client.add(
        "my.rainmachine.com",
        "/devices/login-sprinkler",
        "post",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture("remote_auth_login_2_response.json")), status=200
        ),
    )
    client.add(
        "api.rainmachine.com",
        f"/{TEST_SPRINKLER_ID}/api/4/apiVer",
        "get",
        response=aiohttp.web_response.json_response(api_version_response, status=200),
    )
    return client


@pytest.fixture(name="provision_name_response")
def provision_name_response_fixture() -> dict[str, Any]:
    """Return an API response that contains the controller name.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("provision_name_response.json"))
    )


@pytest.fixture(name="provision_wifi_response")
def provision_wifi_response_fixture() -> dict[str, Any]:
    """Return an API response that contains WiFi info.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("provision_wifi_response.json"))
    )


@pytest.fixture(name="remote_auth_login_1_response")
def remote_auth_login_1_response_fixture() -> dict[str, Any]:
    """Return an API response that contains first-stage remote login info.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("remote_auth_login_1_response.json"))
    )


@pytest.fixture(name="remote_sprinklers_response")
def remote_sprinklers_response_fixture() -> dict[str, Any]:
    """Return an API response that contains first-stage remote sprinkler info.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("remote_sprinklers_response.json"))
    )
