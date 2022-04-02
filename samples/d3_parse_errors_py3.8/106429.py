# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\cookies.py
"""
requests.cookies
~~~~~~~~~~~~~~~~

Compatibility code to be able to use `cookielib.CookieJar` with requests.

requests.utils imports from here, so be careful with imports.
"""
import copy, time, calendar
from ._internal_utils import to_native_string
from .compat import cookielib, urlparse, urlunparse, Morsel, MutableMapping
try:
    import threading
except ImportError:
    import dummy_threading as threading
else:

    class MockRequest(object):
        __doc__ = 'Wraps a `requests.Request` to mimic a `urllib2.Request`.\n\n    The code in `cookielib.CookieJar` expects this interface in order to correctly\n    manage cookie policies, i.e., determine whether a cookie can be set, given the\n    domains of the request and the cookie.\n\n    The original request object is read-only. The client is responsible for collecting\n    the new headers via `get_new_headers()` and interpreting them appropriately. You\n    probably want `get_cookie_header`, defined below.\n    '

        def __init__(self, request):
            self._r = request
            self._new_headers = {}
            self.type = urlparse(self._r.url).scheme

        def get_type(self):
            return self.type

        def get_host(self):
            return urlparse(self._r.url).netloc

        def get_origin_req_host(self):
            return self.get_host()

        def get_full_url(self):
            if not self._r.headers.get('Host'):
                return self._r.url
            host = to_native_string((self._r.headers['Host']), encoding='utf-8')
            parsed = urlparse(self._r.url)
            return urlunparse([
             parsed.scheme, host, parsed.path, parsed.params, parsed.query,
             parsed.fragment])

        def is_unverifiable(self):
            return True

        def has_header(self, name):
            return name in self._r.headers or name in self._new_headers

        def get_header(self, name, default=None):
            return self._r.headers.get(name, self._new_headers.get(name, default))

        def add_header(self, key, val):
            """cookielib has no legitimate use for this method; add it back if you find one."""
            raise NotImplementedError('Cookie headers should be added with add_unredirected_header()')

        def add_unredirected_header(self, name, value):
            self._new_headers[name] = value

        def get_new_headers(self):
            return self._new_headers

        @property
        def unverifiable(self):
            return self.is_unverifiable()

        @property
        def origin_req_host(self):
            return self.get_origin_req_host()

        @property
        def host(self):
            return self.get_host()


    class MockResponse(object):
        __doc__ = 'Wraps a `httplib.HTTPMessage` to mimic a `urllib.addinfourl`.\n\n    ...what? Basically, expose the parsed HTTP headers from the server response\n    the way `cookielib` expects to see them.\n    '

        def __init__(self, headers):
            """Make a MockResponse for `cookielib` to read.

        :param headers: a httplib.HTTPMessage or analogous carrying the headers
        """
            self._headers = headers

        def info(self):
            return self._headers

        def getheaders(self, name):
            self._headers.getheaders(name)


    def extract_cookies_to_jar(jar, request, response):
        """Extract the cookies from the response into a CookieJar.

    :param jar: cookielib.CookieJar (not necessarily a RequestsCookieJar)
    :param request: our own requests.Request object
    :param response: urllib3.HTTPResponse object
    """
        if not (hasattr(response, '_original_response') and response._original_response):
            return
        req = MockRequest(request)
        res = MockResponse(response._original_response.msg)
        jar.extract_cookies(res, req)


    def get_cookie_header(jar, request):
        """
    Produce an appropriate Cookie header string to be sent with `request`, or None.

    :rtype: str
    """
        r = MockRequest(request)
        jar.add_cookie_header(r)
        return r.get_new_headers().get('Cookie')


    def remove_cookie_by_name--- This code section failed: ---

 L. 151         0  BUILD_LIST_0          0 
                2  STORE_FAST               'clearables'

 L. 152         4  LOAD_FAST                'cookiejar'
                6  GET_ITER         
              8_0  COME_FROM            86  '86'
              8_1  COME_FROM            62  '62'
              8_2  COME_FROM            42  '42'
              8_3  COME_FROM            22  '22'
                8  FOR_ITER             88  'to 88'
               10  STORE_FAST               'cookie'

 L. 153        12  LOAD_FAST                'cookie'
               14  LOAD_ATTR                name
               16  LOAD_FAST                'name'
               18  COMPARE_OP               !=
               20  POP_JUMP_IF_FALSE    24  'to 24'

 L. 154        22  JUMP_BACK             8  'to 8'
             24_0  COME_FROM            20  '20'

 L. 155        24  LOAD_FAST                'domain'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  LOAD_FAST                'domain'
               34  LOAD_FAST                'cookie'
               36  LOAD_ATTR                domain
               38  COMPARE_OP               !=
               40  POP_JUMP_IF_FALSE    44  'to 44'

 L. 156        42  JUMP_BACK             8  'to 8'
             44_0  COME_FROM            40  '40'
             44_1  COME_FROM            30  '30'

 L. 157        44  LOAD_FAST                'path'
               46  LOAD_CONST               None
               48  COMPARE_OP               is-not
               50  POP_JUMP_IF_FALSE    64  'to 64'
               52  LOAD_FAST                'path'
               54  LOAD_FAST                'cookie'
               56  LOAD_ATTR                path
               58  COMPARE_OP               !=
               60  POP_JUMP_IF_FALSE    64  'to 64'

 L. 158        62  JUMP_BACK             8  'to 8'
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            50  '50'

 L. 159        64  LOAD_FAST                'clearables'
               66  LOAD_METHOD              append
               68  LOAD_FAST                'cookie'
               70  LOAD_ATTR                domain
               72  LOAD_FAST                'cookie'
               74  LOAD_ATTR                path
               76  LOAD_FAST                'cookie'
               78  LOAD_ATTR                name
               80  BUILD_TUPLE_3         3 
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
               86  JUMP_BACK             8  'to 8'
             88_0  COME_FROM             8  '8'

 L. 161        88  LOAD_FAST                'clearables'
               90  GET_ITER         
             92_0  COME_FROM           116  '116'
               92  FOR_ITER            118  'to 118'
               94  UNPACK_SEQUENCE_3     3 
               96  STORE_FAST               'domain'
               98  STORE_FAST               'path'
              100  STORE_FAST               'name'

 L. 162       102  LOAD_FAST                'cookiejar'
              104  LOAD_METHOD              clear
              106  LOAD_FAST                'domain'
              108  LOAD_FAST                'path'
              110  LOAD_FAST                'name'
              112  CALL_METHOD_3         3  ''
              114  POP_TOP          
              116  JUMP_BACK            92  'to 92'
            118_0  COME_FROM            92  '92'

