"""Define an object to interact with zones."""
import asyncio
from typing import Any, Awaitable, Callable, Dict, Optional, cast


class Zone:
    """Define a zone object."""

    def __init__(self, request: Callable[..., Awaitable[Dict[str, Any]]]) -> None:
        """Initialize."""
        self._request = request

    async def _post(
        self, zone_id: int, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Post data to a (non)existing zone."""
        return await self._request("post", f"zone/{zone_id}/properties", json=json)

    async def all(
        self, *, details: bool = False, include_inactive: bool = False
    ) -> Dict[int, Dict[str, Any]]:
        """Return all zones (with optional advanced properties)."""
        tasks = [self._request("get", "zone")]

        if details:
            tasks.append(self._request("get", "zone/properties"))

        results = await asyncio.gather(*tasks)

        zones = {}
        for zone in results[0]["zones"]:
            if details:
                [extra] = [z for z in results[1]["zones"] if z["uid"] == zone["uid"]]
                zone_data = {**zone, **extra}
            else:
                if "active" not in zone:
                    zone["active"] = True
                zone_data = zone

            if zone_data["active"] or include_inactive:
                zones[zone_data["uid"]] = zone_data

        return zones

    async def disable(self, zone_id: int) -> Dict[str, Any]:
        """Disable a zone."""
        return await self._post(zone_id, {"active": False})

    async def enable(self, zone_id: int) -> Dict[str, Any]:
        """Enable a zone."""
        return await self._post(zone_id, {"active": True})

    async def get(self, zone_id: int, *, details: bool = False) -> Dict[str, Any]:
        """Return a specific zone."""
        tasks = [self._request("get", f"zone/{zone_id}")]
        if details:
            tasks.append(self._request("get", f"zone/{zone_id}/properties"))

        results = await asyncio.gather(*tasks)

        if len(results) == 1:
            return cast(Dict[str, Any], results[0])

        return {**results[0], **results[1]}

    async def start(self, zone_id: int, time: int) -> Dict[str, Any]:
        """Start a zone.

        Note that in addition to including it in the query URL, the zone ID must be
        provided in the request body to accommodate 1st generation controllers.
        """
        return await self._request(
            "post", f"zone/{zone_id}/start", json={"time": time, "zid": zone_id}
        )

    async def stop(self, zone_id: int) -> Dict[str, Any]:
        """Stop a zone.

        Note that in addition to including it in the query URL, the zone ID must be
        provided in the request body to accommodate 1st generation controllers.
        """
        return await self._request(
            "post", f"zone/{zone_id}/stop", json={"zid": zone_id}
        )
