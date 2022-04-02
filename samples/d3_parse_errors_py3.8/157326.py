# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\psutil\_pssunos.py
"""Sun OS Solaris platform implementation."""
import errno, functools, os, socket, subprocess, sys
from collections import namedtuple
from socket import AF_INET
from . import _common
from . import _psposix
from . import _psutil_posix as cext_posix
from . import _psutil_sunos as cext
from ._common import AccessDenied
from ._common import AF_INET6
from ._common import debug
from ._common import get_procfs_path
from ._common import isfile_strict
from ._common import memoize_when_activated
from ._common import NoSuchProcess
from ._common import sockfam_to_enum
from ._common import socktype_to_enum
from ._common import usage_percent
from ._common import ZombieProcess
from ._compat import b
from ._compat import FileNotFoundError
from ._compat import PermissionError
from ._compat import ProcessLookupError
from ._compat import PY3
__extra__all__ = [
 'CONN_IDLE', 'CONN_BOUND', 'PROCFS_PATH']
PAGE_SIZE = cext_posix.getpagesize()
AF_LINK = cext_posix.AF_LINK
IS_64_BIT = sys.maxsize > 4294967296
CONN_IDLE = 'IDLE'
CONN_BOUND = 'BOUND'
PROC_STATUSES = {cext.SSLEEP: _common.STATUS_SLEEPING, 
 cext.SRUN: _common.STATUS_RUNNING, 
 cext.SZOMB: _common.STATUS_ZOMBIE, 
 cext.SSTOP: _common.STATUS_STOPPED, 
 cext.SIDL: _common.STATUS_IDLE, 
 cext.SONPROC: _common.STATUS_RUNNING, 
 cext.SWAIT: _common.STATUS_WAITING}
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
 cext.PSUTIL_CONN_NONE: _common.CONN_NONE, 
 cext.TCPS_IDLE: CONN_IDLE, 
 cext.TCPS_BOUND: CONN_BOUND}
proc_info_map = dict(ppid=0,
  rss=1,
  vms=2,
  create_time=3,
  nice=4,
  num_threads=5,
  status=6,
  ttynr=7,
  uid=8,
  euid=9,
  gid=10,
  egid=11)
scputimes = namedtuple('scputimes', ['user', 'system', 'idle', 'iowait'])
pcputimes = namedtuple('pcputimes', [
 'user', 'system', 'children_user', 'children_system'])
svmem = namedtuple('svmem', ['total', 'available', 'percent', 'used', 'free'])
pmem = namedtuple('pmem', ['rss', 'vms'])
pfullmem = pmem
pmmap_grouped = namedtuple('pmmap_grouped', [
 'path', 'rss', 'anonymous', 'locked'])
pmmap_ext = namedtuple('pmmap_ext', 'addr perms ' + ' '.join(pmmap_grouped._fields))

def virtual_memory():
    """Report virtual memory metrics."""
    total = os.sysconf('SC_PHYS_PAGES') * PAGE_SIZE
    free = avail = os.sysconf('SC_AVPHYS_PAGES') * PAGE_SIZE
    used = total - free
    percent = usage_percent(used, total, round_=1)
    return svmem(total, avail, percent, used, free)


def swap_memory():
    """Report swap memory metrics."""
    sin, sout = cext.swap_mem()
    p = subprocess.Popen(['/usr/bin/env',
     'PATH=/usr/sbin:/sbin:%s' % os.environ['PATH'], 'swap', '-l'],
      stdout=(subprocess.PIPE))
    stdout, stderr = p.communicate()
    if PY3:
        stdout = stdout.decode(sys.stdout.encoding)
    if p.returncode != 0:
        raise RuntimeError("'swap -l' failed (retcode=%s)" % p.returncode)
    lines = stdout.strip().split('\n')[1:]
    if not lines:
        raise RuntimeError('no swap device(s) configured')
    total = free = 0
    for line in lines:
        line = line.split()
        t, f = line[3:4]
        total += int(int(t) * 512)
        free += int(int(f) * 512)
    else:
        used = total - free
        percent = usage_percent(used, total, round_=1)
        return _common.sswap(total, used, free, percent, sin * PAGE_SIZE, sout * PAGE_SIZE)


def cpu_times():
    """Return system-wide CPU times as a named tuple"""
    ret = cext.per_cpu_times()
    return scputimes(*[sum(x) for x in zip(*ret)])


def per_cpu_times():
    """Return system per-CPU times as a list of named tuples"""
    ret = cext.per_cpu_times()
    return [scputimes(*x) for x in ret]


def cpu_count_logical--- This code section failed: ---

 L. 186         0  SETUP_FINALLY        14  'to 14'

 L. 187         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              sysconf
                6  LOAD_STR                 'SC_NPROCESSORS_ONLN'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 188        14  DUP_TOP          
               16  LOAD_GLOBAL              ValueError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 190        28  POP_EXCEPT       
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'
               34  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 30


def cpu_count_physical():
    """Return the number of physical CPUs in the system."""
    return cext.cpu_count_phys()


