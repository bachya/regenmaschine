"""Define an object to interact with RainMachine diagnostics."""
from __future__ import annotations

from typing import Any, cast

from regenmaschine.endpoints import EndpointManager


class Diagnostics(EndpointManager):
    """Define a diagnostics object."""

    @EndpointManager.raise_on_gen1_controller
    async def current(self) -> dict[str, Any]:
        """Get current diagnostics.

        Returns:
            An API response payload.
        """
        return await self.controller.request("get", "diag")

    @EndpointManager.raise_on_gen1_controller
    async def log(self) -> str:
        """Get the device log.

        Returns:
            A log string.
        """
        data = await self.controller.request("get", "diag/log")
        return cast(str, data["log"])
