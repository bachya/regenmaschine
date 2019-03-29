"""Define tests for restriction endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import datetime
import json

import aiohttp
import pytest

from regenmaschine import login

from tests.const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from tests.fixtures import authenticated_local_client, auth_login_json
from tests.fixtures.api import apiver_json
from tests.fixtures.provision import provision_name_json, provision_wifi_json
from tests.fixtures.watering import *


@pytest.mark.asyncio
async def test_watering_log_details(
        aresponses, authenticated_local_client, event_loop, watering_log_json):
    """Test getting watering log details."""
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/watering/log/details/{0}/{1}'.format(today_str, 2), 'get',
            aresponses.Response(
                text=json.dumps(watering_log_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.watering.log(today, 2, details=True)
            assert len(data) == 2


@pytest.mark.asyncio
async def test_watering_pause(
        aresponses, authenticated_local_client, event_loop, watering_pause_json):
    """Test pausing and unpausing watering."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/pauseall',
            'post',
            aresponses.Response(
                text=json.dumps(watering_pause_json), status=200))
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/pauseall',
            'post',
            aresponses.Response(
                text=json.dumps(watering_pause_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.watering.pause_all(30)
            assert data['message'] == 'OK'

            data = await client.watering.unpause_all()
            assert data['message'] == 'OK'


@pytest.mark.asyncio
async def test_watering_queue(
        aresponses, authenticated_local_client, event_loop, watering_queue_json):
    """Test getting the watering queue."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/queue',
            'get',
            aresponses.Response(
                text=json.dumps(watering_queue_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.watering.queue()
            assert not data


@pytest.mark.asyncio
async def test_watering_past(
        aresponses, authenticated_local_client, event_loop, watering_past_json):
    """Test gettinng info on past watering runs."""
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT),
            '/api/4/watering/past/{0}/{1}'.format(today_str, 2), 'get',
            aresponses.Response(
                text=json.dumps(watering_past_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.watering.runs(today, 2)
            assert len(data) == 8


@pytest.mark.asyncio
async def test_watering_stop(
        aresponses, authenticated_local_client, event_loop, watering_stopall_json):
    """Test stopping all watering activities."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/watering/stopall',
            'post',
            aresponses.Response(
                text=json.dumps(watering_stopall_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.watering.stop_all()
            assert data['message'] == 'OK'
