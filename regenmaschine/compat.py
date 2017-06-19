# -*- coding: utf-8 -*-

"""
File: compat.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
Description: This module handles import compatibility issues between Python 2 and
Python 3. Lovingly borroed from Kenneth Reitzr
(https://raw.githubusercontent.com/kennethreitz/maya/master/maya/compat.py)
"""

import sys

# Syntax sugar.
_VER = sys.version_info

#: Python 2.x?
IS_PY2 = (_VER[0] == 2)

#: Python 3.x?
IS_PY3 = (_VER[0] == 3)

if IS_PY2:
    cmp = cmp # pylint: disable=invalid-name, undefined-variable

elif IS_PY3:
    def cmp(a, b): # pylint: disable=invalid-name
        """
        Compare two objects.
        Returns a negative number if C{a < b}, zero if they are equal, and a
        positive number if C{a > b}.
        """
        if a < b:
            return -1
        if a == b:
            return 0
        return 1


def comparable(klass):
    """
    Class decorator that ensures support for the special C{__cmp__} method.
    On Python 2 this does nothing.
    On Python 3, C{__eq__}, C{__lt__}, etc. methods are added to the class,
    relying on C{__cmp__} to implement their comparisons.
    """
    # On Python 2, __cmp__ will just work, so no need to add extra methods:
    if not IS_PY3:
        return klass

    def __eq__(self, other):
        c = self.__cmp__(other) # pylint: disable=invalid-name
        if c is NotImplemented:
            return c
        return c == 0

    def __ne__(self, other):
        c = self.__cmp__(other) # pylint: disable=invalid-name
        if c is NotImplemented:
            return c
        return c != 0

    def __lt__(self, other):
        c = self.__cmp__(other) # pylint: disable=invalid-name
        if c is NotImplemented:
            return c
        return c < 0

    def __le__(self, other):
        c = self.__cmp__(other) # pylint: disable=invalid-name
        if c is NotImplemented:
            return c
        return c <= 0

    def __gt__(self, other):
        c = self.__cmp__(other) # pylint: disable=invalid-name
        if c is NotImplemented:
            return c
        return c > 0

    def __ge__(self, other):
        c = self.__cmp__(other) # pylint: disable=invalid-name
        if c is NotImplemented:
            return c
        return c >= 0

    klass.__lt__ = __lt__
    klass.__gt__ = __gt__
    klass.__le__ = __le__
    klass.__ge__ = __ge__
    klass.__eq__ = __eq__
    klass.__ne__ = __ne__
    return klass
