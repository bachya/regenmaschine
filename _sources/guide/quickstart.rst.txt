Quickstart
==========

Regenmaschine aims to be easy in both setup and usage. Here's how to get started.

Authentication
--------------

Authentication is the first step and can be done against the local device or the
cloud API:

.. code-block:: python

  import regenmaschine as rm

  # Authenticate against the local device or the remote API:

  auth = rm.Authenticator.create_local('192.168.1.100', 'password', port=8080, https=True)
  auth = rm.Authenticator.create_remote('email@host.com', 'password')

Note that if your RainMachine uses a port other than 8080 (the default on newer
units), you can use the optional :code:`port` parameter to change it when
creating a local Authenticator. You can also enable/disable HTTPS depending on
your needs via the optional :code:`https` parameter.

This :code:`Authenticator` object can then be used to instantiate a
Regenmaschine :code:`Client`:

.. code-block:: python

  client = rm.Client(auth)

It's important to note that once instantiated, the :code:`Client` only knows
about the device/service against which it was authenticated. Put simply, if
you create a "local :code:`Client`" and later want a "remote :code:`Client`,"
you'll need to re-authenticate and re-create the :code:`Client`.

Programs
--------

RainMachine™ :code:`programs` are collections of zone actions grouped together.
For complete information on the response formats for program operations, check
out the official RainMachine™ API docs:
`<http://docs.rainmachine.apiary.io/#reference/programs>`_

In terms of retrieving program information, Regenmaschine offers several
methods. To retrieve information on all programs:

.. code-block:: python

  client.programs.all()
  # >>> {u'programs': [{u'startDate': u'2017-07-01',}] ... }

