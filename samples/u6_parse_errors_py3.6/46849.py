# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\pool.py
__all__ = [
 'Pool', 'ThreadPool']
import threading, queue, itertools, collections, os, time, traceback
from . import util
from . import get_context, TimeoutError
RUN = 0
CLOSE = 1
TERMINATE = 2
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


def worker(inqueue, outqueue, initializer=None, initargs=(), maxtasks=None, wrap_exception=False):
    if not maxtasks is None:
        if not (type(maxtasks) == int and maxtasks > 0):
            raise AssertionError
    else:
        put = outqueue.put
        get = inqueue.get
        if hasattr(inqueue, '_writer'):
            inqueue._writer.close()
            outqueue._reader.close()
        if initializer is not None:
            initializer(*initargs)
    completed = 0
    while maxtasks is None or maxtasks and completed < maxtasks:
        try:
            task = get()
        except (EOFError, OSError):
            util.debug('worker got EOFError or OSError -- exiting')
            break

        if task is None:
            util.debug('worker got sentinel -- exiting')
            break
        job, i, func, args, kwds = task
        try:
            result = (
             True, func(*args, **kwds))
        except Exception as e:
            if wrap_exception:
                e = ExceptionWithTraceback(e, e.__traceback__)
            result = (
             False, e)

        try:
            put((job, i, result))
        except Exception as e:
            wrapped = MaybeEncodingError(e, result[1])
            util.debug('Possible encoding error while sending result: %s' % wrapped)
            put((job, i, (False, wrapped)))

        completed += 1

    util.debug('worker exiting after %d tasks' % completed)


