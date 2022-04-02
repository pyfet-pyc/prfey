# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\sessions.py
"""
requests.session
~~~~~~~~~~~~~~~~

This module provides a Session object to manage and persist settings across
requests (cookies, auth, proxies).

"""
import os
from collections import Mapping
from datetime import datetime
from .auth import _basic_auth_str
from .compat import cookielib, OrderedDict, urljoin, urlparse
from .cookies import cookiejar_from_dict, extract_cookies_to_jar, RequestsCookieJar, merge_cookies
from .models import Request, PreparedRequest, DEFAULT_REDIRECT_LIMIT
from .hooks import default_hooks, dispatch_hook
from .utils import to_key_val_list, default_headers, to_native_string
from .exceptions import TooManyRedirects, InvalidSchema, ChunkedEncodingError, ContentDecodingError
from packages.urllib3._collections import RecentlyUsedContainer
from .structures import CaseInsensitiveDict
from .adapters import HTTPAdapter
from .utils import requote_uri, get_environ_proxies, get_netrc_auth, should_bypass_proxies, get_auth_from_url
from .status_codes import codes
from .models import REDIRECT_STATI
REDIRECT_CACHE_SIZE = 1000

def merge_setting(request_setting, session_setting, dict_class=OrderedDict):
    """
    Determines appropriate setting for a given request, taking into account the
    explicit setting on that request, and the setting in the session. If a
    setting is a dictionary, they will be merged together using `dict_class`
    """
    if session_setting is None:
        return request_setting
    if request_setting is None:
        return session_setting
    if not (isinstance(session_setting, Mapping) and isinstance(request_setting, Mapping)):
        return request_setting
    merged_setting = dict_class(to_key_val_list(session_setting))
    merged_setting.update(to_key_val_list(request_setting))
    for k, v in request_setting.items():
        if v is None:
            del merged_setting[k]
    else:
        merged_setting = dict(((k, v) for k, v in merged_setting.items() if v is not None))
        return merged_setting


def merge_hooks(request_hooks, session_hooks, dict_class=OrderedDict):
    """
    Properly merges both requests and session hooks.

    This is necessary because when request_hooks == {'response': []}, the
    merge breaks Session hooks entirely.
    """
    if session_hooks is None or (session_hooks.get('response') == []):
        return request_hooks
    if request_hooks is None or (request_hooks.get('response') == []):
        return session_hooks
    return merge_setting(request_hooks, session_hooks, dict_class)


