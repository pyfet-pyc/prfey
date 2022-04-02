# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: psutil\_pslinux.py
"""Linux platform implementation."""
from __future__ import division
import base64, collections, errno, functools, glob, os, re, socket, struct, sys, traceback, warnings
from collections import defaultdict
from collections import namedtuple
from . import _common
from . import _psposix
from . import _psutil_linux as cext
from . import _psutil_posix as cext_posix
from ._common import AccessDenied
from ._common import debug
from ._common import decode
from ._common import get_procfs_path
from ._common import isfile_strict
from ._common import memoize
from ._common import memoize_when_activated
from ._common import NIC_DUPLEX_FULL
from ._common import NIC_DUPLEX_HALF
from ._common import NIC_DUPLEX_UNKNOWN
from ._common import NoSuchProcess
from ._common import open_binary
from ._common import open_text
from ._common import parse_environ_block
from ._common import path_exists_strict
from ._common import supports_ipv6
from ._common import usage_percent
from ._common import ZombieProcess
from ._compat import b
from ._compat import basestring
from ._compat import FileNotFoundError
from ._compat import PermissionError
from ._compat import ProcessLookupError
from ._compat import PY3
if sys.version_info >= (3, 4):
    import enum
else:
    enum = None
__extra__all__ = [
 'PROCFS_PATH',
 'IOPRIO_CLASS_NONE', 'IOPRIO_CLASS_RT', 'IOPRIO_CLASS_BE',
 'IOPRIO_CLASS_IDLE',
 'CONN_ESTABLISHED', 'CONN_SYN_SENT', 'CONN_SYN_RECV', 'CONN_FIN_WAIT1',
 'CONN_FIN_WAIT2', 'CONN_TIME_WAIT', 'CONN_CLOSE', 'CONN_CLOSE_WAIT',
 'CONN_LAST_ACK', 'CONN_LISTEN', 'CONN_CLOSING']
POWER_SUPPLY_PATH = '/sys/class/power_supply'
HAS_SMAPS = os.path.exists('/proc/%s/smaps' % os.getpid())
HAS_PROC_IO_PRIORITY = hasattr(cext, 'proc_ioprio_get')
HAS_CPU_AFFINITY = hasattr(cext, 'proc_cpu_affinity_get')
_DEFAULT = object()
CLOCK_TICKS = os.sysconf('SC_CLK_TCK')
PAGESIZE = cext_posix.getpagesize()
BOOT_TIME = None
BIGFILE_BUFFERING = -1 if PY3 else 8192
LITTLE_ENDIAN = sys.byteorder == 'little'
DISK_SECTOR_SIZE = 512
if enum is None:
    AF_LINK = socket.AF_PACKET
else:
    AddressFamily = enum.IntEnum('AddressFamily', {'AF_LINK': int(socket.AF_PACKET)})
    AF_LINK = AddressFamily.AF_LINK
if enum is None:
    IOPRIO_CLASS_NONE = 0
    IOPRIO_CLASS_RT = 1
    IOPRIO_CLASS_BE = 2
    IOPRIO_CLASS_IDLE = 3
else:

    class IOPriority(enum.IntEnum):
        IOPRIO_CLASS_NONE = 0
        IOPRIO_CLASS_RT = 1
        IOPRIO_CLASS_BE = 2
        IOPRIO_CLASS_IDLE = 3


    globals().update(IOPriority.__members__)
PROC_STATUSES = {'R':_common.STATUS_RUNNING, 
 'S':_common.STATUS_SLEEPING, 
 'D':_common.STATUS_DISK_SLEEP, 
 'T':_common.STATUS_STOPPED, 
 't':_common.STATUS_TRACING_STOP, 
 'Z':_common.STATUS_ZOMBIE, 
 'X':_common.STATUS_DEAD, 
 'x':_common.STATUS_DEAD, 
 'K':_common.STATUS_WAKE_KILL, 
 'W':_common.STATUS_WAKING, 
 'I':_common.STATUS_IDLE, 
 'P':_common.STATUS_PARKED}
TCP_STATUSES = {'01':_common.CONN_ESTABLISHED, 
 '02':_common.CONN_SYN_SENT, 
 '03':_common.CONN_SYN_RECV, 
 '04':_common.CONN_FIN_WAIT1, 
 '05':_common.CONN_FIN_WAIT2, 
 '06':_common.CONN_TIME_WAIT, 
 '07':_common.CONN_CLOSE, 
 '08':_common.CONN_CLOSE_WAIT, 
 '09':_common.CONN_LAST_ACK, 
 '0A':_common.CONN_LISTEN, 
 '0B':_common.CONN_CLOSING}
svmem = namedtuple('svmem', ['total', 'available', 'percent', 'used', 'free',
 'active', 'inactive', 'buffers', 'cached', 'shared', 'slab'])
sdiskio = namedtuple('sdiskio', ['read_count', 'write_count',
 'read_bytes', 'write_bytes',
 'read_time', 'write_time',
 'read_merged_count', 'write_merged_count',
 'busy_time'])
popenfile = namedtuple('popenfile', ['path', 'fd', 'position', 'mode', 'flags'])
pmem = namedtuple('pmem', 'rss vms shared text lib data dirty')
pfullmem = namedtuple('pfullmem', pmem._fields + ('uss', 'pss', 'swap'))
pmmap_grouped = namedtuple('pmmap_grouped', [
 'path', 'rss', 'size', 'pss', 'shared_clean', 'shared_dirty',
 'private_clean', 'private_dirty', 'referenced', 'anonymous', 'swap'])
pmmap_ext = namedtuple('pmmap_ext', 'addr perms ' + ' '.join(pmmap_grouped._fields))
pio = namedtuple('pio', ['read_count', 'write_count',
 'read_bytes', 'write_bytes',
 'read_chars', 'write_chars'])
pcputimes = namedtuple('pcputimes', [
 'user', 'system', 'children_user', 'children_system',
 'iowait'])

def readlink(path):
    """Wrapper around os.readlink()."""
    assert isinstance(path, basestring), path
    path = os.readlink(path)
    path = path.split('\x00')[0]
    if path.endswith(' (deleted)'):
        if not path_exists_strict(path):
            path = path[:-10]
    return path


def file_flags_to_mode(flags):
    """Convert file's open() flags into a readable string.
    Used by Process.open_files().
    """
    modes_map = {os.O_RDONLY: 'r', os.O_WRONLY: 'w', os.O_RDWR: 'w+'}
    mode = modes_map[(flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR))]
    if flags & os.O_APPEND:
        mode = mode.replace('w', 'a', 1)
    mode = mode.replace('w+', 'r+')
    return mode


def is_storage_device(name):
    """Return True if the given name refers to a root device (e.g.
    "sda", "nvme0n1") as opposed to a logical partition (e.g.  "sda1",
    "nvme0n1p1"). If name is a virtual device (e.g. "loop1", "ram")
    return True.
    """
    name = name.replace('/', '!')
    including_virtual = True
    if including_virtual:
        path = '/sys/block/%s' % name
    else:
        path = '/sys/block/%s/device' % name
    return os.access(path, os.F_OK)


@memoize
def set_scputimes_ntuple(procfs_path):
    """Set a namedtuple of variable fields depending on the CPU times
    available on this Linux kernel version which may be:
    (user, nice, system, idle, iowait, irq, softirq, [steal, [guest,
     [guest_nice]]])
    Used by cpu_times() function.
    """
    global scputimes
    with open_binary('%s/stat' % procfs_path) as (f):
        values = f.readline().split()[1:]
    fields = [
     'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq']
    vlen = len(values)
    if vlen >= 8:
        fields.append('steal')
    if vlen >= 9:
        fields.append('guest')
    if vlen >= 10:
        fields.append('guest_nice')
    scputimes = namedtuple('scputimes', fields)


def cat--- This code section failed: ---

 L. 291         0  SETUP_FINALLY        60  'to 60'

 L. 292         2  LOAD_FAST                'binary'
                4  POP_JUMP_IF_FALSE    14  'to 14'
                6  LOAD_GLOBAL              open_binary
                8  LOAD_FAST                'fname'
               10  CALL_FUNCTION_1       1  ''
               12  JUMP_FORWARD         20  'to 20'
             14_0  COME_FROM             4  '4'
               14  LOAD_GLOBAL              open_text
               16  LOAD_FAST                'fname'
               18  CALL_FUNCTION_1       1  ''
             20_0  COME_FROM            12  '12'
               20  SETUP_WITH           50  'to 50'
               22  STORE_FAST               'f'

 L. 293        24  LOAD_FAST                'f'
               26  LOAD_METHOD              read
               28  CALL_METHOD_0         0  ''
               30  LOAD_METHOD              strip
               32  CALL_METHOD_0         0  ''
               34  POP_BLOCK        
               36  ROT_TWO          
               38  BEGIN_FINALLY    
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  POP_FINALLY           0  ''
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_WITH       20  '20'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      
               56  POP_BLOCK        
               58  JUMP_FORWARD        102  'to 102'
             60_0  COME_FROM_FINALLY     0  '0'

 L. 294        60  DUP_TOP          
               62  LOAD_GLOBAL              IOError
               64  LOAD_GLOBAL              OSError
               66  BUILD_TUPLE_2         2 
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE   100  'to 100'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 295        78  LOAD_FAST                'fallback'
               80  LOAD_GLOBAL              _DEFAULT
               82  COMPARE_OP               is-not
               84  POP_JUMP_IF_FALSE    94  'to 94'

 L. 296        86  LOAD_FAST                'fallback'
               88  ROT_FOUR         
               90  POP_EXCEPT       
               92  RETURN_VALUE     
             94_0  COME_FROM            84  '84'

 L. 298        94  RAISE_VARARGS_0       0  'reraise'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            70  '70'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            58  '58'

