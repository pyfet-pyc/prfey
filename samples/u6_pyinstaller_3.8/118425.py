# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\websockets\protocol.py
"""
:mod:`websockets.protocol` handles WebSocket control and data frames.

See `sections 4 to 8 of RFC 6455`_.

.. _sections 4 to 8 of RFC 6455: http://tools.ietf.org/html/rfc6455#section-4

"""
import asyncio, codecs, collections, enum, logging, random, struct, sys, warnings
from typing import Any, AsyncIterable, AsyncIterator, Awaitable, Deque, Dict, Iterable, List, Optional, Union, cast
from .exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK, InvalidState, PayloadTooBig, ProtocolError
from extensions.base import Extension
from .framing import *
from .handshake import *
from .http import Headers
from .typing import Data
__all__ = [
 'WebSocketCommonProtocol']
logger = logging.getLogger(__name__)

class State(enum.IntEnum):
    CONNECTING, OPEN, CLOSING, CLOSED = range(4)


class WebSocketCommonProtocol(asyncio.Protocol):
    __doc__ = "\n    :class:`~asyncio.Protocol` subclass implementing the data transfer phase.\n\n    Once the WebSocket connection is established, during the data transfer\n    phase, the protocol is almost symmetrical between the server side and the\n    client side. :class:`WebSocketCommonProtocol` implements logic that's\n    shared between servers and clients..\n\n    Subclasses such as :class:`~websockets.server.WebSocketServerProtocol` and\n    :class:`~websockets.client.WebSocketClientProtocol` implement the opening\n    handshake, which is different between servers and clients.\n\n    :class:`WebSocketCommonProtocol` performs four functions:\n\n    * It runs a task that stores incoming data frames in a queue and makes\n      them available with the :meth:`recv` coroutine.\n    * It sends outgoing data frames with the :meth:`send` coroutine.\n    * It deals with control frames automatically.\n    * It performs the closing handshake.\n\n    :class:`WebSocketCommonProtocol` supports asynchronous iteration::\n\n        async for message in websocket:\n            await process(message)\n\n    The iterator yields incoming messages. It exits normally when the\n    connection is closed with the close code 1000 (OK) or 1001 (going away).\n    It raises a :exc:`~websockets.exceptions.ConnectionClosedError` exception\n    when the connection is closed with any other code.\n\n    Once the connection is open, a `Ping frame`_ is sent every\n    ``ping_interval`` seconds. This serves as a keepalive. It helps keeping\n    the connection open, especially in the presence of proxies with short\n    timeouts on inactive connections. Set ``ping_interval`` to ``None`` to\n    disable this behavior.\n\n    .. _Ping frame: https://tools.ietf.org/html/rfc6455#section-5.5.2\n\n    If the corresponding `Pong frame`_ isn't received within ``ping_timeout``\n    seconds, the connection is considered unusable and is closed with\n    code 1011. This ensures that the remote endpoint remains responsive. Set\n    ``ping_timeout`` to ``None`` to disable this behavior.\n\n    .. _Pong frame: https://tools.ietf.org/html/rfc6455#section-5.5.3\n\n    The ``close_timeout`` parameter defines a maximum wait time in seconds for\n    completing the closing handshake and terminating the TCP connection.\n    :meth:`close` completes in at most ``4 * close_timeout`` on the server\n    side and ``5 * close_timeout`` on the client side.\n\n    ``close_timeout`` needs to be a parameter of the protocol because\n    ``websockets`` usually calls :meth:`close` implicitly:\n\n    - on the server side, when the connection handler terminates,\n    - on the client side, when exiting the context manager for the connection.\n\n    To apply a timeout to any other API, wrap it in :func:`~asyncio.wait_for`.\n\n    The ``max_size`` parameter enforces the maximum size for incoming messages\n    in bytes. The default value is 1\xa0MiB. ``None`` disables the limit. If a\n    message larger than the maximum size is received, :meth:`recv` will\n    raise :exc:`~websockets.exceptions.ConnectionClosedError` and the\n    connection will be closed with code 1009.\n\n    The ``max_queue`` parameter sets the maximum length of the queue that\n    holds incoming messages. The default value is ``32``. ``None`` disables\n    the limit. Messages are added to an in-memory queue when they're received;\n    then :meth:`recv` pops from that queue. In order to prevent excessive\n    memory consumption when messages are received faster than they can be\n    processed, the queue must be bounded. If the queue fills up, the protocol\n    stops processing incoming data until :meth:`recv` is called. In this\n    situation, various receive buffers (at least in ``asyncio`` and in the OS)\n    will fill up, then the TCP receive window will shrink, slowing down\n    transmission to avoid packet loss.\n\n    Since Python can use up to 4 bytes of memory to represent a single\n    character, each connection may use up to ``4 * max_size * max_queue``\n    bytes of memory to store incoming messages. By default, this is 128\xa0MiB.\n    You may want to lower the limits, depending on your application's\n    requirements.\n\n    The ``read_limit`` argument sets the high-water limit of the buffer for\n    incoming bytes. The low-water limit is half the high-water limit. The\n    default value is 64\xa0KiB, half of asyncio's default (based on the current\n    implementation of :class:`~asyncio.StreamReader`).\n\n    The ``write_limit`` argument sets the high-water limit of the buffer for\n    outgoing bytes. The low-water limit is a quarter of the high-water limit.\n    The default value is 64\xa0KiB, equal to asyncio's default (based on the\n    current implementation of ``FlowControlMixin``).\n\n    As soon as the HTTP request and response in the opening handshake are\n    processed:\n\n    * the request path is available in the :attr:`path` attribute;\n    * the request and response HTTP headers are available in the\n      :attr:`request_headers` and :attr:`response_headers` attributes,\n      which are :class:`~websockets.http.Headers` instances.\n\n    If a subprotocol was negotiated, it's available in the :attr:`subprotocol`\n    attribute.\n\n    Once the connection is closed, the code is available in the\n    :attr:`close_code` attribute and the reason in :attr:`close_reason`.\n\n    All these attributes must be treated as read-only.\n\n    "
    is_client: bool
    side = 'undefined'
    side: str

    def __init__(self, *, ping_interval: Optional[float]=20, ping_timeout: Optional[float]=20, close_timeout: Optional[float]=None, max_size: Optional[int]=1048576, max_queue: Optional[int]=32, read_limit: int=65536, write_limit: int=65536, loop: Optional[asyncio.AbstractEventLoop]=None, host: Optional[str]=None, port: Optional[int]=None, secure: Optional[bool]=None, legacy_recv: bool=False, timeout: Optional[float]=None) -> None:
        if timeout is None:
            timeout = 10
        else:
            warnings.warn('rename timeout to close_timeout', DeprecationWarning)
        if close_timeout is None:
            close_timeout = timeout
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.close_timeout = close_timeout
        self.max_size = max_size
        self.max_queue = max_queue
        self.read_limit = read_limit
        self.write_limit = write_limit
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self._host = host
        self._port = port
        self._secure = secure
        self.legacy_recv = legacy_recv
        self.reader = asyncio.StreamReader(limit=(read_limit // 2), loop=loop)
        self._paused = False
        self._drain_waiter = None
        self._drain_lock = asyncio.Lock(loop=(loop if sys.version_info[:2] < (3, 8) else None))
        self.state = State.CONNECTING
        logger.debug('%s - state = CONNECTING', self.side)
        self
        self
        self
        self.extensions = []
        self.subprotocol = None
        self
        self
        self.connection_lost_waiter = loop.create_future()
        self.messages = collections.deque()
        self._pop_message_waiter = None
        self._put_message_waiter = None
        self._fragmented_message_waiter = None
        self.pings = {}
        self
        self.transfer_data_exc = None
        self
        self

    async def _drain_helper(self) -> None:
        if self.connection_lost_waiter.done():
            raise ConnectionResetError('Connection lost')
        else:
            if not self._paused:
                return
            waiter = self._drain_waiter
            if not waiter is None:
                if not waiter.cancelled():
                    raise AssertionError
        waiter = self.loop.create_future()
        self._drain_waiter = waiter
        await waiter

    async def _drain(self) -> None:
        if self.reader is not None:
            exc = self.reader.exception()
            if exc is not None:
                raise exc
        if self.transport is not None:
            if self.transport.is_closing():
                await asyncio.sleep(0,
                  loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
        await self._drain_helper()

    def connection_open(self) -> None:
        """
        Callback when the WebSocket opening handshake completes.

        Enter the OPEN state and start the data transfer phase.

        """
        assert self.state is State.CONNECTING
        self.state = State.OPEN
        logger.debug('%s - state = OPEN', self.side)
        self.transfer_data_task = self.loop.create_task(self.transfer_data())
        self.keepalive_ping_task = self.loop.create_task(self.keepalive_ping())
        self.close_connection_task = self.loop.create_task(self.close_connection())

    @property
    def host(self) -> Optional[str]:
        alternative = 'remote_address' if self.is_client else 'local_address'
        warnings.warn(f"use {alternative}[0] instead of host", DeprecationWarning)
        return self._host

    @property
    def port(self) -> Optional[int]:
        alternative = 'remote_address' if self.is_client else 'local_address'
        warnings.warn(f"use {alternative}[1] instead of port", DeprecationWarning)
        return self._port

    @property
    def secure(self) -> Optional[bool]:
        warnings.warn("don't use secure", DeprecationWarning)
        return self._secure

    @property
    def local_address(self) -> Any:
        """
        Local address of the connection.

        This is a ``(host, port)`` tuple or ``None`` if the connection hasn't
        been established yet.

        """
        try:
            transport = self.transport
        except AttributeError:
            return
        else:
            return transport.get_extra_info('sockname')

    @property
    def remote_address(self) -> Any:
        """
        Remote address of the connection.

        This is a ``(host, port)`` tuple or ``None`` if the connection hasn't
        been established yet.

        """
        try:
            transport = self.transport
        except AttributeError:
            return
        else:
            return transport.get_extra_info('peername')

    @property
    def open(self) -> bool:
        """
        ``True`` when the connection is usable.

        It may be used to detect disconnections. However, this approach is
        discouraged per the EAFP_ principle.

        When ``open`` is ``False``, using the connection raises a
        :exc:`~websockets.exceptions.ConnectionClosed` exception.

        .. _EAFP: https://docs.python.org/3/glossary.html#term-eafp

        """
        return self.state is State.OPEN and not self.transfer_data_task.done()

    @property
    def closed(self) -> bool:
        """
        ``True`` once the connection is closed.

        Be aware that both :attr:`open` and :attr:`closed` are ``False`` during
        the opening and closing sequences.

        """
        return self.state is State.CLOSED

    async def wait_closed(self) -> None:
        """
        Wait until the connection is closed.

        This is identical to :attr:`closed`, except it can be awaited.

        This can make it easier to handle connection termination, regardless
        of its cause, in tasks that interact with the WebSocket connection.

        """
        await asyncio.shield(self.connection_lost_waiter)

    async def __aiter__(self) -> AsyncIterator[Data]:
        """
        Iterate on received messages.

        Exit normally when the connection is closed with code 1000 or 1001.

        Raise an exception in other cases.

        """
        try:
            while True:
                (yield await self.recv())

        except ConnectionClosedOK:
            return

    async def recv(self) -> Data:
        """
        Receive the next message.

        Return a :class:`str` for a text frame and :class:`bytes` for a binary
        frame.

        When the end of the message stream is reached, :meth:`recv` raises
        :exc:`~websockets.exceptions.ConnectionClosed`. Specifically, it
        raises :exc:`~websockets.exceptions.ConnectionClosedOK` after a normal
        connection closure and
        :exc:`~websockets.exceptions.ConnectionClosedError` after a protocol
        error or a network failure.

        .. versionchanged:: 3.0

            :meth:`recv` used to return ``None`` instead. Refer to the
            changelog for details.

        Canceling :meth:`recv` is safe. There's no risk of losing the next
        message. The next invocation of :meth:`recv` will return it. This
        makes it possible to enforce a timeout by wrapping :meth:`recv` in
        :func:`~asyncio.wait_for`.

        :raises ~websockets.exceptions.ConnectionClosed: when the
            connection is closed
        :raises RuntimeError: if two coroutines call :meth:`recv` concurrently

        """
        if self._pop_message_waiter is not None:
            raise RuntimeError('cannot call recv while another coroutine is already waiting for the next message')
        else:
            while True:
                if len(self.messages) <= 0:
                    pop_message_waiter = self.loop.create_future()
                    self._pop_message_waiter = pop_message_waiter
                    try:
                        await asyncio.wait([
                         pop_message_waiter, self.transfer_data_task],
                          loop=(self.loop if sys.version_info[:2] < (3, 8) else None),
                          return_when=(asyncio.FIRST_COMPLETED))
                    finally:
                        self._pop_message_waiter = None

                    if not pop_message_waiter.done():
                        if self.legacy_recv:
                            return
                        await self.ensure_open()

        message = self.messages.popleft()
        if self._put_message_waiter is not None:
            self._put_message_waiter.set_result(None)
            self._put_message_waiter = None
        return message

    async def send(self, message: Union[(Data, Iterable[Data], AsyncIterable[Data])]) -> None:
        """
        Send a message.

        A string (:class:`str`) is sent as a `Text frame`_. A bytestring or
        bytes-like object (:class:`bytes`, :class:`bytearray`, or
        :class:`memoryview`) is sent as a `Binary frame`_.

        .. _Text frame: https://tools.ietf.org/html/rfc6455#section-5.6
        .. _Binary frame: https://tools.ietf.org/html/rfc6455#section-5.6

        :meth:`send` also accepts an iterable or an asynchronous iterable of
        strings, bytestrings, or bytes-like objects. In that case the message
        is fragmented. Each item is treated as a message fragment and sent in
        its own frame. All items must be of the same type, or else
        :meth:`send` will raise a :exc:`TypeError` and the connection will be
        closed.

        Canceling :meth:`send` is discouraged. Instead, you should close the
        connection with :meth:`close`. Indeed, there only two situations where
        :meth:`send` yields control to the event loop:

        1. The write buffer is full. If you don't want to wait until enough
           data is sent, your only alternative is to close the connection.
           :meth:`close` will likely time out then abort the TCP connection.
        2. ``message`` is an asynchronous iterator. Stopping in the middle of
           a fragmented message will cause a protocol error. Closing the
           connection has the same effect.

        :raises TypeError: for unsupported inputs

        """
        await self.ensure_open()
        while self._fragmented_message_waiter is not None:
            await asyncio.shield(self._fragmented_message_waiter)

        if isinstance(message, (str, bytes, bytearray, memoryview)):
            opcode, data = prepare_data(message)
            await self.write_frame(True, opcode, data)
        else:
            if isinstance(message, Iterable):
                message = cast(Iterable[Data], message)
                iter_message = iter(message)
                try:
                    message_chunk = next(iter_message)
                except StopIteration:
                    return
                else:
                    opcode, data = prepare_data(message_chunk)
                    self._fragmented_message_waiter = asyncio.Future()
                    try:
                        try:
                            await self.write_frame(False, opcode, data)
                            for message_chunk in iter_message:
                                confirm_opcode, data = prepare_data(message_chunk)
                                if confirm_opcode != opcode:
                                    raise TypeError('data contains inconsistent types')
                                await self.write_frame(False, OP_CONT, data)

                            await self.write_frame(True, OP_CONT, b'')
                        except Exception:
                            self.fail_connection(1011)
                            raise

                    finally:
                        self._fragmented_message_waiter.set_result(None)
                        self._fragmented_message_waiter = None

            else:
                if isinstance(message, AsyncIterable):
                    aiter_message = type(message).__aiter__(message)
                    try:
                        message_chunk = await type(aiter_message).__anext__(aiter_message)
                    except StopAsyncIteration:
                        return
                    else:
                        opcode, data = prepare_data(message_chunk)
                        self._fragmented_message_waiter = asyncio.Future()
                        try:
                            try:
                                await self.write_frame(False, opcode, data)
                                async for message_chunk in aiter_message:
                                    confirm_opcode, data = prepare_data(message_chunk)
                                    if confirm_opcode != opcode:
                                        raise TypeError('data contains inconsistent types')
                                    await self.write_frame(False, OP_CONT, data)

                            await self.write_frame(True, OP_CONT, b'')
                        except Exception:
                            self.fail_connection(1011)
                            raise

                    finally:
                        self._fragmented_message_waiter.set_result(None)
                        self._fragmented_message_waiter = None

            else:
                raise TypeError('data must be bytes, str, or iterable')

    async def close(self, code: int=1000, reason: str='') -> None:
        """
        Perform the closing handshake.

        :meth:`close` waits for the other end to complete the handshake and
        for the TCP connection to terminate. As a consequence, there's no need
        to await :meth:`wait_closed`; :meth:`close` already does it.

        :meth:`close` is idempotent: it doesn't do anything once the
        connection is closed.

        Wrapping :func:`close` in :func:`~asyncio.create_task` is safe, given
        that errors during connection termination aren't particularly useful.

        Canceling :meth:`close` is discouraged. If it takes too long, you can
        set a shorter ``close_timeout``. If you don't want to wait, let the
        Python process exit, then the OS will close the TCP connection.

        :param code: WebSocket close code
        :param reason: WebSocket close reason

        """
        try:
            await asyncio.wait_for((self.write_close_frame(serialize_close(code, reason))),
              (self.close_timeout),
              loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
        except asyncio.TimeoutError:
            self.fail_connection()
        else:
            try:
                await asyncio.wait_for((self.transfer_data_task),
                  (self.close_timeout),
                  loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
            except (asyncio.TimeoutError, asyncio.CancelledError):
                pass
            else:
                await asyncio.shield(self.close_connection_task)

    async def ping(self, data: Optional[Data]=None) -> Awaitable[None]:
        """
        Send a ping.

        Return a :class:`~asyncio.Future` which will be completed when the
        corresponding pong is received and which you may ignore if you don't
        want to wait.

        A ping may serve as a keepalive or as a check that the remote endpoint
        received all messages up to this point::

            pong_waiter = await ws.ping()
            await pong_waiter   # only if you want to wait for the pong

        By default, the ping contains four random bytes. This payload may be
        overridden with the optional ``data`` argument which must be a string
        (which will be encoded to UTF-8) or a bytes-like object.

        Canceling :meth:`ping` is discouraged. If :meth:`ping` doesn't return
        immediately, it means the write buffer is full. If you don't want to
        wait, you should close the connection.

        Canceling the :class:`~asyncio.Future` returned by :meth:`ping` has no
        effect.

        """
        await self.ensure_open()
        if data is not None:
            data = encode_data(data)
        else:
            if data in self.pings:
                raise ValueError('already waiting for a pong with the same data')
            while True:
                if data is None or data in self.pings:
                    data = struct.pack('!I', random.getrandbits(32))

        self.pings[data] = self.loop.create_future()
        await self.write_frame(True, OP_PING, data)
        return asyncio.shield(self.pings[data])

    async def pong(self, data: Data=b'') -> None:
        """
        Send a pong.

        An unsolicited pong may serve as a unidirectional heartbeat.

        The payload may be set with the optional ``data`` argument which must
        be a string (which will be encoded to UTF-8) or a bytes-like object.

        Canceling :meth:`pong` is discouraged for the same reason as
        :meth:`ping`.

        """
        await self.ensure_open()
        data = encode_data(data)
        await self.write_frame(True, OP_PONG, data)

    def connection_closed_exc(self) -> ConnectionClosed:
        if self.close_code == 1000 or self.close_code == 1001:
            exception = ConnectionClosedOK(self.close_code, self.close_reason)
        else:
            exception = ConnectionClosedError(self.close_code, self.close_reason)
        exception.__cause__ = self.transfer_data_exc
        return exception

    async def ensure_open(self) -> None:
        """
        Check that the WebSocket connection is open.

        Raise :exc:`~websockets.exceptions.ConnectionClosed` if it isn't.

        """
        if self.state is State.OPEN:
            if self.transfer_data_task.done():
                await asyncio.shield(self.close_connection_task)
                raise self.connection_closed_exc()
            else:
                return
        if self.state is State.CLOSED:
            raise self.connection_closed_exc()
        if self.state is State.CLOSING:
            await asyncio.shield(self.close_connection_task)
            raise self.connection_closed_exc()
        assert self.state is State.CONNECTING
        raise InvalidState("WebSocket connection isn't established yet")

    async def transfer_data(self) -> None:
        """
        Read incoming messages and put them in a queue.

        This coroutine runs in a task until the closing handshake is started.

        """
        try:
            while True:
                message = await self.read_message()
                if message is None:
                    break
                if self.max_queue is not None and len(self.messages) >= self.max_queue:
                    self._put_message_waiter = self.loop.create_future()
                    try:
                        await asyncio.shield(self._put_message_waiter)
                    finally:
                        self._put_message_waiter = None

                else:
                    self.messages.append(message)
                    if self._pop_message_waiter is not None:
                        self._pop_message_waiter.set_result(None)
                        self._pop_message_waiter = None

        except asyncio.CancelledError as exc:
            try:
                self.transfer_data_exc = exc
                raise
            finally:
                exc = None
                del exc

        except ProtocolError as exc:
            try:
                self.transfer_data_exc = exc
                self.fail_connection(1002)
            finally:
                exc = None
                del exc

        except (ConnectionError, EOFError) as exc:
            try:
                self.transfer_data_exc = exc
                self.fail_connection(1006)
            finally:
                exc = None
                del exc

        except UnicodeDecodeError as exc:
            try:
                self.transfer_data_exc = exc
                self.fail_connection(1007)
            finally:
                exc = None
                del exc

        except PayloadTooBig as exc:
            try:
                self.transfer_data_exc = exc
                self.fail_connection(1009)
            finally:
                exc = None
                del exc

        except Exception as exc:
            try:
                logger.error('Error in data transfer', exc_info=True)
                self.transfer_data_exc = exc
                self.fail_connection(1011)
            finally:
                exc = None
                del exc

    async def read_message(self) -> Optional[Data]:
        """
        Read a single message from the connection.

        Re-assemble data frames if the message is fragmented.

        Return ``None`` when the closing handshake is started.

        """
        frame = await self.read_data_frame(max_size=(self.max_size))
        if frame is None:
            return
        else:
            if frame.opcode == OP_TEXT:
                text = True
            else:
                if frame.opcode == OP_BINARY:
                    text = False
                else:
                    raise ProtocolError('unexpected opcode')
            if frame.fin:
                if text:
                    return frame.data.decode('utf-8')
            else:
                return frame.data
                chunks = []
                max_size = self.max_size
                if text:
                    decoder_factory = codecs.getincrementaldecoder('utf-8')
                    decoder = decoder_factory(errors='strict')
                    if max_size is None:

                        def append(frame):
                            chunks.append(decoder.decode(frame.data, frame.fin))

                    else:

                        def append(frame):
                            nonlocal max_size
                            chunks.append(decoder.decode(frame.data, frame.fin))
                            assert isinstance(max_size, int)
                            max_size -= len(frame.data)

                elif max_size is None:

                    def append(frame):
                        chunks.append(frame.data)

                else:

                    def append(frame):
                        nonlocal max_size
                        chunks.append(frame.data)
                        assert isinstance(max_size, int)
                        max_size -= len(frame.data)

            append(frame)
            while True:
                if not frame.fin:
                    frame = await self.read_data_frame(max_size=max_size)
                    if frame is None:
                        raise ProtocolError('incomplete fragmented message')
                    if frame.opcode != OP_CONT:
                        raise ProtocolError('unexpected opcode')
                    append(frame)

        return ('' if text else b'').join(chunks)

    async def read_data_frame(self, max_size: Optional[int]) -> Optional[Frame]:
        """
        Read a single data frame from the connection.

        Process control frames received before the next data frame.

        Return ``None`` if a close frame is encountered before any data frame.

        """
        while True:
            frame = await self.read_frame(max_size)
            if frame.opcode == OP_CLOSE:
                self.close_code, self.close_reason = parse_close(frame.data)
                try:
                    await self.write_close_frame(frame.data)
                except ConnectionClosed:
                    pass
                else:
                    return
            if frame.opcode == OP_PING:
                ping_hex = frame.data.hex() or '[empty]'
                logger.debug('%s - received ping, sending pong: %s', self.side, ping_hex)
                await self.pong(frame.data)
            elif frame.opcode == OP_PONG:
                if frame.data in self.pings:
                    logger.debug('%s - received solicited pong: %s', self.side, frame.data.hex() or '[empty]')
                    ping_id = None
                    ping_ids = []
                    for ping_id, ping in self.pings.items():
                        ping_ids.append(ping_id)
                        if not ping.done():
                            ping.set_result(None)
                        if ping_id == frame.data:
                            break
                        assert False, 'ping_id is in self.pings'
                        for ping_id in ping_ids:
                            del self.pings[ping_id]
                        else:
                            ping_ids = ping_ids[:-1]

                        if ping_ids:
                            pings_hex = ', '.join((ping_id.hex() or '[empty]' for ping_id in ping_ids))
                            plural = 's' if len(ping_ids) > 1 else ''
                            logger.debug('%s - acknowledged previous ping%s: %s', self.side, plural, pings_hex)

                else:
                    logger.debug('%s - received unsolicited pong: %s', self.side, frame.data.hex() or '[empty]')
            else:
                return frame

    async def read_frame(self, max_size: Optional[int]) -> Frame:
        """
        Read a single frame from the connection.

        """
        frame = await Frame.read((self.reader.readexactly),
          mask=(not self.is_client),
          max_size=max_size,
          extensions=(self.extensions))
        logger.debug('%s < %r', self.side, frame)
        return frame

    async def write_frame--- This code section failed: ---

 L.1060         0  LOAD_FAST                'self'
                2  LOAD_ATTR                state
                4  LOAD_FAST                '_expected_state'
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    30  'to 30'

 L.1061        10  LOAD_GLOBAL              InvalidState

 L.1062        12  LOAD_STR                 'Cannot write to a WebSocket in the '
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                state
               18  LOAD_ATTR                name
               20  FORMAT_VALUE          0  ''
               22  LOAD_STR                 ' state'
               24  BUILD_STRING_3        3 

 L.1061        26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM             8  '8'

 L.1065        30  LOAD_GLOBAL              Frame
               32  LOAD_FAST                'fin'
               34  LOAD_FAST                'opcode'
               36  LOAD_FAST                'data'
               38  CALL_FUNCTION_3       3  ''
               40  STORE_FAST               'frame'

 L.1066        42  LOAD_GLOBAL              logger
               44  LOAD_METHOD              debug
               46  LOAD_STR                 '%s > %r'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                side
               52  LOAD_FAST                'frame'
               54  CALL_METHOD_3         3  ''
               56  POP_TOP          

 L.1067        58  LOAD_FAST                'frame'
               60  LOAD_ATTR                write

 L.1068        62  LOAD_FAST                'self'
               64  LOAD_ATTR                transport
               66  LOAD_ATTR                write

 L.1068        68  LOAD_FAST                'self'
               70  LOAD_ATTR                is_client

 L.1068        72  LOAD_FAST                'self'
               74  LOAD_ATTR                extensions

 L.1067        76  LOAD_CONST               ('mask', 'extensions')
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  POP_TOP          

 L.1071        82  SETUP_FINALLY       134  'to 134'

 L.1075        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _drain_lock
               88  BEFORE_ASYNC_WITH
               90  GET_AWAITABLE    
               92  LOAD_CONST               None
               94  YIELD_FROM       
               96  SETUP_ASYNC_WITH    118  'to 118'
               98  POP_TOP          

 L.1077       100  LOAD_FAST                'self'
              102  LOAD_METHOD              _drain
              104  CALL_METHOD_0         0  ''
              106  GET_AWAITABLE    
              108  LOAD_CONST               None
              110  YIELD_FROM       
              112  POP_TOP          
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM_ASYNC_WITH    96  '96'
              118  WITH_CLEANUP_START
              120  GET_AWAITABLE    
              122  LOAD_CONST               None
              124  YIELD_FROM       
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      
              130  POP_BLOCK        
              132  JUMP_FORWARD        176  'to 176'
            134_0  COME_FROM_FINALLY    82  '82'

 L.1078       134  DUP_TOP          
              136  LOAD_GLOBAL              ConnectionError
              138  COMPARE_OP               exception-match
              140  POP_JUMP_IF_FALSE   174  'to 174'
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          

 L.1080       148  LOAD_FAST                'self'
              150  LOAD_METHOD              fail_connection
              152  CALL_METHOD_0         0  ''
              154  POP_TOP          

 L.1083       156  LOAD_FAST                'self'
              158  LOAD_METHOD              ensure_open
              160  CALL_METHOD_0         0  ''
              162  GET_AWAITABLE    
              164  LOAD_CONST               None
              166  YIELD_FROM       
              168  POP_TOP          
              170  POP_EXCEPT       
              172  JUMP_FORWARD        176  'to 176'
            174_0  COME_FROM           140  '140'
              174  END_FINALLY      
            176_0  COME_FROM           172  '172'
            176_1  COME_FROM           132  '132'

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 118_0

    async def write_close_frame(self, data: bytes=b'') -> None:
        """
        Write a close frame if and only if the connection state is OPEN.

        This dedicated coroutine must be used for writing close frames to
        ensure that at most one close frame is sent on a given connection.

        """
        if self.state is State.OPEN:
            self.state = State.CLOSING
            logger.debug('%s - state = CLOSING', self.side)
            await self.write_frame(True, OP_CLOSE, data, _expected_state=(State.CLOSING))

    async def keepalive_ping(self) -> None:
        """
        Send a Ping frame and wait for a Pong frame at regular intervals.

        This coroutine exits when the connection terminates and one of the
        following happens:

        - :meth:`ping` raises :exc:`ConnectionClosed`, or
        - :meth:`close_connection` cancels :attr:`keepalive_ping_task`.

        """
        if self.ping_interval is None:
            return
        try:
            while True:
                await asyncio.sleep((self.ping_interval),
                  loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
                ping_waiter = await self.ping()
                if self.ping_timeout is not None:
                    try:
                        await asyncio.wait_for(ping_waiter,
                          (self.ping_timeout),
                          loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
                    except asyncio.TimeoutError:
                        logger.debug('%s ! timed out waiting for pong', self.side)
                        self.fail_connection(1011)
                        break

        except asyncio.CancelledError:
            raise
        except ConnectionClosed:
            pass
        except Exception:
            logger.warning('Unexpected exception in keepalive ping task', exc_info=True)

    async def close_connection--- This code section failed: ---

 L.1165         0  LOAD_CONST               None
                2  SETUP_FINALLY       204  'to 204'

 L.1167         4  LOAD_GLOBAL              hasattr
                6  LOAD_FAST                'self'
                8  LOAD_STR                 'transfer_data_task'
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    54  'to 54'

 L.1168        14  SETUP_FINALLY        32  'to 32'

 L.1169        16  LOAD_FAST                'self'
               18  LOAD_ATTR                transfer_data_task
               20  GET_AWAITABLE    
               22  LOAD_CONST               None
               24  YIELD_FROM       
               26  POP_TOP          
               28  POP_BLOCK        
               30  JUMP_FORWARD         54  'to 54'
             32_0  COME_FROM_FINALLY    14  '14'

 L.1170        32  DUP_TOP          
               34  LOAD_GLOBAL              asyncio
               36  LOAD_ATTR                CancelledError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    52  'to 52'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.1171        48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            40  '40'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM            30  '30'
             54_2  COME_FROM            12  '12'

 L.1174        54  LOAD_GLOBAL              hasattr
               56  LOAD_FAST                'self'
               58  LOAD_STR                 'keepalive_ping_task'
               60  CALL_FUNCTION_2       2  ''
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L.1175        64  LOAD_FAST                'self'
               66  LOAD_ATTR                keepalive_ping_task
               68  LOAD_METHOD              cancel
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          
             74_0  COME_FROM            62  '62'

 L.1178        74  LOAD_FAST                'self'
               76  LOAD_ATTR                is_client
               78  POP_JUMP_IF_FALSE   128  'to 128'
               80  LOAD_GLOBAL              hasattr
               82  LOAD_FAST                'self'
               84  LOAD_STR                 'transfer_data_task'
               86  CALL_FUNCTION_2       2  ''
               88  POP_JUMP_IF_FALSE   128  'to 128'

 L.1179        90  LOAD_FAST                'self'
               92  LOAD_METHOD              wait_for_connection_lost
               94  CALL_METHOD_0         0  ''
               96  GET_AWAITABLE    
               98  LOAD_CONST               None
              100  YIELD_FROM       
              102  POP_JUMP_IF_FALSE   114  'to 114'

 L.1180       104  POP_BLOCK        
              106  CALL_FINALLY        204  'to 204'
              108  POP_TOP          
              110  LOAD_CONST               None
              112  RETURN_VALUE     
            114_0  COME_FROM           102  '102'

 L.1181       114  LOAD_GLOBAL              logger
              116  LOAD_METHOD              debug
              118  LOAD_STR                 '%s ! timed out waiting for TCP close'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                side
              124  CALL_METHOD_2         2  ''
              126  POP_TOP          
            128_0  COME_FROM            88  '88'
            128_1  COME_FROM            78  '78'

 L.1184       128  LOAD_FAST                'self'
              130  LOAD_ATTR                transport
              132  LOAD_METHOD              can_write_eof
              134  CALL_METHOD_0         0  ''
              136  POP_JUMP_IF_FALSE   200  'to 200'

 L.1185       138  LOAD_GLOBAL              logger
              140  LOAD_METHOD              debug
              142  LOAD_STR                 '%s x half-closing TCP connection'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                side
              148  CALL_METHOD_2         2  ''
              150  POP_TOP          

 L.1186       152  LOAD_FAST                'self'
              154  LOAD_ATTR                transport
              156  LOAD_METHOD              write_eof
              158  CALL_METHOD_0         0  ''
              160  POP_TOP          

 L.1188       162  LOAD_FAST                'self'
              164  LOAD_METHOD              wait_for_connection_lost
              166  CALL_METHOD_0         0  ''
              168  GET_AWAITABLE    
              170  LOAD_CONST               None
              172  YIELD_FROM       
              174  POP_JUMP_IF_FALSE   186  'to 186'

 L.1189       176  POP_BLOCK        
              178  CALL_FINALLY        204  'to 204'
              180  POP_TOP          
              182  LOAD_CONST               None
              184  RETURN_VALUE     
            186_0  COME_FROM           174  '174'

 L.1190       186  LOAD_GLOBAL              logger
              188  LOAD_METHOD              debug
              190  LOAD_STR                 '%s ! timed out waiting for TCP close'
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                side
              196  CALL_METHOD_2         2  ''
              198  POP_TOP          
            200_0  COME_FROM           136  '136'
              200  POP_BLOCK        
              202  BEGIN_FINALLY    
            204_0  COME_FROM           178  '178'
            204_1  COME_FROM           106  '106'
            204_2  COME_FROM_FINALLY     2  '2'

 L.1199       204  LOAD_FAST                'self'
              206  LOAD_ATTR                connection_lost_waiter
              208  LOAD_METHOD              done
              210  CALL_METHOD_0         0  ''
              212  POP_JUMP_IF_FALSE   232  'to 232'
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                transport
              218  LOAD_METHOD              is_closing
              220  CALL_METHOD_0         0  ''
              222  POP_JUMP_IF_FALSE   232  'to 232'

 L.1200       224  POP_FINALLY           0  ''
              226  POP_TOP          
              228  LOAD_CONST               None
              230  RETURN_VALUE     
            232_0  COME_FROM           222  '222'
            232_1  COME_FROM           212  '212'

 L.1203       232  LOAD_GLOBAL              logger
              234  LOAD_METHOD              debug
              236  LOAD_STR                 '%s x closing TCP connection'
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                side
              242  CALL_METHOD_2         2  ''
              244  POP_TOP          

 L.1204       246  LOAD_FAST                'self'
              248  LOAD_ATTR                transport
              250  LOAD_METHOD              close
              252  CALL_METHOD_0         0  ''
              254  POP_TOP          

 L.1206       256  LOAD_FAST                'self'
              258  LOAD_METHOD              wait_for_connection_lost
              260  CALL_METHOD_0         0  ''
              262  GET_AWAITABLE    
              264  LOAD_CONST               None
              266  YIELD_FROM       
          268_270  POP_JUMP_IF_FALSE   280  'to 280'

 L.1207       272  POP_FINALLY           0  ''
              274  POP_TOP          
              276  LOAD_CONST               None
              278  RETURN_VALUE     
            280_0  COME_FROM           268  '268'

 L.1208       280  LOAD_GLOBAL              logger
              282  LOAD_METHOD              debug
              284  LOAD_STR                 '%s ! timed out waiting for TCP close'
              286  LOAD_FAST                'self'
              288  LOAD_ATTR                side
              290  CALL_METHOD_2         2  ''
              292  POP_TOP          

 L.1211       294  LOAD_GLOBAL              logger
              296  LOAD_METHOD              debug
              298  LOAD_STR                 '%s x aborting TCP connection'
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                side
              304  CALL_METHOD_2         2  ''
              306  POP_TOP          

 L.1212       308  LOAD_FAST                'self'
              310  LOAD_ATTR                transport
              312  LOAD_METHOD              abort
              314  CALL_METHOD_0         0  ''
              316  POP_TOP          

 L.1215       318  LOAD_FAST                'self'
              320  LOAD_METHOD              wait_for_connection_lost
              322  CALL_METHOD_0         0  ''
              324  GET_AWAITABLE    
              326  LOAD_CONST               None
              328  YIELD_FROM       
              330  POP_TOP          
              332  END_FINALLY      
              334  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 106

    async def wait_for_connection_lost(self) -> bool:
        """
        Wait until the TCP connection is closed or ``self.close_timeout`` elapses.

        Return ``True`` if the connection is closed and ``False`` otherwise.

        """
        if not self.connection_lost_waiter.done():
            try:
                await asyncio.wait_for((asyncio.shield(self.connection_lost_waiter)),
                  (self.close_timeout),
                  loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
            except asyncio.TimeoutError:
                pass

        return self.connection_lost_waiter.done()

    def fail_connection(self, code: int=1006, reason: str='') -> None:
        """
        7.1.7. Fail the WebSocket Connection

        This requires:

        1. Stopping all processing of incoming data, which means cancelling
           :attr:`transfer_data_task`. The close code will be 1006 unless a
           close frame was received earlier.

        2. Sending a close frame with an appropriate code if the opening
           handshake succeeded and the other side is likely to process it.

        3. Closing the connection. :meth:`close_connection` takes care of
           this once :attr:`transfer_data_task` exits after being canceled.

        (The specification describes these steps in the opposite order.)

        """
        logger.debug('%s ! failing %s WebSocket connection with code %d', self.side, self.state.name, code)
        if hasattr(self, 'transfer_data_task'):
            self.transfer_data_task.cancel()
        if code != 1006:
            if self.state is State.OPEN:
                frame_data = serialize_close(code, reason)
                self.state = State.CLOSING
                logger.debug('%s - state = CLOSING', self.side)
                frame = Frame(True, OP_CLOSE, frame_data)
                logger.debug('%s > %r', self.side, frame)
                frame.write((self.transport.write),
                  mask=(self.is_client), extensions=(self.extensions))
        if not hasattr(self, 'close_connection_task'):
            self.close_connection_task = self.loop.create_task(self.close_connection())

    def abort_pings(self) -> None:
        """
        Raise ConnectionClosed in pending keepalive pings.

        They'll never receive a pong once the connection is closed.

        """
        assert self.state is State.CLOSED
        exc = self.connection_closed_exc()
        for ping in self.pings.values():
            ping.set_exception(exc)
            ping.cancel()
        else:
            if self.pings:
                pings_hex = ', '.join((ping_id.hex() or '[empty]' for ping_id in self.pings))
                plural = 's' if len(self.pings) > 1 else ''
                logger.debug('%s - aborted pending ping%s: %s', self.side, plural, pings_hex)

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        """
        Configure write buffer limits.

        The high-water limit is defined by ``self.write_limit``.

        The low-water limit currently defaults to ``self.write_limit // 4`` in
        :meth:`~asyncio.WriteTransport.set_write_buffer_limits`, which should
        be all right for reasonable use cases of this library.

        This is the earliest point where we can get hold of the transport,
        which means it's the best point for configuring it.

        """
        logger.debug('%s - event = connection_made(%s)', self.side, transport)
        transport = cast(asyncio.Transport, transport)
        transport.set_write_buffer_limits(self.write_limit)
        self.transport = transport
        self.reader.set_transport(transport)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """
        7.1.4. The WebSocket Connection is Closed.

        """
        logger.debug('%s - event = connection_lost(%s)', self.side, exc)
        self.state = State.CLOSED
        logger.debug('%s - state = CLOSED', self.side)
        if not hasattr(self, 'close_code'):
            self.close_code = 1006
        else:
            if not hasattr(self, 'close_reason'):
                self.close_reason = ''
            else:
                logger.debug('%s x code = %d, reason = %s', self.side, self.close_code, self.close_reason or '[no reason]')
                self.abort_pings()
                self.connection_lost_waiter.set_result(None)
                if self.reader is not None:
                    if exc is None:
                        self.reader.feed_eof()
                    else:
                        self.reader.set_exception(exc)
            if not self._paused:
                return
                waiter = self._drain_waiter
                if waiter is None:
                    return
                self._drain_waiter = None
                if waiter.done():
                    return
                if exc is None:
                    waiter.set_result(None)
            else:
                waiter.set_exception(exc)

    def pause_writing(self) -> None:
        assert not self._paused
        self._paused = True

    def resume_writing(self) -> None:
        assert self._paused
        self._paused = False
        waiter = self._drain_waiter
        if waiter is not None:
            self._drain_waiter = None
            if not waiter.done():
                waiter.set_result(None)

    def data_received(self, data: bytes) -> None:
        logger.debug('%s - event = data_received(<%d bytes>)', self.side, len(data))
        self.reader.feed_data(data)

    def eof_received(self) -> None:
        """
        Close the transport after receiving EOF.

        The WebSocket protocol has its own closing handshake: endpoints close
        the TCP or TLS connection after sending and receiving a close frame.

        As a consequence, they never need to write after receiving EOF, so
        there's no reason to keep the transport open by returning ``True``.

        Besides, that doesn't work on TLS connections.

        """
        logger.debug('%s - event = eof_received()', self.side)
        self.reader.feed_eof()