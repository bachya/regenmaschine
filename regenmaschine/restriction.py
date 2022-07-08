"""Define an object to interact with restriction info."""
from __future__ import annotations

from datetime import timedelta
from time import time
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

    async def restrict(self, duration: timedelta) -> dict[str, Any]:
        """Restrict all watering activities for a time period."""
        return await self._request(
            "post",
            "restrictions/global",
            json={
                "rainDelayStartTime": round(time()),
                "rainDelayDuration": duration.total_seconds(),
            },
        )

    async def universal(self) -> dict[str, Any]:
        """Get global (always active) restrictions."""
        return await self._request("get", "restrictions/global")

    async def unrestrict(self) -> dict[str, Any]:
        """Unrestrict all watering activities."""
        return await self._request(
            "post",
            "restrictions/global",
            json={
                "rainDelayStartTime": round(time()),
                "rainDelayDuration": 0,
            },
        )
