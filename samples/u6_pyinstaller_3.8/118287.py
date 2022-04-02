# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\pool.py
import contextlib, copy, os, platform, socket, sys, threading, collections
try:
    import ssl
    from ssl import SSLError
    _HAVE_SNI = getattr(ssl, 'HAS_SNI', False)
except ImportError:
    _HAVE_SNI = False

    class SSLError(socket.error):
        pass


else:
    try:
        from ssl import CertificateError as _SSLCertificateError
    except ImportError:

        class _SSLCertificateError(ValueError):
            pass


    else:
        from bson import DEFAULT_CODEC_OPTIONS
        from bson.py3compat import imap, itervalues, _unicode, integer_types
        from bson.son import SON
        from pymongo import auth, helpers, thread_util, __version__
        from pymongo.client_session import _validate_session_write_concern
        from pymongo.common import MAX_BSON_SIZE, MAX_IDLE_TIME_SEC, MAX_MESSAGE_SIZE, MAX_POOL_SIZE, MAX_WIRE_VERSION, MAX_WRITE_BATCH_SIZE, MIN_POOL_SIZE, ORDERED_TYPES, WAIT_QUEUE_TIMEOUT
        from pymongo.errors import AutoReconnect, ConnectionFailure, ConfigurationError, InvalidOperation, DocumentTooLarge, NetworkTimeout, NotMasterError, OperationFailure, PyMongoError
        from pymongo.ismaster import IsMaster
        import pymongo.monotonic as _time
        from pymongo.monitoring import ConnectionCheckOutFailedReason, ConnectionClosedReason
        from pymongo.network import command, receive_message, SocketChecker
        from pymongo.read_preferences import ReadPreference
        from pymongo.server_type import SERVER_TYPE
        from pymongo.ssl_match_hostname import match_hostname, CertificateError
try:
    from ipaddress import ip_address

    def is_ip_address--- This code section failed: ---

 L.  80         0  SETUP_FINALLY        20  'to 20'

 L.  81         2  LOAD_GLOBAL              ip_address
                4  LOAD_GLOBAL              _unicode
                6  LOAD_FAST                'address'
                8  CALL_FUNCTION_1       1  ''
               10  CALL_FUNCTION_1       1  ''
               12  POP_TOP          

 L.  82        14  POP_BLOCK        
               16  LOAD_CONST               True
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  83        20  DUP_TOP          
               22  LOAD_GLOBAL              ValueError
               24  LOAD_GLOBAL              UnicodeError
               26  BUILD_TUPLE_2         2 
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  84        38  POP_EXCEPT       
               40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 18


except ImportError:
    if hasattr(socket, 'inet_pton') and socket.has_ipv6:

        def is_ip_address--- This code section failed: ---

 L.  89         0  SETUP_FINALLY        18  'to 18'

 L.  93         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              inet_aton
                6  LOAD_FAST                'address'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L.  94        12  POP_BLOCK        
               14  LOAD_CONST               True
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.  95        18  DUP_TOP          
               20  LOAD_GLOBAL              socket
               22  LOAD_ATTR                error
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    88  'to 88'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  96        34  SETUP_FINALLY        58  'to 58'

 L.  97        36  LOAD_GLOBAL              socket
               38  LOAD_METHOD              inet_pton
               40  LOAD_GLOBAL              socket
               42  LOAD_ATTR                AF_INET6
               44  LOAD_FAST                'address'
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          

 L.  98        50  POP_BLOCK        
               52  POP_EXCEPT       
               54  LOAD_CONST               True
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY    34  '34'

 L.  99        58  DUP_TOP          
               60  LOAD_GLOBAL              socket
               62  LOAD_ATTR                error
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    82  'to 82'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 100        74  POP_EXCEPT       
               76  POP_EXCEPT       
               78  LOAD_CONST               False
               80  RETURN_VALUE     
             82_0  COME_FROM            66  '66'
               82  END_FINALLY      
               84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            26  '26'
               88  END_FINALLY      
             90_0  COME_FROM            86  '86'

