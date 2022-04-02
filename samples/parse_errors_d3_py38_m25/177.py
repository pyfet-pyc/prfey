# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\selector_events.py
"""Event loop using a selector and related classes.

A selector is a "notify-when-ready" multiplexer.  For a subclass which
also includes support for signal handling, see the unix_events sub-module.
"""
__all__ = ('BaseSelectorEventLoop', )
import collections, errno, functools, selectors, socket, warnings, weakref
try:
    import ssl
except ImportError:
    ssl = None
else:
    from . import base_events
    from . import constants
    from . import events
    from . import futures
    from . import protocols
    from . import sslproto
    from . import transports
    from . import trsock
    from .log import logger

    def _test_selector_event(selector, fd, event):
        try:
            key = selector.get_key(fd)
        except KeyError:
            return False
        else:
            return bool(key.events & event)


    def _check_ssl_socket(sock):
        if ssl is not None:
            if isinstance(sock, ssl.SSLSocket):
                raise TypeError('Socket cannot be of type SSLSocket')


    class BaseSelectorEventLoop(base_events.BaseEventLoop):
        __doc__ = 'Selector event loop.\n\n    See events.EventLoop for API specification.\n    '

        def __init__(self, selector=None):
            super().__init__()
            if selector is None:
                selector = selectors.DefaultSelector()
            logger.debug('Using selector: %s', selector.__class__.__name__)
            self._selector = selector
            self._make_self_pipe()
            self._transports = weakref.WeakValueDictionary()

        def _make_socket_transport(self, sock, protocol, waiter=None, *, extra=None, server=None):
            return _SelectorSocketTransport(self, sock, protocol, waiter, extra, server)

        def _make_ssl_transport(self, rawsock, protocol, sslcontext, waiter=None, *, server_side=False, server_hostname=None, extra=None, server=None, ssl_handshake_timeout=constants.SSL_HANDSHAKE_TIMEOUT):
            ssl_protocol = sslproto.SSLProtocol(self,
              protocol, sslcontext, waiter, server_side,
              server_hostname, ssl_handshake_timeout=ssl_handshake_timeout)
            _SelectorSocketTransport(self, rawsock, ssl_protocol, extra=extra,
              server=server)
            return ssl_protocol._app_transport

        def _make_datagram_transport(self, sock, protocol, address=None, waiter=None, extra=None):
            return _SelectorDatagramTransport(self, sock, protocol, address, waiter, extra)

        def close(self):
            if self.is_running():
                raise RuntimeError('Cannot close a running event loop')
            if self.is_closed():
                return
            self._close_self_pipe()
            super().close()
            if self._selector is not None:
                self._selector.close()
                self._selector = None

        def _close_self_pipe(self):
            self._remove_reader(self._ssock.fileno())
            self._ssock.close()
            self._ssock = None
            self._csock.close()
            self._csock = None
            self._internal_fds -= 1

        def _make_self_pipe(self):
            self._ssock, self._csock = socket.socketpair()
            self._ssock.setblocking(False)
            self._csock.setblocking(False)
            self._internal_fds += 1
            self._add_reader(self._ssock.fileno(), self._read_from_self)

        def _process_self_data(self, data):
            pass

        def _read_from_self--- This code section failed: ---
              0_0  COME_FROM            82  '82'
              0_1  COME_FROM            78  '78'
              0_2  COME_FROM            56  '56'
              0_3  COME_FROM            52  '52'
              0_4  COME_FROM            34  '34'

 L. 119         0  SETUP_FINALLY        36  'to 36'

 L. 120         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _ssock
                6  LOAD_METHOD              recv
                8  LOAD_CONST               4096
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'data'

 L. 121        14  LOAD_FAST                'data'
               16  POP_JUMP_IF_TRUE     22  'to 22'

 L. 122        18  POP_BLOCK        
               20  BREAK_LOOP           84  'to 84'
             22_0  COME_FROM            16  '16'

 L. 123        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _process_self_data
               26  LOAD_FAST                'data'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          
               32  POP_BLOCK        
               34  JUMP_BACK             0  'to 0'
             36_0  COME_FROM_FINALLY     0  '0'

 L. 124        36  DUP_TOP          
               38  LOAD_GLOBAL              InterruptedError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    58  'to 58'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 125        50  POP_EXCEPT       
               52  JUMP_BACK             0  'to 0'
               54  POP_EXCEPT       
               56  JUMP_BACK             0  'to 0'
             58_0  COME_FROM            42  '42'

 L. 126        58  DUP_TOP          
               60  LOAD_GLOBAL              BlockingIOError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    80  'to 80'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 127        72  POP_EXCEPT       
               74  BREAK_LOOP           84  'to 84'
               76  POP_EXCEPT       
               78  JUMP_BACK             0  'to 0'
             80_0  COME_FROM            64  '64'
               80  END_FINALLY      
               82  JUMP_BACK             0  'to 0'
             84_0  COME_FROM            74  '74'
             84_1  COME_FROM            20  '20'

