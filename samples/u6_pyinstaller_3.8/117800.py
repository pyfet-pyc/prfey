# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\helpers.py
"""Various helper functions"""
import asyncio, base64, binascii, cgi, datetime, functools, inspect, netrc, os, platform, re, sys, time, warnings, weakref
from collections import namedtuple
from contextlib import suppress
from math import ceil
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Dict, Iterable, Iterator, List, Mapping, Optional, Pattern, Set, Tuple, Type, TypeVar, Union, cast
from urllib.parse import quote
from urllib.request import getproxies
import async_timeout, attr
from multidict import MultiDict, MultiDictProxy
from yarl import URL
from . import hdrs
from .log import client_logger, internal_logger
from .typedefs import PathLike
__all__ = ('BasicAuth', 'ChainMapProxy')
PY_36 = sys.version_info >= (3, 6)
PY_37 = sys.version_info >= (3, 7)
PY_38 = sys.version_info >= (3, 8)
if not PY_37:
    import idna_ssl
    idna_ssl.patch_match_hostname()
try:
    from typing import ContextManager
except ImportError:
    from typing_extensions import ContextManager
else:

    def all_tasks(loop: Optional[asyncio.AbstractEventLoop]=None) -> Set['asyncio.Task[Any]']:
        tasks = list(asyncio.Task.all_tasks(loop))
        return {t for t in tasks if not t.done() if not t.done()}


    if PY_37:
        all_tasks = getattr(asyncio, 'all_tasks')
    _T = TypeVar('_T')
    sentinel = object()
    NO_EXTENSIONS = bool(os.environ.get('AIOHTTP_NO_EXTENSIONS'))
    DEBUG = getattr(sys.flags, 'dev_mode', False) or not sys.flags.ignore_environment and bool(os.environ.get('PYTHONASYNCIODEBUG'))
    CHAR = set((chr(i) for i in range(0, 128)))
    CTL = set((chr(i) for i in range(0, 32))) | {chr(127)}
    SEPARATORS = {'(', ')', '<', '>', '@', ',', ';', ':', '\\', '"', '/', '[', ']',
     '?', '=', '{', '}', ' ', chr(9)}
    TOKEN = CHAR ^ CTL ^ SEPARATORS
    coroutines = asyncio.coroutines
    old_debug = coroutines._DEBUG
    coroutines._DEBUG = False

    @asyncio.coroutine
    def noop(*args, **kwargs):
        pass


    async def noop2(*args: Any, **kwargs: Any) -> None:
        pass


    coroutines._DEBUG = old_debug

    class BasicAuth(namedtuple('BasicAuth', ['login', 'password', 'encoding'])):
        __doc__ = 'Http basic authentication helper.'

        def __new__(cls, login, password='', encoding='latin1'):
            if login is None:
                raise ValueError('None is not allowed as login value')
            if password is None:
                raise ValueError('None is not allowed as password value')
            if ':' in login:
                raise ValueError('A ":" is not allowed in login (RFC 1945#section-11.1)')
            return super().__new__(cls, login, password, encoding)

        @classmethod
        def decode(cls, auth_header: str, encoding: str='latin1') -> 'BasicAuth':
            """Create a BasicAuth object from an Authorization HTTP header."""
            try:
                auth_type, encoded_credentials = auth_header.split(' ', 1)
            except ValueError:
                raise ValueError('Could not parse authorization header.')
            else:
                if auth_type.lower() != 'basic':
                    raise ValueError('Unknown authorization method %s' % auth_type)
                try:
                    decoded = base64.b64decode((encoded_credentials.encode('ascii')),
                      validate=True).decode(encoding)
                except binascii.Error:
                    raise ValueError('Invalid base64 encoding.')
                else:
                    try:
                        username, password = decoded.split(':', 1)
                    except ValueError:
                        raise ValueError('Invalid credentials.')
                    else:
                        return cls(username, password, encoding=encoding)

        @classmethod
        def from_url(cls, url: URL, *, encoding: str='latin1') -> Optional['BasicAuth']:
            """Create BasicAuth from url."""
            if not isinstance(url, URL):
                raise TypeError('url should be yarl.URL instance')
            if url.user is None:
                return
            return cls((url.user), (url.password or ''), encoding=encoding)

        def encode(self) -> str:
            """Encode credentials."""
            creds = ('%s:%s' % (self.login, self.password)).encode(self.encoding)
            return 'Basic %s' % base64.b64encode(creds).decode(self.encoding)


    def strip_auth_from_url(url: URL) -> Tuple[(URL, Optional[BasicAuth])]:
        auth = BasicAuth.from_url(url)
        if auth is None:
            return (
             url, None)
        return (url.with_user(None), auth)


    def netrc_from_env--- This code section failed: ---

 L. 195         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                environ
                4  LOAD_METHOD              get
                6  LOAD_STR                 'NETRC'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'netrc_env'

 L. 197        12  LOAD_FAST                'netrc_env'
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE    30  'to 30'

 L. 198        20  LOAD_GLOBAL              Path
               22  LOAD_FAST                'netrc_env'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'netrc_path'
               28  JUMP_FORWARD        120  'to 120'
             30_0  COME_FROM            18  '18'

 L. 200        30  SETUP_FINALLY        44  'to 44'

 L. 201        32  LOAD_GLOBAL              Path
               34  LOAD_METHOD              home
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'home_dir'
               40  POP_BLOCK        
               42  JUMP_FORWARD         96  'to 96'
             44_0  COME_FROM_FINALLY    30  '30'

 L. 202        44  DUP_TOP          
               46  LOAD_GLOBAL              RuntimeError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    94  'to 94'
               52  POP_TOP          
               54  STORE_FAST               'e'
               56  POP_TOP          
               58  SETUP_FINALLY        82  'to 82'

 L. 204        60  LOAD_GLOBAL              client_logger
               62  LOAD_METHOD              debug
               64  LOAD_STR                 'Could not resolve home directory when trying to look for .netrc file: %s'

 L. 205        66  LOAD_FAST                'e'

 L. 204        68  CALL_METHOD_2         2  ''
               70  POP_TOP          

 L. 206        72  POP_BLOCK        
               74  POP_EXCEPT       
               76  CALL_FINALLY         82  'to 82'
               78  LOAD_CONST               None
               80  RETURN_VALUE     
             82_0  COME_FROM            76  '76'
             82_1  COME_FROM_FINALLY    58  '58'
               82  LOAD_CONST               None
               84  STORE_FAST               'e'
               86  DELETE_FAST              'e'
               88  END_FINALLY      
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            50  '50'
               94  END_FINALLY      
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            42  '42'

 L. 208        96  LOAD_FAST                'home_dir'

 L. 209        98  LOAD_GLOBAL              platform
              100  LOAD_METHOD              system
              102  CALL_METHOD_0         0  ''
              104  LOAD_STR                 'Windows'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   114  'to 114'
              110  LOAD_STR                 '_netrc'
              112  JUMP_FORWARD        116  'to 116'
            114_0  COME_FROM           108  '108'
              114  LOAD_STR                 '.netrc'
            116_0  COME_FROM           112  '112'

 L. 208       116  BINARY_TRUE_DIVIDE
              118  STORE_FAST               'netrc_path'
            120_0  COME_FROM            28  '28'

 L. 211       120  SETUP_FINALLY       138  'to 138'

 L. 212       122  LOAD_GLOBAL              netrc
              124  LOAD_METHOD              netrc
              126  LOAD_GLOBAL              str
              128  LOAD_FAST                'netrc_path'
              130  CALL_FUNCTION_1       1  ''
              132  CALL_METHOD_1         1  ''
              134  POP_BLOCK        
              136  RETURN_VALUE     
            138_0  COME_FROM_FINALLY   120  '120'

 L. 213       138  DUP_TOP          
              140  LOAD_GLOBAL              netrc
              142  LOAD_ATTR                NetrcParseError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   184  'to 184'
              148  POP_TOP          
              150  STORE_FAST               'e'
              152  POP_TOP          
              154  SETUP_FINALLY       172  'to 172'

 L. 214       156  LOAD_GLOBAL              client_logger
              158  LOAD_METHOD              warning
              160  LOAD_STR                 'Could not parse .netrc file: %s'
              162  LOAD_FAST                'e'
              164  CALL_METHOD_2         2  ''
              166  POP_TOP          
              168  POP_BLOCK        
              170  BEGIN_FINALLY    
            172_0  COME_FROM_FINALLY   154  '154'
              172  LOAD_CONST               None
              174  STORE_FAST               'e'
              176  DELETE_FAST              'e'
              178  END_FINALLY      
              180  POP_EXCEPT       
              182  JUMP_FORWARD        242  'to 242'
            184_0  COME_FROM           146  '146'

 L. 215       184  DUP_TOP          
              186  LOAD_GLOBAL              OSError
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   240  'to 240'
              192  POP_TOP          
              194  STORE_FAST               'e'
              196  POP_TOP          
              198  SETUP_FINALLY       228  'to 228'

 L. 217       200  LOAD_FAST                'netrc_env'
              202  POP_JUMP_IF_TRUE    212  'to 212'
              204  LOAD_FAST                'netrc_path'
              206  LOAD_METHOD              is_file
              208  CALL_METHOD_0         0  ''
              210  POP_JUMP_IF_FALSE   224  'to 224'
            212_0  COME_FROM           202  '202'

 L. 220       212  LOAD_GLOBAL              client_logger
              214  LOAD_METHOD              warning
              216  LOAD_STR                 'Could not read .netrc file: %s'
              218  LOAD_FAST                'e'
              220  CALL_METHOD_2         2  ''
              222  POP_TOP          
            224_0  COME_FROM           210  '210'
              224  POP_BLOCK        
              226  BEGIN_FINALLY    
            228_0  COME_FROM_FINALLY   198  '198'
              228  LOAD_CONST               None
              230  STORE_FAST               'e'
              232  DELETE_FAST              'e'
              234  END_FINALLY      
              236  POP_EXCEPT       
              238  JUMP_FORWARD        242  'to 242'
            240_0  COME_FROM           190  '190'
              240  END_FINALLY      
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM           182  '182'

