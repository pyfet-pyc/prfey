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
import os, sys, time
from datetime import timedelta
from .auth import _basic_auth_str
from .compat import cookielib, is_py3, OrderedDict, urljoin, urlparse, Mapping
from .cookies import cookiejar_from_dict, extract_cookies_to_jar, RequestsCookieJar, merge_cookies
from .models import Request, PreparedRequest, DEFAULT_REDIRECT_LIMIT
from .hooks import default_hooks, dispatch_hook
from ._internal_utils import to_native_string
from .utils import to_key_val_list, default_headers, DEFAULT_PORTS
from .exceptions import TooManyRedirects, InvalidSchema, ChunkedEncodingError, ContentDecodingError
from .structures import CaseInsensitiveDict
from .adapters import HTTPAdapter
from .utils import requote_uri, get_environ_proxies, get_netrc_auth, should_bypass_proxies, get_auth_from_url, rewind_body
from .status_codes import codes
from .models import REDIRECT_STATI
if sys.platform == 'win32':
    try:
        preferred_clock = time.perf_counter
    except AttributeError:
        preferred_clock = time.clock

else:
    preferred_clock = time.time

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

    def get_redirect_target(self, resp):
        """Receives a Response. Returns a redirect URI or ``None``"""
        if resp.is_redirect:
            location = resp.headers['location']
            if is_py3:
                location = location.encode('latin1')
            return to_native_string(location, 'utf8')

    def should_strip_auth(self, old_url, new_url):
        """Decide whether Authorization header should be removed when redirecting"""
        old_parsed = urlparse(old_url)
        new_parsed = urlparse(new_url)
        if old_parsed.hostname != new_parsed.hostname:
            return True
        if old_parsed.scheme == 'http':
            if old_parsed.port in (80, None):
                if new_parsed.scheme == 'https':
                    if new_parsed.port in (443, None):
                        return False
        changed_port = old_parsed.port != new_parsed.port
        changed_scheme = old_parsed.scheme != new_parsed.scheme
        default_port = (DEFAULT_PORTS.get(old_parsed.scheme, None), None)
        if not changed_scheme:
            if old_parsed.port in default_port:
                if new_parsed.port in default_port:
                    return False
        return changed_port or changed_scheme

    def resolve_redirects--- This code section failed: ---

 L. 147         0  BUILD_LIST_0          0 
                2  STORE_FAST               'hist'

 L. 149         4  LOAD_FAST                'self'
                6  LOAD_METHOD              get_redirect_target
                8  LOAD_FAST                'resp'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'url'

 L. 150        14  LOAD_GLOBAL              urlparse
               16  LOAD_FAST                'req'
               18  LOAD_ATTR                url
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_ATTR                fragment
               24  STORE_FAST               'previous_fragment'
             26_0  COME_FROM           596  '596'
             26_1  COME_FROM           530  '530'

 L. 151        26  LOAD_FAST                'url'
            28_30  POP_JUMP_IF_FALSE   598  'to 598'

 L. 152        32  LOAD_FAST                'req'
               34  LOAD_METHOD              copy
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'prepared_request'

 L. 156        40  LOAD_FAST                'hist'
               42  LOAD_METHOD              append
               44  LOAD_FAST                'resp'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 157        50  LOAD_FAST                'hist'
               52  LOAD_CONST               1
               54  LOAD_CONST               None
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  LOAD_FAST                'resp'
               62  STORE_ATTR               history

 L. 159        64  SETUP_FINALLY        76  'to 76'

 L. 160        66  LOAD_FAST                'resp'
               68  LOAD_ATTR                content
               70  POP_TOP          
               72  POP_BLOCK        
               74  JUMP_FORWARD        116  'to 116'
             76_0  COME_FROM_FINALLY    64  '64'

 L. 161        76  DUP_TOP          
               78  LOAD_GLOBAL              ChunkedEncodingError
               80  LOAD_GLOBAL              ContentDecodingError
               82  LOAD_GLOBAL              RuntimeError
               84  BUILD_TUPLE_3         3 
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   114  'to 114'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 162        96  LOAD_FAST                'resp'
               98  LOAD_ATTR                raw
              100  LOAD_ATTR                read
              102  LOAD_CONST               False
              104  LOAD_CONST               ('decode_content',)
              106  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              108  POP_TOP          
              110  POP_EXCEPT       
              112  JUMP_FORWARD        116  'to 116'
            114_0  COME_FROM            88  '88'
              114  END_FINALLY      
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM            74  '74'

 L. 164       116  LOAD_GLOBAL              len
              118  LOAD_FAST                'resp'
              120  LOAD_ATTR                history
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                max_redirects
              128  COMPARE_OP               >=
              130  POP_JUMP_IF_FALSE   150  'to 150'

 L. 165       132  LOAD_GLOBAL              TooManyRedirects
              134  LOAD_STR                 'Exceeded %s redirects.'
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                max_redirects
              140  BINARY_MODULO    
              142  LOAD_FAST                'resp'
              144  LOAD_CONST               ('response',)
              146  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              148  RAISE_VARARGS_1       1  'exception instance'
            150_0  COME_FROM           130  '130'

 L. 168       150  LOAD_FAST                'resp'
              152  LOAD_METHOD              close
              154  CALL_METHOD_0         0  ''
              156  POP_TOP          

 L. 171       158  LOAD_FAST                'url'
              160  LOAD_METHOD              startswith
              162  LOAD_STR                 '//'
              164  CALL_METHOD_1         1  ''
              166  POP_JUMP_IF_FALSE   196  'to 196'

 L. 172       168  LOAD_GLOBAL              urlparse
              170  LOAD_FAST                'resp'
              172  LOAD_ATTR                url
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'parsed_rurl'

 L. 173       178  LOAD_STR                 '%s:%s'
              180  LOAD_GLOBAL              to_native_string
              182  LOAD_FAST                'parsed_rurl'
              184  LOAD_ATTR                scheme
              186  CALL_FUNCTION_1       1  ''
              188  LOAD_FAST                'url'
              190  BUILD_TUPLE_2         2 
              192  BINARY_MODULO    
              194  STORE_FAST               'url'
            196_0  COME_FROM           166  '166'

 L. 176       196  LOAD_GLOBAL              urlparse
              198  LOAD_FAST                'url'
              200  CALL_FUNCTION_1       1  ''
              202  STORE_FAST               'parsed'

 L. 177       204  LOAD_FAST                'parsed'
              206  LOAD_ATTR                fragment
              208  LOAD_STR                 ''
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   232  'to 232'
              214  LOAD_FAST                'previous_fragment'
              216  POP_JUMP_IF_FALSE   232  'to 232'

 L. 178       218  LOAD_FAST                'parsed'
              220  LOAD_ATTR                _replace
              222  LOAD_FAST                'previous_fragment'
              224  LOAD_CONST               ('fragment',)
              226  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              228  STORE_FAST               'parsed'
              230  JUMP_FORWARD        244  'to 244'
            232_0  COME_FROM           216  '216'
            232_1  COME_FROM           212  '212'

 L. 179       232  LOAD_FAST                'parsed'
              234  LOAD_ATTR                fragment
              236  POP_JUMP_IF_FALSE   244  'to 244'

 L. 180       238  LOAD_FAST                'parsed'
              240  LOAD_ATTR                fragment
              242  STORE_FAST               'previous_fragment'
            244_0  COME_FROM           236  '236'
            244_1  COME_FROM           230  '230'

 L. 181       244  LOAD_FAST                'parsed'
              246  LOAD_METHOD              geturl
              248  CALL_METHOD_0         0  ''
              250  STORE_FAST               'url'

 L. 186       252  LOAD_FAST                'parsed'
              254  LOAD_ATTR                netloc
          256_258  POP_JUMP_IF_TRUE    278  'to 278'

 L. 187       260  LOAD_GLOBAL              urljoin
              262  LOAD_FAST                'resp'
              264  LOAD_ATTR                url
              266  LOAD_GLOBAL              requote_uri
              268  LOAD_FAST                'url'
              270  CALL_FUNCTION_1       1  ''
              272  CALL_FUNCTION_2       2  ''
              274  STORE_FAST               'url'
              276  JUMP_FORWARD        286  'to 286'
            278_0  COME_FROM           256  '256'

 L. 189       278  LOAD_GLOBAL              requote_uri
              280  LOAD_FAST                'url'
              282  CALL_FUNCTION_1       1  ''
              284  STORE_FAST               'url'
            286_0  COME_FROM           276  '276'

 L. 191       286  LOAD_GLOBAL              to_native_string
              288  LOAD_FAST                'url'
              290  CALL_FUNCTION_1       1  ''
              292  LOAD_FAST                'prepared_request'
              294  STORE_ATTR               url

 L. 193       296  LOAD_FAST                'self'
              298  LOAD_METHOD              rebuild_method
              300  LOAD_FAST                'prepared_request'
              302  LOAD_FAST                'resp'
              304  CALL_METHOD_2         2  ''
              306  POP_TOP          

 L. 196       308  LOAD_FAST                'resp'
              310  LOAD_ATTR                status_code
              312  LOAD_GLOBAL              codes
              314  LOAD_ATTR                temporary_redirect
              316  LOAD_GLOBAL              codes
              318  LOAD_ATTR                permanent_redirect
              320  BUILD_TUPLE_2         2 
              322  COMPARE_OP               not-in
          324_326  POP_JUMP_IF_FALSE   364  'to 364'

 L. 198       328  LOAD_CONST               ('Content-Length', 'Content-Type', 'Transfer-Encoding')
              330  STORE_FAST               'purged_headers'

 L. 199       332  LOAD_FAST                'purged_headers'
              334  GET_ITER         
            336_0  COME_FROM           354  '354'
              336  FOR_ITER            358  'to 358'
              338  STORE_FAST               'header'

 L. 200       340  LOAD_FAST                'prepared_request'
              342  LOAD_ATTR                headers
              344  LOAD_METHOD              pop
              346  LOAD_FAST                'header'
              348  LOAD_CONST               None
              350  CALL_METHOD_2         2  ''
              352  POP_TOP          
          354_356  JUMP_BACK           336  'to 336'
            358_0  COME_FROM           336  '336'

 L. 201       358  LOAD_CONST               None
              360  LOAD_FAST                'prepared_request'
              362  STORE_ATTR               body
            364_0  COME_FROM           324  '324'

 L. 203       364  LOAD_FAST                'prepared_request'
              366  LOAD_ATTR                headers
              368  STORE_FAST               'headers'

 L. 204       370  SETUP_FINALLY       382  'to 382'

 L. 205       372  LOAD_FAST                'headers'
              374  LOAD_STR                 'Cookie'
              376  DELETE_SUBSCR    
              378  POP_BLOCK        
              380  JUMP_FORWARD        404  'to 404'
            382_0  COME_FROM_FINALLY   370  '370'

 L. 206       382  DUP_TOP          
              384  LOAD_GLOBAL              KeyError
              386  COMPARE_OP               exception-match
          388_390  POP_JUMP_IF_FALSE   402  'to 402'
              392  POP_TOP          
              394  POP_TOP          
              396  POP_TOP          

 L. 207       398  POP_EXCEPT       
              400  BREAK_LOOP          404  'to 404'
            402_0  COME_FROM           388  '388'
              402  END_FINALLY      
            404_0  COME_FROM           400  '400'
            404_1  COME_FROM           380  '380'

 L. 212       404  LOAD_GLOBAL              extract_cookies_to_jar
              406  LOAD_FAST                'prepared_request'
              408  LOAD_ATTR                _cookies
              410  LOAD_FAST                'req'
              412  LOAD_FAST                'resp'
              414  LOAD_ATTR                raw
              416  CALL_FUNCTION_3       3  ''
              418  POP_TOP          

 L. 213       420  LOAD_GLOBAL              merge_cookies
              422  LOAD_FAST                'prepared_request'
              424  LOAD_ATTR                _cookies
              426  LOAD_FAST                'self'
              428  LOAD_ATTR                cookies
              430  CALL_FUNCTION_2       2  ''
              432  POP_TOP          

 L. 214       434  LOAD_FAST                'prepared_request'
              436  LOAD_METHOD              prepare_cookies
              438  LOAD_FAST                'prepared_request'
              440  LOAD_ATTR                _cookies
              442  CALL_METHOD_1         1  ''
              444  POP_TOP          

 L. 217       446  LOAD_FAST                'self'
              448  LOAD_METHOD              rebuild_proxies
              450  LOAD_FAST                'prepared_request'
              452  LOAD_FAST                'proxies'
              454  CALL_METHOD_2         2  ''
              456  STORE_FAST               'proxies'

 L. 218       458  LOAD_FAST                'self'
              460  LOAD_METHOD              rebuild_auth
              462  LOAD_FAST                'prepared_request'
              464  LOAD_FAST                'resp'
              466  CALL_METHOD_2         2  ''
              468  POP_TOP          

 L. 224       470  LOAD_FAST                'prepared_request'
              472  LOAD_ATTR                _body_position
              474  LOAD_CONST               None
              476  COMPARE_OP               is-not
          478_480  JUMP_IF_FALSE_OR_POP   498  'to 498'

 L. 225       482  LOAD_STR                 'Content-Length'
              484  LOAD_FAST                'headers'
              486  COMPARE_OP               in
          488_490  JUMP_IF_TRUE_OR_POP   498  'to 498'
              492  LOAD_STR                 'Transfer-Encoding'
              494  LOAD_FAST                'headers'
              496  COMPARE_OP               in
            498_0  COME_FROM           488  '488'
            498_1  COME_FROM           478  '478'

 L. 223       498  STORE_FAST               'rewindable'

 L. 229       500  LOAD_FAST                'rewindable'
          502_504  POP_JUMP_IF_FALSE   514  'to 514'

 L. 230       506  LOAD_GLOBAL              rewind_body
              508  LOAD_FAST                'prepared_request'
              510  CALL_FUNCTION_1       1  ''
              512  POP_TOP          
            514_0  COME_FROM           502  '502'

 L. 233       514  LOAD_FAST                'prepared_request'
              516  STORE_FAST               'req'

 L. 235       518  LOAD_FAST                'yield_requests'
          520_522  POP_JUMP_IF_FALSE   532  'to 532'

 L. 236       524  LOAD_FAST                'req'
              526  YIELD_VALUE      
              528  POP_TOP          
              530  JUMP_BACK            26  'to 26'
            532_0  COME_FROM           520  '520'

 L. 239       532  LOAD_FAST                'self'
              534  LOAD_ATTR                send

 L. 240       536  LOAD_FAST                'req'

 L. 239       538  BUILD_TUPLE_1         1 

 L. 241       540  LOAD_FAST                'stream'

 L. 242       542  LOAD_FAST                'timeout'

 L. 243       544  LOAD_FAST                'verify'

 L. 244       546  LOAD_FAST                'cert'

 L. 245       548  LOAD_FAST                'proxies'

 L. 246       550  LOAD_CONST               False

 L. 239       552  LOAD_CONST               ('stream', 'timeout', 'verify', 'cert', 'proxies', 'allow_redirects')
              554  BUILD_CONST_KEY_MAP_6     6 

 L. 247       556  LOAD_FAST                'adapter_kwargs'

 L. 239       558  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              560  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              562  STORE_FAST               'resp'

 L. 250       564  LOAD_GLOBAL              extract_cookies_to_jar
              566  LOAD_FAST                'self'
              568  LOAD_ATTR                cookies
              570  LOAD_FAST                'prepared_request'
              572  LOAD_FAST                'resp'
              574  LOAD_ATTR                raw
              576  CALL_FUNCTION_3       3  ''
              578  POP_TOP          

 L. 253       580  LOAD_FAST                'self'
              582  LOAD_METHOD              get_redirect_target
              584  LOAD_FAST                'resp'
              586  CALL_METHOD_1         1  ''
              588  STORE_FAST               'url'

 L. 254       590  LOAD_FAST                'resp'
              592  YIELD_VALUE      
              594  POP_TOP          
              596  JUMP_BACK            26  'to 26'
            598_0  COME_FROM            28  '28'

