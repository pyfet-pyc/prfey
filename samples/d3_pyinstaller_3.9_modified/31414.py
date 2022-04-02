# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\windows_events.py
"""Selector and proactor event loops for Windows."""
import _overlapped, _winapi, errno, math, msvcrt, socket, struct, time, weakref
from . import events
from . import base_subprocess
from . import futures
from . import exceptions
from . import proactor_events
from . import selector_events
from . import tasks
from . import windows_utils
from .log import logger
__all__ = ('SelectorEventLoop', 'ProactorEventLoop', 'IocpProactor', 'DefaultEventLoopPolicy',
           'WindowsSelectorEventLoopPolicy', 'WindowsProactorEventLoopPolicy')
NULL = 0
INFINITE = 4294967295
ERROR_CONNECTION_REFUSED = 1225
ERROR_CONNECTION_ABORTED = 1236
CONNECT_PIPE_INIT_DELAY = 0.001
CONNECT_PIPE_MAX_DELAY = 0.1

class _OverlappedFuture(futures.Future):
    __doc__ = 'Subclass of Future which represents an overlapped operation.\n\n    Cancelling it will immediately cancel the overlapped operation.\n    '

    def __init__(self, ov, *, loop=None):
        super().__init__(loop=loop)
        if self._source_traceback:
            del self._source_traceback[-1]
        self._ov = ov

    def _repr_info--- This code section failed: ---

 L.  56         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              _repr_info
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'info'

 L.  57        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _ov
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    68  'to 68'

 L.  58        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _ov
               24  LOAD_ATTR                pending
               26  POP_JUMP_IF_FALSE    32  'to 32'
               28  LOAD_STR                 'pending'
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            26  '26'
               32  LOAD_STR                 'completed'
             34_0  COME_FROM            30  '30'
               34  STORE_FAST               'state'

 L.  59        36  LOAD_FAST                'info'
               38  LOAD_METHOD              insert
               40  LOAD_CONST               1
               42  LOAD_STR                 'overlapped=<'
               44  LOAD_FAST                'state'
               46  FORMAT_VALUE          0  ''
               48  LOAD_STR                 ', '
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _ov
               54  LOAD_ATTR                address
               56  LOAD_STR                 '#x'
               58  FORMAT_VALUE_ATTR     4  ''
               60  LOAD_STR                 '>'
               62  BUILD_STRING_5        5 
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          
             68_0  COME_FROM            18  '18'

 L.  60        68  LOAD_FAST                'info'
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def _cancel_overlapped--- This code section failed: ---

 L.  63         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ov
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  64        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  65        14  SETUP_FINALLY        30  'to 30'

 L.  66        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _ov
               20  LOAD_METHOD              cancel
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
               26  POP_BLOCK        
               28  JUMP_FORWARD        106  'to 106'
             30_0  COME_FROM_FINALLY    14  '14'

 L.  67        30  DUP_TOP          
               32  LOAD_GLOBAL              OSError
               34  <121>               104  ''
               36  POP_TOP          
               38  STORE_FAST               'exc'
               40  POP_TOP          
               42  SETUP_FINALLY        96  'to 96'

 L.  69        44  LOAD_STR                 'Cancelling an overlapped future failed'

 L.  70        46  LOAD_FAST                'exc'

 L.  71        48  LOAD_FAST                'self'

 L.  68        50  LOAD_CONST               ('message', 'exception', 'future')
               52  BUILD_CONST_KEY_MAP_3     3 
               54  STORE_FAST               'context'

 L.  73        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _source_traceback
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L.  74        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _source_traceback
               66  LOAD_FAST                'context'
               68  LOAD_STR                 'source_traceback'
               70  STORE_SUBSCR     
             72_0  COME_FROM            60  '60'

 L.  75        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _loop
               76  LOAD_METHOD              call_exception_handler
               78  LOAD_FAST                'context'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  POP_BLOCK        
               86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  STORE_FAST               'exc'
               92  DELETE_FAST              'exc'
               94  JUMP_FORWARD        106  'to 106'
             96_0  COME_FROM_FINALLY    42  '42'
               96  LOAD_CONST               None
               98  STORE_FAST               'exc'
              100  DELETE_FAST              'exc'
              102  <48>             
              104  <48>             
            106_0  COME_FROM            94  '94'
            106_1  COME_FROM            28  '28'

 L.  76       106  LOAD_CONST               None
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _ov

Parse error at or near `None' instruction at offset -1

    def cancel(self, msg=None):
        self._cancel_overlapped
        return super().cancel(msg=msg)

    def set_exception(self, exception):
        super().set_exceptionexception
        self._cancel_overlapped

    def set_result(self, result):
        super().set_resultresult
        self._ov = None


class _BaseWaitHandleFuture(futures.Future):
    __doc__ = 'Subclass of Future which represents a wait handle.'

    def __init__(self, ov, handle, wait_handle, *, loop=None):
        super().__init__(loop=loop)
        if self._source_traceback:
            del self._source_traceback[-1]
        self._ov = ov
        self._handle = handle
        self._wait_handle = wait_handle
        self._registered = True

    def _poll(self):
        return _winapi.WaitForSingleObjectself._handle0 == _winapi.WAIT_OBJECT_0

    def _repr_info--- This code section failed: ---

 L. 114         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              _repr_info
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'info'

 L. 115        10  LOAD_FAST                'info'
               12  LOAD_METHOD              append
               14  LOAD_STR                 'handle='
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _handle
               20  LOAD_STR                 '#x'
               22  FORMAT_VALUE_ATTR     4  ''
               24  BUILD_STRING_2        2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 116        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _handle
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    66  'to 66'

 L. 117        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _poll
               44  CALL_METHOD_0         0  ''
               46  POP_JUMP_IF_FALSE    52  'to 52'
               48  LOAD_STR                 'signaled'
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            46  '46'
               52  LOAD_STR                 'waiting'
             54_0  COME_FROM            50  '50'
               54  STORE_FAST               'state'

 L. 118        56  LOAD_FAST                'info'
               58  LOAD_METHOD              append
               60  LOAD_FAST                'state'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
             66_0  COME_FROM            38  '38'

 L. 119        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _wait_handle
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_FALSE    96  'to 96'

 L. 120        76  LOAD_FAST                'info'
               78  LOAD_METHOD              append
               80  LOAD_STR                 'wait_handle='
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                _wait_handle
               86  LOAD_STR                 '#x'
               88  FORMAT_VALUE_ATTR     4  ''
               90  BUILD_STRING_2        2 
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
             96_0  COME_FROM            74  '74'

 L. 121        96  LOAD_FAST                'info'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 36

    def _unregister_wait_cb(self, fut):
        self._ov = None

    def _unregister_wait--- This code section failed: ---

 L. 129         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _registered
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 130         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 131        10  LOAD_CONST               False
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _registered

 L. 133        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _wait_handle
               20  STORE_FAST               'wait_handle'

 L. 134        22  LOAD_CONST               None
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _wait_handle

 L. 135        28  SETUP_FINALLY        44  'to 44'

 L. 136        30  LOAD_GLOBAL              _overlapped
               32  LOAD_METHOD              UnregisterWait
               34  LOAD_FAST                'wait_handle'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD        146  'to 146'
             44_0  COME_FROM_FINALLY    28  '28'

 L. 137        44  DUP_TOP          
               46  LOAD_GLOBAL              OSError
               48  <121>               144  ''
               50  POP_TOP          
               52  STORE_FAST               'exc'
               54  POP_TOP          
               56  SETUP_FINALLY       136  'to 136'

 L. 138        58  LOAD_FAST                'exc'
               60  LOAD_ATTR                winerror
               62  LOAD_GLOBAL              _overlapped
               64  LOAD_ATTR                ERROR_IO_PENDING
               66  COMPARE_OP               !=
               68  POP_JUMP_IF_FALSE   124  'to 124'

 L. 140        70  LOAD_STR                 'Failed to unregister the wait handle'

 L. 141        72  LOAD_FAST                'exc'

 L. 142        74  LOAD_FAST                'self'

 L. 139        76  LOAD_CONST               ('message', 'exception', 'future')
               78  BUILD_CONST_KEY_MAP_3     3 
               80  STORE_FAST               'context'

 L. 144        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _source_traceback
               86  POP_JUMP_IF_FALSE    98  'to 98'

 L. 145        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _source_traceback
               92  LOAD_FAST                'context'
               94  LOAD_STR                 'source_traceback'
               96  STORE_SUBSCR     
             98_0  COME_FROM            86  '86'

 L. 146        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _loop
              102  LOAD_METHOD              call_exception_handler
              104  LOAD_FAST                'context'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 147       110  POP_BLOCK        
              112  POP_EXCEPT       
              114  LOAD_CONST               None
              116  STORE_FAST               'exc'
              118  DELETE_FAST              'exc'
              120  LOAD_CONST               None
              122  RETURN_VALUE     
            124_0  COME_FROM            68  '68'
              124  POP_BLOCK        
              126  POP_EXCEPT       
              128  LOAD_CONST               None
              130  STORE_FAST               'exc'
              132  DELETE_FAST              'exc'
              134  JUMP_FORWARD        146  'to 146'
            136_0  COME_FROM_FINALLY    56  '56'
              136  LOAD_CONST               None
              138  STORE_FAST               'exc'
              140  DELETE_FAST              'exc'
              142  <48>             
              144  <48>             
            146_0  COME_FROM           134  '134'
            146_1  COME_FROM            42  '42'

 L. 150       146  LOAD_FAST                'self'
              148  LOAD_METHOD              _unregister_wait_cb
              150  LOAD_CONST               None
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          

Parse error at or near `<121>' instruction at offset 48

    def cancel(self, msg=None):
        self._unregister_wait
        return super().cancel(msg=msg)

    def set_exception(self, exception):
        self._unregister_wait
        super().set_exceptionexception

    def set_result(self, result):
        self._unregister_wait
        super().set_resultresult


