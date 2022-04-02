# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\proactor_events.py
"""Event loop using a proactor and related classes.

A proactor is a "notify-on-completion" multiplexer.  Currently a
proactor is only implemented on Windows with IOCP.
"""
__all__ = ('BaseProactorEventLoop', )
import io, os, socket, warnings, signal, threading, collections
from . import base_events
from . import constants
from . import futures
from . import exceptions
from . import protocols
from . import sslproto
from . import transports
from . import trsock
from .log import logger

def _set_socket_extra(transport, sock):
    transport._extra['socket'] = trsock.TransportSocket(sock)
    try:
        transport._extra['sockname'] = sock.getsockname()
    except socket.error:
        if transport._loop.get_debug():
            logger.warning('getsockname() failed on %r',
              sock, exc_info=True)
    else:
        if 'peername' not in transport._extra:
            try:
                transport._extra['peername'] = sock.getpeername()
            except socket.error:
                transport._extra['peername'] = None


class _ProactorBasePipeTransport(transports._FlowControlMixin, transports.BaseTransport):
    __doc__ = 'Base class for pipe and socket transports.'

    def __init__(self, loop, sock, protocol, waiter=None, extra=None, server=None):
        super().__init__(extra, loop)
        self._set_extra(sock)
        self._sock = sock
        self.set_protocol(protocol)
        self._server = server
        self._buffer = None
        self._read_fut = None
        self._write_fut = None
        self._pending_write = 0
        self._conn_lost = 0
        self._closing = False
        self._eof_written = False
        if self._server is not None:
            self._server._attach()
        self._loop.call_soon(self._protocol.connection_made, self)
        if waiter is not None:
            self._loop.call_soon(futures._set_result_unless_cancelled, waiter, None)

    def __repr__(self):
        info = [self.__class__.__name__]
        if self._sock is None:
            info.append('closed')
        else:
            if self._closing:
                info.append('closing')
        if self._sock is not None:
            info.append(f"fd={self._sock.fileno()}")
        if self._read_fut is not None:
            info.append(f"read={self._read_fut!r}")
        if self._write_fut is not None:
            info.append(f"write={self._write_fut!r}")
        if self._buffer:
            info.append(f"write_bufsize={len(self._buffer)}")
        if self._eof_written:
            info.append('EOF written')
        return '<{}>'.format(' '.join(info))

    def _set_extra(self, sock):
        self._extra['pipe'] = sock

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def is_closing(self):
        return self._closing

    def close(self):
        if self._closing:
            return
        self._closing = True
        self._conn_lost += 1
        if not self._buffer:
            if self._write_fut is None:
                self._loop.call_soon(self._call_connection_lost, None)
        if self._read_fut is not None:
            self._read_fut.cancel()
            self._read_fut = None

    def __del__(self, _warn=warnings.warn):
        if self._sock is not None:
            _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
            self.close()

    def _fatal_error(self, exc, message='Fatal error on pipe transport'):
        try:
            if isinstance(exc, OSError):
                if self._loop.get_debug():
                    logger.debug('%r: %s', self, message, exc_info=True)
            else:
                self._loop.call_exception_handler({'message':message, 
                 'exception':exc, 
                 'transport':self, 
                 'protocol':self._protocol})
        finally:
            self._force_close(exc)

    def _force_close(self, exc):
        if self._empty_waiter is not None:
            if not self._empty_waiter.done():
                if exc is None:
                    self._empty_waiter.set_result(None)
                else:
                    self._empty_waiter.set_exception(exc)
        if self._closing:
            return
        self._closing = True
        self._conn_lost += 1
        if self._write_fut:
            self._write_fut.cancel()
            self._write_fut = None
        if self._read_fut:
            self._read_fut.cancel()
            self._read_fut = None
        self._pending_write = 0
        self._buffer = None
        self._loop.call_soon(self._call_connection_lost, exc)

    def _call_connection_lost(self, exc):
        try:
            self._protocol.connection_lost(exc)
        finally:
            if hasattr(self._sock, 'shutdown'):
                self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()
            self._sock = None
            server = self._server
            if server is not None:
                server._detach()
                self._server = None

    def get_write_buffer_size(self):
        size = self._pending_write
        if self._buffer is not None:
            size += len(self._buffer)
        return size


class _ProactorReadPipeTransport(_ProactorBasePipeTransport, transports.ReadTransport):
    __doc__ = 'Transport for read pipes.'

    def __init__(self, loop, sock, protocol, waiter=None, extra=None, server=None):
        self._pending_data = None
        self._paused = True
        super().__init__(loop, sock, protocol, waiter, extra, server)
        self._loop.call_soon(self._loop_reading)
        self._paused = False

    def is_reading(self):
        return not self._paused and not self._closing

    def pause_reading(self):
        if self._closing or self._paused:
            return
        self._paused = True
        if self._loop.get_debug():
            logger.debug('%r pauses reading', self)

    def resume_reading(self):
        return self._closing or self._paused or None
        self._paused = False
        if self._read_fut is None:
            self._loop.call_soon(self._loop_reading, None)
        data = self._pending_data
        self._pending_data = None
        if data is not None:
            self._loop.call_soon(self._data_received, data)
        if self._loop.get_debug():
            logger.debug('%r resumes reading', self)

    def _eof_received--- This code section failed: ---

 L. 231         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loop
                4  LOAD_METHOD              get_debug
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 232        10  LOAD_GLOBAL              logger
               12  LOAD_METHOD              debug
               14  LOAD_STR                 '%r received EOF'
               16  LOAD_FAST                'self'
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          
             22_0  COME_FROM             8  '8'

 L. 234        22  SETUP_FINALLY        38  'to 38'

 L. 235        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _protocol
               28  LOAD_METHOD              eof_received
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'keep_open'
               34  POP_BLOCK        
               36  JUMP_FORWARD        114  'to 114'
             38_0  COME_FROM_FINALLY    22  '22'

 L. 236        38  DUP_TOP          
               40  LOAD_GLOBAL              SystemExit
               42  LOAD_GLOBAL              KeyboardInterrupt
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 237        56  RAISE_VARARGS_0       0  'reraise'
               58  POP_EXCEPT       
               60  JUMP_FORWARD        114  'to 114'
             62_0  COME_FROM            48  '48'

 L. 238        62  DUP_TOP          
               64  LOAD_GLOBAL              BaseException
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE   112  'to 112'
               70  POP_TOP          
               72  STORE_FAST               'exc'
               74  POP_TOP          
               76  SETUP_FINALLY       100  'to 100'

 L. 239        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _fatal_error

 L. 240        82  LOAD_FAST                'exc'

 L. 240        84  LOAD_STR                 'Fatal error: protocol.eof_received() call failed.'

 L. 239        86  CALL_METHOD_2         2  ''
               88  POP_TOP          

 L. 241        90  POP_BLOCK        
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

 L. 243       114  LOAD_FAST                'keep_open'
              116  POP_JUMP_IF_TRUE    126  'to 126'

 L. 244       118  LOAD_FAST                'self'
              120  LOAD_METHOD              close
              122  CALL_METHOD_0         0  ''
              124  POP_TOP          
            126_0  COME_FROM           116  '116'

