"""Define an object to interact with RainMachine weather parsers."""
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, cast


class Parser:
    """Define a parser object."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def current(self) -> dict[str, Any]:
        """Get current diagnostics."""
        data = await self._request("get", "parser")
        return cast(Dict[str, Any], data["parsers"])

    async def post_data(
        self, payload: dict[str, list[dict[str, Any]]]
    ) -> dict[str, Any]:
        """Post weather data from an external source.

        Reference API Documentation for details:
        https://rainmachine.docs.apiary.io/#reference/weather-services/parserdata/post
        """
        return await self._request("post", "parser/data", json=payload)
