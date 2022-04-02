# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\future\backports\urllib\request.py
"""
Ported using Python-Future from the Python 3.3 standard library.

An extensible library for opening URLs using a variety of protocols

The simplest way to use this module is to call the urlopen function,
which accepts a string containing a URL or a Request object (described
below).  It opens the URL and returns the results as file-like
object; the returned object has some extra methods described below.

The OpenerDirector manages a collection of Handler objects that do
all the actual work.  Each Handler implements a particular protocol or
option.  The OpenerDirector is a composite object that invokes the
Handlers needed to open the requested URL.  For example, the
HTTPHandler performs HTTP GET and POST requests and deals with
non-error returns.  The HTTPRedirectHandler automatically deals with
HTTP 301, 302, 303 and 307 redirect errors, and the HTTPDigestAuthHandler
deals with digest authentication.

urlopen(url, data=None) -- Basic usage is the same as original
urllib.  pass the url and optionally data to post to an HTTP URL, and
get a file-like object back.  One difference is that you can also pass
a Request instance instead of URL.  Raises a URLError (subclass of
IOError); for HTTP errors, raises an HTTPError, which can also be
treated as a valid response.

build_opener -- Function that creates a new OpenerDirector instance.
Will install the default handlers.  Accepts one or more Handlers as
arguments, either instances or Handler classes that it will
instantiate.  If one of the argument is a subclass of the default
handler, the argument will be installed instead of the default.

install_opener -- Installs a new opener as the default opener.

objects of interest:

OpenerDirector -- Sets up the User Agent as the Python-urllib client and manages
the Handler classes, while dealing with requests and responses.

Request -- An object that encapsulates the state of a request.  The
state can be as simple as the URL.  It can also include extra HTTP
headers, e.g. a User-Agent.

BaseHandler --

internals:
BaseHandler and parent
_call_chain conventions

Example usage:

import urllib.request

# set up authentication info
authinfo = urllib.request.HTTPBasicAuthHandler()
authinfo.add_password(realm='PDQ Application',
                      uri='https://mahler:8092/site-updates.py',
                      user='klem',
                      passwd='geheim$parole')

proxy_support = urllib.request.ProxyHandler({"http" : "http://ahad-haam:3128"})

# build a new opener that adds authentication and caching FTP handlers
opener = urllib.request.build_opener(proxy_support, authinfo,
                                     urllib.request.CacheFTPHandler)

# install it
urllib.request.install_opener(opener)

f = urllib.request.urlopen('http://www.python.org/')
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import bytes, dict, filter, input, int, map, open, str
from future.utils import PY2, PY3, raise_with_traceback
import base64, bisect, hashlib, array
from future.backports import email
from future.backports.http import client as http_client
from .error import URLError, HTTPError, ContentTooShortError
from .parse import urlparse, urlsplit, urljoin, unwrap, quote, unquote, splittype, splithost, splitport, splituser, splitpasswd, splitattr, splitquery, splitvalue, splittag, to_bytes, urlunparse
from .response import addinfourl, addclosehook
import io, os, posixpath, re, socket, sys, time, collections, tempfile, contextlib, warnings
try:
    import ssl
    from ssl import SSLContext
except ImportError:
    _have_ssl = False
else:
    _have_ssl = True

__all__ = [
 b'Request', b'OpenerDirector', b'BaseHandler', b'HTTPDefaultErrorHandler',
 b'HTTPRedirectHandler', b'HTTPCookieProcessor', b'ProxyHandler',
 b'HTTPPasswordMgr', b'HTTPPasswordMgrWithDefaultRealm',
 b'AbstractBasicAuthHandler', b'HTTPBasicAuthHandler', b'ProxyBasicAuthHandler',
 b'AbstractDigestAuthHandler', b'HTTPDigestAuthHandler', b'ProxyDigestAuthHandler',
 b'HTTPHandler', b'FileHandler', b'FTPHandler', b'CacheFTPHandler',
 b'UnknownHandler', b'HTTPErrorProcessor',
 b'urlopen', b'install_opener', b'build_opener',
 b'pathname2url', b'url2pathname', b'getproxies',
 b'urlretrieve', b'urlcleanup', b'URLopener', b'FancyURLopener']
__version__ = sys.version[:3]
_opener = None

def urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, **_3to2kwargs):
    global _opener
    if b'cadefault' in _3to2kwargs:
        cadefault = _3to2kwargs[b'cadefault']
        del _3to2kwargs[b'cadefault']
    else:
        cadefault = False
    if b'capath' in _3to2kwargs:
        capath = _3to2kwargs[b'capath']
        del _3to2kwargs[b'capath']
    else:
        capath = None
    if b'cafile' in _3to2kwargs:
        cafile = _3to2kwargs[b'cafile']
        del _3to2kwargs[b'cafile']
    else:
        cafile = None
    if cafile or capath or cadefault:
        if not _have_ssl:
            raise ValueError(b'SSL support not available')
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.options |= ssl.OP_NO_SSLv2
        context.verify_mode = ssl.CERT_REQUIRED
        if cafile or capath:
            context.load_verify_locations(cafile, capath)
        else:
            context.set_default_verify_paths()
        https_handler = HTTPSHandler(context=context, check_hostname=True)
        opener = build_opener(https_handler)
    elif _opener is None:
        _opener = opener = build_opener()
    else:
        opener = _opener
    return opener.open(url, data, timeout)


def install_opener(opener):
    global _opener
    _opener = opener


_url_tempfiles = []

def urlretrieve(url, filename=None, reporthook=None, data=None):
    """
    Retrieve a URL into a temporary location on disk.

    Requires a URL argument. If a filename is passed, it is used as
    the temporary file location. The reporthook argument should be
    a callable that accepts a block number, a read size, and the
    total file size of the URL target. The data argument should be
    valid URL encoded data.

    If a filename is passed and the URL points to a local resource,
    the result is a copy from local file to new file.

    Returns a tuple containing the path to the newly created
    data file as well as the resulting HTTPMessage object.
    """
    url_type, path = splittype(url)
    with contextlib.closing(urlopen(url, data)) as (fp):
        headers = fp.info()
        if url_type == b'file' and not filename:
            return (os.path.normpath(path), headers)
        if filename:
            tfp = open(filename, b'wb')
        else:
            tfp = tempfile.NamedTemporaryFile(delete=False)
            filename = tfp.name
            _url_tempfiles.append(filename)
        with tfp:
            result = (
             filename, headers)
            bs = 8192
            size = -1
            read = 0
            blocknum = 0
            if b'content-length' in headers:
                size = int(headers[b'Content-Length'])
            if reporthook:
                reporthook(blocknum, bs, size)
            while True:
                block = fp.read(bs)
                if not block:
                    break
                read += len(block)
                tfp.write(block)
                blocknum += 1
                if reporthook:
                    reporthook(blocknum, bs, size)

    if size >= 0 and read < size:
        raise ContentTooShortError(b'retrieval incomplete: got only %i out of %i bytes' % (
         read, size), result)
    return result


def urlcleanup():
    global _opener
    for temp_file in _url_tempfiles:
        try:
            os.unlink(temp_file)
        except EnvironmentError:
            pass

    del _url_tempfiles[:]
    if _opener:
        _opener = None
    return


if PY3:
    _cut_port_re = re.compile(b':\\d+$', re.ASCII)
else:
    _cut_port_re = re.compile(b':\\d+$')

def request_host(request):
    """Return request-host, as defined by RFC 2965.

    Variation from RFC: returned value is lowercased, for convenient
    comparison.

    """
    url = request.full_url
    host = urlparse(url)[1]
    if host == b'':
        host = request.get_header(b'Host', b'')
    host = _cut_port_re.sub(b'', host, 1)
    return host.lower()


class Request(object):

    def __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None):
        self.full_url = unwrap(url)
        self.full_url, self.fragment = splittag(self.full_url)
        self.data = data
        self.headers = {}
        self._tunnel_host = None
        for key, value in headers.items():
            self.add_header(key, value)

        self.unredirected_hdrs = {}
        if origin_req_host is None:
            origin_req_host = request_host(self)
        self.origin_req_host = origin_req_host
        self.unverifiable = unverifiable
        self.method = method
        self._parse()
        return

    def _parse(self):
        self.type, rest = splittype(self.full_url)
        if self.type is None:
            raise ValueError(b'unknown url type: %r' % self.full_url)
        self.host, self.selector = splithost(rest)
        if self.host:
            self.host = unquote(self.host)
        return

    def get_method(self):
        """Return a string indicating the HTTP request method."""
        if self.method is not None:
            return self.method
        else:
            if self.data is not None:
                return b'POST'
            else:
                return b'GET'

            return

    def get_full_url(self):
        if self.fragment:
            return b'%s#%s' % (self.full_url, self.fragment)
        else:
            return self.full_url

    def add_data(self, data):
        msg = b'Request.add_data method is deprecated.'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        self.data = data

    def has_data(self):
        msg = b'Request.has_data method is deprecated.'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        return self.data is not None

    def get_data(self):
        msg = b'Request.get_data method is deprecated.'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        return self.data

    def get_type(self):
        msg = b'Request.get_type method is deprecated.'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        return self.type

    def get_host(self):
        msg = b'Request.get_host method is deprecated.'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        return self.host

    def get_selector(self):
        msg = b'Request.get_selector method is deprecated.'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        return self.selector

    def is_unverifiable(self):
        msg = b'Request.is_unverifiable method is deprecated.'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        return self.unverifiable

    def get_origin_req_host(self):
        msg = b'Request.get_origin_req_host method is deprecated.'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        return self.origin_req_host

    def set_proxy(self, host, type):
        if self.type == b'https' and not self._tunnel_host:
            self._tunnel_host = self.host
        else:
            self.type = type
            self.selector = self.full_url
        self.host = host

    def has_proxy(self):
        return self.selector == self.full_url

    def add_header(self, key, val):
        self.headers[key.capitalize()] = val

    def add_unredirected_header(self, key, val):
        self.unredirected_hdrs[key.capitalize()] = val

    def has_header(self, header_name):
        return header_name in self.headers or header_name in self.unredirected_hdrs

    def get_header(self, header_name, default=None):
        return self.headers.get(header_name, self.unredirected_hdrs.get(header_name, default))

    def header_items(self):
        hdrs = self.unredirected_hdrs.copy()
        hdrs.update(self.headers)
        return list(hdrs.items())


class OpenerDirector(object):

    def __init__(self):
        client_version = b'Python-urllib/%s' % __version__
        self.addheaders = [(b'User-agent', client_version)]
        self.handlers = []
        self.handle_open = {}
        self.handle_error = {}
        self.process_response = {}
        self.process_request = {}

    def add_handler(self, handler):
        if not hasattr(handler, b'add_parent'):
            raise TypeError(b'expected BaseHandler instance, got %r' % type(handler))
        added = False
        for meth in dir(handler):
            if meth in ('redirect_request', 'do_open', 'proxy_open'):
                continue
            i = meth.find(b'_')
            protocol = meth[:i]
            condition = meth[i + 1:]
            if condition.startswith(b'error'):
                j = condition.find(b'_') + i + 1
                kind = meth[j + 1:]
                try:
                    kind = int(kind)
                except ValueError:
                    pass

                lookup = self.handle_error.get(protocol, {})
                self.handle_error[protocol] = lookup
            elif condition == b'open':
                kind = protocol
                lookup = self.handle_open
            elif condition == b'response':
                kind = protocol
                lookup = self.process_response
            elif condition == b'request':
                kind = protocol
                lookup = self.process_request
            else:
                continue
            handlers = lookup.setdefault(kind, [])
            if handlers:
                bisect.insort(handlers, handler)
            else:
                handlers.append(handler)
            added = True

        if added:
            bisect.insort(self.handlers, handler)
            handler.add_parent(self)

    def close(self):
        pass

    def _call_chain(self, chain, kind, meth_name, *args):
        handlers = chain.get(kind, ())
        for handler in handlers:
            func = getattr(handler, meth_name)
            result = func(*args)
            if result is not None:
                return result

        return

    def open(self, fullurl, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """
        Accept a URL or a Request object

        Python-Future: if the URL is passed as a byte-string, decode it first.
        """
        if isinstance(fullurl, bytes):
            fullurl = fullurl.decode()
        if isinstance(fullurl, str):
            req = Request(fullurl, data)
        else:
            req = fullurl
            if data is not None:
                req.data = data
            req.timeout = timeout
            protocol = req.type
            meth_name = protocol + b'_request'
            for processor in self.process_request.get(protocol, []):
                meth = getattr(processor, meth_name)
                req = meth(req)

            response = self._open(req, data)
            meth_name = protocol + b'_response'
            for processor in self.process_response.get(protocol, []):
                meth = getattr(processor, meth_name)
                response = meth(req, response)

        return response

    def _open(self, req, data=None):
        result = self._call_chain(self.handle_open, b'default', b'default_open', req)
        if result:
            return result
        protocol = req.type
        result = self._call_chain(self.handle_open, protocol, protocol + b'_open', req)
        if result:
            return result
        return self._call_chain(self.handle_open, b'unknown', b'unknown_open', req)

    def error(self, proto, *args):
        if proto in ('http', 'https'):
            dict = self.handle_error[b'http']
            proto = args[2]
            meth_name = b'http_error_%s' % proto
            http_err = 1
            orig_args = args
        else:
            dict = self.handle_error
            meth_name = proto + b'_error'
            http_err = 0
        args = (
         dict, proto, meth_name) + args
        result = self._call_chain(*args)
        if result:
            return result
        if http_err:
            args = (
             dict, b'default', b'http_error_default') + orig_args
            return self._call_chain(*args)


def build_opener(*handlers):
    """Create an opener object from a list of handlers.

    The opener will use several default handlers, including support
    for HTTP, FTP and when applicable HTTPS.

    If any of the handlers passed as arguments are subclasses of the
    default handlers, the default handlers will not be used.
    """

    def isclass(obj):
        return isinstance(obj, type) or hasattr(obj, b'__bases__')

    opener = OpenerDirector()
    default_classes = [ProxyHandler, UnknownHandler, HTTPHandler,
     HTTPDefaultErrorHandler, HTTPRedirectHandler,
     FTPHandler, FileHandler, HTTPErrorProcessor]
    if hasattr(http_client, b'HTTPSConnection'):
        default_classes.append(HTTPSHandler)
    skip = set()
    for klass in default_classes:
        for check in handlers:
            if isclass(check):
                if issubclass(check, klass):
                    skip.add(klass)
            elif isinstance(check, klass):
                skip.add(klass)

    for klass in skip:
        default_classes.remove(klass)

    for klass in default_classes:
        opener.add_handler(klass())

    for h in handlers:
        if isclass(h):
            h = h()
        opener.add_handler(h)

    return opener


class BaseHandler(object):
    handler_order = 500

    def add_parent(self, parent):
        self.parent = parent

    def close(self):
        pass

    def __lt__(self, other):
        if not hasattr(other, b'handler_order'):
            return True
        return self.handler_order < other.handler_order


class HTTPErrorProcessor(BaseHandler):
    """Process HTTP error responses."""
    handler_order = 1000

    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()
        if not 200 <= code < 300:
            response = self.parent.error(b'http', request, response, code, msg, hdrs)
        return response

    https_response = http_response


class HTTPDefaultErrorHandler(BaseHandler):

    def http_error_default(self, req, fp, code, msg, hdrs):
        raise HTTPError(req.full_url, code, msg, hdrs, fp)


class HTTPRedirectHandler(BaseHandler):
    max_repeats = 4
    max_redirections = 10

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Return a Request or None in response to a redirect.

        This is called by the http_error_30x methods when a
        redirection response is received.  If a redirection should
        take place, return a new Request to allow http_error_30x to
        perform the redirect.  Otherwise, raise HTTPError if no-one
        else should try to handle this url.  Return None if you can't
        but another Handler might.
        """
        m = req.get_method()
        if not (code in (301, 302, 303, 307) and m in ('GET', 'HEAD') or code in (301,
                                                                                  302,
                                                                                  303) and m == b'POST'):
            raise HTTPError(req.full_url, code, msg, headers, fp)
        newurl = newurl.replace(b' ', b'%20')
        CONTENT_HEADERS = ('content-length', 'content-type')
        newheaders = dict((k, v) for k, v in req.headers.items() if k.lower() not in CONTENT_HEADERS)
        return Request(newurl, headers=newheaders, origin_req_host=req.origin_req_host, unverifiable=True)

    def http_error_302(self, req, fp, code, msg, headers):
        if b'location' in headers:
            newurl = headers[b'location']
        elif b'uri' in headers:
            newurl = headers[b'uri']
        else:
            return
        urlparts = urlparse(newurl)
        if urlparts.scheme not in ('http', 'https', 'ftp', ''):
            raise HTTPError(newurl, code, b"%s - Redirection to url '%s' is not allowed" % (msg, newurl), headers, fp)
        if not urlparts.path:
            urlparts = list(urlparts)
            urlparts[2] = b'/'
        newurl = urlunparse(urlparts)
        newurl = urljoin(req.full_url, newurl)
        new = self.redirect_request(req, fp, code, msg, headers, newurl)
        if new is None:
            return
        else:
            if hasattr(req, b'redirect_dict'):
                visited = new.redirect_dict = req.redirect_dict
                if visited.get(newurl, 0) >= self.max_repeats or len(visited) >= self.max_redirections:
                    raise HTTPError(req.full_url, code, self.inf_msg + msg, headers, fp)
            else:
                visited = new.redirect_dict = req.redirect_dict = {}
            visited[newurl] = visited.get(newurl, 0) + 1
            fp.read()
            fp.close()
            return self.parent.open(new, timeout=req.timeout)

    http_error_301 = http_error_303 = http_error_307 = http_error_302
    inf_msg = b'The HTTP server returned a redirect error that would lead to an infinite loop.\nThe last 30x error message was:\n'


