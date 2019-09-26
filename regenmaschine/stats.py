"""Define an object to interact with RainMachine statistics."""
import datetime
from typing import Awaitable, Callable


class Stats:
    """Define a statistics object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def on_date(self, date: datetime.date) -> dict:
        """Get statistics for a certain date."""
        return await self._request("get", f"dailystats/{date.strftime('%Y-%m-%d')}")

    async def upcoming(self, details: bool = False) -> list:
        """Return watering statistics for the next 6 days."""
        endpoint: str = "dailystats"
        key: str = "DailyStats"
        if details:
            endpoint += "/details"
            key = "DailyStatsDetails"
        data: dict = await self._request("get", endpoint)
        return data[key]
