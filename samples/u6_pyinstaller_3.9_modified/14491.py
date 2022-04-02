# uncompyle6 version 3.7.4
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
from util.url import get_host, Url, NORMALIZABLE_SCHEMES
from util.queue import LifoQueue
xrange = six.moves.xrange
log = logging.getLogger(__name__)
_Default = object()

class ConnectionPool(object):
    __doc__ = '\n    Base class for all connection pools, such as\n    :class:`.HTTPConnectionPool` and :class:`.HTTPSConnectionPool`.\n    '
    scheme = None
    QueueCls = LifoQueue

    def __init__(self, host, port=None):
        if not host:
            raise LocationValueError('No host specified.')
        self.host = _ipv6_host(host, self.scheme)
        self._proxy_host = host.lower()
        self.port = port

    def __str__(self):
        return '%s(host=%r, port=%r)' % (type(self).__name__,
         self.host, self.port)

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

 L. 164         0  LOAD_GLOBAL              ConnectionPool
                2  LOAD_METHOD              __init__
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'host'
                8  LOAD_FAST                'port'
               10  CALL_METHOD_3         3  ''
               12  POP_TOP          

 L. 165        14  LOAD_GLOBAL              RequestMethods
               16  LOAD_METHOD              __init__
               18  LOAD_FAST                'self'
               20  LOAD_FAST                'headers'
               22  CALL_METHOD_2         2  ''
               24  POP_TOP          

 L. 167        26  LOAD_FAST                'strict'
               28  LOAD_FAST                'self'
               30  STORE_ATTR               strict

 L. 169        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'timeout'
               36  LOAD_GLOBAL              Timeout
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_TRUE     52  'to 52'

 L. 170        42  LOAD_GLOBAL              Timeout
               44  LOAD_METHOD              from_float
               46  LOAD_FAST                'timeout'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'timeout'
             52_0  COME_FROM            40  '40'

 L. 172        52  LOAD_FAST                'retries'
               54  LOAD_CONST               None
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 173        60  LOAD_GLOBAL              Retry
               62  LOAD_ATTR                DEFAULT
               64  STORE_FAST               'retries'
             66_0  COME_FROM            58  '58'

 L. 175        66  LOAD_FAST                'timeout'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               timeout

 L. 176        72  LOAD_FAST                'retries'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               retries

 L. 178        78  LOAD_FAST                'self'
               80  LOAD_METHOD              QueueCls
               82  LOAD_FAST                'maxsize'
               84  CALL_METHOD_1         1  ''
               86  LOAD_FAST                'self'
               88  STORE_ATTR               pool

 L. 179        90  LOAD_FAST                'block'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               block

 L. 181        96  LOAD_FAST                '_proxy'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               proxy

 L. 182       102  LOAD_FAST                '_proxy_headers'
              104  JUMP_IF_TRUE_OR_POP   108  'to 108'
              106  BUILD_MAP_0           0 
            108_0  COME_FROM           104  '104'
              108  LOAD_FAST                'self'
              110  STORE_ATTR               proxy_headers

 L. 185       112  LOAD_GLOBAL              xrange
              114  LOAD_FAST                'maxsize'
              116  CALL_FUNCTION_1       1  ''
              118  GET_ITER         
              120  FOR_ITER            138  'to 138'
              122  STORE_FAST               '_'

 L. 186       124  LOAD_FAST                'self'
              126  LOAD_ATTR                pool
              128  LOAD_METHOD              put
              130  LOAD_CONST               None
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
              136  JUMP_BACK           120  'to 120'

 L. 189       138  LOAD_CONST               0
              140  LOAD_FAST                'self'
              142  STORE_ATTR               num_connections

 L. 190       144  LOAD_CONST               0
              146  LOAD_FAST                'self'
              148  STORE_ATTR               num_requests

 L. 191       150  LOAD_FAST                'conn_kw'
              152  LOAD_FAST                'self'
              154  STORE_ATTR               conn_kw

 L. 193       156  LOAD_FAST                'self'
              158  LOAD_ATTR                proxy
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L. 197       162  LOAD_FAST                'self'
              164  LOAD_ATTR                conn_kw
              166  LOAD_METHOD              setdefault
              168  LOAD_STR                 'socket_options'
              170  BUILD_LIST_0          0 
              172  CALL_METHOD_2         2  ''
              174  POP_TOP          
            176_0  COME_FROM           160  '160'

