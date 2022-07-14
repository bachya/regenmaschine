"""Define an object to interact with machine info."""
from __future__ import annotations

from typing import Any, Awaitable, Callable


class Machine:  # pylint: disable=too-few-public-methods
    """Define an API object."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def _handle_firmware_request(self, method: str) -> dict[str, Any]:
        """Handle a firmware-related request."""
        await self._request("post", "machine/update/check")
        return await self._request(method, "machine/update")

    async def get_firmware_update_status(self) -> dict[str, Any]:
        """Get the status of any pending firmware updates."""
        return await self._handle_firmware_request("get")

    async def reboot(self) -> dict[str, Any]:
        """Reboot the controller."""
        return await self._request("post", "machine/reboot")

    async def update_firmware(self) -> dict[str, Any]:
        """Attempt to start the firmware update."""
        return await self._handle_firmware_request("post")