Parse error at or near `JUMP_BACK' instruction at offset 56

        def _write_to_self(self):
            csock = self._csock
            if csock is not None:
                try:
                    csock.send(b'\x00')
                except OSError:
                    if self._debug:
                        logger.debug('Fail to write a null byte into the self-pipe socket', exc_info=True)

        def _start_serving(self, protocol_factory, sock, sslcontext=None, server=None, backlog=100, ssl_handshake_timeout=constants.SSL_HANDSHAKE_TIMEOUT):
            self._add_reader(sock.fileno(), self._accept_connection, protocol_factory, sock, sslcontext, server, backlog, ssl_handshake_timeout)

        def _accept_connection(self, protocol_factory, sock, sslcontext=None, server=None, backlog=100, ssl_handshake_timeout=constants.SSL_HANDSHAKE_TIMEOUT):
            for _ in range(backlog):
                try:
                    conn, addr = sock.accept()
                    if self._debug:
                        logger.debug('%r got a new connection from %r: %r', server, addr, conn)
                    conn.setblocking(False)
                except (BlockingIOError, InterruptedError, ConnectionAbortedError):
                    return None
                except OSError as exc:
                    try:
                        if exc.errno in (errno.EMFILE, errno.ENFILE,
                         errno.ENOBUFS, errno.ENOMEM):
                            self.call_exception_handler({'message':'socket.accept() out of system resource', 
                             'exception':exc, 
                             'socket':trsock.TransportSocket(sock)})
                            self._remove_reader(sock.fileno())
                            self.call_later(constants.ACCEPT_RETRY_DELAY, self._start_serving, protocol_factory, sock, sslcontext, server, backlog, ssl_handshake_timeout)
                        else:
                            raise
                    finally:
                        exc = None
                        del exc

                else:
                    extra = {'peername': addr}
                    accept = self._accept_connection2(protocol_factory, conn, extra, sslcontext, server, ssl_handshake_timeout)
                    self.create_task(accept)

        async def _accept_connection2(self, protocol_factory, conn, extra, sslcontext=None, server=None, ssl_handshake_timeout=constants.SSL_HANDSHAKE_TIMEOUT):
            protocol = None
            transport = None
            try:
                protocol = protocol_factory()
                waiter = self.create_future()
                if sslcontext:
                    transport = self._make_ssl_transport(conn,
                      protocol, sslcontext, waiter=waiter, server_side=True,
                      extra=extra,
                      server=server,
                      ssl_handshake_timeout=ssl_handshake_timeout)
                else:
                    transport = self._make_socket_transport(conn,
                      protocol, waiter=waiter, extra=extra, server=server)
                try:
                    await waiter
                except BaseException:
                    transport.close()
                    raise

            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as exc:
                try:
                    if self._debug:
                        context = {'message':'Error on transport creation for incoming connection', 
                         'exception':exc}
                        if protocol is not None:
                            context['protocol'] = protocol
                        if transport is not None:
                            context['transport'] = transport
                        self.call_exception_handler(context)
                finally:
                    exc = None
                    del exc

        def _ensure_fd_no_transport(self, fd):
            fileno = fd
            if not isinstance(fileno, int):
                try:
                    fileno = int(fileno.fileno())
                except (AttributeError, TypeError, ValueError):
                    raise ValueError(f"Invalid file object: {fd!r}") from None

            try:
                transport = self._transports[fileno]
            except KeyError:
                pass
            else:
                if not transport.is_closing():
                    raise RuntimeError(f"File descriptor {fd!r} is used by transport {transport!r}")

        def _add_reader(self, fd, callback, *args):
            self._check_closed()
            handle = events.Handle(callback, args, self, None)
            try:
                key = self._selector.get_key(fd)
            except KeyError:
                self._selector.register(fd, selectors.EVENT_READ, (
                 handle, None))
            else:
                mask, (reader, writer) = key.events, key.data
                self._selector.modify(fd, mask | selectors.EVENT_READ, (
                 handle, writer))
                if reader is not None:
                    reader.cancel()

        def _remove_reader(self, fd):
            if self.is_closed():
                return False
            try:
                key = self._selector.get_key(fd)
            except KeyError:
                return False
            else:
                mask, (reader, writer) = key.events, key.data
                mask &= ~selectors.EVENT_READ
                if not mask:
                    self._selector.unregister(fd)
                else:
                    self._selector.modify(fd, mask, (None, writer))
                if reader is not None:
                    reader.cancel()
                    return True
                return False

        def _add_writer(self, fd, callback, *args):
            self._check_closed()
            handle = events.Handle(callback, args, self, None)
            try:
                key = self._selector.get_key(fd)
            except KeyError:
                self._selector.register(fd, selectors.EVENT_WRITE, (
                 None, handle))
            else:
                mask, (reader, writer) = key.events, key.data
                self._selector.modify(fd, mask | selectors.EVENT_WRITE, (
                 reader, handle))
                if writer is not None:
                    writer.cancel()

        def _remove_writer(self, fd):
            """Remove a writer callback."""
            if self.is_closed():
                return False
            try:
                key = self._selector.get_key(fd)
            except KeyError:
                return False
            else:
                mask, (reader, writer) = key.events, key.data
                mask &= ~selectors.EVENT_WRITE
                if not mask:
                    self._selector.unregister(fd)
                else:
                    self._selector.modify(fd, mask, (reader, None))
                if writer is not None:
                    writer.cancel()
                    return True
                return False

        def add_reader(self, fd, callback, *args):
            """Add a reader callback."""
            self._ensure_fd_no_transport(fd)
            return (self._add_reader)(fd, callback, *args)

        def remove_reader(self, fd):
            """Remove a reader callback."""
            self._ensure_fd_no_transport(fd)
            return self._remove_reader(fd)

        def add_writer(self, fd, callback, *args):
            """Add a writer callback.."""
            self._ensure_fd_no_transport(fd)
            return (self._add_writer)(fd, callback, *args)

        def remove_writer(self, fd):
            """Remove a writer callback."""
            self._ensure_fd_no_transport(fd)
            return self._remove_writer(fd)

        async def sock_recv--- This code section failed: ---

 L. 356         0  LOAD_GLOBAL              _check_ssl_socket
                2  LOAD_FAST                'sock'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L. 357         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _debug
               12  POP_JUMP_IF_FALSE    34  'to 34'
               14  LOAD_FAST                'sock'
               16  LOAD_METHOD              gettimeout
               18  CALL_METHOD_0         0  ''
               20  LOAD_CONST               0
               22  COMPARE_OP               !=
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 358        26  LOAD_GLOBAL              ValueError
               28  LOAD_STR                 'the socket must be non-blocking'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'
             34_1  COME_FROM            12  '12'

 L. 359        34  SETUP_FINALLY        48  'to 48'

 L. 360        36  LOAD_FAST                'sock'
               38  LOAD_METHOD              recv
               40  LOAD_FAST                'n'
               42  CALL_METHOD_1         1  ''
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    34  '34'

 L. 361        48  DUP_TOP          
               50  LOAD_GLOBAL              BlockingIOError
               52  LOAD_GLOBAL              InterruptedError
               54  BUILD_TUPLE_2         2 
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    70  'to 70'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 362        66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            58  '58'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'

 L. 363        72  LOAD_FAST                'self'
               74  LOAD_METHOD              create_future
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'fut'

 L. 364        80  LOAD_FAST                'sock'
               82  LOAD_METHOD              fileno
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'fd'

 L. 365        88  LOAD_FAST                'self'
               90  LOAD_METHOD              add_reader
               92  LOAD_FAST                'fd'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                _sock_recv
               98  LOAD_FAST                'fut'
              100  LOAD_FAST                'sock'
              102  LOAD_FAST                'n'
              104  CALL_METHOD_5         5  ''
              106  POP_TOP          

 L. 366       108  LOAD_FAST                'fut'
              110  LOAD_METHOD              add_done_callback

 L. 367       112  LOAD_GLOBAL              functools
              114  LOAD_METHOD              partial
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _sock_read_done
              120  LOAD_FAST                'fd'
              122  CALL_METHOD_2         2  ''

 L. 366       124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L. 368       128  LOAD_FAST                'fut'
              130  GET_AWAITABLE    
              132  LOAD_CONST               None
              134  YIELD_FROM       
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 70_0

        def _sock_read_done(self, fd, fut):
            self.remove_reader(fd)

        def _sock_recv(self, fut, sock, n):
            if fut.done():
                return
            try:
                data = sock.recv(n)
            except (BlockingIOError, InterruptedError):
                return
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as exc:
                try:
                    fut.set_exception(exc)
                finally:
                    exc = None
                    del exc

            else:
                fut.set_result(data)

        async def sock_recv_into--- This code section failed: ---

 L. 395         0  LOAD_GLOBAL              _check_ssl_socket
                2  LOAD_FAST                'sock'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L. 396         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _debug
               12  POP_JUMP_IF_FALSE    34  'to 34'
               14  LOAD_FAST                'sock'
               16  LOAD_METHOD              gettimeout
               18  CALL_METHOD_0         0  ''
               20  LOAD_CONST               0
               22  COMPARE_OP               !=
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 397        26  LOAD_GLOBAL              ValueError
               28  LOAD_STR                 'the socket must be non-blocking'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'
             34_1  COME_FROM            12  '12'

 L. 398        34  SETUP_FINALLY        48  'to 48'

 L. 399        36  LOAD_FAST                'sock'
               38  LOAD_METHOD              recv_into
               40  LOAD_FAST                'buf'
               42  CALL_METHOD_1         1  ''
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    34  '34'

 L. 400        48  DUP_TOP          
               50  LOAD_GLOBAL              BlockingIOError
               52  LOAD_GLOBAL              InterruptedError
               54  BUILD_TUPLE_2         2 
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    70  'to 70'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 401        66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            58  '58'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'

 L. 402        72  LOAD_FAST                'self'
               74  LOAD_METHOD              create_future
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'fut'

 L. 403        80  LOAD_FAST                'sock'
               82  LOAD_METHOD              fileno
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'fd'

 L. 404        88  LOAD_FAST                'self'
               90  LOAD_METHOD              add_reader
               92  LOAD_FAST                'fd'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                _sock_recv_into
               98  LOAD_FAST                'fut'
              100  LOAD_FAST                'sock'
              102  LOAD_FAST                'buf'
              104  CALL_METHOD_5         5  ''
              106  POP_TOP          

 L. 405       108  LOAD_FAST                'fut'
              110  LOAD_METHOD              add_done_callback

 L. 406       112  LOAD_GLOBAL              functools
              114  LOAD_METHOD              partial
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _sock_read_done
              120  LOAD_FAST                'fd'
              122  CALL_METHOD_2         2  ''

 L. 405       124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L. 407       128  LOAD_FAST                'fut'
              130  GET_AWAITABLE    
              132  LOAD_CONST               None
              134  YIELD_FROM       
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 70_0

        def _sock_recv_into(self, fut, sock, buf):
            if fut.done():
                return
            try:
                nbytes = sock.recv_into(buf)
            except (BlockingIOError, InterruptedError):
                return
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as exc:
                try:
                    fut.set_exception(exc)
                finally:
                    exc = None
                    del exc

            else:
                fut.set_result(nbytes)

        async def sock_sendall(self, sock, data):
            """Send data to the socket.

        The socket must be connected to a remote socket. This method continues
        to send data from data until either all data has been sent or an
        error occurs. None is returned on success. On error, an exception is
        raised, and there is no way to determine how much data, if any, was
        successfully processed by the receiving end of the connection.
        """
            _check_ssl_socket(sock)
            if self._debug:
                if sock.gettimeout() != 0:
                    raise ValueError('the socket must be non-blocking')
            try:
                n = sock.send(data)
            except (BlockingIOError, InterruptedError):
                n = 0
            else:
                if n == len(data):
                    return
                else:
                    fut = self.create_future()
                    fd = sock.fileno()
                    fut.add_done_callback(functools.partial(self._sock_write_done, fd))
                    self.add_writer(fd, self._sock_sendall, fut, sock, memoryview(data), [n])
                    return await fut

        def _sock_sendall--- This code section failed: ---

 L. 457         0  LOAD_FAST                'fut'
                2  LOAD_METHOD              done
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 459         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 460        12  LOAD_FAST                'pos'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'start'

 L. 461        20  SETUP_FINALLY        44  'to 44'

 L. 462        22  LOAD_FAST                'sock'
               24  LOAD_METHOD              send
               26  LOAD_FAST                'view'
               28  LOAD_FAST                'start'
               30  LOAD_CONST               None
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'n'
               40  POP_BLOCK        
               42  JUMP_FORWARD        142  'to 142'
             44_0  COME_FROM_FINALLY    20  '20'

 L. 463        44  DUP_TOP          
               46  LOAD_GLOBAL              BlockingIOError
               48  LOAD_GLOBAL              InterruptedError
               50  BUILD_TUPLE_2         2 
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    68  'to 68'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 464        62  POP_EXCEPT       
               64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            54  '54'

 L. 465        68  DUP_TOP          
               70  LOAD_GLOBAL              SystemExit
               72  LOAD_GLOBAL              KeyboardInterrupt
               74  BUILD_TUPLE_2         2 
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE    92  'to 92'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 466        86  RAISE_VARARGS_0       0  'reraise'
               88  POP_EXCEPT       
               90  JUMP_FORWARD        142  'to 142'
             92_0  COME_FROM            78  '78'

 L. 467        92  DUP_TOP          
               94  LOAD_GLOBAL              BaseException
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   140  'to 140'
              100  POP_TOP          
              102  STORE_FAST               'exc'
              104  POP_TOP          
              106  SETUP_FINALLY       128  'to 128'

 L. 468       108  LOAD_FAST                'fut'
              110  LOAD_METHOD              set_exception
              112  LOAD_FAST                'exc'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 469       118  POP_BLOCK        
              120  POP_EXCEPT       
              122  CALL_FINALLY        128  'to 128'
              124  LOAD_CONST               None
              126  RETURN_VALUE     
            128_0  COME_FROM           122  '122'
            128_1  COME_FROM_FINALLY   106  '106'
              128  LOAD_CONST               None
              130  STORE_FAST               'exc'
              132  DELETE_FAST              'exc'
              134  END_FINALLY      
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM            98  '98'
              140  END_FINALLY      
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM            90  '90'
            142_2  COME_FROM            42  '42'

 L. 471       142  LOAD_FAST                'start'
              144  LOAD_FAST                'n'
              146  INPLACE_ADD      
              148  STORE_FAST               'start'

 L. 473       150  LOAD_FAST                'start'
              152  LOAD_GLOBAL              len
              154  LOAD_FAST                'view'
              156  CALL_FUNCTION_1       1  ''
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   174  'to 174'

 L. 474       162  LOAD_FAST                'fut'
              164  LOAD_METHOD              set_result
              166  LOAD_CONST               None
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  JUMP_FORWARD        182  'to 182'
            174_0  COME_FROM           160  '160'

 L. 476       174  LOAD_FAST                'start'
              176  LOAD_FAST                'pos'
              178  LOAD_CONST               0
              180  STORE_SUBSCR     
            182_0  COME_FROM           172  '172'

Parse error at or near `CALL_FINALLY' instruction at offset 122

        async def sock_connect(self, sock, address):
            """Connect to a remote socket at address.

        This method is a coroutine.
        """
            _check_ssl_socket(sock)
            if self._debug:
                if sock.gettimeout() != 0:
                    raise ValueError('the socket must be non-blocking')
            if not hasattr(socket, 'AF_UNIX') or sock.family != socket.AF_UNIX:
                resolved = await self._ensure_resolved(address,
                  family=(sock.family), proto=(sock.proto), loop=self)
                _, _, _, _, address = resolved[0]
            fut = self.create_future()
            self._sock_connect(fut, sock, address)
            return await fut

        def _sock_connect(self, fut, sock, address):
            fd = sock.fileno()
            try:
                sock.connect(address)
            except (BlockingIOError, InterruptedError):
                fut.add_done_callback(functools.partial(self._sock_write_done, fd))
                self.add_writerfdself._sock_connect_cbfutsockaddress
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as exc:
                try:
                    fut.set_exception(exc)
                finally:
                    exc = None
                    del exc

            else:
                fut.set_result(None)

        def _sock_write_done(self, fd, fut):
            self.remove_writer(fd)

        def _sock_connect_cb(self, fut, sock, address):
            if fut.done():
                return
            try:
                err = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                if err != 0:
                    raise OSError(err, f"Connect call failed {address}")
            except (BlockingIOError, InterruptedError):
                pass
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as exc:
                try:
                    fut.set_exception(exc)
                finally:
                    exc = None
                    del exc

            else:
                fut.set_result(None)

        async def sock_accept(self, sock):
            """Accept a connection.

        The socket must be bound to an address and listening for connections.
        The return value is a pair (conn, address) where conn is a new socket
        object usable to send and receive data on the connection, and address
        is the address bound to the socket on the other end of the connection.
        """
            _check_ssl_socket(sock)
            if self._debug:
                if sock.gettimeout() != 0:
                    raise ValueError('the socket must be non-blocking')
            fut = self.create_future()
            self._sock_accept(fut, False, sock)
            return await fut

        def _sock_accept(self, fut, registered, sock):
            fd = sock.fileno()
            if registered:
                self.remove_reader(fd)
            if fut.done():
                return
            try:
                conn, address = sock.accept()
                conn.setblocking(False)
            except (BlockingIOError, InterruptedError):
                self.add_readerfdself._sock_acceptfutTruesock
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as exc:
                try:
                    fut.set_exception(exc)
                finally:
                    exc = None
                    del exc

            else:
                fut.set_result((conn, address))

        async def _sendfile_native(self, transp, file, offset, count):
            del self._transports[transp._sock_fd]
            resume_reading = transp.is_reading()
            transp.pause_reading()
            await transp._make_empty_waiter()
            try:
                return await self.sock_sendfile((transp._sock), file, offset, count, fallback=False)
            finally:
                transp._reset_empty_waiter()
                if resume_reading:
                    transp.resume_reading()
                self._transports[transp._sock_fd] = transp

        def _process_events(self, event_list):
            for key, mask in event_list:
                fileobj, (reader, writer) = key.fileobj, key.data
                if mask & selectors.EVENT_READ:
                    if reader is not None:
                        if reader._cancelled:
                            self._remove_reader(fileobj)
                        else:
                            self._add_callback(reader)
                if mask & selectors.EVENT_WRITE:
                    if writer is not None:
                        if writer._cancelled:
                            self._remove_writer(fileobj)
                        else:
                            self._add_callback(writer)

        def _stop_serving(self, sock):
            self._remove_reader(sock.fileno())
            sock.close()


    class _SelectorTransport(transports._FlowControlMixin, transports.Transport):
        max_size = 262144
        _buffer_factory = bytearray
        _sock = None

        def __init__(self, loop, sock, protocol, extra=None, server=None):
            super().__init__(extra, loop)
            self._extra['socket'] = trsock.TransportSocket(sock)
            try:
                self._extra['sockname'] = sock.getsockname()
            except OSError:
                self._extra['sockname'] = None
            else:
                if 'peername' not in self._extra:
                    try:
                        self._extra['peername'] = sock.getpeername()
                    except socket.error:
                        self._extra['peername'] = None
                    else:
                        self._sock = sock
                        self._sock_fd = sock.fileno()
                        self._protocol_connected = False
                        self.set_protocol(protocol)
                        self._server = server
                        self._buffer = self._buffer_factory()
                        self._conn_lost = 0
                        self._closing = False
                        if self._server is not None:
                            self._server._attach()
                loop._transports[self._sock_fd] = self

        def __repr__(self):
            info = [self.__class__.__name__]
            if self._sock is None:
                info.append('closed')
            elif self._closing:
                info.append('closing')
            info.append(f"fd={self._sock_fd}")
            if self._loop is not None:
                if not self._loop.is_closed():
                    polling = _test_selector_event(self._loop._selector, self._sock_fd, selectors.EVENT_READ)
                    if polling:
                        info.append('read=polling')
                    else:
                        info.append('read=idle')
                    polling = _test_selector_event(self._loop._selector, self._sock_fd, selectors.EVENT_WRITE)
                    if polling:
                        state = 'polling'
                    else:
                        state = 'idle'
                    bufsize = self.get_write_buffer_size()
                    info.append(f"write=<{state}, bufsize={bufsize}>")
                return '<{}>'.format(' '.join(info))

        def abort(self):
            self._force_close(None)

        def set_protocol(self, protocol):
            self._protocol = protocol
            self._protocol_connected = True

        def get_protocol(self):
            return self._protocol

        def is_closing(self):
            return self._closing

        def close(self):
            if self._closing:
                return
            self._closing = True
            self._loop._remove_reader(self._sock_fd)
            if not self._buffer:
                self._conn_lost += 1
                self._loop._remove_writer(self._sock_fd)
                self._loop.call_soon(self._call_connection_lost, None)

        def __del__(self, _warn=warnings.warn):
            if self._sock is not None:
                _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
                self._sock.close()

        def _fatal_error(self, exc, message='Fatal error on transport'):
            if isinstance(exc, OSError):
                if self._loop.get_debug():
                    logger.debug('%r: %s', self, message, exc_info=True)
            else:
                self._loop.call_exception_handler({'message':message, 
                 'exception':exc, 
                 'transport':self, 
                 'protocol':self._protocol})
            self._force_close(exc)

        def _force_close(self, exc):
            if self._conn_lost:
                return
            if self._buffer:
                self._buffer.clear()
                self._loop._remove_writer(self._sock_fd)
            if not self._closing:
                self._closing = True
                self._loop._remove_reader(self._sock_fd)
            self._conn_lost += 1
            self._loop.call_soon(self._call_connection_lost, exc)

        def _call_connection_lost(self, exc):
            try:
                if self._protocol_connected:
                    self._protocol.connection_lost(exc)
            finally:
                self._sock.close()
                self._sock = None
                self._protocol = None
                self._loop = None
                server = self._server
                if server is not None:
                    server._detach()
                    self._server = None

        def get_write_buffer_size(self):
            return len(self._buffer)

        def _add_reader(self, fd, callback, *args):
            if self._closing:
                return
            (self._loop._add_reader)(fd, callback, *args)


    class _SelectorSocketTransport(_SelectorTransport):
        _start_tls_compatible = True
        _sendfile_compatible = constants._SendfileMode.TRY_NATIVE

        def __init__(self, loop, sock, protocol, waiter=None, extra=None, server=None):
            self._read_ready_cb = None
            super().__init__loopsockprotocolextraserver
            self._eof = False
            self._paused = False
            self._empty_waiter = None
            base_events._set_nodelay(self._sock)
            self._loop.call_soon(self._protocol.connection_made, self)
            self._loop.call_soon(self._add_reader, self._sock_fd, self._read_ready)
            if waiter is not None:
                self._loop.call_soon(futures._set_result_unless_cancelled, waiter, None)

        def set_protocol(self, protocol):
            if isinstance(protocol, protocols.BufferedProtocol):
                self._read_ready_cb = self._read_ready__get_buffer
            else:
                self._read_ready_cb = self._read_ready__data_received
            super().set_protocol(protocol)

        def is_reading(self):
            return not self._paused and not self._closing

        def pause_reading(self):
            if self._closing or (self._paused):
                return
            self._paused = True
            self._loop._remove_reader(self._sock_fd)
            if self._loop.get_debug():
                logger.debug('%r pauses reading', self)

        def resume_reading(self):
            if not (self._closing or self._paused):
                return
            self._paused = False
            self._add_reader(self._sock_fd, self._read_ready)
            if self._loop.get_debug():
                logger.debug('%r resumes reading', self)

        def _read_ready(self):
            self._read_ready_cb()

        def _read_ready__get_buffer--- This code section failed: ---

 L. 806         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _conn_lost
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 807         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 809        10  SETUP_FINALLY        44  'to 44'

 L. 810        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _protocol
               16  LOAD_METHOD              get_buffer
               18  LOAD_CONST               -1
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'buf'

 L. 811        24  LOAD_GLOBAL              len
               26  LOAD_FAST                'buf'
               28  CALL_FUNCTION_1       1  ''
               30  POP_JUMP_IF_TRUE     40  'to 40'

 L. 812        32  LOAD_GLOBAL              RuntimeError
               34  LOAD_STR                 'get_buffer() returned an empty buffer'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'
               40  POP_BLOCK        
               42  JUMP_FORWARD        120  'to 120'
             44_0  COME_FROM_FINALLY    10  '10'

 L. 813        44  DUP_TOP          
               46  LOAD_GLOBAL              SystemExit
               48  LOAD_GLOBAL              KeyboardInterrupt
               50  BUILD_TUPLE_2         2 
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    68  'to 68'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 814        62  RAISE_VARARGS_0       0  'reraise'
               64  POP_EXCEPT       
               66  JUMP_FORWARD        120  'to 120'
             68_0  COME_FROM            54  '54'

 L. 815        68  DUP_TOP          
               70  LOAD_GLOBAL              BaseException
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   118  'to 118'
               76  POP_TOP          
               78  STORE_FAST               'exc'
               80  POP_TOP          
               82  SETUP_FINALLY       106  'to 106'

 L. 816        84  LOAD_FAST                'self'
               86  LOAD_METHOD              _fatal_error

 L. 817        88  LOAD_FAST                'exc'

 L. 817        90  LOAD_STR                 'Fatal error: protocol.get_buffer() call failed.'

 L. 816        92  CALL_METHOD_2         2  ''
               94  POP_TOP          

 L. 818        96  POP_BLOCK        
               98  POP_EXCEPT       
              100  CALL_FINALLY        106  'to 106'
              102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'
            106_1  COME_FROM_FINALLY    82  '82'
              106  LOAD_CONST               None
              108  STORE_FAST               'exc'
              110  DELETE_FAST              'exc'
              112  END_FINALLY      
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            74  '74'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            66  '66'
            120_2  COME_FROM            42  '42'

 L. 820       120  SETUP_FINALLY       138  'to 138'

 L. 821       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _sock
              126  LOAD_METHOD              recv_into
              128  LOAD_FAST                'buf'
              130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'nbytes'
              134  POP_BLOCK        
              136  JUMP_FORWARD        238  'to 238'
            138_0  COME_FROM_FINALLY   120  '120'

 L. 822       138  DUP_TOP          
              140  LOAD_GLOBAL              BlockingIOError
              142  LOAD_GLOBAL              InterruptedError
              144  BUILD_TUPLE_2         2 
              146  COMPARE_OP               exception-match
              148  POP_JUMP_IF_FALSE   162  'to 162'
              150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L. 823       156  POP_EXCEPT       
              158  LOAD_CONST               None
              160  RETURN_VALUE     
            162_0  COME_FROM           148  '148'

 L. 824       162  DUP_TOP          
              164  LOAD_GLOBAL              SystemExit
              166  LOAD_GLOBAL              KeyboardInterrupt
              168  BUILD_TUPLE_2         2 
              170  COMPARE_OP               exception-match
              172  POP_JUMP_IF_FALSE   186  'to 186'
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          

 L. 825       180  RAISE_VARARGS_0       0  'reraise'
              182  POP_EXCEPT       
              184  JUMP_FORWARD        238  'to 238'
            186_0  COME_FROM           172  '172'

 L. 826       186  DUP_TOP          
              188  LOAD_GLOBAL              BaseException
              190  COMPARE_OP               exception-match
              192  POP_JUMP_IF_FALSE   236  'to 236'
              194  POP_TOP          
              196  STORE_FAST               'exc'
              198  POP_TOP          
              200  SETUP_FINALLY       224  'to 224'

 L. 827       202  LOAD_FAST                'self'
              204  LOAD_METHOD              _fatal_error
              206  LOAD_FAST                'exc'
              208  LOAD_STR                 'Fatal read error on socket transport'
              210  CALL_METHOD_2         2  ''
              212  POP_TOP          

 L. 828       214  POP_BLOCK        
              216  POP_EXCEPT       
              218  CALL_FINALLY        224  'to 224'
              220  LOAD_CONST               None
              222  RETURN_VALUE     
            224_0  COME_FROM           218  '218'
            224_1  COME_FROM_FINALLY   200  '200'
              224  LOAD_CONST               None
              226  STORE_FAST               'exc'
              228  DELETE_FAST              'exc'
              230  END_FINALLY      
              232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
            236_0  COME_FROM           192  '192'
              236  END_FINALLY      
            238_0  COME_FROM           234  '234'
            238_1  COME_FROM           184  '184'
            238_2  COME_FROM           136  '136'

 L. 830       238  LOAD_FAST                'nbytes'
          240_242  POP_JUMP_IF_TRUE    256  'to 256'

 L. 831       244  LOAD_FAST                'self'
              246  LOAD_METHOD              _read_ready__on_eof
              248  CALL_METHOD_0         0  ''
              250  POP_TOP          

 L. 832       252  LOAD_CONST               None
              254  RETURN_VALUE     
            256_0  COME_FROM           240  '240'

 L. 834       256  SETUP_FINALLY       274  'to 274'

 L. 835       258  LOAD_FAST                'self'
              260  LOAD_ATTR                _protocol
              262  LOAD_METHOD              buffer_updated
              264  LOAD_FAST                'nbytes'
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          
              270  POP_BLOCK        
              272  JUMP_FORWARD        348  'to 348'
            274_0  COME_FROM_FINALLY   256  '256'

 L. 836       274  DUP_TOP          
              276  LOAD_GLOBAL              SystemExit
              278  LOAD_GLOBAL              KeyboardInterrupt
              280  BUILD_TUPLE_2         2 
              282  COMPARE_OP               exception-match
          284_286  POP_JUMP_IF_FALSE   300  'to 300'
              288  POP_TOP          
              290  POP_TOP          
              292  POP_TOP          

 L. 837       294  RAISE_VARARGS_0       0  'reraise'
              296  POP_EXCEPT       
              298  JUMP_FORWARD        348  'to 348'
            300_0  COME_FROM           284  '284'

 L. 838       300  DUP_TOP          
              302  LOAD_GLOBAL              BaseException
              304  COMPARE_OP               exception-match
          306_308  POP_JUMP_IF_FALSE   346  'to 346'
              310  POP_TOP          
              312  STORE_FAST               'exc'
              314  POP_TOP          
              316  SETUP_FINALLY       334  'to 334'

 L. 839       318  LOAD_FAST                'self'
              320  LOAD_METHOD              _fatal_error

 L. 840       322  LOAD_FAST                'exc'

 L. 840       324  LOAD_STR                 'Fatal error: protocol.buffer_updated() call failed.'

 L. 839       326  CALL_METHOD_2         2  ''
              328  POP_TOP          
              330  POP_BLOCK        
              332  BEGIN_FINALLY    
            334_0  COME_FROM_FINALLY   316  '316'
              334  LOAD_CONST               None
              336  STORE_FAST               'exc'
              338  DELETE_FAST              'exc'
              340  END_FINALLY      
              342  POP_EXCEPT       
              344  JUMP_FORWARD        348  'to 348'
            346_0  COME_FROM           306  '306'
              346  END_FINALLY      
            348_0  COME_FROM           344  '344'
            348_1  COME_FROM           298  '298'
            348_2  COME_FROM           272  '272'

