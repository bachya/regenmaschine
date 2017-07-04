.. Regenmaschine documentation master file, created by
   sphinx-quickstart on Mon Jul  3 16:48:32 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Regenmaschine: A Simple Python Library for RainMachine™
=======================================================

Release v\ |version|

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

The Main Features
-----------------

- Query the local device - no internet needed!
- Query the remote RainMachine™ API
- Manage, view, and control programs and zones
- View useful info (watering restrictions, stats, weather information, etc.)
- Retrieve diagnostics from the local device
- Pool HTTP connections
- Easy authentication caching
- and more!

The Guide
---------

.. toctree::
   :maxdepth: 2

   guide/installation
   guide/quickstart

