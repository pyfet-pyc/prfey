# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: psutil\_psaix.py
"""AIX platform implementation."""
import functools, glob, os, re, subprocess, sys
from collections import namedtuple
from . import _common
from . import _psposix
from . import _psutil_aix as cext
from . import _psutil_posix as cext_posix
from ._common import AccessDenied
from ._common import conn_to_ntuple
from ._common import get_procfs_path
from ._common import memoize_when_activated
from ._common import NIC_DUPLEX_FULL
from ._common import NIC_DUPLEX_HALF
from ._common import NIC_DUPLEX_UNKNOWN
from ._common import NoSuchProcess
from ._common import usage_percent
from ._common import ZombieProcess
from ._compat import FileNotFoundError
from ._compat import PermissionError
from ._compat import ProcessLookupError
from ._compat import PY3
__extra__all__ = [
 'PROCFS_PATH']
HAS_THREADS = hasattr(cext, 'proc_threads')
HAS_NET_IO_COUNTERS = hasattr(cext, 'net_io_counters')
HAS_PROC_IO_COUNTERS = hasattr(cext, 'proc_io_counters')
PAGE_SIZE = cext_posix.getpagesize()
AF_LINK = cext_posix.AF_LINK
PROC_STATUSES = {cext.SIDL: _common.STATUS_IDLE, 
 cext.SZOMB: _common.STATUS_ZOMBIE, 
 cext.SACTIVE: _common.STATUS_RUNNING, 
 cext.SSWAP: _common.STATUS_RUNNING, 
 cext.SSTOP: _common.STATUS_STOPPED}
TCP_STATUSES = {cext.TCPS_ESTABLISHED: _common.CONN_ESTABLISHED, 
 cext.TCPS_SYN_SENT: _common.CONN_SYN_SENT, 
 cext.TCPS_SYN_RCVD: _common.CONN_SYN_RECV, 
 cext.TCPS_FIN_WAIT_1: _common.CONN_FIN_WAIT1, 
 cext.TCPS_FIN_WAIT_2: _common.CONN_FIN_WAIT2, 
 cext.TCPS_TIME_WAIT: _common.CONN_TIME_WAIT, 
 cext.TCPS_CLOSED: _common.CONN_CLOSE, 
 cext.TCPS_CLOSE_WAIT: _common.CONN_CLOSE_WAIT, 
 cext.TCPS_LAST_ACK: _common.CONN_LAST_ACK, 
 cext.TCPS_LISTEN: _common.CONN_LISTEN, 
 cext.TCPS_CLOSING: _common.CONN_CLOSING, 
 cext.PSUTIL_CONN_NONE: _common.CONN_NONE}
proc_info_map = dict(ppid=0,
  rss=1,
  vms=2,
  create_time=3,
  nice=4,
  num_threads=5,
  status=6,
  ttynr=7)
pmem = namedtuple('pmem', ['rss', 'vms'])
pfullmem = pmem
scputimes = namedtuple('scputimes', ['user', 'system', 'idle', 'iowait'])
svmem = namedtuple('svmem', ['total', 'available', 'percent', 'used', 'free'])

def virtual_memory():
    total, avail, free, pinned, inuse = cext.virtual_mem()
    percent = usage_percent((total - avail), total, round_=1)
    return svmem(total, avail, percent, inuse, free)


def swap_memory():
    """Swap system memory as a (total, used, free, sin, sout) tuple."""
    total, free, sin, sout = cext.swap_mem()
    used = total - free
    percent = usage_percent(used, total, round_=1)
    return _common.sswap(total, used, free, percent, sin, sout)


def cpu_times():
    """Return system-wide CPU times as a named tuple"""
    ret = cext.per_cpu_times()
    return scputimes(*[sum(x) for x in zip(*ret)])


def per_cpu_times():
    """Return system per-CPU times as a list of named tuples"""
    ret = cext.per_cpu_times()
    return [scputimes(*x) for x in ret]


def cpu_count_logical--- This code section failed: ---

 L. 139         0  SETUP_FINALLY        14  'to 14'

 L. 140         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              sysconf
                6  LOAD_STR                 'SC_NPROCESSORS_ONLN'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 141        14  DUP_TOP          
               16  LOAD_GLOBAL              ValueError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 143        28  POP_EXCEPT       
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'
               34  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24


