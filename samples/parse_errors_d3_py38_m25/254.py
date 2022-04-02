# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\locks.py
"""Synchronization primitives."""
__all__ = ('Lock', 'Event', 'Condition', 'Semaphore', 'BoundedSemaphore')
import collections, types, warnings
from . import events
from . import futures
from . import exceptions
from . import coroutines

class _ContextManager:
    __doc__ = "Context manager.\n\n    This enables the following idiom for acquiring and releasing a\n    lock around a block:\n\n        with (yield from lock):\n            <block>\n\n    while failing loudly when accidentally using:\n\n        with lock:\n            <block>\n\n    Deprecated, use 'async with' statement:\n        async with lock:\n            <block>\n    "

    def __init__(self, lock):
        self._lock = lock

    def __enter__(self):
        pass

    def __exit__(self, *args):
        try:
            self._lock.release()
        finally:
            self._lock = None


class _ContextManagerMixin:

    def __enter__(self):
        raise RuntimeError('"yield from" should be used as context manager expression')

    def __exit__(self, *args):
        pass

    @types.coroutine
    def __iter__(self):
        warnings.warn("'with (yield from lock)' is deprecated use 'async with lock' instead", DeprecationWarning,
          stacklevel=2)
        yield from self.acquire()
        return _ContextManager(self)
        if False:
            yield None

    __iter__._is_coroutine = coroutines._is_coroutine

    async def __acquire_ctx(self):
        await self.acquire()
        return _ContextManager(self)

    def __await__(self):
        warnings.warn("'with await lock' is deprecated use 'async with lock' instead", DeprecationWarning,
          stacklevel=2)
        return self._ContextManagerMixin__acquire_ctx().__await__()

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        self.release()


class Lock(_ContextManagerMixin):
    __doc__ = "Primitive lock objects.\n\n    A primitive lock is a synchronization primitive that is not owned\n    by a particular coroutine when locked.  A primitive lock is in one\n    of two states, 'locked' or 'unlocked'.\n\n    It is created in the unlocked state.  It has two basic methods,\n    acquire() and release().  When the state is unlocked, acquire()\n    changes the state to locked and returns immediately.  When the\n    state is locked, acquire() blocks until a call to release() in\n    another coroutine changes it to unlocked, then the acquire() call\n    resets it to locked and returns.  The release() method should only\n    be called in the locked state; it changes the state to unlocked\n    and returns immediately.  If an attempt is made to release an\n    unlocked lock, a RuntimeError will be raised.\n\n    When more than one coroutine is blocked in acquire() waiting for\n    the state to turn to unlocked, only one coroutine proceeds when a\n    release() call resets the state to unlocked; first coroutine which\n    is blocked in acquire() is being processed.\n\n    acquire() is a coroutine and should be called with 'await'.\n\n    Locks also support the asynchronous context management protocol.\n    'async with lock' statement should be used.\n\n    Usage:\n\n        lock = Lock()\n        ...\n        await lock.acquire()\n        try:\n            ...\n        finally:\n            lock.release()\n\n    Context manager usage:\n\n        lock = Lock()\n        ...\n        async with lock:\n             ...\n\n    Lock objects can be tested for locking state:\n\n        if not lock.locked():\n           await lock.acquire()\n        else:\n           # lock is acquired\n           ...\n\n    "

    def __init__(self, *, loop=None):
        self._waiters = None
        self._locked = False
        if loop is None:
            self._loop = events.get_event_loop()
        else:
            self._loop = loop
            warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
              stacklevel=2)

    def __repr__(self):
        res = super().__repr__()
        extra = 'locked' if self._locked else 'unlocked'
        if self._waiters:
            extra = f"{extra}, waiters:{len(self._waiters)}"
        return f"<{res[1:-1]} [{extra}]>"

    def locked(self):
        """Return True if lock is acquired."""
        return self._locked

    async def acquire(self):
        """Acquire a lock.

        This method blocks until the lock is unlocked, then sets it to
        locked and returns True.
        """
        if not self._locked:
            if self._waiters is None or (all((w.cancelled() for w in self._waiters))):
                self._locked = True
                return True
            if self._waiters is None:
                self._waiters = collections.deque()
            fut = self._loop.create_future()
            self._waiters.append(fut)
            try:
                try:
                    await fut
                finally:
                    self._waiters.remove(fut)

            except exceptions.CancelledError:
                if not self._locked:
                    self._wake_up_first()
                else:
                    raise
            else:
                self._locked = True
            return True

    def release(self):
        """Release a lock.

        When the lock is locked, reset it to unlocked, and return.
        If any other coroutines are blocked waiting for the lock to become
        unlocked, allow exactly one of them to proceed.

        When invoked on an unlocked lock, a RuntimeError is raised.

        There is no return value.
        """
        if self._locked:
            self._locked = False
            self._wake_up_first()
        else:
            raise RuntimeError('Lock is not acquired.')

    def _wake_up_first(self):
        """Wake up the first waiter if it isn't done."""
        if not self._waiters:
            return
        try:
            fut = next(iter(self._waiters))
        except StopIteration:
            return
        else:
            if not fut.done():
                fut.set_result(True)