class Pool(object):
    __doc__ = '\n    Class which supports an async version of applying functions to arguments.\n    '
    _wrap_exception = True

    def Process(self, *args, **kwds):
        return (self._ctx.Process)(*args, **kwds)

    def __init__(self, processes=None, initializer=None, initargs=(), maxtasksperchild=None, context=None):
        self._ctx = context or get_context()
        self._setup_queues()
        self._taskqueue = queue.Queue()
        self._cache = {}
        self._state = RUN
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
        self._pool = []
        self._repopulate_pool()
        self._worker_handler = threading.Thread(target=(Pool._handle_workers),
          args=(
         self,))
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
         self._worker_handler, self._task_handler,
         self._result_handler, self._cache),
          exitpriority=15)

    def _join_exited_workers(self):
        """Cleanup after any worker processes which have exited due to reaching
        their specified lifetime.  Returns True if any workers were cleaned up.
        """
        cleaned = False
        for i in reversed(range(len(self._pool))):
            worker = self._pool[i]
            if worker.exitcode is not None:
                util.debug('cleaning up worker %d' % i)
                worker.join()
                cleaned = True
                del self._pool[i]

        return cleaned

    def _repopulate_pool(self):
        """Bring the number of pool processes up to the specified number,
        for use after reaping workers which have exited.
        """
        for i in range(self._processes - len(self._pool)):
            w = self.Process(target=worker, args=(
             self._inqueue, self._outqueue,
             self._initializer,
             self._initargs, self._maxtasksperchild,
             self._wrap_exception))
            self._pool.append(w)
            w.name = w.name.replace('Process', 'PoolWorker')
            w.daemon = True
            w.start()
            util.debug('added worker')

    def _maintain_pool(self):
        """Clean up any exited workers and start replacements for them.
        """
        if self._join_exited_workers():
            self._repopulate_pool()

    def _setup_queues(self):
        self._inqueue = self._ctx.SimpleQueue()
        self._outqueue = self._ctx.SimpleQueue()
        self._quick_put = self._inqueue._writer.send
        self._quick_get = self._outqueue._reader.recv

    def apply(self, func, args=(), kwds={}):
        """
        Equivalent of `func(*args, **kwds)`.
        """
        assert self._state == RUN
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

    def imap(self, func, iterable, chunksize=1):
        """
        Equivalent of `map()` -- can be MUCH slower than `Pool.map()`.
        """
        if self._state != RUN:
            raise ValueError('Pool not running')
        if chunksize == 1:
            result = IMapIterator(self._cache)
            self._taskqueue.put((
             ((result._job, i, func, (x,), {}) for i, x in enumerate(iterable)), result._set_length))
            return result
        else:
            assert chunksize > 1
            task_batches = Pool._get_tasks(func, iterable, chunksize)
            result = IMapIterator(self._cache)
            self._taskqueue.put((
             ((result._job, i, mapstar, (x,), {}) for i, x in enumerate(task_batches)), result._set_length))
            return (item for chunk in result for item in chunk)

    def imap_unordered(self, func, iterable, chunksize=1):
        """
        Like `imap()` method but ordering of results is arbitrary.
        """
        if self._state != RUN:
            raise ValueError('Pool not running')
        if chunksize == 1:
            result = IMapUnorderedIterator(self._cache)
            self._taskqueue.put((
             ((result._job, i, func, (x,), {}) for i, x in enumerate(iterable)), result._set_length))
            return result
        else:
            assert chunksize > 1
            task_batches = Pool._get_tasks(func, iterable, chunksize)
            result = IMapUnorderedIterator(self._cache)
            self._taskqueue.put((
             ((result._job, i, mapstar, (x,), {}) for i, x in enumerate(task_batches)), result._set_length))
            return (item for chunk in result for item in chunk)

    def apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
        """
        Asynchronous version of `apply()` method.
        """
        if self._state != RUN:
            raise ValueError('Pool not running')
        result = ApplyResult(self._cache, callback, error_callback)
        self._taskqueue.put(([(result._job, None, func, args, kwds)], None))
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
        if self._state != RUN:
            raise ValueError('Pool not running')
        else:
            if not hasattr(iterable, '__len__'):
                iterable = list(iterable)
            if chunksize is None:
                chunksize, extra = divmod(len(iterable), len(self._pool) * 4)
                if extra:
                    chunksize += 1
            if len(iterable) == 0:
                chunksize = 0
        task_batches = Pool._get_tasks(func, iterable, chunksize)
        result = MapResult((self._cache), chunksize, (len(iterable)), callback, error_callback=error_callback)
        self._taskqueue.put((
         ((result._job, i, mapper, (x,), {}) for i, x in enumerate(task_batches)), None))
        return result

    @staticmethod
    def _handle_workers(pool):
        thread = threading.current_thread()
        while thread._state == RUN or pool._cache and thread._state != TERMINATE:
            pool._maintain_pool()
            time.sleep(0.1)

        pool._taskqueue.put(None)
        util.debug('worker handler exiting')

    @staticmethod
    def _handle_tasks--- This code section failed: ---

 L. 374         0  LOAD_GLOBAL              threading
                2  LOAD_ATTR                current_thread
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  STORE_FAST               'thread'

 L. 376         8  SETUP_LOOP          366  'to 366'
               12  LOAD_GLOBAL              iter
               14  LOAD_FAST                'taskqueue'
               16  LOAD_ATTR                get
               18  LOAD_CONST               None
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  GET_ITER         
               24  FOR_ITER            354  'to 354'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'taskseq'
               32  STORE_FAST               'set_length'

 L. 377        34  LOAD_CONST               None
               36  STORE_FAST               'task'

 L. 378        38  LOAD_CONST               -1
               40  STORE_FAST               'i'

 L. 379        42  SETUP_EXCEPT        228  'to 228'

 L. 380        44  SETUP_LOOP          222  'to 222'
               46  LOAD_GLOBAL              enumerate
               48  LOAD_FAST                'taskseq'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  GET_ITER         
               54  FOR_ITER            192  'to 192'
               56  UNPACK_SEQUENCE_2     2 
               58  STORE_FAST               'i'
               60  STORE_FAST               'task'

 L. 381        62  LOAD_FAST                'thread'
               64  LOAD_ATTR                _state
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 382        68  LOAD_GLOBAL              util
               70  LOAD_ATTR                debug
               72  LOAD_STR                 'task handler found thread._state != RUN'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  POP_TOP          

 L. 383        78  BREAK_LOOP       
             80_0  COME_FROM            66  '66'

 L. 384        80  SETUP_EXCEPT         94  'to 94'

 L. 385        82  LOAD_FAST                'put'
               84  LOAD_FAST                'task'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  POP_TOP          
               90  POP_BLOCK        
               92  JUMP_BACK            54  'to 54'
             94_0  COME_FROM_EXCEPT     80  '80'

 L. 386        94  DUP_TOP          
               96  LOAD_GLOBAL              Exception
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   188  'to 188'
              102  POP_TOP          
              104  STORE_FAST               'e'
              106  POP_TOP          
              108  SETUP_FINALLY       178  'to 178'

 L. 387       110  LOAD_FAST                'task'
              112  LOAD_CONST               None
              114  LOAD_CONST               2
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  UNPACK_SEQUENCE_2     2 
              122  STORE_FAST               'job'
              124  STORE_FAST               'ind'

 L. 388       126  SETUP_EXCEPT        152  'to 152'

 L. 389       128  LOAD_FAST                'cache'
              130  LOAD_FAST                'job'
              132  BINARY_SUBSCR    
              134  LOAD_ATTR                _set
              136  LOAD_FAST                'ind'
              138  LOAD_CONST               False
              140  LOAD_FAST                'e'
              142  BUILD_TUPLE_2         2 
              144  CALL_FUNCTION_2       2  '2 positional arguments'
              146  POP_TOP          
              148  POP_BLOCK        
              150  JUMP_FORWARD        172  'to 172'
            152_0  COME_FROM_EXCEPT    126  '126'

 L. 390       152  DUP_TOP          
              154  LOAD_GLOBAL              KeyError
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   170  'to 170'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 391       166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM           150  '150'
              172  POP_BLOCK        
              174  POP_EXCEPT       
              176  LOAD_CONST               None
            178_0  COME_FROM_FINALLY   108  '108'
              178  LOAD_CONST               None
              180  STORE_FAST               'e'
              182  DELETE_FAST              'e'
              184  END_FINALLY      
              186  JUMP_BACK            54  'to 54'
              188  END_FINALLY      
              190  JUMP_BACK            54  'to 54'
              192  POP_BLOCK        

 L. 393       194  LOAD_FAST                'set_length'
              196  POP_JUMP_IF_FALSE   220  'to 220'

 L. 394       198  LOAD_GLOBAL              util
              200  LOAD_ATTR                debug
              202  LOAD_STR                 'doing set_length()'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  POP_TOP          

 L. 395       208  LOAD_FAST                'set_length'
              210  LOAD_FAST                'i'
              212  LOAD_CONST               1
              214  BINARY_ADD       
              216  CALL_FUNCTION_1       1  '1 positional argument'
              218  POP_TOP          
            220_0  COME_FROM           196  '196'

 L. 396       220  CONTINUE_LOOP        24  'to 24'
            222_0  COME_FROM_LOOP       44  '44'

 L. 397       222  BREAK_LOOP       
              224  POP_BLOCK        
              226  JUMP_BACK            24  'to 24'
            228_0  COME_FROM_EXCEPT     42  '42'

 L. 398       228  DUP_TOP          
              230  LOAD_GLOBAL              Exception
              232  COMPARE_OP               exception-match
              234  POP_JUMP_IF_FALSE   350  'to 350'
              238  POP_TOP          
              240  STORE_FAST               'ex'
              242  POP_TOP          
              244  SETUP_FINALLY       340  'to 340'

 L. 399       246  LOAD_FAST                'task'
              248  POP_JUMP_IF_FALSE   264  'to 264'
              252  LOAD_FAST                'task'
              254  LOAD_CONST               None
              256  LOAD_CONST               2
              258  BUILD_SLICE_2         2 
              260  BINARY_SUBSCR    
              262  JUMP_FORWARD        266  'to 266'
              264  ELSE                     '266'
              264  LOAD_CONST               (0, 0)
            266_0  COME_FROM           262  '262'
              266  UNPACK_SEQUENCE_2     2 
              268  STORE_FAST               'job'
              270  STORE_FAST               'ind'

 L. 400       272  LOAD_FAST                'job'
              274  LOAD_FAST                'cache'
              276  COMPARE_OP               in
              278  POP_JUMP_IF_FALSE   306  'to 306'

 L. 401       282  LOAD_FAST                'cache'
              284  LOAD_FAST                'job'
              286  BINARY_SUBSCR    
              288  LOAD_ATTR                _set
              290  LOAD_FAST                'ind'
              292  LOAD_CONST               1
              294  BINARY_ADD       
              296  LOAD_CONST               False
              298  LOAD_FAST                'ex'
              300  BUILD_TUPLE_2         2 
              302  CALL_FUNCTION_2       2  '2 positional arguments'
              304  POP_TOP          
            306_0  COME_FROM           278  '278'

 L. 402       306  LOAD_FAST                'set_length'
              308  POP_JUMP_IF_FALSE   334  'to 334'

 L. 403       312  LOAD_GLOBAL              util
              314  LOAD_ATTR                debug
              316  LOAD_STR                 'doing set_length()'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  POP_TOP          

 L. 404       322  LOAD_FAST                'set_length'
              324  LOAD_FAST                'i'
              326  LOAD_CONST               1
              328  BINARY_ADD       
              330  CALL_FUNCTION_1       1  '1 positional argument'
              332  POP_TOP          
            334_0  COME_FROM           308  '308'
              334  POP_BLOCK        
              336  POP_EXCEPT       
              338  LOAD_CONST               None
            340_0  COME_FROM_FINALLY   244  '244'
              340  LOAD_CONST               None
              342  STORE_FAST               'ex'
              344  DELETE_FAST              'ex'
              346  END_FINALLY      
              348  JUMP_BACK            24  'to 24'
              350  END_FINALLY      
              352  JUMP_BACK            24  'to 24'
              354  POP_BLOCK        

 L. 406       356  LOAD_GLOBAL              util
              358  LOAD_ATTR                debug
              360  LOAD_STR                 'task handler got sentinel'
              362  CALL_FUNCTION_1       1  '1 positional argument'
              364  POP_TOP          
            366_0  COME_FROM_LOOP        8  '8'

 L. 409       366  SETUP_EXCEPT        426  'to 426'

 L. 411       368  LOAD_GLOBAL              util
              370  LOAD_ATTR                debug
              372  LOAD_STR                 'task handler sending sentinel to result handler'
              374  CALL_FUNCTION_1       1  '1 positional argument'
              376  POP_TOP          

 L. 412       378  LOAD_FAST                'outqueue'
              380  LOAD_ATTR                put
              382  LOAD_CONST               None
              384  CALL_FUNCTION_1       1  '1 positional argument'
              386  POP_TOP          

 L. 415       388  LOAD_GLOBAL              util
              390  LOAD_ATTR                debug
              392  LOAD_STR                 'task handler sending sentinel to workers'
              394  CALL_FUNCTION_1       1  '1 positional argument'
              396  POP_TOP          

 L. 416       398  SETUP_LOOP          422  'to 422'
              400  LOAD_FAST                'pool'
              402  GET_ITER         
              404  FOR_ITER            420  'to 420'
              406  STORE_FAST               'p'

 L. 417       408  LOAD_FAST                'put'
              410  LOAD_CONST               None
              412  CALL_FUNCTION_1       1  '1 positional argument'
              414  POP_TOP          
              416  JUMP_BACK           404  'to 404'
              420  POP_BLOCK        
            422_0  COME_FROM_LOOP      398  '398'
              422  POP_BLOCK        
              424  JUMP_FORWARD        458  'to 458'
            426_0  COME_FROM_EXCEPT    366  '366'

 L. 418       426  DUP_TOP          
              428  LOAD_GLOBAL              OSError
              430  COMPARE_OP               exception-match
              432  POP_JUMP_IF_FALSE   456  'to 456'
              436  POP_TOP          
              438  POP_TOP          
              440  POP_TOP          

 L. 419       442  LOAD_GLOBAL              util
              444  LOAD_ATTR                debug
              446  LOAD_STR                 'task handler got OSError when sending sentinels'
              448  CALL_FUNCTION_1       1  '1 positional argument'
              450  POP_TOP          
              452  POP_EXCEPT       
              454  JUMP_FORWARD        458  'to 458'
              456  END_FINALLY      
            458_0  COME_FROM           454  '454'
            458_1  COME_FROM           424  '424'

 L. 421       458  LOAD_GLOBAL              util
              460  LOAD_ATTR                debug
              462  LOAD_STR                 'task handler exiting'
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  POP_TOP          

