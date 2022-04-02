# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: psutil\_psbsd.py
"""FreeBSD, OpenBSD and NetBSD platforms implementation."""
import contextlib, errno, functools, os
import xml.etree.ElementTree as ET
from collections import namedtuple
from collections import defaultdict
from . import _common
from . import _psposix
from . import _psutil_bsd as cext
from . import _psutil_posix as cext_posix
from ._common import AccessDenied
from ._common import conn_tmap
from ._common import conn_to_ntuple
from ._common import FREEBSD
from ._common import memoize
from ._common import memoize_when_activated
from ._common import NETBSD
from ._common import NoSuchProcess
from ._common import OPENBSD
from ._common import usage_percent
from ._common import ZombieProcess
from ._compat import FileNotFoundError
from ._compat import PermissionError
from ._compat import ProcessLookupError
from ._compat import which
__extra__all__ = []
if FREEBSD:
    PROC_STATUSES = {cext.SIDL: _common.STATUS_IDLE, 
     cext.SRUN: _common.STATUS_RUNNING, 
     cext.SSLEEP: _common.STATUS_SLEEPING, 
     cext.SSTOP: _common.STATUS_STOPPED, 
     cext.SZOMB: _common.STATUS_ZOMBIE, 
     cext.SWAIT: _common.STATUS_WAITING, 
     cext.SLOCK: _common.STATUS_LOCKED}
elif OPENBSD:
    PROC_STATUSES = {cext.SIDL: _common.STATUS_IDLE, 
     cext.SSLEEP: _common.STATUS_SLEEPING, 
     cext.SSTOP: _common.STATUS_STOPPED, 
     cext.SDEAD: _common.STATUS_ZOMBIE, 
     cext.SZOMB: _common.STATUS_ZOMBIE, 
     cext.SRUN: _common.STATUS_WAKING, 
     cext.SONPROC: _common.STATUS_RUNNING}
elif NETBSD:
    PROC_STATUSES = {cext.SIDL: _common.STATUS_IDLE, 
     cext.SSLEEP: _common.STATUS_SLEEPING, 
     cext.SSTOP: _common.STATUS_STOPPED, 
     cext.SZOMB: _common.STATUS_ZOMBIE, 
     cext.SRUN: _common.STATUS_WAKING, 
     cext.SONPROC: _common.STATUS_RUNNING}
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
PAGESIZE = cext_posix.getpagesize()
AF_LINK = cext_posix.AF_LINK
HAS_PER_CPU_TIMES = hasattr(cext, 'per_cpu_times')
HAS_PROC_NUM_THREADS = hasattr(cext, 'proc_num_threads')
HAS_PROC_OPEN_FILES = hasattr(cext, 'proc_open_files')
HAS_PROC_NUM_FDS = hasattr(cext, 'proc_num_fds')
kinfo_proc_map = dict(ppid=0,
  status=1,
  real_uid=2,
  effective_uid=3,
  saved_uid=4,
  real_gid=5,
  effective_gid=6,
  saved_gid=7,
  ttynr=8,
  create_time=9,
  ctx_switches_vol=10,
  ctx_switches_unvol=11,
  read_io_count=12,
  write_io_count=13,
  user_time=14,
  sys_time=15,
  ch_user_time=16,
  ch_sys_time=17,
  rss=18,
  vms=19,
  memtext=20,
  memdata=21,
  memstack=22,
  cpunum=23,
  name=24)
svmem = namedtuple('svmem', ['total', 'available', 'percent', 'used', 'free',
 'active', 'inactive', 'buffers', 'cached', 'shared', 'wired'])
scputimes = namedtuple('scputimes', ['user', 'nice', 'system', 'idle', 'irq'])
pmem = namedtuple('pmem', ['rss', 'vms', 'text', 'data', 'stack'])
pfullmem = pmem
pcputimes = namedtuple('pcputimes', [
 'user', 'system', 'children_user', 'children_system'])
pmmap_grouped = namedtuple('pmmap_grouped', 'path rss, private, ref_count, shadow_count')
pmmap_ext = namedtuple('pmmap_ext', 'addr, perms path rss, private, ref_count, shadow_count')
if FREEBSD:
    sdiskio = namedtuple('sdiskio', ['read_count', 'write_count',
     'read_bytes', 'write_bytes',
     'read_time', 'write_time',
     'busy_time'])
else:
    sdiskio = namedtuple('sdiskio', ['read_count', 'write_count',
     'read_bytes', 'write_bytes'])

def virtual_memory():
    """System virtual memory as a namedtuple."""
    mem = cext.virtual_mem()
    total, free, active, inactive, wired, cached, buffers, shared = mem
    if NETBSD:
        with open('/proc/meminfo', 'rb') as f:
            for line in f:
                if line.startswith(b'Buffers:'):
                    buffers = int(line.split()[1]) * 1024
                else:
                    if line.startswith(b'MemShared:'):
                        shared = int(line.split()[1]) * 1024

    avail = inactive + cached + free
    used = active + wired + cached
    percent = usage_percent((total - avail), total, round_=1)
    return svmem(total, avail, percent, used, free, active, inactive, buffers, cached, shared, wired)


