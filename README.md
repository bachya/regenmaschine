# 💧 Regenmaschine: A Simple Python Library for RainMachine™

[![CI](https://github.com/bachya/regenmaschine/workflows/CI/badge.svg)](https://github.com/bachya/regenmaschine/actions)
[![PyPi](https://img.shields.io/pypi/v/regenmaschine.svg)](https://pypi.python.org/pypi/regenmaschine)
[![Version](https://img.shields.io/pypi/pyversions/regenmaschine.svg)](https://pypi.python.org/pypi/regenmaschine)
[![License](https://img.shields.io/pypi/l/regenmaschine.svg)](https://github.com/bachya/regenmaschine/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/regenmaschine/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/regenmaschine)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/bachya/regenmaschine/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`regenmaschine` (German for "rain machine") is a simple, clean, well-tested
Python library for interacting with
[RainMachine™ smart sprinkler controllers](http://www.rainmachine.com/).
It gives developers an easy API to manage their controllers over their local
LAN or remotely via the RainMachine™ cloud.

# Python Versions

`regenmaschine` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8

# Installation

```python
pip install regenmaschine
```

# Example

`regenmaschine` starts within an
[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:

```python
import asyncio

from aiohttp import ClientSession

from regenmaschine import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        # YOUR CODE HERE...


asyncio.get_event_loop().run_until_complete(main())
```

Creating a `regenmaschine` `Client` might be the easiest thing you do all day:

```python
import asyncio

from aiohttp import ClientSession

from regenmaschine import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        client = Client(websession)


asyncio.get_event_loop().run_until_complete(main())
```

Once you have a client, you can load a local controller (i.e., one that is
accessible over the LAN) very easily:

```python
import asyncio

from aiohttp import ClientSession

from regenmaschine import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        client = Client(websession)

        await client.load_local("192.168.1.101", "my_password", port=8080, ssl=True)

        controllers = client.controllers
        # >>> {'ab:cd:ef:12:34:56': <LocalController>}


asyncio.get_event_loop().run_until_complete(main())
```

If you have 1, 2 or 100 other local controllers, you can load them in the same
way – `client.controllers` will keep your controllers all organized.

What if you have controllers around the world and can't access them all over
the same local network? No problem! `regenmaschine` allows you to load remote
controllers very easily, as well:

```python
import asyncio

from aiohttp import ClientSession

from regenmaschine import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        client = Client(websession)

        await client.load_remote("rainmachine_email@host.com", "my_password")

        controllers = client.controllers
        # >>> {'xx:xx:xx:xx:xx:xx': <RemoteController>, ...}


asyncio.get_event_loop().run_until_complete(main())
```

Bonus tip: `client.load_remote` will load _all_ controllers owned by that email
address.

Regardless of the type of controller you have loaded (local or remote), the
same properties and methods are available to each:

```python
import asyncio
import datetime

from aiohttp import ClientSession

from regenmaschine import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        client = Client(websession)

        # Load a local controller:
        await client.load_local("192.168.1.101", "my_password", port=8080, ssl=True)

        # Load all remote controllers associated with an account:
        await client.load_remote("rainmachine_email@host.com", "my_password")

        # They all act the same! The only difference is that remote API calls
        # will pass through the RainMachine™ cloud:
        for mac_address, controller in client.controllers:
            # Print some client properties:
            print(f"Name: {controller.name}")
            print(f"Host: {controller.host}")
            print(f"MAC Address: {controller.mac}")
            print(f"API Version: {controller.api_version}")
            print(f"Software Version: {controller.software_version}")
            print(f"Hardware Version: {controller.hardware_version}")

            # Get all diagnostic information:
            diagnostics = await controller.diagnostics.current()

            # Get all weather parsers:
            parsers = await controller.parsers.current()

            # Get all programs:
            programs = await controller.programs.all()

            # Include inactive programs:
            programs = await controller.programs.all(include_inactive=True)

            # Get a specific program:
            program_1 = await controller.programs.get(1)

            # Enable or disable a specific program:
            await controller.programs.enable(1)
            await controller.programs.disable(1)

            # Get the next run time for all programs:
            runs = await controller.programs.next()

            # Get all running programs:
            programs = await controller.programs.running()

            # Start and stop a program:
            await controller.programs.start(1)
            await controller.programs.stop(1)

            # Get basic details about all zones:
            zones = await controller.zones.all()

            # Get advanced details about all zones:
            zones = await controller.zones.all(details=True)

            # Include inactive zones:
            zones = await controller.zones.all(include_inactive=True)

            # Get basic details about a specific zone:
            zone_1 = await controller.zones.get(1)

            # Get advanced details about a specific zone:
            zone_1 = await controller.zones.get(1, details=True)

            # Enable or disable a specific zone:
            await controller.zones.enable(1)
            await controller.zones.disable(1)

            # Start a zone for 60 seconds:
            await controller.zones.start(1, 60)

            # ...and stop it:
            await controller.zones.stop(1)

            # Get the device name:
            name = await controller.provisioning.device_name

            # Get all provisioning settings:
            settings = await controller.provisioning.settings()

            # Get all networking info related to the device:
            wifi = await controller.provisioning.wifi()

            # Get various types of active watering restrictions:
            current = await controller.restrictions.current()
            universal = await controller.restrictions.universal()
            hourly = await controller.restrictions.hourly()
            raindelay = await controller.restrictions.raindelay()

            # Get watering stats:
            today = await controller.stats.on_date(datetime.date.today())
            upcoming_days = await controller.stats.upcoming(details=True)

            # Get info on various watering activities not already covered:
            log = await controller.watering.log(datetime.date.today(), 2)
            queue = await controller.watering.queue()
            runs = await controller.watering.runs(datetime.date.today())

            # Pause all watering activities for 30 seconds:
            await controller.watering.pause_all(30)

            # Unpause all watering activities:
            await controller.watering.unpause_all()

            # Stop all watering activities:
            await controller.watering.stop_all()


asyncio.get_event_loop().run_until_complete(main())
```

Check out `example.py`, the tests, and the source files themselves for method
signatures and more examples.

# Loading Controllers Multiple Times

It is technically possible to load a controller multiple times. Let's pretend
for a moment that:

* We have a local controller named `Home` (available at `192.168.1.101`).
* We have a remote controller named `Grandma's House`.
* Both controllers live under our email address: `user@host.com`

If we load them thus:

```python
import asyncio

from aiohttp import ClientSession

from regenmaschine import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        client = Client(websession)

        # Load "Home" locally:
        await client.load_local("192.168.1.101", "my_password")

        # Load all of my controllers remotely:
        await client.load_remote("user@host.com", "my_password")


asyncio.get_event_loop().run_until_complete(main())
```

...then we will have the following:

1. `Home` will be a `LocalController` and accessible over the LAN.
2. `Grandma's House` will be a `RemoteController` and accessible only over the
RainMachine™ cloud.

Notice that `regenmaschine` is smart enough to not overwrite a controller that
already exists: even though `Home` exists as a remote controller owned by
`user@host.com`, it had already been loaded locally. By default,
`regenmaschine` will only load a controller if it hasn't been loaded before
(locally _or_ remotely). If you want to change this behavior, both `load_local`
and `load_remote` accept an optional `skip_existing` parameter:

```python
import asyncio

from aiohttp import ClientSession

from regenmaschine import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        client = Client(websession)

        # Load all of my controllers remotely:
        await client.load_remote("user@host.com", "my_password")

        # Load "Home" locally, overwriting the existing remote controller:
        await client.load_local("192.168.1.101", "my_password", skip_existing=False)


asyncio.get_event_loop().run_until_complete(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/regenmaschine/issues)
  or [initiate a discussion on one](https://github.com/bachya/regenmaschine/issues/new).
2. [Fork the repository](https://github.com/bachya/regenmaschine/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
