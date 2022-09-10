"""Define an object to interact with restriction info."""
from __future__ import annotations

from typing import Any, Dict, List, cast

from regenmaschine.endpoints import EndpointManager


class Restriction(EndpointManager):
    """Define a restriction object."""

    @EndpointManager.raise_on_gen1_controller
    async def current(self) -> dict[str, Any]:
        """Get currently active restrictions."""
        return await self.controller.request("get", "restrictions/currently")

    @EndpointManager.raise_on_gen1_controller
    async def hourly(self) -> list[dict[str, Any]]:
        """Get a list of restrictions that are active over the next hour."""
        data = await self.controller.request("get", "restrictions/hourly")
        return cast(List[Dict[str, Any]], data["hourlyRestrictions"])

    async def raindelay(self) -> dict[str, Any]:
        """Get restriction info related to rain delays."""
        return await self.controller.request("get", "restrictions/raindelay")

    @EndpointManager.raise_on_gen1_controller
    async def set_universal(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Set global (always active) restrictions based on a payload."""
        return await self.controller.request(
            "post", "restrictions/global", json=payload
        )

    @EndpointManager.raise_on_gen1_controller
    async def universal(self) -> dict[str, Any]:
        """Get global (always active) restrictions."""
        return await self.controller.request("get", "restrictions/global")
