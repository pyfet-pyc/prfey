# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: keyring\core.py
"""
Core API functions and initialization routines.
"""
import configparser, os, sys, logging, typing
from . import backend, credentials
from .util import platform_ as platform
from .backends import fail
log = logging.getLogger(__name__)
_keyring_backend = None

def set_keyring(keyring):
    """Set current keyring backend."""
    global _keyring_backend
    if not isinstance(keyring, backend.KeyringBackend):
        raise TypeError('The keyring must be a subclass of KeyringBackend')
    _keyring_backend = keyring


def get_keyring--- This code section failed: ---

 L.  31         0  LOAD_GLOBAL              _keyring_backend
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  32         8  LOAD_GLOBAL              init_backend
               10  CALL_FUNCTION_0       0  ''
               12  POP_TOP          
             14_0  COME_FROM             6  '6'

 L.  33        14  LOAD_GLOBAL              typing
               16  LOAD_METHOD              cast
               18  LOAD_GLOBAL              backend
               20  LOAD_ATTR                KeyringBackend
               22  LOAD_GLOBAL              _keyring_backend
               24  CALL_METHOD_2         2  ''
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def disable--- This code section failed: ---

 L.  40         0  LOAD_GLOBAL              platform
                2  LOAD_METHOD              config_root
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'root'

 L.  41         8  SETUP_FINALLY        24  'to 24'

 L.  42        10  LOAD_GLOBAL              os
               12  LOAD_METHOD              makedirs
               14  LOAD_FAST                'root'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          
               20  POP_BLOCK        
               22  JUMP_FORWARD         42  'to 42'
             24_0  COME_FROM_FINALLY     8  '8'

 L.  43        24  DUP_TOP          
               26  LOAD_GLOBAL              OSError
               28  <121>                40  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  44        36  POP_EXCEPT       
               38  JUMP_FORWARD         42  'to 42'
               40  <48>             
             42_0  COME_FROM            38  '38'
             42_1  COME_FROM            22  '22'

 L.  45        42  LOAD_GLOBAL              os
               44  LOAD_ATTR                path
               46  LOAD_METHOD              join
               48  LOAD_FAST                'root'
               50  LOAD_STR                 'keyringrc.cfg'
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'filename'

 L.  46        56  LOAD_GLOBAL              os
               58  LOAD_ATTR                path
               60  LOAD_METHOD              exists
               62  LOAD_FAST                'filename'
               64  CALL_METHOD_1         1  ''
               66  POP_JUMP_IF_FALSE    86  'to 86'

 L.  47        68  LOAD_STR                 'Refusing to overwrite '
               70  LOAD_FAST                'filename'
               72  FORMAT_VALUE          0  ''
               74  BUILD_STRING_2        2 
               76  STORE_FAST               'msg'

 L.  48        78  LOAD_GLOBAL              RuntimeError
               80  LOAD_FAST                'msg'
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            66  '66'

 L.  49        86  LOAD_GLOBAL              open
               88  LOAD_FAST                'filename'
               90  LOAD_STR                 'w'
               92  CALL_FUNCTION_2       2  ''
               94  SETUP_WITH          122  'to 122'
               96  STORE_FAST               'file'

 L.  50        98  LOAD_FAST                'file'
              100  LOAD_METHOD              write
              102  LOAD_STR                 '[backend]\ndefault-keyring=keyring.backends.null.Keyring'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
              108  POP_BLOCK        
              110  LOAD_CONST               None
              112  DUP_TOP          
              114  DUP_TOP          
              116  CALL_FUNCTION_3       3  ''
              118  POP_TOP          
              120  JUMP_FORWARD        138  'to 138'
            122_0  COME_FROM_WITH       94  '94'
              122  <49>             
              124  POP_JUMP_IF_TRUE    128  'to 128'
              126  <48>             
            128_0  COME_FROM           124  '124'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          
              134  POP_EXCEPT       
              136  POP_TOP          
            138_0  COME_FROM           120  '120'

Parse error at or near `<121>' instruction at offset 28


def get_password(service_name: str, username: str) -> typing.Optional[str]:
    """Get password from the specified service."""
    return get_keyring.get_passwordservice_nameusername


def set_password(service_name: str, username: str, password: str) -> None:
    """Set password for the user in the specified service."""
    get_keyring.set_password(service_name, username, password)


def delete_password(service_name: str, username: str) -> None:
    """Delete the password for the user in the specified service."""
    get_keyring.delete_passwordservice_nameusername


def get_credential(service_name: str, username: typing.Optional[str]) -> typing.Optional[credentials.Credential]:
    """Get a Credential for the specified service."""
    return get_keyring.get_credentialservice_nameusername


def recommended(backend):
    return backend.priority >= 1


def init_backend(limit=None):
    """
    Load a detected backend.
    """
    set_keyring(_detect_backend(limit))


def _detect_backend(limit=None):
    """
    Return a keyring specified in the config file or infer the best available.

    Limit, if supplied, should be a callable taking a backend and returning
    True if that backend should be included for consideration.
    """
    backend._limit = limit
    return load_env or load_config or max((filter(limit, backend.get_all_keyring)),
      default=(fail.Keyring),
      key=(backend.by_priority))


def _load_keyring_class(keyring_name):
    """
    Load the keyring class indicated by name.

    These popular names are tested to ensure their presence.

    >>> popular_names = [
    ...      'keyring.backends.Windows.WinVaultKeyring',
    ...      'keyring.backends.macOS.Keyring',
    ...      'keyring.backends.kwallet.DBusKeyring',
    ...      'keyring.backends.SecretService.Keyring',
    ...  ]
    >>> list(map(_load_keyring_class, popular_names))
    [...]
    """
    module_name, sep, class_name = keyring_name.rpartition('.')
    __import__(module_name)
    module = sys.modules[module_name]
    return getattr(module, class_name)


def load_keyring(keyring_name):
    """
    Load the specified keyring by name (a fully-qualified name to the
    keyring, such as 'keyring.backends.file.PlaintextKeyring')
    """
    class_ = _load_keyring_class(keyring_name)
    class_.priority
    return class_


def load_env--- This code section failed: ---

 L. 142         0  SETUP_FINALLY        18  'to 18'

 L. 143         2  LOAD_GLOBAL              load_keyring
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                environ
                8  LOAD_STR                 'PYTHON_KEYRING_BACKEND'
               10  BINARY_SUBSCR    
               12  CALL_FUNCTION_1       1  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 144        18  DUP_TOP          
               20  LOAD_GLOBAL              KeyError
               22  <121>                34  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 145        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
               34  <48>             
             36_0  COME_FROM            32  '32'

Parse error at or near `<121>' instruction at offset 22


