# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\base_tasks.py
import linecache, traceback
from . import base_futures
from . import coroutines

def _task_repr_info--- This code section failed: ---

 L.   9         0  LOAD_GLOBAL              base_futures
                2  LOAD_METHOD              _future_repr_info
                4  LOAD_FAST                'task'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'info'

 L.  11        10  LOAD_FAST                'task'
               12  LOAD_ATTR                _must_cancel
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L.  13        16  LOAD_STR                 'cancelling'
               18  LOAD_FAST                'info'
               20  LOAD_CONST               0
               22  STORE_SUBSCR     
             24_0  COME_FROM            14  '14'

 L.  15        24  LOAD_FAST                'info'
               26  LOAD_METHOD              insert
               28  LOAD_CONST               1
               30  LOAD_STR                 'name=%r'
               32  LOAD_FAST                'task'
               34  LOAD_METHOD              get_name
               36  CALL_METHOD_0         0  ''
               38  BINARY_MODULO    
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          

 L.  17        44  LOAD_GLOBAL              coroutines
               46  LOAD_METHOD              _format_coroutine
               48  LOAD_FAST                'task'
               50  LOAD_ATTR                _coro
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               'coro'

 L.  18        56  LOAD_FAST                'info'
               58  LOAD_METHOD              insert
               60  LOAD_CONST               2
               62  LOAD_STR                 'coro=<'
               64  LOAD_FAST                'coro'
               66  FORMAT_VALUE          0  ''
               68  LOAD_STR                 '>'
               70  BUILD_STRING_3        3 
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          

 L.  20        76  LOAD_FAST                'task'
               78  LOAD_ATTR                _fut_waiter
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   106  'to 106'

 L.  21        86  LOAD_FAST                'info'
               88  LOAD_METHOD              insert
               90  LOAD_CONST               3
               92  LOAD_STR                 'wait_for='
               94  LOAD_FAST                'task'
               96  LOAD_ATTR                _fut_waiter
               98  FORMAT_VALUE          2  '!r'
              100  BUILD_STRING_2        2 
              102  CALL_METHOD_2         2  ''
              104  POP_TOP          
            106_0  COME_FROM            84  '84'

 L.  22       106  LOAD_FAST                'info'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 82