Parse error at or near `CALL_FINALLY' instruction at offset 94

    def _data_received--- This code section failed: ---

 L. 247         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _paused
                4  POP_JUMP_IF_FALSE    30  'to 30'

 L. 250         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _pending_data
               10  LOAD_CONST               None
               12  COMPARE_OP               is
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  LOAD_ASSERT              AssertionError
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 251        20  LOAD_FAST                'data'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _pending_data

 L. 252        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM             4  '4'

 L. 254        30  LOAD_FAST                'data'
               32  POP_JUMP_IF_TRUE     46  'to 46'

 L. 255        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _eof_received
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 256        42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            32  '32'

 L. 258        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _protocol
               52  LOAD_GLOBAL              protocols
               54  LOAD_ATTR                BufferedProtocol
               56  CALL_FUNCTION_2       2  ''
               58  POP_JUMP_IF_FALSE   158  'to 158'

 L. 259        60  SETUP_FINALLY        80  'to 80'

 L. 260        62  LOAD_GLOBAL              protocols
               64  LOAD_METHOD              _feed_data_to_buffered_proto
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _protocol
               70  LOAD_FAST                'data'
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          
               76  POP_BLOCK        
               78  JUMP_ABSOLUTE       170  'to 170'
             80_0  COME_FROM_FINALLY    60  '60'

 L. 261        80  DUP_TOP          
               82  LOAD_GLOBAL              SystemExit
               84  LOAD_GLOBAL              KeyboardInterrupt
               86  BUILD_TUPLE_2         2 
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   104  'to 104'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 262        98  RAISE_VARARGS_0       0  'reraise'
              100  POP_EXCEPT       
              102  JUMP_ABSOLUTE       170  'to 170'
            104_0  COME_FROM            90  '90'

 L. 263       104  DUP_TOP          
              106  LOAD_GLOBAL              BaseException
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   154  'to 154'
              112  POP_TOP          
              114  STORE_FAST               'exc'
              116  POP_TOP          
              118  SETUP_FINALLY       142  'to 142'

 L. 264       120  LOAD_FAST                'self'
              122  LOAD_METHOD              _fatal_error
              124  LOAD_FAST                'exc'

 L. 265       126  LOAD_STR                 'Fatal error: protocol.buffer_updated() call failed.'

 L. 264       128  CALL_METHOD_2         2  ''
              130  POP_TOP          

 L. 267       132  POP_BLOCK        
              134  POP_EXCEPT       
              136  CALL_FINALLY        142  'to 142'
              138  LOAD_CONST               None
              140  RETURN_VALUE     
            142_0  COME_FROM           136  '136'
            142_1  COME_FROM_FINALLY   118  '118'
              142  LOAD_CONST               None
              144  STORE_FAST               'exc'
              146  DELETE_FAST              'exc'
              148  END_FINALLY      
              150  POP_EXCEPT       
              152  JUMP_ABSOLUTE       170  'to 170'
            154_0  COME_FROM           110  '110'
              154  END_FINALLY      
              156  JUMP_FORWARD        170  'to 170'
            158_0  COME_FROM            58  '58'

 L. 269       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _protocol
              162  LOAD_METHOD              data_received
              164  LOAD_FAST                'data'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
            170_0  COME_FROM_EXCEPT_CLAUSE   156  '156'
            170_1  COME_FROM_EXCEPT_CLAUSE   102  '102'

Parse error at or near `CALL_FINALLY' instruction at offset 136

    def _loop_reading--- This code section failed: ---

 L. 272         0  LOAD_CONST               None
                2  STORE_FAST               'data'

 L. 273       4_6  SETUP_FINALLY       378  'to 378'
                8  SETUP_FINALLY       152  'to 152'

 L. 274        10  LOAD_FAST                'fut'
               12  LOAD_CONST               None
               14  COMPARE_OP               is-not
               16  POP_JUMP_IF_FALSE    80  'to 80'

 L. 275        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _read_fut
               22  LOAD_FAST                'fut'
               24  COMPARE_OP               is
               26  POP_JUMP_IF_TRUE     48  'to 48'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _read_fut
               32  LOAD_CONST               None
               34  COMPARE_OP               is
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 276        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _closing

 L. 275        42  POP_JUMP_IF_TRUE     48  'to 48'
             44_0  COME_FROM            36  '36'
               44  LOAD_ASSERT              AssertionError
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'
             48_1  COME_FROM            26  '26'

 L. 277        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _read_fut

 L. 278        54  LOAD_FAST                'fut'
               56  LOAD_METHOD              done
               58  CALL_METHOD_0         0  ''
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L. 280        62  LOAD_FAST                'fut'
               64  LOAD_METHOD              result
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'data'
               70  JUMP_FORWARD         80  'to 80'
             72_0  COME_FROM            60  '60'

 L. 283        72  LOAD_FAST                'fut'
               74  LOAD_METHOD              cancel
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          
             80_0  COME_FROM            70  '70'
             80_1  COME_FROM            16  '16'

 L. 285        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _closing
               84  POP_JUMP_IF_FALSE   102  'to 102'

 L. 287        86  LOAD_CONST               None
               88  STORE_FAST               'data'

 L. 288        90  POP_BLOCK        
               92  POP_BLOCK        
            94_96  CALL_FINALLY        378  'to 378'
               98  LOAD_CONST               None
              100  RETURN_VALUE     
            102_0  COME_FROM            84  '84'

 L. 290       102  LOAD_FAST                'data'
              104  LOAD_CONST               b''
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   122  'to 122'

 L. 292       110  POP_BLOCK        
              112  POP_BLOCK        
          114_116  CALL_FINALLY        378  'to 378'
              118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM           108  '108'

 L. 297       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _paused
              126  POP_JUMP_IF_TRUE    148  'to 148'

 L. 299       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _loop
              132  LOAD_ATTR                _proactor
              134  LOAD_METHOD              recv
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _sock
              140  LOAD_CONST               32768
              142  CALL_METHOD_2         2  ''
              144  LOAD_FAST                'self'
              146  STORE_ATTR               _read_fut
            148_0  COME_FROM           126  '126'
              148  POP_BLOCK        
              150  JUMP_FORWARD        352  'to 352'
            152_0  COME_FROM_FINALLY     8  '8'

 L. 300       152  DUP_TOP          
              154  LOAD_GLOBAL              ConnectionAbortedError
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   228  'to 228'
              160  POP_TOP          
              162  STORE_FAST               'exc'
              164  POP_TOP          
              166  SETUP_FINALLY       216  'to 216'

 L. 301       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _closing
              172  POP_JUMP_IF_TRUE    188  'to 188'

 L. 302       174  LOAD_FAST                'self'
              176  LOAD_METHOD              _fatal_error
              178  LOAD_FAST                'exc'
              180  LOAD_STR                 'Fatal read error on pipe transport'
              182  CALL_METHOD_2         2  ''
              184  POP_TOP          
              186  JUMP_FORWARD        212  'to 212'
            188_0  COME_FROM           172  '172'

 L. 303       188  LOAD_FAST                'self'
              190  LOAD_ATTR                _loop
              192  LOAD_METHOD              get_debug
              194  CALL_METHOD_0         0  ''
              196  POP_JUMP_IF_FALSE   212  'to 212'

 L. 304       198  LOAD_GLOBAL              logger
              200  LOAD_ATTR                debug
              202  LOAD_STR                 'Read error on pipe transport while closing'

 L. 305       204  LOAD_CONST               True

 L. 304       206  LOAD_CONST               ('exc_info',)
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  POP_TOP          
            212_0  COME_FROM           196  '196'
            212_1  COME_FROM           186  '186'
              212  POP_BLOCK        
              214  BEGIN_FINALLY    
            216_0  COME_FROM_FINALLY   166  '166'
              216  LOAD_CONST               None
              218  STORE_FAST               'exc'
              220  DELETE_FAST              'exc'
              222  END_FINALLY      
              224  POP_EXCEPT       
              226  JUMP_FORWARD        374  'to 374'
            228_0  COME_FROM           158  '158'

 L. 306       228  DUP_TOP          
              230  LOAD_GLOBAL              ConnectionResetError
              232  COMPARE_OP               exception-match
          234_236  POP_JUMP_IF_FALSE   272  'to 272'
              238  POP_TOP          
              240  STORE_FAST               'exc'
              242  POP_TOP          
              244  SETUP_FINALLY       260  'to 260'

 L. 307       246  LOAD_FAST                'self'
              248  LOAD_METHOD              _force_close
              250  LOAD_FAST                'exc'
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          
              256  POP_BLOCK        
              258  BEGIN_FINALLY    
            260_0  COME_FROM_FINALLY   244  '244'
              260  LOAD_CONST               None
              262  STORE_FAST               'exc'
              264  DELETE_FAST              'exc'
              266  END_FINALLY      
              268  POP_EXCEPT       
              270  JUMP_FORWARD        374  'to 374'
            272_0  COME_FROM           234  '234'

 L. 308       272  DUP_TOP          
              274  LOAD_GLOBAL              OSError
              276  COMPARE_OP               exception-match
          278_280  POP_JUMP_IF_FALSE   318  'to 318'
              282  POP_TOP          
              284  STORE_FAST               'exc'
              286  POP_TOP          
              288  SETUP_FINALLY       306  'to 306'

 L. 309       290  LOAD_FAST                'self'
              292  LOAD_METHOD              _fatal_error
              294  LOAD_FAST                'exc'
              296  LOAD_STR                 'Fatal read error on pipe transport'
              298  CALL_METHOD_2         2  ''
              300  POP_TOP          
              302  POP_BLOCK        
              304  BEGIN_FINALLY    
            306_0  COME_FROM_FINALLY   288  '288'
              306  LOAD_CONST               None
              308  STORE_FAST               'exc'
              310  DELETE_FAST              'exc'
              312  END_FINALLY      
              314  POP_EXCEPT       
              316  JUMP_FORWARD        374  'to 374'
            318_0  COME_FROM           278  '278'

 L. 310       318  DUP_TOP          
              320  LOAD_GLOBAL              exceptions
              322  LOAD_ATTR                CancelledError
              324  COMPARE_OP               exception-match
          326_328  POP_JUMP_IF_FALSE   350  'to 350'
              330  POP_TOP          
              332  POP_TOP          
              334  POP_TOP          

 L. 311       336  LOAD_FAST                'self'
              338  LOAD_ATTR                _closing
          340_342  POP_JUMP_IF_TRUE    346  'to 346'

 L. 312       344  RAISE_VARARGS_0       0  'reraise'
            346_0  COME_FROM           340  '340'
              346  POP_EXCEPT       
              348  JUMP_FORWARD        374  'to 374'
            350_0  COME_FROM           326  '326'
              350  END_FINALLY      
            352_0  COME_FROM           150  '150'

 L. 314       352  LOAD_FAST                'self'
              354  LOAD_ATTR                _paused
          356_358  POP_JUMP_IF_TRUE    374  'to 374'

 L. 315       360  LOAD_FAST                'self'
              362  LOAD_ATTR                _read_fut
              364  LOAD_METHOD              add_done_callback
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                _loop_reading
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          
            374_0  COME_FROM           356  '356'
            374_1  COME_FROM           348  '348'
            374_2  COME_FROM           316  '316'
            374_3  COME_FROM           270  '270'
            374_4  COME_FROM           226  '226'
              374  POP_BLOCK        
              376  BEGIN_FINALLY    
            378_0  COME_FROM           114  '114'
            378_1  COME_FROM            94  '94'
            378_2  COME_FROM_FINALLY     4  '4'

 L. 317       378  LOAD_FAST                'data'
              380  LOAD_CONST               None
              382  COMPARE_OP               is-not
          384_386  POP_JUMP_IF_FALSE   398  'to 398'

 L. 318       388  LOAD_FAST                'self'
              390  LOAD_METHOD              _data_received
              392  LOAD_FAST                'data'
              394  CALL_METHOD_1         1  ''
              396  POP_TOP          
            398_0  COME_FROM           384  '384'
              398  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 92


