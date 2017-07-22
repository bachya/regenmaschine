Advanced Topics
===============

Developers with an interest in Regenmaschine's guts should consume and absorb
all of the topics contained here.

Exceptions
----------

Regenmaschine may raise any of the following:

* `Built-in Python Exceptions <https://docs.python.org/3/library/exceptions.html#bltin-exceptions>`_
* `Regenmaschine Exceptions <https://github.com/bachya/regenmaschine/blob/master/regenmaschine/exceptions.py>`_

One exception to pay particular note of is
:code:`regenmaschine.exceptions.BrokenAPICall`. Unfortunately, there are
currently some API calls that work correctly in the local API, but not the
remote API; as a result, this exception is raised to protect client libraries
appropriately.

Here is the current list of "broken" RainMachine™ API calls:

* :code:`client.programs.start()`: remote API returns an HTTP status of 500
* :code:`client.programs.stop()`: remote API returns an HTTP status of 500

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
sensitive information. *Therefore, it should be cached and stored securely*.

One common use of this mechanism would be to check the expiration date of the
access token; assuming it is still valid, a corresponding client can be
recreated quite easily:

.. code-block:: python

  if auth_json['expires_in'] > 1000:
    auth = rm.Authenticator.load(auth_json)
  else:
    auth = rm.Authenticator.create_local('192.168.1.100', 'password')

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
  auth = rm.Authenticator.create_local('192.168.1.100', 'password')
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
  auth = rm.Authenticator.create_local('192.168.1.100', 'password')

  # The client will now refrain from verifying the SSL connection's validity:
  client = rm.Client(auth)

Connection Pooling
------------------

If desired, Regenmaschine can accept a session object that allows it to re-use
the same HTTP connection for every call (rather than opening up a new one each
time):

.. code-block:: python

  from requests.sessions import Session
  with Session() as session:
    auth = rm.Authenticator.create_local('192.168.1.100', 'password', session)
    client = rm.Client(auth)

    # Each of these calls uses the same HTTP connection:
    client.zones.all()
    client.zones.get(1)
