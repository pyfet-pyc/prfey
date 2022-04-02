# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\sslproto.py
import collections, warnings
try:
    import ssl
except ImportError:
    ssl = None
else:
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
            if self._state == _SHUTDOWN:
                raise RuntimeError('shutdown in progress')
            assert self._state in (_WRAPPED, _DO_HANDSHAKE)
            self._state = _SHUTDOWN
            self._shutdown_cb = callback
            ssldata, appdata = self.feed_ssldata(b'')
            if not appdata == []:
                assert appdata == [b'']
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
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            42  '42'

 L. 184        56  BUILD_LIST_0          0 
               58  STORE_FAST               'ssldata'

 L. 185        60  BUILD_LIST_0          0 
               62  STORE_FAST               'appdata'

 L. 186        64  SETUP_FINALLY       244  'to 244'

 L. 187        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _state
               70  LOAD_GLOBAL              _DO_HANDSHAKE
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE   122  'to 122'

 L. 189        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _sslobj
               80  LOAD_METHOD              do_handshake
               82  CALL_METHOD_0         0  ''
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
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
            108_0  COME_FROM            96  '96'

 L. 193       108  LOAD_FAST                'only_handshake'
              110  POP_JUMP_IF_FALSE   122  'to 122'

 L. 194       112  LOAD_FAST                'ssldata'
              114  LOAD_FAST                'appdata'
              116  BUILD_TUPLE_2         2 
              118  POP_BLOCK        
              120  RETURN_VALUE     
            122_0  COME_FROM           110  '110'
            122_1  COME_FROM            74  '74'

 L. 197       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _state
              126  LOAD_GLOBAL              _WRAPPED
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   166  'to 166'
            132_0  COME_FROM           162  '162'
            132_1  COME_FROM           158  '158'

 L. 200       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _sslobj
              136  LOAD_METHOD              read
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                max_size
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'chunk'

 L. 201       146  LOAD_FAST                'appdata'
              148  LOAD_METHOD              append
              150  LOAD_FAST                'chunk'
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          

 L. 202       156  LOAD_FAST                'chunk'
              158  POP_JUMP_IF_TRUE_BACK   132  'to 132'

 L. 203       160  JUMP_FORWARD        240  'to 240'
              162  JUMP_BACK           132  'to 132'
              164  JUMP_FORWARD        240  'to 240'
            166_0  COME_FROM           130  '130'

 L. 205       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _state
              170  LOAD_GLOBAL              _SHUTDOWN
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   214  'to 214'

 L. 207       176  LOAD_FAST                'self'
              178  LOAD_ATTR                _sslobj
              180  LOAD_METHOD              unwrap
              182  CALL_METHOD_0         0  ''
              184  POP_TOP          

 L. 208       186  LOAD_CONST               None
              188  LOAD_FAST                'self'
              190  STORE_ATTR               _sslobj

 L. 209       192  LOAD_GLOBAL              _UNWRAPPED
              194  LOAD_FAST                'self'
              196  STORE_ATTR               _state

 L. 210       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _shutdown_cb
              202  POP_JUMP_IF_FALSE   240  'to 240'

 L. 211       204  LOAD_FAST                'self'
              206  LOAD_METHOD              _shutdown_cb
              208  CALL_METHOD_0         0  ''
              210  POP_TOP          
              212  JUMP_FORWARD        240  'to 240'
            214_0  COME_FROM           174  '174'

 L. 213       214  LOAD_FAST                'self'
              216  LOAD_ATTR                _state
              218  LOAD_GLOBAL              _UNWRAPPED
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   240  'to 240'

 L. 215       224  LOAD_FAST                'appdata'
              226  LOAD_METHOD              append
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                _incoming
              232  LOAD_METHOD              read
              234  CALL_METHOD_0         0  ''
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
            240_0  COME_FROM           222  '222'
            240_1  COME_FROM           212  '212'
            240_2  COME_FROM           202  '202'
            240_3  COME_FROM           164  '164'
            240_4  COME_FROM           160  '160'
              240  POP_BLOCK        
              242  JUMP_FORWARD        366  'to 366'
            244_0  COME_FROM_FINALLY    64  '64'

 L. 216       244  DUP_TOP          
              246  LOAD_GLOBAL              ssl
              248  LOAD_ATTR                SSLError
              250  LOAD_GLOBAL              ssl
              252  LOAD_ATTR                CertificateError
              254  BUILD_TUPLE_2         2 
              256  COMPARE_OP               exception-match
          258_260  POP_JUMP_IF_FALSE   364  'to 364'
              262  POP_TOP          
              264  STORE_FAST               'exc'
              266  POP_TOP          
              268  SETUP_FINALLY       352  'to 352'

 L. 217       270  LOAD_GLOBAL              getattr
              272  LOAD_FAST                'exc'
              274  LOAD_STR                 'errno'
              276  LOAD_CONST               None
              278  CALL_FUNCTION_3       3  ''
              280  STORE_FAST               'exc_errno'

 L. 218       282  LOAD_FAST                'exc_errno'

 L. 219       284  LOAD_GLOBAL              ssl
              286  LOAD_ATTR                SSL_ERROR_WANT_READ

 L. 219       288  LOAD_GLOBAL              ssl
              290  LOAD_ATTR                SSL_ERROR_WANT_WRITE

 L. 220       292  LOAD_GLOBAL              ssl
              294  LOAD_ATTR                SSL_ERROR_SYSCALL

 L. 218       296  BUILD_TUPLE_3         3 
              298  COMPARE_OP               not-in
          300_302  POP_JUMP_IF_FALSE   336  'to 336'

 L. 221       304  LOAD_FAST                'self'
              306  LOAD_ATTR                _state
              308  LOAD_GLOBAL              _DO_HANDSHAKE
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   334  'to 334'
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                _handshake_cb
          320_322  POP_JUMP_IF_FALSE   334  'to 334'

 L. 222       324  LOAD_FAST                'self'
              326  LOAD_METHOD              _handshake_cb
              328  LOAD_FAST                'exc'
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          
            334_0  COME_FROM           320  '320'
            334_1  COME_FROM           312  '312'

 L. 223       334  RAISE_VARARGS_0       0  'reraise'
            336_0  COME_FROM           300  '300'

 L. 224       336  LOAD_FAST                'exc_errno'
              338  LOAD_GLOBAL              ssl
              340  LOAD_ATTR                SSL_ERROR_WANT_READ
              342  COMPARE_OP               ==
              344  LOAD_FAST                'self'
              346  STORE_ATTR               _need_ssldata
              348  POP_BLOCK        
              350  BEGIN_FINALLY    
            352_0  COME_FROM_FINALLY   268  '268'
              352  LOAD_CONST               None
              354  STORE_FAST               'exc'
              356  DELETE_FAST              'exc'
              358  END_FINALLY      
              360  POP_EXCEPT       
              362  JUMP_FORWARD        366  'to 366'
            364_0  COME_FROM           258  '258'
              364  END_FINALLY      
            366_0  COME_FROM           362  '362'
            366_1  COME_FROM           242  '242'

 L. 228       366  LOAD_FAST                'self'
              368  LOAD_ATTR                _outgoing
              370  LOAD_ATTR                pending
          372_374  POP_JUMP_IF_FALSE   392  'to 392'

 L. 229       376  LOAD_FAST                'ssldata'
              378  LOAD_METHOD              append
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                _outgoing
              384  LOAD_METHOD              read
              386  CALL_METHOD_0         0  ''
              388  CALL_METHOD_1         1  ''
              390  POP_TOP          
            392_0  COME_FROM           372  '372'

 L. 230       392  LOAD_FAST                'ssldata'
              394  LOAD_FAST                'appdata'
              396  BUILD_TUPLE_2         2 
              398  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 162

        def feed_appdata--- This code section failed: ---

 L. 247         0  LOAD_CONST               0
                2  LOAD_FAST                'offset'
                4  DUP_TOP          
                6  ROT_THREE        
                8  COMPARE_OP               <=
               10  POP_JUMP_IF_FALSE    24  'to 24'
               12  LOAD_GLOBAL              len
               14  LOAD_FAST                'data'
               16  CALL_FUNCTION_1       1  ''
               18  COMPARE_OP               <=
               20  POP_JUMP_IF_TRUE     30  'to 30'
               22  JUMP_FORWARD         26  'to 26'
             24_0  COME_FROM            10  '10'
               24  POP_TOP          
             26_0  COME_FROM            22  '22'
               26  LOAD_GLOBAL              AssertionError
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 248        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _state
               34  LOAD_GLOBAL              _UNWRAPPED
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    84  'to 84'

 L. 250        40  LOAD_FAST                'offset'
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'data'
               46  CALL_FUNCTION_1       1  ''
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE    68  'to 68'

 L. 251        52  LOAD_FAST                'data'
               54  LOAD_FAST                'offset'
               56  LOAD_CONST               None
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  BUILD_LIST_1          1 
               64  STORE_FAST               'ssldata'
               66  JUMP_FORWARD         72  'to 72'
             68_0  COME_FROM            50  '50'

 L. 253        68  BUILD_LIST_0          0 
               70  STORE_FAST               'ssldata'
             72_0  COME_FROM            66  '66'

 L. 254        72  LOAD_FAST                'ssldata'
               74  LOAD_GLOBAL              len
               76  LOAD_FAST                'data'
               78  CALL_FUNCTION_1       1  ''
               80  BUILD_TUPLE_2         2 
               82  RETURN_VALUE     
             84_0  COME_FROM            38  '38'

 L. 256        84  BUILD_LIST_0          0 
               86  STORE_FAST               'ssldata'

 L. 257        88  LOAD_GLOBAL              memoryview
               90  LOAD_FAST                'data'
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'view'
             96_0  COME_FROM           298  '298'
             96_1  COME_FROM           292  '292'

 L. 259        96  LOAD_CONST               False
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _need_ssldata

 L. 260       102  SETUP_FINALLY       144  'to 144'

 L. 261       104  LOAD_FAST                'offset'
              106  LOAD_GLOBAL              len
              108  LOAD_FAST                'view'
              110  CALL_FUNCTION_1       1  ''
              112  COMPARE_OP               <
              114  POP_JUMP_IF_FALSE   140  'to 140'

 L. 262       116  LOAD_FAST                'offset'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _sslobj
              122  LOAD_METHOD              write
              124  LOAD_FAST                'view'
              126  LOAD_FAST                'offset'
              128  LOAD_CONST               None
              130  BUILD_SLICE_2         2 
              132  BINARY_SUBSCR    
              134  CALL_METHOD_1         1  ''
              136  INPLACE_ADD      
              138  STORE_FAST               'offset'
            140_0  COME_FROM           114  '114'
              140  POP_BLOCK        
              142  JUMP_FORWARD        248  'to 248'
            144_0  COME_FROM_FINALLY   102  '102'

 L. 263       144  DUP_TOP          
              146  LOAD_GLOBAL              ssl
              148  LOAD_ATTR                SSLError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   246  'to 246'
              154  POP_TOP          
              156  STORE_FAST               'exc'
              158  POP_TOP          
              160  SETUP_FINALLY       234  'to 234'

 L. 267       162  LOAD_GLOBAL              getattr
              164  LOAD_FAST                'exc'
              166  LOAD_STR                 'errno'
              168  LOAD_CONST               None
              170  CALL_FUNCTION_3       3  ''
              172  STORE_FAST               'exc_errno'

 L. 268       174  LOAD_FAST                'exc'
              176  LOAD_ATTR                reason
              178  LOAD_STR                 'PROTOCOL_IS_SHUTDOWN'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   196  'to 196'

 L. 269       184  LOAD_GLOBAL              ssl
              186  LOAD_ATTR                SSL_ERROR_WANT_READ
              188  DUP_TOP          
              190  STORE_FAST               'exc_errno'
              192  LOAD_FAST                'exc'
              194  STORE_ATTR               errno
            196_0  COME_FROM           182  '182'

 L. 270       196  LOAD_FAST                'exc_errno'
              198  LOAD_GLOBAL              ssl
              200  LOAD_ATTR                SSL_ERROR_WANT_READ

 L. 271       202  LOAD_GLOBAL              ssl
              204  LOAD_ATTR                SSL_ERROR_WANT_WRITE

 L. 272       206  LOAD_GLOBAL              ssl
              208  LOAD_ATTR                SSL_ERROR_SYSCALL

 L. 270       210  BUILD_TUPLE_3         3 
              212  COMPARE_OP               not-in
              214  POP_JUMP_IF_FALSE   218  'to 218'

 L. 273       216  RAISE_VARARGS_0       0  'reraise'
            218_0  COME_FROM           214  '214'

 L. 274       218  LOAD_FAST                'exc_errno'
              220  LOAD_GLOBAL              ssl
              222  LOAD_ATTR                SSL_ERROR_WANT_READ
              224  COMPARE_OP               ==
              226  LOAD_FAST                'self'
              228  STORE_ATTR               _need_ssldata
              230  POP_BLOCK        
              232  BEGIN_FINALLY    
            234_0  COME_FROM_FINALLY   160  '160'
              234  LOAD_CONST               None
              236  STORE_FAST               'exc'
              238  DELETE_FAST              'exc'
              240  END_FINALLY      
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
            246_0  COME_FROM           152  '152'
              246  END_FINALLY      
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           142  '142'

 L. 277       248  LOAD_FAST                'self'
              250  LOAD_ATTR                _outgoing
              252  LOAD_ATTR                pending
          254_256  POP_JUMP_IF_FALSE   274  'to 274'

 L. 278       258  LOAD_FAST                'ssldata'
              260  LOAD_METHOD              append
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                _outgoing
              266  LOAD_METHOD              read
              268  CALL_METHOD_0         0  ''
              270  CALL_METHOD_1         1  ''
              272  POP_TOP          
            274_0  COME_FROM           254  '254'

 L. 279       274  LOAD_FAST                'offset'
              276  LOAD_GLOBAL              len
              278  LOAD_FAST                'view'
              280  CALL_FUNCTION_1       1  ''
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_TRUE    300  'to 300'
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                _need_ssldata
              292  POP_JUMP_IF_FALSE_BACK    96  'to 96'

 L. 280   294_296  JUMP_FORWARD        300  'to 300'
              298  JUMP_BACK            96  'to 96'
            300_0  COME_FROM           294  '294'
            300_1  COME_FROM           284  '284'

 L. 281       300  LOAD_FAST                'ssldata'
              302  LOAD_FAST                'offset'
              304  BUILD_TUPLE_2         2 
              306  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 298


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

        def __del__(self, _warn=warnings.warn):
            if not self._closed:
                _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
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
            if not data:
                return
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
            elif ssl_handshake_timeout <= 0:
                raise ValueError(f"ssl_handshake_timeout should be a positive number, got {ssl_handshake_timeout}")
            if not sslcontext:
                sslcontext = _create_transport_context(server_side, server_hostname)
            self._server_side = server_side
            if server_hostname and not server_side:
                self._server_hostname = server_hostname
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
            elif self._app_transport is not None:
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

        def data_received--- This code section failed: ---

 L. 524         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _sslpipe
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 526        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 528        14  SETUP_FINALLY        36  'to 36'

 L. 529        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _sslpipe
               20  LOAD_METHOD              feed_ssldata
               22  LOAD_FAST                'data'
               24  CALL_METHOD_1         1  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'ssldata'
               30  STORE_FAST               'appdata'
               32  POP_BLOCK        
               34  JUMP_FORWARD        112  'to 112'
             36_0  COME_FROM_FINALLY    14  '14'

 L. 530        36  DUP_TOP          
               38  LOAD_GLOBAL              SystemExit
               40  LOAD_GLOBAL              KeyboardInterrupt
               42  BUILD_TUPLE_2         2 
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    60  'to 60'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 531        54  RAISE_VARARGS_0       0  'reraise'
               56  POP_EXCEPT       
               58  JUMP_FORWARD        112  'to 112'
             60_0  COME_FROM            46  '46'

 L. 532        60  DUP_TOP          
               62  LOAD_GLOBAL              BaseException
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE   110  'to 110'
               68  POP_TOP          
               70  STORE_FAST               'e'
               72  POP_TOP          
               74  SETUP_FINALLY        98  'to 98'

 L. 533        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _fatal_error
               80  LOAD_FAST                'e'
               82  LOAD_STR                 'SSL error in data received'
               84  CALL_METHOD_2         2  ''
               86  POP_TOP          

 L. 534        88  POP_BLOCK        
               90  POP_EXCEPT       
               92  CALL_FINALLY         98  'to 98'
               94  LOAD_CONST               None
               96  RETURN_VALUE     
             98_0  COME_FROM            92  '92'
             98_1  COME_FROM_FINALLY    74  '74'
               98  LOAD_CONST               None
              100  STORE_FAST               'e'
              102  DELETE_FAST              'e'
              104  END_FINALLY      
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM            66  '66'
              110  END_FINALLY      
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            58  '58'
            112_2  COME_FROM            34  '34'

 L. 536       112  LOAD_FAST                'ssldata'
              114  GET_ITER         
            116_0  COME_FROM           132  '132'
              116  FOR_ITER            134  'to 134'
              118  STORE_FAST               'chunk'

 L. 537       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _transport
              124  LOAD_METHOD              write
              126  LOAD_FAST                'chunk'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
              132  JUMP_BACK           116  'to 116'
            134_0  COME_FROM           116  '116'

 L. 539       134  LOAD_FAST                'appdata'
              136  GET_ITER         
            138_0  COME_FROM           284  '284'
            138_1  COME_FROM           268  '268'
              138  FOR_ITER            286  'to 286'
              140  STORE_FAST               'chunk'

 L. 540       142  LOAD_FAST                'chunk'
          144_146  POP_JUMP_IF_FALSE   270  'to 270'

 L. 541       148  SETUP_FINALLY       188  'to 188'

 L. 542       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _app_protocol_is_buffer
              154  POP_JUMP_IF_FALSE   172  'to 172'

 L. 543       156  LOAD_GLOBAL              protocols
              158  LOAD_METHOD              _feed_data_to_buffered_proto

 L. 544       160  LOAD_FAST                'self'
              162  LOAD_ATTR                _app_protocol

 L. 544       164  LOAD_FAST                'chunk'

 L. 543       166  CALL_METHOD_2         2  ''
              168  POP_TOP          
              170  JUMP_FORWARD        184  'to 184'
            172_0  COME_FROM           154  '154'

 L. 546       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _app_protocol
              176  LOAD_METHOD              data_received
              178  LOAD_FAST                'chunk'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
            184_0  COME_FROM           170  '170'
              184  POP_BLOCK        
              186  JUMP_FORWARD        268  'to 268'
            188_0  COME_FROM_FINALLY   148  '148'

 L. 547       188  DUP_TOP          
              190  LOAD_GLOBAL              SystemExit
              192  LOAD_GLOBAL              KeyboardInterrupt
              194  BUILD_TUPLE_2         2 
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   212  'to 212'
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L. 548       206  RAISE_VARARGS_0       0  'reraise'
              208  POP_EXCEPT       
              210  JUMP_FORWARD        268  'to 268'
            212_0  COME_FROM           198  '198'

 L. 549       212  DUP_TOP          
              214  LOAD_GLOBAL              BaseException
              216  COMPARE_OP               exception-match
          218_220  POP_JUMP_IF_FALSE   266  'to 266'
              222  POP_TOP          
              224  STORE_FAST               'ex'
              226  POP_TOP          
              228  SETUP_FINALLY       254  'to 254'

 L. 550       230  LOAD_FAST                'self'
              232  LOAD_METHOD              _fatal_error

 L. 551       234  LOAD_FAST                'ex'

 L. 551       236  LOAD_STR                 'application protocol failed to receive SSL data'

 L. 550       238  CALL_METHOD_2         2  ''
              240  POP_TOP          

 L. 552       242  POP_BLOCK        
              244  POP_EXCEPT       
              246  CALL_FINALLY        254  'to 254'
              248  POP_TOP          
              250  LOAD_CONST               None
              252  RETURN_VALUE     
            254_0  COME_FROM           246  '246'
            254_1  COME_FROM_FINALLY   228  '228'
              254  LOAD_CONST               None
              256  STORE_FAST               'ex'
              258  DELETE_FAST              'ex'
              260  END_FINALLY      
              262  POP_EXCEPT       
              264  JUMP_FORWARD        268  'to 268'
            266_0  COME_FROM           218  '218'
              266  END_FINALLY      
            268_0  COME_FROM           264  '264'
            268_1  COME_FROM           210  '210'
            268_2  COME_FROM           186  '186'
              268  JUMP_BACK           138  'to 138'
            270_0  COME_FROM           144  '144'

 L. 554       270  LOAD_FAST                'self'
              272  LOAD_METHOD              _start_shutdown
              274  CALL_METHOD_0         0  ''
              276  POP_TOP          

 L. 555       278  POP_TOP          
          280_282  BREAK_LOOP          286  'to 286'
              284  JUMP_BACK           138  'to 138'
            286_0  COME_FROM           280  '280'
            286_1  COME_FROM           138  '138'

