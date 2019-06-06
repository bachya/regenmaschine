"""Define an object to interact with zones."""
from typing import Awaitable, Callable


class Zone:
    """Define a zone object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request = request

    async def _post(self, zone_id: int = None, json: dict = None) -> dict:
        """Post data to a (non)existing zone."""
        return await self._request(
            "post", "zone/{0}/properties".format(zone_id), json=json
        )

    async def all(
        self, *, details: bool = False, include_inactive: bool = False
    ) -> list:
        """Return all zones (with optional advanced properties)."""
        endpoint = "zone"
        if details:
            endpoint += "/properties"
        data = await self._request("get", endpoint)
        return [z for z in data["zones"] if include_inactive or z["active"]]

    async def disable(self, zone_id: int) -> dict:
        """Disable a zone."""
        return await self._post(zone_id, {"active": False})

    async def enable(self, zone_id: int) -> dict:
        """Enable a zone."""
        return await self._post(zone_id, {"active": True})

    async def get(self, zone_id: int, *, details: bool = False) -> dict:
        """Return a specific zone."""
        endpoint = "zone/{0}".format(zone_id)
        if details:
            endpoint += "/properties"
        return await self._request("get", endpoint)

    async def start(self, zone_id: int, time: int) -> dict:
        """Start a program."""
        return await self._request(
            "post", "zone/{0}/start".format(zone_id), json={"time": time}
        )

    async def stop(self, zone_id: int) -> dict:
        """Stop a program."""
        return await self._request("post", "zone/{0}/stop".format(zone_id))
