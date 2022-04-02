# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\tasks.py
"""Support for tasks, coroutines and the scheduler."""
__all__ = ('Task', 'create_task', 'FIRST_COMPLETED', 'FIRST_EXCEPTION', 'ALL_COMPLETED',
           'wait', 'wait_for', 'as_completed', 'sleep', 'gather', 'shield', 'ensure_future',
           'run_coroutine_threadsafe', 'current_task', 'all_tasks', '_register_task',
           '_unregister_task', '_enter_task', '_leave_task')
import concurrent.futures, contextvars, functools, inspect, itertools, types, warnings, weakref
from . import base_tasks
from . import coroutines
from . import events
from . import exceptions
from . import futures
from .coroutines import _is_coroutine
_task_name_counter = itertools.count(1).__next__

def current_task(loop=None):
    """Return a currently executed task."""
    if loop is None:
        loop = events.get_running_loop()
    return _current_tasks.get(loop)


def all_tasks--- This code section failed: ---

 L.  43         0  LOAD_DEREF               'loop'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  44         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_running_loop
               12  CALL_METHOD_0         0  ''
               14  STORE_DEREF              'loop'
             16_0  COME_FROM             6  '6'

 L.  50        16  LOAD_CONST               0
               18  STORE_FAST               'i'

 L.  52        20  SETUP_FINALLY        34  'to 34'

 L.  53        22  LOAD_GLOBAL              list
               24  LOAD_GLOBAL              _all_tasks
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'tasks'
               30  POP_BLOCK        
               32  BREAK_LOOP           76  'to 76'
             34_0  COME_FROM_FINALLY    20  '20'

 L.  54        34  DUP_TOP          
               36  LOAD_GLOBAL              RuntimeError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    70  'to 70'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  55        48  LOAD_FAST                'i'
               50  LOAD_CONST               1
               52  INPLACE_ADD      
               54  STORE_FAST               'i'

 L.  56        56  LOAD_FAST                'i'
               58  LOAD_CONST               1000
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_FALSE    66  'to 66'

 L.  57        64  RAISE_VARARGS_0       0  'reraise'
             66_0  COME_FROM            62  '62'
               66  POP_EXCEPT       
               68  JUMP_BACK            20  'to 20'
             70_0  COME_FROM            40  '40'
               70  END_FINALLY      

 L.  59        72  BREAK_LOOP           76  'to 76'
               74  JUMP_BACK            20  'to 20'

 L.  60        76  LOAD_CLOSURE             'loop'
               78  BUILD_TUPLE_1         1 
               80  LOAD_SETCOMP             '<code_object <setcomp>>'
               82  LOAD_STR                 'all_tasks.<locals>.<setcomp>'
               84  MAKE_FUNCTION_8          'closure'
               86  LOAD_FAST                'tasks'
               88  GET_ITER         
               90  CALL_FUNCTION_1       1  ''
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 44


def _all_tasks_compat--- This code section failed: ---

 L.  68         0  LOAD_DEREF               'loop'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  69         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  STORE_DEREF              'loop'
             16_0  COME_FROM             6  '6'

 L.  75        16  LOAD_CONST               0
               18  STORE_FAST               'i'

 L.  77        20  SETUP_FINALLY        34  'to 34'

 L.  78        22  LOAD_GLOBAL              list
               24  LOAD_GLOBAL              _all_tasks
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'tasks'
               30  POP_BLOCK        
               32  BREAK_LOOP           76  'to 76'
             34_0  COME_FROM_FINALLY    20  '20'

 L.  79        34  DUP_TOP          
               36  LOAD_GLOBAL              RuntimeError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    70  'to 70'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  80        48  LOAD_FAST                'i'
               50  LOAD_CONST               1
               52  INPLACE_ADD      
               54  STORE_FAST               'i'

 L.  81        56  LOAD_FAST                'i'
               58  LOAD_CONST               1000
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_FALSE    66  'to 66'

 L.  82        64  RAISE_VARARGS_0       0  'reraise'
             66_0  COME_FROM            62  '62'
               66  POP_EXCEPT       
               68  JUMP_BACK            20  'to 20'
             70_0  COME_FROM            40  '40'
               70  END_FINALLY      

 L.  84        72  BREAK_LOOP           76  'to 76'
               74  JUMP_BACK            20  'to 20'

 L.  85        76  LOAD_CLOSURE             'loop'
               78  BUILD_TUPLE_1         1 
               80  LOAD_SETCOMP             '<code_object <setcomp>>'
               82  LOAD_STR                 '_all_tasks_compat.<locals>.<setcomp>'
               84  MAKE_FUNCTION_8          'closure'
               86  LOAD_FAST                'tasks'
               88  GET_ITER         
               90  CALL_FUNCTION_1       1  ''
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 44


def _set_task_name(task, name):
    if name is not None:
        try:
            set_name = task.set_name
        except AttributeError:
            pass
        else:
            set_name(name)


