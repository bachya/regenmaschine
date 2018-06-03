"""Define an object to interact with RainMachine diagnostics."""
from aiohttp import ClientSession


class Diagnostics(object):
    """Define a diagnostics object."""

    def __init__(self, request: ClientSession) -> None:
        """Initialize."""
        self._request = request

    async def current(self) -> dict:
        """Get current diagnostics."""
        return await self._request('get', 'diag')

    async def log(self) -> dict:
        """Get the device log."""
        data = await self._request('get', 'diag/log')
        return data['log']
