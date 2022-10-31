"""Define tests for parser endpoints."""
import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from tests.common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_parsers_current(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
) -> None:
    """Test getting all current parsers.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/parser",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("parser_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.parsers.current()
            assert len(data) == 1
            assert data[0]["name"] == "NOAA Parser"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_parsers_post_data(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
) -> None:
    """Test pushing data to parser.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/parser/data",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("parser_post_data_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))
            payload = json.loads(load_fixture("parser_post_data_payload.json"))
            data = await controller.parsers.post_data(payload)
            assert len(data) == 2
            assert data["message"] == "OK"

    aresponses.assert_plan_strictly_followed()