Parse error at or near `<117>' instruction at offset 56

    def _new_conn--- This code section failed: ---

 L. 203         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                num_connections
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               num_connections

 L. 204        14  LOAD_GLOBAL              log
               16  LOAD_METHOD              debug
               18  LOAD_STR                 'Starting new HTTP connection (%d): %s:%s'

 L. 205        20  LOAD_FAST                'self'
               22  LOAD_ATTR                num_connections
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                host
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                port
               32  JUMP_IF_TRUE_OR_POP    36  'to 36'
               34  LOAD_STR                 '80'
             36_0  COME_FROM            32  '32'

 L. 204        36  CALL_METHOD_4         4  ''
               38  POP_TOP          

 L. 207        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ConnectionCls
               44  BUILD_TUPLE_0         0 
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                host
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                port

 L. 208        54  LOAD_FAST                'self'
               56  LOAD_ATTR                timeout
               58  LOAD_ATTR                connect_timeout

 L. 209        60  LOAD_FAST                'self'
               62  LOAD_ATTR                strict

 L. 207        64  LOAD_CONST               ('host', 'port', 'timeout', 'strict')
               66  BUILD_CONST_KEY_MAP_4     4 

 L. 209        68  LOAD_FAST                'self'
               70  LOAD_ATTR                conn_kw

 L. 207        72  <164>                 1  ''
               74  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               76  STORE_FAST               'conn'

 L. 210        78  LOAD_FAST                'conn'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 72

    def _get_conn--- This code section failed: ---

 L. 224         0  LOAD_CONST               None
                2  STORE_FAST               'conn'

 L. 225         4  SETUP_FINALLY        28  'to 28'

 L. 226         6  LOAD_FAST                'self'
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

 L. 228        28  DUP_TOP          
               30  LOAD_GLOBAL              AttributeError
               32  <121>                54  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 229        40  LOAD_GLOBAL              ClosedPoolError
               42  LOAD_FAST                'self'
               44  LOAD_STR                 'Pool is closed.'
               46  CALL_FUNCTION_2       2  ''
               48  RAISE_VARARGS_1       1  'exception instance'
               50  POP_EXCEPT       
               52  JUMP_FORWARD         90  'to 90'

 L. 231        54  DUP_TOP          
               56  LOAD_GLOBAL              queue
               58  LOAD_ATTR                Empty
               60  <121>                88  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 232        68  LOAD_FAST                'self'
               70  LOAD_ATTR                block
               72  POP_JUMP_IF_FALSE    84  'to 84'

 L. 233        74  LOAD_GLOBAL              EmptyPoolError
               76  LOAD_FAST                'self'

 L. 234        78  LOAD_STR                 'Pool reached maximum size and no more connections are allowed.'

 L. 233        80  CALL_FUNCTION_2       2  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            72  '72'

 L. 236        84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
               88  <48>             
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            52  '52'
             90_2  COME_FROM            26  '26'

 L. 239        90  LOAD_FAST                'conn'
               92  POP_JUMP_IF_FALSE   144  'to 144'
               94  LOAD_GLOBAL              is_connection_dropped
               96  LOAD_FAST                'conn'
               98  CALL_FUNCTION_1       1  ''
              100  POP_JUMP_IF_FALSE   144  'to 144'

 L. 240       102  LOAD_GLOBAL              log
              104  LOAD_METHOD              debug
              106  LOAD_STR                 'Resetting dropped connection: %s'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                host
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          

 L. 241       116  LOAD_FAST                'conn'
              118  LOAD_METHOD              close
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          

 L. 242       124  LOAD_GLOBAL              getattr
              126  LOAD_FAST                'conn'
              128  LOAD_STR                 'auto_open'
              130  LOAD_CONST               1
              132  CALL_FUNCTION_3       3  ''
              134  LOAD_CONST               0
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   144  'to 144'

 L. 246       140  LOAD_CONST               None
              142  STORE_FAST               'conn'
            144_0  COME_FROM           138  '138'
            144_1  COME_FROM           100  '100'
            144_2  COME_FROM            92  '92'

 L. 248       144  LOAD_FAST                'conn'
              146  JUMP_IF_TRUE_OR_POP   154  'to 154'
              148  LOAD_FAST                'self'
              150  LOAD_METHOD              _new_conn
              152  CALL_METHOD_0         0  ''
            154_0  COME_FROM           146  '146'
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 32

    def _put_conn--- This code section failed: ---

 L. 264         0  SETUP_FINALLY        24  'to 24'

 L. 265         2  LOAD_FAST                'self'
                4  LOAD_ATTR                pool
                6  LOAD_ATTR                put
                8  LOAD_FAST                'conn'
               10  LOAD_CONST               False
               12  LOAD_CONST               ('block',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  POP_TOP          

 L. 266        18  POP_BLOCK        
               20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L. 267        24  DUP_TOP          
               26  LOAD_GLOBAL              AttributeError
               28  <121>                40  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 269        36  POP_EXCEPT       
               38  JUMP_FORWARD         74  'to 74'

 L. 270        40  DUP_TOP          
               42  LOAD_GLOBAL              queue
               44  LOAD_ATTR                Full
               46  <121>                72  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 272        54  LOAD_GLOBAL              log
               56  LOAD_METHOD              warning

 L. 273        58  LOAD_STR                 'Connection pool is full, discarding connection: %s'

 L. 274        60  LOAD_FAST                'self'
               62  LOAD_ATTR                host

 L. 272        64  CALL_METHOD_2         2  ''
               66  POP_TOP          
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
               72  <48>             
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            38  '38'

 L. 277        74  LOAD_FAST                'conn'
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 278        78  LOAD_FAST                'conn'
               80  LOAD_METHOD              close
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          
             86_0  COME_FROM            76  '76'

Parse error at or near `RETURN_VALUE' instruction at offset 22

    def _validate_conn(self, conn):
        """
        Called right before a request is made, after the socket is created.
        """
        pass

    def _prepare_proxy(self, conn):
        pass

    def _get_timeout--- This code section failed: ---

 L. 292         0  LOAD_FAST                'timeout'
                2  LOAD_GLOBAL              _Default
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 293         8  LOAD_FAST                'self'
               10  LOAD_ATTR                timeout
               12  LOAD_METHOD              clone
               14  CALL_METHOD_0         0  ''
               16  RETURN_VALUE     
             18_0  COME_FROM             6  '6'

 L. 295        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'timeout'
               22  LOAD_GLOBAL              Timeout
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 296        28  LOAD_FAST                'timeout'
               30  LOAD_METHOD              clone
               32  CALL_METHOD_0         0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM            26  '26'

 L. 300        36  LOAD_GLOBAL              Timeout
               38  LOAD_METHOD              from_float
               40  LOAD_FAST                'timeout'
               42  CALL_METHOD_1         1  ''
               44  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def _raise_timeout--- This code section failed: ---

 L. 305         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'err'
                4  LOAD_GLOBAL              SocketTimeout
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 306        10  LOAD_GLOBAL              ReadTimeoutError
               12  LOAD_FAST                'self'
               14  LOAD_FAST                'url'
               16  LOAD_STR                 'Read timed out. (read timeout=%s)'
               18  LOAD_FAST                'timeout_value'
               20  BINARY_MODULO    
               22  CALL_FUNCTION_3       3  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 310        26  LOAD_GLOBAL              hasattr
               28  LOAD_FAST                'err'
               30  LOAD_STR                 'errno'
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE    62  'to 62'
               36  LOAD_FAST                'err'
               38  LOAD_ATTR                errno
               40  LOAD_GLOBAL              _blocking_errnos
               42  <118>                 0  ''
               44  POP_JUMP_IF_FALSE    62  'to 62'

 L. 311        46  LOAD_GLOBAL              ReadTimeoutError
               48  LOAD_FAST                'self'
               50  LOAD_FAST                'url'
               52  LOAD_STR                 'Read timed out. (read timeout=%s)'
               54  LOAD_FAST                'timeout_value'
               56  BINARY_MODULO    
               58  CALL_FUNCTION_3       3  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            44  '44'
             62_1  COME_FROM            34  '34'

 L. 316        62  LOAD_STR                 'timed out'
               64  LOAD_GLOBAL              str
               66  LOAD_FAST                'err'
               68  CALL_FUNCTION_1       1  ''
               70  <118>                 0  ''
               72  POP_JUMP_IF_TRUE     86  'to 86'
               74  LOAD_STR                 'did not complete (read)'
               76  LOAD_GLOBAL              str
               78  LOAD_FAST                'err'
               80  CALL_FUNCTION_1       1  ''
               82  <118>                 0  ''
               84  POP_JUMP_IF_FALSE   102  'to 102'
             86_0  COME_FROM            72  '72'

 L. 317        86  LOAD_GLOBAL              ReadTimeoutError
               88  LOAD_FAST                'self'
               90  LOAD_FAST                'url'
               92  LOAD_STR                 'Read timed out. (read timeout=%s)'
               94  LOAD_FAST                'timeout_value'
               96  BINARY_MODULO    
               98  CALL_FUNCTION_3       3  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            84  '84'

