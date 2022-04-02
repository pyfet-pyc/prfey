# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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

        def __init__--- This code section failed: ---

 L.  51         0  LOAD_FAST                'ctx'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  52         8  LOAD_GLOBAL              context
               10  LOAD_ATTR                _default_context
               12  LOAD_METHOD              get_context
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'ctx'
             18_0  COME_FROM             6  '6'

 L.  53        18  LOAD_FAST                'ctx'
               20  LOAD_METHOD              get_start_method
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'name'

 L.  54        26  LOAD_GLOBAL              sys
               28  LOAD_ATTR                platform
               30  LOAD_STR                 'win32'
               32  COMPARE_OP               ==
               34  JUMP_IF_TRUE_OR_POP    42  'to 42'
               36  LOAD_FAST                'name'
               38  LOAD_STR                 'fork'
               40  COMPARE_OP               ==
             42_0  COME_FROM            34  '34'
               42  STORE_FAST               'unlink_now'

 L.  55        44  LOAD_GLOBAL              range
               46  LOAD_CONST               100
               48  CALL_FUNCTION_1       1  ''
               50  GET_ITER         
             52_0  COME_FROM           114  '114'
             52_1  COME_FROM           106  '106'
               52  FOR_ITER            116  'to 116'
               54  STORE_FAST               'i'

 L.  56        56  SETUP_FINALLY        90  'to 90'

 L.  57        58  LOAD_GLOBAL              _multiprocessing
               60  LOAD_METHOD              SemLock

 L.  58        62  LOAD_FAST                'kind'

 L.  58        64  LOAD_FAST                'value'

 L.  58        66  LOAD_FAST                'maxvalue'

 L.  58        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _make_name
               72  CALL_METHOD_0         0  ''

 L.  59        74  LOAD_FAST                'unlink_now'

 L.  57        76  CALL_METHOD_5         5  ''
               78  DUP_TOP          
               80  STORE_FAST               'sl'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _semlock
               86  POP_BLOCK        
               88  JUMP_FORWARD        110  'to 110'
             90_0  COME_FROM_FINALLY    56  '56'

 L.  60        90  DUP_TOP          
               92  LOAD_GLOBAL              FileExistsError
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   108  'to 108'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L.  61       104  POP_EXCEPT       
              106  JUMP_BACK            52  'to 52'
            108_0  COME_FROM            96  '96'
              108  END_FINALLY      
            110_0  COME_FROM            88  '88'

 L.  63       110  POP_TOP          
              112  BREAK_LOOP          124  'to 124'
              114  JUMP_BACK            52  'to 52'
            116_0  COME_FROM            52  '52'

 L.  65       116  LOAD_GLOBAL              FileExistsError
              118  LOAD_STR                 'cannot find name for semaphore'
              120  CALL_FUNCTION_1       1  ''
              122  RAISE_VARARGS_1       1  'exception instance'
            124_0  COME_FROM           112  '112'

 L.  67       124  LOAD_GLOBAL              util
              126  LOAD_METHOD              debug
              128  LOAD_STR                 'created semlock with handle %s'
              130  LOAD_FAST                'sl'
              132  LOAD_ATTR                handle
              134  BINARY_MODULO    
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          

 L.  68       140  LOAD_FAST                'self'
              142  LOAD_METHOD              _make_methods
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          

 L.  70       148  LOAD_GLOBAL              sys
              150  LOAD_ATTR                platform
              152  LOAD_STR                 'win32'
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   178  'to 178'

 L.  71       158  LOAD_CODE                <code_object _after_fork>
              160  LOAD_STR                 'SemLock.__init__.<locals>._after_fork'
              162  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              164  STORE_FAST               '_after_fork'

 L.  73       166  LOAD_GLOBAL              util
              168  LOAD_METHOD              register_after_fork
              170  LOAD_FAST                'self'
              172  LOAD_FAST                '_after_fork'
              174  CALL_METHOD_2         2  ''
              176  POP_TOP          
            178_0  COME_FROM           156  '156'

 L.  75       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _semlock
              182  LOAD_ATTR                name
              184  LOAD_CONST               None
              186  COMPARE_OP               is-not
              188  POP_JUMP_IF_FALSE   242  'to 242'

 L.  79       190  LOAD_CONST               1
              192  LOAD_CONST               ('register',)
              194  IMPORT_NAME              resource_tracker
              196  IMPORT_FROM              register
              198  STORE_FAST               'register'
              200  POP_TOP          

 L.  80       202  LOAD_FAST                'register'
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                _semlock
              208  LOAD_ATTR                name
              210  LOAD_STR                 'semaphore'
              212  CALL_FUNCTION_2       2  ''
              214  POP_TOP          

 L.  81       216  LOAD_GLOBAL              util
              218  LOAD_ATTR                Finalize
              220  LOAD_FAST                'self'
              222  LOAD_GLOBAL              SemLock
              224  LOAD_ATTR                _cleanup
              226  LOAD_FAST                'self'
              228  LOAD_ATTR                _semlock
              230  LOAD_ATTR                name
              232  BUILD_TUPLE_1         1 

 L.  82       234  LOAD_CONST               0

 L.  81       236  LOAD_CONST               ('exitpriority',)
              238  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              240  POP_TOP          
            242_0  COME_FROM           188  '188'

