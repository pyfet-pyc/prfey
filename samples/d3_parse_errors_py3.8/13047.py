# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: urllib\parse.py
"""Parse (absolute and relative) URLs.

urlparse module is based upon the following RFC specifications.

RFC 3986 (STD66): "Uniform Resource Identifiers" by T. Berners-Lee, R. Fielding
and L.  Masinter, January 2005.

RFC 2732 : "Format for Literal IPv6 Addresses in URL's by R.Hinden, B.Carpenter
and L.Masinter, December 1999.

RFC 2396:  "Uniform Resource Identifiers (URI)": Generic Syntax by T.
Berners-Lee, R. Fielding, and L. Masinter, August 1998.

RFC 2368: "The mailto URL scheme", by P.Hoffman , L Masinter, J. Zawinski, July 1998.

RFC 1808: "Relative Uniform Resource Locators", by R. Fielding, UC Irvine, June
1995.

RFC 1738: "Uniform Resource Locators (URL)" by T. Berners-Lee, L. Masinter, M.
McCahill, December 1994

RFC 3986 is considered the current standard and any future changes to
urlparse module should conform with it.  The urlparse module is
currently not entirely compliant with this RFC due to defacto
scenarios for parsing, and for backward compatibility purposes, some
parsing quirks from older RFCs are retained. The testcases in
test_urlparse.py provides a good indicator of parsing behavior.
"""
import re, sys, collections, warnings
__all__ = [
 'urlparse', 'urlunparse', 'urljoin', 'urldefrag',
 'urlsplit', 'urlunsplit', 'urlencode', 'parse_qs',
 'parse_qsl', 'quote', 'quote_plus', 'quote_from_bytes',
 'unquote', 'unquote_plus', 'unquote_to_bytes',
 'DefragResult', 'ParseResult', 'SplitResult',
 'DefragResultBytes', 'ParseResultBytes', 'SplitResultBytes']
uses_relative = [
 '', 'ftp', 'http', 'gopher', 'nntp', 'imap',
 'wais', 'file', 'https', 'shttp', 'mms',
 'prospero', 'rtsp', 'rtspu', 'sftp',
 'svn', 'svn+ssh', 'ws', 'wss']
uses_netloc = [
 '', 'ftp', 'http', 'gopher', 'nntp', 'telnet',
 'imap', 'wais', 'file', 'mms', 'https', 'shttp',
 'snews', 'prospero', 'rtsp', 'rtspu', 'rsync',
 'svn', 'svn+ssh', 'sftp', 'nfs', 'git', 'git+ssh',
 'ws', 'wss']
uses_params = [
 '', 'ftp', 'hdl', 'prospero', 'http', 'imap',
 'https', 'shttp', 'rtsp', 'rtspu', 'sip', 'sips',
 'mms', 'sftp', 'tel']
non_hierarchical = [
 'gopher', 'hdl', 'mailto', 'news',
 'telnet', 'wais', 'imap', 'snews', 'sip', 'sips']
uses_query = [
 '', 'http', 'wais', 'imap', 'https', 'shttp', 'mms',
 'gopher', 'rtsp', 'rtspu', 'sip', 'sips']
uses_fragment = [
 '', 'ftp', 'hdl', 'http', 'gopher', 'news',
 'nntp', 'wais', 'https', 'shttp', 'snews',
 'file', 'prospero']
scheme_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.'
MAX_CACHE_SIZE = 20
_parse_cache = {}

def clear_cache():
    """Clear the parse cache and the quoters cache."""
    _parse_cache.clear()
    _safe_quoters.clear()


_implicit_encoding = 'ascii'
_implicit_errors = 'strict'

def _noop(obj):
    return obj


def _encode_result(obj, encoding=_implicit_encoding, errors=_implicit_errors):
    return obj.encode(encoding, errors)


def _decode_args(args, encoding=_implicit_encoding, errors=_implicit_errors):
    return tuple(((x.decode(encoding, errors) if x else '') for x in args))


def _coerce_args(*args):
    str_input = isinstance(args[0], str)
    for arg in args[1:]:
        if arg:
            if isinstance(arg, str) != str_input:
                raise TypeError('Cannot mix str and non-str arguments')
    else:
        if str_input:
            return args + (_noop,)
        return _decode_args(args) + (_encode_result,)


class _ResultMixinStr(object):
    __doc__ = 'Standard approach to encoding parsed results from str to bytes'
    __slots__ = ()

    def encode(self, encoding='ascii', errors='strict'):
        return (self._encoded_counterpart)(*(x.encode(encoding, errors) for x in self))


class _ResultMixinBytes(object):
    __doc__ = 'Standard approach to decoding parsed results from bytes to str'
    __slots__ = ()

    def decode(self, encoding='ascii', errors='strict'):
        return (self._decoded_counterpart)(*(x.decode(encoding, errors) for x in self))


class _NetlocResultMixinBase(object):
    __doc__ = 'Shared methods for the parsed result objects containing a netloc element'
    __slots__ = ()

    @property
    def username(self):
        return self._userinfo[0]

    @property
    def password(self):
        return self._userinfo[1]

    @property
    def hostname(self):
        hostname = self._hostinfo[0]
        if not hostname:
            return
        separator = '%' if isinstance(hostname, str) else b'%'
        hostname, percent, zone = hostname.partition(separator)
        return hostname.lower() + percent + zone

    @property
    def port(self):
        port = self._hostinfo[1]
        if port is not None:
            try:
                port = int(port, 10)
            except ValueError:
                message = f"Port could not be cast to integer value as {port!r}"
                raise ValueError(message) from None
            else:
                if not 0 <= port <= 65535:
                    raise ValueError('Port out of range 0-65535')
            return port


