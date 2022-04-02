# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\web_urldispatcher.py
import abc, asyncio, base64, hashlib, inspect, keyword, os, re, warnings
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Container, Dict, Generator, Iterable, Iterator, List, Mapping, Optional, Set, Sized, Tuple, Type, Union, cast
from yarl import URL
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
HTTP_METHOD_RE = re.compile("^[0-9A-Za-z!#\\$%&'\\*\\+\\-\\.\\^_`\\|~]+$")
ROUTE_RE = re.compile('(\\{[_a-zA-Z][^{}]*(?:\\{[^{}]*\\}[^{}]*)*\\})')
PATH_SEP = re.escape('/')
_WebHandler = Callable[([Request], Awaitable[StreamResponse])]
_ExpectHandler = Callable[([Request], Awaitable[None])]
_Resolve = Tuple[(Optional[AbstractMatchInfo], Set[str])]

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
    def get_info(self) -> Dict[(str, Any)]:
        """Return a dict with additional info useful for introspection"""
        pass

    def freeze(self) -> None:
        pass

    @abc.abstractmethod
    def raw_match(self, path: str) -> bool:
        """Perform a raw match against path"""
        pass


class AbstractRoute(abc.ABC):

    def __init__(self, method: str, handler: Union[(_WebHandler, Type[AbstractView])], *, expect_handler: _ExpectHandler=None, resource: AbstractResource=None) -> None:
        if expect_handler is None:
            expect_handler = _default_expect_handler
        else:
            assert asyncio.iscoroutinefunction(expect_handler), 'Coroutine is expected, got {!r}'.format(expect_handler)
            method = method.upper()
            assert HTTP_METHOD_RE.match(method), '{} is not allowed HTTP method'.format(method)
        assert callable(handler), handler
        if asyncio.iscoroutinefunction(handler):
            pass
        elif inspect.isgeneratorfunction(handler):
            warnings.warn('Bare generators are deprecated, use @coroutine wrapper', DeprecationWarning)
        else:
            if isinstance(handler, type) and issubclass(handler, AbstractView):
                pass
            else:
                warnings.warn('Bare functions are deprecated, use async ones', DeprecationWarning)

                @wraps(handler)
                async def handler_wrapper(request):
                    result = old_handler(request)
                    if asyncio.iscoroutine(result):
                        return await result
                    return result

                old_handler = handler
                handler = handler_wrapper
            self._method = method
            self._handler = handler
            self._expect_handler = expect_handler
            self._resource = resource

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
    def get_info(self) -> Dict[(str, Any)]:
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

    def get_info(self) -> Dict[(str, str)]:
        return self._route.get_info()

    @property
    def apps(self) -> Tuple[('Application', Ellipsis)]:
        return tuple(self._apps)

    def add_app(self, app: 'Application') -> None:
        if self._frozen:
            raise RuntimeError('Cannot change apps stack after .freeze() call')
        if self._current_app is None:
            self._current_app = app
        self._apps.insert(0, app)

    @property
    def current_app(self) -> 'Application':
        app = self._current_app
        assert app is not None
        return app

    @contextmanager
    def set_current_app(self, app: 'Application') -> Generator[(None, None, None)]:
        if DEBUG:
            if app not in self._apps:
                raise RuntimeError('Expected one of the following apps {!r}, got {!r}'.format(self._apps, app))
        prev = self._current_app
        self._current_app = app
        try:
            (yield)
        finally:
            self._current_app = prev

    def freeze(self) -> None:
        self._frozen = True

    def __repr__(self):
        return '<MatchInfo {}: {}>'.format(super().__repr__(), self._route)


class MatchInfoError(UrlMappingMatchInfo):

    def __init__(self, http_exception):
        self._exception = http_exception
        super().__init__({}, SystemRoute(self._exception))

    @property
    def http_exception(self) -> HTTPException:
        return self._exception

    def __repr__(self) -> str:
        return '<MatchInfoError {}: {}>'.format(self._exception.status, self._exception.reason)


async def _default_expect_handler(request: Request) -> None:
    """Default handler for Expect header.

    Just send "100 Continue" to client.
    raise HTTPExpectationFailed if value of header is not "100-continue"
    """
    expect = request.headers.get(hdrs.EXPECT)
    if request.version == HttpVersion11:
        if expect.lower() == '100-continue':
            await request.writer.write(b'HTTP/1.1 100 Continue\r\n\r\n')
        else:
            raise HTTPExpectationFailed(text=('Unknown Expect: %s' % expect))


