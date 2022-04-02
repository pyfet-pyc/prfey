# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: psutil\_common.py
"""Common objects shared by __init__.py and _ps*.py modules."""
from __future__ import division, print_function
import contextlib, errno, functools, os, socket, stat, sys, threading, warnings
from collections import defaultdict
from collections import namedtuple
from socket import AF_INET
from socket import SOCK_DGRAM
from socket import SOCK_STREAM
try:
    from socket import AF_INET6
except ImportError:
    AF_INET6 = None
else:
    try:
        from socket import AF_UNIX
    except ImportError:
        AF_UNIX = None
    else:
        if sys.version_info >= (3, 4):
            import enum
        else:
            enum = None
        PY3 = sys.version_info[0] == 3
        __all__ = [
         'FREEBSD', 'BSD', 'LINUX', 'NETBSD', 'OPENBSD', 'MACOS', 'OSX', 'POSIX',
         'SUNOS', 'WINDOWS',
         'CONN_CLOSE', 'CONN_CLOSE_WAIT', 'CONN_CLOSING', 'CONN_ESTABLISHED',
         'CONN_FIN_WAIT1', 'CONN_FIN_WAIT2', 'CONN_LAST_ACK', 'CONN_LISTEN',
         'CONN_NONE', 'CONN_SYN_RECV', 'CONN_SYN_SENT', 'CONN_TIME_WAIT',
         'NIC_DUPLEX_FULL', 'NIC_DUPLEX_HALF', 'NIC_DUPLEX_UNKNOWN',
         'STATUS_DEAD', 'STATUS_DISK_SLEEP', 'STATUS_IDLE', 'STATUS_LOCKED',
         'STATUS_RUNNING', 'STATUS_SLEEPING', 'STATUS_STOPPED', 'STATUS_SUSPENDED',
         'STATUS_TRACING_STOP', 'STATUS_WAITING', 'STATUS_WAKE_KILL',
         'STATUS_WAKING', 'STATUS_ZOMBIE', 'STATUS_PARKED',
         'ENCODING', 'ENCODING_ERRS', 'AF_INET6',
         'pconn', 'pcputimes', 'pctxsw', 'pgids', 'pio', 'pionice', 'popenfile',
         'pthread', 'puids', 'sconn', 'scpustats', 'sdiskio', 'sdiskpart',
         'sdiskusage', 'snetio', 'snicaddr', 'snicstats', 'sswap', 'suser',
         'conn_tmap', 'deprecated_method', 'isfile_strict', 'memoize',
         'parse_environ_block', 'path_exists_strict', 'usage_percent',
         'supports_ipv6', 'sockfam_to_enum', 'socktype_to_enum', 'wrap_numbers',
         'bytes2human', 'conn_to_ntuple', 'debug',
         'hilite', 'term_supports_colors', 'print_color']
        POSIX = os.name == 'posix'
        WINDOWS = os.name == 'nt'
        LINUX = sys.platform.startswith('linux')
        MACOS = sys.platform.startswith('darwin')
        OSX = MACOS
        FREEBSD = sys.platform.startswith('freebsd')
        OPENBSD = sys.platform.startswith('openbsd')
        NETBSD = sys.platform.startswith('netbsd')
        BSD = FREEBSD or OPENBSD or NETBSD
        SUNOS = sys.platform.startswith(('sunos', 'solaris'))
        AIX = sys.platform.startswith('aix')
        STATUS_RUNNING = 'running'
        STATUS_SLEEPING = 'sleeping'
        STATUS_DISK_SLEEP = 'disk-sleep'
        STATUS_STOPPED = 'stopped'
        STATUS_TRACING_STOP = 'tracing-stop'
        STATUS_ZOMBIE = 'zombie'
        STATUS_DEAD = 'dead'
        STATUS_WAKE_KILL = 'wake-kill'
        STATUS_WAKING = 'waking'
        STATUS_IDLE = 'idle'
        STATUS_LOCKED = 'locked'
        STATUS_WAITING = 'waiting'
        STATUS_SUSPENDED = 'suspended'
        STATUS_PARKED = 'parked'
        CONN_ESTABLISHED = 'ESTABLISHED'
        CONN_SYN_SENT = 'SYN_SENT'
        CONN_SYN_RECV = 'SYN_RECV'
        CONN_FIN_WAIT1 = 'FIN_WAIT1'
        CONN_FIN_WAIT2 = 'FIN_WAIT2'
        CONN_TIME_WAIT = 'TIME_WAIT'
        CONN_CLOSE = 'CLOSE'
        CONN_CLOSE_WAIT = 'CLOSE_WAIT'
        CONN_LAST_ACK = 'LAST_ACK'
        CONN_LISTEN = 'LISTEN'
        CONN_CLOSING = 'CLOSING'
        CONN_NONE = 'NONE'
        if enum is None:
            NIC_DUPLEX_FULL = 2
            NIC_DUPLEX_HALF = 1
            NIC_DUPLEX_UNKNOWN = 0
        else:

            class NicDuplex(enum.IntEnum):
                NIC_DUPLEX_FULL = 2
                NIC_DUPLEX_HALF = 1
                NIC_DUPLEX_UNKNOWN = 0


            globals().update(NicDuplex.__members__)
        if enum is None:
            POWER_TIME_UNKNOWN = -1
            POWER_TIME_UNLIMITED = -2
        else:

            class BatteryTime(enum.IntEnum):
                POWER_TIME_UNKNOWN = -1
                POWER_TIME_UNLIMITED = -2


            globals().update(BatteryTime.__members__)
        ENCODING = sys.getfilesystemencoding()
