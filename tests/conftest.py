"""Define fixtures available for all tests."""
import aresponses
import pytest

from .common import TEST_HOST, TEST_PORT, TEST_SPRINKLER_ID, load_fixture


@pytest.fixture(name="authenticated_local_client")
def authenticated_local_client_fixture(provision_name_response):
    """Return an aresponses server for an authenticated local client."""
    client = aresponses.ResponsesMockServer()
    client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/auth/login",
        "post",
        aresponses.Response(text=load_fixture("auth_login_response.json"), status=200),
    )
    client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/provision/name",
        "get",
        aresponses.Response(text=provision_name_response, status=200),
    )
    client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/provision/wifi",
        "get",
        aresponses.Response(
            text=load_fixture("provision_wifi_response.json"), status=200
        ),
    )
    client.add(
        f"{TEST_HOST}:{TEST_PORT}",
        "/api/4/apiVer",
        "get",
        aresponses.Response(text=load_fixture("api_version_response.json"), status=200),
    )

    return client


@pytest.fixture(name="authenticated_remote_client")
def authenticated_remote_client_fixture():
    """Return an aresponses server for an authenticated remote client."""
    client = aresponses.ResponsesMockServer()
    client.add(
        "my.rainmachine.com",
        "/login/auth",
        "post",
        aresponses.Response(
            text=load_fixture("remote_auth_login_1_response.json"), status=200
        ),
    )
    client.add(
        "my.rainmachine.com",
        "/devices/get-sprinklers",
        "post",
        aresponses.Response(
            text=load_fixture("remote_sprinklers_response.json"), status=200
        ),
    )
    client.add(
        "my.rainmachine.com",
        "/devices/login-sprinkler",
        "post",
        aresponses.Response(
            text=load_fixture("remote_auth_login_2_response.json"), status=200
        ),
    )
    client.add(
        "api.rainmachine.com",
        f"/{TEST_SPRINKLER_ID}/api/4/apiVer",
        "get",
        aresponses.Response(text=load_fixture("api_version_response.json"), status=200),
    )

    return client


@pytest.fixture(name="provision_name_response")
def provision_name_response_fixture():
    """Return an API response that contains the controller name."""
    return load_fixture("provision_name_response.json")
