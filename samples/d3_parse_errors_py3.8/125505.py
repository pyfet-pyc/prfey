# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: requests\utils.py
"""
requests.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within Requests
that are also useful for external consumption.
"""
import codecs, contextlib, io, os, re, socket, struct, sys, tempfile, warnings, zipfile
from collections import OrderedDict
from .__version__ import __version__
from . import certs
from ._internal_utils import to_native_string
from .compat import parse_http_list as _parse_list_header
from .compat import quote, urlparse, bytes, str, unquote, getproxies, proxy_bypass, urlunparse, basestring, integer_types, is_py3, proxy_bypass_environment, getproxies_environment, Mapping
from .cookies import cookiejar_from_dict
from .structures import CaseInsensitiveDict
from .exceptions import InvalidURL, InvalidHeader, FileModeWarning, UnrewindableBodyError
NETRC_FILES = ('.netrc', '_netrc')
DEFAULT_CA_BUNDLE_PATH = certs.where()
DEFAULT_PORTS = {'http':80, 
 'https':443}
if sys.platform == 'win32':

    def proxy_bypass_registry(host):
        try:
            if is_py3:
                import winreg
            else:
                import _winreg as winreg
        except ImportError:
            return False
        else:
            try:
                internetSettings = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings')
                proxyEnable = int(winreg.QueryValueEx(internetSettings, 'ProxyEnable')[0])
                proxyOverride = winreg.QueryValueEx(internetSettings, 'ProxyOverride')[0]
            except OSError:
                return False
            else:
                if not (proxyEnable and proxyOverride):
                    return False
                else:
                    proxyOverride = proxyOverride.split(';')
                    for test in proxyOverride:
                        if test == '<local>':
                            if '.' not in host:
                                return True
                        test = test.replace('.', '\\.')
                        test = test.replace('*', '.*')
                        test = test.replace('?', '.')
                        if re.match(test, host, re.I):
                            return True
                    else:
                        return False


    def proxy_bypass(host):
        """Return True, if the host should be bypassed.

        Checks proxy settings gathered from the environment, if specified,
        or the registry.
        """
        if getproxies_environment():
            return proxy_bypass_environment(host)
        return proxy_bypass_registry(host)


def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""
    if hasattr(d, 'items'):
        d = d.items()
    return d


def super_len(o):
    total_length = None
    current_position = 0
    if hasattr(o, '__len__'):
        total_length = len(o)
    elif hasattr(o, 'len'):
        total_length = o.len
    elif hasattr(o, 'fileno'):
        try:
            fileno = o.fileno()
        except io.UnsupportedOperation:
            pass
        else:
            total_length = os.fstat(fileno).st_size
            if 'b' not in o.mode:
                warnings.warn("Requests has determined the content-length for this request using the binary size of the file: however, the file has been opened in text mode (i.e. without the 'b' flag in the mode). This may lead to an incorrect content-length. In Requests 3.0, support will be removed for files in text mode.", FileModeWarning)
    if hasattr(o, 'tell'):
        try:
            current_position = o.tell()
        except (OSError, IOError):
            if total_length is not None:
                current_position = total_length
        else:
            if not hasattr(o, 'seek') or total_length is None:
                try:
                    o.seek(0, 2)
                    total_length = o.tell()
                    o.seek(current_position or 0)
                except (OSError, IOError):
                    total_length = 0
                else:
                    if total_length is None:
                        total_length = 0
        return max(0, total_length - current_position)


