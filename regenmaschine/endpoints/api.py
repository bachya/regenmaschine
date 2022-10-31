"""Define an object to interact with API info."""
from __future__ import annotations

from typing import Any

from regenmaschine.endpoints import EndpointManager


class API(EndpointManager):  # pylint: disable=too-few-public-methods
    """Define an API object."""

    async def versions(self) -> dict[str, Any]:
        """Get software, hardware, and API versions.

        Returns:
            An API response payload.
        """
        return await self.controller.request("get", "apiVer")
