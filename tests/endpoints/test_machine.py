"""Define tests for api endpoints."""
import json
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from regenmaschine import Client
from tests.common import TEST_HOST, TEST_PASSWORD, TEST_PORT, load_fixture


@pytest.fixture(name="machine_check_update_response")
def machine_check_update_response_fixture() -> dict[str, Any]:
    """Return an API response that contains firmware update check data.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("machine_check_update_response.json"))
    )


@pytest.fixture(name="machine_get_update_response")
def machine_get_update_response_fixture() -> dict[str, Any]:
    """Return an API response that contains firmware update data.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("machine_get_update_response.json"))
    )


@pytest.mark.asyncio
async def test_get_firmware_update_status(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    machine_check_update_response: dict[str, Any],
    machine_get_update_response: dict[str, Any],
) -> None:
    """Test getting the status of a firmware update.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        machine_check_update_response: An API response payload.
        machine_get_update_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update/check",
            "post",
            response=aiohttp.web_response.json_response(
                machine_check_update_response, status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update",
            "get",
            response=aiohttp.web_response.json_response(
                machine_get_update_response, status=200
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
            assert len(data["packageDetails"]) == 2

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_firmware_update_status_gen1(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    machine_get_update_response: dict[str, Any],
) -> None:
    """Test getting the status of a firmware update on a 1st generation controller.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        machine_get_update_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update",
            "get",
            response=aiohttp.web_response.json_response(
                machine_get_update_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = Client(session=session)
            await client.load_local(
                TEST_HOST, TEST_PASSWORD, port=TEST_PORT, use_ssl=False
            )
            controller = next(iter(client.controllers.values()))

            # Simulate this controller being a 1st generation controller:
            controller.hardware_version = "1"

            data = await controller.machine.get_firmware_update_status()
            assert data["update"] is False
            assert data["updateStatus"] == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_reboot(
    aresponses: ResponsesMockServer, authenticated_local_client: ResponsesMockServer
) -> None:
    """Test requesting a reboot.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/reboot",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("machine_reboot_response.json")),
                status=200,
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

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_update_firmware(
    aresponses: ResponsesMockServer,
    authenticated_local_client: ResponsesMockServer,
    machine_check_update_response: dict[str, Any],
) -> None:
    """Test requesting a firmware update.

    Args:
        aresponses: An aresponses server.
        authenticated_local_client: A mock local controller.
        machine_check_update_response: An API response payload.
    """
    async with authenticated_local_client:
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update/check",
            "post",
            response=aiohttp.web_response.json_response(
                machine_check_update_response, status=200
            ),
        )
        authenticated_local_client.add(
            f"{TEST_HOST}:{TEST_PORT}",
            "/api/4/machine/update",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("machine_update_response.json")), status=200
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

    aresponses.assert_plan_strictly_followed()
