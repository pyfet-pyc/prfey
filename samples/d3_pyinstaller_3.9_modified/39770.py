# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\util\connection.py
from __future__ import absolute_import
import socket
from urllib3.exceptions import LocationParseError
from ..contrib import _appengine_environ
from ..packages import six
from .wait import NoWayToWaitForSocketError, wait_for_read

def is_connection_dropped--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'conn'
                4  LOAD_STR                 'sock'
                6  LOAD_CONST               False
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'sock'

 L.  23        12  LOAD_FAST                'sock'
               14  LOAD_CONST               False
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  24        20  LOAD_CONST               False
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.  25        24  LOAD_FAST                'sock'
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L.  26        32  LOAD_CONST               True
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L.  27        36  SETUP_FINALLY        52  'to 52'

 L.  29        38  LOAD_GLOBAL              wait_for_read
               40  LOAD_FAST                'sock'
               42  LOAD_CONST               0.0
               44  LOAD_CONST               ('timeout',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    36  '36'

 L.  30        52  DUP_TOP          
               54  LOAD_GLOBAL              NoWayToWaitForSocketError
               56  <121>                70  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  31        64  POP_EXCEPT       
               66  LOAD_CONST               False
               68  RETURN_VALUE     
               70  <48>             

Parse error at or near `<117>' instruction at offset 16


def create_connection--- This code section failed: ---

 L.  56         0  LOAD_FAST                'address'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'host'
                6  STORE_FAST               'port'

 L.  57         8  LOAD_FAST                'host'
               10  LOAD_METHOD              startswith
               12  LOAD_STR                 '['
               14  CALL_METHOD_1         1  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L.  58        18  LOAD_FAST                'host'
               20  LOAD_METHOD              strip
               22  LOAD_STR                 '[]'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'host'
             28_0  COME_FROM            16  '16'

 L.  59        28  LOAD_CONST               None
               30  STORE_FAST               'err'

 L.  64        32  LOAD_GLOBAL              allowed_gai_family
               34  CALL_FUNCTION_0       0  ''
               36  STORE_FAST               'family'

 L.  66        38  SETUP_FINALLY        54  'to 54'

 L.  67        40  LOAD_FAST                'host'
               42  LOAD_METHOD              encode
               44  LOAD_STR                 'idna'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  POP_BLOCK        
               52  JUMP_FORWARD         92  'to 92'
             54_0  COME_FROM_FINALLY    38  '38'

 L.  68        54  DUP_TOP          
               56  LOAD_GLOBAL              UnicodeError
               58  <121>                90  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  69        66  LOAD_GLOBAL              six
               68  LOAD_METHOD              raise_from

 L.  70        70  LOAD_GLOBAL              LocationParseError
               72  LOAD_STR                 "'%s', label empty or too long"
               74  LOAD_FAST                'host'
               76  BINARY_MODULO    
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_CONST               None

 L.  69        82  CALL_METHOD_2         2  ''
               84  ROT_FOUR         
               86  POP_EXCEPT       
               88  RETURN_VALUE     
               90  <48>             
             92_0  COME_FROM            52  '52'

 L.  73        92  LOAD_GLOBAL              socket
               94  LOAD_METHOD              getaddrinfo
               96  LOAD_FAST                'host'
               98  LOAD_FAST                'port'
              100  LOAD_FAST                'family'
              102  LOAD_GLOBAL              socket
              104  LOAD_ATTR                SOCK_STREAM
              106  CALL_METHOD_4         4  ''
              108  GET_ITER         
            110_0  COME_FROM           278  '278'
            110_1  COME_FROM           266  '266'
              110  FOR_ITER            280  'to 280'
              112  STORE_FAST               'res'

 L.  74       114  LOAD_FAST                'res'
              116  UNPACK_SEQUENCE_5     5 
              118  STORE_FAST               'af'
              120  STORE_FAST               'socktype'
              122  STORE_FAST               'proto'
              124  STORE_FAST               'canonname'
              126  STORE_FAST               'sa'

 L.  75       128  LOAD_CONST               None
              130  STORE_FAST               'sock'

 L.  76       132  SETUP_FINALLY       212  'to 212'

 L.  77       134  LOAD_GLOBAL              socket
              136  LOAD_METHOD              socket
              138  LOAD_FAST                'af'
              140  LOAD_FAST                'socktype'
              142  LOAD_FAST                'proto'
              144  CALL_METHOD_3         3  ''
              146  STORE_FAST               'sock'

 L.  80       148  LOAD_GLOBAL              _set_socket_options
              150  LOAD_FAST                'sock'
              152  LOAD_FAST                'socket_options'
              154  CALL_FUNCTION_2       2  ''
              156  POP_TOP          

 L.  82       158  LOAD_FAST                'timeout'
              160  LOAD_GLOBAL              socket
              162  LOAD_ATTR                _GLOBAL_DEFAULT_TIMEOUT
              164  <117>                 1  ''
              166  POP_JUMP_IF_FALSE   178  'to 178'

 L.  83       168  LOAD_FAST                'sock'
              170  LOAD_METHOD              settimeout
              172  LOAD_FAST                'timeout'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
            178_0  COME_FROM           166  '166'

 L.  84       178  LOAD_FAST                'source_address'
              180  POP_JUMP_IF_FALSE   192  'to 192'

 L.  85       182  LOAD_FAST                'sock'
              184  LOAD_METHOD              bind
              186  LOAD_FAST                'source_address'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          
            192_0  COME_FROM           180  '180'

 L.  86       192  LOAD_FAST                'sock'
              194  LOAD_METHOD              connect
              196  LOAD_FAST                'sa'
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L.  87       202  LOAD_FAST                'sock'
              204  POP_BLOCK        
              206  ROT_TWO          
              208  POP_TOP          
              210  RETURN_VALUE     
            212_0  COME_FROM_FINALLY   132  '132'

 L.  89       212  DUP_TOP          
              214  LOAD_GLOBAL              socket
              216  LOAD_ATTR                error
          218_220  <121>               276  ''
              222  POP_TOP          
              224  STORE_FAST               'e'
              226  POP_TOP          
              228  SETUP_FINALLY       268  'to 268'

 L.  90       230  LOAD_FAST                'e'
              232  STORE_FAST               'err'

 L.  91       234  LOAD_FAST                'sock'
              236  LOAD_CONST               None
              238  <117>                 1  ''
          240_242  POP_JUMP_IF_FALSE   256  'to 256'

 L.  92       244  LOAD_FAST                'sock'
              246  LOAD_METHOD              close
              248  CALL_METHOD_0         0  ''
              250  POP_TOP          

 L.  93       252  LOAD_CONST               None
              254  STORE_FAST               'sock'
            256_0  COME_FROM           240  '240'
              256  POP_BLOCK        
              258  POP_EXCEPT       
              260  LOAD_CONST               None
              262  STORE_FAST               'e'
              264  DELETE_FAST              'e'
              266  JUMP_BACK           110  'to 110'
            268_0  COME_FROM_FINALLY   228  '228'
              268  LOAD_CONST               None
              270  STORE_FAST               'e'
              272  DELETE_FAST              'e'
              274  <48>             
              276  <48>             
              278  JUMP_BACK           110  'to 110'
            280_0  COME_FROM           110  '110'

 L.  95       280  LOAD_FAST                'err'
              282  LOAD_CONST               None
              284  <117>                 1  ''
          286_288  POP_JUMP_IF_FALSE   294  'to 294'

 L.  96       290  LOAD_FAST                'err'
              292  RAISE_VARARGS_1       1  'exception instance'
            294_0  COME_FROM           286  '286'

 L.  98       294  LOAD_GLOBAL              socket
              296  LOAD_METHOD              error
              298  LOAD_STR                 'getaddrinfo returns an empty list'
              300  CALL_METHOD_1         1  ''
              302  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 58


def _set_socket_options--- This code section failed: ---

 L. 102         0  LOAD_FAST                'options'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 103         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 105        12  LOAD_FAST                'options'
               14  GET_ITER         
             16_0  COME_FROM            30  '30'
               16  FOR_ITER             32  'to 32'
               18  STORE_FAST               'opt'

 L. 106        20  LOAD_FAST                'sock'
               22  LOAD_ATTR                setsockopt
               24  LOAD_FAST                'opt'
               26  CALL_FUNCTION_EX      0  'positional arguments only'
               28  POP_TOP          
               30  JUMP_BACK            16  'to 16'
             32_0  COME_FROM            16  '16'

Parse error at or near `None' instruction at offset -1


def allowed_gai_family():
    """This function is designed to work in the context of
    getaddrinfo, where family=socket.AF_UNSPEC is the default and
    will perform a DNS search for both IPv6 and IPv4 records."""
    family = socket.AF_INET
    if HAS_IPV6:
        family = socket.AF_UNSPEC
    return family


def _has_ipv6--- This code section failed: ---

 L. 122         0  LOAD_CONST               None
                2  STORE_FAST               'sock'

 L. 123         4  LOAD_CONST               False
                6  STORE_FAST               'has_ipv6'

 L. 129         8  LOAD_GLOBAL              _appengine_environ
               10  LOAD_METHOD              is_appengine_sandbox
               12  CALL_METHOD_0         0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 130        16  LOAD_CONST               False
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 132        20  LOAD_GLOBAL              socket
               22  LOAD_ATTR                has_ipv6
               24  POP_JUMP_IF_FALSE    80  'to 80'

 L. 138        26  SETUP_FINALLY        62  'to 62'

 L. 139        28  LOAD_GLOBAL              socket
               30  LOAD_METHOD              socket
               32  LOAD_GLOBAL              socket
               34  LOAD_ATTR                AF_INET6
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'sock'

 L. 140        40  LOAD_FAST                'sock'
               42  LOAD_METHOD              bind
               44  LOAD_FAST                'host'
               46  LOAD_CONST               0
               48  BUILD_TUPLE_2         2 
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 141        54  LOAD_CONST               True
               56  STORE_FAST               'has_ipv6'
               58  POP_BLOCK        
               60  JUMP_FORWARD         80  'to 80'
             62_0  COME_FROM_FINALLY    26  '26'

 L. 142        62  DUP_TOP          
               64  LOAD_GLOBAL              Exception
               66  <121>                78  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 143        74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
               78  <48>             
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            60  '60'
             80_2  COME_FROM            24  '24'

 L. 145        80  LOAD_FAST                'sock'
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L. 146        84  LOAD_FAST                'sock'
               86  LOAD_METHOD              close
               88  CALL_METHOD_0         0  ''
               90  POP_TOP          
             92_0  COME_FROM            82  '82'

 L. 147        92  LOAD_FAST                'has_ipv6'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 66


HAS_IPV6 = _has_ipv6('::1')