# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_routedef.py
import abc, os
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Iterator, List, Optional, Sequence, Type, Union, overload
import attr
from . import hdrs
from .abc import AbstractView
from .typedefs import PathLike
if TYPE_CHECKING:
    from .web_request import Request
    from .web_response import StreamResponse
    from .web_urldispatcher import AbstractRoute, UrlDispatcher
else:
    Request = StreamResponse = UrlDispatcher = AbstractRoute = None
__all__ = ('AbstractRouteDef', 'RouteDef', 'StaticDef', 'RouteTableDef', 'head', 'options',
           'get', 'post', 'patch', 'put', 'delete', 'route', 'view', 'static')

class AbstractRouteDef(abc.ABC):

    @abc.abstractmethod
    def register(self, router: UrlDispatcher) -> List[AbstractRoute]:
        pass


_SimpleHandler = Callable[([Request], Awaitable[StreamResponse])]
_HandlerType = Union[(Type[AbstractView], _SimpleHandler)]

@attr.s(auto_attribs=True, frozen=True, repr=False, slots=True)
class RouteDef(AbstractRouteDef):
    method: str
    path: str
    handler: _HandlerType
    kwargs: Dict[(str, Any)]

    def __repr__(self) -> str:
        info = []
        for name, value in sorted(self.kwargs.items()):
            info.append(f", {name}={value!r}")
        else:
            return '<RouteDef {method} {path} -> {handler.__name__!r}{info}>'.format(method=(self.method),
              path=(self.path),
              handler=(self.handler),
              info=(''.join(info)))

    def register--- This code section failed: ---

 L.  76         0  LOAD_FAST                'self'
                2  LOAD_ATTR                method
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_ALL
                8  <118>                 0  ''
               10  POP_JUMP_IF_FALSE    58  'to 58'

 L.  77        12  LOAD_GLOBAL              getattr
               14  LOAD_FAST                'router'
               16  LOAD_STR                 'add_'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                method
               22  LOAD_METHOD              lower
               24  CALL_METHOD_0         0  ''
               26  BINARY_ADD       
               28  CALL_FUNCTION_2       2  ''
               30  STORE_FAST               'reg'

 L.  78        32  LOAD_FAST                'reg'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                path
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                handler
               42  BUILD_TUPLE_2         2 
               44  BUILD_MAP_0           0 
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                kwargs
               50  <164>                 1  ''
               52  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               54  BUILD_LIST_1          1 
               56  RETURN_VALUE     
             58_0  COME_FROM            10  '10'

 L.  81        58  LOAD_FAST                'router'
               60  LOAD_ATTR                add_route
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                method
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                path
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                handler
               74  BUILD_TUPLE_3         3 
               76  BUILD_MAP_0           0 
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                kwargs
               82  <164>                 1  ''
               84  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L.  80        86  BUILD_LIST_1          1 
               88  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


@attr.s(auto_attribs=True, frozen=True, repr=False, slots=True)
class StaticDef(AbstractRouteDef):
    prefix: str
    path: PathLike
    kwargs: Dict[(str, Any)]

    def __repr__(self) -> str:
        info = []
        for name, value in sorted(self.kwargs.items()):
            info.append(f", {name}={value!r}")
        else:
            return '<StaticDef {prefix} -> {path}{info}>'.format(prefix=(self.prefix),
              path=(self.path),
              info=(''.join(info)))

    def register--- This code section failed: ---

 L. 100         0  LOAD_FAST                'router'
                2  LOAD_ATTR                add_static
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                prefix
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                path
               12  BUILD_TUPLE_2         2 
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                kwargs
               20  <164>                 1  ''
               22  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               24  STORE_FAST               'resource'

 L. 101        26  LOAD_FAST                'resource'
               28  LOAD_METHOD              get_info
               30  CALL_METHOD_0         0  ''
               32  LOAD_METHOD              get
               34  LOAD_STR                 'routes'
               36  BUILD_MAP_0           0 
               38  CALL_METHOD_2         2  ''
               40  STORE_FAST               'routes'

 L. 102        42  LOAD_GLOBAL              list
               44  LOAD_FAST                'routes'
               46  LOAD_METHOD              values
               48  CALL_METHOD_0         0  ''
               50  CALL_FUNCTION_1       1  ''
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def route(method: str, path: str, handler: _HandlerType, **kwargs: Any) -> RouteDef:
    return RouteDef(method, path, handler, kwargs)


