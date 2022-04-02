# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\util\connection.py
from __future__ import absolute_import
import socket
from .wait import NoWayToWaitForSocketError, wait_for_read
from ..contrib import _appengine_environ

def is_connection_dropped--- This code section failed: ---

 L.  17         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'conn'
                4  LOAD_STR                 'sock'
                6  LOAD_CONST               False
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'sock'

 L.  18        12  LOAD_FAST                'sock'
               14  LOAD_CONST               False
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  19        20  LOAD_CONST               False
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.  20        24  LOAD_FAST                'sock'
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L.  21        32  LOAD_CONST               True
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L.  22        36  SETUP_FINALLY        52  'to 52'

 L.  24        38  LOAD_GLOBAL              wait_for_read
               40  LOAD_FAST                'sock'
               42  LOAD_CONST               0.0
               44  LOAD_CONST               ('timeout',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    36  '36'

 L.  25        52  DUP_TOP          
               54  LOAD_GLOBAL              NoWayToWaitForSocketError
               56  <121>                70  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  26        64  POP_EXCEPT       
               66  LOAD_CONST               False
               68  RETURN_VALUE     
               70  <48>             

Parse error at or near `<117>' instruction at offset 16


def create_connection--- This code section failed: ---

 L.  47         0  LOAD_FAST                'address'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'host'
                6  STORE_FAST               'port'

 L.  48         8  LOAD_FAST                'host'
               10  LOAD_METHOD              startswith
               12  LOAD_STR                 '['
               14  CALL_METHOD_1         1  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L.  49        18  LOAD_FAST                'host'
               20  LOAD_METHOD              strip
               22  LOAD_STR                 '[]'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'host'
             28_0  COME_FROM            16  '16'

 L.  50        28  LOAD_CONST               None
               30  STORE_FAST               'err'

 L.  55        32  LOAD_GLOBAL              allowed_gai_family
               34  CALL_FUNCTION_0       0  ''
               36  STORE_FAST               'family'

 L.  57        38  LOAD_GLOBAL              socket
               40  LOAD_METHOD              getaddrinfo
               42  LOAD_FAST                'host'
               44  LOAD_FAST                'port'
               46  LOAD_FAST                'family'
               48  LOAD_GLOBAL              socket
               50  LOAD_ATTR                SOCK_STREAM
               52  CALL_METHOD_4         4  ''
               54  GET_ITER         
             56_0  COME_FROM           220  '220'
             56_1  COME_FROM           208  '208'
               56  FOR_ITER            222  'to 222'
               58  STORE_FAST               'res'

 L.  58        60  LOAD_FAST                'res'
               62  UNPACK_SEQUENCE_5     5 
               64  STORE_FAST               'af'
               66  STORE_FAST               'socktype'
               68  STORE_FAST               'proto'
               70  STORE_FAST               'canonname'
               72  STORE_FAST               'sa'

 L.  59        74  LOAD_CONST               None
               76  STORE_FAST               'sock'

 L.  60        78  SETUP_FINALLY       158  'to 158'

 L.  61        80  LOAD_GLOBAL              socket
               82  LOAD_METHOD              socket
               84  LOAD_FAST                'af'
               86  LOAD_FAST                'socktype'
               88  LOAD_FAST                'proto'
               90  CALL_METHOD_3         3  ''
               92  STORE_FAST               'sock'

 L.  64        94  LOAD_GLOBAL              _set_socket_options
               96  LOAD_FAST                'sock'
               98  LOAD_FAST                'socket_options'
              100  CALL_FUNCTION_2       2  ''
              102  POP_TOP          

 L.  66       104  LOAD_FAST                'timeout'
              106  LOAD_GLOBAL              socket
              108  LOAD_ATTR                _GLOBAL_DEFAULT_TIMEOUT
              110  <117>                 1  ''
              112  POP_JUMP_IF_FALSE   124  'to 124'

 L.  67       114  LOAD_FAST                'sock'
              116  LOAD_METHOD              settimeout
              118  LOAD_FAST                'timeout'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
            124_0  COME_FROM           112  '112'

 L.  68       124  LOAD_FAST                'source_address'
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L.  69       128  LOAD_FAST                'sock'
              130  LOAD_METHOD              bind
              132  LOAD_FAST                'source_address'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           126  '126'

 L.  70       138  LOAD_FAST                'sock'
              140  LOAD_METHOD              connect
              142  LOAD_FAST                'sa'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

 L.  71       148  LOAD_FAST                'sock'
              150  POP_BLOCK        
              152  ROT_TWO          
              154  POP_TOP          
              156  RETURN_VALUE     
            158_0  COME_FROM_FINALLY    78  '78'

 L.  73       158  DUP_TOP          
              160  LOAD_GLOBAL              socket
              162  LOAD_ATTR                error
              164  <121>               218  ''
              166  POP_TOP          
              168  STORE_FAST               'e'
              170  POP_TOP          
              172  SETUP_FINALLY       210  'to 210'

 L.  74       174  LOAD_FAST                'e'
              176  STORE_FAST               'err'

 L.  75       178  LOAD_FAST                'sock'
              180  LOAD_CONST               None
              182  <117>                 1  ''
              184  POP_JUMP_IF_FALSE   198  'to 198'

 L.  76       186  LOAD_FAST                'sock'
              188  LOAD_METHOD              close
              190  CALL_METHOD_0         0  ''
              192  POP_TOP          

 L.  77       194  LOAD_CONST               None
              196  STORE_FAST               'sock'
            198_0  COME_FROM           184  '184'
              198  POP_BLOCK        
              200  POP_EXCEPT       
              202  LOAD_CONST               None
              204  STORE_FAST               'e'
              206  DELETE_FAST              'e'
              208  JUMP_BACK            56  'to 56'
            210_0  COME_FROM_FINALLY   172  '172'
              210  LOAD_CONST               None
              212  STORE_FAST               'e'
              214  DELETE_FAST              'e'
              216  <48>             
              218  <48>             
              220  JUMP_BACK            56  'to 56'
            222_0  COME_FROM            56  '56'

 L.  79       222  LOAD_FAST                'err'
              224  LOAD_CONST               None
              226  <117>                 1  ''
              228  POP_JUMP_IF_FALSE   234  'to 234'

 L.  80       230  LOAD_FAST                'err'
              232  RAISE_VARARGS_1       1  'exception instance'
            234_0  COME_FROM           228  '228'

 L.  82       234  LOAD_GLOBAL              socket
              236  LOAD_METHOD              error
              238  LOAD_STR                 'getaddrinfo returns an empty list'
              240  CALL_METHOD_1         1  ''
              242  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 110


def _set_socket_options--- This code section failed: ---

 L.  86         0  LOAD_FAST                'options'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  87         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  89        12  LOAD_FAST                'options'
               14  GET_ITER         
             16_0  COME_FROM            30  '30'
               16  FOR_ITER             32  'to 32'
               18  STORE_FAST               'opt'

 L.  90        20  LOAD_FAST                'sock'
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

 L. 106         0  LOAD_CONST               None
                2  STORE_FAST               'sock'

 L. 107         4  LOAD_CONST               False
                6  STORE_FAST               'has_ipv6'

 L. 113         8  LOAD_GLOBAL              _appengine_environ
               10  LOAD_METHOD              is_appengine_sandbox
               12  CALL_METHOD_0         0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 114        16  LOAD_CONST               False
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 116        20  LOAD_GLOBAL              socket
               22  LOAD_ATTR                has_ipv6
               24  POP_JUMP_IF_FALSE    80  'to 80'

 L. 122        26  SETUP_FINALLY        62  'to 62'

 L. 123        28  LOAD_GLOBAL              socket
               30  LOAD_METHOD              socket
               32  LOAD_GLOBAL              socket
               34  LOAD_ATTR                AF_INET6
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'sock'

 L. 124        40  LOAD_FAST                'sock'
               42  LOAD_METHOD              bind
               44  LOAD_FAST                'host'
               46  LOAD_CONST               0
               48  BUILD_TUPLE_2         2 
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 125        54  LOAD_CONST               True
               56  STORE_FAST               'has_ipv6'
               58  POP_BLOCK        
               60  JUMP_FORWARD         80  'to 80'
             62_0  COME_FROM_FINALLY    26  '26'

 L. 126        62  DUP_TOP          
               64  LOAD_GLOBAL              Exception
               66  <121>                78  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 127        74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
               78  <48>             
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            60  '60'
             80_2  COME_FROM            24  '24'

 L. 129        80  LOAD_FAST                'sock'
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L. 130        84  LOAD_FAST                'sock'
               86  LOAD_METHOD              close
               88  CALL_METHOD_0         0  ''
               90  POP_TOP          
             92_0  COME_FROM            82  '82'

 L. 131        92  LOAD_FAST                'has_ipv6'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 66


HAS_IPV6 = _has_ipv6('::1')