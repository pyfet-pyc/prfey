# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\client_proto.py
import asyncio
from contextlib import suppress
from typing import Any, Optional, Tuple
from .base_protocol import BaseProtocol
from .client_exceptions import ClientOSError, ClientPayloadError, ServerDisconnectedError, ServerTimeoutError
from .helpers import BaseTimerContext
from .http import HttpResponseParser, RawResponseMessage
from .streams import EMPTY_PAYLOAD, DataQueue, StreamReader

class ResponseHandler(BaseProtocol, DataQueue[Tuple[(RawResponseMessage, StreamReader)]]):
    __doc__ = 'Helper class to adapt between Protocol and StreamReader.'

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        BaseProtocol.__init__(self, loop=loop)
        DataQueue.__init__(self, loop)
        self._should_close = False
        self._payload = None
        self._skip_payload = False
        self._payload_parser = None
        self._timer = None
        self._tail = b''
        self._upgraded = False
        self._parser = None
        self._read_timeout = None
        self._read_timeout_handle = None

    @property
    def upgraded(self) -> bool:
        return self._upgraded

    @property
    def should_close--- This code section failed: ---

 L.  47         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _payload
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L.  48        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _payload
               14  LOAD_METHOD              is_eof
               16  CALL_METHOD_0         0  ''

 L.  47        18  POP_JUMP_IF_FALSE    26  'to 26'
             20_0  COME_FROM             8  '8'

 L.  48        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _upgraded

 L.  47        24  POP_JUMP_IF_FALSE    30  'to 30'
             26_0  COME_FROM            18  '18'

 L.  49        26  LOAD_CONST               True
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L.  51        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _should_close
               34  JUMP_IF_TRUE_OR_POP    84  'to 84'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _upgraded
               40  JUMP_IF_TRUE_OR_POP    84  'to 84'

 L.  52        42  LOAD_FAST                'self'
               44  LOAD_METHOD              exception
               46  CALL_METHOD_0         0  ''
               48  LOAD_CONST               None
               50  COMPARE_OP               is-not

 L.  51        52  JUMP_IF_TRUE_OR_POP    84  'to 84'

 L.  53        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _payload_parser
               58  LOAD_CONST               None
               60  COMPARE_OP               is-not

 L.  51        62  JUMP_IF_TRUE_OR_POP    84  'to 84'

 L.  54        64  LOAD_GLOBAL              len
               66  LOAD_FAST                'self'
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_CONST               0
               72  COMPARE_OP               >

 L.  51        74  JUMP_IF_TRUE_OR_POP    84  'to 84'

 L.  54        76  LOAD_GLOBAL              bool
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _tail
               82  CALL_FUNCTION_1       1  ''
             84_0  COME_FROM            74  '74'
             84_1  COME_FROM            62  '62'
             84_2  COME_FROM            52  '52'
             84_3  COME_FROM            40  '40'
             84_4  COME_FROM            34  '34'

 L.  51        84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 84

    def force_close(self) -> None:
        self._should_close = True

    def close(self) -> None:
        transport = self.transport
        if transport is not None:
            transport.close
            self.transport = None
            self._payload = None
            self._drop_timeout

    def is_connected(self) -> bool:
        return self.transport is not None

    def connection_lost(self, exc):
        self._drop_timeout
        if self._payload_parser is not None:
            with suppress(Exception):
                self._payload_parser.feed_eof
        uncompleted = None
        if self._parser is not None:
            try:
                uncompleted = self._parser.feed_eof
            except Exception:
                if self._payload is not None:
                    self._payload.set_exception(ClientPayloadError('Response payload is not completed'))

        if not self.is_eof:
            if isinstance(exc, OSError):
                exc = ClientOSError(*exc.args)
            if exc is None:
                exc = ServerDisconnectedError(uncompleted)
            self.set_exception(exc)
        self._should_close = True
        self._parser = None
        self._payload = None
        self._payload_parser = None
        self._reading_paused = False
        super().connection_lost(exc)

    def eof_received(self) -> None:
        self._drop_timeout

    def pause_reading(self):
        super().pause_reading
        self._drop_timeout

    def resume_reading(self):
        super().resume_reading
        self._reschedule_timeout

    def set_exception(self, exc):
        self._should_close = True
        self._drop_timeout
        super().set_exception(exc)

    def set_parser(self, parser: Any, payload: Any) -> None:
        self._payload = payload
        self._payload_parser = parser
        self._drop_timeout
        if self._tail:
            data, self._tail = self._tail, b''
            self.data_received(data)

    def set_response_params(self, *, timer: BaseTimerContext=None, skip_payload: bool=False, read_until_eof: bool=False, auto_decompress: bool=True, read_timeout: Optional[float]=None) -> None:
        self._skip_payload = skip_payload
        self._read_timeout = read_timeout
        self._reschedule_timeout
        self._parser = HttpResponseParser(self,
          (self._loop), timer=timer, payload_exception=ClientPayloadError,
          read_until_eof=read_until_eof,
          auto_decompress=auto_decompress)
        if self._tail:
            data, self._tail = self._tail, b''
            self.data_received(data)

    def _drop_timeout(self) -> None:
        if self._read_timeout_handle is not None:
            self._read_timeout_handle.cancel
            self._read_timeout_handle = None

    def _reschedule_timeout(self) -> None:
        timeout = self._read_timeout
        if self._read_timeout_handle is not None:
            self._read_timeout_handle.cancel
        elif timeout:
            self._read_timeout_handle = self._loop.call_later(timeout, self._on_read_timeout)
        else:
            self._read_timeout_handle = None

    def _on_read_timeout(self) -> None:
        exc = ServerTimeoutError('Timeout on reading data from socket')
        self.set_exception(exc)
        if self._payload is not None:
            self._payload.set_exception(exc)

    def data_received--- This code section failed: ---

 L. 179         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _reschedule_timeout
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 181         8  LOAD_FAST                'data'
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L. 182        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 185        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _payload_parser
               20  LOAD_CONST               None
               22  COMPARE_OP               is-not
               24  POP_JUMP_IF_FALSE    76  'to 76'

 L. 186        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _payload_parser
               30  LOAD_METHOD              feed_data
               32  LOAD_FAST                'data'
               34  CALL_METHOD_1         1  ''
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'eof'
               40  STORE_FAST               'tail'

 L. 187        42  LOAD_FAST                'eof'
               44  POP_JUMP_IF_FALSE    72  'to 72'

 L. 188        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _payload

 L. 189        52  LOAD_CONST               None
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _payload_parser

 L. 191        58  LOAD_FAST                'tail'
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L. 192        62  LOAD_FAST                'self'
               64  LOAD_METHOD              data_received
               66  LOAD_FAST                'tail'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
             72_0  COME_FROM            60  '60'
             72_1  COME_FROM            44  '44'

 L. 193        72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            24  '24'

 L. 195        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _upgraded
               80  POP_JUMP_IF_TRUE     92  'to 92'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                _parser
               86  LOAD_CONST               None
               88  COMPARE_OP               is
               90  POP_JUMP_IF_FALSE   110  'to 110'
             92_0  COME_FROM            80  '80'

 L. 197        92  LOAD_FAST                'self'
               94  DUP_TOP          
               96  LOAD_ATTR                _tail
               98  LOAD_FAST                'data'
              100  INPLACE_ADD      
              102  ROT_TWO          
              104  STORE_ATTR               _tail
          106_108  JUMP_FORWARD        372  'to 372'
            110_0  COME_FROM            90  '90'

 L. 200       110  SETUP_FINALLY       134  'to 134'

 L. 201       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _parser
              116  LOAD_METHOD              feed_data
              118  LOAD_FAST                'data'
              120  CALL_METHOD_1         1  ''
              122  UNPACK_SEQUENCE_3     3 
              124  STORE_FAST               'messages'
              126  STORE_FAST               'upgraded'
              128  STORE_FAST               'tail'
              130  POP_BLOCK        
              132  JUMP_FORWARD        204  'to 204'
            134_0  COME_FROM_FINALLY   110  '110'

 L. 202       134  DUP_TOP          
              136  LOAD_GLOBAL              BaseException
              138  COMPARE_OP               exception-match
              140  POP_JUMP_IF_FALSE   202  'to 202'
              142  POP_TOP          
              144  STORE_FAST               'exc'
              146  POP_TOP          
              148  SETUP_FINALLY       190  'to 190'

 L. 203       150  LOAD_FAST                'self'
              152  LOAD_ATTR                transport
              154  LOAD_CONST               None
              156  COMPARE_OP               is-not
              158  POP_JUMP_IF_FALSE   170  'to 170'

 L. 207       160  LOAD_FAST                'self'
              162  LOAD_ATTR                transport
              164  LOAD_METHOD              close
              166  CALL_METHOD_0         0  ''
              168  POP_TOP          
            170_0  COME_FROM           158  '158'

 L. 209       170  LOAD_FAST                'self'
              172  LOAD_METHOD              set_exception
              174  LOAD_FAST                'exc'
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          

 L. 210       180  POP_BLOCK        
              182  POP_EXCEPT       
              184  CALL_FINALLY        190  'to 190'
              186  LOAD_CONST               None
              188  RETURN_VALUE     
            190_0  COME_FROM           184  '184'
            190_1  COME_FROM_FINALLY   148  '148'
              190  LOAD_CONST               None
              192  STORE_FAST               'exc'
              194  DELETE_FAST              'exc'
              196  END_FINALLY      
              198  POP_EXCEPT       
              200  JUMP_FORWARD        204  'to 204'
            202_0  COME_FROM           140  '140'
              202  END_FINALLY      
            204_0  COME_FROM           200  '200'
            204_1  COME_FROM           132  '132'

 L. 212       204  LOAD_FAST                'upgraded'
              206  LOAD_FAST                'self'
              208  STORE_ATTR               _upgraded

 L. 214       210  LOAD_CONST               None
              212  STORE_FAST               'payload'

 L. 215       214  LOAD_FAST                'messages'
              216  GET_ITER         
              218  FOR_ITER            300  'to 300'
              220  UNPACK_SEQUENCE_2     2 
              222  STORE_FAST               'message'
              224  STORE_FAST               'payload'

 L. 216       226  LOAD_FAST                'message'
              228  LOAD_ATTR                should_close
              230  POP_JUMP_IF_FALSE   238  'to 238'

 L. 217       232  LOAD_CONST               True
              234  LOAD_FAST                'self'
              236  STORE_ATTR               _should_close
            238_0  COME_FROM           230  '230'

 L. 219       238  LOAD_FAST                'payload'
              240  LOAD_FAST                'self'
              242  STORE_ATTR               _payload

 L. 221       244  LOAD_FAST                'self'
              246  LOAD_ATTR                _skip_payload
          248_250  POP_JUMP_IF_TRUE    264  'to 264'
              252  LOAD_FAST                'message'
              254  LOAD_ATTR                code
              256  LOAD_CONST               (204, 304)
              258  COMPARE_OP               in
          260_262  POP_JUMP_IF_FALSE   282  'to 282'
            264_0  COME_FROM           248  '248'

 L. 222       264  LOAD_FAST                'self'
              266  LOAD_METHOD              feed_data
              268  LOAD_FAST                'message'
              270  LOAD_GLOBAL              EMPTY_PAYLOAD
              272  BUILD_TUPLE_2         2 
              274  LOAD_CONST               0
              276  CALL_METHOD_2         2  ''
              278  POP_TOP          
              280  JUMP_BACK           218  'to 218'
            282_0  COME_FROM           260  '260'

 L. 224       282  LOAD_FAST                'self'
              284  LOAD_METHOD              feed_data
              286  LOAD_FAST                'message'
              288  LOAD_FAST                'payload'
              290  BUILD_TUPLE_2         2 
              292  LOAD_CONST               0
              294  CALL_METHOD_2         2  ''
              296  POP_TOP          
              298  JUMP_BACK           218  'to 218'

 L. 225       300  LOAD_FAST                'payload'
              302  LOAD_CONST               None
              304  COMPARE_OP               is-not
          306_308  POP_JUMP_IF_FALSE   342  'to 342'

 L. 230       310  LOAD_FAST                'payload'
              312  LOAD_GLOBAL              EMPTY_PAYLOAD
              314  COMPARE_OP               is-not
          316_318  POP_JUMP_IF_FALSE   334  'to 334'

 L. 231       320  LOAD_FAST                'payload'
              322  LOAD_METHOD              on_eof
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                _drop_timeout
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
              332  JUMP_FORWARD        342  'to 342'
            334_0  COME_FROM           316  '316'

 L. 233       334  LOAD_FAST                'self'
              336  LOAD_METHOD              _drop_timeout
              338  CALL_METHOD_0         0  ''
              340  POP_TOP          
            342_0  COME_FROM           332  '332'
            342_1  COME_FROM           306  '306'

 L. 235       342  LOAD_FAST                'tail'
          344_346  POP_JUMP_IF_FALSE   372  'to 372'

 L. 236       348  LOAD_FAST                'upgraded'
          350_352  POP_JUMP_IF_FALSE   366  'to 366'

 L. 237       354  LOAD_FAST                'self'
              356  LOAD_METHOD              data_received
              358  LOAD_FAST                'tail'
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          
              364  JUMP_FORWARD        372  'to 372'
            366_0  COME_FROM           350  '350'

 L. 239       366  LOAD_FAST                'tail'
              368  LOAD_FAST                'self'
              370  STORE_ATTR               _tail
            372_0  COME_FROM           364  '364'
            372_1  COME_FROM           344  '344'
            372_2  COME_FROM           106  '106'

Parse error at or near `CALL_FINALLY' instruction at offset 184