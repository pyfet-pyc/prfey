# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: requests\sessions.py
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
from ._internal_utils import to_native_string
from .utils import to_key_val_list, default_headers
from .exceptions import TooManyRedirects, InvalidSchema, ChunkedEncodingError, ContentDecodingError
from packages.urllib3._collections import RecentlyUsedContainer
from .structures import CaseInsensitiveDict
from .adapters import HTTPAdapter
from .utils import requote_uri, get_environ_proxies, get_netrc_auth, should_bypass_proxies, get_auth_from_url, rewind_body
from .status_codes import codes
from .models import REDIRECT_STATI
REDIRECT_CACHE_SIZE = 1000

def merge_setting(request_setting, session_setting, dict_class=OrderedDict):
    """Determines appropriate setting for a given request, taking into account
    the explicit setting on that request, and the setting in the session. If a
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
    none_keys = [k for k, v in merged_setting.items() if v is None]
    for key in none_keys:
        del merged_setting[key]
    else:
        return merged_setting


def merge_hooks(request_hooks, session_hooks, dict_class=OrderedDict):
    """Properly merges both requests and session hooks.

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

 L.  93         0  LOAD_CONST               0
                2  STORE_FAST               'i'

 L.  94         4  BUILD_LIST_0          0 
                6  STORE_FAST               'hist'
              8_0  COME_FROM           566  '566'

 L.  96         8  LOAD_FAST                'resp'
               10  LOAD_ATTR                is_redirect
            12_14  POP_JUMP_IF_FALSE   568  'to 568'

 L.  97        16  LOAD_FAST                'req'
               18  LOAD_METHOD              copy
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'prepared_request'

 L.  99        24  LOAD_FAST                'i'
               26  LOAD_CONST               0
               28  COMPARE_OP               >
               30  POP_JUMP_IF_FALSE    56  'to 56'

 L. 101        32  LOAD_FAST                'hist'
               34  LOAD_METHOD              append
               36  LOAD_FAST                'resp'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 102        42  LOAD_GLOBAL              list
               44  LOAD_FAST                'hist'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'new_hist'

 L. 103        50  LOAD_FAST                'new_hist'
               52  LOAD_FAST                'resp'
               54  STORE_ATTR               history
             56_0  COME_FROM            30  '30'

 L. 105        56  SETUP_FINALLY        68  'to 68'

 L. 106        58  LOAD_FAST                'resp'
               60  LOAD_ATTR                content
               62  POP_TOP          
               64  POP_BLOCK        
               66  JUMP_FORWARD        108  'to 108'
             68_0  COME_FROM_FINALLY    56  '56'

 L. 107        68  DUP_TOP          
               70  LOAD_GLOBAL              ChunkedEncodingError
               72  LOAD_GLOBAL              ContentDecodingError
               74  LOAD_GLOBAL              RuntimeError
               76  BUILD_TUPLE_3         3 
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   106  'to 106'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 108        88  LOAD_FAST                'resp'
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

 L. 110       108  LOAD_FAST                'i'
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                max_redirects
              114  COMPARE_OP               >=
              116  POP_JUMP_IF_FALSE   136  'to 136'

 L. 111       118  LOAD_GLOBAL              TooManyRedirects
              120  LOAD_STR                 'Exceeded %s redirects.'
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                max_redirects
              126  BINARY_MODULO    
              128  LOAD_FAST                'resp'
              130  LOAD_CONST               ('response',)
              132  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           116  '116'

 L. 114       136  LOAD_FAST                'resp'
              138  LOAD_METHOD              close
              140  CALL_METHOD_0         0  ''
              142  POP_TOP          

 L. 116       144  LOAD_FAST                'resp'
              146  LOAD_ATTR                headers
              148  LOAD_STR                 'location'
              150  BINARY_SUBSCR    
              152  STORE_FAST               'url'

 L. 119       154  LOAD_FAST                'url'
              156  LOAD_METHOD              startswith
              158  LOAD_STR                 '//'
              160  CALL_METHOD_1         1  ''
              162  POP_JUMP_IF_FALSE   188  'to 188'

 L. 120       164  LOAD_GLOBAL              urlparse
              166  LOAD_FAST                'resp'
              168  LOAD_ATTR                url
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               'parsed_rurl'

 L. 121       174  LOAD_STR                 '%s:%s'
              176  LOAD_FAST                'parsed_rurl'
              178  LOAD_ATTR                scheme
              180  LOAD_FAST                'url'
              182  BUILD_TUPLE_2         2 
              184  BINARY_MODULO    
              186  STORE_FAST               'url'
            188_0  COME_FROM           162  '162'

 L. 124       188  LOAD_GLOBAL              urlparse
              190  LOAD_FAST                'url'
              192  CALL_FUNCTION_1       1  ''
              194  STORE_FAST               'parsed'

 L. 125       196  LOAD_FAST                'parsed'
              198  LOAD_METHOD              geturl
              200  CALL_METHOD_0         0  ''
              202  STORE_FAST               'url'

 L. 130       204  LOAD_FAST                'parsed'
              206  LOAD_ATTR                netloc
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 131       210  LOAD_GLOBAL              urljoin
              212  LOAD_FAST                'resp'
              214  LOAD_ATTR                url
              216  LOAD_GLOBAL              requote_uri
              218  LOAD_FAST                'url'
              220  CALL_FUNCTION_1       1  ''
              222  CALL_FUNCTION_2       2  ''
              224  STORE_FAST               'url'
              226  JUMP_FORWARD        236  'to 236'
            228_0  COME_FROM           208  '208'

 L. 133       228  LOAD_GLOBAL              requote_uri
              230  LOAD_FAST                'url'
              232  CALL_FUNCTION_1       1  ''
              234  STORE_FAST               'url'
            236_0  COME_FROM           226  '226'

 L. 135       236  LOAD_GLOBAL              to_native_string
              238  LOAD_FAST                'url'
              240  CALL_FUNCTION_1       1  ''
              242  LOAD_FAST                'prepared_request'
              244  STORE_ATTR               url

 L. 137       246  LOAD_FAST                'resp'
              248  LOAD_ATTR                is_permanent_redirect
          250_252  POP_JUMP_IF_FALSE   282  'to 282'
              254  LOAD_FAST                'req'
              256  LOAD_ATTR                url
              258  LOAD_FAST                'prepared_request'
              260  LOAD_ATTR                url
              262  COMPARE_OP               !=
          264_266  POP_JUMP_IF_FALSE   282  'to 282'

 L. 138       268  LOAD_FAST                'prepared_request'
              270  LOAD_ATTR                url
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                redirect_cache
              276  LOAD_FAST                'req'
              278  LOAD_ATTR                url
              280  STORE_SUBSCR     
            282_0  COME_FROM           264  '264'
            282_1  COME_FROM           250  '250'

 L. 140       282  LOAD_FAST                'self'
              284  LOAD_METHOD              rebuild_method
              286  LOAD_FAST                'prepared_request'
              288  LOAD_FAST                'resp'
              290  CALL_METHOD_2         2  ''
              292  POP_TOP          

 L. 143       294  LOAD_FAST                'resp'
              296  LOAD_ATTR                status_code
              298  LOAD_GLOBAL              codes
              300  LOAD_ATTR                temporary_redirect
              302  LOAD_GLOBAL              codes
              304  LOAD_ATTR                permanent_redirect
              306  BUILD_TUPLE_2         2 
              308  COMPARE_OP               not-in
          310_312  POP_JUMP_IF_FALSE   350  'to 350'

 L. 145       314  LOAD_CONST               ('Content-Length', 'Content-Type', 'Transfer-Encoding')
              316  STORE_FAST               'purged_headers'

 L. 146       318  LOAD_FAST                'purged_headers'
              320  GET_ITER         
            322_0  COME_FROM           340  '340'
              322  FOR_ITER            344  'to 344'
              324  STORE_FAST               'header'

 L. 147       326  LOAD_FAST                'prepared_request'
              328  LOAD_ATTR                headers
              330  LOAD_METHOD              pop
              332  LOAD_FAST                'header'
              334  LOAD_CONST               None
              336  CALL_METHOD_2         2  ''
              338  POP_TOP          
          340_342  JUMP_BACK           322  'to 322'
            344_0  COME_FROM           322  '322'

 L. 148       344  LOAD_CONST               None
              346  LOAD_FAST                'prepared_request'
              348  STORE_ATTR               body
            350_0  COME_FROM           310  '310'

 L. 150       350  LOAD_FAST                'prepared_request'
              352  LOAD_ATTR                headers
              354  STORE_FAST               'headers'

 L. 151       356  SETUP_FINALLY       368  'to 368'

 L. 152       358  LOAD_FAST                'headers'
              360  LOAD_STR                 'Cookie'
              362  DELETE_SUBSCR    
              364  POP_BLOCK        
              366  JUMP_FORWARD        390  'to 390'
            368_0  COME_FROM_FINALLY   356  '356'

 L. 153       368  DUP_TOP          
              370  LOAD_GLOBAL              KeyError
              372  COMPARE_OP               exception-match
          374_376  POP_JUMP_IF_FALSE   388  'to 388'
              378  POP_TOP          
              380  POP_TOP          
              382  POP_TOP          

 L. 154       384  POP_EXCEPT       
              386  BREAK_LOOP          390  'to 390'
            388_0  COME_FROM           374  '374'
              388  END_FINALLY      
            390_0  COME_FROM           386  '386'
            390_1  COME_FROM           366  '366'

 L. 159       390  LOAD_GLOBAL              extract_cookies_to_jar
              392  LOAD_FAST                'prepared_request'
              394  LOAD_ATTR                _cookies
              396  LOAD_FAST                'req'
              398  LOAD_FAST                'resp'
              400  LOAD_ATTR                raw
              402  CALL_FUNCTION_3       3  ''
              404  POP_TOP          

 L. 160       406  LOAD_GLOBAL              merge_cookies
              408  LOAD_FAST                'prepared_request'
              410  LOAD_ATTR                _cookies
              412  LOAD_FAST                'self'
              414  LOAD_ATTR                cookies
              416  CALL_FUNCTION_2       2  ''
              418  POP_TOP          

 L. 161       420  LOAD_FAST                'prepared_request'
              422  LOAD_METHOD              prepare_cookies
              424  LOAD_FAST                'prepared_request'
              426  LOAD_ATTR                _cookies
              428  CALL_METHOD_1         1  ''
              430  POP_TOP          

 L. 164       432  LOAD_FAST                'self'
              434  LOAD_METHOD              rebuild_proxies
              436  LOAD_FAST                'prepared_request'
              438  LOAD_FAST                'proxies'
              440  CALL_METHOD_2         2  ''
              442  STORE_FAST               'proxies'

 L. 165       444  LOAD_FAST                'self'
              446  LOAD_METHOD              rebuild_auth
              448  LOAD_FAST                'prepared_request'
              450  LOAD_FAST                'resp'
              452  CALL_METHOD_2         2  ''
              454  POP_TOP          

 L. 171       456  LOAD_FAST                'prepared_request'
              458  LOAD_ATTR                _body_position
              460  LOAD_CONST               None
              462  COMPARE_OP               is-not
          464_466  JUMP_IF_FALSE_OR_POP   484  'to 484'

 L. 172       468  LOAD_STR                 'Content-Length'
              470  LOAD_FAST                'headers'
              472  COMPARE_OP               in
          474_476  JUMP_IF_TRUE_OR_POP   484  'to 484'
              478  LOAD_STR                 'Transfer-Encoding'
              480  LOAD_FAST                'headers'
              482  COMPARE_OP               in
            484_0  COME_FROM           474  '474'
            484_1  COME_FROM           464  '464'

 L. 170       484  STORE_FAST               'rewindable'

 L. 176       486  LOAD_FAST                'rewindable'
          488_490  POP_JUMP_IF_FALSE   500  'to 500'

 L. 177       492  LOAD_GLOBAL              rewind_body
              494  LOAD_FAST                'prepared_request'
              496  CALL_FUNCTION_1       1  ''
              498  POP_TOP          
            500_0  COME_FROM           488  '488'

 L. 180       500  LOAD_FAST                'prepared_request'
              502  STORE_FAST               'req'

 L. 182       504  LOAD_FAST                'self'
              506  LOAD_ATTR                send

 L. 183       508  LOAD_FAST                'req'

 L. 182       510  BUILD_TUPLE_1         1 

 L. 184       512  LOAD_FAST                'stream'

 L. 185       514  LOAD_FAST                'timeout'

 L. 186       516  LOAD_FAST                'verify'

 L. 187       518  LOAD_FAST                'cert'

 L. 188       520  LOAD_FAST                'proxies'

 L. 189       522  LOAD_CONST               False

 L. 182       524  LOAD_CONST               ('stream', 'timeout', 'verify', 'cert', 'proxies', 'allow_redirects')
              526  BUILD_CONST_KEY_MAP_6     6 

 L. 190       528  LOAD_FAST                'adapter_kwargs'

 L. 182       530  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              532  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              534  STORE_FAST               'resp'

 L. 193       536  LOAD_GLOBAL              extract_cookies_to_jar
              538  LOAD_FAST                'self'
              540  LOAD_ATTR                cookies
              542  LOAD_FAST                'prepared_request'
              544  LOAD_FAST                'resp'
              546  LOAD_ATTR                raw
              548  CALL_FUNCTION_3       3  ''
              550  POP_TOP          

 L. 195       552  LOAD_FAST                'i'
              554  LOAD_CONST               1
              556  INPLACE_ADD      
              558  STORE_FAST               'i'

 L. 196       560  LOAD_FAST                'resp'
              562  YIELD_VALUE      
              564  POP_TOP          
              566  JUMP_BACK             8  'to 8'
            568_0  COME_FROM            12  '12'