class Task(futures._PyFuture):
    __doc__ = 'A coroutine wrapped in a Future.'
    _log_destroy_pending = True

    @classmethod
    def current_task(cls, loop=None):
        """Return the currently running task in an event loop or None.

        By default the current task for the current event loop is returned.

        None is returned when called not in the context of a Task.
        """
        warnings.warn('Task.current_task() is deprecated since Python 3.7, use asyncio.current_task() instead', DeprecationWarning,
          stacklevel=2)
        if loop is None:
            loop = events.get_event_loop()
        return current_task(loop)

    @classmethod
    def all_tasks(cls, loop=None):
        """Return a set of all tasks for an event loop.

        By default all tasks for the current event loop are returned.
        """
        warnings.warn('Task.all_tasks() is deprecated since Python 3.7, use asyncio.all_tasks() instead', DeprecationWarning,
          stacklevel=2)
        return _all_tasks_compat(loop)

    def __init__(self, coro, *, loop=None, name=None):
        super().__init__(loop=loop)
        if self._source_traceback:
            del self._source_traceback[-1]
        else:
            if not coroutines.iscoroutine(coro):
                self._log_destroy_pending = False
                raise TypeError(f"a coroutine was expected, got {coro!r}")
            if name is None:
                self._name = f"Task-{_task_name_counter()}"
            else:
                self._name = str(name)
        self._must_cancel = False
        self._fut_waiter = None
        self._coro = coro
        self._context = contextvars.copy_context()
        self._loop.call_soon((self._Task__step), context=(self._context))
        _register_task(self)

    def __del__(self):
        if self._state == futures._PENDING:
            if self._log_destroy_pending:
                context = {'task':self, 
                 'message':'Task was destroyed but it is pending!'}
                if self._source_traceback:
                    context['source_traceback'] = self._source_traceback
                self._loop.call_exception_handler(context)
        super().__del__()

    def _repr_info(self):
        return base_tasks._task_repr_info(self)

    def get_coro(self):
        return self._coro

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = str(value)

    def set_result(self, result):
        raise RuntimeError('Task does not support set_result operation')

    def set_exception(self, exception):
        raise RuntimeError('Task does not support set_exception operation')

    def get_stack(self, *, limit=None):
        """Return the list of stack frames for this task's coroutine.

        If the coroutine is not done, this returns the stack where it is
        suspended.  If the coroutine has completed successfully or was
        cancelled, this returns an empty list.  If the coroutine was
        terminated by an exception, this returns the list of traceback
        frames.

        The frames are always ordered from oldest to newest.

        The optional limit gives the maximum number of frames to
        return; by default all available frames are returned.  Its
        meaning differs depending on whether a stack or a traceback is
        returned: the newest frames of a stack are returned, but the
        oldest frames of a traceback are returned.  (This matches the
        behavior of the traceback module.)

        For reasons beyond our control, only one stack frame is
        returned for a suspended coroutine.
        """
        return base_tasks._task_get_stack(self, limit)

    def print_stack(self, *, limit=None, file=None):
        """Print the stack or traceback for this task's coroutine.

        This produces output similar to that of the traceback module,
        for the frames retrieved by get_stack().  The limit argument
        is passed to get_stack().  The file argument is an I/O stream
        to which the output is written; by default output is written
        to sys.stderr.
        """
        return base_tasks._task_print_stack(self, limit, file)

    def cancel(self):
        """Request that this task cancel itself.

        This arranges for a CancelledError to be thrown into the
        wrapped coroutine on the next cycle through the event loop.
        The coroutine then has a chance to clean up or even deny
        the request using try/except/finally.

        Unlike Future.cancel, this does not guarantee that the
        task will be cancelled: the exception might be caught and
        acted upon, delaying cancellation of the task or preventing
        cancellation completely.  The task may also return a value or
        raise a different exception.

        Immediately after this method is called, Task.cancelled() will
        not return True (unless the task was already cancelled).  A
        task will be marked as cancelled when the wrapped coroutine
        terminates with a CancelledError exception (even if cancel()
        was not called).
        """
        self._log_traceback = False
        if self.done():
            return False
        if self._fut_waiter is not None:
            if self._fut_waiter.cancel():
                return True
        self._must_cancel = True
        return True

    def __step(self, exc=None):
        if self.done():
            raise exceptions.InvalidStateError(f"_step(): already done: {self!r}, {exc!r}")
        if self._must_cancel:
            if not isinstance(exc, exceptions.CancelledError):
                exc = exceptions.CancelledError()
            self._must_cancel = False
        coro = self._coro
        self._fut_waiter = None
        _enter_task(self._loop, self)
        try:
            try:
                if exc is None:
                    result = coro.send(None)
                else:
                    result = coro.throw(exc)
            except StopIteration as exc:
                try:
                    if self._must_cancel:
                        self._must_cancel = False
                        super().cancel()
                    else:
                        super().set_result(exc.value)
                finally:
                    exc = None
                    del exc

            except exceptions.CancelledError:
                super().cancel()
            except (KeyboardInterrupt, SystemExit) as exc:
                try:
                    super().set_exception(exc)
                    raise
                finally:
                    exc = None
                    del exc

            except BaseException as exc:
                try:
                    super().set_exception(exc)
                finally:
                    exc = None
                    del exc

            else:
                blocking = getattr(result, '_asyncio_future_blocking', None)
                if blocking is not None:
                    if futures._get_loop(result) is not self._loop:
                        new_exc = RuntimeError(f"Task {self!r} got Future {result!r} attached to a different loop")
                        self._loop.call_soon((self._Task__step),
                          new_exc, context=(self._context))
                    else:
                        if blocking:
                            if result is self:
                                new_exc = RuntimeError(f"Task cannot await on itself: {self!r}")
                                self._loop.call_soon((self._Task__step),
                                  new_exc, context=(self._context))
                            else:
                                result._asyncio_future_blocking = False
                                result.add_done_callback((self._Task__wakeup),
                                  context=(self._context))
                                self._fut_waiter = result
                                if self._must_cancel:
                                    if self._fut_waiter.cancel():
                                        self._must_cancel = False
                                    else:
                                        new_exc = RuntimeError(f"yield was used instead of yield from in task {self!r} with {result!r}")
                                        self._loop.call_soon((self._Task__step),
                                          new_exc, context=(self._context))
                        else:
                            pass
                if result is None:
                    self._loop.call_soon((self._Task__step), context=(self._context))
                elif inspect.isgenerator(result):
                    new_exc = RuntimeError(f"yield was used instead of yield from for generator in task {self!r} with {result!r}")
                    self._loop.call_soon((self._Task__step),
                      new_exc, context=(self._context))
                else:
                    new_exc = RuntimeError(f"Task got bad yield: {result!r}")
                    self._loop.call_soon((self._Task__step),
                      new_exc, context=(self._context))
        finally:
            _leave_task(self._loop, self)
            self = None

    def __wakeup(self, future):
        try:
            future.result()
        except BaseException as exc:
            try:
                self._Task__step(exc)
            finally:
                exc = None
                del exc

        else:
            self._Task__step()
        self = None


