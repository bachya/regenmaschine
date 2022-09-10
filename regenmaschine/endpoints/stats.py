"""Define an object to interact with RainMachine statistics."""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, cast

from regenmaschine.endpoints import EndpointManager


class Stats(EndpointManager):
    """Define a statistics object."""

    async def on_date(self, date: datetime.date) -> dict[str, Any]:
        """Get statistics for a certain date."""
        return await self.controller.request(
            "get", f"dailystats/{date.strftime('%Y-%m-%d')}"
        )

    async def upcoming(self, details: bool = False) -> list[dict[str, Any]]:
        """Return watering statistics for the next 6 days."""
        endpoint = "dailystats"
        data_key = "DailyStats"
        if details:
            endpoint += "/details"
            data_key = "DailyStatsDetails"
        data = await self.controller.request("get", endpoint)
        return cast(List[Dict[str, Any]], data[data_key])
