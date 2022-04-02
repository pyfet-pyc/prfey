# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\models.py
"""
requests.models
~~~~~~~~~~~~~~~

This module contains the primary objects that power Requests.
"""
import datetime, sys, encodings.idna
from urllib3.fields import RequestField
from urllib3.filepost import encode_multipart_formdata
from urllib3.util import parse_url
from urllib3.exceptions import DecodeError, ReadTimeoutError, ProtocolError, LocationParseError
from io import UnsupportedOperation
from .hooks import default_hooks
from .structures import CaseInsensitiveDict
from .auth import HTTPBasicAuth
from .cookies import cookiejar_from_dict, get_cookie_header, _copy_cookie_jar
from .exceptions import HTTPError, MissingSchema, InvalidURL, ChunkedEncodingError, ContentDecodingError, ConnectionError, StreamConsumedError
from ._internal_utils import to_native_string, unicode_is_ascii
from .utils import guess_filename, get_auth_from_url, requote_uri, stream_decode_response_unicode, to_key_val_list, parse_header_links, iter_slices, guess_json_utf, super_len, check_header_validity
from .compat import Callable, Mapping, cookielib, urlunparse, urlsplit, urlencode, str, bytes, is_py2, chardet, builtin_str, basestring
from .compat import json as complexjson
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

            return urlencode(result, doseq=True)
        return data

    @staticmethod
    def _encode_files(files, data):
        """Build the body for a multipart/form-data request.

        Will successfully encode files when passed as a dict or a list of
        tuples. Order is retained if data is a list of tuples but arbitrary
        if parameters are supplied as a dict.
        The tuples may be 2-tuples (filename, fileobj), 3-tuples (filename, fileobj, contentype)
        or 4-tuples (filename, fileobj, contentype, custom_headers).
        """
        if not files:
            raise ValueError('Files must be provided.')
        elif isinstance(data, basestring):
            raise ValueError('Data must not be a string.')
        new_fields = []
        fields = to_key_val_list(data or {})
        files = to_key_val_list(files or {})
        for field, val in fields:
            if not (isinstance(val, basestring) or hasattr(val, '__iter__')):
                val = [
                 val]
            for v in val:
                if v is not None:
                    if not isinstance(v, bytes):
                        v = str(v)
                    else:
                        new_fields.append((
                         field.decode('utf-8') if isinstance(field, bytes) else field,
                         v.encode('utf-8') if isinstance(v, str) else v))

        for k, v in files:
            ft = None
            fh = None
            if isinstance(v, (tuple, list)):
                if len(v) == 2:
                    fn, fp = v
                elif len(v) == 3:
                    fn, fp, ft = v
                else:
                    fn, fp, ft, fh = v
            else:
                fn = guess_filename(v) or k
                fp = v
            if isinstance(fp, (str, bytes, bytearray)):
                fdata = fp
            else:
                if hasattr(fp, 'read'):
                    fdata = fp.read()
                else:
                    if fp is None:
                        continue
                    else:
                        fdata = fp
            rf = RequestField(name=k, data=fdata, filename=fn, headers=fh)
            rf.make_multipart(content_type=ft)
            new_fields.append(rf)

        body, content_type = encode_multipart_formdata(new_fields)
        return (
         body, content_type)


class RequestHooksMixin(object):

    def register_hook(self, event, hook):
        """Properly register a hook."""
        if event not in self.hooks:
            raise ValueError('Unsupported event specified, with event name "%s"' % event)
        if isinstance(hook, Callable):
            self.hooks[event].append(hook)
        elif hasattr(hook, '__iter__'):
            self.hooks[event].extend((h for h in hook if isinstance(h, Callable)))

    def deregister_hook(self, event, hook):
        """Deregister a previously registered hook.
        Returns True if the hook existed, False if not.
        """
        try:
            self.hooks[event].remove(hook)
            return True
        except ValueError:
            return False