Parse error at or near `ROT_TWO' instruction at offset 36


try:
    set_scputimes_ntuple('/proc')
except Exception:
    traceback.print_exc()
    scputimes = namedtuple('scputimes', 'user system idle')(0.0, 0.0, 0.0)
else:
    prlimit = None
    try:
        from resource import prlimit
    except ImportError:
        import ctypes
        libc = ctypes.CDLL(None, use_errno=True)
        if hasattr(libc, 'prlimit'):

            def prlimit(pid, resource_, limits=None):

                class StructRlimit(ctypes.Structure):
                    _fields_ = [
                     (
                      'rlim_cur', ctypes.c_longlong),
                     (
                      'rlim_max', ctypes.c_longlong)]

                current = StructRlimit()
                if limits is None:
                    ret = libc.prlimit(pid, resource_, None, ctypes.byref(current))
                else:
                    new = StructRlimit()
                    new.rlim_cur = limits[0]
                    new.rlim_max = limits[1]
                    ret = libc.prlimit(pid, resource_, ctypes.byref(new), ctypes.byref(current))
                if ret != 0:
                    errno = ctypes.get_errno()
                    raise OSError(errno, os.strerror(errno))
                return (
                 current.rlim_cur, current.rlim_max)


    else:
        if prlimit is not None:
            __extra__all__.extend([x for x in dir(cext) if x.startswith('RLIM') if x.isupper()])
        else:

            def calculate_avail_vmem(mems):
                """Fallback for kernels < 3.14 where /proc/meminfo does not provide
    "MemAvailable:" column, see:
    https://blog.famzah.net/2014/09/24/
    This code reimplements the algorithm outlined here:
    https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/
        commit/?id=34e431b0ae398fc54ea69ff85ec700722c9da773

    XXX: on recent kernels this calculation differs by ~1.5% than
    "MemAvailable:" as it's calculated slightly differently, see:
    https://gitlab.com/procps-ng/procps/issues/42
    https://github.com/famzah/linux-memavailable-procfs/issues/2
    It is still way more realistic than doing (free + cached) though.
    """
                free = mems[b'MemFree:']
                fallback = free + mems.get(b'Cached:', 0)
                try:
                    lru_active_file = mems[b'Active(file):']
                    lru_inactive_file = mems[b'Inactive(file):']
                    slab_reclaimable = mems[b'SReclaimable:']
                except KeyError:
                    return fallback
                else:
                    try:
                        f = open_binary('%s/zoneinfo' % get_procfs_path())
                    except IOError:
                        return fallback
                    else:
                        watermark_low = 0
                        with f:
                            for line in f:
                                line = line.strip()

                            if line.startswith(b'low'):
                                watermark_low += int(line.split()[1])
                        watermark_low *= PAGESIZE
                        avail = free - watermark_low
                        pagecache = lru_active_file + lru_inactive_file
                        pagecache -= min(pagecache / 2, watermark_low)
                        avail += pagecache
                        avail += slab_reclaimable - min(slab_reclaimable / 2.0, watermark_low)
                        return int(avail)


            def virtual_memory():
                """Report virtual memory stats.
    This implementation matches "free" and "vmstat -s" cmdline
    utility values and procps-ng-3.3.12 source was used as a reference
    (2016-09-18):
    https://gitlab.com/procps-ng/procps/blob/
        24fd2605c51fccc375ab0287cec33aa767f06718/proc/sysinfo.c
    For reference, procps-ng-3.3.10 is the version available on Ubuntu
    16.04.

    Note about "available" memory: up until psutil 4.3 it was
    calculated as "avail = (free + buffers + cached)". Now
    "MemAvailable:" column (kernel 3.14) from /proc/meminfo is used as
    it's more accurate.
    That matches "available" column in newer versions of "free".
    """
                missing_fields = []
                mems = {}
                with open_binary('%s/meminfo' % get_procfs_path()) as (f):
                    for line in f:
                        fields = line.split()
                        mems[fields[0]] = int(fields[1]) * 1024

                total = mems[b'MemTotal:']
                free = mems[b'MemFree:']
                try:
                    buffers = mems[b'Buffers:']
                except KeyError:
                    buffers = 0
                    missing_fields.append('buffers')
                else:
                    try:
                        cached = mems[b'Cached:']
                    except KeyError:
                        cached = 0
                        missing_fields.append('cached')
                    else:
                        cached += mems.get(b'SReclaimable:', 0)
                try:
                    shared = mems[b'Shmem:']
                except KeyError:
                    try:
                        shared = mems[b'MemShared:']
                    except KeyError:
                        shared = 0
                        missing_fields.append('shared')

                try:
                    active = mems[b'Active:']
                except KeyError:
                    active = 0
                    missing_fields.append('active')

                try:
                    inactive = mems[b'Inactive:']
                except KeyError:
                    try:
                        inactive = mems[b'Inact_dirty:'] + mems[b'Inact_clean:'] + mems[b'Inact_laundry:']
                    except KeyError:
                        inactive = 0
                        missing_fields.append('inactive')

                else:
                    try:
                        slab = mems[b'Slab:']
                    except KeyError:
                        slab = 0
                    else:
                        used = total - free - cached - buffers
                        if used < 0:
                            used = total - free
                try:
                    avail = mems[b'MemAvailable:']
                except KeyError:
                    avail = calculate_avail_vmem(mems)
                else:
                    if avail < 0:
                        avail = 0
                        missing_fields.append('available')
                    if avail > total:
                        avail = free
                    percent = usage_percent((total - avail), total, round_=1)
                    if missing_fields:
                        msg = "%s memory stats couldn't be determined and %s set to 0" % (
                         ', '.join(missing_fields),
                         'was' if len(missing_fields) == 1 else 'were')
                        warnings.warn(msg, RuntimeWarning)
                    return svmem(total, avail, percent, used, free, active, inactive, buffers, cached, shared, slab)


            def swap_memory():
                """Return swap memory metrics."""
                mems = {}
                with open_binary('%s/meminfo' % get_procfs_path()) as (f):
                    for line in f:
                        fields = line.split()
                        mems[fields[0]] = int(fields[1]) * 1024

                try:
                    total = mems[b'SwapTotal:']
                    free = mems[b'SwapFree:']
                except KeyError:
                    _, _, _, _, total, free, unit_multiplier = cext.linux_sysinfo()
                    total *= unit_multiplier
                    free *= unit_multiplier
                else:
                    used = total - free
                    percent = usage_percent(used, total, round_=1)
                    try:
                        f = open_binary('%s/vmstat' % get_procfs_path())
                    except IOError as err:
                        try:
                            msg = "'sin' and 'sout' swap memory stats couldn't be determined and were set to 0 (%s)" % str(err)
                            warnings.warn(msg, RuntimeWarning)
                            sin = sout = 0
                        finally:
                            err = None
                            del err

                    else:
                        with f:
                            sin = sout = None
                            for line in f:
                                if line.startswith(b'pswpin'):
                                    sin = int(line.split(b' ')[1]) * 4 * 1024
                                else:
                                    if line.startswith(b'pswpout'):
                                        sout = int(line.split(b' ')[1]) * 4 * 1024
                                    if sin is not None and sout is not None:
                                        break
                                    msg = "'sin' and 'sout' swap memory stats couldn't be determined and were set to 0"
                                    warnings.warn(msg, RuntimeWarning)
                                    sin = sout = 0

                    return _common.sswap(total, used, free, percent, sin, sout)


            def cpu_times():
                """Return a named tuple representing the following system-wide
    CPU times:
    (user, nice, system, idle, iowait, irq, softirq [steal, [guest,
     [guest_nice]]])
    Last 3 fields may not be available on all Linux kernel versions.
    """
                procfs_path = get_procfs_path()
                set_scputimes_ntuple(procfs_path)
                with open_binary('%s/stat' % procfs_path) as (f):
                    values = f.readline().split()
                fields = values[1:len(scputimes._fields) + 1]
                fields = [float(x) / CLOCK_TICKS for x in fields]
                return scputimes(*fields)


            def per_cpu_times--- This code section failed: ---

 L. 614         0  LOAD_GLOBAL              get_procfs_path
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'procfs_path'

 L. 615         6  LOAD_GLOBAL              set_scputimes_ntuple
                8  LOAD_FAST                'procfs_path'
               10  CALL_FUNCTION_1       1  ''
               12  POP_TOP          

 L. 616        14  BUILD_LIST_0          0 
               16  STORE_FAST               'cpus'

 L. 617        18  LOAD_GLOBAL              open_binary
               20  LOAD_STR                 '%s/stat'
               22  LOAD_FAST                'procfs_path'
               24  BINARY_MODULO    
               26  CALL_FUNCTION_1       1  ''
               28  SETUP_WITH          138  'to 138'
               30  STORE_FAST               'f'

 L. 619        32  LOAD_FAST                'f'
               34  LOAD_METHOD              readline
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L. 620        40  LOAD_FAST                'f'
               42  GET_ITER         
             44_0  COME_FROM            56  '56'
               44  FOR_ITER            122  'to 122'
               46  STORE_FAST               'line'

 L. 621        48  LOAD_FAST                'line'
               50  LOAD_METHOD              startswith
               52  LOAD_CONST               b'cpu'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE    44  'to 44'

 L. 622        58  LOAD_FAST                'line'
               60  LOAD_METHOD              split
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'values'

 L. 623        66  LOAD_FAST                'values'
               68  LOAD_CONST               1
               70  LOAD_GLOBAL              len
               72  LOAD_GLOBAL              scputimes
               74  LOAD_ATTR                _fields
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_CONST               1
               80  BINARY_ADD       
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  STORE_FAST               'fields'

 L. 624        88  LOAD_LISTCOMP            '<code_object <listcomp>>'
               90  LOAD_STR                 'per_cpu_times.<locals>.<listcomp>'
               92  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               94  LOAD_FAST                'fields'
               96  GET_ITER         
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'fields'

 L. 625       102  LOAD_GLOBAL              scputimes
              104  LOAD_FAST                'fields'
              106  CALL_FUNCTION_EX      0  'positional arguments only'
              108  STORE_FAST               'entry'

 L. 626       110  LOAD_FAST                'cpus'
              112  LOAD_METHOD              append
              114  LOAD_FAST                'entry'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          
              120  JUMP_BACK            44  'to 44'

 L. 627       122  LOAD_FAST                'cpus'
              124  POP_BLOCK        
              126  ROT_TWO          
              128  BEGIN_FINALLY    
              130  WITH_CLEANUP_START
              132  WITH_CLEANUP_FINISH
              134  POP_FINALLY           0  ''
              136  RETURN_VALUE     
            138_0  COME_FROM_WITH       28  '28'
              138  WITH_CLEANUP_START
              140  WITH_CLEANUP_FINISH
              142  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 126


            def cpu_count_logical--- This code section failed: ---

 L. 632         0  SETUP_FINALLY        14  'to 14'

 L. 633         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              sysconf
                6  LOAD_STR                 'SC_NPROCESSORS_ONLN'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 634        14  DUP_TOP          
               16  LOAD_GLOBAL              ValueError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE   198  'to 198'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 636        28  LOAD_CONST               0
               30  STORE_FAST               'num'

 L. 637        32  LOAD_GLOBAL              open_binary
               34  LOAD_STR                 '%s/cpuinfo'
               36  LOAD_GLOBAL              get_procfs_path
               38  CALL_FUNCTION_0       0  ''
               40  BINARY_MODULO    
               42  CALL_FUNCTION_1       1  ''
               44  SETUP_WITH           84  'to 84'
               46  STORE_FAST               'f'

 L. 638        48  LOAD_FAST                'f'
               50  GET_ITER         
             52_0  COME_FROM            68  '68'
               52  FOR_ITER             80  'to 80'
               54  STORE_FAST               'line'

 L. 639        56  LOAD_FAST                'line'
               58  LOAD_METHOD              lower
               60  CALL_METHOD_0         0  ''
               62  LOAD_METHOD              startswith
               64  LOAD_CONST               b'processor'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_FALSE    52  'to 52'

 L. 640        70  LOAD_FAST                'num'
               72  LOAD_CONST               1
               74  INPLACE_ADD      
               76  STORE_FAST               'num'
               78  JUMP_BACK            52  'to 52'
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       44  '44'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      

 L. 645        90  LOAD_FAST                'num'
               92  LOAD_CONST               0
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   176  'to 176'

 L. 646        98  LOAD_GLOBAL              re
              100  LOAD_METHOD              compile
              102  LOAD_STR                 'cpu\\d'
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'search'

 L. 647       108  LOAD_GLOBAL              open_text
              110  LOAD_STR                 '%s/stat'
              112  LOAD_GLOBAL              get_procfs_path
              114  CALL_FUNCTION_0       0  ''
              116  BINARY_MODULO    
              118  CALL_FUNCTION_1       1  ''
              120  SETUP_WITH          170  'to 170'
              122  STORE_FAST               'f'

 L. 648       124  LOAD_FAST                'f'
              126  GET_ITER         
            128_0  COME_FROM           154  '154'
              128  FOR_ITER            166  'to 166'
              130  STORE_FAST               'line'

 L. 649       132  LOAD_FAST                'line'
              134  LOAD_METHOD              split
              136  LOAD_STR                 ' '
              138  CALL_METHOD_1         1  ''
              140  LOAD_CONST               0
              142  BINARY_SUBSCR    
              144  STORE_FAST               'line'

 L. 650       146  LOAD_FAST                'search'
              148  LOAD_METHOD              match
              150  LOAD_FAST                'line'
              152  CALL_METHOD_1         1  ''
              154  POP_JUMP_IF_FALSE   128  'to 128'

 L. 651       156  LOAD_FAST                'num'
              158  LOAD_CONST               1
              160  INPLACE_ADD      
              162  STORE_FAST               'num'
              164  JUMP_BACK           128  'to 128'
              166  POP_BLOCK        
              168  BEGIN_FINALLY    
            170_0  COME_FROM_WITH      120  '120'
              170  WITH_CLEANUP_START
              172  WITH_CLEANUP_FINISH
              174  END_FINALLY      
            176_0  COME_FROM            96  '96'

 L. 653       176  LOAD_FAST                'num'
              178  LOAD_CONST               0
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   190  'to 190'

 L. 655       184  POP_EXCEPT       
              186  LOAD_CONST               None
              188  RETURN_VALUE     
            190_0  COME_FROM           182  '182'

 L. 656       190  LOAD_FAST                'num'
              192  ROT_FOUR         
              194  POP_EXCEPT       
              196  RETURN_VALUE     
            198_0  COME_FROM            20  '20'
              198  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24


            def cpu_count_physical():
                """Return the number of physical cores in the system."""
                ls = set()
                p1 = '/sys/devices/system/cpu/cpu[0-9]*/topology/core_cpus_list'
                p2 = '/sys/devices/system/cpu/cpu[0-9]*/topology/thread_siblings_list'
                for path in glob.glob(p1) or glob.glob(p2):
                    with open_binary(path) as (f):
                        ls.add(f.read().strip())
                else:
                    result = len(ls)
                    if result != 0:
                        return result
                    mapping = {}
                    current_info = {}
                    with open_binary('%s/cpuinfo' % get_procfs_path()) as (f):
                        for line in f:
                            line = line.strip().lower()
                            if not line:
                                try:
                                    mapping[current_info[b'physical id']] = current_info[b'cpu cores']
                                except KeyError:
                                    pass
                                else:
                                    current_info = {}
                        else:
                            if line.startswith((b'physical id', b'cpu cores')):
                                key, value = line.split(b'\t:', 1)
                                current_info[key] = int(value)

                    result = sum(mapping.values())
                    return result or None


            def cpu_stats():
                """Return various CPU stats as a named tuple."""
                with open_binary('%s/stat' % get_procfs_path()) as (f):
                    ctx_switches = None
                    interrupts = None
                    soft_interrupts = None
                    for line in f:
                        if line.startswith(b'ctxt'):
                            ctx_switches = int(line.split()[1])
                        else:
                            if line.startswith(b'intr'):
                                interrupts = int(line.split()[1])
                            else:
                                if line.startswith(b'softirq'):
                                    soft_interrupts = int(line.split()[1])
                        if ctx_switches is not None and soft_interrupts is not None and interrupts is not None:
                            break

                syscalls = 0
                return _common.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


            if os.path.exists('/sys/devices/system/cpu/cpufreq/policy0') or os.path.exists('/sys/devices/system/cpu/cpu0/cpufreq'):

                def cpu_freq():
                    """Return frequency metrics for all CPUs.
        Contrarily to other OSes, Linux updates these values in
        real-time.
        """

                    def get_path(num):
                        for p in (
                         '/sys/devices/system/cpu/cpufreq/policy%s' % num,
                         '/sys/devices/system/cpu/cpu%s/cpufreq' % num):
                            if os.path.exists(p):
                                return p

                    ret = []
                    for n in range(cpu_count_logical()):
                        path = get_path(n)
                        if not path:
                            pass
                        else:
                            pjoin = os.path.join
                            curr = cat((pjoin(path, 'scaling_cur_freq')), fallback=None)
                            if curr is None:
                                curr = cat((pjoin(path, 'cpuinfo_cur_freq')), fallback=None)
                                if curr is None:
                                    raise NotImplementedError("can't find current frequency file")
                            curr = int(curr) / 1000
                            max_ = int(cat(pjoin(path, 'scaling_max_freq'))) / 1000
                            min_ = int(cat(pjoin(path, 'scaling_min_freq'))) / 1000
                            ret.append(_common.scpufreq(curr, min_, max_))
                    else:
                        return ret


            else:
                if os.path.exists('/proc/cpuinfo'):

                    def cpu_freq():
                        """Alternate implementation using /proc/cpuinfo.
        min and max frequencies are not available and are set to None.
        """
                        ret = []
                        with open_binary('%s/cpuinfo' % get_procfs_path()) as (f):
                            for line in f:
                                if line.lower().startswith(b'cpu mhz'):
                                    key, value = line.split(b':', 1)
                                    ret.append(_common.scpufreq(float(value), 0.0, 0.0))

                        return ret


                else:

                    def cpu_freq():
                        """Dummy implementation when none of the above files are present.
        """
                        return []


        net_if_addrs = cext_posix.net_if_addrs

        class _Ipv6UnsupportedError(Exception):
            pass


        class Connections:
            __doc__ = 'A wrapper on top of /proc/net/* files, retrieving per-process\n    and system-wide open connections (TCP, UDP, UNIX) similarly to\n    "netstat -an".\n\n    Note: in case of UNIX sockets we\'re only able to determine the\n    local endpoint/path, not the one it\'s connected to.\n    According to [1] it would be possible but not easily.\n\n    [1] http://serverfault.com/a/417946\n    '

            def __init__(self):
                tcp4 = (
                 'tcp', socket.AF_INET, socket.SOCK_STREAM)
                tcp6 = ('tcp6', socket.AF_INET6, socket.SOCK_STREAM)
                udp4 = ('udp', socket.AF_INET, socket.SOCK_DGRAM)
                udp6 = ('udp6', socket.AF_INET6, socket.SOCK_DGRAM)
                unix = ('unix', socket.AF_UNIX, None)
                self.tmap = {'all':(
                  tcp4, tcp6, udp4, udp6, unix), 
                 'tcp':(
                  tcp4, tcp6), 
                 'tcp4':(
                  tcp4,), 
                 'tcp6':(
                  tcp6,), 
                 'udp':(
                  udp4, udp6), 
                 'udp4':(
                  udp4,), 
                 'udp6':(
                  udp6,), 
                 'unix':(
                  unix,), 
                 'inet':(
                  tcp4, tcp6, udp4, udp6), 
                 'inet4':(
                  tcp4, udp4), 
                 'inet6':(
                  tcp6, udp6)}
                self._procfs_path = None

            def get_proc_inodes--- This code section failed: ---

 L. 824         0  LOAD_GLOBAL              defaultdict
                2  LOAD_GLOBAL              list
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'inodes'

 L. 825         8  LOAD_GLOBAL              os
               10  LOAD_METHOD              listdir
               12  LOAD_STR                 '%s/%s/fd'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _procfs_path
               18  LOAD_FAST                'pid'
               20  BUILD_TUPLE_2         2 
               22  BINARY_MODULO    
               24  CALL_METHOD_1         1  ''
               26  GET_ITER         
             28_0  COME_FROM           148  '148'
               28  FOR_ITER            194  'to 194'
               30  STORE_FAST               'fd'

 L. 826        32  SETUP_FINALLY        58  'to 58'

 L. 827        34  LOAD_GLOBAL              readlink
               36  LOAD_STR                 '%s/%s/fd/%s'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _procfs_path
               42  LOAD_FAST                'pid'
               44  LOAD_FAST                'fd'
               46  BUILD_TUPLE_3         3 
               48  BINARY_MODULO    
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'inode'
               54  POP_BLOCK        
               56  JUMP_FORWARD        140  'to 140'
             58_0  COME_FROM_FINALLY    32  '32'

 L. 828        58  DUP_TOP          
               60  LOAD_GLOBAL              FileNotFoundError
               62  LOAD_GLOBAL              ProcessLookupError
               64  BUILD_TUPLE_2         2 
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    84  'to 84'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 832        76  POP_EXCEPT       
               78  JUMP_BACK            28  'to 28'
               80  POP_EXCEPT       
               82  JUMP_BACK            28  'to 28'
             84_0  COME_FROM            68  '68'

 L. 833        84  DUP_TOP          
               86  LOAD_GLOBAL              OSError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   138  'to 138'
               92  POP_TOP          
               94  STORE_FAST               'err'
               96  POP_TOP          
               98  SETUP_FINALLY       126  'to 126'

 L. 834       100  LOAD_FAST                'err'
              102  LOAD_ATTR                errno
              104  LOAD_GLOBAL              errno
              106  LOAD_ATTR                EINVAL
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   120  'to 120'

 L. 836       112  POP_BLOCK        
              114  POP_EXCEPT       
              116  CALL_FINALLY        126  'to 126'
              118  JUMP_BACK            28  'to 28'
            120_0  COME_FROM           110  '110'

 L. 837       120  RAISE_VARARGS_0       0  'reraise'
              122  POP_BLOCK        
              124  BEGIN_FINALLY    
            126_0  COME_FROM           116  '116'
            126_1  COME_FROM_FINALLY    98  '98'
              126  LOAD_CONST               None
              128  STORE_FAST               'err'
              130  DELETE_FAST              'err'
              132  END_FINALLY      
              134  POP_EXCEPT       
              136  JUMP_BACK            28  'to 28'
            138_0  COME_FROM            90  '90'
              138  END_FINALLY      
            140_0  COME_FROM            56  '56'

 L. 839       140  LOAD_FAST                'inode'
              142  LOAD_METHOD              startswith
              144  LOAD_STR                 'socket:['
              146  CALL_METHOD_1         1  ''
              148  POP_JUMP_IF_FALSE    28  'to 28'

 L. 841       150  LOAD_FAST                'inode'
              152  LOAD_CONST               8
              154  LOAD_CONST               None
              156  BUILD_SLICE_2         2 
              158  BINARY_SUBSCR    
              160  LOAD_CONST               None
              162  LOAD_CONST               -1
              164  BUILD_SLICE_2         2 
              166  BINARY_SUBSCR    
              168  STORE_FAST               'inode'

 L. 842       170  LOAD_FAST                'inodes'
              172  LOAD_FAST                'inode'
              174  BINARY_SUBSCR    
              176  LOAD_METHOD              append
              178  LOAD_FAST                'pid'
              180  LOAD_GLOBAL              int
              182  LOAD_FAST                'fd'
              184  CALL_FUNCTION_1       1  ''
              186  BUILD_TUPLE_2         2 
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          
              192  JUMP_BACK            28  'to 28'

 L. 843       194  LOAD_FAST                'inodes'
              196  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 80

            def get_all_inodes--- This code section failed: ---

 L. 846         0  BUILD_MAP_0           0 
                2  STORE_FAST               'inodes'

 L. 847         4  LOAD_GLOBAL              pids
                6  CALL_FUNCTION_0       0  ''
                8  GET_ITER         
               10  FOR_ITER             68  'to 68'
               12  STORE_FAST               'pid'

 L. 848        14  SETUP_FINALLY        36  'to 36'

 L. 849        16  LOAD_FAST                'inodes'
               18  LOAD_METHOD              update
               20  LOAD_FAST                'self'
               22  LOAD_METHOD              get_proc_inodes
               24  LOAD_FAST                'pid'
               26  CALL_METHOD_1         1  ''
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          
               32  POP_BLOCK        
               34  JUMP_BACK            10  'to 10'
             36_0  COME_FROM_FINALLY    14  '14'

 L. 850        36  DUP_TOP          
               38  LOAD_GLOBAL              FileNotFoundError
               40  LOAD_GLOBAL              ProcessLookupError
               42  LOAD_GLOBAL              PermissionError
               44  BUILD_TUPLE_3         3 
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    64  'to 64'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 858        56  POP_EXCEPT       
               58  JUMP_BACK            10  'to 10'
               60  POP_EXCEPT       
               62  JUMP_BACK            10  'to 10'
             64_0  COME_FROM            48  '48'
               64  END_FINALLY      
               66  JUMP_BACK            10  'to 10'

 L. 859        68  LOAD_FAST                'inodes'
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 60

            @staticmethod
            def decode_address(addr, family):
                """Accept an "ip:port" address as displayed in /proc/net/*
        and convert it into a human readable form, like:

        "0500000A:0016" -> ("10.0.0.5", 22)
        "0000000000000000FFFF00000100007F:9E49" -> ("::ffff:127.0.0.1", 40521)

        The IP address portion is a little or big endian four-byte
        hexadecimal number; that is, the least significant byte is listed
        first, so we need to reverse the order of the bytes to convert it
        to an IP address.
        The port is represented as a two-byte hexadecimal number.

        Reference:
        http://linuxdevcenter.com/pub/a/linux/2000/11/16/LinuxAdmin.html
        """
                ip, port = addr.split(':')
                port = int(port, 16)
                if not port:
                    return ()
                    if PY3:
                        ip = ip.encode('ascii')
                    if family == socket.AF_INET:
                        if LITTLE_ENDIAN:
                            ip = socket.inet_ntop(family, base64.b16decode(ip)[::-1])
                        else:
                            ip = socket.inet_ntop(family, base64.b16decode(ip))
                else:
                    ip = base64.b16decode(ip)
                try:
                    if LITTLE_ENDIAN:
                        ip = socket.inet_ntop(socket.AF_INET6, (struct.pack)(*('>4I', ), *struct.unpack('<4I', ip)))
                    else:
                        ip = socket.inet_ntop(socket.AF_INET6, (struct.pack)(*('<4I', ), *struct.unpack('<4I', ip)))
                except ValueError:
                    if not supports_ipv6():
                        raise _Ipv6UnsupportedError
                    else:
                        raise
                else:
                    return _common.addr(ip, port)

            @staticmethod
            def process_inet--- This code section failed: ---

 L. 915         0  LOAD_FAST                'file'
                2  LOAD_METHOD              endswith
                4  LOAD_STR                 '6'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'
               10  LOAD_GLOBAL              os
               12  LOAD_ATTR                path
               14  LOAD_METHOD              exists
               16  LOAD_FAST                'file'
               18  CALL_METHOD_1         1  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L. 917        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'
             26_1  COME_FROM             8  '8'

 L. 918        26  LOAD_GLOBAL              open_text
               28  LOAD_FAST                'file'
               30  LOAD_GLOBAL              BIGFILE_BUFFERING
               32  LOAD_CONST               ('buffering',)
               34  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
            36_38  SETUP_WITH          310  'to 310'
               40  STORE_FAST               'f'

 L. 919        42  LOAD_FAST                'f'
               44  LOAD_METHOD              readline
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          

 L. 920        50  LOAD_GLOBAL              enumerate
               52  LOAD_FAST                'f'
               54  LOAD_CONST               1
               56  CALL_FUNCTION_2       2  ''
               58  GET_ITER         
               60  FOR_ITER            306  'to 306'
               62  UNPACK_SEQUENCE_2     2 
               64  STORE_FAST               'lineno'
               66  STORE_FAST               'line'

 L. 921        68  SETUP_FINALLY       110  'to 110'

 L. 923        70  LOAD_FAST                'line'
               72  LOAD_METHOD              split
               74  CALL_METHOD_0         0  ''
               76  LOAD_CONST               None
               78  LOAD_CONST               10
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    

 L. 922        84  UNPACK_SEQUENCE_10    10 
               86  STORE_FAST               '_'
               88  STORE_FAST               'laddr'
               90  STORE_FAST               'raddr'
               92  STORE_FAST               'status'
               94  STORE_FAST               '_'
               96  STORE_FAST               '_'
               98  STORE_FAST               '_'
              100  STORE_FAST               '_'
              102  STORE_FAST               '_'
              104  STORE_FAST               'inode'
              106  POP_BLOCK        
              108  JUMP_FORWARD        148  'to 148'
            110_0  COME_FROM_FINALLY    68  '68'

 L. 924       110  DUP_TOP          
              112  LOAD_GLOBAL              ValueError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   146  'to 146'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 925       124  LOAD_GLOBAL              RuntimeError

 L. 926       126  LOAD_STR                 'error while parsing %s; malformed line %s %r'

 L. 927       128  LOAD_FAST                'file'

 L. 927       130  LOAD_FAST                'lineno'

 L. 927       132  LOAD_FAST                'line'

 L. 926       134  BUILD_TUPLE_3         3 
              136  BINARY_MODULO    

 L. 925       138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           116  '116'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           108  '108'

 L. 928       148  LOAD_FAST                'inode'
              150  LOAD_FAST                'inodes'
              152  COMPARE_OP               in
              154  POP_JUMP_IF_FALSE   174  'to 174'

 L. 935       156  LOAD_FAST                'inodes'
              158  LOAD_FAST                'inode'
              160  BINARY_SUBSCR    
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'pid'
              170  STORE_FAST               'fd'
              172  JUMP_FORWARD        182  'to 182'
            174_0  COME_FROM           154  '154'

 L. 937       174  LOAD_CONST               (None, -1)
              176  UNPACK_SEQUENCE_2     2 
              178  STORE_FAST               'pid'
              180  STORE_FAST               'fd'
            182_0  COME_FROM           172  '172'

 L. 938       182  LOAD_FAST                'filter_pid'
              184  LOAD_CONST               None
              186  COMPARE_OP               is-not
              188  POP_JUMP_IF_FALSE   202  'to 202'
              190  LOAD_FAST                'filter_pid'
              192  LOAD_FAST                'pid'
              194  COMPARE_OP               !=
              196  POP_JUMP_IF_FALSE   202  'to 202'

 L. 939       198  CONTINUE             60  'to 60'
              200  JUMP_BACK            60  'to 60'
            202_0  COME_FROM           196  '196'
            202_1  COME_FROM           188  '188'

 L. 941       202  LOAD_FAST                'type_'
              204  LOAD_GLOBAL              socket
              206  LOAD_ATTR                SOCK_STREAM
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   222  'to 222'

 L. 942       212  LOAD_GLOBAL              TCP_STATUSES
              214  LOAD_FAST                'status'
              216  BINARY_SUBSCR    
              218  STORE_FAST               'status'
              220  JUMP_FORWARD        228  'to 228'
            222_0  COME_FROM           210  '210'

 L. 944       222  LOAD_GLOBAL              _common
              224  LOAD_ATTR                CONN_NONE
              226  STORE_FAST               'status'
            228_0  COME_FROM           220  '220'

 L. 945       228  SETUP_FINALLY       258  'to 258'

 L. 946       230  LOAD_GLOBAL              Connections
              232  LOAD_METHOD              decode_address
              234  LOAD_FAST                'laddr'
              236  LOAD_FAST                'family'
              238  CALL_METHOD_2         2  ''
              240  STORE_FAST               'laddr'

 L. 947       242  LOAD_GLOBAL              Connections
              244  LOAD_METHOD              decode_address
              246  LOAD_FAST                'raddr'
              248  LOAD_FAST                'family'
              250  CALL_METHOD_2         2  ''
              252  STORE_FAST               'raddr'
              254  POP_BLOCK        
              256  JUMP_FORWARD        284  'to 284'
            258_0  COME_FROM_FINALLY   228  '228'

 L. 948       258  DUP_TOP          
              260  LOAD_GLOBAL              _Ipv6UnsupportedError
              262  COMPARE_OP               exception-match
          264_266  POP_JUMP_IF_FALSE   282  'to 282'
              268  POP_TOP          
              270  POP_TOP          
              272  POP_TOP          

 L. 949       274  POP_EXCEPT       
              276  JUMP_BACK            60  'to 60'
              278  POP_EXCEPT       
              280  JUMP_FORWARD        284  'to 284'
            282_0  COME_FROM           264  '264'
              282  END_FINALLY      
            284_0  COME_FROM           280  '280'
            284_1  COME_FROM           256  '256'

 L. 950       284  LOAD_FAST                'fd'
              286  LOAD_FAST                'family'
              288  LOAD_FAST                'type_'
              290  LOAD_FAST                'laddr'
              292  LOAD_FAST                'raddr'
              294  LOAD_FAST                'status'
              296  LOAD_FAST                'pid'
              298  BUILD_TUPLE_7         7 
              300  YIELD_VALUE      
              302  POP_TOP          
              304  JUMP_BACK            60  'to 60'
              306  POP_BLOCK        
              308  BEGIN_FINALLY    
            310_0  COME_FROM_WITH       36  '36'
              310  WITH_CLEANUP_START
              312  WITH_CLEANUP_FINISH
              314  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 278

            @staticmethod
            def process_unix--- This code section failed: ---

 L. 955         0  LOAD_GLOBAL              open_text
                2  LOAD_FAST                'file'
                4  LOAD_GLOBAL              BIGFILE_BUFFERING
                6  LOAD_CONST               ('buffering',)
                8  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               10  SETUP_WITH          252  'to 252'
               12  STORE_FAST               'f'

 L. 956        14  LOAD_FAST                'f'
               16  LOAD_METHOD              readline
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          

 L. 957        22  LOAD_FAST                'f'
               24  GET_ITER         
               26  FOR_ITER            248  'to 248'
               28  STORE_FAST               'line'

 L. 958        30  LOAD_FAST                'line'
               32  LOAD_METHOD              split
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'tokens'

 L. 959        38  SETUP_FINALLY        70  'to 70'

 L. 960        40  LOAD_FAST                'tokens'
               42  LOAD_CONST               0
               44  LOAD_CONST               7
               46  BUILD_SLICE_2         2 
               48  BINARY_SUBSCR    
               50  UNPACK_SEQUENCE_7     7 
               52  STORE_FAST               '_'
               54  STORE_FAST               '_'
               56  STORE_FAST               '_'
               58  STORE_FAST               '_'
               60  STORE_FAST               'type_'
               62  STORE_FAST               '_'
               64  STORE_FAST               'inode'
               66  POP_BLOCK        
               68  JUMP_FORWARD        118  'to 118'
             70_0  COME_FROM_FINALLY    38  '38'

 L. 961        70  DUP_TOP          
               72  LOAD_GLOBAL              ValueError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE   116  'to 116'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 962        84  LOAD_STR                 ' '
               86  LOAD_FAST                'line'
               88  COMPARE_OP               not-in
               90  POP_JUMP_IF_FALSE    96  'to 96'

 L. 964        92  POP_EXCEPT       
               94  JUMP_BACK            26  'to 26'
             96_0  COME_FROM            90  '90'

 L. 965        96  LOAD_GLOBAL              RuntimeError

 L. 966        98  LOAD_STR                 'error while parsing %s; malformed line %r'

 L. 967       100  LOAD_FAST                'file'

 L. 967       102  LOAD_FAST                'line'

 L. 966       104  BUILD_TUPLE_2         2 
              106  BINARY_MODULO    

 L. 965       108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
              112  POP_EXCEPT       
              114  JUMP_FORWARD        118  'to 118'
            116_0  COME_FROM            76  '76'
              116  END_FINALLY      
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM            68  '68'

 L. 968       118  LOAD_FAST                'inode'
              120  LOAD_FAST                'inodes'
              122  COMPARE_OP               in
              124  POP_JUMP_IF_FALSE   136  'to 136'

 L. 971       126  LOAD_FAST                'inodes'
              128  LOAD_FAST                'inode'
              130  BINARY_SUBSCR    
              132  STORE_FAST               'pairs'
              134  JUMP_FORWARD        142  'to 142'
            136_0  COME_FROM           124  '124'

 L. 973       136  LOAD_CONST               (None, -1)
              138  BUILD_LIST_1          1 
              140  STORE_FAST               'pairs'
            142_0  COME_FROM           134  '134'

 L. 974       142  LOAD_FAST                'pairs'
              144  GET_ITER         
              146  FOR_ITER            246  'to 246'
              148  UNPACK_SEQUENCE_2     2 
              150  STORE_FAST               'pid'
              152  STORE_FAST               'fd'

 L. 975       154  LOAD_FAST                'filter_pid'
              156  LOAD_CONST               None
              158  COMPARE_OP               is-not
              160  POP_JUMP_IF_FALSE   174  'to 174'
              162  LOAD_FAST                'filter_pid'
              164  LOAD_FAST                'pid'
              166  COMPARE_OP               !=
              168  POP_JUMP_IF_FALSE   174  'to 174'

 L. 976       170  CONTINUE            146  'to 146'
              172  JUMP_BACK           146  'to 146'
            174_0  COME_FROM           168  '168'
            174_1  COME_FROM           160  '160'

 L. 978       174  LOAD_GLOBAL              len
              176  LOAD_FAST                'tokens'
              178  CALL_FUNCTION_1       1  ''
              180  LOAD_CONST               8
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   196  'to 196'

 L. 979       186  LOAD_FAST                'tokens'
              188  LOAD_CONST               -1
              190  BINARY_SUBSCR    
              192  STORE_FAST               'path'
              194  JUMP_FORWARD        200  'to 200'
            196_0  COME_FROM           184  '184'

 L. 981       196  LOAD_STR                 ''
              198  STORE_FAST               'path'
            200_0  COME_FROM           194  '194'

 L. 982       200  LOAD_GLOBAL              _common
              202  LOAD_METHOD              socktype_to_enum
              204  LOAD_GLOBAL              int
              206  LOAD_FAST                'type_'
              208  CALL_FUNCTION_1       1  ''
              210  CALL_METHOD_1         1  ''
              212  STORE_FAST               'type_'

 L. 986       214  LOAD_STR                 ''
              216  STORE_FAST               'raddr'

 L. 987       218  LOAD_GLOBAL              _common
              220  LOAD_ATTR                CONN_NONE
              222  STORE_FAST               'status'

 L. 988       224  LOAD_FAST                'fd'
              226  LOAD_FAST                'family'
              228  LOAD_FAST                'type_'
              230  LOAD_FAST                'path'
              232  LOAD_FAST                'raddr'
              234  LOAD_FAST                'status'
              236  LOAD_FAST                'pid'
              238  BUILD_TUPLE_7         7 
              240  YIELD_VALUE      
              242  POP_TOP          
              244  JUMP_BACK           146  'to 146'
              246  JUMP_BACK            26  'to 26'
              248  POP_BLOCK        
              250  BEGIN_FINALLY    
            252_0  COME_FROM_WITH       10  '10'
              252  WITH_CLEANUP_START
              254  WITH_CLEANUP_FINISH
              256  END_FINALLY      

Parse error at or near `JUMP_BACK' instruction at offset 94

            def retrieve(self, kind, pid=None):
                if kind not in self.tmap:
                    raise ValueError('invalid %r kind argument; choose between %s' % (
                     kind, ', '.join([repr(x) for x in self.tmap])))
                else:
                    self._procfs_path = get_procfs_path()
                    if pid is not None:
                        inodes = self.get_proc_inodes(pid)
                        return inodes or []
                    else:
                        inodes = self.get_all_inodes()
                ret = set()
                for proto_name, family, type_ in self.tmap[kind]:
                    path = '%s/net/%s' % (self._procfs_path, proto_name)
                    if family in (socket.AF_INET, socket.AF_INET6):
                        ls = self.process_inet(path,
                          family, type_, inodes, filter_pid=pid)
                    else:
                        ls = self.process_unix(path,
                          family, inodes, filter_pid=pid)
                    for fd, family, type_, laddr, raddr, status, bound_pid in ls:
                        if pid:
                            conn = _common.pconn(fd, family, type_, laddr, raddr, status)
                        else:
                            conn = _common.sconn(fd, family, type_, laddr, raddr, status, bound_pid)
                        ret.add(conn)
                    else:
                        return list(ret)


        _connections = Connections()

        def net_connections(kind='inet'):
            """Return system-wide open connections."""
            return _connections.retrieve(kind)


        def net_io_counters():
            """Return network I/O statistics for every network interface
    installed on the system as a dict of raw tuples.
    """
            with open_text('%s/net/dev' % get_procfs_path()) as (f):
                lines = f.readlines()
            retdict = {}
            for line in lines[2:]:
                colon = line.rfind(':')
                assert colon > 0, repr(line)
                name = line[:colon].strip()
                fields = line[colon + 1:].strip().split()
                bytes_recv, packets_recv, errin, dropin, fifoin, framein, compressedin, multicastin, bytes_sent, packets_sent, errout, dropout, fifoout, collisionsout, carrierout, compressedout = map(int, fields)
                retdict[name] = (
                 bytes_sent, bytes_recv, packets_sent, packets_recv,
                 errin, errout, dropin, dropout)
            else:
                return retdict


        def net_if_stats():
            """Get NIC stats (isup, duplex, speed, mtu)."""
            duplex_map = {cext.DUPLEX_FULL: NIC_DUPLEX_FULL, 
             cext.DUPLEX_HALF: NIC_DUPLEX_HALF, 
             cext.DUPLEX_UNKNOWN: NIC_DUPLEX_UNKNOWN}
            names = net_io_counters().keys()
            ret = {}
            for name in names:
                try:
                    mtu = cext_posix.net_if_mtu(name)
                    isup = cext_posix.net_if_is_running(name)
                    duplex, speed = cext.net_if_duplex_speed(name)
                except OSError as err:
                    try:
                        if err.errno != errno.ENODEV:
                            raise
                    finally:
                        err = None
                        del err

                else:
                    ret[name] = _common.snicstats(isup, duplex_map[duplex], speed, mtu)
            else:
                return ret


        disk_usage = _psposix.disk_usage

        def disk_io_counters(perdisk=False):
            """Return disk I/O statistics for every disk installed on the
    system as a dict of raw tuples.
    """

            def read_procfs():
                with open_text('%s/diskstats' % get_procfs_path()) as (f):
                    lines = f.readlines()
                for line in lines:
                    fields = line.split()
                    flen = len(fields)
                    if flen == 15:
                        name = fields[3]
                        reads = int(fields[2])
                        reads_merged, rbytes, rtime, writes, writes_merged, wbytes, wtime, _, busy_time, _ = map(int, fields[4:14])
                    else:
                        if flen == 14 or flen >= 18:
                            name = fields[2]
                            reads, reads_merged, rbytes, rtime, writes, writes_merged, wbytes, wtime, _, busy_time, _ = map(int, fields[3:14])
                        else:
                            if flen == 7:
                                name = fields[2]
                                reads, rbytes, writes, wbytes = map(int, fields[3:])
                                rtime = wtime = reads_merged = writes_merged = busy_time = 0
                            else:
                                raise ValueError('not sure how to interpret line %r' % line)
                    (yield (
                     name, reads, writes, rbytes, wbytes, rtime, wtime,
                     reads_merged, writes_merged, busy_time))

            def read_sysfs():
                for block in os.listdir('/sys/block'):
                    for root, _, files in os.walk(os.path.join('/sys/block', block)):
                        if 'stat' not in files:
                            pass
                        else:
                            with open_text(os.path.join(root, 'stat')) as (f):
                                fields = f.read().strip().split()
                            name = os.path.basename(root)
                            reads, reads_merged, rbytes, rtime, writes, writes_merged, wbytes, wtime, _, busy_time = map(int, fields[:10])
                            (yield (name, reads, writes, rbytes, wbytes, rtime,
                             wtime, reads_merged, writes_merged, busy_time))

            if os.path.exists('%s/diskstats' % get_procfs_path()):
                gen = read_procfs()
            else:
                if os.path.exists('/sys/block'):
                    gen = read_sysfs()
                else:
                    raise NotImplementedError('%s/diskstats nor /sys/block filesystem are available on this system' % get_procfs_path())
            retdict = {}
            for entry in gen:
                name, reads, writes, rbytes, wbytes, rtime, wtime, reads_merged, writes_merged, busy_time = entry
                if not (perdisk or is_storage_device(name)):
                    pass
                else:
                    rbytes *= DISK_SECTOR_SIZE
                    wbytes *= DISK_SECTOR_SIZE
                    retdict[name] = (reads, writes, rbytes, wbytes, rtime, wtime,
                     reads_merged, writes_merged, busy_time)
            else:
                return retdict


        def disk_partitions(all=False):
            """Return mounted disk partitions as a list of namedtuples."""
            fstypes = set()
            procfs_path = get_procfs_path()
            with open_text('%s/filesystems' % procfs_path) as (f):
                for line in f:
                    line = line.strip()
                    if not line.startswith('nodev'):
                        fstypes.add(line.strip())
                    else:
                        fstype = line.split('\t')[1]

                if fstype == 'zfs':
                    fstypes.add('zfs')
            if procfs_path == '/proc' and os.path.isfile('/etc/mtab'):
                mounts_path = os.path.realpath('/etc/mtab')
            else:
                mounts_path = os.path.realpath('%s/self/mounts' % procfs_path)
            retlist = []
            partitions = cext.disk_partitions(mounts_path)
            for partition in partitions:
                device, mountpoint, fstype, opts = partition
                if device == 'none':
                    device = ''
                if (all or device == '' or fstype) not in fstypes:
                    pass
                else:
                    maxfile = maxpath = None
                    ntuple = _common.sdiskpart(device, mountpoint, fstype, opts, maxfile, maxpath)
                    retlist.append(ntuple)
            else:
                return retlist


        def sensors_temperatures--- This code section failed: ---

 L.1247         0  LOAD_GLOBAL              collections
                2  LOAD_METHOD              defaultdict
                4  LOAD_GLOBAL              list
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'ret'

 L.1248        10  LOAD_GLOBAL              glob
               12  LOAD_METHOD              glob
               14  LOAD_STR                 '/sys/class/hwmon/hwmon*/temp*_*'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'basenames'

 L.1252        20  LOAD_FAST                'basenames'
               22  LOAD_METHOD              extend
               24  LOAD_GLOBAL              glob
               26  LOAD_METHOD              glob
               28  LOAD_STR                 '/sys/class/hwmon/hwmon*/device/temp*_*'
               30  CALL_METHOD_1         1  ''
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L.1253        36  LOAD_GLOBAL              sorted
               38  LOAD_GLOBAL              set
               40  LOAD_LISTCOMP            '<code_object <listcomp>>'
               42  LOAD_STR                 'sensors_temperatures.<locals>.<listcomp>'
               44  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               46  LOAD_FAST                'basenames'
               48  GET_ITER         
               50  CALL_FUNCTION_1       1  ''
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'basenames'

 L.1259        58  LOAD_GLOBAL              glob
               60  LOAD_METHOD              glob

 L.1260        62  LOAD_STR                 '/sys/devices/platform/coretemp.*/hwmon/hwmon*/temp*_*'

 L.1259        64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'basenames2'

 L.1261        68  LOAD_GLOBAL              re
               70  LOAD_METHOD              compile
               72  LOAD_STR                 '/sys/devices/platform/coretemp.*/hwmon/'
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'repl'

 L.1262        78  LOAD_FAST                'basenames2'
               80  GET_ITER         
             82_0  COME_FROM           104  '104'
               82  FOR_ITER            118  'to 118'
               84  STORE_FAST               'name'

 L.1263        86  LOAD_FAST                'repl'
               88  LOAD_METHOD              sub
               90  LOAD_STR                 '/sys/class/hwmon/'
               92  LOAD_FAST                'name'
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'altname'

 L.1264        98  LOAD_FAST                'altname'
              100  LOAD_FAST                'basenames'
              102  COMPARE_OP               not-in
              104  POP_JUMP_IF_FALSE    82  'to 82'

 L.1265       106  LOAD_FAST                'basenames'
              108  LOAD_METHOD              append
              110  LOAD_FAST                'name'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  JUMP_BACK            82  'to 82'

 L.1267       118  LOAD_FAST                'basenames'
              120  GET_ITER         
          122_124  FOR_ITER            404  'to 404'
              126  STORE_FAST               'base'

 L.1268       128  SETUP_FINALLY       192  'to 192'

 L.1269       130  LOAD_FAST                'base'
              132  LOAD_STR                 '_input'
              134  BINARY_ADD       
              136  STORE_FAST               'path'

 L.1270       138  LOAD_GLOBAL              float
              140  LOAD_GLOBAL              cat
              142  LOAD_FAST                'path'
              144  CALL_FUNCTION_1       1  ''
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_CONST               1000.0
              150  BINARY_TRUE_DIVIDE
              152  STORE_FAST               'current'

 L.1271       154  LOAD_GLOBAL              os
              156  LOAD_ATTR                path
              158  LOAD_METHOD              join
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_METHOD              dirname
              166  LOAD_FAST                'base'
              168  CALL_METHOD_1         1  ''
              170  LOAD_STR                 'name'
              172  CALL_METHOD_2         2  ''
              174  STORE_FAST               'path'

 L.1272       176  LOAD_GLOBAL              cat
              178  LOAD_FAST                'path'
              180  LOAD_CONST               False
              182  LOAD_CONST               ('binary',)
              184  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              186  STORE_FAST               'unit_name'
              188  POP_BLOCK        
              190  JUMP_FORWARD        222  'to 222'
            192_0  COME_FROM_FINALLY   128  '128'

 L.1273       192  DUP_TOP          
              194  LOAD_GLOBAL              IOError
              196  LOAD_GLOBAL              OSError
              198  LOAD_GLOBAL              ValueError
              200  BUILD_TUPLE_3         3 
              202  COMPARE_OP               exception-match
              204  POP_JUMP_IF_FALSE   220  'to 220'
              206  POP_TOP          
              208  POP_TOP          
              210  POP_TOP          

 L.1282       212  POP_EXCEPT       
              214  JUMP_BACK           122  'to 122'
              216  POP_EXCEPT       
              218  JUMP_FORWARD        222  'to 222'
            220_0  COME_FROM           204  '204'
              220  END_FINALLY      
            222_0  COME_FROM           218  '218'
            222_1  COME_FROM           190  '190'

 L.1284       222  LOAD_GLOBAL              cat
              224  LOAD_FAST                'base'
              226  LOAD_STR                 '_max'
              228  BINARY_ADD       
              230  LOAD_CONST               None
              232  LOAD_CONST               ('fallback',)
              234  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              236  STORE_FAST               'high'

 L.1285       238  LOAD_GLOBAL              cat
              240  LOAD_FAST                'base'
              242  LOAD_STR                 '_crit'
              244  BINARY_ADD       
              246  LOAD_CONST               None
              248  LOAD_CONST               ('fallback',)
              250  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              252  STORE_FAST               'critical'

 L.1286       254  LOAD_GLOBAL              cat
              256  LOAD_FAST                'base'
              258  LOAD_STR                 '_label'
              260  BINARY_ADD       
              262  LOAD_STR                 ''
              264  LOAD_CONST               False
              266  LOAD_CONST               ('fallback', 'binary')
              268  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              270  STORE_FAST               'label'

 L.1288       272  LOAD_FAST                'high'
              274  LOAD_CONST               None
              276  COMPARE_OP               is-not
          278_280  POP_JUMP_IF_FALSE   326  'to 326'

 L.1289       282  SETUP_FINALLY       300  'to 300'

 L.1290       284  LOAD_GLOBAL              float
              286  LOAD_FAST                'high'
              288  CALL_FUNCTION_1       1  ''
              290  LOAD_CONST               1000.0
              292  BINARY_TRUE_DIVIDE
              294  STORE_FAST               'high'
              296  POP_BLOCK        
              298  JUMP_FORWARD        326  'to 326'
            300_0  COME_FROM_FINALLY   282  '282'

 L.1291       300  DUP_TOP          
              302  LOAD_GLOBAL              ValueError
              304  COMPARE_OP               exception-match
          306_308  POP_JUMP_IF_FALSE   324  'to 324'
              310  POP_TOP          
              312  POP_TOP          
              314  POP_TOP          

 L.1292       316  LOAD_CONST               None
              318  STORE_FAST               'high'
              320  POP_EXCEPT       
              322  JUMP_FORWARD        326  'to 326'
            324_0  COME_FROM           306  '306'
              324  END_FINALLY      
            326_0  COME_FROM           322  '322'
            326_1  COME_FROM           298  '298'
            326_2  COME_FROM           278  '278'

 L.1293       326  LOAD_FAST                'critical'
              328  LOAD_CONST               None
              330  COMPARE_OP               is-not
          332_334  POP_JUMP_IF_FALSE   380  'to 380'

 L.1294       336  SETUP_FINALLY       354  'to 354'

 L.1295       338  LOAD_GLOBAL              float
              340  LOAD_FAST                'critical'
              342  CALL_FUNCTION_1       1  ''
              344  LOAD_CONST               1000.0
              346  BINARY_TRUE_DIVIDE
              348  STORE_FAST               'critical'
              350  POP_BLOCK        
              352  JUMP_FORWARD        380  'to 380'
            354_0  COME_FROM_FINALLY   336  '336'

 L.1296       354  DUP_TOP          
              356  LOAD_GLOBAL              ValueError
              358  COMPARE_OP               exception-match
          360_362  POP_JUMP_IF_FALSE   378  'to 378'
              364  POP_TOP          
              366  POP_TOP          
              368  POP_TOP          

 L.1297       370  LOAD_CONST               None
              372  STORE_FAST               'critical'
              374  POP_EXCEPT       
              376  JUMP_FORWARD        380  'to 380'
            378_0  COME_FROM           360  '360'
              378  END_FINALLY      
            380_0  COME_FROM           376  '376'
            380_1  COME_FROM           352  '352'
            380_2  COME_FROM           332  '332'

 L.1299       380  LOAD_FAST                'ret'
              382  LOAD_FAST                'unit_name'
              384  BINARY_SUBSCR    
              386  LOAD_METHOD              append
              388  LOAD_FAST                'label'
              390  LOAD_FAST                'current'
              392  LOAD_FAST                'high'
              394  LOAD_FAST                'critical'
              396  BUILD_TUPLE_4         4 
              398  CALL_METHOD_1         1  ''
              400  POP_TOP          
              402  JUMP_BACK           122  'to 122'

 L.1302       404  LOAD_FAST                'basenames'
          406_408  POP_JUMP_IF_TRUE    864  'to 864'

 L.1303       410  LOAD_GLOBAL              glob
              412  LOAD_METHOD              glob
              414  LOAD_STR                 '/sys/class/thermal/thermal_zone*'
              416  CALL_METHOD_1         1  ''
              418  STORE_FAST               'basenames'

 L.1304       420  LOAD_GLOBAL              sorted
              422  LOAD_GLOBAL              set
              424  LOAD_FAST                'basenames'
              426  CALL_FUNCTION_1       1  ''
              428  CALL_FUNCTION_1       1  ''
              430  STORE_FAST               'basenames'

 L.1306       432  LOAD_FAST                'basenames'
              434  GET_ITER         
          436_438  FOR_ITER            864  'to 864'
              440  STORE_FAST               'base'

 L.1307       442  SETUP_FINALLY       504  'to 504'

 L.1308       444  LOAD_GLOBAL              os
              446  LOAD_ATTR                path
              448  LOAD_METHOD              join
              450  LOAD_FAST                'base'
              452  LOAD_STR                 'temp'
              454  CALL_METHOD_2         2  ''
              456  STORE_FAST               'path'

 L.1309       458  LOAD_GLOBAL              float
              460  LOAD_GLOBAL              cat
              462  LOAD_FAST                'path'
              464  CALL_FUNCTION_1       1  ''
              466  CALL_FUNCTION_1       1  ''
              468  LOAD_CONST               1000.0
              470  BINARY_TRUE_DIVIDE
              472  STORE_FAST               'current'

 L.1310       474  LOAD_GLOBAL              os
              476  LOAD_ATTR                path
              478  LOAD_METHOD              join
              480  LOAD_FAST                'base'
              482  LOAD_STR                 'type'
              484  CALL_METHOD_2         2  ''
              486  STORE_FAST               'path'

 L.1311       488  LOAD_GLOBAL              cat
              490  LOAD_FAST                'path'
              492  LOAD_CONST               False
              494  LOAD_CONST               ('binary',)
              496  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              498  STORE_FAST               'unit_name'
              500  POP_BLOCK        
              502  JUMP_FORWARD        572  'to 572'
            504_0  COME_FROM_FINALLY   442  '442'

 L.1312       504  DUP_TOP          
              506  LOAD_GLOBAL              IOError
              508  LOAD_GLOBAL              OSError
              510  LOAD_GLOBAL              ValueError
              512  BUILD_TUPLE_3         3 
              514  COMPARE_OP               exception-match
          516_518  POP_JUMP_IF_FALSE   570  'to 570'
              520  POP_TOP          
              522  STORE_FAST               'err'
              524  POP_TOP          
              526  SETUP_FINALLY       558  'to 558'

 L.1313       528  LOAD_GLOBAL              debug
              530  LOAD_STR                 'ignoring %r for file %r'
              532  LOAD_FAST                'err'
              534  LOAD_FAST                'path'
              536  BUILD_TUPLE_2         2 
              538  BINARY_MODULO    
              540  CALL_FUNCTION_1       1  ''
              542  POP_TOP          

 L.1314       544  POP_BLOCK        
              546  POP_EXCEPT       
              548  CALL_FINALLY        558  'to 558'
          550_552  JUMP_BACK           436  'to 436'
              554  POP_BLOCK        
              556  BEGIN_FINALLY    
            558_0  COME_FROM           548  '548'
            558_1  COME_FROM_FINALLY   526  '526'
              558  LOAD_CONST               None
              560  STORE_FAST               'err'
              562  DELETE_FAST              'err'
              564  END_FINALLY      
              566  POP_EXCEPT       
              568  JUMP_FORWARD        572  'to 572'
            570_0  COME_FROM           516  '516'
              570  END_FINALLY      
            572_0  COME_FROM           568  '568'
            572_1  COME_FROM           502  '502'

 L.1316       572  LOAD_GLOBAL              glob
              574  LOAD_METHOD              glob
              576  LOAD_FAST                'base'
              578  LOAD_STR                 '/trip_point*'
              580  BINARY_ADD       
              582  CALL_METHOD_1         1  ''
              584  STORE_FAST               'trip_paths'

 L.1317       586  LOAD_GLOBAL              set
              588  LOAD_LISTCOMP            '<code_object <listcomp>>'
              590  LOAD_STR                 'sensors_temperatures.<locals>.<listcomp>'
              592  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1318       594  LOAD_FAST                'trip_paths'

 L.1317       596  GET_ITER         
              598  CALL_FUNCTION_1       1  ''
              600  CALL_FUNCTION_1       1  ''
              602  STORE_FAST               'trip_points'

 L.1319       604  LOAD_CONST               None
              606  STORE_FAST               'critical'

 L.1320       608  LOAD_CONST               None
              610  STORE_FAST               'high'

 L.1321       612  LOAD_FAST                'trip_points'
              614  GET_ITER         
            616_0  COME_FROM           786  '786'
              616  FOR_ITER            838  'to 838'
              618  STORE_FAST               'trip_point'

 L.1322       620  LOAD_GLOBAL              os
              622  LOAD_ATTR                path
              624  LOAD_METHOD              join
              626  LOAD_FAST                'base'
              628  LOAD_FAST                'trip_point'
              630  LOAD_STR                 '_type'
              632  BINARY_ADD       
              634  CALL_METHOD_2         2  ''
              636  STORE_FAST               'path'

 L.1323       638  LOAD_GLOBAL              cat
              640  LOAD_FAST                'path'
              642  LOAD_STR                 ''
              644  LOAD_CONST               False
              646  LOAD_CONST               ('fallback', 'binary')
              648  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              650  STORE_FAST               'trip_type'

 L.1324       652  LOAD_FAST                'trip_type'
              654  LOAD_STR                 'critical'
              656  COMPARE_OP               ==
          658_660  POP_JUMP_IF_FALSE   690  'to 690'

 L.1325       662  LOAD_GLOBAL              cat
              664  LOAD_GLOBAL              os
              666  LOAD_ATTR                path
              668  LOAD_METHOD              join
              670  LOAD_FAST                'base'
              672  LOAD_FAST                'trip_point'
              674  LOAD_STR                 '_temp'
              676  BINARY_ADD       
              678  CALL_METHOD_2         2  ''

 L.1326       680  LOAD_CONST               None

 L.1325       682  LOAD_CONST               ('fallback',)
              684  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              686  STORE_FAST               'critical'
              688  JUMP_FORWARD        726  'to 726'
            690_0  COME_FROM           658  '658'

 L.1327       690  LOAD_FAST                'trip_type'
              692  LOAD_STR                 'high'
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   726  'to 726'

 L.1328       700  LOAD_GLOBAL              cat
              702  LOAD_GLOBAL              os
              704  LOAD_ATTR                path
              706  LOAD_METHOD              join
              708  LOAD_FAST                'base'
              710  LOAD_FAST                'trip_point'
              712  LOAD_STR                 '_temp'
              714  BINARY_ADD       
              716  CALL_METHOD_2         2  ''

 L.1329       718  LOAD_CONST               None

 L.1328       720  LOAD_CONST               ('fallback',)
              722  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              724  STORE_FAST               'high'
            726_0  COME_FROM           696  '696'
            726_1  COME_FROM           688  '688'

 L.1331       726  LOAD_FAST                'high'
              728  LOAD_CONST               None
              730  COMPARE_OP               is-not
          732_734  POP_JUMP_IF_FALSE   780  'to 780'

 L.1332       736  SETUP_FINALLY       754  'to 754'

 L.1333       738  LOAD_GLOBAL              float
              740  LOAD_FAST                'high'
              742  CALL_FUNCTION_1       1  ''
              744  LOAD_CONST               1000.0
              746  BINARY_TRUE_DIVIDE
              748  STORE_FAST               'high'
              750  POP_BLOCK        
              752  JUMP_FORWARD        780  'to 780'
            754_0  COME_FROM_FINALLY   736  '736'

 L.1334       754  DUP_TOP          
              756  LOAD_GLOBAL              ValueError
              758  COMPARE_OP               exception-match
          760_762  POP_JUMP_IF_FALSE   778  'to 778'
              764  POP_TOP          
              766  POP_TOP          
              768  POP_TOP          

 L.1335       770  LOAD_CONST               None
              772  STORE_FAST               'high'
              774  POP_EXCEPT       
              776  JUMP_FORWARD        780  'to 780'
            778_0  COME_FROM           760  '760'
              778  END_FINALLY      
            780_0  COME_FROM           776  '776'
            780_1  COME_FROM           752  '752'
            780_2  COME_FROM           732  '732'

 L.1336       780  LOAD_FAST                'critical'
              782  LOAD_CONST               None
              784  COMPARE_OP               is-not
          786_788  POP_JUMP_IF_FALSE   616  'to 616'

 L.1337       790  SETUP_FINALLY       808  'to 808'

 L.1338       792  LOAD_GLOBAL              float
              794  LOAD_FAST                'critical'
              796  CALL_FUNCTION_1       1  ''
              798  LOAD_CONST               1000.0
              800  BINARY_TRUE_DIVIDE
              802  STORE_FAST               'critical'
              804  POP_BLOCK        
              806  JUMP_BACK           616  'to 616'
            808_0  COME_FROM_FINALLY   790  '790'

 L.1339       808  DUP_TOP          
              810  LOAD_GLOBAL              ValueError
              812  COMPARE_OP               exception-match
          814_816  POP_JUMP_IF_FALSE   832  'to 832'
              818  POP_TOP          
              820  POP_TOP          
              822  POP_TOP          

 L.1340       824  LOAD_CONST               None
              826  STORE_FAST               'critical'
              828  POP_EXCEPT       
              830  JUMP_BACK           616  'to 616'
            832_0  COME_FROM           814  '814'
              832  END_FINALLY      
          834_836  JUMP_BACK           616  'to 616'

 L.1342       838  LOAD_FAST                'ret'
              840  LOAD_FAST                'unit_name'
              842  BINARY_SUBSCR    
              844  LOAD_METHOD              append
              846  LOAD_STR                 ''
              848  LOAD_FAST                'current'
              850  LOAD_FAST                'high'
              852  LOAD_FAST                'critical'
              854  BUILD_TUPLE_4         4 
              856  CALL_METHOD_1         1  ''
              858  POP_TOP          
          860_862  JUMP_BACK           436  'to 436'
            864_0  COME_FROM           406  '406'

 L.1344       864  LOAD_GLOBAL              dict
              866  LOAD_FAST                'ret'
              868  CALL_FUNCTION_1       1  ''
              870  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 216


        def sensors_fans--- This code section failed: ---

 L.1357         0  LOAD_GLOBAL              collections
                2  LOAD_METHOD              defaultdict
                4  LOAD_GLOBAL              list
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'ret'

 L.1358        10  LOAD_GLOBAL              glob
               12  LOAD_METHOD              glob
               14  LOAD_STR                 '/sys/class/hwmon/hwmon*/fan*_*'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'basenames'

 L.1359        20  LOAD_FAST                'basenames'
               22  POP_JUMP_IF_TRUE     34  'to 34'

 L.1362        24  LOAD_GLOBAL              glob
               26  LOAD_METHOD              glob
               28  LOAD_STR                 '/sys/class/hwmon/hwmon*/device/fan*_*'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'basenames'
             34_0  COME_FROM            22  '22'

 L.1364        34  LOAD_GLOBAL              sorted
               36  LOAD_GLOBAL              set
               38  LOAD_LISTCOMP            '<code_object <listcomp>>'
               40  LOAD_STR                 'sensors_fans.<locals>.<listcomp>'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               44  LOAD_FAST                'basenames'
               46  GET_ITER         
               48  CALL_FUNCTION_1       1  ''
               50  CALL_FUNCTION_1       1  ''
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'basenames'

 L.1365        56  LOAD_FAST                'basenames'
               58  GET_ITER         
               60  FOR_ITER            220  'to 220'
               62  STORE_FAST               'base'

 L.1366        64  SETUP_FINALLY        86  'to 86'

 L.1367        66  LOAD_GLOBAL              int
               68  LOAD_GLOBAL              cat
               70  LOAD_FAST                'base'
               72  LOAD_STR                 '_input'
               74  BINARY_ADD       
               76  CALL_FUNCTION_1       1  ''
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'current'
               82  POP_BLOCK        
               84  JUMP_FORWARD        148  'to 148'
             86_0  COME_FROM_FINALLY    64  '64'

 L.1368        86  DUP_TOP          
               88  LOAD_GLOBAL              IOError
               90  LOAD_GLOBAL              OSError
               92  BUILD_TUPLE_2         2 
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   146  'to 146'
               98  POP_TOP          
              100  STORE_FAST               'err'
              102  POP_TOP          
              104  SETUP_FINALLY       134  'to 134'

 L.1369       106  LOAD_GLOBAL              warnings
              108  LOAD_METHOD              warn
              110  LOAD_STR                 'ignoring %r'
              112  LOAD_FAST                'err'
              114  BINARY_MODULO    
              116  LOAD_GLOBAL              RuntimeWarning
              118  CALL_METHOD_2         2  ''
              120  POP_TOP          

 L.1370       122  POP_BLOCK        
              124  POP_EXCEPT       
              126  CALL_FINALLY        134  'to 134'
              128  JUMP_BACK            60  'to 60'
              130  POP_BLOCK        
              132  BEGIN_FINALLY    
            134_0  COME_FROM           126  '126'
            134_1  COME_FROM_FINALLY   104  '104'
              134  LOAD_CONST               None
              136  STORE_FAST               'err'
              138  DELETE_FAST              'err'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM            96  '96'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            84  '84'

 L.1371       148  LOAD_GLOBAL              cat
              150  LOAD_GLOBAL              os
              152  LOAD_ATTR                path
              154  LOAD_METHOD              join
              156  LOAD_GLOBAL              os
              158  LOAD_ATTR                path
              160  LOAD_METHOD              dirname
              162  LOAD_FAST                'base'
              164  CALL_METHOD_1         1  ''
              166  LOAD_STR                 'name'
              168  CALL_METHOD_2         2  ''

 L.1372       170  LOAD_CONST               False

 L.1371       172  LOAD_CONST               ('binary',)
              174  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              176  STORE_FAST               'unit_name'

 L.1373       178  LOAD_GLOBAL              cat
              180  LOAD_FAST                'base'
              182  LOAD_STR                 '_label'
              184  BINARY_ADD       
              186  LOAD_STR                 ''
              188  LOAD_CONST               False
              190  LOAD_CONST               ('fallback', 'binary')
              192  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              194  STORE_FAST               'label'

 L.1374       196  LOAD_FAST                'ret'
              198  LOAD_FAST                'unit_name'
              200  BINARY_SUBSCR    
              202  LOAD_METHOD              append
              204  LOAD_GLOBAL              _common
              206  LOAD_METHOD              sfan
              208  LOAD_FAST                'label'
              210  LOAD_FAST                'current'
              212  CALL_METHOD_2         2  ''
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
              218  JUMP_BACK            60  'to 60'

 L.1376       220  LOAD_GLOBAL              dict
              222  LOAD_FAST                'ret'
              224  CALL_FUNCTION_1       1  ''
              226  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 126


        def sensors_battery():
            """Return battery information.
    Implementation note: it appears /sys/class/power_supply/BAT0/
    directory structure may vary and provide files with the same
    meaning but under different names, see:
    https://github.com/giampaolo/psutil/issues/966
    """
            null = object()

            def multi_cat(*paths):
                for path in paths:
                    ret = cat(path, fallback=null)
                    if ret != null:
                        return int(ret) if ret.isdigit() else ret

            bats = [x for x in os.listdir(POWER_SUPPLY_PATH) if not x.startswith('BAT') if 'battery' in x.lower()]
            if not bats:
                return
            root = os.path.join(POWER_SUPPLY_PATH, sorted(bats)[0])
            energy_now = multi_cat(root + '/energy_now', root + '/charge_now')
            power_now = multi_cat(root + '/power_now', root + '/current_now')
            energy_full = multi_cat(root + '/energy_full', root + '/charge_full')
            time_to_empty = multi_cat(root + '/time_to_empty_now')
            if energy_full is not None and energy_now is not None:
                try:
                    percent = 100.0 * energy_now / energy_full
                except ZeroDivisionError:
                    percent = 0.0

            else:
                percent = int(cat((root + '/capacity'), fallback=(-1)))
                if percent == -1:
                    return
            power_plugged = None
            online = multi_cat(os.path.join(POWER_SUPPLY_PATH, 'AC0/online'), os.path.join(POWER_SUPPLY_PATH, 'AC/online'))
            if online is not None:
                power_plugged = online == 1
            else:
                status = cat((root + '/status'), fallback='', binary=False).lower()
                if status == 'discharging':
                    power_plugged = False
                else:
                    if status in ('charging', 'full'):
                        power_plugged = True
                    elif power_plugged:
                        secsleft = _common.POWER_TIME_UNLIMITED
                    else:
                        if energy_now is not None and power_now is not None:
                            try:
                                secsleft = int(energy_now / power_now * 3600)
                            except ZeroDivisionError:
                                secsleft = _common.POWER_TIME_UNKNOWN

                        else:
                            if time_to_empty is not None:
                                secsleft = int(time_to_empty * 60)
                                if secsleft < 0:
                                    secsleft = _common.POWER_TIME_UNKNOWN
                            else:
                                secsleft = _common.POWER_TIME_UNKNOWN
                    return _common.sbattery(percent, secsleft, power_plugged)


        def users():
            """Return currently connected users as a list of namedtuples."""
            retlist = []
            rawlist = cext.users()
            for item in rawlist:
                user, tty, hostname, tstamp, user_process, pid = item
                if not user_process:
                    pass
                else:
                    if hostname in (':0.0', ':0'):
                        hostname = 'localhost'
                    nt = _common.suser(user, tty or None, hostname, tstamp, pid)
                    retlist.append(nt)
            else:
                return retlist


        def boot_time--- This code section failed: ---

 L.1494         0  LOAD_STR                 '%s/stat'
                2  LOAD_GLOBAL              get_procfs_path
                4  CALL_FUNCTION_0       0  ''
                6  BINARY_MODULO    
                8  STORE_FAST               'path'

 L.1495        10  LOAD_GLOBAL              open_binary
               12  LOAD_FAST                'path'
               14  CALL_FUNCTION_1       1  ''
               16  SETUP_WITH          100  'to 100'
               18  STORE_FAST               'f'

 L.1496        20  LOAD_FAST                'f'
               22  GET_ITER         
             24_0  COME_FROM            36  '36'
               24  FOR_ITER             84  'to 84'
               26  STORE_FAST               'line'

 L.1497        28  LOAD_FAST                'line'
               30  LOAD_METHOD              startswith
               32  LOAD_CONST               b'btime'
               34  CALL_METHOD_1         1  ''
               36  POP_JUMP_IF_FALSE    24  'to 24'

 L.1498        38  LOAD_GLOBAL              float
               40  LOAD_FAST                'line'
               42  LOAD_METHOD              strip
               44  CALL_METHOD_0         0  ''
               46  LOAD_METHOD              split
               48  CALL_METHOD_0         0  ''
               50  LOAD_CONST               1
               52  BINARY_SUBSCR    
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'ret'

 L.1499        58  LOAD_FAST                'ret'
               60  STORE_GLOBAL             BOOT_TIME

 L.1500        62  LOAD_FAST                'ret'
               64  ROT_TWO          
               66  POP_TOP          
               68  POP_BLOCK        
               70  ROT_TWO          
               72  BEGIN_FINALLY    
               74  WITH_CLEANUP_START
               76  WITH_CLEANUP_FINISH
               78  POP_FINALLY           0  ''
               80  RETURN_VALUE     
               82  JUMP_BACK            24  'to 24'

 L.1501        84  LOAD_GLOBAL              RuntimeError

 L.1502        86  LOAD_STR                 "line 'btime' not found in %s"
               88  LOAD_FAST                'path'
               90  BINARY_MODULO    

 L.1501        92  CALL_FUNCTION_1       1  ''
               94  RAISE_VARARGS_1       1  'exception instance'
               96  POP_BLOCK        
               98  BEGIN_FINALLY    
            100_0  COME_FROM_WITH       16  '16'
              100  WITH_CLEANUP_START
              102  WITH_CLEANUP_FINISH
              104  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 68


        def pids():
            """Returns a list of PIDs currently running on the system."""
            return [int(x) for x in os.listdir(b(get_procfs_path())) if x.isdigit()]


        def pid_exists--- This code section failed: ---

 L.1519         0  LOAD_GLOBAL              _psposix
                2  LOAD_METHOD              pid_exists
                4  LOAD_FAST                'pid'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L.1520        10  LOAD_CONST               False
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.1530        14  SETUP_FINALLY       128  'to 128'

 L.1534        16  LOAD_STR                 '%s/%s/status'
               18  LOAD_GLOBAL              get_procfs_path
               20  CALL_FUNCTION_0       0  ''
               22  LOAD_FAST                'pid'
               24  BUILD_TUPLE_2         2 
               26  BINARY_MODULO    
               28  STORE_FAST               'path'

 L.1535        30  LOAD_GLOBAL              open_binary
               32  LOAD_FAST                'path'
               34  CALL_FUNCTION_1       1  ''
               36  SETUP_WITH          118  'to 118'
               38  STORE_FAST               'f'

 L.1536        40  LOAD_FAST                'f'
               42  GET_ITER         
             44_0  COME_FROM            56  '56'
               44  FOR_ITER            102  'to 102'
               46  STORE_FAST               'line'

 L.1537        48  LOAD_FAST                'line'
               50  LOAD_METHOD              startswith
               52  LOAD_CONST               b'Tgid:'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE    44  'to 44'

 L.1538        58  LOAD_GLOBAL              int
               60  LOAD_FAST                'line'
               62  LOAD_METHOD              split
               64  CALL_METHOD_0         0  ''
               66  LOAD_CONST               1
               68  BINARY_SUBSCR    
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               'tgid'

 L.1541        74  LOAD_FAST                'tgid'
               76  LOAD_FAST                'pid'
               78  COMPARE_OP               ==
               80  ROT_TWO          
               82  POP_TOP          
               84  POP_BLOCK        
               86  ROT_TWO          
               88  BEGIN_FINALLY    
               90  WITH_CLEANUP_START
               92  WITH_CLEANUP_FINISH
               94  POP_FINALLY           0  ''
               96  POP_BLOCK        
               98  RETURN_VALUE     
              100  JUMP_BACK            44  'to 44'

 L.1542       102  LOAD_GLOBAL              ValueError
              104  LOAD_STR                 "'Tgid' line not found in %s"
              106  LOAD_FAST                'path'
              108  BINARY_MODULO    
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM_WITH       36  '36'
              118  WITH_CLEANUP_START
              120  WITH_CLEANUP_FINISH
              122  END_FINALLY      
              124  POP_BLOCK        
              126  JUMP_FORWARD        162  'to 162'
            128_0  COME_FROM_FINALLY    14  '14'

 L.1543       128  DUP_TOP          
              130  LOAD_GLOBAL              EnvironmentError
              132  LOAD_GLOBAL              ValueError
              134  BUILD_TUPLE_2         2 
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   160  'to 160'
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L.1544       146  LOAD_FAST                'pid'
              148  LOAD_GLOBAL              pids
              150  CALL_FUNCTION_0       0  ''
              152  COMPARE_OP               in
              154  ROT_FOUR         
              156  POP_EXCEPT       
              158  RETURN_VALUE     
            160_0  COME_FROM           138  '138'
              160  END_FINALLY      
            162_0  COME_FROM           126  '126'

