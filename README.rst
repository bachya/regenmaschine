💧 Regenmaschine: A Simple Python Library for RainMachine™
=======================================================

.. image:: https://travis-ci.org/bachya/regenmaschine.svg?branch=master
  :target: https://travis-ci.org/bachya/regenmaschine

.. image:: https://img.shields.io/pypi/v/regenmaschine.svg
  :target: https://pypi.python.org/pypi/regenmaschine

.. image:: https://img.shields.io/pypi/pyversions/Regenmaschine.svg
  :target: https://pypi.python.org/pypi/regenmaschine

.. image:: https://img.shields.io/pypi/l/Regenmaschine.svg
  :target: https://pypi.python.org/pypi/regenmaschine

.. image:: https://codecov.io/gh/bachya/regenmaschine/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bachya/regenmaschine

.. image:: https://img.shields.io/codeclimate/github/bachya/regenmaschine.svg
  :target: https://codeclimate.com/github/bachya/regenmaschine

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
  :target: https://saythanks.io/to/bachya

Regenmaschine (German for "rain machine") is a simple, clean, well-tested Python
library for interacting with `RainMachine™ smart sprinkler controllers
<http://www.rainmachine.com/>`_. It gives developers an easy API to manage their
controllers over a LAN or via RainMachine™'s cloud.

💧 Installation
===============

.. code-block:: bash

  $ pip install regenmaschine

💧 Usage
========

Authentication & Creating a Client
----------------------------------

Authentication is the first step and can be done against the local device or the
cloud API:

.. code-block:: python

  import regenmaschine as rm

  # Authenticate against the local device or the remote API:
  auth = rm.Authenticator.create_local('192.168.1.100', 'MY_RM_PASSWORD')
  auth = rm.Authenticator.create_remote('EMAIL_ADDRESS', 'MY_RM_PASSWORD')

  # Then, create a client:
  client = rm.Client(auth)

Diagnostics
-----------

More info on response formats, etc.:
`<http://docs.rainmachine.apiary.io/#reference/diagnostics>`_

.. code-block:: python

  client.diagnostics.current() # Returns current diagnostic info
  client.diagnostics.log()     # Returns entire device log

Programs
--------

More info on response formats, etc.:
`<http://docs.rainmachine.apiary.io/#reference/programs>`_

.. code-block:: python

  client.programs.all()     # Returns info on all programs
  client.programs.get(1)    # Returns info about program with UID of 1
  client.programs.next()    # Returns the next run date/time for all programs
  client.programs.running() # Returns all running programs
  client.programs.start(7)  # Starts program 7
  client.programs.stop(7)   # Stops program 7

Restrictions
------------

More info on response formats, etc.:
`<http://docs.rainmachine.apiary.io/#reference/restrictions>`_

.. code-block:: python

  client.restrictions.current()   # Returns currently active restrictions
  client.restrictions.hourly()    # Returns restrictions over the next hour
  client.restrictions.raindelay() # Returns all rain-related restrictions
  client.restrictions.universal() # Returns the global list of restrictions

Stats
-----

More info on response formats, etc.:
`<http://docs.rainmachine.apiary.io/#reference/daily-stats>`_

.. code-block:: python

  client.stats.on_date('6/29/2017')           # Returns all stats for a date
  client.stats.on_date('2017-06-29')          # Returns all stats for a date
  client.stats.on_date('1 week ago')          # Returns all stats for a date
  client.stats.upcoming()                     # Returns expected stats for the next 7 days
  client.stats.upcoming(include_details=True) # Deeper look at the next 7 days

Watering
--------

More info on response formats, etc.:
`<http://docs.rainmachine.apiary.io/#reference/watering>`_

.. code-block:: python

  client.watering.log()                             # Returns log of all watering activities
  client.watering.log(details=True)                 # Returns full log of all watering activities
  client.watering.log('6/29/2017', 2, details=True) # Returns log for 6/27-6/29
  client.watering.log('2017-06-29', 2)              # Returns log for 6/27-6/29
  client.watering.log('2017-06-29', 2)              # Returns full log for 6/27-6/29
  client.watering.log('2 days ago', 3)              # Returns log 2-5 days ago

  client.watering.queue()                            # Returns the active queue of watering activities
  client.watering.runs('6/29/2017', 2)               # Alternate view of log()
  client.watering.runs('2017-06-29', 2)              # Alternate view of log()
  client.watering.runs('2 days ago', 3)              # Alternate view of log()
  client.watering.stop_all()                         # Immediately stops all programs and zones

Weather Services
----------------

More info on response formats, etc.:
`<http://docs.rainmachine.apiary.io/#reference/weather-services>`_

.. code-block:: python

  client.parsers.current() # Returns current weather services being used

Zones
-----

More info on response formats, etc.:
`<http://docs.rainmachine.apiary.io/#reference/zones>`_

