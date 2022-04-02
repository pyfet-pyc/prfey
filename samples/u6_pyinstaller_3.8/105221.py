# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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

    def addAsyncCleanup(self, func, *args, **kwargs):
        (self.addCleanup)(*(func, *args), **kwargs)

    def _callSetUp(self):
        self.setUp()
        self._callAsync(self.asyncSetUp)

    def _callTestMethod(self, method):
        self._callMaybeAsync(method)

    def _callTearDown(self):
        self._callAsync(self.asyncTearDown)
        self.tearDown()

    def _callCleanup(self, function, *args, **kwargs):
        (self._callMaybeAsync)(function, *args, **kwargs)

    def _callAsync(self, func, *args, **kwargs):
        assert self._asyncioTestLoop is not None
        ret = func(*args, **kwargs)
        assert inspect.isawaitable(ret)
        fut = self._asyncioTestLoop.create_future()
        self._asyncioCallsQueue.put_nowait((fut, ret))
        return self._asyncioTestLoop.run_until_complete(fut)

    def _callMaybeAsync(self, func, *args, **kwargs):
        assert self._asyncioTestLoop is not None
        ret = func(*args, **kwargs)
        if inspect.isawaitable(ret):
            fut = self._asyncioTestLoop.create_future()
            self._asyncioCallsQueue.put_nowait((fut, ret))
            return self._asyncioTestLoop.run_until_complete(fut)
        return ret

    async def _asyncioLoopRunner(self, fut):
        self._asyncioCallsQueue = queue = asyncio.Queue()
        fut.set_result(None)
        while True:
            query = await queue.get()
            queue.task_done()
            if query is None:
                return
            fut, awaitable = query
            try:
                ret = await awaitable
                if not fut.cancelled():
                    fut.set_result(ret)
            except asyncio.CancelledError:
                raise
            except Exception as ex:
                try:
                    if not fut.cancelled():
                        fut.set_exception(ex)
                finally:
                    ex = None
                    del ex

    def _setupAsyncioLoop(self):
        assert self._asyncioTestLoop is None
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_debug(True)
        self._asyncioTestLoop = loop
        fut = loop.create_future()
        self._asyncioCallsTask = loop.create_task(self._asyncioLoopRunner(fut))
        loop.run_until_complete(fut)

    def _tearDownAsyncioLoop--- This code section failed: ---

 L. 122         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _asyncioTestLoop
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  LOAD_ASSERT              AssertionError
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

 L. 128        54  SETUP_FINALLY       192  'to 192'

 L. 130        56  LOAD_GLOBAL              asyncio
               58  LOAD_METHOD              all_tasks
               60  LOAD_FAST                'loop'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'to_cancel'

 L. 131        66  LOAD_FAST                'to_cancel'
               68  POP_JUMP_IF_TRUE     78  'to 78'

 L. 132        70  POP_BLOCK        
               72  CALL_FINALLY        192  'to 192'
               74  LOAD_CONST               None
               76  RETURN_VALUE     
             78_0  COME_FROM            68  '68'

 L. 134        78  LOAD_FAST                'to_cancel'
               80  GET_ITER         
               82  FOR_ITER             96  'to 96'
               84  STORE_FAST               'task'

 L. 135        86  LOAD_FAST                'task'
               88  LOAD_METHOD              cancel
               90  CALL_METHOD_0         0  ''
               92  POP_TOP          
               94  JUMP_BACK            82  'to 82'

 L. 137        96  LOAD_FAST                'loop'
               98  LOAD_METHOD              run_until_complete

 L. 138       100  LOAD_GLOBAL              asyncio
              102  LOAD_ATTR                gather
              104  LOAD_FAST                'to_cancel'
              106  LOAD_FAST                'loop'
              108  LOAD_CONST               True
              110  LOAD_CONST               ('loop', 'return_exceptions')
              112  BUILD_CONST_KEY_MAP_2     2 
              114  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 137       116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 140       120  LOAD_FAST                'to_cancel'
              122  GET_ITER         
            124_0  COME_FROM           148  '148'
              124  FOR_ITER            174  'to 174'
              126  STORE_FAST               'task'

 L. 141       128  LOAD_FAST                'task'
              130  LOAD_METHOD              cancelled
              132  CALL_METHOD_0         0  ''
              134  POP_JUMP_IF_FALSE   138  'to 138'

 L. 142       136  JUMP_BACK           124  'to 124'
            138_0  COME_FROM           134  '134'

 L. 143       138  LOAD_FAST                'task'
              140  LOAD_METHOD              exception
              142  CALL_METHOD_0         0  ''
              144  LOAD_CONST               None
              146  COMPARE_OP               is-not
              148  POP_JUMP_IF_FALSE   124  'to 124'

 L. 144       150  LOAD_FAST                'loop'
              152  LOAD_METHOD              call_exception_handler

 L. 145       154  LOAD_STR                 'unhandled exception during test shutdown'

 L. 146       156  LOAD_FAST                'task'
              158  LOAD_METHOD              exception
              160  CALL_METHOD_0         0  ''

 L. 147       162  LOAD_FAST                'task'

 L. 144       164  LOAD_CONST               ('message', 'exception', 'task')
              166  BUILD_CONST_KEY_MAP_3     3 
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  JUMP_BACK           124  'to 124'

 L. 150       174  LOAD_FAST                'loop'
              176  LOAD_METHOD              run_until_complete
              178  LOAD_FAST                'loop'
              180  LOAD_METHOD              shutdown_asyncgens
              182  CALL_METHOD_0         0  ''
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
              188  POP_BLOCK        
              190  BEGIN_FINALLY    
            192_0  COME_FROM            72  '72'
            192_1  COME_FROM_FINALLY    54  '54'

 L. 152       192  LOAD_GLOBAL              asyncio
              194  LOAD_METHOD              set_event_loop
              196  LOAD_CONST               None
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L. 153       202  LOAD_FAST                'loop'
              204  LOAD_METHOD              close
              206  CALL_METHOD_0         0  ''
              208  POP_TOP          
              210  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 72

    def run(self, result=None):
        self._setupAsyncioLoop()
        try:
            return super().run(result)
        finally:
            self._tearDownAsyncioLoop()