def _parse_proxy(proxy):
    """Return (scheme, user, password, host/port) given a URL or an authority.

    If a URL is supplied, it must have an authority (host:port) component.
    According to RFC 3986, having an authority component means the URL must
    have two slashes after the scheme:

    >>> _parse_proxy('file:/ftp.example.com/')
    Traceback (most recent call last):
    ValueError: proxy URL with no authority: 'file:/ftp.example.com/'

    The first three items of the returned tuple may be None.

    Examples of authority parsing:

    >>> _parse_proxy('proxy.example.com')
    (None, None, None, 'proxy.example.com')
    >>> _parse_proxy('proxy.example.com:3128')
    (None, None, None, 'proxy.example.com:3128')

    The authority component may optionally include userinfo (assumed to be
    username:password):

    >>> _parse_proxy('joe:password@proxy.example.com')
    (None, 'joe', 'password', 'proxy.example.com')
    >>> _parse_proxy('joe:password@proxy.example.com:3128')
    (None, 'joe', 'password', 'proxy.example.com:3128')

    Same examples, but with URLs instead:

    >>> _parse_proxy('http://proxy.example.com/')
    ('http', None, None, 'proxy.example.com')
    >>> _parse_proxy('http://proxy.example.com:3128/')
    ('http', None, None, 'proxy.example.com:3128')
    >>> _parse_proxy('http://joe:password@proxy.example.com/')
    ('http', 'joe', 'password', 'proxy.example.com')
    >>> _parse_proxy('http://joe:password@proxy.example.com:3128')
    ('http', 'joe', 'password', 'proxy.example.com:3128')

    Everything after the authority is ignored:

    >>> _parse_proxy('ftp://joe:password@proxy.example.com/rubbish:3128')
    ('ftp', 'joe', 'password', 'proxy.example.com')

    Test for no trailing '/' case:

    >>> _parse_proxy('http://joe:password@proxy.example.com')
    ('http', 'joe', 'password', 'proxy.example.com')

    """
    scheme, r_scheme = splittype(proxy)
    if not r_scheme.startswith(b'/'):
        scheme = None
        authority = proxy
    else:
        if not r_scheme.startswith(b'//'):
            raise ValueError(b'proxy URL with no authority: %r' % proxy)
        end = r_scheme.find(b'/', 2)
        if end == -1:
            end = None
        authority = r_scheme[2:end]
    userinfo, hostport = splituser(authority)
    if userinfo is not None:
        user, password = splitpasswd(userinfo)
    else:
        user = password = None
    return (
     scheme, user, password, hostport)