_PyTask = Task
try:
    import _asyncio
except ImportError:
    pass
else:
    Task = _CTask = _asyncio.Task

def create_task(coro, *, name=None):
    """Schedule the execution of a coroutine object in a spawn task.

    Return a Task object.
    """
    loop = events.get_running_loop()
    task = loop.create_task(coro)
    _set_task_name(task, name)
    return task


FIRST_COMPLETED = concurrent.futures.FIRST_COMPLETED
FIRST_EXCEPTION = concurrent.futures.FIRST_EXCEPTION
ALL_COMPLETED = concurrent.futures.ALL_COMPLETED

async def wait--- This code section failed: ---

 L. 410         0  LOAD_GLOBAL              futures
                2  LOAD_METHOD              isfuture
                4  LOAD_FAST                'fs'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     20  'to 20'
               10  LOAD_GLOBAL              coroutines
               12  LOAD_METHOD              iscoroutine
               14  LOAD_FAST                'fs'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_FALSE    40  'to 40'
             20_0  COME_FROM             8  '8'

 L. 411        20  LOAD_GLOBAL              TypeError
               22  LOAD_STR                 'expect a list of futures, not '
               24  LOAD_GLOBAL              type
               26  LOAD_FAST                'fs'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_ATTR                __name__
               32  FORMAT_VALUE          0  ''
               34  BUILD_STRING_2        2 
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            18  '18'

 L. 412        40  LOAD_FAST                'fs'
               42  POP_JUMP_IF_TRUE     52  'to 52'

 L. 413        44  LOAD_GLOBAL              ValueError
               46  LOAD_STR                 'Set of coroutines/Futures is empty.'
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            42  '42'

 L. 414        52  LOAD_FAST                'return_when'
               54  LOAD_GLOBAL              FIRST_COMPLETED
               56  LOAD_GLOBAL              FIRST_EXCEPTION
               58  LOAD_GLOBAL              ALL_COMPLETED
               60  BUILD_TUPLE_3         3 
               62  COMPARE_OP               not-in
               64  POP_JUMP_IF_FALSE    80  'to 80'

 L. 415        66  LOAD_GLOBAL              ValueError
               68  LOAD_STR                 'Invalid return_when value: '
               70  LOAD_FAST                'return_when'
               72  FORMAT_VALUE          0  ''
               74  BUILD_STRING_2        2 
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            64  '64'

 L. 417        80  LOAD_DEREF               'loop'
               82  LOAD_CONST               None
               84  COMPARE_OP               is
               86  POP_JUMP_IF_FALSE    98  'to 98'

 L. 418        88  LOAD_GLOBAL              events
               90  LOAD_METHOD              get_running_loop
               92  CALL_METHOD_0         0  ''
               94  STORE_DEREF              'loop'
               96  JUMP_FORWARD        114  'to 114'
             98_0  COME_FROM            86  '86'

 L. 420        98  LOAD_GLOBAL              warnings
              100  LOAD_ATTR                warn
              102  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L. 422       104  LOAD_GLOBAL              DeprecationWarning

 L. 422       106  LOAD_CONST               2

 L. 420       108  LOAD_CONST               ('stacklevel',)
              110  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              112  POP_TOP          
            114_0  COME_FROM            96  '96'

 L. 424       114  LOAD_CLOSURE             'loop'
              116  BUILD_TUPLE_1         1 
              118  LOAD_SETCOMP             '<code_object <setcomp>>'
              120  LOAD_STR                 'wait.<locals>.<setcomp>'
              122  MAKE_FUNCTION_8          'closure'
              124  LOAD_GLOBAL              set
              126  LOAD_FAST                'fs'
              128  CALL_FUNCTION_1       1  ''
              130  GET_ITER         
              132  CALL_FUNCTION_1       1  ''
              134  STORE_FAST               'fs'

 L. 426       136  LOAD_GLOBAL              _wait
              138  LOAD_FAST                'fs'
              140  LOAD_FAST                'timeout'
              142  LOAD_FAST                'return_when'
              144  LOAD_DEREF               'loop'
              146  CALL_FUNCTION_4       4  ''
              148  GET_AWAITABLE    
              150  LOAD_CONST               None
              152  YIELD_FROM       
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 118