Parse error at or near `RETURN_VALUE' instruction at offset 16


    else:

        def is_ip_address--- This code section failed: ---

 L. 104         0  SETUP_FINALLY        18  'to 18'

 L. 105         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              inet_aton
                6  LOAD_FAST                'address'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 106        12  POP_BLOCK        
               14  LOAD_CONST               True
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 107        18  DUP_TOP          
               20  LOAD_GLOBAL              socket
               22  LOAD_ATTR                error
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    54  'to 54'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 108        34  LOAD_STR                 ':'
               36  LOAD_FAST                'address'
               38  COMPARE_OP               in
               40  POP_JUMP_IF_FALSE    48  'to 48'

 L. 117        42  POP_EXCEPT       
               44  LOAD_CONST               True
               46  RETURN_VALUE     
             48_0  COME_FROM            40  '40'

 L. 118        48  POP_EXCEPT       
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            26  '26'
               54  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 16


else:
    try:
        from fcntl import fcntl, F_GETFD, F_SETFD, FD_CLOEXEC

        def _set_non_inheritable_non_atomic(fd):
            """Set the close-on-exec flag on the given file descriptor."""
            flags = fcntl(fd, F_GETFD)
            fcntl(fd, F_SETFD, flags | FD_CLOEXEC)


    except ImportError:

        def _set_non_inheritable_non_atomic(dummy):
            """Dummy function for platforms that don't provide fcntl."""
            pass


    else:
        _MAX_TCP_KEEPIDLE = 300
        _MAX_TCP_KEEPINTVL = 10
        _MAX_TCP_KEEPCNT = 9
        if sys.platform == 'win32':
            try:
                import _winreg as winreg
            except ImportError:
                import winreg
            else:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters') as (key):
                        _DEFAULT_TCP_IDLE_MS, _ = winreg.QueryValueEx(key, 'KeepAliveTime')
                        _DEFAULT_TCP_INTERVAL_MS, _ = winreg.QueryValueEx(key, 'KeepAliveInterval')
                        if not isinstance(_DEFAULT_TCP_IDLE_MS, integer_types):
                            raise ValueError
                        if not isinstance(_DEFAULT_TCP_INTERVAL_MS, integer_types):
                            raise ValueError
                except (OSError, ValueError):

                    def _set_keepalive_times(dummy):
                        pass


                else:

                    def _set_keepalive_times(sock):
                        idle_ms = min(_DEFAULT_TCP_IDLE_MS, _MAX_TCP_KEEPIDLE * 1000)
                        interval_ms = min(_DEFAULT_TCP_INTERVAL_MS, _MAX_TCP_KEEPINTVL * 1000)
                        if idle_ms < _DEFAULT_TCP_IDLE_MS or interval_ms < _DEFAULT_TCP_INTERVAL_MS:
                            sock.ioctl(socket.SIO_KEEPALIVE_VALS, (
                             1, idle_ms, interval_ms))


        else:

            def _set_tcp_option(sock, tcp_option, max_value):
                if hasattr(socket, tcp_option):
                    sockopt = getattr(socket, tcp_option)
                    try:
                        default = sock.getsockopt(socket.IPPROTO_TCP, sockopt)
                        if default > max_value:
                            sock.setsockopt(socket.IPPROTO_TCP, sockopt, max_value)
                    except socket.error:
                        pass


            def _set_keepalive_times(sock):
                _set_tcp_option(sock, 'TCP_KEEPIDLE', _MAX_TCP_KEEPIDLE)
                _set_tcp_option(sock, 'TCP_KEEPINTVL', _MAX_TCP_KEEPINTVL)
                _set_tcp_option(sock, 'TCP_KEEPCNT', _MAX_TCP_KEEPCNT)


        _METADATA = SON([
         (
          'driver', SON([('name', 'PyMongo'), ('version', __version__)]))])
        if sys.platform.startswith('linux'):
            if sys.version_info[:2] < (3, 5):
                _name = ' '.join([part for part in platform.linux_distribution() if part])
            else:
                _name = platform.system()
            _METADATA['os'] = SON([
             (
              'type', platform.system()),
             (
              'name', _name),
             (
              'architecture', platform.machine()),
             (
              'version', platform.release())])
        else:
            if sys.platform == 'darwin':
                _METADATA['os'] = SON([
                 (
                  'type', platform.system()),
                 (
                  'name', platform.system()),
                 (
                  'architecture', platform.machine()),
                 (
                  'version', platform.mac_ver()[0])])
            else:
                if sys.platform == 'win32':
                    _METADATA['os'] = SON([
                     (
                      'type', platform.system()),
                     (
                      'name', ' '.join((platform.system(), platform.release()))),
                     (
                      'architecture', platform.machine()),
                     (
                      'version', '-'.join(platform.win32_ver()[1:3]))])
                else:
                    if sys.platform.startswith('java'):
                        _name, _ver, _arch = platform.java_ver()[(-1)]
                        _METADATA['os'] = SON([
                         (
                          'type', _name),
                         (
                          'name', _name),
                         (
                          'architecture', _arch),
                         (
                          'version', _ver)])
                    else:
                        _aliased = platform.system_alias(platform.system(), platform.release(), platform.version())
                        _METADATA['os'] = SON([
                         (
                          'type', platform.system()),
                         (
                          'name', ' '.join([part for part in _aliased[:2] if part])),
                         (
                          'architecture', platform.machine()),
                         (
                          'version', _aliased[2])])
        if platform.python_implementation().startswith('PyPy'):
            _METADATA['platform'] = ' '.join((
             platform.python_implementation(),
             '.'.join(imap(str, sys.pypy_version_info)),
             '(Python %s)' % '.'.join(imap(str, sys.version_info))))
        else:
            if sys.platform.startswith('java'):
                _METADATA['platform'] = ' '.join((
                 platform.python_implementation(),
                 '.'.join(imap(str, sys.version_info)),
                 '(%s)' % ' '.join((platform.system(), platform.release()))))
            else:
                _METADATA['platform'] = ' '.join((
                 platform.python_implementation(),
                 '.'.join(imap(str, sys.version_info))))
        'foo'.encode('idna')

        def _raise_connection_failure(address, error, msg_prefix=None):
            """Convert a socket.error to ConnectionFailure and raise it."""
            host, port = address
            if port is not None:
                msg = '%s:%d: %s' % (host, port, error)
            else:
                msg = '%s: %s' % (host, error)
            if msg_prefix:
                msg = msg_prefix + msg
            elif isinstance(error, socket.timeout):
                raise NetworkTimeout(msg)
            else:
                if isinstance(error, SSLError) and 'timed out' in str(error):
                    raise NetworkTimeout(msg)
                else:
                    raise AutoReconnect(msg)


        class PoolOptions(object):
            __slots__ = ('__max_pool_size', '__min_pool_size', '__max_idle_time_seconds',
                         '__connect_timeout', '__socket_timeout', '__wait_queue_timeout',
                         '__wait_queue_multiple', '__ssl_context', '__ssl_match_hostname',
                         '__socket_keepalive', '__event_listeners', '__appname',
                         '__driver', '__metadata', '__compression_settings')

            def __init__(self, max_pool_size=MAX_POOL_SIZE, min_pool_size=MIN_POOL_SIZE, max_idle_time_seconds=MAX_IDLE_TIME_SEC, connect_timeout=None, socket_timeout=None, wait_queue_timeout=WAIT_QUEUE_TIMEOUT, wait_queue_multiple=None, ssl_context=None, ssl_match_hostname=True, socket_keepalive=True, event_listeners=None, appname=None, driver=None, compression_settings=None):
                self._PoolOptions__max_pool_size = max_pool_size
                self._PoolOptions__min_pool_size = min_pool_size
                self._PoolOptions__max_idle_time_seconds = max_idle_time_seconds
                self._PoolOptions__connect_timeout = connect_timeout
                self._PoolOptions__socket_timeout = socket_timeout
                self._PoolOptions__wait_queue_timeout = wait_queue_timeout
                self._PoolOptions__wait_queue_multiple = wait_queue_multiple
                self._PoolOptions__ssl_context = ssl_context
                self._PoolOptions__ssl_match_hostname = ssl_match_hostname
                self._PoolOptions__socket_keepalive = socket_keepalive
                self._PoolOptions__event_listeners = event_listeners
                self._PoolOptions__appname = appname
                self._PoolOptions__driver = driver
                self._PoolOptions__compression_settings = compression_settings
                self._PoolOptions__metadata = copy.deepcopy(_METADATA)
                if appname:
                    self._PoolOptions__metadata['application'] = {'name': appname}
                if driver:
                    if driver.name:
                        self._PoolOptions__metadata['driver']['name'] = '%s|%s' % (
                         _METADATA['driver']['name'], driver.name)
                    if driver.version:
                        self._PoolOptions__metadata['driver']['version'] = '%s|%s' % (
                         _METADATA['driver']['version'], driver.version)
                    if driver.platform:
                        self._PoolOptions__metadata['platform'] = '%s|%s' % (
                         _METADATA['platform'], driver.platform)

            @property
            def non_default_options(self):
                """The non-default options this pool was created with.

        Added for CMAP's :class:`PoolCreatedEvent`.
        """
                opts = {}
                if self._PoolOptions__max_pool_size != MAX_POOL_SIZE:
                    opts['maxPoolSize'] = self._PoolOptions__max_pool_size
                if self._PoolOptions__min_pool_size != MIN_POOL_SIZE:
                    opts['minPoolSize'] = self._PoolOptions__min_pool_size
                if self._PoolOptions__max_idle_time_seconds != MAX_IDLE_TIME_SEC:
                    opts['maxIdleTimeMS'] = self._PoolOptions__max_idle_time_seconds * 1000
                if self._PoolOptions__wait_queue_timeout != WAIT_QUEUE_TIMEOUT:
                    opts['waitQueueTimeoutMS'] = self._PoolOptions__wait_queue_timeout * 1000
                return opts

            @property
            def max_pool_size(self):
                """The maximum allowable number of concurrent connections to each
        connected server. Requests to a server will block if there are
        `maxPoolSize` outstanding connections to the requested server.
        Defaults to 100. Cannot be 0.

        When a server's pool has reached `max_pool_size`, operations for that
        server block waiting for a socket to be returned to the pool. If
        ``waitQueueTimeoutMS`` is set, a blocked operation will raise
        :exc:`~pymongo.errors.ConnectionFailure` after a timeout.
        By default ``waitQueueTimeoutMS`` is not set.
        """
                return self._PoolOptions__max_pool_size

            @property
            def min_pool_size(self):
                """The minimum required number of concurrent connections that the pool
        will maintain to each connected server. Default is 0.
        """
                return self._PoolOptions__min_pool_size

            @property
            def max_idle_time_seconds(self):
                """The maximum number of seconds that a connection can remain
        idle in the pool before being removed and replaced. Defaults to
        `None` (no limit).
        """
                return self._PoolOptions__max_idle_time_seconds

            @property
            def connect_timeout(self):
                """How long a connection can take to be opened before timing out.
        """
                return self._PoolOptions__connect_timeout

            @property
            def socket_timeout(self):
                """How long a send or receive on a socket can take before timing out.
        """
                return self._PoolOptions__socket_timeout

            @property
            def wait_queue_timeout(self):
                """How long a thread will wait for a socket from the pool if the pool
        has no free sockets.
        """
                return self._PoolOptions__wait_queue_timeout

            @property
            def wait_queue_multiple(self):
                """Multiplied by max_pool_size to give the number of threads allowed
        to wait for a socket at one time.
        """
                return self._PoolOptions__wait_queue_multiple

            @property
            def ssl_context(self):
                """An SSLContext instance or None.
        """
                return self._PoolOptions__ssl_context

            @property
            def ssl_match_hostname(self):
                """Call ssl.match_hostname if cert_reqs is not ssl.CERT_NONE.
        """
                return self._PoolOptions__ssl_match_hostname

            @property
            def socket_keepalive(self):
                """Whether to send periodic messages to determine if a connection
        is closed.
        """
                return self._PoolOptions__socket_keepalive

            @property
            def event_listeners(self):
                """An instance of pymongo.monitoring._EventListeners.
        """
                return self._PoolOptions__event_listeners

            @property
            def appname(self):
                """The application name, for sending with ismaster in server handshake.
        """
                return self._PoolOptions__appname

            @property
            def driver(self):
                """Driver name and version, for sending with ismaster in handshake.
        """
                return self._PoolOptions__driver

            @property
            def compression_settings(self):
                return self._PoolOptions__compression_settings

            @property
            def metadata(self):
                """A dict of metadata about the application, driver, os, and platform.
        """
                return self._PoolOptions__metadata.copy()


        class SocketInfo(object):
            __doc__ = "Store a socket with some metadata.\n\n    :Parameters:\n      - `sock`: a raw socket object\n      - `pool`: a Pool instance\n      - `address`: the server's (host, port)\n      - `id`: the id of this socket in it's pool\n    "

            def __init__(self, sock, pool, address, id):
                self.sock = sock
                self.address = address
                self.id = id
                self.authset = set()
                self.closed = False
                self.last_checkin_time = _time()
                self.performed_handshake = False
                self.is_writable = False
                self.max_wire_version = MAX_WIRE_VERSION
                self.max_bson_size = MAX_BSON_SIZE
                self.max_message_size = MAX_MESSAGE_SIZE
                self.max_write_batch_size = MAX_WRITE_BATCH_SIZE
                self.supports_sessions = False
                self.is_mongos = False
                self.op_msg_enabled = False
                self.listeners = pool.opts.event_listeners
                self.enabled_for_cmap = pool.enabled_for_cmap
                self.compression_settings = pool.opts.compression_settings
                self.compression_context = None
                self.pool_id = pool.pool_id
                self.ready = False

            def ismaster(self, metadata, cluster_time):
                cmd = SON([('ismaster', 1)])
                if not self.performed_handshake:
                    cmd['client'] = metadata
                    if self.compression_settings:
                        cmd['compression'] = self.compression_settings.compressors
                if self.max_wire_version >= 6:
                    if cluster_time is not None:
                        cmd['$clusterTime'] = cluster_time
                ismaster = IsMaster(self.command('admin', cmd, publish_events=False))
                self.is_writable = ismaster.is_writable
                self.max_wire_version = ismaster.max_wire_version
                self.max_bson_size = ismaster.max_bson_size
                self.max_message_size = ismaster.max_message_size
                self.max_write_batch_size = ismaster.max_write_batch_size
                self.supports_sessions = ismaster.logical_session_timeout_minutes is not None
                self.is_mongos = ismaster.server_type == SERVER_TYPE.Mongos
                if not self.performed_handshake:
                    if self.compression_settings:
                        ctx = self.compression_settings.get_compression_context(ismaster.compressors)
                        self.compression_context = ctx
                self.performed_handshake = True
                self.op_msg_enabled = ismaster.max_wire_version >= 6
                return ismaster

            def command--- This code section failed: ---

 L. 570         0  LOAD_FAST                'self'
                2  LOAD_METHOD              validate_session
                4  LOAD_FAST                'client'
                6  LOAD_FAST                'session'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 571        12  LOAD_GLOBAL              _validate_session_write_concern
               14  LOAD_FAST                'session'
               16  LOAD_FAST                'write_concern'
               18  CALL_FUNCTION_2       2  ''
               20  STORE_FAST               'session'

 L. 574        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'spec'
               26  LOAD_GLOBAL              ORDERED_TYPES
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_TRUE     40  'to 40'

 L. 575        32  LOAD_GLOBAL              SON
               34  LOAD_FAST                'spec'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'spec'
             40_0  COME_FROM            30  '30'

 L. 577        40  LOAD_FAST                'read_concern'
               42  POP_JUMP_IF_FALSE    80  'to 80'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                max_wire_version
               48  LOAD_CONST               4
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    80  'to 80'

 L. 578        54  LOAD_FAST                'read_concern'
               56  LOAD_ATTR                ok_for_legacy

 L. 577        58  POP_JUMP_IF_TRUE     80  'to 80'

 L. 579        60  LOAD_GLOBAL              ConfigurationError

 L. 580        62  LOAD_STR                 'read concern level of %s is not valid with a max wire version of %d.'

 L. 582        64  LOAD_FAST                'read_concern'
               66  LOAD_ATTR                level
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                max_wire_version
               72  BUILD_TUPLE_2         2 

 L. 580        74  BINARY_MODULO    

 L. 579        76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            58  '58'
             80_1  COME_FROM            52  '52'
             80_2  COME_FROM            42  '42'

 L. 583        80  LOAD_FAST                'write_concern'
               82  LOAD_CONST               None
               84  COMPARE_OP               is
               86  POP_JUMP_IF_TRUE    110  'to 110'
               88  LOAD_FAST                'write_concern'
               90  LOAD_ATTR                acknowledged
               92  POP_JUMP_IF_TRUE    110  'to 110'

 L. 584        94  LOAD_FAST                'collation'
               96  LOAD_CONST               None
               98  COMPARE_OP               is

 L. 583       100  POP_JUMP_IF_TRUE    110  'to 110'

 L. 585       102  LOAD_GLOBAL              ConfigurationError

 L. 586       104  LOAD_STR                 'Collation is unsupported for unacknowledged writes.'

 L. 585       106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM           100  '100'
            110_1  COME_FROM            92  '92'
            110_2  COME_FROM            86  '86'

 L. 587       110  LOAD_FAST                'self'
              112  LOAD_ATTR                max_wire_version
              114  LOAD_CONST               5
              116  COMPARE_OP               >=
              118  POP_JUMP_IF_FALSE   142  'to 142'

 L. 588       120  LOAD_FAST                'write_concern'

 L. 587       122  POP_JUMP_IF_FALSE   142  'to 142'

 L. 589       124  LOAD_FAST                'write_concern'
              126  LOAD_ATTR                is_server_default

 L. 587       128  POP_JUMP_IF_TRUE    142  'to 142'

 L. 590       130  LOAD_FAST                'write_concern'
              132  LOAD_ATTR                document
              134  LOAD_FAST                'spec'
              136  LOAD_STR                 'writeConcern'
              138  STORE_SUBSCR     
              140  JUMP_FORWARD        168  'to 168'
            142_0  COME_FROM           128  '128'
            142_1  COME_FROM           122  '122'
            142_2  COME_FROM           118  '118'

 L. 591       142  LOAD_FAST                'self'
              144  LOAD_ATTR                max_wire_version
              146  LOAD_CONST               5
              148  COMPARE_OP               <
              150  POP_JUMP_IF_FALSE   168  'to 168'
              152  LOAD_FAST                'collation'
              154  LOAD_CONST               None
              156  COMPARE_OP               is-not
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L. 592       160  LOAD_GLOBAL              ConfigurationError

 L. 593       162  LOAD_STR                 'Must be connected to MongoDB 3.4+ to use a collation.'

 L. 592       164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
            168_0  COME_FROM           158  '158'
            168_1  COME_FROM           150  '150'
            168_2  COME_FROM           140  '140'

 L. 595       168  LOAD_FAST                'session'
              170  POP_JUMP_IF_FALSE   186  'to 186'

 L. 596       172  LOAD_FAST                'session'
              174  LOAD_METHOD              _apply_to
              176  LOAD_FAST                'spec'
              178  LOAD_FAST                'retryable_write'
              180  LOAD_FAST                'read_preference'
              182  CALL_METHOD_3         3  ''
              184  POP_TOP          
            186_0  COME_FROM           170  '170'

 L. 597       186  LOAD_FAST                'self'
              188  LOAD_METHOD              send_cluster_time
              190  LOAD_FAST                'spec'
              192  LOAD_FAST                'session'
              194  LOAD_FAST                'client'
              196  CALL_METHOD_3         3  ''
              198  POP_TOP          

 L. 598       200  LOAD_FAST                'publish_events'
              202  POP_JUMP_IF_FALSE   210  'to 210'
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                listeners
              208  JUMP_FORWARD        212  'to 212'
            210_0  COME_FROM           202  '202'
              210  LOAD_CONST               None
            212_0  COME_FROM           208  '208'
              212  STORE_FAST               'listeners'

 L. 599       214  LOAD_FAST                'write_concern'
              216  JUMP_IF_FALSE_OR_POP   224  'to 224'
              218  LOAD_FAST                'write_concern'
              220  LOAD_ATTR                acknowledged
              222  UNARY_NOT        
            224_0  COME_FROM           216  '216'
              224  STORE_FAST               'unacknowledged'

 L. 600       226  LOAD_FAST                'self'
              228  LOAD_ATTR                op_msg_enabled
              230  POP_JUMP_IF_FALSE   242  'to 242'

 L. 601       232  LOAD_FAST                'self'
              234  LOAD_METHOD              _raise_if_not_writable
              236  LOAD_FAST                'unacknowledged'
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
            242_0  COME_FROM           230  '230'

 L. 602       242  SETUP_FINALLY       310  'to 310'

 L. 603       244  LOAD_GLOBAL              command
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                sock
              250  LOAD_FAST                'dbname'
              252  LOAD_FAST                'spec'
              254  LOAD_FAST                'slave_ok'

 L. 604       256  LOAD_FAST                'self'
              258  LOAD_ATTR                is_mongos

 L. 604       260  LOAD_FAST                'read_preference'

 L. 604       262  LOAD_FAST                'codec_options'

 L. 605       264  LOAD_FAST                'session'

 L. 605       266  LOAD_FAST                'client'

 L. 605       268  LOAD_FAST                'check'

 L. 605       270  LOAD_FAST                'allowable_errors'

 L. 606       272  LOAD_FAST                'self'
              274  LOAD_ATTR                address

 L. 606       276  LOAD_FAST                'check_keys'

 L. 606       278  LOAD_FAST                'listeners'

 L. 607       280  LOAD_FAST                'self'
              282  LOAD_ATTR                max_bson_size

 L. 607       284  LOAD_FAST                'read_concern'

 L. 608       286  LOAD_FAST                'parse_write_concern_error'

 L. 609       288  LOAD_FAST                'collation'

 L. 610       290  LOAD_FAST                'self'
              292  LOAD_ATTR                compression_context

 L. 611       294  LOAD_FAST                'self'
              296  LOAD_ATTR                op_msg_enabled

 L. 612       298  LOAD_FAST                'unacknowledged'

 L. 613       300  LOAD_FAST                'user_fields'

 L. 603       302  LOAD_CONST               ('parse_write_concern_error', 'collation', 'compression_ctx', 'use_op_msg', 'unacknowledged', 'user_fields')
              304  CALL_FUNCTION_KW_22    22  '22 total positional and keyword args'
              306  POP_BLOCK        
              308  RETURN_VALUE     
            310_0  COME_FROM_FINALLY   242  '242'

 L. 614       310  DUP_TOP          
              312  LOAD_GLOBAL              OperationFailure
              314  COMPARE_OP               exception-match
          316_318  POP_JUMP_IF_FALSE   332  'to 332'
              320  POP_TOP          
              322  POP_TOP          
              324  POP_TOP          

 L. 615       326  RAISE_VARARGS_0       0  'reraise'
              328  POP_EXCEPT       
              330  JUMP_FORWARD        378  'to 378'
            332_0  COME_FROM           316  '316'

 L. 617       332  DUP_TOP          
              334  LOAD_GLOBAL              BaseException
              336  COMPARE_OP               exception-match
          338_340  POP_JUMP_IF_FALSE   376  'to 376'
              342  POP_TOP          
              344  STORE_FAST               'error'
              346  POP_TOP          
              348  SETUP_FINALLY       364  'to 364'

 L. 618       350  LOAD_FAST                'self'
              352  LOAD_METHOD              _raise_connection_failure
              354  LOAD_FAST                'error'
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          
              360  POP_BLOCK        
              362  BEGIN_FINALLY    
            364_0  COME_FROM_FINALLY   348  '348'
              364  LOAD_CONST               None
              366  STORE_FAST               'error'
              368  DELETE_FAST              'error'
              370  END_FINALLY      
              372  POP_EXCEPT       
              374  JUMP_FORWARD        378  'to 378'
            376_0  COME_FROM           338  '338'
              376  END_FINALLY      
            378_0  COME_FROM           374  '374'
            378_1  COME_FROM           330  '330'

Parse error at or near `POP_TOP' instruction at offset 322

            def send_message(self, message, max_doc_size):
                """Send a raw BSON message or raise ConnectionFailure.

        If a network exception is raised, the socket is closed.
        """
                if self.max_bson_size is not None:
                    if max_doc_size > self.max_bson_size:
                        raise DocumentTooLarge('BSON document too large (%d bytes) - the connected server supports BSON document sizes up to %d bytes.' % (
                         max_doc_size, self.max_bson_size))
                try:
                    self.sock.sendall(message)
                except BaseException as error:
                    try:
                        self._raise_connection_failure(error)
                    finally:
                        error = None
                        del error

            def receive_message(self, request_id):
                """Receive a raw BSON message or raise ConnectionFailure.

        If any exception is raised, the socket is closed.
        """
                try:
                    return receive_message(self.sock, request_id, self.max_message_size)
                            except BaseException as error:
                    try:
                        self._raise_connection_failure(error)
                    finally:
                        error = None
                        del error

            def _raise_if_not_writable(self, unacknowledged):
                """Raise NotMasterError on unacknowledged write if this socket is not
        writable.
        """
                if unacknowledged:
                    if not self.is_writable:
                        raise NotMasterError('not master', {'ok':0, 
                         'errmsg':'not master',  'code':10107})

            def legacy_write(self, request_id, msg, max_doc_size, with_last_error):
                """Send OP_INSERT, etc., optionally returning response as a dict.

        Can raise ConnectionFailure or OperationFailure.

        :Parameters:
          - `request_id`: an int.
          - `msg`: bytes, an OP_INSERT, OP_UPDATE, or OP_DELETE message,
            perhaps with a getlasterror command appended.
          - `max_doc_size`: size in bytes of the largest document in `msg`.
          - `with_last_error`: True if a getlasterror command is appended.
        """
                self._raise_if_not_writable(not with_last_error)
                self.send_message(msg, max_doc_size)
                if with_last_error:
                    reply = self.receive_message(request_id)
                    return helpers._check_gle_response(reply.command_response())

            def write_command(self, request_id, msg):
                """Send "insert" etc. command, returning response as a dict.

        Can raise ConnectionFailure or OperationFailure.

        :Parameters:
          - `request_id`: an int.
          - `msg`: bytes, the command message.
        """
                self.send_message(msg, 0)
                reply = self.receive_message(request_id)
                result = reply.command_response()
                helpers._check_command_response(result)
                return result

            def check_auth(self, all_credentials):
                """Update this socket's authentication.

        Log in or out to bring this socket's credentials up to date with
        those provided. Can raise ConnectionFailure or OperationFailure.

        :Parameters:
          - `all_credentials`: dict, maps auth source to MongoCredential.
        """
                if all_credentials or self.authset:
                    cached = set(itervalues(all_credentials))
                    authset = self.authset.copy()
                    for credentials in authset - cached:
                        auth.logout(credentials.source, self)
                        self.authset.discard(credentials)
                    else:
                        for credentials in cached - authset:
                            auth.authenticate(credentials, self)
                            self.authset.add(credentials)

                if not self.ready:
                    self.ready = True
                    if self.enabled_for_cmap:
                        self.listeners.publish_connection_ready(self.address, self.id)

            def authenticate(self, credentials):
                """Log in to the server and store these credentials in `authset`.

        Can raise ConnectionFailure or OperationFailure.

        :Parameters:
          - `credentials`: A MongoCredential.
        """
                auth.authenticate(credentials, self)
                self.authset.add(credentials)

            def validate_session(self, client, session):
                """Validate this session before use with client.

        Raises error if this session is logged in as a different user or
        the client is not the one that created the session.
        """
                if session:
                    if session._client is not client:
                        raise InvalidOperation('Can only use session with the MongoClient that started it')
                    if session._authset != self.authset:
                        raise InvalidOperation('Cannot use session after authenticating with different credentials')

            def close_socket(self, reason):
                """Close this connection with a reason."""
                if self.closed:
                    return
                self.closed = True
                try:
                    self.sock.close()
                except Exception:
                    pass
                else:
                    if reason:
                        if self.enabled_for_cmap:
                            self.listeners.publish_connection_closed(self.address, self.id, reason)

            def send_cluster_time(self, command, session, client):
                """Add cluster time for MongoDB >= 3.6."""
                if self.max_wire_version >= 6:
                    if client:
                        client._send_cluster_time(command, session)

            def update_last_checkin_time(self):
                self.last_checkin_time = _time()

            def update_is_writable(self, is_writable):
                self.is_writable = is_writable

            def idle_time_seconds(self):
                """Seconds since this socket was last checked into its pool."""
                return _time() - self.last_checkin_time

            def _raise_connection_failure(self, error):
                self.close_socket(ConnectionClosedReason.ERROR)
                if isinstance(error, socket.error):
                    _raise_connection_failure(self.address, error)
                else:
                    raise

            def __eq__(self, other):
                return self.sock == other.sock

            def __ne__(self, other):
                return not self == other

            def __hash__(self):
                return hash(self.sock)

            def __repr__(self):
                return 'SocketInfo(%s)%s at %s' % (
                 repr(self.sock),
                 self.closed and ' CLOSED' or '',
                 id(self))


        def _create_connection--- This code section failed: ---

 L. 823         0  LOAD_FAST                'address'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'host'
                6  STORE_FAST               'port'

 L. 826         8  LOAD_FAST                'host'
               10  LOAD_METHOD              endswith
               12  LOAD_STR                 '.sock'
               14  CALL_METHOD_1         1  ''
               16  POP_JUMP_IF_FALSE   110  'to 110'

 L. 827        18  LOAD_GLOBAL              hasattr
               20  LOAD_GLOBAL              socket
               22  LOAD_STR                 'AF_UNIX'
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_TRUE     36  'to 36'

 L. 828        28  LOAD_GLOBAL              ConnectionFailure
               30  LOAD_STR                 'UNIX-sockets are not supported on this system'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 830        36  LOAD_GLOBAL              socket
               38  LOAD_METHOD              socket
               40  LOAD_GLOBAL              socket
               42  LOAD_ATTR                AF_UNIX
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'sock'

 L. 832        48  LOAD_GLOBAL              _set_non_inheritable_non_atomic
               50  LOAD_FAST                'sock'
               52  LOAD_METHOD              fileno
               54  CALL_METHOD_0         0  ''
               56  CALL_FUNCTION_1       1  ''
               58  POP_TOP          

 L. 833        60  SETUP_FINALLY        78  'to 78'

 L. 834        62  LOAD_FAST                'sock'
               64  LOAD_METHOD              connect
               66  LOAD_FAST                'host'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 835        72  LOAD_FAST                'sock'
               74  POP_BLOCK        
               76  RETURN_VALUE     
             78_0  COME_FROM_FINALLY    60  '60'

 L. 836        78  DUP_TOP          
               80  LOAD_GLOBAL              socket
               82  LOAD_ATTR                error
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   108  'to 108'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L. 837        94  LOAD_FAST                'sock'
               96  LOAD_METHOD              close
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          

 L. 838       102  RAISE_VARARGS_0       0  'reraise'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            86  '86'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            16  '16'

 L. 843       110  LOAD_GLOBAL              socket
              112  LOAD_ATTR                AF_INET
              114  STORE_FAST               'family'

 L. 844       116  LOAD_GLOBAL              socket
              118  LOAD_ATTR                has_ipv6
              120  POP_JUMP_IF_FALSE   136  'to 136'
              122  LOAD_FAST                'host'
              124  LOAD_STR                 'localhost'
              126  COMPARE_OP               !=
              128  POP_JUMP_IF_FALSE   136  'to 136'

 L. 845       130  LOAD_GLOBAL              socket
              132  LOAD_ATTR                AF_UNSPEC
              134  STORE_FAST               'family'
            136_0  COME_FROM           128  '128'
            136_1  COME_FROM           120  '120'

 L. 847       136  LOAD_CONST               None
              138  STORE_FAST               'err'

 L. 848       140  LOAD_GLOBAL              socket
              142  LOAD_METHOD              getaddrinfo
              144  LOAD_FAST                'host'
              146  LOAD_FAST                'port'
              148  LOAD_FAST                'family'
              150  LOAD_GLOBAL              socket
              152  LOAD_ATTR                SOCK_STREAM
              154  CALL_METHOD_4         4  ''
              156  GET_ITER         
              158  FOR_ITER            396  'to 396'
              160  STORE_FAST               'res'

 L. 849       162  LOAD_FAST                'res'
              164  UNPACK_SEQUENCE_5     5 
              166  STORE_FAST               'af'
              168  STORE_FAST               'socktype'
              170  STORE_FAST               'proto'
              172  STORE_FAST               'dummy'
              174  STORE_FAST               'sa'

 L. 853       176  SETUP_FINALLY       208  'to 208'

 L. 854       178  LOAD_GLOBAL              socket
              180  LOAD_METHOD              socket

 L. 855       182  LOAD_FAST                'af'

 L. 855       184  LOAD_FAST                'socktype'
              186  LOAD_GLOBAL              getattr
              188  LOAD_GLOBAL              socket
              190  LOAD_STR                 'SOCK_CLOEXEC'
              192  LOAD_CONST               0
              194  CALL_FUNCTION_3       3  ''
              196  BINARY_OR        

 L. 855       198  LOAD_FAST                'proto'

 L. 854       200  CALL_METHOD_3         3  ''
              202  STORE_FAST               'sock'
              204  POP_BLOCK        
              206  JUMP_FORWARD        244  'to 244'
            208_0  COME_FROM_FINALLY   176  '176'

 L. 856       208  DUP_TOP          
              210  LOAD_GLOBAL              socket
              212  LOAD_ATTR                error
              214  COMPARE_OP               exception-match
              216  POP_JUMP_IF_FALSE   242  'to 242'
              218  POP_TOP          
              220  POP_TOP          
              222  POP_TOP          

 L. 859       224  LOAD_GLOBAL              socket
              226  LOAD_METHOD              socket
              228  LOAD_FAST                'af'
              230  LOAD_FAST                'socktype'
              232  LOAD_FAST                'proto'
              234  CALL_METHOD_3         3  ''
              236  STORE_FAST               'sock'
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           216  '216'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           206  '206'

 L. 861       244  LOAD_GLOBAL              _set_non_inheritable_non_atomic
              246  LOAD_FAST                'sock'
              248  LOAD_METHOD              fileno
              250  CALL_METHOD_0         0  ''
              252  CALL_FUNCTION_1       1  ''
              254  POP_TOP          

 L. 862       256  SETUP_FINALLY       344  'to 344'

 L. 863       258  LOAD_FAST                'sock'
              260  LOAD_METHOD              setsockopt
              262  LOAD_GLOBAL              socket
              264  LOAD_ATTR                IPPROTO_TCP
              266  LOAD_GLOBAL              socket
              268  LOAD_ATTR                TCP_NODELAY
              270  LOAD_CONST               1
              272  CALL_METHOD_3         3  ''
              274  POP_TOP          

 L. 864       276  LOAD_FAST                'sock'
              278  LOAD_METHOD              settimeout
              280  LOAD_FAST                'options'
              282  LOAD_ATTR                connect_timeout
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L. 865       288  LOAD_FAST                'sock'
              290  LOAD_METHOD              setsockopt
              292  LOAD_GLOBAL              socket
              294  LOAD_ATTR                SOL_SOCKET
              296  LOAD_GLOBAL              socket
              298  LOAD_ATTR                SO_KEEPALIVE

 L. 866       300  LOAD_FAST                'options'
              302  LOAD_ATTR                socket_keepalive

 L. 865       304  CALL_METHOD_3         3  ''
              306  POP_TOP          

 L. 867       308  LOAD_FAST                'options'
              310  LOAD_ATTR                socket_keepalive
          312_314  POP_JUMP_IF_FALSE   324  'to 324'

 L. 868       316  LOAD_GLOBAL              _set_keepalive_times
              318  LOAD_FAST                'sock'
              320  CALL_FUNCTION_1       1  ''
              322  POP_TOP          
            324_0  COME_FROM           312  '312'

 L. 869       324  LOAD_FAST                'sock'
              326  LOAD_METHOD              connect
              328  LOAD_FAST                'sa'
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          

 L. 870       334  LOAD_FAST                'sock'
              336  POP_BLOCK        
              338  ROT_TWO          
              340  POP_TOP          
              342  RETURN_VALUE     
            344_0  COME_FROM_FINALLY   256  '256'

 L. 871       344  DUP_TOP          
              346  LOAD_GLOBAL              socket
              348  LOAD_ATTR                error
              350  COMPARE_OP               exception-match
          352_354  POP_JUMP_IF_FALSE   392  'to 392'
              356  POP_TOP          
              358  STORE_FAST               'e'
              360  POP_TOP          
              362  SETUP_FINALLY       380  'to 380'

 L. 872       364  LOAD_FAST                'e'
              366  STORE_FAST               'err'

 L. 873       368  LOAD_FAST                'sock'
              370  LOAD_METHOD              close
              372  CALL_METHOD_0         0  ''
              374  POP_TOP          
              376  POP_BLOCK        
              378  BEGIN_FINALLY    
            380_0  COME_FROM_FINALLY   362  '362'
              380  LOAD_CONST               None
              382  STORE_FAST               'e'
              384  DELETE_FAST              'e'
              386  END_FINALLY      
              388  POP_EXCEPT       
              390  JUMP_BACK           158  'to 158'
            392_0  COME_FROM           352  '352'
              392  END_FINALLY      
              394  JUMP_BACK           158  'to 158'

 L. 875       396  LOAD_FAST                'err'
              398  LOAD_CONST               None
              400  COMPARE_OP               is-not
          402_404  POP_JUMP_IF_FALSE   412  'to 412'

 L. 876       406  LOAD_FAST                'err'
              408  RAISE_VARARGS_1       1  'exception instance'
              410  JUMP_FORWARD        422  'to 422'
            412_0  COME_FROM           402  '402'

 L. 882       412  LOAD_GLOBAL              socket
              414  LOAD_METHOD              error
              416  LOAD_STR                 'getaddrinfo failed'
              418  CALL_METHOD_1         1  ''
              420  RAISE_VARARGS_1       1  'exception instance'
            422_0  COME_FROM           410  '410'

