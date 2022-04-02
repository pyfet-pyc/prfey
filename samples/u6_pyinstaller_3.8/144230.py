# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\models.py
"""
requests.models
~~~~~~~~~~~~~~~

This module contains the primary objects that power Requests.
"""
import collections, datetime
from io import BytesIO, UnsupportedOperation
from .hooks import default_hooks
from .structures import CaseInsensitiveDict
from .auth import HTTPBasicAuth
from .cookies import cookiejar_from_dict, get_cookie_header, _copy_cookie_jar
from packages.urllib3.fields import RequestField
from packages.urllib3.filepost import encode_multipart_formdata
from packages.urllib3.util import parse_url
from packages.urllib3.exceptions import DecodeError, ReadTimeoutError, ProtocolError, LocationParseError
from .exceptions import HTTPError, MissingSchema, InvalidURL, ChunkedEncodingError, ContentDecodingError, ConnectionError, StreamConsumedError
from .utils import guess_filename, get_auth_from_url, requote_uri, stream_decode_response_unicode, to_key_val_list, parse_header_links, iter_slices, guess_json_utf, super_len, to_native_string
from .compat import cookielib, urlunparse, urlsplit, urlencode, str, bytes, StringIO, is_py2, chardet, json, builtin_str, basestring
from .status_codes import codes
REDIRECT_STATI = (
 codes.moved,
 codes.found,
 codes.other,
 codes.temporary_redirect,
 codes.permanent_redirect)
DEFAULT_REDIRECT_LIMIT = 30
CONTENT_CHUNK_SIZE = 10240
ITER_CHUNK_SIZE = 512
json_dumps = json.dumps

class RequestEncodingMixin(object):

    @property
    def path_url(self):
        """Build the path URL to use."""
        url = []
        p = urlsplit(self.url)
        path = p.path
        if not path:
            path = '/'
        url.append(path)
        query = p.query
        if query:
            url.append('?')
            url.append(query)
        return ''.join(url)

    @staticmethod
    def _encode_params(data):
        """Encode parameters in a piece of data.

        Will successfully encode parameters when passed as a dict or a list of
        2-tuples. Order is retained if data is a list of 2-tuples but arbitrary
        if parameters are supplied as a dict.
        """
        if isinstance(data, (str, bytes)):
            return data
        if hasattr(data, 'read'):
            return data
        if hasattr(data, '__iter__'):
            result = []
            for k, vs in to_key_val_list(data):
                if not (isinstance(vs, basestring) or hasattr(vs, '__iter__')):
                    vs = [
                     vs]
                for v in vs:
                    if v is not None:
                        result.append((
                         k.encode('utf-8') if isinstance(k, str) else k,
                         v.encode('utf-8') if isinstance(v, str) else v))
                else:
                    return urlencode(result, doseq=True)

        return data

    @staticmethod
    def _encode_files(files, data):
        """Build the body for a multipart/form-data request.

        Will successfully encode files when passed as a dict or a list of
        2-tuples. Order is retained if data is a list of 2-tuples but arbitrary
        if parameters are supplied as a dict.

        """
        if not files:
            raise ValueError('Files must be provided.')
        else:
            if isinstance(data, basestring):
                raise ValueError('Data must not be a string.')
            else:
                new_fields = []
                fields = to_key_val_list(data or {})
                files = to_key_val_list(files or {})
                for field, val in fields:
                    val = isinstance(val, basestring) or hasattr(val, '__iter__') or [
                     val]

            for v in val:
                if v is not None:
                    if not isinstance(v, bytes):
                        v = str(v)
                    new_fields.append((
                     field.decode('utf-8') if isinstance(field, bytes) else field,
                     v.encode('utf-8') if isinstance(v, str) else v))
            else:
                for k, v in files:
                    ft = None
                    fh = None
                    if isinstance(v, (tuple, list)):
                        if len(v) == 2:
                            fn, fp = v
                        else:
                            if len(v) == 3:
                                fn, fp, ft = v
                            else:
                                fn, fp, ft, fh = v
                    else:
                        fn = guess_filename(v) or k
                        fp = v
                    if isinstance(fp, (str, bytes, bytearray)):
                        fdata = fp
                    else:
                        fdata = fp.read()
                    rf = RequestField(name=k, data=fdata, filename=fn,
                      headers=fh)
                    rf.make_multipart(content_type=ft)
                    new_fields.append(rf)
                else:
                    body, content_type = encode_multipart_formdata(new_fields)
                    return (
                     body, content_type)