def cpu_stats():
    """Return various CPU stats as a named tuple."""
    ctx_switches, interrupts, syscalls, traps = cext.cpu_stats()
    soft_interrupts = 0
    return _common.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


disk_io_counters = cext.disk_io_counters
disk_usage = _psposix.disk_usage

def disk_partitions--- This code section failed: ---

 L. 219         0  BUILD_LIST_0          0 
                2  STORE_FAST               'retlist'

 L. 220         4  LOAD_GLOBAL              cext
                6  LOAD_METHOD              disk_partitions
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'partitions'

 L. 221        12  LOAD_FAST                'partitions'
               14  GET_ITER         
             16_0  COME_FROM           164  '164'
             16_1  COME_FROM           106  '106'
             16_2  COME_FROM            62  '62'
               16  FOR_ITER            166  'to 166'
               18  STORE_FAST               'partition'

 L. 222        20  LOAD_FAST                'partition'
               22  UNPACK_SEQUENCE_4     4 
               24  STORE_FAST               'device'
               26  STORE_FAST               'mountpoint'
               28  STORE_FAST               'fstype'
               30  STORE_FAST               'opts'

 L. 223        32  LOAD_FAST                'device'
               34  LOAD_STR                 'none'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L. 224        40  LOAD_STR                 ''
               42  STORE_FAST               'device'
             44_0  COME_FROM            38  '38'

 L. 225        44  LOAD_FAST                'all'
               46  POP_JUMP_IF_TRUE    126  'to 126'

 L. 229        48  SETUP_FINALLY        68  'to 68'

 L. 230        50  LOAD_GLOBAL              disk_usage
               52  LOAD_FAST                'mountpoint'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_ATTR                total
               58  POP_JUMP_IF_TRUE     64  'to 64'

 L. 231        60  POP_BLOCK        
               62  JUMP_BACK            16  'to 16'
             64_0  COME_FROM            58  '58'
               64  POP_BLOCK        
               66  JUMP_FORWARD        126  'to 126'
             68_0  COME_FROM_FINALLY    48  '48'

 L. 232        68  DUP_TOP          
               70  LOAD_GLOBAL              OSError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   124  'to 124'
               76  POP_TOP          
               78  STORE_FAST               'err'
               80  POP_TOP          
               82  SETUP_FINALLY       112  'to 112'

 L. 234        84  LOAD_GLOBAL              debug
               86  LOAD_STR                 'skipping %r: %r'
               88  LOAD_FAST                'mountpoint'
               90  LOAD_FAST                'err'
               92  BUILD_TUPLE_2         2 
               94  BINARY_MODULO    
               96  CALL_FUNCTION_1       1  ''
               98  POP_TOP          

 L. 235       100  POP_BLOCK        
              102  POP_EXCEPT       
              104  CALL_FINALLY        112  'to 112'
              106  JUMP_BACK            16  'to 16'
              108  POP_BLOCK        
              110  BEGIN_FINALLY    
            112_0  COME_FROM           104  '104'
            112_1  COME_FROM_FINALLY    82  '82'
              112  LOAD_CONST               None
              114  STORE_FAST               'err'
              116  DELETE_FAST              'err'
              118  END_FINALLY      
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM            74  '74'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM            66  '66'
            126_2  COME_FROM            46  '46'

 L. 236       126  LOAD_CONST               None
              128  DUP_TOP          
              130  STORE_FAST               'maxfile'
              132  STORE_FAST               'maxpath'

 L. 237       134  LOAD_GLOBAL              _common
              136  LOAD_METHOD              sdiskpart
              138  LOAD_FAST                'device'
              140  LOAD_FAST                'mountpoint'
              142  LOAD_FAST                'fstype'
              144  LOAD_FAST                'opts'

 L. 238       146  LOAD_FAST                'maxfile'

 L. 238       148  LOAD_FAST                'maxpath'

 L. 237       150  CALL_METHOD_6         6  ''
              152  STORE_FAST               'ntuple'

 L. 239       154  LOAD_FAST                'retlist'
              156  LOAD_METHOD              append
              158  LOAD_FAST                'ntuple'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  JUMP_BACK            16  'to 16'
            166_0  COME_FROM            16  '16'

 L. 240       166  LOAD_FAST                'retlist'
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 62


net_io_counters = cext.net_io_counters
net_if_addrs = cext_posix.net_if_addrs

