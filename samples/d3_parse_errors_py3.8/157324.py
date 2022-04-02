# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\psutil\_psosx.py
"""macOS platform implementation."""
import contextlib, errno, functools, os
from collections import namedtuple
from . import _common
from . import _psposix
from . import _psutil_osx as cext
from . import _psutil_posix as cext_posix
from ._common import AccessDenied
from ._common import conn_tmap
from ._common import conn_to_ntuple
from ._common import isfile_strict
from ._common import memoize_when_activated
from ._common import NoSuchProcess
from ._common import parse_environ_block
from ._common import usage_percent
from ._common import ZombieProcess
from ._compat import PermissionError
from ._compat import ProcessLookupError
__extra__all__ = []
PAGESIZE = cext_posix.getpagesize()
AF_LINK = cext_posix.AF_LINK
TCP_STATUSES = {cext.TCPS_ESTABLISHED: _common.CONN_ESTABLISHED, 
 cext.TCPS_SYN_SENT: _common.CONN_SYN_SENT, 
 cext.TCPS_SYN_RECEIVED: _common.CONN_SYN_RECV, 
 cext.TCPS_FIN_WAIT_1: _common.CONN_FIN_WAIT1, 
 cext.TCPS_FIN_WAIT_2: _common.CONN_FIN_WAIT2, 
 cext.TCPS_TIME_WAIT: _common.CONN_TIME_WAIT, 
 cext.TCPS_CLOSED: _common.CONN_CLOSE, 
 cext.TCPS_CLOSE_WAIT: _common.CONN_CLOSE_WAIT, 
 cext.TCPS_LAST_ACK: _common.CONN_LAST_ACK, 
 cext.TCPS_LISTEN: _common.CONN_LISTEN, 
 cext.TCPS_CLOSING: _common.CONN_CLOSING, 
 cext.PSUTIL_CONN_NONE: _common.CONN_NONE}
PROC_STATUSES = {cext.SIDL: _common.STATUS_IDLE, 
 cext.SRUN: _common.STATUS_RUNNING, 
 cext.SSLEEP: _common.STATUS_SLEEPING, 
 cext.SSTOP: _common.STATUS_STOPPED, 
 cext.SZOMB: _common.STATUS_ZOMBIE}
kinfo_proc_map = dict(ppid=0,
  ruid=1,
  euid=2,
  suid=3,
  rgid=4,
  egid=5,
  sgid=6,
  ttynr=7,
  ctime=8,
  status=9,
  name=10)
pidtaskinfo_map = dict(cpuutime=0,
  cpustime=1,
  rss=2,
  vms=3,
  pfaults=4,
  pageins=5,
  numthreads=6,
  volctxsw=7)
scputimes = namedtuple('scputimes', ['user', 'nice', 'system', 'idle'])
svmem = namedtuple('svmem', ['total', 'available', 'percent', 'used', 'free',
 'active', 'inactive', 'wired'])
pmem = namedtuple('pmem', ['rss', 'vms', 'pfaults', 'pageins'])
pfullmem = namedtuple('pfullmem', pmem._fields + ('uss', ))

def virtual_memory():
    """System virtual memory as a namedtuple."""
    total, active, inactive, wired, free, speculative = cext.virtual_mem()
    avail = inactive + free
    used = active + wired
    free -= speculative
    percent = usage_percent((total - avail), total, round_=1)
    return svmem(total, avail, percent, used, free, active, inactive, wired)


def swap_memory():
    """Swap system memory as a (total, used, free, sin, sout) tuple."""
    total, used, free, sin, sout = cext.swap_mem()
    percent = usage_percent(used, total, round_=1)
    return _common.sswap(total, used, free, percent, sin, sout)


def cpu_times():
    """Return system CPU times as a namedtuple."""
    user, nice, system, idle = cext.cpu_times()
    return scputimes(user, nice, system, idle)