Parse error at or near `POP_BLOCK' instruction at offset 84


        def ppid_map():
            """Obtain a {pid: ppid, ...} dict for all running processes in
    one shot. Used to speed up Process.children().
    """
            ret = {}
            procfs_path = get_procfs_path()
            for pid in pids():
                try:
                    with open_binary('%s/%s/stat' % (procfs_path, pid)) as (f):
                        data = f.read()
                except (FileNotFoundError, ProcessLookupError):
                    pass
                else:
                    rpar = data.rfind(b')')
                    dset = data[rpar + 2:].split()
                    ppid = int(dset[1])
                    ret[pid] = ppid
            else:
                return ret


        def wrap_exceptions(fun):
            """Decorator which translates bare OSError and IOError exceptions
    into NoSuchProcess and AccessDenied.
    """

            @functools.wraps(fun)
            def wrapper--- This code section failed: ---

 L.1575         0  SETUP_FINALLY        20  'to 20'

 L.1576         2  LOAD_DEREF               'fun'
                4  LOAD_FAST                'self'
                6  BUILD_TUPLE_1         1 
                8  LOAD_FAST                'args'
               10  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               12  LOAD_FAST                'kwargs'
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.1577        20  DUP_TOP          
               22  LOAD_GLOBAL              PermissionError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    52  'to 52'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.1578        34  LOAD_GLOBAL              AccessDenied
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                pid
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _name
               44  CALL_FUNCTION_2       2  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_EXCEPT       
               50  JUMP_FORWARD        144  'to 144'
             52_0  COME_FROM            26  '26'

 L.1579        52  DUP_TOP          
               54  LOAD_GLOBAL              ProcessLookupError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    84  'to 84'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.1580        66  LOAD_GLOBAL              NoSuchProcess
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                pid
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _name
               76  CALL_FUNCTION_2       2  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  POP_EXCEPT       
               82  JUMP_FORWARD        144  'to 144'
             84_0  COME_FROM            58  '58'

 L.1581        84  DUP_TOP          
               86  LOAD_GLOBAL              FileNotFoundError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   142  'to 142'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.1582        98  LOAD_GLOBAL              os
              100  LOAD_ATTR                path
              102  LOAD_METHOD              exists
              104  LOAD_STR                 '%s/%s'
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _procfs_path
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                pid
              114  BUILD_TUPLE_2         2 
              116  BINARY_MODULO    
              118  CALL_METHOD_1         1  ''
              120  POP_JUMP_IF_TRUE    136  'to 136'

 L.1583       122  LOAD_GLOBAL              NoSuchProcess
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                pid
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                _name
              132  CALL_FUNCTION_2       2  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           120  '120'

 L.1586       136  RAISE_VARARGS_0       0  'reraise'
              138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM            90  '90'
              142  END_FINALLY      
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM            82  '82'
            144_2  COME_FROM            50  '50'

Parse error at or near `POP_TOP' instruction at offset 30

            return wrapper


        class Process(object):
            __doc__ = 'Linux process implementation.'
            __slots__ = [
             'pid', '_name', '_ppid', '_procfs_path', '_cache']

            def __init__(self, pid):
                self.pid = pid
                self._name = None
                self._ppid = None
                self._procfs_path = get_procfs_path()

            def _assert_alive(self):
                """Raise NSP if the process disappeared on us."""
                os.stat('%s/%s' % (self._procfs_path, self.pid))

            @wrap_exceptions
            @memoize_when_activated
            def _parse_stat_file(self):
                """Parse /proc/{pid}/stat file and return a dict with various
        process info.
        Using "man proc" as a reference: where "man proc" refers to
        position N always substract 3 (e.g ppid position 4 in
        'man proc' == position 1 in here).
        The return value is cached in case oneshot() ctx manager is
        in use.
        """
                with open_binary('%s/%s/stat' % (self._procfs_path, self.pid)) as (f):
                    data = f.read()
                rpar = data.rfind(b')')
                name = data[data.find(b'(') + 1:rpar]
                fields = data[rpar + 2:].split()
                ret = {}
                ret['name'] = name
                ret['status'] = fields[0]
                ret['ppid'] = fields[1]
                ret['ttynr'] = fields[4]
                ret['utime'] = fields[11]
                ret['stime'] = fields[12]
                ret['children_utime'] = fields[13]
                ret['children_stime'] = fields[14]
                ret['create_time'] = fields[19]
                ret['cpu_num'] = fields[36]
                ret['blkio_ticks'] = fields[39]
                return ret

            @wrap_exceptions
            @memoize_when_activated
            def _read_status_file--- This code section failed: ---

 L.1649         0  LOAD_GLOBAL              open_binary
                2  LOAD_STR                 '%s/%s/status'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _procfs_path
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                pid
               12  BUILD_TUPLE_2         2 
               14  BINARY_MODULO    
               16  CALL_FUNCTION_1       1  ''
               18  SETUP_WITH           42  'to 42'
               20  STORE_FAST               'f'

 L.1650        22  LOAD_FAST                'f'
               24  LOAD_METHOD              read
               26  CALL_METHOD_0         0  ''
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  RETURN_VALUE     
             42_0  COME_FROM_WITH       18  '18'
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 30

            @wrap_exceptions
            @memoize_when_activated
            def _read_smaps_file--- This code section failed: ---

 L.1655         0  LOAD_GLOBAL              open_binary
                2  LOAD_STR                 '%s/%s/smaps'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _procfs_path
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                pid
               12  BUILD_TUPLE_2         2 
               14  BINARY_MODULO    

 L.1656        16  LOAD_GLOBAL              BIGFILE_BUFFERING

 L.1655        18  LOAD_CONST               ('buffering',)
               20  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               22  SETUP_WITH           50  'to 50'

 L.1656        24  STORE_FAST               'f'

 L.1657        26  LOAD_FAST                'f'
               28  LOAD_METHOD              read
               30  CALL_METHOD_0         0  ''
               32  LOAD_METHOD              strip
               34  CALL_METHOD_0         0  ''
               36  POP_BLOCK        
               38  ROT_TWO          
               40  BEGIN_FINALLY    
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  RETURN_VALUE     
             50_0  COME_FROM_WITH       22  '22'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 38

            def oneshot_enter(self):
                self._parse_stat_file.cache_activate(self)
                self._read_status_file.cache_activate(self)
                self._read_smaps_file.cache_activate(self)

            def oneshot_exit(self):
                self._parse_stat_file.cache_deactivate(self)
                self._read_status_file.cache_deactivate(self)
                self._read_smaps_file.cache_deactivate(self)

            @wrap_exceptions
            def name(self):
                name = self._parse_stat_file()['name']
                if PY3:
                    name = decode(name)
                return name

            def exe--- This code section failed: ---

 L.1678         0  SETUP_FINALLY        24  'to 24'

 L.1679         2  LOAD_GLOBAL              readlink
                4  LOAD_STR                 '%s/%s/exe'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _procfs_path
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                pid
               14  BUILD_TUPLE_2         2 
               16  BINARY_MODULO    
               18  CALL_FUNCTION_1       1  ''
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.1680        24  DUP_TOP          
               26  LOAD_GLOBAL              FileNotFoundError
               28  LOAD_GLOBAL              ProcessLookupError
               30  BUILD_TUPLE_2         2 
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE   120  'to 120'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.1684        42  LOAD_GLOBAL              os
               44  LOAD_ATTR                path
               46  LOAD_METHOD              lexists
               48  LOAD_STR                 '%s/%s'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _procfs_path
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                pid
               58  BUILD_TUPLE_2         2 
               60  BINARY_MODULO    
               62  CALL_METHOD_1         1  ''
               64  POP_JUMP_IF_FALSE    72  'to 72'

 L.1685        66  POP_EXCEPT       
               68  LOAD_STR                 ''
               70  RETURN_VALUE     
             72_0  COME_FROM            64  '64'

 L.1687        72  LOAD_GLOBAL              pid_exists
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                pid
               78  CALL_FUNCTION_1       1  ''
               80  POP_JUMP_IF_TRUE     98  'to 98'

 L.1688        82  LOAD_GLOBAL              NoSuchProcess
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                pid
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _name
               92  CALL_FUNCTION_2       2  ''
               94  RAISE_VARARGS_1       1  'exception instance'
               96  JUMP_FORWARD        116  'to 116'
             98_0  COME_FROM            80  '80'

 L.1690        98  LOAD_GLOBAL              ZombieProcess
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                pid
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _name
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _ppid
              112  CALL_FUNCTION_3       3  ''
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM            96  '96'
              116  POP_EXCEPT       
              118  JUMP_FORWARD        154  'to 154'
            120_0  COME_FROM            34  '34'

 L.1691       120  DUP_TOP          
              122  LOAD_GLOBAL              PermissionError
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   152  'to 152'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L.1692       134  LOAD_GLOBAL              AccessDenied
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                pid
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                _name
              144  CALL_FUNCTION_2       2  ''
              146  RAISE_VARARGS_1       1  'exception instance'
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
            152_0  COME_FROM           126  '126'
              152  END_FINALLY      
            154_0  COME_FROM           150  '150'
            154_1  COME_FROM           118  '118'

