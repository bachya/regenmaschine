"""Define an object to interact with RainMachine weather parsers."""
from aiohttp import ClientSession


class Parser(object):  # pylint: disable=too-few-public-methods
    """Define a parser object."""

    def __init__(self, request: ClientSession) -> None:
        """Initialize."""
        self._request = request

    async def current(self) -> dict:
        """Get current diagnostics."""
        data = await self._request('get', 'parser')
        return data['parsers']