class RequestHooksMixin(object):

    def register_hook(self, event, hook):
        """Properly register a hook."""
        if event not in self.hooks:
            raise ValueError('Unsupported event specified, with event name "%s"' % event)
        elif isinstance(hook, collections.Callable):
            self.hooks[event].append(hook)
        else:
            if hasattr(hook, '__iter__'):
                self.hooks[event].extend((h for h in hook if isinstance(h, collections.Callable)))

    def deregister_hook--- This code section failed: ---

 L. 179         0  SETUP_FINALLY        24  'to 24'

 L. 180         2  LOAD_FAST                'self'
                4  LOAD_ATTR                hooks
                6  LOAD_FAST                'event'
                8  BINARY_SUBSCR    
               10  LOAD_METHOD              remove
               12  LOAD_FAST                'hook'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L. 181        18  POP_BLOCK        
               20  LOAD_CONST               True
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L. 182        24  DUP_TOP          
               26  LOAD_GLOBAL              ValueError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 183        38  POP_EXCEPT       
               40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 22


class Request(RequestHooksMixin):
    __doc__ = "A user-created :class:`Request <Request>` object.\n\n    Used to prepare a :class:`PreparedRequest <PreparedRequest>`, which is sent to the server.\n\n    :param method: HTTP method to use.\n    :param url: URL to send.\n    :param headers: dictionary of headers to send.\n    :param files: dictionary of {filename: fileobject} files to multipart upload.\n    :param data: the body to attach to the request. If a dictionary is provided, form-encoding will take place.\n    :param json: json for the body to attach to the request (if data is not specified).\n    :param params: dictionary of URL parameters to append to the URL.\n    :param auth: Auth handler or (user, pass) tuple.\n    :param cookies: dictionary or CookieJar of cookies to attach to this request.\n    :param hooks: dictionary of callback hooks, for internal usage.\n\n    Usage::\n\n      >>> import requests\n      >>> req = requests.Request('GET', 'http://httpbin.org/get')\n      >>> req.prepare()\n      <PreparedRequest [GET]>\n\n    "

    def __init__(self, method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None, json=None):
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params
        hooks = {} if hooks is None else hooks
        self.hooks = default_hooks()
        for k, v in list(hooks.items()):
            self.register_hook(event=k, hook=v)
        else:
            self.method = method
            self.url = url
            self.headers = headers
            self.files = files
            self.data = data
            self.json = json
            self.params = params
            self.auth = auth
            self.cookies = cookies

    def __repr__(self):
        return '<Request [%s]>' % self.method

    def prepare(self):
        """Constructs a :class:`PreparedRequest <PreparedRequest>` for transmission and returns it."""
        p = PreparedRequest()
        p.prepare(method=(self.method),
          url=(self.url),
          headers=(self.headers),
          files=(self.files),
          data=(self.data),
          json=(self.json),
          params=(self.params),
          auth=(self.auth),
          cookies=(self.cookies),
          hooks=(self.hooks))
        return p


