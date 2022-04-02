# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\periodic_executor.py
"""Run a target function on a background thread."""
import atexit, threading, time, weakref
import pymongo.monotonic as _time

class PeriodicExecutor(object):

    def __init__(self, interval, min_interval, target, name=None):
        """"Run a target function periodically on a background thread.

        If the target's return value is false, the executor stops.

        :Parameters:
          - `interval`: Seconds between calls to `target`.
          - `min_interval`: Minimum seconds between calls if `wake` is
            called very often.
          - `target`: A function.
          - `name`: A name to give the underlying thread.
        """
        self._event = False
        self._interval = interval
        self._min_interval = min_interval
        self._target = target
        self._stopped = False
        self._thread = None
        self._name = name
        self._thread_will_exit = False
        self._lock = threading.Lock()

    def open(self):
        """Start. Multiple calls have no effect.

        Not safe to call from multiple threads at once.
        """
        with self._lock:
            if self._thread_will_exit:
                try:
                    self._thread.join()
                except ReferenceError:
                    pass

            self._thread_will_exit = False
            self._stopped = False
        started = False
        try:
            started = self._thread and self._thread.is_alive()
        except ReferenceError:
            pass
        else:
            if not started:
                thread = threading.Thread(target=(self._run), name=(self._name))
                thread.daemon = True
                self._thread = weakref.proxy(thread)
                _register_executor(self)
                thread.start()

    def close(self, dummy=None):
        """Stop. To restart, call open().

        The dummy parameter allows an executor's close method to be a weakref
        callback; see monitor.py.
        """
        self._stopped = True

    def join(self, timeout=None):
        if self._thread is not None:
            try:
                self._thread.join(timeout)
            except (ReferenceError, RuntimeError):
                pass

    def wake(self):
        """Execute the target function soon."""
        self._event = True

    def update_interval(self, new_interval):
        self._interval = new_interval

    def __should_stop--- This code section failed: ---

 L. 109         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           48  'to 48'
                6  POP_TOP          

 L. 110         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _stopped
               12  POP_JUMP_IF_FALSE    34  'to 34'

 L. 111        14  LOAD_CONST               True
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _thread_will_exit

 L. 112        20  POP_BLOCK        
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  LOAD_CONST               True
               32  RETURN_VALUE     
             34_0  COME_FROM            12  '12'

 L. 113        34  POP_BLOCK        
               36  BEGIN_FINALLY    
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  POP_FINALLY           0  ''
               44  LOAD_CONST               False
               46  RETURN_VALUE     
             48_0  COME_FROM_WITH        4  '4'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 22

    def _run--- This code section failed: ---

 L. 116         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _PeriodicExecutor__should_stop
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_TRUE    134  'to 134'

 L. 117         8  SETUP_FINALLY        32  'to 32'

 L. 118        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _target
               14  CALL_METHOD_0         0  ''
               16  POP_JUMP_IF_TRUE     28  'to 28'

 L. 119        18  LOAD_CONST               True
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _stopped

 L. 120        24  POP_BLOCK        
               26  JUMP_ABSOLUTE       134  'to 134'
             28_0  COME_FROM            16  '16'
               28  POP_BLOCK        
               30  JUMP_FORWARD         76  'to 76'
             32_0  COME_FROM_FINALLY     8  '8'

 L. 121        32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 122        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _lock
               42  SETUP_WITH           62  'to 62'
               44  POP_TOP          

 L. 123        46  LOAD_CONST               True
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _stopped

 L. 124        52  LOAD_CONST               True
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _thread_will_exit
               58  POP_BLOCK        
               60  BEGIN_FINALLY    
             62_0  COME_FROM_WITH       42  '42'
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      

 L. 126        68  RAISE_VARARGS_0       0  'reraise'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            30  '30'

 L. 128        76  LOAD_GLOBAL              _time
               78  CALL_FUNCTION_0       0  ''
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _interval
               84  BINARY_ADD       
               86  STORE_FAST               'deadline'
             88_0  COME_FROM           120  '120'

 L. 130        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _stopped
               92  POP_JUMP_IF_TRUE    126  'to 126'
               94  LOAD_GLOBAL              _time
               96  CALL_FUNCTION_0       0  ''
               98  LOAD_FAST                'deadline'
              100  COMPARE_OP               <
              102  POP_JUMP_IF_FALSE   126  'to 126'

 L. 131       104  LOAD_GLOBAL              time
              106  LOAD_METHOD              sleep
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _min_interval
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L. 132       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _event
              120  POP_JUMP_IF_FALSE    88  'to 88'

 L. 133       122  BREAK_LOOP          126  'to 126'
              124  JUMP_BACK            88  'to 88'
            126_0  COME_FROM           102  '102'
            126_1  COME_FROM            92  '92'

 L. 135       126  LOAD_CONST               False
              128  LOAD_FAST                'self'
              130  STORE_ATTR               _event
              132  JUMP_BACK             0  'to 0'
            134_0  COME_FROM             6  '6'

Parse error at or near `COME_FROM' instruction at offset 28_0


_EXECUTORS = set()

def _register_executor(executor):
    ref = weakref.ref(executor, _on_executor_deleted)
    _EXECUTORS.add(ref)


def _on_executor_deleted(ref):
    _EXECUTORS.remove(ref)


def _shutdown_executors():
    if _EXECUTORS is None:
        return
    executors = list(_EXECUTORS)
    for ref in executors:
        executor = ref()
        if executor:
            executor.close()
        for ref in executors:
            executor = ref()
            if executor:
                executor.join(1)
            executor = None


atexit.register(_shutdown_executors)