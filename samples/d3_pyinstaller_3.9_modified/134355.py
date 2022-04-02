# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_urldispatcher.py
import abc, asyncio, base64, hashlib, inspect, keyword, os, re, warnings
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Container, Dict, Generator, Iterable, Iterator, List, Mapping, Optional, Pattern, Set, Sized, Tuple, Type, Union, cast
from typing_extensions import TypedDict
from yarl import URL, __version__ as yarl_version
from . import hdrs
from .abc import AbstractMatchInfo, AbstractRouter, AbstractView
from .helpers import DEBUG
from .http import HttpVersion11
from .typedefs import PathLike
from .web_exceptions import HTTPException, HTTPExpectationFailed, HTTPForbidden, HTTPMethodNotAllowed, HTTPNotFound
from .web_fileresponse import FileResponse
from .web_request import Request
from .web_response import Response, StreamResponse
from .web_routedef import AbstractRouteDef
__all__ = ('UrlDispatcher', 'UrlMappingMatchInfo', 'AbstractResource', 'Resource',
           'PlainResource', 'DynamicResource', 'AbstractRoute', 'ResourceRoute',
           'StaticResource', 'View')
if TYPE_CHECKING:
    from .web_app import Application
    BaseDict = Dict[(str, str)]
else:
    BaseDict = dict
YARL_VERSION = tuple(map(int, yarl_version.split('.')[:2]))
HTTP_METHOD_RE = re.compile("^[0-9A-Za-z!#\\$%&'\\*\\+\\-\\.\\^_`\\|~]+$")
ROUTE_RE = re.compile('(\\{[_a-zA-Z][^{}]*(?:\\{[^{}]*\\}[^{}]*)*\\})')
PATH_SEP = re.escape('/')
_WebHandler = Callable[([Request], Awaitable[StreamResponse])]
_ExpectHandler = Callable[([Request], Awaitable[None])]
_Resolve = Tuple[(Optional[AbstractMatchInfo], Set[str])]

class _InfoDict(TypedDict, total=False):
    path: str
    formatter: str
    pattern: Pattern[str]
    directory: Path
    prefix: str
    routes: Mapping[(str, 'AbstractRoute')]
    app: 'Application'
    domain: str
    rule: 'AbstractRuleMatching'
    http_exception: HTTPException


class AbstractResource(Sized, Iterable['AbstractRoute']):

    def __init__(self, *, name: Optional[str]=None) -> None:
        self._name = name

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    @abc.abstractmethod
    def canonical(self) -> str:
        """Exposes the resource's canonical path.

        For example '/foo/bar/{name}'

        """
        pass

    @abc.abstractmethod
    def url_for(self, **kwargs: str) -> URL:
        """Construct url for resource with additional params."""
        pass

    @abc.abstractmethod
    async def resolve(self, request: Request) -> _Resolve:
        """Resolve resource

        Return (UrlMappingMatchInfo, allowed_methods) pair."""
        pass

    @abc.abstractmethod
    def add_prefix(self, prefix: str) -> None:
        """Add a prefix to processed URLs.

        Required for subapplications support.

        """
        pass

    @abc.abstractmethod
    def get_info(self) -> _InfoDict:
        """Return a dict with additional info useful for introspection"""
        pass

    def freeze(self) -> None:
        pass

    @abc.abstractmethod
    def raw_match(self, path: str) -> bool:
        """Perform a raw match against path"""
        pass


class AbstractRoute(abc.ABC):

    def __init__--- This code section failed: ---

 L. 165         0  LOAD_FAST                'expect_handler'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 166         8  LOAD_GLOBAL              _default_expect_handler
               10  STORE_FAST               'expect_handler'
             12_0  COME_FROM             6  '6'

 L. 168        12  LOAD_GLOBAL              asyncio
               14  LOAD_METHOD              iscoroutinefunction

 L. 169        16  LOAD_FAST                'expect_handler'

 L. 168        18  CALL_METHOD_1         1  ''
               20  POP_JUMP_IF_TRUE     36  'to 36'
               22  <74>             

 L. 170        24  LOAD_STR                 'Coroutine is expected, got '
               26  LOAD_FAST                'expect_handler'
               28  FORMAT_VALUE          2  '!r'
               30  BUILD_STRING_2        2 

 L. 168        32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            20  '20'

 L. 172        36  LOAD_FAST                'method'
               38  LOAD_METHOD              upper
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'method'

 L. 173        44  LOAD_GLOBAL              HTTP_METHOD_RE
               46  LOAD_METHOD              match
               48  LOAD_FAST                'method'
               50  CALL_METHOD_1         1  ''
               52  POP_JUMP_IF_TRUE     68  'to 68'

 L. 174        54  LOAD_GLOBAL              ValueError
               56  LOAD_FAST                'method'
               58  FORMAT_VALUE          0  ''
               60  LOAD_STR                 ' is not allowed HTTP method'
               62  BUILD_STRING_2        2 
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            52  '52'

 L. 176        68  LOAD_GLOBAL              callable
               70  LOAD_FAST                'handler'
               72  CALL_FUNCTION_1       1  ''
               74  POP_JUMP_IF_TRUE     84  'to 84'
               76  <74>             
               78  LOAD_FAST                'handler'
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            74  '74'

 L. 177        84  LOAD_GLOBAL              asyncio
               86  LOAD_METHOD              iscoroutinefunction
               88  LOAD_FAST                'handler'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE    96  'to 96'

 L. 178        94  JUMP_FORWARD        190  'to 190'
             96_0  COME_FROM            92  '92'

 L. 179        96  LOAD_GLOBAL              inspect
               98  LOAD_METHOD              isgeneratorfunction
              100  LOAD_FAST                'handler'
              102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_FALSE   120  'to 120'

 L. 180       106  LOAD_GLOBAL              warnings
              108  LOAD_METHOD              warn

 L. 181       110  LOAD_STR                 'Bare generators are deprecated, use @coroutine wrapper'

 L. 182       112  LOAD_GLOBAL              DeprecationWarning

 L. 180       114  CALL_METHOD_2         2  ''
              116  POP_TOP          
              118  JUMP_FORWARD        190  'to 190'
            120_0  COME_FROM           104  '104'

 L. 184       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'handler'
              124  LOAD_GLOBAL              type
              126  CALL_FUNCTION_2       2  ''
              128  POP_JUMP_IF_FALSE   142  'to 142'
              130  LOAD_GLOBAL              issubclass
              132  LOAD_FAST                'handler'
              134  LOAD_GLOBAL              AbstractView
              136  CALL_FUNCTION_2       2  ''
              138  POP_JUMP_IF_FALSE   142  'to 142'

 L. 185       140  JUMP_FORWARD        190  'to 190'
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM           128  '128'

 L. 187       142  LOAD_GLOBAL              warnings
              144  LOAD_METHOD              warn

 L. 188       146  LOAD_STR                 'Bare functions are deprecated, use async ones'
              148  LOAD_GLOBAL              DeprecationWarning

 L. 187       150  CALL_METHOD_2         2  ''
              152  POP_TOP          

 L. 191       154  LOAD_GLOBAL              wraps
              156  LOAD_FAST                'handler'
              158  CALL_FUNCTION_1       1  ''

 L. 192       160  LOAD_GLOBAL              Request
              162  LOAD_GLOBAL              StreamResponse
              164  LOAD_CONST               ('request', 'return')
              166  BUILD_CONST_KEY_MAP_2     2 
              168  LOAD_CLOSURE             'old_handler'
              170  BUILD_TUPLE_1         1 
              172  LOAD_CODE                <code_object handler_wrapper>
              174  LOAD_STR                 'AbstractRoute.__init__.<locals>.handler_wrapper'
              176  MAKE_FUNCTION_12         'annotation, closure'
              178  CALL_FUNCTION_1       1  ''
              180  STORE_FAST               'handler_wrapper'

 L. 198       182  LOAD_FAST                'handler'
              184  STORE_DEREF              'old_handler'

 L. 199       186  LOAD_FAST                'handler_wrapper'
              188  STORE_FAST               'handler'
            190_0  COME_FROM           140  '140'
            190_1  COME_FROM           118  '118'
            190_2  COME_FROM            94  '94'

 L. 201       190  LOAD_FAST                'method'
              192  LOAD_FAST                'self'
              194  STORE_ATTR               _method

 L. 202       196  LOAD_FAST                'handler'
              198  LOAD_FAST                'self'
              200  STORE_ATTR               _handler

 L. 203       202  LOAD_FAST                'expect_handler'
              204  LOAD_FAST                'self'
              206  STORE_ATTR               _expect_handler

 L. 204       208  LOAD_FAST                'resource'
              210  LOAD_FAST                'self'
              212  STORE_ATTR               _resource

Parse error at or near `None' instruction at offset -1

    @property
    def method(self) -> str:
        return self._method

    @property
    def handler(self) -> _WebHandler:
        return self._handler

    @property
    @abc.abstractmethod
    def name(self) -> Optional[str]:
        """Optional route's name, always equals to resource's name."""
        pass

    @property
    def resource(self) -> Optional[AbstractResource]:
        return self._resource

    @abc.abstractmethod
    def get_info(self) -> _InfoDict:
        """Return a dict with additional info useful for introspection"""
        pass

    @abc.abstractmethod
    def url_for(self, *args: str, **kwargs: str) -> URL:
        """Construct url for route with additional params."""
        pass

    async def handle_expect_header(self, request: Request) -> None:
        await self._expect_handler(request)


class UrlMappingMatchInfo(BaseDict, AbstractMatchInfo):

    def __init__(self, match_dict, route):
        super().__init__(match_dict)
        self._route = route
        self._apps = []
        self._current_app = None
        self._frozen = False

    @property
    def handler(self) -> _WebHandler:
        return self._route.handler

    @property
    def route(self) -> AbstractRoute:
        return self._route

    @property
    def expect_handler(self) -> _ExpectHandler:
        return self._route.handle_expect_header

    @property
    def http_exception(self) -> Optional[HTTPException]:
        pass

    def get_info(self) -> _InfoDict:
        return self._route.get_info

    @property
    def apps(self) -> Tuple[('Application', Ellipsis)]:
        return tuple(self._apps)

    def add_app--- This code section failed: ---

 L. 267         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _frozen
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 268         6  LOAD_GLOBAL              RuntimeError
                8  LOAD_STR                 'Cannot change apps stack after .freeze() call'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 269        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _current_app
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 270        24  LOAD_FAST                'app'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _current_app
             30_0  COME_FROM            22  '22'

 L. 271        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _apps
               34  LOAD_METHOD              insert
               36  LOAD_CONST               0
               38  LOAD_FAST                'app'
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          

Parse error at or near `<117>' instruction at offset 20

    @property
    def current_app--- This code section failed: ---

 L. 275         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _current_app
                4  STORE_FAST               'app'

 L. 276         6  LOAD_FAST                'app'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L. 277        18  LOAD_FAST                'app'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    @contextmanager
    def set_current_app--- This code section failed: ---

 L. 281         0  LOAD_GLOBAL              DEBUG
                2  POP_JUMP_IF_FALSE    32  'to 32'

 L. 282         4  LOAD_FAST                'app'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _apps
               10  <118>                 1  ''
               12  POP_JUMP_IF_FALSE    32  'to 32'

 L. 283        14  LOAD_GLOBAL              RuntimeError

 L. 284        16  LOAD_STR                 'Expected one of the following apps {!r}, got {!r}'
               18  LOAD_METHOD              format

 L. 285        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _apps
               24  LOAD_FAST                'app'

 L. 284        26  CALL_METHOD_2         2  ''

 L. 283        28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            12  '12'
             32_1  COME_FROM             2  '2'

 L. 288        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _current_app
               36  STORE_FAST               'prev'

 L. 289        38  LOAD_FAST                'app'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _current_app

 L. 290        44  SETUP_FINALLY        62  'to 62'

 L. 291        46  LOAD_CONST               None
               48  YIELD_VALUE      
               50  POP_TOP          
               52  POP_BLOCK        

 L. 293        54  LOAD_FAST                'prev'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _current_app
               60  JUMP_FORWARD         70  'to 70'
             62_0  COME_FROM_FINALLY    44  '44'
               62  LOAD_FAST                'prev'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _current_app
               68  <48>             
             70_0  COME_FROM            60  '60'

