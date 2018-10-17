"""Define tests for program endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments
import json

import aiohttp
import pytest

from regenmaschine import Client

from .const import TEST_HOST, TEST_PORT, TEST_PASSWORD
from .fixtures import authenticated_client, auth_login_json
from .fixtures.program import *
from .fixtures.provision import provision_name_json, provision_wifi_json


@pytest.mark.asyncio
async def test_endpoints(
        aresponses, authenticated_client, event_loop, program_json,
        program_id_json, program_nextrun_json, program_start_stop_json,
        watering_program_json):
    """Test all endpoints."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program', 'get',
            aresponses.Response(text=json.dumps(program_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program/1', 'get',
            aresponses.Response(text=json.dumps(program_id_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program/nextrun',
            'get',
            aresponses.Response(
                text=json.dumps(program_nextrun_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/program',
            'get',
            aresponses.Response(
                text=json.dumps(watering_program_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program/1/start',
            'post',
            aresponses.Response(
                text=json.dumps(program_start_stop_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program/1/stop',
            'post',
            aresponses.Response(
                text=json.dumps(program_start_stop_json), status=200))

        # pylint: disable=protected-access
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await Client.authenticate_via_password(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.programs.all()
            assert len(data) == 1
            assert data[0]['name'] == 'Morning'

            data = await client.programs.get(1)
            assert data['name'] == 'Morning'

            data = await client.programs.next()
            assert len(data) == 2

            data = await client.programs.running()
            assert len(data) == 1
            assert data[0]['name'] == 'Evening'

            data = await client.programs.start(1)
            assert data['message'] == 'OK'

            data = await client.programs.stop(1)
            assert data['message'] == 'OK'
