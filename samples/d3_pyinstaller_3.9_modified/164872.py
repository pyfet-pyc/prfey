# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\connectionpool.py
from __future__ import absolute_import
import errno, logging, sys, warnings
from socket import error as SocketError, timeout as SocketTimeout
import socket
from .exceptions import ClosedPoolError, ProtocolError, EmptyPoolError, HeaderParsingError, HostChangedError, LocationValueError, MaxRetryError, ProxyError, ReadTimeoutError, SSLError, TimeoutError, InsecureRequestWarning, NewConnectionError
from packages.ssl_match_hostname import CertificateError
from .packages import six
from packages.six.moves import queue
from .connection import port_by_scheme, DummyConnection, HTTPConnection, HTTPSConnection, VerifiedHTTPSConnection, HTTPException, BaseSSLError
from .request import RequestMethods
from .response import HTTPResponse
from util.connection import is_connection_dropped
from util.request import set_file_position
from util.response import assert_header_parsing
from util.retry import Retry
from util.timeout import Timeout
from util.url import get_host, parse_url, Url, _normalize_host as normalize_host, _encode_target
from util.queue import LifoQueue
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
    __doc__ = '\n    Thread-safe connection pool for one host.\n\n    :param host:\n        Host used for this HTTP Connection (e.g. "localhost"), passed into\n        :class:`httplib.HTTPConnection`.\n\n    :param port:\n        Port used for this HTTP Connection (None is equivalent to 80), passed\n        into :class:`httplib.HTTPConnection`.\n\n    :param strict:\n        Causes BadStatusLine to be raised if the status line can\'t be parsed\n        as a valid HTTP/1.0 or 1.1 status line, passed into\n        :class:`httplib.HTTPConnection`.\n\n        .. note::\n           Only works in Python 2. This parameter is ignored in Python 3.\n\n    :param timeout:\n        Socket timeout in seconds for each individual connection. This can\n        be a float or integer, which sets the timeout for the HTTP request,\n        or an instance of :class:`urllib3.util.Timeout` which gives you more\n        fine-grained control over request timeouts. After the constructor has\n        been parsed, this is always a `urllib3.util.Timeout` object.\n\n    :param maxsize:\n        Number of connections to save that can be reused. More than 1 is useful\n        in multithreaded situations. If ``block`` is set to False, more\n        connections will be created but they will not be saved once they\'ve\n        been used.\n\n    :param block:\n        If set to True, no more than ``maxsize`` connections will be used at\n        a time. When no free connections are available, the call will block\n        until a connection has been released. This is a useful side effect for\n        particular multithreaded situations where one does not want to use more\n        than maxsize connections per host to prevent flooding.\n\n    :param headers:\n        Headers to include with all requests, unless other headers are given\n        explicitly.\n\n    :param retries:\n        Retry configuration to use by default with requests in this pool.\n\n    :param _proxy:\n        Parsed proxy URL, should not be used directly, instead, see\n        :class:`urllib3.connectionpool.ProxyManager`"\n\n    :param _proxy_headers:\n        A dictionary with proxy headers, should not be used directly,\n        instead, see :class:`urllib3.connectionpool.ProxyManager`"\n\n    :param \\**conn_kw:\n        Additional parameters are used to create fresh :class:`urllib3.connection.HTTPConnection`,\n        :class:`urllib3.connection.HTTPSConnection` instances.\n    '
    scheme = 'http'
    ConnectionCls = HTTPConnection
    ResponseCls = HTTPResponse

    def __init__--- This code section failed: ---

 L. 186         0  LOAD_GLOBAL              ConnectionPool
                2  LOAD_METHOD              __init__
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'host'
                8  LOAD_FAST                'port'
               10  CALL_METHOD_3         3  ''
               12  POP_TOP          

 L. 187        14  LOAD_GLOBAL              RequestMethods
               16  LOAD_METHOD              __init__
               18  LOAD_FAST                'self'
               20  LOAD_FAST                'headers'
               22  CALL_METHOD_2         2  ''
               24  POP_TOP          

 L. 189        26  LOAD_FAST                'strict'
               28  LOAD_FAST                'self'
               30  STORE_ATTR               strict

 L. 191        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'timeout'
               36  LOAD_GLOBAL              Timeout
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_TRUE     52  'to 52'

 L. 192        42  LOAD_GLOBAL              Timeout
               44  LOAD_METHOD              from_float
               46  LOAD_FAST                'timeout'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'timeout'
             52_0  COME_FROM            40  '40'

 L. 194        52  LOAD_FAST                'retries'
               54  LOAD_CONST               None
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 195        60  LOAD_GLOBAL              Retry
               62  LOAD_ATTR                DEFAULT
               64  STORE_FAST               'retries'
             66_0  COME_FROM            58  '58'

 L. 197        66  LOAD_FAST                'timeout'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               timeout

 L. 198        72  LOAD_FAST                'retries'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               retries

 L. 200        78  LOAD_FAST                'self'
               80  LOAD_METHOD              QueueCls
               82  LOAD_FAST                'maxsize'
               84  CALL_METHOD_1         1  ''
               86  LOAD_FAST                'self'
               88  STORE_ATTR               pool

 L. 201        90  LOAD_FAST                'block'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               block

 L. 203        96  LOAD_FAST                '_proxy'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               proxy

 L. 204       102  LOAD_FAST                '_proxy_headers'
              104  JUMP_IF_TRUE_OR_POP   108  'to 108'
              106  BUILD_MAP_0           0 
            108_0  COME_FROM           104  '104'
              108  LOAD_FAST                'self'
              110  STORE_ATTR               proxy_headers

 L. 207       112  LOAD_GLOBAL              xrange
              114  LOAD_FAST                'maxsize'
              116  CALL_FUNCTION_1       1  ''
              118  GET_ITER         
            120_0  COME_FROM           136  '136'
              120  FOR_ITER            138  'to 138'
              122  STORE_FAST               '_'

 L. 208       124  LOAD_FAST                'self'
              126  LOAD_ATTR                pool
              128  LOAD_METHOD              put
              130  LOAD_CONST               None
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
              136  JUMP_BACK           120  'to 120'
            138_0  COME_FROM           120  '120'

 L. 211       138  LOAD_CONST               0
              140  LOAD_FAST                'self'
              142  STORE_ATTR               num_connections

 L. 212       144  LOAD_CONST               0
              146  LOAD_FAST                'self'
              148  STORE_ATTR               num_requests

 L. 213       150  LOAD_FAST                'conn_kw'
              152  LOAD_FAST                'self'
              154  STORE_ATTR               conn_kw

 L. 215       156  LOAD_FAST                'self'
              158  LOAD_ATTR                proxy
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L. 219       162  LOAD_FAST                'self'
              164  LOAD_ATTR                conn_kw
              166  LOAD_METHOD              setdefault
              168  LOAD_STR                 'socket_options'
              170  BUILD_LIST_0          0 
              172  CALL_METHOD_2         2  ''
              174  POP_TOP          
            176_0  COME_FROM           160  '160'