def get_netrc_auth--- This code section failed: ---

 L. 172         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                environ
                4  LOAD_METHOD              get
                6  LOAD_STR                 'NETRC'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'netrc_file'

 L. 173        12  LOAD_FAST                'netrc_file'
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 174        20  LOAD_FAST                'netrc_file'
               22  BUILD_TUPLE_1         1 
               24  STORE_FAST               'netrc_locations'
               26  JUMP_FORWARD         42  'to 42'
             28_0  COME_FROM            18  '18'

 L. 176        28  LOAD_GENEXPR             '<code_object <genexpr>>'
               30  LOAD_STR                 'get_netrc_auth.<locals>.<genexpr>'
               32  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               34  LOAD_GLOBAL              NETRC_FILES
               36  GET_ITER         
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'netrc_locations'
             42_0  COME_FROM            26  '26'

 L. 178     42_44  SETUP_FINALLY       302  'to 302'

 L. 179        46  LOAD_CONST               0
               48  LOAD_CONST               ('netrc', 'NetrcParseError')
               50  IMPORT_NAME              netrc
               52  IMPORT_FROM              netrc
               54  STORE_FAST               'netrc'
               56  IMPORT_FROM              NetrcParseError
               58  STORE_FAST               'NetrcParseError'
               60  POP_TOP          

 L. 181        62  LOAD_CONST               None
               64  STORE_FAST               'netrc_path'

 L. 183        66  LOAD_FAST                'netrc_locations'
               68  GET_ITER         
             70_0  COME_FROM           138  '138'
             70_1  COME_FROM           128  '128'
               70  FOR_ITER            140  'to 140'
               72  STORE_FAST               'f'

 L. 184        74  SETUP_FINALLY        92  'to 92'

 L. 185        76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              expanduser
               82  LOAD_FAST                'f'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'loc'
               88  POP_BLOCK        
               90  JUMP_FORWARD        118  'to 118'
             92_0  COME_FROM_FINALLY    74  '74'

 L. 186        92  DUP_TOP          
               94  LOAD_GLOBAL              KeyError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   116  'to 116'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 190       106  POP_EXCEPT       
              108  POP_TOP          
              110  POP_BLOCK        
              112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM            98  '98'
              116  END_FINALLY      
            118_0  COME_FROM            90  '90'

 L. 192       118  LOAD_GLOBAL              os
              120  LOAD_ATTR                path
              122  LOAD_METHOD              exists
              124  LOAD_FAST                'loc'
              126  CALL_METHOD_1         1  ''
              128  POP_JUMP_IF_FALSE_BACK    70  'to 70'

 L. 193       130  LOAD_FAST                'loc'
              132  STORE_FAST               'netrc_path'

 L. 194       134  POP_TOP          
              136  BREAK_LOOP          140  'to 140'
              138  JUMP_BACK            70  'to 70'
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM            70  '70'

 L. 197       140  LOAD_FAST                'netrc_path'
              142  LOAD_CONST               None
              144  COMPARE_OP               is
              146  POP_JUMP_IF_FALSE   154  'to 154'

 L. 198       148  POP_BLOCK        
              150  LOAD_CONST               None
              152  RETURN_VALUE     
            154_0  COME_FROM           146  '146'

 L. 200       154  LOAD_GLOBAL              urlparse
              156  LOAD_FAST                'url'
              158  CALL_FUNCTION_1       1  ''
              160  STORE_FAST               'ri'

 L. 204       162  LOAD_CONST               b':'
              164  STORE_FAST               'splitstr'

 L. 205       166  LOAD_GLOBAL              isinstance
              168  LOAD_FAST                'url'
              170  LOAD_GLOBAL              str
              172  CALL_FUNCTION_2       2  ''
              174  POP_JUMP_IF_FALSE   186  'to 186'

 L. 206       176  LOAD_FAST                'splitstr'
              178  LOAD_METHOD              decode
              180  LOAD_STR                 'ascii'
              182  CALL_METHOD_1         1  ''
              184  STORE_FAST               'splitstr'
            186_0  COME_FROM           174  '174'

 L. 207       186  LOAD_FAST                'ri'
              188  LOAD_ATTR                netloc
              190  LOAD_METHOD              split
              192  LOAD_FAST                'splitstr'
              194  CALL_METHOD_1         1  ''
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  STORE_FAST               'host'

 L. 209       202  SETUP_FINALLY       264  'to 264'

 L. 210       204  LOAD_FAST                'netrc'
              206  LOAD_FAST                'netrc_path'
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_METHOD              authenticators
              212  LOAD_FAST                'host'
              214  CALL_METHOD_1         1  ''
              216  STORE_FAST               '_netrc'

 L. 211       218  LOAD_FAST                '_netrc'
          220_222  POP_JUMP_IF_FALSE   260  'to 260'

 L. 213       224  LOAD_FAST                '_netrc'
              226  LOAD_CONST               0
              228  BINARY_SUBSCR    
              230  POP_JUMP_IF_FALSE   236  'to 236'
              232  LOAD_CONST               0
              234  JUMP_FORWARD        238  'to 238'
            236_0  COME_FROM           230  '230'
              236  LOAD_CONST               1
            238_0  COME_FROM           234  '234'
              238  STORE_FAST               'login_i'

 L. 214       240  LOAD_FAST                '_netrc'
              242  LOAD_FAST                'login_i'
              244  BINARY_SUBSCR    
              246  LOAD_FAST                '_netrc'
              248  LOAD_CONST               2
              250  BINARY_SUBSCR    
              252  BUILD_TUPLE_2         2 
              254  POP_BLOCK        
              256  POP_BLOCK        
              258  RETURN_VALUE     
            260_0  COME_FROM           220  '220'
              260  POP_BLOCK        
              262  JUMP_FORWARD        298  'to 298'
            264_0  COME_FROM_FINALLY   202  '202'

 L. 215       264  DUP_TOP          
              266  LOAD_FAST                'NetrcParseError'
              268  LOAD_GLOBAL              IOError
              270  BUILD_TUPLE_2         2 
              272  COMPARE_OP               exception-match
          274_276  POP_JUMP_IF_FALSE   296  'to 296'
              278  POP_TOP          
              280  POP_TOP          
              282  POP_TOP          

 L. 218       284  LOAD_FAST                'raise_errors'
          286_288  POP_JUMP_IF_FALSE   292  'to 292'

 L. 219       290  RAISE_VARARGS_0       0  'reraise'
            292_0  COME_FROM           286  '286'
              292  POP_EXCEPT       
              294  JUMP_FORWARD        298  'to 298'
            296_0  COME_FROM           274  '274'
              296  END_FINALLY      
            298_0  COME_FROM           294  '294'
            298_1  COME_FROM           262  '262'
              298  POP_BLOCK        
              300  JUMP_FORWARD        328  'to 328'
            302_0  COME_FROM_FINALLY    42  '42'

 L. 222       302  DUP_TOP          
              304  LOAD_GLOBAL              ImportError
              306  LOAD_GLOBAL              AttributeError
              308  BUILD_TUPLE_2         2 
              310  COMPARE_OP               exception-match
          312_314  POP_JUMP_IF_FALSE   326  'to 326'
              316  POP_TOP          
              318  POP_TOP          
              320  POP_TOP          

 L. 223       322  POP_EXCEPT       
              324  JUMP_FORWARD        328  'to 328'
            326_0  COME_FROM           312  '312'
              326  END_FINALLY      
            328_0  COME_FROM           324  '324'
            328_1  COME_FROM           300  '300'