class _ProactorBaseWritePipeTransport(_ProactorBasePipeTransport, transports.WriteTransport):
    __doc__ = 'Transport for write pipes.'
    _start_tls_compatible = True

    def __init__(self, *args, **kw):
        (super().__init__)(*args, **kw)
        self._empty_waiter = None

    def write(self, data):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError(f"data argument must be a bytes-like object, not {type(data).__name__}")
        elif self._eof_written:
            raise RuntimeError('write_eof() already called')
        else:
            if self._empty_waiter is not None:
                raise RuntimeError('unable to write; sendfile is in progress')
            elif not data:
                return
                if self._conn_lost:
                    if self._conn_lost >= constants.LOG_THRESHOLD_FOR_CONNLOST_WRITES:
                        logger.warning('socket.send() raised exception.')
                    self._conn_lost += 1
                    return
                    if self._write_fut is None:
                        assert self._buffer is None
                        self._loop_writing(data=(bytes(data)))
                else:
                    self._buffer = self._buffer or bytearray(data)
                    self._maybe_pause_protocol()
            else:
                pass
            self._buffer.extend(data)
            self._maybe_pause_protocol()

    def _loop_writing--- This code section failed: ---

 L. 370       0_2  SETUP_FINALLY       280  'to 280'

 L. 371         4  LOAD_FAST                'f'
                6  LOAD_CONST               None
                8  COMPARE_OP               is-not
               10  POP_JUMP_IF_FALSE    34  'to 34'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _write_fut
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _closing
               26  POP_JUMP_IF_FALSE    34  'to 34'

 L. 374        28  POP_BLOCK        
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            26  '26'
             34_1  COME_FROM            20  '20'
             34_2  COME_FROM            10  '10'

 L. 375        34  LOAD_FAST                'f'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _write_fut
               40  COMPARE_OP               is
               42  POP_JUMP_IF_TRUE     48  'to 48'
               44  LOAD_ASSERT              AssertionError
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'

 L. 376        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _write_fut

 L. 377        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _pending_write

 L. 378        60  LOAD_FAST                'f'
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 379        64  LOAD_FAST                'f'
               66  LOAD_METHOD              result
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          
             72_0  COME_FROM            62  '62'

 L. 380        72  LOAD_FAST                'data'
               74  LOAD_CONST               None
               76  COMPARE_OP               is
               78  POP_JUMP_IF_FALSE    92  'to 92'

 L. 381        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _buffer
               84  STORE_FAST               'data'

 L. 382        86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _buffer
             92_0  COME_FROM            78  '78'

 L. 383        92  LOAD_FAST                'data'
               94  POP_JUMP_IF_TRUE    148  'to 148'

 L. 384        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _closing
              100  POP_JUMP_IF_FALSE   118  'to 118'

 L. 385       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _loop
              106  LOAD_METHOD              call_soon
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _call_connection_lost
              112  LOAD_CONST               None
              114  CALL_METHOD_2         2  ''
              116  POP_TOP          
            118_0  COME_FROM           100  '100'

 L. 386       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _eof_written
              122  POP_JUMP_IF_FALSE   138  'to 138'

 L. 387       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _sock
              128  LOAD_METHOD              shutdown
              130  LOAD_GLOBAL              socket
              132  LOAD_ATTR                SHUT_WR
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           122  '122'

 L. 393       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _maybe_resume_protocol
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          
              146  JUMP_FORWARD        240  'to 240'
            148_0  COME_FROM            94  '94'

 L. 395       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _loop
              152  LOAD_ATTR                _proactor
              154  LOAD_METHOD              send
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _sock
              160  LOAD_FAST                'data'
              162  CALL_METHOD_2         2  ''
              164  LOAD_FAST                'self'
              166  STORE_ATTR               _write_fut

 L. 396       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _write_fut
              172  LOAD_METHOD              done
              174  CALL_METHOD_0         0  ''
              176  POP_JUMP_IF_TRUE    226  'to 226'

 L. 397       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _pending_write
              182  LOAD_CONST               0
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_TRUE    192  'to 192'
              188  LOAD_ASSERT              AssertionError
              190  RAISE_VARARGS_1       1  'exception instance'
            192_0  COME_FROM           186  '186'

 L. 398       192  LOAD_GLOBAL              len
              194  LOAD_FAST                'data'
              196  CALL_FUNCTION_1       1  ''
              198  LOAD_FAST                'self'
              200  STORE_ATTR               _pending_write

 L. 399       202  LOAD_FAST                'self'
              204  LOAD_ATTR                _write_fut
              206  LOAD_METHOD              add_done_callback
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                _loop_writing
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 400       216  LOAD_FAST                'self'
              218  LOAD_METHOD              _maybe_pause_protocol
              220  CALL_METHOD_0         0  ''
              222  POP_TOP          
              224  JUMP_FORWARD        240  'to 240'
            226_0  COME_FROM           176  '176'

 L. 402       226  LOAD_FAST                'self'
              228  LOAD_ATTR                _write_fut
              230  LOAD_METHOD              add_done_callback
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                _loop_writing
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
            240_0  COME_FROM           224  '224'
            240_1  COME_FROM           146  '146'

 L. 403       240  LOAD_FAST                'self'
              242  LOAD_ATTR                _empty_waiter
              244  LOAD_CONST               None
              246  COMPARE_OP               is-not
          248_250  POP_JUMP_IF_FALSE   276  'to 276'
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                _write_fut
              256  LOAD_CONST               None
              258  COMPARE_OP               is
          260_262  POP_JUMP_IF_FALSE   276  'to 276'

 L. 404       264  LOAD_FAST                'self'
              266  LOAD_ATTR                _empty_waiter
              268  LOAD_METHOD              set_result
              270  LOAD_CONST               None
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
            276_0  COME_FROM           260  '260'
            276_1  COME_FROM           248  '248'
              276  POP_BLOCK        
              278  JUMP_FORWARD        372  'to 372'
            280_0  COME_FROM_FINALLY     0  '0'

 L. 405       280  DUP_TOP          
              282  LOAD_GLOBAL              ConnectionResetError
              284  COMPARE_OP               exception-match
          286_288  POP_JUMP_IF_FALSE   324  'to 324'
              290  POP_TOP          
              292  STORE_FAST               'exc'
              294  POP_TOP          
              296  SETUP_FINALLY       312  'to 312'

 L. 406       298  LOAD_FAST                'self'
              300  LOAD_METHOD              _force_close
              302  LOAD_FAST                'exc'
              304  CALL_METHOD_1         1  ''
              306  POP_TOP          
              308  POP_BLOCK        
              310  BEGIN_FINALLY    
            312_0  COME_FROM_FINALLY   296  '296'
              312  LOAD_CONST               None
              314  STORE_FAST               'exc'
              316  DELETE_FAST              'exc'
              318  END_FINALLY      
              320  POP_EXCEPT       
              322  JUMP_FORWARD        372  'to 372'
            324_0  COME_FROM           286  '286'

 L. 407       324  DUP_TOP          
              326  LOAD_GLOBAL              OSError
              328  COMPARE_OP               exception-match
          330_332  POP_JUMP_IF_FALSE   370  'to 370'
              334  POP_TOP          
              336  STORE_FAST               'exc'
              338  POP_TOP          
              340  SETUP_FINALLY       358  'to 358'

 L. 408       342  LOAD_FAST                'self'
              344  LOAD_METHOD              _fatal_error
              346  LOAD_FAST                'exc'
              348  LOAD_STR                 'Fatal write error on pipe transport'
              350  CALL_METHOD_2         2  ''
              352  POP_TOP          
              354  POP_BLOCK        
              356  BEGIN_FINALLY    
            358_0  COME_FROM_FINALLY   340  '340'
              358  LOAD_CONST               None
              360  STORE_FAST               'exc'
              362  DELETE_FAST              'exc'
              364  END_FINALLY      
              366  POP_EXCEPT       
              368  JUMP_FORWARD        372  'to 372'
            370_0  COME_FROM           330  '330'
              370  END_FINALLY      
            372_0  COME_FROM           368  '368'
            372_1  COME_FROM           322  '322'
            372_2  COME_FROM           278  '278'

