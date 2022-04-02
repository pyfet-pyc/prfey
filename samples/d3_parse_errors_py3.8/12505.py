# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: concurrent\futures\_base.py
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
import collections, logging, threading, time
FIRST_COMPLETED = 'FIRST_COMPLETED'
FIRST_EXCEPTION = 'FIRST_EXCEPTION'
ALL_COMPLETED = 'ALL_COMPLETED'
_AS_COMPLETED = '_AS_COMPLETED'
PENDING = 'PENDING'
RUNNING = 'RUNNING'
CANCELLED = 'CANCELLED'
CANCELLED_AND_NOTIFIED = 'CANCELLED_AND_NOTIFIED'
FINISHED = 'FINISHED'
_FUTURE_STATES = [
 PENDING,
 RUNNING,
 CANCELLED,
 CANCELLED_AND_NOTIFIED,
 FINISHED]
_STATE_TO_DESCRIPTION_MAP = {PENDING: 'pending', 
 RUNNING: 'running', 
 CANCELLED: 'cancelled', 
 CANCELLED_AND_NOTIFIED: 'cancelled', 
 FINISHED: 'finished'}
LOGGER = logging.getLogger('concurrent.futures')

class Error(Exception):
    __doc__ = 'Base class for all future-related exceptions.'


class CancelledError(Error):
    __doc__ = 'The Future was cancelled.'


class TimeoutError(Error):
    __doc__ = 'The operation exceeded the given deadline.'


class InvalidStateError(Error):
    __doc__ = 'The operation is not allowed in this state.'


class _Waiter(object):
    __doc__ = 'Provides the event that wait() and as_completed() block on.'

    def __init__(self):
        self.event = threading.Event()
        self.finished_futures = []

    def add_result(self, future):
        self.finished_futures.append(future)

    def add_exception(self, future):
        self.finished_futures.append(future)

    def add_cancelled(self, future):
        self.finished_futures.append(future)


class _AsCompletedWaiter(_Waiter):
    __doc__ = 'Used by as_completed().'

    def __init__(self):
        super(_AsCompletedWaiter, self).__init__()
        self.lock = threading.Lock()

    def add_result(self, future):
        with self.lock:
            super(_AsCompletedWaiter, self).add_result(future)
            self.event.set()

    def add_exception(self, future):
        with self.lock:
            super(_AsCompletedWaiter, self).add_exception(future)
            self.event.set()

    def add_cancelled(self, future):
        with self.lock:
            super(_AsCompletedWaiter, self).add_cancelled(future)
            self.event.set()


class _FirstCompletedWaiter(_Waiter):
    __doc__ = 'Used by wait(return_when=FIRST_COMPLETED).'

    def add_result(self, future):
        super().add_result(future)
        self.event.set()

    def add_exception(self, future):
        super().add_exception(future)
        self.event.set()

    def add_cancelled(self, future):
        super().add_cancelled(future)
        self.event.set()


class _AllCompletedWaiter(_Waiter):
    __doc__ = 'Used by wait(return_when=FIRST_EXCEPTION and ALL_COMPLETED).'

    def __init__(self, num_pending_calls, stop_on_exception):
        self.num_pending_calls = num_pending_calls
        self.stop_on_exception = stop_on_exception
        self.lock = threading.Lock()
        super().__init__()

    def _decrement_pending_calls(self):
        with self.lock:
            self.num_pending_calls -= 1
            if not self.num_pending_calls:
                self.event.set()

    def add_result(self, future):
        super().add_result(future)
        self._decrement_pending_calls()

    def add_exception(self, future):
        super().add_exception(future)
        if self.stop_on_exception:
            self.event.set()
        else:
            self._decrement_pending_calls()

    def add_cancelled(self, future):
        super().add_cancelled(future)
        self._decrement_pending_calls()


