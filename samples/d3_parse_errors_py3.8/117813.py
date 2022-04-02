# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\streams.py
import asyncio, collections, warnings
from typing import List
from typing import Awaitable, Callable, Generic, Optional, Tuple, TypeVar
from .base_protocol import BaseProtocol
from .helpers import BaseTimerContext, set_exception, set_result
from .log import internal_logger
try:
    from typing import Deque
except ImportError:
    from typing_extensions import Deque
else:
    __all__ = ('EMPTY_PAYLOAD', 'EofStream', 'StreamReader', 'DataQueue', 'FlowControlDataQueue')
    DEFAULT_LIMIT = 65536
    _T = TypeVar('_T')

    class EofStream(Exception):
        __doc__ = 'eof stream indication.'


    class AsyncStreamIterator(Generic[_T]):

        def __init__(self, read_func: Callable[([], Awaitable[_T])]) -> None:
            self.read_func = read_func

        def __aiter__(self) -> 'AsyncStreamIterator[_T]':
            return self

        async def __anext__(self) -> _T:
            try:
                rv = await self.read_func()
            except EofStream:
                raise StopAsyncIteration
            else:
                if rv == b'':
                    raise StopAsyncIteration
                else:
                    return rv


    class ChunkTupleAsyncStreamIterator:

        def __init__(self, stream: 'StreamReader') -> None:
            self._stream = stream

        def __aiter__(self) -> 'ChunkTupleAsyncStreamIterator':
            return self

        async def __anext__(self) -> Tuple[(bytes, bool)]:
            rv = await self._stream.readchunk()
            if rv == (b'', False):
                raise StopAsyncIteration
            return rv


    class AsyncStreamReaderMixin:

        def __aiter__(self) -> AsyncStreamIterator[bytes]:
            return AsyncStreamIterator(self.readline)

        def iter_chunked(self, n: int) -> AsyncStreamIterator[bytes]:
            """Returns an asynchronous iterator that yields chunks of size n.

        Python-3.5 available for Python 3.5+ only
        """
            return AsyncStreamIterator(lambda: self.read(n))

        def iter_any(self) -> AsyncStreamIterator[bytes]:
            """Returns an asynchronous iterator that yields all the available
        data as soon as it is received

        Python-3.5 available for Python 3.5+ only
        """
            return AsyncStreamIterator(self.readany)

        def iter_chunks(self) -> ChunkTupleAsyncStreamIterator:
            """Returns an asynchronous iterator that yields chunks of data
        as they are received by the server. The yielded objects are tuples
        of (bytes, bool) as returned by the StreamReader.readchunk method.

        Python-3.5 available for Python 3.5+ only
        """
            return ChunkTupleAsyncStreamIterator(self)


    class StreamReader(AsyncStreamReaderMixin):
        __doc__ = 'An enhancement of asyncio.StreamReader.\n\n    Supports asynchronous iteration by line, chunk or as available::\n\n        async for line in reader:\n            ...\n        async for chunk in reader.iter_chunked(1024):\n            ...\n        async for slice in reader.iter_any():\n            ...\n\n    '
        total_bytes = 0

        def __init__(self, protocol: BaseProtocol, *, limit: int=DEFAULT_LIMIT, timer: Optional[BaseTimerContext]=None, loop: Optional[asyncio.AbstractEventLoop]=None) -> None:
            self._protocol = protocol
            self._low_water = limit
            self._high_water = limit * 2
            if loop is None:
                loop = asyncio.get_event_loop()
            self._loop = loop
            self._size = 0
            self._cursor = 0
            self._http_chunk_splits = None
            self._buffer = collections.deque()
            self._buffer_offset = 0
            self._eof = False
            self._waiter = None
            self._eof_waiter = None
            self._exception = None
            self._timer = timer
            self._eof_callbacks = []

        def __repr__(self) -> str:
            info = [self.__class__.__name__]
            if self._size:
                info.append('%d bytes' % self._size)
            if self._eof:
                info.append('eof')
            if self._low_water != DEFAULT_LIMIT:
                info.append('low=%d high=%d' % (self._low_water, self._high_water))
            if self._waiter:
                info.append('w=%r' % self._waiter)
            if self._exception:
                info.append('e=%r' % self._exception)
            return '<%s>' % ' '.join(info)

        def exception(self) -> Optional[BaseException]:
            return self._exception

        def set_exception(self, exc: BaseException) -> None:
            self._exception = exc
            self._eof_callbacks.clear()
            waiter = self._waiter
            if waiter is not None:
                self._waiter = None
                set_exception(waiter, exc)
            waiter = self._eof_waiter
            if waiter is not None:
                self._eof_waiter = None
                set_exception(waiter, exc)

        def on_eof(self, callback: Callable[([], None)]) -> None:
            if self._eof:
                try:
                    callback()
                except Exception:
                    internal_logger.exception('Exception in eof callback')

            else:
                self._eof_callbacks.append(callback)

        def feed_eof(self) -> None:
            self._eof = True
            waiter = self._waiter
            if waiter is not None:
                self._waiter = None
                set_result(waiter, None)
            waiter = self._eof_waiter
            if waiter is not None:
                self._eof_waiter = None
                set_result(waiter, None)
            for cb in self._eof_callbacks:
                try:
                    cb()
                except Exception:
                    internal_logger.exception('Exception in eof callback')

            else:
                self._eof_callbacks.clear()

        def is_eof(self) -> bool:
            """Return True if  'feed_eof' was called."""
            return self._eof

        def at_eof(self) -> bool:
            """Return True if the buffer is empty and 'feed_eof' was called."""
            return self._eof and not self._buffer

        async def wait_eof(self) -> None:
            if self._eof:
                return
            assert self._eof_waiter is None
            self._eof_waiter = self._loop.create_future()
            try:
                await self._eof_waiter
            finally:
                self._eof_waiter = None

        def unread_data(self, data: bytes) -> None:
            """ rollback reading some data from stream, inserting it to buffer head.
        """
            warnings.warn('unread_data() is deprecated and will be removed in future releases (#3260)', DeprecationWarning,
              stacklevel=2)
            if not data:
                return
            if self._buffer_offset:
                self._buffer[0] = self._buffer[0][self._buffer_offset:]
                self._buffer_offset = 0
            self._size += len(data)
            self._cursor -= len(data)
            self._buffer.appendleft(data)
            self._eof_counter = 0

        def feed_data(self, data: bytes, size: int=0) -> None:
            if self._eof:
                raise AssertionError('feed_data after feed_eof')
            if not data:
                return
            self._size += len(data)
            self._buffer.append(data)
            self.total_bytes += len(data)
            waiter = self._waiter
            if waiter is not None:
                self._waiter = None
                set_result(waiter, None)
            if self._size > self._high_water:
                if not self._protocol._reading_paused:
                    self._protocol.pause_reading()

        def begin_http_chunk_receiving(self) -> None:
            if self._http_chunk_splits is None:
                if self.total_bytes:
                    raise RuntimeError('Called begin_http_chunk_receiving whensome data was already fed')
                self._http_chunk_splits = []

        def end_http_chunk_receiving(self) -> None:
            if self._http_chunk_splits is None:
                raise RuntimeError('Called end_chunk_receiving without calling begin_chunk_receiving first')
            pos = self._http_chunk_splits[(-1)] if self._http_chunk_splits else 0
            if self.total_bytes == pos:
                return
            self._http_chunk_splits.append(self.total_bytes)
            waiter = self._waiter
            if waiter is not None:
                self._waiter = None
                set_result(waiter, None)

        async def _wait(self, func_name: str) -> None:
            if self._waiter is not None:
                raise RuntimeError('%s() called while another coroutine is already waiting for incoming data' % func_name)
            waiter = self._waiter = self._loop.create_future()
            try:
                if self._timer:
                    with self._timer:
                        await waiter
                else:
                    await waiter
            finally:
                self._waiter = None

        async def readline(self) -> bytes:
            if self._exception is not None:
                raise self._exception
            line = []
            line_size = 0
            not_enough = True
            while True:
                if not_enough:
                    while self._buffer:
                        if not_enough:
                            offset = self._buffer_offset
                            ichar = self._buffer[0].find(b'\n', offset) + 1
                            data = self._read_nowait_chunk(ichar - offset if ichar else -1)
                            line.append(data)
                            line_size += len(data)
                            if ichar:
                                not_enough = False
                            if line_size > self._high_water:
                                raise ValueError('Line is too long')

                    if self._eof:
                        pass
                    else:
                        if not_enough:
                            await self._wait('readline')

            return (b'').join(line)

        async def read(self, n: int=-1) -> bytes:
            if self._exception is not None:
                raise self._exception
            if self._eof:
                if not self._buffer:
                    self._eof_counter = getattr(self, '_eof_counter', 0) + 1
                    if self._eof_counter > 5:
                        internal_logger.warning('Multiple access to StreamReader in eof state, might be infinite loop.',
                          stack_info=True)
                if not n:
                    return b''
                if n < 0:
                    blocks = []
                    while True:
                        block = await self.readany()
                        if not block:
                            pass
                        else:
                            blocks.append(block)

                    return (b'').join(blocks)
                    while True:
                        await (self._buffer or self._eof or self._wait('read'))

                return self._read_nowait(n)

        async def readany(self) -> bytes:
            if self._exception is not None:
                raise self._exception
                while True:
                    await (self._buffer or self._eof or self._wait('readany'))

                return self._read_nowait(-1)

        async def readchunk(self) -> Tuple[(bytes, bool)]:
            """Returns a tuple of (data, end_of_http_chunk). When chunked transfer
        encoding is used, end_of_http_chunk is a boolean indicating if the end
        of the data corresponds to the end of a HTTP chunk , otherwise it is
        always False.
        """
            while self._exception is not None:
                raise self._exception
                while True:
                    if self._http_chunk_splits:
                        pos = self._http_chunk_splits.pop(0)
                        if pos == self._cursor:
                            return (b'', True)
                        if pos > self._cursor:
                            return (self._read_nowait(pos - self._cursor), True)
                        internal_logger.warning('Skipping HTTP chunk end due to data consumption beyond chunk boundary')

                if self._buffer:
                    return (self._read_nowait_chunk(-1), False)
                else:
                    if self._eof:
                        return (b'', False)
                    await self._wait('readchunk')

        async def readexactly(self, n: int) -> bytes:
            if self._exception is not None:
                raise self._exception
            blocks = []
            while True:
                if n > 0:
                    block = await self.read(n)
                    if not block:
                        partial = (b'').join(blocks)
                        raise asyncio.IncompleteReadError(partial, len(partial) + n)
                    blocks.append(block)
                    n -= len(block)

            return (b'').join(blocks)

        def read_nowait(self, n: int=-1) -> bytes:
            if self._exception is not None:
                raise self._exception
            if self._waiter:
                if not self._waiter.done():
                    raise RuntimeError('Called while some coroutine is waiting for incoming data.')
                return self._read_nowait(n)

        def _read_nowait_chunk(self, n: int) -> bytes:
            first_buffer = self._buffer[0]
            offset = self._buffer_offset
            if n != -1 and len(first_buffer) - offset > n:
                data = first_buffer[offset:offset + n]
                self._buffer_offset += n
            elif offset:
                self._buffer.popleft()
                data = first_buffer[offset:]
                self._buffer_offset = 0
            else:
                data = self._buffer.popleft()
            self._size -= len(data)
            self._cursor += len(data)
            chunk_splits = self._http_chunk_splits
            while chunk_splits:
                if chunk_splits[0] < self._cursor:
                    chunk_splits.pop(0)

            if self._size < self._low_water:
                if self._protocol._reading_paused:
                    self._protocol.resume_reading()
            return data

        def _read_nowait--- This code section failed: ---

 L. 473         0  BUILD_LIST_0          0 
                2  STORE_FAST               'chunks'
              4_0  COME_FROM            60  '60'
              4_1  COME_FROM            56  '56'
              4_2  COME_FROM            36  '36'

 L. 475         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _buffer
                8  POP_JUMP_IF_FALSE    62  'to 62'

 L. 476        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _read_nowait_chunk
               14  LOAD_FAST                'n'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'chunk'

 L. 477        20  LOAD_FAST                'chunks'
               22  LOAD_METHOD              append
               24  LOAD_FAST                'chunk'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 478        30  LOAD_FAST                'n'
               32  LOAD_CONST               -1
               34  COMPARE_OP               !=
               36  POP_JUMP_IF_FALSE_BACK     4  'to 4'

 L. 479        38  LOAD_FAST                'n'
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'chunk'
               44  CALL_FUNCTION_1       1  ''
               46  INPLACE_SUBTRACT 
               48  STORE_FAST               'n'

 L. 480        50  LOAD_FAST                'n'
               52  LOAD_CONST               0
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE_BACK     4  'to 4'

 L. 481        58  JUMP_FORWARD         62  'to 62'
               60  JUMP_BACK             4  'to 4'
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM             8  '8'

 L. 483        62  LOAD_FAST                'chunks'
               64  POP_JUMP_IF_FALSE    76  'to 76'
               66  LOAD_CONST               b''
               68  LOAD_METHOD              join
               70  LOAD_FAST                'chunks'
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            64  '64'
               76  LOAD_CONST               b''
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 60


    class EmptyStreamReader(AsyncStreamReaderMixin):

        def exception(self) -> Optional[BaseException]:
            pass

        def set_exception(self, exc: BaseException) -> None:
            pass

        def on_eof(self, callback: Callable[([], None)]) -> None:
            try:
                callback()
            except Exception:
                internal_logger.exception('Exception in eof callback')

        def feed_eof(self) -> None:
            pass

        def is_eof(self) -> bool:
            return True

        def at_eof(self) -> bool:
            return True

        async def wait_eof(self) -> None:
            pass

        def feed_data(self, data: bytes, n: int=0) -> None:
            pass

        async def readline(self) -> bytes:
            return b''

        async def read(self, n: int=-1) -> bytes:
            return b''

        async def readany(self) -> bytes:
            return b''

        async def readchunk(self) -> Tuple[(bytes, bool)]:
            return (b'', True)

        async def readexactly(self, n: int) -> bytes:
            raise asyncio.IncompleteReadError(b'', n)

        def read_nowait(self) -> bytes:
            return b''


    EMPTY_PAYLOAD = EmptyStreamReader()

    class DataQueue(Generic[_T]):
        __doc__ = 'DataQueue is a general-purpose blocking queue with one reader.'

        def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
            self._loop = loop
            self._eof = False
            self._waiter = None
            self._exception = None
            self._size = 0
            self._buffer = collections.deque()

        def __len__(self) -> int:
            return len(self._buffer)

        def is_eof(self) -> bool:
            return self._eof

        def at_eof(self) -> bool:
            return self._eof and not self._buffer

        def exception(self) -> Optional[BaseException]:
            return self._exception

        def set_exception(self, exc: BaseException) -> None:
            self._eof = True
            self._exception = exc
            waiter = self._waiter
            if waiter is not None:
                self._waiter = None
                set_exception(waiter, exc)

        def feed_data(self, data: _T, size: int=0) -> None:
            self._size += size
            self._buffer.append((data, size))
            waiter = self._waiter
            if waiter is not None:
                self._waiter = None
                set_result(waiter, None)

        def feed_eof(self) -> None:
            self._eof = True
            waiter = self._waiter
            if waiter is not None:
                self._waiter = None
                set_result(waiter, None)

        async def read(self) -> _T:
            if not (self._buffer or self._eof):
                assert not self._waiter
                self._waiter = self._loop.create_future()
                try:
                    await self._waiter
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    self._waiter = None
                    raise

            if self._buffer:
                data, size = self._buffer.popleft()
                self._size -= size
                return data
            if self._exception is not None:
                raise self._exception
            else:
                raise EofStream

        def __aiter__(self) -> AsyncStreamIterator[_T]:
            return AsyncStreamIterator(self.read)


    class FlowControlDataQueue(DataQueue[_T]):
        __doc__ = 'FlowControlDataQueue resumes and pauses an underlying stream.\n\n    It is a destination for parsed data.'

        def __init__(self, protocol, *, limit=DEFAULT_LIMIT, loop):
            super().__init__(loop=loop)
            self._protocol = protocol
            self._limit = limit * 2

        def feed_data(self, data, size=0):
            super().feed_data(data, size)
            if self._size > self._limit:
                if not self._protocol._reading_paused:
                    self._protocol.pause_reading()

        async def read(self):
            try:
                return await super().read()
            finally:
                if self._size < self._limit:
                    if self._protocol._reading_paused:
                        self._protocol.resume_reading()