class Event:
    __doc__ = 'Asynchronous equivalent to threading.Event.\n\n    Class implementing event objects. An event manages a flag that can be set\n    to true with the set() method and reset to false with the clear() method.\n    The wait() method blocks until the flag is true. The flag is initially\n    false.\n    '

    def __init__(self, *, loop=None):
        self._waiters = collections.deque()
        self._value = False
        if loop is None:
            self._loop = events.get_event_loop()
        else:
            self._loop = loop
            warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
              stacklevel=2)

    def __repr__(self):
        res = super().__repr__()
        extra = 'set' if self._value else 'unset'
        if self._waiters:
            extra = f"{extra}, waiters:{len(self._waiters)}"
        return f"<{res[1:-1]} [{extra}]>"

    def is_set(self):
        """Return True if and only if the internal flag is true."""
        return self._value

    def set(self):
        """Set the internal flag to true. All coroutines waiting for it to
        become true are awakened. Coroutine that call wait() once the flag is
        true will not block at all.
        """
        if not self._value:
            self._value = True
            for fut in self._waiters:
                if not fut.done():
                    fut.set_result(True)

    def clear(self):
        """Reset the internal flag to false. Subsequently, coroutines calling
        wait() will block until set() is called to set the internal flag
        to true again."""
        self._value = False

    async def wait--- This code section failed: ---

 L. 303         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _value
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 304         6  LOAD_CONST               True
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 306        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _loop
               14  LOAD_METHOD              create_future
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'fut'

 L. 307        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _waiters
               24  LOAD_METHOD              append
               26  LOAD_FAST                'fut'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 308        32  SETUP_FINALLY        52  'to 52'

 L. 309        34  LOAD_FAST                'fut'
               36  GET_AWAITABLE    
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  POP_TOP          

 L. 310        44  POP_BLOCK        
               46  CALL_FINALLY         52  'to 52'
               48  LOAD_CONST               True
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'
             52_1  COME_FROM_FINALLY    32  '32'

 L. 312        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _waiters
               56  LOAD_METHOD              remove
               58  LOAD_FAST                'fut'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          
               64  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 46