Parse error at or near `LOAD_CONST' instruction at offset 30

    def can_write_eof(self):
        return True

    def write_eof(self):
        self.close()

    def abort(self):
        self._force_close(None)

    def _make_empty_waiter(self):
        if self._empty_waiter is not None:
            raise RuntimeError('Empty waiter is already set')
        self._empty_waiter = self._loop.create_future()
        if self._write_fut is None:
            self._empty_waiter.set_result(None)
        return self._empty_waiter

    def _reset_empty_waiter(self):
        self._empty_waiter = None


class _ProactorWritePipeTransport(_ProactorBaseWritePipeTransport):

    def __init__(self, *args, **kw):
        (super().__init__)(*args, **kw)
        self._read_fut = self._loop._proactor.recv(self._sock, 16)
        self._read_fut.add_done_callback(self._pipe_closed)

    def _pipe_closed(self, fut):
        if fut.cancelled():
            return
        else:
            assert fut.result() == b''
            if self._closing:
                assert self._read_fut is None
                return
                assert fut is self._read_fut, (fut, self._read_fut)
                self._read_fut = None
                if self._write_fut is not None:
                    self._force_close(BrokenPipeError())
            else:
                self.close()


class _ProactorDatagramTransport(_ProactorBasePipeTransport):
    max_size = 262144

    def __init__(self, loop, sock, protocol, address=None, waiter=None, extra=None):
        self._address = address
        self._empty_waiter = None
        super().__init__(loop, sock, protocol, waiter=waiter, extra=extra)
        self._buffer = collections.deque()
        self._loop.call_soon(self._loop_reading)

    def _set_extra(self, sock):
        _set_socket_extra(self, sock)

    def get_write_buffer_size(self):
        return sum((len(data) for data, _ in self._buffer))

    def abort(self):
        self._force_close(None)

    def sendto(self, data, addr=None):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data argument must be bytes-like object (%r)', type(data))
        else:
            if not data:
                return
            if self._address is not None:
                if addr not in (None, self._address):
                    raise ValueError(f"Invalid address: must be None or {self._address}")
            if self._conn_lost and self._address:
                if self._conn_lost >= constants.LOG_THRESHOLD_FOR_CONNLOST_WRITES:
                    logger.warning('socket.sendto() raised exception.')
                self._conn_lost += 1
                return
        self._buffer.append((bytes(data), addr))
        if self._write_fut is None:
            self._loop_writing()
        self._maybe_pause_protocol()

    def _loop_writing--- This code section failed: ---

 L. 505         0  SETUP_FINALLY       166  'to 166'

 L. 506         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _conn_lost
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 507         8  POP_BLOCK        
               10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             6  '6'

 L. 509        14  LOAD_FAST                'fut'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _write_fut
               20  COMPARE_OP               is
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  LOAD_ASSERT              AssertionError
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 510        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _write_fut

 L. 511        34  LOAD_FAST                'fut'
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 513        38  LOAD_FAST                'fut'
               40  LOAD_METHOD              result
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          
             46_0  COME_FROM            36  '36'

 L. 515        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _buffer
               50  POP_JUMP_IF_FALSE    64  'to 64'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _conn_lost
               56  POP_JUMP_IF_FALSE    92  'to 92'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _address
               62  POP_JUMP_IF_FALSE    92  'to 92'
             64_0  COME_FROM            50  '50'

 L. 517        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _closing
               68  POP_JUMP_IF_FALSE    86  'to 86'

 L. 518        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _loop
               74  LOAD_METHOD              call_soon
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _call_connection_lost
               80  LOAD_CONST               None
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          
             86_0  COME_FROM            68  '68'

 L. 519        86  POP_BLOCK        
               88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            62  '62'
             92_1  COME_FROM            56  '56'

 L. 521        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _buffer
               96  LOAD_METHOD              popleft
               98  CALL_METHOD_0         0  ''
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'data'
              104  STORE_FAST               'addr'

 L. 522       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _address
              110  LOAD_CONST               None
              112  COMPARE_OP               is-not
              114  POP_JUMP_IF_FALSE   138  'to 138'

 L. 523       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _loop
              120  LOAD_ATTR                _proactor
              122  LOAD_METHOD              send
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _sock

 L. 524       128  LOAD_FAST                'data'

 L. 523       130  CALL_METHOD_2         2  ''
              132  LOAD_FAST                'self'
              134  STORE_ATTR               _write_fut
              136  JUMP_FORWARD        162  'to 162'
            138_0  COME_FROM           114  '114'

 L. 526       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _loop
              142  LOAD_ATTR                _proactor
              144  LOAD_ATTR                sendto
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                _sock

 L. 527       150  LOAD_FAST                'data'

 L. 528       152  LOAD_FAST                'addr'

 L. 526       154  LOAD_CONST               ('addr',)
              156  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              158  LOAD_FAST                'self'
              160  STORE_ATTR               _write_fut
            162_0  COME_FROM           136  '136'
              162  POP_BLOCK        
              164  JUMP_FORWARD        256  'to 256'
            166_0  COME_FROM_FINALLY     0  '0'

 L. 529       166  DUP_TOP          
              168  LOAD_GLOBAL              OSError
              170  COMPARE_OP               exception-match
              172  POP_JUMP_IF_FALSE   210  'to 210'
              174  POP_TOP          
              176  STORE_FAST               'exc'
              178  POP_TOP          
              180  SETUP_FINALLY       198  'to 198'

 L. 530       182  LOAD_FAST                'self'
              184  LOAD_ATTR                _protocol
              186  LOAD_METHOD              error_received
              188  LOAD_FAST                'exc'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
              194  POP_BLOCK        
              196  BEGIN_FINALLY    
            198_0  COME_FROM_FINALLY   180  '180'
              198  LOAD_CONST               None
              200  STORE_FAST               'exc'
              202  DELETE_FAST              'exc'
              204  END_FINALLY      
              206  POP_EXCEPT       
              208  JUMP_FORWARD        278  'to 278'
            210_0  COME_FROM           172  '172'

 L. 531       210  DUP_TOP          
              212  LOAD_GLOBAL              Exception
              214  COMPARE_OP               exception-match
              216  POP_JUMP_IF_FALSE   254  'to 254'
              218  POP_TOP          
              220  STORE_FAST               'exc'
              222  POP_TOP          
              224  SETUP_FINALLY       242  'to 242'

 L. 532       226  LOAD_FAST                'self'
              228  LOAD_METHOD              _fatal_error
              230  LOAD_FAST                'exc'
              232  LOAD_STR                 'Fatal write error on datagram transport'
              234  CALL_METHOD_2         2  ''
              236  POP_TOP          
              238  POP_BLOCK        
              240  BEGIN_FINALLY    
            242_0  COME_FROM_FINALLY   224  '224'
              242  LOAD_CONST               None
              244  STORE_FAST               'exc'
              246  DELETE_FAST              'exc'
              248  END_FINALLY      
              250  POP_EXCEPT       
              252  JUMP_FORWARD        278  'to 278'
            254_0  COME_FROM           216  '216'
              254  END_FINALLY      
            256_0  COME_FROM           164  '164'

 L. 534       256  LOAD_FAST                'self'
              258  LOAD_ATTR                _write_fut
              260  LOAD_METHOD              add_done_callback
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                _loop_writing
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          

 L. 535       270  LOAD_FAST                'self'
              272  LOAD_METHOD              _maybe_resume_protocol
              274  CALL_METHOD_0         0  ''
              276  POP_TOP          
            278_0  COME_FROM           252  '252'
            278_1  COME_FROM           208  '208'

Parse error at or near `LOAD_CONST' instruction at offset 10

    def _loop_reading--- This code section failed: ---

 L. 538         0  LOAD_CONST               None
                2  STORE_FAST               'data'

 L. 539       4_6  SETUP_FINALLY       316  'to 316'
                8  SETUP_FINALLY       208  'to 208'

 L. 540        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _conn_lost
               14  POP_JUMP_IF_FALSE    28  'to 28'

 L. 541        16  POP_BLOCK        
               18  POP_BLOCK        
            20_22  CALL_FINALLY        316  'to 316'
               24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            14  '14'

 L. 543        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _read_fut
               32  LOAD_FAST                'fut'
               34  COMPARE_OP               is
               36  POP_JUMP_IF_TRUE     58  'to 58'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _read_fut
               42  LOAD_CONST               None
               44  COMPARE_OP               is
               46  POP_JUMP_IF_FALSE    54  'to 54'

 L. 544        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _closing

 L. 543        52  POP_JUMP_IF_TRUE     58  'to 58'
             54_0  COME_FROM            46  '46'
               54  LOAD_ASSERT              AssertionError
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            52  '52'
             58_1  COME_FROM            36  '36'

 L. 546        58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _read_fut

 L. 547        64  LOAD_FAST                'fut'
               66  LOAD_CONST               None
               68  COMPARE_OP               is-not
               70  POP_JUMP_IF_FALSE   132  'to 132'

 L. 548        72  LOAD_FAST                'fut'
               74  LOAD_METHOD              result
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'res'

 L. 550        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _closing
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L. 552        86  LOAD_CONST               None
               88  STORE_FAST               'data'

 L. 553        90  POP_BLOCK        
               92  POP_BLOCK        
               94  CALL_FINALLY        316  'to 316'
               96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM            84  '84'

 L. 555       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _address
              104  LOAD_CONST               None
              106  COMPARE_OP               is-not
              108  POP_JUMP_IF_FALSE   124  'to 124'

 L. 556       110  LOAD_FAST                'res'
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _address
              116  ROT_TWO          
              118  STORE_FAST               'data'
              120  STORE_FAST               'addr'
              122  JUMP_FORWARD        132  'to 132'
            124_0  COME_FROM           108  '108'

 L. 558       124  LOAD_FAST                'res'
              126  UNPACK_SEQUENCE_2     2 
              128  STORE_FAST               'data'
              130  STORE_FAST               'addr'
            132_0  COME_FROM           122  '122'
            132_1  COME_FROM            70  '70'

 L. 560       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _conn_lost
              136  POP_JUMP_IF_FALSE   148  'to 148'

 L. 561       138  POP_BLOCK        
              140  POP_BLOCK        
              142  CALL_FINALLY        316  'to 316'
              144  LOAD_CONST               None
              146  RETURN_VALUE     
            148_0  COME_FROM           136  '136'

 L. 562       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _address
              152  LOAD_CONST               None
              154  COMPARE_OP               is-not
              156  POP_JUMP_IF_FALSE   182  'to 182'

 L. 563       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _loop
              162  LOAD_ATTR                _proactor
              164  LOAD_METHOD              recv
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _sock

 L. 564       170  LOAD_FAST                'self'
              172  LOAD_ATTR                max_size

 L. 563       174  CALL_METHOD_2         2  ''
              176  LOAD_FAST                'self'
              178  STORE_ATTR               _read_fut
              180  JUMP_FORWARD        204  'to 204'
            182_0  COME_FROM           156  '156'

 L. 566       182  LOAD_FAST                'self'
              184  LOAD_ATTR                _loop
              186  LOAD_ATTR                _proactor
              188  LOAD_METHOD              recvfrom
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                _sock

 L. 567       194  LOAD_FAST                'self'
              196  LOAD_ATTR                max_size

 L. 566       198  CALL_METHOD_2         2  ''
              200  LOAD_FAST                'self'
              202  STORE_ATTR               _read_fut
            204_0  COME_FROM           180  '180'
              204  POP_BLOCK        
              206  JUMP_FORWARD        286  'to 286'
            208_0  COME_FROM_FINALLY     8  '8'

 L. 568       208  DUP_TOP          
              210  LOAD_GLOBAL              OSError
              212  COMPARE_OP               exception-match
              214  POP_JUMP_IF_FALSE   252  'to 252'
              216  POP_TOP          
              218  STORE_FAST               'exc'
              220  POP_TOP          
              222  SETUP_FINALLY       240  'to 240'

 L. 569       224  LOAD_FAST                'self'
              226  LOAD_ATTR                _protocol
              228  LOAD_METHOD              error_received
              230  LOAD_FAST                'exc'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          
              236  POP_BLOCK        
              238  BEGIN_FINALLY    
            240_0  COME_FROM_FINALLY   222  '222'
              240  LOAD_CONST               None
              242  STORE_FAST               'exc'
              244  DELETE_FAST              'exc'
              246  END_FINALLY      
              248  POP_EXCEPT       
              250  JUMP_FORWARD        312  'to 312'
            252_0  COME_FROM           214  '214'

 L. 570       252  DUP_TOP          
              254  LOAD_GLOBAL              exceptions
              256  LOAD_ATTR                CancelledError
              258  COMPARE_OP               exception-match
          260_262  POP_JUMP_IF_FALSE   284  'to 284'
              264  POP_TOP          
              266  POP_TOP          
              268  POP_TOP          

 L. 571       270  LOAD_FAST                'self'
              272  LOAD_ATTR                _closing
          274_276  POP_JUMP_IF_TRUE    280  'to 280'

 L. 572       278  RAISE_VARARGS_0       0  'reraise'
            280_0  COME_FROM           274  '274'
              280  POP_EXCEPT       
              282  JUMP_FORWARD        312  'to 312'
            284_0  COME_FROM           260  '260'
              284  END_FINALLY      
            286_0  COME_FROM           206  '206'

 L. 574       286  LOAD_FAST                'self'
              288  LOAD_ATTR                _read_fut
              290  LOAD_CONST               None
              292  COMPARE_OP               is-not
          294_296  POP_JUMP_IF_FALSE   312  'to 312'

 L. 575       298  LOAD_FAST                'self'
              300  LOAD_ATTR                _read_fut
              302  LOAD_METHOD              add_done_callback
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                _loop_reading
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          
            312_0  COME_FROM           294  '294'
            312_1  COME_FROM           282  '282'
            312_2  COME_FROM           250  '250'
              312  POP_BLOCK        
              314  BEGIN_FINALLY    
            316_0  COME_FROM           142  '142'
            316_1  COME_FROM            94  '94'
            316_2  COME_FROM            20  '20'
            316_3  COME_FROM_FINALLY     4  '4'

 L. 577       316  LOAD_FAST                'data'
          318_320  POP_JUMP_IF_FALSE   336  'to 336'

 L. 578       322  LOAD_FAST                'self'
              324  LOAD_ATTR                _protocol
              326  LOAD_METHOD              datagram_received
              328  LOAD_FAST                'data'
              330  LOAD_FAST                'addr'
              332  CALL_METHOD_2         2  ''
              334  POP_TOP          
            336_0  COME_FROM           318  '318'
              336  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 18