def per_cpu_times():
    """Return system CPU times as a named tuple"""
    ret = []
    for cpu_t in cext.per_cpu_times():
        user, nice, system, idle = cpu_t
        item = scputimes(user, nice, system, idle)
        ret.append(item)
    else:
        return ret


def cpu_count_logical():
    """Return the number of logical CPUs in the system."""
    return cext.cpu_count_logical()


def cpu_count_physical():
    """Return the number of physical CPUs in the system."""
    return cext.cpu_count_phys()


def cpu_stats():
    ctx_switches, interrupts, soft_interrupts, syscalls, traps = cext.cpu_stats()
    return _common.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


def cpu_freq():
    """Return CPU frequency.
    On macOS per-cpu frequency is not supported.
    Also, the returned frequency never changes, see:
    https://arstechnica.com/civis/viewtopic.php?f=19&t=465002
    """
    curr, min_, max_ = cext.cpu_freq()
    return [
     _common.scpufreq(curr, min_, max_)]


disk_usage = _psposix.disk_usage
disk_io_counters = cext.disk_io_counters

def disk_partitions--- This code section failed: ---

 L. 195         0  BUILD_LIST_0          0 
                2  STORE_FAST               'retlist'

 L. 196         4  LOAD_GLOBAL              cext
                6  LOAD_METHOD              disk_partitions
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'partitions'

 L. 197        12  LOAD_FAST                'partitions'
               14  GET_ITER         
             16_0  COME_FROM           112  '112'
             16_1  COME_FROM            72  '72'
             16_2  COME_FROM            58  '58'
               16  FOR_ITER            114  'to 114'
               18  STORE_FAST               'partition'

 L. 198        20  LOAD_FAST                'partition'
               22  UNPACK_SEQUENCE_4     4 
               24  STORE_FAST               'device'
               26  STORE_FAST               'mountpoint'
               28  STORE_FAST               'fstype'
               30  STORE_FAST               'opts'

 L. 199        32  LOAD_FAST                'device'
               34  LOAD_STR                 'none'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L. 200        40  LOAD_STR                 ''
               42  STORE_FAST               'device'
             44_0  COME_FROM            38  '38'

 L. 201        44  LOAD_FAST                'all'
               46  POP_JUMP_IF_TRUE     74  'to 74'

 L. 202        48  LOAD_GLOBAL              os
               50  LOAD_ATTR                path
               52  LOAD_METHOD              isabs
               54  LOAD_FAST                'device'
               56  CALL_METHOD_1         1  ''
               58  POP_JUMP_IF_FALSE_BACK    16  'to 16'
               60  LOAD_GLOBAL              os
               62  LOAD_ATTR                path
               64  LOAD_METHOD              exists
               66  LOAD_FAST                'device'
               68  CALL_METHOD_1         1  ''
               70  POP_JUMP_IF_TRUE     74  'to 74'

 L. 203        72  JUMP_BACK            16  'to 16'
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            46  '46'

 L. 204        74  LOAD_CONST               None
               76  DUP_TOP          
               78  STORE_FAST               'maxfile'
               80  STORE_FAST               'maxpath'

 L. 205        82  LOAD_GLOBAL              _common
               84  LOAD_METHOD              sdiskpart
               86  LOAD_FAST                'device'
               88  LOAD_FAST                'mountpoint'
               90  LOAD_FAST                'fstype'
               92  LOAD_FAST                'opts'

 L. 206        94  LOAD_FAST                'maxfile'

 L. 206        96  LOAD_FAST                'maxpath'

 L. 205        98  CALL_METHOD_6         6  ''
              100  STORE_FAST               'ntuple'

 L. 207       102  LOAD_FAST                'retlist'
              104  LOAD_METHOD              append
              106  LOAD_FAST                'ntuple'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
              112  JUMP_BACK            16  'to 16'
            114_0  COME_FROM            16  '16'

 L. 208       114  LOAD_FAST                'retlist'
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 114


