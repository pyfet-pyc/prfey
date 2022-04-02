# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: dropbox\dropbox.py
__all__ = ['Dropbox',
 'DropboxTeam',
 'create_session']
__version__ = '10.3.1'
import contextlib, json, logging, random, time, requests, six
from datetime import datetime, timedelta
from . import files, stone_serializers
from .auth import AuthError_validator, RateLimitError_validator
from .common import PathRoot, PathRoot_validator, PathRootError_validator
from .base import DropboxBase
from .base_team import DropboxTeamBase
from .exceptions import ApiError, AuthError, BadInputError, HttpError, PathRootError, InternalServerError, RateLimitError
from .session import API_HOST, API_CONTENT_HOST, API_NOTIFICATION_HOST, HOST_API, HOST_CONTENT, HOST_NOTIFY, pinned_session, DEFAULT_TIMEOUT
PATH_ROOT_HEADER = 'Dropbox-API-Path-Root'
HTTP_STATUS_INVALID_PATH_ROOT = 422
TOKEN_EXPIRATION_BUFFER = 300
SELECT_ADMIN_HEADER = 'Dropbox-API-Select-Admin'
SELECT_USER_HEADER = 'Dropbox-API-Select-User'

class RouteResult(object):
    __doc__ = 'The successful result of a call to a route.'

    def __init__(self, obj_result, http_resp=None):
        """
        :param str obj_result: The result of a route not including the binary
            payload portion, if one exists. Must be serialized JSON.
        :param requests.models.Response http_resp: A raw HTTP response. It will
            be used to stream the binary-body payload of the response.
        """
        assert isinstance(obj_result, six.string_types), 'obj_result: expected string, got %r' % type(obj_result)
        if http_resp is not None:
            assert isinstance(http_resp, requests.models.Response), 'http_resp: expected requests.models.Response, got %r' % type(http_resp)
        self.obj_result = obj_result
        self.http_resp = http_resp


class RouteErrorResult(object):
    __doc__ = 'The error result of a call to a route.'

    def __init__(self, request_id, obj_result):
        """
        :param str request_id: A request_id can be shared with Dropbox Support
            to pinpoint the exact request that returns an error.
        :param str obj_result: The result of a route not including the binary
            payload portion, if one exists.
        """
        self.request_id = request_id
        self.obj_result = obj_result


def create_session(max_connections=8, proxies=None):
    """
    Creates a session object that can be used by multiple :class:`Dropbox` and
    :class:`DropboxTeam` instances. This lets you share a connection pool
    amongst them, as well as proxy parameters.

    :param int max_connections: Maximum connection pool size.
    :param dict proxies: See the `requests module
            <http://docs.python-requests.org/en/latest/user/advanced/#proxies>`_
            for more details.
    :rtype: :class:`requests.sessions.Session`. `See the requests module
        <http://docs.python-requests.org/en/latest/user/advanced/#session-objects>`_
        for more details.
    """
    session = pinned_session(pool_maxsize=max_connections)
    if proxies:
        session.proxies = proxies
    return session


