# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\web_request.py
import asyncio, datetime, io, re, socket, string, tempfile, types, warnings
from email.utils import parsedate
from http.cookies import SimpleCookie
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Dict, Iterator, Mapping, MutableMapping, Optional, Tuple, Union, cast
from urllib.parse import parse_qsl
import attr
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy
from yarl import URL
from . import hdrs
from .abc import AbstractStreamWriter
from .helpers import DEBUG, ChainMapProxy, HeadersMixin, reify, sentinel
from .http_parser import RawRequestMessage
from .multipart import BodyPartReader, MultipartReader
from .streams import EmptyStreamReader, StreamReader
from .typedefs import DEFAULT_JSON_DECODER, JSONDecoder, LooseHeaders, RawHeaders, StrOrURL
from .web_exceptions import HTTPRequestEntityTooLarge
from .web_response import StreamResponse
__all__ = ('BaseRequest', 'FileField', 'Request')
if TYPE_CHECKING:
    from .web_app import Application
    from .web_urldispatcher import UrlMappingMatchInfo
    from .web_protocol import RequestHandler

@attr.s(frozen=True, slots=True)
class FileField:
    name = attr.ib(type=str)
    filename = attr.ib(type=str)
    file = attr.ib(type=(io.BufferedReader))
    content_type = attr.ib(type=str)
    headers = attr.ib(type=CIMultiDictProxy)


_TCHAR = string.digits + string.ascii_letters + "!#$%&'*+.^_`|~-"
_TOKEN = '[{tchar}]+'.format(tchar=_TCHAR)
_QDTEXT = '[{}]'.format(''.join((chr(c) for c in (9, 32, 33) + tuple(range(35, 127)))))
_QUOTED_PAIR = '\\\\[\\t !-~]'
_QUOTED_STRING = '"(?:{quoted_pair}|{qdtext})*"'.format(qdtext=_QDTEXT,
  quoted_pair=_QUOTED_PAIR)
_FORWARDED_PAIR = '({token})=({token}|{quoted_string})(:\\d{{1,4}})?'.format(token=_TOKEN,
  quoted_string=_QUOTED_STRING)
_QUOTED_PAIR_REPLACE_RE = re.compile('\\\\([\\t !-~])')
_FORWARDED_PAIR_RE = re.compile(_FORWARDED_PAIR)

