# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\coroutines.py
__all__ = ('coroutine', 'iscoroutinefunction', 'iscoroutine')
import collections.abc, functools, inspect, os, sys, traceback, types, warnings
from . import base_futures
from . import constants
from . import format_helpers
from .log import logger

def _is_debug_mode():
    return (sys.flags.dev_mode) or ((not sys.flags.ignore_environment) and (bool(os.environ.get('PYTHONASYNCIODEBUG'))))


_DEBUG = _is_debug_mode()

class CoroWrapper:

    def __init__--- This code section failed: ---

 L.  40         0  LOAD_GLOBAL              inspect
                2  LOAD_METHOD              isgenerator
                4  LOAD_FAST                'gen'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     28  'to 28'
               10  LOAD_GLOBAL              inspect
               12  LOAD_METHOD              iscoroutine
               14  LOAD_FAST                'gen'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'
               20  <74>             
               22  LOAD_FAST                'gen'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM             8  '8'

 L.  41        28  LOAD_FAST                'gen'
               30  LOAD_FAST                'self'
               32  STORE_ATTR               gen

 L.  42        34  LOAD_FAST                'func'
               36  LOAD_FAST                'self'
               38  STORE_ATTR               func

 L.  43        40  LOAD_GLOBAL              format_helpers
               42  LOAD_METHOD              extract_stack
               44  LOAD_GLOBAL              sys
               46  LOAD_METHOD              _getframe
               48  LOAD_CONST               1
               50  CALL_METHOD_1         1  ''
               52  CALL_METHOD_1         1  ''
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _source_traceback

 L.  44        58  LOAD_GLOBAL              getattr
               60  LOAD_FAST                'gen'
               62  LOAD_STR                 '__name__'
               64  LOAD_CONST               None
               66  CALL_FUNCTION_3       3  ''
               68  LOAD_FAST                'self'
               70  STORE_ATTR               __name__

 L.  45        72  LOAD_GLOBAL              getattr
               74  LOAD_FAST                'gen'
               76  LOAD_STR                 '__qualname__'
               78  LOAD_CONST               None
               80  CALL_FUNCTION_3       3  ''
               82  LOAD_FAST                'self'
               84  STORE_ATTR               __qualname__

Parse error at or near `None' instruction at offset -1

    def __repr__(self):
        coro_repr = _format_coroutine(self)
        if self._source_traceback:
            frame = self._source_traceback[(-1)]
            coro_repr += f", created at {frame[0]}:{frame[1]}"
        return f"<{self.__class__.__name__} {coro_repr}>"

    def __iter__(self):
        return self

    def __next__(self):
        return self.gen.send(None)

    def send(self, value):
        return self.gen.send(value)

    def throw(self, type, value=None, traceback=None):
        return self.gen.throw(type, value, traceback)

    def close(self):
        return self.gen.close()

    @property
    def gi_frame(self):
        return self.gen.gi_frame

    @property
    def gi_running(self):
        return self.gen.gi_running

    @property
    def gi_code(self):
        return self.gen.gi_code

    def __await__(self):
        return self

    @property
    def gi_yieldfrom(self):
        return self.gen.gi_yieldfrom

    def __del__--- This code section failed: ---

 L.  91         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'gen'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'gen'

 L.  92        12  LOAD_GLOBAL              getattr
               14  LOAD_FAST                'gen'
               16  LOAD_STR                 'gi_frame'
               18  LOAD_CONST               None
               20  CALL_FUNCTION_3       3  ''
               22  STORE_FAST               'frame'

 L.  93        24  LOAD_FAST                'frame'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE   124  'to 124'
               32  LOAD_FAST                'frame'
               34  LOAD_ATTR                f_lasti
               36  LOAD_CONST               -1
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE   124  'to 124'

 L.  94        42  LOAD_FAST                'self'
               44  FORMAT_VALUE          2  '!r'
               46  LOAD_STR                 ' was never yielded from'
               48  BUILD_STRING_2        2 
               50  STORE_FAST               'msg'

 L.  95        52  LOAD_GLOBAL              getattr
               54  LOAD_FAST                'self'
               56  LOAD_STR                 '_source_traceback'
               58  LOAD_CONST               ()
               60  CALL_FUNCTION_3       3  ''
               62  STORE_FAST               'tb'

 L.  96        64  LOAD_FAST                'tb'
               66  POP_JUMP_IF_FALSE   114  'to 114'

 L.  97        68  LOAD_STR                 ''
               70  LOAD_METHOD              join
               72  LOAD_GLOBAL              traceback
               74  LOAD_METHOD              format_list
               76  LOAD_FAST                'tb'
               78  CALL_METHOD_1         1  ''
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'tb'

 L.  98        84  LOAD_FAST                'msg'
               86  LOAD_STR                 '\nCoroutine object created at (most recent call last, truncated to '

 L. 100        88  LOAD_GLOBAL              constants
               90  LOAD_ATTR                DEBUG_STACK_DEPTH

 L.  98        92  FORMAT_VALUE          0  ''
               94  LOAD_STR                 ' last lines):\n'
               96  BUILD_STRING_3        3 
               98  INPLACE_ADD      
              100  STORE_FAST               'msg'

 L. 101       102  LOAD_FAST                'msg'
              104  LOAD_FAST                'tb'
              106  LOAD_METHOD              rstrip
              108  CALL_METHOD_0         0  ''
              110  INPLACE_ADD      
              112  STORE_FAST               'msg'
            114_0  COME_FROM            66  '66'

 L. 102       114  LOAD_GLOBAL              logger
              116  LOAD_METHOD              error
              118  LOAD_FAST                'msg'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
            124_0  COME_FROM            40  '40'
            124_1  COME_FROM            30  '30'

Parse error at or near `<117>' instruction at offset 28


