# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\util\timeout.py
from __future__ import absolute_import
from socket import _GLOBAL_DEFAULT_TIMEOUT
import time
from ..exceptions import TimeoutStateError
_Default = object()
current_time = getattr(time, 'monotonic', time.time)

class Timeout(object):
    __doc__ = ' Timeout configuration.\n\n    Timeouts can be defined as a default for a pool::\n\n        timeout = Timeout(connect=2.0, read=7.0)\n        http = PoolManager(timeout=timeout)\n        response = http.request(\'GET\', \'http://example.com/\')\n\n    Or per-request (which overrides the default for the pool)::\n\n        response = http.request(\'GET\', \'http://example.com/\', timeout=Timeout(10))\n\n    Timeouts can be disabled by setting all the parameters to ``None``::\n\n        no_timeout = Timeout(connect=None, read=None)\n        response = http.request(\'GET\', \'http://example.com/, timeout=no_timeout)\n\n\n    :param total:\n        This combines the connect and read timeouts into one; the read timeout\n        will be set to the time leftover from the connect attempt. In the\n        event that both a connect timeout and a total are specified, or a read\n        timeout and a total are specified, the shorter timeout will be applied.\n\n        Defaults to None.\n\n    :type total: integer, float, or None\n\n    :param connect:\n        The maximum amount of time to wait for a connection attempt to a server\n        to succeed. Omitting the parameter will default the connect timeout to\n        the system default, probably `the global default timeout in socket.py\n        <http://hg.python.org/cpython/file/603b4d593758/Lib/socket.py#l535>`_.\n        None will set an infinite timeout for connection attempts.\n\n    :type connect: integer, float, or None\n\n    :param read:\n        The maximum amount of time to wait between consecutive\n        read operations for a response from the server. Omitting\n        the parameter will default the read timeout to the system\n        default, probably `the global default timeout in socket.py\n        <http://hg.python.org/cpython/file/603b4d593758/Lib/socket.py#l535>`_.\n        None will set an infinite timeout.\n\n    :type read: integer, float, or None\n\n    .. note::\n\n        Many factors can affect the total amount of time for urllib3 to return\n        an HTTP response.\n\n        For example, Python\'s DNS resolver does not obey the timeout specified\n        on the socket. Other factors that can affect total request time include\n        high CPU load, high swap, the program running at a low priority level,\n        or other behaviors.\n\n        In addition, the read and total timeouts only measure the time between\n        read operations on the socket connecting the client and the server,\n        not the total amount of time for the request to return a complete\n        response. For most requests, the timeout is raised because the server\n        has not sent the first byte in the specified time. This is not always\n        the case; if a server streams one byte every fifteen seconds, a timeout\n        of 20 seconds will not trigger, even though the request will take\n        several minutes to complete.\n\n        If your goal is to cut off any request after a set amount of wall clock\n        time, consider having a second "watcher" thread to cut off a slow\n        request.\n    '
    DEFAULT_TIMEOUT = _GLOBAL_DEFAULT_TIMEOUT

    def __init__(self, total=None, connect=_Default, read=_Default):
        self._connect = self._validate_timeout(connect, 'connect')
        self._read = self._validate_timeout(read, 'read')
        self.total = self._validate_timeout(total, 'total')
        self._start_connect = None

    def __str__(self):
        return '%s(connect=%r, read=%r, total=%r)' % (
         type(self).__name__, self._connect, self._read, self.total)

    @classmethod
    def _validate_timeout--- This code section failed: ---

 L. 114         0  LOAD_FAST                'value'
                2  LOAD_GLOBAL              _Default
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 115         8  LOAD_FAST                'cls'
               10  LOAD_ATTR                DEFAULT_TIMEOUT
               12  RETURN_VALUE     
             14_0  COME_FROM             6  '6'

 L. 117        14  LOAD_FAST                'value'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_TRUE     32  'to 32'
               22  LOAD_FAST                'value'
               24  LOAD_FAST                'cls'
               26  LOAD_ATTR                DEFAULT_TIMEOUT
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    36  'to 36'
             32_0  COME_FROM            20  '20'

 L. 118        32  LOAD_FAST                'value'
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L. 120        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'value'
               40  LOAD_GLOBAL              bool
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 121        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'Timeout cannot be a boolean value. It must be an int, float or None.'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L. 123        54  SETUP_FINALLY        68  'to 68'

 L. 124        56  LOAD_GLOBAL              float
               58  LOAD_FAST                'value'
               60  CALL_FUNCTION_1       1  ''
               62  POP_TOP          
               64  POP_BLOCK        
               66  JUMP_FORWARD        106  'to 106'
             68_0  COME_FROM_FINALLY    54  '54'

 L. 125        68  DUP_TOP          
               70  LOAD_GLOBAL              TypeError
               72  LOAD_GLOBAL              ValueError
               74  BUILD_TUPLE_2         2 
               76  <121>               104  ''
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 126        84  LOAD_GLOBAL              ValueError
               86  LOAD_STR                 'Timeout value %s was %s, but it must be an int, float or None.'

 L. 127        88  LOAD_FAST                'name'
               90  LOAD_FAST                'value'
               92  BUILD_TUPLE_2         2 

 L. 126        94  BINARY_MODULO    
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
              100  POP_EXCEPT       
              102  JUMP_FORWARD        106  'to 106'
              104  <48>             
            106_0  COME_FROM           102  '102'
            106_1  COME_FROM            66  '66'

 L. 129       106  SETUP_FINALLY       136  'to 136'

 L. 130       108  LOAD_FAST                'value'
              110  LOAD_CONST               0
              112  COMPARE_OP               <=
              114  POP_JUMP_IF_FALSE   132  'to 132'

 L. 131       116  LOAD_GLOBAL              ValueError
              118  LOAD_STR                 'Attempted to set %s timeout to %s, but the timeout cannot be set to a value less than or equal to 0.'

 L. 133       120  LOAD_FAST                'name'
              122  LOAD_FAST                'value'
              124  BUILD_TUPLE_2         2 

 L. 131       126  BINARY_MODULO    
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           114  '114'
              132  POP_BLOCK        
              134  JUMP_FORWARD        170  'to 170'
            136_0  COME_FROM_FINALLY   106  '106'

 L. 134       136  DUP_TOP          
              138  LOAD_GLOBAL              TypeError
              140  <121>               168  ''
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          

 L. 135       148  LOAD_GLOBAL              ValueError
              150  LOAD_STR                 'Timeout value %s was %s, but it must be an int, float or None.'

 L. 136       152  LOAD_FAST                'name'
              154  LOAD_FAST                'value'
              156  BUILD_TUPLE_2         2 

 L. 135       158  BINARY_MODULO    
              160  CALL_FUNCTION_1       1  ''
              162  RAISE_VARARGS_1       1  'exception instance'
              164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
              168  <48>             
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           134  '134'

 L. 138       170  LOAD_FAST                'value'
              172  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def from_float(cls, timeout):
        """ Create a new Timeout from a legacy timeout value.

        The timeout value used by httplib.py sets the same timeout on the
        connect(), and recv() socket requests. This creates a :class:`Timeout`
        object that sets the individual timeouts to the ``timeout`` value
        passed to this function.

        :param timeout: The legacy timeout value.
        :type timeout: integer, float, sentinel default object, or None
        :return: Timeout object
        :rtype: :class:`Timeout`
        """
        return Timeout(read=timeout, connect=timeout)

    def clone(self):
        """ Create a copy of the timeout object

        Timeout properties are stored per-pool but each request needs a fresh
        Timeout object to ensure each one has its own start/stop configured.

        :return: a copy of the timeout object
        :rtype: :class:`Timeout`
        """
        return Timeout(connect=(self._connect), read=(self._read), total=(self.total))

    def start_connect--- This code section failed: ---

 L. 177         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _start_connect
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 178        10  LOAD_GLOBAL              TimeoutStateError
               12  LOAD_STR                 'Timeout timer has already been started.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 179        18  LOAD_GLOBAL              current_time
               20  CALL_FUNCTION_0       0  ''
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _start_connect

 L. 180        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _start_connect
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def get_connect_duration--- This code section failed: ---

 L. 190         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _start_connect
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 191        10  LOAD_GLOBAL              TimeoutStateError
               12  LOAD_STR                 "Can't get connect duration for timer that has not started."
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 193        18  LOAD_GLOBAL              current_time
               20  CALL_FUNCTION_0       0  ''
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _start_connect
               26  BINARY_SUBTRACT  
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @property
    def connect_timeout--- This code section failed: ---

 L. 205         0  LOAD_FAST                'self'
                2  LOAD_ATTR                total
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 206        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _connect
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L. 208        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _connect
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_TRUE     38  'to 38'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _connect
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                DEFAULT_TIMEOUT
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    44  'to 44'
             38_0  COME_FROM            24  '24'

 L. 209        38  LOAD_FAST                'self'
               40  LOAD_ATTR                total
               42  RETURN_VALUE     
             44_0  COME_FROM            36  '36'

 L. 211        44  LOAD_GLOBAL              min
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _connect
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                total
               54  CALL_FUNCTION_2       2  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @property
    def read_timeout--- This code section failed: ---

 L. 230         0  LOAD_FAST                'self'
                2  LOAD_ATTR                total
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    88  'to 88'

 L. 231        10  LOAD_FAST                'self'
               12  LOAD_ATTR                total
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                DEFAULT_TIMEOUT
               18  <117>                 1  ''

 L. 230        20  POP_JUMP_IF_FALSE    88  'to 88'

 L. 232        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _read
               26  LOAD_CONST               None
               28  <117>                 1  ''

 L. 230        30  POP_JUMP_IF_FALSE    88  'to 88'

 L. 233        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _read
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                DEFAULT_TIMEOUT
               40  <117>                 1  ''

 L. 230        42  POP_JUMP_IF_FALSE    88  'to 88'

 L. 235        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _start_connect
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    60  'to 60'

 L. 236        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _read
               58  RETURN_VALUE     
             60_0  COME_FROM            52  '52'

 L. 237        60  LOAD_GLOBAL              max
               62  LOAD_CONST               0
               64  LOAD_GLOBAL              min
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                total
               70  LOAD_FAST                'self'
               72  LOAD_METHOD              get_connect_duration
               74  CALL_METHOD_0         0  ''
               76  BINARY_SUBTRACT  

 L. 238        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _read

 L. 237        82  CALL_FUNCTION_2       2  ''
               84  CALL_FUNCTION_2       2  ''
               86  RETURN_VALUE     
             88_0  COME_FROM            42  '42'
             88_1  COME_FROM            30  '30'
             88_2  COME_FROM            20  '20'
             88_3  COME_FROM             8  '8'

 L. 239        88  LOAD_FAST                'self'
               90  LOAD_ATTR                total
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   130  'to 130'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                total
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                DEFAULT_TIMEOUT
              106  <117>                 1  ''
              108  POP_JUMP_IF_FALSE   130  'to 130'

 L. 240       110  LOAD_GLOBAL              max
              112  LOAD_CONST               0
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                total
              118  LOAD_FAST                'self'
              120  LOAD_METHOD              get_connect_duration
              122  CALL_METHOD_0         0  ''
              124  BINARY_SUBTRACT  
              126  CALL_FUNCTION_2       2  ''
              128  RETURN_VALUE     
            130_0  COME_FROM           108  '108'
            130_1  COME_FROM            96  '96'

 L. 242       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _read
              134  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1