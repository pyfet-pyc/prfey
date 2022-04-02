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

 L.  40        52  SETUP_FINALLY        96  'to 96'

 L.  41        54  LOAD_GLOBAL              events
               56  LOAD_METHOD              set_event_loop
               58  LOAD_FAST                'loop'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L.  42        64  LOAD_FAST                'debug'
               66  LOAD_CONST               None
               68  COMPARE_OP               is-not
               70  POP_JUMP_IF_FALSE    82  'to 82'

 L.  43        72  LOAD_FAST                'loop'
               74  LOAD_METHOD              set_debug
               76  LOAD_FAST                'debug'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            70  '70'

 L.  44        82  LOAD_FAST                'loop'
               84  LOAD_METHOD              run_until_complete
               86  LOAD_FAST                'main'
               88  CALL_METHOD_1         1  ''
               90  POP_BLOCK        
               92  CALL_FINALLY         96  'to 96'
               94  RETURN_VALUE     
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM_FINALLY    52  '52'

 L.  46        96  SETUP_FINALLY       124  'to 124'

 L.  47        98  LOAD_GLOBAL              _cancel_all_tasks
              100  LOAD_FAST                'loop'
              102  CALL_FUNCTION_1       1  ''
              104  POP_TOP          

 L.  48       106  LOAD_FAST                'loop'
              108  LOAD_METHOD              run_until_complete
              110  LOAD_FAST                'loop'
              112  LOAD_METHOD              shutdown_asyncgens
              114  CALL_METHOD_0         0  ''
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          
              120  POP_BLOCK        
              122  BEGIN_FINALLY    
            124_0  COME_FROM_FINALLY    96  '96'

 L.  50       124  LOAD_GLOBAL              events
              126  LOAD_METHOD              set_event_loop
              128  LOAD_CONST               None
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          

 L.  51       134  LOAD_FAST                'loop'
              136  LOAD_METHOD              close
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          
              142  END_FINALLY      
              144  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 92


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