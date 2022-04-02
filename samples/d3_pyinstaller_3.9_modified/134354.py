# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_server.py
"""Low level HTTP server."""
import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Optional
from .abc import AbstractStreamWriter
from .helpers import get_running_loop
from .http_parser import RawRequestMessage
from .streams import StreamReader
from .web_protocol import RequestHandler, _RequestFactory, _RequestHandler
from .web_request import BaseRequest
__all__ = ('Server', )

class Server:

    def __init__(self, handler: _RequestHandler, *, request_factory: Optional[_RequestFactory]=None, loop: Optional[asyncio.AbstractEventLoop]=None, **kwargs: Any) -> None:
        self._loop = get_running_loop(loop)
        self._connections = {}
        self._kwargs = kwargs
        self.requests_count = 0
        self.request_handler = handler
        self.request_factory = request_factory or self._make_request

    @property
    def connections(self) -> List[RequestHandler]:
        return list(self._connections.keys())

    def connection_made(self, handler: RequestHandler, transport: asyncio.Transport) -> None:
        self._connections[handler] = transport

    def connection_lost--- This code section failed: ---

 L.  43         0  LOAD_FAST                'handler'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _connections
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  44        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _connections
               14  LOAD_FAST                'handler'
               16  DELETE_SUBSCR    
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def _make_request(self, message: RawRequestMessage, payload: StreamReader, protocol: RequestHandler, writer: AbstractStreamWriter, task: 'asyncio.Task[None]') -> BaseRequest:
        return BaseRequest(message, payload, protocol, writer, task, self._loop)

    async def shutdown(self, timeout: Optional[float]=None) -> None:
        coros = [conn.shutdown(timeout) for conn in self._connections]
        await (asyncio.gather)(*coros)
        self._connections.clear()

    def __call__--- This code section failed: ---

 L.  62         0  LOAD_GLOBAL              RequestHandler
                2  LOAD_FAST                'self'
                4  BUILD_TUPLE_1         1 
                6  LOAD_STR                 'loop'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _loop
               12  BUILD_MAP_1           1 
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _kwargs
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1