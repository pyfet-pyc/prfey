# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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

    def _repr_info(self):
        info = super()._repr_info()
        if self._ov is not None:
            state = 'pending' if self._ov.pending else 'completed'
            info.insert(1, f"overlapped=<{state}, {self._ov.address:#x}>")
        return info

    def _cancel_overlapped(self):
        if self._ov is None:
            return
        try:
            self._ov.cancel()
        except OSError as exc:
            try:
                context = {'message':'Cancelling an overlapped future failed', 
                 'exception':exc, 
                 'future':self}
                if self._source_traceback:
                    context['source_traceback'] = self._source_traceback
                self._loop.call_exception_handler(context)
            finally:
                exc = None
                del exc

        else:
            self._ov = None

    def cancel(self):
        self._cancel_overlapped()
        return super().cancel()

    def set_exception(self, exception):
        super().set_exception(exception)
        self._cancel_overlapped()

    def set_result(self, result):
        super().set_result(result)
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
        return _winapi.WaitForSingleObject(self._handle, 0) == _winapi.WAIT_OBJECT_0

    def _repr_info(self):
        info = super()._repr_info()
        info.append(f"handle={self._handle:#x}")
        if self._handle is not None:
            state = 'signaled' if self._poll() else 'waiting'
            info.append(state)
        if self._wait_handle is not None:
            info.append(f"wait_handle={self._wait_handle:#x}")
        return info

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
               42  JUMP_FORWARD        140  'to 140'
             44_0  COME_FROM_FINALLY    28  '28'

 L. 137        44  DUP_TOP          
               46  LOAD_GLOBAL              OSError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE   138  'to 138'
               52  POP_TOP          
               54  STORE_FAST               'exc'
               56  POP_TOP          
               58  SETUP_FINALLY       126  'to 126'

 L. 138        60  LOAD_FAST                'exc'
               62  LOAD_ATTR                winerror
               64  LOAD_GLOBAL              _overlapped
               66  LOAD_ATTR                ERROR_IO_PENDING
               68  COMPARE_OP               !=
               70  POP_JUMP_IF_FALSE   122  'to 122'

 L. 140        72  LOAD_STR                 'Failed to unregister the wait handle'

 L. 141        74  LOAD_FAST                'exc'

 L. 142        76  LOAD_FAST                'self'

 L. 139        78  LOAD_CONST               ('message', 'exception', 'future')
               80  BUILD_CONST_KEY_MAP_3     3 
               82  STORE_FAST               'context'

 L. 144        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _source_traceback
               88  POP_JUMP_IF_FALSE   100  'to 100'

 L. 145        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _source_traceback
               94  LOAD_FAST                'context'
               96  LOAD_STR                 'source_traceback'
               98  STORE_SUBSCR     
            100_0  COME_FROM            88  '88'

 L. 146       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _loop
              104  LOAD_METHOD              call_exception_handler
              106  LOAD_FAST                'context'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 147       112  POP_BLOCK        
              114  POP_EXCEPT       
              116  CALL_FINALLY        126  'to 126'
              118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM            70  '70'
              122  POP_BLOCK        
              124  BEGIN_FINALLY    
            126_0  COME_FROM           116  '116'
            126_1  COME_FROM_FINALLY    58  '58'
              126  LOAD_CONST               None
              128  STORE_FAST               'exc'
              130  DELETE_FAST              'exc'
              132  END_FINALLY      
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM            50  '50'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM            42  '42'

 L. 150       140  LOAD_FAST                'self'
              142  LOAD_METHOD              _unregister_wait_cb
              144  LOAD_CONST               None
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 114

    def cancel(self):
        self._unregister_wait()
        return super().cancel()

    def set_exception(self, exception):
        self._unregister_wait()
        super().set_exception(exception)

    def set_result(self, result):
        self._unregister_wait()
        super().set_result(result)


class _WaitCancelFuture(_BaseWaitHandleFuture):
    __doc__ = 'Subclass of Future which represents a wait for the cancellation of a\n    _WaitHandleFuture using an event.\n    '

    def __init__(self, ov, event, wait_handle, *, loop=None):
        super().__init__(ov, event, wait_handle, loop=loop)
        self._done_callback = None

    def cancel(self):
        raise RuntimeError('_WaitCancelFuture must not be cancelled')

    def set_result(self, result):
        super().set_result(result)
        if self._done_callback is not None:
            self._done_callback(self)

    def set_exception(self, exception):
        super().set_exception(exception)
        if self._done_callback is not None:
            self._done_callback(self)


