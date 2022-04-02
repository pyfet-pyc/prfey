# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\unix_events.py
"""Selector event loop for Unix with signal handling."""
import errno, io, os, selectors, signal, socket, stat, subprocess, sys, threading, warnings
from . import base_events
from . import base_subprocess
from . import constants
from . import coroutines
from . import events
from . import futures
from . import selector_events
from . import tasks
from . import transports
from .log import logger
__all__ = ('SelectorEventLoop', 'AbstractChildWatcher', 'SafeChildWatcher', 'FastChildWatcher',
           'DefaultEventLoopPolicy')
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

    def close--- This code section failed: ---

 L.  55         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  LOAD_METHOD              close
                6  CALL_METHOD_0         0  '0 positional arguments'
                8  POP_TOP          

 L.  56        10  LOAD_GLOBAL              sys
               12  LOAD_METHOD              is_finalizing
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  POP_JUMP_IF_TRUE     50  'to 50'

 L.  57        18  SETUP_LOOP           90  'to 90'
               20  LOAD_GLOBAL              list
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _signal_handlers
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  GET_ITER         
               30  FOR_ITER             46  'to 46'
               32  STORE_FAST               'sig'

 L.  58        34  LOAD_FAST                'self'
               36  LOAD_METHOD              remove_signal_handler
               38  LOAD_FAST                'sig'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  POP_TOP          
               44  JUMP_BACK            30  'to 30'
               46  POP_BLOCK        
               48  JUMP_FORWARD         90  'to 90'
             50_0  COME_FROM            16  '16'

 L.  60        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _signal_handlers
               54  POP_JUMP_IF_FALSE    90  'to 90'

 L.  61        56  LOAD_GLOBAL              warnings
               58  LOAD_ATTR                warn
               60  LOAD_STR                 'Closing the loop '
               62  LOAD_FAST                'self'
               64  FORMAT_VALUE          2  '!r'
               66  LOAD_STR                 ' on interpreter shutdown stage, skipping signal handlers removal'
               68  BUILD_STRING_3        3 

 L.  64        70  LOAD_GLOBAL              ResourceWarning

 L.  65        72  LOAD_FAST                'self'
               74  LOAD_CONST               ('source',)
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  POP_TOP          

 L.  66        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _signal_handlers
               84  LOAD_METHOD              clear
               86  CALL_METHOD_0         0  '0 positional arguments'
               88  POP_TOP          
             90_0  COME_FROM            54  '54'
             90_1  COME_FROM            48  '48'
             90_2  COME_FROM_LOOP       18  '18'