def swap_memory():
    """System swap memory as (total, used, free, sin, sout) namedtuple."""
    total, used, free, sin, sout = cext.swap_mem()
    percent = usage_percent(used, total, round_=1)
    return _common.sswap(total, used, free, percent, sin, sout)


def cpu_times():
    """Return system per-CPU times as a namedtuple"""
    user, nice, system, idle, irq = cext.cpu_times()
    return scputimes(user, nice, system, idle, irq)


if HAS_PER_CPU_TIMES:

    def per_cpu_times():
        """Return system CPU times as a namedtuple"""
        ret = []
        for cpu_t in cext.per_cpu_times():
            user, nice, system, idle, irq = cpu_t
            item = scputimes(user, nice, system, idle, irq)
            ret.append(item)
        else:
            return ret


else:

    def per_cpu_times():
        """Return system CPU times as a namedtuple"""
        if cpu_count_logical() == 1:
            return [cpu_times()]
        if per_cpu_times.__called__:
            raise NotImplementedError('supported only starting from FreeBSD 8')
        per_cpu_times.__called__ = True
        return [
         cpu_times()]


    per_cpu_times.__called__ = False

def cpu_count_logical():
    """Return the number of logical CPUs in the system."""
    return cext.cpu_count_logical()


if OPENBSD or NETBSD:

    def cpu_count_physical():
        if cpu_count_logical() == 1:
            return 1


else:

    def cpu_count_physical():
        """Return the number of physical CPUs in the system."""
        ret = None
        s = cext.cpu_count_phys()
        if s is not None:
            index = s.rfind('</groups>')
            if index != -1:
                s = s[:index + 9]
                root = ET.fromstring(s)
                try:
                    ret = len(root.findall('group/children/group/cpu')) or None
                finally:
                    root.clear()

        if not ret:
            if cpu_count_logical() == 1:
                return 1
        return ret


def cpu_stats():
    """Return various CPU stats as a named tuple."""
    if FREEBSD:
        ctxsw, intrs, soft_intrs, syscalls, traps = cext.cpu_stats()
    elif NETBSD:
        ctxsw, intrs, soft_intrs, syscalls, traps, faults, forks = cext.cpu_stats()
        with open('/proc/stat', 'rb') as f:
            for line in f:
                if line.startswith(b'intr'):
                    intrs = int(line.split()[1])

    elif OPENBSD:
        ctxsw, intrs, soft_intrs, syscalls, traps, faults, forks = cext.cpu_stats()
    return _common.scpustats(ctxsw, intrs, soft_intrs, syscalls)


def disk_partitions(all=False):
    """Return mounted disk partitions as a list of namedtuples.
    'all' argument is ignored, see:
    https://github.com/giampaolo/psutil/issues/906
    """
    retlist = []
    partitions = cext.disk_partitions()
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        maxfile = maxpath = None
        ntuple = _common.sdiskpart(device, mountpoint, fstype, opts, maxfile, maxpath)
        retlist.append(ntuple)
    else:
        return retlist


disk_usage = _psposix.disk_usage
disk_io_counters = cext.disk_io_counters
net_io_counters = cext.net_io_counters
net_if_addrs = cext_posix.net_if_addrs

def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    names = net_io_counters().keys()
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


