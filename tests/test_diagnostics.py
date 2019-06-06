"""Define tests for diagnostics endpoints."""
# pylint: disable=redefined-outer-name

import json

import aiohttp
import aresponses
import pytest

from regenmaschine import login

from tests.const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from tests.fixtures import authenticated_local_client, auth_login_json
from tests.fixtures.api import apiver_json
from tests.fixtures.diagnostics import *
from tests.fixtures.provision import provision_name_json, provision_wifi_json


@pytest.mark.asyncio
async def test_diagnostics_current(
    aresponses, authenticated_local_client, diag_json, event_loop
):
    """Test retrieving current diagnostics."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            "{0}:{1}".format(TEST_HOST, TEST_PORT),
            "/api/4/diag",
            "get",
            aresponses.Response(text=json.dumps(diag_json), status=200),
        )

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.diagnostics.current()
            assert data["memUsage"] == 18220


@pytest.mark.asyncio
async def test_diagnostics_log(
    aresponses, authenticated_local_client, diag_log_json, event_loop
):
    """Test retrieving the entire diagnostics log."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            "{0}:{1}".format(TEST_HOST, TEST_PORT),
            "/api/4/diag/log",
            "get",
            aresponses.Response(text=json.dumps(diag_log_json), status=200),
        )

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.diagnostics.log()
            assert data == "----"