class _WaitHandleFuture(_BaseWaitHandleFuture):

    def __init__(self, ov, handle, wait_handle, proactor, *, loop=None):
        super().__init__(ov, handle, wait_handle, loop=loop)
        self._proactor = proactor
        self._unregister_proactor = True
        self._event = _overlapped.CreateEvent(None, True, False, None)
        self._event_fut = None

    def _unregister_wait_cb(self, fut):
        if self._event is not None:
            _winapi.CloseHandle(self._event)
            self._event = None
            self._event_fut = None
        self._proactor._unregister(self._ov)
        self._proactor = None
        super()._unregister_wait_cb(fut)

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
               46  JUMP_FORWARD        144  'to 144'
             48_0  COME_FROM_FINALLY    28  '28'

 L. 224        48  DUP_TOP          
               50  LOAD_GLOBAL              OSError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE   142  'to 142'
               56  POP_TOP          
               58  STORE_FAST               'exc'
               60  POP_TOP          
               62  SETUP_FINALLY       130  'to 130'

 L. 225        64  LOAD_FAST                'exc'
               66  LOAD_ATTR                winerror
               68  LOAD_GLOBAL              _overlapped
               70  LOAD_ATTR                ERROR_IO_PENDING
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE   126  'to 126'

 L. 227        76  LOAD_STR                 'Failed to unregister the wait handle'

 L. 228        78  LOAD_FAST                'exc'

 L. 229        80  LOAD_FAST                'self'

 L. 226        82  LOAD_CONST               ('message', 'exception', 'future')
               84  BUILD_CONST_KEY_MAP_3     3 
               86  STORE_FAST               'context'

 L. 231        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _source_traceback
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L. 232        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _source_traceback
               98  LOAD_FAST                'context'
              100  LOAD_STR                 'source_traceback'
              102  STORE_SUBSCR     
            104_0  COME_FROM            92  '92'

 L. 233       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _loop
              108  LOAD_METHOD              call_exception_handler
              110  LOAD_FAST                'context'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L. 234       116  POP_BLOCK        
              118  POP_EXCEPT       
              120  CALL_FINALLY        130  'to 130'
              122  LOAD_CONST               None
              124  RETURN_VALUE     
            126_0  COME_FROM            74  '74'
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM           120  '120'
            130_1  COME_FROM_FINALLY    62  '62'
              130  LOAD_CONST               None
              132  STORE_FAST               'exc'
              134  DELETE_FAST              'exc'
              136  END_FINALLY      
              138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM            54  '54'
              142  END_FINALLY      
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM            46  '46'

 L. 237       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _proactor
              148  LOAD_METHOD              _wait_cancel
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                _event

 L. 238       154  LOAD_FAST                'self'
              156  LOAD_ATTR                _unregister_wait_cb

 L. 237       158  CALL_METHOD_2         2  ''
              160  LOAD_FAST                'self'
              162  STORE_ATTR               _event_fut

