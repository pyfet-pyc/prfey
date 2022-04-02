# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\utils.py
import abc, inspect, sys, typing, warnings

class CryptographyDeprecationWarning(UserWarning):
    pass


PersistentlyDeprecated2017 = CryptographyDeprecationWarning
PersistentlyDeprecated2019 = CryptographyDeprecationWarning
DeprecatedIn34 = CryptographyDeprecationWarning

def _check_bytes(name: str, value: bytes):
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


def read_only_property(name: str):
    return property(lambda self: getattr(self, name))


def register_interface(iface):

    def register_decorator(klass, *, check_annotations=False):
        verify_interface(iface, klass, check_annotations=check_annotations)
        iface.register(klass)
        return klass

    return register_decorator


def register_interface_if(predicate, iface):

    def register_decorator(klass, *, check_annotations=False):
        if predicate:
            verify_interface(iface, klass, check_annotations=check_annotations)
            iface.register(klass)
        return klass

    return register_decorator


def int_to_bytes(integer: int, length: typing.Optional[int]=None) -> bytes:
    return integer.to_bytes(length or (integer.bit_length() + 7) // 8 or 1, 'big')


class InterfaceNotImplemented(Exception):
    pass


def strip_annotation(signature):
    return inspect.Signature([param.replace(annotation=(inspect.Parameter.empty)) for param in signature.parameters.values()])


def verify_interface(iface, klass, *, check_annotations=False):
    for method in iface.__abstractmethods__:
        if not hasattr(klass, method):
            raise InterfaceNotImplemented('{} is missing a {!r} method'.format(klass, method))
        if isinstance(getattr(iface, method), abc.abstractproperty):
            pass
        else:
            sig = inspect.signature(getattr(iface, method))
            actual = inspect.signature(getattr(klass, method))
            if check_annotations:
                ok = sig == actual
            else:
                ok = strip_annotation(sig) == strip_annotation(actual)
            if not ok:
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

 L. 149         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'instance'
                4  LOAD_DEREF               'cached_name'
                6  LOAD_DEREF               'sentinel'
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'cache'

 L. 150        12  LOAD_FAST                'cache'
               14  LOAD_DEREF               'sentinel'
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 151        20  LOAD_FAST                'cache'
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 152        24  LOAD_DEREF               'func'
               26  LOAD_FAST                'instance'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'result'

 L. 153        32  LOAD_GLOBAL              setattr
               34  LOAD_FAST                'instance'
               36  LOAD_DEREF               'cached_name'
               38  LOAD_FAST                'result'
               40  CALL_FUNCTION_3       3  ''
               42  POP_TOP          

 L. 154        44  LOAD_FAST                'result'
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    return property(inner)


int_from_bytes = deprecated(int.from_bytes, __name__, 'int_from_bytes is deprecated, use int.from_bytes instead', DeprecatedIn34)