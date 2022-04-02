# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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
                8  <117>                 1  ''
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

 L.  40        52  SETUP_FINALLY       256  'to 256'

 L.  41        54  LOAD_GLOBAL              events
               56  LOAD_METHOD              set_event_loop
               58  LOAD_FAST                'loop'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L.  42        64  LOAD_FAST                'debug'
               66  LOAD_CONST               None
               68  <117>                 1  ''
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

 L.  46        92  SETUP_FINALLY       152  'to 152'

 L.  47        94  LOAD_GLOBAL              _cancel_all_tasks
               96  LOAD_FAST                'loop'
               98  CALL_FUNCTION_1       1  ''
              100  POP_TOP          

 L.  48       102  LOAD_FAST                'loop'
              104  LOAD_METHOD              run_until_complete
              106  LOAD_FAST                'loop'
              108  LOAD_METHOD              shutdown_asyncgens
              110  CALL_METHOD_0         0  ''
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L.  49       116  LOAD_FAST                'loop'
              118  LOAD_METHOD              run_until_complete
              120  LOAD_FAST                'loop'
              122  LOAD_METHOD              shutdown_default_executor
              124  CALL_METHOD_0         0  ''
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
              130  POP_BLOCK        

 L.  51       132  LOAD_GLOBAL              events
              134  LOAD_METHOD              set_event_loop
              136  LOAD_CONST               None
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L.  52       142  LOAD_FAST                'loop'
              144  LOAD_METHOD              close
              146  CALL_METHOD_0         0  ''
              148  POP_TOP          
              150  RETURN_VALUE     
            152_0  COME_FROM_FINALLY    92  '92'

 L.  51       152  LOAD_GLOBAL              events
              154  LOAD_METHOD              set_event_loop
              156  LOAD_CONST               None
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L.  52       162  LOAD_FAST                'loop'
              164  LOAD_METHOD              close
              166  CALL_METHOD_0         0  ''
              168  POP_TOP          
              170  <48>             

 L.  44       172  RETURN_VALUE     

 L.  46       174  SETUP_FINALLY       234  'to 234'

 L.  47       176  LOAD_GLOBAL              _cancel_all_tasks
              178  LOAD_FAST                'loop'
              180  CALL_FUNCTION_1       1  ''
              182  POP_TOP          

 L.  48       184  LOAD_FAST                'loop'
              186  LOAD_METHOD              run_until_complete
              188  LOAD_FAST                'loop'
              190  LOAD_METHOD              shutdown_asyncgens
              192  CALL_METHOD_0         0  ''
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          

 L.  49       198  LOAD_FAST                'loop'
              200  LOAD_METHOD              run_until_complete
              202  LOAD_FAST                'loop'
              204  LOAD_METHOD              shutdown_default_executor
              206  CALL_METHOD_0         0  ''
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
              212  POP_BLOCK        

 L.  51       214  LOAD_GLOBAL              events
              216  LOAD_METHOD              set_event_loop
              218  LOAD_CONST               None
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          

 L.  52       224  LOAD_FAST                'loop'
              226  LOAD_METHOD              close
              228  CALL_METHOD_0         0  ''
              230  POP_TOP          
              232  JUMP_FORWARD        254  'to 254'
            234_0  COME_FROM_FINALLY   174  '174'

 L.  51       234  LOAD_GLOBAL              events
              236  LOAD_METHOD              set_event_loop
              238  LOAD_CONST               None
              240  CALL_METHOD_1         1  ''
              242  POP_TOP          

 L.  52       244  LOAD_FAST                'loop'
              246  LOAD_METHOD              close
              248  CALL_METHOD_0         0  ''
              250  POP_TOP          
              252  <48>             
            254_0  COME_FROM           232  '232'
              254  JUMP_FORWARD        338  'to 338'
            256_0  COME_FROM_FINALLY    52  '52'

 L.  46       256  SETUP_FINALLY       316  'to 316'

 L.  47       258  LOAD_GLOBAL              _cancel_all_tasks
              260  LOAD_FAST                'loop'
              262  CALL_FUNCTION_1       1  ''
              264  POP_TOP          

 L.  48       266  LOAD_FAST                'loop'
              268  LOAD_METHOD              run_until_complete
              270  LOAD_FAST                'loop'
              272  LOAD_METHOD              shutdown_asyncgens
              274  CALL_METHOD_0         0  ''
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          

 L.  49       280  LOAD_FAST                'loop'
              282  LOAD_METHOD              run_until_complete
              284  LOAD_FAST                'loop'
              286  LOAD_METHOD              shutdown_default_executor
              288  CALL_METHOD_0         0  ''
              290  CALL_METHOD_1         1  ''
              292  POP_TOP          
              294  POP_BLOCK        

 L.  51       296  LOAD_GLOBAL              events
              298  LOAD_METHOD              set_event_loop
              300  LOAD_CONST               None
              302  CALL_METHOD_1         1  ''
              304  POP_TOP          

 L.  52       306  LOAD_FAST                'loop'
              308  LOAD_METHOD              close
              310  CALL_METHOD_0         0  ''
              312  POP_TOP          
              314  JUMP_FORWARD        336  'to 336'
            316_0  COME_FROM_FINALLY   256  '256'

 L.  51       316  LOAD_GLOBAL              events
              318  LOAD_METHOD              set_event_loop
              320  LOAD_CONST               None
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          

 L.  52       326  LOAD_FAST                'loop'
              328  LOAD_METHOD              close
              330  CALL_METHOD_0         0  ''
              332  POP_TOP          
              334  <48>             
            336_0  COME_FROM           314  '314'
              336  <48>             
            338_0  COME_FROM           254  '254'

