# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: _py_abc.py
from _weakrefset import WeakSet

def get_cache_token():
    """Returns the current ABC cache token.

    The token is an opaque object (supporting equality testing) identifying the
    current version of the ABC cache for virtual subclasses. The token changes
    with every call to ``register()`` on any ABC.
    """
    return ABCMeta._abc_invalidation_counter


class ABCMeta(type):
    __doc__ = "Metaclass for defining Abstract Base Classes (ABCs).\n\n    Use this metaclass to create an ABC.  An ABC can be subclassed\n    directly, and then acts as a mix-in class.  You can also register\n    unrelated concrete classes (even built-in classes) and unrelated\n    ABCs as 'virtual subclasses' -- these and their descendants will\n    be considered subclasses of the registering ABC by the built-in\n    issubclass() function, but the registering ABC won't show up in\n    their MRO (Method Resolution Order) nor will method\n    implementations defined by the registering ABC be callable (not\n    even via super()).\n    "
    _abc_invalidation_counter = 0

    def __new__--- This code section failed: ---

 L.  36         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __new__
                6  LOAD_FAST                'mcls'
                8  LOAD_FAST                'name'
               10  LOAD_FAST                'bases'
               12  LOAD_FAST                'namespace'
               14  BUILD_TUPLE_4         4 
               16  BUILD_MAP_0           0 
               18  LOAD_FAST                'kwargs'
               20  <164>                 1  ''
               22  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               24  STORE_FAST               'cls'

 L.  38        26  LOAD_SETCOMP             '<code_object <setcomp>>'
               28  LOAD_STR                 'ABCMeta.__new__.<locals>.<setcomp>'
               30  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  39        32  LOAD_FAST                'namespace'
               34  LOAD_METHOD              items
               36  CALL_METHOD_0         0  ''

 L.  38        38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'abstracts'

 L.  41        44  LOAD_FAST                'bases'
               46  GET_ITER         
             48_0  COME_FROM           106  '106'
               48  FOR_ITER            108  'to 108'
               50  STORE_FAST               'base'

 L.  42        52  LOAD_GLOBAL              getattr
               54  LOAD_FAST                'base'
               56  LOAD_STR                 '__abstractmethods__'
               58  LOAD_GLOBAL              set
               60  CALL_FUNCTION_0       0  ''
               62  CALL_FUNCTION_3       3  ''
               64  GET_ITER         
             66_0  COME_FROM           104  '104'
             66_1  COME_FROM            92  '92'
               66  FOR_ITER            106  'to 106'
               68  STORE_FAST               'name'

 L.  43        70  LOAD_GLOBAL              getattr
               72  LOAD_FAST                'cls'
               74  LOAD_FAST                'name'
               76  LOAD_CONST               None
               78  CALL_FUNCTION_3       3  ''
               80  STORE_FAST               'value'

 L.  44        82  LOAD_GLOBAL              getattr
               84  LOAD_FAST                'value'
               86  LOAD_STR                 '__isabstractmethod__'
               88  LOAD_CONST               False
               90  CALL_FUNCTION_3       3  ''
               92  POP_JUMP_IF_FALSE_BACK    66  'to 66'

 L.  45        94  LOAD_FAST                'abstracts'
               96  LOAD_METHOD              add
               98  LOAD_FAST                'name'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  JUMP_BACK            66  'to 66'
            106_0  COME_FROM            66  '66'
              106  JUMP_BACK            48  'to 48'
            108_0  COME_FROM            48  '48'

 L.  46       108  LOAD_GLOBAL              frozenset
              110  LOAD_FAST                'abstracts'
              112  CALL_FUNCTION_1       1  ''
              114  LOAD_FAST                'cls'
              116  STORE_ATTR               __abstractmethods__

 L.  48       118  LOAD_GLOBAL              WeakSet
              120  CALL_FUNCTION_0       0  ''
              122  LOAD_FAST                'cls'
              124  STORE_ATTR               _abc_registry

 L.  49       126  LOAD_GLOBAL              WeakSet
              128  CALL_FUNCTION_0       0  ''
              130  LOAD_FAST                'cls'
              132  STORE_ATTR               _abc_cache

 L.  50       134  LOAD_GLOBAL              WeakSet
              136  CALL_FUNCTION_0       0  ''
              138  LOAD_FAST                'cls'
              140  STORE_ATTR               _abc_negative_cache

 L.  51       142  LOAD_GLOBAL              ABCMeta
              144  LOAD_ATTR                _abc_invalidation_counter
              146  LOAD_FAST                'cls'
              148  STORE_ATTR               _abc_negative_cache_version

 L.  52       150  LOAD_FAST                'cls'
              152  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def register(cls, subclass):
        """Register a virtual subclass of an ABC.

        Returns the subclass, to allow usage as a class decorator.
        """
        if not isinstance(subclass, type):
            raise TypeError('Can only register classes')
        if issubclass(subclass, cls):
            return subclass
        if issubclass(cls, subclass):
            raise RuntimeError('Refusing to create an inheritance cycle')
        cls._abc_registry.addsubclass
        ABCMeta._abc_invalidation_counter += 1
        return subclass

    def _dump_registry(cls, file=None):
        """Debug helper to print the ABC registry."""
        print(f"Class: {cls.__module__}.{cls.__qualname__}", file=file)
        print(f"Inv. counter: {get_cache_token}", file=file)
        for name in cls.__dict__:
            if name.startswith'_abc_':
                value = getattr(cls, name)
                if isinstance(value, WeakSet):
                    value = set(value)
                else:
                    print(f"{name}: {value!r}", file=file)

    def _abc_registry_clear(cls):
        """Clear the registry (for debugging or testing)."""
        cls._abc_registry.clear

    def _abc_caches_clear(cls):
        """Clear the caches (for debugging or testing)."""
        cls._abc_cache.clear
        cls._abc_negative_cache.clear

    def __instancecheck__--- This code section failed: ---

 L.  95         0  LOAD_FAST                'instance'
                2  LOAD_ATTR                __class__
                4  STORE_FAST               'subclass'

 L.  96         6  LOAD_FAST                'subclass'
                8  LOAD_DEREF               'cls'
               10  LOAD_ATTR                _abc_cache
               12  <118>                 0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L.  97        16  LOAD_CONST               True
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L.  98        20  LOAD_GLOBAL              type
               22  LOAD_FAST                'instance'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'subtype'

 L.  99        28  LOAD_FAST                'subtype'
               30  LOAD_FAST                'subclass'
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    72  'to 72'

 L. 100        36  LOAD_DEREF               'cls'
               38  LOAD_ATTR                _abc_negative_cache_version

 L. 101        40  LOAD_GLOBAL              ABCMeta
               42  LOAD_ATTR                _abc_invalidation_counter

 L. 100        44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    62  'to 62'

 L. 102        48  LOAD_FAST                'subclass'
               50  LOAD_DEREF               'cls'
               52  LOAD_ATTR                _abc_negative_cache
               54  <118>                 0  ''

 L. 100        56  POP_JUMP_IF_FALSE    62  'to 62'

 L. 103        58  LOAD_CONST               False
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'
             62_1  COME_FROM            46  '46'

 L. 105        62  LOAD_DEREF               'cls'
               64  LOAD_METHOD              __subclasscheck__
               66  LOAD_FAST                'subclass'
               68  CALL_METHOD_1         1  ''
               70  RETURN_VALUE     
             72_0  COME_FROM            34  '34'

 L. 106        72  LOAD_GLOBAL              any
               74  LOAD_CLOSURE             'cls'
               76  BUILD_TUPLE_1         1 
               78  LOAD_GENEXPR             '<code_object <genexpr>>'
               80  LOAD_STR                 'ABCMeta.__instancecheck__.<locals>.<genexpr>'
               82  MAKE_FUNCTION_8          'closure'
               84  LOAD_FAST                'subclass'
               86  LOAD_FAST                'subtype'
               88  BUILD_TUPLE_2         2 
               90  GET_ITER         
               92  CALL_FUNCTION_1       1  ''
               94  CALL_FUNCTION_1       1  ''
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 12

    def __subclasscheck__--- This code section failed: ---

 L. 110         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'subclass'
                4  LOAD_GLOBAL              type
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 111        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'issubclass() arg 1 must be a class'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 113        18  LOAD_FAST                'subclass'
               20  LOAD_FAST                'cls'
               22  LOAD_ATTR                _abc_cache
               24  <118>                 0  ''
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 114        28  LOAD_CONST               True
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 116        32  LOAD_FAST                'cls'
               34  LOAD_ATTR                _abc_negative_cache_version
               36  LOAD_GLOBAL              ABCMeta
               38  LOAD_ATTR                _abc_invalidation_counter
               40  COMPARE_OP               <
               42  POP_JUMP_IF_FALSE    62  'to 62'

 L. 118        44  LOAD_GLOBAL              WeakSet
               46  CALL_FUNCTION_0       0  ''
               48  LOAD_FAST                'cls'
               50  STORE_ATTR               _abc_negative_cache

 L. 119        52  LOAD_GLOBAL              ABCMeta
               54  LOAD_ATTR                _abc_invalidation_counter
               56  LOAD_FAST                'cls'
               58  STORE_ATTR               _abc_negative_cache_version
               60  JUMP_FORWARD         76  'to 76'
             62_0  COME_FROM            42  '42'

 L. 120        62  LOAD_FAST                'subclass'
               64  LOAD_FAST                'cls'
               66  LOAD_ATTR                _abc_negative_cache
               68  <118>                 0  ''
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L. 121        72  LOAD_CONST               False
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'
             76_1  COME_FROM            60  '60'

 L. 123        76  LOAD_FAST                'cls'
               78  LOAD_METHOD              __subclasshook__
               80  LOAD_FAST                'subclass'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'ok'

 L. 124        86  LOAD_FAST                'ok'
               88  LOAD_GLOBAL              NotImplemented
               90  <117>                 1  ''
               92  POP_JUMP_IF_FALSE   142  'to 142'

 L. 125        94  LOAD_GLOBAL              isinstance
               96  LOAD_FAST                'ok'
               98  LOAD_GLOBAL              bool
              100  CALL_FUNCTION_2       2  ''
              102  POP_JUMP_IF_TRUE    108  'to 108'
              104  <74>             
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM           102  '102'

 L. 126       108  LOAD_FAST                'ok'
              110  POP_JUMP_IF_FALSE   126  'to 126'

 L. 127       112  LOAD_FAST                'cls'
              114  LOAD_ATTR                _abc_cache
              116  LOAD_METHOD              add
              118  LOAD_FAST                'subclass'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  JUMP_FORWARD        138  'to 138'
            126_0  COME_FROM           110  '110'

 L. 129       126  LOAD_FAST                'cls'
              128  LOAD_ATTR                _abc_negative_cache
              130  LOAD_METHOD              add
              132  LOAD_FAST                'subclass'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           124  '124'

 L. 130       138  LOAD_FAST                'ok'
              140  RETURN_VALUE     
            142_0  COME_FROM            92  '92'

 L. 132       142  LOAD_FAST                'cls'
              144  LOAD_GLOBAL              getattr
              146  LOAD_FAST                'subclass'
              148  LOAD_STR                 '__mro__'
              150  LOAD_CONST               ()
              152  CALL_FUNCTION_3       3  ''
              154  <118>                 0  ''
              156  POP_JUMP_IF_FALSE   174  'to 174'

 L. 133       158  LOAD_FAST                'cls'
              160  LOAD_ATTR                _abc_cache
              162  LOAD_METHOD              add
              164  LOAD_FAST                'subclass'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 134       170  LOAD_CONST               True
              172  RETURN_VALUE     
            174_0  COME_FROM           156  '156'

 L. 136       174  LOAD_FAST                'cls'
              176  LOAD_ATTR                _abc_registry
              178  GET_ITER         
            180_0  COME_FROM           212  '212'
            180_1  COME_FROM           192  '192'
              180  FOR_ITER            214  'to 214'
              182  STORE_FAST               'rcls'

 L. 137       184  LOAD_GLOBAL              issubclass
              186  LOAD_FAST                'subclass'
              188  LOAD_FAST                'rcls'
              190  CALL_FUNCTION_2       2  ''
              192  POP_JUMP_IF_FALSE_BACK   180  'to 180'

 L. 138       194  LOAD_FAST                'cls'
              196  LOAD_ATTR                _abc_cache
              198  LOAD_METHOD              add
              200  LOAD_FAST                'subclass'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 139       206  POP_TOP          
              208  LOAD_CONST               True
              210  RETURN_VALUE     
              212  JUMP_BACK           180  'to 180'
            214_0  COME_FROM           180  '180'

 L. 141       214  LOAD_FAST                'cls'
              216  LOAD_METHOD              __subclasses__
              218  CALL_METHOD_0         0  ''
              220  GET_ITER         
            222_0  COME_FROM           254  '254'
            222_1  COME_FROM           234  '234'
              222  FOR_ITER            256  'to 256'
              224  STORE_FAST               'scls'

 L. 142       226  LOAD_GLOBAL              issubclass
              228  LOAD_FAST                'subclass'
              230  LOAD_FAST                'scls'
              232  CALL_FUNCTION_2       2  ''
              234  POP_JUMP_IF_FALSE_BACK   222  'to 222'

 L. 143       236  LOAD_FAST                'cls'
              238  LOAD_ATTR                _abc_cache
              240  LOAD_METHOD              add
              242  LOAD_FAST                'subclass'
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 144       248  POP_TOP          
              250  LOAD_CONST               True
              252  RETURN_VALUE     
              254  JUMP_BACK           222  'to 222'
            256_0  COME_FROM           222  '222'

 L. 146       256  LOAD_FAST                'cls'
              258  LOAD_ATTR                _abc_negative_cache
              260  LOAD_METHOD              add
              262  LOAD_FAST                'subclass'
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          

 L. 147       268  LOAD_CONST               False
              270  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 24