Parse error at or near `COME_FROM' instruction at offset 90_1

    def _process_self_data(self, data):
        for signum in data:
            if not signum:
                continue
            self._handle_signal(signum)

    def add_signal_handler(self, sig, callback, *args):
        """Add a handler for a signal.  UNIX only.

        Raise ValueError if the signal number is invalid or uncatchable.
        Raise RuntimeError if there is a problem setting up the handler.
        """
        if coroutines.iscoroutine(callback) or coroutines.iscoroutinefunction(callback):
            raise TypeError('coroutines cannot be used with add_signal_handler()')
        self._check_signal(sig)
        self._check_closed
        try:
            signal.set_wakeup_fd(self._csock.fileno)
        except (ValueError, OSError) as exc:
            try:
                raise RuntimeError(str(exc))
            finally:
                exc = None
                del exc

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
        if not 1 <= sig < signal.NSIG:
            raise ValueError(f"sig {sig} out of range(1, {signal.NSIG})")

    def _make_read_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
        return _UnixReadPipeTransport(self, pipe, protocol, waiter, extra)

    def _make_write_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
        return _UnixWritePipeTransport(self, pipe, protocol, waiter, extra)

    async def _make_subprocess_transport(self, protocol, args, shell, stdin, stdout, stderr, bufsize, extra=None, **kwargs):
        with events.get_child_watcher as (watcher):
            waiter = self.create_future
            transp = _UnixSubprocessTransport(self, protocol, args, shell,
 stdin, stdout, stderr, bufsize, waiter=waiter, 
             extra=extra, **kwargs)
            watcher.add_child_handler(transp.get_pid, self._child_watcher_callback, transp)
            try:
                await waiter
            except Exception:
                transp.close
                await transp._wait
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
                sock.close
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
                        sock.close
                        if exc.errno == errno.EADDRINUSE:
                            msg = f"Address {path!r} is already in use"
                            raise OSError(errno.EADDRINUSE, msg) from None
                        else:
                            raise
                    finally:
                        exc = None
                        del exc

                except:
                    sock.close
                    raise

        else:
            if sock is None:
                raise ValueError('path was not specified, and no sock specified')
            if sock.family != socket.AF_UNIX or sock.type != socket.SOCK_STREAM:
                raise ValueError(f"A UNIX Domain Stream Socket was expected, got {sock!r}")
            sock.setblocking(False)
            server = base_events.Server(self, [sock], protocol_factory, ssl, backlog, ssl_handshake_timeout)
            if start_serving:
                server._start_serving
                await tasks.sleep(0, loop=self)
            return server

    async def _sock_sendfile_native(self, sock, file, offset, count):
        try:
            os.sendfile
        except AttributeError as exc:
            try:
                raise events.SendfileNotAvailableError('os.sendfile() is not available')
            finally:
                exc = None
                del exc

        try:
            fileno = file.fileno
        except (AttributeError, io.UnsupportedOperation) as err:
            try:
                raise events.SendfileNotAvailableError('not a regular file')
            finally:
                err = None
                del err

        try:
            fsize = os.fstat(fileno).st_size
        except OSError as err:
            try:
                raise events.SendfileNotAvailableError('not a regular file')
            finally:
                err = None
                del err

        blocksize = count if count else fsize
        if not blocksize:
            return 0
        fut = self.create_future
        self._sock_sendfile_native_impl(fut, None, sock, fileno, offset, count, blocksize, 0)
        return await fut

    def _sock_sendfile_native_impl(self, fut, registered_fd, sock, fileno, offset, count, blocksize, total_sent):
        fd = sock.fileno
        if registered_fd is not None:
            self.remove_writer(registered_fd)
        if fut.cancelled:
            self._sock_sendfile_update_filepos(fileno, offset, total_sent)
            return
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
                if registered_fd is not None:
                    if exc.errno == errno.ENOTCONN:
                        if type(exc) is not ConnectionError:
                            new_exc = ConnectionError('socket is not connected', errno.ENOTCONN)
                            new_exc.__cause__ = exc
                            exc = new_exc
                if total_sent == 0:
                    err = events.SendfileNotAvailableError('os.sendfile call failed')
                    self._sock_sendfile_update_filepos(fileno, offset, total_sent)
                    fut.set_exception(err)
                else:
                    self._sock_sendfile_update_filepos(fileno, offset, total_sent)
                    fut.set_exception(exc)
            finally:
                exc = None
                del exc

        except Exception as exc:
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
            if fut.cancelled:
                fd = sock.fileno
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
        self._fileno = pipe.fileno
        self._protocol = protocol
        self._closing = False
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
                if self._loop.get_debug:
                    logger.info('%r was closed by peer', self)
                self._closing = True
                self._loop._remove_reader(self._fileno)
                self._loop.call_soon(self._protocol.eof_received)
                self._loop.call_soon(self._call_connection_lost, None)

    def pause_reading(self):
        self._loop._remove_reader(self._fileno)

    def resume_reading(self):
        self._loop._add_reader(self._fileno, self._read_ready)

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def is_closing(self):
        return self._closing

    def close(self):
        if not self._closing:
            self._close(None)

    def __del__(self):
        if self._pipe is not None:
            warnings.warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
            self._pipe.close

    def _fatal_error(self, exc, message='Fatal error on pipe transport'):
        if isinstance(exc, OSError) and exc.errno == errno.EIO:
            if self._loop.get_debug:
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
            self._pipe.close
            self._pipe = None
            self._protocol = None
            self._loop = None


class _UnixWritePipeTransport(transports._FlowControlMixin, transports.WriteTransport):

    def __init__--- This code section failed: ---

 L. 552         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  LOAD_METHOD              __init__
                6  LOAD_FAST                'extra'
                8  LOAD_FAST                'loop'
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  POP_TOP          

 L. 553        14  LOAD_FAST                'pipe'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _extra
               20  LOAD_STR                 'pipe'
               22  STORE_SUBSCR     

 L. 554        24  LOAD_FAST                'pipe'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _pipe

 L. 555        30  LOAD_FAST                'pipe'
               32  LOAD_METHOD              fileno
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _fileno

 L. 556        40  LOAD_FAST                'protocol'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _protocol

 L. 557        46  LOAD_GLOBAL              bytearray
               48  CALL_FUNCTION_0       0  '0 positional arguments'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _buffer

 L. 558        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _conn_lost

 L. 559        60  LOAD_CONST               False
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _closing

 L. 561        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              fstat
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _fileno
               74  CALL_METHOD_1         1  '1 positional argument'
               76  LOAD_ATTR                st_mode
               78  STORE_FAST               'mode'

 L. 562        80  LOAD_GLOBAL              stat
               82  LOAD_METHOD              S_ISCHR
               84  LOAD_FAST                'mode'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'is_char'

 L. 563        90  LOAD_GLOBAL              stat
               92  LOAD_METHOD              S_ISFIFO
               94  LOAD_FAST                'mode'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  STORE_FAST               'is_fifo'

 L. 564       100  LOAD_GLOBAL              stat
              102  LOAD_METHOD              S_ISSOCK
              104  LOAD_FAST                'mode'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               'is_socket'

 L. 565       110  LOAD_FAST                'is_char'
              112  POP_JUMP_IF_TRUE    148  'to 148'
              114  LOAD_FAST                'is_fifo'
              116  POP_JUMP_IF_TRUE    148  'to 148'
              118  LOAD_FAST                'is_socket'
              120  POP_JUMP_IF_TRUE    148  'to 148'

 L. 566       122  LOAD_CONST               None
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _pipe

 L. 567       128  LOAD_CONST               None
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _fileno

 L. 568       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _protocol

 L. 569       140  LOAD_GLOBAL              ValueError
              142  LOAD_STR                 'Pipe transport is only for pipes, sockets and character devices'
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           120  '120'
            148_1  COME_FROM           116  '116'
            148_2  COME_FROM           112  '112'

 L. 572       148  LOAD_GLOBAL              os
              150  LOAD_METHOD              set_blocking
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _fileno
              156  LOAD_CONST               False
              158  CALL_METHOD_2         2  '2 positional arguments'
              160  POP_TOP          

 L. 573       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _loop
              166  LOAD_METHOD              call_soon
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                _protocol
              172  LOAD_ATTR                connection_made
              174  LOAD_FAST                'self'
              176  CALL_METHOD_2         2  '2 positional arguments'
              178  POP_TOP          

 L. 578       180  LOAD_FAST                'is_socket'
              182  POP_JUMP_IF_TRUE    200  'to 200'
              184  LOAD_FAST                'is_fifo'
              186  POP_JUMP_IF_FALSE   224  'to 224'
              188  LOAD_GLOBAL              sys
              190  LOAD_ATTR                platform
              192  LOAD_METHOD              startswith
              194  LOAD_STR                 'aix'
              196  CALL_METHOD_1         1  '1 positional argument'
              198  POP_JUMP_IF_TRUE    224  'to 224'
            200_0  COME_FROM           182  '182'

 L. 580       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _loop
              204  LOAD_METHOD              call_soon
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                _loop
              210  LOAD_ATTR                _add_reader

 L. 581       212  LOAD_FAST                'self'
              214  LOAD_ATTR                _fileno
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                _read_ready
              220  CALL_METHOD_3         3  '3 positional arguments'
              222  POP_TOP          
            224_0  COME_FROM           198  '198'
            224_1  COME_FROM           186  '186'

 L. 583       224  LOAD_FAST                'waiter'
              226  LOAD_CONST               None
              228  COMPARE_OP               is-not
              230  POP_JUMP_IF_FALSE   250  'to 250'

 L. 585       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _loop
              236  LOAD_METHOD              call_soon
              238  LOAD_GLOBAL              futures
              240  LOAD_ATTR                _set_result_unless_cancelled

 L. 586       242  LOAD_FAST                'waiter'
              244  LOAD_CONST               None
              246  CALL_METHOD_3         3  '3 positional arguments'
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
                    bufsize = self.get_write_buffer_size
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
        if self._loop.get_debug:
            logger.info('%r was closed by peer', self)
        elif self._buffer:
            self._close(BrokenPipeError())
        else:
            self._close

    def write(self, data):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise AssertionError(repr(data))
        else:
            if isinstance(data, bytearray):
                data = memoryview(data)
            return data or None
        if self._conn_lost or self._closing:
            if self._conn_lost >= constants.LOG_THRESHOLD_FOR_CONNLOST_WRITES:
                logger.warning('pipe closed by peer or os.write(pipe, data) raised exception.')
            self._conn_lost += 1
            return
        if not self._buffer:
            try:
                n = os.write(self._fileno, data)
            except (BlockingIOError, InterruptedError):
                n = 0
            except Exception as exc:
                try:
                    self._conn_lost += 1
                    self._fatal_error(exc, 'Fatal write error on pipe transport')
                    return
                finally:
                    exc = None
                    del exc

            if n == len(data):
                return
            if n > 0:
                data = memoryview(data)[n:]
            self._loop._add_writer(self._fileno, self._write_ready)
        self._buffer += data
        self._maybe_pause_protocol

    def _write_ready(self):
        assert self._buffer, 'Data should not be empty'
        try:
            n = os.write(self._fileno, self._buffer)
        except (BlockingIOError, InterruptedError):
            pass
        except Exception as exc:
            try:
                self._buffer.clear
                self._conn_lost += 1
                self._loop._remove_writer(self._fileno)
                self._fatal_error(exc, 'Fatal write error on pipe transport')
            finally:
                exc = None
                del exc

        else:
            if n == len(self._buffer):
                self._buffer.clear
                self._loop._remove_writer(self._fileno)
                self._maybe_resume_protocol
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
                self.write_eof

    def __del__(self):
        if self._pipe is not None:
            warnings.warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
            self._pipe.close

    def abort(self):
        self._close(None)

    def _fatal_error(self, exc, message='Fatal error on pipe transport'):
        if isinstance(exc, OSError):
            if self._loop.get_debug:
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
        self._buffer.clear
        self._loop._remove_reader(self._fileno)
        self._loop.call_soon(self._call_connection_lost, exc)

    def _call_connection_lost(self, exc):
        try:
            self._protocol.connection_lost(exc)
        finally:
            self._pipe.close
            self._pipe = None
            self._protocol = None
            self._loop = None


class _UnixSubprocessTransport(base_subprocess.BaseSubprocessTransport):

    def _start(self, args, shell, stdin, stdout, stderr, bufsize, **kwargs):
        stdin_w = None
        if stdin == subprocess.PIPE:
            stdin, stdin_w = socket.socketpair
        try:
            self._proc = (subprocess.Popen)(
 args, shell=shell, stdin=stdin, stdout=stdout, stderr=stderr, universal_newlines=False, 
             bufsize=bufsize, **kwargs)
            if stdin_w is not None:
                stdin.close
                self._proc.stdin = open((stdin_w.detach), 'wb', buffering=bufsize)
                stdin_w = None
        finally:
            if stdin_w is not None:
                stdin.close
                stdin_w.close


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

    def __enter__(self):
        """Enter the watcher's context and allow starting new processes

        This function must return self"""
        raise NotImplementedError()

    def __exit__(self, a, b, c):
        """Exit the watcher's context"""
        raise NotImplementedError()


class BaseChildWatcher(AbstractChildWatcher):

    def __init__(self):
        self._loop = None
        self._callbacks = {}

    def close(self):
        self.attach_loop(None)

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
            self._do_waitpid_all

    def _sig_chld(self):
        try:
            self._do_waitpid_all
        except Exception as exc:
            try:
                self._loop.call_exception_handler({'message':'Unknown exception in SIGCHLD handler', 
                 'exception':exc})
            finally:
                exc = None
                del exc

    def _compute_returncode(self, status):
        if os.WIFSIGNALED(status):
            return -os.WTERMSIG(status)
        if os.WIFEXITED(status):
            return os.WEXITSTATUS(status)
        return status


class SafeChildWatcher(BaseChildWatcher):
    __doc__ = "'Safe' child watcher implementation.\n\n    This implementation avoids disrupting other code spawning processes by\n    polling explicitly each process in the SIGCHLD handler instead of calling\n    os.waitpid(-1).\n\n    This is a safe solution but it has a significant overhead when handling a\n    big number of children (O(n) each time SIGCHLD is raised)\n    "

    def close(self):
        self._callbacks.clear
        super().close

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

    def add_child_handler(self, pid, callback, *args):
        if self._loop is None:
            raise RuntimeError('Cannot add child handler, the child watcher does not have a loop attached')
        self._callbacks[pid] = (
         callback, args)
        self._do_waitpid(pid)

    def remove_child_handler(self, pid):
        try:
            del self._callbacks[pid]
            return True
        except KeyError:
            return False

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
                    returncode = self._compute_returncode(status)
                    if self._loop.get_debug:
                        logger.debug('process %s exited with returncode %s', expected_pid, returncode)
                else:
                    try:
                        callback, args = self._callbacks.pop(pid)
                    except KeyError:
                        if self._loop.get_debug:
                            logger.warning('Child watcher got an unexpected pid: %r', pid,
                              exc_info=True)

                callback(pid, returncode, *args)


class FastChildWatcher(BaseChildWatcher):
    __doc__ = "'Fast' child watcher implementation.\n\n    This implementation reaps every terminated processes by calling\n    os.waitpid(-1) directly, possibly breaking other code spawning processes\n    and waiting for their termination.\n\n    There is no noticeable overhead when handling a big number of children\n    (O(1) each time a child terminates).\n    "

    def __init__(self):
        super().__init__
        self._lock = threading.Lock
        self._zombies = {}
        self._forks = 0

    def close(self):
        self._callbacks.clear
        self._zombies.clear
        super().close

    def __enter__(self):
        with self._lock:
            self._forks += 1
            return self

    def __exit__(self, a, b, c):
        with self._lock:
            self._forks -= 1
            return self._forks or self._zombies or None
            collateral_victims = str(self._zombies)
            self._zombies.clear
        logger.warning('Caught subprocesses termination from unknown pids: %s', collateral_victims)

    def add_child_handler(self, pid, callback, *args):
        assert self._forks, 'Must use the context manager'
        if self._loop is None:
            raise RuntimeError('Cannot add child handler, the child watcher does not have a loop attached')
        with self._lock:
            try:
                returncode = self._zombies.pop(pid)
            except KeyError:
                self._callbacks[pid] = (
                 callback, args)
                return

        callback(pid, returncode, *args)

    def remove_child_handler(self, pid):
        try:
            del self._callbacks[pid]
            return True
        except KeyError:
            return False

    def _do_waitpid_all(self):
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                return
            else:
                if pid == 0:
                    return
                    returncode = self._compute_returncode(status)
                    with self._lock:
                        try:
                            callback, args = self._callbacks.pop(pid)
                        except KeyError:
                            if self._forks:
                                self._zombies[pid] = returncode
                                if self._loop.get_debug:
                                    logger.debug('unknown process %s exited with returncode %s', pid, returncode)
                                continue
                            callback = None
                        else:
                            if self._loop.get_debug:
                                logger.debug('process %s exited with returncode %s', pid, returncode)
                    if callback is None:
                        logger.warning('Caught subprocess termination from unknown pid: %d -> %d', pid, returncode)
                else:
                    callback(pid, returncode, *args)


class _UnixDefaultEventLoopPolicy(events.BaseDefaultEventLoopPolicy):
    __doc__ = 'UNIX event loop policy with a watcher for child processes.'
    _loop_factory = _UnixSelectorEventLoop

    def __init__(self):
        super().__init__
        self._watcher = None

    def _init_watcher(self):
        with events._lock:
            if self._watcher is None:
                self._watcher = SafeChildWatcher()
                if isinstance(threading.current_thread, threading._MainThread):
                    self._watcher.attach_loop(self._local._loop)

    def set_event_loop(self, loop):
        super().set_event_loop(loop)
        if self._watcher is not None:
            if isinstance(threading.current_thread, threading._MainThread):
                self._watcher.attach_loop(loop)

    def get_child_watcher(self):
        """Get the watcher for child processes.

        If not yet set, a SafeChildWatcher object is automatically created.
        """
        if self._watcher is None:
            self._init_watcher
        return self._watcher

    def set_child_watcher(self, watcher):
        """Set the watcher for child processes."""
        if not watcher is None:
            assert isinstance(watcher, AbstractChildWatcher)
        if self._watcher is not None:
            self._watcher.close
        self._watcher = watcher


SelectorEventLoop = _UnixSelectorEventLoop
DefaultEventLoopPolicy = _UnixDefaultEventLoopPolicy