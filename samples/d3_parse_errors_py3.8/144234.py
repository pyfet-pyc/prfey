# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\utils.py
"""
requests.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within Requests
that are also useful for external consumption.

"""
import cgi, codecs, collections, io, os, platform, re, sys, socket, struct, warnings
from . import __version__
from . import certs
from .compat import parse_http_list as _parse_list_header
from .compat import quote, urlparse, bytes, str, OrderedDict, unquote, is_py2, builtin_str, getproxies, proxy_bypass, urlunparse, basestring
from .cookies import RequestsCookieJar, cookiejar_from_dict
from .structures import CaseInsensitiveDict
from .exceptions import InvalidURL
_hush_pyflakes = (
 RequestsCookieJar,)
NETRC_FILES = ('.netrc', '_netrc')
DEFAULT_CA_BUNDLE_PATH = certs.where()

def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""
    if hasattr(d, 'items'):
        d = d.items()
    return d


def super_len(o):
    if hasattr(o, '__len__'):
        return len(o)
    if hasattr(o, 'len'):
        return o.len
    if hasattr(o, 'fileno'):
        try:
            fileno = o.fileno()
        except io.UnsupportedOperation:
            pass
        else:
            return os.fstat(fileno).st_size
        if hasattr(o, 'getvalue'):
            return len(o.getvalue())


