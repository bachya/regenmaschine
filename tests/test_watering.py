"""Define tests for restriction endpoints."""
import datetime

import aiohttp
import pytest

from regenmaschine import login

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_watering_log_details(aresponses, authenticated_local_client):
    """Test getting watering log details."""
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            f"/api/4/watering/log/details/{today_str}/2",
            "get",
            aresponses.Response(
                text=load_fixture("watering_log_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.watering.log(today, 2, details=True)
            assert len(data) == 2


@pytest.mark.asyncio
async def test_watering_pause(aresponses, authenticated_local_client):
    """Test pausing and unpausing watering."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/pauseall",
            "post",
            aresponses.Response(
                text=load_fixture("watering_pause_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/pauseall",
            "post",
            aresponses.Response(
                text=load_fixture("watering_pause_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.watering.pause_all(30)
            assert data["message"] == "OK"

            data = await client.watering.unpause_all()
            assert data["message"] == "OK"


@pytest.mark.asyncio
async def test_watering_queue(aresponses, authenticated_local_client):
    """Test getting the watering queue."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/queue",
            "get",
            aresponses.Response(
                text=load_fixture("watering_queue_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.watering.queue()
            assert not data


@pytest.mark.asyncio
async def test_watering_past(aresponses, authenticated_local_client):
    """Test gettinng info on past watering runs."""
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            f"/api/4/watering/past/{today_str}/2",
            "get",
            aresponses.Response(
                text=load_fixture("watering_past_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.watering.runs(today, 2)
            assert len(data) == 8


@pytest.mark.asyncio
async def test_watering_stop(aresponses, authenticated_local_client):
    """Test stopping all watering activities."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/stopall",
            "post",
            aresponses.Response(
                text=load_fixture("watering_stopall_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.watering.stop_all()
            assert data["message"] == "OK"