def net_connections--- This code section failed: ---

 L. 370         0  LOAD_GLOBAL              OPENBSD
                2  POP_JUMP_IF_FALSE   116  'to 116'

 L. 371         4  BUILD_LIST_0          0 
                6  STORE_FAST               'ret'

 L. 372         8  LOAD_GLOBAL              pids
               10  CALL_FUNCTION_0       0  ''
               12  GET_ITER         
             14_0  COME_FROM           110  '110'
             14_1  COME_FROM            62  '62'
             14_2  COME_FROM            58  '58'
               14  FOR_ITER            112  'to 112'
               16  STORE_FAST               'pid'

 L. 373        18  SETUP_FINALLY        38  'to 38'

 L. 374        20  LOAD_GLOBAL              Process
               22  LOAD_FAST                'pid'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_METHOD              connections
               28  LOAD_FAST                'kind'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'cons'
               34  POP_BLOCK        
               36  JUMP_FORWARD         66  'to 66'
             38_0  COME_FROM_FINALLY    18  '18'

 L. 375        38  DUP_TOP          
               40  LOAD_GLOBAL              NoSuchProcess
               42  LOAD_GLOBAL              ZombieProcess
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    64  'to 64'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 376        56  POP_EXCEPT       
               58  JUMP_BACK            14  'to 14'
               60  POP_EXCEPT       
               62  JUMP_BACK            14  'to 14'
             64_0  COME_FROM            48  '48'
               64  END_FINALLY      
             66_0  COME_FROM            36  '36'

 L. 378        66  LOAD_FAST                'cons'
               68  GET_ITER         
             70_0  COME_FROM           108  '108'
               70  FOR_ITER            110  'to 110'
               72  STORE_FAST               'conn'

 L. 379        74  LOAD_GLOBAL              list
               76  LOAD_FAST                'conn'
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'conn'

 L. 380        82  LOAD_FAST                'conn'
               84  LOAD_METHOD              append
               86  LOAD_FAST                'pid'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L. 381        92  LOAD_FAST                'ret'
               94  LOAD_METHOD              append
               96  LOAD_GLOBAL              _common
               98  LOAD_ATTR                sconn
              100  LOAD_FAST                'conn'
              102  CALL_FUNCTION_EX      0  'positional arguments only'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
              108  JUMP_BACK            70  'to 70'
            110_0  COME_FROM            70  '70'
              110  JUMP_BACK            14  'to 14'
            112_0  COME_FROM            14  '14'

 L. 382       112  LOAD_FAST                'ret'
              114  RETURN_VALUE     
            116_0  COME_FROM             2  '2'

 L. 384       116  LOAD_FAST                'kind'
              118  LOAD_GLOBAL              _common
              120  LOAD_ATTR                conn_tmap
              122  COMPARE_OP               not-in
              124  POP_JUMP_IF_FALSE   158  'to 158'

 L. 385       126  LOAD_GLOBAL              ValueError
              128  LOAD_STR                 'invalid %r kind argument; choose between %s'

 L. 386       130  LOAD_FAST                'kind'
              132  LOAD_STR                 ', '
              134  LOAD_METHOD              join
              136  LOAD_LISTCOMP            '<code_object <listcomp>>'
              138  LOAD_STR                 'net_connections.<locals>.<listcomp>'
              140  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              142  LOAD_GLOBAL              conn_tmap
              144  GET_ITER         
              146  CALL_FUNCTION_1       1  ''
              148  CALL_METHOD_1         1  ''
              150  BUILD_TUPLE_2         2 

 L. 385       152  BINARY_MODULO    
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           124  '124'

 L. 387       158  LOAD_GLOBAL              conn_tmap
              160  LOAD_FAST                'kind'
              162  BINARY_SUBSCR    
              164  UNPACK_SEQUENCE_2     2 
              166  STORE_FAST               'families'
              168  STORE_FAST               'types'

 L. 388       170  LOAD_GLOBAL              set
              172  CALL_FUNCTION_0       0  ''
              174  STORE_FAST               'ret'

 L. 389       176  LOAD_GLOBAL              NETBSD
              178  POP_JUMP_IF_FALSE   192  'to 192'

 L. 390       180  LOAD_GLOBAL              cext
              182  LOAD_METHOD              net_connections
              184  LOAD_CONST               -1
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'rawlist'
              190  JUMP_FORWARD        200  'to 200'
            192_0  COME_FROM           178  '178'

 L. 392       192  LOAD_GLOBAL              cext
              194  LOAD_METHOD              net_connections
              196  CALL_METHOD_0         0  ''
              198  STORE_FAST               'rawlist'
            200_0  COME_FROM           190  '190'

 L. 393       200  LOAD_FAST                'rawlist'
              202  GET_ITER         
            204_0  COME_FROM           274  '274'
            204_1  COME_FROM           240  '240'
            204_2  COME_FROM           232  '232'
              204  FOR_ITER            276  'to 276'
              206  STORE_FAST               'item'

 L. 394       208  LOAD_FAST                'item'
              210  UNPACK_SEQUENCE_7     7 
              212  STORE_FAST               'fd'
              214  STORE_FAST               'fam'
              216  STORE_FAST               'type'
              218  STORE_FAST               'laddr'
              220  STORE_FAST               'raddr'
              222  STORE_FAST               'status'
              224  STORE_FAST               'pid'

 L. 396       226  LOAD_FAST                'fam'
              228  LOAD_FAST                'families'
              230  COMPARE_OP               in
              232  POP_JUMP_IF_FALSE_BACK   204  'to 204'
              234  LOAD_FAST                'type'
              236  LOAD_FAST                'types'
              238  COMPARE_OP               in
              240  POP_JUMP_IF_FALSE_BACK   204  'to 204'

 L. 397       242  LOAD_GLOBAL              conn_to_ntuple
              244  LOAD_FAST                'fd'
              246  LOAD_FAST                'fam'
              248  LOAD_FAST                'type'
              250  LOAD_FAST                'laddr'
              252  LOAD_FAST                'raddr'
              254  LOAD_FAST                'status'

 L. 398       256  LOAD_GLOBAL              TCP_STATUSES

 L. 398       258  LOAD_FAST                'pid'

 L. 397       260  CALL_FUNCTION_8       8  ''
              262  STORE_FAST               'nt'

 L. 399       264  LOAD_FAST                'ret'
              266  LOAD_METHOD              add
              268  LOAD_FAST                'nt'
              270  CALL_METHOD_1         1  ''
              272  POP_TOP          
              274  JUMP_BACK           204  'to 204'
            276_0  COME_FROM           204  '204'

 L. 400       276  LOAD_GLOBAL              list
              278  LOAD_FAST                'ret'
              280  CALL_FUNCTION_1       1  ''
              282  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 62


