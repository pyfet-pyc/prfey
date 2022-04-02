# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\psutil\_psposix.py
"""Routines common to all posix systems."""
import glob, os, signal, sys, time
from ._common import memoize
from ._common import sdiskusage
from ._common import TimeoutExpired
from ._common import usage_percent
from ._compat import ChildProcessError
from ._compat import FileNotFoundError
from ._compat import InterruptedError
from ._compat import PermissionError
from ._compat import ProcessLookupError
from ._compat import PY3
from ._compat import unicode
if sys.version_info >= (3, 4):
    import enum
else:
    enum = None
__all__ = [
 'pid_exists', 'wait_pid', 'disk_usage', 'get_terminal_map']

def pid_exists(pid):
    """Check whether pid exists in the current process table."""
    if pid == 0:
        return True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    else:
        return True


if enum is not None and hasattr(signal, 'Signals'):
    Negsignal = enum.IntEnum('Negsignal', dict([(x.name, -x.value) for x in signal.Signals]))

    def negsig_to_enum(num):
        """Convert a negative signal value to an enum."""
        try:
            return Negsignal(num)
        except ValueError:
            return num


else:

    def negsig_to_enum(num):
        return num


def wait_pid--- This code section failed: ---

 L.  96         0  LOAD_DEREF               'pid'
                2  LOAD_CONST               0
                4  COMPARE_OP               <=
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  97         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 "can't wait for PID 0"
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  98        16  LOAD_CONST               0.0001
               18  STORE_FAST               'interval'

 L.  99        20  LOAD_CONST               0
               22  STORE_FAST               'flags'

 L. 100        24  LOAD_DEREF               'timeout'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_FALSE    52  'to 52'

 L. 101        32  LOAD_FAST                'flags'
               34  LOAD_GLOBAL              os
               36  LOAD_ATTR                WNOHANG
               38  INPLACE_OR       
               40  STORE_FAST               'flags'

 L. 102        42  LOAD_DEREF               '_timer'
               44  CALL_FUNCTION_0       0  ''
               46  LOAD_DEREF               'timeout'
               48  BINARY_ADD       
               50  STORE_DEREF              'stop_at'
             52_0  COME_FROM            30  '30'

 L. 104        52  LOAD_CLOSURE             '_min'
               54  LOAD_CLOSURE             '_sleep'
               56  LOAD_CLOSURE             '_timer'
               58  LOAD_CLOSURE             'pid'
               60  LOAD_CLOSURE             'proc_name'
               62  LOAD_CLOSURE             'stop_at'
               64  LOAD_CLOSURE             'timeout'
               66  BUILD_TUPLE_7         7 
               68  LOAD_CODE                <code_object sleep>
               70  LOAD_STR                 'wait_pid.<locals>.sleep'
               72  MAKE_FUNCTION_8          'closure'
               74  STORE_FAST               'sleep'
             76_0  COME_FROM           242  '242'
             76_1  COME_FROM           182  '182'
             76_2  COME_FROM           180  '180'
             76_3  COME_FROM           122  '122'

 L. 114        76  SETUP_FINALLY        98  'to 98'

 L. 115        78  LOAD_GLOBAL              os
               80  LOAD_METHOD              waitpid
               82  LOAD_DEREF               'pid'
               84  LOAD_FAST                'flags'
               86  CALL_METHOD_2         2  ''
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'retpid'
               92  STORE_FAST               'status'
               94  POP_BLOCK        
               96  JUMP_FORWARD        164  'to 164'
             98_0  COME_FROM_FINALLY    76  '76'

 L. 116        98  DUP_TOP          
              100  LOAD_GLOBAL              InterruptedError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   124  'to 124'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L. 117       112  LOAD_FAST                'sleep'
              114  LOAD_FAST                'interval'
              116  CALL_FUNCTION_1       1  ''
              118  STORE_FAST               'interval'
              120  POP_EXCEPT       
              122  JUMP_BACK            76  'to 76'
            124_0  COME_FROM           104  '104'

 L. 118       124  DUP_TOP          
              126  LOAD_GLOBAL              ChildProcessError
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   162  'to 162'
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          
            138_0  COME_FROM           154  '154'

 L. 125       138  LOAD_FAST                '_pid_exists'
              140  LOAD_DEREF               'pid'
              142  CALL_FUNCTION_1       1  ''
              144  POP_JUMP_IF_FALSE   156  'to 156'

 L. 126       146  LOAD_FAST                'sleep'
              148  LOAD_FAST                'interval'
              150  CALL_FUNCTION_1       1  ''
              152  STORE_FAST               'interval'
              154  JUMP_BACK           138  'to 138'
            156_0  COME_FROM           144  '144'

 L. 127       156  POP_EXCEPT       
              158  LOAD_CONST               None
              160  RETURN_VALUE     
            162_0  COME_FROM           130  '130'
              162  END_FINALLY      
            164_0  COME_FROM            96  '96'

 L. 129       164  LOAD_FAST                'retpid'
              166  LOAD_CONST               0
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   184  'to 184'

 L. 131       172  LOAD_FAST                'sleep'
              174  LOAD_FAST                'interval'
              176  CALL_FUNCTION_1       1  ''
              178  STORE_FAST               'interval'

 L. 132       180  CONTINUE             76  'to 76'
              182  JUMP_BACK            76  'to 76'
            184_0  COME_FROM           170  '170'

 L. 133       184  LOAD_GLOBAL              os
              186  LOAD_METHOD              WIFEXITED
              188  LOAD_FAST                'status'
              190  CALL_METHOD_1         1  ''
              192  POP_JUMP_IF_FALSE   204  'to 204'

 L. 137       194  LOAD_GLOBAL              os
              196  LOAD_METHOD              WEXITSTATUS
              198  LOAD_FAST                'status'
              200  CALL_METHOD_1         1  ''
              202  RETURN_VALUE     
            204_0  COME_FROM           192  '192'

 L. 138       204  LOAD_GLOBAL              os
              206  LOAD_METHOD              WIFSIGNALED
              208  LOAD_FAST                'status'
              210  CALL_METHOD_1         1  ''
              212  POP_JUMP_IF_FALSE   230  'to 230'

 L. 141       214  LOAD_GLOBAL              negsig_to_enum
              216  LOAD_GLOBAL              os
              218  LOAD_METHOD              WTERMSIG
              220  LOAD_FAST                'status'
              222  CALL_METHOD_1         1  ''
              224  UNARY_NEGATIVE   
              226  CALL_FUNCTION_1       1  ''
              228  RETURN_VALUE     
            230_0  COME_FROM           212  '212'

 L. 158       230  LOAD_GLOBAL              ValueError
              232  LOAD_STR                 'unknown process exit status %r'
              234  LOAD_FAST                'status'
              236  BINARY_MODULO    
              238  CALL_FUNCTION_1       1  ''
              240  RAISE_VARARGS_1       1  'exception instance'
              242  JUMP_BACK            76  'to 76'

