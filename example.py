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
            await client.load_local("<IP ADDRESS>", "<PASSWORD>")

            for controller in client.controllers.values():
                print("CLIENT INFORMATION")
                print(f"Name: {controller.name}")
                print(f"MAC Address: {controller.mac}")
                print(f"API Version: {controller.api_version}")
                print(f"Software Version: {controller.software_version}")
                print(f"Hardware Version: {controller.hardware_version}")

                # Work with diagnostics:
                print()
                print("RAINMACHINE DIAGNOSTICS")
                data = await controller.diagnostics.current()
                print(f"Uptime: {data['uptime']}")
                print(f"Software Version: {data['softwareVersion']}")

                # Work with parsers:
                print()
                print("RAINMACHINE PARSERS")
                for parser in await controller.parsers.current():
                    print(parser["name"])

                # Work with programs:
                print()
                print("ALL PROGRAMS")
                for program in await controller.programs.all(include_inactive=True):
                    print(f"Program #{program['uid']}: {program['name']}")

                print()
                print("PROGRAM BY ID")
                program_1 = await controller.programs.get(1)
                print(f"Program 1's Start Time: {program_1['startTime']}")

                print()
                print("NEXT RUN TIMES")
                for program in await controller.programs.next():
                    print(f"Program #{program['pid']}: {program['startTime']}")

                print()
                print("RUNNING PROGRAMS")
                for program in await controller.programs.running():
                    print(f"Program #{program['uid']}")

                print()
                print("STARTING PROGRAM #1")
                print(await controller.programs.start(1))

                await asyncio.sleep(3)

                print()
                print("STOPPING PROGRAM #1")
                print(await controller.programs.stop(1))

                # Work with provisioning:
                print()
                print("PROVISIONING INFO")
                name = await controller.provisioning.device_name
                print(f"Device Name: {name}")
                settings = await controller.provisioning.settings()
                print(f"Database Path: {settings['system']['databasePath']}")
                print(f"Station Name: {settings['location']['stationName']}")
                wifi = await controller.provisioning.wifi()
                print(f"IP Address: {wifi['ipAddress']}")

                # Work with restrictions:
                print()
                print("RESTRICTIONS")
                current = await controller.restrictions.current()
                print(f"Rain Delay Restrictions: {current['rainDelay']}")
                universal = await controller.restrictions.universal()
                print(f"Freeze Protect: {universal['freezeProtectEnabled']}")
                print("Hourly Restrictions:")
                for restriction in await controller.restrictions.hourly():
                    print(restriction["name"])
                raindelay = await controller.restrictions.raindelay()
                print(f"Rain Delay Counter: {raindelay['delayCounter']}")

                # Work with restrictions:
                print()
                print("STATS")
                today = await controller.stats.on_date(date=datetime.date.today())
                print(f"Min for Today: {today['mint']}")
                for day in await controller.stats.upcoming(details=True):
                    print(f"{day['day']} Min: {day['mint']}")

                # Work with watering:
                print()
                print("WATERING")
                for day in await controller.watering.log(date=datetime.date.today()):
                    print(f"{day['date']} duration: {day['realDuration']}")
                queue = await controller.watering.queue()
                print(f"Current Queue: {queue}")

                print("Runs:")
                for watering_run in await controller.watering.runs(
                    date=datetime.date.today()
                ):
                    print(f"{watering_run['dateTime']} ({watering_run['et0']})")

                print()
                print("PAUSING ALL WATERING FOR 30 SECONDS")
                print(await controller.watering.pause_all(30))

                await asyncio.sleep(3)

                print()
                print("UNPAUSING WATERING")
                print(await controller.watering.unpause_all())

                print()
                print("STOPPING ALL WATERING")
                print(await controller.watering.stop_all())

                # Work with zones:
                print()
                print("ALL ACTIVE ZONES")
                for zone in await controller.zones.all(details=True):
                    print(f"Zone #{zone['uid']}: {zone['name']} (soil: {zone['soil']})")

                print()
                print("ZONE BY ID")
                zone_1 = await controller.zones.get(1, details=True)
                print(f"Zone 1's Name: {zone_1['name']} (soil: {zone_1['soil']})")

                print()
                print("STARTING ZONE #1 FOR 3 SECONDS")
                print(await controller.zones.start(1, 3))

                await asyncio.sleep(3)

                print()
                print("STOPPING ZONE #1")
                print(await controller.zones.stop(1))
        except RainMachineError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