def get_netrc_auth--- This code section failed: ---

 L.  73         0  SETUP_FINALLY       228  'to 228'

 L.  74         2  LOAD_CONST               0
                4  LOAD_CONST               ('netrc', 'NetrcParseError')
                6  IMPORT_NAME              netrc
                8  IMPORT_FROM              netrc
               10  STORE_FAST               'netrc'
               12  IMPORT_FROM              NetrcParseError
               14  STORE_FAST               'NetrcParseError'
               16  POP_TOP          

 L.  76        18  LOAD_CONST               None
               20  STORE_FAST               'netrc_path'

 L.  78        22  LOAD_GLOBAL              NETRC_FILES
               24  GET_ITER         
             26_0  COME_FROM           100  '100'
             26_1  COME_FROM            90  '90'
               26  FOR_ITER            102  'to 102'
               28  STORE_FAST               'f'

 L.  79        30  SETUP_FINALLY        54  'to 54'

 L.  80        32  LOAD_GLOBAL              os
               34  LOAD_ATTR                path
               36  LOAD_METHOD              expanduser
               38  LOAD_STR                 '~/{0}'
               40  LOAD_METHOD              format
               42  LOAD_FAST                'f'
               44  CALL_METHOD_1         1  ''
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'loc'
               50  POP_BLOCK        
               52  JUMP_FORWARD         80  'to 80'
             54_0  COME_FROM_FINALLY    30  '30'

 L.  81        54  DUP_TOP          
               56  LOAD_GLOBAL              KeyError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    78  'to 78'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L.  85        68  POP_EXCEPT       
               70  POP_TOP          
               72  POP_BLOCK        
               74  LOAD_CONST               None
               76  RETURN_VALUE     
             78_0  COME_FROM            60  '60'
               78  END_FINALLY      
             80_0  COME_FROM            52  '52'

 L.  87        80  LOAD_GLOBAL              os
               82  LOAD_ATTR                path
               84  LOAD_METHOD              exists
               86  LOAD_FAST                'loc'
               88  CALL_METHOD_1         1  ''
               90  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L.  88        92  LOAD_FAST                'loc'
               94  STORE_FAST               'netrc_path'

 L.  89        96  POP_TOP          
               98  BREAK_LOOP          102  'to 102'
              100  JUMP_BACK            26  'to 26'
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            26  '26'

 L.  92       102  LOAD_FAST                'netrc_path'
              104  LOAD_CONST               None
              106  COMPARE_OP               is
              108  POP_JUMP_IF_FALSE   116  'to 116'

 L.  93       110  POP_BLOCK        
              112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM           108  '108'

 L.  95       116  LOAD_GLOBAL              urlparse
              118  LOAD_FAST                'url'
              120  CALL_FUNCTION_1       1  ''
              122  STORE_FAST               'ri'

 L.  98       124  LOAD_FAST                'ri'
              126  LOAD_ATTR                netloc
              128  LOAD_METHOD              split
              130  LOAD_STR                 ':'
              132  CALL_METHOD_1         1  ''
              134  LOAD_CONST               0
              136  BINARY_SUBSCR    
              138  STORE_FAST               'host'

 L. 100       140  SETUP_FINALLY       200  'to 200'

 L. 101       142  LOAD_FAST                'netrc'
              144  LOAD_FAST                'netrc_path'
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_METHOD              authenticators
              150  LOAD_FAST                'host'
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               '_netrc'

 L. 102       156  LOAD_FAST                '_netrc'
              158  POP_JUMP_IF_FALSE   196  'to 196'

 L. 104       160  LOAD_FAST                '_netrc'
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  POP_JUMP_IF_FALSE   172  'to 172'
              168  LOAD_CONST               0
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           166  '166'
              172  LOAD_CONST               1
            174_0  COME_FROM           170  '170'
              174  STORE_FAST               'login_i'

 L. 105       176  LOAD_FAST                '_netrc'
              178  LOAD_FAST                'login_i'
              180  BINARY_SUBSCR    
              182  LOAD_FAST                '_netrc'
              184  LOAD_CONST               2
              186  BINARY_SUBSCR    
              188  BUILD_TUPLE_2         2 
              190  POP_BLOCK        
              192  POP_BLOCK        
              194  RETURN_VALUE     
            196_0  COME_FROM           158  '158'
              196  POP_BLOCK        
              198  JUMP_FORWARD        224  'to 224'
            200_0  COME_FROM_FINALLY   140  '140'

 L. 106       200  DUP_TOP          
              202  LOAD_FAST                'NetrcParseError'
              204  LOAD_GLOBAL              IOError
              206  BUILD_TUPLE_2         2 
              208  COMPARE_OP               exception-match
              210  POP_JUMP_IF_FALSE   222  'to 222'
              212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          

 L. 109       218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
            222_0  COME_FROM           210  '210'
              222  END_FINALLY      
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           198  '198'
              224  POP_BLOCK        
              226  JUMP_FORWARD        252  'to 252'
            228_0  COME_FROM_FINALLY     0  '0'

 L. 112       228  DUP_TOP          
              230  LOAD_GLOBAL              ImportError
              232  LOAD_GLOBAL              AttributeError
              234  BUILD_TUPLE_2         2 
              236  COMPARE_OP               exception-match
              238  POP_JUMP_IF_FALSE   250  'to 250'
              240  POP_TOP          
              242  POP_TOP          
              244  POP_TOP          

 L. 113       246  POP_EXCEPT       
              248  JUMP_FORWARD        252  'to 252'
            250_0  COME_FROM           238  '238'
              250  END_FINALLY      
            252_0  COME_FROM           248  '248'
            252_1  COME_FROM           226  '226'

