# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\unix_events.py
"""Selector event loop for Unix with signal handling."""
import errno, io, itertools, os, selectors, signal, socket, stat, subprocess, sys, threading, warnings
from . import base_events
from . import base_subprocess
from . import constants
from . import coroutines
from . import events
from . import exceptions
from . import futures
from . import selector_events
from . import tasks
from . import transports
from .log import logger
__all__ = ('SelectorEventLoop', 'AbstractChildWatcher', 'SafeChildWatcher', 'FastChildWatcher',
           'MultiLoopChildWatcher', 'ThreadedChildWatcher', 'DefaultEventLoopPolicy')
if sys.platform == 'win32':
    raise ImportError('Signals are not really supported on Windows')

def _sighandler_noop(signum, frame):
    """Dummy signal handler."""
    pass


class _UnixSelectorEventLoop(selector_events.BaseSelectorEventLoop):
    __doc__ = 'Unix event loop.\n\n    Adds signal handling and UNIX Domain Socket support to SelectorEventLoop.\n    '

    def __init__(self, selector=None):
        super().__init__(selector)
        self._signal_handlers = {}

    def close(self):
        super().close()
        if not sys.is_finalizing():
            for sig in list(self._signal_handlers):
                self.remove_signal_handler(sig)

        else:
            if self._signal_handlers:
                warnings.warn(f"Closing the loop {self!r} on interpreter shutdown stage, skipping signal handlers removal", ResourceWarning,
                  source=self)
                self._signal_handlers.clear()

    def _process_self_data(self, data):
        for signum in data:
            if not signum:
                pass
            else:
                self._handle_signal(signum)

    def add_signal_handler(self, sig, callback, *args):
        """Add a handler for a signal.  UNIX only.

        Raise ValueError if the signal number is invalid or uncatchable.
        Raise RuntimeError if there is a problem setting up the handler.
        """
        if coroutines.iscoroutine(callback) or coroutines.iscoroutinefunction(callback):
            raise TypeError('coroutines cannot be used with add_signal_handler()')
        self._check_signal(sig)
        self._check_closed()
        try:
            signal.set_wakeup_fd(self._csock.fileno())
        except (ValueError, OSError) as exc:
            try:
                raise RuntimeError(str(exc))
            finally:
                exc = None
                del exc

        else:
            handle = events.Handle(callback, args, self, None)
            self._signal_handlers[sig] = handle
        try:
            signal.signal(sig, _sighandler_noop)
            signal.siginterrupt(sig, False)
        except OSError as exc:
            try:
                del self._signal_handlers[sig]
                if not self._signal_handlers:
                    try:
                        signal.set_wakeup_fd(-1)
                    except (ValueError, OSError) as nexc:
                        try:
                            logger.info('set_wakeup_fd(-1) failed: %s', nexc)
                        finally:
                            nexc = None
                            del nexc

                elif exc.errno == errno.EINVAL:
                    raise RuntimeError(f"sig {sig} cannot be caught")
                else:
                    raise
            finally:
                exc = None
                del exc

    def _handle_signal(self, sig):
        """Internal helper that is the actual signal handler."""
        handle = self._signal_handlers.get(sig)
        if handle is None:
            return
        elif handle._cancelled:
            self.remove_signal_handler(sig)
        else:
            self._add_callback_signalsafe(handle)

    def remove_signal_handler(self, sig):
        """Remove a handler for a signal.  UNIX only.

        Return True if a signal handler was removed, False if not.
        """
        self._check_signal(sig)
        try:
            del self._signal_handlers[sig]
        except KeyError:
            return False
        else:
            if sig == signal.SIGINT:
                handler = signal.default_int_handler
            else:
                handler = signal.SIG_DFL
            try:
                signal.signal(sig, handler)
            except OSError as exc:
                try:
                    if exc.errno == errno.EINVAL:
                        raise RuntimeError(f"sig {sig} cannot be caught")
                    else:
                        raise
                finally:
                    exc = None
                    del exc

            else:
                if not self._signal_handlers:
                    try:
                        signal.set_wakeup_fd(-1)
                    except (ValueError, OSError) as exc:
                        try:
                            logger.info('set_wakeup_fd(-1) failed: %s', exc)
                        finally:
                            exc = None
                            del exc

                return True

    def _check_signal(self, sig):
        """Internal helper to validate a signal.

        Raise ValueError if the signal number is invalid or uncatchable.
        Raise RuntimeError if there is a problem setting up the handler.
        """
        if not isinstance(sig, int):
            raise TypeError(f"sig must be an int, not {sig!r}")
        if sig not in signal.valid_signals():
            raise ValueError(f"invalid signal number {sig}")

    def _make_read_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
        return _UnixReadPipeTransport(self, pipe, protocol, waiter, extra)

    def _make_write_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
        return _UnixWritePipeTransport(self, pipe, protocol, waiter, extra)

    async def _make_subprocess_transport(self, protocol, args, shell, stdin, stdout, stderr, bufsize, extra=None, **kwargs):
        with events.get_child_watcher() as (watcher):
            if not watcher.is_active():
                raise RuntimeError('asyncio.get_child_watcher() is not activated, subprocess support is not installed.')
            waiter = self.create_future()
            transp = _UnixSubprocessTransport(self, protocol, args, shell,
 stdin, stdout, stderr, bufsize, waiter=waiter, 
             extra=extra, **kwargs)
            watcher.add_child_handler(transp.get_pid(), self._child_watcher_callback, transp)
            try:
                await waiter
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException:
                transp.close()
                await transp._wait()
                raise

        return transp

    def _child_watcher_callback(self, pid, returncode, transp):
        self.call_soon_threadsafe(transp._process_exited, returncode)

    async def create_unix_connection(self, protocol_factory, path=None, *, ssl=None, sock=None, server_hostname=None, ssl_handshake_timeout=None):
        if not server_hostname is None:
            assert isinstance(server_hostname, str)
        elif ssl:
            if server_hostname is None:
                raise ValueError('you have to pass server_hostname when using ssl')
            else:
                if server_hostname is not None:
                    raise ValueError('server_hostname is only meaningful with ssl')
                if ssl_handshake_timeout is not None:
                    raise ValueError('ssl_handshake_timeout is only meaningful with ssl')
            if path is not None:
                if sock is not None:
                    raise ValueError('path and sock can not be specified at the same time')
                path = os.fspath(path)
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
                try:
                    sock.setblocking(False)
                    await self.sock_connect(sock, path)
                except:
                    sock.close()
                    raise

        else:
            if sock is None:
                raise ValueError('no path and sock were specified')
            if sock.family != socket.AF_UNIX or sock.type != socket.SOCK_STREAM:
                raise ValueError(f"A UNIX Domain Stream Socket was expected, got {sock!r}")
            sock.setblocking(False)
        transport, protocol = await self._create_connection_transport(sock,
          protocol_factory, ssl, server_hostname, ssl_handshake_timeout=ssl_handshake_timeout)
        return (transport, protocol)

    async def create_unix_server(self, protocol_factory, path=None, *, sock=None, backlog=100, ssl=None, ssl_handshake_timeout=None, start_serving=True):
        if isinstance(ssl, bool):
            raise TypeError('ssl argument must be an SSLContext or None')
        if ssl_handshake_timeout is not None:
            if not ssl:
                raise ValueError('ssl_handshake_timeout is only meaningful with ssl')
        if path is not None:
            if sock is not None:
                raise ValueError('path and sock can not be specified at the same time')
            else:
                path = os.fspath(path)
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                if path[0] not in (0, '\x00'):
                    try:
                        if stat.S_ISSOCK(os.stat(path).st_mode):
                            os.remove(path)
                    except FileNotFoundError:
                        pass
                    except OSError as err:
                        try:
                            logger.error('Unable to check or remove stale UNIX socket %r: %r', path, err)
                        finally:
                            err = None
                            del err

                try:
                    sock.bind(path)
                except OSError as exc:
                    try:
                        sock.close()
                        if exc.errno == errno.EADDRINUSE:
                            msg = f"Address {path!r} is already in use"
                            raise OSError(errno.EADDRINUSE, msg) from None
                        else:
                            raise
                    finally:
                        exc = None
                        del exc

                except:
                    sock.close()
                    raise

        else:
            if sock is None:
                raise ValueError('path was not specified, and no sock specified')
            if sock.family != socket.AF_UNIX or sock.type != socket.SOCK_STREAM:
                raise ValueError(f"A UNIX Domain Stream Socket was expected, got {sock!r}")
            sock.setblocking(False)
            server = base_events.Server(self, [sock], protocol_factory, ssl, backlog, ssl_handshake_timeout)
            if start_serving:
                server._start_serving()
                await tasks.sleep(0, loop=self)
            return server

    async def _sock_sendfile_native(self, sock, file, offset, count):
        try:
            os.sendfile
        except AttributeError as exc:
            try:
                raise exceptions.SendfileNotAvailableError('os.sendfile() is not available')
            finally:
                exc = None
                del exc

        else:
            try:
                fileno = file.fileno()
            except (AttributeError, io.UnsupportedOperation) as err:
                try:
                    raise exceptions.SendfileNotAvailableError('not a regular file')
                finally:
                    err = None
                    del err

            else:
                try:
                    fsize = os.fstat(fileno).st_size
                except OSError as err:
                    try:
                        raise exceptions.SendfileNotAvailableError('not a regular file')
                    finally:
                        err = None
                        del err

                else:
                    blocksize = count if count else fsize
                    if not blocksize:
                        return 0
                    fut = self.create_future()
                    self._sock_sendfile_native_impl(fut, None, sock, fileno, offset, count, blocksize, 0)
                    return await fut

    def _sock_sendfile_native_impl(self, fut, registered_fd, sock, fileno, offset, count, blocksize, total_sent):
        fd = sock.fileno()
        if registered_fd is not None:
            self.remove_writer(registered_fd)
        if fut.cancelled():
            self._sock_sendfile_update_filepos(fileno, offset, total_sent)
            return None
        if count:
            blocksize = count - total_sent
            if blocksize <= 0:
                self._sock_sendfile_update_filepos(fileno, offset, total_sent)
                fut.set_result(total_sent)
                return
        try:
            sent = os.sendfile(fd, fileno, offset, blocksize)
        except (BlockingIOError, InterruptedError):
            if registered_fd is None:
                self._sock_add_cancellation_callback(fut, sock)
            self.add_writer(fd, self._sock_sendfile_native_impl, fut, fd, sock, fileno, offset, count, blocksize, total_sent)
        except OSError as exc:
            try:
                if registered_fd is not None and exc.errno == errno.ENOTCONN:
                    if type(exc) is not ConnectionError:
                        new_exc = ConnectionError('socket is not connected', errno.ENOTCONN)
                        new_exc.__cause__ = exc
                        exc = new_exc
                elif total_sent == 0:
                    err = exceptions.SendfileNotAvailableError('os.sendfile call failed')
                    self._sock_sendfile_update_filepos(fileno, offset, total_sent)
                    fut.set_exception(err)
                else:
                    self._sock_sendfile_update_filepos(fileno, offset, total_sent)
                    fut.set_exception(exc)
            finally:
                exc = None
                del exc

        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as exc:
            try:
                self._sock_sendfile_update_filepos(fileno, offset, total_sent)
                fut.set_exception(exc)
            finally:
                exc = None
                del exc

        else:
            if sent == 0:
                self._sock_sendfile_update_filepos(fileno, offset, total_sent)
                fut.set_result(total_sent)
            else:
                offset += sent
                total_sent += sent
                if registered_fd is None:
                    self._sock_add_cancellation_callback(fut, sock)
                self.add_writer(fd, self._sock_sendfile_native_impl, fut, fd, sock, fileno, offset, count, blocksize, total_sent)

    def _sock_sendfile_update_filepos(self, fileno, offset, total_sent):
        if total_sent > 0:
            os.lseek(fileno, offset, os.SEEK_SET)

    def _sock_add_cancellation_callback(self, fut, sock):

        def cb(fut):
            if fut.cancelled():
                fd = sock.fileno()
                if fd != -1:
                    self.remove_writer(fd)

        fut.add_done_callback(cb)