class Resource(AbstractResource):

    def __init__(self, *, name=None):
        super().__init__(name=name)
        self._routes = []

    def add_route(self, method: str, handler: Union[(Type[AbstractView], _WebHandler)], *, expect_handler: Optional[_ExpectHandler]=None) -> 'ResourceRoute':
        for route_obj in self._routes:
            if route_obj.method == method or route_obj.method == hdrs.METH_ANY:
                raise RuntimeError('Added route will never be executed, method {route.method} is already registered'.format(route=route_obj))
            route_obj = ResourceRoute(method, handler, self, expect_handler=expect_handler)
            self.register_route(route_obj)
            return route_obj

    def register_route(self, route: 'ResourceRoute') -> None:
        assert isinstance(route, ResourceRoute), 'Instance of Route class is required, got {!r}'.format(route)
        self._routes.append(route)

    async def resolve(self, request: Request) -> _Resolve:
        allowed_methods = set()
        match_dict = self._match(request.rel_url.raw_path)
        if match_dict is None:
            return (
             None, allowed_methods)
        for route_obj in self._routes:
            route_method = route_obj.method
            allowed_methods.add(route_method)
            if route_method == request.method or route_method == hdrs.METH_ANY:
                return (UrlMappingMatchInfo(match_dict, route_obj),
                 allowed_methods)
            return (None, allowed_methods)

    @abc.abstractmethod
    def _match(self, path: str) -> Optional[Dict[(str, str)]]:
        pass

    def __len__(self) -> int:
        return len(self._routes)

    def __iter__(self) -> Iterator[AbstractRoute]:
        return iter(self._routes)


class PlainResource(Resource):

    def __init__(self, path, *, name=None):
        super().__init__(name=name)
        if path:
            assert path.startswith('/')
        self._path = path

    @property
    def canonical(self) -> str:
        return self._path

    def freeze(self) -> None:
        if not self._path:
            self._path = '/'

    def add_prefix(self, prefix: str) -> None:
        assert prefix.startswith('/')
        assert not prefix.endswith('/')
        assert len(prefix) > 1
        self._path = prefix + self._path

    def _match(self, path: str) -> Optional[Dict[(str, str)]]:
        if self._path == path:
            return {}
        return

    def raw_match(self, path: str) -> bool:
        return self._path == path

    def get_info(self) -> Dict[(str, Any)]:
        return {'path': self._path}

    def url_for(self) -> URL:
        return URL.build(path=(self._path), encoded=True)

    def __repr__(self) -> str:
        name = "'" + self.name + "' " if self.name is not None else ''
        return '<PlainResource {name} {path}>'.format(name=name, path=(self._path))


class DynamicResource(Resource):
    DYN = re.compile('\\{(?P<var>[_a-zA-Z][_a-zA-Z0-9]*)\\}')
    DYN_WITH_RE = re.compile('\\{(?P<var>[_a-zA-Z][_a-zA-Z0-9]*):(?P<re>.+)\\}')
    GOOD = '[^{}/]+'

    def __init__(self, path, *, name=None):
        super().__init__(name=name)
        pattern = ''
        formatter = ''
        for part in ROUTE_RE.split(path):
            match = self.DYN.fullmatch(part)
            if match:
                pattern += '(?P<{}>{})'.format(match.group('var'), self.GOOD)
                formatter += '{' + match.group('var') + '}'
            else:
                match = self.DYN_WITH_RE.fullmatch(part)
                if match:
                    pattern += ('(?P<{var}>{re})'.format)(**match.groupdict())
                    formatter += '{' + match.group('var') + '}'
                else:
                    if '{' in part or '}' in part:
                        raise ValueError("Invalid path '{}'['{}']".format(path, part))
                    path = URL.build(path=part).raw_path
                    formatter += path
                    pattern += re.escape(path)
        else:
            try:
                compiled = re.compile(pattern)
            except re.error as exc:
                try:
                    raise ValueError("Bad pattern '{}': {}".format(pattern, exc)) from None
                finally:
                    exc = None
                    del exc

            else:
                assert compiled.pattern.startswith(PATH_SEP)
                assert formatter.startswith('/')
                self._pattern = compiled
                self._formatter = formatter

    @property
    def canonical(self) -> str:
        return self._formatter

    def add_prefix(self, prefix: str) -> None:
        assert prefix.startswith('/')
        assert not prefix.endswith('/')
        assert len(prefix) > 1
        self._pattern = re.compile(re.escape(prefix) + self._pattern.pattern)
        self._formatter = prefix + self._formatter

    def _match(self, path: str) -> Optional[Dict[(str, str)]]:
        match = self._pattern.fullmatch(path)
        if match is None:
            return
        return {URL.build(path=value, encoded=True).path:key for key, value in match.groupdict().items()}

    def raw_match(self, path: str) -> bool:
        return self._formatter == path

    def get_info(self) -> Dict[(str, Any)]:
        return {'formatter':self._formatter,  'pattern':self._pattern}

    def url_for(self, **parts: str) -> URL:
        url = self._formatter.format_map({URL.build(path=v).raw_path:k for k, v in parts.items()})
        return URL.build(path=url)

    def __repr__(self) -> str:
        name = "'" + self.name + "' " if self.name is not None else ''
        return '<DynamicResource {name} {formatter}>'.format(name=name,
          formatter=(self._formatter))