def net_connections(kind, _pid=-1):
    """Return socket connections.  If pid == -1 return system-wide
    connections (as opposed to connections opened by one process only).
    Only INET sockets are returned (UNIX are not).
    """
    cmap = _common.conn_tmap.copy()
    if _pid == -1:
        cmap.pop('unix', 0)
    if kind not in cmap:
        raise ValueError('invalid %r kind argument; choose between %s' % (
         kind, ', '.join([repr(x) for x in cmap])))
    families, types = _common.conn_tmap[kind]
    rawlist = cext.net_connections(_pid)
    ret = set()
    for item in rawlist:
        fd, fam, type_, laddr, raddr, status, pid = item
        if fam not in families:
            pass
        else:
            if type_ not in types:
                pass
            else:
                if fam in (AF_INET, AF_INET6):
                    if laddr:
                        laddr = (_common.addr)(*laddr)
                    if raddr:
                        raddr = (_common.addr)(*raddr)
                status = TCP_STATUSES[status]
                fam = sockfam_to_enum(fam)
                type_ = socktype_to_enum(type_)
                if _pid == -1:
                    nt = _common.sconn(fd, fam, type_, laddr, raddr, status, pid)
                else:
                    nt = _common.pconn(fd, fam, type_, laddr, raddr, status)
                ret.add(nt)
    else:
        return list(ret)


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    ret = cext.net_if_stats()
    for name, items in ret.items():
        isup, duplex, speed, mtu = items
        if hasattr(_common, 'NicDuplex'):
            duplex = _common.NicDuplex(duplex)
        else:
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
            retlist.append(nt)
    else:
        return retlist


def pids():
    """Returns a list of PIDs currently running on the system."""
    return [int(x) for x in os.listdir(b(get_procfs_path())) if x.isdigit()]


def pid_exists(pid):
    """Check for the existence of a unix pid."""
    return _psposix.pid_exists(pid)


def wrap_exceptions(fun):
    """Call callable into a try/except clause and translate ENOENT,
    EACCES and EPERM in NoSuchProcess or AccessDenied exceptions.
    """

    @functools.wraps(fun)
    def wrapper--- This code section failed: ---

 L. 350         0  SETUP_FINALLY        20  'to 20'

 L. 351         2  LOAD_DEREF               'fun'
                4  LOAD_FAST                'self'
                6  BUILD_TUPLE_1         1 
                8  LOAD_FAST                'args'
               10  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               12  LOAD_FAST                'kwargs'
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 352        20  DUP_TOP          
               22  LOAD_GLOBAL              FileNotFoundError
               24  LOAD_GLOBAL              ProcessLookupError
               26  BUILD_TUPLE_2         2 
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    86  'to 86'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 356        38  LOAD_GLOBAL              pid_exists
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                pid
               44  CALL_FUNCTION_1       1  ''
               46  POP_JUMP_IF_TRUE     64  'to 64'

 L. 357        48  LOAD_GLOBAL              NoSuchProcess
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                pid
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _name
               58  CALL_FUNCTION_2       2  ''
               60  RAISE_VARARGS_1       1  'exception instance'
               62  JUMP_FORWARD         82  'to 82'
             64_0  COME_FROM            46  '46'

 L. 359        64  LOAD_GLOBAL              ZombieProcess
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
               84  JUMP_FORWARD        178  'to 178'
             86_0  COME_FROM            30  '30'

 L. 360        86  DUP_TOP          
               88  LOAD_GLOBAL              PermissionError
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   118  'to 118'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 361       100  LOAD_GLOBAL              AccessDenied
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                pid
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _name
              110  CALL_FUNCTION_2       2  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        178  'to 178'
            118_0  COME_FROM            92  '92'

 L. 362       118  DUP_TOP          
              120  LOAD_GLOBAL              OSError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   176  'to 176'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 363       132  LOAD_FAST                'self'
              134  LOAD_ATTR                pid
              136  LOAD_CONST               0
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   170  'to 170'

 L. 364       142  LOAD_CONST               0
              144  LOAD_GLOBAL              pids
              146  CALL_FUNCTION_0       0  ''
              148  COMPARE_OP               in
              150  POP_JUMP_IF_FALSE   168  'to 168'

 L. 365       152  LOAD_GLOBAL              AccessDenied
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                pid
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                _name
              162  CALL_FUNCTION_2       2  ''
              164  RAISE_VARARGS_1       1  'exception instance'
              166  JUMP_FORWARD        170  'to 170'
            168_0  COME_FROM           150  '150'

 L. 367       168  RAISE_VARARGS_0       0  'reraise'
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           140  '140'

 L. 368       170  RAISE_VARARGS_0       0  'reraise'
              172  POP_EXCEPT       
              174  JUMP_FORWARD        178  'to 178'
            176_0  COME_FROM           124  '124'
              176  END_FINALLY      
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           116  '116'
            178_2  COME_FROM            84  '84'

