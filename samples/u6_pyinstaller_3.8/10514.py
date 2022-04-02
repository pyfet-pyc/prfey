# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\pool.py
__all__ = [
 'Pool', 'ThreadPool']
import collections, itertools, os, queue, threading, time, traceback, warnings
from queue import Empty
from . import util
from . import get_context, TimeoutError
from .connection import wait
INIT = 'INIT'
RUN = 'RUN'
CLOSE = 'CLOSE'
TERMINATE = 'TERMINATE'
job_counter = itertools.count()

def mapstar(args):
    return list(map(*args))


def starmapstar(args):
    return list(itertools.starmap(args[0], args[1]))


class RemoteTraceback(Exception):

    def __init__(self, tb):
        self.tb = tb

    def __str__(self):
        return self.tb


class ExceptionWithTraceback:

    def __init__(self, exc, tb):
        tb = traceback.format_exception(type(exc), exc, tb)
        tb = ''.join(tb)
        self.exc = exc
        self.tb = '\n"""\n%s"""' % tb

    def __reduce__(self):
        return (rebuild_exc, (self.exc, self.tb))


def rebuild_exc(exc, tb):
    exc.__cause__ = RemoteTraceback(tb)
    return exc


class MaybeEncodingError(Exception):
    __doc__ = 'Wraps possible unpickleable errors, so they can be\n    safely sent through the socket.'

    def __init__(self, exc, value):
        self.exc = repr(exc)
        self.value = repr(value)
        super(MaybeEncodingError, self).__init__(self.exc, self.value)

    def __str__(self):
        return "Error sending result: '%s'. Reason: '%s'" % (self.value,
         self.exc)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)


