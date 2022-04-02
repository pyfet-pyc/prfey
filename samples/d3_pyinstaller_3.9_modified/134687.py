# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: keyring\util\properties.py
from collections import abc

class ClassProperty(property):
    __doc__ = "\n    An implementation of a property callable on a class. Used to decorate a\n    classmethod but to then treat it like a property.\n\n    Example:\n\n    >>> class MyClass:\n    ...    @ClassProperty\n    ...    @classmethod\n    ...    def skillz(cls):\n    ...        return cls.__name__.startswith('My')\n    >>> MyClass.skillz\n    True\n    >>> class YourClass(MyClass): pass\n    >>> YourClass.skillz\n    False\n    "

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class NonDataProperty:
    __doc__ = 'Much like the property builtin, but only implements __get__,\n    making it a non-data property, and can be subsequently reset.\n\n    See http://users.rcn.com/python/download/Descriptor.htm for more\n    information.\n\n    >>> class X:\n    ...   @NonDataProperty\n    ...   def foo(self):\n    ...     return 3\n    >>> x = X()\n    >>> x.foo\n    3\n    >>> x.foo = 4\n    >>> x.foo\n    4\n    '

    def __init__--- This code section failed: ---

 L.  50         0  LOAD_FAST                'fget'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'fget cannot be none'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  51        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'fget'
               20  LOAD_GLOBAL              abc
               22  LOAD_ATTR                Callable
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_TRUE     36  'to 36'
               28  <74>             
               30  LOAD_STR                 'fget must be callable'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L.  52        36  LOAD_FAST                'fget'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               fget

Parse error at or near `None' instruction at offset -1

    def __get__--- This code section failed: ---

 L.  55         0  LOAD_FAST                'obj'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  56         8  LOAD_FAST                'self'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  57        12  LOAD_FAST                'self'
               14  LOAD_METHOD              fget
               16  LOAD_FAST                'obj'
               18  CALL_METHOD_1         1  ''
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1