Parse error at or near `END_FINALLY' instruction at offset 388

    def rebuild_auth(self, prepared_request, response):
        """When being redirected we may want to strip authentication from the
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
        """This method re-evaluates the proxy configuration by considering the
        environment variables. If we are redirected to a URL covered by
        NO_PROXY, we strip the proxy configuration. Otherwise, we set missing
        proxy keys for this URL (in case they were stripped by a previous
        redirect).

        This method also replaces the Proxy-Authorization header where
        necessary.

        :rtype: dict
        """
        headers = prepared_request.headers
        url = prepared_request.url
        scheme = urlparse(url).scheme
        new_proxies = proxies.copy() if proxies is not None else {}
        if self.trust_env:
            if not should_bypass_proxies(url):
                environ_proxies = get_environ_proxies(url)
                proxy = environ_proxies.getschemeenviron_proxies.get('all')
                if proxy:
                    new_proxies.setdefaultschemeproxy
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

    def rebuild_method(self, prepared_request, response):
        """When being redirected we may want to change the method of the request
        based on certain specs or browser behavior.
        """
        method = prepared_request.method
        if response.status_code == codes.see_other:
            if method != 'HEAD':
                method = 'GET'
        if response.status_code == codes.found:
            if method != 'HEAD':
                method = 'GET'
        if response.status_code == codes.moved:
            if method == 'POST':
                method = 'GET'
        prepared_request.method = method


class Session(SessionRedirectMixin):
    __doc__ = "A Requests session.\n\n    Provides cookie persistence, connection-pooling, and configuration.\n\n    Basic Usage::\n\n      >>> import requests\n      >>> s = requests.Session()\n      >>> s.get('http://httpbin.org/get')\n      <Response [200]>\n\n    Or as a context manager::\n\n      >>> with requests.Session() as s:\n      >>>     s.get('http://httpbin.org/get')\n      <Response [200]>\n    "
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
        :rtype: requests.PreparedRequest
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
        :param data: (optional) Dictionary, bytes, or file-like object to send
            in the body of the :class:`Request`.
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
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) whether the SSL cert will be verified.
            A CA_BUNDLE path can also be provided. Defaults to ``True``.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :rtype: requests.Response
        """
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
        :rtype: requests.Response
        """
        kwargs.setdefault'allow_redirects'True
        return (self.request)('GET', url, **kwargs)

    def options(self, url, **kwargs):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault'allow_redirects'True
        return (self.request)('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault'allow_redirects'False
        return (self.request)('HEAD', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return (self.request)('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return (self.request)('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return (self.request)('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return (self.request)('DELETE', url, **kwargs)

    def send(self, request, **kwargs):
        """
        Send a given PreparedRequest.

        :rtype: requests.Response
        """
        kwargs.setdefault'stream'self.stream
        kwargs.setdefault'verify'self.verify
        kwargs.setdefault'cert'self.cert
        kwargs.setdefault'proxies'self.proxies
        if isinstance(request, Request):
            raise ValueError('You can only send PreparedRequests.')
        allow_redirects = kwargs.pop'allow_redirects'True
        stream = kwargs.get('stream')
        hooks = request.hooks
        if allow_redirects:
            checked_urls = set()
            while True:
                if request.url in self.redirect_cache:
                    checked_urls.add(request.url)
                    new_url = self.redirect_cache.get(request.url)
                    if new_url in checked_urls:
                        pass
                    else:
                        request.url = new_url

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
                    stream or r.content

            return r

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        """
        Check the environment and merge it with some settings.

        :rtype: dict
        """
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
        """
        Returns the appropriate connection adapter for the given URL.

        :rtype: requests.adapters.BaseAdapter
        """
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

        Adapters are sorted in descending order by key length.
        """
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
    """
    Returns a :class:`Session` for context-management.

    :rtype: Session
    """
    return Session()