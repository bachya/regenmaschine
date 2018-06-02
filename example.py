"""Run an example script to quickly test."""
import asyncio
from pprint import pprint

from aiohttp import ClientSession

from regenmaschine import Client, RequestError


async def main():
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        await run(websession)


async def run(websession):
    """Run."""
    client = Client('localhost', websession, port=9999)

    try:
        await client.authenticate('yvV880VFQFs*X6IHh[YWoKnVU')

        next_run = await client.programs.next()
        pprint(next_run)
    except RequestError as err:
        print(err)


asyncio.get_event_loop().run_until_complete(main())
