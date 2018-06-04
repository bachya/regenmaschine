"""Define an object to interact with RainMachine statistics."""
import datetime

from aiohttp import ClientSession


class Stats(object):
    """Define a statistics object."""

    def __init__(self, request: ClientSession) -> None:
        """Initialize."""
        self._request = request

    async def on_date(self, date: datetime.date) -> dict:
        """Get statistics for a certain date."""
        return await self._request('get', 'dailystats/{0}'.format(
            date.strftime('%Y-%m-%d')))

    async def upcoming(self, details: bool = False) -> list:
        """Returns watering statistics for the next 6 days."""
        endpoint = 'dailystats'
        key = 'DailyStats'
        if details:
            endpoint += '/details'
            key = 'DailyStatsDetails'
        data = await self._request('get', endpoint)
        return data[key]
