# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\connectionpool.py
from __future__ import absolute_import
import errno, logging, socket, sys, warnings
from socket import error as SocketError
from socket import timeout as SocketTimeout
from .connection import BaseSSLError, BrokenPipeError, DummyConnection, HTTPConnection, HTTPException, HTTPSConnection, VerifiedHTTPSConnection, port_by_scheme
from .exceptions import ClosedPoolError, EmptyPoolError, HeaderParsingError, HostChangedError, InsecureRequestWarning, LocationValueError, MaxRetryError, NewConnectionError, ProtocolError, ProxyError, ReadTimeoutError, SSLError, TimeoutError
from .packages import six
from packages.six.moves import queue
from packages.ssl_match_hostname import CertificateError
from .request import RequestMethods
from .response import HTTPResponse
from util.connection import is_connection_dropped
from util.proxy import connection_requires_http_tunnel
from util.queue import LifoQueue
from util.request import set_file_position
from util.response import assert_header_parsing
from util.retry import Retry
from util.timeout import Timeout
from util.url import Url, _encode_target
import util.url as normalize_host
from util.url import get_host, parse_url
xrange = six.moves.xrange
log = logging.getLogger(__name__)
_Default = object()

class ConnectionPool(object):
    __doc__ = "\n    Base class for all connection pools, such as\n    :class:`.HTTPConnectionPool` and :class:`.HTTPSConnectionPool`.\n\n    .. note::\n       ConnectionPool.urlopen() does not normalize or percent-encode target URIs\n       which is useful if your target server doesn't support percent-encoded\n       target URIs.\n    "
    scheme = None
    QueueCls = LifoQueue

    def __init__(self, host, port=None):
        if not host:
            raise LocationValueError('No host specified.')
        self.host = _normalize_host(host, scheme=(self.scheme))
        self._proxy_host = host.lower()
        self.port = port

    def __str__(self):
        return '%s(host=%r, port=%r)' % (type(self).__name__, self.host, self.port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def close(self):
        """
        Close all pooled connections and disable the pool.
        """
        pass


_blocking_errnos = {
 errno.EAGAIN, errno.EWOULDBLOCK}

class HTTPConnectionPool(ConnectionPool, RequestMethods):
    __doc__ = '\n    Thread-safe connection pool for one host.\n\n    :param host:\n        Host used for this HTTP Connection (e.g. "localhost"), passed into\n        :class:`http.client.HTTPConnection`.\n\n    :param port:\n        Port used for this HTTP Connection (None is equivalent to 80), passed\n        into :class:`http.client.HTTPConnection`.\n\n    :param strict:\n        Causes BadStatusLine to be raised if the status line can\'t be parsed\n        as a valid HTTP/1.0 or 1.1 status line, passed into\n        :class:`http.client.HTTPConnection`.\n\n        .. note::\n           Only works in Python 2. This parameter is ignored in Python 3.\n\n    :param timeout:\n        Socket timeout in seconds for each individual connection. This can\n        be a float or integer, which sets the timeout for the HTTP request,\n        or an instance of :class:`urllib3.util.Timeout` which gives you more\n        fine-grained control over request timeouts. After the constructor has\n        been parsed, this is always a `urllib3.util.Timeout` object.\n\n    :param maxsize:\n        Number of connections to save that can be reused. More than 1 is useful\n        in multithreaded situations. If ``block`` is set to False, more\n        connections will be created but they will not be saved once they\'ve\n        been used.\n\n    :param block:\n        If set to True, no more than ``maxsize`` connections will be used at\n        a time. When no free connections are available, the call will block\n        until a connection has been released. This is a useful side effect for\n        particular multithreaded situations where one does not want to use more\n        than maxsize connections per host to prevent flooding.\n\n    :param headers:\n        Headers to include with all requests, unless other headers are given\n        explicitly.\n\n    :param retries:\n        Retry configuration to use by default with requests in this pool.\n\n    :param _proxy:\n        Parsed proxy URL, should not be used directly, instead, see\n        :class:`urllib3.ProxyManager`\n\n    :param _proxy_headers:\n        A dictionary with proxy headers, should not be used directly,\n        instead, see :class:`urllib3.ProxyManager`\n\n    :param \\**conn_kw:\n        Additional parameters are used to create fresh :class:`urllib3.connection.HTTPConnection`,\n        :class:`urllib3.connection.HTTPSConnection` instances.\n    '
    scheme = 'http'
    ConnectionCls = HTTPConnection
    ResponseCls = HTTPResponse

    def __init__--- This code section failed: ---

 L. 183         0  LOAD_GLOBAL              ConnectionPool
                2  LOAD_METHOD              __init__
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'host'
                8  LOAD_FAST                'port'
               10  CALL_METHOD_3         3  ''
               12  POP_TOP          

 L. 184        14  LOAD_GLOBAL              RequestMethods
               16  LOAD_METHOD              __init__
               18  LOAD_FAST                'self'
               20  LOAD_FAST                'headers'
               22  CALL_METHOD_2         2  ''
               24  POP_TOP          

 L. 186        26  LOAD_FAST                'strict'
               28  LOAD_FAST                'self'
               30  STORE_ATTR               strict

 L. 188        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'timeout'
               36  LOAD_GLOBAL              Timeout
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_TRUE     52  'to 52'

 L. 189        42  LOAD_GLOBAL              Timeout
               44  LOAD_METHOD              from_float
               46  LOAD_FAST                'timeout'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'timeout'
             52_0  COME_FROM            40  '40'

 L. 191        52  LOAD_FAST                'retries'
               54  LOAD_CONST               None
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 192        60  LOAD_GLOBAL              Retry
               62  LOAD_ATTR                DEFAULT
               64  STORE_FAST               'retries'
             66_0  COME_FROM            58  '58'

 L. 194        66  LOAD_FAST                'timeout'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               timeout

 L. 195        72  LOAD_FAST                'retries'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               retries

 L. 197        78  LOAD_FAST                'self'
               80  LOAD_METHOD              QueueCls
               82  LOAD_FAST                'maxsize'
               84  CALL_METHOD_1         1  ''
               86  LOAD_FAST                'self'
               88  STORE_ATTR               pool

 L. 198        90  LOAD_FAST                'block'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               block

 L. 200        96  LOAD_FAST                '_proxy'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               proxy

 L. 201       102  LOAD_FAST                '_proxy_headers'
              104  JUMP_IF_TRUE_OR_POP   108  'to 108'
              106  BUILD_MAP_0           0 
            108_0  COME_FROM           104  '104'
              108  LOAD_FAST                'self'
              110  STORE_ATTR               proxy_headers

 L. 202       112  LOAD_FAST                '_proxy_config'
              114  LOAD_FAST                'self'
              116  STORE_ATTR               proxy_config

 L. 205       118  LOAD_GLOBAL              xrange
              120  LOAD_FAST                'maxsize'
              122  CALL_FUNCTION_1       1  ''
              124  GET_ITER         
            126_0  COME_FROM           142  '142'
              126  FOR_ITER            144  'to 144'
              128  STORE_FAST               '_'

 L. 206       130  LOAD_FAST                'self'
              132  LOAD_ATTR                pool
              134  LOAD_METHOD              put
              136  LOAD_CONST               None
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_BACK           126  'to 126'
            144_0  COME_FROM           126  '126'

 L. 209       144  LOAD_CONST               0
              146  LOAD_FAST                'self'
              148  STORE_ATTR               num_connections

 L. 210       150  LOAD_CONST               0
              152  LOAD_FAST                'self'
              154  STORE_ATTR               num_requests

 L. 211       156  LOAD_FAST                'conn_kw'
              158  LOAD_FAST                'self'
              160  STORE_ATTR               conn_kw

 L. 213       162  LOAD_FAST                'self'
              164  LOAD_ATTR                proxy
              166  POP_JUMP_IF_FALSE   206  'to 206'

 L. 217       168  LOAD_FAST                'self'
              170  LOAD_ATTR                conn_kw
              172  LOAD_METHOD              setdefault
              174  LOAD_STR                 'socket_options'
              176  BUILD_LIST_0          0 
              178  CALL_METHOD_2         2  ''
              180  POP_TOP          

 L. 219       182  LOAD_FAST                'self'
              184  LOAD_ATTR                proxy
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                conn_kw
              190  LOAD_STR                 'proxy'
              192  STORE_SUBSCR     

 L. 220       194  LOAD_FAST                'self'
              196  LOAD_ATTR                proxy_config
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                conn_kw
              202  LOAD_STR                 'proxy_config'
              204  STORE_SUBSCR     
            206_0  COME_FROM           166  '166'

Parse error at or near `<117>' instruction at offset 56

    def _new_conn--- This code section failed: ---

 L. 226         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                num_connections
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               num_connections

 L. 227        14  LOAD_GLOBAL              log
               16  LOAD_METHOD              debug

 L. 228        18  LOAD_STR                 'Starting new HTTP connection (%d): %s:%s'

 L. 229        20  LOAD_FAST                'self'
               22  LOAD_ATTR                num_connections

 L. 230        24  LOAD_FAST                'self'
               26  LOAD_ATTR                host

 L. 231        28  LOAD_FAST                'self'
               30  LOAD_ATTR                port
               32  JUMP_IF_TRUE_OR_POP    36  'to 36'
               34  LOAD_STR                 '80'
             36_0  COME_FROM            32  '32'

 L. 227        36  CALL_METHOD_4         4  ''
               38  POP_TOP          

 L. 234        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ConnectionCls
               44  BUILD_TUPLE_0         0 

 L. 235        46  LOAD_FAST                'self'
               48  LOAD_ATTR                host

 L. 236        50  LOAD_FAST                'self'
               52  LOAD_ATTR                port

 L. 237        54  LOAD_FAST                'self'
               56  LOAD_ATTR                timeout
               58  LOAD_ATTR                connect_timeout

 L. 238        60  LOAD_FAST                'self'
               62  LOAD_ATTR                strict

 L. 234        64  LOAD_CONST               ('host', 'port', 'timeout', 'strict')
               66  BUILD_CONST_KEY_MAP_4     4 

 L. 239        68  LOAD_FAST                'self'
               70  LOAD_ATTR                conn_kw

 L. 234        72  <164>                 1  ''
               74  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               76  STORE_FAST               'conn'

 L. 241        78  LOAD_FAST                'conn'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 72

    def _get_conn--- This code section failed: ---

 L. 255         0  LOAD_CONST               None
                2  STORE_FAST               'conn'

 L. 256         4  SETUP_FINALLY        28  'to 28'

 L. 257         6  LOAD_FAST                'self'
                8  LOAD_ATTR                pool
               10  LOAD_ATTR                get
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                block
               16  LOAD_FAST                'timeout'
               18  LOAD_CONST               ('block', 'timeout')
               20  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               22  STORE_FAST               'conn'
               24  POP_BLOCK        
               26  JUMP_FORWARD         90  'to 90'
             28_0  COME_FROM_FINALLY     4  '4'

 L. 259        28  DUP_TOP          
               30  LOAD_GLOBAL              AttributeError
               32  <121>                54  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 260        40  LOAD_GLOBAL              ClosedPoolError
               42  LOAD_FAST                'self'
               44  LOAD_STR                 'Pool is closed.'
               46  CALL_FUNCTION_2       2  ''
               48  RAISE_VARARGS_1       1  'exception instance'
               50  POP_EXCEPT       
               52  JUMP_FORWARD         90  'to 90'

 L. 262        54  DUP_TOP          
               56  LOAD_GLOBAL              queue
               58  LOAD_ATTR                Empty
               60  <121>                88  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 263        68  LOAD_FAST                'self'
               70  LOAD_ATTR                block
               72  POP_JUMP_IF_FALSE    84  'to 84'

 L. 264        74  LOAD_GLOBAL              EmptyPoolError

 L. 265        76  LOAD_FAST                'self'

 L. 266        78  LOAD_STR                 'Pool reached maximum size and no more connections are allowed.'

 L. 264        80  CALL_FUNCTION_2       2  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            72  '72'

 L. 268        84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
               88  <48>             
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            52  '52'
             90_2  COME_FROM            26  '26'

 L. 271        90  LOAD_FAST                'conn'
               92  POP_JUMP_IF_FALSE   144  'to 144'
               94  LOAD_GLOBAL              is_connection_dropped
               96  LOAD_FAST                'conn'
               98  CALL_FUNCTION_1       1  ''
              100  POP_JUMP_IF_FALSE   144  'to 144'

 L. 272       102  LOAD_GLOBAL              log
              104  LOAD_METHOD              debug
              106  LOAD_STR                 'Resetting dropped connection: %s'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                host
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          

 L. 273       116  LOAD_FAST                'conn'
              118  LOAD_METHOD              close
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          

 L. 274       124  LOAD_GLOBAL              getattr
              126  LOAD_FAST                'conn'
              128  LOAD_STR                 'auto_open'
              130  LOAD_CONST               1
              132  CALL_FUNCTION_3       3  ''
              134  LOAD_CONST               0
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   144  'to 144'

 L. 278       140  LOAD_CONST               None
              142  STORE_FAST               'conn'
            144_0  COME_FROM           138  '138'
            144_1  COME_FROM           100  '100'
            144_2  COME_FROM            92  '92'

 L. 280       144  LOAD_FAST                'conn'
              146  JUMP_IF_TRUE_OR_POP   154  'to 154'
              148  LOAD_FAST                'self'
              150  LOAD_METHOD              _new_conn
              152  CALL_METHOD_0         0  ''
            154_0  COME_FROM           146  '146'
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 32

    def _put_conn--- This code section failed: ---

 L. 296         0  SETUP_FINALLY        24  'to 24'

 L. 297         2  LOAD_FAST                'self'
                4  LOAD_ATTR                pool
                6  LOAD_ATTR                put
                8  LOAD_FAST                'conn'
               10  LOAD_CONST               False
               12  LOAD_CONST               ('block',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  POP_TOP          

 L. 298        18  POP_BLOCK        
               20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L. 299        24  DUP_TOP          
               26  LOAD_GLOBAL              AttributeError
               28  <121>                40  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 301        36  POP_EXCEPT       
               38  JUMP_FORWARD         74  'to 74'

 L. 302        40  DUP_TOP          
               42  LOAD_GLOBAL              queue
               44  LOAD_ATTR                Full
               46  <121>                72  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 304        54  LOAD_GLOBAL              log
               56  LOAD_METHOD              warning
               58  LOAD_STR                 'Connection pool is full, discarding connection: %s'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                host
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
               72  <48>             
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            38  '38'

 L. 307        74  LOAD_FAST                'conn'
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 308        78  LOAD_FAST                'conn'
               80  LOAD_METHOD              close
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          
             86_0  COME_FROM            76  '76'

Parse error at or near `DUP_TOP' instruction at offset 24

    def _validate_conn(self, conn):
        """
        Called right before a request is made, after the socket is created.
        """
        pass

    def _prepare_proxy(self, conn):
        pass

    def _get_timeout--- This code section failed: ---

 L. 322         0  LOAD_FAST                'timeout'
                2  LOAD_GLOBAL              _Default
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 323         8  LOAD_FAST                'self'
               10  LOAD_ATTR                timeout
               12  LOAD_METHOD              clone
               14  CALL_METHOD_0         0  ''
               16  RETURN_VALUE     
             18_0  COME_FROM             6  '6'

 L. 325        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'timeout'
               22  LOAD_GLOBAL              Timeout
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 326        28  LOAD_FAST                'timeout'
               30  LOAD_METHOD              clone
               32  CALL_METHOD_0         0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM            26  '26'

 L. 330        36  LOAD_GLOBAL              Timeout
               38  LOAD_METHOD              from_float
               40  LOAD_FAST                'timeout'
               42  CALL_METHOD_1         1  ''
               44  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def _raise_timeout--- This code section failed: ---

 L. 335         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'err'
                4  LOAD_GLOBAL              SocketTimeout
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 336        10  LOAD_GLOBAL              ReadTimeoutError

 L. 337        12  LOAD_FAST                'self'
               14  LOAD_FAST                'url'
               16  LOAD_STR                 'Read timed out. (read timeout=%s)'
               18  LOAD_FAST                'timeout_value'
               20  BINARY_MODULO    

 L. 336        22  CALL_FUNCTION_3       3  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 342        26  LOAD_GLOBAL              hasattr
               28  LOAD_FAST                'err'
               30  LOAD_STR                 'errno'
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE    62  'to 62'
               36  LOAD_FAST                'err'
               38  LOAD_ATTR                errno
               40  LOAD_GLOBAL              _blocking_errnos
               42  <118>                 0  ''
               44  POP_JUMP_IF_FALSE    62  'to 62'

 L. 343        46  LOAD_GLOBAL              ReadTimeoutError

 L. 344        48  LOAD_FAST                'self'
               50  LOAD_FAST                'url'
               52  LOAD_STR                 'Read timed out. (read timeout=%s)'
               54  LOAD_FAST                'timeout_value'
               56  BINARY_MODULO    

 L. 343        58  CALL_FUNCTION_3       3  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            44  '44'
             62_1  COME_FROM            34  '34'

 L. 350        62  LOAD_STR                 'timed out'
               64  LOAD_GLOBAL              str
               66  LOAD_FAST                'err'
               68  CALL_FUNCTION_1       1  ''
               70  <118>                 0  ''
               72  POP_JUMP_IF_TRUE     86  'to 86'
               74  LOAD_STR                 'did not complete (read)'
               76  LOAD_GLOBAL              str

 L. 351        78  LOAD_FAST                'err'

 L. 350        80  CALL_FUNCTION_1       1  ''
               82  <118>                 0  ''
               84  POP_JUMP_IF_FALSE   102  'to 102'
             86_0  COME_FROM            72  '72'

 L. 353        86  LOAD_GLOBAL              ReadTimeoutError

 L. 354        88  LOAD_FAST                'self'
               90  LOAD_FAST                'url'
               92  LOAD_STR                 'Read timed out. (read timeout=%s)'
               94  LOAD_FAST                'timeout_value'
               96  BINARY_MODULO    

 L. 353        98  CALL_FUNCTION_3       3  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            84  '84'

Parse error at or near `<118>' instruction at offset 42

    def _make_request--- This code section failed: ---

 L. 374         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                num_requests
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               num_requests

 L. 376        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _get_timeout
               18  LOAD_FAST                'timeout'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'timeout_obj'

 L. 377        24  LOAD_FAST                'timeout_obj'
               26  LOAD_METHOD              start_connect
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          

 L. 378        32  LOAD_FAST                'timeout_obj'
               34  LOAD_ATTR                connect_timeout
               36  LOAD_FAST                'conn'
               38  STORE_ATTR               timeout

 L. 381        40  SETUP_FINALLY        56  'to 56'

 L. 382        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _validate_conn
               46  LOAD_FAST                'conn'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
               52  POP_BLOCK        
               54  JUMP_FORWARD        116  'to 116'
             56_0  COME_FROM_FINALLY    40  '40'

 L. 383        56  DUP_TOP          
               58  LOAD_GLOBAL              SocketTimeout
               60  LOAD_GLOBAL              BaseSSLError
               62  BUILD_TUPLE_2         2 
               64  <121>               114  ''
               66  POP_TOP          
               68  STORE_FAST               'e'
               70  POP_TOP          
               72  SETUP_FINALLY       106  'to 106'

 L. 385        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _raise_timeout
               78  LOAD_FAST                'e'
               80  LOAD_FAST                'url'
               82  LOAD_FAST                'conn'
               84  LOAD_ATTR                timeout
               86  LOAD_CONST               ('err', 'url', 'timeout_value')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  POP_TOP          

 L. 386        92  RAISE_VARARGS_0       0  'reraise'
               94  POP_BLOCK        
               96  POP_EXCEPT       
               98  LOAD_CONST               None
              100  STORE_FAST               'e'
              102  DELETE_FAST              'e'
              104  JUMP_FORWARD        116  'to 116'
            106_0  COME_FROM_FINALLY    72  '72'
              106  LOAD_CONST               None
              108  STORE_FAST               'e'
              110  DELETE_FAST              'e'
              112  <48>             
              114  <48>             
            116_0  COME_FROM           104  '104'
            116_1  COME_FROM            54  '54'

 L. 390       116  SETUP_FINALLY       168  'to 168'

 L. 391       118  LOAD_FAST                'chunked'
              120  POP_JUMP_IF_FALSE   144  'to 144'

 L. 392       122  LOAD_FAST                'conn'
              124  LOAD_ATTR                request_chunked
              126  LOAD_FAST                'method'
              128  LOAD_FAST                'url'
              130  BUILD_TUPLE_2         2 
              132  BUILD_MAP_0           0 
              134  LOAD_FAST                'httplib_request_kw'
              136  <164>                 1  ''
              138  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              140  POP_TOP          
              142  JUMP_FORWARD        164  'to 164'
            144_0  COME_FROM           120  '120'

 L. 394       144  LOAD_FAST                'conn'
              146  LOAD_ATTR                request
              148  LOAD_FAST                'method'
              150  LOAD_FAST                'url'
              152  BUILD_TUPLE_2         2 
              154  BUILD_MAP_0           0 
              156  LOAD_FAST                'httplib_request_kw'
              158  <164>                 1  ''
              160  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              162  POP_TOP          
            164_0  COME_FROM           142  '142'
              164  POP_BLOCK        
              166  JUMP_FORWARD        244  'to 244'
            168_0  COME_FROM_FINALLY   116  '116'

 L. 399       168  DUP_TOP          
              170  LOAD_GLOBAL              BrokenPipeError
              172  <121>               184  ''
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          

 L. 401       180  POP_EXCEPT       
              182  JUMP_FORWARD        244  'to 244'

 L. 402       184  DUP_TOP          
              186  LOAD_GLOBAL              IOError
              188  <121>               242  ''
              190  POP_TOP          
              192  STORE_FAST               'e'
              194  POP_TOP          
              196  SETUP_FINALLY       234  'to 234'

 L. 406       198  LOAD_FAST                'e'
              200  LOAD_ATTR                errno

 L. 407       202  LOAD_GLOBAL              errno
              204  LOAD_ATTR                EPIPE

 L. 408       206  LOAD_GLOBAL              errno
              208  LOAD_ATTR                ESHUTDOWN

 L. 409       210  LOAD_GLOBAL              errno
              212  LOAD_ATTR                EPROTOTYPE

 L. 406       214  BUILD_SET_3           3 
              216  <118>                 1  ''
              218  POP_JUMP_IF_FALSE   222  'to 222'

 L. 411       220  RAISE_VARARGS_0       0  'reraise'
            222_0  COME_FROM           218  '218'
              222  POP_BLOCK        
              224  POP_EXCEPT       
              226  LOAD_CONST               None
              228  STORE_FAST               'e'
              230  DELETE_FAST              'e'
              232  JUMP_FORWARD        244  'to 244'
            234_0  COME_FROM_FINALLY   196  '196'
              234  LOAD_CONST               None
              236  STORE_FAST               'e'
              238  DELETE_FAST              'e'
              240  <48>             
              242  <48>             
            244_0  COME_FROM           232  '232'
            244_1  COME_FROM           182  '182'
            244_2  COME_FROM           166  '166'

 L. 414       244  LOAD_FAST                'timeout_obj'
              246  LOAD_ATTR                read_timeout
              248  STORE_FAST               'read_timeout'

 L. 417       250  LOAD_GLOBAL              getattr
              252  LOAD_FAST                'conn'
              254  LOAD_STR                 'sock'
              256  LOAD_CONST               None
              258  CALL_FUNCTION_3       3  ''
          260_262  POP_JUMP_IF_FALSE   332  'to 332'

 L. 423       264  LOAD_FAST                'read_timeout'
              266  LOAD_CONST               0
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   290  'to 290'

 L. 424       274  LOAD_GLOBAL              ReadTimeoutError

 L. 425       276  LOAD_FAST                'self'
              278  LOAD_FAST                'url'
              280  LOAD_STR                 'Read timed out. (read timeout=%s)'
              282  LOAD_FAST                'read_timeout'
              284  BINARY_MODULO    

 L. 424       286  CALL_FUNCTION_3       3  ''
              288  RAISE_VARARGS_1       1  'exception instance'
            290_0  COME_FROM           270  '270'

 L. 427       290  LOAD_FAST                'read_timeout'
              292  LOAD_GLOBAL              Timeout
              294  LOAD_ATTR                DEFAULT_TIMEOUT
              296  <117>                 0  ''
          298_300  POP_JUMP_IF_FALSE   320  'to 320'

 L. 428       302  LOAD_FAST                'conn'
              304  LOAD_ATTR                sock
              306  LOAD_METHOD              settimeout
              308  LOAD_GLOBAL              socket
              310  LOAD_METHOD              getdefaulttimeout
              312  CALL_METHOD_0         0  ''
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          
              318  JUMP_FORWARD        332  'to 332'
            320_0  COME_FROM           298  '298'

 L. 430       320  LOAD_FAST                'conn'
              322  LOAD_ATTR                sock
              324  LOAD_METHOD              settimeout
              326  LOAD_FAST                'read_timeout'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
            332_0  COME_FROM           318  '318'
            332_1  COME_FROM           260  '260'

 L. 433       332  SETUP_FINALLY       440  'to 440'

 L. 434       334  SETUP_FINALLY       352  'to 352'

 L. 436       336  LOAD_FAST                'conn'
              338  LOAD_ATTR                getresponse
              340  LOAD_CONST               True
              342  LOAD_CONST               ('buffering',)
              344  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              346  STORE_FAST               'httplib_response'
              348  POP_BLOCK        
              350  JUMP_FORWARD        436  'to 436'
            352_0  COME_FROM_FINALLY   334  '334'

 L. 437       352  DUP_TOP          
              354  LOAD_GLOBAL              TypeError
          356_358  <121>               434  ''
              360  POP_TOP          
              362  POP_TOP          
              364  POP_TOP          

 L. 439       366  SETUP_FINALLY       380  'to 380'

 L. 440       368  LOAD_FAST                'conn'
              370  LOAD_METHOD              getresponse
              372  CALL_METHOD_0         0  ''
              374  STORE_FAST               'httplib_response'
              376  POP_BLOCK        
              378  JUMP_FORWARD        430  'to 430'
            380_0  COME_FROM_FINALLY   366  '366'

 L. 441       380  DUP_TOP          
              382  LOAD_GLOBAL              BaseException
          384_386  <121>               428  ''
              388  POP_TOP          
              390  STORE_FAST               'e'
              392  POP_TOP          
              394  SETUP_FINALLY       420  'to 420'

 L. 445       396  LOAD_GLOBAL              six
              398  LOAD_METHOD              raise_from
              400  LOAD_FAST                'e'
              402  LOAD_CONST               None
              404  CALL_METHOD_2         2  ''
              406  POP_TOP          
              408  POP_BLOCK        
              410  POP_EXCEPT       
              412  LOAD_CONST               None
              414  STORE_FAST               'e'
              416  DELETE_FAST              'e'
              418  JUMP_FORWARD        430  'to 430'
            420_0  COME_FROM_FINALLY   394  '394'
              420  LOAD_CONST               None
              422  STORE_FAST               'e'
              424  DELETE_FAST              'e'
              426  <48>             
              428  <48>             
            430_0  COME_FROM           418  '418'
            430_1  COME_FROM           378  '378'
              430  POP_EXCEPT       
              432  JUMP_FORWARD        436  'to 436'
              434  <48>             
            436_0  COME_FROM           432  '432'
            436_1  COME_FROM           350  '350'
              436  POP_BLOCK        
              438  JUMP_FORWARD        502  'to 502'
            440_0  COME_FROM_FINALLY   332  '332'

 L. 446       440  DUP_TOP          
              442  LOAD_GLOBAL              SocketTimeout
              444  LOAD_GLOBAL              BaseSSLError
              446  LOAD_GLOBAL              SocketError
              448  BUILD_TUPLE_3         3 
          450_452  <121>               500  ''
              454  POP_TOP          
              456  STORE_FAST               'e'
              458  POP_TOP          
              460  SETUP_FINALLY       492  'to 492'

 L. 447       462  LOAD_FAST                'self'
              464  LOAD_ATTR                _raise_timeout
              466  LOAD_FAST                'e'
              468  LOAD_FAST                'url'
              470  LOAD_FAST                'read_timeout'
              472  LOAD_CONST               ('err', 'url', 'timeout_value')
              474  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              476  POP_TOP          

 L. 448       478  RAISE_VARARGS_0       0  'reraise'
              480  POP_BLOCK        
              482  POP_EXCEPT       
              484  LOAD_CONST               None
              486  STORE_FAST               'e'
              488  DELETE_FAST              'e'
              490  JUMP_FORWARD        502  'to 502'
            492_0  COME_FROM_FINALLY   460  '460'
              492  LOAD_CONST               None
              494  STORE_FAST               'e'
              496  DELETE_FAST              'e'
              498  <48>             
              500  <48>             
            502_0  COME_FROM           490  '490'
            502_1  COME_FROM           438  '438'

 L. 451       502  LOAD_GLOBAL              getattr
              504  LOAD_FAST                'conn'
              506  LOAD_STR                 '_http_vsn_str'
              508  LOAD_STR                 'HTTP/?'
              510  CALL_FUNCTION_3       3  ''
              512  STORE_FAST               'http_version'

 L. 452       514  LOAD_GLOBAL              log
              516  LOAD_METHOD              debug

 L. 453       518  LOAD_STR                 '%s://%s:%s "%s %s %s" %s %s'

 L. 454       520  LOAD_FAST                'self'
              522  LOAD_ATTR                scheme

 L. 455       524  LOAD_FAST                'self'
              526  LOAD_ATTR                host

 L. 456       528  LOAD_FAST                'self'
              530  LOAD_ATTR                port

 L. 457       532  LOAD_FAST                'method'

 L. 458       534  LOAD_FAST                'url'

 L. 459       536  LOAD_FAST                'http_version'

 L. 460       538  LOAD_FAST                'httplib_response'
              540  LOAD_ATTR                status

 L. 461       542  LOAD_FAST                'httplib_response'
              544  LOAD_ATTR                length

 L. 452       546  CALL_METHOD_9         9  ''
              548  POP_TOP          

 L. 464       550  SETUP_FINALLY       566  'to 566'

 L. 465       552  LOAD_GLOBAL              assert_header_parsing
              554  LOAD_FAST                'httplib_response'
              556  LOAD_ATTR                msg
              558  CALL_FUNCTION_1       1  ''
              560  POP_TOP          
              562  POP_BLOCK        
              564  JUMP_FORWARD        632  'to 632'
            566_0  COME_FROM_FINALLY   550  '550'

 L. 466       566  DUP_TOP          
              568  LOAD_GLOBAL              HeaderParsingError
              570  LOAD_GLOBAL              TypeError
              572  BUILD_TUPLE_2         2 
          574_576  <121>               630  ''
              578  POP_TOP          
              580  STORE_FAST               'hpe'
              582  POP_TOP          
              584  SETUP_FINALLY       622  'to 622'

 L. 467       586  LOAD_GLOBAL              log
              588  LOAD_ATTR                warning

 L. 468       590  LOAD_STR                 'Failed to parse headers (url=%s): %s'

 L. 469       592  LOAD_FAST                'self'
              594  LOAD_METHOD              _absolute_url
              596  LOAD_FAST                'url'
              598  CALL_METHOD_1         1  ''

 L. 470       600  LOAD_FAST                'hpe'

 L. 471       602  LOAD_CONST               True

 L. 467       604  LOAD_CONST               ('exc_info',)
              606  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              608  POP_TOP          
              610  POP_BLOCK        
              612  POP_EXCEPT       
              614  LOAD_CONST               None
              616  STORE_FAST               'hpe'
              618  DELETE_FAST              'hpe'
              620  JUMP_FORWARD        632  'to 632'
            622_0  COME_FROM_FINALLY   584  '584'
              622  LOAD_CONST               None
              624  STORE_FAST               'hpe'
              626  DELETE_FAST              'hpe'
              628  <48>             
              630  <48>             
            632_0  COME_FROM           620  '620'
            632_1  COME_FROM           564  '564'

 L. 474       632  LOAD_FAST                'httplib_response'
              634  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 64

    def _absolute_url(self, path):
        return Url(scheme=(self.scheme), host=(self.host), port=(self.port), path=path).url

    def close--- This code section failed: ---

 L. 483         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pool
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 484        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 486        14  LOAD_FAST                'self'
               16  LOAD_ATTR                pool
               18  LOAD_CONST               None
               20  ROT_TWO          
               22  STORE_FAST               'old_pool'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               pool

 L. 488        28  SETUP_FINALLY        60  'to 60'
             30_0  COME_FROM            54  '54'
             30_1  COME_FROM            44  '44'

 L. 490        30  LOAD_FAST                'old_pool'
               32  LOAD_ATTR                get
               34  LOAD_CONST               False
               36  LOAD_CONST               ('block',)
               38  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               40  STORE_FAST               'conn'

 L. 491        42  LOAD_FAST                'conn'
               44  POP_JUMP_IF_FALSE_BACK    30  'to 30'

 L. 492        46  LOAD_FAST                'conn'
               48  LOAD_METHOD              close
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          
               54  JUMP_BACK            30  'to 30'
               56  POP_BLOCK        
               58  JUMP_FORWARD         80  'to 80'
             60_0  COME_FROM_FINALLY    28  '28'

 L. 494        60  DUP_TOP          
               62  LOAD_GLOBAL              queue
               64  LOAD_ATTR                Empty
               66  <121>                78  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 495        74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
               78  <48>             
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            58  '58'

Parse error at or near `None' instruction at offset -1

    def is_same_host--- This code section failed: ---

 L. 502         0  LOAD_FAST                'url'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 503        10  LOAD_CONST               True
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 506        14  LOAD_GLOBAL              get_host
               16  LOAD_FAST                'url'
               18  CALL_FUNCTION_1       1  ''
               20  UNPACK_SEQUENCE_3     3 
               22  STORE_FAST               'scheme'
               24  STORE_FAST               'host'
               26  STORE_FAST               'port'

 L. 507        28  LOAD_FAST                'host'
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    48  'to 48'

 L. 508        36  LOAD_GLOBAL              _normalize_host
               38  LOAD_FAST                'host'
               40  LOAD_FAST                'scheme'
               42  LOAD_CONST               ('scheme',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  STORE_FAST               'host'
             48_0  COME_FROM            34  '34'

 L. 511        48  LOAD_FAST                'self'
               50  LOAD_ATTR                port
               52  POP_JUMP_IF_FALSE    70  'to 70'
               54  LOAD_FAST                'port'
               56  POP_JUMP_IF_TRUE     70  'to 70'

 L. 512        58  LOAD_GLOBAL              port_by_scheme
               60  LOAD_METHOD              get
               62  LOAD_FAST                'scheme'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'port'
               68  JUMP_FORWARD         94  'to 94'
             70_0  COME_FROM            56  '56'
             70_1  COME_FROM            52  '52'

 L. 513        70  LOAD_FAST                'self'
               72  LOAD_ATTR                port
               74  POP_JUMP_IF_TRUE     94  'to 94'
               76  LOAD_FAST                'port'
               78  LOAD_GLOBAL              port_by_scheme
               80  LOAD_METHOD              get
               82  LOAD_FAST                'scheme'
               84  CALL_METHOD_1         1  ''
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE    94  'to 94'

 L. 514        90  LOAD_CONST               None
               92  STORE_FAST               'port'
             94_0  COME_FROM            88  '88'
             94_1  COME_FROM            74  '74'
             94_2  COME_FROM            68  '68'

 L. 516        94  LOAD_FAST                'scheme'
               96  LOAD_FAST                'host'
               98  LOAD_FAST                'port'
              100  BUILD_TUPLE_3         3 
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                scheme
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                host
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                port
              114  BUILD_TUPLE_3         3 
              116  COMPARE_OP               ==
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 32

    def urlopen--- This code section failed: ---

 L. 627         0  LOAD_GLOBAL              parse_url
                2  LOAD_FAST                'url'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'parsed_url'

 L. 628         8  LOAD_FAST                'parsed_url'
               10  LOAD_ATTR                scheme
               12  STORE_FAST               'destination_scheme'

 L. 630        14  LOAD_FAST                'headers'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 631        22  LOAD_FAST                'self'
               24  LOAD_ATTR                headers
               26  STORE_FAST               'headers'
             28_0  COME_FROM            20  '20'

 L. 633        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'retries'
               32  LOAD_GLOBAL              Retry
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_TRUE     56  'to 56'

 L. 634        38  LOAD_GLOBAL              Retry
               40  LOAD_ATTR                from_int
               42  LOAD_FAST                'retries'
               44  LOAD_FAST                'redirect'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                retries
               50  LOAD_CONST               ('redirect', 'default')
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  STORE_FAST               'retries'
             56_0  COME_FROM            36  '36'

 L. 636        56  LOAD_FAST                'release_conn'
               58  LOAD_CONST               None
               60  <117>                 0  ''
               62  POP_JUMP_IF_FALSE    76  'to 76'

 L. 637        64  LOAD_FAST                'response_kw'
               66  LOAD_METHOD              get
               68  LOAD_STR                 'preload_content'
               70  LOAD_CONST               True
               72  CALL_METHOD_2         2  ''
               74  STORE_FAST               'release_conn'
             76_0  COME_FROM            62  '62'

 L. 640        76  LOAD_FAST                'assert_same_host'
               78  POP_JUMP_IF_FALSE   102  'to 102'
               80  LOAD_FAST                'self'
               82  LOAD_METHOD              is_same_host
               84  LOAD_FAST                'url'
               86  CALL_METHOD_1         1  ''
               88  POP_JUMP_IF_TRUE    102  'to 102'

 L. 641        90  LOAD_GLOBAL              HostChangedError
               92  LOAD_FAST                'self'
               94  LOAD_FAST                'url'
               96  LOAD_FAST                'retries'
               98  CALL_FUNCTION_3       3  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            88  '88'
            102_1  COME_FROM            78  '78'

 L. 644       102  LOAD_FAST                'url'
              104  LOAD_METHOD              startswith
              106  LOAD_STR                 '/'
              108  CALL_METHOD_1         1  ''
              110  POP_JUMP_IF_FALSE   128  'to 128'

 L. 645       112  LOAD_GLOBAL              six
              114  LOAD_METHOD              ensure_str
              116  LOAD_GLOBAL              _encode_target
              118  LOAD_FAST                'url'
              120  CALL_FUNCTION_1       1  ''
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'url'
              126  JUMP_FORWARD        140  'to 140'
            128_0  COME_FROM           110  '110'

 L. 647       128  LOAD_GLOBAL              six
              130  LOAD_METHOD              ensure_str
              132  LOAD_FAST                'parsed_url'
              134  LOAD_ATTR                url
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'url'
            140_0  COME_FROM           126  '126'

 L. 649       140  LOAD_CONST               None
              142  STORE_FAST               'conn'

 L. 660       144  LOAD_FAST                'release_conn'
              146  STORE_FAST               'release_this_conn'

 L. 662       148  LOAD_GLOBAL              connection_requires_http_tunnel

 L. 663       150  LOAD_FAST                'self'
              152  LOAD_ATTR                proxy
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                proxy_config
              158  LOAD_FAST                'destination_scheme'

 L. 662       160  CALL_FUNCTION_3       3  ''
              162  STORE_FAST               'http_tunnel_required'

 L. 669       164  LOAD_FAST                'http_tunnel_required'
              166  POP_JUMP_IF_TRUE    188  'to 188'

 L. 670       168  LOAD_FAST                'headers'
              170  LOAD_METHOD              copy
              172  CALL_METHOD_0         0  ''
              174  STORE_FAST               'headers'

 L. 671       176  LOAD_FAST                'headers'
              178  LOAD_METHOD              update
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                proxy_headers
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
            188_0  COME_FROM           166  '166'

 L. 675       188  LOAD_CONST               None
              190  STORE_FAST               'err'

 L. 679       192  LOAD_CONST               False
              194  STORE_FAST               'clean_exit'

 L. 683       196  LOAD_GLOBAL              set_file_position
              198  LOAD_FAST                'body'
              200  LOAD_FAST                'body_pos'
              202  CALL_FUNCTION_2       2  ''
              204  STORE_FAST               'body_pos'

 L. 685   206_208  SETUP_FINALLY       628  'to 628'
              210  SETUP_FINALLY       372  'to 372'

 L. 687       212  LOAD_FAST                'self'
              214  LOAD_METHOD              _get_timeout
              216  LOAD_FAST                'timeout'
              218  CALL_METHOD_1         1  ''
              220  STORE_FAST               'timeout_obj'

 L. 688       222  LOAD_FAST                'self'
              224  LOAD_ATTR                _get_conn
              226  LOAD_FAST                'pool_timeout'
              228  LOAD_CONST               ('timeout',)
              230  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              232  STORE_FAST               'conn'

 L. 690       234  LOAD_FAST                'timeout_obj'
              236  LOAD_ATTR                connect_timeout
              238  LOAD_FAST                'conn'
              240  STORE_ATTR               timeout

 L. 692       242  LOAD_FAST                'self'
              244  LOAD_ATTR                proxy
              246  LOAD_CONST               None
              248  <117>                 1  ''
          250_252  JUMP_IF_FALSE_OR_POP   266  'to 266'
              254  LOAD_GLOBAL              getattr

 L. 693       256  LOAD_FAST                'conn'
              258  LOAD_STR                 'sock'
              260  LOAD_CONST               None

 L. 692       262  CALL_FUNCTION_3       3  ''
              264  UNARY_NOT        
            266_0  COME_FROM           250  '250'
              266  STORE_FAST               'is_new_proxy_conn'

 L. 695       268  LOAD_FAST                'is_new_proxy_conn'
          270_272  POP_JUMP_IF_FALSE   290  'to 290'
              274  LOAD_FAST                'http_tunnel_required'
          276_278  POP_JUMP_IF_FALSE   290  'to 290'

 L. 696       280  LOAD_FAST                'self'
              282  LOAD_METHOD              _prepare_proxy
              284  LOAD_FAST                'conn'
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          
            290_0  COME_FROM           276  '276'
            290_1  COME_FROM           270  '270'

 L. 699       290  LOAD_FAST                'self'
              292  LOAD_ATTR                _make_request

 L. 700       294  LOAD_FAST                'conn'

 L. 701       296  LOAD_FAST                'method'

 L. 702       298  LOAD_FAST                'url'

 L. 703       300  LOAD_FAST                'timeout_obj'

 L. 704       302  LOAD_FAST                'body'

 L. 705       304  LOAD_FAST                'headers'

 L. 706       306  LOAD_FAST                'chunked'

 L. 699       308  LOAD_CONST               ('timeout', 'body', 'headers', 'chunked')
              310  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              312  STORE_FAST               'httplib_response'

 L. 713       314  LOAD_FAST                'release_conn'
          316_318  POP_JUMP_IF_TRUE    324  'to 324'
              320  LOAD_FAST                'conn'
              322  JUMP_FORWARD        326  'to 326'
            324_0  COME_FROM           316  '316'
              324  LOAD_CONST               None
            326_0  COME_FROM           322  '322'
              326  STORE_FAST               'response_conn'

 L. 716       328  LOAD_FAST                'method'
              330  LOAD_FAST                'response_kw'
              332  LOAD_STR                 'request_method'
              334  STORE_SUBSCR     

 L. 719       336  LOAD_FAST                'self'
              338  LOAD_ATTR                ResponseCls
              340  LOAD_ATTR                from_httplib

 L. 720       342  LOAD_FAST                'httplib_response'

 L. 719       344  BUILD_TUPLE_1         1 

 L. 721       346  LOAD_FAST                'self'

 L. 722       348  LOAD_FAST                'response_conn'

 L. 723       350  LOAD_FAST                'retries'

 L. 719       352  LOAD_CONST               ('pool', 'connection', 'retries')
              354  BUILD_CONST_KEY_MAP_3     3 

 L. 724       356  LOAD_FAST                'response_kw'

 L. 719       358  <164>                 1  ''
              360  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              362  STORE_FAST               'response'

 L. 728       364  LOAD_CONST               True
              366  STORE_FAST               'clean_exit'
              368  POP_BLOCK        
              370  JUMP_FORWARD        584  'to 584'
            372_0  COME_FROM_FINALLY   210  '210'

 L. 730       372  DUP_TOP          
              374  LOAD_GLOBAL              EmptyPoolError
          376_378  <121>               400  ''
              380  POP_TOP          
              382  POP_TOP          
              384  POP_TOP          

 L. 732       386  LOAD_CONST               True
              388  STORE_FAST               'clean_exit'

 L. 733       390  LOAD_CONST               False
              392  STORE_FAST               'release_this_conn'

 L. 734       394  RAISE_VARARGS_0       0  'reraise'
              396  POP_EXCEPT       
              398  JUMP_FORWARD        584  'to 584'

 L. 736       400  DUP_TOP          

 L. 737       402  LOAD_GLOBAL              TimeoutError

 L. 738       404  LOAD_GLOBAL              HTTPException

 L. 739       406  LOAD_GLOBAL              SocketError

 L. 740       408  LOAD_GLOBAL              ProtocolError

 L. 741       410  LOAD_GLOBAL              BaseSSLError

 L. 742       412  LOAD_GLOBAL              SSLError

 L. 743       414  LOAD_GLOBAL              CertificateError

 L. 736       416  BUILD_TUPLE_7         7 
          418_420  <121>               582  ''
              422  POP_TOP          
              424  STORE_FAST               'e'
              426  POP_TOP          
              428  SETUP_FINALLY       574  'to 574'

 L. 747       430  LOAD_CONST               False
              432  STORE_FAST               'clean_exit'

 L. 748       434  LOAD_GLOBAL              isinstance
              436  LOAD_FAST                'e'
              438  LOAD_GLOBAL              BaseSSLError
              440  LOAD_GLOBAL              CertificateError
              442  BUILD_TUPLE_2         2 
              444  CALL_FUNCTION_2       2  ''
          446_448  POP_JUMP_IF_FALSE   460  'to 460'

 L. 749       450  LOAD_GLOBAL              SSLError
              452  LOAD_FAST                'e'
              454  CALL_FUNCTION_1       1  ''
              456  STORE_FAST               'e'
              458  JUMP_FORWARD        522  'to 522'
            460_0  COME_FROM           446  '446'

 L. 750       460  LOAD_GLOBAL              isinstance
              462  LOAD_FAST                'e'
              464  LOAD_GLOBAL              SocketError
              466  LOAD_GLOBAL              NewConnectionError
              468  BUILD_TUPLE_2         2 
              470  CALL_FUNCTION_2       2  ''
          472_474  POP_JUMP_IF_FALSE   496  'to 496'
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                proxy
          480_482  POP_JUMP_IF_FALSE   496  'to 496'

 L. 751       484  LOAD_GLOBAL              ProxyError
              486  LOAD_STR                 'Cannot connect to proxy.'
              488  LOAD_FAST                'e'
              490  CALL_FUNCTION_2       2  ''
              492  STORE_FAST               'e'
              494  JUMP_FORWARD        522  'to 522'
            496_0  COME_FROM           480  '480'
            496_1  COME_FROM           472  '472'

 L. 752       496  LOAD_GLOBAL              isinstance
              498  LOAD_FAST                'e'
              500  LOAD_GLOBAL              SocketError
              502  LOAD_GLOBAL              HTTPException
              504  BUILD_TUPLE_2         2 
              506  CALL_FUNCTION_2       2  ''
          508_510  POP_JUMP_IF_FALSE   522  'to 522'

 L. 753       512  LOAD_GLOBAL              ProtocolError
              514  LOAD_STR                 'Connection aborted.'
              516  LOAD_FAST                'e'
              518  CALL_FUNCTION_2       2  ''
              520  STORE_FAST               'e'
            522_0  COME_FROM           508  '508'
            522_1  COME_FROM           494  '494'
            522_2  COME_FROM           458  '458'

 L. 755       522  LOAD_FAST                'retries'
              524  LOAD_ATTR                increment

 L. 756       526  LOAD_FAST                'method'
              528  LOAD_FAST                'url'
              530  LOAD_FAST                'e'
              532  LOAD_FAST                'self'
              534  LOAD_GLOBAL              sys
              536  LOAD_METHOD              exc_info
              538  CALL_METHOD_0         0  ''
              540  LOAD_CONST               2
              542  BINARY_SUBSCR    

 L. 755       544  LOAD_CONST               ('error', '_pool', '_stacktrace')
              546  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              548  STORE_FAST               'retries'

 L. 758       550  LOAD_FAST                'retries'
              552  LOAD_METHOD              sleep
              554  CALL_METHOD_0         0  ''
              556  POP_TOP          

 L. 761       558  LOAD_FAST                'e'
              560  STORE_FAST               'err'
              562  POP_BLOCK        
              564  POP_EXCEPT       
              566  LOAD_CONST               None
              568  STORE_FAST               'e'
              570  DELETE_FAST              'e'
              572  JUMP_FORWARD        584  'to 584'
            574_0  COME_FROM_FINALLY   428  '428'
              574  LOAD_CONST               None
              576  STORE_FAST               'e'
              578  DELETE_FAST              'e'
              580  <48>             
              582  <48>             
            584_0  COME_FROM           572  '572'
            584_1  COME_FROM           398  '398'
            584_2  COME_FROM           370  '370'
              584  POP_BLOCK        

 L. 764       586  LOAD_FAST                'clean_exit'
          588_590  POP_JUMP_IF_TRUE    610  'to 610'

 L. 769       592  LOAD_FAST                'conn'
          594_596  JUMP_IF_FALSE_OR_POP   604  'to 604'
              598  LOAD_FAST                'conn'
              600  LOAD_METHOD              close
              602  CALL_METHOD_0         0  ''
            604_0  COME_FROM           594  '594'
              604  STORE_FAST               'conn'

 L. 770       606  LOAD_CONST               True
              608  STORE_FAST               'release_this_conn'
            610_0  COME_FROM           588  '588'

 L. 772       610  LOAD_FAST                'release_this_conn'
          612_614  POP_JUMP_IF_FALSE   670  'to 670'

 L. 776       616  LOAD_FAST                'self'
              618  LOAD_METHOD              _put_conn
              620  LOAD_FAST                'conn'
              622  CALL_METHOD_1         1  ''
              624  POP_TOP          
              626  JUMP_FORWARD        670  'to 670'
            628_0  COME_FROM_FINALLY   206  '206'

 L. 764       628  LOAD_FAST                'clean_exit'
          630_632  POP_JUMP_IF_TRUE    652  'to 652'

 L. 769       634  LOAD_FAST                'conn'
          636_638  JUMP_IF_FALSE_OR_POP   646  'to 646'
              640  LOAD_FAST                'conn'
              642  LOAD_METHOD              close
              644  CALL_METHOD_0         0  ''
            646_0  COME_FROM           636  '636'
              646  STORE_FAST               'conn'

 L. 770       648  LOAD_CONST               True
              650  STORE_FAST               'release_this_conn'
            652_0  COME_FROM           630  '630'

 L. 772       652  LOAD_FAST                'release_this_conn'
          654_656  POP_JUMP_IF_FALSE   668  'to 668'

 L. 776       658  LOAD_FAST                'self'
              660  LOAD_METHOD              _put_conn
              662  LOAD_FAST                'conn'
              664  CALL_METHOD_1         1  ''
              666  POP_TOP          
            668_0  COME_FROM           654  '654'
              668  <48>             
            670_0  COME_FROM           626  '626'
            670_1  COME_FROM           612  '612'

 L. 778       670  LOAD_FAST                'conn'
          672_674  POP_JUMP_IF_TRUE    734  'to 734'

 L. 780       676  LOAD_GLOBAL              log
              678  LOAD_METHOD              warning

 L. 781       680  LOAD_STR                 "Retrying (%r) after connection broken by '%r': %s"
              682  LOAD_FAST                'retries'
              684  LOAD_FAST                'err'
              686  LOAD_FAST                'url'

 L. 780       688  CALL_METHOD_4         4  ''
              690  POP_TOP          

 L. 783       692  LOAD_FAST                'self'
              694  LOAD_ATTR                urlopen

 L. 784       696  LOAD_FAST                'method'

 L. 785       698  LOAD_FAST                'url'

 L. 786       700  LOAD_FAST                'body'

 L. 787       702  LOAD_FAST                'headers'

 L. 788       704  LOAD_FAST                'retries'

 L. 789       706  LOAD_FAST                'redirect'

 L. 790       708  LOAD_FAST                'assert_same_host'

 L. 783       710  BUILD_TUPLE_7         7 

 L. 791       712  LOAD_FAST                'timeout'

 L. 792       714  LOAD_FAST                'pool_timeout'

 L. 793       716  LOAD_FAST                'release_conn'

 L. 794       718  LOAD_FAST                'chunked'

 L. 795       720  LOAD_FAST                'body_pos'

 L. 783       722  LOAD_CONST               ('timeout', 'pool_timeout', 'release_conn', 'chunked', 'body_pos')
              724  BUILD_CONST_KEY_MAP_5     5 

 L. 796       726  LOAD_FAST                'response_kw'

 L. 783       728  <164>                 1  ''
              730  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              732  RETURN_VALUE     
            734_0  COME_FROM           672  '672'

 L. 800       734  LOAD_FAST                'redirect'
          736_738  JUMP_IF_FALSE_OR_POP   746  'to 746'
              740  LOAD_FAST                'response'
              742  LOAD_METHOD              get_redirect_location
              744  CALL_METHOD_0         0  ''
            746_0  COME_FROM           736  '736'
              746  STORE_FAST               'redirect_location'

 L. 801       748  LOAD_FAST                'redirect_location'
          750_752  POP_JUMP_IF_FALSE   910  'to 910'

 L. 802       754  LOAD_FAST                'response'
              756  LOAD_ATTR                status
              758  LOAD_CONST               303
              760  COMPARE_OP               ==
          762_764  POP_JUMP_IF_FALSE   770  'to 770'

 L. 803       766  LOAD_STR                 'GET'
              768  STORE_FAST               'method'
            770_0  COME_FROM           762  '762'

 L. 805       770  SETUP_FINALLY       794  'to 794'

 L. 806       772  LOAD_FAST                'retries'
              774  LOAD_ATTR                increment
              776  LOAD_FAST                'method'
              778  LOAD_FAST                'url'
              780  LOAD_FAST                'response'
              782  LOAD_FAST                'self'
              784  LOAD_CONST               ('response', '_pool')
              786  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              788  STORE_FAST               'retries'
              790  POP_BLOCK        
              792  JUMP_FORWARD        836  'to 836'
            794_0  COME_FROM_FINALLY   770  '770'

 L. 807       794  DUP_TOP          
              796  LOAD_GLOBAL              MaxRetryError
          798_800  <121>               834  ''
              802  POP_TOP          
              804  POP_TOP          
              806  POP_TOP          

 L. 808       808  LOAD_FAST                'retries'
              810  LOAD_ATTR                raise_on_redirect
          812_814  POP_JUMP_IF_FALSE   826  'to 826'

 L. 809       816  LOAD_FAST                'response'
              818  LOAD_METHOD              drain_conn
              820  CALL_METHOD_0         0  ''
              822  POP_TOP          

 L. 810       824  RAISE_VARARGS_0       0  'reraise'
            826_0  COME_FROM           812  '812'

 L. 811       826  LOAD_FAST                'response'
              828  ROT_FOUR         
              830  POP_EXCEPT       
              832  RETURN_VALUE     
              834  <48>             
            836_0  COME_FROM           792  '792'

 L. 813       836  LOAD_FAST                'response'
              838  LOAD_METHOD              drain_conn
              840  CALL_METHOD_0         0  ''
              842  POP_TOP          

 L. 814       844  LOAD_FAST                'retries'
              846  LOAD_METHOD              sleep_for_retry
              848  LOAD_FAST                'response'
              850  CALL_METHOD_1         1  ''
              852  POP_TOP          

 L. 815       854  LOAD_GLOBAL              log
              856  LOAD_METHOD              debug
              858  LOAD_STR                 'Redirecting %s -> %s'
              860  LOAD_FAST                'url'
              862  LOAD_FAST                'redirect_location'
              864  CALL_METHOD_3         3  ''
              866  POP_TOP          

 L. 816       868  LOAD_FAST                'self'
              870  LOAD_ATTR                urlopen

 L. 817       872  LOAD_FAST                'method'

 L. 818       874  LOAD_FAST                'redirect_location'

 L. 819       876  LOAD_FAST                'body'

 L. 820       878  LOAD_FAST                'headers'

 L. 816       880  BUILD_TUPLE_4         4 

 L. 821       882  LOAD_FAST                'retries'

 L. 822       884  LOAD_FAST                'redirect'

 L. 823       886  LOAD_FAST                'assert_same_host'

 L. 824       888  LOAD_FAST                'timeout'

 L. 825       890  LOAD_FAST                'pool_timeout'

 L. 826       892  LOAD_FAST                'release_conn'

 L. 827       894  LOAD_FAST                'chunked'

 L. 828       896  LOAD_FAST                'body_pos'

 L. 816       898  LOAD_CONST               ('retries', 'redirect', 'assert_same_host', 'timeout', 'pool_timeout', 'release_conn', 'chunked', 'body_pos')
              900  BUILD_CONST_KEY_MAP_8     8 

 L. 829       902  LOAD_FAST                'response_kw'

 L. 816       904  <164>                 1  ''
              906  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              908  RETURN_VALUE     
            910_0  COME_FROM           750  '750'

 L. 833       910  LOAD_GLOBAL              bool
              912  LOAD_FAST                'response'
              914  LOAD_METHOD              getheader
              916  LOAD_STR                 'Retry-After'
              918  CALL_METHOD_1         1  ''
              920  CALL_FUNCTION_1       1  ''
              922  STORE_FAST               'has_retry_after'

 L. 834       924  LOAD_FAST                'retries'
              926  LOAD_METHOD              is_retry
              928  LOAD_FAST                'method'
              930  LOAD_FAST                'response'
              932  LOAD_ATTR                status
              934  LOAD_FAST                'has_retry_after'
              936  CALL_METHOD_3         3  ''
          938_940  POP_JUMP_IF_FALSE  1080  'to 1080'

 L. 835       942  SETUP_FINALLY       966  'to 966'

 L. 836       944  LOAD_FAST                'retries'
              946  LOAD_ATTR                increment
              948  LOAD_FAST                'method'
              950  LOAD_FAST                'url'
              952  LOAD_FAST                'response'
              954  LOAD_FAST                'self'
              956  LOAD_CONST               ('response', '_pool')
              958  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              960  STORE_FAST               'retries'
              962  POP_BLOCK        
              964  JUMP_FORWARD       1008  'to 1008'
            966_0  COME_FROM_FINALLY   942  '942'

 L. 837       966  DUP_TOP          
              968  LOAD_GLOBAL              MaxRetryError
          970_972  <121>              1006  ''
              974  POP_TOP          
              976  POP_TOP          
              978  POP_TOP          

 L. 838       980  LOAD_FAST                'retries'
              982  LOAD_ATTR                raise_on_status
          984_986  POP_JUMP_IF_FALSE   998  'to 998'

 L. 839       988  LOAD_FAST                'response'
              990  LOAD_METHOD              drain_conn
              992  CALL_METHOD_0         0  ''
              994  POP_TOP          

 L. 840       996  RAISE_VARARGS_0       0  'reraise'
            998_0  COME_FROM           984  '984'

 L. 841       998  LOAD_FAST                'response'
             1000  ROT_FOUR         
             1002  POP_EXCEPT       
             1004  RETURN_VALUE     
             1006  <48>             
           1008_0  COME_FROM           964  '964'

 L. 843      1008  LOAD_FAST                'response'
             1010  LOAD_METHOD              drain_conn
             1012  CALL_METHOD_0         0  ''
             1014  POP_TOP          

 L. 844      1016  LOAD_FAST                'retries'
             1018  LOAD_METHOD              sleep
             1020  LOAD_FAST                'response'
             1022  CALL_METHOD_1         1  ''
             1024  POP_TOP          

 L. 845      1026  LOAD_GLOBAL              log
             1028  LOAD_METHOD              debug
             1030  LOAD_STR                 'Retry: %s'
             1032  LOAD_FAST                'url'
             1034  CALL_METHOD_2         2  ''
             1036  POP_TOP          

 L. 846      1038  LOAD_FAST                'self'
             1040  LOAD_ATTR                urlopen

 L. 847      1042  LOAD_FAST                'method'

 L. 848      1044  LOAD_FAST                'url'

 L. 849      1046  LOAD_FAST                'body'

 L. 850      1048  LOAD_FAST                'headers'

 L. 846      1050  BUILD_TUPLE_4         4 

 L. 851      1052  LOAD_FAST                'retries'

 L. 852      1054  LOAD_FAST                'redirect'

 L. 853      1056  LOAD_FAST                'assert_same_host'

 L. 854      1058  LOAD_FAST                'timeout'

 L. 855      1060  LOAD_FAST                'pool_timeout'

 L. 856      1062  LOAD_FAST                'release_conn'

 L. 857      1064  LOAD_FAST                'chunked'

 L. 858      1066  LOAD_FAST                'body_pos'

 L. 846      1068  LOAD_CONST               ('retries', 'redirect', 'assert_same_host', 'timeout', 'pool_timeout', 'release_conn', 'chunked', 'body_pos')
             1070  BUILD_CONST_KEY_MAP_8     8 

 L. 859      1072  LOAD_FAST                'response_kw'

 L. 846      1074  <164>                 1  ''
             1076  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1078  RETURN_VALUE     
           1080_0  COME_FROM           938  '938'

 L. 862      1080  LOAD_FAST                'response'
             1082  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18


class HTTPSConnectionPool(HTTPConnectionPool):
    __doc__ = '\n    Same as :class:`.HTTPConnectionPool`, but HTTPS.\n\n    :class:`.HTTPSConnection` uses one of ``assert_fingerprint``,\n    ``assert_hostname`` and ``host`` in this order to verify connections.\n    If ``assert_hostname`` is False, no verification is done.\n\n    The ``key_file``, ``cert_file``, ``cert_reqs``, ``ca_certs``,\n    ``ca_cert_dir``, ``ssl_version``, ``key_password`` are only used if :mod:`ssl`\n    is available and are fed into :meth:`urllib3.util.ssl_wrap_socket` to upgrade\n    the connection socket into an SSL socket.\n    '
    scheme = 'https'
    ConnectionCls = HTTPSConnection

    def __init__--- This code section failed: ---

 L. 906         0  LOAD_GLOBAL              HTTPConnectionPool
                2  LOAD_ATTR                __init__

 L. 907         4  LOAD_FAST                'self'

 L. 908         6  LOAD_FAST                'host'

 L. 909         8  LOAD_FAST                'port'

 L. 910        10  LOAD_FAST                'strict'

 L. 911        12  LOAD_FAST                'timeout'

 L. 912        14  LOAD_FAST                'maxsize'

 L. 913        16  LOAD_FAST                'block'

 L. 914        18  LOAD_FAST                'headers'

 L. 915        20  LOAD_FAST                'retries'

 L. 916        22  LOAD_FAST                '_proxy'

 L. 917        24  LOAD_FAST                '_proxy_headers'

 L. 906        26  BUILD_TUPLE_11       11 
               28  BUILD_MAP_0           0 

 L. 918        30  LOAD_FAST                'conn_kw'

 L. 906        32  <164>                 1  ''
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  POP_TOP          

 L. 921        38  LOAD_FAST                'key_file'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               key_file

 L. 922        44  LOAD_FAST                'cert_file'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               cert_file

 L. 923        50  LOAD_FAST                'cert_reqs'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               cert_reqs

 L. 924        56  LOAD_FAST                'key_password'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               key_password

 L. 925        62  LOAD_FAST                'ca_certs'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               ca_certs

 L. 926        68  LOAD_FAST                'ca_cert_dir'
               70  LOAD_FAST                'self'
               72  STORE_ATTR               ca_cert_dir

 L. 927        74  LOAD_FAST                'ssl_version'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               ssl_version

 L. 928        80  LOAD_FAST                'assert_hostname'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               assert_hostname

 L. 929        86  LOAD_FAST                'assert_fingerprint'
               88  LOAD_FAST                'self'
               90  STORE_ATTR               assert_fingerprint

Parse error at or near `<164>' instruction at offset 32

    def _prepare_conn(self, conn):
        """
        Prepare the ``connection`` for :meth:`urllib3.util.ssl_wrap_socket`
        and establish the tunnel if proxy is used.
        """
        if isinstanceconnVerifiedHTTPSConnection:
            conn.set_cert(key_file=(self.key_file),
              key_password=(self.key_password),
              cert_file=(self.cert_file),
              cert_reqs=(self.cert_reqs),
              ca_certs=(self.ca_certs),
              ca_cert_dir=(self.ca_cert_dir),
              assert_hostname=(self.assert_hostname),
              assert_fingerprint=(self.assert_fingerprint))
            conn.ssl_version = self.ssl_version
        return conn

    def _prepare_proxy(self, conn):
        """
        Establishes a tunnel connection through HTTP CONNECT.

        Tunnel connection is established early because otherwise httplib would
        improperly set Host: header to proxy's IP:port.
        """
        conn.set_tunnelself._proxy_hostself.portself.proxy_headers
        if self.proxy.scheme == 'https':
            conn.tls_in_tls_required = True
        conn.connect()

    def _new_conn--- This code section failed: ---

 L. 970         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                num_connections
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               num_connections

 L. 971        14  LOAD_GLOBAL              log
               16  LOAD_METHOD              debug

 L. 972        18  LOAD_STR                 'Starting new HTTPS connection (%d): %s:%s'

 L. 973        20  LOAD_FAST                'self'
               22  LOAD_ATTR                num_connections

 L. 974        24  LOAD_FAST                'self'
               26  LOAD_ATTR                host

 L. 975        28  LOAD_FAST                'self'
               30  LOAD_ATTR                port
               32  JUMP_IF_TRUE_OR_POP    36  'to 36'
               34  LOAD_STR                 '443'
             36_0  COME_FROM            32  '32'

 L. 971        36  CALL_METHOD_4         4  ''
               38  POP_TOP          

 L. 978        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ConnectionCls
               44  POP_JUMP_IF_FALSE    56  'to 56'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                ConnectionCls
               50  LOAD_GLOBAL              DummyConnection
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    64  'to 64'
             56_0  COME_FROM            44  '44'

 L. 979        56  LOAD_GLOBAL              SSLError

 L. 980        58  LOAD_STR                 "Can't connect to HTTPS URL because the SSL module is not available."

 L. 979        60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'

 L. 983        64  LOAD_FAST                'self'
               66  LOAD_ATTR                host
               68  STORE_FAST               'actual_host'

 L. 984        70  LOAD_FAST                'self'
               72  LOAD_ATTR                port
               74  STORE_FAST               'actual_port'

 L. 985        76  LOAD_FAST                'self'
               78  LOAD_ATTR                proxy
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   102  'to 102'

 L. 986        86  LOAD_FAST                'self'
               88  LOAD_ATTR                proxy
               90  LOAD_ATTR                host
               92  STORE_FAST               'actual_host'

 L. 987        94  LOAD_FAST                'self'
               96  LOAD_ATTR                proxy
               98  LOAD_ATTR                port
              100  STORE_FAST               'actual_port'
            102_0  COME_FROM            84  '84'

 L. 989       102  LOAD_FAST                'self'
              104  LOAD_ATTR                ConnectionCls
              106  BUILD_TUPLE_0         0 

 L. 990       108  LOAD_FAST                'actual_host'

 L. 991       110  LOAD_FAST                'actual_port'

 L. 992       112  LOAD_FAST                'self'
              114  LOAD_ATTR                timeout
              116  LOAD_ATTR                connect_timeout

 L. 993       118  LOAD_FAST                'self'
              120  LOAD_ATTR                strict

 L. 994       122  LOAD_FAST                'self'
              124  LOAD_ATTR                cert_file

 L. 995       126  LOAD_FAST                'self'
              128  LOAD_ATTR                key_file

 L. 996       130  LOAD_FAST                'self'
              132  LOAD_ATTR                key_password

 L. 989       134  LOAD_CONST               ('host', 'port', 'timeout', 'strict', 'cert_file', 'key_file', 'key_password')
              136  BUILD_CONST_KEY_MAP_7     7 

 L. 997       138  LOAD_FAST                'self'
              140  LOAD_ATTR                conn_kw

 L. 989       142  <164>                 1  ''
              144  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              146  STORE_FAST               'conn'

 L.1000       148  LOAD_FAST                'self'
              150  LOAD_METHOD              _prepare_conn
              152  LOAD_FAST                'conn'
              154  CALL_METHOD_1         1  ''
              156  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 52

    def _validate_conn(self, conn):
        superHTTPSConnectionPoolself._validate_conn(conn)
        if not getattr(conn, 'sock', None):
            conn.connect()
        if not conn.is_verified:
            warnings.warn("Unverified HTTPS request is being made to host '%s'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings" % conn.host)InsecureRequestWarning


def connection_from_url--- This code section failed: ---

 L.1044         0  LOAD_GLOBAL              get_host
                2  LOAD_FAST                'url'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_3     3 
                8  STORE_FAST               'scheme'
               10  STORE_FAST               'host'
               12  STORE_FAST               'port'

 L.1045        14  LOAD_FAST                'port'
               16  JUMP_IF_TRUE_OR_POP    28  'to 28'
               18  LOAD_GLOBAL              port_by_scheme
               20  LOAD_METHOD              get
               22  LOAD_FAST                'scheme'
               24  LOAD_CONST               80
               26  CALL_METHOD_2         2  ''
             28_0  COME_FROM            16  '16'
               28  STORE_FAST               'port'

 L.1046        30  LOAD_FAST                'scheme'
               32  LOAD_STR                 'https'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    58  'to 58'

 L.1047        38  LOAD_GLOBAL              HTTPSConnectionPool
               40  LOAD_FAST                'host'
               42  BUILD_TUPLE_1         1 
               44  LOAD_STR                 'port'
               46  LOAD_FAST                'port'
               48  BUILD_MAP_1           1 
               50  LOAD_FAST                'kw'
               52  <164>                 1  ''
               54  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               56  RETURN_VALUE     
             58_0  COME_FROM            36  '36'

 L.1049        58  LOAD_GLOBAL              HTTPConnectionPool
               60  LOAD_FAST                'host'
               62  BUILD_TUPLE_1         1 
               64  LOAD_STR                 'port'
               66  LOAD_FAST                'port'
               68  BUILD_MAP_1           1 
               70  LOAD_FAST                'kw'
               72  <164>                 1  ''
               74  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               76  RETURN_VALUE     

Parse error at or near `<164>' instruction at offset 52


def _normalize_host(host, scheme):
    """
    Normalize hosts for comparisons and use with sockets.
    """
    host = normalize_hosthostscheme
    if host.startswith('['):
        if host.endswith(']'):
            host = host[1:-1]
    return host