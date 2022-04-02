# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
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
import collections, collections.abc, concurrent.futures, heapq, itertools, logging, os, socket, subprocess, threading, time, traceback, sys, warnings, weakref
try:
    import ssl
except ImportError:
    ssl = None

from . import constants
from . import coroutines
from . import events
from . import futures
from . import protocols
from . import sslproto
from . import tasks
from . import transports
from .log import logger
__all__ = ('BaseEventLoop', )
_MIN_SCHEDULED_TIMER_HANDLES = 100
_MIN_CANCELLED_TIMER_HANDLES_FRACTION = 0.5
_HAS_IPv6 = hasattr(socket, 'AF_INET6')
MAXIMUM_SELECT_TIMEOUT = 86400

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


def _ipaddr_info(host, port, family, type, proto, flowinfo=0, scopeid=0):
    if not hasattr(socket, 'inet_pton'):
        return
    elif not proto not in {0, socket.IPPROTO_TCP, socket.IPPROTO_UDP}:
        if host is None:
            return
        if type == socket.SOCK_STREAM:
            proto = socket.IPPROTO_TCP
    elif type == socket.SOCK_DGRAM:
        proto = socket.IPPROTO_UDP
    else:
        return
    if port is None:
        port = 0
    else:
        if isinstance(port, bytes) and port == b'':
            port = 0
        else:
            if isinstance(port, str) and port == '':
                port = 0
            else:
                try:
                    port = int(port)
                except (TypeError, ValueError):
                    return

                if family == socket.AF_UNSPEC:
                    afs = [
                     socket.AF_INET]
                    if _HAS_IPv6:
                        afs.append(socket.AF_INET6)
                else:
                    afs = [
                     family]
                if isinstance(host, bytes):
                    host = host.decode('idna')
                if '%' in host:
                    return
                for af in afs:
                    try:
                        socket.inet_pton(af, host)
                        if _HAS_IPv6:
                            if af == socket.AF_INET6:
                                return (
                                 af, type, proto, '', (host, port, flowinfo, scopeid))
                        return (
                         af, type, proto, '', (host, port))
                    except OSError:
                        pass


