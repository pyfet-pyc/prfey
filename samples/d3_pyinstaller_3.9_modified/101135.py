# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\proactor_events.py
"""Event loop using a proactor and related classes.

A proactor is a "notify-on-completion" multiplexer.  Currently a
proactor is only implemented on Windows with IOCP.
"""
__all__ = ('BaseProactorEventLoop', )
import io, os, socket, warnings, signal, threading, collections
from . import base_events
from . import constants
from . import futures
from . import exceptions
from . import protocols
from . import sslproto
from . import transports
from . import trsock
from .log import logger

def _set_socket_extra--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL              trsock
                2  LOAD_METHOD              TransportSocket
                4  LOAD_FAST                'sock'
                6  CALL_METHOD_1         1  ''
                8  LOAD_FAST                'transport'
               10  LOAD_ATTR                _extra
               12  LOAD_STR                 'socket'
               14  STORE_SUBSCR     

 L.  31        16  SETUP_FINALLY        36  'to 36'

 L.  32        18  LOAD_FAST                'sock'
               20  LOAD_METHOD              getsockname
               22  CALL_METHOD_0         0  ''
               24  LOAD_FAST                'transport'
               26  LOAD_ATTR                _extra
               28  LOAD_STR                 'sockname'
               30  STORE_SUBSCR     
               32  POP_BLOCK        
               34  JUMP_FORWARD         82  'to 82'
             36_0  COME_FROM_FINALLY    16  '16'

 L.  33        36  DUP_TOP          
               38  LOAD_GLOBAL              socket
               40  LOAD_ATTR                error
               42  <121>                80  ''
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L.  34        50  LOAD_FAST                'transport'
               52  LOAD_ATTR                _loop
               54  LOAD_METHOD              get_debug
               56  CALL_METHOD_0         0  ''
               58  POP_JUMP_IF_FALSE    76  'to 76'

 L.  35        60  LOAD_GLOBAL              logger
               62  LOAD_ATTR                warning

 L.  36        64  LOAD_STR                 'getsockname() failed on %r'
               66  LOAD_FAST                'sock'
               68  LOAD_CONST               True

 L.  35        70  LOAD_CONST               ('exc_info',)
               72  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               74  POP_TOP          
             76_0  COME_FROM            58  '58'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
               80  <48>             
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            34  '34'

 L.  38        82  LOAD_STR                 'peername'
               84  LOAD_FAST                'transport'
               86  LOAD_ATTR                _extra
               88  <118>                 1  ''
               90  POP_JUMP_IF_FALSE   142  'to 142'

 L.  39        92  SETUP_FINALLY       112  'to 112'

 L.  40        94  LOAD_FAST                'sock'
               96  LOAD_METHOD              getpeername
               98  CALL_METHOD_0         0  ''
              100  LOAD_FAST                'transport'
              102  LOAD_ATTR                _extra
              104  LOAD_STR                 'peername'
              106  STORE_SUBSCR     
              108  POP_BLOCK        
              110  JUMP_FORWARD        142  'to 142'
            112_0  COME_FROM_FINALLY    92  '92'

 L.  41       112  DUP_TOP          
              114  LOAD_GLOBAL              socket
              116  LOAD_ATTR                error
              118  <121>               140  ''
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L.  43       126  LOAD_CONST               None
              128  LOAD_FAST                'transport'
              130  LOAD_ATTR                _extra
              132  LOAD_STR                 'peername'
              134  STORE_SUBSCR     
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
              140  <48>             
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM           110  '110'
            142_2  COME_FROM            90  '90'

Parse error at or near `<121>' instruction at offset 42


class _ProactorBasePipeTransport(transports._FlowControlMixin, transports.BaseTransport):
    __doc__ = 'Base class for pipe and socket transports.'

    def __init__--- This code section failed: ---

 L.  52         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __init__
                6  LOAD_FAST                'extra'
                8  LOAD_FAST                'loop'
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L.  53        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _set_extra
               18  LOAD_FAST                'sock'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L.  54        24  LOAD_FAST                'sock'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _sock

 L.  55        30  LOAD_FAST                'self'
               32  LOAD_METHOD              set_protocol
               34  LOAD_FAST                'protocol'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L.  56        40  LOAD_FAST                'server'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _server

 L.  57        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _buffer

 L.  58        52  LOAD_CONST               None
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _read_fut

 L.  59        58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _write_fut

 L.  60        64  LOAD_CONST               0
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _pending_write

 L.  61        70  LOAD_CONST               0
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _conn_lost

 L.  62        76  LOAD_CONST               False
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _closing

 L.  63        82  LOAD_CONST               False
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _eof_written

 L.  64        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _server
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   108  'to 108'

 L.  65        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _server
              102  LOAD_METHOD              _attach
              104  CALL_METHOD_0         0  ''
              106  POP_TOP          
            108_0  COME_FROM            96  '96'

 L.  66       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _loop
              112  LOAD_METHOD              call_soon
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _protocol
              118  LOAD_ATTR                connection_made
              120  LOAD_FAST                'self'
              122  CALL_METHOD_2         2  ''
              124  POP_TOP          

 L.  67       126  LOAD_FAST                'waiter'
              128  LOAD_CONST               None
              130  <117>                 1  ''
              132  POP_JUMP_IF_FALSE   152  'to 152'

 L.  69       134  LOAD_FAST                'self'
              136  LOAD_ATTR                _loop
              138  LOAD_METHOD              call_soon
              140  LOAD_GLOBAL              futures
              142  LOAD_ATTR                _set_result_unless_cancelled

 L.  70       144  LOAD_FAST                'waiter'
              146  LOAD_CONST               None

 L.  69       148  CALL_METHOD_3         3  ''
              150  POP_TOP          
            152_0  COME_FROM           132  '132'

Parse error at or near `<117>' instruction at offset 94

    def __repr__--- This code section failed: ---

 L.  73         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_ATTR                __name__
                6  BUILD_LIST_1          1 
                8  STORE_FAST               'info'

 L.  74        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L.  75        20  LOAD_FAST                'info'
               22  LOAD_METHOD              append
               24  LOAD_STR                 'closed'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
               30  JUMP_FORWARD         48  'to 48'
             32_0  COME_FROM            18  '18'

 L.  76        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _closing
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L.  77        38  LOAD_FAST                'info'
               40  LOAD_METHOD              append
               42  LOAD_STR                 'closing'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            36  '36'
             48_1  COME_FROM            30  '30'

 L.  78        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _sock
               52  LOAD_CONST               None
               54  <117>                 1  ''
               56  POP_JUMP_IF_FALSE    80  'to 80'

 L.  79        58  LOAD_FAST                'info'
               60  LOAD_METHOD              append
               62  LOAD_STR                 'fd='
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _sock
               68  LOAD_METHOD              fileno
               70  CALL_METHOD_0         0  ''
               72  FORMAT_VALUE          0  ''
               74  BUILD_STRING_2        2 
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
             80_0  COME_FROM            56  '56'

 L.  80        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _read_fut
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE   108  'to 108'

 L.  81        90  LOAD_FAST                'info'
               92  LOAD_METHOD              append
               94  LOAD_STR                 'read='
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _read_fut
              100  FORMAT_VALUE          2  '!r'
              102  BUILD_STRING_2        2 
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
            108_0  COME_FROM            88  '88'

 L.  82       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _write_fut
              112  LOAD_CONST               None
              114  <117>                 1  ''
              116  POP_JUMP_IF_FALSE   136  'to 136'

 L.  83       118  LOAD_FAST                'info'
              120  LOAD_METHOD              append
              122  LOAD_STR                 'write='
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _write_fut
              128  FORMAT_VALUE          2  '!r'
              130  BUILD_STRING_2        2 
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
            136_0  COME_FROM           116  '116'

 L.  84       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _buffer
              140  POP_JUMP_IF_FALSE   164  'to 164'

 L.  85       142  LOAD_FAST                'info'
              144  LOAD_METHOD              append
              146  LOAD_STR                 'write_bufsize='
              148  LOAD_GLOBAL              len
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                _buffer
              154  CALL_FUNCTION_1       1  ''
              156  FORMAT_VALUE          0  ''
              158  BUILD_STRING_2        2 
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
            164_0  COME_FROM           140  '140'

 L.  86       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _eof_written
              168  POP_JUMP_IF_FALSE   180  'to 180'

 L.  87       170  LOAD_FAST                'info'
              172  LOAD_METHOD              append
              174  LOAD_STR                 'EOF written'
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          
            180_0  COME_FROM           168  '168'

 L.  88       180  LOAD_STR                 '<{}>'
              182  LOAD_METHOD              format
              184  LOAD_STR                 ' '
              186  LOAD_METHOD              join
              188  LOAD_FAST                'info'
              190  CALL_METHOD_1         1  ''
              192  CALL_METHOD_1         1  ''
              194  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def _set_extra(self, sock):
        self._extra['pipe'] = sock

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def is_closing(self):
        return self._closing

    def close--- This code section failed: ---

 L. 103         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _closing
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 104         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 105        10  LOAD_CONST               True
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _closing

 L. 106        16  LOAD_FAST                'self'
               18  DUP_TOP          
               20  LOAD_ATTR                _conn_lost
               22  LOAD_CONST               1
               24  INPLACE_ADD      
               26  ROT_TWO          
               28  STORE_ATTR               _conn_lost

 L. 107        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _buffer
               34  POP_JUMP_IF_TRUE     62  'to 62'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _write_fut
               40  LOAD_CONST               None
               42  <117>                 0  ''
               44  POP_JUMP_IF_FALSE    62  'to 62'

 L. 108        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _loop
               50  LOAD_METHOD              call_soon
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _call_connection_lost
               56  LOAD_CONST               None
               58  CALL_METHOD_2         2  ''
               60  POP_TOP          
             62_0  COME_FROM            44  '44'
             62_1  COME_FROM            34  '34'

 L. 109        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _read_fut
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    88  'to 88'

 L. 110        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _read_fut
               76  LOAD_METHOD              cancel
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          

 L. 111        82  LOAD_CONST               None
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _read_fut
             88_0  COME_FROM            70  '70'