def sensors_battery():
    """Return battery information."""
    try:
        percent, minsleft, power_plugged = cext.sensors_battery()
    except NotImplementedError:
        return
    else:
        power_plugged = power_plugged == 1
        if power_plugged:
            secsleft = _common.POWER_TIME_UNLIMITED
        elif minsleft == -1:
            secsleft = _common.POWER_TIME_UNKNOWN
        else:
            secsleft = minsleft * 60
        return _common.sbattery(percent, secsleft, power_plugged)


net_io_counters = cext.net_io_counters
net_if_addrs = cext_posix.net_if_addrs

def net_connections--- This code section failed: ---

 L. 246         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ret'

 L. 247         4  LOAD_GLOBAL              pids
                6  CALL_FUNCTION_0       0  ''
                8  GET_ITER         
             10_0  COME_FROM           102  '102'
             10_1  COME_FROM            60  '60'
             10_2  COME_FROM            54  '54'
             10_3  COME_FROM            50  '50'
               10  FOR_ITER            104  'to 104'
               12  STORE_FAST               'pid'

 L. 248        14  SETUP_FINALLY        34  'to 34'

 L. 249        16  LOAD_GLOBAL              Process
               18  LOAD_FAST                'pid'
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_METHOD              connections
               24  LOAD_FAST                'kind'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'cons'
               30  POP_BLOCK        
               32  JUMP_FORWARD         58  'to 58'
             34_0  COME_FROM_FINALLY    14  '14'

 L. 250        34  DUP_TOP          
               36  LOAD_GLOBAL              NoSuchProcess
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    56  'to 56'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 251        48  POP_EXCEPT       
               50  JUMP_BACK            10  'to 10'
               52  POP_EXCEPT       
               54  JUMP_BACK            10  'to 10'
             56_0  COME_FROM            40  '40'
               56  END_FINALLY      
             58_0  COME_FROM            32  '32'

 L. 253        58  LOAD_FAST                'cons'
               60  POP_JUMP_IF_FALSE_BACK    10  'to 10'

 L. 254        62  LOAD_FAST                'cons'
               64  GET_ITER         
             66_0  COME_FROM           100  '100'
               66  FOR_ITER            102  'to 102'
               68  STORE_FAST               'c'

 L. 255        70  LOAD_GLOBAL              list
               72  LOAD_FAST                'c'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_FAST                'pid'
               78  BUILD_LIST_1          1 
               80  BINARY_ADD       
               82  STORE_FAST               'c'

 L. 256        84  LOAD_FAST                'ret'
               86  LOAD_METHOD              append
               88  LOAD_GLOBAL              _common
               90  LOAD_ATTR                sconn
               92  LOAD_FAST                'c'
               94  CALL_FUNCTION_EX      0  'positional arguments only'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  JUMP_BACK            66  'to 66'
            102_0  COME_FROM            66  '66'
              102  JUMP_BACK            10  'to 10'
            104_0  COME_FROM            10  '10'

 L. 257       104  LOAD_FAST                'ret'
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 54


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    names = net_io_counters.keys()
    ret = {}
    for name in names:
        try:
            mtu = cext_posix.net_if_mtu(name)
            isup = cext_posix.net_if_is_running(name)
            duplex, speed = cext_posix.net_if_duplex_speed(name)
        except OSError as err:
            try:
                if err.errno != errno.ENODEV:
                    raise
            finally:
                err = None
                del err

        else:
            if hasattr(_common, 'NicDuplex'):
                duplex = _common.NicDuplex(duplex)
            ret[name] = _common.snicstats(isup, duplex, speed, mtu)
    else:
        return ret


def boot_time():
    """The system boot time expressed in seconds since the epoch."""
    return cext.boot_time()


