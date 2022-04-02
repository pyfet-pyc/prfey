# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: secretstorage\util.py
"""This module provides some utility functions, but these shouldn't
normally be used by external applications."""
import os
from typing import Any, List, Tuple
from jeepney import DBusAddress, DBusErrorResponse, MatchRule, Message, MessageType, new_method_call, Properties
from jeepney.io.blocking import DBusConnection
from secretstorage.defines import DBUS_UNKNOWN_METHOD, DBUS_NO_SUCH_OBJECT, DBUS_SERVICE_UNKNOWN, DBUS_NO_REPLY, DBUS_NOT_SUPPORTED, DBUS_EXEC_FAILED, SS_PATH, SS_PREFIX, ALGORITHM_DH, ALGORITHM_PLAIN
from secretstorage.dhcrypto import Session, int_to_bytes
from secretstorage.exceptions import ItemNotFoundException, SecretServiceNotAvailableException
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
BUS_NAME = 'org.freedesktop.secrets'
SERVICE_IFACE = SS_PREFIX + 'Service'
PROMPT_IFACE = SS_PREFIX + 'Prompt'

class DBusAddressWrapper(DBusAddress):
    __doc__ = 'A wrapper class around :class:`jeepney.wrappers.DBusAddress`\n\tthat adds some additional methods for calling and working with\n\tproperties, and converts error responses to SecretStorage\n\texceptions.\n\n\t.. versionadded:: 3.0\n\t'

    def __init__(self, path: str, interface: str, connection: DBusConnection) -> None:
        DBusAddress.__init__(self, path, BUS_NAME, interface)
        self._connection = connection

    def send_and_get_reply--- This code section failed: ---

 L.  45         0  SETUP_FINALLY        20  'to 20'

 L.  46         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _connection
                6  LOAD_ATTR                send_and_get_reply
                8  LOAD_FAST                'msg'
               10  LOAD_CONST               True
               12  LOAD_CONST               ('unwrap',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  47        20  DUP_TOP          
               22  LOAD_GLOBAL              DBusErrorResponse
               24  <121>               132  ''
               26  POP_TOP          
               28  STORE_FAST               'resp'
               30  POP_TOP          
               32  SETUP_FINALLY       124  'to 124'

 L.  48        34  LOAD_FAST                'resp'
               36  LOAD_ATTR                name
               38  LOAD_GLOBAL              DBUS_UNKNOWN_METHOD
               40  LOAD_GLOBAL              DBUS_NO_SUCH_OBJECT
               42  BUILD_TUPLE_2         2 
               44  <118>                 0  ''
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L.  49        48  LOAD_GLOBAL              ItemNotFoundException
               50  LOAD_STR                 'Item does not exist!'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_FAST                'resp'
               56  RAISE_VARARGS_2       2  'exception instance with __cause__'
               58  JUMP_FORWARD        110  'to 110'
             60_0  COME_FROM            46  '46'

 L.  50        60  LOAD_FAST                'resp'
               62  LOAD_ATTR                name
               64  LOAD_GLOBAL              DBUS_SERVICE_UNKNOWN
               66  LOAD_GLOBAL              DBUS_EXEC_FAILED

 L.  51        68  LOAD_GLOBAL              DBUS_NO_REPLY

 L.  50        70  BUILD_TUPLE_3         3 
               72  <118>                 0  ''
               74  POP_JUMP_IF_FALSE   110  'to 110'

 L.  52        76  LOAD_FAST                'resp'
               78  LOAD_ATTR                data
               80  STORE_FAST               'data'

 L.  53        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'data'
               86  LOAD_GLOBAL              tuple
               88  CALL_FUNCTION_2       2  ''
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L.  54        92  LOAD_FAST                'data'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  STORE_FAST               'data'
            100_0  COME_FROM            90  '90'

 L.  55       100  LOAD_GLOBAL              SecretServiceNotAvailableException
              102  LOAD_FAST                'data'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_FAST                'resp'
              108  RAISE_VARARGS_2       2  'exception instance with __cause__'
            110_0  COME_FROM            74  '74'
            110_1  COME_FROM            58  '58'

 L.  56       110  RAISE_VARARGS_0       0  'reraise'
              112  POP_BLOCK        
              114  POP_EXCEPT       
              116  LOAD_CONST               None
              118  STORE_FAST               'resp'
              120  DELETE_FAST              'resp'
              122  JUMP_FORWARD        134  'to 134'
            124_0  COME_FROM_FINALLY    32  '32'
              124  LOAD_CONST               None
              126  STORE_FAST               'resp'
              128  DELETE_FAST              'resp'
              130  <48>             
              132  <48>             
            134_0  COME_FROM           122  '122'

Parse error at or near `<121>' instruction at offset 24

    def call(self, method: str, signature: str, *body: Any) -> Any:
        msg = new_method_call(self, method, signature, body)
        return self.send_and_get_reply(msg)

    def get_property(self, name: str) -> Any:
        msg = Properties(self).get(name)
        (signature, value), = self.send_and_get_reply(msg)
        return value

    def set_property(self, name: str, signature: str, value: Any) -> None:
        msg = Properties(self).set(name, signature, value)
        self.send_and_get_reply(msg)


def open_session--- This code section failed: ---

 L.  74         0  LOAD_GLOBAL              DBusAddressWrapper
                2  LOAD_GLOBAL              SS_PATH
                4  LOAD_GLOBAL              SERVICE_IFACE
                6  LOAD_FAST                'connection'
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'service'

 L.  75        12  LOAD_GLOBAL              Session
               14  CALL_FUNCTION_0       0  ''
               16  STORE_FAST               'session'

 L.  76        18  SETUP_FINALLY        54  'to 54'

 L.  77        20  LOAD_FAST                'service'
               22  LOAD_METHOD              call
               24  LOAD_STR                 'OpenSession'
               26  LOAD_STR                 'sv'

 L.  78        28  LOAD_GLOBAL              ALGORITHM_DH

 L.  79        30  LOAD_STR                 'ay'
               32  LOAD_GLOBAL              int_to_bytes
               34  LOAD_FAST                'session'
               36  LOAD_ATTR                my_public_key
               38  CALL_FUNCTION_1       1  ''
               40  BUILD_TUPLE_2         2 

 L.  77        42  CALL_METHOD_4         4  ''
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'output'
               48  STORE_FAST               'result'
               50  POP_BLOCK        
               52  JUMP_FORWARD        128  'to 128'
             54_0  COME_FROM_FINALLY    18  '18'

 L.  80        54  DUP_TOP          
               56  LOAD_GLOBAL              DBusErrorResponse
               58  <121>               126  ''
               60  POP_TOP          
               62  STORE_FAST               'resp'
               64  POP_TOP          
               66  SETUP_FINALLY       118  'to 118'

 L.  81        68  LOAD_FAST                'resp'
               70  LOAD_ATTR                name
               72  LOAD_GLOBAL              DBUS_NOT_SUPPORTED
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_FALSE    80  'to 80'

 L.  82        78  RAISE_VARARGS_0       0  'reraise'
             80_0  COME_FROM            76  '76'

 L.  83        80  LOAD_FAST                'service'
               82  LOAD_METHOD              call
               84  LOAD_STR                 'OpenSession'
               86  LOAD_STR                 'sv'

 L.  84        88  LOAD_GLOBAL              ALGORITHM_PLAIN

 L.  85        90  LOAD_CONST               ('s', '')

 L.  83        92  CALL_METHOD_4         4  ''
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'output'
               98  STORE_FAST               'result'

 L.  86       100  LOAD_CONST               False
              102  LOAD_FAST                'session'
              104  STORE_ATTR               encrypted
              106  POP_BLOCK        
              108  POP_EXCEPT       
              110  LOAD_CONST               None
              112  STORE_FAST               'resp'
              114  DELETE_FAST              'resp'
              116  JUMP_FORWARD        170  'to 170'
            118_0  COME_FROM_FINALLY    66  '66'
              118  LOAD_CONST               None
              120  STORE_FAST               'resp'
              122  DELETE_FAST              'resp'
              124  <48>             
              126  <48>             
            128_0  COME_FROM            52  '52'

 L.  88       128  LOAD_FAST                'output'
              130  UNPACK_SEQUENCE_2     2 
              132  STORE_FAST               'signature'
              134  STORE_FAST               'value'

 L.  89       136  LOAD_FAST                'signature'
              138  LOAD_STR                 'ay'
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_TRUE    148  'to 148'
              144  <74>             
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           142  '142'

 L.  90       148  LOAD_GLOBAL              int
              150  LOAD_METHOD              from_bytes
              152  LOAD_FAST                'value'
              154  LOAD_STR                 'big'
              156  CALL_METHOD_2         2  ''
              158  STORE_FAST               'key'

 L.  91       160  LOAD_FAST                'session'
              162  LOAD_METHOD              set_server_public_key
              164  LOAD_FAST                'key'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
            170_0  COME_FROM           116  '116'

 L.  92       170  LOAD_FAST                'result'
              172  LOAD_FAST                'session'
              174  STORE_ATTR               object_path

 L.  93       176  LOAD_FAST                'session'
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 58


def format_secret--- This code section failed: ---

 L.  99         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'secret'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 100        10  LOAD_FAST                'secret'
               12  LOAD_METHOD              encode
               14  LOAD_STR                 'utf-8'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'secret'
               20  JUMP_FORWARD         40  'to 40'
             22_0  COME_FROM             8  '8'

 L. 101        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'secret'
               26  LOAD_GLOBAL              bytes
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_TRUE     40  'to 40'

 L. 102        32  LOAD_GLOBAL              TypeError
               34  LOAD_STR                 'secret must be bytes'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'
             40_1  COME_FROM            20  '20'

 L. 103        40  LOAD_FAST                'session'
               42  LOAD_ATTR                object_path
               44  LOAD_CONST               None
               46  <117>                 1  ''
               48  POP_JUMP_IF_TRUE     54  'to 54'
               50  <74>             
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            48  '48'

 L. 104        54  LOAD_FAST                'session'
               56  LOAD_ATTR                encrypted
               58  POP_JUMP_IF_TRUE     74  'to 74'

 L. 105        60  LOAD_FAST                'session'
               62  LOAD_ATTR                object_path
               64  LOAD_CONST               b''
               66  LOAD_FAST                'secret'
               68  LOAD_FAST                'content_type'
               70  BUILD_TUPLE_4         4 
               72  RETURN_VALUE     
             74_0  COME_FROM            58  '58'

 L. 106        74  LOAD_FAST                'session'
               76  LOAD_ATTR                aes_key
               78  LOAD_CONST               None
               80  <117>                 1  ''
               82  POP_JUMP_IF_TRUE     88  'to 88'
               84  <74>             
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            82  '82'

 L. 108        88  LOAD_CONST               16
               90  LOAD_GLOBAL              len
               92  LOAD_FAST                'secret'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_CONST               15
               98  BINARY_AND       
              100  BINARY_SUBTRACT  
              102  STORE_FAST               'padding'

 L. 109       104  LOAD_FAST                'secret'
              106  LOAD_GLOBAL              bytes
              108  LOAD_FAST                'padding'
              110  BUILD_TUPLE_1         1 
              112  LOAD_FAST                'padding'
              114  BINARY_MULTIPLY  
              116  CALL_FUNCTION_1       1  ''
              118  INPLACE_ADD      
              120  STORE_FAST               'secret'

 L. 110       122  LOAD_GLOBAL              os
              124  LOAD_METHOD              urandom
              126  LOAD_CONST               16
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'aes_iv'

 L. 111       132  LOAD_GLOBAL              algorithms
              134  LOAD_METHOD              AES
              136  LOAD_FAST                'session'
              138  LOAD_ATTR                aes_key
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'aes'

 L. 112       144  LOAD_GLOBAL              Cipher
              146  LOAD_FAST                'aes'
              148  LOAD_GLOBAL              modes
              150  LOAD_METHOD              CBC
              152  LOAD_FAST                'aes_iv'
              154  CALL_METHOD_1         1  ''
              156  LOAD_GLOBAL              default_backend
              158  CALL_FUNCTION_0       0  ''
              160  CALL_FUNCTION_3       3  ''
              162  LOAD_METHOD              encryptor
              164  CALL_METHOD_0         0  ''
              166  STORE_FAST               'encryptor'

 L. 113       168  LOAD_FAST                'encryptor'
              170  LOAD_METHOD              update
              172  LOAD_FAST                'secret'
              174  CALL_METHOD_1         1  ''
              176  LOAD_FAST                'encryptor'
              178  LOAD_METHOD              finalize
              180  CALL_METHOD_0         0  ''
              182  BINARY_ADD       
              184  STORE_FAST               'encrypted_secret'

 L. 115       186  LOAD_FAST                'session'
              188  LOAD_ATTR                object_path

 L. 116       190  LOAD_FAST                'aes_iv'

 L. 117       192  LOAD_FAST                'encrypted_secret'

 L. 118       194  LOAD_FAST                'content_type'

 L. 114       196  BUILD_TUPLE_4         4 
              198  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 46


def exec_prompt--- This code section failed: ---

 L. 130         0  LOAD_GLOBAL              DBusAddressWrapper
                2  LOAD_FAST                'prompt_path'
                4  LOAD_GLOBAL              PROMPT_IFACE
                6  LOAD_FAST                'connection'
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'prompt'

 L. 131        12  LOAD_GLOBAL              MatchRule

 L. 132        14  LOAD_FAST                'prompt_path'

 L. 133        16  LOAD_GLOBAL              PROMPT_IFACE

 L. 134        18  LOAD_STR                 'Completed'

 L. 135        20  LOAD_GLOBAL              MessageType
               22  LOAD_ATTR                signal

 L. 131        24  LOAD_CONST               ('path', 'interface', 'member', 'type')
               26  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               28  STORE_FAST               'rule'

 L. 137        30  LOAD_FAST                'connection'
               32  LOAD_METHOD              filter
               34  LOAD_FAST                'rule'
               36  CALL_METHOD_1         1  ''
               38  SETUP_WITH           86  'to 86'
               40  STORE_FAST               'signals'

 L. 138        42  LOAD_FAST                'prompt'
               44  LOAD_METHOD              call
               46  LOAD_STR                 'Prompt'
               48  LOAD_STR                 's'
               50  LOAD_STR                 ''
               52  CALL_METHOD_3         3  ''
               54  POP_TOP          

 L. 139        56  LOAD_FAST                'connection'
               58  LOAD_METHOD              recv_until_filtered
               60  LOAD_FAST                'signals'
               62  CALL_METHOD_1         1  ''
               64  LOAD_ATTR                body
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'dismissed'
               70  STORE_FAST               'result'
               72  POP_BLOCK        
               74  LOAD_CONST               None
               76  DUP_TOP          
               78  DUP_TOP          
               80  CALL_FUNCTION_3       3  ''
               82  POP_TOP          
               84  JUMP_FORWARD        102  'to 102'
             86_0  COME_FROM_WITH       38  '38'
               86  <49>             
               88  POP_JUMP_IF_TRUE     92  'to 92'
               90  <48>             
             92_0  COME_FROM            88  '88'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          
               98  POP_EXCEPT       
              100  POP_TOP          
            102_0  COME_FROM            84  '84'

 L. 140       102  LOAD_FAST                'dismissed'
              104  LOAD_CONST               None
              106  <117>                 1  ''
              108  POP_JUMP_IF_TRUE    114  'to 114'
              110  <74>             
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           108  '108'

 L. 141       114  LOAD_FAST                'result'
              116  LOAD_CONST               None
              118  <117>                 1  ''
              120  POP_JUMP_IF_TRUE    126  'to 126'
              122  <74>             
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM           120  '120'

 L. 142       126  LOAD_FAST                'dismissed'
              128  LOAD_FAST                'result'
              130  BUILD_TUPLE_2         2 
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 76


def unlock_objects--- This code section failed: ---

 L. 150         0  LOAD_GLOBAL              DBusAddressWrapper
                2  LOAD_GLOBAL              SS_PATH
                4  LOAD_GLOBAL              SERVICE_IFACE
                6  LOAD_FAST                'connection'
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'service'

 L. 151        12  LOAD_FAST                'service'
               14  LOAD_METHOD              call
               16  LOAD_STR                 'Unlock'
               18  LOAD_STR                 'ao'
               20  LOAD_FAST                'paths'
               22  CALL_METHOD_3         3  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'unlocked_paths'
               28  STORE_FAST               'prompt'

 L. 152        30  LOAD_GLOBAL              len
               32  LOAD_FAST                'prompt'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_CONST               1
               38  COMPARE_OP               >
               40  POP_JUMP_IF_FALSE    76  'to 76'

 L. 153        42  LOAD_GLOBAL              exec_prompt
               44  LOAD_FAST                'connection'
               46  LOAD_FAST                'prompt'
               48  CALL_FUNCTION_2       2  ''
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'dismissed'
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'signature'
               58  STORE_FAST               'unlocked'

 L. 154        60  LOAD_FAST                'signature'
               62  LOAD_STR                 'ao'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_TRUE     72  'to 72'
               68  <74>             
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            66  '66'

 L. 155        72  LOAD_FAST                'dismissed'
               74  RETURN_VALUE     
             76_0  COME_FROM            40  '40'

 L. 156        76  LOAD_CONST               False
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 68


def add_match_rules(connection: DBusConnection) -> None:
    """Adds match rules for the given connection.

        Currently it matches all messages from the Prompt interface, as the
        mock service (unlike GNOME Keyring) does not specify the signal
        destination.

        .. versionadded:: 3.1
        """
    rule = MatchRule(sender=BUS_NAME, interface=PROMPT_IFACE)
    dbus = DBusAddressWrapper(path='/org/freedesktop/DBus', interface='org.freedesktop.DBus',
      connection=connection)
    dbus.bus_name = 'org.freedesktop.DBus'
    dbus.call('AddMatch', 's', rule.serialise)