class _DropboxTransport(object):
    __doc__ = '\n    Responsible for implementing the wire protocol for making requests to the\n    Dropbox API.\n    '
    _API_VERSION = '2'
    _ROUTE_STYLE_DOWNLOAD = 'download'
    _ROUTE_STYLE_UPLOAD = 'upload'
    _ROUTE_STYLE_RPC = 'rpc'

    def __init__(self, oauth2_access_token=None, max_retries_on_error=4, max_retries_on_rate_limit=None, user_agent=None, session=None, headers=None, timeout=DEFAULT_TIMEOUT, oauth2_refresh_token=None, oauth2_access_token_expiration=None, app_key=None, app_secret=None, scope=None):
        """
        :param str oauth2_access_token: OAuth2 access token for making client
            requests.
        :param int max_retries_on_error: On 5xx errors, the number of times to
            retry.
        :param Optional[int] max_retries_on_rate_limit: On 429 errors, the
            number of times to retry. If `None`, always retries.
        :param str user_agent: The user agent to use when making requests. This
            helps us identify requests coming from your application. We
            recommend you use the format "AppName/Version". If set, we append
            "/OfficialDropboxPythonSDKv2/__version__" to the user_agent,
        :param session: If not provided, a new session (connection pool) is
            created. To share a session across multiple clients, use
            :func:`create_session`.
        :type session: :class:`requests.sessions.Session`
        :param dict headers: Additional headers to add to requests.
        :param Optional[float] timeout: Maximum duration in seconds that
            client will wait for any single packet from the
            server. After the timeout the client will give up on
            connection. If `None`, client will wait forever. Defaults
            to 100 seconds.
        :param str oauth2_refresh_token: OAuth2 refresh token for refreshing access token
        :param datetime oauth2_access_token_expiration: Expiration for oauth2_access_token
        :param str app_key: application key of requesting application; used for token refresh
        :param str app_secret: application secret of requesting application; used for token refresh
            Not required if PKCE was used to authorize the token
        :param list scope: list of scopes to request on refresh.  If left blank,
            refresh will request all available scopes for application
        """
        if not oauth2_access_token:
            if not oauth2_refresh_token:
                raise BadInputException('OAuth2 access token or refresh token must be set')
        if headers is not None:
            if not isinstance(headers, dict):
                raise BadInputException('Expected dict, got {}'.format(headers))
        if oauth2_refresh_token:
            if not app_key:
                raise BadInputException('app_key is required to refresh tokens')
            if scope is not None:
                if not (len(scope) == 0 or isinstance(scope, list)):
                    raise BadInputException('Scope list must be of type list')
        self._oauth2_access_token = oauth2_access_token
        self._oauth2_refresh_token = oauth2_refresh_token
        self._oauth2_access_token_expiration = oauth2_access_token_expiration
        self._app_key = app_key
        self._app_secret = app_secret
        self._scope = scope
        self._max_retries_on_error = max_retries_on_error
        self._max_retries_on_rate_limit = max_retries_on_rate_limit
        if session:
            if not isinstance(session, requests.sessions.Session):
                raise BadInputException('Expected requests.sessions.Session, got {}'.format(session))
            self._session = session
        else:
            self._session = create_session()
        self._headers = headers
        base_user_agent = 'OfficialDropboxPythonSDKv2/' + __version__
        if user_agent:
            self._raw_user_agent = user_agent
            self._user_agent = '{}/{}'.format(user_agent, base_user_agent)
        else:
            self._raw_user_agent = None
            self._user_agent = base_user_agent
        self._logger = logging.getLogger('dropbox')
        self._host_map = {HOST_API: API_HOST, 
         HOST_CONTENT: API_CONTENT_HOST, 
         HOST_NOTIFY: API_NOTIFICATION_HOST}
        self._timeout = timeout

    def clone(self, oauth2_access_token=None, max_retries_on_error=None, max_retries_on_rate_limit=None, user_agent=None, session=None, headers=None, timeout=None, oauth2_refresh_token=None, oauth2_access_token_expiration=None, app_key=None, app_secret=None, scope=None):
        """
        Creates a new copy of the Dropbox client with the same defaults unless modified by
        arguments to clone()

        See constructor for original parameter descriptions.

        :return: New instance of Dropbox client
        :rtype: Dropbox
        """
        return self.__class__(oauth2_access_token or self._oauth2_access_token, max_retries_on_error or self._max_retries_on_error, max_retries_on_rate_limit or self._max_retries_on_rate_limit, user_agent or self._user_agent, session or self._session, headers or self._headers, timeout or self._timeout, oauth2_refresh_token or self._oauth2_refresh_token, oauth2_access_token_expiration or self._oauth2_access_token_expiration, app_key or self._app_key, app_secret or self._app_secret, scope or self._scope)

    def request(self, route, namespace, request_arg, request_binary, timeout=None):
        """
        Makes a request to the Dropbox API and in the process validates that
        the route argument and result are the expected data types. The
        request_arg is converted to JSON based on the arg_data_type. Likewise,
        the response is deserialized from JSON and converted to an object based
        on the {result,error}_data_type.

        :param host: The Dropbox API host to connect to.
        :param route: The route to make the request to.
        :type route: :class:`.datatypes.stone_base.Route`
        :param request_arg: Argument for the route that conforms to the
            validator specified by route.arg_type.
        :param request_binary: String or file pointer representing the binary
            payload. Use None if there is no binary payload.
        :param Optional[float] timeout: Maximum duration in seconds
            that client will wait for any single packet from the
            server. After the timeout the client will give up on
            connection. If `None`, will use default timeout set on
            Dropbox object.  Defaults to `None`.
        :return: The route's result.
        """
        self.check_and_refresh_access_token()
        host = route.attrs['host'] or 'api'
        route_name = namespace + '/' + route.name
        if route.version > 1:
            route_name += '_v{}'.format(route.version)
        route_style = route.attrs['style'] or 'rpc'
        serialized_arg = stone_serializers.json_encode(route.arg_type, request_arg)
        if timeout is None:
            if route == files.list_folder_longpoll:
                timeout = request_arg.timeout + 90
        res = self.request_json_string_with_retry(host, route_name,
          route_style,
          serialized_arg,
          request_binary,
          timeout=timeout)
        decoded_obj_result = json.loads(res.obj_result)
        if isinstance(res, RouteResult):
            returned_data_type = route.result_type
            obj = decoded_obj_result
        elif isinstance(res, RouteErrorResult):
            returned_data_type = route.error_type
            obj = decoded_obj_result['error']
            user_message = decoded_obj_result.get('user_message')
            user_message_text = user_message and user_message.get('text')
            user_message_locale = user_message and user_message.get('locale')
        else:
            raise AssertionError('Expected RouteResult or RouteErrorResult, but res is %s' % type(res))
        deserialized_result = stone_serializers.json_compat_obj_decode(returned_data_type,
          obj, strict=False)
        if isinstance(res, RouteErrorResult):
            raise ApiError(res.request_id, deserialized_result, user_message_text, user_message_locale)
        else:
            if route_style == self._ROUTE_STYLE_DOWNLOAD:
                return (deserialized_result, res.http_resp)
            return deserialized_result

    def check_and_refresh_access_token(self):
        """
        Checks if access token needs to be refreshed and refreshes if possible
        :return:
        """
        can_refresh = self._oauth2_refresh_token and self._app_key
        needs_refresh = self._oauth2_access_token_expiration and datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION_BUFFER) >= self._oauth2_access_token_expiration
        needs_token = not self._oauth2_access_token
        if needs_refresh or (needs_token):
            if can_refresh:
                self.refresh_access_token(scope=(self._scope))

    def refresh_access_token(self, host=API_HOST, scope=None):
        """
        Refreshes an access token via refresh token if available

        :param host: host to hit token endpoint with
        :param scope: list of permission scopes for access token
        :return:
        """
        if scope is not None:
            if not (len(scope) == 0 or isinstance(scope, list)):
                raise BadInputException('Scope list must be of type list')
            if not (self._oauth2_refresh_token and self._app_key):
                self._logger.warning('Unable to refresh access token without                 refresh token and app key')
                return
            self._logger.info('Refreshing access token.')
            url = 'https://{}/oauth2/token'.format(host)
            body = {'grant_type':'refresh_token',  'refresh_token':self._oauth2_refresh_token, 
             'client_id':self._app_key}
            if self._app_secret:
                body['client_secret'] = self._app_secret
            if scope:
                scope = ' '.join(scope)
                body['scope'] = scope
            timeout = DEFAULT_TIMEOUT
            if self._timeout:
                timeout = self._timeout
            res = self._session.post(url, data=body, timeout=timeout)
            if res.status_code == 400:
                if res.json()['error'] == 'invalid_grant':
                    request_id = res.headers.get('x-dropbox-request-id')
                    err = stone_serializers.json_compat_obj_decode(AuthError_validator, 'invalid_access_token')
                    raise AuthError(request_id, err)
        res.raise_for_status()
        token_content = res.json()
        self._oauth2_access_token = token_content['access_token']
        self._oauth2_access_token_expiration = datetime.utcnow() + timedelta(seconds=(int(token_content['expires_in'])))

    def request_json_object(self, host, route_name, route_style, request_arg, request_binary, timeout=None):
        """
        Makes a request to the Dropbox API, taking a JSON-serializable Python
        object as an argument, and returning one as a response.

        :param host: The Dropbox API host to connect to.
        :param route_name: The name of the route to invoke.
        :param route_style: The style of the route.
        :param str request_arg: A JSON-serializable Python object representing
            the argument for the route.
        :param Optional[bytes] request_binary: Bytes representing the binary
            payload. Use None if there is no binary payload.
        :param Optional[float] timeout: Maximum duration in seconds
            that client will wait for any single packet from the
            server. After the timeout the client will give up on
            connection. If `None`, will use default timeout set on
            Dropbox object.  Defaults to `None`.
        :return: The route's result as a JSON-serializable Python object.
        """
        serialized_arg = json.dumps(request_arg)
        res = self.request_json_string_with_retry(host, route_name,
          route_style,
          serialized_arg,
          request_binary,
          timeout=timeout)
        deserialized_result = json.loads(res.obj_result)
        if isinstance(res, RouteResult):
            if res.http_resp is not None:
                return (
                 deserialized_result, res.http_resp)
        return deserialized_result

    def request_json_string_with_retry--- This code section failed: ---

 L. 457         0  LOAD_CONST               0
                2  STORE_FAST               'attempt'

 L. 458         4  LOAD_CONST               0
                6  STORE_FAST               'rate_limit_errors'

 L. 459         8  LOAD_CONST               False
               10  STORE_FAST               'has_refreshed'
             12_0  COME_FROM           356  '356'
             12_1  COME_FROM           352  '352'
             12_2  COME_FROM           236  '236'
             12_3  COME_FROM           138  '138'

 L. 461        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _logger
               16  LOAD_METHOD              info
               18  LOAD_STR                 'Request to %s'
               20  LOAD_FAST                'route_name'
               22  CALL_METHOD_2         2  ''
               24  POP_TOP          

 L. 462        26  SETUP_FINALLY        52  'to 52'

 L. 463        28  LOAD_FAST                'self'
               30  LOAD_ATTR                request_json_string
               32  LOAD_FAST                'host'

 L. 464        34  LOAD_FAST                'route_name'

 L. 465        36  LOAD_FAST                'route_style'

 L. 466        38  LOAD_FAST                'request_json_arg'

 L. 467        40  LOAD_FAST                'request_binary'

 L. 468        42  LOAD_FAST                'timeout'

 L. 463        44  LOAD_CONST               ('timeout',)
               46  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    26  '26'

 L. 469        52  DUP_TOP          
               54  LOAD_GLOBAL              AuthError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE   140  'to 140'
               60  POP_TOP          
               62  STORE_FAST               'e'
               64  POP_TOP          
               66  SETUP_FINALLY       128  'to 128'

 L. 470        68  LOAD_FAST                'e'
               70  LOAD_ATTR                error
               72  POP_JUMP_IF_FALSE   122  'to 122'
               74  LOAD_FAST                'e'
               76  LOAD_ATTR                error
               78  LOAD_METHOD              is_expired_access_token
               80  CALL_METHOD_0         0  ''
               82  POP_JUMP_IF_FALSE   122  'to 122'

 L. 471        84  LOAD_FAST                'has_refreshed'
               86  POP_JUMP_IF_FALSE    92  'to 92'

 L. 472        88  RAISE_VARARGS_0       0  'reraise'
               90  BREAK_LOOP          124  'to 124'
             92_0  COME_FROM            86  '86'

 L. 474        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _logger
               96  LOAD_METHOD              info

 L. 475        98  LOAD_STR                 'ExpiredCredentials status_code=%s: Refreshing and Retrying'

 L. 476       100  LOAD_FAST                'e'
              102  LOAD_ATTR                status_code

 L. 474       104  CALL_METHOD_2         2  ''
              106  POP_TOP          

 L. 477       108  LOAD_FAST                'self'
              110  LOAD_METHOD              refresh_access_token
              112  CALL_METHOD_0         0  ''
              114  POP_TOP          

 L. 478       116  LOAD_CONST               True
              118  STORE_FAST               'has_refreshed'
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM            82  '82'
            122_1  COME_FROM            72  '72'

 L. 480       122  RAISE_VARARGS_0       0  'reraise'
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            90  '90'
              124  POP_BLOCK        
              126  BEGIN_FINALLY    
            128_0  COME_FROM_FINALLY    66  '66'
              128  LOAD_CONST               None
              130  STORE_FAST               'e'
              132  DELETE_FAST              'e'
              134  END_FINALLY      
              136  POP_EXCEPT       
              138  JUMP_BACK            12  'to 12'
            140_0  COME_FROM            58  '58'

 L. 481       140  DUP_TOP          
              142  LOAD_GLOBAL              InternalServerError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   238  'to 238'
              148  POP_TOP          
              150  STORE_FAST               'e'
              152  POP_TOP          
              154  SETUP_FINALLY       226  'to 226'

 L. 482       156  LOAD_FAST                'attempt'
              158  LOAD_CONST               1
              160  INPLACE_ADD      
              162  STORE_FAST               'attempt'

 L. 483       164  LOAD_FAST                'attempt'
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _max_retries_on_error
              170  COMPARE_OP               <=
              172  POP_JUMP_IF_FALSE   220  'to 220'

 L. 485       174  LOAD_CONST               2
              176  LOAD_FAST                'attempt'
              178  BINARY_POWER     
              180  LOAD_GLOBAL              random
              182  LOAD_METHOD              random
              184  CALL_METHOD_0         0  ''
              186  BINARY_MULTIPLY  
              188  STORE_FAST               'backoff'

 L. 486       190  LOAD_FAST                'self'
              192  LOAD_ATTR                _logger
              194  LOAD_METHOD              info

 L. 487       196  LOAD_STR                 'HttpError status_code=%s: Retrying in %.1f seconds'

 L. 488       198  LOAD_FAST                'e'
              200  LOAD_ATTR                status_code

 L. 488       202  LOAD_FAST                'backoff'

 L. 486       204  CALL_METHOD_3         3  ''
              206  POP_TOP          

 L. 489       208  LOAD_GLOBAL              time
              210  LOAD_METHOD              sleep
              212  LOAD_FAST                'backoff'
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
              218  JUMP_FORWARD        222  'to 222'
            220_0  COME_FROM           172  '172'

 L. 491       220  RAISE_VARARGS_0       0  'reraise'
            222_0  COME_FROM           218  '218'
              222  POP_BLOCK        
              224  BEGIN_FINALLY    
            226_0  COME_FROM_FINALLY   154  '154'
              226  LOAD_CONST               None
              228  STORE_FAST               'e'
              230  DELETE_FAST              'e'
              232  END_FINALLY      
              234  POP_EXCEPT       
              236  JUMP_BACK            12  'to 12'
            238_0  COME_FROM           146  '146'

 L. 492       238  DUP_TOP          
              240  LOAD_GLOBAL              RateLimitError
              242  COMPARE_OP               exception-match
          244_246  POP_JUMP_IF_FALSE   354  'to 354'
              248  POP_TOP          
              250  STORE_FAST               'e'
              252  POP_TOP          
              254  SETUP_FINALLY       342  'to 342'

 L. 493       256  LOAD_FAST                'rate_limit_errors'
              258  LOAD_CONST               1
              260  INPLACE_ADD      
              262  STORE_FAST               'rate_limit_errors'

 L. 494       264  LOAD_FAST                'self'
              266  LOAD_ATTR                _max_retries_on_rate_limit
              268  LOAD_CONST               None
              270  COMPARE_OP               is
          272_274  POP_JUMP_IF_TRUE    288  'to 288'

 L. 495       276  LOAD_FAST                'self'
              278  LOAD_ATTR                _max_retries_on_rate_limit
              280  LOAD_FAST                'rate_limit_errors'
              282  COMPARE_OP               >=

 L. 494   284_286  POP_JUMP_IF_FALSE   336  'to 336'
            288_0  COME_FROM           272  '272'

 L. 497       288  LOAD_FAST                'e'
              290  LOAD_ATTR                backoff
              292  LOAD_CONST               None
              294  COMPARE_OP               is-not
          296_298  POP_JUMP_IF_FALSE   306  'to 306'
              300  LOAD_FAST                'e'
              302  LOAD_ATTR                backoff
              304  JUMP_FORWARD        308  'to 308'
            306_0  COME_FROM           296  '296'
              306  LOAD_CONST               5.0
            308_0  COME_FROM           304  '304'
              308  STORE_FAST               'backoff'

 L. 498       310  LOAD_FAST                'self'
              312  LOAD_ATTR                _logger
              314  LOAD_METHOD              info

 L. 499       316  LOAD_STR                 'Ratelimit: Retrying in %.1f seconds.'

 L. 499       318  LOAD_FAST                'backoff'

 L. 498       320  CALL_METHOD_2         2  ''
              322  POP_TOP          

 L. 500       324  LOAD_GLOBAL              time
              326  LOAD_METHOD              sleep
              328  LOAD_FAST                'backoff'
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          
              334  JUMP_FORWARD        338  'to 338'
            336_0  COME_FROM           284  '284'

 L. 502       336  RAISE_VARARGS_0       0  'reraise'
            338_0  COME_FROM           334  '334'
              338  POP_BLOCK        
              340  BEGIN_FINALLY    
            342_0  COME_FROM_FINALLY   254  '254'
              342  LOAD_CONST               None
              344  STORE_FAST               'e'
              346  DELETE_FAST              'e'
              348  END_FINALLY      
              350  POP_EXCEPT       
              352  JUMP_BACK            12  'to 12'
            354_0  COME_FROM           244  '244'
              354  END_FINALLY      
              356  JUMP_BACK            12  'to 12'

