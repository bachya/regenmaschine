"""Run an example script to quickly test."""

# pylint: disable=too-many-locals,too-many-statements
import asyncio
import datetime
import logging

from aiohttp import ClientSession

from regenmaschine import Client
from regenmaschine.errors import RainMachineError

IP_ADDRESS = "<IP_ADDRESS>"
PASSWORD = "<PASSWORD>"  # noqa: S105

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Run."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            client = Client(session=session)
            await client.load_local(IP_ADDRESS, PASSWORD)

            for controller in client.controllers.values():
                _LOGGER.info("CLIENT INFORMATION")
                _LOGGER.info("Name: %s", controller.name)
                _LOGGER.info("MAC Address: %s", controller.mac)
                _LOGGER.info("API Version: %s", controller.api_version)
                _LOGGER.info("Software Version: %s", controller.software_version)
                _LOGGER.info("Hardware Version: %s", controller.hardware_version)

                _LOGGER.info("RAINMACHINE DIAGNOSTICS")
                diagnostics = await controller.diagnostics.current()
                _LOGGER.info(diagnostics)

                _LOGGER.info("RAINMACHINE PARSERS")
                parsers = await controller.parsers.current()
                _LOGGER.info(parsers)

                # Work with programs:
                _LOGGER.info("ALL PROGRAMS")
                programs = await controller.programs.all(include_inactive=True)
                _LOGGER.info(programs)

                _LOGGER.info("NEXT RUN TIMES")
                next_programs = await controller.programs.next()
                _LOGGER.info(next_programs)

                _LOGGER.info("RUNNING PROGRAMS")
                running_programs = await controller.programs.running()
                _LOGGER.info(running_programs)

                _LOGGER.info("PROVISIONING INFO")
                name = await controller.provisioning.device_name
                _LOGGER.info("Device Name: %s", name)
                settings = await controller.provisioning.settings()
                _LOGGER.info(settings)
                wifi = await controller.provisioning.wifi()
                _LOGGER.info(wifi)

                _LOGGER.info("RESTRICTIONS")
                current = await controller.restrictions.current()
                _LOGGER.info(current)
                universal = await controller.restrictions.universal()
                _LOGGER.info(universal)
                hourly = await controller.restrictions.hourly()
                _LOGGER.info(hourly)
                raindelay = await controller.restrictions.raindelay()
                _LOGGER.info(raindelay)

                _LOGGER.info("STATS")
                today = await controller.stats.on_date(date=datetime.date.today())
                _LOGGER.info(today)
                upcoming = await controller.stats.upcoming(details=True)
                _LOGGER.info(upcoming)

                _LOGGER.info("WATERING")
                log = await controller.watering.log(date=datetime.date.today())
                _LOGGER.info(log)
                queue = await controller.watering.queue()
                _LOGGER.info(queue)

                runs = await controller.watering.runs(date=datetime.date.today())
                _LOGGER.info(runs)

                _LOGGER.info("ALL ACTIVE ZONES")
                zones = await controller.zones.all(details=True)
                _LOGGER.info(zones)

                _LOGGER.info("FLOW METER")
                flowmeter = await controller.watering.flowmeter()
                _LOGGER.info(flowmeter)

        except RainMachineError as err:
            print(err)


asyncio.run(main())
