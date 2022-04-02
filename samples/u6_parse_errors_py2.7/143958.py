# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: C:\Users\Administrator\Desktop\PyInstaller-2.1\send\build\send\out00-PYZ.pyz\psutil._pslinux
"""Linux platform implementation."""
from __future__ import division
import os, errno, socket, struct, sys, base64, re, warnings, _psutil_posix, _psutil_linux
from psutil import _psposix
from psutil._error import AccessDenied, NoSuchProcess, TimeoutExpired
from psutil._common import *
from _psutil_linux import *
from psutil._compat import PY3, xrange, long, namedtuple, wraps
__extra__all__ = [
 'IOPRIO_CLASS_NONE', 'IOPRIO_CLASS_RT', 'IOPRIO_CLASS_BE',
 'IOPRIO_CLASS_IDLE',
 'CONN_ESTABLISHED', 'CONN_SYN_SENT', 'CONN_SYN_RECV', 'CONN_FIN_WAIT1',
 'CONN_FIN_WAIT2', 'CONN_TIME_WAIT', 'CONN_CLOSE', 'CONN_CLOSE_WAIT',
 'CONN_LAST_ACK', 'CONN_LISTEN', 'CONN_CLOSING',
 'phymem_buffers', 'cached_phymem']
HAS_PRLIMIT = hasattr(_psutil_linux, 'prlimit')
if HAS_PRLIMIT:
    for name in dir(_psutil_linux):
        if name.startswith('RLIM'):
            __extra__all__.append(name)

def get_system_boot_time():
    """Return the system boot time expressed in seconds since the epoch."""
    f = open('/proc/stat', 'r')
    try:
        for line in f:
            if line.startswith('btime'):
                return float(line.strip().split()[1])

        raise RuntimeError("line 'btime' not found")
    finally:
        f.close()


def get_num_cpus():
    """Return the number of CPUs on the system"""
    try:
        return os.sysconf('SC_NPROCESSORS_ONLN')
    except ValueError:
        num = 0
        f = open('/proc/cpuinfo', 'r')
        try:
            lines = f.readlines()
        finally:
            f.close()

        for line in lines:
            if line.lower().startswith('processor'):
                num += 1

    if num == 0:
        f = open('/proc/stat', 'r')
        try:
            lines = f.readlines()
        finally:
            f.close()

        search = re.compile('cpu\\d')
        for line in lines:
            line = line.split(' ')[0]
            if search.match(line):
                num += 1

    if num == 0:
        raise RuntimeError("couldn't determine platform's NUM_CPUS")
    return num


_CLOCK_TICKS = os.sysconf('SC_CLK_TCK')
_PAGESIZE = os.sysconf('SC_PAGE_SIZE')
try:
    BOOT_TIME = get_system_boot_time()
except Exception:
    BOOT_TIME = None
    warnings.warn("couldn't determine platform's BOOT_TIME", RuntimeWarning)

try:
    NUM_CPUS = get_num_cpus()
except Exception:
    NUM_CPUS = None
    warnings.warn("couldn't determine platform's NUM_CPUS", RuntimeWarning)

try:
    TOTAL_PHYMEM = _psutil_linux.get_sysinfo()[0]
except Exception:
    TOTAL_PHYMEM = None
    warnings.warn("couldn't determine platform's TOTAL_PHYMEM", RuntimeWarning)

IOPRIO_CLASS_NONE = 0
IOPRIO_CLASS_RT = 1
IOPRIO_CLASS_BE = 2
IOPRIO_CLASS_IDLE = 3
_TCP_STATES_TABLE = {'01': CONN_ESTABLISHED, '02': CONN_SYN_SENT, 
   '03': CONN_SYN_RECV, 
   '04': CONN_FIN_WAIT1, 
   '05': CONN_FIN_WAIT2, 
   '06': CONN_TIME_WAIT, 
   '07': CONN_CLOSE, 
   '08': CONN_CLOSE_WAIT, 
   '09': CONN_LAST_ACK, 
   '0A': CONN_LISTEN, 
   '0B': CONN_CLOSING}
nt_virtmem_info = namedtuple('vmem', (' ').join([
 'total', 'available', 'percent', 'used', 'free',
 'active',
 'inactive',
 'buffers',
 'cached']))