class _NetlocResultMixinStr(_NetlocResultMixinBase, _ResultMixinStr):
    __slots__ = ()

    @property
    def _userinfo(self):
        netloc = self.netloc
        userinfo, have_info, hostinfo = netloc.rpartition('@')
        if have_info:
            username, have_password, password = userinfo.partition(':')
            if not have_password:
                password = None
        else:
            username = password = None
        return (username, password)

    @property
    def _hostinfo(self):
        netloc = self.netloc
        _, _, hostinfo = netloc.rpartition('@')
        _, have_open_br, bracketed = hostinfo.partition('[')
        if have_open_br:
            hostname, _, port = bracketed.partition(']')
            _, _, port = port.partition(':')
        else:
            hostname, _, port = hostinfo.partition(':')
        if not port:
            port = None
        return (hostname, port)


class _NetlocResultMixinBytes(_NetlocResultMixinBase, _ResultMixinBytes):
    __slots__ = ()

    @property
    def _userinfo(self):
        netloc = self.netloc
        userinfo, have_info, hostinfo = netloc.rpartition(b'@')
        if have_info:
            username, have_password, password = userinfo.partition(b':')
            if not have_password:
                password = None
        else:
            username = password = None
        return (username, password)

    @property
    def _hostinfo(self):
        netloc = self.netloc
        _, _, hostinfo = netloc.rpartition(b'@')
        _, have_open_br, bracketed = hostinfo.partition(b'[')
        if have_open_br:
            hostname, _, port = bracketed.partition(b']')
            _, _, port = port.partition(b':')
        else:
            hostname, _, port = hostinfo.partition(b':')
        if not port:
            port = None
        return (hostname, port)


from collections import namedtuple
_DefragResultBase = namedtuple('DefragResult', 'url fragment')
_SplitResultBase = namedtuple('SplitResult', 'scheme netloc path query fragment')
_ParseResultBase = namedtuple('ParseResult', 'scheme netloc path params query fragment')
_DefragResultBase.__doc__ = '\nDefragResult(url, fragment)\n\nA 2-tuple that contains the url without fragment identifier and the fragment\nidentifier as a separate argument.\n'
_DefragResultBase.url.__doc__ = 'The URL with no fragment identifier.'
_DefragResultBase.fragment.__doc__ = '\nFragment identifier separated from URL, that allows indirect identification of a\nsecondary resource by reference to a primary resource and additional identifying\ninformation.\n'
_SplitResultBase.__doc__ = '\nSplitResult(scheme, netloc, path, query, fragment)\n\nA 5-tuple that contains the different components of a URL. Similar to\nParseResult, but does not split params.\n'
_SplitResultBase.scheme.__doc__ = 'Specifies URL scheme for the request.'
_SplitResultBase.netloc.__doc__ = '\nNetwork location where the request is made to.\n'
_SplitResultBase.path.__doc__ = '\nThe hierarchical path, such as the path to a file to download.\n'
_SplitResultBase.query.__doc__ = "\nThe query component, that contains non-hierarchical data, that along with data\nin path component, identifies a resource in the scope of URI's scheme and\nnetwork location.\n"
_SplitResultBase.fragment.__doc__ = '\nFragment identifier, that allows indirect identification of a secondary resource\nby reference to a primary resource and additional identifying information.\n'
_ParseResultBase.__doc__ = '\nParseResult(scheme, netloc, path, params, query, fragment)\n\nA 6-tuple that contains components of a parsed URL.\n'
_ParseResultBase.scheme.__doc__ = _SplitResultBase.scheme.__doc__
_ParseResultBase.netloc.__doc__ = _SplitResultBase.netloc.__doc__
_ParseResultBase.path.__doc__ = _SplitResultBase.path.__doc__
_ParseResultBase.params.__doc__ = '\nParameters for last path element used to dereference the URI in order to provide\naccess to perform some operation on the resource.\n'
_ParseResultBase.query.__doc__ = _SplitResultBase.query.__doc__
_ParseResultBase.fragment.__doc__ = _SplitResultBase.fragment.__doc__
ResultBase = _NetlocResultMixinStr

class DefragResult(_DefragResultBase, _ResultMixinStr):
    __slots__ = ()

    def geturl(self):
        if self.fragment:
            return self.url + '#' + self.fragment
        return self.url


class SplitResult(_SplitResultBase, _NetlocResultMixinStr):
    __slots__ = ()

    def geturl(self):
        return urlunsplit(self)


class ParseResult(_ParseResultBase, _NetlocResultMixinStr):
    __slots__ = ()

    def geturl(self):
        return urlunparse(self)


class DefragResultBytes(_DefragResultBase, _ResultMixinBytes):
    __slots__ = ()

    def geturl(self):
        if self.fragment:
            return self.url + b'#' + self.fragment
        return self.url


class SplitResultBytes(_SplitResultBase, _NetlocResultMixinBytes):
    __slots__ = ()

    def geturl(self):
        return urlunsplit(self)


class ParseResultBytes(_ParseResultBase, _NetlocResultMixinBytes):
    __slots__ = ()

    def geturl(self):
        return urlunparse(self)


def _fix_result_transcoding():
    _result_pairs = (
     (
      DefragResult, DefragResultBytes),
     (
      SplitResult, SplitResultBytes),
     (
      ParseResult, ParseResultBytes))
    for _decoded, _encoded in _result_pairs:
        _decoded._encoded_counterpart = _encoded
        _encoded._decoded_counterpart = _decoded


_fix_result_transcoding()
del _fix_result_transcoding