def cpu_count_physical():
    cmd = 'lsdev -Cc processor'
    p = subprocess.Popen(cmd, shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
    stdout, stderr = p.communicate()
    if PY3:
        stdout, stderr = [x.decodesys.stdout.encoding for x in (stdout, stderr)]
    if p.returncode != 0:
        raise RuntimeError('%r command error\n%s' % (cmd, stderr))
    processors = stdout.strip().splitlines()
    return len(processors) or None


def cpu_stats():
    """Return various CPU stats as a named tuple."""
    ctx_switches, interrupts, soft_interrupts, syscalls = cext.cpu_stats()
    return _common.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


disk_io_counters = cext.disk_io_counters
disk_usage = _psposix.disk_usage

def disk_partitions(all=False):
    """Return system disk partitions."""
    retlist = []
    partitions = cext.disk_partitions()
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        if device == 'none':
            device = ''
        if not (all or disk_usage(mountpoint).total):
            pass
        else:
            maxfile = maxpath = None
            ntuple = _common.sdiskpart(device, mountpoint, fstype, opts, maxfile, maxpath)
            retlist.appendntuple
    else:
        return retlist


net_if_addrs = cext_posix.net_if_addrs
if HAS_NET_IO_COUNTERS:
    net_io_counters = cext.net_io_counters

def net_connections(kind, _pid=-1):
    """Return socket connections.  If pid == -1 return system-wide
    connections (as opposed to connections opened by one process only).
    """
    cmap = _common.conn_tmap
    if kind not in cmap:
        raise ValueError('invalid %r kind argument; choose between %s' % (
         kind, ', '.join[repr(x) for x in cmap]))
    families, types = _common.conn_tmap[kind]
    rawlist = cext.net_connections_pid
    ret = []
    for item in rawlist:
        fd, fam, type_, laddr, raddr, status, pid = item
        if fam not in families:
            pass
        elif type_ not in types:
            pass
        else:
            nt = conn_to_ntuple(fd, fam, type_, laddr, raddr, status, TCP_STATUSES,
              pid=(pid if _pid == -1 else None))
            ret.appendnt
    else:
        return ret


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    duplex_map = {'Full':NIC_DUPLEX_FULL, 
     'Half':NIC_DUPLEX_HALF}
    names = set([x[0] for x in net_if_addrs()])
    ret = {}
    for name in names:
        isup, mtu = cext.net_if_statsname
        duplex = ''
        speed = 0
        p = subprocess.Popen(['/usr/bin/entstat', '-d', name], stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        stdout, stderr = p.communicate()
        if PY3:
            stdout, stderr = [x.decodesys.stdout.encoding for x in (stdout, stderr)]
        if p.returncode == 0:
            re_result = re.search('Running: (\\d+) Mbps.*?(\\w+) Duplex', stdout)
            if re_result is not None:
                speed = int(re_result.group1)
                duplex = re_result.group2
        duplex = duplex_map.get(duplex, NIC_DUPLEX_UNKNOWN)
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
    localhost = (':0.0', ':0')
    for item in rawlist:
        user, tty, hostname, tstamp, user_process, pid = item
        if not user_process:
            pass
        else:
            if hostname in localhost:
                hostname = 'localhost'
            nt = _common.suser(user, tty, hostname, tstamp, pid)
            retlist.appendnt
    else:
        return retlist


def pids():
    """Returns a list of PIDs currently running on the system."""
    return [int(x) for x in os.listdirget_procfs_path() if x.isdigit()]


def pid_exists(pid):
    """Check for the existence of a unix pid."""
    return os.path.existsos.path.join(get_procfs_path(), str(pid), 'psinfo')


def wrap_exceptions(fun):
    """Call callable into a try/except clause and translate ENOENT,
    EACCES and EPERM in NoSuchProcess or AccessDenied exceptions.
    """

    @functools.wrapsfun
    def wrapper--- This code section failed: ---

 L. 315         0  SETUP_FINALLY        20  'to 20'

 L. 316         2  LOAD_DEREF               'fun'
                4  LOAD_FAST                'self'
                6  BUILD_TUPLE_1         1 
                8  LOAD_FAST                'args'
               10  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               12  LOAD_FAST                'kwargs'
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 317        20  DUP_TOP          
               22  LOAD_GLOBAL              FileNotFoundError
               24  LOAD_GLOBAL              ProcessLookupError
               26  BUILD_TUPLE_2         2 
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    86  'to 86'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 321        38  LOAD_GLOBAL              pid_exists
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                pid
               44  CALL_FUNCTION_1       1  ''
               46  POP_JUMP_IF_TRUE     64  'to 64'

 L. 322        48  LOAD_GLOBAL              NoSuchProcess
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                pid
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _name
               58  CALL_FUNCTION_2       2  ''
               60  RAISE_VARARGS_1       1  'exception instance'
               62  JUMP_FORWARD         82  'to 82'
             64_0  COME_FROM            46  '46'

 L. 324        64  LOAD_GLOBAL              ZombieProcess
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                pid
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _name
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _ppid
               78  CALL_FUNCTION_3       3  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            62  '62'
               82  POP_EXCEPT       
               84  JUMP_FORWARD        120  'to 120'
             86_0  COME_FROM            30  '30'

 L. 325        86  DUP_TOP          
               88  LOAD_GLOBAL              PermissionError
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   118  'to 118'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 326       100  LOAD_GLOBAL              AccessDenied
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                pid
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _name
              110  CALL_FUNCTION_2       2  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            92  '92'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            84  '84'

Parse error at or near `POP_TOP' instruction at offset 34

    return wrapper


class Process(object):
    __doc__ = 'Wrapper class around underlying C implementation.'
    __slots__ = [
     'pid', '_name', '_ppid', '_procfs_path', '_cache']

    def __init__(self, pid):
        self.pid = pid
        self._name = None
        self._ppid = None
        self._procfs_path = get_procfs_path()

    def oneshot_enter(self):
        self._proc_basic_info.cache_activateself
        self._proc_cred.cache_activateself

    def oneshot_exit(self):
        self._proc_basic_info.cache_deactivateself
        self._proc_cred.cache_deactivateself

    @wrap_exceptions
    @memoize_when_activated
    def _proc_basic_info(self):
        return cext.proc_basic_info(self.pid, self._procfs_path)

    @wrap_exceptions
    @memoize_when_activated
    def _proc_cred(self):
        return cext.proc_cred(self.pid, self._procfs_path)

    @wrap_exceptions
    def name(self):
        if self.pid == 0:
            return 'swapper'
        return cext.proc_name(self.pid, self._procfs_path).rstrip'\x00'

    @wrap_exceptions
    def exe(self):
        cmdline = self.cmdline()
        if not cmdline:
            return ''
        exe = cmdline[0]
        if os.path.sep in exe:
            if not os.path.isabsexe:
                exe = os.path.abspathos.path.join(self.cwd(), exe)
            if os.path.isabsexe:
                if os.path.isfileexe:
                    if os.access(exe, os.X_OK):
                        return exe
            exe = os.path.basenameexe
        for path in os.environ['PATH'].split':':
            possible_exe = os.path.abspathos.path.join(path, exe)
            if os.path.isfilepossible_exe and os.access(possible_exe, os.X_OK):
                return possible_exe
            return ''

    @wrap_exceptions
    def cmdline(self):
        return cext.proc_argsself.pid

    @wrap_exceptions
    def environ(self):
        return cext.proc_environself.pid

    @wrap_exceptions
    def create_time(self):
        return self._proc_basic_info()[proc_info_map['create_time']]

    @wrap_exceptions
    def num_threads(self):
        return self._proc_basic_info()[proc_info_map['num_threads']]

    if HAS_THREADS:

        @wrap_exceptions
        def threads(self):
            rawlist = cext.proc_threadsself.pid
            retlist = []
            for thread_id, utime, stime in rawlist:
                ntuple = _common.pthread(thread_id, utime, stime)
                retlist.appendntuple
            else:
                if not retlist:
                    os.stat('%s/%s' % (self._procfs_path, self.pid))
                return retlist

    @wrap_exceptions
    def connections(self, kind='inet'):
        ret = net_connections(kind, _pid=(self.pid))
        if not ret:
            os.stat('%s/%s' % (self._procfs_path, self.pid))
        return ret

    @wrap_exceptions
    def nice_get(self):
        return cext_posix.getpriorityself.pid

    @wrap_exceptions
    def nice_set(self, value):
        return cext_posix.setpriority(self.pid, value)

    @wrap_exceptions
    def ppid(self):
        self._ppid = self._proc_basic_info()[proc_info_map['ppid']]
        return self._ppid

    @wrap_exceptions
    def uids(self):
        real, effective, saved, _, _, _ = self._proc_cred()
        return _common.puids(real, effective, saved)

    @wrap_exceptions
    def gids(self):
        _, _, _, real, effective, saved = self._proc_cred()
        return _common.puids(real, effective, saved)

    @wrap_exceptions
    def cpu_times(self):
        cpu_times = cext.proc_cpu_times(self.pid, self._procfs_path)
        return (_common.pcputimes)(*cpu_times)

    @wrap_exceptions
    def terminal(self):
        ttydev = self._proc_basic_info()[proc_info_map['ttynr']]
        ttydev = (ttydev & 281470681743360) >> 16 | ttydev & 65535
        for dev in glob.glob'/dev/**/*':
            if os.statdev.st_rdev == ttydev:
                return dev

    @wrap_exceptions
    def cwd--- This code section failed: ---

 L. 481         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _procfs_path
                4  STORE_FAST               'procfs_path'

 L. 482         6  SETUP_FINALLY        40  'to 40'

 L. 483         8  LOAD_GLOBAL              os
               10  LOAD_METHOD              readlink
               12  LOAD_STR                 '%s/%s/cwd'
               14  LOAD_FAST                'procfs_path'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                pid
               20  BUILD_TUPLE_2         2 
               22  BINARY_MODULO    
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'result'

 L. 484        28  LOAD_FAST                'result'
               30  LOAD_METHOD              rstrip
               32  LOAD_STR                 '/'
               34  CALL_METHOD_1         1  ''
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY     6  '6'

 L. 485        40  DUP_TOP          
               42  LOAD_GLOBAL              FileNotFoundError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    80  'to 80'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 486        54  LOAD_GLOBAL              os
               56  LOAD_METHOD              stat
               58  LOAD_STR                 '%s/%s'
               60  LOAD_FAST                'procfs_path'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                pid
               66  BUILD_TUPLE_2         2 
               68  BINARY_MODULO    
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          

 L. 487        74  POP_EXCEPT       
               76  LOAD_CONST               None
               78  RETURN_VALUE     
             80_0  COME_FROM            46  '46'
               80  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 50

    @wrap_exceptions
    def memory_info(self):
        ret = self._proc_basic_info()
        rss = ret[proc_info_map['rss']] * 1024
        vms = ret[proc_info_map['vms']] * 1024
        return pmem(rss, vms)

    memory_full_info = memory_info

    @wrap_exceptions
    def status(self):
        code = self._proc_basic_info()[proc_info_map['status']]
        return PROC_STATUSES.get(code, '?')

    def open_files(self):
        p = subprocess.Popen(['/usr/bin/procfiles', '-n', str(self.pid)], stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        stdout, stderr = p.communicate()
        if PY3:
            stdout, stderr = [x.decodesys.stdout.encoding for x in (stdout, stderr)]
        if 'no such process' in stderr.lower():
            raise NoSuchProcess(self.pid, self._name)
        procfiles = re.findall('(\\d+): S_IFREG.*\\s*.*name:(.*)\\n', stdout)
        retlist = []
        for fd, path in procfiles:
            path = path.strip()
            if path.startswith'//':
                path = path[1:]
            if path.lower() == 'cannot be retrieved':
                pass
            else:
                retlist.append_common.popenfile(path, int(fd))
        else:
            return retlist

    @wrap_exceptions
    def num_fds(self):
        if self.pid == 0:
            return 0
        return len(os.listdir('%s/%s/fd' % (self._procfs_path, self.pid)))

    @wrap_exceptions
    def num_ctx_switches(self):
        return (_common.pctxsw)(*cext.proc_num_ctx_switchesself.pid)

    @wrap_exceptions
    def wait(self, timeout=None):
        return _psposix.wait_pid(self.pid, timeout, self._name)

    if HAS_PROC_IO_COUNTERS:

        @wrap_exceptions
        def io_counters(self):
            try:
                rc, wc, rb, wb = cext.proc_io_countersself.pid
            except OSError:
                if not pid_exists(self.pid):
                    raise NoSuchProcess(self.pid, self._name)
                raise
            else:
                return _common.pio(rc, wc, rb, wb)