def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    for item in rawlist:
        user, tty, hostname, tstamp, pid = item
        if tty == '~':
            pass
        else:
            if not tstamp:
                pass
            else:
                nt = _common.suser(user, tty or None, hostname or None, tstamp, pid)
                retlist.append(nt)
    else:
        return retlist


def pids():
    ls = cext.pids()
    if 0 not in ls:
        try:
            Process(0).create_time()
            ls.insert(0, 0)
        except NoSuchProcess:
            pass
        except AccessDenied:
            ls.insert(0, 0)

        return ls


pid_exists = _psposix.pid_exists

def is_zombie--- This code section failed: ---

 L. 330         0  SETUP_FINALLY        32  'to 32'

 L. 331         2  LOAD_GLOBAL              cext
                4  LOAD_METHOD              proc_kinfo_oneshot
                6  LOAD_FAST                'pid'
                8  CALL_METHOD_1         1  ''
               10  LOAD_GLOBAL              kinfo_proc_map
               12  LOAD_STR                 'status'
               14  BINARY_SUBSCR    
               16  BINARY_SUBSCR    
               18  STORE_FAST               'st'

 L. 332        20  LOAD_FAST                'st'
               22  LOAD_GLOBAL              cext
               24  LOAD_ATTR                SZOMB
               26  COMPARE_OP               ==
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     0  '0'

 L. 333        32  DUP_TOP          
               34  LOAD_GLOBAL              Exception
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    52  'to 52'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 334        46  POP_EXCEPT       
               48  LOAD_CONST               False
               50  RETURN_VALUE     
             52_0  COME_FROM            38  '38'
               52  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 48


def wrap_exceptions(fun):
    """Decorator which translates bare OSError exceptions into
    NoSuchProcess and AccessDenied.
    """

    @functools.wraps(fun)
    def wrapper--- This code section failed: ---

 L. 343         0  SETUP_FINALLY        20  'to 20'

 L. 344         2  LOAD_DEREF               'fun'
                4  LOAD_FAST                'self'
                6  BUILD_TUPLE_1         1 
                8  LOAD_FAST                'args'
               10  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               12  LOAD_FAST                'kwargs'
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 345        20  DUP_TOP          
               22  LOAD_GLOBAL              ProcessLookupError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    82  'to 82'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 346        34  LOAD_GLOBAL              is_zombie
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                pid
               40  CALL_FUNCTION_1       1  ''
               42  POP_JUMP_IF_FALSE    64  'to 64'

 L. 347        44  LOAD_GLOBAL              ZombieProcess
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                pid
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _name
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _ppid
               58  CALL_FUNCTION_3       3  ''
               60  RAISE_VARARGS_1       1  'exception instance'
               62  JUMP_FORWARD         78  'to 78'
             64_0  COME_FROM            42  '42'

 L. 349        64  LOAD_GLOBAL              NoSuchProcess
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                pid
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _name
               74  CALL_FUNCTION_2       2  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            62  '62'
               78  POP_EXCEPT       
               80  JUMP_FORWARD        154  'to 154'
             82_0  COME_FROM            26  '26'

 L. 350        82  DUP_TOP          
               84  LOAD_GLOBAL              PermissionError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   114  'to 114'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 351        96  LOAD_GLOBAL              AccessDenied
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                pid
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                _name
              106  CALL_FUNCTION_2       2  ''
              108  RAISE_VARARGS_1       1  'exception instance'
              110  POP_EXCEPT       
              112  JUMP_FORWARD        154  'to 154'
            114_0  COME_FROM            88  '88'

 L. 352       114  DUP_TOP          
              116  LOAD_GLOBAL              cext
              118  LOAD_ATTR                ZombieProcessError
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   152  'to 152'
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          

 L. 353       130  LOAD_GLOBAL              ZombieProcess
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                pid
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _name
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                _ppid
              144  CALL_FUNCTION_3       3  ''
              146  RAISE_VARARGS_1       1  'exception instance'
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
            152_0  COME_FROM           122  '122'
              152  END_FINALLY      
            154_0  COME_FROM           150  '150'
            154_1  COME_FROM           112  '112'
            154_2  COME_FROM            80  '80'