Parse error at or near `BREAK_LOOP' instruction at offset 222

    @staticmethod
    def _handle_results(outqueue, get, cache):
        thread = threading.current_thread()
        while True:
            try:
                task = get()
            except (OSError, EOFError):
                util.debug('result handler got EOFError/OSError -- exiting')
                return
            else:
                if thread._state:
                    assert thread._state == TERMINATE
                    util.debug('result handler found thread._state=TERMINATE')
                    break
                if task is None:
                    util.debug('result handler got sentinel')
                    break
                job, i, obj = task
                try:
                    cache[job]._set(i, obj)
                except KeyError:
                    pass

        while cache and thread._state != TERMINATE:
            try:
                task = get()
            except (OSError, EOFError):
                util.debug('result handler got EOFError/OSError -- exiting')
                return

            if task is None:
                util.debug('result handler ignoring extra sentinel')
            else:
                job, i, obj = task
                try:
                    cache[job]._set(i, obj)
                except KeyError:
                    pass

        if hasattr(outqueue, '_reader'):
            util.debug('ensuring that outqueue is not full')
            try:
                for i in range(10):
                    if not outqueue._reader.poll():
                        break
                    get()

            except (OSError, EOFError):
                pass

        util.debug('result handler exiting: len(cache)=%s, thread._state=%s', len(cache), thread._state)

    @staticmethod
    def _get_tasks(func, it, size):
        it = iter(it)
        while True:
            x = tuple(itertools.islice(it, size))
            if not x:
                return
            yield (
             func, x)

    def __reduce__(self):
        raise NotImplementedError('pool objects cannot be passed between processes or pickled')

    def close(self):
        util.debug('closing pool')
        if self._state == RUN:
            self._state = CLOSE
            self._worker_handler._state = CLOSE

    def terminate(self):
        util.debug('terminating pool')
        self._state = TERMINATE
        self._worker_handler._state = TERMINATE
        self._terminate()

    def join(self):
        util.debug('joining pool')
        assert self._state in (CLOSE, TERMINATE)
        self._worker_handler.join()
        self._task_handler.join()
        self._result_handler.join()
        for p in self._pool:
            p.join()

    @staticmethod
    def _help_stuff_finish(inqueue, task_handler, size):
        util.debug('removing tasks from inqueue until task handler finished')
        inqueue._rlock.acquire()
        while task_handler.is_alive() and inqueue._reader.poll():
            inqueue._reader.recv()
            time.sleep(0)

    @classmethod
    def _terminate_pool(cls, taskqueue, inqueue, outqueue, pool, worker_handler, task_handler, result_handler, cache):
        util.debug('finalizing pool')
        worker_handler._state = TERMINATE
        task_handler._state = TERMINATE
        util.debug('helping task handler/workers to finish')
        cls._help_stuff_finish(inqueue, task_handler, len(pool))
        if not result_handler.is_alive():
            if not len(cache) == 0:
                raise AssertionError
        result_handler._state = TERMINATE
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
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()


class ApplyResult(object):

    def __init__(self, cache, callback, error_callback):
        self._event = threading.Event()
        self._job = next(job_counter)
        self._cache = cache
        self._callback = callback
        self._error_callback = error_callback
        cache[self._job] = self

    def ready(self):
        return self._event.is_set()

    def successful(self):
        assert self.ready()
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


AsyncResult = ApplyResult

class MapResult(ApplyResult):

    def __init__(self, cache, chunksize, length, callback, error_callback):
        ApplyResult.__init__(self, cache, callback, error_callback=error_callback)
        self._success = True
        self._value = [None] * length
        self._chunksize = chunksize
        if chunksize <= 0:
            self._number_left = 0
            self._event.set()
            del cache[self._job]
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


class IMapIterator(object):

    def __init__(self, cache):
        self._cond = threading.Condition(threading.Lock())
        self._job = next(job_counter)
        self._cache = cache
        self._items = collections.deque()
        self._index = 0
        self._length = None
        self._unsorted = {}
        cache[self._job] = self

    def __iter__(self):
        return self

    def next(self, timeout=None):
        with self._cond:
            try:
                item = self._items.popleft()
            except IndexError:
                if self._index == self._length:
                    raise StopIteration
                self._cond.wait(timeout)
                try:
                    item = self._items.popleft()
                except IndexError:
                    if self._index == self._length:
                        raise StopIteration
                    raise TimeoutError

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

    def _set_length(self, length):
        with self._cond:
            self._length = length
            if self._index == self._length:
                self._cond.notify()
                del self._cache[self._job]


class IMapUnorderedIterator(IMapIterator):

    def _set(self, i, obj):
        with self._cond:
            self._items.append(obj)
            self._index += 1
            self._cond.notify()
            if self._index == self._length:
                del self._cache[self._job]


class ThreadPool(Pool):
    _wrap_exception = False

    @staticmethod
    def Process(*args, **kwds):
        from .dummy import Process
        return Process(*args, **kwds)

    def __init__(self, processes=None, initializer=None, initargs=()):
        Pool.__init__(self, processes, initializer, initargs)

    def _setup_queues(self):
        self._inqueue = queue.Queue()
        self._outqueue = queue.Queue()
        self._quick_put = self._inqueue.put
        self._quick_get = self._outqueue.get

    @staticmethod
    def _help_stuff_finish(inqueue, task_handler, size):
        with inqueue.not_empty:
            inqueue.queue.clear()
            inqueue.queue.extend([None] * size)
            inqueue.not_empty.notify_all()