def worker--- This code section failed: ---

 L.  99         0  LOAD_FAST                'maxtasks'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    40  'to 40'
                8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'maxtasks'
               12  LOAD_GLOBAL              int
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 100        18  LOAD_FAST                'maxtasks'
               20  LOAD_CONST               1
               22  COMPARE_OP               >=

 L.  99        24  POP_JUMP_IF_TRUE     40  'to 40'
             26_0  COME_FROM            16  '16'

 L. 101        26  LOAD_ASSERT              AssertionError
               28  LOAD_STR                 'Maxtasks {!r} is not valid'
               30  LOAD_METHOD              format
               32  LOAD_FAST                'maxtasks'
               34  CALL_METHOD_1         1  ''
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            24  '24'
             40_1  COME_FROM             6  '6'

 L. 102        40  LOAD_FAST                'outqueue'
               42  LOAD_ATTR                put
               44  STORE_FAST               'put'

 L. 103        46  LOAD_FAST                'inqueue'
               48  LOAD_ATTR                get
               50  STORE_FAST               'get'

 L. 104        52  LOAD_GLOBAL              hasattr
               54  LOAD_FAST                'inqueue'
               56  LOAD_STR                 '_writer'
               58  CALL_FUNCTION_2       2  ''
               60  POP_JUMP_IF_FALSE    82  'to 82'

 L. 105        62  LOAD_FAST                'inqueue'
               64  LOAD_ATTR                _writer
               66  LOAD_METHOD              close
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          

 L. 106        72  LOAD_FAST                'outqueue'
               74  LOAD_ATTR                _reader
               76  LOAD_METHOD              close
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          
             82_0  COME_FROM            60  '60'

 L. 108        82  LOAD_FAST                'initializer'
               84  LOAD_CONST               None
               86  COMPARE_OP               is-not
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 109        90  LOAD_FAST                'initializer'
               92  LOAD_FAST                'initargs'
               94  CALL_FUNCTION_EX      0  'positional arguments only'
               96  POP_TOP          
             98_0  COME_FROM            88  '88'

 L. 111        98  LOAD_CONST               0
              100  STORE_FAST               'completed'

 L. 112       102  LOAD_FAST                'maxtasks'
              104  LOAD_CONST               None
              106  COMPARE_OP               is
              108  POP_JUMP_IF_TRUE    126  'to 126'
              110  LOAD_FAST                'maxtasks'
          112_114  POP_JUMP_IF_FALSE   442  'to 442'
              116  LOAD_FAST                'completed'
              118  LOAD_FAST                'maxtasks'
              120  COMPARE_OP               <
          122_124  POP_JUMP_IF_FALSE   442  'to 442'
            126_0  COME_FROM           108  '108'

 L. 113       126  SETUP_FINALLY       138  'to 138'

 L. 114       128  LOAD_FAST                'get'
              130  CALL_FUNCTION_0       0  ''
              132  STORE_FAST               'task'
              134  POP_BLOCK        
              136  JUMP_FORWARD        178  'to 178'
            138_0  COME_FROM_FINALLY   126  '126'

 L. 115       138  DUP_TOP          
              140  LOAD_GLOBAL              EOFError
              142  LOAD_GLOBAL              OSError
              144  BUILD_TUPLE_2         2 
              146  COMPARE_OP               exception-match
              148  POP_JUMP_IF_FALSE   176  'to 176'
              150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L. 116       156  LOAD_GLOBAL              util
              158  LOAD_METHOD              debug
              160  LOAD_STR                 'worker got EOFError or OSError -- exiting'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          

 L. 117       166  POP_EXCEPT       
          168_170  JUMP_ABSOLUTE       442  'to 442'
              172  POP_EXCEPT       
              174  JUMP_FORWARD        178  'to 178'
            176_0  COME_FROM           148  '148'
              176  END_FINALLY      
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           136  '136'

 L. 119       178  LOAD_FAST                'task'
              180  LOAD_CONST               None
              182  COMPARE_OP               is
              184  POP_JUMP_IF_FALSE   200  'to 200'

 L. 120       186  LOAD_GLOBAL              util
              188  LOAD_METHOD              debug
              190  LOAD_STR                 'worker got sentinel -- exiting'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          

 L. 121   196_198  BREAK_LOOP          442  'to 442'
            200_0  COME_FROM           184  '184'

 L. 123       200  LOAD_FAST                'task'
              202  UNPACK_SEQUENCE_5     5 
              204  STORE_FAST               'job'
              206  STORE_FAST               'i'
              208  STORE_FAST               'func'
              210  STORE_FAST               'args'
              212  STORE_FAST               'kwds'

 L. 124       214  SETUP_FINALLY       234  'to 234'

 L. 125       216  LOAD_CONST               True
              218  LOAD_FAST                'func'
              220  LOAD_FAST                'args'
              222  LOAD_FAST                'kwds'
              224  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              226  BUILD_TUPLE_2         2 
              228  STORE_FAST               'result'
              230  POP_BLOCK        
              232  JUMP_FORWARD        306  'to 306'
            234_0  COME_FROM_FINALLY   214  '214'

 L. 126       234  DUP_TOP          
              236  LOAD_GLOBAL              Exception
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   304  'to 304'
              244  POP_TOP          
              246  STORE_FAST               'e'
              248  POP_TOP          
              250  SETUP_FINALLY       292  'to 292'

 L. 127       252  LOAD_FAST                'wrap_exception'
          254_256  POP_JUMP_IF_FALSE   280  'to 280'
              258  LOAD_FAST                'func'
              260  LOAD_GLOBAL              _helper_reraises_exception
              262  COMPARE_OP               is-not
          264_266  POP_JUMP_IF_FALSE   280  'to 280'

 L. 128       268  LOAD_GLOBAL              ExceptionWithTraceback
              270  LOAD_FAST                'e'
              272  LOAD_FAST                'e'
              274  LOAD_ATTR                __traceback__
              276  CALL_FUNCTION_2       2  ''
              278  STORE_FAST               'e'
            280_0  COME_FROM           264  '264'
            280_1  COME_FROM           254  '254'

 L. 129       280  LOAD_CONST               False
              282  LOAD_FAST                'e'
              284  BUILD_TUPLE_2         2 
              286  STORE_FAST               'result'
              288  POP_BLOCK        
              290  BEGIN_FINALLY    
            292_0  COME_FROM_FINALLY   250  '250'
              292  LOAD_CONST               None
              294  STORE_FAST               'e'
              296  DELETE_FAST              'e'
              298  END_FINALLY      
              300  POP_EXCEPT       
              302  JUMP_FORWARD        306  'to 306'
            304_0  COME_FROM           240  '240'
              304  END_FINALLY      
            306_0  COME_FROM           302  '302'
            306_1  COME_FROM           232  '232'

 L. 130       306  SETUP_FINALLY       326  'to 326'

 L. 131       308  LOAD_FAST                'put'
              310  LOAD_FAST                'job'
              312  LOAD_FAST                'i'
              314  LOAD_FAST                'result'
              316  BUILD_TUPLE_3         3 
              318  CALL_FUNCTION_1       1  ''
              320  POP_TOP          
              322  POP_BLOCK        
              324  JUMP_FORWARD        408  'to 408'
            326_0  COME_FROM_FINALLY   306  '306'

 L. 132       326  DUP_TOP          
              328  LOAD_GLOBAL              Exception
              330  COMPARE_OP               exception-match
          332_334  POP_JUMP_IF_FALSE   406  'to 406'
              336  POP_TOP          
              338  STORE_FAST               'e'
              340  POP_TOP          
              342  SETUP_FINALLY       394  'to 394'

 L. 133       344  LOAD_GLOBAL              MaybeEncodingError
              346  LOAD_FAST                'e'
              348  LOAD_FAST                'result'
              350  LOAD_CONST               1
              352  BINARY_SUBSCR    
              354  CALL_FUNCTION_2       2  ''
              356  STORE_FAST               'wrapped'

 L. 134       358  LOAD_GLOBAL              util
              360  LOAD_METHOD              debug
              362  LOAD_STR                 'Possible encoding error while sending result: %s'

 L. 135       364  LOAD_FAST                'wrapped'

 L. 134       366  BINARY_MODULO    
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          

 L. 136       372  LOAD_FAST                'put'
              374  LOAD_FAST                'job'
              376  LOAD_FAST                'i'
              378  LOAD_CONST               False
              380  LOAD_FAST                'wrapped'
              382  BUILD_TUPLE_2         2 
              384  BUILD_TUPLE_3         3 
              386  CALL_FUNCTION_1       1  ''
              388  POP_TOP          
              390  POP_BLOCK        
              392  BEGIN_FINALLY    
            394_0  COME_FROM_FINALLY   342  '342'
              394  LOAD_CONST               None
              396  STORE_FAST               'e'
              398  DELETE_FAST              'e'
              400  END_FINALLY      
              402  POP_EXCEPT       
              404  JUMP_FORWARD        408  'to 408'
            406_0  COME_FROM           332  '332'
              406  END_FINALLY      
            408_0  COME_FROM           404  '404'
            408_1  COME_FROM           324  '324'

 L. 138       408  LOAD_CONST               None
              410  DUP_TOP          
              412  STORE_FAST               'task'
              414  DUP_TOP          
              416  STORE_FAST               'job'
              418  DUP_TOP          
              420  STORE_FAST               'result'
              422  DUP_TOP          
              424  STORE_FAST               'func'
              426  DUP_TOP          
              428  STORE_FAST               'args'
              430  STORE_FAST               'kwds'

 L. 139       432  LOAD_FAST                'completed'
              434  LOAD_CONST               1
              436  INPLACE_ADD      
              438  STORE_FAST               'completed'
              440  JUMP_BACK           102  'to 102'
            442_0  COME_FROM           122  '122'
            442_1  COME_FROM           112  '112'

 L. 140       442  LOAD_GLOBAL              util
              444  LOAD_METHOD              debug
              446  LOAD_STR                 'worker exiting after %d tasks'
              448  LOAD_FAST                'completed'
              450  BINARY_MODULO    
              452  CALL_METHOD_1         1  ''
              454  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 172


