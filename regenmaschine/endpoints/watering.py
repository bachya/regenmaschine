"""Define an object to interact with generic watering data/actions."""
from __future__ import annotations

import datetime
from typing import Any, cast

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
        """Get watering information for X days from Y date.

        Args:
            date: The date to examine.
            days: The number of days' worth of logs to retrieve.
            details: Whether to include extra details.

        Returns:
            An API response payload.
        """
        endpoint = "watering/log"
        if details:
            endpoint += "/details"

        if date and days:
            endpoint = f"{endpoint}/{date.strftime('%Y-%m-%d')}/{days}"

        data = await self.controller.request("get", endpoint)
        return cast(list[dict[str, Any]], data["waterLog"]["days"])

    @EndpointManager.raise_on_gen1_controller
    async def flowmeter(self) -> dict[str, Any]:
        """Return the registered values from flowmeter.

        Returns:
            An API response payload.
        """
        return await self.controller.request("get", "watering/flowmeter")

    @EndpointManager.raise_on_gen1_controller
    async def post_flowmeter(
        self, value: float, units: str = "litre"
    ) -> dict[str, Any]:
        """Add values to flowmeter counters from an external meter.

        Args:
            value: The flow meter value.
            units: A valid unit ("clicks", "gal", "m3" and "litre").

        Returns:
            An API response payload.
        """
        return await self.controller.request(
            "post", "watering/flowmeter", json={"value": value, "units": units}
        )

    @EndpointManager.raise_on_gen1_controller
    async def pause_all(self, seconds: int) -> dict[str, Any]:
        """Pause all watering for a specified number of seconds.

        Args:
            seconds: The number of seconds to pause.

        Returns:
            An API response payload.

        Raises:
            ValueError: Raised if the maximum duration is exceeded.
        """
        if seconds > MAX_PAUSE_DURATION:
            raise ValueError(
                f"Cannot pause watering for more than {MAX_PAUSE_DURATION} seconds"
            )

        return await self.controller.request(
            "post", "watering/pauseall", json={"duration": seconds}
        )

    @EndpointManager.raise_on_gen1_controller
    async def queue(self) -> list[dict[str, Any]]:
        """Return the queue of active watering activities.

        Returns:
            An API response payload.
        """
        data = await self.controller.request("get", "watering/queue")
        return cast(list[dict[str, Any]], data["queue"])

    @EndpointManager.raise_on_gen1_controller
    async def runs(
        self, date: datetime.date | None = None, days: int | None = None
    ) -> list[dict[str, Any]]:
        """Return all program runs for X days from Y date.

        Args:
            date: The date to examine.
            days: The number of days' worth of runs to retrieve.

        Returns:
            An API response payload.
        """
        endpoint = "watering/past"

        if date and days:
            endpoint = f"{endpoint}/{date.strftime('%Y-%m-%d')}/{days}"

        data = await self.controller.request("get", endpoint)
        return cast(list[dict[str, Any]], data["pastValues"])

    @EndpointManager.raise_on_gen1_controller
    async def stop_all(self) -> dict[str, Any]:
        """Stop all programs and zones from running.

        Returns:
            An API response payload.
        """
        return await self.controller.request("post", "watering/stopall")

    @EndpointManager.raise_on_gen1_controller
    async def unpause_all(self) -> dict[str, Any]:
        """Unpause all paused watering.

        Returns:
            An API response payload.
        """
        data = await self.pause_all(0)
        return cast(dict[str, Any], data)
