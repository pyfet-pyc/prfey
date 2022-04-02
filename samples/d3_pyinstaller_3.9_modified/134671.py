# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: keyring\backend.py
"""
Keyring implementation support
"""
import os, abc, logging, operator
from typing import Optional
import importlib_metadata as metadata
from . import credentials, errors, util
from .util import properties
log = logging.getLogger(__name__)
by_priority = operator.attrgetter('priority')
_limit = None

class KeyringBackendMeta(abc.ABCMeta):
    __doc__ = "\n    A metaclass that's both an ABCMeta and a type that keeps a registry of\n    all (non-abstract) types.\n    "

    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        if not hasattr(cls, '_classes'):
            cls._classes = set()
        classes = cls._classes
        if not cls.__abstractmethods__:
            classes.add(cls)


class KeyringBackend(metaclass=KeyringBackendMeta):
    __doc__ = 'The abstract base class of the keyring, every backend must implement\n    this interface.\n    '

    def __init__(self):
        self.set_properties_from_env()

    def priority(cls):
        """
        Each backend class must supply a priority, a number (float or integer)
        indicating the priority of the backend relative to all other backends.
        The priority need not be static -- it may (and should) vary based
        attributes of the environment in which is runs (platform, available
        packages, etc.).

        A higher number indicates a higher priority. The priority should raise
        a RuntimeError with a message indicating the underlying cause if the
        backend is not suitable for the current environment.

        As a rule of thumb, a priority between zero but less than one is
        suitable, but a priority of one or greater is recommended.
        """
        pass

    @properties.ClassProperty
    @classmethod
    def viable--- This code section failed: ---

 L.  67         0  LOAD_GLOBAL              errors
                2  LOAD_METHOD              ExceptionRaisedContext
                4  CALL_METHOD_0         0  ''
                6  SETUP_WITH           30  'to 30'
                8  STORE_FAST               'exc'

 L.  68        10  LOAD_FAST                'cls'
               12  LOAD_ATTR                priority
               14  POP_TOP          
               16  POP_BLOCK        
               18  LOAD_CONST               None
               20  DUP_TOP          
               22  DUP_TOP          
               24  CALL_FUNCTION_3       3  ''
               26  POP_TOP          
               28  JUMP_FORWARD         46  'to 46'
             30_0  COME_FROM_WITH        6  '6'
               30  <49>             
               32  POP_JUMP_IF_TRUE     36  'to 36'
               34  <48>             
             36_0  COME_FROM            32  '32'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          
               42  POP_EXCEPT       
               44  POP_TOP          
             46_0  COME_FROM            28  '28'

 L.  69        46  LOAD_FAST                'exc'
               48  UNARY_NOT        
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 20

    @classmethod
    def get_viable_backends(cls):
        """
        Return all subclasses deemed viable.
        """
        return filter(operator.attrgetter('viable'), cls._classes)

    @properties.ClassProperty
    @classmethod
    def name(cls):
        """
        The keyring name, suitable for display.

        The name is derived from module and class name.
        """
        parent, sep, mod_name = cls.__module__.rpartition('.')
        mod_name = mod_name.replace('_', ' ')
        return ' '.join([mod_name, cls.__name__])

    def __str__(self):
        keyring_class = type(self)
        return '{}.{} (priority: {:g})'.format(keyring_class.__module__, keyring_class.__name__, keyring_class.priority)

    @abc.abstractmethod
    def get_password(self, service: str, username: str) -> Optional[str]:
        """Get password of the username for the service"""
        pass

    @abc.abstractmethod
    def set_password(self, service: str, username: str, password: str) -> None:
        """Set password for the username of the service.

        If the backend cannot store passwords, raise
        PasswordSetError.
        """
        raise errors.PasswordSetError('reason')

    def delete_password(self, service: str, username: str) -> None:
        """Delete the password for the username of the service.

        If the backend cannot delete passwords, raise
        PasswordDeleteError.
        """
        raise errors.PasswordDeleteError('reason')

    def get_credential--- This code section failed: ---

 L. 137         0  LOAD_FAST                'username'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    40  'to 40'

 L. 138         8  LOAD_FAST                'self'
               10  LOAD_METHOD              get_password
               12  LOAD_FAST                'service'
               14  LOAD_FAST                'username'
               16  CALL_METHOD_2         2  ''
               18  STORE_FAST               'password'

 L. 139        20  LOAD_FAST                'password'
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 140        28  LOAD_GLOBAL              credentials
               30  LOAD_METHOD              SimpleCredential
               32  LOAD_FAST                'username'
               34  LOAD_FAST                'password'
               36  CALL_METHOD_2         2  ''
               38  RETURN_VALUE     
             40_0  COME_FROM            26  '26'
             40_1  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1

    def set_properties_from_env(self):
        """For all KEYRING_PROPERTY_* env var, set that property."""

        def parse(item):
            key, value = item
            pre, sep, name = key.partition('KEYRING_PROPERTY_')
            return sep and (name.lower(), value)

        props = filter(None, map(parse, os.environ.items()))
        for name, value in props:
            setattr(self, name, value)