class _AcquireFutures(object):
    __doc__ = 'A context manager that does an ordered acquire of Future conditions.'

    def __init__(self, futures):
        self.futures = sorted(futures, key=id)

    def __enter__(self):
        for future in self.futures:
            future._condition.acquire()

    def __exit__(self, *args):
        for future in self.futures:
            future._condition.release()


def _create_and_install_waiters(fs, return_when):
    if return_when == _AS_COMPLETED:
        waiter = _AsCompletedWaiter()
    elif return_when == FIRST_COMPLETED:
        waiter = _FirstCompletedWaiter()
    else:
        pending_count = sum((f._state not in (CANCELLED_AND_NOTIFIED, FINISHED) for f in fs))
        if return_when == FIRST_EXCEPTION:
            waiter = _AllCompletedWaiter(pending_count, stop_on_exception=True)
        elif return_when == ALL_COMPLETED:
            waiter = _AllCompletedWaiter(pending_count, stop_on_exception=False)
        else:
            raise ValueError('Invalid return condition: %r' % return_when)
    for f in fs:
        f._waiters.append(waiter)
    else:
        return waiter


def _yield_finished_futures(fs, waiter, ref_collect):
    """
    Iterate on the list *fs*, yielding finished futures one by one in
    reverse order.
    Before yielding a future, *waiter* is removed from its waiters
    and the future is removed from each set in the collection of sets
    *ref_collect*.

    The aim of this function is to avoid keeping stale references after
    the future is yielded and before the iterator resumes.
    """
    while True:
        if fs:
            f = fs[(-1)]
            for futures_set in ref_collect:
                futures_set.remove(f)
            else:
                with f._condition:
                    f._waiters.remove(waiter)
                del f
                yield fs.pop()


def as_completed(fs, timeout=None):
    """An iterator over the given futures that yields each as it completes.

    Args:
        fs: The sequence of Futures (possibly created by different Executors) to
            iterate over.
        timeout: The maximum number of seconds to wait. If None, then there
            is no limit on the wait time.

    Returns:
        An iterator that yields the given Futures as they complete (finished or
        cancelled). If any given Futures are duplicated, they will be returned
        once.

    Raises:
        TimeoutError: If the entire result iterator could not be generated
            before the given timeout.
    """
    if timeout is not None:
        end_time = timeout + time.monotonic()
    fs = set(fs)
    total_futures = len(fs)
    with _AcquireFutures(fs):
        finished = set((f for f in fs if f._state in (CANCELLED_AND_NOTIFIED, FINISHED)))
        pending = fs - finished
        waiter = _create_and_install_waiters(fs, _AS_COMPLETED)
    finished = list(finished)
    try:
        yield from _yield_finished_futures(finished, waiter, ref_collect=(
         fs,))
        while True:
            if pending:
                if timeout is None:
                    wait_timeout = None
                else:
                    wait_timeout = end_time - time.monotonic()
                    if wait_timeout < 0:
                        raise TimeoutError('%d (of %d) futures unfinished' % (
                         len(pending), total_futures))
                waiter.event.wait(wait_timeout)
                with waiter.lock:
                    finished = waiter.finished_futures
                    waiter.finished_futures = []
                    waiter.event.clear()
                finished.reverse()
                yield from _yield_finished_futures(finished, waiter, ref_collect=(
                 fs, pending))

    finally:
        for f in fs:
            with f._condition:
                f._waiters.remove(waiter)

    if False:
        yield None


DoneAndNotDoneFutures = collections.namedtuple('DoneAndNotDoneFutures', 'done not_done')