Parse error at or near `LOAD_CONST' instruction at offset 158


def disk_usage(path):
    """Return disk usage associated with path.
    Note: UNIX usually reserves 5% disk space which is not accessible
    by user. In this function "total" and "used" values reflect the
    total and used disk space whereas "free" and "percent" represent
    the "free" and "used percent" user disk space.
    """
    if PY3:
        st = os.statvfspath
    else:
        pass
    try:
        st = os.statvfspath
    except UnicodeEncodeError:
        if isinstance(path, unicode):
            try:
                path = path.encodesys.getfilesystemencoding()
            except UnicodeEncodeError:
                pass
            else:
                st = os.statvfspath
        else:
            raise
    else:
        total = st.f_blocks * st.f_frsize
        avail_to_root = st.f_bfree * st.f_frsize
        avail_to_user = st.f_bavail * st.f_frsize
        used = total - avail_to_root
        total_user = used + avail_to_user
        usage_percent_user = usage_percent(used, total_user, round_=1)
        return sdiskusage(total=total,
          used=used,
          free=avail_to_user,
          percent=usage_percent_user)


@memoize
def get_terminal_map():
    """Get a map of device-id -> path as a dict.
    Used by Process.terminal()
    """
    ret = {}
    ls = glob.glob'/dev/tty*' + glob.glob'/dev/pts/*'
    for name in ls:
        if not name not in ret:
            raise AssertionError(name)
        else:
            try:
                ret[os.statname.st_rdev] = name
            except FileNotFoundError:
                pass

    else:
        return ret