Parse error at or near `<118>' instruction at offset 10

    def freeze(self) -> None:
        self._frozen = True

    def __repr__(self):
        return f"<MatchInfo {super().__repr__}: {self._route}>"


class MatchInfoError(UrlMappingMatchInfo):

    def __init__(self, http_exception):
        self._exception = http_exception
        super().__init__{}SystemRoute(self._exception)

    @property
    def http_exception(self) -> HTTPException:
        return self._exception

    def __repr__(self) -> str:
        return '<MatchInfoError {}: {}>'.formatself._exception.statusself._exception.reason


async def _default_expect_handler(request: Request) -> None:
    """Default handler for Expect header.

    Just send "100 Continue" to client.
    raise HTTPExpectationFailed if value of header is not "100-continue"
    """
    expect = request.headers.gethdrs.EXPECT''
    if request.version == HttpVersion11:
        if expect.lower == '100-continue':
            await request.writer.write(b'HTTP/1.1 100 Continue\r\n\r\n')
        else:
            raise HTTPExpectationFailed(text=('Unknown Expect: %s' % expect))


class Resource(AbstractResource):

    def __init__(self, *, name=None):
        super().__init__(name=name)
        self._routes = []

    def add_route(self, method: str, handler: Union[(Type[AbstractView], _WebHandler)], *, expect_handler: Optional[_ExpectHandler]=None) -> 'ResourceRoute':
        for route_obj in self._routes:
            if not route_obj.method == method:
                if route_obj.method == hdrs.METH_ANY:
                    pass
            raise RuntimeError('Added route will never be executed, method {route.method} is already registered'.format(route=route_obj))
        else:
            route_obj = ResourceRoute(method, handler, self, expect_handler=expect_handler)
            self.register_route(route_obj)
            return route_obj

    def register_route--- This code section failed: ---

 L. 357         0  LOAD_GLOBAL              isinstance

 L. 358         2  LOAD_FAST                'route'
                4  LOAD_GLOBAL              ResourceRoute

 L. 357         6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     24  'to 24'
               10  <74>             

 L. 359        12  LOAD_STR                 'Instance of Route class is required, got '
               14  LOAD_FAST                'route'
               16  FORMAT_VALUE          2  '!r'
               18  BUILD_STRING_2        2 

 L. 357        20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM             8  '8'

 L. 360        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _routes
               28  LOAD_METHOD              append
               30  LOAD_FAST                'route'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

Parse error at or near `<74>' instruction at offset 10

    async def resolve--- This code section failed: ---

 L. 363         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'allowed_methods'

 L. 365         6  LOAD_FAST                'self'
                8  LOAD_METHOD              _match
               10  LOAD_FAST                'request'
               12  LOAD_ATTR                rel_url
               14  LOAD_ATTR                raw_path
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'match_dict'

 L. 366        20  LOAD_FAST                'match_dict'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 367        28  LOAD_CONST               None
               30  LOAD_FAST                'allowed_methods'
               32  BUILD_TUPLE_2         2 
               34  RETURN_VALUE     
             36_0  COME_FROM            26  '26'

 L. 369        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _routes
               40  GET_ITER         
             42_0  COME_FROM           100  '100'
             42_1  COME_FROM            80  '80'
               42  FOR_ITER            102  'to 102'
               44  STORE_FAST               'route_obj'

 L. 370        46  LOAD_FAST                'route_obj'
               48  LOAD_ATTR                method
               50  STORE_FAST               'route_method'

 L. 371        52  LOAD_FAST                'allowed_methods'
               54  LOAD_METHOD              add
               56  LOAD_FAST                'route_method'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 373        62  LOAD_FAST                'route_method'
               64  LOAD_FAST                'request'
               66  LOAD_ATTR                method
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_TRUE     82  'to 82'
               72  LOAD_FAST                'route_method'
               74  LOAD_GLOBAL              hdrs
               76  LOAD_ATTR                METH_ANY
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE_BACK    42  'to 42'
             82_0  COME_FROM            70  '70'

 L. 374        82  LOAD_GLOBAL              UrlMappingMatchInfo
               84  LOAD_FAST                'match_dict'
               86  LOAD_FAST                'route_obj'
               88  CALL_FUNCTION_2       2  ''
               90  LOAD_FAST                'allowed_methods'
               92  BUILD_TUPLE_2         2 
               94  ROT_TWO          
               96  POP_TOP          
               98  RETURN_VALUE     
              100  JUMP_BACK            42  'to 42'
            102_0  COME_FROM            42  '42'

 L. 376       102  LOAD_CONST               None
              104  LOAD_FAST                'allowed_methods'
              106  BUILD_TUPLE_2         2 
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    @abc.abstractmethod
    def _match(self, path: str) -> Optional[Dict[(str, str)]]:
        pass

    def __len__(self) -> int:
        return len(self._routes)

    def __iter__(self) -> Iterator[AbstractRoute]:
        return iter(self._routes)