class _WaitCancelFuture(_BaseWaitHandleFuture):
    __doc__ = 'Subclass of Future which represents a wait for the cancellation of a\n    _WaitHandleFuture using an event.\n    '

    def __init__(self, ov, event, wait_handle, *, loop=None):
        super().__init__(ov, event, wait_handle, loop=loop)
        self._done_callback = None

    def cancel(self):
        raise RuntimeError('_WaitCancelFuture must not be cancelled')

    def set_result--- This code section failed: ---

 L. 179         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              set_result
                6  LOAD_FAST                'result'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 180        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _done_callback
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 181        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _done_callback
               26  LOAD_FAST                'self'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          
             32_0  COME_FROM            20  '20'

Parse error at or near `<117>' instruction at offset 18

    def set_exception--- This code section failed: ---

 L. 184         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              set_exception
                6  LOAD_FAST                'exception'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 185        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _done_callback
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 186        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _done_callback
               26  LOAD_FAST                'self'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          
             32_0  COME_FROM            20  '20'

Parse error at or near `<117>' instruction at offset 18


class _WaitHandleFuture(_BaseWaitHandleFuture):

    def __init__(self, ov, handle, wait_handle, proactor, *, loop=None):
        super().__init__(ov, handle, wait_handle, loop=loop)
        self._proactor = proactor
        self._unregister_proactor = True
        self._event = _overlapped.CreateEvent(None, True, False, None)
        self._event_fut = None

    def _unregister_wait_cb--- This code section failed: ---

 L. 198         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _event
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    34  'to 34'

 L. 199        10  LOAD_GLOBAL              _winapi
               12  LOAD_METHOD              CloseHandle
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _event
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 200        22  LOAD_CONST               None
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _event

 L. 201        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _event_fut
             34_0  COME_FROM             8  '8'

 L. 210        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _proactor
               38  LOAD_METHOD              _unregister
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _ov
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 211        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _proactor

 L. 213        54  LOAD_GLOBAL              super
               56  CALL_FUNCTION_0       0  ''
               58  LOAD_METHOD              _unregister_wait_cb
               60  LOAD_FAST                'fut'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _unregister_wait--- This code section failed: ---

 L. 216         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _registered
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 217         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 218        10  LOAD_CONST               False
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _registered

 L. 220        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _wait_handle
               20  STORE_FAST               'wait_handle'

 L. 221        22  LOAD_CONST               None
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _wait_handle

 L. 222        28  SETUP_FINALLY        48  'to 48'

 L. 223        30  LOAD_GLOBAL              _overlapped
               32  LOAD_METHOD              UnregisterWaitEx
               34  LOAD_FAST                'wait_handle'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _event
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          
               44  POP_BLOCK        
               46  JUMP_FORWARD        150  'to 150'
             48_0  COME_FROM_FINALLY    28  '28'

 L. 224        48  DUP_TOP          
               50  LOAD_GLOBAL              OSError
               52  <121>               148  ''
               54  POP_TOP          
               56  STORE_FAST               'exc'
               58  POP_TOP          
               60  SETUP_FINALLY       140  'to 140'

 L. 225        62  LOAD_FAST                'exc'
               64  LOAD_ATTR                winerror
               66  LOAD_GLOBAL              _overlapped
               68  LOAD_ATTR                ERROR_IO_PENDING
               70  COMPARE_OP               !=
               72  POP_JUMP_IF_FALSE   128  'to 128'

 L. 227        74  LOAD_STR                 'Failed to unregister the wait handle'

 L. 228        76  LOAD_FAST                'exc'

 L. 229        78  LOAD_FAST                'self'

 L. 226        80  LOAD_CONST               ('message', 'exception', 'future')
               82  BUILD_CONST_KEY_MAP_3     3 
               84  STORE_FAST               'context'

 L. 231        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _source_traceback
               90  POP_JUMP_IF_FALSE   102  'to 102'

 L. 232        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _source_traceback
               96  LOAD_FAST                'context'
               98  LOAD_STR                 'source_traceback'
              100  STORE_SUBSCR     
            102_0  COME_FROM            90  '90'

 L. 233       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _loop
              106  LOAD_METHOD              call_exception_handler
              108  LOAD_FAST                'context'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 234       114  POP_BLOCK        
              116  POP_EXCEPT       
              118  LOAD_CONST               None
              120  STORE_FAST               'exc'
              122  DELETE_FAST              'exc'
              124  LOAD_CONST               None
              126  RETURN_VALUE     
            128_0  COME_FROM            72  '72'
              128  POP_BLOCK        
              130  POP_EXCEPT       
              132  LOAD_CONST               None
              134  STORE_FAST               'exc'
              136  DELETE_FAST              'exc'
              138  JUMP_FORWARD        150  'to 150'
            140_0  COME_FROM_FINALLY    60  '60'
              140  LOAD_CONST               None
              142  STORE_FAST               'exc'
              144  DELETE_FAST              'exc'
              146  <48>             
              148  <48>             
            150_0  COME_FROM           138  '138'
            150_1  COME_FROM            46  '46'

 L. 237       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _proactor
              154  LOAD_METHOD              _wait_cancel
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _event

 L. 238       160  LOAD_FAST                'self'
              162  LOAD_ATTR                _unregister_wait_cb

 L. 237       164  CALL_METHOD_2         2  ''
              166  LOAD_FAST                'self'
              168  STORE_ATTR               _event_fut

Parse error at or near `<121>' instruction at offset 52


class PipeServer(object):
    __doc__ = 'Class representing a pipe server.\n\n    This is much like a bound, listening socket.\n    '

    def __init__(self, address):
        self._address = address
        self._free_instances = weakref.WeakSet
        self._pipe = None
        self._accept_pipe_future = None
        self._pipe = self._server_pipe_handleTrue

    def _get_unconnected_pipe(self):
        tmp, self._pipe = self._pipe, self._server_pipe_handleFalse
        return tmp

    def _server_pipe_handle(self, first):
        if self.closed:
            return
        flags = _winapi.PIPE_ACCESS_DUPLEX | _winapi.FILE_FLAG_OVERLAPPED
        if first:
            flags |= _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE
        h = _winapi.CreateNamedPipe(self._address, flags, _winapi.PIPE_TYPE_MESSAGE | _winapi.PIPE_READMODE_MESSAGE | _winapi.PIPE_WAIT, _winapi.PIPE_UNLIMITED_INSTANCES, windows_utils.BUFSIZE, windows_utils.BUFSIZE, _winapi.NMPWAIT_WAIT_FOREVER, _winapi.NULL)
        pipe = windows_utils.PipeHandleh
        self._free_instances.addpipe
        return pipe

    def closed--- This code section failed: ---

 L. 283         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _address
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def close--- This code section failed: ---

 L. 286         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _accept_pipe_future
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 287        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _accept_pipe_future
               14  LOAD_METHOD              cancel
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 288        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _accept_pipe_future
             26_0  COME_FROM             8  '8'

 L. 290        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _address
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    78  'to 78'

 L. 291        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _free_instances
               40  GET_ITER         
             42_0  COME_FROM            54  '54'
               42  FOR_ITER             56  'to 56'
               44  STORE_FAST               'pipe'

 L. 292        46  LOAD_FAST                'pipe'
               48  LOAD_METHOD              close
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          
               54  JUMP_BACK            42  'to 42'
             56_0  COME_FROM            42  '42'

 L. 293        56  LOAD_CONST               None
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _pipe

 L. 294        62  LOAD_CONST               None
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _address

 L. 295        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _free_instances
               72  LOAD_METHOD              clear
               74  CALL_METHOD_0         0  ''
               76  POP_TOP          
             78_0  COME_FROM            34  '34'

Parse error at or near `None' instruction at offset -1

    __del__ = close


class _WindowsSelectorEventLoop(selector_events.BaseSelectorEventLoop):
    __doc__ = 'Windows version of selector event loop.'


class ProactorEventLoop(proactor_events.BaseProactorEventLoop):
    __doc__ = 'Windows version of proactor event loop using IOCP.'

    def __init__--- This code section failed: ---

 L. 308         0  LOAD_FAST                'proactor'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 309         8  LOAD_GLOBAL              IocpProactor
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'proactor'
             14_0  COME_FROM             6  '6'

 L. 310        14  LOAD_GLOBAL              super
               16  CALL_FUNCTION_0       0  ''
               18  LOAD_METHOD              __init__
               20  LOAD_FAST                'proactor'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def run_forever--- This code section failed: ---

 L. 313         0  SETUP_FINALLY        96  'to 96'

 L. 314         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _self_reading_future
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 315        16  LOAD_FAST                'self'
               18  LOAD_METHOD              call_soon
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _loop_self_reading
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L. 316        28  LOAD_GLOBAL              super
               30  CALL_FUNCTION_0       0  ''
               32  LOAD_METHOD              run_forever
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          
               38  POP_BLOCK        

 L. 318        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _self_reading_future
               44  LOAD_CONST               None
               46  <117>                 1  ''
               48  POP_JUMP_IF_FALSE   152  'to 152'

 L. 319        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _self_reading_future
               54  LOAD_ATTR                _ov
               56  STORE_FAST               'ov'

 L. 320        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _self_reading_future
               62  LOAD_METHOD              cancel
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          

 L. 327        68  LOAD_FAST                'ov'
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_FALSE    88  'to 88'

 L. 328        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _proactor
               80  LOAD_METHOD              _unregister
               82  LOAD_FAST                'ov'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
             88_0  COME_FROM            74  '74'

 L. 329        88  LOAD_CONST               None
               90  LOAD_FAST                'self'
               92  STORE_ATTR               _self_reading_future
               94  JUMP_FORWARD        152  'to 152'
             96_0  COME_FROM_FINALLY     0  '0'

 L. 318        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _self_reading_future
              100  LOAD_CONST               None
              102  <117>                 1  ''
              104  POP_JUMP_IF_FALSE   150  'to 150'

 L. 319       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _self_reading_future
              110  LOAD_ATTR                _ov
              112  STORE_FAST               'ov'

 L. 320       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _self_reading_future
              118  LOAD_METHOD              cancel
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          

 L. 327       124  LOAD_FAST                'ov'
              126  LOAD_CONST               None
              128  <117>                 1  ''
              130  POP_JUMP_IF_FALSE   144  'to 144'

 L. 328       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _proactor
              136  LOAD_METHOD              _unregister
              138  LOAD_FAST                'ov'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           130  '130'

 L. 329       144  LOAD_CONST               None
              146  LOAD_FAST                'self'
              148  STORE_ATTR               _self_reading_future
            150_0  COME_FROM           104  '104'
              150  <48>             
            152_0  COME_FROM            94  '94'
            152_1  COME_FROM            48  '48'