Parse error at or near `<118>' instruction at offset 42

    def _make_request--- This code section failed: ---

 L. 335         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                num_requests
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               num_requests

 L. 337        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _get_timeout
               18  LOAD_FAST                'timeout'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'timeout_obj'

 L. 338        24  LOAD_FAST                'timeout_obj'
               26  LOAD_METHOD              start_connect
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          

 L. 339        32  LOAD_FAST                'timeout_obj'
               34  LOAD_ATTR                connect_timeout
               36  LOAD_FAST                'conn'
               38  STORE_ATTR               timeout

 L. 342        40  SETUP_FINALLY        56  'to 56'

 L. 343        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _validate_conn
               46  LOAD_FAST                'conn'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
               52  POP_BLOCK        
               54  JUMP_FORWARD        116  'to 116'
             56_0  COME_FROM_FINALLY    40  '40'

 L. 344        56  DUP_TOP          
               58  LOAD_GLOBAL              SocketTimeout
               60  LOAD_GLOBAL              BaseSSLError
               62  BUILD_TUPLE_2         2 
               64  <121>               114  ''
               66  POP_TOP          
               68  STORE_FAST               'e'
               70  POP_TOP          
               72  SETUP_FINALLY       106  'to 106'

 L. 346        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _raise_timeout
               78  LOAD_FAST                'e'
               80  LOAD_FAST                'url'
               82  LOAD_FAST                'conn'
               84  LOAD_ATTR                timeout
               86  LOAD_CONST               ('err', 'url', 'timeout_value')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  POP_TOP          

 L. 347        92  RAISE_VARARGS_0       0  'reraise'
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

 L. 351       116  LOAD_FAST                'chunked'
              118  POP_JUMP_IF_FALSE   142  'to 142'

 L. 352       120  LOAD_FAST                'conn'
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

 L. 354       142  LOAD_FAST                'conn'
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

 L. 357       162  LOAD_FAST                'timeout_obj'
              164  LOAD_ATTR                read_timeout
              166  STORE_FAST               'read_timeout'

 L. 360       168  LOAD_GLOBAL              getattr
              170  LOAD_FAST                'conn'
              172  LOAD_STR                 'sock'
              174  LOAD_CONST               None
              176  CALL_FUNCTION_3       3  ''
              178  POP_JUMP_IF_FALSE   244  'to 244'

 L. 366       180  LOAD_FAST                'read_timeout'
              182  LOAD_CONST               0
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   204  'to 204'

 L. 367       188  LOAD_GLOBAL              ReadTimeoutError

 L. 368       190  LOAD_FAST                'self'
              192  LOAD_FAST                'url'
              194  LOAD_STR                 'Read timed out. (read timeout=%s)'
              196  LOAD_FAST                'read_timeout'
              198  BINARY_MODULO    

 L. 367       200  CALL_FUNCTION_3       3  ''
              202  RAISE_VARARGS_1       1  'exception instance'
            204_0  COME_FROM           186  '186'

 L. 369       204  LOAD_FAST                'read_timeout'
              206  LOAD_GLOBAL              Timeout
              208  LOAD_ATTR                DEFAULT_TIMEOUT
              210  <117>                 0  ''
              212  POP_JUMP_IF_FALSE   232  'to 232'

 L. 370       214  LOAD_FAST                'conn'
              216  LOAD_ATTR                sock
              218  LOAD_METHOD              settimeout
              220  LOAD_GLOBAL              socket
              222  LOAD_METHOD              getdefaulttimeout
              224  CALL_METHOD_0         0  ''
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          
              230  JUMP_FORWARD        244  'to 244'
            232_0  COME_FROM           212  '212'

 L. 372       232  LOAD_FAST                'conn'
              234  LOAD_ATTR                sock
              236  LOAD_METHOD              settimeout
              238  LOAD_FAST                'read_timeout'
              240  CALL_METHOD_1         1  ''
              242  POP_TOP          
            244_0  COME_FROM           230  '230'
            244_1  COME_FROM           178  '178'

 L. 375       244  SETUP_FINALLY       352  'to 352'

 L. 376       246  SETUP_FINALLY       264  'to 264'

 L. 377       248  LOAD_FAST                'conn'
              250  LOAD_ATTR                getresponse
              252  LOAD_CONST               True
              254  LOAD_CONST               ('buffering',)
              256  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              258  STORE_FAST               'httplib_response'
              260  POP_BLOCK        
              262  JUMP_FORWARD        348  'to 348'
            264_0  COME_FROM_FINALLY   246  '246'

 L. 378       264  DUP_TOP          
              266  LOAD_GLOBAL              TypeError
          268_270  <121>               346  ''
              272  POP_TOP          
              274  POP_TOP          
              276  POP_TOP          

 L. 379       278  SETUP_FINALLY       292  'to 292'

 L. 380       280  LOAD_FAST                'conn'
              282  LOAD_METHOD              getresponse
              284  CALL_METHOD_0         0  ''
              286  STORE_FAST               'httplib_response'
              288  POP_BLOCK        
              290  JUMP_FORWARD        342  'to 342'
            292_0  COME_FROM_FINALLY   278  '278'

 L. 381       292  DUP_TOP          
              294  LOAD_GLOBAL              Exception
          296_298  <121>               340  ''
              300  POP_TOP          
              302  STORE_FAST               'e'
              304  POP_TOP          
              306  SETUP_FINALLY       332  'to 332'

 L. 384       308  LOAD_GLOBAL              six
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

 L. 385       352  DUP_TOP          
              354  LOAD_GLOBAL              SocketTimeout
              356  LOAD_GLOBAL              BaseSSLError
              358  LOAD_GLOBAL              SocketError
              360  BUILD_TUPLE_3         3 
          362_364  <121>               412  ''
              366  POP_TOP          
              368  STORE_FAST               'e'
              370  POP_TOP          
              372  SETUP_FINALLY       404  'to 404'

 L. 386       374  LOAD_FAST                'self'
              376  LOAD_ATTR                _raise_timeout
              378  LOAD_FAST                'e'
              380  LOAD_FAST                'url'
              382  LOAD_FAST                'read_timeout'
              384  LOAD_CONST               ('err', 'url', 'timeout_value')
              386  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              388  POP_TOP          

 L. 387       390  RAISE_VARARGS_0       0  'reraise'
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

 L. 390       414  LOAD_GLOBAL              getattr
              416  LOAD_FAST                'conn'
              418  LOAD_STR                 '_http_vsn_str'
              420  LOAD_STR                 'HTTP/?'
              422  CALL_FUNCTION_3       3  ''
              424  STORE_FAST               'http_version'

 L. 391       426  LOAD_GLOBAL              log
              428  LOAD_METHOD              debug
              430  LOAD_STR                 '%s://%s:%s "%s %s %s" %s %s'
              432  LOAD_FAST                'self'
              434  LOAD_ATTR                scheme
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                host
              440  LOAD_FAST                'self'
              442  LOAD_ATTR                port

 L. 392       444  LOAD_FAST                'method'
              446  LOAD_FAST                'url'
              448  LOAD_FAST                'http_version'
              450  LOAD_FAST                'httplib_response'
              452  LOAD_ATTR                status

 L. 393       454  LOAD_FAST                'httplib_response'
              456  LOAD_ATTR                length

 L. 391       458  CALL_METHOD_9         9  ''
              460  POP_TOP          

 L. 395       462  SETUP_FINALLY       478  'to 478'

 L. 396       464  LOAD_GLOBAL              assert_header_parsing
              466  LOAD_FAST                'httplib_response'
              468  LOAD_ATTR                msg
              470  CALL_FUNCTION_1       1  ''
              472  POP_TOP          
              474  POP_BLOCK        
              476  JUMP_FORWARD        544  'to 544'
            478_0  COME_FROM_FINALLY   462  '462'

 L. 397       478  DUP_TOP          
              480  LOAD_GLOBAL              HeaderParsingError
              482  LOAD_GLOBAL              TypeError
              484  BUILD_TUPLE_2         2 
          486_488  <121>               542  ''
              490  POP_TOP          
              492  STORE_FAST               'hpe'
              494  POP_TOP          
              496  SETUP_FINALLY       534  'to 534'

 L. 398       498  LOAD_GLOBAL              log
              500  LOAD_ATTR                warning

 L. 399       502  LOAD_STR                 'Failed to parse headers (url=%s): %s'

 L. 400       504  LOAD_FAST                'self'
              506  LOAD_METHOD              _absolute_url
              508  LOAD_FAST                'url'
              510  CALL_METHOD_1         1  ''
              512  LOAD_FAST                'hpe'
              514  LOAD_CONST               True

 L. 398       516  LOAD_CONST               ('exc_info',)
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

 L. 402       544  LOAD_FAST                'httplib_response'
              546  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 64

    def _absolute_url(self, path):
        return Url(scheme=(self.scheme), host=(self.host), port=(self.port), path=path).url

    def close--- This code section failed: ---

 L. 411         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pool
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 412        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 414        14  LOAD_FAST                'self'
               16  LOAD_ATTR                pool
               18  LOAD_CONST               None
               20  ROT_TWO          
               22  STORE_FAST               'old_pool'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               pool

 L. 416        28  SETUP_FINALLY        60  'to 60'
             30_0  COME_FROM            44  '44'

 L. 418        30  LOAD_FAST                'old_pool'
               32  LOAD_ATTR                get
               34  LOAD_CONST               False
               36  LOAD_CONST               ('block',)
               38  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               40  STORE_FAST               'conn'

 L. 419        42  LOAD_FAST                'conn'
               44  POP_JUMP_IF_FALSE    30  'to 30'

 L. 420        46  LOAD_FAST                'conn'
               48  LOAD_METHOD              close
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          
               54  JUMP_BACK            30  'to 30'
               56  POP_BLOCK        
               58  JUMP_FORWARD         80  'to 80'
             60_0  COME_FROM_FINALLY    28  '28'

 L. 422        60  DUP_TOP          
               62  LOAD_GLOBAL              queue
               64  LOAD_ATTR                Empty
               66  <121>                78  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 423        74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
               78  <48>             
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            58  '58'

Parse error at or near `None' instruction at offset -1

    def is_same_host(self, url):
        """
        Check if the given ``url`` is a member of the same host as this
        connection pool.
        """
        if url.startswith('/'):
            return True
        scheme, host, port = get_host(url)
        host = _ipv6_host(host, self.scheme)
        if self.port:
            port = port or port_by_scheme.get(scheme)
        else:
            if not self.port:
                if port == port_by_scheme.get(scheme):
                    port = None
        return (
         scheme, host, port) == (self.scheme, self.host, self.port)

    def urlopen--- This code section failed: ---

 L. 540         0  LOAD_FAST                'headers'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 541         8  LOAD_FAST                'self'
               10  LOAD_ATTR                headers
               12  STORE_FAST               'headers'
             14_0  COME_FROM             6  '6'

 L. 543        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'retries'
               18  LOAD_GLOBAL              Retry
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     42  'to 42'

 L. 544        24  LOAD_GLOBAL              Retry
               26  LOAD_ATTR                from_int
               28  LOAD_FAST                'retries'
               30  LOAD_FAST                'redirect'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                retries
               36  LOAD_CONST               ('redirect', 'default')
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  STORE_FAST               'retries'
             42_0  COME_FROM            22  '22'

 L. 546        42  LOAD_FAST                'release_conn'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L. 547        50  LOAD_FAST                'response_kw'
               52  LOAD_METHOD              get
               54  LOAD_STR                 'preload_content'
               56  LOAD_CONST               True
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'release_conn'
             62_0  COME_FROM            48  '48'

 L. 550        62  LOAD_FAST                'assert_same_host'
               64  POP_JUMP_IF_FALSE    88  'to 88'
               66  LOAD_FAST                'self'
               68  LOAD_METHOD              is_same_host
               70  LOAD_FAST                'url'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_TRUE     88  'to 88'

 L. 551        76  LOAD_GLOBAL              HostChangedError
               78  LOAD_FAST                'self'
               80  LOAD_FAST                'url'
               82  LOAD_FAST                'retries'
               84  CALL_FUNCTION_3       3  ''
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            74  '74'
             88_1  COME_FROM            64  '64'

 L. 553        88  LOAD_CONST               None
               90  STORE_FAST               'conn'

 L. 564        92  LOAD_FAST                'release_conn'
               94  STORE_FAST               'release_this_conn'

 L. 569        96  LOAD_FAST                'self'
               98  LOAD_ATTR                scheme
              100  LOAD_STR                 'http'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   126  'to 126'

 L. 570       106  LOAD_FAST                'headers'
              108  LOAD_METHOD              copy
              110  CALL_METHOD_0         0  ''
              112  STORE_FAST               'headers'

 L. 571       114  LOAD_FAST                'headers'
              116  LOAD_METHOD              update
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                proxy_headers
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
            126_0  COME_FROM           104  '104'

 L. 575       126  LOAD_CONST               None
              128  STORE_FAST               'err'

 L. 579       130  LOAD_CONST               False
              132  STORE_FAST               'clean_exit'

 L. 583       134  LOAD_GLOBAL              set_file_position
              136  LOAD_FAST                'body'
              138  LOAD_FAST                'body_pos'
              140  CALL_FUNCTION_2       2  ''
              142  STORE_FAST               'body_pos'

 L. 585   144_146  SETUP_FINALLY       556  'to 556'
              148  SETUP_FINALLY       298  'to 298'

 L. 587       150  LOAD_FAST                'self'
              152  LOAD_METHOD              _get_timeout
              154  LOAD_FAST                'timeout'
              156  CALL_METHOD_1         1  ''
              158  STORE_FAST               'timeout_obj'

 L. 588       160  LOAD_FAST                'self'
              162  LOAD_ATTR                _get_conn
              164  LOAD_FAST                'pool_timeout'
              166  LOAD_CONST               ('timeout',)
              168  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              170  STORE_FAST               'conn'

 L. 590       172  LOAD_FAST                'timeout_obj'
              174  LOAD_ATTR                connect_timeout
              176  LOAD_FAST                'conn'
              178  STORE_ATTR               timeout

 L. 592       180  LOAD_FAST                'self'
              182  LOAD_ATTR                proxy
              184  LOAD_CONST               None
              186  <117>                 1  ''
              188  JUMP_IF_FALSE_OR_POP   202  'to 202'
              190  LOAD_GLOBAL              getattr
              192  LOAD_FAST                'conn'
              194  LOAD_STR                 'sock'
              196  LOAD_CONST               None
              198  CALL_FUNCTION_3       3  ''
              200  UNARY_NOT        
            202_0  COME_FROM           188  '188'
              202  STORE_FAST               'is_new_proxy_conn'

 L. 593       204  LOAD_FAST                'is_new_proxy_conn'
              206  POP_JUMP_IF_FALSE   218  'to 218'

 L. 594       208  LOAD_FAST                'self'
              210  LOAD_METHOD              _prepare_proxy
              212  LOAD_FAST                'conn'
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
            218_0  COME_FROM           206  '206'

 L. 597       218  LOAD_FAST                'self'
              220  LOAD_ATTR                _make_request
              222  LOAD_FAST                'conn'
              224  LOAD_FAST                'method'
              226  LOAD_FAST                'url'

 L. 598       228  LOAD_FAST                'timeout_obj'

 L. 599       230  LOAD_FAST                'body'
              232  LOAD_FAST                'headers'

 L. 600       234  LOAD_FAST                'chunked'

 L. 597       236  LOAD_CONST               ('timeout', 'body', 'headers', 'chunked')
              238  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              240  STORE_FAST               'httplib_response'

 L. 606       242  LOAD_FAST                'release_conn'
              244  POP_JUMP_IF_TRUE    250  'to 250'
              246  LOAD_FAST                'conn'
              248  JUMP_FORWARD        252  'to 252'
            250_0  COME_FROM           244  '244'
              250  LOAD_CONST               None
            252_0  COME_FROM           248  '248'
              252  STORE_FAST               'response_conn'

 L. 609       254  LOAD_FAST                'method'
              256  LOAD_FAST                'response_kw'
              258  LOAD_STR                 'request_method'
              260  STORE_SUBSCR     

 L. 612       262  LOAD_FAST                'self'
              264  LOAD_ATTR                ResponseCls
              266  LOAD_ATTR                from_httplib
              268  LOAD_FAST                'httplib_response'
              270  BUILD_TUPLE_1         1 

 L. 613       272  LOAD_FAST                'self'

 L. 614       274  LOAD_FAST                'response_conn'

 L. 615       276  LOAD_FAST                'retries'

 L. 612       278  LOAD_CONST               ('pool', 'connection', 'retries')
              280  BUILD_CONST_KEY_MAP_3     3 

 L. 616       282  LOAD_FAST                'response_kw'

 L. 612       284  <164>                 1  ''
              286  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              288  STORE_FAST               'response'

 L. 619       290  LOAD_CONST               True
              292  STORE_FAST               'clean_exit'
              294  POP_BLOCK        
              296  JUMP_FORWARD        512  'to 512'
            298_0  COME_FROM_FINALLY   148  '148'

 L. 621       298  DUP_TOP          
              300  LOAD_GLOBAL              queue
              302  LOAD_ATTR                Empty
          304_306  <121>               328  ''
              308  POP_TOP          
              310  POP_TOP          
              312  POP_TOP          

 L. 623       314  LOAD_GLOBAL              EmptyPoolError
              316  LOAD_FAST                'self'
              318  LOAD_STR                 'No pool connections are available.'
              320  CALL_FUNCTION_2       2  ''
              322  RAISE_VARARGS_1       1  'exception instance'
              324  POP_EXCEPT       
              326  JUMP_FORWARD        512  'to 512'

 L. 625       328  DUP_TOP          
              330  LOAD_GLOBAL              TimeoutError
              332  LOAD_GLOBAL              HTTPException
              334  LOAD_GLOBAL              SocketError
              336  LOAD_GLOBAL              ProtocolError

 L. 626       338  LOAD_GLOBAL              BaseSSLError
              340  LOAD_GLOBAL              SSLError
              342  LOAD_GLOBAL              CertificateError

 L. 625       344  BUILD_TUPLE_7         7 
          346_348  <121>               510  ''
              350  POP_TOP          
              352  STORE_FAST               'e'
              354  POP_TOP          
              356  SETUP_FINALLY       502  'to 502'

 L. 629       358  LOAD_CONST               False
              360  STORE_FAST               'clean_exit'

 L. 630       362  LOAD_GLOBAL              isinstance
              364  LOAD_FAST                'e'
              366  LOAD_GLOBAL              BaseSSLError
              368  LOAD_GLOBAL              CertificateError
              370  BUILD_TUPLE_2         2 
              372  CALL_FUNCTION_2       2  ''
          374_376  POP_JUMP_IF_FALSE   388  'to 388'

 L. 631       378  LOAD_GLOBAL              SSLError
              380  LOAD_FAST                'e'
              382  CALL_FUNCTION_1       1  ''
              384  STORE_FAST               'e'
              386  JUMP_FORWARD        450  'to 450'
            388_0  COME_FROM           374  '374'

 L. 632       388  LOAD_GLOBAL              isinstance
              390  LOAD_FAST                'e'
              392  LOAD_GLOBAL              SocketError
              394  LOAD_GLOBAL              NewConnectionError
              396  BUILD_TUPLE_2         2 
              398  CALL_FUNCTION_2       2  ''
          400_402  POP_JUMP_IF_FALSE   424  'to 424'
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                proxy
          408_410  POP_JUMP_IF_FALSE   424  'to 424'

 L. 633       412  LOAD_GLOBAL              ProxyError
              414  LOAD_STR                 'Cannot connect to proxy.'
              416  LOAD_FAST                'e'
              418  CALL_FUNCTION_2       2  ''
              420  STORE_FAST               'e'
              422  JUMP_FORWARD        450  'to 450'
            424_0  COME_FROM           408  '408'
            424_1  COME_FROM           400  '400'

 L. 634       424  LOAD_GLOBAL              isinstance
              426  LOAD_FAST                'e'
              428  LOAD_GLOBAL              SocketError
              430  LOAD_GLOBAL              HTTPException
              432  BUILD_TUPLE_2         2 
              434  CALL_FUNCTION_2       2  ''
          436_438  POP_JUMP_IF_FALSE   450  'to 450'

 L. 635       440  LOAD_GLOBAL              ProtocolError
              442  LOAD_STR                 'Connection aborted.'
              444  LOAD_FAST                'e'
              446  CALL_FUNCTION_2       2  ''
              448  STORE_FAST               'e'
            450_0  COME_FROM           436  '436'
            450_1  COME_FROM           422  '422'
            450_2  COME_FROM           386  '386'

 L. 637       450  LOAD_FAST                'retries'
              452  LOAD_ATTR                increment
              454  LOAD_FAST                'method'
              456  LOAD_FAST                'url'
              458  LOAD_FAST                'e'
              460  LOAD_FAST                'self'

 L. 638       462  LOAD_GLOBAL              sys
              464  LOAD_METHOD              exc_info
              466  CALL_METHOD_0         0  ''
              468  LOAD_CONST               2
              470  BINARY_SUBSCR    

 L. 637       472  LOAD_CONST               ('error', '_pool', '_stacktrace')
              474  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              476  STORE_FAST               'retries'

 L. 639       478  LOAD_FAST                'retries'
              480  LOAD_METHOD              sleep
              482  CALL_METHOD_0         0  ''
              484  POP_TOP          

 L. 642       486  LOAD_FAST                'e'
              488  STORE_FAST               'err'
              490  POP_BLOCK        
              492  POP_EXCEPT       
              494  LOAD_CONST               None
              496  STORE_FAST               'e'
              498  DELETE_FAST              'e'
              500  JUMP_FORWARD        512  'to 512'
            502_0  COME_FROM_FINALLY   356  '356'
              502  LOAD_CONST               None
              504  STORE_FAST               'e'
              506  DELETE_FAST              'e'
              508  <48>             
              510  <48>             
            512_0  COME_FROM           500  '500'
            512_1  COME_FROM           326  '326'
            512_2  COME_FROM           296  '296'
              512  POP_BLOCK        

 L. 645       514  LOAD_FAST                'clean_exit'
          516_518  POP_JUMP_IF_TRUE    538  'to 538'

 L. 650       520  LOAD_FAST                'conn'
          522_524  JUMP_IF_FALSE_OR_POP   532  'to 532'
              526  LOAD_FAST                'conn'
              528  LOAD_METHOD              close
              530  CALL_METHOD_0         0  ''
            532_0  COME_FROM           522  '522'
              532  STORE_FAST               'conn'

 L. 651       534  LOAD_CONST               True
              536  STORE_FAST               'release_this_conn'
            538_0  COME_FROM           516  '516'

 L. 653       538  LOAD_FAST                'release_this_conn'
          540_542  POP_JUMP_IF_FALSE   598  'to 598'

 L. 657       544  LOAD_FAST                'self'
              546  LOAD_METHOD              _put_conn
              548  LOAD_FAST                'conn'
              550  CALL_METHOD_1         1  ''
              552  POP_TOP          
              554  JUMP_FORWARD        598  'to 598'
            556_0  COME_FROM_FINALLY   144  '144'

 L. 645       556  LOAD_FAST                'clean_exit'
          558_560  POP_JUMP_IF_TRUE    580  'to 580'

 L. 650       562  LOAD_FAST                'conn'
          564_566  JUMP_IF_FALSE_OR_POP   574  'to 574'
              568  LOAD_FAST                'conn'
              570  LOAD_METHOD              close
              572  CALL_METHOD_0         0  ''
            574_0  COME_FROM           564  '564'
              574  STORE_FAST               'conn'

 L. 651       576  LOAD_CONST               True
              578  STORE_FAST               'release_this_conn'
            580_0  COME_FROM           558  '558'

 L. 653       580  LOAD_FAST                'release_this_conn'
          582_584  POP_JUMP_IF_FALSE   596  'to 596'

 L. 657       586  LOAD_FAST                'self'
              588  LOAD_METHOD              _put_conn
              590  LOAD_FAST                'conn'
              592  CALL_METHOD_1         1  ''
              594  POP_TOP          
            596_0  COME_FROM           582  '582'
              596  <48>             
            598_0  COME_FROM           554  '554'
            598_1  COME_FROM           540  '540'

 L. 659       598  LOAD_FAST                'conn'
          600_602  POP_JUMP_IF_TRUE    660  'to 660'

 L. 661       604  LOAD_GLOBAL              log
              606  LOAD_METHOD              warning
              608  LOAD_STR                 "Retrying (%r) after connection broken by '%r': %s"

 L. 662       610  LOAD_FAST                'retries'
              612  LOAD_FAST                'err'
              614  LOAD_FAST                'url'

 L. 661       616  CALL_METHOD_4         4  ''
              618  POP_TOP          

 L. 663       620  LOAD_FAST                'self'
              622  LOAD_ATTR                urlopen
              624  LOAD_FAST                'method'
              626  LOAD_FAST                'url'
              628  LOAD_FAST                'body'
              630  LOAD_FAST                'headers'
              632  LOAD_FAST                'retries'

 L. 664       634  LOAD_FAST                'redirect'
              636  LOAD_FAST                'assert_same_host'

 L. 663       638  BUILD_TUPLE_7         7 

 L. 665       640  LOAD_FAST                'timeout'
              642  LOAD_FAST                'pool_timeout'

 L. 666       644  LOAD_FAST                'release_conn'
              646  LOAD_FAST                'body_pos'

 L. 663       648  LOAD_CONST               ('timeout', 'pool_timeout', 'release_conn', 'body_pos')
              650  BUILD_CONST_KEY_MAP_4     4 

 L. 667       652  LOAD_FAST                'response_kw'

 L. 663       654  <164>                 1  ''
              656  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              658  RETURN_VALUE     
            660_0  COME_FROM           600  '600'

 L. 669       660  LOAD_CODE                <code_object drain_and_release_conn>
              662  LOAD_STR                 'HTTPConnectionPool.urlopen.<locals>.drain_and_release_conn'
              664  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              666  STORE_FAST               'drain_and_release_conn'

 L. 679       668  LOAD_FAST                'redirect'
          670_672  JUMP_IF_FALSE_OR_POP   680  'to 680'
              674  LOAD_FAST                'response'
              676  LOAD_METHOD              get_redirect_location
              678  CALL_METHOD_0         0  ''
            680_0  COME_FROM           670  '670'
              680  STORE_FAST               'redirect_location'

 L. 680       682  LOAD_FAST                'redirect_location'
          684_686  POP_JUMP_IF_FALSE   842  'to 842'

 L. 681       688  LOAD_FAST                'response'
              690  LOAD_ATTR                status
              692  LOAD_CONST               303
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   704  'to 704'

 L. 682       700  LOAD_STR                 'GET'
              702  STORE_FAST               'method'
            704_0  COME_FROM           696  '696'

 L. 684       704  SETUP_FINALLY       728  'to 728'

 L. 685       706  LOAD_FAST                'retries'
              708  LOAD_ATTR                increment
              710  LOAD_FAST                'method'
              712  LOAD_FAST                'url'
              714  LOAD_FAST                'response'
              716  LOAD_FAST                'self'
              718  LOAD_CONST               ('response', '_pool')
              720  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              722  STORE_FAST               'retries'
              724  POP_BLOCK        
              726  JUMP_FORWARD        770  'to 770'
            728_0  COME_FROM_FINALLY   704  '704'

 L. 686       728  DUP_TOP          
              730  LOAD_GLOBAL              MaxRetryError
          732_734  <121>               768  ''
              736  POP_TOP          
              738  POP_TOP          
              740  POP_TOP          

 L. 687       742  LOAD_FAST                'retries'
              744  LOAD_ATTR                raise_on_redirect
          746_748  POP_JUMP_IF_FALSE   760  'to 760'

 L. 690       750  LOAD_FAST                'drain_and_release_conn'
              752  LOAD_FAST                'response'
              754  CALL_FUNCTION_1       1  ''
              756  POP_TOP          

 L. 691       758  RAISE_VARARGS_0       0  'reraise'
            760_0  COME_FROM           746  '746'

 L. 692       760  LOAD_FAST                'response'
              762  ROT_FOUR         
              764  POP_EXCEPT       
              766  RETURN_VALUE     
              768  <48>             
            770_0  COME_FROM           726  '726'

 L. 695       770  LOAD_FAST                'drain_and_release_conn'
              772  LOAD_FAST                'response'
              774  CALL_FUNCTION_1       1  ''
              776  POP_TOP          

 L. 697       778  LOAD_FAST                'retries'
              780  LOAD_METHOD              sleep_for_retry
              782  LOAD_FAST                'response'
              784  CALL_METHOD_1         1  ''
              786  POP_TOP          

 L. 698       788  LOAD_GLOBAL              log
              790  LOAD_METHOD              debug
              792  LOAD_STR                 'Redirecting %s -> %s'
              794  LOAD_FAST                'url'
              796  LOAD_FAST                'redirect_location'
              798  CALL_METHOD_3         3  ''
              800  POP_TOP          

 L. 699       802  LOAD_FAST                'self'
              804  LOAD_ATTR                urlopen

 L. 700       806  LOAD_FAST                'method'
              808  LOAD_FAST                'redirect_location'
              810  LOAD_FAST                'body'
              812  LOAD_FAST                'headers'

 L. 699       814  BUILD_TUPLE_4         4 

 L. 701       816  LOAD_FAST                'retries'
              818  LOAD_FAST                'redirect'

 L. 702       820  LOAD_FAST                'assert_same_host'

 L. 703       822  LOAD_FAST                'timeout'
              824  LOAD_FAST                'pool_timeout'

 L. 704       826  LOAD_FAST                'release_conn'
              828  LOAD_FAST                'body_pos'

 L. 699       830  LOAD_CONST               ('retries', 'redirect', 'assert_same_host', 'timeout', 'pool_timeout', 'release_conn', 'body_pos')
              832  BUILD_CONST_KEY_MAP_7     7 

 L. 705       834  LOAD_FAST                'response_kw'

 L. 699       836  <164>                 1  ''
              838  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              840  RETURN_VALUE     
            842_0  COME_FROM           684  '684'

 L. 708       842  LOAD_GLOBAL              bool
              844  LOAD_FAST                'response'
              846  LOAD_METHOD              getheader
              848  LOAD_STR                 'Retry-After'
              850  CALL_METHOD_1         1  ''
              852  CALL_FUNCTION_1       1  ''
              854  STORE_FAST               'has_retry_after'

 L. 709       856  LOAD_FAST                'retries'
              858  LOAD_METHOD              is_retry
              860  LOAD_FAST                'method'
              862  LOAD_FAST                'response'
              864  LOAD_ATTR                status
              866  LOAD_FAST                'has_retry_after'
              868  CALL_METHOD_3         3  ''
          870_872  POP_JUMP_IF_FALSE  1010  'to 1010'

 L. 710       874  SETUP_FINALLY       898  'to 898'

 L. 711       876  LOAD_FAST                'retries'
              878  LOAD_ATTR                increment
              880  LOAD_FAST                'method'
              882  LOAD_FAST                'url'
              884  LOAD_FAST                'response'
              886  LOAD_FAST                'self'
              888  LOAD_CONST               ('response', '_pool')
              890  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              892  STORE_FAST               'retries'
              894  POP_BLOCK        
              896  JUMP_FORWARD        940  'to 940'
            898_0  COME_FROM_FINALLY   874  '874'

 L. 712       898  DUP_TOP          
              900  LOAD_GLOBAL              MaxRetryError
          902_904  <121>               938  ''
              906  POP_TOP          
              908  POP_TOP          
              910  POP_TOP          

 L. 713       912  LOAD_FAST                'retries'
              914  LOAD_ATTR                raise_on_status
          916_918  POP_JUMP_IF_FALSE   930  'to 930'

 L. 716       920  LOAD_FAST                'drain_and_release_conn'
              922  LOAD_FAST                'response'
              924  CALL_FUNCTION_1       1  ''
              926  POP_TOP          

 L. 717       928  RAISE_VARARGS_0       0  'reraise'
            930_0  COME_FROM           916  '916'

 L. 718       930  LOAD_FAST                'response'
              932  ROT_FOUR         
              934  POP_EXCEPT       
              936  RETURN_VALUE     
              938  <48>             
            940_0  COME_FROM           896  '896'

 L. 721       940  LOAD_FAST                'drain_and_release_conn'
              942  LOAD_FAST                'response'
              944  CALL_FUNCTION_1       1  ''
              946  POP_TOP          

 L. 723       948  LOAD_FAST                'retries'
              950  LOAD_METHOD              sleep
              952  LOAD_FAST                'response'
              954  CALL_METHOD_1         1  ''
              956  POP_TOP          

 L. 724       958  LOAD_GLOBAL              log
              960  LOAD_METHOD              debug
              962  LOAD_STR                 'Retry: %s'
              964  LOAD_FAST                'url'
              966  CALL_METHOD_2         2  ''
              968  POP_TOP          

 L. 725       970  LOAD_FAST                'self'
              972  LOAD_ATTR                urlopen

 L. 726       974  LOAD_FAST                'method'
              976  LOAD_FAST                'url'
              978  LOAD_FAST                'body'
              980  LOAD_FAST                'headers'

 L. 725       982  BUILD_TUPLE_4         4 

 L. 727       984  LOAD_FAST                'retries'
              986  LOAD_FAST                'redirect'

 L. 728       988  LOAD_FAST                'assert_same_host'

 L. 729       990  LOAD_FAST                'timeout'
              992  LOAD_FAST                'pool_timeout'

 L. 730       994  LOAD_FAST                'release_conn'

 L. 731       996  LOAD_FAST                'body_pos'

 L. 725       998  LOAD_CONST               ('retries', 'redirect', 'assert_same_host', 'timeout', 'pool_timeout', 'release_conn', 'body_pos')
             1000  BUILD_CONST_KEY_MAP_7     7 

 L. 731      1002  LOAD_FAST                'response_kw'

 L. 725      1004  <164>                 1  ''
             1006  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1008  RETURN_VALUE     
           1010_0  COME_FROM           870  '870'

 L. 733      1010  LOAD_FAST                'response'
             1012  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class HTTPSConnectionPool(HTTPConnectionPool):
    __doc__ = '\n    Same as :class:`.HTTPConnectionPool`, but HTTPS.\n\n    When Python is compiled with the :mod:`ssl` module, then\n    :class:`.VerifiedHTTPSConnection` is used, which *can* verify certificates,\n    instead of :class:`.HTTPSConnection`.\n\n    :class:`.VerifiedHTTPSConnection` uses one of ``assert_fingerprint``,\n    ``assert_hostname`` and ``host`` in this order to verify connections.\n    If ``assert_hostname`` is False, no verification is done.\n\n    The ``key_file``, ``cert_file``, ``cert_reqs``, ``ca_certs``,\n    ``ca_cert_dir``, and ``ssl_version`` are only used if :mod:`ssl` is\n    available and are fed into :meth:`urllib3.util.ssl_wrap_socket` to upgrade\n    the connection socket into an SSL socket.\n    '
    scheme = 'https'
    ConnectionCls = HTTPSConnection

    def __init__--- This code section failed: ---

 L. 766         0  LOAD_GLOBAL              HTTPConnectionPool
                2  LOAD_ATTR                __init__
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'host'
                8  LOAD_FAST                'port'
               10  LOAD_FAST                'strict'
               12  LOAD_FAST                'timeout'
               14  LOAD_FAST                'maxsize'

 L. 767        16  LOAD_FAST                'block'
               18  LOAD_FAST                'headers'
               20  LOAD_FAST                'retries'
               22  LOAD_FAST                '_proxy'
               24  LOAD_FAST                '_proxy_headers'

 L. 766        26  BUILD_TUPLE_11       11 
               28  BUILD_MAP_0           0 

 L. 768        30  LOAD_FAST                'conn_kw'

 L. 766        32  <164>                 1  ''
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  POP_TOP          

 L. 770        38  LOAD_FAST                'ca_certs'
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  LOAD_FAST                'cert_reqs'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 771        50  LOAD_STR                 'CERT_REQUIRED'
               52  STORE_FAST               'cert_reqs'
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM            40  '40'

 L. 773        54  LOAD_FAST                'key_file'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               key_file

 L. 774        60  LOAD_FAST                'cert_file'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               cert_file

 L. 775        66  LOAD_FAST                'cert_reqs'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               cert_reqs

 L. 776        72  LOAD_FAST                'ca_certs'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               ca_certs

 L. 777        78  LOAD_FAST                'ca_cert_dir'
               80  LOAD_FAST                'self'
               82  STORE_ATTR               ca_cert_dir

 L. 778        84  LOAD_FAST                'ssl_version'
               86  LOAD_FAST                'self'
               88  STORE_ATTR               ssl_version

 L. 779        90  LOAD_FAST                'assert_hostname'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               assert_hostname

 L. 780        96  LOAD_FAST                'assert_fingerprint'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               assert_fingerprint