class ProxyHandler(BaseHandler):
    handler_order = 100

    def __init__--- This code section failed: ---

 L. 803         0  LOAD_FAST             1  'proxies'
                3  LOAD_CONST               None
                6  COMPARE_OP            8  is
                9  POP_JUMP_IF_FALSE    24  'to 24'

 L. 804        12  LOAD_GLOBAL           1  'getproxies'
               15  CALL_FUNCTION_0       0  None
               18  STORE_FAST            1  'proxies'
               21  JUMP_FORWARD          0  'to 24'
             24_0  COME_FROM            21  '21'

 L. 805        24  LOAD_GLOBAL           2  'hasattr'
               27  LOAD_FAST             1  'proxies'
               30  LOAD_CONST               'keys'
               33  CALL_FUNCTION_2       2  None
               36  POP_JUMP_IF_TRUE     48  'to 48'
               39  LOAD_ASSERT              AssertionError
               42  LOAD_CONST               'proxies must be a mapping'
               45  RAISE_VARARGS_2       2  None

 L. 806        48  LOAD_FAST             1  'proxies'
               51  LOAD_FAST             0  'self'
               54  STORE_ATTR            4  'proxies'

 L. 807        57  SETUP_LOOP           61  'to 121'
               60  LOAD_FAST             1  'proxies'
               63  LOAD_ATTR             5  'items'
               66  CALL_FUNCTION_0       0  None
               69  GET_ITER         
               70  FOR_ITER             47  'to 120'
               73  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST            2  'type'
               79  STORE_FAST            3  'url'

 L. 808        82  LOAD_GLOBAL           6  'setattr'
               85  LOAD_FAST             0  'self'
               88  LOAD_CONST               '%s_open'
               91  LOAD_FAST             2  'type'
               94  BINARY_MODULO    

 L. 809        95  LOAD_FAST             3  'url'
               98  LOAD_FAST             2  'type'
              101  LOAD_FAST             0  'self'
              104  LOAD_ATTR             7  'proxy_open'
              107  LOAD_LAMBDA              '<code_object <lambda>>'
              110  MAKE_FUNCTION_3       3  None
              113  CALL_FUNCTION_3       3  None
              116  POP_TOP          
              117  JUMP_BACK            70  'to 70'
              120  POP_BLOCK        
            121_0  COME_FROM            57  '57'
              121  LOAD_CONST               None
              124  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 121

    def proxy_open(self, req, proxy, type):
        orig_type = req.type
        proxy_type, user, password, hostport = _parse_proxy(proxy)
        if proxy_type is None:
            proxy_type = orig_type
        if req.host and proxy_bypass(req.host):
            return
        else:
            if user and password:
                user_pass = b'%s:%s' % (unquote(user),
                 unquote(password))
                creds = base64.b64encode(user_pass.encode()).decode(b'ascii')
                req.add_header(b'Proxy-authorization', b'Basic ' + creds)
            hostport = unquote(hostport)
            req.set_proxy(hostport, proxy_type)
            if orig_type == proxy_type or orig_type == b'https':
                return
            return self.parent.open(req, timeout=req.timeout)
            return


class HTTPPasswordMgr(object):

    def __init__(self):
        self.passwd = {}

    def add_password(self, realm, uri, user, passwd):
        if isinstance(uri, str):
            uri = [
             uri]
        if realm not in self.passwd:
            self.passwd[realm] = {}
        for default_port in (True, False):
            reduced_uri = tuple([ self.reduce_uri(u, default_port) for u in uri ])
            self.passwd[realm][reduced_uri] = (
             user, passwd)

    def find_user_password(self, realm, authuri):
        domains = self.passwd.get(realm, {})
        for default_port in (True, False):
            reduced_authuri = self.reduce_uri(authuri, default_port)
            for uris, authinfo in domains.items():
                for uri in uris:
                    if self.is_suburi(uri, reduced_authuri):
                        return authinfo

        return (None, None)

    def reduce_uri(self, uri, default_port=True):
        """Accept authority or URI and extract only the authority and path."""
        parts = urlsplit(uri)
        if parts[1]:
            scheme = parts[0]
            authority = parts[1]
            path = parts[2] or b'/'
        else:
            scheme = None
            authority = uri
            path = b'/'
        host, port = splitport(authority)
        if default_port and port is None and scheme is not None:
            dport = {b'http': 80, b'https': 443}.get(scheme)
            if dport is not None:
                authority = b'%s:%d' % (host, dport)
        return (
         authority, path)

    def is_suburi(self, base, test):
        """Check if test is below base in a URI tree

        Both args must be URIs in reduced form.
        """
        if base == test:
            return True
        if base[0] != test[0]:
            return False
        common = posixpath.commonprefix((base[1], test[1]))
        if len(common) == len(base[1]):
            return True
        return False


class HTTPPasswordMgrWithDefaultRealm(HTTPPasswordMgr):

    def find_user_password(self, realm, authuri):
        user, password = HTTPPasswordMgr.find_user_password(self, realm, authuri)
        if user is not None:
            return (user, password)
        else:
            return HTTPPasswordMgr.find_user_password(self, None, authuri)


class AbstractBasicAuthHandler(object):
    rx = re.compile(b'(?:.*,)*[ \t]*([^ \t]+)[ \t]+realm=(["\']?)([^"\']*)\\2', re.I)

    def __init__(self, password_mgr=None):
        if password_mgr is None:
            password_mgr = HTTPPasswordMgr()
        self.passwd = password_mgr
        self.add_password = self.passwd.add_password
        self.retried = 0
        return

    def reset_retry_count(self):
        self.retried = 0

    def http_error_auth_reqed(self, authreq, host, req, headers):
        authreq = headers.get(authreq, None)
        if self.retried > 5:
            raise HTTPError(req.get_full_url(), 401, b'basic auth failed', headers, None)
        else:
            self.retried += 1
        if authreq:
            scheme = authreq.split()[0]
            if scheme.lower() != b'basic':
                raise ValueError(b"AbstractBasicAuthHandler does not support the following scheme: '%s'" % scheme)
            else:
                mo = AbstractBasicAuthHandler.rx.search(authreq)
                if mo:
                    scheme, quote, realm = mo.groups()
                    if quote not in ('"', "'"):
                        warnings.warn(b'Basic Auth Realm was unquoted', UserWarning, 2)
                    if scheme.lower() == b'basic':
                        response = self.retry_http_basic_auth(host, req, realm)
                        if response and response.code != 401:
                            self.retried = 0
                        return response
        return

    def retry_http_basic_auth(self, host, req, realm):
        user, pw = self.passwd.find_user_password(realm, host)
        if pw is not None:
            raw = b'%s:%s' % (user, pw)
            auth = b'Basic ' + base64.b64encode(raw.encode()).decode(b'ascii')
            if req.headers.get(self.auth_header, None) == auth:
                return
            req.add_unredirected_header(self.auth_header, auth)
            return self.parent.open(req, timeout=req.timeout)
        else:
            return
            return


class HTTPBasicAuthHandler(AbstractBasicAuthHandler, BaseHandler):
    auth_header = b'Authorization'

    def http_error_401(self, req, fp, code, msg, headers):
        url = req.full_url
        response = self.http_error_auth_reqed(b'www-authenticate', url, req, headers)
        self.reset_retry_count()
        return response


class ProxyBasicAuthHandler(AbstractBasicAuthHandler, BaseHandler):
    auth_header = b'Proxy-authorization'

    def http_error_407(self, req, fp, code, msg, headers):
        authority = req.host
        response = self.http_error_auth_reqed(b'proxy-authenticate', authority, req, headers)
        self.reset_retry_count()
        return response


_randombytes = os.urandom

