"""Define an object to interact with API info."""
from __future__ import annotations

from typing import Any, Awaitable, Callable


class API:  # pylint: disable=too-few-public-methods
    """Define an API object."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def versions(self) -> dict[str, Any]:
        """Get software, hardware, and API versions."""
        return await self._request("get", "apiVer")
