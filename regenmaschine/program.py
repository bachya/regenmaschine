"""Define an object to interact with programs."""
from typing import Awaitable, Callable


class Program:
    """Define a program object."""

    def __init__(self, request: Callable[..., Awaitable[dict]]) -> None:
        """Initialize."""
        self._request = request

    async def all(self) -> list:
        """Return all programs."""
        data = await self._request('get', 'program')
        return data['programs']

    async def get(self, program_id: int) -> dict:
        """Return a specific program."""
        return await self._request('get', 'program/{0}'.format(program_id))

    async def next(self) -> list:
        """Return the next run date/time for all programs."""
        data = await self._request('get', 'program/nextrun')
        return data['nextRuns']

    async def running(self) -> list:
        """Return all running programs."""
        data = await self._request('get', 'watering/program')
        return data['programs']

    async def start(self, program_id: int) -> dict:
        """Start a program."""
        return await self._request(
            'post', 'program/{0}/start'.format(program_id))

    async def stop(self, program_id: int) -> dict:
        """Stop a program."""
        return await self._request(
            'post', 'program/{0}/stop'.format(program_id))
