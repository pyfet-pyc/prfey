# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: attr\filters.py
"""
Commonly useful filters for `attr.asdict`.
"""
from __future__ import absolute_import, division, print_function
from ._compat import isclass
from ._make import Attribute

def _split_what(what):
    """
    Returns a tuple of `frozenset`s of classes and attributes.
    """
    return (
     frozenset((cls for cls in what if isclass(cls))),
     frozenset((cls for cls in what if isinstance(cls, Attribute))))


def include(*what):
    r"""
    Whitelist *what*.

    :param what: What to whitelist.
    :type what: `list` of `type` or `attr.Attribute`\ s

    :rtype: `callable`
    """
    cls, attrs = _split_what(what)

    def include_--- This code section failed: ---

 L.  33         0  LOAD_FAST                'value'
                2  LOAD_ATTR                __class__
                4  LOAD_DEREF               'cls'
                6  <118>                 0  ''
                8  JUMP_IF_TRUE_OR_POP    16  'to 16'
               10  LOAD_FAST                'attribute'
               12  LOAD_DEREF               'attrs'
               14  <118>                 0  ''
             16_0  COME_FROM             8  '8'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    return include_


def exclude(*what):
    r"""
    Blacklist *what*.

    :param what: What to blacklist.
    :type what: `list` of classes or `attr.Attribute`\ s.

    :rtype: `callable`
    """
    cls, attrs = _split_what(what)

    def exclude_--- This code section failed: ---

 L.  50         0  LOAD_FAST                'value'
                2  LOAD_ATTR                __class__
                4  LOAD_DEREF               'cls'
                6  <118>                 1  ''
                8  JUMP_IF_FALSE_OR_POP    16  'to 16'
               10  LOAD_FAST                'attribute'
               12  LOAD_DEREF               'attrs'
               14  <118>                 1  ''
             16_0  COME_FROM             8  '8'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    return exclude_