class PrefixResource(AbstractResource):

    def __init__(self, prefix, *, name=None):
        if prefix:
            assert prefix.startswith('/'), prefix
        if not prefix in ('', '/'):
            if prefix.endswith('/'):
                raise AssertionError(prefix)
        super().__init__(name=name)
        self._prefix = URL.build(path=prefix).raw_path

    @property
    def canonical(self) -> str:
        return self._prefix

    def add_prefix(self, prefix: str) -> None:
        assert prefix.startswith('/')
        assert not prefix.endswith('/')
        assert len(prefix) > 1
        self._prefix = prefix + self._prefix

    def raw_match(self, prefix: str) -> bool:
        return False


class StaticResource(PrefixResource):
    VERSION_KEY = 'v'

    def __init__(self, prefix, directory, *, name=None, expect_handler=None, chunk_size=262144, show_index=False, follow_symlinks=False, append_version=False):
        super().__init__(prefix, name=name)
        try:
            directory = Path(directory)
            if str(directory).startswith('~'):
                directory = Path(os.path.expanduser(str(directory)))
            directory = directory.resolve()
            if not directory.is_dir():
                raise ValueError('Not a directory')
        except (FileNotFoundError, ValueError) as error:
            try:
                raise ValueError("No directory exists at '{}'".format(directory)) from error
            finally:
                error = None
                del error

        else:
            self._directory = directory
            self._show_index = show_index
            self._chunk_size = chunk_size
            self._follow_symlinks = follow_symlinks
            self._expect_handler = expect_handler
            self._append_version = append_version
            self._routes = {'GET':ResourceRoute('GET', self._handle, self, expect_handler=expect_handler), 
             'HEAD':ResourceRoute('HEAD', self._handle, self, expect_handler=expect_handler)}

    def url_for(self, *, filename: Union[(str, Path)], append_version: Optional[bool]=None) -> URL:
        if append_version is None:
            append_version = self._append_version
        else:
            if isinstance(filename, Path):
                filename = str(filename)
            else:
                while True:
                    if filename.startswith('/'):
                        filename = filename[1:]

            filename = '/' + filename
            url = URL.build(path=(self._prefix + filename))
            if append_version:
                try:
                    if filename.startswith('/'):
                        filename = filename[1:]
                    filepath = self._directory.joinpath(filename).resolve()
                    if not self._follow_symlinks:
                        filepath.relative_to(self._directory)
                except (ValueError, FileNotFoundError):
                    return url
                else:
                    if filepath.is_file():
                        with open((str(filepath)), mode='rb') as (f):
                            file_bytes = f.read()
                        h = self._get_file_hash(file_bytes)
                        url = url.with_query({self.VERSION_KEY: h})
                        return url
        return url

    @staticmethod
    def _get_file_hash(byte_array: bytes) -> str:
        m = hashlib.sha256()
        m.update(byte_array)
        b64 = base64.urlsafe_b64encode(m.digest())
        return b64.decode('ascii')

    def get_info(self) -> Dict[(str, Any)]:
        return {'directory':self._directory,  'prefix':self._prefix}

    def set_options_route(self, handler: _WebHandler) -> None:
        if 'OPTIONS' in self._routes:
            raise RuntimeError('OPTIONS route was set already')
        self._routes['OPTIONS'] = ResourceRoute('OPTIONS',
          handler, self, expect_handler=(self._expect_handler))

    async def resolve(self, request: Request) -> _Resolve:
        path = request.rel_url.raw_path
        method = request.method
        allowed_methods = set(self._routes)
        if not path.startswith(self._prefix):
            return (
             None, set())
        if method not in allowed_methods:
            return (
             None, allowed_methods)
        match_dict = {'filename': URL.build(path=(path[len(self._prefix) + 1:]), encoded=True).path}
        return (UrlMappingMatchInfo(match_dict, self._routes[method]),
         allowed_methods)

    def __len__(self) -> int:
        return len(self._routes)

    def __iter__(self) -> Iterator[AbstractRoute]:
        return iter(self._routes.values())

    async def _handle--- This code section failed: ---

 L. 603         0  LOAD_FAST                'request'
                2  LOAD_ATTR                match_info
                4  LOAD_STR                 'filename'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'rel_url'

 L. 604        10  SETUP_FINALLY        70  'to 70'

 L. 605        12  LOAD_GLOBAL              Path
               14  LOAD_FAST                'rel_url'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'filename'

 L. 606        20  LOAD_FAST                'filename'
               22  LOAD_ATTR                anchor
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L. 610        26  LOAD_GLOBAL              HTTPForbidden
               28  CALL_FUNCTION_0       0  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            24  '24'

 L. 611        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _directory
               36  LOAD_METHOD              joinpath
               38  LOAD_FAST                'filename'
               40  CALL_METHOD_1         1  ''
               42  LOAD_METHOD              resolve
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'filepath'

 L. 612        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _follow_symlinks
               52  POP_JUMP_IF_TRUE     66  'to 66'

 L. 613        54  LOAD_FAST                'filepath'
               56  LOAD_METHOD              relative_to
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _directory
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
             66_0  COME_FROM            52  '52'
               66  POP_BLOCK        
               68  JUMP_FORWARD        190  'to 190'
             70_0  COME_FROM_FINALLY    10  '10'

 L. 614        70  DUP_TOP          
               72  LOAD_GLOBAL              ValueError
               74  LOAD_GLOBAL              FileNotFoundError
               76  BUILD_TUPLE_2         2 
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   114  'to 114'
               82  POP_TOP          
               84  STORE_FAST               'error'
               86  POP_TOP          
               88  SETUP_FINALLY       102  'to 102'

 L. 616        90  LOAD_GLOBAL              HTTPNotFound
               92  CALL_FUNCTION_0       0  ''
               94  LOAD_FAST                'error'
               96  RAISE_VARARGS_2       2  'exception instance with __cause__'
               98  POP_BLOCK        
              100  BEGIN_FINALLY    
            102_0  COME_FROM_FINALLY    88  '88'
              102  LOAD_CONST               None
              104  STORE_FAST               'error'
              106  DELETE_FAST              'error'
              108  END_FINALLY      
              110  POP_EXCEPT       
              112  JUMP_FORWARD        190  'to 190'
            114_0  COME_FROM            80  '80'

 L. 617       114  DUP_TOP          
              116  LOAD_GLOBAL              HTTPForbidden
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   134  'to 134'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L. 618       128  RAISE_VARARGS_0       0  'reraise'
              130  POP_EXCEPT       
              132  JUMP_FORWARD        190  'to 190'
            134_0  COME_FROM           120  '120'

 L. 619       134  DUP_TOP          
              136  LOAD_GLOBAL              Exception
              138  COMPARE_OP               exception-match
              140  POP_JUMP_IF_FALSE   188  'to 188'
              142  POP_TOP          
              144  STORE_FAST               'error'
              146  POP_TOP          
              148  SETUP_FINALLY       176  'to 176'

 L. 621       150  LOAD_FAST                'request'
              152  LOAD_ATTR                app
              154  LOAD_ATTR                logger
              156  LOAD_METHOD              exception
              158  LOAD_FAST                'error'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          

 L. 622       164  LOAD_GLOBAL              HTTPNotFound
              166  CALL_FUNCTION_0       0  ''
              168  LOAD_FAST                'error'
              170  RAISE_VARARGS_2       2  'exception instance with __cause__'
              172  POP_BLOCK        
              174  BEGIN_FINALLY    
            176_0  COME_FROM_FINALLY   148  '148'
              176  LOAD_CONST               None
              178  STORE_FAST               'error'
              180  DELETE_FAST              'error'
              182  END_FINALLY      
              184  POP_EXCEPT       
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           140  '140'
              188  END_FINALLY      
            190_0  COME_FROM           186  '186'
            190_1  COME_FROM           132  '132'
            190_2  COME_FROM           112  '112'
            190_3  COME_FROM            68  '68'

 L. 625       190  LOAD_FAST                'filepath'
              192  LOAD_METHOD              is_dir
              194  CALL_METHOD_0         0  ''
          196_198  POP_JUMP_IF_FALSE   268  'to 268'

 L. 626       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _show_index
          204_206  POP_JUMP_IF_FALSE   260  'to 260'

 L. 627       208  SETUP_FINALLY       230  'to 230'

 L. 628       210  LOAD_GLOBAL              Response
              212  LOAD_FAST                'self'
              214  LOAD_METHOD              _directory_as_html
              216  LOAD_FAST                'filepath'
              218  CALL_METHOD_1         1  ''

 L. 629       220  LOAD_STR                 'text/html'

 L. 628       222  LOAD_CONST               ('text', 'content_type')
              224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              226  POP_BLOCK        
              228  RETURN_VALUE     
            230_0  COME_FROM_FINALLY   208  '208'

 L. 630       230  DUP_TOP          
              232  LOAD_GLOBAL              PermissionError
              234  COMPARE_OP               exception-match
          236_238  POP_JUMP_IF_FALSE   256  'to 256'
              240  POP_TOP          
              242  POP_TOP          
              244  POP_TOP          

 L. 631       246  LOAD_GLOBAL              HTTPForbidden
              248  CALL_FUNCTION_0       0  ''
              250  RAISE_VARARGS_1       1  'exception instance'
              252  POP_EXCEPT       
              254  JUMP_FORWARD        258  'to 258'
            256_0  COME_FROM           236  '236'
              256  END_FINALLY      
            258_0  COME_FROM           254  '254'
              258  JUMP_FORWARD        266  'to 266'
            260_0  COME_FROM           204  '204'

 L. 633       260  LOAD_GLOBAL              HTTPForbidden
              262  CALL_FUNCTION_0       0  ''
              264  RAISE_VARARGS_1       1  'exception instance'
            266_0  COME_FROM           258  '258'
              266  JUMP_FORWARD        296  'to 296'
            268_0  COME_FROM           196  '196'

 L. 634       268  LOAD_FAST                'filepath'
              270  LOAD_METHOD              is_file
              272  CALL_METHOD_0         0  ''
          274_276  POP_JUMP_IF_FALSE   292  'to 292'

 L. 635       278  LOAD_GLOBAL              FileResponse
              280  LOAD_FAST                'filepath'
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                _chunk_size
              286  LOAD_CONST               ('chunk_size',)
              288  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              290  RETURN_VALUE     
            292_0  COME_FROM           274  '274'

 L. 637       292  LOAD_GLOBAL              HTTPNotFound
              294  RAISE_VARARGS_1       1  'exception instance'
            296_0  COME_FROM           266  '266'

