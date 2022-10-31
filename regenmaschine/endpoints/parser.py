"""Define an object to interact with RainMachine weather parsers."""
from __future__ import annotations

from typing import Any, cast

from regenmaschine.endpoints import EndpointManager


class Parser(EndpointManager):
    """Define a parser object."""

    async def current(self) -> list[dict[str, Any]]:
        """Get current diagnostics.

        Returns:
            An API response payload.
        """
        data = await self.controller.request("get", "parser")
        return cast(list[dict[str, Any]], data["parsers"])

    async def post_data(
        self, payload: dict[str, list[dict[str, Any]]]
    ) -> dict[str, Any]:
        """Post weather data from an external source.

        Reference API Documentation for details:
        https://rainmachine.docs.apiary.io/#reference/weather-services/parserdata/post

        Args:
            payload: A dictionary of parser data.

        Returns:
            An API response payload.
        """
        return await self.controller.request("post", "parser/data", json=payload)