Parse error at or near `<117>' instruction at offset 8

    async def create_pipe_connection(self, protocol_factory, address):
        f = self._proactor.connect_pipeaddress
        pipe = await f
        protocol = protocol_factory()
        trans = self._make_duplex_pipe_transport(pipe, protocol, extra={'addr': address})
        return (
         trans, protocol)

    async def start_serving_pipe(self, protocol_factory, address):
        server = PipeServer(address)

        def loop_accept_pipe--- This code section failed: ---

 L. 343         0  LOAD_CONST               None
                2  STORE_FAST               'pipe'

 L. 344         4  SETUP_FINALLY       116  'to 116'

 L. 345         6  LOAD_FAST                'f'
                8  POP_JUMP_IF_FALSE    78  'to 78'

 L. 346        10  LOAD_FAST                'f'
               12  LOAD_METHOD              result
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'pipe'

 L. 347        18  LOAD_DEREF               'server'
               20  LOAD_ATTR                _free_instances
               22  LOAD_METHOD              discard
               24  LOAD_FAST                'pipe'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 349        30  LOAD_DEREF               'server'
               32  LOAD_METHOD              closed
               34  CALL_METHOD_0         0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 352        38  LOAD_FAST                'pipe'
               40  LOAD_METHOD              close
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L. 353        46  POP_BLOCK        
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            36  '36'

 L. 355        52  LOAD_DEREF               'protocol_factory'
               54  CALL_FUNCTION_0       0  ''
               56  STORE_FAST               'protocol'

 L. 356        58  LOAD_DEREF               'self'
               60  LOAD_ATTR                _make_duplex_pipe_transport

 L. 357        62  LOAD_FAST                'pipe'
               64  LOAD_FAST                'protocol'
               66  LOAD_STR                 'addr'
               68  LOAD_DEREF               'address'
               70  BUILD_MAP_1           1 

 L. 356        72  LOAD_CONST               ('extra',)
               74  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               76  POP_TOP          
             78_0  COME_FROM             8  '8'

 L. 359        78  LOAD_DEREF               'server'
               80  LOAD_METHOD              _get_unconnected_pipe
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'pipe'

 L. 360        86  LOAD_FAST                'pipe'
               88  LOAD_CONST               None
               90  <117>                 0  ''
               92  POP_JUMP_IF_FALSE   100  'to 100'

 L. 361        94  POP_BLOCK        
               96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM            92  '92'

 L. 363       100  LOAD_DEREF               'self'
              102  LOAD_ATTR                _proactor
              104  LOAD_METHOD              accept_pipe
              106  LOAD_FAST                'pipe'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'f'
              112  POP_BLOCK        
              114  JUMP_FORWARD        248  'to 248'
            116_0  COME_FROM_FINALLY     4  '4'

 L. 364       116  DUP_TOP          
              118  LOAD_GLOBAL              OSError
              120  <121>               216  ''
              122  POP_TOP          
              124  STORE_FAST               'exc'
              126  POP_TOP          
              128  SETUP_FINALLY       208  'to 208'

 L. 365       130  LOAD_FAST                'pipe'
              132  POP_JUMP_IF_FALSE   174  'to 174'
              134  LOAD_FAST                'pipe'
              136  LOAD_METHOD              fileno
              138  CALL_METHOD_0         0  ''
              140  LOAD_CONST               -1
              142  COMPARE_OP               !=
              144  POP_JUMP_IF_FALSE   174  'to 174'

 L. 366       146  LOAD_DEREF               'self'
              148  LOAD_METHOD              call_exception_handler

 L. 367       150  LOAD_STR                 'Pipe accept failed'

 L. 368       152  LOAD_FAST                'exc'

 L. 369       154  LOAD_FAST                'pipe'

 L. 366       156  LOAD_CONST               ('message', 'exception', 'pipe')
              158  BUILD_CONST_KEY_MAP_3     3 
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          

 L. 371       164  LOAD_FAST                'pipe'
              166  LOAD_METHOD              close
              168  CALL_METHOD_0         0  ''
              170  POP_TOP          
              172  JUMP_FORWARD        196  'to 196'
            174_0  COME_FROM           144  '144'
            174_1  COME_FROM           132  '132'

 L. 372       174  LOAD_DEREF               'self'
              176  LOAD_ATTR                _debug
              178  POP_JUMP_IF_FALSE   196  'to 196'

 L. 373       180  LOAD_GLOBAL              logger
              182  LOAD_ATTR                warning
              184  LOAD_STR                 'Accept pipe failed on pipe %r'

 L. 374       186  LOAD_FAST                'pipe'
              188  LOAD_CONST               True

 L. 373       190  LOAD_CONST               ('exc_info',)
              192  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              194  POP_TOP          
            196_0  COME_FROM           178  '178'
            196_1  COME_FROM           172  '172'
              196  POP_BLOCK        
              198  POP_EXCEPT       
              200  LOAD_CONST               None
              202  STORE_FAST               'exc'
              204  DELETE_FAST              'exc'
              206  JUMP_FORWARD        264  'to 264'
            208_0  COME_FROM_FINALLY   128  '128'
              208  LOAD_CONST               None
              210  STORE_FAST               'exc'
              212  DELETE_FAST              'exc'
              214  <48>             

 L. 375       216  DUP_TOP          
              218  LOAD_GLOBAL              exceptions
              220  LOAD_ATTR                CancelledError
              222  <121>               246  ''
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 376       230  LOAD_FAST                'pipe'
              232  POP_JUMP_IF_FALSE   242  'to 242'

 L. 377       234  LOAD_FAST                'pipe'
              236  LOAD_METHOD              close
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          
            242_0  COME_FROM           232  '232'
              242  POP_EXCEPT       
              244  JUMP_FORWARD        264  'to 264'
              246  <48>             
            248_0  COME_FROM           114  '114'

 L. 379       248  LOAD_FAST                'f'
              250  LOAD_DEREF               'server'
              252  STORE_ATTR               _accept_pipe_future

 L. 380       254  LOAD_FAST                'f'
              256  LOAD_METHOD              add_done_callback
              258  LOAD_DEREF               'loop_accept_pipe'
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
            264_0  COME_FROM           244  '244'
            264_1  COME_FROM           206  '206'

Parse error at or near `LOAD_CONST' instruction at offset 48

        self.call_soonloop_accept_pipe
        return [
         server]

    async def _make_subprocess_transport--- This code section failed: ---

 L. 388         0  LOAD_FAST                'self'
                2  LOAD_METHOD              create_future
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'waiter'

 L. 389         8  LOAD_GLOBAL              _WindowsSubprocessTransport
               10  LOAD_FAST                'self'
               12  LOAD_FAST                'protocol'
               14  LOAD_FAST                'args'
               16  LOAD_FAST                'shell'

 L. 390        18  LOAD_FAST                'stdin'
               20  LOAD_FAST                'stdout'
               22  LOAD_FAST                'stderr'
               24  LOAD_FAST                'bufsize'

 L. 389        26  BUILD_TUPLE_8         8 

 L. 391        28  LOAD_FAST                'waiter'
               30  LOAD_FAST                'extra'

 L. 389        32  LOAD_CONST               ('waiter', 'extra')
               34  BUILD_CONST_KEY_MAP_2     2 

 L. 392        36  LOAD_FAST                'kwargs'

 L. 389        38  <164>                 1  ''
               40  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               42  STORE_FAST               'transp'

 L. 393        44  SETUP_FINALLY        60  'to 60'

 L. 394        46  LOAD_FAST                'waiter'
               48  GET_AWAITABLE    
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  POP_TOP          
               56  POP_BLOCK        
               58  JUMP_FORWARD        124  'to 124'
             60_0  COME_FROM_FINALLY    44  '44'

 L. 395        60  DUP_TOP          
               62  LOAD_GLOBAL              SystemExit
               64  LOAD_GLOBAL              KeyboardInterrupt
               66  BUILD_TUPLE_2         2 
               68  <121>                82  ''
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 396        76  RAISE_VARARGS_0       0  'reraise'
               78  POP_EXCEPT       
               80  JUMP_FORWARD        124  'to 124'

 L. 397        82  DUP_TOP          
               84  LOAD_GLOBAL              BaseException
               86  <121>               122  ''
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L. 398        94  LOAD_FAST                'transp'
               96  LOAD_METHOD              close
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          

 L. 399       102  LOAD_FAST                'transp'
              104  LOAD_METHOD              _wait
              106  CALL_METHOD_0         0  ''
              108  GET_AWAITABLE    
              110  LOAD_CONST               None
              112  YIELD_FROM       
              114  POP_TOP          

 L. 400       116  RAISE_VARARGS_0       0  'reraise'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
              122  <48>             
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            80  '80'
            124_2  COME_FROM            58  '58'

 L. 402       124  LOAD_FAST                'transp'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 38