Parse error at or near `POP_TOP' instruction at offset 242

    def _directory_as_html(self, filepath: Path) -> str:
        assert filepath.is_dir()
        relative_path_to_dir = filepath.relative_to(self._directory).as_posix()
        index_of = 'Index of /{}'.format(relative_path_to_dir)
        h1 = '<h1>{}</h1>'.format(index_of)
        index_list = []
        dir_index = filepath.iterdir()
        for _file in sorted(dir_index):
            rel_path = _file.relative_to(self._directory).as_posix()
            file_url = self._prefix + '/' + rel_path
            if _file.is_dir():
                file_name = '{}/'.format(_file.name)
            else:
                file_name = _file.name
            index_list.append('<li><a href="{url}">{name}</a></li>'.format(url=file_url, name=file_name))
        else:
            ul = '<ul>\n{}\n</ul>'.format('\n'.join(index_list))
            body = '<body>\n{}\n{}\n</body>'.format(h1, ul)
            head_str = '<head>\n<title>{}</title>\n</head>'.format(index_of)
            html = '<html>\n{}\n{}\n</html>'.format(head_str, body)
            return html

    def __repr__(self) -> str:
        name = "'" + self.name + "'" if self.name is not None else ''
        return '<StaticResource {name} {path} -> {directory!r}>'.format(name=name,
          path=(self._prefix),
          directory=(self._directory))


class PrefixedSubAppResource(PrefixResource):

    def __init__(self, prefix, app):
        super().__init__(prefix)
        self._app = app
        for resource in app.router.resources():
            resource.add_prefix(prefix)

    def add_prefix(self, prefix):
        super().add_prefix(prefix)
        for resource in self._app.router.resources():
            resource.add_prefix(prefix)

    def url_for(self, *args: str, **kwargs: str) -> URL:
        raise RuntimeError('.url_for() is not supported by sub-application root')

    def get_info(self) -> Dict[(str, Any)]:
        return {'app':self._app,  'prefix':self._prefix}

    async def resolve(self, request: Request) -> _Resolve:
        if not request.url.raw_path.startswith(self._prefix + '/'):
            if request.url.raw_path != self._prefix:
                return (None, set())
        else:
            match_info = await self._app.router.resolve(request)
            match_info.add_app(self._app)
            if isinstance(match_info.http_exception, HTTPMethodNotAllowed):
                methods = match_info.http_exception.allowed_methods
            else:
                methods = set()
        return (
         match_info, methods)

    def __len__(self) -> int:
        return len(self._app.router.routes())

    def __iter__(self) -> Iterator[AbstractRoute]:
        return iter(self._app.router.routes())

    def __repr__(self) -> str:
        return '<PrefixedSubAppResource {prefix} -> {app!r}>'.format(prefix=(self._prefix),
          app=(self._app))


class AbstractRuleMatching(abc.ABC):

    @abc.abstractmethod
    async def match(self, request: Request) -> bool:
        """Return bool if the request satisfies the criteria"""
        pass

    @abc.abstractmethod
    def get_info(self) -> Dict[(str, Any)]:
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
        super().__init__()
        self._domain = self.validation(domain)

    @property
    def canonical(self) -> str:
        return self._domain

    def validation(self, domain: str) -> str:
        if not isinstance(domain, str):
            raise TypeError('Domain must be str')
        domain = domain.rstrip('.').lower()
        if not domain:
            raise ValueError('Domain cannot be empty')
        else:
            if '://' in domain:
                raise ValueError('Scheme not supported')
            else:
                url = URL('http://' + domain)
                assert all((self.re_part.fullmatch(x) for x in url.raw_host.split('.'))), 'Domain not valid'
            if url.port == 80:
                return url.raw_host
            return '{}:{}'.format(url.raw_host, url.port)

    async def match(self, request: Request) -> bool:
        host = request.headers.get(hdrs.HOST)
        return host and self.match_domain(host)

    def match_domain(self, host: str) -> bool:
        return host.lower() == self._domain

    def get_info(self) -> Dict[(str, Any)]:
        return {'domain': self._domain}


class MaskDomain(Domain):
    re_part = re.compile('(?!-)[a-z\\d\\*-]{1,63}(?<!-)')

    def __init__(self, domain):
        super().__init__(domain)
        mask = self._domain.replace('.', '\\.').replace('*', '.*')
        self._mask = re.compile(mask)

    @property
    def canonical(self) -> str:
        return self._mask.pattern

    def match_domain(self, host: str) -> bool:
        return self._mask.fullmatch(host) is not None


class MatchedSubAppResource(PrefixedSubAppResource):

    def __init__(self, rule: AbstractRuleMatching, app: 'Application') -> None:
        AbstractResource.__init__(self)
        self._prefix = ''
        self._app = app
        self._rule = rule

    @property
    def canonical(self) -> str:
        return self._rule.canonical

    def get_info(self) -> Dict[(str, Any)]:
        return {'app':self._app,  'rule':self._rule}

    async def resolve(self, request: Request) -> _Resolve:
        if not await self._rule.match(request):
            return (
             None, set())
        else:
            match_info = await self._app.router.resolve(request)
            match_info.add_app(self._app)
            if isinstance(match_info.http_exception, HTTPMethodNotAllowed):
                methods = match_info.http_exception.allowed_methods
            else:
                methods = set()
        return (
         match_info, methods)

    def __repr__(self) -> str:
        return '<MatchedSubAppResource -> {app!r}>'.format(app=(self._app))


class ResourceRoute(AbstractRoute):
    __doc__ = 'A route with resource'

    def __init__(self, method, handler, resource, *, expect_handler=None):
        super().__init__(method, handler, expect_handler=expect_handler, resource=resource)

    def __repr__(self) -> str:
        return '<ResourceRoute [{method}] {resource} -> {handler!r}'.format(method=(self.method),
          resource=(self._resource),
          handler=(self.handler))

    @property
    def name(self) -> Optional[str]:
        return self._resource.name

    def url_for(self, *args: str, **kwargs: str) -> URL:
        """Construct url for route with additional params."""
        return (self._resource.url_for)(*args, **kwargs)

    def get_info(self) -> Dict[(str, Any)]:
        return self._resource.get_info()


class SystemRoute(AbstractRoute):

    def __init__(self, http_exception):
        super().__init__(hdrs.METH_ANY, self._handle)
        self._http_exception = http_exception

    def url_for(self, *args: str, **kwargs: str) -> URL:
        raise RuntimeError('.url_for() is not allowed for SystemRoute')

    @property
    def name(self) -> Optional[str]:
        pass

    def get_info(self) -> Dict[(str, Any)]:
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

    async def _iter(self) -> StreamResponse:
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()
        method = getattr(self, self.request.method.lower(), None)
        if method is None:
            self._raise_allowed_methods()
        resp = await method()
        return resp

    def __await__(self) -> Generator[(Any, None, StreamResponse)]:
        return self._iter().__await__()

    def _raise_allowed_methods--- This code section failed: ---

 L. 899         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_SETCOMP             '<code_object <setcomp>>'
                6  LOAD_STR                 'View._raise_allowed_methods.<locals>.<setcomp>'
                8  MAKE_FUNCTION_8          'closure'

 L. 900        10  LOAD_GLOBAL              hdrs
               12  LOAD_ATTR                METH_ALL

 L. 899        14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'allowed_methods'

 L. 901        20  LOAD_GLOBAL              HTTPMethodNotAllowed
               22  LOAD_DEREF               'self'
               24  LOAD_ATTR                request
               26  LOAD_ATTR                method
               28  LOAD_FAST                'allowed_methods'
               30  CALL_FUNCTION_2       2  ''
               32  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `None' instruction at offset -1


