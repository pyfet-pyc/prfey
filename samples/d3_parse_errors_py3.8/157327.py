# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\psutil\_pswindows.py
"""Windows platform implementation."""
import contextlib, errno, functools, os, signal, sys, time
from collections import namedtuple
from . import _common
from ._common import AccessDenied
from ._common import conn_tmap
from ._common import conn_to_ntuple
from ._common import debug
from ._common import ENCODING
from ._common import ENCODING_ERRS
from ._common import isfile_strict
from ._common import memoize
from ._common import memoize_when_activated
from ._common import NoSuchProcess
from ._common import parse_environ_block
from ._common import TimeoutExpired
from ._common import usage_percent
from ._compat import long
from ._compat import lru_cache
from ._compat import PY3
from ._compat import range
from ._compat import unicode
from ._psutil_windows import ABOVE_NORMAL_PRIORITY_CLASS
from ._psutil_windows import BELOW_NORMAL_PRIORITY_CLASS
from ._psutil_windows import HIGH_PRIORITY_CLASS
from ._psutil_windows import IDLE_PRIORITY_CLASS
from ._psutil_windows import NORMAL_PRIORITY_CLASS
from ._psutil_windows import REALTIME_PRIORITY_CLASS
try:
    from . import _psutil_windows as cext
except ImportError as err:
    try:
        if str(err).lower().startswith('dll load failed') and sys.getwindowsversion()[0] < 6:
            msg = 'this Windows version is too old (< Windows Vista); '
            msg += 'psutil 3.4.2 is the latest version which supports Windows '
            msg += '2000, XP and 2003 server'
            raise RuntimeError(msg)
        else:
            raise
    finally:
        err = None
        del err

