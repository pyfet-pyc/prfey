# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: unittest\signals.py
import signal, weakref
from functools import wraps
__unittest = True

class _InterruptHandler(object):

    def __init__(self, default_handler):
        self.called = False
        self.original_handler = default_handler
        if isinstance(default_handler, int):
            if default_handler == signal.SIG_DFL:
                default_handler = signal.default_int_handler
            elif default_handler == signal.SIG_IGN:

                def default_handler(unused_signum, unused_frame):
                    pass

            else:
                raise TypeError('expected SIGINT signal handler to be signal.SIG_IGN, signal.SIG_DFL, or a callable object')
        self.default_handler = default_handler

    def __call__--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL              signal
                2  LOAD_METHOD              getsignal
                4  LOAD_GLOBAL              signal
                6  LOAD_ATTR                SIGINT
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'installed_handler'

 L.  30        12  LOAD_FAST                'installed_handler'
               14  LOAD_FAST                'self'
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L.  33        20  LOAD_FAST                'self'
               22  LOAD_METHOD              default_handler
               24  LOAD_FAST                'signum'
               26  LOAD_FAST                'frame'
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          
             32_0  COME_FROM            18  '18'

 L.  35        32  LOAD_FAST                'self'
               34  LOAD_ATTR                called
               36  POP_JUMP_IF_FALSE    50  'to 50'

 L.  36        38  LOAD_FAST                'self'
               40  LOAD_METHOD              default_handler
               42  LOAD_FAST                'signum'
               44  LOAD_FAST                'frame'
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          
             50_0  COME_FROM            36  '36'

 L.  37        50  LOAD_CONST               True
               52  LOAD_FAST                'self'
               54  STORE_ATTR               called

 L.  38        56  LOAD_GLOBAL              _results
               58  LOAD_METHOD              keys
               60  CALL_METHOD_0         0  ''
               62  GET_ITER         
             64_0  COME_FROM            76  '76'
               64  FOR_ITER             78  'to 78'
               66  STORE_FAST               'result'

 L.  39        68  LOAD_FAST                'result'
               70  LOAD_METHOD              stop
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          
               76  JUMP_BACK            64  'to 64'
             78_0  COME_FROM            64  '64'

Parse error at or near `<117>' instruction at offset 16


_results = weakref.WeakKeyDictionary()

def registerResult(result):
    _results[result] = 1


def removeResult(result):
    return bool(_results.popresultNone)


_interrupt_handler = None

def installHandler--- This code section failed: ---

 L.  51         0  LOAD_GLOBAL              _interrupt_handler
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    42  'to 42'

 L.  52         8  LOAD_GLOBAL              signal
               10  LOAD_METHOD              getsignal
               12  LOAD_GLOBAL              signal
               14  LOAD_ATTR                SIGINT
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'default_handler'

 L.  53        20  LOAD_GLOBAL              _InterruptHandler
               22  LOAD_FAST                'default_handler'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_GLOBAL             _interrupt_handler

 L.  54        28  LOAD_GLOBAL              signal
               30  LOAD_METHOD              signal
               32  LOAD_GLOBAL              signal
               34  LOAD_ATTR                SIGINT
               36  LOAD_GLOBAL              _interrupt_handler
               38  CALL_METHOD_2         2  ''
               40  POP_TOP          
             42_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1


def removeHandler--- This code section failed: ---

 L.  58         0  LOAD_DEREF               'method'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    32  'to 32'

 L.  59         8  LOAD_GLOBAL              wraps
               10  LOAD_DEREF               'method'
               12  CALL_FUNCTION_1       1  ''

 L.  60        14  LOAD_CLOSURE             'method'
               16  BUILD_TUPLE_1         1 
               18  LOAD_CODE                <code_object inner>
               20  LOAD_STR                 'removeHandler.<locals>.inner'
               22  MAKE_FUNCTION_8          'closure'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'inner'

 L.  67        28  LOAD_FAST                'inner'
               30  RETURN_VALUE     
             32_0  COME_FROM             6  '6'

 L.  70        32  LOAD_GLOBAL              _interrupt_handler
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'

 L.  71        40  LOAD_GLOBAL              signal
               42  LOAD_METHOD              signal
               44  LOAD_GLOBAL              signal
               46  LOAD_ATTR                SIGINT
               48  LOAD_GLOBAL              _interrupt_handler
               50  LOAD_ATTR                original_handler
               52  CALL_METHOD_2         2  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

Parse error at or near `None' instruction at offset -1


# global _interrupt_handler ## Warning: Unused global