"""Define an object to interact with RainMachine weather parsers."""
from typing import Awaitable, Callable


class Parser:  # pylint: disable=too-few-public-methods
    """Define a parser object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def current(self) -> dict:
        """Get current diagnostics."""
        data: dict = await self._request("get", "parser")
        return data["parsers"]