if FREEBSD:

    def sensors_battery():
        """Return battery info."""
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


    def sensors_temperatures():
        """Return CPU cores temperatures if available, else an empty dict."""
        ret = defaultdict(list)
        num_cpus = cpu_count_logical()
        for cpu in range(num_cpus):
            try:
                current, high = cext.sensors_cpu_temperature(cpu)
                if high <= 0:
                    high = None
                name = 'Core %s' % cpu
                ret['coretemp'].append(_common.shwtemp(name, current, high, high))
            except NotImplementedError:
                pass

        else:
            return ret


    def cpu_freq--- This code section failed: ---

 L. 448         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ret'

 L. 449         4  LOAD_GLOBAL              cpu_count_logical
                6  CALL_FUNCTION_0       0  ''
                8  STORE_FAST               'num_cpus'

 L. 450        10  LOAD_GLOBAL              range
               12  LOAD_FAST                'num_cpus'
               14  CALL_FUNCTION_1       1  ''
               16  GET_ITER         
             18_0  COME_FROM           214  '214'
             18_1  COME_FROM            58  '58'
               18  FOR_ITER            216  'to 216'
               20  STORE_FAST               'cpu'

 L. 451        22  SETUP_FINALLY        42  'to 42'

 L. 452        24  LOAD_GLOBAL              cext
               26  LOAD_METHOD              cpu_frequency
               28  LOAD_FAST                'cpu'
               30  CALL_METHOD_1         1  ''
               32  UNPACK_SEQUENCE_2     2 
               34  STORE_FAST               'current'
               36  STORE_FAST               'available_freq'
               38  POP_BLOCK        
               40  JUMP_FORWARD         66  'to 66'
             42_0  COME_FROM_FINALLY    22  '22'

 L. 453        42  DUP_TOP          
               44  LOAD_GLOBAL              NotImplementedError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    64  'to 64'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 454        56  POP_EXCEPT       
               58  JUMP_BACK            18  'to 18'
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            48  '48'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            40  '40'

 L. 455        66  LOAD_FAST                'available_freq'
               68  POP_JUMP_IF_FALSE   194  'to 194'

 L. 456        70  SETUP_FINALLY       104  'to 104'

 L. 457        72  LOAD_GLOBAL              int
               74  LOAD_FAST                'available_freq'
               76  LOAD_METHOD              split
               78  LOAD_STR                 ' '
               80  CALL_METHOD_1         1  ''
               82  LOAD_CONST               -1
               84  BINARY_SUBSCR    
               86  LOAD_METHOD              split
               88  LOAD_STR                 '/'
               90  CALL_METHOD_1         1  ''
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  CALL_FUNCTION_1       1  ''
               98  STORE_FAST               'min_freq'
              100  POP_BLOCK        
              102  JUMP_FORWARD        132  'to 132'
            104_0  COME_FROM_FINALLY    70  '70'

 L. 458       104  DUP_TOP          
              106  LOAD_GLOBAL              IndexError
              108  LOAD_GLOBAL              ValueError
              110  BUILD_TUPLE_2         2 
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   130  'to 130'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 459       122  LOAD_CONST               None
              124  STORE_FAST               'min_freq'
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM           114  '114'
              130  END_FINALLY      
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM           102  '102'

 L. 460       132  SETUP_FINALLY       166  'to 166'

 L. 461       134  LOAD_GLOBAL              int
              136  LOAD_FAST                'available_freq'
              138  LOAD_METHOD              split
              140  LOAD_STR                 ' '
              142  CALL_METHOD_1         1  ''
              144  LOAD_CONST               0
              146  BINARY_SUBSCR    
              148  LOAD_METHOD              split
              150  LOAD_STR                 '/'
              152  CALL_METHOD_1         1  ''
              154  LOAD_CONST               0
              156  BINARY_SUBSCR    
              158  CALL_FUNCTION_1       1  ''
              160  STORE_FAST               'max_freq'
              162  POP_BLOCK        
              164  JUMP_FORWARD        194  'to 194'
            166_0  COME_FROM_FINALLY   132  '132'

 L. 462       166  DUP_TOP          
              168  LOAD_GLOBAL              IndexError
              170  LOAD_GLOBAL              ValueError
              172  BUILD_TUPLE_2         2 
              174  COMPARE_OP               exception-match
              176  POP_JUMP_IF_FALSE   192  'to 192'
              178  POP_TOP          
              180  POP_TOP          
              182  POP_TOP          

 L. 463       184  LOAD_CONST               None
              186  STORE_FAST               'max_freq'
              188  POP_EXCEPT       
              190  JUMP_FORWARD        194  'to 194'
            192_0  COME_FROM           176  '176'
              192  END_FINALLY      
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           164  '164'
            194_2  COME_FROM            68  '68'

 L. 464       194  LOAD_FAST                'ret'
              196  LOAD_METHOD              append
              198  LOAD_GLOBAL              _common
              200  LOAD_METHOD              scpufreq
              202  LOAD_FAST                'current'
              204  LOAD_FAST                'min_freq'
              206  LOAD_FAST                'max_freq'
              208  CALL_METHOD_3         3  ''
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          
              214  JUMP_BACK            18  'to 18'
            216_0  COME_FROM            18  '18'

 L. 465       216  LOAD_FAST                'ret'
              218  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 64_0