Parse error at or near `<117>' instruction at offset 56

    def _new_conn--- This code section failed: ---

 L. 225         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                num_connections
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               num_connections

 L. 226        14  LOAD_GLOBAL              log
               16  LOAD_METHOD              debug

 L. 227        18  LOAD_STR                 'Starting new HTTP connection (%d): %s:%s'

 L. 228        20  LOAD_FAST                'self'
               22  LOAD_ATTR                num_connections

 L. 229        24  LOAD_FAST                'self'
               26  LOAD_ATTR                host

 L. 230        28  LOAD_FAST                'self'
               30  LOAD_ATTR                port
               32  JUMP_IF_TRUE_OR_POP    36  'to 36'
               34  LOAD_STR                 '80'
             36_0  COME_FROM            32  '32'

 L. 226        36  CALL_METHOD_4         4  ''
               38  POP_TOP          

 L. 233        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ConnectionCls
               44  BUILD_TUPLE_0         0 

 L. 234        46  LOAD_FAST                'self'
               48  LOAD_ATTR                host

 L. 235        50  LOAD_FAST                'self'
               52  LOAD_ATTR                port

 L. 236        54  LOAD_FAST                'self'
               56  LOAD_ATTR                timeout
               58  LOAD_ATTR                connect_timeout

 L. 237        60  LOAD_FAST                'self'
               62  LOAD_ATTR                strict

 L. 233        64  LOAD_CONST               ('host', 'port', 'timeout', 'strict')
               66  BUILD_CONST_KEY_MAP_4     4 

 L. 238        68  LOAD_FAST                'self'
               70  LOAD_ATTR                conn_kw

 L. 233        72  <164>                 1  ''
               74  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               76  STORE_FAST               'conn'

 L. 240        78  LOAD_FAST                'conn'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 72

    def _get_conn--- This code section failed: ---

 L. 254         0  LOAD_CONST               None
                2  STORE_FAST               'conn'

 L. 255         4  SETUP_FINALLY        28  'to 28'

 L. 256         6  LOAD_FAST                'self'
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

 L. 258        28  DUP_TOP          
               30  LOAD_GLOBAL              AttributeError
               32  <121>                54  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 259        40  LOAD_GLOBAL              ClosedPoolError
               42  LOAD_FAST                'self'
               44  LOAD_STR                 'Pool is closed.'
               46  CALL_FUNCTION_2       2  ''
               48  RAISE_VARARGS_1       1  'exception instance'
               50  POP_EXCEPT       
               52  JUMP_FORWARD         90  'to 90'

 L. 261        54  DUP_TOP          
               56  LOAD_GLOBAL              queue
               58  LOAD_ATTR                Empty
               60  <121>                88  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 262        68  LOAD_FAST                'self'
               70  LOAD_ATTR                block
               72  POP_JUMP_IF_FALSE    84  'to 84'

 L. 263        74  LOAD_GLOBAL              EmptyPoolError

 L. 264        76  LOAD_FAST                'self'

 L. 265        78  LOAD_STR                 'Pool reached maximum size and no more connections are allowed.'

 L. 263        80  CALL_FUNCTION_2       2  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            72  '72'

 L. 267        84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
               88  <48>             
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            52  '52'
             90_2  COME_FROM            26  '26'

 L. 270        90  LOAD_FAST                'conn'
               92  POP_JUMP_IF_FALSE   144  'to 144'
               94  LOAD_GLOBAL              is_connection_dropped
               96  LOAD_FAST                'conn'
               98  CALL_FUNCTION_1       1  ''
              100  POP_JUMP_IF_FALSE   144  'to 144'

 L. 271       102  LOAD_GLOBAL              log
              104  LOAD_METHOD              debug
              106  LOAD_STR                 'Resetting dropped connection: %s'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                host
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          

 L. 272       116  LOAD_FAST                'conn'
              118  LOAD_METHOD              close
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          

 L. 273       124  LOAD_GLOBAL              getattr
              126  LOAD_FAST                'conn'
              128  LOAD_STR                 'auto_open'
              130  LOAD_CONST               1
              132  CALL_FUNCTION_3       3  ''
              134  LOAD_CONST               0
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   144  'to 144'

 L. 277       140  LOAD_CONST               None
              142  STORE_FAST               'conn'
            144_0  COME_FROM           138  '138'
            144_1  COME_FROM           100  '100'
            144_2  COME_FROM            92  '92'

 L. 279       144  LOAD_FAST                'conn'
              146  JUMP_IF_TRUE_OR_POP   154  'to 154'
              148  LOAD_FAST                'self'
              150  LOAD_METHOD              _new_conn
              152  CALL_METHOD_0         0  ''
            154_0  COME_FROM           146  '146'
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 32

    def _put_conn--- This code section failed: ---

 L. 295         0  SETUP_FINALLY        24  'to 24'

 L. 296         2  LOAD_FAST                'self'
                4  LOAD_ATTR                pool
                6  LOAD_ATTR                put
                8  LOAD_FAST                'conn'
               10  LOAD_CONST               False
               12  LOAD_CONST               ('block',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  POP_TOP          

 L. 297        18  POP_BLOCK        
               20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L. 298        24  DUP_TOP          
               26  LOAD_GLOBAL              AttributeError
               28  <121>                40  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 300        36  POP_EXCEPT       
               38  JUMP_FORWARD         74  'to 74'

 L. 301        40  DUP_TOP          
               42  LOAD_GLOBAL              queue
               44  LOAD_ATTR                Full
               46  <121>                72  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 303        54  LOAD_GLOBAL              log
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

 L. 306        74  LOAD_FAST                'conn'
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 307        78  LOAD_FAST                'conn'
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

 L. 321         0  LOAD_FAST                'timeout'
                2  LOAD_GLOBAL              _Default
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 322         8  LOAD_FAST                'self'
               10  LOAD_ATTR                timeout
               12  LOAD_METHOD              clone
               14  CALL_METHOD_0         0  ''
               16  RETURN_VALUE     
             18_0  COME_FROM             6  '6'

 L. 324        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'timeout'
               22  LOAD_GLOBAL              Timeout
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 325        28  LOAD_FAST                'timeout'
               30  LOAD_METHOD              clone
               32  CALL_METHOD_0         0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM            26  '26'

 L. 329        36  LOAD_GLOBAL              Timeout
               38  LOAD_METHOD              from_float
               40  LOAD_FAST                'timeout'
               42  CALL_METHOD_1         1  ''
               44  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def _raise_timeout--- This code section failed: ---

 L. 334         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'err'
                4  LOAD_GLOBAL              SocketTimeout
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 335        10  LOAD_GLOBAL              ReadTimeoutError

 L. 336        12  LOAD_FAST                'self'
               14  LOAD_FAST                'url'
               16  LOAD_STR                 'Read timed out. (read timeout=%s)'
               18  LOAD_FAST                'timeout_value'
               20  BINARY_MODULO    

 L. 335        22  CALL_FUNCTION_3       3  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 341        26  LOAD_GLOBAL              hasattr
               28  LOAD_FAST                'err'
               30  LOAD_STR                 'errno'
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE    62  'to 62'
               36  LOAD_FAST                'err'
               38  LOAD_ATTR                errno
               40  LOAD_GLOBAL              _blocking_errnos
               42  <118>                 0  ''
               44  POP_JUMP_IF_FALSE    62  'to 62'

 L. 342        46  LOAD_GLOBAL              ReadTimeoutError

 L. 343        48  LOAD_FAST                'self'
               50  LOAD_FAST                'url'
               52  LOAD_STR                 'Read timed out. (read timeout=%s)'
               54  LOAD_FAST                'timeout_value'
               56  BINARY_MODULO    

 L. 342        58  CALL_FUNCTION_3       3  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            44  '44'
             62_1  COME_FROM            34  '34'

 L. 349        62  LOAD_STR                 'timed out'
               64  LOAD_GLOBAL              str
               66  LOAD_FAST                'err'
               68  CALL_FUNCTION_1       1  ''
               70  <118>                 0  ''
               72  POP_JUMP_IF_TRUE     86  'to 86'
               74  LOAD_STR                 'did not complete (read)'
               76  LOAD_GLOBAL              str

 L. 350        78  LOAD_FAST                'err'

 L. 349        80  CALL_FUNCTION_1       1  ''
               82  <118>                 0  ''
               84  POP_JUMP_IF_FALSE   102  'to 102'
             86_0  COME_FROM            72  '72'

 L. 352        86  LOAD_GLOBAL              ReadTimeoutError

 L. 353        88  LOAD_FAST                'self'
               90  LOAD_FAST                'url'
               92  LOAD_STR                 'Read timed out. (read timeout=%s)'
               94  LOAD_FAST                'timeout_value'
               96  BINARY_MODULO    

 L. 352        98  CALL_FUNCTION_3       3  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            84  '84'

Parse error at or near `<118>' instruction at offset 42

    def _make_request--- This code section failed: ---

 L. 373         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                num_requests
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               num_requests

 L. 375        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _get_timeout
               18  LOAD_FAST                'timeout'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'timeout_obj'

 L. 376        24  LOAD_FAST                'timeout_obj'
               26  LOAD_METHOD              start_connect
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          

 L. 377        32  LOAD_FAST                'timeout_obj'
               34  LOAD_ATTR                connect_timeout
               36  LOAD_FAST                'conn'
               38  STORE_ATTR               timeout

 L. 380        40  SETUP_FINALLY        56  'to 56'

 L. 381        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _validate_conn
               46  LOAD_FAST                'conn'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
               52  POP_BLOCK        
               54  JUMP_FORWARD        116  'to 116'
             56_0  COME_FROM_FINALLY    40  '40'

 L. 382        56  DUP_TOP          
               58  LOAD_GLOBAL              SocketTimeout
               60  LOAD_GLOBAL              BaseSSLError
               62  BUILD_TUPLE_2         2 
               64  <121>               114  ''
               66  POP_TOP          
               68  STORE_FAST               'e'
               70  POP_TOP          
               72  SETUP_FINALLY       106  'to 106'

 L. 384        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _raise_timeout
               78  LOAD_FAST                'e'
               80  LOAD_FAST                'url'
               82  LOAD_FAST                'conn'
               84  LOAD_ATTR                timeout
               86  LOAD_CONST               ('err', 'url', 'timeout_value')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  POP_TOP          

 L. 385        92  RAISE_VARARGS_0       0  'reraise'
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

 L. 389       116  LOAD_FAST                'chunked'
              118  POP_JUMP_IF_FALSE   142  'to 142'

 L. 390       120  LOAD_FAST                'conn'
              122  LOAD_ATTR                request_chunked
              124  LOAD_FAST                'method'
              126  LOAD_FAST                'url'
              128  BUILD_TUPLE_2         2 
              130  BUILD_MAP_0           0 
              132  LOAD_FAST                'httplib_request_kw'
              134  <164>                 1  ''
              136  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              138  POP_TOP          
              140  JUMP_FORWARD        162  'to 162'
            142_0  COME_FROM           118  '118'

 L. 392       142  LOAD_FAST                'conn'
              144  LOAD_ATTR                request
              146  LOAD_FAST                'method'
              148  LOAD_FAST                'url'
              150  BUILD_TUPLE_2         2 
              152  BUILD_MAP_0           0 
              154  LOAD_FAST                'httplib_request_kw'
              156  <164>                 1  ''
              158  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              160  POP_TOP          
            162_0  COME_FROM           140  '140'

 L. 395       162  LOAD_FAST                'timeout_obj'
              164  LOAD_ATTR                read_timeout
              166  STORE_FAST               'read_timeout'

 L. 398       168  LOAD_GLOBAL              getattr
              170  LOAD_FAST                'conn'
              172  LOAD_STR                 'sock'
              174  LOAD_CONST               None
              176  CALL_FUNCTION_3       3  ''
              178  POP_JUMP_IF_FALSE   244  'to 244'

 L. 404       180  LOAD_FAST                'read_timeout'
              182  LOAD_CONST               0
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   204  'to 204'

 L. 405       188  LOAD_GLOBAL              ReadTimeoutError

 L. 406       190  LOAD_FAST                'self'
              192  LOAD_FAST                'url'
              194  LOAD_STR                 'Read timed out. (read timeout=%s)'
              196  LOAD_FAST                'read_timeout'
              198  BINARY_MODULO    

 L. 405       200  CALL_FUNCTION_3       3  ''
              202  RAISE_VARARGS_1       1  'exception instance'
            204_0  COME_FROM           186  '186'

 L. 408       204  LOAD_FAST                'read_timeout'
              206  LOAD_GLOBAL              Timeout
              208  LOAD_ATTR                DEFAULT_TIMEOUT
              210  <117>                 0  ''
              212  POP_JUMP_IF_FALSE   232  'to 232'

 L. 409       214  LOAD_FAST                'conn'
              216  LOAD_ATTR                sock
              218  LOAD_METHOD              settimeout
              220  LOAD_GLOBAL              socket
              222  LOAD_METHOD              getdefaulttimeout
              224  CALL_METHOD_0         0  ''
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          
              230  JUMP_FORWARD        244  'to 244'
            232_0  COME_FROM           212  '212'

 L. 411       232  LOAD_FAST                'conn'
              234  LOAD_ATTR                sock
              236  LOAD_METHOD              settimeout
              238  LOAD_FAST                'read_timeout'
              240  CALL_METHOD_1         1  ''
              242  POP_TOP          
            244_0  COME_FROM           230  '230'
            244_1  COME_FROM           178  '178'

 L. 414       244  SETUP_FINALLY       352  'to 352'

 L. 415       246  SETUP_FINALLY       264  'to 264'

 L. 417       248  LOAD_FAST                'conn'
              250  LOAD_ATTR                getresponse
              252  LOAD_CONST               True
              254  LOAD_CONST               ('buffering',)
              256  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              258  STORE_FAST               'httplib_response'
              260  POP_BLOCK        
              262  JUMP_FORWARD        348  'to 348'
            264_0  COME_FROM_FINALLY   246  '246'

 L. 418       264  DUP_TOP          
              266  LOAD_GLOBAL              TypeError
          268_270  <121>               346  ''
              272  POP_TOP          
              274  POP_TOP          
              276  POP_TOP          

 L. 420       278  SETUP_FINALLY       292  'to 292'

 L. 421       280  LOAD_FAST                'conn'
              282  LOAD_METHOD              getresponse
              284  CALL_METHOD_0         0  ''
              286  STORE_FAST               'httplib_response'
              288  POP_BLOCK        
              290  JUMP_FORWARD        342  'to 342'
            292_0  COME_FROM_FINALLY   278  '278'

 L. 422       292  DUP_TOP          
              294  LOAD_GLOBAL              BaseException
          296_298  <121>               340  ''
              300  POP_TOP          
              302  STORE_FAST               'e'
              304  POP_TOP          
              306  SETUP_FINALLY       332  'to 332'

 L. 426       308  LOAD_GLOBAL              six
              310  LOAD_METHOD              raise_from
              312  LOAD_FAST                'e'
              314  LOAD_CONST               None
              316  CALL_METHOD_2         2  ''
              318  POP_TOP          
              320  POP_BLOCK        
              322  POP_EXCEPT       
              324  LOAD_CONST               None
              326  STORE_FAST               'e'
              328  DELETE_FAST              'e'
              330  JUMP_FORWARD        342  'to 342'
            332_0  COME_FROM_FINALLY   306  '306'
              332  LOAD_CONST               None
              334  STORE_FAST               'e'
              336  DELETE_FAST              'e'
              338  <48>             
              340  <48>             
            342_0  COME_FROM           330  '330'
            342_1  COME_FROM           290  '290'
              342  POP_EXCEPT       
              344  JUMP_FORWARD        348  'to 348'
              346  <48>             
            348_0  COME_FROM           344  '344'
            348_1  COME_FROM           262  '262'
              348  POP_BLOCK        
              350  JUMP_FORWARD        414  'to 414'
            352_0  COME_FROM_FINALLY   244  '244'

 L. 427       352  DUP_TOP          
              354  LOAD_GLOBAL              SocketTimeout
              356  LOAD_GLOBAL              BaseSSLError
              358  LOAD_GLOBAL              SocketError
              360  BUILD_TUPLE_3         3 
          362_364  <121>               412  ''
              366  POP_TOP          
              368  STORE_FAST               'e'
              370  POP_TOP          
              372  SETUP_FINALLY       404  'to 404'

 L. 428       374  LOAD_FAST                'self'
              376  LOAD_ATTR                _raise_timeout
              378  LOAD_FAST                'e'
              380  LOAD_FAST                'url'
              382  LOAD_FAST                'read_timeout'
              384  LOAD_CONST               ('err', 'url', 'timeout_value')
              386  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              388  POP_TOP          

 L. 429       390  RAISE_VARARGS_0       0  'reraise'
              392  POP_BLOCK        
              394  POP_EXCEPT       
              396  LOAD_CONST               None
              398  STORE_FAST               'e'
              400  DELETE_FAST              'e'
              402  JUMP_FORWARD        414  'to 414'
            404_0  COME_FROM_FINALLY   372  '372'
              404  LOAD_CONST               None
              406  STORE_FAST               'e'
              408  DELETE_FAST              'e'
              410  <48>             
              412  <48>             
            414_0  COME_FROM           402  '402'
            414_1  COME_FROM           350  '350'

 L. 432       414  LOAD_GLOBAL              getattr
              416  LOAD_FAST                'conn'
              418  LOAD_STR                 '_http_vsn_str'
              420  LOAD_STR                 'HTTP/?'
              422  CALL_FUNCTION_3       3  ''
              424  STORE_FAST               'http_version'

 L. 433       426  LOAD_GLOBAL              log
              428  LOAD_METHOD              debug

 L. 434       430  LOAD_STR                 '%s://%s:%s "%s %s %s" %s %s'

 L. 435       432  LOAD_FAST                'self'
              434  LOAD_ATTR                scheme

 L. 436       436  LOAD_FAST                'self'
              438  LOAD_ATTR                host

 L. 437       440  LOAD_FAST                'self'
              442  LOAD_ATTR                port

 L. 438       444  LOAD_FAST                'method'

 L. 439       446  LOAD_FAST                'url'

 L. 440       448  LOAD_FAST                'http_version'

 L. 441       450  LOAD_FAST                'httplib_response'
              452  LOAD_ATTR                status

 L. 442       454  LOAD_FAST                'httplib_response'
              456  LOAD_ATTR                length

 L. 433       458  CALL_METHOD_9         9  ''
              460  POP_TOP          

 L. 445       462  SETUP_FINALLY       478  'to 478'

 L. 446       464  LOAD_GLOBAL              assert_header_parsing
              466  LOAD_FAST                'httplib_response'
              468  LOAD_ATTR                msg
              470  CALL_FUNCTION_1       1  ''
              472  POP_TOP          
              474  POP_BLOCK        
              476  JUMP_FORWARD        544  'to 544'
            478_0  COME_FROM_FINALLY   462  '462'

 L. 447       478  DUP_TOP          
              480  LOAD_GLOBAL              HeaderParsingError
              482  LOAD_GLOBAL              TypeError
              484  BUILD_TUPLE_2         2 
          486_488  <121>               542  ''
              490  POP_TOP          
              492  STORE_FAST               'hpe'
              494  POP_TOP          
              496  SETUP_FINALLY       534  'to 534'

 L. 448       498  LOAD_GLOBAL              log
              500  LOAD_ATTR                warning

 L. 449       502  LOAD_STR                 'Failed to parse headers (url=%s): %s'

 L. 450       504  LOAD_FAST                'self'
              506  LOAD_METHOD              _absolute_url
              508  LOAD_FAST                'url'
              510  CALL_METHOD_1         1  ''

 L. 451       512  LOAD_FAST                'hpe'

 L. 452       514  LOAD_CONST               True

 L. 448       516  LOAD_CONST               ('exc_info',)
              518  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              520  POP_TOP          
              522  POP_BLOCK        
              524  POP_EXCEPT       
              526  LOAD_CONST               None
              528  STORE_FAST               'hpe'
              530  DELETE_FAST              'hpe'
              532  JUMP_FORWARD        544  'to 544'
            534_0  COME_FROM_FINALLY   496  '496'
              534  LOAD_CONST               None
              536  STORE_FAST               'hpe'
              538  DELETE_FAST              'hpe'
              540  <48>             
              542  <48>             
            544_0  COME_FROM           532  '532'
            544_1  COME_FROM           476  '476'

 L. 455       544  LOAD_FAST                'httplib_response'
              546  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 64

    def _absolute_url(self, path):
        return Url(scheme=(self.scheme), host=(self.host), port=(self.port), path=path).url

    def close--- This code section failed: ---

 L. 464         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pool
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 465        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 467        14  LOAD_FAST                'self'
               16  LOAD_ATTR                pool
               18  LOAD_CONST               None
               20  ROT_TWO          
               22  STORE_FAST               'old_pool'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               pool

 L. 469        28  SETUP_FINALLY        60  'to 60'
             30_0  COME_FROM            54  '54'
             30_1  COME_FROM            44  '44'

 L. 471        30  LOAD_FAST                'old_pool'
               32  LOAD_ATTR                get
               34  LOAD_CONST               False
               36  LOAD_CONST               ('block',)
               38  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               40  STORE_FAST               'conn'

 L. 472        42  LOAD_FAST                'conn'
               44  POP_JUMP_IF_FALSE_BACK    30  'to 30'

 L. 473        46  LOAD_FAST                'conn'
               48  LOAD_METHOD              close
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          
               54  JUMP_BACK            30  'to 30'
               56  POP_BLOCK        
               58  JUMP_FORWARD         80  'to 80'
             60_0  COME_FROM_FINALLY    28  '28'

 L. 475        60  DUP_TOP          
               62  LOAD_GLOBAL              queue
               64  LOAD_ATTR                Empty
               66  <121>                78  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 476        74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
               78  <48>             
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            58  '58'

