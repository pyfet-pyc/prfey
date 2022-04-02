# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\base_protocol.py
import asyncio
from typing import Optional, cast
from .tcp_helpers import tcp_nodelay

class BaseProtocol(asyncio.Protocol):
    __slots__ = ('_loop', '_paused', '_drain_waiter', '_connection_lost', '_reading_paused',
                 'transport')

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop
        self._paused = False
        self._drain_waiter = None
        self._connection_lost = False
        self._reading_paused = False
        self.transport = None

    def pause_writing--- This code section failed: ---

 L.  27         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _paused
                4  POP_JUMP_IF_FALSE    10  'to 10'
                6  <74>             
                8  RAISE_VARARGS_1       1  'exception instance'
             10_0  COME_FROM             4  '4'

 L.  28        10  LOAD_CONST               True
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _paused

Parse error at or near `None' instruction at offset -1

    def resume_writing--- This code section failed: ---

 L.  31         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _paused
                4  POP_JUMP_IF_TRUE     10  'to 10'
                6  <74>             
                8  RAISE_VARARGS_1       1  'exception instance'
             10_0  COME_FROM             4  '4'

 L.  32        10  LOAD_CONST               False
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _paused

 L.  34        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _drain_waiter
               20  STORE_FAST               'waiter'

 L.  35        22  LOAD_FAST                'waiter'
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    54  'to 54'

 L.  36        30  LOAD_CONST               None
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _drain_waiter

 L.  37        36  LOAD_FAST                'waiter'
               38  LOAD_METHOD              done
               40  CALL_METHOD_0         0  ''
               42  POP_JUMP_IF_TRUE     54  'to 54'

 L.  38        44  LOAD_FAST                'waiter'
               46  LOAD_METHOD              set_result
               48  LOAD_CONST               None
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
             54_0  COME_FROM            42  '42'
             54_1  COME_FROM            28  '28'

Parse error at or near `None' instruction at offset -1

    def pause_reading--- This code section failed: ---

 L.  41         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _reading_paused
                4  POP_JUMP_IF_TRUE     62  'to 62'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                transport
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    62  'to 62'

 L.  42        16  SETUP_FINALLY        32  'to 32'

 L.  43        18  LOAD_FAST                'self'
               20  LOAD_ATTR                transport
               22  LOAD_METHOD              pause_reading
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          
               28  POP_BLOCK        
               30  JUMP_FORWARD         56  'to 56'
             32_0  COME_FROM_FINALLY    16  '16'

 L.  44        32  DUP_TOP          
               34  LOAD_GLOBAL              AttributeError
               36  LOAD_GLOBAL              NotImplementedError
               38  LOAD_GLOBAL              RuntimeError
               40  BUILD_TUPLE_3         3 
               42  <121>                54  ''
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L.  45        50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
               54  <48>             
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            30  '30'

 L.  46        56  LOAD_CONST               True
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _reading_paused
             62_0  COME_FROM            14  '14'
             62_1  COME_FROM             4  '4'

Parse error at or near `None' instruction at offset -1

    def resume_reading--- This code section failed: ---

 L.  49         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _reading_paused
                4  POP_JUMP_IF_FALSE    62  'to 62'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                transport
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    62  'to 62'

 L.  50        16  SETUP_FINALLY        32  'to 32'

 L.  51        18  LOAD_FAST                'self'
               20  LOAD_ATTR                transport
               22  LOAD_METHOD              resume_reading
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          
               28  POP_BLOCK        
               30  JUMP_FORWARD         56  'to 56'
             32_0  COME_FROM_FINALLY    16  '16'

 L.  52        32  DUP_TOP          
               34  LOAD_GLOBAL              AttributeError
               36  LOAD_GLOBAL              NotImplementedError
               38  LOAD_GLOBAL              RuntimeError
               40  BUILD_TUPLE_3         3 
               42  <121>                54  ''
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L.  53        50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
               54  <48>             
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            30  '30'

 L.  54        56  LOAD_CONST               False
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _reading_paused
             62_0  COME_FROM            14  '14'
             62_1  COME_FROM             4  '4'

Parse error at or near `None' instruction at offset -1

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        tr = cast(asyncio.Transport, transport)
        tcp_nodelay(tr, True)
        self.transport = tr

    def connection_lost--- This code section failed: ---

 L.  62         0  LOAD_CONST               True
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _connection_lost

 L.  64         6  LOAD_CONST               None
                8  LOAD_FAST                'self'
               10  STORE_ATTR               transport

 L.  65        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _paused
               16  POP_JUMP_IF_TRUE     22  'to 22'

 L.  66        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  67        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _drain_waiter
               26  STORE_FAST               'waiter'

 L.  68        28  LOAD_FAST                'waiter'
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L.  69        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L.  70        40  LOAD_CONST               None
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _drain_waiter

 L.  71        46  LOAD_FAST                'waiter'
               48  LOAD_METHOD              done
               50  CALL_METHOD_0         0  ''
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L.  72        54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L.  73        58  LOAD_FAST                'exc'
               60  LOAD_CONST               None
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE    78  'to 78'

 L.  74        66  LOAD_FAST                'waiter'
               68  LOAD_METHOD              set_result
               70  LOAD_CONST               None
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
               76  JUMP_FORWARD         88  'to 88'
             78_0  COME_FROM            64  '64'

 L.  76        78  LOAD_FAST                'waiter'
               80  LOAD_METHOD              set_exception
               82  LOAD_FAST                'exc'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
             88_0  COME_FROM            76  '76'

Parse error at or near `<117>' instruction at offset 32

    async def _drain_helper--- This code section failed: ---

 L.  79         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _connection_lost
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L.  80         6  LOAD_GLOBAL              ConnectionResetError
                8  LOAD_STR                 'Connection lost'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L.  81        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _paused
               18  POP_JUMP_IF_TRUE     24  'to 24'

 L.  82        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.  83        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _drain_waiter
               28  STORE_FAST               'waiter'

 L.  84        30  LOAD_FAST                'waiter'
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

 L.  85        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _loop
               54  LOAD_METHOD              create_future
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'waiter'

 L.  86        60  LOAD_FAST                'waiter'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _drain_waiter

 L.  87        66  LOAD_FAST                'waiter'
               68  GET_AWAITABLE    
               70  LOAD_CONST               None
               72  YIELD_FROM       
               74  POP_TOP          

Parse error at or near `<117>' instruction at offset 34