# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\daemon.py
"""Support for spawning a daemon process.

PyMongo only attempts to spawn the mongocryptd daemon process when automatic
client-side field level encryption is enabled. See
:ref:`automatic-client-side-encryption` for more info.
"""
import os, subprocess, sys, time
_WAIT_TIMEOUT = 10
_THIS_FILE = os.path.realpath(__file__)
if sys.version_info[0] < 3:

    def _popen_wait(popen, timeout):
        """Implement wait timeout support for Python 2."""
        import pymongo.monotonic as _time
        deadline = _time() + timeout
        delay = 0.0005
        while True:
            returncode = popen.poll()
            if returncode is not None:
                return returncode
            else:
                remaining = deadline - _time()
                if remaining <= 0:
                    return
                delay = min(delay * 2, remaining, 0.5)
                time.sleep(delay)


else:

    def _popen_wait--- This code section failed: ---

 L.  53         0  SETUP_FINALLY        16  'to 16'

 L.  54         2  LOAD_FAST                'popen'
                4  LOAD_ATTR                wait
                6  LOAD_FAST                'timeout'
                8  LOAD_CONST               ('timeout',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  55        16  DUP_TOP          
               18  LOAD_GLOBAL              subprocess
               20  LOAD_ATTR                TimeoutExpired
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    38  'to 38'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  57        32  POP_EXCEPT       
               34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            24  '24'
               38  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 34


def _silence_resource_warning(popen):
    """Silence Popen's ResourceWarning.

    Note this should only be used if the process was created as a daemon.
    """
    popen.returncode = 0


if sys.platform == 'win32':
    _DETACHED_PROCESS = getattr(subprocess, 'DETACHED_PROCESS', 8)

    def _spawn_daemon(args):
        """Spawn a daemon process (Windows)."""
        with open(os.devnull, 'r+b') as devnull:
            popen = subprocess.Popen(args,
              creationflags=_DETACHED_PROCESS,
              stdin=devnull,
              stderr=devnull,
              stdout=devnull)
            _silence_resource_warning(popen)


else:

    def _spawn(args):
        """Spawn the process and silence stdout/stderr."""
        with open(os.devnull, 'r+b') as devnull:
            return subprocess.Popen(args,
              close_fds=True,
              stdin=devnull,
              stderr=devnull,
              stdout=devnull)


    def _spawn_daemon_double_popen(args):
        """Spawn a daemon process using a double subprocess.Popen."""
        spawner_args = [
         sys.executable, _THIS_FILE]
        spawner_args.extend(args)
        temp_proc = subprocess.Popen(spawner_args, close_fds=True)
        _popen_wait(temp_proc, _WAIT_TIMEOUT)


    def _spawn_daemon(args):
        """Spawn a daemon process (Unix)."""
        if sys.executable:
            _spawn_daemon_double_popen(args)
        else:
            _spawn(args)


    if __name__ == '__main__':
        if hasattr(os, 'setsid'):
            try:
                os.setsid()
            except OSError:
                pass

        _silence_resource_warning(_spawn(sys.argv[1:]))
        os._exit(0)