def _release_waiter(waiter, *args):
    if not waiter.done():
        waiter.set_result(None)


async def wait_for--- This code section failed: ---

 L. 447         0  LOAD_FAST                'loop'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 448         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_running_loop
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'loop'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L. 450        18  LOAD_GLOBAL              warnings
               20  LOAD_ATTR                warn
               22  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L. 452        24  LOAD_GLOBAL              DeprecationWarning

 L. 452        26  LOAD_CONST               2

 L. 450        28  LOAD_CONST               ('stacklevel',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  POP_TOP          
             34_0  COME_FROM            16  '16'

 L. 454        34  LOAD_FAST                'timeout'
               36  LOAD_CONST               None
               38  COMPARE_OP               is
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 455        42  LOAD_FAST                'fut'
               44  GET_AWAITABLE    
               46  LOAD_CONST               None
               48  YIELD_FROM       
               50  RETURN_VALUE     
             52_0  COME_FROM            40  '40'

 L. 457        52  LOAD_FAST                'timeout'
               54  LOAD_CONST               0
               56  COMPARE_OP               <=
               58  POP_JUMP_IF_FALSE   104  'to 104'

 L. 458        60  LOAD_GLOBAL              ensure_future
               62  LOAD_FAST                'fut'
               64  LOAD_FAST                'loop'
               66  LOAD_CONST               ('loop',)
               68  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               70  STORE_FAST               'fut'

 L. 460        72  LOAD_FAST                'fut'
               74  LOAD_METHOD              done
               76  CALL_METHOD_0         0  ''
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L. 461        80  LOAD_FAST                'fut'
               82  LOAD_METHOD              result
               84  CALL_METHOD_0         0  ''
               86  RETURN_VALUE     
             88_0  COME_FROM            78  '78'

 L. 463        88  LOAD_FAST                'fut'
               90  LOAD_METHOD              cancel
               92  CALL_METHOD_0         0  ''
               94  POP_TOP          

 L. 464        96  LOAD_GLOBAL              exceptions
               98  LOAD_METHOD              TimeoutError
              100  CALL_METHOD_0         0  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            58  '58'

 L. 466       104  LOAD_FAST                'loop'
              106  LOAD_METHOD              create_future
              108  CALL_METHOD_0         0  ''
              110  STORE_FAST               'waiter'

 L. 467       112  LOAD_FAST                'loop'
              114  LOAD_METHOD              call_later
              116  LOAD_FAST                'timeout'
              118  LOAD_GLOBAL              _release_waiter
              120  LOAD_FAST                'waiter'
              122  CALL_METHOD_3         3  ''
              124  STORE_FAST               'timeout_handle'

 L. 468       126  LOAD_GLOBAL              functools
              128  LOAD_METHOD              partial
              130  LOAD_GLOBAL              _release_waiter
              132  LOAD_FAST                'waiter'
              134  CALL_METHOD_2         2  ''
              136  STORE_FAST               'cb'

 L. 470       138  LOAD_GLOBAL              ensure_future
              140  LOAD_FAST                'fut'
              142  LOAD_FAST                'loop'
              144  LOAD_CONST               ('loop',)
              146  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              148  STORE_FAST               'fut'

 L. 471       150  LOAD_FAST                'fut'
              152  LOAD_METHOD              add_done_callback
              154  LOAD_FAST                'cb'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          

 L. 473       160  SETUP_FINALLY       280  'to 280'

 L. 475       162  SETUP_FINALLY       178  'to 178'

 L. 476       164  LOAD_FAST                'waiter'
              166  GET_AWAITABLE    
              168  LOAD_CONST               None
              170  YIELD_FROM       
              172  POP_TOP          
              174  POP_BLOCK        
              176  JUMP_FORWARD        220  'to 220'
            178_0  COME_FROM_FINALLY   162  '162'

 L. 477       178  DUP_TOP          
              180  LOAD_GLOBAL              exceptions
              182  LOAD_ATTR                CancelledError
              184  COMPARE_OP               exception-match
              186  POP_JUMP_IF_FALSE   218  'to 218'
              188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          

 L. 478       194  LOAD_FAST                'fut'
              196  LOAD_METHOD              remove_done_callback
              198  LOAD_FAST                'cb'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          

 L. 479       204  LOAD_FAST                'fut'
              206  LOAD_METHOD              cancel
              208  CALL_METHOD_0         0  ''
              210  POP_TOP          

 L. 480       212  RAISE_VARARGS_0       0  'reraise'
              214  POP_EXCEPT       
              216  JUMP_FORWARD        220  'to 220'
            218_0  COME_FROM           186  '186'
              218  END_FINALLY      
            220_0  COME_FROM           216  '216'
            220_1  COME_FROM           176  '176'

 L. 482       220  LOAD_FAST                'fut'
              222  LOAD_METHOD              done
              224  CALL_METHOD_0         0  ''
              226  POP_JUMP_IF_FALSE   240  'to 240'

 L. 483       228  LOAD_FAST                'fut'
              230  LOAD_METHOD              result
              232  CALL_METHOD_0         0  ''
              234  POP_BLOCK        
              236  CALL_FINALLY        280  'to 280'
              238  RETURN_VALUE     
            240_0  COME_FROM           226  '226'

 L. 485       240  LOAD_FAST                'fut'
              242  LOAD_METHOD              remove_done_callback
              244  LOAD_FAST                'cb'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          

 L. 489       250  LOAD_GLOBAL              _cancel_and_wait
              252  LOAD_FAST                'fut'
              254  LOAD_FAST                'loop'
              256  LOAD_CONST               ('loop',)
              258  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              260  GET_AWAITABLE    
              262  LOAD_CONST               None
              264  YIELD_FROM       
              266  POP_TOP          

 L. 490       268  LOAD_GLOBAL              exceptions
              270  LOAD_METHOD              TimeoutError
              272  CALL_METHOD_0         0  ''
              274  RAISE_VARARGS_1       1  'exception instance'
              276  POP_BLOCK        
              278  BEGIN_FINALLY    
            280_0  COME_FROM           236  '236'
            280_1  COME_FROM_FINALLY   160  '160'

 L. 492       280  LOAD_FAST                'timeout_handle'
              282  LOAD_METHOD              cancel
              284  CALL_METHOD_0         0  ''
              286  POP_TOP          
              288  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 236


async def _wait(fs, timeout, return_when, loop):
    """Internal helper for wait().

    The fs argument must be a collection of Futures.
    """
    assert fs, 'Set of Futures is empty.'
    waiter = loop.create_future()
    timeout_handle = None
    if timeout is not None:
        timeout_handle = loop.call_later(timeout, _release_waiter, waiter)
    counter = len(fs)

    def _on_completion--- This code section failed: ---

 L. 509         0  LOAD_DEREF               'counter'
                2  LOAD_CONST               1
                4  INPLACE_SUBTRACT 
                6  STORE_DEREF              'counter'

 L. 510         8  LOAD_DEREF               'counter'
               10  LOAD_CONST               0
               12  COMPARE_OP               <=
               14  POP_JUMP_IF_TRUE     52  'to 52'

 L. 511        16  LOAD_DEREF               'return_when'
               18  LOAD_GLOBAL              FIRST_COMPLETED
               20  COMPARE_OP               ==

 L. 510        22  POP_JUMP_IF_TRUE     52  'to 52'

 L. 512        24  LOAD_DEREF               'return_when'
               26  LOAD_GLOBAL              FIRST_EXCEPTION
               28  COMPARE_OP               ==

 L. 510        30  POP_JUMP_IF_FALSE    86  'to 86'

 L. 512        32  LOAD_FAST                'f'
               34  LOAD_METHOD              cancelled
               36  CALL_METHOD_0         0  ''

 L. 510        38  POP_JUMP_IF_TRUE     86  'to 86'

 L. 513        40  LOAD_FAST                'f'
               42  LOAD_METHOD              exception
               44  CALL_METHOD_0         0  ''
               46  LOAD_CONST               None
               48  COMPARE_OP               is-not

 L. 510        50  POP_JUMP_IF_FALSE    86  'to 86'
             52_0  COME_FROM            22  '22'
             52_1  COME_FROM            14  '14'

 L. 514        52  LOAD_DEREF               'timeout_handle'
               54  LOAD_CONST               None
               56  COMPARE_OP               is-not
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 515        60  LOAD_DEREF               'timeout_handle'
               62  LOAD_METHOD              cancel
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          
             68_0  COME_FROM            58  '58'

 L. 516        68  LOAD_DEREF               'waiter'
               70  LOAD_METHOD              done
               72  CALL_METHOD_0         0  ''
               74  POP_JUMP_IF_TRUE     86  'to 86'

 L. 517        76  LOAD_DEREF               'waiter'
               78  LOAD_METHOD              set_result
               80  LOAD_CONST               None
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
             86_0  COME_FROM            74  '74'
             86_1  COME_FROM            50  '50'
             86_2  COME_FROM            38  '38'
             86_3  COME_FROM            30  '30'

Parse error at or near `COME_FROM' instruction at offset 86_2

    for f in fs:
        f.add_done_callback(_on_completion)
    else:
        try:
            await waiter
        finally:
            if timeout_handle is not None:
                timeout_handle.cancel()
            for f in fs:
                f.remove_done_callback(_on_completion)

        done, pending = set(), set()
        for f in fs:
            if f.done():
                done.add(f)
            else:
                pending.add(f)
        else:
            return (
             done, pending)


async def _cancel_and_wait(fut, loop):
    """Cancel the *fut* future or task and wait until it completes."""
    waiter = loop.create_future()
    cb = functools.partial(_release_waiter, waiter)
    fut.add_done_callback(cb)
    try:
        fut.cancel()
        await waiter
    finally:
        fut.remove_done_callback(cb)


def as_completed--- This code section failed: ---

 L. 574         0  LOAD_GLOBAL              futures
                2  LOAD_METHOD              isfuture
                4  LOAD_FAST                'fs'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     20  'to 20'
               10  LOAD_GLOBAL              coroutines
               12  LOAD_METHOD              iscoroutine
               14  LOAD_FAST                'fs'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_FALSE    40  'to 40'
             20_0  COME_FROM             8  '8'

 L. 575        20  LOAD_GLOBAL              TypeError
               22  LOAD_STR                 'expect a list of futures, not '
               24  LOAD_GLOBAL              type
               26  LOAD_FAST                'fs'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_ATTR                __name__
               32  FORMAT_VALUE          0  ''
               34  BUILD_STRING_2        2 
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            18  '18'

 L. 577        40  LOAD_CONST               1
               42  LOAD_CONST               ('Queue',)
               44  IMPORT_NAME              queues
               46  IMPORT_FROM              Queue
               48  STORE_FAST               'Queue'
               50  POP_TOP          

 L. 578        52  LOAD_FAST                'Queue'
               54  LOAD_DEREF               'loop'
               56  LOAD_CONST               ('loop',)
               58  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               60  STORE_DEREF              'done'

 L. 580        62  LOAD_DEREF               'loop'
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  POP_JUMP_IF_FALSE    80  'to 80'

 L. 581        70  LOAD_GLOBAL              events
               72  LOAD_METHOD              get_event_loop
               74  CALL_METHOD_0         0  ''
               76  STORE_DEREF              'loop'
               78  JUMP_FORWARD         96  'to 96'
             80_0  COME_FROM            68  '68'

 L. 583        80  LOAD_GLOBAL              warnings
               82  LOAD_ATTR                warn
               84  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L. 585        86  LOAD_GLOBAL              DeprecationWarning

 L. 585        88  LOAD_CONST               2

 L. 583        90  LOAD_CONST               ('stacklevel',)
               92  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               94  POP_TOP          
             96_0  COME_FROM            78  '78'

 L. 586        96  LOAD_CLOSURE             'loop'
               98  BUILD_TUPLE_1         1 
              100  LOAD_SETCOMP             '<code_object <setcomp>>'
              102  LOAD_STR                 'as_completed.<locals>.<setcomp>'
              104  MAKE_FUNCTION_8          'closure'
              106  LOAD_GLOBAL              set
              108  LOAD_FAST                'fs'
              110  CALL_FUNCTION_1       1  ''
              112  GET_ITER         
              114  CALL_FUNCTION_1       1  ''
              116  STORE_DEREF              'todo'

 L. 587       118  LOAD_CONST               None
              120  STORE_DEREF              'timeout_handle'

 L. 589       122  LOAD_CLOSURE             '_on_completion'
              124  LOAD_CLOSURE             'done'
              126  LOAD_CLOSURE             'todo'
              128  BUILD_TUPLE_3         3 
              130  LOAD_CODE                <code_object _on_timeout>
              132  LOAD_STR                 'as_completed.<locals>._on_timeout'
              134  MAKE_FUNCTION_8          'closure'
              136  STORE_FAST               '_on_timeout'

 L. 595       138  LOAD_CLOSURE             'done'
              140  LOAD_CLOSURE             'timeout_handle'
              142  LOAD_CLOSURE             'todo'
              144  BUILD_TUPLE_3         3 
              146  LOAD_CODE                <code_object _on_completion>
              148  LOAD_STR                 'as_completed.<locals>._on_completion'
              150  MAKE_FUNCTION_8          'closure'
              152  STORE_DEREF              '_on_completion'

 L. 603       154  LOAD_CLOSURE             'done'
              156  BUILD_TUPLE_1         1 
              158  LOAD_CODE                <code_object _wait_for_one>
              160  LOAD_STR                 'as_completed.<locals>._wait_for_one'
              162  MAKE_FUNCTION_8          'closure'
              164  STORE_FAST               '_wait_for_one'

 L. 610       166  LOAD_DEREF               'todo'
              168  GET_ITER         
              170  FOR_ITER            186  'to 186'
              172  STORE_FAST               'f'

 L. 611       174  LOAD_FAST                'f'
              176  LOAD_METHOD              add_done_callback
              178  LOAD_DEREF               '_on_completion'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
              184  JUMP_BACK           170  'to 170'

 L. 612       186  LOAD_DEREF               'todo'
              188  POP_JUMP_IF_FALSE   210  'to 210'
              190  LOAD_FAST                'timeout'
              192  LOAD_CONST               None
              194  COMPARE_OP               is-not
              196  POP_JUMP_IF_FALSE   210  'to 210'

 L. 613       198  LOAD_DEREF               'loop'
              200  LOAD_METHOD              call_later
              202  LOAD_FAST                'timeout'
              204  LOAD_FAST                '_on_timeout'
              206  CALL_METHOD_2         2  ''
              208  STORE_DEREF              'timeout_handle'
            210_0  COME_FROM           196  '196'
            210_1  COME_FROM           188  '188'

 L. 614       210  LOAD_GLOBAL              range
              212  LOAD_GLOBAL              len
              214  LOAD_DEREF               'todo'
              216  CALL_FUNCTION_1       1  ''
              218  CALL_FUNCTION_1       1  ''
              220  GET_ITER         
              222  FOR_ITER            236  'to 236'
              224  STORE_FAST               '_'

 L. 615       226  LOAD_FAST                '_wait_for_one'
              228  CALL_FUNCTION_0       0  ''
              230  YIELD_VALUE      
              232  POP_TOP          
              234  JUMP_BACK           222  'to 222'

Parse error at or near `LOAD_SETCOMP' instruction at offset 100


@types.coroutine
def __sleep0():
    """Skip one event loop run cycle.

    This is a private helper for 'asyncio.sleep()', used
    when the 'delay' is set to 0.  It uses a bare 'yield'
    expression (which Task.__step knows how to handle)
    instead of creating a Future object.
    """
    (yield)


async def sleep(delay, result=None, *, loop=None):
    """Coroutine that completes after a given time (in seconds)."""
    if delay <= 0:
        await __sleep0()
        return result
    elif loop is None:
        loop = events.get_running_loop()
    else:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
          stacklevel=2)
    future = loop.create_future()
    h = loop.call_later(delay, futures._set_result_unless_cancelled, future, result)
    try:
        return await future
    finally:
        h.cancel()


