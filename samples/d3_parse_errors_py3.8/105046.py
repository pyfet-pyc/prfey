# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: threading.py
"""Thread module emulating a subset of Java's threading model."""
import os as _os, sys as _sys, _thread
from time import monotonic as _time
from _weakrefset import WeakSet
from itertools import islice as _islice, count as _count
try:
    from _collections import deque as _deque
except ImportError:
    from collections import deque as _deque
else:
    __all__ = [
     'get_ident', 'active_count', 'Condition', 'current_thread',
     'enumerate', 'main_thread', 'TIMEOUT_MAX',
     'Event', 'Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Thread',
     'Barrier', 'BrokenBarrierError', 'Timer', 'ThreadError',
     'setprofile', 'settrace', 'local', 'stack_size',
     'excepthook', 'ExceptHookArgs']
    _start_new_thread = _thread.start_new_thread
    _allocate_lock = _thread.allocate_lock
    _set_sentinel = _thread._set_sentinel
    get_ident = _thread.get_ident
    try:
        get_native_id = _thread.get_native_id
        _HAVE_THREAD_NATIVE_ID = True
        __all__.append('get_native_id')
    except AttributeError:
        _HAVE_THREAD_NATIVE_ID = False
    else:
        ThreadError = _thread.error
        try:
            _CRLock = _thread.RLock
        except AttributeError:
            _CRLock = None
        else:
            TIMEOUT_MAX = _thread.TIMEOUT_MAX
            del _thread
            _profile_hook = None
            _trace_hook = None

            def setprofile(func):
                """Set a profile function for all threads started from the threading module.

    The func will be passed to sys.setprofile() for each thread, before its
    run() method is called.

    """
                global _profile_hook
                _profile_hook = func


            def settrace(func):
                """Set a trace function for all threads started from the threading module.

    The func will be passed to sys.settrace() for each thread, before its run()
    method is called.

    """
                global _trace_hook
                _trace_hook = func


            Lock = _allocate_lock

            def RLock(*args, **kwargs):
                """Factory function that returns a new reentrant lock.

    A reentrant lock must be released by the thread that acquired it. Once a
    thread has acquired a reentrant lock, the same thread may acquire it again
    without blocking; the thread must release it once for each time it has
    acquired it.

    """
                if _CRLock is None:
                    return _PyRLock(*args, **kwargs)
                return _CRLock(*args, **kwargs)


            class _RLock:
                __doc__ = 'This class implements reentrant lock objects.\n\n    A reentrant lock must be released by the thread that acquired it. Once a\n    thread has acquired a reentrant lock, the same thread may acquire it\n    again without blocking; the thread must release it once for each time it\n    has acquired it.\n\n    '

                def __init__(self):
                    self._block = _allocate_lock()
                    self._owner = None
                    self._count = 0

                def __repr__(self):
                    owner = self._owner
                    try:
                        owner = _active[owner].name
                    except KeyError:
                        pass
                    else:
                        return '<%s %s.%s object owner=%r count=%d at %s>' % (
                         'locked' if self._block.locked() else 'unlocked',
                         self.__class__.__module__,
                         self.__class__.__qualname__,
                         owner,
                         self._count,
                         hex(id(self)))

                def acquire(self, blocking=True, timeout=-1):
                    """Acquire a lock, blocking or non-blocking.

        When invoked without arguments: if this thread already owns the lock,
        increment the recursion level by one, and return immediately. Otherwise,
        if another thread owns the lock, block until the lock is unlocked. Once
        the lock is unlocked (not owned by any thread), then grab ownership, set
        the recursion level to one, and return. If more than one thread is
        blocked waiting until the lock is unlocked, only one at a time will be
        able to grab ownership of the lock. There is no return value in this
        case.

        When invoked with the blocking argument set to true, do the same thing
        as when called without arguments, and return true.

        When invoked with the blocking argument set to false, do not block. If a
        call without an argument would block, return false immediately;
        otherwise, do the same thing as when called without arguments, and
        return true.

        When invoked with the floating-point timeout argument set to a positive
        value, block for at most the number of seconds specified by timeout
        and as long as the lock cannot be acquired.  Return true if the lock has
        been acquired, false if the timeout has elapsed.

        """
                    me = get_ident()
                    if self._owner == me:
                        self._count += 1
                        return 1
                    rc = self._block.acquire(blocking, timeout)
                    if rc:
                        self._owner = me
                        self._count = 1
                    return rc

                __enter__ = acquire

                def release(self):
                    """Release a lock, decrementing the recursion level.

        If after the decrement it is zero, reset the lock to unlocked (not owned
        by any thread), and if any other threads are blocked waiting for the
        lock to become unlocked, allow exactly one of them to proceed. If after
        the decrement the recursion level is still nonzero, the lock remains
        locked and owned by the calling thread.

        Only call this method when the calling thread owns the lock. A
        RuntimeError is raised if this method is called when the lock is
        unlocked.

        There is no return value.

        """
                    if self._owner != get_ident():
                        raise RuntimeError('cannot release un-acquired lock')
                    self._count = count = self._count - 1
                    if not count:
                        self._owner = None
                        self._block.release()

                def __exit__(self, t, v, tb):
                    self.release()

                def _acquire_restore(self, state):
                    self._block.acquire()
                    self._count, self._owner = state

                def _release_save(self):
                    if self._count == 0:
                        raise RuntimeError('cannot release un-acquired lock')
                    count = self._count
                    self._count = 0
                    owner = self._owner
                    self._owner = None
                    self._block.release()
                    return (
                     count, owner)

                def _is_owned(self):
                    return self._owner == get_ident()


            _PyRLock = _RLock

            class Condition:
                __doc__ = 'Class that implements a condition variable.\n\n    A condition variable allows one or more threads to wait until they are\n    notified by another thread.\n\n    If the lock argument is given and not None, it must be a Lock or RLock\n    object, and it is used as the underlying lock. Otherwise, a new RLock object\n    is created and used as the underlying lock.\n\n    '

                def __init__(self, lock=None):
                    if lock is None:
                        lock = RLock()
                    self._lock = lock
                    self.acquire = lock.acquire
                    self.release = lock.release
                    try:
                        self._release_save = lock._release_save
                    except AttributeError:
                        pass
                    else:
                        try:
                            self._acquire_restore = lock._acquire_restore
                        except AttributeError:
                            pass
                        else:
                            try:
                                self._is_owned = lock._is_owned
                            except AttributeError:
                                pass
                            else:
                                self._waiters = _deque()

                def __enter__(self):
                    return self._lock.__enter__()

                def __exit__(self, *args):
                    return (self._lock.__exit__)(*args)

                def __repr__(self):
                    return '<Condition(%s, %d)>' % (self._lock, len(self._waiters))

                def _release_save(self):
                    self._lock.release()

                def _acquire_restore(self, x):
                    self._lock.acquire()

                def _is_owned(self):
                    if self._lock.acquire(0):
                        self._lock.release()
                        return False
                    return True

                def wait--- This code section failed: ---

 L. 293         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _is_owned
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L. 294         8  LOAD_GLOBAL              RuntimeError
               10  LOAD_STR                 'cannot wait on un-acquired lock'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 295        16  LOAD_GLOBAL              _allocate_lock
               18  CALL_FUNCTION_0       0  ''
               20  STORE_FAST               'waiter'

 L. 296        22  LOAD_FAST                'waiter'
               24  LOAD_METHOD              acquire
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          

 L. 297        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _waiters
               34  LOAD_METHOD              append
               36  LOAD_FAST                'waiter'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 298        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _release_save
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'saved_state'

 L. 299        50  LOAD_CONST               False
               52  STORE_FAST               'gotit'

 L. 300        54  SETUP_FINALLY       118  'to 118'

 L. 301        56  LOAD_FAST                'timeout'
               58  LOAD_CONST               None
               60  COMPARE_OP               is
               62  POP_JUMP_IF_FALSE    78  'to 78'

 L. 302        64  LOAD_FAST                'waiter'
               66  LOAD_METHOD              acquire
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          

 L. 303        72  LOAD_CONST               True
               74  STORE_FAST               'gotit'
               76  JUMP_FORWARD        110  'to 110'
             78_0  COME_FROM            62  '62'

 L. 305        78  LOAD_FAST                'timeout'
               80  LOAD_CONST               0
               82  COMPARE_OP               >
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L. 306        86  LOAD_FAST                'waiter'
               88  LOAD_METHOD              acquire
               90  LOAD_CONST               True
               92  LOAD_FAST                'timeout'
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'gotit'
               98  JUMP_FORWARD        110  'to 110'
            100_0  COME_FROM            84  '84'

 L. 308       100  LOAD_FAST                'waiter'
              102  LOAD_METHOD              acquire
              104  LOAD_CONST               False
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'gotit'
            110_0  COME_FROM            98  '98'
            110_1  COME_FROM            76  '76'

 L. 309       110  LOAD_FAST                'gotit'
              112  POP_BLOCK        
              114  CALL_FINALLY        118  'to 118'
              116  RETURN_VALUE     
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM_FINALLY    54  '54'

 L. 311       118  LOAD_FAST                'self'
              120  LOAD_METHOD              _acquire_restore
              122  LOAD_FAST                'saved_state'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L. 312       128  LOAD_FAST                'gotit'
              130  POP_JUMP_IF_TRUE    170  'to 170'

 L. 313       132  SETUP_FINALLY       150  'to 150'

 L. 314       134  LOAD_FAST                'self'
              136  LOAD_ATTR                _waiters
              138  LOAD_METHOD              remove
              140  LOAD_FAST                'waiter'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
              146  POP_BLOCK        
              148  JUMP_FORWARD        170  'to 170'
            150_0  COME_FROM_FINALLY   132  '132'

 L. 315       150  DUP_TOP          
              152  LOAD_GLOBAL              ValueError
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   168  'to 168'
              158  POP_TOP          
              160  POP_TOP          
              162  POP_TOP          

 L. 316       164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
            168_0  COME_FROM           156  '156'
              168  END_FINALLY      
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           148  '148'
            170_2  COME_FROM           130  '130'
              170  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 114

                def wait_for(self, predicate, timeout=None):
                    """Wait until a condition evaluates to True.

        predicate should be a callable which result will be interpreted as a
        boolean value.  A timeout may be provided giving the maximum time to
        wait.

        """
                    endtime = None
                    waittime = timeout
                    result = predicate()
                    while True:
                        if not result:
                            if waittime is not None:
                                if endtime is None:
                                    endtime = _time() + waittime
                                else:
                                    waittime = endtime - _time()
                                    if waittime <= 0:
                                        pass
                                    else:
                                        pass
                            self.wait(waittime)
                            result = predicate()

                    return result

                def notify(self, n=1):
                    """Wake up one or more threads waiting on this condition, if any.

        If the calling thread has not acquired the lock when this method is
        called, a RuntimeError is raised.

        This method wakes up at most n of the threads waiting for the condition
        variable; it is a no-op if no threads are waiting.

        """
                    if not self._is_owned():
                        raise RuntimeError('cannot notify on un-acquired lock')
                    all_waiters = self._waiters
                    waiters_to_notify = _deque(_islice(all_waiters, n))
                    if not waiters_to_notify:
                        return
                    for waiter in waiters_to_notify:
                        waiter.release()
                        try:
                            all_waiters.remove(waiter)
                        except ValueError:
                            pass

                def notify_all(self):
                    """Wake up all threads waiting on this condition.

        If the calling thread has not acquired the lock when this method
        is called, a RuntimeError is raised.

        """
                    self.notify(len(self._waiters))

                notifyAll = notify_all


            class Semaphore:
                __doc__ = 'This class implements semaphore objects.\n\n    Semaphores manage a counter representing the number of release() calls minus\n    the number of acquire() calls, plus an initial value. The acquire() method\n    blocks if necessary until it can return without making the counter\n    negative. If not given, value defaults to 1.\n\n    '

                def __init__(self, value=1):
                    if value < 0:
                        raise ValueError('semaphore initial value must be >= 0')
                    self._cond = Condition(Lock())
                    self._value = value

                def acquire--- This code section failed: ---

 L. 418         0  LOAD_FAST                'blocking'
                2  POP_JUMP_IF_TRUE     20  'to 20'
                4  LOAD_FAST                'timeout'
                6  LOAD_CONST               None
                8  COMPARE_OP               is-not
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 419        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 "can't specify timeout for non-blocking acquire"
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'
             20_1  COME_FROM             2  '2'

 L. 420        20  LOAD_CONST               False
               22  STORE_FAST               'rc'

 L. 421        24  LOAD_CONST               None
               26  STORE_FAST               'endtime'

 L. 422        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _cond
               32  SETUP_WITH          136  'to 136'
               34  POP_TOP          
             36_0  COME_FROM           112  '112'

 L. 423        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _value
               40  LOAD_CONST               0
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE   114  'to 114'

 L. 424        46  LOAD_FAST                'blocking'
               48  POP_JUMP_IF_TRUE     52  'to 52'

 L. 425        50  JUMP_FORWARD        132  'to 132'
             52_0  COME_FROM            48  '48'

 L. 426        52  LOAD_FAST                'timeout'
               54  LOAD_CONST               None
               56  COMPARE_OP               is-not
               58  POP_JUMP_IF_FALSE   100  'to 100'

 L. 427        60  LOAD_FAST                'endtime'
               62  LOAD_CONST               None
               64  COMPARE_OP               is
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 428        68  LOAD_GLOBAL              _time
               70  CALL_FUNCTION_0       0  ''
               72  LOAD_FAST                'timeout'
               74  BINARY_ADD       
               76  STORE_FAST               'endtime'
               78  JUMP_FORWARD        100  'to 100'
             80_0  COME_FROM            66  '66'

 L. 430        80  LOAD_FAST                'endtime'
               82  LOAD_GLOBAL              _time
               84  CALL_FUNCTION_0       0  ''
               86  BINARY_SUBTRACT  
               88  STORE_FAST               'timeout'

 L. 431        90  LOAD_FAST                'timeout'
               92  LOAD_CONST               0
               94  COMPARE_OP               <=
               96  POP_JUMP_IF_FALSE   100  'to 100'

 L. 432        98  JUMP_FORWARD        132  'to 132'
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            78  '78'
            100_2  COME_FROM            58  '58'

 L. 433       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _cond
              104  LOAD_METHOD              wait
              106  LOAD_FAST                'timeout'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
              112  JUMP_BACK            36  'to 36'
            114_0  COME_FROM            44  '44'

 L. 435       114  LOAD_FAST                'self'
              116  DUP_TOP          
              118  LOAD_ATTR                _value
              120  LOAD_CONST               1
              122  INPLACE_SUBTRACT 
              124  ROT_TWO          
              126  STORE_ATTR               _value

 L. 436       128  LOAD_CONST               True
              130  STORE_FAST               'rc'
            132_0  COME_FROM            98  '98'
            132_1  COME_FROM            50  '50'
              132  POP_BLOCK        
              134  BEGIN_FINALLY    
            136_0  COME_FROM_WITH       32  '32'
              136  WITH_CLEANUP_START
              138  WITH_CLEANUP_FINISH
              140  END_FINALLY      

 L. 437       142  LOAD_FAST                'rc'
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 134

                __enter__ = acquire

                def release(self):
                    """Release a semaphore, incrementing the internal counter by one.

        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.

        """
                    with self._cond:
                        self._value += 1
                        self._cond.notify()

                def __exit__(self, t, v, tb):
                    self.release()


            class BoundedSemaphore(Semaphore):
                __doc__ = "Implements a bounded semaphore.\n\n    A bounded semaphore checks to make sure its current value doesn't exceed its\n    initial value. If it does, ValueError is raised. In most situations\n    semaphores are used to guard resources with limited capacity.\n\n    If the semaphore is released too many times it's a sign of a bug. If not\n    given, value defaults to 1.\n\n    Like regular semaphores, bounded semaphores manage a counter representing\n    the number of release() calls minus the number of acquire() calls, plus an\n    initial value. The acquire() method blocks if necessary until it can return\n    without making the counter negative. If not given, value defaults to 1.\n\n    "

                def __init__(self, value=1):
                    Semaphore.__init__(self, value)
                    self._initial_value = value

                def release(self):
                    """Release a semaphore, incrementing the internal counter by one.

        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.

        If the number of releases exceeds the number of acquires,
        raise a ValueError.

        """
                    with self._cond:
                        if self._value >= self._initial_value:
                            raise ValueError('Semaphore released too many times')
                        self._value += 1
                        self._cond.notify()


            class Event:
                __doc__ = 'Class implementing event objects.\n\n    Events manage a flag that can be set to true with the set() method and reset\n    to false with the clear() method. The wait() method blocks until the flag is\n    true.  The flag is initially false.\n\n    '

                def __init__(self):
                    self._cond = Condition(Lock())
                    self._flag = False

                def _reset_internal_locks(self):
                    self._cond.__init__(Lock())

                def is_set(self):
                    """Return true if and only if the internal flag is true."""
                    return self._flag

                isSet = is_set

                def set(self):
                    """Set the internal flag to true.

        All threads waiting for it to become true are awakened. Threads
        that call wait() once the flag is true will not block at all.

        """
                    with self._cond:
                        self._flag = True
                        self._cond.notify_all()

                def clear(self):
                    """Reset the internal flag to false.

        Subsequently, threads calling wait() will block until set() is called to
        set the internal flag to true again.

        """
                    with self._cond:
                        self._flag = False

                def wait(self, timeout=None):
                    """Block until the internal flag is true.

        If the internal flag is true on entry, return immediately. Otherwise,
        block until another thread calls set() to set the flag to true, or until
        the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof).

        This method returns the internal flag on exit, so it will always return
        True except if a timeout is given and the operation times out.

        """
                    with self._cond:
                        signaled = self._flag
                        if not signaled:
                            signaled = self._cond.wait(timeout)
                        return signaled


            class Barrier:
                __doc__ = "Implements a Barrier.\n\n    Useful for synchronizing a fixed number of threads at known synchronization\n    points.  Threads block on 'wait()' and are simultaneously awoken once they\n    have all made that call.\n\n    "

                def __init__(self, parties, action=None, timeout=None):
                    """Create a barrier, initialised to 'parties' threads.

        'action' is a callable which, when supplied, will be called by one of
        the threads after they have all entered the barrier and just prior to
        releasing them all. If a 'timeout' is provided, it is used as the
        default for all subsequent 'wait()' calls.

        """
                    self._cond = Condition(Lock())
                    self._action = action
                    self._timeout = timeout
                    self._parties = parties
                    self._state = 0
                    self._count = 0

                def wait--- This code section failed: ---

 L. 607         0  LOAD_FAST                'timeout'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 608         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _timeout
               12  STORE_FAST               'timeout'
             14_0  COME_FROM             6  '6'

 L. 609        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _cond
               18  SETUP_WITH          134  'to 134'
               20  POP_TOP          

 L. 610        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _enter
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          

 L. 611        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _count
               34  STORE_FAST               'index'

 L. 612        36  LOAD_FAST                'self'
               38  DUP_TOP          
               40  LOAD_ATTR                _count
               42  LOAD_CONST               1
               44  INPLACE_ADD      
               46  ROT_TWO          
               48  STORE_ATTR               _count

 L. 613        50  SETUP_FINALLY       106  'to 106'

 L. 614        52  LOAD_FAST                'index'
               54  LOAD_CONST               1
               56  BINARY_ADD       
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _parties
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    76  'to 76'

 L. 616        66  LOAD_FAST                'self'
               68  LOAD_METHOD              _release
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          
               74  JUMP_FORWARD         86  'to 86'
             76_0  COME_FROM            64  '64'

 L. 619        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _wait
               80  LOAD_FAST                'timeout'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
             86_0  COME_FROM            74  '74'

 L. 620        86  LOAD_FAST                'index'
               88  POP_BLOCK        
               90  CALL_FINALLY        106  'to 106'
               92  POP_BLOCK        
               94  ROT_TWO          
               96  BEGIN_FINALLY    
               98  WITH_CLEANUP_START
              100  WITH_CLEANUP_FINISH
              102  POP_FINALLY           0  ''
              104  RETURN_VALUE     
            106_0  COME_FROM            90  '90'
            106_1  COME_FROM_FINALLY    50  '50'

 L. 622       106  LOAD_FAST                'self'
              108  DUP_TOP          
              110  LOAD_ATTR                _count
              112  LOAD_CONST               1
              114  INPLACE_SUBTRACT 
              116  ROT_TWO          
              118  STORE_ATTR               _count

 L. 624       120  LOAD_FAST                'self'
              122  LOAD_METHOD              _exit
              124  CALL_METHOD_0         0  ''
              126  POP_TOP          
              128  END_FINALLY      
              130  POP_BLOCK        
              132  BEGIN_FINALLY    
            134_0  COME_FROM_WITH       18  '18'
              134  WITH_CLEANUP_START
              136  WITH_CLEANUP_FINISH
              138  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 90

                def _enter(self):
                    while True:
                        if self._state in (-1, 1):
                            self._cond.wait()

                    if self._state < 0:
                        raise BrokenBarrierError
                    assert self._state == 0

                def _release(self):
                    try:
                        if self._action:
                            self._action()
                        self._state = 1
                        self._cond.notify_all()
                    except:
                        self._break()
                        raise

                def _wait(self, timeout):
                    if not self._cond.wait_for(lambda: self._state != 0, timeout):
                        self._break()
                        raise BrokenBarrierError
                    if self._state < 0:
                        raise BrokenBarrierError
                    assert self._state == 1

                def _exit(self):
                    if self._count == 0:
                        if self._state in (-1, 1):
                            self._state = 0
                            self._cond.notify_all()

                def reset(self):
                    """Reset the barrier to the initial state.

        Any threads currently waiting will get the BrokenBarrier exception
        raised.

        """
                    with self._cond:
                        if self._count > 0:
                            if self._state == 0:
                                self._state = -1
                            elif self._state == -2:
                                self._state = -1
                        else:
                            self._state = 0
                        self._cond.notify_all()

                def abort(self):
                    """Place the barrier into a 'broken' state.

        Useful in case of error.  Any currently waiting threads and threads
        attempting to 'wait()' will have BrokenBarrierError raised.

        """
                    with self._cond:
                        self._break()

                def _break(self):
                    self._state = -2
                    self._cond.notify_all()

                @property
                def parties(self):
                    """Return the number of threads required to trip the barrier."""
                    return self._parties

                @property
                def n_waiting(self):
                    """Return the number of threads currently waiting at the barrier."""
                    if self._state == 0:
                        return self._count
                    return 0

                @property
                def broken(self):
                    """Return True if the barrier is in a broken state."""
                    return self._state == -2


            class BrokenBarrierError(RuntimeError):
                pass


            _counter = _count().__next__
            _counter()

            def _newname(template='Thread-%d'):
                return template % _counter()


            _active_limbo_lock = _allocate_lock()
            _active = {}
            _limbo = {}
            _dangling = WeakSet()
            _shutdown_locks_lock = _allocate_lock()
            _shutdown_locks = set()

            class Thread:
                __doc__ = 'A class that represents a thread of control.\n\n    This class can be safely subclassed in a limited fashion. There are two ways\n    to specify the activity: by passing a callable object to the constructor, or\n    by overriding the run() method in a subclass.\n\n    '
                _initialized = False

                def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
                    """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is the argument tuple for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
                    assert group is None, 'group argument must be None for now'
                    if kwargs is None:
                        kwargs = {}
                    self._target = target
                    self._name = str(name or _newname())
                    self._args = args
                    self._kwargs = kwargs
                    if daemon is not None:
                        self._daemonic = daemon
                    else:
                        self._daemonic = current_thread().daemon
                    self._ident = None
                    if _HAVE_THREAD_NATIVE_ID:
                        self._native_id = None
                    self._tstate_lock = None
                    self._started = Event()
                    self._is_stopped = False
                    self._initialized = True
                    self._stderr = _sys.stderr
                    self._invoke_excepthook = _make_invoke_excepthook()
                    _dangling.add(self)

                def _reset_internal_locks(self, is_alive):
                    self._started._reset_internal_locks()
                    if is_alive:
                        self._set_tstate_lock()
                    else:
                        self._is_stopped = True
                        self._tstate_lock = None

                def __repr__(self):
                    assert self._initialized, 'Thread.__init__() was not called'
                    status = 'initial'
                    if self._started.is_set():
                        status = 'started'
                    self.is_alive()
                    if self._is_stopped:
                        status = 'stopped'
                    if self._daemonic:
                        status += ' daemon'
                    if self._ident is not None:
                        status += ' %s' % self._ident
                    return '<%s(%s, %s)>' % (self.__class__.__name__, self._name, status)

                def start(self):
                    """Start the thread's activity.

        It must be called at most once per thread object. It arranges for the
        object's run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        """
                    global _active_limbo_lock
                    if not self._initialized:
                        raise RuntimeError('thread.__init__() not called')
                    if self._started.is_set():
                        raise RuntimeError('threads can only be started once')
                    with _active_limbo_lock:
                        _limbo[self] = self
                    try:
                        _start_new_thread(self._bootstrap, ())
                    except Exception:
                        with _active_limbo_lock:
                            del _limbo[self]
                        raise
                    else:
                        self._started.wait()

                def run(self):
                    """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
                    try:
                        if self._target:
                            (self._target)(*self._args, **self._kwargs)
                    finally:
                        del self._target
                        del self._args
                        del self._kwargs

                def _bootstrap--- This code section failed: ---

 L. 889         0  SETUP_FINALLY        14  'to 14'

 L. 890         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _bootstrap_inner
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         48  'to 48'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 891        14  POP_TOP          
               16  POP_TOP          
               18  POP_TOP          

 L. 892        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _daemonic
               24  POP_JUMP_IF_FALSE    40  'to 40'
               26  LOAD_GLOBAL              _sys
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L. 893        34  POP_EXCEPT       
               36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            32  '32'
             40_1  COME_FROM            24  '24'

 L. 894        40  RAISE_VARARGS_0       0  'reraise'
               42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  END_FINALLY      
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            12  '12'

Parse error at or near `LOAD_CONST' instruction at offset 36

                def _set_ident(self):
                    self._ident = get_ident()

                if _HAVE_THREAD_NATIVE_ID:

                    def _set_native_id(self):
                        self._native_id = get_native_id()

                def _set_tstate_lock(self):
                    """
        Set a lock object which will be released by the interpreter when
        the underlying thread state (see pystate.h) gets deleted.
        """
                    global _shutdown_locks
                    global _shutdown_locks_lock
                    self._tstate_lock = _set_sentinel()
                    self._tstate_lock.acquire()
                    if not self.daemon:
                        with _shutdown_locks_lock:
                            _shutdown_locks.add(self._tstate_lock)

                def _bootstrap_inner(self):
                    try:
                        self._set_ident()
                        self._set_tstate_lock()
                        if _HAVE_THREAD_NATIVE_ID:
                            self._set_native_id()
                        self._started.set()
                        with _active_limbo_lock:
                            _active[self._ident] = self
                            del _limbo[self]
                        if _trace_hook:
                            _sys.settrace(_trace_hook)
                        if _profile_hook:
                            _sys.setprofile(_profile_hook)
                        try:
                            self.run()
                        except:
                            self._invoke_excepthook(self)

                    finally:
                        with _active_limbo_lock:
                            try:
                                del _active[get_ident()]
                            except:
                                pass

                def _stop(self):
                    lock = self._tstate_lock
                    if lock is not None:
                        assert not lock.locked()
                    self._is_stopped = True
                    self._tstate_lock = None
                    if not self.daemon:
                        with _shutdown_locks_lock:
                            _shutdown_locks.discard(lock)

                def _delete(self):
                    """Remove current thread from the dict of currently running threads."""
                    with _active_limbo_lock:
                        del _active[get_ident()]

                def join(self, timeout=None):
                    """Wait until the thread terminates.

        This blocks the calling thread until the thread whose join() method is
        called terminates -- either normally or through an unhandled exception
        or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof). As join() always returns None, you must call
        is_alive() after join() to decide whether a timeout happened -- if the
        thread is still alive, the join() call timed out.

        When the timeout argument is not present or None, the operation will
        block until the thread terminates.

        A thread can be join()ed many times.

        join() raises a RuntimeError if an attempt is made to join the current
        thread as that would cause a deadlock. It is also an error to join() a
        thread before it has been started and attempts to do so raises the same
        exception.

        """
                    if not self._initialized:
                        raise RuntimeError('Thread.__init__() not called')
                    if not self._started.is_set():
                        raise RuntimeError('cannot join thread before it is started')
                    if self is current_thread():
                        raise RuntimeError('cannot join current thread')
                    if timeout is None:
                        self._wait_for_tstate_lock()
                    else:
                        self._wait_for_tstate_lock(timeout=(max(timeout, 0)))

                def _wait_for_tstate_lock(self, block=True, timeout=-1):
                    lock = self._tstate_lock
                    if lock is None:
                        assert self._is_stopped
                    elif lock.acquire(block, timeout):
                        lock.release()
                        self._stop()

                @property
                def name(self):
                    """A string used for identification purposes only.

        It has no semantics. Multiple threads may be given the same name. The
        initial name is set by the constructor.

        """
                    assert self._initialized, 'Thread.__init__() not called'
                    return self._name

                @name.setter
                def name(self, name):
                    assert self._initialized, 'Thread.__init__() not called'
                    self._name = str(name)

                @property
                def ident(self):
                    """Thread identifier of this thread or None if it has not been started.

        This is a nonzero integer. See the get_ident() function. Thread
        identifiers may be recycled when a thread exits and another thread is
        created. The identifier is available even after the thread has exited.

        """
                    assert self._initialized, 'Thread.__init__() not called'
                    return self._ident

                if _HAVE_THREAD_NATIVE_ID:

                    @property
                    def native_id(self):
                        """Native integral thread ID of this thread, or None if it has not been started.

            This is a non-negative integer. See the get_native_id() function.
            This represents the Thread ID as reported by the kernel.

            """
                        assert self._initialized, 'Thread.__init__() not called'
                        return self._native_id

                def is_alive(self):
                    """Return whether the thread is alive.

        This method returns True just before the run() method starts until just
        after the run() method terminates. The module function enumerate()
        returns a list of all alive threads.

        """
                    assert self._initialized, 'Thread.__init__() not called'
                    if not (self._is_stopped or self._started.is_set()):
                        return False
                    self._wait_for_tstate_lock(False)
                    return not self._is_stopped

                def isAlive(self):
                    """Return whether the thread is alive.

        This method is deprecated, use is_alive() instead.
        """
                    import warnings
                    warnings.warn('isAlive() is deprecated, use is_alive() instead', DeprecationWarning,
                      stacklevel=2)
                    return self.is_alive()

                @property
                def daemon(self):
                    """A boolean value indicating whether this thread is a daemon thread.

        This must be set before start() is called, otherwise RuntimeError is
        raised. Its initial value is inherited from the creating thread; the
        main thread is not a daemon thread and therefore all threads created in
        the main thread default to daemon = False.

        The entire Python program exits when only daemon threads are left.

        """
                    assert self._initialized, 'Thread.__init__() not called'
                    return self._daemonic

                @daemon.setter
                def daemon(self, daemonic):
                    if not self._initialized:
                        raise RuntimeError('Thread.__init__() not called')
                    if self._started.is_set():
                        raise RuntimeError('cannot set daemon status of active thread')
                    self._daemonic = daemonic

                def isDaemon(self):
                    return self.daemon

                def setDaemon(self, daemonic):
                    self.daemon = daemonic

                def getName(self):
                    return self.name

                def setName(self, name):
                    self.name = name


            try:
                from _thread import _excepthook as excepthook, _ExceptHookArgs as ExceptHookArgs
            except ImportError:
                from traceback import print_exception as _print_exception
                from collections import namedtuple
                _ExceptHookArgs = namedtuple('ExceptHookArgs', 'exc_type exc_value exc_traceback thread')

                def ExceptHookArgs(args):
                    return _ExceptHookArgs(*args)


                def excepthook(args):
                    """
        Handle uncaught Thread.run() exception.
        """
                    if args.exc_type == SystemExit:
                        return
                    if _sys is not None and _sys.stderr is not None:
                        stderr = _sys.stderr
                    elif args.thread is not None:
                        stderr = args.thread._stderr
                        if stderr is None:
                            return
                    else:
                        return
                    if args.thread is not None:
                        name = args.thread.name
                    else:
                        name = get_ident()
                    print(f"Exception in thread {name}:", file=stderr,
                      flush=True)
                    _print_exception((args.exc_type), (args.exc_value), (args.exc_traceback), file=stderr)
                    stderr.flush()


            else:

                def _make_invoke_excepthook():
                    global excepthook
                    old_excepthook = excepthook
                    old_sys_excepthook = _sys.excepthook
                    if old_excepthook is None:
                        raise RuntimeError('threading.excepthook is None')
                    if old_sys_excepthook is None:
                        raise RuntimeError('sys.excepthook is None')
                    sys_exc_info = _sys.exc_info
                    local_print = print
                    local_sys = _sys

                    def invoke_excepthook(thread):
                        try:
                            try:
                                hook = excepthook
                                if hook is None:
                                    hook = old_excepthook
                                args = ExceptHookArgs([*sys_exc_info(), thread])
                                hook(args)
                            except Exception as exc:
                                try:
                                    exc.__suppress_context__ = True
                                    del exc
                                    if local_sys is not None and local_sys.stderr is not None:
                                        stderr = local_sys.stderr
                                    else:
                                        stderr = thread._stderr
                                    local_print('Exception in threading.excepthook:', file=stderr,
                                      flush=True)
                                    if local_sys is not None and local_sys.excepthook is not None:
                                        sys_excepthook = local_sys.excepthook
                                    else:
                                        sys_excepthook = old_sys_excepthook
                                    sys_excepthook(*sys_exc_info())
                                finally:
                                    exc = None
                                    del exc

                        finally:
                            args = None

                    return invoke_excepthook


                class Timer(Thread):
                    __doc__ = "Call a function after a specified number of seconds:\n\n            t = Timer(30.0, f, args=None, kwargs=None)\n            t.start()\n            t.cancel()     # stop the timer's action if it's still waiting\n\n    "

                    def __init__(self, interval, function, args=None, kwargs=None):
                        Thread.__init__(self)
                        self.interval = interval
                        self.function = function
                        self.args = args if args is not None else []
                        self.kwargs = kwargs if kwargs is not None else {}
                        self.finished = Event()

                    def cancel(self):
                        """Stop the timer if it hasn't finished yet."""
                        self.finished.set()

                    def run(self):
                        self.finished.wait(self.interval)
                        if not self.finished.is_set():
                            (self.function)(*self.args, **self.kwargs)
                        self.finished.set()


                class _MainThread(Thread):

                    def __init__(self):
                        Thread.__init__(self, name='MainThread', daemon=False)
                        self._set_tstate_lock()
                        self._started.set()
                        self._set_ident()
                        if _HAVE_THREAD_NATIVE_ID:
                            self._set_native_id()
                        with _active_limbo_lock:
                            _active[self._ident] = self


                class _DummyThread(Thread):

                    def __init__(self):
                        Thread.__init__(self, name=(_newname('Dummy-%d')), daemon=True)
                        self._started.set()
                        self._set_ident()
                        if _HAVE_THREAD_NATIVE_ID:
                            self._set_native_id()
                        with _active_limbo_lock:
                            _active[self._ident] = self

                    def _stop(self):
                        pass

                    def is_alive(self):
                        if not (self._is_stopped or self._started.is_set()):
                            raise AssertionError
                        return True

                    def join(self, timeout=None):
                        assert False, 'cannot join a dummy thread'


                def current_thread():
                    """Return the current Thread object, corresponding to the caller's thread of control.

    If the caller's thread of control was not created through the threading
    module, a dummy thread object with limited functionality is returned.

    """
                    try:
                        return _active[get_ident()]
                    except KeyError:
                        return _DummyThread()


                currentThread = current_thread

                def active_count():
                    """Return the number of Thread objects currently alive.

    The returned count is equal to the length of the list returned by
    enumerate().

    """
                    with _active_limbo_lock:
                        return len(_active) + len(_limbo)


                activeCount = active_count

                def _enumerate():
                    return list(_active.values()) + list(_limbo.values())


                def enumerate():
                    """Return a list of all Thread objects currently alive.

    The list includes daemonic threads, dummy thread objects created by
    current_thread(), and the main thread. It excludes terminated threads and
    threads that have not yet been started.

    """
                    with _active_limbo_lock:
                        return list(_active.values()) + list(_limbo.values())


                from _thread import stack_size
                _main_thread = _MainThread()

                def _shutdown():
                    """
    Wait until the Python thread state of all non-daemon threads get deleted.
    """
                    global _main_thread
                    if _main_thread._is_stopped:
                        return
                    tlock = _main_thread._tstate_lock
                    assert tlock is not None
                    assert tlock.locked()
                    tlock.release()
                    _main_thread._stop()
                    while True:
                        with _shutdown_locks_lock:
                            locks = list(_shutdown_locks)
                            _shutdown_locks.clear()
                        if not locks:
                            pass
                        else:
                            for lock in locks:
                                lock.acquire()
                                lock.release()


                def main_thread():
                    """Return the main thread object.

    In normal conditions, the main thread is the thread from which the
    Python interpreter was started.
    """
                    return _main_thread


                try:
                    from _thread import _local as local
                except ImportError:
                    from _threading_local import local
                else:

                    def _after_fork():
                        """
    Cleanup threading module state that should not exist after a fork.
    """
                        global _active_limbo_lock
                        global _main_thread
                        global _shutdown_locks
                        global _shutdown_locks_lock
                        _active_limbo_lock = _allocate_lock()
                        new_active = {}
                        try:
                            current = _active[get_ident()]
                        except KeyError:
                            current = _MainThread()
                        else:
                            _main_thread = current
                            _shutdown_locks_lock = _allocate_lock()
                            _shutdown_locks = set()
                            with _active_limbo_lock:
                                threads = set(_enumerate())
                                threads.update(_dangling)
                                for thread in threads:
                                    if thread is current:
                                        thread._reset_internal_locks(True)
                                        ident = get_ident()
                                        thread._ident = ident
                                        new_active[ident] = thread
                                    else:
                                        thread._reset_internal_locks(False)
                                        thread._stop()
                                else:
                                    _limbo.clear()
                                    _active.clear()
                                    _active.update(new_active)
                                    assert len(_active) == 1


                    if hasattr(_os, 'register_at_fork'):
                        _os.register_at_fork(after_in_child=_after_fork)