def boot_time():
    """The system boot time expressed in seconds since the epoch."""
    return cext.boot_time()


def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    for item in rawlist:
        user, tty, hostname, tstamp, pid = item
        if pid == -1:
            assert OPENBSD
            pid = None
        if tty == '~':
            pass
        else:
            nt = _common.suser(user, tty or None, hostname, tstamp, pid)
            retlist.append(nt)
    else:
        return retlist


@memoize
def _pid_0_exists():
    try:
        Process(0).name()
    except NoSuchProcess:
        return False
    except AccessDenied:
        return True
    else:
        return True


def pids():
    """Returns a list of PIDs currently running on the system."""
    ret = cext.pids()
    if OPENBSD:
        if 0 not in ret:
            if _pid_0_exists():
                ret.insert(0, 0)
    return ret


if OPENBSD or NETBSD:

    def pid_exists(pid):
        """Return True if pid exists."""
        exists = _psposix.pid_exists(pid)
        if not exists:
            return pid in pids()
        return True


else:
    pid_exists = _psposix.pid_exists

def is_zombie--- This code section failed: ---

 L. 536         0  SETUP_FINALLY        32  'to 32'

 L. 537         2  LOAD_GLOBAL              cext
                4  LOAD_METHOD              proc_oneshot_info
                6  LOAD_FAST                'pid'
                8  CALL_METHOD_1         1  ''
               10  LOAD_GLOBAL              kinfo_proc_map
               12  LOAD_STR                 'status'
               14  BINARY_SUBSCR    
               16  BINARY_SUBSCR    
               18  STORE_FAST               'st'

 L. 538        20  LOAD_FAST                'st'
               22  LOAD_GLOBAL              cext
               24  LOAD_ATTR                SZOMB
               26  COMPARE_OP               ==
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     0  '0'

 L. 539        32  DUP_TOP          
               34  LOAD_GLOBAL              Exception
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    52  'to 52'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 540        46  POP_EXCEPT       
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

 L. 549         0  SETUP_FINALLY        20  'to 20'

 L. 550         2  LOAD_DEREF               'fun'
                4  LOAD_FAST                'self'
                6  BUILD_TUPLE_1         1 
                8  LOAD_FAST                'args'
               10  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               12  LOAD_FAST                'kwargs'
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 551        20  DUP_TOP          
               22  LOAD_GLOBAL              ProcessLookupError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    82  'to 82'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 552        34  LOAD_GLOBAL              is_zombie
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                pid
               40  CALL_FUNCTION_1       1  ''
               42  POP_JUMP_IF_FALSE    64  'to 64'

 L. 553        44  LOAD_GLOBAL              ZombieProcess
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

 L. 555        64  LOAD_GLOBAL              NoSuchProcess
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                pid
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _name
               74  CALL_FUNCTION_2       2  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            62  '62'
               78  POP_EXCEPT       
               80  JUMP_FORWARD        174  'to 174'
             82_0  COME_FROM            26  '26'

 L. 556        82  DUP_TOP          
               84  LOAD_GLOBAL              PermissionError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   114  'to 114'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 557        96  LOAD_GLOBAL              AccessDenied
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                pid
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                _name
              106  CALL_FUNCTION_2       2  ''
              108  RAISE_VARARGS_1       1  'exception instance'
              110  POP_EXCEPT       
              112  JUMP_FORWARD        174  'to 174'
            114_0  COME_FROM            88  '88'

 L. 558       114  DUP_TOP          
              116  LOAD_GLOBAL              OSError
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   172  'to 172'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L. 559       128  LOAD_FAST                'self'
              130  LOAD_ATTR                pid
              132  LOAD_CONST               0
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   166  'to 166'

 L. 560       138  LOAD_CONST               0
              140  LOAD_GLOBAL              pids
              142  CALL_FUNCTION_0       0  ''
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE   164  'to 164'

 L. 561       148  LOAD_GLOBAL              AccessDenied
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                pid
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                _name
              158  CALL_FUNCTION_2       2  ''
              160  RAISE_VARARGS_1       1  'exception instance'
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           146  '146'

 L. 563       164  RAISE_VARARGS_0       0  'reraise'
            166_0  COME_FROM           162  '162'
            166_1  COME_FROM           136  '136'

 L. 564       166  RAISE_VARARGS_0       0  'reraise'
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           120  '120'
              172  END_FINALLY      
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           112  '112'
            174_2  COME_FROM            80  '80'