def virtual_memory():
    total, free, buffers, shared, _, _ = _psutil_linux.get_sysinfo()
    cached = active = inactive = None
    f = open('/proc/meminfo', 'r')
    try:
        for line in f:
            if line.startswith('Cached:'):
                cached = int(line.split()[1]) * 1024
            elif line.startswith('Active:'):
                active = int(line.split()[1]) * 1024
            elif line.startswith('Inactive:'):
                inactive = int(line.split()[1]) * 1024
            if cached is not None and active is not None and inactive is not None:
                break
        else:
            msg = "'cached', 'active' and 'inactive' memory stats couldn't be determined and were set to 0"
            warnings.warn(msg, RuntimeWarning)
            cached = active = inactive = 0

    finally:
        f.close()

    avail = free + buffers + cached
    used = total - free
    percent = usage_percent(total - avail, total, _round=1)
    return nt_virtmem_info(total, avail, percent, used, free, active, inactive, buffers, cached)


def swap_memory():
    _, _, _, _, total, free = _psutil_linux.get_sysinfo()
    used = total - free
    percent = usage_percent(used, total, _round=1)
    f = open('/proc/vmstat', 'r')
    sin = sout = None
    try:
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

    finally:
        f.close()

    return nt_swapmeminfo(total, used, free, percent, sin, sout)


@deprecated('psutil.virtual_memory().cached')
def cached_phymem():
    return virtual_memory().cached


@deprecated('psutil.virtual_memory().buffers')
def phymem_buffers():
    return virtual_memory().buffers


@memoize
def _get_cputimes_ntuple():
    """ Return a (nt, rindex) tuple depending on the CPU times available
    on this Linux kernel version which may be:
    user, nice, system, idle, iowait, irq, softirq [steal, [guest, [guest_nice]]]
    """
    f = open('/proc/stat', 'r')
    try:
        values = f.readline().split()[1:]
    finally:
        f.close()

    fields = [
     'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq']
    rindex = 8
    vlen = len(values)
    if vlen >= 8:
        fields.append('steal')
        rindex += 1
    if vlen >= 9:
        fields.append('guest')
        rindex += 1
    if vlen >= 10:
        fields.append('guest_nice')
        rindex += 1
    return (
     namedtuple('cputimes', (' ').join(fields)), rindex)


def get_system_cpu_times():
    """Return a named tuple representing the following system-wide
    CPU times:
    user, nice, system, idle, iowait, irq, softirq [steal, [guest, [guest_nice]]]
    Last 3 fields may not be available on all Linux kernel versions.
    """
    f = open('/proc/stat', 'r')
    try:
        values = f.readline().split()
    finally:
        f.close()

    nt, rindex = _get_cputimes_ntuple()
    fields = values[1:rindex]
    fields = [ float(x) / _CLOCK_TICKS for x in fields ]
    return nt(*fields)


def get_system_per_cpu_times():
    """Return a list of namedtuple representing the CPU times
    for every CPU available on the system.
    """
    nt, rindex = _get_cputimes_ntuple()
    cpus = []
    f = open('/proc/stat', 'r')
    try:
        f.readline()
        for line in f:
            if line.startswith('cpu'):
                fields = line.split()[1:rindex]
                fields = [ float(x) / _CLOCK_TICKS for x in fields ]
                entry = nt(*fields)
                cpus.append(entry)

        return cpus
    finally:
        f.close()


def disk_partitions(all=False):
    """Return mounted disk partitions as a list of nameduples"""
    phydevs = []
    f = open('/proc/filesystems', 'r')
    try:
        for line in f:
            if not line.startswith('nodev'):
                phydevs.append(line.strip())

    finally:
        f.close()

    retlist = []
    partitions = _psutil_linux.get_disk_partitions()
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        if device == 'none':
            device = ''
        if not all:
            if device == '' or fstype not in phydevs:
                continue
        ntuple = nt_partition(device, mountpoint, fstype, opts)
        retlist.append(ntuple)

    return retlist


get_disk_usage = _psposix.get_disk_usage

def get_system_users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = _psutil_linux.get_system_users()
    for item in rawlist:
        user, tty, hostname, tstamp, user_process = item
        if not user_process:
            continue
        if hostname == ':0.0':
            hostname = 'localhost'
        nt = nt_user(user, tty or None, hostname, tstamp)
        retlist.append(nt)

    return retlist