def _task_get_stack--- This code section failed: ---

 L.  26         0  BUILD_LIST_0          0 
                2  STORE_FAST               'frames'

 L.  27         4  LOAD_GLOBAL              hasattr
                6  LOAD_FAST                'task'
                8  LOAD_ATTR                _coro
               10  LOAD_STR                 'cr_frame'
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L.  29        16  LOAD_FAST                'task'
               18  LOAD_ATTR                _coro
               20  LOAD_ATTR                cr_frame
               22  STORE_FAST               'f'
               24  JUMP_FORWARD         74  'to 74'
             26_0  COME_FROM            14  '14'

 L.  30        26  LOAD_GLOBAL              hasattr
               28  LOAD_FAST                'task'
               30  LOAD_ATTR                _coro
               32  LOAD_STR                 'gi_frame'
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L.  32        38  LOAD_FAST                'task'
               40  LOAD_ATTR                _coro
               42  LOAD_ATTR                gi_frame
               44  STORE_FAST               'f'
               46  JUMP_FORWARD         74  'to 74'
             48_0  COME_FROM            36  '36'

 L.  33        48  LOAD_GLOBAL              hasattr
               50  LOAD_FAST                'task'
               52  LOAD_ATTR                _coro
               54  LOAD_STR                 'ag_frame'
               56  CALL_FUNCTION_2       2  ''
               58  POP_JUMP_IF_FALSE    70  'to 70'

 L.  35        60  LOAD_FAST                'task'
               62  LOAD_ATTR                _coro
               64  LOAD_ATTR                ag_frame
               66  STORE_FAST               'f'
               68  JUMP_FORWARD         74  'to 74'
             70_0  COME_FROM            58  '58'

 L.  38        70  LOAD_CONST               None
               72  STORE_FAST               'f'
             74_0  COME_FROM            68  '68'
             74_1  COME_FROM            46  '46'
             74_2  COME_FROM            24  '24'

 L.  39        74  LOAD_FAST                'f'
               76  LOAD_CONST               None
               78  <117>                 1  ''
               80  POP_JUMP_IF_FALSE   144  'to 144'

 L.  40        82  LOAD_FAST                'f'
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE   134  'to 134'

 L.  41        90  LOAD_FAST                'limit'
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   116  'to 116'

 L.  42        98  LOAD_FAST                'limit'
              100  LOAD_CONST               0
              102  COMPARE_OP               <=
              104  POP_JUMP_IF_FALSE   108  'to 108'

 L.  43       106  BREAK_LOOP          134  'to 134'
            108_0  COME_FROM           104  '104'

 L.  44       108  LOAD_FAST                'limit'
              110  LOAD_CONST               1
              112  INPLACE_SUBTRACT 
              114  STORE_FAST               'limit'
            116_0  COME_FROM            96  '96'

 L.  45       116  LOAD_FAST                'frames'
              118  LOAD_METHOD              append
              120  LOAD_FAST                'f'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L.  46       126  LOAD_FAST                'f'
              128  LOAD_ATTR                f_back
              130  STORE_FAST               'f'
              132  JUMP_BACK            82  'to 82'
            134_0  COME_FROM            88  '88'

 L.  47       134  LOAD_FAST                'frames'
              136  LOAD_METHOD              reverse
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          
              142  JUMP_FORWARD        216  'to 216'
            144_0  COME_FROM            80  '80'

 L.  48       144  LOAD_FAST                'task'
              146  LOAD_ATTR                _exception
              148  LOAD_CONST               None
              150  <117>                 1  ''
              152  POP_JUMP_IF_FALSE   216  'to 216'

 L.  49       154  LOAD_FAST                'task'
              156  LOAD_ATTR                _exception
              158  LOAD_ATTR                __traceback__
              160  STORE_FAST               'tb'

 L.  50       162  LOAD_FAST                'tb'
              164  LOAD_CONST               None
              166  <117>                 1  ''
              168  POP_JUMP_IF_FALSE   216  'to 216'

 L.  51       170  LOAD_FAST                'limit'
              172  LOAD_CONST               None
              174  <117>                 1  ''
              176  POP_JUMP_IF_FALSE   196  'to 196'

 L.  52       178  LOAD_FAST                'limit'
              180  LOAD_CONST               0
              182  COMPARE_OP               <=
              184  POP_JUMP_IF_FALSE   188  'to 188'

 L.  53       186  BREAK_LOOP          216  'to 216'
            188_0  COME_FROM           184  '184'

 L.  54       188  LOAD_FAST                'limit'
              190  LOAD_CONST               1
              192  INPLACE_SUBTRACT 
              194  STORE_FAST               'limit'
            196_0  COME_FROM           176  '176'

 L.  55       196  LOAD_FAST                'frames'
              198  LOAD_METHOD              append
              200  LOAD_FAST                'tb'
              202  LOAD_ATTR                tb_frame
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L.  56       208  LOAD_FAST                'tb'
              210  LOAD_ATTR                tb_next
              212  STORE_FAST               'tb'
              214  JUMP_BACK           162  'to 162'
            216_0  COME_FROM           168  '168'
            216_1  COME_FROM           152  '152'
            216_2  COME_FROM           142  '142'

 L.  57       216  LOAD_FAST                'frames'
              218  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 78


