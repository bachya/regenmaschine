"""
File: test_regenmaschine.py
Author: Aaron Bach
Email: bachya1208@gmail.com
Github: https://github.com/bachya/regenmaschine
Description:
"""

import pytest
import responses

import regenmaschine


def test_local_authentication(mocker):
    """Local client auth test"""

# def test_spy(mocker):
#     class Foo(object):
#         def bar(self):
#             return 42

#     foo = Foo()
#     mocker.spy(foo, 'bar')
#     assert foo.bar() == 42
#     assert foo.bar.call_count == 1