def ensure_future(coro_or_future, *, loop=None):
    """Wrap a coroutine or an awaitable in a future.

    If the argument is a Future, it is returned directly.
    """
    if coroutines.iscoroutine(coro_or_future):
        if loop is None:
            loop = events.get_event_loop()
        task = loop.create_task(coro_or_future)
        if task._source_traceback:
            del task._source_traceback[-1]
        return task
    if futures.isfuture(coro_or_future):
        if loop is not None:
            if loop is not futures._get_loop(coro_or_future):
                raise ValueError('The future belongs to a different loop than the one specified as the loop argument')
        return coro_or_future
    if inspect.isawaitable(coro_or_future):
        return ensure_future((_wrap_awaitable(coro_or_future)), loop=loop)
    raise TypeError('An asyncio.Future, a coroutine or an awaitable is required')


@types.coroutine
def _wrap_awaitable(awaitable):
    """Helper for asyncio.ensure_future().

    Wraps awaitable (an object with __await__) into a coroutine
    that will later be wrapped in a Task by ensure_future().
    """
    return (yield from awaitable.__await__())
    if False:
        yield None


_wrap_awaitable._is_coroutine = _is_coroutine

class _GatheringFuture(futures.Future):
    __doc__ = "Helper for gather().\n\n    This overrides cancel() to cancel all the children and act more\n    like Task.cancel(), which doesn't immediately mark itself as\n    cancelled.\n    "

    def __init__(self, children, *, loop=None):
        super().__init__(loop=loop)
        self._children = children
        self._cancel_requested = False

    def cancel(self):
        if self.done():
            return False
        ret = False
        for child in self._children:
            if child.cancel():
                ret = True
            if ret:
                self._cancel_requested = True
            return ret