class Condition(_ContextManagerMixin):
    __doc__ = 'Asynchronous equivalent to threading.Condition.\n\n    This class implements condition variable objects. A condition variable\n    allows one or more coroutines to wait until they are notified by another\n    coroutine.\n\n    A new Lock object is created and used as the underlying lock.\n    '

    def __init__(self, lock=None, *, loop=None):
        if loop is None:
            self._loop = events.get_event_loop()
        else:
            self._loop = loop
            warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
              stacklevel=2)
        if lock is None:
            lock = Lock(loop=loop)
        elif lock._loop is not self._loop:
            raise ValueError('loop argument must agree with lock')
        self._lock = lock
        self.locked = lock.locked
        self.acquire = lock.acquire
        self.release = lock.release
        self._waiters = collections.deque()

    def __repr__(self):
        res = super().__repr__()
        extra = 'locked' if self.locked() else 'unlocked'
        if self._waiters:
            extra = f"{extra}, waiters:{len(self._waiters)}"
        return f"<{res[1:-1]} [{extra}]>"

    async def wait--- This code section failed: ---

 L. 365         0  LOAD_FAST                'self'
                2  LOAD_METHOD              locked
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L. 366         8  LOAD_GLOBAL              RuntimeError
               10  LOAD_STR                 'cannot wait on un-acquired lock'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 368        16  LOAD_FAST                'self'
               18  LOAD_METHOD              release
               20  CALL_METHOD_0         0  ''
               22  POP_TOP          

 L. 369        24  SETUP_FINALLY        90  'to 90'

 L. 370        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _loop
               30  LOAD_METHOD              create_future
               32  CALL_METHOD_0         0  ''
               34  STORE_FAST               'fut'

 L. 371        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _waiters
               40  LOAD_METHOD              append
               42  LOAD_FAST                'fut'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 372        48  SETUP_FINALLY        72  'to 72'

 L. 373        50  LOAD_FAST                'fut'
               52  GET_AWAITABLE    
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  POP_TOP          

 L. 374        60  POP_BLOCK        
               62  CALL_FINALLY         72  'to 72'
               64  POP_BLOCK        
               66  CALL_FINALLY         90  'to 90'
               68  LOAD_CONST               True
               70  RETURN_VALUE     
             72_0  COME_FROM            62  '62'
             72_1  COME_FROM_FINALLY    48  '48'

 L. 376        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _waiters
               76  LOAD_METHOD              remove
               78  LOAD_FAST                'fut'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  END_FINALLY      
               86  POP_BLOCK        
               88  BEGIN_FINALLY    
             90_0  COME_FROM            66  '66'
             90_1  COME_FROM_FINALLY    24  '24'

 L. 380        90  LOAD_CONST               False
               92  STORE_FAST               'cancelled'
             94_0  COME_FROM           144  '144'
             94_1  COME_FROM           140  '140'
             94_2  COME_FROM           116  '116'

 L. 382        94  SETUP_FINALLY       118  'to 118'

 L. 383        96  LOAD_FAST                'self'
               98  LOAD_METHOD              acquire
              100  CALL_METHOD_0         0  ''
              102  GET_AWAITABLE    
              104  LOAD_CONST               None
              106  YIELD_FROM       
              108  POP_TOP          

 L. 384       110  POP_BLOCK        
              112  BREAK_LOOP          146  'to 146'
              114  POP_BLOCK        
              116  JUMP_BACK            94  'to 94'
            118_0  COME_FROM_FINALLY    94  '94'

 L. 385       118  DUP_TOP          
              120  LOAD_GLOBAL              exceptions
              122  LOAD_ATTR                CancelledError
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   142  'to 142'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 386       134  LOAD_CONST               True
              136  STORE_FAST               'cancelled'
              138  POP_EXCEPT       
              140  JUMP_BACK            94  'to 94'
            142_0  COME_FROM           126  '126'
              142  END_FINALLY      
              144  JUMP_BACK            94  'to 94'
            146_0  COME_FROM           112  '112'

 L. 388       146  LOAD_FAST                'cancelled'
              148  POP_JUMP_IF_FALSE   156  'to 156'

 L. 389       150  LOAD_GLOBAL              exceptions
              152  LOAD_ATTR                CancelledError
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           148  '148'
              156  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 62

    async def wait_for(self, predicate):
        """Wait until a predicate becomes true.

        The predicate should be a callable which result will be
        interpreted as a boolean value.  The final predicate value is
        the return value.
        """
        result = predicate()
        while True:
            if not result:
                await self.wait()
                result = predicate()

        return result

    def notify--- This code section failed: ---

 L. 416         0  LOAD_FAST                'self'
                2  LOAD_METHOD              locked
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L. 417         8  LOAD_GLOBAL              RuntimeError
               10  LOAD_STR                 'cannot notify on un-acquired lock'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 419        16  LOAD_CONST               0
               18  STORE_FAST               'idx'

 L. 420        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _waiters
               24  GET_ITER         
             26_0  COME_FROM            68  '68'
             26_1  COME_FROM            48  '48'
               26  FOR_ITER             70  'to 70'
               28  STORE_FAST               'fut'

 L. 421        30  LOAD_FAST                'idx'
               32  LOAD_FAST                'n'
               34  COMPARE_OP               >=
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 422        38  POP_TOP          
               40  BREAK_LOOP           70  'to 70'
             42_0  COME_FROM            36  '36'

 L. 424        42  LOAD_FAST                'fut'
               44  LOAD_METHOD              done
               46  CALL_METHOD_0         0  ''
               48  POP_JUMP_IF_TRUE_BACK    26  'to 26'

 L. 425        50  LOAD_FAST                'idx'
               52  LOAD_CONST               1
               54  INPLACE_ADD      
               56  STORE_FAST               'idx'

 L. 426        58  LOAD_FAST                'fut'
               60  LOAD_METHOD              set_result
               62  LOAD_CONST               False
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
               68  JUMP_BACK            26  'to 26'
             70_0  COME_FROM            40  '40'
             70_1  COME_FROM            26  '26'

