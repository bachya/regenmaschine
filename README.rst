Regenmaschine: A Simple Python Library for RainMachine™
=======================================================

.. image:: https://img.shields.io/pypi/v/regenmaschine.svg
  :target: https://pypi.python.org/pypi/regenmaschine

.. image:: https://travis-ci.org/bachya/regenmaschine.svg?branch=master
  :target: https://travis-ci.org/bachya/regenmaschine

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
  :target: https://saythanks.io/to/bachya

Regenmaschine (German for "rain machine") is a simple, clean, well-tested Python
library for interacting with `RainMachine smart sprinkler controllers
<http://www.rainmachine.com/>`_. It gives developers an easy API to manage their
controllers over a LAN or via RainMachine's cloud API.

💧 Installation
===============
.. code-block:: bash

  $ pip install regenmaschine

💧 Usage
========

Authentication
--------------

First, we need to authenticate. Authentication can be done against the local
device or the cloud API:

.. code-block:: python

  import regenmaschine as rm

  # Using the local API:
  auth = rm.Authenticator.create_local('<DEVICE_IP_ADDRESS>', '<PASSWORD>')

  # Using the remote API:
  auth = rm.Authenticator.create_remote('<EMAIL ADDRESS>', '<PASSWORD>')

If authentication is successful, this :code:`auth` object can then be used to
create a client:

.. code-block:: python

  client = rm.Client(auth)

Programs
--------

.. code-block:: python

  client.programs.all()             # Returns all program information
  client.programs.get(<program_id>) # Returns info about a single program
  client.programs.next()            # Returns the next run date/time for all programs

Authentication Caching
----------------------

Although there doesn't appear to be a limit to the number of times RainMachine
will allow authentication to occur, for speed/efficiency, it is often desirable
to use the same credentials long-term. The :code:`auth` object can be dumped
and saved in any number of manners:

.. code-block:: python

  # Outputs a dict:
  auth_json = auth.dump()

  # Outputs a string version of the dict:
  auth_str = auth.dumps()

At any point, this authentication can be loaded back into a Regenmaschine
client:

.. code-block:: python

  # Outputs a dict:
  auth.load(auth_json)

  # Outputs a string version of the dict:
  auth.loads(auth_str)

*Beware:* the dumped :code:`auth` object contains the access token needed to
query the API, as well as the information needed to reconstruct the client.
Therefore, it should be cached and stored securely.
