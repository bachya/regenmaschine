"""Define an object to interact with RainMachine diagnostics."""
from typing import Awaitable, Callable


class Diagnostics:
    """Define a diagnostics object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def current(self) -> dict:
        """Get current diagnostics."""
        return await self._request("get", "diag")

    async def log(self) -> dict:
        """Get the device log."""
        data: dict = await self._request("get", "diag/log")
        return data["log"]