if not PY3:
    ENCODING_ERRS = 'replace'
else:
    try:
        ENCODING_ERRS = sys.getfilesystemencodeerrors()
    except AttributeError:
        ENCODING_ERRS = 'surrogateescape' if POSIX else 'replace'
    else:
        sswap = namedtuple('sswap', ['total', 'used', 'free', 'percent', 'sin',
         'sout'])
        sdiskusage = namedtuple('sdiskusage', ['total', 'used', 'free', 'percent'])
        sdiskio = namedtuple('sdiskio', ['read_count', 'write_count',
         'read_bytes', 'write_bytes',
         'read_time', 'write_time'])
        sdiskpart = namedtuple('sdiskpart', ['device', 'mountpoint', 'fstype', 'opts',
         'maxfile', 'maxpath'])
        snetio = namedtuple('snetio', ['bytes_sent', 'bytes_recv',
         'packets_sent', 'packets_recv',
         'errin', 'errout',
         'dropin', 'dropout'])
        suser = namedtuple('suser', ['name', 'terminal', 'host', 'started', 'pid'])
        sconn = namedtuple('sconn', ['fd', 'family', 'type', 'laddr', 'raddr',
         'status', 'pid'])
        snicaddr = namedtuple('snicaddr', [
         'family', 'address', 'netmask', 'broadcast', 'ptp'])
        snicstats = namedtuple('snicstats', ['isup', 'duplex', 'speed', 'mtu'])
        scpustats = namedtuple('scpustats', ['ctx_switches', 'interrupts', 'soft_interrupts', 'syscalls'])
        scpufreq = namedtuple('scpufreq', ['current', 'min', 'max'])
        shwtemp = namedtuple('shwtemp', ['label', 'current', 'high', 'critical'])
        sbattery = namedtuple('sbattery', ['percent', 'secsleft', 'power_plugged'])
        sfan = namedtuple('sfan', ['label', 'current'])
        pcputimes = namedtuple('pcputimes', [
         'user', 'system', 'children_user', 'children_system'])
        popenfile = namedtuple('popenfile', ['path', 'fd'])
        pthread = namedtuple('pthread', ['id', 'user_time', 'system_time'])
        puids = namedtuple('puids', ['real', 'effective', 'saved'])
        pgids = namedtuple('pgids', ['real', 'effective', 'saved'])
        pio = namedtuple('pio', ['read_count', 'write_count',
         'read_bytes', 'write_bytes'])
        pionice = namedtuple('pionice', ['ioclass', 'value'])
        pctxsw = namedtuple('pctxsw', ['voluntary', 'involuntary'])
        pconn = namedtuple('pconn', ['fd', 'family', 'type', 'laddr', 'raddr',
         'status'])
        addr = namedtuple('addr', ['ip', 'port'])
        conn_tmap = {'all':(
          [
           AF_INET, AF_INET6, AF_UNIX], [SOCK_STREAM, SOCK_DGRAM]), 
         'tcp':(
          [
           AF_INET, AF_INET6], [SOCK_STREAM]), 
         'tcp4':(
          [
           AF_INET], [SOCK_STREAM]), 
         'udp':(
          [
           AF_INET, AF_INET6], [SOCK_DGRAM]), 
         'udp4':(
          [
           AF_INET], [SOCK_DGRAM]), 
         'inet':(
          [
           AF_INET, AF_INET6], [SOCK_STREAM, SOCK_DGRAM]), 
         'inet4':(
          [
           AF_INET], [SOCK_STREAM, SOCK_DGRAM]), 
         'inet6':(
          [
           AF_INET6], [SOCK_STREAM, SOCK_DGRAM])}
        if AF_INET6 is not None:
            conn_tmap.update({'tcp6':(
              [
               AF_INET6], [SOCK_STREAM]), 
             'udp6':(
              [
               AF_INET6], [SOCK_DGRAM])})
        else:
            if AF_UNIX is not None:
                conn_tmap.update({'unix': ([AF_UNIX], [SOCK_STREAM, SOCK_DGRAM])})
            else:

                class Error(Exception):
                    __doc__ = 'Base exception class. All other psutil exceptions inherit\n    from this one.\n    '
                    __module__ = 'psutil'

                    def __init__(self, msg=''):
                        Exception.__init__(self, msg)
                        self.msg = msg

                    def __repr__(self):
                        ret = 'psutil.%s %s' % (self.__class__.__name__, self.msg)
                        return ret.strip()

                    __str__ = __repr__


                class NoSuchProcess(Error):
                    __doc__ = "Exception raised when a process with a certain PID doesn't\n    or no longer exists.\n    "
                    __module__ = 'psutil'

                    def __init__(self, pid, name=None, msg=None):
                        Error.__init__(self, msg)
                        self.pid = pid
                        self.name = name
                        self.msg = msg
                        if msg is None:
                            if name:
                                details = '(pid=%s, name=%s)' % (self.pid, repr(self.name))
                            else:
                                details = '(pid=%s)' % self.pid
                            self.msg = 'process no longer exists ' + details


                class ZombieProcess(NoSuchProcess):
                    __doc__ = "Exception raised when querying a zombie process. This is\n    raised on macOS, BSD and Solaris only, and not always: depending\n    on the query the OS may be able to succeed anyway.\n    On Linux all zombie processes are querable (hence this is never\n    raised). Windows doesn't have zombie processes.\n    "
                    __module__ = 'psutil'

                    def __init__(self, pid, name=None, ppid=None, msg=None):
                        NoSuchProcess.__init__(self, msg)
                        self.pid = pid
                        self.ppid = ppid
                        self.name = name
                        self.msg = msg
                        if msg is None:
                            args = [
                             'pid=%s' % pid]
                            if name:
                                args.append('name=%s' % repr(self.name))
                            if ppid:
                                args.append('ppid=%s' % self.ppid)
                            details = '(%s)' % ', '.join(args)
                            self.msg = "process still exists but it's a zombie " + details


                class AccessDenied(Error):
                    __doc__ = 'Exception raised when permission to perform an action is denied.'
                    __module__ = 'psutil'

                    def __init__(self, pid=None, name=None, msg=None):
                        Error.__init__(self, msg)
                        self.pid = pid
                        self.name = name
                        self.msg = msg
                        if msg is None:
                            if pid is not None and name is not None:
                                self.msg = '(pid=%s, name=%s)' % (pid, repr(name))
                            else:
                                if pid is not None:
                                    self.msg = '(pid=%s)' % self.pid
                                else:
                                    self.msg = ''


                class TimeoutExpired(Error):
                    __doc__ = 'Raised on Process.wait(timeout) if timeout expires and process\n    is still alive.\n    '
                    __module__ = 'psutil'

                    def __init__(self, seconds, pid=None, name=None):
                        Error.__init__(self, 'timeout after %s seconds' % seconds)
                        self.seconds = seconds
                        self.pid = pid
                        self.name = name
                        if pid is not None and name is not None:
                            self.msg += ' (pid=%s, name=%s)' % (pid, repr(name))
                        else:
                            if pid is not None:
                                self.msg += ' (pid=%s)' % self.pid


                def usage_percent(used, total, round_=None):
                    """Calculate percentage usage of 'used' against 'total'."""
                    try:
                        ret = float(used) / total * 100
                    except ZeroDivisionError:
                        return 0.0
                    else:
                        if round_ is not None:
                            ret = round(ret, round_)
                        return ret


                def memoize(fun):
                    """A simple memoize decorator for functions supporting (hashable)
    positional arguments.
    It also provides a cache_clear() function for clearing the cache:

    >>> @memoize
    ... def foo()
    ...     return 1
        ...
    >>> foo()
    1
    >>> foo.cache_clear()
    >>>
    """

                    @functools.wraps(fun)
                    def wrapper--- This code section failed: ---

 L. 401         0  LOAD_FAST                'args'
                2  LOAD_GLOBAL              frozenset
                4  LOAD_GLOBAL              sorted
                6  LOAD_FAST                'kwargs'
                8  LOAD_METHOD              items
               10  CALL_METHOD_0         0  ''
               12  CALL_FUNCTION_1       1  ''
               14  CALL_FUNCTION_1       1  ''
               16  BUILD_TUPLE_2         2 
               18  STORE_FAST               'key'

 L. 402        20  SETUP_FINALLY        32  'to 32'

 L. 403        22  LOAD_DEREF               'cache'
               24  LOAD_FAST                'key'
               26  BINARY_SUBSCR    
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY    20  '20'

 L. 404        32  DUP_TOP          
               34  LOAD_GLOBAL              KeyError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    72  'to 72'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 405        46  LOAD_DEREF               'fun'
               48  LOAD_FAST                'args'
               50  LOAD_FAST                'kwargs'
               52  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               54  DUP_TOP          
               56  STORE_FAST               'ret'
               58  LOAD_DEREF               'cache'
               60  LOAD_FAST                'key'
               62  STORE_SUBSCR     

 L. 406        64  LOAD_FAST                'ret'
               66  ROT_FOUR         
               68  POP_EXCEPT       
               70  RETURN_VALUE     
             72_0  COME_FROM            38  '38'
               72  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 42

                    def cache_clear():
                        cache.clear()

                    cache = {}
                    wrapper.cache_clear = cache_clear
                    return wrapper


                def memoize_when_activated(fun):
                    """A memoize decorator which is disabled by default. It can be
    activated and deactivated on request.
    For efficiency reasons it can be used only against class methods
    accepting no arguments.

    >>> class Foo:
    ...     @memoize
    ...     def foo()
    ...         print(1)
    ...
    >>> f = Foo()
    >>> # deactivated (default)
    >>> foo()
    1
    >>> foo()
    1
    >>>
    >>> # activated
    >>> foo.cache_activate(self)
    >>> foo()
    1
    >>> foo()
    >>> foo()
    >>>
    """

                    @functools.wraps(fun)
                    def wrapper(self):
                        try:
                            ret = self._cache[fun]
                        except AttributeError:
                            return fun(self)
                        except KeyError:
                            ret = self._cache[fun] = fun(self)
                        else:
                            return ret

                    def cache_activate(proc):
                        """Activate cache. Expects a Process instance. Cache will be
        stored as a "_cache" instance attribute."""
                        proc._cache = {}

                    def cache_deactivate(proc):
                        """Deactivate and clear cache."""
                        try:
                            del proc._cache
                        except AttributeError:
                            pass

                    wrapper.cache_activate = cache_activate
                    wrapper.cache_deactivate = cache_deactivate
                    return wrapper


                def isfile_strict--- This code section failed: ---

 L. 479         0  SETUP_FINALLY        16  'to 16'

 L. 480         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              stat
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'st'
               12  POP_BLOCK        
               14  JUMP_FORWARD         76  'to 76'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 481        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    74  'to 74'
               24  POP_TOP          
               26  STORE_FAST               'err'
               28  POP_TOP          
               30  SETUP_FINALLY        62  'to 62'

 L. 482        32  LOAD_FAST                'err'
               34  LOAD_ATTR                errno
               36  LOAD_GLOBAL              errno
               38  LOAD_ATTR                EPERM
               40  LOAD_GLOBAL              errno
               42  LOAD_ATTR                EACCES
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               in
               48  POP_JUMP_IF_FALSE    52  'to 52'

 L. 483        50  RAISE_VARARGS_0       0  'reraise'
             52_0  COME_FROM            48  '48'

 L. 484        52  POP_BLOCK        
               54  POP_EXCEPT       
               56  CALL_FINALLY         62  'to 62'
               58  LOAD_CONST               False
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'
             62_1  COME_FROM_FINALLY    30  '30'
               62  LOAD_CONST               None
               64  STORE_FAST               'err'
               66  DELETE_FAST              'err'
               68  END_FINALLY      
               70  POP_EXCEPT       
               72  JUMP_FORWARD         88  'to 88'
             74_0  COME_FROM            22  '22'
               74  END_FINALLY      
             76_0  COME_FROM            14  '14'

 L. 486        76  LOAD_GLOBAL              stat
               78  LOAD_METHOD              S_ISREG
               80  LOAD_FAST                'st'
               82  LOAD_ATTR                st_mode
               84  CALL_METHOD_1         1  ''
               86  RETURN_VALUE     
             88_0  COME_FROM            72  '72'

