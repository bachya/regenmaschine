"""Define tests for api endpoints."""
import aiohttp
import pytest

from regenmaschine import Client

from .common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.mark.asyncio
async def test_get_firmware_update_status(aresponses, authenticated_local_client):
    """Test getting the status of a firmware update."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update/check",
            "post",
            aresponses.Response(
                text=load_fixture("machine_check_update_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update",
            "get",
            aresponses.Response(
                text=load_fixture("machine_get_update_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.machine.get_firmware_update_status()
            assert data["update"] is False
            assert data["updateStatus"] == 1


@pytest.mark.asyncio
async def test_get_firmware_update_status_gen1(aresponses, authenticated_local_client):
    """Test getting the status of a firmware update on a 1st generation controller."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update",
            "get",
            aresponses.Response(
                text=load_fixture("machine_get_update_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            # Simulate this controller being a 1st generation controller:
            controller.hardware_version = 1

            data = await controller.machine.get_firmware_update_status()
            assert data["update"] is False
            assert data["updateStatus"] == 1


@pytest.mark.asyncio
async def test_reboot(aresponses, authenticated_local_client):
    """Test requesting a reboot."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/reboot",
            "post",
            aresponses.Response(
                text=load_fixture("machine_reboot_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.machine.reboot()
            assert data["message"] == "OK"


@pytest.mark.asyncio
async def test_update_firmware(aresponses, authenticated_local_client):
    """Test requesting a firmware update."""
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update/check",
            "post",
            aresponses.Response(
                text=load_fixture("machine_check_update_response.json"), status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update",
            "post",
            aresponses.Response(
                text=load_fixture("machine_update_response.json"), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            data = await controller.machine.update_firmware()
            assert data["message"] == "OK"