Parse error at or near `DUP_TOP' instruction at offset 82

    return wrapper


@contextlib.contextmanager
def wrap_exceptions_procfs(inst):
    """Same as above, for routines relying on reading /proc fs."""
    try:
        yield
    except (ProcessLookupError, FileNotFoundError):
        if is_zombie(inst.pid):
            raise ZombieProcess(inst.pid, inst._name, inst._ppid)
        else:
            raise NoSuchProcess(inst.pid, inst._name)
    except PermissionError:
        raise AccessDenied(inst.pid, inst._name)


class Process(object):
    __doc__ = 'Wrapper class around underlying C implementation.'
    __slots__ = [
     'pid', '_name', '_ppid', '_cache']

    def __init__(self, pid):
        self.pid = pid
        self._name = None
        self._ppid = None

    def _assert_alive(self):
        """Raise NSP if the process disappeared on us."""
        cext.proc_name(self.pid)

    @wrap_exceptions
    @memoize_when_activated
    def oneshot(self):
        """Retrieves multiple process info in one shot as a raw tuple."""
        ret = cext.proc_oneshot_info(self.pid)
        assert len(ret) == len(kinfo_proc_map)
        return ret

    def oneshot_enter(self):
        self.oneshot.cache_activate(self)

    def oneshot_exit(self):
        self.oneshot.cache_deactivate(self)

    @wrap_exceptions
    def name(self):
        name = self.oneshot()[kinfo_proc_map['name']]
        if name is not None:
            return name
        return cext.proc_name(self.pid)

    @wrap_exceptions
    def exe(self):
        if FREEBSD:
            if self.pid == 0:
                return ''
            return cext.proc_exe(self.pid)
        if NETBSD:
            if self.pid == 0:
                return ''
            with wrap_exceptions_procfs(self):
                return os.readlink('/proc/%s/exe' % self.pid)
        else:
            cmdline = self.cmdline()
            if cmdline:
                return which(cmdline[0]) or ''
            return ''

    @wrap_exceptions
    def cmdline--- This code section failed: ---

 L. 646         0  LOAD_GLOBAL              OPENBSD
                2  POP_JUMP_IF_FALSE    18  'to 18'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                pid
                8  LOAD_CONST               0
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 647        14  BUILD_LIST_0          0 
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'
             18_1  COME_FROM             2  '2'

 L. 648        18  LOAD_GLOBAL              NETBSD
               20  POP_JUMP_IF_FALSE   162  'to 162'

 L. 653        22  SETUP_FINALLY        38  'to 38'

 L. 654        24  LOAD_GLOBAL              cext
               26  LOAD_METHOD              proc_cmdline
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                pid
               32  CALL_METHOD_1         1  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    22  '22'

 L. 655        38  DUP_TOP          
               40  LOAD_GLOBAL              OSError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE   158  'to 158'
               46  POP_TOP          
               48  STORE_FAST               'err'
               50  POP_TOP          
               52  SETUP_FINALLY       146  'to 146'

 L. 656        54  LOAD_FAST                'err'
               56  LOAD_ATTR                errno
               58  LOAD_GLOBAL              errno
               60  LOAD_ATTR                EINVAL
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE   140  'to 140'

 L. 657        66  LOAD_GLOBAL              is_zombie
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                pid
               72  CALL_FUNCTION_1       1  ''
               74  POP_JUMP_IF_FALSE    96  'to 96'

 L. 658        76  LOAD_GLOBAL              ZombieProcess
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                pid
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                _name
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _ppid
               90  CALL_FUNCTION_3       3  ''
               92  RAISE_VARARGS_1       1  'exception instance'
               94  JUMP_FORWARD        142  'to 142'
             96_0  COME_FROM            74  '74'

 L. 659        96  LOAD_GLOBAL              pid_exists
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                pid
              102  CALL_FUNCTION_1       1  ''
              104  POP_JUMP_IF_TRUE    126  'to 126'

 L. 660       106  LOAD_GLOBAL              NoSuchProcess
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                pid
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _name
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _ppid
              120  CALL_FUNCTION_3       3  ''
              122  RAISE_VARARGS_1       1  'exception instance'
              124  JUMP_FORWARD        142  'to 142'
            126_0  COME_FROM           104  '104'

 L. 664       126  BUILD_LIST_0          0 
              128  ROT_FOUR         
              130  POP_BLOCK        
              132  POP_EXCEPT       
              134  CALL_FINALLY        146  'to 146'
              136  RETURN_VALUE     
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM            64  '64'

 L. 666       140  RAISE_VARARGS_0       0  'reraise'
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM           124  '124'
            142_2  COME_FROM            94  '94'
              142  POP_BLOCK        
              144  BEGIN_FINALLY    
            146_0  COME_FROM           134  '134'
            146_1  COME_FROM_FINALLY    52  '52'
              146  LOAD_CONST               None
              148  STORE_FAST               'err'
              150  DELETE_FAST              'err'
              152  END_FINALLY      
              154  POP_EXCEPT       
              156  JUMP_FORWARD        174  'to 174'
            158_0  COME_FROM            44  '44'
              158  END_FINALLY      
              160  JUMP_FORWARD        174  'to 174'
            162_0  COME_FROM            20  '20'

 L. 668       162  LOAD_GLOBAL              cext
              164  LOAD_METHOD              proc_cmdline
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                pid
              170  CALL_METHOD_1         1  ''
              172  RETURN_VALUE     
            174_0  COME_FROM           160  '160'
            174_1  COME_FROM           156  '156'

Parse error at or near `POP_BLOCK' instruction at offset 130

    @wrap_exceptions
    def environ(self):
        return cext.proc_environ(self.pid)

    @wrap_exceptions
    def terminal--- This code section failed: ---

 L. 676         0  LOAD_FAST                'self'
                2  LOAD_METHOD              oneshot
                4  CALL_METHOD_0         0  ''
                6  LOAD_GLOBAL              kinfo_proc_map
                8  LOAD_STR                 'ttynr'
               10  BINARY_SUBSCR    
               12  BINARY_SUBSCR    
               14  STORE_FAST               'tty_nr'

 L. 677        16  LOAD_GLOBAL              _psposix
               18  LOAD_METHOD              get_terminal_map
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'tmap'

 L. 678        24  SETUP_FINALLY        36  'to 36'

 L. 679        26  LOAD_FAST                'tmap'
               28  LOAD_FAST                'tty_nr'
               30  BINARY_SUBSCR    
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    24  '24'

 L. 680        36  DUP_TOP          
               38  LOAD_GLOBAL              KeyError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    56  'to 56'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 681        50  POP_EXCEPT       
               52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            42  '42'
               56  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 52

    @wrap_exceptions
    def ppid(self):
        self._ppid = self.oneshot()[kinfo_proc_map['ppid']]
        return self._ppid

    @wrap_exceptions
    def uids(self):
        rawtuple = self.oneshot()
        return _common.puids(rawtuple[kinfo_proc_map['real_uid']], rawtuple[kinfo_proc_map['effective_uid']], rawtuple[kinfo_proc_map['saved_uid']])

    @wrap_exceptions
    def gids(self):
        rawtuple = self.oneshot()
        return _common.pgids(rawtuple[kinfo_proc_map['real_gid']], rawtuple[kinfo_proc_map['effective_gid']], rawtuple[kinfo_proc_map['saved_gid']])

    @wrap_exceptions
    def cpu_times(self):
        rawtuple = self.oneshot()
        return _common.pcputimes(rawtuple[kinfo_proc_map['user_time']], rawtuple[kinfo_proc_map['sys_time']], rawtuple[kinfo_proc_map['ch_user_time']], rawtuple[kinfo_proc_map['ch_sys_time']])

    if FREEBSD:

        @wrap_exceptions
        def cpu_num(self):
            return self.oneshot()[kinfo_proc_map['cpunum']]

    @wrap_exceptions
    def memory_info(self):
        rawtuple = self.oneshot()
        return pmem(rawtuple[kinfo_proc_map['rss']], rawtuple[kinfo_proc_map['vms']], rawtuple[kinfo_proc_map['memtext']], rawtuple[kinfo_proc_map['memdata']], rawtuple[kinfo_proc_map['memstack']])

    memory_full_info = memory_info

    @wrap_exceptions
    def create_time(self):
        return self.oneshot()[kinfo_proc_map['create_time']]

    @wrap_exceptions
    def num_threads(self):
        if HAS_PROC_NUM_THREADS:
            return cext.proc_num_threads(self.pid)
        return len(self.threads())

    @wrap_exceptions
    def num_ctx_switches(self):
        rawtuple = self.oneshot()
        return _common.pctxsw(rawtuple[kinfo_proc_map['ctx_switches_vol']], rawtuple[kinfo_proc_map['ctx_switches_unvol']])

    @wrap_exceptions
    def threads(self):
        rawlist = cext.proc_threads(self.pid)
        retlist = []
        for thread_id, utime, stime in rawlist:
            ntuple = _common.pthread(thread_id, utime, stime)
            retlist.append(ntuple)
        else:
            if OPENBSD:
                self._assert_alive()
            return retlist

    @wrap_exceptions
    def connections(self, kind='inet'):
        if kind not in conn_tmap:
            raise ValueError('invalid %r kind argument; choose between %s' % (
             kind, ', '.join([repr(x) for x in conn_tmap])))
        if NETBSD:
            families, types = conn_tmap[kind]
            ret = []
            rawlist = cext.net_connections(self.pid)
            for item in rawlist:
                fd, fam, type, laddr, raddr, status, pid = item
                assert pid == self.pid
                if fam in families:
                    if type in types:
                        nt = conn_to_ntuple(fd, fam, type, laddr, raddr, status, TCP_STATUSES)
                        ret.append(nt)
                    self._assert_alive()
                    return list(ret)

        families, types = conn_tmap[kind]
        rawlist = cext.proc_connections(self.pid, families, types)
        ret = []
        for item in rawlist:
            fd, fam, type, laddr, raddr, status = item
            nt = conn_to_ntuple(fd, fam, type, laddr, raddr, status, TCP_STATUSES)
            ret.append(nt)
        else:
            if OPENBSD:
                self._assert_alive()
            return ret

    @wrap_exceptions
    def wait(self, timeout=None):
        return _psposix.wait_pid(self.pid, timeout, self._name)

    @wrap_exceptions
    def nice_get(self):
        return cext_posix.getpriority(self.pid)

    @wrap_exceptions
    def nice_set(self, value):
        return cext_posix.setpriority(self.pid, value)

    @wrap_exceptions
    def status(self):
        code = self.oneshot()[kinfo_proc_map['status']]
        return PROC_STATUSES.get(code, '?')

    @wrap_exceptions
    def io_counters(self):
        rawtuple = self.oneshot()
        return _common.pio(rawtuple[kinfo_proc_map['read_io_count']], rawtuple[kinfo_proc_map['write_io_count']], -1, -1)

    @wrap_exceptions
    def cwd(self):
        """Return process current working directory."""
        if OPENBSD:
            if self.pid == 0:
                return
        if NETBSD or (HAS_PROC_OPEN_FILES):
            return cext.proc_cwd(self.pid) or None
        raise NotImplementedError('supported only starting from FreeBSD 8' if FREEBSD else '')

    nt_mmap_grouped = namedtuple('mmap', 'path rss, private, ref_count, shadow_count')
    nt_mmap_ext = namedtuple('mmap', 'addr, perms path rss, private, ref_count, shadow_count')

    def _not_implemented(self):
        raise NotImplementedError

    if HAS_PROC_OPEN_FILES:

        @wrap_exceptions
        def open_files(self):
            """Return files opened by process as a list of namedtuples."""
            rawlist = cext.proc_open_files(self.pid)
            return [_common.popenfile(path, fd) for path, fd in rawlist]

    else:
        open_files = _not_implemented
    if HAS_PROC_NUM_FDS:

        @wrap_exceptions
        def num_fds(self):
            """Return the number of file descriptors opened by this process."""
            ret = cext.proc_num_fds(self.pid)
            if NETBSD:
                self._assert_alive()
            return ret

    else:
        num_fds = _not_implemented
    if FREEBSD:

        @wrap_exceptions
        def cpu_affinity_get(self):
            return cext.proc_cpu_affinity_get(self.pid)

        @wrap_exceptions
        def cpu_affinity_set(self, cpus):
            allcpus = tuple(range(len(per_cpu_times())))
            for cpu in cpus:
                if cpu not in allcpus:
                    raise ValueError('invalid CPU #%i (choose between %s)' % (
                     cpu, allcpus))

            try:
                cext.proc_cpu_affinity_set(self.pid, cpus)
            except OSError as err:
                try:
                    if err.errno in (errno.EINVAL, errno.EDEADLK):
                        for cpu in cpus:
                            if cpu not in allcpus:
                                raise ValueError('invalid CPU #%i (choose between %s)' % (
                                 cpu, allcpus))
                        else:
                            raise

                finally:
                    err = None
                    del err

        @wrap_exceptions
        def memory_maps(self):
            return cext.proc_memory_maps(self.pid)

        @wrap_exceptions
        def rlimit(self, resource, limits=None):
            if limits is None:
                return cext.proc_getrlimit(self.pid, resource)
            if len(limits) != 2:
                raise ValueError('second argument must be a (soft, hard) tuple, got %s' % repr(limits))
            soft, hard = limits
            return cext.proc_setrlimit(self.pid, resource, soft, hard)