def urlparse(url, scheme='', allow_fragments=True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    splitresult = urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = splitresult
    if scheme in uses_params and ';' in url:
        url, params = _splitparams(url)
    else:
        params = ''
    result = ParseResult(scheme, netloc, url, params, query, fragment)
    return _coerce_result(result)


def _splitparams(url):
    if '/' in url:
        i = url.find(';', url.rfind('/'))
        if i < 0:
            return (url, '')
    else:
        i = url.find(';')
    return (url[:i], url[i + 1:])


def _splitnetloc(url, start=0):
    delim = len(url)
    for c in '/?#':
        wdelim = url.find(c, start)
        if wdelim >= 0:
            delim = min(delim, wdelim)
    else:
        return (
         url[start:delim], url[delim:])


def _checknetloc(netloc):
    if not netloc or netloc.isascii():
        return
    import unicodedata
    n = netloc.replace('@', '')
    n = n.replace(':', '')
    n = n.replace('#', '')
    n = n.replace('?', '')
    netloc2 = unicodedata.normalize('NFKC', n)
    if n == netloc2:
        return
    for c in '/?#@:':
        if c in netloc2:
            raise ValueError("netloc '" + netloc + "' contains invalid " + 'characters under NFKC normalization')


def urlsplit(url, scheme='', allow_fragments=True):
    """Parse a URL into 5 components:
    <scheme>://<netloc>/<path>?<query>#<fragment>
    Return a 5-tuple: (scheme, netloc, path, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    allow_fragments = bool(allow_fragments)
    key = (url, scheme, allow_fragments, type(url), type(scheme))
    cached = _parse_cache.get(key, None)
    if cached:
        return _coerce_result(cached)
    if len(_parse_cache) >= MAX_CACHE_SIZE:
        clear_cache()
    netloc = query = fragment = ''
    i = url.find(':')
    if i > 0:
        if url[:i] == 'http':
            url = url[i + 1:]
            if url[:2] == '//':
                netloc, url = _splitnetloc(url, 2)
                if '[' in netloc and not ']' not in netloc:
                    if not ']' in netloc or '[' not in netloc:
                        raise ValueError('Invalid IPv6 URL')
                if allow_fragments:
                    if '#' in url:
                        url, fragment = url.split('#', 1)
                if '?' in url:
                    url, query = url.split('?', 1)
                _checknetloc(netloc)
                v = SplitResult('http', netloc, url, query, fragment)
                _parse_cache[key] = v
                return _coerce_result(v)
        for c in url[:i]:
            if c not in scheme_chars:
                break
        else:
            rest = url[i + 1:]
            if not rest or any((c not in '0123456789' for c in rest)):
                scheme, url = url[:i].lower(), rest

    if url[:2] == '//':
        netloc, url = _splitnetloc(url, 2)
        if '[' in netloc and not ']' not in netloc:
            if not ']' in netloc or '[' not in netloc:
                raise ValueError('Invalid IPv6 URL')
        if allow_fragments:
            if '#' in url:
                url, fragment = url.split('#', 1)
        if '?' in url:
            url, query = url.split('?', 1)
        _checknetloc(netloc)
        v = SplitResult(scheme, netloc, url, query, fragment)
        _parse_cache[key] = v
        return _coerce_result(v)


def urlunparse(components):
    """Put a parsed URL back together again.  This may result in a
    slightly different, but equivalent URL, if the URL that was parsed
    originally had redundant delimiters, e.g. a ? with an empty query
    (the draft states that these are equivalent)."""
    scheme, netloc, url, params, query, fragment, _coerce_result = _coerce_args(*components)
    if params:
        url = '%s;%s' % (url, params)
    return _coerce_result(urlunsplit((scheme, netloc, url, query, fragment)))


def urlunsplit(components):
    """Combine the elements of a tuple as returned by urlsplit() into a
    complete URL as a string. The data argument can be any five-item iterable.
    This may result in a slightly different, but equivalent URL, if the URL that
    was parsed originally had unnecessary delimiters (for example, a ? with an
    empty query; the RFC states that these are equivalent)."""
    scheme, netloc, url, query, fragment, _coerce_result = _coerce_args(*components)
    if not netloc:
        if scheme:
            if not scheme in uses_netloc or url[:2] != '//':
                if url:
                    if url[:1] != '/':
                        url = '/' + url
                url = '//' + (netloc or '') + url
        if scheme:
            url = scheme + ':' + url
        if query:
            url = url + '?' + query
        if fragment:
            url = url + '#' + fragment
        return _coerce_result(url)


def urljoin--- This code section failed: ---

 L. 507         0  LOAD_FAST                'base'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 508         4  LOAD_FAST                'url'
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 509         8  LOAD_FAST                'url'
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L. 510        12  LOAD_FAST                'base'
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 512        16  LOAD_GLOBAL              _coerce_args
               18  LOAD_FAST                'base'
               20  LOAD_FAST                'url'
               22  CALL_FUNCTION_2       2  ''
               24  UNPACK_SEQUENCE_3     3 
               26  STORE_FAST               'base'
               28  STORE_FAST               'url'
               30  STORE_FAST               '_coerce_result'

 L. 514        32  LOAD_GLOBAL              urlparse
               34  LOAD_FAST                'base'
               36  LOAD_STR                 ''
               38  LOAD_FAST                'allow_fragments'
               40  CALL_FUNCTION_3       3  ''

 L. 513        42  UNPACK_SEQUENCE_6     6 
               44  STORE_FAST               'bscheme'
               46  STORE_FAST               'bnetloc'
               48  STORE_FAST               'bpath'
               50  STORE_FAST               'bparams'
               52  STORE_FAST               'bquery'
               54  STORE_FAST               'bfragment'

 L. 516        56  LOAD_GLOBAL              urlparse
               58  LOAD_FAST                'url'
               60  LOAD_FAST                'bscheme'
               62  LOAD_FAST                'allow_fragments'
               64  CALL_FUNCTION_3       3  ''

 L. 515        66  UNPACK_SEQUENCE_6     6 
               68  STORE_FAST               'scheme'
               70  STORE_FAST               'netloc'
               72  STORE_FAST               'path'
               74  STORE_FAST               'params'
               76  STORE_FAST               'query'
               78  STORE_FAST               'fragment'

 L. 518        80  LOAD_FAST                'scheme'
               82  LOAD_FAST                'bscheme'
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_TRUE     96  'to 96'
               88  LOAD_FAST                'scheme'
               90  LOAD_GLOBAL              uses_relative
               92  COMPARE_OP               not-in
               94  POP_JUMP_IF_FALSE   104  'to 104'
             96_0  COME_FROM            86  '86'

 L. 519        96  LOAD_FAST                '_coerce_result'
               98  LOAD_FAST                'url'
              100  CALL_FUNCTION_1       1  ''
              102  RETURN_VALUE     
            104_0  COME_FROM            94  '94'

 L. 520       104  LOAD_FAST                'scheme'
              106  LOAD_GLOBAL              uses_netloc
              108  COMPARE_OP               in
              110  POP_JUMP_IF_FALSE   144  'to 144'

 L. 521       112  LOAD_FAST                'netloc'
              114  POP_JUMP_IF_FALSE   140  'to 140'

 L. 522       116  LOAD_FAST                '_coerce_result'
              118  LOAD_GLOBAL              urlunparse
              120  LOAD_FAST                'scheme'
              122  LOAD_FAST                'netloc'
              124  LOAD_FAST                'path'

 L. 523       126  LOAD_FAST                'params'

 L. 523       128  LOAD_FAST                'query'

 L. 523       130  LOAD_FAST                'fragment'

 L. 522       132  BUILD_TUPLE_6         6 
              134  CALL_FUNCTION_1       1  ''
              136  CALL_FUNCTION_1       1  ''
              138  RETURN_VALUE     
            140_0  COME_FROM           114  '114'

 L. 524       140  LOAD_FAST                'bnetloc'
              142  STORE_FAST               'netloc'
            144_0  COME_FROM           110  '110'

 L. 526       144  LOAD_FAST                'path'
              146  POP_JUMP_IF_TRUE    192  'to 192'
              148  LOAD_FAST                'params'
              150  POP_JUMP_IF_TRUE    192  'to 192'

 L. 527       152  LOAD_FAST                'bpath'
              154  STORE_FAST               'path'

 L. 528       156  LOAD_FAST                'bparams'
              158  STORE_FAST               'params'

 L. 529       160  LOAD_FAST                'query'
              162  POP_JUMP_IF_TRUE    168  'to 168'

 L. 530       164  LOAD_FAST                'bquery'
              166  STORE_FAST               'query'
            168_0  COME_FROM           162  '162'

 L. 531       168  LOAD_FAST                '_coerce_result'
              170  LOAD_GLOBAL              urlunparse
              172  LOAD_FAST                'scheme'
              174  LOAD_FAST                'netloc'
              176  LOAD_FAST                'path'

 L. 532       178  LOAD_FAST                'params'

 L. 532       180  LOAD_FAST                'query'

 L. 532       182  LOAD_FAST                'fragment'

 L. 531       184  BUILD_TUPLE_6         6 
              186  CALL_FUNCTION_1       1  ''
              188  CALL_FUNCTION_1       1  ''
              190  RETURN_VALUE     
            192_0  COME_FROM           150  '150'
            192_1  COME_FROM           146  '146'

 L. 534       192  LOAD_FAST                'bpath'
              194  LOAD_METHOD              split
              196  LOAD_STR                 '/'
              198  CALL_METHOD_1         1  ''
              200  STORE_FAST               'base_parts'

 L. 535       202  LOAD_FAST                'base_parts'
              204  LOAD_CONST               -1
              206  BINARY_SUBSCR    
              208  LOAD_STR                 ''
              210  COMPARE_OP               !=
              212  POP_JUMP_IF_FALSE   220  'to 220'

 L. 538       214  LOAD_FAST                'base_parts'
              216  LOAD_CONST               -1
              218  DELETE_SUBSCR    
            220_0  COME_FROM           212  '212'

 L. 541       220  LOAD_FAST                'path'
              222  LOAD_CONST               None
              224  LOAD_CONST               1
              226  BUILD_SLICE_2         2 
              228  BINARY_SUBSCR    
              230  LOAD_STR                 '/'
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_FALSE   248  'to 248'

 L. 542       236  LOAD_FAST                'path'
              238  LOAD_METHOD              split
              240  LOAD_STR                 '/'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'segments'
              246  JUMP_FORWARD        288  'to 288'
            248_0  COME_FROM           234  '234'

 L. 544       248  LOAD_FAST                'base_parts'
              250  LOAD_FAST                'path'
              252  LOAD_METHOD              split
              254  LOAD_STR                 '/'
              256  CALL_METHOD_1         1  ''
              258  BINARY_ADD       
              260  STORE_FAST               'segments'

 L. 547       262  LOAD_GLOBAL              filter
              264  LOAD_CONST               None
              266  LOAD_FAST                'segments'
              268  LOAD_CONST               1
              270  LOAD_CONST               -1
              272  BUILD_SLICE_2         2 
              274  BINARY_SUBSCR    
              276  CALL_FUNCTION_2       2  ''
              278  LOAD_FAST                'segments'
              280  LOAD_CONST               1
              282  LOAD_CONST               -1
              284  BUILD_SLICE_2         2 
              286  STORE_SUBSCR     
            288_0  COME_FROM           246  '246'

 L. 549       288  BUILD_LIST_0          0 
              290  STORE_FAST               'resolved_path'

 L. 551       292  LOAD_FAST                'segments'
              294  GET_ITER         
            296_0  COME_FROM           374  '374'
            296_1  COME_FROM           362  '362'
            296_2  COME_FROM           358  '358'
            296_3  COME_FROM           346  '346'
              296  FOR_ITER            378  'to 378'
              298  STORE_FAST               'seg'

 L. 552       300  LOAD_FAST                'seg'
              302  LOAD_STR                 '..'
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   348  'to 348'

 L. 553       310  SETUP_FINALLY       324  'to 324'

 L. 554       312  LOAD_FAST                'resolved_path'
              314  LOAD_METHOD              pop
              316  CALL_METHOD_0         0  ''
              318  POP_TOP          
              320  POP_BLOCK        
              322  JUMP_FORWARD        346  'to 346'
            324_0  COME_FROM_FINALLY   310  '310'

 L. 555       324  DUP_TOP          
              326  LOAD_GLOBAL              IndexError
              328  COMPARE_OP               exception-match
          330_332  POP_JUMP_IF_FALSE   344  'to 344'
              334  POP_TOP          
              336  POP_TOP          
              338  POP_TOP          

 L. 558       340  POP_EXCEPT       
              342  BREAK_LOOP          346  'to 346'
            344_0  COME_FROM           330  '330'
              344  END_FINALLY      
            346_0  COME_FROM           342  '342'
            346_1  COME_FROM           322  '322'
              346  JUMP_BACK           296  'to 296'
            348_0  COME_FROM           306  '306'

 L. 559       348  LOAD_FAST                'seg'
              350  LOAD_STR                 '.'
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_FALSE   364  'to 364'

 L. 560   358_360  CONTINUE            296  'to 296'
              362  JUMP_BACK           296  'to 296'
            364_0  COME_FROM           354  '354'

 L. 562       364  LOAD_FAST                'resolved_path'
              366  LOAD_METHOD              append
              368  LOAD_FAST                'seg'
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          
          374_376  JUMP_BACK           296  'to 296'
            378_0  COME_FROM           296  '296'

 L. 564       378  LOAD_FAST                'segments'
              380  LOAD_CONST               -1
              382  BINARY_SUBSCR    
              384  LOAD_CONST               ('.', '..')
              386  COMPARE_OP               in
          388_390  POP_JUMP_IF_FALSE   402  'to 402'

 L. 567       392  LOAD_FAST                'resolved_path'
              394  LOAD_METHOD              append
              396  LOAD_STR                 ''
              398  CALL_METHOD_1         1  ''
              400  POP_TOP          
            402_0  COME_FROM           388  '388'

 L. 569       402  LOAD_FAST                '_coerce_result'
              404  LOAD_GLOBAL              urlunparse
              406  LOAD_FAST                'scheme'
              408  LOAD_FAST                'netloc'
              410  LOAD_STR                 '/'
              412  LOAD_METHOD              join

 L. 570       414  LOAD_FAST                'resolved_path'

 L. 569       416  CALL_METHOD_1         1  ''
          418_420  JUMP_IF_TRUE_OR_POP   424  'to 424'

 L. 570       422  LOAD_STR                 '/'
            424_0  COME_FROM           418  '418'

 L. 570       424  LOAD_FAST                'params'

 L. 570       426  LOAD_FAST                'query'

 L. 570       428  LOAD_FAST                'fragment'

 L. 569       430  BUILD_TUPLE_6         6 
              432  CALL_FUNCTION_1       1  ''
              434  CALL_FUNCTION_1       1  ''
              436  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 344


def urldefrag(url):
    """Removes any existing fragment from URL.

    Returns a tuple of the defragmented URL and the fragment.  If
    the URL contained no fragments, the second element is the
    empty string.
    """
    url, _coerce_result = _coerce_args(url)
    if '#' in url:
        s, n, p, a, q, frag = urlparse(url)
        defrag = urlunparse((s, n, p, a, q, ''))
    else:
        frag = ''
        defrag = url
    return _coerce_result(DefragResult(defrag, frag))


_hexdig = '0123456789ABCDEFabcdef'
_hextobyte = None

def unquote_to_bytes(string):
    """unquote_to_bytes('abc%20def') -> b'abc def'."""
    global _hextobyte
    if not string:
        string.split
        return b''
    if isinstance(string, str):
        string = string.encode('utf-8')
    bits = string.split(b'%')
    if len(bits) == 1:
        return string
    res = [
     bits[0]]
    append = res.append
    if _hextobyte is None:
        _hextobyte = {bytes.fromhex(a + b):(a + b).encode() for a in _hexdig for b in _hexdig}
    for item in bits[1:]:
        try:
            append(_hextobyte[item[:2]])
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    else:
        return (b'').join(res)


_asciire = re.compile('([\x00-\x7f]+)')

def unquote(string, encoding='utf-8', errors='replace'):
    """Replace %xx escapes by their single-character equivalent. The optional
    encoding and errors parameters specify how to decode percent-encoded
    sequences into Unicode characters, as accepted by the bytes.decode()
    method.
    By default, percent-encoded sequences are decoded with UTF-8, and invalid
    sequences are replaced by a placeholder character.

    unquote('abc%20def') -> 'abc def'.
    """
    if isinstance(string, bytes):
        raise TypeError('Expected str, got bytes')
    if '%' not in string:
        string.split
        return string
    if encoding is None:
        encoding = 'utf-8'
    if errors is None:
        errors = 'replace'
    bits = _asciire.split(string)
    res = [bits[0]]
    append = res.append
    for i in range(1, len(bits), 2):
        append(unquote_to_bytes(bits[i]).decode(encoding, errors))
        append(bits[(i + 1)])
    else:
        return ''.join(res)


def parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None, separator='&'):
    """Parse a query given as a string argument.

        Arguments:

        qs: percent-encoded query string to be parsed

        keep_blank_values: flag indicating whether blank values in
            percent-encoded queries should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.

        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.

        encoding and errors: specify how to decode percent-encoded sequences
            into Unicode characters, as accepted by the bytes.decode() method.

        max_num_fields: int. If set, then throws a ValueError if there
            are more than n fields read by parse_qsl().

        separator: str. The symbol to use for separating the query arguments.
            Defaults to &.

        Returns a dictionary.
    """
    parsed_result = {}
    pairs = parse_qsl(qs, keep_blank_values, strict_parsing, encoding=encoding,
      errors=errors,
      max_num_fields=max_num_fields,
      separator=separator)
    for name, value in pairs:
        if name in parsed_result:
            parsed_result[name].append(value)
        else:
            parsed_result[name] = [
             value]
    else:
        return parsed_result


def parse_qsl--- This code section failed: ---

 L. 723         0  LOAD_GLOBAL              _coerce_args
                2  LOAD_FAST                'qs'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'qs'
               10  STORE_FAST               '_coerce_result'

 L. 725        12  LOAD_FAST                'separator'
               14  POP_JUMP_IF_FALSE    30  'to 30'
               16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'separator'
               20  LOAD_GLOBAL              str
               22  LOAD_GLOBAL              bytes
               24  BUILD_TUPLE_2         2 
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     38  'to 38'
             30_0  COME_FROM            14  '14'

 L. 726        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'Separator must be of type string or bytes.'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 731        38  LOAD_FAST                'max_num_fields'
               40  LOAD_CONST               None
               42  COMPARE_OP               is-not
               44  POP_JUMP_IF_FALSE    76  'to 76'

 L. 732        46  LOAD_CONST               1
               48  LOAD_FAST                'qs'
               50  LOAD_METHOD              count
               52  LOAD_FAST                'separator'
               54  CALL_METHOD_1         1  ''
               56  BINARY_ADD       
               58  STORE_FAST               'num_fields'

 L. 733        60  LOAD_FAST                'max_num_fields'
               62  LOAD_FAST                'num_fields'
               64  COMPARE_OP               <
               66  POP_JUMP_IF_FALSE    76  'to 76'

 L. 734        68  LOAD_GLOBAL              ValueError
               70  LOAD_STR                 'Max number of fields exceeded'
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'
             76_1  COME_FROM            44  '44'

 L. 736        76  LOAD_LISTCOMP            '<code_object <listcomp>>'
               78  LOAD_STR                 'parse_qsl.<locals>.<listcomp>'
               80  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               82  LOAD_FAST                'qs'
               84  LOAD_METHOD              split
               86  LOAD_FAST                'separator'
               88  CALL_METHOD_1         1  ''
               90  GET_ITER         
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'pairs'

 L. 737        96  BUILD_LIST_0          0 
               98  STORE_FAST               'r'

 L. 738       100  LOAD_FAST                'pairs'
              102  GET_ITER         
            104_0  COME_FROM           284  '284'
            104_1  COME_FROM           192  '192'
            104_2  COME_FROM           176  '176'
            104_3  COME_FROM           162  '162'
            104_4  COME_FROM           116  '116'
              104  FOR_ITER            286  'to 286'
              106  STORE_FAST               'name_value'

 L. 739       108  LOAD_FAST                'name_value'
              110  POP_JUMP_IF_TRUE    118  'to 118'
              112  LOAD_FAST                'strict_parsing'
              114  POP_JUMP_IF_TRUE    118  'to 118'

 L. 740       116  JUMP_BACK           104  'to 104'
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM           110  '110'

 L. 741       118  LOAD_FAST                'name_value'
              120  LOAD_METHOD              split
              122  LOAD_STR                 '='
              124  LOAD_CONST               1
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'nv'

 L. 742       130  LOAD_GLOBAL              len
              132  LOAD_FAST                'nv'
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_CONST               2
              138  COMPARE_OP               !=
              140  POP_JUMP_IF_FALSE   178  'to 178'

 L. 743       142  LOAD_FAST                'strict_parsing'
              144  POP_JUMP_IF_FALSE   160  'to 160'

 L. 744       146  LOAD_GLOBAL              ValueError
              148  LOAD_STR                 'bad query field: %r'
              150  LOAD_FAST                'name_value'
              152  BUILD_TUPLE_1         1 
              154  BINARY_MODULO    
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
            160_0  COME_FROM           144  '144'

 L. 746       160  LOAD_FAST                'keep_blank_values'
              162  POP_JUMP_IF_FALSE_BACK   104  'to 104'

 L. 747       164  LOAD_FAST                'nv'
              166  LOAD_METHOD              append
              168  LOAD_STR                 ''
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          
              174  JUMP_FORWARD        178  'to 178'

 L. 749       176  JUMP_BACK           104  'to 104'
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           140  '140'

 L. 750       178  LOAD_GLOBAL              len
              180  LOAD_FAST                'nv'
              182  LOAD_CONST               1
              184  BINARY_SUBSCR    
              186  CALL_FUNCTION_1       1  ''
              188  POP_JUMP_IF_TRUE    194  'to 194'
              190  LOAD_FAST                'keep_blank_values'
              192  POP_JUMP_IF_FALSE_BACK   104  'to 104'
            194_0  COME_FROM           188  '188'

 L. 751       194  LOAD_FAST                'nv'
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  LOAD_METHOD              replace
              202  LOAD_STR                 '+'
              204  LOAD_STR                 ' '
              206  CALL_METHOD_2         2  ''
              208  STORE_FAST               'name'

 L. 752       210  LOAD_GLOBAL              unquote
              212  LOAD_FAST                'name'
              214  LOAD_FAST                'encoding'
              216  LOAD_FAST                'errors'
              218  LOAD_CONST               ('encoding', 'errors')
              220  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              222  STORE_FAST               'name'

 L. 753       224  LOAD_FAST                '_coerce_result'
              226  LOAD_FAST                'name'
              228  CALL_FUNCTION_1       1  ''
              230  STORE_FAST               'name'

 L. 754       232  LOAD_FAST                'nv'
              234  LOAD_CONST               1
              236  BINARY_SUBSCR    
              238  LOAD_METHOD              replace
              240  LOAD_STR                 '+'
              242  LOAD_STR                 ' '
              244  CALL_METHOD_2         2  ''
              246  STORE_FAST               'value'

 L. 755       248  LOAD_GLOBAL              unquote
              250  LOAD_FAST                'value'
              252  LOAD_FAST                'encoding'
              254  LOAD_FAST                'errors'
              256  LOAD_CONST               ('encoding', 'errors')
              258  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              260  STORE_FAST               'value'

 L. 756       262  LOAD_FAST                '_coerce_result'
              264  LOAD_FAST                'value'
              266  CALL_FUNCTION_1       1  ''
              268  STORE_FAST               'value'

 L. 757       270  LOAD_FAST                'r'
              272  LOAD_METHOD              append
              274  LOAD_FAST                'name'
              276  LOAD_FAST                'value'
              278  BUILD_TUPLE_2         2 
              280  CALL_METHOD_1         1  ''
              282  POP_TOP          
              284  JUMP_BACK           104  'to 104'
            286_0  COME_FROM           104  '104'

 L. 758       286  LOAD_FAST                'r'
              288  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 176


def unquote_plus(string, encoding='utf-8', errors='replace'):
    """Like unquote(), but also replace plus signs by spaces, as required for
    unquoting HTML form values.

    unquote_plus('%7e/abc+def') -> '~/abc def'
    """
    string = string.replace('+', ' ')
    return unquote(string, encoding, errors)


_ALWAYS_SAFE = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-~')
_ALWAYS_SAFE_BYTES = bytes(_ALWAYS_SAFE)
_safe_quoters = {}

class Quoter(collections.defaultdict):
    __doc__ = 'A mapping from bytes (in range(0,256)) to strings.\n\n    String values are percent-encoded byte values, unless the key < 128, and\n    in the "safe" set (either the specified safe set, or default set).\n    '

    def __init__(self, safe):
        """safe: bytes object."""
        self.safe = _ALWAYS_SAFE.union(safe)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, dict(self))

    def __missing__(self, b):
        res = chr(b) if b in self.safe else '%{:02X}'.format(b)
        self[b] = res
        return res


def quote(string, safe='/', encoding=None, errors=None):
    """quote('abc def') -> 'abc%20def'

    Each part of a URL, e.g. the path info, the query, etc., has a
    different set of reserved characters that must be quoted. The
    quote function offers a cautious (not minimal) way to quote a
    string for most of these parts.

    RFC 3986 Uniform Resource Identifier (URI): Generic Syntax lists
    the following (un)reserved characters.

    unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
    reserved      = gen-delims / sub-delims
    gen-delims    = ":" / "/" / "?" / "#" / "[" / "]" / "@"
    sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
                  / "*" / "+" / "," / ";" / "="

    Each of the reserved characters is reserved in some component of a URL,
    but not necessarily in all of them.

    The quote function %-escapes all characters that are neither in the
    unreserved chars ("always safe") nor the additional chars set via the
    safe arg.

    The default for the safe arg is '/'. The character is reserved, but in
    typical usage the quote function is being called on a path where the
    existing slash characters are to be preserved.

    Python 3.7 updates from using RFC 2396 to RFC 3986 to quote URL strings.
    Now, "~" is included in the set of unreserved characters.

    string and safe may be either str or bytes objects. encoding and errors
    must not be specified if string is a bytes object.

    The optional encoding and errors parameters specify how to deal with
    non-ASCII characters, as accepted by the str.encode method.
    By default, encoding='utf-8' (characters are encoded with UTF-8), and
    errors='strict' (unsupported characters raise a UnicodeEncodeError).
    """
    if isinstance(string, str):
        if not string:
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'strict'
        string = string.encode(encoding, errors)
    else:
        if encoding is not None:
            raise TypeError("quote() doesn't support 'encoding' for bytes")
        if errors is not None:
            raise TypeError("quote() doesn't support 'errors' for bytes")
    return quote_from_bytes(string, safe)


def quote_plus(string, safe='', encoding=None, errors=None):
    """Like quote(), but also replace ' ' with '+', as required for quoting
    HTML form values. Plus signs in the original string are escaped unless
    they are included in safe. It also does not have safe default to '/'.
    """
    if not (isinstance(string, str) and ' ' not in string):
        if not isinstance(string, bytes) or b' ' not in string:
            return quote(string, safe, encoding, errors)
        if isinstance(safe, str):
            space = ' '
        else:
            space = b' '
        string = quote(string, safe + space, encoding, errors)
        return string.replace(' ', '+')


def quote_from_bytes(bs, safe='/'):
    """Like quote(), but accepts a bytes object rather than a str, and does
    not perform string-to-bytes encoding.  It always returns an ASCII string.
    quote_from_bytes(b'abc def?') -> 'abc%20def%3f'
    """
    if not isinstance(bs, (bytes, bytearray)):
        raise TypeError('quote_from_bytes() expected bytes')
    if not bs:
        return ''
    if isinstance(safe, str):
        safe = safe.encode('ascii', 'ignore')
    else:
        safe = bytes([c for c in safe if c < 128])
    if not bs.rstrip(_ALWAYS_SAFE_BYTES + safe):
        return bs.decode()
    try:
        quoter = _safe_quoters[safe]
    except KeyError:
        _safe_quoters[safe] = quoter = Quoter(safe).__getitem__
    else:
        return ''.join([quoter(char) for char in bs])


def urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus):
    """Encode a dict or sequence of two-element tuples into a URL query string.

    If any values in the query arg are sequences and doseq is true, each
    sequence element is converted to a separate parameter.

    If the query arg is a sequence of two-element tuples, the order of the
    parameters in the output will match the order of parameters in the
    input.

    The components of a query arg may each be either a string or a bytes type.

    The safe, encoding, and errors parameters are passed down to the function
    specified by quote_via (encoding and errors only if a component is a str).
    """
    if hasattr(query, 'items'):
        query = query.items()
    else:
        pass
    try:
        if len(query):
            if not isinstance(query[0], tuple):
                raise TypeError
    except TypeError:
        ty, va, tb = sys.exc_info()
        raise TypeError('not a valid non-string sequence or mapping object').with_traceback(tb)
    else:
        l = []
        if not doseq:
            for k, v in query:
                if isinstance(k, bytes):
                    k = quote_via(k, safe)
                else:
                    k = quote_via(str(k), safe, encoding, errors)
                if isinstance(v, bytes):
                    v = quote_via(v, safe)
                else:
                    v = quote_via(str(v), safe, encoding, errors)
                l.append(k + '=' + v)

        else:
            pass
        for k, v in query:
            if isinstance(k, bytes):
                k = quote_via(k, safe)
            else:
                k = quote_via(str(k), safe, encoding, errors)
            if isinstance(v, bytes):
                v = quote_via(v, safe)
                l.append(k + '=' + v)
            else:
                if isinstance(v, str):
                    v = quote_via(v, safe, encoding, errors)
                    l.append(k + '=' + v)
                try:
                    x = len(v)
                except TypeError:
                    v = quote_via(str(v), safe, encoding, errors)
                    l.append(k + '=' + v)
                else:
                    for elt in v:
                        if isinstance(elt, bytes):
                            elt = quote_via(elt, safe)
                        else:
                            elt = quote_via(str(elt), safe, encoding, errors)
                        l.append(k + '=' + elt)

        else:
            return '&'.join(l)


def to_bytes(url):
    warnings.warn('urllib.parse.to_bytes() is deprecated as of 3.8', DeprecationWarning,
      stacklevel=2)
    return _to_bytes(url)


def _to_bytes(url):
    """to_bytes(u"URL") --> 'URL'."""
    if isinstance(url, str):
        try:
            url = url.encode('ASCII').decode()
        except UnicodeError:
            raise UnicodeError('URL ' + repr(url) + ' contains non-ASCII characters')

        return url


def unwrap(url):
    """Transform a string like '<URL:scheme://host/path>' into 'scheme://host/path'.

    The string is returned unchanged if it's not a wrapped URL.
    """
    url = str(url).strip()
    if url[:1] == '<':
        if url[-1:] == '>':
            url = url[1:-1].strip()
    if url[:4] == 'URL:':
        url = url[4:].strip()
    return url


def splittype(url):
    warnings.warn('urllib.parse.splittype() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning,
      stacklevel=2)
    return _splittype(url)


_typeprog = None

def _splittype(url):
    """splittype('type:opaquestring') --> 'type', 'opaquestring'."""
    global _typeprog
    if _typeprog is None:
        _typeprog = re.compile('([^/:]+):(.*)', re.DOTALL)
    match = _typeprog.match(url)
    if match:
        scheme, data = match.groups()
        return (
         scheme.lower(), data)
    return (None, url)


def splithost(url):
    warnings.warn('urllib.parse.splithost() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning,
      stacklevel=2)
    return _splithost(url)


_hostprog = None

def _splithost(url):
    """splithost('//host[:port]/path') --> 'host[:port]', '/path'."""
    global _hostprog
    if _hostprog is None:
        _hostprog = re.compile('//([^/#?]*)(.*)', re.DOTALL)
    match = _hostprog.match(url)
    if match:
        host_port, path = match.groups()
        if path:
            if path[0] != '/':
                path = '/' + path
        return (
         host_port, path)
    return (None, url)


def splituser(host):
    warnings.warn('urllib.parse.splituser() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning,
      stacklevel=2)
    return _splituser(host)


def _splituser(host):
    """splituser('user[:passwd]@host[:port]') --> 'user[:passwd]', 'host[:port]'."""
    user, delim, host = host.rpartition('@')
    return (
     user if delim else None, host)


def splitpasswd(user):
    warnings.warn('urllib.parse.splitpasswd() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning,
      stacklevel=2)
    return _splitpasswd(user)


def _splitpasswd(user):
    """splitpasswd('user:passwd') -> 'user', 'passwd'."""
    user, delim, passwd = user.partition(':')
    return (
     user, passwd if delim else None)


def splitport(host):
    warnings.warn('urllib.parse.splitport() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning,
      stacklevel=2)
    return _splitport(host)


_portprog = None

def _splitport(host):
    """splitport('host:port') --> 'host', 'port'."""
    global _portprog
    if _portprog is None:
        _portprog = re.compile('(.*):([0-9]*)', re.DOTALL)
    match = _portprog.fullmatch(host)
    if match:
        host, port = match.groups()
        if port:
            return (host, port)
    return (
     host, None)


def splitnport(host, defport=-1):
    warnings.warn('urllib.parse.splitnport() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning,
      stacklevel=2)
    return _splitnport(host, defport)


def _splitnport(host, defport=-1):
    """Split host and port, returning numeric port.
    Return given default port if no ':' found; defaults to -1.
    Return numerical port if a valid number are found after ':'.
    Return None if ':' but not a valid number."""
    host, delim, port = host.rpartition(':')
    if not delim:
        host = port
    else:
        pass
    if port:
        try:
            nport = int(port)
        except ValueError:
            nport = None
        else:
            return (
             host, nport)
        return (host, defport)


def splitquery(url):
    warnings.warn('urllib.parse.splitquery() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning,
      stacklevel=2)
    return _splitquery(url)


def _splitquery(url):
    """splitquery('/path?query') --> '/path', 'query'."""
    path, delim, query = url.rpartition('?')
    if delim:
        return (path, query)
    return (url, None)


def splittag(url):
    warnings.warn('urllib.parse.splittag() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning,
      stacklevel=2)
    return _splittag(url)


def _splittag(url):
    """splittag('/path#tag') --> '/path', 'tag'."""
    path, delim, tag = url.rpartition('#')
    if delim:
        return (path, tag)
    return (url, None)


def splitattr(url):
    warnings.warn('urllib.parse.splitattr() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning,
      stacklevel=2)
    return _splitattr(url)


def _splitattr(url):
    """splitattr('/path;attr1=value1;attr2=value2;...') ->
        '/path', ['attr1=value1', 'attr2=value2', ...]."""
    words = url.split(';')
    return (
     words[0], words[1:])


def splitvalue(attr):
    warnings.warn('urllib.parse.splitvalue() is deprecated as of 3.8, use urllib.parse.parse_qsl() instead', DeprecationWarning,
      stacklevel=2)
    return _splitvalue(attr)


def _splitvalue(attr):
    """splitvalue('attr=value') --> 'attr', 'value'."""
    attr, delim, value = attr.partition('=')
    return (
     attr, value if delim else None)