# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\base_futures.py
__all__ = ()
import reprlib
from _thread import get_ident
from . import format_helpers
_PENDING = 'PENDING'
_CANCELLED = 'CANCELLED'
_FINISHED = 'FINISHED'

def isfuture--- This code section failed: ---

 L.  21         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'obj'
                4  LOAD_ATTR                __class__
                6  LOAD_STR                 '_asyncio_future_blocking'
                8  CALL_FUNCTION_2       2  ''
               10  JUMP_IF_FALSE_OR_POP    20  'to 20'

 L.  22        12  LOAD_FAST                'obj'
               14  LOAD_ATTR                _asyncio_future_blocking
               16  LOAD_CONST               None
               18  <117>                 1  ''
             20_0  COME_FROM            10  '10'

 L.  21        20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18


def _format_callbacks(cb):
    """helper function for Future.__repr__"""
    size = len(cb)
    if not size:
        cb = ''

    def format_cb(callback):
        return format_helpers._format_callback_source(callback, ())

    if size == 1:
        cb = format_cb(cb[0][0])
    elif size == 2:
        cb = '{}, {}'.format(format_cb(cb[0][0]), format_cb(cb[1][0]))
    elif size > 2:
        cb = '{}, <{} more>, {}'.format(format_cb(cb[0][0]), size - 2, format_cb(cb[(-1)][0]))
    return f"cb=[{cb}]"


_repr_running = set()

def _future_repr_info--- This code section failed: ---

 L.  58         0  LOAD_FAST                'future'
                2  LOAD_ATTR                _state
                4  LOAD_METHOD              lower
                6  CALL_METHOD_0         0  ''
                8  BUILD_LIST_1          1 
               10  STORE_FAST               'info'

 L.  59        12  LOAD_FAST                'future'
               14  LOAD_ATTR                _state
               16  LOAD_GLOBAL              _FINISHED
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE   146  'to 146'

 L.  60        22  LOAD_FAST                'future'
               24  LOAD_ATTR                _exception
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    52  'to 52'

 L.  61        32  LOAD_FAST                'info'
               34  LOAD_METHOD              append
               36  LOAD_STR                 'exception='
               38  LOAD_FAST                'future'
               40  LOAD_ATTR                _exception
               42  FORMAT_VALUE          2  '!r'
               44  BUILD_STRING_2        2 
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  JUMP_FORWARD        146  'to 146'
             52_0  COME_FROM            30  '30'

 L.  63        52  LOAD_GLOBAL              id
               54  LOAD_FAST                'future'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_GLOBAL              get_ident
               60  CALL_FUNCTION_0       0  ''
               62  BUILD_TUPLE_2         2 
               64  STORE_FAST               'key'

 L.  64        66  LOAD_FAST                'key'
               68  LOAD_GLOBAL              _repr_running
               70  <118>                 0  ''
               72  POP_JUMP_IF_FALSE    80  'to 80'

 L.  65        74  LOAD_STR                 '...'
               76  STORE_FAST               'result'
               78  JUMP_FORWARD        130  'to 130'
             80_0  COME_FROM            72  '72'

 L.  67        80  LOAD_GLOBAL              _repr_running
               82  LOAD_METHOD              add
               84  LOAD_FAST                'key'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L.  68        90  SETUP_FINALLY       118  'to 118'

 L.  71        92  LOAD_GLOBAL              reprlib
               94  LOAD_METHOD              repr
               96  LOAD_FAST                'future'
               98  LOAD_ATTR                _result
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'result'
              104  POP_BLOCK        

 L.  73       106  LOAD_GLOBAL              _repr_running
              108  LOAD_METHOD              discard
              110  LOAD_FAST                'key'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  JUMP_FORWARD        130  'to 130'
            118_0  COME_FROM_FINALLY    90  '90'
              118  LOAD_GLOBAL              _repr_running
              120  LOAD_METHOD              discard
              122  LOAD_FAST                'key'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
              128  <48>             
            130_0  COME_FROM           116  '116'
            130_1  COME_FROM            78  '78'

 L.  74       130  LOAD_FAST                'info'
              132  LOAD_METHOD              append
              134  LOAD_STR                 'result='
              136  LOAD_FAST                'result'
              138  FORMAT_VALUE          0  ''
              140  BUILD_STRING_2        2 
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
            146_0  COME_FROM            50  '50'
            146_1  COME_FROM            20  '20'

 L.  75       146  LOAD_FAST                'future'
              148  LOAD_ATTR                _callbacks
              150  POP_JUMP_IF_FALSE   168  'to 168'

 L.  76       152  LOAD_FAST                'info'
              154  LOAD_METHOD              append
              156  LOAD_GLOBAL              _format_callbacks
              158  LOAD_FAST                'future'
              160  LOAD_ATTR                _callbacks
              162  CALL_FUNCTION_1       1  ''
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
            168_0  COME_FROM           150  '150'

 L.  77       168  LOAD_FAST                'future'
              170  LOAD_ATTR                _source_traceback
              172  POP_JUMP_IF_FALSE   214  'to 214'

 L.  78       174  LOAD_FAST                'future'
              176  LOAD_ATTR                _source_traceback
              178  LOAD_CONST               -1
              180  BINARY_SUBSCR    
              182  STORE_FAST               'frame'

 L.  79       184  LOAD_FAST                'info'
              186  LOAD_METHOD              append
              188  LOAD_STR                 'created at '
              190  LOAD_FAST                'frame'
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  FORMAT_VALUE          0  ''
              198  LOAD_STR                 ':'
              200  LOAD_FAST                'frame'
              202  LOAD_CONST               1
              204  BINARY_SUBSCR    
              206  FORMAT_VALUE          0  ''
              208  BUILD_STRING_4        4 
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          
            214_0  COME_FROM           172  '172'

 L.  80       214  LOAD_FAST                'info'
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28