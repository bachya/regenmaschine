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
  auth = rm.Authenticator.create_local('192.168.1.100', 'MY_RM_PASSWORD')
  auth = rm.Authenticator.create_remote('EMAIL_ADDRESS', 'MY_RM_PASSWORD')

This Authenticator object can then be used to instantiate a Regenmaschine client:

.. code-block:: python

  client = rm.Client(auth)

It's important to note that once instantiated, the client only knows about the
device/service against which it was authenticated. Put simply, if you create a
"local client" and later want a "remote client," you'll need to re-authenticate
and re-create the client.

Client Usage
------------
