# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\payload.py
import asyncio, enum, io, json, mimetypes, os, warnings
from abc import ABC, abstractmethod
from itertools import chain
from typing import IO, TYPE_CHECKING, Any, ByteString, Dict, Iterable, Optional, Text, TextIO, Tuple, Type, Union
from multidict import CIMultiDict
from . import hdrs
from .abc import AbstractStreamWriter
from .helpers import PY_36, content_disposition_header, guess_filename, parse_mimetype, sentinel
from .streams import DEFAULT_LIMIT, StreamReader
from .typedefs import JSONEncoder, _CIMultiDict
__all__ = ('PAYLOAD_REGISTRY', 'get_payload', 'payload_type', 'Payload', 'BytesPayload',
           'StringPayload', 'IOBasePayload', 'BytesIOPayload', 'BufferedReaderPayload',
           'TextIOPayload', 'StringIOPayload', 'JsonPayload', 'AsyncIterablePayload')
TOO_LARGE_BYTES_BODY = 1048576
if TYPE_CHECKING:
    from typing import List

class LookupError(Exception):
    pass


class Order(str, enum.Enum):
    normal = 'normal'
    try_first = 'try_first'
    try_last = 'try_last'


def get_payload(data: Any, *args: Any, **kwargs: Any) -> 'Payload':
    return (PAYLOAD_REGISTRY.get)(data, *args, **kwargs)


def register_payload(factory: Type['Payload'], type: Any, *, order: Order=Order.normal) -> None:
    PAYLOAD_REGISTRY.register(factory, type, order=order)


class payload_type:

    def __init__(self, type: Any, *, order: Order=Order.normal) -> None:
        self.type = type
        self.order = order

    def __call__(self, factory: Type['Payload']) -> Type['Payload']:
        register_payload(factory, (self.type), order=(self.order))
        return factory


class PayloadRegistry:
    __doc__ = 'Payload registry.\n\n    note: we need zope.interface for more efficient adapter search\n    '

    def __init__(self) -> None:
        self._first = []
        self._normal = []
        self._last = []

    def get(self, data: Any, *args: Any, _CHAIN: Any=chain, **kwargs: Any) -> 'Payload':
        if isinstance(data, Payload):
            return data
        for factory, type in _CHAIN(self._first, self._normal, self._last):
            if isinstance(data, type):
                return factory(data, *args, **kwargs)
        else:
            raise LookupError()

    def register(self, factory: Type['Payload'], type: Any, *, order: Order=Order.normal) -> None:
        if order is Order.try_first:
            self._first.append((factory, type))
        elif order is Order.normal:
            self._normal.append((factory, type))
        elif order is Order.try_last:
            self._last.append((factory, type))
        else:
            raise ValueError('Unsupported order {!r}'.format(order))


class Payload(ABC):
    _default_content_type = 'application/octet-stream'
    _size = None

    def __init__(self, value: Any, headers: Optional[Union[(
 _CIMultiDict,
 Dict[(str, str)],
 Iterable[Tuple[(str, str)]])]]=None, content_type: Optional[str]=sentinel, filename: Optional[str]=None, encoding: Optional[str]=None, **kwargs: Any) -> None:
        self._encoding = encoding
        self._filename = filename
        self._headers = CIMultiDict()
        self._value = value
        if content_type is not sentinel and content_type is not None:
            self._headers[hdrs.CONTENT_TYPE] = content_type
        elif self._filename is not None:
            content_type = mimetypes.guess_type(self._filename)[0]
            if content_type is None:
                content_type = self._default_content_type
            self._headers[hdrs.CONTENT_TYPE] = content_type
        else:
            self._headers[hdrs.CONTENT_TYPE] = self._default_content_type
        self._headers.update(headers or {})

    @property
    def size(self) -> Optional[int]:
        """Size of the payload."""
        return self._size

    @property
    def filename(self) -> Optional[str]:
        """Filename of the payload."""
        return self._filename

    @property
    def headers(self) -> _CIMultiDict:
        """Custom item headers"""
        return self._headers

    @property
    def _binary_headers(self) -> bytes:
        return ''.join([k + ': ' + v + '\r\n' for k, v in self.headers.items()]).encode('utf-8') + b'\r\n'

    @property
    def encoding(self) -> Optional[str]:
        """Payload encoding"""
        return self._encoding

    @property
    def content_type(self) -> str:
        """Content type"""
        return self._headers[hdrs.CONTENT_TYPE]

    def set_content_disposition(self, disptype: str, quote_fields: bool=True, **params: Any) -> None:
        """Sets ``Content-Disposition`` header."""
        self._headers[hdrs.CONTENT_DISPOSITION] = content_disposition_header(
 disptype, quote_fields=quote_fields, **params)

    @abstractmethod
    async def write(self, writer: AbstractStreamWriter) -> None:
        """Write payload.

        writer is an AbstractStreamWriter instance:
        """
        pass


