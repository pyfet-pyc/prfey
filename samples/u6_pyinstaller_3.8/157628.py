# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\base_events.py
"""Base implementation of event loop.

The event loop can be broken up into a multiplexer (the part
responsible for notifying us of I/O events) and the event loop proper,
which wraps a multiplexer with functionality for scheduling callbacks,
immediately or at a given time in the future.

Whenever a public API takes a callback, subsequent positional
arguments will be passed to the callback if/when it is called.  This
avoids the proliferation of trivial lambdas implementing closures.
Keyword arguments for the callback are not supported; this is a
conscious design decision, leaving the door open for keyword arguments
to modify the meaning of the API call itself.
"""
import collections, collections.abc, concurrent.futures, functools, heapq, itertools, os, socket, stat, subprocess, threading, time, traceback, sys, warnings, weakref
try:
    import ssl
except ImportError:
    ssl = None
else:
    from . import constants
    from . import coroutines
    from . import events
    from . import exceptions
    from . import futures
    from . import protocols
    from . import sslproto
    from . import staggered
    from . import tasks
    from . import transports
    from . import trsock
    from .log import logger
    __all__ = ('BaseEventLoop', )
    _MIN_SCHEDULED_TIMER_HANDLES = 100
    _MIN_CANCELLED_TIMER_HANDLES_FRACTION = 0.5
    _HAS_IPv6 = hasattr(socket, 'AF_INET6')
    MAXIMUM_SELECT_TIMEOUT = 86400
    _unset = object()

    def _format_handle(handle):
        cb = handle._callback
        if isinstance(getattr(cb, '__self__', None), tasks.Task):
            return repr(cb.__self__)
        return str(handle)


    def _format_pipe(fd):
        if fd == subprocess.PIPE:
            return '<pipe>'
        if fd == subprocess.STDOUT:
            return '<stdout>'
        return repr(fd)


    def _set_reuseport(sock):
        if not hasattr(socket, 'SO_REUSEPORT'):
            raise ValueError('reuse_port not supported by socket module')
        else:
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except OSError:
                raise ValueError('reuse_port not supported by socket module, SO_REUSEPORT defined but not implemented.')


    def _ipaddr_info--- This code section failed: ---

 L. 106         0  LOAD_GLOBAL              hasattr
                2  LOAD_GLOBAL              socket
                4  LOAD_STR                 'inet_pton'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 107        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 109        14  LOAD_FAST                'proto'
               16  LOAD_CONST               0
               18  LOAD_GLOBAL              socket
               20  LOAD_ATTR                IPPROTO_TCP
               22  LOAD_GLOBAL              socket
               24  LOAD_ATTR                IPPROTO_UDP
               26  BUILD_SET_3           3 
               28  COMPARE_OP               not-in
               30  POP_JUMP_IF_TRUE     40  'to 40'

 L. 110        32  LOAD_FAST                'host'
               34  LOAD_CONST               None
               36  COMPARE_OP               is

 L. 109        38  POP_JUMP_IF_FALSE    44  'to 44'
             40_0  COME_FROM            30  '30'

 L. 111        40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'

 L. 113        44  LOAD_FAST                'type'
               46  LOAD_GLOBAL              socket
               48  LOAD_ATTR                SOCK_STREAM
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 114        54  LOAD_GLOBAL              socket
               56  LOAD_ATTR                IPPROTO_TCP
               58  STORE_FAST               'proto'
               60  JUMP_FORWARD         84  'to 84'
             62_0  COME_FROM            52  '52'

 L. 115        62  LOAD_FAST                'type'
               64  LOAD_GLOBAL              socket
               66  LOAD_ATTR                SOCK_DGRAM
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 116        72  LOAD_GLOBAL              socket
               74  LOAD_ATTR                IPPROTO_UDP
               76  STORE_FAST               'proto'
               78  JUMP_FORWARD         84  'to 84'
             80_0  COME_FROM            70  '70'

 L. 118        80  LOAD_CONST               None
               82  RETURN_VALUE     
             84_0  COME_FROM            78  '78'
             84_1  COME_FROM            60  '60'

 L. 120        84  LOAD_FAST                'port'
               86  LOAD_CONST               None
               88  COMPARE_OP               is
               90  POP_JUMP_IF_FALSE    98  'to 98'

 L. 121        92  LOAD_CONST               0
               94  STORE_FAST               'port'
               96  JUMP_FORWARD        186  'to 186'
             98_0  COME_FROM            90  '90'

 L. 122        98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'port'
              102  LOAD_GLOBAL              bytes
              104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_FALSE   122  'to 122'
              108  LOAD_FAST                'port'
              110  LOAD_CONST               b''
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   122  'to 122'

 L. 123       116  LOAD_CONST               0
              118  STORE_FAST               'port'
              120  JUMP_FORWARD        186  'to 186'
            122_0  COME_FROM           114  '114'
            122_1  COME_FROM           106  '106'

 L. 124       122  LOAD_GLOBAL              isinstance
              124  LOAD_FAST                'port'
              126  LOAD_GLOBAL              str
              128  CALL_FUNCTION_2       2  ''
              130  POP_JUMP_IF_FALSE   146  'to 146'
              132  LOAD_FAST                'port'
              134  LOAD_STR                 ''
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   146  'to 146'

 L. 125       140  LOAD_CONST               0
              142  STORE_FAST               'port'
              144  JUMP_FORWARD        186  'to 186'
            146_0  COME_FROM           138  '138'
            146_1  COME_FROM           130  '130'

 L. 128       146  SETUP_FINALLY       160  'to 160'

 L. 129       148  LOAD_GLOBAL              int
              150  LOAD_FAST                'port'
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'port'
              156  POP_BLOCK        
              158  JUMP_FORWARD        186  'to 186'
            160_0  COME_FROM_FINALLY   146  '146'

 L. 130       160  DUP_TOP          
              162  LOAD_GLOBAL              TypeError
              164  LOAD_GLOBAL              ValueError
              166  BUILD_TUPLE_2         2 
              168  COMPARE_OP               exception-match
              170  POP_JUMP_IF_FALSE   184  'to 184'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 131       178  POP_EXCEPT       
              180  LOAD_CONST               None
              182  RETURN_VALUE     
            184_0  COME_FROM           170  '170'
              184  END_FINALLY      
            186_0  COME_FROM           158  '158'
            186_1  COME_FROM           144  '144'
            186_2  COME_FROM           120  '120'
            186_3  COME_FROM            96  '96'

 L. 133       186  LOAD_FAST                'family'
              188  LOAD_GLOBAL              socket
              190  LOAD_ATTR                AF_UNSPEC
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   222  'to 222'

 L. 134       196  LOAD_GLOBAL              socket
              198  LOAD_ATTR                AF_INET
              200  BUILD_LIST_1          1 
              202  STORE_FAST               'afs'

 L. 135       204  LOAD_GLOBAL              _HAS_IPv6
              206  POP_JUMP_IF_FALSE   228  'to 228'

 L. 136       208  LOAD_FAST                'afs'
              210  LOAD_METHOD              append
              212  LOAD_GLOBAL              socket
              214  LOAD_ATTR                AF_INET6
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          
              220  JUMP_FORWARD        228  'to 228'
            222_0  COME_FROM           194  '194'

 L. 138       222  LOAD_FAST                'family'
              224  BUILD_LIST_1          1 
              226  STORE_FAST               'afs'
            228_0  COME_FROM           220  '220'
            228_1  COME_FROM           206  '206'

 L. 140       228  LOAD_GLOBAL              isinstance
              230  LOAD_FAST                'host'
              232  LOAD_GLOBAL              bytes
              234  CALL_FUNCTION_2       2  ''
              236  POP_JUMP_IF_FALSE   248  'to 248'

 L. 141       238  LOAD_FAST                'host'
              240  LOAD_METHOD              decode
              242  LOAD_STR                 'idna'
              244  CALL_METHOD_1         1  ''
              246  STORE_FAST               'host'
            248_0  COME_FROM           236  '236'

 L. 142       248  LOAD_STR                 '%'
              250  LOAD_FAST                'host'
              252  COMPARE_OP               in
          254_256  POP_JUMP_IF_FALSE   262  'to 262'

 L. 145       258  LOAD_CONST               None
              260  RETURN_VALUE     
            262_0  COME_FROM           254  '254'

 L. 147       262  LOAD_FAST                'afs'
              264  GET_ITER         
              266  FOR_ITER            384  'to 384'
              268  STORE_FAST               'af'

 L. 148       270  SETUP_FINALLY       358  'to 358'

 L. 149       272  LOAD_GLOBAL              socket
              274  LOAD_METHOD              inet_pton
              276  LOAD_FAST                'af'
              278  LOAD_FAST                'host'
              280  CALL_METHOD_2         2  ''
              282  POP_TOP          

 L. 151       284  LOAD_GLOBAL              _HAS_IPv6
          286_288  POP_JUMP_IF_FALSE   330  'to 330'
              290  LOAD_FAST                'af'
              292  LOAD_GLOBAL              socket
              294  LOAD_ATTR                AF_INET6
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_FALSE   330  'to 330'

 L. 152       302  LOAD_FAST                'af'
              304  LOAD_FAST                'type'
              306  LOAD_FAST                'proto'
              308  LOAD_STR                 ''
              310  LOAD_FAST                'host'
              312  LOAD_FAST                'port'
              314  LOAD_FAST                'flowinfo'
              316  LOAD_FAST                'scopeid'
              318  BUILD_TUPLE_4         4 
              320  BUILD_TUPLE_5         5 
              322  POP_BLOCK        
              324  ROT_TWO          
              326  POP_TOP          
              328  RETURN_VALUE     
            330_0  COME_FROM           298  '298'
            330_1  COME_FROM           286  '286'

 L. 154       330  LOAD_FAST                'af'
              332  LOAD_FAST                'type'
              334  LOAD_FAST                'proto'
              336  LOAD_STR                 ''
              338  LOAD_FAST                'host'
              340  LOAD_FAST                'port'
              342  BUILD_TUPLE_2         2 
              344  BUILD_TUPLE_5         5 
              346  POP_BLOCK        
              348  ROT_TWO          
              350  POP_TOP          
              352  RETURN_VALUE     
              354  POP_BLOCK        
              356  JUMP_BACK           266  'to 266'
            358_0  COME_FROM_FINALLY   270  '270'

 L. 155       358  DUP_TOP          
              360  LOAD_GLOBAL              OSError
              362  COMPARE_OP               exception-match
          364_366  POP_JUMP_IF_FALSE   378  'to 378'
              368  POP_TOP          
              370  POP_TOP          
              372  POP_TOP          

 L. 156       374  POP_EXCEPT       
              376  JUMP_BACK           266  'to 266'
            378_0  COME_FROM           364  '364'
              378  END_FINALLY      
          380_382  JUMP_BACK           266  'to 266'