class AbstractDigestAuthHandler(object):

    def __init__(self, passwd=None):
        if passwd is None:
            passwd = HTTPPasswordMgr()
        self.passwd = passwd
        self.add_password = self.passwd.add_password
        self.retried = 0
        self.nonce_count = 0
        self.last_nonce = None
        return

    def reset_retry_count(self):
        self.retried = 0

    def http_error_auth_reqed(self, auth_header, host, req, headers):
        authreq = headers.get(auth_header, None)
        if self.retried > 5:
            raise HTTPError(req.full_url, 401, b'digest auth failed', headers, None)
        else:
            self.retried += 1
        if authreq:
            scheme = authreq.split()[0]
            if scheme.lower() == b'digest':
                return self.retry_http_digest_auth(req, authreq)
            if scheme.lower() != b'basic':
                raise ValueError(b"AbstractDigestAuthHandler does not support the following scheme: '%s'" % scheme)
        return

    def retry_http_digest_auth(self, req, auth):
        token, challenge = auth.split(b' ', 1)
        chal = parse_keqv_list(filter(None, parse_http_list(challenge)))
        auth = self.get_authorization(req, chal)
        if auth:
            auth_val = b'Digest %s' % auth
            if req.headers.get(self.auth_header, None) == auth_val:
                return
            req.add_unredirected_header(self.auth_header, auth_val)
            resp = self.parent.open(req, timeout=req.timeout)
            return resp
        else:
            return

    def get_cnonce(self, nonce):
        s = b'%s:%s:%s:' % (self.nonce_count, nonce, time.ctime())
        b = s.encode(b'ascii') + _randombytes(8)
        dig = hashlib.sha1(b).hexdigest()
        return dig[:16]

    def get_authorization(self, req, chal):
        try:
            realm = chal[b'realm']
            nonce = chal[b'nonce']
            qop = chal.get(b'qop')
            algorithm = chal.get(b'algorithm', b'MD5')
            opaque = chal.get(b'opaque', None)
        except KeyError:
            return

        H, KD = self.get_algorithm_impls(algorithm)
        if H is None:
            return
        else:
            user, pw = self.passwd.find_user_password(realm, req.full_url)
            if user is None:
                return
            if req.data is not None:
                entdig = self.get_entity_digest(req.data, chal)
            else:
                entdig = None
            A1 = b'%s:%s:%s' % (user, realm, pw)
            A2 = b'%s:%s' % (req.get_method(),
             req.selector)
            if qop == b'auth':
                if nonce == self.last_nonce:
                    self.nonce_count += 1
                else:
                    self.nonce_count = 1
                    self.last_nonce = nonce
                ncvalue = b'%08x' % self.nonce_count
                cnonce = self.get_cnonce(nonce)
                noncebit = b'%s:%s:%s:%s:%s' % (nonce, ncvalue, cnonce, qop, H(A2))
                respdig = KD(H(A1), noncebit)
            elif qop is None:
                respdig = KD(H(A1), b'%s:%s' % (nonce, H(A2)))
            else:
                raise URLError(b"qop '%s' is not supported." % qop)
            base = b'username="%s", realm="%s", nonce="%s", uri="%s", response="%s"' % (
             user, realm, nonce, req.selector,
             respdig)
            if opaque:
                base += b', opaque="%s"' % opaque
            if entdig:
                base += b', digest="%s"' % entdig
            base += b', algorithm="%s"' % algorithm
            if qop:
                base += b', qop=auth, nc=%s, cnonce="%s"' % (ncvalue, cnonce)
            return base

    def get_algorithm_impls(self, algorithm):
        if algorithm == b'MD5':
            H = lambda x: hashlib.md5(x.encode(b'ascii')).hexdigest()
        elif algorithm == b'SHA':
            H = lambda x: hashlib.sha1(x.encode(b'ascii')).hexdigest()
        KD = lambda s, d: H(b'%s:%s' % (s, d))
        return (H, KD)

    def get_entity_digest(self, data, chal):
        return


class HTTPDigestAuthHandler(BaseHandler, AbstractDigestAuthHandler):
    """An authentication protocol defined by RFC 2069

    Digest authentication improves on basic authentication because it
    does not transmit passwords in the clear.
    """
    auth_header = b'Authorization'
    handler_order = 490

    def http_error_401(self, req, fp, code, msg, headers):
        host = urlparse(req.full_url)[1]
        retry = self.http_error_auth_reqed(b'www-authenticate', host, req, headers)
        self.reset_retry_count()
        return retry


class ProxyDigestAuthHandler(BaseHandler, AbstractDigestAuthHandler):
    auth_header = b'Proxy-Authorization'
    handler_order = 490

    def http_error_407(self, req, fp, code, msg, headers):
        host = req.host
        retry = self.http_error_auth_reqed(b'proxy-authenticate', host, req, headers)
        self.reset_retry_count()
        return retry


class AbstractHTTPHandler(BaseHandler):

    def __init__(self, debuglevel=0):
        self._debuglevel = debuglevel

    def set_http_debuglevel(self, level):
        self._debuglevel = level

    def do_request_(self, request):
        host = request.host
        if not host:
            raise URLError(b'no host given')
        if request.data is not None:
            data = request.data
            if isinstance(data, str):
                msg = b'POST data should be bytes or an iterable of bytes. It cannot be of type str.'
                raise TypeError(msg)
            if not request.has_header(b'Content-type'):
                request.add_unredirected_header(b'Content-type', b'application/x-www-form-urlencoded')
            if not request.has_header(b'Content-length'):
                size = None
                try:
                    if PY2 and isinstance(data, array.array):
                        size = len(data) * data.itemsize
                    else:
                        mv = memoryview(data)
                        size = len(mv) * mv.itemsize
                except TypeError:
                    if isinstance(data, collections.Iterable):
                        raise ValueError(b'Content-Length should be specified for iterable data of type %r %r' % (
                         type(data),
                         data))
                else:
                    request.add_unredirected_header(b'Content-length', b'%d' % size)

        sel_host = host
        if request.has_proxy():
            scheme, sel = splittype(request.selector)
            sel_host, sel_path = splithost(sel)
        if not request.has_header(b'Host'):
            request.add_unredirected_header(b'Host', sel_host)
        for name, value in self.parent.addheaders:
            name = name.capitalize()
            if not request.has_header(name):
                request.add_unredirected_header(name, value)

        return request

    def do_open(self, http_class, req, **http_conn_args):
        """Return an HTTPResponse object for the request, using http_class.

        http_class must implement the HTTPConnection API from http.client.
        """
        host = req.host
        if not host:
            raise URLError(b'no host given')
        h = http_class(host, timeout=req.timeout, **http_conn_args)
        headers = dict(req.unredirected_hdrs)
        headers.update(dict((k, v) for k, v in req.headers.items() if k not in headers))
        headers[b'Connection'] = b'close'
        headers = dict((name.title(), val) for name, val in headers.items())
        if req._tunnel_host:
            tunnel_headers = {}
            proxy_auth_hdr = b'Proxy-Authorization'
            if proxy_auth_hdr in headers:
                tunnel_headers[proxy_auth_hdr] = headers[proxy_auth_hdr]
                del headers[proxy_auth_hdr]
            h.set_tunnel(req._tunnel_host, headers=tunnel_headers)
        try:
            h.request(req.get_method(), req.selector, req.data, headers)
        except socket.error as err:
            h.close()
            raise URLError(err)

        r = h.getresponse()
        if h.sock:
            h.sock.close()
            h.sock = None
        r.url = req.get_full_url()
        r.msg = r.reason
        return r


class HTTPHandler(AbstractHTTPHandler):

    def http_open(self, req):
        return self.do_open(http_client.HTTPConnection, req)

    http_request = AbstractHTTPHandler.do_request_


if hasattr(http_client, b'HTTPSConnection'):

    class HTTPSHandler(AbstractHTTPHandler):

        def __init__(self, debuglevel=0, context=None, check_hostname=None):
            AbstractHTTPHandler.__init__(self, debuglevel)
            self._context = context
            self._check_hostname = check_hostname

        def https_open(self, req):
            return self.do_open(http_client.HTTPSConnection, req, context=self._context, check_hostname=self._check_hostname)

        https_request = AbstractHTTPHandler.do_request_


    __all__.append(b'HTTPSHandler')

class HTTPCookieProcessor(BaseHandler):

    def __init__(self, cookiejar=None):
        import future.backports.http.cookiejar as http_cookiejar
        if cookiejar is None:
            cookiejar = http_cookiejar.CookieJar()
        self.cookiejar = cookiejar
        return

    def http_request(self, request):
        self.cookiejar.add_cookie_header(request)
        return request

    def http_response(self, request, response):
        self.cookiejar.extract_cookies(response, request)
        return response

    https_request = http_request
    https_response = http_response


class UnknownHandler(BaseHandler):

    def unknown_open(self, req):
        type = req.type
        raise URLError(b'unknown url type: %s' % type)


def parse_keqv_list(l):
    """Parse list of key=value strings where keys are not duplicated."""
    parsed = {}
    for elt in l:
        k, v = elt.split(b'=', 1)
        if v[0] == b'"' and v[(-1)] == b'"':
            v = v[1:-1]
        parsed[k] = v

    return parsed