class BytesPayload(Payload):

    def __init__(self, value, *args, **kwargs):
        if not isinstance(value, (bytes, bytearray, memoryview)):
            raise TypeError('value argument must be byte-ish, not {!r}'.format(type(value)))
        if 'content_type' not in kwargs:
            kwargs['content_type'] = 'application/octet-stream'
        (super().__init__)(value, *args, **kwargs)
        self._size = len(value)
        if self._size > TOO_LARGE_BYTES_BODY:
            if PY_36:
                kwargs = {'source': self}
            else:
                kwargs = {}
            (warnings.warn)('Sending a large body directly with raw bytes might lock the event loop. You should probably pass an io.BytesIO object instead', 
             ResourceWarning, **kwargs)

    async def write(self, writer: AbstractStreamWriter) -> None:
        await writer.write(self._value)


class StringPayload(BytesPayload):

    def __init__(self, value, *args, encoding=None, content_type=None, **kwargs):
        if encoding is None:
            if content_type is None:
                real_encoding = 'utf-8'
                content_type = 'text/plain; charset=utf-8'
            else:
                mimetype = parse_mimetype(content_type)
                real_encoding = mimetype.parameters.get('charset', 'utf-8')
        else:
            if content_type is None:
                content_type = 'text/plain; charset=%s' % encoding
            real_encoding = encoding
        (super().__init__)(
 (value.encode(real_encoding)), *args, encoding=real_encoding, 
         content_type=content_type, **kwargs)


class StringIOPayload(StringPayload):

    def __init__(self, value, *args, **kwargs):
        (super().__init__)(value.read(), *args, **kwargs)


class IOBasePayload(Payload):

    def __init__(self, value, disposition='attachment', *args, **kwargs):
        if 'filename' not in kwargs:
            kwargs['filename'] = guess_filename(value)
        (super().__init__)(value, *args, **kwargs)
        if self._filename is not None:
            if disposition is not None:
                if hdrs.CONTENT_DISPOSITION not in self.headers:
                    self.set_content_disposition(disposition,
                      filename=(self._filename))

    async def write(self, writer: AbstractStreamWriter) -> None:
        loop = asyncio.get_event_loop()
        try:
            chunk = await loop.run_in_executor(None, self._value.read, DEFAULT_LIMIT)
            while True:
                if chunk:
                    await writer.write(chunk)
                    chunk = await loop.run_in_executor(None, self._value.read, DEFAULT_LIMIT)

        finally:
            await loop.run_in_executor(None, self._value.close)


class TextIOPayload(IOBasePayload):

    def __init__(self, value, *args, encoding=None, content_type=None, **kwargs):
        if encoding is None:
            if content_type is None:
                encoding = 'utf-8'
                content_type = 'text/plain; charset=utf-8'
            else:
                mimetype = parse_mimetype(content_type)
                encoding = mimetype.parameters.get('charset', 'utf-8')
        elif content_type is None:
            content_type = 'text/plain; charset=%s' % encoding
        (super().__init__)(
 value, *args, content_type=content_type, 
         encoding=encoding, **kwargs)

    @property
    def size--- This code section failed: ---

 L. 336         0  SETUP_FINALLY        32  'to 32'

 L. 337         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              fstat
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _value
               10  LOAD_METHOD              fileno
               12  CALL_METHOD_0         0  ''
               14  CALL_METHOD_1         1  ''
               16  LOAD_ATTR                st_size
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _value
               22  LOAD_METHOD              tell
               24  CALL_METHOD_0         0  ''
               26  BINARY_SUBTRACT  
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     0  '0'

 L. 338        32  DUP_TOP          
               34  LOAD_GLOBAL              OSError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    52  'to 52'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 339        46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            38  '38'
               52  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 48

    async def write(self, writer: AbstractStreamWriter) -> None:
        loop = asyncio.get_event_loop()
        try:
            chunk = await loop.run_in_executor(None, self._value.read, DEFAULT_LIMIT)
            while True:
                if chunk:
                    await writer.write(chunk.encode(self._encoding))
                    chunk = await loop.run_in_executor(None, self._value.read, DEFAULT_LIMIT)

        finally:
            await loop.run_in_executor(None, self._value.close)


