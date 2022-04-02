# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\psutil-5.4.4-py2.7-win32.egg\psutil\_pslinux.py
"""Linux platform implementation."""
from __future__ import division
import base64, collections, errno, functools, glob, os, re, socket, struct, sys, traceback, warnings
from collections import defaultdict
from collections import namedtuple
from . import _common
from . import _psposix
from . import _psutil_linux as cext
from . import _psutil_posix as cext_posix
from ._common import ENCODING
from ._common import ENCODING_ERRS
from ._common import isfile_strict
from ._common import memoize
from ._common import memoize_when_activated
from ._common import NIC_DUPLEX_FULL
from ._common import NIC_DUPLEX_HALF
from ._common import NIC_DUPLEX_UNKNOWN
from ._common import parse_environ_block
from ._common import path_exists_strict
from ._common import supports_ipv6
from ._common import usage_percent
from ._compat import b
from ._compat import basestring
from ._compat import long
from ._compat import PY3
from ._exceptions import AccessDenied
from ._exceptions import NoSuchProcess
from ._exceptions import ZombieProcess
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
HAS_PRLIMIT = hasattr(cext, 'linux_prlimit')
_DEFAULT = object()
if HAS_PRLIMIT:
    for name in dir(cext):
        if name.startswith('RLIM'):
            __extra__all__.append(name)

CLOCK_TICKS = os.sysconf('SC_CLK_TCK')
PAGESIZE = os.sysconf('SC_PAGE_SIZE')
BOOT_TIME = None
BIGFILE_BUFFERING = -1 if PY3 else 8192
LITTLE_ENDIAN = sys.byteorder == 'little'
SECTOR_SIZE_FALLBACK = 512
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
PROC_STATUSES = {'R': _common.STATUS_RUNNING, 
   'S': _common.STATUS_SLEEPING, 
   'D': _common.STATUS_DISK_SLEEP, 
   'T': _common.STATUS_STOPPED, 
   't': _common.STATUS_TRACING_STOP, 
   'Z': _common.STATUS_ZOMBIE, 
   'X': _common.STATUS_DEAD, 
   'x': _common.STATUS_DEAD, 
   'K': _common.STATUS_WAKE_KILL, 
   'W': _common.STATUS_WAKING}
TCP_STATUSES = {'01': _common.CONN_ESTABLISHED, 
   '02': _common.CONN_SYN_SENT, 
   '03': _common.CONN_SYN_RECV, 
   '04': _common.CONN_FIN_WAIT1, 
   '05': _common.CONN_FIN_WAIT2, 
   '06': _common.CONN_TIME_WAIT, 
   '07': _common.CONN_CLOSE, 
   '08': _common.CONN_CLOSE_WAIT, 
   '09': _common.CONN_LAST_ACK, 
   '0A': _common.CONN_LISTEN, 
   '0B': _common.CONN_CLOSING}
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
pmmap_ext = namedtuple('pmmap_ext', 'addr perms ' + (' ').join(pmmap_grouped._fields))
pio = namedtuple('pio', ['read_count', 'write_count',
 'read_bytes', 'write_bytes',
 'read_chars', 'write_chars'])

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


if PY3:

    def decode(s):
        return s.decode(encoding=ENCODING, errors=ENCODING_ERRS)


else:

    def decode(s):
        return s


def get_procfs_path():
    """Return updated psutil.PROCFS_PATH constant."""
    return sys.modules['psutil'].PROCFS_PATH


def readlink--- This code section failed: ---

 L. 219         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'path'
                6  LOAD_GLOBAL           1  'basestring'
                9  CALL_FUNCTION_2       2  None
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_FAST             0  'path'
               21  RAISE_VARARGS_2       2  None

 L. 220        24  LOAD_GLOBAL           3  'os'
               27  LOAD_ATTR             4  'readlink'
               30  LOAD_FAST             0  'path'
               33  CALL_FUNCTION_1       1  None
               36  STORE_FAST            0  'path'

 L. 228        39  LOAD_FAST             0  'path'
               42  LOAD_ATTR             5  'split'
               45  LOAD_CONST               '\x00'
               48  CALL_FUNCTION_1       1  None
               51  LOAD_CONST               0
               54  BINARY_SUBSCR    
               55  STORE_FAST            0  'path'

 L. 232        58  LOAD_FAST             0  'path'
               61  LOAD_ATTR             6  'endswith'
               64  LOAD_CONST               ' (deleted)'
               67  CALL_FUNCTION_1       1  None
               70  POP_JUMP_IF_FALSE    99  'to 99'
               73  LOAD_GLOBAL           7  'path_exists_strict'
               76  LOAD_FAST             0  'path'
               79  CALL_FUNCTION_1       1  None
               82  UNARY_NOT        
             83_0  COME_FROM            70  '70'
               83  POP_JUMP_IF_FALSE    99  'to 99'

 L. 233        86  LOAD_FAST             0  'path'
               89  LOAD_CONST               -10
               92  SLICE+2          
               93  STORE_FAST            0  'path'
               96  JUMP_FORWARD          0  'to 99'
             99_0  COME_FROM            96  '96'

 L. 234        99  LOAD_FAST             0  'path'
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 102


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


def get_sector_size(partition):
    """Return the sector size of a partition.
    Used by disk_io_counters().
    """
    try:
        with open('/sys/block/%s/queue/hw_sector_size' % partition, 'rt') as (f):
            return int(f.read())
    except (IOError, ValueError):
        return SECTOR_SIZE_FALLBACK


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


def cat(fname, fallback=_DEFAULT, binary=True):
    """Return file content.
    fallback: the value returned in case the file does not exist or
              cannot be read
    binary: whether to open the file in binary or text mode.
    """
    try:
        with open_binary(fname) if binary else open_text(fname) as (f):
            return f.read().strip()
    except IOError:
        if fallback is not _DEFAULT:
            return fallback
        raise


try:
    set_scputimes_ntuple('/proc')