Parse error at or near `CALL_FINALLY' instruction at offset 100

        def _read_ready__data_received--- This code section failed: ---

 L. 843         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _conn_lost
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 844         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 845        10  SETUP_FINALLY        30  'to 30'

 L. 846        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _sock
               16  LOAD_METHOD              recv
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                max_size
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'data'
               26  POP_BLOCK        
               28  JUMP_FORWARD        130  'to 130'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 847        30  DUP_TOP          
               32  LOAD_GLOBAL              BlockingIOError
               34  LOAD_GLOBAL              InterruptedError
               36  BUILD_TUPLE_2         2 
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 848        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'

 L. 849        54  DUP_TOP          
               56  LOAD_GLOBAL              SystemExit
               58  LOAD_GLOBAL              KeyboardInterrupt
               60  BUILD_TUPLE_2         2 
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    78  'to 78'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 850        72  RAISE_VARARGS_0       0  'reraise'
               74  POP_EXCEPT       
               76  JUMP_FORWARD        130  'to 130'
             78_0  COME_FROM            64  '64'

 L. 851        78  DUP_TOP          
               80  LOAD_GLOBAL              BaseException
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   128  'to 128'
               86  POP_TOP          
               88  STORE_FAST               'exc'
               90  POP_TOP          
               92  SETUP_FINALLY       116  'to 116'

 L. 852        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _fatal_error
               98  LOAD_FAST                'exc'
              100  LOAD_STR                 'Fatal read error on socket transport'
              102  CALL_METHOD_2         2  ''
              104  POP_TOP          

 L. 853       106  POP_BLOCK        
              108  POP_EXCEPT       
              110  CALL_FINALLY        116  'to 116'
              112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM           110  '110'
            116_1  COME_FROM_FINALLY    92  '92'
              116  LOAD_CONST               None
              118  STORE_FAST               'exc'
              120  DELETE_FAST              'exc'
              122  END_FINALLY      
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM            84  '84'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM            76  '76'
            130_2  COME_FROM            28  '28'

 L. 855       130  LOAD_FAST                'data'
              132  POP_JUMP_IF_TRUE    146  'to 146'

 L. 856       134  LOAD_FAST                'self'
              136  LOAD_METHOD              _read_ready__on_eof
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          

 L. 857       142  LOAD_CONST               None
              144  RETURN_VALUE     
            146_0  COME_FROM           132  '132'

 L. 859       146  SETUP_FINALLY       164  'to 164'

 L. 860       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _protocol
              152  LOAD_METHOD              data_received
              154  LOAD_FAST                'data'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
              160  POP_BLOCK        
              162  JUMP_FORWARD        234  'to 234'
            164_0  COME_FROM_FINALLY   146  '146'

 L. 861       164  DUP_TOP          
              166  LOAD_GLOBAL              SystemExit
              168  LOAD_GLOBAL              KeyboardInterrupt
              170  BUILD_TUPLE_2         2 
              172  COMPARE_OP               exception-match
              174  POP_JUMP_IF_FALSE   188  'to 188'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L. 862       182  RAISE_VARARGS_0       0  'reraise'
              184  POP_EXCEPT       
              186  JUMP_FORWARD        234  'to 234'
            188_0  COME_FROM           174  '174'

 L. 863       188  DUP_TOP          
              190  LOAD_GLOBAL              BaseException
              192  COMPARE_OP               exception-match
              194  POP_JUMP_IF_FALSE   232  'to 232'
              196  POP_TOP          
              198  STORE_FAST               'exc'
              200  POP_TOP          
              202  SETUP_FINALLY       220  'to 220'

 L. 864       204  LOAD_FAST                'self'
              206  LOAD_METHOD              _fatal_error

 L. 865       208  LOAD_FAST                'exc'

 L. 865       210  LOAD_STR                 'Fatal error: protocol.data_received() call failed.'

 L. 864       212  CALL_METHOD_2         2  ''
              214  POP_TOP          
              216  POP_BLOCK        
              218  BEGIN_FINALLY    
            220_0  COME_FROM_FINALLY   202  '202'
              220  LOAD_CONST               None
              222  STORE_FAST               'exc'
              224  DELETE_FAST              'exc'
              226  END_FINALLY      
              228  POP_EXCEPT       
              230  JUMP_FORWARD        234  'to 234'
            232_0  COME_FROM           194  '194'
              232  END_FINALLY      
            234_0  COME_FROM           230  '230'
            234_1  COME_FROM           186  '186'
            234_2  COME_FROM           162  '162'

Parse error at or near `CALL_FINALLY' instruction at offset 110

        def _read_ready__on_eof--- This code section failed: ---

 L. 868         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loop
                4  LOAD_METHOD              get_debug
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 869        10  LOAD_GLOBAL              logger
               12  LOAD_METHOD              debug
               14  LOAD_STR                 '%r received EOF'
               16  LOAD_FAST                'self'
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          
             22_0  COME_FROM             8  '8'

 L. 871        22  SETUP_FINALLY        38  'to 38'

 L. 872        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _protocol
               28  LOAD_METHOD              eof_received
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'keep_open'
               34  POP_BLOCK        
               36  JUMP_FORWARD        114  'to 114'
             38_0  COME_FROM_FINALLY    22  '22'

 L. 873        38  DUP_TOP          
               40  LOAD_GLOBAL              SystemExit
               42  LOAD_GLOBAL              KeyboardInterrupt
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 874        56  RAISE_VARARGS_0       0  'reraise'
               58  POP_EXCEPT       
               60  JUMP_FORWARD        114  'to 114'
             62_0  COME_FROM            48  '48'

 L. 875        62  DUP_TOP          
               64  LOAD_GLOBAL              BaseException
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE   112  'to 112'
               70  POP_TOP          
               72  STORE_FAST               'exc'
               74  POP_TOP          
               76  SETUP_FINALLY       100  'to 100'

 L. 876        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _fatal_error

 L. 877        82  LOAD_FAST                'exc'

 L. 877        84  LOAD_STR                 'Fatal error: protocol.eof_received() call failed.'

 L. 876        86  CALL_METHOD_2         2  ''
               88  POP_TOP          

 L. 878        90  POP_BLOCK        
               92  POP_EXCEPT       
               94  CALL_FINALLY        100  'to 100'
               96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM            94  '94'
            100_1  COME_FROM_FINALLY    76  '76'
              100  LOAD_CONST               None
              102  STORE_FAST               'exc'
              104  DELETE_FAST              'exc'
              106  END_FINALLY      
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM            68  '68'
              112  END_FINALLY      
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            60  '60'
            114_2  COME_FROM            36  '36'

 L. 880       114  LOAD_FAST                'keep_open'
              116  POP_JUMP_IF_FALSE   134  'to 134'

 L. 884       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _loop
              122  LOAD_METHOD              _remove_reader
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _sock_fd
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
              132  JUMP_FORWARD        142  'to 142'
            134_0  COME_FROM           116  '116'

 L. 886       134  LOAD_FAST                'self'
              136  LOAD_METHOD              close
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          
            142_0  COME_FROM           132  '132'