class PlainResource(Resource):

    def __init__--- This code section failed: ---

 L. 393         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'name'
                8  LOAD_CONST               ('name',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_TOP          

 L. 394        14  LOAD_FAST                'path'
               16  POP_JUMP_IF_FALSE    32  'to 32'
               18  LOAD_FAST                'path'
               20  LOAD_METHOD              startswith
               22  LOAD_STR                 '/'
               24  CALL_METHOD_1         1  ''
               26  POP_JUMP_IF_TRUE     32  'to 32'
               28  <74>             
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            26  '26'
             32_1  COME_FROM            16  '16'

 L. 395        32  LOAD_FAST                'path'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _path

Parse error at or near `<74>' instruction at offset 28

    @property
    def canonical(self) -> str:
        return self._path

    def freeze(self) -> None:
        if not self._path:
            self._path = '/'

    def add_prefix--- This code section failed: ---

 L. 406         0  LOAD_FAST                'prefix'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 407        14  LOAD_FAST                'prefix'
               16  LOAD_METHOD              endswith
               18  LOAD_STR                 '/'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 408        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'prefix'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               1
               36  COMPARE_OP               >
               38  POP_JUMP_IF_TRUE     44  'to 44'
               40  <74>             
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            38  '38'

 L. 409        44  LOAD_FAST                'prefix'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _path
               50  BINARY_ADD       
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _path

Parse error at or near `None' instruction at offset -1

    def _match(self, path: str) -> Optional[Dict[(str, str)]]:
        if self._path == path:
            return {}
        return

    def raw_match(self, path: str) -> bool:
        return self._path == path

    def get_info(self) -> _InfoDict:
        return {'path': self._path}

    def url_for(self) -> URL:
        return URL.build(path=(self._path), encoded=True)

    def __repr__--- This code section failed: ---

 L. 428         0  LOAD_FAST                'self'
                2  LOAD_ATTR                name
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'
               10  LOAD_STR                 "'"
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                name
               16  BINARY_ADD       
               18  LOAD_STR                 "' "
               20  BINARY_ADD       
               22  JUMP_FORWARD         26  'to 26'
             24_0  COME_FROM             8  '8'
               24  LOAD_STR                 ''
             26_0  COME_FROM            22  '22'
               26  STORE_FAST               'name'

 L. 429        28  LOAD_STR                 '<PlainResource '
               30  LOAD_FAST                'name'
               32  FORMAT_VALUE          0  ''
               34  LOAD_STR                 ' '
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _path
               40  FORMAT_VALUE          0  ''
               42  LOAD_STR                 '>'
               44  BUILD_STRING_5        5 
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class DynamicResource(Resource):
    DYN = re.compile('\\{(?P<var>[_a-zA-Z][_a-zA-Z0-9]*)\\}')
    DYN_WITH_RE = re.compile('\\{(?P<var>[_a-zA-Z][_a-zA-Z0-9]*):(?P<re>.+)\\}')
    GOOD = '[^{}/]+'

    def __init__--- This code section failed: ---

 L. 439         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'name'
                8  LOAD_CONST               ('name',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_TOP          

 L. 440        14  LOAD_STR                 ''
               16  STORE_FAST               'pattern'

 L. 441        18  LOAD_STR                 ''
               20  STORE_FAST               'formatter'

 L. 442        22  LOAD_GLOBAL              ROUTE_RE
               24  LOAD_METHOD              split
               26  LOAD_FAST                'path'
               28  CALL_METHOD_1         1  ''
               30  GET_ITER         
             32_0  COME_FROM           232  '232'
             32_1  COME_FROM           162  '162'
             32_2  COME_FROM            98  '98'
               32  FOR_ITER            234  'to 234'
               34  STORE_FAST               'part'

 L. 443        36  LOAD_FAST                'self'
               38  LOAD_ATTR                DYN
               40  LOAD_METHOD              fullmatch
               42  LOAD_FAST                'part'
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'match'

 L. 444        48  LOAD_FAST                'match'
               50  POP_JUMP_IF_FALSE   100  'to 100'

 L. 445        52  LOAD_FAST                'pattern'
               54  LOAD_STR                 '(?P<{}>{})'
               56  LOAD_METHOD              format
               58  LOAD_FAST                'match'
               60  LOAD_METHOD              group
               62  LOAD_STR                 'var'
               64  CALL_METHOD_1         1  ''
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                GOOD
               70  CALL_METHOD_2         2  ''
               72  INPLACE_ADD      
               74  STORE_FAST               'pattern'

 L. 446        76  LOAD_FAST                'formatter'
               78  LOAD_STR                 '{'
               80  LOAD_FAST                'match'
               82  LOAD_METHOD              group
               84  LOAD_STR                 'var'
               86  CALL_METHOD_1         1  ''
               88  BINARY_ADD       
               90  LOAD_STR                 '}'
               92  BINARY_ADD       
               94  INPLACE_ADD      
               96  STORE_FAST               'formatter'

 L. 447        98  JUMP_BACK            32  'to 32'
            100_0  COME_FROM            50  '50'

 L. 449       100  LOAD_FAST                'self'
              102  LOAD_ATTR                DYN_WITH_RE
              104  LOAD_METHOD              fullmatch
              106  LOAD_FAST                'part'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'match'

 L. 450       112  LOAD_FAST                'match'
              114  POP_JUMP_IF_FALSE   164  'to 164'

 L. 451       116  LOAD_FAST                'pattern'
              118  LOAD_STR                 '(?P<{var}>{re})'
              120  LOAD_ATTR                format
              122  BUILD_TUPLE_0         0 
              124  BUILD_MAP_0           0 
              126  LOAD_FAST                'match'
              128  LOAD_METHOD              groupdict
              130  CALL_METHOD_0         0  ''
              132  <164>                 1  ''
              134  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              136  INPLACE_ADD      
              138  STORE_FAST               'pattern'

 L. 452       140  LOAD_FAST                'formatter'
              142  LOAD_STR                 '{'
              144  LOAD_FAST                'match'
              146  LOAD_METHOD              group
              148  LOAD_STR                 'var'
              150  CALL_METHOD_1         1  ''
              152  BINARY_ADD       
              154  LOAD_STR                 '}'
              156  BINARY_ADD       
              158  INPLACE_ADD      
              160  STORE_FAST               'formatter'

 L. 453       162  JUMP_BACK            32  'to 32'
            164_0  COME_FROM           114  '114'

 L. 455       164  LOAD_STR                 '{'
              166  LOAD_FAST                'part'
              168  <118>                 0  ''
              170  POP_JUMP_IF_TRUE    180  'to 180'
              172  LOAD_STR                 '}'
              174  LOAD_FAST                'part'
              176  <118>                 0  ''
              178  POP_JUMP_IF_FALSE   202  'to 202'
            180_0  COME_FROM           170  '170'

 L. 456       180  LOAD_GLOBAL              ValueError
              182  LOAD_STR                 "Invalid path '"
              184  LOAD_FAST                'path'
              186  FORMAT_VALUE          0  ''
              188  LOAD_STR                 "'['"
              190  LOAD_FAST                'part'
              192  FORMAT_VALUE          0  ''
              194  LOAD_STR                 "']"
              196  BUILD_STRING_5        5 
              198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  'exception instance'
            202_0  COME_FROM           178  '178'

 L. 458       202  LOAD_GLOBAL              _requote_path
              204  LOAD_FAST                'part'
              206  CALL_FUNCTION_1       1  ''
              208  STORE_FAST               'part'

 L. 459       210  LOAD_FAST                'formatter'
              212  LOAD_FAST                'part'
              214  INPLACE_ADD      
              216  STORE_FAST               'formatter'

 L. 460       218  LOAD_FAST                'pattern'
              220  LOAD_GLOBAL              re
              222  LOAD_METHOD              escape
              224  LOAD_FAST                'part'
              226  CALL_METHOD_1         1  ''
              228  INPLACE_ADD      
              230  STORE_FAST               'pattern'
              232  JUMP_BACK            32  'to 32'
            234_0  COME_FROM            32  '32'

 L. 462       234  SETUP_FINALLY       250  'to 250'

 L. 463       236  LOAD_GLOBAL              re
              238  LOAD_METHOD              compile
              240  LOAD_FAST                'pattern'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'compiled'
              246  POP_BLOCK        
              248  JUMP_FORWARD        312  'to 312'
            250_0  COME_FROM_FINALLY   234  '234'

 L. 464       250  DUP_TOP          
              252  LOAD_GLOBAL              re
              254  LOAD_ATTR                error
          256_258  <121>               310  ''
              260  POP_TOP          
              262  STORE_FAST               'exc'
              264  POP_TOP          
              266  SETUP_FINALLY       302  'to 302'

 L. 465       268  LOAD_GLOBAL              ValueError
              270  LOAD_STR                 "Bad pattern '"
              272  LOAD_FAST                'pattern'
              274  FORMAT_VALUE          0  ''
              276  LOAD_STR                 "': "
              278  LOAD_FAST                'exc'
              280  FORMAT_VALUE          0  ''
              282  BUILD_STRING_4        4 
              284  CALL_FUNCTION_1       1  ''
              286  LOAD_CONST               None
              288  RAISE_VARARGS_2       2  'exception instance with __cause__'
              290  POP_BLOCK        
              292  POP_EXCEPT       
              294  LOAD_CONST               None
              296  STORE_FAST               'exc'
              298  DELETE_FAST              'exc'
              300  JUMP_FORWARD        312  'to 312'
            302_0  COME_FROM_FINALLY   266  '266'
              302  LOAD_CONST               None
              304  STORE_FAST               'exc'
              306  DELETE_FAST              'exc'
              308  <48>             
              310  <48>             
            312_0  COME_FROM           300  '300'
            312_1  COME_FROM           248  '248'

 L. 466       312  LOAD_FAST                'compiled'
              314  LOAD_ATTR                pattern
              316  LOAD_METHOD              startswith
              318  LOAD_GLOBAL              PATH_SEP
              320  CALL_METHOD_1         1  ''
          322_324  POP_JUMP_IF_TRUE    330  'to 330'
              326  <74>             
              328  RAISE_VARARGS_1       1  'exception instance'
            330_0  COME_FROM           322  '322'

 L. 467       330  LOAD_FAST                'formatter'
              332  LOAD_METHOD              startswith
              334  LOAD_STR                 '/'
              336  CALL_METHOD_1         1  ''
          338_340  POP_JUMP_IF_TRUE    346  'to 346'
              342  <74>             
              344  RAISE_VARARGS_1       1  'exception instance'
            346_0  COME_FROM           338  '338'

 L. 468       346  LOAD_FAST                'compiled'
              348  LOAD_FAST                'self'
              350  STORE_ATTR               _pattern

 L. 469       352  LOAD_FAST                'formatter'
              354  LOAD_FAST                'self'
              356  STORE_ATTR               _formatter

Parse error at or near `<164>' instruction at offset 132

    @property
    def canonical(self) -> str:
        return self._formatter

    def add_prefix--- This code section failed: ---

 L. 476         0  LOAD_FAST                'prefix'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 477        14  LOAD_FAST                'prefix'
               16  LOAD_METHOD              endswith
               18  LOAD_STR                 '/'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 478        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'prefix'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               1
               36  COMPARE_OP               >
               38  POP_JUMP_IF_TRUE     44  'to 44'
               40  <74>             
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            38  '38'

 L. 479        44  LOAD_GLOBAL              re
               46  LOAD_METHOD              compile
               48  LOAD_GLOBAL              re
               50  LOAD_METHOD              escape
               52  LOAD_FAST                'prefix'
               54  CALL_METHOD_1         1  ''
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _pattern
               60  LOAD_ATTR                pattern
               62  BINARY_ADD       
               64  CALL_METHOD_1         1  ''
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _pattern

 L. 480        70  LOAD_FAST                'prefix'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _formatter
               76  BINARY_ADD       
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _formatter

Parse error at or near `None' instruction at offset -1

    def _match--- This code section failed: ---

 L. 483         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _pattern
                4  LOAD_METHOD              fullmatch
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'match'

 L. 484        12  LOAD_FAST                'match'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 485        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 487        24  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               26  LOAD_STR                 'DynamicResource._match.<locals>.<dictcomp>'
               28  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 488        30  LOAD_FAST                'match'
               32  LOAD_METHOD              groupdict
               34  CALL_METHOD_0         0  ''
               36  LOAD_METHOD              items
               38  CALL_METHOD_0         0  ''

 L. 487        40  GET_ITER         
               42  CALL_FUNCTION_1       1  ''
               44  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 16

    def raw_match(self, path: str) -> bool:
        return self._formatter == path

    def get_info(self) -> _InfoDict:
        return {'formatter':self._formatter, 
         'pattern':self._pattern}

    def url_for(self, **parts: str) -> URL:
        url = self._formatter.format_map({_quote_path(v):k for k, v in parts.items})
        return URL.build(path=url, encoded=True)

    def __repr__--- This code section failed: ---

 L. 502         0  LOAD_FAST                'self'
                2  LOAD_ATTR                name
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'
               10  LOAD_STR                 "'"
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                name
               16  BINARY_ADD       
               18  LOAD_STR                 "' "
               20  BINARY_ADD       
               22  JUMP_FORWARD         26  'to 26'
             24_0  COME_FROM             8  '8'
               24  LOAD_STR                 ''
             26_0  COME_FROM            22  '22'
               26  STORE_FAST               'name'

 L. 503        28  LOAD_STR                 '<DynamicResource {name} {formatter}>'
               30  LOAD_ATTR                format

 L. 504        32  LOAD_FAST                'name'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _formatter

 L. 503        38  LOAD_CONST               ('name', 'formatter')
               40  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class PrefixResource(AbstractResource):

    def __init__--- This code section failed: ---

 L. 510         0  LOAD_FAST                'prefix'
                2  POP_JUMP_IF_FALSE    22  'to 22'
                4  LOAD_FAST                'prefix'
                6  LOAD_METHOD              startswith
                8  LOAD_STR                 '/'
               10  CALL_METHOD_1         1  ''
               12  POP_JUMP_IF_TRUE     22  'to 22'
               14  <74>             
               16  LOAD_FAST                'prefix'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'
             22_1  COME_FROM             2  '2'

 L. 511        22  LOAD_FAST                'prefix'
               24  LOAD_CONST               ('', '/')
               26  <118>                 0  ''
               28  POP_JUMP_IF_TRUE     48  'to 48'
               30  LOAD_FAST                'prefix'
               32  LOAD_METHOD              endswith
               34  LOAD_STR                 '/'
               36  CALL_METHOD_1         1  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'
               40  <74>             
               42  LOAD_FAST                'prefix'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            28  '28'

 L. 512        48  LOAD_GLOBAL              super
               50  CALL_FUNCTION_0       0  ''
               52  LOAD_ATTR                __init__
               54  LOAD_FAST                'name'
               56  LOAD_CONST               ('name',)
               58  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               60  POP_TOP          

 L. 513        62  LOAD_GLOBAL              _requote_path
               64  LOAD_FAST                'prefix'
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_FAST                'self'
               70  STORE_ATTR               _prefix

Parse error at or near `None' instruction at offset -1

    @property
    def canonical(self) -> str:
        return self._prefix

    def add_prefix--- This code section failed: ---

 L. 520         0  LOAD_FAST                'prefix'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 521        14  LOAD_FAST                'prefix'
               16  LOAD_METHOD              endswith
               18  LOAD_STR                 '/'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 522        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'prefix'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               1
               36  COMPARE_OP               >
               38  POP_JUMP_IF_TRUE     44  'to 44'
               40  <74>             
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            38  '38'

 L. 523        44  LOAD_FAST                'prefix'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _prefix
               50  BINARY_ADD       
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _prefix

Parse error at or near `None' instruction at offset -1

    def raw_match(self, prefix: str) -> bool:
        return False


class StaticResource(PrefixResource):
    VERSION_KEY = 'v'

    def __init__--- This code section failed: ---

 L. 546         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'prefix'
                8  LOAD_FAST                'name'
               10  LOAD_CONST               ('name',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  POP_TOP          

 L. 547        16  SETUP_FINALLY        88  'to 88'

 L. 548        18  LOAD_GLOBAL              Path
               20  LOAD_FAST                'directory'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'directory'

 L. 549        26  LOAD_GLOBAL              str
               28  LOAD_FAST                'directory'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_METHOD              startswith
               34  LOAD_STR                 '~'
               36  CALL_METHOD_1         1  ''
               38  POP_JUMP_IF_FALSE    60  'to 60'

 L. 550        40  LOAD_GLOBAL              Path
               42  LOAD_GLOBAL              os
               44  LOAD_ATTR                path
               46  LOAD_METHOD              expanduser
               48  LOAD_GLOBAL              str
               50  LOAD_FAST                'directory'
               52  CALL_FUNCTION_1       1  ''
               54  CALL_METHOD_1         1  ''
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'directory'
             60_0  COME_FROM            38  '38'

 L. 551        60  LOAD_FAST                'directory'
               62  LOAD_METHOD              resolve
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'directory'

 L. 552        68  LOAD_FAST                'directory'
               70  LOAD_METHOD              is_dir
               72  CALL_METHOD_0         0  ''
               74  POP_JUMP_IF_TRUE     84  'to 84'

 L. 553        76  LOAD_GLOBAL              ValueError
               78  LOAD_STR                 'Not a directory'
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            74  '74'
               84  POP_BLOCK        
               86  JUMP_FORWARD        146  'to 146'
             88_0  COME_FROM_FINALLY    16  '16'

 L. 554        88  DUP_TOP          
               90  LOAD_GLOBAL              FileNotFoundError
               92  LOAD_GLOBAL              ValueError
               94  BUILD_TUPLE_2         2 
               96  <121>               144  ''
               98  POP_TOP          
              100  STORE_FAST               'error'
              102  POP_TOP          
              104  SETUP_FINALLY       136  'to 136'

 L. 555       106  LOAD_GLOBAL              ValueError
              108  LOAD_STR                 "No directory exists at '"
              110  LOAD_FAST                'directory'
              112  FORMAT_VALUE          0  ''
              114  LOAD_STR                 "'"
              116  BUILD_STRING_3        3 
              118  CALL_FUNCTION_1       1  ''
              120  LOAD_FAST                'error'
              122  RAISE_VARARGS_2       2  'exception instance with __cause__'
              124  POP_BLOCK        
              126  POP_EXCEPT       
              128  LOAD_CONST               None
              130  STORE_FAST               'error'
              132  DELETE_FAST              'error'
              134  JUMP_FORWARD        146  'to 146'
            136_0  COME_FROM_FINALLY   104  '104'
              136  LOAD_CONST               None
              138  STORE_FAST               'error'
              140  DELETE_FAST              'error'
              142  <48>             
              144  <48>             
            146_0  COME_FROM           134  '134'
            146_1  COME_FROM            86  '86'

 L. 556       146  LOAD_FAST                'directory'
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _directory

 L. 557       152  LOAD_FAST                'show_index'
              154  LOAD_FAST                'self'
              156  STORE_ATTR               _show_index

 L. 558       158  LOAD_FAST                'chunk_size'
              160  LOAD_FAST                'self'
              162  STORE_ATTR               _chunk_size

 L. 559       164  LOAD_FAST                'follow_symlinks'
              166  LOAD_FAST                'self'
              168  STORE_ATTR               _follow_symlinks

 L. 560       170  LOAD_FAST                'expect_handler'
              172  LOAD_FAST                'self'
              174  STORE_ATTR               _expect_handler

 L. 561       176  LOAD_FAST                'append_version'
              178  LOAD_FAST                'self'
              180  STORE_ATTR               _append_version

 L. 564       182  LOAD_GLOBAL              ResourceRoute

 L. 565       184  LOAD_STR                 'GET'
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                _handle
              190  LOAD_FAST                'self'
              192  LOAD_FAST                'expect_handler'

 L. 564       194  LOAD_CONST               ('expect_handler',)
              196  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 567       198  LOAD_GLOBAL              ResourceRoute

 L. 568       200  LOAD_STR                 'HEAD'
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                _handle
              206  LOAD_FAST                'self'
              208  LOAD_FAST                'expect_handler'

 L. 567       210  LOAD_CONST               ('expect_handler',)
              212  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 563       214  LOAD_CONST               ('GET', 'HEAD')
              216  BUILD_CONST_KEY_MAP_2     2 
              218  LOAD_FAST                'self'
              220  STORE_ATTR               _routes

Parse error at or near `<121>' instruction at offset 96

    def url_for--- This code section failed: ---

 L. 578         0  LOAD_FAST                'append_version'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 579         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _append_version
               12  STORE_FAST               'append_version'
             14_0  COME_FROM             6  '6'

 L. 580        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'filename'
               18  LOAD_GLOBAL              Path
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 581        24  LOAD_GLOBAL              str
               26  LOAD_FAST                'filename'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'filename'
             32_0  COME_FROM            22  '22'

 L. 582        32  LOAD_FAST                'filename'
               34  LOAD_METHOD              lstrip
               36  LOAD_STR                 '/'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'filename'

 L. 584        42  LOAD_GLOBAL              URL
               44  LOAD_ATTR                build
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _prefix
               50  LOAD_CONST               True
               52  LOAD_CONST               ('path', 'encoded')
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  STORE_FAST               'url'

 L. 586        58  LOAD_GLOBAL              YARL_VERSION
               60  LOAD_CONST               (1, 6)
               62  COMPARE_OP               <
               64  POP_JUMP_IF_FALSE    84  'to 84'

 L. 587        66  LOAD_FAST                'url'
               68  LOAD_FAST                'filename'
               70  LOAD_METHOD              replace
               72  LOAD_STR                 '%'
               74  LOAD_STR                 '%25'
               76  CALL_METHOD_2         2  ''
               78  BINARY_TRUE_DIVIDE
               80  STORE_FAST               'url'
               82  JUMP_FORWARD         92  'to 92'
             84_0  COME_FROM            64  '64'

 L. 589        84  LOAD_FAST                'url'
               86  LOAD_FAST                'filename'
               88  BINARY_TRUE_DIVIDE
               90  STORE_FAST               'url'
             92_0  COME_FROM            82  '82'

 L. 591        92  LOAD_FAST                'append_version'
               94  POP_JUMP_IF_FALSE   250  'to 250'

 L. 592        96  SETUP_FINALLY       136  'to 136'

 L. 593        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _directory
              102  LOAD_METHOD              joinpath
              104  LOAD_FAST                'filename'
              106  CALL_METHOD_1         1  ''
              108  LOAD_METHOD              resolve
              110  CALL_METHOD_0         0  ''
              112  STORE_FAST               'filepath'

 L. 594       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _follow_symlinks
              118  POP_JUMP_IF_TRUE    132  'to 132'

 L. 595       120  LOAD_FAST                'filepath'
              122  LOAD_METHOD              relative_to
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _directory
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
            132_0  COME_FROM           118  '118'
              132  POP_BLOCK        
              134  JUMP_FORWARD        162  'to 162'
            136_0  COME_FROM_FINALLY    96  '96'

 L. 596       136  DUP_TOP          
              138  LOAD_GLOBAL              ValueError
              140  LOAD_GLOBAL              FileNotFoundError
              142  BUILD_TUPLE_2         2 
              144  <121>               160  ''
              146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L. 599       152  LOAD_FAST                'url'
              154  ROT_FOUR         
              156  POP_EXCEPT       
              158  RETURN_VALUE     
              160  <48>             
            162_0  COME_FROM           134  '134'

 L. 600       162  LOAD_FAST                'filepath'
              164  LOAD_METHOD              is_file
              166  CALL_METHOD_0         0  ''
              168  POP_JUMP_IF_FALSE   250  'to 250'

 L. 603       170  LOAD_FAST                'filepath'
              172  LOAD_METHOD              open
              174  LOAD_STR                 'rb'
              176  CALL_METHOD_1         1  ''
              178  SETUP_WITH          204  'to 204'
              180  STORE_FAST               'f'

 L. 604       182  LOAD_FAST                'f'
              184  LOAD_METHOD              read
              186  CALL_METHOD_0         0  ''
              188  STORE_FAST               'file_bytes'
              190  POP_BLOCK        
              192  LOAD_CONST               None
              194  DUP_TOP          
              196  DUP_TOP          
              198  CALL_FUNCTION_3       3  ''
              200  POP_TOP          
              202  JUMP_FORWARD        220  'to 220'
            204_0  COME_FROM_WITH      178  '178'
              204  <49>             
              206  POP_JUMP_IF_TRUE    210  'to 210'
              208  <48>             
            210_0  COME_FROM           206  '206'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          
              216  POP_EXCEPT       
              218  POP_TOP          
            220_0  COME_FROM           202  '202'

 L. 605       220  LOAD_FAST                'self'
              222  LOAD_METHOD              _get_file_hash
              224  LOAD_FAST                'file_bytes'
              226  CALL_METHOD_1         1  ''
              228  STORE_FAST               'h'

 L. 606       230  LOAD_FAST                'url'
              232  LOAD_METHOD              with_query
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                VERSION_KEY
              238  LOAD_FAST                'h'
              240  BUILD_MAP_1           1 
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'url'

 L. 607       246  LOAD_FAST                'url'
              248  RETURN_VALUE     
            250_0  COME_FROM           168  '168'
            250_1  COME_FROM            94  '94'

 L. 608       250  LOAD_FAST                'url'
              252  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @staticmethod
    def _get_file_hash(byte_array: bytes) -> str:
        m = hashlib.sha256
        m.update(byte_array)
        b64 = base64.urlsafe_b64encode(m.digest)
        return b64.decode('ascii')

    def get_info(self) -> _InfoDict:
        return {'directory':self._directory, 
         'prefix':self._prefix, 
         'routes':self._routes}

    def set_options_route--- This code section failed: ---

 L. 625         0  LOAD_STR                 'OPTIONS'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _routes
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 626        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'OPTIONS route was set already'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 627        18  LOAD_GLOBAL              ResourceRoute

 L. 628        20  LOAD_STR                 'OPTIONS'
               22  LOAD_FAST                'handler'
               24  LOAD_FAST                'self'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _expect_handler

 L. 627        30  LOAD_CONST               ('expect_handler',)
               32  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _routes
               38  LOAD_STR                 'OPTIONS'
               40  STORE_SUBSCR     

Parse error at or near `None' instruction at offset -1

    async def resolve--- This code section failed: ---

 L. 632         0  LOAD_FAST                'request'
                2  LOAD_ATTR                rel_url
                4  LOAD_ATTR                raw_path
                6  STORE_FAST               'path'

 L. 633         8  LOAD_FAST                'request'
               10  LOAD_ATTR                method
               12  STORE_FAST               'method'

 L. 634        14  LOAD_GLOBAL              set
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _routes
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'allowed_methods'

 L. 635        24  LOAD_FAST                'path'
               26  LOAD_METHOD              startswith
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _prefix
               32  CALL_METHOD_1         1  ''
               34  POP_JUMP_IF_TRUE     46  'to 46'

 L. 636        36  LOAD_CONST               None
               38  LOAD_GLOBAL              set
               40  CALL_FUNCTION_0       0  ''
               42  BUILD_TUPLE_2         2 
               44  RETURN_VALUE     
             46_0  COME_FROM            34  '34'

 L. 638        46  LOAD_FAST                'method'
               48  LOAD_FAST                'allowed_methods'
               50  <118>                 1  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 639        54  LOAD_CONST               None
               56  LOAD_FAST                'allowed_methods'
               58  BUILD_TUPLE_2         2 
               60  RETURN_VALUE     
             62_0  COME_FROM            52  '52'

 L. 641        62  LOAD_STR                 'filename'
               64  LOAD_GLOBAL              _unquote_path
               66  LOAD_FAST                'path'
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _prefix
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_CONST               1
               78  BINARY_ADD       
               80  LOAD_CONST               None
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  CALL_FUNCTION_1       1  ''
               88  BUILD_MAP_1           1 
               90  STORE_FAST               'match_dict'

 L. 642        92  LOAD_GLOBAL              UrlMappingMatchInfo
               94  LOAD_FAST                'match_dict'
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _routes
              100  LOAD_FAST                'method'
              102  BINARY_SUBSCR    
              104  CALL_FUNCTION_2       2  ''
              106  LOAD_FAST                'allowed_methods'
              108  BUILD_TUPLE_2         2 
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 50

    def __len__(self) -> int:
        return len(self._routes)

    def __iter__(self) -> Iterator[AbstractRoute]:
        return iter(self._routes.values)

    async def _handle--- This code section failed: ---

 L. 651         0  LOAD_FAST                'request'
                2  LOAD_ATTR                match_info
                4  LOAD_STR                 'filename'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'rel_url'

 L. 652        10  SETUP_FINALLY        70  'to 70'

 L. 653        12  LOAD_GLOBAL              Path
               14  LOAD_FAST                'rel_url'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'filename'

 L. 654        20  LOAD_FAST                'filename'
               22  LOAD_ATTR                anchor
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L. 658        26  LOAD_GLOBAL              HTTPForbidden
               28  CALL_FUNCTION_0       0  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            24  '24'

 L. 659        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _directory
               36  LOAD_METHOD              joinpath
               38  LOAD_FAST                'filename'
               40  CALL_METHOD_1         1  ''
               42  LOAD_METHOD              resolve
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'filepath'

 L. 660        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _follow_symlinks
               52  POP_JUMP_IF_TRUE     66  'to 66'

 L. 661        54  LOAD_FAST                'filepath'
               56  LOAD_METHOD              relative_to
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _directory
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
             66_0  COME_FROM            52  '52'
               66  POP_BLOCK        
               68  JUMP_FORWARD        192  'to 192'
             70_0  COME_FROM_FINALLY    10  '10'

 L. 662        70  DUP_TOP          
               72  LOAD_GLOBAL              ValueError
               74  LOAD_GLOBAL              FileNotFoundError
               76  BUILD_TUPLE_2         2 
               78  <121>               116  ''
               80  POP_TOP          
               82  STORE_FAST               'error'
               84  POP_TOP          
               86  SETUP_FINALLY       108  'to 108'

 L. 664        88  LOAD_GLOBAL              HTTPNotFound
               90  CALL_FUNCTION_0       0  ''
               92  LOAD_FAST                'error'
               94  RAISE_VARARGS_2       2  'exception instance with __cause__'
               96  POP_BLOCK        
               98  POP_EXCEPT       
              100  LOAD_CONST               None
              102  STORE_FAST               'error'
              104  DELETE_FAST              'error'
              106  JUMP_FORWARD        192  'to 192'
            108_0  COME_FROM_FINALLY    86  '86'
              108  LOAD_CONST               None
              110  STORE_FAST               'error'
              112  DELETE_FAST              'error'
              114  <48>             

 L. 665       116  DUP_TOP          
              118  LOAD_GLOBAL              HTTPForbidden
              120  <121>               134  ''
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L. 666       128  RAISE_VARARGS_0       0  'reraise'
              130  POP_EXCEPT       
              132  JUMP_FORWARD        192  'to 192'

 L. 667       134  DUP_TOP          
              136  LOAD_GLOBAL              Exception
              138  <121>               190  ''
              140  POP_TOP          
              142  STORE_FAST               'error'
              144  POP_TOP          
              146  SETUP_FINALLY       182  'to 182'

 L. 669       148  LOAD_FAST                'request'
              150  LOAD_ATTR                app
              152  LOAD_ATTR                logger
              154  LOAD_METHOD              exception
              156  LOAD_FAST                'error'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L. 670       162  LOAD_GLOBAL              HTTPNotFound
              164  CALL_FUNCTION_0       0  ''
              166  LOAD_FAST                'error'
              168  RAISE_VARARGS_2       2  'exception instance with __cause__'
              170  POP_BLOCK        
              172  POP_EXCEPT       
              174  LOAD_CONST               None
              176  STORE_FAST               'error'
              178  DELETE_FAST              'error'
              180  JUMP_FORWARD        192  'to 192'
            182_0  COME_FROM_FINALLY   146  '146'
              182  LOAD_CONST               None
              184  STORE_FAST               'error'
              186  DELETE_FAST              'error'
              188  <48>             
              190  <48>             
            192_0  COME_FROM           180  '180'
            192_1  COME_FROM           132  '132'
            192_2  COME_FROM           106  '106'
            192_3  COME_FROM            68  '68'

 L. 673       192  LOAD_FAST                'filepath'
              194  LOAD_METHOD              is_dir
              196  CALL_METHOD_0         0  ''
          198_200  POP_JUMP_IF_FALSE   268  'to 268'

 L. 674       202  LOAD_FAST                'self'
              204  LOAD_ATTR                _show_index
          206_208  POP_JUMP_IF_FALSE   260  'to 260'

 L. 675       210  SETUP_FINALLY       232  'to 232'

 L. 676       212  LOAD_GLOBAL              Response

 L. 677       214  LOAD_FAST                'self'
              216  LOAD_METHOD              _directory_as_html
              218  LOAD_FAST                'filepath'
              220  CALL_METHOD_1         1  ''
              222  LOAD_STR                 'text/html'

 L. 676       224  LOAD_CONST               ('text', 'content_type')
              226  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              228  POP_BLOCK        
              230  RETURN_VALUE     
            232_0  COME_FROM_FINALLY   210  '210'

 L. 679       232  DUP_TOP          
              234  LOAD_GLOBAL              PermissionError
          236_238  <121>               256  ''
              240  POP_TOP          
              242  POP_TOP          
              244  POP_TOP          

 L. 680       246  LOAD_GLOBAL              HTTPForbidden
              248  CALL_FUNCTION_0       0  ''
              250  RAISE_VARARGS_1       1  'exception instance'
              252  POP_EXCEPT       
              254  JUMP_FORWARD        258  'to 258'
              256  <48>             
            258_0  COME_FROM           254  '254'
              258  JUMP_FORWARD        266  'to 266'
            260_0  COME_FROM           206  '206'

 L. 682       260  LOAD_GLOBAL              HTTPForbidden
              262  CALL_FUNCTION_0       0  ''
              264  RAISE_VARARGS_1       1  'exception instance'
            266_0  COME_FROM           258  '258'
              266  JUMP_FORWARD        296  'to 296'
            268_0  COME_FROM           198  '198'

 L. 683       268  LOAD_FAST                'filepath'
              270  LOAD_METHOD              is_file
              272  CALL_METHOD_0         0  ''
          274_276  POP_JUMP_IF_FALSE   292  'to 292'

 L. 684       278  LOAD_GLOBAL              FileResponse
              280  LOAD_FAST                'filepath'
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                _chunk_size
              286  LOAD_CONST               ('chunk_size',)
              288  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              290  RETURN_VALUE     
            292_0  COME_FROM           274  '274'

 L. 686       292  LOAD_GLOBAL              HTTPNotFound
              294  RAISE_VARARGS_1       1  'exception instance'
            296_0  COME_FROM           266  '266'

Parse error at or near `<121>' instruction at offset 78

    def _directory_as_html--- This code section failed: ---

 L. 692         0  LOAD_FAST                'filepath'
                2  LOAD_METHOD              is_dir
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L. 694        12  LOAD_FAST                'filepath'
               14  LOAD_METHOD              relative_to
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _directory
               20  CALL_METHOD_1         1  ''
               22  LOAD_METHOD              as_posix
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'relative_path_to_dir'

 L. 695        28  LOAD_STR                 'Index of /'
               30  LOAD_FAST                'relative_path_to_dir'
               32  FORMAT_VALUE          0  ''
               34  BUILD_STRING_2        2 
               36  STORE_FAST               'index_of'

 L. 696        38  LOAD_STR                 '<h1>'
               40  LOAD_FAST                'index_of'
               42  FORMAT_VALUE          0  ''
               44  LOAD_STR                 '</h1>'
               46  BUILD_STRING_3        3 
               48  STORE_FAST               'h1'

 L. 698        50  BUILD_LIST_0          0 
               52  STORE_FAST               'index_list'

 L. 699        54  LOAD_FAST                'filepath'
               56  LOAD_METHOD              iterdir
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'dir_index'

 L. 700        62  LOAD_GLOBAL              sorted
               64  LOAD_FAST                'dir_index'
               66  CALL_FUNCTION_1       1  ''
               68  GET_ITER         
             70_0  COME_FROM           152  '152'
               70  FOR_ITER            154  'to 154'
               72  STORE_FAST               '_file'

 L. 702        74  LOAD_FAST                '_file'
               76  LOAD_METHOD              relative_to
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _directory
               82  CALL_METHOD_1         1  ''
               84  LOAD_METHOD              as_posix
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'rel_path'

 L. 703        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _prefix
               94  LOAD_STR                 '/'
               96  BINARY_ADD       
               98  LOAD_FAST                'rel_path'
              100  BINARY_ADD       
              102  STORE_FAST               'file_url'

 L. 706       104  LOAD_FAST                '_file'
              106  LOAD_METHOD              is_dir
              108  CALL_METHOD_0         0  ''
              110  POP_JUMP_IF_FALSE   126  'to 126'

 L. 707       112  LOAD_FAST                '_file'
              114  LOAD_ATTR                name
              116  FORMAT_VALUE          0  ''
              118  LOAD_STR                 '/'
              120  BUILD_STRING_2        2 
              122  STORE_FAST               'file_name'
              124  JUMP_FORWARD        132  'to 132'
            126_0  COME_FROM           110  '110'

 L. 709       126  LOAD_FAST                '_file'
              128  LOAD_ATTR                name
              130  STORE_FAST               'file_name'
            132_0  COME_FROM           124  '124'

 L. 711       132  LOAD_FAST                'index_list'
              134  LOAD_METHOD              append

 L. 712       136  LOAD_STR                 '<li><a href="{url}">{name}</a></li>'
              138  LOAD_ATTR                format

 L. 713       140  LOAD_FAST                'file_url'
              142  LOAD_FAST                'file_name'

 L. 712       144  LOAD_CONST               ('url', 'name')
              146  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 711       148  CALL_METHOD_1         1  ''
              150  POP_TOP          
              152  JUMP_BACK            70  'to 70'
            154_0  COME_FROM            70  '70'

 L. 716       154  LOAD_STR                 '<ul>\n{}\n</ul>'
              156  LOAD_METHOD              format
              158  LOAD_STR                 '\n'
              160  LOAD_METHOD              join
              162  LOAD_FAST                'index_list'
              164  CALL_METHOD_1         1  ''
              166  CALL_METHOD_1         1  ''
              168  STORE_FAST               'ul'

 L. 717       170  LOAD_STR                 '<body>\n'
              172  LOAD_FAST                'h1'
              174  FORMAT_VALUE          0  ''
              176  LOAD_STR                 '\n'
              178  LOAD_FAST                'ul'
              180  FORMAT_VALUE          0  ''
              182  LOAD_STR                 '\n</body>'
              184  BUILD_STRING_5        5 
              186  STORE_FAST               'body'

 L. 719       188  LOAD_STR                 '<head>\n<title>'
              190  LOAD_FAST                'index_of'
              192  FORMAT_VALUE          0  ''
              194  LOAD_STR                 '</title>\n</head>'
              196  BUILD_STRING_3        3 
              198  STORE_FAST               'head_str'

 L. 720       200  LOAD_STR                 '<html>\n'
              202  LOAD_FAST                'head_str'
              204  FORMAT_VALUE          0  ''
              206  LOAD_STR                 '\n'
              208  LOAD_FAST                'body'
              210  FORMAT_VALUE          0  ''
              212  LOAD_STR                 '\n</html>'
              214  BUILD_STRING_5        5 
              216  STORE_FAST               'html'

 L. 722       218  LOAD_FAST                'html'
              220  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __repr__--- This code section failed: ---

 L. 725         0  LOAD_FAST                'self'
                2  LOAD_ATTR                name
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'
               10  LOAD_STR                 "'"
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                name
               16  BINARY_ADD       
               18  LOAD_STR                 "'"
               20  BINARY_ADD       
               22  JUMP_FORWARD         26  'to 26'
             24_0  COME_FROM             8  '8'
               24  LOAD_STR                 ''
             26_0  COME_FROM            22  '22'
               26  STORE_FAST               'name'

 L. 726        28  LOAD_STR                 '<StaticResource {name} {path} -> {directory!r}>'
               30  LOAD_ATTR                format

 L. 727        32  LOAD_FAST                'name'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _prefix
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _directory

 L. 726        42  LOAD_CONST               ('name', 'path', 'directory')
               44  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class PrefixedSubAppResource(PrefixResource):

    def __init__(self, prefix, app):
        super().__init__(prefix)
        self._app = app
        for resource in app.router.resources:
            resource.add_prefix(prefix)

    def add_prefix(self, prefix):
        super().add_prefix(prefix)
        for resource in self._app.router.resources:
            resource.add_prefix(prefix)

    def url_for(self, *args: str, **kwargs: str) -> URL:
        raise RuntimeError('.url_for() is not supported by sub-application root')

    def get_info(self) -> _InfoDict:
        return {'app':self._app, 
         'prefix':self._prefix}

    async def resolve(self, request: Request) -> _Resolve:
        if not request.url.raw_path.startswith(self._prefix + '/'):
            if request.url.raw_path != self._prefix:
                return (
                 None, set())
        match_info = await self._app.router.resolve(request)
        match_info.add_app(self._app)
        if isinstance(match_info.http_exception, HTTPMethodNotAllowed):
            methods = match_info.http_exception.allowed_methods
        else:
            methods = set()
        return (match_info, methods)

    def __len__(self) -> int:
        return len(self._app.router.routes)

    def __iter__(self) -> Iterator[AbstractRoute]:
        return iter(self._app.router.routes)

    def __repr__(self) -> str:
        return '<PrefixedSubAppResource {prefix} -> {app!r}>'.format(prefix=(self._prefix),
          app=(self._app))


class AbstractRuleMatching(abc.ABC):

    @abc.abstractmethod
    async def match(self, request: Request) -> bool:
        """Return bool if the request satisfies the criteria"""
        pass

    @abc.abstractmethod
    def get_info(self) -> _InfoDict:
        """Return a dict with additional info useful for introspection"""
        pass

    @property
    @abc.abstractmethod
    def canonical(self) -> str:
        """Return a str"""
        pass


class Domain(AbstractRuleMatching):
    re_part = re.compile('(?!-)[a-z\\d-]{1,63}(?<!-)')

    def __init__(self, domain):
        super().__init__
        self._domain = self.validation(domain)

    @property
    def canonical(self) -> str:
        return self._domain

    def validation--- This code section failed: ---

 L. 802         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'domain'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 803        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Domain must be str'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 804        18  LOAD_FAST                'domain'
               20  LOAD_METHOD              rstrip
               22  LOAD_STR                 '.'
               24  CALL_METHOD_1         1  ''
               26  LOAD_METHOD              lower
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'domain'

 L. 805        32  LOAD_FAST                'domain'
               34  POP_JUMP_IF_TRUE     46  'to 46'

 L. 806        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'Domain cannot be empty'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
               44  JUMP_FORWARD         62  'to 62'
             46_0  COME_FROM            34  '34'

 L. 807        46  LOAD_STR                 '://'
               48  LOAD_FAST                'domain'
               50  <118>                 0  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 808        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'Scheme not supported'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            44  '44'

 L. 809        62  LOAD_GLOBAL              URL
               64  LOAD_STR                 'http://'
               66  LOAD_FAST                'domain'
               68  BINARY_ADD       
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               'url'

 L. 810        74  LOAD_FAST                'url'
               76  LOAD_ATTR                raw_host
               78  LOAD_CONST               None
               80  <117>                 1  ''
               82  POP_JUMP_IF_TRUE     88  'to 88'
               84  <74>             
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            82  '82'

 L. 811        88  LOAD_GLOBAL              all
               90  LOAD_CLOSURE             'self'
               92  BUILD_TUPLE_1         1 
               94  LOAD_GENEXPR             '<code_object <genexpr>>'
               96  LOAD_STR                 'Domain.validation.<locals>.<genexpr>'
               98  MAKE_FUNCTION_8          'closure'
              100  LOAD_FAST                'url'
              102  LOAD_ATTR                raw_host
              104  LOAD_METHOD              split
              106  LOAD_STR                 '.'
              108  CALL_METHOD_1         1  ''
              110  GET_ITER         
              112  CALL_FUNCTION_1       1  ''
              114  CALL_FUNCTION_1       1  ''
              116  POP_JUMP_IF_TRUE    126  'to 126'

 L. 812       118  LOAD_GLOBAL              ValueError
              120  LOAD_STR                 'Domain not valid'
              122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM           116  '116'

 L. 813       126  LOAD_FAST                'url'
              128  LOAD_ATTR                port
              130  LOAD_CONST               80
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   142  'to 142'

 L. 814       136  LOAD_FAST                'url'
              138  LOAD_ATTR                raw_host
              140  RETURN_VALUE     
            142_0  COME_FROM           134  '134'

 L. 815       142  LOAD_FAST                'url'
              144  LOAD_ATTR                raw_host
              146  FORMAT_VALUE          0  ''
              148  LOAD_STR                 ':'
              150  LOAD_FAST                'url'
              152  LOAD_ATTR                port
              154  FORMAT_VALUE          0  ''
              156  BUILD_STRING_3        3 
              158  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 50

    async def match(self, request: Request) -> bool:
        host = request.headers.get(hdrs.HOST)
        if not host:
            return False
        return self.match_domain(host)

    def match_domain(self, host: str) -> bool:
        return host.lower == self._domain

    def get_info(self) -> _InfoDict:
        return {'domain': self._domain}


class MaskDomain(Domain):
    re_part = re.compile('(?!-)[a-z\\d\\*-]{1,63}(?<!-)')

    def __init__(self, domain):
        super().__init__(domain)
        mask = self._domain.replace'.''\\.'.replace'*''.*'
        self._mask = re.compile(mask)

    @property
    def canonical(self) -> str:
        return self._mask.pattern

    def match_domain--- This code section failed: ---

 L. 843         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _mask
                4  LOAD_METHOD              fullmatch
                6  LOAD_FAST                'host'
                8  CALL_METHOD_1         1  ''
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class MatchedSubAppResource(PrefixedSubAppResource):

    def __init__(self, rule: AbstractRuleMatching, app: 'Application') -> None:
        AbstractResource.__init__(self)
        self._prefix = ''
        self._app = app
        self._rule = rule

    @property
    def canonical(self) -> str:
        return self._rule.canonical

    def get_info(self) -> _InfoDict:
        return {'app':self._app, 
         'rule':self._rule}

    async def resolve(self, request: Request) -> _Resolve:
        if not await self._rule.match(request):
            return (None, set())
        match_info = await self._app.router.resolve(request)
        match_info.add_app(self._app)
        if isinstance(match_info.http_exception, HTTPMethodNotAllowed):
            methods = match_info.http_exception.allowed_methods
        else:
            methods = set()
        return (match_info, methods)

    def __repr__(self) -> str:
        return '<MatchedSubAppResource -> {app!r}>'.format(app=(self._app))


class ResourceRoute(AbstractRoute):
    __doc__ = 'A route with resource'

    def __init__(self, method, handler, resource, *, expect_handler=None):
        super().__init__(method,
          handler, expect_handler=expect_handler, resource=resource)

    def __repr__(self) -> str:
        return '<ResourceRoute [{method}] {resource} -> {handler!r}'.format(method=(self.method),
          resource=(self._resource),
          handler=(self.handler))

    @property
    def name--- This code section failed: ---

 L. 897         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _resource
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 898        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 899        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _resource
               18  LOAD_ATTR                name
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def url_for--- This code section failed: ---

 L. 903         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _resource
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 904        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _resource
               18  LOAD_ATTR                url_for
               20  LOAD_FAST                'args'
               22  BUILD_MAP_0           0 
               24  LOAD_FAST                'kwargs'
               26  <164>                 1  ''
               28  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def get_info--- This code section failed: ---

 L. 907         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _resource
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 908        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _resource
               18  LOAD_METHOD              get_info
               20  CALL_METHOD_0         0  ''
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class SystemRoute(AbstractRoute):

    def __init__(self, http_exception):
        super().__init__hdrs.METH_ANYself._handle
        self._http_exception = http_exception

    def url_for(self, *args: str, **kwargs: str) -> URL:
        raise RuntimeError('.url_for() is not allowed for SystemRoute')

    @property
    def name(self) -> Optional[str]:
        pass

    def get_info(self) -> _InfoDict:
        return {'http_exception': self._http_exception}

    async def _handle(self, request: Request) -> StreamResponse:
        raise self._http_exception

    @property
    def status(self) -> int:
        return self._http_exception.status

    @property
    def reason(self) -> str:
        return self._http_exception.reason

    def __repr__(self) -> str:
        return '<SystemRoute {self.status}: {self.reason}>'.format(self=self)


class View(AbstractView):

    async def _iter--- This code section failed: ---

 L. 943         0  LOAD_FAST                'self'
                2  LOAD_ATTR                request
                4  LOAD_ATTR                method
                6  LOAD_GLOBAL              hdrs
                8  LOAD_ATTR                METH_ALL
               10  <118>                 1  ''
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 944        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _raise_allowed_methods
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          
             22_0  COME_FROM            12  '12'

 L. 945        22  LOAD_GLOBAL              getattr
               24  LOAD_FAST                'self'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                request
               30  LOAD_ATTR                method
               32  LOAD_METHOD              lower
               34  CALL_METHOD_0         0  ''
               36  LOAD_CONST               None
               38  CALL_FUNCTION_3       3  ''
               40  STORE_FAST               'method'

 L. 946        42  LOAD_FAST                'method'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L. 947        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _raise_allowed_methods
               54  CALL_METHOD_0         0  ''
               56  POP_TOP          
             58_0  COME_FROM            48  '48'

 L. 948        58  LOAD_FAST                'method'
               60  CALL_FUNCTION_0       0  ''
               62  GET_AWAITABLE    
               64  LOAD_CONST               None
               66  YIELD_FROM       
               68  STORE_FAST               'resp'

 L. 949        70  LOAD_FAST                'resp'
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __await__(self) -> Generator[(Any, None, StreamResponse)]:
        return self._iter.__await__

    def _raise_allowed_methods(self) -> None:
        allowed_methods = {m for m in hdrs.METH_ALL if hasattr(self, m.lower)}
        raise HTTPMethodNotAllowed(self.request.method, allowed_methods)


class ResourcesView(Sized, Iterable[AbstractResource], Container[AbstractResource]):

    def __init__(self, resources: List[AbstractResource]) -> None:
        self._resources = resources

    def __len__(self) -> int:
        return len(self._resources)

    def __iter__(self) -> Iterator[AbstractResource]:
        yield from self._resources
        if False:
            yield None

    def __contains__--- This code section failed: ---

 L. 970         0  LOAD_FAST                'resource'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _resources
                6  <118>                 0  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class RoutesView(Sized, Iterable[AbstractRoute], Container[AbstractRoute]):

    def __init__(self, resources: List[AbstractResource]):
        self._routes = []
        for resource in resources:
            for route in resource:
                self._routes.append(route)

    def __len__(self) -> int:
        return len(self._routes)

    def __iter__(self) -> Iterator[AbstractRoute]:
        yield from self._routes
        if False:
            yield None

    def __contains__--- This code section failed: ---

 L. 987         0  LOAD_FAST                'route'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _routes
                6  <118>                 0  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class UrlDispatcher(AbstractRouter, Mapping[(str, AbstractResource)]):
    NAME_SPLIT_RE = re.compile('[.:-]')

    def __init__(self):
        super().__init__
        self._resources = []
        self._named_resources = {}

    async def resolve--- This code section failed: ---

 L.1000         0  LOAD_FAST                'request'
                2  LOAD_ATTR                method
                4  STORE_FAST               'method'

 L.1001         6  LOAD_GLOBAL              set
                8  CALL_FUNCTION_0       0  ''
               10  STORE_FAST               'allowed_methods'

 L.1003        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _resources
               16  GET_ITER         
             18_0  COME_FROM            66  '66'
               18  FOR_ITER             68  'to 68'
               20  STORE_FAST               'resource'

 L.1004        22  LOAD_FAST                'resource'
               24  LOAD_METHOD              resolve
               26  LOAD_FAST                'request'
               28  CALL_METHOD_1         1  ''
               30  GET_AWAITABLE    
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'match_dict'
               40  STORE_FAST               'allowed'

 L.1005        42  LOAD_FAST                'match_dict'
               44  LOAD_CONST               None
               46  <117>                 1  ''
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L.1006        50  LOAD_FAST                'match_dict'
               52  ROT_TWO          
               54  POP_TOP          
               56  RETURN_VALUE     
             58_0  COME_FROM            48  '48'

 L.1008        58  LOAD_FAST                'allowed_methods'
               60  LOAD_FAST                'allowed'
               62  INPLACE_OR       
               64  STORE_FAST               'allowed_methods'
               66  JUMP_BACK            18  'to 18'
             68_0  COME_FROM            18  '18'

 L.1010        68  LOAD_FAST                'allowed_methods'
               70  POP_JUMP_IF_FALSE    86  'to 86'

 L.1011        72  LOAD_GLOBAL              MatchInfoError
               74  LOAD_GLOBAL              HTTPMethodNotAllowed
               76  LOAD_FAST                'method'
               78  LOAD_FAST                'allowed_methods'
               80  CALL_FUNCTION_2       2  ''
               82  CALL_FUNCTION_1       1  ''
               84  RETURN_VALUE     
             86_0  COME_FROM            70  '70'

 L.1013        86  LOAD_GLOBAL              MatchInfoError
               88  LOAD_GLOBAL              HTTPNotFound
               90  CALL_FUNCTION_0       0  ''
               92  CALL_FUNCTION_1       1  ''
               94  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 46

    def __iter__(self) -> Iterator[str]:
        return iter(self._named_resources)

    def __len__(self) -> int:
        return len(self._named_resources)

    def __contains__--- This code section failed: ---

 L.1022         0  LOAD_FAST                'resource'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _named_resources
                6  <118>                 0  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __getitem__(self, name: str) -> AbstractResource:
        return self._named_resources[name]

    def resources(self) -> ResourcesView:
        return ResourcesView(self._resources)

    def routes(self) -> RoutesView:
        return RoutesView(self._resources)

    def named_resources(self) -> Mapping[(str, AbstractResource)]:
        return MappingProxyType(self._named_resources)

    def register_resource--- This code section failed: ---

 L.1037         0  LOAD_GLOBAL              isinstance

 L.1038         2  LOAD_FAST                'resource'
                4  LOAD_GLOBAL              AbstractResource

 L.1037         6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     24  'to 24'
               10  <74>             

 L.1039        12  LOAD_STR                 'Instance of AbstractResource class is required, got '
               14  LOAD_FAST                'resource'
               16  FORMAT_VALUE          2  '!r'
               18  BUILD_STRING_2        2 

 L.1037        20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM             8  '8'

 L.1040        24  LOAD_FAST                'self'
               26  LOAD_ATTR                frozen
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L.1041        30  LOAD_GLOBAL              RuntimeError
               32  LOAD_STR                 'Cannot register a resource into frozen router.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L.1043        38  LOAD_FAST                'resource'
               40  LOAD_ATTR                name
               42  STORE_FAST               'name'

 L.1045        44  LOAD_FAST                'name'
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE   164  'to 164'

 L.1046        52  LOAD_FAST                'self'
               54  LOAD_ATTR                NAME_SPLIT_RE
               56  LOAD_METHOD              split
               58  LOAD_FAST                'name'
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'parts'

 L.1047        64  LOAD_FAST                'parts'
               66  GET_ITER         
             68_0  COME_FROM           120  '120'
             68_1  COME_FROM           104  '104'
               68  FOR_ITER            122  'to 122'
               70  STORE_FAST               'part'

 L.1048        72  LOAD_GLOBAL              keyword
               74  LOAD_METHOD              iskeyword
               76  LOAD_FAST                'part'
               78  CALL_METHOD_1         1  ''
               80  POP_JUMP_IF_FALSE    98  'to 98'

 L.1049        82  LOAD_GLOBAL              ValueError

 L.1050        84  LOAD_STR                 'Incorrect route name '
               86  LOAD_FAST                'name'
               88  FORMAT_VALUE          2  '!r'
               90  LOAD_STR                 ', python keywords cannot be used for route name'
               92  BUILD_STRING_3        3 

 L.1049        94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            80  '80'

 L.1054        98  LOAD_FAST                'part'
              100  LOAD_METHOD              isidentifier
              102  CALL_METHOD_0         0  ''
              104  POP_JUMP_IF_TRUE_BACK    68  'to 68'

 L.1055       106  LOAD_GLOBAL              ValueError

 L.1056       108  LOAD_STR                 'Incorrect route name {!r}, the name should be a sequence of python identifiers separated by dash, dot or column'
              110  LOAD_METHOD              format

 L.1059       112  LOAD_FAST                'name'

 L.1056       114  CALL_METHOD_1         1  ''

 L.1055       116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
              120  JUMP_BACK            68  'to 68'
            122_0  COME_FROM            68  '68'

 L.1061       122  LOAD_FAST                'name'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _named_resources
              128  <118>                 0  ''
              130  POP_JUMP_IF_FALSE   154  'to 154'

 L.1062       132  LOAD_GLOBAL              ValueError

 L.1063       134  LOAD_STR                 'Duplicate {!r}, already handled by {!r}'
              136  LOAD_METHOD              format

 L.1064       138  LOAD_FAST                'name'
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                _named_resources
              144  LOAD_FAST                'name'
              146  BINARY_SUBSCR    

 L.1063       148  CALL_METHOD_2         2  ''

 L.1062       150  CALL_FUNCTION_1       1  ''
              152  RAISE_VARARGS_1       1  'exception instance'
            154_0  COME_FROM           130  '130'

 L.1066       154  LOAD_FAST                'resource'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _named_resources
              160  LOAD_FAST                'name'
              162  STORE_SUBSCR     
            164_0  COME_FROM            50  '50'

 L.1067       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _resources
              168  LOAD_METHOD              append
              170  LOAD_FAST                'resource'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          

Parse error at or near `<74>' instruction at offset 10

    def add_resource--- This code section failed: ---

 L.1070         0  LOAD_FAST                'path'
                2  POP_JUMP_IF_FALSE    22  'to 22'
                4  LOAD_FAST                'path'
                6  LOAD_METHOD              startswith
                8  LOAD_STR                 '/'
               10  CALL_METHOD_1         1  ''
               12  POP_JUMP_IF_TRUE     22  'to 22'

 L.1071        14  LOAD_GLOBAL              ValueError
               16  LOAD_STR                 'path should be started with / or be empty'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'
             22_1  COME_FROM             2  '2'

 L.1073        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _resources
               26  POP_JUMP_IF_FALSE    68  'to 68'

 L.1074        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _resources
               32  LOAD_CONST               -1
               34  BINARY_SUBSCR    
               36  STORE_FAST               'resource'

 L.1075        38  LOAD_FAST                'resource'
               40  LOAD_ATTR                name
               42  LOAD_FAST                'name'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    68  'to 68'
               48  LOAD_FAST                'resource'
               50  LOAD_METHOD              raw_match
               52  LOAD_FAST                'path'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L.1076        58  LOAD_GLOBAL              cast
               60  LOAD_GLOBAL              Resource
               62  LOAD_FAST                'resource'
               64  CALL_FUNCTION_2       2  ''
               66  RETURN_VALUE     
             68_0  COME_FROM            56  '56'
             68_1  COME_FROM            46  '46'
             68_2  COME_FROM            26  '26'

 L.1077        68  LOAD_STR                 '{'
               70  LOAD_FAST                'path'
               72  <118>                 0  ''
               74  POP_JUMP_IF_TRUE    124  'to 124'
               76  LOAD_STR                 '}'
               78  LOAD_FAST                'path'
               80  <118>                 0  ''
               82  POP_JUMP_IF_TRUE    124  'to 124'
               84  LOAD_GLOBAL              ROUTE_RE
               86  LOAD_METHOD              search
               88  LOAD_FAST                'path'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_TRUE    124  'to 124'

 L.1078        94  LOAD_GLOBAL              PlainResource
               96  LOAD_GLOBAL              _requote_path
               98  LOAD_FAST                'path'
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_FAST                'name'
              104  LOAD_CONST               ('name',)
              106  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              108  STORE_FAST               'resource'

 L.1079       110  LOAD_FAST                'self'
              112  LOAD_METHOD              register_resource
              114  LOAD_FAST                'resource'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L.1080       120  LOAD_FAST                'resource'
              122  RETURN_VALUE     
            124_0  COME_FROM            92  '92'
            124_1  COME_FROM            82  '82'
            124_2  COME_FROM            74  '74'

 L.1081       124  LOAD_GLOBAL              DynamicResource
              126  LOAD_FAST                'path'
              128  LOAD_FAST                'name'
              130  LOAD_CONST               ('name',)
              132  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              134  STORE_FAST               'resource'

 L.1082       136  LOAD_FAST                'self'
              138  LOAD_METHOD              register_resource
              140  LOAD_FAST                'resource'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          

 L.1083       146  LOAD_FAST                'resource'
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 72

    def add_route(self, method: str, path: str, handler: Union[(_WebHandler, Type[AbstractView])], *, name: Optional[str]=None, expect_handler: Optional[_ExpectHandler]=None) -> AbstractRoute:
        resource = self.add_resource(path, name=name)
        return resource.add_route(method, handler, expect_handler=expect_handler)

    def add_static--- This code section failed: ---

 L.1115         0  LOAD_FAST                'prefix'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L.1116        14  LOAD_FAST                'prefix'
               16  LOAD_METHOD              endswith
               18  LOAD_STR                 '/'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_FALSE    36  'to 36'

 L.1117        24  LOAD_FAST                'prefix'
               26  LOAD_CONST               None
               28  LOAD_CONST               -1
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    
               34  STORE_FAST               'prefix'
             36_0  COME_FROM            22  '22'

 L.1118        36  LOAD_GLOBAL              StaticResource

 L.1119        38  LOAD_FAST                'prefix'

 L.1120        40  LOAD_FAST                'path'

 L.1121        42  LOAD_FAST                'name'

 L.1122        44  LOAD_FAST                'expect_handler'

 L.1123        46  LOAD_FAST                'chunk_size'

 L.1124        48  LOAD_FAST                'show_index'

 L.1125        50  LOAD_FAST                'follow_symlinks'

 L.1126        52  LOAD_FAST                'append_version'

 L.1118        54  LOAD_CONST               ('name', 'expect_handler', 'chunk_size', 'show_index', 'follow_symlinks', 'append_version')
               56  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
               58  STORE_FAST               'resource'

 L.1128        60  LOAD_FAST                'self'
               62  LOAD_METHOD              register_resource
               64  LOAD_FAST                'resource'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L.1129        70  LOAD_FAST                'resource'
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_head--- This code section failed: ---

 L.1135         0  LOAD_FAST                'self'
                2  LOAD_ATTR                add_route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_HEAD
                8  LOAD_FAST                'path'
               10  LOAD_FAST                'handler'
               12  BUILD_TUPLE_3         3 
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_options--- This code section failed: ---

 L.1143         0  LOAD_FAST                'self'
                2  LOAD_ATTR                add_route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_OPTIONS
                8  LOAD_FAST                'path'
               10  LOAD_FAST                'handler'
               12  BUILD_TUPLE_3         3 
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_get--- This code section failed: ---

 L.1158         0  LOAD_FAST                'self'
                2  LOAD_ATTR                add_resource
                4  LOAD_FAST                'path'
                6  LOAD_FAST                'name'
                8  LOAD_CONST               ('name',)
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  STORE_FAST               'resource'

 L.1159        14  LOAD_FAST                'allow_head'
               16  POP_JUMP_IF_FALSE    40  'to 40'

 L.1160        18  LOAD_FAST                'resource'
               20  LOAD_ATTR                add_route
               22  LOAD_GLOBAL              hdrs
               24  LOAD_ATTR                METH_HEAD
               26  LOAD_FAST                'handler'
               28  BUILD_TUPLE_2         2 
               30  BUILD_MAP_0           0 
               32  LOAD_FAST                'kwargs'
               34  <164>                 1  ''
               36  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               38  POP_TOP          
             40_0  COME_FROM            16  '16'

 L.1161        40  LOAD_FAST                'resource'
               42  LOAD_ATTR                add_route
               44  LOAD_GLOBAL              hdrs
               46  LOAD_ATTR                METH_GET
               48  LOAD_FAST                'handler'
               50  BUILD_TUPLE_2         2 
               52  BUILD_MAP_0           0 
               54  LOAD_FAST                'kwargs'
               56  <164>                 1  ''
               58  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 34

    def add_post--- This code section failed: ---

 L.1167         0  LOAD_FAST                'self'
                2  LOAD_ATTR                add_route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_POST
                8  LOAD_FAST                'path'
               10  LOAD_FAST                'handler'
               12  BUILD_TUPLE_3         3 
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_put--- This code section failed: ---

 L.1173         0  LOAD_FAST                'self'
                2  LOAD_ATTR                add_route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_PUT
                8  LOAD_FAST                'path'
               10  LOAD_FAST                'handler'
               12  BUILD_TUPLE_3         3 
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_patch--- This code section failed: ---

 L.1181         0  LOAD_FAST                'self'
                2  LOAD_ATTR                add_route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_PATCH
                8  LOAD_FAST                'path'
               10  LOAD_FAST                'handler'
               12  BUILD_TUPLE_3         3 
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_delete--- This code section failed: ---

 L.1189         0  LOAD_FAST                'self'
                2  LOAD_ATTR                add_route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_DELETE
                8  LOAD_FAST                'path'
               10  LOAD_FAST                'handler'
               12  BUILD_TUPLE_3         3 
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_view--- This code section failed: ---

 L.1197         0  LOAD_FAST                'self'
                2  LOAD_ATTR                add_route
                4  LOAD_GLOBAL              hdrs
                6  LOAD_ATTR                METH_ANY
                8  LOAD_FAST                'path'
               10  LOAD_FAST                'handler'
               12  BUILD_TUPLE_3         3 
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def freeze(self):
        super().freeze
        for resource in self._resources:
            resource.freeze

    def add_routes(self, routes: Iterable[AbstractRouteDef]) -> List[AbstractRoute]:
        """Append routes to route table.

        Parameter should be a sequence of RouteDef objects.

        Returns a list of registered AbstractRoute instances.
        """
        registered_routes = []
        for route_def in routes:
            registered_routes.extend(route_def.register(self))
        else:
            return registered_routes


def _quote_path(value: str) -> str:
    if YARL_VERSION < (1, 6):
        value = value.replace'%''%25'
    return URL.build(path=value, encoded=False).raw_path


def _unquote_path(value: str) -> str:
    return URL.build(path=value, encoded=True).path


def _requote_path--- This code section failed: ---

 L.1230         0  LOAD_GLOBAL              _quote_path
                2  LOAD_FAST                'value'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'result'

 L.1231         8  LOAD_STR                 '%'
               10  LOAD_FAST                'value'
               12  <118>                 0  ''
               14  POP_JUMP_IF_FALSE    28  'to 28'

 L.1232        16  LOAD_FAST                'result'
               18  LOAD_METHOD              replace
               20  LOAD_STR                 '%25'
               22  LOAD_STR                 '%'
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'result'
             28_0  COME_FROM            14  '14'

 L.1233        28  LOAD_FAST                'result'
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 12