Parse error at or near `POP_TOP' instruction at offset 38

            @wrap_exceptions
            def cmdline(self):
                with open_text('%s/%s/cmdline' % (self._procfs_path, self.pid)) as (f):
                    data = f.read()
                if not data:
                    return []
                sep = '\x00' if data.endswith('\x00') else ' '
                if data.endswith(sep):
                    data = data[:-1]
                cmdline = data.split(sep)
                if sep == '\x00':
                    if len(cmdline) == 1:
                        if ' ' in data:
                            cmdline = data.split(' ')
                return cmdline

            @wrap_exceptions
            def environ(self):
                with open_text('%s/%s/environ' % (self._procfs_path, self.pid)) as (f):
                    data = f.read()
                return parse_environ_block(data)

            @wrap_exceptions
            def terminal--- This code section failed: ---

 L.1727         0  LOAD_GLOBAL              int
                2  LOAD_FAST                'self'
                4  LOAD_METHOD              _parse_stat_file
                6  CALL_METHOD_0         0  ''
                8  LOAD_STR                 'ttynr'
               10  BINARY_SUBSCR    
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'tty_nr'

 L.1728        16  LOAD_GLOBAL              _psposix
               18  LOAD_METHOD              get_terminal_map
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'tmap'

 L.1729        24  SETUP_FINALLY        36  'to 36'

 L.1730        26  LOAD_FAST                'tmap'
               28  LOAD_FAST                'tty_nr'
               30  BINARY_SUBSCR    
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    24  '24'

 L.1731        36  DUP_TOP          
               38  LOAD_GLOBAL              KeyError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    56  'to 56'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L.1732        50  POP_EXCEPT       
               52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            42  '42'
               56  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 46

            if os.path.exists('/proc/%s/io' % os.getpid()):

                @wrap_exceptions
                def io_counters--- This code section failed: ---

 L.1738         0  LOAD_STR                 '%s/%s/io'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _procfs_path
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                pid
               10  BUILD_TUPLE_2         2 
               12  BINARY_MODULO    
               14  STORE_FAST               'fname'

 L.1739        16  BUILD_MAP_0           0 
               18  STORE_FAST               'fields'

 L.1740        20  LOAD_GLOBAL              open_binary
               22  LOAD_FAST                'fname'
               24  CALL_FUNCTION_1       1  ''
               26  SETUP_WITH          112  'to 112'
               28  STORE_FAST               'f'

 L.1741        30  LOAD_FAST                'f'
               32  GET_ITER         
             34_0  COME_FROM            48  '48'
               34  FOR_ITER            108  'to 108'
               36  STORE_FAST               'line'

 L.1743        38  LOAD_FAST                'line'
               40  LOAD_METHOD              strip
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'line'

 L.1744        46  LOAD_FAST                'line'
               48  POP_JUMP_IF_FALSE    34  'to 34'

 L.1745        50  SETUP_FINALLY        70  'to 70'

 L.1746        52  LOAD_FAST                'line'
               54  LOAD_METHOD              split
               56  LOAD_CONST               b': '
               58  CALL_METHOD_1         1  ''
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'name'
               64  STORE_FAST               'value'
               66  POP_BLOCK        
               68  JUMP_FORWARD         94  'to 94'
             70_0  COME_FROM_FINALLY    50  '50'

 L.1747        70  DUP_TOP          
               72  LOAD_GLOBAL              ValueError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE    92  'to 92'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L.1749        84  POP_EXCEPT       
               86  JUMP_BACK            34  'to 34'
               88  POP_EXCEPT       
               90  JUMP_BACK            34  'to 34'
             92_0  COME_FROM            76  '76'
               92  END_FINALLY      
             94_0  COME_FROM            68  '68'

 L.1751        94  LOAD_GLOBAL              int
               96  LOAD_FAST                'value'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_FAST                'fields'
              102  LOAD_FAST                'name'
              104  STORE_SUBSCR     
              106  JUMP_BACK            34  'to 34'
              108  POP_BLOCK        
              110  BEGIN_FINALLY    
            112_0  COME_FROM_WITH       26  '26'
              112  WITH_CLEANUP_START
              114  WITH_CLEANUP_FINISH
              116  END_FINALLY      

 L.1752       118  LOAD_FAST                'fields'
              120  POP_JUMP_IF_TRUE    134  'to 134'

 L.1753       122  LOAD_GLOBAL              RuntimeError
              124  LOAD_STR                 '%s file was empty'
              126  LOAD_FAST                'fname'
              128  BINARY_MODULO    
              130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           120  '120'

 L.1754       134  SETUP_FINALLY       180  'to 180'

 L.1755       136  LOAD_GLOBAL              pio

 L.1756       138  LOAD_FAST                'fields'
              140  LOAD_CONST               b'syscr'
              142  BINARY_SUBSCR    

 L.1757       144  LOAD_FAST                'fields'
              146  LOAD_CONST               b'syscw'
              148  BINARY_SUBSCR    

 L.1758       150  LOAD_FAST                'fields'
              152  LOAD_CONST               b'read_bytes'
              154  BINARY_SUBSCR    

 L.1759       156  LOAD_FAST                'fields'
              158  LOAD_CONST               b'write_bytes'
              160  BINARY_SUBSCR    

 L.1760       162  LOAD_FAST                'fields'
              164  LOAD_CONST               b'rchar'
              166  BINARY_SUBSCR    

 L.1761       168  LOAD_FAST                'fields'
              170  LOAD_CONST               b'wchar'
              172  BINARY_SUBSCR    

 L.1755       174  CALL_FUNCTION_6       6  ''
              176  POP_BLOCK        
              178  RETURN_VALUE     
            180_0  COME_FROM_FINALLY   134  '134'

 L.1763       180  DUP_TOP          
              182  LOAD_GLOBAL              KeyError
              184  COMPARE_OP               exception-match
              186  POP_JUMP_IF_FALSE   234  'to 234'
              188  POP_TOP          
              190  STORE_FAST               'err'
              192  POP_TOP          
              194  SETUP_FINALLY       222  'to 222'

 L.1764       196  LOAD_GLOBAL              ValueError
              198  LOAD_STR                 '%r field was not found in %s; found fields are %r'

 L.1765       200  LOAD_FAST                'err'
              202  LOAD_CONST               0
              204  BINARY_SUBSCR    
              206  LOAD_FAST                'fname'
              208  LOAD_FAST                'fields'
              210  BUILD_TUPLE_3         3 

 L.1764       212  BINARY_MODULO    
              214  CALL_FUNCTION_1       1  ''
              216  RAISE_VARARGS_1       1  'exception instance'
              218  POP_BLOCK        
              220  BEGIN_FINALLY    
            222_0  COME_FROM_FINALLY   194  '194'
              222  LOAD_CONST               None
              224  STORE_FAST               'err'
              226  DELETE_FAST              'err'
              228  END_FINALLY      
              230  POP_EXCEPT       
              232  JUMP_FORWARD        236  'to 236'
            234_0  COME_FROM           186  '186'
              234  END_FINALLY      
            236_0  COME_FROM           232  '232'

Parse error at or near `POP_EXCEPT' instruction at offset 88

            else:

                @wrap_exceptions
                def cpu_times(self):
                    values = self._parse_stat_file()
                    utime = float(values['utime']) / CLOCK_TICKS
                    stime = float(values['stime']) / CLOCK_TICKS
                    children_utime = float(values['children_utime']) / CLOCK_TICKS
                    children_stime = float(values['children_stime']) / CLOCK_TICKS
                    iowait = float(values['blkio_ticks']) / CLOCK_TICKS
                    return pcputimes(utime, stime, children_utime, children_stime, iowait)

                @wrap_exceptions
                def cpu_num(self):
                    """What CPU the process is on."""
                    return int(self._parse_stat_file()['cpu_num'])

                @wrap_exceptions
                def wait(self, timeout=None):
                    return _psposix.wait_pid(self.pid, timeout, self._name)

                @wrap_exceptions
                def create_time(self):
                    global BOOT_TIME
                    ctime = float(self._parse_stat_file()['create_time'])
                    bt = BOOT_TIME or boot_time()
                    return ctime / CLOCK_TICKS + bt

                @wrap_exceptions
                def memory_info(self):
                    with open_binary('%s/%s/statm' % (self._procfs_path, self.pid)) as (f):
                        vms, rss, shared, text, lib, data, dirty = [int(x) * PAGESIZE for x in f.readline().split()[:7]]
                    return pmem(rss, vms, shared, text, lib, data, dirty)

                if HAS_SMAPS:

                    @wrap_exceptions
                    def memory_full_info(self, _private_re=re.compile(b'\\nPrivate.*:\\s+(\\d+)'), _pss_re=re.compile(b'\\nPss\\:\\s+(\\d+)'), _swap_re=re.compile(b'\\nSwap\\:\\s+(\\d+)')):
                        basic_mem = self.memory_info()
                        smaps_data = self._read_smaps_file()
                        uss = sum(map(int, _private_re.findall(smaps_data))) * 1024
                        pss = sum(map(int, _pss_re.findall(smaps_data))) * 1024
                        swap = sum(map(int, _swap_re.findall(smaps_data))) * 1024
                        return pfullmem(*basic_mem + (uss, pss, swap))

                else:
                    memory_full_info = memory_info
            if HAS_SMAPS:

                @wrap_exceptions
                def memory_maps(self):
                    """Return process's mapped memory regions as a list of named
            tuples. Fields are explained in 'man proc'; here is an updated
            (Apr 2012) version: http://goo.gl/fmebo

            /proc/{PID}/smaps does not exist on kernels < 2.6.14 or if
            CONFIG_MMU kernel configuration option is not enabled.
            """

                    def get_blocks--- This code section failed: ---

 L.1862         0  BUILD_MAP_0           0 
                2  STORE_FAST               'data'

 L.1863         4  LOAD_FAST                'lines'
                6  GET_ITER         
                8  FOR_ITER            148  'to 148'
               10  STORE_FAST               'line'

 L.1864        12  LOAD_FAST                'line'
               14  LOAD_METHOD              split
               16  LOAD_CONST               None
               18  LOAD_CONST               5
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'fields'

 L.1865        24  LOAD_FAST                'fields'
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  LOAD_METHOD              endswith
               32  LOAD_CONST               b':'
               34  CALL_METHOD_1         1  ''
               36  POP_JUMP_IF_TRUE     64  'to 64'

 L.1867        38  LOAD_FAST                'current_block'
               40  LOAD_METHOD              pop
               42  CALL_METHOD_0         0  ''
               44  LOAD_FAST                'data'
               46  BUILD_TUPLE_2         2 
               48  YIELD_VALUE      
               50  POP_TOP          

 L.1868        52  LOAD_FAST                'current_block'
               54  LOAD_METHOD              append
               56  LOAD_FAST                'line'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  JUMP_BACK             8  'to 8'
             64_0  COME_FROM            36  '36'

 L.1870        64  SETUP_FINALLY        94  'to 94'

 L.1871        66  LOAD_GLOBAL              int
               68  LOAD_FAST                'fields'
               70  LOAD_CONST               1
               72  BINARY_SUBSCR    
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_CONST               1024
               78  BINARY_MULTIPLY  
               80  LOAD_FAST                'data'
               82  LOAD_FAST                'fields'
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  STORE_SUBSCR     
               90  POP_BLOCK        
               92  JUMP_BACK             8  'to 8'
             94_0  COME_FROM_FINALLY    64  '64'

 L.1872        94  DUP_TOP          
               96  LOAD_GLOBAL              ValueError
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   144  'to 144'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L.1873       108  LOAD_FAST                'fields'
              110  LOAD_CONST               0
              112  BINARY_SUBSCR    
              114  LOAD_METHOD              startswith
              116  LOAD_CONST               b'VmFlags:'
              118  CALL_METHOD_1         1  ''
              120  POP_JUMP_IF_FALSE   128  'to 128'

 L.1875       122  POP_EXCEPT       
              124  JUMP_BACK             8  'to 8'
              126  JUMP_FORWARD        140  'to 140'
            128_0  COME_FROM           120  '120'

 L.1877       128  LOAD_GLOBAL              ValueError
              130  LOAD_STR                 "don't know how to interpret line %r"

 L.1878       132  LOAD_FAST                'line'

 L.1877       134  BINARY_MODULO    
              136  CALL_FUNCTION_1       1  ''
              138  RAISE_VARARGS_1       1  'exception instance'
            140_0  COME_FROM           126  '126'
              140  POP_EXCEPT       
              142  JUMP_BACK             8  'to 8'
            144_0  COME_FROM           100  '100'
              144  END_FINALLY      
              146  JUMP_BACK             8  'to 8'

 L.1879       148  LOAD_FAST                'current_block'
              150  LOAD_METHOD              pop
              152  CALL_METHOD_0         0  ''
              154  LOAD_FAST                'data'
              156  BUILD_TUPLE_2         2 
              158  YIELD_VALUE      
              160  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 124

                    data = self._read_smaps_file()
                    if not data:
                        return []
                    lines = data.split(b'\n')
                    ls = []
                    first_line = lines.pop(0)
                    current_block = [first_line]
                    for header, data in get_blocks(lines, current_block):
                        hfields = header.split(None, 5)
                        try:
                            addr, perms, offset, dev, inode, path = hfields
                        except ValueError:
                            addr, perms, offset, dev, inode, path = hfields + ['']
                        else:
                            if not path:
                                path = '[anon]'
                            else:
                                if PY3:
                                    path = decode(path)
                                path = path.strip()
                                if path.endswith(' (deleted)'):
                                    path = path_exists_strict(path) or path[:-10]
                            ls.append((
                             decode(addr), decode(perms), path,
                             data.get(b'Rss:', 0),
                             data.get(b'Size:', 0),
                             data.get(b'Pss:', 0),
                             data.get(b'Shared_Clean:', 0),
                             data.get(b'Shared_Dirty:', 0),
                             data.get(b'Private_Clean:', 0),
                             data.get(b'Private_Dirty:', 0),
                             data.get(b'Referenced:', 0),
                             data.get(b'Anonymous:', 0),
                             data.get(b'Swap:', 0)))
                    else:
                        return ls

            @wrap_exceptions
            def cwd--- This code section failed: ---

 L.1922         0  SETUP_FINALLY        24  'to 24'

 L.1923         2  LOAD_GLOBAL              readlink
                4  LOAD_STR                 '%s/%s/cwd'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _procfs_path
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                pid
               14  BUILD_TUPLE_2         2 
               16  BINARY_MODULO    
               18  CALL_FUNCTION_1       1  ''
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.1924        24  DUP_TOP          
               26  LOAD_GLOBAL              FileNotFoundError
               28  LOAD_GLOBAL              ProcessLookupError
               30  BUILD_TUPLE_2         2 
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    90  'to 90'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.1926        42  LOAD_GLOBAL              pid_exists
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                pid
               48  CALL_FUNCTION_1       1  ''
               50  POP_JUMP_IF_TRUE     68  'to 68'

 L.1927        52  LOAD_GLOBAL              NoSuchProcess
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                pid
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _name
               62  CALL_FUNCTION_2       2  ''
               64  RAISE_VARARGS_1       1  'exception instance'
               66  JUMP_FORWARD         86  'to 86'
             68_0  COME_FROM            50  '50'

 L.1929        68  LOAD_GLOBAL              ZombieProcess
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                pid
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _name
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _ppid
               82  CALL_FUNCTION_3       3  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            66  '66'
               86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
             90_0  COME_FROM            34  '34'
               90  END_FINALLY      
             92_0  COME_FROM            88  '88'