else:
    if sys.version_info >= (3, 4):
        import enum
    else:
        enum = None
    __extra__all__ = [
     'win_service_iter', 'win_service_get',
     'ABOVE_NORMAL_PRIORITY_CLASS', 'BELOW_NORMAL_PRIORITY_CLASS',
     'HIGH_PRIORITY_CLASS', 'IDLE_PRIORITY_CLASS', 'NORMAL_PRIORITY_CLASS',
     'REALTIME_PRIORITY_CLASS',
     'IOPRIO_VERYLOW', 'IOPRIO_LOW', 'IOPRIO_NORMAL', 'IOPRIO_HIGH',
     'CONN_DELETE_TCB', 'AF_LINK']
    CONN_DELETE_TCB = 'DELETE_TCB'
    ERROR_PARTIAL_COPY = 299
    PYPY = '__pypy__' in sys.builtin_module_names
    if enum is None:
        AF_LINK = -1
    else:
        AddressFamily = enum.IntEnum('AddressFamily', {'AF_LINK': -1})
        AF_LINK = AddressFamily.AF_LINK
    TCP_STATUSES = {cext.MIB_TCP_STATE_ESTAB: _common.CONN_ESTABLISHED, 
     cext.MIB_TCP_STATE_SYN_SENT: _common.CONN_SYN_SENT, 
     cext.MIB_TCP_STATE_SYN_RCVD: _common.CONN_SYN_RECV, 
     cext.MIB_TCP_STATE_FIN_WAIT1: _common.CONN_FIN_WAIT1, 
     cext.MIB_TCP_STATE_FIN_WAIT2: _common.CONN_FIN_WAIT2, 
     cext.MIB_TCP_STATE_TIME_WAIT: _common.CONN_TIME_WAIT, 
     cext.MIB_TCP_STATE_CLOSED: _common.CONN_CLOSE, 
     cext.MIB_TCP_STATE_CLOSE_WAIT: _common.CONN_CLOSE_WAIT, 
     cext.MIB_TCP_STATE_LAST_ACK: _common.CONN_LAST_ACK, 
     cext.MIB_TCP_STATE_LISTEN: _common.CONN_LISTEN, 
     cext.MIB_TCP_STATE_CLOSING: _common.CONN_CLOSING, 
     cext.MIB_TCP_STATE_DELETE_TCB: CONN_DELETE_TCB, 
     cext.PSUTIL_CONN_NONE: _common.CONN_NONE}
    if enum is not None:

        class Priority(enum.IntEnum):
            ABOVE_NORMAL_PRIORITY_CLASS = ABOVE_NORMAL_PRIORITY_CLASS
            BELOW_NORMAL_PRIORITY_CLASS = BELOW_NORMAL_PRIORITY_CLASS
            HIGH_PRIORITY_CLASS = HIGH_PRIORITY_CLASS
            IDLE_PRIORITY_CLASS = IDLE_PRIORITY_CLASS
            NORMAL_PRIORITY_CLASS = NORMAL_PRIORITY_CLASS
            REALTIME_PRIORITY_CLASS = REALTIME_PRIORITY_CLASS


        globals().update(Priority.__members__)
    if enum is None:
        IOPRIO_VERYLOW = 0
        IOPRIO_LOW = 1
        IOPRIO_NORMAL = 2
        IOPRIO_HIGH = 3
    else:

        class IOPriority(enum.IntEnum):
            IOPRIO_VERYLOW = 0
            IOPRIO_LOW = 1
            IOPRIO_NORMAL = 2
            IOPRIO_HIGH = 3


        globals().update(IOPriority.__members__)
    pinfo_map = dict(num_handles=0,
      ctx_switches=1,
      user_time=2,
      kernel_time=3,
      create_time=4,
      num_threads=5,
      io_rcount=6,
      io_wcount=7,
      io_rbytes=8,
      io_wbytes=9,
      io_count_others=10,
      io_bytes_others=11,
      num_page_faults=12,
      peak_wset=13,
      wset=14,
      peak_paged_pool=15,
      paged_pool=16,
      peak_non_paged_pool=17,
      non_paged_pool=18,
      pagefile=19,
      peak_pagefile=20,
      mem_private=21)
    scputimes = namedtuple('scputimes', [
     'user', 'system', 'idle', 'interrupt', 'dpc'])
    svmem = namedtuple('svmem', ['total', 'available', 'percent', 'used', 'free'])
    pmem = namedtuple('pmem', ['rss', 'vms',
     'num_page_faults', 'peak_wset', 'wset', 'peak_paged_pool',
     'paged_pool', 'peak_nonpaged_pool', 'nonpaged_pool',
     'pagefile', 'peak_pagefile', 'private'])
    pfullmem = namedtuple('pfullmem', pmem._fields + ('uss', ))
    pmmap_grouped = namedtuple('pmmap_grouped', ['path', 'rss'])
    pmmap_ext = namedtuple('pmmap_ext', 'addr perms ' + ' '.join(pmmap_grouped._fields))
    pio = namedtuple('pio', ['read_count', 'write_count',
     'read_bytes', 'write_bytes',
     'other_count', 'other_bytes'])

    @lru_cache(maxsize=512)
    def convert_dos_path(s):
        r"""Convert paths using native DOS format like:
        "\Device\HarddiskVolume1\Windows\systemew\file.txt"
    into:
        "C:\Windows\systemew\file.txt"
    """
        rawdrive = '\\'.join(s.split('\\')[:3])
        driveletter = cext.win32_QueryDosDevice(rawdrive)
        remainder = s[len(rawdrive):]
        return os.path.join(driveletter, remainder)


    def py2_strencode(s):
        """Encode a unicode string to a byte string by using the default fs
    encoding + "replace" error handler.
    """
        if PY3:
            return s
        if isinstance(s, str):
            return s
        return s.encode(ENCODING, ENCODING_ERRS)


    @memoize
    def getpagesize():
        return cext.getpagesize()


    def virtual_memory():
        """System virtual memory as a namedtuple."""
        mem = cext.virtual_mem()
        totphys, availphys, totpagef, availpagef, totvirt, freevirt = mem
        total = totphys
        avail = availphys
        free = availphys
        used = total - avail
        percent = usage_percent((total - avail), total, round_=1)
        return svmem(total, avail, percent, used, free)


    def swap_memory():
        """Swap system memory as a (total, used, free, sin, sout) tuple."""
        mem = cext.virtual_mem()
        total = mem[2]
        free = mem[3]
        used = total - free
        percent = usage_percent(used, total, round_=1)
        return _common.sswap(total, used, free, percent, 0, 0)


    disk_io_counters = cext.disk_io_counters

    def disk_usage(path):
        """Return disk usage associated with path."""
        if PY3:
            if isinstance(path, bytes):
                path = path.decode(ENCODING, errors='strict')
        total, free = cext.disk_usage(path)
        used = total - free
        percent = usage_percent(used, total, round_=1)
        return _common.sdiskusage(total, used, free, percent)


    def disk_partitions(all):
        """Return disk partitions."""
        rawlist = cext.disk_partitions(all)
        return [(_common.sdiskpart)(*x) for x in rawlist]


    def cpu_times():
        """Return system CPU times as a named tuple."""
        user, system, idle = cext.cpu_times()
        percpu_summed = scputimes(*[sum(n) for n in zip(*cext.per_cpu_times())])
        return scputimes(user, system, idle, percpu_summed.interrupt, percpu_summed.dpc)


    def per_cpu_times():
        """Return system per-CPU times as a list of named tuples."""
        ret = []
        for user, system, idle, interrupt, dpc in cext.per_cpu_times():
            item = scputimes(user, system, idle, interrupt, dpc)
            ret.append(item)
        else:
            return ret


    def cpu_count_logical():
        """Return the number of logical CPUs in the system."""
        return cext.cpu_count_logical()


    def cpu_count_physical():
        """Return the number of physical CPU cores in the system."""
        return cext.cpu_count_phys()


    def cpu_stats():
        """Return CPU statistics."""
        ctx_switches, interrupts, dpcs, syscalls = cext.cpu_stats()
        soft_interrupts = 0
        return _common.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


    def cpu_freq():
        """Return CPU frequency.
    On Windows per-cpu frequency is not supported.
    """
        curr, max_ = cext.cpu_freq()
        min_ = 0.0
        return [
         _common.scpufreq(float(curr), min_, float(max_))]


    _loadavg_inititialized = False

    def getloadavg():
        """Return the number of processes in the system run queue averaged
    over the last 1, 5, and 15 minutes respectively as a tuple"""
        global _loadavg_inititialized
        if not _loadavg_inititialized:
            cext.init_loadavg_counter()
            _loadavg_inititialized = True
        raw_loads = cext.getloadavg()
        return tuple([round(load, 2) for load in raw_loads])


    def net_connections(kind, _pid=-1):
        """Return socket connections.  If pid == -1 return system-wide
    connections (as opposed to connections opened by one process only).
    """
        if kind not in conn_tmap:
            raise ValueError('invalid %r kind argument; choose between %s' % (
             kind, ', '.join([repr(x) for x in conn_tmap])))
        families, types = conn_tmap[kind]
        rawlist = cext.net_connections(_pid, families, types)
        ret = set()
        for item in rawlist:
            fd, fam, type, laddr, raddr, status, pid = item
            nt = conn_to_ntuple(fd, fam, type, laddr, raddr, status, TCP_STATUSES, pid=(pid if _pid == -1 else None))
            ret.add(nt)
        else:
            return list(ret)


    def net_if_stats():
        """Get NIC stats (isup, duplex, speed, mtu)."""
        ret = {}
        rawdict = cext.net_if_stats()
        for name, items in rawdict.items():
            if not PY3:
                if not isinstance(name, unicode):
                    raise AssertionError(type(name))
                else:
                    name = py2_strencode(name)
            else:
                isup, duplex, speed, mtu = items
                if hasattr(_common, 'NicDuplex'):
                    duplex = _common.NicDuplex(duplex)
                ret[name] = _common.snicstats(isup, duplex, speed, mtu)
        else:
            return ret


    def net_io_counters():
        """Return network I/O statistics for every network interface
    installed on the system as a dict of raw tuples.
    """
        ret = cext.net_io_counters()
        return dict([(py2_strencode(k), v) for k, v in ret.items()])


    def net_if_addrs():
        """Return the addresses associated to each NIC."""
        ret = []
        for items in cext.net_if_addrs():
            items = list(items)
            items[0] = py2_strencode(items[0])
            ret.append(items)
        else:
            return ret


    def sensors_battery():
        """Return battery information."""
        acline_status, flags, percent, secsleft = cext.sensors_battery()
        power_plugged = acline_status == 1
        no_battery = bool(flags & 128)
        charging = bool(flags & 8)
        if no_battery:
            return
        if power_plugged or charging:
            secsleft = _common.POWER_TIME_UNLIMITED
        elif secsleft == -1:
            secsleft = _common.POWER_TIME_UNKNOWN
        return _common.sbattery(percent, secsleft, power_plugged)


    _last_btime = 0

    def boot_time():
        """The system boot time expressed in seconds since the epoch."""
        global _last_btime
        ret = float(cext.boot_time())
        if abs(ret - _last_btime) <= 1:
            return _last_btime
        _last_btime = ret
        return ret


    def users():
        """Return currently connected users as a list of namedtuples."""
        retlist = []
        rawlist = cext.users()
        for item in rawlist:
            user, hostname, tstamp = item
            user = py2_strencode(user)
            nt = _common.suser(user, None, hostname, tstamp, None)
            retlist.append(nt)
        else:
            return retlist


    def win_service_iter():
        """Yields a list of WindowsService instances."""
        for name, display_name in cext.winservice_enumerate():
            yield WindowsService(py2_strencode(name), py2_strencode(display_name))


    def win_service_get(name):
        """Open a Windows service and return it as a WindowsService instance."""
        service = WindowsService(name, None)
        service._display_name = service._query_config()['display_name']
        return service


    class WindowsService(object):
        __doc__ = 'Represents an installed Windows service.'

        def __init__(self, name, display_name):
            self._name = name
            self._display_name = display_name

        def __str__(self):
            details = '(name=%r, display_name=%r)' % (
             self._name, self._display_name)
            return '%s%s' % (self.__class__.__name__, details)

        def __repr__(self):
            return '<%s at %s>' % (self.__str__(), id(self))

        def __eq__(self, other):
            if not isinstance(other, WindowsService):
                return NotImplemented
            return self._name == other._name

        def __ne__(self, other):
            return not self == other

        def _query_config(self):
            with self._wrap_exceptions():
                display_name, binpath, username, start_type = cext.winservice_query_config(self._name)
            return dict(display_name=(py2_strencode(display_name)),
              binpath=(py2_strencode(binpath)),
              username=(py2_strencode(username)),
              start_type=(py2_strencode(start_type)))

        def _query_status(self):
            with self._wrap_exceptions():
                status, pid = cext.winservice_query_status(self._name)
            if pid == 0:
                pid = None
            return dict(status=status, pid=pid)

        @contextlib.contextmanager
        def _wrap_exceptions(self):
            """Ctx manager which translates bare OSError and WindowsError
        exceptions into NoSuchProcess and AccessDenied.
        """
            try:
                yield
            except OSError as err:
                try:
                    if is_permission_err(err):
                        raise AccessDenied(pid=None,
                          name=(self._name),
                          msg=('service %r is not querable (not enough privileges)' % self._name))
                    elif err.winerror in (cext.ERROR_INVALID_NAME,
                     cext.ERROR_SERVICE_DOES_NOT_EXIST):
                        raise NoSuchProcess(pid=None,
                          name=(self._name),
                          msg=('service %r does not exist)' % self._name))
                    else:
                        raise
                finally:
                    err = None
                    del err

        def name(self):
            """The service name. This string is how a service is referenced
        and can be passed to win_service_get() to get a new
        WindowsService instance.
        """
            return self._name

        def display_name(self):
            """The service display name. The value is cached when this class
        is instantiated.
        """
            return self._display_name

        def binpath(self):
            """The fully qualified path to the service binary/exe file as
        a string, including command line arguments.
        """
            return self._query_config()['binpath']

        def username(self):
            """The name of the user that owns this service."""
            return self._query_config()['username']

        def start_type(self):
            """A string which can either be "automatic", "manual" or
        "disabled".
        """
            return self._query_config()['start_type']

        def pid(self):
            """The process PID, if any, else None. This can be passed
        to Process class to control the service's process.
        """
            return self._query_status()['pid']

        def status(self):
            """Service status as a string."""
            return self._query_status()['status']

        def description(self):
            """Service long description."""
            return py2_strencode(cext.winservice_query_descr(self.name()))

        def as_dict(self):
            """Utility method retrieving all the information above as a
        dictionary.
        """
            d = self._query_config()
            d.update(self._query_status())
            d['name'] = self.name()
            d['display_name'] = self.display_name()
            d['description'] = self.description()
            return d


    pids = cext.pids
    pid_exists = cext.pid_exists
    ppid_map = cext.ppid_map

    def is_permission_err(exc):
        """Return True if this is a permission error."""
        assert isinstance(exc, OSError), exc
        return exc.errno in (errno.EPERM, errno.EACCES) or getattr(exc, 'winerror', -1) in (cext.ERROR_ACCESS_DENIED,
         cext.ERROR_PRIVILEGE_NOT_HELD)


    def convert_oserror(exc, pid=None, name=None):
        """Convert OSError into NoSuchProcess or AccessDenied."""
        assert isinstance(exc, OSError), exc
        if is_permission_err(exc):
            return AccessDenied(pid=pid, name=name)
        if exc.errno == errno.ESRCH:
            return NoSuchProcess(pid=pid, name=name)
        raise exc


    def wrap_exceptions(fun):
        """Decorator which converts OSError into NoSuchProcess or AccessDenied."""

        @functools.wraps(fun)
        def wrapper(self, *args, **kwargs):
            try:
                return fun(self, *args, **kwargs)
                    except OSError as err:
                try:
                    raise convert_oserror(err, pid=(self.pid), name=(self._name))
                finally:
                    err = None
                    del err

        return wrapper


    def retry_error_partial_copy(fun):
        """Workaround for https://github.com/giampaolo/psutil/issues/875.
    See: https://stackoverflow.com/questions/4457745#4457745
    """

        @functools.wraps(fun)
        def wrapper--- This code section failed: ---

 L. 691         0  LOAD_CONST               0.0001
                2  STORE_FAST               'delay'

 L. 692         4  LOAD_CONST               33
                6  STORE_FAST               'times'

 L. 693         8  LOAD_GLOBAL              range
               10  LOAD_FAST                'times'
               12  CALL_FUNCTION_1       1  ''
               14  GET_ITER         
             16_0  COME_FROM           128  '128'
             16_1  COME_FROM           124  '124'
             16_2  COME_FROM           104  '104'
               16  FOR_ITER            130  'to 130'
               18  STORE_FAST               'x'

 L. 694        20  SETUP_FINALLY        44  'to 44'

 L. 695        22  LOAD_DEREF               'fun'
               24  LOAD_FAST                'self'
               26  BUILD_TUPLE_1         1 
               28  LOAD_FAST                'args'
               30  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               32  LOAD_FAST                'kwargs'
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  POP_BLOCK        
               38  ROT_TWO          
               40  POP_TOP          
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    20  '20'

 L. 696        44  DUP_TOP          
               46  LOAD_GLOBAL              WindowsError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE   126  'to 126'
               52  POP_TOP          
               54  STORE_FAST               '_'
               56  POP_TOP          
               58  SETUP_FINALLY       114  'to 114'

 L. 697        60  LOAD_FAST                '_'
               62  STORE_FAST               'err'

 L. 698        64  LOAD_FAST                'err'
               66  LOAD_ATTR                winerror
               68  LOAD_GLOBAL              ERROR_PARTIAL_COPY
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE   108  'to 108'

 L. 699        74  LOAD_GLOBAL              time
               76  LOAD_METHOD              sleep
               78  LOAD_FAST                'delay'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 700        84  LOAD_GLOBAL              min
               86  LOAD_FAST                'delay'
               88  LOAD_CONST               2
               90  BINARY_MULTIPLY  
               92  LOAD_CONST               0.04
               94  CALL_FUNCTION_2       2  ''
               96  STORE_FAST               'delay'

 L. 701        98  POP_BLOCK        
              100  POP_EXCEPT       
              102  CALL_FINALLY        114  'to 114'
              104  JUMP_BACK            16  'to 16'
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            72  '72'

 L. 703       108  RAISE_VARARGS_0       0  'reraise'
            110_0  COME_FROM           106  '106'
              110  POP_BLOCK        
              112  BEGIN_FINALLY    
            114_0  COME_FROM           102  '102'
            114_1  COME_FROM_FINALLY    58  '58'
              114  LOAD_CONST               None
              116  STORE_FAST               '_'
              118  DELETE_FAST              '_'
              120  END_FINALLY      
              122  POP_EXCEPT       
              124  JUMP_BACK            16  'to 16'
            126_0  COME_FROM            50  '50'
              126  END_FINALLY      
              128  JUMP_BACK            16  'to 16'
            130_0  COME_FROM            16  '16'

 L. 705       130  LOAD_STR                 "%s retried %s times, converted to AccessDenied as it's still returning %r"

 L. 706       132  LOAD_DEREF               'fun'
              134  LOAD_FAST                'times'
              136  LOAD_FAST                'err'
              138  BUILD_TUPLE_3         3 

 L. 705       140  BINARY_MODULO    
              142  STORE_FAST               'msg'

 L. 707       144  LOAD_GLOBAL              AccessDenied
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                pid
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                _name
              154  LOAD_FAST                'msg'
              156  LOAD_CONST               ('pid', 'name', 'msg')
              158  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              160  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 40

        return wrapper


    class Process(object):
        __doc__ = 'Wrapper class around underlying C implementation.'
        __slots__ = [
         'pid', '_name', '_ppid', '_cache']

        def __init__(self, pid):
            self.pid = pid
            self._name = None
            self._ppid = None

        def oneshot_enter(self):
            self._proc_info.cache_activate(self)
            self.exe.cache_activate(self)

        def oneshot_exit(self):
            self._proc_info.cache_deactivate(self)
            self.exe.cache_deactivate(self)

        @memoize_when_activated
        def _proc_info(self):
            """Return multiple information about this process as a
        raw tuple.
        """
            ret = cext.proc_info(self.pid)
            assert len(ret) == len(pinfo_map)
            return ret

        def name(self):
            """Return process name, which on Windows is always the final
        part of the executable.
        """
            if self.pid == 0:
                return 'System Idle Process'
            if self.pid == 4:
                return 'System'
            return os.path.basename(self.exe())

        @wrap_exceptions
        @memoize_when_activated
        def exe(self):
            if PYPY:
                try:
                    exe = cext.proc_exe(self.pid)
                except WindowsError as err:
                    try:
                        if err.errno == 24:
                            debug('%r forced into AccessDenied' % err)
                            raise AccessDenied(self.pid, self._name)
                        raise
                    finally:
                        err = None
                        del err

            else:
                exe = cext.proc_exe(self.pid)
            if not PY3:
                exe = py2_strencode(exe)
            if exe.startswith('\\'):
                return convert_dos_path(exe)
            return exe

        @wrap_exceptions
        @retry_error_partial_copy
        def cmdline(self):
            if cext.WINVER >= cext.WINDOWS_8_1:
                try:
                    ret = cext.proc_cmdline((self.pid), use_peb=True)
                except OSError as err:
                    try:
                        if is_permission_err(err):
                            ret = cext.proc_cmdline((self.pid), use_peb=False)
                        else:
                            raise
                    finally:
                        err = None
                        del err

            else:
                ret = cext.proc_cmdline((self.pid), use_peb=True)
            if PY3:
                return ret
            return [py2_strencode(s) for s in ret]

        @wrap_exceptions
        @retry_error_partial_copy
        def environ(self):
            ustr = cext.proc_environ(self.pid)
            if ustr:
                if not PY3:
                    assert isinstance(ustr, unicode), type(ustr)
                return parse_environ_block(py2_strencode(ustr))

        def ppid(self):
            try:
                return ppid_map()[self.pid]
            except KeyError:
                raise NoSuchProcess(self.pid, self._name)

        def _get_raw_meminfo--- This code section failed: ---

 L. 808         0  SETUP_FINALLY        16  'to 16'

 L. 809         2  LOAD_GLOBAL              cext
                4  LOAD_METHOD              proc_memory_info
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                pid
               10  CALL_METHOD_1         1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 810        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE   178  'to 178'
               24  POP_TOP          
               26  STORE_FAST               'err'
               28  POP_TOP          
               30  SETUP_FINALLY       166  'to 166'

 L. 811        32  LOAD_GLOBAL              is_permission_err
               34  LOAD_FAST                'err'
               36  CALL_FUNCTION_1       1  ''
               38  POP_JUMP_IF_FALSE   160  'to 160'

 L. 814        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _proc_info
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'info'

 L. 816        48  LOAD_FAST                'info'
               50  LOAD_GLOBAL              pinfo_map
               52  LOAD_STR                 'num_page_faults'
               54  BINARY_SUBSCR    
               56  BINARY_SUBSCR    

 L. 817        58  LOAD_FAST                'info'
               60  LOAD_GLOBAL              pinfo_map
               62  LOAD_STR                 'peak_wset'
               64  BINARY_SUBSCR    
               66  BINARY_SUBSCR    

 L. 818        68  LOAD_FAST                'info'
               70  LOAD_GLOBAL              pinfo_map
               72  LOAD_STR                 'wset'
               74  BINARY_SUBSCR    
               76  BINARY_SUBSCR    

 L. 819        78  LOAD_FAST                'info'
               80  LOAD_GLOBAL              pinfo_map
               82  LOAD_STR                 'peak_paged_pool'
               84  BINARY_SUBSCR    
               86  BINARY_SUBSCR    

 L. 820        88  LOAD_FAST                'info'
               90  LOAD_GLOBAL              pinfo_map
               92  LOAD_STR                 'paged_pool'
               94  BINARY_SUBSCR    
               96  BINARY_SUBSCR    

 L. 821        98  LOAD_FAST                'info'
              100  LOAD_GLOBAL              pinfo_map
              102  LOAD_STR                 'peak_non_paged_pool'
              104  BINARY_SUBSCR    
              106  BINARY_SUBSCR    

 L. 822       108  LOAD_FAST                'info'
              110  LOAD_GLOBAL              pinfo_map
              112  LOAD_STR                 'non_paged_pool'
              114  BINARY_SUBSCR    
              116  BINARY_SUBSCR    

 L. 823       118  LOAD_FAST                'info'
              120  LOAD_GLOBAL              pinfo_map
              122  LOAD_STR                 'pagefile'
              124  BINARY_SUBSCR    
              126  BINARY_SUBSCR    

 L. 824       128  LOAD_FAST                'info'
              130  LOAD_GLOBAL              pinfo_map
              132  LOAD_STR                 'peak_pagefile'
              134  BINARY_SUBSCR    
              136  BINARY_SUBSCR    

 L. 825       138  LOAD_FAST                'info'
              140  LOAD_GLOBAL              pinfo_map
              142  LOAD_STR                 'mem_private'
              144  BINARY_SUBSCR    
              146  BINARY_SUBSCR    

 L. 815       148  BUILD_TUPLE_10       10 
              150  ROT_FOUR         
              152  POP_BLOCK        
              154  POP_EXCEPT       
              156  CALL_FINALLY        166  'to 166'
              158  RETURN_VALUE     
            160_0  COME_FROM            38  '38'

 L. 827       160  RAISE_VARARGS_0       0  'reraise'
              162  POP_BLOCK        
              164  BEGIN_FINALLY    
            166_0  COME_FROM           156  '156'
            166_1  COME_FROM_FINALLY    30  '30'
              166  LOAD_CONST               None
              168  STORE_FAST               'err'
              170  DELETE_FAST              'err'
              172  END_FINALLY      
              174  POP_EXCEPT       
              176  JUMP_FORWARD        180  'to 180'
            178_0  COME_FROM            22  '22'
              178  END_FINALLY      
            180_0  COME_FROM           176  '176'

