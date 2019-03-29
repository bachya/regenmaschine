"""Define tests for program endpoints."""
# pylint: disable=redefined-outer-name,too-many-arguments

import json

import aiohttp
import pytest

from regenmaschine import login

from tests.const import TEST_HOST, TEST_PASSWORD, TEST_PORT
from tests.fixtures import authenticated_local_client, auth_login_json
from tests.fixtures.api import apiver_json
from tests.fixtures.provision import provision_name_json, provision_wifi_json
from tests.fixtures.zone import *


@pytest.mark.asyncio
async def test_zone_enable_disable(
        aresponses, authenticated_local_client, event_loop, zone_post_json):
    """Test enabling a zone."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/1/properties',
            'post',
            aresponses.Response(text=json.dumps(zone_post_json), status=200))
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/1/properties',
            'post',
            aresponses.Response(text=json.dumps(zone_post_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            resp = await client.zones.enable(1)
            assert resp['message'] == 'OK'

            resp = await client.zones.disable(1)
            assert resp['message'] == 'OK'


@pytest.mark.asyncio
async def test_zone_get(
        aresponses, authenticated_local_client, event_loop, zone_properties_json):
    """Test getting info on all zones."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/properties',
            'get',
            aresponses.Response(
                text=json.dumps(zone_properties_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.zones.all(details=True, include_inactive=True)
            assert len(data) == 2
            assert data[0]['name'] == 'Landscaping'


@pytest.mark.asyncio
async def test_zone_get_active(
        aresponses, authenticated_local_client, event_loop, zone_properties_json):
    """Test getting info on active zones."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/properties',
            'get',
            aresponses.Response(
                text=json.dumps(zone_properties_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.zones.all(details=True)
            assert len(data) == 1
            assert data[0]['name'] == 'Landscaping'


@pytest.mark.asyncio
async def test_zone_get_by_id(
        aresponses, authenticated_local_client, event_loop, zone_id_properties_json):
    """Test getting properties on a specific zone by ID."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/1/properties',
            'get',
            aresponses.Response(
                text=json.dumps(zone_id_properties_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.zones.get(1, details=True)
            assert data['name'] == 'Landscaping'


@pytest.mark.asyncio
async def test_zone_start_stop(
        aresponses, authenticated_local_client, event_loop, zone_start_stop_json):
    """Test starting and stopping a zone."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/1/start',
            'post',
            aresponses.Response(
                text=json.dumps(zone_start_stop_json), status=200))
        authenticated_local_client.add(
            '{0}:{1}'.format(TEST_HOST, TEST_PORT), '/api/4/zone/1/stop',
            'post',
            aresponses.Response(
                text=json.dumps(zone_start_stop_json), status=200))

        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await login(
                TEST_HOST,
                TEST_PASSWORD,
                websession,
                port=TEST_PORT,
                ssl=False)

            data = await client.zones.start(1, 60)
            assert data['message'] == 'OK'

            data = await client.zones.stop(1)
            assert data['message'] == 'OK'