def get_pid_list():
    """Returns a list of PIDs currently running on the system."""
    pids = [ int(x) for x in os.listdir('/proc') if x.isdigit() ]
    return pids


def pid_exists(pid):
    """Check For the existence of a unix pid."""
    return _psposix.pid_exists(pid)


def net_io_counters--- This code section failed: ---

 L. 349         0  LOAD_GLOBAL           0  'open'
                3  LOAD_CONST               '/proc/net/dev'
                6  LOAD_CONST               'r'
                9  CALL_FUNCTION_2       2  None
               12  STORE_FAST            0  'f'

 L. 350        15  SETUP_FINALLY        16  'to 34'

 L. 351        18  LOAD_FAST             0  'f'
               21  LOAD_ATTR             1  'readlines'
               24  CALL_FUNCTION_0       0  None
               27  STORE_FAST            1  'lines'
               30  POP_BLOCK        
               31  LOAD_CONST               None
             34_0  COME_FROM_FINALLY    15  '15'

 L. 353        34  LOAD_FAST             0  'f'
               37  LOAD_ATTR             2  'close'
               40  CALL_FUNCTION_0       0  None
               43  POP_TOP          
               44  END_FINALLY      

 L. 355        45  BUILD_MAP_0           0  None
               48  STORE_FAST            2  'retdict'

 L. 356        51  SETUP_LOOP          264  'to 318'
               54  LOAD_FAST             1  'lines'
               57  LOAD_CONST               2
               60  SLICE+1          
               61  GET_ITER         
               62  FOR_ITER            252  'to 317'
               65  STORE_FAST            3  'line'

 L. 357        68  LOAD_FAST             3  'line'
               71  LOAD_ATTR             3  'rfind'
               74  LOAD_CONST               ':'
               77  CALL_FUNCTION_1       1  None
               80  STORE_FAST            4  'colon'

 L. 358        83  LOAD_FAST             4  'colon'
               86  LOAD_CONST               0
               89  COMPARE_OP            4  >
               92  POP_JUMP_IF_TRUE    110  'to 110'
               95  LOAD_ASSERT              AssertionError
               98  LOAD_GLOBAL           5  'repr'
              101  LOAD_FAST             3  'line'
              104  CALL_FUNCTION_1       1  None
              107  RAISE_VARARGS_2       2  None

 L. 359       110  LOAD_FAST             3  'line'
              113  LOAD_FAST             4  'colon'
              116  SLICE+2          
              117  LOAD_ATTR             6  'strip'
              120  CALL_FUNCTION_0       0  None
              123  STORE_FAST            5  'name'

 L. 360       126  LOAD_FAST             3  'line'
              129  LOAD_FAST             4  'colon'
              132  LOAD_CONST               1
              135  BINARY_ADD       
              136  SLICE+1          
              137  LOAD_ATTR             6  'strip'
              140  CALL_FUNCTION_0       0  None
              143  LOAD_ATTR             7  'split'
              146  CALL_FUNCTION_0       0  None
              149  STORE_FAST            6  'fields'

 L. 361       152  LOAD_GLOBAL           8  'int'
              155  LOAD_FAST             6  'fields'
              158  LOAD_CONST               0
              161  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  None
              165  STORE_FAST            7  'bytes_recv'

 L. 362       168  LOAD_GLOBAL           8  'int'
              171  LOAD_FAST             6  'fields'
              174  LOAD_CONST               1
              177  BINARY_SUBSCR    
              178  CALL_FUNCTION_1       1  None
              181  STORE_FAST            8  'packets_recv'

 L. 363       184  LOAD_GLOBAL           8  'int'
              187  LOAD_FAST             6  'fields'
              190  LOAD_CONST               2
              193  BINARY_SUBSCR    
              194  CALL_FUNCTION_1       1  None
              197  STORE_FAST            9  'errin'

 L. 364       200  LOAD_GLOBAL           8  'int'
              203  LOAD_FAST             6  'fields'
              206  LOAD_CONST               3
              209  BINARY_SUBSCR    
              210  CALL_FUNCTION_1       1  None
              213  STORE_FAST           10  'dropin'

 L. 365       216  LOAD_GLOBAL           8  'int'
              219  LOAD_FAST             6  'fields'
              222  LOAD_CONST               8
              225  BINARY_SUBSCR    
              226  CALL_FUNCTION_1       1  None
              229  STORE_FAST           11  'bytes_sent'

 L. 366       232  LOAD_GLOBAL           8  'int'
              235  LOAD_FAST             6  'fields'
              238  LOAD_CONST               9
              241  BINARY_SUBSCR    
              242  CALL_FUNCTION_1       1  None
              245  STORE_FAST           12  'packets_sent'

 L. 367       248  LOAD_GLOBAL           8  'int'
              251  LOAD_FAST             6  'fields'
              254  LOAD_CONST               10
              257  BINARY_SUBSCR    
              258  CALL_FUNCTION_1       1  None
              261  STORE_FAST           13  'errout'

 L. 368       264  LOAD_GLOBAL           8  'int'
              267  LOAD_FAST             6  'fields'
              270  LOAD_CONST               11
              273  BINARY_SUBSCR    
              274  CALL_FUNCTION_1       1  None
              277  STORE_FAST           14  'dropout'

 L. 369       280  LOAD_FAST            11  'bytes_sent'
              283  LOAD_FAST             7  'bytes_recv'
              286  LOAD_FAST            12  'packets_sent'
              289  LOAD_FAST             8  'packets_recv'

 L. 370       292  LOAD_FAST             9  'errin'
              295  LOAD_FAST            13  'errout'
              298  LOAD_FAST            10  'dropin'
              301  LOAD_FAST            14  'dropout'
              304  BUILD_TUPLE_8         8 
              307  LOAD_FAST             2  'retdict'
              310  LOAD_FAST             5  'name'
              313  STORE_SUBSCR     
              314  JUMP_BACK            62  'to 62'
              317  POP_BLOCK        
            318_0  COME_FROM            51  '51'

 L. 371       318  LOAD_FAST             2  'retdict'
              321  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 317


