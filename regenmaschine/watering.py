"""Define an object to interact with generic watering data/actions."""
import datetime
from typing import Awaitable, Callable


class Watering:
    """Define a watering object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def log(
        self, date: datetime.date = None, days: int = None, details: bool = False
    ) -> list:
        """Get watering information for X days from Y date."""
        endpoint: str = "watering/log"
        if details:
            endpoint += "/details"

        if date and days:
            endpoint = f"{endpoint}/{date.strftime('%Y-%m-%d')}/{days}"

        data: dict = await self._request("get", endpoint)
        return data["waterLog"]["days"]

    async def pause_all(self, seconds: int) -> dict:
        """Pause all watering for a specified number of seconds."""
        return await self._request(
            "post", "watering/pauseall", json={"duration": seconds}
        )

    async def queue(self) -> list:
        """Return the queue of active watering activities."""
        data: dict = await self._request("get", "watering/queue")
        return data["queue"]

    async def runs(self, date: datetime.date = None, days: int = None) -> list:
        """Return all program runs for X days from Y date."""
        endpoint: str = "watering/past"

        if date and days:
            endpoint = f"{endpoint}/{date.strftime('%Y-%m-%d')}/{days}"

        data: dict = await self._request("get", endpoint)
        return data["pastValues"]

    async def stop_all(self) -> dict:
        """Stop all programs and zones from running."""
        return await self._request("post", "watering/stopall")

    async def unpause_all(self) -> dict:
        """Unpause all paused watering."""
        return await self.pause_all(0)