class PreparedRequest(RequestEncodingMixin, RequestHooksMixin):
    __doc__ = "The fully mutable :class:`PreparedRequest <PreparedRequest>` object,\n    containing the exact bytes that will be sent to the server.\n\n    Generated from either a :class:`Request <Request>` object or manually.\n\n    Usage::\n\n      >>> import requests\n      >>> req = requests.Request('GET', 'http://httpbin.org/get')\n      >>> r = req.prepare()\n      <PreparedRequest [GET]>\n\n      >>> s = requests.Session()\n      >>> s.send(r)\n      <Response [200]>\n\n    "

    def __init__(self):
        self.method = None
        self.url = None
        self.headers = None
        self._cookies = None
        self.body = None
        self.hooks = default_hooks()

    def prepare(self, method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None, json=None):
        """Prepares the entire request with the given parameters."""
        self.prepare_method(method)
        self.prepare_url(url, params)
        self.prepare_headers(headers)
        self.prepare_cookies(cookies)
        self.prepare_body(data, files, json)
        self.prepare_auth(auth, url)
        self.prepare_hooks(hooks)

    def __repr__(self):
        return '<PreparedRequest [%s]>' % self.method

    def copy(self):
        p = PreparedRequest()
        p.method = self.method
        p.url = self.url
        p.headers = self.headers.copy() if self.headers is not None else None
        p._cookies = _copy_cookie_jar(self._cookies)
        p.body = self.body
        p.hooks = self.hooks
        return p

    def prepare_method(self, method):
        """Prepares the given HTTP method."""
        self.method = method
        if self.method is not None:
            self.method = self.method.upper()

    def prepare_url(self, url, params):
        """Prepares the given HTTP URL."""
        if isinstance(url, bytes):
            url = url.decode('utf8')
        else:
            url = unicode(url) if is_py2 else str(url)
        if ':' in url:
            if not url.lower().startswith('http'):
                self.url = url
                return
        try:
            scheme, auth, host, port, path, query, fragment = parse_url(url)
        except LocationParseError as e:
            try:
                raise InvalidURL(*e.args)
            finally:
                e = None
                del e

        else:
            if not scheme:
                raise MissingSchema('Invalid URL {0!r}: No schema supplied. Perhaps you meant http://{0}?'.format(to_native_string(url, 'utf8')))
            if not host:
                raise InvalidURL('Invalid URL %r: No host supplied' % url)
        try:
            host = host.encode('idna').decode('utf-8')
        except UnicodeError:
            raise InvalidURL('URL has an invalid label.')
        else:
            netloc = auth or ''
            if netloc:
                netloc += '@'
            netloc += host
            if port:
                netloc += ':' + str(port)
            if not path:
                path = '/'
            if is_py2:
                if isinstance(scheme, str):
                    scheme = scheme.encode('utf-8')
                if isinstance(netloc, str):
                    netloc = netloc.encode('utf-8')
                if isinstance(path, str):
                    path = path.encode('utf-8')
                if isinstance(query, str):
                    query = query.encode('utf-8')
                if isinstance(fragment, str):
                    fragment = fragment.encode('utf-8')
            enc_params = self._encode_params(params)
            if enc_params:
                if query:
                    query = '%s&%s' % (query, enc_params)
                else:
                    query = enc_params
            url = requote_uri(urlunparse([scheme, netloc, path, None, query, fragment]))
            self.url = url

    def prepare_headers(self, headers):
        """Prepares the given HTTP headers."""
        if headers:
            self.headers = CaseInsensitiveDict(((to_native_string(name), value) for name, value in headers.items()))
        else:
            self.headers = CaseInsensitiveDict()

    def prepare_body(self, data, files, json=None):
        """Prepares the given HTTP body data."""
        body = None
        content_type = None
        length = None
        if json is not None:
            content_type = 'application/json'
            body = json_dumps(json)
        is_stream = all([
         hasattr(data, '__iter__'),
         not isinstance(data, (basestring, list, tuple, dict))])
        try:
            length = super_len(data)
        except (TypeError, AttributeError, UnsupportedOperation):
            length = None

        if is_stream:
            body = data
            if files:
                raise NotImplementedError('Streamed bodies and files are mutually exclusive.')
            elif length is not None:
                self.headers['Content-Length'] = builtin_str(length)
            else:
                self.headers['Transfer-Encoding'] = 'chunked'
        else:
            if files:
                body, content_type = self._encode_files(files, data)
            else:
                if data and json is None:
                    body = self._encode_params(data)
                    if isinstance(data, basestring) or hasattr(data, 'read'):
                        content_type = None
                    else:
                        content_type = 'application/x-www-form-urlencoded'
            self.prepare_content_length(body)
            if content_type:
                if 'content-type' not in self.headers:
                    self.headers['Content-Type'] = content_type
            self.body = body

    def prepare_content_length(self, body):
        if hasattr(body, 'seek') and hasattr(body, 'tell'):
            body.seek(0, 2)
            self.headers['Content-Length'] = builtin_str(body.tell())
            body.seek(0, 0)
        else:
            if body is not None:
                l = super_len(body)
                if l:
                    self.headers['Content-Length'] = builtin_str(l)
            elif self.method not in ('GET', 'HEAD') and self.headers.get('Content-Length') is None:
                self.headers['Content-Length'] = '0'

    def prepare_auth(self, auth, url=''):
        """Prepares the given HTTP auth data."""
        if auth is None:
            url_auth = get_auth_from_url(self.url)
            auth = url_auth if any(url_auth) else None
        if auth:
            if isinstance(auth, tuple):
                if len(auth) == 2:
                    auth = HTTPBasicAuth(*auth)
            r = auth(self)
            self.__dict__.update(r.__dict__)
            self.prepare_content_length(self.body)

    def prepare_cookies(self, cookies):
        """Prepares the given HTTP cookie data.

        This function eventually generates a ``Cookie`` header from the
        given cookies using cookielib. Due to cookielib's design, the header
        will not be regenerated if it already exists, meaning this function
        can only be called once for the life of the
        :class:`PreparedRequest <PreparedRequest>` object. Any subsequent calls
        to ``prepare_cookies`` will have no actual effect, unless the "Cookie"
        header is removed beforehand."""
        if isinstance(cookies, cookielib.CookieJar):
            self._cookies = cookies
        else:
            self._cookies = cookiejar_from_dict(cookies)
        cookie_header = get_cookie_header(self._cookies, self)
        if cookie_header is not None:
            self.headers['Cookie'] = cookie_header

    def prepare_hooks(self, hooks):
        """Prepares the given hooks."""
        hooks = hooks or []
        for event in hooks:
            self.register_hook(event, hooks[event])