Parse error at or near `CALL_FINALLY' instruction at offset 76


    @attr.s(frozen=True, slots=True)
    class ProxyInfo:
        proxy = attr.ib(type=URL)
        proxy_auth = attr.ib(type=(Optional[BasicAuth]))


    def proxies_from_env() -> Dict[(str, ProxyInfo)]:
        proxy_urls = {URL(v):k for k, v in getproxies().items() if k in ('http', 'https') if k in ('http',
                                                                                                   'https')}
        netrc_obj = netrc_from_env()
        stripped = {strip_auth_from_url(v):k for k, v in proxy_urls.items()}
        ret = {}
        for proto, val in stripped.items():
            proxy, auth = val
            if proxy.scheme == 'https':
                client_logger.warning('HTTPS proxies %s are not supported, ignoring', proxy)
            else:
                if netrc_obj:
                    if auth is None:
                        auth_from_netrc = None
                        if proxy.host is not None:
                            auth_from_netrc = netrc_obj.authenticators(proxy.host)
                        if auth_from_netrc is not None:
                            *logins, password = auth_from_netrc
                            login = logins[0] if logins[0] else logins[(-1)]
                            auth = BasicAuth(cast(str, login), cast(str, password))
                ret[proto] = ProxyInfo(proxy, auth)
        else:
            return ret


    def current_task(loop: Optional[asyncio.AbstractEventLoop]=None) -> asyncio.Task:
        if PY_37:
            return asyncio.current_task(loop=loop)
        return asyncio.Task.current_task(loop=loop)


    def get_running_loop(loop: Optional[asyncio.AbstractEventLoop]=None) -> asyncio.AbstractEventLoop:
        if loop is None:
            loop = asyncio.get_event_loop()
        if not loop.is_running():
            warnings.warn('The object should be created from async function', DeprecationWarning,
              stacklevel=3)
            if loop.get_debug():
                internal_logger.warning('The object should be created from async function',
                  stack_info=True)
        return loop


    def isasyncgenfunction(obj: Any) -> bool:
        func = getattr(inspect, 'isasyncgenfunction', None)
        if func is not None:
            return func(obj)
        return False


    @attr.s(frozen=True, slots=True)
    class MimeType:
        type = attr.ib(type=str)
        subtype = attr.ib(type=str)
        suffix = attr.ib(type=str)
        parameters = attr.ib(type=MultiDictProxy)


    @functools.lru_cache(maxsize=56)
    def parse_mimetype(mimetype: str) -> MimeType:
        """Parses a MIME type into its components.

    mimetype is a MIME type string.

    Returns a MimeType object.

    Example:

    >>> parse_mimetype('text/html; charset=utf-8')
    MimeType(type='text', subtype='html', suffix='',
             parameters={'charset': 'utf-8'})

    """
        if not mimetype:
            return MimeType(type='', subtype='', suffix='', parameters=(MultiDictProxy(MultiDict())))
        parts = mimetype.split(';')
        params = MultiDict()
        for item in parts[1:]:
            if not item:
                pass
            else:
                key, value = cast(Tuple[(str, str)], item.split('=', 1) if '=' in item else (item, ''))
                params.add(key.lower().strip(), value.strip(' "'))
        else:
            fulltype = parts[0].strip().lower()
            if fulltype == '*':
                fulltype = '*/*'
            mtype, stype = cast(Tuple[(str, str)], fulltype.split('/', 1)) if '/' in fulltype else (fulltype, '')
            stype, suffix = cast(Tuple[(str, str)], stype.split('+', 1)) if '+' in stype else (stype, '')
            return MimeType(type=mtype, subtype=stype, suffix=suffix, parameters=(MultiDictProxy(params)))


    def guess_filename(obj: Any, default: Optional[str]=None) -> Optional[str]:
        name = getattr(obj, 'name', None)
        if name:
            if isinstance(name, str):
                if name[0] != '<':
                    if name[(-1)] != '>':
                        return Path(name).name
        return default


    def content_disposition_header(disptype: str, quote_fields: bool=True, **params: str) -> str:
        """Sets ``Content-Disposition`` header.

    disptype is a disposition type: inline, attachment, form-data.
    Should be valid extension token (see RFC 2183)

    params is a dict with disposition params.
    """
        if not (disptype and TOKEN > set(disptype)):
            raise ValueError('bad content disposition type {!r}'.format(disptype))
        value = disptype
        if params:
            lparams = []
            for key, val in params.items():
                if key:
                    if not TOKEN > set(key):
                        raise ValueError('bad content disposition parameter {!r}={!r}'.format(key, val))
                    qval = quote(val, '') if quote_fields else val
                    lparams.append((key, '"%s"' % qval))
                    if key == 'filename':
                        lparams.append(('filename*', "utf-8''" + qval))
                sparams = '; '.join(('='.join(pair) for pair in lparams))
                value = '; '.join((value, sparams))

        return value


    class reify:
        __doc__ = 'Use as a class method decorator.  It operates almost exactly like\n    the Python `@property` decorator, but it puts the result of the\n    method it decorates into the instance dict after the first call,\n    effectively replacing the function it decorates with an instance\n    variable.  It is, in Python parlance, a data descriptor.\n\n    '

        def __init__(self, wrapped: Callable[(..., Any)]) -> None:
            self.wrapped = wrapped
            self.__doc__ = wrapped.__doc__
            self.name = wrapped.__name__

        def __get__--- This code section failed: ---

 L. 389         0  SETUP_FINALLY        72  'to 72'

 L. 390         2  SETUP_FINALLY        20  'to 20'

 L. 391         4  LOAD_FAST                'inst'
                6  LOAD_ATTR                _cache
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                name
               12  BINARY_SUBSCR    
               14  POP_BLOCK        
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     2  '2'

 L. 392        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    66  'to 66'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 393        34  LOAD_FAST                'self'
               36  LOAD_METHOD              wrapped
               38  LOAD_FAST                'inst'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'val'

 L. 394        44  LOAD_FAST                'val'
               46  LOAD_FAST                'inst'
               48  LOAD_ATTR                _cache
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                name
               54  STORE_SUBSCR     

 L. 395        56  LOAD_FAST                'val'
               58  ROT_FOUR         
               60  POP_EXCEPT       
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM            26  '26'
               66  END_FINALLY      
               68  POP_BLOCK        
               70  JUMP_FORWARD        110  'to 110'
             72_0  COME_FROM_FINALLY     0  '0'

 L. 396        72  DUP_TOP          
               74  LOAD_GLOBAL              AttributeError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   108  'to 108'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 397        86  LOAD_FAST                'inst'
               88  LOAD_CONST               None
               90  COMPARE_OP               is
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 398        94  LOAD_FAST                'self'
               96  ROT_FOUR         
               98  POP_EXCEPT       
              100  RETURN_VALUE     
            102_0  COME_FROM            92  '92'

 L. 399       102  RAISE_VARARGS_0       0  'reraise'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            78  '78'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            70  '70'

Parse error at or near `POP_BLOCK' instruction at offset 16

        def __set__(self, inst: Any, value: Any) -> None:
            raise AttributeError('reified property is read-only')


    reify_py = reify
    try:
        from ._helpers import reify as reify_c
        if not NO_EXTENSIONS:
            reify = reify_c
    except ImportError:
        pass
    else:
        _ipv4_pattern = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        _ipv6_pattern = '^(?:(?:(?:[A-F0-9]{1,4}:){6}|(?=(?:[A-F0-9]{0,4}:){0,6}(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$)(([0-9A-F]{1,4}:){0,5}|:)((:[0-9A-F]{1,4}){1,5}:|:)|::(?:[A-F0-9]{1,4}:){5})(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])|(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}|(?=(?:[A-F0-9]{0,4}:){0,7}[A-F0-9]{0,4}$)(([0-9A-F]{1,4}:){1,7}|:)((:[0-9A-F]{1,4}){1,7}|:)|(?:[A-F0-9]{1,4}:){7}:|:(:[A-F0-9]{1,4}){7})$'
        _ipv4_regex = re.compile(_ipv4_pattern)
        _ipv6_regex = re.compile(_ipv6_pattern, flags=(re.IGNORECASE))
        _ipv4_regexb = re.compile(_ipv4_pattern.encode('ascii'))
        _ipv6_regexb = re.compile((_ipv6_pattern.encode('ascii')), flags=(re.IGNORECASE))

        def _is_ip_address(regex: Pattern[str], regexb: Pattern[bytes], host: Optional[Union[(str, bytes)]]) -> bool:
            if host is None:
                return False
            if isinstance(host, str):
                return bool(regex.match(host))
            if isinstance(host, (bytes, bytearray, memoryview)):
                return bool(regexb.match(host))
            raise TypeError('{} [{}] is not a str or bytes'.format(host, type(host)))


        is_ipv4_address = functools.partial(_is_ip_address, _ipv4_regex, _ipv4_regexb)
        is_ipv6_address = functools.partial(_is_ip_address, _ipv6_regex, _ipv6_regexb)

        def is_ip_address(host: Optional[Union[(str, bytes, bytearray, memoryview)]]) -> bool:
            return is_ipv4_address(host) or is_ipv6_address(host)


        def next_whole_second() -> datetime.datetime:
            """Return current time rounded up to the next whole second."""
            return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) + datetime.timedelta(seconds=0)


        _cached_current_datetime = None
        _cached_formatted_datetime = ''

        def rfc822_formatted_time() -> str:
            global _cached_current_datetime
            global _cached_formatted_datetime
            now = int(time.time())
            if now != _cached_current_datetime:
                _weekdayname = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
                _monthname = ('', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                              'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
                year, month, day, hh, mm, ss, wd, *tail = time.gmtime(now)
                _cached_formatted_datetime = '%s, %02d %3s %4d %02d:%02d:%02d GMT' % (
                 _weekdayname[wd], day, _monthname[month], year, hh, mm, ss)
                _cached_current_datetime = now
            return _cached_formatted_datetime


        def _weakref_handle(info):
            ref, name = info
            ob = ref()
            if ob is not None:
                with suppress(Exception):
                    getattr(ob, name)()


        def weakref_handle(ob, name, timeout, loop, ceil_timeout=True):
            if timeout is not None:
                if timeout > 0:
                    when = loop.time() + timeout
                    if ceil_timeout:
                        when = ceil(when)
                    return loop.call_at(when, _weakref_handle, (weakref.ref(ob), name))


        def call_later(cb, timeout, loop):
            if timeout is not None:
                if timeout > 0:
                    when = ceil(loop.time() + timeout)
                    return loop.call_at(when, cb)


        class TimeoutHandle:
            __doc__ = ' Timeout handle '

            def __init__(self, loop: asyncio.AbstractEventLoop, timeout: Optional[float]) -> None:
                self._timeout = timeout
                self._loop = loop
                self._callbacks = []

            def register(self, callback: Callable[(Ellipsis, None)], *args: Any, **kwargs: Any) -> None:
                self._callbacks.append((callback, args, kwargs))

            def close(self) -> None:
                self._callbacks.clear()

            def start(self) -> Optional[asyncio.Handle]:
                if self._timeout is not None:
                    if self._timeout > 0:
                        at = ceil(self._loop.time() + self._timeout)
                        return self._loop.call_at(at, self.__call__)
                return

            def timer(self) -> 'BaseTimerContext':
                if self._timeout is not None:
                    if self._timeout > 0:
                        timer = TimerContext(self._loop)
                        self.register(timer.timeout)
                        return timer
                return TimerNoop()

            def __call__(self) -> None:
                for cb, args, kwargs in self._callbacks:
                    with suppress(Exception):
                        cb(*args, **kwargs)
                else:
                    self._callbacks.clear()


        class BaseTimerContext(ContextManager['BaseTimerContext']):
            pass


        class TimerNoop(BaseTimerContext):

            def __enter__(self) -> BaseTimerContext:
                return self

            def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> Optional[bool]:
                return False


        class TimerContext(BaseTimerContext):
            __doc__ = ' Low resolution timeout context manager '

            def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
                self._loop = loop
                self._tasks = []
                self._cancelled = False

            def __enter__(self) -> BaseTimerContext:
                task = current_task(loop=(self._loop))
                if task is None:
                    raise RuntimeError('Timeout context manager should be used inside a task')
                if self._cancelled:
                    task.cancel()
                    raise asyncio.TimeoutError from None
                self._tasks.append(task)
                return self

            def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> Optional[bool]:
                if self._tasks:
                    self._tasks.pop()
                if exc_type is asyncio.CancelledError:
                    if self._cancelled:
                        raise asyncio.TimeoutError from None

            def timeout(self) -> None:
                if not self._cancelled:
                    for task in set(self._tasks):
                        task.cancel()
                    else:
                        self._cancelled = True


        class CeilTimeout(async_timeout.timeout):

            def __enter__(self) -> async_timeout.timeout:
                if self._timeout is not None:
                    self._task = current_task(loop=(self._loop))
                    if self._task is None:
                        raise RuntimeError('Timeout context manager should be used inside a task')
                    self._cancel_handler = self._loop.call_at(ceil(self._loop.time() + self._timeout), self._cancel_task)
                return self


        class HeadersMixin:
            ATTRS = frozenset([
             '_content_type', '_content_dict', '_stored_content_type'])
            _content_type = None
            _content_dict = None
            _stored_content_type = sentinel

            def _parse_content_type(self, raw: str) -> None:
                self._stored_content_type = raw
                if raw is None:
                    self._content_type = 'application/octet-stream'
                    self._content_dict = {}
                else:
                    self._content_type, self._content_dict = cgi.parse_header(raw)

            @property
            def content_type(self) -> str:
                """The value of content part for Content-Type HTTP header."""
                raw = self._headers.get(hdrs.CONTENT_TYPE)
                if self._stored_content_type != raw:
                    self._parse_content_type(raw)
                return self._content_type

            @property
            def charset(self) -> Optional[str]:
                """The value of charset part for Content-Type HTTP header."""
                raw = self._headers.get(hdrs.CONTENT_TYPE)
                if self._stored_content_type != raw:
                    self._parse_content_type(raw)
                return self._content_dict.get('charset')

            @property
            def content_length(self) -> Optional[int]:
                """The value of Content-Length HTTP header."""
                content_length = self._headers.get(hdrs.CONTENT_LENGTH)
                if content_length is not None:
                    return int(content_length)
                return


        def set_result(fut: 'asyncio.Future[_T]', result: _T) -> None:
            if not fut.done():
                fut.set_result(result)


        def set_exception(fut: 'asyncio.Future[_T]', exc: BaseException) -> None:
            if not fut.done():
                fut.set_exception(exc)


        class ChainMapProxy(Mapping[(str, Any)]):
            __slots__ = ('_maps', )

            def __init__(self, maps: Iterable[Mapping[(str, Any)]]) -> None:
                self._maps = tuple(maps)

            def __init_subclass__(cls) -> None:
                raise TypeError('Inheritance class {} from ChainMapProxy is forbidden'.format(cls.__name__))

            def __getitem__--- This code section failed: ---

 L. 686         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _maps
                4  GET_ITER         
                6  FOR_ITER             48  'to 48'
                8  STORE_FAST               'mapping'

 L. 687        10  SETUP_FINALLY        26  'to 26'

 L. 688        12  LOAD_FAST                'mapping'
               14  LOAD_FAST                'key'
               16  BINARY_SUBSCR    
               18  POP_BLOCK        
               20  ROT_TWO          
               22  POP_TOP          
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    10  '10'

 L. 689        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 690        40  POP_EXCEPT       
               42  JUMP_BACK             6  'to 6'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
               46  JUMP_BACK             6  'to 6'

 L. 691        48  LOAD_GLOBAL              KeyError
               50  LOAD_FAST                'key'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 20

            def get(self, key: str, default: Any=None) -> Any:
                if key in self:
                    return self[key]
                return default

            def __len__(self) -> int:
                return len((set().union)(*self._maps))

            def __iter__(self) -> Iterator[str]:
                d = {}
                for mapping in reversed(self._maps):
                    d.update(mapping)
                else:
                    return iter(d)

            def __contains__(self, key: object) -> bool:
                return any((key in m for m in self._maps))

            def __bool__(self) -> bool:
                return any(self._maps)

            def __repr__(self) -> str:
                content = ', '.join(map(repr, self._maps))
                return 'ChainMapProxy({})'.format(content)