def parse_http_list(s):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Neither commas nor quotes count if they are escaped.
    Only double-quotes count, not single-quotes.
    """
    res = []
    part = b''
    escape = quote = False
    for cur in s:
        if escape:
            part += cur
            escape = False
            continue
        if quote:
            if cur == b'\\':
                escape = True
                continue
            elif cur == b'"':
                quote = False
            part += cur
            continue
        if cur == b',':
            res.append(part)
            part = b''
            continue
        if cur == b'"':
            quote = True
        part += cur

    if part:
        res.append(part)
    return [ part.strip() for part in res ]


class FileHandler(BaseHandler):

    def file_open(self, req):
        url = req.selector
        if url[:2] == b'//' and url[2:3] != b'/' and req.host and req.host != b'localhost':
            if req.host is not self.get_names():
                raise URLError(b'file:// scheme is supported only on localhost')
        else:
            return self.open_local_file(req)

    names = None

    def get_names(self):
        if FileHandler.names is None:
            try:
                FileHandler.names = tuple(socket.gethostbyname_ex(b'localhost')[2] + socket.gethostbyname_ex(socket.gethostname())[2])
            except socket.gaierror:
                FileHandler.names = (
                 socket.gethostbyname(b'localhost'),)

        return FileHandler.names

    def open_local_file(self, req):
        import future.backports.email.utils as email_utils, mimetypes
        host = req.host
        filename = req.selector
        localfile = url2pathname(filename)
        try:
            stats = os.stat(localfile)
            size = stats.st_size
            modified = email_utils.formatdate(stats.st_mtime, usegmt=True)
            mtype = mimetypes.guess_type(filename)[0]
            headers = email.message_from_string(b'Content-type: %s\nContent-length: %d\nLast-modified: %s\n' % (
             mtype or b'text/plain', size, modified))
            if host:
                host, port = splitport(host)
            if not host or not port and _safe_gethostbyname(host) in self.get_names():
                if host:
                    origurl = b'file://' + host + filename
                else:
                    origurl = b'file://' + filename
                return addinfourl(open(localfile, b'rb'), headers, origurl)
        except OSError as exp:
            raise URLError(exp)

        raise URLError(b'file not on local host')


def _safe_gethostbyname(host):
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return

    return


class FTPHandler(BaseHandler):

    def ftp_open(self, req):
        import ftplib, mimetypes
        host = req.host
        if not host:
            raise URLError(b'ftp error: no host given')
        host, port = splitport(host)
        if port is None:
            port = ftplib.FTP_PORT
        else:
            port = int(port)
        user, host = splituser(host)
        if user:
            user, passwd = splitpasswd(user)
        else:
            passwd = None
        host = unquote(host)
        user = user or b''
        passwd = passwd or b''
        try:
            host = socket.gethostbyname(host)
        except socket.error as msg:
            raise URLError(msg)

        path, attrs = splitattr(req.selector)
        dirs = path.split(b'/')
        dirs = list(map(unquote, dirs))
        dirs, file = dirs[:-1], dirs[(-1)]
        if dirs and not dirs[0]:
            dirs = dirs[1:]
        try:
            fw = self.connect_ftp(user, passwd, host, port, dirs, req.timeout)
            type = file and b'I' or b'D'
            for attr in attrs:
                attr, value = splitvalue(attr)
                if attr.lower() == b'type' and value in ('a', 'A', 'i', 'I', 'd', 'D'):
                    type = value.upper()

            fp, retrlen = fw.retrfile(file, type)
            headers = b''
            mtype = mimetypes.guess_type(req.full_url)[0]
            if mtype:
                headers += b'Content-type: %s\n' % mtype
            if retrlen is not None and retrlen >= 0:
                headers += b'Content-length: %d\n' % retrlen
            headers = email.message_from_string(headers)
            return addinfourl(fp, headers, req.full_url)
        except ftplib.all_errors as exp:
            exc = URLError(b'ftp error: %r' % exp)
            raise_with_traceback(exc)

        return

    def connect_ftp(self, user, passwd, host, port, dirs, timeout):
        return ftpwrapper(user, passwd, host, port, dirs, timeout, persistent=False)


class CacheFTPHandler(FTPHandler):

    def __init__(self):
        self.cache = {}
        self.timeout = {}
        self.soonest = 0
        self.delay = 60
        self.max_conns = 16

    def setTimeout(self, t):
        self.delay = t

    def setMaxConns(self, m):
        self.max_conns = m

    def connect_ftp(self, user, passwd, host, port, dirs, timeout):
        key = (
         user, host, port, (b'/').join(dirs), timeout)
        if key in self.cache:
            self.timeout[key] = time.time() + self.delay
        else:
            self.cache[key] = ftpwrapper(user, passwd, host, port, dirs, timeout)
            self.timeout[key] = time.time() + self.delay
        self.check_cache()
        return self.cache[key]

    def check_cache(self):
        t = time.time()
        if self.soonest <= t:
            for k, v in list(self.timeout.items()):
                if v < t:
                    self.cache[k].close()
                    del self.cache[k]
                    del self.timeout[k]

        self.soonest = min(list(self.timeout.values()))
        if len(self.cache) == self.max_conns:
            for k, v in list(self.timeout.items()):
                if v == self.soonest:
                    del self.cache[k]
                    del self.timeout[k]
                    break

            self.soonest = min(list(self.timeout.values()))

    def clear_cache(self):
        for conn in self.cache.values():
            conn.close()

        self.cache.clear()
        self.timeout.clear()


MAXFTPCACHE = 10
if os.name == b'nt':
    from nturl2path import url2pathname, pathname2url
else:

    def url2pathname(pathname):
        """OS-specific conversion from a relative URL of the 'file' scheme
        to a file system path; not recommended for general use."""
        return unquote(pathname)


    def pathname2url(pathname):
        """OS-specific conversion from a file system path to a relative URL
        of the 'file' scheme; not recommended for general use."""
        return quote(pathname)


ftpcache = {}

class URLopener(object):
    """Class to open URLs.
    This is a class rather than just a subroutine because we may need
    more than one set of global protocol-specific options.
    Note -- this is a base class for those who don't want the
    automatic handling of errors type 302 (relocated) and 401
    (authorization needed)."""
    __tempfiles = None
    version = b'Python-urllib/%s' % __version__

    def __init__--- This code section failed: ---

 L.1618         0  LOAD_CONST               '%(class)s style of invoking requests is deprecated. Use newer urlopen functions/methods'

 L.1619         3  BUILD_MAP_1           1  None
                6  LOAD_FAST             0  'self'
                9  LOAD_ATTR             0  '__class__'
               12  LOAD_ATTR             1  '__name__'
               15  LOAD_CONST               'class'
               18  STORE_MAP        
               19  BINARY_MODULO    
               20  STORE_FAST            3  'msg'

 L.1620        23  LOAD_GLOBAL           2  'warnings'
               26  LOAD_ATTR             3  'warn'
               29  LOAD_FAST             3  'msg'
               32  LOAD_GLOBAL           4  'DeprecationWarning'
               35  LOAD_CONST               'stacklevel'
               38  LOAD_CONST               3
               41  CALL_FUNCTION_258   258  None
               44  POP_TOP          

 L.1621        45  LOAD_FAST             1  'proxies'
               48  LOAD_CONST               None
               51  COMPARE_OP            8  is
               54  POP_JUMP_IF_FALSE    69  'to 69'

 L.1622        57  LOAD_GLOBAL           6  'getproxies'
               60  CALL_FUNCTION_0       0  None
               63  STORE_FAST            1  'proxies'
               66  JUMP_FORWARD          0  'to 69'
             69_0  COME_FROM            66  '66'

 L.1623        69  LOAD_GLOBAL           7  'hasattr'
               72  LOAD_FAST             1  'proxies'
               75  LOAD_CONST               'keys'
               78  CALL_FUNCTION_2       2  None
               81  POP_JUMP_IF_TRUE     93  'to 93'
               84  LOAD_ASSERT              AssertionError
               87  LOAD_CONST               'proxies must be a mapping'
               90  RAISE_VARARGS_2       2  None

 L.1624        93  LOAD_FAST             1  'proxies'
               96  LOAD_FAST             0  'self'
               99  STORE_ATTR            9  'proxies'

 L.1625       102  LOAD_FAST             2  'x509'
              105  LOAD_ATTR            10  'get'
              108  LOAD_CONST               'key_file'
              111  CALL_FUNCTION_1       1  None
              114  LOAD_FAST             0  'self'
              117  STORE_ATTR           11  'key_file'

 L.1626       120  LOAD_FAST             2  'x509'
              123  LOAD_ATTR            10  'get'
              126  LOAD_CONST               'cert_file'
              129  CALL_FUNCTION_1       1  None
              132  LOAD_FAST             0  'self'
              135  STORE_ATTR           12  'cert_file'

 L.1627       138  LOAD_CONST               'User-Agent'
              141  LOAD_FAST             0  'self'
              144  LOAD_ATTR            13  'version'
              147  BUILD_TUPLE_2         2 
              150  BUILD_LIST_1          1 
              153  LOAD_FAST             0  'self'
              156  STORE_ATTR           14  'addheaders'

 L.1628       159  BUILD_LIST_0          0 
              162  LOAD_FAST             0  'self'
              165  STORE_ATTR           15  '__tempfiles'

 L.1629       168  LOAD_GLOBAL          16  'os'
              171  LOAD_ATTR            17  'unlink'
              174  LOAD_FAST             0  'self'
              177  STORE_ATTR           18  '__unlink'

 L.1630       180  LOAD_CONST               None
              183  LOAD_FAST             0  'self'
              186  STORE_ATTR           19  'tempcache'

 L.1637       189  LOAD_GLOBAL          20  'ftpcache'
              192  LOAD_FAST             0  'self'
              195  STORE_ATTR           20  'ftpcache'
              198  LOAD_CONST               None
              201  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 198

    def __del__(self):
        self.close()

    def close(self):
        self.cleanup()

    def cleanup(self):
        if self.__tempfiles:
            for file in self.__tempfiles:
                try:
                    self.__unlink(file)
                except OSError:
                    pass

            del self.__tempfiles[:]
        if self.tempcache:
            self.tempcache.clear()

    def addheader(self, *args):
        """Add a header to be used by the HTTP interface only
        e.g. u.addheader('Accept', 'sound/basic')"""
        self.addheaders.append(args)

    def open(self, fullurl, data=None):
        """Use URLopener().open(file) instead of open(file, 'r')."""
        fullurl = unwrap(to_bytes(fullurl))
        fullurl = quote(fullurl, safe=b"%/:=&?~#+!$,;'@()*[]|")
        if self.tempcache and fullurl in self.tempcache:
            filename, headers = self.tempcache[fullurl]
            fp = open(filename, b'rb')
            return addinfourl(fp, headers, fullurl)
        else:
            urltype, url = splittype(fullurl)
            if not urltype:
                urltype = b'file'
            if urltype in self.proxies:
                proxy = self.proxies[urltype]
                urltype, proxyhost = splittype(proxy)
                host, selector = splithost(proxyhost)
                url = (host, fullurl)
            else:
                proxy = None
            name = b'open_' + urltype
            self.type = urltype
            name = name.replace(b'-', b'_')
            if not hasattr(self, name):
                if proxy:
                    return self.open_unknown_proxy(proxy, fullurl, data)
                else:
                    return self.open_unknown(fullurl, data)

            try:
                if data is None:
                    return getattr(self, name)(url)
                else:
                    return getattr(self, name)(url, data)

            except HTTPError:
                raise
            except socket.error as msg:
                raise_with_traceback(IOError(b'socket error', msg))

            return

    def open_unknown(self, fullurl, data=None):
        """Overridable interface to open unknown URL type."""
        type, url = splittype(fullurl)
        raise IOError(b'url error', b'unknown url type', type)

    def open_unknown_proxy(self, proxy, fullurl, data=None):
        """Overridable interface to open unknown URL type."""
        type, url = splittype(fullurl)
        raise IOError(b'url error', b'invalid proxy for %s' % type, proxy)

    def retrieve(self, url, filename=None, reporthook=None, data=None):
        """retrieve(url) returns (filename, headers) for a local object
        or (tempfilename, headers) for a remote object."""
        url = unwrap(to_bytes(url))
        if self.tempcache and url in self.tempcache:
            return self.tempcache[url]
        else:
            type, url1 = splittype(url)
            if filename is None and (not type or type == b'file'):
                try:
                    fp = self.open_local_file(url1)
                    hdrs = fp.info()
                    fp.close()
                    return (url2pathname(splithost(url1)[1]), hdrs)
                except IOError as msg:
                    pass

            fp = self.open(url, data)
            try:
                headers = fp.info()
                if filename:
                    tfp = open(filename, b'wb')
                else:
                    import tempfile
                    garbage, path = splittype(url)
                    garbage, path = splithost(path or b'')
                    path, garbage = splitquery(path or b'')
                    path, garbage = splitattr(path or b'')
                    suffix = os.path.splitext(path)[1]
                    fd, filename = tempfile.mkstemp(suffix)
                    self.__tempfiles.append(filename)
                    tfp = os.fdopen(fd, b'wb')
                try:
                    result = (
                     filename, headers)
                    if self.tempcache is not None:
                        self.tempcache[url] = result
                    bs = 8192
                    size = -1
                    read = 0
                    blocknum = 0
                    if b'content-length' in headers:
                        size = int(headers[b'Content-Length'])
                    if reporthook:
                        reporthook(blocknum, bs, size)
                    while 1:
                        block = fp.read(bs)
                        if not block:
                            break
                        read += len(block)
                        tfp.write(block)
                        blocknum += 1
                        if reporthook:
                            reporthook(blocknum, bs, size)

                finally:
                    tfp.close()

            finally:
                fp.close()

            if size >= 0 and read < size:
                raise ContentTooShortError(b'retrieval incomplete: got only %i out of %i bytes' % (
                 read, size), result)
            return result

    def _open_generic_http(self, connection_factory, url, data):
        """Make an HTTP connection using connection_class.

        This is an internal method that should be called from
        open_http() or open_https().

        Arguments:
        - connection_factory should take a host name and return an
          HTTPConnection instance.
        - url is the url to retrieval or a host, relative-path pair.
        - data is payload for a POST request or None.
        """
        user_passwd = None
        proxy_passwd = None
        if isinstance(url, str):
            host, selector = splithost(url)
            if host:
                user_passwd, host = splituser(host)
                host = unquote(host)
            realhost = host
        else:
            host, selector = url
            proxy_passwd, host = splituser(host)
            urltype, rest = splittype(selector)
            url = rest
            user_passwd = None
            if urltype.lower() != b'http':
                realhost = None
            else:
                realhost, rest = splithost(rest)
                if realhost:
                    user_passwd, realhost = splituser(realhost)
                if user_passwd:
                    selector = b'%s://%s%s' % (urltype, realhost, rest)
                if proxy_bypass(realhost):
                    host = realhost
                if not host:
                    raise IOError(b'http error', b'no host given')
                if proxy_passwd:
                    proxy_passwd = unquote(proxy_passwd)
                    proxy_auth = base64.b64encode(proxy_passwd.encode()).decode(b'ascii')
                else:
                    proxy_auth = None
                if user_passwd:
                    user_passwd = unquote(user_passwd)
                    auth = base64.b64encode(user_passwd.encode()).decode(b'ascii')
                else:
                    auth = None
                http_conn = connection_factory(host)
                headers = {}
                if proxy_auth:
                    headers[b'Proxy-Authorization'] = b'Basic %s' % proxy_auth
                if auth:
                    headers[b'Authorization'] = b'Basic %s' % auth
                if realhost:
                    headers[b'Host'] = realhost
                headers[b'Connection'] = b'close'
                for header, value in self.addheaders:
                    headers[header] = value

            if data is not None:
                headers[b'Content-Type'] = b'application/x-www-form-urlencoded'
                http_conn.request(b'POST', selector, data, headers)
            else:
                http_conn.request(b'GET', selector, headers=headers)
            try:
                response = http_conn.getresponse()
            except http_client.BadStatusLine:
                raise URLError(b'http protocol error: bad status line')

        if 200 <= response.status < 300:
            return addinfourl(response, response.msg, b'http:' + url, response.status)
        else:
            return self.http_error(url, response.fp, response.status, response.reason, response.msg, data)
            return

    def open_http(self, url, data=None):
        """Use HTTP protocol."""
        return self._open_generic_http(http_client.HTTPConnection, url, data)

    def http_error(self, url, fp, errcode, errmsg, headers, data=None):
        """Handle http errors.

        Derived class can override this, or provide specific handlers
        named http_error_DDD where DDD is the 3-digit error code."""
        name = b'http_error_%d' % errcode
        if hasattr(self, name):
            method = getattr(self, name)
            if data is None:
                result = method(url, fp, errcode, errmsg, headers)
            else:
                result = method(url, fp, errcode, errmsg, headers, data)
            if result:
                return result
        return self.http_error_default(url, fp, errcode, errmsg, headers)

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        """Default error handler: close the connection and raise IOError."""
        fp.close()
        raise HTTPError(url, errcode, errmsg, headers, None)
        return

    if _have_ssl:

        def _https_connection(self, host):
            return http_client.HTTPSConnection(host, key_file=self.key_file, cert_file=self.cert_file)

        def open_https(self, url, data=None):
            """Use HTTPS protocol."""
            return self._open_generic_http(self._https_connection, url, data)

    def open_file(self, url):
        """Use local file or FTP depending on form of URL."""
        if not isinstance(url, str):
            raise URLError(b'file error: proxy support for file protocol currently not implemented')
        if url[:2] == b'//' and url[2:3] != b'/' and url[2:12].lower() != b'localhost/':
            raise ValueError(b'file:// scheme is supported only on localhost')
        else:
            return self.open_local_file(url)

    def open_local_file(self, url):
        """Use local file."""
        import future.backports.email.utils as email_utils, mimetypes
        host, file = splithost(url)
        localname = url2pathname(file)
        try:
            stats = os.stat(localname)
        except OSError as e:
            raise URLError(e.strerror, e.filename)

        size = stats.st_size
        modified = email_utils.formatdate(stats.st_mtime, usegmt=True)
        mtype = mimetypes.guess_type(url)[0]
        headers = email.message_from_string(b'Content-Type: %s\nContent-Length: %d\nLast-modified: %s\n' % (
         mtype or b'text/plain', size, modified))
        if not host:
            urlfile = file
            if file[:1] == b'/':
                urlfile = b'file://' + file
            return addinfourl(open(localname, b'rb'), headers, urlfile)
        host, port = splitport(host)
        if not port and socket.gethostbyname(host) in (localhost(),) + thishost():
            urlfile = file
            if file[:1] == b'/':
                urlfile = b'file://' + file
            elif file[:2] == b'./':
                raise ValueError(b'local file url may start with / or file:. Unknown url of type: %s' % url)
            return addinfourl(open(localname, b'rb'), headers, urlfile)
        raise URLError(b'local file error: not on local host')

    def open_ftp(self, url):
        """Use FTP protocol."""
        if not isinstance(url, str):
            raise URLError(b'ftp error: proxy support for ftp protocol currently not implemented')
        import mimetypes
        host, path = splithost(url)
        if not host:
            raise URLError(b'ftp error: no host given')
        host, port = splitport(host)
        user, host = splituser(host)
        if user:
            user, passwd = splitpasswd(user)
        else:
            passwd = None
        host = unquote(host)
        user = unquote(user or b'')
        passwd = unquote(passwd or b'')
        host = socket.gethostbyname(host)
        if not port:
            import ftplib
            port = ftplib.FTP_PORT
        else:
            port = int(port)
        path, attrs = splitattr(path)
        path = unquote(path)
        dirs = path.split(b'/')
        dirs, file = dirs[:-1], dirs[(-1)]
        if dirs and not dirs[0]:
            dirs = dirs[1:]
        if dirs and not dirs[0]:
            dirs[0] = b'/'
        key = (
         user, host, port, (b'/').join(dirs))
        if len(self.ftpcache) > MAXFTPCACHE:
            for k in self.ftpcache.keys():
                if k != key:
                    v = self.ftpcache[k]
                    del self.ftpcache[k]
                    v.close()

        try:
            if key not in self.ftpcache:
                self.ftpcache[key] = ftpwrapper(user, passwd, host, port, dirs)
            if not file:
                type = b'D'
            else:
                type = b'I'
            for attr in attrs:
                attr, value = splitvalue(attr)
                if attr.lower() == b'type' and value in ('a', 'A', 'i', 'I', 'd', 'D'):
                    type = value.upper()

            fp, retrlen = self.ftpcache[key].retrfile(file, type)
            mtype = mimetypes.guess_type(b'ftp:' + url)[0]
            headers = b''
            if mtype:
                headers += b'Content-Type: %s\n' % mtype
            if retrlen is not None and retrlen >= 0:
                headers += b'Content-Length: %d\n' % retrlen
            headers = email.message_from_string(headers)
            return addinfourl(fp, headers, b'ftp:' + url)
        except ftperrors() as exp:
            raise_with_traceback(URLError(b'ftp error %r' % exp))

        return

    def open_data(self, url, data=None):
        """Use "data" URL."""
        if not isinstance(url, str):
            raise URLError(b'data error: proxy support for data protocol currently not implemented')
        try:
            type, data = url.split(b',', 1)
        except ValueError:
            raise IOError(b'data error', b'bad data URL')

        if not type:
            type = b'text/plain;charset=US-ASCII'
        semi = type.rfind(b';')
        if semi >= 0 and b'=' not in type[semi:]:
            encoding = type[semi + 1:]
            type = type[:semi]
        else:
            encoding = b''
        msg = []
        msg.append(b'Date: %s' % time.strftime(b'%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time())))
        msg.append(b'Content-type: %s' % type)
        if encoding == b'base64':
            data = base64.decodebytes(data.encode(b'ascii')).decode(b'latin-1')
        else:
            data = unquote(data)
        msg.append(b'Content-Length: %d' % len(data))
        msg.append(b'')
        msg.append(data)
        msg = (b'\n').join(msg)
        headers = email.message_from_string(msg)
        f = io.StringIO(msg)
        return addinfourl(f, headers, url)


class FancyURLopener(URLopener):
    """Derived class with handlers for errors we can handle (perhaps)."""

    def __init__(self, *args, **kwargs):
        URLopener.__init__(self, *args, **kwargs)
        self.auth_cache = {}
        self.tries = 0
        self.maxtries = 10

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        """Default error handling -- don't raise an exception."""
        return addinfourl(fp, headers, b'http:' + url, errcode)

    def http_error_302(self, url, fp, errcode, errmsg, headers, data=None):
        """Error 302 -- relocated (temporarily)."""
        self.tries += 1
        if self.maxtries and self.tries >= self.maxtries:
            if hasattr(self, b'http_error_500'):
                meth = self.http_error_500
            else:
                meth = self.http_error_default
            self.tries = 0
            return meth(url, fp, 500, b'Internal Server Error: Redirect Recursion', headers)
        result = self.redirect_internal(url, fp, errcode, errmsg, headers, data)
        self.tries = 0
        return result

    def redirect_internal(self, url, fp, errcode, errmsg, headers, data):
        if b'location' in headers:
            newurl = headers[b'location']
        elif b'uri' in headers:
            newurl = headers[b'uri']
        else:
            return
        fp.close()
        newurl = urljoin(self.type + b':' + url, newurl)
        urlparts = urlparse(newurl)
        if urlparts.scheme not in ('http', 'https', 'ftp', ''):
            raise HTTPError(newurl, errcode, errmsg + b" Redirection to url '%s' is not allowed." % newurl, headers, fp)
        return self.open(newurl)

    def http_error_301(self, url, fp, errcode, errmsg, headers, data=None):
        """Error 301 -- also relocated (permanently)."""
        return self.http_error_302(url, fp, errcode, errmsg, headers, data)

    def http_error_303(self, url, fp, errcode, errmsg, headers, data=None):
        """Error 303 -- also relocated (essentially identical to 302)."""
        return self.http_error_302(url, fp, errcode, errmsg, headers, data)

    def http_error_307(self, url, fp, errcode, errmsg, headers, data=None):
        """Error 307 -- relocated, but turn POST into error."""
        if data is None:
            return self.http_error_302(url, fp, errcode, errmsg, headers, data)
        else:
            return self.http_error_default(url, fp, errcode, errmsg, headers)
            return

    def http_error_401(self, url, fp, errcode, errmsg, headers, data=None, retry=False):
        """Error 401 -- authentication required.
        This function supports Basic authentication only."""
        if b'www-authenticate' not in headers:
            URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
        stuff = headers[b'www-authenticate']
        match = re.match(b'[ \t]*([^ \t]+)[ \t]+realm="([^"]*)"', stuff)
        if not match:
            URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
        scheme, realm = match.groups()
        if scheme.lower() != b'basic':
            URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
        if not retry:
            URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
        name = b'retry_' + self.type + b'_basic_auth'
        if data is None:
            return getattr(self, name)(url, realm)
        else:
            return getattr(self, name)(url, realm, data)
            return

    def http_error_407(self, url, fp, errcode, errmsg, headers, data=None, retry=False):
        """Error 407 -- proxy authentication required.
        This function supports Basic authentication only."""
        if b'proxy-authenticate' not in headers:
            URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
        stuff = headers[b'proxy-authenticate']
        match = re.match(b'[ \t]*([^ \t]+)[ \t]+realm="([^"]*)"', stuff)
        if not match:
            URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
        scheme, realm = match.groups()
        if scheme.lower() != b'basic':
            URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
        if not retry:
            URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
        name = b'retry_proxy_' + self.type + b'_basic_auth'
        if data is None:
            return getattr(self, name)(url, realm)
        else:
            return getattr(self, name)(url, realm, data)
            return

    def retry_proxy_http_basic_auth(self, url, realm, data=None):
        host, selector = splithost(url)
        newurl = b'http://' + host + selector
        proxy = self.proxies[b'http']
        urltype, proxyhost = splittype(proxy)
        proxyhost, proxyselector = splithost(proxyhost)
        i = proxyhost.find(b'@') + 1
        proxyhost = proxyhost[i:]
        user, passwd = self.get_user_passwd(proxyhost, realm, i)
        if not (user or passwd):
            return
        else:
            proxyhost = b'%s:%s@%s' % (quote(user, safe=b''),
             quote(passwd, safe=b''), proxyhost)
            self.proxies[b'http'] = b'http://' + proxyhost + proxyselector
            if data is None:
                return self.open(newurl)
            return self.open(newurl, data)
            return

    def retry_proxy_https_basic_auth(self, url, realm, data=None):
        host, selector = splithost(url)
        newurl = b'https://' + host + selector
        proxy = self.proxies[b'https']
        urltype, proxyhost = splittype(proxy)
        proxyhost, proxyselector = splithost(proxyhost)
        i = proxyhost.find(b'@') + 1
        proxyhost = proxyhost[i:]
        user, passwd = self.get_user_passwd(proxyhost, realm, i)
        if not (user or passwd):
            return
        else:
            proxyhost = b'%s:%s@%s' % (quote(user, safe=b''),
             quote(passwd, safe=b''), proxyhost)
            self.proxies[b'https'] = b'https://' + proxyhost + proxyselector
            if data is None:
                return self.open(newurl)
            return self.open(newurl, data)
            return

    def retry_http_basic_auth(self, url, realm, data=None):
        host, selector = splithost(url)
        i = host.find(b'@') + 1
        host = host[i:]
        user, passwd = self.get_user_passwd(host, realm, i)
        if not (user or passwd):
            return
        else:
            host = b'%s:%s@%s' % (quote(user, safe=b''),
             quote(passwd, safe=b''), host)
            newurl = b'http://' + host + selector
            if data is None:
                return self.open(newurl)
            return self.open(newurl, data)
            return

    def retry_https_basic_auth(self, url, realm, data=None):
        host, selector = splithost(url)
        i = host.find(b'@') + 1
        host = host[i:]
        user, passwd = self.get_user_passwd(host, realm, i)
        if not (user or passwd):
            return
        else:
            host = b'%s:%s@%s' % (quote(user, safe=b''),
             quote(passwd, safe=b''), host)
            newurl = b'https://' + host + selector
            if data is None:
                return self.open(newurl)
            return self.open(newurl, data)
            return

    def get_user_passwd(self, host, realm, clear_cache=0):
        key = realm + b'@' + host.lower()
        if key in self.auth_cache:
            if clear_cache:
                del self.auth_cache[key]
            else:
                return self.auth_cache[key]
        user, passwd = self.prompt_user_passwd(host, realm)
        if user or passwd:
            self.auth_cache[key] = (user, passwd)
        return (
         user, passwd)

    def prompt_user_passwd(self, host, realm):
        """Override this in a GUI environment!"""
        import getpass
        try:
            user = input(b'Enter username for %s at %s: ' % (realm, host))
            passwd = getpass.getpass(b'Enter password for %s in %s at %s: ' % (
             user, realm, host))
            return (user, passwd)
        except KeyboardInterrupt:
            print()
            return (None, None)

        return