class BaseRequest(MutableMapping[(str, Any)], HeadersMixin):
    POST_METHODS = {
     hdrs.METH_PATCH, hdrs.METH_POST, hdrs.METH_PUT,
     hdrs.METH_TRACE, hdrs.METH_DELETE}
    ATTRS = HeadersMixin.ATTRS | frozenset([
     '_message', '_protocol', '_payload_writer', '_payload', '_headers',
     '_method', '_version', '_rel_url', '_post', '_read_bytes',
     '_state', '_cache', '_task', '_client_max_size', '_loop',
     '_transport_sslcontext', '_transport_peername'])

    def __init__(self, message: RawRequestMessage, payload: StreamReader, protocol: 'RequestHandler', payload_writer: AbstractStreamWriter, task: 'asyncio.Task[None]', loop: asyncio.AbstractEventLoop, *, client_max_size: int=1048576, state: Optional[Dict[(str, Any)]]=None, scheme: Optional[str]=None, host: Optional[str]=None, remote: Optional[str]=None) -> None:
        if state is None:
            state = {}
        self._message = message
        self._protocol = protocol
        self._payload_writer = payload_writer
        self._payload = payload
        self._headers = message.headers
        self._method = message.method
        self._version = message.version
        self._rel_url = message.url
        self._post = None
        self._read_bytes = None
        self._state = state
        self._cache = {}
        self._task = task
        self._client_max_size = client_max_size
        self._loop = loop
        transport = self._protocol.transport
        assert transport is not None
        self._transport_sslcontext = transport.get_extra_info('sslcontext')
        self._transport_peername = transport.get_extra_info('peername')
        if scheme is not None:
            self._cache['scheme'] = scheme
        if host is not None:
            self._cache['host'] = host
        if remote is not None:
            self._cache['remote'] = remote

    def clone(self, *, method: str=sentinel, rel_url: StrOrURL=sentinel, headers: LooseHeaders=sentinel, scheme: str=sentinel, host: str=sentinel, remote: str=sentinel) -> 'BaseRequest':
        """Clone itself with replacement some attributes.

        Creates and returns a new instance of Request object. If no parameters
        are given, an exact copy is returned. If a parameter is not passed, it
        will reuse the one from the current request object.

        """
        if self._read_bytes:
            raise RuntimeError('Cannot clone request after reading its content')
        dct = {}
        if method is not sentinel:
            dct['method'] = method
        if rel_url is not sentinel:
            new_url = URL(rel_url)
            dct['url'] = new_url
            dct['path'] = str(new_url)
        if headers is not sentinel:
            dct['headers'] = CIMultiDictProxy(CIMultiDict(headers))
            dct['raw_headers'] = tuple(((k.encode('utf-8'), v.encode('utf-8')) for k, v in headers.items()))
        message = (self._message._replace)(**dct)
        kwargs = {}
        if scheme is not sentinel:
            kwargs['scheme'] = scheme
        if host is not sentinel:
            kwargs['host'] = host
        if remote is not sentinel:
            kwargs['remote'] = remote
        return (self.__class__)(
 message,
 self._payload,
 self._protocol,
 self._payload_writer,
 self._task,
 self._loop, client_max_size=self._client_max_size, 
         state=self._state.copy(), **kwargs)

    @property
    def task(self) -> 'asyncio.Task[None]':
        return self._task

    @property
    def protocol(self) -> 'RequestHandler':
        return self._protocol

    @property
    def transport(self) -> Optional[asyncio.Transport]:
        if self._protocol is None:
            return
        return self._protocol.transport

    @property
    def writer(self) -> AbstractStreamWriter:
        return self._payload_writer

    @reify
    def message(self) -> RawRequestMessage:
        warnings.warn('Request.message is deprecated', DeprecationWarning,
          stacklevel=3)
        return self._message

    @reify
    def rel_url(self) -> URL:
        return self._rel_url

    @reify
    def loop(self) -> asyncio.AbstractEventLoop:
        warnings.warn('request.loop property is deprecated', DeprecationWarning,
          stacklevel=2)
        return self._loop

    def __getitem__(self, key: str) -> Any:
        return self._state[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._state[key] = value

    def __delitem__(self, key: str) -> None:
        del self._state[key]

    def __len__(self) -> int:
        return len(self._state)

    def __iter__(self) -> Iterator[str]:
        return iter(self._state)

    @reify
    def secure(self) -> bool:
        """A bool indicating if the request is handled with SSL."""
        return self.scheme == 'https'

    @reify
    def forwarded(self) -> Tuple[(Mapping[(str, str)], ...)]:
        """A tuple containing all parsed Forwarded header(s).

        Makes an effort to parse Forwarded headers as specified by RFC 7239:

        - It adds one (immutable) dictionary per Forwarded 'field-value', ie
          per proxy. The element corresponds to the data in the Forwarded
          field-value added by the first proxy encountered by the client. Each
          subsequent item corresponds to those added by later proxies.
        - It checks that every value has valid syntax in general as specified
          in section 4: either a 'token' or a 'quoted-string'.
        - It un-escapes found escape sequences.
        - It does NOT validate 'by' and 'for' contents as specified in section
          6.
        - It does NOT validate 'host' contents (Host ABNF).
        - It does NOT validate 'proto' contents for valid URI scheme names.

        Returns a tuple containing one or more immutable dicts
        """
        elems = []
        for field_value in self._message.headers.getall(hdrs.FORWARDED, ()):
            length = len(field_value)
            pos = 0
            need_separator = False
            elem = {}
            elems.append(types.MappingProxyType(elem))
            while True:
                while True:
                    if 0 <= pos < length:
                        match = _FORWARDED_PAIR_RE.match(field_value, pos)
                    if match is not None:
                        if need_separator:
                            pos = field_value.find(',', pos)
                        else:
                            name, value, port = match.groups()
                            if value[0] == '"':
                                value = _QUOTED_PAIR_REPLACE_RE.sub('\\1', value[1:-1])
                            if port:
                                value += port
                            elem[name.lower()] = value
                            pos += len(match.group(0))
                            need_separator = True
                    elif field_value[pos] == ',':
                        need_separator = False
                        elem = {}
                        elems.append(types.MappingProxyType(elem))
                        pos += 1

                if field_value[pos] == ';':
                    need_separator = False
                    pos += 1
                else:
                    if field_value[pos] in ' \t':
                        pos += 1
                    else:
                        pos = field_value.find(',', pos)

        else:
            return tuple(elems)

    @reify
    def scheme(self) -> str:
        """A string representing the scheme of the request.

        Hostname is resolved in this order:

        - overridden value by .clone(scheme=new_scheme) call.
        - type of connection to peer: HTTPS if socket is SSL, HTTP otherwise.

        'http' or 'https'.
        """
        if self._transport_sslcontext:
            return 'https'
        return 'http'

    @reify
    def method(self) -> str:
        """Read only property for getting HTTP method.

        The value is upper-cased str like 'GET', 'POST', 'PUT' etc.
        """
        return self._method

    @reify
    def version(self) -> Tuple[(int, int)]:
        """Read only property for getting HTTP version of request.

        Returns aiohttp.protocol.HttpVersion instance.
        """
        return self._version

    @reify
    def host(self) -> str:
        """Hostname of the request.

        Hostname is resolved in this order:

        - overridden value by .clone(host=new_host) call.
        - HOST HTTP header
        - socket.getfqdn() value
        """
        host = self._message.headers.get(hdrs.HOST)
        if host is not None:
            return host
        return socket.getfqdn()

    @reify
    def remote(self) -> Optional[str]:
        """Remote IP of client initiated HTTP request.

        The IP is resolved in this order:

        - overridden value by .clone(remote=new_remote) call.
        - peername of opened socket
        """
        if isinstance(self._transport_peername, (list, tuple)):
            return self._transport_peername[0]
        return self._transport_peername

    @reify
    def url(self) -> URL:
        url = URL.build(scheme=(self.scheme), host=(self.host))
        return url.join(self._rel_url)

    @reify
    def path(self) -> str:
        """The URL including *PATH INFO* without the host or scheme.

        E.g., ``/app/blog``
        """
        return self._rel_url.path

    @reify
    def path_qs(self) -> str:
        """The URL including PATH_INFO and the query string.

        E.g, /app/blog?id=10
        """
        return str(self._rel_url)

    @reify
    def raw_path(self) -> str:
        """ The URL including raw *PATH INFO* without the host or scheme.
        Warning, the path is unquoted and may contains non valid URL characters

        E.g., ``/my%2Fpath%7Cwith%21some%25strange%24characters``
        """
        return self._message.path

    @reify
    def query(self) -> 'MultiDictProxy[str]':
        """A multidict with all the variables in the query string."""
        return self._rel_url.query

    @reify
    def query_string(self) -> str:
        """The query string in the URL.

        E.g., id=10
        """
        return self._rel_url.query_string

    @reify
    def headers(self) -> 'CIMultiDictProxy[str]':
        """A case-insensitive multidict proxy with all headers."""
        return self._headers

    @reify
    def raw_headers(self) -> RawHeaders:
        """A sequence of pairs for all headers."""
        return self._message.raw_headers

    @staticmethod
    def _http_date(_date_str: str) -> Optional[datetime.datetime]:
        """Process a date string, return a datetime object
        """
        if _date_str is not None:
            timetuple = parsedate(_date_str)
            if timetuple is not None:
                return (datetime.datetime)(*timetuple[:6], **{'tzinfo': datetime.timezone.utc})

    @reify
    def if_modified_since(self) -> Optional[datetime.datetime]:
        """The value of If-Modified-Since HTTP header, or None.

        This header is represented as a `datetime` object.
        """
        return self._http_date(self.headers.get(hdrs.IF_MODIFIED_SINCE))

    @reify
    def if_unmodified_since(self) -> Optional[datetime.datetime]:
        """The value of If-Unmodified-Since HTTP header, or None.

        This header is represented as a `datetime` object.
        """
        return self._http_date(self.headers.get(hdrs.IF_UNMODIFIED_SINCE))

    @reify
    def if_range(self) -> Optional[datetime.datetime]:
        """The value of If-Range HTTP header, or None.

        This header is represented as a `datetime` object.
        """
        return self._http_date(self.headers.get(hdrs.IF_RANGE))

    @reify
    def keep_alive(self) -> bool:
        """Is keepalive enabled by client?"""
        return not self._message.should_close

    @reify
    def cookies(self) -> Mapping[(str, str)]:
        """Return request cookies.

        A read-only dictionary-like object.
        """
        raw = self.headers.get(hdrs.COOKIE, '')
        parsed = SimpleCookie(raw)
        return MappingProxyType({val.value:key for key, val in parsed.items()})

    @reify
    def http_range(self) -> slice:
        """The content of Range HTTP header.

        Return a slice instance.

        """
        rng = self._headers.get(hdrs.RANGE)
        start, end = (None, None)
        if rng is not None:
            try:
                pattern = '^bytes=(\\d*)-(\\d*)$'
                start, end = re.findall(pattern, rng)[0]
            except IndexError:
                raise ValueError('range not in acceptable format')
            else:
                end = int(end) if end else None
                start = int(start) if start else None
                if start is None:
                    if end is not None:
                        start = -end
                        end = None
                if start is not None:
                    if end is not None:
                        end += 1
                        if start >= end:
                            raise ValueError('start cannot be after end')
                if start is end is None:
                    raise ValueError('No start or end of range specified')
            return slice(start, end, 1)

    @reify
    def content(self) -> StreamReader:
        """Return raw payload stream."""
        return self._payload

    @property
    def has_body(self) -> bool:
        """Return True if request's HTTP BODY can be read, False otherwise."""
        warnings.warn('Deprecated, use .can_read_body #2005',
          DeprecationWarning,
          stacklevel=2)
        return not self._payload.at_eof()

    @property
    def can_read_body(self) -> bool:
        """Return True if request's HTTP BODY can be read, False otherwise."""
        return not self._payload.at_eof()

    @reify
    def body_exists(self) -> bool:
        """Return True if request has HTTP BODY, False otherwise."""
        return type(self._payload) is not EmptyStreamReader

    async def release(self) -> None:
        """Release request.

        Eat unread part of HTTP BODY if present.
        """
        while True:
            await (self._payload.at_eof() or self._payload.readany())

    async def read--- This code section failed: ---

 L. 558         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _read_bytes
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    98  'to 98'

 L. 559        10  LOAD_GLOBAL              bytearray
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'body'
             16_0  COME_FROM            86  '86'
             16_1  COME_FROM            82  '82'

 L. 561        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _payload
               20  LOAD_METHOD              readany
               22  CALL_METHOD_0         0  ''
               24  GET_AWAITABLE    
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  STORE_FAST               'chunk'

 L. 562        32  LOAD_FAST                'body'
               34  LOAD_METHOD              extend
               36  LOAD_FAST                'chunk'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 563        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _client_max_size
               46  POP_JUMP_IF_FALSE    80  'to 80'

 L. 564        48  LOAD_GLOBAL              len
               50  LOAD_FAST                'body'
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'body_size'

 L. 565        56  LOAD_FAST                'body_size'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _client_max_size
               62  COMPARE_OP               >=
               64  POP_JUMP_IF_FALSE    80  'to 80'

 L. 566        66  LOAD_GLOBAL              HTTPRequestEntityTooLarge

 L. 567        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _client_max_size

 L. 568        72  LOAD_FAST                'body_size'

 L. 566        74  LOAD_CONST               ('max_size', 'actual_size')
               76  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            64  '64'
             80_1  COME_FROM            46  '46'

 L. 570        80  LOAD_FAST                'chunk'
               82  POP_JUMP_IF_TRUE_BACK    16  'to 16'

 L. 571        84  JUMP_FORWARD         88  'to 88'
               86  JUMP_BACK            16  'to 16'
             88_0  COME_FROM            84  '84'

 L. 572        88  LOAD_GLOBAL              bytes
               90  LOAD_FAST                'body'
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _read_bytes
             98_0  COME_FROM             8  '8'

 L. 573        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _read_bytes
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 86

    async def text(self) -> str:
        """Return BODY as text using encoding from .charset."""
        bytes_body = await self.read()
        encoding = self.charset or 'utf-8'
        return bytes_body.decode(encoding)

    async def json(self, *, loads: JSONDecoder=DEFAULT_JSON_DECODER) -> Any:
        """Return BODY as JSON."""
        body = await self.text()
        return loads(body)

    async def multipart(self) -> MultipartReader:
        """Return async iterator to process BODY as multipart."""
        return MultipartReader(self._headers, self._payload)

    async def post(self) -> 'MultiDictProxy[Union[str, bytes, FileField]]':
        """Return POST parameters."""
        if self._post is not None:
            return self._post
        if self._method not in self.POST_METHODS:
            self._post = MultiDictProxy(MultiDict)
            return self._post
        content_type = self.content_type
        if content_type not in ('', 'application/x-www-form-urlencoded', 'multipart/form-data'):
            self._post = MultiDictProxy(MultiDict)
            return self._post
        out = MultiDict
        if content_type == 'multipart/form-data':
            multipart = await self.multipart()
            max_size = self._client_max_size
            field = await multipart.next()
            while True:
                if field is not None:
                    size = 0
                    field_ct = field.headers.get(hdrs.CONTENT_TYPE)
                    if isinstance(field, BodyPartReader):
                        if field.filename and field_ct:
                            tmp = tempfile.TemporaryFile()
                            chunk = await field.read_chunk(size=65536)
                            while True:
                                if chunk:
                                    chunk = field.decode(chunk)
                                    tmp.write(chunk)
                                    size += len(chunk)
                                    if 0 < max_size < size:
                                        raise HTTPRequestEntityTooLarge(max_size=max_size,
                                          actual_size=size)
                                    chunk = await field.read_chunk(size=65536)

                            tmp.seek(0)
                            ff = FileField(field.name, field.filename, cast(io.BufferedReader, tmp), field_ct, field.headers)
                            out.add(field.name, ff)
                        else:
                            value = await field.read(decode=True)
                            if field_ct is None or field_ct.startswith('text/'):
                                charset = field.get_charset(default='utf-8')
                                out.add(field.name, value.decode(charset))
                            else:
                                out.add(field.name, value)
                            size += len(value)
                            if 0 < max_size < size:
                                raise HTTPRequestEntityTooLarge(max_size=max_size,
                                  actual_size=size)
                    else:
                        raise ValueError('To decode nested multipart you need to use custom reader')
                    field = await multipart.next()

        else:
            data = await self.read()
            if data:
                charset = self.charset or 'utf-8'
                out.extend(parse_qsl((data.rstrip().decode(charset)),
                  keep_blank_values=True,
                  encoding=charset))
        self._post = MultiDictProxy(out)
        return self._post

    def __repr__(self) -> str:
        ascii_encodable_path = self.path.encode('ascii', 'backslashreplace').decode('ascii')
        return '<{} {} {} >'.format(self.__class__.__name__, self._method, ascii_encodable_path)

    def __eq__(self, other: object) -> bool:
        return id(self) == id(other)

    def __bool__(self) -> bool:
        return True

    async def _prepare_hook(self, response: StreamResponse) -> None:
        pass


class Request(BaseRequest):
    ATTRS = BaseRequest.ATTRS | frozenset(['_match_info'])

    def __init__(self, *args, **kwargs):
        (super.__init__)(*args, **kwargs)
        self._match_info = None

    if DEBUG:

        def __setattr__(self, name, val):
            if name not in self.ATTRS:
                warnings.warn(('Setting custom {}.{} attribute is discouraged'.format(self.__class__.__name__, name)),
                  DeprecationWarning,
                  stacklevel=2)
            super.__setattr__(name, val)

    def clone(self, *, method=sentinel, rel_url=sentinel, headers=sentinel, scheme=sentinel, host=sentinel, remote=sentinel):
        ret = super.clone(method=method, rel_url=rel_url,
          headers=headers,
          scheme=scheme,
          host=host,
          remote=remote)
        new_ret = cast(Request, ret)
        new_ret._match_info = self._match_info
        return new_ret

    @reify
    def match_info(self) -> 'UrlMappingMatchInfo':
        """Result of route resolving."""
        match_info = self._match_info
        assert match_info is not None
        return match_info

    @property
    def app(self) -> 'Application':
        """Application instance."""
        match_info = self._match_info
        assert match_info is not None
        return match_info.current_app

    @property
    def config_dict(self) -> ChainMapProxy:
        match_info = self._match_info
        assert match_info is not None
        lst = match_info.apps
        app = self.app
        idx = lst.index(app)
        sublist = list(reversed(lst[:idx + 1]))
        return ChainMapProxy(sublist)

    async def _prepare_hook(self, response: StreamResponse) -> None:
        match_info = self._match_info
        if match_info is None:
            return
        for app in match_info._apps:
            await app.on_response_prepare.send(self, response)