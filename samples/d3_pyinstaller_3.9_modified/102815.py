# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\base_futures.py
__all__ = ()
import reprlib
from . import format_helpers
_PENDING = 'PENDING'
_CANCELLED = 'CANCELLED'
_FINISHED = 'FINISHED'

def isfuture--- This code section failed: ---

 L.  20         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'obj'
                4  LOAD_ATTR                __class__
                6  LOAD_STR                 '_asyncio_future_blocking'
                8  CALL_FUNCTION_2       2  ''
               10  JUMP_IF_FALSE_OR_POP    20  'to 20'

 L.  21        12  LOAD_FAST                'obj'
               14  LOAD_ATTR                _asyncio_future_blocking
               16  LOAD_CONST               None
               18  <117>                 1  ''
             20_0  COME_FROM            10  '10'

 L.  20        20  RETURN_VALUE     
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


def _future_repr_info--- This code section failed: ---

 L.  47         0  LOAD_FAST                'future'
                2  LOAD_ATTR                _state
                4  LOAD_METHOD              lower
                6  CALL_METHOD_0         0  ''
                8  BUILD_LIST_1          1 
               10  STORE_FAST               'info'

 L.  48        12  LOAD_FAST                'future'
               14  LOAD_ATTR                _state
               16  LOAD_GLOBAL              _FINISHED
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    80  'to 80'

 L.  49        22  LOAD_FAST                'future'
               24  LOAD_ATTR                _exception
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    52  'to 52'

 L.  50        32  LOAD_FAST                'info'
               34  LOAD_METHOD              append
               36  LOAD_STR                 'exception='
               38  LOAD_FAST                'future'
               40  LOAD_ATTR                _exception
               42  FORMAT_VALUE          2  '!r'
               44  BUILD_STRING_2        2 
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  JUMP_FORWARD         80  'to 80'
             52_0  COME_FROM            30  '30'

 L.  54        52  LOAD_GLOBAL              reprlib
               54  LOAD_METHOD              repr
               56  LOAD_FAST                'future'
               58  LOAD_ATTR                _result
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'result'

 L.  55        64  LOAD_FAST                'info'
               66  LOAD_METHOD              append
               68  LOAD_STR                 'result='
               70  LOAD_FAST                'result'
               72  FORMAT_VALUE          0  ''
               74  BUILD_STRING_2        2 
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
             80_0  COME_FROM            50  '50'
             80_1  COME_FROM            20  '20'

 L.  56        80  LOAD_FAST                'future'
               82  LOAD_ATTR                _callbacks
               84  POP_JUMP_IF_FALSE   102  'to 102'

 L.  57        86  LOAD_FAST                'info'
               88  LOAD_METHOD              append
               90  LOAD_GLOBAL              _format_callbacks
               92  LOAD_FAST                'future'
               94  LOAD_ATTR                _callbacks
               96  CALL_FUNCTION_1       1  ''
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
            102_0  COME_FROM            84  '84'

 L.  58       102  LOAD_FAST                'future'
              104  LOAD_ATTR                _source_traceback
              106  POP_JUMP_IF_FALSE   148  'to 148'

 L.  59       108  LOAD_FAST                'future'
              110  LOAD_ATTR                _source_traceback
              112  LOAD_CONST               -1
              114  BINARY_SUBSCR    
              116  STORE_FAST               'frame'

 L.  60       118  LOAD_FAST                'info'
              120  LOAD_METHOD              append
              122  LOAD_STR                 'created at '
              124  LOAD_FAST                'frame'
              126  LOAD_CONST               0
              128  BINARY_SUBSCR    
              130  FORMAT_VALUE          0  ''
              132  LOAD_STR                 ':'
              134  LOAD_FAST                'frame'
              136  LOAD_CONST               1
              138  BINARY_SUBSCR    
              140  FORMAT_VALUE          0  ''
              142  BUILD_STRING_4        4 
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
            148_0  COME_FROM           106  '106'

 L.  61       148  LOAD_FAST                'info'
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28