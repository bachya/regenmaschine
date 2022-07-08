"""Define an object to interact with RainMachine statistics."""
from __future__ import annotations

import datetime
from typing import Any, Awaitable, Callable, Dict, List, cast


class Stats:
    """Define a statistics object."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def on_date(self, date: datetime.date) -> dict[str, Any]:
        """Get statistics for a certain date."""
        return await self._request("get", f"dailystats/{date.strftime('%Y-%m-%d')}")

    async def upcoming(self, details: bool = False) -> list[dict[str, Any]]:
        """Return watering statistics for the next 6 days."""
        endpoint = "dailystats"
        key = "DailyStats"
        if details:
            endpoint += "/details"
            key = "DailyStatsDetails"
        data = await self._request("get", endpoint)
        return cast(List[Dict[str, Any]], data[key])
