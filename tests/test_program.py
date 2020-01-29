"""Define tests for program endpoints."""
import aiohttp
import pytest

from regenmaschine import login

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_program_enable_disable(aresponses, authenticated_local_client):
    """Test enabling a program."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1",
            "post",
            aresponses.Response(
                text=load_fixture("program_post_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1",
            "post",
            aresponses.Response(
                text=load_fixture("program_post_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            resp = await client.programs.enable(1)
            assert resp["message"] == "OK"

            resp = await client.programs.disable(1)
            assert resp["message"] == "OK"


@pytest.mark.asyncio
async def test_program_get(aresponses, authenticated_local_client):
    """Test getting all programs."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program",
            "get",
            aresponses.Response(text=load_fixture("program_response.json"), status=200),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.programs.all(include_inactive=True)
            assert len(data) == 2
            assert data[0]["name"] == "Morning"


@pytest.mark.asyncio
async def test_program_get_active(aresponses, authenticated_local_client):
    """Test getting only active programs."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program",
            "get",
            aresponses.Response(text=load_fixture("program_response.json"), status=200),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.programs.all()
            assert len(data) == 1
            assert data[0]["name"] == "Morning"


@pytest.mark.asyncio
async def test_program_get_by_id(aresponses, authenticated_local_client):
    """Test getting a program by its ID."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1",
            "get",
            aresponses.Response(
                text=load_fixture("program_id_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.programs.get(1)
            assert data["name"] == "Morning"


@pytest.mark.asyncio
async def test_program_next_run(aresponses, authenticated_local_client):
    """Test getting the next run of a program."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/nextrun",
            "get",
            aresponses.Response(
                text=load_fixture("program_nextrun_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.programs.next()
            assert len(data) == 2


@pytest.mark.asyncio
async def test_program_running(aresponses, authenticated_local_client):
    """Test getting all running programs."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/program",
            "get",
            aresponses.Response(
                text=load_fixture("watering_program_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.programs.running()
            assert len(data) == 1
            assert data[0]["name"] == "Evening"


@pytest.mark.asyncio
async def test_program_start_and_stop(aresponses, authenticated_local_client):
    """Test starting and stopping a program."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1/start",
            "post",
            aresponses.Response(
                text=load_fixture("program_start_stop_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1/stop",
            "post",
            aresponses.Response(
                text=load_fixture("program_start_stop_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as websession:
            client = await login(
                TEST_HOST, TEST_PASSWORD, websession, port=TEST_PORT, ssl=False
            )

            data = await client.programs.start(1)
            assert data["message"] == "OK"

            data = await client.programs.stop(1)
            assert data["message"] == "OK"
