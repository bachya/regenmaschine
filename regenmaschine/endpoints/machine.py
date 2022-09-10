"""Define an object to interact with machine info."""
from __future__ import annotations

from typing import Any

from regenmaschine.endpoints import EndpointManager
from regenmaschine.errors import UnknownAPICallError


class Machine(EndpointManager):
    """Define an API object."""

    @EndpointManager.raise_on_gen1_controller
    async def _check_firmware_update_status(self) -> dict[str, Any]:
        """Check for new firmware update information."""
        return await self.controller.request("post", "machine/update/check")

    async def get_firmware_update_status(self) -> dict[str, Any]:
        """Get the status of any pending firmware updates."""
        try:
            await self._check_firmware_update_status()
        except UnknownAPICallError:
            # 1st generation controllers don't support the POST /machine/update/check
            # endpoint, so if that call fails because of an UnknownAPICallError, swallow
            # it (with the assumption that GET /machine/update will return the needed
            # information):
            pass
        return await self.controller.request("get", "machine/update")

    async def reboot(self) -> dict[str, Any]:
        """Reboot the controller."""
        return await self.controller.request("post", "machine/reboot")

    async def update_firmware(self) -> dict[str, Any]:
        """Attempt to start the firmware update."""
        return await self.controller.request("post", "machine/update")
