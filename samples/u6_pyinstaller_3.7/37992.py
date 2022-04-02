# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\sslproto.py
import collections, warnings
try:
    import ssl
except ImportError:
    ssl = None

from . import base_events
from . import constants
from . import protocols
from . import transports
from .log import logger

def _create_transport_context(server_side, server_hostname):
    if server_side:
        raise ValueError('Server side SSL needs a valid SSLContext')
    sslcontext = ssl.create_default_context()
    if not server_hostname:
        sslcontext.check_hostname = False
    return sslcontext


_UNWRAPPED = 'UNWRAPPED'
_DO_HANDSHAKE = 'DO_HANDSHAKE'
_WRAPPED = 'WRAPPED'
_SHUTDOWN = 'SHUTDOWN'

class _SSLPipe(object):
    __doc__ = 'An SSL "Pipe".\n\n    An SSL pipe allows you to communicate with an SSL/TLS protocol instance\n    through memory buffers. It can be used to implement a security layer for an\n    existing connection where you don\'t have access to the connection\'s file\n    descriptor, or for some reason you don\'t want to use it.\n\n    An SSL pipe can be in "wrapped" and "unwrapped" mode. In unwrapped mode,\n    data is passed through untransformed. In wrapped mode, application level\n    data is encrypted to SSL record level data and vice versa. The SSL record\n    level is the lowest level in the SSL protocol suite and is what travels\n    as-is over the wire.\n\n    An SslPipe initially is in "unwrapped" mode. To start SSL, call\n    do_handshake(). To shutdown SSL again, call unwrap().\n    '
    max_size = 262144

    def __init__(self, context, server_side, server_hostname=None):
        """
        The *context* argument specifies the ssl.SSLContext to use.

        The *server_side* argument indicates whether this is a server side or
        client side transport.

        The optional *server_hostname* argument can be used to specify the
        hostname you are connecting to. You may only specify this parameter if
        the _ssl module supports Server Name Indication (SNI).
        """
        self._context = context
        self._server_side = server_side
        self._server_hostname = server_hostname
        self._state = _UNWRAPPED
        self._incoming = ssl.MemoryBIO()
        self._outgoing = ssl.MemoryBIO()
        self._sslobj = None
        self._need_ssldata = False
        self._handshake_cb = None
        self._shutdown_cb = None

    @property
    def context(self):
        """The SSL context passed to the constructor."""
        return self._context

    @property
    def ssl_object(self):
        """The internal ssl.SSLObject instance.

        Return None if the pipe is not wrapped.
        """
        return self._sslobj

    @property
    def need_ssldata(self):
        """Whether more record level data is needed to complete a handshake
        that is currently in progress."""
        return self._need_ssldata

    @property
    def wrapped(self):
        """
        Whether a security layer is currently in effect.

        Return False during handshake.
        """
        return self._state == _WRAPPED

    def do_handshake(self, callback=None):
        """Start the SSL handshake.

        Return a list of ssldata. A ssldata element is a list of buffers

        The optional *callback* argument can be used to install a callback that
        will be called when the handshake is complete. The callback will be
        called with None if successful, else an exception instance.
        """
        if self._state != _UNWRAPPED:
            raise RuntimeError('handshake in progress or completed')
        self._sslobj = self._context.wrap_bio((self._incoming),
          (self._outgoing), server_side=(self._server_side),
          server_hostname=(self._server_hostname))
        self._state = _DO_HANDSHAKE
        self._handshake_cb = callback
        ssldata, appdata = self.feed_ssldata(b'', only_handshake=True)
        assert len(appdata) == 0
        return ssldata

    def shutdown(self, callback=None):
        """Start the SSL shutdown sequence.

        Return a list of ssldata. A ssldata element is a list of buffers

        The optional *callback* argument can be used to install a callback that
        will be called when the shutdown is complete. The callback will be
        called without arguments.
        """
        if self._state == _UNWRAPPED:
            raise RuntimeError('no security layer present')
        else:
            if self._state == _SHUTDOWN:
                raise RuntimeError('shutdown in progress')
            assert self._state in (_WRAPPED, _DO_HANDSHAKE)
            self._state = _SHUTDOWN
            self._shutdown_cb = callback
            ssldata, appdata = self.feed_ssldata(b'')
            if not appdata == []:
                if not appdata == [b'']:
                    raise AssertionError
        return ssldata

    def feed_eof(self):
        """Send a potentially "ragged" EOF.

        This method will raise an SSL_ERROR_EOF exception if the EOF is
        unexpected.
        """
        self._incoming.write_eof()
        ssldata, appdata = self.feed_ssldata(b'')
        if not appdata == []:
            assert appdata == [b'']

    def feed_ssldata--- This code section failed: ---

 L. 172         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _state
                4  LOAD_GLOBAL              _UNWRAPPED
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    34  'to 34'

 L. 174        10  LOAD_FAST                'data'
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 175        14  LOAD_FAST                'data'
               16  BUILD_LIST_1          1 
               18  STORE_FAST               'appdata'
               20  JUMP_FORWARD         26  'to 26'
             22_0  COME_FROM            12  '12'

 L. 177        22  BUILD_LIST_0          0 
               24  STORE_FAST               'appdata'
             26_0  COME_FROM            20  '20'

 L. 178        26  BUILD_LIST_0          0 
               28  LOAD_FAST                'appdata'
               30  BUILD_TUPLE_2         2 
               32  RETURN_VALUE     
             34_0  COME_FROM             8  '8'

 L. 180        34  LOAD_CONST               False
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _need_ssldata

 L. 181        40  LOAD_FAST                'data'
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L. 182        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _incoming
               48  LOAD_METHOD              write
               50  LOAD_FAST                'data'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_TOP          
             56_0  COME_FROM            42  '42'

 L. 184        56  BUILD_LIST_0          0 
               58  STORE_FAST               'ssldata'

 L. 185        60  BUILD_LIST_0          0 
               62  STORE_FAST               'appdata'

 L. 186        64  SETUP_EXCEPT        246  'to 246'

 L. 187        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _state
               70  LOAD_GLOBAL              _DO_HANDSHAKE
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE   120  'to 120'

 L. 189        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _sslobj
               80  LOAD_METHOD              do_handshake
               82  CALL_METHOD_0         0  '0 positional arguments'
               84  POP_TOP          

 L. 190        86  LOAD_GLOBAL              _WRAPPED
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _state

 L. 191        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _handshake_cb
               96  POP_JUMP_IF_FALSE   108  'to 108'

 L. 192        98  LOAD_FAST                'self'
              100  LOAD_METHOD              _handshake_cb
              102  LOAD_CONST               None
              104  CALL_METHOD_1         1  '1 positional argument'
              106  POP_TOP          
            108_0  COME_FROM            96  '96'

 L. 193       108  LOAD_FAST                'only_handshake'
              110  POP_JUMP_IF_FALSE   120  'to 120'

 L. 194       112  LOAD_FAST                'ssldata'
              114  LOAD_FAST                'appdata'
              116  BUILD_TUPLE_2         2 
              118  RETURN_VALUE     
            120_0  COME_FROM           110  '110'
            120_1  COME_FROM            74  '74'

 L. 197       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _state
              124  LOAD_GLOBAL              _WRAPPED
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   168  'to 168'

 L. 199       130  SETUP_LOOP          242  'to 242'
            132_0  COME_FROM           158  '158'

 L. 200       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _sslobj
              136  LOAD_METHOD              read
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                max_size
              142  CALL_METHOD_1         1  '1 positional argument'
              144  STORE_FAST               'chunk'

 L. 201       146  LOAD_FAST                'appdata'
              148  LOAD_METHOD              append
              150  LOAD_FAST                'chunk'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  POP_TOP          

 L. 202       156  LOAD_FAST                'chunk'
              158  POP_JUMP_IF_TRUE    132  'to 132'

 L. 203       160  BREAK_LOOP       
              162  JUMP_BACK           132  'to 132'
              164  POP_BLOCK        
              166  JUMP_FORWARD        242  'to 242'
            168_0  COME_FROM           128  '128'

 L. 205       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _state
              172  LOAD_GLOBAL              _SHUTDOWN
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   216  'to 216'

 L. 207       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _sslobj
              182  LOAD_METHOD              unwrap
              184  CALL_METHOD_0         0  '0 positional arguments'
              186  POP_TOP          

 L. 208       188  LOAD_CONST               None
              190  LOAD_FAST                'self'
              192  STORE_ATTR               _sslobj

 L. 209       194  LOAD_GLOBAL              _UNWRAPPED
              196  LOAD_FAST                'self'
              198  STORE_ATTR               _state

 L. 210       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _shutdown_cb
              204  POP_JUMP_IF_FALSE   242  'to 242'

 L. 211       206  LOAD_FAST                'self'
              208  LOAD_METHOD              _shutdown_cb
              210  CALL_METHOD_0         0  '0 positional arguments'
              212  POP_TOP          
              214  JUMP_FORWARD        242  'to 242'
            216_0  COME_FROM           176  '176'

 L. 213       216  LOAD_FAST                'self'
              218  LOAD_ATTR                _state
              220  LOAD_GLOBAL              _UNWRAPPED
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE   242  'to 242'

 L. 215       226  LOAD_FAST                'appdata'
              228  LOAD_METHOD              append
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                _incoming
              234  LOAD_METHOD              read
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  POP_TOP          
            242_0  COME_FROM           224  '224'
            242_1  COME_FROM           214  '214'
            242_2  COME_FROM           204  '204'
            242_3  COME_FROM           166  '166'
            242_4  COME_FROM_LOOP      130  '130'
              242  POP_BLOCK        
              244  JUMP_FORWARD        368  'to 368'
            246_0  COME_FROM_EXCEPT     64  '64'

 L. 216       246  DUP_TOP          
              248  LOAD_GLOBAL              ssl
              250  LOAD_ATTR                SSLError
              252  LOAD_GLOBAL              ssl
              254  LOAD_ATTR                CertificateError
              256  BUILD_TUPLE_2         2 
              258  COMPARE_OP               exception-match
          260_262  POP_JUMP_IF_FALSE   366  'to 366'
              264  POP_TOP          
              266  STORE_FAST               'exc'
              268  POP_TOP          
              270  SETUP_FINALLY       354  'to 354'

 L. 217       272  LOAD_GLOBAL              getattr
              274  LOAD_FAST                'exc'
              276  LOAD_STR                 'errno'
              278  LOAD_CONST               None
              280  CALL_FUNCTION_3       3  '3 positional arguments'
              282  STORE_FAST               'exc_errno'

 L. 218       284  LOAD_FAST                'exc_errno'

 L. 219       286  LOAD_GLOBAL              ssl
              288  LOAD_ATTR                SSL_ERROR_WANT_READ
              290  LOAD_GLOBAL              ssl
              292  LOAD_ATTR                SSL_ERROR_WANT_WRITE

 L. 220       294  LOAD_GLOBAL              ssl
              296  LOAD_ATTR                SSL_ERROR_SYSCALL
              298  BUILD_TUPLE_3         3 
              300  COMPARE_OP               not-in
          302_304  POP_JUMP_IF_FALSE   338  'to 338'

 L. 221       306  LOAD_FAST                'self'
              308  LOAD_ATTR                _state
              310  LOAD_GLOBAL              _DO_HANDSHAKE
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   336  'to 336'
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                _handshake_cb
          322_324  POP_JUMP_IF_FALSE   336  'to 336'

 L. 222       326  LOAD_FAST                'self'
              328  LOAD_METHOD              _handshake_cb
              330  LOAD_FAST                'exc'
              332  CALL_METHOD_1         1  '1 positional argument'
              334  POP_TOP          
            336_0  COME_FROM           322  '322'
            336_1  COME_FROM           314  '314'

 L. 223       336  RAISE_VARARGS_0       0  'reraise'
            338_0  COME_FROM           302  '302'

 L. 224       338  LOAD_FAST                'exc_errno'
              340  LOAD_GLOBAL              ssl
              342  LOAD_ATTR                SSL_ERROR_WANT_READ
              344  COMPARE_OP               ==
              346  LOAD_FAST                'self'
              348  STORE_ATTR               _need_ssldata
              350  POP_BLOCK        
              352  LOAD_CONST               None
            354_0  COME_FROM_FINALLY   270  '270'
              354  LOAD_CONST               None
              356  STORE_FAST               'exc'
              358  DELETE_FAST              'exc'
              360  END_FINALLY      
              362  POP_EXCEPT       
              364  JUMP_FORWARD        368  'to 368'
            366_0  COME_FROM           260  '260'
              366  END_FINALLY      
            368_0  COME_FROM           364  '364'
            368_1  COME_FROM           244  '244'

 L. 228       368  LOAD_FAST                'self'
              370  LOAD_ATTR                _outgoing
              372  LOAD_ATTR                pending
          374_376  POP_JUMP_IF_FALSE   394  'to 394'

 L. 229       378  LOAD_FAST                'ssldata'
              380  LOAD_METHOD              append
              382  LOAD_FAST                'self'
              384  LOAD_ATTR                _outgoing
              386  LOAD_METHOD              read
              388  CALL_METHOD_0         0  '0 positional arguments'
              390  CALL_METHOD_1         1  '1 positional argument'
              392  POP_TOP          
            394_0  COME_FROM           374  '374'

 L. 230       394  LOAD_FAST                'ssldata'
              396  LOAD_FAST                'appdata'
              398  BUILD_TUPLE_2         2 
              400  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 166

    def feed_appdata(self, data, offset=0):
        """Feed plaintext data into the pipe.

        Return an (ssldata, offset) tuple. The ssldata element is a list of
        buffers containing record level data that needs to be sent to the
        remote SSL instance. The offset is the number of plaintext bytes that
        were processed, which may be less than the length of data.

        NOTE: In case of short writes, this call MUST be retried with the SAME
        buffer passed into the *data* argument (i.e. the id() must be the
        same). This is an OpenSSL requirement. A further particularity is that
        a short write will always have offset == 0, because the _ssl module
        does not enable partial writes. And even though the offset is zero,
        there will still be encrypted data in ssldata.
        """
        assert 0 <= offset <= len(data)
        if self._state == _UNWRAPPED:
            if offset < len(data):
                ssldata = [
                 data[offset:]]
            else:
                ssldata = []
            return (
             ssldata, len(data))
        ssldata = []
        view = memoryview(data)
        while 1:
            self._need_ssldata = False
            try:
                if offset < len(view):
                    offset += self._sslobj.write(view[offset:])
            except ssl.SSLError as exc:
                try:
                    exc_errno = getattr(exc, 'errno', None)
                    if exc.reason == 'PROTOCOL_IS_SHUTDOWN':
                        exc_errno = exc.errno = ssl.SSL_ERROR_WANT_READ
                    if exc_errno not in (ssl.SSL_ERROR_WANT_READ,
                     ssl.SSL_ERROR_WANT_WRITE,
                     ssl.SSL_ERROR_SYSCALL):
                        raise
                    self._need_ssldata = exc_errno == ssl.SSL_ERROR_WANT_READ
                finally:
                    exc = None
                    del exc

            if self._outgoing.pending:
                ssldata.append(self._outgoing.read())
            if offset == len(view) or self._need_ssldata:
                break

        return (
         ssldata, offset)


