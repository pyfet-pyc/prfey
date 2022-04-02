# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\synchronize.py
__all__ = [
 'Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Condition', 'Event']
import threading, sys, tempfile, _multiprocessing, time
from . import context
from . import process
from . import util
try:
    from _multiprocessing import SemLock, sem_unlink
except ImportError:
    raise ImportError('This platform lacks a functioning sem_open implementation, therefore, the required synchronization primitives needed will not function, see issue 3770.')
else:
    RECURSIVE_MUTEX, SEMAPHORE = list(range(2))
    SEM_VALUE_MAX = _multiprocessing.SemLock.SEM_VALUE_MAX

    class SemLock(object):
        _rand = tempfile._RandomNameSequence()

        def __init__(self, kind, value, maxvalue, *, ctx):
            if ctx is None:
                ctx = context._default_context.get_context()
            name = ctx.get_start_method()
            unlink_now = sys.platform == 'win32' or name == 'fork'
            for i in range(100):
                try:
                    sl = self._semlock = _multiprocessing.SemLock(kind, value, maxvalue, self._make_name(), unlink_now)
                except FileExistsError:
                    pass
                else:
                    break
            else:
                raise FileExistsError('cannot find name for semaphore')
                util.debug('created semlock with handle %s' % sl.handle)
                self._make_methods()
                if sys.platform != 'win32':

                    def _after_fork(obj):
                        obj._semlock._after_fork()

                    util.register_after_fork(self, _after_fork)
                if self._semlock.name is not None:
                    from .resource_tracker import register
                    register(self._semlock.name, 'semaphore')
                    util.Finalize(self, (SemLock._cleanup), (self._semlock.name,), exitpriority=0)

        @staticmethod
        def _cleanup(name):
            from .resource_tracker import unregister
            sem_unlink(name)
            unregister(name, 'semaphore')

        def _make_methods(self):
            self.acquire = self._semlock.acquire
            self.release = self._semlock.release

        def __enter__(self):
            return self._semlock.__enter__()

        def __exit__(self, *args):
            return (self._semlock.__exit__)(*args)

        def __getstate__(self):
            context.assert_spawning(self)
            sl = self._semlock
            if sys.platform == 'win32':
                h = context.get_spawning_popen().duplicate_for_child(sl.handle)
            else:
                h = sl.handle
            return (
             h, sl.kind, sl.maxvalue, sl.name)

        def __setstate__(self, state):
            self._semlock = (_multiprocessing.SemLock._rebuild)(*state)
            util.debug('recreated blocker with handle %r' % state[0])
            self._make_methods()

        @staticmethod
        def _make_name():
            return '%s-%s' % (process.current_process()._config['semprefix'],
             next(SemLock._rand))


    class Semaphore(SemLock):

        def __init__(self, value=1, *, ctx):
            SemLock.__init__(self, SEMAPHORE, value, SEM_VALUE_MAX, ctx=ctx)

        def get_value(self):
            return self._semlock._get_value()

        def __repr__(self):
            try:
                value = self._semlock._get_value()
            except Exception:
                value = 'unknown'
            else:
                return '<%s(value=%s)>' % (self.__class__.__name__, value)


    class BoundedSemaphore(Semaphore):

        def __init__(self, value=1, *, ctx):
            SemLock.__init__(self, SEMAPHORE, value, value, ctx=ctx)

        def __repr__(self):
            try:
                value = self._semlock._get_value()
            except Exception:
                value = 'unknown'
            else:
                return '<%s(value=%s, maxvalue=%s)>' % (
                 self.__class__.__name__, value, self._semlock.maxvalue)


    class Lock(SemLock):

        def __init__(self, *, ctx):
            SemLock.__init__(self, SEMAPHORE, 1, 1, ctx=ctx)

        def __repr__(self):
            try:
                if self._semlock._is_mine():
                    name = process.current_process().name
                    if threading.current_thread().name != 'MainThread':
                        name += '|' + threading.current_thread().name
                elif self._semlock._get_value() == 1:
                    name = 'None'
                else:
                    if self._semlock._count() > 0:
                        name = 'SomeOtherThread'
                    else:
                        name = 'SomeOtherProcess'
            except Exception:
                name = 'unknown'
            else:
                return '<%s(owner=%s)>' % (self.__class__.__name__, name)


    class RLock(SemLock):

        def __init__(self, *, ctx):
            SemLock.__init__(self, RECURSIVE_MUTEX, 1, 1, ctx=ctx)

        def __repr__(self):
            try:
                if self._semlock._is_mine():
                    name = process.current_process().name
                    if threading.current_thread().name != 'MainThread':
                        name += '|' + threading.current_thread().name
                    count = self._semlock._count()
                else:
                    if self._semlock._get_value() == 1:
                        name, count = ('None', 0)
                    else:
                        if self._semlock._count() > 0:
                            name, count = ('SomeOtherThread', 'nonzero')
                        else:
                            name, count = ('SomeOtherProcess', 'nonzero')
            except Exception:
                name, count = ('unknown', 'unknown')
            else:
                return '<%s(%s, %s)>' % (self.__class__.__name__, name, count)


    class Condition(object):

        def __init__(self, lock=None, *, ctx):
            self._lock = lock or ctx.RLock()
            self._sleeping_count = ctx.Semaphore(0)
            self._woken_count = ctx.Semaphore(0)
            self._wait_semaphore = ctx.Semaphore(0)
            self._make_methods()

        def __getstate__(self):
            context.assert_spawning(self)
            return (self._lock, self._sleeping_count,
             self._woken_count, self._wait_semaphore)

        def __setstate__(self, state):
            self._lock, self._sleeping_count, self._woken_count, self._wait_semaphore = state
            self._make_methods()

        def __enter__(self):
            return self._lock.__enter__()

        def __exit__(self, *args):
            return (self._lock.__exit__)(*args)

        def _make_methods(self):
            self.acquire = self._lock.acquire
            self.release = self._lock.release

        def __repr__(self):
            try:
                num_waiters = self._sleeping_count._semlock._get_value() - self._woken_count._semlock._get_value()
            except Exception:
                num_waiters = 'unknown'
            else:
                return '<%s(%s, %s)>' % (self.__class__.__name__, self._lock, num_waiters)

        def wait(self, timeout=None):
            assert self._lock._semlock._is_mine(), 'must acquire() condition before using wait()'
            self._sleeping_count.release()
            count = self._lock._semlock._count()
            for i in range(count):
                self._lock.release()
            else:
                try:
                    return self._wait_semaphore.acquire(True, timeout)
                finally:
                    self._woken_count.release()
                    for i in range(count):
                        self._lock.acquire()

        def notify(self, n=1):
            if not self._lock._semlock._is_mine():
                raise AssertionError('lock is not owned')
            elif self._wait_semaphore.acquire(False):
                raise AssertionError('notify: Should not have been able to acquire _wait_semaphore')
            else:
                while self._woken_count.acquire(False):
                    res = self._sleeping_count.acquire(False)
                    assert res, 'notify: Bug in sleeping_count.acquire- res should not be False'

                sleepers = 0
                while True:
                    if sleepers < n and self._sleeping_count.acquire(False):
                        self._wait_semaphore.release()
                        sleepers += 1

            if sleepers:
                for i in range(sleepers):
                    self._woken_count.acquire()
                else:
                    while self._wait_semaphore.acquire(False):
                        pass

        def notify_all(self):
            self.notify(n=(sys.maxsize))

        def wait_for(self, predicate, timeout=None):
            result = predicate()
            if result:
                return result
            if timeout is not None:
                endtime = time.monotonic() + timeout
            else:
                endtime = None
                waittime = None
                while not result:
                    if endtime is not None:
                        waittime = endtime - time.monotonic()
                        if waittime <= 0:
                            break
                    self.wait(waittime)
                    result = predicate()

                return result


    class Event(object):

        def __init__(self, *, ctx):
            self._cond = ctx.Condition(ctx.Lock())
            self._flag = ctx.Semaphore(0)

        def is_set--- This code section failed: ---

 L. 328         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cond
                4  SETUP_WITH           58  'to 58'
                6  POP_TOP          

 L. 329         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _flag
               12  LOAD_METHOD              acquire
               14  LOAD_CONST               False
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_FALSE    44  'to 44'

 L. 330        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _flag
               24  LOAD_METHOD              release
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          

 L. 331        30  POP_BLOCK        
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  LOAD_CONST               True
               42  RETURN_VALUE     
             44_0  COME_FROM            18  '18'

 L. 332        44  POP_BLOCK        
               46  BEGIN_FINALLY    
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  POP_FINALLY           0  ''
               54  LOAD_CONST               False
               56  RETURN_VALUE     
             58_0  COME_FROM_WITH        4  '4'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 32

        def set(self):
            with self._cond:
                self._flag.acquire(False)
                self._flag.release()
                self._cond.notify_all()

        def clear(self):
            with self._cond:
                self._flag.acquire(False)

        def wait--- This code section failed: ---

 L. 345         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cond
                4  SETUP_WITH           94  'to 94'
                6  POP_TOP          

 L. 346         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _flag
               12  LOAD_METHOD              acquire
               14  LOAD_CONST               False
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 347        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _flag
               24  LOAD_METHOD              release
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          
               30  JUMP_FORWARD         44  'to 44'
             32_0  COME_FROM            18  '18'

 L. 349        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _cond
               36  LOAD_METHOD              wait
               38  LOAD_FAST                'timeout'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
             44_0  COME_FROM            30  '30'

 L. 351        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _flag
               48  LOAD_METHOD              acquire
               50  LOAD_CONST               False
               52  CALL_METHOD_1         1  ''
               54  POP_JUMP_IF_FALSE    80  'to 80'

 L. 352        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _flag
               60  LOAD_METHOD              release
               62  CALL_METHOD_0         0  ''
               64  POP_TOP          

 L. 353        66  POP_BLOCK        
               68  BEGIN_FINALLY    
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  POP_FINALLY           0  ''
               76  LOAD_CONST               True
               78  RETURN_VALUE     
             80_0  COME_FROM            54  '54'

 L. 354        80  POP_BLOCK        
               82  BEGIN_FINALLY    
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  POP_FINALLY           0  ''
               90  LOAD_CONST               False
               92  RETURN_VALUE     
             94_0  COME_FROM_WITH        4  '4'
               94  WITH_CLEANUP_START
               96  WITH_CLEANUP_FINISH
               98  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 68


    class Barrier(threading.Barrier):

        def __init__(self, parties, action=None, timeout=None, *, ctx):
            import struct
            from .heap import BufferWrapper
            wrapper = BufferWrapper(struct.calcsize('i') * 2)
            cond = ctx.Condition()
            self.__setstate__((parties, action, timeout, cond, wrapper))
            self._state = 0
            self._count = 0

        def __setstate__(self, state):
            self._parties, self._action, self._timeout, self._cond, self._wrapper = state
            self._array = self._wrapper.create_memoryview().cast('i')

        def __getstate__(self):
            return (
             self._parties, self._action, self._timeout,
             self._cond, self._wrapper)

        @property
        def _state(self):
            return self._array[0]

        @_state.setter
        def _state(self, value):
            self._array[0] = value

        @property
        def _count(self):
            return self._array[1]

        @_count.setter
        def _count(self, value):
            self._array[1] = value