class _UnixReadPipeTransport(transports.ReadTransport):
    max_size = 262144

    def __init__(self, loop, pipe, protocol, waiter=None, extra=None):
        super().__init__(extra)
        self._extra['pipe'] = pipe
        self._loop = loop
        self._pipe = pipe
        self._fileno = pipe.fileno()
        self._protocol = protocol
        self._closing = False
        self._paused = False
        mode = os.fstat(self._fileno).st_mode
        if not stat.S_ISFIFO(mode):
            if not stat.S_ISSOCK(mode):
                if not stat.S_ISCHR(mode):
                    self._pipe = None
                    self._fileno = None
                    self._protocol = None
                    raise ValueError('Pipe transport is for pipes/sockets only.')
        os.set_blocking(self._fileno, False)
        self._loop.call_soon(self._protocol.connection_made, self)
        self._loop.call_soon(self._loop._add_reader, self._fileno, self._read_ready)
        if waiter is not None:
            self._loop.call_soon(futures._set_result_unless_cancelled, waiter, None)

    def __repr__(self):
        info = [self.__class__.__name__]
        if self._pipe is None:
            info.append('closed')
        else:
            if self._closing:
                info.append('closing')
            else:
                info.append(f"fd={self._fileno}")
                selector = getattr(self._loop, '_selector', None)
                if self._pipe is not None:
                    if selector is not None:
                        polling = selector_events._test_selector_event(selector, self._fileno, selectors.EVENT_READ)
                        if polling:
                            info.append('polling')
                    else:
                        info.append('idle')
                elif self._pipe is not None:
                    info.append('open')
                else:
                    info.append('closed')
            return '<{}>'.format(' '.join(info))

    def _read_ready(self):
        try:
            data = os.read(self._fileno, self.max_size)
        except (BlockingIOError, InterruptedError):
            pass
        except OSError as exc:
            try:
                self._fatal_error(exc, 'Fatal read error on pipe transport')
            finally:
                exc = None
                del exc

        else:
            if data:
                self._protocol.data_received(data)
            else:
                if self._loop.get_debug():
                    logger.info('%r was closed by peer', self)
                self._closing = True
                self._loop._remove_reader(self._fileno)
                self._loop.call_soon(self._protocol.eof_received)
                self._loop.call_soon(self._call_connection_lost, None)

    def pause_reading(self):
        if self._closing or self._paused:
            return
        self._paused = True
        self._loop._remove_reader(self._fileno)
        if self._loop.get_debug():
            logger.debug('%r pauses reading', self)

    def resume_reading(self):
        return self._closing or self._paused or None
        self._paused = False
        self._loop._add_reader(self._fileno, self._read_ready)
        if self._loop.get_debug():
            logger.debug('%r resumes reading', self)

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def is_closing(self):
        return self._closing

    def close(self):
        if not self._closing:
            self._close(None)

    def __del__(self, _warn=warnings.warn):
        if self._pipe is not None:
            _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
            self._pipe.close()

    def _fatal_error(self, exc, message='Fatal error on pipe transport'):
        if isinstance(exc, OSError) and exc.errno == errno.EIO:
            if self._loop.get_debug():
                logger.debug('%r: %s', self, message, exc_info=True)
        else:
            self._loop.call_exception_handler({'message':message, 
             'exception':exc, 
             'transport':self, 
             'protocol':self._protocol})
        self._close(exc)

    def _close(self, exc):
        self._closing = True
        self._loop._remove_reader(self._fileno)
        self._loop.call_soon(self._call_connection_lost, exc)

    def _call_connection_lost(self, exc):
        try:
            self._protocol.connection_lost(exc)
        finally:
            self._pipe.close()
            self._pipe = None
            self._protocol = None
            self._loop = None


