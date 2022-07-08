"""Define an object to interact with programs."""
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, List, cast


class Program:
    """Define a program object."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def all(self, include_inactive: bool = False) -> dict[int, dict[str, Any]]:
        """Return all programs."""
        data = await self._request("get", "program")
        return {
            program["uid"]: program
            for program in data["programs"]
            if include_inactive or program["active"]
        }

    async def disable(self, program_id: int) -> dict[str, Any]:
        """Disable a program."""
        return await self._request(
            "post", f"program/{program_id}", json={"active": False}
        )

    async def enable(self, program_id: int) -> dict[str, Any]:
        """Enable a program."""
        return await self._request(
            "post", f"program/{program_id}", json={"active": True}
        )

    async def get(self, program_id: int) -> dict[str, Any]:
        """Return a specific program."""
        return await self._request("get", f"program/{program_id}")

    async def next(self) -> list[dict[str, Any]]:
        """Return the next run date/time for all programs."""
        data = await self._request("get", "program/nextrun")
        return cast(List[Dict[str, Any]], data["nextRuns"])

    async def running(self) -> list[dict[str, Any]]:
        """Return all running programs."""
        data = await self._request("get", "watering/program")
        return cast(List[Dict[str, Any]], data["programs"])

    async def start(self, program_id: int) -> dict[str, Any]:
        """Start a program.

        Note that in addition to including it in the query URL, the program ID must be
        provided in the request body to accommodate 1st generation controllers.
        """
        return await self._request(
            "post", f"program/{program_id}/start", json={"pid": program_id}
        )

    async def stop(self, program_id: int) -> dict[str, Any]:
        """Stop a program.

        Note that in addition to including it in the query URL, the program ID must be
        provided in the request body to accommodate 1st generation controllers.
        """
        return await self._request(
            "post", f"program/{program_id}/stop", json={"pid": program_id}
        )