def _task_print_stack--- This code section failed: ---

 L.  61         0  BUILD_LIST_0          0 
                2  STORE_FAST               'extracted_list'

 L.  62         4  LOAD_GLOBAL              set
                6  CALL_FUNCTION_0       0  ''
                8  STORE_FAST               'checked'

 L.  63        10  LOAD_FAST                'task'
               12  LOAD_ATTR                get_stack
               14  LOAD_FAST                'limit'
               16  LOAD_CONST               ('limit',)
               18  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               20  GET_ITER         
               22  FOR_ITER            114  'to 114'
               24  STORE_FAST               'f'

 L.  64        26  LOAD_FAST                'f'
               28  LOAD_ATTR                f_lineno
               30  STORE_FAST               'lineno'

 L.  65        32  LOAD_FAST                'f'
               34  LOAD_ATTR                f_code
               36  STORE_FAST               'co'

 L.  66        38  LOAD_FAST                'co'
               40  LOAD_ATTR                co_filename
               42  STORE_FAST               'filename'

 L.  67        44  LOAD_FAST                'co'
               46  LOAD_ATTR                co_name
               48  STORE_FAST               'name'

 L.  68        50  LOAD_FAST                'filename'
               52  LOAD_FAST                'checked'
               54  <118>                 1  ''
               56  POP_JUMP_IF_FALSE    78  'to 78'

 L.  69        58  LOAD_FAST                'checked'
               60  LOAD_METHOD              add
               62  LOAD_FAST                'filename'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L.  70        68  LOAD_GLOBAL              linecache
               70  LOAD_METHOD              checkcache
               72  LOAD_FAST                'filename'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
             78_0  COME_FROM            56  '56'

 L.  71        78  LOAD_GLOBAL              linecache
               80  LOAD_METHOD              getline
               82  LOAD_FAST                'filename'
               84  LOAD_FAST                'lineno'
               86  LOAD_FAST                'f'
               88  LOAD_ATTR                f_globals
               90  CALL_METHOD_3         3  ''
               92  STORE_FAST               'line'

 L.  72        94  LOAD_FAST                'extracted_list'
               96  LOAD_METHOD              append
               98  LOAD_FAST                'filename'
              100  LOAD_FAST                'lineno'
              102  LOAD_FAST                'name'
              104  LOAD_FAST                'line'
              106  BUILD_TUPLE_4         4 
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
              112  JUMP_BACK            22  'to 22'

 L.  74       114  LOAD_FAST                'task'
              116  LOAD_ATTR                _exception
              118  STORE_FAST               'exc'

 L.  75       120  LOAD_FAST                'extracted_list'
              122  POP_JUMP_IF_TRUE    144  'to 144'

 L.  76       124  LOAD_GLOBAL              print
              126  LOAD_STR                 'No stack for '
              128  LOAD_FAST                'task'
              130  FORMAT_VALUE          2  '!r'
              132  BUILD_STRING_2        2 
              134  LOAD_FAST                'file'
              136  LOAD_CONST               ('file',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              140  POP_TOP          
              142  JUMP_FORWARD        194  'to 194'
            144_0  COME_FROM           122  '122'

 L.  77       144  LOAD_FAST                'exc'
              146  LOAD_CONST               None
              148  <117>                 1  ''
              150  POP_JUMP_IF_FALSE   174  'to 174'

 L.  78       152  LOAD_GLOBAL              print
              154  LOAD_STR                 'Traceback for '
              156  LOAD_FAST                'task'
              158  FORMAT_VALUE          2  '!r'
              160  LOAD_STR                 ' (most recent call last):'
              162  BUILD_STRING_3        3 
              164  LOAD_FAST                'file'
              166  LOAD_CONST               ('file',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          
              172  JUMP_FORWARD        194  'to 194'
            174_0  COME_FROM           150  '150'

 L.  80       174  LOAD_GLOBAL              print
              176  LOAD_STR                 'Stack for '
              178  LOAD_FAST                'task'
              180  FORMAT_VALUE          2  '!r'
              182  LOAD_STR                 ' (most recent call last):'
              184  BUILD_STRING_3        3 
              186  LOAD_FAST                'file'
              188  LOAD_CONST               ('file',)
              190  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              192  POP_TOP          
            194_0  COME_FROM           172  '172'
            194_1  COME_FROM           142  '142'

 L.  82       194  LOAD_GLOBAL              traceback
              196  LOAD_ATTR                print_list
              198  LOAD_FAST                'extracted_list'
              200  LOAD_FAST                'file'
              202  LOAD_CONST               ('file',)
              204  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              206  POP_TOP          

 L.  83       208  LOAD_FAST                'exc'
              210  LOAD_CONST               None
              212  <117>                 1  ''
              214  POP_JUMP_IF_FALSE   250  'to 250'

 L.  84       216  LOAD_GLOBAL              traceback
              218  LOAD_METHOD              format_exception_only
              220  LOAD_FAST                'exc'
              222  LOAD_ATTR                __class__
              224  LOAD_FAST                'exc'
              226  CALL_METHOD_2         2  ''
              228  GET_ITER         
              230  FOR_ITER            250  'to 250'
              232  STORE_FAST               'line'

 L.  85       234  LOAD_GLOBAL              print
              236  LOAD_FAST                'line'
              238  LOAD_FAST                'file'
              240  LOAD_STR                 ''
              242  LOAD_CONST               ('file', 'end')
              244  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              246  POP_TOP          
              248  JUMP_BACK           230  'to 230'
            250_0  COME_FROM           214  '214'

Parse error at or near `<118>' instruction at offset 54