Parse error at or near `POP_TOP' instruction at offset 240

        @staticmethod
        def _cleanup(name):
            from .resource_tracker import unregister
            sem_unlink(name)
            unregistername'semaphore'

        def _make_methods(self):
            self.acquire = self._semlock.acquire
            self.release = self._semlock.release

        def __enter__(self):
            return self._semlock.__enter__()

        def __exit__(self, *args):
            return (self._semlock.__exit__)(*args)

        def __getstate__(self):
            context.assert_spawningself
            sl = self._semlock
            if sys.platform == 'win32':
                h = context.get_spawning_popen().duplicate_for_childsl.handle
            else:
                h = sl.handle
            return (h, sl.kind, sl.maxvalue, sl.name)

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
                elif self._semlock._count() > 0:
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
                elif self._semlock._get_value() == 1:
                    name, count = ('None', 0)
                elif self._semlock._count() > 0:
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
            self._sleeping_count = ctx.Semaphore0
            self._woken_count = ctx.Semaphore0
            self._wait_semaphore = ctx.Semaphore0
            self._make_methods()

        def __getstate__(self):
            context.assert_spawningself
            return (
             self._lock, self._sleeping_count,
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
                    return self._wait_semaphore.acquireTruetimeout
                finally:
                    self._woken_count.release()
                    for i in range(count):
                        self._lock.acquire()

        def notify(self, n=1):
            assert self._lock._semlock._is_mine(), 'lock is not owned'
            if self._wait_semaphore.acquireFalse:
                raise AssertionError('notify: Should not have been able to acquire _wait_semaphore')
                while True:
                    if self._woken_count.acquireFalse:
                        res = self._sleeping_count.acquireFalse
                        assert not res, 'notify: Bug in sleeping_count.acquire- res should not be False'

                sleepers = 0
                while sleepers < n:
                    if self._sleeping_count.acquireFalse:
                        self._wait_semaphore.release()
                        sleepers += 1

                if sleepers:
                    for i in range(sleepers):
                        self._woken_count.acquire()
                    else:
                        while self._wait_semaphore.acquireFalse:
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
            while True:
                if not result:
                    if endtime is not None:
                        waittime = endtime - time.monotonic()
                        if waittime <= 0:
                            pass
                        else:
                            pass
                    self.waitwaittime
                    result = predicate()

            return result


    class Event(object):

        def __init__(self, *, ctx):
            self._cond = ctx.Conditionctx.Lock()
            self._flag = ctx.Semaphore0

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
                self._flag.acquireFalse
                self._flag.release()
                self._cond.notify_all()

        def clear(self):
            with self._cond:
                self._flag.acquireFalse

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
            wrapper = BufferWrapper(struct.calcsize'i' * 2)
            cond = ctx.Condition()
            self.__setstate__(parties, action, timeout, cond, wrapper)
            self._state = 0
            self._count = 0

        def __setstate__(self, state):
            self._parties, self._action, self._timeout, self._cond, self._wrapper = state
            self._array = self._wrapper.create_memoryview().cast'i'

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