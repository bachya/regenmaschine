💧 Regenmaschine: A Simple Python Library for RainMachine™
==========================================================

.. image:: https://travis-ci.org/bachya/regenmaschine.svg?branch=master
  :target: https://travis-ci.org/bachya/regenmaschine

.. image:: https://img.shields.io/pypi/v/regenmaschine.svg
  :target: https://pypi.python.org/pypi/regenmaschine

.. image:: https://img.shields.io/pypi/pyversions/Regenmaschine.svg
  :target: https://pypi.python.org/pypi/regenmaschine

.. image:: https://img.shields.io/pypi/l/Regenmaschine.svg
  :target: https://github.com/bachya/regenmaschine/blob/master/LICENSE

.. image:: https://codecov.io/gh/bachya/regenmaschine/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bachya/regenmaschine

.. image:: https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability
   :target: https://codeclimate.com/github/codeclimate/codeclimate/maintainability
   :alt: Maintainability

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
  :target: https://saythanks.io/to/bachya

Regenmaschine (German for "rain machine") is a simple, clean, well-tested Python
library for interacting with `RainMachine™ smart sprinkler controllers
<http://www.rainmachine.com/>`_. It gives developers an easy API to manage their
controllers over their local LAN.

💧 PLEASE READ: 1.0.0 and Beyond
================================

Version 1.0.0 of Regenmaschine makes several breaking, but necessary changes:

* Moves the underlying library from
  `Requests <http://docs.python-requests.org/en/master/>`_ to
  `aiohttp <https://aiohttp.readthedocs.io/en/stable/>`_
* Changes the entire library to use :code:`asyncio`
* Makes 3.6 the minimum version of Python required

If you wish to continue using the previous, synchronous version of
Regenmaschine, make sure to pin version 0.4.2.

💧 Installation
===============

.. code-block:: bash

  $ pip install regenmaschine

💧 Example
==========

Regenmaschine starts within an
`aiohttp <https://aiohttp.readthedocs.io/en/stable/>`_ :code:`ClientSession`:

.. code-block:: python

  import asyncio

  from aiohttp import ClientSession

  from regenmaschine import Client


  async def main() -> None:
      """Create the aiohttp session and run the example."""
      async with ClientSession() as websession:
          await run(websession)


  async def run(websession):
      """Run."""
      # YOUR CODE HERE

  asyncio.get_event_loop().run_until_complete(main())

A Regenmaschine :code:`Client` can be created manually:

.. code-block:: python

  client = Client('192.168.1.100', websession, port=9999)

...or you can attempt to discover one on your local network:

.. code-block:: python

  from regenmaschine import DiscoveryFailedError, scan

  try:
    client = scan(websession)
  except DiscoveryFailedError:
    print("Couldn't find a valid RainMachine unit via discovery")

Once you have a client, authenticate it by using your RainMachine password:

.. code-block:: python

  await client.authenticate('my_password_123')

You can now get some properties with your authenticated client:

.. code-block:: python

  print('Name: {0}'.format(client.name))
  print('Host: {0}'.format(client.host))
  print('MAC Address: {0}'.format(client.mac))

...and get to work controlling your RainMachine!

.. code-block:: python

  # Get all diagnostic information:
  diagnostics = await client.diagnostics.current()

  # Get all weather parsers:
  parsers = await client.parsers.current():

  # Get all programs:
  programs = await client.programs.all():

  # Get a specific program:
  program_1 = await client.programs.get(1)

  # Get the next run time for all programs:
  runs = await client.programs.next()

  # Get all running programs:
  programs = await client.programs.running()

  # Start and stop a program:
  client.programs.start(1)
  client.programs.stop(1)

  # Get the device name:
  name = await client.provisioning.device_name

  # Get all provisioning settings:
  settings = await client.provisioning.settings()

  # Get all networking info related to the device:
  wifi = await client.provisioning.wifi()

  # Get various types of active watering restrictions:
  current = await client.restrictions.current()
  universal = await client.restrictions.universal()
  hourly = await client.restrictions.hourly():
  raindelay = await client.restrictions.raindelay()

  # Get watering stats:
  today = await client.stats.on_date(date=datetime.date.today())
  upcoming_days = client.stats.upcoming(details=True):

  # Get info on various watering activities not already covered:
  log_2_day = client.watering.log(date=datetime.date.today(), 2):
  queue = await client.watering.queue()
  runs = await client.watering.runs(date=datetime.date.today())

  # Stop all watering activities:
  await client.watering.stop_all()

Check out `example.py`, the tests, and the source files themselves for method
signatures and more examples.

💧 Contributing
===============

#. `Check for open features/bugs <https://github.com/bachya/regenmaschine/issues>`_
   or `initiate a discussion on one <https://github.com/bachya/regenmaschine/issues/new>`_.
#. `Fork the repository <https://github.com/bachya/regenmaschine/fork>`_.
#. Install the dev environment: :code:`make init`.
#. Enter the virtual environment: :code:`pipenv shell`
#. Code your new feature or bug fix.
#. Write a test that covers your new functionality.
#. Run tests: :code:`make test`
#. Build new docs: :code:`make docs`
#. Add yourself to AUTHORS.rst.
#. Submit a pull request!
