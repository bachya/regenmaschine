"""Define an object to interact with provisioning info."""
from aiohttp import ClientSession


class Provision(object):
    """Define a provisioning object."""

    def __init__(self, request: ClientSession) -> None:
        """Initialize."""
        self._request = request

    @property
    async def device_name(self) -> str:
        """Get the name of the device."""
        data = await self._request('get', 'provision/name')
        return data['name']

    async def settings(self) -> dict:
        """Get a multitude of settings info."""
        return await self._request('get', 'provision')

    async def wifi(self) -> dict:
        """Get wifi info from the device."""
        return await self._request('get', 'provision/wifi')
