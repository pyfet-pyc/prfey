# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\exceptions.py
"""asyncio exceptions."""
__all__ = ('CancelledError', 'InvalidStateError', 'TimeoutError', 'IncompleteReadError',
           'LimitOverrunError', 'SendfileNotAvailableError')

class CancelledError(BaseException):
    __doc__ = 'The Future or Task was cancelled.'


class TimeoutError(Exception):
    __doc__ = 'The operation exceeded the given deadline.'


class InvalidStateError(Exception):
    __doc__ = 'The operation is not allowed in this state.'


class SendfileNotAvailableError(RuntimeError):
    __doc__ = 'Sendfile syscall is not available.\n\n    Raised if OS does not support sendfile syscall for given socket or\n    file type.\n    '


class IncompleteReadError(EOFError):
    __doc__ = '\n    Incomplete read error. Attributes:\n\n    - partial: read bytes string before the end of stream was reached\n    - expected: total number of expected bytes (or None if unknown)\n    '

    def __init__--- This code section failed: ---

 L.  37         0  LOAD_FAST                'expected'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'
                8  LOAD_STR                 'undefined'
               10  JUMP_FORWARD         18  'to 18'
             12_0  COME_FROM             6  '6'
               12  LOAD_GLOBAL              repr
               14  LOAD_FAST                'expected'
               16  CALL_FUNCTION_1       1  ''
             18_0  COME_FROM            10  '10'
               18  STORE_FAST               'r_expected'

 L.  38        20  LOAD_GLOBAL              super
               22  CALL_FUNCTION_0       0  ''
               24  LOAD_METHOD              __init__
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'partial'
               30  CALL_FUNCTION_1       1  ''
               32  FORMAT_VALUE          0  ''
               34  LOAD_STR                 ' bytes read on a total of '

 L.  39        36  LOAD_FAST                'r_expected'

 L.  38        38  FORMAT_VALUE          0  ''
               40  LOAD_STR                 ' expected bytes'
               42  BUILD_STRING_4        4 
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L.  40        48  LOAD_FAST                'partial'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               partial

 L.  41        54  LOAD_FAST                'expected'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               expected

Parse error at or near `None' instruction at offset -1

    def __reduce__(self):
        return (
         type(self), (self.partial, self.expected))


class LimitOverrunError(Exception):
    __doc__ = 'Reached the buffer limit while looking for a separator.\n\n    Attributes:\n    - consumed: total number of to be consumed bytes.\n    '

    def __init__(self, message, consumed):
        super.__init__message
        self.consumed = consumed

    def __reduce__(self):
        return (
         type(self), (self.args[0], self.consumed))