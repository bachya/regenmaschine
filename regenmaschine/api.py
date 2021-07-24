"""Define an object to interact with API info."""
from typing import Any, Awaitable, Callable, Dict


class API:  # pylint: disable=too-few-public-methods
    """Define an API object."""

    def __init__(self, request: Callable[..., Awaitable[Dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def versions(self) -> Dict[str, Any]:
        """Get software, hardware, and API versions."""
        return await self._request("get", "apiVer")