def gather(*coros_or_futures, loop=None, return_exceptions=False):
    """Return a future aggregating results from the given coroutines/futures.

    Coroutines will be wrapped in a future and scheduled in the event
    loop. They will not necessarily be scheduled in the same order as
    passed in.

    All futures must share the same event loop.  If all the tasks are
    done successfully, the returned future's result is the list of
    results (in the order of the original sequence, not necessarily
    the order of results arrival).  If *return_exceptions* is True,
    exceptions in the tasks are treated the same as successful
    results, and gathered in the result list; otherwise, the first
    raised exception will be immediately propagated to the returned
    future.

    Cancellation: if the outer Future is cancelled, all children (that
    have not completed yet) are also cancelled.  If any child is
    cancelled, this is treated as if it raised CancelledError --
    the outer Future is *not* cancelled in this case.  (This is to
    prevent the cancellation of one child to cause other children to
    be cancelled.)
    """
    if not coros_or_futures:
        if loop is None:
            loop = events.get_event_loop()
        else:
            warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
              stacklevel=2)
        outer = loop.create_future()
        outer.set_result([])
        return outer

    def _done_callback(fut):
        nonlocal nfinished
        nfinished += 1
        if outer.done():
            if not fut.cancelled():
                fut.exception()
            return
        if not return_exceptions:
            if fut.cancelled():
                exc = exceptions.CancelledError()
                outer.set_exception(exc)
                return None
            exc = fut.exception()
            if exc is not None:
                outer.set_exception(exc)
                return
        elif nfinished == nfuts:
            results = []
            for fut in children:
                if fut.cancelled():
                    res = exceptions.CancelledError()
                else:
                    res = fut.exception()
                    if res is None:
                        res = fut.result()
                results.append(res)
            else:
                if outer._cancel_requested:
                    outer.set_exception(exceptions.CancelledError())
                else:
                    outer.set_result(results)

    arg_to_fut = {}
    children = []
    nfuts = 0
    nfinished = 0
    for arg in coros_or_futures:
        if arg not in arg_to_fut:
            fut = ensure_future(arg, loop=loop)
            if loop is None:
                loop = futures._get_loop(fut)
            if fut is not arg:
                fut._log_destroy_pending = False
            nfuts += 1
            arg_to_fut[arg] = fut
            fut.add_done_callback(_done_callback)
        else:
            fut = arg_to_fut[arg]
        children.append(fut)
    else:
        outer = _GatheringFuture(children, loop=loop)
        return outer


