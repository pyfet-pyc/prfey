# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: async_timeout\__init__.py
import asyncio, sys
from types import TracebackType
from typing import Optional, Type, Any
__version__ = '3.0.1'
PY_37 = sys.version_info >= (3, 7)

class timeout:
    __doc__ = "timeout context manager.\n\n    Useful in cases when you want to apply timeout logic around block\n    of code or in cases when asyncio.wait_for is not suitable. For example:\n\n    >>> with timeout(0.001):\n    ...     async with aiohttp.get('https://github.com') as r:\n    ...         await r.text()\n\n\n    timeout - value in seconds or None to disable timeout logic\n    loop - asyncio compatible event loop\n    "

    def __init__--- This code section failed: ---

 L.  29         0  LOAD_FAST                'timeout'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _timeout

 L.  30         6  LOAD_FAST                'loop'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L.  31        14  LOAD_GLOBAL              asyncio
               16  LOAD_METHOD              get_event_loop
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'loop'
             22_0  COME_FROM            12  '12'

 L.  32        22  LOAD_FAST                'loop'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _loop

 L.  33        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _task

 L.  34        34  LOAD_CONST               False
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _cancelled

 L.  35        40  LOAD_CONST               None
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _cancel_handler

 L.  36        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _cancel_at

Parse error at or near `<117>' instruction at offset 10

    def __enter__(self) -> 'timeout':
        return self._do_enter

    def __exit__(self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> Optional[bool]:
        self._do_exit(exc_type)

    async def __aenter__(self) -> 'timeout':
        return self._do_enter

    async def __aexit__(self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
        self._do_exit(exc_type)

    @property
    def expired(self) -> bool:
        return self._cancelled

    @property
    def remaining--- This code section failed: ---

 L.  63         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cancel_at
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L.  64        10  LOAD_GLOBAL              max
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _cancel_at
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _loop
               20  LOAD_METHOD              time
               22  CALL_METHOD_0         0  ''
               24  BINARY_SUBTRACT  
               26  LOAD_CONST               0.0
               28  CALL_FUNCTION_2       2  ''
               30  RETURN_VALUE     
             32_0  COME_FROM             8  '8'

 L.  66        32  LOAD_CONST               None
               34  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def _do_enter--- This code section failed: ---

 L.  71         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _timeout
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  72        10  LOAD_FAST                'self'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  74        14  LOAD_GLOBAL              current_task
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _loop
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _task

 L.  75        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _task
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L.  76        36  LOAD_GLOBAL              RuntimeError
               38  LOAD_STR                 'Timeout context manager should be used inside a task'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L.  79        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _timeout
               48  LOAD_CONST               0
               50  COMPARE_OP               <=
               52  POP_JUMP_IF_FALSE    72  'to 72'

 L.  80        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _loop
               58  LOAD_METHOD              call_soon
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _cancel_task
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L.  81        68  LOAD_FAST                'self'
               70  RETURN_VALUE     
             72_0  COME_FROM            52  '52'

 L.  83        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _loop
               76  LOAD_METHOD              time
               78  CALL_METHOD_0         0  ''
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _timeout
               84  BINARY_ADD       
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _cancel_at

 L.  84        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _loop
               94  LOAD_METHOD              call_at

 L.  85        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _cancel_at
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                _cancel_task

 L.  84       104  CALL_METHOD_2         2  ''
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _cancel_handler

 L.  86       110  LOAD_FAST                'self'
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _do_exit--- This code section failed: ---

 L.  89         0  LOAD_FAST                'exc_type'
                2  LOAD_GLOBAL              asyncio
                4  LOAD_ATTR                CancelledError
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    34  'to 34'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _cancelled
               14  POP_JUMP_IF_FALSE    34  'to 34'

 L.  90        16  LOAD_CONST               None
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _cancel_handler

 L.  91        22  LOAD_CONST               None
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _task

 L.  92        28  LOAD_GLOBAL              asyncio
               30  LOAD_ATTR                TimeoutError
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            14  '14'
             34_1  COME_FROM             8  '8'

 L.  93        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _timeout
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    70  'to 70'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _cancel_handler
               48  LOAD_CONST               None
               50  <117>                 1  ''
               52  POP_JUMP_IF_FALSE    70  'to 70'

 L.  94        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _cancel_handler
               58  LOAD_METHOD              cancel
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          

 L.  95        64  LOAD_CONST               None
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _cancel_handler
             70_0  COME_FROM            52  '52'
             70_1  COME_FROM            42  '42'

 L.  96        70  LOAD_CONST               None
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _task

Parse error at or near `None' instruction at offset -1

    def _cancel_task--- This code section failed: ---

 L. 100         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _task
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 101        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _task
               14  LOAD_METHOD              cancel
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 102        20  LOAD_CONST               True
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _cancelled
             26_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1


def current_task--- This code section failed: ---

 L. 106         0  LOAD_GLOBAL              PY_37
                2  POP_JUMP_IF_FALSE    18  'to 18'

 L. 107         4  LOAD_GLOBAL              asyncio
                6  LOAD_ATTR                current_task
                8  LOAD_FAST                'loop'
               10  LOAD_CONST               ('loop',)
               12  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               14  STORE_FAST               'task'
               16  JUMP_FORWARD         32  'to 32'
             18_0  COME_FROM             2  '2'

 L. 109        18  LOAD_GLOBAL              asyncio
               20  LOAD_ATTR                Task
               22  LOAD_ATTR                current_task
               24  LOAD_FAST                'loop'
               26  LOAD_CONST               ('loop',)
               28  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               30  STORE_FAST               'task'
             32_0  COME_FROM            16  '16'

 L. 110        32  LOAD_FAST                'task'
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    58  'to 58'

 L. 112        40  LOAD_GLOBAL              hasattr
               42  LOAD_FAST                'loop'
               44  LOAD_STR                 'current_task'
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L. 113        50  LOAD_FAST                'loop'
               52  LOAD_METHOD              current_task
               54  CALL_METHOD_0         0  ''
               56  STORE_FAST               'task'
             58_0  COME_FROM            48  '48'
             58_1  COME_FROM            38  '38'

 L. 115        58  LOAD_FAST                'task'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 36