class Request(RequestHooksMixin):
    __doc__ = "A user-created :class:`Request <Request>` object.\n\n    Used to prepare a :class:`PreparedRequest <PreparedRequest>`, which is sent to the server.\n\n    :param method: HTTP method to use.\n    :param url: URL to send.\n    :param headers: dictionary of headers to send.\n    :param files: dictionary of {filename: fileobject} files to multipart upload.\n    :param data: the body to attach to the request. If a dictionary or\n        list of tuples ``[(key, value)]`` is provided, form-encoding will\n        take place.\n    :param json: json for the body to attach to the request (if files or data is not specified).\n    :param params: URL parameters to append to the URL. If a dictionary or\n        list of tuples ``[(key, value)]`` is provided, form-encoding will\n        take place.\n    :param auth: Auth handler or (user, pass) tuple.\n    :param cookies: dictionary or CookieJar of cookies to attach to this request.\n    :param hooks: dictionary of callback hooks, for internal usage.\n\n    Usage::\n\n      >>> import requests\n      >>> req = requests.Request('GET', 'https://httpbin.org/get')\n      >>> req.prepare()\n      <PreparedRequest [GET]>\n    "

    def __init__(self, method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None, json=None):
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params
        hooks = {} if hooks is None else hooks
        self.hooks = default_hooks()
        for k, v in list(hooks.items()):
            self.register_hook(event=k, hook=v)

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
    __doc__ = "The fully mutable :class:`PreparedRequest <PreparedRequest>` object,\n    containing the exact bytes that will be sent to the server.\n\n    Instances are generated from a :class:`Request <Request>` object, and\n    should not be instantiated manually; doing so may produce undesirable\n    effects.\n\n    Usage::\n\n      >>> import requests\n      >>> req = requests.Request('GET', 'https://httpbin.org/get')\n      >>> r = req.prepare()\n      >>> r\n      <PreparedRequest [GET]>\n\n      >>> s = requests.Session()\n      >>> s.send(r)\n      <Response [200]>\n    "

    def __init__(self):
        self.method = None
        self.url = None
        self.headers = None
        self._cookies = None
        self.body = None
        self.hooks = default_hooks()
        self._body_position = None

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
        p._body_position = self._body_position
        return p

    def prepare_method(self, method):
        """Prepares the given HTTP method."""
        self.method = method
        if self.method is not None:
            self.method = to_native_string(self.method.upper())

    @staticmethod
    def _get_idna_encoded_host(host):
        import idna
        try:
            host = idna.encode(host, uts46=True).decode('utf-8')
        except idna.IDNAError:
            raise UnicodeError

        return host

    def prepare_url(self, url, params):
        """Prepares the given HTTP URL."""
        if isinstance(url, bytes):
            url = url.decode('utf8')
        else:
            url = unicode(url) if is_py2 else str(url)
        url = url.lstrip()
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

            if not scheme:
                error = 'Invalid URL {0!r}: No schema supplied. Perhaps you meant http://{0}?'
                error = error.format(to_native_string(url, 'utf8'))
                raise MissingSchema(error)
            if not host:
                raise InvalidURL('Invalid URL %r: No host supplied' % url)
            if not unicode_is_ascii(host):
                try:
                    host = self._get_idna_encoded_host(host)
                except UnicodeError:
                    raise InvalidURL('URL has an invalid label.')

            elif host.startswith('*'):
                raise InvalidURL('URL has an invalid label.')
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
            if isinstance(params, (str, bytes)):
                params = to_native_string(params)
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
        self.headers = CaseInsensitiveDict()
        if headers:
            for header in headers.items():
                check_header_validity(header)
                name, value = header
                self.headers[to_native_string(name)] = value

    def prepare_body(self, data, files, json=None):
        """Prepares the given HTTP body data."""
        body = None
        content_type = None
        if not data or json is not None:
            content_type = 'application/json'
            body = complexjson.dumps(json)
            if not isinstance(body, bytes):
                body = body.encode('utf-8')
            is_stream = all([
             hasattr(data, '__iter__'),
             not isinstance(data, (basestring, list, tuple, Mapping))])
            if is_stream:
                try:
                    length = super_len(data)
                except (TypeError, AttributeError, UnsupportedOperation):
                    length = None

                body = data
                if getattr(body, 'tell', None) is not None:
                    try:
                        self._body_position = body.tell()
                    except (IOError, OSError):
                        self._body_position = object()

                    if files:
                        raise NotImplementedError('Streamed bodies and files are mutually exclusive.')
                if length:
                    self.headers['Content-Length'] = builtin_str(length)
                else:
                    self.headers['Transfer-Encoding'] = 'chunked'
            else:
                if files:
                    body, content_type = self._encode_files(files, data)
                elif data:
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
        """Prepare Content-Length header based on request method and body"""
        if body is not None:
            length = super_len(body)
            if length:
                self.headers['Content-Length'] = builtin_str(length)
        elif self.method not in ('GET', 'HEAD'):
            if self.headers.get('Content-Length') is None:
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
        header is removed beforehand.
        """
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
     '_content', 'status_code', 'headers', 'url', 'history',
     'encoding', 'reason', 'cookies', 'elapsed', 'request']

    def __init__(self):
        self._content = False
        self._content_consumed = False
        self._next = None
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

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __getstate__(self):
        if not self._content_consumed:
            self.content
        return {attr:getattr(self, attr, None) for attr in self.__attrs__}

    def __setstate__(self, state):
        for name, value in state.items():
            setattr(self, name, value)

        setattr(self, '_content_consumed', True)
        setattr(self, 'raw', None)

    def __repr__(self):
        return '<Response [%s]>' % self.status_code

    def __bool__(self):
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        return self.ok

    def __nonzero__(self):
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
        return self.ok

    def __iter__(self):
        """Allows you to use a response as an iterator."""
        return self.iter_content(128)

    @property
    def ok(self):
        """Returns True if :attr:`status_code` is less than 400, False if not.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """
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
        """True if this Response one of the permanent versions of redirect."""
        return 'location' in self.headers and self.status_code in (codes.moved_permanently, codes.permanent_redirect)

    @property
    def next(self):
        """Returns a PreparedRequest for the next request in a redirect chain, if there is one."""
        return self._next

    @property
    def apparent_encoding(self):
        """The apparent encoding, provided by the chardet library."""
        return chardet.detect(self.content)['encoding']

    def iter_content(self, chunk_size=1, decode_unicode=False):
        """Iterates over the response data.  When stream=True is set on the
        request, this avoids reading the content at once into memory for
        large responses.  The chunk size is the number of bytes it should
        read into memory.  This is not necessarily the length of each item
        returned as decoding can take place.

        chunk_size must be of type int or None. A value of None will
        function differently depending on the value of `stream`.
        stream=True will read data as it arrives in whatever size the
        chunks are received. If stream=False, data is returned as
        a single chunk.

        If decode_unicode is True, content will be decoded using the best
        available encoding based on the response.
        """

        def generate--- This code section failed: ---

 L. 751         0  LOAD_GLOBAL              hasattr
                2  LOAD_DEREF               'self'
                4  LOAD_ATTR                raw
                6  LOAD_STR                 'stream'
                8  CALL_FUNCTION_2       2  '2 positional arguments'
               10  POP_JUMP_IF_FALSE   174  'to 174'

 L. 752        12  SETUP_EXCEPT         50  'to 50'

 L. 753        14  SETUP_LOOP           46  'to 46'
               16  LOAD_DEREF               'self'
               18  LOAD_ATTR                raw
               20  LOAD_ATTR                stream
               22  LOAD_DEREF               'chunk_size'
               24  LOAD_CONST               True
               26  LOAD_CONST               ('decode_content',)
               28  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               30  GET_ITER         
             32_0  COME_FROM            42  '42'
               32  FOR_ITER             44  'to 44'
               34  STORE_FAST               'chunk'

 L. 754        36  LOAD_FAST                'chunk'
               38  YIELD_VALUE      
               40  POP_TOP          
               42  JUMP_BACK            32  'to 32'
               44  POP_BLOCK        
             46_0  COME_FROM_LOOP       14  '14'
               46  POP_BLOCK        
               48  JUMP_FORWARD        204  'to 204'
             50_0  COME_FROM_EXCEPT     12  '12'

 L. 755        50  DUP_TOP          
               52  LOAD_GLOBAL              ProtocolError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    90  'to 90'
               58  POP_TOP          
               60  STORE_FAST               'e'
               62  POP_TOP          
               64  SETUP_FINALLY        78  'to 78'

 L. 756        66  LOAD_GLOBAL              ChunkedEncodingError
               68  LOAD_FAST                'e'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  RAISE_VARARGS_1       1  'exception instance'
               74  POP_BLOCK        
               76  LOAD_CONST               None
             78_0  COME_FROM_FINALLY    64  '64'
               78  LOAD_CONST               None
               80  STORE_FAST               'e'
               82  DELETE_FAST              'e'
               84  END_FINALLY      
               86  POP_EXCEPT       
               88  JUMP_FORWARD        204  'to 204'
             90_0  COME_FROM            56  '56'

 L. 757        90  DUP_TOP          
               92  LOAD_GLOBAL              DecodeError
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   130  'to 130'
               98  POP_TOP          
              100  STORE_FAST               'e'
              102  POP_TOP          
              104  SETUP_FINALLY       118  'to 118'

 L. 758       106  LOAD_GLOBAL              ContentDecodingError
              108  LOAD_FAST                'e'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  RAISE_VARARGS_1       1  'exception instance'
              114  POP_BLOCK        
              116  LOAD_CONST               None
            118_0  COME_FROM_FINALLY   104  '104'
              118  LOAD_CONST               None
              120  STORE_FAST               'e'
              122  DELETE_FAST              'e'
              124  END_FINALLY      
              126  POP_EXCEPT       
              128  JUMP_FORWARD        204  'to 204'
            130_0  COME_FROM            96  '96'

 L. 759       130  DUP_TOP          
              132  LOAD_GLOBAL              ReadTimeoutError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   170  'to 170'
              138  POP_TOP          
              140  STORE_FAST               'e'
              142  POP_TOP          
              144  SETUP_FINALLY       158  'to 158'

 L. 760       146  LOAD_GLOBAL              ConnectionError
              148  LOAD_FAST                'e'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  RAISE_VARARGS_1       1  'exception instance'
              154  POP_BLOCK        
              156  LOAD_CONST               None
            158_0  COME_FROM_FINALLY   144  '144'
              158  LOAD_CONST               None
              160  STORE_FAST               'e'
              162  DELETE_FAST              'e'
              164  END_FINALLY      
              166  POP_EXCEPT       
              168  JUMP_FORWARD        204  'to 204'
            170_0  COME_FROM           136  '136'
              170  END_FINALLY      
              172  JUMP_FORWARD        204  'to 204'
            174_0  COME_FROM            10  '10'

 L. 763       174  SETUP_LOOP          204  'to 204'
            176_0  COME_FROM           200  '200'

 L. 764       176  LOAD_DEREF               'self'
              178  LOAD_ATTR                raw
              180  LOAD_METHOD              read
              182  LOAD_DEREF               'chunk_size'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  STORE_FAST               'chunk'

 L. 765       188  LOAD_FAST                'chunk'
              190  POP_JUMP_IF_TRUE    194  'to 194'

 L. 766       192  BREAK_LOOP       
            194_0  COME_FROM           190  '190'

 L. 767       194  LOAD_FAST                'chunk'
              196  YIELD_VALUE      
              198  POP_TOP          
              200  JUMP_BACK           176  'to 176'
              202  POP_BLOCK        
            204_0  COME_FROM_LOOP      174  '174'
            204_1  COME_FROM_EXCEPT_CLAUSE   172  '172'
            204_2  COME_FROM_EXCEPT_CLAUSE   168  '168'
            204_3  COME_FROM_EXCEPT_CLAUSE   128  '128'
            204_4  COME_FROM_EXCEPT_CLAUSE    88  '88'
            204_5  COME_FROM_EXCEPT_CLAUSE    48  '48'

 L. 769       204  LOAD_CONST               True
              206  LOAD_DEREF               'self'
              208  STORE_ATTR               _content_consumed

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 204_1

        if self._content_consumed and isinstance(self._content, bool):
            raise StreamConsumedError()
        else:
            pass
        if chunk_size is not None:
            if not isinstance(chunk_size, int):
                raise TypeError('chunk_size must be an int, it is instead a %s.' % type(chunk_size))
            reused_chunks = iter_slices(self._content, chunk_size)
            stream_chunks = generate()
            chunks = reused_chunks if self._content_consumed else stream_chunks
            if decode_unicode:
                chunks = stream_decode_response_unicode(chunks, self)
            return chunks

    def iter_lines(self, chunk_size=ITER_CHUNK_SIZE, decode_unicode=False, delimiter=None):
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
                if linesand lines[(-1)] and lines[(-1)] and lines[(-1)][(-1)] == chunk[(-1)]:
                    pending = lines.pop()
                else:
                    pending = None
                for line in lines:
                    yield line

        if pending is not None:
            yield pending

    @property
    def content(self):
        """Content of the response, in bytes."""
        if self._content is False:
            if self._content_consumed:
                raise RuntimeError('The content for this response was already consumed')
            if self.status_code == 0 or self.raw is None:
                self._content = None
            else:
                self._content = ''.join(self.iter_content(CONTENT_CHUNK_SIZE)) or ''
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

        return content

    def json(self, **kwargs):
        r"""Returns the json-encoded content of a response, if any.

        :param \*\*kwargs: Optional arguments that ``json.loads`` takes.
        :raises ValueError: If the response body does not contain valid json.
        """
        if not self.encoding:
            if self.content:
                if len(self.content) > 3:
                    encoding = guess_json_utf(self.content)
                    if encoding is not None:
                        try:
                            return (complexjson.loads)(
                             (self.content.decode(encoding)), **kwargs)
                        except UnicodeDecodeError:
                            pass

        return (complexjson.loads)((self.text), **kwargs)

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
        """Raises :class:`HTTPError`, if one occurred."""
        http_error_msg = ''
        if isinstance(self.reason, bytes):
            try:
                reason = self.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = self.reason.decode('iso-8859-1')

        else:
            reason = self.reason
        if 400 <= self.status_code < 500:
            http_error_msg = '%s Client Error: %s for url: %s' % (self.status_code, reason, self.url)
        elif 500 <= self.status_code < 600:
            http_error_msg = '%s Server Error: %s for url: %s' % (self.status_code, reason, self.url)
        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)

    def close(self):
        """Releases the connection back to the pool. Once this method has been
        called the underlying ``raw`` object must not be accessed again.

        *Note: Should not normally need to be called explicitly.*
        """
        if not self._content_consumed:
            self.raw.close()
        release_conn = getattr(self.raw, 'release_conn', None)
        if release_conn is not None:
            release_conn()