To retrieve information on a specific program (in this case, program #6):

.. code-block:: python

  client.programs.get(6)
  # >>> {u'status': 0, u'ignoreInternetWeather': False, ... }

To retrieve the next run date/time for all programs:

.. code-block:: python

  client.programs.next()
  # >>> {u'nextRuns': [{u'pid': 3, u'startTime': u'06:00'}, ] ... }

To retrieve all running programs:

.. code-block:: python

  client.programs.running()
  # >>> {u'programs': [{u'startDate': u'2017-07-01',}] ... }

Regenmaschine also offers two methods to spur programs into (in)action. To
start program #7:

.. code-block:: python

  client.programs.start(7)
  # >>> {u'message': u'OK', u'statusCode': 0}

...and to stop it:

.. code-block:: python

  client.programs.stop(7)
  # >>> {u'message': u'OK', u'statusCode': 0}

Zones
-----

RainMachine™ :code:`zones` are physical locations where watering occurs. For
complete information on the response formats for zone operations, check out
the official RainMachine™ API docs:
`<http://docs.rainmachine.apiary.io/#reference/zones>`_

As with programs, Regenmaschine offers several retrieval methods for zone
information. To retrieve information on all zones:

.. code-block:: python

  client.zones.all()
  # >>> { "zones": [ { "uid": 1, "name": "Backyard Landscaping",}] ... }

To retrieve even more detailed information about all zones, simply set the
:code:`properties` parameter to :code:`True` before running:

.. code-block:: python

  client.zones.all(properties=True)
  # >>> { "zones": [ { "uid": 1, "name": "Backyard Landscaping", ] ... }

To retrieve information about a specific zone (in this case, zone #2):

.. code-block:: python

  client.zones.get(2)
  # >>> { "uid": 1, "name": "Backyard Landscaping", "state": 0, ... }

Once again, detailed information about a zone can be retrieved by setting the
:code:`properties` parameter to :code:`True` before running:

.. code-block:: python

  client.zones.get(2, properties=True)
  # >>> { "uid": 1, "name": "Backyard Landscaping", "valveid": 1, ... }

As with programs, zones can also be started and stopped from Regenmaschine. To
start zone 3 for 60 seconds:

.. code-block:: python

  client.zones.start(3, 60)
  # >>> { "statusCode": 0, "message": "OK" }

...and to stop it:

.. code-block:: python

  client.zones.stop(3)
  # >>> { "statusCode": 0, "message": "OK" }

Regenmaschine also can return a "simulated run" for zones, which provivdes an
understanding of what a specific zone will do when run next. To do this:

.. code-block:: python

  # Get the complete properties of the zone we want to simulate:
  properties = client.zones.get(2, properties=True)

  client.zones.simulate(properties)
  # >>> { "referenceTime": 1243, "currentFieldCapacity": 30.92 }

Watering
--------

The :code:`watering` component of Regenmaschine provides some comprehensive
data and operations for programs *and* zones. For complete information on the
response formats for zone operations, check out the official RainMachine™ API
docs:
`<http://docs.rainmachine.apiary.io/#reference/watering>`_

To return the log of all recent watering activities:

.. code-block:: python

  client.watering.log()
  # >>> { "waterLog": { "days": [ { "date": "2017-06-29", } ] } ... }

An even more detailed log can be retrieved by setting the :code:`details`
parameter to :code:`True` before running:

.. code-block:: python

  client.watering.log(details=True)
  # >>> { "waterLog": { "days": [ { "date": "2017-07-07",  } ] } ... }

Regenmaschine can retrieve log entries for specific days (with the starting
date being any normal, acceptable date format); furthermore, the trusty
:code:`details` parameter can be included or removed at will:

.. code-block:: python

  # Returns log for 6/27-6/29
  client.watering.log('2017-06-29', 2)

  # Returns detailed log for 6/27-6/29:
  client.watering.log('6/29/2017', 2, details=True)

  # Returns log for 2-5 days ago:
  client.watering.log('2 days ago', 3)

Log-style information can also be retrieved as a series of "runs":

.. code-block:: python

  client.watering.runs('6/29/2017', 2)
  client.watering.runs('2017-06-29', 2)
  client.watering.runs('2 days ago', 3)

To retrieve the active queue of upcoming water activities:

.. code-block:: python

  client.watering.queue()
  # >>> { "queue": [ { "availableWater": 0, "realDuration": 0,}] ... }

Finally, to stop *all* watering activities at once:

.. code-block:: python

  client.watering.stop_all()
  # >>> { "statusCode": 0, "message": "OK" }

Restrictions
------------

RainMachine™ :code:`restrictions` represent reasons that would prevent the
device from completing watering activities. For complete information on the
response formats for restriction operations, check out the official RainMachine™
API docs:
`<http://docs.rainmachine.apiary.io/#reference/restrictions>`_

To retrieve currently active restrictions:

.. code-block:: python

  client.restrictions.current()
  # >>> { "hourly": false, "freeze": false, "month": false, ... }

To retrieve restrictions that will be active over the next hour:

.. code-block:: python

  client.restrictions.hourly()
  # >>> { "hourlyRestrictions": [] }

To retrieve all temporary restrictions due to a rain delay:

.. code-block:: python

  client.restrictions.raindelay()
  # >>> { "delayCounter": -1 }

To retrieve all global (always-active) restrictions:

.. code-block:: python

  client.restrictions.universal()
  # >>> { "hotDaysExtraWatering": false, "freezeProtectEnabled": false, ... }

Weather Services
----------------

Weather services (referred to by RainMachine™ as :code:`parsers`) represent
the weather services actively in use by the device. For complete information
on the response formats for parser operations, check out the official
RainMachine™ API docs:
`<http://docs.rainmachine.apiary.io/#reference/weather-services>`_

To retrieve a list of all current, actively-used weather services:

.. code-block:: python

  client.parsers.current()
  # >>> { "parsers": [ { "lastRun": null, "lastKnownError": "", } ] ... }

Stats
-----

RainMachine™ :code:`stats` are statistics on device usage, etc. For complete
information on the response formats for stat operations, check out the
official RainMachine™ API docs:
`<http://docs.rainmachine.apiary.io/#reference/daily-stats>`_

To retrieve the expected statistics for the next 7 days:

.. code-block:: python

  client.stats.upcoming()
  # >>> { "DailyStats": [ { "id": 0, "day": "2017-06-27", "mint": 14,}] ... }

More detailed statistics can be retrieved by setting the :code:`include_details`
parameter to :code:`True`:

.. code-block:: python

  client.stats.upcoming(include_details=True)
  # >>> { "DailyStatsDetails": [ { "dayTimestamp": 1498543200,  } ] ... }

It is also possible to get statistics for a date (in any reasonable format).
If a date in the past is given, actual statistics will be returned; dates in the
future will return expected statistics:

.. code-block:: python

  client.stats.on_date('6/29/2017')
  client.stats.on_date('2017-06-29')
  client.stats.on_date('1 week ago')
  # >>> { "id": -10, "day": "2017-06-27", "mint": 17.94, ... }

Provision Info
--------------

RainMachine™ provides :code:`provision` info for every device; contained within
is device information, such as device name, network information, and more. For
information on the response formats for diagnostic operations, check out the
official RainMachine™ API docs:
`<http://docs.rainmachine.apiary.io/#reference/provision>`_

To retrieve the device name:

.. code-block:: python

  client.provision.device_name()
  # >>> { "name": "Home" }

To retrieve all device settings:

.. code-block:: python

  client.diagnostics.settings()
  # >>> { "system": { "httpenabled": true, "rainsensorsnoozeduration":  } ... }

To retrieve wifi information:

.. code-block:: python

  client.diagnostics.wifi()
  # >>> { "macAddress": "00:00:00:00:00:00", "ssid": "My Wifi", ... }

Diagnostics
-----------

RainMachine™ :code:`diagnostics` are exactly what they sound like! For complete
information on the response formats for diagnostic operations, check out the
official RainMachine™ API docs:
`<http://docs.rainmachine.apiary.io/#reference/diagnostics>`_

To retrieve current diagnostic information:

.. code-block:: python

  client.diagnostics.current()
  # >>> { "hasWifi": true, "uptime": "18 days, 16:16:48", ... }

To retrieve the entire device log:

.. code-block:: python

  client.diagnostics.log()
  # >>> { "log": "--------------------------- GENERAL RAINMACHINE LOG -- ... }