class BytesIOPayload(IOBasePayload):

    @property
    def size(self) -> int:
        position = self._value.tell()
        end = self._value.seek(0, os.SEEK_END)
        self._value.seek(position)
        return end - position


class BufferedReaderPayload(IOBasePayload):

    @property
    def size--- This code section failed: ---

 L. 370         0  SETUP_FINALLY        32  'to 32'

 L. 371         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              fstat
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _value
               10  LOAD_METHOD              fileno
               12  CALL_METHOD_0         0  ''
               14  CALL_METHOD_1         1  ''
               16  LOAD_ATTR                st_size
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _value
               22  LOAD_METHOD              tell
               24  CALL_METHOD_0         0  ''
               26  BINARY_SUBTRACT  
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     0  '0'

 L. 372        32  DUP_TOP          
               34  LOAD_GLOBAL              OSError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    52  'to 52'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 375        46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            38  '38'
               52  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 48


class JsonPayload(BytesPayload):

    def __init__(self, value, encoding='utf-8', content_type='application/json', dumps=json.dumps, *args, **kwargs):
        (super().__init__)(
 (dumps(value).encode(encoding)), *args, content_type=content_type, 
         encoding=encoding, **kwargs)


if TYPE_CHECKING:
    from typing import AsyncIterator, AsyncIterable
    _AsyncIterator = AsyncIterator[bytes]
    _AsyncIterable = AsyncIterable[bytes]
else:
    from collections.abc import AsyncIterable, AsyncIterator
    _AsyncIterator = AsyncIterator
    _AsyncIterable = AsyncIterable

class AsyncIterablePayload(Payload):
    _iter = None

    def __init__(self, value, *args, **kwargs):
        if not isinstance(value, AsyncIterable):
            raise TypeError('value argument must support collections.abc.AsyncIterablebe interface, got {!r}'.format(type(value)))
        if 'content_type' not in kwargs:
            kwargs['content_type'] = 'application/octet-stream'
        (super().__init__)(value, *args, **kwargs)
        self._iter = value.__aiter__()

    async def write(self, writer: AbstractStreamWriter) -> None:
        if self._iter:
            try:
                while True:
                    chunk = await self._iter.__anext__()
                    await writer.write(chunk)

            except StopAsyncIteration:
                self._iter = None


class StreamReaderPayload(AsyncIterablePayload):

    def __init__(self, value, *args, **kwargs):
        (super().__init__)(value.iter_any(), *args, **kwargs)


PAYLOAD_REGISTRY = PayloadRegistry()
PAYLOAD_REGISTRY.register(BytesPayload, (bytes, bytearray, memoryview))
PAYLOAD_REGISTRY.register(StringPayload, str)
PAYLOAD_REGISTRY.register(StringIOPayload, io.StringIO)
PAYLOAD_REGISTRY.register(TextIOPayload, io.TextIOBase)
PAYLOAD_REGISTRY.register(BytesIOPayload, io.BytesIO)
PAYLOAD_REGISTRY.register(BufferedReaderPayload, (io.BufferedReader, io.BufferedRandom))
PAYLOAD_REGISTRY.register(IOBasePayload, io.IOBase)
PAYLOAD_REGISTRY.register(StreamReaderPayload, StreamReader)
PAYLOAD_REGISTRY.register(AsyncIterablePayload, AsyncIterable, order=(Order.try_last))