def _run_until_complete_cb(fut):
    if not fut.cancelled():
        exc = fut.exception()
        if isinstance(exc, BaseException):
            if not isinstance(exc, Exception):
                return
    futures._get_loop(fut).stop()


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
            transp.set_protocol(self)
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
                self._write_ready_fut.set_exception(ConnectionError('Connection is closed by peer'))
            else:
                self._write_ready_fut.set_exception(exc)
        self._proto.connection_lost(exc)

    def pause_writing(self):
        if self._write_ready_fut is not None:
            return
        self._write_ready_fut = self._transport._loop.create_future()

    def resume_writing(self):
        if self._write_ready_fut is None:
            return
        self._write_ready_fut.set_result(False)
        self._write_ready_fut = None

    def data_received(self, data):
        raise RuntimeError('Invalid state: reading should be paused')

    def eof_received(self):
        raise RuntimeError('Invalid state: reading should be paused')

    async def restore(self):
        self._transport.set_protocol(self._proto)
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
                waiter.set_result(waiter)

    def _start_serving(self):
        if self._serving:
            return
        self._serving = True
        for sock in self._sockets:
            sock.listen(self._backlog)
            self._loop._start_serving(self._protocol_factory, sock, self._ssl_context, self, self._backlog, self._ssl_handshake_timeout)

    def get_loop(self):
        return self._loop

    def is_serving(self):
        return self._serving

    @property
    def sockets(self):
        if self._sockets is None:
            return []
        return list(self._sockets)

    def close(self):
        sockets = self._sockets
        if sockets is None:
            return
        self._sockets = None
        for sock in sockets:
            self._loop._stop_serving(sock)

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
            except futures.CancelledError:
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
        self._waiters.append(waiter)
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
        self._clock_resolution = time.get_clock_info('monotonic').resolution
        self._exception_handler = None
        self.set_debug(coroutines._is_debug_mode())
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

    def create_task(self, coro):
        """Schedule a coroutine object.

        Return a task object.
        """
        self._check_closed()
        if self._task_factory is None:
            task = tasks.Task(coro, loop=self)
            if task._source_traceback:
                del task._source_traceback[-1]
        else:
            task = self._task_factory(self, coro)
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
        self._asyncgens.discard(agen)
        if not self.is_closed():
            self.call_soon_threadsafe(self.create_task, agen.aclose())

    def _asyncgen_firstiter_hook(self, agen):
        if self._asyncgens_shutdown_called:
            warnings.warn(f"asynchronous generator {agen!r} was scheduled after loop.shutdown_asyncgens() call",
              ResourceWarning,
              source=self)
        self._asyncgens.add(agen)

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
                self.call_exception_handler({'message':f"an error occurred during closing of asynchronous generator {agen!r}", 
                 'exception':result, 
                 'asyncgen':agen})

    def run_forever(self):
        """Run until stop() is called."""
        self._check_closed()
        if self.is_running():
            raise RuntimeError('This event loop is already running')
        if events._get_running_loop() is not None:
            raise RuntimeError('Cannot run the event loop while another loop is running')
        self._set_coroutine_origin_tracking(self._debug)
        self._thread_id = threading.get_ident()
        old_agen_hooks = sys.get_asyncgen_hooks()
        sys.set_asyncgen_hooks(firstiter=(self._asyncgen_firstiter_hook), finalizer=(self._asyncgen_finalizer_hook))
        try:
            events._set_running_loop(self)
            while 1:
                self._run_once()
                if self._stopping:
                    break

        finally:
            self._stopping = False
            self._thread_id = None
            events._set_running_loop(None)
            self._set_coroutine_origin_tracking(False)
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
        new_task = not futures.isfuture(future)
        future = tasks.ensure_future(future, loop=self)
        if new_task:
            future._log_destroy_pending = False
        future.add_done_callback(_run_until_complete_cb)
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
            future.remove_done_callback(_run_until_complete_cb)

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
            logger.debug('Close %r', self)
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

    def __del__(self):
        if not self.is_closed():
            warnings.warn(f"unclosed event loop {self!r}", ResourceWarning, source=self)
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
            self._check_callback(callback, 'call_at')
        timer = events.TimerHandle(when, callback, args, self, context)
        if timer._source_traceback:
            del timer._source_traceback[-1]
        heapq.heappush(self._scheduled, timer)
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
            self._check_callback(callback, 'call_soon')
        handle = self._call_soon(callback, args, context)
        if handle._source_traceback:
            del handle._source_traceback[-1]
        return handle

    def _check_callback(self, callback, method):
        if coroutines.iscoroutine(callback) or coroutines.iscoroutinefunction(callback):
            raise TypeError(f"coroutines cannot be used with {method}()")
        if not callable(callback):
            raise TypeError(f"a callable object was expected by {method}(), got {callback!r}")

    def _call_soon(self, callback, args, context):
        handle = events.Handle(callback, args, self, context)
        if handle._source_traceback:
            del handle._source_traceback[-1]
        self._ready.append(handle)
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
            self._check_callback(callback, 'call_soon_threadsafe')
        handle = self._call_soon(callback, args, context)
        if handle._source_traceback:
            del handle._source_traceback[-1]
        self._write_to_self()
        return handle

    def run_in_executor(self, executor, func, *args):
        self._check_closed()
        if self._debug:
            self._check_callback(func, 'run_in_executor')
        if executor is None:
            executor = self._default_executor
            if executor is None:
                executor = concurrent.futures.ThreadPoolExecutor()
                self._default_executor = executor
        return futures.wrap_future((executor.submit)(func, *args),
          loop=self)

    def set_default_executor(self, executor):
        self._default_executor = executor

    def _getaddrinfo_debug(self, host, port, family, type, proto, flags):
        msg = [
         f"{host}:{port!r}"]
        if family:
            msg.append(f"family={family!r}")
        else:
            if type:
                msg.append(f"type={type!r}")
            if proto:
                msg.append(f"proto={proto!r}")
            if flags:
                msg.append(f"flags={flags!r}")
            msg = ', '.join(msg)
            logger.debug('Get address info %s', msg)
            t0 = self.time()
            addrinfo = socket.getaddrinfo(host, port, family, type, proto, flags)
            dt = self.time() - t0
            msg = f"Getting address info {msg} took {dt * 1000.0:.3f}ms: {addrinfo!r}"
            if dt >= self.slow_callback_duration:
                logger.info(msg)
            else:
                logger.debug(msg)
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
        except events.SendfileNotAvailableError as exc:
            try:
                if not fallback:
                    raise
            finally:
                exc = None
                del exc

        return await self._sock_sendfile_fallback(sock, file, offset, count)

    async def _sock_sendfile_native(self, sock, file, offset, count):
        raise events.SendfileNotAvailableError(f"syscall sendfile is not available for socket {sock!r} and file {{file!r}} combination")

    async def _sock_sendfile_fallback(self, sock, file, offset, count):
        if offset:
            file.seek(offset)
        blocksize = min(count, constants.SENDFILE_FALLBACK_READBUFFER_SIZE) if count else constants.SENDFILE_FALLBACK_READBUFFER_SIZE
        buf = bytearray(blocksize)
        total_sent = 0
        try:
            while True:
                if count:
                    blocksize = min(count - total_sent, blocksize)
                    if blocksize <= 0:
                        break
                view = memoryview(buf)[:blocksize]
                read = await self.run_in_executor(None, file.readinto, view)
                if not read:
                    break
                await self.sock_sendall(sock, view[:read])
                total_sent += read

            return total_sent
        finally:
            if total_sent > 0:
                if hasattr(file, 'seek'):
                    file.seek(offset + total_sent)

    def _check_sendfile_params(self, sock, file, offset, count):
        if 'b' not in getattr(file, 'mode', 'b'):
            raise ValueError('file should be opened in binary mode')
        else:
            if not sock.type == socket.SOCK_STREAM:
                raise ValueError('only SOCK_STREAM type sockets are supported')
            if count is not None:
                if not isinstance(count, int):
                    raise TypeError('count must be a positive integer (got {!r})'.format(count))
                if count <= 0:
                    raise ValueError('count must be a positive integer (got {!r})'.format(count))
            assert isinstance(offset, int), 'offset must be a non-negative integer (got {!r})'.format(offset)
        if offset < 0:
            raise ValueError('offset must be a non-negative integer (got {!r})'.format(offset))

    async def create_connection(self, protocol_factory, host=None, port=None, *, ssl=None, family=0, proto=0, flags=0, sock=None, local_addr=None, server_hostname=None, ssl_handshake_timeout=None):
        """Connect to a TCP server.

        Create a streaming transport connection to a given Internet host and
        port: socket family AF_INET or socket.AF_INET6 depending on host (or
        family if specified), socket type SOCK_STREAM. protocol_factory must be
        a callable returning a protocol instance.

        This method is a coroutine which will try to establish the connection
        in the background.  When successful, the coroutine returns a
        (transport, protocol) pair.
        """
        if server_hostname is not None:
            if not ssl:
                raise ValueError('server_hostname is only meaningful with ssl')
            elif server_hostname is None and ssl:
                if not host:
                    raise ValueError('You must set server_hostname when using ssl without a host')
                server_hostname = host
            if ssl_handshake_timeout is not None:
                if not ssl:
                    raise ValueError('ssl_handshake_timeout is only meaningful with ssl')
            if host is not None or port is not None:
                if sock is not None:
                    raise ValueError('host/port and sock can not be specified at the same time')
                else:
                    infos = await self._ensure_resolved((
                     host, port),
                      family=family, type=(socket.SOCK_STREAM),
                      proto=proto,
                      flags=flags,
                      loop=self)
                    if not infos:
                        raise OSError('getaddrinfo() returned empty list')
                    if local_addr is not None:
                        laddr_infos = await self._ensure_resolved(local_addr,
                          family=family, type=(socket.SOCK_STREAM),
                          proto=proto,
                          flags=flags,
                          loop=self)
                        if not laddr_infos:
                            raise OSError('getaddrinfo() returned empty list')
                    exceptions = []
                    for family, type, proto, cname, address in infos:
                        try:
                            sock = socket.socket(family=family, type=type, proto=proto)
                            sock.setblocking(False)
                            if local_addr is not None:
                                for _, _, _, _, laddr in laddr_infos:
                                    try:
                                        sock.bind(laddr)
                                        break
                                    except OSError as exc:
                                        try:
                                            msg = f"error while attempting to bind on address {laddr!r}: {exc.strerror.lower()}"
                                            exc = OSError(exc.errno, msg)
                                            exceptions.append(exc)
                                        finally:
                                            exc = None
                                            del exc

                                else:
                                    sock.close()
                                    sock = None
                                    continue

                            if self._debug:
                                logger.debug('connect %r to %r', sock, address)
                            await self.sock_connect(sock, address)
                        except OSError as exc:
                            try:
                                if sock is not None:
                                    sock.close()
                                exceptions.append(exc)
                            finally:
                                exc = None
                                del exc

                        except:
                            if sock is not None:
                                sock.close()
                            raise
                        else:
                            break
                    else:
                        if len(exceptions) == 1:
                            raise exceptions[0]
                        else:
                            model = str(exceptions[0])
                            if all((str(exc) == model for exc in exceptions)):
                                raise exceptions[0]

                    raise OSError('Multiple exceptions: {}'.format(', '.join((str(exc) for exc in exceptions))))
        else:
            if sock is None:
                raise ValueError('host and port was not specified and no sock specified')
            if sock.type != socket.SOCK_STREAM:
                raise ValueError(f"A Stream Socket was expected, got {sock!r}")
        transport, protocol = await self._create_connection_transport(sock,
          protocol_factory, ssl, server_hostname, ssl_handshake_timeout=ssl_handshake_timeout)
        if self._debug:
            sock = transport.get_extra_info('socket')
            logger.debug('%r connected to %s:%r: (%r, %r)', sock, host, port, transport, protocol)
        return (
         transport, protocol)

    async def _create_connection_transport(self, sock, protocol_factory, ssl, server_hostname, server_side=False, ssl_handshake_timeout=None):
        sock.setblocking(False)
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

        return (transport, protocol)

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
                except events.SendfileNotAvailableError as exc:
                    try:
                        if not fallback:
                            raise
                    finally:
                        exc = None
                        del exc

            assert fallback, f"fallback is disabled and native sendfile is not supported for transport {transport!r}"
        return await self._sendfile_fallback(transport, file, offset, count)

    async def _sendfile_native(self, transp, file, offset, count):
        raise events.SendfileNotAvailableError('sendfile syscall is not supported')

    async def _sendfile_fallback(self, transp, file, offset, count):
        if offset:
            file.seek(offset)
        blocksize = min(count, 16384) if count else 16384
        buf = bytearray(blocksize)
        total_sent = 0
        proto = _SendfileFallbackProtocol(transp)
        try:
            while 1:
                if count:
                    blocksize = min(count - total_sent, blocksize)
                    if blocksize <= 0:
                        return total_sent
                view = memoryview(buf)[:blocksize]
                read = await self.run_in_executor(None, file.readinto, view)
                if not read:
                    return total_sent
                    await proto.drain()
                    transp.write(view[:read])
                    total_sent += read

        finally:
            if total_sent > 0:
                if hasattr(file, 'seek'):
                    file.seek(offset + total_sent)
            await proto.restore()

    async def start_tls(self, transport, protocol, sslcontext, *, server_side=False, server_hostname=None, ssl_handshake_timeout=None):
        """Upgrade transport to TLS.

        Return a new transport that *protocol* should start using
        immediately.
        """
        if ssl is None:
            raise RuntimeError('Python ssl module is not available')
        elif not isinstance(sslcontext, ssl.SSLContext):
            raise TypeError(f"sslcontext is expected to be an instance of ssl.SSLContext, got {sslcontext!r}")
        else:
            if not getattr(transport, '_start_tls_compatible', False):
                raise TypeError(f"transport {transport!r} is not supported by start_tls()")
            waiter = self.create_future()
            ssl_protocol = sslproto.SSLProtocol(self,
              protocol, sslcontext, waiter, server_side,
              server_hostname, ssl_handshake_timeout=ssl_handshake_timeout,
              call_connection_made=False)
            transport.pause_reading()
            transport.set_protocol(ssl_protocol)
            conmade_cb = self.call_soon(ssl_protocol.connection_made, transport)
            resume_cb = self.call_soon(transport.resume_reading)
            try:
                await waiter
            except Exception:
                transport.close()
                conmade_cb.cancel()
                resume_cb.cancel()
                raise

        return ssl_protocol._app_transport

    async def create_datagram_endpoint--- This code section failed: ---

 L.1144         0  LOAD_FAST                'sock'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE   148  'to 148'

 L.1145         8  LOAD_FAST                'sock'
               10  LOAD_ATTR                type
               12  LOAD_GLOBAL              socket
               14  LOAD_ATTR                SOCK_DGRAM
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L.1146        20  LOAD_GLOBAL              ValueError

 L.1147        22  LOAD_STR                 'A UDP Socket was expected, got '
               24  LOAD_FAST                'sock'
               26  FORMAT_VALUE          2  '!r'
               28  BUILD_STRING_2        2 
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            18  '18'

 L.1148        34  LOAD_DEREF               'local_addr'
               36  POP_JUMP_IF_TRUE     66  'to 66'
               38  LOAD_DEREF               'remote_addr'
               40  POP_JUMP_IF_TRUE     66  'to 66'

 L.1149        42  LOAD_FAST                'family'
               44  POP_JUMP_IF_TRUE     66  'to 66'
               46  LOAD_FAST                'proto'
               48  POP_JUMP_IF_TRUE     66  'to 66'
               50  LOAD_FAST                'flags'
               52  POP_JUMP_IF_TRUE     66  'to 66'

 L.1150        54  LOAD_FAST                'reuse_address'
               56  POP_JUMP_IF_TRUE     66  'to 66'
               58  LOAD_FAST                'reuse_port'
               60  POP_JUMP_IF_TRUE     66  'to 66'
               62  LOAD_FAST                'allow_broadcast'
               64  POP_JUMP_IF_FALSE   130  'to 130'
             66_0  COME_FROM            60  '60'
             66_1  COME_FROM            56  '56'
             66_2  COME_FROM            52  '52'
             66_3  COME_FROM            48  '48'
             66_4  COME_FROM            44  '44'
             66_5  COME_FROM            40  '40'
             66_6  COME_FROM            36  '36'

 L.1152        66  LOAD_GLOBAL              dict
               68  LOAD_DEREF               'local_addr'
               70  LOAD_DEREF               'remote_addr'

 L.1153        72  LOAD_FAST                'family'
               74  LOAD_FAST                'proto'
               76  LOAD_FAST                'flags'

 L.1154        78  LOAD_FAST                'reuse_address'
               80  LOAD_FAST                'reuse_port'

 L.1155        82  LOAD_FAST                'allow_broadcast'
               84  LOAD_CONST               ('local_addr', 'remote_addr', 'family', 'proto', 'flags', 'reuse_address', 'reuse_port', 'allow_broadcast')
               86  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
               88  STORE_FAST               'opts'

 L.1156        90  LOAD_STR                 ', '
               92  LOAD_METHOD              join
               94  LOAD_GENEXPR             '<code_object <genexpr>>'
               96  LOAD_STR                 'BaseEventLoop.create_datagram_endpoint.<locals>.<genexpr>'
               98  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              100  LOAD_FAST                'opts'
              102  LOAD_METHOD              items
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  GET_ITER         
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  CALL_METHOD_1         1  '1 positional argument'
              112  STORE_FAST               'problems'

 L.1157       114  LOAD_GLOBAL              ValueError

 L.1158       116  LOAD_STR                 'socket modifier keyword arguments can not be used when sock is specified. ('
              118  LOAD_FAST                'problems'
              120  FORMAT_VALUE          0  ''
              122  LOAD_STR                 ')'
              124  BUILD_STRING_3        3 
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM            64  '64'

 L.1160       130  LOAD_FAST                'sock'
              132  LOAD_METHOD              setblocking
              134  LOAD_CONST               False
              136  CALL_METHOD_1         1  '1 positional argument'
              138  POP_TOP          

 L.1161       140  LOAD_CONST               None
              142  STORE_FAST               'r_addr'
          144_146  JUMP_FORWARD        838  'to 838'
            148_0  COME_FROM             6  '6'

 L.1163       148  LOAD_DEREF               'local_addr'
              150  POP_JUMP_IF_TRUE    190  'to 190'
              152  LOAD_DEREF               'remote_addr'
              154  POP_JUMP_IF_TRUE    190  'to 190'

 L.1164       156  LOAD_FAST                'family'
              158  LOAD_CONST               0
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   172  'to 172'

 L.1165       164  LOAD_GLOBAL              ValueError
              166  LOAD_STR                 'unexpected address family'
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  RAISE_VARARGS_1       1  'exception instance'
            172_0  COME_FROM           162  '162'

 L.1166       172  LOAD_FAST                'family'
              174  LOAD_FAST                'proto'
              176  BUILD_TUPLE_2         2 
              178  LOAD_CONST               (None, None)
              180  BUILD_TUPLE_2         2 
              182  BUILD_TUPLE_1         1 
              184  STORE_FAST               'addr_pairs_info'
          186_188  JUMP_FORWARD        512  'to 512'
            190_0  COME_FROM           154  '154'
            190_1  COME_FROM           150  '150'

 L.1167       190  LOAD_GLOBAL              hasattr
              192  LOAD_GLOBAL              socket
              194  LOAD_STR                 'AF_UNIX'
              196  CALL_FUNCTION_2       2  '2 positional arguments'
          198_200  POP_JUMP_IF_FALSE   278  'to 278'
              202  LOAD_FAST                'family'
              204  LOAD_GLOBAL              socket
              206  LOAD_ATTR                AF_UNIX
              208  COMPARE_OP               ==
          210_212  POP_JUMP_IF_FALSE   278  'to 278'

 L.1168       214  SETUP_LOOP          258  'to 258'
              216  LOAD_DEREF               'local_addr'
              218  LOAD_DEREF               'remote_addr'
              220  BUILD_TUPLE_2         2 
              222  GET_ITER         
            224_0  COME_FROM           244  '244'
            224_1  COME_FROM           234  '234'
              224  FOR_ITER            256  'to 256'
              226  STORE_FAST               'addr'

 L.1169       228  LOAD_FAST                'addr'
              230  LOAD_CONST               None
              232  COMPARE_OP               is-not
              234  POP_JUMP_IF_FALSE   224  'to 224'
              236  LOAD_GLOBAL              isinstance
              238  LOAD_FAST                'addr'
              240  LOAD_GLOBAL              str
              242  CALL_FUNCTION_2       2  '2 positional arguments'
              244  POP_JUMP_IF_TRUE    224  'to 224'

 L.1170       246  LOAD_GLOBAL              TypeError
              248  LOAD_STR                 'string is expected'
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  RAISE_VARARGS_1       1  'exception instance'
              254  JUMP_BACK           224  'to 224'
              256  POP_BLOCK        
            258_0  COME_FROM_LOOP      214  '214'

 L.1171       258  LOAD_FAST                'family'
              260  LOAD_FAST                'proto'
              262  BUILD_TUPLE_2         2 

 L.1172       264  LOAD_DEREF               'local_addr'
              266  LOAD_DEREF               'remote_addr'
              268  BUILD_TUPLE_2         2 
              270  BUILD_TUPLE_2         2 
              272  BUILD_TUPLE_1         1 
              274  STORE_FAST               'addr_pairs_info'
              276  JUMP_FORWARD        512  'to 512'
            278_0  COME_FROM           210  '210'
            278_1  COME_FROM           198  '198'

 L.1175       278  LOAD_GLOBAL              collections
              280  LOAD_METHOD              OrderedDict
              282  CALL_METHOD_0         0  '0 positional arguments'
              284  STORE_FAST               'addr_infos'

 L.1176       286  SETUP_LOOP          474  'to 474'
              288  LOAD_CONST               0
              290  LOAD_DEREF               'local_addr'
              292  BUILD_TUPLE_2         2 
              294  LOAD_CONST               1
              296  LOAD_DEREF               'remote_addr'
              298  BUILD_TUPLE_2         2 
              300  BUILD_TUPLE_2         2 
              302  GET_ITER         
            304_0  COME_FROM           318  '318'
              304  FOR_ITER            472  'to 472'
              306  UNPACK_SEQUENCE_2     2 
              308  STORE_FAST               'idx'
              310  STORE_FAST               'addr'

 L.1177       312  LOAD_FAST                'addr'
              314  LOAD_CONST               None
              316  COMPARE_OP               is-not
          318_320  POP_JUMP_IF_FALSE   304  'to 304'

 L.1178       322  LOAD_GLOBAL              isinstance
              324  LOAD_FAST                'addr'
              326  LOAD_GLOBAL              tuple
              328  CALL_FUNCTION_2       2  '2 positional arguments'
          330_332  POP_JUMP_IF_FALSE   348  'to 348'
              334  LOAD_GLOBAL              len
              336  LOAD_FAST                'addr'
              338  CALL_FUNCTION_1       1  '1 positional argument'
              340  LOAD_CONST               2
              342  COMPARE_OP               ==
          344_346  POP_JUMP_IF_TRUE    356  'to 356'
            348_0  COME_FROM           330  '330'
              348  LOAD_ASSERT              AssertionError

 L.1179       350  LOAD_STR                 '2-tuple is expected'
              352  CALL_FUNCTION_1       1  '1 positional argument'
              354  RAISE_VARARGS_1       1  'exception instance'
            356_0  COME_FROM           344  '344'

 L.1181       356  LOAD_FAST                'self'
              358  LOAD_ATTR                _ensure_resolved

 L.1182       360  LOAD_FAST                'addr'
              362  LOAD_FAST                'family'
              364  LOAD_GLOBAL              socket
              366  LOAD_ATTR                SOCK_DGRAM

 L.1183       368  LOAD_FAST                'proto'
              370  LOAD_FAST                'flags'
              372  LOAD_FAST                'self'
              374  LOAD_CONST               ('family', 'type', 'proto', 'flags', 'loop')
              376  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              378  GET_AWAITABLE    
              380  LOAD_CONST               None
              382  YIELD_FROM       
              384  STORE_FAST               'infos'

 L.1184       386  LOAD_FAST                'infos'
          388_390  POP_JUMP_IF_TRUE    400  'to 400'

 L.1185       392  LOAD_GLOBAL              OSError
              394  LOAD_STR                 'getaddrinfo() returned empty list'
              396  CALL_FUNCTION_1       1  '1 positional argument'
              398  RAISE_VARARGS_1       1  'exception instance'
            400_0  COME_FROM           388  '388'

 L.1187       400  SETUP_LOOP          468  'to 468'
              402  LOAD_FAST                'infos'
              404  GET_ITER         
              406  FOR_ITER            466  'to 466'
              408  UNPACK_SEQUENCE_5     5 
              410  STORE_FAST               'fam'
              412  STORE_FAST               '_'
              414  STORE_FAST               'pro'
              416  STORE_FAST               '_'
              418  STORE_FAST               'address'

 L.1188       420  LOAD_FAST                'fam'
              422  LOAD_FAST                'pro'
              424  BUILD_TUPLE_2         2 
              426  STORE_FAST               'key'

 L.1189       428  LOAD_FAST                'key'
              430  LOAD_FAST                'addr_infos'
              432  COMPARE_OP               not-in
          434_436  POP_JUMP_IF_FALSE   450  'to 450'

 L.1190       438  LOAD_CONST               None
              440  LOAD_CONST               None
              442  BUILD_LIST_2          2 
              444  LOAD_FAST                'addr_infos'
              446  LOAD_FAST                'key'
              448  STORE_SUBSCR     
            450_0  COME_FROM           434  '434'

 L.1191       450  LOAD_FAST                'address'
              452  LOAD_FAST                'addr_infos'
              454  LOAD_FAST                'key'
              456  BINARY_SUBSCR    
              458  LOAD_FAST                'idx'
              460  STORE_SUBSCR     
          462_464  JUMP_BACK           406  'to 406'
              466  POP_BLOCK        
            468_0  COME_FROM_LOOP      400  '400'
          468_470  JUMP_BACK           304  'to 304'
              472  POP_BLOCK        
            474_0  COME_FROM_LOOP      286  '286'

 L.1195       474  LOAD_CLOSURE             'local_addr'
              476  LOAD_CLOSURE             'remote_addr'
              478  BUILD_TUPLE_2         2 
              480  LOAD_LISTCOMP            '<code_object <listcomp>>'
              482  LOAD_STR                 'BaseEventLoop.create_datagram_endpoint.<locals>.<listcomp>'
              484  MAKE_FUNCTION_8          'closure'
              486  LOAD_FAST                'addr_infos'
              488  LOAD_METHOD              items
              490  CALL_METHOD_0         0  '0 positional arguments'
              492  GET_ITER         
              494  CALL_FUNCTION_1       1  '1 positional argument'
              496  STORE_FAST               'addr_pairs_info'

 L.1199       498  LOAD_FAST                'addr_pairs_info'
          500_502  POP_JUMP_IF_TRUE    512  'to 512'

 L.1200       504  LOAD_GLOBAL              ValueError
              506  LOAD_STR                 'can not get address information'
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  RAISE_VARARGS_1       1  'exception instance'
            512_0  COME_FROM           500  '500'
            512_1  COME_FROM           276  '276'
            512_2  COME_FROM           186  '186'

 L.1202       512  BUILD_LIST_0          0 
              514  STORE_FAST               'exceptions'

 L.1204       516  LOAD_FAST                'reuse_address'
              518  LOAD_CONST               None
              520  COMPARE_OP               is
          522_524  POP_JUMP_IF_FALSE   548  'to 548'

 L.1205       526  LOAD_GLOBAL              os
              528  LOAD_ATTR                name
              530  LOAD_STR                 'posix'
              532  COMPARE_OP               ==
          534_536  JUMP_IF_FALSE_OR_POP   546  'to 546'
              538  LOAD_GLOBAL              sys
              540  LOAD_ATTR                platform
              542  LOAD_STR                 'cygwin'
              544  COMPARE_OP               !=
            546_0  COME_FROM           534  '534'
              546  STORE_FAST               'reuse_address'
            548_0  COME_FROM           522  '522'

 L.1207   548_550  SETUP_LOOP          838  'to 838'

 L.1208       552  LOAD_FAST                'addr_pairs_info'
              554  GET_ITER         
          556_558  FOR_ITER            828  'to 828'
              560  UNPACK_SEQUENCE_2     2 
              562  UNPACK_SEQUENCE_2     2 
              564  STORE_FAST               'family'
              566  STORE_FAST               'proto'
              568  UNPACK_SEQUENCE_2     2 
              570  STORE_FAST               'local_address'
              572  STORE_FAST               'remote_address'

 L.1209       574  LOAD_CONST               None
              576  STORE_FAST               'sock'

 L.1210       578  LOAD_CONST               None
              580  STORE_FAST               'r_addr'

 L.1211       582  SETUP_EXCEPT        728  'to 728'

 L.1212       584  LOAD_GLOBAL              socket
              586  LOAD_ATTR                socket

 L.1213       588  LOAD_FAST                'family'
              590  LOAD_GLOBAL              socket
              592  LOAD_ATTR                SOCK_DGRAM
              594  LOAD_FAST                'proto'
              596  LOAD_CONST               ('family', 'type', 'proto')
              598  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              600  STORE_FAST               'sock'

 L.1214       602  LOAD_FAST                'reuse_address'
          604_606  POP_JUMP_IF_FALSE   626  'to 626'

 L.1215       608  LOAD_FAST                'sock'
              610  LOAD_METHOD              setsockopt

 L.1216       612  LOAD_GLOBAL              socket
              614  LOAD_ATTR                SOL_SOCKET
              616  LOAD_GLOBAL              socket
              618  LOAD_ATTR                SO_REUSEADDR
              620  LOAD_CONST               1
              622  CALL_METHOD_3         3  '3 positional arguments'
              624  POP_TOP          
            626_0  COME_FROM           604  '604'

 L.1217       626  LOAD_FAST                'reuse_port'
          628_630  POP_JUMP_IF_FALSE   640  'to 640'

 L.1218       632  LOAD_GLOBAL              _set_reuseport
              634  LOAD_FAST                'sock'
              636  CALL_FUNCTION_1       1  '1 positional argument'
              638  POP_TOP          
            640_0  COME_FROM           628  '628'

 L.1219       640  LOAD_FAST                'allow_broadcast'
          642_644  POP_JUMP_IF_FALSE   664  'to 664'

 L.1220       646  LOAD_FAST                'sock'
              648  LOAD_METHOD              setsockopt

 L.1221       650  LOAD_GLOBAL              socket
              652  LOAD_ATTR                SOL_SOCKET
              654  LOAD_GLOBAL              socket
              656  LOAD_ATTR                SO_BROADCAST
              658  LOAD_CONST               1
              660  CALL_METHOD_3         3  '3 positional arguments'
              662  POP_TOP          
            664_0  COME_FROM           642  '642'

 L.1222       664  LOAD_FAST                'sock'
              666  LOAD_METHOD              setblocking
              668  LOAD_CONST               False
              670  CALL_METHOD_1         1  '1 positional argument'
              672  POP_TOP          

 L.1224       674  LOAD_DEREF               'local_addr'
          676_678  POP_JUMP_IF_FALSE   690  'to 690'

 L.1225       680  LOAD_FAST                'sock'
              682  LOAD_METHOD              bind
              684  LOAD_FAST                'local_address'
              686  CALL_METHOD_1         1  '1 positional argument'
              688  POP_TOP          
            690_0  COME_FROM           676  '676'

 L.1226       690  LOAD_DEREF               'remote_addr'
          692_694  POP_JUMP_IF_FALSE   724  'to 724'

 L.1227       696  LOAD_FAST                'allow_broadcast'
          698_700  POP_JUMP_IF_TRUE    720  'to 720'

 L.1228       702  LOAD_FAST                'self'
              704  LOAD_METHOD              sock_connect
              706  LOAD_FAST                'sock'
              708  LOAD_FAST                'remote_address'
              710  CALL_METHOD_2         2  '2 positional arguments'
              712  GET_AWAITABLE    
              714  LOAD_CONST               None
              716  YIELD_FROM       
              718  POP_TOP          
            720_0  COME_FROM           698  '698'

 L.1229       720  LOAD_FAST                'remote_address'
              722  STORE_FAST               'r_addr'
            724_0  COME_FROM           692  '692'
              724  POP_BLOCK        
              726  JUMP_FORWARD        822  'to 822'
            728_0  COME_FROM_EXCEPT    582  '582'

 L.1230       728  DUP_TOP          
              730  LOAD_GLOBAL              OSError
              732  COMPARE_OP               exception-match
          734_736  POP_JUMP_IF_FALSE   790  'to 790'
              738  POP_TOP          
              740  STORE_FAST               'exc'
              742  POP_TOP          
              744  SETUP_FINALLY       778  'to 778'

 L.1231       746  LOAD_FAST                'sock'
              748  LOAD_CONST               None
              750  COMPARE_OP               is-not
          752_754  POP_JUMP_IF_FALSE   764  'to 764'

 L.1232       756  LOAD_FAST                'sock'
              758  LOAD_METHOD              close
              760  CALL_METHOD_0         0  '0 positional arguments'
              762  POP_TOP          
            764_0  COME_FROM           752  '752'

 L.1233       764  LOAD_FAST                'exceptions'
              766  LOAD_METHOD              append
              768  LOAD_FAST                'exc'
              770  CALL_METHOD_1         1  '1 positional argument'
              772  POP_TOP          
              774  POP_BLOCK        
              776  LOAD_CONST               None
            778_0  COME_FROM_FINALLY   744  '744'
              778  LOAD_CONST               None
              780  STORE_FAST               'exc'
              782  DELETE_FAST              'exc'
              784  END_FINALLY      
              786  POP_EXCEPT       
              788  JUMP_BACK           556  'to 556'
            790_0  COME_FROM           734  '734'

 L.1234       790  POP_TOP          
              792  POP_TOP          
              794  POP_TOP          

 L.1235       796  LOAD_FAST                'sock'
              798  LOAD_CONST               None
              800  COMPARE_OP               is-not
          802_804  POP_JUMP_IF_FALSE   814  'to 814'

 L.1236       806  LOAD_FAST                'sock'
              808  LOAD_METHOD              close
              810  CALL_METHOD_0         0  '0 positional arguments'
              812  POP_TOP          
            814_0  COME_FROM           802  '802'

 L.1237       814  RAISE_VARARGS_0       0  'reraise'
              816  POP_EXCEPT       
              818  JUMP_BACK           556  'to 556'
              820  END_FINALLY      
            822_0  COME_FROM           726  '726'

 L.1239       822  BREAK_LOOP       
          824_826  JUMP_BACK           556  'to 556'
              828  POP_BLOCK        

 L.1241       830  LOAD_FAST                'exceptions'
              832  LOAD_CONST               0
              834  BINARY_SUBSCR    
              836  RAISE_VARARGS_1       1  'exception instance'
            838_0  COME_FROM_LOOP      548  '548'
            838_1  COME_FROM           144  '144'

 L.1243       838  LOAD_FAST                'protocol_factory'
              840  CALL_FUNCTION_0       0  '0 positional arguments'
              842  STORE_FAST               'protocol'

 L.1244       844  LOAD_FAST                'self'
              846  LOAD_METHOD              create_future
              848  CALL_METHOD_0         0  '0 positional arguments'
              850  STORE_FAST               'waiter'

 L.1245       852  LOAD_FAST                'self'
              854  LOAD_METHOD              _make_datagram_transport

 L.1246       856  LOAD_FAST                'sock'
              858  LOAD_FAST                'protocol'
              860  LOAD_FAST                'r_addr'
              862  LOAD_FAST                'waiter'
              864  CALL_METHOD_4         4  '4 positional arguments'
              866  STORE_FAST               'transport'

 L.1247       868  LOAD_FAST                'self'
              870  LOAD_ATTR                _debug
          872_874  POP_JUMP_IF_FALSE   918  'to 918'

 L.1248       876  LOAD_DEREF               'local_addr'
          878_880  POP_JUMP_IF_FALSE   902  'to 902'

 L.1249       882  LOAD_GLOBAL              logger
              884  LOAD_METHOD              info
              886  LOAD_STR                 'Datagram endpoint local_addr=%r remote_addr=%r created: (%r, %r)'

 L.1251       888  LOAD_DEREF               'local_addr'
              890  LOAD_DEREF               'remote_addr'
              892  LOAD_FAST                'transport'
              894  LOAD_FAST                'protocol'
              896  CALL_METHOD_5         5  '5 positional arguments'
              898  POP_TOP          
              900  JUMP_FORWARD        918  'to 918'
            902_0  COME_FROM           878  '878'

 L.1253       902  LOAD_GLOBAL              logger
              904  LOAD_METHOD              debug
              906  LOAD_STR                 'Datagram endpoint remote_addr=%r created: (%r, %r)'

 L.1255       908  LOAD_DEREF               'remote_addr'
              910  LOAD_FAST                'transport'
              912  LOAD_FAST                'protocol'
              914  CALL_METHOD_4         4  '4 positional arguments'
              916  POP_TOP          
            918_0  COME_FROM           900  '900'
            918_1  COME_FROM           872  '872'

 L.1257       918  SETUP_EXCEPT        934  'to 934'

 L.1258       920  LOAD_FAST                'waiter'
              922  GET_AWAITABLE    
              924  LOAD_CONST               None
              926  YIELD_FROM       
              928  POP_TOP          
              930  POP_BLOCK        
              932  JUMP_FORWARD        956  'to 956'
            934_0  COME_FROM_EXCEPT    918  '918'

 L.1259       934  POP_TOP          
              936  POP_TOP          
              938  POP_TOP          

 L.1260       940  LOAD_FAST                'transport'
              942  LOAD_METHOD              close
              944  CALL_METHOD_0         0  '0 positional arguments'
              946  POP_TOP          

 L.1261       948  RAISE_VARARGS_0       0  'reraise'
              950  POP_EXCEPT       
              952  JUMP_FORWARD        956  'to 956'
              954  END_FINALLY      
            956_0  COME_FROM           952  '952'
            956_1  COME_FROM           932  '932'

 L.1263       956  LOAD_FAST                'transport'
              958  LOAD_FAST                'protocol'
              960  BUILD_TUPLE_2         2 
              962  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 130_0

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

    async def create_server(self, protocol_factory, host=None, port=None, *, family=socket.AF_UNSPEC, flags=socket.AI_PASSIVE, sock=None, backlog=100, ssl=None, reuse_address=None, reuse_port=None, ssl_handshake_timeout=None, start_serving=True):
        """Create a TCP server.

        The host parameter can be a string, in that case the TCP server is
        bound to host and port.

        The host parameter can also be a sequence of strings and in that case
        the TCP server is bound to all hosts of the sequence. If a host
        appears multiple times (possibly indirectly e.g. when hostnames
        resolve to the same IP address), the server is only bound once to that
        host.

        Return a Server object which can be used to stop the service.

        This method is a coroutine.
        """
        if isinstance(ssl, bool):
            raise TypeError('ssl argument must be an SSLContext or None')
        elif ssl_handshake_timeout is not None:
            if ssl is None:
                raise ValueError('ssl_handshake_timeout is only meaningful with ssl')
            elif host is not None or port is not None:
                if sock is not None:
                    raise ValueError('host/port and sock can not be specified at the same time')
                if reuse_address is None:
                    reuse_address = os.name == 'posix' and sys.platform != 'cygwin'
                sockets = []
                if host == '':
                    hosts = [
                     None]
                else:
                    hosts = isinstance(host, str) or isinstance(host, collections.abc.Iterable) or [
                     host]
            else:
                hosts = host
            fs = [self._create_server_getaddrinfo(host, port, family=family, flags=flags) for host in hosts]
            infos = await (tasks.gather)(*fs, **{'loop': self})
            infos = set(itertools.chain.from_iterable(infos))
            completed = False
            try:
                for res in infos:
                    af, socktype, proto, canonname, sa = res
                    try:
                        sock = socket.socket(af, socktype, proto)
                    except socket.error:
                        if self._debug:
                            logger.warning('create_server() failed to create socket.socket(%r, %r, %r)', af,
                              socktype, proto, exc_info=True)
                        continue

                    sockets.append(sock)
                    if reuse_address:
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
                    if reuse_port:
                        _set_reuseport(sock)
                    if _HAS_IPv6 and af == socket.AF_INET6:
                        if hasattr(socket, 'IPPROTO_IPV6'):
                            sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, True)
                    try:
                        sock.bind(sa)
                    except OSError as err:
                        try:
                            raise OSError(err.errno, 'error while attempting to bind on address %r: %s' % (
                             sa, err.strerror.lower())) from None
                        finally:
                            err = None
                            del err

                completed = True
            finally:
                if not completed:
                    for sock in sockets:
                        sock.close()

        else:
            if sock is None:
                raise ValueError('Neither host/port nor sock were specified')
            if sock.type != socket.SOCK_STREAM:
                raise ValueError(f"A Stream Socket was expected, got {sock!r}")
            sockets = [
             sock]
        for sock in sockets:
            sock.setblocking(False)

        server = Server(self, sockets, protocol_factory, ssl, backlog, ssl_handshake_timeout)
        if start_serving:
            server._start_serving()
            await tasks.sleep(0, loop=self)
        if self._debug:
            logger.info('%r is serving', server)
        return server

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
            sock = transport.get_extra_info('socket')
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

        if self._debug:
            logger.debug('Write pipe %r connected: (%r, %r)', pipe.fileno(), transport, protocol)
        return (
         transport, protocol)

    def _log_subprocess(self, msg, stdin, stdout, stderr):
        info = [
         msg]
        if stdin is not None:
            info.append(f"stdin={_format_pipe(stdin)}")
        if stdout is not None and stderr == subprocess.STDOUT:
            info.append(f"stdout=stderr={_format_pipe(stdout)}")
        else:
            if stdout is not None:
                info.append(f"stdout={_format_pipe(stdout)}")
            if stderr is not None:
                info.append(f"stderr={_format_pipe(stderr)}")
        logger.debug(' '.join(info))

    async def subprocess_shell(self, protocol_factory, cmd, *, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=False, shell=True, bufsize=0, **kwargs):
        if not isinstance(cmd, (bytes, str)):
            raise ValueError('cmd must be a string')
        else:
            if universal_newlines:
                raise ValueError('universal_newlines must be False')
            if not shell:
                raise ValueError('shell must be True')
            if bufsize != 0:
                raise ValueError('bufsize must be 0')
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

    async def subprocess_exec(self, protocol_factory, program, *args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=False, shell=False, bufsize=0, **kwargs):
        if universal_newlines:
            raise ValueError('universal_newlines must be False')
        else:
            if shell:
                raise ValueError('shell must be False')
            if bufsize != 0:
                raise ValueError('bufsize must be 0')
            popen_args = (
             program,) + args
            for arg in popen_args:
                if not isinstance(arg, (str, bytes)):
                    raise TypeError(f"program arguments must be a bytes or text string, not {type(arg).__name__}")

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
        message = context.get('message')
        if not message:
            message = 'Unhandled exception in event loop'
        else:
            exception = context.get('exception')
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
            if key in {'exception', 'message'}:
                continue
            else:
                value = context[key]
                if key == 'source_traceback':
                    tb = ''.join(traceback.format_list(value))
                    value = 'Object created at (most recent call last):\n'
                    value += tb.rstrip()
                else:
                    if key == 'handle_traceback':
                        tb = ''.join(traceback.format_list(value))
                        value = 'Handle created at (most recent call last):\n'
                        value += tb.rstrip()
                    else:
                        value = repr(value)
            log_lines.append(f"{key}: {value}")

        logger.error(('\n'.join(log_lines)), exc_info=exc_info)

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
                self.default_exception_handler(context)
            except Exception:
                logger.error('Exception in default exception handler', exc_info=True)

        else:
            try:
                self._exception_handler(self, context)
            except Exception as exc:
                try:
                    try:
                        self.default_exception_handler({'message':'Unhandled error in exception handler', 
                         'exception':exc, 
                         'context':context})
                    except Exception:
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
        self._ready.append(handle)

    def _add_callback_signalsafe(self, handle):
        """Like _add_callback() but called from a signal handler."""
        self._add_callback(handle)
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
                    new_scheduled.append(handle)

            heapq.heapify(new_scheduled)
            self._scheduled = new_scheduled
            self._timer_cancelled_count = 0
        else:
            while self._scheduled and self._scheduled[0]._cancelled:
                self._timer_cancelled_count -= 1
                handle = heapq.heappop(self._scheduled)
                handle._scheduled = False

        timeout = None
        if self._ready or self._stopping:
            timeout = 0
        else:
            if self._scheduled:
                when = self._scheduled[0]._when
                timeout = min(max(0, when - self.time()), MAXIMUM_SELECT_TIMEOUT)
            elif self._debug:
                if timeout != 0:
                    t0 = self.time()
                    event_list = self._selector.select(timeout)
                    dt = self.time() - t0
                    if dt >= 1.0:
                        level = logging.INFO
                    else:
                        level = logging.DEBUG
                    nevent = len(event_list)
                    if timeout is None:
                        logger.log(level, 'poll took %.3f ms: %s events', dt * 1000.0, nevent)
                elif nevent:
                    logger.log(level, 'poll %.3f ms took %.3f ms: %s events', timeout * 1000.0, dt * 1000.0, nevent)
                else:
                    if dt >= 1.0:
                        logger.log(level, 'poll %.3f ms took %.3f ms: timeout', timeout * 1000.0, dt * 1000.0)
            else:
                event_list = self._selector.select(timeout)
            self._process_events(event_list)
            end_time = self.time() + self._clock_resolution
            while self._scheduled:
                handle = self._scheduled[0]
                if handle._when >= end_time:
                    break
                handle = heapq.heappop(self._scheduled)
                handle._scheduled = False
                self._ready.append(handle)

            ntodo = len(self._ready)
            for i in range(ntodo):
                handle = self._ready.popleft()
                if handle._cancelled:
                    continue
                if self._debug:
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

            handle = None

    def _set_coroutine_origin_tracking(self, enabled):
        if bool(enabled) == bool(self._coroutine_origin_tracking_enabled):
            return
        elif enabled:
            self._coroutine_origin_tracking_saved_depth = sys.get_coroutine_origin_tracking_depth()
            sys.set_coroutine_origin_tracking_depth(constants.DEBUG_STACK_DEPTH)
        else:
            sys.set_coroutine_origin_tracking_depth(self._coroutine_origin_tracking_saved_depth)
        self._coroutine_origin_tracking_enabled = enabled

    def get_debug(self):
        return self._debug

    def set_debug(self, enabled):
        self._debug = enabled
        if self.is_running():
            self.call_soon_threadsafe(self._set_coroutine_origin_tracking, enabled)