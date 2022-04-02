# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\threads.py
"""High-level support for working with threads in asyncio"""
import functools, contextvars
from . import events
__all__ = ('to_thread', )

async def to_thread--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL              events
                2  LOAD_METHOD              get_running_loop
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'loop'

 L.  23         8  LOAD_GLOBAL              contextvars
               10  LOAD_METHOD              copy_context
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'ctx'

 L.  24        16  LOAD_GLOBAL              functools
               18  LOAD_ATTR                partial
               20  LOAD_FAST                'ctx'
               22  LOAD_ATTR                run
               24  LOAD_FAST                'func'
               26  BUILD_LIST_2          2 
               28  LOAD_FAST                'args'
               30  CALL_FINALLY         33  'to 33'
               32  WITH_CLEANUP_FINISH
               34  BUILD_MAP_0           0 
               36  LOAD_FAST                'kwargs'
               38  <164>                 1  ''
               40  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               42  STORE_FAST               'func_call'

 L.  25        44  LOAD_FAST                'loop'
               46  LOAD_METHOD              run_in_executor
               48  LOAD_CONST               None
               50  LOAD_FAST                'func_call'
               52  CALL_METHOD_2         2  ''
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 30