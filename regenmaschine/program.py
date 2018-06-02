"""Define an object to get program data."""
from aiohttp import ClientSession


class Program(object):
    """Define a program object."""

    def __init__(self, request: ClientSession) -> None:
        """Initialize."""
        self._request = request

    async def all(self) -> dict:
        """Return all programs."""
        return await self._request('get', 'program')

    async def get(self, program_id: int) -> dict:
        """Return a specific program."""
        return await self._request('get', 'program/{0}'.format(program_id))

    async def next(self) -> dict:
        """Return the next run date/time for all programs."""
        return await self._request('get', 'program/nextrun')

    async def running(self) -> dict:
        """Return all running programs."""
        return await self._request('get', 'watering/program')

    async def start(self, program_id: int) -> dict:
        """Start a program."""
        return await self._request('post',
                                   'program/{0}/start'.format(program_id))

    async def stop(self, program_id: int) -> dict:
        """Stop a program."""
        return await self._request('post',
                                   'program/{0}/stop'.format(program_id))