_localhost = None

def localhost():
    """Return the IP address of the magic hostname 'localhost'."""
    global _localhost
    if _localhost is None:
        _localhost = socket.gethostbyname(b'localhost')
    return _localhost


_thishost = None

def thishost():
    """Return the IP addresses of the current host."""
    global _thishost
    if _thishost is None:
        try:
            _thishost = tuple(socket.gethostbyname_ex(socket.gethostname())[2])
        except socket.gaierror:
            _thishost = tuple(socket.gethostbyname_ex(b'localhost')[2])

    return _thishost


_ftperrors = None

def ftperrors():
    """Return the set of errors raised by the FTP class."""
    global _ftperrors
    if _ftperrors is None:
        import ftplib
        _ftperrors = ftplib.all_errors
    return _ftperrors


_noheaders = None

def noheaders():
    """Return an empty email Message object."""
    global _noheaders
    if _noheaders is None:
        _noheaders = email.message_from_string(b'')
    return _noheaders


class ftpwrapper(object):
    """Class used by open_ftp() for cache of open FTP connections."""

    def __init__(self, user, passwd, host, port, dirs, timeout=None, persistent=True):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port
        self.dirs = dirs
        self.timeout = timeout
        self.refcount = 0
        self.keepalive = persistent
        self.init()

    def init(self):
        import ftplib
        self.busy = 0
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.host, self.port, self.timeout)
        self.ftp.login(self.user, self.passwd)
        _target = (b'/').join(self.dirs)
        self.ftp.cwd(_target)

    def retrfile(self, file, type):
        import ftplib
        self.endtransfer()
        if type in ('d', 'D'):
            cmd = b'TYPE A'
            isdir = 1
        else:
            cmd = b'TYPE ' + type
            isdir = 0
        try:
            self.ftp.voidcmd(cmd)
        except ftplib.all_errors:
            self.init()
            self.ftp.voidcmd(cmd)

        conn = None
        if file and not isdir:
            try:
                cmd = b'RETR ' + file
                conn, retrlen = self.ftp.ntransfercmd(cmd)
            except ftplib.error_perm as reason:
                if str(reason)[:3] != b'550':
                    raise_with_traceback(URLError(b'ftp error: %r' % reason))

        if not conn:
            self.ftp.voidcmd(b'TYPE A')
            if file:
                pwd = self.ftp.pwd()
                try:
                    try:
                        self.ftp.cwd(file)
                    except ftplib.error_perm as reason:
                        exc = URLError(b'ftp error: %r' % reason)
                        exc.__cause__ = reason
                        raise exc

                finally:
                    self.ftp.cwd(pwd)

                cmd = b'LIST ' + file
            else:
                cmd = b'LIST'
            conn, retrlen = self.ftp.ntransfercmd(cmd)
        self.busy = 1
        ftpobj = addclosehook(conn.makefile(b'rb'), self.file_close)
        self.refcount += 1
        conn.close()
        return (
         ftpobj, retrlen)

    def endtransfer(self):
        self.busy = 0

    def close(self):
        self.keepalive = False
        if self.refcount <= 0:
            self.real_close()

    def file_close(self):
        self.endtransfer()
        self.refcount -= 1
        if self.refcount <= 0 and not self.keepalive:
            self.real_close()

    def real_close(self):
        self.endtransfer()
        try:
            self.ftp.close()
        except ftperrors():
            pass


