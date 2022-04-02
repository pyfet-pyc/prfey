# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
        elif type(val) is SplitResult:
            assert encoded, 'Cannot apply decoding to SplitResult'
        elif isinstance(val, str):
            val = urlsplit(str(val))
        else:
            raise TypeError('Constructor parameter should be str')
        if not encoded:
            if not val[1]:
                netloc = ''
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
        if port:
            if not host:
                raise ValueError('Can\'t build URL with "port" but without "host".')
            if query:
                if query_string:
                    raise ValueError('Only one of "query" or "query_string" should be passed')
            if path is None or (query_string is None or fragment is None):
                raise TypeError('NoneType is illegal for "path", "query_string" and "fragment" args, use string values instead.')
            if not (user or password or host or port):
                netloc = ''
            else:
                netloc = cls._make_netloc(user, password, host, port, encode=(not encoded))
            if not encoded:
                path = cls._PATH_QUOTER(path)
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
        if not val.path or self.is_absolute():
            if val.query or (val.fragment):
                val = val._replace(path='/')
            return urlunsplit(val)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, str(self))

    def __eq__(self, other):
        if type(other) is not URL:
            return NotImplemented
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
        path = self._val.path
        if path == '/':
            new_path = '/' + name
        elif not (path or self.is_absolute()):
            new_path = name
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
    def host(self):
        """Decoded host part of URL.

        None for relative URLs.

        """
        raw = self.raw_host
        if raw is None:
            return
        if '%' in raw:
            return raw
        try:
            return idna.decode(raw.encode('ascii'))
        except UnicodeError:
            return raw.encode('ascii').decode('idna')

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
            if self.raw_fragment or (self.raw_query_string):
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
        if not len(host) > 0 or len(path) > 0:
            if not path.startswith('/'):
                raise ValueError("Path in a URL with authority should start with a slash ('/') if set")

    @classmethod
    def _normalize_path--- This code section failed: ---

 L. 636         0  LOAD_FAST                'path'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'segments'

 L. 637        10  BUILD_LIST_0          0 
               12  STORE_FAST               'resolved_path'

 L. 639        14  LOAD_FAST                'segments'
               16  GET_ITER         
             18_0  COME_FROM            88  '88'
             18_1  COME_FROM            76  '76'
             18_2  COME_FROM            74  '74'
             18_3  COME_FROM            64  '64'
               18  FOR_ITER             90  'to 90'
               20  STORE_FAST               'seg'

 L. 640        22  LOAD_FAST                'seg'
               24  LOAD_STR                 '..'
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    66  'to 66'

 L. 641        30  SETUP_FINALLY        44  'to 44'

 L. 642        32  LOAD_FAST                'resolved_path'
               34  LOAD_METHOD              pop
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD         88  'to 88'
             44_0  COME_FROM_FINALLY    30  '30'

 L. 643        44  DUP_TOP          
               46  LOAD_GLOBAL              IndexError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    62  'to 62'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 647        58  POP_EXCEPT       
               60  BREAK_LOOP           88  'to 88'
             62_0  COME_FROM            50  '50'
               62  END_FINALLY      
               64  JUMP_BACK            18  'to 18'
             66_0  COME_FROM            28  '28'

 L. 648        66  LOAD_FAST                'seg'
               68  LOAD_STR                 '.'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    78  'to 78'

 L. 649        74  CONTINUE             18  'to 18'
               76  JUMP_BACK            18  'to 18'
             78_0  COME_FROM            72  '72'

 L. 651        78  LOAD_FAST                'resolved_path'
               80  LOAD_METHOD              append
               82  LOAD_FAST                'seg'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
             88_0  COME_FROM            60  '60'
             88_1  COME_FROM            42  '42'
               88  JUMP_BACK            18  'to 18'
             90_0  COME_FROM            18  '18'

 L. 653        90  LOAD_FAST                'segments'
               92  LOAD_CONST               -1
               94  BINARY_SUBSCR    
               96  LOAD_CONST               ('.', '..')
               98  COMPARE_OP               in
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L. 657       102  LOAD_FAST                'resolved_path'
              104  LOAD_METHOD              append
              106  LOAD_STR                 ''
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
            112_0  COME_FROM           100  '100'

 L. 659       112  LOAD_STR                 '/'
              114  LOAD_METHOD              join
              116  LOAD_FAST                'resolved_path'
              118  CALL_METHOD_1         1  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 62

    if sys.version_info >= (3, 7):

        @classmethod
        def _encode_host(cls, host):
            try:
                ip, sep, zone = host.partition('%')
                ip = ip_address(ip)
            except ValueError:
                if host.isascii():
                    return host
                else:
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
        def _encode_host--- This code section failed: ---

 L. 689         0  SETUP_FINALLY        30  'to 30'

 L. 690         2  LOAD_FAST                'host'
                4  LOAD_METHOD              partition
                6  LOAD_STR                 '%'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_3     3 
               12  STORE_FAST               'ip'
               14  STORE_FAST               'sep'
               16  STORE_FAST               'zone'

 L. 691        18  LOAD_GLOBAL              ip_address
               20  LOAD_FAST                'ip'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'ip'
               26  POP_BLOCK        
               28  JUMP_FORWARD        142  'to 142'
             30_0  COME_FROM_FINALLY     0  '0'

 L. 692        30  DUP_TOP          
               32  LOAD_GLOBAL              ValueError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE   140  'to 140'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 693        44  LOAD_FAST                'host'
               46  GET_ITER         
             48_0  COME_FROM            64  '64'
             48_1  COME_FROM            58  '58'
               48  FOR_ITER             66  'to 66'
               50  STORE_FAST               'char'

 L. 694        52  LOAD_FAST                'char'
               54  LOAD_STR                 '\x7f'
               56  COMPARE_OP               >
               58  POP_JUMP_IF_FALSE_BACK    48  'to 48'

 L. 695        60  POP_TOP          
               62  BREAK_LOOP           74  'to 74'
               64  JUMP_BACK            48  'to 48'
             66_0  COME_FROM            48  '48'

 L. 697        66  LOAD_FAST                'host'
               68  ROT_FOUR         
               70  POP_EXCEPT       
               72  RETURN_VALUE     
             74_0  COME_FROM            62  '62'

 L. 698        74  SETUP_FINALLY       100  'to 100'

 L. 699        76  LOAD_GLOBAL              idna
               78  LOAD_ATTR                encode
               80  LOAD_FAST                'host'
               82  LOAD_CONST               True
               84  LOAD_CONST               ('uts46',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  LOAD_METHOD              decode
               90  LOAD_STR                 'ascii'
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'host'
               96  POP_BLOCK        
               98  JUMP_FORWARD        136  'to 136'
            100_0  COME_FROM_FINALLY    74  '74'

 L. 700       100  DUP_TOP          
              102  LOAD_GLOBAL              UnicodeError
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   134  'to 134'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 701       114  LOAD_FAST                'host'
              116  LOAD_METHOD              encode
              118  LOAD_STR                 'idna'
              120  CALL_METHOD_1         1  ''
              122  LOAD_METHOD              decode
              124  LOAD_STR                 'ascii'
              126  CALL_METHOD_1         1  ''
              128  STORE_FAST               'host'
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM           106  '106'
              134  END_FINALLY      
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM            98  '98'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        186  'to 186'
            140_0  COME_FROM            36  '36'
              140  END_FINALLY      
            142_0  COME_FROM            28  '28'

 L. 703       142  LOAD_FAST                'ip'
              144  LOAD_ATTR                compressed
              146  STORE_FAST               'host'

 L. 704       148  LOAD_FAST                'sep'
              150  POP_JUMP_IF_FALSE   164  'to 164'

 L. 705       152  LOAD_FAST                'host'
              154  LOAD_STR                 '%'
              156  LOAD_FAST                'zone'
              158  BINARY_ADD       
              160  INPLACE_ADD      
              162  STORE_FAST               'host'
            164_0  COME_FROM           150  '150'

 L. 706       164  LOAD_FAST                'ip'
              166  LOAD_ATTR                version
              168  LOAD_CONST               6
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   186  'to 186'

 L. 707       174  LOAD_STR                 '['
              176  LOAD_FAST                'host'
              178  BINARY_ADD       
              180  LOAD_STR                 ']'
              182  BINARY_ADD       
              184  STORE_FAST               'host'
            186_0  COME_FROM           172  '172'
            186_1  COME_FROM           138  '138'

 L. 708       186  LOAD_FAST                'host'
              188  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 140_0

    @classmethod
    def _make_netloc(cls, user, password, host, port, encode):
        if encode:
            ret = cls._encode_host(host)
        else:
            ret = host
        if port:
            ret = ret + ':' + str(port)
        if password is not None:
            if not user:
                user = ''
            elif encode:
                user = cls._QUOTER(user)
            if encode:
                password = cls._QUOTER(password)
            user = user + ':' + password
        elif user:
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
        elif isinstance(user, str):
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
        if not self.is_absolute():
            raise ValueError('host replacement is not allowed for relative URLs')
        if not host:
            raise ValueError('host removing is not allowed')
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
        if len(path) > 0:
            if path[0] != '/':
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
        elif len(args) == 1:
            query = args[0]
        else:
            raise ValueError('Either kwargs or single query parameter must be present')
        if query is None:
            query = ''
        elif isinstance(query, Mapping):
            quoter = self._QUERY_PART_QUOTER
            query = '&'.join((quoter(k) + '=' + quoter(self._query_var(v)) for k, v in query.items()))
        elif isinstance(query, str):
            query = self._QUERY_QUOTER(query)
        elif isinstance(query, (bytes, bytearray, memoryview)):
            raise TypeError('Invalid query type: bytes, bytearray and memoryview are forbidden')
        elif isinstance(query, Sequence):
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
        elif not isinstance(fragment, str):
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

        Construct a full (“absolute”) URL by combining a “base URL”
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