def wait(fs, timeout=None, return_when=ALL_COMPLETED):
    """Wait for the futures in the given sequence to complete.

    Args:
        fs: The sequence of Futures (possibly created by different Executors) to
            wait upon.
        timeout: The maximum number of seconds to wait. If None, then there
            is no limit on the wait time.
        return_when: Indicates when this function should return. The options
            are:

            FIRST_COMPLETED - Return when any future finishes or is
                              cancelled.
            FIRST_EXCEPTION - Return when any future finishes by raising an
                              exception. If no future raises an exception
                              then it is equivalent to ALL_COMPLETED.
            ALL_COMPLETED -   Return when all futures finish or are cancelled.

    Returns:
        A named 2-tuple of sets. The first set, named 'done', contains the
        futures that completed (is finished or cancelled) before the wait
        completed. The second set, named 'not_done', contains uncompleted
        futures.
    """
    with _AcquireFutures(fs):
        done = set((f for f in fs if f._state in (CANCELLED_AND_NOTIFIED, FINISHED)))
        not_done = set(fs) - done
        if return_when == FIRST_COMPLETED:
            if done:
                return DoneAndNotDoneFutures(done, not_done)
        if return_when == FIRST_EXCEPTION:
            if done:
                if any((f for f in done if not f.cancelled() if f.exception() is not None)):
                    return DoneAndNotDoneFutures(done, not_done)
        if len(done) == len(fs):
            return DoneAndNotDoneFutures(done, not_done)
        waiter = _create_and_install_waiters(fs, return_when)
    waiter.event.wait(timeout)
    for f in fs:
        with f._condition:
            f._waiters.remove(waiter)
    else:
        done.update(waiter.finished_futures)
        return DoneAndNotDoneFutures(done, set(fs) - done)


class Future(object):
    __doc__ = 'Represents the result of an asynchronous computation.'

    def __init__(self):
        """Initializes the future. Should not be called by clients."""
        self._condition = threading.Condition()
        self._state = PENDING
        self._result = None
        self._exception = None
        self._waiters = []
        self._done_callbacks = []

    def _invoke_callbacks(self):
        for callback in self._done_callbacks:
            try:
                callback(self)
            except Exception:
                LOGGER.exception('exception calling callback for %r', self)

    def __repr__(self):
        with self._condition:
            if self._state == FINISHED:
                if self._exception:
                    return '<%s at %#x state=%s raised %s>' % (
                     self.__class__.__name__,
                     id(self),
                     _STATE_TO_DESCRIPTION_MAP[self._state],
                     self._exception.__class__.__name__)
                return '<%s at %#x state=%s returned %s>' % (
                 self.__class__.__name__,
                 id(self),
                 _STATE_TO_DESCRIPTION_MAP[self._state],
                 self._result.__class__.__name__)
            return '<%s at %#x state=%s>' % (
             self.__class__.__name__,
             id(self),
             _STATE_TO_DESCRIPTION_MAP[self._state])

    def cancel--- This code section failed: ---

 L. 358         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH           84  'to 84'
                6  POP_TOP          

 L. 359         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              RUNNING
               14  LOAD_GLOBAL              FINISHED
               16  BUILD_TUPLE_2         2 
               18  COMPARE_OP               in
               20  POP_JUMP_IF_FALSE    36  'to 36'

 L. 360        22  POP_BLOCK        
               24  BEGIN_FINALLY    
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  POP_FINALLY           0  ''
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            20  '20'

 L. 362        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _state
               40  LOAD_GLOBAL              CANCELLED
               42  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               in
               48  POP_JUMP_IF_FALSE    64  'to 64'

 L. 363        50  POP_BLOCK        
               52  BEGIN_FINALLY    
               54  WITH_CLEANUP_START
               56  WITH_CLEANUP_FINISH
               58  POP_FINALLY           0  ''
               60  LOAD_CONST               True
               62  RETURN_VALUE     
             64_0  COME_FROM            48  '48'

 L. 365        64  LOAD_GLOBAL              CANCELLED
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _state

 L. 366        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _condition
               74  LOAD_METHOD              notify_all
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH        4  '4'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      

 L. 368        90  LOAD_FAST                'self'
               92  LOAD_METHOD              _invoke_callbacks
               94  CALL_METHOD_0         0  ''
               96  POP_TOP          

 L. 369        98  LOAD_CONST               True
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def cancelled(self):
        """Return True if the future was cancelled."""
        with self._condition:
            return self._state in (CANCELLED, CANCELLED_AND_NOTIFIED)

    def running(self):
        """Return True if the future is currently executing."""
        with self._condition:
            return self._state == RUNNING

    def done(self):
        """Return True of the future was cancelled or finished executing."""
        with self._condition:
            return self._state in (CANCELLED, CANCELLED_AND_NOTIFIED, FINISHED)

    def __get_result(self):
        if self._exception:
            try:
                raise self._exception
            finally:
                self = None

        else:
            return self._result

    def add_done_callback--- This code section failed: ---

 L. 407         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH           54  'to 54'
                6  POP_TOP          

 L. 408         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              CANCELLED
               14  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               16  LOAD_GLOBAL              FINISHED
               18  BUILD_TUPLE_3         3 
               20  COMPARE_OP               not-in
               22  POP_JUMP_IF_FALSE    50  'to 50'

 L. 409        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _done_callbacks
               28  LOAD_METHOD              append
               30  LOAD_FAST                'fn'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 410        36  POP_BLOCK        
               38  BEGIN_FINALLY    
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  POP_FINALLY           0  ''
               46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            22  '22'
               50  POP_BLOCK        
               52  BEGIN_FINALLY    
             54_0  COME_FROM_WITH        4  '4'
               54  WITH_CLEANUP_START
               56  WITH_CLEANUP_FINISH
               58  END_FINALLY      

 L. 411        60  SETUP_FINALLY        74  'to 74'

 L. 412        62  LOAD_FAST                'fn'
               64  LOAD_FAST                'self'
               66  CALL_FUNCTION_1       1  ''
               68  POP_TOP          
               70  POP_BLOCK        
               72  JUMP_FORWARD        106  'to 106'
             74_0  COME_FROM_FINALLY    60  '60'

 L. 413        74  DUP_TOP          
               76  LOAD_GLOBAL              Exception
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   104  'to 104'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 414        88  LOAD_GLOBAL              LOGGER
               90  LOAD_METHOD              exception
               92  LOAD_STR                 'exception calling callback for %r'
               94  LOAD_FAST                'self'
               96  CALL_METHOD_2         2  ''
               98  POP_TOP          
              100  POP_EXCEPT       
              102  JUMP_FORWARD        106  'to 106'
            104_0  COME_FROM            80  '80'
              104  END_FINALLY      
            106_0  COME_FROM           102  '102'
            106_1  COME_FROM            72  '72'