def shield(arg, *, loop=None):
    """Wait for a future, shielding it from cancellation.

    The statement

        res = await shield(something())

    is exactly equivalent to the statement

        res = await something()

    *except* that if the coroutine containing it is cancelled, the
    task running in something() is not cancelled.  From the POV of
    something(), the cancellation did not happen.  But its caller is
    still cancelled, so the yield-from expression still raises
    CancelledError.  Note: If something() is cancelled by other means
    this will still cancel shield().

    If you want to completely ignore cancellation (not recommended)
    you can combine shield() with a try/except clause, as follows:

        try:
            res = await shield(something())
        except CancelledError:
            res = None
    """
    if loop is not None:
        warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
          stacklevel=2)
    inner = ensure_future(arg, loop=loop)
    if inner.done():
        return inner
    loop = futures._get_loop(inner)
    outer = loop.create_future()

    def _inner_done_callback(inner):
        if outer.cancelled():
            if not inner.cancelled():
                inner.exception()
            return
        if inner.cancelled():
            outer.cancel()
        else:
            exc = inner.exception()
            if exc is not None:
                outer.set_exception(exc)
            else:
                outer.set_result(inner.result())

    def _outer_done_callback(outer):
        if not inner.done():
            inner.remove_done_callback(_inner_done_callback)

    inner.add_done_callback(_inner_done_callback)
    outer.add_done_callback(_outer_done_callback)
    return outer