Parse error at or near `CALL_FINALLY' instruction at offset 56


                def path_exists_strict--- This code section failed: ---

 L. 494         0  SETUP_FINALLY        16  'to 16'

 L. 495         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              stat
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         76  'to 76'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 496        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    74  'to 74'
               24  POP_TOP          
               26  STORE_FAST               'err'
               28  POP_TOP          
               30  SETUP_FINALLY        62  'to 62'

 L. 497        32  LOAD_FAST                'err'
               34  LOAD_ATTR                errno
               36  LOAD_GLOBAL              errno
               38  LOAD_ATTR                EPERM
               40  LOAD_GLOBAL              errno
               42  LOAD_ATTR                EACCES
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               in
               48  POP_JUMP_IF_FALSE    52  'to 52'

 L. 498        50  RAISE_VARARGS_0       0  'reraise'
             52_0  COME_FROM            48  '48'

 L. 499        52  POP_BLOCK        
               54  POP_EXCEPT       
               56  CALL_FINALLY         62  'to 62'
               58  LOAD_CONST               False
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'
             62_1  COME_FROM_FINALLY    30  '30'
               62  LOAD_CONST               None
               64  STORE_FAST               'err'
               66  DELETE_FAST              'err'
               68  END_FINALLY      
               70  POP_EXCEPT       
               72  JUMP_FORWARD         80  'to 80'
             74_0  COME_FROM            22  '22'
               74  END_FINALLY      
             76_0  COME_FROM            14  '14'

 L. 501        76  LOAD_CONST               True
               78  RETURN_VALUE     
             80_0  COME_FROM            72  '72'

Parse error at or near `CALL_FINALLY' instruction at offset 56


                @memoize
                def supports_ipv6--- This code section failed: ---

 L. 507         0  LOAD_GLOBAL              socket
                2  LOAD_ATTR                has_ipv6
                4  POP_JUMP_IF_FALSE    14  'to 14'
                6  LOAD_GLOBAL              AF_INET6
                8  LOAD_CONST               None
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    18  'to 18'
             14_0  COME_FROM             4  '4'

 L. 508        14  LOAD_CONST               False
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 509        18  SETUP_FINALLY        72  'to 72'

 L. 510        20  LOAD_GLOBAL              socket
               22  LOAD_METHOD              socket
               24  LOAD_GLOBAL              AF_INET6
               26  LOAD_GLOBAL              socket
               28  LOAD_ATTR                SOCK_STREAM
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'sock'

 L. 511        34  LOAD_GLOBAL              contextlib
               36  LOAD_METHOD              closing
               38  LOAD_FAST                'sock'
               40  CALL_METHOD_1         1  ''
               42  SETUP_WITH           60  'to 60'
               44  POP_TOP          

 L. 512        46  LOAD_FAST                'sock'
               48  LOAD_METHOD              bind
               50  LOAD_CONST               ('::1', 0)
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
               56  POP_BLOCK        
               58  BEGIN_FINALLY    
             60_0  COME_FROM_WITH       42  '42'
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  END_FINALLY      

 L. 513        66  POP_BLOCK        
               68  LOAD_CONST               True
               70  RETURN_VALUE     
             72_0  COME_FROM_FINALLY    18  '18'

 L. 514        72  DUP_TOP          
               74  LOAD_GLOBAL              socket
               76  LOAD_ATTR                error
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE    94  'to 94'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 515        88  POP_EXCEPT       
               90  LOAD_CONST               False
               92  RETURN_VALUE     
             94_0  COME_FROM            80  '80'
               94  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 70


                def parse_environ_block(data):
                    """Parse a C environ block of environment variables into a dictionary."""
                    ret = {}
                    pos = 0
                    WINDOWS_ = WINDOWS
                    while True:
                        next_pos = data.find('\x00', pos)
                        if next_pos <= pos:
                            break
                        equal_pos = data.find('=', pos, next_pos)
                        if equal_pos > pos:
                            key = data[pos:equal_pos]
                            value = data[equal_pos + 1:next_pos]
                            if WINDOWS_:
                                key = key.upper()
                            ret[key] = value
                        pos = next_pos + 1

                    return ret


                def sockfam_to_enum--- This code section failed: ---

 L. 550         0  LOAD_GLOBAL              enum
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 551         8  LOAD_FAST                'num'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 553        12  SETUP_FINALLY        26  'to 26'

 L. 554        14  LOAD_GLOBAL              socket
               16  LOAD_METHOD              AddressFamily
               18  LOAD_FAST                'num'
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    12  '12'

 L. 555        26  DUP_TOP          
               28  LOAD_GLOBAL              ValueError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    48  'to 48'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 556        40  LOAD_FAST                'num'
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  RETURN_VALUE     
             48_0  COME_FROM            32  '32'
               48  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 36


                def socktype_to_enum--- This code section failed: ---

 L. 563         0  LOAD_GLOBAL              enum
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 564         8  LOAD_FAST                'num'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 566        12  SETUP_FINALLY        26  'to 26'

 L. 567        14  LOAD_GLOBAL              socket
               16  LOAD_METHOD              SocketKind
               18  LOAD_FAST                'num'
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    12  '12'

 L. 568        26  DUP_TOP          
               28  LOAD_GLOBAL              ValueError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    48  'to 48'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 569        40  LOAD_FAST                'num'
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  RETURN_VALUE     
             48_0  COME_FROM            32  '32'
               48  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 36


                def conn_to_ntuple(fd, fam, type_, laddr, raddr, status, status_map, pid=None):
                    """Convert a raw connection tuple to a proper ntuple."""
                    if fam in (socket.AF_INET, AF_INET6):
                        if laddr:
                            laddr = addr(*laddr)
                        if raddr:
                            raddr = addr(*raddr)
                    if type_ == socket.SOCK_STREAM and fam in (AF_INET, AF_INET6):
                        status = status_map.get(status, CONN_NONE)
                    else:
                        status = CONN_NONE
                    fam = sockfam_to_enum(fam)
                    type_ = socktype_to_enum(type_)
                    if pid is None:
                        return pconn(fd, fam, type_, laddr, raddr, status)
                    return sconn(fd, fam, type_, laddr, raddr, status, pid)


                def deprecated_method(replacement):
                    """A decorator which can be used to mark a method as deprecated
    'replcement' is the method name which will be called instead.
    """

                    def outer(fun):
                        msg = '%s() is deprecated and will be removed; use %s() instead' % (
                         fun.__name__, replacement)
                        if fun.__doc__ is None:
                            fun.__doc__ = msg

                        @functools.wraps(fun)
                        def inner(self, *args, **kwargs):
                            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
                            return (getattr(self, replacement))(*args, **kwargs)

                        return inner

                    return outer


                class _WrapNumbers:
                    __doc__ = "Watches numbers so that they don't overflow and wrap\n    (reset to zero).\n    "

                    def __init__(self):
                        self.lock = threading.Lock()
                        self.cache = {}
                        self.reminders = {}
                        self.reminder_keys = {}

                    def _add_dict(self, input_dict, name):
                        assert name not in self.cache
                        assert name not in self.reminders
                        assert name not in self.reminder_keys
                        self.cache[name] = input_dict
                        self.reminders[name] = defaultdict(int)
                        self.reminder_keys[name] = defaultdict(set)

                    def _remove_dead_reminders(self, input_dict, name):
                        """In case the number of keys changed between calls (e.g. a
        disk disappears) this removes the entry from self.reminders.
        """
                        old_dict = self.cache[name]
                        gone_keys = set(old_dict.keys()) - set(input_dict.keys())
                        for gone_key in gone_keys:
                            for remkey in self.reminder_keys[name][gone_key]:
                                del self.reminders[name][remkey]
                            else:
                                del self.reminder_keys[name][gone_key]

                    def run--- This code section failed: ---

 L. 643         0  LOAD_FAST                'name'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                cache
                6  COMPARE_OP               not-in
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 645        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _add_dict
               14  LOAD_FAST                'input_dict'
               16  LOAD_FAST                'name'
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          

 L. 646        22  LOAD_FAST                'input_dict'
               24  RETURN_VALUE     
             26_0  COME_FROM             8  '8'

 L. 648        26  LOAD_FAST                'self'
               28  LOAD_METHOD              _remove_dead_reminders
               30  LOAD_FAST                'input_dict'
               32  LOAD_FAST                'name'
               34  CALL_METHOD_2         2  ''
               36  POP_TOP          

 L. 650        38  LOAD_FAST                'self'
               40  LOAD_ATTR                cache
               42  LOAD_FAST                'name'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'old_dict'

 L. 651        48  BUILD_MAP_0           0 
               50  STORE_FAST               'new_dict'

 L. 652        52  LOAD_FAST                'input_dict'
               54  LOAD_METHOD              keys
               56  CALL_METHOD_0         0  ''
               58  GET_ITER         
               60  FOR_ITER            252  'to 252'
               62  STORE_FAST               'key'

 L. 653        64  LOAD_FAST                'input_dict'
               66  LOAD_FAST                'key'
               68  BINARY_SUBSCR    
               70  STORE_FAST               'input_tuple'

 L. 654        72  SETUP_FINALLY        86  'to 86'

 L. 655        74  LOAD_FAST                'old_dict'
               76  LOAD_FAST                'key'
               78  BINARY_SUBSCR    
               80  STORE_FAST               'old_tuple'
               82  POP_BLOCK        
               84  JUMP_FORWARD        118  'to 118'
             86_0  COME_FROM_FINALLY    72  '72'

 L. 656        86  DUP_TOP          
               88  LOAD_GLOBAL              KeyError
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   116  'to 116'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 659       100  LOAD_FAST                'input_tuple'
              102  LOAD_FAST                'new_dict'
              104  LOAD_FAST                'key'
              106  STORE_SUBSCR     

 L. 660       108  POP_EXCEPT       
              110  JUMP_BACK            60  'to 60'
              112  POP_EXCEPT       
              114  JUMP_FORWARD        118  'to 118'
            116_0  COME_FROM            92  '92'
              116  END_FINALLY      
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM            84  '84'

 L. 662       118  BUILD_LIST_0          0 
              120  STORE_FAST               'bits'

 L. 663       122  LOAD_GLOBAL              range
              124  LOAD_GLOBAL              len
              126  LOAD_FAST                'input_tuple'
              128  CALL_FUNCTION_1       1  ''
              130  CALL_FUNCTION_1       1  ''
              132  GET_ITER         
              134  FOR_ITER            238  'to 238'
              136  STORE_FAST               'i'

 L. 664       138  LOAD_FAST                'input_tuple'
              140  LOAD_FAST                'i'
              142  BINARY_SUBSCR    
              144  STORE_FAST               'input_value'

 L. 665       146  LOAD_FAST                'old_tuple'
              148  LOAD_FAST                'i'
              150  BINARY_SUBSCR    
              152  STORE_FAST               'old_value'

 L. 666       154  LOAD_FAST                'key'
              156  LOAD_FAST                'i'
              158  BUILD_TUPLE_2         2 
              160  STORE_FAST               'remkey'

 L. 667       162  LOAD_FAST                'input_value'
              164  LOAD_FAST                'old_value'
              166  COMPARE_OP               <
              168  POP_JUMP_IF_FALSE   212  'to 212'

 L. 669       170  LOAD_FAST                'self'
              172  LOAD_ATTR                reminders
              174  LOAD_FAST                'name'
              176  BINARY_SUBSCR    
              178  LOAD_FAST                'remkey'
              180  DUP_TOP_TWO      
              182  BINARY_SUBSCR    
              184  LOAD_FAST                'old_value'
              186  INPLACE_ADD      
              188  ROT_THREE        
              190  STORE_SUBSCR     

 L. 670       192  LOAD_FAST                'self'
              194  LOAD_ATTR                reminder_keys
              196  LOAD_FAST                'name'
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'key'
              202  BINARY_SUBSCR    
              204  LOAD_METHOD              add
              206  LOAD_FAST                'remkey'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
            212_0  COME_FROM           168  '168'

 L. 671       212  LOAD_FAST                'bits'
              214  LOAD_METHOD              append
              216  LOAD_FAST                'input_value'
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                reminders
              222  LOAD_FAST                'name'
              224  BINARY_SUBSCR    
              226  LOAD_FAST                'remkey'
              228  BINARY_SUBSCR    
              230  BINARY_ADD       
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          
              236  JUMP_BACK           134  'to 134'

 L. 673       238  LOAD_GLOBAL              tuple
              240  LOAD_FAST                'bits'
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_FAST                'new_dict'
              246  LOAD_FAST                'key'
              248  STORE_SUBSCR     
              250  JUMP_BACK            60  'to 60'

 L. 675       252  LOAD_FAST                'input_dict'
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                cache
              258  LOAD_FAST                'name'
              260  STORE_SUBSCR     

 L. 676       262  LOAD_FAST                'new_dict'
              264  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 112

                    def cache_clear(self, name=None):
                        """Clear the internal cache, optionally only for function 'name'."""
                        with self.lock:
                            if name is None:
                                self.cache.clear()
                                self.reminders.clear()
                                self.reminder_keys.clear()
                            else:
                                self.cache.pop(name, None)
                                self.reminders.pop(name, None)
                                self.reminder_keys.pop(name, None)

                    def cache_info--- This code section failed: ---

 L. 692         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lock
                4  SETUP_WITH           36  'to 36'
                6  POP_TOP          

 L. 693         8  LOAD_FAST                'self'
               10  LOAD_ATTR                cache
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                reminders
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                reminder_keys
               20  BUILD_TUPLE_3         3 
               22  POP_BLOCK        
               24  ROT_TWO          
               26  BEGIN_FINALLY    
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  POP_FINALLY           0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM_WITH        4  '4'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 24


                def wrap_numbers--- This code section failed: ---

 L. 701         0  LOAD_GLOBAL              _wn
                2  LOAD_ATTR                lock
                4  SETUP_WITH           32  'to 32'
                6  POP_TOP          

 L. 702         8  LOAD_GLOBAL              _wn
               10  LOAD_METHOD              run
               12  LOAD_FAST                'input_dict'
               14  LOAD_FAST                'name'
               16  CALL_METHOD_2         2  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        4  '4'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20


                _wn = _WrapNumbers()
                wrap_numbers.cache_clear = _wn.cache_clear
                wrap_numbers.cache_info = _wn.cache_info

                def open_binary(fname, **kwargs):
                    return open(fname, 'rb', **kwargs)


                def open_text(fname, **kwargs):
                    """On Python 3 opens a file in text mode by using fs encoding and
    a proper en/decoding errors handler.
    On Python 2 this is just an alias for open(name, 'rt').
    """
                    if PY3:
                        kwargs.setdefault('encoding', ENCODING)
                        kwargs.setdefault('errors', ENCODING_ERRS)
                    return open(fname, 'rt', **kwargs)


                def bytes2human(n, format='%(value).1f%(symbol)s'):
                    """Used by various scripts. See:
    http://goo.gl/zeJZl

    >>> bytes2human(10000)
    '9.8K'
    >>> bytes2human(100001221)
    '95.4M'
    """
                    symbols = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
                    prefix = {}
                    for i, s in enumerate(symbols[1:]):
                        prefix[s] = 1 << (i + 1) * 10
                    else:
                        for symbol in reversed(symbols[1:]):
                            if n >= prefix[symbol]:
                                value = float(n) / prefix[symbol]
                                return format % locals()
                            return format % dict(symbol=(symbols[0]), value=n)


                def get_procfs_path():
                    """Return updated psutil.PROCFS_PATH constant."""
                    return sys.modules['psutil'].PROCFS_PATH


                if PY3:

                    def decode(s):
                        return s.decode(encoding=ENCODING, errors=ENCODING_ERRS)


                else:

                    def decode(s):
                        return s


            @memoize
            def term_supports_colors(file=sys.stdout):
                if os.name == 'nt':
                    return True
                try:
                    import curses
                    assert file.isatty()
                    curses.setupterm()
                    assert curses.tigetnum('colors') > 0
                except Exception:
                    return False
                else:
                    return True


            def hilite(s, color=None, bold=False):
                """Return an highlighted version of 'string'."""
                if not term_supports_colors():
                    return s
                attr = []
                colors = dict(green='32', red='91', brown='33', yellow='93', blue='34', violet='35',
                  lightblue='36',
                  grey='37',
                  darkgrey='30')
                colors[None] = '29'
                try:
                    color = colors[color]
                except KeyError:
                    raise ValueError('invalid color %r; choose between %s' % list(colors.keys()))
                else:
                    attr.append(color)
                    if bold:
                        attr.append('1')
                    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), s)


            def print_color(s, color=None, bold=False, file=sys.stdout):
                """Print a colorized version of string."""
                if not term_supports_colors():
                    print(s, file=file)
                else:
                    if POSIX:
                        print((hilite(s, color, bold)), file=file)
                    else:
                        import ctypes
                        DEFAULT_COLOR = 7
                        GetStdHandle = ctypes.windll.Kernel32.GetStdHandle
                        SetConsoleTextAttribute = ctypes.windll.Kernel32.SetConsoleTextAttribute
                        colors = dict(green=2, red=4, brown=6, yellow=6)
                        colors[None] = DEFAULT_COLOR
                try:
                    color = colors[color]
                except KeyError:
                    raise ValueError('invalid color %r; choose between %r' % (
                     color, list(colors.keys())))
                else:
                    if bold:
                        if color <= 7:
                            color += 8
                    handle_id = -12 if file is sys.stderr else -11
                    GetStdHandle.restype = ctypes.c_ulong
                    handle = GetStdHandle(handle_id)
                    SetConsoleTextAttribute(handle, color)
                    try:
                        print(s, file=file)
                    finally:
                        SetConsoleTextAttribute(handle, DEFAULT_COLOR)


            if bool(os.getenv('PSUTIL_DEBUG', 0)):
                import inspect

                def debug(msg):
                    """If PSUTIL_DEBUG env var is set, print a debug message to stderr."""
                    fname, lineno, func_name, lines, index = inspect.getframeinfo(inspect.currentframe().f_back)
                    print(('psutil-debug [%s:%s]> %s' % (fname, lineno, msg)), file=(sys.stderr))


            else:

                def debug(msg):
                    pass