Parse error at or near `DUP_TOP' instruction at offset 82

    return wrapper


@contextlib.contextmanager
def catch_zombie(proc):
    """There are some poor C APIs which incorrectly raise ESRCH when
    the process is still alive or it's a zombie, or even RuntimeError
    (those who don't set errno). This is here in order to solve:
    https://github.com/giampaolo/psutil/issues/1044
    """
    try:
        yield
    except (OSError, RuntimeError) as err:
        try:
            if isinstance(err, RuntimeError) or err.errno == errno.ESRCH:
                try:
                    status = proc.status()
                except NoSuchProcess:
                    raise err
                else:
                    if status == _common.STATUS_ZOMBIE:
                        raise ZombieProcess(proc.pid, proc._name, proc._ppid)
                    else:
                        raise AccessDenied(proc.pid, proc._name)
            else:
                raise
        finally:
            err = None
            del err


class Process(object):
    __doc__ = 'Wrapper class around underlying C implementation.'
    __slots__ = [
     'pid', '_name', '_ppid', '_cache']

    def __init__(self, pid):
        self.pid = pid
        self._name = None
        self._ppid = None

    @wrap_exceptions
    @memoize_when_activated
    def _get_kinfo_proc(self):
        ret = cext.proc_kinfo_oneshot(self.pid)
        assert len(ret) == len(kinfo_proc_map)
        return ret

    @wrap_exceptions
    @memoize_when_activated
    def _get_pidtaskinfo(self):
        with catch_zombie(self):
            ret = cext.proc_pidtaskinfo_oneshot(self.pid)
        assert len(ret) == len(pidtaskinfo_map)
        return ret

    def oneshot_enter(self):
        self._get_kinfo_proc.cache_activate(self)
        self._get_pidtaskinfo.cache_activate(self)

    def oneshot_exit(self):
        self._get_kinfo_proc.cache_deactivate(self)
        self._get_pidtaskinfo.cache_deactivate(self)

    @wrap_exceptions
    def name(self):
        name = self._get_kinfo_proc()[kinfo_proc_map['name']]
        if name is not None:
            return name
        return cext.proc_name(self.pid)

    @wrap_exceptions
    def exe(self):
        with catch_zombie(self):
            return cext.proc_exe(self.pid)

    @wrap_exceptions
    def cmdline(self):
        with catch_zombie(self):
            return cext.proc_cmdline(self.pid)

    @wrap_exceptions
    def environ(self):
        with catch_zombie(self):
            return parse_environ_block(cext.proc_environ(self.pid))

    @wrap_exceptions
    def ppid(self):
        self._ppid = self._get_kinfo_proc()[kinfo_proc_map['ppid']]
        return self._ppid

    @wrap_exceptions
    def cwd(self):
        with catch_zombie(self):
            return cext.proc_cwd(self.pid)

    @wrap_exceptions
    def uids(self):
        rawtuple = self._get_kinfo_proc()
        return _common.puids(rawtuple[kinfo_proc_map['ruid']], rawtuple[kinfo_proc_map['euid']], rawtuple[kinfo_proc_map['suid']])

    @wrap_exceptions
    def gids(self):
        rawtuple = self._get_kinfo_proc()
        return _common.puids(rawtuple[kinfo_proc_map['rgid']], rawtuple[kinfo_proc_map['egid']], rawtuple[kinfo_proc_map['sgid']])

    @wrap_exceptions
    def terminal--- This code section failed: ---

 L. 466         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_kinfo_proc
                4  CALL_METHOD_0         0  ''
                6  LOAD_GLOBAL              kinfo_proc_map
                8  LOAD_STR                 'ttynr'
               10  BINARY_SUBSCR    
               12  BINARY_SUBSCR    
               14  STORE_FAST               'tty_nr'

 L. 467        16  LOAD_GLOBAL              _psposix
               18  LOAD_METHOD              get_terminal_map
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'tmap'

 L. 468        24  SETUP_FINALLY        36  'to 36'

 L. 469        26  LOAD_FAST                'tmap'
               28  LOAD_FAST                'tty_nr'
               30  BINARY_SUBSCR    
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    24  '24'

 L. 470        36  DUP_TOP          
               38  LOAD_GLOBAL              KeyError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    56  'to 56'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 471        50  POP_EXCEPT       
               52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            42  '42'
               56  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 52

    @wrap_exceptions
    def memory_info(self):
        rawtuple = self._get_pidtaskinfo()
        return pmem(rawtuple[pidtaskinfo_map['rss']], rawtuple[pidtaskinfo_map['vms']], rawtuple[pidtaskinfo_map['pfaults']], rawtuple[pidtaskinfo_map['pageins']])

    @wrap_exceptions
    def memory_full_info(self):
        basic_mem = self.memory_info()
        uss = cext.proc_memory_uss(self.pid)
        return pfullmem(*basic_mem + (uss,))

    @wrap_exceptions
    def cpu_times(self):
        rawtuple = self._get_pidtaskinfo()
        return _common.pcputimes(rawtuple[pidtaskinfo_map['cpuutime']], rawtuple[pidtaskinfo_map['cpustime']], 0.0, 0.0)

    @wrap_exceptions
    def create_time(self):
        return self._get_kinfo_proc()[kinfo_proc_map['ctime']]

    @wrap_exceptions
    def num_ctx_switches(self):
        vol = self._get_pidtaskinfo()[pidtaskinfo_map['volctxsw']]
        return _common.pctxsw(vol, 0)

    @wrap_exceptions
    def num_threads(self):
        return self._get_pidtaskinfo()[pidtaskinfo_map['numthreads']]

    @wrap_exceptions
    def open_files(self):
        if self.pid == 0:
            return []
        files = []
        with catch_zombie(self):
            rawlist = cext.proc_open_files(self.pid)
        for path, fd in rawlist:
            if isfile_strict(path):
                ntuple = _common.popenfile(path, fd)
                files.append(ntuple)
        else:
            return files

    @wrap_exceptions
    def connections(self, kind='inet'):
        if kind not in conn_tmap:
            raise ValueError('invalid %r kind argument; choose between %s' % (
             kind, ', '.join([repr(x) for x in conn_tmap])))
        families, types = conn_tmap[kind]
        with catch_zombie(self):
            rawlist = cext.proc_connections(self.pid, families, types)
        ret = []
        for item in rawlist:
            fd, fam, type, laddr, raddr, status = item
            nt = conn_to_ntuple(fd, fam, type, laddr, raddr, status, TCP_STATUSES)
            ret.append(nt)
        else:
            return ret

    @wrap_exceptions
    def num_fds(self):
        if self.pid == 0:
            return 0
        with catch_zombie(self):
            return cext.proc_num_fds(self.pid)

    @wrap_exceptions
    def wait(self, timeout=None):
        return _psposix.wait_pid(self.pid, timeout, self._name)

    @wrap_exceptions
    def nice_get(self):
        with catch_zombie(self):
            return cext_posix.getpriority(self.pid)

    @wrap_exceptions
    def nice_set(self, value):
        with catch_zombie(self):
            return cext_posix.setpriority(self.pid, value)

    @wrap_exceptions
    def status(self):
        code = self._get_kinfo_proc()[kinfo_proc_map['status']]
        return PROC_STATUSES.get(code, '?')

    @wrap_exceptions
    def threads(self):
        rawlist = cext.proc_threads(self.pid)
        retlist = []
        for thread_id, utime, stime in rawlist:
            ntuple = _common.pthread(thread_id, utime, stime)
            retlist.append(ntuple)
        else:
            return retlist