def _helper_reraises_exception(ex):
    """Pickle-able helper function for use by _guarded_task_generation."""
    raise ex


class _PoolCache(dict):
    __doc__ = '\n    Class that implements a cache for the Pool class that will notify\n    the pool management threads every time the cache is emptied. The\n    notification is done by the use of a queue that is provided when\n    instantiating the cache.\n    '

    def __init__(self, *args, notifier=None, **kwds):
        self.notifier = notifier
        (super.__init__)(*args, **kwds)

    def __delitem__(self, item):
        super.__delitem__(item)
        if not self:
            self.notifier.put(None)


class Pool(object):
    __doc__ = '\n    Class which supports an async version of applying functions to arguments.\n    '
    _wrap_exception = True

    @staticmethod
    def Process(ctx, *args, **kwds):
        return (ctx.Process)(*args, **kwds)

    def __init__(self, processes=None, initializer=None, initargs=(), maxtasksperchild=None, context=None):
        self._pool = []
        self._state = INIT
        self._ctx = context or get_context
        self._setup_queues()
        self._taskqueue = queue.SimpleQueue()
        self._change_notifier = self._ctx.SimpleQueue()
        self._cache = _PoolCache(notifier=(self._change_notifier))
        self._maxtasksperchild = maxtasksperchild
        self._initializer = initializer
        self._initargs = initargs
        if processes is None:
            processes = os.cpu_count() or 1
        if processes < 1:
            raise ValueError('Number of processes must be at least 1')
        if initializer is not None:
            if not callable(initializer):
                raise TypeError('initializer must be a callable')
        self._processes = processes
        try:
            self._repopulate_pool()
        except Exception:
            for p in self._pool:
                if p.exitcode is None:
                    p.terminate()
            else:
                for p in self._pool:
                    p.join()
                else:
                    raise

        else:
            sentinels = self._get_sentinels()
            self._worker_handler = threading.Thread(target=(Pool._handle_workers),
              args=(
             self._cache, self._taskqueue, self._ctx, self.Process,
             self._processes, self._pool, self._inqueue, self._outqueue,
             self._initializer, self._initargs, self._maxtasksperchild,
             self._wrap_exception, sentinels, self._change_notifier))
            self._worker_handler.daemon = True
            self._worker_handler._state = RUN
            self._worker_handler.start()
            self._task_handler = threading.Thread(target=(Pool._handle_tasks),
              args=(
             self._taskqueue, self._quick_put, self._outqueue,
             self._pool, self._cache))
            self._task_handler.daemon = True
            self._task_handler._state = RUN
            self._task_handler.start()
            self._result_handler = threading.Thread(target=(Pool._handle_results),
              args=(
             self._outqueue, self._quick_get, self._cache))
            self._result_handler.daemon = True
            self._result_handler._state = RUN
            self._result_handler.start()
            self._terminate = util.Finalize(self,
              (self._terminate_pool), args=(
             self._taskqueue, self._inqueue, self._outqueue, self._pool,
             self._change_notifier, self._worker_handler, self._task_handler,
             self._result_handler, self._cache),
              exitpriority=15)
            self._state = RUN

    def __del__(self, _warn=warnings.warn, RUN=RUN):
        if self._state == RUN:
            _warn(f"unclosed running multiprocessing pool {self!r}", ResourceWarning,
              source=self)
            if getattr(self, '_change_notifier', None) is not None:
                self._change_notifier.put(None)

    def __repr__(self):
        cls = self.__class__
        return f"<{cls.__module__}.{cls.__qualname__} state={self._state} pool_size={len(self._pool)}>"

    def _get_sentinels(self):
        task_queue_sentinels = [
         self._outqueue._reader]
        self_notifier_sentinels = [self._change_notifier._reader]
        return [*task_queue_sentinels, *self_notifier_sentinels]

    @staticmethod
    def _get_worker_sentinels(workers):
        return [worker.sentinel for worker in workers if hasattr(worker, 'sentinel')]

    @staticmethod
    def _join_exited_workers(pool):
        """Cleanup after any worker processes which have exited due to reaching
        their specified lifetime.  Returns True if any workers were cleaned up.
        """
        cleaned = False
        for i in reversed(range(len(pool))):
            worker = pool[i]
            if worker.exitcode is not None:
                util.debug('cleaning up worker %d' % i)
                worker.join()
                cleaned = True
                del pool[i]
            return cleaned

    def _repopulate_pool(self):
        return self._repopulate_pool_static(self._ctx, self.Process, self._processes, self._pool, self._inqueue, self._outqueue, self._initializer, self._initargs, self._maxtasksperchild, self._wrap_exception)

    @staticmethod
    def _repopulate_pool_static(ctx, Process, processes, pool, inqueue, outqueue, initializer, initargs, maxtasksperchild, wrap_exception):
        """Bring the number of pool processes up to the specified number,
        for use after reaping workers which have exited.
        """
        for i in range(processes - len(pool)):
            w = Process(ctx, target=worker, args=(
             inqueue, outqueue,
             initializer,
             initargs, maxtasksperchild,
             wrap_exception))
            w.name = w.name.replace('Process', 'PoolWorker')
            w.daemon = True
            w.start()
            pool.append(w)
            util.debug('added worker')

    @staticmethod
    def _maintain_pool(ctx, Process, processes, pool, inqueue, outqueue, initializer, initargs, maxtasksperchild, wrap_exception):
        """Clean up any exited workers and start replacements for them.
        """
        if Pool._join_exited_workers(pool):
            Pool._repopulate_pool_static(ctx, Process, processes, pool, inqueue, outqueue, initializer, initargs, maxtasksperchild, wrap_exception)

    def _setup_queues(self):
        self._inqueue = self._ctx.SimpleQueue()
        self._outqueue = self._ctx.SimpleQueue()
        self._quick_put = self._inqueue._writer.send
        self._quick_get = self._outqueue._reader.recv

    def _check_running(self):
        if self._state != RUN:
            raise ValueError('Pool not running')

    def apply(self, func, args=(), kwds={}):
        """
        Equivalent of `func(*args, **kwds)`.
        Pool must be running.
        """
        return self.apply_async(func, args, kwds).get()

    def map(self, func, iterable, chunksize=None):
        """
        Apply `func` to each element in `iterable`, collecting the results
        in a list that is returned.
        """
        return self._map_async(func, iterable, mapstar, chunksize).get()

    def starmap(self, func, iterable, chunksize=None):
        """
        Like `map()` method but the elements of the `iterable` are expected to
        be iterables as well and will be unpacked as arguments. Hence
        `func` and (a, b) becomes func(a, b).
        """
        return self._map_async(func, iterable, starmapstar, chunksize).get()

    def starmap_async(self, func, iterable, chunksize=None, callback=None, error_callback=None):
        """
        Asynchronous version of `starmap()` method.
        """
        return self._map_async(func, iterable, starmapstar, chunksize, callback, error_callback)

    def _guarded_task_generation(self, result_job, func, iterable):
        """Provides a generator of tasks for imap and imap_unordered with
        appropriate handling for iterables which throw exceptions during
        iteration."""
        try:
            i = -1
            for i, x in enumerate(iterable):
                (yield (
                 result_job, i, func, (x,), {}))

        except Exception as e:
            try:
                (yield (
                 result_job, i + 1, _helper_reraises_exception, (e,), {}))
            finally:
                e = None
                del e

    def imap(self, func, iterable, chunksize=1):
        """
        Equivalent of `map()` -- can be MUCH slower than `Pool.map()`.
        """
        self._check_running()
        if chunksize == 1:
            result = IMapIterator(self)
            self._taskqueue.put((
             self._guarded_task_generation(result._job, func, iterable),
             result._set_length))
            return result
        if chunksize < 1:
            raise ValueError('Chunksize must be 1+, not {0:n}'.format(chunksize))
        task_batches = Pool._get_tasks(func, iterable, chunksize)
        result = IMapIterator(self)
        self._taskqueue.put((
         self._guarded_task_generation(result._job, mapstar, task_batches),
         result._set_length))
        return (item for chunk in result for item in chunk)

    def imap_unordered(self, func, iterable, chunksize=1):
        """
        Like `imap()` method but ordering of results is arbitrary.
        """
        self._check_running()
        if chunksize == 1:
            result = IMapUnorderedIterator(self)
            self._taskqueue.put((
             self._guarded_task_generation(result._job, func, iterable),
             result._set_length))
            return result
        if chunksize < 1:
            raise ValueError('Chunksize must be 1+, not {0!r}'.format(chunksize))
        task_batches = Pool._get_tasks(func, iterable, chunksize)
        result = IMapUnorderedIterator(self)
        self._taskqueue.put((
         self._guarded_task_generation(result._job, mapstar, task_batches),
         result._set_length))
        return (item for chunk in result for item in chunk)

    def apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
        """
        Asynchronous version of `apply()` method.
        """
        self._check_running()
        result = ApplyResult(self, callback, error_callback)
        self._taskqueue.put(([(result._job, 0, func, args, kwds)], None))
        return result

    def map_async(self, func, iterable, chunksize=None, callback=None, error_callback=None):
        """
        Asynchronous version of `map()` method.
        """
        return self._map_async(func, iterable, mapstar, chunksize, callback, error_callback)

    def _map_async(self, func, iterable, mapper, chunksize=None, callback=None, error_callback=None):
        """
        Helper function to implement map, starmap and their async counterparts.
        """
        self._check_running()
        if not hasattr(iterable, '__len__'):
            iterable = list(iterable)
        if chunksize is None:
            chunksize, extra = divmod(len(iterable), len(self._pool) * 4)
            if extra:
                chunksize += 1
        if len(iterable) == 0:
            chunksize = 0
        task_batches = Pool._get_tasks(func, iterable, chunksize)
        result = MapResult(self, chunksize, (len(iterable)), callback, error_callback=error_callback)
        self._taskqueue.put((
         self._guarded_task_generation(result._job, mapper, task_batches),
         None))
        return result

    @staticmethod
    def _wait_for_updates(sentinels, change_notifier, timeout=None):
        wait(sentinels, timeout=timeout)
        while not change_notifier.empty():
            change_notifier.get()

    @classmethod
    def _handle_workers(cls, cache, taskqueue, ctx, Process, processes, pool, inqueue, outqueue, initializer, initargs, maxtasksperchild, wrap_exception, sentinels, change_notifier):
        thread = threading.current_thread()
        while not thread._state == RUN:
            if cache:
                if thread._state != TERMINATE:
                    cls._maintain_pool(ctx, Process, processes, pool, inqueue, outqueue, initializer, initargs, maxtasksperchild, wrap_exception)
                    current_sentinels = [
                     *cls._get_worker_sentinels(pool), *sentinels]
                    cls._wait_for_updates(current_sentinels, change_notifier)

        taskqueue.put(None)
        util.debug('worker handler exiting')

    @staticmethod
    def _handle_tasks--- This code section failed: ---

 L. 526         0  LOAD_GLOBAL              threading
                2  LOAD_METHOD              current_thread
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'thread'

 L. 528         8  LOAD_GLOBAL              iter
               10  LOAD_FAST                'taskqueue'
               12  LOAD_ATTR                get
               14  LOAD_CONST               None
               16  CALL_FUNCTION_2       2  ''
               18  GET_ITER         
               20  FOR_ITER            256  'to 256'
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'taskseq'
               26  STORE_FAST               'set_length'

 L. 529        28  LOAD_CONST               None
               30  STORE_FAST               'task'

 L. 530        32  SETUP_FINALLY       240  'to 240'

 L. 532        34  LOAD_FAST                'taskseq'
               36  GET_ITER         
               38  FOR_ITER            178  'to 178'
               40  STORE_FAST               'task'

 L. 533        42  LOAD_FAST                'thread'
               44  LOAD_ATTR                _state
               46  LOAD_GLOBAL              RUN
               48  COMPARE_OP               !=
               50  POP_JUMP_IF_FALSE    66  'to 66'

 L. 534        52  LOAD_GLOBAL              util
               54  LOAD_METHOD              debug
               56  LOAD_STR                 'task handler found thread._state != RUN'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 535        62  POP_TOP          
               64  BREAK_LOOP          226  'to 226'
             66_0  COME_FROM            50  '50'

 L. 536        66  SETUP_FINALLY        80  'to 80'

 L. 537        68  LOAD_FAST                'put'
               70  LOAD_FAST                'task'
               72  CALL_FUNCTION_1       1  ''
               74  POP_TOP          
               76  POP_BLOCK        
               78  JUMP_BACK            38  'to 38'
             80_0  COME_FROM_FINALLY    66  '66'

 L. 538        80  DUP_TOP          
               82  LOAD_GLOBAL              Exception
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   174  'to 174'
               88  POP_TOP          
               90  STORE_FAST               'e'
               92  POP_TOP          
               94  SETUP_FINALLY       162  'to 162'

 L. 539        96  LOAD_FAST                'task'
               98  LOAD_CONST               None
              100  LOAD_CONST               2
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_FAST               'job'
              110  STORE_FAST               'idx'

 L. 540       112  SETUP_FINALLY       138  'to 138'

 L. 541       114  LOAD_FAST                'cache'
              116  LOAD_FAST                'job'
              118  BINARY_SUBSCR    
              120  LOAD_METHOD              _set
              122  LOAD_FAST                'idx'
              124  LOAD_CONST               False
              126  LOAD_FAST                'e'
              128  BUILD_TUPLE_2         2 
              130  CALL_METHOD_2         2  ''
              132  POP_TOP          
              134  POP_BLOCK        
              136  JUMP_FORWARD        158  'to 158'
            138_0  COME_FROM_FINALLY   112  '112'

 L. 542       138  DUP_TOP          
              140  LOAD_GLOBAL              KeyError
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   156  'to 156'
              146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L. 543       152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM           144  '144'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM           136  '136'
              158  POP_BLOCK        
              160  BEGIN_FINALLY    
            162_0  COME_FROM_FINALLY    94  '94'
              162  LOAD_CONST               None
              164  STORE_FAST               'e'
              166  DELETE_FAST              'e'
              168  END_FINALLY      
              170  POP_EXCEPT       
              172  JUMP_BACK            38  'to 38'
            174_0  COME_FROM            86  '86'
              174  END_FINALLY      
              176  JUMP_BACK            38  'to 38'

 L. 545       178  LOAD_FAST                'set_length'
              180  POP_JUMP_IF_FALSE   220  'to 220'

 L. 546       182  LOAD_GLOBAL              util
              184  LOAD_METHOD              debug
              186  LOAD_STR                 'doing set_length()'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L. 547       192  LOAD_FAST                'task'
              194  POP_JUMP_IF_FALSE   204  'to 204'
              196  LOAD_FAST                'task'
              198  LOAD_CONST               1
              200  BINARY_SUBSCR    
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           194  '194'
              204  LOAD_CONST               -1
            206_0  COME_FROM           202  '202'
              206  STORE_FAST               'idx'

 L. 548       208  LOAD_FAST                'set_length'
              210  LOAD_FAST                'idx'
              212  LOAD_CONST               1
              214  BINARY_ADD       
              216  CALL_FUNCTION_1       1  ''
              218  POP_TOP          
            220_0  COME_FROM           180  '180'

 L. 549       220  POP_BLOCK        
              222  CALL_FINALLY        240  'to 240'
              224  JUMP_BACK            20  'to 20'

 L. 550       226  POP_BLOCK        
              228  CALL_FINALLY        240  'to 240'
              230  POP_TOP          
          232_234  JUMP_ABSOLUTE       266  'to 266'
              236  POP_BLOCK        
              238  BEGIN_FINALLY    
            240_0  COME_FROM           228  '228'
            240_1  COME_FROM           222  '222'
            240_2  COME_FROM_FINALLY    32  '32'

 L. 552       240  LOAD_CONST               None
              242  DUP_TOP          
              244  STORE_FAST               'task'
              246  DUP_TOP          
              248  STORE_FAST               'taskseq'
              250  STORE_FAST               'job'
              252  END_FINALLY      
              254  JUMP_BACK            20  'to 20'

 L. 554       256  LOAD_GLOBAL              util
              258  LOAD_METHOD              debug
              260  LOAD_STR                 'task handler got sentinel'
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          

 L. 556       266  SETUP_FINALLY       322  'to 322'

 L. 558       268  LOAD_GLOBAL              util
              270  LOAD_METHOD              debug
              272  LOAD_STR                 'task handler sending sentinel to result handler'
              274  CALL_METHOD_1         1  ''
              276  POP_TOP          

 L. 559       278  LOAD_FAST                'outqueue'
              280  LOAD_METHOD              put
              282  LOAD_CONST               None
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L. 562       288  LOAD_GLOBAL              util
              290  LOAD_METHOD              debug
              292  LOAD_STR                 'task handler sending sentinel to workers'
              294  CALL_METHOD_1         1  ''
              296  POP_TOP          

 L. 563       298  LOAD_FAST                'pool'
              300  GET_ITER         
              302  FOR_ITER            318  'to 318'
              304  STORE_FAST               'p'

 L. 564       306  LOAD_FAST                'put'
              308  LOAD_CONST               None
              310  CALL_FUNCTION_1       1  ''
              312  POP_TOP          
          314_316  JUMP_BACK           302  'to 302'
              318  POP_BLOCK        
              320  JUMP_FORWARD        354  'to 354'
            322_0  COME_FROM_FINALLY   266  '266'

 L. 565       322  DUP_TOP          
              324  LOAD_GLOBAL              OSError
              326  COMPARE_OP               exception-match
          328_330  POP_JUMP_IF_FALSE   352  'to 352'
              332  POP_TOP          
              334  POP_TOP          
              336  POP_TOP          

 L. 566       338  LOAD_GLOBAL              util
              340  LOAD_METHOD              debug
              342  LOAD_STR                 'task handler got OSError when sending sentinels'
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          
              348  POP_EXCEPT       
              350  JUMP_FORWARD        354  'to 354'
            352_0  COME_FROM           328  '328'
              352  END_FINALLY      
            354_0  COME_FROM           350  '350'
            354_1  COME_FROM           320  '320'

 L. 568       354  LOAD_GLOBAL              util
              356  LOAD_METHOD              debug
              358  LOAD_STR                 'task handler exiting'
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 222

    @staticmethod
    def _handle_results--- This code section failed: ---

 L. 572         0  LOAD_GLOBAL              threading
                2  LOAD_METHOD              current_thread
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'thread'

 L. 575         8  SETUP_FINALLY        20  'to 20'

 L. 576        10  LOAD_FAST                'get'
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'task'
               16  POP_BLOCK        
               18  JUMP_FORWARD         56  'to 56'
             20_0  COME_FROM_FINALLY     8  '8'

 L. 577        20  DUP_TOP          
               22  LOAD_GLOBAL              OSError
               24  LOAD_GLOBAL              EOFError
               26  BUILD_TUPLE_2         2 
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    54  'to 54'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 578        38  LOAD_GLOBAL              util
               40  LOAD_METHOD              debug
               42  LOAD_STR                 'result handler got EOFError/OSError -- exiting'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 579        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            30  '30'
               54  END_FINALLY      
             56_0  COME_FROM            18  '18'

 L. 581        56  LOAD_FAST                'thread'
               58  LOAD_ATTR                _state
               60  LOAD_GLOBAL              RUN
               62  COMPARE_OP               !=
               64  POP_JUMP_IF_FALSE    96  'to 96'

 L. 582        66  LOAD_FAST                'thread'
               68  LOAD_ATTR                _state
               70  LOAD_GLOBAL              TERMINATE
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_TRUE     84  'to 84'
               76  LOAD_ASSERT              AssertionError
               78  LOAD_STR                 'Thread not in TERMINATE'
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            74  '74'

 L. 583        84  LOAD_GLOBAL              util
               86  LOAD_METHOD              debug
               88  LOAD_STR                 'result handler found thread._state=TERMINATE'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 584        94  BREAK_LOOP          182  'to 182'
             96_0  COME_FROM            64  '64'

 L. 586        96  LOAD_FAST                'task'
               98  LOAD_CONST               None
              100  COMPARE_OP               is
              102  POP_JUMP_IF_FALSE   116  'to 116'

 L. 587       104  LOAD_GLOBAL              util
              106  LOAD_METHOD              debug
              108  LOAD_STR                 'result handler got sentinel'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 588       114  BREAK_LOOP          182  'to 182'
            116_0  COME_FROM           102  '102'

 L. 590       116  LOAD_FAST                'task'
              118  UNPACK_SEQUENCE_3     3 
              120  STORE_FAST               'job'
              122  STORE_FAST               'i'
              124  STORE_FAST               'obj'

 L. 591       126  SETUP_FINALLY       148  'to 148'

 L. 592       128  LOAD_FAST                'cache'
              130  LOAD_FAST                'job'
              132  BINARY_SUBSCR    
              134  LOAD_METHOD              _set
              136  LOAD_FAST                'i'
              138  LOAD_FAST                'obj'
              140  CALL_METHOD_2         2  ''
              142  POP_TOP          
              144  POP_BLOCK        
              146  JUMP_FORWARD        168  'to 168'
            148_0  COME_FROM_FINALLY   126  '126'

 L. 593       148  DUP_TOP          
              150  LOAD_GLOBAL              KeyError
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   166  'to 166'
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 594       162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
            166_0  COME_FROM           154  '154'
              166  END_FINALLY      
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           146  '146'

 L. 595       168  LOAD_CONST               None
              170  DUP_TOP          
              172  STORE_FAST               'task'
              174  DUP_TOP          
              176  STORE_FAST               'job'
              178  STORE_FAST               'obj'
              180  JUMP_BACK             8  'to 8'

 L. 597       182  LOAD_FAST                'cache'
          184_186  POP_JUMP_IF_FALSE   338  'to 338'
              188  LOAD_FAST                'thread'
              190  LOAD_ATTR                _state
              192  LOAD_GLOBAL              TERMINATE
              194  COMPARE_OP               !=
          196_198  POP_JUMP_IF_FALSE   338  'to 338'

 L. 598       200  SETUP_FINALLY       212  'to 212'

 L. 599       202  LOAD_FAST                'get'
              204  CALL_FUNCTION_0       0  ''
              206  STORE_FAST               'task'
              208  POP_BLOCK        
              210  JUMP_FORWARD        248  'to 248'
            212_0  COME_FROM_FINALLY   200  '200'

 L. 600       212  DUP_TOP          
              214  LOAD_GLOBAL              OSError
              216  LOAD_GLOBAL              EOFError
              218  BUILD_TUPLE_2         2 
              220  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   246  'to 246'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 601       230  LOAD_GLOBAL              util
              232  LOAD_METHOD              debug
              234  LOAD_STR                 'result handler got EOFError/OSError -- exiting'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L. 602       240  POP_EXCEPT       
              242  LOAD_CONST               None
              244  RETURN_VALUE     
            246_0  COME_FROM           222  '222'
              246  END_FINALLY      
            248_0  COME_FROM           210  '210'

 L. 604       248  LOAD_FAST                'task'
              250  LOAD_CONST               None
              252  COMPARE_OP               is
          254_256  POP_JUMP_IF_FALSE   270  'to 270'

 L. 605       258  LOAD_GLOBAL              util
              260  LOAD_METHOD              debug
              262  LOAD_STR                 'result handler ignoring extra sentinel'
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          

 L. 606       268  JUMP_BACK           182  'to 182'
            270_0  COME_FROM           254  '254'

 L. 607       270  LOAD_FAST                'task'
              272  UNPACK_SEQUENCE_3     3 
              274  STORE_FAST               'job'
              276  STORE_FAST               'i'
              278  STORE_FAST               'obj'

 L. 608       280  SETUP_FINALLY       302  'to 302'

 L. 609       282  LOAD_FAST                'cache'
              284  LOAD_FAST                'job'
              286  BINARY_SUBSCR    
              288  LOAD_METHOD              _set
              290  LOAD_FAST                'i'
              292  LOAD_FAST                'obj'
              294  CALL_METHOD_2         2  ''
              296  POP_TOP          
              298  POP_BLOCK        
              300  JUMP_FORWARD        324  'to 324'
            302_0  COME_FROM_FINALLY   280  '280'

 L. 610       302  DUP_TOP          
              304  LOAD_GLOBAL              KeyError
              306  COMPARE_OP               exception-match
          308_310  POP_JUMP_IF_FALSE   322  'to 322'
              312  POP_TOP          
              314  POP_TOP          
              316  POP_TOP          

 L. 611       318  POP_EXCEPT       
              320  JUMP_FORWARD        324  'to 324'
            322_0  COME_FROM           308  '308'
              322  END_FINALLY      
            324_0  COME_FROM           320  '320'
            324_1  COME_FROM           300  '300'

 L. 612       324  LOAD_CONST               None
              326  DUP_TOP          
              328  STORE_FAST               'task'
              330  DUP_TOP          
              332  STORE_FAST               'job'
              334  STORE_FAST               'obj'
              336  JUMP_BACK           182  'to 182'
            338_0  COME_FROM           196  '196'
            338_1  COME_FROM           184  '184'

 L. 614       338  LOAD_GLOBAL              hasattr
              340  LOAD_FAST                'outqueue'
              342  LOAD_STR                 '_reader'
              344  CALL_FUNCTION_2       2  ''
          346_348  POP_JUMP_IF_FALSE   432  'to 432'

 L. 615       350  LOAD_GLOBAL              util
              352  LOAD_METHOD              debug
              354  LOAD_STR                 'ensuring that outqueue is not full'
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          

 L. 619       360  SETUP_FINALLY       406  'to 406'

 L. 620       362  LOAD_GLOBAL              range
              364  LOAD_CONST               10
              366  CALL_FUNCTION_1       1  ''
              368  GET_ITER         
              370  FOR_ITER            402  'to 402'
              372  STORE_FAST               'i'

 L. 621       374  LOAD_FAST                'outqueue'
              376  LOAD_ATTR                _reader
              378  LOAD_METHOD              poll
              380  CALL_METHOD_0         0  ''
          382_384  POP_JUMP_IF_TRUE    392  'to 392'

 L. 622       386  POP_TOP          
          388_390  BREAK_LOOP          402  'to 402'
            392_0  COME_FROM           382  '382'

 L. 623       392  LOAD_FAST                'get'
              394  CALL_FUNCTION_0       0  ''
              396  POP_TOP          
          398_400  JUMP_BACK           370  'to 370'
              402  POP_BLOCK        
              404  JUMP_FORWARD        432  'to 432'
            406_0  COME_FROM_FINALLY   360  '360'

 L. 624       406  DUP_TOP          
              408  LOAD_GLOBAL              OSError
              410  LOAD_GLOBAL              EOFError
              412  BUILD_TUPLE_2         2 
              414  COMPARE_OP               exception-match
          416_418  POP_JUMP_IF_FALSE   430  'to 430'
              420  POP_TOP          
              422  POP_TOP          
              424  POP_TOP          

 L. 625       426  POP_EXCEPT       
              428  JUMP_FORWARD        432  'to 432'
            430_0  COME_FROM           416  '416'
              430  END_FINALLY      
            432_0  COME_FROM           428  '428'
            432_1  COME_FROM           404  '404'
            432_2  COME_FROM           346  '346'

 L. 627       432  LOAD_GLOBAL              util
              434  LOAD_METHOD              debug
              436  LOAD_STR                 'result handler exiting: len(cache)=%s, thread._state=%s'

 L. 628       438  LOAD_GLOBAL              len
              440  LOAD_FAST                'cache'
              442  CALL_FUNCTION_1       1  ''

 L. 628       444  LOAD_FAST                'thread'
              446  LOAD_ATTR                _state

 L. 627       448  CALL_METHOD_3         3  ''
              450  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 50

    @staticmethod
    def _get_tasks(func, it, size):
        it = iter(it)
        while True:
            x = tuple(itertools.islice(it, size))
            if not x:
                return
            (yield (
             func, x))

    def __reduce__(self):
        raise NotImplementedError('pool objects cannot be passed between processes or pickled')

    def close(self):
        util.debug('closing pool')
        if self._state == RUN:
            self._state = CLOSE
            self._worker_handler._state = CLOSE
            self._change_notifier.put(None)

    def terminate(self):
        util.debug('terminating pool')
        self._state = TERMINATE
        self._worker_handler._state = TERMINATE
        self._change_notifier.put(None)
        self._terminate()

    def join(self):
        util.debug('joining pool')
        if self._state == RUN:
            raise ValueError('Pool is still running')
        else:
            if self._state not in (CLOSE, TERMINATE):
                raise ValueError('In unknown state')
        self._worker_handler.join()
        self._task_handler.join()
        self._result_handler.join()
        for p in self._pool:
            p.join()

    @staticmethod
    def _help_stuff_finish(inqueue, task_handler, size):
        util.debug('removing tasks from inqueue until task handler finished')
        inqueue._rlock.acquire()
        while task_handler.is_alive():
            if inqueue._reader.poll():
                inqueue._reader.recv()
                time.sleep(0)

    @classmethod
    def _terminate_pool(cls, taskqueue, inqueue, outqueue, pool, change_notifier, worker_handler, task_handler, result_handler, cache):
        util.debug('finalizing pool')
        worker_handler._state = TERMINATE
        task_handler._state = TERMINATE
        util.debug('helping task handler/workers to finish')
        cls._help_stuff_finish(inqueue, task_handler, len(pool))
        if not result_handler.is_alive():
            if len(cache) != 0:
                raise AssertionError('Cannot have cache with result_hander not alive')
        result_handler._state = TERMINATE
        change_notifier.put(None)
        outqueue.put(None)
        util.debug('joining worker handler')
        if threading.current_thread() is not worker_handler:
            worker_handler.join()
        if pool:
            if hasattr(pool[0], 'terminate'):
                util.debug('terminating workers')
                for p in pool:
                    if p.exitcode is None:
                        p.terminate()

        util.debug('joining task handler')
        if threading.current_thread() is not task_handler:
            task_handler.join()
        util.debug('joining result handler')
        if threading.current_thread() is not result_handler:
            result_handler.join()
        if pool:
            if hasattr(pool[0], 'terminate'):
                util.debug('joining pool workers')
                for p in pool:
                    if p.is_alive():
                        util.debug('cleaning up worker %d' % p.pid)
                        p.join()

    def __enter__(self):
        self._check_running()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()


