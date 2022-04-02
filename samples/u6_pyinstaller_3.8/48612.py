# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\urllib3\util\connection.py
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
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  24        20  LOAD_CONST               False
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.  25        24  LOAD_FAST                'sock'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
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
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    72  'to 72'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  31        66  POP_EXCEPT       
               68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            58  '58'
               72  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 62


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
               52  JUMP_FORWARD         94  'to 94'
             54_0  COME_FROM_FINALLY    38  '38'

 L.  68        54  DUP_TOP          
               56  LOAD_GLOBAL              UnicodeError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    92  'to 92'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L.  69        68  LOAD_GLOBAL              six
               70  LOAD_METHOD              raise_from

 L.  70        72  LOAD_GLOBAL              LocationParseError
               74  LOAD_STR                 "'%s', label empty or too long"
               76  LOAD_FAST                'host'
               78  BINARY_MODULO    
               80  CALL_FUNCTION_1       1  ''

 L.  70        82  LOAD_CONST               None

 L.  69        84  CALL_METHOD_2         2  ''
               86  ROT_FOUR         
               88  POP_EXCEPT       
               90  RETURN_VALUE     
             92_0  COME_FROM            60  '60'
               92  END_FINALLY      
             94_0  COME_FROM            52  '52'

 L.  73        94  LOAD_GLOBAL              socket
               96  LOAD_METHOD              getaddrinfo
               98  LOAD_FAST                'host'
              100  LOAD_FAST                'port'
              102  LOAD_FAST                'family'
              104  LOAD_GLOBAL              socket
              106  LOAD_ATTR                SOCK_STREAM
              108  CALL_METHOD_4         4  ''
              110  GET_ITER         
              112  FOR_ITER            280  'to 280'
              114  STORE_FAST               'res'

 L.  74       116  LOAD_FAST                'res'
              118  UNPACK_SEQUENCE_5     5 
              120  STORE_FAST               'af'
              122  STORE_FAST               'socktype'
              124  STORE_FAST               'proto'
              126  STORE_FAST               'canonname'
              128  STORE_FAST               'sa'

 L.  75       130  LOAD_CONST               None
              132  STORE_FAST               'sock'

 L.  76       134  SETUP_FINALLY       214  'to 214'

 L.  77       136  LOAD_GLOBAL              socket
              138  LOAD_METHOD              socket
              140  LOAD_FAST                'af'
              142  LOAD_FAST                'socktype'
              144  LOAD_FAST                'proto'
              146  CALL_METHOD_3         3  ''
              148  STORE_FAST               'sock'

 L.  80       150  LOAD_GLOBAL              _set_socket_options
              152  LOAD_FAST                'sock'
              154  LOAD_FAST                'socket_options'
              156  CALL_FUNCTION_2       2  ''
              158  POP_TOP          

 L.  82       160  LOAD_FAST                'timeout'
              162  LOAD_GLOBAL              socket
              164  LOAD_ATTR                _GLOBAL_DEFAULT_TIMEOUT
              166  COMPARE_OP               is-not
              168  POP_JUMP_IF_FALSE   180  'to 180'

 L.  83       170  LOAD_FAST                'sock'
              172  LOAD_METHOD              settimeout
              174  LOAD_FAST                'timeout'
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          
            180_0  COME_FROM           168  '168'

 L.  84       180  LOAD_FAST                'source_address'
              182  POP_JUMP_IF_FALSE   194  'to 194'

 L.  85       184  LOAD_FAST                'sock'
              186  LOAD_METHOD              bind
              188  LOAD_FAST                'source_address'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
            194_0  COME_FROM           182  '182'

 L.  86       194  LOAD_FAST                'sock'
              196  LOAD_METHOD              connect
              198  LOAD_FAST                'sa'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          

 L.  87       204  LOAD_FAST                'sock'
              206  POP_BLOCK        
              208  ROT_TWO          
              210  POP_TOP          
              212  RETURN_VALUE     
            214_0  COME_FROM_FINALLY   134  '134'

 L.  89       214  DUP_TOP          
              216  LOAD_GLOBAL              socket
              218  LOAD_ATTR                error
              220  COMPARE_OP               exception-match
          222_224  POP_JUMP_IF_FALSE   276  'to 276'
              226  POP_TOP          
              228  STORE_FAST               'e'
              230  POP_TOP          
              232  SETUP_FINALLY       264  'to 264'

 L.  90       234  LOAD_FAST                'e'
              236  STORE_FAST               'err'

 L.  91       238  LOAD_FAST                'sock'
              240  LOAD_CONST               None
              242  COMPARE_OP               is-not
          244_246  POP_JUMP_IF_FALSE   260  'to 260'

 L.  92       248  LOAD_FAST                'sock'
              250  LOAD_METHOD              close
              252  CALL_METHOD_0         0  ''
              254  POP_TOP          

 L.  93       256  LOAD_CONST               None
              258  STORE_FAST               'sock'
            260_0  COME_FROM           244  '244'
              260  POP_BLOCK        
              262  BEGIN_FINALLY    
            264_0  COME_FROM_FINALLY   232  '232'
              264  LOAD_CONST               None
              266  STORE_FAST               'e'
              268  DELETE_FAST              'e'
              270  END_FINALLY      
              272  POP_EXCEPT       
              274  JUMP_BACK           112  'to 112'
            276_0  COME_FROM           222  '222'
              276  END_FINALLY      
              278  JUMP_BACK           112  'to 112'

 L.  95       280  LOAD_FAST                'err'
              282  LOAD_CONST               None
              284  COMPARE_OP               is-not
          286_288  POP_JUMP_IF_FALSE   294  'to 294'

 L.  96       290  LOAD_FAST                'err'
              292  RAISE_VARARGS_1       1  'exception instance'
            294_0  COME_FROM           286  '286'

 L.  98       294  LOAD_GLOBAL              socket
              296  LOAD_METHOD              error
              298  LOAD_STR                 'getaddrinfo returns an empty list'
              300  CALL_METHOD_1         1  ''
              302  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 208


def _set_socket_options(sock, options):
    if options is None:
        return
    for opt in options:
        (sock.setsockopt)(*opt)


def allowed_gai_family():
    """This function is designed to work in the context of
    getaddrinfo, where family=socket.AF_UNSPEC is the default and
    will perform a DNS search for both IPv6 and IPv4 records."""
    family = socket.AF_INET
    if HAS_IPV6:
        family = socket.AF_UNSPEC
    return family


def _has_ipv6(host):
    """ Returns True if the system can bind an IPv6 address. """
    sock = None
    has_ipv6 = False
    if _appengine_environ.is_appengine_sandbox:
        return False
    if socket.has_ipv6:
        try:
            sock = socket.socketsocket.AF_INET6
            sock.bind(host, 0)
            has_ipv6 = True
        except Exception:
            pass

    if sock:
        sock.close
    return has_ipv6


HAS_IPV6 = _has_ipv6('::1')