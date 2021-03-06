# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\yarl\__init__.py
import sys, warnings
from collections.abc import Mapping, Sequence
from ipaddress import ip_address
from urllib.parse import SplitResult, parse_qsl, urljoin, urlsplit, urlunsplit
from multidict import MultiDict, MultiDictProxy
import idna
from .quoting import _Quoter, _Unquoter
__version__ = '1.4.2'
__all__ = ('URL', )
DEFAULT_PORTS = {'http':80, 
 'https':443,  'ws':80,  'wss':443}
sentinel = object()

class cached_property:
    __doc__ = 'Use as a class method decorator.  It operates almost exactly like\n    the Python `@property` decorator, but it puts the result of the\n    method it decorates into the instance dict after the first call,\n    effectively replacing the function it decorates with an instance\n    variable.  It is, in Python parlance, a data descriptor.\n\n    '

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except AttributeError:
            self.__doc__ = ''
        else:
            self.name = wrapped.__name__

    def __get__(self, inst, owner, _sentinel=sentinel):
        if inst is None:
            return self
        val = inst._cache.get(self.name, _sentinel)
        if val is not _sentinel:
            return val
        val = self.wrapped(inst)
        inst._cache[self.name] = val
        return val

    def __set__(self, inst, value):
        raise AttributeError('cached property is read-only')


