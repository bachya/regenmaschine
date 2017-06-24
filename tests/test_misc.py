"""
File: test_misc.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine.__version__ as v

def test_version():
    """ Test that we have a version """
    assert v.__version__ is not None