Parse error at or near `DUP_TOP' instruction at offset 86

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

    def _assert_alive(self):
        """Raise NSP if the process disappeared on us."""
        os.stat('%s/%s' % (self._procfs_path, self.pid))

    def oneshot_enter(self):
        self._proc_name_and_args.cache_activate(self)
        self._proc_basic_info.cache_activate(self)
        self._proc_cred.cache_activate(self)

    def oneshot_exit(self):
        self._proc_name_and_args.cache_deactivate(self)
        self._proc_basic_info.cache_deactivate(self)
        self._proc_cred.cache_deactivate(self)

    @wrap_exceptions
    @memoize_when_activated
    def _proc_name_and_args(self):
        return cext.proc_name_and_args(self.pid, self._procfs_path)

    @wrap_exceptions
    @memoize_when_activated
    def _proc_basic_info(self):
        if self.pid == 0:
            if not os.path.exists('%s/%s/psinfo' % (self._procfs_path, self.pid)):
                raise AccessDenied(self.pid)
            ret = cext.proc_basic_info(self.pid, self._procfs_path)
            assert len(ret) == len(proc_info_map)
            return ret

    @wrap_exceptions
    @memoize_when_activated
    def _proc_cred(self):
        return cext.proc_cred(self.pid, self._procfs_path)

    @wrap_exceptions
    def name(self):
        return self._proc_name_and_args()[0]

    @wrap_exceptions
    def exe--- This code section failed: ---

 L. 426         0  SETUP_FINALLY        26  'to 26'

 L. 427         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              readlink

 L. 428         6  LOAD_STR                 '%s/%s/path/a.out'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _procfs_path
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                pid
               16  BUILD_TUPLE_2         2 
               18  BINARY_MODULO    

 L. 427        20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY     0  '0'

 L. 429        26  DUP_TOP          
               28  LOAD_GLOBAL              OSError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 430        40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

 L. 434        46  LOAD_FAST                'self'
               48  LOAD_METHOD              cmdline
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L. 435        54  LOAD_STR                 ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 44_0

    @wrap_exceptions
    def cmdline(self):
        return self._proc_name_and_args()[1].split(' ')

    @wrap_exceptions
    def environ(self):
        return cext.proc_environ(self.pid, self._procfs_path)

    @wrap_exceptions
    def create_time(self):
        return self._proc_basic_info()[proc_info_map['create_time']]

    @wrap_exceptions
    def num_threads(self):
        return self._proc_basic_info()[proc_info_map['num_threads']]

    @wrap_exceptions
    def nice_get(self):
        return self._proc_basic_info()[proc_info_map['nice']]

    @wrap_exceptions
    def nice_set(self, value):
        if self.pid in (2, 3):
            raise AccessDenied(self.pid, self._name)
        return cext_posix.setpriority(self.pid, value)

    @wrap_exceptions
    def ppid(self):
        self._ppid = self._proc_basic_info()[proc_info_map['ppid']]
        return self._ppid

    @wrap_exceptions
    def uids(self):
        try:
            real, effective, saved, _, _, _ = self._proc_cred()
        except AccessDenied:
            real = self._proc_basic_info()[proc_info_map['uid']]
            effective = self._proc_basic_info()[proc_info_map['euid']]
            saved = None
        else:
            return _common.puids(real, effective, saved)

    @wrap_exceptions
    def gids(self):
        try:
            _, _, _, real, effective, saved = self._proc_cred()
        except AccessDenied:
            real = self._proc_basic_info()[proc_info_map['gid']]
            effective = self._proc_basic_info()[proc_info_map['egid']]
            saved = None
        else:
            return _common.puids(real, effective, saved)

    @wrap_exceptions
    def cpu_times(self):
        try:
            times = cext.proc_cpu_times(self.pid, self._procfs_path)
        except OSError as err:
            try:
                if err.errno == errno.EOVERFLOW and not IS_64_BIT:
                    times = (0.0, 0.0, 0.0, 0.0)
                else:
                    raise
            finally:
                err = None
                del err

        else:
            return (_common.pcputimes)(*times)

    @wrap_exceptions
    def cpu_num(self):
        return cext.proc_cpu_num(self.pid, self._procfs_path)

    @wrap_exceptions
    def terminal--- This code section failed: ---

 L. 519         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _procfs_path
                4  STORE_FAST               'procfs_path'

 L. 520         6  LOAD_CONST               False
                8  STORE_FAST               'hit_enoent'

 L. 521        10  LOAD_GLOBAL              wrap_exceptions

 L. 522        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _proc_basic_info
               16  CALL_METHOD_0         0  ''
               18  LOAD_GLOBAL              proc_info_map
               20  LOAD_STR                 'ttynr'
               22  BINARY_SUBSCR    
               24  BINARY_SUBSCR    

 L. 521        26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'tty'

 L. 523        30  LOAD_FAST                'tty'
               32  LOAD_GLOBAL              cext
               34  LOAD_ATTR                PRNODEV
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE   108  'to 108'

 L. 524        40  LOAD_CONST               (0, 1, 2, 255)
               42  GET_ITER         
             44_0  COME_FROM           106  '106'
             44_1  COME_FROM           102  '102'
             44_2  COME_FROM            98  '98'
               44  FOR_ITER            108  'to 108'
               46  STORE_FAST               'x'

 L. 525        48  SETUP_FINALLY        78  'to 78'

 L. 526        50  LOAD_GLOBAL              os
               52  LOAD_METHOD              readlink

 L. 527        54  LOAD_STR                 '%s/%d/path/%d'
               56  LOAD_FAST                'procfs_path'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                pid
               62  LOAD_FAST                'x'
               64  BUILD_TUPLE_3         3 
               66  BINARY_MODULO    

 L. 526        68  CALL_METHOD_1         1  ''
               70  POP_BLOCK        
               72  ROT_TWO          
               74  POP_TOP          
               76  RETURN_VALUE     
             78_0  COME_FROM_FINALLY    48  '48'

 L. 528        78  DUP_TOP          
               80  LOAD_GLOBAL              FileNotFoundError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   104  'to 104'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 529        92  LOAD_CONST               True
               94  STORE_FAST               'hit_enoent'

 L. 530        96  POP_EXCEPT       
               98  JUMP_BACK            44  'to 44'
              100  POP_EXCEPT       
              102  JUMP_BACK            44  'to 44'
            104_0  COME_FROM            84  '84'
              104  END_FINALLY      
              106  JUMP_BACK            44  'to 44'
            108_0  COME_FROM            44  '44'
            108_1  COME_FROM            38  '38'

 L. 531       108  LOAD_FAST                'hit_enoent'
              110  POP_JUMP_IF_FALSE   120  'to 120'

 L. 532       112  LOAD_FAST                'self'
              114  LOAD_METHOD              _assert_alive
              116  CALL_METHOD_0         0  ''
              118  POP_TOP          
            120_0  COME_FROM           110  '110'

Parse error at or near `ROT_TWO' instruction at offset 72

    @wrap_exceptions
    def cwd--- This code section failed: ---

 L. 540         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _procfs_path
                4  STORE_FAST               'procfs_path'

 L. 541         6  SETUP_FINALLY        30  'to 30'

 L. 542         8  LOAD_GLOBAL              os
               10  LOAD_METHOD              readlink
               12  LOAD_STR                 '%s/%s/path/cwd'
               14  LOAD_FAST                'procfs_path'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                pid
               20  BUILD_TUPLE_2         2 
               22  BINARY_MODULO    
               24  CALL_METHOD_1         1  ''
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY     6  '6'

 L. 543        30  DUP_TOP          
               32  LOAD_GLOBAL              FileNotFoundError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    70  'to 70'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 544        44  LOAD_GLOBAL              os
               46  LOAD_METHOD              stat
               48  LOAD_STR                 '%s/%s'
               50  LOAD_FAST                'procfs_path'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                pid
               56  BUILD_TUPLE_2         2 
               58  BINARY_MODULO    
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 545        64  POP_EXCEPT       
               66  LOAD_CONST               None
               68  RETURN_VALUE     
             70_0  COME_FROM            36  '36'
               70  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 66

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

    @wrap_exceptions
    def threads--- This code section failed: ---

 L. 564         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _procfs_path
                4  STORE_FAST               'procfs_path'

 L. 565         6  BUILD_LIST_0          0 
                8  STORE_FAST               'ret'

 L. 566        10  LOAD_GLOBAL              os
               12  LOAD_METHOD              listdir
               14  LOAD_STR                 '%s/%d/lwp'
               16  LOAD_FAST                'procfs_path'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                pid
               22  BUILD_TUPLE_2         2 
               24  BINARY_MODULO    
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'tids'

 L. 567        30  LOAD_CONST               False
               32  STORE_FAST               'hit_enoent'

 L. 568        34  LOAD_FAST                'tids'
               36  GET_ITER         
             38_0  COME_FROM           184  '184'
             38_1  COME_FROM           156  '156'
             38_2  COME_FROM           138  '138'
             38_3  COME_FROM           114  '114'
               38  FOR_ITER            186  'to 186'
               40  STORE_FAST               'tid'

 L. 569        42  LOAD_GLOBAL              int
               44  LOAD_FAST                'tid'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'tid'

 L. 570        50  SETUP_FINALLY        76  'to 76'

 L. 571        52  LOAD_GLOBAL              cext
               54  LOAD_METHOD              query_process_thread

 L. 572        56  LOAD_FAST                'self'
               58  LOAD_ATTR                pid

 L. 572        60  LOAD_FAST                'tid'

 L. 572        62  LOAD_FAST                'procfs_path'

 L. 571        64  CALL_METHOD_3         3  ''
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'utime'
               70  STORE_FAST               'stime'
               72  POP_BLOCK        
               74  JUMP_FORWARD        160  'to 160'
             76_0  COME_FROM_FINALLY    50  '50'

 L. 573        76  DUP_TOP          
               78  LOAD_GLOBAL              EnvironmentError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   158  'to 158'
               84  POP_TOP          
               86  STORE_FAST               'err'
               88  POP_TOP          
               90  SETUP_FINALLY       146  'to 146'

 L. 574        92  LOAD_FAST                'err'
               94  LOAD_ATTR                errno
               96  LOAD_GLOBAL              errno
               98  LOAD_ATTR                EOVERFLOW
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   116  'to 116'
              104  LOAD_GLOBAL              IS_64_BIT
              106  POP_JUMP_IF_TRUE    116  'to 116'

 L. 582       108  POP_BLOCK        
              110  POP_EXCEPT       
              112  CALL_FINALLY        146  'to 146'
              114  JUMP_BACK            38  'to 38'
            116_0  COME_FROM           106  '106'
            116_1  COME_FROM           102  '102'

 L. 584       116  LOAD_FAST                'err'
              118  LOAD_ATTR                errno
              120  LOAD_GLOBAL              errno
              122  LOAD_ATTR                ENOENT
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   140  'to 140'

 L. 585       128  LOAD_CONST               True
              130  STORE_FAST               'hit_enoent'

 L. 586       132  POP_BLOCK        
              134  POP_EXCEPT       
              136  CALL_FINALLY        146  'to 146'
              138  JUMP_BACK            38  'to 38'
            140_0  COME_FROM           126  '126'

 L. 587       140  RAISE_VARARGS_0       0  'reraise'
              142  POP_BLOCK        
              144  BEGIN_FINALLY    
            146_0  COME_FROM           136  '136'
            146_1  COME_FROM           112  '112'
            146_2  COME_FROM_FINALLY    90  '90'
              146  LOAD_CONST               None
              148  STORE_FAST               'err'
              150  DELETE_FAST              'err'
              152  END_FINALLY      
              154  POP_EXCEPT       
              156  JUMP_BACK            38  'to 38'
            158_0  COME_FROM            82  '82'
              158  END_FINALLY      
            160_0  COME_FROM            74  '74'

 L. 589       160  LOAD_GLOBAL              _common
              162  LOAD_METHOD              pthread
              164  LOAD_FAST                'tid'
              166  LOAD_FAST                'utime'
              168  LOAD_FAST                'stime'
              170  CALL_METHOD_3         3  ''
              172  STORE_FAST               'nt'

 L. 590       174  LOAD_FAST                'ret'
              176  LOAD_METHOD              append
              178  LOAD_FAST                'nt'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
              184  JUMP_BACK            38  'to 38'
            186_0  COME_FROM            38  '38'

 L. 591       186  LOAD_FAST                'hit_enoent'
              188  POP_JUMP_IF_FALSE   198  'to 198'

 L. 592       190  LOAD_FAST                'self'
              192  LOAD_METHOD              _assert_alive
              194  CALL_METHOD_0         0  ''
              196  POP_TOP          
            198_0  COME_FROM           188  '188'

 L. 593       198  LOAD_FAST                'ret'
              200  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 110

    @wrap_exceptions
    def open_files--- This code section failed: ---

 L. 597         0  BUILD_LIST_0          0 
                2  STORE_FAST               'retlist'

 L. 598         4  LOAD_CONST               False
                6  STORE_FAST               'hit_enoent'

 L. 599         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _procfs_path
               12  STORE_FAST               'procfs_path'

 L. 600        14  LOAD_STR                 '%s/%d/path'
               16  LOAD_FAST                'procfs_path'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                pid
               22  BUILD_TUPLE_2         2 
               24  BINARY_MODULO    
               26  STORE_FAST               'pathdir'

 L. 601        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              listdir
               32  LOAD_STR                 '%s/%d/fd'
               34  LOAD_FAST                'procfs_path'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                pid
               40  BUILD_TUPLE_2         2 
               42  BINARY_MODULO    
               44  CALL_METHOD_1         1  ''
               46  GET_ITER         
             48_0  COME_FROM           152  '152'
             48_1  COME_FROM           128  '128'
             48_2  COME_FROM           118  '118'
             48_3  COME_FROM           114  '114'
             48_4  COME_FROM            76  '76'
               48  FOR_ITER            154  'to 154'
               50  STORE_FAST               'fd'

 L. 602        52  LOAD_GLOBAL              os
               54  LOAD_ATTR                path
               56  LOAD_METHOD              join
               58  LOAD_FAST                'pathdir'
               60  LOAD_FAST                'fd'
               62  CALL_METHOD_2         2  ''
               64  STORE_FAST               'path'

 L. 603        66  LOAD_GLOBAL              os
               68  LOAD_ATTR                path
               70  LOAD_METHOD              islink
               72  LOAD_FAST                'path'
               74  CALL_METHOD_1         1  ''
               76  POP_JUMP_IF_FALSE_BACK    48  'to 48'

 L. 604        78  SETUP_FINALLY        94  'to 94'

 L. 605        80  LOAD_GLOBAL              os
               82  LOAD_METHOD              readlink
               84  LOAD_FAST                'path'
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'file'
               90  POP_BLOCK        
               92  JUMP_FORWARD        122  'to 122'
             94_0  COME_FROM_FINALLY    78  '78'

 L. 606        94  DUP_TOP          
               96  LOAD_GLOBAL              FileNotFoundError
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   120  'to 120'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L. 607       108  LOAD_CONST               True
              110  STORE_FAST               'hit_enoent'

 L. 608       112  POP_EXCEPT       
              114  JUMP_BACK            48  'to 48'
              116  POP_EXCEPT       
              118  JUMP_BACK            48  'to 48'
            120_0  COME_FROM           100  '100'
              120  END_FINALLY      
            122_0  COME_FROM            92  '92'

 L. 610       122  LOAD_GLOBAL              isfile_strict
              124  LOAD_FAST                'file'
              126  CALL_FUNCTION_1       1  ''
              128  POP_JUMP_IF_FALSE_BACK    48  'to 48'

 L. 611       130  LOAD_FAST                'retlist'
              132  LOAD_METHOD              append
              134  LOAD_GLOBAL              _common
              136  LOAD_METHOD              popenfile
              138  LOAD_FAST                'file'
              140  LOAD_GLOBAL              int
              142  LOAD_FAST                'fd'
              144  CALL_FUNCTION_1       1  ''
              146  CALL_METHOD_2         2  ''
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          
              152  JUMP_BACK            48  'to 48'
            154_0  COME_FROM            48  '48'

 L. 612       154  LOAD_FAST                'hit_enoent'
              156  POP_JUMP_IF_FALSE   166  'to 166'

 L. 613       158  LOAD_FAST                'self'
              160  LOAD_METHOD              _assert_alive
              162  CALL_METHOD_0         0  ''
              164  POP_TOP          
            166_0  COME_FROM           156  '156'

 L. 614       166  LOAD_FAST                'retlist'
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 118

    def _get_unix_sockets(self, pid):
        """Get UNIX sockets used by process by parsing 'pfiles' output."""
        cmd = 'pfiles %s' % pid
        p = subprocess.Popen(cmd, shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        stdout, stderr = p.communicate()
        if PY3:
            stdout, stderr = [x.decode(sys.stdout.encoding) for x in (stdout, stderr)]
        if p.returncode != 0:
            if 'permission denied' in stderr.lower():
                raise AccessDenied(self.pid, self._name)
            if 'no such process' in stderr.lower():
                raise NoSuchProcess(self.pid, self._name)
            raise RuntimeError('%r command error\n%s' % (cmd, stderr))
        lines = stdout.split('\n')[2:]
        for i, line in enumerate(lines):
            line = line.lstrip()
            if line.startswith('sockname: AF_UNIX'):
                path = line.split(' ', 2)[2]
                type = lines[(i - 2)].strip()
                if type == 'SOCK_STREAM':
                    type = socket.SOCK_STREAM
                elif type == 'SOCK_DGRAM':
                    type = socket.SOCK_DGRAM
                else:
                    type = -1
                yield (
                 -1, socket.AF_UNIX, type, path, '', _common.CONN_NONE)

    @wrap_exceptions
    def connections(self, kind='inet'):
        ret = net_connections(kind, _pid=(self.pid))
        if not ret:
            os.stat('%s/%s' % (self._procfs_path, self.pid))
        if kind in ('all', 'unix'):
            ret.extend([(_common.pconn)(*conn) for conn in self._get_unix_sockets(self.pid)])
        return ret

    nt_mmap_grouped = namedtuple('mmap', 'path rss anon locked')
    nt_mmap_ext = namedtuple('mmap', 'addr perms path rss anon locked')

    @wrap_exceptions
    def memory_maps--- This code section failed: ---

 L. 671         0  LOAD_CODE                <code_object toaddr>
                2  LOAD_STR                 'Process.memory_maps.<locals>.toaddr'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'toaddr'

 L. 675         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _procfs_path
               12  STORE_FAST               'procfs_path'

 L. 676        14  BUILD_LIST_0          0 
               16  STORE_FAST               'retlist'

 L. 677        18  SETUP_FINALLY        38  'to 38'

 L. 678        20  LOAD_GLOBAL              cext
               22  LOAD_METHOD              proc_memory_maps
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                pid
               28  LOAD_FAST                'procfs_path'
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'rawlist'
               34  POP_BLOCK        
               36  JUMP_FORWARD        102  'to 102'
             38_0  COME_FROM_FINALLY    18  '18'

 L. 679        38  DUP_TOP          
               40  LOAD_GLOBAL              OSError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE   100  'to 100'
               46  POP_TOP          
               48  STORE_FAST               'err'
               50  POP_TOP          
               52  SETUP_FINALLY        88  'to 88'

 L. 680        54  LOAD_FAST                'err'
               56  LOAD_ATTR                errno
               58  LOAD_GLOBAL              errno
               60  LOAD_ATTR                EOVERFLOW
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    82  'to 82'
               66  LOAD_GLOBAL              IS_64_BIT
               68  POP_JUMP_IF_TRUE     82  'to 82'

 L. 688        70  BUILD_LIST_0          0 
               72  ROT_FOUR         
               74  POP_BLOCK        
               76  POP_EXCEPT       
               78  CALL_FINALLY         88  'to 88'
               80  RETURN_VALUE     
             82_0  COME_FROM            68  '68'
             82_1  COME_FROM            64  '64'

 L. 690        82  RAISE_VARARGS_0       0  'reraise'
               84  POP_BLOCK        
               86  BEGIN_FINALLY    
             88_0  COME_FROM            78  '78'
             88_1  COME_FROM_FINALLY    52  '52'
               88  LOAD_CONST               None
               90  STORE_FAST               'err'
               92  DELETE_FAST              'err'
               94  END_FINALLY      
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            44  '44'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            36  '36'

 L. 691       102  LOAD_CONST               False
              104  STORE_FAST               'hit_enoent'

 L. 692       106  LOAD_FAST                'rawlist'
              108  GET_ITER         
            110_0  COME_FROM           272  '272'
              110  FOR_ITER            274  'to 274'
              112  STORE_FAST               'item'

 L. 693       114  LOAD_FAST                'item'
              116  UNPACK_SEQUENCE_7     7 
              118  STORE_FAST               'addr'
              120  STORE_FAST               'addrsize'
              122  STORE_FAST               'perm'
              124  STORE_FAST               'name'
              126  STORE_FAST               'rss'
              128  STORE_FAST               'anon'
              130  STORE_FAST               'locked'

 L. 694       132  LOAD_FAST                'toaddr'
              134  LOAD_FAST                'addr'
              136  LOAD_FAST                'addrsize'
              138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'addr'

 L. 695       142  LOAD_FAST                'name'
              144  LOAD_METHOD              startswith
              146  LOAD_STR                 '['
              148  CALL_METHOD_1         1  ''
              150  POP_JUMP_IF_TRUE    250  'to 250'

 L. 696       152  SETUP_FINALLY       180  'to 180'

 L. 697       154  LOAD_GLOBAL              os
              156  LOAD_METHOD              readlink

 L. 698       158  LOAD_STR                 '%s/%s/path/%s'
              160  LOAD_FAST                'procfs_path'
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                pid
              166  LOAD_FAST                'name'
              168  BUILD_TUPLE_3         3 
              170  BINARY_MODULO    

 L. 697       172  CALL_METHOD_1         1  ''
              174  STORE_FAST               'name'
              176  POP_BLOCK        
              178  JUMP_FORWARD        250  'to 250'
            180_0  COME_FROM_FINALLY   152  '152'

 L. 699       180  DUP_TOP          
              182  LOAD_GLOBAL              OSError
              184  COMPARE_OP               exception-match
              186  POP_JUMP_IF_FALSE   248  'to 248'
              188  POP_TOP          
              190  STORE_FAST               'err'
              192  POP_TOP          
              194  SETUP_FINALLY       236  'to 236'

 L. 700       196  LOAD_FAST                'err'
              198  LOAD_ATTR                errno
              200  LOAD_GLOBAL              errno
              202  LOAD_ATTR                ENOENT
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   230  'to 230'

 L. 707       208  LOAD_STR                 '%s/%s/path/%s'
              210  LOAD_FAST                'procfs_path'
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                pid
              216  LOAD_FAST                'name'
              218  BUILD_TUPLE_3         3 
              220  BINARY_MODULO    
              222  STORE_FAST               'name'

 L. 708       224  LOAD_CONST               True
              226  STORE_FAST               'hit_enoent'
              228  JUMP_FORWARD        232  'to 232'
            230_0  COME_FROM           206  '206'

 L. 710       230  RAISE_VARARGS_0       0  'reraise'
            232_0  COME_FROM           228  '228'
              232  POP_BLOCK        
              234  BEGIN_FINALLY    
            236_0  COME_FROM_FINALLY   194  '194'
              236  LOAD_CONST               None
              238  STORE_FAST               'err'
              240  DELETE_FAST              'err'
              242  END_FINALLY      
              244  POP_EXCEPT       
              246  JUMP_FORWARD        250  'to 250'
            248_0  COME_FROM           186  '186'
              248  END_FINALLY      
            250_0  COME_FROM           246  '246'
            250_1  COME_FROM           178  '178'
            250_2  COME_FROM           150  '150'

 L. 711       250  LOAD_FAST                'retlist'
              252  LOAD_METHOD              append
              254  LOAD_FAST                'addr'
              256  LOAD_FAST                'perm'
              258  LOAD_FAST                'name'
              260  LOAD_FAST                'rss'
              262  LOAD_FAST                'anon'
              264  LOAD_FAST                'locked'
              266  BUILD_TUPLE_6         6 
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          
              272  JUMP_BACK           110  'to 110'
            274_0  COME_FROM           110  '110'

 L. 712       274  LOAD_FAST                'hit_enoent'
          276_278  POP_JUMP_IF_FALSE   288  'to 288'

 L. 713       280  LOAD_FAST                'self'
              282  LOAD_METHOD              _assert_alive
              284  CALL_METHOD_0         0  ''
              286  POP_TOP          
            288_0  COME_FROM           276  '276'

 L. 714       288  LOAD_FAST                'retlist'
              290  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 74

    @wrap_exceptions
    def num_fds(self):
        return len(os.listdir('%s/%s/fd' % (self._procfs_path, self.pid)))

    @wrap_exceptions
    def num_ctx_switches(self):
        return (_common.pctxsw)(*cext.proc_num_ctx_switches(self.pid, self._procfs_path))

    @wrap_exceptions
    def wait(self, timeout=None):
        return _psposix.wait_pid(self.pid, timeout, self._name)