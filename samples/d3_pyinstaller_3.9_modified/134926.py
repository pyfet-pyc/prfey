# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32ctypes\pywin32\win32cred.py
""" Interface to credentials management functions. """
from __future__ import absolute_import
from win32ctypes.core import _authentication, _common, _backend
import win32ctypes.pywin32.pywintypes as _pywin32error
CRED_TYPE_GENERIC = 1
CRED_PERSIST_SESSION = 1
CRED_PERSIST_LOCAL_MACHINE = 2
CRED_PERSIST_ENTERPRISE = 3
CRED_PRESERVE_CREDENTIAL_BLOB = 0

def CredWrite--- This code section failed: ---

 L.  34         0  LOAD_GLOBAL              _authentication
                2  LOAD_ATTR                CREDENTIAL
                4  LOAD_METHOD              fromdict
                6  LOAD_FAST                'Credential'
                8  LOAD_FAST                'Flags'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'c_creds'

 L.  35        14  LOAD_GLOBAL              _authentication
               16  LOAD_METHOD              PCREDENTIAL
               18  LOAD_FAST                'c_creds'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'c_pcreds'

 L.  36        24  LOAD_GLOBAL              _pywin32error
               26  CALL_FUNCTION_0       0  ''
               28  SETUP_WITH           58  'to 58'
               30  POP_TOP          

 L.  37        32  LOAD_GLOBAL              _authentication
               34  LOAD_METHOD              _CredWrite
               36  LOAD_FAST                'c_pcreds'
               38  LOAD_CONST               0
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          
               44  POP_BLOCK        
               46  LOAD_CONST               None
               48  DUP_TOP          
               50  DUP_TOP          
               52  CALL_FUNCTION_3       3  ''
               54  POP_TOP          
               56  JUMP_FORWARD         74  'to 74'
             58_0  COME_FROM_WITH       28  '28'
               58  <49>             
               60  POP_JUMP_IF_TRUE     64  'to 64'
               62  <48>             
             64_0  COME_FROM            60  '60'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          
               70  POP_EXCEPT       
               72  POP_TOP          
             74_0  COME_FROM            56  '56'

Parse error at or near `DUP_TOP' instruction at offset 48


def CredRead--- This code section failed: ---

 L.  59         0  LOAD_FAST                'Type'
                2  LOAD_GLOBAL              CRED_TYPE_GENERIC
                4  COMPARE_OP               !=
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  60         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Type != CRED_TYPE_GENERIC not yet supported'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  62        16  LOAD_CONST               0
               18  STORE_FAST               'flag'

 L.  63        20  LOAD_GLOBAL              _pywin32error
               22  CALL_FUNCTION_0       0  ''
               24  SETUP_WITH          116  'to 116'
               26  POP_TOP          

 L.  64        28  LOAD_GLOBAL              _backend
               30  LOAD_STR                 'cffi'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    72  'to 72'

 L.  65        36  LOAD_GLOBAL              _authentication
               38  LOAD_METHOD              PPCREDENTIAL
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'ppcreds'

 L.  66        44  LOAD_GLOBAL              _authentication
               46  LOAD_METHOD              _CredRead
               48  LOAD_FAST                'TargetName'
               50  LOAD_FAST                'Type'
               52  LOAD_FAST                'flag'
               54  LOAD_FAST                'ppcreds'
               56  CALL_METHOD_4         4  ''
               58  POP_TOP          

 L.  67        60  LOAD_GLOBAL              _common
               62  LOAD_METHOD              dereference
               64  LOAD_FAST                'ppcreds'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'pcreds'
               70  JUMP_FORWARD        102  'to 102'
             72_0  COME_FROM            34  '34'

 L.  69        72  LOAD_GLOBAL              _authentication
               74  LOAD_METHOD              PCREDENTIAL
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'pcreds'

 L.  70        80  LOAD_GLOBAL              _authentication
               82  LOAD_METHOD              _CredRead

 L.  71        84  LOAD_FAST                'TargetName'
               86  LOAD_FAST                'Type'
               88  LOAD_FAST                'flag'
               90  LOAD_GLOBAL              _common
               92  LOAD_METHOD              byreference
               94  LOAD_FAST                'pcreds'
               96  CALL_METHOD_1         1  ''

 L.  70        98  CALL_METHOD_4         4  ''
              100  POP_TOP          
            102_0  COME_FROM            70  '70'
              102  POP_BLOCK        
              104  LOAD_CONST               None
              106  DUP_TOP          
              108  DUP_TOP          
              110  CALL_FUNCTION_3       3  ''
              112  POP_TOP          
              114  JUMP_FORWARD        132  'to 132'
            116_0  COME_FROM_WITH       24  '24'
              116  <49>             
              118  POP_JUMP_IF_TRUE    122  'to 122'
              120  <48>             
            122_0  COME_FROM           118  '118'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          
              128  POP_EXCEPT       
              130  POP_TOP          
            132_0  COME_FROM           114  '114'

 L.  72       132  SETUP_FINALLY       162  'to 162'

 L.  73       134  LOAD_GLOBAL              _authentication
              136  LOAD_METHOD              credential2dict
              138  LOAD_GLOBAL              _common
              140  LOAD_METHOD              dereference
              142  LOAD_FAST                'pcreds'
              144  CALL_METHOD_1         1  ''
              146  CALL_METHOD_1         1  ''
              148  POP_BLOCK        

 L.  75       150  LOAD_GLOBAL              _authentication
              152  LOAD_METHOD              _CredFree
              154  LOAD_FAST                'pcreds'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          

 L.  73       160  RETURN_VALUE     
            162_0  COME_FROM_FINALLY   132  '132'

 L.  75       162  LOAD_GLOBAL              _authentication
              164  LOAD_METHOD              _CredFree
              166  LOAD_FAST                'pcreds'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  <48>             

Parse error at or near `DUP_TOP' instruction at offset 106


def CredDelete--- This code section failed: ---

 L.  91         0  LOAD_FAST                'Type'
                2  LOAD_GLOBAL              CRED_TYPE_GENERIC
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L.  92         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Type != CRED_TYPE_GENERIC not yet supported.'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  93        16  LOAD_GLOBAL              _pywin32error
               18  CALL_FUNCTION_0       0  ''
               20  SETUP_WITH           52  'to 52'
               22  POP_TOP          

 L.  94        24  LOAD_GLOBAL              _authentication
               26  LOAD_METHOD              _CredDelete
               28  LOAD_FAST                'TargetName'
               30  LOAD_FAST                'Type'
               32  LOAD_CONST               0
               34  CALL_METHOD_3         3  ''
               36  POP_TOP          
               38  POP_BLOCK        
               40  LOAD_CONST               None
               42  DUP_TOP          
               44  DUP_TOP          
               46  CALL_FUNCTION_3       3  ''
               48  POP_TOP          
               50  JUMP_FORWARD         68  'to 68'
             52_0  COME_FROM_WITH       20  '20'
               52  <49>             
               54  POP_JUMP_IF_TRUE     58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          
               64  POP_EXCEPT       
               66  POP_TOP          
             68_0  COME_FROM            50  '50'

Parse error at or near `DUP_TOP' instruction at offset 42