class IocpProactor:
    __doc__ = 'Proactor implementation using IOCP.'

    def __init__(self, concurrency=4294967295):
        self._loop = None
        self._results = []
        self._iocp = _overlapped.CreateIoCompletionPort(_overlapped.INVALID_HANDLE_VALUE, NULL, 0, concurrency)
        self._cache = {}
        self._registered = weakref.WeakSet
        self._unregistered = []
        self._stopped_serving = weakref.WeakSet

    def _check_closed--- This code section failed: ---

 L. 419         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _iocp
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 420        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'IocpProactor is closed'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def __repr__--- This code section failed: ---

 L. 423         0  LOAD_STR                 'overlapped#=%s'
                2  LOAD_GLOBAL              len
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _cache
                8  CALL_FUNCTION_1       1  ''
               10  BINARY_MODULO    

 L. 424        12  LOAD_STR                 'result#=%s'
               14  LOAD_GLOBAL              len
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _results
               20  CALL_FUNCTION_1       1  ''
               22  BINARY_MODULO    

 L. 423        24  BUILD_LIST_2          2 
               26  STORE_FAST               'info'

 L. 425        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _iocp
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L. 426        38  LOAD_FAST                'info'
               40  LOAD_METHOD              append
               42  LOAD_STR                 'closed'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            36  '36'

 L. 427        48  LOAD_STR                 '<%s %s>'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                __class__
               54  LOAD_ATTR                __name__
               56  LOAD_STR                 ' '
               58  LOAD_METHOD              join
               60  LOAD_FAST                'info'
               62  CALL_METHOD_1         1  ''
               64  BUILD_TUPLE_2         2 
               66  BINARY_MODULO    
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 34

    def set_loop(self, loop):
        self._loop = loop

    def select(self, timeout=None):
        if not self._results:
            self._polltimeout
        tmp = self._results
        self._results = []
        return tmp

    def _result(self, value):
        fut = self._loop.create_future
        fut.set_resultvalue
        return fut

    def recv--- This code section failed: ---

 L. 445         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _register_with_iocp
                4  LOAD_FAST                'conn'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 446        10  LOAD_GLOBAL              _overlapped
               12  LOAD_METHOD              Overlapped
               14  LOAD_GLOBAL              NULL
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'ov'

 L. 447        20  SETUP_FINALLY        74  'to 74'

 L. 448        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'conn'
               26  LOAD_GLOBAL              socket
               28  LOAD_ATTR                socket
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    54  'to 54'

 L. 449        34  LOAD_FAST                'ov'
               36  LOAD_METHOD              WSARecv
               38  LOAD_FAST                'conn'
               40  LOAD_METHOD              fileno
               42  CALL_METHOD_0         0  ''
               44  LOAD_FAST                'nbytes'
               46  LOAD_FAST                'flags'
               48  CALL_METHOD_3         3  ''
               50  POP_TOP          
               52  JUMP_FORWARD         70  'to 70'
             54_0  COME_FROM            32  '32'

 L. 451        54  LOAD_FAST                'ov'
               56  LOAD_METHOD              ReadFile
               58  LOAD_FAST                'conn'
               60  LOAD_METHOD              fileno
               62  CALL_METHOD_0         0  ''
               64  LOAD_FAST                'nbytes'
               66  CALL_METHOD_2         2  ''
               68  POP_TOP          
             70_0  COME_FROM            52  '52'
               70  POP_BLOCK        
               72  JUMP_FORWARD        102  'to 102'
             74_0  COME_FROM_FINALLY    20  '20'

 L. 452        74  DUP_TOP          
               76  LOAD_GLOBAL              BrokenPipeError
               78  <121>               100  ''
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 453        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _result
               90  LOAD_CONST               b''
               92  CALL_METHOD_1         1  ''
               94  ROT_FOUR         
               96  POP_EXCEPT       
               98  RETURN_VALUE     
              100  <48>             
            102_0  COME_FROM            72  '72'

 L. 455       102  LOAD_CODE                <code_object finish_recv>
              104  LOAD_STR                 'IocpProactor.recv.<locals>.finish_recv'
              106  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              108  STORE_FAST               'finish_recv'

 L. 465       110  LOAD_FAST                'self'
              112  LOAD_METHOD              _register
              114  LOAD_FAST                'ov'
              116  LOAD_FAST                'conn'
              118  LOAD_FAST                'finish_recv'
              120  CALL_METHOD_3         3  ''
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 78

    def recv_into--- This code section failed: ---

 L. 468         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _register_with_iocp
                4  LOAD_FAST                'conn'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 469        10  LOAD_GLOBAL              _overlapped
               12  LOAD_METHOD              Overlapped
               14  LOAD_GLOBAL              NULL
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'ov'

 L. 470        20  SETUP_FINALLY        74  'to 74'

 L. 471        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'conn'
               26  LOAD_GLOBAL              socket
               28  LOAD_ATTR                socket
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    54  'to 54'

 L. 472        34  LOAD_FAST                'ov'
               36  LOAD_METHOD              WSARecvInto
               38  LOAD_FAST                'conn'
               40  LOAD_METHOD              fileno
               42  CALL_METHOD_0         0  ''
               44  LOAD_FAST                'buf'
               46  LOAD_FAST                'flags'
               48  CALL_METHOD_3         3  ''
               50  POP_TOP          
               52  JUMP_FORWARD         70  'to 70'
             54_0  COME_FROM            32  '32'

 L. 474        54  LOAD_FAST                'ov'
               56  LOAD_METHOD              ReadFileInto
               58  LOAD_FAST                'conn'
               60  LOAD_METHOD              fileno
               62  CALL_METHOD_0         0  ''
               64  LOAD_FAST                'buf'
               66  CALL_METHOD_2         2  ''
               68  POP_TOP          
             70_0  COME_FROM            52  '52'
               70  POP_BLOCK        
               72  JUMP_FORWARD        102  'to 102'
             74_0  COME_FROM_FINALLY    20  '20'

 L. 475        74  DUP_TOP          
               76  LOAD_GLOBAL              BrokenPipeError
               78  <121>               100  ''
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 476        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _result
               90  LOAD_CONST               0
               92  CALL_METHOD_1         1  ''
               94  ROT_FOUR         
               96  POP_EXCEPT       
               98  RETURN_VALUE     
              100  <48>             
            102_0  COME_FROM            72  '72'

 L. 478       102  LOAD_CODE                <code_object finish_recv>
              104  LOAD_STR                 'IocpProactor.recv_into.<locals>.finish_recv'
              106  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              108  STORE_FAST               'finish_recv'

 L. 488       110  LOAD_FAST                'self'
              112  LOAD_METHOD              _register
              114  LOAD_FAST                'ov'
              116  LOAD_FAST                'conn'
              118  LOAD_FAST                'finish_recv'
              120  CALL_METHOD_3         3  ''
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 78

    def recvfrom--- This code section failed: ---

 L. 491         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _register_with_iocp
                4  LOAD_FAST                'conn'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 492        10  LOAD_GLOBAL              _overlapped
               12  LOAD_METHOD              Overlapped
               14  LOAD_GLOBAL              NULL
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'ov'

 L. 493        20  SETUP_FINALLY        44  'to 44'

 L. 494        22  LOAD_FAST                'ov'
               24  LOAD_METHOD              WSARecvFrom
               26  LOAD_FAST                'conn'
               28  LOAD_METHOD              fileno
               30  CALL_METHOD_0         0  ''
               32  LOAD_FAST                'nbytes'
               34  LOAD_FAST                'flags'
               36  CALL_METHOD_3         3  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD         72  'to 72'
             44_0  COME_FROM_FINALLY    20  '20'

 L. 495        44  DUP_TOP          
               46  LOAD_GLOBAL              BrokenPipeError
               48  <121>                70  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 496        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _result
               60  LOAD_CONST               (b'', None)
               62  CALL_METHOD_1         1  ''
               64  ROT_FOUR         
               66  POP_EXCEPT       
               68  RETURN_VALUE     
               70  <48>             
             72_0  COME_FROM            42  '42'

 L. 498        72  LOAD_CODE                <code_object finish_recv>
               74  LOAD_STR                 'IocpProactor.recvfrom.<locals>.finish_recv'
               76  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               78  STORE_FAST               'finish_recv'

 L. 508        80  LOAD_FAST                'self'
               82  LOAD_METHOD              _register
               84  LOAD_FAST                'ov'
               86  LOAD_FAST                'conn'
               88  LOAD_FAST                'finish_recv'
               90  CALL_METHOD_3         3  ''
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 48

    def sendto(self, conn, buf, flags=0, addr=None):
        self._register_with_iocpconn
        ov = _overlapped.OverlappedNULL
        ov.WSASendTo(conn.fileno, buf, flags, addr)

        def finish_send--- This code section failed: ---

 L. 517         0  SETUP_FINALLY        12  'to 12'

 L. 518         2  LOAD_FAST                'ov'
                4  LOAD_METHOD              getresult
                6  CALL_METHOD_0         0  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 519        12  DUP_TOP          
               14  LOAD_GLOBAL              OSError
               16  <121>                78  ''
               18  POP_TOP          
               20  STORE_FAST               'exc'
               22  POP_TOP          
               24  SETUP_FINALLY        70  'to 70'

 L. 520        26  LOAD_FAST                'exc'
               28  LOAD_ATTR                winerror
               30  LOAD_GLOBAL              _overlapped
               32  LOAD_ATTR                ERROR_NETNAME_DELETED

 L. 521        34  LOAD_GLOBAL              _overlapped
               36  LOAD_ATTR                ERROR_OPERATION_ABORTED

 L. 520        38  BUILD_TUPLE_2         2 
               40  <118>                 0  ''
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L. 522        44  LOAD_GLOBAL              ConnectionResetError
               46  LOAD_FAST                'exc'
               48  LOAD_ATTR                args
               50  CALL_FUNCTION_EX      0  'positional arguments only'
               52  RAISE_VARARGS_1       1  'exception instance'
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            42  '42'

 L. 524        56  RAISE_VARARGS_0       0  'reraise'
             58_0  COME_FROM            54  '54'
               58  POP_BLOCK        
               60  POP_EXCEPT       
               62  LOAD_CONST               None
               64  STORE_FAST               'exc'
               66  DELETE_FAST              'exc'
               68  JUMP_FORWARD         80  'to 80'
             70_0  COME_FROM_FINALLY    24  '24'
               70  LOAD_CONST               None
               72  STORE_FAST               'exc'
               74  DELETE_FAST              'exc'
               76  <48>             
               78  <48>             
             80_0  COME_FROM            68  '68'