class _SSLProtocolTransport(transports._FlowControlMixin, transports.Transport):
    _sendfile_compatible = constants._SendfileMode.FALLBACK

    def __init__(self, loop, ssl_protocol):
        self._loop = loop
        self._ssl_protocol = ssl_protocol
        self._closed = False

    def get_extra_info(self, name, default=None):
        """Get optional transport information."""
        return self._ssl_protocol._get_extra_info(name, default)

    def set_protocol(self, protocol):
        self._ssl_protocol._set_app_protocol(protocol)

    def get_protocol(self):
        return self._ssl_protocol._app_protocol

    def is_closing(self):
        return self._closed

    def close(self):
        """Close the transport.

        Buffered data will be flushed asynchronously.  No more data
        will be received.  After all buffered data is flushed, the
        protocol's connection_lost() method will (eventually) called
        with None as its argument.
        """
        self._closed = True
        self._ssl_protocol._start_shutdown()

    def __del__(self):
        if not self._closed:
            warnings.warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
            self.close()

    def is_reading(self):
        tr = self._ssl_protocol._transport
        if tr is None:
            raise RuntimeError('SSL transport has not been initialized yet')
        return tr.is_reading()

    def pause_reading(self):
        """Pause the receiving end.

        No data will be passed to the protocol's data_received()
        method until resume_reading() is called.
        """
        self._ssl_protocol._transport.pause_reading()

    def resume_reading(self):
        """Resume the receiving end.

        Data received will once again be passed to the protocol's
        data_received() method.
        """
        self._ssl_protocol._transport.resume_reading()

    def set_write_buffer_limits(self, high=None, low=None):
        """Set the high- and low-water limits for write flow control.

        These two values control when to call the protocol's
        pause_writing() and resume_writing() methods.  If specified,
        the low-water limit must be less than or equal to the
        high-water limit.  Neither value can be negative.

        The defaults are implementation-specific.  If only the
        high-water limit is given, the low-water limit defaults to an
        implementation-specific value less than or equal to the
        high-water limit.  Setting high to zero forces low to zero as
        well, and causes pause_writing() to be called whenever the
        buffer becomes non-empty.  Setting low to zero causes
        resume_writing() to be called only once the buffer is empty.
        Use of zero for either limit is generally sub-optimal as it
        reduces opportunities for doing I/O and computation
        concurrently.
        """
        self._ssl_protocol._transport.set_write_buffer_limits(high, low)

    def get_write_buffer_size(self):
        """Return the current size of the write buffer."""
        return self._ssl_protocol._transport.get_write_buffer_size()

    @property
    def _protocol_paused(self):
        return self._ssl_protocol._transport._protocol_paused

    def write(self, data):
        """Write some data bytes to the transport.

        This does not block; it buffers the data and arranges for it
        to be sent out asynchronously.
        """
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError(f"data: expecting a bytes-like instance, got {type(data).__name__}")
        else:
            return data or None
        self._ssl_protocol._write_appdata(data)

    def can_write_eof(self):
        """Return True if this transport supports write_eof(), False if not."""
        return False

    def abort(self):
        """Close the transport immediately.

        Buffered data will be lost.  No more data will be received.
        The protocol's connection_lost() method will (eventually) be
        called with None as its argument.
        """
        self._ssl_protocol._abort()
        self._closed = True


