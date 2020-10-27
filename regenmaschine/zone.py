"""Define an object to interact with zones."""
import asyncio
from typing import Awaitable, Callable, Dict


class Zone:
    """Define a zone object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request

    async def _post(self, zone_id: int = None, json: dict = None) -> dict:
        """Post data to a (non)existing zone."""
        return await self._request("post", f"zone/{zone_id}/properties", json=json)

    async def all(
        self, *, details: bool = False, include_inactive: bool = False
    ) -> Dict[int, dict]:
        """Return all zones (with optional advanced properties)."""
        tasks = [self._request("get", "zone")]
        if details:
            tasks.append(self._request("get", "zone/properties"))

        results = await asyncio.gather(*tasks)

        if len(results) == 1:
            return {
                zone["uid"]: zone
                for zone in results[0]["zones"]
                if zone["active"] or include_inactive
            }

        return {
            zone["uid"]: {
                **zone,
                **next((z for z in results[1]["zones"] if z["uid"] == zone["uid"])),
            }
            for zone in results[0]["zones"]
            if zone["active"] or include_inactive
        }

    async def disable(self, zone_id: int) -> dict:
        """Disable a zone."""
        return await self._post(zone_id, {"active": False})

    async def enable(self, zone_id: int) -> dict:
        """Enable a zone."""
        return await self._post(zone_id, {"active": True})

    async def get(self, zone_id: int, *, details: bool = False) -> dict:
        """Return a specific zone."""
        tasks = [self._request("get", f"zone/{zone_id}")]
        if details:
            tasks.append(self._request("get", f"zone/{zone_id}/properties"))

        results = await asyncio.gather(*tasks)

        if len(results) == 1:
            return results[0]

        return {**results[0], **results[1]}

    async def start(self, zone_id: int, time: int) -> dict:
        """Start a program."""
        return await self._request("post", f"zone/{zone_id}/start", json={"time": time})

    async def stop(self, zone_id: int) -> dict:
        """Stop a program."""
        return await self._request("post", f"zone/{zone_id}/stop")