.. code-block:: python

  client.zones.all()                   # Returns all zone info
  client.zones.all(properties=True)    # Returns advanced info for all zones
  client.zones.get(2)                  # Returns info about a zone with UID of 2
  client.zones.get(2, properties=True) # Returns advanced info about zone 2
  client.zones.start(3, 60)            # Starts zone 3 for 60 seconds
  client.zones.stop(3)                 # Stops zone 3

  # You can also simulate what a zone will do:
  properties = client.zones.get(2, properties=True)
  client.zones.simulate(properties)

💧 Exceptions
=============

Regenmaschine may raise any of the following:

* `Built-in Python Exceptions <https://docs.python.org/3/library/exceptions.html#bltin-exceptions>`_
* `Requests Exceptions <https://github.com/requests/requests/blob/master/requests/exceptions.py>`_
* `Regenmaschine Exceptions <https://github.com/bachya/regenmaschine/blob/master/regenmaschine/exceptions.py>`_

One exception to pay particular note of is
:code:`regenmaschine.exceptions.BrokenAPICall`. Unfortunately, there are
currently some API calls that work correctly in the local API, but not the
remote API; as a result, this exception is raised to protect client libraries
appropriately.

Here is the current list of broken API calls:

* :code:`client.programs.start()`: remote API returns an HTTP status of 500
* :code:`client.programs.stop()`: remote API returns an HTTP status of 500

💧 Advanced Usage
=================

Connection Pooling
------------------

If desired, Regenmaschine can accept a session object that allows it to re-use
the same HTTP connection for every call (rather than opening up a new one each
time):

.. code-block:: python

  from requests.sessions import Session
  with Session() as session:
    auth = rm.Authenticator.create_local('192.168.1.100', 'MY_RM_PASSWORD', session)
    client = rm.Client(auth)
    client.zones.all()
    client.zones.get(1)

Authentication Caching
----------------------

There doesn't appear to be a limit on the number of times RainMachine™
will allow new access tokens to be generated. However, it may be desirable to
use the same credentials long term. Therefore, the :code:`auth` object can be
dumped and saved:

.. code-block:: python

  # Outputs a dict:
  auth_json = auth.dump()

  # Outputs a string version of the dict:
  auth_str = auth.dumps()

The :code:`auth` object contains the access token used to authenticate API
requests, as well as an expiration timeframe and more:

.. code-block:: python

  {
    "sprinkler_id": None,
    "cookies": {
      "access_token": "24551da62895"
    },
    "api_url": "https://192.168.1.100:8080/api/4",
    "url": "https://192.168.1.100:8080/api/4",
    "checksum": u "c5e29cdef3b1e",
    "expires_in": 157680000,
    "api_endpoint": "auth/login",
    "access_token": u "24551da62895",
    "verify_ssl": False,
    "session": None,
    "expiration": u "Fri, 01 Jul 2022 20:11:48 GMT",
    "timeout": 10,
    "status_code": 0,
    "using_remote_api": False,
    "data": {
      "pwd": "MY_RM_PASSWORD",
      "remember": 1
    }
  }

**TAKE NOTE:** the dumped :code:`auth` object contains the access token
needed to query the API, sprinkler IDs, RainMachine™ credentials, and other
sensitive information. **Therefore, it should be cached and stored securely**.

One common use of this mechanism would be to check the expiration date of the
access token; assuming it is still valid, a corresponding client can be
recreated quite easily:

.. code-block:: python

  # The dict and the string versions can each be loaded:
  if auth_json['expires_in'] > 1000:
    auth = rm.Authenticator.load(auth_json)
    client = rm.Client(auth)

SSL Usage
---------

By default, Regenmaschine routes all API calls – local or remote – through HTTPS.
However, RainMachine devices use self-signed SSL certificates; therefore,
Regenmaschine disables verifying the validity of local SSL certificates before
processing local requests. In practice, this shouldn't be a problem. However, for the security conscious, this behavior can be changed.

First, `provide a CA-signed SSL certificate to the local device <https://support.rainmachine.com/hc/en-us/community/posts/115006512067-rovide-custom-SSL-Certificate>`_. Then, override the default local Authenticator behavior:

.. code-block:: python

  # Create a local Authenticator and force it to use SSL:
  auth = rm.Authenticator.create_local('192.168.1.100', 'MY_RM_PASSWORD')
  auth.verify_ssl = True

  # The client will now verify the SSL certificate on the local device before
  # processing every request:
  client = rm.Client(auth)

*Note:* after this, if Regenmaschine cannot recognize a CA-signed certificate
when querying the local device, a :code:`requests.exceptions.SSLError`
exception will be raised.

To disable SSL once again, re-authenticate and re-create a client:

.. code-block:: python

  # Create a local Authenticator (with the default behavior):
  auth = rm.Authenticator.create_local('<DEVICE_IP_ADDRESS>', '<PASSWORD>')

  # The client will now refrain from verifying the SSL connection's validity:
  client = rm.Client(auth)

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
