"""Define an object to interact with provisioning info."""
from typing import Any, Awaitable, Callable, Dict, cast


class Provision:
    """Define a provisioning object."""

    def __init__(self, request: Callable[..., Awaitable[Dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    @property
    async def device_name(self) -> str:
        """Get the name of the device."""
        data = await self._request("get", "provision/name")
        return cast(str, data["name"])

    async def settings(self) -> Dict[str, Any]:
        """Get a multitude of settings info."""
        return await self._request("get", "provision")

    async def wifi(self) -> Dict[str, Any]:
        """Get wifi info from the device."""
        return await self._request("get", "provision/wifi")
