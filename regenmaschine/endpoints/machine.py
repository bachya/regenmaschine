"""Define an object to interact with machine info."""
from __future__ import annotations

from typing import Any

from regenmaschine.endpoints import EndpointManager


class Machine(EndpointManager):  # pylint: disable=too-few-public-methods
    """Define an API object."""

    @EndpointManager.raise_on_gen1_controller
    async def get_firmware_update_status(self) -> dict[str, Any]:
        """Get the status of any pending firmware updates."""
        return await self.controller.request("get", "machine/update")

    async def reboot(self) -> dict[str, Any]:
        """Reboot the controller."""
        return await self.controller.request("post", "machine/reboot")

    async def update_firmware(self) -> dict[str, Any]:
        """Attempt to start the firmware update."""
        return await self.controller.request("post", "machine/update")
