"""
File: test_misc.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
"""

# -*- coding: utf-8 -*-

import regenmaschine

def test_version():
    """ Test that we have a version """
    assert regenmaschine.__author__ != ''
    assert regenmaschine.__author_email__ != ''
    assert regenmaschine.__copyright__ != ''
    assert regenmaschine.__description__ != ''
    assert regenmaschine.__license__ != ''
    assert regenmaschine.__title__ != ''
    assert regenmaschine.__url__ != ''
    assert regenmaschine.__version__ != ''