class SessionRedirectMixin(object):

    def resolve_redirects--- This code section failed: ---

 L.  96         0  LOAD_CONST               0
                2  STORE_FAST               'i'

 L.  97         4  BUILD_LIST_0          0 
                6  STORE_FAST               'hist'
              8_0  COME_FROM           592  '592'

 L.  99         8  LOAD_FAST                'resp'
               10  LOAD_ATTR                is_redirect
            12_14  POP_JUMP_IF_FALSE   594  'to 594'

 L. 100        16  LOAD_FAST                'req'
               18  LOAD_METHOD              copy
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'prepared_request'

 L. 102        24  LOAD_FAST                'i'
               26  LOAD_CONST               0
               28  COMPARE_OP               >
               30  POP_JUMP_IF_FALSE    56  'to 56'

 L. 104        32  LOAD_FAST                'hist'
               34  LOAD_METHOD              append
               36  LOAD_FAST                'resp'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 105        42  LOAD_GLOBAL              list
               44  LOAD_FAST                'hist'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'new_hist'

 L. 106        50  LOAD_FAST                'new_hist'
               52  LOAD_FAST                'resp'
               54  STORE_ATTR               history
             56_0  COME_FROM            30  '30'

 L. 108        56  SETUP_FINALLY        68  'to 68'

 L. 109        58  LOAD_FAST                'resp'
               60  LOAD_ATTR                content
               62  POP_TOP          
               64  POP_BLOCK        
               66  JUMP_FORWARD        108  'to 108'
             68_0  COME_FROM_FINALLY    56  '56'

 L. 110        68  DUP_TOP          
               70  LOAD_GLOBAL              ChunkedEncodingError
               72  LOAD_GLOBAL              ContentDecodingError
               74  LOAD_GLOBAL              RuntimeError
               76  BUILD_TUPLE_3         3 
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   106  'to 106'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 111        88  LOAD_FAST                'resp'
               90  LOAD_ATTR                raw
               92  LOAD_ATTR                read
               94  LOAD_CONST               False
               96  LOAD_CONST               ('decode_content',)
               98  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              100  POP_TOP          
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            80  '80'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            66  '66'

 L. 113       108  LOAD_FAST                'i'
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                max_redirects
              114  COMPARE_OP               >=
              116  POP_JUMP_IF_FALSE   132  'to 132'

 L. 114       118  LOAD_GLOBAL              TooManyRedirects
              120  LOAD_STR                 'Exceeded %s redirects.'
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                max_redirects
              126  BINARY_MODULO    
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           116  '116'

 L. 117       132  LOAD_FAST                'resp'
              134  LOAD_METHOD              close
              136  CALL_METHOD_0         0  ''
              138  POP_TOP          

 L. 119       140  LOAD_FAST                'resp'
              142  LOAD_ATTR                headers
              144  LOAD_STR                 'location'
              146  BINARY_SUBSCR    
              148  STORE_FAST               'url'

 L. 120       150  LOAD_FAST                'req'
              152  LOAD_ATTR                method
              154  STORE_FAST               'method'

 L. 123       156  LOAD_FAST                'url'
              158  LOAD_METHOD              startswith
              160  LOAD_STR                 '//'
              162  CALL_METHOD_1         1  ''
              164  POP_JUMP_IF_FALSE   190  'to 190'

 L. 124       166  LOAD_GLOBAL              urlparse
              168  LOAD_FAST                'resp'
              170  LOAD_ATTR                url
              172  CALL_FUNCTION_1       1  ''
              174  STORE_FAST               'parsed_rurl'

 L. 125       176  LOAD_STR                 '%s:%s'
              178  LOAD_FAST                'parsed_rurl'
              180  LOAD_ATTR                scheme
              182  LOAD_FAST                'url'
              184  BUILD_TUPLE_2         2 
              186  BINARY_MODULO    
              188  STORE_FAST               'url'
            190_0  COME_FROM           164  '164'

 L. 128       190  LOAD_GLOBAL              urlparse
              192  LOAD_FAST                'url'
              194  CALL_FUNCTION_1       1  ''
              196  STORE_FAST               'parsed'

 L. 129       198  LOAD_FAST                'parsed'
              200  LOAD_METHOD              geturl
              202  CALL_METHOD_0         0  ''
              204  STORE_FAST               'url'

 L. 134       206  LOAD_FAST                'parsed'
              208  LOAD_ATTR                netloc
              210  POP_JUMP_IF_TRUE    230  'to 230'

 L. 135       212  LOAD_GLOBAL              urljoin
              214  LOAD_FAST                'resp'
              216  LOAD_ATTR                url
              218  LOAD_GLOBAL              requote_uri
              220  LOAD_FAST                'url'
              222  CALL_FUNCTION_1       1  ''
              224  CALL_FUNCTION_2       2  ''
              226  STORE_FAST               'url'
              228  JUMP_FORWARD        238  'to 238'
            230_0  COME_FROM           210  '210'

 L. 137       230  LOAD_GLOBAL              requote_uri
              232  LOAD_FAST                'url'
              234  CALL_FUNCTION_1       1  ''
              236  STORE_FAST               'url'
            238_0  COME_FROM           228  '228'

 L. 139       238  LOAD_GLOBAL              to_native_string
              240  LOAD_FAST                'url'
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_FAST                'prepared_request'
              246  STORE_ATTR               url

 L. 141       248  LOAD_FAST                'resp'
              250  LOAD_ATTR                is_permanent_redirect
          252_254  POP_JUMP_IF_FALSE   284  'to 284'
              256  LOAD_FAST                'req'
              258  LOAD_ATTR                url
              260  LOAD_FAST                'prepared_request'
              262  LOAD_ATTR                url
              264  COMPARE_OP               !=
          266_268  POP_JUMP_IF_FALSE   284  'to 284'

 L. 142       270  LOAD_FAST                'prepared_request'
              272  LOAD_ATTR                url
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                redirect_cache
              278  LOAD_FAST                'req'
              280  LOAD_ATTR                url
              282  STORE_SUBSCR     
            284_0  COME_FROM           266  '266'
            284_1  COME_FROM           252  '252'

 L. 145       284  LOAD_FAST                'resp'
              286  LOAD_ATTR                status_code
              288  LOAD_GLOBAL              codes
              290  LOAD_ATTR                see_other
              292  COMPARE_OP               ==
          294_296  POP_JUMP_IF_FALSE   312  'to 312'

 L. 146       298  LOAD_FAST                'method'
              300  LOAD_STR                 'HEAD'
              302  COMPARE_OP               !=

 L. 145   304_306  POP_JUMP_IF_FALSE   312  'to 312'

 L. 147       308  LOAD_STR                 'GET'
              310  STORE_FAST               'method'
            312_0  COME_FROM           304  '304'
            312_1  COME_FROM           294  '294'

 L. 151       312  LOAD_FAST                'resp'
              314  LOAD_ATTR                status_code
              316  LOAD_GLOBAL              codes
              318  LOAD_ATTR                found
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_FALSE   340  'to 340'
              326  LOAD_FAST                'method'
              328  LOAD_STR                 'HEAD'
              330  COMPARE_OP               !=
          332_334  POP_JUMP_IF_FALSE   340  'to 340'

 L. 152       336  LOAD_STR                 'GET'
              338  STORE_FAST               'method'
            340_0  COME_FROM           332  '332'
            340_1  COME_FROM           322  '322'

 L. 156       340  LOAD_FAST                'resp'
              342  LOAD_ATTR                status_code
              344  LOAD_GLOBAL              codes
              346  LOAD_ATTR                moved
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   368  'to 368'
              354  LOAD_FAST                'method'
              356  LOAD_STR                 'POST'
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_FALSE   368  'to 368'

 L. 157       364  LOAD_STR                 'GET'
              366  STORE_FAST               'method'
            368_0  COME_FROM           360  '360'
            368_1  COME_FROM           350  '350'

 L. 159       368  LOAD_FAST                'method'
              370  LOAD_FAST                'prepared_request'
              372  STORE_ATTR               method

 L. 162       374  LOAD_FAST                'resp'
              376  LOAD_ATTR                status_code
              378  LOAD_GLOBAL              codes
              380  LOAD_ATTR                temporary_redirect
              382  LOAD_GLOBAL              codes
              384  LOAD_ATTR                permanent_redirect
              386  BUILD_TUPLE_2         2 
              388  COMPARE_OP               not-in
          390_392  POP_JUMP_IF_FALSE   420  'to 420'

 L. 163       394  LOAD_STR                 'Content-Length'
              396  LOAD_FAST                'prepared_request'
              398  LOAD_ATTR                headers
              400  COMPARE_OP               in
          402_404  POP_JUMP_IF_FALSE   414  'to 414'

 L. 164       406  LOAD_FAST                'prepared_request'
              408  LOAD_ATTR                headers
              410  LOAD_STR                 'Content-Length'
              412  DELETE_SUBSCR    
            414_0  COME_FROM           402  '402'

 L. 166       414  LOAD_CONST               None
              416  LOAD_FAST                'prepared_request'
              418  STORE_ATTR               body
            420_0  COME_FROM           390  '390'

 L. 168       420  LOAD_FAST                'prepared_request'
              422  LOAD_ATTR                headers
              424  STORE_FAST               'headers'

 L. 169       426  SETUP_FINALLY       438  'to 438'

 L. 170       428  LOAD_FAST                'headers'
              430  LOAD_STR                 'Cookie'
              432  DELETE_SUBSCR    
              434  POP_BLOCK        
              436  JUMP_FORWARD        460  'to 460'
            438_0  COME_FROM_FINALLY   426  '426'

 L. 171       438  DUP_TOP          
              440  LOAD_GLOBAL              KeyError
              442  COMPARE_OP               exception-match
          444_446  POP_JUMP_IF_FALSE   458  'to 458'
              448  POP_TOP          
              450  POP_TOP          
              452  POP_TOP          

 L. 172       454  POP_EXCEPT       
              456  BREAK_LOOP          460  'to 460'
            458_0  COME_FROM           444  '444'
              458  END_FINALLY      
            460_0  COME_FROM           456  '456'
            460_1  COME_FROM           436  '436'

 L. 177       460  LOAD_GLOBAL              extract_cookies_to_jar
              462  LOAD_FAST                'prepared_request'
              464  LOAD_ATTR                _cookies
              466  LOAD_FAST                'req'
              468  LOAD_FAST                'resp'
              470  LOAD_ATTR                raw
              472  CALL_FUNCTION_3       3  ''
              474  POP_TOP          

 L. 178       476  LOAD_FAST                'prepared_request'
              478  LOAD_ATTR                _cookies
              480  LOAD_METHOD              update
              482  LOAD_FAST                'self'
              484  LOAD_ATTR                cookies
              486  CALL_METHOD_1         1  ''
              488  POP_TOP          

 L. 179       490  LOAD_FAST                'prepared_request'
              492  LOAD_METHOD              prepare_cookies
              494  LOAD_FAST                'prepared_request'
              496  LOAD_ATTR                _cookies
              498  CALL_METHOD_1         1  ''
              500  POP_TOP          

 L. 182       502  LOAD_FAST                'self'
              504  LOAD_METHOD              rebuild_proxies
              506  LOAD_FAST                'prepared_request'
              508  LOAD_FAST                'proxies'
              510  CALL_METHOD_2         2  ''
              512  STORE_FAST               'proxies'

 L. 183       514  LOAD_FAST                'self'
              516  LOAD_METHOD              rebuild_auth
              518  LOAD_FAST                'prepared_request'
              520  LOAD_FAST                'resp'
              522  CALL_METHOD_2         2  ''
              524  POP_TOP          

 L. 186       526  LOAD_FAST                'prepared_request'
              528  STORE_FAST               'req'

 L. 188       530  LOAD_FAST                'self'
              532  LOAD_ATTR                send

 L. 189       534  LOAD_FAST                'req'

 L. 188       536  BUILD_TUPLE_1         1 

 L. 190       538  LOAD_FAST                'stream'

 L. 191       540  LOAD_FAST                'timeout'

 L. 192       542  LOAD_FAST                'verify'

 L. 193       544  LOAD_FAST                'cert'

 L. 194       546  LOAD_FAST                'proxies'

 L. 195       548  LOAD_CONST               False

 L. 188       550  LOAD_CONST               ('stream', 'timeout', 'verify', 'cert', 'proxies', 'allow_redirects')
              552  BUILD_CONST_KEY_MAP_6     6 

 L. 196       554  LOAD_FAST                'adapter_kwargs'

 L. 188       556  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              558  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              560  STORE_FAST               'resp'

 L. 199       562  LOAD_GLOBAL              extract_cookies_to_jar
              564  LOAD_FAST                'self'
              566  LOAD_ATTR                cookies
              568  LOAD_FAST                'prepared_request'
              570  LOAD_FAST                'resp'
              572  LOAD_ATTR                raw
              574  CALL_FUNCTION_3       3  ''
              576  POP_TOP          

 L. 201       578  LOAD_FAST                'i'
              580  LOAD_CONST               1
              582  INPLACE_ADD      
              584  STORE_FAST               'i'

 L. 202       586  LOAD_FAST                'resp'
              588  YIELD_VALUE      
              590  POP_TOP          
              592  JUMP_BACK             8  'to 8'
            594_0  COME_FROM            12  '12'