def load_config--- This code section failed: ---

 L. 151         0  LOAD_STR                 'keyringrc.cfg'
                2  STORE_FAST               'filename'

 L. 153         4  LOAD_GLOBAL              os
                6  LOAD_ATTR                path
                8  LOAD_METHOD              join
               10  LOAD_GLOBAL              platform
               12  LOAD_METHOD              config_root
               14  CALL_METHOD_0         0  ''
               16  LOAD_FAST                'filename'
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'keyring_cfg'

 L. 155        22  LOAD_GLOBAL              os
               24  LOAD_ATTR                path
               26  LOAD_METHOD              exists
               28  LOAD_FAST                'keyring_cfg'
               30  CALL_METHOD_1         1  ''
               32  POP_JUMP_IF_TRUE     38  'to 38'

 L. 156        34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 158        38  LOAD_GLOBAL              configparser
               40  LOAD_METHOD              RawConfigParser
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'config'

 L. 159        46  LOAD_FAST                'config'
               48  LOAD_METHOD              read
               50  LOAD_FAST                'keyring_cfg'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 160        56  LOAD_GLOBAL              _load_keyring_path
               58  LOAD_FAST                'config'
               60  CALL_FUNCTION_1       1  ''
               62  POP_TOP          

 L. 163        64  SETUP_FINALLY       110  'to 110'

 L. 164        66  LOAD_FAST                'config'
               68  LOAD_METHOD              has_section
               70  LOAD_STR                 'backend'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_FALSE    94  'to 94'

 L. 165        76  LOAD_FAST                'config'
               78  LOAD_METHOD              get
               80  LOAD_STR                 'backend'
               82  LOAD_STR                 'default-keyring'
               84  CALL_METHOD_2         2  ''
               86  LOAD_METHOD              strip
               88  CALL_METHOD_0         0  ''
               90  STORE_FAST               'keyring_name'
               92  JUMP_FORWARD        106  'to 106'
             94_0  COME_FROM            74  '74'

 L. 167        94  LOAD_GLOBAL              configparser
               96  LOAD_METHOD              NoOptionError
               98  LOAD_STR                 'backend'
              100  LOAD_STR                 'default-keyring'
              102  CALL_METHOD_2         2  ''
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            92  '92'
              106  POP_BLOCK        
              108  JUMP_FORWARD        164  'to 164'
            110_0  COME_FROM_FINALLY    64  '64'

 L. 169       110  DUP_TOP          
              112  LOAD_GLOBAL              configparser
              114  LOAD_ATTR                NoOptionError
              116  LOAD_GLOBAL              ImportError
              118  BUILD_TUPLE_2         2 
              120  <121>               162  ''
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L. 170       128  LOAD_GLOBAL              logging
              130  LOAD_METHOD              getLogger
              132  LOAD_STR                 'keyring'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'logger'

 L. 171       138  LOAD_FAST                'logger'
              140  LOAD_METHOD              warning

 L. 172       142  LOAD_STR                 'Keyring config file contains incorrect values.\n'

 L. 173       144  LOAD_STR                 'Config file: %s'
              146  LOAD_FAST                'keyring_cfg'
              148  BINARY_MODULO    

 L. 172       150  BINARY_ADD       

 L. 171       152  CALL_METHOD_1         1  ''
              154  POP_TOP          

 L. 175       156  POP_EXCEPT       
              158  LOAD_CONST               None
              160  RETURN_VALUE     
              162  <48>             
            164_0  COME_FROM           108  '108'

 L. 177       164  LOAD_GLOBAL              load_keyring
              166  LOAD_FAST                'keyring_name'
              168  CALL_FUNCTION_1       1  ''
              170  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 120


def _load_keyring_path--- This code section failed: ---

 L. 182         0  SETUP_FINALLY        36  'to 36'

 L. 183         2  LOAD_FAST                'config'
                4  LOAD_METHOD              get
                6  LOAD_STR                 'backend'
                8  LOAD_STR                 'keyring-path'
               10  CALL_METHOD_2         2  ''
               12  LOAD_METHOD              strip
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'path'

 L. 184        18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                path
               22  LOAD_METHOD              insert
               24  LOAD_CONST               0
               26  LOAD_FAST                'path'
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          
               32  POP_BLOCK        
               34  JUMP_FORWARD         62  'to 62'
             36_0  COME_FROM_FINALLY     0  '0'

 L. 185        36  DUP_TOP          
               38  LOAD_GLOBAL              configparser
               40  LOAD_ATTR                NoOptionError
               42  LOAD_GLOBAL              configparser
               44  LOAD_ATTR                NoSectionError
               46  BUILD_TUPLE_2         2 
               48  <121>                60  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 186        56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
               60  <48>             
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            34  '34'

Parse error at or near `<121>' instruction at offset 48