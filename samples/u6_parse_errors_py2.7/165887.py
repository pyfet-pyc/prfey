# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\psutil-5.4.4-py2.7-win32.egg\psutil\_psposix.py
"""Routines common to all posix systems."""
import errno, glob, os, sys, time
from ._common import memoize
from ._common import sdiskusage
from ._common import usage_percent
from ._compat import PY3
from ._compat import unicode
from ._exceptions import TimeoutExpired
__all__ = [
 'pid_exists', 'wait_pid', 'disk_usage', 'get_terminal_map']

def pid_exists(pid):
    """Check whether pid exists in the current process table."""
    if pid == 0:
        return True
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            return False
        if err.errno == errno.EPERM:
            return True
        raise err
    else:
        return True


def wait_pid(pid, timeout=None, proc_name=None):
    """Wait for process with pid 'pid' to terminate and return its
    exit status code as an integer.

    If pid is not a children of os.getpid() (current process) just
    waits until the process disappears and return None.

    If pid does not exist at all return None immediately.

    Raise TimeoutExpired on timeout expired.
    """

    def check_timeout(delay):
        if timeout is not None:
            if timer() >= stop_at:
                raise TimeoutExpired(timeout, pid=pid, name=proc_name)
        time.sleep(delay)
        return min(delay * 2, 0.04)

    timer = getattr(time, 'monotonic', time.time)
    if timeout is not None:

        def waitcall():
            return os.waitpid(pid, os.WNOHANG)

        stop_at = timer() + timeout
    else:

        def waitcall():
            return os.waitpid(pid, 0)

    delay = 0.0001
    while True:
        try:
            retpid, status = waitcall()
        except OSError as err:
            if err.errno == errno.EINTR:
                delay = check_timeout(delay)
                continue
            elif err.errno == errno.ECHILD:
                while True:
                    if pid_exists(pid):
                        delay = check_timeout(delay)
                    else:
                        return

            else:
                raise
        else:
            if retpid == 0:
                delay = check_timeout(delay)
                continue
            if os.WIFSIGNALED(status):
                return -os.WTERMSIG(status)
            if os.WIFEXITED(status):
                return os.WEXITSTATUS(status)
            raise ValueError('unknown process exit status %r' % status)

    return


def disk_usage(path):
    """Return disk usage associated with path.
    Note: UNIX usually reserves 5% disk space which is not accessible
    by user. In this function "total" and "used" values reflect the
    total and used disk space whereas "free" and "percent" represent
    the "free" and "used percent" user disk space.
    """
    if PY3:
        st = os.statvfs(path)
    else:
        try:
            st = os.statvfs(path)
        except UnicodeEncodeError:
            if isinstance(path, unicode):
                try:
                    path = path.encode(sys.getfilesystemencoding())
                except UnicodeEncodeError:
                    pass

                st = os.statvfs(path)
            else:
                raise

    total = st.f_blocks * st.f_frsize
    avail_to_root = st.f_bfree * st.f_frsize
    avail_to_user = st.f_bavail * st.f_frsize
    used = total - avail_to_root
    total_user = used + avail_to_user
    usage_percent_user = usage_percent(used, total_user, _round=1)
    return sdiskusage(total=total, used=used, free=avail_to_user, percent=usage_percent_user)


@memoize
def get_terminal_map--- This code section failed: ---

 L. 173         0  BUILD_MAP_0           0  None
                3  STORE_FAST            0  'ret'

 L. 174         6  LOAD_GLOBAL           0  'glob'
                9  LOAD_ATTR             0  'glob'
               12  LOAD_CONST               '/dev/tty*'
               15  CALL_FUNCTION_1       1  None
               18  LOAD_GLOBAL           0  'glob'
               21  LOAD_ATTR             0  'glob'
               24  LOAD_CONST               '/dev/pts/*'
               27  CALL_FUNCTION_1       1  None
               30  BINARY_ADD       
               31  STORE_FAST            1  'ls'

 L. 175        34  SETUP_LOOP          107  'to 144'
               37  LOAD_FAST             1  'ls'
               40  GET_ITER         
               41  FOR_ITER             99  'to 143'
               44  STORE_FAST            2  'name'

 L. 176        47  LOAD_FAST             2  'name'
               50  LOAD_FAST             0  'ret'
               53  COMPARE_OP            7  not-in
               56  POP_JUMP_IF_TRUE     68  'to 68'
               59  LOAD_ASSERT              AssertionError
               62  LOAD_FAST             2  'name'
               65  RAISE_VARARGS_2       2  None

 L. 177        68  SETUP_EXCEPT         26  'to 97'

 L. 178        71  LOAD_FAST             2  'name'
               74  LOAD_FAST             0  'ret'
               77  LOAD_GLOBAL           2  'os'
               80  LOAD_ATTR             3  'stat'
               83  LOAD_FAST             2  'name'
               86  CALL_FUNCTION_1       1  None
               89  LOAD_ATTR             4  'st_rdev'
               92  STORE_SUBSCR     
               93  POP_BLOCK        
               94  JUMP_BACK            41  'to 41'
             97_0  COME_FROM            68  '68'

 L. 179        97  DUP_TOP          
               98  LOAD_GLOBAL           5  'OSError'
              101  COMPARE_OP           10  exception-match
              104  POP_JUMP_IF_FALSE   139  'to 139'
              107  POP_TOP          
              108  STORE_FAST            3  'err'
              111  POP_TOP          

 L. 180       112  LOAD_FAST             3  'err'
              115  LOAD_ATTR             6  'errno'
              118  LOAD_GLOBAL           6  'errno'
              121  LOAD_ATTR             7  'ENOENT'
              124  COMPARE_OP            3  !=
              127  POP_JUMP_IF_FALSE   140  'to 140'

 L. 181       130  RAISE_VARARGS_0       0  None
              133  JUMP_ABSOLUTE       140  'to 140'
              136  JUMP_BACK            41  'to 41'
              139  END_FINALLY      
            140_0  COME_FROM           139  '139'
              140  JUMP_BACK            41  'to 41'
              143  POP_BLOCK        
            144_0  COME_FROM            34  '34'

 L. 182       144  LOAD_FAST             0  'ret'
              147  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 143