Parse error at or near `POP_TOP' instruction at offset 90


        _PY37PLUS = sys.version_info[:2] >= (3, 7)

        def _configured_socket(address, options):
            """Given (host, port) and PoolOptions, return a configured socket.

    Can raise socket.error, ConnectionFailure, or CertificateError.

    Sets socket's SSL and timeout options.
    """
            sock = _create_connection(address, options)
            ssl_context = options.ssl_context
            if ssl_context is not None:
                host = address[0]
                try:
                    if _HAVE_SNI:
                        if not is_ip_address(host) or _PY37PLUS:
                            sock = ssl_context.wrap_socket(sock, server_hostname=host)
                    else:
                        sock = ssl_context.wrap_socket(sock)
                except _SSLCertificateError:
                    sock.close()
                    raise
                except IOError as exc:
                    try:
                        sock.close()
                        _raise_connection_failure(address, exc, 'SSL handshake failed: ')
                    finally:
                        exc = None
                        del exc

                if ssl_context.verify_mode and not getattr(ssl_context, 'check_hostname', False):
                    if options.ssl_match_hostname:
                        try:
                            match_hostname((sock.getpeercert()), hostname=host)
                        except CertificateError:
                            sock.close()
                            raise

            sock.settimeout(options.socket_timeout)
            return sock


        class _PoolClosedError(PyMongoError):
            __doc__ = 'Internal error raised when a thread tries to get a connection from a\n    closed pool.\n    '


        class Pool:

            def __init__(self, address, options, handshake=True):
                """
        :Parameters:
          - `address`: a (hostname, port) tuple
          - `options`: a PoolOptions instance
          - `handshake`: whether to call ismaster for each new SocketInfo
        """
                self._check_interval_seconds = 1
                self.sockets = collections.deque()
                self.lock = threading.Lock()
                self.active_sockets = 0
                self.next_connection_id = 1
                self.closed = False
                self.is_writable = None
                self.pool_id = 0
                self.pid = os.getpid()
                self.address = address
                self.opts = options
                self.handshake = handshake
                self.enabled_for_cmap = self.handshake and self.opts.event_listeners is not None and self.opts.event_listeners.enabled_for_cmap
                if self.opts.wait_queue_multiple is None or self.opts.max_pool_size is None:
                    max_waiters = None
                else:
                    max_waiters = self.opts.max_pool_size * self.opts.wait_queue_multiple
                self._socket_semaphore = thread_util.create_semaphore(self.opts.max_pool_size, max_waiters)
                self.socket_checker = SocketChecker()
                if self.enabled_for_cmap:
                    self.opts.event_listeners.publish_pool_created(self.address, self.opts.non_default_options)

            def _reset--- This code section failed: ---

 L. 996         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lock
                4  SETUP_WITH           90  'to 90'
                6  POP_TOP          

 L. 997         8  LOAD_FAST                'self'
               10  LOAD_ATTR                closed
               12  POP_JUMP_IF_FALSE    28  'to 28'

 L. 998        14  POP_BLOCK        
               16  BEGIN_FINALLY    
               18  WITH_CLEANUP_START
               20  WITH_CLEANUP_FINISH
               22  POP_FINALLY           0  ''
               24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            12  '12'

 L. 999        28  LOAD_FAST                'self'
               30  DUP_TOP          
               32  LOAD_ATTR                pool_id
               34  LOAD_CONST               1
               36  INPLACE_ADD      
               38  ROT_TWO          
               40  STORE_ATTR               pool_id

 L.1000        42  LOAD_GLOBAL              os
               44  LOAD_METHOD              getpid
               46  CALL_METHOD_0         0  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               pid

 L.1001        52  LOAD_FAST                'self'
               54  LOAD_ATTR                sockets
               56  LOAD_GLOBAL              collections
               58  LOAD_METHOD              deque
               60  CALL_METHOD_0         0  ''
               62  ROT_TWO          
               64  STORE_FAST               'sockets'
               66  LOAD_FAST                'self'
               68  STORE_ATTR               sockets

 L.1002        70  LOAD_CONST               0
               72  LOAD_FAST                'self'
               74  STORE_ATTR               active_sockets

 L.1003        76  LOAD_FAST                'close'
               78  POP_JUMP_IF_FALSE    86  'to 86'

 L.1004        80  LOAD_CONST               True
               82  LOAD_FAST                'self'
               84  STORE_ATTR               closed
             86_0  COME_FROM            78  '78'
               86  POP_BLOCK        
               88  BEGIN_FINALLY    
             90_0  COME_FROM_WITH        4  '4'
               90  WITH_CLEANUP_START
               92  WITH_CLEANUP_FINISH
               94  END_FINALLY      

 L.1006        96  LOAD_FAST                'self'
               98  LOAD_ATTR                opts
              100  LOAD_ATTR                event_listeners
              102  STORE_FAST               'listeners'

 L.1010       104  LOAD_FAST                'close'
              106  POP_JUMP_IF_FALSE   150  'to 150'

 L.1011       108  LOAD_FAST                'sockets'
              110  GET_ITER         
              112  FOR_ITER            130  'to 130'
              114  STORE_FAST               'sock_info'

 L.1012       116  LOAD_FAST                'sock_info'
              118  LOAD_METHOD              close_socket
              120  LOAD_GLOBAL              ConnectionClosedReason
              122  LOAD_ATTR                POOL_CLOSED
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
              128  JUMP_BACK           112  'to 112'

 L.1013       130  LOAD_FAST                'self'
              132  LOAD_ATTR                enabled_for_cmap
              134  POP_JUMP_IF_FALSE   190  'to 190'

 L.1014       136  LOAD_FAST                'listeners'
              138  LOAD_METHOD              publish_pool_closed
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                address
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
              148  JUMP_FORWARD        190  'to 190'
            150_0  COME_FROM           106  '106'

 L.1016       150  LOAD_FAST                'self'
              152  LOAD_ATTR                enabled_for_cmap
              154  POP_JUMP_IF_FALSE   168  'to 168'

 L.1017       156  LOAD_FAST                'listeners'
              158  LOAD_METHOD              publish_pool_cleared
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                address
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
            168_0  COME_FROM           154  '154'

 L.1018       168  LOAD_FAST                'sockets'
              170  GET_ITER         
              172  FOR_ITER            190  'to 190'
              174  STORE_FAST               'sock_info'

 L.1019       176  LOAD_FAST                'sock_info'
              178  LOAD_METHOD              close_socket
              180  LOAD_GLOBAL              ConnectionClosedReason
              182  LOAD_ATTR                STALE
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
              188  JUMP_BACK           172  'to 172'
            190_0  COME_FROM           148  '148'
            190_1  COME_FROM           134  '134'

Parse error at or near `BEGIN_FINALLY' instruction at offset 16

            def update_is_writable(self, is_writable):
                """Updates the is_writable attribute on all sockets currently in the
        Pool.
        """
                self.is_writable = is_writable
                with self.lock:
                    for socket in self.sockets:
                        socket.update_is_writable(self.is_writable)

            def reset(self):
                self._reset(close=False)

            def close(self):
                self._reset(close=True)

            def remove_stale_sockets--- This code section failed: ---

 L.1042         0  LOAD_FAST                'self'
                2  LOAD_ATTR                opts
                4  LOAD_ATTR                max_idle_time_seconds
                6  LOAD_CONST               None
                8  COMPARE_OP               is-not
               10  POP_JUMP_IF_FALSE    82  'to 82'

 L.1043        12  LOAD_FAST                'self'
               14  LOAD_ATTR                lock
               16  SETUP_WITH           76  'to 76'
               18  POP_TOP          

 L.1044        20  LOAD_FAST                'self'
               22  LOAD_ATTR                sockets
               24  POP_JUMP_IF_FALSE    72  'to 72'

 L.1045        26  LOAD_FAST                'self'
               28  LOAD_ATTR                sockets
               30  LOAD_CONST               -1
               32  BINARY_SUBSCR    
               34  LOAD_METHOD              idle_time_seconds
               36  CALL_METHOD_0         0  ''
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                opts
               42  LOAD_ATTR                max_idle_time_seconds
               44  COMPARE_OP               >

 L.1044        46  POP_JUMP_IF_FALSE    72  'to 72'

 L.1046        48  LOAD_FAST                'self'
               50  LOAD_ATTR                sockets
               52  LOAD_METHOD              pop
               54  CALL_METHOD_0         0  ''
               56  STORE_FAST               'sock_info'

 L.1047        58  LOAD_FAST                'sock_info'
               60  LOAD_METHOD              close_socket
               62  LOAD_GLOBAL              ConnectionClosedReason
               64  LOAD_ATTR                IDLE
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
               70  JUMP_BACK            20  'to 20'
             72_0  COME_FROM            46  '46'
             72_1  COME_FROM            24  '24'
               72  POP_BLOCK        
               74  BEGIN_FINALLY    
             76_0  COME_FROM_WITH       16  '16'
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  END_FINALLY      
             82_0  COME_FROM            10  '10'

 L.1050        82  LOAD_FAST                'self'
               84  LOAD_ATTR                lock
               86  SETUP_WITH          130  'to 130'
               88  POP_TOP          

 L.1051        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                sockets
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                active_sockets
              102  BINARY_ADD       

 L.1052       104  LOAD_FAST                'self'
              106  LOAD_ATTR                opts
              108  LOAD_ATTR                min_pool_size

 L.1051       110  COMPARE_OP               >=
              112  POP_JUMP_IF_FALSE   126  'to 126'

 L.1054       114  POP_BLOCK        
              116  BEGIN_FINALLY    
              118  WITH_CLEANUP_START
              120  WITH_CLEANUP_FINISH
              122  POP_FINALLY           0  ''
              124  BREAK_LOOP          246  'to 246'
            126_0  COME_FROM           112  '112'
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_WITH       86  '86'
              130  WITH_CLEANUP_START
              132  WITH_CLEANUP_FINISH
              134  END_FINALLY      

 L.1057       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _socket_semaphore
              140  LOAD_METHOD              acquire
              142  LOAD_CONST               False
              144  CALL_METHOD_1         1  ''
              146  POP_JUMP_IF_TRUE    150  'to 150'

 L.1058       148  BREAK_LOOP          246  'to 246'
            150_0  COME_FROM           146  '146'

 L.1059       150  SETUP_FINALLY       232  'to 232'

 L.1060       152  LOAD_FAST                'self'
              154  LOAD_METHOD              connect
              156  CALL_METHOD_0         0  ''
              158  STORE_FAST               'sock_info'

 L.1061       160  LOAD_FAST                'self'
              162  LOAD_ATTR                lock
              164  SETUP_WITH          222  'to 222'
              166  POP_TOP          

 L.1064       168  LOAD_FAST                'self'
              170  LOAD_ATTR                pool_id
              172  LOAD_FAST                'reference_pool_id'
              174  COMPARE_OP               !=
              176  POP_JUMP_IF_FALSE   206  'to 206'

 L.1065       178  LOAD_FAST                'sock_info'
              180  LOAD_METHOD              close_socket
              182  LOAD_GLOBAL              ConnectionClosedReason
              184  LOAD_ATTR                STALE
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L.1066       190  POP_BLOCK        
              192  BEGIN_FINALLY    
              194  WITH_CLEANUP_START
              196  WITH_CLEANUP_FINISH
              198  POP_FINALLY           0  ''
              200  POP_BLOCK        
              202  CALL_FINALLY        232  'to 232'
              204  BREAK_LOOP          246  'to 246'
            206_0  COME_FROM           176  '176'

 L.1067       206  LOAD_FAST                'self'
              208  LOAD_ATTR                sockets
              210  LOAD_METHOD              appendleft
              212  LOAD_FAST                'sock_info'
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
              218  POP_BLOCK        
              220  BEGIN_FINALLY    
            222_0  COME_FROM_WITH      164  '164'
              222  WITH_CLEANUP_START
              224  WITH_CLEANUP_FINISH
              226  END_FINALLY      
              228  POP_BLOCK        
              230  BEGIN_FINALLY    
            232_0  COME_FROM           202  '202'
            232_1  COME_FROM_FINALLY   150  '150'

 L.1069       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _socket_semaphore
              236  LOAD_METHOD              release
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          
              242  END_FINALLY      
              244  JUMP_BACK            82  'to 82'

