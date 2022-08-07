"""Define an object to interact with restriction info."""
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, List, cast


class Restriction:
    """Define a restriction object."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def current(self) -> dict[str, Any]:
        """Get currently active restrictions."""
        return await self._request("get", "restrictions/currently")

    async def hourly(self) -> list[dict[str, Any]]:
        """Get a list of restrictions that are active over the next hour."""
        data = await self._request("get", "restrictions/hourly")
        return cast(List[Dict[str, Any]], data["hourlyRestrictions"])

    async def raindelay(self) -> dict[str, Any]:
        """Get restriction info related to rain delays."""
        return await self._request("get", "restrictions/raindelay")

    async def set_universal(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Set global (always active) restrictions based on a payload."""
        return await self._request("post", "restrictions/global", json=payload)

    async def universal(self) -> dict[str, Any]:
        """Get global (always active) restrictions."""
        return await self._request("get", "restrictions/global")