def coroutine(func):
    """Decorator to mark coroutines.

    If the coroutine is not yielded from before it is destroyed,
    an error message is logged.
    """
    warnings.warn('"@coroutine" decorator is deprecated since Python 3.8, use "async def" instead', DeprecationWarning,
      stacklevel=2)
    if inspect.iscoroutinefunction(func):
        return func
    if inspect.isgeneratorfunction(func):
        coro = func
    else:

        @functools.wraps(func)
        def coro--- This code section failed: ---

 L. 124         0  LOAD_DEREF               'func'
                2  LOAD_FAST                'args'
                4  BUILD_MAP_0           0 
                6  LOAD_FAST                'kw'
                8  <164>                 1  ''
               10  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               12  STORE_FAST               'res'

 L. 125        14  LOAD_GLOBAL              base_futures
               16  LOAD_METHOD              isfuture
               18  LOAD_FAST                'res'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_TRUE     44  'to 44'
               24  LOAD_GLOBAL              inspect
               26  LOAD_METHOD              isgenerator
               28  LOAD_FAST                'res'
               30  CALL_METHOD_1         1  ''
               32  POP_JUMP_IF_TRUE     44  'to 44'

 L. 126        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'res'
               38  LOAD_GLOBAL              CoroWrapper
               40  CALL_FUNCTION_2       2  ''

 L. 125        42  POP_JUMP_IF_FALSE    56  'to 56'
             44_0  COME_FROM            32  '32'
             44_1  COME_FROM            22  '22'

 L. 127        44  LOAD_FAST                'res'
               46  GET_YIELD_FROM_ITER
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  STORE_FAST               'res'
               54  JUMP_FORWARD        112  'to 112'
             56_0  COME_FROM            42  '42'

 L. 130        56  SETUP_FINALLY        68  'to 68'

 L. 131        58  LOAD_FAST                'res'
               60  LOAD_ATTR                __await__
               62  STORE_FAST               'await_meth'
               64  POP_BLOCK        
               66  JUMP_FORWARD         86  'to 86'
             68_0  COME_FROM_FINALLY    56  '56'

 L. 132        68  DUP_TOP          
               70  LOAD_GLOBAL              AttributeError
               72  <121>                84  ''
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 133        80  POP_EXCEPT       
               82  JUMP_FORWARD        112  'to 112'
               84  <48>             
             86_0  COME_FROM            66  '66'

 L. 135        86  LOAD_GLOBAL              isinstance
               88  LOAD_FAST                'res'
               90  LOAD_GLOBAL              collections
               92  LOAD_ATTR                abc
               94  LOAD_ATTR                Awaitable
               96  CALL_FUNCTION_2       2  ''
               98  POP_JUMP_IF_FALSE   112  'to 112'

 L. 136       100  LOAD_FAST                'await_meth'
              102  CALL_FUNCTION_0       0  ''
              104  GET_YIELD_FROM_ITER
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  STORE_FAST               'res'
            112_0  COME_FROM            98  '98'
            112_1  COME_FROM            82  '82'
            112_2  COME_FROM            54  '54'

 L. 137       112  LOAD_FAST                'res'
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    coro = types.coroutine(coro)
    if not _DEBUG:
        wrapper = coro
    else:

        @functools.wraps(func)
        def wrapper--- This code section failed: ---

 L. 145         0  LOAD_GLOBAL              CoroWrapper
                2  LOAD_DEREF               'coro'
                4  LOAD_FAST                'args'
                6  BUILD_MAP_0           0 
                8  LOAD_FAST                'kwds'
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  LOAD_DEREF               'func'
               16  LOAD_CONST               ('func',)
               18  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               20  STORE_FAST               'w'

 L. 146        22  LOAD_FAST                'w'
               24  LOAD_ATTR                _source_traceback
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 147        28  LOAD_FAST                'w'
               30  LOAD_ATTR                _source_traceback
               32  LOAD_CONST               -1
               34  DELETE_SUBSCR    
             36_0  COME_FROM            26  '26'

 L. 152        36  LOAD_GLOBAL              getattr
               38  LOAD_DEREF               'func'
               40  LOAD_STR                 '__name__'
               42  LOAD_CONST               None
               44  CALL_FUNCTION_3       3  ''
               46  LOAD_FAST                'w'
               48  STORE_ATTR               __name__

 L. 153        50  LOAD_GLOBAL              getattr
               52  LOAD_DEREF               'func'
               54  LOAD_STR                 '__qualname__'
               56  LOAD_CONST               None
               58  CALL_FUNCTION_3       3  ''
               60  LOAD_FAST                'w'
               62  STORE_ATTR               __qualname__

 L. 154        64  LOAD_FAST                'w'
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    wrapper._is_coroutine = _is_coroutine
    return wrapper