Parse error at or near `POP_BLOCK' instruction at offset 72


def guess_filename(obj):
    """Tries to guess the filename of the given object."""
    name = getattr(obj, 'name', None)
    if name:
        if isinstance(name, basestring):
            if name[0] != '<':
                if name[(-1)] != '>':
                    return os.path.basename(name)


def from_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. Unless it can not be represented as such, return an
    OrderedDict, e.g.,

    ::

        >>> from_key_val_list([('key', 'val')])
        OrderedDict([('key', 'val')])
        >>> from_key_val_list('string')
        ValueError: need more than 1 value to unpack
        >>> from_key_val_list({'key': 'val'})
        OrderedDict([('key', 'val')])
    """
    if value is None:
        return
    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')
    return OrderedDict(value)


def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,

    ::

        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list('string')
        ValueError: cannot encode objects that are not 2-tuples.
    """
    if value is None:
        return
    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')
    if isinstance(value, collections.Mapping):
        value = value.items()
    return list(value)


def parse_list_header(value):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Quotes are removed automatically after parsing.

    It basically works like :func:`parse_set_header` just that items
    may appear multiple times and case sensitivity is preserved.

    The return value is a standard :class:`list`:

    >>> parse_list_header('token, "quoted value"')
    ['token', 'quoted value']

    To create a header from the :class:`list` again, use the
    :func:`dump_header` function.

    :param value: a string with a list header.
    :return: :class:`list`
    """
    result = []
    for item in _parse_list_header(value):
        if item[:1] == item[-1:] == '"':
            item = unquote_header_value(item[1:-1])
        else:
            result.append(item)
    else:
        return result


def parse_dict_header(value):
    """Parse lists of key, value pairs as described by RFC 2068 Section 2 and
    convert them into a python dict:

    >>> d = parse_dict_header('foo="is a fish", bar="as well"')
    >>> type(d) is dict
    True
    >>> sorted(d.items())
    [('bar', 'as well'), ('foo', 'is a fish')]

    If there is no value for a key it will be `None`:

    >>> parse_dict_header('key_without_value')
    {'key_without_value': None}

    To create a header from the :class:`dict` again, use the
    :func:`dump_header` function.

    :param value: a string with a dict header.
    :return: :class:`dict`
    """
    result = {}
    for item in _parse_list_header(value):
        if '=' not in item:
            result[item] = None
        else:
            name, value = item.split('=', 1)
            if value[:1] == value[-1:] == '"':
                value = unquote_header_value(value[1:-1])
            result[name] = value
    else:
        return result


def unquote_header_value(value, is_filename=False):
    """Unquotes a header value.  (Reversal of :func:`quote_header_value`).
    This does not use the real unquoting but what browsers are actually
    using for quoting.

    :param value: the header value to unquote.
    """
    if value:
        if value[0] == value[(-1)] == '"':
            value = value[1:-1]
            if not is_filename or value[:2] != '\\\\':
                return value.replace('\\\\', '\\').replace('\\"', '"')
    return value


def dict_from_cookiejar(cj):
    """Returns a key/value dictionary from a CookieJar.

    :param cj: CookieJar object to extract cookies from.
    """
    cookie_dict = {}
    for cookie in cj:
        cookie_dict[cookie.name] = cookie.value
    else:
        return cookie_dict


def add_dict_to_cookiejar(cj, cookie_dict):
    """Returns a CookieJar from a key/value dictionary.

    :param cj: CookieJar to insert cookies into.
    :param cookie_dict: Dict of key/values to insert into CookieJar.
    """
    cj2 = cookiejar_from_dict(cookie_dict)
    cj.update(cj2)
    return cj


def get_encodings_from_content(content):
    """Returns encodings from given content string.

    :param content: bytestring to extract encodings from.
    """
    warnings.warn('In requests 3.0, get_encodings_from_content will be removed. For more information, please see the discussion on issue #2266. (This warning should only appear once.)', DeprecationWarning)
    charset_re = re.compile('<meta.*?charset=["\\\']*(.+?)["\\\'>]', flags=(re.I))
    pragma_re = re.compile('<meta.*?content=["\\\']*;?charset=(.+?)["\\\'>]', flags=(re.I))
    xml_re = re.compile('^<\\?xml.*?encoding=["\\\']*(.+?)["\\\'>]')
    return charset_re.findall(content) + pragma_re.findall(content) + xml_re.findall(content)


def get_encoding_from_headers(headers):
    """Returns encodings from given HTTP Header Dict.

    :param headers: dictionary to extract encoding from.
    """
    content_type = headers.get('content-type')
    if not content_type:
        return
    content_type, params = cgi.parse_header(content_type)
    if 'charset' in params:
        return params['charset'].strip('\'"')
    if 'text' in content_type:
        return 'ISO-8859-1'


def stream_decode_response_unicode(iterator, r):
    """Stream decodes a iterator."""
    if r.encoding is None:
        for item in iterator:
            yield item
        else:
            return

    decoder = codecs.getincrementaldecoder(r.encoding)(errors='replace')
    for chunk in iterator:
        rv = decoder.decode(chunk)
        if rv:
            yield rv
    else:
        rv = decoder.decode(b'', final=True)
        if rv:
            yield rv


def iter_slices(string, slice_length):
    """Iterate over slices of a string."""
    pos = 0
    while True:
        if pos < len(string):
            yield string[pos:pos + slice_length]
            pos += slice_length


def get_unicode_from_response(r):
    """Returns the requested content back in unicode.

    :param r: Response object to get unicode content from.

    Tried:

    1. charset from content-type
    2. fall back and replace all unicode characters

    """
    warnings.warn('In requests 3.0, get_unicode_from_response will be removed. For more information, please see the discussion on issue #2266. (This warning should only appear once.)', DeprecationWarning)
    tried_encodings = []
    encoding = get_encoding_from_headers(r.headers)
    if encoding:
        try:
            return str(r.content, encoding)
        except UnicodeError:
            tried_encodings.append(encoding)

    try:
        return str((r.content), encoding, errors='replace')
    except TypeError:
        return r.content


UNRESERVED_SET = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~')

def unquote_unreserved(uri):
    """Un-escape any percent-escape sequences in a URI that are unreserved
    characters. This leaves all reserved, illegal and non-ASCII bytes encoded.
    """
    parts = uri.split('%')
    for i in range(1, len(parts)):
        h = parts[i][0:2]
        if len(h) == 2 and h.isalnum():
            try:
                c = chr(int(h, 16))
            except ValueError:
                raise InvalidURL("Invalid percent-escape sequence: '%s'" % h)
            else:
                if c in UNRESERVED_SET:
                    parts[i] = c + parts[i][2:]
                else:
                    parts[i] = '%' + parts[i]
        else:
            parts[i] = '%' + parts[i]
    else:
        return ''.join(parts)


def requote_uri(uri):
    """Re-quote the given URI.

    This function passes the given URI through an unquote/quote cycle to
    ensure that it is fully and consistently quoted.
    """
    safe_with_percent = "!#$%&'()*+,/:;=?@[]~"
    safe_without_percent = "!#$&'()*+,/:;=?@[]~"
    try:
        return quote((unquote_unreserved(uri)), safe=safe_with_percent)
    except InvalidURL:
        return quote(uri, safe=safe_without_percent)


def address_in_network(ip, net):
    """
    This function allows you to check if on IP belongs to a network subnet
    Example: returns True if ip = 192.168.1.1 and net = 192.168.1.0/24
             returns False if ip = 192.168.1.1 and net = 192.168.100.0/24
    """
    ipaddr = struct.unpack('=L', socket.inet_aton(ip))[0]
    netaddr, bits = net.split('/')
    netmask = struct.unpack('=L', socket.inet_aton(dotted_netmask(int(bits))))[0]
    network = struct.unpack('=L', socket.inet_aton(netaddr))[0] & netmask
    return ipaddr & netmask == network & netmask


def dotted_netmask(mask):
    """
    Converts mask from /xx format to xxx.xxx.xxx.xxx
    Example: if mask is 24 function returns 255.255.255.0
    """
    bits = 4294967295 ^ (1 << 32 - mask) - 1
    return socket.inet_ntoa(struct.pack('>I', bits))


def is_ipv4_address(string_ip):
    try:
        socket.inet_aton(string_ip)
    except socket.error:
        return False
    else:
        return True


def is_valid_cidr(string_network):
    """Very simple check of the cidr format in no_proxy variable"""
    if string_network.count('/') == 1:
        try:
            mask = int(string_network.split('/')[1])
        except ValueError:
            return False
        else:
            if mask < 1 or (mask > 32):
                return False
            try:
                socket.inet_aton(string_network.split('/')[0])
            except socket.error:
                return False

    else:
        return False
    return True


def should_bypass_proxies(url):
    """
    Returns whether we should bypass proxies or not.
    """
    get_proxy = lambda k: os.environ.get(k) or os.environ.get(k.upper())
    no_proxy = get_proxy('no_proxy')
    netloc = urlparse(url).netloc
    if no_proxy:
        no_proxy = no_proxy.replace(' ', '').split(',')
        ip = netloc.split(':')[0]
        if is_ipv4_address(ip):
            for proxy_ip in no_proxy:
                if is_valid_cidr(proxy_ip):
                    if address_in_network(ip, proxy_ip):
                        return True

        else:
            for host in no_proxy:
                if not netloc.endswith(host):
                    if netloc.split(':')[0].endswith(host):
                        pass
                return True

    try:
        bypass = proxy_bypass(netloc)
    except (TypeError, socket.gaierror):
        bypass = False
    else:
        if bypass:
            return True
        else:
            return False


def get_environ_proxies(url):
    """Return a dict of environment proxies."""
    if should_bypass_proxies(url):
        return {}
    return getproxies()


def default_user_agent(name='python-requests'):
    """Return a string representing the default user agent."""
    _implementation = platform.python_implementation()
    if _implementation == 'CPython':
        _implementation_version = platform.python_version()
    elif _implementation == 'PyPy':
        _implementation_version = '%s.%s.%s' % (sys.pypy_version_info.major,
         sys.pypy_version_info.minor,
         sys.pypy_version_info.micro)
        if sys.pypy_version_info.releaselevel != 'final':
            _implementation_version = ''.join([_implementation_version, sys.pypy_version_info.releaselevel])
    elif _implementation == 'Jython':
        _implementation_version = platform.python_version()
    elif _implementation == 'IronPython':
        _implementation_version = platform.python_version()
    else:
        _implementation_version = 'Unknown'
    try:
        p_system = platform.system()
        p_release = platform.release()
    except IOError:
        p_system = 'Unknown'
        p_release = 'Unknown'
    else:
        return ' '.join(['%s/%s' % (name, __version__),
         '%s/%s' % (_implementation, _implementation_version),
         '%s/%s' % (p_system, p_release)])


def default_headers():
    return CaseInsensitiveDict({'User-Agent':default_user_agent(), 
     'Accept-Encoding':', '.join(('gzip', 'deflate')), 
     'Accept':'*/*', 
     'Connection':'keep-alive'})


def parse_header_links--- This code section failed: ---

 L. 587         0  BUILD_LIST_0          0 
                2  STORE_FAST               'links'

 L. 589         4  LOAD_STR                 ' \'"'
                6  STORE_FAST               'replace_chars'

 L. 591         8  LOAD_GLOBAL              re
               10  LOAD_METHOD              split
               12  LOAD_STR                 ', *<'
               14  LOAD_FAST                'value'
               16  CALL_METHOD_2         2  ''
               18  GET_ITER         
             20_0  COME_FROM           186  '186'
               20  FOR_ITER            188  'to 188'
               22  STORE_FAST               'val'

 L. 592        24  SETUP_FINALLY        46  'to 46'

 L. 593        26  LOAD_FAST                'val'
               28  LOAD_METHOD              split
               30  LOAD_STR                 ';'
               32  LOAD_CONST               1
               34  CALL_METHOD_2         2  ''
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'url'
               40  STORE_FAST               'params'
               42  POP_BLOCK        
               44  JUMP_FORWARD         76  'to 76'
             46_0  COME_FROM_FINALLY    24  '24'

 L. 594        46  DUP_TOP          
               48  LOAD_GLOBAL              ValueError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    74  'to 74'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 595        60  LOAD_FAST                'val'
               62  LOAD_STR                 ''
               64  ROT_TWO          
               66  STORE_FAST               'url'
               68  STORE_FAST               'params'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            52  '52'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            44  '44'

 L. 597        76  BUILD_MAP_0           0 
               78  STORE_FAST               'link'

 L. 599        80  LOAD_FAST                'url'
               82  LOAD_METHOD              strip
               84  LOAD_STR                 '<> \'"'
               86  CALL_METHOD_1         1  ''
               88  LOAD_FAST                'link'
               90  LOAD_STR                 'url'
               92  STORE_SUBSCR     

 L. 601        94  LOAD_FAST                'params'
               96  LOAD_METHOD              split
               98  LOAD_STR                 ';'
              100  CALL_METHOD_1         1  ''
              102  GET_ITER         
            104_0  COME_FROM           174  '174'
              104  FOR_ITER            176  'to 176'
              106  STORE_FAST               'param'

 L. 602       108  SETUP_FINALLY       128  'to 128'

 L. 603       110  LOAD_FAST                'param'
              112  LOAD_METHOD              split
              114  LOAD_STR                 '='
              116  CALL_METHOD_1         1  ''
              118  UNPACK_SEQUENCE_2     2 
              120  STORE_FAST               'key'
              122  STORE_FAST               'value'
              124  POP_BLOCK        
              126  JUMP_FORWARD        154  'to 154'
            128_0  COME_FROM_FINALLY   108  '108'

 L. 604       128  DUP_TOP          
              130  LOAD_GLOBAL              ValueError
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   152  'to 152'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L. 605       142  POP_EXCEPT       
              144  POP_TOP          
              146  JUMP_FORWARD        176  'to 176'
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
            152_0  COME_FROM           134  '134'
              152  END_FINALLY      
            154_0  COME_FROM           150  '150'
            154_1  COME_FROM           126  '126'

 L. 607       154  LOAD_FAST                'value'
              156  LOAD_METHOD              strip
              158  LOAD_FAST                'replace_chars'
              160  CALL_METHOD_1         1  ''
              162  LOAD_FAST                'link'
              164  LOAD_FAST                'key'
              166  LOAD_METHOD              strip
              168  LOAD_FAST                'replace_chars'
              170  CALL_METHOD_1         1  ''
              172  STORE_SUBSCR     
              174  JUMP_BACK           104  'to 104'
            176_0  COME_FROM           146  '146'
            176_1  COME_FROM           104  '104'

 L. 609       176  LOAD_FAST                'links'
              178  LOAD_METHOD              append
              180  LOAD_FAST                'link'
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          
              186  JUMP_BACK            20  'to 20'
            188_0  COME_FROM            20  '20'

 L. 611       188  LOAD_FAST                'links'
              190  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 146


_null = '\x00'.encode('ascii')
_null2 = _null * 2
_null3 = _null * 3

def guess_json_utf(data):
    sample = data[:4]
    if sample in (codecs.BOM_UTF32_LE, codecs.BOM32_BE):
        return 'utf-32'
    if sample[:3] == codecs.BOM_UTF8:
        return 'utf-8-sig'
    if sample[:2] in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE):
        return 'utf-16'
    nullcount = sample.count(_null)
    if nullcount == 0:
        return 'utf-8'
    if nullcount == 2:
        if sample[::2] == _null2:
            return 'utf-16-be'
        if sample[1::2] == _null2:
            return 'utf-16-le'
    if nullcount == 3:
        if sample[:3] == _null3:
            return 'utf-32-be'
        if sample[1:] == _null3:
            return 'utf-32-le'


def prepend_scheme_if_needed(url, new_scheme):
    """Given a URL that may or may not have a scheme, prepend the given scheme.
    Does not replace a present scheme with the one provided as an argument."""
    scheme, netloc, path, params, query, fragment = urlparse(url, new_scheme)
    if not netloc:
        netloc, path = path, netloc
    return urlunparse((scheme, netloc, path, params, query, fragment))


def get_auth_from_url(url):
    """Given a url with authentication components, extract them into a tuple of
    username,password."""
    parsed = urlparse(url)
    try:
        auth = (unquote(parsed.username), unquote(parsed.password))
    except (AttributeError, TypeError):
        auth = ('', '')
    else:
        return auth


def to_native_string(string, encoding='ascii'):
    """
    Given a string object, regardless of type, returns a representation of that
    string in the native string type, encoding and decoding where necessary.
    This assumes ASCII unless told otherwise.
    """
    out = None
    if isinstance(string, builtin_str):
        out = string
    elif is_py2:
        out = string.encode(encoding)
    else:
        out = string.decode(encoding)
    return out


def urldefragauth(url):
    """
    Given a url remove the fragment and the authentication part
    """
    scheme, netloc, path, params, query, fragment = urlparse(url)
    if not netloc:
        netloc, path = path, netloc
    netloc = netloc.rsplit('@', 1)[(-1)]
    return urlunparse((scheme, netloc, path, params, query, ''))