Parse error at or near `<121>' instruction at offset 16

        return self._registerovconnfinish_send

    def send(self, conn, buf, flags=0):
        self._register_with_iocpconn
        ov = _overlapped.OverlappedNULL
        if isinstance(conn, socket.socket):
            ov.WSASendconn.filenobufflags
        else:
            ov.WriteFileconn.filenobuf

        def finish_send--- This code section failed: ---

 L. 537         0  SETUP_FINALLY        12  'to 12'

 L. 538         2  LOAD_FAST                'ov'
                4  LOAD_METHOD              getresult
                6  CALL_METHOD_0         0  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 539        12  DUP_TOP          
               14  LOAD_GLOBAL              OSError
               16  <121>                78  ''
               18  POP_TOP          
               20  STORE_FAST               'exc'
               22  POP_TOP          
               24  SETUP_FINALLY        70  'to 70'

 L. 540        26  LOAD_FAST                'exc'
               28  LOAD_ATTR                winerror
               30  LOAD_GLOBAL              _overlapped
               32  LOAD_ATTR                ERROR_NETNAME_DELETED

 L. 541        34  LOAD_GLOBAL              _overlapped
               36  LOAD_ATTR                ERROR_OPERATION_ABORTED

 L. 540        38  BUILD_TUPLE_2         2 
               40  <118>                 0  ''
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L. 542        44  LOAD_GLOBAL              ConnectionResetError
               46  LOAD_FAST                'exc'
               48  LOAD_ATTR                args
               50  CALL_FUNCTION_EX      0  'positional arguments only'
               52  RAISE_VARARGS_1       1  'exception instance'
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            42  '42'

 L. 544        56  RAISE_VARARGS_0       0  'reraise'
             58_0  COME_FROM            54  '54'
               58  POP_BLOCK        
               60  POP_EXCEPT       
               62  LOAD_CONST               None
               64  STORE_FAST               'exc'
               66  DELETE_FAST              'exc'
               68  JUMP_FORWARD         80  'to 80'
             70_0  COME_FROM_FINALLY    24  '24'
               70  LOAD_CONST               None
               72  STORE_FAST               'exc'
               74  DELETE_FAST              'exc'
               76  <48>             
               78  <48>             
             80_0  COME_FROM            68  '68'

Parse error at or near `<121>' instruction at offset 16

        return self._registerovconnfinish_send

    def accept(self, listener):
        self._register_with_iocplistener
        conn = self._get_accept_socketlistener.family
        ov = _overlapped.OverlappedNULL
        ov.AcceptExlistener.filenoconn.fileno

        def finish_accept(trans, key, ov):
            ov.getresult
            buf = struct.pack'@P'listener.fileno
            conn.setsockoptsocket.SOL_SOCKET_overlapped.SO_UPDATE_ACCEPT_CONTEXTbuf
            conn.settimeoutlistener.gettimeout
            return (
             conn, conn.getpeername)

        async def accept_coro--- This code section failed: ---

 L. 565         0  SETUP_FINALLY        16  'to 16'

 L. 566         2  LOAD_FAST                'future'
                4  GET_AWAITABLE    
                6  LOAD_CONST               None
                8  YIELD_FROM       
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         46  'to 46'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 567        16  DUP_TOP          
               18  LOAD_GLOBAL              exceptions
               20  LOAD_ATTR                CancelledError
               22  <121>                44  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 568        30  LOAD_FAST                'conn'
               32  LOAD_METHOD              close
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          

 L. 569        38  RAISE_VARARGS_0       0  'reraise'
               40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
               44  <48>             
             46_0  COME_FROM            42  '42'
             46_1  COME_FROM            14  '14'