Parse error at or near `<117>' instruction at offset 42

    def __del__--- This code section failed: ---

 L. 114         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _sock
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    38  'to 38'

 L. 115        10  LOAD_FAST                '_warn'
               12  LOAD_STR                 'unclosed transport '
               14  LOAD_FAST                'self'
               16  FORMAT_VALUE          2  '!r'
               18  BUILD_STRING_2        2 
               20  LOAD_GLOBAL              ResourceWarning
               22  LOAD_FAST                'self'
               24  LOAD_CONST               ('source',)
               26  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               28  POP_TOP          

 L. 116        30  LOAD_FAST                'self'
               32  LOAD_METHOD              close
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          
             38_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def _fatal_error--- This code section failed: ---

 L. 119         0  SETUP_FINALLY        80  'to 80'

 L. 120         2  LOAD_GLOBAL              isinstance
                4  LOAD_FAST                'exc'
                6  LOAD_GLOBAL              OSError
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    42  'to 42'

 L. 121        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _loop
               16  LOAD_METHOD              get_debug
               18  CALL_METHOD_0         0  ''
               20  POP_JUMP_IF_FALSE    66  'to 66'

 L. 122        22  LOAD_GLOBAL              logger
               24  LOAD_ATTR                debug
               26  LOAD_STR                 '%r: %s'
               28  LOAD_FAST                'self'
               30  LOAD_FAST                'message'
               32  LOAD_CONST               True
               34  LOAD_CONST               ('exc_info',)
               36  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               38  POP_TOP          
               40  JUMP_FORWARD         66  'to 66'
             42_0  COME_FROM            10  '10'

 L. 124        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _loop
               46  LOAD_METHOD              call_exception_handler

 L. 125        48  LOAD_FAST                'message'

 L. 126        50  LOAD_FAST                'exc'

 L. 127        52  LOAD_FAST                'self'

 L. 128        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _protocol

 L. 124        58  LOAD_CONST               ('message', 'exception', 'transport', 'protocol')
               60  BUILD_CONST_KEY_MAP_4     4 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
             66_0  COME_FROM            40  '40'
             66_1  COME_FROM            20  '20'
               66  POP_BLOCK        

 L. 131        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _force_close
               72  LOAD_FAST                'exc'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
               78  JUMP_FORWARD         92  'to 92'
             80_0  COME_FROM_FINALLY     0  '0'
               80  LOAD_FAST                'self'
               82  LOAD_METHOD              _force_close
               84  LOAD_FAST                'exc'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
               90  <48>             
             92_0  COME_FROM            78  '78'

Parse error at or near `POP_TOP' instruction at offset 76

    def _force_close--- This code section failed: ---

 L. 134         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _empty_waiter
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    54  'to 54'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _empty_waiter
               14  LOAD_METHOD              done
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_TRUE     54  'to 54'

 L. 135        20  LOAD_FAST                'exc'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    42  'to 42'

 L. 136        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _empty_waiter
               32  LOAD_METHOD              set_result
               34  LOAD_CONST               None
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
               40  JUMP_FORWARD         54  'to 54'
             42_0  COME_FROM            26  '26'

 L. 138        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _empty_waiter
               46  LOAD_METHOD              set_exception
               48  LOAD_FAST                'exc'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
             54_0  COME_FROM            40  '40'
             54_1  COME_FROM            18  '18'
             54_2  COME_FROM             8  '8'

 L. 139        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _closing
               58  POP_JUMP_IF_FALSE    64  'to 64'

 L. 140        60  LOAD_CONST               None
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'

 L. 141        64  LOAD_CONST               True
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _closing

 L. 142        70  LOAD_FAST                'self'
               72  DUP_TOP          
               74  LOAD_ATTR                _conn_lost
               76  LOAD_CONST               1
               78  INPLACE_ADD      
               80  ROT_TWO          
               82  STORE_ATTR               _conn_lost

 L. 143        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _write_fut
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L. 144        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _write_fut
               94  LOAD_METHOD              cancel
               96  CALL_METHOD_0         0  ''
               98  POP_TOP          

 L. 145       100  LOAD_CONST               None
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _write_fut
            106_0  COME_FROM            88  '88'

 L. 146       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _read_fut
              110  POP_JUMP_IF_FALSE   128  'to 128'

 L. 147       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _read_fut
              116  LOAD_METHOD              cancel
              118  CALL_METHOD_0         0  ''
              120  POP_TOP          

 L. 148       122  LOAD_CONST               None
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _read_fut
            128_0  COME_FROM           110  '110'

 L. 149       128  LOAD_CONST               0
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _pending_write

 L. 150       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _buffer

 L. 151       140  LOAD_FAST                'self'
              142  LOAD_ATTR                _loop
              144  LOAD_METHOD              call_soon
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                _call_connection_lost
              150  LOAD_FAST                'exc'
              152  CALL_METHOD_2         2  ''
              154  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _call_connection_lost--- This code section failed: ---

 L. 154         0  SETUP_FINALLY        88  'to 88'

 L. 155         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _protocol
                6  LOAD_METHOD              connection_lost
                8  LOAD_FAST                'exc'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        

 L. 161        16  LOAD_GLOBAL              hasattr
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _sock
               22  LOAD_STR                 'shutdown'
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    42  'to 42'

 L. 162        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _sock
               32  LOAD_METHOD              shutdown
               34  LOAD_GLOBAL              socket
               36  LOAD_ATTR                SHUT_RDWR
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
             42_0  COME_FROM            26  '26'

 L. 163        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _sock
               46  LOAD_METHOD              close
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          

 L. 164        52  LOAD_CONST               None
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _sock

 L. 165        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _server
               62  STORE_FAST               'server'

 L. 166        64  LOAD_FAST                'server'
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE   160  'to 160'

 L. 167        72  LOAD_FAST                'server'
               74  LOAD_METHOD              _detach
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L. 168        80  LOAD_CONST               None
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _server
               86  JUMP_FORWARD        160  'to 160'
             88_0  COME_FROM_FINALLY     0  '0'

 L. 161        88  LOAD_GLOBAL              hasattr
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _sock
               94  LOAD_STR                 'shutdown'
               96  CALL_FUNCTION_2       2  ''
               98  POP_JUMP_IF_FALSE   114  'to 114'

 L. 162       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _sock
              104  LOAD_METHOD              shutdown
              106  LOAD_GLOBAL              socket
              108  LOAD_ATTR                SHUT_RDWR
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          
            114_0  COME_FROM            98  '98'

 L. 163       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _sock
              118  LOAD_METHOD              close
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          

 L. 164       124  LOAD_CONST               None
              126  LOAD_FAST                'self'
              128  STORE_ATTR               _sock

 L. 165       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _server
              134  STORE_FAST               'server'

 L. 166       136  LOAD_FAST                'server'
              138  LOAD_CONST               None
              140  <117>                 1  ''
              142  POP_JUMP_IF_FALSE   158  'to 158'

 L. 167       144  LOAD_FAST                'server'
              146  LOAD_METHOD              _detach
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          

 L. 168       152  LOAD_CONST               None
              154  LOAD_FAST                'self'
              156  STORE_ATTR               _server
            158_0  COME_FROM           142  '142'
              158  <48>             
            160_0  COME_FROM            86  '86'
            160_1  COME_FROM            70  '70'

Parse error at or near `POP_TOP' instruction at offset 40

    def get_write_buffer_size--- This code section failed: ---

 L. 171         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _pending_write
                4  STORE_FAST               'size'

 L. 172         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _buffer
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    30  'to 30'

 L. 173        16  LOAD_FAST                'size'
               18  LOAD_GLOBAL              len
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _buffer
               24  CALL_FUNCTION_1       1  ''
               26  INPLACE_ADD      
               28  STORE_FAST               'size'
             30_0  COME_FROM            14  '14'

 L. 174        30  LOAD_FAST                'size'
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12


class _ProactorReadPipeTransport(_ProactorBasePipeTransport, transports.ReadTransport):
    __doc__ = 'Transport for read pipes.'

    def __init__(self, loop, sock, protocol, waiter=None, extra=None, server=None):
        self._pending_data = None
        self._paused = True
        super.__init__(loop, sock, protocol, waiter, extra, server)
        self._loop.call_soonself._loop_reading
        self._paused = False

    def is_reading(self):
        return not self._paused and not self._closing

    def pause_reading(self):
        if self._closing or (self._paused):
            return
        self._paused = True
        if self._loop.get_debug:
            logger.debug'%r pauses reading'self

    def resume_reading--- This code section failed: ---

 L. 213         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _closing
                4  POP_JUMP_IF_TRUE     12  'to 12'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _paused
               10  POP_JUMP_IF_TRUE     16  'to 16'
             12_0  COME_FROM             4  '4'

 L. 214        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 216        16  LOAD_CONST               False
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _paused

 L. 217        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _read_fut
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    48  'to 48'

 L. 218        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _loop
               36  LOAD_METHOD              call_soon
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _loop_reading
               42  LOAD_CONST               None
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          
             48_0  COME_FROM            30  '30'

 L. 220        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _pending_data
               52  STORE_FAST               'data'

 L. 221        54  LOAD_CONST               None
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _pending_data

 L. 222        60  LOAD_FAST                'data'
               62  LOAD_CONST               None
               64  <117>                 1  ''
               66  POP_JUMP_IF_FALSE    84  'to 84'

 L. 225        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _loop
               72  LOAD_METHOD              call_soon
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _data_received
               78  LOAD_FAST                'data'
               80  CALL_METHOD_2         2  ''
               82  POP_TOP          
             84_0  COME_FROM            66  '66'

 L. 227        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _loop
               88  LOAD_METHOD              get_debug
               90  CALL_METHOD_0         0  ''
               92  POP_JUMP_IF_FALSE   106  'to 106'

 L. 228        94  LOAD_GLOBAL              logger
               96  LOAD_METHOD              debug
               98  LOAD_STR                 '%r resumes reading'
              100  LOAD_FAST                'self'
              102  CALL_METHOD_2         2  ''
              104  POP_TOP          
            106_0  COME_FROM            92  '92'

Parse error at or near `<117>' instruction at offset 28

    def _eof_received--- This code section failed: ---

 L. 231         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loop
                4  LOAD_METHOD              get_debug
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 232        10  LOAD_GLOBAL              logger
               12  LOAD_METHOD              debug
               14  LOAD_STR                 '%r received EOF'
               16  LOAD_FAST                'self'
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          
             22_0  COME_FROM             8  '8'

 L. 234        22  SETUP_FINALLY        38  'to 38'

 L. 235        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _protocol
               28  LOAD_METHOD              eof_received
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'keep_open'
               34  POP_BLOCK        
               36  JUMP_FORWARD        110  'to 110'
             38_0  COME_FROM_FINALLY    22  '22'

 L. 236        38  DUP_TOP          
               40  LOAD_GLOBAL              SystemExit
               42  LOAD_GLOBAL              KeyboardInterrupt
               44  BUILD_TUPLE_2         2 
               46  <121>                60  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 237        54  RAISE_VARARGS_0       0  'reraise'
               56  POP_EXCEPT       
               58  JUMP_FORWARD        110  'to 110'

 L. 238        60  DUP_TOP          
               62  LOAD_GLOBAL              BaseException
               64  <121>               108  ''
               66  POP_TOP          
               68  STORE_FAST               'exc'
               70  POP_TOP          
               72  SETUP_FINALLY       100  'to 100'

 L. 239        74  LOAD_FAST                'self'
               76  LOAD_METHOD              _fatal_error

 L. 240        78  LOAD_FAST                'exc'
               80  LOAD_STR                 'Fatal error: protocol.eof_received() call failed.'

 L. 239        82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 241        86  POP_BLOCK        
               88  POP_EXCEPT       
               90  LOAD_CONST               None
               92  STORE_FAST               'exc'
               94  DELETE_FAST              'exc'
               96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM_FINALLY    72  '72'
              100  LOAD_CONST               None
              102  STORE_FAST               'exc'
              104  DELETE_FAST              'exc'
              106  <48>             
              108  <48>             
            110_0  COME_FROM            58  '58'
            110_1  COME_FROM            36  '36'

 L. 243       110  LOAD_FAST                'keep_open'
              112  POP_JUMP_IF_TRUE    122  'to 122'

 L. 244       114  LOAD_FAST                'self'
              116  LOAD_METHOD              close
              118  CALL_METHOD_0         0  ''
              120  POP_TOP          
            122_0  COME_FROM           112  '112'

