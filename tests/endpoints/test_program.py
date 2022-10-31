"""Define tests for program endpoints."""
import json
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from tests.common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.fixture(name="program_post_response")
def program_post_response_fixture() -> dict[str, Any]:
    """Return an API response that contains program post data.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("program_post_response.json")))


@pytest.fixture(name="program_response")
def program_response_fixture() -> dict[str, Any]:
    """Return an API response that contains program data.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("program_response.json")))


@pytest.fixture(name="program_start_stop_response")
def program_start_stop_response_fixture() -> dict[str, Any]:
    """Return an API response that contains program start/stop data.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("program_start_stop_response.json"))
    )


@pytest.mark.asyncio
async def test_program_enable_disable(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    program_post_response: dict[str, Any],
) -> None:
    """Test enabling a program.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        program_post_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1",
            "post",
            response=aiohttp.web_response.json_response(
                program_post_response, status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1",
            "post",
            response=aiohttp.web_response.json_response(
                program_post_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            resp = await controller.programs.enable(1)
            assert resp["message"] == "OK"

            resp = await controller.programs.disable(1)
            assert resp["message"] == "OK"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_program_get(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    program_response: dict[str, Any],
) -> None:
    """Test getting all programs.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        program_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program",
            "get",
            response=aiohttp.web_response.json_response(program_response, status=200),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            programs = await controller.programs.all(include_inactive=True)
            assert len(programs) == 2
            assert programs[1]["name"] == "Morning"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_program_get_active(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    program_response: dict[str, Any],
) -> None:
    """Test getting only active programs.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        program_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program",
            "get",
            response=aiohttp.web_response.json_response(program_response, status=200),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            programs = await controller.programs.all()
            assert len(programs) == 1
            assert programs[1]["name"] == "Morning"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_program_get_by_id(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting a program by its ID.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("program_id_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.programs.get(1)
            assert data["name"] == "Morning"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_program_next_run(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting the next run of a program.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/nextrun",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("program_nextrun_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.programs.next()
            assert len(data) == 2

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_program_running(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test getting all running programs.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/watering/program",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("watering_program_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.programs.running()
            assert len(data) == 1
            assert data[0]["name"] == "Evening"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_program_start_and_stop(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    program_start_stop_response: dict[str, Any],
) -> None:
    """Test starting and stopping a program.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        program_start_stop_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1/start",
            "post",
            response=aiohttp.web_response.json_response(
                program_start_stop_response, status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/program/1/stop",
            "post",
            response=aiohttp.web_response.json_response(
                program_start_stop_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.programs.start(1)
            assert data["message"] == "OK"

            data = await controller.programs.stop(1)
            assert data["message"] == "OK"

    aresponses.assert_plan_strictly_followed()
