"""Define an object to interact with programs."""
from typing import Awaitable, Callable


class Program:
    """Define a program object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def _post(self, program_id: int = None, json: dict = None) -> dict:
        """Post data to a (non)existing program."""
        return await self._request("post", f"program/{program_id}", json=json)

    async def all(self, include_inactive: bool = False) -> list:
        """Return all programs."""
        data: dict = await self._request("get", "program")
        return [p for p in data["programs"] if include_inactive or p["active"]]

    async def disable(self, program_id: int) -> dict:
        """Disable a program."""
        return await self._post(program_id, {"active": False})

    async def enable(self, program_id: int) -> dict:
        """Enable a program."""
        return await self._post(program_id, {"active": True})

    async def get(self, program_id: int) -> dict:
        """Return a specific program."""
        return await self._request("get", f"program/{program_id}")

    async def next(self) -> list:
        """Return the next run date/time for all programs."""
        data: dict = await self._request("get", "program/nextrun")
        return data["nextRuns"]

    async def running(self) -> list:
        """Return all running programs."""
        data: dict = await self._request("get", "watering/program")
        return data["programs"]

    async def start(self, program_id: int) -> dict:
        """Start a program."""
        return await self._request("post", f"program/{program_id}/start")

    async def stop(self, program_id: int) -> dict:
        """Stop a program."""
        return await self._request("post", f"program/{program_id}/stop")