Parse error at or near `ROT_TWO' instruction at offset 324


    def _interleave_addrinfos(addrinfos, first_address_family_count=1):
        """Interleave list of addrinfo tuples by family."""
        addrinfos_by_family = collections.OrderedDict()
        for addr in addrinfos:
            family = addr[0]
            if family not in addrinfos_by_family:
                addrinfos_by_family[family] = []
            addrinfos_by_family[family].appendaddr
        else:
            addrinfos_lists = list(addrinfos_by_family.values())
            reordered = []
            if first_address_family_count > 1:
                reordered.extendaddrinfos_lists[0][:first_address_family_count - 1]
                del addrinfos_lists[0][:first_address_family_count - 1]
            reordered.extend(a for a in itertools.chain.from_iterable(itertools.zip_longest)(*addrinfos_lists) if a is not None)
            return reordered


    def _run_until_complete_cb(fut):
        if not fut.cancelled():
            exc = fut.exception()
            if isinstance(exc, (SystemExit, KeyboardInterrupt)):
                return
        futures._get_loopfut.stop()


    if hasattr(socket, 'TCP_NODELAY'):

        def _set_nodelay(sock):
            if sock.family in {socket.AF_INET, socket.AF_INET6}:
                if sock.type == socket.SOCK_STREAM:
                    if sock.proto == socket.IPPROTO_TCP:
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


    else:

        def _set_nodelay(sock):
            pass


    class _SendfileFallbackProtocol(protocols.Protocol):

        def __init__(self, transp):
            if not isinstance(transp, transports._FlowControlMixin):
                raise TypeError('transport should be _FlowControlMixin instance')
            else:
                self._transport = transp
                self._proto = transp.get_protocol()
                self._should_resume_reading = transp.is_reading()
                self._should_resume_writing = transp._protocol_paused
                transp.pause_reading()
                transp.set_protocolself
                if self._should_resume_writing:
                    self._write_ready_fut = self._transport._loop.create_future()
                else:
                    self._write_ready_fut = None

        async def drain(self):
            if self._transport.is_closing():
                raise ConnectionError('Connection closed by peer')
            fut = self._write_ready_fut
            if fut is None:
                return
            await fut

        def connection_made(self, transport):
            raise RuntimeError('Invalid state: connection should have been established already.')

        def connection_lost(self, exc):
            if self._write_ready_fut is not None:
                if exc is None:
                    self._write_ready_fut.set_exceptionConnectionError('Connection is closed by peer')
                else:
                    self._write_ready_fut.set_exceptionexc
            self._proto.connection_lostexc

        def pause_writing(self):
            if self._write_ready_fut is not None:
                return
            self._write_ready_fut = self._transport._loop.create_future()

        def resume_writing(self):
            if self._write_ready_fut is None:
                return
            self._write_ready_fut.set_resultFalse
            self._write_ready_fut = None

        def data_received(self, data):
            raise RuntimeError('Invalid state: reading should be paused')

        def eof_received(self):
            raise RuntimeError('Invalid state: reading should be paused')

        async def restore(self):
            self._transport.set_protocolself._proto
            if self._should_resume_reading:
                self._transport.resume_reading()
            if self._write_ready_fut is not None:
                self._write_ready_fut.cancel()
            if self._should_resume_writing:
                self._proto.resume_writing()


    class Server(events.AbstractServer):

        def __init__(self, loop, sockets, protocol_factory, ssl_context, backlog, ssl_handshake_timeout):
            self._loop = loop
            self._sockets = sockets
            self._active_count = 0
            self._waiters = []
            self._protocol_factory = protocol_factory
            self._backlog = backlog
            self._ssl_context = ssl_context
            self._ssl_handshake_timeout = ssl_handshake_timeout
            self._serving = False
            self._serving_forever_fut = None

        def __repr__(self):
            return f"<{self.__class__.__name__} sockets={self.sockets!r}>"

        def _attach(self):
            assert self._sockets is not None
            self._active_count += 1

        def _detach(self):
            assert self._active_count > 0
            self._active_count -= 1
            if self._active_count == 0:
                if self._sockets is None:
                    self._wakeup()

        def _wakeup(self):
            waiters = self._waiters
            self._waiters = None
            for waiter in waiters:
                if not waiter.done():
                    waiter.set_resultwaiter

        def _start_serving(self):
            if self._serving:
                return
            self._serving = True
            for sock in self._sockets:
                sock.listenself._backlog
                self._loop._start_serving(self._protocol_factory, sock, self._ssl_context, self, self._backlog, self._ssl_handshake_timeout)

        def get_loop(self):
            return self._loop

        def is_serving(self):
            return self._serving

        @property
        def sockets(self):
            if self._sockets is None:
                return ()
            return tuple((trsock.TransportSockets for s in self._sockets))

        def close(self):
            sockets = self._sockets
            if sockets is None:
                return
            self._sockets = None
            for sock in sockets:
                self._loop._stop_servingsock
            else:
                self._serving = False
                if self._serving_forever_fut is not None:
                    if not self._serving_forever_fut.done():
                        self._serving_forever_fut.cancel()
                        self._serving_forever_fut = None
                if self._active_count == 0:
                    self._wakeup()

        async def start_serving(self):
            self._start_serving()
            await tasks.sleep(0, loop=(self._loop))

        async def serve_forever(self):
            if self._serving_forever_fut is not None:
                raise RuntimeError(f"server {self!r} is already being awaited on serve_forever()")
            if self._sockets is None:
                raise RuntimeError(f"server {self!r} is closed")
            self._start_serving()
            self._serving_forever_fut = self._loop.create_future()
            try:
                try:
                    await self._serving_forever_fut
                except exceptions.CancelledError:
                    try:
                        self.close()
                        await self.wait_closed()
                    finally:
                        raise

            finally:
                self._serving_forever_fut = None

        async def wait_closed(self):
            if self._sockets is None or self._waiters is None:
                return
            waiter = self._loop.create_future()
            self._waiters.appendwaiter
            await waiter


    class BaseEventLoop(events.AbstractEventLoop):

        def __init__(self):
            self._timer_cancelled_count = 0
            self._closed = False
            self._stopping = False
            self._ready = collections.deque()
            self._scheduled = []
            self._default_executor = None
            self._internal_fds = 0
            self._thread_id = None
            self._clock_resolution = time.get_clock_info'monotonic'.resolution
            self._exception_handler = None
            self.set_debugcoroutines._is_debug_mode()
            self.slow_callback_duration = 0.1
            self._current_handle = None
            self._task_factory = None
            self._coroutine_origin_tracking_enabled = False
            self._coroutine_origin_tracking_saved_depth = None
            self._asyncgens = weakref.WeakSet()
            self._asyncgens_shutdown_called = False

        def __repr__(self):
            return f"<{self.__class__.__name__} running={self.is_running()} closed={self.is_closed()} debug={self.get_debug()}>"

        def create_future(self):
            """Create a Future object attached to the loop."""
            return futures.Future(loop=self)

        def create_task(self, coro, *, name=None):
            """Schedule a coroutine object.

        Return a task object.
        """
            self._check_closed()
            if self._task_factory is None:
                task = tasks.Task(coro, loop=self, name=name)
                if task._source_traceback:
                    del task._source_traceback[-1]
            else:
                task = self._task_factoryselfcoro
                tasks._set_task_nametaskname
            return task

        def set_task_factory(self, factory):
            """Set a task factory that will be used by loop.create_task().

        If factory is None the default task factory will be set.

        If factory is a callable, it should have a signature matching
        '(loop, coro)', where 'loop' will be a reference to the active
        event loop, 'coro' will be a coroutine object.  The callable
        must return a Future.
        """
            if factory is not None:
                if not callable(factory):
                    raise TypeError('task factory must be a callable or None')
            self._task_factory = factory

        def get_task_factory(self):
            """Return a task factory, or None if the default one is in use."""
            return self._task_factory

        def _make_socket_transport(self, sock, protocol, waiter=None, *, extra=None, server=None):
            """Create socket transport."""
            raise NotImplementedError

        def _make_ssl_transport(self, rawsock, protocol, sslcontext, waiter=None, *, server_side=False, server_hostname=None, extra=None, server=None, ssl_handshake_timeout=None, call_connection_made=True):
            """Create SSL transport."""
            raise NotImplementedError

        def _make_datagram_transport(self, sock, protocol, address=None, waiter=None, extra=None):
            """Create datagram transport."""
            raise NotImplementedError

        def _make_read_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
            """Create read pipe transport."""
            raise NotImplementedError

        def _make_write_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
            """Create write pipe transport."""
            raise NotImplementedError

        async def _make_subprocess_transport(self, protocol, args, shell, stdin, stdout, stderr, bufsize, extra=None, **kwargs):
            """Create subprocess transport."""
            raise NotImplementedError

        def _write_to_self(self):
            """Write a byte to self-pipe, to wake up the event loop.

        This may be called from a different thread.

        The subclass is responsible for implementing the self-pipe.
        """
            raise NotImplementedError

        def _process_events(self, event_list):
            """Process selector events."""
            raise NotImplementedError

        def _check_closed(self):
            if self._closed:
                raise RuntimeError('Event loop is closed')

        def _asyncgen_finalizer_hook(self, agen):
            self._asyncgens.discardagen
            if not self.is_closed():
                self.call_soon_threadsafeself.create_taskagen.aclose()

        def _asyncgen_firstiter_hook(self, agen):
            if self._asyncgens_shutdown_called:
                warnings.warn(f"asynchronous generator {agen!r} was scheduled after loop.shutdown_asyncgens() call",
                  ResourceWarning,
                  source=self)
            self._asyncgens.addagen

        async def shutdown_asyncgens(self):
            """Shutdown all active asynchronous generators."""
            self._asyncgens_shutdown_called = True
            if not len(self._asyncgens):
                return
            closing_agens = list(self._asyncgens)
            self._asyncgens.clear()
            results = await (tasks.gather)(*[ag.aclose() for ag in closing_agens], return_exceptions=True, 
             loop=self)
            for result, agen in zip(results, closing_agens):
                if isinstance(result, Exception):
                    self.call_exception_handler{'message':f"an error occurred during closing of asynchronous generator {agen!r}", 
                     'exception':result, 
                     'asyncgen':agen}

        def run_forever(self):
            """Run until stop() is called."""
            self._check_closed()
            if self.is_running():
                raise RuntimeError('This event loop is already running')
            if events._get_running_loop() is not None:
                raise RuntimeError('Cannot run the event loop while another loop is running')
            self._set_coroutine_origin_trackingself._debug
            self._thread_id = threading.get_ident()
            old_agen_hooks = sys.get_asyncgen_hooks()
            sys.set_asyncgen_hooks(firstiter=(self._asyncgen_firstiter_hook), finalizer=(self._asyncgen_finalizer_hook))
            try:
                events._set_running_loopself
                while True:
                    self._run_once()
                    if self._stopping:
                        break

            finally:
                self._stopping = False
                self._thread_id = None
                events._set_running_loopNone
                self._set_coroutine_origin_trackingFalse
                (sys.set_asyncgen_hooks)(*old_agen_hooks)

        def run_until_complete(self, future):
            """Run until the Future is done.

        If the argument is a coroutine, it is wrapped in a Task.

        WARNING: It would be disastrous to call run_until_complete()
        with the same coroutine twice -- it would wrap it in two
        different Tasks and that can't be good.

        Return the Future's result, or raise its exception.
        """
            self._check_closed()
            new_task = not futures.isfuturefuture
            future = tasks.ensure_future(future, loop=self)
            if new_task:
                future._log_destroy_pending = False
            future.add_done_callback_run_until_complete_cb
            try:
                try:
                    self.run_forever()
                except:
                    if new_task:
                        if future.done():
                            if not future.cancelled():
                                future.exception()
                    raise

            finally:
                future.remove_done_callback_run_until_complete_cb

            if not future.done():
                raise RuntimeError('Event loop stopped before Future completed.')
            return future.result()

        def stop(self):
            """Stop running the event loop.

        Every callback already scheduled will still run.  This simply informs
        run_forever to stop looping after a complete iteration.
        """
            self._stopping = True

        def close(self):
            """Close the event loop.

        This clears the queues and shuts down the executor,
        but does not wait for the executor to finish.

        The event loop must not be running.
        """
            if self.is_running():
                raise RuntimeError('Cannot close a running event loop')
            if self._closed:
                return
            if self._debug:
                logger.debug'Close %r'self
            self._closed = True
            self._ready.clear()
            self._scheduled.clear()
            executor = self._default_executor
            if executor is not None:
                self._default_executor = None
                executor.shutdown(wait=False)

        def is_closed(self):
            """Returns True if the event loop was closed."""
            return self._closed

        def __del__(self, _warn=warnings.warn):
            if not self.is_closed():
                _warn(f"unclosed event loop {self!r}", ResourceWarning, source=self)
                if not self.is_running():
                    self.close()

        def is_running(self):
            """Returns True if the event loop is running."""
            return self._thread_id is not None

        def time(self):
            """Return the time according to the event loop's clock.

        This is a float expressed in seconds since an epoch, but the
        epoch, precision, accuracy and drift are unspecified and may
        differ per event loop.
        """
            return time.monotonic()

        def call_later(self, delay, callback, *args, context=None):
            """Arrange for a callback to be called at a given time.

        Return a Handle: an opaque object with a cancel() method that
        can be used to cancel the call.

        The delay can be an int or float, expressed in seconds.  It is
        always relative to the current time.

        Each callback will be called exactly once.  If two callbacks
        are scheduled for exactly the same time, it undefined which
        will be called first.

        Any positional arguments after the callback will be passed to
        the callback when it is called.
        """
            timer = (self.call_at)(self.time() + delay, callback, *args, **{'context': context})
            if timer._source_traceback:
                del timer._source_traceback[-1]
            return timer

        def call_at(self, when, callback, *args, context=None):
            """Like call_later(), but uses an absolute time.

        Absolute time corresponds to the event loop's time() method.
        """
            self._check_closed()
            if self._debug:
                self._check_thread()
                self._check_callbackcallback'call_at'
            timer = events.TimerHandle(when, callback, args, self, context)
            if timer._source_traceback:
                del timer._source_traceback[-1]
            heapq.heappushself._scheduledtimer
            timer._scheduled = True
            return timer

        def call_soon(self, callback, *args, context=None):
            """Arrange for a callback to be called as soon as possible.

        This operates as a FIFO queue: callbacks are called in the
        order in which they are registered.  Each callback will be
        called exactly once.

        Any positional arguments after the callback will be passed to
        the callback when it is called.
        """
            self._check_closed()
            if self._debug:
                self._check_thread()
                self._check_callbackcallback'call_soon'
            handle = self._call_soon(callback, args, context)
            if handle._source_traceback:
                del handle._source_traceback[-1]
            return handle

        def _check_callback(self, callback, method):
            if coroutines.iscoroutinecallback or coroutines.iscoroutinefunctioncallback:
                raise TypeError(f"coroutines cannot be used with {method}()")
            if not callable(callback):
                raise TypeError(f"a callable object was expected by {method}(), got {callback!r}")

        def _call_soon(self, callback, args, context):
            handle = events.Handle(callback, args, self, context)
            if handle._source_traceback:
                del handle._source_traceback[-1]
            self._ready.appendhandle
            return handle

        def _check_thread(self):
            """Check that the current thread is the thread running the event loop.

        Non-thread-safe methods of this class make this assumption and will
        likely behave incorrectly when the assumption is violated.

        Should only be called when (self._debug == True).  The caller is
        responsible for checking this condition for performance reasons.
        """
            if self._thread_id is None:
                return
            thread_id = threading.get_ident()
            if thread_id != self._thread_id:
                raise RuntimeError('Non-thread-safe operation invoked on an event loop other than the current one')

        def call_soon_threadsafe(self, callback, *args, context=None):
            """Like call_soon(), but thread-safe."""
            self._check_closed()
            if self._debug:
                self._check_callbackcallback'call_soon_threadsafe'
            handle = self._call_soon(callback, args, context)
            if handle._source_traceback:
                del handle._source_traceback[-1]
            self._write_to_self()
            return handle

        def run_in_executor(self, executor, func, *args):
            self._check_closed()
            if self._debug:
                self._check_callbackfunc'run_in_executor'
            if executor is None:
                executor = self._default_executor
                if executor is None:
                    executor = concurrent.futures.ThreadPoolExecutor()
                    self._default_executor = executor
            return futures.wrap_future((executor.submit)(func, *args),
              loop=self)

        def set_default_executor(self, executor):
            if not isinstance(executor, concurrent.futures.ThreadPoolExecutor):
                warnings.warn('Using the default executor that is not an instance of ThreadPoolExecutor is deprecated and will be prohibited in Python 3.9', DeprecationWarning, 2)
            self._default_executor = executor

        def _getaddrinfo_debug(self, host, port, family, type, proto, flags):
            msg = [
             f"{host}:{port!r}"]
            if family:
                msg.appendf"family={family!r}"
            else:
                if type:
                    msg.appendf"type={type!r}"
                if proto:
                    msg.appendf"proto={proto!r}"
                if flags:
                    msg.appendf"flags={flags!r}"
                msg = ', '.joinmsg
                logger.debug'Get address info %s'msg
                t0 = self.time()
                addrinfo = socket.getaddrinfo(host, port, family, type, proto, flags)
                dt = self.time() - t0
                msg = f"Getting address info {msg} took {dt * 1000.0:.3f}ms: {addrinfo!r}"
                if dt >= self.slow_callback_duration:
                    logger.infomsg
                else:
                    logger.debugmsg
            return addrinfo

        async def getaddrinfo(self, host, port, *, family=0, type=0, proto=0, flags=0):
            if self._debug:
                getaddr_func = self._getaddrinfo_debug
            else:
                getaddr_func = socket.getaddrinfo
            return await self.run_in_executor(None, getaddr_func, host, port, family, type, proto, flags)

        async def getnameinfo(self, sockaddr, flags=0):
            return await self.run_in_executor(None, socket.getnameinfo, sockaddr, flags)

        async def sock_sendfile(self, sock, file, offset=0, count=None, *, fallback=True):
            if self._debug:
                if sock.gettimeout() != 0:
                    raise ValueError('the socket must be non-blocking')
            self._check_sendfile_params(sock, file, offset, count)
            try:
                return await self._sock_sendfile_native(sock, file, offset, count)
                    except exceptions.SendfileNotAvailableError as exc:
                try:
                    if not fallback:
                        raise
                finally:
                    exc = None
                    del exc

            return await self._sock_sendfile_fallback(sock, file, offset, count)

        async def _sock_sendfile_native(self, sock, file, offset, count):
            raise exceptions.SendfileNotAvailableErrorf"syscall sendfile is not available for socket {sock!r} and file {{file!r}} combination"

        async def _sock_sendfile_fallback--- This code section failed: ---

 L. 850         0  LOAD_FAST                'offset'
                2  POP_JUMP_IF_FALSE    14  'to 14'

 L. 851         4  LOAD_FAST                'file'
                6  LOAD_METHOD              seek
                8  LOAD_FAST                'offset'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
             14_0  COME_FROM             2  '2'

 L. 854        14  LOAD_FAST                'count'

 L. 853        16  POP_JUMP_IF_FALSE    30  'to 30'
               18  LOAD_GLOBAL              min
               20  LOAD_FAST                'count'
               22  LOAD_GLOBAL              constants
               24  LOAD_ATTR                SENDFILE_FALLBACK_READBUFFER_SIZE
               26  CALL_FUNCTION_2       2  ''
               28  JUMP_FORWARD         34  'to 34'
             30_0  COME_FROM            16  '16'

 L. 854        30  LOAD_GLOBAL              constants
               32  LOAD_ATTR                SENDFILE_FALLBACK_READBUFFER_SIZE
             34_0  COME_FROM            28  '28'

 L. 852        34  STORE_FAST               'blocksize'

 L. 856        36  LOAD_GLOBAL              bytearray
               38  LOAD_FAST                'blocksize'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'buf'

 L. 857        44  LOAD_CONST               0
               46  STORE_FAST               'total_sent'

 L. 858        48  SETUP_FINALLY       166  'to 166'

 L. 860        50  LOAD_FAST                'count'
               52  POP_JUMP_IF_FALSE    78  'to 78'

 L. 861        54  LOAD_GLOBAL              min
               56  LOAD_FAST                'count'
               58  LOAD_FAST                'total_sent'
               60  BINARY_SUBTRACT  
               62  LOAD_FAST                'blocksize'
               64  CALL_FUNCTION_2       2  ''
               66  STORE_FAST               'blocksize'

 L. 862        68  LOAD_FAST                'blocksize'
               70  LOAD_CONST               0
               72  COMPARE_OP               <=
               74  POP_JUMP_IF_FALSE    78  'to 78'

 L. 863        76  BREAK_LOOP          158  'to 158'
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            52  '52'

 L. 864        78  LOAD_GLOBAL              memoryview
               80  LOAD_FAST                'buf'
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_CONST               None
               86  LOAD_FAST                'blocksize'
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  STORE_FAST               'view'

 L. 865        94  LOAD_FAST                'self'
               96  LOAD_METHOD              run_in_executor
               98  LOAD_CONST               None
              100  LOAD_FAST                'file'
              102  LOAD_ATTR                readinto
              104  LOAD_FAST                'view'
              106  CALL_METHOD_3         3  ''
              108  GET_AWAITABLE    
              110  LOAD_CONST               None
              112  YIELD_FROM       
              114  STORE_FAST               'read'

 L. 866       116  LOAD_FAST                'read'
              118  POP_JUMP_IF_TRUE    122  'to 122'

 L. 867       120  BREAK_LOOP          158  'to 158'
            122_0  COME_FROM           118  '118'

 L. 868       122  LOAD_FAST                'self'
              124  LOAD_METHOD              sock_sendall
              126  LOAD_FAST                'sock'
              128  LOAD_FAST                'view'
              130  LOAD_CONST               None
              132  LOAD_FAST                'read'
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  CALL_METHOD_2         2  ''
              140  GET_AWAITABLE    
              142  LOAD_CONST               None
              144  YIELD_FROM       
              146  POP_TOP          

 L. 869       148  LOAD_FAST                'total_sent'
              150  LOAD_FAST                'read'
              152  INPLACE_ADD      
              154  STORE_FAST               'total_sent'
              156  JUMP_BACK            50  'to 50'

 L. 870       158  LOAD_FAST                'total_sent'
              160  POP_BLOCK        
              162  CALL_FINALLY        166  'to 166'
              164  RETURN_VALUE     
            166_0  COME_FROM           162  '162'
            166_1  COME_FROM_FINALLY    48  '48'

 L. 872       166  LOAD_FAST                'total_sent'
              168  LOAD_CONST               0
              170  COMPARE_OP               >
              172  POP_JUMP_IF_FALSE   198  'to 198'
              174  LOAD_GLOBAL              hasattr
              176  LOAD_FAST                'file'
              178  LOAD_STR                 'seek'
              180  CALL_FUNCTION_2       2  ''
              182  POP_JUMP_IF_FALSE   198  'to 198'

 L. 873       184  LOAD_FAST                'file'
              186  LOAD_METHOD              seek
              188  LOAD_FAST                'offset'
              190  LOAD_FAST                'total_sent'
              192  BINARY_ADD       
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          
            198_0  COME_FROM           182  '182'
            198_1  COME_FROM           172  '172'
              198  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 162

        def _check_sendfile_params(self, sock, file, offset, count):
            if 'b' not in getattr(file, 'mode', 'b'):
                raise ValueError('file should be opened in binary mode')
            else:
                if not sock.type == socket.SOCK_STREAM:
                    raise ValueError('only SOCK_STREAM type sockets are supported')
                if count is not None:
                    if not isinstance(count, int):
                        raise TypeError('count must be a positive integer (got {!r})'.formatcount)
                    if count <= 0:
                        raise ValueError('count must be a positive integer (got {!r})'.formatcount)
                assert isinstance(offset, int), 'offset must be a non-negative integer (got {!r})'.formatoffset
            if offset < 0:
                raise ValueError('offset must be a non-negative integer (got {!r})'.formatoffset)

        async def _connect_sock--- This code section failed: ---

 L. 898         0  BUILD_LIST_0          0 
                2  STORE_FAST               'my_exceptions'

 L. 899         4  LOAD_FAST                'exceptions'
                6  LOAD_METHOD              append
                8  LOAD_FAST                'my_exceptions'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          

 L. 900        14  LOAD_FAST                'addr_info'
               16  UNPACK_SEQUENCE_5     5 
               18  STORE_FAST               'family'
               20  STORE_FAST               'type_'
               22  STORE_FAST               'proto'
               24  STORE_FAST               '_'
               26  STORE_FAST               'address'

 L. 901        28  LOAD_CONST               None
               30  STORE_FAST               'sock'

 L. 902        32  SETUP_FINALLY       220  'to 220'

 L. 903        34  LOAD_GLOBAL              socket
               36  LOAD_ATTR                socket
               38  LOAD_FAST                'family'
               40  LOAD_FAST                'type_'
               42  LOAD_FAST                'proto'
               44  LOAD_CONST               ('family', 'type', 'proto')
               46  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               48  STORE_FAST               'sock'

 L. 904        50  LOAD_FAST                'sock'
               52  LOAD_METHOD              setblocking
               54  LOAD_CONST               False
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 905        60  LOAD_FAST                'local_addr_infos'
               62  LOAD_CONST               None
               64  COMPARE_OP               is-not
               66  POP_JUMP_IF_FALSE   196  'to 196'

 L. 906        68  LOAD_FAST                'local_addr_infos'
               70  GET_ITER         
               72  FOR_ITER            188  'to 188'
               74  UNPACK_SEQUENCE_5     5 
               76  STORE_FAST               '_'
               78  STORE_FAST               '_'
               80  STORE_FAST               '_'
               82  STORE_FAST               '_'
               84  STORE_FAST               'laddr'

 L. 907        86  SETUP_FINALLY       108  'to 108'

 L. 908        88  LOAD_FAST                'sock'
               90  LOAD_METHOD              bind
               92  LOAD_FAST                'laddr'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 909        98  POP_BLOCK        
              100  POP_TOP          
              102  JUMP_ABSOLUTE       196  'to 196'
              104  POP_BLOCK        
              106  JUMP_BACK            72  'to 72'
            108_0  COME_FROM_FINALLY    86  '86'

 L. 910       108  DUP_TOP          
              110  LOAD_GLOBAL              OSError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   184  'to 184'
              116  POP_TOP          
              118  STORE_FAST               'exc'
              120  POP_TOP          
              122  SETUP_FINALLY       172  'to 172'

 L. 912       124  LOAD_STR                 'error while attempting to bind on address '
              126  LOAD_FAST                'laddr'
              128  FORMAT_VALUE          2  '!r'
              130  LOAD_STR                 ': '
              132  LOAD_FAST                'exc'
              134  LOAD_ATTR                strerror
              136  LOAD_METHOD              lower
              138  CALL_METHOD_0         0  ''
              140  FORMAT_VALUE          0  ''
              142  BUILD_STRING_4        4 

 L. 911       144  STORE_FAST               'msg'

 L. 916       146  LOAD_GLOBAL              OSError
              148  LOAD_FAST                'exc'
              150  LOAD_ATTR                errno
              152  LOAD_FAST                'msg'
              154  CALL_FUNCTION_2       2  ''
              156  STORE_FAST               'exc'

 L. 917       158  LOAD_FAST                'my_exceptions'
              160  LOAD_METHOD              append
              162  LOAD_FAST                'exc'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
              168  POP_BLOCK        
              170  BEGIN_FINALLY    
            172_0  COME_FROM_FINALLY   122  '122'
              172  LOAD_CONST               None
              174  STORE_FAST               'exc'
              176  DELETE_FAST              'exc'
              178  END_FINALLY      
              180  POP_EXCEPT       
              182  JUMP_BACK            72  'to 72'
            184_0  COME_FROM           114  '114'
              184  END_FINALLY      
              186  JUMP_BACK            72  'to 72'

 L. 919       188  LOAD_FAST                'my_exceptions'
              190  LOAD_METHOD              pop
              192  CALL_METHOD_0         0  ''
              194  RAISE_VARARGS_1       1  'exception instance'
            196_0  COME_FROM            66  '66'

 L. 920       196  LOAD_FAST                'self'
              198  LOAD_METHOD              sock_connect
              200  LOAD_FAST                'sock'
              202  LOAD_FAST                'address'
              204  CALL_METHOD_2         2  ''
              206  GET_AWAITABLE    
              208  LOAD_CONST               None
              210  YIELD_FROM       
              212  POP_TOP          

 L. 921       214  LOAD_FAST                'sock'
              216  POP_BLOCK        
              218  RETURN_VALUE     
            220_0  COME_FROM_FINALLY    32  '32'

 L. 922       220  DUP_TOP          
              222  LOAD_GLOBAL              OSError
              224  COMPARE_OP               exception-match
          226_228  POP_JUMP_IF_FALSE   284  'to 284'
              230  POP_TOP          
              232  STORE_FAST               'exc'
              234  POP_TOP          
              236  SETUP_FINALLY       272  'to 272'

 L. 923       238  LOAD_FAST                'my_exceptions'
              240  LOAD_METHOD              append
              242  LOAD_FAST                'exc'
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 924       248  LOAD_FAST                'sock'
              250  LOAD_CONST               None
              252  COMPARE_OP               is-not
          254_256  POP_JUMP_IF_FALSE   266  'to 266'

 L. 925       258  LOAD_FAST                'sock'
              260  LOAD_METHOD              close
              262  CALL_METHOD_0         0  ''
              264  POP_TOP          
            266_0  COME_FROM           254  '254'

 L. 926       266  RAISE_VARARGS_0       0  'reraise'
              268  POP_BLOCK        
              270  BEGIN_FINALLY    
            272_0  COME_FROM_FINALLY   236  '236'
              272  LOAD_CONST               None
              274  STORE_FAST               'exc'
              276  DELETE_FAST              'exc'
              278  END_FINALLY      
              280  POP_EXCEPT       
              282  JUMP_FORWARD        316  'to 316'
            284_0  COME_FROM           226  '226'

 L. 927       284  POP_TOP          
              286  POP_TOP          
              288  POP_TOP          

 L. 928       290  LOAD_FAST                'sock'
              292  LOAD_CONST               None
              294  COMPARE_OP               is-not
          296_298  POP_JUMP_IF_FALSE   308  'to 308'

 L. 929       300  LOAD_FAST                'sock'
              302  LOAD_METHOD              close
              304  CALL_METHOD_0         0  ''
              306  POP_TOP          
            308_0  COME_FROM           296  '296'

 L. 930       308  RAISE_VARARGS_0       0  'reraise'
              310  POP_EXCEPT       
              312  JUMP_FORWARD        316  'to 316'
              314  END_FINALLY      
            316_0  COME_FROM           312  '312'
            316_1  COME_FROM           282  '282'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 102

        async def create_connection--- This code section failed: ---

 L. 950         0  LOAD_FAST                'server_hostname'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    20  'to 20'
                8  LOAD_FAST                'ssl'
               10  POP_JUMP_IF_TRUE     20  'to 20'

 L. 951        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 'server_hostname is only meaningful with ssl'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'
             20_1  COME_FROM             6  '6'

 L. 953        20  LOAD_FAST                'server_hostname'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    48  'to 48'
               28  LOAD_FAST                'ssl'
               30  POP_JUMP_IF_FALSE    48  'to 48'

 L. 964        32  LOAD_FAST                'host'
               34  POP_JUMP_IF_TRUE     44  'to 44'

 L. 965        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'You must set server_hostname when using ssl without a host'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 967        44  LOAD_FAST                'host'
               46  STORE_FAST               'server_hostname'
             48_0  COME_FROM            30  '30'
             48_1  COME_FROM            26  '26'

 L. 969        48  LOAD_FAST                'ssl_handshake_timeout'
               50  LOAD_CONST               None
               52  COMPARE_OP               is-not
               54  POP_JUMP_IF_FALSE    68  'to 68'
               56  LOAD_FAST                'ssl'
               58  POP_JUMP_IF_TRUE     68  'to 68'

 L. 970        60  LOAD_GLOBAL              ValueError

 L. 971        62  LOAD_STR                 'ssl_handshake_timeout is only meaningful with ssl'

 L. 970        64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'
             68_1  COME_FROM            54  '54'

 L. 973        68  LOAD_FAST                'happy_eyeballs_delay'
               70  LOAD_CONST               None
               72  COMPARE_OP               is-not
               74  POP_JUMP_IF_FALSE    88  'to 88'
               76  LOAD_FAST                'interleave'
               78  LOAD_CONST               None
               80  COMPARE_OP               is
               82  POP_JUMP_IF_FALSE    88  'to 88'

 L. 975        84  LOAD_CONST               1
               86  STORE_FAST               'interleave'
             88_0  COME_FROM            82  '82'
             88_1  COME_FROM            74  '74'

 L. 977        88  LOAD_FAST                'host'
               90  LOAD_CONST               None
               92  COMPARE_OP               is-not
               94  POP_JUMP_IF_TRUE    106  'to 106'
               96  LOAD_FAST                'port'
               98  LOAD_CONST               None
              100  COMPARE_OP               is-not
          102_104  POP_JUMP_IF_FALSE   498  'to 498'
            106_0  COME_FROM            94  '94'

 L. 978       106  LOAD_FAST                'sock'
              108  LOAD_CONST               None
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 979       114  LOAD_GLOBAL              ValueError

 L. 980       116  LOAD_STR                 'host/port and sock can not be specified at the same time'

 L. 979       118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'

 L. 982       122  LOAD_DEREF               'self'
              124  LOAD_ATTR                _ensure_resolved

 L. 983       126  LOAD_FAST                'host'
              128  LOAD_FAST                'port'
              130  BUILD_TUPLE_2         2 

 L. 983       132  LOAD_FAST                'family'

 L. 984       134  LOAD_GLOBAL              socket
              136  LOAD_ATTR                SOCK_STREAM

 L. 984       138  LOAD_FAST                'proto'

 L. 984       140  LOAD_FAST                'flags'

 L. 984       142  LOAD_DEREF               'self'

 L. 982       144  LOAD_CONST               ('family', 'type', 'proto', 'flags', 'loop')
              146  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              148  GET_AWAITABLE    
              150  LOAD_CONST               None
              152  YIELD_FROM       
              154  STORE_FAST               'infos'

 L. 985       156  LOAD_FAST                'infos'
              158  POP_JUMP_IF_TRUE    168  'to 168'

 L. 986       160  LOAD_GLOBAL              OSError
              162  LOAD_STR                 'getaddrinfo() returned empty list'
              164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
            168_0  COME_FROM           158  '158'

 L. 988       168  LOAD_FAST                'local_addr'
              170  LOAD_CONST               None
              172  COMPARE_OP               is-not
              174  POP_JUMP_IF_FALSE   220  'to 220'

 L. 989       176  LOAD_DEREF               'self'
              178  LOAD_ATTR                _ensure_resolved

 L. 990       180  LOAD_FAST                'local_addr'

 L. 990       182  LOAD_FAST                'family'

 L. 991       184  LOAD_GLOBAL              socket
              186  LOAD_ATTR                SOCK_STREAM

 L. 991       188  LOAD_FAST                'proto'

 L. 992       190  LOAD_FAST                'flags'

 L. 992       192  LOAD_DEREF               'self'

 L. 989       194  LOAD_CONST               ('family', 'type', 'proto', 'flags', 'loop')
              196  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              198  GET_AWAITABLE    
              200  LOAD_CONST               None
              202  YIELD_FROM       
              204  STORE_DEREF              'laddr_infos'

 L. 993       206  LOAD_DEREF               'laddr_infos'
              208  POP_JUMP_IF_TRUE    224  'to 224'

 L. 994       210  LOAD_GLOBAL              OSError
              212  LOAD_STR                 'getaddrinfo() returned empty list'
              214  CALL_FUNCTION_1       1  ''
              216  RAISE_VARARGS_1       1  'exception instance'
              218  JUMP_FORWARD        224  'to 224'
            220_0  COME_FROM           174  '174'

 L. 996       220  LOAD_CONST               None
              222  STORE_DEREF              'laddr_infos'
            224_0  COME_FROM           218  '218'
            224_1  COME_FROM           208  '208'

 L. 998       224  LOAD_FAST                'interleave'
              226  POP_JUMP_IF_FALSE   238  'to 238'

 L. 999       228  LOAD_GLOBAL              _interleave_addrinfos
              230  LOAD_FAST                'infos'
              232  LOAD_FAST                'interleave'
              234  CALL_FUNCTION_2       2  ''
              236  STORE_FAST               'infos'
            238_0  COME_FROM           226  '226'

 L.1001       238  BUILD_LIST_0          0 
              240  STORE_DEREF              'exceptions'

 L.1002       242  LOAD_FAST                'happy_eyeballs_delay'
              244  LOAD_CONST               None
              246  COMPARE_OP               is
          248_250  POP_JUMP_IF_FALSE   328  'to 328'

 L.1004       252  LOAD_FAST                'infos'
              254  GET_ITER         
              256  FOR_ITER            326  'to 326'
              258  STORE_FAST               'addrinfo'

 L.1005       260  SETUP_FINALLY       294  'to 294'

 L.1006       262  LOAD_DEREF               'self'
              264  LOAD_METHOD              _connect_sock

 L.1007       266  LOAD_DEREF               'exceptions'

 L.1007       268  LOAD_FAST                'addrinfo'

 L.1007       270  LOAD_DEREF               'laddr_infos'

 L.1006       272  CALL_METHOD_3         3  ''
              274  GET_AWAITABLE    
              276  LOAD_CONST               None
              278  YIELD_FROM       
              280  STORE_FAST               'sock'

 L.1008       282  POP_BLOCK        
              284  POP_TOP          
          286_288  JUMP_ABSOLUTE       374  'to 374'
              290  POP_BLOCK        
              292  JUMP_BACK           256  'to 256'
            294_0  COME_FROM_FINALLY   260  '260'

 L.1009       294  DUP_TOP          
              296  LOAD_GLOBAL              OSError
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   320  'to 320'
              304  POP_TOP          
              306  POP_TOP          
              308  POP_TOP          

 L.1010       310  POP_EXCEPT       
          312_314  JUMP_BACK           256  'to 256'
              316  POP_EXCEPT       
              318  JUMP_BACK           256  'to 256'
            320_0  COME_FROM           300  '300'
              320  END_FINALLY      
          322_324  JUMP_BACK           256  'to 256'
              326  JUMP_FORWARD        374  'to 374'
            328_0  COME_FROM           248  '248'

 L.1012       328  LOAD_GLOBAL              staggered
              330  LOAD_ATTR                staggered_race

 L.1013       332  LOAD_CLOSURE             'exceptions'
              334  LOAD_CLOSURE             'laddr_infos'
              336  LOAD_CLOSURE             'self'
              338  BUILD_TUPLE_3         3 
              340  LOAD_GENEXPR             '<code_object <genexpr>>'
              342  LOAD_STR                 'BaseEventLoop.create_connection.<locals>.<genexpr>'
              344  MAKE_FUNCTION_8          'closure'

 L.1015       346  LOAD_FAST                'infos'

 L.1013       348  GET_ITER         
              350  CALL_FUNCTION_1       1  ''

 L.1016       352  LOAD_FAST                'happy_eyeballs_delay'

 L.1016       354  LOAD_DEREF               'self'

 L.1012       356  LOAD_CONST               ('loop',)
              358  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              360  GET_AWAITABLE    
              362  LOAD_CONST               None
              364  YIELD_FROM       
              366  UNPACK_SEQUENCE_3     3 
              368  STORE_FAST               'sock'
              370  STORE_FAST               '_'
              372  STORE_FAST               '_'
            374_0  COME_FROM           326  '326'

 L.1018       374  LOAD_FAST                'sock'
              376  LOAD_CONST               None
              378  COMPARE_OP               is
          380_382  POP_JUMP_IF_FALSE   544  'to 544'

 L.1019       384  LOAD_LISTCOMP            '<code_object <listcomp>>'
              386  LOAD_STR                 'BaseEventLoop.create_connection.<locals>.<listcomp>'
              388  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              390  LOAD_DEREF               'exceptions'
              392  GET_ITER         
              394  CALL_FUNCTION_1       1  ''
              396  STORE_DEREF              'exceptions'

 L.1020       398  LOAD_GLOBAL              len
              400  LOAD_DEREF               'exceptions'
              402  CALL_FUNCTION_1       1  ''
              404  LOAD_CONST               1
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   422  'to 422'

 L.1021       412  LOAD_DEREF               'exceptions'
              414  LOAD_CONST               0
              416  BINARY_SUBSCR    
              418  RAISE_VARARGS_1       1  'exception instance'
              420  JUMP_FORWARD        496  'to 496'
            422_0  COME_FROM           408  '408'

 L.1024       422  LOAD_GLOBAL              str
              424  LOAD_DEREF               'exceptions'
              426  LOAD_CONST               0
              428  BINARY_SUBSCR    
              430  CALL_FUNCTION_1       1  ''
              432  STORE_DEREF              'model'

 L.1025       434  LOAD_GLOBAL              all
              436  LOAD_CLOSURE             'model'
              438  BUILD_TUPLE_1         1 
              440  LOAD_GENEXPR             '<code_object <genexpr>>'
              442  LOAD_STR                 'BaseEventLoop.create_connection.<locals>.<genexpr>'
              444  MAKE_FUNCTION_8          'closure'
              446  LOAD_DEREF               'exceptions'
              448  GET_ITER         
              450  CALL_FUNCTION_1       1  ''
              452  CALL_FUNCTION_1       1  ''
          454_456  POP_JUMP_IF_FALSE   466  'to 466'

 L.1026       458  LOAD_DEREF               'exceptions'
              460  LOAD_CONST               0
              462  BINARY_SUBSCR    
              464  RAISE_VARARGS_1       1  'exception instance'
            466_0  COME_FROM           454  '454'

 L.1029       466  LOAD_GLOBAL              OSError
              468  LOAD_STR                 'Multiple exceptions: {}'
              470  LOAD_METHOD              format

 L.1030       472  LOAD_STR                 ', '
              474  LOAD_METHOD              join
              476  LOAD_GENEXPR             '<code_object <genexpr>>'
              478  LOAD_STR                 'BaseEventLoop.create_connection.<locals>.<genexpr>'
              480  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              482  LOAD_DEREF               'exceptions'
              484  GET_ITER         
              486  CALL_FUNCTION_1       1  ''
              488  CALL_METHOD_1         1  ''

 L.1029       490  CALL_METHOD_1         1  ''
              492  CALL_FUNCTION_1       1  ''
              494  RAISE_VARARGS_1       1  'exception instance'
            496_0  COME_FROM           420  '420'
              496  JUMP_FORWARD        544  'to 544'
            498_0  COME_FROM           102  '102'

 L.1033       498  LOAD_FAST                'sock'
              500  LOAD_CONST               None
              502  COMPARE_OP               is
          504_506  POP_JUMP_IF_FALSE   516  'to 516'

 L.1034       508  LOAD_GLOBAL              ValueError

 L.1035       510  LOAD_STR                 'host and port was not specified and no sock specified'

 L.1034       512  CALL_FUNCTION_1       1  ''
              514  RAISE_VARARGS_1       1  'exception instance'
            516_0  COME_FROM           504  '504'

 L.1036       516  LOAD_FAST                'sock'
              518  LOAD_ATTR                type
              520  LOAD_GLOBAL              socket
              522  LOAD_ATTR                SOCK_STREAM
              524  COMPARE_OP               !=
          526_528  POP_JUMP_IF_FALSE   544  'to 544'

 L.1043       530  LOAD_GLOBAL              ValueError

 L.1044       532  LOAD_STR                 'A Stream Socket was expected, got '
              534  LOAD_FAST                'sock'
              536  FORMAT_VALUE          2  '!r'
              538  BUILD_STRING_2        2 

 L.1043       540  CALL_FUNCTION_1       1  ''
              542  RAISE_VARARGS_1       1  'exception instance'
            544_0  COME_FROM           526  '526'
            544_1  COME_FROM           496  '496'
            544_2  COME_FROM           380  '380'

 L.1046       544  LOAD_DEREF               'self'
              546  LOAD_ATTR                _create_connection_transport

 L.1047       548  LOAD_FAST                'sock'

 L.1047       550  LOAD_FAST                'protocol_factory'

 L.1047       552  LOAD_FAST                'ssl'

 L.1047       554  LOAD_FAST                'server_hostname'

 L.1048       556  LOAD_FAST                'ssl_handshake_timeout'

 L.1046       558  LOAD_CONST               ('ssl_handshake_timeout',)
              560  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              562  GET_AWAITABLE    
              564  LOAD_CONST               None
              566  YIELD_FROM       
              568  UNPACK_SEQUENCE_2     2 
              570  STORE_FAST               'transport'
              572  STORE_FAST               'protocol'

 L.1049       574  LOAD_DEREF               'self'
              576  LOAD_ATTR                _debug
          578_580  POP_JUMP_IF_FALSE   612  'to 612'

 L.1052       582  LOAD_FAST                'transport'
              584  LOAD_METHOD              get_extra_info
              586  LOAD_STR                 'socket'
              588  CALL_METHOD_1         1  ''
              590  STORE_FAST               'sock'

 L.1053       592  LOAD_GLOBAL              logger
              594  LOAD_METHOD              debug
              596  LOAD_STR                 '%r connected to %s:%r: (%r, %r)'

 L.1054       598  LOAD_FAST                'sock'

 L.1054       600  LOAD_FAST                'host'

 L.1054       602  LOAD_FAST                'port'

 L.1054       604  LOAD_FAST                'transport'

 L.1054       606  LOAD_FAST                'protocol'

 L.1053       608  CALL_METHOD_6         6  ''
              610  POP_TOP          
            612_0  COME_FROM           578  '578'

 L.1055       612  LOAD_FAST                'transport'
              614  LOAD_FAST                'protocol'
              616  BUILD_TUPLE_2         2 
              618  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 286_288

        async def _create_connection_transport(self, sock, protocol_factory, ssl, server_hostname, server_side=False, ssl_handshake_timeout=None):
            sock.setblockingFalse
            protocol = protocol_factory()
            waiter = self.create_future()
            if ssl:
                sslcontext = None if isinstance(ssl, bool) else ssl
                transport = self._make_ssl_transport(sock,
                  protocol, sslcontext, waiter, server_side=server_side,
                  server_hostname=server_hostname,
                  ssl_handshake_timeout=ssl_handshake_timeout)
            else:
                transport = self._make_socket_transport(sock, protocol, waiter)
            try:
                await waiter
            except:
                transport.close()
                raise
            else:
                return (
                 transport, protocol)

        async def sendfile(self, transport, file, offset=0, count=None, *, fallback=True):
            """Send a file to transport.

        Return the total number of bytes which were sent.

        The method uses high-performance os.sendfile if available.

        file must be a regular file object opened in binary mode.

        offset tells from where to start reading the file. If specified,
        count is the total number of bytes to transmit as opposed to
        sending the file until EOF is reached. File position is updated on
        return or also in case of error in which case file.tell()
        can be used to figure out the number of bytes
        which were sent.

        fallback set to True makes asyncio to manually read and send
        the file when the platform does not support the sendfile syscall
        (e.g. Windows or SSL socket on Unix).

        Raise SendfileNotAvailableError if the system does not support
        sendfile syscall and fallback is False.
        """
            if transport.is_closing():
                raise RuntimeError('Transport is closing')
            else:
                mode = getattr(transport, '_sendfile_compatible', constants._SendfileMode.UNSUPPORTED)
                if mode is constants._SendfileMode.UNSUPPORTED:
                    raise RuntimeError(f"sendfile is not supported for transport {transport!r}")
                if mode is constants._SendfileMode.TRY_NATIVE:
                    try:
                        return await self._sendfile_native(transport, file, offset, count)
                                    except exceptions.SendfileNotAvailableError as exc:
                        try:
                            if not fallback:
                                raise
                        finally:
                            exc = None
                            del exc

                assert fallback, f"fallback is disabled and native sendfile is not supported for transport {transport!r}"
            return await self._sendfile_fallback(transport, file, offset, count)

        async def _sendfile_native(self, transp, file, offset, count):
            raise exceptions.SendfileNotAvailableError'sendfile syscall is not supported'

        async def _sendfile_fallback--- This code section failed: ---

 L.1135         0  LOAD_FAST                'offset'
                2  POP_JUMP_IF_FALSE    14  'to 14'

 L.1136         4  LOAD_FAST                'file'
                6  LOAD_METHOD              seek
                8  LOAD_FAST                'offset'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
             14_0  COME_FROM             2  '2'

 L.1137        14  LOAD_FAST                'count'
               16  POP_JUMP_IF_FALSE    28  'to 28'
               18  LOAD_GLOBAL              min
               20  LOAD_FAST                'count'
               22  LOAD_CONST               16384
               24  CALL_FUNCTION_2       2  ''
               26  JUMP_FORWARD         30  'to 30'
             28_0  COME_FROM            16  '16'
               28  LOAD_CONST               16384
             30_0  COME_FROM            26  '26'
               30  STORE_FAST               'blocksize'

 L.1138        32  LOAD_GLOBAL              bytearray
               34  LOAD_FAST                'blocksize'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'buf'

 L.1139        40  LOAD_CONST               0
               42  STORE_FAST               'total_sent'

 L.1140        44  LOAD_GLOBAL              _SendfileFallbackProtocol
               46  LOAD_FAST                'transp'
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'proto'

 L.1141        52  SETUP_FINALLY       184  'to 184'

 L.1143        54  LOAD_FAST                'count'
               56  POP_JUMP_IF_FALSE    88  'to 88'

 L.1144        58  LOAD_GLOBAL              min
               60  LOAD_FAST                'count'
               62  LOAD_FAST                'total_sent'
               64  BINARY_SUBTRACT  
               66  LOAD_FAST                'blocksize'
               68  CALL_FUNCTION_2       2  ''
               70  STORE_FAST               'blocksize'

 L.1145        72  LOAD_FAST                'blocksize'
               74  LOAD_CONST               0
               76  COMPARE_OP               <=
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L.1146        80  LOAD_FAST                'total_sent'
               82  POP_BLOCK        
               84  CALL_FINALLY        184  'to 184'
               86  RETURN_VALUE     
             88_0  COME_FROM            78  '78'
             88_1  COME_FROM            56  '56'

 L.1147        88  LOAD_GLOBAL              memoryview
               90  LOAD_FAST                'buf'
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_CONST               None
               96  LOAD_FAST                'blocksize'
               98  BUILD_SLICE_2         2 
              100  BINARY_SUBSCR    
              102  STORE_FAST               'view'

 L.1148       104  LOAD_FAST                'self'
              106  LOAD_METHOD              run_in_executor
              108  LOAD_CONST               None
              110  LOAD_FAST                'file'
              112  LOAD_ATTR                readinto
              114  LOAD_FAST                'view'
              116  CALL_METHOD_3         3  ''
              118  GET_AWAITABLE    
              120  LOAD_CONST               None
              122  YIELD_FROM       
              124  STORE_FAST               'read'

 L.1149       126  LOAD_FAST                'read'
              128  POP_JUMP_IF_TRUE    138  'to 138'

 L.1150       130  LOAD_FAST                'total_sent'
              132  POP_BLOCK        
              134  CALL_FINALLY        184  'to 184'
              136  RETURN_VALUE     
            138_0  COME_FROM           128  '128'

 L.1151       138  LOAD_FAST                'proto'
              140  LOAD_METHOD              drain
              142  CALL_METHOD_0         0  ''
              144  GET_AWAITABLE    
              146  LOAD_CONST               None
              148  YIELD_FROM       
              150  POP_TOP          

 L.1152       152  LOAD_FAST                'transp'
              154  LOAD_METHOD              write
              156  LOAD_FAST                'view'
              158  LOAD_CONST               None
              160  LOAD_FAST                'read'
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L.1153       170  LOAD_FAST                'total_sent'
              172  LOAD_FAST                'read'
              174  INPLACE_ADD      
              176  STORE_FAST               'total_sent'
              178  JUMP_BACK            54  'to 54'
              180  POP_BLOCK        
              182  BEGIN_FINALLY    
            184_0  COME_FROM           134  '134'
            184_1  COME_FROM            84  '84'
            184_2  COME_FROM_FINALLY    52  '52'

 L.1155       184  LOAD_FAST                'total_sent'
              186  LOAD_CONST               0
              188  COMPARE_OP               >
              190  POP_JUMP_IF_FALSE   216  'to 216'
              192  LOAD_GLOBAL              hasattr
              194  LOAD_FAST                'file'
              196  LOAD_STR                 'seek'
              198  CALL_FUNCTION_2       2  ''
              200  POP_JUMP_IF_FALSE   216  'to 216'

 L.1156       202  LOAD_FAST                'file'
              204  LOAD_METHOD              seek
              206  LOAD_FAST                'offset'
              208  LOAD_FAST                'total_sent'
              210  BINARY_ADD       
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          
            216_0  COME_FROM           200  '200'
            216_1  COME_FROM           190  '190'

 L.1157       216  LOAD_FAST                'proto'
              218  LOAD_METHOD              restore
              220  CALL_METHOD_0         0  ''
              222  GET_AWAITABLE    
              224  LOAD_CONST               None
              226  YIELD_FROM       
              228  POP_TOP          
              230  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 84

        async def start_tls(self, transport, protocol, sslcontext, *, server_side=False, server_hostname=None, ssl_handshake_timeout=None):
            """Upgrade transport to TLS.

        Return a new transport that *protocol* should start using
        immediately.
        """
            if ssl is None:
                raise RuntimeError('Python ssl module is not available')
            else:
                if not isinstance(sslcontext, ssl.SSLContext):
                    raise TypeError(f"sslcontext is expected to be an instance of ssl.SSLContext, got {sslcontext!r}")
                assert getattr(transport, '_start_tls_compatible', False), f"transport {transport!r} is not supported by start_tls()"
            waiter = self.create_future()
            ssl_protocol = sslproto.SSLProtocol(self,
              protocol, sslcontext, waiter, server_side,
              server_hostname, ssl_handshake_timeout=ssl_handshake_timeout,
              call_connection_made=False)
            transport.pause_reading()
            transport.set_protocolssl_protocol
            conmade_cb = self.call_soonssl_protocol.connection_madetransport
            resume_cb = self.call_soontransport.resume_reading
            try:
                await waiter
            except BaseException:
                transport.close()
                conmade_cb.cancel()
                resume_cb.cancel()
                raise
            else:
                return ssl_protocol._app_transport

        async def create_datagram_endpoint--- This code section failed: ---

 L.1211         0  LOAD_FAST                'sock'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE   144  'to 144'

 L.1212         8  LOAD_FAST                'sock'
               10  LOAD_ATTR                type
               12  LOAD_GLOBAL              socket
               14  LOAD_ATTR                SOCK_DGRAM
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L.1213        20  LOAD_GLOBAL              ValueError

 L.1214        22  LOAD_STR                 'A UDP Socket was expected, got '
               24  LOAD_FAST                'sock'
               26  FORMAT_VALUE          2  '!r'
               28  BUILD_STRING_2        2 

 L.1213        30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            18  '18'

 L.1215        34  LOAD_DEREF               'local_addr'
               36  POP_JUMP_IF_TRUE     62  'to 62'
               38  LOAD_DEREF               'remote_addr'
               40  POP_JUMP_IF_TRUE     62  'to 62'

 L.1216        42  LOAD_FAST                'family'

 L.1215        44  POP_JUMP_IF_TRUE     62  'to 62'

 L.1216        46  LOAD_FAST                'proto'

 L.1215        48  POP_JUMP_IF_TRUE     62  'to 62'

 L.1216        50  LOAD_FAST                'flags'

 L.1215        52  POP_JUMP_IF_TRUE     62  'to 62'

 L.1217        54  LOAD_FAST                'reuse_port'

 L.1215        56  POP_JUMP_IF_TRUE     62  'to 62'

 L.1217        58  LOAD_FAST                'allow_broadcast'

 L.1215        60  POP_JUMP_IF_FALSE   126  'to 126'
             62_0  COME_FROM            56  '56'
             62_1  COME_FROM            52  '52'
             62_2  COME_FROM            48  '48'
             62_3  COME_FROM            44  '44'
             62_4  COME_FROM            40  '40'
             62_5  COME_FROM            36  '36'

 L.1219        62  LOAD_GLOBAL              dict
               64  LOAD_DEREF               'local_addr'
               66  LOAD_DEREF               'remote_addr'

 L.1220        68  LOAD_FAST                'family'

 L.1220        70  LOAD_FAST                'proto'

 L.1220        72  LOAD_FAST                'flags'

 L.1221        74  LOAD_FAST                'reuse_address'

 L.1221        76  LOAD_FAST                'reuse_port'

 L.1222        78  LOAD_FAST                'allow_broadcast'

 L.1219        80  LOAD_CONST               ('local_addr', 'remote_addr', 'family', 'proto', 'flags', 'reuse_address', 'reuse_port', 'allow_broadcast')
               82  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
               84  STORE_FAST               'opts'

 L.1223        86  LOAD_STR                 ', '
               88  LOAD_METHOD              join
               90  LOAD_GENEXPR             '<code_object <genexpr>>'
               92  LOAD_STR                 'BaseEventLoop.create_datagram_endpoint.<locals>.<genexpr>'
               94  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               96  LOAD_FAST                'opts'
               98  LOAD_METHOD              items
              100  CALL_METHOD_0         0  ''
              102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'problems'

 L.1224       110  LOAD_GLOBAL              ValueError

 L.1225       112  LOAD_STR                 'socket modifier keyword arguments can not be used when sock is specified. ('
              114  LOAD_FAST                'problems'
              116  FORMAT_VALUE          0  ''
              118  LOAD_STR                 ')'
              120  BUILD_STRING_3        3 

 L.1224       122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM            60  '60'

 L.1227       126  LOAD_FAST                'sock'
              128  LOAD_METHOD              setblocking
              130  LOAD_CONST               False
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          

 L.1228       136  LOAD_CONST               None
              138  STORE_FAST               'r_addr'
          140_142  JUMP_FORWARD        926  'to 926'
            144_0  COME_FROM             6  '6'

 L.1230       144  LOAD_DEREF               'local_addr'
              146  POP_JUMP_IF_TRUE    186  'to 186'
              148  LOAD_DEREF               'remote_addr'
              150  POP_JUMP_IF_TRUE    186  'to 186'

 L.1231       152  LOAD_FAST                'family'
              154  LOAD_CONST               0
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L.1232       160  LOAD_GLOBAL              ValueError
              162  LOAD_STR                 'unexpected address family'
              164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
            168_0  COME_FROM           158  '158'

 L.1233       168  LOAD_FAST                'family'
              170  LOAD_FAST                'proto'
              172  BUILD_TUPLE_2         2 
              174  LOAD_CONST               (None, None)
              176  BUILD_TUPLE_2         2 
              178  BUILD_TUPLE_1         1 
              180  STORE_FAST               'addr_pairs_info'
          182_184  JUMP_FORWARD        618  'to 618'
            186_0  COME_FROM           150  '150'
            186_1  COME_FROM           146  '146'

 L.1234       186  LOAD_GLOBAL              hasattr
              188  LOAD_GLOBAL              socket
              190  LOAD_STR                 'AF_UNIX'
              192  CALL_FUNCTION_2       2  ''
          194_196  POP_JUMP_IF_FALSE   396  'to 396'
              198  LOAD_FAST                'family'
              200  LOAD_GLOBAL              socket
              202  LOAD_ATTR                AF_UNIX
              204  COMPARE_OP               ==
          206_208  POP_JUMP_IF_FALSE   396  'to 396'

 L.1235       210  LOAD_DEREF               'local_addr'
              212  LOAD_DEREF               'remote_addr'
              214  BUILD_TUPLE_2         2 
              216  GET_ITER         
            218_0  COME_FROM           238  '238'
            218_1  COME_FROM           228  '228'
              218  FOR_ITER            250  'to 250'
              220  STORE_FAST               'addr'

 L.1236       222  LOAD_FAST                'addr'
              224  LOAD_CONST               None
              226  COMPARE_OP               is-not
              228  POP_JUMP_IF_FALSE   218  'to 218'
              230  LOAD_GLOBAL              isinstance
              232  LOAD_FAST                'addr'
              234  LOAD_GLOBAL              str
              236  CALL_FUNCTION_2       2  ''
              238  POP_JUMP_IF_TRUE    218  'to 218'

 L.1237       240  LOAD_GLOBAL              TypeError
              242  LOAD_STR                 'string is expected'
              244  CALL_FUNCTION_1       1  ''
              246  RAISE_VARARGS_1       1  'exception instance'
              248  JUMP_BACK           218  'to 218'

 L.1239       250  LOAD_DEREF               'local_addr'
          252_254  POP_JUMP_IF_FALSE   376  'to 376'
              256  LOAD_DEREF               'local_addr'
              258  LOAD_CONST               0
              260  BINARY_SUBSCR    
              262  LOAD_CONST               (0, '\x00')
              264  COMPARE_OP               not-in
          266_268  POP_JUMP_IF_FALSE   376  'to 376'

 L.1240       270  SETUP_FINALLY       306  'to 306'

 L.1241       272  LOAD_GLOBAL              stat
              274  LOAD_METHOD              S_ISSOCK
              276  LOAD_GLOBAL              os
              278  LOAD_METHOD              stat
              280  LOAD_DEREF               'local_addr'
              282  CALL_METHOD_1         1  ''
              284  LOAD_ATTR                st_mode
              286  CALL_METHOD_1         1  ''
          288_290  POP_JUMP_IF_FALSE   302  'to 302'

 L.1242       292  LOAD_GLOBAL              os
              294  LOAD_METHOD              remove
              296  LOAD_DEREF               'local_addr'
              298  CALL_METHOD_1         1  ''
              300  POP_TOP          
            302_0  COME_FROM           288  '288'
              302  POP_BLOCK        
              304  JUMP_FORWARD        376  'to 376'
            306_0  COME_FROM_FINALLY   270  '270'

 L.1243       306  DUP_TOP          
              308  LOAD_GLOBAL              FileNotFoundError
              310  COMPARE_OP               exception-match
          312_314  POP_JUMP_IF_FALSE   326  'to 326'
              316  POP_TOP          
              318  POP_TOP          
              320  POP_TOP          

 L.1244       322  POP_EXCEPT       
              324  JUMP_FORWARD        376  'to 376'
            326_0  COME_FROM           312  '312'

 L.1245       326  DUP_TOP          
              328  LOAD_GLOBAL              OSError
              330  COMPARE_OP               exception-match
          332_334  POP_JUMP_IF_FALSE   374  'to 374'
              336  POP_TOP          
              338  STORE_FAST               'err'
              340  POP_TOP          
              342  SETUP_FINALLY       362  'to 362'

 L.1247       344  LOAD_GLOBAL              logger
              346  LOAD_METHOD              error
              348  LOAD_STR                 'Unable to check or remove stale UNIX socket %r: %r'

 L.1249       350  LOAD_DEREF               'local_addr'

 L.1249       352  LOAD_FAST                'err'

 L.1247       354  CALL_METHOD_3         3  ''
              356  POP_TOP          
              358  POP_BLOCK        
              360  BEGIN_FINALLY    
            362_0  COME_FROM_FINALLY   342  '342'
              362  LOAD_CONST               None
              364  STORE_FAST               'err'
              366  DELETE_FAST              'err'
              368  END_FINALLY      
              370  POP_EXCEPT       
              372  JUMP_FORWARD        376  'to 376'
            374_0  COME_FROM           332  '332'
              374  END_FINALLY      
            376_0  COME_FROM           372  '372'
            376_1  COME_FROM           324  '324'
            376_2  COME_FROM           304  '304'
            376_3  COME_FROM           266  '266'
            376_4  COME_FROM           252  '252'

 L.1251       376  LOAD_FAST                'family'
              378  LOAD_FAST                'proto'
              380  BUILD_TUPLE_2         2 

 L.1252       382  LOAD_DEREF               'local_addr'
              384  LOAD_DEREF               'remote_addr'
              386  BUILD_TUPLE_2         2 

 L.1251       388  BUILD_TUPLE_2         2 
              390  BUILD_TUPLE_1         1 
              392  STORE_FAST               'addr_pairs_info'
              394  JUMP_FORWARD        618  'to 618'
            396_0  COME_FROM           206  '206'
            396_1  COME_FROM           194  '194'

 L.1255       396  BUILD_MAP_0           0 
              398  STORE_FAST               'addr_infos'

 L.1256       400  LOAD_CONST               0
              402  LOAD_DEREF               'local_addr'
              404  BUILD_TUPLE_2         2 
              406  LOAD_CONST               1
              408  LOAD_DEREF               'remote_addr'
              410  BUILD_TUPLE_2         2 
              412  BUILD_TUPLE_2         2 
              414  GET_ITER         
            416_0  COME_FROM           430  '430'
              416  FOR_ITER            580  'to 580'
              418  UNPACK_SEQUENCE_2     2 
              420  STORE_FAST               'idx'
              422  STORE_FAST               'addr'

 L.1257       424  LOAD_FAST                'addr'
              426  LOAD_CONST               None
              428  COMPARE_OP               is-not
          430_432  POP_JUMP_IF_FALSE   416  'to 416'

 L.1258       434  LOAD_GLOBAL              isinstance
              436  LOAD_FAST                'addr'
              438  LOAD_GLOBAL              tuple
              440  CALL_FUNCTION_2       2  ''
          442_444  POP_JUMP_IF_FALSE   460  'to 460'
              446  LOAD_GLOBAL              len
              448  LOAD_FAST                'addr'
              450  CALL_FUNCTION_1       1  ''
              452  LOAD_CONST               2
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_TRUE    468  'to 468'
            460_0  COME_FROM           442  '442'
              460  LOAD_ASSERT              AssertionError

 L.1259       462  LOAD_STR                 '2-tuple is expected'

 L.1258       464  CALL_FUNCTION_1       1  ''
              466  RAISE_VARARGS_1       1  'exception instance'
            468_0  COME_FROM           456  '456'

 L.1261       468  LOAD_FAST                'self'
              470  LOAD_ATTR                _ensure_resolved

 L.1262       472  LOAD_FAST                'addr'

 L.1262       474  LOAD_FAST                'family'

 L.1262       476  LOAD_GLOBAL              socket
              478  LOAD_ATTR                SOCK_DGRAM

 L.1263       480  LOAD_FAST                'proto'

 L.1263       482  LOAD_FAST                'flags'

 L.1263       484  LOAD_FAST                'self'

 L.1261       486  LOAD_CONST               ('family', 'type', 'proto', 'flags', 'loop')
              488  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              490  GET_AWAITABLE    
              492  LOAD_CONST               None
              494  YIELD_FROM       
              496  STORE_FAST               'infos'

 L.1264       498  LOAD_FAST                'infos'
          500_502  POP_JUMP_IF_TRUE    512  'to 512'

 L.1265       504  LOAD_GLOBAL              OSError
              506  LOAD_STR                 'getaddrinfo() returned empty list'
              508  CALL_FUNCTION_1       1  ''
              510  RAISE_VARARGS_1       1  'exception instance'
            512_0  COME_FROM           500  '500'

 L.1267       512  LOAD_FAST                'infos'
              514  GET_ITER         
              516  FOR_ITER            576  'to 576'
              518  UNPACK_SEQUENCE_5     5 
              520  STORE_FAST               'fam'
              522  STORE_FAST               '_'
              524  STORE_FAST               'pro'
              526  STORE_FAST               '_'
              528  STORE_FAST               'address'

 L.1268       530  LOAD_FAST                'fam'
              532  LOAD_FAST                'pro'
              534  BUILD_TUPLE_2         2 
              536  STORE_FAST               'key'

 L.1269       538  LOAD_FAST                'key'
              540  LOAD_FAST                'addr_infos'
              542  COMPARE_OP               not-in
          544_546  POP_JUMP_IF_FALSE   560  'to 560'

 L.1270       548  LOAD_CONST               None
              550  LOAD_CONST               None
              552  BUILD_LIST_2          2 
              554  LOAD_FAST                'addr_infos'
              556  LOAD_FAST                'key'
              558  STORE_SUBSCR     
            560_0  COME_FROM           544  '544'

 L.1271       560  LOAD_FAST                'address'
              562  LOAD_FAST                'addr_infos'
              564  LOAD_FAST                'key'
              566  BINARY_SUBSCR    
              568  LOAD_FAST                'idx'
              570  STORE_SUBSCR     
          572_574  JUMP_BACK           516  'to 516'
          576_578  JUMP_BACK           416  'to 416'

 L.1274       580  LOAD_CLOSURE             'local_addr'
              582  LOAD_CLOSURE             'remote_addr'
              584  BUILD_TUPLE_2         2 
              586  LOAD_LISTCOMP            '<code_object <listcomp>>'
              588  LOAD_STR                 'BaseEventLoop.create_datagram_endpoint.<locals>.<listcomp>'
              590  MAKE_FUNCTION_8          'closure'

 L.1275       592  LOAD_FAST                'addr_infos'
              594  LOAD_METHOD              items
              596  CALL_METHOD_0         0  ''

 L.1274       598  GET_ITER         
              600  CALL_FUNCTION_1       1  ''
              602  STORE_FAST               'addr_pairs_info'

 L.1279       604  LOAD_FAST                'addr_pairs_info'
          606_608  POP_JUMP_IF_TRUE    618  'to 618'

 L.1280       610  LOAD_GLOBAL              ValueError
              612  LOAD_STR                 'can not get address information'
              614  CALL_FUNCTION_1       1  ''
              616  RAISE_VARARGS_1       1  'exception instance'
            618_0  COME_FROM           606  '606'
            618_1  COME_FROM           394  '394'
            618_2  COME_FROM           182  '182'

 L.1282       618  BUILD_LIST_0          0 
              620  STORE_FAST               'exceptions'

 L.1285       622  LOAD_FAST                'reuse_address'
              624  LOAD_GLOBAL              _unset
              626  COMPARE_OP               is-not
          628_630  POP_JUMP_IF_FALSE   664  'to 664'

 L.1286       632  LOAD_FAST                'reuse_address'
          634_636  POP_JUMP_IF_FALSE   648  'to 648'

 L.1287       638  LOAD_GLOBAL              ValueError
              640  LOAD_STR                 'Passing `reuse_address=True` is no longer supported, as the usage of SO_REUSEPORT in UDP poses a significant security concern.'
              642  CALL_FUNCTION_1       1  ''
              644  RAISE_VARARGS_1       1  'exception instance'
              646  JUMP_FORWARD        664  'to 664'
            648_0  COME_FROM           634  '634'

 L.1292       648  LOAD_GLOBAL              warnings
              650  LOAD_ATTR                warn
              652  LOAD_STR                 'The *reuse_address* parameter has been deprecated as of 3.5.10 and is scheduled for removal in 3.11.'

 L.1294       654  LOAD_GLOBAL              DeprecationWarning

 L.1295       656  LOAD_CONST               2

 L.1292       658  LOAD_CONST               ('stacklevel',)
              660  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              662  POP_TOP          
            664_0  COME_FROM           646  '646'
            664_1  COME_FROM           628  '628'

 L.1298       664  LOAD_FAST                'addr_pairs_info'

 L.1297       666  GET_ITER         
              668  FOR_ITER            918  'to 918'
              670  UNPACK_SEQUENCE_2     2 
              672  UNPACK_SEQUENCE_2     2 
              674  STORE_FAST               'family'
              676  STORE_FAST               'proto'

 L.1298       678  UNPACK_SEQUENCE_2     2 
              680  STORE_FAST               'local_address'
              682  STORE_FAST               'remote_address'

 L.1299       684  LOAD_CONST               None
              686  STORE_FAST               'sock'

 L.1300       688  LOAD_CONST               None
              690  STORE_FAST               'r_addr'

 L.1301       692  SETUP_FINALLY       814  'to 814'

 L.1302       694  LOAD_GLOBAL              socket
              696  LOAD_ATTR                socket

 L.1303       698  LOAD_FAST                'family'

 L.1303       700  LOAD_GLOBAL              socket
              702  LOAD_ATTR                SOCK_DGRAM

 L.1303       704  LOAD_FAST                'proto'

 L.1302       706  LOAD_CONST               ('family', 'type', 'proto')
              708  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              710  STORE_FAST               'sock'

 L.1304       712  LOAD_FAST                'reuse_port'
          714_716  POP_JUMP_IF_FALSE   726  'to 726'

 L.1305       718  LOAD_GLOBAL              _set_reuseport
              720  LOAD_FAST                'sock'
              722  CALL_FUNCTION_1       1  ''
              724  POP_TOP          
            726_0  COME_FROM           714  '714'

 L.1306       726  LOAD_FAST                'allow_broadcast'
          728_730  POP_JUMP_IF_FALSE   750  'to 750'

 L.1307       732  LOAD_FAST                'sock'
              734  LOAD_METHOD              setsockopt

 L.1308       736  LOAD_GLOBAL              socket
              738  LOAD_ATTR                SOL_SOCKET

 L.1308       740  LOAD_GLOBAL              socket
              742  LOAD_ATTR                SO_BROADCAST

 L.1308       744  LOAD_CONST               1

 L.1307       746  CALL_METHOD_3         3  ''
              748  POP_TOP          
            750_0  COME_FROM           728  '728'

 L.1309       750  LOAD_FAST                'sock'
              752  LOAD_METHOD              setblocking
              754  LOAD_CONST               False
              756  CALL_METHOD_1         1  ''
              758  POP_TOP          

 L.1311       760  LOAD_DEREF               'local_addr'
          762_764  POP_JUMP_IF_FALSE   776  'to 776'

 L.1312       766  LOAD_FAST                'sock'
              768  LOAD_METHOD              bind
              770  LOAD_FAST                'local_address'
              772  CALL_METHOD_1         1  ''
              774  POP_TOP          
            776_0  COME_FROM           762  '762'

 L.1313       776  LOAD_DEREF               'remote_addr'
          778_780  POP_JUMP_IF_FALSE   810  'to 810'

 L.1314       782  LOAD_FAST                'allow_broadcast'
          784_786  POP_JUMP_IF_TRUE    806  'to 806'

 L.1315       788  LOAD_FAST                'self'
              790  LOAD_METHOD              sock_connect
              792  LOAD_FAST                'sock'
              794  LOAD_FAST                'remote_address'
              796  CALL_METHOD_2         2  ''
              798  GET_AWAITABLE    
              800  LOAD_CONST               None
              802  YIELD_FROM       
              804  POP_TOP          
            806_0  COME_FROM           784  '784'

 L.1316       806  LOAD_FAST                'remote_address'
              808  STORE_FAST               'r_addr'
            810_0  COME_FROM           778  '778'
              810  POP_BLOCK        
              812  JUMP_FORWARD        908  'to 908'
            814_0  COME_FROM_FINALLY   692  '692'

 L.1317       814  DUP_TOP          
              816  LOAD_GLOBAL              OSError
              818  COMPARE_OP               exception-match
          820_822  POP_JUMP_IF_FALSE   876  'to 876'
              824  POP_TOP          
              826  STORE_FAST               'exc'
              828  POP_TOP          
              830  SETUP_FINALLY       864  'to 864'

 L.1318       832  LOAD_FAST                'sock'
              834  LOAD_CONST               None
              836  COMPARE_OP               is-not
          838_840  POP_JUMP_IF_FALSE   850  'to 850'

 L.1319       842  LOAD_FAST                'sock'
              844  LOAD_METHOD              close
              846  CALL_METHOD_0         0  ''
              848  POP_TOP          
            850_0  COME_FROM           838  '838'

 L.1320       850  LOAD_FAST                'exceptions'
              852  LOAD_METHOD              append
              854  LOAD_FAST                'exc'
              856  CALL_METHOD_1         1  ''
              858  POP_TOP          
              860  POP_BLOCK        
              862  BEGIN_FINALLY    
            864_0  COME_FROM_FINALLY   830  '830'
              864  LOAD_CONST               None
              866  STORE_FAST               'exc'
              868  DELETE_FAST              'exc'
              870  END_FINALLY      
              872  POP_EXCEPT       
              874  JUMP_BACK           668  'to 668'
            876_0  COME_FROM           820  '820'

 L.1321       876  POP_TOP          
              878  POP_TOP          
              880  POP_TOP          

 L.1322       882  LOAD_FAST                'sock'
              884  LOAD_CONST               None
              886  COMPARE_OP               is-not
          888_890  POP_JUMP_IF_FALSE   900  'to 900'

 L.1323       892  LOAD_FAST                'sock'
              894  LOAD_METHOD              close
              896  CALL_METHOD_0         0  ''
              898  POP_TOP          
            900_0  COME_FROM           888  '888'

 L.1324       900  RAISE_VARARGS_0       0  'reraise'
              902  POP_EXCEPT       
              904  JUMP_BACK           668  'to 668'
              906  END_FINALLY      
            908_0  COME_FROM           812  '812'

 L.1326       908  POP_TOP          
          910_912  BREAK_LOOP          926  'to 926'
          914_916  JUMP_BACK           668  'to 668'

 L.1328       918  LOAD_FAST                'exceptions'
              920  LOAD_CONST               0
              922  BINARY_SUBSCR    
              924  RAISE_VARARGS_1       1  'exception instance'
            926_0  COME_FROM           140  '140'

 L.1330       926  LOAD_FAST                'protocol_factory'
              928  CALL_FUNCTION_0       0  ''
              930  STORE_FAST               'protocol'

 L.1331       932  LOAD_FAST                'self'
              934  LOAD_METHOD              create_future
              936  CALL_METHOD_0         0  ''
              938  STORE_FAST               'waiter'

 L.1332       940  LOAD_FAST                'self'
              942  LOAD_METHOD              _make_datagram_transport

 L.1333       944  LOAD_FAST                'sock'

 L.1333       946  LOAD_FAST                'protocol'

 L.1333       948  LOAD_FAST                'r_addr'

 L.1333       950  LOAD_FAST                'waiter'

 L.1332       952  CALL_METHOD_4         4  ''
              954  STORE_FAST               'transport'

 L.1334       956  LOAD_FAST                'self'
              958  LOAD_ATTR                _debug
          960_962  POP_JUMP_IF_FALSE  1006  'to 1006'

 L.1335       964  LOAD_DEREF               'local_addr'
          966_968  POP_JUMP_IF_FALSE   990  'to 990'

 L.1336       970  LOAD_GLOBAL              logger
              972  LOAD_METHOD              info
              974  LOAD_STR                 'Datagram endpoint local_addr=%r remote_addr=%r created: (%r, %r)'

 L.1338       976  LOAD_DEREF               'local_addr'

 L.1338       978  LOAD_DEREF               'remote_addr'

 L.1338       980  LOAD_FAST                'transport'

 L.1338       982  LOAD_FAST                'protocol'

 L.1336       984  CALL_METHOD_5         5  ''
              986  POP_TOP          
              988  JUMP_FORWARD       1006  'to 1006'
            990_0  COME_FROM           966  '966'

 L.1340       990  LOAD_GLOBAL              logger
              992  LOAD_METHOD              debug
              994  LOAD_STR                 'Datagram endpoint remote_addr=%r created: (%r, %r)'

 L.1342       996  LOAD_DEREF               'remote_addr'

 L.1342       998  LOAD_FAST                'transport'

 L.1342      1000  LOAD_FAST                'protocol'

 L.1340      1002  CALL_METHOD_4         4  ''
             1004  POP_TOP          
           1006_0  COME_FROM           988  '988'
           1006_1  COME_FROM           960  '960'

 L.1344      1006  SETUP_FINALLY      1022  'to 1022'

 L.1345      1008  LOAD_FAST                'waiter'
             1010  GET_AWAITABLE    
             1012  LOAD_CONST               None
             1014  YIELD_FROM       
             1016  POP_TOP          
             1018  POP_BLOCK        
             1020  JUMP_FORWARD       1044  'to 1044'
           1022_0  COME_FROM_FINALLY  1006  '1006'

 L.1346      1022  POP_TOP          
             1024  POP_TOP          
             1026  POP_TOP          

 L.1347      1028  LOAD_FAST                'transport'
             1030  LOAD_METHOD              close
             1032  CALL_METHOD_0         0  ''
             1034  POP_TOP          

 L.1348      1036  RAISE_VARARGS_0       0  'reraise'
             1038  POP_EXCEPT       
             1040  JUMP_FORWARD       1044  'to 1044'
             1042  END_FINALLY      
           1044_0  COME_FROM          1040  '1040'
           1044_1  COME_FROM          1020  '1020'

 L.1350      1044  LOAD_FAST                'transport'
             1046  LOAD_FAST                'protocol'
             1048  BUILD_TUPLE_2         2 
             1050  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 140_142

        async def _ensure_resolved(self, address, *, family=0, type=socket.SOCK_STREAM, proto=0, flags=0, loop):
            host, port = address[:2]
            info = _ipaddr_info(host, port, family, type, proto, *address[2:])
            if info is not None:
                return [info]
            return await loop.getaddrinfo(host, port, family=family, type=type, proto=proto,
              flags=flags)

        async def _create_server_getaddrinfo(self, host, port, family, flags):
            infos = await self._ensure_resolved((host, port), family=family, type=(socket.SOCK_STREAM),
              flags=flags,
              loop=self)
            if not infos:
                raise OSError(f"getaddrinfo({host!r}) returned empty list")
            return infos

        async def create_server--- This code section failed: ---

 L.1399         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'ssl'
                4  LOAD_GLOBAL              bool
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.1400        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'ssl argument must be an SSLContext or None'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.1402        18  LOAD_FAST                'ssl_handshake_timeout'
               20  LOAD_CONST               None
               22  COMPARE_OP               is-not
               24  POP_JUMP_IF_FALSE    42  'to 42'
               26  LOAD_FAST                'ssl'
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L.1403        34  LOAD_GLOBAL              ValueError

 L.1404        36  LOAD_STR                 'ssl_handshake_timeout is only meaningful with ssl'

 L.1403        38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            32  '32'
             42_1  COME_FROM            24  '24'

 L.1406        42  LOAD_FAST                'host'
               44  LOAD_CONST               None
               46  COMPARE_OP               is-not
               48  POP_JUMP_IF_TRUE     60  'to 60'
               50  LOAD_DEREF               'port'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
            56_58  POP_JUMP_IF_FALSE   546  'to 546'
             60_0  COME_FROM            48  '48'

 L.1407        60  LOAD_FAST                'sock'
               62  LOAD_CONST               None
               64  COMPARE_OP               is-not
               66  POP_JUMP_IF_FALSE    76  'to 76'

 L.1408        68  LOAD_GLOBAL              ValueError

 L.1409        70  LOAD_STR                 'host/port and sock can not be specified at the same time'

 L.1408        72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'

 L.1411        76  LOAD_FAST                'reuse_address'
               78  LOAD_CONST               None
               80  COMPARE_OP               is
               82  POP_JUMP_IF_FALSE   104  'to 104'

 L.1412        84  LOAD_GLOBAL              os
               86  LOAD_ATTR                name
               88  LOAD_STR                 'posix'
               90  COMPARE_OP               ==
               92  JUMP_IF_FALSE_OR_POP   102  'to 102'
               94  LOAD_GLOBAL              sys
               96  LOAD_ATTR                platform
               98  LOAD_STR                 'cygwin'
              100  COMPARE_OP               !=
            102_0  COME_FROM            92  '92'
              102  STORE_FAST               'reuse_address'
            104_0  COME_FROM            82  '82'

 L.1413       104  BUILD_LIST_0          0 
              106  STORE_FAST               'sockets'

 L.1414       108  LOAD_FAST                'host'
              110  LOAD_STR                 ''
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L.1415       116  LOAD_CONST               None
              118  BUILD_LIST_1          1 
              120  STORE_FAST               'hosts'
              122  JUMP_FORWARD        160  'to 160'
            124_0  COME_FROM           114  '114'

 L.1416       124  LOAD_GLOBAL              isinstance
              126  LOAD_FAST                'host'
              128  LOAD_GLOBAL              str
              130  CALL_FUNCTION_2       2  ''
              132  POP_JUMP_IF_TRUE    148  'to 148'

 L.1417       134  LOAD_GLOBAL              isinstance
              136  LOAD_FAST                'host'
              138  LOAD_GLOBAL              collections
              140  LOAD_ATTR                abc
              142  LOAD_ATTR                Iterable
              144  CALL_FUNCTION_2       2  ''

 L.1416       146  POP_JUMP_IF_TRUE    156  'to 156'
            148_0  COME_FROM           132  '132'

 L.1418       148  LOAD_FAST                'host'
              150  BUILD_LIST_1          1 
              152  STORE_FAST               'hosts'
              154  JUMP_FORWARD        160  'to 160'
            156_0  COME_FROM           146  '146'

 L.1420       156  LOAD_FAST                'host'
              158  STORE_FAST               'hosts'
            160_0  COME_FROM           154  '154'
            160_1  COME_FROM           122  '122'

 L.1422       160  LOAD_CLOSURE             'family'
              162  LOAD_CLOSURE             'flags'
              164  LOAD_CLOSURE             'port'
              166  LOAD_CLOSURE             'self'
              168  BUILD_TUPLE_4         4 
              170  LOAD_LISTCOMP            '<code_object <listcomp>>'
              172  LOAD_STR                 'BaseEventLoop.create_server.<locals>.<listcomp>'
              174  MAKE_FUNCTION_8          'closure'

 L.1424       176  LOAD_FAST                'hosts'

 L.1422       178  GET_ITER         
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               'fs'

 L.1425       184  LOAD_GLOBAL              tasks
              186  LOAD_ATTR                gather
              188  LOAD_FAST                'fs'
              190  LOAD_STR                 'loop'
              192  LOAD_DEREF               'self'
              194  BUILD_MAP_1           1 
              196  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              198  GET_AWAITABLE    
              200  LOAD_CONST               None
              202  YIELD_FROM       
              204  STORE_FAST               'infos'

 L.1426       206  LOAD_GLOBAL              set
              208  LOAD_GLOBAL              itertools
              210  LOAD_ATTR                chain
              212  LOAD_METHOD              from_iterable
              214  LOAD_FAST                'infos'
              216  CALL_METHOD_1         1  ''
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'infos'

 L.1428       222  LOAD_CONST               False
              224  STORE_FAST               'completed'

 L.1429   226_228  SETUP_FINALLY       516  'to 516'

 L.1430       230  LOAD_FAST                'infos'
              232  GET_ITER         
          234_236  FOR_ITER            508  'to 508'
              238  STORE_FAST               'res'

 L.1431       240  LOAD_FAST                'res'
              242  UNPACK_SEQUENCE_5     5 
              244  STORE_FAST               'af'
              246  STORE_FAST               'socktype'
              248  STORE_FAST               'proto'
              250  STORE_FAST               'canonname'
              252  STORE_FAST               'sa'

 L.1432       254  SETUP_FINALLY       274  'to 274'

 L.1433       256  LOAD_GLOBAL              socket
              258  LOAD_METHOD              socket
              260  LOAD_FAST                'af'
              262  LOAD_FAST                'socktype'
              264  LOAD_FAST                'proto'
              266  CALL_METHOD_3         3  ''
              268  STORE_FAST               'sock'
              270  POP_BLOCK        
              272  JUMP_FORWARD        330  'to 330'
            274_0  COME_FROM_FINALLY   254  '254'

 L.1434       274  DUP_TOP          
              276  LOAD_GLOBAL              socket
              278  LOAD_ATTR                error
              280  COMPARE_OP               exception-match
          282_284  POP_JUMP_IF_FALSE   328  'to 328'
              286  POP_TOP          
              288  POP_TOP          
              290  POP_TOP          

 L.1436       292  LOAD_DEREF               'self'
              294  LOAD_ATTR                _debug
          296_298  POP_JUMP_IF_FALSE   320  'to 320'

 L.1437       300  LOAD_GLOBAL              logger
              302  LOAD_ATTR                warning
              304  LOAD_STR                 'create_server() failed to create socket.socket(%r, %r, %r)'

 L.1439       306  LOAD_FAST                'af'

 L.1439       308  LOAD_FAST                'socktype'

 L.1439       310  LOAD_FAST                'proto'

 L.1439       312  LOAD_CONST               True

 L.1437       314  LOAD_CONST               ('exc_info',)
              316  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              318  POP_TOP          
            320_0  COME_FROM           296  '296'

 L.1440       320  POP_EXCEPT       
              322  JUMP_BACK           234  'to 234'
              324  POP_EXCEPT       
              326  JUMP_FORWARD        330  'to 330'
            328_0  COME_FROM           282  '282'
              328  END_FINALLY      
            330_0  COME_FROM           326  '326'
            330_1  COME_FROM           272  '272'

 L.1441       330  LOAD_FAST                'sockets'
              332  LOAD_METHOD              append
              334  LOAD_FAST                'sock'
              336  CALL_METHOD_1         1  ''
              338  POP_TOP          

 L.1442       340  LOAD_FAST                'reuse_address'
          342_344  POP_JUMP_IF_FALSE   364  'to 364'

 L.1443       346  LOAD_FAST                'sock'
              348  LOAD_METHOD              setsockopt

 L.1444       350  LOAD_GLOBAL              socket
              352  LOAD_ATTR                SOL_SOCKET

 L.1444       354  LOAD_GLOBAL              socket
              356  LOAD_ATTR                SO_REUSEADDR

 L.1444       358  LOAD_CONST               True

 L.1443       360  CALL_METHOD_3         3  ''
              362  POP_TOP          
            364_0  COME_FROM           342  '342'

 L.1445       364  LOAD_FAST                'reuse_port'
          366_368  POP_JUMP_IF_FALSE   378  'to 378'

 L.1446       370  LOAD_GLOBAL              _set_reuseport
              372  LOAD_FAST                'sock'
              374  CALL_FUNCTION_1       1  ''
              376  POP_TOP          
            378_0  COME_FROM           366  '366'

 L.1450       378  LOAD_GLOBAL              _HAS_IPv6
          380_382  POP_JUMP_IF_FALSE   426  'to 426'

 L.1451       384  LOAD_FAST                'af'
              386  LOAD_GLOBAL              socket
              388  LOAD_ATTR                AF_INET6
              390  COMPARE_OP               ==

 L.1450   392_394  POP_JUMP_IF_FALSE   426  'to 426'

 L.1452       396  LOAD_GLOBAL              hasattr
              398  LOAD_GLOBAL              socket
              400  LOAD_STR                 'IPPROTO_IPV6'
              402  CALL_FUNCTION_2       2  ''

 L.1450   404_406  POP_JUMP_IF_FALSE   426  'to 426'

 L.1453       408  LOAD_FAST                'sock'
              410  LOAD_METHOD              setsockopt
              412  LOAD_GLOBAL              socket
              414  LOAD_ATTR                IPPROTO_IPV6

 L.1454       416  LOAD_GLOBAL              socket
              418  LOAD_ATTR                IPV6_V6ONLY

 L.1455       420  LOAD_CONST               True

 L.1453       422  CALL_METHOD_3         3  ''
              424  POP_TOP          
            426_0  COME_FROM           404  '404'
            426_1  COME_FROM           392  '392'
            426_2  COME_FROM           380  '380'

 L.1456       426  SETUP_FINALLY       442  'to 442'

 L.1457       428  LOAD_FAST                'sock'
              430  LOAD_METHOD              bind
              432  LOAD_FAST                'sa'
              434  CALL_METHOD_1         1  ''
              436  POP_TOP          
              438  POP_BLOCK        
              440  JUMP_BACK           234  'to 234'
            442_0  COME_FROM_FINALLY   426  '426'

 L.1458       442  DUP_TOP          
              444  LOAD_GLOBAL              OSError
              446  COMPARE_OP               exception-match
          448_450  POP_JUMP_IF_FALSE   504  'to 504'
              452  POP_TOP          
              454  STORE_FAST               'err'
              456  POP_TOP          
              458  SETUP_FINALLY       492  'to 492'

 L.1459       460  LOAD_GLOBAL              OSError
              462  LOAD_FAST                'err'
              464  LOAD_ATTR                errno
              466  LOAD_STR                 'error while attempting to bind on address %r: %s'

 L.1461       468  LOAD_FAST                'sa'
              470  LOAD_FAST                'err'
              472  LOAD_ATTR                strerror
              474  LOAD_METHOD              lower
              476  CALL_METHOD_0         0  ''
              478  BUILD_TUPLE_2         2 

 L.1459       480  BINARY_MODULO    
              482  CALL_FUNCTION_2       2  ''

 L.1461       484  LOAD_CONST               None

 L.1459       486  RAISE_VARARGS_2       2  'exception instance with __cause__'
              488  POP_BLOCK        
              490  BEGIN_FINALLY    
            492_0  COME_FROM_FINALLY   458  '458'
              492  LOAD_CONST               None
              494  STORE_FAST               'err'
              496  DELETE_FAST              'err'
              498  END_FINALLY      
              500  POP_EXCEPT       
              502  JUMP_BACK           234  'to 234'
            504_0  COME_FROM           448  '448'
              504  END_FINALLY      
              506  JUMP_BACK           234  'to 234'

 L.1462       508  LOAD_CONST               True
              510  STORE_FAST               'completed'
              512  POP_BLOCK        
              514  BEGIN_FINALLY    
            516_0  COME_FROM_FINALLY   226  '226'

 L.1464       516  LOAD_FAST                'completed'
          518_520  POP_JUMP_IF_TRUE    542  'to 542'

 L.1465       522  LOAD_FAST                'sockets'
              524  GET_ITER         
              526  FOR_ITER            542  'to 542'
              528  STORE_FAST               'sock'

 L.1466       530  LOAD_FAST                'sock'
              532  LOAD_METHOD              close
              534  CALL_METHOD_0         0  ''
              536  POP_TOP          
          538_540  JUMP_BACK           526  'to 526'
            542_0  COME_FROM           518  '518'
              542  END_FINALLY      
              544  JUMP_FORWARD        598  'to 598'
            546_0  COME_FROM            56  '56'

 L.1468       546  LOAD_FAST                'sock'
              548  LOAD_CONST               None
              550  COMPARE_OP               is
          552_554  POP_JUMP_IF_FALSE   564  'to 564'

 L.1469       556  LOAD_GLOBAL              ValueError
              558  LOAD_STR                 'Neither host/port nor sock were specified'
              560  CALL_FUNCTION_1       1  ''
              562  RAISE_VARARGS_1       1  'exception instance'
            564_0  COME_FROM           552  '552'

 L.1470       564  LOAD_FAST                'sock'
              566  LOAD_ATTR                type
              568  LOAD_GLOBAL              socket
              570  LOAD_ATTR                SOCK_STREAM
              572  COMPARE_OP               !=
          574_576  POP_JUMP_IF_FALSE   592  'to 592'

 L.1471       578  LOAD_GLOBAL              ValueError
              580  LOAD_STR                 'A Stream Socket was expected, got '
              582  LOAD_FAST                'sock'
              584  FORMAT_VALUE          2  '!r'
              586  BUILD_STRING_2        2 
              588  CALL_FUNCTION_1       1  ''
              590  RAISE_VARARGS_1       1  'exception instance'
            592_0  COME_FROM           574  '574'

 L.1472       592  LOAD_FAST                'sock'
              594  BUILD_LIST_1          1 
              596  STORE_FAST               'sockets'
            598_0  COME_FROM           544  '544'

 L.1474       598  LOAD_FAST                'sockets'
              600  GET_ITER         
              602  FOR_ITER            620  'to 620'
              604  STORE_FAST               'sock'

 L.1475       606  LOAD_FAST                'sock'
              608  LOAD_METHOD              setblocking
              610  LOAD_CONST               False
              612  CALL_METHOD_1         1  ''
              614  POP_TOP          
          616_618  JUMP_BACK           602  'to 602'

 L.1477       620  LOAD_GLOBAL              Server
              622  LOAD_DEREF               'self'
              624  LOAD_FAST                'sockets'
              626  LOAD_FAST                'protocol_factory'

 L.1478       628  LOAD_FAST                'ssl'

 L.1478       630  LOAD_FAST                'backlog'

 L.1478       632  LOAD_FAST                'ssl_handshake_timeout'

 L.1477       634  CALL_FUNCTION_6       6  ''
              636  STORE_FAST               'server'

 L.1479       638  LOAD_FAST                'start_serving'
          640_642  POP_JUMP_IF_FALSE   672  'to 672'

 L.1480       644  LOAD_FAST                'server'
              646  LOAD_METHOD              _start_serving
              648  CALL_METHOD_0         0  ''
              650  POP_TOP          

 L.1483       652  LOAD_GLOBAL              tasks
              654  LOAD_ATTR                sleep
              656  LOAD_CONST               0
              658  LOAD_DEREF               'self'
              660  LOAD_CONST               ('loop',)
              662  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              664  GET_AWAITABLE    
              666  LOAD_CONST               None
              668  YIELD_FROM       
              670  POP_TOP          
            672_0  COME_FROM           640  '640'

 L.1485       672  LOAD_DEREF               'self'
              674  LOAD_ATTR                _debug
          676_678  POP_JUMP_IF_FALSE   692  'to 692'

 L.1486       680  LOAD_GLOBAL              logger
              682  LOAD_METHOD              info
              684  LOAD_STR                 '%r is serving'
              686  LOAD_FAST                'server'
              688  CALL_METHOD_2         2  ''
              690  POP_TOP          
            692_0  COME_FROM           676  '676'

 L.1487       692  LOAD_FAST                'server'
              694  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 324

        async def connect_accepted_socket(self, protocol_factory, sock, *, ssl=None, ssl_handshake_timeout=None):
            """Handle an accepted connection.

        This is used by servers that accept connections outside of
        asyncio but that use asyncio to handle connections.

        This method is a coroutine.  When completed, the coroutine
        returns a (transport, protocol) pair.
        """
            if sock.type != socket.SOCK_STREAM:
                raise ValueError(f"A Stream Socket was expected, got {sock!r}")
            if ssl_handshake_timeout is not None:
                if not ssl:
                    raise ValueError('ssl_handshake_timeout is only meaningful with ssl')
            transport, protocol = await self._create_connection_transport(sock,
              protocol_factory, ssl, '', server_side=True, ssl_handshake_timeout=ssl_handshake_timeout)
            if self._debug:
                sock = transport.get_extra_info'socket'
                logger.debug('%r handled: (%r, %r)', sock, transport, protocol)
            return (
             transport, protocol)

        async def connect_read_pipe(self, protocol_factory, pipe):
            protocol = protocol_factory()
            waiter = self.create_future()
            transport = self._make_read_pipe_transport(pipe, protocol, waiter)
            try:
                await waiter
            except:
                transport.close()
                raise
            else:
                if self._debug:
                    logger.debug('Read pipe %r connected: (%r, %r)', pipe.fileno(), transport, protocol)
                return (
                 transport, protocol)

        async def connect_write_pipe(self, protocol_factory, pipe):
            protocol = protocol_factory()
            waiter = self.create_future()
            transport = self._make_write_pipe_transport(pipe, protocol, waiter)
            try:
                await waiter
            except:
                transport.close()
                raise
            else:
                if self._debug:
                    logger.debug('Write pipe %r connected: (%r, %r)', pipe.fileno(), transport, protocol)
                return (
                 transport, protocol)

        def _log_subprocess(self, msg, stdin, stdout, stderr):
            info = [msg]
            if stdin is not None:
                info.appendf"stdin={_format_pipe(stdin)}"
            if stdout is not None and stderr == subprocess.STDOUT:
                info.appendf"stdout=stderr={_format_pipe(stdout)}"
            else:
                if stdout is not None:
                    info.appendf"stdout={_format_pipe(stdout)}"
                if stderr is not None:
                    info.appendf"stderr={_format_pipe(stderr)}"
            logger.debug' '.joininfo

        async def subprocess_shell(self, protocol_factory, cmd, *, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=False, shell=True, bufsize=0, encoding=None, errors=None, text=None, **kwargs):
            if not isinstance(cmd, (bytes, str)):
                raise ValueError('cmd must be a string')
            else:
                if universal_newlines:
                    raise ValueError('universal_newlines must be False')
                if not shell:
                    raise ValueError('shell must be True')
                if bufsize != 0:
                    raise ValueError('bufsize must be 0')
                if text:
                    raise ValueError('text must be False')
                if encoding is not None:
                    raise ValueError('encoding must be None')
                if errors is not None:
                    raise ValueError('errors must be None')
                protocol = protocol_factory()
                debug_log = None
                if self._debug:
                    debug_log = 'run shell command %r' % cmd
                    self._log_subprocess(debug_log, stdin, stdout, stderr)
                transport = await (self._make_subprocess_transport)(
                 protocol, cmd, True, stdin, stdout, stderr, bufsize, **kwargs)
                if self._debug and debug_log is not None:
                    logger.info('%s: %r', debug_log, transport)
            return (
             transport, protocol)

        async def subprocess_exec(self, protocol_factory, program, *args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=False, shell=False, bufsize=0, encoding=None, errors=None, text=None, **kwargs):
            if universal_newlines:
                raise ValueError('universal_newlines must be False')
            else:
                if shell:
                    raise ValueError('shell must be False')
                if bufsize != 0:
                    raise ValueError('bufsize must be 0')
                if text:
                    raise ValueError('text must be False')
                if encoding is not None:
                    raise ValueError('encoding must be None')
                if errors is not None:
                    raise ValueError('errors must be None')
                popen_args = (program,) + args
                protocol = protocol_factory()
                debug_log = None
                if self._debug:
                    debug_log = f"execute program {program!r}"
                    self._log_subprocess(debug_log, stdin, stdout, stderr)
                transport = await (self._make_subprocess_transport)(
                 protocol, popen_args, False, stdin, stdout, stderr, 
                 bufsize, **kwargs)
                if self._debug and debug_log is not None:
                    logger.info('%s: %r', debug_log, transport)
            return (
             transport, protocol)

        def get_exception_handler(self):
            """Return an exception handler, or None if the default one is in use.
        """
            return self._exception_handler

        def set_exception_handler(self, handler):
            """Set handler as the new event loop exception handler.

        If handler is None, the default exception handler will
        be set.

        If handler is a callable object, it should have a
        signature matching '(loop, context)', where 'loop'
        will be a reference to the active event loop, 'context'
        will be a dict object (see `call_exception_handler()`
        documentation for details about context).
        """
            if handler is not None:
                if not callable(handler):
                    raise TypeError(f"A callable object or None is expected, got {handler!r}")
            self._exception_handler = handler

        def default_exception_handler(self, context):
            """Default exception handler.

        This is called when an exception occurs and no exception
        handler is set, and can be called by a custom exception
        handler that wants to defer to the default behavior.

        This default handler logs the error message and other
        context-dependent information.  In debug mode, a truncated
        stack trace is also appended showing where the given object
        (e.g. a handle or future or task) was created, if any.

        The context parameter has the same meaning as in
        `call_exception_handler()`.
        """
            message = context.get'message'
            if not message:
                message = 'Unhandled exception in event loop'
            else:
                exception = context.get'exception'
                if exception is not None:
                    exc_info = (
                     type(exception), exception, exception.__traceback__)
                else:
                    exc_info = False
            if 'source_traceback' not in context:
                if self._current_handle is not None:
                    if self._current_handle._source_traceback:
                        context['handle_traceback'] = self._current_handle._source_traceback
            log_lines = [
             message]
            for key in sorted(context):
                if key in {'message', 'exception'}:
                    pass
                else:
                    value = context[key]
                    if key == 'source_traceback':
                        tb = ''.jointraceback.format_listvalue
                        value = 'Object created at (most recent call last):\n'
                        value += tb.rstrip()
                    else:
                        if key == 'handle_traceback':
                            tb = ''.jointraceback.format_listvalue
                            value = 'Handle created at (most recent call last):\n'
                            value += tb.rstrip()
                        else:
                            value = repr(value)
                    log_lines.appendf"{key}: {value}"
            else:
                logger.error(('\n'.joinlog_lines), exc_info=exc_info)

        def call_exception_handler(self, context):
            """Call the current event loop's exception handler.

        The context argument is a dict containing the following keys:

        - 'message': Error message;
        - 'exception' (optional): Exception object;
        - 'future' (optional): Future instance;
        - 'task' (optional): Task instance;
        - 'handle' (optional): Handle instance;
        - 'protocol' (optional): Protocol instance;
        - 'transport' (optional): Transport instance;
        - 'socket' (optional): Socket instance;
        - 'asyncgen' (optional): Asynchronous generator that caused
                                 the exception.

        New keys maybe introduced in the future.

        Note: do not overload this method in an event loop subclass.
        For custom exception handling, use the
        `set_exception_handler()` method.
        """
            if self._exception_handler is None:
                try:
                    self.default_exception_handlercontext
                except (SystemExit, KeyboardInterrupt):
                    raise
                except BaseException:
                    logger.error('Exception in default exception handler', exc_info=True)

            else:
                try:
                    self._exception_handlerselfcontext
                except (SystemExit, KeyboardInterrupt):
                    raise
                except BaseException as exc:
                    try:
                        try:
                            self.default_exception_handler{'message':'Unhandled error in exception handler', 
                             'exception':exc, 
                             'context':context}
                        except (SystemExit, KeyboardInterrupt):
                            raise
                        except BaseException:
                            logger.error('Exception in default exception handler while handling an unexpected error in custom exception handler', exc_info=True)

                    finally:
                        exc = None
                        del exc

        def _add_callback(self, handle):
            """Add a Handle to _scheduled (TimerHandle) or _ready."""
            assert isinstance(handle, events.Handle), 'A Handle is required here'
            if handle._cancelled:
                return
            assert not isinstance(handle, events.TimerHandle)
            self._ready.appendhandle

        def _add_callback_signalsafe(self, handle):
            """Like _add_callback() but called from a signal handler."""
            self._add_callbackhandle
            self._write_to_self()

        def _timer_handle_cancelled(self, handle):
            """Notification that a TimerHandle has been cancelled."""
            if handle._scheduled:
                self._timer_cancelled_count += 1

        def _run_once(self):
            """Run one full iteration of the event loop.

        This calls all currently ready callbacks, polls for I/O,
        schedules the resulting callbacks, and finally schedules
        'call_later' callbacks.
        """
            sched_count = len(self._scheduled)
            if sched_count > _MIN_SCHEDULED_TIMER_HANDLES and self._timer_cancelled_count / sched_count > _MIN_CANCELLED_TIMER_HANDLES_FRACTION:
                new_scheduled = []
                for handle in self._scheduled:
                    if handle._cancelled:
                        handle._scheduled = False
                    else:
                        new_scheduled.appendhandle
                else:
                    heapq.heapifynew_scheduled
                    self._scheduled = new_scheduled
                    self._timer_cancelled_count = 0

            else:
                while self._scheduled:
                    if self._scheduled[0]._cancelled:
                        self._timer_cancelled_count -= 1
                        handle = heapq.heappopself._scheduled
                        handle._scheduled = False

                timeout = None
            if self._ready or self._stopping:
                timeout = 0
            else:
                if self._scheduled:
                    when = self._scheduled[0]._when
                    timeout = min(max(0, when - self.time()), MAXIMUM_SELECT_TIMEOUT)
                else:
                    event_list = self._selector.selecttimeout
                    self._process_eventsevent_list
                    end_time = self.time() + self._clock_resolution
                    while True:
                        if self._scheduled:
                            handle = self._scheduled[0]
                            if handle._when >= end_time:
                                break
                            handle = heapq.heappopself._scheduled
                            handle._scheduled = False
                            self._ready.appendhandle

                ntodo = len(self._ready)
                for i in range(ntodo):
                    handle = self._ready.popleft()
                    if handle._cancelled:
                        pass
                    elif self._debug:
                        try:
                            self._current_handle = handle
                            t0 = self.time()
                            handle._run()
                            dt = self.time() - t0
                            if dt >= self.slow_callback_duration:
                                logger.warning('Executing %s took %.3f seconds', _format_handle(handle), dt)
                        finally:
                            self._current_handle = None

                    else:
                        handle._run()
                else:
                    handle = None

        def _set_coroutine_origin_tracking(self, enabled):
            if bool(enabled) == bool(self._coroutine_origin_tracking_enabled):
                return
            elif enabled:
                self._coroutine_origin_tracking_saved_depth = sys.get_coroutine_origin_tracking_depth()
                sys.set_coroutine_origin_tracking_depthconstants.DEBUG_STACK_DEPTH
            else:
                sys.set_coroutine_origin_tracking_depthself._coroutine_origin_tracking_saved_depth
            self._coroutine_origin_tracking_enabled = enabled

        def get_debug(self):
            return self._debug

        def set_debug(self, enabled):
            self._debug = enabled
            if self.is_running():
                self.call_soon_threadsafeself._set_coroutine_origin_trackingenabled