Parse error at or near `POP_BLOCK' instruction at offset 110


def guess_filename(obj):
    """Tries to guess the filename of the given object."""
    name = getattr(obj, 'name', None)
    if name:
        if isinstance(name, basestring):
            if name[0] != '<':
                if name[(-1)] != '>':
                    return os.path.basename(name)


def extract_zipped_paths(path):
    """Replace nonexistent paths that look like they refer to a member of a zip
    archive with the location of an extracted copy of the target, or else
    just return the provided path unchanged.
    """
    if os.path.exists(path):
        return path
    archive, member = os.path.split(path)
    while True:
        if archive:
            archive, prefix = os.path.exists(archive) or os.path.split(archive)
            member = '/'.join([prefix, member])

    if not zipfile.is_zipfile(archive):
        return path
    zip_file = zipfile.ZipFile(archive)
    if member not in zip_file.namelist():
        return path
    tmp = tempfile.gettempdir()
    extracted_path = (os.path.join)(tmp, *member.split('/'))
    if not os.path.exists(extracted_path):
        extracted_path = zip_file.extract(member, path=tmp)
    return extracted_path


def from_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. Unless it can not be represented as such, return an
    OrderedDict, e.g.,

    ::

        >>> from_key_val_list([('key', 'val')])
        OrderedDict([('key', 'val')])
        >>> from_key_val_list('string')
        Traceback (most recent call last):
        ...
        ValueError: cannot encode objects that are not 2-tuples
        >>> from_key_val_list({'key': 'val'})
        OrderedDict([('key', 'val')])

    :rtype: OrderedDict
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
        Traceback (most recent call last):
        ...
        ValueError: cannot encode objects that are not 2-tuples

    :rtype: list
    """
    if value is None:
        return
    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')
    if isinstance(value, Mapping):
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
    :rtype: list
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
    :rtype: dict
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
    :rtype: str
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
    :rtype: dict
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
    :rtype: CookieJar
    """
    return cookiejar_from_dict(cookie_dict, cj)


def get_encodings_from_content(content):
    """Returns encodings from given content string.

    :param content: bytestring to extract encodings from.
    """
    warnings.warn('In requests 3.0, get_encodings_from_content will be removed. For more information, please see the discussion on issue #2266. (This warning should only appear once.)', DeprecationWarning)
    charset_re = re.compile('<meta.*?charset=["\\\']*(.+?)["\\\'>]', flags=(re.I))
    pragma_re = re.compile('<meta.*?content=["\\\']*;?charset=(.+?)["\\\'>]', flags=(re.I))
    xml_re = re.compile('^<\\?xml.*?encoding=["\\\']*(.+?)["\\\'>]')
    return charset_re.findall(content) + pragma_re.findall(content) + xml_re.findall(content)


def _parse_content_type_header(header):
    """Returns content type and parameters from given header

    :param header: string
    :return: tuple containing content type and dictionary of
         parameters
    """
    tokens = header.split(';')
    content_type, params = tokens[0].strip(), tokens[1:]
    params_dict = {}
    items_to_strip = '"\' '
    for param in params:
        param = param.strip()
        if param:
            key, value = param, True
            index_of_equals = param.find('=')
        if index_of_equals != -1:
            key = param[:index_of_equals].strip(items_to_strip)
            value = param[index_of_equals + 1:].strip(items_to_strip)
        else:
            params_dict[key.lower()] = value
    else:
        return (
         content_type, params_dict)


def get_encoding_from_headers(headers):
    """Returns encodings from given HTTP Header Dict.

    :param headers: dictionary to extract encoding from.
    :rtype: str
    """
    content_type = headers.get('content-type')
    if not content_type:
        return
    content_type, params = _parse_content_type_header(content_type)
    if 'charset' in params:
        return params['charset'].strip('\'"')
    if 'text' in content_type:
        return 'ISO-8859-1'
    if 'application/json' in content_type:
        return 'utf-8'


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
    if slice_length is None or slice_length <= 0:
        slice_length = len(string)
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

    :rtype: str
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

    :rtype: str
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

    :rtype: str
    """
    safe_with_percent = "!#$%&'()*+,/:;=?@[]~"
    safe_without_percent = "!#$&'()*+,/:;=?@[]~"
    try:
        return quote((unquote_unreserved(uri)), safe=safe_with_percent)
    except InvalidURL:
        return quote(uri, safe=safe_without_percent)


def address_in_network(ip, net):
    """This function allows you to check if an IP belongs to a network subnet

    Example: returns True if ip = 192.168.1.1 and net = 192.168.1.0/24
             returns False if ip = 192.168.1.1 and net = 192.168.100.0/24

    :rtype: bool
    """
    ipaddr = struct.unpack('=L', socket.inet_aton(ip))[0]
    netaddr, bits = net.split('/')
    netmask = struct.unpack('=L', socket.inet_aton(dotted_netmask(int(bits))))[0]
    network = struct.unpack('=L', socket.inet_aton(netaddr))[0] & netmask
    return ipaddr & netmask == network & netmask


def dotted_netmask(mask):
    """Converts mask from /xx format to xxx.xxx.xxx.xxx

    Example: if mask is 24 function returns 255.255.255.0

    :rtype: str
    """
    bits = 4294967295 ^ (1 << 32 - mask) - 1
    return socket.inet_ntoa(struct.pack('>I', bits))


def is_ipv4_address(string_ip):
    """
    :rtype: bool
    """
    try:
        socket.inet_aton(string_ip)
    except socket.error:
        return False
    else:
        return True


def is_valid_cidr(string_network):
    """
    Very simple check of the cidr format in no_proxy variable.

    :rtype: bool
    """
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


@contextlib.contextmanager
def set_environ(env_name, value):
    """Set the environment variable 'env_name' to 'value'

    Save previous value, yield, and then restore the previous value stored in
    the environment variable 'env_name'.

    If 'value' is None, do nothing"""
    value_changed = value is not None
    if value_changed:
        old_value = os.environ.get(env_name)
        os.environ[env_name] = value
    try:
        yield
    finally:
        if value_changed:
            if old_value is None:
                del os.environ[env_name]
            else:
                os.environ[env_name] = old_value


def should_bypass_proxies(url, no_proxy):
    """
    Returns whether we should bypass proxies or not.

    :rtype: bool
    """
    get_proxy = lambda k: os.environ.get(k) or os.environ.get(k.upper())
    no_proxy_arg = no_proxy
    if no_proxy is None:
        no_proxy = get_proxy('no_proxy')
    parsed = urlparse(url)
    if parsed.hostname is None:
        return True
    if no_proxy:
        no_proxy = (host for host in no_proxy.replace(' ', '').split(',') if host)
        if is_ipv4_address(parsed.hostname):
            for proxy_ip in no_proxy:
                if is_valid_cidr(proxy_ip):
                    if address_in_network(parsed.hostname, proxy_ip):
                        return True
                else:
                    if parsed.hostname == proxy_ip:
                        return True

        else:
            host_with_port = parsed.hostname
            if parsed.port:
                host_with_port += ':{}'.format(parsed.port)
        for host in no_proxy:
            if not parsed.hostname.endswith(host):
                if host_with_port.endswith(host):
                    pass
            return True
        else:
            with set_environ('no_proxy', no_proxy_arg):
                try:
                    bypass = proxy_bypass(parsed.hostname)
                except (TypeError, socket.gaierror):
                    bypass = False

            if bypass:
                return True

        return False


def get_environ_proxies(url, no_proxy=None):
    """
    Return a dict of environment proxies.

    :rtype: dict
    """
    if should_bypass_proxies(url, no_proxy=no_proxy):
        return {}
    return getproxies()


def select_proxy(url, proxies):
    """Select a proxy for the url, if applicable.

    :param url: The url being for the request
    :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs
    """
    proxies = proxies or {}
    urlparts = urlparse(url)
    if urlparts.hostname is None:
        return proxies.get(urlparts.scheme, proxies.get('all'))
    proxy_keys = [
     urlparts.scheme + '://' + urlparts.hostname,
     urlparts.scheme,
     'all://' + urlparts.hostname,
     'all']
    proxy = None
    for proxy_key in proxy_keys:
        if proxy_key in proxies:
            proxy = proxies[proxy_key]
            break
    else:
        return proxy


def default_user_agent(name='python-requests'):
    """
    Return a string representing the default user agent.

    :rtype: str
    """
    return '%s/%s' % (name, __version__)


def default_headers():
    """
    :rtype: requests.structures.CaseInsensitiveDict
    """
    return CaseInsensitiveDict({'User-Agent':default_user_agent(), 
     'Accept-Encoding':', '.join(('gzip', 'deflate')), 
     'Accept':'*/*', 
     'Connection':'keep-alive'})


def parse_header_links--- This code section failed: ---

 L. 837         0  BUILD_LIST_0          0 
                2  STORE_FAST               'links'

 L. 839         4  LOAD_STR                 ' \'"'
                6  STORE_FAST               'replace_chars'

 L. 841         8  LOAD_FAST                'value'
               10  LOAD_METHOD              strip
               12  LOAD_FAST                'replace_chars'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'value'

 L. 842        18  LOAD_FAST                'value'
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L. 843        22  LOAD_FAST                'links'
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 845        26  LOAD_GLOBAL              re
               28  LOAD_METHOD              split
               30  LOAD_STR                 ', *<'
               32  LOAD_FAST                'value'
               34  CALL_METHOD_2         2  ''
               36  GET_ITER         
             38_0  COME_FROM           200  '200'
               38  FOR_ITER            202  'to 202'
               40  STORE_FAST               'val'

 L. 846        42  SETUP_FINALLY        64  'to 64'

 L. 847        44  LOAD_FAST                'val'
               46  LOAD_METHOD              split
               48  LOAD_STR                 ';'
               50  LOAD_CONST               1
               52  CALL_METHOD_2         2  ''
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'url'
               58  STORE_FAST               'params'
               60  POP_BLOCK        
               62  JUMP_FORWARD         94  'to 94'
             64_0  COME_FROM_FINALLY    42  '42'

 L. 848        64  DUP_TOP          
               66  LOAD_GLOBAL              ValueError
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE    92  'to 92'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 849        78  LOAD_FAST                'val'
               80  LOAD_STR                 ''
               82  ROT_TWO          
               84  STORE_FAST               'url'
               86  STORE_FAST               'params'
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
             92_0  COME_FROM            70  '70'
               92  END_FINALLY      
             94_0  COME_FROM            90  '90'
             94_1  COME_FROM            62  '62'

 L. 851        94  LOAD_STR                 'url'
               96  LOAD_FAST                'url'
               98  LOAD_METHOD              strip
              100  LOAD_STR                 '<> \'"'
              102  CALL_METHOD_1         1  ''
              104  BUILD_MAP_1           1 
              106  STORE_FAST               'link'

 L. 853       108  LOAD_FAST                'params'
              110  LOAD_METHOD              split
              112  LOAD_STR                 ';'
              114  CALL_METHOD_1         1  ''
              116  GET_ITER         
            118_0  COME_FROM           188  '188'
              118  FOR_ITER            190  'to 190'
              120  STORE_FAST               'param'

 L. 854       122  SETUP_FINALLY       142  'to 142'

 L. 855       124  LOAD_FAST                'param'
              126  LOAD_METHOD              split
              128  LOAD_STR                 '='
              130  CALL_METHOD_1         1  ''
              132  UNPACK_SEQUENCE_2     2 
              134  STORE_FAST               'key'
              136  STORE_FAST               'value'
              138  POP_BLOCK        
              140  JUMP_FORWARD        168  'to 168'
            142_0  COME_FROM_FINALLY   122  '122'

 L. 856       142  DUP_TOP          
              144  LOAD_GLOBAL              ValueError
              146  COMPARE_OP               exception-match
              148  POP_JUMP_IF_FALSE   166  'to 166'
              150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L. 857       156  POP_EXCEPT       
              158  POP_TOP          
              160  JUMP_FORWARD        190  'to 190'
              162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
            166_0  COME_FROM           148  '148'
              166  END_FINALLY      
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           140  '140'

 L. 859       168  LOAD_FAST                'value'
              170  LOAD_METHOD              strip
              172  LOAD_FAST                'replace_chars'
              174  CALL_METHOD_1         1  ''
              176  LOAD_FAST                'link'
              178  LOAD_FAST                'key'
              180  LOAD_METHOD              strip
              182  LOAD_FAST                'replace_chars'
              184  CALL_METHOD_1         1  ''
              186  STORE_SUBSCR     
              188  JUMP_BACK           118  'to 118'
            190_0  COME_FROM           160  '160'
            190_1  COME_FROM           118  '118'

 L. 861       190  LOAD_FAST                'links'
              192  LOAD_METHOD              append
              194  LOAD_FAST                'link'
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
              200  JUMP_BACK            38  'to 38'
            202_0  COME_FROM            38  '38'

 L. 863       202  LOAD_FAST                'links'
              204  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 160


_null = '\x00'.encode('ascii')
_null2 = _null * 2
_null3 = _null * 3

def guess_json_utf(data):
    """
    :rtype: str
    """
    sample = data[:4]
    if sample in (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE):
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
    Does not replace a present scheme with the one provided as an argument.

    :rtype: str
    """
    scheme, netloc, path, params, query, fragment = urlparse(url, new_scheme)
    if not netloc:
        netloc, path = path, netloc
    return urlunparse((scheme, netloc, path, params, query, fragment))


def get_auth_from_url(url):
    """Given a url with authentication components, extract them into a tuple of
    username,password.

    :rtype: (str,str)
    """
    parsed = urlparse(url)
    try:
        auth = (unquote(parsed.username), unquote(parsed.password))
    except (AttributeError, TypeError):
        auth = ('', '')
    else:
        return auth


_CLEAN_HEADER_REGEX_BYTE = re.compile(b'^\\S[^\\r\\n]*$|^$')
_CLEAN_HEADER_REGEX_STR = re.compile('^\\S[^\\r\\n]*$|^$')

def check_header_validity(header):
    """Verifies that header value is a string which doesn't contain
    leading whitespace or return characters. This prevents unintended
    header injection.

    :param header: tuple, in the format (name, value).
    """
    name, value = header
    if isinstance(value, bytes):
        pat = _CLEAN_HEADER_REGEX_BYTE
    else:
        pat = _CLEAN_HEADER_REGEX_STR
    try:
        if not pat.match(value):
            raise InvalidHeader('Invalid return character or leading space in header: %s' % name)
    except TypeError:
        raise InvalidHeader('Value for header {%s: %s} must be of type str or bytes, not %s' % (
         name, value, type(value)))


def urldefragauth(url):
    """
    Given a url remove the fragment and the authentication part.

    :rtype: str
    """
    scheme, netloc, path, params, query, fragment = urlparse(url)
    if not netloc:
        netloc, path = path, netloc
    netloc = netloc.rsplit('@', 1)[(-1)]
    return urlunparse((scheme, netloc, path, params, query, ''))


def rewind_body(prepared_request):
    """Move file pointer back to its recorded starting position
    so it can be read again on redirect.
    """
    body_seek = getattr(prepared_request.body, 'seek', None)
    if body_seek is not None and isinstance(prepared_request._body_position, integer_types):
        try:
            body_seek(prepared_request._body_position)
        except (IOError, OSError):
            raise UnrewindableBodyError('An error occurred when rewinding request body for redirect.')

    else:
        raise UnrewindableBodyError('Unable to rewind request body for redirect.')