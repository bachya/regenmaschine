"""Define an object to interact with restriction info."""
from typing import Awaitable, Callable


class Restriction:
    """Define a restriction object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def current(self) -> dict:
        """Get currently active restrictions."""
        return await self._request("get", "restrictions/currently")

    async def hourly(self) -> list:
        """Get a list of restrictions that are active over the next hour."""
        data: dict = await self._request("get", "restrictions/hourly")
        return data["hourlyRestrictions"]

    async def raindelay(self) -> dict:
        """Get restriction info related to rain delays."""
        return await self._request("get", "restrictions/raindelay")

    async def universal(self) -> dict:
        """Get global (always active) restrictions."""
        return await self._request("get", "restrictions/global")