class SSLProtocol(protocols.Protocol):
    __doc__ = 'SSL protocol.\n\n    Implementation of SSL on top of a socket using incoming and outgoing\n    buffers which are ssl.MemoryBIO objects.\n    '

    def __init__(self, loop, app_protocol, sslcontext, waiter, server_side=False, server_hostname=None, call_connection_made=True, ssl_handshake_timeout=None):
        if ssl is None:
            raise RuntimeError('stdlib ssl module not available')
        if ssl_handshake_timeout is None:
            ssl_handshake_timeout = constants.SSL_HANDSHAKE_TIMEOUT
        else:
            if ssl_handshake_timeout <= 0:
                raise ValueError(f"ssl_handshake_timeout should be a positive number, got {ssl_handshake_timeout}")
            else:
                sslcontext = sslcontext or _create_transport_context(server_side, server_hostname)
            self._server_side = server_side
            if server_hostname:
                self._server_hostname = server_side or server_hostname
            else:
                self._server_hostname = None
            self._sslcontext = sslcontext
            self._extra = dict(sslcontext=sslcontext)
            self._write_backlog = collections.deque()
            self._write_buffer_size = 0
            self._waiter = waiter
            self._loop = loop
            self._set_app_protocol(app_protocol)
            self._app_transport = _SSLProtocolTransport(self._loop, self)
            self._sslpipe = None
            self._session_established = False
            self._in_handshake = False
            self._in_shutdown = False
            self._transport = None
            self._call_connection_made = call_connection_made
            self._ssl_handshake_timeout = ssl_handshake_timeout

    def _set_app_protocol(self, app_protocol):
        self._app_protocol = app_protocol
        self._app_protocol_is_buffer = isinstance(app_protocol, protocols.BufferedProtocol)

    def _wakeup_waiter(self, exc=None):
        if self._waiter is None:
            return
            if not self._waiter.cancelled():
                if exc is not None:
                    self._waiter.set_exception(exc)
        else:
            self._waiter.set_result(None)
        self._waiter = None

    def connection_made(self, transport):
        """Called when the low-level connection is made.

        Start the SSL handshake.
        """
        self._transport = transport
        self._sslpipe = _SSLPipe(self._sslcontext, self._server_side, self._server_hostname)
        self._start_handshake()

    def connection_lost(self, exc):
        """Called when the low-level connection is lost or closed.

        The argument is an exception object or None (the latter
        meaning a regular EOF is received or the connection was
        aborted or closed).
        """
        if self._session_established:
            self._session_established = False
            self._loop.call_soon(self._app_protocol.connection_lost, exc)
        else:
            if self._app_transport is not None:
                self._app_transport._closed = True
        self._transport = None
        self._app_transport = None
        if getattr(self, '_handshake_timeout_handle', None):
            self._handshake_timeout_handle.cancel()
        self._wakeup_waiter(exc)
        self._app_protocol = None
        self._sslpipe = None

    def pause_writing(self):
        """Called when the low-level transport's buffer goes over
        the high-water mark.
        """
        self._app_protocol.pause_writing()

    def resume_writing(self):
        """Called when the low-level transport's buffer drains below
        the low-water mark.
        """
        self._app_protocol.resume_writing()

    def data_received(self, data):
        """Called when some SSL data is received.

        The argument is a bytes object.
        """
        if self._sslpipe is None:
            return
        try:
            ssldata, appdata = self._sslpipe.feed_ssldata(data)
        except Exception as e:
            try:
                self._fatal_error(e, 'SSL error in data received')
                return
            finally:
                e = None
                del e

        for chunk in ssldata:
            self._transport.write(chunk)

        for chunk in appdata:
            if chunk:
                try:
                    if self._app_protocol_is_buffer:
                        protocols._feed_data_to_buffered_proto(self._app_protocol, chunk)
                    else:
                        self._app_protocol.data_received(chunk)
                except Exception as ex:
                    try:
                        self._fatal_error(ex, 'application protocol failed to receive SSL data')
                        return
                    finally:
                        ex = None
                        del ex

            else:
                self._start_shutdown()
                break

    def eof_received(self):
        """Called when the other end of the low-level stream
        is half-closed.

        If this returns a false value (including None), the transport
        will close itself.  If it returns a true value, closing the
        transport is up to the protocol.
        """
        try:
            if self._loop.get_debug():
                logger.debug('%r received EOF', self)
            self._wakeup_waiter(ConnectionResetError)
            if not self._in_handshake:
                keep_open = self._app_protocol.eof_received()
                if keep_open:
                    logger.warning('returning true from eof_received() has no effect when using ssl')
        finally:
            self._transport.close()

    def _get_extra_info(self, name, default=None):
        if name in self._extra:
            return self._extra[name]
        if self._transport is not None:
            return self._transport.get_extra_info(name, default)
        return default

    def _start_shutdown(self):
        if self._in_shutdown:
            return
        if self._in_handshake:
            self._abort()
        else:
            self._in_shutdown = True
            self._write_appdata(b'')

    def _write_appdata(self, data):
        self._write_backlog.append((data, 0))
        self._write_buffer_size += len(data)
        self._process_write_backlog()

    def _start_handshake(self):
        if self._loop.get_debug():
            logger.debug('%r starts SSL handshake', self)
            self._handshake_start_time = self._loop.time()
        else:
            self._handshake_start_time = None
        self._in_handshake = True
        self._write_backlog.append((b'', 1))
        self._handshake_timeout_handle = self._loop.call_later(self._ssl_handshake_timeout, self._check_handshake_timeout)
        self._process_write_backlog()

    def _check_handshake_timeout(self):
        if self._in_handshake is True:
            msg = f"SSL handshake is taking longer than {self._ssl_handshake_timeout} seconds: aborting the connection"
            self._fatal_error(ConnectionAbortedError(msg))

    def _on_handshake_complete(self, handshake_exc):
        self._in_handshake = False
        self._handshake_timeout_handle.cancel()
        sslobj = self._sslpipe.ssl_object
        try:
            if handshake_exc is not None:
                raise handshake_exc
            peercert = sslobj.getpeercert()
        except Exception as exc:
            try:
                if isinstance(exc, ssl.CertificateError):
                    msg = 'SSL handshake failed on verifying the certificate'
                else:
                    msg = 'SSL handshake failed'
                self._fatal_error(exc, msg)
                return
            finally:
                exc = None
                del exc

        if self._loop.get_debug():
            dt = self._loop.time() - self._handshake_start_time
            logger.debug('%r: SSL handshake took %.1f ms', self, dt * 1000.0)
        self._extra.update(peercert=peercert, cipher=(sslobj.cipher()),
          compression=(sslobj.compression()),
          ssl_object=sslobj)
        if self._call_connection_made:
            self._app_protocol.connection_made(self._app_transport)
        self._wakeup_waiter()
        self._session_established = True
        self._loop.call_soon(self._process_write_backlog)

    def _process_write_backlog(self):
        if self._transport is None or self._sslpipe is None:
            return
        try:
            for i in range(len(self._write_backlog)):
                data, offset = self._write_backlog[0]
                if data:
                    ssldata, offset = self._sslpipe.feed_appdata(data, offset)
                else:
                    if offset:
                        ssldata = self._sslpipe.do_handshake(self._on_handshake_complete)
                        offset = 1
                    else:
                        ssldata = self._sslpipe.shutdown(self._finalize)
                        offset = 1
                for chunk in ssldata:
                    self._transport.write(chunk)

                if offset < len(data):
                    self._write_backlog[0] = (
                     data, offset)
                    assert self._sslpipe.need_ssldata
                    if self._transport._paused:
                        self._transport.resume_reading()
                    break
                del self._write_backlog[0]
                self._write_buffer_size -= len(data)

        except Exception as exc:
            try:
                if self._in_handshake:
                    self._on_handshake_complete(exc)
                else:
                    self._fatal_error(exc, 'Fatal error on SSL transport')
            finally:
                exc = None
                del exc

    def _fatal_error(self, exc, message='Fatal error on transport'):
        if isinstance(exc, OSError):
            if self._loop.get_debug():
                logger.debug('%r: %s', self, message, exc_info=True)
        else:
            self._loop.call_exception_handler({'message':message, 
             'exception':exc, 
             'transport':self._transport, 
             'protocol':self})
        if self._transport:
            self._transport._force_close(exc)

    def _finalize(self):
        self._sslpipe = None
        if self._transport is not None:
            self._transport.close()

    def _abort(self):
        try:
            if self._transport is not None:
                self._transport.abort()
        finally:
            self._finalize()