Parse error at or near `JUMP_BACK' instruction at offset 138

    def request_json_string(self, host, func_name, route_style, request_json_arg, request_binary, timeout=None):
        """
        See :meth:`request_json_string_with_retry` for description of
        parameters.
        """
        if host not in self._host_map:
            raise ValueError('Unknown value for host: %r' % host)
        if not isinstance(request_binary, (six.binary_type, type(None))):
            raise TypeError('expected request_binary as binary type, got %s' % type(request_binary))
        fq_hostname = self._host_map[host]
        url = self._get_route_url(fq_hostname, func_name)
        headers = {'User-Agent': self._user_agent}
        if host != HOST_NOTIFY:
            headers['Authorization'] = 'Bearer %s' % self._oauth2_access_token
            if self._headers:
                headers.update(self._headers)
        body = None
        stream = False
        if route_style == self._ROUTE_STYLE_RPC:
            headers['Content-Type'] = 'application/json'
            body = request_json_arg
        elif route_style == self._ROUTE_STYLE_DOWNLOAD:
            headers['Dropbox-API-Arg'] = request_json_arg
            stream = True
        elif route_style == self._ROUTE_STYLE_UPLOAD:
            headers['Content-Type'] = 'application/octet-stream'
            headers['Dropbox-API-Arg'] = request_json_arg
            body = request_binary
        else:
            raise ValueError('Unknown operation style: %r' % route_style)
        if timeout is None:
            timeout = self._timeout
        r = self._session.post(url, headers=headers,
          data=body,
          stream=stream,
          verify=True,
          timeout=timeout)
        request_id = r.headers.get('x-dropbox-request-id')
        if r.status_code >= 500:
            raise InternalServerError(request_id, r.status_code, r.text)
        elif r.status_code == 400:
            raise BadInputError(request_id, r.text)
        elif r.status_code == 401:
            assert r.headers.get('content-type') == 'application/json', 'Expected content-type to be application/json, got %r' % r.headers.get('content-type')
            err = stone_serializers.json_compat_obj_decode(AuthError_validator, r.json()['error'])
            raise AuthError(request_id, err)
        elif r.status_code == HTTP_STATUS_INVALID_PATH_ROOT:
            err = stone_serializers.json_compat_obj_decode(PathRootError_validator, r.json()['error'])
            raise PathRootError(request_id, err)
        elif r.status_code == 429:
            err = None
            if r.headers.get('content-type') == 'application/json':
                err = stone_serializers.json_compat_obj_decode(RateLimitError_validator, r.json()['error'])
                retry_after = err.retry_after
            else:
                retry_after_str = r.headers.get('retry-after')
                if retry_after_str is not None:
                    retry_after = int(retry_after_str)
                else:
                    retry_after = None
            raise RateLimitError(request_id, err, retry_after)
        elif 200 <= r.status_code <= 299:
            if route_style == self._ROUTE_STYLE_DOWNLOAD:
                raw_resp = r.headers['dropbox-api-result']
            else:
                assert r.headers.get('content-type') == 'application/json', 'Expected content-type to be application/json, got %r' % r.headers.get('content-type')
                raw_resp = r.content.decode('utf-8')
            if route_style == self._ROUTE_STYLE_DOWNLOAD:
                return RouteResult(raw_resp, r)
            return RouteResult(raw_resp)
        else:
            if r.status_code in (403, 404, 409):
                raw_resp = r.content.decode('utf-8')
                return RouteErrorResult(request_id, raw_resp)
            raise HttpError(request_id, r.status_code, r.text)

    def _get_route_url(self, hostname, route_name):
        """Returns the URL of the route.

        :param str hostname: Hostname to make the request to.
        :param str route_name: Name of the route.
        :rtype: str
        """
        return 'https://{hostname}/{version}/{route_name}'.format(hostname=hostname,
          version=(Dropbox._API_VERSION),
          route_name=route_name)

    def _save_body_to_file(self, download_path, http_resp, chunksize=65536):
        """
        Saves the body of an HTTP response to a file.

        :param str download_path: Local path to save data to.
        :param http_resp: The HTTP response whose body will be saved.
        :type http_resp: :class:`requests.models.Response`
        :rtype: None
        """
        with open(download_path, 'wb') as f:
            with contextlib.closing(http_resp):
                for c in http_resp.iter_content(chunksize):
                    f.write(c)

    def with_path_root(self, path_root):
        """
        Creates a clone of the Dropbox instance with the Dropbox-API-Path-Root header
        as the appropriate serialized instance of PathRoot.

        For more information, see
        https://www.dropbox.com/developers/reference/namespace-guide#pathrootmodes

        :param PathRoot path_root: instance of PathRoot to serialize into the headers field
        :return: A :class: `Dropbox`
        :rtype: Dropbox
        """
        if not isinstance(path_root, PathRoot):
            raise ValueError('path_root must be an instance of PathRoot')
        new_headers = self._headers.copy() if self._headers else {}
        new_headers[PATH_ROOT_HEADER] = stone_serializers.json_encode(PathRoot_validator, path_root)
        return self.clone(headers=new_headers)

    def close(self):
        """
        Cleans up all resources like the request session/network connection.
        """
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class Dropbox(_DropboxTransport, DropboxBase):
    __doc__ = "\n    Use this class to make requests to the Dropbox API using a user's access\n    token. Methods of this class are meant to act on the corresponding user's\n    Dropbox.\n    "


class DropboxTeam(_DropboxTransport, DropboxTeamBase):
    __doc__ = "\n    Use this class to make requests to the Dropbox API using a team's access\n    token. Methods of this class are meant to act on the team, but there is\n    also an :meth:`as_user` method for assuming a team member's identity.\n    "

    def as_admin(self, team_member_id):
        """
        Allows a team credential to assume the identity of an administrator on the team
        and perform operations on any team-owned content.

        :param str team_member_id: team member id of administrator to perform actions with
        :return: A :class:`Dropbox` object that can be used to query on behalf
            of this admin of the team.
        :rtype: Dropbox
        """
        return self._get_dropbox_client_with_select_header(SELECT_ADMIN_HEADER, team_member_id)

    def as_user(self, team_member_id):
        """
        Allows a team credential to assume the identity of a member of the
        team.

        :param str team_member_id: team member id of team member to perform actions with
        :return: A :class:`Dropbox` object that can be used to query on behalf
            of this member of the team.
        :rtype: Dropbox
        """
        return self._get_dropbox_client_with_select_header(SELECT_USER_HEADER, team_member_id)

    def _get_dropbox_client_with_select_header(self, select_header_name, team_member_id):
        """
        Get Dropbox client with modified headers

        :param str select_header_name: Header name used to select users
        :param str team_member_id: team member id of team member to perform actions with
        :return: A :class:`Dropbox` object that can be used to query on behalf
            of a member or admin of the team
        :rtype: Dropbox
        """
        new_headers = self._headers.copy() if self._headers else {}
        new_headers[select_header_name] = team_member_id
        return Dropbox((self._oauth2_access_token),
          oauth2_refresh_token=(self._oauth2_refresh_token),
          oauth2_access_token_expiration=(self._oauth2_access_token_expiration),
          max_retries_on_error=(self._max_retries_on_error),
          max_retries_on_rate_limit=(self._max_retries_on_rate_limit),
          timeout=(self._timeout),
          user_agent=(self._raw_user_agent),
          session=(self._session),
          headers=new_headers)


class BadInputException(Exception):
    __doc__ = '\n    Thrown if incorrect types/values are used\n\n    This should only ever be thrown during testing, app should have validation of input prior to\n    reaching this point\n    '