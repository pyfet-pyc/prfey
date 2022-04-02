# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\streams.py
__all__ = ('StreamReader', 'StreamWriter', 'StreamReaderProtocol', 'open_connection',
           'start_server')
import socket, sys, warnings, weakref
if hasattr(socket, 'AF_UNIX'):
    __all__ += ('open_unix_connection', 'start_unix_server')
from . import coroutines
from . import events
from . import exceptions
from . import format_helpers
from . import protocols
from .log import logger
from .tasks import sleep
_DEFAULT_LIMIT = 65536

async def open_connection--- This code section failed: ---

 L.  44         0  LOAD_FAST                'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  45         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'loop'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L.  47        18  LOAD_GLOBAL              warnings
               20  LOAD_ATTR                warn
               22  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L.  49        24  LOAD_GLOBAL              DeprecationWarning
               26  LOAD_CONST               2

 L.  47        28  LOAD_CONST               ('stacklevel',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  POP_TOP          
             34_0  COME_FROM            16  '16'

 L.  50        34  LOAD_GLOBAL              StreamReader
               36  LOAD_FAST                'limit'
               38  LOAD_FAST                'loop'
               40  LOAD_CONST               ('limit', 'loop')
               42  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               44  STORE_FAST               'reader'

 L.  51        46  LOAD_GLOBAL              StreamReaderProtocol
               48  LOAD_FAST                'reader'
               50  LOAD_FAST                'loop'
               52  LOAD_CONST               ('loop',)
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  STORE_DEREF              'protocol'

 L.  52        58  LOAD_FAST                'loop'
               60  LOAD_ATTR                create_connection

 L.  53        62  LOAD_CLOSURE             'protocol'
               64  BUILD_TUPLE_1         1 
               66  LOAD_LAMBDA              '<code_object <lambda>>'
               68  LOAD_STR                 'open_connection.<locals>.<lambda>'
               70  MAKE_FUNCTION_8          'closure'
               72  LOAD_FAST                'host'
               74  LOAD_FAST                'port'

 L.  52        76  BUILD_TUPLE_3         3 
               78  BUILD_MAP_0           0 

 L.  53        80  LOAD_FAST                'kwds'

 L.  52        82  <164>                 1  ''
               84  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               86  GET_AWAITABLE    
               88  LOAD_CONST               None
               90  YIELD_FROM       
               92  UNPACK_SEQUENCE_2     2 
               94  STORE_FAST               'transport'
               96  STORE_FAST               '_'

 L.  54        98  LOAD_GLOBAL              StreamWriter
              100  LOAD_FAST                'transport'
              102  LOAD_DEREF               'protocol'
              104  LOAD_FAST                'reader'
              106  LOAD_FAST                'loop'
              108  CALL_FUNCTION_4       4  ''
              110  STORE_FAST               'writer'

 L.  55       112  LOAD_FAST                'reader'
              114  LOAD_FAST                'writer'
              116  BUILD_TUPLE_2         2 
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


async def start_server--- This code section failed: ---

 L.  81         0  LOAD_DEREF               'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  82         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  STORE_DEREF              'loop'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L.  84        18  LOAD_GLOBAL              warnings
               20  LOAD_ATTR                warn
               22  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L.  86        24  LOAD_GLOBAL              DeprecationWarning
               26  LOAD_CONST               2

 L.  84        28  LOAD_CONST               ('stacklevel',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  POP_TOP          
             34_0  COME_FROM            16  '16'

 L.  88        34  LOAD_CLOSURE             'client_connected_cb'
               36  LOAD_CLOSURE             'limit'
               38  LOAD_CLOSURE             'loop'
               40  BUILD_TUPLE_3         3 
               42  LOAD_CODE                <code_object factory>
               44  LOAD_STR                 'start_server.<locals>.factory'
               46  MAKE_FUNCTION_8          'closure'
               48  STORE_FAST               'factory'

 L.  94        50  LOAD_DEREF               'loop'
               52  LOAD_ATTR                create_server
               54  LOAD_FAST                'factory'
               56  LOAD_FAST                'host'
               58  LOAD_FAST                'port'
               60  BUILD_TUPLE_3         3 
               62  BUILD_MAP_0           0 
               64  LOAD_FAST                'kwds'
               66  <164>                 1  ''
               68  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               70  GET_AWAITABLE    
               72  LOAD_CONST               None
               74  YIELD_FROM       
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


if hasattr(socket, 'AF_UNIX'):

    async def open_unix_connection--- This code section failed: ---

 L. 103         0  LOAD_FAST                'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 104         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'loop'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L. 106        18  LOAD_GLOBAL              warnings
               20  LOAD_ATTR                warn
               22  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L. 108        24  LOAD_GLOBAL              DeprecationWarning
               26  LOAD_CONST               2

 L. 106        28  LOAD_CONST               ('stacklevel',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  POP_TOP          
             34_0  COME_FROM            16  '16'

 L. 109        34  LOAD_GLOBAL              StreamReader
               36  LOAD_FAST                'limit'
               38  LOAD_FAST                'loop'
               40  LOAD_CONST               ('limit', 'loop')
               42  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               44  STORE_FAST               'reader'

 L. 110        46  LOAD_GLOBAL              StreamReaderProtocol
               48  LOAD_FAST                'reader'
               50  LOAD_FAST                'loop'
               52  LOAD_CONST               ('loop',)
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  STORE_DEREF              'protocol'

 L. 111        58  LOAD_FAST                'loop'
               60  LOAD_ATTR                create_unix_connection

 L. 112        62  LOAD_CLOSURE             'protocol'
               64  BUILD_TUPLE_1         1 
               66  LOAD_LAMBDA              '<code_object <lambda>>'
               68  LOAD_STR                 'open_unix_connection.<locals>.<lambda>'
               70  MAKE_FUNCTION_8          'closure'
               72  LOAD_FAST                'path'

 L. 111        74  BUILD_TUPLE_2         2 
               76  BUILD_MAP_0           0 

 L. 112        78  LOAD_FAST                'kwds'

 L. 111        80  <164>                 1  ''
               82  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               84  GET_AWAITABLE    
               86  LOAD_CONST               None
               88  YIELD_FROM       
               90  UNPACK_SEQUENCE_2     2 
               92  STORE_FAST               'transport'
               94  STORE_FAST               '_'

 L. 113        96  LOAD_GLOBAL              StreamWriter
               98  LOAD_FAST                'transport'
              100  LOAD_DEREF               'protocol'
              102  LOAD_FAST                'reader'
              104  LOAD_FAST                'loop'
              106  CALL_FUNCTION_4       4  ''
              108  STORE_FAST               'writer'

 L. 114       110  LOAD_FAST                'reader'
              112  LOAD_FAST                'writer'
              114  BUILD_TUPLE_2         2 
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


    async def start_unix_server--- This code section failed: ---

 L. 119         0  LOAD_DEREF               'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 120         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  STORE_DEREF              'loop'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L. 122        18  LOAD_GLOBAL              warnings
               20  LOAD_ATTR                warn
               22  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L. 124        24  LOAD_GLOBAL              DeprecationWarning
               26  LOAD_CONST               2

 L. 122        28  LOAD_CONST               ('stacklevel',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  POP_TOP          
             34_0  COME_FROM            16  '16'

 L. 126        34  LOAD_CLOSURE             'client_connected_cb'
               36  LOAD_CLOSURE             'limit'
               38  LOAD_CLOSURE             'loop'
               40  BUILD_TUPLE_3         3 
               42  LOAD_CODE                <code_object factory>
               44  LOAD_STR                 'start_unix_server.<locals>.factory'
               46  MAKE_FUNCTION_8          'closure'
               48  STORE_FAST               'factory'

 L. 132        50  LOAD_DEREF               'loop'
               52  LOAD_ATTR                create_unix_server
               54  LOAD_FAST                'factory'
               56  LOAD_FAST                'path'
               58  BUILD_TUPLE_2         2 
               60  BUILD_MAP_0           0 
               62  LOAD_FAST                'kwds'
               64  <164>                 1  ''
               66  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               68  GET_AWAITABLE    
               70  LOAD_CONST               None
               72  YIELD_FROM       
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class FlowControlMixin(protocols.Protocol):
    __doc__ = 'Reusable flow control logic for StreamWriter.drain().\n\n    This implements the protocol methods pause_writing(),\n    resume_writing() and connection_lost().  If the subclass overrides\n    these it must call the super methods.\n\n    StreamWriter.drain() must wait for _drain_helper() coroutine.\n    '

    def __init__--- This code section failed: ---

 L. 146         0  LOAD_FAST                'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 147         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _loop
               18  JUMP_FORWARD         26  'to 26'
             20_0  COME_FROM             6  '6'

 L. 149        20  LOAD_FAST                'loop'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _loop
             26_0  COME_FROM            18  '18'

 L. 150        26  LOAD_CONST               False
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _paused

 L. 151        32  LOAD_CONST               None
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _drain_waiter

 L. 152        38  LOAD_CONST               False
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _connection_lost

Parse error at or near `None' instruction at offset -1

    def pause_writing--- This code section failed: ---

 L. 155         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _paused
                4  POP_JUMP_IF_FALSE    10  'to 10'
                6  <74>             
                8  RAISE_VARARGS_1       1  'exception instance'
             10_0  COME_FROM             4  '4'

 L. 156        10  LOAD_CONST               True
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _paused

 L. 157        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _loop
               20  LOAD_METHOD              get_debug
               22  CALL_METHOD_0         0  ''
               24  POP_JUMP_IF_FALSE    38  'to 38'

 L. 158        26  LOAD_GLOBAL              logger
               28  LOAD_METHOD              debug
               30  LOAD_STR                 '%r pauses writing'
               32  LOAD_FAST                'self'
               34  CALL_METHOD_2         2  ''
               36  POP_TOP          
             38_0  COME_FROM            24  '24'

Parse error at or near `None' instruction at offset -1

    def resume_writing--- This code section failed: ---

 L. 161         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _paused
                4  POP_JUMP_IF_TRUE     10  'to 10'
                6  <74>             
                8  RAISE_VARARGS_1       1  'exception instance'
             10_0  COME_FROM             4  '4'

 L. 162        10  LOAD_CONST               False
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _paused

 L. 163        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _loop
               20  LOAD_METHOD              get_debug
               22  CALL_METHOD_0         0  ''
               24  POP_JUMP_IF_FALSE    38  'to 38'

 L. 164        26  LOAD_GLOBAL              logger
               28  LOAD_METHOD              debug
               30  LOAD_STR                 '%r resumes writing'
               32  LOAD_FAST                'self'
               34  CALL_METHOD_2         2  ''
               36  POP_TOP          
             38_0  COME_FROM            24  '24'

 L. 166        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _drain_waiter
               42  STORE_FAST               'waiter'

 L. 167        44  LOAD_FAST                'waiter'
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE    76  'to 76'

 L. 168        52  LOAD_CONST               None
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _drain_waiter

 L. 169        58  LOAD_FAST                'waiter'
               60  LOAD_METHOD              done
               62  CALL_METHOD_0         0  ''
               64  POP_JUMP_IF_TRUE     76  'to 76'

 L. 170        66  LOAD_FAST                'waiter'
               68  LOAD_METHOD              set_result
               70  LOAD_CONST               None
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            50  '50'

Parse error at or near `None' instruction at offset -1

    def connection_lost--- This code section failed: ---

 L. 173         0  LOAD_CONST               True
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _connection_lost

 L. 175         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _paused
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L. 176        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 177        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _drain_waiter
               20  STORE_FAST               'waiter'

 L. 178        22  LOAD_FAST                'waiter'
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    34  'to 34'

 L. 179        30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'

 L. 180        34  LOAD_CONST               None
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _drain_waiter

 L. 181        40  LOAD_FAST                'waiter'
               42  LOAD_METHOD              done
               44  CALL_METHOD_0         0  ''
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L. 182        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'

 L. 183        52  LOAD_FAST                'exc'
               54  LOAD_CONST               None
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    72  'to 72'

 L. 184        60  LOAD_FAST                'waiter'
               62  LOAD_METHOD              set_result
               64  LOAD_CONST               None
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
               70  JUMP_FORWARD         82  'to 82'
             72_0  COME_FROM            58  '58'

 L. 186        72  LOAD_FAST                'waiter'
               74  LOAD_METHOD              set_exception
               76  LOAD_FAST                'exc'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            70  '70'

Parse error at or near `<117>' instruction at offset 26

    async def _drain_helper--- This code section failed: ---

 L. 189         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _connection_lost
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 190         6  LOAD_GLOBAL              ConnectionResetError
                8  LOAD_STR                 'Connection lost'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 191        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _paused
               18  POP_JUMP_IF_TRUE     24  'to 24'

 L. 192        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 193        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _drain_waiter
               28  STORE_FAST               'waiter'

 L. 194        30  LOAD_FAST                'waiter'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_TRUE     50  'to 50'
               38  LOAD_FAST                'waiter'
               40  LOAD_METHOD              cancelled
               42  CALL_METHOD_0         0  ''
               44  POP_JUMP_IF_TRUE     50  'to 50'
               46  <74>             
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            44  '44'
             50_1  COME_FROM            36  '36'

 L. 195        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _loop
               54  LOAD_METHOD              create_future
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'waiter'

 L. 196        60  LOAD_FAST                'waiter'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _drain_waiter

 L. 197        66  LOAD_FAST                'waiter'
               68  GET_AWAITABLE    
               70  LOAD_CONST               None
               72  YIELD_FROM       
               74  POP_TOP          

Parse error at or near `<117>' instruction at offset 34

    def _get_close_waiter(self, stream):
        raise NotImplementedError


class StreamReaderProtocol(FlowControlMixin, protocols.Protocol):
    __doc__ = 'Helper class to adapt between Protocol and StreamReader.\n\n    (This is a helper class instead of making StreamReader itself a\n    Protocol subclass, because the StreamReader has other potential\n    uses, and to prevent the user of the StreamReader to accidentally\n    call inappropriate methods of the protocol.)\n    '
    _source_traceback = None

    def __init__--- This code section failed: ---

 L. 215         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'loop'
                8  LOAD_CONST               ('loop',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_TOP          

 L. 216        14  LOAD_FAST                'stream_reader'
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    44  'to 44'

 L. 217        22  LOAD_GLOBAL              weakref
               24  LOAD_METHOD              ref
               26  LOAD_FAST                'stream_reader'
               28  CALL_METHOD_1         1  ''
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _stream_reader_wr

 L. 218        34  LOAD_FAST                'stream_reader'
               36  LOAD_ATTR                _source_traceback
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _source_traceback
               42  JUMP_FORWARD         50  'to 50'
             44_0  COME_FROM            20  '20'

 L. 220        44  LOAD_CONST               None
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _stream_reader_wr
             50_0  COME_FROM            42  '42'

 L. 221        50  LOAD_FAST                'client_connected_cb'
               52  LOAD_CONST               None
               54  <117>                 1  ''
               56  POP_JUMP_IF_FALSE    64  'to 64'

 L. 225        58  LOAD_FAST                'stream_reader'
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _strong_reader
             64_0  COME_FROM            56  '56'

 L. 226        64  LOAD_CONST               False
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _reject_connection

 L. 227        70  LOAD_CONST               None
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _stream_writer

 L. 228        76  LOAD_CONST               None
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _transport

 L. 229        82  LOAD_FAST                'client_connected_cb'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _client_connected_cb

 L. 230        88  LOAD_CONST               False
               90  LOAD_FAST                'self'
               92  STORE_ATTR               _over_ssl

 L. 231        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _loop
               98  LOAD_METHOD              create_future
              100  CALL_METHOD_0         0  ''
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _closed

Parse error at or near `<117>' instruction at offset 18

    @property
    def _stream_reader--- This code section failed: ---

 L. 235         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _stream_reader_wr
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 236        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 237        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _stream_reader_wr
               18  CALL_METHOD_0         0  ''
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def connection_made--- This code section failed: ---

 L. 240         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _reject_connection
                4  POP_JUMP_IF_FALSE    54  'to 54'

 L. 242         6  LOAD_STR                 'message'
                8  LOAD_STR                 'An open stream was garbage collected prior to establishing network connection; call "stream.close()" explicitly.'

 L. 241        10  BUILD_MAP_1           1 
               12  STORE_FAST               'context'

 L. 246        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _source_traceback
               18  POP_JUMP_IF_FALSE    30  'to 30'

 L. 247        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _source_traceback
               24  LOAD_FAST                'context'
               26  LOAD_STR                 'source_traceback'
               28  STORE_SUBSCR     
             30_0  COME_FROM            18  '18'

 L. 248        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _loop
               34  LOAD_METHOD              call_exception_handler
               36  LOAD_FAST                'context'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 249        42  LOAD_FAST                'transport'
               44  LOAD_METHOD              abort
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          

 L. 250        50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM             4  '4'

 L. 251        54  LOAD_FAST                'transport'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _transport

 L. 252        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _stream_reader
               64  STORE_FAST               'reader'

 L. 253        66  LOAD_FAST                'reader'
               68  LOAD_CONST               None
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    84  'to 84'

 L. 254        74  LOAD_FAST                'reader'
               76  LOAD_METHOD              set_transport
               78  LOAD_FAST                'transport'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
             84_0  COME_FROM            72  '72'

 L. 255        84  LOAD_FAST                'transport'
               86  LOAD_METHOD              get_extra_info
               88  LOAD_STR                 'sslcontext'
               90  CALL_METHOD_1         1  ''
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  LOAD_FAST                'self'
               98  STORE_ATTR               _over_ssl

 L. 256       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _client_connected_cb
              104  LOAD_CONST               None
              106  <117>                 1  ''
              108  POP_JUMP_IF_FALSE   170  'to 170'

 L. 257       110  LOAD_GLOBAL              StreamWriter
              112  LOAD_FAST                'transport'
              114  LOAD_FAST                'self'

 L. 258       116  LOAD_FAST                'reader'

 L. 259       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _loop

 L. 257       122  CALL_FUNCTION_4       4  ''
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _stream_writer

 L. 260       128  LOAD_FAST                'self'
              130  LOAD_METHOD              _client_connected_cb
              132  LOAD_FAST                'reader'

 L. 261       134  LOAD_FAST                'self'
              136  LOAD_ATTR                _stream_writer

 L. 260       138  CALL_METHOD_2         2  ''
              140  STORE_FAST               'res'

 L. 262       142  LOAD_GLOBAL              coroutines
              144  LOAD_METHOD              iscoroutine
              146  LOAD_FAST                'res'
              148  CALL_METHOD_1         1  ''
              150  POP_JUMP_IF_FALSE   164  'to 164'

 L. 263       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _loop
              156  LOAD_METHOD              create_task
              158  LOAD_FAST                'res'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
            164_0  COME_FROM           150  '150'

 L. 264       164  LOAD_CONST               None
              166  LOAD_FAST                'self'
              168  STORE_ATTR               _strong_reader
            170_0  COME_FROM           108  '108'

Parse error at or near `<117>' instruction at offset 70

    def connection_lost--- This code section failed: ---

 L. 267         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _stream_reader
                4  STORE_FAST               'reader'

 L. 268         6  LOAD_FAST                'reader'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    42  'to 42'

 L. 269        14  LOAD_FAST                'exc'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 270        22  LOAD_FAST                'reader'
               24  LOAD_METHOD              feed_eof
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          
               30  JUMP_FORWARD         42  'to 42'
             32_0  COME_FROM            20  '20'

 L. 272        32  LOAD_FAST                'reader'
               34  LOAD_METHOD              set_exception
               36  LOAD_FAST                'exc'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
             42_0  COME_FROM            30  '30'
             42_1  COME_FROM            12  '12'

 L. 273        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _closed
               46  LOAD_METHOD              done
               48  CALL_METHOD_0         0  ''
               50  POP_JUMP_IF_TRUE     86  'to 86'

 L. 274        52  LOAD_FAST                'exc'
               54  LOAD_CONST               None
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    74  'to 74'

 L. 275        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _closed
               64  LOAD_METHOD              set_result
               66  LOAD_CONST               None
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
               72  JUMP_FORWARD         86  'to 86'
             74_0  COME_FROM            58  '58'

 L. 277        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _closed
               78  LOAD_METHOD              set_exception
               80  LOAD_FAST                'exc'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
             86_0  COME_FROM            72  '72'
             86_1  COME_FROM            50  '50'

 L. 278        86  LOAD_GLOBAL              super
               88  CALL_FUNCTION_0       0  ''
               90  LOAD_METHOD              connection_lost
               92  LOAD_FAST                'exc'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 279        98  LOAD_CONST               None
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _stream_reader_wr

 L. 280       104  LOAD_CONST               None
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _stream_writer

 L. 281       110  LOAD_CONST               None
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _transport

Parse error at or near `<117>' instruction at offset 10

    def data_received--- This code section failed: ---

 L. 284         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _stream_reader
                4  STORE_FAST               'reader'

 L. 285         6  LOAD_FAST                'reader'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    24  'to 24'

 L. 286        14  LOAD_FAST                'reader'
               16  LOAD_METHOD              feed_data
               18  LOAD_FAST                'data'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          
             24_0  COME_FROM            12  '12'

Parse error at or near `<117>' instruction at offset 10

    def eof_received--- This code section failed: ---

 L. 289         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _stream_reader
                4  STORE_FAST               'reader'

 L. 290         6  LOAD_FAST                'reader'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 291        14  LOAD_FAST                'reader'
               16  LOAD_METHOD              feed_eof
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          
             22_0  COME_FROM            12  '12'

 L. 292        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _over_ssl
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 296        28  LOAD_CONST               False
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 297        32  LOAD_CONST               True
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def _get_close_waiter(self, stream):
        return self._closed

    def __del__(self):
        closed = self._closed
        if closed.done:
            if not closed.cancelled:
                closed.exception


class StreamWriter:
    __doc__ = 'Wraps a Transport.\n\n    This exposes write(), writelines(), [can_]write_eof(),\n    get_extra_info() and close().  It adds drain() which returns an\n    optional Future on which you can wait for flow control.  It also\n    adds a transport property which references the Transport\n    directly.\n    '

    def __init__--- This code section failed: ---

 L. 321         0  LOAD_FAST                'transport'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _transport

 L. 322         6  LOAD_FAST                'protocol'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _protocol

 L. 324        12  LOAD_FAST                'reader'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_TRUE     34  'to 34'
               20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'reader'
               24  LOAD_GLOBAL              StreamReader
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  <74>             
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            28  '28'
             34_1  COME_FROM            18  '18'

 L. 325        34  LOAD_FAST                'reader'
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _reader

 L. 326        40  LOAD_FAST                'loop'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _loop

 L. 327        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _loop
               50  LOAD_METHOD              create_future
               52  CALL_METHOD_0         0  ''
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _complete_fut

 L. 328        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _complete_fut
               62  LOAD_METHOD              set_result
               64  LOAD_CONST               None
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

Parse error at or near `<117>' instruction at offset 16

    def __repr__--- This code section failed: ---

 L. 331         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_ATTR                __name__
                6  LOAD_STR                 'transport='
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _transport
               12  FORMAT_VALUE          2  '!r'
               14  BUILD_STRING_2        2 
               16  BUILD_LIST_2          2 
               18  STORE_FAST               'info'

 L. 332        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _reader
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    48  'to 48'

 L. 333        30  LOAD_FAST                'info'
               32  LOAD_METHOD              append
               34  LOAD_STR                 'reader='
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _reader
               40  FORMAT_VALUE          2  '!r'
               42  BUILD_STRING_2        2 
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            28  '28'

 L. 334        48  LOAD_STR                 '<{}>'
               50  LOAD_METHOD              format
               52  LOAD_STR                 ' '
               54  LOAD_METHOD              join
               56  LOAD_FAST                'info'
               58  CALL_METHOD_1         1  ''
               60  CALL_METHOD_1         1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    @property
    def transport(self):
        return self._transport

    def write(self, data):
        self._transport.writedata

    def writelines(self, data):
        self._transport.writelinesdata

    def write_eof(self):
        return self._transport.write_eof

    def can_write_eof(self):
        return self._transport.can_write_eof

    def close(self):
        return self._transport.close

    def is_closing(self):
        return self._transport.is_closing

    async def wait_closed(self):
        await self._protocol._get_close_waiterself

    def get_extra_info(self, name, default=None):
        return self._transport.get_extra_infonamedefault

    async def drain--- This code section failed: ---

 L. 372         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _reader
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L. 373        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _reader
               14  LOAD_METHOD              exception
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'exc'

 L. 374        20  LOAD_FAST                'exc'
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 375        28  LOAD_FAST                'exc'
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            26  '26'
             32_1  COME_FROM             8  '8'

 L. 376        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _transport
               36  LOAD_METHOD              is_closing
               38  CALL_METHOD_0         0  ''
               40  POP_JUMP_IF_FALSE    56  'to 56'

 L. 386        42  LOAD_GLOBAL              sleep
               44  LOAD_CONST               0
               46  CALL_FUNCTION_1       1  ''
               48  GET_AWAITABLE    
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  POP_TOP          
             56_0  COME_FROM            40  '40'

 L. 387        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _protocol
               60  LOAD_METHOD              _drain_helper
               62  CALL_METHOD_0         0  ''
               64  GET_AWAITABLE    
               66  LOAD_CONST               None
               68  YIELD_FROM       
               70  POP_TOP          

Parse error at or near `None' instruction at offset -1


class StreamReader:
    _source_traceback = None

    def __init__--- This code section failed: ---

 L. 398         0  LOAD_FAST                'limit'
                2  LOAD_CONST               0
                4  COMPARE_OP               <=
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 399         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Limit cannot be <= 0'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 401        16  LOAD_FAST                'limit'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _limit

 L. 402        22  LOAD_FAST                'loop'
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L. 403        30  LOAD_GLOBAL              events
               32  LOAD_METHOD              get_event_loop
               34  CALL_METHOD_0         0  ''
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _loop
               40  JUMP_FORWARD         48  'to 48'
             42_0  COME_FROM            28  '28'

 L. 405        42  LOAD_FAST                'loop'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _loop
             48_0  COME_FROM            40  '40'

 L. 406        48  LOAD_GLOBAL              bytearray
               50  CALL_FUNCTION_0       0  ''
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _buffer

 L. 407        56  LOAD_CONST               False
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _eof

 L. 408        62  LOAD_CONST               None
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _waiter

 L. 409        68  LOAD_CONST               None
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _exception

 L. 410        74  LOAD_CONST               None
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _transport

 L. 411        80  LOAD_CONST               False
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _paused

 L. 412        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _loop
               90  LOAD_METHOD              get_debug
               92  CALL_METHOD_0         0  ''
               94  POP_JUMP_IF_FALSE   114  'to 114'

 L. 413        96  LOAD_GLOBAL              format_helpers
               98  LOAD_METHOD              extract_stack

 L. 414       100  LOAD_GLOBAL              sys
              102  LOAD_METHOD              _getframe
              104  LOAD_CONST               1
              106  CALL_METHOD_1         1  ''

 L. 413       108  CALL_METHOD_1         1  ''
              110  LOAD_FAST                'self'
              112  STORE_ATTR               _source_traceback
            114_0  COME_FROM            94  '94'

Parse error at or near `<117>' instruction at offset 26

    def __repr__(self):
        info = [
         'StreamReader']
        if self._buffer:
            info.appendf"{len(self._buffer)} bytes"
        if self._eof:
            info.append'eof'
        if self._limit != _DEFAULT_LIMIT:
            info.appendf"limit={self._limit}"
        if self._waiter:
            info.appendf"waiter={self._waiter!r}"
        if self._exception:
            info.appendf"exception={self._exception!r}"
        if self._transport:
            info.appendf"transport={self._transport!r}"
        if self._paused:
            info.append'paused'
        return '<{}>'.format' '.joininfo

    def exception(self):
        return self._exception

    def set_exception--- This code section failed: ---

 L. 438         0  LOAD_FAST                'exc'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _exception

 L. 440         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _waiter
               10  STORE_FAST               'waiter'

 L. 441        12  LOAD_FAST                'waiter'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    44  'to 44'

 L. 442        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _waiter

 L. 443        26  LOAD_FAST                'waiter'
               28  LOAD_METHOD              cancelled
               30  CALL_METHOD_0         0  ''
               32  POP_JUMP_IF_TRUE     44  'to 44'

 L. 444        34  LOAD_FAST                'waiter'
               36  LOAD_METHOD              set_exception
               38  LOAD_FAST                'exc'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
             44_0  COME_FROM            32  '32'
             44_1  COME_FROM            18  '18'

Parse error at or near `<117>' instruction at offset 16

    def _wakeup_waiter--- This code section failed: ---

 L. 448         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _waiter
                4  STORE_FAST               'waiter'

 L. 449         6  LOAD_FAST                'waiter'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    38  'to 38'

 L. 450        14  LOAD_CONST               None
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _waiter

 L. 451        20  LOAD_FAST                'waiter'
               22  LOAD_METHOD              cancelled
               24  CALL_METHOD_0         0  ''
               26  POP_JUMP_IF_TRUE     38  'to 38'

 L. 452        28  LOAD_FAST                'waiter'
               30  LOAD_METHOD              set_result
               32  LOAD_CONST               None
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
             38_0  COME_FROM            26  '26'
             38_1  COME_FROM            12  '12'

Parse error at or near `<117>' instruction at offset 10

    def set_transport--- This code section failed: ---

 L. 455         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _transport
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'
               10  <74>             
               12  LOAD_STR                 'Transport already set'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 456        18  LOAD_FAST                'transport'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _transport

Parse error at or near `None' instruction at offset -1

    def _maybe_resume_transport(self):
        if self._paused:
            if len(self._buffer) <= self._limit:
                self._paused = False
                self._transport.resume_reading

    def feed_eof(self):
        self._eof = True
        self._wakeup_waiter

    def at_eof(self):
        """Return True if the buffer is empty and 'feed_eof' was called."""
        return self._eof and not self._buffer

    def feed_data--- This code section failed: ---

 L. 472         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _eof
                4  POP_JUMP_IF_FALSE    14  'to 14'
                6  <74>             
                8  LOAD_STR                 'feed_data after feed_eof'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 474        14  LOAD_FAST                'data'
               16  POP_JUMP_IF_TRUE     22  'to 22'

 L. 475        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 477        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _buffer
               26  LOAD_METHOD              extend
               28  LOAD_FAST                'data'
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 478        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _wakeup_waiter
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 480        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _transport
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE   124  'to 124'

 L. 481        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _paused

 L. 480        56  POP_JUMP_IF_TRUE    124  'to 124'

 L. 482        58  LOAD_GLOBAL              len
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _buffer
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_CONST               2
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _limit
               72  BINARY_MULTIPLY  
               74  COMPARE_OP               >

 L. 480        76  POP_JUMP_IF_FALSE   124  'to 124'

 L. 483        78  SETUP_FINALLY        94  'to 94'

 L. 484        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _transport
               84  LOAD_METHOD              pause_reading
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          
               90  POP_BLOCK        
               92  JUMP_FORWARD        118  'to 118'
             94_0  COME_FROM_FINALLY    78  '78'

 L. 485        94  DUP_TOP          
               96  LOAD_GLOBAL              NotImplementedError
               98  <121>               116  ''
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 489       106  LOAD_CONST               None
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _transport
              112  POP_EXCEPT       
              114  JUMP_FORWARD        124  'to 124'
              116  <48>             
            118_0  COME_FROM            92  '92'

 L. 491       118  LOAD_CONST               True
              120  LOAD_FAST                'self'
              122  STORE_ATTR               _paused
            124_0  COME_FROM           114  '114'
            124_1  COME_FROM            76  '76'
            124_2  COME_FROM            56  '56'
            124_3  COME_FROM            50  '50'

Parse error at or near `None' instruction at offset -1

    async def _wait_for_data--- This code section failed: ---

 L. 502         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _waiter
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 503        10  LOAD_GLOBAL              RuntimeError

 L. 504        12  LOAD_FAST                'func_name'
               14  FORMAT_VALUE          0  ''
               16  LOAD_STR                 '() called while another coroutine is already waiting for incoming data'
               18  BUILD_STRING_2        2 

 L. 503        20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM             8  '8'

 L. 507        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _eof
               28  POP_JUMP_IF_FALSE    38  'to 38'
               30  <74>             
               32  LOAD_STR                 '_wait_for_data after EOF'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 511        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _paused
               42  POP_JUMP_IF_FALSE    60  'to 60'

 L. 512        44  LOAD_CONST               False
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _paused

 L. 513        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _transport
               54  LOAD_METHOD              resume_reading
               56  CALL_METHOD_0         0  ''
               58  POP_TOP          
             60_0  COME_FROM            42  '42'

 L. 515        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _loop
               64  LOAD_METHOD              create_future
               66  CALL_METHOD_0         0  ''
               68  LOAD_FAST                'self'
               70  STORE_ATTR               _waiter

 L. 516        72  SETUP_FINALLY        96  'to 96'

 L. 517        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _waiter
               78  GET_AWAITABLE    
               80  LOAD_CONST               None
               82  YIELD_FROM       
               84  POP_TOP          
               86  POP_BLOCK        

 L. 519        88  LOAD_CONST               None
               90  LOAD_FAST                'self'
               92  STORE_ATTR               _waiter
               94  JUMP_FORWARD        104  'to 104'
             96_0  COME_FROM_FINALLY    72  '72'
               96  LOAD_CONST               None
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _waiter
              102  <48>             
            104_0  COME_FROM            94  '94'

Parse error at or near `None' instruction at offset -1

    async def readline--- This code section failed: ---

 L. 537         0  LOAD_CONST               b'\n'
                2  STORE_FAST               'sep'

 L. 538         4  LOAD_GLOBAL              len
                6  LOAD_FAST                'sep'
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'seplen'

 L. 539        12  SETUP_FINALLY        34  'to 34'

 L. 540        14  LOAD_FAST                'self'
               16  LOAD_METHOD              readuntil
               18  LOAD_FAST                'sep'
               20  CALL_METHOD_1         1  ''
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  STORE_FAST               'line'
               30  POP_BLOCK        
               32  JUMP_FORWARD        182  'to 182'
             34_0  COME_FROM_FINALLY    12  '12'

 L. 541        34  DUP_TOP          
               36  LOAD_GLOBAL              exceptions
               38  LOAD_ATTR                IncompleteReadError
               40  <121>                76  ''
               42  POP_TOP          
               44  STORE_FAST               'e'
               46  POP_TOP          
               48  SETUP_FINALLY        68  'to 68'

 L. 542        50  LOAD_FAST                'e'
               52  LOAD_ATTR                partial
               54  POP_BLOCK        
               56  ROT_FOUR         
               58  POP_EXCEPT       
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY    48  '48'
               68  LOAD_CONST               None
               70  STORE_FAST               'e'
               72  DELETE_FAST              'e'
               74  <48>             

 L. 543        76  DUP_TOP          
               78  LOAD_GLOBAL              exceptions
               80  LOAD_ATTR                LimitOverrunError
               82  <121>               180  ''
               84  POP_TOP          
               86  STORE_FAST               'e'
               88  POP_TOP          
               90  SETUP_FINALLY       172  'to 172'

 L. 544        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _buffer
               96  LOAD_METHOD              startswith
               98  LOAD_FAST                'sep'
              100  LOAD_FAST                'e'
              102  LOAD_ATTR                consumed
              104  CALL_METHOD_2         2  ''
              106  POP_JUMP_IF_FALSE   128  'to 128'

 L. 545       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _buffer
              112  LOAD_CONST               None
              114  LOAD_FAST                'e'
              116  LOAD_ATTR                consumed
              118  LOAD_FAST                'seplen'
              120  BINARY_ADD       
              122  BUILD_SLICE_2         2 
              124  DELETE_SUBSCR    
              126  JUMP_FORWARD        138  'to 138'
            128_0  COME_FROM           106  '106'

 L. 547       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _buffer
              132  LOAD_METHOD              clear
              134  CALL_METHOD_0         0  ''
              136  POP_TOP          
            138_0  COME_FROM           126  '126'

 L. 548       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _maybe_resume_transport
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          

 L. 549       146  LOAD_GLOBAL              ValueError
              148  LOAD_FAST                'e'
              150  LOAD_ATTR                args
              152  LOAD_CONST               0
              154  BINARY_SUBSCR    
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
              160  POP_BLOCK        
              162  POP_EXCEPT       
              164  LOAD_CONST               None
              166  STORE_FAST               'e'
              168  DELETE_FAST              'e'
              170  JUMP_FORWARD        182  'to 182'
            172_0  COME_FROM_FINALLY    90  '90'
              172  LOAD_CONST               None
              174  STORE_FAST               'e'
              176  DELETE_FAST              'e'
              178  <48>             
              180  <48>             
            182_0  COME_FROM           170  '170'
            182_1  COME_FROM            32  '32'

 L. 550       182  LOAD_FAST                'line'
              184  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 40

    async def readuntil--- This code section failed: ---

 L. 572         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'separator'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'seplen'

 L. 573         8  LOAD_FAST                'seplen'
               10  LOAD_CONST               0
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 574        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'Separator should be at least one-byte string'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 576        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _exception
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L. 577        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _exception
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            32  '32'

 L. 598        40  LOAD_CONST               0
               42  STORE_FAST               'offset'
             44_0  COME_FROM           178  '178'

 L. 603        44  LOAD_GLOBAL              len
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _buffer
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'buflen'

 L. 607        54  LOAD_FAST                'buflen'
               56  LOAD_FAST                'offset'
               58  BINARY_SUBTRACT  
               60  LOAD_FAST                'seplen'
               62  COMPARE_OP               >=
               64  POP_JUMP_IF_FALSE   124  'to 124'

 L. 608        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _buffer
               70  LOAD_METHOD              find
               72  LOAD_FAST                'separator'
               74  LOAD_FAST                'offset'
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'isep'

 L. 610        80  LOAD_FAST                'isep'
               82  LOAD_CONST               -1
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE    90  'to 90'

 L. 613        88  JUMP_FORWARD        180  'to 180'
             90_0  COME_FROM            86  '86'

 L. 616        90  LOAD_FAST                'buflen'
               92  LOAD_CONST               1
               94  BINARY_ADD       
               96  LOAD_FAST                'seplen'
               98  BINARY_SUBTRACT  
              100  STORE_FAST               'offset'

 L. 617       102  LOAD_FAST                'offset'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _limit
              108  COMPARE_OP               >
              110  POP_JUMP_IF_FALSE   124  'to 124'

 L. 618       112  LOAD_GLOBAL              exceptions
              114  LOAD_METHOD              LimitOverrunError

 L. 619       116  LOAD_STR                 'Separator is not found, and chunk exceed the limit'

 L. 620       118  LOAD_FAST                'offset'

 L. 618       120  CALL_METHOD_2         2  ''
              122  RAISE_VARARGS_1       1  'exception instance'
            124_0  COME_FROM           110  '110'
            124_1  COME_FROM            64  '64'

 L. 626       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _eof
              128  POP_JUMP_IF_FALSE   162  'to 162'

 L. 627       130  LOAD_GLOBAL              bytes
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                _buffer
              136  CALL_FUNCTION_1       1  ''
              138  STORE_FAST               'chunk'

 L. 628       140  LOAD_FAST                'self'
              142  LOAD_ATTR                _buffer
              144  LOAD_METHOD              clear
              146  CALL_METHOD_0         0  ''
              148  POP_TOP          

 L. 629       150  LOAD_GLOBAL              exceptions
              152  LOAD_METHOD              IncompleteReadError
              154  LOAD_FAST                'chunk'
              156  LOAD_CONST               None
              158  CALL_METHOD_2         2  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           128  '128'

 L. 632       162  LOAD_FAST                'self'
              164  LOAD_METHOD              _wait_for_data
              166  LOAD_STR                 'readuntil'
              168  CALL_METHOD_1         1  ''
              170  GET_AWAITABLE    
              172  LOAD_CONST               None
              174  YIELD_FROM       
              176  POP_TOP          
              178  JUMP_BACK            44  'to 44'
            180_0  COME_FROM            88  '88'

 L. 634       180  LOAD_FAST                'isep'
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                _limit
              186  COMPARE_OP               >
              188  POP_JUMP_IF_FALSE   202  'to 202'

 L. 635       190  LOAD_GLOBAL              exceptions
              192  LOAD_METHOD              LimitOverrunError

 L. 636       194  LOAD_STR                 'Separator is found, but chunk is longer than limit'
              196  LOAD_FAST                'isep'

 L. 635       198  CALL_METHOD_2         2  ''
              200  RAISE_VARARGS_1       1  'exception instance'
            202_0  COME_FROM           188  '188'

 L. 638       202  LOAD_FAST                'self'
              204  LOAD_ATTR                _buffer
              206  LOAD_CONST               None
              208  LOAD_FAST                'isep'
              210  LOAD_FAST                'seplen'
              212  BINARY_ADD       
              214  BUILD_SLICE_2         2 
              216  BINARY_SUBSCR    
              218  STORE_FAST               'chunk'

 L. 639       220  LOAD_FAST                'self'
              222  LOAD_ATTR                _buffer
              224  LOAD_CONST               None
              226  LOAD_FAST                'isep'
              228  LOAD_FAST                'seplen'
              230  BINARY_ADD       
              232  BUILD_SLICE_2         2 
              234  DELETE_SUBSCR    

 L. 640       236  LOAD_FAST                'self'
              238  LOAD_METHOD              _maybe_resume_transport
              240  CALL_METHOD_0         0  ''
              242  POP_TOP          

 L. 641       244  LOAD_GLOBAL              bytes
              246  LOAD_FAST                'chunk'
              248  CALL_FUNCTION_1       1  ''
              250  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 30

    async def read--- This code section failed: ---

 L. 664         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _exception
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 665        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _exception
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             8  '8'

 L. 667        16  LOAD_FAST                'n'
               18  LOAD_CONST               0
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 668        24  LOAD_CONST               b''
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 670        28  LOAD_FAST                'n'
               30  LOAD_CONST               0
               32  COMPARE_OP               <
               34  POP_JUMP_IF_FALSE    86  'to 86'

 L. 675        36  BUILD_LIST_0          0 
               38  STORE_FAST               'blocks'
             40_0  COME_FROM            74  '74'

 L. 677        40  LOAD_FAST                'self'
               42  LOAD_METHOD              read
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _limit
               48  CALL_METHOD_1         1  ''
               50  GET_AWAITABLE    
               52  LOAD_CONST               None
               54  YIELD_FROM       
               56  STORE_FAST               'block'

 L. 678        58  LOAD_FAST                'block'
               60  POP_JUMP_IF_TRUE     64  'to 64'

 L. 679        62  JUMP_FORWARD         76  'to 76'
             64_0  COME_FROM            60  '60'

 L. 680        64  LOAD_FAST                'blocks'
               66  LOAD_METHOD              append
               68  LOAD_FAST                'block'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  JUMP_BACK            40  'to 40'
             76_0  COME_FROM            62  '62'

 L. 681        76  LOAD_CONST               b''
               78  LOAD_METHOD              join
               80  LOAD_FAST                'blocks'
               82  CALL_METHOD_1         1  ''
               84  RETURN_VALUE     
             86_0  COME_FROM            34  '34'

 L. 683        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _buffer
               90  POP_JUMP_IF_TRUE    114  'to 114'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _eof
               96  POP_JUMP_IF_TRUE    114  'to 114'

 L. 684        98  LOAD_FAST                'self'
              100  LOAD_METHOD              _wait_for_data
              102  LOAD_STR                 'read'
              104  CALL_METHOD_1         1  ''
              106  GET_AWAITABLE    
              108  LOAD_CONST               None
              110  YIELD_FROM       
              112  POP_TOP          
            114_0  COME_FROM            96  '96'
            114_1  COME_FROM            90  '90'

 L. 687       114  LOAD_GLOBAL              bytes
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _buffer
              120  LOAD_CONST               None
              122  LOAD_FAST                'n'
              124  BUILD_SLICE_2         2 
              126  BINARY_SUBSCR    
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'data'

 L. 688       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _buffer
              136  LOAD_CONST               None
              138  LOAD_FAST                'n'
              140  BUILD_SLICE_2         2 
              142  DELETE_SUBSCR    

 L. 690       144  LOAD_FAST                'self'
              146  LOAD_METHOD              _maybe_resume_transport
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          

 L. 691       152  LOAD_FAST                'data'
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    async def readexactly--- This code section failed: ---

 L. 708         0  LOAD_FAST                'n'
                2  LOAD_CONST               0
                4  COMPARE_OP               <
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 709         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'readexactly size can not be less than zero'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 711        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _exception
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L. 712        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _exception
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            24  '24'

 L. 714        32  LOAD_FAST                'n'
               34  LOAD_CONST               0
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L. 715        40  LOAD_CONST               b''
               42  RETURN_VALUE     
             44_0  COME_FROM           112  '112'
             44_1  COME_FROM            38  '38'

 L. 717        44  LOAD_GLOBAL              len
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _buffer
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'n'
               54  COMPARE_OP               <
               56  POP_JUMP_IF_FALSE   114  'to 114'

 L. 718        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _eof
               62  POP_JUMP_IF_FALSE    96  'to 96'

 L. 719        64  LOAD_GLOBAL              bytes
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _buffer
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               'incomplete'

 L. 720        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _buffer
               78  LOAD_METHOD              clear
               80  CALL_METHOD_0         0  ''
               82  POP_TOP          

 L. 721        84  LOAD_GLOBAL              exceptions
               86  LOAD_METHOD              IncompleteReadError
               88  LOAD_FAST                'incomplete'
               90  LOAD_FAST                'n'
               92  CALL_METHOD_2         2  ''
               94  RAISE_VARARGS_1       1  'exception instance'
             96_0  COME_FROM            62  '62'

 L. 723        96  LOAD_FAST                'self'
               98  LOAD_METHOD              _wait_for_data
              100  LOAD_STR                 'readexactly'
              102  CALL_METHOD_1         1  ''
              104  GET_AWAITABLE    
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  POP_TOP          
              112  JUMP_BACK            44  'to 44'
            114_0  COME_FROM            56  '56'

 L. 725       114  LOAD_GLOBAL              len
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _buffer
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_FAST                'n'
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   150  'to 150'

 L. 726       128  LOAD_GLOBAL              bytes
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                _buffer
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'data'

 L. 727       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _buffer
              142  LOAD_METHOD              clear
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          
              148  JUMP_FORWARD        180  'to 180'
            150_0  COME_FROM           126  '126'

 L. 729       150  LOAD_GLOBAL              bytes
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _buffer
              156  LOAD_CONST               None
              158  LOAD_FAST                'n'
              160  BUILD_SLICE_2         2 
              162  BINARY_SUBSCR    
              164  CALL_FUNCTION_1       1  ''
              166  STORE_FAST               'data'

 L. 730       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _buffer
              172  LOAD_CONST               None
              174  LOAD_FAST                'n'
              176  BUILD_SLICE_2         2 
              178  DELETE_SUBSCR    
            180_0  COME_FROM           148  '148'

 L. 731       180  LOAD_FAST                'self'
              182  LOAD_METHOD              _maybe_resume_transport
              184  CALL_METHOD_0         0  ''
              186  POP_TOP          

 L. 732       188  LOAD_FAST                'data'
              190  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22

    def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.readline
        if val == b'':
            raise StopAsyncIteration
        return val