Parse error at or near `None' instruction at offset -1

    def is_same_host--- This code section failed: ---

 L. 483         0  LOAD_FAST                'url'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 484        10  LOAD_CONST               True
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 487        14  LOAD_GLOBAL              get_host
               16  LOAD_FAST                'url'
               18  CALL_FUNCTION_1       1  ''
               20  UNPACK_SEQUENCE_3     3 
               22  STORE_FAST               'scheme'
               24  STORE_FAST               'host'
               26  STORE_FAST               'port'

 L. 488        28  LOAD_FAST                'host'
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    48  'to 48'

 L. 489        36  LOAD_GLOBAL              _normalize_host
               38  LOAD_FAST                'host'
               40  LOAD_FAST                'scheme'
               42  LOAD_CONST               ('scheme',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  STORE_FAST               'host'
             48_0  COME_FROM            34  '34'

 L. 492        48  LOAD_FAST                'self'
               50  LOAD_ATTR                port
               52  POP_JUMP_IF_FALSE    70  'to 70'
               54  LOAD_FAST                'port'
               56  POP_JUMP_IF_TRUE     70  'to 70'

 L. 493        58  LOAD_GLOBAL              port_by_scheme
               60  LOAD_METHOD              get
               62  LOAD_FAST                'scheme'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'port'
               68  JUMP_FORWARD         94  'to 94'
             70_0  COME_FROM            56  '56'
             70_1  COME_FROM            52  '52'

 L. 494        70  LOAD_FAST                'self'
               72  LOAD_ATTR                port
               74  POP_JUMP_IF_TRUE     94  'to 94'
               76  LOAD_FAST                'port'
               78  LOAD_GLOBAL              port_by_scheme
               80  LOAD_METHOD              get
               82  LOAD_FAST                'scheme'
               84  CALL_METHOD_1         1  ''
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE    94  'to 94'

 L. 495        90  LOAD_CONST               None
               92  STORE_FAST               'port'
             94_0  COME_FROM            88  '88'
             94_1  COME_FROM            74  '74'
             94_2  COME_FROM            68  '68'

 L. 497        94  LOAD_FAST                'scheme'
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

 L. 605         0  LOAD_FAST                'headers'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 606         8  LOAD_FAST                'self'
               10  LOAD_ATTR                headers
               12  STORE_FAST               'headers'
             14_0  COME_FROM             6  '6'

 L. 608        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'retries'
               18  LOAD_GLOBAL              Retry
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     42  'to 42'

 L. 609        24  LOAD_GLOBAL              Retry
               26  LOAD_ATTR                from_int
               28  LOAD_FAST                'retries'
               30  LOAD_FAST                'redirect'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                retries
               36  LOAD_CONST               ('redirect', 'default')
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  STORE_FAST               'retries'
             42_0  COME_FROM            22  '22'

 L. 611        42  LOAD_FAST                'release_conn'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L. 612        50  LOAD_FAST                'response_kw'
               52  LOAD_METHOD              get
               54  LOAD_STR                 'preload_content'
               56  LOAD_CONST               True
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'release_conn'
             62_0  COME_FROM            48  '48'

 L. 615        62  LOAD_FAST                'assert_same_host'
               64  POP_JUMP_IF_FALSE    88  'to 88'
               66  LOAD_FAST                'self'
               68  LOAD_METHOD              is_same_host
               70  LOAD_FAST                'url'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_TRUE     88  'to 88'

 L. 616        76  LOAD_GLOBAL              HostChangedError
               78  LOAD_FAST                'self'
               80  LOAD_FAST                'url'
               82  LOAD_FAST                'retries'
               84  CALL_FUNCTION_3       3  ''
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            74  '74'
             88_1  COME_FROM            64  '64'

 L. 619        88  LOAD_FAST                'url'
               90  LOAD_METHOD              startswith
               92  LOAD_STR                 '/'
               94  CALL_METHOD_1         1  ''
               96  POP_JUMP_IF_FALSE   114  'to 114'

 L. 620        98  LOAD_GLOBAL              six
              100  LOAD_METHOD              ensure_str
              102  LOAD_GLOBAL              _encode_target
              104  LOAD_FAST                'url'
              106  CALL_FUNCTION_1       1  ''
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'url'
              112  JUMP_FORWARD        130  'to 130'
            114_0  COME_FROM            96  '96'

 L. 622       114  LOAD_GLOBAL              six
              116  LOAD_METHOD              ensure_str
              118  LOAD_GLOBAL              parse_url
              120  LOAD_FAST                'url'
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_ATTR                url
              126  CALL_METHOD_1         1  ''
              128  STORE_FAST               'url'
            130_0  COME_FROM           112  '112'

 L. 624       130  LOAD_CONST               None
              132  STORE_FAST               'conn'

 L. 635       134  LOAD_FAST                'release_conn'
              136  STORE_FAST               'release_this_conn'

 L. 640       138  LOAD_FAST                'self'
              140  LOAD_ATTR                scheme
              142  LOAD_STR                 'http'
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   168  'to 168'

 L. 641       148  LOAD_FAST                'headers'
              150  LOAD_METHOD              copy
              152  CALL_METHOD_0         0  ''
              154  STORE_FAST               'headers'

 L. 642       156  LOAD_FAST                'headers'
              158  LOAD_METHOD              update
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                proxy_headers
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
            168_0  COME_FROM           146  '146'

 L. 646       168  LOAD_CONST               None
              170  STORE_FAST               'err'

 L. 650       172  LOAD_CONST               False
              174  STORE_FAST               'clean_exit'

 L. 654       176  LOAD_GLOBAL              set_file_position
              178  LOAD_FAST                'body'
              180  LOAD_FAST                'body_pos'
              182  CALL_FUNCTION_2       2  ''
              184  STORE_FAST               'body_pos'

 L. 656   186_188  SETUP_FINALLY       600  'to 600'
              190  SETUP_FINALLY       344  'to 344'

 L. 658       192  LOAD_FAST                'self'
              194  LOAD_METHOD              _get_timeout
              196  LOAD_FAST                'timeout'
              198  CALL_METHOD_1         1  ''
              200  STORE_FAST               'timeout_obj'

 L. 659       202  LOAD_FAST                'self'
              204  LOAD_ATTR                _get_conn
              206  LOAD_FAST                'pool_timeout'
              208  LOAD_CONST               ('timeout',)
              210  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              212  STORE_FAST               'conn'

 L. 661       214  LOAD_FAST                'timeout_obj'
              216  LOAD_ATTR                connect_timeout
              218  LOAD_FAST                'conn'
              220  STORE_ATTR               timeout

 L. 663       222  LOAD_FAST                'self'
              224  LOAD_ATTR                proxy
              226  LOAD_CONST               None
              228  <117>                 1  ''
              230  JUMP_IF_FALSE_OR_POP   244  'to 244'
              232  LOAD_GLOBAL              getattr

 L. 664       234  LOAD_FAST                'conn'
              236  LOAD_STR                 'sock'
              238  LOAD_CONST               None

 L. 663       240  CALL_FUNCTION_3       3  ''
              242  UNARY_NOT        
            244_0  COME_FROM           230  '230'
              244  STORE_FAST               'is_new_proxy_conn'

 L. 666       246  LOAD_FAST                'is_new_proxy_conn'
          248_250  POP_JUMP_IF_FALSE   262  'to 262'

 L. 667       252  LOAD_FAST                'self'
              254  LOAD_METHOD              _prepare_proxy
              256  LOAD_FAST                'conn'
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          
            262_0  COME_FROM           248  '248'

 L. 670       262  LOAD_FAST                'self'
              264  LOAD_ATTR                _make_request

 L. 671       266  LOAD_FAST                'conn'

 L. 672       268  LOAD_FAST                'method'

 L. 673       270  LOAD_FAST                'url'

 L. 674       272  LOAD_FAST                'timeout_obj'

 L. 675       274  LOAD_FAST                'body'

 L. 676       276  LOAD_FAST                'headers'

 L. 677       278  LOAD_FAST                'chunked'

 L. 670       280  LOAD_CONST               ('timeout', 'body', 'headers', 'chunked')
              282  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              284  STORE_FAST               'httplib_response'

 L. 684       286  LOAD_FAST                'release_conn'
          288_290  POP_JUMP_IF_TRUE    296  'to 296'
              292  LOAD_FAST                'conn'
              294  JUMP_FORWARD        298  'to 298'
            296_0  COME_FROM           288  '288'
              296  LOAD_CONST               None
            298_0  COME_FROM           294  '294'
              298  STORE_FAST               'response_conn'

 L. 687       300  LOAD_FAST                'method'
              302  LOAD_FAST                'response_kw'
              304  LOAD_STR                 'request_method'
              306  STORE_SUBSCR     

 L. 690       308  LOAD_FAST                'self'
              310  LOAD_ATTR                ResponseCls
              312  LOAD_ATTR                from_httplib

 L. 691       314  LOAD_FAST                'httplib_response'

 L. 690       316  BUILD_TUPLE_1         1 

 L. 692       318  LOAD_FAST                'self'

 L. 693       320  LOAD_FAST                'response_conn'

 L. 694       322  LOAD_FAST                'retries'

 L. 690       324  LOAD_CONST               ('pool', 'connection', 'retries')
              326  BUILD_CONST_KEY_MAP_3     3 

 L. 695       328  LOAD_FAST                'response_kw'

 L. 690       330  <164>                 1  ''
              332  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              334  STORE_FAST               'response'

 L. 699       336  LOAD_CONST               True
              338  STORE_FAST               'clean_exit'
              340  POP_BLOCK        
              342  JUMP_FORWARD        556  'to 556'
            344_0  COME_FROM_FINALLY   190  '190'

 L. 701       344  DUP_TOP          
              346  LOAD_GLOBAL              EmptyPoolError
          348_350  <121>               372  ''
              352  POP_TOP          
              354  POP_TOP          
              356  POP_TOP          

 L. 703       358  LOAD_CONST               True
              360  STORE_FAST               'clean_exit'

 L. 704       362  LOAD_CONST               False
              364  STORE_FAST               'release_this_conn'

 L. 705       366  RAISE_VARARGS_0       0  'reraise'
              368  POP_EXCEPT       
              370  JUMP_FORWARD        556  'to 556'

 L. 707       372  DUP_TOP          

 L. 708       374  LOAD_GLOBAL              TimeoutError

 L. 709       376  LOAD_GLOBAL              HTTPException

 L. 710       378  LOAD_GLOBAL              SocketError

 L. 711       380  LOAD_GLOBAL              ProtocolError

 L. 712       382  LOAD_GLOBAL              BaseSSLError

 L. 713       384  LOAD_GLOBAL              SSLError

 L. 714       386  LOAD_GLOBAL              CertificateError

 L. 707       388  BUILD_TUPLE_7         7 
          390_392  <121>               554  ''
              394  POP_TOP          
              396  STORE_FAST               'e'
              398  POP_TOP          
              400  SETUP_FINALLY       546  'to 546'

 L. 718       402  LOAD_CONST               False
              404  STORE_FAST               'clean_exit'

 L. 719       406  LOAD_GLOBAL              isinstance
              408  LOAD_FAST                'e'
              410  LOAD_GLOBAL              BaseSSLError
              412  LOAD_GLOBAL              CertificateError
              414  BUILD_TUPLE_2         2 
              416  CALL_FUNCTION_2       2  ''
          418_420  POP_JUMP_IF_FALSE   432  'to 432'

 L. 720       422  LOAD_GLOBAL              SSLError
              424  LOAD_FAST                'e'
              426  CALL_FUNCTION_1       1  ''
              428  STORE_FAST               'e'
              430  JUMP_FORWARD        494  'to 494'
            432_0  COME_FROM           418  '418'

 L. 721       432  LOAD_GLOBAL              isinstance
              434  LOAD_FAST                'e'
              436  LOAD_GLOBAL              SocketError
              438  LOAD_GLOBAL              NewConnectionError
              440  BUILD_TUPLE_2         2 
              442  CALL_FUNCTION_2       2  ''
          444_446  POP_JUMP_IF_FALSE   468  'to 468'
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                proxy
          452_454  POP_JUMP_IF_FALSE   468  'to 468'

 L. 722       456  LOAD_GLOBAL              ProxyError
              458  LOAD_STR                 'Cannot connect to proxy.'
              460  LOAD_FAST                'e'
              462  CALL_FUNCTION_2       2  ''
              464  STORE_FAST               'e'
              466  JUMP_FORWARD        494  'to 494'
            468_0  COME_FROM           452  '452'
            468_1  COME_FROM           444  '444'

 L. 723       468  LOAD_GLOBAL              isinstance
              470  LOAD_FAST                'e'
              472  LOAD_GLOBAL              SocketError
              474  LOAD_GLOBAL              HTTPException
              476  BUILD_TUPLE_2         2 
              478  CALL_FUNCTION_2       2  ''
          480_482  POP_JUMP_IF_FALSE   494  'to 494'

 L. 724       484  LOAD_GLOBAL              ProtocolError
              486  LOAD_STR                 'Connection aborted.'
              488  LOAD_FAST                'e'
              490  CALL_FUNCTION_2       2  ''
              492  STORE_FAST               'e'
            494_0  COME_FROM           480  '480'
            494_1  COME_FROM           466  '466'
            494_2  COME_FROM           430  '430'

 L. 726       494  LOAD_FAST                'retries'
              496  LOAD_ATTR                increment

 L. 727       498  LOAD_FAST                'method'
              500  LOAD_FAST                'url'
              502  LOAD_FAST                'e'
              504  LOAD_FAST                'self'
              506  LOAD_GLOBAL              sys
              508  LOAD_METHOD              exc_info
              510  CALL_METHOD_0         0  ''
              512  LOAD_CONST               2
              514  BINARY_SUBSCR    

 L. 726       516  LOAD_CONST               ('error', '_pool', '_stacktrace')
              518  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              520  STORE_FAST               'retries'

 L. 729       522  LOAD_FAST                'retries'
              524  LOAD_METHOD              sleep
              526  CALL_METHOD_0         0  ''
              528  POP_TOP          

 L. 732       530  LOAD_FAST                'e'
              532  STORE_FAST               'err'
              534  POP_BLOCK        
              536  POP_EXCEPT       
              538  LOAD_CONST               None
              540  STORE_FAST               'e'
              542  DELETE_FAST              'e'
              544  JUMP_FORWARD        556  'to 556'
            546_0  COME_FROM_FINALLY   400  '400'
              546  LOAD_CONST               None
              548  STORE_FAST               'e'
              550  DELETE_FAST              'e'
              552  <48>             
              554  <48>             
            556_0  COME_FROM           544  '544'
            556_1  COME_FROM           370  '370'
            556_2  COME_FROM           342  '342'
              556  POP_BLOCK        

 L. 735       558  LOAD_FAST                'clean_exit'
          560_562  POP_JUMP_IF_TRUE    582  'to 582'

 L. 740       564  LOAD_FAST                'conn'
          566_568  JUMP_IF_FALSE_OR_POP   576  'to 576'
              570  LOAD_FAST                'conn'
              572  LOAD_METHOD              close
              574  CALL_METHOD_0         0  ''
            576_0  COME_FROM           566  '566'
              576  STORE_FAST               'conn'

 L. 741       578  LOAD_CONST               True
              580  STORE_FAST               'release_this_conn'
            582_0  COME_FROM           560  '560'

 L. 743       582  LOAD_FAST                'release_this_conn'
          584_586  POP_JUMP_IF_FALSE   642  'to 642'

 L. 747       588  LOAD_FAST                'self'
              590  LOAD_METHOD              _put_conn
              592  LOAD_FAST                'conn'
              594  CALL_METHOD_1         1  ''
              596  POP_TOP          
              598  JUMP_FORWARD        642  'to 642'
            600_0  COME_FROM_FINALLY   186  '186'

 L. 735       600  LOAD_FAST                'clean_exit'
          602_604  POP_JUMP_IF_TRUE    624  'to 624'

 L. 740       606  LOAD_FAST                'conn'
          608_610  JUMP_IF_FALSE_OR_POP   618  'to 618'
              612  LOAD_FAST                'conn'
              614  LOAD_METHOD              close
              616  CALL_METHOD_0         0  ''
            618_0  COME_FROM           608  '608'
              618  STORE_FAST               'conn'

 L. 741       620  LOAD_CONST               True
              622  STORE_FAST               'release_this_conn'
            624_0  COME_FROM           602  '602'

 L. 743       624  LOAD_FAST                'release_this_conn'
          626_628  POP_JUMP_IF_FALSE   640  'to 640'

 L. 747       630  LOAD_FAST                'self'
              632  LOAD_METHOD              _put_conn
              634  LOAD_FAST                'conn'
              636  CALL_METHOD_1         1  ''
              638  POP_TOP          
            640_0  COME_FROM           626  '626'
              640  <48>             
            642_0  COME_FROM           598  '598'
            642_1  COME_FROM           584  '584'

 L. 749       642  LOAD_FAST                'conn'
          644_646  POP_JUMP_IF_TRUE    706  'to 706'

 L. 751       648  LOAD_GLOBAL              log
              650  LOAD_METHOD              warning

 L. 752       652  LOAD_STR                 "Retrying (%r) after connection broken by '%r': %s"
              654  LOAD_FAST                'retries'
              656  LOAD_FAST                'err'
              658  LOAD_FAST                'url'

 L. 751       660  CALL_METHOD_4         4  ''
              662  POP_TOP          

 L. 754       664  LOAD_FAST                'self'
              666  LOAD_ATTR                urlopen

 L. 755       668  LOAD_FAST                'method'

 L. 756       670  LOAD_FAST                'url'

 L. 757       672  LOAD_FAST                'body'

 L. 758       674  LOAD_FAST                'headers'

 L. 759       676  LOAD_FAST                'retries'

 L. 760       678  LOAD_FAST                'redirect'

 L. 761       680  LOAD_FAST                'assert_same_host'

 L. 754       682  BUILD_TUPLE_7         7 

 L. 762       684  LOAD_FAST                'timeout'

 L. 763       686  LOAD_FAST                'pool_timeout'

 L. 764       688  LOAD_FAST                'release_conn'

 L. 765       690  LOAD_FAST                'chunked'

 L. 766       692  LOAD_FAST                'body_pos'

 L. 754       694  LOAD_CONST               ('timeout', 'pool_timeout', 'release_conn', 'chunked', 'body_pos')
              696  BUILD_CONST_KEY_MAP_5     5 

 L. 767       698  LOAD_FAST                'response_kw'

 L. 754       700  <164>                 1  ''
              702  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              704  RETURN_VALUE     
            706_0  COME_FROM           644  '644'

 L. 771       706  LOAD_FAST                'redirect'
          708_710  JUMP_IF_FALSE_OR_POP   718  'to 718'
              712  LOAD_FAST                'response'
              714  LOAD_METHOD              get_redirect_location
              716  CALL_METHOD_0         0  ''
            718_0  COME_FROM           708  '708'
              718  STORE_FAST               'redirect_location'

 L. 772       720  LOAD_FAST                'redirect_location'
          722_724  POP_JUMP_IF_FALSE   882  'to 882'

 L. 773       726  LOAD_FAST                'response'
              728  LOAD_ATTR                status
              730  LOAD_CONST               303
              732  COMPARE_OP               ==
          734_736  POP_JUMP_IF_FALSE   742  'to 742'

 L. 774       738  LOAD_STR                 'GET'
              740  STORE_FAST               'method'
            742_0  COME_FROM           734  '734'

 L. 776       742  SETUP_FINALLY       766  'to 766'

 L. 777       744  LOAD_FAST                'retries'
              746  LOAD_ATTR                increment
              748  LOAD_FAST                'method'
              750  LOAD_FAST                'url'
              752  LOAD_FAST                'response'
              754  LOAD_FAST                'self'
              756  LOAD_CONST               ('response', '_pool')
              758  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              760  STORE_FAST               'retries'
              762  POP_BLOCK        
              764  JUMP_FORWARD        808  'to 808'
            766_0  COME_FROM_FINALLY   742  '742'

 L. 778       766  DUP_TOP          
              768  LOAD_GLOBAL              MaxRetryError
          770_772  <121>               806  ''
              774  POP_TOP          
              776  POP_TOP          
              778  POP_TOP          

 L. 779       780  LOAD_FAST                'retries'
              782  LOAD_ATTR                raise_on_redirect
          784_786  POP_JUMP_IF_FALSE   798  'to 798'

 L. 780       788  LOAD_FAST                'response'
              790  LOAD_METHOD              drain_conn
              792  CALL_METHOD_0         0  ''
              794  POP_TOP          

 L. 781       796  RAISE_VARARGS_0       0  'reraise'
            798_0  COME_FROM           784  '784'

 L. 782       798  LOAD_FAST                'response'
              800  ROT_FOUR         
              802  POP_EXCEPT       
              804  RETURN_VALUE     
              806  <48>             
            808_0  COME_FROM           764  '764'

 L. 784       808  LOAD_FAST                'response'
              810  LOAD_METHOD              drain_conn
              812  CALL_METHOD_0         0  ''
              814  POP_TOP          

 L. 785       816  LOAD_FAST                'retries'
              818  LOAD_METHOD              sleep_for_retry
              820  LOAD_FAST                'response'
              822  CALL_METHOD_1         1  ''
              824  POP_TOP          

 L. 786       826  LOAD_GLOBAL              log
              828  LOAD_METHOD              debug
              830  LOAD_STR                 'Redirecting %s -> %s'
              832  LOAD_FAST                'url'
              834  LOAD_FAST                'redirect_location'
              836  CALL_METHOD_3         3  ''
              838  POP_TOP          

 L. 787       840  LOAD_FAST                'self'
              842  LOAD_ATTR                urlopen

 L. 788       844  LOAD_FAST                'method'

 L. 789       846  LOAD_FAST                'redirect_location'

 L. 790       848  LOAD_FAST                'body'

 L. 791       850  LOAD_FAST                'headers'

 L. 787       852  BUILD_TUPLE_4         4 

 L. 792       854  LOAD_FAST                'retries'

 L. 793       856  LOAD_FAST                'redirect'

 L. 794       858  LOAD_FAST                'assert_same_host'

 L. 795       860  LOAD_FAST                'timeout'

 L. 796       862  LOAD_FAST                'pool_timeout'

 L. 797       864  LOAD_FAST                'release_conn'

 L. 798       866  LOAD_FAST                'chunked'

 L. 799       868  LOAD_FAST                'body_pos'

 L. 787       870  LOAD_CONST               ('retries', 'redirect', 'assert_same_host', 'timeout', 'pool_timeout', 'release_conn', 'chunked', 'body_pos')
              872  BUILD_CONST_KEY_MAP_8     8 

 L. 800       874  LOAD_FAST                'response_kw'

 L. 787       876  <164>                 1  ''
              878  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              880  RETURN_VALUE     
            882_0  COME_FROM           722  '722'

 L. 804       882  LOAD_GLOBAL              bool
              884  LOAD_FAST                'response'
              886  LOAD_METHOD              getheader
              888  LOAD_STR                 'Retry-After'
              890  CALL_METHOD_1         1  ''
              892  CALL_FUNCTION_1       1  ''
              894  STORE_FAST               'has_retry_after'

 L. 805       896  LOAD_FAST                'retries'
              898  LOAD_METHOD              is_retry
              900  LOAD_FAST                'method'
              902  LOAD_FAST                'response'
              904  LOAD_ATTR                status
              906  LOAD_FAST                'has_retry_after'
              908  CALL_METHOD_3         3  ''
          910_912  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 806       914  SETUP_FINALLY       938  'to 938'

 L. 807       916  LOAD_FAST                'retries'
              918  LOAD_ATTR                increment
              920  LOAD_FAST                'method'
              922  LOAD_FAST                'url'
              924  LOAD_FAST                'response'
              926  LOAD_FAST                'self'
              928  LOAD_CONST               ('response', '_pool')
              930  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              932  STORE_FAST               'retries'
              934  POP_BLOCK        
              936  JUMP_FORWARD        980  'to 980'
            938_0  COME_FROM_FINALLY   914  '914'

 L. 808       938  DUP_TOP          
              940  LOAD_GLOBAL              MaxRetryError
          942_944  <121>               978  ''
              946  POP_TOP          
              948  POP_TOP          
              950  POP_TOP          

 L. 809       952  LOAD_FAST                'retries'
              954  LOAD_ATTR                raise_on_status
          956_958  POP_JUMP_IF_FALSE   970  'to 970'

 L. 810       960  LOAD_FAST                'response'
              962  LOAD_METHOD              drain_conn
              964  CALL_METHOD_0         0  ''
              966  POP_TOP          

 L. 811       968  RAISE_VARARGS_0       0  'reraise'
            970_0  COME_FROM           956  '956'

 L. 812       970  LOAD_FAST                'response'
              972  ROT_FOUR         
              974  POP_EXCEPT       
              976  RETURN_VALUE     
              978  <48>             
            980_0  COME_FROM           936  '936'

 L. 814       980  LOAD_FAST                'response'
              982  LOAD_METHOD              drain_conn
              984  CALL_METHOD_0         0  ''
              986  POP_TOP          

 L. 815       988  LOAD_FAST                'retries'
              990  LOAD_METHOD              sleep
              992  LOAD_FAST                'response'
              994  CALL_METHOD_1         1  ''
              996  POP_TOP          

 L. 816       998  LOAD_GLOBAL              log
             1000  LOAD_METHOD              debug
             1002  LOAD_STR                 'Retry: %s'
             1004  LOAD_FAST                'url'
             1006  CALL_METHOD_2         2  ''
             1008  POP_TOP          

 L. 817      1010  LOAD_FAST                'self'
             1012  LOAD_ATTR                urlopen

 L. 818      1014  LOAD_FAST                'method'

 L. 819      1016  LOAD_FAST                'url'

 L. 820      1018  LOAD_FAST                'body'

 L. 821      1020  LOAD_FAST                'headers'

 L. 817      1022  BUILD_TUPLE_4         4 

 L. 822      1024  LOAD_FAST                'retries'

 L. 823      1026  LOAD_FAST                'redirect'

 L. 824      1028  LOAD_FAST                'assert_same_host'

 L. 825      1030  LOAD_FAST                'timeout'

 L. 826      1032  LOAD_FAST                'pool_timeout'

 L. 827      1034  LOAD_FAST                'release_conn'

 L. 828      1036  LOAD_FAST                'chunked'

 L. 829      1038  LOAD_FAST                'body_pos'

 L. 817      1040  LOAD_CONST               ('retries', 'redirect', 'assert_same_host', 'timeout', 'pool_timeout', 'release_conn', 'chunked', 'body_pos')
             1042  BUILD_CONST_KEY_MAP_8     8 

 L. 830      1044  LOAD_FAST                'response_kw'

 L. 817      1046  <164>                 1  ''
             1048  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1050  RETURN_VALUE     
           1052_0  COME_FROM           910  '910'

 L. 833      1052  LOAD_FAST                'response'
             1054  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class HTTPSConnectionPool(HTTPConnectionPool):
    __doc__ = '\n    Same as :class:`.HTTPConnectionPool`, but HTTPS.\n\n    When Python is compiled with the :mod:`ssl` module, then\n    :class:`.VerifiedHTTPSConnection` is used, which *can* verify certificates,\n    instead of :class:`.HTTPSConnection`.\n\n    :class:`.VerifiedHTTPSConnection` uses one of ``assert_fingerprint``,\n    ``assert_hostname`` and ``host`` in this order to verify connections.\n    If ``assert_hostname`` is False, no verification is done.\n\n    The ``key_file``, ``cert_file``, ``cert_reqs``, ``ca_certs``,\n    ``ca_cert_dir``, ``ssl_version``, ``key_password`` are only used if :mod:`ssl`\n    is available and are fed into :meth:`urllib3.util.ssl_wrap_socket` to upgrade\n    the connection socket into an SSL socket.\n    '
    scheme = 'https'
    ConnectionCls = HTTPSConnection

    def __init__--- This code section failed: ---

 L. 881         0  LOAD_GLOBAL              HTTPConnectionPool
                2  LOAD_ATTR                __init__

 L. 882         4  LOAD_FAST                'self'

 L. 883         6  LOAD_FAST                'host'

 L. 884         8  LOAD_FAST                'port'

 L. 885        10  LOAD_FAST                'strict'

 L. 886        12  LOAD_FAST                'timeout'

 L. 887        14  LOAD_FAST                'maxsize'

 L. 888        16  LOAD_FAST                'block'

 L. 889        18  LOAD_FAST                'headers'

 L. 890        20  LOAD_FAST                'retries'

 L. 891        22  LOAD_FAST                '_proxy'

 L. 892        24  LOAD_FAST                '_proxy_headers'

 L. 881        26  BUILD_TUPLE_11       11 
               28  BUILD_MAP_0           0 

 L. 893        30  LOAD_FAST                'conn_kw'

 L. 881        32  <164>                 1  ''
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  POP_TOP          

 L. 896        38  LOAD_FAST                'key_file'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               key_file

 L. 897        44  LOAD_FAST                'cert_file'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               cert_file

 L. 898        50  LOAD_FAST                'cert_reqs'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               cert_reqs

 L. 899        56  LOAD_FAST                'key_password'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               key_password

 L. 900        62  LOAD_FAST                'ca_certs'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               ca_certs

 L. 901        68  LOAD_FAST                'ca_cert_dir'
               70  LOAD_FAST                'self'
               72  STORE_ATTR               ca_cert_dir

 L. 902        74  LOAD_FAST                'ssl_version'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               ssl_version

 L. 903        80  LOAD_FAST                'assert_hostname'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               assert_hostname

 L. 904        86  LOAD_FAST                'assert_fingerprint'
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
        Establish tunnel connection early, because otherwise httplib
        would improperly set Host: header to proxy's IP:port.
        """
        conn.set_tunnelself._proxy_hostself.portself.proxy_headers
        conn.connect()

    def _new_conn--- This code section failed: ---

 L. 938         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                num_connections
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               num_connections

 L. 939        14  LOAD_GLOBAL              log
               16  LOAD_METHOD              debug

 L. 940        18  LOAD_STR                 'Starting new HTTPS connection (%d): %s:%s'

 L. 941        20  LOAD_FAST                'self'
               22  LOAD_ATTR                num_connections

 L. 942        24  LOAD_FAST                'self'
               26  LOAD_ATTR                host

 L. 943        28  LOAD_FAST                'self'
               30  LOAD_ATTR                port
               32  JUMP_IF_TRUE_OR_POP    36  'to 36'
               34  LOAD_STR                 '443'
             36_0  COME_FROM            32  '32'

 L. 939        36  CALL_METHOD_4         4  ''
               38  POP_TOP          

 L. 946        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ConnectionCls
               44  POP_JUMP_IF_FALSE    56  'to 56'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                ConnectionCls
               50  LOAD_GLOBAL              DummyConnection
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    64  'to 64'
             56_0  COME_FROM            44  '44'

 L. 947        56  LOAD_GLOBAL              SSLError

 L. 948        58  LOAD_STR                 "Can't connect to HTTPS URL because the SSL module is not available."

 L. 947        60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'

 L. 951        64  LOAD_FAST                'self'
               66  LOAD_ATTR                host
               68  STORE_FAST               'actual_host'

 L. 952        70  LOAD_FAST                'self'
               72  LOAD_ATTR                port
               74  STORE_FAST               'actual_port'

 L. 953        76  LOAD_FAST                'self'
               78  LOAD_ATTR                proxy
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   102  'to 102'

 L. 954        86  LOAD_FAST                'self'
               88  LOAD_ATTR                proxy
               90  LOAD_ATTR                host
               92  STORE_FAST               'actual_host'

 L. 955        94  LOAD_FAST                'self'
               96  LOAD_ATTR                proxy
               98  LOAD_ATTR                port
              100  STORE_FAST               'actual_port'
            102_0  COME_FROM            84  '84'

 L. 957       102  LOAD_FAST                'self'
              104  LOAD_ATTR                ConnectionCls
              106  BUILD_TUPLE_0         0 

 L. 958       108  LOAD_FAST                'actual_host'

 L. 959       110  LOAD_FAST                'actual_port'

 L. 960       112  LOAD_FAST                'self'
              114  LOAD_ATTR                timeout
              116  LOAD_ATTR                connect_timeout

 L. 961       118  LOAD_FAST                'self'
              120  LOAD_ATTR                strict

 L. 962       122  LOAD_FAST                'self'
              124  LOAD_ATTR                cert_file

 L. 963       126  LOAD_FAST                'self'
              128  LOAD_ATTR                key_file

 L. 964       130  LOAD_FAST                'self'
              132  LOAD_ATTR                key_password

 L. 957       134  LOAD_CONST               ('host', 'port', 'timeout', 'strict', 'cert_file', 'key_file', 'key_password')
              136  BUILD_CONST_KEY_MAP_7     7 

 L. 965       138  LOAD_FAST                'self'
              140  LOAD_ATTR                conn_kw

 L. 957       142  <164>                 1  ''
              144  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              146  STORE_FAST               'conn'

 L. 968       148  LOAD_FAST                'self'
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

 L.1012         0  LOAD_GLOBAL              get_host
                2  LOAD_FAST                'url'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_3     3 
                8  STORE_FAST               'scheme'
               10  STORE_FAST               'host'
               12  STORE_FAST               'port'

 L.1013        14  LOAD_FAST                'port'
               16  JUMP_IF_TRUE_OR_POP    28  'to 28'
               18  LOAD_GLOBAL              port_by_scheme
               20  LOAD_METHOD              get
               22  LOAD_FAST                'scheme'
               24  LOAD_CONST               80
               26  CALL_METHOD_2         2  ''
             28_0  COME_FROM            16  '16'
               28  STORE_FAST               'port'

 L.1014        30  LOAD_FAST                'scheme'
               32  LOAD_STR                 'https'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    58  'to 58'

 L.1015        38  LOAD_GLOBAL              HTTPSConnectionPool
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

 L.1017        58  LOAD_GLOBAL              HTTPConnectionPool
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