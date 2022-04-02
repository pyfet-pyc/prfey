# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\utils.py
from __future__ import absolute_import, division, print_function
import abc, binascii, inspect, sys, warnings

class CryptographyDeprecationWarning(UserWarning):
    pass


PersistentlyDeprecated2017 = CryptographyDeprecationWarning
PersistentlyDeprecated2019 = CryptographyDeprecationWarning

def _check_bytes(name, value):
    if not isinstance(value, bytes):
        raise TypeError('{} must be bytes'.format(name))


def _check_byteslike--- This code section failed: ---

 L.  33         0  SETUP_FINALLY        14  'to 14'

 L.  34         2  LOAD_GLOBAL              memoryview
                4  LOAD_FAST                'value'
                6  CALL_FUNCTION_1       1  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         46  'to 46'
             14_0  COME_FROM_FINALLY     0  '0'

 L.  35        14  DUP_TOP          
               16  LOAD_GLOBAL              TypeError
               18  <121>                44  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  36        26  LOAD_GLOBAL              TypeError
               28  LOAD_STR                 '{} must be bytes-like'
               30  LOAD_METHOD              format
               32  LOAD_FAST                'name'
               34  CALL_METHOD_1         1  ''
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
               40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
               44  <48>             
             46_0  COME_FROM            42  '42'
             46_1  COME_FROM            12  '12'

Parse error at or near `<121>' instruction at offset 18


def read_only_property(name):
    return property(lambda self: getattr(self, name))


def register_interface(iface):

    def register_decorator(klass):
        verify_interface(iface, klass)
        iface.register(klass)
        return klass

    return register_decorator


def register_interface_if(predicate, iface):

    def register_decorator(klass):
        if predicate:
            verify_interface(iface, klass)
            iface.register(klass)
        return klass

    return register_decorator


if hasattr(int, 'from_bytes'):
    int_from_bytes = int.from_bytes
else:

    def int_from_bytes--- This code section failed: ---

 L.  67         0  LOAD_FAST                'byteorder'
                2  LOAD_STR                 'big'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L.  68        12  LOAD_FAST                'signed'
               14  POP_JUMP_IF_FALSE    20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L.  70        20  LOAD_GLOBAL              int
               22  LOAD_GLOBAL              binascii
               24  LOAD_METHOD              hexlify
               26  LOAD_FAST                'data'
               28  CALL_METHOD_1         1  ''
               30  LOAD_CONST               16
               32  CALL_FUNCTION_2       2  ''
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


if hasattr(int, 'to_bytes'):

    def int_to_bytes(integer, length=None):
        return integer.to_bytes(length or (integer.bit_length() + 7) // 8 or 1, 'big')


else:

    def int_to_bytes--- This code section failed: ---

 L.  84         0  LOAD_STR                 '%x'
                2  LOAD_FAST                'integer'
                4  BINARY_MODULO    
                6  STORE_FAST               'hex_string'

 L.  85         8  LOAD_FAST                'length'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L.  86        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'hex_string'
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'n'
               24  JUMP_FORWARD         34  'to 34'
             26_0  COME_FROM            14  '14'

 L.  88        26  LOAD_FAST                'length'
               28  LOAD_CONST               2
               30  BINARY_MULTIPLY  
               32  STORE_FAST               'n'
             34_0  COME_FROM            24  '24'

 L.  89        34  LOAD_GLOBAL              binascii
               36  LOAD_METHOD              unhexlify
               38  LOAD_FAST                'hex_string'
               40  LOAD_METHOD              zfill
               42  LOAD_FAST                'n'
               44  LOAD_FAST                'n'
               46  LOAD_CONST               1
               48  BINARY_AND       
               50  BINARY_ADD       
               52  CALL_METHOD_1         1  ''
               54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12


class InterfaceNotImplemented(Exception):
    pass


if hasattr(inspect, 'signature'):
    signature = inspect.signature
else:
    signature = inspect.getargspec

def verify_interface(iface, klass):
    for method in iface.__abstractmethods__:
        if not hasattr(klass, method):
            raise InterfaceNotImplemented('{} is missing a {!r} method'.format(klass, method))
        if isinstance(getattr(iface, method), abc.abstractproperty):
            pass
        else:
            sig = signature(getattr(iface, method))
            actual = signature(getattr(klass, method))
            if sig != actual:
                raise InterfaceNotImplemented("{}.{}'s signature differs from the expected. Expected: {!r}. Received: {!r}".format(klass, method, sig, actual))


class _DeprecatedValue(object):

    def __init__(self, value, message, warning_class):
        self.value = value
        self.message = message
        self.warning_class = warning_class


class _ModuleWithDeprecations(object):

    def __init__(self, module):
        self.__dict__['_module'] = module

    def __getattr__(self, attr):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn((obj.message), (obj.warning_class), stacklevel=2)
            obj = obj.value
        return obj

    def __setattr__(self, attr, value):
        setattr(self._module, attr, value)

    def __delattr__(self, attr):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn((obj.message), (obj.warning_class), stacklevel=2)
        delattr(self._module, attr)

    def __dir__(self):
        return [
         '_module'] + dir(self._module)


def deprecated(value, module_name, message, warning_class):
    module = sys.modules[module_name]
    if not isinstance(module, _ModuleWithDeprecations):
        sys.modules[module_name] = _ModuleWithDeprecations(module)
    return _DeprecatedValue(value, message, warning_class)


def cached_property(func):
    cached_name = '_cached_{}'.format(func)
    sentinel = object()

    def inner--- This code section failed: ---

 L. 164         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'instance'
                4  LOAD_DEREF               'cached_name'
                6  LOAD_DEREF               'sentinel'
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'cache'

 L. 165        12  LOAD_FAST                'cache'
               14  LOAD_DEREF               'sentinel'
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 166        20  LOAD_FAST                'cache'
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 167        24  LOAD_DEREF               'func'
               26  LOAD_FAST                'instance'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'result'

 L. 168        32  LOAD_GLOBAL              setattr
               34  LOAD_FAST                'instance'
               36  LOAD_DEREF               'cached_name'
               38  LOAD_FAST                'result'
               40  CALL_FUNCTION_3       3  ''
               42  POP_TOP          

 L. 169        44  LOAD_FAST                'result'
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    return property(inner)