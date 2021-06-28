"""Run an example script to quickly test."""
# pylint: disable=too-many-locals,too-many-statements
import asyncio
import datetime

from aiohttp import ClientSession

from regenmaschine import Client
from regenmaschine.errors import RainMachineError


async def main():
    """Run."""
    async with ClientSession() as session:
        try:
            client = Client(session=session)
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
                programs = await controller.programs.all(include_inactive=True)
                for program in programs.values():
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

                # Work with zones:
                print()
                print("ALL ACTIVE ZONES")
                zones = await controller.zones.all(details=True)
                for zone in zones.values():
                    print(f"Zone #{zone['uid']}: {zone['name']} (soil: {zone['soil']})")

                print()
                print("ZONE BY ID")
                zone_1 = await controller.zones.get(1, details=True)
                print(f"Zone 1's Name: {zone_1['name']} (soil: {zone_1['soil']})")
        except RainMachineError as err:
            print(err)


asyncio.run(main())
