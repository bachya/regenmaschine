"""Define tests for program endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments
import json

import aiohttp
import pytest

from regenmaschine import login

from .const import TEST_HOST, TEST_PORT, TEST_PASSWORD
from .fixtures import authenticated_client, auth_login_json
from .fixtures.api import apiver_json
from .fixtures.program import *
from .fixtures.provision import provision_name_json, provision_wifi_json


@pytest.mark.asyncio
async def test_program_enable_disable(
        aresponses, authenticated_client, event_loop, program_post_json):
    """Test enabling a program."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program/1', 'post',
            aresponses.Response(
                text=json.dumps(program_post_json), status=200))
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program/1', 'post',
            aresponses.Response(
                text=json.dumps(program_post_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            resp = await client.programs.enable(1)
            assert resp['message'] == 'OK'

            resp = await client.programs.disable(1)
            assert resp['message'] == 'OK'


@pytest.mark.asyncio
async def test_program_get(
        aresponses, authenticated_client, event_loop, program_json):
    """Test getting all programs."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program', 'get',
            aresponses.Response(text=json.dumps(program_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.programs.all(include_inactive=True)
            assert len(data) == 2
            assert data[0]['name'] == 'Morning'


@pytest.mark.asyncio
async def test_program_get_active(
        aresponses, authenticated_client, event_loop, program_json):
    """Test getting only active programs."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program', 'get',
            aresponses.Response(text=json.dumps(program_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.programs.all()
            assert len(data) == 1
            assert data[0]['name'] == 'Morning'


@pytest.mark.asyncio
async def test_program_get_by_id(
        aresponses, authenticated_client, event_loop, program_id_json):
    """Test getting a program by its ID."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program/1', 'get',
            aresponses.Response(text=json.dumps(program_id_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.programs.get(1)
            assert data['name'] == 'Morning'


@pytest.mark.asyncio
async def test_program_next_run(
        aresponses, authenticated_client, event_loop, program_nextrun_json,
        program_start_stop_json, watering_program_json):
    """Test getting the next run of a program."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/program/nextrun',
            'get',
            aresponses.Response(
                text=json.dumps(program_nextrun_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.programs.next()
            assert len(data) == 2


@pytest.mark.asyncio
async def test_program_running(
        aresponses, authenticated_client, event_loop, watering_program_json):
    """Test getting all running programs."""
    async with authenticated_client:
        authenticated_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/program',
            'get',
            aresponses.Response(
                text=json.dumps(watering_program_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.programs.running()
            assert len(data) == 1
            assert data[0]['name'] == 'Evening'


@pytest.mark.asyncio
async def test_program_start_and_stop(
        aresponses, authenticated_client, event_loop, program_start_stop_json):
    """Test starting and stopping a program."""
    async with authenticated_client:
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

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.programs.start(1)
            assert data['message'] == 'OK'

            data = await client.programs.stop(1)
            assert data['message'] == 'OK'