Parse error at or near `BEGIN_FINALLY' instruction at offset 38

    def result--- This code section failed: ---

 L. 432         0  SETUP_FINALLY       154  'to 154'

 L. 433         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _condition
                6  SETUP_WITH          144  'to 144'
                8  POP_TOP          

 L. 434        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _state
               14  LOAD_GLOBAL              CANCELLED
               16  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               18  BUILD_TUPLE_2         2 
               20  COMPARE_OP               in
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 435        24  LOAD_GLOBAL              CancelledError
               26  CALL_FUNCTION_0       0  ''
               28  RAISE_VARARGS_1       1  'exception instance'
               30  JUMP_FORWARD         66  'to 66'
             32_0  COME_FROM            22  '22'

 L. 436        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _state
               36  LOAD_GLOBAL              FINISHED
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    66  'to 66'

 L. 437        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _Future__get_result
               46  CALL_METHOD_0         0  ''
               48  POP_BLOCK        
               50  ROT_TWO          
               52  BEGIN_FINALLY    
               54  WITH_CLEANUP_START
               56  WITH_CLEANUP_FINISH
               58  POP_FINALLY           0  ''
               60  POP_BLOCK        
               62  CALL_FINALLY        154  'to 154'
               64  RETURN_VALUE     
             66_0  COME_FROM            40  '40'
             66_1  COME_FROM            30  '30'

 L. 439        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _condition
               70  LOAD_METHOD              wait
               72  LOAD_FAST                'timeout'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 441        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _state
               82  LOAD_GLOBAL              CANCELLED
               84  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               86  BUILD_TUPLE_2         2 
               88  COMPARE_OP               in
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 442        92  LOAD_GLOBAL              CancelledError
               94  CALL_FUNCTION_0       0  ''
               96  RAISE_VARARGS_1       1  'exception instance'
               98  JUMP_FORWARD        140  'to 140'
            100_0  COME_FROM            90  '90'

 L. 443       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _state
              104  LOAD_GLOBAL              FINISHED
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   134  'to 134'

 L. 444       110  LOAD_FAST                'self'
              112  LOAD_METHOD              _Future__get_result
              114  CALL_METHOD_0         0  ''
              116  POP_BLOCK        
              118  ROT_TWO          
              120  BEGIN_FINALLY    
              122  WITH_CLEANUP_START
              124  WITH_CLEANUP_FINISH
              126  POP_FINALLY           0  ''
              128  POP_BLOCK        
              130  CALL_FINALLY        154  'to 154'
              132  RETURN_VALUE     
            134_0  COME_FROM           108  '108'

 L. 446       134  LOAD_GLOBAL              TimeoutError
              136  CALL_FUNCTION_0       0  ''
              138  RAISE_VARARGS_1       1  'exception instance'
            140_0  COME_FROM            98  '98'
              140  POP_BLOCK        
              142  BEGIN_FINALLY    
            144_0  COME_FROM_WITH        6  '6'
              144  WITH_CLEANUP_START
              146  WITH_CLEANUP_FINISH
              148  END_FINALLY      
              150  POP_BLOCK        
              152  BEGIN_FINALLY    
            154_0  COME_FROM           130  '130'
            154_1  COME_FROM            62  '62'
            154_2  COME_FROM_FINALLY     0  '0'

 L. 449       154  LOAD_CONST               None
              156  STORE_FAST               'self'
              158  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 60

    def exception(self, timeout=None):
        """Return the exception raised by the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the exception if the
                future isn't done. If None, then there is no limit on the wait
                time.

        Returns:
            The exception raised by the call that the future represents or None
            if the call completed without raising.

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the given
                timeout.
        """
        with self._condition:
            if self._state in (CANCELLED, CANCELLED_AND_NOTIFIED):
                raise CancelledError()
            elif self._state == FINISHED:
                return self._exception
            self._condition.wait(timeout)
            if self._state in (CANCELLED, CANCELLED_AND_NOTIFIED):
                raise CancelledError()
            else:
                if self._state == FINISHED:
                    return self._exception
                raise TimeoutError()

    def set_running_or_notify_cancel--- This code section failed: ---

 L. 508         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH          122  'to 122'
                6  POP_TOP          

 L. 509         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              CANCELLED
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE    60  'to 60'

 L. 510        18  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _state

 L. 511        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _waiters
               28  GET_ITER         
             30_0  COME_FROM            44  '44'
               30  FOR_ITER             46  'to 46'
               32  STORE_FAST               'waiter'

 L. 512        34  LOAD_FAST                'waiter'
               36  LOAD_METHOD              add_cancelled
               38  LOAD_FAST                'self'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
               44  JUMP_BACK            30  'to 30'
             46_0  COME_FROM            30  '30'

 L. 515        46  POP_BLOCK        
               48  BEGIN_FINALLY    
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  POP_FINALLY           0  ''
               56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            16  '16'

 L. 516        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _state
               64  LOAD_GLOBAL              PENDING
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    90  'to 90'

 L. 517        70  LOAD_GLOBAL              RUNNING
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _state

 L. 518        76  POP_BLOCK        
               78  BEGIN_FINALLY    
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  POP_FINALLY           0  ''
               86  LOAD_CONST               True
               88  RETURN_VALUE     
             90_0  COME_FROM            68  '68'

 L. 520        90  LOAD_GLOBAL              LOGGER
               92  LOAD_METHOD              critical
               94  LOAD_STR                 'Future %s in unexpected state: %s'

 L. 521        96  LOAD_GLOBAL              id
               98  LOAD_FAST                'self'
              100  CALL_FUNCTION_1       1  ''

 L. 522       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _state

 L. 520       106  CALL_METHOD_3         3  ''
              108  POP_TOP          

 L. 523       110  LOAD_GLOBAL              RuntimeError
              112  LOAD_STR                 'Future in unexpected state'
              114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM_WITH        4  '4'
              122  WITH_CLEANUP_START
              124  WITH_CLEANUP_FINISH
              126  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 48

    def set_result(self, result):
        """Sets the return value of work associated with the future.

        Should only be used by Executor implementations and unit tests.
        """
        with self._condition:
            if self._state in {CANCELLED, CANCELLED_AND_NOTIFIED, FINISHED}:
                raise InvalidStateError('{}: {!r}'.format(self._state, self))
            self._result = result
            self._state = FINISHED
            for waiter in self._waiters:
                waiter.add_result(self)
            else:
                self._condition.notify_all()

        self._invoke_callbacks()

    def set_exception(self, exception):
        """Sets the result of the future as being the given exception.

        Should only be used by Executor implementations and unit tests.
        """
        with self._condition:
            if self._state in {CANCELLED, CANCELLED_AND_NOTIFIED, FINISHED}:
                raise InvalidStateError('{}: {!r}'.format(self._state, self))
            self._exception = exception
            self._state = FINISHED
            for waiter in self._waiters:
                waiter.add_exception(self)
            else:
                self._condition.notify_all()

        self._invoke_callbacks()


class Executor(object):
    __doc__ = 'This is an abstract base class for concrete asynchronous executors.'

    def submit(*args, **kwargs):
        """Submits a callable to be executed with the given arguments.

        Schedules the callable to be executed as fn(*args, **kwargs) and returns
        a Future instance representing the execution of the callable.

        Returns:
            A Future representing the given call.
        """
        if len(args) >= 2:
            pass
        elif not args:
            raise TypeError("descriptor 'submit' of 'Executor' object needs an argument")
        elif 'fn' in kwargs:
            import warnings
            warnings.warn("Passing 'fn' as keyword argument is deprecated", DeprecationWarning,
              stacklevel=2)
        else:
            raise TypeError('submit expected at least 1 positional argument, got %d' % (len(args) - 1))
        raise NotImplementedError()

    submit.__text_signature__ = '($self, fn, /, *args, **kwargs)'

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        """Returns an iterator equivalent to map(fn, iter).

        Args:
            fn: A callable that will take as many arguments as there are
                passed iterables.
            timeout: The maximum number of seconds to wait. If None, then there
                is no limit on the wait time.
            chunksize: The size of the chunks the iterable will be broken into
                before being passed to a child process. This argument is only
                used by ProcessPoolExecutor; it is ignored by
                ThreadPoolExecutor.

        Returns:
            An iterator equivalent to: map(func, *iterables) but the calls may
            be evaluated out-of-order.

        Raises:
            TimeoutError: If the entire result iterator could not be generated
                before the given timeout.
            Exception: If fn(*args) raises for any values.
        """
        if timeout is not None:
            end_time = timeout + time.monotonic()
        fs = [(self.submit)(fn, *args) for args in zip(*iterables)]

        def result_iterator():
            try:
                fs.reverse()
                while True:
                    if fs:
                        if timeout is None:
                            yield fs.pop().result()
                        else:
                            yield fs.pop().result(end_time - time.monotonic())

            finally:
                for future in fs:
                    future.cancel()

        return result_iterator()

    def shutdown(self, wait=True):
        """Clean-up the resources associated with the Executor.

        It is safe to call this method several times. Otherwise, no other
        methods can be called after this one.

        Args:
            wait: If True then shutdown will not return until all running
                futures have finished executing and the resources used by the
                executor have been reclaimed.
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False


class BrokenExecutor(RuntimeError):
    __doc__ = '\n    Raised when a executor has become non-functional after a severe failure.\n    '