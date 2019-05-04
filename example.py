"""Run an example script to quickly test."""
# pylint: disable=too-many-locals,too-many-statements
import asyncio
import datetime

from aiohttp import ClientSession

from regenmaschine import Client
from regenmaschine.errors import RainMachineError


async def main():
    """Run."""
    async with ClientSession() as websession:
        try:
            client = Client(websession)
            await client.load_local('<IP ADDRESS>', '<PASSWORD>')

            for controller in client.controllers.values():
                print('CLIENT INFORMATION')
                print('Name: {0}'.format(controller.name))
                print('MAC Address: {0}'.format(controller.mac))
                print('API Version: {0}'.format(controller.api_version))
                print(
                    'Software Version: {0}'.format(
                        controller.software_version))
                print(
                    'Hardware Version: {0}'.format(
                        controller.hardware_version))

                # Work with diagnostics:
                print()
                print('RAINMACHINE DIAGNOSTICS')
                data = await controller.diagnostics.current()
                print('Uptime: {0}'.format(data['uptime']))
                print('Software Version: {0}'.format(data['softwareVersion']))

                # Work with parsers:
                print()
                print('RAINMACHINE PARSERS')
                for parser in await controller.parsers.current():
                    print(parser['name'])

                # Work with programs:
                print()
                print('ALL PROGRAMS')
                for program in await controller.programs.all(
                        include_inactive=True):
                    print(
                        'Program #{0}: {1}'.format(
                            program['uid'], program['name']))

                print()
                print('PROGRAM BY ID')
                program_1 = await controller.programs.get(1)
                print(
                    "Program 1's Start Time: {0}".format(
                        program_1['startTime']))

                print()
                print('NEXT RUN TIMES')
                for program in await controller.programs.next():
                    print(
                        'Program #{0}: {1}'.format(
                            program['pid'], program['startTime']))

                print()
                print('RUNNING PROGRAMS')
                for program in await controller.programs.running():
                    print('Program #{0}'.format(program['uid']))

                print()
                print('STARTING PROGRAM #1')
                print(await controller.programs.start(1))

                await asyncio.sleep(3)

                print()
                print('STOPPING PROGRAM #1')
                print(await controller.programs.stop(1))

                # Work with provisioning:
                print()
                print('PROVISIONING INFO')
                name = await controller.provisioning.device_name
                print('Device Name: {0}'.format(name))
                settings = await controller.provisioning.settings()
                print(
                    'Database Path: {0}'.format(
                        settings['system']['databasePath']))
                print(
                    'Station Name: {0}'.format(
                        settings['location']['stationName']))
                wifi = await controller.provisioning.wifi()
                print('IP Address: {0}'.format(wifi['ipAddress']))

                # Work with restrictions:
                print()
                print('RESTRICTIONS')
                current = await controller.restrictions.current()
                print(
                    'Rain Delay Restrictions: {0}'.format(
                        current['rainDelay']))
                universal = await controller.restrictions.universal()
                print(
                    'Freeze Protect: {0}'.format(
                        universal['freezeProtectEnabled']))
                print('Hourly Restrictions:')
                for restriction in await controller.restrictions.hourly():
                    print(restriction['name'])
                raindelay = await controller.restrictions.raindelay()
                print(
                    'Rain Delay Counter: {0}'.format(
                        raindelay['delayCounter']))

                # Work with restrictions:
                print()
                print('STATS')
                today = await controller.stats.on_date(
                    date=datetime.date.today())
                print('Min for Today: {0}'.format(today['mint']))
                for day in await controller.stats.upcoming(details=True):
                    print('{0} Min: {1}'.format(day['day'], day['mint']))

                # Work with watering:
                print()
                print('WATERING')
                for day in await controller.watering.log(
                        date=datetime.date.today()):
                    print(
                        '{0} duration: {1}'.format(
                            day['date'], day['realDuration']))
                queue = await controller.watering.queue()
                print('Current Queue: {0}'.format(queue))

                print('Runs:')
                for watering_run in await controller.watering.runs(
                        date=datetime.date.today()):
                    print(
                        '{0} ({1})'.format(
                            watering_run['dateTime'], watering_run['et0']))

                print()
                print('PAUSING ALL WATERING FOR 30 SECONDS')
                print(await controller.watering.pause_all(30))

                await asyncio.sleep(3)

                print()
                print('UNPAUSING WATERING')
                print(await controller.watering.unpause_all())

                print()
                print('STOPPING ALL WATERING')
                print(await controller.watering.stop_all())

                # Work with zones:
                print()
                print('ALL ACTIVE ZONES')
                for zone in await controller.zones.all(details=True):
                    print(
                        'Zone #{0}: {1} (soil: {2})'.format(
                            zone['uid'], zone['name'], zone['soil']))

                print()
                print('ZONE BY ID')
                zone_1 = await controller.zones.get(1, details=True)
                print(
                    "Zone 1's Name: {0} (soil: {1})".format(
                        zone_1['name'], zone_1['soil']))

                print()
                print('STARTING ZONE #1 FOR 3 SECONDS')
                print(await controller.zones.start(1, 3))

                await asyncio.sleep(3)

                print()
                print('STOPPING ZONE #1')
                print(await controller.zones.stop(1))
        except RainMachineError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