class ApplyResult(object):

    def __init__(self, pool, callback, error_callback):
        self._pool = pool
        self._event = threading.Event()
        self._job = next(job_counter)
        self._cache = pool._cache
        self._callback = callback
        self._error_callback = error_callback
        self._cache[self._job] = self

    def ready(self):
        return self._event.is_set()

    def successful(self):
        if not self.ready():
            raise ValueError('{0!r} not ready'.format(self))
        return self._success

    def wait(self, timeout=None):
        self._event.wait(timeout)

    def get(self, timeout=None):
        self.wait(timeout)
        if not self.ready():
            raise TimeoutError
        if self._success:
            return self._value
        raise self._value

    def _set(self, i, obj):
        self._success, self._value = obj
        if self._callback:
            if self._success:
                self._callback(self._value)
        if self._error_callback:
            if not self._success:
                self._error_callback(self._value)
        self._event.set()
        del self._cache[self._job]
        self._pool = None


AsyncResult = ApplyResult

class MapResult(ApplyResult):

    def __init__(self, pool, chunksize, length, callback, error_callback):
        ApplyResult.__init__(self, pool, callback, error_callback=error_callback)
        self._success = True
        self._value = [None] * length
        self._chunksize = chunksize
        if chunksize <= 0:
            self._number_left = 0
            self._event.set()
            del self._cache[self._job]
        else:
            self._number_left = length // chunksize + bool(length % chunksize)

    def _set(self, i, success_result):
        self._number_left -= 1
        success, result = success_result
        if success and self._success:
            self._value[i * self._chunksize:(i + 1) * self._chunksize] = result
            if self._number_left == 0:
                if self._callback:
                    self._callback(self._value)
                del self._cache[self._job]
                self._event.set()
                self._pool = None
        else:
            if not success:
                if self._success:
                    self._success = False
                    self._value = result
            if self._number_left == 0:
                if self._error_callback:
                    self._error_callback(self._value)
                del self._cache[self._job]
                self._event.set()
                self._pool = None


