# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\payload_streamer.py
""" Payload implemenation for coroutines as data provider.

As a simple case, you can upload data from file::

   @aiohttp.streamer
   async def file_sender(writer, file_name=None):
      with open(file_name, 'rb') as f:
          chunk = f.read(2**16)
          while chunk:
              await writer.write(chunk)

              chunk = f.read(2**16)

Then you can use `file_sender` like this:

    async with session.post('http://httpbin.org/post',
                            data=file_sender(file_name='huge_file')) as resp:
        print(await resp.text())

..note:: Coroutine must accept `writer` as first argument

"""
import types, warnings
from typing import Any, Awaitable, Callable, Dict, Tuple
from .abc import AbstractStreamWriter
from .payload import Payload, payload_type
__all__ = ('streamer', )

class _stream_wrapper:

    def __init__(self, coro: Callable[(..., Awaitable[None])], args: Tuple[(Any, ...)], kwargs: Dict[(str, Any)]) -> None:
        self.coro = types.coroutine(coro)
        self.args = args
        self.kwargs = kwargs

    async def __call__--- This code section failed: ---

 L.  46         0  LOAD_FAST                'self'
                2  LOAD_ATTR                coro
                4  LOAD_FAST                'writer'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                args
               12  CALL_FINALLY         15  'to 15'
               14  WITH_CLEANUP_FINISH
               16  BUILD_MAP_0           0 
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                kwargs
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  POP_TOP          

Parse error at or near `None' instruction at offset -1


class streamer:

    def __init__(self, coro: Callable[(..., Awaitable[None])]) -> None:
        warnings.warn('@streamer is deprecated, use async generators instead',
          DeprecationWarning,
          stacklevel=2)
        self.coro = coro

    def __call__(self, *args: Any, **kwargs: Any) -> _stream_wrapper:
        return _stream_wrapper(self.coro, args, kwargs)


@payload_type(_stream_wrapper)
class StreamWrapperPayload(Payload):

    async def write(self, writer: AbstractStreamWriter) -> None:
        await self._value(writer)


@payload_type(streamer)
class StreamPayload(StreamWrapperPayload):

    def __init__--- This code section failed: ---

 L.  71         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'value'
                8  CALL_FUNCTION_0       0  ''
               10  BUILD_LIST_1          1 
               12  LOAD_FAST                'args'
               14  CALL_FINALLY         17  'to 17'
               16  WITH_CLEANUP_FINISH
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  POP_TOP          

Parse error at or near `None' instruction at offset -1

    async def write(self, writer: AbstractStreamWriter) -> None:
        await self._value(writer)