def disk_io_counters():
    """Return disk I/O statistics for every disk installed on the
    system as a dict of raw tuples.
    """
    SECTOR_SIZE = 512
    partitions = []
    f = open('/proc/partitions', 'r')
    try:
        lines = f.readlines()[2:]
    finally:
        f.close()

    for line in reversed(lines):
        _, _, _, name = line.split()
        if name[(-1)].isdigit():
            partitions.append(name)
        elif not partitions or not partitions[(-1)].startswith(name):
            partitions.append(name)

    retdict = {}
    f = open('/proc/diskstats', 'r')
    try:
        lines = f.readlines()
    finally:
        f.close()

    for line in lines:
        _, _, name, reads, _, rbytes, rtime, writes, _, wbytes, wtime = line.split()[:11]
        if name in partitions:
            rbytes = int(rbytes) * SECTOR_SIZE
            wbytes = int(wbytes) * SECTOR_SIZE
            reads = int(reads)
            writes = int(writes)
            rtime = int(rtime)
            wtime = int(wtime)
            retdict[name] = (reads, writes, rbytes, wbytes, rtime, wtime)

    return retdict


_status_map = {'R': STATUS_RUNNING, 'S': STATUS_SLEEPING, 
   'D': STATUS_DISK_SLEEP, 
   'T': STATUS_STOPPED, 
   't': STATUS_TRACING_STOP, 
   'Z': STATUS_ZOMBIE, 
   'X': STATUS_DEAD, 
   'x': STATUS_DEAD, 
   'K': STATUS_WAKE_KILL, 
   'W': STATUS_WAKING}

def wrap_exceptions(fun):
    """Decorator which translates bare OSError and IOError exceptions
    into NoSuchProcess and AccessDenied.
    """

    @wraps(fun)
    def wrapper(self, *args, **kwargs):
        try:
            return fun(self, *args, **kwargs)
        except EnvironmentError:
            err = sys.exc_info()[1]
            if err.errno in (errno.ENOENT, errno.ESRCH):
                raise NoSuchProcess(self.pid, self._process_name)
            if err.errno in (errno.EPERM, errno.EACCES):
                raise AccessDenied(self.pid, self._process_name)
            raise

    return wrapper


