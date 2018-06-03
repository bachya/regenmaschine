"""Run an example script to quickly test."""
import asyncio

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
            print('Program #{0}: {1}'.format(program['pid'],
                                             program['startTime']))

        print()
        print('RUNNING PROGRAMS')
        for program in await client.programs.running():
            print('Program #{0}'.format(program['uid']))

        # print()
        # print('STARTING PROGRAM #1')
        # print(await client.programs.start(1))

        # await asyncio.sleep(3)

        # print()
        # print('STOPPING PROGRAM #1')
        # print(await client.programs.stop(1))

        print('ALL ACTIVE ZONES')
        for zone in await client.zones.all(details=True):
            print('Zone #{0}: {1} (soil: {2})'.format(
                zone['uid'], zone['name'], zone['soil']))

        print()
        print('ZONE BY ID')
        zone_1 = await client.zones.get(1, details=True)
        print("Zone 1's Name: {0} (soil: {1})".format(zone_1['name'],
                                                      zone_1['soil']))

        # print()
        # print('STARTING ZONE #1 FOR 3 SECONDS')
        # print(await client.zones.start(1, 3))

        # await asyncio.sleep(3)

        # print()
        # print('STOPPING ZONE #1')
        # print(await client.zones.stop(1))

        print()
        print('RAINMACHINE DIAGNOSTICS')
        data = await client.diagnostics.current()
        print('Uptime: {0}'.format(data['uptime']))
        print('Software Version: {0}'.format(data['softwareVersion']))

        print()
        print('RAINMACHINE PARSERS')
        for parser in await client.parsers.current():
            print(parser['name'])

        print()
        print('PROVISIONING INFO')
        name = await client.provisioning.device_name
        print('Device Name: {0}'.format(name))
        settings = await client.provisioning.settings()
        print('Database Path: {0}'.format(settings['system']['databasePath']))
        print('Station Name: {0}'.format(settings['location']['stationName']))
        wifi = await client.provisioning.wifi()
        print('IP Address: {0}'.format(wifi['ipAddress']))

        print()
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

    except RequestError as err:
        print(err)


asyncio.get_event_loop().run_until_complete(main())
