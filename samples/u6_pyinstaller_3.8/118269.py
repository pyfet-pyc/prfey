# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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

Parse error at or near `POP_TOP' instruction at offset 28


def _silence_resource_warning(popen):
    """Silence Popen's ResourceWarning.

    Note this should only be used if the process was created as a daemon.
    """
    popen.returncode = 0


if sys.platform == 'win32':
    _DETACHED_PROCESS = getattr(subprocess, 'DETACHED_PROCESS', 8)

    def _spawn_daemon(args):
        """Spawn a daemon process (Windows)."""
        with open(os.devnull, 'r+b') as (devnull):
            popen = subprocess.Popen(args,
              creationflags=_DETACHED_PROCESS,
              stdin=devnull,
              stderr=devnull,
              stdout=devnull)
            _silence_resource_warning(popen)


else:

    def _spawn--- This code section failed: ---

 L.  98         0  LOAD_GLOBAL              open
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                devnull
                6  LOAD_STR                 'r+b'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           46  'to 46'
               12  STORE_FAST               'devnull'

 L.  99        14  LOAD_GLOBAL              subprocess
               16  LOAD_ATTR                Popen

 L. 100        18  LOAD_FAST                'args'

 L. 101        20  LOAD_CONST               True

 L. 102        22  LOAD_FAST                'devnull'

 L. 102        24  LOAD_FAST                'devnull'

 L. 102        26  LOAD_FAST                'devnull'

 L.  99        28  LOAD_CONST               ('close_fds', 'stdin', 'stderr', 'stdout')
               30  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               32  POP_BLOCK        
               34  ROT_TWO          
               36  BEGIN_FINALLY    
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  POP_FINALLY           0  ''
               44  RETURN_VALUE     
             46_0  COME_FROM_WITH       10  '10'
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 34


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