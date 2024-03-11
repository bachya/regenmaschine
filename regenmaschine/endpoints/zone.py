"""Define an object to interact with zones."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from regenmaschine.endpoints import EndpointManager


class Zone(EndpointManager):
    """Define a zone object."""

    async def _post(self, zone_id: int, json: dict[str, Any]) -> dict[str, Any]:
        """Post data to a (non)existing zone.

        Args:
            zone_id: A zone ID.
            json: An API request payload.

        Returns:
            An API response payload.
        """
        return await self.controller.request(
            "post", f"zone/{zone_id}/properties", json=json
        )

    async def all(
        self, *, details: bool = False, include_inactive: bool = False
    ) -> dict[int, dict[str, Any]]:
        """Return all zones (with optional advanced properties).

        Args:
            details: Whether extra details should be included.
            include_inactive: Whether to include inactive programs.

        Returns:
            An API response payload.
        """
        raw_zones = await self.controller.request("get", "zone")
        zone_details: dict | None = None

        if details:
            zone_details = await self.controller.request("get", "zone/properties")

        zones: dict[int, dict[str, Any]] = {}
        for zone in raw_zones["zones"]:
            if details:
                if TYPE_CHECKING:
                    assert zone_details is not None
                [extra] = [z for z in zone_details["zones"] if z["uid"] == zone["uid"]]
                zone_data = {**zone, **extra}
            else:
                if "active" not in zone:
                    zone["active"] = True
                zone_data = zone

            if zone_data["active"] or include_inactive:
                zones[zone_data["uid"]] = zone_data

        return zones

    async def disable(self, zone_id: int) -> dict[str, Any]:
        """Disable a zone.

        Args:
            zone_id: A zone ID.

        Returns:
            An API response payload.
        """
        return await self._post(zone_id, {"active": False})

    async def enable(self, zone_id: int) -> dict[str, Any]:
        """Enable a zone.

        Args:
            zone_id: A zone ID.

        Returns:
            An API response payload.
        """
        return await self._post(zone_id, {"active": True})

    async def get(self, zone_id: int, *, details: bool = False) -> dict[str, Any]:
        """Return a specific zone.

        Args:
            zone_id: A zone ID.
            details: Whether extra details should be included.

        Returns:
            An API response payload.
        """
        zone = await self.controller.request("get", f"zone/{zone_id}")
        if not details:
            return zone
        zone_details = await self.controller.request(
            "get", f"zone/{zone_id}/properties"
        )
        return {**zone, **zone_details}

    async def running(self) -> list[dict[str, Any]]:
        """Return all running zones.

        Returns:
            An API response payload.
        """
        data = await self.controller.request("get", "watering/zone")
        return cast(list[dict[str, Any]], data["zones"])

    async def start(self, zone_id: int, time: int) -> dict[str, Any]:
        """Start a zone.

        Note that in addition to including it in the query URL, the zone ID must be
        provided in the request body to accommodate 1st generation controllers.

        Args:
            zone_id: A zone ID.
            time: The number of seconds to run the zone for.

        Returns:
            An API response payload.
        """
        return await self.controller.request(
            "post", f"zone/{zone_id}/start", json={"time": time, "zid": zone_id}
        )

    async def stop(self, zone_id: int) -> dict[str, Any]:
        """Stop a zone.

        Note that in addition to including it in the query URL, the zone ID must be
        provided in the request body to accommodate 1st generation controllers.

        Args:
            zone_id: A zone ID.

        Returns:
            An API response payload.
        """
        return await self.controller.request(
            "post", f"zone/{zone_id}/stop", json={"zid": zone_id}
        )
