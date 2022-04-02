# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\remote\remote_connection.py
import base64, logging, platform, socket, string, urllib3
try:
    from urllib import parse
except ImportError:
    import urlparse as parse
else:
    import selenium.webdriver.common as common_utils
    from selenium import __version__
    from .command import Command
    from .errorhandler import ErrorCode
    from . import utils
    LOGGER = logging.getLogger(__name__)

    class RemoteConnection(object):
        __doc__ = 'A connection with the Remote WebDriver server.\n\n    Communicates with the server using the WebDriver wire protocol:\n    https://github.com/SeleniumHQ/selenium/wiki/JsonWireProtocol'
        _timeout = socket._GLOBAL_DEFAULT_TIMEOUT

        @classmethod
        def get_timeout(cls):
            """
        :Returns:
            Timeout value in seconds for all http requests made to the Remote Connection
        """
            if cls._timeout == socket._GLOBAL_DEFAULT_TIMEOUT:
                return
            return cls._timeout

        @classmethod
        def set_timeout(cls, timeout):
            """
        Override the default timeout

        :Args:
            - timeout - timeout value for http requests in seconds
        """
            cls._timeout = timeout

        @classmethod
        def reset_timeout(cls):
            """
        Reset the http request timeout to socket._GLOBAL_DEFAULT_TIMEOUT
        """
            cls._timeout = socket._GLOBAL_DEFAULT_TIMEOUT

        @classmethod
        def get_remote_connection_headers(cls, parsed_url, keep_alive=False):
            """
        Get headers for remote request.

        :Args:
         - parsed_url - The parsed url
         - keep_alive (Boolean) - Is this a keep-alive connection (default: False)
        """
            system = platform.system().lower()
            if system == 'darwin':
                system = 'mac'
            headers = {'Accept':'application/json', 
             'Content-Type':'application/json;charset=UTF-8', 
             'User-Agent':'selenium/{} (python {})'.format(__version__, system)}
            if parsed_url.username:
                base64string = base64.b64encode('{0.username}:{0.password}'.format(parsed_url).encode())
                headers.update({'Authorization': 'Basic {}'.format(base64string.decode())})
            if keep_alive:
                headers.update({'Connection': 'keep-alive'})
            return headers

        def __init__(self, remote_server_addr, keep_alive=False, resolve_ip=True):
            self.keep_alive = keep_alive
            parsed_url = parse.urlparse(remote_server_addr)
            if parsed_url.hostname:
                if resolve_ip:
                    port = parsed_url.port or None
                    if parsed_url.scheme == 'https':
                        ip = parsed_url.hostname
                    elif port and not common_utils.is_connectable(port, parsed_url.hostname):
                        ip = None
                        LOGGER.info('Could not connect to port {} on host {}'.format(port, parsed_url.hostname))
                    else:
                        ip = common_utils.find_connectable_ip((parsed_url.hostname), port=port)
                    if ip:
                        netloc = ip
                        if parsed_url.port:
                            netloc = common_utils.join_host_port(netloc, parsed_url.port)
                        if parsed_url.username:
                            auth = parsed_url.username
                            if parsed_url.password:
                                auth += ':%s' % parsed_url.password
                            netloc = '%s@%s' % (auth, netloc)
                        remote_server_addr = parse.urlunparse((
                         parsed_url.scheme, netloc, parsed_url.path,
                         parsed_url.params, parsed_url.query, parsed_url.fragment))
                    else:
                        LOGGER.info('Could not get IP address for host: %s' % parsed_url.hostname)
            self._url = remote_server_addr
            if keep_alive:
                self._conn = urllib3.PoolManager(timeout=(self._timeout))
            self._commands = {Command.STATUS: ('GET', '/status'), 
             Command.NEW_SESSION: ('POST', '/session'), 
             Command.GET_ALL_SESSIONS: ('GET', '/sessions'), 
             Command.QUIT: ('DELETE', '/session/$sessionId'), 
             Command.GET_CURRENT_WINDOW_HANDLE: ('GET', '/session/$sessionId/window_handle'), 
             
             Command.W3C_GET_CURRENT_WINDOW_HANDLE: ('GET', '/session/$sessionId/window'), 
             
             Command.GET_WINDOW_HANDLES: ('GET', '/session/$sessionId/window_handles'), 
             
             Command.W3C_GET_WINDOW_HANDLES: ('GET', '/session/$sessionId/window/handles'), 
             
             Command.GET: ('POST', '/session/$sessionId/url'), 
             Command.GO_FORWARD: ('POST', '/session/$sessionId/forward'), 
             Command.GO_BACK: ('POST', '/session/$sessionId/back'), 
             Command.REFRESH: ('POST', '/session/$sessionId/refresh'), 
             Command.EXECUTE_SCRIPT: ('POST', '/session/$sessionId/execute'), 
             Command.W3C_EXECUTE_SCRIPT: ('POST', '/session/$sessionId/execute/sync'), 
             
             Command.W3C_EXECUTE_SCRIPT_ASYNC: ('POST', '/session/$sessionId/execute/async'), 
             
             Command.GET_CURRENT_URL: ('GET', '/session/$sessionId/url'), 
             Command.GET_TITLE: ('GET', '/session/$sessionId/title'), 
             Command.GET_PAGE_SOURCE: ('GET', '/session/$sessionId/source'), 
             Command.SCREENSHOT: ('GET', '/session/$sessionId/screenshot'), 
             Command.ELEMENT_SCREENSHOT: ('GET', '/session/$sessionId/element/$id/screenshot'), 
             Command.FIND_ELEMENT: ('POST', '/session/$sessionId/element'), 
             Command.FIND_ELEMENTS: ('POST', '/session/$sessionId/elements'), 
             Command.W3C_GET_ACTIVE_ELEMENT: ('GET', '/session/$sessionId/element/active'), 
             Command.GET_ACTIVE_ELEMENT: ('POST', '/session/$sessionId/element/active'), 
             
             Command.FIND_CHILD_ELEMENT: ('POST', '/session/$sessionId/element/$id/element'), 
             
             Command.FIND_CHILD_ELEMENTS: ('POST', '/session/$sessionId/element/$id/elements'), 
             
             Command.CLICK_ELEMENT: ('POST', '/session/$sessionId/element/$id/click'), 
             Command.CLEAR_ELEMENT: ('POST', '/session/$sessionId/element/$id/clear'), 
             Command.SUBMIT_ELEMENT: ('POST', '/session/$sessionId/element/$id/submit'), 
             Command.GET_ELEMENT_TEXT: ('GET', '/session/$sessionId/element/$id/text'), 
             Command.SEND_KEYS_TO_ELEMENT: ('POST', '/session/$sessionId/element/$id/value'), 
             
             Command.SEND_KEYS_TO_ACTIVE_ELEMENT: ('POST', '/session/$sessionId/keys'), 
             
             Command.UPLOAD_FILE: ('POST', '/session/$sessionId/file'), 
             Command.GET_ELEMENT_VALUE: ('GET', '/session/$sessionId/element/$id/value'), 
             
             Command.GET_ELEMENT_TAG_NAME: ('GET', '/session/$sessionId/element/$id/name'), 
             
             Command.IS_ELEMENT_SELECTED: ('GET', '/session/$sessionId/element/$id/selected'), 
             
             Command.SET_ELEMENT_SELECTED: ('POST', '/session/$sessionId/element/$id/selected'), 
             
             Command.IS_ELEMENT_ENABLED: ('GET', '/session/$sessionId/element/$id/enabled'), 
             
             Command.IS_ELEMENT_DISPLAYED: ('GET', '/session/$sessionId/element/$id/displayed'), 
             
             Command.GET_ELEMENT_LOCATION: ('GET', '/session/$sessionId/element/$id/location'), 
             
             Command.GET_ELEMENT_LOCATION_ONCE_SCROLLED_INTO_VIEW: ('GET', '/session/$sessionId/element/$id/location_in_view'), 
             
             Command.GET_ELEMENT_SIZE: ('GET', '/session/$sessionId/element/$id/size'), 
             
             Command.GET_ELEMENT_RECT: ('GET', '/session/$sessionId/element/$id/rect'), 
             
             Command.GET_ELEMENT_ATTRIBUTE: ('GET', '/session/$sessionId/element/$id/attribute/$name'), 
             
             Command.GET_ELEMENT_PROPERTY: ('GET', '/session/$sessionId/element/$id/property/$name'), 
             
             Command.GET_ALL_COOKIES: ('GET', '/session/$sessionId/cookie'), 
             Command.ADD_COOKIE: ('POST', '/session/$sessionId/cookie'), 
             Command.GET_COOKIE: ('GET', '/session/$sessionId/cookie/$name'), 
             Command.DELETE_ALL_COOKIES: ('DELETE', '/session/$sessionId/cookie'), 
             
             Command.DELETE_COOKIE: ('DELETE', '/session/$sessionId/cookie/$name'), 
             
             Command.SWITCH_TO_FRAME: ('POST', '/session/$sessionId/frame'), 
             Command.SWITCH_TO_PARENT_FRAME: ('POST', '/session/$sessionId/frame/parent'), 
             Command.SWITCH_TO_WINDOW: ('POST', '/session/$sessionId/window'), 
             Command.CLOSE: ('DELETE', '/session/$sessionId/window'), 
             Command.GET_ELEMENT_VALUE_OF_CSS_PROPERTY: ('GET', '/session/$sessionId/element/$id/css/$propertyName'), 
             
             Command.IMPLICIT_WAIT: ('POST', '/session/$sessionId/timeouts/implicit_wait'), 
             
             Command.EXECUTE_ASYNC_SCRIPT: ('POST', '/session/$sessionId/execute_async'), 
             Command.SET_SCRIPT_TIMEOUT: ('POST', '/session/$sessionId/timeouts/async_script'), 
             
             Command.SET_TIMEOUTS: ('POST', '/session/$sessionId/timeouts'), 
             
             Command.DISMISS_ALERT: ('POST', '/session/$sessionId/dismiss_alert'), 
             
             Command.W3C_DISMISS_ALERT: ('POST', '/session/$sessionId/alert/dismiss'), 
             
             Command.ACCEPT_ALERT: ('POST', '/session/$sessionId/accept_alert'), 
             
             Command.W3C_ACCEPT_ALERT: ('POST', '/session/$sessionId/alert/accept'), 
             
             Command.SET_ALERT_VALUE: ('POST', '/session/$sessionId/alert_text'), 
             
             Command.W3C_SET_ALERT_VALUE: ('POST', '/session/$sessionId/alert/text'), 
             
             Command.GET_ALERT_TEXT: ('GET', '/session/$sessionId/alert_text'), 
             
             Command.W3C_GET_ALERT_TEXT: ('GET', '/session/$sessionId/alert/text'), 
             
             Command.SET_ALERT_CREDENTIALS: ('POST', '/session/$sessionId/alert/credentials'), 
             
             Command.CLICK: ('POST', '/session/$sessionId/click'), 
             
             Command.W3C_ACTIONS: ('POST', '/session/$sessionId/actions'), 
             
             Command.W3C_CLEAR_ACTIONS: ('DELETE', '/session/$sessionId/actions'), 
             
             Command.DOUBLE_CLICK: ('POST', '/session/$sessionId/doubleclick'), 
             
             Command.MOUSE_DOWN: ('POST', '/session/$sessionId/buttondown'), 
             
             Command.MOUSE_UP: ('POST', '/session/$sessionId/buttonup'), 
             
             Command.MOVE_TO: ('POST', '/session/$sessionId/moveto'), 
             
             Command.GET_WINDOW_SIZE: ('GET', '/session/$sessionId/window/$windowHandle/size'), 
             
             Command.SET_WINDOW_SIZE: ('POST', '/session/$sessionId/window/$windowHandle/size'), 
             
             Command.GET_WINDOW_POSITION: ('GET', '/session/$sessionId/window/$windowHandle/position'), 
             
             Command.SET_WINDOW_POSITION: ('POST', '/session/$sessionId/window/$windowHandle/position'), 
             
             Command.SET_WINDOW_RECT: ('POST', '/session/$sessionId/window/rect'), 
             
             Command.GET_WINDOW_RECT: ('GET', '/session/$sessionId/window/rect'), 
             
             Command.MAXIMIZE_WINDOW: ('POST', '/session/$sessionId/window/$windowHandle/maximize'), 
             
             Command.W3C_MAXIMIZE_WINDOW: ('POST', '/session/$sessionId/window/maximize'), 
             
             Command.SET_SCREEN_ORIENTATION: ('POST', '/session/$sessionId/orientation'), 
             
             Command.GET_SCREEN_ORIENTATION: ('GET', '/session/$sessionId/orientation'), 
             
             Command.SINGLE_TAP: ('POST', '/session/$sessionId/touch/click'), 
             
             Command.TOUCH_DOWN: ('POST', '/session/$sessionId/touch/down'), 
             
             Command.TOUCH_UP: ('POST', '/session/$sessionId/touch/up'), 
             
             Command.TOUCH_MOVE: ('POST', '/session/$sessionId/touch/move'), 
             
             Command.TOUCH_SCROLL: ('POST', '/session/$sessionId/touch/scroll'), 
             
             Command.DOUBLE_TAP: ('POST', '/session/$sessionId/touch/doubleclick'), 
             
             Command.LONG_PRESS: ('POST', '/session/$sessionId/touch/longclick'), 
             
             Command.FLICK: ('POST', '/session/$sessionId/touch/flick'), 
             
             Command.EXECUTE_SQL: ('POST', '/session/$sessionId/execute_sql'), 
             
             Command.GET_LOCATION: ('GET', '/session/$sessionId/location'), 
             
             Command.SET_LOCATION: ('POST', '/session/$sessionId/location'), 
             
             Command.GET_APP_CACHE: ('GET', '/session/$sessionId/application_cache'), 
             
             Command.GET_APP_CACHE_STATUS: ('GET', '/session/$sessionId/application_cache/status'), 
             
             Command.CLEAR_APP_CACHE: ('DELETE', '/session/$sessionId/application_cache/clear'), 
             
             Command.GET_NETWORK_CONNECTION: ('GET', '/session/$sessionId/network_connection'), 
             
             Command.SET_NETWORK_CONNECTION: ('POST', '/session/$sessionId/network_connection'), 
             
             Command.GET_LOCAL_STORAGE_ITEM: ('GET', '/session/$sessionId/local_storage/key/$key'), 
             
             Command.REMOVE_LOCAL_STORAGE_ITEM: ('DELETE', '/session/$sessionId/local_storage/key/$key'), 
             
             Command.GET_LOCAL_STORAGE_KEYS: ('GET', '/session/$sessionId/local_storage'), 
             
             Command.SET_LOCAL_STORAGE_ITEM: ('POST', '/session/$sessionId/local_storage'), 
             
             Command.CLEAR_LOCAL_STORAGE: ('DELETE', '/session/$sessionId/local_storage'), 
             
             Command.GET_LOCAL_STORAGE_SIZE: ('GET', '/session/$sessionId/local_storage/size'), 
             
             Command.GET_SESSION_STORAGE_ITEM: ('GET', '/session/$sessionId/session_storage/key/$key'), 
             
             Command.REMOVE_SESSION_STORAGE_ITEM: ('DELETE', '/session/$sessionId/session_storage/key/$key'), 
             
             Command.GET_SESSION_STORAGE_KEYS: ('GET', '/session/$sessionId/session_storage'), 
             
             Command.SET_SESSION_STORAGE_ITEM: ('POST', '/session/$sessionId/session_storage'), 
             
             Command.CLEAR_SESSION_STORAGE: ('DELETE', '/session/$sessionId/session_storage'), 
             
             Command.GET_SESSION_STORAGE_SIZE: ('GET', '/session/$sessionId/session_storage/size'), 
             
             Command.GET_LOG: ('POST', '/session/$sessionId/log'), 
             
             Command.GET_AVAILABLE_LOG_TYPES: ('GET', '/session/$sessionId/log/types'), 
             
             Command.CURRENT_CONTEXT_HANDLE: ('GET', '/session/$sessionId/context'), 
             
             Command.CONTEXT_HANDLES: ('GET', '/session/$sessionId/contexts'), 
             
             Command.SWITCH_TO_CONTEXT: ('POST', '/session/$sessionId/context'), 
             
             Command.FULLSCREEN_WINDOW: ('POST', '/session/$sessionId/window/fullscreen'), 
             
             Command.MINIMIZE_WINDOW: ('POST', '/session/$sessionId/window/minimize')}

        def execute(self, command, params):
            """
        Send a command to the remote server.

        Any path subtitutions required for the URL mapped to the command should be
        included in the command parameters.

        :Args:
         - command - A string specifying the command to execute.
         - params - A dictionary of named parameters to send with the command as
           its JSON payload.
        """
            command_info = self._commands[command]
            assert command_info is not None, 'Unrecognised command %s' % command
            path = string.Template(command_info[1]).substitute(params)
            if hasattr(self, 'w3c'):
                if self.w3c:
                    if isinstance(params, dict):
                        if 'sessionId' in params:
                            del params['sessionId']
            data = utils.dump_json(params)
            url = '%s%s' % (self._url, path)
            return self._request((command_info[0]), url, body=data)

        def _request--- This code section failed: ---

 L. 388         0  LOAD_GLOBAL              LOGGER
                2  LOAD_METHOD              debug
                4  LOAD_STR                 '%s %s %s'
                6  LOAD_FAST                'method'
                8  LOAD_FAST                'url'
               10  LOAD_FAST                'body'
               12  BUILD_TUPLE_3         3 
               14  BINARY_MODULO    
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L. 390        20  LOAD_GLOBAL              parse
               22  LOAD_METHOD              urlparse
               24  LOAD_FAST                'url'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'parsed_url'

 L. 391        30  LOAD_FAST                'self'
               32  LOAD_METHOD              get_remote_connection_headers
               34  LOAD_FAST                'parsed_url'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                keep_alive
               40  CALL_METHOD_2         2  ''
               42  STORE_FAST               'headers'

 L. 392        44  LOAD_CONST               None
               46  STORE_DEREF              'resp'

 L. 393        48  LOAD_FAST                'body'
               50  POP_JUMP_IF_FALSE    72  'to 72'
               52  LOAD_FAST                'method'
               54  LOAD_STR                 'POST'
               56  COMPARE_OP               !=
               58  POP_JUMP_IF_FALSE    72  'to 72'
               60  LOAD_FAST                'method'
               62  LOAD_STR                 'PUT'
               64  COMPARE_OP               !=
               66  POP_JUMP_IF_FALSE    72  'to 72'

 L. 394        68  LOAD_CONST               None
               70  STORE_FAST               'body'
             72_0  COME_FROM            66  '66'
             72_1  COME_FROM            58  '58'
             72_2  COME_FROM            50  '50'

 L. 396        72  LOAD_FAST                'self'
               74  LOAD_ATTR                keep_alive
               76  POP_JUMP_IF_FALSE   106  'to 106'

 L. 397        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _conn
               82  LOAD_ATTR                request
               84  LOAD_FAST                'method'
               86  LOAD_FAST                'url'
               88  LOAD_FAST                'body'
               90  LOAD_FAST                'headers'
               92  LOAD_CONST               ('body', 'headers')
               94  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               96  STORE_DEREF              'resp'

 L. 399        98  LOAD_DEREF               'resp'
              100  LOAD_ATTR                status
              102  STORE_FAST               'statuscode'
              104  JUMP_FORWARD        208  'to 208'
            106_0  COME_FROM            76  '76'

 L. 401       106  LOAD_GLOBAL              urllib3
              108  LOAD_ATTR                PoolManager
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                _timeout
              114  LOAD_CONST               ('timeout',)
              116  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              118  STORE_FAST               'http'

 L. 402       120  LOAD_FAST                'http'
              122  LOAD_ATTR                request
              124  LOAD_FAST                'method'
              126  LOAD_FAST                'url'
              128  LOAD_FAST                'body'
              130  LOAD_FAST                'headers'
              132  LOAD_CONST               ('body', 'headers')
              134  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              136  STORE_DEREF              'resp'

 L. 404       138  LOAD_DEREF               'resp'
              140  LOAD_ATTR                status
              142  STORE_FAST               'statuscode'

 L. 405       144  LOAD_GLOBAL              hasattr
              146  LOAD_DEREF               'resp'
              148  LOAD_STR                 'getheader'
              150  CALL_FUNCTION_2       2  ''
              152  POP_JUMP_IF_TRUE    208  'to 208'

 L. 406       154  LOAD_GLOBAL              hasattr
              156  LOAD_DEREF               'resp'
              158  LOAD_ATTR                headers
              160  LOAD_STR                 'getheader'
              162  CALL_FUNCTION_2       2  ''
              164  POP_JUMP_IF_FALSE   182  'to 182'

 L. 407       166  LOAD_CLOSURE             'resp'
              168  BUILD_TUPLE_1         1 
              170  LOAD_LAMBDA              '<code_object <lambda>>'
              172  LOAD_STR                 'RemoteConnection._request.<locals>.<lambda>'
              174  MAKE_FUNCTION_8          'closure'
              176  LOAD_DEREF               'resp'
              178  STORE_ATTR               getheader
              180  JUMP_FORWARD        208  'to 208'
            182_0  COME_FROM           164  '164'

 L. 408       182  LOAD_GLOBAL              hasattr
              184  LOAD_DEREF               'resp'
              186  LOAD_ATTR                headers
              188  LOAD_STR                 'get'
              190  CALL_FUNCTION_2       2  ''
              192  POP_JUMP_IF_FALSE   208  'to 208'

 L. 409       194  LOAD_CLOSURE             'resp'
              196  BUILD_TUPLE_1         1 
              198  LOAD_LAMBDA              '<code_object <lambda>>'
              200  LOAD_STR                 'RemoteConnection._request.<locals>.<lambda>'
              202  MAKE_FUNCTION_8          'closure'
              204  LOAD_DEREF               'resp'
              206  STORE_ATTR               getheader
            208_0  COME_FROM           192  '192'
            208_1  COME_FROM           180  '180'
            208_2  COME_FROM           152  '152'
            208_3  COME_FROM           104  '104'

 L. 411       208  LOAD_DEREF               'resp'
              210  LOAD_ATTR                data
              212  LOAD_METHOD              decode
              214  LOAD_STR                 'UTF-8'
              216  CALL_METHOD_1         1  ''
              218  STORE_FAST               'data'

 L. 412   220_222  SETUP_FINALLY       522  'to 522'

 L. 413       224  LOAD_CONST               300
              226  LOAD_FAST                'statuscode'
              228  DUP_TOP          
              230  ROT_THREE        
              232  COMPARE_OP               <=
              234  POP_JUMP_IF_FALSE   246  'to 246'
              236  LOAD_CONST               304
              238  COMPARE_OP               <
          240_242  POP_JUMP_IF_FALSE   274  'to 274'
              244  JUMP_FORWARD        250  'to 250'
            246_0  COME_FROM           234  '234'
              246  POP_TOP          
              248  JUMP_FORWARD        274  'to 274'
            250_0  COME_FROM           244  '244'

 L. 414       250  LOAD_FAST                'self'
              252  LOAD_METHOD              _request
              254  LOAD_STR                 'GET'
              256  LOAD_DEREF               'resp'
              258  LOAD_METHOD              getheader
              260  LOAD_STR                 'location'
              262  CALL_METHOD_1         1  ''
              264  CALL_METHOD_2         2  ''
              266  POP_BLOCK        
          268_270  CALL_FINALLY        522  'to 522'
              272  RETURN_VALUE     
            274_0  COME_FROM           248  '248'
            274_1  COME_FROM           240  '240'

 L. 415       274  LOAD_CONST               399
              276  LOAD_FAST                'statuscode'
              278  DUP_TOP          
              280  ROT_THREE        
              282  COMPARE_OP               <
          284_286  POP_JUMP_IF_FALSE   298  'to 298'
              288  LOAD_CONST               500
              290  COMPARE_OP               <=
          292_294  POP_JUMP_IF_FALSE   316  'to 316'
              296  JUMP_FORWARD        302  'to 302'
            298_0  COME_FROM           284  '284'
              298  POP_TOP          
              300  JUMP_FORWARD        316  'to 316'
            302_0  COME_FROM           296  '296'

 L. 416       302  LOAD_FAST                'statuscode'
              304  LOAD_FAST                'data'
              306  LOAD_CONST               ('status', 'value')
              308  BUILD_CONST_KEY_MAP_2     2 
              310  POP_BLOCK        
              312  CALL_FINALLY        522  'to 522'
              314  RETURN_VALUE     
            316_0  COME_FROM           300  '300'
            316_1  COME_FROM           292  '292'

 L. 417       316  BUILD_LIST_0          0 
              318  STORE_FAST               'content_type'

 L. 418       320  LOAD_DEREF               'resp'
              322  LOAD_METHOD              getheader
              324  LOAD_STR                 'Content-Type'
              326  CALL_METHOD_1         1  ''
              328  LOAD_CONST               None
              330  COMPARE_OP               is-not
          332_334  POP_JUMP_IF_FALSE   352  'to 352'

 L. 419       336  LOAD_DEREF               'resp'
              338  LOAD_METHOD              getheader
              340  LOAD_STR                 'Content-Type'
              342  CALL_METHOD_1         1  ''
              344  LOAD_METHOD              split
              346  LOAD_STR                 ';'
              348  CALL_METHOD_1         1  ''
              350  STORE_FAST               'content_type'
            352_0  COME_FROM           332  '332'

 L. 420       352  LOAD_GLOBAL              any
              354  LOAD_LISTCOMP            '<code_object <listcomp>>'
              356  LOAD_STR                 'RemoteConnection._request.<locals>.<listcomp>'
              358  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              360  LOAD_FAST                'content_type'
              362  GET_ITER         
              364  CALL_FUNCTION_1       1  ''
              366  CALL_FUNCTION_1       1  ''
          368_370  POP_JUMP_IF_TRUE    500  'to 500'

 L. 422       372  SETUP_FINALLY       392  'to 392'

 L. 423       374  LOAD_GLOBAL              utils
              376  LOAD_METHOD              load_json
              378  LOAD_FAST                'data'
              380  LOAD_METHOD              strip
              382  CALL_METHOD_0         0  ''
              384  CALL_METHOD_1         1  ''
              386  STORE_FAST               'data'
              388  POP_BLOCK        
              390  JUMP_FORWARD        474  'to 474'
            392_0  COME_FROM_FINALLY   372  '372'

 L. 424       392  DUP_TOP          
              394  LOAD_GLOBAL              ValueError
              396  COMPARE_OP               exception-match
          398_400  POP_JUMP_IF_FALSE   472  'to 472'
              402  POP_TOP          
              404  POP_TOP          
              406  POP_TOP          

 L. 425       408  LOAD_CONST               199
              410  LOAD_FAST                'statuscode'
              412  DUP_TOP          
              414  ROT_THREE        
              416  COMPARE_OP               <
          418_420  POP_JUMP_IF_FALSE   432  'to 432'
              422  LOAD_CONST               300
              424  COMPARE_OP               <
          426_428  POP_JUMP_IF_FALSE   444  'to 444'
              430  JUMP_FORWARD        436  'to 436'
            432_0  COME_FROM           418  '418'
              432  POP_TOP          
              434  JUMP_FORWARD        444  'to 444'
            436_0  COME_FROM           430  '430'

 L. 426       436  LOAD_GLOBAL              ErrorCode
              438  LOAD_ATTR                SUCCESS
              440  STORE_FAST               'status'
              442  JUMP_FORWARD        450  'to 450'
            444_0  COME_FROM           434  '434'
            444_1  COME_FROM           426  '426'

 L. 428       444  LOAD_GLOBAL              ErrorCode
              446  LOAD_ATTR                UNKNOWN_ERROR
              448  STORE_FAST               'status'
            450_0  COME_FROM           442  '442'

 L. 429       450  LOAD_FAST                'status'
              452  LOAD_FAST                'data'
              454  LOAD_METHOD              strip
              456  CALL_METHOD_0         0  ''
              458  LOAD_CONST               ('status', 'value')
              460  BUILD_CONST_KEY_MAP_2     2 
              462  ROT_FOUR         
              464  POP_EXCEPT       
              466  POP_BLOCK        
              468  CALL_FINALLY        522  'to 522'
              470  RETURN_VALUE     
            472_0  COME_FROM           398  '398'
              472  END_FINALLY      
            474_0  COME_FROM           390  '390'

 L. 433       474  LOAD_STR                 'value'
              476  LOAD_FAST                'data'
              478  COMPARE_OP               not-in
          480_482  POP_JUMP_IF_FALSE   492  'to 492'

 L. 434       484  LOAD_CONST               None
              486  LOAD_FAST                'data'
              488  LOAD_STR                 'value'
              490  STORE_SUBSCR     
            492_0  COME_FROM           480  '480'

 L. 435       492  LOAD_FAST                'data'
              494  POP_BLOCK        
              496  CALL_FINALLY        522  'to 522'
              498  RETURN_VALUE     
            500_0  COME_FROM           368  '368'

 L. 437       500  LOAD_CONST               0
              502  LOAD_FAST                'data'
              504  LOAD_CONST               ('status', 'value')
              506  BUILD_CONST_KEY_MAP_2     2 
              508  STORE_FAST               'data'

 L. 438       510  LOAD_FAST                'data'
              512  POP_BLOCK        
              514  CALL_FINALLY        522  'to 522'
              516  RETURN_VALUE     
              518  POP_BLOCK        
              520  BEGIN_FINALLY    
            522_0  COME_FROM           514  '514'
            522_1  COME_FROM           496  '496'
            522_2  COME_FROM           468  '468'
            522_3  COME_FROM           312  '312'
            522_4  COME_FROM           268  '268'
            522_5  COME_FROM_FINALLY   220  '220'

 L. 440       522  LOAD_GLOBAL              LOGGER
              524  LOAD_METHOD              debug
              526  LOAD_STR                 'Finished Request'
              528  CALL_METHOD_1         1  ''
              530  POP_TOP          

 L. 441       532  LOAD_DEREF               'resp'
              534  LOAD_METHOD              close
              536  CALL_METHOD_0         0  ''
              538  POP_TOP          
              540  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 268_270