def getproxies_environment():
    """Return a dictionary of scheme -> proxy server URL mappings.

    Scan the environment for variables named <scheme>_proxy;
    this seems to be the standard convention.  If you need a
    different way, you can pass a proxies dictionary to the
    [Fancy]URLopener constructor.

    """
    proxies = {}
    for name, value in os.environ.items():
        name = name.lower()
        if value and name[-6:] == b'_proxy':
            proxies[name[:-6]] = value

    return proxies


def proxy_bypass_environment(host):
    """Test if proxies should not be used for a particular host.

    Checks the environment for a variable named no_proxy, which should
    be a list of DNS suffixes separated by commas, or '*' for all hosts.
    """
    no_proxy = os.environ.get(b'no_proxy', b'') or os.environ.get(b'NO_PROXY', b'')
    if no_proxy == b'*':
        return 1
    hostonly, port = splitport(host)
    no_proxy_list = [ proxy.strip() for proxy in no_proxy.split(b',') ]
    for name in no_proxy_list:
        if name and (hostonly.endswith(name) or host.endswith(name)):
            return 1

    return 0


def _proxy_bypass_macosx_sysconf(host, proxy_settings):
    """
    Return True iff this host shouldn't be accessed using a proxy

    This function uses the MacOSX framework SystemConfiguration
    to fetch the proxy information.

    proxy_settings come from _scproxy._get_proxy_settings or get mocked ie:
    { 'exclude_simple': bool,
      'exceptions': ['foo.bar', '*.bar.com', '127.0.0.1', '10.1', '10.0/16']
    }
    """
    from fnmatch import fnmatch
    hostonly, port = splitport(host)

    def ip2num(ipAddr):
        parts = ipAddr.split(b'.')
        parts = list(map(int, parts))
        if len(parts) != 4:
            parts = (parts + [0, 0, 0, 0])[:4]
        return parts[0] << 24 | parts[1] << 16 | parts[2] << 8 | parts[3]

    if b'.' not in host:
        if proxy_settings[b'exclude_simple']:
            return True
    hostIP = None
    for value in proxy_settings.get(b'exceptions', ()):
        if not value:
            continue
        m = re.match(b'(\\d+(?:\\.\\d+)*)(/\\d+)?', value)
        if m is not None:
            if hostIP is None:
                try:
                    hostIP = socket.gethostbyname(hostonly)
                    hostIP = ip2num(hostIP)
                except socket.error:
                    continue

            base = ip2num(m.group(1))
            mask = m.group(2)
            if mask is None:
                mask = 8 * (m.group(1).count(b'.') + 1)
            else:
                mask = int(mask[1:])
            mask = 32 - mask
            if hostIP >> mask == base >> mask:
                return True
        elif fnmatch(host, value):
            return True

    return False


