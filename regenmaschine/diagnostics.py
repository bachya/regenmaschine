"""Define an object to interact with RainMachine diagnostics."""
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, cast


class Diagnostics:
    """Define a diagnostics object."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def current(self) -> dict[str, Any]:
        """Get current diagnostics."""
        return await self._request("get", "diag")

    async def log(self) -> dict[str, Any]:
        """Get the device log."""
        data = await self._request("get", "diag/log")
        return cast(Dict[str, Any], data["log"])