except Exception:
    traceback.print_exc()
    scputimes = namedtuple('scputimes', 'user system idle')(0.0, 0.0, 0.0)

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
    free = mems['MemFree:']
    fallback = free + mems.get('Cached:', 0)
    try:
        lru_active_file = mems['Active(file):']
        lru_inactive_file = mems['Inactive(file):']
        slab_reclaimable = mems['SReclaimable:']
    except KeyError:
        return fallback

    try:
        f = open_binary('%s/zoneinfo' % get_procfs_path())
    except IOError:
        return fallback

    watermark_low = 0
    with f:
        for line in f:
            line = line.strip()
            if line.startswith('low'):
                watermark_low += int(line.split()[1])

    watermark_low *= PAGESIZE
    watermark_low = watermark_low
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

    total = mems['MemTotal:']
    free = mems['MemFree:']
    try:
        buffers = mems['Buffers:']
    except KeyError:
        buffers = 0
        missing_fields.append('buffers')

    try:
        cached = mems['Cached:']
    except KeyError:
        cached = 0
        missing_fields.append('cached')
    else:
        cached += mems.get('SReclaimable:', 0)

    try:
        shared = mems['Shmem:']
    except KeyError:
        try:
            shared = mems['MemShared:']
        except KeyError:
            shared = 0
            missing_fields.append('shared')

    try:
        active = mems['Active:']
    except KeyError:
        active = 0
        missing_fields.append('active')

    try:
        inactive = mems['Inactive:']
    except KeyError:
        try:
            inactive = mems['Inact_dirty:'] + mems['Inact_clean:'] + mems['Inact_laundry:']
        except KeyError:
            inactive = 0
            missing_fields.append('inactive')

    try:
        slab = mems['Slab:']
    except KeyError:
        slab = 0

    used = total - free - cached - buffers
    if used < 0:
        used = total - free
    try:
        avail = mems['MemAvailable:']
    except KeyError:
        avail = calculate_avail_vmem(mems)

    if avail < 0:
        avail = 0
        missing_fields.append('available')
    if avail > total:
        avail = free
    percent = usage_percent(total - avail, total, _round=1)
    if missing_fields:
        msg = "%s memory stats couldn't be determined and %s set to 0" % (
         (', ').join(missing_fields),
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
        total = mems['SwapTotal:']
        free = mems['SwapFree:']
    except KeyError:
        _, _, _, _, total, free, unit_multiplier = cext.linux_sysinfo()
        total *= unit_multiplier
        free *= unit_multiplier

    used = total - free
    percent = usage_percent(used, total, _round=1)
    try:
        f = open_binary('%s/vmstat' % get_procfs_path())
    except IOError as err:
        msg = "'sin' and 'sout' swap memory stats couldn't be determined and were set to 0 (%s)" % str(err)
        warnings.warn(msg, RuntimeWarning)
        sin = sout = 0
    else:
        with f:
            sin = sout = None
            for line in f:
                if line.startswith('pswpin'):
                    sin = int(line.split(' ')[1]) * 4 * 1024
                elif line.startswith('pswpout'):
                    sout = int(line.split(' ')[1]) * 4 * 1024
                if sin is not None and sout is not None:
                    break
            else:
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
    fields = [ float(x) / CLOCK_TICKS for x in fields ]
    return scputimes(*fields)


def per_cpu_times():
    """Return a list of namedtuple representing the CPU times
    for every CPU available on the system.
    """
    procfs_path = get_procfs_path()
    set_scputimes_ntuple(procfs_path)
    cpus = []
    with open_binary('%s/stat' % procfs_path) as (f):
        f.readline()
        for line in f:
            if line.startswith('cpu'):
                values = line.split()
                fields = values[1:len(scputimes._fields) + 1]
                fields = [ float(x) / CLOCK_TICKS for x in fields ]
                entry = scputimes(*fields)
                cpus.append(entry)

        return cpus


def cpu_count_logical():
    """Return the number of logical CPUs in the system."""
    try:
        return os.sysconf('SC_NPROCESSORS_ONLN')
    except ValueError:
        num = 0
        with open_binary('%s/cpuinfo' % get_procfs_path()) as (f):
            for line in f:
                if line.lower().startswith('processor'):
                    num += 1

        if num == 0:
            search = re.compile('cpu\\d')
            with open_text('%s/stat' % get_procfs_path()) as (f):
                for line in f:
                    line = line.split(' ')[0]
                    if search.match(line):
                        num += 1

        if num == 0:
            return
        return num

    return


def cpu_count_physical():
    """Return the number of physical cores in the system."""
    mapping = {}
    current_info = {}
    with open_binary('%s/cpuinfo' % get_procfs_path()) as (f):
        for line in f:
            line = line.strip().lower()
            if not line:
                if 'physical id' in current_info and 'cpu cores' in current_info:
                    mapping[current_info['physical id']] = current_info['cpu cores']
                current_info = {}
            elif line.startswith('physical id') or line.startswith('cpu cores'):
                key, value = line.split('\t:', 1)
                current_info[key] = int(value)

    return sum(mapping.values()) or None


def cpu_stats():
    """Return various CPU stats as a named tuple."""
    with open_binary('%s/stat' % get_procfs_path()) as (f):
        ctx_switches = None
        interrupts = None
        soft_interrupts = None
        for line in f:
            if line.startswith('ctxt'):
                ctx_switches = int(line.split()[1])
            elif line.startswith('intr'):
                interrupts = int(line.split()[1])
            elif line.startswith('softirq'):
                soft_interrupts = int(line.split()[1])
            if ctx_switches is not None and soft_interrupts is not None and interrupts is not None:
                break

    syscalls = 0
    return _common.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


if os.path.exists('/sys/devices/system/cpu/cpufreq') or os.path.exists('/sys/devices/system/cpu/cpu0/cpufreq'):

    def cpu_freq():
        """Return frequency metrics for all CPUs.
        Contrarily to other OSes, Linux updates these values in
        real-time.
        """
        ret = []
        ls = glob.glob('/sys/devices/system/cpu/cpufreq/policy*')
        if ls:
            ls.sort(key=lambda x: int(os.path.basename(x)[6:]))
        else:
            ls = glob.glob('/sys/devices/system/cpu/cpu[0-9]*/cpufreq')
            ls.sort(key=lambda x: int(re.search('[0-9]+', x).group(0)))
        pjoin = os.path.join
        for path in ls:
            curr = cat(pjoin(path, 'scaling_cur_freq'), fallback=None)
            if curr is None:
                curr = cat(pjoin(path, 'cpuinfo_cur_freq'), fallback=None)
                if curr is None:
                    raise NotImplementedError("can't find current frequency file")
            curr = int(curr) / 1000
            max_ = int(cat(pjoin(path, 'scaling_max_freq'))) / 1000
            min_ = int(cat(pjoin(path, 'scaling_min_freq'))) / 1000
            ret.append(_common.scpufreq(curr, min_, max_))

        return ret


net_if_addrs = cext_posix.net_if_addrs

class _Ipv6UnsupportedError(Exception):
    pass


class Connections:
    """A wrapper on top of /proc/net/* files, retrieving per-process
    and system-wide open connections (TCP, UDP, UNIX) similarly to
    "netstat -an".

    Note: in case of UNIX sockets we're only able to determine the
    local endpoint/path, not the one it's connected to.
    According to [1] it would be possible but not easily.

    [1] http://serverfault.com/a/417946
    """

    def __init__(self):
        tcp4 = (
         'tcp', socket.AF_INET, socket.SOCK_STREAM)
        tcp6 = ('tcp6', socket.AF_INET6, socket.SOCK_STREAM)
        udp4 = ('udp', socket.AF_INET, socket.SOCK_DGRAM)
        udp6 = ('udp6', socket.AF_INET6, socket.SOCK_DGRAM)
        unix = ('unix', socket.AF_UNIX, None)
        self.tmap = {'all': (
                 tcp4, tcp6, udp4, udp6, unix), 
           'tcp': (
                 tcp4, tcp6), 
           'tcp4': (
                  tcp4,), 
           'tcp6': (
                  tcp6,), 
           'udp': (
                 udp4, udp6), 
           'udp4': (
                  udp4,), 
           'udp6': (
                  udp6,), 
           'unix': (
                  unix,), 
           'inet': (
                  tcp4, tcp6, udp4, udp6), 
           'inet4': (
                   tcp4, udp4), 
           'inet6': (
                   tcp6, udp6)}
        self._procfs_path = None
        return

    def get_proc_inodes(self, pid):
        inodes = defaultdict(list)
        for fd in os.listdir('%s/%s/fd' % (self._procfs_path, pid)):
            try:
                inode = readlink('%s/%s/fd/%s' % (self._procfs_path, pid, fd))
            except OSError as err:
                if err.errno in (errno.ENOENT, errno.ESRCH):
                    continue
                elif err.errno == errno.EINVAL:
                    continue
                else:
                    raise
            else:
                if inode.startswith('socket:['):
                    inode = inode[8:][:-1]
                    inodes[inode].append((pid, int(fd)))

        return inodes

    def get_all_inodes(self):
        inodes = {}
        for pid in pids():
            try:
                inodes.update(self.get_proc_inodes(pid))
            except OSError as err:
                if err.errno not in (
                 errno.ENOENT, errno.ESRCH, errno.EPERM, errno.EACCES):
                    raise

        return inodes

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
                    ip = socket.inet_ntop(socket.AF_INET6, struct.pack('>4I', *struct.unpack('<4I', ip)))
                else:
                    ip = socket.inet_ntop(socket.AF_INET6, struct.pack('<4I', *struct.unpack('<4I', ip)))
            except ValueError:
                if not supports_ipv6():
                    raise _Ipv6UnsupportedError
                else:
                    raise

        return _common.addr(ip, port)

    @staticmethod
    def process_inet(file, family, type_, inodes, filter_pid=None):
        """Parse /proc/net/tcp* and /proc/net/udp* files."""
        if file.endswith('6') and not os.path.exists(file):
            return
        else:
            with open_text(file, buffering=BIGFILE_BUFFERING) as (f):
                f.readline()
                for lineno, line in enumerate(f, 1):
                    try:
                        _, laddr, raddr, status, _, _, _, _, _, inode = line.split()[:10]
                    except ValueError:
                        raise RuntimeError('error while parsing %s; malformed line %s %r' % (
                         file, lineno, line))

                    if inode in inodes:
                        pid, fd = inodes[inode][0]
                    else:
                        pid, fd = (None, -1)
                    if filter_pid is not None and filter_pid != pid:
                        continue
                    else:
                        if type_ == socket.SOCK_STREAM:
                            status = TCP_STATUSES[status]
                        else:
                            status = _common.CONN_NONE
                        try:
                            laddr = Connections.decode_address(laddr, family)
                            raddr = Connections.decode_address(raddr, family)
                        except _Ipv6UnsupportedError:
                            continue

                        yield (
                         fd, family, type_, laddr, raddr, status, pid)

            return

    @staticmethod
    def process_unix(file, family, inodes, filter_pid=None):
        """Parse /proc/net/unix files."""
        with open_text(file, buffering=BIGFILE_BUFFERING) as (f):
            f.readline()
            for line in f:
                tokens = line.split()
                try:
                    _, _, _, _, type_, _, inode = tokens[0:7]
                except ValueError:
                    if ' ' not in line:
                        continue
                    raise RuntimeError('error while parsing %s; malformed line %r' % (
                     file, line))

                if inode in inodes:
                    pairs = inodes[inode]
                else:
                    pairs = [
                     (None, -1)]
                for pid, fd in pairs:
                    if filter_pid is not None and filter_pid != pid:
                        continue
                    else:
                        if len(tokens) == 8:
                            path = tokens[(-1)]
                        else:
                            path = ''
                        type_ = int(type_)
                        raddr = ''
                        status = _common.CONN_NONE
                        yield (fd, family, type_, path, raddr, status, pid)

        return

    def retrieve(self, kind, pid=None):
        if kind not in self.tmap:
            raise ValueError('invalid %r kind argument; choose between %s' % (
             kind, (', ').join([ repr(x) for x in self.tmap ])))
        self._procfs_path = get_procfs_path()
        if pid is not None:
            inodes = self.get_proc_inodes(pid)
            if not inodes:
                return []
        else:
            inodes = self.get_all_inodes()
        ret = set()
        for f, family, type_ in self.tmap[kind]:
            if family in (socket.AF_INET, socket.AF_INET6):
                ls = self.process_inet('%s/net/%s' % (self._procfs_path, f), family, type_, inodes, filter_pid=pid)
            else:
                ls = self.process_unix('%s/net/%s' % (self._procfs_path, f), family, inodes, filter_pid=pid)
            for fd, family, type_, laddr, raddr, status, bound_pid in ls:
                if pid:
                    conn = _common.pconn(fd, family, type_, laddr, raddr, status)
                else:
                    conn = _common.sconn(fd, family, type_, laddr, raddr, status, bound_pid)
                ret.add(conn)

        return list(ret)


_connections = Connections()

def net_connections(kind='inet'):
    """Return system-wide open connections."""
    return _connections.retrieve(kind)


def net_io_counters--- This code section failed: ---

 L. 964         0  LOAD_GLOBAL           0  'open_text'
                3  LOAD_CONST               '%s/net/dev'
                6  LOAD_GLOBAL           1  'get_procfs_path'
                9  CALL_FUNCTION_0       0  None
               12  BINARY_MODULO    
               13  CALL_FUNCTION_1       1  None
               16  SETUP_WITH           19  'to 38'
               19  STORE_FAST            0  'f'

 L. 965        22  LOAD_FAST             0  'f'
               25  LOAD_ATTR             2  'readlines'
               28  CALL_FUNCTION_0       0  None
               31  STORE_FAST            1  'lines'
               34  POP_BLOCK        
               35  LOAD_CONST               None
             38_0  COME_FROM_WITH       16  '16'
               38  WITH_CLEANUP     
               39  END_FINALLY      

 L. 966        40  BUILD_MAP_0           0  None
               43  STORE_FAST            2  'retdict'

 L. 967        46  SETUP_LOOP          199  'to 248'
               49  LOAD_FAST             1  'lines'
               52  LOAD_CONST               2
               55  SLICE+1          
               56  GET_ITER         
               57  FOR_ITER            187  'to 247'
               60  STORE_FAST            3  'line'

 L. 968        63  LOAD_FAST             3  'line'
               66  LOAD_ATTR             3  'rfind'
               69  LOAD_CONST               ':'
               72  CALL_FUNCTION_1       1  None
               75  STORE_FAST            4  'colon'

 L. 969        78  LOAD_FAST             4  'colon'
               81  LOAD_CONST               0
               84  COMPARE_OP            4  >
               87  POP_JUMP_IF_TRUE    105  'to 105'
               90  LOAD_ASSERT              AssertionError
               93  LOAD_GLOBAL           5  'repr'
               96  LOAD_FAST             3  'line'
               99  CALL_FUNCTION_1       1  None
              102  RAISE_VARARGS_2       2  None

 L. 970       105  LOAD_FAST             3  'line'
              108  LOAD_FAST             4  'colon'
              111  SLICE+2          
              112  LOAD_ATTR             6  'strip'
              115  CALL_FUNCTION_0       0  None
              118  STORE_FAST            5  'name'

 L. 971       121  LOAD_FAST             3  'line'
              124  LOAD_FAST             4  'colon'
              127  LOAD_CONST               1
              130  BINARY_ADD       
              131  SLICE+1          
              132  LOAD_ATTR             6  'strip'
              135  CALL_FUNCTION_0       0  None
              138  LOAD_ATTR             7  'split'
              141  CALL_FUNCTION_0       0  None
              144  STORE_FAST            6  'fields'

 L. 990       147  LOAD_GLOBAL           8  'map'
              150  LOAD_GLOBAL           9  'int'
              153  LOAD_FAST             6  'fields'
              156  CALL_FUNCTION_2       2  None
              159  UNPACK_SEQUENCE_16    16 
              162  STORE_FAST            7  'bytes_recv'
              165  STORE_FAST            8  'packets_recv'
              168  STORE_FAST            9  'errin'
              171  STORE_FAST           10  'dropin'
              174  STORE_FAST           11  'fifoin'
              177  STORE_FAST           12  'framein'
              180  STORE_FAST           13  'compressedin'
              183  STORE_FAST           14  'multicastin'
              186  STORE_FAST           15  'bytes_sent'
              189  STORE_FAST           16  'packets_sent'
              192  STORE_FAST           17  'errout'
              195  STORE_FAST           18  'dropout'
              198  STORE_FAST           19  'fifoout'
              201  STORE_FAST           20  'collisionsout'
              204  STORE_FAST           21  'carrierout'
              207  STORE_FAST           22  'compressedout'

 L. 992       210  LOAD_FAST            15  'bytes_sent'
              213  LOAD_FAST             7  'bytes_recv'
              216  LOAD_FAST            16  'packets_sent'
              219  LOAD_FAST             8  'packets_recv'

 L. 993       222  LOAD_FAST             9  'errin'
              225  LOAD_FAST            17  'errout'
              228  LOAD_FAST            10  'dropin'
              231  LOAD_FAST            18  'dropout'
              234  BUILD_TUPLE_8         8 
              237  LOAD_FAST             2  'retdict'
              240  LOAD_FAST             5  'name'
              243  STORE_SUBSCR     
              244  JUMP_BACK            57  'to 57'
              247  POP_BLOCK        
            248_0  COME_FROM            46  '46'

 L. 994       248  LOAD_FAST             2  'retdict'
              251  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 247


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    duplex_map = {cext.DUPLEX_FULL: NIC_DUPLEX_FULL, cext.DUPLEX_HALF: NIC_DUPLEX_HALF, 
       cext.DUPLEX_UNKNOWN: NIC_DUPLEX_UNKNOWN}
    names = net_io_counters().keys()
    ret = {}
    for name in names:
        mtu = cext_posix.net_if_mtu(name)
        isup = cext_posix.net_if_flags(name)
        duplex, speed = cext.net_if_duplex_speed(name)
        ret[name] = _common.snicstats(isup, duplex_map[duplex], speed, mtu)

    return ret


disk_usage = _psposix.disk_usage

def disk_io_counters():
    """Return disk I/O statistics for every disk installed on the
    system as a dict of raw tuples.
    """

    def get_partitions():
        partitions = []
        with open_text('%s/partitions' % get_procfs_path()) as (f):
            lines = f.readlines()[2:]
        for line in reversed(lines):
            _, _, _, name = line.split()
            if name[(-1)].isdigit():
                partitions.append(name)
            elif not partitions or not partitions[(-1)].startswith(name):
                partitions.append(name)

        return partitions

    retdict = {}
    partitions = get_partitions()
    with open_text('%s/diskstats' % get_procfs_path()) as (f):
        lines = f.readlines()
    for line in lines:
        fields = line.split()
        fields_len = len(fields)
        if fields_len == 15:
            name = fields[3]
            reads = int(fields[2])
            reads_merged, rbytes, rtime, writes, writes_merged, wbytes, wtime, _, busy_time, _ = map(int, fields[4:14])
        elif fields_len == 14:
            name = fields[2]
            reads, reads_merged, rbytes, rtime, writes, writes_merged, wbytes, wtime, _, busy_time, _ = map(int, fields[3:14])
        elif fields_len == 7:
            name = fields[2]
            reads, rbytes, writes, wbytes = map(int, fields[3:])
            rtime = wtime = reads_merged = writes_merged = busy_time = 0
        else:
            raise ValueError('not sure how to interpret line %r' % line)
        if name in partitions:
            ssize = get_sector_size(name)
            rbytes *= ssize
            wbytes *= ssize
            retdict[name] = (reads, writes, rbytes, wbytes, rtime, wtime,
             reads_merged, writes_merged, busy_time)

    return retdict


def disk_partitions(all=False):
    """Return mounted disk partitions as a list of namedtuples."""
    fstypes = set()
    with open_text('%s/filesystems' % get_procfs_path()) as (f):
        for line in f:
            line = line.strip()
            if not line.startswith('nodev'):
                fstypes.add(line.strip())
            else:
                fstype = line.split('\t')[1]
                if fstype == 'zfs':
                    fstypes.add('zfs')

    retlist = []
    partitions = cext.disk_partitions()
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        if device == 'none':
            device = ''
        if not all:
            if device == '' or fstype not in fstypes:
                continue
        ntuple = _common.sdiskpart(device, mountpoint, fstype, opts)
        retlist.append(ntuple)

    return retlist


def sensors_temperatures():
    """Return hardware (CPU and others) temperatures as a dict
    including hardware name, label, current, max and critical
    temperatures.

    Implementation notes:
    - /sys/class/hwmon looks like the most recent interface to
      retrieve this info, and this implementation relies on it
      only (old distros will probably use something else)
    - lm-sensors on Ubuntu 16.04 relies on /sys/class/hwmon
    - /sys/class/thermal/thermal_zone* is another one but it's more
      difficult to parse
    """
    ret = collections.defaultdict(list)
    basenames = glob.glob('/sys/class/hwmon/hwmon*/temp*_*')
    basenames.extend(glob.glob('/sys/class/hwmon/hwmon*/device/temp*_*'))
    basenames = sorted(set([ x.split('_')[0] for x in basenames ]))
    for base in basenames:
        try:
            path = base + '_input'
            current = float(cat(path)) / 1000.0
            path = os.path.join(os.path.dirname(base), 'name')
            unit_name = cat(path, binary=False)
        except (IOError, OSError) as err:
            warnings.warn('ignoring %r for file %r' % (err, path), RuntimeWarning)
            continue

        high = cat(base + '_max', fallback=None)
        critical = cat(base + '_crit', fallback=None)
        label = cat(base + '_label', fallback='', binary=False)
        if high is not None:
            high = float(high) / 1000.0
        if critical is not None:
            critical = float(critical) / 1000.0
        ret[unit_name].append((label, current, high, critical))

    return ret


def sensors_fans():
    """Return hardware fans info (for CPU and other peripherals) as a
    dict including hardware label and current speed.

    Implementation notes:
    - /sys/class/hwmon looks like the most recent interface to
      retrieve this info, and this implementation relies on it
      only (old distros will probably use something else)
    - lm-sensors on Ubuntu 16.04 relies on /sys/class/hwmon
    """
    ret = collections.defaultdict(list)
    basenames = glob.glob('/sys/class/hwmon/hwmon*/fan*_*')
    if not basenames:
        basenames = glob.glob('/sys/class/hwmon/hwmon*/device/fan*_*')
    basenames = sorted(set([ x.split('_')[0] for x in basenames ]))
    for base in basenames:
        try:
            current = int(cat(base + '_input'))
        except (IOError, OSError) as err:
            warnings.warn('ignoring %r' % err, RuntimeWarning)
            continue

        unit_name = cat(os.path.join(os.path.dirname(base), 'name'), binary=False)
        label = cat(base + '_label', fallback='', binary=False)
        ret[unit_name].append(_common.sfan(label, current))

    return dict(ret)


def sensors_battery():
    """Return battery information.
    Implementation note: it appears /sys/class/power_supply/BAT0/
    directory structure may vary and provide files with the same
    meaning but under different names, see:
    https://github.com/giampaolo/psutil/issues/966
    """
    null = object()

    def multi_cat(*paths):
        """Attempt to read the content of multiple files which may
        not exist. If none of them exist return None.
        """
        for path in paths:
            ret = cat(path, fallback=null)
            if ret != null:
                if ret.isdigit():
                    return int(ret)
                return ret

        return

    root = os.path.join(POWER_SUPPLY_PATH, 'BAT0')
    if not os.path.exists(root):
        return
    else:
        energy_now = multi_cat(root + '/energy_now', root + '/charge_now')
        power_now = multi_cat(root + '/power_now', root + '/current_now')
        energy_full = multi_cat(root + '/energy_full', root + '/charge_full')
        if energy_now is None or power_now is None:
            return
        if energy_full is not None:
            try:
                percent = 100.0 * energy_now / energy_full
            except ZeroDivisionError:
                percent = 0.0

        else:
            percent = int(cat(root + '/capacity', fallback=-1))
            if percent == -1:
                return
        power_plugged = None
        online = multi_cat(os.path.join(POWER_SUPPLY_PATH, 'AC0/online'), os.path.join(POWER_SUPPLY_PATH, 'AC/online'))
        if online is not None:
            power_plugged = online == 1
        else:
            status = cat(root + '/status', fallback='', binary=False).lower()
            if status == 'discharging':
                power_plugged = False
            elif status in ('charging', 'full'):
                power_plugged = True
            if power_plugged:
                secsleft = _common.POWER_TIME_UNLIMITED
            else:
                try:
                    secsleft = int(energy_now / power_now * 3600)
                except ZeroDivisionError:
                    secsleft = _common.POWER_TIME_UNKNOWN

        return _common.sbattery(percent, secsleft, power_plugged)


def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    for item in rawlist:
        user, tty, hostname, tstamp, user_process, pid = item
        if not user_process:
            continue
        if hostname in (':0.0', ':0'):
            hostname = 'localhost'
        nt = _common.suser(user, tty or None, hostname, tstamp, pid)
        retlist.append(nt)

    return retlist


def boot_time():
    """Return the system boot time expressed in seconds since the epoch."""
    global BOOT_TIME
    path = '%s/stat' % get_procfs_path()
    with open_binary(path) as (f):
        for line in f:
            if line.startswith('btime'):
                ret = float(line.strip().split()[1])
                BOOT_TIME = ret
                return ret

        raise RuntimeError("line 'btime' not found in %s" % path)


def pids():
    """Returns a list of PIDs currently running on the system."""
    return [ int(x) for x in os.listdir(b(get_procfs_path())) if x.isdigit() ]


def pid_exists(pid):
    """Check for the existence of a unix PID. Linux TIDs are not
    supported (always return False).
    """
    if not _psposix.pid_exists(pid):
        return False
    try:
        path = '%s/%s/status' % (get_procfs_path(), pid)
        with open_binary(path) as (f):
            for line in f:
                if line.startswith('Tgid:'):
                    tgid = int(line.split()[1])
                    return tgid == pid

            raise ValueError("'Tgid' line not found in %s" % path)
    except (EnvironmentError, ValueError):
        return pid in pids()


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
        except EnvironmentError as err:
            if err.errno not in (errno.ENOENT, errno.ESRCH,
             errno.EPERM, errno.EACCES):
                raise
        else:
            rpar = data.rfind(')')
            dset = data[rpar + 2:].split()
            ppid = int(dset[1])
            ret[pid] = ppid

    return ret


def wrap_exceptions(fun):
    """Decorator which translates bare OSError and IOError exceptions
    into NoSuchProcess and AccessDenied.
    """

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        try:
            return fun(self, *args, **kwargs)
        except EnvironmentError as err:
            if err.errno in (errno.EPERM, errno.EACCES):
                raise AccessDenied(self.pid, self._name)
            if err.errno == errno.ESRCH:
                raise NoSuchProcess(self.pid, self._name)
            if err.errno == errno.ENOENT and not os.path.exists('%s/%s' % (
             self._procfs_path, self.pid)):
                raise NoSuchProcess(self.pid, self._name)
            raise

    return wrapper


class Process(object):
    """Linux process implementation."""
    __slots__ = [
     'pid', '_name', '_ppid', '_procfs_path']

    def __init__(self, pid):
        self.pid = pid
        self._name = None
        self._ppid = None
        self._procfs_path = get_procfs_path()
        return

    @memoize_when_activated
    def _parse_stat_file(self):
        """Parse /proc/{pid}/stat file. Return a list of fields where
        process name is in position 0.
        Using "man proc" as a reference: where "man proc" refers to
        position N, always substract 2 (e.g starttime pos 22 in
        'man proc' == pos 20 in the list returned here).
        The return value is cached in case oneshot() ctx manager is
        in use.
        """
        with open_binary('%s/%s/stat' % (self._procfs_path, self.pid)) as (f):
            data = f.read()
        rpar = data.rfind(')')
        name = data[data.find('(') + 1:rpar]
        others = data[rpar + 2:].split()
        return [name] + others

    @memoize_when_activated
    def _read_status_file(self):
        """Read /proc/{pid}/stat file and return its content.
        The return value is cached in case oneshot() ctx manager is
        in use.
        """
        with open_binary('%s/%s/status' % (self._procfs_path, self.pid)) as (f):
            return f.read()

    @memoize_when_activated
    def _read_smaps_file(self):
        with open_binary('%s/%s/smaps' % (self._procfs_path, self.pid), buffering=BIGFILE_BUFFERING) as (f):
            return f.read().strip()

    def oneshot_enter(self):
        self._parse_stat_file.cache_activate()
        self._read_status_file.cache_activate()
        self._read_smaps_file.cache_activate()

    def oneshot_exit(self):
        self._parse_stat_file.cache_deactivate()
        self._read_status_file.cache_deactivate()
        self._read_smaps_file.cache_deactivate()

    @wrap_exceptions
    def name(self):
        name = self._parse_stat_file()[0]
        if PY3:
            name = decode(name)
        return name

    def exe(self):
        try:
            return readlink('%s/%s/exe' % (self._procfs_path, self.pid))
        except OSError as err:
            if err.errno in (errno.ENOENT, errno.ESRCH):
                if os.path.lexists('%s/%s' % (self._procfs_path, self.pid)):
                    return ''
                if not pid_exists(self.pid):
                    raise NoSuchProcess(self.pid, self._name)
                else:
                    raise ZombieProcess(self.pid, self._name, self._ppid)
            if err.errno in (errno.EPERM, errno.EACCES):
                raise AccessDenied(self.pid, self._name)
            raise

    @wrap_exceptions
    def cmdline(self):
        with open_text('%s/%s/cmdline' % (self._procfs_path, self.pid)) as (f):
            data = f.read()
        if not data:
            return []
        sep = '\x00' if data.endswith('\x00') else ' '
        if data.endswith(sep):
            data = data[:-1]
        return [ x for x in data.split(sep) ]

    @wrap_exceptions
    def environ(self):
        with open_text('%s/%s/environ' % (self._procfs_path, self.pid)) as (f):
            data = f.read()
        return parse_environ_block(data)

    @wrap_exceptions
    def terminal(self):
        tty_nr = int(self._parse_stat_file()[5])
        tmap = _psposix.get_terminal_map()
        try:
            return tmap[tty_nr]
        except KeyError:
            return

        return

    if os.path.exists('/proc/%s/io' % os.getpid()):

        @wrap_exceptions
        def io_counters(self):
            fname = '%s/%s/io' % (self._procfs_path, self.pid)
            fields = {}
            with open_binary(fname) as (f):
                for line in f:
                    line = line.strip()
                    if line:
                        name, value = line.split(': ')
                        fields[name] = int(value)

            if not fields:
                raise RuntimeError('%s file was empty' % fname)
            return pio(fields['syscr'], fields['syscw'], fields['read_bytes'], fields['write_bytes'], fields['rchar'], fields['wchar'])

    else:

        def io_counters(self):
            raise NotImplementedError("couldn't find /proc/%s/io (kernel too old?)" % self.pid)

    @wrap_exceptions
    def cpu_times(self):
        values = self._parse_stat_file()
        utime = float(values[12]) / CLOCK_TICKS
        stime = float(values[13]) / CLOCK_TICKS
        children_utime = float(values[14]) / CLOCK_TICKS
        children_stime = float(values[15]) / CLOCK_TICKS
        return _common.pcputimes(utime, stime, children_utime, children_stime)

    @wrap_exceptions
    def cpu_num(self):
        """What CPU the process is on."""
        return int(self._parse_stat_file()[37])

    @wrap_exceptions
    def wait(self, timeout=None):
        return _psposix.wait_pid(self.pid, timeout, self._name)

    @wrap_exceptions
    def create_time(self):
        values = self._parse_stat_file()
        bt = BOOT_TIME or boot_time()
        return float(values[20]) / CLOCK_TICKS + bt

    @wrap_exceptions
    def memory_info(self):
        with open_binary('%s/%s/statm' % (self._procfs_path, self.pid)) as (f):
            vms, rss, shared, text, lib, data, dirty = [ int(x) * PAGESIZE for x in f.readline().split()[:7] ]
        return pmem(rss, vms, shared, text, lib, data, dirty)

    if HAS_SMAPS:

        @wrap_exceptions
        def memory_full_info(self, _private_re=re.compile('\\nPrivate.*:\\s+(\\d+)'), _pss_re=re.compile('\\nPss\\:\\s+(\\d+)'), _swap_re=re.compile('\\nSwap\\:\\s+(\\d+)')):
            basic_mem = self.memory_info()
            smaps_data = self._read_smaps_file()
            uss = sum(map(int, _private_re.findall(smaps_data))) * 1024
            pss = sum(map(int, _pss_re.findall(smaps_data))) * 1024
            swap = sum(map(int, _swap_re.findall(smaps_data))) * 1024
            return pfullmem(*(basic_mem + (uss, pss, swap)))

    else:
        memory_full_info = memory_info
    if HAS_SMAPS:

        @wrap_exceptions
        def memory_maps(self):
            """Return process's mapped memory regions as a list of named
            tuples. Fields are explained in 'man proc'; here is an updated
            (Apr 2012) version: http://goo.gl/fmebo
            """

            def get_blocks(lines, current_block):
                data = {}
                for line in lines:
                    fields = line.split(None, 5)
                    if not fields[0].endswith(':'):
                        yield (current_block.pop(), data)
                        current_block.append(line)
                    else:
                        try:
                            data[fields[0]] = int(fields[1]) * 1024
                        except ValueError:
                            if fields[0].startswith('VmFlags:'):
                                continue
                            else:
                                raise ValueError("don't know how to interpret line %r" % line)

                yield (
                 current_block.pop(), data)
                return

            data = self._read_smaps_file()
            if not data:
                return []
            else:
                lines = data.split('\n')
                ls = []
                first_line = lines.pop(0)
                current_block = [first_line]
                for header, data in get_blocks(lines, current_block):
                    hfields = header.split(None, 5)
                    try:
                        addr, perms, offset, dev, inode, path = hfields
                    except ValueError:
                        addr, perms, offset, dev, inode, path = hfields + ['']

                    if not path:
                        path = '[anon]'
                    else:
                        if PY3:
                            path = decode(path)
                        path = path.strip()
                        if path.endswith(' (deleted)') and not path_exists_strict(path):
                            path = path[:-10]
                    ls.append((
                     decode(addr), decode(perms), path,
                     data['Rss:'],
                     data.get('Size:', 0),
                     data.get('Pss:', 0),
                     data.get('Shared_Clean:', 0),
                     data.get('Shared_Dirty:', 0),
                     data.get('Private_Clean:', 0),
                     data.get('Private_Dirty:', 0),
                     data.get('Referenced:', 0),
                     data.get('Anonymous:', 0),
                     data.get('Swap:', 0)))

                return ls

    else:

        def memory_maps(self):
            raise NotImplementedError('/proc/%s/smaps does not exist on kernels < 2.6.14 or if CONFIG_MMU kernel configuration option is not enabled.' % self.pid)

    @wrap_exceptions
    def cwd(self):
        try:
            return readlink('%s/%s/cwd' % (self._procfs_path, self.pid))
        except OSError as err:
            if err.errno in (errno.ENOENT, errno.ESRCH):
                if not pid_exists(self.pid):
                    raise NoSuchProcess(self.pid, self._name)
                else:
                    raise ZombieProcess(self.pid, self._name, self._ppid)
            raise

    @wrap_exceptions
    def num_ctx_switches(self, _ctxsw_re=re.compile('ctxt_switches:\\t(\\d+)')):
        data = self._read_status_file()
        ctxsw = _ctxsw_re.findall(data)
        if not ctxsw:
            raise NotImplementedError("'voluntary_ctxt_switches' and 'nonvoluntary_ctxt_switches'lines were not found in %s/%s/status; the kernel is probably older than 2.6.23" % (
             self._procfs_path, self.pid))
        else:
            return _common.pctxsw(int(ctxsw[0]), int(ctxsw[1]))

    @wrap_exceptions
    def num_threads(self, _num_threads_re=re.compile('Threads:\\t(\\d+)')):
        data = self._read_status_file()
        return int(_num_threads_re.findall(data)[0])

    @wrap_exceptions
    def threads(self):
        thread_ids = os.listdir('%s/%s/task' % (self._procfs_path, self.pid))
        thread_ids.sort()
        retlist = []
        hit_enoent = False
        for thread_id in thread_ids:
            fname = '%s/%s/task/%s/stat' % (
             self._procfs_path, self.pid, thread_id)
            try:
                with open_binary(fname) as (f):
                    st = f.read().strip()
            except IOError as err:
                if err.errno == errno.ENOENT:
                    hit_enoent = True
                    continue
                raise

            st = st[st.find(')') + 2:]
            values = st.split(' ')
            utime = float(values[11]) / CLOCK_TICKS
            stime = float(values[12]) / CLOCK_TICKS
            ntuple = _common.pthread(int(thread_id), utime, stime)
            retlist.append(ntuple)

        if hit_enoent:
            os.stat('%s/%s' % (self._procfs_path, self.pid))
        return retlist

    @wrap_exceptions
    def nice_get(self):
        return cext_posix.getpriority(self.pid)

    @wrap_exceptions
    def nice_set(self, value):
        return cext_posix.setpriority(self.pid, value)

    @wrap_exceptions
    def cpu_affinity_get(self):
        return cext.proc_cpu_affinity_get(self.pid)

    def _get_eligible_cpus(self, _re=re.compile('Cpus_allowed_list:\\t(\\d+)-(\\d+)')):
        data = self._read_status_file()
        match = _re.findall(data)
        if match:
            return list(range(int(match[0][0]), int(match[0][1]) + 1))
        else:
            return list(range(len(per_cpu_times())))

    @wrap_exceptions
    def cpu_affinity_set(self, cpus):
        try:
            cext.proc_cpu_affinity_set(self.pid, cpus)
        except (OSError, ValueError) as err:
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

    if hasattr(cext, 'proc_ioprio_get'):

        @wrap_exceptions
        def ionice_get(self):
            ioclass, value = cext.proc_ioprio_get(self.pid)
            if enum is not None:
                ioclass = IOPriority(ioclass)
            return _common.pionice(ioclass, value)

        @wrap_exceptions
        def ionice_set(self, ioclass, value):
            if value is not None:
                if not PY3 and not isinstance(value, (int, long)):
                    msg = 'value argument is not an integer (gor %r)' % value
                    raise TypeError(msg)
                if not 0 <= value <= 7:
                    raise ValueError('value argument range expected is between 0 and 7')
            if ioclass in (IOPRIO_CLASS_NONE, None):
                if value:
                    msg = "can't specify value with IOPRIO_CLASS_NONE (got %r)" % value
                    raise ValueError(msg)
                ioclass = IOPRIO_CLASS_NONE
                value = 0
            elif ioclass == IOPRIO_CLASS_IDLE:
                if value:
                    msg = "can't specify value with IOPRIO_CLASS_IDLE (got %r)" % value
                    raise ValueError(msg)
                value = 0
            elif ioclass in (IOPRIO_CLASS_RT, IOPRIO_CLASS_BE):
                if value is None:
                    value = 4
            else:
                raise ValueError('invalid ioclass argument %r' % ioclass)
            return cext.proc_ioprio_set(self.pid, ioclass, value)

    if HAS_PRLIMIT:

        @wrap_exceptions
        def rlimit(self, resource, limits=None):
            if self.pid == 0:
                raise ValueError("can't use prlimit() against PID 0 process")
            try:
                if limits is None:
                    return cext.linux_prlimit(self.pid, resource)
                if len(limits) != 2:
                    raise ValueError('second argument must be a (soft, hard) tuple, got %s' % repr(limits))
                soft, hard = limits
                cext.linux_prlimit(self.pid, resource, soft, hard)
            except OSError as err:
                if err.errno == errno.ENOSYS and pid_exists(self.pid):
                    raise ZombieProcess(self.pid, self._name, self._ppid)
                else:
                    raise

            return

    @wrap_exceptions
    def status(self):
        letter = self._parse_stat_file()[1]
        if PY3:
            letter = letter.decode()
        return PROC_STATUSES.get(letter, '?')

    @wrap_exceptions
    def open_files(self):
        retlist = []
        files = os.listdir('%s/%s/fd' % (self._procfs_path, self.pid))
        hit_enoent = False
        for fd in files:
            file = '%s/%s/fd/%s' % (self._procfs_path, self.pid, fd)
            try:
                path = readlink(file)
            except OSError as err:
                if err.errno in (errno.ENOENT, errno.ESRCH):
                    hit_enoent = True
                    continue
                elif err.errno == errno.EINVAL:
                    continue
                else:
                    raise
            else:
                if path.startswith('/') and isfile_strict(path):
                    file = '%s/%s/fdinfo/%s' % (
                     self._procfs_path, self.pid, fd)
                    try:
                        with open_binary(file) as (f):
                            pos = int(f.readline().split()[1])
                            flags = int(f.readline().split()[1], 8)
                    except IOError as err:
                        if err.errno == errno.ENOENT:
                            hit_enoent = True
                        else:
                            raise
                    else:
                        mode = file_flags_to_mode(flags)
                        ntuple = popenfile(path, int(fd), int(pos), mode, flags)
                        retlist.append(ntuple)

        if hit_enoent:
            os.stat('%s/%s' % (self._procfs_path, self.pid))
        return retlist

    @wrap_exceptions
    def connections(self, kind='inet'):
        ret = _connections.retrieve(kind, self.pid)
        os.stat('%s/%s' % (self._procfs_path, self.pid))
        return ret

    @wrap_exceptions
    def num_fds(self):
        return len(os.listdir('%s/%s/fd' % (self._procfs_path, self.pid)))

    @wrap_exceptions
    def ppid(self):
        return int(self._parse_stat_file()[2])

    @wrap_exceptions
    def uids(self, _uids_re=re.compile('Uid:\\t(\\d+)\\t(\\d+)\\t(\\d+)')):
        data = self._read_status_file()
        real, effective, saved = _uids_re.findall(data)[0]
        return _common.puids(int(real), int(effective), int(saved))

    @wrap_exceptions
    def gids(self, _gids_re=re.compile('Gid:\\t(\\d+)\\t(\\d+)\\t(\\d+)')):
        data = self._read_status_file()
        real, effective, saved = _gids_re.findall(data)[0]
        return _common.pgids(int(real), int(effective), int(saved))