Parse error at or near `POP_EXCEPT' instruction at offset 118


class PipeServer(object):
    __doc__ = 'Class representing a pipe server.\n\n    This is much like a bound, listening socket.\n    '

    def __init__(self, address):
        self._address = address
        self._free_instances = weakref.WeakSet()
        self._pipe = None
        self._accept_pipe_future = None
        self._pipe = self._server_pipe_handle(True)

    def _get_unconnected_pipe(self):
        tmp, self._pipe = self._pipe, self._server_pipe_handle(False)
        return tmp

    def _server_pipe_handle(self, first):
        if self.closed():
            return
        flags = _winapi.PIPE_ACCESS_DUPLEX | _winapi.FILE_FLAG_OVERLAPPED
        if first:
            flags |= _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE
        h = _winapi.CreateNamedPipe(self._address, flags, _winapi.PIPE_TYPE_MESSAGE | _winapi.PIPE_READMODE_MESSAGE | _winapi.PIPE_WAIT, _winapi.PIPE_UNLIMITED_INSTANCES, windows_utils.BUFSIZE, windows_utils.BUFSIZE, _winapi.NMPWAIT_WAIT_FOREVER, _winapi.NULL)
        pipe = windows_utils.PipeHandle(h)
        self._free_instances.add(pipe)
        return pipe

    def closed(self):
        return self._address is None

    def close(self):
        if self._accept_pipe_future is not None:
            self._accept_pipe_future.cancel()
            self._accept_pipe_future = None
        if self._address is not None:
            for pipe in self._free_instances:
                pipe.close()
            else:
                self._pipe = None
                self._address = None
                self._free_instances.clear()

    __del__ = close


class _WindowsSelectorEventLoop(selector_events.BaseSelectorEventLoop):
    __doc__ = 'Windows version of selector event loop.'


class ProactorEventLoop(proactor_events.BaseProactorEventLoop):
    __doc__ = 'Windows version of proactor event loop using IOCP.'

    def __init__(self, proactor=None):
        if proactor is None:
            proactor = IocpProactor()
        super().__init__(proactor)

    def run_forever(self):
        try:
            assert self._self_reading_future is None
            self.call_soon(self._loop_self_reading)
            super().run_forever()
        finally:
            if self._self_reading_future is not None:
                ov = self._self_reading_future._ov
                self._self_reading_future.cancel()
                if ov is not None:
                    self._proactor._unregister(ov)
                self._self_reading_future = None

    async def create_pipe_connection(self, protocol_factory, address):
        f = self._proactor.connect_pipe(address)
        pipe = await f
        protocol = protocol_factory()
        trans = self._make_duplex_pipe_transport(pipe, protocol, extra={'addr': address})
        return (trans, protocol)

    async def start_serving_pipe(self, protocol_factory, address):
        server = PipeServer(address)

        def loop_accept_pipe--- This code section failed: ---

 L. 339         0  LOAD_CONST               None
                2  STORE_FAST               'pipe'

 L. 340         4  SETUP_FINALLY       116  'to 116'

 L. 341         6  LOAD_FAST                'f'
                8  POP_JUMP_IF_FALSE    78  'to 78'

 L. 342        10  LOAD_FAST                'f'
               12  LOAD_METHOD              result
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'pipe'

 L. 343        18  LOAD_DEREF               'server'
               20  LOAD_ATTR                _free_instances
               22  LOAD_METHOD              discard
               24  LOAD_FAST                'pipe'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 345        30  LOAD_DEREF               'server'
               32  LOAD_METHOD              closed
               34  CALL_METHOD_0         0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 348        38  LOAD_FAST                'pipe'
               40  LOAD_METHOD              close
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L. 349        46  POP_BLOCK        
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            36  '36'

 L. 351        52  LOAD_DEREF               'protocol_factory'
               54  CALL_FUNCTION_0       0  ''
               56  STORE_FAST               'protocol'

 L. 352        58  LOAD_DEREF               'self'
               60  LOAD_ATTR                _make_duplex_pipe_transport

 L. 353        62  LOAD_FAST                'pipe'

 L. 353        64  LOAD_FAST                'protocol'

 L. 353        66  LOAD_STR                 'addr'
               68  LOAD_DEREF               'address'
               70  BUILD_MAP_1           1 

 L. 352        72  LOAD_CONST               ('extra',)
               74  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               76  POP_TOP          
             78_0  COME_FROM             8  '8'

 L. 355        78  LOAD_DEREF               'server'
               80  LOAD_METHOD              _get_unconnected_pipe
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'pipe'

 L. 356        86  LOAD_FAST                'pipe'
               88  LOAD_CONST               None
               90  COMPARE_OP               is
               92  POP_JUMP_IF_FALSE   100  'to 100'

 L. 357        94  POP_BLOCK        
               96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM            92  '92'

 L. 359       100  LOAD_DEREF               'self'
              102  LOAD_ATTR                _proactor
              104  LOAD_METHOD              accept_pipe
              106  LOAD_FAST                'pipe'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'f'
              112  POP_BLOCK        
              114  JUMP_FORWARD        248  'to 248'
            116_0  COME_FROM_FINALLY     4  '4'

 L. 360       116  DUP_TOP          
              118  LOAD_GLOBAL              OSError
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   214  'to 214'
              124  POP_TOP          
              126  STORE_FAST               'exc'
              128  POP_TOP          
              130  SETUP_FINALLY       202  'to 202'

 L. 361       132  LOAD_FAST                'pipe'
              134  POP_JUMP_IF_FALSE   176  'to 176'
              136  LOAD_FAST                'pipe'
              138  LOAD_METHOD              fileno
              140  CALL_METHOD_0         0  ''
              142  LOAD_CONST               -1
              144  COMPARE_OP               !=
              146  POP_JUMP_IF_FALSE   176  'to 176'

 L. 362       148  LOAD_DEREF               'self'
              150  LOAD_METHOD              call_exception_handler

 L. 363       152  LOAD_STR                 'Pipe accept failed'

 L. 364       154  LOAD_FAST                'exc'

 L. 365       156  LOAD_FAST                'pipe'

 L. 362       158  LOAD_CONST               ('message', 'exception', 'pipe')
              160  BUILD_CONST_KEY_MAP_3     3 
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          

 L. 367       166  LOAD_FAST                'pipe'
              168  LOAD_METHOD              close
              170  CALL_METHOD_0         0  ''
              172  POP_TOP          
              174  JUMP_FORWARD        198  'to 198'
            176_0  COME_FROM           146  '146'
            176_1  COME_FROM           134  '134'

 L. 368       176  LOAD_DEREF               'self'
              178  LOAD_ATTR                _debug
              180  POP_JUMP_IF_FALSE   198  'to 198'

 L. 369       182  LOAD_GLOBAL              logger
              184  LOAD_ATTR                warning
              186  LOAD_STR                 'Accept pipe failed on pipe %r'

 L. 370       188  LOAD_FAST                'pipe'

 L. 370       190  LOAD_CONST               True

 L. 369       192  LOAD_CONST               ('exc_info',)
              194  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              196  POP_TOP          
            198_0  COME_FROM           180  '180'
            198_1  COME_FROM           174  '174'
              198  POP_BLOCK        
              200  BEGIN_FINALLY    
            202_0  COME_FROM_FINALLY   130  '130'
              202  LOAD_CONST               None
              204  STORE_FAST               'exc'
              206  DELETE_FAST              'exc'
              208  END_FINALLY      
              210  POP_EXCEPT       
              212  JUMP_FORWARD        264  'to 264'
            214_0  COME_FROM           122  '122'

 L. 371       214  DUP_TOP          
              216  LOAD_GLOBAL              exceptions
              218  LOAD_ATTR                CancelledError
              220  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   246  'to 246'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 372       230  LOAD_FAST                'pipe'
              232  POP_JUMP_IF_FALSE   242  'to 242'

 L. 373       234  LOAD_FAST                'pipe'
              236  LOAD_METHOD              close
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          
            242_0  COME_FROM           232  '232'
              242  POP_EXCEPT       
              244  JUMP_FORWARD        264  'to 264'
            246_0  COME_FROM           222  '222'
              246  END_FINALLY      
            248_0  COME_FROM           114  '114'

 L. 375       248  LOAD_FAST                'f'
              250  LOAD_DEREF               'server'
              252  STORE_ATTR               _accept_pipe_future

 L. 376       254  LOAD_FAST                'f'
              256  LOAD_METHOD              add_done_callback
              258  LOAD_DEREF               'loop_accept_pipe'
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
            264_0  COME_FROM           244  '244'
            264_1  COME_FROM           212  '212'

Parse error at or near `LOAD_CONST' instruction at offset 48

        self.call_soon(loop_accept_pipe)
        return [server]

    async def _make_subprocess_transport(self, protocol, args, shell, stdin, stdout, stderr, bufsize, extra=None, **kwargs):
        waiter = self.create_future()
        transp = _WindowsSubprocessTransport(self, protocol, args, shell,
 stdin, stdout, stderr, bufsize, waiter=waiter, 
         extra=extra, **kwargs)
        try:
            await waiter
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException:
            transp.close()
            await transp._wait()
            raise
        else:
            return transp


