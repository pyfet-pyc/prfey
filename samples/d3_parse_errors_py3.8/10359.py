# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\runners.py
__all__ = ('run', )
from . import coroutines
from . import events
from . import tasks

def run--- This code section failed: ---

 L.  32         0  LOAD_GLOBAL              events
                2  LOAD_METHOD              _get_running_loop
                4  CALL_METHOD_0         0  ''
                6  LOAD_CONST               None
                8  COMPARE_OP               is-not
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  33        12  LOAD_GLOBAL              RuntimeError

 L.  34        14  LOAD_STR                 'asyncio.run() cannot be called from a running event loop'

 L.  33        16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L.  36        20  LOAD_GLOBAL              coroutines
               22  LOAD_METHOD              iscoroutine
               24  LOAD_FAST                'main'
               26  CALL_METHOD_1         1  ''
               28  POP_JUMP_IF_TRUE     44  'to 44'

 L.  37        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'a coroutine was expected, got {!r}'
               34  LOAD_METHOD              format
               36  LOAD_FAST                'main'
               38  CALL_METHOD_1         1  ''
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            28  '28'

 L.  39        44  LOAD_GLOBAL              events
               46  LOAD_METHOD              new_event_loop
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'loop'

 L.  40        52  SETUP_FINALLY        88  'to 88'

 L.  41        54  LOAD_GLOBAL              events
               56  LOAD_METHOD              set_event_loop
               58  LOAD_FAST                'loop'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L.  42        64  LOAD_FAST                'loop'
               66  LOAD_METHOD              set_debug
               68  LOAD_FAST                'debug'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          

 L.  43        74  LOAD_FAST                'loop'
               76  LOAD_METHOD              run_until_complete
               78  LOAD_FAST                'main'
               80  CALL_METHOD_1         1  ''
               82  POP_BLOCK        
               84  CALL_FINALLY         88  'to 88'
               86  RETURN_VALUE     
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM_FINALLY    52  '52'

 L.  45        88  SETUP_FINALLY       116  'to 116'

 L.  46        90  LOAD_GLOBAL              _cancel_all_tasks
               92  LOAD_FAST                'loop'
               94  CALL_FUNCTION_1       1  ''
               96  POP_TOP          

 L.  47        98  LOAD_FAST                'loop'
              100  LOAD_METHOD              run_until_complete
              102  LOAD_FAST                'loop'
              104  LOAD_METHOD              shutdown_asyncgens
              106  CALL_METHOD_0         0  ''
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM_FINALLY    88  '88'

 L.  49       116  LOAD_GLOBAL              events
              118  LOAD_METHOD              set_event_loop
              120  LOAD_CONST               None
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L.  50       126  LOAD_FAST                'loop'
              128  LOAD_METHOD              close
              130  CALL_METHOD_0         0  ''
              132  POP_TOP          
              134  END_FINALLY      
              136  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 84


def _cancel_all_tasks(loop):
    to_cancel = tasks.all_tasksloop
    if not to_cancel:
        return
    for task in to_cancel:
        task.cancel
    else:
        loop.run_until_complete(tasks.gather)(*to_cancel, loop=loop, return_exceptions=True)
        for task in to_cancel:
            if task.cancelled:
                pass
            else:
                if task.exception is not None:
                    loop.call_exception_handler{'message':'unhandled exception during asyncio.run() shutdown', 
                     'exception':task.exception, 
                     'task':task}