class _ProactorDuplexPipeTransport(_ProactorReadPipeTransport, _ProactorBaseWritePipeTransport, transports.Transport):
    __doc__ = 'Transport for duplex pipes.'

    def can_write_eof(self):
        return False

    def write_eof(self):
        raise NotImplementedError


class _ProactorSocketTransport(_ProactorReadPipeTransport, _ProactorBaseWritePipeTransport, transports.Transport):
    __doc__ = 'Transport for connected sockets.'
    _sendfile_compatible = constants._SendfileMode.TRY_NATIVE

    def __init__(self, loop, sock, protocol, waiter=None, extra=None, server=None):
        super().__init__(loop, sock, protocol, waiter, extra, server)
        base_events._set_nodelay(sock)

    def _set_extra(self, sock):
        _set_socket_extra(self, sock)

    def can_write_eof(self):
        return True

    def write_eof(self):
        if self._closing or self._eof_written:
            return
        self._eof_written = True
        if self._write_fut is None:
            self._sock.shutdown(socket.SHUT_WR)


class BaseProactorEventLoop(base_events.BaseEventLoop):

    def __init__(self, proactor):
        super().__init__()
        logger.debug('Using proactor: %s', proactor.__class__.__name__)
        self._proactor = proactor
        self._selector = proactor
        self._self_reading_future = None
        self._accept_futures = {}
        proactor.set_loop(self)
        self._make_self_pipe()
        if threading.current_thread() is threading.main_thread():
            signal.set_wakeup_fd(self._csock.fileno())

    def _make_socket_transport(self, sock, protocol, waiter=None, extra=None, server=None):
        return _ProactorSocketTransport(self, sock, protocol, waiter, extra, server)

    def _make_ssl_transport(self, rawsock, protocol, sslcontext, waiter=None, *, server_side=False, server_hostname=None, extra=None, server=None, ssl_handshake_timeout=None):
        ssl_protocol = sslproto.SSLProtocol(self,
          protocol, sslcontext, waiter, server_side,
          server_hostname, ssl_handshake_timeout=ssl_handshake_timeout)
        _ProactorSocketTransport(self, rawsock, ssl_protocol, extra=extra,
          server=server)
        return ssl_protocol._app_transport

    def _make_datagram_transport(self, sock, protocol, address=None, waiter=None, extra=None):
        return _ProactorDatagramTransport(self, sock, protocol, address, waiter, extra)

    def _make_duplex_pipe_transport(self, sock, protocol, waiter=None, extra=None):
        return _ProactorDuplexPipeTransport(self, sock, protocol, waiter, extra)

    def _make_read_pipe_transport(self, sock, protocol, waiter=None, extra=None):
        return _ProactorReadPipeTransport(self, sock, protocol, waiter, extra)

    def _make_write_pipe_transport(self, sock, protocol, waiter=None, extra=None):
        return _ProactorWritePipeTransport(self, sock, protocol, waiter, extra)

    def close(self):
        if self.is_running():
            raise RuntimeError('Cannot close a running event loop')
        if self.is_closed():
            return
        if threading.current_thread() is threading.main_thread():
            signal.set_wakeup_fd(-1)
        self._stop_accept_futures()
        self._close_self_pipe()
        self._proactor.close()
        self._proactor = None
        self._selector = None
        super().close()

    async def sock_recv(self, sock, n):
        return await self._proactor.recv(sock, n)

    async def sock_recv_into(self, sock, buf):
        return await self._proactor.recv_into(sock, buf)

    async def sock_sendall(self, sock, data):
        return await self._proactor.send(sock, data)

    async def sock_connect(self, sock, address):
        return await self._proactor.connect(sock, address)

    async def sock_accept(self, sock):
        return await self._proactor.accept(sock)

    async def _sock_sendfile_native--- This code section failed: ---

 L. 708         0  SETUP_FINALLY        14  'to 14'

 L. 709         2  LOAD_FAST                'file'
                4  LOAD_METHOD              fileno
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'fileno'
               10  POP_BLOCK        
               12  JUMP_FORWARD         64  'to 64'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 710        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  LOAD_GLOBAL              io
               20  LOAD_ATTR                UnsupportedOperation
               22  BUILD_TUPLE_2         2 
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    62  'to 62'
               28  POP_TOP          
               30  STORE_FAST               'err'
               32  POP_TOP          
               34  SETUP_FINALLY        50  'to 50'

 L. 711        36  LOAD_GLOBAL              exceptions
               38  LOAD_METHOD              SendfileNotAvailableError
               40  LOAD_STR                 'not a regular file'
               42  CALL_METHOD_1         1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_BLOCK        
               48  BEGIN_FINALLY    
             50_0  COME_FROM_FINALLY    34  '34'
               50  LOAD_CONST               None
               52  STORE_FAST               'err'
               54  DELETE_FAST              'err'
               56  END_FINALLY      
               58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            26  '26'
               62  END_FINALLY      
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            12  '12'

 L. 712        64  SETUP_FINALLY        82  'to 82'

 L. 713        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              fstat
               70  LOAD_FAST                'fileno'
               72  CALL_METHOD_1         1  ''
               74  LOAD_ATTR                st_size
               76  STORE_FAST               'fsize'
               78  POP_BLOCK        
               80  JUMP_FORWARD        126  'to 126'
             82_0  COME_FROM_FINALLY    64  '64'

 L. 714        82  DUP_TOP          
               84  LOAD_GLOBAL              OSError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   124  'to 124'
               90  POP_TOP          
               92  STORE_FAST               'err'
               94  POP_TOP          
               96  SETUP_FINALLY       112  'to 112'

 L. 715        98  LOAD_GLOBAL              exceptions
              100  LOAD_METHOD              SendfileNotAvailableError
              102  LOAD_STR                 'not a regular file'
              104  CALL_METHOD_1         1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
              108  POP_BLOCK        
              110  BEGIN_FINALLY    
            112_0  COME_FROM_FINALLY    96  '96'
              112  LOAD_CONST               None
              114  STORE_FAST               'err'
              116  DELETE_FAST              'err'
              118  END_FINALLY      
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM            88  '88'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM            80  '80'

 L. 716       126  LOAD_FAST                'count'
              128  POP_JUMP_IF_FALSE   134  'to 134'
              130  LOAD_FAST                'count'
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM           128  '128'
              134  LOAD_FAST                'fsize'
            136_0  COME_FROM           132  '132'
              136  STORE_FAST               'blocksize'

 L. 717       138  LOAD_FAST                'blocksize'
              140  POP_JUMP_IF_TRUE    146  'to 146'

 L. 718       142  LOAD_CONST               0
              144  RETURN_VALUE     
            146_0  COME_FROM           140  '140'

 L. 720       146  LOAD_GLOBAL              min
              148  LOAD_FAST                'blocksize'
              150  LOAD_CONST               4294967295
              152  CALL_FUNCTION_2       2  ''
              154  STORE_FAST               'blocksize'

 L. 721       156  LOAD_FAST                'count'
              158  POP_JUMP_IF_FALSE   174  'to 174'
              160  LOAD_GLOBAL              min
              162  LOAD_FAST                'offset'
              164  LOAD_FAST                'count'
              166  BINARY_ADD       
              168  LOAD_FAST                'fsize'
              170  CALL_FUNCTION_2       2  ''
              172  JUMP_FORWARD        176  'to 176'
            174_0  COME_FROM           158  '158'
              174  LOAD_FAST                'fsize'
            176_0  COME_FROM           172  '172'
              176  STORE_FAST               'end_pos'

 L. 722       178  LOAD_GLOBAL              min
              180  LOAD_FAST                'offset'
              182  LOAD_FAST                'fsize'
              184  CALL_FUNCTION_2       2  ''
              186  STORE_FAST               'offset'

 L. 723       188  LOAD_CONST               0
              190  STORE_FAST               'total_sent'

 L. 724       192  SETUP_FINALLY       270  'to 270'

 L. 726       194  LOAD_GLOBAL              min
              196  LOAD_FAST                'end_pos'
              198  LOAD_FAST                'offset'
              200  BINARY_SUBTRACT  
              202  LOAD_FAST                'blocksize'
              204  CALL_FUNCTION_2       2  ''
              206  STORE_FAST               'blocksize'

 L. 727       208  LOAD_FAST                'blocksize'
              210  LOAD_CONST               0
              212  COMPARE_OP               <=
              214  POP_JUMP_IF_FALSE   224  'to 224'

 L. 728       216  LOAD_FAST                'total_sent'
              218  POP_BLOCK        
              220  CALL_FINALLY        270  'to 270'
              222  RETURN_VALUE     
            224_0  COME_FROM           214  '214'

 L. 729       224  LOAD_FAST                'self'
              226  LOAD_ATTR                _proactor
              228  LOAD_METHOD              sendfile
              230  LOAD_FAST                'sock'
              232  LOAD_FAST                'file'
              234  LOAD_FAST                'offset'
              236  LOAD_FAST                'blocksize'
              238  CALL_METHOD_4         4  ''
              240  GET_AWAITABLE    
              242  LOAD_CONST               None
              244  YIELD_FROM       
              246  POP_TOP          

 L. 730       248  LOAD_FAST                'offset'
              250  LOAD_FAST                'blocksize'
              252  INPLACE_ADD      
              254  STORE_FAST               'offset'

 L. 731       256  LOAD_FAST                'total_sent'
              258  LOAD_FAST                'blocksize'
              260  INPLACE_ADD      
              262  STORE_FAST               'total_sent'
              264  JUMP_BACK           194  'to 194'
              266  POP_BLOCK        
              268  BEGIN_FINALLY    
            270_0  COME_FROM           220  '220'
            270_1  COME_FROM_FINALLY   192  '192'

 L. 733       270  LOAD_FAST                'total_sent'
              272  LOAD_CONST               0
              274  COMPARE_OP               >
          276_278  POP_JUMP_IF_FALSE   290  'to 290'

 L. 734       280  LOAD_FAST                'file'
              282  LOAD_METHOD              seek
              284  LOAD_FAST                'offset'
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          
            290_0  COME_FROM           276  '276'
              290  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 220

    async def _sendfile_native(self, transp, file, offset, count):
        resume_reading = transp.is_reading()
        transp.pause_reading()
        await transp._make_empty_waiter()
        try:
            return await self.sock_sendfile((transp._sock), file, offset, count, fallback=False)
        finally:
            transp._reset_empty_waiter()
            if resume_reading:
                transp.resume_reading()

    def _close_self_pipe(self):
        if self._self_reading_future is not None:
            self._self_reading_future.cancel()
            self._self_reading_future = None
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

    def _loop_self_reading(self, f=None):
        try:
            if f is not None:
                f.result()
            f = self._proactor.recv(self._ssock, 4096)
        except exceptions.CancelledError:
            return
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as exc:
            try:
                self.call_exception_handler({'message':'Error on reading from the event loop self pipe', 
                 'exception':exc, 
                 'loop':self})
            finally:
                exc = None
                del exc

        else:
            self._self_reading_future = f
            f.add_done_callback(self._loop_self_reading)

    def _write_to_self(self):
        try:
            self._csock.send(b'\x00')
        except OSError:
            if self._debug:
                logger.debug('Fail to write a null byte into the self-pipe socket', exc_info=True)

    def _start_serving(self, protocol_factory, sock, sslcontext=None, server=None, backlog=100, ssl_handshake_timeout=None):

        def loop--- This code section failed: ---

 L. 799         0  SETUP_FINALLY       140  'to 140'

 L. 800         2  LOAD_FAST                'f'
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE   110  'to 110'

 L. 801        10  LOAD_FAST                'f'
               12  LOAD_METHOD              result
               14  CALL_METHOD_0         0  ''
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'conn'
               20  STORE_FAST               'addr'

 L. 802        22  LOAD_DEREF               'self'
               24  LOAD_ATTR                _debug
               26  POP_JUMP_IF_FALSE    44  'to 44'

 L. 803        28  LOAD_GLOBAL              logger
               30  LOAD_METHOD              debug
               32  LOAD_STR                 '%r got a new connection from %r: %r'

 L. 804        34  LOAD_DEREF               'server'

 L. 804        36  LOAD_FAST                'addr'

 L. 804        38  LOAD_FAST                'conn'

 L. 803        40  CALL_METHOD_4         4  ''
               42  POP_TOP          
             44_0  COME_FROM            26  '26'

 L. 805        44  LOAD_DEREF               'protocol_factory'
               46  CALL_FUNCTION_0       0  ''
               48  STORE_FAST               'protocol'

 L. 806        50  LOAD_DEREF               'sslcontext'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
               56  POP_JUMP_IF_FALSE    88  'to 88'

 L. 807        58  LOAD_DEREF               'self'
               60  LOAD_ATTR                _make_ssl_transport

 L. 808        62  LOAD_FAST                'conn'

 L. 808        64  LOAD_FAST                'protocol'

 L. 808        66  LOAD_DEREF               'sslcontext'

 L. 808        68  LOAD_CONST               True

 L. 809        70  LOAD_STR                 'peername'
               72  LOAD_FAST                'addr'
               74  BUILD_MAP_1           1 

 L. 809        76  LOAD_DEREF               'server'

 L. 810        78  LOAD_DEREF               'ssl_handshake_timeout'

 L. 807        80  LOAD_CONST               ('server_side', 'extra', 'server', 'ssl_handshake_timeout')
               82  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
               84  POP_TOP          
               86  JUMP_FORWARD        110  'to 110'
             88_0  COME_FROM            56  '56'

 L. 812        88  LOAD_DEREF               'self'
               90  LOAD_ATTR                _make_socket_transport

 L. 813        92  LOAD_FAST                'conn'

 L. 813        94  LOAD_FAST                'protocol'

 L. 814        96  LOAD_STR                 'peername'
               98  LOAD_FAST                'addr'
              100  BUILD_MAP_1           1 

 L. 814       102  LOAD_DEREF               'server'

 L. 812       104  LOAD_CONST               ('extra', 'server')
              106  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              108  POP_TOP          
            110_0  COME_FROM            86  '86'
            110_1  COME_FROM             8  '8'

 L. 815       110  LOAD_DEREF               'self'
              112  LOAD_METHOD              is_closed
              114  CALL_METHOD_0         0  ''
              116  POP_JUMP_IF_FALSE   124  'to 124'

 L. 816       118  POP_BLOCK        
              120  LOAD_CONST               None
              122  RETURN_VALUE     
            124_0  COME_FROM           116  '116'

 L. 817       124  LOAD_DEREF               'self'
              126  LOAD_ATTR                _proactor
              128  LOAD_METHOD              accept
              130  LOAD_DEREF               'sock'
              132  CALL_METHOD_1         1  ''
              134  STORE_FAST               'f'
              136  POP_BLOCK        
              138  JUMP_FORWARD        272  'to 272'
            140_0  COME_FROM_FINALLY     0  '0'

 L. 818       140  DUP_TOP          
              142  LOAD_GLOBAL              OSError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   240  'to 240'
              148  POP_TOP          
              150  STORE_FAST               'exc'
              152  POP_TOP          
              154  SETUP_FINALLY       228  'to 228'

 L. 819       156  LOAD_DEREF               'sock'
              158  LOAD_METHOD              fileno
              160  CALL_METHOD_0         0  ''
              162  LOAD_CONST               -1
              164  COMPARE_OP               !=
              166  POP_JUMP_IF_FALSE   202  'to 202'

 L. 820       168  LOAD_DEREF               'self'
              170  LOAD_METHOD              call_exception_handler

 L. 821       172  LOAD_STR                 'Accept failed on a socket'

 L. 822       174  LOAD_FAST                'exc'

 L. 823       176  LOAD_GLOBAL              trsock
              178  LOAD_METHOD              TransportSocket
              180  LOAD_DEREF               'sock'
              182  CALL_METHOD_1         1  ''

 L. 820       184  LOAD_CONST               ('message', 'exception', 'socket')
              186  BUILD_CONST_KEY_MAP_3     3 
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L. 825       192  LOAD_DEREF               'sock'
              194  LOAD_METHOD              close
              196  CALL_METHOD_0         0  ''
              198  POP_TOP          
              200  JUMP_FORWARD        224  'to 224'
            202_0  COME_FROM           166  '166'

 L. 826       202  LOAD_DEREF               'self'
              204  LOAD_ATTR                _debug
              206  POP_JUMP_IF_FALSE   224  'to 224'

 L. 827       208  LOAD_GLOBAL              logger
              210  LOAD_ATTR                debug
              212  LOAD_STR                 'Accept failed on socket %r'

 L. 828       214  LOAD_DEREF               'sock'

 L. 828       216  LOAD_CONST               True

 L. 827       218  LOAD_CONST               ('exc_info',)
              220  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              222  POP_TOP          
            224_0  COME_FROM           206  '206'
            224_1  COME_FROM           200  '200'
              224  POP_BLOCK        
              226  BEGIN_FINALLY    
            228_0  COME_FROM_FINALLY   154  '154'
              228  LOAD_CONST               None
              230  STORE_FAST               'exc'
              232  DELETE_FAST              'exc'
              234  END_FINALLY      
              236  POP_EXCEPT       
              238  JUMP_FORWARD        296  'to 296'
            240_0  COME_FROM           146  '146'

 L. 829       240  DUP_TOP          
              242  LOAD_GLOBAL              exceptions
              244  LOAD_ATTR                CancelledError
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   270  'to 270'
              252  POP_TOP          
              254  POP_TOP          
              256  POP_TOP          

 L. 830       258  LOAD_DEREF               'sock'
              260  LOAD_METHOD              close
              262  CALL_METHOD_0         0  ''
              264  POP_TOP          
              266  POP_EXCEPT       
              268  JUMP_FORWARD        296  'to 296'
            270_0  COME_FROM           248  '248'
              270  END_FINALLY      
            272_0  COME_FROM           138  '138'

 L. 832       272  LOAD_FAST                'f'
              274  LOAD_DEREF               'self'
              276  LOAD_ATTR                _accept_futures
              278  LOAD_DEREF               'sock'
              280  LOAD_METHOD              fileno
              282  CALL_METHOD_0         0  ''
              284  STORE_SUBSCR     

 L. 833       286  LOAD_FAST                'f'
              288  LOAD_METHOD              add_done_callback
              290  LOAD_DEREF               'loop'
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
            296_0  COME_FROM           268  '268'
            296_1  COME_FROM           238  '238'

Parse error at or near `LOAD_CONST' instruction at offset 120

        self.call_soon(loop)

    def _process_events(self, event_list):
        pass

    def _stop_accept_futures(self):
        for future in self._accept_futures.values():
            future.cancel()
        else:
            self._accept_futures.clear()

    def _stop_serving(self, sock):
        future = self._accept_futures.pop(sock.fileno(), None)
        if future:
            future.cancel()
        self._proactor._stop_serving(sock)
        sock.close()