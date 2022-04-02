# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: unittest\async_case.py
import asyncio, inspect
from .case import TestCase

class IsolatedAsyncioTestCase(TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self._asyncioTestLoop = None
        self._asyncioCallsQueue = None

    async def asyncSetUp(self):
        pass

    async def asyncTearDown(self):
        pass

    def addAsyncCleanup--- This code section failed: ---

 L.  58         0  LOAD_FAST                'self'
                2  LOAD_ATTR                addCleanup
                4  LOAD_FAST                'func'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _callSetUp(self):
        self.setUp()
        self._callAsync(self.asyncSetUp)

    def _callTestMethod(self, method):
        self._callMaybeAsync(method)

    def _callTearDown(self):
        self._callAsync(self.asyncTearDown)
        self.tearDown()

    def _callCleanup--- This code section failed: ---

 L.  72         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _callMaybeAsync
                4  LOAD_FAST                'function'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _callAsync--- This code section failed: ---

 L.  75         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _asyncioTestLoop
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L.  76        14  LOAD_FAST                'func'
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  STORE_FAST               'ret'

 L.  77        28  LOAD_GLOBAL              inspect
               30  LOAD_METHOD              isawaitable
               32  LOAD_FAST                'ret'
               34  CALL_METHOD_1         1  ''
               36  POP_JUMP_IF_TRUE     42  'to 42'
               38  <74>             
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            36  '36'

 L.  78        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _asyncioTestLoop
               46  LOAD_METHOD              create_future
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'fut'

 L.  79        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _asyncioCallsQueue
               56  LOAD_METHOD              put_nowait
               58  LOAD_FAST                'fut'
               60  LOAD_FAST                'ret'
               62  BUILD_TUPLE_2         2 
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L.  80        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _asyncioTestLoop
               72  LOAD_METHOD              run_until_complete
               74  LOAD_FAST                'fut'
               76  CALL_METHOD_1         1  ''
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _callMaybeAsync--- This code section failed: ---

 L.  83         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _asyncioTestLoop
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L.  84        14  LOAD_FAST                'func'
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  STORE_FAST               'ret'

 L.  85        28  LOAD_GLOBAL              inspect
               30  LOAD_METHOD              isawaitable
               32  LOAD_FAST                'ret'
               34  CALL_METHOD_1         1  ''
               36  POP_JUMP_IF_FALSE    76  'to 76'

 L.  86        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _asyncioTestLoop
               42  LOAD_METHOD              create_future
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'fut'

 L.  87        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _asyncioCallsQueue
               52  LOAD_METHOD              put_nowait
               54  LOAD_FAST                'fut'
               56  LOAD_FAST                'ret'
               58  BUILD_TUPLE_2         2 
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L.  88        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _asyncioTestLoop
               68  LOAD_METHOD              run_until_complete
               70  LOAD_FAST                'fut'
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            36  '36'

 L.  90        76  LOAD_FAST                'ret'
               78  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    async def _asyncioLoopRunner--- This code section failed: ---

 L.  93         0  LOAD_GLOBAL              asyncio
                2  LOAD_METHOD              Queue
                4  CALL_METHOD_0         0  ''
                6  DUP_TOP          
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _asyncioCallsQueue
               12  STORE_FAST               'queue'

 L.  94        14  LOAD_FAST                'fut'
               16  LOAD_METHOD              set_result
               18  LOAD_CONST               None
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L.  96        24  LOAD_FAST                'queue'
               26  LOAD_METHOD              get
               28  CALL_METHOD_0         0  ''
               30  GET_AWAITABLE    
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  STORE_FAST               'query'

 L.  97        38  LOAD_FAST                'queue'
               40  LOAD_METHOD              task_done
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L.  98        46  LOAD_FAST                'query'
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L.  99        54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 100        58  LOAD_FAST                'query'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'fut'
               64  STORE_FAST               'awaitable'

 L. 101        66  SETUP_FINALLY       100  'to 100'

 L. 102        68  LOAD_FAST                'awaitable'
               70  GET_AWAITABLE    
               72  LOAD_CONST               None
               74  YIELD_FROM       
               76  STORE_FAST               'ret'

 L. 103        78  LOAD_FAST                'fut'
               80  LOAD_METHOD              cancelled
               82  CALL_METHOD_0         0  ''
               84  POP_JUMP_IF_TRUE     96  'to 96'

 L. 104        86  LOAD_FAST                'fut'
               88  LOAD_METHOD              set_result
               90  LOAD_FAST                'ret'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
             96_0  COME_FROM            84  '84'
               96  POP_BLOCK        
               98  JUMP_BACK            24  'to 24'
            100_0  COME_FROM_FINALLY    66  '66'

 L. 105       100  DUP_TOP          
              102  LOAD_GLOBAL              asyncio
              104  LOAD_ATTR                CancelledError
              106  <121>               120  ''
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 106       114  RAISE_VARARGS_0       0  'reraise'
              116  POP_EXCEPT       
              118  JUMP_BACK            24  'to 24'

 L. 107       120  DUP_TOP          
              122  LOAD_GLOBAL              Exception
              124  <121>               172  ''
              126  POP_TOP          
              128  STORE_FAST               'ex'
              130  POP_TOP          
              132  SETUP_FINALLY       164  'to 164'

 L. 108       134  LOAD_FAST                'fut'
              136  LOAD_METHOD              cancelled
              138  CALL_METHOD_0         0  ''
              140  POP_JUMP_IF_TRUE    152  'to 152'

 L. 109       142  LOAD_FAST                'fut'
              144  LOAD_METHOD              set_exception
              146  LOAD_FAST                'ex'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          
            152_0  COME_FROM           140  '140'
              152  POP_BLOCK        
              154  POP_EXCEPT       
              156  LOAD_CONST               None
              158  STORE_FAST               'ex'
              160  DELETE_FAST              'ex'
              162  JUMP_BACK            24  'to 24'
            164_0  COME_FROM_FINALLY   132  '132'
              164  LOAD_CONST               None
              166  STORE_FAST               'ex'
              168  DELETE_FAST              'ex'
              170  <48>             
              172  <48>             
              174  JUMP_BACK            24  'to 24'

Parse error at or near `<117>' instruction at offset 50

    def _setupAsyncioLoop--- This code section failed: ---

 L. 112         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _asyncioTestLoop
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 113        14  LOAD_GLOBAL              asyncio
               16  LOAD_METHOD              new_event_loop
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'loop'

 L. 114        22  LOAD_GLOBAL              asyncio
               24  LOAD_METHOD              set_event_loop
               26  LOAD_FAST                'loop'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 115        32  LOAD_FAST                'loop'
               34  LOAD_METHOD              set_debug
               36  LOAD_CONST               True
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 116        42  LOAD_FAST                'loop'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _asyncioTestLoop

 L. 117        48  LOAD_FAST                'loop'
               50  LOAD_METHOD              create_future
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'fut'

 L. 118        56  LOAD_FAST                'loop'
               58  LOAD_METHOD              create_task
               60  LOAD_FAST                'self'
               62  LOAD_METHOD              _asyncioLoopRunner
               64  LOAD_FAST                'fut'
               66  CALL_METHOD_1         1  ''
               68  CALL_METHOD_1         1  ''
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _asyncioCallsTask

 L. 119        74  LOAD_FAST                'loop'
               76  LOAD_METHOD              run_until_complete
               78  LOAD_FAST                'fut'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _tearDownAsyncioLoop--- This code section failed: ---

 L. 122         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _asyncioTestLoop
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 123        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _asyncioTestLoop
               18  STORE_FAST               'loop'

 L. 124        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _asyncioTestLoop

 L. 125        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _asyncioCallsQueue
               30  LOAD_METHOD              put_nowait
               32  LOAD_CONST               None
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L. 126        38  LOAD_FAST                'loop'
               40  LOAD_METHOD              run_until_complete
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _asyncioCallsQueue
               46  LOAD_METHOD              join
               48  CALL_METHOD_0         0  ''
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 128        54  SETUP_FINALLY       226  'to 226'

 L. 130        56  LOAD_GLOBAL              asyncio
               58  LOAD_METHOD              all_tasks
               60  LOAD_FAST                'loop'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'to_cancel'

 L. 131        66  LOAD_FAST                'to_cancel'
               68  POP_JUMP_IF_TRUE     94  'to 94'

 L. 132        70  POP_BLOCK        

 L. 152        72  LOAD_GLOBAL              asyncio
               74  LOAD_METHOD              set_event_loop
               76  LOAD_CONST               None
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 153        82  LOAD_FAST                'loop'
               84  LOAD_METHOD              close
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          

 L. 132        90  LOAD_CONST               None
               92  RETURN_VALUE     
             94_0  COME_FROM            68  '68'

 L. 134        94  LOAD_FAST                'to_cancel'
               96  GET_ITER         
               98  FOR_ITER            112  'to 112'
              100  STORE_FAST               'task'

 L. 135       102  LOAD_FAST                'task'
              104  LOAD_METHOD              cancel
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          
              110  JUMP_BACK            98  'to 98'

 L. 137       112  LOAD_FAST                'loop'
              114  LOAD_METHOD              run_until_complete

 L. 138       116  LOAD_GLOBAL              asyncio
              118  LOAD_ATTR                gather
              120  LOAD_FAST                'to_cancel'
              122  LOAD_FAST                'loop'
              124  LOAD_CONST               True
              126  LOAD_CONST               ('loop', 'return_exceptions')
              128  BUILD_CONST_KEY_MAP_2     2 
              130  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 137       132  CALL_METHOD_1         1  ''
              134  POP_TOP          

 L. 140       136  LOAD_FAST                'to_cancel'
              138  GET_ITER         
            140_0  COME_FROM           164  '164'
              140  FOR_ITER            190  'to 190'
              142  STORE_FAST               'task'

 L. 141       144  LOAD_FAST                'task'
              146  LOAD_METHOD              cancelled
              148  CALL_METHOD_0         0  ''
              150  POP_JUMP_IF_FALSE   154  'to 154'

 L. 142       152  JUMP_BACK           140  'to 140'
            154_0  COME_FROM           150  '150'

 L. 143       154  LOAD_FAST                'task'
              156  LOAD_METHOD              exception
              158  CALL_METHOD_0         0  ''
              160  LOAD_CONST               None
              162  <117>                 1  ''
              164  POP_JUMP_IF_FALSE   140  'to 140'

 L. 144       166  LOAD_FAST                'loop'
              168  LOAD_METHOD              call_exception_handler

 L. 145       170  LOAD_STR                 'unhandled exception during test shutdown'

 L. 146       172  LOAD_FAST                'task'
              174  LOAD_METHOD              exception
              176  CALL_METHOD_0         0  ''

 L. 147       178  LOAD_FAST                'task'

 L. 144       180  LOAD_CONST               ('message', 'exception', 'task')
              182  BUILD_CONST_KEY_MAP_3     3 
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
              188  JUMP_BACK           140  'to 140'

 L. 150       190  LOAD_FAST                'loop'
              192  LOAD_METHOD              run_until_complete
              194  LOAD_FAST                'loop'
              196  LOAD_METHOD              shutdown_asyncgens
              198  CALL_METHOD_0         0  ''
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          
              204  POP_BLOCK        

 L. 152       206  LOAD_GLOBAL              asyncio
              208  LOAD_METHOD              set_event_loop
              210  LOAD_CONST               None
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 153       216  LOAD_FAST                'loop'
              218  LOAD_METHOD              close
              220  CALL_METHOD_0         0  ''
              222  POP_TOP          
              224  JUMP_FORWARD        246  'to 246'
            226_0  COME_FROM_FINALLY    54  '54'

 L. 152       226  LOAD_GLOBAL              asyncio
              228  LOAD_METHOD              set_event_loop
              230  LOAD_CONST               None
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          

 L. 153       236  LOAD_FAST                'loop'
              238  LOAD_METHOD              close
              240  CALL_METHOD_0         0  ''
              242  POP_TOP          
              244  <48>             
            246_0  COME_FROM           224  '224'

Parse error at or near `None' instruction at offset -1

    def run--- This code section failed: ---

 L. 156         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _setupAsyncioLoop
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 157         8  SETUP_FINALLY        32  'to 32'

 L. 158        10  LOAD_GLOBAL              super
               12  CALL_FUNCTION_0       0  ''
               14  LOAD_METHOD              run
               16  LOAD_FAST                'result'
               18  CALL_METHOD_1         1  ''
               20  POP_BLOCK        

 L. 160        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _tearDownAsyncioLoop
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          

 L. 158        30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     8  '8'

 L. 160        32  LOAD_FAST                'self'
               34  LOAD_METHOD              _tearDownAsyncioLoop
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          
               40  <48>             

Parse error at or near `LOAD_FAST' instruction at offset 22