class URL:
    __slots__ = ('_cache', '_val')
    _QUOTER = _Quoter()
    _PATH_QUOTER = _Quoter(safe='@:', protected='/+')
    _QUERY_QUOTER = _Quoter(safe='?/:@', protected='=+&;', qs=True)
    _QUERY_PART_QUOTER = _Quoter(safe='?/:@', qs=True)
    _FRAGMENT_QUOTER = _Quoter(safe='?/:@')
    _UNQUOTER = _Unquoter()
    _PATH_UNQUOTER = _Unquoter(unsafe='+')
    _QS_UNQUOTER = _Unquoter(qs=True)

    def __new__(cls, val='', *, encoded=False, strict=None):
        if strict is not None:
            warnings.warn('strict parameter is ignored')
        if type(val) is cls:
            return val
        if type(val) is str:
            val = urlsplit(val)
        else:
            if type(val) is SplitResult:
                if not encoded:
                    raise ValueError('Cannot apply decoding to SplitResult')
                else:
                    if isinstance(val, str):
                        val = urlsplit(str(val))
                    else:
                        raise TypeError('Constructor parameter should be str')
            elif not encoded:
                netloc = val[1] or ''
                host = ''
            else:
                host = val.hostname
                if host is None:
                    raise ValueError('Invalid URL: host is required for absolute urls')
                try:
                    port = val.port
                except ValueError as e:
                    try:
                        raise ValueError("Invalid URL: port can't be converted to integer") from e
                    finally:
                        e = None
                        del e

                else:
                    netloc = cls._make_netloc((val.username),
                      (val.password), host, port, encode=True)
                path = cls._PATH_QUOTER(val[2])
                if netloc:
                    path = cls._normalize_path(path)
                cls._validate_authority_uri_abs_path(host=host, path=path)
                query = cls._QUERY_QUOTER(val[3])
                fragment = cls._FRAGMENT_QUOTER(val[4])
                val = SplitResult(val[0], netloc, path, query, fragment)
            self = object.__new__(cls)
            self._val = val
            self._cache = {}
            return self

    @classmethod
    def build(cls, *, scheme='', user=None, password=None, host='', port=None, path='', query=None, query_string='', fragment='', encoded=False):
        """Creates and returns a new URL"""
        if not host:
            if scheme:
                raise ValueError('Can\'t build URL with "scheme" but without "host".')
        else:
            if port:
                if not host:
                    raise ValueError('Can\'t build URL with "port" but without "host".')
                elif query and query_string:
                    raise ValueError('Only one of "query" or "query_string" should be passed')
                if path is None or query_string is None or fragment is None:
                    raise TypeError('NoneType is illegal for "path", "query_string" and "fragment" args, use string values instead.')
                netloc = user or password or host or port or ''
            else:
                netloc = cls._make_netloc(user, password, host, port, encode=(not encoded))
            path = encoded or cls._PATH_QUOTER(path)
            if netloc:
                path = cls._normalize_path(path)
            cls._validate_authority_uri_abs_path(host=host, path=path)
            query_string = cls._QUERY_QUOTER(query_string)
            fragment = cls._FRAGMENT_QUOTER(fragment)
        url = cls((SplitResult(scheme, netloc, path, query_string, fragment)),
          encoded=True)
        if query:
            return url.with_query(query)
        return url

    def __init_subclass__(cls):
        raise TypeError('Inheritance a class {!r} from URL is forbidden'.format(cls))

    def __str__(self):
        val = self._val
        if not val.path:
            if self.is_absolute():
                if val.query or val.fragment:
                    val = val._replace(path='/')
        return urlunsplit(val)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, str(self))

    def __eq__(self, other):
        if type(other) is not URL:
            return NotImplemented
        else:
            val1 = self._val
            if not val1.path:
                if self.is_absolute():
                    val1 = val1._replace(path='/')
            val2 = other._val
            if not val2.path:
                if other.is_absolute():
                    val2 = val2._replace(path='/')
        return val1 == val2

    def __hash__(self):
        ret = self._cache.get('hash')
        if ret is None:
            val = self._val
            if not val.path:
                if self.is_absolute():
                    val = val._replace(path='/')
            ret = self._cache['hash'] = hash(val)
        return ret

    def __le__(self, other):
        if type(other) is not URL:
            return NotImplemented
        return self._val <= other._val

    def __lt__(self, other):
        if type(other) is not URL:
            return NotImplemented
        return self._val < other._val

    def __ge__(self, other):
        if type(other) is not URL:
            return NotImplemented
        return self._val >= other._val

    def __gt__(self, other):
        if type(other) is not URL:
            return NotImplemented
        return self._val > other._val

    def __truediv__(self, name):
        name = self._PATH_QUOTER(name)
        if name.startswith('/'):
            raise ValueError('Appending path {!r} starting from slash is forbidden'.format(name))
        else:
            path = self._val.path
            if path == '/':
                new_path = '/' + name
            else:
                if not path:
                    new_path = self.is_absolute() or name
                else:
                    parts = path.rstrip('/').split('/')
                    parts.append(name)
                    new_path = '/'.join(parts)
        if self.is_absolute():
            new_path = self._normalize_path(new_path)
        return URL(self._val._replace(path=new_path, query='', fragment=''),
          encoded=True)

    def __bool__(self) -> bool:
        return bool(self._val.netloc or self._val.path or self._val.query or self._val.fragment)

    def __getstate__(self):
        return (
         self._val,)

    def __setstate__(self, state):
        if state[0] is None and isinstance(state[1], dict):
            self._val = state[1]['_val']
        else:
            self._val, *unused = state
        self._cache = {}

    def is_absolute(self):
        """A check for absolute URLs.

        Return True for absolute ones (having scheme or starting
        with //), False otherwise.

        """
        return self.raw_host is not None

    def is_default_port(self):
        """A check for default port.

        Return True if port is default for specified scheme,
        e.g. 'http://python.org' or 'http://python.org:80', False
        otherwise.

        """
        if self.port is None:
            return False
        default = DEFAULT_PORTS.get(self.scheme)
        if default is None:
            return False
        return self.port == default

    def origin(self):
        """Return an URL with scheme, host and port parts only.

        user, password, path, query and fragment are removed.

        """
        if not self.is_absolute():
            raise ValueError('URL should be absolute')
        if not self._val.scheme:
            raise ValueError('URL should have scheme')
        v = self._val
        netloc = self._make_netloc(None, None, (v.hostname), (v.port), encode=False)
        val = v._replace(netloc=netloc, path='', query='', fragment='')
        return URL(val, encoded=True)

    def relative(self):
        """Return a relative part of the URL.

        scheme, user, password, host and port are removed.

        """
        if not self.is_absolute():
            raise ValueError('URL should be absolute')
        val = self._val._replace(scheme='', netloc='')
        return URL(val, encoded=True)

    @property
    def scheme(self):
        """Scheme for absolute URLs.

        Empty string for relative URLs or URLs starting with //

        """
        return self._val.scheme

    @property
    def raw_user(self):
        """Encoded user part of URL.

        None if user is missing.

        """
        ret = self._val.username
        if not ret:
            return
        return ret

    @cached_property
    def user(self):
        """Decoded user part of URL.

        None if user is missing.

        """
        return self._UNQUOTER(self.raw_user)

    @property
    def raw_password(self):
        """Encoded password part of URL.

        None if password is missing.

        """
        return self._val.password

    @cached_property
    def password(self):
        """Decoded password part of URL.

        None if password is missing.

        """
        return self._UNQUOTER(self.raw_password)

    @property
    def raw_host(self):
        """Encoded host part of URL.

        None for relative URLs.

        """
        return self._val.hostname

    @cached_property
    def host--- This code section failed: ---

 L. 445         0  LOAD_FAST                'self'
                2  LOAD_ATTR                raw_host
                4  STORE_FAST               'raw'

 L. 446         6  LOAD_FAST                'raw'
                8  LOAD_CONST               None
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 447        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 448        18  LOAD_STR                 '%'
               20  LOAD_FAST                'raw'
               22  COMPARE_OP               in
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 452        26  LOAD_FAST                'raw'
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 453        30  SETUP_FINALLY        50  'to 50'

 L. 454        32  LOAD_GLOBAL              idna
               34  LOAD_METHOD              decode
               36  LOAD_FAST                'raw'
               38  LOAD_METHOD              encode
               40  LOAD_STR                 'ascii'
               42  CALL_METHOD_1         1  ''
               44  CALL_METHOD_1         1  ''
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    30  '30'

 L. 455        50  DUP_TOP          
               52  LOAD_GLOBAL              UnicodeError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    84  'to 84'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 456        64  LOAD_FAST                'raw'
               66  LOAD_METHOD              encode
               68  LOAD_STR                 'ascii'
               70  CALL_METHOD_1         1  ''
               72  LOAD_METHOD              decode
               74  LOAD_STR                 'idna'
               76  CALL_METHOD_1         1  ''
               78  ROT_FOUR         
               80  POP_EXCEPT       
               82  RETURN_VALUE     
             84_0  COME_FROM            56  '56'
               84  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 60

    @property
    def port(self):
        """Port part of URL, with scheme-based fallback.

        None for relative URLs or URLs without explicit port and
        scheme without default port substitution.

        """
        return self._val.port or DEFAULT_PORTS.get(self._val.scheme)

    @property
    def explicit_port(self):
        """Port part of URL, without scheme-based fallback.

        None for relative URLs or URLs without explicit port.

        """
        return self._val.port

    @property
    def raw_path(self):
        """Encoded path of URL.

        / for absolute URLs without path part.

        """
        ret = self._val.path
        if not ret:
            if self.is_absolute():
                ret = '/'
        return ret

    @cached_property
    def path(self):
        """Decoded path of URL.

        / for absolute URLs without path part.

        """
        return self._PATH_UNQUOTER(self.raw_path)

    @cached_property
    def query(self):
        """A MultiDictProxy representing parsed query parameters in decoded
        representation.

        Empty value if URL has no query part.

        """
        ret = MultiDict(parse_qsl((self.raw_query_string), keep_blank_values=True))
        return MultiDictProxy(ret)

    @property
    def raw_query_string(self):
        """Encoded query part of URL.

        Empty string if query is missing.

        """
        return self._val.query

    @cached_property
    def query_string(self):
        """Decoded query part of URL.

        Empty string if query is missing.

        """
        return self._QS_UNQUOTER(self.raw_query_string)

    @cached_property
    def path_qs(self):
        """Decoded path of URL with query."""
        if not self.query_string:
            return self.path
        return '{}?{}'.format(self.path, self.query_string)

    @cached_property
    def raw_path_qs(self):
        """Encoded path of URL with query."""
        if not self.raw_query_string:
            return self.raw_path
        return '{}?{}'.format(self.raw_path, self.raw_query_string)

    @property
    def raw_fragment(self):
        """Encoded fragment part of URL.

        Empty string if fragment is missing.

        """
        return self._val.fragment

    @cached_property
    def fragment(self):
        """Decoded fragment part of URL.

        Empty string if fragment is missing.

        """
        return self._UNQUOTER(self.raw_fragment)

    @cached_property
    def raw_parts(self):
        """A tuple containing encoded *path* parts.

        ('/',) for absolute URLs if *path* is missing.

        """
        path = self._val.path
        if self.is_absolute():
            if not path:
                parts = [
                 '/']
            else:
                parts = [
                 '/'] + path[1:].split('/')
        elif path.startswith('/'):
            parts = [
             '/'] + path[1:].split('/')
        else:
            parts = path.split('/')
        return tuple(parts)

    @cached_property
    def parts(self):
        """A tuple containing decoded *path* parts.

        ('/',) for absolute URLs if *path* is missing.

        """
        return tuple((self._UNQUOTER(part) for part in self.raw_parts))

    @cached_property
    def parent(self):
        """A new URL with last part of path removed and cleaned up query and
        fragment.

        """
        path = self.raw_path
        if not path or path == '/':
            if self.raw_fragment or self.raw_query_string:
                return URL(self._val._replace(query='', fragment=''), encoded=True)
            return self
        parts = path.split('/')
        val = self._val._replace(path=('/'.join(parts[:-1])), query='', fragment='')
        return URL(val, encoded=True)

    @cached_property
    def raw_name(self):
        """The last part of raw_parts."""
        parts = self.raw_parts
        if self.is_absolute():
            parts = parts[1:]
            if not parts:
                return ''
            return parts[(-1)]
        else:
            return parts[(-1)]

    @cached_property
    def name(self):
        """The last part of parts."""
        return self._UNQUOTER(self.raw_name)

    @staticmethod
    def _validate_authority_uri_abs_path(host, path):
        """Ensure that path in URL with authority starts with a leading slash.

        Raise ValueError if not.
        """
        if len(host) > 0:
            if len(path) > 0:
                if not path.startswith('/'):
                    raise ValueError("Path in a URL with authority should start with a slash ('/') if set")

    @classmethod
    def _normalize_path(cls, path):
        segments = path.split('/')
        resolved_path = []
        for seg in segments:
            if seg == '..':
                try:
                    resolved_path.pop()
                except IndexError:
                    pass

            elif seg == '.':
                continue
            else:
                resolved_path.append(seg)
        else:
            if segments[(-1)] in ('.', '..'):
                resolved_path.append('')
            return '/'.join(resolved_path)

    if sys.version_info >= (3, 7):

        @classmethod
        def _encode_host(cls, host):
            try:
                ip, sep, zone = host.partition('%')
                ip = ip_address(ip)
            except ValueError:
                if host.isascii():
                    return host
                try:
                    host = idna.encode(host, uts46=True).decode('ascii')
                except UnicodeError:
                    host = host.encode('idna').decode('ascii')

            else:
                host = ip.compressed
                if sep:
                    host += '%' + zone
                if ip.version == 6:
                    host = '[' + host + ']'
            return host

    else:

        @classmethod
        def _encode_host(cls, host):
            try:
                ip, sep, zone = host.partition('%')
                ip = ip_address(ip)
            except ValueError:
                for char in host:
                    if char > '\x7f':
                        break
                    return host
                    try:
                        host = idna.encode(host, uts46=True).decode('ascii')
                    except UnicodeError:
                        host = host.encode('idna').decode('ascii')

            else:
                host = ip.compressed
                if sep:
                    host += '%' + zone
                if ip.version == 6:
                    host = '[' + host + ']'
            return host

    @classmethod
    def _make_netloc(cls, user, password, host, port, encode):
        if encode:
            ret = cls._encode_host(host)
        else:
            ret = host
        if port:
            ret = ret + ':' + str(port)
        elif password is not None:
            if not user:
                user = ''
            else:
                if encode:
                    user = cls._QUOTER(user)
            if encode:
                password = cls._QUOTER(password)
            user = user + ':' + password
        else:
            if user:
                if encode:
                    user = cls._QUOTER(user)
        if user:
            ret = user + '@' + ret
        return ret

    def with_scheme(self, scheme):
        """Return a new URL with scheme replaced."""
        if not isinstance(scheme, str):
            raise TypeError('Invalid scheme type')
        if not self.is_absolute():
            raise ValueError('scheme replacement is not allowed for relative URLs')
        return URL(self._val._replace(scheme=(scheme.lower())), encoded=True)

    def with_user(self, user):
        """Return a new URL with user replaced.

        Autoencode user if needed.

        Clear user/password if user is None.

        """
        val = self._val
        if user is None:
            password = None
        else:
            if isinstance(user, str):
                user = self._QUOTER(user)
                password = val.password
            else:
                raise TypeError('Invalid user type')
        if not self.is_absolute():
            raise ValueError('user replacement is not allowed for relative URLs')
        return URL(self._val._replace(netloc=self._make_netloc(user,
          password, (val.hostname), (val.port), encode=False)),
          encoded=True)

    def with_password(self, password):
        """Return a new URL with password replaced.

        Autoencode password if needed.

        Clear password if argument is None.

        """
        if password is None:
            pass
        elif isinstance(password, str):
            password = self._QUOTER(password)
        else:
            raise TypeError('Invalid password type')
        if not self.is_absolute():
            raise ValueError('password replacement is not allowed for relative URLs')
        val = self._val
        return URL(self._val._replace(netloc=self._make_netloc((val.username),
          password, (val.hostname), (val.port), encode=False)),
          encoded=True)

    def with_host(self, host):
        """Return a new URL with host replaced.

        Autoencode host if needed.

        Changing host for relative URLs is not allowed, use .join()
        instead.

        """
        if not isinstance(host, str):
            raise TypeError('Invalid host type')
        else:
            if not self.is_absolute():
                raise ValueError('host replacement is not allowed for relative URLs')
            assert host, 'host removing is not allowed'
        host = self._encode_host(host)
        val = self._val
        return URL(self._val._replace(netloc=self._make_netloc((val.username),
          (val.password), host, (val.port), encode=False)),
          encoded=True)

    def with_port(self, port):
        """Return a new URL with port replaced.

        Clear port to default if None is passed.

        """
        if port is not None:
            if not isinstance(port, int):
                raise TypeError('port should be int or None, got {}'.format(type(port)))
        if not self.is_absolute():
            raise ValueError('port replacement is not allowed for relative URLs')
        val = self._val
        return URL(self._val._replace(netloc=self._make_netloc((val.username),
          (val.password), (val.hostname), port, encode=False)),
          encoded=True)

    def with_path(self, path, *, encoded=False):
        """Return a new URL with path replaced."""
        if not encoded:
            path = self._PATH_QUOTER(path)
            if self.is_absolute():
                path = self._normalize_path(path)
        elif len(path) > 0 and path[0] != '/':
            path = '/' + path
        return URL(self._val._replace(path=path, query='', fragment=''), encoded=True)

    @staticmethod
    def _query_var(v):
        if isinstance(v, str):
            return v
        if type(v) is int:
            return str(v)
        raise TypeError('Invalid variable type: value should be str or int, got {!r} of type {}'.format(v, type(v)))

    def _get_str_query(self, *args, **kwargs):
        if kwargs:
            if len(args) > 0:
                raise ValueError('Either kwargs or single query parameter must be present')
            query = kwargs
        else:
            if len(args) == 1:
                query = args[0]
            else:
                raise ValueError('Either kwargs or single query parameter must be present')
        if query is None:
            query = ''
        else:
            if isinstance(query, Mapping):
                quoter = self._QUERY_PART_QUOTER
                query = '&'.join((quoter(k) + '=' + quoter(self._query_var(v)) for k, v in query.items()))
            else:
                if isinstance(query, str):
                    query = self._QUERY_QUOTER(query)
                else:
                    if isinstance(query, (bytes, bytearray, memoryview)):
                        raise TypeError('Invalid query type: bytes, bytearray and memoryview are forbidden')
                    else:
                        if isinstance(query, Sequence):
                            quoter = self._QUERY_PART_QUOTER
                            query = '&'.join((quoter(k) + '=' + quoter(self._query_var(v)) for k, v in query))
                        else:
                            raise TypeError('Invalid query type: only str, mapping or sequence of (str, str) pairs is allowed')
        return query

    def with_query(self, *args, **kwargs):
        """Return a new URL with query part replaced.

        Accepts any Mapping (e.g. dict, multidict.MultiDict instances)
        or str, autoencode the argument if needed.

        A sequence of (key, value) pairs is supported as well.

        It also can take an arbitrary number of keyword arguments.

        Clear query if None is passed.

        """
        new_query = (self._get_str_query)(*args, **kwargs)
        return URL(self._val._replace(path=(self._val.path), query=new_query),
          encoded=True)

    def update_query(self, *args, **kwargs):
        """Return a new URL with query part updated."""
        s = (self._get_str_query)(*args, **kwargs)
        new_query = MultiDict(parse_qsl(s, keep_blank_values=True))
        query = MultiDict(self.query)
        query.update(new_query)
        return URL(self._val._replace(query=(self._get_str_query(query))), encoded=True)

    def with_fragment(self, fragment):
        """Return a new URL with fragment replaced.

        Autoencode fragment if needed.

        Clear fragment to default if None is passed.

        """
        if fragment is None:
            raw_fragment = ''
        else:
            if not isinstance(fragment, str):
                raise TypeError('Invalid fragment type')
            else:
                raw_fragment = self._FRAGMENT_QUOTER(fragment)
        if self.raw_fragment == raw_fragment:
            return self
        return URL(self._val._replace(fragment=raw_fragment), encoded=True)

    def with_name(self, name):
        """Return a new URL with name (last part of path) replaced.

        Query and fragment parts are cleaned up.

        Name is encoded if needed.

        """
        if not isinstance(name, str):
            raise TypeError('Invalid name type')
        else:
            if '/' in name:
                raise ValueError('Slash in name is not allowed')
            name = self._PATH_QUOTER(name)
            if name in ('.', '..'):
                raise ValueError('. and .. values are forbidden')
            parts = list(self.raw_parts)
            if self.is_absolute():
                if len(parts) == 1:
                    parts.append(name)
                else:
                    parts[-1] = name
                parts[0] = ''
            else:
                parts[-1] = name
                if parts[0] == '/':
                    parts[0] = ''
        return URL(self._val._replace(path=('/'.join(parts)), query='', fragment=''),
          encoded=True)

    def join(self, url):
        """Join URLs

        Construct a full (???absolute???) URL by combining a ???base URL???
        (self) with another URL (url).

        Informally, this uses components of the base URL, in
        particular the addressing scheme, the network location and
        (part of) the path, to provide missing components in the
        relative URL.

        """
        if not isinstance(url, URL):
            raise TypeError('url should be URL')
        return URL((urljoin(str(self), str(url))), encoded=True)

    def human_repr(self):
        """Return decoded human readable string for URL representation."""
        return urlunsplit(SplitResult(self.scheme, self._make_netloc((self.user),
          (self.password), (self.host), (self._val.port), encode=False), self.path, self.query_string, self.fragment))