Parse error at or near `None' instruction at offset -1


def _cancel_all_tasks--- This code section failed: ---

 L.  56         0  LOAD_GLOBAL              tasks
                2  LOAD_METHOD              all_tasks
                4  LOAD_FAST                'loop'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'to_cancel'

 L.  57        10  LOAD_FAST                'to_cancel'
               12  POP_JUMP_IF_TRUE     18  'to 18'

 L.  58        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L.  60        18  LOAD_FAST                'to_cancel'
               20  GET_ITER         
               22  FOR_ITER             36  'to 36'
               24  STORE_FAST               'task'

 L.  61        26  LOAD_FAST                'task'
               28  LOAD_METHOD              cancel
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          
               34  JUMP_BACK            22  'to 22'

 L.  63        36  LOAD_FAST                'loop'
               38  LOAD_METHOD              run_until_complete

 L.  64        40  LOAD_GLOBAL              tasks
               42  LOAD_ATTR                gather
               44  LOAD_FAST                'to_cancel'
               46  LOAD_FAST                'loop'
               48  LOAD_CONST               True
               50  LOAD_CONST               ('loop', 'return_exceptions')
               52  BUILD_CONST_KEY_MAP_2     2 
               54  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L.  63        56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.  66        60  LOAD_FAST                'to_cancel'
               62  GET_ITER         
             64_0  COME_FROM            88  '88'
               64  FOR_ITER            114  'to 114'
               66  STORE_FAST               'task'

 L.  67        68  LOAD_FAST                'task'
               70  LOAD_METHOD              cancelled
               72  CALL_METHOD_0         0  ''
               74  POP_JUMP_IF_FALSE    78  'to 78'

 L.  68        76  JUMP_BACK            64  'to 64'
             78_0  COME_FROM            74  '74'

 L.  69        78  LOAD_FAST                'task'
               80  LOAD_METHOD              exception
               82  CALL_METHOD_0         0  ''
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE    64  'to 64'

 L.  70        90  LOAD_FAST                'loop'
               92  LOAD_METHOD              call_exception_handler

 L.  71        94  LOAD_STR                 'unhandled exception during asyncio.run() shutdown'

 L.  72        96  LOAD_FAST                'task'
               98  LOAD_METHOD              exception
              100  CALL_METHOD_0         0  ''

 L.  73       102  LOAD_FAST                'task'

 L.  70       104  LOAD_CONST               ('message', 'exception', 'task')
              106  BUILD_CONST_KEY_MAP_3     3 
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
              112  JUMP_BACK            64  'to 64'

Parse error at or near `<117>' instruction at offset 86