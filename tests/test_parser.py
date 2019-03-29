"""Define tests for parser endpoints."""
# pylint: disable=redefined-outer-name
import json

import aiohttp
import pytest

from regenmaschine import login

from tests.const import TEST_ACCESS_TOKEN, TEST_HOST, TEST_PASSWORD, TEST_PORT
from tests.fixtures import authenticated_client, auth_login_json
from tests.fixtures.api import apiver_json
from tests.fixtures.parser import *
from tests.fixtures.provision import provision_name_json, provision_wifi_json


@pytest.mark.asyncio
async def test_parsers_current(
        aresponses, authenticated_client, event_loop, parser_json):
    """Test getting all current parsers."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/parser', 'get',
            aresponses.Response(text=json.dumps(parser_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.parsers.current()
            assert len(data) == 1
            assert data[0]['name'] == 'NOAA Parser'