class ResourcesView(Sized, Iterable[AbstractResource], Container[AbstractResource]):

    def __init__(self, resources: List[AbstractResource]) -> None:
        self._resources = resources

    def __len__(self) -> int:
        return len(self._resources)

    def __iter__(self) -> Iterator[AbstractResource]:
        (yield from self._resources)
        if False:
            yield None

    def __contains__(self, resource: object) -> bool:
        return resource in self._resources


class RoutesView(Sized, Iterable[AbstractRoute], Container[AbstractRoute]):

    def __init__(self, resources: List[AbstractResource]):
        self._routes = []
        for resource in resources:
            for route in resource:
                self._routes.append(route)

    def __len__(self) -> int:
        return len(self._routes)

    def __iter__(self) -> Iterator[AbstractRoute]:
        (yield from self._routes)
        if False:
            yield None

    def __contains__(self, route: object) -> bool:
        return route in self._routes


class UrlDispatcher(AbstractRouter, Mapping[(str, AbstractResource)]):
    NAME_SPLIT_RE = re.compile('[.:-]')

    def __init__(self):
        super().__init__()
        self._resources = []
        self._named_resources = {}

    async def resolve(self, request: Request) -> AbstractMatchInfo:
        method = request.method
        allowed_methods = set()
        for resource in self._resources:
            match_dict, allowed = await resource.resolve(request)
            if match_dict is not None:
                return match_dict
            allowed_methods |= allowed
        else:
            if allowed_methods:
                return MatchInfoError(HTTPMethodNotAllowed(method, allowed_methods))
            return MatchInfoError(HTTPNotFound())

    def __iter__(self) -> Iterator[str]:
        return iter(self._named_resources)

    def __len__(self) -> int:
        return len(self._named_resources)

    def __contains__(self, resource: object) -> bool:
        return resource in self._named_resources

    def __getitem__(self, name: str) -> AbstractResource:
        return self._named_resources[name]

    def resources(self) -> ResourcesView:
        return ResourcesView(self._resources)

    def routes(self) -> RoutesView:
        return RoutesView(self._resources)

    def named_resources(self) -> Mapping[(str, AbstractResource)]:
        return MappingProxyType(self._named_resources)

    def register_resource(self, resource: AbstractResource) -> None:
        assert isinstance(resource, AbstractResource), 'Instance of AbstractResource class is required, got {!r}'.format(resource)
        if self.frozen:
            raise RuntimeError('Cannot register a resource into frozen router.')
        name = resource.name
        if name is not None:
            parts = self.NAME_SPLIT_RE.split(name)
            for part in parts:
                if not part.isidentifier() or keyword.iskeyword(part):
                    raise ValueError('Incorrect route name {!r}, the name should be a sequence of python identifiers separated by dash, dot or column'.format(name))
            else:
                if name in self._named_resources:
                    raise ValueError('Duplicate {!r}, already handled by {!r}'.format(name, self._named_resources[name]))
                self._named_resources[name] = resource

        self._resources.append(resource)

    def add_resource(self, path: str, *, name: Optional[str]=None) -> Resource:
        if path:
            if not path.startswith('/'):
                raise ValueError('path should be started with / or be empty')
            elif self._resources:
                resource = self._resources[(-1)]
                if resource.name == name and resource.raw_match(path):
                    return cast(Resource, resource)
        elif not '{' in path:
            if not '}' in path:
                if not ROUTE_RE.search(path):
                    url = URL.build(path=path)
                    resource = PlainResource((url.raw_path), name=name)
                    self.register_resource(resource)
                    return resource
        resource = DynamicResource(path, name=name)
        self.register_resource(resource)
        return resource

    def add_route(self, method: str, path: str, handler: Union[(_WebHandler, Type[AbstractView])], *, name: Optional[str]=None, expect_handler: Optional[_ExpectHandler]=None) -> AbstractRoute:
        resource = self.add_resource(path, name=name)
        return resource.add_route(method, handler, expect_handler=expect_handler)

    def add_static(self, prefix: str, path: PathLike, *, name: Optional[str]=None, expect_handler: Optional[_ExpectHandler]=None, chunk_size: int=262144, show_index: bool=False, follow_symlinks: bool=False, append_version: bool=False) -> AbstractResource:
        """Add static files view.

        prefix - url prefix
        path - folder with files

        """
        assert prefix.startswith('/')
        if prefix.endswith('/'):
            prefix = prefix[:-1]
        resource = StaticResource(prefix, path, name=name,
          expect_handler=expect_handler,
          chunk_size=chunk_size,
          show_index=show_index,
          follow_symlinks=follow_symlinks,
          append_version=append_version)
        self.register_resource(resource)
        return resource

    def add_head(self, path: str, handler: _WebHandler, **kwargs: Any) -> AbstractRoute:
        """
        Shortcut for add_route with method HEAD
        """
        return (self.add_route)((hdrs.METH_HEAD), path, handler, **kwargs)

    def add_options(self, path: str, handler: _WebHandler, **kwargs: Any) -> AbstractRoute:
        """
        Shortcut for add_route with method OPTIONS
        """
        return (self.add_route)((hdrs.METH_OPTIONS), path, handler, **kwargs)

    def add_get(self, path: str, handler: _WebHandler, *, name: Optional[str]=None, allow_head: bool=True, **kwargs: Any) -> AbstractRoute:
        """
        Shortcut for add_route with method GET, if allow_head is true another
        route is added allowing head requests to the same endpoint
        """
        resource = self.add_resource(path, name=name)
        if allow_head:
            (resource.add_route)((hdrs.METH_HEAD), handler, **kwargs)
        return (resource.add_route)((hdrs.METH_GET), handler, **kwargs)

    def add_post(self, path: str, handler: _WebHandler, **kwargs: Any) -> AbstractRoute:
        """
        Shortcut for add_route with method POST
        """
        return (self.add_route)((hdrs.METH_POST), path, handler, **kwargs)

    def add_put(self, path: str, handler: _WebHandler, **kwargs: Any) -> AbstractRoute:
        """
        Shortcut for add_route with method PUT
        """
        return (self.add_route)((hdrs.METH_PUT), path, handler, **kwargs)

    def add_patch(self, path: str, handler: _WebHandler, **kwargs: Any) -> AbstractRoute:
        """
        Shortcut for add_route with method PATCH
        """
        return (self.add_route)((hdrs.METH_PATCH), path, handler, **kwargs)

    def add_delete(self, path: str, handler: _WebHandler, **kwargs: Any) -> AbstractRoute:
        """
        Shortcut for add_route with method DELETE
        """
        return (self.add_route)((hdrs.METH_DELETE), path, handler, **kwargs)

    def add_view(self, path: str, handler: Type[AbstractView], **kwargs: Any) -> AbstractRoute:
        """
        Shortcut for add_route with ANY methods for a class-based view
        """
        return (self.add_route)((hdrs.METH_ANY), path, handler, **kwargs)

    def freeze(self):
        super().freeze()
        for resource in self._resources:
            resource.freeze()

    def add_routes(self, routes: Iterable[AbstractRouteDef]) -> None:
        """Append routes to route table.

        Parameter should be a sequence of RouteDef objects.
        """
        for route_def in routes:
            route_def.register(self)