class IocpProactor:
    __doc__ = 'Proactor implementation using IOCP.'

    def __init__(self, concurrency=4294967295):
        self._loop = None
        self._results = []
        self._iocp = _overlapped.CreateIoCompletionPort(_overlapped.INVALID_HANDLE_VALUE, NULL, 0, concurrency)
        self._cache = {}
        self._registered = weakref.WeakSet()
        self._unregistered = []
        self._stopped_serving = weakref.WeakSet()

    def _check_closed(self):
        if self._iocp is None:
            raise RuntimeError('IocpProactor is closed')

    def __repr__(self):
        info = ['overlapped#=%s' % len(self._cache),
         'result#=%s' % len(self._results)]
        if self._iocp is None:
            info.append('closed')
        return '<%s %s>' % (self.__class__.__name__, ' '.join(info))

    def set_loop(self, loop):
        self._loop = loop

    def select(self, timeout=None):
        if not self._results:
            self._poll(timeout)
        tmp = self._results
        self._results = []
        return tmp

    def _result(self, value):
        fut = self._loop.create_future()
        fut.set_result(value)
        return fut

    def recv(self, conn, nbytes, flags=0):
        self._register_with_iocp(conn)
        ov = _overlapped.Overlapped(NULL)
        try:
            if isinstance(conn, socket.socket):
                ov.WSARecv(conn.fileno(), nbytes, flags)
            else:
                ov.ReadFile(conn.fileno(), nbytes)
        except BrokenPipeError:
            return self._result(b'')
        else:

            def finish_recv(trans, key, ov):
                try:
                    return ov.getresult()
                            except OSError as exc:
                    try:
                        if exc.winerror in (_overlapped.ERROR_NETNAME_DELETED,
                         _overlapped.ERROR_OPERATION_ABORTED):
                            raise ConnectionResetError(*exc.args)
                        else:
                            raise
                    finally:
                        exc = None
                        del exc

            return self._register(ov, conn, finish_recv)

    def recv_into(self, conn, buf, flags=0):
        self._register_with_iocp(conn)
        ov = _overlapped.Overlapped(NULL)
        try:
            if isinstance(conn, socket.socket):
                ov.WSARecvInto(conn.fileno(), buf, flags)
            else:
                ov.ReadFileInto(conn.fileno(), buf)
        except BrokenPipeError:
            return self._result(b'')
        else:

            def finish_recv(trans, key, ov):
                try:
                    return ov.getresult()
                            except OSError as exc:
                    try:
                        if exc.winerror in (_overlapped.ERROR_NETNAME_DELETED,
                         _overlapped.ERROR_OPERATION_ABORTED):
                            raise ConnectionResetError(*exc.args)
                        else:
                            raise
                    finally:
                        exc = None
                        del exc

            return self._register(ov, conn, finish_recv)

    def recvfrom(self, conn, nbytes, flags=0):
        self._register_with_iocp(conn)
        ov = _overlapped.Overlapped(NULL)
        try:
            ov.WSARecvFrom(conn.fileno(), nbytes, flags)
        except BrokenPipeError:
            return self._result((b'', None))
        else:

            def finish_recv(trans, key, ov):
                try:
                    return ov.getresult()
                            except OSError as exc:
                    try:
                        if exc.winerror in (_overlapped.ERROR_NETNAME_DELETED,
                         _overlapped.ERROR_OPERATION_ABORTED):
                            raise ConnectionResetError(*exc.args)
                        else:
                            raise
                    finally:
                        exc = None
                        del exc

            return self._register(ov, conn, finish_recv)

    def sendto(self, conn, buf, flags=0, addr=None):
        self._register_with_iocp(conn)
        ov = _overlapped.Overlapped(NULL)
        ov.WSASendTo(conn.fileno(), buf, flags, addr)

        def finish_send(trans, key, ov):
            try:
                return ov.getresult()
                    except OSError as exc:
                try:
                    if exc.winerror in (_overlapped.ERROR_NETNAME_DELETED,
                     _overlapped.ERROR_OPERATION_ABORTED):
                        raise ConnectionResetError(*exc.args)
                    else:
                        raise
                finally:
                    exc = None
                    del exc

        return self._register(ov, conn, finish_send)

    def send(self, conn, buf, flags=0):
        self._register_with_iocp(conn)
        ov = _overlapped.Overlapped(NULL)
        if isinstance(conn, socket.socket):
            ov.WSASend(conn.fileno(), buf, flags)
        else:
            ov.WriteFile(conn.fileno(), buf)

        def finish_send(trans, key, ov):
            try:
                return ov.getresult()
                    except OSError as exc:
                try:
                    if exc.winerror in (_overlapped.ERROR_NETNAME_DELETED,
                     _overlapped.ERROR_OPERATION_ABORTED):
                        raise ConnectionResetError(*exc.args)
                    else:
                        raise
                finally:
                    exc = None
                    del exc

        return self._register(ov, conn, finish_send)

    def accept(self, listener):
        self._register_with_iocp(listener)
        conn = self._get_accept_socket(listener.family)
        ov = _overlapped.Overlapped(NULL)
        ov.AcceptEx(listener.fileno(), conn.fileno())

        def finish_accept(trans, key, ov):
            ov.getresult()
            buf = struct.pack('@P', listener.fileno())
            conn.setsockopt(socket.SOL_SOCKET, _overlapped.SO_UPDATE_ACCEPT_CONTEXT, buf)
            conn.settimeout(listener.gettimeout())
            return (conn, conn.getpeername())

        async def accept_coro(future, conn):
            try:
                await future
            except exceptions.CancelledError:
                conn.close()
                raise

        future = self._register(ov, listener, finish_accept)
        coro = accept_coro(future, conn)
        tasks.ensure_future(coro, loop=(self._loop))
        return future

    def connect(self, conn, address):
        if conn.type == socket.SOCK_DGRAM:
            _overlapped.WSAConnect(conn.fileno(), address)
            fut = self._loop.create_future()
            fut.set_result(None)
            return fut
        self._register_with_iocp(conn)
        try:
            _overlapped.BindLocal(conn.fileno(), conn.family)
        except OSError as e:
            try:
                if e.winerror != errno.WSAEINVAL:
                    raise
                if conn.getsockname()[1] == 0:
                    raise
            finally:
                e = None
                del e

        else:
            ov = _overlapped.Overlapped(NULL)
            ov.ConnectEx(conn.fileno(), address)

            def finish_connect(trans, key, ov):
                ov.getresult()
                conn.setsockopt(socket.SOL_SOCKET, _overlapped.SO_UPDATE_CONNECT_CONTEXT, 0)
                return conn

            return self._register(ov, conn, finish_connect)

    def sendfile(self, sock, file, offset, count):
        self._register_with_iocp(sock)
        ov = _overlapped.Overlapped(NULL)
        offset_low = offset & 4294967295
        offset_high = offset >> 32 & 4294967295
        ov.TransmitFile(sock.fileno(), msvcrt.get_osfhandle(file.fileno()), offset_low, offset_high, count, 0, 0)

        def finish_sendfile(trans, key, ov):
            try:
                return ov.getresult()
                    except OSError as exc:
                try:
                    if exc.winerror in (_overlapped.ERROR_NETNAME_DELETED,
                     _overlapped.ERROR_OPERATION_ABORTED):
                        raise ConnectionResetError(*exc.args)
                    else:
                        raise
                finally:
                    exc = None
                    del exc

        return self._register(ov, sock, finish_sendfile)

    def accept_pipe(self, pipe):
        self._register_with_iocp(pipe)
        ov = _overlapped.Overlapped(NULL)
        connected = ov.ConnectNamedPipe(pipe.fileno())
        if connected:
            return self._result(pipe)

        def finish_accept_pipe(trans, key, ov):
            ov.getresult()
            return pipe

        return self._register(ov, pipe, finish_accept_pipe)

    async def connect_pipe(self, address):
        delay = CONNECT_PIPE_INIT_DELAY
        while True:
            try:
                handle = _overlapped.ConnectPipe(address)
                break
            except OSError as exc:
                try:
                    if exc.winerror != _overlapped.ERROR_PIPE_BUSY:
                        raise
                finally:
                    exc = None
                    del exc

            else:
                delay = min(delay * 2, CONNECT_PIPE_MAX_DELAY)
                await tasks.sleep(delay)

        return windows_utils.PipeHandle(handle)

    def wait_for_handle(self, handle, timeout=None):
        """Wait for a handle.

        Return a Future object. The result of the future is True if the wait
        completed, or False if the wait did not complete (on timeout).
        """
        return self._wait_for_handle(handle, timeout, False)

    def _wait_cancel(self, event, done_callback):
        fut = self._wait_for_handle(event, None, True)
        fut._done_callback = done_callback
        return fut

    def _wait_for_handle(self, handle, timeout, _is_cancel):
        self._check_closed()
        if timeout is None:
            ms = _winapi.INFINITE
        else:
            ms = math.ceil(timeout * 1000.0)
        ov = _overlapped.Overlapped(NULL)
        wait_handle = _overlapped.RegisterWaitWithQueue(handle, self._iocp, ov.address, ms)
        if _is_cancel:
            f = _WaitCancelFuture(ov, handle, wait_handle, loop=(self._loop))
        else:
            f = _WaitHandleFuture(ov, handle, wait_handle, self, loop=(self._loop))
        if f._source_traceback:
            del f._source_traceback[-1]

        def finish_wait_for_handle(trans, key, ov):
            return f._poll()

        self._cache[ov.address] = (
         f, ov, 0, finish_wait_for_handle)
        return f

    def _register_with_iocp(self, obj):
        if obj not in self._registered:
            self._registered.add(obj)
            _overlapped.CreateIoCompletionPort(obj.fileno(), self._iocp, 0, 0)

    def _register(self, ov, obj, callback):
        self._check_closed()
        f = _OverlappedFuture(ov, loop=(self._loop))
        if f._source_traceback:
            del f._source_traceback[-1]
        elif not ov.pending:
            try:
                value = callback(None, None, ov)
            except OSError as e:
                try:
                    f.set_exception(e)
                finally:
                    e = None
                    del e

            else:
                f.set_result(value)
        self._cache[ov.address] = (
         f, ov, obj, callback)
        return f

    def _unregister(self, ov):
        """Unregister an overlapped object.

        Call this method when its future has been cancelled. The event can
        already be signalled (pending in the proactor event queue). It is also
        safe if the event is never signalled (because it was cancelled).
        """
        self._check_closed()
        self._unregistered.append(ov)

    def _get_accept_socket(self, family):
        s = socket.socket(family)
        s.settimeout(0)
        return s

    def _poll--- This code section failed: ---

 L. 767         0  LOAD_FAST                'timeout'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 768         8  LOAD_GLOBAL              INFINITE
               10  STORE_FAST               'ms'
               12  JUMP_FORWARD         62  'to 62'
             14_0  COME_FROM             6  '6'

 L. 769        14  LOAD_FAST                'timeout'
               16  LOAD_CONST               0
               18  COMPARE_OP               <
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 770        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 'negative timeout'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
               30  JUMP_FORWARD         62  'to 62'
             32_0  COME_FROM            20  '20'

 L. 774        32  LOAD_GLOBAL              math
               34  LOAD_METHOD              ceil
               36  LOAD_FAST                'timeout'
               38  LOAD_CONST               1000.0
               40  BINARY_MULTIPLY  
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'ms'

 L. 775        46  LOAD_FAST                'ms'
               48  LOAD_GLOBAL              INFINITE
               50  COMPARE_OP               >=
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 776        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'timeout too big'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM           244  '244'
             62_1  COME_FROM            52  '52'
             62_2  COME_FROM            30  '30'
             62_3  COME_FROM            12  '12'

 L. 779        62  LOAD_GLOBAL              _overlapped
               64  LOAD_METHOD              GetQueuedCompletionStatus
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _iocp
               70  LOAD_FAST                'ms'
               72  CALL_METHOD_2         2  ''
               74  STORE_FAST               'status'

 L. 780        76  LOAD_FAST                'status'
               78  LOAD_CONST               None
               80  COMPARE_OP               is
               82  POP_JUMP_IF_FALSE    88  'to 88'

 L. 781     84_86  BREAK_LOOP          346  'to 346'
             88_0  COME_FROM            82  '82'

 L. 782        88  LOAD_CONST               0
               90  STORE_FAST               'ms'

 L. 784        92  LOAD_FAST                'status'
               94  UNPACK_SEQUENCE_4     4 
               96  STORE_FAST               'err'
               98  STORE_FAST               'transferred'
              100  STORE_FAST               'key'
              102  STORE_FAST               'address'

 L. 785       104  SETUP_FINALLY       130  'to 130'

 L. 786       106  LOAD_FAST                'self'
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
              128  JUMP_FORWARD        218  'to 218'
            130_0  COME_FROM_FINALLY   104  '104'

 L. 787       130  DUP_TOP          
              132  LOAD_GLOBAL              KeyError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   216  'to 216'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 788       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _loop
              148  LOAD_METHOD              get_debug
              150  CALL_METHOD_0         0  ''
              152  POP_JUMP_IF_FALSE   184  'to 184'

 L. 789       154  LOAD_FAST                'self'
              156  LOAD_ATTR                _loop
              158  LOAD_METHOD              call_exception_handler

 L. 790       160  LOAD_STR                 'GetQueuedCompletionStatus() returned an unexpected event'

 L. 792       162  LOAD_STR                 'err=%s transferred=%s key=%#x address=%#x'

 L. 793       164  LOAD_FAST                'err'
              166  LOAD_FAST                'transferred'
              168  LOAD_FAST                'key'
              170  LOAD_FAST                'address'
              172  BUILD_TUPLE_4         4 

 L. 792       174  BINARY_MODULO    

 L. 789       176  LOAD_CONST               ('message', 'status')
              178  BUILD_CONST_KEY_MAP_2     2 
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
            184_0  COME_FROM           152  '152'

 L. 798       184  LOAD_FAST                'key'
              186  LOAD_CONST               0
              188  LOAD_GLOBAL              _overlapped
              190  LOAD_ATTR                INVALID_HANDLE_VALUE
              192  BUILD_TUPLE_2         2 
              194  COMPARE_OP               not-in
              196  POP_JUMP_IF_FALSE   208  'to 208'

 L. 799       198  LOAD_GLOBAL              _winapi
              200  LOAD_METHOD              CloseHandle
              202  LOAD_FAST                'key'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          
            208_0  COME_FROM           196  '196'

 L. 800       208  POP_EXCEPT       
              210  JUMP_BACK            62  'to 62'
              212  POP_EXCEPT       
              214  JUMP_FORWARD        218  'to 218'
            216_0  COME_FROM           136  '136'
              216  END_FINALLY      
            218_0  COME_FROM           214  '214'
            218_1  COME_FROM           128  '128'

 L. 802       218  LOAD_FAST                'obj'
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                _stopped_serving
              224  COMPARE_OP               in
              226  POP_JUMP_IF_FALSE   238  'to 238'

 L. 803       228  LOAD_FAST                'f'
              230  LOAD_METHOD              cancel
              232  CALL_METHOD_0         0  ''
              234  POP_TOP          
              236  JUMP_BACK            62  'to 62'
            238_0  COME_FROM           226  '226'

 L. 806       238  LOAD_FAST                'f'
              240  LOAD_METHOD              done
              242  CALL_METHOD_0         0  ''
              244  POP_JUMP_IF_TRUE     62  'to 62'

 L. 807       246  SETUP_FINALLY       264  'to 264'

 L. 808       248  LOAD_FAST                'callback'
              250  LOAD_FAST                'transferred'
              252  LOAD_FAST                'key'
              254  LOAD_FAST                'ov'
              256  CALL_FUNCTION_3       3  ''
              258  STORE_FAST               'value'
              260  POP_BLOCK        
              262  JUMP_FORWARD        322  'to 322'
            264_0  COME_FROM_FINALLY   246  '246'

 L. 809       264  DUP_TOP          
              266  LOAD_GLOBAL              OSError
              268  COMPARE_OP               exception-match
          270_272  POP_JUMP_IF_FALSE   320  'to 320'
              274  POP_TOP          
              276  STORE_FAST               'e'
              278  POP_TOP          
              280  SETUP_FINALLY       308  'to 308'

 L. 810       282  LOAD_FAST                'f'
              284  LOAD_METHOD              set_exception
              286  LOAD_FAST                'e'
              288  CALL_METHOD_1         1  ''
              290  POP_TOP          

 L. 811       292  LOAD_FAST                'self'
              294  LOAD_ATTR                _results
              296  LOAD_METHOD              append
              298  LOAD_FAST                'f'
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          
              304  POP_BLOCK        
              306  BEGIN_FINALLY    
            308_0  COME_FROM_FINALLY   280  '280'
              308  LOAD_CONST               None
              310  STORE_FAST               'e'
              312  DELETE_FAST              'e'
              314  END_FINALLY      
              316  POP_EXCEPT       
              318  JUMP_BACK            62  'to 62'
            320_0  COME_FROM           270  '270'
              320  END_FINALLY      
            322_0  COME_FROM           262  '262'

 L. 813       322  LOAD_FAST                'f'
              324  LOAD_METHOD              set_result
              326  LOAD_FAST                'value'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          

 L. 814       332  LOAD_FAST                'self'
              334  LOAD_ATTR                _results
              336  LOAD_METHOD              append
              338  LOAD_FAST                'f'
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          
              344  JUMP_BACK            62  'to 62'

 L. 817       346  LOAD_FAST                'self'
              348  LOAD_ATTR                _unregistered
              350  GET_ITER         
              352  FOR_ITER            376  'to 376'
              354  STORE_FAST               'ov'

 L. 818       356  LOAD_FAST                'self'
              358  LOAD_ATTR                _cache
              360  LOAD_METHOD              pop
              362  LOAD_FAST                'ov'
              364  LOAD_ATTR                address
              366  LOAD_CONST               None
              368  CALL_METHOD_2         2  ''
              370  POP_TOP          
          372_374  JUMP_BACK           352  'to 352'

 L. 819       376  LOAD_FAST                'self'
              378  LOAD_ATTR                _unregistered
              380  LOAD_METHOD              clear
              382  CALL_METHOD_0         0  ''
              384  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 212

    def _stop_serving(self, obj):
        self._stopped_serving.add(obj)

    def close(self):
        if self._iocp is None:
            return
        for address, (fut, ov, obj, callback) in list(self._cache.items()):
            if fut.cancelled():
                pass
            elif isinstance(fut, _WaitCancelFuture):
                pass
            else:
                try:
                    fut.cancel()
                except OSError as exc:
                    try:
                        if self._loop is not None:
                            context = {'message':'Cancelling a future failed',  'exception':exc, 
                             'future':fut}
                            if fut._source_traceback:
                                context['source_traceback'] = fut._source_traceback
                            self._loop.call_exception_handler(context)
                    finally:
                        exc = None
                        del exc

        else:
            msg_update = 1.0
            start_time = time.monotonic()
            next_msg = start_time + msg_update
            while self._cache:
                if next_msg <= time.monotonic():
                    logger.debug('%r is running after closing for %.1f seconds', self, time.monotonic() - start_time)
                    next_msg = time.monotonic() + msg_update
                self._poll(msg_update)

            self._results = []
            _winapi.CloseHandle(self._iocp)
            self._iocp = None

    def __del__(self):
        self.close()


class _WindowsSubprocessTransport(base_subprocess.BaseSubprocessTransport):

    def _start(self, args, shell, stdin, stdout, stderr, bufsize, **kwargs):
        self._proc = (windows_utils.Popen)(
 args, shell=shell, 
         stdin=stdin, stdout=stdout, stderr=stderr, bufsize=bufsize, **kwargs)

        def callback(f):
            returncode = self._proc.poll()
            self._process_exited(returncode)

        f = self._loop._proactor.wait_for_handle(int(self._proc._handle))
        f.add_done_callback(callback)


SelectorEventLoop = _WindowsSelectorEventLoop

class WindowsSelectorEventLoopPolicy(events.BaseDefaultEventLoopPolicy):
    _loop_factory = SelectorEventLoop


class WindowsProactorEventLoopPolicy(events.BaseDefaultEventLoopPolicy):
    _loop_factory = ProactorEventLoop


DefaultEventLoopPolicy = WindowsProactorEventLoopPolicy