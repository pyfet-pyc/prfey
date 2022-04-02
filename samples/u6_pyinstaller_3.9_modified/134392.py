# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: attr\setters.py
"""
Commonly used hooks for on_setattr.
"""
from __future__ import absolute_import, division, print_function
from . import _config
from .exceptions import FrozenAttributeError

def pipe(*setters):
    """
    Run all *setters* and return the return value of the last one.

    .. versionadded:: 20.1.0
    """

    def wrapped_pipe(instance, attrib, new_value):
        rv = new_value
        for setter in setters:
            rv = setter(instance, attrib, rv)
        else:
            return rv

    return wrapped_pipe


def frozen(_, __, ___):
    """
    Prevent an attribute to be modified.

    .. versionadded:: 20.1.0
    """
    raise FrozenAttributeError()


def validate--- This code section failed: ---

 L.  44         0  LOAD_GLOBAL              _config
                2  LOAD_ATTR                _run_validators
                4  LOAD_CONST               False
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  45        10  LOAD_FAST                'new_value'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  47        14  LOAD_FAST                'attrib'
               16  LOAD_ATTR                validator
               18  STORE_FAST               'v'

 L.  48        20  LOAD_FAST                'v'
               22  POP_JUMP_IF_TRUE     28  'to 28'

 L.  49        24  LOAD_FAST                'new_value'
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L.  51        28  LOAD_FAST                'v'
               30  LOAD_FAST                'instance'
               32  LOAD_FAST                'attrib'
               34  LOAD_FAST                'new_value'
               36  CALL_FUNCTION_3       3  ''
               38  POP_TOP          

 L.  53        40  LOAD_FAST                'new_value'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def convert(instance, attrib, new_value):
    """
    Run *attrib*'s converter -- if it has one --  on *new_value* and return the
    result.

    .. versionadded:: 20.1.0
    """
    c = attrib.converter
    if c:
        return c(new_value)
    return new_value


NO_OP = object()