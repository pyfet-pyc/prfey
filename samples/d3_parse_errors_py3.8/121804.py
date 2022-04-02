# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: comtypes\patcher.py


class Patch(object):
    __doc__ = '\n    Implements a class decorator suitable for patching an existing class with\n    a new namespace.\n\n    For example, consider this trivial class (that your code doesn\'t own):\n\n    >>> class MyClass:\n    ...     def __init__(self, param):\n    ...         self.param = param\n    ...     def bar(self):\n    ...         print("orig bar")\n\n    To add attributes to MyClass, you can use Patch:\n\n    >>> @Patch(MyClass)\n    ... class JustANamespace:\n    ...     def print_param(self):\n    ...         print(self.param)\n    >>> ob = MyClass(\'foo\')\n    >>> ob.print_param()\n    foo\n\n    The namespace is assigned None, so there\'s no mistaking the purpose\n    >>> JustANamespace\n\n    The patcher will replace the existing methods:\n\n    >>> @Patch(MyClass)\n    ... class SomeNamespace:\n    ...     def bar(self):\n    ...         print("replaced bar")\n    >>> ob = MyClass(\'foo\')\n    >>> ob.bar()\n    replaced bar\n\n    But it will not replace methods if no_replace is indicated.\n\n    >>> @Patch(MyClass)\n    ... class AnotherNamespace:\n    ...     @no_replace\n    ...     def bar(self):\n    ...         print("candy bar")\n    >>> ob = MyClass(\'foo\')\n    >>> ob.bar()\n    replaced bar\n\n    '

    def __init__(self, target):
        self.target = target

    def __call__--- This code section failed: ---

 L.  55         0  LOAD_GLOBAL              list
                2  LOAD_GLOBAL              vars
                4  LOAD_FAST                'patches'
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_METHOD              items
               10  CALL_METHOD_0         0  ''
               12  CALL_FUNCTION_1       1  ''
               14  GET_ITER         
             16_0  COME_FROM            82  '82'
             16_1  COME_FROM            66  '66'
             16_2  COME_FROM            36  '36'
               16  FOR_ITER             84  'to 84'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'name'
               22  STORE_FAST               'value'

 L.  56        24  LOAD_FAST                'name'
               26  LOAD_GLOBAL              vars
               28  LOAD_GLOBAL              ReferenceEmptyClass
               30  CALL_FUNCTION_1       1  ''
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE    38  'to 38'

 L.  57        36  JUMP_BACK            16  'to 16'
             38_0  COME_FROM            34  '34'

 L.  58        38  LOAD_GLOBAL              getattr
               40  LOAD_FAST                'value'
               42  LOAD_STR                 '__no_replace'
               44  LOAD_CONST               False
               46  CALL_FUNCTION_3       3  ''
               48  STORE_FAST               'no_replace'

 L.  59        50  LOAD_FAST                'no_replace'
               52  POP_JUMP_IF_FALSE    68  'to 68'
               54  LOAD_GLOBAL              hasattr
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                target
               60  LOAD_FAST                'name'
               62  CALL_FUNCTION_2       2  ''
               64  POP_JUMP_IF_FALSE    68  'to 68'

 L.  60        66  JUMP_BACK            16  'to 16'
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            52  '52'

 L.  61        68  LOAD_GLOBAL              setattr
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                target
               74  LOAD_FAST                'name'
               76  LOAD_FAST                'value'
               78  CALL_FUNCTION_3       3  ''
               80  POP_TOP          
               82  JUMP_BACK            16  'to 16'
             84_0  COME_FROM            16  '16'

Parse error at or near `JUMP_BACK' instruction at offset 82


def no_replace(f):
    """
    Method decorator to indicate that a method definition shall
    silently be ignored if it already exists in the target class.
    """
    f.__no_replace = True
    return f


class ReferenceEmptyClass(object):
    __doc__ = '\n    This empty class will serve as a reference for attributes present on\n    any class.\n    '