def head--- This code section failed: ---

 L. 110         0  LOAD_GLOBAL              route
                2  LOAD_GLOBAL              hdrs
                4  LOAD_ATTR                METH_HEAD
                6  LOAD_FAST                'path'
                8  LOAD_FAST                'handler'
               10  BUILD_TUPLE_3         3 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def options--- This code section failed: ---

 L. 114         0  LOAD_GLOBAL              route
                2  LOAD_GLOBAL              hdrs
                4  LOAD_ATTR                METH_OPTIONS
                6  LOAD_FAST                'path'
                8  LOAD_FAST                'handler'
               10  BUILD_TUPLE_3         3 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def get--- This code section failed: ---

 L. 125         0  LOAD_GLOBAL              route

 L. 126         2  LOAD_GLOBAL              hdrs
                4  LOAD_ATTR                METH_GET
                6  LOAD_FAST                'path'
                8  LOAD_FAST                'handler'

 L. 125        10  BUILD_TUPLE_3         3 

 L. 126        12  LOAD_FAST                'name'
               14  LOAD_FAST                'allow_head'

 L. 125        16  LOAD_CONST               ('name', 'allow_head')
               18  BUILD_CONST_KEY_MAP_2     2 

 L. 126        20  LOAD_FAST                'kwargs'

 L. 125        22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22


def post--- This code section failed: ---

 L. 131         0  LOAD_GLOBAL              route
                2  LOAD_GLOBAL              hdrs
                4  LOAD_ATTR                METH_POST
                6  LOAD_FAST                'path'
                8  LOAD_FAST                'handler'
               10  BUILD_TUPLE_3         3 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def put--- This code section failed: ---

 L. 135         0  LOAD_GLOBAL              route
                2  LOAD_GLOBAL              hdrs
                4  LOAD_ATTR                METH_PUT
                6  LOAD_FAST                'path'
                8  LOAD_FAST                'handler'
               10  BUILD_TUPLE_3         3 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def patch--- This code section failed: ---

 L. 139         0  LOAD_GLOBAL              route
                2  LOAD_GLOBAL              hdrs
                4  LOAD_ATTR                METH_PATCH
                6  LOAD_FAST                'path'
                8  LOAD_FAST                'handler'
               10  BUILD_TUPLE_3         3 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def delete--- This code section failed: ---

 L. 143         0  LOAD_GLOBAL              route
                2  LOAD_GLOBAL              hdrs
                4  LOAD_ATTR                METH_DELETE
                6  LOAD_FAST                'path'
                8  LOAD_FAST                'handler'
               10  BUILD_TUPLE_3         3 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def view--- This code section failed: ---

 L. 147         0  LOAD_GLOBAL              route
                2  LOAD_GLOBAL              hdrs
                4  LOAD_ATTR                METH_ANY
                6  LOAD_FAST                'path'
                8  LOAD_FAST                'handler'
               10  BUILD_TUPLE_3         3 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def static(prefix: str, path: PathLike, **kwargs: Any) -> StaticDef:
    return StaticDef(prefix, path, kwargs)


_Deco = Callable[([_HandlerType], _HandlerType)]

class RouteTableDef(Sequence[AbstractRouteDef]):
    __doc__ = 'Route definition table'

    def __init__(self) -> None:
        self._items = []

    def __repr__(self) -> str:
        return '<RouteTableDef count={}>'.format(len(self._items))

    @overload
    def __getitem__(self, index: int) -> AbstractRouteDef:
        pass

    @overload
    def __getitem__(self, index: slice) -> List[AbstractRouteDef]:
        pass

    def __getitem__(self, index):
        return self._items[index]

    def __iter__(self) -> Iterator[AbstractRouteDef]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__--- This code section failed: ---

 L. 184         0  LOAD_FAST                'item'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _items
                6  <118>                 0  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def route(self, method: str, path: str, **kwargs: Any) -> _Deco:

        def inner(handler):
            self._items.append(RouteDef(method, path, handler, kwargs))
            return handler

        return inner

    def head--- This code section failed: ---

 L. 194         0  LOAD_FAST                'self'
                2  LOAD_ATTR                route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_HEAD
                8  LOAD_FAST                'path'
               10  BUILD_TUPLE_2         2 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def get--- This code section failed: ---

 L. 197         0  LOAD_FAST                'self'
                2  LOAD_ATTR                route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_GET
                8  LOAD_FAST                'path'
               10  BUILD_TUPLE_2         2 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def post--- This code section failed: ---

 L. 200         0  LOAD_FAST                'self'
                2  LOAD_ATTR                route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_POST
                8  LOAD_FAST                'path'
               10  BUILD_TUPLE_2         2 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def put--- This code section failed: ---

 L. 203         0  LOAD_FAST                'self'
                2  LOAD_ATTR                route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_PUT
                8  LOAD_FAST                'path'
               10  BUILD_TUPLE_2         2 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def patch--- This code section failed: ---

 L. 206         0  LOAD_FAST                'self'
                2  LOAD_ATTR                route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_PATCH
                8  LOAD_FAST                'path'
               10  BUILD_TUPLE_2         2 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def delete--- This code section failed: ---

 L. 209         0  LOAD_FAST                'self'
                2  LOAD_ATTR                route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_DELETE
                8  LOAD_FAST                'path'
               10  BUILD_TUPLE_2         2 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def view--- This code section failed: ---

 L. 212         0  LOAD_FAST                'self'
                2  LOAD_ATTR                route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_ANY
                8  LOAD_FAST                'path'
               10  BUILD_TUPLE_2         2 
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def static(self, prefix: str, path: PathLike, **kwargs: Any) -> None:
        self._items.append(StaticDef(prefix, path, kwargs))