"""Define tests for diagnostics endpoints."""
import aiohttp
import pytest

from regenmaschine import Client

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_diagnostics_current(aresponses, authenticated_local_client):
    """Test retrieving current diagnostics."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/diag",
            "get",
            aresponses.Response(text=load_fixture("diag_response.json"), status=200),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False)
            controller = next(iter(client.controllers.values()))

            data = await controller.diagnostics.current()
            assert data["memUsage"] == 18220


@pytest.mark.asyncio
async def test_diagnostics_log(aresponses, authenticated_local_client):
    """Test retrieving the entire diagnostics log."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/diag/log",
            "get",
            aresponses.Response(
                text=load_fixture("diag_log_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(TEST_HOST, TEST_PASSWORD, port=TEST_PORT, ssl=False)
            controller = next(iter(client.controllers.values()))

            data = await controller.diagnostics.log()
            assert data == "----"
