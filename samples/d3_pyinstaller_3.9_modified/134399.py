# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: attr\_next_gen.py
"""
These are Python 3.6+-only and keyword-only APIs that call `attr.s` and
`attr.ib` with different default values.
"""
from functools import partial
from attr.exceptions import UnannotatedAttributeError
from . import setters
from ._make import NOTHING, _frozen_setattrs, attrib, attrs

def define--- This code section failed: ---

 L.  53         0  LOAD_CLOSURE             'auto_detect'
                2  LOAD_CLOSURE             'auto_exc'
                4  LOAD_CLOSURE             'cache_hash'
                6  LOAD_CLOSURE             'eq'
                8  LOAD_CLOSURE             'field_transformer'
               10  LOAD_CLOSURE             'frozen'
               12  LOAD_CLOSURE             'getstate_setstate'
               14  LOAD_CLOSURE             'hash'
               16  LOAD_CLOSURE             'init'
               18  LOAD_CLOSURE             'kw_only'
               20  LOAD_CLOSURE             'on_setattr'
               22  LOAD_CLOSURE             'order'
               24  LOAD_CLOSURE             'repr'
               26  LOAD_CLOSURE             'slots'
               28  LOAD_CLOSURE             'str'
               30  LOAD_CLOSURE             'these'
               32  LOAD_CLOSURE             'weakref_slot'
               34  BUILD_TUPLE_17       17 
               36  LOAD_CODE                <code_object do_it>
               38  LOAD_STR                 'define.<locals>.do_it'
               40  MAKE_FUNCTION_8          'closure'
               42  STORE_DEREF              'do_it'

 L.  77        44  LOAD_CLOSURE             'auto_attribs'
               46  LOAD_CLOSURE             'do_it'
               48  LOAD_CLOSURE             'frozen'
               50  LOAD_CLOSURE             'on_setattr'
               52  BUILD_TUPLE_4         4 
               54  LOAD_CODE                <code_object wrap>
               56  LOAD_STR                 'define.<locals>.wrap'
               58  MAKE_FUNCTION_8          'closure'
               60  STORE_FAST               'wrap'

 L. 114        62  LOAD_FAST                'maybe_cls'
               64  LOAD_CONST               None
               66  <117>                 0  ''
               68  POP_JUMP_IF_FALSE    74  'to 74'

 L. 115        70  LOAD_FAST                'wrap'
               72  RETURN_VALUE     
             74_0  COME_FROM            68  '68'

 L. 117        74  LOAD_FAST                'wrap'
               76  LOAD_FAST                'maybe_cls'
               78  CALL_FUNCTION_1       1  ''
               80  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 66


mutable = define
frozen = partial(define, frozen=True, on_setattr=None)

def field(*, default=NOTHING, validator=None, repr=True, hash=None, init=True, metadata=None, converter=None, factory=None, kw_only=False, eq=None, order=None, on_setattr=None):
    """
    Identical to `attr.ib`, except keyword-only and with some arguments
    removed.

    .. versionadded:: 20.1.0
    """
    return attrib(default=default,
      validator=validator,
      repr=repr,
      hash=hash,
      init=init,
      metadata=metadata,
      converter=converter,
      factory=factory,
      kw_only=kw_only,
      eq=eq,
      order=order,
      on_setattr=on_setattr)