class _UnixWritePipeTransport(transports._FlowControlMixin, transports.WriteTransport):

    def __init__--- This code section failed: ---

 L. 576         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __init__
                6  LOAD_FAST                'extra'
                8  LOAD_FAST                'loop'
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L. 577        14  LOAD_FAST                'pipe'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _extra
               20  LOAD_STR                 'pipe'
               22  STORE_SUBSCR     

 L. 578        24  LOAD_FAST                'pipe'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _pipe

 L. 579        30  LOAD_FAST                'pipe'
               32  LOAD_METHOD              fileno
               34  CALL_METHOD_0         0  ''
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _fileno

 L. 580        40  LOAD_FAST                'protocol'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _protocol

 L. 581        46  LOAD_GLOBAL              bytearray
               48  CALL_FUNCTION_0       0  ''
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _buffer

 L. 582        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _conn_lost

 L. 583        60  LOAD_CONST               False
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _closing

 L. 585        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              fstat
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _fileno
               74  CALL_METHOD_1         1  ''
               76  LOAD_ATTR                st_mode
               78  STORE_FAST               'mode'

 L. 586        80  LOAD_GLOBAL              stat
               82  LOAD_METHOD              S_ISCHR
               84  LOAD_FAST                'mode'
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'is_char'

 L. 587        90  LOAD_GLOBAL              stat
               92  LOAD_METHOD              S_ISFIFO
               94  LOAD_FAST                'mode'
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'is_fifo'

 L. 588       100  LOAD_GLOBAL              stat
              102  LOAD_METHOD              S_ISSOCK
              104  LOAD_FAST                'mode'
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'is_socket'

 L. 589       110  LOAD_FAST                'is_char'
              112  POP_JUMP_IF_TRUE    148  'to 148'
              114  LOAD_FAST                'is_fifo'
              116  POP_JUMP_IF_TRUE    148  'to 148'
              118  LOAD_FAST                'is_socket'
              120  POP_JUMP_IF_TRUE    148  'to 148'

 L. 590       122  LOAD_CONST               None
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _pipe

 L. 591       128  LOAD_CONST               None
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _fileno

 L. 592       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _protocol

 L. 593       140  LOAD_GLOBAL              ValueError
              142  LOAD_STR                 'Pipe transport is only for pipes, sockets and character devices'
              144  CALL_FUNCTION_1       1  ''
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           120  '120'
            148_1  COME_FROM           116  '116'
            148_2  COME_FROM           112  '112'

 L. 596       148  LOAD_GLOBAL              os
              150  LOAD_METHOD              set_blocking
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _fileno
              156  LOAD_CONST               False
              158  CALL_METHOD_2         2  ''
              160  POP_TOP          

 L. 597       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _loop
              166  LOAD_METHOD              call_soon
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                _protocol
              172  LOAD_ATTR                connection_made
              174  LOAD_FAST                'self'
              176  CALL_METHOD_2         2  ''
              178  POP_TOP          

 L. 602       180  LOAD_FAST                'is_socket'
              182  POP_JUMP_IF_TRUE    200  'to 200'
              184  LOAD_FAST                'is_fifo'
              186  POP_JUMP_IF_FALSE   224  'to 224'
              188  LOAD_GLOBAL              sys
              190  LOAD_ATTR                platform
              192  LOAD_METHOD              startswith
              194  LOAD_STR                 'aix'
              196  CALL_METHOD_1         1  ''
              198  POP_JUMP_IF_TRUE    224  'to 224'
            200_0  COME_FROM           182  '182'

 L. 604       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _loop
              204  LOAD_METHOD              call_soon
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                _loop
              210  LOAD_ATTR                _add_reader

 L. 605       212  LOAD_FAST                'self'
              214  LOAD_ATTR                _fileno

 L. 605       216  LOAD_FAST                'self'
              218  LOAD_ATTR                _read_ready

 L. 604       220  CALL_METHOD_3         3  ''
              222  POP_TOP          
            224_0  COME_FROM           198  '198'
            224_1  COME_FROM           186  '186'

 L. 607       224  LOAD_FAST                'waiter'
              226  LOAD_CONST               None
              228  COMPARE_OP               is-not
              230  POP_JUMP_IF_FALSE   250  'to 250'

 L. 609       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _loop
              236  LOAD_METHOD              call_soon
              238  LOAD_GLOBAL              futures
              240  LOAD_ATTR                _set_result_unless_cancelled

 L. 610       242  LOAD_FAST                'waiter'

 L. 610       244  LOAD_CONST               None

 L. 609       246  CALL_METHOD_3         3  ''
              248  POP_TOP          
            250_0  COME_FROM           230  '230'