Parse error at or near `CALL_FINALLY' instruction at offset 94

        def write--- This code section failed: ---

 L. 889         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  LOAD_GLOBAL              memoryview
               10  BUILD_TUPLE_3         3 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     36  'to 36'

 L. 890        16  LOAD_GLOBAL              TypeError
               18  LOAD_STR                 'data argument must be a bytes-like object, not '
               20  LOAD_GLOBAL              type
               22  LOAD_FAST                'data'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_ATTR                __name__
               28  FORMAT_VALUE          2  '!r'
               30  BUILD_STRING_2        2 
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            14  '14'

 L. 892        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _eof
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L. 893        42  LOAD_GLOBAL              RuntimeError
               44  LOAD_STR                 'Cannot call write() after write_eof()'
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            40  '40'

 L. 894        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _empty_waiter
               54  LOAD_CONST               None
               56  COMPARE_OP               is-not
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 895        60  LOAD_GLOBAL              RuntimeError
               62  LOAD_STR                 'unable to write; sendfile is in progress'
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 896        68  LOAD_FAST                'data'
               70  POP_JUMP_IF_TRUE     76  'to 76'

 L. 897        72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'

 L. 899        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _conn_lost
               80  POP_JUMP_IF_FALSE   122  'to 122'

 L. 900        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _conn_lost
               86  LOAD_GLOBAL              constants
               88  LOAD_ATTR                LOG_THRESHOLD_FOR_CONNLOST_WRITES
               90  COMPARE_OP               >=
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L. 901        94  LOAD_GLOBAL              logger
               96  LOAD_METHOD              warning
               98  LOAD_STR                 'socket.send() raised exception.'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
            104_0  COME_FROM            92  '92'

 L. 902       104  LOAD_FAST                'self'
              106  DUP_TOP          
              108  LOAD_ATTR                _conn_lost
              110  LOAD_CONST               1
              112  INPLACE_ADD      
              114  ROT_TWO          
              116  STORE_ATTR               _conn_lost

 L. 903       118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM            80  '80'

 L. 905       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _buffer
          126_128  POP_JUMP_IF_TRUE    286  'to 286'

 L. 907       130  SETUP_FINALLY       148  'to 148'

 L. 908       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _sock
              136  LOAD_METHOD              send
              138  LOAD_FAST                'data'
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'n'
              144  POP_BLOCK        
              146  JUMP_FORWARD        246  'to 246'
            148_0  COME_FROM_FINALLY   130  '130'

 L. 909       148  DUP_TOP          
              150  LOAD_GLOBAL              BlockingIOError
              152  LOAD_GLOBAL              InterruptedError
              154  BUILD_TUPLE_2         2 
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   170  'to 170'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 910       166  POP_EXCEPT       
              168  JUMP_FORWARD        268  'to 268'
            170_0  COME_FROM           158  '158'

 L. 911       170  DUP_TOP          
              172  LOAD_GLOBAL              SystemExit
              174  LOAD_GLOBAL              KeyboardInterrupt
              176  BUILD_TUPLE_2         2 
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   194  'to 194'
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          

 L. 912       188  RAISE_VARARGS_0       0  'reraise'
              190  POP_EXCEPT       
              192  JUMP_FORWARD        268  'to 268'
            194_0  COME_FROM           180  '180'

 L. 913       194  DUP_TOP          
              196  LOAD_GLOBAL              BaseException
              198  COMPARE_OP               exception-match
              200  POP_JUMP_IF_FALSE   244  'to 244'
              202  POP_TOP          
              204  STORE_FAST               'exc'
              206  POP_TOP          
              208  SETUP_FINALLY       232  'to 232'

 L. 914       210  LOAD_FAST                'self'
              212  LOAD_METHOD              _fatal_error
              214  LOAD_FAST                'exc'
              216  LOAD_STR                 'Fatal write error on socket transport'
              218  CALL_METHOD_2         2  ''
              220  POP_TOP          

 L. 915       222  POP_BLOCK        
              224  POP_EXCEPT       
              226  CALL_FINALLY        232  'to 232'
              228  LOAD_CONST               None
              230  RETURN_VALUE     
            232_0  COME_FROM           226  '226'
            232_1  COME_FROM_FINALLY   208  '208'
              232  LOAD_CONST               None
              234  STORE_FAST               'exc'
              236  DELETE_FAST              'exc'
              238  END_FINALLY      
              240  POP_EXCEPT       
              242  JUMP_FORWARD        268  'to 268'
            244_0  COME_FROM           200  '200'
              244  END_FINALLY      
            246_0  COME_FROM           146  '146'

 L. 917       246  LOAD_FAST                'data'
              248  LOAD_FAST                'n'
              250  LOAD_CONST               None
              252  BUILD_SLICE_2         2 
              254  BINARY_SUBSCR    
              256  STORE_FAST               'data'

 L. 918       258  LOAD_FAST                'data'
          260_262  POP_JUMP_IF_TRUE    268  'to 268'

 L. 919       264  LOAD_CONST               None
              266  RETURN_VALUE     
            268_0  COME_FROM           260  '260'
            268_1  COME_FROM           242  '242'
            268_2  COME_FROM           192  '192'
            268_3  COME_FROM           168  '168'

 L. 921       268  LOAD_FAST                'self'
              270  LOAD_ATTR                _loop
              272  LOAD_METHOD              _add_writer
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                _sock_fd
              278  LOAD_FAST                'self'
              280  LOAD_ATTR                _write_ready
              282  CALL_METHOD_2         2  ''
              284  POP_TOP          
            286_0  COME_FROM           126  '126'

 L. 924       286  LOAD_FAST                'self'
              288  LOAD_ATTR                _buffer
              290  LOAD_METHOD              extend
              292  LOAD_FAST                'data'
              294  CALL_METHOD_1         1  ''
              296  POP_TOP          

 L. 925       298  LOAD_FAST                'self'
              300  LOAD_METHOD              _maybe_pause_protocol
              302  CALL_METHOD_0         0  ''
              304  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 226

        def _write_ready(self):
            assert self._buffer, 'Data should not be empty'
            if self._conn_lost:
                return
            try:
                n = self._sock.send(self._buffer)
            except (BlockingIOError, InterruptedError):
                pass
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as exc:
                try:
                    self._loop._remove_writer(self._sock_fd)
                    self._buffer.clear()
                    self._fatal_error(exc, 'Fatal write error on socket transport')
                    if self._empty_waiter is not None:
                        self._empty_waiter.set_exception(exc)
                finally:
                    exc = None
                    del exc

            else:
                if n:
                    del self._buffer[:n]
                self._maybe_resume_protocol()
                if not self._buffer:
                    self._loop._remove_writer(self._sock_fd)
                    if self._empty_waiter is not None:
                        self._empty_waiter.set_result(None)
                    if self._closing:
                        self._call_connection_lost(None)
                    elif self._eof:
                        self._sock.shutdown(socket.SHUT_WR)

        def write_eof(self):
            if self._closing or (self._eof):
                return
            self._eof = True
            if not self._buffer:
                self._sock.shutdown(socket.SHUT_WR)

        def can_write_eof(self):
            return True

        def _call_connection_lost(self, exc):
            super()._call_connection_lost(exc)
            if self._empty_waiter is not None:
                self._empty_waiter.set_exception(ConnectionError('Connection is closed by peer'))

        def _make_empty_waiter(self):
            if self._empty_waiter is not None:
                raise RuntimeError('Empty waiter is already set')
            self._empty_waiter = self._loop.create_future()
            if not self._buffer:
                self._empty_waiter.set_result(None)
            return self._empty_waiter

        def _reset_empty_waiter(self):
            self._empty_waiter = None


    class _SelectorDatagramTransport(_SelectorTransport):
        _buffer_factory = collections.deque

        def __init__(self, loop, sock, protocol, address=None, waiter=None, extra=None):
            super().__init__(loop, sock, protocol, extra)
            self._address = address
            self._loop.call_soon(self._protocol.connection_made, self)
            self._loop.call_soon(self._add_reader, self._sock_fd, self._read_ready)
            if waiter is not None:
                self._loop.call_soon(futures._set_result_unless_cancelled, waiter, None)

        def get_write_buffer_size(self):
            return sum((len(data) for data, _ in self._buffer))

        def _read_ready(self):
            if self._conn_lost:
                return
            try:
                data, addr = self._sock.recvfrom(self.max_size)
            except (BlockingIOError, InterruptedError):
                pass
            except OSError as exc:
                try:
                    self._protocol.error_received(exc)
                finally:
                    exc = None
                    del exc

            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as exc:
                try:
                    self._fatal_error(exc, 'Fatal read error on datagram transport')
                finally:
                    exc = None
                    del exc

            else:
                self._protocol.datagram_received(data, addr)

        def sendto--- This code section failed: ---

 L.1022         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  LOAD_GLOBAL              memoryview
               10  BUILD_TUPLE_3         3 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     36  'to 36'

 L.1023        16  LOAD_GLOBAL              TypeError
               18  LOAD_STR                 'data argument must be a bytes-like object, not '
               20  LOAD_GLOBAL              type
               22  LOAD_FAST                'data'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_ATTR                __name__
               28  FORMAT_VALUE          2  '!r'
               30  BUILD_STRING_2        2 
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            14  '14'

 L.1025        36  LOAD_FAST                'data'
               38  POP_JUMP_IF_TRUE     44  'to 44'

 L.1026        40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'

 L.1028        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _address
               48  POP_JUMP_IF_FALSE    86  'to 86'

 L.1029        50  LOAD_FAST                'addr'
               52  LOAD_CONST               None
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _address
               58  BUILD_TUPLE_2         2 
               60  COMPARE_OP               not-in
               62  POP_JUMP_IF_FALSE    80  'to 80'

 L.1030        64  LOAD_GLOBAL              ValueError

 L.1031        66  LOAD_STR                 'Invalid address: must be None or '
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _address
               72  FORMAT_VALUE          0  ''
               74  BUILD_STRING_2        2 

 L.1030        76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            62  '62'

 L.1032        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _address
               84  STORE_FAST               'addr'
             86_0  COME_FROM            48  '48'

 L.1034        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _conn_lost
               90  POP_JUMP_IF_FALSE   138  'to 138'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _address
               96  POP_JUMP_IF_FALSE   138  'to 138'

 L.1035        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _conn_lost
              102  LOAD_GLOBAL              constants
              104  LOAD_ATTR                LOG_THRESHOLD_FOR_CONNLOST_WRITES
              106  COMPARE_OP               >=
              108  POP_JUMP_IF_FALSE   120  'to 120'

 L.1036       110  LOAD_GLOBAL              logger
              112  LOAD_METHOD              warning
              114  LOAD_STR                 'socket.send() raised exception.'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          
            120_0  COME_FROM           108  '108'

 L.1037       120  LOAD_FAST                'self'
              122  DUP_TOP          
              124  LOAD_ATTR                _conn_lost
              126  LOAD_CONST               1
              128  INPLACE_ADD      
              130  ROT_TWO          
              132  STORE_ATTR               _conn_lost

 L.1038       134  LOAD_CONST               None
              136  RETURN_VALUE     
            138_0  COME_FROM            96  '96'
            138_1  COME_FROM            90  '90'

 L.1040       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _buffer
          142_144  POP_JUMP_IF_TRUE    364  'to 364'

 L.1042       146  SETUP_FINALLY       192  'to 192'

 L.1043       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _extra
              152  LOAD_STR                 'peername'
              154  BINARY_SUBSCR    
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L.1044       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _sock
              162  LOAD_METHOD              send
              164  LOAD_FAST                'data'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
              170  JUMP_FORWARD        186  'to 186'
            172_0  COME_FROM           156  '156'

 L.1046       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _sock
              176  LOAD_METHOD              sendto
              178  LOAD_FAST                'data'
              180  LOAD_FAST                'addr'
              182  CALL_METHOD_2         2  ''
              184  POP_TOP          
            186_0  COME_FROM           170  '170'

 L.1047       186  POP_BLOCK        
              188  LOAD_CONST               None
              190  RETURN_VALUE     
            192_0  COME_FROM_FINALLY   146  '146'

 L.1048       192  DUP_TOP          
              194  LOAD_GLOBAL              BlockingIOError
              196  LOAD_GLOBAL              InterruptedError
              198  BUILD_TUPLE_2         2 
              200  COMPARE_OP               exception-match
              202  POP_JUMP_IF_FALSE   232  'to 232'
              204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L.1049       210  LOAD_FAST                'self'
              212  LOAD_ATTR                _loop
              214  LOAD_METHOD              _add_writer
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                _sock_fd
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                _sendto_ready
              224  CALL_METHOD_2         2  ''
              226  POP_TOP          
              228  POP_EXCEPT       
              230  JUMP_FORWARD        364  'to 364'
            232_0  COME_FROM           202  '202'

 L.1050       232  DUP_TOP          
              234  LOAD_GLOBAL              OSError
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   284  'to 284'
              242  POP_TOP          
              244  STORE_FAST               'exc'
              246  POP_TOP          
              248  SETUP_FINALLY       272  'to 272'

 L.1051       250  LOAD_FAST                'self'
              252  LOAD_ATTR                _protocol
              254  LOAD_METHOD              error_received
              256  LOAD_FAST                'exc'
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          

 L.1052       262  POP_BLOCK        
              264  POP_EXCEPT       
              266  CALL_FINALLY        272  'to 272'
              268  LOAD_CONST               None
              270  RETURN_VALUE     
            272_0  COME_FROM           266  '266'
            272_1  COME_FROM_FINALLY   248  '248'
              272  LOAD_CONST               None
              274  STORE_FAST               'exc'
              276  DELETE_FAST              'exc'
              278  END_FINALLY      
              280  POP_EXCEPT       
              282  JUMP_FORWARD        364  'to 364'
            284_0  COME_FROM           238  '238'

 L.1053       284  DUP_TOP          
              286  LOAD_GLOBAL              SystemExit
              288  LOAD_GLOBAL              KeyboardInterrupt
              290  BUILD_TUPLE_2         2 
              292  COMPARE_OP               exception-match
          294_296  POP_JUMP_IF_FALSE   310  'to 310'
              298  POP_TOP          
              300  POP_TOP          
              302  POP_TOP          

 L.1054       304  RAISE_VARARGS_0       0  'reraise'
              306  POP_EXCEPT       
              308  JUMP_FORWARD        364  'to 364'
            310_0  COME_FROM           294  '294'

 L.1055       310  DUP_TOP          
              312  LOAD_GLOBAL              BaseException
              314  COMPARE_OP               exception-match
          316_318  POP_JUMP_IF_FALSE   362  'to 362'
              320  POP_TOP          
              322  STORE_FAST               'exc'
              324  POP_TOP          
              326  SETUP_FINALLY       350  'to 350'

 L.1056       328  LOAD_FAST                'self'
              330  LOAD_METHOD              _fatal_error

 L.1057       332  LOAD_FAST                'exc'

 L.1057       334  LOAD_STR                 'Fatal write error on datagram transport'

 L.1056       336  CALL_METHOD_2         2  ''
              338  POP_TOP          

 L.1058       340  POP_BLOCK        
              342  POP_EXCEPT       
              344  CALL_FINALLY        350  'to 350'
              346  LOAD_CONST               None
              348  RETURN_VALUE     
            350_0  COME_FROM           344  '344'
            350_1  COME_FROM_FINALLY   326  '326'
              350  LOAD_CONST               None
              352  STORE_FAST               'exc'
              354  DELETE_FAST              'exc'
              356  END_FINALLY      
              358  POP_EXCEPT       
              360  JUMP_FORWARD        364  'to 364'
            362_0  COME_FROM           316  '316'
              362  END_FINALLY      
            364_0  COME_FROM           360  '360'
            364_1  COME_FROM           308  '308'
            364_2  COME_FROM           282  '282'
            364_3  COME_FROM           230  '230'
            364_4  COME_FROM           142  '142'

 L.1061       364  LOAD_FAST                'self'
              366  LOAD_ATTR                _buffer
              368  LOAD_METHOD              append
              370  LOAD_GLOBAL              bytes
              372  LOAD_FAST                'data'
              374  CALL_FUNCTION_1       1  ''
              376  LOAD_FAST                'addr'
              378  BUILD_TUPLE_2         2 
              380  CALL_METHOD_1         1  ''
              382  POP_TOP          

 L.1062       384  LOAD_FAST                'self'
              386  LOAD_METHOD              _maybe_pause_protocol
              388  CALL_METHOD_0         0  ''
              390  POP_TOP          

Parse error at or near `DUP_TOP' instruction at offset 192

        def _sendto_ready--- This code section failed: ---
              0_0  COME_FROM           232  '232'
              0_1  COME_FROM           228  '228'
              0_2  COME_FROM           178  '178'
              0_3  COME_FROM           154  '154'
              0_4  COME_FROM           104  '104'
              0_5  COME_FROM            62  '62'

 L.1065         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _buffer
                4  POP_JUMP_IF_FALSE   234  'to 234'

 L.1066         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _buffer
               10  LOAD_METHOD              popleft
               12  CALL_METHOD_0         0  ''
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'data'
               18  STORE_FAST               'addr'

 L.1067        20  SETUP_FINALLY        64  'to 64'

 L.1068        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _extra
               26  LOAD_STR                 'peername'
               28  BINARY_SUBSCR    
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L.1069        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _sock
               36  LOAD_METHOD              send
               38  LOAD_FAST                'data'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
               44  JUMP_FORWARD         60  'to 60'
             46_0  COME_FROM            30  '30'

 L.1071        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _sock
               50  LOAD_METHOD              sendto
               52  LOAD_FAST                'data'
               54  LOAD_FAST                'addr'
               56  CALL_METHOD_2         2  ''
               58  POP_TOP          
             60_0  COME_FROM            44  '44'
               60  POP_BLOCK        
               62  JUMP_BACK             0  'to 0'
             64_0  COME_FROM_FINALLY    20  '20'

 L.1072        64  DUP_TOP          
               66  LOAD_GLOBAL              BlockingIOError
               68  LOAD_GLOBAL              InterruptedError
               70  BUILD_TUPLE_2         2 
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   106  'to 106'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L.1073        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _buffer
               86  LOAD_METHOD              appendleft
               88  LOAD_FAST                'data'
               90  LOAD_FAST                'addr'
               92  BUILD_TUPLE_2         2 
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L.1074        98  POP_EXCEPT       
              100  BREAK_LOOP          234  'to 234'
              102  POP_EXCEPT       
              104  JUMP_BACK             0  'to 0'
            106_0  COME_FROM            74  '74'

 L.1075       106  DUP_TOP          
              108  LOAD_GLOBAL              OSError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   156  'to 156'
              114  POP_TOP          
              116  STORE_FAST               'exc'
              118  POP_TOP          
              120  SETUP_FINALLY       144  'to 144'

 L.1076       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _protocol
              126  LOAD_METHOD              error_received
              128  LOAD_FAST                'exc'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          

 L.1077       134  POP_BLOCK        
              136  POP_EXCEPT       
              138  CALL_FINALLY        144  'to 144'
              140  LOAD_CONST               None
              142  RETURN_VALUE     
            144_0  COME_FROM           138  '138'
            144_1  COME_FROM_FINALLY   120  '120'
              144  LOAD_CONST               None
              146  STORE_FAST               'exc'
              148  DELETE_FAST              'exc'
              150  END_FINALLY      
              152  POP_EXCEPT       
              154  JUMP_BACK             0  'to 0'
            156_0  COME_FROM           112  '112'

 L.1078       156  DUP_TOP          
              158  LOAD_GLOBAL              SystemExit
              160  LOAD_GLOBAL              KeyboardInterrupt
              162  BUILD_TUPLE_2         2 
              164  COMPARE_OP               exception-match
              166  POP_JUMP_IF_FALSE   180  'to 180'
              168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          

 L.1079       174  RAISE_VARARGS_0       0  'reraise'
              176  POP_EXCEPT       
              178  JUMP_BACK             0  'to 0'
            180_0  COME_FROM           166  '166'

 L.1080       180  DUP_TOP          
              182  LOAD_GLOBAL              BaseException
              184  COMPARE_OP               exception-match
              186  POP_JUMP_IF_FALSE   230  'to 230'
              188  POP_TOP          
              190  STORE_FAST               'exc'
              192  POP_TOP          
              194  SETUP_FINALLY       218  'to 218'

 L.1081       196  LOAD_FAST                'self'
              198  LOAD_METHOD              _fatal_error

 L.1082       200  LOAD_FAST                'exc'

 L.1082       202  LOAD_STR                 'Fatal write error on datagram transport'

 L.1081       204  CALL_METHOD_2         2  ''
              206  POP_TOP          

 L.1083       208  POP_BLOCK        
              210  POP_EXCEPT       
              212  CALL_FINALLY        218  'to 218'
              214  LOAD_CONST               None
              216  RETURN_VALUE     
            218_0  COME_FROM           212  '212'
            218_1  COME_FROM_FINALLY   194  '194'
              218  LOAD_CONST               None
              220  STORE_FAST               'exc'
              222  DELETE_FAST              'exc'
              224  END_FINALLY      
              226  POP_EXCEPT       
              228  JUMP_BACK             0  'to 0'
            230_0  COME_FROM           186  '186'
              230  END_FINALLY      
              232  JUMP_BACK             0  'to 0'
            234_0  COME_FROM           100  '100'
            234_1  COME_FROM             4  '4'

 L.1085       234  LOAD_FAST                'self'
              236  LOAD_METHOD              _maybe_resume_protocol
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          

 L.1086       242  LOAD_FAST                'self'
              244  LOAD_ATTR                _buffer
          246_248  POP_JUMP_IF_TRUE    282  'to 282'

 L.1087       250  LOAD_FAST                'self'
              252  LOAD_ATTR                _loop
              254  LOAD_METHOD              _remove_writer
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                _sock_fd
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          

 L.1088       264  LOAD_FAST                'self'
              266  LOAD_ATTR                _closing
          268_270  POP_JUMP_IF_FALSE   282  'to 282'

 L.1089       272  LOAD_FAST                'self'
              274  LOAD_METHOD              _call_connection_lost
              276  LOAD_CONST               None
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          
            282_0  COME_FROM           268  '268'
            282_1  COME_FROM           246  '246'

Parse error at or near `CALL_FINALLY' instruction at offset 138