Parse error at or near `CALL_FINALLY' instruction at offset 92

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

        def _on_handshake_complete--- This code section failed: ---

 L. 626         0  LOAD_CONST               False
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _in_handshake

 L. 627         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _handshake_timeout_handle
               10  LOAD_METHOD              cancel
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 629        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _sslpipe
               20  LOAD_ATTR                ssl_object
               22  STORE_FAST               'sslobj'

 L. 630        24  SETUP_FINALLY        50  'to 50'

 L. 631        26  LOAD_FAST                'handshake_exc'
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 632        34  LOAD_FAST                'handshake_exc'
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            32  '32'

 L. 634        38  LOAD_FAST                'sslobj'
               40  LOAD_METHOD              getpeercert
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'peercert'
               46  POP_BLOCK        
               48  JUMP_FORWARD        148  'to 148'
             50_0  COME_FROM_FINALLY    24  '24'

 L. 635        50  DUP_TOP          
               52  LOAD_GLOBAL              SystemExit
               54  LOAD_GLOBAL              KeyboardInterrupt
               56  BUILD_TUPLE_2         2 
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    74  'to 74'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 636        68  RAISE_VARARGS_0       0  'reraise'
               70  POP_EXCEPT       
               72  JUMP_FORWARD        148  'to 148'
             74_0  COME_FROM            60  '60'

 L. 637        74  DUP_TOP          
               76  LOAD_GLOBAL              BaseException
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   146  'to 146'
               82  POP_TOP          
               84  STORE_FAST               'exc'
               86  POP_TOP          
               88  SETUP_FINALLY       134  'to 134'

 L. 638        90  LOAD_GLOBAL              isinstance
               92  LOAD_FAST                'exc'
               94  LOAD_GLOBAL              ssl
               96  LOAD_ATTR                CertificateError
               98  CALL_FUNCTION_2       2  ''
              100  POP_JUMP_IF_FALSE   108  'to 108'

 L. 639       102  LOAD_STR                 'SSL handshake failed on verifying the certificate'
              104  STORE_FAST               'msg'
              106  JUMP_FORWARD        112  'to 112'
            108_0  COME_FROM           100  '100'

 L. 641       108  LOAD_STR                 'SSL handshake failed'
              110  STORE_FAST               'msg'
            112_0  COME_FROM           106  '106'

 L. 642       112  LOAD_FAST                'self'
              114  LOAD_METHOD              _fatal_error
              116  LOAD_FAST                'exc'
              118  LOAD_FAST                'msg'
              120  CALL_METHOD_2         2  ''
              122  POP_TOP          

 L. 643       124  POP_BLOCK        
              126  POP_EXCEPT       
              128  CALL_FINALLY        134  'to 134'
              130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           128  '128'
            134_1  COME_FROM_FINALLY    88  '88'
              134  LOAD_CONST               None
              136  STORE_FAST               'exc'
              138  DELETE_FAST              'exc'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM            80  '80'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            72  '72'
            148_2  COME_FROM            48  '48'

 L. 645       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _loop
              152  LOAD_METHOD              get_debug
              154  CALL_METHOD_0         0  ''
              156  POP_JUMP_IF_FALSE   192  'to 192'

 L. 646       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _loop
              162  LOAD_METHOD              time
              164  CALL_METHOD_0         0  ''
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _handshake_start_time
              170  BINARY_SUBTRACT  
              172  STORE_FAST               'dt'

 L. 647       174  LOAD_GLOBAL              logger
              176  LOAD_METHOD              debug
              178  LOAD_STR                 '%r: SSL handshake took %.1f ms'
              180  LOAD_FAST                'self'
              182  LOAD_FAST                'dt'
              184  LOAD_CONST               1000.0
              186  BINARY_MULTIPLY  
              188  CALL_METHOD_3         3  ''
              190  POP_TOP          
            192_0  COME_FROM           156  '156'

 L. 650       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _extra
              196  LOAD_ATTR                update
              198  LOAD_FAST                'peercert'

 L. 651       200  LOAD_FAST                'sslobj'
              202  LOAD_METHOD              cipher
              204  CALL_METHOD_0         0  ''

 L. 652       206  LOAD_FAST                'sslobj'
              208  LOAD_METHOD              compression
              210  CALL_METHOD_0         0  ''

 L. 653       212  LOAD_FAST                'sslobj'

 L. 650       214  LOAD_CONST               ('peercert', 'cipher', 'compression', 'ssl_object')
              216  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              218  POP_TOP          

 L. 655       220  LOAD_FAST                'self'
              222  LOAD_ATTR                _call_connection_made
              224  POP_JUMP_IF_FALSE   240  'to 240'

 L. 656       226  LOAD_FAST                'self'
              228  LOAD_ATTR                _app_protocol
              230  LOAD_METHOD              connection_made
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                _app_transport
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
            240_0  COME_FROM           224  '224'

 L. 657       240  LOAD_FAST                'self'
              242  LOAD_METHOD              _wakeup_waiter
              244  CALL_METHOD_0         0  ''
              246  POP_TOP          

 L. 658       248  LOAD_CONST               True
              250  LOAD_FAST                'self'
              252  STORE_ATTR               _session_established

 L. 664       254  LOAD_FAST                'self'
              256  LOAD_ATTR                _loop
              258  LOAD_METHOD              call_soon
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                _process_write_backlog
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 128

        def _process_write_backlog--- This code section failed: ---

 L. 668         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _transport
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_TRUE     20  'to 20'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sslpipe
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    24  'to 24'
             20_0  COME_FROM             8  '8'

 L. 669        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 671        24  SETUP_FINALLY       238  'to 238'

 L. 672        26  LOAD_GLOBAL              range
               28  LOAD_GLOBAL              len
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _write_backlog
               34  CALL_FUNCTION_1       1  ''
               36  CALL_FUNCTION_1       1  ''
               38  GET_ITER         
             40_0  COME_FROM           232  '232'
               40  FOR_ITER            234  'to 234'
               42  STORE_FAST               'i'

 L. 673        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _write_backlog
               48  LOAD_CONST               0
               50  BINARY_SUBSCR    
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'data'
               56  STORE_FAST               'offset'

 L. 674        58  LOAD_FAST                'data'
               60  POP_JUMP_IF_FALSE    82  'to 82'

 L. 675        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _sslpipe
               66  LOAD_METHOD              feed_appdata
               68  LOAD_FAST                'data'
               70  LOAD_FAST                'offset'
               72  CALL_METHOD_2         2  ''
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'ssldata'
               78  STORE_FAST               'offset'
               80  JUMP_FORWARD        124  'to 124'
             82_0  COME_FROM            60  '60'

 L. 676        82  LOAD_FAST                'offset'
               84  POP_JUMP_IF_FALSE   106  'to 106'

 L. 677        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _sslpipe
               90  LOAD_METHOD              do_handshake

 L. 678        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _on_handshake_complete

 L. 677        96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'ssldata'

 L. 679       100  LOAD_CONST               1
              102  STORE_FAST               'offset'
              104  JUMP_FORWARD        124  'to 124'
            106_0  COME_FROM            84  '84'

 L. 681       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _sslpipe
              110  LOAD_METHOD              shutdown
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _finalize
              116  CALL_METHOD_1         1  ''
              118  STORE_FAST               'ssldata'

 L. 682       120  LOAD_CONST               1
              122  STORE_FAST               'offset'
            124_0  COME_FROM           104  '104'
            124_1  COME_FROM            80  '80'

 L. 684       124  LOAD_FAST                'ssldata'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            146  'to 146'
              130  STORE_FAST               'chunk'

 L. 685       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _transport
              136  LOAD_METHOD              write
              138  LOAD_FAST                'chunk'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_BACK           128  'to 128'
            146_0  COME_FROM           128  '128'

 L. 687       146  LOAD_FAST                'offset'
              148  LOAD_GLOBAL              len
              150  LOAD_FAST                'data'
              152  CALL_FUNCTION_1       1  ''
              154  COMPARE_OP               <
              156  POP_JUMP_IF_FALSE   206  'to 206'

 L. 688       158  LOAD_FAST                'data'
              160  LOAD_FAST                'offset'
              162  BUILD_TUPLE_2         2 
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                _write_backlog
              168  LOAD_CONST               0
              170  STORE_SUBSCR     

 L. 691       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _sslpipe
              176  LOAD_ATTR                need_ssldata
              178  POP_JUMP_IF_TRUE    184  'to 184'
              180  LOAD_ASSERT              AssertionError
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           178  '178'

 L. 692       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _transport
              188  LOAD_ATTR                _paused
              190  POP_JUMP_IF_FALSE   202  'to 202'

 L. 693       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _transport
              196  LOAD_METHOD              resume_reading
              198  CALL_METHOD_0         0  ''
              200  POP_TOP          
            202_0  COME_FROM           190  '190'

 L. 694       202  POP_TOP          
              204  BREAK_LOOP          234  'to 234'
            206_0  COME_FROM           156  '156'

 L. 698       206  LOAD_FAST                'self'
              208  LOAD_ATTR                _write_backlog
              210  LOAD_CONST               0
              212  DELETE_SUBSCR    

 L. 699       214  LOAD_FAST                'self'
              216  DUP_TOP          
              218  LOAD_ATTR                _write_buffer_size
              220  LOAD_GLOBAL              len
              222  LOAD_FAST                'data'
              224  CALL_FUNCTION_1       1  ''
              226  INPLACE_SUBTRACT 
              228  ROT_TWO          
              230  STORE_ATTR               _write_buffer_size
              232  JUMP_BACK            40  'to 40'
            234_0  COME_FROM           204  '204'
            234_1  COME_FROM            40  '40'
              234  POP_BLOCK        
              236  JUMP_FORWARD        332  'to 332'
            238_0  COME_FROM_FINALLY    24  '24'

 L. 700       238  DUP_TOP          
              240  LOAD_GLOBAL              SystemExit
              242  LOAD_GLOBAL              KeyboardInterrupt
              244  BUILD_TUPLE_2         2 
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   264  'to 264'
              252  POP_TOP          
              254  POP_TOP          
              256  POP_TOP          

 L. 701       258  RAISE_VARARGS_0       0  'reraise'
              260  POP_EXCEPT       
              262  JUMP_FORWARD        332  'to 332'
            264_0  COME_FROM           248  '248'

 L. 702       264  DUP_TOP          
              266  LOAD_GLOBAL              BaseException
              268  COMPARE_OP               exception-match
          270_272  POP_JUMP_IF_FALSE   330  'to 330'
              274  POP_TOP          
              276  STORE_FAST               'exc'
              278  POP_TOP          
              280  SETUP_FINALLY       318  'to 318'

 L. 703       282  LOAD_FAST                'self'
              284  LOAD_ATTR                _in_handshake
          286_288  POP_JUMP_IF_FALSE   302  'to 302'

 L. 705       290  LOAD_FAST                'self'
              292  LOAD_METHOD              _on_handshake_complete
              294  LOAD_FAST                'exc'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
              300  JUMP_FORWARD        314  'to 314'
            302_0  COME_FROM           286  '286'

 L. 707       302  LOAD_FAST                'self'
              304  LOAD_METHOD              _fatal_error
              306  LOAD_FAST                'exc'
              308  LOAD_STR                 'Fatal error on SSL transport'
              310  CALL_METHOD_2         2  ''
              312  POP_TOP          
            314_0  COME_FROM           300  '300'
              314  POP_BLOCK        
              316  BEGIN_FINALLY    
            318_0  COME_FROM_FINALLY   280  '280'
              318  LOAD_CONST               None
              320  STORE_FAST               'exc'
              322  DELETE_FAST              'exc'
              324  END_FINALLY      
              326  POP_EXCEPT       
              328  JUMP_FORWARD        332  'to 332'
            330_0  COME_FROM           270  '270'
              330  END_FINALLY      
            332_0  COME_FROM           328  '328'
            332_1  COME_FROM           262  '262'
            332_2  COME_FROM           236  '236'

Parse error at or near `POP_TOP' instruction at offset 254

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