Parse error at or near `COME_FROM' instruction at offset 70_0

    def notify_all(self):
        """Wake up all threads waiting on this condition. This method acts
        like notify(), but wakes up all waiting threads instead of one. If the
        calling thread has not acquired the lock when this method is called,
        a RuntimeError is raised.
        """
        self.notify(len(self._waiters))


class Semaphore(_ContextManagerMixin):
    __doc__ = 'A Semaphore implementation.\n\n    A semaphore manages an internal counter which is decremented by each\n    acquire() call and incremented by each release() call. The counter\n    can never go below zero; when acquire() finds that it is zero, it blocks,\n    waiting until some other thread calls release().\n\n    Semaphores also support the context management protocol.\n\n    The optional argument gives the initial value for the internal\n    counter; it defaults to 1. If the value given is less than 0,\n    ValueError is raised.\n    '

    def __init__(self, value=1, *, loop=None):
        if value < 0:
            raise ValueError('Semaphore initial value must be >= 0')
        self._value = value
        self._waiters = collections.deque()
        if loop is None:
            self._loop = events.get_event_loop()
        else:
            self._loop = loop
            warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
              stacklevel=2)

    def __repr__(self):
        res = super().__repr__()
        extra = 'locked' if self.locked() else f"unlocked, value:{self._value}"
        if self._waiters:
            extra = f"{extra}, waiters:{len(self._waiters)}"
        return f"<{res[1:-1]} [{extra}]>"

    def _wake_up_next(self):
        while True:
            if self._waiters:
                waiter = self._waiters.popleft()
                if not waiter.done():
                    waiter.set_result(None)
                return

    def locked(self):
        """Returns True if semaphore can not be acquired immediately."""
        return self._value == 0

    async def acquire--- This code section failed: ---
              0_0  COME_FROM            96  '96'
              0_1  COME_FROM            92  '92'
              0_2  COME_FROM            46  '46'

 L. 492         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _value
                4  LOAD_CONST               0
                6  COMPARE_OP               <=
                8  POP_JUMP_IF_FALSE    98  'to 98'

 L. 493        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _loop
               14  LOAD_METHOD              create_future
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'fut'

 L. 494        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _waiters
               24  LOAD_METHOD              append
               26  LOAD_FAST                'fut'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 495        32  SETUP_FINALLY        48  'to 48'

 L. 496        34  LOAD_FAST                'fut'
               36  GET_AWAITABLE    
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  POP_TOP          
               44  POP_BLOCK        
               46  JUMP_BACK             0  'to 0'
             48_0  COME_FROM_FINALLY    32  '32'

 L. 497        48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 499        54  LOAD_FAST                'fut'
               56  LOAD_METHOD              cancel
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          

 L. 500        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _value
               66  LOAD_CONST               0
               68  COMPARE_OP               >
               70  POP_JUMP_IF_FALSE    88  'to 88'
               72  LOAD_FAST                'fut'
               74  LOAD_METHOD              cancelled
               76  CALL_METHOD_0         0  ''
               78  POP_JUMP_IF_TRUE     88  'to 88'

 L. 501        80  LOAD_FAST                'self'
               82  LOAD_METHOD              _wake_up_next
               84  CALL_METHOD_0         0  ''
               86  POP_TOP          
             88_0  COME_FROM            78  '78'
             88_1  COME_FROM            70  '70'

 L. 502        88  RAISE_VARARGS_0       0  'reraise'
               90  POP_EXCEPT       
               92  JUMP_BACK             0  'to 0'
               94  END_FINALLY      
               96  JUMP_BACK             0  'to 0'
             98_0  COME_FROM             8  '8'

 L. 503        98  LOAD_FAST                'self'
              100  DUP_TOP          
              102  LOAD_ATTR                _value
              104  LOAD_CONST               1
              106  INPLACE_SUBTRACT 
              108  ROT_TWO          
              110  STORE_ATTR               _value

 L. 504       112  LOAD_CONST               True
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 92

    def release(self):
        """Release a semaphore, incrementing the internal counter by one.
        When it was zero on entry and another coroutine is waiting for it to
        become larger than zero again, wake up that coroutine.
        """
        self._value += 1
        self._wake_up_next()


class BoundedSemaphore(Semaphore):
    __doc__ = 'A bounded semaphore implementation.\n\n    This raises ValueError in release() if it would increase the value\n    above the initial value.\n    '

    def __init__(self, value=1, *, loop=None):
        if loop:
            warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
              stacklevel=2)
        self._bound_value = value
        super().__init__(value, loop=loop)

    def release(self):
        if self._value >= self._bound_value:
            raise ValueError('BoundedSemaphore released too many times')
        super().release()