class Process(object):
    """Linux process implementation."""
    __slots__ = [
     'pid', '_process_name']

    def __init__(self, pid):
        self.pid = pid
        self._process_name = None
        return

    @wrap_exceptions
    def get_process_name(self):
        f = open('/proc/%s/stat' % self.pid)
        try:
            name = f.read().split(' ')[1].replace('(', '').replace(')', '')
        finally:
            f.close()

        return name

    def get_process_exe(self):
        try:
            exe = os.readlink('/proc/%s/exe' % self.pid)
        except (OSError, IOError):
            err = sys.exc_info()[1]
            if err.errno == errno.ENOENT:
                if os.path.lexists('/proc/%s/exe' % self.pid):
                    return ''
                raise NoSuchProcess(self.pid, self._process_name)
            if err.errno in (errno.EPERM, errno.EACCES):
                raise AccessDenied(self.pid, self._process_name)
            raise

        exe = exe.replace('\x00', '')
        if exe.endswith(' (deleted)') and not os.path.exists(exe):
            exe = exe[:-10]
        return exe

    @wrap_exceptions
    def get_process_cmdline(self):
        f = open('/proc/%s/cmdline' % self.pid)
        try:
            return [ x for x in f.read().split('\x00') if x ]
        finally:
            f.close()

    @wrap_exceptions
    def get_process_terminal(self):
        tmap = _psposix._get_terminal_map()
        f = open('/proc/%s/stat' % self.pid)
        try:
            tty_nr = int(f.read().split(' ')[6])
        finally:
            f.close()

        try:
            return tmap[tty_nr]
        except KeyError:
            return

        return

    if os.path.exists('/proc/%s/io' % os.getpid()):

        @wrap_exceptions
        def get_process_io_counters(self):
            fname = '/proc/%s/io' % self.pid
            f = open(fname)
            try:
                rcount = wcount = rbytes = wbytes = None
                for line in f:
                    if rcount is None and line.startswith('syscr'):
                        rcount = int(line.split()[1])
                    elif wcount is None and line.startswith('syscw'):
                        wcount = int(line.split()[1])
                    elif rbytes is None and line.startswith('read_bytes'):
                        rbytes = int(line.split()[1])
                    elif wbytes is None and line.startswith('write_bytes'):
                        wbytes = int(line.split()[1])

                for x in (rcount, wcount, rbytes, wbytes):
                    if x is None:
                        raise NotImplementedError("couldn't read all necessary info from %r" % fname)

                return nt_io(rcount, wcount, rbytes, wbytes)
            finally:
                f.close()

            return

    else:

        def get_process_io_counters(self):
            raise NotImplementedError("couldn't find /proc/%s/io (kernel too old?)" % self.pid)

    @wrap_exceptions
    def get_cpu_times(self):
        f = open('/proc/%s/stat' % self.pid)
        try:
            st = f.read().strip()
        finally:
            f.close()

        st = st[st.find(')') + 2:]
        values = st.split(' ')
        utime = float(values[11]) / _CLOCK_TICKS
        stime = float(values[12]) / _CLOCK_TICKS
        return nt_cputimes(utime, stime)

    @wrap_exceptions
    def process_wait(self, timeout=None):
        try:
            return _psposix.wait_pid(self.pid, timeout)
        except TimeoutExpired:
            raise TimeoutExpired(self.pid, self._process_name)

    @wrap_exceptions
    def get_process_create_time(self):
        f = open('/proc/%s/stat' % self.pid)
        try:
            st = f.read().strip()
        finally:
            f.close()

        st = st[st.rfind(')') + 2:]
        values = st.split(' ')
        starttime = float(values[19]) / _CLOCK_TICKS + BOOT_TIME
        return starttime

    @wrap_exceptions
    def get_memory_info(self):
        f = open('/proc/%s/statm' % self.pid)
        try:
            vms, rss = f.readline().split()[:2]
            return nt_meminfo(int(rss) * _PAGESIZE, int(vms) * _PAGESIZE)
        finally:
            f.close()

    _nt_ext_mem = namedtuple('meminfo', 'rss vms shared text lib data dirty')

    @wrap_exceptions
    def get_ext_memory_info(self):
        f = open('/proc/%s/statm' % self.pid)
        try:
            vms, rss, shared, text, lib, data, dirty = [ int(x) * _PAGESIZE for x in f.readline().split()[:7] ]
        finally:
            f.close()

        return self._nt_ext_mem(rss, vms, shared, text, lib, data, dirty)

    _mmap_base_fields = [
     'path', 'rss', 'size', 'pss', 'shared_clean',
     'shared_dirty', 'private_clean', 'private_dirty',
     'referenced', 'anonymous', 'swap']
    nt_mmap_grouped = namedtuple('mmap', (' ').join(_mmap_base_fields))
    nt_mmap_ext = namedtuple('mmap', 'addr perms ' + (' ').join(_mmap_base_fields))

    def get_memory_maps(self):
        """Return process's mapped memory regions as a list of nameduples.
        Fields are explained in 'man proc'; here is an updated (Apr 2012)
        version: http://goo.gl/fmebo
        """
        f = None
        try:
            f = open('/proc/%s/smaps' % self.pid)
            first_line = f.readline()
            current_block = [first_line]

            def get_blocks():
                data = {}
                for line in f:
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

            if first_line:
                for header, data in get_blocks():
                    hfields = header.split(None, 5)
                    try:
                        addr, perms, offset, dev, inode, path = hfields
                    except ValueError:
                        addr, perms, offset, dev, inode, path = hfields + ['']

                    if not path:
                        path = '[anon]'
                    else:
                        path = path.strip()
                    yield (
                     addr, perms, path,
                     data['Rss:'],
                     data.get('Size:', 0),
                     data.get('Pss:', 0),
                     data.get('Shared_Clean:', 0),
                     data.get('Shared_Dirty:', 0),
                     data.get('Private_Clean:', 0),
                     data.get('Private_Dirty:', 0),
                     data.get('Referenced:', 0),
                     data.get('Anonymous:', 0),
                     data.get('Swap:', 0))

            f.close()
        except EnvironmentError:
            if f is not None:
                f.close()
            err = sys.exc_info()[1]
            if err.errno in (errno.ENOENT, errno.ESRCH):
                raise NoSuchProcess(self.pid, self._process_name)
            if err.errno in (errno.EPERM, errno.EACCES):
                raise AccessDenied(self.pid, self._process_name)
            raise
        except:
            if f is not None:
                f.close()
            raise

        f.close()
        return

    if not os.path.exists('/proc/%s/smaps' % os.getpid()):

        def get_memory_maps(self, ext):
            msg = "couldn't find /proc/%s/smaps; kernel < 2.6.14 or CONFIG_MMU kernel configuration option is not enabled" % self.pid
            raise NotImplementedError(msg)

    @wrap_exceptions
    def get_process_cwd(self):
        path = os.readlink('/proc/%s/cwd' % self.pid)
        return path.replace('\x00', '')

    @wrap_exceptions
    def get_num_ctx_switches(self):
        vol = unvol = None
        f = open('/proc/%s/status' % self.pid)
        try:
            for line in f:
                if line.startswith('voluntary_ctxt_switches'):
                    vol = int(line.split()[1])
                else:
                    if line.startswith('nonvoluntary_ctxt_switches'):
                        unvol = int(line.split()[1])
                    if vol is not None and unvol is not None:
                        return nt_ctxsw(vol, unvol)

            raise NotImplementedError("the 'voluntary_ctxt_switches' and 'nonvoluntary_ctxt_switches' fields were not found in /proc/%s/status; the kernel is probably older than 2.6.23" % self.pid)
        finally:
            f.close()

        return

    @wrap_exceptions
    def get_process_num_threads(self):
        f = open('/proc/%s/status' % self.pid)
        try:
            for line in f:
                if line.startswith('Threads:'):
                    return int(line.split()[1])

            raise NotImplementedError('line not found')
        finally:
            f.close()

    @wrap_exceptions
    def get_process_threads(self):
        thread_ids = os.listdir('/proc/%s/task' % self.pid)
        thread_ids.sort()
        retlist = []
        hit_enoent = False
        for thread_id in thread_ids:
            try:
                f = open('/proc/%s/task/%s/stat' % (self.pid, thread_id))
            except EnvironmentError:
                err = sys.exc_info()[1]
                if err.errno == errno.ENOENT:
                    hit_enoent = True
                    continue
                raise

            try:
                st = f.read().strip()
            finally:
                f.close()

            st = st[st.find(')') + 2:]
            values = st.split(' ')
            utime = float(values[11]) / _CLOCK_TICKS
            stime = float(values[12]) / _CLOCK_TICKS
            ntuple = nt_thread(int(thread_id), utime, stime)
            retlist.append(ntuple)

        if hit_enoent:
            os.stat('/proc/%s' % self.pid)
        return retlist

    @wrap_exceptions
    def get_process_nice(self):
        return _psutil_posix.getpriority(self.pid)

    @wrap_exceptions
    def set_process_nice(self, value):
        return _psutil_posix.setpriority(self.pid, value)

    @wrap_exceptions
    def get_process_cpu_affinity(self):
        from_bitmask = lambda x: [ i for i in xrange(64) if 1 << i & x ]
        bitmask = _psutil_linux.get_process_cpu_affinity(self.pid)
        return from_bitmask(bitmask)

    @wrap_exceptions
    def set_process_cpu_affinity(self, value):

        def to_bitmask(l):
            if not l:
                raise ValueError('invalid argument %r' % l)
            out = 0
            for b in l:
                if not isinstance(b, (int, long)) or b < 0:
                    raise ValueError('invalid argument %r' % b)
                out |= 2 ** b

            return out

        bitmask = to_bitmask(value)
        try:
            _psutil_linux.set_process_cpu_affinity(self.pid, bitmask)
        except OSError:
            err = sys.exc_info()[1]
            if err.errno == errno.EINVAL:
                allcpus = list(range(len(get_system_per_cpu_times())))
                for cpu in value:
                    if cpu not in allcpus:
                        raise ValueError('invalid CPU %i' % cpu)

            raise

    if hasattr(_psutil_linux, 'ioprio_get'):

        @wrap_exceptions
        def get_process_ionice(self):
            ioclass, value = _psutil_linux.ioprio_get(self.pid)
            return nt_ionice(ioclass, value)

        @wrap_exceptions
        def set_process_ionice(self, ioclass, value):
            if ioclass in (IOPRIO_CLASS_NONE, None):
                if value:
                    raise ValueError("can't specify value with IOPRIO_CLASS_NONE")
                ioclass = IOPRIO_CLASS_NONE
                value = 0
            if ioclass in (IOPRIO_CLASS_RT, IOPRIO_CLASS_BE):
                if value is None:
                    value = 4
            elif ioclass == IOPRIO_CLASS_IDLE:
                if value:
                    raise ValueError("can't specify value with IOPRIO_CLASS_IDLE")
                value = 0
            else:
                value = 0
            if not 0 <= value <= 8:
                raise ValueError('value argument range expected is between 0 and 8')
            return _psutil_linux.ioprio_set(self.pid, ioclass, value)

    if HAS_PRLIMIT:

        @wrap_exceptions
        def process_rlimit(self, resource, limits=None):
            if limits is None:
                return _psutil_linux.prlimit(self.pid, resource)
            else:
                if len(limits) != 2:
                    raise ValueError('second argument must be a (soft, hard) tuple')
                soft, hard = limits
                _psutil_linux.prlimit(self.pid, resource, soft, hard)
                return

    @wrap_exceptions
    def get_process_status(self):
        f = open('/proc/%s/status' % self.pid)
        try:
            for line in f:
                if line.startswith('State:'):
                    letter = line.split()[1]
                    return _status_map.get(letter, '?')

        finally:
            f.close()

    @wrap_exceptions
    def get_open_files(self):
        retlist = []
        files = os.listdir('/proc/%s/fd' % self.pid)
        hit_enoent = False
        for fd in files:
            file = '/proc/%s/fd/%s' % (self.pid, fd)
            if os.path.islink(file):
                try:
                    file = os.readlink(file)
                except OSError:
                    err = sys.exc_info()[1]
                    if err.errno == errno.ENOENT:
                        hit_enoent = True
                        continue
                    raise
                else:
                    if file.startswith('/') and isfile_strict(file):
                        ntuple = nt_openfile(file, int(fd))
                        retlist.append(ntuple)

        if hit_enoent:
            os.stat('/proc/%s' % self.pid)
        return retlist

    @wrap_exceptions
    def get_connections(self, kind='inet'):
        """Return connections opened by process as a list of namedtuples.
        The kind parameter filters for connections that fit the following
        criteria:

        Kind Value      Number of connections using
        inet            IPv4 and IPv6
        inet4           IPv4
        inet6           IPv6
        tcp             TCP
        tcp4            TCP over IPv4
        tcp6            TCP over IPv6
        udp             UDP
        udp4            UDP over IPv4
        udp6            UDP over IPv6
        all             the sum of all the possible families and protocols
        """
        inodes = {}
        for fd in os.listdir('/proc/%s/fd' % self.pid):
            try:
                inode = os.readlink('/proc/%s/fd/%s' % (self.pid, fd))
            except OSError:
                continue

            if inode.startswith('socket:['):
                inode = inode[8:][:-1]
                inodes[inode] = fd

        if not inodes:
            return []
        else:

            def process(file, family, type_):
                retlist = []
                try:
                    f = open(file, 'r')
                except IOError:
                    err = sys.exc_info()[1]
                    if err.errno == errno.ENOENT and file.endswith('6'):
                        return []
                    raise

                try:
                    f.readline()
                    for line in f:
                        if family in (socket.AF_INET, socket.AF_INET6):
                            _, laddr, raddr, status, _, _, _, _, _, inode = line.split()[:10]
                            if inode in inodes:
                                laddr = self._decode_address(laddr, family)
                                raddr = self._decode_address(raddr, family)
                                if type_ == socket.SOCK_STREAM:
                                    status = _TCP_STATES_TABLE[status]
                                else:
                                    status = CONN_NONE
                                fd = int(inodes[inode])
                                conn = nt_connection(fd, family, type_, laddr, raddr, status)
                                retlist.append(conn)
                        elif family == socket.AF_UNIX:
                            tokens = line.split()
                            _, _, _, _, type_, _, inode = tokens[0:7]
                            if inode in inodes:
                                if len(tokens) == 8:
                                    path = tokens[(-1)]
                                else:
                                    path = ''
                                fd = int(inodes[inode])
                                type_ = int(type_)
                                conn = nt_connection(fd, family, type_, path, None, CONN_NONE)
                                retlist.append(conn)
                        else:
                            raise ValueError(family)

                    return retlist
                finally:
                    f.close()

                return

            tcp4 = (
             'tcp', socket.AF_INET, socket.SOCK_STREAM)
            tcp6 = ('tcp6', socket.AF_INET6, socket.SOCK_STREAM)
            udp4 = ('udp', socket.AF_INET, socket.SOCK_DGRAM)
            udp6 = ('udp6', socket.AF_INET6, socket.SOCK_DGRAM)
            unix = ('unix', socket.AF_UNIX, None)
            tmap = {'all': (
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
            if kind not in tmap:
                raise ValueError('invalid %r kind argument; choose between %s' % (
                 kind, (', ').join([ repr(x) for x in tmap ])))
            ret = []
            for f, family, type_ in tmap[kind]:
                ret += process('/proc/net/%s' % f, family, type_)

            os.stat('/proc/%s' % self.pid)
            return ret

    @wrap_exceptions
    def get_num_fds(self):
        return len(os.listdir('/proc/%s/fd' % self.pid))

    @wrap_exceptions
    def get_process_ppid(self):
        f = open('/proc/%s/status' % self.pid)
        try:
            for line in f:
                if line.startswith('PPid:'):
                    return int(line.split()[1])

            raise NotImplementedError('line not found')
        finally:
            f.close()

    @wrap_exceptions
    def get_process_uids(self):
        f = open('/proc/%s/status' % self.pid)
        try:
            for line in f:
                if line.startswith('Uid:'):
                    _, real, effective, saved, fs = line.split()
                    return nt_uids(int(real), int(effective), int(saved))

            raise NotImplementedError('line not found')
        finally:
            f.close()

    @wrap_exceptions
    def get_process_gids(self):
        f = open('/proc/%s/status' % self.pid)
        try:
            for line in f:
                if line.startswith('Gid:'):
                    _, real, effective, saved, fs = line.split()
                    return nt_gids(int(real), int(effective), int(saved))

            raise NotImplementedError('line not found')
        finally:
            f.close()

    @staticmethod
    def _decode_address(addr, family):
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
        if PY3:
            ip = ip.encode('ascii')
        if not port:
            return ()
        if family == socket.AF_INET:
            if sys.byteorder == 'little':
                ip = socket.inet_ntop(family, base64.b16decode(ip)[::-1])
            else:
                ip = socket.inet_ntop(family, base64.b16decode(ip))
        else:
            ip = base64.b16decode(ip)
            if sys.byteorder == 'little':
                ip = socket.inet_ntop(socket.AF_INET6, struct.pack('>4I', *struct.unpack('<4I', ip)))
            else:
                ip = socket.inet_ntop(socket.AF_INET6, struct.pack('<4I', *struct.unpack('<4I', ip)))
        return (
         ip, port)