Parse error at or near `POP_TOP' instruction at offset 248

    def __repr__(self):
        info = [
         self.__class__.__name__]
        if self._pipe is None:
            info.append('closed')
        else:
            if self._closing:
                info.append('closing')
            else:
                info.append(f"fd={self._fileno}")
                selector = getattr(self._loop, '_selector', None)
                if self._pipe is not None and selector is not None:
                    polling = selector_events._test_selector_event(selector, self._fileno, selectors.EVENT_WRITE)
                    if polling:
                        info.append('polling')
                    else:
                        info.append('idle')
                    bufsize = self.get_write_buffer_size()
                    info.append(f"bufsize={bufsize}")
                else:
                    if self._pipe is not None:
                        info.append('open')
                    else:
                        info.append('closed')
            return '<{}>'.format(' '.join(info))

    def get_write_buffer_size(self):
        return len(self._buffer)

    def _read_ready(self):
        if self._loop.get_debug():
            logger.info('%r was closed by peer', self)
        elif self._buffer:
            self._close(BrokenPipeError())
        else:
            self._close()

    def write--- This code section failed: ---

 L. 649         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  LOAD_GLOBAL              memoryview
               10  BUILD_TUPLE_3         3 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     28  'to 28'
               16  LOAD_ASSERT              AssertionError
               18  LOAD_GLOBAL              repr
               20  LOAD_FAST                'data'
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            14  '14'

 L. 650        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'data'
               32  LOAD_GLOBAL              bytearray
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 651        38  LOAD_GLOBAL              memoryview
               40  LOAD_FAST                'data'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'data'
             46_0  COME_FROM            36  '36'

 L. 652        46  LOAD_FAST                'data'
               48  POP_JUMP_IF_TRUE     54  'to 54'

 L. 653        50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'

 L. 655        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _conn_lost
               58  POP_JUMP_IF_TRUE     66  'to 66'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _closing
               64  POP_JUMP_IF_FALSE   106  'to 106'
             66_0  COME_FROM            58  '58'

 L. 656        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _conn_lost
               70  LOAD_GLOBAL              constants
               72  LOAD_ATTR                LOG_THRESHOLD_FOR_CONNLOST_WRITES
               74  COMPARE_OP               >=
               76  POP_JUMP_IF_FALSE    88  'to 88'

 L. 657        78  LOAD_GLOBAL              logger
               80  LOAD_METHOD              warning
               82  LOAD_STR                 'pipe closed by peer or os.write(pipe, data) raised exception.'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
             88_0  COME_FROM            76  '76'

 L. 659        88  LOAD_FAST                'self'
               90  DUP_TOP          
               92  LOAD_ATTR                _conn_lost
               94  LOAD_CONST               1
               96  INPLACE_ADD      
               98  ROT_TWO          
              100  STORE_ATTR               _conn_lost

 L. 660       102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM            64  '64'

 L. 662       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _buffer
          110_112  POP_JUMP_IF_TRUE    312  'to 312'

 L. 664       114  SETUP_FINALLY       134  'to 134'

 L. 665       116  LOAD_GLOBAL              os
              118  LOAD_METHOD              write
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _fileno
              124  LOAD_FAST                'data'
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'n'
              130  POP_BLOCK        
              132  JUMP_FORWARD        250  'to 250'
            134_0  COME_FROM_FINALLY   114  '114'

 L. 666       134  DUP_TOP          
              136  LOAD_GLOBAL              BlockingIOError
              138  LOAD_GLOBAL              InterruptedError
              140  BUILD_TUPLE_2         2 
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   160  'to 160'
              146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L. 667       152  LOAD_CONST               0
              154  STORE_FAST               'n'
              156  POP_EXCEPT       
              158  JUMP_FORWARD        250  'to 250'
            160_0  COME_FROM           144  '144'

 L. 668       160  DUP_TOP          
              162  LOAD_GLOBAL              SystemExit
              164  LOAD_GLOBAL              KeyboardInterrupt
              166  BUILD_TUPLE_2         2 
              168  COMPARE_OP               exception-match
              170  POP_JUMP_IF_FALSE   184  'to 184'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 669       178  RAISE_VARARGS_0       0  'reraise'
              180  POP_EXCEPT       
              182  JUMP_FORWARD        250  'to 250'
            184_0  COME_FROM           170  '170'

 L. 670       184  DUP_TOP          
              186  LOAD_GLOBAL              BaseException
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   248  'to 248'
              192  POP_TOP          
              194  STORE_FAST               'exc'
              196  POP_TOP          
              198  SETUP_FINALLY       236  'to 236'

 L. 671       200  LOAD_FAST                'self'
              202  DUP_TOP          
              204  LOAD_ATTR                _conn_lost
              206  LOAD_CONST               1
              208  INPLACE_ADD      
              210  ROT_TWO          
              212  STORE_ATTR               _conn_lost

 L. 672       214  LOAD_FAST                'self'
              216  LOAD_METHOD              _fatal_error
              218  LOAD_FAST                'exc'
              220  LOAD_STR                 'Fatal write error on pipe transport'
              222  CALL_METHOD_2         2  ''
              224  POP_TOP          

 L. 673       226  POP_BLOCK        
              228  POP_EXCEPT       
              230  CALL_FINALLY        236  'to 236'
              232  LOAD_CONST               None
              234  RETURN_VALUE     
            236_0  COME_FROM           230  '230'
            236_1  COME_FROM_FINALLY   198  '198'
              236  LOAD_CONST               None
              238  STORE_FAST               'exc'
              240  DELETE_FAST              'exc'
              242  END_FINALLY      
              244  POP_EXCEPT       
              246  JUMP_FORWARD        250  'to 250'
            248_0  COME_FROM           190  '190'
              248  END_FINALLY      
            250_0  COME_FROM           246  '246'
            250_1  COME_FROM           182  '182'
            250_2  COME_FROM           158  '158'
            250_3  COME_FROM           132  '132'

 L. 674       250  LOAD_FAST                'n'
              252  LOAD_GLOBAL              len
              254  LOAD_FAST                'data'
              256  CALL_FUNCTION_1       1  ''
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   268  'to 268'

 L. 675       264  LOAD_CONST               None
              266  RETURN_VALUE     
            268_0  COME_FROM           260  '260'

 L. 676       268  LOAD_FAST                'n'
              270  LOAD_CONST               0
              272  COMPARE_OP               >
          274_276  POP_JUMP_IF_FALSE   294  'to 294'

 L. 677       278  LOAD_GLOBAL              memoryview
              280  LOAD_FAST                'data'
              282  CALL_FUNCTION_1       1  ''
              284  LOAD_FAST                'n'
              286  LOAD_CONST               None
              288  BUILD_SLICE_2         2 
              290  BINARY_SUBSCR    
              292  STORE_FAST               'data'
            294_0  COME_FROM           274  '274'

 L. 678       294  LOAD_FAST                'self'
              296  LOAD_ATTR                _loop
              298  LOAD_METHOD              _add_writer
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                _fileno
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                _write_ready
              308  CALL_METHOD_2         2  ''
              310  POP_TOP          
            312_0  COME_FROM           110  '110'

 L. 680       312  LOAD_FAST                'self'
              314  DUP_TOP          
              316  LOAD_ATTR                _buffer
              318  LOAD_FAST                'data'
              320  INPLACE_ADD      
              322  ROT_TWO          
              324  STORE_ATTR               _buffer

 L. 681       326  LOAD_FAST                'self'
              328  LOAD_METHOD              _maybe_pause_protocol
              330  CALL_METHOD_0         0  ''
              332  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 230

    def _write_ready(self):
        assert self._buffer, 'Data should not be empty'
        try:
            n = os.write(self._fileno, self._buffer)
        except (BlockingIOError, InterruptedError):
            pass
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as exc:
            try:
                self._buffer.clear()
                self._conn_lost += 1
                self._loop._remove_writer(self._fileno)
                self._fatal_error(exc, 'Fatal write error on pipe transport')
            finally:
                exc = None
                del exc

        else:
            if n == len(self._buffer):
                self._buffer.clear()
                self._loop._remove_writer(self._fileno)
                self._maybe_resume_protocol()
                if self._closing:
                    self._loop._remove_reader(self._fileno)
                    self._call_connection_lost(None)
                return
        if n > 0:
            del self._buffer[:n]

    def can_write_eof(self):
        return True

    def write_eof(self):
        if self._closing:
            return
        else:
            assert self._pipe
            self._closing = True
            self._buffer or self._loop._remove_reader(self._fileno)
            self._loop.call_soon(self._call_connection_lost, None)

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def is_closing(self):
        return self._closing

    def close(self):
        if self._pipe is not None:
            if not self._closing:
                self.write_eof()

    def __del__(self, _warn=warnings.warn):
        if self._pipe is not None:
            _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
            self._pipe.close()

    def abort(self):
        self._close(None)

    def _fatal_error(self, exc, message='Fatal error on pipe transport'):
        if isinstance(exc, OSError):
            if self._loop.get_debug():
                logger.debug('%r: %s', self, message, exc_info=True)
        else:
            self._loop.call_exception_handler({'message':message, 
             'exception':exc, 
             'transport':self, 
             'protocol':self._protocol})
        self._close(exc)

    def _close(self, exc=None):
        self._closing = True
        if self._buffer:
            self._loop._remove_writer(self._fileno)
        self._buffer.clear()
        self._loop._remove_reader(self._fileno)
        self._loop.call_soon(self._call_connection_lost, exc)

    def _call_connection_lost(self, exc):
        try:
            self._protocol.connection_lost(exc)
        finally:
            self._pipe.close()
            self._pipe = None
            self._protocol = None
            self._loop = None


class _UnixSubprocessTransport(base_subprocess.BaseSubprocessTransport):

    def _start(self, args, shell, stdin, stdout, stderr, bufsize, **kwargs):
        stdin_w = None
        if stdin == subprocess.PIPE:
            stdin, stdin_w = socket.socketpair()
        try:
            self._proc = (subprocess.Popen)(
 args, shell=shell, 
             stdin=stdin, stdout=stdout, stderr=stderr, universal_newlines=False, 
             bufsize=bufsize, **kwargs)
            if stdin_w is not None:
                stdin.close()
                self._proc.stdin = open((stdin_w.detach()), 'wb', buffering=bufsize)
                stdin_w = None
        finally:
            if stdin_w is not None:
                stdin.close()
                stdin_w.close()


class AbstractChildWatcher:
    __doc__ = 'Abstract base class for monitoring child processes.\n\n    Objects derived from this class monitor a collection of subprocesses and\n    report their termination or interruption by a signal.\n\n    New callbacks are registered with .add_child_handler(). Starting a new\n    process must be done within a \'with\' block to allow the watcher to suspend\n    its activity until the new process if fully registered (this is needed to\n    prevent a race condition in some implementations).\n\n    Example:\n        with watcher:\n            proc = subprocess.Popen("sleep 1")\n            watcher.add_child_handler(proc.pid, callback)\n\n    Notes:\n        Implementations of this class must be thread-safe.\n\n        Since child watcher objects may catch the SIGCHLD signal and call\n        waitpid(-1), there should be only one active object per process.\n    '

    def add_child_handler(self, pid, callback, *args):
        """Register a new child handler.

        Arrange for callback(pid, returncode, *args) to be called when
        process 'pid' terminates. Specifying another callback for the same
        process replaces the previous handler.

        Note: callback() must be thread-safe.
        """
        raise NotImplementedError()

    def remove_child_handler(self, pid):
        """Removes the handler for process 'pid'.

        The function returns True if the handler was successfully removed,
        False if there was nothing to remove."""
        raise NotImplementedError()

    def attach_loop(self, loop):
        """Attach the watcher to an event loop.

        If the watcher was previously attached to an event loop, then it is
        first detached before attaching to the new loop.

        Note: loop may be None.
        """
        raise NotImplementedError()

    def close(self):
        """Close the watcher.

        This must be called to make sure that any underlying resource is freed.
        """
        raise NotImplementedError()

    def is_active(self):
        """Return ``True`` if the watcher is active and is used by the event loop.

        Return True if the watcher is installed and ready to handle process exit
        notifications.

        """
        raise NotImplementedError()

    def __enter__(self):
        """Enter the watcher's context and allow starting new processes

        This function must return self"""
        raise NotImplementedError()

    def __exit__(self, a, b, c):
        """Exit the watcher's context"""
        raise NotImplementedError()


def _compute_returncode(status):
    if os.WIFSIGNALED(status):
        return -os.WTERMSIG(status)
    if os.WIFEXITED(status):
        return os.WEXITSTATUS(status)
    return status


class BaseChildWatcher(AbstractChildWatcher):

    def __init__(self):
        self._loop = None
        self._callbacks = {}

    def close(self):
        self.attach_loop(None)

    def is_active(self):
        return self._loop is not None and self._loop.is_running()

    def _do_waitpid(self, expected_pid):
        raise NotImplementedError()

    def _do_waitpid_all(self):
        raise NotImplementedError()

    def attach_loop(self, loop):
        if not loop is None:
            assert isinstance(loop, events.AbstractEventLoop)
        if self._loop is not None:
            if loop is None:
                if self._callbacks:
                    warnings.warn('A loop is being detached from a child watcher with pending handlers', RuntimeWarning)
        if self._loop is not None:
            self._loop.remove_signal_handler(signal.SIGCHLD)
        self._loop = loop
        if loop is not None:
            loop.add_signal_handler(signal.SIGCHLD, self._sig_chld)
            self._do_waitpid_all()

    def _sig_chld(self):
        try:
            self._do_waitpid_all()
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as exc:
            try:
                self._loop.call_exception_handler({'message':'Unknown exception in SIGCHLD handler', 
                 'exception':exc})
            finally:
                exc = None
                del exc


class SafeChildWatcher(BaseChildWatcher):
    __doc__ = "'Safe' child watcher implementation.\n\n    This implementation avoids disrupting other code spawning processes by\n    polling explicitly each process in the SIGCHLD handler instead of calling\n    os.waitpid(-1).\n\n    This is a safe solution but it has a significant overhead when handling a\n    big number of children (O(n) each time SIGCHLD is raised)\n    "

    def close(self):
        self._callbacks.clear()
        super().close()

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

    def add_child_handler(self, pid, callback, *args):
        self._callbacks[pid] = (
         callback, args)
        self._do_waitpid(pid)

    def remove_child_handler--- This code section failed: ---

 L. 976         0  SETUP_FINALLY        16  'to 16'

 L. 977         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _callbacks
                6  LOAD_FAST                'pid'
                8  DELETE_SUBSCR    

 L. 978        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 979        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 980        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14

    def _do_waitpid_all(self):
        for pid in list(self._callbacks):
            self._do_waitpid(pid)

    def _do_waitpid(self, expected_pid):
        if not expected_pid > 0:
            raise AssertionError
        else:
            try:
                pid, status = os.waitpid(expected_pid, os.WNOHANG)
            except ChildProcessError:
                pid = expected_pid
                returncode = 255
                logger.warning('Unknown child process pid %d, will report returncode 255', pid)
            else:
                if pid == 0:
                    return
                    returncode = _compute_returncode(status)
                    if self._loop.get_debug():
                        logger.debug('process %s exited with returncode %s', expected_pid, returncode)
                else:
                    try:
                        callback, args = self._callbacks.pop(pid)
                    except KeyError:
                        if self._loop.get_debug():
                            logger.warning('Child watcher got an unexpected pid: %r', pid,
                              exc_info=True)

                callback(pid, returncode, *args)


class FastChildWatcher(BaseChildWatcher):
    __doc__ = "'Fast' child watcher implementation.\n\n    This implementation reaps every terminated processes by calling\n    os.waitpid(-1) directly, possibly breaking other code spawning processes\n    and waiting for their termination.\n\n    There is no noticeable overhead when handling a big number of children\n    (O(1) each time a child terminates).\n    "

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._zombies = {}
        self._forks = 0

    def close(self):
        self._callbacks.clear()
        self._zombies.clear()
        super().close()

    def __enter__--- This code section failed: ---

 L.1044         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           38  'to 38'
                6  POP_TOP          

 L.1045         8  LOAD_FAST                'self'
               10  DUP_TOP          
               12  LOAD_ATTR                _forks
               14  LOAD_CONST               1
               16  INPLACE_ADD      
               18  ROT_TWO          
               20  STORE_ATTR               _forks

 L.1047        22  LOAD_FAST                'self'
               24  POP_BLOCK        
               26  ROT_TWO          
               28  BEGIN_FINALLY    
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  POP_FINALLY           0  ''
               36  RETURN_VALUE     
             38_0  COME_FROM_WITH        4  '4'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 26

    def __exit__--- This code section failed: ---

 L.1050         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           72  'to 72'
                6  POP_TOP          

 L.1051         8  LOAD_FAST                'self'
               10  DUP_TOP          
               12  LOAD_ATTR                _forks
               14  LOAD_CONST               1
               16  INPLACE_SUBTRACT 
               18  ROT_TWO          
               20  STORE_ATTR               _forks

 L.1053        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _forks
               26  POP_JUMP_IF_TRUE     34  'to 34'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _zombies
               32  POP_JUMP_IF_TRUE     48  'to 48'
             34_0  COME_FROM            26  '26'

 L.1054        34  POP_BLOCK        
               36  BEGIN_FINALLY    
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  POP_FINALLY           0  ''
               44  LOAD_CONST               None
               46  RETURN_VALUE     
             48_0  COME_FROM            32  '32'

 L.1056        48  LOAD_GLOBAL              str
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _zombies
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'collateral_victims'

 L.1057        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _zombies
               62  LOAD_METHOD              clear
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          
               68  POP_BLOCK        
               70  BEGIN_FINALLY    
             72_0  COME_FROM_WITH        4  '4'
               72  WITH_CLEANUP_START
               74  WITH_CLEANUP_FINISH
               76  END_FINALLY      

 L.1059        78  LOAD_GLOBAL              logger
               80  LOAD_METHOD              warning

 L.1060        82  LOAD_STR                 'Caught subprocesses termination from unknown pids: %s'

 L.1061        84  LOAD_FAST                'collateral_victims'

 L.1059        86  CALL_METHOD_2         2  ''
               88  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 36

    def add_child_handler--- This code section failed: ---

 L.1064         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _forks
                4  POP_JUMP_IF_TRUE     14  'to 14'
                6  LOAD_ASSERT              AssertionError
                8  LOAD_STR                 'Must use the context manager'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L.1066        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _lock
               18  SETUP_WITH           90  'to 90'
               20  POP_TOP          

 L.1067        22  SETUP_FINALLY        40  'to 40'

 L.1068        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _zombies
               28  LOAD_METHOD              pop
               30  LOAD_FAST                'pid'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'returncode'
               36  POP_BLOCK        
               38  JUMP_FORWARD         86  'to 86'
             40_0  COME_FROM_FINALLY    22  '22'

 L.1069        40  DUP_TOP          
               42  LOAD_GLOBAL              KeyError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    84  'to 84'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.1071        54  LOAD_FAST                'callback'
               56  LOAD_FAST                'args'
               58  BUILD_TUPLE_2         2 
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _callbacks
               64  LOAD_FAST                'pid'
               66  STORE_SUBSCR     

 L.1072        68  POP_EXCEPT       
               70  POP_BLOCK        
               72  BEGIN_FINALLY    
               74  WITH_CLEANUP_START
               76  WITH_CLEANUP_FINISH
               78  POP_FINALLY           0  ''
               80  LOAD_CONST               None
               82  RETURN_VALUE     
             84_0  COME_FROM            46  '46'
               84  END_FINALLY      
             86_0  COME_FROM            38  '38'
               86  POP_BLOCK        
               88  BEGIN_FINALLY    
             90_0  COME_FROM_WITH       18  '18'
               90  WITH_CLEANUP_START
               92  WITH_CLEANUP_FINISH
               94  END_FINALLY      

 L.1075        96  LOAD_FAST                'callback'
               98  LOAD_FAST                'pid'
              100  LOAD_FAST                'returncode'
              102  BUILD_TUPLE_2         2 
              104  LOAD_FAST                'args'
              106  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              108  CALL_FUNCTION_EX      0  'positional arguments only'
              110  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 70

    def remove_child_handler--- This code section failed: ---

 L.1078         0  SETUP_FINALLY        16  'to 16'

 L.1079         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _callbacks
                6  LOAD_FAST                'pid'
                8  DELETE_SUBSCR    

 L.1080        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.1081        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.1082        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14

    def _do_waitpid_all--- This code section failed: ---

 L.1088         0  SETUP_FINALLY        24  'to 24'

 L.1089         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              waitpid
                6  LOAD_CONST               -1
                8  LOAD_GLOBAL              os
               10  LOAD_ATTR                WNOHANG
               12  CALL_METHOD_2         2  ''
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'pid'
               18  STORE_FAST               'status'
               20  POP_BLOCK        
               22  JUMP_FORWARD         46  'to 46'
             24_0  COME_FROM_FINALLY     0  '0'

 L.1090        24  DUP_TOP          
               26  LOAD_GLOBAL              ChildProcessError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.1092        38  POP_EXCEPT       
               40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      
             46_0  COME_FROM            22  '22'

 L.1094        46  LOAD_FAST                'pid'
               48  LOAD_CONST               0
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L.1096        54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L.1098        58  LOAD_GLOBAL              _compute_returncode
               60  LOAD_FAST                'status'
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'returncode'

 L.1100        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _lock
               70  SETUP_WITH          202  'to 202'
               72  POP_TOP          

 L.1101        74  SETUP_FINALLY        96  'to 96'

 L.1102        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _callbacks
               80  LOAD_METHOD              pop
               82  LOAD_FAST                'pid'
               84  CALL_METHOD_1         1  ''
               86  UNPACK_SEQUENCE_2     2 
               88  STORE_FAST               'callback'
               90  STORE_FAST               'args'
               92  POP_BLOCK        
               94  JUMP_FORWARD        174  'to 174'
             96_0  COME_FROM_FINALLY    74  '74'

 L.1103        96  DUP_TOP          
               98  LOAD_GLOBAL              KeyError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   172  'to 172'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L.1105       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _forks
              114  POP_JUMP_IF_FALSE   164  'to 164'

 L.1107       116  LOAD_FAST                'returncode'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _zombies
              122  LOAD_FAST                'pid'
              124  STORE_SUBSCR     

 L.1108       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _loop
              130  LOAD_METHOD              get_debug
              132  CALL_METHOD_0         0  ''
              134  POP_JUMP_IF_FALSE   150  'to 150'

 L.1109       136  LOAD_GLOBAL              logger
              138  LOAD_METHOD              debug
              140  LOAD_STR                 'unknown process %s exited with returncode %s'

 L.1111       142  LOAD_FAST                'pid'

 L.1111       144  LOAD_FAST                'returncode'

 L.1109       146  CALL_METHOD_3         3  ''
              148  POP_TOP          
            150_0  COME_FROM           134  '134'

 L.1112       150  POP_EXCEPT       
              152  POP_BLOCK        
              154  BEGIN_FINALLY    
              156  WITH_CLEANUP_START
              158  WITH_CLEANUP_FINISH
              160  POP_FINALLY           0  ''
              162  JUMP_BACK             0  'to 0'
            164_0  COME_FROM           114  '114'

 L.1113       164  LOAD_CONST               None
              166  STORE_FAST               'callback'
              168  POP_EXCEPT       
              170  JUMP_FORWARD        198  'to 198'
            172_0  COME_FROM           102  '102'
              172  END_FINALLY      
            174_0  COME_FROM            94  '94'

 L.1115       174  LOAD_FAST                'self'
              176  LOAD_ATTR                _loop
              178  LOAD_METHOD              get_debug
              180  CALL_METHOD_0         0  ''
              182  POP_JUMP_IF_FALSE   198  'to 198'

 L.1116       184  LOAD_GLOBAL              logger
              186  LOAD_METHOD              debug
              188  LOAD_STR                 'process %s exited with returncode %s'

 L.1117       190  LOAD_FAST                'pid'

 L.1117       192  LOAD_FAST                'returncode'

 L.1116       194  CALL_METHOD_3         3  ''
              196  POP_TOP          
            198_0  COME_FROM           182  '182'
            198_1  COME_FROM           170  '170'
              198  POP_BLOCK        
              200  BEGIN_FINALLY    
            202_0  COME_FROM_WITH       70  '70'
              202  WITH_CLEANUP_START
              204  WITH_CLEANUP_FINISH
              206  END_FINALLY      

 L.1119       208  LOAD_FAST                'callback'
              210  LOAD_CONST               None
              212  COMPARE_OP               is
              214  POP_JUMP_IF_FALSE   232  'to 232'

 L.1120       216  LOAD_GLOBAL              logger
              218  LOAD_METHOD              warning

 L.1121       220  LOAD_STR                 'Caught subprocess termination from unknown pid: %d -> %d'

 L.1122       222  LOAD_FAST                'pid'

 L.1122       224  LOAD_FAST                'returncode'

 L.1120       226  CALL_METHOD_3         3  ''
              228  POP_TOP          
              230  JUMP_BACK             0  'to 0'
            232_0  COME_FROM           214  '214'

 L.1124       232  LOAD_FAST                'callback'
              234  LOAD_FAST                'pid'
              236  LOAD_FAST                'returncode'
              238  BUILD_TUPLE_2         2 
              240  LOAD_FAST                'args'
              242  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              244  CALL_FUNCTION_EX      0  'positional arguments only'
              246  POP_TOP          
              248  JUMP_BACK             0  'to 0'

Parse error at or near `POP_BLOCK' instruction at offset 152