Parse error at or near `END_FINALLY' instruction at offset 402

    def rebuild_auth(self, prepared_request, response):
        """When being redirected we may want to strip authentication from the
        request to avoid leaking credentials. This method intelligently removes
        and reapplies authentication where possible to avoid credential loss.
        """
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            if self.should_strip_auth(response.request.url, url):
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
        proxies = proxies if proxies is not None else {}
        headers = prepared_request.headers
        url = prepared_request.url
        scheme = urlparse(url).scheme
        new_proxies = proxies.copy()
        no_proxy = proxies.get('no_proxy')
        bypass_proxy = should_bypass_proxies(url, no_proxy=no_proxy)
        if self.trust_env:
            if not bypass_proxy:
                environ_proxies = get_environ_proxies(url, no_proxy=no_proxy)
                proxy = environ_proxies.get(scheme, environ_proxies.get('all'))
                if proxy:
                    new_proxies.setdefault(scheme, proxy)
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
    __doc__ = "A Requests session.\n\n    Provides cookie persistence, connection-pooling, and configuration.\n\n    Basic Usage::\n\n      >>> import requests\n      >>> s = requests.Session()\n      >>> s.get('https://httpbin.org/get')\n      <Response [200]>\n\n    Or as a context manager::\n\n      >>> with requests.Session() as s:\n      >>>     s.get('https://httpbin.org/get')\n      <Response [200]>\n    "
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
        self.mount('https://', HTTPAdapter())
        self.mount('http://', HTTPAdapter())

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
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
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
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
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
        kwargs.setdefault('allow_redirects', True)
        return (self.request)('GET', url, **kwargs)

    def options(self, url, **kwargs):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        return (self.request)('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', False)
        return (self.request)('HEAD', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return (self.request)('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return (self.request)('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
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
        """Send a given PreparedRequest.

        :rtype: requests.Response
        """
        kwargs.setdefault('stream', self.stream)
        kwargs.setdefault('verify', self.verify)
        kwargs.setdefault('cert', self.cert)
        kwargs.setdefault('proxies', self.proxies)
        if isinstance(request, Request):
            raise ValueError('You can only send PreparedRequests.')
        allow_redirects = kwargs.pop('allow_redirects', True)
        stream = kwargs.get('stream')
        hooks = request.hooks
        adapter = self.get_adapter(url=(request.url))
        start = preferred_clock()
        r = (adapter.send)(request, **kwargs)
        elapsed = preferred_clock() - start
        r.elapsed = timedelta(seconds=elapsed)
        r = dispatch_hook('response', hooks, r, **kwargs)
        if r.history:
            for resp in r.history:
                extract_cookies_to_jar(self.cookies, resp.request, resp.raw)
            else:
                extract_cookies_to_jar(self.cookies, request, r.raw)
                gen = (self.resolve_redirects)(r, request, **kwargs)
                history = [resp for resp in gen] if allow_redirects else []
                if history:
                    history.insert(0, r)
                    r = history.pop()
                    r.history = history

        if not allow_redirects:
            try:
                r._next = next((self.resolve_redirects)(r, request, yield_requests=True, **kwargs))
            except StopIteration:
                pass
            else:
                if not stream:
                    r.content
            return r

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        """
        Check the environment and merge it with some settings.

        :rtype: dict
        """
        if self.trust_env:
            no_proxy = proxies.get('no_proxy') if proxies is not None else None
            env_proxies = get_environ_proxies(url, no_proxy=no_proxy)
            for k, v in env_proxies.items():
                proxies.setdefault(k, v)
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
            if url.lower().startswith(prefix.lower()):
                return adapter
        else:
            raise InvalidSchema("No connection adapters were found for '%s'" % url)

    def close(self):
        """Closes all adapters and as such the session"""
        for v in self.adapters.values():
            v.close()

    def mount(self, prefix, adapter):
        """Registers a connection adapter to a prefix.

        Adapters are sorted in descending order by prefix length.
        """
        self.adapters[prefix] = adapter
        keys_to_move = [k for k in self.adapters if len(k) < len(prefix)]
        for key in keys_to_move:
            self.adapters[key] = self.adapters.pop(key)

    def __getstate__(self):
        state = {getattr(self, attr, None):attr for attr in self.__attrs__}
        return state

    def __setstate__(self, state):
        for attr, value in state.items():
            setattr(self, attr, value)


def session():
    """
    Returns a :class:`Session` for context-management.

    .. deprecated:: 1.0.0

        This method has been deprecated since version 1.0.0 and is only kept for
        backwards compatibility. New code should use :class:`~requests.sessions.Session`
        to create a session. This may be removed at a future date.

    :rtype: Session
    """
    return Session()