if sys.platform == b'darwin':
    from _scproxy import _get_proxy_settings, _get_proxies

    def proxy_bypass_macosx_sysconf(host):
        proxy_settings = _get_proxy_settings()
        return _proxy_bypass_macosx_sysconf(host, proxy_settings)


    def getproxies_macosx_sysconf():
        """Return a dictionary of scheme -> proxy server URL mappings.

        This function uses the MacOSX framework SystemConfiguration
        to fetch the proxy information.
        """
        return _get_proxies()


    def proxy_bypass(host):
        if getproxies_environment():
            return proxy_bypass_environment(host)
        else:
            return proxy_bypass_macosx_sysconf(host)


    def getproxies():
        return getproxies_environment() or getproxies_macosx_sysconf()


elif os.name == b'nt':

    def getproxies_registry():
        """Return a dictionary of scheme -> proxy server URL mappings.

        Win32 uses the registry to store proxies.

        """
        proxies = {}
        try:
            import winreg
        except ImportError:
            return proxies

        try:
            internetSettings = winreg.OpenKey(winreg.HKEY_CURRENT_USER, b'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings')
            proxyEnable = winreg.QueryValueEx(internetSettings, b'ProxyEnable')[0]
            if proxyEnable:
                proxyServer = str(winreg.QueryValueEx(internetSettings, b'ProxyServer')[0])
                if b'=' in proxyServer:
                    for p in proxyServer.split(b';'):
                        protocol, address = p.split(b'=', 1)
                        if not re.match(b'^([^/:]+)://', address):
                            address = b'%s://%s' % (protocol, address)
                        proxies[protocol] = address

                elif proxyServer[:5] == b'http:':
                    proxies[b'http'] = proxyServer
                else:
                    proxies[b'http'] = b'http://%s' % proxyServer
                    proxies[b'https'] = b'https://%s' % proxyServer
                    proxies[b'ftp'] = b'ftp://%s' % proxyServer
            internetSettings.Close()
        except (WindowsError, ValueError, TypeError):
            pass

        return proxies


    def getproxies():
        """Return a dictionary of scheme -> proxy server URL mappings.

        Returns settings gathered from the environment, if specified,
        or the registry.

        """
        return getproxies_environment() or getproxies_registry()


    def proxy_bypass_registry(host):
        try:
            import winreg
        except ImportError:
            return 0

        try:
            internetSettings = winreg.OpenKey(winreg.HKEY_CURRENT_USER, b'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings')
            proxyEnable = winreg.QueryValueEx(internetSettings, b'ProxyEnable')[0]
            proxyOverride = str(winreg.QueryValueEx(internetSettings, b'ProxyOverride')[0])
        except WindowsError:
            return 0

        if not proxyEnable or not proxyOverride:
            return 0
        rawHost, port = splitport(host)
        host = [rawHost]
        try:
            addr = socket.gethostbyname(rawHost)
            if addr != rawHost:
                host.append(addr)
        except socket.error:
            pass

        try:
            fqdn = socket.getfqdn(rawHost)
            if fqdn != rawHost:
                host.append(fqdn)
        except socket.error:
            pass

        proxyOverride = proxyOverride.split(b';')
        for test in proxyOverride:
            if test == b'<local>':
                if b'.' not in rawHost:
                    return 1
            test = test.replace(b'.', b'\\.')
            test = test.replace(b'*', b'.*')
            test = test.replace(b'?', b'.')
            for val in host:
                if re.match(test, val, re.I):
                    return 1

        return 0


    def proxy_bypass(host):
        """Return a dictionary of scheme -> proxy server URL mappings.

        Returns settings gathered from the environment, if specified,
        or the registry.

        """
        if getproxies_environment():
            return proxy_bypass_environment(host)
        else:
            return proxy_bypass_registry(host)


else:
    getproxies = getproxies_environment
    proxy_bypass = proxy_bypass_environment