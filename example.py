"""Run an example script to quickly test."""
import asyncio
import datetime

from aiohttp import ClientSession

from regenmaschine import Client, scan
from regenmaschine.errors import DiscoveryFailedError, RequestError


async def diagnostics(client: Client) -> None:
    """Output diagnostic information."""
    print('RAINMACHINE DIAGNOSTICS')
    data = await client.diagnostics.current()
    print('Uptime: {0}'.format(data['uptime']))
    print('Software Version: {0}'.format(data['softwareVersion']))


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        await run(websession)


async def parsers(client: Client) -> None:
    """Output parser-related information."""
    print('RAINMACHINE PARSERS')
    for parser in await client.parsers.current():
        print(parser['name'])


async def programs(client: Client) -> None:
    """Output program-related information."""
    print('ALL PROGRAMS')
    for program in await client.programs.all():
        print('Program #{0}: {1}'.format(program['uid'], program['name']))

    print()
    print('PROGRAM BY ID')
    program_1 = await client.programs.get(1)
    print("Program 1's Start Time: {0}".format(program_1['startTime']))

    print()
    print('NEXT RUN TIMES')
    for program in await client.programs.next():
        print('Program #{0}: {1}'.format(program['pid'], program['startTime']))

    print()
    print('RUNNING PROGRAMS')
    for program in await client.programs.running():
        print('Program #{0}'.format(program['uid']))

    print()
    print('STARTING PROGRAM #1')
    print(await client.programs.start(1))

    await asyncio.sleep(3)

    print()
    print('STOPPING PROGRAM #1')
    print(await client.programs.stop(1))


async def provisioning(client: Client) -> None:
    """Output provisioning-related information."""
    print('PROVISIONING INFO')
    name = await client.provisioning.device_name
    print('Device Name: {0}'.format(name))
    settings = await client.provisioning.settings()
    print('Database Path: {0}'.format(settings['system']['databasePath']))
    print('Station Name: {0}'.format(settings['location']['stationName']))
    wifi = await client.provisioning.wifi()
    print('IP Address: {0}'.format(wifi['ipAddress']))


async def restrictions(client: Client) -> None:
    """Output restriction-related information."""
    print('RESTRICTIONS')
    current = await client.restrictions.current()
    print('Rain Delay Restrictions: {0}'.format(current['rainDelay']))
    universal = await client.restrictions.universal()
    print('Freeze Protect: {0}'.format(universal['freezeProtectEnabled']))
    print('Hourly Restrictions:')
    for restriction in await client.restrictions.hourly():
        print(restriction['name'])
    raindelay = await client.restrictions.raindelay()
    print('Rain Delay Counter: {0}'.format(raindelay['delayCounter']))


async def stats(client: Client) -> None:
    """Output stat-related information."""
    print('STATS')
    today = await client.stats.on_date(date=datetime.date.today())
    print('Min for Today: {0}'.format(today['mint']))
    for day in await client.stats.upcoming(details=True):
        print('{0} Min: {1}'.format(day['day'], day['mint']))


async def watering(client: Client) -> None:
    """Output watering-related information."""
    print('WATERING')
    for day in await client.watering.log(date=datetime.date.today()):
        print('{0} duration: {1}'.format(day['date'], day['realDuration']))
    queue = await client.watering.queue()
    print('Current Queue: {0}'.format(queue))

    print('Runs:')
    for watering_run in await client.watering.runs(date=datetime.date.today()):
        print(
            '{0} ({1})'.format(watering_run['dateTime'], watering_run['et0']))

    print()
    print('STOPPING ALL WATERING')
    print(await client.watering.stop_all())


async def zones(client: Client) -> None:
    """Output zone-related information."""
    print('ALL ACTIVE ZONES')
    for zone in await client.zones.all(details=True):
        print(
            'Zone #{0}: {1} (soil: {2})'.format(
                zone['uid'], zone['name'], zone['soil']))

    print()
    print('ZONE BY ID')
    zone_1 = await client.zones.get(1, details=True)
    print(
        "Zone 1's Name: {0} (soil: {1})".format(
            zone_1['name'], zone_1['soil']))

    print()
    print('STARTING ZONE #1 FOR 3 SECONDS')
    print(await client.zones.start(1, 3))

    await asyncio.sleep(3)

    print()
    print('STOPPING ZONE #1')
    print(await client.zones.stop(1))


async def run(websession):
    """Run."""
    try:
        # Create a client manually:
        client = Client('<IP ADDRESS>', websession)

        # Or attempt to discover it on the local network:
        # print('Attempting to discover a RainMachine unit...\n')
        # client = await scan(websession)

        # Authenticate the client by providing the device password:
        await client.authenticate('<PASSWORD>')

        print('CLIENT INFORMATION')
        print('Name: {0}'.format(client.name))
        print('Host: {0}'.format(client.host))
        print('MAC Address: {0}'.format(client.mac))

        # Work with diagnostics:
        print()
        await diagnostics(client)

        # Work with parsers:
        print()
        await parsers(client)

        # Work with programs:
        print()
        await programs(client)

        # Work with provisioning:
        print()
        await provisioning(client)

        # Work with restrictions:
        print()
        await restrictions(client)

        # Work with restrictions:
        print()
        await stats(client)

        # Work with watering:
        print()
        await watering(client)

        # Work with zones:
        print()
        await zones(client)
    except RequestError as err:
        print(err)


asyncio.get_event_loop().run_until_complete(main())