class Response(object):
    __doc__ = "The :class:`Response <Response>` object, which contains a\n    server's response to an HTTP request.\n    "
    __attrs__ = [
     '_content',
     'status_code',
     'headers',
     'url',
     'history',
     'encoding',
     'reason',
     'cookies',
     'elapsed',
     'request']

    def __init__(self):
        super(Response, self).__init__()
        self._content = False
        self._content_consumed = False
        self.status_code = None
        self.headers = CaseInsensitiveDict()
        self.raw = None
        self.url = None
        self.encoding = None
        self.history = []
        self.reason = None
        self.cookies = cookiejar_from_dict({})
        self.elapsed = datetime.timedelta(0)
        self.request = None

    def __getstate__(self):
        if not self._content_consumed:
            self.content
        return dict(((
         attr, getattr(self, attr, None)) for attr in self.__attrs__))

    def __setstate__(self, state):
        for name, value in state.items():
            setattr(self, name, value)
        else:
            setattr(self, '_content_consumed', True)
            setattr(self, 'raw', None)

    def __repr__(self):
        return '<Response [%s]>' % self.status_code

    def __bool__(self):
        """Returns true if :attr:`status_code` is 'OK'."""
        return self.ok

    def __nonzero__(self):
        """Returns true if :attr:`status_code` is 'OK'."""
        return self.ok

    def __iter__(self):
        """Allows you to use a response as an iterator."""
        return self.iter_content(128)

    @property
    def ok(self):
        try:
            self.raise_for_status()
        except HTTPError:
            return False
        else:
            return True

    @property
    def is_redirect(self):
        """True if this Response is a well-formed HTTP redirect that could have
        been processed automatically (by :meth:`Session.resolve_redirects`).
        """
        return 'location' in self.headers and self.status_code in REDIRECT_STATI

    @property
    def is_permanent_redirect(self):
        """True if this Response one of the permanant versions of redirect"""
        return 'location' in self.headers and self.status_code in (codes.moved_permanently, codes.permanent_redirect)

    @property
    def apparent_encoding(self):
        """The apparent encoding, provided by the chardet library"""
        return chardet.detect(self.content)['encoding']

    def iter_content(self, chunk_size=1, decode_unicode=False):
        """Iterates over the response data.  When stream=True is set on the
        request, this avoids reading the content at once into memory for
        large responses.  The chunk size is the number of bytes it should
        read into memory.  This is not necessarily the length of each item
        returned as decoding can take place.

        If decode_unicode is True, content will be decoded using the best
        available encoding based on the response.
        """

        def generate():
            try:
                try:
                    for chunk in self.raw.stream(chunk_size, decode_content=True):
                        (yield chunk)

                except ProtocolError as e:
                    try:
                        raise ChunkedEncodingError(e)
                    finally:
                        e = None
                        del e

                except DecodeError as e:
                    try:
                        raise ContentDecodingError(e)
                    finally:
                        e = None
                        del e

                except ReadTimeoutError as e:
                    try:
                        raise ConnectionError(e)
                    finally:
                        e = None
                        del e

            except AttributeError:
                while True:
                    chunk = self.raw.read(chunk_size)
                    if not chunk:
                        break
                    (yield chunk)

            else:
                self._content_consumed = True

        if self._content_consumed:
            if isinstance(self._content, bool):
                raise StreamConsumedError()
        reused_chunks = iter_slices(self._content, chunk_size)
        stream_chunks = generate()
        chunks = reused_chunks if self._content_consumed else stream_chunks
        if decode_unicode:
            chunks = stream_decode_response_unicode(chunks, self)
        return chunks

    def iter_lines(self, chunk_size=ITER_CHUNK_SIZE, decode_unicode=None, delimiter=None):
        """Iterates over the response data, one line at a time.  When
        stream=True is set on the request, this avoids reading the
        content at once into memory for large responses.

        .. note:: This method is not reentrant safe.
        """
        pending = None
        for chunk in self.iter_content(chunk_size=chunk_size, decode_unicode=decode_unicode):
            if pending is not None:
                chunk = pending + chunk
            else:
                if delimiter:
                    lines = chunk.split(delimiter)
                else:
                    lines = chunk.splitlines()
                if lines and lines[(-1)] and chunk and lines[(-1)][(-1)] == chunk[(-1)]:
                    pending = lines.pop()
                else:
                    pass
                pending = None

        for line in lines:
            (yield line)
        else:
            if pending is not None:
                (yield pending)

    @property
    def content(self):
        """Content of the response, in bytes."""
        if self._content is False:
            try:
                if self._content_consumed:
                    raise RuntimeError('The content for this response was already consumed')
                elif self.status_code == 0:
                    self._content = None
                else:
                    self._content = bytes().join(self.iter_content(CONTENT_CHUNK_SIZE)) or bytes()
            except AttributeError:
                self._content = None

        self._content_consumed = True
        return self._content

    @property
    def text(self):
        """Content of the response, in unicode.

        If Response.encoding is None, encoding will be guessed using
        ``chardet``.

        The encoding of the response content is determined based solely on HTTP
        headers, following RFC 2616 to the letter. If you can take advantage of
        non-HTTP knowledge to make a better guess at the encoding, you should
        set ``r.encoding`` appropriately before accessing this property.
        """
        content = None
        encoding = self.encoding
        if not self.content:
            return str('')
        if self.encoding is None:
            encoding = self.apparent_encoding
        try:
            content = str((self.content), encoding, errors='replace')
        except (LookupError, TypeError):
            content = str((self.content), errors='replace')
        else:
            return content

    def json--- This code section failed: ---

 L. 804         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encoding
                4  POP_JUMP_IF_TRUE     84  'to 84'
                6  LOAD_GLOBAL              len
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                content
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_CONST               3
               16  COMPARE_OP               >
               18  POP_JUMP_IF_FALSE    84  'to 84'

 L. 809        20  LOAD_GLOBAL              guess_json_utf
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                content
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'encoding'

 L. 810        30  LOAD_FAST                'encoding'
               32  LOAD_CONST               None
               34  COMPARE_OP               is-not
               36  POP_JUMP_IF_FALSE    84  'to 84'

 L. 811        38  SETUP_FINALLY        64  'to 64'

 L. 812        40  LOAD_GLOBAL              json
               42  LOAD_ATTR                loads
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                content
               48  LOAD_METHOD              decode
               50  LOAD_FAST                'encoding'
               52  CALL_METHOD_1         1  ''
               54  BUILD_TUPLE_1         1 
               56  LOAD_FAST                'kwargs'
               58  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               60  POP_BLOCK        
               62  RETURN_VALUE     
             64_0  COME_FROM_FINALLY    38  '38'

 L. 813        64  DUP_TOP          
               66  LOAD_GLOBAL              UnicodeDecodeError
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE    82  'to 82'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 818        78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
             82_0  COME_FROM            70  '70'
               82  END_FINALLY      
             84_0  COME_FROM            80  '80'
             84_1  COME_FROM            36  '36'
             84_2  COME_FROM            18  '18'
             84_3  COME_FROM             4  '4'

 L. 819        84  LOAD_GLOBAL              json
               86  LOAD_ATTR                loads
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                text
               92  BUILD_TUPLE_1         1 
               94  LOAD_FAST                'kwargs'
               96  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 74

    @property
    def links(self):
        """Returns the parsed header links of the response, if any."""
        header = self.headers.get('link')
        l = {}
        if header:
            links = parse_header_links(header)
            for link in links:
                key = link.get('rel') or link.get('url')
                l[key] = link

        return l

    def raise_for_status(self):
        """Raises stored :class:`HTTPError`, if one occurred."""
        http_error_msg = ''
        if 400 <= self.status_code < 500:
            http_error_msg = '%s Client Error: %s' % (self.status_code, self.reason)
        else:
            if 500 <= self.status_code < 600:
                http_error_msg = '%s Server Error: %s' % (self.status_code, self.reason)
        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)

    def close(self):
        """Releases the connection back to the pool. Once this method has been
        called the underlying ``raw`` object must not be accessed again.

        *Note: Should not normally need to be called explicitly.*
        """
        return self.raw.release_conn()