Parse error at or near `<121>' instruction at offset 22

        future = self._registerovlistenerfinish_accept
        coro = accept_coro(future, conn)
        tasks.ensure_future(coro, loop=(self._loop))
        return future

    def connect--- This code section failed: ---

 L. 577         0  LOAD_DEREF               'conn'
                2  LOAD_ATTR                type
                4  LOAD_GLOBAL              socket
                6  LOAD_ATTR                SOCK_DGRAM
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    52  'to 52'

 L. 580        12  LOAD_GLOBAL              _overlapped
               14  LOAD_METHOD              WSAConnect
               16  LOAD_DEREF               'conn'
               18  LOAD_METHOD              fileno
               20  CALL_METHOD_0         0  ''
               22  LOAD_FAST                'address'
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          

 L. 581        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _loop
               32  LOAD_METHOD              create_future
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'fut'

 L. 582        38  LOAD_FAST                'fut'
               40  LOAD_METHOD              set_result
               42  LOAD_CONST               None
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 583        48  LOAD_FAST                'fut'
               50  RETURN_VALUE     
             52_0  COME_FROM            10  '10'

 L. 585        52  LOAD_FAST                'self'
               54  LOAD_METHOD              _register_with_iocp
               56  LOAD_DEREF               'conn'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 587        62  SETUP_FINALLY        86  'to 86'

 L. 588        64  LOAD_GLOBAL              _overlapped
               66  LOAD_METHOD              BindLocal
               68  LOAD_DEREF               'conn'
               70  LOAD_METHOD              fileno
               72  CALL_METHOD_0         0  ''
               74  LOAD_DEREF               'conn'
               76  LOAD_ATTR                family
               78  CALL_METHOD_2         2  ''
               80  POP_TOP          
               82  POP_BLOCK        
               84  JUMP_FORWARD        154  'to 154'
             86_0  COME_FROM_FINALLY    62  '62'

 L. 589        86  DUP_TOP          
               88  LOAD_GLOBAL              OSError
               90  <121>               152  ''
               92  POP_TOP          
               94  STORE_FAST               'e'
               96  POP_TOP          
               98  SETUP_FINALLY       144  'to 144'

 L. 590       100  LOAD_FAST                'e'
              102  LOAD_ATTR                winerror
              104  LOAD_GLOBAL              errno
              106  LOAD_ATTR                WSAEINVAL
              108  COMPARE_OP               !=
              110  POP_JUMP_IF_FALSE   114  'to 114'

 L. 591       112  RAISE_VARARGS_0       0  'reraise'
            114_0  COME_FROM           110  '110'

 L. 593       114  LOAD_DEREF               'conn'
              116  LOAD_METHOD              getsockname
              118  CALL_METHOD_0         0  ''
              120  LOAD_CONST               1
              122  BINARY_SUBSCR    
              124  LOAD_CONST               0
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   132  'to 132'

 L. 594       130  RAISE_VARARGS_0       0  'reraise'
            132_0  COME_FROM           128  '128'
              132  POP_BLOCK        
              134  POP_EXCEPT       
              136  LOAD_CONST               None
              138  STORE_FAST               'e'
              140  DELETE_FAST              'e'
              142  JUMP_FORWARD        154  'to 154'
            144_0  COME_FROM_FINALLY    98  '98'
              144  LOAD_CONST               None
              146  STORE_FAST               'e'
              148  DELETE_FAST              'e'
              150  <48>             
              152  <48>             
            154_0  COME_FROM           142  '142'
            154_1  COME_FROM            84  '84'

 L. 595       154  LOAD_GLOBAL              _overlapped
              156  LOAD_METHOD              Overlapped
              158  LOAD_GLOBAL              NULL
              160  CALL_METHOD_1         1  ''
              162  STORE_FAST               'ov'

 L. 596       164  LOAD_FAST                'ov'
              166  LOAD_METHOD              ConnectEx
              168  LOAD_DEREF               'conn'
              170  LOAD_METHOD              fileno
              172  CALL_METHOD_0         0  ''
              174  LOAD_FAST                'address'
              176  CALL_METHOD_2         2  ''
              178  POP_TOP          

 L. 598       180  LOAD_CLOSURE             'conn'
              182  BUILD_TUPLE_1         1 
              184  LOAD_CODE                <code_object finish_connect>
              186  LOAD_STR                 'IocpProactor.connect.<locals>.finish_connect'
              188  MAKE_FUNCTION_8          'closure'
              190  STORE_FAST               'finish_connect'

 L. 605       192  LOAD_FAST                'self'
              194  LOAD_METHOD              _register
              196  LOAD_FAST                'ov'
              198  LOAD_DEREF               'conn'
              200  LOAD_FAST                'finish_connect'
              202  CALL_METHOD_3         3  ''
              204  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 90

    def sendfile(self, sock, file, offset, count):
        self._register_with_iocpsock
        ov = _overlapped.OverlappedNULL
        offset_low = offset & 4294967295
        offset_high = offset >> 32 & 4294967295
        ov.TransmitFile(sock.fileno, msvcrt.get_osfhandlefile.fileno, offset_low, offset_high, count, 0, 0)

        def finish_sendfile--- This code section failed: ---

 L. 618         0  SETUP_FINALLY        12  'to 12'

 L. 619         2  LOAD_FAST                'ov'
                4  LOAD_METHOD              getresult
                6  CALL_METHOD_0         0  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 620        12  DUP_TOP          
               14  LOAD_GLOBAL              OSError
               16  <121>                78  ''
               18  POP_TOP          
               20  STORE_FAST               'exc'
               22  POP_TOP          
               24  SETUP_FINALLY        70  'to 70'

 L. 621        26  LOAD_FAST                'exc'
               28  LOAD_ATTR                winerror
               30  LOAD_GLOBAL              _overlapped
               32  LOAD_ATTR                ERROR_NETNAME_DELETED

 L. 622        34  LOAD_GLOBAL              _overlapped
               36  LOAD_ATTR                ERROR_OPERATION_ABORTED

 L. 621        38  BUILD_TUPLE_2         2 
               40  <118>                 0  ''
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L. 623        44  LOAD_GLOBAL              ConnectionResetError
               46  LOAD_FAST                'exc'
               48  LOAD_ATTR                args
               50  CALL_FUNCTION_EX      0  'positional arguments only'
               52  RAISE_VARARGS_1       1  'exception instance'
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            42  '42'

 L. 625        56  RAISE_VARARGS_0       0  'reraise'
             58_0  COME_FROM            54  '54'
               58  POP_BLOCK        
               60  POP_EXCEPT       
               62  LOAD_CONST               None
               64  STORE_FAST               'exc'
               66  DELETE_FAST              'exc'
               68  JUMP_FORWARD         80  'to 80'
             70_0  COME_FROM_FINALLY    24  '24'
               70  LOAD_CONST               None
               72  STORE_FAST               'exc'
               74  DELETE_FAST              'exc'
               76  <48>             
               78  <48>             
             80_0  COME_FROM            68  '68'

Parse error at or near `<121>' instruction at offset 16

        return self._registerovsockfinish_sendfile

    def accept_pipe(self, pipe):
        self._register_with_iocppipe
        ov = _overlapped.OverlappedNULL
        connected = ov.ConnectNamedPipepipe.fileno
        if connected:
            return self._resultpipe

        def finish_accept_pipe(trans, key, ov):
            ov.getresult
            return pipe

        return self._registerovpipefinish_accept_pipe

    async def connect_pipe--- This code section failed: ---

 L. 646         0  LOAD_GLOBAL              CONNECT_PIPE_INIT_DELAY
                2  STORE_FAST               'delay'
              4_0  COME_FROM           104  '104'

 L. 651         4  SETUP_FINALLY        24  'to 24'

 L. 652         6  LOAD_GLOBAL              _overlapped
                8  LOAD_METHOD              ConnectPipe
               10  LOAD_FAST                'address'
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'handle'

 L. 653        16  POP_BLOCK        
               18  BREAK_LOOP          106  'to 106'
               20  POP_BLOCK        
               22  JUMP_FORWARD         74  'to 74'
             24_0  COME_FROM_FINALLY     4  '4'

 L. 654        24  DUP_TOP          
               26  LOAD_GLOBAL              OSError
               28  <121>                72  ''
               30  POP_TOP          
               32  STORE_FAST               'exc'
               34  POP_TOP          
               36  SETUP_FINALLY        64  'to 64'

 L. 655        38  LOAD_FAST                'exc'
               40  LOAD_ATTR                winerror
               42  LOAD_GLOBAL              _overlapped
               44  LOAD_ATTR                ERROR_PIPE_BUSY
               46  COMPARE_OP               !=
               48  POP_JUMP_IF_FALSE    52  'to 52'

 L. 656        50  RAISE_VARARGS_0       0  'reraise'
             52_0  COME_FROM            48  '48'
               52  POP_BLOCK        
               54  POP_EXCEPT       
               56  LOAD_CONST               None
               58  STORE_FAST               'exc'
               60  DELETE_FAST              'exc'
               62  JUMP_FORWARD         74  'to 74'
             64_0  COME_FROM_FINALLY    36  '36'
               64  LOAD_CONST               None
               66  STORE_FAST               'exc'
               68  DELETE_FAST              'exc'
               70  <48>             
               72  <48>             
             74_0  COME_FROM            62  '62'
             74_1  COME_FROM            22  '22'

 L. 659        74  LOAD_GLOBAL              min
               76  LOAD_FAST                'delay'
               78  LOAD_CONST               2
               80  BINARY_MULTIPLY  
               82  LOAD_GLOBAL              CONNECT_PIPE_MAX_DELAY
               84  CALL_FUNCTION_2       2  ''
               86  STORE_FAST               'delay'

 L. 660        88  LOAD_GLOBAL              tasks
               90  LOAD_METHOD              sleep
               92  LOAD_FAST                'delay'
               94  CALL_METHOD_1         1  ''
               96  GET_AWAITABLE    
               98  LOAD_CONST               None
              100  YIELD_FROM       
              102  POP_TOP          
              104  JUMP_BACK             4  'to 4'
            106_0  COME_FROM            18  '18'

 L. 662       106  LOAD_GLOBAL              windows_utils
              108  LOAD_METHOD              PipeHandle
              110  LOAD_FAST                'handle'
              112  CALL_METHOD_1         1  ''
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 28

    def wait_for_handle(self, handle, timeout=None):
        """Wait for a handle.

        Return a Future object. The result of the future is True if the wait
        completed, or False if the wait did not complete (on timeout).
        """
        return self._wait_for_handlehandletimeoutFalse

    def _wait_cancel(self, event, done_callback):
        fut = self._wait_for_handleeventNoneTrue
        fut._done_callback = done_callback
        return fut

    def _wait_for_handle--- This code section failed: ---

 L. 680         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_closed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 682         8  LOAD_FAST                'timeout'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 683        16  LOAD_GLOBAL              _winapi
               18  LOAD_ATTR                INFINITE
               20  STORE_FAST               'ms'
               22  JUMP_FORWARD         38  'to 38'
             24_0  COME_FROM            14  '14'

 L. 687        24  LOAD_GLOBAL              math
               26  LOAD_METHOD              ceil
               28  LOAD_FAST                'timeout'
               30  LOAD_CONST               1000.0
               32  BINARY_MULTIPLY  
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'ms'
             38_0  COME_FROM            22  '22'

 L. 690        38  LOAD_GLOBAL              _overlapped
               40  LOAD_METHOD              Overlapped
               42  LOAD_GLOBAL              NULL
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'ov'

 L. 691        48  LOAD_GLOBAL              _overlapped
               50  LOAD_METHOD              RegisterWaitWithQueue

 L. 692        52  LOAD_FAST                'handle'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _iocp
               58  LOAD_FAST                'ov'
               60  LOAD_ATTR                address
               62  LOAD_FAST                'ms'

 L. 691        64  CALL_METHOD_4         4  ''
               66  STORE_FAST               'wait_handle'

 L. 693        68  LOAD_FAST                '_is_cancel'
               70  POP_JUMP_IF_FALSE    92  'to 92'

 L. 694        72  LOAD_GLOBAL              _WaitCancelFuture
               74  LOAD_FAST                'ov'
               76  LOAD_FAST                'handle'
               78  LOAD_FAST                'wait_handle'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _loop
               84  LOAD_CONST               ('loop',)
               86  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               88  STORE_DEREF              'f'
               90  JUMP_FORWARD        112  'to 112'
             92_0  COME_FROM            70  '70'

 L. 696        92  LOAD_GLOBAL              _WaitHandleFuture
               94  LOAD_FAST                'ov'
               96  LOAD_FAST                'handle'
               98  LOAD_FAST                'wait_handle'
              100  LOAD_FAST                'self'

 L. 697       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _loop

 L. 696       106  LOAD_CONST               ('loop',)
              108  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              110  STORE_DEREF              'f'
            112_0  COME_FROM            90  '90'

 L. 698       112  LOAD_DEREF               'f'
              114  LOAD_ATTR                _source_traceback
              116  POP_JUMP_IF_FALSE   126  'to 126'

 L. 699       118  LOAD_DEREF               'f'
              120  LOAD_ATTR                _source_traceback
              122  LOAD_CONST               -1
              124  DELETE_SUBSCR    
            126_0  COME_FROM           116  '116'

 L. 701       126  LOAD_CLOSURE             'f'
              128  BUILD_TUPLE_1         1 
              130  LOAD_CODE                <code_object finish_wait_for_handle>
              132  LOAD_STR                 'IocpProactor._wait_for_handle.<locals>.finish_wait_for_handle'
              134  MAKE_FUNCTION_8          'closure'
              136  STORE_FAST               'finish_wait_for_handle'

 L. 710       138  LOAD_DEREF               'f'
              140  LOAD_FAST                'ov'
              142  LOAD_CONST               0
              144  LOAD_FAST                'finish_wait_for_handle'
              146  BUILD_TUPLE_4         4 
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                _cache
              152  LOAD_FAST                'ov'
              154  LOAD_ATTR                address
              156  STORE_SUBSCR     

 L. 711       158  LOAD_DEREF               'f'
              160  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12

    def _register_with_iocp--- This code section failed: ---

 L. 716         0  LOAD_FAST                'obj'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _registered
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    44  'to 44'

 L. 717        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _registered
               14  LOAD_METHOD              add
               16  LOAD_FAST                'obj'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 718        22  LOAD_GLOBAL              _overlapped
               24  LOAD_METHOD              CreateIoCompletionPort
               26  LOAD_FAST                'obj'
               28  LOAD_METHOD              fileno
               30  CALL_METHOD_0         0  ''
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _iocp
               36  LOAD_CONST               0
               38  LOAD_CONST               0
               40  CALL_METHOD_4         4  ''
               42  POP_TOP          
             44_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def _register--- This code section failed: ---

 L. 724         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_closed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 729         8  LOAD_GLOBAL              _OverlappedFuture
               10  LOAD_FAST                'ov'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _loop
               16  LOAD_CONST               ('loop',)
               18  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               20  STORE_FAST               'f'

 L. 730        22  LOAD_FAST                'f'
               24  LOAD_ATTR                _source_traceback
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 731        28  LOAD_FAST                'f'
               30  LOAD_ATTR                _source_traceback
               32  LOAD_CONST               -1
               34  DELETE_SUBSCR    
             36_0  COME_FROM            26  '26'

 L. 732        36  LOAD_FAST                'ov'
               38  LOAD_ATTR                pending
               40  POP_JUMP_IF_TRUE    116  'to 116'

 L. 737        42  SETUP_FINALLY        60  'to 60'

 L. 738        44  LOAD_FAST                'callback'
               46  LOAD_CONST               None
               48  LOAD_CONST               None
               50  LOAD_FAST                'ov'
               52  CALL_FUNCTION_3       3  ''
               54  STORE_FAST               'value'
               56  POP_BLOCK        
               58  JUMP_FORWARD        106  'to 106'
             60_0  COME_FROM_FINALLY    42  '42'

 L. 739        60  DUP_TOP          
               62  LOAD_GLOBAL              OSError
               64  <121>               104  ''
               66  POP_TOP          
               68  STORE_FAST               'e'
               70  POP_TOP          
               72  SETUP_FINALLY        96  'to 96'

 L. 740        74  LOAD_FAST                'f'
               76  LOAD_METHOD              set_exception
               78  LOAD_FAST                'e'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  POP_BLOCK        
               86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  STORE_FAST               'e'
               92  DELETE_FAST              'e'
               94  JUMP_FORWARD        116  'to 116'
             96_0  COME_FROM_FINALLY    72  '72'
               96  LOAD_CONST               None
               98  STORE_FAST               'e'
              100  DELETE_FAST              'e'
              102  <48>             
              104  <48>             
            106_0  COME_FROM            58  '58'

 L. 742       106  LOAD_FAST                'f'
              108  LOAD_METHOD              set_result
              110  LOAD_FAST                'value'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
            116_0  COME_FROM            94  '94'
            116_1  COME_FROM            40  '40'

 L. 752       116  LOAD_FAST                'f'
              118  LOAD_FAST                'ov'
              120  LOAD_FAST                'obj'
              122  LOAD_FAST                'callback'
              124  BUILD_TUPLE_4         4 
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                _cache
              130  LOAD_FAST                'ov'
              132  LOAD_ATTR                address
              134  STORE_SUBSCR     

 L. 753       136  LOAD_FAST                'f'
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 64

    def _unregister(self, ov):
        """Unregister an overlapped object.

        Call this method when its future has been cancelled. The event can
        already be signalled (pending in the proactor event queue). It is also
        safe if the event is never signalled (because it was cancelled).
        """
        self._check_closed
        self._unregistered.appendov

    def _get_accept_socket(self, family):
        s = socket.socketfamily
        s.settimeout0
        return s

    def _poll--- This code section failed: ---

 L. 771         0  LOAD_FAST                'timeout'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 772         8  LOAD_GLOBAL              INFINITE
               10  STORE_FAST               'ms'
               12  JUMP_FORWARD         62  'to 62'
             14_0  COME_FROM             6  '6'

 L. 773        14  LOAD_FAST                'timeout'
               16  LOAD_CONST               0
               18  COMPARE_OP               <
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 774        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 'negative timeout'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
               30  JUMP_FORWARD         62  'to 62'
             32_0  COME_FROM            20  '20'

 L. 778        32  LOAD_GLOBAL              math
               34  LOAD_METHOD              ceil
               36  LOAD_FAST                'timeout'
               38  LOAD_CONST               1000.0
               40  BINARY_MULTIPLY  
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'ms'

 L. 779        46  LOAD_FAST                'ms'
               48  LOAD_GLOBAL              INFINITE
               50  COMPARE_OP               >=
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 780        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'timeout too big'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM           344  '344'
             62_1  COME_FROM           310  '310'
             62_2  COME_FROM           242  '242'
             62_3  COME_FROM           234  '234'
             62_4  COME_FROM           208  '208'
             62_5  COME_FROM            52  '52'
             62_6  COME_FROM            30  '30'
             62_7  COME_FROM            12  '12'

 L. 783        62  LOAD_GLOBAL              _overlapped
               64  LOAD_METHOD              GetQueuedCompletionStatus
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _iocp
               70  LOAD_FAST                'ms'
               72  CALL_METHOD_2         2  ''
               74  STORE_FAST               'status'

 L. 784        76  LOAD_FAST                'status'
               78  LOAD_CONST               None
               80  <117>                 0  ''
               82  POP_JUMP_IF_FALSE    88  'to 88'

 L. 785     84_86  JUMP_FORWARD        346  'to 346'
             88_0  COME_FROM            82  '82'

 L. 786        88  LOAD_CONST               0
               90  STORE_FAST               'ms'

 L. 788        92  LOAD_FAST                'status'
               94  UNPACK_SEQUENCE_4     4 
               96  STORE_FAST               'err'
               98  STORE_FAST               'transferred'
              100  STORE_FAST               'key'
              102  STORE_FAST               'address'

 L. 789       104  SETUP_FINALLY       130  'to 130'

 L. 790       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _cache
              110  LOAD_METHOD              pop
              112  LOAD_FAST                'address'
              114  CALL_METHOD_1         1  ''
              116  UNPACK_SEQUENCE_4     4 
              118  STORE_FAST               'f'
              120  STORE_FAST               'ov'
              122  STORE_FAST               'obj'
              124  STORE_FAST               'callback'
              126  POP_BLOCK        
              128  JUMP_FORWARD        216  'to 216'
            130_0  COME_FROM_FINALLY   104  '104'

 L. 791       130  DUP_TOP          
              132  LOAD_GLOBAL              KeyError
              134  <121>               214  ''
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L. 792       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _loop
              146  LOAD_METHOD              get_debug
              148  CALL_METHOD_0         0  ''
              150  POP_JUMP_IF_FALSE   182  'to 182'

 L. 793       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _loop
              156  LOAD_METHOD              call_exception_handler

 L. 794       158  LOAD_STR                 'GetQueuedCompletionStatus() returned an unexpected event'

 L. 796       160  LOAD_STR                 'err=%s transferred=%s key=%#x address=%#x'

 L. 797       162  LOAD_FAST                'err'
              164  LOAD_FAST                'transferred'
              166  LOAD_FAST                'key'
              168  LOAD_FAST                'address'
              170  BUILD_TUPLE_4         4 

 L. 796       172  BINARY_MODULO    

 L. 793       174  LOAD_CONST               ('message', 'status')
              176  BUILD_CONST_KEY_MAP_2     2 
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          
            182_0  COME_FROM           150  '150'

 L. 802       182  LOAD_FAST                'key'
              184  LOAD_CONST               0
              186  LOAD_GLOBAL              _overlapped
              188  LOAD_ATTR                INVALID_HANDLE_VALUE
              190  BUILD_TUPLE_2         2 
              192  <118>                 1  ''
              194  POP_JUMP_IF_FALSE   206  'to 206'

 L. 803       196  LOAD_GLOBAL              _winapi
              198  LOAD_METHOD              CloseHandle
              200  LOAD_FAST                'key'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          
            206_0  COME_FROM           194  '194'

 L. 804       206  POP_EXCEPT       
              208  JUMP_BACK            62  'to 62'
              210  POP_EXCEPT       
              212  JUMP_FORWARD        216  'to 216'
              214  <48>             
            216_0  COME_FROM           212  '212'
            216_1  COME_FROM           128  '128'

 L. 806       216  LOAD_FAST                'obj'
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                _stopped_serving
              222  <118>                 0  ''
              224  POP_JUMP_IF_FALSE   236  'to 236'

 L. 807       226  LOAD_FAST                'f'
              228  LOAD_METHOD              cancel
              230  CALL_METHOD_0         0  ''
              232  POP_TOP          
              234  JUMP_BACK            62  'to 62'
            236_0  COME_FROM           224  '224'

 L. 810       236  LOAD_FAST                'f'
              238  LOAD_METHOD              done
              240  CALL_METHOD_0         0  ''
              242  POP_JUMP_IF_TRUE_BACK    62  'to 62'

 L. 811       244  SETUP_FINALLY       262  'to 262'

 L. 812       246  LOAD_FAST                'callback'
              248  LOAD_FAST                'transferred'
              250  LOAD_FAST                'key'
              252  LOAD_FAST                'ov'
              254  CALL_FUNCTION_3       3  ''
              256  STORE_FAST               'value'
              258  POP_BLOCK        
              260  JUMP_FORWARD        322  'to 322'
            262_0  COME_FROM_FINALLY   244  '244'

 L. 813       262  DUP_TOP          
              264  LOAD_GLOBAL              OSError
          266_268  <121>               320  ''
              270  POP_TOP          
              272  STORE_FAST               'e'
              274  POP_TOP          
              276  SETUP_FINALLY       312  'to 312'

 L. 814       278  LOAD_FAST                'f'
              280  LOAD_METHOD              set_exception
              282  LOAD_FAST                'e'
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L. 815       288  LOAD_FAST                'self'
              290  LOAD_ATTR                _results
              292  LOAD_METHOD              append
              294  LOAD_FAST                'f'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
              300  POP_BLOCK        
              302  POP_EXCEPT       
              304  LOAD_CONST               None
              306  STORE_FAST               'e'
              308  DELETE_FAST              'e'
              310  JUMP_BACK            62  'to 62'
            312_0  COME_FROM_FINALLY   276  '276'
              312  LOAD_CONST               None
              314  STORE_FAST               'e'
              316  DELETE_FAST              'e'
              318  <48>             
              320  <48>             
            322_0  COME_FROM           260  '260'

 L. 817       322  LOAD_FAST                'f'
              324  LOAD_METHOD              set_result
              326  LOAD_FAST                'value'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          

 L. 818       332  LOAD_FAST                'self'
              334  LOAD_ATTR                _results
              336  LOAD_METHOD              append
              338  LOAD_FAST                'f'
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          
              344  JUMP_BACK            62  'to 62'
            346_0  COME_FROM            84  '84'

 L. 821       346  LOAD_FAST                'self'
              348  LOAD_ATTR                _unregistered
              350  GET_ITER         
            352_0  COME_FROM           372  '372'
              352  FOR_ITER            376  'to 376'
              354  STORE_FAST               'ov'

 L. 822       356  LOAD_FAST                'self'
              358  LOAD_ATTR                _cache
              360  LOAD_METHOD              pop
              362  LOAD_FAST                'ov'
              364  LOAD_ATTR                address
              366  LOAD_CONST               None
              368  CALL_METHOD_2         2  ''
              370  POP_TOP          
          372_374  JUMP_BACK           352  'to 352'
            376_0  COME_FROM           352  '352'

 L. 823       376  LOAD_FAST                'self'
              378  LOAD_ATTR                _unregistered
              380  LOAD_METHOD              clear
              382  CALL_METHOD_0         0  ''
              384  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _stop_serving(self, obj):
        self._stopped_serving.addobj

    def close--- This code section failed: ---

 L. 832         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _iocp
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 834        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 837        14  LOAD_GLOBAL              list
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _cache
               20  LOAD_METHOD              items
               22  CALL_METHOD_0         0  ''
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
             28_0  COME_FROM           166  '166'
             28_1  COME_FROM           154  '154'
             28_2  COME_FROM            78  '78'
             28_3  COME_FROM            64  '64'
             28_4  COME_FROM            52  '52'
               28  FOR_ITER            168  'to 168'
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'address'
               34  UNPACK_SEQUENCE_4     4 
               36  STORE_FAST               'fut'
               38  STORE_FAST               'ov'
               40  STORE_FAST               'obj'
               42  STORE_FAST               'callback'

 L. 838        44  LOAD_FAST                'fut'
               46  LOAD_METHOD              cancelled
               48  CALL_METHOD_0         0  ''
               50  POP_JUMP_IF_FALSE    54  'to 54'

 L. 840        52  JUMP_BACK            28  'to 28'
             54_0  COME_FROM            50  '50'

 L. 841        54  LOAD_GLOBAL              isinstance
               56  LOAD_FAST                'fut'
               58  LOAD_GLOBAL              _WaitCancelFuture
               60  CALL_FUNCTION_2       2  ''
               62  POP_JUMP_IF_FALSE    66  'to 66'

 L. 843        64  JUMP_BACK            28  'to 28'
             66_0  COME_FROM            62  '62'

 L. 845        66  SETUP_FINALLY        80  'to 80'

 L. 846        68  LOAD_FAST                'fut'
               70  LOAD_METHOD              cancel
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          
               76  POP_BLOCK        
               78  JUMP_BACK            28  'to 28'
             80_0  COME_FROM_FINALLY    66  '66'

 L. 847        80  DUP_TOP          
               82  LOAD_GLOBAL              OSError
               84  <121>               164  ''
               86  POP_TOP          
               88  STORE_FAST               'exc'
               90  POP_TOP          
               92  SETUP_FINALLY       156  'to 156'

 L. 848        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _loop
               98  LOAD_CONST               None
              100  <117>                 1  ''
              102  POP_JUMP_IF_FALSE   144  'to 144'

 L. 850       104  LOAD_STR                 'Cancelling a future failed'

 L. 851       106  LOAD_FAST                'exc'

 L. 852       108  LOAD_FAST                'fut'

 L. 849       110  LOAD_CONST               ('message', 'exception', 'future')
              112  BUILD_CONST_KEY_MAP_3     3 
              114  STORE_FAST               'context'

 L. 854       116  LOAD_FAST                'fut'
              118  LOAD_ATTR                _source_traceback
              120  POP_JUMP_IF_FALSE   132  'to 132'

 L. 855       122  LOAD_FAST                'fut'
              124  LOAD_ATTR                _source_traceback
              126  LOAD_FAST                'context'
              128  LOAD_STR                 'source_traceback'
              130  STORE_SUBSCR     
            132_0  COME_FROM           120  '120'

 L. 856       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _loop
              136  LOAD_METHOD              call_exception_handler
              138  LOAD_FAST                'context'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           102  '102'
              144  POP_BLOCK        
              146  POP_EXCEPT       
              148  LOAD_CONST               None
              150  STORE_FAST               'exc'
              152  DELETE_FAST              'exc'
              154  JUMP_BACK            28  'to 28'
            156_0  COME_FROM_FINALLY    92  '92'
              156  LOAD_CONST               None
              158  STORE_FAST               'exc'
              160  DELETE_FAST              'exc'
              162  <48>             
              164  <48>             
              166  JUMP_BACK            28  'to 28'
            168_0  COME_FROM            28  '28'

 L. 861       168  LOAD_CONST               1.0
              170  STORE_FAST               'msg_update'

 L. 862       172  LOAD_GLOBAL              time
              174  LOAD_METHOD              monotonic
              176  CALL_METHOD_0         0  ''
              178  STORE_FAST               'start_time'

 L. 863       180  LOAD_FAST                'start_time'
              182  LOAD_FAST                'msg_update'
              184  BINARY_ADD       
              186  STORE_FAST               'next_msg'
            188_0  COME_FROM           250  '250'

 L. 864       188  LOAD_FAST                'self'
              190  LOAD_ATTR                _cache
              192  POP_JUMP_IF_FALSE   252  'to 252'

 L. 865       194  LOAD_FAST                'next_msg'
              196  LOAD_GLOBAL              time
              198  LOAD_METHOD              monotonic
              200  CALL_METHOD_0         0  ''
              202  COMPARE_OP               <=
              204  POP_JUMP_IF_FALSE   240  'to 240'

 L. 866       206  LOAD_GLOBAL              logger
              208  LOAD_METHOD              debug
              210  LOAD_STR                 '%r is running after closing for %.1f seconds'

 L. 867       212  LOAD_FAST                'self'
              214  LOAD_GLOBAL              time
              216  LOAD_METHOD              monotonic
              218  CALL_METHOD_0         0  ''
              220  LOAD_FAST                'start_time'
              222  BINARY_SUBTRACT  

 L. 866       224  CALL_METHOD_3         3  ''
              226  POP_TOP          

 L. 868       228  LOAD_GLOBAL              time
              230  LOAD_METHOD              monotonic
              232  CALL_METHOD_0         0  ''
              234  LOAD_FAST                'msg_update'
              236  BINARY_ADD       
              238  STORE_FAST               'next_msg'
            240_0  COME_FROM           204  '204'

 L. 871       240  LOAD_FAST                'self'
              242  LOAD_METHOD              _poll
              244  LOAD_FAST                'msg_update'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
              250  JUMP_BACK           188  'to 188'
            252_0  COME_FROM           192  '192'

 L. 873       252  BUILD_LIST_0          0 
              254  LOAD_FAST                'self'
              256  STORE_ATTR               _results

 L. 875       258  LOAD_GLOBAL              _winapi
              260  LOAD_METHOD              CloseHandle
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                _iocp
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          

 L. 876       270  LOAD_CONST               None
              272  LOAD_FAST                'self'
              274  STORE_ATTR               _iocp

