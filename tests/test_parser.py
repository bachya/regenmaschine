"""Define tests for parser endpoints."""
import aiohttp
import pytest

from regenmaschine import Client

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_parsers_current(aresponses, authenticated_local_client):
    """Test getting all current parsers."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/parser",
            "get",
            aresponses.Response(text=load_fixture("parser_response.json"), status=200),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False)
            controller = next(iter(client.controllers.values()))

            data = await controller.parsers.current()
            assert len(data) == 1
            assert data[0]["name"] == "NOAA Parser"


@pytest.mark.asyncio
async def test_parsers_post_data(aresponses, authenticated_local_client):
    """Test pushing data to parser."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/parser/data",
            "post",
            aresponses.Response(
                text=load_fixture("parser_post_data_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False)
            controller = next(iter(client.controllers.values()))
            payload = load_fixture("parser_post_data_payload.json")
            data = await controller.parsers.post_data(payload)
            assert len(data) == 2
            assert data["message"] == "OK"