Parse error at or near `<164>' instruction at offset 32

    def _prepare_conn(self, conn):
        """
        Prepare the ``connection`` for :meth:`urllib3.util.ssl_wrap_socket`
        and establish the tunnel if proxy is used.
        """
        if isinstance(conn, VerifiedHTTPSConnection):
            conn.set_cert(key_file=(self.key_file), cert_file=(self.cert_file),
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

 L. 811         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                num_connections
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               num_connections

 L. 812        14  LOAD_GLOBAL              log
               16  LOAD_METHOD              debug
               18  LOAD_STR                 'Starting new HTTPS connection (%d): %s:%s'

 L. 813        20  LOAD_FAST                'self'
               22  LOAD_ATTR                num_connections
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                host
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                port
               32  JUMP_IF_TRUE_OR_POP    36  'to 36'
               34  LOAD_STR                 '443'
             36_0  COME_FROM            32  '32'

 L. 812        36  CALL_METHOD_4         4  ''
               38  POP_TOP          

 L. 815        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ConnectionCls
               44  POP_JUMP_IF_FALSE    56  'to 56'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                ConnectionCls
               50  LOAD_GLOBAL              DummyConnection
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    64  'to 64'
             56_0  COME_FROM            44  '44'

 L. 816        56  LOAD_GLOBAL              SSLError
               58  LOAD_STR                 "Can't connect to HTTPS URL because the SSL module is not available."
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'

 L. 819        64  LOAD_FAST                'self'
               66  LOAD_ATTR                host
               68  STORE_FAST               'actual_host'

 L. 820        70  LOAD_FAST                'self'
               72  LOAD_ATTR                port
               74  STORE_FAST               'actual_port'

 L. 821        76  LOAD_FAST                'self'
               78  LOAD_ATTR                proxy
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   102  'to 102'

 L. 822        86  LOAD_FAST                'self'
               88  LOAD_ATTR                proxy
               90  LOAD_ATTR                host
               92  STORE_FAST               'actual_host'

 L. 823        94  LOAD_FAST                'self'
               96  LOAD_ATTR                proxy
               98  LOAD_ATTR                port
              100  STORE_FAST               'actual_port'
            102_0  COME_FROM            84  '84'

 L. 825       102  LOAD_FAST                'self'
              104  LOAD_ATTR                ConnectionCls
              106  BUILD_TUPLE_0         0 
              108  LOAD_FAST                'actual_host'
              110  LOAD_FAST                'actual_port'

 L. 826       112  LOAD_FAST                'self'
              114  LOAD_ATTR                timeout
              116  LOAD_ATTR                connect_timeout

 L. 827       118  LOAD_FAST                'self'
              120  LOAD_ATTR                strict

 L. 825       122  LOAD_CONST               ('host', 'port', 'timeout', 'strict')
              124  BUILD_CONST_KEY_MAP_4     4 

 L. 827       126  LOAD_FAST                'self'
              128  LOAD_ATTR                conn_kw

 L. 825       130  <164>                 1  ''
              132  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              134  STORE_FAST               'conn'

 L. 829       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _prepare_conn
              140  LOAD_FAST                'conn'
              142  CALL_METHOD_1         1  ''
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 52

    def _validate_conn(self, conn):
        super(HTTPSConnectionPool, self)._validate_conn(conn)
        if not getattr(conn, 'sock', None):
            conn.connect()
        if not conn.is_verified:
            warnings.warn'Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings'InsecureRequestWarning


def connection_from_url--- This code section failed: ---

 L. 870         0  LOAD_GLOBAL              get_host
                2  LOAD_FAST                'url'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_3     3 
                8  STORE_FAST               'scheme'
               10  STORE_FAST               'host'
               12  STORE_FAST               'port'

 L. 871        14  LOAD_FAST                'port'
               16  JUMP_IF_TRUE_OR_POP    28  'to 28'
               18  LOAD_GLOBAL              port_by_scheme
               20  LOAD_METHOD              get
               22  LOAD_FAST                'scheme'
               24  LOAD_CONST               80
               26  CALL_METHOD_2         2  ''
             28_0  COME_FROM            16  '16'
               28  STORE_FAST               'port'

 L. 872        30  LOAD_FAST                'scheme'
               32  LOAD_STR                 'https'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    58  'to 58'

 L. 873        38  LOAD_GLOBAL              HTTPSConnectionPool
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

 L. 875        58  LOAD_GLOBAL              HTTPConnectionPool
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


def _ipv6_host--- This code section failed: ---

 L. 892         0  LOAD_FAST                'host'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '['
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    38  'to 38'
               10  LOAD_FAST                'host'
               12  LOAD_METHOD              endswith
               14  LOAD_STR                 ']'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L. 893        20  LOAD_FAST                'host'
               22  LOAD_METHOD              replace
               24  LOAD_STR                 '%25'
               26  LOAD_STR                 '%'
               28  CALL_METHOD_2         2  ''
               30  LOAD_METHOD              strip
               32  LOAD_STR                 '[]'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'host'
             38_0  COME_FROM            18  '18'
             38_1  COME_FROM             8  '8'

 L. 894        38  LOAD_FAST                'scheme'
               40  LOAD_GLOBAL              NORMALIZABLE_SCHEMES
               42  <118>                 0  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 895        46  LOAD_FAST                'host'
               48  LOAD_METHOD              lower
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'host'
             54_0  COME_FROM            44  '44'

 L. 896        54  LOAD_FAST                'host'
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 42