class MultiLoopChildWatcher(AbstractChildWatcher):
    __doc__ = "A watcher that doesn't require running loop in the main thread.\n\n    This implementation registers a SIGCHLD signal handler on\n    instantiation (which may conflict with other code that\n    install own handler for this signal).\n\n    The solution is safe but it has a significant overhead when\n    handling a big number of processes (*O(n)* each time a\n    SIGCHLD is received).\n    "

    def __init__(self):
        self._callbacks = {}
        self._saved_sighandler = None

    def is_active(self):
        return self._saved_sighandler is not None

    def close(self):
        self._callbacks.clear()
        if self._saved_sighandler is not None:
            handler = signal.getsignal(signal.SIGCHLD)
            if handler != self._sig_chld:
                logger.warning('SIGCHLD handler was changed by outside code')
            else:
                signal.signal(signal.SIGCHLD, self._saved_sighandler)
            self._saved_sighandler = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_child_handler(self, pid, callback, *args):
        loop = events.get_running_loop()
        self._callbacks[pid] = (loop, callback, args)
        self._do_waitpid(pid)

    def remove_child_handler--- This code section failed: ---

 L.1177         0  SETUP_FINALLY        16  'to 16'

 L.1178         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _callbacks
                6  LOAD_FAST                'pid'
                8  DELETE_SUBSCR    

 L.1179        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.1180        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.1181        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14

    def attach_loop(self, loop):
        if self._saved_sighandler is None:
            self._saved_sighandler = signal.signal(signal.SIGCHLD, self._sig_chld)
            if self._saved_sighandler is None:
                logger.warning('Previous SIGCHLD handler was set by non-Python code, restore to default handler on watcher close.')
                self._saved_sighandler = signal.SIG_DFL
            signal.siginterrupt(signal.SIGCHLD, False)

    def _do_waitpid_all(self):
        for pid in list(self._callbacks):
            self._do_waitpid(pid)

    def _do_waitpid(self, expected_pid):
        assert expected_pid > 0
        try:
            pid, status = os.waitpid(expected_pid, os.WNOHANG)
        except ChildProcessError:
            pid = expected_pid
            returncode = 255
            logger.warning('Unknown child process pid %d, will report returncode 255', pid)
            debug_log = False
        else:
            if pid == 0:
                return
                returncode = _compute_returncode(status)
                debug_log = True
            else:
                try:
                    loop, callback, args = self._callbacks.pop(pid)
                except KeyError:
                    logger.warning('Child watcher got an unexpected pid: %r', pid,
                      exc_info=True)
                else:
                    if loop.is_closed():
                        logger.warning('Loop %r that handles pid %r is closed', loop, pid)
                    else:
                        if debug_log:
                            if loop.get_debug():
                                logger.debug('process %s exited with returncode %s', expected_pid, returncode)
                        (loop.call_soon_threadsafe)(callback, pid, returncode, *args)

    def _sig_chld(self, signum, frame):
        try:
            self._do_waitpid_all()
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException:
            logger.warning('Unknown exception in SIGCHLD handler', exc_info=True)