_is_coroutine = object()

def iscoroutinefunction--- This code section failed: ---

 L. 166         0  LOAD_GLOBAL              inspect
                2  LOAD_METHOD              iscoroutinefunction
                4  LOAD_FAST                'func'
                6  CALL_METHOD_1         1  ''
                8  JUMP_IF_TRUE_OR_POP    24  'to 24'

 L. 167        10  LOAD_GLOBAL              getattr
               12  LOAD_FAST                'func'
               14  LOAD_STR                 '_is_coroutine'
               16  LOAD_CONST               None
               18  CALL_FUNCTION_3       3  ''
               20  LOAD_GLOBAL              _is_coroutine
               22  <117>                 0  ''
             24_0  COME_FROM             8  '8'

 L. 166        24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22


_COROUTINE_TYPES = (
 types.CoroutineType, types.GeneratorType,
 collections.abc.Coroutine, CoroWrapper)
_iscoroutine_typecache = set()

def iscoroutine--- This code section failed: ---

 L. 179         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'obj'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              _iscoroutine_typecache
                8  <118>                 0  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 180        12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 182        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'obj'
               20  LOAD_GLOBAL              _COROUTINE_TYPES
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_FALSE    56  'to 56'

 L. 186        26  LOAD_GLOBAL              len
               28  LOAD_GLOBAL              _iscoroutine_typecache
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               100
               34  COMPARE_OP               <
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 187        38  LOAD_GLOBAL              _iscoroutine_typecache
               40  LOAD_METHOD              add
               42  LOAD_GLOBAL              type
               44  LOAD_FAST                'obj'
               46  CALL_FUNCTION_1       1  ''
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
             52_0  COME_FROM            36  '36'

 L. 188        52  LOAD_CONST               True
               54  RETURN_VALUE     
             56_0  COME_FROM            24  '24'

 L. 190        56  LOAD_CONST               False
               58  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _format_coroutine--- This code section failed: ---

 L. 194         0  LOAD_GLOBAL              iscoroutine
                2  LOAD_FAST                'coro'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L. 196        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'coro'
               16  LOAD_GLOBAL              CoroWrapper
               18  CALL_FUNCTION_2       2  ''
               20  STORE_DEREF              'is_corowrapper'

 L. 198        22  LOAD_CLOSURE             'is_corowrapper'
               24  BUILD_TUPLE_1         1 
               26  LOAD_CODE                <code_object get_name>
               28  LOAD_STR                 '_format_coroutine.<locals>.get_name'
               30  MAKE_FUNCTION_8          'closure'
               32  STORE_FAST               'get_name'

 L. 215        34  LOAD_CODE                <code_object is_running>
               36  LOAD_STR                 '_format_coroutine.<locals>.is_running'
               38  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               40  STORE_FAST               'is_running'

 L. 224        42  LOAD_CONST               None
               44  STORE_FAST               'coro_code'

 L. 225        46  LOAD_GLOBAL              hasattr
               48  LOAD_FAST                'coro'
               50  LOAD_STR                 'cr_code'
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_FALSE    70  'to 70'
               56  LOAD_FAST                'coro'
               58  LOAD_ATTR                cr_code
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L. 226        62  LOAD_FAST                'coro'
               64  LOAD_ATTR                cr_code
               66  STORE_FAST               'coro_code'
               68  JUMP_FORWARD         92  'to 92'
             70_0  COME_FROM            60  '60'
             70_1  COME_FROM            54  '54'

 L. 227        70  LOAD_GLOBAL              hasattr
               72  LOAD_FAST                'coro'
               74  LOAD_STR                 'gi_code'
               76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_FALSE    92  'to 92'
               80  LOAD_FAST                'coro'
               82  LOAD_ATTR                gi_code
               84  POP_JUMP_IF_FALSE    92  'to 92'

 L. 228        86  LOAD_FAST                'coro'
               88  LOAD_ATTR                gi_code
               90  STORE_FAST               'coro_code'
             92_0  COME_FROM            84  '84'
             92_1  COME_FROM            78  '78'
             92_2  COME_FROM            68  '68'

 L. 230        92  LOAD_FAST                'get_name'
               94  LOAD_FAST                'coro'
               96  CALL_FUNCTION_1       1  ''
               98  STORE_FAST               'coro_name'

 L. 232       100  LOAD_FAST                'coro_code'
              102  POP_JUMP_IF_TRUE    126  'to 126'

 L. 234       104  LOAD_FAST                'is_running'
              106  LOAD_FAST                'coro'
              108  CALL_FUNCTION_1       1  ''
              110  POP_JUMP_IF_FALSE   122  'to 122'

 L. 235       112  LOAD_FAST                'coro_name'
              114  FORMAT_VALUE          0  ''
              116  LOAD_STR                 ' running'
              118  BUILD_STRING_2        2 
              120  RETURN_VALUE     
            122_0  COME_FROM           110  '110'

 L. 237       122  LOAD_FAST                'coro_name'
              124  RETURN_VALUE     
            126_0  COME_FROM           102  '102'

 L. 239       126  LOAD_CONST               None
              128  STORE_FAST               'coro_frame'

 L. 240       130  LOAD_GLOBAL              hasattr
              132  LOAD_FAST                'coro'
              134  LOAD_STR                 'gi_frame'
              136  CALL_FUNCTION_2       2  ''
              138  POP_JUMP_IF_FALSE   154  'to 154'
              140  LOAD_FAST                'coro'
              142  LOAD_ATTR                gi_frame
              144  POP_JUMP_IF_FALSE   154  'to 154'

 L. 241       146  LOAD_FAST                'coro'
              148  LOAD_ATTR                gi_frame
              150  STORE_FAST               'coro_frame'
              152  JUMP_FORWARD        176  'to 176'
            154_0  COME_FROM           144  '144'
            154_1  COME_FROM           138  '138'

 L. 242       154  LOAD_GLOBAL              hasattr
              156  LOAD_FAST                'coro'
              158  LOAD_STR                 'cr_frame'
              160  CALL_FUNCTION_2       2  ''
              162  POP_JUMP_IF_FALSE   176  'to 176'
              164  LOAD_FAST                'coro'
              166  LOAD_ATTR                cr_frame
              168  POP_JUMP_IF_FALSE   176  'to 176'

 L. 243       170  LOAD_FAST                'coro'
              172  LOAD_ATTR                cr_frame
              174  STORE_FAST               'coro_frame'
            176_0  COME_FROM           168  '168'
            176_1  COME_FROM           162  '162'
            176_2  COME_FROM           152  '152'

 L. 247       176  LOAD_FAST                'coro_code'
              178  LOAD_ATTR                co_filename
              180  JUMP_IF_TRUE_OR_POP   184  'to 184'
              182  LOAD_STR                 '<empty co_filename>'
            184_0  COME_FROM           180  '180'
              184  STORE_FAST               'filename'

 L. 249       186  LOAD_CONST               0
              188  STORE_FAST               'lineno'

 L. 250       190  LOAD_DEREF               'is_corowrapper'
          192_194  POP_JUMP_IF_FALSE   304  'to 304'

 L. 251       196  LOAD_FAST                'coro'
              198  LOAD_ATTR                func
              200  LOAD_CONST               None
              202  <117>                 1  ''

 L. 250   204_206  POP_JUMP_IF_FALSE   304  'to 304'

 L. 252       208  LOAD_GLOBAL              inspect
              210  LOAD_METHOD              isgeneratorfunction
              212  LOAD_FAST                'coro'
              214  LOAD_ATTR                func
              216  CALL_METHOD_1         1  ''

 L. 250   218_220  POP_JUMP_IF_TRUE    304  'to 304'

 L. 253       222  LOAD_GLOBAL              format_helpers
              224  LOAD_METHOD              _get_function_source
              226  LOAD_FAST                'coro'
              228  LOAD_ATTR                func
              230  CALL_METHOD_1         1  ''
              232  STORE_FAST               'source'

 L. 254       234  LOAD_FAST                'source'
              236  LOAD_CONST               None
              238  <117>                 1  ''
              240  POP_JUMP_IF_FALSE   250  'to 250'

 L. 255       242  LOAD_FAST                'source'
              244  UNPACK_SEQUENCE_2     2 
              246  STORE_FAST               'filename'
              248  STORE_FAST               'lineno'
            250_0  COME_FROM           240  '240'

 L. 256       250  LOAD_FAST                'coro_frame'
              252  LOAD_CONST               None
              254  <117>                 0  ''
          256_258  POP_JUMP_IF_FALSE   282  'to 282'

 L. 257       260  LOAD_FAST                'coro_name'
              262  FORMAT_VALUE          0  ''
              264  LOAD_STR                 ' done, defined at '
              266  LOAD_FAST                'filename'
              268  FORMAT_VALUE          0  ''
              270  LOAD_STR                 ':'
              272  LOAD_FAST                'lineno'
              274  FORMAT_VALUE          0  ''
              276  BUILD_STRING_5        5 
              278  STORE_FAST               'coro_repr'
              280  JUMP_FORWARD        302  'to 302'
            282_0  COME_FROM           256  '256'

 L. 259       282  LOAD_FAST                'coro_name'
              284  FORMAT_VALUE          0  ''
              286  LOAD_STR                 ' running, defined at '
              288  LOAD_FAST                'filename'
              290  FORMAT_VALUE          0  ''
              292  LOAD_STR                 ':'
              294  LOAD_FAST                'lineno'
              296  FORMAT_VALUE          0  ''
              298  BUILD_STRING_5        5 
              300  STORE_FAST               'coro_repr'
            302_0  COME_FROM           280  '280'
              302  JUMP_FORWARD        368  'to 368'
            304_0  COME_FROM           218  '218'
            304_1  COME_FROM           204  '204'
            304_2  COME_FROM           192  '192'

 L. 261       304  LOAD_FAST                'coro_frame'
              306  LOAD_CONST               None
              308  <117>                 1  ''
          310_312  POP_JUMP_IF_FALSE   342  'to 342'

 L. 262       314  LOAD_FAST                'coro_frame'
              316  LOAD_ATTR                f_lineno
              318  STORE_FAST               'lineno'

 L. 263       320  LOAD_FAST                'coro_name'
              322  FORMAT_VALUE          0  ''
              324  LOAD_STR                 ' running at '
              326  LOAD_FAST                'filename'
              328  FORMAT_VALUE          0  ''
              330  LOAD_STR                 ':'
              332  LOAD_FAST                'lineno'
              334  FORMAT_VALUE          0  ''
              336  BUILD_STRING_5        5 
              338  STORE_FAST               'coro_repr'
              340  JUMP_FORWARD        368  'to 368'
            342_0  COME_FROM           310  '310'

 L. 266       342  LOAD_FAST                'coro_code'
              344  LOAD_ATTR                co_firstlineno
              346  STORE_FAST               'lineno'

 L. 267       348  LOAD_FAST                'coro_name'
              350  FORMAT_VALUE          0  ''
              352  LOAD_STR                 ' done, defined at '
              354  LOAD_FAST                'filename'
              356  FORMAT_VALUE          0  ''
              358  LOAD_STR                 ':'
              360  LOAD_FAST                'lineno'
              362  FORMAT_VALUE          0  ''
              364  BUILD_STRING_5        5 
              366  STORE_FAST               'coro_repr'
            368_0  COME_FROM           340  '340'
            368_1  COME_FROM           302  '302'

 L. 269       368  LOAD_FAST                'coro_repr'
              370  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1