def run_coroutine_threadsafe(coro, loop):
    """Submit a coroutine object to a given event loop.

    Return a concurrent.futures.Future to access the result.
    """
    if not coroutines.iscoroutine(coro):
        raise TypeError('A coroutine object is required')
    future = concurrent.futures.Future()

    def callback():
        try:
            futures._chain_future(ensure_future(coro, loop=loop), future)
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as exc:
            try:
                if future.set_running_or_notify_cancel():
                    future.set_exception(exc)
                raise
            finally:
                exc = None
                del exc

    loop.call_soon_threadsafe(callback)
    return future


_all_tasks = weakref.WeakSet()
_current_tasks = {}

def _register_task(task):
    """Register a new task in asyncio as executed by loop."""
    _all_tasks.add(task)


def _enter_task(loop, task):
    current_task = _current_tasks.get(loop)
    if current_task is not None:
        raise RuntimeError(f"Cannot enter into task {task!r} while another task {current_task!r} is being executed.")
    _current_tasks[loop] = task


def _leave_task(loop, task):
    current_task = _current_tasks.get(loop)
    if current_task is not task:
        raise RuntimeError(f"Leaving task {task!r} does not match the current task {current_task!r}.")
    del _current_tasks[loop]


def _unregister_task(task):
    """Unregister a task."""
    _all_tasks.discard(task)


_py_register_task = _register_task
_py_unregister_task = _unregister_task
_py_enter_task = _enter_task
_py_leave_task = _leave_task
try:
    from _asyncio import _register_task, _unregister_task, _enter_task, _leave_task, _all_tasks, _current_tasks
except ImportError:
    pass
else:
    _c_register_task = _register_task
    _c_unregister_task = _unregister_task
    _c_enter_task = _enter_task
    _c_leave_task = _leave_task