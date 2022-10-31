"""Define an object to interact with provisioning info."""
from __future__ import annotations

from typing import Any, cast

from regenmaschine.endpoints import EndpointManager


class Provision(EndpointManager):
    """Define a provisioning object."""

    @property
    async def device_name(self) -> str:
        """Get the name of the device.

        Returns:
            The device name.
        """
        data = await self.controller.request("get", "provision/name")
        return cast(str, data["name"])

    async def settings(self) -> dict[str, Any]:
        """Get a multitude of settings info.

        Returns:
            An API response payload.
        """
        return await self.controller.request("get", "provision")

    async def wifi(self) -> dict[str, Any]:
        """Get wifi info from the device.

        Returns:
            An API response payload.
        """
        return await self.controller.request("get", "provision/wifi")