Parse error at or near `POP_TOP' instruction at offset 38

            @wrap_exceptions
            def num_ctx_switches(self, _ctxsw_re=re.compile(b'ctxt_switches:\\t(\\d+)')):
                data = self._read_status_file()
                ctxsw = _ctxsw_re.findall(data)
                if not ctxsw:
                    raise NotImplementedError("'voluntary_ctxt_switches' and 'nonvoluntary_ctxt_switches'lines were not found in %s/%s/status; the kernel is probably older than 2.6.23" % (
                     self._procfs_path, self.pid))
                else:
                    return _common.pctxsw(int(ctxsw[0]), int(ctxsw[1]))

            @wrap_exceptions
            def num_threads(self, _num_threads_re=re.compile(b'Threads:\\t(\\d+)')):
                data = self._read_status_file()
                return int(_num_threads_re.findall(data)[0])

            @wrap_exceptions
            def threads--- This code section failed: ---

 L.1955         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              listdir
                4  LOAD_STR                 '%s/%s/task'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _procfs_path
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                pid
               14  BUILD_TUPLE_2         2 
               16  BINARY_MODULO    
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'thread_ids'

 L.1956        22  LOAD_FAST                'thread_ids'
               24  LOAD_METHOD              sort
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          

 L.1957        30  BUILD_LIST_0          0 
               32  STORE_FAST               'retlist'

 L.1958        34  LOAD_CONST               False
               36  STORE_FAST               'hit_enoent'

 L.1959        38  LOAD_FAST                'thread_ids'
               40  GET_ITER         
               42  FOR_ITER            224  'to 224'
               44  STORE_FAST               'thread_id'

 L.1960        46  LOAD_STR                 '%s/%s/task/%s/stat'

 L.1961        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _procfs_path

 L.1961        52  LOAD_FAST                'self'
               54  LOAD_ATTR                pid

 L.1961        56  LOAD_FAST                'thread_id'

 L.1960        58  BUILD_TUPLE_3         3 
               60  BINARY_MODULO    
               62  STORE_FAST               'fname'

 L.1962        64  SETUP_FINALLY       102  'to 102'

 L.1963        66  LOAD_GLOBAL              open_binary
               68  LOAD_FAST                'fname'
               70  CALL_FUNCTION_1       1  ''
               72  SETUP_WITH           92  'to 92'
               74  STORE_FAST               'f'

 L.1964        76  LOAD_FAST                'f'
               78  LOAD_METHOD              read
               80  CALL_METHOD_0         0  ''
               82  LOAD_METHOD              strip
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'st'
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_WITH       72  '72'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      
               98  POP_BLOCK        
              100  JUMP_FORWARD        130  'to 130'
            102_0  COME_FROM_FINALLY    64  '64'

 L.1965       102  DUP_TOP          
              104  LOAD_GLOBAL              FileNotFoundError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   128  'to 128'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L.1968       116  LOAD_CONST               True
              118  STORE_FAST               'hit_enoent'

 L.1969       120  POP_EXCEPT       
              122  JUMP_BACK            42  'to 42'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           108  '108'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           100  '100'

 L.1971       130  LOAD_FAST                'st'
              132  LOAD_FAST                'st'
              134  LOAD_METHOD              find
              136  LOAD_CONST               b')'
              138  CALL_METHOD_1         1  ''
              140  LOAD_CONST               2
              142  BINARY_ADD       
              144  LOAD_CONST               None
              146  BUILD_SLICE_2         2 
              148  BINARY_SUBSCR    
              150  STORE_FAST               'st'

 L.1972       152  LOAD_FAST                'st'
              154  LOAD_METHOD              split
              156  LOAD_CONST               b' '
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               'values'

 L.1973       162  LOAD_GLOBAL              float
              164  LOAD_FAST                'values'
              166  LOAD_CONST               11
              168  BINARY_SUBSCR    
              170  CALL_FUNCTION_1       1  ''
              172  LOAD_GLOBAL              CLOCK_TICKS
              174  BINARY_TRUE_DIVIDE
              176  STORE_FAST               'utime'

 L.1974       178  LOAD_GLOBAL              float
              180  LOAD_FAST                'values'
              182  LOAD_CONST               12
              184  BINARY_SUBSCR    
              186  CALL_FUNCTION_1       1  ''
              188  LOAD_GLOBAL              CLOCK_TICKS
              190  BINARY_TRUE_DIVIDE
              192  STORE_FAST               'stime'

 L.1975       194  LOAD_GLOBAL              _common
              196  LOAD_METHOD              pthread
              198  LOAD_GLOBAL              int
              200  LOAD_FAST                'thread_id'
              202  CALL_FUNCTION_1       1  ''
              204  LOAD_FAST                'utime'
              206  LOAD_FAST                'stime'
              208  CALL_METHOD_3         3  ''
              210  STORE_FAST               'ntuple'

 L.1976       212  LOAD_FAST                'retlist'
              214  LOAD_METHOD              append
              216  LOAD_FAST                'ntuple'
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
              222  JUMP_BACK            42  'to 42'

 L.1977       224  LOAD_FAST                'hit_enoent'
              226  POP_JUMP_IF_FALSE   236  'to 236'

 L.1978       228  LOAD_FAST                'self'
              230  LOAD_METHOD              _assert_alive
              232  CALL_METHOD_0         0  ''
              234  POP_TOP          
            236_0  COME_FROM           226  '226'

 L.1979       236  LOAD_FAST                'retlist'
              238  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 124

            @wrap_exceptions
            def nice_get(self):
                return cext_posix.getpriority(self.pid)

            @wrap_exceptions
            def nice_set(self, value):
                return cext_posix.setpriority(self.pid, value)

            if HAS_CPU_AFFINITY:

                @wrap_exceptions
                def cpu_affinity_get(self):
                    return cext.proc_cpu_affinity_get(self.pid)

                def _get_eligible_cpus(self, _re=re.compile(b'Cpus_allowed_list:\\t(\\d+)-(\\d+)')):
                    data = self._read_status_file()
                    match = _re.findall(data)
                    if match:
                        return list(range(int(match[0][0]), int(match[0][1]) + 1))
                    return list(range(len(per_cpu_times())))

                @wrap_exceptions
                def cpu_affinity_set(self, cpus):
                    try:
                        cext.proc_cpu_affinity_set(self.pid, cpus)
                    except (OSError, ValueError) as err:
                        try:
                            if isinstance(err, ValueError) or err.errno == errno.EINVAL:
                                eligible_cpus = self._get_eligible_cpus()
                                all_cpus = tuple(range(len(per_cpu_times())))
                                for cpu in cpus:
                                    if cpu not in all_cpus:
                                        raise ValueError('invalid CPU number %r; choose between %s' % (
                                         cpu, eligible_cpus))
                                    if cpu not in eligible_cpus:
                                        raise ValueError('CPU number %r is not eligible; choose between %s' % (
                                         cpu, eligible_cpus))

                            raise
                        finally:
                            err = None
                            del err

            if HAS_PROC_IO_PRIORITY:

                @wrap_exceptions
                def ionice_get(self):
                    ioclass, value = cext.proc_ioprio_get(self.pid)
                    if enum is not None:
                        ioclass = IOPriority(ioclass)
                    return _common.pionice(ioclass, value)

                @wrap_exceptions
                def ionice_set(self, ioclass, value):
                    if value is None:
                        value = 0
                    if value:
                        if ioclass in (IOPRIO_CLASS_IDLE, IOPRIO_CLASS_NONE):
                            raise ValueError('%r ioclass accepts no value' % ioclass)
                    if value < 0 or value > 7:
                        raise ValueError('value not in 0-7 range')
                    return cext.proc_ioprio_set(self.pid, ioclass, value)

            if prlimit is not None:

                @wrap_exceptions
                def rlimit(self, resource_, limits=None):
                    if self.pid == 0:
                        raise ValueError("can't use prlimit() against PID 0 process")
                    try:
                        if limits is None:
                            return prlimit(self.pid, resource_)
                        if len(limits) != 2:
                            raise ValueError('second argument must be a (soft, hard) tuple, got %s' % repr(limits))
                        prlimit(self.pid, resource_, limits)
                    except OSError as err:
                        try:
                            if err.errno == errno.ENOSYS and pid_exists(self.pid):
                                raise ZombieProcess(self.pid, self._name, self._ppid)
                            else:
                                raise
                        finally:
                            err = None
                            del err

            @wrap_exceptions
            def status(self):
                letter = self._parse_stat_file()['status']
                if PY3:
                    letter = letter.decode()
                return PROC_STATUSES.get(letter, '?')

            @wrap_exceptions
            def open_files--- This code section failed: ---

 L.2088         0  BUILD_LIST_0          0 
                2  STORE_FAST               'retlist'

 L.2089         4  LOAD_GLOBAL              os
                6  LOAD_METHOD              listdir
                8  LOAD_STR                 '%s/%s/fd'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _procfs_path
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                pid
               18  BUILD_TUPLE_2         2 
               20  BINARY_MODULO    
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'files'

 L.2090        26  LOAD_CONST               False
               28  STORE_FAST               'hit_enoent'

 L.2091        30  LOAD_FAST                'files'
               32  GET_ITER         
             34_0  COME_FROM           174  '174'
             34_1  COME_FROM           166  '166'
            34_36  FOR_ITER            332  'to 332'
               38  STORE_FAST               'fd'

 L.2092        40  LOAD_STR                 '%s/%s/fd/%s'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _procfs_path
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                pid
               50  LOAD_FAST                'fd'
               52  BUILD_TUPLE_3         3 
               54  BINARY_MODULO    
               56  STORE_FAST               'file'

 L.2093        58  SETUP_FINALLY        72  'to 72'

 L.2094        60  LOAD_GLOBAL              readlink
               62  LOAD_FAST                'file'
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'path'
               68  POP_BLOCK        
               70  JUMP_FORWARD        158  'to 158'
             72_0  COME_FROM_FINALLY    58  '58'

 L.2095        72  DUP_TOP          
               74  LOAD_GLOBAL              FileNotFoundError
               76  LOAD_GLOBAL              ProcessLookupError
               78  BUILD_TUPLE_2         2 
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   102  'to 102'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L.2097        90  LOAD_CONST               True
               92  STORE_FAST               'hit_enoent'

 L.2098        94  POP_EXCEPT       
               96  JUMP_BACK            34  'to 34'
               98  POP_EXCEPT       
              100  JUMP_BACK            34  'to 34'
            102_0  COME_FROM            82  '82'

 L.2099       102  DUP_TOP          
              104  LOAD_GLOBAL              OSError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   156  'to 156'
              110  POP_TOP          
              112  STORE_FAST               'err'
              114  POP_TOP          
              116  SETUP_FINALLY       144  'to 144'

 L.2100       118  LOAD_FAST                'err'
              120  LOAD_ATTR                errno
              122  LOAD_GLOBAL              errno
              124  LOAD_ATTR                EINVAL
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   138  'to 138'

 L.2102       130  POP_BLOCK        
              132  POP_EXCEPT       
              134  CALL_FINALLY        144  'to 144'
              136  JUMP_BACK            34  'to 34'
            138_0  COME_FROM           128  '128'

 L.2103       138  RAISE_VARARGS_0       0  'reraise'
              140  POP_BLOCK        
              142  BEGIN_FINALLY    
            144_0  COME_FROM           134  '134'
            144_1  COME_FROM_FINALLY   116  '116'
              144  LOAD_CONST               None
              146  STORE_FAST               'err'
              148  DELETE_FAST              'err'
              150  END_FINALLY      
              152  POP_EXCEPT       
              154  JUMP_BACK            34  'to 34'
            156_0  COME_FROM           108  '108'
              156  END_FINALLY      
            158_0  COME_FROM            70  '70'

 L.2109       158  LOAD_FAST                'path'
              160  LOAD_METHOD              startswith
              162  LOAD_STR                 '/'
              164  CALL_METHOD_1         1  ''
              166  POP_JUMP_IF_FALSE    34  'to 34'
              168  LOAD_GLOBAL              isfile_strict
              170  LOAD_FAST                'path'
              172  CALL_FUNCTION_1       1  ''
              174  POP_JUMP_IF_FALSE    34  'to 34'

 L.2111       176  LOAD_STR                 '%s/%s/fdinfo/%s'

 L.2112       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _procfs_path

 L.2112       182  LOAD_FAST                'self'
              184  LOAD_ATTR                pid

 L.2112       186  LOAD_FAST                'fd'

 L.2111       188  BUILD_TUPLE_3         3 
              190  BINARY_MODULO    
              192  STORE_FAST               'file'

 L.2113       194  SETUP_FINALLY       262  'to 262'

 L.2114       196  LOAD_GLOBAL              open_binary
              198  LOAD_FAST                'file'
              200  CALL_FUNCTION_1       1  ''
              202  SETUP_WITH          252  'to 252'
              204  STORE_FAST               'f'

 L.2115       206  LOAD_GLOBAL              int
              208  LOAD_FAST                'f'
              210  LOAD_METHOD              readline
              212  CALL_METHOD_0         0  ''
              214  LOAD_METHOD              split
              216  CALL_METHOD_0         0  ''
              218  LOAD_CONST               1
              220  BINARY_SUBSCR    
              222  CALL_FUNCTION_1       1  ''
              224  STORE_FAST               'pos'

 L.2116       226  LOAD_GLOBAL              int
              228  LOAD_FAST                'f'
              230  LOAD_METHOD              readline
              232  CALL_METHOD_0         0  ''
              234  LOAD_METHOD              split
              236  CALL_METHOD_0         0  ''
              238  LOAD_CONST               1
              240  BINARY_SUBSCR    
              242  LOAD_CONST               8
              244  CALL_FUNCTION_2       2  ''
              246  STORE_FAST               'flags'
              248  POP_BLOCK        
              250  BEGIN_FINALLY    
            252_0  COME_FROM_WITH      202  '202'
              252  WITH_CLEANUP_START
              254  WITH_CLEANUP_FINISH
              256  END_FINALLY      
              258  POP_BLOCK        
              260  JUMP_FORWARD        288  'to 288'
            262_0  COME_FROM_FINALLY   194  '194'

 L.2117       262  DUP_TOP          
              264  LOAD_GLOBAL              FileNotFoundError
              266  COMPARE_OP               exception-match
          268_270  POP_JUMP_IF_FALSE   286  'to 286'
              272  POP_TOP          
              274  POP_TOP          
              276  POP_TOP          

 L.2120       278  LOAD_CONST               True
              280  STORE_FAST               'hit_enoent'
              282  POP_EXCEPT       
              284  JUMP_BACK            34  'to 34'
            286_0  COME_FROM           268  '268'
              286  END_FINALLY      
            288_0  COME_FROM           260  '260'

 L.2122       288  LOAD_GLOBAL              file_flags_to_mode
              290  LOAD_FAST                'flags'
              292  CALL_FUNCTION_1       1  ''
              294  STORE_FAST               'mode'

 L.2123       296  LOAD_GLOBAL              popenfile

 L.2124       298  LOAD_FAST                'path'

 L.2124       300  LOAD_GLOBAL              int
              302  LOAD_FAST                'fd'
              304  CALL_FUNCTION_1       1  ''

 L.2124       306  LOAD_GLOBAL              int
              308  LOAD_FAST                'pos'
              310  CALL_FUNCTION_1       1  ''

 L.2124       312  LOAD_FAST                'mode'

 L.2124       314  LOAD_FAST                'flags'

 L.2123       316  CALL_FUNCTION_5       5  ''
              318  STORE_FAST               'ntuple'

 L.2125       320  LOAD_FAST                'retlist'
              322  LOAD_METHOD              append
              324  LOAD_FAST                'ntuple'
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          
              330  JUMP_BACK            34  'to 34'

 L.2126       332  LOAD_FAST                'hit_enoent'
          334_336  POP_JUMP_IF_FALSE   346  'to 346'

 L.2127       338  LOAD_FAST                'self'
              340  LOAD_METHOD              _assert_alive
              342  CALL_METHOD_0         0  ''
              344  POP_TOP          
            346_0  COME_FROM           334  '334'

 L.2128       346  LOAD_FAST                'retlist'
              348  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 98

            @wrap_exceptions
            def connections(self, kind='inet'):
                ret = _connections.retrieve(kind, self.pid)
                self._assert_alive()
                return ret

            @wrap_exceptions
            def num_fds(self):
                return len(os.listdir('%s/%s/fd' % (self._procfs_path, self.pid)))

            @wrap_exceptions
            def ppid(self):
                return int(self._parse_stat_file()['ppid'])

            @wrap_exceptions
            def uids(self, _uids_re=re.compile(b'Uid:\\t(\\d+)\\t(\\d+)\\t(\\d+)')):
                data = self._read_status_file()
                real, effective, saved = _uids_re.findall(data)[0]
                return _common.puids(int(real), int(effective), int(saved))

            @wrap_exceptions
            def gids(self, _gids_re=re.compile(b'Gid:\\t(\\d+)\\t(\\d+)\\t(\\d+)')):
                data = self._read_status_file()
                real, effective, saved = _gids_re.findall(data)[0]
                return _common.pgids(int(real), int(effective), int(saved))