class Crypter:
    __doc__ = 'Base class providing encryption and decryption'

    @abc.abstractmethod
    def encrypt(self, value):
        """Encrypt the value."""
        pass

    @abc.abstractmethod
    def decrypt(self, value):
        """Decrypt the value."""
        pass


class NullCrypter(Crypter):
    __doc__ = 'A crypter that does nothing'

    def encrypt(self, value):
        return value

    def decrypt(self, value):
        return value


def _load_plugins--- This code section failed: ---

 L. 198         0  LOAD_GLOBAL              metadata
                2  LOAD_ATTR                entry_points
                4  LOAD_STR                 'keyring.backends'
                6  LOAD_CONST               ('group',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  GET_ITER         
             12_0  COME_FROM            94  '94'
             12_1  COME_FROM            90  '90'
             12_2  COME_FROM            56  '56'
               12  FOR_ITER             96  'to 96'
               14  STORE_FAST               'ep'

 L. 199        16  SETUP_FINALLY        58  'to 58'

 L. 200        18  LOAD_GLOBAL              log
               20  LOAD_METHOD              debug
               22  LOAD_STR                 'Loading %s'
               24  LOAD_FAST                'ep'
               26  LOAD_ATTR                name
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          

 L. 201        32  LOAD_FAST                'ep'
               34  LOAD_METHOD              load
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'init_func'

 L. 202        40  LOAD_GLOBAL              callable
               42  LOAD_FAST                'init_func'
               44  CALL_FUNCTION_1       1  ''
               46  POP_JUMP_IF_FALSE    54  'to 54'

 L. 203        48  LOAD_FAST                'init_func'
               50  CALL_FUNCTION_0       0  ''
               52  POP_TOP          
             54_0  COME_FROM            46  '46'
               54  POP_BLOCK        
               56  JUMP_BACK            12  'to 12'
             58_0  COME_FROM_FINALLY    16  '16'

 L. 204        58  DUP_TOP          
               60  LOAD_GLOBAL              Exception
               62  <121>                92  ''
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 205        70  LOAD_GLOBAL              log
               72  LOAD_METHOD              exception
               74  LOAD_STR                 'Error initializing plugin '
               76  LOAD_FAST                'ep'
               78  FORMAT_VALUE          0  ''
               80  LOAD_STR                 '.'
               82  BUILD_STRING_3        3 
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
               88  POP_EXCEPT       
               90  JUMP_BACK            12  'to 12'
               92  <48>             
               94  JUMP_BACK            12  'to 12'
             96_0  COME_FROM            12  '12'

Parse error at or near `<121>' instruction at offset 62


@util.once
def get_all_keyring():
    """
    Return a list of all implemented keyrings that can be constructed without
    parameters.
    """
    _load_plugins()
    viable_classes = KeyringBackend.get_viable_backends()
    rings = util.suppress_exceptions(viable_classes, exceptions=TypeError)
    return list(rings)