class ThreadedChildWatcher(AbstractChildWatcher):
    __doc__ = "Threaded child watcher implementation.\n\n    The watcher uses a thread per process\n    for waiting for the process finish.\n\n    It doesn't require subscription on POSIX signal\n    but a thread creation is not free.\n\n    The watcher has O(1) complexity, its performance doesn't depend\n    on amount of spawn processes.\n    "

    def __init__(self):
        self._pid_counter = itertools.count(0)
        self._threads = {}

    def is_active(self):
        return True

    def close(self):
        self._join_threads()

    def _join_threads(self):
        """Internal: Join all non-daemon threads"""
        threads = [thread for thread in list(self._threads.values()) if thread.is_alive() if not thread.daemon]
        for thread in threads:
            thread.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self, _warn=warnings.warn):
        threads = [thread for thread in list(self._threads.values()) if thread.is_alive()]
        if threads:
            _warn(f"{self.__class__} has registered but not finished child processes", ResourceWarning,
              source=self)

    def add_child_handler(self, pid, callback, *args):
        loop = events.get_running_loop()
        thread = threading.Thread(target=(self._do_waitpid), name=f"waitpid-{next(self._pid_counter)}",
          args=(
         loop, pid, callback, args),
          daemon=True)
        self._threads[pid] = thread
        thread.start()

    def remove_child_handler(self, pid):
        return True

    def attach_loop(self, loop):
        pass

    def _do_waitpid(self, loop, expected_pid, callback, args):
        assert expected_pid > 0
        try:
            pid, status = os.waitpid(expected_pid, 0)
        except ChildProcessError:
            pid = expected_pid
            returncode = 255
            logger.warning('Unknown child process pid %d, will report returncode 255', pid)
        else:
            returncode = _compute_returncode(status)
            if loop.get_debug():
                logger.debug('process %s exited with returncode %s', expected_pid, returncode)
            elif loop.is_closed():
                logger.warning('Loop %r that handles pid %r is closed', loop, pid)
            else:
                (loop.call_soon_threadsafe)(callback, pid, returncode, *args)
            self._threads.pop(expected_pid)


