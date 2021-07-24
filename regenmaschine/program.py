"""Define an object to interact with programs."""
from typing import Any, Awaitable, Callable, Dict, List, cast


class Program:
    """Define a program object."""

    def __init__(self, request: Callable[..., Awaitable[Dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def all(self, include_inactive: bool = False) -> Dict[int, Dict[str, Any]]:
        """Return all programs."""
        data = await self._request("get", "program")
        return {
            program["uid"]: program
            for program in data["programs"]
            if include_inactive or program["active"]
        }

    async def disable(self, program_id: int) -> Dict[str, Any]:
        """Disable a program."""
        return await self._request(
            "post", f"program/{program_id}", json={"active": False}
        )

    async def enable(self, program_id: int) -> Dict[str, Any]:
        """Enable a program."""
        return await self._request(
            "post", f"program/{program_id}", json={"active": True}
        )

    async def get(self, program_id: int) -> Dict[str, Any]:
        """Return a specific program."""
        return await self._request("get", f"program/{program_id}")

    async def next(self) -> List[Dict[str, Any]]:
        """Return the next run date/time for all programs."""
        data = await self._request("get", "program/nextrun")
        return cast(List[Dict[str, Any]], data["nextRuns"])

    async def running(self) -> List[Dict[str, Any]]:
        """Return all running programs."""
        data = await self._request("get", "watering/program")
        return cast(List[Dict[str, Any]], data["programs"])

    async def start(self, program_id: int) -> Dict[str, Any]:
        """Start a program."""
        return await self._request("post", f"program/{program_id}/start")

    async def stop(self, program_id: int) -> Dict[str, Any]:
        """Stop a program."""
        return await self._request("post", f"program/{program_id}/stop")
