"""Define an object to interact with API info."""
from typing import Awaitable, Callable


class API:  # pylint: disable=too-few-public-methods
    """Define an API object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def versions(self) -> dict:
        """Get software, hardware, and API versions."""
        return await self._request("get", "apiVer")
