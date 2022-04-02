# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\staggered.py
"""Support for running coroutines in parallel with staggered start times."""
__all__ = ('staggered_race', )
import contextlib, typing
from . import events
from . import futures
from . import locks
from . import tasks

async def staggered_race--- This code section failed: ---

 L.  75         0  LOAD_DEREF               'loop'
                2  JUMP_IF_TRUE_OR_POP    10  'to 10'
                4  LOAD_GLOBAL              events
                6  LOAD_METHOD              get_running_loop
                8  CALL_METHOD_0         0  ''
             10_0  COME_FROM             2  '2'
               10  STORE_DEREF              'loop'

 L.  76        12  LOAD_GLOBAL              enumerate
               14  LOAD_FAST                'coro_fns'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_DEREF              'enum_coro_fns'

 L.  77        20  LOAD_CONST               None
               22  STORE_DEREF              'winner_result'

 L.  78        24  LOAD_CONST               None
               26  STORE_DEREF              'winner_index'

 L.  79        28  BUILD_LIST_0          0 
               30  STORE_DEREF              'exceptions'

 L.  80        32  BUILD_LIST_0          0 
               34  STORE_DEREF              'running_tasks'

 L.  83        36  LOAD_GLOBAL              typing
               38  LOAD_ATTR                Optional
               40  LOAD_GLOBAL              locks
               42  LOAD_ATTR                Event
               44  BINARY_SUBSCR    

 L.  83        46  LOAD_CONST               None

 L.  82        48  LOAD_CONST               ('previous_failed', 'return')
               50  BUILD_CONST_KEY_MAP_2     2 
               52  LOAD_CLOSURE             'delay'
               54  LOAD_CLOSURE             'enum_coro_fns'
               56  LOAD_CLOSURE             'exceptions'
               58  LOAD_CLOSURE             'loop'
               60  LOAD_CLOSURE             'run_one_coro'
               62  LOAD_CLOSURE             'running_tasks'
               64  LOAD_CLOSURE             'winner_index'
               66  LOAD_CLOSURE             'winner_result'
               68  BUILD_TUPLE_8         8 
               70  LOAD_CODE                <code_object run_one_coro>
               72  LOAD_STR                 'staggered_race.<locals>.run_one_coro'
               74  MAKE_FUNCTION_12         'annotation, closure'
               76  STORE_DEREF              'run_one_coro'

 L. 130        78  LOAD_DEREF               'loop'
               80  LOAD_METHOD              create_task
               82  LOAD_DEREF               'run_one_coro'
               84  LOAD_CONST               None
               86  CALL_FUNCTION_1       1  ''
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'first_task'

 L. 131        92  LOAD_DEREF               'running_tasks'
               94  LOAD_METHOD              append
               96  LOAD_FAST                'first_task'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 132       102  SETUP_FINALLY       206  'to 206'

 L. 135       104  LOAD_CONST               0
              106  STORE_FAST               'done_count'

 L. 136       108  LOAD_FAST                'done_count'
              110  LOAD_GLOBAL              len
              112  LOAD_DEREF               'running_tasks'
              114  CALL_FUNCTION_1       1  ''
              116  COMPARE_OP               !=
              118  POP_JUMP_IF_FALSE   192  'to 192'

 L. 137       120  LOAD_GLOBAL              tasks
              122  LOAD_METHOD              wait
              124  LOAD_DEREF               'running_tasks'
              126  CALL_METHOD_1         1  ''
              128  GET_AWAITABLE    
              130  LOAD_CONST               None
              132  YIELD_FROM       
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'done'
              138  STORE_FAST               '_'

 L. 138       140  LOAD_GLOBAL              len
              142  LOAD_FAST                'done'
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'done_count'

 L. 142       148  LOAD_FAST                'done'
              150  GET_ITER         
            152_0  COME_FROM           178  '178'
            152_1  COME_FROM           170  '170'
            152_2  COME_FROM           162  '162'
              152  FOR_ITER            190  'to 190'
              154  STORE_FAST               'd'

 L. 143       156  LOAD_FAST                'd'
              158  LOAD_METHOD              done
              160  CALL_METHOD_0         0  ''
              162  POP_JUMP_IF_FALSE   152  'to 152'
              164  LOAD_FAST                'd'
              166  LOAD_METHOD              cancelled
              168  CALL_METHOD_0         0  ''
              170  POP_JUMP_IF_TRUE    152  'to 152'
              172  LOAD_FAST                'd'
              174  LOAD_METHOD              exception
              176  CALL_METHOD_0         0  ''
              178  POP_JUMP_IF_FALSE   152  'to 152'

 L. 144       180  LOAD_FAST                'd'
              182  LOAD_METHOD              exception
              184  CALL_METHOD_0         0  ''
              186  RAISE_VARARGS_1       1  'exception instance'
              188  JUMP_BACK           152  'to 152'
              190  JUMP_BACK           108  'to 108'
            192_0  COME_FROM           118  '118'

 L. 145       192  LOAD_DEREF               'winner_result'
              194  LOAD_DEREF               'winner_index'
              196  LOAD_DEREF               'exceptions'
              198  BUILD_TUPLE_3         3 
              200  POP_BLOCK        
              202  CALL_FINALLY        206  'to 206'
              204  RETURN_VALUE     
            206_0  COME_FROM           202  '202'
            206_1  COME_FROM_FINALLY   102  '102'

 L. 148       206  LOAD_DEREF               'running_tasks'
              208  GET_ITER         
              210  FOR_ITER            224  'to 224'
              212  STORE_FAST               't'

 L. 149       214  LOAD_FAST                't'
              216  LOAD_METHOD              cancel
              218  CALL_METHOD_0         0  ''
              220  POP_TOP          
              222  JUMP_BACK           210  'to 210'
              224  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 202