Parse error at or near `END_FINALLY' instruction at offset 458

    def rebuild_auth(self, prepared_request, response):
        """
        When being redirected we may want to strip authentication from the
        request to avoid leaking credentials. This method intelligently removes
        and reapplies authentication where possible to avoid credential loss.
        """
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = urlparse(response.request.url)
            redirect_parsed = urlparse(url)
            if original_parsed.hostname != redirect_parsed.hostname:
                del headers['Authorization']
        new_auth = get_netrc_auth(url) if self.trust_env else None
        if new_auth is not None:
            prepared_request.prepare_auth(new_auth)

    def rebuild_proxies(self, prepared_request, proxies):
        """
        This method re-evaluates the proxy configuration by considering the
        environment variables. If we are redirected to a URL covered by
        NO_PROXY, we strip the proxy configuration. Otherwise, we set missing
        proxy keys for this URL (in case they were stripped by a previous
        redirect).

        This method also replaces the Proxy-Authorization header where
        necessary.
        """
        headers = prepared_request.headers
        url = prepared_request.url
        scheme = urlparse(url).scheme
        new_proxies = proxies.copy() if proxies is not None else {}
        if self.trust_env:
            if not should_bypass_proxies(url):
                environ_proxies = get_environ_proxies(url)
                proxy = environ_proxies.get(scheme)
                if proxy:
                    new_proxies.setdefaultschemeenviron_proxies[scheme]
            if 'Proxy-Authorization' in headers:
                del headers['Proxy-Authorization']
        try:
            username, password = get_auth_from_url(new_proxies[scheme])
        except KeyError:
            username, password = (None, None)
        else:
            if username:
                if password:
                    headers['Proxy-Authorization'] = _basic_auth_str(username, password)
            return new_proxies


class Session(SessionRedirectMixin):
    __doc__ = "A Requests session.\n\n    Provides cookie persistence, connection-pooling, and configuration.\n\n    Basic Usage::\n\n      >>> import requests\n      >>> s = requests.Session()\n      >>> s.get('http://httpbin.org/get')\n      200\n    "
    __attrs__ = [
     'headers', 'cookies', 'auth', 'proxies', 'hooks', 'params', 'verify',
     'cert', 'prefetch', 'adapters', 'stream', 'trust_env',
     'max_redirects']

    def __init__(self):
        self.headers = default_headers()
        self.auth = None
        self.proxies = {}
        self.hooks = default_hooks()
        self.params = {}
        self.stream = False
        self.verify = True
        self.cert = None
        self.max_redirects = DEFAULT_REDIRECT_LIMIT
        self.trust_env = True
        self.cookies = cookiejar_from_dict({})
        self.adapters = OrderedDict()
        self.mount'https://'HTTPAdapter()
        self.mount'http://'HTTPAdapter()
        self.redirect_cache = RecentlyUsedContainer(REDIRECT_CACHE_SIZE)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def prepare_request(self, request):
        """Constructs a :class:`PreparedRequest <PreparedRequest>` for
        transmission and returns it. The :class:`PreparedRequest` has settings
        merged from the :class:`Request <Request>` instance and those of the
        :class:`Session`.

        :param request: :class:`Request` instance to prepare with this
            session's settings.
        """
        cookies = request.cookies or {}
        if not isinstance(cookies, cookielib.CookieJar):
            cookies = cookiejar_from_dict(cookies)
        merged_cookies = merge_cookies(merge_cookies(RequestsCookieJar(), self.cookies), cookies)
        auth = request.auth
        if self.trust_env:
            if not auth:
                if not self.auth:
                    auth = get_netrc_auth(request.url)
            p = PreparedRequest()
            p.prepare(method=(request.method.upper()),
              url=(request.url),
              files=(request.files),
              data=(request.data),
              json=(request.json),
              headers=merge_setting((request.headers), (self.headers), dict_class=CaseInsensitiveDict),
              params=(merge_setting(request.params, self.params)),
              auth=(merge_setting(auth, self.auth)),
              cookies=merged_cookies,
              hooks=(merge_hooks(request.hooks, self.hooks)))
            return p

    def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary or bytes to send in the body of the
            :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a (`connect timeout, read
            timeout <user/advanced.html#timeouts>`_) tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol to the URL of
            the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) if ``True``, the SSL cert will be verified.
            A CA_BUNDLE path can also be provided.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        """
        method = to_native_string(method)
        req = Request(method=(method.upper()),
          url=url,
          headers=headers,
          files=files,
          data=(data or {}),
          json=json,
          params=(params or {}),
          auth=auth,
          cookies=cookies,
          hooks=hooks)
        prep = self.prepare_request(req)
        proxies = proxies or {}
        settings = self.merge_environment_settings(prep.url, proxies, stream, verify, cert)
        send_kwargs = {'timeout':timeout, 
         'allow_redirects':allow_redirects}
        send_kwargs.update(settings)
        resp = (self.send)(prep, **send_kwargs)
        return resp

    def get(self, url, **kwargs):
        r"""Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """
        kwargs.setdefault'allow_redirects'True
        return (self.request)('GET', url, **kwargs)

    def options(self, url, **kwargs):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """
        kwargs.setdefault'allow_redirects'True
        return (self.request)('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """
        kwargs.setdefault'allow_redirects'False
        return (self.request)('HEAD', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """
        return (self.request)('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """
        return (self.request)('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """
        return (self.request)('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """
        return (self.request)('DELETE', url, **kwargs)

    def send(self, request, **kwargs):
        """Send a given PreparedRequest."""
        kwargs.setdefault'stream'self.stream
        kwargs.setdefault'verify'self.verify
        kwargs.setdefault'cert'self.cert
        kwargs.setdefault'proxies'self.proxies
        if not isinstance(request, PreparedRequest):
            raise ValueError('You can only send PreparedRequests.')
        checked_urls = set()
        while True:
            if request.url in self.redirect_cache:
                checked_urls.add(request.url)
                new_url = self.redirect_cache.get(request.url)
                if new_url in checked_urls:
                    pass
                else:
                    request.url = new_url

        allow_redirects = kwargs.pop'allow_redirects'True
        stream = kwargs.get('stream')
        hooks = request.hooks
        adapter = self.get_adapter(url=(request.url))
        start = datetime.utcnow()
        r = (adapter.send)(request, **kwargs)
        r.elapsed = datetime.utcnow() - start
        r = dispatch_hook('response', hooks, r, **kwargs)
        if r.history:
            for resp in r.history:
                extract_cookies_to_jar(self.cookies, resp.request, resp.raw)
            else:
                extract_cookies_to_jar(self.cookies, request, r.raw)
                gen = (self.resolve_redirects)(r, request, **kwargs)
                history = [resp for resp in gen] if allow_redirects else []
                if history:
                    history.insert0r
                    r = history.pop()
                    r.history = history
                if not stream:
                    r.content

            return r

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        """Check the environment and merge it with some settings."""
        if self.trust_env:
            env_proxies = get_environ_proxies(url) or {}
            for k, v in env_proxies.items():
                proxies.setdefaultkv
            else:
                if verify is True or (verify is None):
                    verify = os.environ.get('REQUESTS_CA_BUNDLE') or os.environ.get('CURL_CA_BUNDLE')
                proxies = merge_setting(proxies, self.proxies)
                stream = merge_setting(stream, self.stream)
                verify = merge_setting(verify, self.verify)
                cert = merge_setting(cert, self.cert)

            return {'verify':verify, 
             'proxies':proxies,  'stream':stream,  'cert':cert}

    def get_adapter(self, url):
        """Returns the appropriate connnection adapter for the given URL."""
        for prefix, adapter in self.adapters.items():
            if url.lower().startswith(prefix):
                return adapter
        else:
            raise InvalidSchema("No connection adapters were found for '%s'" % url)

    def close(self):
        """Closes all adapters and as such the session"""
        for v in self.adapters.values():
            v.close()

    def mount(self, prefix, adapter):
        """Registers a connection adapter to a prefix.

        Adapters are sorted in descending order by key length."""
        self.adapters[prefix] = adapter
        keys_to_move = [k for k in self.adapters if len(k) < len(prefix)]
        for key in keys_to_move:
            self.adapters[key] = self.adapters.pop(key)

    def __getstate__(self):
        state = dict(((attr, getattr(self, attr, None)) for attr in self.__attrs__))
        state['redirect_cache'] = dict(self.redirect_cache)
        return state

    def __setstate__(self, state):
        redirect_cache = state.pop'redirect_cache'{}
        for attr, value in state.items():
            setattr(self, attr, value)
        else:
            self.redirect_cache = RecentlyUsedContainer(REDIRECT_CACHE_SIZE)
            for redirect, to in redirect_cache.items():
                self.redirect_cache[redirect] = to


def session():
    """Returns a :class:`Session` for context-management."""
    return Session()