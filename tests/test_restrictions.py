"""Define tests for restriction endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments
import json

import aiohttp
import pytest

from regenmaschine import login

from tests.const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from tests.fixtures import authenticated_local_client, auth_login_json
from tests.fixtures.api import apiver_json
from tests.fixtures.provision import provision_name_json, provision_wifi_json
from tests.fixtures.restrictions import *


@pytest.mark.asyncio
async def test_restrictions_current(
    aresponses, authenticated_local_client, event_loop, restrictions_currently_json
):
    """Test getting any current restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/currently",
            "get",
            aresponses.Response(
                text=json.dumps(restrictions_currently_json), status=200
            ),
        )

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.restrictions.current()
            assert data["hourly"] is False


@pytest.mark.asyncio
async def test_restrictions_global(
    aresponses, authenticated_local_client, event_loop, restrictions_global_json
):
    """Test getting any global restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/global",
            "get",
            aresponses.Response(text=json.dumps(restrictions_global_json), status=200),
        )

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.restrictions.universal()
            assert data["freezeProtectTemp"] == 2


@pytest.mark.asyncio
async def test_restrictions_hourly(
    aresponses, authenticated_local_client, event_loop, restrictions_hourly_json
):
    """Test getting any hourly restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/hourly",
            "get",
            aresponses.Response(text=json.dumps(restrictions_hourly_json), status=200),
        )

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.restrictions.hourly()
            assert not data


@pytest.mark.asyncio
async def test_restrictions_raindelay(
    aresponses, authenticated_local_client, event_loop, restrictions_raindelay_json
):
    """Test getting any rain delay-related restrictions."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/restrictions/raindelay",
            "get",
            aresponses.Response(
                text=json.dumps(restrictions_raindelay_json), status=200
            ),
        )

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.restrictions.raindelay()
            assert data["delayCounter"] == -1
