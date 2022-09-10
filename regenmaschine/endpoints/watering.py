"""Define an object to interact with generic watering data/actions."""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, cast

from regenmaschine.endpoints import EndpointManager

MAX_PAUSE_DURATION = 43200


class Watering(EndpointManager):
    """Define a watering object."""

    @EndpointManager.raise_on_gen1_controller
    async def log(
        self,
        date: datetime.date | None = None,
        days: int | None = None,
        details: bool = False,
    ) -> list[dict[str, Any]]:
        """Get watering information for X days from Y date."""
        endpoint = "watering/log"
        if details:
            endpoint += "/details"

        if date and days:
            endpoint = f"{endpoint}/{date.strftime('%Y-%m-%d')}/{days}"

        data = await self.controller.request("get", endpoint)
        return cast(List[Dict[str, Any]], data["waterLog"]["days"])

    @EndpointManager.raise_on_gen1_controller
    async def pause_all(self, seconds: int) -> dict[str, Any]:
        """Pause all watering for a specified number of seconds."""
        if seconds > MAX_PAUSE_DURATION:
            raise ValueError(
                f"Cannot pause watering for more than {MAX_PAUSE_DURATION} seconds"
            )

        return await self.controller.request(
            "post", "watering/pauseall", json={"duration": seconds}
        )

    @EndpointManager.raise_on_gen1_controller
    async def queue(self) -> list[dict[str, Any]]:
        """Return the queue of active watering activities."""
        data = await self.controller.request("get", "watering/queue")
        return cast(List[Dict[str, Any]], data["queue"])

    @EndpointManager.raise_on_gen1_controller
    async def runs(
        self, date: datetime.date | None = None, days: int | None = None
    ) -> list[dict[str, Any]]:
        """Return all program runs for X days from Y date."""
        endpoint = "watering/past"

        if date and days:
            endpoint = f"{endpoint}/{date.strftime('%Y-%m-%d')}/{days}"

        data = await self.controller.request("get", endpoint)
        return cast(List[Dict[str, Any]], data["pastValues"])

    @EndpointManager.raise_on_gen1_controller
    async def stop_all(self) -> dict[str, Any]:
        """Stop all programs and zones from running."""
        return await self.controller.request("post", "watering/stopall")

    @EndpointManager.raise_on_gen1_controller
    async def unpause_all(self) -> dict[str, Any]:
        """Unpause all paused watering."""
        data = await self.pause_all(0)
        return cast(Dict[str, Any], data)