class IMapIterator(object):

    def __init__(self, pool):
        self._pool = pool
        self._cond = threading.Condition(threading.Lock())
        self._job = next(job_counter)
        self._cache = pool._cache
        self._items = collections.deque()
        self._index = 0
        self._length = None
        self._unsorted = {}
        self._cache[self._job] = self

    def __iter__(self):
        return self

    def next(self, timeout=None):
        with self._cond:
            try:
                item = self._items.popleft()
            except IndexError:
                if self._index == self._length:
                    self._pool = None
                    raise StopIteration from None
                self._cond.wait(timeout)
                try:
                    item = self._items.popleft()
                except IndexError:
                    if self._index == self._length:
                        self._pool = None
                        raise StopIteration from None
                    raise TimeoutError from None

        success, value = item
        if success:
            return value
        raise value

    __next__ = next

    def _set(self, i, obj):
        with self._cond:
            if self._index == i:
                self._items.append(obj)
                self._index += 1
                while self._index in self._unsorted:
                    obj = self._unsorted.pop(self._index)
                    self._items.append(obj)
                    self._index += 1

                self._cond.notify()
            else:
                self._unsorted[i] = obj
            if self._index == self._length:
                del self._cache[self._job]
                self._pool = None

    def _set_length(self, length):
        with self._cond:
            self._length = length
            if self._index == self._length:
                self._cond.notify()
                del self._cache[self._job]
                self._pool = None


class IMapUnorderedIterator(IMapIterator):

    def _set(self, i, obj):
        with self._cond:
            self._items.append(obj)
            self._index += 1
            self._cond.notify()
            if self._index == self._length:
                del self._cache[self._job]
                self._pool = None


class ThreadPool(Pool):
    _wrap_exception = False

    @staticmethod
    def Process(ctx, *args, **kwds):
        from .dummy import Process
        return Process(*args, **kwds)

    def __init__(self, processes=None, initializer=None, initargs=()):
        Pool.__init__(self, processes, initializer, initargs)

    def _setup_queues(self):
        self._inqueue = queue.SimpleQueue()
        self._outqueue = queue.SimpleQueue()
        self._quick_put = self._inqueue.put
        self._quick_get = self._outqueue.get

    def _get_sentinels(self):
        return [
         self._change_notifier._reader]

    @staticmethod
    def _get_worker_sentinels(workers):
        return []

    @staticmethod
    def _help_stuff_finish(inqueue, task_handler, size):
        try:
            while True:
                inqueue.get(block=False)

        except queue.Empty:
            pass
        else:
            for i in range(size):
                inqueue.put(None)

    def _wait_for_updates(self, sentinels, change_notifier, timeout):
        time.sleep(timeout)