Parse error at or near `BEGIN_FINALLY' instruction at offset 116

            def connect(self):
                """Connect to Mongo and return a new SocketInfo.

        Can raise ConnectionFailure or CertificateError.

        Note that the pool does not keep a reference to the socket -- you
        must call return_socket() when you're done with it.
        """
                with self.lock:
                    conn_id = self.next_connection_id
                    self.next_connection_id += 1
                listeners = self.opts.event_listeners
                if self.enabled_for_cmap:
                    listeners.publish_connection_created(self.address, conn_id)
                sock = None
                try:
                    sock = _configured_socket(self.address, self.opts)
                except socket.error as error:
                    try:
                        if sock is not None:
                            sock.close()
                        if self.enabled_for_cmap:
                            listeners.publish_connection_closed(self.address, conn_id, ConnectionClosedReason.ERROR)
                        _raise_connection_failure(self.address, error)
                    finally:
                        error = None
                        del error

                else:
                    sock_info = SocketInfo(sock, self, self.address, conn_id)
                    if self.handshake:
                        sock_info.ismaster(self.opts.metadata, None)
                        self.is_writable = sock_info.is_writable
                    return sock_info

            @contextlib.contextmanager
            def get_socket(self, all_credentials, checkout=False):
                """Get a socket from the pool. Use with a "with" statement.

        Returns a :class:`SocketInfo` object wrapping a connected
        :class:`socket.socket`.

        This method should always be used in a with-statement::

            with pool.get_socket(credentials, checkout) as socket_info:
                socket_info.send_message(msg)
                data = socket_info.receive_message(op_code, request_id)

        The socket is logged in or out as needed to match ``all_credentials``
        using the correct authentication mechanism for the server's wire
        protocol version.

        Can raise ConnectionFailure or OperationFailure.

        :Parameters:
          - `all_credentials`: dict, maps auth source to MongoCredential.
          - `checkout` (optional): keep socket checked out.
        """
                listeners = self.opts.event_listeners
                if self.enabled_for_cmap:
                    listeners.publish_connection_check_out_started(self.address)
                sock_info = self._get_socket_no_auth()
                checked_auth = False
                try:
                    sock_info.check_auth(all_credentials)
                    checked_auth = True
                    if self.enabled_for_cmap:
                        listeners.publish_connection_checked_out(self.address, sock_info.id)
                    (yield sock_info)
                except:
                    self.return_socket(sock_info, publish_checkin=checked_auth)
                    if self.enabled_for_cmap:
                        if not checked_auth:
                            self.opts.event_listeners.publish_connection_check_out_failed(self.address, ConnectionCheckOutFailedReason.CONN_ERROR)
                    raise
                else:
                    if not checkout:
                        self.return_socket(sock_info)

            def _get_socket_no_auth(self):
                """Get or create a SocketInfo. Can raise ConnectionFailure."""
                if self.pid != os.getpid():
                    self.reset()
                else:
                    if self.closed:
                        if self.enabled_for_cmap:
                            self.opts.event_listeners.publish_connection_check_out_failed(self.address, ConnectionCheckOutFailedReason.POOL_CLOSED)
                        raise _PoolClosedError('Attempted to check out a connection from closed connection pool')
                    self._socket_semaphore.acquire(True, self.opts.wait_queue_timeout) or self._raise_wait_queue_timeout()
                with self.lock:
                    self.active_sockets += 1
                try:
                    sock_info = None
                    while sock_info is None:
                        try:
                            with self.lock:
                                sock_info = self.sockets.popleft()
                        except IndexError:
                            sock_info = self.connect()
                        else:
                            if self._perished(sock_info):
                                sock_info = None

                except Exception:
                    self._socket_semaphore.release()
                    with self.lock:
                        self.active_sockets -= 1
                    if self.enabled_for_cmap:
                        self.opts.event_listeners.publish_connection_check_out_failed(self.address, ConnectionCheckOutFailedReason.CONN_ERROR)
                    raise
                else:
                    return sock_info

            def return_socket(self, sock_info, publish_checkin=True):
                """Return the socket to the pool, or if it's closed discard it.

        :Parameters:
          - `sock_info`: The socket to check into the pool.
          - `publish_checkin`: If False, a ConnectionCheckedInEvent will not
            be published.
        """
                listeners = self.opts.event_listeners
                if self.enabled_for_cmap:
                    if publish_checkin:
                        listeners.publish_connection_checked_in(self.address, sock_info.id)
                elif self.pid != os.getpid():
                    self.reset()
                else:
                    if self.closed:
                        sock_info.close_socket(ConnectionClosedReason.POOL_CLOSED)
                    else:
                        if sock_info.pool_id != self.pool_id:
                            sock_info.close_socket(ConnectionClosedReason.STALE)
                        else:
                            if not sock_info.closed:
                                sock_info.update_last_checkin_time()
                                sock_info.update_is_writable(self.is_writable)
                                with self.lock:
                                    self.sockets.appendleft(sock_info)
                self._socket_semaphore.release()
                with self.lock:
                    self.active_sockets -= 1

            def _perished(self, sock_info):
                """This side-effecty function checks if this socket has been idle for
        for longer than the max idle time, or if the socket has been closed by
        some external network error.

        Checking sockets lets us avoid seeing *some*
        :class:`~pymongo.errors.AutoReconnect` exceptions on server
        hiccups, etc. We only check if the socket was closed by an external
        error if it has been > 1 second since the socket was checked into the
        pool, to keep performance reasonable - we can't avoid AutoReconnects
        completely anyway.
        """
                idle_time_seconds = sock_info.idle_time_seconds()
                if self.opts.max_idle_time_seconds is not None:
                    if idle_time_seconds > self.opts.max_idle_time_seconds:
                        sock_info.close_socket(ConnectionClosedReason.IDLE)
                        return True
                if self._check_interval_seconds is not None:
                    if 0 == self._check_interval_seconds or idle_time_seconds > self._check_interval_seconds:
                        if self.socket_checker.socket_closed(sock_info.sock):
                            sock_info.close_socket(ConnectionClosedReason.ERROR)
                            return True
                return False

            def _raise_wait_queue_timeout(self):
                listeners = self.opts.event_listeners
                if self.enabled_for_cmap:
                    listeners.publish_connection_check_out_failed(self.address, ConnectionCheckOutFailedReason.TIMEOUT)
                raise ConnectionFailure('Timed out while checking out a connection from connection pool with max_size %r and wait_queue_timeout %r' % (
                 self.opts.max_pool_size, self.opts.wait_queue_timeout))

            def __del__(self):
                for sock_info in self.sockets:
                    sock_info.close_socket(None)