Parse error at or near `None' instruction at offset -1

    def __del__(self):
        self.close


class _WindowsSubprocessTransport(base_subprocess.BaseSubprocessTransport):

    def _start--- This code section failed: ---

 L. 885         0  LOAD_GLOBAL              windows_utils
                2  LOAD_ATTR                Popen

 L. 886         4  LOAD_FAST                'args'

 L. 885         6  BUILD_TUPLE_1         1 

 L. 886         8  LOAD_FAST                'shell'
               10  LOAD_FAST                'stdin'
               12  LOAD_FAST                'stdout'
               14  LOAD_FAST                'stderr'

 L. 887        16  LOAD_FAST                'bufsize'

 L. 885        18  LOAD_CONST               ('shell', 'stdin', 'stdout', 'stderr', 'bufsize')
               20  BUILD_CONST_KEY_MAP_5     5 

 L. 887        22  LOAD_FAST                'kwargs'

 L. 885        24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  LOAD_DEREF               'self'
               30  STORE_ATTR               _proc

 L. 889        32  LOAD_CLOSURE             'self'
               34  BUILD_TUPLE_1         1 
               36  LOAD_CODE                <code_object callback>
               38  LOAD_STR                 '_WindowsSubprocessTransport._start.<locals>.callback'
               40  MAKE_FUNCTION_8          'closure'
               42  STORE_FAST               'callback'

 L. 893        44  LOAD_DEREF               'self'
               46  LOAD_ATTR                _loop
               48  LOAD_ATTR                _proactor
               50  LOAD_METHOD              wait_for_handle
               52  LOAD_GLOBAL              int
               54  LOAD_DEREF               'self'
               56  LOAD_ATTR                _proc
               58  LOAD_ATTR                _handle
               60  CALL_FUNCTION_1       1  ''
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'f'

 L. 894        66  LOAD_FAST                'f'
               68  LOAD_METHOD              add_done_callback
               70  LOAD_FAST                'callback'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

Parse error at or near `<164>' instruction at offset 24


SelectorEventLoop = _WindowsSelectorEventLoop

class WindowsSelectorEventLoopPolicy(events.BaseDefaultEventLoopPolicy):
    _loop_factory = SelectorEventLoop


class WindowsProactorEventLoopPolicy(events.BaseDefaultEventLoopPolicy):
    _loop_factory = ProactorEventLoop


DefaultEventLoopPolicy = WindowsProactorEventLoopPolicy