# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\urllib3\util\connection.py
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
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  19        20  LOAD_CONST               False
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.  20        24  LOAD_FAST                'sock'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
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
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    72  'to 72'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  26        66  POP_EXCEPT       
               68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            58  '58'
               72  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 62


def create_connection--- This code section failed: ---

 L.  51         0  LOAD_FAST                'address'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'host'
                6  STORE_FAST               'port'

 L.  52         8  LOAD_FAST                'host'
               10  LOAD_METHOD              startswith
               12  LOAD_STR                 '['
               14  CALL_METHOD_1         1  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L.  53        18  LOAD_FAST                'host'
               20  LOAD_METHOD              strip
               22  LOAD_STR                 '[]'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'host'
             28_0  COME_FROM            16  '16'

 L.  54        28  LOAD_CONST               None
               30  STORE_FAST               'err'

 L.  59        32  LOAD_GLOBAL              allowed_gai_family
               34  CALL_FUNCTION_0       0  ''
               36  STORE_FAST               'family'

 L.  61        38  LOAD_GLOBAL              socket
               40  LOAD_METHOD              getaddrinfo
               42  LOAD_FAST                'host'
               44  LOAD_FAST                'port'
               46  LOAD_FAST                'family'
               48  LOAD_GLOBAL              socket
               50  LOAD_ATTR                SOCK_STREAM
               52  CALL_METHOD_4         4  ''
               54  GET_ITER         
               56  FOR_ITER            220  'to 220'
               58  STORE_FAST               'res'

 L.  62        60  LOAD_FAST                'res'
               62  UNPACK_SEQUENCE_5     5 
               64  STORE_FAST               'af'
               66  STORE_FAST               'socktype'
               68  STORE_FAST               'proto'
               70  STORE_FAST               'canonname'
               72  STORE_FAST               'sa'

 L.  63        74  LOAD_CONST               None
               76  STORE_FAST               'sock'

 L.  64        78  SETUP_FINALLY       158  'to 158'

 L.  65        80  LOAD_GLOBAL              socket
               82  LOAD_METHOD              socket
               84  LOAD_FAST                'af'
               86  LOAD_FAST                'socktype'
               88  LOAD_FAST                'proto'
               90  CALL_METHOD_3         3  ''
               92  STORE_FAST               'sock'

 L.  68        94  LOAD_GLOBAL              _set_socket_options
               96  LOAD_FAST                'sock'
               98  LOAD_FAST                'socket_options'
              100  CALL_FUNCTION_2       2  ''
              102  POP_TOP          

 L.  70       104  LOAD_FAST                'timeout'
              106  LOAD_GLOBAL              socket
              108  LOAD_ATTR                _GLOBAL_DEFAULT_TIMEOUT
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_FALSE   124  'to 124'

 L.  71       114  LOAD_FAST                'sock'
              116  LOAD_METHOD              settimeout
              118  LOAD_FAST                'timeout'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
            124_0  COME_FROM           112  '112'

 L.  72       124  LOAD_FAST                'source_address'
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L.  73       128  LOAD_FAST                'sock'
              130  LOAD_METHOD              bind
              132  LOAD_FAST                'source_address'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           126  '126'

 L.  74       138  LOAD_FAST                'sock'
              140  LOAD_METHOD              connect
              142  LOAD_FAST                'sa'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

 L.  75       148  LOAD_FAST                'sock'
              150  POP_BLOCK        
              152  ROT_TWO          
              154  POP_TOP          
              156  RETURN_VALUE     
            158_0  COME_FROM_FINALLY    78  '78'

 L.  77       158  DUP_TOP          
              160  LOAD_GLOBAL              socket
              162  LOAD_ATTR                error
              164  COMPARE_OP               exception-match
              166  POP_JUMP_IF_FALSE   216  'to 216'
              168  POP_TOP          
              170  STORE_FAST               'e'
              172  POP_TOP          
              174  SETUP_FINALLY       204  'to 204'

 L.  78       176  LOAD_FAST                'e'
              178  STORE_FAST               'err'

 L.  79       180  LOAD_FAST                'sock'
              182  LOAD_CONST               None
              184  COMPARE_OP               is-not
              186  POP_JUMP_IF_FALSE   200  'to 200'

 L.  80       188  LOAD_FAST                'sock'
              190  LOAD_METHOD              close
              192  CALL_METHOD_0         0  ''
              194  POP_TOP          

 L.  81       196  LOAD_CONST               None
              198  STORE_FAST               'sock'
            200_0  COME_FROM           186  '186'
              200  POP_BLOCK        
              202  BEGIN_FINALLY    
            204_0  COME_FROM_FINALLY   174  '174'
              204  LOAD_CONST               None
              206  STORE_FAST               'e'
              208  DELETE_FAST              'e'
              210  END_FINALLY      
              212  POP_EXCEPT       
              214  JUMP_BACK            56  'to 56'
            216_0  COME_FROM           166  '166'
              216  END_FINALLY      
              218  JUMP_BACK            56  'to 56'

 L.  83       220  LOAD_FAST                'err'
              222  LOAD_CONST               None
              224  COMPARE_OP               is-not
              226  POP_JUMP_IF_FALSE   232  'to 232'

 L.  84       228  LOAD_FAST                'err'
              230  RAISE_VARARGS_1       1  'exception instance'
            232_0  COME_FROM           226  '226'

 L.  86       232  LOAD_GLOBAL              socket
              234  LOAD_METHOD              error
              236  LOAD_STR                 'getaddrinfo returns an empty list'
              238  CALL_METHOD_1         1  ''
              240  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 152


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