class _UnixDefaultEventLoopPolicy(events.BaseDefaultEventLoopPolicy):
    __doc__ = 'UNIX event loop policy with a watcher for child processes.'
    _loop_factory = _UnixSelectorEventLoop

    def __init__(self):
        super().__init__()
        self._watcher = None

    def _init_watcher(self):
        with events._lock:
            if self._watcher is None:
                self._watcher = ThreadedChildWatcher()
                if isinstance(threading.current_thread(), threading._MainThread):
                    self._watcher.attach_loop(self._local._loop)

    def set_event_loop(self, loop):
        super().set_event_loop(loop)
        if self._watcher is not None:
            if isinstance(threading.current_thread(), threading._MainThread):
                self._watcher.attach_loop(loop)

    def get_child_watcher(self):
        """Get the watcher for child processes.

        If not yet set, a ThreadedChildWatcher object is automatically created.
        """
        if self._watcher is None:
            self._init_watcher()
        return self._watcher

    def set_child_watcher(self, watcher):
        """Set the watcher for child processes."""
        if not watcher is None:
            assert isinstance(watcher, AbstractChildWatcher)
        if self._watcher is not None:
            self._watcher.close()
        self._watcher = watcher


SelectorEventLoop = _UnixSelectorEventLoop
DefaultEventLoopPolicy = _UnixDefaultEventLoopPolicy