Parse error at or near `LOAD_FAST' instruction at offset 88


    class CookieConflictError(RuntimeError):
        __doc__ = 'There are two cookies that meet the criteria specified in the cookie jar.\n    Use .get and .set and include domain and path args in order to be more specific.\n    '


    class RequestsCookieJar(cookielib.CookieJar, MutableMapping):
        __doc__ = "Compatibility class; is a cookielib.CookieJar, but exposes a dict\n    interface.\n\n    This is the CookieJar we create by default for requests and sessions that\n    don't specify one, since some clients may expect response.cookies and\n    session.cookies to support dict operations.\n\n    Requests does not use the dict interface internally; it's just for\n    compatibility with external client code. All requests code should work\n    out of the box with externally provided instances of ``CookieJar``, e.g.\n    ``LWPCookieJar`` and ``FileCookieJar``.\n\n    Unlike a regular CookieJar, this class is pickleable.\n\n    .. warning:: dictionary operations that are normally O(1) may be O(n).\n    "

        def get(self, name, default=None, domain=None, path=None):
            """Dict-like get() that also supports optional domain and path args in
        order to resolve naming collisions from using one cookie jar over
        multiple domains.

        .. warning:: operation is O(n), not O(1).
        """
            try:
                return self._find_no_duplicatesnamedomainpath
            except KeyError:
                return default

        def set(self, name, value, **kwargs):
            """Dict-like set() that also supports optional domain and path args in
        order to resolve naming collisions from using one cookie jar over
        multiple domains.
        """
            if value is None:
                remove_cookie_by_name(self, name, domain=(kwargs.get('domain')), path=(kwargs.get('path')))
                return
            if isinstance(value, Morsel):
                c = morsel_to_cookie(value)
            else:
                c = create_cookie(name, value, **kwargs)
            self.set_cookie(c)
            return c

        def iterkeys(self):
            """Dict-like iterkeys() that returns an iterator of names of cookies
        from the jar.

        .. seealso:: itervalues() and iteritems().
        """
            for cookie in iter(self):
                yield cookie.name

        def keys(self):
            """Dict-like keys() that returns a list of names of cookies from the
        jar.

        .. seealso:: values() and items().
        """
            return list(self.iterkeys())

        def itervalues(self):
            """Dict-like itervalues() that returns an iterator of values of cookies
        from the jar.

        .. seealso:: iterkeys() and iteritems().
        """
            for cookie in iter(self):
                yield cookie.value

        def values(self):
            """Dict-like values() that returns a list of values of cookies from the
        jar.

        .. seealso:: keys() and items().
        """
            return list(self.itervalues())

        def iteritems(self):
            """Dict-like iteritems() that returns an iterator of name-value tuples
        from the jar.

        .. seealso:: iterkeys() and itervalues().
        """
            for cookie in iter(self):
                yield (
                 cookie.name, cookie.value)

        def items(self):
            """Dict-like items() that returns a list of name-value tuples from the
        jar. Allows client-code to call ``dict(RequestsCookieJar)`` and get a
        vanilla python dict of key value pairs.

        .. seealso:: keys() and values().
        """
            return list(self.iteritems())

        def list_domains(self):
            """Utility method to list all the domains in the jar."""
            domains = []
            for cookie in iter(self):
                if cookie.domain not in domains:
                    domains.append(cookie.domain)
            else:
                return domains

        def list_paths(self):
            """Utility method to list all the paths in the jar."""
            paths = []
            for cookie in iter(self):
                if cookie.path not in paths:
                    paths.append(cookie.path)
            else:
                return paths

        def multiple_domains(self):
            """Returns True if there are multiple domains in the jar.
        Returns False otherwise.

        :rtype: bool
        """
            domains = []
            for cookie in iter(self):
                if cookie.domain is not None:
                    if cookie.domain in domains:
                        return True
                domains.append(cookie.domain)
            else:
                return False

        def get_dict(self, domain=None, path=None):
            """Takes as an argument an optional domain and path and returns a plain
        old Python dict of name-value pairs of cookies that meet the
        requirements.

        :rtype: dict
        """
            dictionary = {}
            for cookie in iter(self):
                if not domain is None:
                    if cookie.domain == domain:
                        pass
                if not path is None:
                    if cookie.path == path:
                        pass
                dictionary[cookie.name] = cookie.value
            else:
                return dictionary

        def __contains__--- This code section failed: ---

 L. 316         0  SETUP_FINALLY        20  'to 20'

 L. 317         2  LOAD_GLOBAL              super
                4  LOAD_GLOBAL              RequestsCookieJar
                6  LOAD_FAST                'self'
                8  CALL_FUNCTION_2       2  ''
               10  LOAD_METHOD              __contains__
               12  LOAD_FAST                'name'
               14  CALL_METHOD_1         1  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 318        20  DUP_TOP          
               22  LOAD_GLOBAL              CookieConflictError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    40  'to 40'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 319        34  POP_EXCEPT       
               36  LOAD_CONST               True
               38  RETURN_VALUE     
             40_0  COME_FROM            26  '26'
               40  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 36

        def __getitem__(self, name):
            """Dict-like __getitem__() for compatibility with client code. Throws
        exception if there are more than one cookie with name. In that case,
        use the more explicit get() method instead.

        .. warning:: operation is O(n), not O(1).
        """
            return self._find_no_duplicates(name)

        def __setitem__(self, name, value):
            """Dict-like __setitem__ for compatibility with client code. Throws
        exception if there is already a cookie of that name in the jar. In that
        case, use the more explicit set() method instead.
        """
            self.set(name, value)

        def __delitem__(self, name):
            """Deletes a cookie given a name. Wraps ``cookielib.CookieJar``'s
        ``remove_cookie_by_name()``.
        """
            remove_cookie_by_name(self, name)

        def set_cookie(self, cookie, *args, **kwargs):
            if hasattr(cookie.value, 'startswith'):
                if cookie.value.startswith('"'):
                    if cookie.value.endswith('"'):
                        cookie.value = cookie.value.replace('\\"', '')
            return (super(RequestsCookieJar, self).set_cookie)(cookie, *args, **kwargs)

        def update(self, other):
            if isinstance(other, cookielib.CookieJar):
                for cookie in other:
                    self.set_cookie(copy.copy(cookie))

            else:
                super(RequestsCookieJar, self).update(other)

        def _find(self, name, domain=None, path=None):
            """Requests uses this method internally to get cookie values.

        If there are conflicting cookies, _find arbitrarily chooses one.
        See _find_no_duplicates if you want an exception thrown if there are
        conflicting cookies.

        :param name: a string containing name of cookie
        :param domain: (optional) string containing domain of cookie
        :param path: (optional) string containing path of cookie
        :return: cookie.value
        """
            for cookie in iter(self):
                if cookie.name == name:
                    if not domain is None:
                        if cookie.domain == domain:
                            pass
                    if not path is None:
                        if cookie.path == path:
                            pass
                    return cookie.value
            else:
                raise KeyError('name=%r, domain=%r, path=%r' % (name, domain, path))

        def _find_no_duplicates(self, name, domain=None, path=None):
            """Both ``__get_item__`` and ``get`` call this function: it's never
        used elsewhere in Requests.

        :param name: a string containing name of cookie
        :param domain: (optional) string containing domain of cookie
        :param path: (optional) string containing path of cookie
        :raises KeyError: if cookie is not found
        :raises CookieConflictError: if there are multiple cookies
            that match name and optionally domain and path
        :return: cookie.value
        """
            toReturn = None
            for cookie in iter(self):
                if cookie.name == name:
                    if not domain is None:
                        if cookie.domain == domain:
                            pass
                    if not path is None:
                        if cookie.path == path:
                            pass
                    if toReturn is not None:
                        raise CookieConflictError('There are multiple cookies with name, %r' % name)
                    else:
                        toReturn = cookie.value
            else:
                if toReturn:
                    return toReturn
                raise KeyError('name=%r, domain=%r, path=%r' % (name, domain, path))

        def __getstate__(self):
            """Unlike a normal CookieJar, this class is pickleable."""
            state = self.__dict__.copy()
            state.pop('_cookies_lock')
            return state

        def __setstate__(self, state):
            """Unlike a normal CookieJar, this class is pickleable."""
            self.__dict__.update(state)
            if '_cookies_lock' not in self.__dict__:
                self._cookies_lock = threading.RLock()

        def copy(self):
            """Return a copy of this RequestsCookieJar."""
            new_cj = RequestsCookieJar()
            new_cj.set_policy(self.get_policy())
            new_cj.update(self)
            return new_cj

        def get_policy(self):
            """Return the CookiePolicy instance used."""
            return self._policy


    def _copy_cookie_jar(jar):
        if jar is None:
            return
        if hasattr(jar, 'copy'):
            return jar.copy()
        new_jar = copy.copy(jar)
        new_jar.clear()
        for cookie in jar:
            new_jar.set_cookie(copy.copy(cookie))
        else:
            return new_jar


    def create_cookie(name, value, **kwargs):
        """Make a cookie from underspecified parameters.

    By default, the pair of `name` and `value` will be set for the domain ''
    and sent on every request (this is sometimes called a "supercookie").
    """
        result = {'version':0, 
         'name':name, 
         'value':value, 
         'port':None, 
         'domain':'', 
         'path':'/', 
         'secure':False, 
         'expires':None, 
         'discard':True, 
         'comment':None, 
         'comment_url':None, 
         'rest':{'HttpOnly': None}, 
         'rfc2109':False}
        badargs = set(kwargs) - set(result)
        if badargs:
            err = 'create_cookie() got unexpected keyword arguments: %s'
            raise TypeError(err % list(badargs))
        result.update(kwargs)
        result['port_specified'] = bool(result['port'])
        result['domain_specified'] = bool(result['domain'])
        result['domain_initial_dot'] = result['domain'].startswith('.')
        result['path_specified'] = bool(result['path'])
        return (cookielib.Cookie)(**result)


    def morsel_to_cookie(morsel):
        """Convert a Morsel object into a Cookie containing the one k/v pair."""
        expires = None
        if morsel['max-age']:
            try:
                expires = int(time.time() + int(morsel['max-age']))
            except ValueError:
                raise TypeError('max-age: %s must be integer' % morsel['max-age'])

        elif morsel['expires']:
            time_template = '%a, %d-%b-%Y %H:%M:%S GMT'
            expires = calendar.timegm(time.strptime(morsel['expires'], time_template))
        return create_cookie(comment=(morsel['comment']),
          comment_url=(bool(morsel['comment'])),
          discard=False,
          domain=(morsel['domain']),
          expires=expires,
          name=(morsel.key),
          path=(morsel['path']),
          port=None,
          rest={'HttpOnly': morsel['httponly']},
          rfc2109=False,
          secure=(bool(morsel['secure'])),
          value=(morsel.value),
          version=(morsel['version'] or 0))


    def cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True):
        """Returns a CookieJar from a key/value dictionary.

    :param cookie_dict: Dict of key/values to insert into CookieJar.
    :param cookiejar: (optional) A cookiejar to add the cookies to.
    :param overwrite: (optional) If False, will not replace cookies
        already in the jar with new ones.
    :rtype: CookieJar
    """
        if cookiejar is None:
            cookiejar = RequestsCookieJar()
        if cookie_dict is not None:
            names_from_jar = [cookie.name for cookie in cookiejar]
            for name in cookie_dict:
                if not overwrite:
                    if name not in names_from_jar:
                        pass
                cookiejar.set_cookie(create_cookie(name, cookie_dict[name]))

            return cookiejar


    def merge_cookies(cookiejar, cookies):
        """Add cookies to cookiejar and returns a merged CookieJar.

    :param cookiejar: CookieJar object to add the cookies to.
    :param cookies: Dictionary or CookieJar object to be added.
    :rtype: CookieJar
    """
        if not isinstance(cookiejar, cookielib.CookieJar):
            raise ValueError('You can only merge into CookieJar')
        if isinstance(cookies, dict):
            cookiejar = cookiejar_from_dict(cookies,
              cookiejar=cookiejar, overwrite=False)
        else:
            pass
        if isinstance(cookies, cookielib.CookieJar):
            try:
                cookiejar.update(cookies)
            except AttributeError:
                for cookie_in_jar in cookies:
                    cookiejar.set_cookie(cookie_in_jar)

            return cookiejar