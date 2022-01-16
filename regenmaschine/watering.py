"""Define an object to interact with generic watering data/actions."""
import datetime
from typing import Any, Awaitable, Callable, Dict, List, Optional, cast

MAX_PAUSE_DURATION = 43200


class Watering:
    """Define a watering object."""

    def __init__(self, request: Callable[..., Awaitable[Dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def log(
        self,
        date: Optional[datetime.date] = None,
        days: Optional[int] = None,
        details: bool = False,
    ) -> List[Dict[str, Any]]:
        """Get watering information for X days from Y date."""
        endpoint = "watering/log"
        if details:
            endpoint += "/details"

        if date and days:
            endpoint = f"{endpoint}/{date.strftime('%Y-%m-%d')}/{days}"

        data = await self._request("get", endpoint)
        return cast(List[Dict[str, Any]], data["waterLog"]["days"])

    async def pause_all(self, seconds: int) -> Dict[str, Any]:
        """Pause all watering for a specified number of seconds."""
        if seconds > MAX_PAUSE_DURATION:
            raise ValueError(
                f"Cannot pause watering for more than {MAX_PAUSE_DURATION} seconds"
            )

        return await self._request(
            "post", "watering/pauseall", json={"duration": seconds}
        )

    async def queue(self) -> List[Dict[str, Any]]:
        """Return the queue of active watering activities."""
        data = await self._request("get", "watering/queue")
        return cast(List[Dict[str, Any]], data["queue"])

    async def runs(
        self, date: Optional[datetime.date] = None, days: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Return all program runs for X days from Y date."""
        endpoint = "watering/past"

        if date and days:
            endpoint = f"{endpoint}/{date.strftime('%Y-%m-%d')}/{days}"

        data = await self._request("get", endpoint)
        return cast(List[Dict[str, Any]], data["pastValues"])

    async def stop_all(self) -> Dict[str, Any]:
        """Stop all programs and zones from running."""
        return await self._request("post", "watering/stopall")

    async def unpause_all(self) -> Dict[str, Any]:
        """Unpause all paused watering."""
        return await self.pause_all(0)
