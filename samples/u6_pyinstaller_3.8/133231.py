# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: urllib\request.py
"""An extensible library for opening URLs using a variety of protocols

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
OSError); for HTTP errors, raises an HTTPError, which can also be
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
import base64, bisect, email, hashlib, http.client, io, os, posixpath, re, socket, string, sys, time, tempfile, contextlib, warnings
from urllib.error import URLError, HTTPError, ContentTooShortError
from urllib.parse import urlparse, urlsplit, urljoin, unwrap, quote, unquote, _splittype, _splithost, _splitport, _splituser, _splitpasswd, _splitattr, _splitquery, _splitvalue, _splittag, _to_bytes, unquote_to_bytes, urlunparse
from urllib.response import addinfourl, addclosehook
try:
    import ssl
except ImportError:
    _have_ssl = False
else:
    _have_ssl = True
__all__ = [
 'Request', 'OpenerDirector', 'BaseHandler', 'HTTPDefaultErrorHandler',
 'HTTPRedirectHandler', 'HTTPCookieProcessor', 'ProxyHandler',
 'HTTPPasswordMgr', 'HTTPPasswordMgrWithDefaultRealm',
 'HTTPPasswordMgrWithPriorAuth', 'AbstractBasicAuthHandler',
 'HTTPBasicAuthHandler', 'ProxyBasicAuthHandler', 'AbstractDigestAuthHandler',
 'HTTPDigestAuthHandler', 'ProxyDigestAuthHandler', 'HTTPHandler',
 'FileHandler', 'FTPHandler', 'CacheFTPHandler', 'DataHandler',
 'UnknownHandler', 'HTTPErrorProcessor',
 'urlopen', 'install_opener', 'build_opener',
 'pathname2url', 'url2pathname', 'getproxies',
 'urlretrieve', 'urlcleanup', 'URLopener', 'FancyURLopener']
__version__ = '%d.%d' % sys.version_info[:2]
_opener = None

def urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, *, cafile=None, capath=None, cadefault=False, context=None):
    """Open the URL url, which can be either a string or a Request object.

    *data* must be an object specifying additional data to be sent to
    the server, or None if no such data is needed.  See Request for
    details.

    urllib.request module uses HTTP/1.1 and includes a "Connection:close"
    header in its HTTP requests.

    The optional *timeout* parameter specifies a timeout in seconds for
    blocking operations like the connection attempt (if not specified, the
    global default timeout setting will be used). This only works for HTTP,
    HTTPS and FTP connections.

    If *context* is specified, it must be a ssl.SSLContext instance describing
    the various SSL options. See HTTPSConnection for more details.

    The optional *cafile* and *capath* parameters specify a set of trusted CA
    certificates for HTTPS requests. cafile should point to a single file
    containing a bundle of CA certificates, whereas capath should point to a
    directory of hashed certificate files. More information can be found in
    ssl.SSLContext.load_verify_locations().

    The *cadefault* parameter is ignored.

    This function always returns an object which can work as a context
    manager and has methods such as

    * geturl() - return the URL of the resource retrieved, commonly used to
      determine if a redirect was followed

    * info() - return the meta-information of the page, such as headers, in the
      form of an email.message_from_string() instance (see Quick Reference to
      HTTP Headers)

    * getcode() - return the HTTP status code of the response.  Raises URLError
      on errors.

    For HTTP and HTTPS URLs, this function returns a http.client.HTTPResponse
    object slightly modified. In addition to the three new methods above, the
    msg attribute contains the same information as the reason attribute ---
    the reason phrase returned by the server --- instead of the response
    headers as it is specified in the documentation for HTTPResponse.

    For FTP, file, and data URLs and requests explicitly handled by legacy
    URLopener and FancyURLopener classes, this function returns a
    urllib.response.addinfourl object.

    Note that None may be returned if no handler handles the request (though
    the default installed global OpenerDirector uses UnknownHandler to ensure
    this never happens).

    In addition, if proxy settings are detected (for example, when a *_proxy
    environment variable like http_proxy is set), ProxyHandler is default
    installed and makes sure the requests are handled through the proxy.

    """
    global _opener
    if not cafile:
        if capath or cadefault:
            import warnings
            warnings.warn('cafile, capath and cadefault are deprecated, use a custom context instead.', DeprecationWarning, 2)
            if context is not None:
                raise ValueError("You can't pass both context and any of cafile, capath, and cadefault")
            if not _have_ssl:
                raise ValueError('SSL support not available')
            context = ssl.create_default_context((ssl.Purpose.SERVER_AUTH), cafile=cafile,
              capath=capath)
            https_handler = HTTPSHandler(context=context)
            opener = build_opener(https_handler)
    elif context:
        https_handler = HTTPSHandler(context=context)
        opener = build_opener(https_handler)
    else:
        if _opener is None:
            _opener = opener = build_opener()
        else:
            opener = _opener
    return opener.open(url, data, timeout)


def install_opener(opener):
    global _opener
    _opener = opener


_url_tempfiles = []

def urlretrieve--- This code section failed: ---

 L. 245         0  LOAD_GLOBAL              _splittype
                2  LOAD_FAST                'url'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'url_type'
               10  STORE_FAST               'path'

 L. 247        12  LOAD_GLOBAL              contextlib
               14  LOAD_METHOD              closing
               16  LOAD_GLOBAL              urlopen
               18  LOAD_FAST                'url'
               20  LOAD_FAST                'data'
               22  CALL_FUNCTION_2       2  ''
               24  CALL_METHOD_1         1  ''
               26  SETUP_WITH          266  'to 266'
               28  STORE_FAST               'fp'

 L. 248        30  LOAD_FAST                'fp'
               32  LOAD_METHOD              info
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'headers'

 L. 252        38  LOAD_FAST                'url_type'
               40  LOAD_STR                 'file'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    78  'to 78'
               46  LOAD_FAST                'filename'
               48  POP_JUMP_IF_TRUE     78  'to 78'

 L. 253        50  LOAD_GLOBAL              os
               52  LOAD_ATTR                path
               54  LOAD_METHOD              normpath
               56  LOAD_FAST                'path'
               58  CALL_METHOD_1         1  ''
               60  LOAD_FAST                'headers'
               62  BUILD_TUPLE_2         2 
               64  POP_BLOCK        
               66  ROT_TWO          
               68  BEGIN_FINALLY    
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  POP_FINALLY           0  ''
               76  RETURN_VALUE     
             78_0  COME_FROM            48  '48'
             78_1  COME_FROM            44  '44'

 L. 256        78  LOAD_FAST                'filename'
               80  POP_JUMP_IF_FALSE    94  'to 94'

 L. 257        82  LOAD_GLOBAL              open
               84  LOAD_FAST                'filename'
               86  LOAD_STR                 'wb'
               88  CALL_FUNCTION_2       2  ''
               90  STORE_FAST               'tfp'
               92  JUMP_FORWARD        122  'to 122'
             94_0  COME_FROM            80  '80'

 L. 259        94  LOAD_GLOBAL              tempfile
               96  LOAD_ATTR                NamedTemporaryFile
               98  LOAD_CONST               False
              100  LOAD_CONST               ('delete',)
              102  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              104  STORE_FAST               'tfp'

 L. 260       106  LOAD_FAST                'tfp'
              108  LOAD_ATTR                name
              110  STORE_FAST               'filename'

 L. 261       112  LOAD_GLOBAL              _url_tempfiles
              114  LOAD_METHOD              append
              116  LOAD_FAST                'filename'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
            122_0  COME_FROM            92  '92'

 L. 263       122  LOAD_FAST                'tfp'
              124  SETUP_WITH          256  'to 256'
              126  POP_TOP          

 L. 264       128  LOAD_FAST                'filename'
              130  LOAD_FAST                'headers'
              132  BUILD_TUPLE_2         2 
              134  STORE_FAST               'result'

 L. 265       136  LOAD_CONST               8192
              138  STORE_FAST               'bs'

 L. 266       140  LOAD_CONST               -1
              142  STORE_FAST               'size'

 L. 267       144  LOAD_CONST               0
              146  STORE_FAST               'read'

 L. 268       148  LOAD_CONST               0
              150  STORE_FAST               'blocknum'

 L. 269       152  LOAD_STR                 'content-length'
              154  LOAD_FAST                'headers'
              156  COMPARE_OP               in
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L. 270       160  LOAD_GLOBAL              int
              162  LOAD_FAST                'headers'
              164  LOAD_STR                 'Content-Length'
              166  BINARY_SUBSCR    
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'size'
            172_0  COME_FROM           158  '158'

 L. 272       172  LOAD_FAST                'reporthook'
              174  POP_JUMP_IF_FALSE   188  'to 188'

 L. 273       176  LOAD_FAST                'reporthook'
              178  LOAD_FAST                'blocknum'
              180  LOAD_FAST                'bs'
              182  LOAD_FAST                'size'
              184  CALL_FUNCTION_3       3  ''
              186  POP_TOP          
            188_0  COME_FROM           236  '236'
            188_1  COME_FROM           174  '174'

 L. 276       188  LOAD_FAST                'fp'
              190  LOAD_METHOD              read
              192  LOAD_FAST                'bs'
              194  CALL_METHOD_1         1  ''
              196  STORE_FAST               'block'

 L. 277       198  LOAD_FAST                'block'
              200  POP_JUMP_IF_TRUE    204  'to 204'

 L. 278       202  BREAK_LOOP          252  'to 252'
            204_0  COME_FROM           200  '200'

 L. 279       204  LOAD_FAST                'read'
              206  LOAD_GLOBAL              len
              208  LOAD_FAST                'block'
              210  CALL_FUNCTION_1       1  ''
              212  INPLACE_ADD      
              214  STORE_FAST               'read'

 L. 280       216  LOAD_FAST                'tfp'
              218  LOAD_METHOD              write
              220  LOAD_FAST                'block'
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L. 281       226  LOAD_FAST                'blocknum'
              228  LOAD_CONST               1
              230  INPLACE_ADD      
              232  STORE_FAST               'blocknum'

 L. 282       234  LOAD_FAST                'reporthook'
              236  POP_JUMP_IF_FALSE   188  'to 188'

 L. 283       238  LOAD_FAST                'reporthook'
              240  LOAD_FAST                'blocknum'
              242  LOAD_FAST                'bs'
              244  LOAD_FAST                'size'
              246  CALL_FUNCTION_3       3  ''
              248  POP_TOP          
              250  JUMP_BACK           188  'to 188'
              252  POP_BLOCK        
              254  BEGIN_FINALLY    
            256_0  COME_FROM_WITH      124  '124'
              256  WITH_CLEANUP_START
              258  WITH_CLEANUP_FINISH
              260  END_FINALLY      
              262  POP_BLOCK        
              264  BEGIN_FINALLY    
            266_0  COME_FROM_WITH       26  '26'
              266  WITH_CLEANUP_START
              268  WITH_CLEANUP_FINISH
              270  END_FINALLY      

 L. 285       272  LOAD_FAST                'size'
              274  LOAD_CONST               0
              276  COMPARE_OP               >=
          278_280  POP_JUMP_IF_FALSE   310  'to 310'
              282  LOAD_FAST                'read'
              284  LOAD_FAST                'size'
              286  COMPARE_OP               <
          288_290  POP_JUMP_IF_FALSE   310  'to 310'

 L. 286       292  LOAD_GLOBAL              ContentTooShortError

 L. 287       294  LOAD_STR                 'retrieval incomplete: got only %i out of %i bytes'

 L. 288       296  LOAD_FAST                'read'
              298  LOAD_FAST                'size'
              300  BUILD_TUPLE_2         2 

 L. 287       302  BINARY_MODULO    

 L. 288       304  LOAD_FAST                'result'

 L. 286       306  CALL_FUNCTION_2       2  ''
              308  RAISE_VARARGS_1       1  'exception instance'
            310_0  COME_FROM           288  '288'
            310_1  COME_FROM           278  '278'

 L. 290       310  LOAD_FAST                'result'
              312  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 66


def urlcleanup():
    """Clean up temporary files from urlretrieve calls."""
    global _opener
    for temp_file in _url_tempfiles:
        try:
            os.unlink(temp_file)
        except OSError:
            pass

    else:
        del _url_tempfiles[:]
        if _opener:
            _opener = None


_cut_port_re = re.compile(':\\d+$', re.ASCII)

def request_host(request):
    """Return request-host, as defined by RFC 2965.

    Variation from RFC: returned value is lowercased, for convenient
    comparison.

    """
    url = request.full_url
    host = urlparse(url)[1]
    if host == '':
        host = request.get_header('Host', '')
    host = _cut_port_re.sub('', host, 1)
    return host.lower


class Request:

    def __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None):
        self.full_url = url
        self.headers = {}
        self.unredirected_hdrs = {}
        self._data = None
        self.data = data
        self._tunnel_host = None
        for key, value in headers.items:
            self.add_header(key, value)
        else:
            if origin_req_host is None:
                origin_req_host = request_host(self)
            self.origin_req_host = origin_req_host
            self.unverifiable = unverifiable
            if method:
                self.method = method

    @property
    def full_url(self):
        if self.fragment:
            return '{}#{}'.format(self._full_url, self.fragment)
        return self._full_url

    @full_url.setter
    def full_url(self, url):
        self._full_url = unwrap(url)
        self._full_url, self.fragment = _splittag(self._full_url)
        self._parse

    @full_url.deleter
    def full_url(self):
        self._full_url = None
        self.fragment = None
        self.selector = ''

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if data != self._data:
            self._data = data
            if self.has_header('Content-length'):
                self.remove_header('Content-length')

    @data.deleter
    def data(self):
        self.data = None

    def _parse(self):
        self.type, rest = _splittype(self._full_url)
        if self.type is None:
            raise ValueError('unknown url type: %r' % self.full_url)
        self.host, self.selector = _splithost(rest)
        if self.host:
            self.host = unquote(self.host)

    def get_method(self):
        """Return a string indicating the HTTP request method."""
        default_method = 'POST' if self.data is not None else 'GET'
        return getattr(self, 'method', default_method)

    def get_full_url(self):
        return self.full_url

    def set_proxy(self, host, type):
        if self.type == 'https':
            self._tunnel_host = self._tunnel_host or self.host
        else:
            self.type = type
            self.selector = self.full_url
        self.host = host

    def has_proxy(self):
        return self.selector == self.full_url

    def add_header(self, key, val):
        self.headers[key.capitalize] = val

    def add_unredirected_header(self, key, val):
        self.unredirected_hdrs[key.capitalize] = val

    def has_header(self, header_name):
        return header_name in self.headers or header_name in self.unredirected_hdrs

    def get_header(self, header_name, default=None):
        return self.headers.get(header_name, self.unredirected_hdrs.get(header_name, default))

    def remove_header(self, header_name):
        self.headers.pop(header_name, None)
        self.unredirected_hdrs.pop(header_name, None)

    def header_items(self):
        hdrs = {**(self.unredirected_hdrs), **(self.headers)}
        return list(hdrs.items)


class OpenerDirector:

    def __init__(self):
        client_version = 'Python-urllib/%s' % __version__
        self.addheaders = [('User-agent', client_version)]
        self.handlers = []
        self.handle_open = {}
        self.handle_error = {}
        self.process_response = {}
        self.process_request = {}

    def add_handler--- This code section failed: ---

 L. 445         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'handler'
                4  LOAD_STR                 'add_parent'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     26  'to 26'

 L. 446        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'expected BaseHandler instance, got %r'

 L. 447        14  LOAD_GLOBAL              type
               16  LOAD_FAST                'handler'
               18  CALL_FUNCTION_1       1  ''

 L. 446        20  BINARY_MODULO    
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 449        26  LOAD_CONST               False
               28  STORE_FAST               'added'

 L. 450        30  LOAD_GLOBAL              dir
               32  LOAD_FAST                'handler'
               34  CALL_FUNCTION_1       1  ''
               36  GET_ITER         
             38_0  COME_FROM           242  '242'
            38_40  FOR_ITER            306  'to 306'
               42  STORE_FAST               'meth'

 L. 451        44  LOAD_FAST                'meth'
               46  LOAD_CONST               ('redirect_request', 'do_open', 'proxy_open')
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE    54  'to 54'

 L. 453        52  JUMP_BACK            38  'to 38'
             54_0  COME_FROM            50  '50'

 L. 455        54  LOAD_FAST                'meth'
               56  LOAD_METHOD              find
               58  LOAD_STR                 '_'
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'i'

 L. 456        64  LOAD_FAST                'meth'
               66  LOAD_CONST               None
               68  LOAD_FAST                'i'
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  STORE_FAST               'protocol'

 L. 457        76  LOAD_FAST                'meth'
               78  LOAD_FAST                'i'
               80  LOAD_CONST               1
               82  BINARY_ADD       
               84  LOAD_CONST               None
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  STORE_FAST               'condition'

 L. 459        92  LOAD_FAST                'condition'
               94  LOAD_METHOD              startswith
               96  LOAD_STR                 'error'
               98  CALL_METHOD_1         1  ''
              100  POP_JUMP_IF_FALSE   196  'to 196'

 L. 460       102  LOAD_FAST                'condition'
              104  LOAD_METHOD              find
              106  LOAD_STR                 '_'
              108  CALL_METHOD_1         1  ''
              110  LOAD_FAST                'i'
              112  BINARY_ADD       
              114  LOAD_CONST               1
              116  BINARY_ADD       
              118  STORE_FAST               'j'

 L. 461       120  LOAD_FAST                'meth'
              122  LOAD_FAST                'j'
              124  LOAD_CONST               1
              126  BINARY_ADD       
              128  LOAD_CONST               None
              130  BUILD_SLICE_2         2 
              132  BINARY_SUBSCR    
              134  STORE_FAST               'kind'

 L. 462       136  SETUP_FINALLY       150  'to 150'

 L. 463       138  LOAD_GLOBAL              int
              140  LOAD_FAST                'kind'
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'kind'
              146  POP_BLOCK        
              148  JUMP_FORWARD        170  'to 170'
            150_0  COME_FROM_FINALLY   136  '136'

 L. 464       150  DUP_TOP          
              152  LOAD_GLOBAL              ValueError
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   168  'to 168'
              158  POP_TOP          
              160  POP_TOP          
              162  POP_TOP          

 L. 465       164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
            168_0  COME_FROM           156  '156'
              168  END_FINALLY      
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           148  '148'

 L. 466       170  LOAD_FAST                'self'
              172  LOAD_ATTR                handle_error
              174  LOAD_METHOD              get
              176  LOAD_FAST                'protocol'
              178  BUILD_MAP_0           0 
              180  CALL_METHOD_2         2  ''
              182  STORE_FAST               'lookup'

 L. 467       184  LOAD_FAST                'lookup'
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                handle_error
              190  LOAD_FAST                'protocol'
              192  STORE_SUBSCR     
              194  JUMP_FORWARD        258  'to 258'
            196_0  COME_FROM           100  '100'

 L. 468       196  LOAD_FAST                'condition'
              198  LOAD_STR                 'open'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   216  'to 216'

 L. 469       204  LOAD_FAST                'protocol'
              206  STORE_FAST               'kind'

 L. 470       208  LOAD_FAST                'self'
              210  LOAD_ATTR                handle_open
              212  STORE_FAST               'lookup'
              214  JUMP_FORWARD        258  'to 258'
            216_0  COME_FROM           202  '202'

 L. 471       216  LOAD_FAST                'condition'
              218  LOAD_STR                 'response'
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   236  'to 236'

 L. 472       224  LOAD_FAST                'protocol'
              226  STORE_FAST               'kind'

 L. 473       228  LOAD_FAST                'self'
              230  LOAD_ATTR                process_response
              232  STORE_FAST               'lookup'
              234  JUMP_FORWARD        258  'to 258'
            236_0  COME_FROM           222  '222'

 L. 474       236  LOAD_FAST                'condition'
              238  LOAD_STR                 'request'
              240  COMPARE_OP               ==
              242  POP_JUMP_IF_FALSE    38  'to 38'

 L. 475       244  LOAD_FAST                'protocol'
              246  STORE_FAST               'kind'

 L. 476       248  LOAD_FAST                'self'
              250  LOAD_ATTR                process_request
              252  STORE_FAST               'lookup'
              254  JUMP_FORWARD        258  'to 258'

 L. 478       256  JUMP_BACK            38  'to 38'
            258_0  COME_FROM           254  '254'
            258_1  COME_FROM           234  '234'
            258_2  COME_FROM           214  '214'
            258_3  COME_FROM           194  '194'

 L. 480       258  LOAD_FAST                'lookup'
              260  LOAD_METHOD              setdefault
              262  LOAD_FAST                'kind'
              264  BUILD_LIST_0          0 
              266  CALL_METHOD_2         2  ''
              268  STORE_FAST               'handlers'

 L. 481       270  LOAD_FAST                'handlers'
          272_274  POP_JUMP_IF_FALSE   290  'to 290'

 L. 482       276  LOAD_GLOBAL              bisect
              278  LOAD_METHOD              insort
              280  LOAD_FAST                'handlers'
              282  LOAD_FAST                'handler'
              284  CALL_METHOD_2         2  ''
              286  POP_TOP          
              288  JUMP_FORWARD        300  'to 300'
            290_0  COME_FROM           272  '272'

 L. 484       290  LOAD_FAST                'handlers'
              292  LOAD_METHOD              append
              294  LOAD_FAST                'handler'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
            300_0  COME_FROM           288  '288'

 L. 485       300  LOAD_CONST               True
              302  STORE_FAST               'added'
              304  JUMP_BACK            38  'to 38'

 L. 487       306  LOAD_FAST                'added'
          308_310  POP_JUMP_IF_FALSE   336  'to 336'

 L. 488       312  LOAD_GLOBAL              bisect
              314  LOAD_METHOD              insort
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                handlers
              320  LOAD_FAST                'handler'
              322  CALL_METHOD_2         2  ''
              324  POP_TOP          

 L. 489       326  LOAD_FAST                'handler'
              328  LOAD_METHOD              add_parent
              330  LOAD_FAST                'self'
              332  CALL_METHOD_1         1  ''
              334  POP_TOP          
            336_0  COME_FROM           308  '308'

Parse error at or near `LOAD_FAST' instruction at offset 306

    def close(self):
        pass

    def _call_chain(self, chain, kind, meth_name, *args):
        handlers = chain.get(kind, ())
        for handler in handlers:
            func = getattr(handler, meth_name)
            result = func(*args)
            if result is not None:
                return result

    def open(self, fullurl, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        if isinstance(fullurl, str):
            req = Request(fullurl, data)
        else:
            req = fullurl
            if data is not None:
                req.data = data
        req.timeout = timeout
        protocol = req.type
        meth_name = protocol + '_request'
        for processor in self.process_request.get(protocol, []):
            meth = getattr(processor, meth_name)
            req = meth(req)
        else:
            sys.audit('urllib.Request', req.full_url, req.data, req.headers, req.get_method)
            response = self._open(req, data)
            meth_name = protocol + '_response'
            for processor in self.process_response.get(protocol, []):
                meth = getattr(processor, meth_name)
                response = meth(req, response)
            else:
                return response

    def _open(self, req, data=None):
        result = self._call_chain(self.handle_open, 'default', 'default_open', req)
        if result:
            return result
        protocol = req.type
        result = self._call_chain(self.handle_open, protocol, protocol + '_open', req)
        if result:
            return result
        return self._call_chain(self.handle_open, 'unknown', 'unknown_open', req)

    def error(self, proto, *args):
        if proto in ('http', 'https'):
            dict = self.handle_error['http']
            proto = args[2]
            meth_name = 'http_error_%s' % proto
            http_err = 1
            orig_args = args
        else:
            dict = self.handle_error
            meth_name = proto + '_error'
            http_err = 0
        args = (
         dict, proto, meth_name) + args
        result = (self._call_chain)(*args)
        if result:
            return result
        if http_err:
            args = (
             dict, 'default', 'http_error_default') + orig_args
            return (self._call_chain)(*args)


def build_opener(*handlers):
    """Create an opener object from a list of handlers.

    The opener will use several default handlers, including support
    for HTTP, FTP and when applicable HTTPS.

    If any of the handlers passed as arguments are subclasses of the
    default handlers, the default handlers will not be used.
    """
    opener = OpenerDirector()
    default_classes = [ProxyHandler, UnknownHandler, HTTPHandler,
     HTTPDefaultErrorHandler, HTTPRedirectHandler,
     FTPHandler, FileHandler, HTTPErrorProcessor,
     DataHandler]
    if hasattr(http.client, 'HTTPSConnection'):
        default_classes.append(HTTPSHandler)
    skip = set()
    for klass in default_classes:
        for check in handlers:
            if isinstance(check, type):
                if issubclass(check, klass):
                    skip.add(klass)
            elif isinstance(check, klass):
                skip.add(klass)

    for klass in skip:
        default_classes.remove(klass)
    else:
        for klass in default_classes:
            opener.add_handler(klass())
        else:
            for h in handlers:
                if isinstance(h, type):
                    h = h()
                opener.add_handler(h)
            else:
                return opener


class BaseHandler:
    handler_order = 500

    def add_parent(self, parent):
        self.parent = parent

    def close(self):
        pass

    def __lt__(self, other):
        if not hasattr(other, 'handler_order'):
            return True
        return self.handler_order < other.handler_order


class HTTPErrorProcessor(BaseHandler):
    __doc__ = 'Process HTTP error responses.'
    handler_order = 1000

    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info
        if not 200 <= code < 300:
            response = self.parent.error('http', request, response, code, msg, hdrs)
        return response

    https_response = http_response


class HTTPDefaultErrorHandler(BaseHandler):

    def http_error_default(self, req, fp, code, msg, hdrs):
        raise HTTPError(req.full_url, code, msg, hdrs, fp)


class HTTPRedirectHandler(BaseHandler):
    max_repeats = 4
    max_redirections = 10

    def redirect_request--- This code section failed: ---

 L. 669         0  LOAD_FAST                'req'
                2  LOAD_METHOD              get_method
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'm'

 L. 670         8  LOAD_FAST                'code'
               10  LOAD_CONST               (301, 302, 303, 307)
               12  COMPARE_OP               in
               14  POP_JUMP_IF_FALSE    24  'to 24'
               16  LOAD_FAST                'm'
               18  LOAD_CONST               ('GET', 'HEAD')
               20  COMPARE_OP               in
               22  POP_JUMP_IF_TRUE     58  'to 58'
             24_0  COME_FROM            14  '14'

 L. 671        24  LOAD_FAST                'code'
               26  LOAD_CONST               (301, 302, 303)
               28  COMPARE_OP               in

 L. 670        30  POP_JUMP_IF_FALSE    40  'to 40'

 L. 671        32  LOAD_FAST                'm'
               34  LOAD_STR                 'POST'
               36  COMPARE_OP               ==

 L. 670        38  POP_JUMP_IF_TRUE     58  'to 58'
             40_0  COME_FROM            30  '30'

 L. 672        40  LOAD_GLOBAL              HTTPError
               42  LOAD_FAST                'req'
               44  LOAD_ATTR                full_url
               46  LOAD_FAST                'code'
               48  LOAD_FAST                'msg'
               50  LOAD_FAST                'headers'
               52  LOAD_FAST                'fp'
               54  CALL_FUNCTION_5       5  ''
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            38  '38'
             58_1  COME_FROM            22  '22'

 L. 683        58  LOAD_FAST                'newurl'
               60  LOAD_METHOD              replace
               62  LOAD_STR                 ' '
               64  LOAD_STR                 '%20'
               66  CALL_METHOD_2         2  ''
               68  STORE_FAST               'newurl'

 L. 685        70  LOAD_CONST               ('content-length', 'content-type')
               72  STORE_DEREF              'CONTENT_HEADERS'

 L. 686        74  LOAD_CLOSURE             'CONTENT_HEADERS'
               76  BUILD_TUPLE_1         1 
               78  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               80  LOAD_STR                 'HTTPRedirectHandler.redirect_request.<locals>.<dictcomp>'
               82  MAKE_FUNCTION_8          'closure'
               84  LOAD_FAST                'req'
               86  LOAD_ATTR                headers
               88  LOAD_METHOD              items
               90  CALL_METHOD_0         0  ''
               92  GET_ITER         
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'newheaders'

 L. 688        98  LOAD_GLOBAL              Request
              100  LOAD_FAST                'newurl'

 L. 689       102  LOAD_FAST                'newheaders'

 L. 690       104  LOAD_FAST                'req'
              106  LOAD_ATTR                origin_req_host

 L. 691       108  LOAD_CONST               True

 L. 688       110  LOAD_CONST               ('headers', 'origin_req_host', 'unverifiable')
              112  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 78

    def http_error_302(self, req, fp, code, msg, headers):
        if 'location' in headers:
            newurl = headers['location']
        else:
            if 'uri' in headers:
                newurl = headers['uri']
            else:
                return
        urlparts = urlparse(newurl)
        if urlparts.scheme not in ('http', 'https', 'ftp', ''):
            raise HTTPError(newurl, code, "%s - Redirection to url '%s' is not allowed" % (msg, newurl), headers, fp)
        elif not urlparts.path:
            if urlparts.netloc:
                urlparts = list(urlparts)
                urlparts[2] = '/'
        else:
            newurl = urlunparse(urlparts)
            newurl = quote(newurl,
              encoding='iso-8859-1', safe=(string.punctuation))
            newurl = urljoin(req.full_url, newurl)
            new = self.redirect_request(req, fp, code, msg, headers, newurl)
            if new is None:
                return
                if hasattr(req, 'redirect_dict'):
                    visited = new.redirect_dict = req.redirect_dict
                    if visited.get(newurl, 0) >= self.max_repeats or len(visited) >= self.max_redirections:
                        raise HTTPError(req.full_url, code, self.inf_msg + msg, headers, fp)
            else:
                visited = new.redirect_dict = req.redirect_dict = {}
        visited[newurl] = visited.get(newurl, 0) + 1
        fp.read
        fp.close
        return self.parent.open(new, timeout=(req.timeout))

    http_error_301 = http_error_303 = http_error_307 = http_error_302
    inf_msg = 'The HTTP server returned a redirect error that would lead to an infinite loop.\nThe last 30x error message was:\n'


def _parse_proxy(proxy):
    """Return (scheme, user, password, host/port) given a URL or an authority.

    If a URL is supplied, it must have an authority (host:port) component.
    According to RFC 3986, having an authority component means the URL must
    have two slashes after the scheme.
    """
    scheme, r_scheme = _splittype(proxy)
    if not r_scheme.startswith('/'):
        scheme = None
        authority = proxy
    else:
        if not r_scheme.startswith('//'):
            raise ValueError('proxy URL with no authority: %r' % proxy)
        end = r_scheme.find('/', 2)
        if end == -1:
            end = None
        authority = r_scheme[2:end]
    userinfo, hostport = _splituser(authority)
    if userinfo is not None:
        user, password = _splitpasswd(userinfo)
    else:
        user = password = None
    return (
     scheme, user, password, hostport)


class ProxyHandler(BaseHandler):
    handler_order = 100

    def __init__(self, proxies=None):
        if proxies is None:
            proxies = getproxies()
        assert hasattr(proxies, 'keys'), 'proxies must be a mapping'
        self.proxies = proxies
        for type, url in proxies.items:
            type = type.lower
            setattr(self, '%s_open' % type, lambda r, proxy=url, type=type, meth=self.proxy_open: meth(r, proxy, type))

    def proxy_open(self, req, proxy, type):
        orig_type = req.type
        proxy_type, user, password, hostport = _parse_proxy(proxy)
        if proxy_type is None:
            proxy_type = orig_type
        if req.host:
            if proxy_bypass(req.host):
                return
        if user:
            if password:
                user_pass = '%s:%s' % (unquote(user),
                 unquote(password))
                creds = base64.b64encode(user_pass.encode).decode('ascii')
                req.add_header('Proxy-authorization', 'Basic ' + creds)
        hostport = unquote(hostport)
        req.set_proxy(hostport, proxy_type)
        if orig_type == proxy_type or orig_type == 'https':
            return
        return self.parent.open(req, timeout=(req.timeout))


class HTTPPasswordMgr:

    def __init__(self):
        self.passwd = {}

    def add_password(self, realm, uri, user, passwd):
        if isinstance(uri, str):
            uri = [
             uri]
        if realm not in self.passwd:
            self.passwd[realm] = {}
        for default_port in (True, False):
            reduced_uri = tuple((self.reduce_uri(u, default_port) for u in uri))
            self.passwd[realm][reduced_uri] = (user, passwd)

    def find_user_password(self, realm, authuri):
        domains = self.passwd.get(realm, {})
        for default_port in (True, False):
            reduced_authuri = self.reduce_uri(authuri, default_port)
            for uris, authinfo in domains.items:
                for uri in uris:
                    if self.is_suburi(uri, reduced_authuri):
                        return authinfo
                else:
                    return (None, None)

    def reduce_uri(self, uri, default_port=True):
        """Accept authority or URI and extract only the authority and path."""
        parts = urlsplit(uri)
        if parts[1]:
            scheme = parts[0]
            authority = parts[1]
            path = parts[2] or '/'
        else:
            scheme = None
            authority = uri
            path = '/'
        host, port = _splitport(authority)
        if default_port:
            if port is None:
                if scheme is not None:
                    dport = {'http':80, 
                     'https':443}.get(scheme)
                    if dport is not None:
                        authority = '%s:%d' % (host, dport)
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
            return (
             user, password)
        return HTTPPasswordMgr.find_user_password(self, None, authuri)


class HTTPPasswordMgrWithPriorAuth(HTTPPasswordMgrWithDefaultRealm):

    def __init__(self, *args, **kwargs):
        self.authenticated = {}
        (super().__init__)(*args, **kwargs)

    def add_password(self, realm, uri, user, passwd, is_authenticated=False):
        self.update_authenticated(uri, is_authenticated)
        if realm is not None:
            super().add_password(None, uri, user, passwd)
        super().add_password(realm, uri, user, passwd)

    def update_authenticated(self, uri, is_authenticated=False):
        if isinstance(uri, str):
            uri = [
             uri]
        for default_port in (True, False):
            for u in uri:
                reduced_uri = self.reduce_uri(u, default_port)
                self.authenticated[reduced_uri] = is_authenticated

    def is_authenticated(self, authuri):
        for default_port in (True, False):
            reduced_authuri = self.reduce_uri(authuri, default_port)
            for uri in self.authenticated:
                if self.is_suburi(uri, reduced_authuri):
                    return self.authenticated[uri]


class AbstractBasicAuthHandler:
    rx = re.compile('(?:^|,)[ \t]*([^ \t]+)[ \t]+realm=(["\']?)([^"\']*)\\2', re.I)

    def __init__(self, password_mgr=None):
        if password_mgr is None:
            password_mgr = HTTPPasswordMgr()
        self.passwd = password_mgr
        self.add_password = self.passwd.add_password

    def _parse_realm(self, header):
        found_challenge = False
        for mo in AbstractBasicAuthHandler.rx.finditer(header):
            scheme, quote, realm = mo.groups
            if quote not in ('"', "'"):
                warnings.warn('Basic Auth Realm was unquoted', UserWarning, 3)
            (yield (scheme, realm))
            found_challenge = True
        else:
            if not found_challenge:
                if header:
                    scheme = header.split[0]
                else:
                    scheme = ''
                (yield (
                 scheme, None))

    def http_error_auth_reqed(self, authreq, host, req, headers):
        headers = headers.get_all(authreq)
        if not headers:
            return
        unsupported = None
        for header in headers:
            for scheme, realm in self._parse_realm(header):
                if scheme.lower != 'basic':
                    unsupported = scheme
                elif realm is not None:
                    return self.retry_http_basic_auth(host, req, realm)
            else:
                if unsupported is not None:
                    raise ValueError('AbstractBasicAuthHandler does not support the following scheme: %r' % (
                     scheme,))

    def retry_http_basic_auth(self, host, req, realm):
        user, pw = self.passwd.find_user_password(realm, host)
        if pw is not None:
            raw = '%s:%s' % (user, pw)
            auth = 'Basic ' + base64.b64encode(raw.encode).decode('ascii')
            if req.get_header(self.auth_header, None) == auth:
                return
            req.add_unredirected_header(self.auth_header, auth)
            return self.parent.open(req, timeout=(req.timeout))
        return

    def http_request(self, req):
        return hasattr(self.passwd, 'is_authenticated') and self.passwd.is_authenticated(req.full_url) or req
        if not req.has_header('Authorization'):
            user, passwd = self.passwd.find_user_password(None, req.full_url)
            credentials = '{0}:{1}'.format(user, passwd).encode
            auth_str = base64.standard_b64encode(credentials).decode
            req.add_unredirected_header('Authorization', 'Basic {}'.format(auth_str.strip))
        return req

    def http_response(self, req, response):
        if hasattr(self.passwd, 'is_authenticated'):
            if 200 <= response.code < 300:
                self.passwd.update_authenticated(req.full_url, True)
            else:
                self.passwd.update_authenticated(req.full_url, False)
        return response

    https_request = http_request
    https_response = http_response


class HTTPBasicAuthHandler(AbstractBasicAuthHandler, BaseHandler):
    auth_header = 'Authorization'

    def http_error_401(self, req, fp, code, msg, headers):
        url = req.full_url
        response = self.http_error_auth_reqed('www-authenticate', url, req, headers)
        return response


class ProxyBasicAuthHandler(AbstractBasicAuthHandler, BaseHandler):
    auth_header = 'Proxy-authorization'

    def http_error_407(self, req, fp, code, msg, headers):
        authority = req.host
        response = self.http_error_auth_reqed('proxy-authenticate', authority, req, headers)
        return response


_randombytes = os.urandom

class AbstractDigestAuthHandler:

    def __init__(self, passwd=None):
        if passwd is None:
            passwd = HTTPPasswordMgr()
        self.passwd = passwd
        self.add_password = self.passwd.add_password
        self.retried = 0
        self.nonce_count = 0
        self.last_nonce = None

    def reset_retry_count(self):
        self.retried = 0

    def http_error_auth_reqed(self, auth_header, host, req, headers):
        authreq = headers.get(auth_header, None)
        if self.retried > 5:
            raise HTTPError(req.full_url, 401, 'digest auth failed', headers, None)
        else:
            self.retried += 1
        if authreq:
            scheme = authreq.split[0]
            if scheme.lower == 'digest':
                return self.retry_http_digest_auth(req, authreq)
            if scheme.lower != 'basic':
                raise ValueError("AbstractDigestAuthHandler does not support the following scheme: '%s'" % scheme)

    def retry_http_digest_auth(self, req, auth):
        token, challenge = auth.split(' ', 1)
        chal = parse_keqv_list(filter(None, parse_http_list(challenge)))
        auth = self.get_authorization(req, chal)
        if auth:
            auth_val = 'Digest %s' % auth
            if req.headers.get(self.auth_header, None) == auth_val:
                return
            req.add_unredirected_header(self.auth_header, auth_val)
            resp = self.parent.open(req, timeout=(req.timeout))
            return resp

    def get_cnonce(self, nonce):
        s = '%s:%s:%s:' % (self.nonce_count, nonce, time.ctime)
        b = s.encode('ascii') + _randombytes(8)
        dig = hashlib.sha1(b).hexdigest
        return dig[:16]

    def get_authorization(self, req, chal):
        try:
            realm = chal['realm']
            nonce = chal['nonce']
            qop = chal.get('qop')
            algorithm = chal.get('algorithm', 'MD5')
            opaque = chal.get('opaque', None)
        except KeyError:
            return
        else:
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
                    A1 = '%s:%s:%s' % (user, realm, pw)
                    A2 = '%s:%s' % (req.get_method,
                     req.selector)
                    if qop is None:
                        respdig = KD(H(A1), '%s:%s' % (nonce, H(A2)))
                elif 'auth' in qop.split(','):
                    if nonce == self.last_nonce:
                        self.nonce_count += 1
                    else:
                        self.nonce_count = 1
                        self.last_nonce = nonce
                    ncvalue = '%08x' % self.nonce_count
                    cnonce = self.get_cnonce(nonce)
                    noncebit = '%s:%s:%s:%s:%s' % (nonce, ncvalue, cnonce, 'auth', H(A2))
                    respdig = KD(H(A1), noncebit)
                else:
                    raise URLError("qop '%s' is not supported." % qop)
            base = 'username="%s", realm="%s", nonce="%s", uri="%s", response="%s"' % (
             user, realm, nonce, req.selector,
             respdig)
            if opaque:
                base += ', opaque="%s"' % opaque
            if entdig:
                base += ', digest="%s"' % entdig
            base += ', algorithm="%s"' % algorithm
            if qop:
                base += ', qop=auth, nc=%s, cnonce="%s"' % (ncvalue, cnonce)
            return base

    def get_algorithm_impls(self, algorithm):
        if algorithm == 'MD5':
            H = lambda x: hashlib.md5(x.encode('ascii')).hexdigest
        else:
            if algorithm == 'SHA':
                H = lambda x: hashlib.sha1(x.encode('ascii')).hexdigest
            else:
                raise ValueError('Unsupported digest authentication algorithm %r' % algorithm)
        KD = lambda s, d: H('%s:%s' % (s, d))
        return (H, KD)

    def get_entity_digest(self, data, chal):
        pass


class HTTPDigestAuthHandler(BaseHandler, AbstractDigestAuthHandler):
    __doc__ = 'An authentication protocol defined by RFC 2069\n\n    Digest authentication improves on basic authentication because it\n    does not transmit passwords in the clear.\n    '
    auth_header = 'Authorization'
    handler_order = 490

    def http_error_401(self, req, fp, code, msg, headers):
        host = urlparse(req.full_url)[1]
        retry = self.http_error_auth_reqed('www-authenticate', host, req, headers)
        self.reset_retry_count
        return retry


class ProxyDigestAuthHandler(BaseHandler, AbstractDigestAuthHandler):
    auth_header = 'Proxy-Authorization'
    handler_order = 490

    def http_error_407(self, req, fp, code, msg, headers):
        host = req.host
        retry = self.http_error_auth_reqed('proxy-authenticate', host, req, headers)
        self.reset_retry_count
        return retry


class AbstractHTTPHandler(BaseHandler):

    def __init__(self, debuglevel=0):
        self._debuglevel = debuglevel

    def set_http_debuglevel(self, level):
        self._debuglevel = level

    def _get_content_length(self, request):
        return http.client.HTTPConnection._get_content_length(request.data, request.get_method)

    def do_request_(self, request):
        host = request.host
        if not host:
            raise URLError('no host given')
        elif request.data is not None:
            data = request.data
            if isinstance(data, str):
                msg = 'POST data should be bytes, an iterable of bytes, or a file object. It cannot be of type str.'
                raise TypeError(msg)
            if not request.has_header('Content-type'):
                request.add_unredirected_header('Content-type', 'application/x-www-form-urlencoded')
            if not request.has_header('Content-length'):
                if not request.has_header('Transfer-encoding'):
                    content_length = self._get_content_length(request)
                    if content_length is not None:
                        request.add_unredirected_header('Content-length', str(content_length))
                    else:
                        request.add_unredirected_header('Transfer-encoding', 'chunked')
        sel_host = host
        if request.has_proxy:
            scheme, sel = _splittype(request.selector)
            sel_host, sel_path = _splithost(sel)
        if not request.has_header('Host'):
            request.add_unredirected_header('Host', sel_host)
        for name, value in self.parent.addheaders:
            name = name.capitalize
            if not request.has_header(name):
                request.add_unredirected_header(name, value)
            return request

    def do_open--- This code section failed: ---

 L.1314         0  LOAD_FAST                'req'
                2  LOAD_ATTR                host
                4  STORE_FAST               'host'

 L.1315         6  LOAD_FAST                'host'
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L.1316        10  LOAD_GLOBAL              URLError
               12  LOAD_STR                 'no host given'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.1319        18  LOAD_FAST                'http_class'
               20  LOAD_FAST                'host'
               22  BUILD_TUPLE_1         1 
               24  LOAD_STR                 'timeout'
               26  LOAD_FAST                'req'
               28  LOAD_ATTR                timeout
               30  BUILD_MAP_1           1 
               32  LOAD_FAST                'http_conn_args'
               34  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               36  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               38  STORE_FAST               'h'

 L.1320        40  LOAD_FAST                'h'
               42  LOAD_METHOD              set_debuglevel
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _debuglevel
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L.1322        52  LOAD_GLOBAL              dict
               54  LOAD_FAST                'req'
               56  LOAD_ATTR                unredirected_hdrs
               58  CALL_FUNCTION_1       1  ''
               60  STORE_DEREF              'headers'

 L.1323        62  LOAD_DEREF               'headers'
               64  LOAD_METHOD              update
               66  LOAD_CLOSURE             'headers'
               68  BUILD_TUPLE_1         1 
               70  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               72  LOAD_STR                 'AbstractHTTPHandler.do_open.<locals>.<dictcomp>'
               74  MAKE_FUNCTION_8          'closure'
               76  LOAD_FAST                'req'
               78  LOAD_ATTR                headers
               80  LOAD_METHOD              items
               82  CALL_METHOD_0         0  ''
               84  GET_ITER         
               86  CALL_FUNCTION_1       1  ''
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L.1335        92  LOAD_STR                 'close'
               94  LOAD_DEREF               'headers'
               96  LOAD_STR                 'Connection'
               98  STORE_SUBSCR     

 L.1336       100  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              102  LOAD_STR                 'AbstractHTTPHandler.do_open.<locals>.<dictcomp>'
              104  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              106  LOAD_DEREF               'headers'
              108  LOAD_METHOD              items
              110  CALL_METHOD_0         0  ''
              112  GET_ITER         
              114  CALL_FUNCTION_1       1  ''
              116  STORE_DEREF              'headers'

 L.1338       118  LOAD_FAST                'req'
              120  LOAD_ATTR                _tunnel_host
              122  POP_JUMP_IF_FALSE   174  'to 174'

 L.1339       124  BUILD_MAP_0           0 
              126  STORE_FAST               'tunnel_headers'

 L.1340       128  LOAD_STR                 'Proxy-Authorization'
              130  STORE_FAST               'proxy_auth_hdr'

 L.1341       132  LOAD_FAST                'proxy_auth_hdr'
              134  LOAD_DEREF               'headers'
              136  COMPARE_OP               in
              138  POP_JUMP_IF_FALSE   158  'to 158'

 L.1342       140  LOAD_DEREF               'headers'
              142  LOAD_FAST                'proxy_auth_hdr'
              144  BINARY_SUBSCR    
              146  LOAD_FAST                'tunnel_headers'
              148  LOAD_FAST                'proxy_auth_hdr'
              150  STORE_SUBSCR     

 L.1345       152  LOAD_DEREF               'headers'
              154  LOAD_FAST                'proxy_auth_hdr'
              156  DELETE_SUBSCR    
            158_0  COME_FROM           138  '138'

 L.1346       158  LOAD_FAST                'h'
              160  LOAD_ATTR                set_tunnel
              162  LOAD_FAST                'req'
              164  LOAD_ATTR                _tunnel_host
              166  LOAD_FAST                'tunnel_headers'
              168  LOAD_CONST               ('headers',)
              170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              172  POP_TOP          
            174_0  COME_FROM           122  '122'

 L.1348       174  SETUP_FINALLY       272  'to 272'

 L.1349       176  SETUP_FINALLY       216  'to 216'

 L.1350       178  LOAD_FAST                'h'
              180  LOAD_ATTR                request
              182  LOAD_FAST                'req'
              184  LOAD_METHOD              get_method
              186  CALL_METHOD_0         0  ''
              188  LOAD_FAST                'req'
              190  LOAD_ATTR                selector
              192  LOAD_FAST                'req'
              194  LOAD_ATTR                data
              196  LOAD_DEREF               'headers'

 L.1351       198  LOAD_FAST                'req'
              200  LOAD_METHOD              has_header
              202  LOAD_STR                 'Transfer-encoding'
              204  CALL_METHOD_1         1  ''

 L.1350       206  LOAD_CONST               ('encode_chunked',)
              208  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              210  POP_TOP          
              212  POP_BLOCK        
              214  JUMP_FORWARD        260  'to 260'
            216_0  COME_FROM_FINALLY   176  '176'

 L.1352       216  DUP_TOP          
              218  LOAD_GLOBAL              OSError
              220  COMPARE_OP               exception-match
          222_224  POP_JUMP_IF_FALSE   258  'to 258'
              226  POP_TOP          
              228  STORE_FAST               'err'
              230  POP_TOP          
              232  SETUP_FINALLY       246  'to 246'

 L.1353       234  LOAD_GLOBAL              URLError
              236  LOAD_FAST                'err'
              238  CALL_FUNCTION_1       1  ''
              240  RAISE_VARARGS_1       1  'exception instance'
              242  POP_BLOCK        
              244  BEGIN_FINALLY    
            246_0  COME_FROM_FINALLY   232  '232'
              246  LOAD_CONST               None
              248  STORE_FAST               'err'
              250  DELETE_FAST              'err'
              252  END_FINALLY      
              254  POP_EXCEPT       
              256  JUMP_FORWARD        260  'to 260'
            258_0  COME_FROM           222  '222'
              258  END_FINALLY      
            260_0  COME_FROM           256  '256'
            260_1  COME_FROM           214  '214'

 L.1354       260  LOAD_FAST                'h'
              262  LOAD_METHOD              getresponse
              264  CALL_METHOD_0         0  ''
              266  STORE_FAST               'r'
              268  POP_BLOCK        
              270  JUMP_FORWARD        294  'to 294'
            272_0  COME_FROM_FINALLY   174  '174'

 L.1355       272  POP_TOP          
              274  POP_TOP          
              276  POP_TOP          

 L.1356       278  LOAD_FAST                'h'
              280  LOAD_METHOD              close
              282  CALL_METHOD_0         0  ''
              284  POP_TOP          

 L.1357       286  RAISE_VARARGS_0       0  'reraise'
              288  POP_EXCEPT       
              290  JUMP_FORWARD        294  'to 294'
              292  END_FINALLY      
            294_0  COME_FROM           290  '290'
            294_1  COME_FROM           270  '270'

 L.1362       294  LOAD_FAST                'h'
              296  LOAD_ATTR                sock
          298_300  POP_JUMP_IF_FALSE   318  'to 318'

 L.1363       302  LOAD_FAST                'h'
              304  LOAD_ATTR                sock
              306  LOAD_METHOD              close
              308  CALL_METHOD_0         0  ''
              310  POP_TOP          

 L.1364       312  LOAD_CONST               None
              314  LOAD_FAST                'h'
              316  STORE_ATTR               sock
            318_0  COME_FROM           298  '298'

 L.1366       318  LOAD_FAST                'req'
              320  LOAD_METHOD              get_full_url
              322  CALL_METHOD_0         0  ''
              324  LOAD_FAST                'r'
              326  STORE_ATTR               url

 L.1372       328  LOAD_FAST                'r'
              330  LOAD_ATTR                reason
              332  LOAD_FAST                'r'
              334  STORE_ATTR               msg

 L.1373       336  LOAD_FAST                'r'
              338  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 70


class HTTPHandler(AbstractHTTPHandler):

    def http_open(self, req):
        return self.do_open(http.client.HTTPConnection, req)

    http_request = AbstractHTTPHandler.do_request_


if hasattr(http.client, 'HTTPSConnection'):

    class HTTPSHandler(AbstractHTTPHandler):

        def __init__(self, debuglevel=0, context=None, check_hostname=None):
            AbstractHTTPHandler.__init__(self, debuglevel)
            self._context = context
            self._check_hostname = check_hostname

        def https_open(self, req):
            return self.do_open((http.client.HTTPSConnection), req, context=(self._context),
              check_hostname=(self._check_hostname))

        https_request = AbstractHTTPHandler.do_request_


    __all__.append('HTTPSHandler')
else:

    class HTTPCookieProcessor(BaseHandler):

        def __init__(self, cookiejar=None):
            import http.cookiejar
            if cookiejar is None:
                cookiejar = http.cookiejar.CookieJar
            self.cookiejar = cookiejar

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
            raise URLError('unknown url type: %s' % type)


    def parse_keqv_list(l):
        """Parse list of key=value strings where keys are not duplicated."""
        parsed = {}
        for elt in l:
            k, v = elt.split('=', 1)
            if v[0] == '"':
                if v[(-1)] == '"':
                    v = v[1:-1]
            parsed[k] = v
        else:
            return parsed


    def parse_http_list--- This code section failed: ---

 L.1442         0  BUILD_LIST_0          0 
                2  STORE_FAST               'res'

 L.1443         4  LOAD_STR                 ''
                6  STORE_FAST               'part'

 L.1445         8  LOAD_CONST               False
               10  DUP_TOP          
               12  STORE_FAST               'escape'
               14  STORE_FAST               'quote'

 L.1446        16  LOAD_FAST                's'
               18  GET_ITER         
               20  FOR_ITER            130  'to 130'
               22  STORE_FAST               'cur'

 L.1447        24  LOAD_FAST                'escape'
               26  POP_JUMP_IF_FALSE    42  'to 42'

 L.1448        28  LOAD_FAST                'part'
               30  LOAD_FAST                'cur'
               32  INPLACE_ADD      
               34  STORE_FAST               'part'

 L.1449        36  LOAD_CONST               False
               38  STORE_FAST               'escape'

 L.1450        40  JUMP_BACK            20  'to 20'
             42_0  COME_FROM            26  '26'

 L.1451        42  LOAD_FAST                'quote'
               44  POP_JUMP_IF_FALSE    84  'to 84'

 L.1452        46  LOAD_FAST                'cur'
               48  LOAD_STR                 '\\'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L.1453        54  LOAD_CONST               True
               56  STORE_FAST               'escape'

 L.1454        58  JUMP_BACK            20  'to 20'
               60  JUMP_FORWARD         74  'to 74'
             62_0  COME_FROM            52  '52'

 L.1455        62  LOAD_FAST                'cur'
               64  LOAD_STR                 '"'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    74  'to 74'

 L.1456        70  LOAD_CONST               False
               72  STORE_FAST               'quote'
             74_0  COME_FROM            68  '68'
             74_1  COME_FROM            60  '60'

 L.1457        74  LOAD_FAST                'part'
               76  LOAD_FAST                'cur'
               78  INPLACE_ADD      
               80  STORE_FAST               'part'

 L.1458        82  JUMP_BACK            20  'to 20'
             84_0  COME_FROM            44  '44'

 L.1460        84  LOAD_FAST                'cur'
               86  LOAD_STR                 ','
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   108  'to 108'

 L.1461        92  LOAD_FAST                'res'
               94  LOAD_METHOD              append
               96  LOAD_FAST                'part'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L.1462       102  LOAD_STR                 ''
              104  STORE_FAST               'part'

 L.1463       106  JUMP_BACK            20  'to 20'
            108_0  COME_FROM            90  '90'

 L.1465       108  LOAD_FAST                'cur'
              110  LOAD_STR                 '"'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   120  'to 120'

 L.1466       116  LOAD_CONST               True
              118  STORE_FAST               'quote'
            120_0  COME_FROM           114  '114'

 L.1468       120  LOAD_FAST                'part'
              122  LOAD_FAST                'cur'
              124  INPLACE_ADD      
              126  STORE_FAST               'part'
              128  JUMP_BACK            20  'to 20'

 L.1471       130  LOAD_FAST                'part'
              132  POP_JUMP_IF_FALSE   144  'to 144'

 L.1472       134  LOAD_FAST                'res'
              136  LOAD_METHOD              append
              138  LOAD_FAST                'part'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           132  '132'

 L.1474       144  LOAD_LISTCOMP            '<code_object <listcomp>>'
              146  LOAD_STR                 'parse_http_list.<locals>.<listcomp>'
              148  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              150  LOAD_FAST                'res'
              152  GET_ITER         
              154  CALL_FUNCTION_1       1  ''
              156  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 60


    class FileHandler(BaseHandler):

        def file_open(self, req):
            url = req.selector
            if url[:2] == '//' and url[2:3] != '/' and req.host and req.host != 'localhost':
                if req.host not in self.get_names:
                    raise URLError('file:// scheme is supported only on localhost')
            else:
                return self.open_local_file(req)

        names = None

        def get_names(self):
            if FileHandler.names is None:
                try:
                    FileHandler.names = tuple(socket.gethostbyname_ex('localhost')[2] + socket.gethostbyname_ex(socket.gethostname)[2])
                except socket.gaierror:
                    FileHandler.names = (
                     socket.gethostbyname('localhost'),)

            return FileHandler.names

        def open_local_file(self, req):
            import email.utils, mimetypes
            host = req.host
            filename = req.selector
            localfile = url2pathname(filename)
            try:
                stats = os.stat(localfile)
                size = stats.st_size
                modified = email.utils.formatdate((stats.st_mtime), usegmt=True)
                mtype = mimetypes.guess_type(filename)[0]
                headers = email.message_from_string('Content-type: %s\nContent-length: %d\nLast-modified: %s\n' % (
                 mtype or 'text/plain', size, modified))
                if host:
                    host, port = _splitport(host)
                elif not host or (port or _safe_gethostbyname(host)) in self.get_names:
                    if host:
                        origurl = 'file://' + host + filename
                    else:
                        origurl = 'file://' + filename
                    return addinfourl(open(localfile, 'rb'), headers, origurl)
            except OSError as exp:
                try:
                    raise URLError(exp)
                finally:
                    exp = None
                    del exp

            else:
                raise URLError('file not on local host')


    def _safe_gethostbyname--- This code section failed: ---

 L.1528         0  SETUP_FINALLY        14  'to 14'

 L.1529         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              gethostbyname
                6  LOAD_FAST                'host'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.1530        14  DUP_TOP          
               16  LOAD_GLOBAL              socket
               18  LOAD_ATTR                gaierror
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.1531        30  POP_EXCEPT       
               32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26


    class FTPHandler(BaseHandler):

        def ftp_open(self, req):
            import ftplib, mimetypes
            host = req.host
            if not host:
                raise URLError('ftp error: no host given')
            else:
                host, port = _splitport(host)
                if port is None:
                    port = ftplib.FTP_PORT
                else:
                    port = int(port)
                user, host = _splituser(host)
                if user:
                    user, passwd = _splitpasswd(user)
                else:
                    passwd = None
            host = unquote(host)
            user = user or ''
            passwd = passwd or ''
            try:
                host = socket.gethostbyname(host)
            except OSError as msg:
                try:
                    raise URLError(msg)
                finally:
                    msg = None
                    del msg

            else:
                path, attrs = _splitattr(req.selector)
                dirs = path.split('/')
                dirs = list(map(unquote, dirs))
                dirs, file = dirs[:-1], dirs[(-1)]
                if dirs:
                    if not dirs[0]:
                        dirs = dirs[1:]
                try:
                    fw = self.connect_ftp(user, passwd, host, port, dirs, req.timeout)
                    type = file and 'I' or 'D'
                    for attr in attrs:
                        attr, value = _splitvalue(attr)
                        if attr.lower == 'type':
                            if value in ('a', 'A', 'i', 'I', 'd', 'D'):
                                type = value.upper
                            fp, retrlen = fw.retrfile(file, type)
                            headers = ''
                            mtype = mimetypes.guess_type(req.full_url)[0]
                            if mtype:
                                headers += 'Content-type: %s\n' % mtype
                            if retrlen is not None:
                                if retrlen >= 0:
                                    headers += 'Content-length: %d\n' % retrlen
                            headers = email.message_from_string(headers)
                            return addinfourl(fp, headers, req.full_url)

                            except ftplib.all_errors as exp:
                    try:
                        exc = URLError('ftp error: %r' % exp)
                        raise exc.with_traceback(sys.exc_info[2])
                    finally:
                        exp = None
                        del exp

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
             user, host, port, '/'.join(dirs), timeout)
            if key in self.cache:
                self.timeout[key] = time.time + self.delay
            else:
                self.cache[key] = ftpwrapper(user, passwd, host, port, dirs, timeout)
                self.timeout[key] = time.time + self.delay
            self.check_cache
            return self.cache[key]

        def check_cache(self):
            t = time.time
            if self.soonest <= t:
                for k, v in list(self.timeout.items):
                    if v < t:
                        self.cache[k].close
                        del self.cache[k]
                        del self.timeout[k]

            self.soonest = min(list(self.timeout.values))
            if len(self.cache) == self.max_conns:
                for k, v in list(self.timeout.items):
                    if v == self.soonest:
                        del self.cache[k]
                        del self.timeout[k]
                        break
                else:
                    self.soonest = min(list(self.timeout.values))

        def clear_cache(self):
            for conn in self.cache.values:
                conn.close
            else:
                self.cache.clear
                self.timeout.clear


    class DataHandler(BaseHandler):

        def data_open(self, req):
            url = req.full_url
            scheme, data = url.split(':', 1)
            mediatype, data = data.split(',', 1)
            data = unquote_to_bytes(data)
            if mediatype.endswith(';base64'):
                data = base64.decodebytes(data)
                mediatype = mediatype[:-7]
            if not mediatype:
                mediatype = 'text/plain;charset=US-ASCII'
            headers = email.message_from_string('Content-type: %s\nContent-length: %d\n' % (
             mediatype, len(data)))
            return addinfourl(io.BytesIO(data), headers, url)


    MAXFTPCACHE = 10
    if os.name == 'nt':
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

    class URLopener:
        __doc__ = "Class to open URLs.\n    This is a class rather than just a subroutine because we may need\n    more than one set of global protocol-specific options.\n    Note -- this is a base class for those who don't want the\n    automatic handling of errors type 302 (relocated) and 401\n    (authorization needed)."
        _URLopener__tempfiles = None
        version = 'Python-urllib/%s' % __version__

        def __init__(self, proxies=None, **x509):
            msg = '%(class)s style of invoking requests is deprecated. Use newer urlopen functions/methods' % {'class': self.__class__.__name__}
            warnings.warn(msg, DeprecationWarning, stacklevel=3)
            if proxies is None:
                proxies = getproxies()
            assert hasattr(proxies, 'keys'), 'proxies must be a mapping'
            self.proxies = proxies
            self.key_file = x509.get('key_file')
            self.cert_file = x509.get('cert_file')
            self.addheaders = [('User-Agent', self.version), ('Accept', '*/*')]
            self._URLopener__tempfiles = []
            self._URLopener__unlink = os.unlink
            self.tempcache = None
            self.ftpcache = ftpcache

        def __del__(self):
            self.close

        def close(self):
            self.cleanup

        def cleanup(self):
            if self._URLopener__tempfiles:
                for file in self._URLopener__tempfiles:
                    try:
                        self._URLopener__unlink(file)
                    except OSError:
                        pass

                else:
                    del self._URLopener__tempfiles[:]

            if self.tempcache:
                self.tempcache.clear

        def addheader(self, *args):
            """Add a header to be used by the HTTP interface only
        e.g. u.addheader('Accept', 'sound/basic')"""
            self.addheaders.append(args)

        def open(self, fullurl, data=None):
            """Use URLopener().open(file) instead of open(file, 'r')."""
            fullurl = unwrap(_to_bytes(fullurl))
            fullurl = quote(fullurl, safe="%/:=&?~#+!$,;'@()*[]|")
            if self.tempcache:
                if fullurl in self.tempcache:
                    filename, headers = self.tempcache[fullurl]
                    fp = open(filename, 'rb')
                    return addinfourl(fp, headers, fullurl)
                else:
                    urltype, url = _splittype(fullurl)
                    if not urltype:
                        urltype = 'file'
                    if urltype in self.proxies:
                        proxy = self.proxies[urltype]
                        urltype, proxyhost = _splittype(proxy)
                        host, selector = _splithost(proxyhost)
                        url = (host, fullurl)
                    else:
                        proxy = None
                name = 'open_' + urltype
                self.type = urltype
                name = name.replace('-', '_')
                if not hasattr(self, name) or name == 'open_local_file':
                    if proxy:
                        return self.open_unknown_proxy(proxy, fullurl, data)
            else:
                return self.open_unknown(fullurl, data)
            try:
                if data is None:
                    return getattr(self, name)(url)
                return getattr(self, name)(url, data)
            except (HTTPError, URLError):
                raise
            except OSError as msg:
                try:
                    raise OSError('socket error', msg).with_traceback(sys.exc_info[2])
                finally:
                    msg = None
                    del msg

        def open_unknown(self, fullurl, data=None):
            """Overridable interface to open unknown URL type."""
            type, url = _splittype(fullurl)
            raise OSError('url error', 'unknown url type', type)

        def open_unknown_proxy(self, proxy, fullurl, data=None):
            """Overridable interface to open unknown URL type."""
            type, url = _splittype(fullurl)
            raise OSError('url error', 'invalid proxy for %s' % type, proxy)

        def retrieve(self, url, filename=None, reporthook=None, data=None):
            """retrieve(url) returns (filename, headers) for a local object
        or (tempfilename, headers) for a remote object."""
            url = unwrap(_to_bytes(url))
            if self.tempcache:
                if url in self.tempcache:
                    return self.tempcache[url]
            type, url1 = _splittype(url)
            if filename is None:
                if not type or type == 'file':
                    try:
                        fp = self.open_local_file(url1)
                        hdrs = fp.info
                        fp.close
                        return (url2pathname(_splithost(url1)[1]), hdrs)
                                    except OSError as msg:
                        try:
                            pass
                        finally:
                            msg = None
                            del msg

            fp = self.open(url, data)
            try:
                headers = fp.info
                if filename:
                    tfp = open(filename, 'wb')
                else:
                    garbage, path = _splittype(url)
                    garbage, path = _splithost(path or '')
                    path, garbage = _splitquery(path or '')
                    path, garbage = _splitattr(path or '')
                    suffix = os.path.splitext(path)[1]
                    fd, filename = tempfile.mkstemp(suffix)
                    self._URLopener__tempfiles.append(filename)
                    tfp = os.fdopen(fd, 'wb')
                try:
                    result = (
                     filename, headers)
                    if self.tempcache is not None:
                        self.tempcache[url] = result
                    bs = 8192
                    size = -1
                    read = 0
                    blocknum = 0
                    if 'content-length' in headers:
                        size = int(headers['Content-Length'])
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

                finally:
                    tfp.close

            finally:
                fp.close

            if size >= 0:
                if read < size:
                    raise ContentTooShortError('retrieval incomplete: got only %i out of %i bytes' % (
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
                host, selector = _splithost(url)
                if host:
                    user_passwd, host = _splituser(host)
                    host = unquote(host)
                realhost = host
            else:
                host, selector = url
                proxy_passwd, host = _splituser(host)
                urltype, rest = _splittype(selector)
                url = rest
                user_passwd = None
                if urltype.lower != 'http':
                    realhost = None
                else:
                    realhost, rest = _splithost(rest)
                    if realhost:
                        user_passwd, realhost = _splituser(realhost)
                    if user_passwd:
                        selector = '%s://%s%s' % (urltype, realhost, rest)
                    if proxy_bypass(realhost):
                        host = realhost
                    else:
                        if not host:
                            raise OSError('http error', 'no host given')
                        elif proxy_passwd:
                            proxy_passwd = unquote(proxy_passwd)
                            proxy_auth = base64.b64encode(proxy_passwd.encode).decode('ascii')
                        else:
                            proxy_auth = None
                        if user_passwd:
                            user_passwd = unquote(user_passwd)
                            auth = base64.b64encode(user_passwd.encode).decode('ascii')
                        else:
                            auth = None
                    http_conn = connection_factory(host)
                    headers = {}
                    if proxy_auth:
                        headers['Proxy-Authorization'] = 'Basic %s' % proxy_auth
                    if auth:
                        headers['Authorization'] = 'Basic %s' % auth
                    if realhost:
                        headers['Host'] = realhost
                headers['Connection'] = 'close'
                for header, value in self.addheaders:
                    headers[header] = value
                else:
                    if data is not None:
                        headers['Content-Type'] = 'application/x-www-form-urlencoded'
                        http_conn.request('POST', selector, data, headers)
                    else:
                        http_conn.request('GET', selector, headers=headers)
                    try:
                        response = http_conn.getresponse
                    except http.client.BadStatusLine:
                        raise URLError('http protocol error: bad status line')
                    else:
                        if 200 <= response.status < 300:
                            return addinfourl(response, response.msg, 'http:' + url, response.status)
                        return self.http_error(url, response.fp, response.status, response.reason, response.msg, data)

        def open_http(self, url, data=None):
            """Use HTTP protocol."""
            return self._open_generic_http(http.client.HTTPConnection, url, data)

        def http_error(self, url, fp, errcode, errmsg, headers, data=None):
            """Handle http errors.

        Derived class can override this, or provide specific handlers
        named http_error_DDD where DDD is the 3-digit error code."""
            name = 'http_error_%d' % errcode
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
            """Default error handler: close the connection and raise OSError."""
            fp.close
            raise HTTPError(url, errcode, errmsg, headers, None)

        if _have_ssl:

            def _https_connection(self, host):
                return http.client.HTTPSConnection(host, key_file=(self.key_file),
                  cert_file=(self.cert_file))

            def open_https(self, url, data=None):
                """Use HTTPS protocol."""
                return self._open_generic_http(self._https_connection, url, data)

        def open_file(self, url):
            """Use local file or FTP depending on form of URL."""
            if not isinstance(url, str):
                raise URLError('file error: proxy support for file protocol currently not implemented')
            elif url[:2] == '//' and url[2:3] != '/' and url[2:12].lower != 'localhost/':
                raise ValueError('file:// scheme is supported only on localhost')
            else:
                return self.open_local_file(url)

        def open_local_file(self, url):
            """Use local file."""
            import email.utils, mimetypes
            host, file = _splithost(url)
            localname = url2pathname(file)
            try:
                stats = os.stat(localname)
            except OSError as e:
                try:
                    raise URLError(e.strerror, e.filename)
                finally:
                    e = None
                    del e

            else:
                size = stats.st_size
                modified = email.utils.formatdate((stats.st_mtime), usegmt=True)
                mtype = mimetypes.guess_type(url)[0]
                headers = email.message_from_string('Content-Type: %s\nContent-Length: %d\nLast-modified: %s\n' % (
                 mtype or 'text/plain', size, modified))
                if not host:
                    urlfile = file
                    if file[:1] == '/':
                        urlfile = 'file://' + file
                    return addinfourl(open(localname, 'rb'), headers, urlfile)
                host, port = _splitport(host)
                if not port:
                    if socket.gethostbyname(host) in (localhost(),) + thishost():
                        urlfile = file
                        if file[:1] == '/':
                            urlfile = 'file://' + file
                        else:
                            if file[:2] == './':
                                raise ValueError('local file url may start with / or file:. Unknown url of type: %s' % url)
                            return addinfourl(open(localname, 'rb'), headers, urlfile)
                raise URLError('local file error: not on local host')

        def open_ftp(self, url):
            """Use FTP protocol."""
            if not isinstance(url, str):
                raise URLError('ftp error: proxy support for ftp protocol currently not implemented')
            else:
                import mimetypes
                host, path = _splithost(url)
                if not host:
                    raise URLError('ftp error: no host given')
                else:
                    host, port = _splitport(host)
                    user, host = _splituser(host)
                    if user:
                        user, passwd = _splitpasswd(user)
                    else:
                        passwd = None
                    host = unquote(host)
                    user = unquote(user or '')
                    passwd = unquote(passwd or '')
                    host = socket.gethostbyname(host)
                    if not port:
                        import ftplib
                        port = ftplib.FTP_PORT
                    else:
                        port = int(port)
                path, attrs = _splitattr(path)
                path = unquote(path)
                dirs = path.split('/')
                dirs, file = dirs[:-1], dirs[(-1)]
                if dirs:
                    if not dirs[0]:
                        dirs = dirs[1:]
                if dirs:
                    if not dirs[0]:
                        dirs[0] = '/'
                key = (
                 user, host, port, '/'.join(dirs))
                if len(self.ftpcache) > MAXFTPCACHE:
                    for k in list(self.ftpcache):
                        if k != key:
                            v = self.ftpcache[k]
                            del self.ftpcache[k]
                            v.close

            try:
                if key not in self.ftpcache:
                    self.ftpcache[key] = ftpwrapper(user, passwd, host, port, dirs)
                elif not file:
                    type = 'D'
                else:
                    type = 'I'
                for attr in attrs:
                    attr, value = _splitvalue(attr)
                    if attr.lower == 'type':
                        if value in ('a', 'A', 'i', 'I', 'd', 'D'):
                            type = value.upper
                        fp, retrlen = self.ftpcache[key].retrfile(file, type)
                        mtype = mimetypes.guess_type('ftp:' + url)[0]
                        headers = ''
                        if mtype:
                            headers += 'Content-Type: %s\n' % mtype
                        if retrlen is not None:
                            if retrlen >= 0:
                                headers += 'Content-Length: %d\n' % retrlen
                        headers = email.message_from_string(headers)
                        return addinfourl(fp, headers, 'ftp:' + url)

                    except ftperrors() as exp:
                try:
                    raise URLError('ftp error %r' % exp).with_traceback(sys.exc_info[2])
                finally:
                    exp = None
                    del exp

        def open_data(self, url, data=None):
            """Use "data" URL."""
            if not isinstance(url, str):
                raise URLError('data error: proxy support for data protocol currently not implemented')
            try:
                type, data = url.split(',', 1)
            except ValueError:
                raise OSError('data error', 'bad data URL')
            else:
                if not type:
                    type = 'text/plain;charset=US-ASCII'
                else:
                    semi = type.rfind(';')
                    if semi >= 0:
                        if '=' not in type[semi:]:
                            encoding = type[semi + 1:]
                            type = type[:semi]
                        else:
                            encoding = ''
                        msg = []
                        msg.append('Date: %s' % time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time)))
                        msg.append('Content-type: %s' % type)
                        if encoding == 'base64':
                            data = base64.decodebytes(data.encode('ascii')).decode('latin-1')
                    else:
                        data = unquote(data)
                msg.append('Content-Length: %d' % len(data))
                msg.append('')
                msg.append(data)
                msg = '\n'.join(msg)
                headers = email.message_from_string(msg)
                f = io.StringIO(msg)
                return addinfourl(f, headers, url)


    class FancyURLopener(URLopener):
        __doc__ = 'Derived class with handlers for errors we can handle (perhaps).'

        def __init__(self, *args, **kwargs):
            (URLopener.__init__)(self, *args, **kwargs)
            self.auth_cache = {}
            self.tries = 0
            self.maxtries = 10

        def http_error_default(self, url, fp, errcode, errmsg, headers):
            """Default error handling -- don't raise an exception."""
            return addinfourl(fp, headers, 'http:' + url, errcode)

        def http_error_302--- This code section failed: ---

 L.2157         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                tries
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               tries

 L.2158        14  SETUP_FINALLY       106  'to 106'

 L.2159        16  LOAD_FAST                'self'
               18  LOAD_ATTR                maxtries
               20  POP_JUMP_IF_FALSE    78  'to 78'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                tries
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                maxtries
               30  COMPARE_OP               >=
               32  POP_JUMP_IF_FALSE    78  'to 78'

 L.2160        34  LOAD_GLOBAL              hasattr
               36  LOAD_FAST                'self'
               38  LOAD_STR                 'http_error_500'
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L.2161        44  LOAD_FAST                'self'
               46  LOAD_ATTR                http_error_500
               48  STORE_FAST               'meth'
               50  JUMP_FORWARD         58  'to 58'
             52_0  COME_FROM            42  '42'

 L.2163        52  LOAD_FAST                'self'
               54  LOAD_ATTR                http_error_default
               56  STORE_FAST               'meth'
             58_0  COME_FROM            50  '50'

 L.2164        58  LOAD_FAST                'meth'
               60  LOAD_FAST                'url'
               62  LOAD_FAST                'fp'
               64  LOAD_CONST               500

 L.2165        66  LOAD_STR                 'Internal Server Error: Redirect Recursion'

 L.2166        68  LOAD_FAST                'headers'

 L.2164        70  CALL_FUNCTION_5       5  ''
               72  POP_BLOCK        
               74  CALL_FINALLY        106  'to 106'
               76  RETURN_VALUE     
             78_0  COME_FROM            32  '32'
             78_1  COME_FROM            20  '20'

 L.2167        78  LOAD_FAST                'self'
               80  LOAD_METHOD              redirect_internal
               82  LOAD_FAST                'url'
               84  LOAD_FAST                'fp'
               86  LOAD_FAST                'errcode'
               88  LOAD_FAST                'errmsg'

 L.2168        90  LOAD_FAST                'headers'

 L.2168        92  LOAD_FAST                'data'

 L.2167        94  CALL_METHOD_6         6  ''
               96  STORE_FAST               'result'

 L.2169        98  LOAD_FAST                'result'
              100  POP_BLOCK        
              102  CALL_FINALLY        106  'to 106'
              104  RETURN_VALUE     
            106_0  COME_FROM           102  '102'
            106_1  COME_FROM            74  '74'
            106_2  COME_FROM_FINALLY    14  '14'

 L.2171       106  LOAD_CONST               0
              108  LOAD_FAST                'self'
              110  STORE_ATTR               tries
              112  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 74

        def redirect_internal(self, url, fp, errcode, errmsg, headers, data):
            if 'location' in headers:
                newurl = headers['location']
            else:
                if 'uri' in headers:
                    newurl = headers['uri']
                else:
                    return
            fp.close
            newurl = urljoin(self.type + ':' + url, newurl)
            urlparts = urlparse(newurl)
            if urlparts.scheme not in ('http', 'https', 'ftp', ''):
                raise HTTPError(newurl, errcode, errmsg + " Redirection to url '%s' is not allowed." % newurl, headers, fp)
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
            return self.http_error_default(url, fp, errcode, errmsg, headers)

        def http_error_401(self, url, fp, errcode, errmsg, headers, data=None, retry=False):
            """Error 401 -- authentication required.
        This function supports Basic authentication only."""
            if 'www-authenticate' not in headers:
                URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
            else:
                stuff = headers['www-authenticate']
                match = re.match('[ \t]*([^ \t]+)[ \t]+realm="([^"]*)"', stuff)
                if not match:
                    URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
                scheme, realm = match.groups
                if scheme.lower != 'basic':
                    URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
                retry or URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
            name = 'retry_' + self.type + '_basic_auth'
            if data is None:
                return getattr(self, name)(url, realm)
            return getattr(self, name)(url, realm, data)

        def http_error_407(self, url, fp, errcode, errmsg, headers, data=None, retry=False):
            """Error 407 -- proxy authentication required.
        This function supports Basic authentication only."""
            if 'proxy-authenticate' not in headers:
                URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
            else:
                stuff = headers['proxy-authenticate']
                match = re.match('[ \t]*([^ \t]+)[ \t]+realm="([^"]*)"', stuff)
                if not match:
                    URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
                scheme, realm = match.groups
                if scheme.lower != 'basic':
                    URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
                retry or URLopener.http_error_default(self, url, fp, errcode, errmsg, headers)
            name = 'retry_proxy_' + self.type + '_basic_auth'
            if data is None:
                return getattr(self, name)(url, realm)
            return getattr(self, name)(url, realm, data)

        def retry_proxy_http_basic_auth(self, url, realm, data=None):
            host, selector = _splithost(url)
            newurl = 'http://' + host + selector
            proxy = self.proxies['http']
            urltype, proxyhost = _splittype(proxy)
            proxyhost, proxyselector = _splithost(proxyhost)
            i = proxyhost.find('@') + 1
            proxyhost = proxyhost[i:]
            user, passwd = self.get_user_passwd(proxyhost, realm, i)
            if not user:
                if not passwd:
                    return
            proxyhost = '%s:%s@%s' % (quote(user, safe=''),
             quote(passwd, safe=''), proxyhost)
            self.proxies['http'] = 'http://' + proxyhost + proxyselector
            if data is None:
                return self.open(newurl)
            return self.open(newurl, data)

        def retry_proxy_https_basic_auth(self, url, realm, data=None):
            host, selector = _splithost(url)
            newurl = 'https://' + host + selector
            proxy = self.proxies['https']
            urltype, proxyhost = _splittype(proxy)
            proxyhost, proxyselector = _splithost(proxyhost)
            i = proxyhost.find('@') + 1
            proxyhost = proxyhost[i:]
            user, passwd = self.get_user_passwd(proxyhost, realm, i)
            if not user:
                if not passwd:
                    return
            proxyhost = '%s:%s@%s' % (quote(user, safe=''),
             quote(passwd, safe=''), proxyhost)
            self.proxies['https'] = 'https://' + proxyhost + proxyselector
            if data is None:
                return self.open(newurl)
            return self.open(newurl, data)

        def retry_http_basic_auth(self, url, realm, data=None):
            host, selector = _splithost(url)
            i = host.find('@') + 1
            host = host[i:]
            user, passwd = self.get_user_passwd(host, realm, i)
            if not user:
                if not passwd:
                    return
            host = '%s:%s@%s' % (quote(user, safe=''),
             quote(passwd, safe=''), host)
            newurl = 'http://' + host + selector
            if data is None:
                return self.open(newurl)
            return self.open(newurl, data)

        def retry_https_basic_auth(self, url, realm, data=None):
            host, selector = _splithost(url)
            i = host.find('@') + 1
            host = host[i:]
            user, passwd = self.get_user_passwd(host, realm, i)
            if not user:
                if not passwd:
                    return
            host = '%s:%s@%s' % (quote(user, safe=''),
             quote(passwd, safe=''), host)
            newurl = 'https://' + host + selector
            if data is None:
                return self.open(newurl)
            return self.open(newurl, data)

        def get_user_passwd(self, host, realm, clear_cache=0):
            key = realm + '@' + host.lower
            if key in self.auth_cache:
                if clear_cache:
                    del self.auth_cache[key]
                else:
                    return self.auth_cache[key]
            user, passwd = self.prompt_user_passwd(host, realm)
            if user or passwd:
                self.auth_cache[key] = (
                 user, passwd)
            return (
             user, passwd)

        def prompt_user_passwd--- This code section failed: ---

 L.2343         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              getpass
                6  STORE_FAST               'getpass'

 L.2344         8  SETUP_FINALLY        56  'to 56'

 L.2345        10  LOAD_GLOBAL              input
               12  LOAD_STR                 'Enter username for %s at %s: '
               14  LOAD_FAST                'realm'
               16  LOAD_FAST                'host'
               18  BUILD_TUPLE_2         2 
               20  BINARY_MODULO    
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'user'

 L.2346        26  LOAD_FAST                'getpass'
               28  LOAD_METHOD              getpass
               30  LOAD_STR                 'Enter password for %s in %s at %s: '

 L.2347        32  LOAD_FAST                'user'
               34  LOAD_FAST                'realm'
               36  LOAD_FAST                'host'
               38  BUILD_TUPLE_3         3 

 L.2346        40  BINARY_MODULO    
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'passwd'

 L.2348        46  LOAD_FAST                'user'
               48  LOAD_FAST                'passwd'
               50  BUILD_TUPLE_2         2 
               52  POP_BLOCK        
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY     8  '8'

 L.2349        56  DUP_TOP          
               58  LOAD_GLOBAL              KeyboardInterrupt
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    82  'to 82'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.2350        70  LOAD_GLOBAL              print
               72  CALL_FUNCTION_0       0  ''
               74  POP_TOP          

 L.2351        76  POP_EXCEPT       
               78  LOAD_CONST               (None, None)
               80  RETURN_VALUE     
             82_0  COME_FROM            62  '62'
               82  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 66


    _localhost = None

    def localhost():
        """Return the IP address of the magic hostname 'localhost'."""
        global _localhost
        if _localhost is None:
            _localhost = socket.gethostbyname('localhost')
        return _localhost


    _thishost = None

    def thishost():
        """Return the IP addresses of the current host."""
        global _thishost
        if _thishost is None:
            try:
                _thishost = tuple(socket.gethostbyname_ex(socket.gethostname)[2])
            except socket.gaierror:
                _thishost = tuple(socket.gethostbyname_ex('localhost')[2])

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
            _noheaders = email.message_from_string('')
        return _noheaders


    class ftpwrapper:
        __doc__ = 'Class used by open_ftp() for cache of open FTP connections.'

        def __init__(self, user, passwd, host, port, dirs, timeout=None, persistent=True):
            self.user = user
            self.passwd = passwd
            self.host = host
            self.port = port
            self.dirs = dirs
            self.timeout = timeout
            self.refcount = 0
            self.keepalive = persistent
            try:
                self.init
            except:
                self.close
                raise

        def init(self):
            import ftplib
            self.busy = 0
            self.ftp = ftplib.FTP
            self.ftp.connect(self.host, self.port, self.timeout)
            self.ftp.login(self.user, self.passwd)
            _target = '/'.join(self.dirs)
            self.ftp.cwd(_target)

        def retrfile(self, file, type):
            import ftplib
            self.endtransfer
            if type in ('d', 'D'):
                cmd = 'TYPE A'
                isdir = 1
            else:
                cmd = 'TYPE ' + type
                isdir = 0
            try:
                self.ftp.voidcmd(cmd)
            except ftplib.all_errors:
                self.init
                self.ftp.voidcmd(cmd)
            else:
                conn = None
                if file and not isdir:
                    try:
                        cmd = 'RETR ' + file
                        conn, retrlen = self.ftp.ntransfercmd(cmd)
                    except ftplib.error_perm as reason:
                        try:
                            if str(reason)[:3] != '550':
                                raise URLError('ftp error: %r' % reason).with_traceback(sys.exc_info[2])
                        finally:
                            reason = None
                            del reason

                    else:
                        if not conn:
                            self.ftp.voidcmd('TYPE A')
                            if file:
                                pwd = self.ftp.pwd
                                try:
                                    try:
                                        self.ftp.cwd(file)
                                    except ftplib.error_perm as reason:
                                        try:
                                            raise URLError('ftp error: %r' % reason) from reason
                                        finally:
                                            reason = None
                                            del reason

                                finally:
                                    self.ftp.cwd(pwd)

                                cmd = 'LIST ' + file
                            else:
                                cmd = 'LIST'
                            conn, retrlen = self.ftp.ntransfercmd(cmd)
                        self.busy = 1
                        ftpobj = addclosehook(conn.makefile('rb'), self.file_close)
                        self.refcount += 1
                        conn.close
                        return (
                         ftpobj, retrlen)

        def endtransfer(self):
            self.busy = 0

        def close(self):
            self.keepalive = False
            if self.refcount <= 0:
                self.real_close

        def file_close(self):
            self.endtransfer
            self.refcount -= 1
            if self.refcount <= 0:
                if not self.keepalive:
                    self.real_close

        def real_close(self):
            self.endtransfer
            try:
                self.ftp.close
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
        for name, value in os.environ.items:
            name = name.lower
            if value and name[-6:] == '_proxy':
                proxies[name[:-6]] = value
        else:
            if 'REQUEST_METHOD' in os.environ:
                proxies.pop('http', None)

        for name, value in os.environ.items:
            if name[-6:] == '_proxy':
                name = name.lower
                if value:
                    proxies[name[:-6]] = value
                else:
                    proxies.pop(name[:-6], None)
            return proxies


    def proxy_bypass_environment(host, proxies=None):
        """Test if proxies should not be used for a particular host.

    Checks the proxy dict for the value of no_proxy, which should
    be a list of comma separated DNS suffixes, or '*' for all hosts.

    """
        if proxies is None:
            proxies = getproxies_environment()
        try:
            no_proxy = proxies['no']
        except KeyError:
            return False
        else:
            if no_proxy == '*':
                return True
            host = host.lower
            hostonly, port = _splitport(host)
            for name in no_proxy.split(','):
                name = name.strip
                if name:
                    name = name.lstrip('.')
                    name = name.lower

            if hostonly == name or host == name:
                return True
                name = '.' + name
                if hostonly.endswith(name) or host.endswith(name):
                    return True
                return False


    def _proxy_bypass_macosx_sysconf--- This code section failed: ---

 L.2570         0  LOAD_CONST               0
                2  LOAD_CONST               ('fnmatch',)
                4  IMPORT_NAME              fnmatch
                6  IMPORT_FROM              fnmatch
                8  STORE_FAST               'fnmatch'
               10  POP_TOP          

 L.2572        12  LOAD_GLOBAL              _splitport
               14  LOAD_FAST                'host'
               16  CALL_FUNCTION_1       1  ''
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'hostonly'
               22  STORE_FAST               'port'

 L.2574        24  LOAD_CODE                <code_object ip2num>
               26  LOAD_STR                 '_proxy_bypass_macosx_sysconf.<locals>.ip2num'
               28  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               30  STORE_FAST               'ip2num'

 L.2582        32  LOAD_STR                 '.'
               34  LOAD_FAST                'host'
               36  COMPARE_OP               not-in
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L.2583        40  LOAD_FAST                'proxy_settings'
               42  LOAD_STR                 'exclude_simple'
               44  BINARY_SUBSCR    
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L.2584        48  LOAD_CONST               True
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'
             52_1  COME_FROM            38  '38'

 L.2586        52  LOAD_CONST               None
               54  STORE_FAST               'hostIP'

 L.2588        56  LOAD_FAST                'proxy_settings'
               58  LOAD_METHOD              get
               60  LOAD_STR                 'exceptions'
               62  LOAD_CONST               ()
               64  CALL_METHOD_2         2  ''
               66  GET_ITER         
             68_0  COME_FROM           290  '290'
             68_1  COME_FROM           236  '236'
               68  FOR_ITER            300  'to 300'
               70  STORE_FAST               'value'

 L.2590        72  LOAD_FAST                'value'
               74  POP_JUMP_IF_TRUE     78  'to 78'

 L.2590        76  JUMP_BACK            68  'to 68'
             78_0  COME_FROM            74  '74'

 L.2592        78  LOAD_GLOBAL              re
               80  LOAD_METHOD              match
               82  LOAD_STR                 '(\\d+(?:\\.\\d+)*)(/\\d+)?'
               84  LOAD_FAST                'value'
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'm'

 L.2593        90  LOAD_FAST                'm'
               92  LOAD_CONST               None
               94  COMPARE_OP               is-not
            96_98  POP_JUMP_IF_FALSE   282  'to 282'

 L.2594       100  LOAD_FAST                'hostIP'
              102  LOAD_CONST               None
              104  COMPARE_OP               is
              106  POP_JUMP_IF_FALSE   156  'to 156'

 L.2595       108  SETUP_FINALLY       132  'to 132'

 L.2596       110  LOAD_GLOBAL              socket
              112  LOAD_METHOD              gethostbyname
              114  LOAD_FAST                'hostonly'
              116  CALL_METHOD_1         1  ''
              118  STORE_FAST               'hostIP'

 L.2597       120  LOAD_FAST                'ip2num'
              122  LOAD_FAST                'hostIP'
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'hostIP'
              128  POP_BLOCK        
              130  JUMP_FORWARD        156  'to 156'
            132_0  COME_FROM_FINALLY   108  '108'

 L.2598       132  DUP_TOP          
              134  LOAD_GLOBAL              OSError
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   154  'to 154'
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L.2599       146  POP_EXCEPT       
              148  JUMP_BACK            68  'to 68'
              150  POP_EXCEPT       
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           138  '138'
              154  END_FINALLY      
            156_0  COME_FROM           152  '152'
            156_1  COME_FROM           130  '130'
            156_2  COME_FROM           106  '106'

 L.2601       156  LOAD_FAST                'ip2num'
              158  LOAD_FAST                'm'
              160  LOAD_METHOD              group
              162  LOAD_CONST               1
              164  CALL_METHOD_1         1  ''
              166  CALL_FUNCTION_1       1  ''
              168  STORE_FAST               'base'

 L.2602       170  LOAD_FAST                'm'
              172  LOAD_METHOD              group
              174  LOAD_CONST               2
              176  CALL_METHOD_1         1  ''
              178  STORE_FAST               'mask'

 L.2603       180  LOAD_FAST                'mask'
              182  LOAD_CONST               None
              184  COMPARE_OP               is
              186  POP_JUMP_IF_FALSE   214  'to 214'

 L.2604       188  LOAD_CONST               8
              190  LOAD_FAST                'm'
              192  LOAD_METHOD              group
              194  LOAD_CONST               1
              196  CALL_METHOD_1         1  ''
              198  LOAD_METHOD              count
              200  LOAD_STR                 '.'
              202  CALL_METHOD_1         1  ''
              204  LOAD_CONST               1
              206  BINARY_ADD       
              208  BINARY_MULTIPLY  
              210  STORE_FAST               'mask'
              212  JUMP_FORWARD        230  'to 230'
            214_0  COME_FROM           186  '186'

 L.2606       214  LOAD_GLOBAL              int
              216  LOAD_FAST                'mask'
              218  LOAD_CONST               1
              220  LOAD_CONST               None
              222  BUILD_SLICE_2         2 
              224  BINARY_SUBSCR    
              226  CALL_FUNCTION_1       1  ''
              228  STORE_FAST               'mask'
            230_0  COME_FROM           212  '212'

 L.2608       230  LOAD_FAST                'mask'
              232  LOAD_CONST               0
              234  COMPARE_OP               <
              236  POP_JUMP_IF_TRUE     68  'to 68'
              238  LOAD_FAST                'mask'
              240  LOAD_CONST               32
              242  COMPARE_OP               >
              244  POP_JUMP_IF_FALSE   248  'to 248'

 L.2610       246  JUMP_BACK            68  'to 68'
            248_0  COME_FROM           244  '244'

 L.2612       248  LOAD_CONST               32
              250  LOAD_FAST                'mask'
              252  BINARY_SUBTRACT  
              254  STORE_FAST               'mask'

 L.2614       256  LOAD_FAST                'hostIP'
              258  LOAD_FAST                'mask'
              260  BINARY_RSHIFT    
              262  LOAD_FAST                'base'
              264  LOAD_FAST                'mask'
              266  BINARY_RSHIFT    
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   298  'to 298'

 L.2615       274  POP_TOP          
              276  LOAD_CONST               True
              278  RETURN_VALUE     
              280  JUMP_BACK            68  'to 68'
            282_0  COME_FROM            96  '96'

 L.2617       282  LOAD_FAST                'fnmatch'
              284  LOAD_FAST                'host'
              286  LOAD_FAST                'value'
              288  CALL_FUNCTION_2       2  ''
              290  POP_JUMP_IF_FALSE    68  'to 68'

 L.2618       292  POP_TOP          
              294  LOAD_CONST               True
              296  RETURN_VALUE     
            298_0  COME_FROM           270  '270'
              298  JUMP_BACK            68  'to 68'

 L.2620       300  LOAD_CONST               False
              302  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 150


    if sys.platform == 'darwin':
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
            """Return True, if host should be bypassed.

        Checks proxy settings gathered from the environment, if specified,
        or from the MacOSX framework SystemConfiguration.

        """
            proxies = getproxies_environment()
            if proxies:
                return proxy_bypass_environment(host, proxies)
            return proxy_bypass_macosx_sysconf(host)


        def getproxies():
            return getproxies_environment() or getproxies_macosx_sysconf()


    else:
        if os.name == 'nt':

            def getproxies_registry():
                """Return a dictionary of scheme -> proxy server URL mappings.

        Win32 uses the registry to store proxies.

        """
                proxies = {}
                try:
                    import winreg
                except ImportError:
                    return proxies
                else:
                    try:
                        internetSettings = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings')
                        proxyEnable = winreg.QueryValueEx(internetSettings, 'ProxyEnable')[0]
                        if proxyEnable:
                            proxyServer = str(winreg.QueryValueEx(internetSettings, 'ProxyServer')[0])
                            if '=' in proxyServer:
                                for p in proxyServer.split(';'):
                                    protocol, address = p.split('=', 1)
                                    if not re.match('(?:[^/:]+)://', address):
                                        address = '%s://%s' % (protocol, address)
                                    proxies[protocol] = address

                            else:
                                if proxyServer[:5] == 'http:':
                                    proxies['http'] = proxyServer
                                else:
                                    proxies['http'] = 'http://%s' % proxyServer
                                    proxies['https'] = 'https://%s' % proxyServer
                                    proxies['ftp'] = 'ftp://%s' % proxyServer
                        internetSettings.Close
                    except (OSError, ValueError, TypeError):
                        pass
                    else:
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
                else:
                    try:
                        internetSettings = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings')
                        proxyEnable = winreg.QueryValueEx(internetSettings, 'ProxyEnable')[0]
                        proxyOverride = str(winreg.QueryValueEx(internetSettings, 'ProxyOverride')[0])
                    except OSError:
                        return 0
                    else:
                        return proxyEnable and proxyOverride or 0
                        rawHost, port = _splitport(host)
                        host = [rawHost]
                        try:
                            addr = socket.gethostbyname(rawHost)
                            if addr != rawHost:
                                host.append(addr)
                        except OSError:
                            pass
                        else:
                            try:
                                fqdn = socket.getfqdn(rawHost)
                                if fqdn != rawHost:
                                    host.append(fqdn)
                            except OSError:
                                pass
                            else:
                                proxyOverride = proxyOverride.split(';')
                        for test in proxyOverride:
                            if test == '<local>':
                                if '.' not in rawHost:
                                    return 1
                            test = test.replace('.', '\\.')
                            test = test.replace('*', '.*')
                            test = test.replace('?', '.')
                            for val in host:
                                if re.match(test, val, re.I):
                                    return 1
                            else:
                                return 0


            def proxy_bypass(host):
                """Return True, if host should be bypassed.

        Checks proxy settings gathered from the environment, if specified,
        or the registry.

        """
                proxies = getproxies_environment()
                if proxies:
                    return proxy_bypass_environment(host, proxies)
                return proxy_bypass_registry(host)


        else:
            getproxies = getproxies_environment
            proxy_bypass = proxy_bypass_environment