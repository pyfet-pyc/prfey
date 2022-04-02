# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
    else:
        if return_when == FIRST_COMPLETED:
            waiter = _FirstCompletedWaiter()
        else:
            pending_count = sum((f._state not in (CANCELLED_AND_NOTIFIED, FINISHED) for f in fs))
            if return_when == FIRST_EXCEPTION:
                waiter = _AllCompletedWaiter(pending_count, stop_on_exception=True)
            else:
                if return_when == ALL_COMPLETED:
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
    while fs:
        f = fs[(-1)]
        for futures_set in ref_collect:
            futures_set.remove(f)
        else:
            with f._condition:
                f._waiters.remove(waiter)
            del f
            (yield fs.pop())


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
        (yield from _yield_finished_futures(finished, waiter, ref_collect=(
         fs,)))
        while pending:
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
            (yield from _yield_finished_futures(finished, waiter, ref_collect=(
             fs, pending)))

    finally:
        for f in fs:
            with f._condition:
                f._waiters.remove(waiter)

    if False:
        yield None


DoneAndNotDoneFutures = collections.namedtuple('DoneAndNotDoneFutures', 'done not_done')

def wait--- This code section failed: ---

 L. 288         0  LOAD_GLOBAL              _AcquireFutures
                2  LOAD_FAST                'fs'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH          178  'to 178'
                8  POP_TOP          

 L. 289        10  LOAD_GLOBAL              set
               12  LOAD_GENEXPR             '<code_object <genexpr>>'
               14  LOAD_STR                 'wait.<locals>.<genexpr>'
               16  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               18  LOAD_FAST                'fs'
               20  GET_ITER         
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'done'

 L. 291        28  LOAD_GLOBAL              set
               30  LOAD_FAST                'fs'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_FAST                'done'
               36  BINARY_SUBTRACT  
               38  STORE_FAST               'not_done'

 L. 293        40  LOAD_FAST                'return_when'
               42  LOAD_GLOBAL              FIRST_COMPLETED
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    74  'to 74'
               48  LOAD_FAST                'done'
               50  POP_JUMP_IF_FALSE    74  'to 74'

 L. 294        52  LOAD_GLOBAL              DoneAndNotDoneFutures
               54  LOAD_FAST                'done'
               56  LOAD_FAST                'not_done'
               58  CALL_FUNCTION_2       2  ''
               60  POP_BLOCK        
               62  ROT_TWO          
               64  BEGIN_FINALLY    
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  POP_FINALLY           0  ''
               72  RETURN_VALUE     
             74_0  COME_FROM            50  '50'
             74_1  COME_FROM            46  '46'

 L. 295        74  LOAD_FAST                'return_when'
               76  LOAD_GLOBAL              FIRST_EXCEPTION
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   126  'to 126'
               82  LOAD_FAST                'done'
               84  POP_JUMP_IF_FALSE   126  'to 126'

 L. 296        86  LOAD_GLOBAL              any
               88  LOAD_GENEXPR             '<code_object <genexpr>>'
               90  LOAD_STR                 'wait.<locals>.<genexpr>'
               92  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               94  LOAD_FAST                'done'
               96  GET_ITER         
               98  CALL_FUNCTION_1       1  ''
              100  CALL_FUNCTION_1       1  ''
              102  POP_JUMP_IF_FALSE   126  'to 126'

 L. 298       104  LOAD_GLOBAL              DoneAndNotDoneFutures
              106  LOAD_FAST                'done'
              108  LOAD_FAST                'not_done'
              110  CALL_FUNCTION_2       2  ''
              112  POP_BLOCK        
              114  ROT_TWO          
              116  BEGIN_FINALLY    
              118  WITH_CLEANUP_START
              120  WITH_CLEANUP_FINISH
              122  POP_FINALLY           0  ''
              124  RETURN_VALUE     
            126_0  COME_FROM           102  '102'
            126_1  COME_FROM            84  '84'
            126_2  COME_FROM            80  '80'

 L. 300       126  LOAD_GLOBAL              len
              128  LOAD_FAST                'done'
              130  CALL_FUNCTION_1       1  ''
              132  LOAD_GLOBAL              len
              134  LOAD_FAST                'fs'
              136  CALL_FUNCTION_1       1  ''
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   164  'to 164'

 L. 301       142  LOAD_GLOBAL              DoneAndNotDoneFutures
              144  LOAD_FAST                'done'
              146  LOAD_FAST                'not_done'
              148  CALL_FUNCTION_2       2  ''
              150  POP_BLOCK        
              152  ROT_TWO          
              154  BEGIN_FINALLY    
              156  WITH_CLEANUP_START
              158  WITH_CLEANUP_FINISH
              160  POP_FINALLY           0  ''
              162  RETURN_VALUE     
            164_0  COME_FROM           140  '140'

 L. 303       164  LOAD_GLOBAL              _create_and_install_waiters
              166  LOAD_FAST                'fs'
              168  LOAD_FAST                'return_when'
              170  CALL_FUNCTION_2       2  ''
              172  STORE_FAST               'waiter'
              174  POP_BLOCK        
              176  BEGIN_FINALLY    
            178_0  COME_FROM_WITH        6  '6'
              178  WITH_CLEANUP_START
              180  WITH_CLEANUP_FINISH
              182  END_FINALLY      

 L. 305       184  LOAD_FAST                'waiter'
              186  LOAD_ATTR                event
              188  LOAD_METHOD              wait
              190  LOAD_FAST                'timeout'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          

 L. 306       196  LOAD_FAST                'fs'
              198  GET_ITER         
              200  FOR_ITER            236  'to 236'
              202  STORE_FAST               'f'

 L. 307       204  LOAD_FAST                'f'
              206  LOAD_ATTR                _condition
              208  SETUP_WITH          228  'to 228'
              210  POP_TOP          

 L. 308       212  LOAD_FAST                'f'
              214  LOAD_ATTR                _waiters
              216  LOAD_METHOD              remove
              218  LOAD_FAST                'waiter'
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          
              224  POP_BLOCK        
              226  BEGIN_FINALLY    
            228_0  COME_FROM_WITH      208  '208'
              228  WITH_CLEANUP_START
              230  WITH_CLEANUP_FINISH
              232  END_FINALLY      
              234  JUMP_BACK           200  'to 200'

 L. 310       236  LOAD_FAST                'done'
              238  LOAD_METHOD              update
              240  LOAD_FAST                'waiter'
              242  LOAD_ATTR                finished_futures
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 311       248  LOAD_GLOBAL              DoneAndNotDoneFutures
              250  LOAD_FAST                'done'
              252  LOAD_GLOBAL              set
              254  LOAD_FAST                'fs'
              256  CALL_FUNCTION_1       1  ''
              258  LOAD_FAST                'done'
              260  BINARY_SUBTRACT  
              262  CALL_FUNCTION_2       2  ''
              264  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 62


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

    def __repr__--- This code section failed: ---

 L. 333         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH          160  'to 160'
                6  POP_TOP          

 L. 334         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              FINISHED
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE   120  'to 120'

 L. 335        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _exception
               22  POP_JUMP_IF_FALSE    72  'to 72'

 L. 336        24  LOAD_STR                 '<%s at %#x state=%s raised %s>'

 L. 337        26  LOAD_FAST                'self'
               28  LOAD_ATTR                __class__
               30  LOAD_ATTR                __name__

 L. 338        32  LOAD_GLOBAL              id
               34  LOAD_FAST                'self'
               36  CALL_FUNCTION_1       1  ''

 L. 339        38  LOAD_GLOBAL              _STATE_TO_DESCRIPTION_MAP
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _state
               44  BINARY_SUBSCR    

 L. 340        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _exception
               50  LOAD_ATTR                __class__
               52  LOAD_ATTR                __name__

 L. 336        54  BUILD_TUPLE_4         4 
               56  BINARY_MODULO    
               58  POP_BLOCK        
               60  ROT_TWO          
               62  BEGIN_FINALLY    
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  POP_FINALLY           0  ''
               70  RETURN_VALUE     
             72_0  COME_FROM            22  '22'

 L. 342        72  LOAD_STR                 '<%s at %#x state=%s returned %s>'

 L. 343        74  LOAD_FAST                'self'
               76  LOAD_ATTR                __class__
               78  LOAD_ATTR                __name__

 L. 344        80  LOAD_GLOBAL              id
               82  LOAD_FAST                'self'
               84  CALL_FUNCTION_1       1  ''

 L. 345        86  LOAD_GLOBAL              _STATE_TO_DESCRIPTION_MAP
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _state
               92  BINARY_SUBSCR    

 L. 346        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _result
               98  LOAD_ATTR                __class__
              100  LOAD_ATTR                __name__

 L. 342       102  BUILD_TUPLE_4         4 
              104  BINARY_MODULO    
              106  POP_BLOCK        
              108  ROT_TWO          
              110  BEGIN_FINALLY    
              112  WITH_CLEANUP_START
              114  WITH_CLEANUP_FINISH
              116  POP_FINALLY           0  ''
              118  RETURN_VALUE     
            120_0  COME_FROM            16  '16'

 L. 347       120  LOAD_STR                 '<%s at %#x state=%s>'

 L. 348       122  LOAD_FAST                'self'
              124  LOAD_ATTR                __class__
              126  LOAD_ATTR                __name__

 L. 349       128  LOAD_GLOBAL              id
              130  LOAD_FAST                'self'
              132  CALL_FUNCTION_1       1  ''

 L. 350       134  LOAD_GLOBAL              _STATE_TO_DESCRIPTION_MAP
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _state
              140  BINARY_SUBSCR    

 L. 347       142  BUILD_TUPLE_3         3 
              144  BINARY_MODULO    
              146  POP_BLOCK        
              148  ROT_TWO          
              150  BEGIN_FINALLY    
              152  WITH_CLEANUP_START
              154  WITH_CLEANUP_FINISH
              156  POP_FINALLY           0  ''
              158  RETURN_VALUE     
            160_0  COME_FROM_WITH        4  '4'
              160  WITH_CLEANUP_START
              162  WITH_CLEANUP_FINISH
              164  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 60

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

    def cancelled--- This code section failed: ---

 L. 373         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH           34  'to 34'
                6  POP_TOP          

 L. 374         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              CANCELLED
               14  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               16  BUILD_TUPLE_2         2 
               18  COMPARE_OP               in
               20  POP_BLOCK        
               22  ROT_TWO          
               24  BEGIN_FINALLY    
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  POP_FINALLY           0  ''
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        4  '4'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 22

    def running--- This code section failed: ---

 L. 378         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH           30  'to 30'
                6  POP_TOP          

 L. 379         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              RUNNING
               14  COMPARE_OP               ==
               16  POP_BLOCK        
               18  ROT_TWO          
               20  BEGIN_FINALLY    
               22  WITH_CLEANUP_START
               24  WITH_CLEANUP_FINISH
               26  POP_FINALLY           0  ''
               28  RETURN_VALUE     
             30_0  COME_FROM_WITH        4  '4'
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 18

    def done--- This code section failed: ---

 L. 383         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH           36  'to 36'
                6  POP_TOP          

 L. 384         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              CANCELLED
               14  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               16  LOAD_GLOBAL              FINISHED
               18  BUILD_TUPLE_3         3 
               20  COMPARE_OP               in
               22  POP_BLOCK        
               24  ROT_TWO          
               26  BEGIN_FINALLY    
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  POP_FINALLY           0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM_WITH        4  '4'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 24

    def __get_result(self):
        if self._exception:
            raise self._exception
        else:
            return self._result

    def add_done_callback--- This code section failed: ---

 L. 403         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH           54  'to 54'
                6  POP_TOP          

 L. 404         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              CANCELLED
               14  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               16  LOAD_GLOBAL              FINISHED
               18  BUILD_TUPLE_3         3 
               20  COMPARE_OP               not-in
               22  POP_JUMP_IF_FALSE    50  'to 50'

 L. 405        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _done_callbacks
               28  LOAD_METHOD              append
               30  LOAD_FAST                'fn'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 406        36  POP_BLOCK        
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

 L. 407        60  SETUP_FINALLY        74  'to 74'

 L. 408        62  LOAD_FAST                'fn'
               64  LOAD_FAST                'self'
               66  CALL_FUNCTION_1       1  ''
               68  POP_TOP          
               70  POP_BLOCK        
               72  JUMP_FORWARD        106  'to 106'
             74_0  COME_FROM_FINALLY    60  '60'

 L. 409        74  DUP_TOP          
               76  LOAD_GLOBAL              Exception
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   104  'to 104'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 410        88  LOAD_GLOBAL              LOGGER
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

 L. 428         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH          134  'to 134'
                6  POP_TOP          

 L. 429         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              CANCELLED
               14  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               16  BUILD_TUPLE_2         2 
               18  COMPARE_OP               in
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 430        22  LOAD_GLOBAL              CancelledError
               24  CALL_FUNCTION_0       0  ''
               26  RAISE_VARARGS_1       1  'exception instance'
               28  JUMP_FORWARD         60  'to 60'
             30_0  COME_FROM            20  '20'

 L. 431        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _state
               34  LOAD_GLOBAL              FINISHED
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    60  'to 60'

 L. 432        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _Future__get_result
               44  CALL_METHOD_0         0  ''
               46  POP_BLOCK        
               48  ROT_TWO          
               50  BEGIN_FINALLY    
               52  WITH_CLEANUP_START
               54  WITH_CLEANUP_FINISH
               56  POP_FINALLY           0  ''
               58  RETURN_VALUE     
             60_0  COME_FROM            38  '38'
             60_1  COME_FROM            28  '28'

 L. 434        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _condition
               64  LOAD_METHOD              wait
               66  LOAD_FAST                'timeout'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 436        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _state
               76  LOAD_GLOBAL              CANCELLED
               78  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               80  BUILD_TUPLE_2         2 
               82  COMPARE_OP               in
               84  POP_JUMP_IF_FALSE    94  'to 94'

 L. 437        86  LOAD_GLOBAL              CancelledError
               88  CALL_FUNCTION_0       0  ''
               90  RAISE_VARARGS_1       1  'exception instance'
               92  JUMP_FORWARD        130  'to 130'
             94_0  COME_FROM            84  '84'

 L. 438        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _state
               98  LOAD_GLOBAL              FINISHED
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   124  'to 124'

 L. 439       104  LOAD_FAST                'self'
              106  LOAD_METHOD              _Future__get_result
              108  CALL_METHOD_0         0  ''
              110  POP_BLOCK        
              112  ROT_TWO          
              114  BEGIN_FINALLY    
              116  WITH_CLEANUP_START
              118  WITH_CLEANUP_FINISH
              120  POP_FINALLY           0  ''
              122  RETURN_VALUE     
            124_0  COME_FROM           102  '102'

 L. 441       124  LOAD_GLOBAL              TimeoutError
              126  CALL_FUNCTION_0       0  ''
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM            92  '92'
              130  POP_BLOCK        
              132  BEGIN_FINALLY    
            134_0  COME_FROM_WITH        4  '4'
              134  WITH_CLEANUP_START
              136  WITH_CLEANUP_FINISH
              138  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 48

    def exception--- This code section failed: ---

 L. 461         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH          130  'to 130'
                6  POP_TOP          

 L. 462         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              CANCELLED
               14  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               16  BUILD_TUPLE_2         2 
               18  COMPARE_OP               in
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 463        22  LOAD_GLOBAL              CancelledError
               24  CALL_FUNCTION_0       0  ''
               26  RAISE_VARARGS_1       1  'exception instance'
               28  JUMP_FORWARD         58  'to 58'
             30_0  COME_FROM            20  '20'

 L. 464        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _state
               34  LOAD_GLOBAL              FINISHED
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    58  'to 58'

 L. 465        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _exception
               44  POP_BLOCK        
               46  ROT_TWO          
               48  BEGIN_FINALLY    
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  POP_FINALLY           0  ''
               56  RETURN_VALUE     
             58_0  COME_FROM            38  '38'
             58_1  COME_FROM            28  '28'

 L. 467        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _condition
               62  LOAD_METHOD              wait
               64  LOAD_FAST                'timeout'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L. 469        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _state
               74  LOAD_GLOBAL              CANCELLED
               76  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               78  BUILD_TUPLE_2         2 
               80  COMPARE_OP               in
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L. 470        84  LOAD_GLOBAL              CancelledError
               86  CALL_FUNCTION_0       0  ''
               88  RAISE_VARARGS_1       1  'exception instance'
               90  JUMP_FORWARD        126  'to 126'
             92_0  COME_FROM            82  '82'

 L. 471        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _state
               96  LOAD_GLOBAL              FINISHED
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   120  'to 120'

 L. 472       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _exception
              106  POP_BLOCK        
              108  ROT_TWO          
              110  BEGIN_FINALLY    
              112  WITH_CLEANUP_START
              114  WITH_CLEANUP_FINISH
              116  POP_FINALLY           0  ''
              118  RETURN_VALUE     
            120_0  COME_FROM           100  '100'

 L. 474       120  LOAD_GLOBAL              TimeoutError
              122  CALL_FUNCTION_0       0  ''
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM            90  '90'
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_WITH        4  '4'
              130  WITH_CLEANUP_START
              132  WITH_CLEANUP_FINISH
              134  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 46

    def set_running_or_notify_cancel--- This code section failed: ---

 L. 500         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _condition
                4  SETUP_WITH          122  'to 122'
                6  POP_TOP          

 L. 501         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              CANCELLED
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE    60  'to 60'

 L. 502        18  LOAD_GLOBAL              CANCELLED_AND_NOTIFIED
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _state

 L. 503        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _waiters
               28  GET_ITER         
               30  FOR_ITER             46  'to 46'
               32  STORE_FAST               'waiter'

 L. 504        34  LOAD_FAST                'waiter'
               36  LOAD_METHOD              add_cancelled
               38  LOAD_FAST                'self'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
               44  JUMP_BACK            30  'to 30'

 L. 507        46  POP_BLOCK        
               48  BEGIN_FINALLY    
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  POP_FINALLY           0  ''
               56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            16  '16'

 L. 508        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _state
               64  LOAD_GLOBAL              PENDING
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    90  'to 90'

 L. 509        70  LOAD_GLOBAL              RUNNING
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _state

 L. 510        76  POP_BLOCK        
               78  BEGIN_FINALLY    
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  POP_FINALLY           0  ''
               86  LOAD_CONST               True
               88  RETURN_VALUE     
             90_0  COME_FROM            68  '68'

 L. 512        90  LOAD_GLOBAL              LOGGER
               92  LOAD_METHOD              critical
               94  LOAD_STR                 'Future %s in unexpected state: %s'

 L. 513        96  LOAD_GLOBAL              id
               98  LOAD_FAST                'self'
              100  CALL_FUNCTION_1       1  ''

 L. 514       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _state

 L. 512       106  CALL_METHOD_3         3  ''
              108  POP_TOP          

 L. 515       110  LOAD_GLOBAL              RuntimeError
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
        else:
            if 'fn' in kwargs:
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
                while fs:
                    if timeout is None:
                        (yield fs.pop().result())
                    else:
                        (yield fs.pop().result(end_time - time.monotonic()))

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