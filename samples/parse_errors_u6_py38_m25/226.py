# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: concurrent\futures\thread.py
"""Implements ThreadPoolExecutor."""
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
import atexit
from concurrent.futures import _base
import itertools, queue, threading, weakref, os
_threads_queues = weakref.WeakKeyDictionary()
_shutdown = False

def _python_exit():
    global _shutdown
    _shutdown = True
    items = list(_threads_queues.items())
    for t, q in items:
        q.put(None)
    else:
        for t, q in items:
            t.join()


atexit.register(_python_exit)

class _WorkItem(object):

    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if not self.future.set_running_or_notify_cancel():
            return
        try:
            result = (self.fn)(*self.args, **self.kwargs)
        except BaseException as exc:
            try:
                self.future.set_exception(exc)
                self = None
            finally:
                exc = None
                del exc

        else:
            self.future.set_result(result)


def _worker--- This code section failed: ---

 L.  67         0  LOAD_FAST                'initializer'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    82  'to 82'

 L.  68         8  SETUP_FINALLY        22  'to 22'

 L.  69        10  LOAD_FAST                'initializer'
               12  LOAD_FAST                'initargs'
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  POP_TOP          
               18  POP_BLOCK        
               20  JUMP_FORWARD         82  'to 82'
             22_0  COME_FROM_FINALLY     8  '8'

 L.  70        22  DUP_TOP          
               24  LOAD_GLOBAL              BaseException
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    80  'to 80'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  71        36  LOAD_GLOBAL              _base
               38  LOAD_ATTR                LOGGER
               40  LOAD_ATTR                critical
               42  LOAD_STR                 'Exception in initializer:'
               44  LOAD_CONST               True
               46  LOAD_CONST               ('exc_info',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  POP_TOP          

 L.  72        52  LOAD_FAST                'executor_reference'
               54  CALL_FUNCTION_0       0  ''
               56  STORE_FAST               'executor'

 L.  73        58  LOAD_FAST                'executor'
               60  LOAD_CONST               None
               62  COMPARE_OP               is-not
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L.  74        66  LOAD_FAST                'executor'
               68  LOAD_METHOD              _initializer_failed
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          
             74_0  COME_FROM            64  '64'

 L.  75        74  POP_EXCEPT       
               76  LOAD_CONST               None
               78  RETURN_VALUE     
             80_0  COME_FROM            28  '28'
               80  END_FINALLY      
             82_0  COME_FROM            20  '20'
             82_1  COME_FROM             6  '6'

 L.  76        82  SETUP_FINALLY       204  'to 204'

 L.  78        84  LOAD_FAST                'work_queue'
               86  LOAD_ATTR                get
               88  LOAD_CONST               True
               90  LOAD_CONST               ('block',)
               92  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               94  STORE_FAST               'work_item'

 L.  79        96  LOAD_FAST                'work_item'
               98  LOAD_CONST               None
              100  COMPARE_OP               is-not
              102  POP_JUMP_IF_FALSE   142  'to 142'

 L.  80       104  LOAD_FAST                'work_item'
              106  LOAD_METHOD              run
              108  CALL_METHOD_0         0  ''
              110  POP_TOP          

 L.  82       112  DELETE_FAST              'work_item'

 L.  85       114  LOAD_FAST                'executor_reference'
              116  CALL_FUNCTION_0       0  ''
              118  STORE_FAST               'executor'

 L.  86       120  LOAD_FAST                'executor'
              122  LOAD_CONST               None
              124  COMPARE_OP               is-not
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L.  87       128  LOAD_FAST                'executor'
              130  LOAD_ATTR                _idle_semaphore
              132  LOAD_METHOD              release
              134  CALL_METHOD_0         0  ''
              136  POP_TOP          
            138_0  COME_FROM           126  '126'

 L.  88       138  DELETE_FAST              'executor'

 L.  89       140  JUMP_BACK            84  'to 84'
            142_0  COME_FROM           102  '102'

 L.  91       142  LOAD_FAST                'executor_reference'
              144  CALL_FUNCTION_0       0  ''
              146  STORE_FAST               'executor'

 L.  96       148  LOAD_GLOBAL              _shutdown
              150  POP_JUMP_IF_TRUE    166  'to 166'
              152  LOAD_FAST                'executor'
              154  LOAD_CONST               None
              156  COMPARE_OP               is
              158  POP_JUMP_IF_TRUE    166  'to 166'
              160  LOAD_FAST                'executor'
              162  LOAD_ATTR                _shutdown
              164  POP_JUMP_IF_FALSE   196  'to 196'
            166_0  COME_FROM           158  '158'
            166_1  COME_FROM           150  '150'

 L.  99       166  LOAD_FAST                'executor'
              168  LOAD_CONST               None
              170  COMPARE_OP               is-not
              172  POP_JUMP_IF_FALSE   180  'to 180'

 L. 100       174  LOAD_CONST               True
              176  LOAD_FAST                'executor'
              178  STORE_ATTR               _shutdown
            180_0  COME_FROM           172  '172'

 L. 102       180  LOAD_FAST                'work_queue'
              182  LOAD_METHOD              put
              184  LOAD_CONST               None
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L. 103       190  POP_BLOCK        
              192  LOAD_CONST               None
              194  RETURN_VALUE     
            196_0  COME_FROM           164  '164'

 L. 104       196  DELETE_FAST              'executor'
              198  JUMP_BACK            84  'to 84'
              200  POP_BLOCK        
              202  JUMP_FORWARD        240  'to 240'
            204_0  COME_FROM_FINALLY    82  '82'

 L. 105       204  DUP_TOP          
              206  LOAD_GLOBAL              BaseException
              208  COMPARE_OP               exception-match
              210  POP_JUMP_IF_FALSE   238  'to 238'
              212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          

 L. 106       218  LOAD_GLOBAL              _base
              220  LOAD_ATTR                LOGGER
              222  LOAD_ATTR                critical
              224  LOAD_STR                 'Exception in worker'
              226  LOAD_CONST               True
              228  LOAD_CONST               ('exc_info',)
              230  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              232  POP_TOP          
              234  POP_EXCEPT       
              236  JUMP_FORWARD        240  'to 240'
            238_0  COME_FROM           210  '210'
              238  END_FINALLY      
            240_0  COME_FROM           236  '236'
            240_1  COME_FROM           202  '202'

Parse error at or near `LOAD_CONST' instruction at offset 76


class BrokenThreadPool(_base.BrokenExecutor):
    __doc__ = '\n    Raised when a worker thread in a ThreadPoolExecutor failed initializing.\n    '


class ThreadPoolExecutor(_base.Executor):
    _counter = itertools.count().__next__

    def __init__(self, max_workers=None, thread_name_prefix='', initializer=None, initargs=()):
        """Initializes a new ThreadPoolExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            initializer: A callable used to initialize worker threads.
            initargs: A tuple of arguments to pass to the initializer.
        """
        if max_workers is None:
            max_workers = min(32, (os.cpu_count() or 1) + 4)
        else:
            if max_workers <= 0:
                raise ValueError('max_workers must be greater than 0')
            if initializer is not None and not callable(initializer):
                raise TypeError('initializer must be a callable')
        self._max_workers = max_workers
        self._work_queue = queue.SimpleQueue()
        self._idle_semaphore = threading.Semaphore(0)
        self._threads = set
        self._broken = False
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._thread_name_prefix = thread_name_prefix or 'ThreadPoolExecutor-%d' % self._counter()
        self._initializer = initializer
        self._initargs = initargs

    def submit--- This code section failed: ---

 L. 159         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'args'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               2
                8  COMPARE_OP               >=
               10  POP_JUMP_IF_FALSE    24  'to 24'

 L. 160        12  LOAD_FAST                'args'
               14  UNPACK_EX_2+0           
               16  STORE_FAST               'self'
               18  STORE_FAST               'fn'
               20  STORE_FAST               'args'
               22  JUMP_FORWARD        110  'to 110'
             24_0  COME_FROM            10  '10'

 L. 161        24  LOAD_FAST                'args'
               26  POP_JUMP_IF_TRUE     38  'to 38'

 L. 162        28  LOAD_GLOBAL              TypeError
               30  LOAD_STR                 "descriptor 'submit' of 'ThreadPoolExecutor' object needs an argument"
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
               36  JUMP_FORWARD        110  'to 110'
             38_0  COME_FROM            26  '26'

 L. 164        38  LOAD_STR                 'fn'
               40  LOAD_FAST                'kwargs'
               42  COMPARE_OP               in
               44  POP_JUMP_IF_FALSE    90  'to 90'

 L. 165        46  LOAD_FAST                'kwargs'
               48  LOAD_METHOD              pop
               50  LOAD_STR                 'fn'
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               'fn'

 L. 166        56  LOAD_FAST                'args'
               58  UNPACK_EX_1+0           
               60  STORE_FAST               'self'
               62  STORE_FAST               'args'

 L. 167        64  LOAD_CONST               0
               66  LOAD_CONST               None
               68  IMPORT_NAME              warnings
               70  STORE_FAST               'warnings'

 L. 168        72  LOAD_FAST                'warnings'
               74  LOAD_ATTR                warn
               76  LOAD_STR                 "Passing 'fn' as keyword argument is deprecated"

 L. 169        78  LOAD_GLOBAL              DeprecationWarning

 L. 169        80  LOAD_CONST               2

 L. 168        82  LOAD_CONST               ('stacklevel',)
               84  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               86  POP_TOP          
               88  JUMP_FORWARD        110  'to 110'
             90_0  COME_FROM            44  '44'

 L. 171        90  LOAD_GLOBAL              TypeError
               92  LOAD_STR                 'submit expected at least 1 positional argument, got %d'

 L. 172        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'args'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               1
              102  BINARY_SUBTRACT  

 L. 171       104  BINARY_MODULO    
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM            88  '88'
            110_1  COME_FROM            36  '36'
            110_2  COME_FROM            22  '22'

 L. 174       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _shutdown_lock
              114  SETUP_WITH          218  'to 218'
              116  POP_TOP          

 L. 175       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _broken
              122  POP_JUMP_IF_FALSE   134  'to 134'

 L. 176       124  LOAD_GLOBAL              BrokenThreadPool
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                _broken
              130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           122  '122'

 L. 178       134  LOAD_FAST                'self'
              136  LOAD_ATTR                _shutdown
              138  POP_JUMP_IF_FALSE   148  'to 148'

 L. 179       140  LOAD_GLOBAL              RuntimeError
              142  LOAD_STR                 'cannot schedule new futures after shutdown'
              144  CALL_FUNCTION_1       1  ''
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           138  '138'

 L. 180       148  LOAD_GLOBAL              _shutdown
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L. 181       152  LOAD_GLOBAL              RuntimeError
              154  LOAD_STR                 'cannot schedule new futures after interpreter shutdown'
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
            160_0  COME_FROM           150  '150'

 L. 184       160  LOAD_GLOBAL              _base
              162  LOAD_METHOD              Future
              164  CALL_METHOD_0         0  ''
              166  STORE_FAST               'f'

 L. 185       168  LOAD_GLOBAL              _WorkItem
              170  LOAD_FAST                'f'
              172  LOAD_FAST                'fn'
              174  LOAD_FAST                'args'
              176  LOAD_FAST                'kwargs'
              178  CALL_FUNCTION_4       4  ''
              180  STORE_FAST               'w'

 L. 187       182  LOAD_FAST                'self'
              184  LOAD_ATTR                _work_queue
              186  LOAD_METHOD              put
              188  LOAD_FAST                'w'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          

 L. 188       194  LOAD_FAST                'self'
              196  LOAD_METHOD              _adjust_thread_count
              198  CALL_METHOD_0         0  ''
              200  POP_TOP          

 L. 189       202  LOAD_FAST                'f'
              204  POP_BLOCK        
              206  ROT_TWO          
              208  BEGIN_FINALLY    
              210  WITH_CLEANUP_START
              212  WITH_CLEANUP_FINISH
              214  POP_FINALLY           0  ''
              216  RETURN_VALUE     
            218_0  COME_FROM_WITH      114  '114'
              218  WITH_CLEANUP_START
              220  WITH_CLEANUP_FINISH
              222  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 206

    submit.__text_signature__ = _base.Executor.submit.__text_signature__
    submit.__doc__ = _base.Executor.submit.__doc__

    def _adjust_thread_count(self):
        if self._idle_semaphore.acquire(timeout=0):
            return

        def weakref_cb(_, q=self._work_queue):
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self._thread_name_prefix or self,
             num_threads)
            t = threading.Thread(name=thread_name, target=_worker, args=(
             weakref.ref(self, weakref_cb),
             self._work_queue,
             self._initializer,
             self._initargs))
            t.daemon = True
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue

    def _initializer_failed(self):
        with self._shutdown_lock:
            self._broken = 'A thread initializer failed, the thread pool is not usable anymore'
            while True:
                try:
                    work_item = self._work_queue.get_nowait()
                except queue.Empty:
                    break
                else:
                    if work_item is not None:
                        work_item.future.set_exception(BrokenThreadPool(self._broken))

    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown = True
            self._work_queue.put(None)
        if wait:
            for t in self._threads:
                t.join()

    shutdown.__doc__ = _base.Executor.shutdown.__doc__