Parse error at or near `POP_BLOCK' instruction at offset 152

        @wrap_exceptions
        def memory_info(self):
            t = self._get_raw_meminfo()
            rss = t[2]
            vms = t[7]
            return pmem(*(rss, vms) + t)

        @wrap_exceptions
        def memory_full_info(self):
            basic_mem = self.memory_info()
            uss = cext.proc_memory_uss(self.pid)
            uss *= getpagesize()
            return pfullmem(*basic_mem + (uss,))

        def memory_maps(self):
            try:
                raw = cext.proc_memory_maps(self.pid)
            except OSError as err:
                try:
                    raise convert_oserror(err, self.pid, self._name)
                finally:
                    err = None
                    del err

            else:
                for addr, perm, path, rss in raw:
                    path = convert_dos_path(path)
                    if not PY3:
                        path = py2_strencode(path)
                    else:
                        addr = hex(addr)
                        yield (addr, perm, path, rss)

        @wrap_exceptions
        def kill(self):
            return cext.proc_kill(self.pid)

        @wrap_exceptions
        def send_signal(self, sig):
            if sig == signal.SIGTERM:
                cext.proc_kill(self.pid)
            elif sig in (getattr(signal, 'CTRL_C_EVENT', object()),
             getattr(signal, 'CTRL_BREAK_EVENT', object())):
                os.kill(self.pid, sig)
            else:
                raise ValueError('only SIGTERM, CTRL_C_EVENT and CTRL_BREAK_EVENT signals are supported on Windows')

        @wrap_exceptions
        def wait(self, timeout=None):
            if timeout is None:
                cext_timeout = cext.INFINITE
            else:
                cext_timeout = int(timeout * 1000)
            timer = getattr(time, 'monotonic', time.time)
            stop_at = timer() + timeout if timeout is not None else None
            try:
                exit_code = cext.proc_wait(self.pid, cext_timeout)
            except cext.TimeoutExpired:
                raise TimeoutExpired(timeout, self.pid, self._name)
            except cext.TimeoutAbandoned:
                exit_code = None
            else:
                delay = 0.0001
                while True:
                    if not pid_exists(self.pid):
                        return exit_code
                    else:
                        if stop_at:
                            if timer() >= stop_at:
                                raise TimeoutExpired(timeout, pid=(self.pid), name=(self._name))
                        time.sleep(delay)
                        delay = min(delay * 2, 0.04)

        @wrap_exceptions
        def username(self):
            if self.pid in (0, 4):
                return 'NT AUTHORITY\\SYSTEM'
            domain, user = cext.proc_username(self.pid)
            return py2_strencode(domain) + '\\' + py2_strencode(user)

        @wrap_exceptions
        def create_time--- This code section failed: ---

 L. 932         0  SETUP_FINALLY        26  'to 26'

 L. 933         2  LOAD_GLOBAL              cext
                4  LOAD_METHOD              proc_times
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                pid
               10  CALL_METHOD_1         1  ''
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'user'
               16  STORE_FAST               'system'
               18  STORE_FAST               'created'

 L. 934        20  LOAD_FAST                'created'
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY     0  '0'

 L. 935        26  DUP_TOP          
               28  LOAD_GLOBAL              OSError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    92  'to 92'
               34  POP_TOP          
               36  STORE_FAST               'err'
               38  POP_TOP          
               40  SETUP_FINALLY        80  'to 80'

 L. 936        42  LOAD_GLOBAL              is_permission_err
               44  LOAD_FAST                'err'
               46  CALL_FUNCTION_1       1  ''
               48  POP_JUMP_IF_FALSE    74  'to 74'

 L. 937        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _proc_info
               54  CALL_METHOD_0         0  ''
               56  LOAD_GLOBAL              pinfo_map
               58  LOAD_STR                 'create_time'
               60  BINARY_SUBSCR    
               62  BINARY_SUBSCR    
               64  ROT_FOUR         
               66  POP_BLOCK        
               68  POP_EXCEPT       
               70  CALL_FINALLY         80  'to 80'
               72  RETURN_VALUE     
             74_0  COME_FROM            48  '48'

 L. 938        74  RAISE_VARARGS_0       0  'reraise'
               76  POP_BLOCK        
               78  BEGIN_FINALLY    
             80_0  COME_FROM            70  '70'
             80_1  COME_FROM_FINALLY    40  '40'
               80  LOAD_CONST               None
               82  STORE_FAST               'err'
               84  DELETE_FAST              'err'
               86  END_FINALLY      
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
             92_0  COME_FROM            32  '32'
               92  END_FINALLY      
             94_0  COME_FROM            90  '90'

Parse error at or near `POP_BLOCK' instruction at offset 66

        @wrap_exceptions
        def num_threads(self):
            return self._proc_info()[pinfo_map['num_threads']]

        @wrap_exceptions
        def threads(self):
            rawlist = cext.proc_threads(self.pid)
            retlist = []
            for thread_id, utime, stime in rawlist:
                ntuple = _common.pthread(thread_id, utime, stime)
                retlist.append(ntuple)
            else:
                return retlist

        @wrap_exceptions
        def cpu_times(self):
            try:
                user, system, created = cext.proc_times(self.pid)
            except OSError as err:
                try:
                    if not is_permission_err(err):
                        raise
                    info = self._proc_info()
                    user = info[pinfo_map['user_time']]
                    system = info[pinfo_map['kernel_time']]
                finally:
                    err = None
                    del err

            else:
                return _common.pcputimes(user, system, 0.0, 0.0)

        @wrap_exceptions
        def suspend(self):
            cext.proc_suspend_or_resume(self.pid, True)

        @wrap_exceptions
        def resume(self):
            cext.proc_suspend_or_resume(self.pid, False)

        @wrap_exceptions
        @retry_error_partial_copy
        def cwd(self):
            if self.pid in (0, 4):
                raise AccessDenied(self.pid, self._name)
            path = cext.proc_cwd(self.pid)
            return py2_strencode(os.path.normpath(path))

        @wrap_exceptions
        def open_files(self):
            if self.pid in (0, 4):
                return []
            ret = set()
            raw_file_names = cext.proc_open_files(self.pid)
            for _file in raw_file_names:
                _file = convert_dos_path(_file)
                if isfile_strict(_file):
                    if not PY3:
                        _file = py2_strencode(_file)
                    else:
                        ntuple = _common.popenfile(_file, -1)
                        ret.add(ntuple)
            else:
                return list(ret)

        @wrap_exceptions
        def connections(self, kind='inet'):
            return net_connections(kind, _pid=(self.pid))

        @wrap_exceptions
        def nice_get(self):
            value = cext.proc_priority_get(self.pid)
            if enum is not None:
                value = Priority(value)
            return value

        @wrap_exceptions
        def nice_set(self, value):
            return cext.proc_priority_set(self.pid, value)

        @wrap_exceptions
        def ionice_get(self):
            ret = cext.proc_io_priority_get(self.pid)
            if enum is not None:
                ret = IOPriority(ret)
            return ret

        @wrap_exceptions
        def ionice_set(self, ioclass, value):
            if value:
                raise TypeError('value argument not accepted on Windows')
            if ioclass not in (IOPRIO_VERYLOW, IOPRIO_LOW, IOPRIO_NORMAL,
             IOPRIO_HIGH):
                raise ValueError('%s is not a valid priority' % ioclass)
            cext.proc_io_priority_set(self.pid, ioclass)

        @wrap_exceptions
        def io_counters(self):
            try:
                ret = cext.proc_io_counters(self.pid)
            except OSError as err:
                try:
                    if not is_permission_err(err):
                        raise
                    info = self._proc_info()
                    ret = (
                     info[pinfo_map['io_rcount']],
                     info[pinfo_map['io_wcount']],
                     info[pinfo_map['io_rbytes']],
                     info[pinfo_map['io_wbytes']],
                     info[pinfo_map['io_count_others']],
                     info[pinfo_map['io_bytes_others']])
                finally:
                    err = None
                    del err

            else:
                return pio(*ret)

        @wrap_exceptions
        def status(self):
            suspended = cext.proc_is_suspended(self.pid)
            if suspended:
                return _common.STATUS_STOPPED
            return _common.STATUS_RUNNING

        @wrap_exceptions
        def cpu_affinity_get(self):

            def from_bitmask(x):
                return [i for i in range(64) if 1 << i & x]

            bitmask = cext.proc_cpu_affinity_get(self.pid)
            return from_bitmask(bitmask)

        @wrap_exceptions
        def cpu_affinity_set(self, value):

            def to_bitmask(ls):
                if not ls:
                    raise ValueError('invalid argument %r' % ls)
                out = 0
                for b in ls:
                    out |= 2 ** b
                else:
                    return out

            allcpus = list(range(len(per_cpu_times())))
            for cpu in value:
                if cpu not in allcpus:
                    if not isinstance(cpu, (int, long)):
                        raise TypeError('invalid CPU %r; an integer is required' % cpu)
                    else:
                        raise ValueError('invalid CPU %r' % cpu)
            else:
                bitmask = to_bitmask(value)
                cext.proc_cpu_affinity_set(self.pid, bitmask)

        @wrap_exceptions
        def num_handles--- This code section failed: ---

 L.1094         0  SETUP_FINALLY        16  'to 16'

 L.1095         2  LOAD_GLOBAL              cext
                4  LOAD_METHOD              proc_num_handles
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                pid
               10  CALL_METHOD_1         1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.1096        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    82  'to 82'
               24  POP_TOP          
               26  STORE_FAST               'err'
               28  POP_TOP          
               30  SETUP_FINALLY        70  'to 70'

 L.1097        32  LOAD_GLOBAL              is_permission_err
               34  LOAD_FAST                'err'
               36  CALL_FUNCTION_1       1  ''
               38  POP_JUMP_IF_FALSE    64  'to 64'

 L.1098        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _proc_info
               44  CALL_METHOD_0         0  ''
               46  LOAD_GLOBAL              pinfo_map
               48  LOAD_STR                 'num_handles'
               50  BINARY_SUBSCR    
               52  BINARY_SUBSCR    
               54  ROT_FOUR         
               56  POP_BLOCK        
               58  POP_EXCEPT       
               60  CALL_FINALLY         70  'to 70'
               62  RETURN_VALUE     
             64_0  COME_FROM            38  '38'

 L.1099        64  RAISE_VARARGS_0       0  'reraise'
               66  POP_BLOCK        
               68  BEGIN_FINALLY    
             70_0  COME_FROM            60  '60'
             70_1  COME_FROM_FINALLY    30  '30'
               70  LOAD_CONST               None
               72  STORE_FAST               'err'
               74  DELETE_FAST              'err'
               76  END_FINALLY      
               78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
             82_0  COME_FROM            22  '22'
               82  END_FINALLY      
             84_0  COME_FROM            80  '80'

Parse error at or near `POP_BLOCK' instruction at offset 56

        @wrap_exceptions
        def num_ctx_switches(self):
            ctx_switches = self._proc_info()[pinfo_map['ctx_switches']]
            return _common.pctxsw(ctx_switches, 0)