Parse error at or near `<121>' instruction at offset 46

    def _data_received--- This code section failed: ---

 L. 247         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _paused
                4  POP_JUMP_IF_FALSE    30  'to 30'

 L. 250         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _pending_data
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 251        20  LOAD_FAST                'data'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _pending_data

 L. 252        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM             4  '4'

 L. 254        30  LOAD_FAST                'data'
               32  POP_JUMP_IF_TRUE     46  'to 46'

 L. 255        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _eof_received
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 256        42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            32  '32'

 L. 258        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _protocol
               52  LOAD_GLOBAL              protocols
               54  LOAD_ATTR                BufferedProtocol
               56  CALL_FUNCTION_2       2  ''
               58  POP_JUMP_IF_FALSE   154  'to 154'

 L. 259        60  SETUP_FINALLY        80  'to 80'

 L. 260        62  LOAD_GLOBAL              protocols
               64  LOAD_METHOD              _feed_data_to_buffered_proto
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _protocol
               70  LOAD_FAST                'data'
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          
               76  POP_BLOCK        
               78  JUMP_FORWARD        166  'to 166'
             80_0  COME_FROM_FINALLY    60  '60'

 L. 261        80  DUP_TOP          
               82  LOAD_GLOBAL              SystemExit
               84  LOAD_GLOBAL              KeyboardInterrupt
               86  BUILD_TUPLE_2         2 
               88  <121>               102  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 262        96  RAISE_VARARGS_0       0  'reraise'
               98  POP_EXCEPT       
              100  JUMP_FORWARD        166  'to 166'

 L. 263       102  DUP_TOP          
              104  LOAD_GLOBAL              BaseException
              106  <121>               150  ''
              108  POP_TOP          
              110  STORE_FAST               'exc'
              112  POP_TOP          
              114  SETUP_FINALLY       142  'to 142'

 L. 264       116  LOAD_FAST                'self'
              118  LOAD_METHOD              _fatal_error
              120  LOAD_FAST                'exc'

 L. 265       122  LOAD_STR                 'Fatal error: protocol.buffer_updated() call failed.'

 L. 264       124  CALL_METHOD_2         2  ''
              126  POP_TOP          

 L. 267       128  POP_BLOCK        
              130  POP_EXCEPT       
              132  LOAD_CONST               None
              134  STORE_FAST               'exc'
              136  DELETE_FAST              'exc'
              138  LOAD_CONST               None
              140  RETURN_VALUE     
            142_0  COME_FROM_FINALLY   114  '114'
              142  LOAD_CONST               None
              144  STORE_FAST               'exc'
              146  DELETE_FAST              'exc'
              148  <48>             
              150  <48>             
              152  JUMP_FORWARD        166  'to 166'
            154_0  COME_FROM            58  '58'

 L. 269       154  LOAD_FAST                'self'
              156  LOAD_ATTR                _protocol
              158  LOAD_METHOD              data_received
              160  LOAD_FAST                'data'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          
            166_0  COME_FROM           152  '152'
            166_1  COME_FROM           100  '100'
            166_2  COME_FROM            78  '78'

Parse error at or near `<117>' instruction at offset 12

    def _loop_reading--- This code section failed: ---

 L. 272         0  LOAD_CONST               None
                2  STORE_FAST               'data'

 L. 273       4_6  SETUP_FINALLY       432  'to 432'
                8  SETUP_FINALLY       180  'to 180'

 L. 274        10  LOAD_FAST                'fut'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    80  'to 80'

 L. 275        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _read_fut
               22  LOAD_FAST                'fut'
               24  <117>                 0  ''
               26  POP_JUMP_IF_TRUE     48  'to 48'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _read_fut
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 276        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _closing

 L. 275        42  POP_JUMP_IF_TRUE     48  'to 48'
             44_0  COME_FROM            36  '36'
               44  <74>             
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'
             48_1  COME_FROM            26  '26'

 L. 277        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _read_fut

 L. 278        54  LOAD_FAST                'fut'
               56  LOAD_METHOD              done
               58  CALL_METHOD_0         0  ''
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L. 280        62  LOAD_FAST                'fut'
               64  LOAD_METHOD              result
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'data'
               70  JUMP_FORWARD         80  'to 80'
             72_0  COME_FROM            60  '60'

 L. 283        72  LOAD_FAST                'fut'
               74  LOAD_METHOD              cancel
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          
             80_0  COME_FROM            70  '70'
             80_1  COME_FROM            16  '16'

 L. 285        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _closing
               84  POP_JUMP_IF_FALSE   116  'to 116'

 L. 287        86  LOAD_CONST               None
               88  STORE_FAST               'data'

 L. 288        90  POP_BLOCK        
               92  POP_BLOCK        

 L. 317        94  LOAD_FAST                'data'
               96  LOAD_CONST               None
               98  <117>                 1  ''
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L. 318       102  LOAD_FAST                'self'
              104  LOAD_METHOD              _data_received
              106  LOAD_FAST                'data'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
            112_0  COME_FROM           100  '100'

 L. 288       112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM            84  '84'

 L. 290       116  LOAD_FAST                'data'
              118  LOAD_CONST               b''
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   150  'to 150'

 L. 292       124  POP_BLOCK        
              126  POP_BLOCK        

 L. 317       128  LOAD_FAST                'data'
              130  LOAD_CONST               None
              132  <117>                 1  ''
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L. 318       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _data_received
              140  LOAD_FAST                'data'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
            146_0  COME_FROM           134  '134'

 L. 292       146  LOAD_CONST               None
              148  RETURN_VALUE     
            150_0  COME_FROM           122  '122'

 L. 297       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _paused
              154  POP_JUMP_IF_TRUE    176  'to 176'

 L. 299       156  LOAD_FAST                'self'
              158  LOAD_ATTR                _loop
              160  LOAD_ATTR                _proactor
              162  LOAD_METHOD              recv
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                _sock
              168  LOAD_CONST               32768
              170  CALL_METHOD_2         2  ''
              172  LOAD_FAST                'self'
              174  STORE_ATTR               _read_fut
            176_0  COME_FROM           154  '154'
              176  POP_BLOCK        
              178  JUMP_FORWARD        386  'to 386'
            180_0  COME_FROM_FINALLY     8  '8'

 L. 300       180  DUP_TOP          
              182  LOAD_GLOBAL              ConnectionAbortedError
          184_186  <121>               260  ''
              188  POP_TOP          
              190  STORE_FAST               'exc'
              192  POP_TOP          
              194  SETUP_FINALLY       252  'to 252'

 L. 301       196  LOAD_FAST                'self'
              198  LOAD_ATTR                _closing
              200  POP_JUMP_IF_TRUE    216  'to 216'

 L. 302       202  LOAD_FAST                'self'
              204  LOAD_METHOD              _fatal_error
              206  LOAD_FAST                'exc'
              208  LOAD_STR                 'Fatal read error on pipe transport'
              210  CALL_METHOD_2         2  ''
              212  POP_TOP          
              214  JUMP_FORWARD        240  'to 240'
            216_0  COME_FROM           200  '200'

 L. 303       216  LOAD_FAST                'self'
              218  LOAD_ATTR                _loop
              220  LOAD_METHOD              get_debug
              222  CALL_METHOD_0         0  ''
              224  POP_JUMP_IF_FALSE   240  'to 240'

 L. 304       226  LOAD_GLOBAL              logger
              228  LOAD_ATTR                debug
              230  LOAD_STR                 'Read error on pipe transport while closing'

 L. 305       232  LOAD_CONST               True

 L. 304       234  LOAD_CONST               ('exc_info',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  POP_TOP          
            240_0  COME_FROM           224  '224'
            240_1  COME_FROM           214  '214'
              240  POP_BLOCK        
              242  POP_EXCEPT       
              244  LOAD_CONST               None
              246  STORE_FAST               'exc'
              248  DELETE_FAST              'exc'
              250  JUMP_FORWARD        408  'to 408'
            252_0  COME_FROM_FINALLY   194  '194'
              252  LOAD_CONST               None
              254  STORE_FAST               'exc'
              256  DELETE_FAST              'exc'
              258  <48>             

 L. 306       260  DUP_TOP          
              262  LOAD_GLOBAL              ConnectionResetError
          264_266  <121>               306  ''
              268  POP_TOP          
              270  STORE_FAST               'exc'
              272  POP_TOP          
              274  SETUP_FINALLY       298  'to 298'

 L. 307       276  LOAD_FAST                'self'
              278  LOAD_METHOD              _force_close
              280  LOAD_FAST                'exc'
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          
              286  POP_BLOCK        
              288  POP_EXCEPT       
              290  LOAD_CONST               None
              292  STORE_FAST               'exc'
              294  DELETE_FAST              'exc'
              296  JUMP_FORWARD        408  'to 408'
            298_0  COME_FROM_FINALLY   274  '274'
              298  LOAD_CONST               None
              300  STORE_FAST               'exc'
              302  DELETE_FAST              'exc'
              304  <48>             

 L. 308       306  DUP_TOP          
              308  LOAD_GLOBAL              OSError
          310_312  <121>               354  ''
              314  POP_TOP          
              316  STORE_FAST               'exc'
              318  POP_TOP          
              320  SETUP_FINALLY       346  'to 346'

 L. 309       322  LOAD_FAST                'self'
              324  LOAD_METHOD              _fatal_error
              326  LOAD_FAST                'exc'
              328  LOAD_STR                 'Fatal read error on pipe transport'
              330  CALL_METHOD_2         2  ''
              332  POP_TOP          
              334  POP_BLOCK        
              336  POP_EXCEPT       
              338  LOAD_CONST               None
              340  STORE_FAST               'exc'
              342  DELETE_FAST              'exc'
              344  JUMP_FORWARD        408  'to 408'
            346_0  COME_FROM_FINALLY   320  '320'
              346  LOAD_CONST               None
              348  STORE_FAST               'exc'
              350  DELETE_FAST              'exc'
              352  <48>             

 L. 310       354  DUP_TOP          
              356  LOAD_GLOBAL              exceptions
              358  LOAD_ATTR                CancelledError
          360_362  <121>               384  ''
              364  POP_TOP          
              366  POP_TOP          
              368  POP_TOP          

 L. 311       370  LOAD_FAST                'self'
              372  LOAD_ATTR                _closing
          374_376  POP_JUMP_IF_TRUE    380  'to 380'

 L. 312       378  RAISE_VARARGS_0       0  'reraise'
            380_0  COME_FROM           374  '374'
              380  POP_EXCEPT       
              382  JUMP_FORWARD        408  'to 408'
              384  <48>             
            386_0  COME_FROM           178  '178'

 L. 314       386  LOAD_FAST                'self'
              388  LOAD_ATTR                _paused
          390_392  POP_JUMP_IF_TRUE    408  'to 408'

 L. 315       394  LOAD_FAST                'self'
              396  LOAD_ATTR                _read_fut
              398  LOAD_METHOD              add_done_callback
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                _loop_reading
              404  CALL_METHOD_1         1  ''
              406  POP_TOP          
            408_0  COME_FROM           390  '390'
            408_1  COME_FROM           382  '382'
            408_2  COME_FROM           344  '344'
            408_3  COME_FROM           296  '296'
            408_4  COME_FROM           250  '250'
              408  POP_BLOCK        

 L. 317       410  LOAD_FAST                'data'
              412  LOAD_CONST               None
              414  <117>                 1  ''
          416_418  POP_JUMP_IF_FALSE   454  'to 454'

 L. 318       420  LOAD_FAST                'self'
              422  LOAD_METHOD              _data_received
              424  LOAD_FAST                'data'
              426  CALL_METHOD_1         1  ''
              428  POP_TOP          
              430  JUMP_FORWARD        454  'to 454'
            432_0  COME_FROM_FINALLY     4  '4'

 L. 317       432  LOAD_FAST                'data'
              434  LOAD_CONST               None
              436  <117>                 1  ''
          438_440  POP_JUMP_IF_FALSE   452  'to 452'

 L. 318       442  LOAD_FAST                'self'
              444  LOAD_METHOD              _data_received
              446  LOAD_FAST                'data'
              448  CALL_METHOD_1         1  ''
              450  POP_TOP          
            452_0  COME_FROM           438  '438'
              452  <48>             
            454_0  COME_FROM           430  '430'
            454_1  COME_FROM           416  '416'

Parse error at or near `<117>' instruction at offset 14


class _ProactorBaseWritePipeTransport(_ProactorBasePipeTransport, transports.WriteTransport):
    __doc__ = 'Transport for write pipes.'
    _start_tls_compatible = True

    def __init__--- This code section failed: ---

 L. 328         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'args'
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kw'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_TOP          

 L. 329        18  LOAD_CONST               None
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _empty_waiter

Parse error at or near `None' instruction at offset -1

    def write--- This code section failed: ---

 L. 332         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  LOAD_GLOBAL              memoryview
               10  BUILD_TUPLE_3         3 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     36  'to 36'

 L. 333        16  LOAD_GLOBAL              TypeError

 L. 334        18  LOAD_STR                 'data argument must be a bytes-like object, not '

 L. 335        20  LOAD_GLOBAL              type
               22  LOAD_FAST                'data'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_ATTR                __name__

 L. 334        28  FORMAT_VALUE          0  ''
               30  BUILD_STRING_2        2 

 L. 333        32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            14  '14'

 L. 336        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _eof_written
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L. 337        42  LOAD_GLOBAL              RuntimeError
               44  LOAD_STR                 'write_eof() already called'
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            40  '40'

 L. 338        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _empty_waiter
               54  LOAD_CONST               None
               56  <117>                 1  ''
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 339        60  LOAD_GLOBAL              RuntimeError
               62  LOAD_STR                 'unable to write; sendfile is in progress'
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 341        68  LOAD_FAST                'data'
               70  POP_JUMP_IF_TRUE     76  'to 76'

 L. 342        72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'

 L. 344        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _conn_lost
               80  POP_JUMP_IF_FALSE   122  'to 122'

 L. 345        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _conn_lost
               86  LOAD_GLOBAL              constants
               88  LOAD_ATTR                LOG_THRESHOLD_FOR_CONNLOST_WRITES
               90  COMPARE_OP               >=
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L. 346        94  LOAD_GLOBAL              logger
               96  LOAD_METHOD              warning
               98  LOAD_STR                 'socket.send() raised exception.'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
            104_0  COME_FROM            92  '92'

 L. 347       104  LOAD_FAST                'self'
              106  DUP_TOP          
              108  LOAD_ATTR                _conn_lost
              110  LOAD_CONST               1
              112  INPLACE_ADD      
              114  ROT_TWO          
              116  STORE_ATTR               _conn_lost

 L. 348       118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM            80  '80'

 L. 356       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _write_fut
              126  LOAD_CONST               None
              128  <117>                 0  ''
              130  POP_JUMP_IF_FALSE   164  'to 164'

 L. 357       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _buffer
              136  LOAD_CONST               None
              138  <117>                 0  ''
              140  POP_JUMP_IF_TRUE    146  'to 146'
              142  <74>             
              144  RAISE_VARARGS_1       1  'exception instance'
            146_0  COME_FROM           140  '140'

 L. 359       146  LOAD_FAST                'self'
              148  LOAD_ATTR                _loop_writing
              150  LOAD_GLOBAL              bytes
              152  LOAD_FAST                'data'
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_CONST               ('data',)
              158  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              160  POP_TOP          
              162  JUMP_FORWARD        210  'to 210'
            164_0  COME_FROM           130  '130'

 L. 360       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _buffer
              168  POP_JUMP_IF_TRUE    190  'to 190'

 L. 362       170  LOAD_GLOBAL              bytearray
              172  LOAD_FAST                'data'
              174  CALL_FUNCTION_1       1  ''
              176  LOAD_FAST                'self'
              178  STORE_ATTR               _buffer

 L. 363       180  LOAD_FAST                'self'
              182  LOAD_METHOD              _maybe_pause_protocol
              184  CALL_METHOD_0         0  ''
              186  POP_TOP          
              188  JUMP_FORWARD        210  'to 210'
            190_0  COME_FROM           168  '168'

 L. 366       190  LOAD_FAST                'self'
              192  LOAD_ATTR                _buffer
              194  LOAD_METHOD              extend
              196  LOAD_FAST                'data'
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L. 367       202  LOAD_FAST                'self'
              204  LOAD_METHOD              _maybe_pause_protocol
              206  CALL_METHOD_0         0  ''
              208  POP_TOP          
            210_0  COME_FROM           188  '188'
            210_1  COME_FROM           162  '162'

Parse error at or near `<117>' instruction at offset 56

    def _loop_writing--- This code section failed: ---

 L. 370       0_2  SETUP_FINALLY       280  'to 280'

 L. 371         4  LOAD_FAST                'f'
                6  LOAD_CONST               None
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    34  'to 34'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _write_fut
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _closing
               26  POP_JUMP_IF_FALSE    34  'to 34'

 L. 374        28  POP_BLOCK        
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            26  '26'
             34_1  COME_FROM            20  '20'
             34_2  COME_FROM            10  '10'

 L. 375        34  LOAD_FAST                'f'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _write_fut
               40  <117>                 0  ''
               42  POP_JUMP_IF_TRUE     48  'to 48'
               44  <74>             
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'

 L. 376        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _write_fut

 L. 377        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _pending_write

 L. 378        60  LOAD_FAST                'f'
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 379        64  LOAD_FAST                'f'
               66  LOAD_METHOD              result
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          
             72_0  COME_FROM            62  '62'

 L. 380        72  LOAD_FAST                'data'
               74  LOAD_CONST               None
               76  <117>                 0  ''
               78  POP_JUMP_IF_FALSE    92  'to 92'

 L. 381        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _buffer
               84  STORE_FAST               'data'

 L. 382        86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _buffer
             92_0  COME_FROM            78  '78'

 L. 383        92  LOAD_FAST                'data'
               94  POP_JUMP_IF_TRUE    148  'to 148'

 L. 384        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _closing
              100  POP_JUMP_IF_FALSE   118  'to 118'

 L. 385       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _loop
              106  LOAD_METHOD              call_soon
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _call_connection_lost
              112  LOAD_CONST               None
              114  CALL_METHOD_2         2  ''
              116  POP_TOP          
            118_0  COME_FROM           100  '100'

 L. 386       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _eof_written
              122  POP_JUMP_IF_FALSE   138  'to 138'

 L. 387       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _sock
              128  LOAD_METHOD              shutdown
              130  LOAD_GLOBAL              socket
              132  LOAD_ATTR                SHUT_WR
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           122  '122'

 L. 393       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _maybe_resume_protocol
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          
              146  JUMP_FORWARD        240  'to 240'
            148_0  COME_FROM            94  '94'

 L. 395       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _loop
              152  LOAD_ATTR                _proactor
              154  LOAD_METHOD              send
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _sock
              160  LOAD_FAST                'data'
              162  CALL_METHOD_2         2  ''
              164  LOAD_FAST                'self'
              166  STORE_ATTR               _write_fut

 L. 396       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _write_fut
              172  LOAD_METHOD              done
              174  CALL_METHOD_0         0  ''
              176  POP_JUMP_IF_TRUE    226  'to 226'

 L. 397       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _pending_write
              182  LOAD_CONST               0
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_TRUE    192  'to 192'
              188  <74>             
              190  RAISE_VARARGS_1       1  'exception instance'
            192_0  COME_FROM           186  '186'

 L. 398       192  LOAD_GLOBAL              len
              194  LOAD_FAST                'data'
              196  CALL_FUNCTION_1       1  ''
              198  LOAD_FAST                'self'
              200  STORE_ATTR               _pending_write

 L. 399       202  LOAD_FAST                'self'
              204  LOAD_ATTR                _write_fut
              206  LOAD_METHOD              add_done_callback
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                _loop_writing
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 400       216  LOAD_FAST                'self'
              218  LOAD_METHOD              _maybe_pause_protocol
              220  CALL_METHOD_0         0  ''
              222  POP_TOP          
              224  JUMP_FORWARD        240  'to 240'
            226_0  COME_FROM           176  '176'

 L. 402       226  LOAD_FAST                'self'
              228  LOAD_ATTR                _write_fut
              230  LOAD_METHOD              add_done_callback
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                _loop_writing
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
            240_0  COME_FROM           224  '224'
            240_1  COME_FROM           146  '146'

 L. 403       240  LOAD_FAST                'self'
              242  LOAD_ATTR                _empty_waiter
              244  LOAD_CONST               None
              246  <117>                 1  ''
          248_250  POP_JUMP_IF_FALSE   276  'to 276'
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                _write_fut
              256  LOAD_CONST               None
              258  <117>                 0  ''
          260_262  POP_JUMP_IF_FALSE   276  'to 276'

 L. 404       264  LOAD_FAST                'self'
              266  LOAD_ATTR                _empty_waiter
              268  LOAD_METHOD              set_result
              270  LOAD_CONST               None
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
            276_0  COME_FROM           260  '260'
            276_1  COME_FROM           248  '248'
              276  POP_BLOCK        
              278  JUMP_FORWARD        376  'to 376'
            280_0  COME_FROM_FINALLY     0  '0'

 L. 405       280  DUP_TOP          
              282  LOAD_GLOBAL              ConnectionResetError
          284_286  <121>               326  ''
              288  POP_TOP          
              290  STORE_FAST               'exc'
              292  POP_TOP          
              294  SETUP_FINALLY       318  'to 318'

 L. 406       296  LOAD_FAST                'self'
              298  LOAD_METHOD              _force_close
              300  LOAD_FAST                'exc'
              302  CALL_METHOD_1         1  ''
              304  POP_TOP          
              306  POP_BLOCK        
              308  POP_EXCEPT       
              310  LOAD_CONST               None
              312  STORE_FAST               'exc'
              314  DELETE_FAST              'exc'
              316  JUMP_FORWARD        376  'to 376'
            318_0  COME_FROM_FINALLY   294  '294'
              318  LOAD_CONST               None
              320  STORE_FAST               'exc'
              322  DELETE_FAST              'exc'
              324  <48>             

 L. 407       326  DUP_TOP          
              328  LOAD_GLOBAL              OSError
          330_332  <121>               374  ''
              334  POP_TOP          
              336  STORE_FAST               'exc'
              338  POP_TOP          
              340  SETUP_FINALLY       366  'to 366'

 L. 408       342  LOAD_FAST                'self'
              344  LOAD_METHOD              _fatal_error
              346  LOAD_FAST                'exc'
              348  LOAD_STR                 'Fatal write error on pipe transport'
              350  CALL_METHOD_2         2  ''
              352  POP_TOP          
              354  POP_BLOCK        
              356  POP_EXCEPT       
              358  LOAD_CONST               None
              360  STORE_FAST               'exc'
              362  DELETE_FAST              'exc'
              364  JUMP_FORWARD        376  'to 376'
            366_0  COME_FROM_FINALLY   340  '340'
              366  LOAD_CONST               None
              368  STORE_FAST               'exc'
              370  DELETE_FAST              'exc'
              372  <48>             
              374  <48>             
            376_0  COME_FROM           364  '364'
            376_1  COME_FROM           316  '316'
            376_2  COME_FROM           278  '278'

Parse error at or near `<117>' instruction at offset 8

    def can_write_eof(self):
        return True

    def write_eof(self):
        self.close

    def abort(self):
        self._force_closeNone

    def _make_empty_waiter--- This code section failed: ---

 L. 420         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _empty_waiter
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 421        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Empty waiter is already set'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 422        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _loop
               22  LOAD_METHOD              create_future
               24  CALL_METHOD_0         0  ''
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _empty_waiter

 L. 423        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _write_fut
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 424        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _empty_waiter
               44  LOAD_METHOD              set_result
               46  LOAD_CONST               None
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
             52_0  COME_FROM            38  '38'

 L. 425        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _empty_waiter
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _reset_empty_waiter(self):
        self._empty_waiter = None


class _ProactorWritePipeTransport(_ProactorBaseWritePipeTransport):

    def __init__--- This code section failed: ---

 L. 433         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'args'
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kw'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_TOP          

 L. 434        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _loop
               22  LOAD_ATTR                _proactor
               24  LOAD_METHOD              recv
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _sock
               30  LOAD_CONST               16
               32  CALL_METHOD_2         2  ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _read_fut

 L. 435        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _read_fut
               42  LOAD_METHOD              add_done_callback
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _pipe_closed
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _pipe_closed--- This code section failed: ---

 L. 438         0  LOAD_FAST                'fut'
                2  LOAD_METHOD              cancelled
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 440         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 441        12  LOAD_FAST                'fut'
               14  LOAD_METHOD              result
               16  CALL_METHOD_0         0  ''
               18  LOAD_CONST               b''
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 442        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _closing
               32  POP_JUMP_IF_FALSE    52  'to 52'

 L. 443        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _read_fut
               38  LOAD_CONST               None
               40  <117>                 0  ''
               42  POP_JUMP_IF_TRUE     48  'to 48'
               44  <74>             
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'

 L. 444        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            32  '32'

 L. 445        52  LOAD_FAST                'fut'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _read_fut
               58  <117>                 0  ''
               60  POP_JUMP_IF_TRUE     76  'to 76'
               62  <74>             
               64  LOAD_FAST                'fut'
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _read_fut
               70  BUILD_TUPLE_2         2 
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            60  '60'

 L. 446        76  LOAD_CONST               None
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _read_fut

 L. 447        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _write_fut
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   106  'to 106'

 L. 448        92  LOAD_FAST                'self'
               94  LOAD_METHOD              _force_close
               96  LOAD_GLOBAL              BrokenPipeError
               98  CALL_FUNCTION_0       0  ''
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  JUMP_FORWARD        114  'to 114'
            106_0  COME_FROM            90  '90'

 L. 450       106  LOAD_FAST                'self'
              108  LOAD_METHOD              close
              110  CALL_METHOD_0         0  ''
              112  POP_TOP          
            114_0  COME_FROM           104  '104'

Parse error at or near `<74>' instruction at offset 24


class _ProactorDatagramTransport(_ProactorBasePipeTransport):
    max_size = 262144

    def __init__(self, loop, sock, protocol, address=None, waiter=None, extra=None):
        self._address = address
        self._empty_waiter = None
        super.__init__(loop, sock, protocol, waiter=waiter, extra=extra)
        self._buffer = collections.deque
        self._loop.call_soonself._loop_reading

    def _set_extra(self, sock):
        _set_socket_extraselfsock

    def get_write_buffer_size(self):
        return sum((len(data) for data, _ in self._buffer))

    def abort(self):
        self._force_closeNone

    def sendto--- This code section failed: ---

 L. 477         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  LOAD_GLOBAL              memoryview
               10  BUILD_TUPLE_3         3 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     30  'to 30'

 L. 478        16  LOAD_GLOBAL              TypeError
               18  LOAD_STR                 'data argument must be bytes-like object (%r)'

 L. 479        20  LOAD_GLOBAL              type
               22  LOAD_FAST                'data'
               24  CALL_FUNCTION_1       1  ''

 L. 478        26  CALL_FUNCTION_2       2  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            14  '14'

 L. 481        30  LOAD_FAST                'data'
               32  POP_JUMP_IF_TRUE     38  'to 38'

 L. 482        34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 484        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _address
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    78  'to 78'
               48  LOAD_FAST                'addr'
               50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _address
               56  BUILD_TUPLE_2         2 
               58  <118>                 1  ''
               60  POP_JUMP_IF_FALSE    78  'to 78'

 L. 485        62  LOAD_GLOBAL              ValueError

 L. 486        64  LOAD_STR                 'Invalid address: must be None or '
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _address
               70  FORMAT_VALUE          0  ''
               72  BUILD_STRING_2        2 

 L. 485        74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            60  '60'
             78_1  COME_FROM            46  '46'

 L. 488        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _conn_lost
               82  POP_JUMP_IF_FALSE   130  'to 130'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _address
               88  POP_JUMP_IF_FALSE   130  'to 130'

 L. 489        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _conn_lost
               94  LOAD_GLOBAL              constants
               96  LOAD_ATTR                LOG_THRESHOLD_FOR_CONNLOST_WRITES
               98  COMPARE_OP               >=
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L. 490       102  LOAD_GLOBAL              logger
              104  LOAD_METHOD              warning
              106  LOAD_STR                 'socket.sendto() raised exception.'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
            112_0  COME_FROM           100  '100'

 L. 491       112  LOAD_FAST                'self'
              114  DUP_TOP          
              116  LOAD_ATTR                _conn_lost
              118  LOAD_CONST               1
              120  INPLACE_ADD      
              122  ROT_TWO          
              124  STORE_ATTR               _conn_lost

 L. 492       126  LOAD_CONST               None
              128  RETURN_VALUE     
            130_0  COME_FROM            88  '88'
            130_1  COME_FROM            82  '82'

 L. 495       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _buffer
              134  LOAD_METHOD              append
              136  LOAD_GLOBAL              bytes
              138  LOAD_FAST                'data'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_FAST                'addr'
              144  BUILD_TUPLE_2         2 
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 497       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _write_fut
              154  LOAD_CONST               None
              156  <117>                 0  ''
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L. 499       160  LOAD_FAST                'self'
              162  LOAD_METHOD              _loop_writing
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
            168_0  COME_FROM           158  '158'

 L. 502       168  LOAD_FAST                'self'
              170  LOAD_METHOD              _maybe_pause_protocol
              172  CALL_METHOD_0         0  ''
              174  POP_TOP          

Parse error at or near `<117>' instruction at offset 44

    def _loop_writing--- This code section failed: ---

 L. 505         0  SETUP_FINALLY       166  'to 166'

 L. 506         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _conn_lost
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 507         8  POP_BLOCK        
               10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             6  '6'

 L. 509        14  LOAD_FAST                'fut'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _write_fut
               20  <117>                 0  ''
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 510        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _write_fut

 L. 511        34  LOAD_FAST                'fut'
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 513        38  LOAD_FAST                'fut'
               40  LOAD_METHOD              result
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          
             46_0  COME_FROM            36  '36'

 L. 515        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _buffer
               50  POP_JUMP_IF_FALSE    64  'to 64'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _conn_lost
               56  POP_JUMP_IF_FALSE    92  'to 92'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _address
               62  POP_JUMP_IF_FALSE    92  'to 92'
             64_0  COME_FROM            50  '50'

 L. 517        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _closing
               68  POP_JUMP_IF_FALSE    86  'to 86'

 L. 518        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _loop
               74  LOAD_METHOD              call_soon
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _call_connection_lost
               80  LOAD_CONST               None
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          
             86_0  COME_FROM            68  '68'

 L. 519        86  POP_BLOCK        
               88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            62  '62'
             92_1  COME_FROM            56  '56'

 L. 521        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _buffer
               96  LOAD_METHOD              popleft
               98  CALL_METHOD_0         0  ''
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'data'
              104  STORE_FAST               'addr'

 L. 522       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _address
              110  LOAD_CONST               None
              112  <117>                 1  ''
              114  POP_JUMP_IF_FALSE   138  'to 138'

 L. 523       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _loop
              120  LOAD_ATTR                _proactor
              122  LOAD_METHOD              send
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _sock

 L. 524       128  LOAD_FAST                'data'

 L. 523       130  CALL_METHOD_2         2  ''
              132  LOAD_FAST                'self'
              134  STORE_ATTR               _write_fut
              136  JUMP_FORWARD        162  'to 162'
            138_0  COME_FROM           114  '114'

 L. 526       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _loop
              142  LOAD_ATTR                _proactor
              144  LOAD_ATTR                sendto
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                _sock

 L. 527       150  LOAD_FAST                'data'

 L. 528       152  LOAD_FAST                'addr'

 L. 526       154  LOAD_CONST               ('addr',)
              156  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              158  LOAD_FAST                'self'
              160  STORE_ATTR               _write_fut
            162_0  COME_FROM           136  '136'
              162  POP_BLOCK        
              164  JUMP_FORWARD        262  'to 262'
            166_0  COME_FROM_FINALLY     0  '0'

 L. 529       166  DUP_TOP          
              168  LOAD_GLOBAL              OSError
              170  <121>               212  ''
              172  POP_TOP          
              174  STORE_FAST               'exc'
              176  POP_TOP          
              178  SETUP_FINALLY       204  'to 204'

 L. 530       180  LOAD_FAST                'self'
              182  LOAD_ATTR                _protocol
              184  LOAD_METHOD              error_received
              186  LOAD_FAST                'exc'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          
              192  POP_BLOCK        
              194  POP_EXCEPT       
              196  LOAD_CONST               None
              198  STORE_FAST               'exc'
              200  DELETE_FAST              'exc'
              202  JUMP_FORWARD        284  'to 284'
            204_0  COME_FROM_FINALLY   178  '178'
              204  LOAD_CONST               None
              206  STORE_FAST               'exc'
              208  DELETE_FAST              'exc'
              210  <48>             

 L. 531       212  DUP_TOP          
              214  LOAD_GLOBAL              Exception
          216_218  <121>               260  ''
              220  POP_TOP          
              222  STORE_FAST               'exc'
              224  POP_TOP          
              226  SETUP_FINALLY       252  'to 252'

 L. 532       228  LOAD_FAST                'self'
              230  LOAD_METHOD              _fatal_error
              232  LOAD_FAST                'exc'
              234  LOAD_STR                 'Fatal write error on datagram transport'
              236  CALL_METHOD_2         2  ''
              238  POP_TOP          
              240  POP_BLOCK        
              242  POP_EXCEPT       
              244  LOAD_CONST               None
              246  STORE_FAST               'exc'
              248  DELETE_FAST              'exc'
              250  JUMP_FORWARD        284  'to 284'
            252_0  COME_FROM_FINALLY   226  '226'
              252  LOAD_CONST               None
              254  STORE_FAST               'exc'
              256  DELETE_FAST              'exc'
              258  <48>             
              260  <48>             
            262_0  COME_FROM           164  '164'

 L. 534       262  LOAD_FAST                'self'
              264  LOAD_ATTR                _write_fut
              266  LOAD_METHOD              add_done_callback
              268  LOAD_FAST                'self'
              270  LOAD_ATTR                _loop_writing
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          

 L. 535       276  LOAD_FAST                'self'
              278  LOAD_METHOD              _maybe_resume_protocol
              280  CALL_METHOD_0         0  ''
              282  POP_TOP          
            284_0  COME_FROM           250  '250'
            284_1  COME_FROM           202  '202'

Parse error at or near `LOAD_CONST' instruction at offset 10

    def _loop_reading--- This code section failed: ---

 L. 538         0  LOAD_CONST               None
                2  STORE_FAST               'data'

 L. 539       4_6  SETUP_FINALLY       384  'to 384'
                8  SETUP_FINALLY       254  'to 254'

 L. 540        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _conn_lost
               14  POP_JUMP_IF_FALSE    42  'to 42'

 L. 541        16  POP_BLOCK        
               18  POP_BLOCK        

 L. 577        20  LOAD_FAST                'data'
               22  POP_JUMP_IF_FALSE    38  'to 38'

 L. 578        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _protocol
               28  LOAD_METHOD              datagram_received
               30  LOAD_FAST                'data'
               32  LOAD_FAST                'addr'
               34  CALL_METHOD_2         2  ''
               36  POP_TOP          
             38_0  COME_FROM            22  '22'

 L. 541        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            14  '14'

 L. 543        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _read_fut
               46  LOAD_FAST                'fut'
               48  <117>                 0  ''
               50  POP_JUMP_IF_TRUE     72  'to 72'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _read_fut
               56  LOAD_CONST               None
               58  <117>                 0  ''
               60  POP_JUMP_IF_FALSE    68  'to 68'

 L. 544        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _closing

 L. 543        66  POP_JUMP_IF_TRUE     72  'to 72'
             68_0  COME_FROM            60  '60'
               68  <74>             
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            66  '66'
             72_1  COME_FROM            50  '50'

 L. 546        72  LOAD_CONST               None
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _read_fut

 L. 547        78  LOAD_FAST                'fut'
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   162  'to 162'

 L. 548        86  LOAD_FAST                'fut'
               88  LOAD_METHOD              result
               90  CALL_METHOD_0         0  ''
               92  STORE_FAST               'res'

 L. 550        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _closing
               98  POP_JUMP_IF_FALSE   130  'to 130'

 L. 552       100  LOAD_CONST               None
              102  STORE_FAST               'data'

 L. 553       104  POP_BLOCK        
              106  POP_BLOCK        

 L. 577       108  LOAD_FAST                'data'
              110  POP_JUMP_IF_FALSE   126  'to 126'

 L. 578       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _protocol
              116  LOAD_METHOD              datagram_received
              118  LOAD_FAST                'data'
              120  LOAD_FAST                'addr'
              122  CALL_METHOD_2         2  ''
              124  POP_TOP          
            126_0  COME_FROM           110  '110'

 L. 553       126  LOAD_CONST               None
              128  RETURN_VALUE     
            130_0  COME_FROM            98  '98'

 L. 555       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _address
              134  LOAD_CONST               None
              136  <117>                 1  ''
              138  POP_JUMP_IF_FALSE   154  'to 154'

 L. 556       140  LOAD_FAST                'res'
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _address
              146  ROT_TWO          
              148  STORE_FAST               'data'
              150  STORE_FAST               'addr'
              152  JUMP_FORWARD        162  'to 162'
            154_0  COME_FROM           138  '138'

 L. 558       154  LOAD_FAST                'res'
              156  UNPACK_SEQUENCE_2     2 
              158  STORE_FAST               'data'
              160  STORE_FAST               'addr'
            162_0  COME_FROM           152  '152'
            162_1  COME_FROM            84  '84'

 L. 560       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _conn_lost
              166  POP_JUMP_IF_FALSE   194  'to 194'

 L. 561       168  POP_BLOCK        
              170  POP_BLOCK        

 L. 577       172  LOAD_FAST                'data'
              174  POP_JUMP_IF_FALSE   190  'to 190'

 L. 578       176  LOAD_FAST                'self'
              178  LOAD_ATTR                _protocol
              180  LOAD_METHOD              datagram_received
              182  LOAD_FAST                'data'
              184  LOAD_FAST                'addr'
              186  CALL_METHOD_2         2  ''
              188  POP_TOP          
            190_0  COME_FROM           174  '174'

 L. 561       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           166  '166'

 L. 562       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _address
              198  LOAD_CONST               None
              200  <117>                 1  ''
              202  POP_JUMP_IF_FALSE   228  'to 228'

 L. 563       204  LOAD_FAST                'self'
              206  LOAD_ATTR                _loop
              208  LOAD_ATTR                _proactor
              210  LOAD_METHOD              recv
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                _sock

 L. 564       216  LOAD_FAST                'self'
              218  LOAD_ATTR                max_size

 L. 563       220  CALL_METHOD_2         2  ''
              222  LOAD_FAST                'self'
              224  STORE_ATTR               _read_fut
              226  JUMP_FORWARD        250  'to 250'
            228_0  COME_FROM           202  '202'

 L. 566       228  LOAD_FAST                'self'
              230  LOAD_ATTR                _loop
              232  LOAD_ATTR                _proactor
              234  LOAD_METHOD              recvfrom
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                _sock

 L. 567       240  LOAD_FAST                'self'
              242  LOAD_ATTR                max_size

 L. 566       244  CALL_METHOD_2         2  ''
              246  LOAD_FAST                'self'
              248  STORE_ATTR               _read_fut
            250_0  COME_FROM           226  '226'
              250  POP_BLOCK        
              252  JUMP_FORWARD        334  'to 334'
            254_0  COME_FROM_FINALLY     8  '8'

 L. 568       254  DUP_TOP          
              256  LOAD_GLOBAL              OSError
          258_260  <121>               302  ''
              262  POP_TOP          
              264  STORE_FAST               'exc'
              266  POP_TOP          
              268  SETUP_FINALLY       294  'to 294'

 L. 569       270  LOAD_FAST                'self'
              272  LOAD_ATTR                _protocol
              274  LOAD_METHOD              error_received
              276  LOAD_FAST                'exc'
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          
              282  POP_BLOCK        
              284  POP_EXCEPT       
              286  LOAD_CONST               None
              288  STORE_FAST               'exc'
              290  DELETE_FAST              'exc'
              292  JUMP_FORWARD        360  'to 360'
            294_0  COME_FROM_FINALLY   268  '268'
              294  LOAD_CONST               None
              296  STORE_FAST               'exc'
              298  DELETE_FAST              'exc'
              300  <48>             

 L. 570       302  DUP_TOP          
              304  LOAD_GLOBAL              exceptions
              306  LOAD_ATTR                CancelledError
          308_310  <121>               332  ''
              312  POP_TOP          
              314  POP_TOP          
              316  POP_TOP          

 L. 571       318  LOAD_FAST                'self'
              320  LOAD_ATTR                _closing
          322_324  POP_JUMP_IF_TRUE    328  'to 328'

 L. 572       326  RAISE_VARARGS_0       0  'reraise'
            328_0  COME_FROM           322  '322'
              328  POP_EXCEPT       
              330  JUMP_FORWARD        360  'to 360'
              332  <48>             
            334_0  COME_FROM           252  '252'

 L. 574       334  LOAD_FAST                'self'
              336  LOAD_ATTR                _read_fut
              338  LOAD_CONST               None
              340  <117>                 1  ''
          342_344  POP_JUMP_IF_FALSE   360  'to 360'

 L. 575       346  LOAD_FAST                'self'
              348  LOAD_ATTR                _read_fut
              350  LOAD_METHOD              add_done_callback
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                _loop_reading
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          
            360_0  COME_FROM           342  '342'
            360_1  COME_FROM           330  '330'
            360_2  COME_FROM           292  '292'
              360  POP_BLOCK        

 L. 577       362  LOAD_FAST                'data'
          364_366  POP_JUMP_IF_FALSE   406  'to 406'

 L. 578       368  LOAD_FAST                'self'
              370  LOAD_ATTR                _protocol
              372  LOAD_METHOD              datagram_received
              374  LOAD_FAST                'data'
              376  LOAD_FAST                'addr'
              378  CALL_METHOD_2         2  ''
              380  POP_TOP          
              382  JUMP_FORWARD        406  'to 406'
            384_0  COME_FROM_FINALLY     4  '4'

 L. 577       384  LOAD_FAST                'data'
          386_388  POP_JUMP_IF_FALSE   404  'to 404'

 L. 578       390  LOAD_FAST                'self'
              392  LOAD_ATTR                _protocol
              394  LOAD_METHOD              datagram_received
              396  LOAD_FAST                'data'
              398  LOAD_FAST                'addr'
              400  CALL_METHOD_2         2  ''
              402  POP_TOP          
            404_0  COME_FROM           386  '386'
              404  <48>             
            406_0  COME_FROM           382  '382'
            406_1  COME_FROM           364  '364'

Parse error at or near `POP_BLOCK' instruction at offset 18


class _ProactorDuplexPipeTransport(_ProactorReadPipeTransport, _ProactorBaseWritePipeTransport, transports.Transport):
    __doc__ = 'Transport for duplex pipes.'

    def can_write_eof(self):
        return False

    def write_eof(self):
        raise NotImplementedError


class _ProactorSocketTransport(_ProactorReadPipeTransport, _ProactorBaseWritePipeTransport, transports.Transport):
    __doc__ = 'Transport for connected sockets.'
    _sendfile_compatible = constants._SendfileMode.TRY_NATIVE

    def __init__(self, loop, sock, protocol, waiter=None, extra=None, server=None):
        super.__init__(loop, sock, protocol, waiter, extra, server)
        base_events._set_nodelaysock

    def _set_extra(self, sock):
        _set_socket_extraselfsock

    def can_write_eof(self):
        return True

    def write_eof--- This code section failed: ---

 L. 612         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _closing
                4  POP_JUMP_IF_TRUE     12  'to 12'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _eof_written
               10  POP_JUMP_IF_FALSE    16  'to 16'
             12_0  COME_FROM             4  '4'

 L. 613        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 614        16  LOAD_CONST               True
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _eof_written

 L. 615        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _write_fut
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L. 616        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _sock
               36  LOAD_METHOD              shutdown
               38  LOAD_GLOBAL              socket
               40  LOAD_ATTR                SHUT_WR
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
             46_0  COME_FROM            30  '30'

Parse error at or near `<117>' instruction at offset 28


class BaseProactorEventLoop(base_events.BaseEventLoop):

    def __init__--- This code section failed: ---

 L. 622         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __init__
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L. 623        10  LOAD_GLOBAL              logger
               12  LOAD_METHOD              debug
               14  LOAD_STR                 'Using proactor: %s'
               16  LOAD_FAST                'proactor'
               18  LOAD_ATTR                __class__
               20  LOAD_ATTR                __name__
               22  CALL_METHOD_2         2  ''
               24  POP_TOP          

 L. 624        26  LOAD_FAST                'proactor'
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _proactor

 L. 625        32  LOAD_FAST                'proactor'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _selector

 L. 626        38  LOAD_CONST               None
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _self_reading_future

 L. 627        44  BUILD_MAP_0           0 
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _accept_futures

 L. 628        50  LOAD_FAST                'proactor'
               52  LOAD_METHOD              set_loop
               54  LOAD_FAST                'self'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 629        60  LOAD_FAST                'self'
               62  LOAD_METHOD              _make_self_pipe
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          

 L. 630        68  LOAD_GLOBAL              threading
               70  LOAD_METHOD              current_thread
               72  CALL_METHOD_0         0  ''
               74  LOAD_GLOBAL              threading
               76  LOAD_METHOD              main_thread
               78  CALL_METHOD_0         0  ''
               80  <117>                 0  ''
               82  POP_JUMP_IF_FALSE   100  'to 100'

 L. 632        84  LOAD_GLOBAL              signal
               86  LOAD_METHOD              set_wakeup_fd
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _csock
               92  LOAD_METHOD              fileno
               94  CALL_METHOD_0         0  ''
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
            100_0  COME_FROM            82  '82'

Parse error at or near `<117>' instruction at offset 80

    def _make_socket_transport(self, sock, protocol, waiter=None, extra=None, server=None):
        return _ProactorSocketTransport(self, sock, protocol, waiter, extra, server)

    def _make_ssl_transport(self, rawsock, protocol, sslcontext, waiter=None, *, server_side=False, server_hostname=None, extra=None, server=None, ssl_handshake_timeout=None):
        ssl_protocol = sslproto.SSLProtocol(self,
          protocol, sslcontext, waiter, server_side,
          server_hostname, ssl_handshake_timeout=ssl_handshake_timeout)
        _ProactorSocketTransport(self, rawsock, ssl_protocol, extra=extra,
          server=server)
        return ssl_protocol._app_transport

    def _make_datagram_transport(self, sock, protocol, address=None, waiter=None, extra=None):
        return _ProactorDatagramTransport(self, sock, protocol, address, waiter, extra)

    def _make_duplex_pipe_transport(self, sock, protocol, waiter=None, extra=None):
        return _ProactorDuplexPipeTransport(self, sock, protocol, waiter, extra)

    def _make_read_pipe_transport(self, sock, protocol, waiter=None, extra=None):
        return _ProactorReadPipeTransport(self, sock, protocol, waiter, extra)

    def _make_write_pipe_transport(self, sock, protocol, waiter=None, extra=None):
        return _ProactorWritePipeTransport(self, sock, protocol, waiter, extra)

    def close--- This code section failed: ---

 L. 673         0  LOAD_FAST                'self'
                2  LOAD_METHOD              is_running
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 674         8  LOAD_GLOBAL              RuntimeError
               10  LOAD_STR                 'Cannot close a running event loop'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 675        16  LOAD_FAST                'self'
               18  LOAD_METHOD              is_closed
               20  CALL_METHOD_0         0  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 676        24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 678        28  LOAD_GLOBAL              threading
               30  LOAD_METHOD              current_thread
               32  CALL_METHOD_0         0  ''
               34  LOAD_GLOBAL              threading
               36  LOAD_METHOD              main_thread
               38  CALL_METHOD_0         0  ''
               40  <117>                 0  ''
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L. 679        44  LOAD_GLOBAL              signal
               46  LOAD_METHOD              set_wakeup_fd
               48  LOAD_CONST               -1
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
             54_0  COME_FROM            42  '42'

 L. 683        54  LOAD_FAST                'self'
               56  LOAD_METHOD              _stop_accept_futures
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          

 L. 684        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _close_self_pipe
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          

 L. 685        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _proactor
               74  LOAD_METHOD              close
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L. 686        80  LOAD_CONST               None
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _proactor

 L. 687        86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _selector

 L. 690        92  LOAD_GLOBAL              super
               94  CALL_FUNCTION_0       0  ''
               96  LOAD_METHOD              close
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          

Parse error at or near `<117>' instruction at offset 40

    async def sock_recv(self, sock, n):
        return await self._proactor.recvsockn

    async def sock_recv_into(self, sock, buf):
        return await self._proactor.recv_intosockbuf

    async def sock_sendall(self, sock, data):
        return await self._proactor.sendsockdata

    async def sock_connect(self, sock, address):
        return await self._proactor.connectsockaddress

    async def sock_accept(self, sock):
        return await self._proactor.acceptsock

    async def _sock_sendfile_native--- This code section failed: ---

 L. 708         0  SETUP_FINALLY        14  'to 14'

 L. 709         2  LOAD_FAST                'file'
                4  LOAD_METHOD              fileno
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'fileno'
               10  POP_BLOCK        
               12  JUMP_FORWARD         66  'to 66'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 710        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  LOAD_GLOBAL              io
               20  LOAD_ATTR                UnsupportedOperation
               22  BUILD_TUPLE_2         2 
               24  <121>                64  ''
               26  POP_TOP          
               28  STORE_FAST               'err'
               30  POP_TOP          
               32  SETUP_FINALLY        56  'to 56'

 L. 711        34  LOAD_GLOBAL              exceptions
               36  LOAD_METHOD              SendfileNotAvailableError
               38  LOAD_STR                 'not a regular file'
               40  CALL_METHOD_1         1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
               44  POP_BLOCK        
               46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  STORE_FAST               'err'
               52  DELETE_FAST              'err'
               54  JUMP_FORWARD         66  'to 66'
             56_0  COME_FROM_FINALLY    32  '32'
               56  LOAD_CONST               None
               58  STORE_FAST               'err'
               60  DELETE_FAST              'err'
               62  <48>             
               64  <48>             
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            12  '12'

 L. 712        66  SETUP_FINALLY        84  'to 84'

 L. 713        68  LOAD_GLOBAL              os
               70  LOAD_METHOD              fstat
               72  LOAD_FAST                'fileno'
               74  CALL_METHOD_1         1  ''
               76  LOAD_ATTR                st_size
               78  STORE_FAST               'fsize'
               80  POP_BLOCK        
               82  JUMP_FORWARD        112  'to 112'
             84_0  COME_FROM_FINALLY    66  '66'

 L. 714        84  DUP_TOP          
               86  LOAD_GLOBAL              OSError
               88  <121>               110  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 715        96  LOAD_GLOBAL              exceptions
               98  LOAD_METHOD              SendfileNotAvailableError
              100  LOAD_STR                 'not a regular file'
              102  CALL_METHOD_1         1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
              110  <48>             
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            82  '82'

 L. 716       112  LOAD_FAST                'count'
              114  POP_JUMP_IF_FALSE   120  'to 120'
              116  LOAD_FAST                'count'
              118  JUMP_FORWARD        122  'to 122'
            120_0  COME_FROM           114  '114'
              120  LOAD_FAST                'fsize'
            122_0  COME_FROM           118  '118'
              122  STORE_FAST               'blocksize'

 L. 717       124  LOAD_FAST                'blocksize'
              126  POP_JUMP_IF_TRUE    132  'to 132'

 L. 718       128  LOAD_CONST               0
              130  RETURN_VALUE     
            132_0  COME_FROM           126  '126'

 L. 720       132  LOAD_GLOBAL              min
              134  LOAD_FAST                'blocksize'
              136  LOAD_CONST               4294967295
              138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'blocksize'

 L. 721       142  LOAD_FAST                'count'
              144  POP_JUMP_IF_FALSE   160  'to 160'
              146  LOAD_GLOBAL              min
              148  LOAD_FAST                'offset'
              150  LOAD_FAST                'count'
              152  BINARY_ADD       
              154  LOAD_FAST                'fsize'
              156  CALL_FUNCTION_2       2  ''
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM           144  '144'
              160  LOAD_FAST                'fsize'
            162_0  COME_FROM           158  '158'
              162  STORE_FAST               'end_pos'

 L. 722       164  LOAD_GLOBAL              min
              166  LOAD_FAST                'offset'
              168  LOAD_FAST                'fsize'
              170  CALL_FUNCTION_2       2  ''
              172  STORE_FAST               'offset'

 L. 723       174  LOAD_CONST               0
              176  STORE_FAST               'total_sent'

 L. 724       178  SETUP_FINALLY       292  'to 292'
            180_0  COME_FROM           266  '266'

 L. 726       180  LOAD_GLOBAL              min
              182  LOAD_FAST                'end_pos'
              184  LOAD_FAST                'offset'
              186  BINARY_SUBTRACT  
              188  LOAD_FAST                'blocksize'
              190  CALL_FUNCTION_2       2  ''
              192  STORE_FAST               'blocksize'

 L. 727       194  LOAD_FAST                'blocksize'
              196  LOAD_CONST               0
              198  COMPARE_OP               <=
              200  POP_JUMP_IF_FALSE   226  'to 226'

 L. 728       202  LOAD_FAST                'total_sent'
              204  POP_BLOCK        

 L. 733       206  LOAD_FAST                'total_sent'
              208  LOAD_CONST               0
              210  COMPARE_OP               >
              212  POP_JUMP_IF_FALSE   224  'to 224'

 L. 734       214  LOAD_FAST                'file'
              216  LOAD_METHOD              seek
              218  LOAD_FAST                'offset'
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          
            224_0  COME_FROM           212  '212'

 L. 728       224  RETURN_VALUE     
            226_0  COME_FROM           200  '200'

 L. 729       226  LOAD_FAST                'self'
              228  LOAD_ATTR                _proactor
              230  LOAD_METHOD              sendfile
              232  LOAD_FAST                'sock'
              234  LOAD_FAST                'file'
              236  LOAD_FAST                'offset'
              238  LOAD_FAST                'blocksize'
              240  CALL_METHOD_4         4  ''
              242  GET_AWAITABLE    
              244  LOAD_CONST               None
              246  YIELD_FROM       
              248  POP_TOP          

 L. 730       250  LOAD_FAST                'offset'
              252  LOAD_FAST                'blocksize'
              254  INPLACE_ADD      
              256  STORE_FAST               'offset'

 L. 731       258  LOAD_FAST                'total_sent'
              260  LOAD_FAST                'blocksize'
              262  INPLACE_ADD      
              264  STORE_FAST               'total_sent'
              266  JUMP_BACK           180  'to 180'
              268  POP_BLOCK        

 L. 733       270  LOAD_FAST                'total_sent'
              272  LOAD_CONST               0
              274  COMPARE_OP               >
          276_278  POP_JUMP_IF_FALSE   314  'to 314'

 L. 734       280  LOAD_FAST                'file'
              282  LOAD_METHOD              seek
              284  LOAD_FAST                'offset'
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          
              290  JUMP_FORWARD        314  'to 314'
            292_0  COME_FROM_FINALLY   178  '178'

 L. 733       292  LOAD_FAST                'total_sent'
              294  LOAD_CONST               0
              296  COMPARE_OP               >
          298_300  POP_JUMP_IF_FALSE   312  'to 312'

 L. 734       302  LOAD_FAST                'file'
              304  LOAD_METHOD              seek
              306  LOAD_FAST                'offset'
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          
            312_0  COME_FROM           298  '298'
              312  <48>             
            314_0  COME_FROM           290  '290'
            314_1  COME_FROM           276  '276'

Parse error at or near `<121>' instruction at offset 24

    async def _sendfile_native--- This code section failed: ---

 L. 737         0  LOAD_FAST                'transp'
                2  LOAD_METHOD              is_reading
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'resume_reading'

 L. 738         8  LOAD_FAST                'transp'
               10  LOAD_METHOD              pause_reading
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 739        16  LOAD_FAST                'transp'
               18  LOAD_METHOD              _make_empty_waiter
               20  CALL_METHOD_0         0  ''
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  POP_TOP          

 L. 740        30  SETUP_FINALLY        84  'to 84'

 L. 741        32  LOAD_FAST                'self'
               34  LOAD_ATTR                sock_sendfile
               36  LOAD_FAST                'transp'
               38  LOAD_ATTR                _sock
               40  LOAD_FAST                'file'
               42  LOAD_FAST                'offset'
               44  LOAD_FAST                'count'

 L. 742        46  LOAD_CONST               False

 L. 741        48  LOAD_CONST               ('fallback',)
               50  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               52  GET_AWAITABLE    
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  POP_BLOCK        

 L. 744        60  LOAD_FAST                'transp'
               62  LOAD_METHOD              _reset_empty_waiter
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          

 L. 745        68  LOAD_FAST                'resume_reading'
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 746        72  LOAD_FAST                'transp'
               74  LOAD_METHOD              resume_reading
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          
             80_0  COME_FROM            70  '70'

 L. 741        80  RETURN_VALUE     

 L. 746        82  JUMP_FORWARD        106  'to 106'
             84_0  COME_FROM_FINALLY    30  '30'

 L. 744        84  LOAD_FAST                'transp'
               86  LOAD_METHOD              _reset_empty_waiter
               88  CALL_METHOD_0         0  ''
               90  POP_TOP          

 L. 745        92  LOAD_FAST                'resume_reading'
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 746        96  LOAD_FAST                'transp'
               98  LOAD_METHOD              resume_reading
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          
            104_0  COME_FROM            94  '94'
              104  <48>             
            106_0  COME_FROM            82  '82'

Parse error at or near `LOAD_FAST' instruction at offset 60

    def _close_self_pipe--- This code section failed: ---

 L. 749         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _self_reading_future
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 750        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _self_reading_future
               14  LOAD_METHOD              cancel
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 751        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _self_reading_future
             26_0  COME_FROM             8  '8'

 L. 752        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _ssock
               30  LOAD_METHOD              close
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          

 L. 753        36  LOAD_CONST               None
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _ssock

 L. 754        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _csock
               46  LOAD_METHOD              close
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          

 L. 755        52  LOAD_CONST               None
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _csock

 L. 756        58  LOAD_FAST                'self'
               60  DUP_TOP          
               62  LOAD_ATTR                _internal_fds
               64  LOAD_CONST               1
               66  INPLACE_SUBTRACT 
               68  ROT_TWO          
               70  STORE_ATTR               _internal_fds

Parse error at or near `None' instruction at offset -1

    def _make_self_pipe(self):
        self._ssock, self._csock = socket.socketpair
        self._ssock.setblockingFalse
        self._csock.setblockingFalse
        self._internal_fds += 1

    def _loop_self_reading--- This code section failed: ---

 L. 766         0  SETUP_FINALLY        54  'to 54'

 L. 767         2  LOAD_FAST                'f'
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 768        10  LOAD_FAST                'f'
               12  LOAD_METHOD              result
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 769        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _self_reading_future
               22  LOAD_FAST                'f'
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    34  'to 34'

 L. 776        28  POP_BLOCK        
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            26  '26'

 L. 777        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _proactor
               38  LOAD_METHOD              recv
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _ssock
               44  LOAD_CONST               4096
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'f'
               50  POP_BLOCK        
               52  JUMP_FORWARD        150  'to 150'
             54_0  COME_FROM_FINALLY     0  '0'

 L. 778        54  DUP_TOP          
               56  LOAD_GLOBAL              exceptions
               58  LOAD_ATTR                CancelledError
               60  <121>                74  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 780        68  POP_EXCEPT       
               70  LOAD_CONST               None
               72  RETURN_VALUE     

 L. 781        74  DUP_TOP          
               76  LOAD_GLOBAL              SystemExit
               78  LOAD_GLOBAL              KeyboardInterrupt
               80  BUILD_TUPLE_2         2 
               82  <121>                96  ''
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 782        90  RAISE_VARARGS_0       0  'reraise'
               92  POP_EXCEPT       
               94  JUMP_FORWARD        168  'to 168'

 L. 783        96  DUP_TOP          
               98  LOAD_GLOBAL              BaseException
              100  <121>               148  ''
              102  POP_TOP          
              104  STORE_FAST               'exc'
              106  POP_TOP          
              108  SETUP_FINALLY       140  'to 140'

 L. 784       110  LOAD_FAST                'self'
              112  LOAD_METHOD              call_exception_handler

 L. 785       114  LOAD_STR                 'Error on reading from the event loop self pipe'

 L. 786       116  LOAD_FAST                'exc'

 L. 787       118  LOAD_FAST                'self'

 L. 784       120  LOAD_CONST               ('message', 'exception', 'loop')
              122  BUILD_CONST_KEY_MAP_3     3 
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
              128  POP_BLOCK        
              130  POP_EXCEPT       
              132  LOAD_CONST               None
              134  STORE_FAST               'exc'
              136  DELETE_FAST              'exc'
              138  JUMP_FORWARD        168  'to 168'
            140_0  COME_FROM_FINALLY   108  '108'
              140  LOAD_CONST               None
              142  STORE_FAST               'exc'
              144  DELETE_FAST              'exc'
              146  <48>             
              148  <48>             
            150_0  COME_FROM            52  '52'

 L. 790       150  LOAD_FAST                'f'
              152  LOAD_FAST                'self'
              154  STORE_ATTR               _self_reading_future

 L. 791       156  LOAD_FAST                'f'
              158  LOAD_METHOD              add_done_callback
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                _loop_self_reading
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
            168_0  COME_FROM           138  '138'
            168_1  COME_FROM            94  '94'

Parse error at or near `<117>' instruction at offset 6

    def _write_to_self--- This code section failed: ---

 L. 799         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _csock
                4  STORE_FAST               'csock'

 L. 800         6  LOAD_FAST                'csock'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 801        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 803        18  SETUP_FINALLY        34  'to 34'

 L. 804        20  LOAD_FAST                'csock'
               22  LOAD_METHOD              send
               24  LOAD_CONST               b'\x00'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
               30  POP_BLOCK        
               32  JUMP_FORWARD         72  'to 72'
             34_0  COME_FROM_FINALLY    18  '18'

 L. 805        34  DUP_TOP          
               36  LOAD_GLOBAL              OSError
               38  <121>                70  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 806        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _debug
               50  POP_JUMP_IF_FALSE    66  'to 66'

 L. 807        52  LOAD_GLOBAL              logger
               54  LOAD_ATTR                debug
               56  LOAD_STR                 'Fail to write a null byte into the self-pipe socket'

 L. 809        58  LOAD_CONST               True

 L. 807        60  LOAD_CONST               ('exc_info',)
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  POP_TOP          
             66_0  COME_FROM            50  '50'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            32  '32'

Parse error at or near `<117>' instruction at offset 10

    def _start_serving(self, protocol_factory, sock, sslcontext=None, server=None, backlog=100, ssl_handshake_timeout=None):

        def loop--- This code section failed: ---

 L. 816         0  SETUP_FINALLY       140  'to 140'

 L. 817         2  LOAD_FAST                'f'
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE   110  'to 110'

 L. 818        10  LOAD_FAST                'f'
               12  LOAD_METHOD              result
               14  CALL_METHOD_0         0  ''
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'conn'
               20  STORE_FAST               'addr'

 L. 819        22  LOAD_DEREF               'self'
               24  LOAD_ATTR                _debug
               26  POP_JUMP_IF_FALSE    44  'to 44'

 L. 820        28  LOAD_GLOBAL              logger
               30  LOAD_METHOD              debug
               32  LOAD_STR                 '%r got a new connection from %r: %r'

 L. 821        34  LOAD_DEREF               'server'
               36  LOAD_FAST                'addr'
               38  LOAD_FAST                'conn'

 L. 820        40  CALL_METHOD_4         4  ''
               42  POP_TOP          
             44_0  COME_FROM            26  '26'

 L. 822        44  LOAD_DEREF               'protocol_factory'
               46  CALL_FUNCTION_0       0  ''
               48  STORE_FAST               'protocol'

 L. 823        50  LOAD_DEREF               'sslcontext'
               52  LOAD_CONST               None
               54  <117>                 1  ''
               56  POP_JUMP_IF_FALSE    88  'to 88'

 L. 824        58  LOAD_DEREF               'self'
               60  LOAD_ATTR                _make_ssl_transport

 L. 825        62  LOAD_FAST                'conn'
               64  LOAD_FAST                'protocol'
               66  LOAD_DEREF               'sslcontext'
               68  LOAD_CONST               True

 L. 826        70  LOAD_STR                 'peername'
               72  LOAD_FAST                'addr'
               74  BUILD_MAP_1           1 
               76  LOAD_DEREF               'server'

 L. 827        78  LOAD_DEREF               'ssl_handshake_timeout'

 L. 824        80  LOAD_CONST               ('server_side', 'extra', 'server', 'ssl_handshake_timeout')
               82  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
               84  POP_TOP          
               86  JUMP_FORWARD        110  'to 110'
             88_0  COME_FROM            56  '56'

 L. 829        88  LOAD_DEREF               'self'
               90  LOAD_ATTR                _make_socket_transport

 L. 830        92  LOAD_FAST                'conn'
               94  LOAD_FAST                'protocol'

 L. 831        96  LOAD_STR                 'peername'
               98  LOAD_FAST                'addr'
              100  BUILD_MAP_1           1 
              102  LOAD_DEREF               'server'

 L. 829       104  LOAD_CONST               ('extra', 'server')
              106  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              108  POP_TOP          
            110_0  COME_FROM            86  '86'
            110_1  COME_FROM             8  '8'

 L. 832       110  LOAD_DEREF               'self'
              112  LOAD_METHOD              is_closed
              114  CALL_METHOD_0         0  ''
              116  POP_JUMP_IF_FALSE   124  'to 124'

 L. 833       118  POP_BLOCK        
              120  LOAD_CONST               None
              122  RETURN_VALUE     
            124_0  COME_FROM           116  '116'

 L. 834       124  LOAD_DEREF               'self'
              126  LOAD_ATTR                _proactor
              128  LOAD_METHOD              accept
              130  LOAD_DEREF               'sock'
              132  CALL_METHOD_1         1  ''
              134  STORE_FAST               'f'
              136  POP_BLOCK        
              138  JUMP_FORWARD        272  'to 272'
            140_0  COME_FROM_FINALLY     0  '0'

 L. 835       140  DUP_TOP          
              142  LOAD_GLOBAL              OSError
              144  <121>               242  ''
              146  POP_TOP          
              148  STORE_FAST               'exc'
              150  POP_TOP          
              152  SETUP_FINALLY       234  'to 234'

 L. 836       154  LOAD_DEREF               'sock'
              156  LOAD_METHOD              fileno
              158  CALL_METHOD_0         0  ''
              160  LOAD_CONST               -1
              162  COMPARE_OP               !=
              164  POP_JUMP_IF_FALSE   200  'to 200'

 L. 837       166  LOAD_DEREF               'self'
              168  LOAD_METHOD              call_exception_handler

 L. 838       170  LOAD_STR                 'Accept failed on a socket'

 L. 839       172  LOAD_FAST                'exc'

 L. 840       174  LOAD_GLOBAL              trsock
              176  LOAD_METHOD              TransportSocket
              178  LOAD_DEREF               'sock'
              180  CALL_METHOD_1         1  ''

 L. 837       182  LOAD_CONST               ('message', 'exception', 'socket')
              184  BUILD_CONST_KEY_MAP_3     3 
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L. 842       190  LOAD_DEREF               'sock'
              192  LOAD_METHOD              close
              194  CALL_METHOD_0         0  ''
              196  POP_TOP          
              198  JUMP_FORWARD        222  'to 222'
            200_0  COME_FROM           164  '164'

 L. 843       200  LOAD_DEREF               'self'
              202  LOAD_ATTR                _debug
              204  POP_JUMP_IF_FALSE   222  'to 222'

 L. 844       206  LOAD_GLOBAL              logger
              208  LOAD_ATTR                debug
              210  LOAD_STR                 'Accept failed on socket %r'

 L. 845       212  LOAD_DEREF               'sock'
              214  LOAD_CONST               True

 L. 844       216  LOAD_CONST               ('exc_info',)
              218  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              220  POP_TOP          
            222_0  COME_FROM           204  '204'
            222_1  COME_FROM           198  '198'
              222  POP_BLOCK        
              224  POP_EXCEPT       
              226  LOAD_CONST               None
              228  STORE_FAST               'exc'
              230  DELETE_FAST              'exc'
              232  JUMP_FORWARD        296  'to 296'
            234_0  COME_FROM_FINALLY   152  '152'
              234  LOAD_CONST               None
              236  STORE_FAST               'exc'
              238  DELETE_FAST              'exc'
              240  <48>             

 L. 846       242  DUP_TOP          
              244  LOAD_GLOBAL              exceptions
              246  LOAD_ATTR                CancelledError
          248_250  <121>               270  ''
              252  POP_TOP          
              254  POP_TOP          
              256  POP_TOP          

 L. 847       258  LOAD_DEREF               'sock'
              260  LOAD_METHOD              close
              262  CALL_METHOD_0         0  ''
              264  POP_TOP          
              266  POP_EXCEPT       
              268  JUMP_FORWARD        296  'to 296'
              270  <48>             
            272_0  COME_FROM           138  '138'

 L. 849       272  LOAD_FAST                'f'
              274  LOAD_DEREF               'self'
              276  LOAD_ATTR                _accept_futures
              278  LOAD_DEREF               'sock'
              280  LOAD_METHOD              fileno
              282  CALL_METHOD_0         0  ''
              284  STORE_SUBSCR     

 L. 850       286  LOAD_FAST                'f'
              288  LOAD_METHOD              add_done_callback
              290  LOAD_DEREF               'loop'
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
            296_0  COME_FROM           268  '268'
            296_1  COME_FROM           232  '232'

Parse error at or near `<117>' instruction at offset 6

        self.call_soonloop

    def _process_events(self, event_list):
        pass

    def _stop_accept_futures(self):
        for future in self._accept_futures.values:
            future.cancel
        else:
            self._accept_futures.clear

    def _stop_serving(self, sock):
        future = self._accept_futures.popsock.filenoNone
        if future:
            future.cancel
        self._proactor._stop_servingsock
        sock.close