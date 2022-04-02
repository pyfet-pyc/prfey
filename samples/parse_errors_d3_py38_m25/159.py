# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\queues.py
__all__ = [
 'Queue', 'SimpleQueue', 'JoinableQueue']
import sys, os, threading, collections, time, weakref, errno
from queue import Empty, Full
import _multiprocessing
from . import connection
from . import context
_ForkingPickler = context.reduction.ForkingPickler
from .util import debug, info, Finalize, register_after_fork, is_exiting

class Queue(object):

    def __init__(self, maxsize=0, *, ctx):
        if maxsize <= 0:
            from .synchronize import SEM_VALUE_MAX as maxsize
        self._maxsize = maxsize
        self._reader, self._writer = connection.Pipe(duplex=False)
        self._rlock = ctx.Lock()
        self._opid = os.getpid()
        if sys.platform == 'win32':
            self._wlock = None
        else:
            self._wlock = ctx.Lock()
        self._sem = ctx.BoundedSemaphore(maxsize)
        self._ignore_epipe = False
        self._after_fork()
        if sys.platform != 'win32':
            register_after_fork(self, Queue._after_fork)

    def __getstate__(self):
        context.assert_spawning(self)
        return (
         self._ignore_epipe, self._maxsize, self._reader, self._writer,
         self._rlock, self._wlock, self._sem, self._opid)

    def __setstate__(self, state):
        self._ignore_epipe, self._maxsize, self._reader, self._writer, self._rlock, self._wlock, self._sem, self._opid = state
        self._after_fork()

    def _after_fork(self):
        debug('Queue._after_fork()')
        self._notempty = threading.Condition(threading.Lock())
        self._buffer = collections.deque()
        self._thread = None
        self._jointhread = None
        self._joincancelled = False
        self._closed = False
        self._close = None
        self._send_bytes = self._writer.send_bytes
        self._recv_bytes = self._reader.recv_bytes
        self._poll = self._reader.poll

    def put(self, obj, block=True, timeout=None):
        if self._closed:
            raise ValueError(f"Queue {self!r} is closed")
        if not self._sem.acquire(block, timeout):
            raise Full
        with self._notempty:
            if self._thread is None:
                self._start_thread()
            self._buffer.append(obj)
            self._notempty.notify()

    def get(self, block=True, timeout=None):
        if self._closed:
            raise ValueError(f"Queue {self!r} is closed")
        if block and timeout is None:
            with self._rlock:
                res = self._recv_bytes()
            self._sem.release()
        else:
            if block:
                deadline = time.monotonic() + timeout
            if not self._rlock.acquire(block, timeout):
                raise Empty
            try:
                if block:
                    timeout = deadline - time.monotonic()
                    assert self._poll(timeout)
                elif not self._poll():
                    raise Empty
                res = self._recv_bytes()
                self._sem.release()
            finally:
                self._rlock.release()

        return _ForkingPickler.loads(res)

    def qsize(self):
        return self._maxsize - self._sem._semlock._get_value()

    def empty(self):
        return not self._poll()

    def full(self):
        return self._sem._semlock._is_zero()

    def get_nowait(self):
        return self.get(False)

    def put_nowait(self, obj):
        return self.put(obj, False)

    def close(self):
        self._closed = True
        try:
            self._reader.close()
        finally:
            close = self._close
            if close:
                self._close = None
                close()

    def join_thread(self):
        debug('Queue.join_thread()')
        assert self._closed, 'Queue {0!r} not closed'.format(self)
        if self._jointhread:
            self._jointhread()

    def cancel_join_thread(self):
        debug('Queue.cancel_join_thread()')
        self._joincancelled = True
        try:
            self._jointhread.cancel()
        except AttributeError:
            pass

    def _start_thread(self):
        debug('Queue._start_thread()')
        self._buffer.clear()
        self._thread = threading.Thread(target=(Queue._feed),
          args=(
         self._buffer, self._notempty, self._send_bytes,
         self._wlock, self._writer.close, self._ignore_epipe,
         self._on_queue_feeder_error, self._sem),
          name='QueueFeederThread')
        self._thread.daemon = True
        debug('doing self._thread.start()')
        self._thread.start()
        debug('... done self._thread.start()')
        if not self._joincancelled:
            self._jointhread = Finalize((self._thread),
              (Queue._finalize_join), [
             weakref.ref(self._thread)],
              exitpriority=(-5))
        self._close = Finalize(self,
          (Queue._finalize_close), [
         self._buffer, self._notempty],
          exitpriority=10)

    @staticmethod
    def _finalize_join(twr):
        debug('joining queue thread')
        thread = twr()
        if thread is not None:
            thread.join()
            debug('... queue thread joined')
        else:
            debug('... queue thread already dead')

    @staticmethod
    def _finalize_close(buffer, notempty):
        debug('telling queue thread to quit')
        with notempty:
            buffer.append(_sentinel)
            notempty.notify()

    @staticmethod
    def _feed--- This code section failed: ---

 L. 210         0  LOAD_GLOBAL              debug
                2  LOAD_STR                 'starting thread to feed data to pipe'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L. 211         8  LOAD_FAST                'notempty'
               10  LOAD_ATTR                acquire
               12  STORE_FAST               'nacquire'

 L. 212        14  LOAD_FAST                'notempty'
               16  LOAD_ATTR                release
               18  STORE_FAST               'nrelease'

 L. 213        20  LOAD_FAST                'notempty'
               22  LOAD_ATTR                wait
               24  STORE_FAST               'nwait'

 L. 214        26  LOAD_FAST                'buffer'
               28  LOAD_ATTR                popleft
               30  STORE_FAST               'bpopleft'

 L. 215        32  LOAD_GLOBAL              _sentinel
               34  STORE_FAST               'sentinel'

 L. 216        36  LOAD_GLOBAL              sys
               38  LOAD_ATTR                platform
               40  LOAD_STR                 'win32'
               42  COMPARE_OP               !=
               44  POP_JUMP_IF_FALSE    60  'to 60'

 L. 217        46  LOAD_FAST                'writelock'
               48  LOAD_ATTR                acquire
               50  STORE_FAST               'wacquire'

 L. 218        52  LOAD_FAST                'writelock'
               54  LOAD_ATTR                release
               56  STORE_FAST               'wrelease'
               58  JUMP_FORWARD         64  'to 64'
             60_0  COME_FROM            44  '44'

 L. 220        60  LOAD_CONST               None
               62  STORE_FAST               'wacquire'
             64_0  COME_FROM           338  '338'
             64_1  COME_FROM           334  '334'
             64_2  COME_FROM           218  '218'
             64_3  COME_FROM            58  '58'

 L. 223        64  SETUP_FINALLY       220  'to 220'

 L. 224        66  LOAD_FAST                'nacquire'
               68  CALL_FUNCTION_0       0  ''
               70  POP_TOP          

 L. 225        72  SETUP_FINALLY        88  'to 88'

 L. 226        74  LOAD_FAST                'buffer'
               76  POP_JUMP_IF_TRUE     84  'to 84'

 L. 227        78  LOAD_FAST                'nwait'
               80  CALL_FUNCTION_0       0  ''
               82  POP_TOP          
             84_0  COME_FROM            76  '76'
               84  POP_BLOCK        
               86  BEGIN_FINALLY    
             88_0  COME_FROM_FINALLY    72  '72'

 L. 229        88  LOAD_FAST                'nrelease'
               90  CALL_FUNCTION_0       0  ''
               92  POP_TOP          
               94  END_FINALLY      

 L. 230        96  SETUP_FINALLY       196  'to 196'
             98_0  COME_FROM           190  '190'
             98_1  COME_FROM           160  '160'

 L. 232        98  LOAD_FAST                'bpopleft'
              100  CALL_FUNCTION_0       0  ''
              102  STORE_FAST               'obj'

 L. 233       104  LOAD_FAST                'obj'
              106  LOAD_FAST                'sentinel'
              108  COMPARE_OP               is
              110  POP_JUMP_IF_FALSE   134  'to 134'

 L. 234       112  LOAD_GLOBAL              debug
              114  LOAD_STR                 'feeder thread got sentinel -- exiting'
              116  CALL_FUNCTION_1       1  ''
              118  POP_TOP          

 L. 235       120  LOAD_FAST                'close'
              122  CALL_FUNCTION_0       0  ''
              124  POP_TOP          

 L. 236       126  POP_BLOCK        
              128  POP_BLOCK        
              130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           110  '110'

 L. 239       134  LOAD_GLOBAL              _ForkingPickler
              136  LOAD_METHOD              dumps
              138  LOAD_FAST                'obj'
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'obj'

 L. 240       144  LOAD_FAST                'wacquire'
              146  LOAD_CONST               None
              148  COMPARE_OP               is
              150  POP_JUMP_IF_FALSE   162  'to 162'

 L. 241       152  LOAD_FAST                'send_bytes'
              154  LOAD_FAST                'obj'
              156  CALL_FUNCTION_1       1  ''
              158  POP_TOP          
              160  JUMP_BACK            98  'to 98'
            162_0  COME_FROM           150  '150'

 L. 243       162  LOAD_FAST                'wacquire'
              164  CALL_FUNCTION_0       0  ''
              166  POP_TOP          

 L. 244       168  SETUP_FINALLY       182  'to 182'

 L. 245       170  LOAD_FAST                'send_bytes'
              172  LOAD_FAST                'obj'
              174  CALL_FUNCTION_1       1  ''
              176  POP_TOP          
              178  POP_BLOCK        
              180  BEGIN_FINALLY    
            182_0  COME_FROM_FINALLY   168  '168'

 L. 247       182  LOAD_FAST                'wrelease'
              184  CALL_FUNCTION_0       0  ''
              186  POP_TOP          
              188  END_FINALLY      
              190  JUMP_BACK            98  'to 98'
              192  POP_BLOCK        
              194  JUMP_FORWARD        216  'to 216'
            196_0  COME_FROM_FINALLY    96  '96'

 L. 248       196  DUP_TOP          
              198  LOAD_GLOBAL              IndexError
              200  COMPARE_OP               exception-match
              202  POP_JUMP_IF_FALSE   214  'to 214'
              204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L. 249       210  POP_EXCEPT       
              212  BREAK_LOOP          216  'to 216'
            214_0  COME_FROM           202  '202'
              214  END_FINALLY      
            216_0  COME_FROM           212  '212'
            216_1  COME_FROM           194  '194'
              216  POP_BLOCK        
              218  JUMP_BACK            64  'to 64'
            220_0  COME_FROM_FINALLY    64  '64'

 L. 250       220  DUP_TOP          
              222  LOAD_GLOBAL              Exception
              224  COMPARE_OP               exception-match
          226_228  POP_JUMP_IF_FALSE   336  'to 336'
              230  POP_TOP          
              232  STORE_FAST               'e'
              234  POP_TOP          
              236  SETUP_FINALLY       324  'to 324'

 L. 251       238  LOAD_FAST                'ignore_epipe'
          240_242  POP_JUMP_IF_FALSE   274  'to 274'
              244  LOAD_GLOBAL              getattr
              246  LOAD_FAST                'e'
              248  LOAD_STR                 'errno'
              250  LOAD_CONST               0
              252  CALL_FUNCTION_3       3  ''
              254  LOAD_GLOBAL              errno
              256  LOAD_ATTR                EPIPE
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   274  'to 274'

 L. 252       264  POP_BLOCK        
              266  POP_EXCEPT       
              268  CALL_FINALLY        324  'to 324'
              270  LOAD_CONST               None
              272  RETURN_VALUE     
            274_0  COME_FROM           260  '260'
            274_1  COME_FROM           240  '240'

 L. 257       274  LOAD_GLOBAL              is_exiting
              276  CALL_FUNCTION_0       0  ''
          278_280  POP_JUMP_IF_FALSE   302  'to 302'

 L. 258       282  LOAD_GLOBAL              info
              284  LOAD_STR                 'error in queue thread: %s'
              286  LOAD_FAST                'e'
              288  CALL_FUNCTION_2       2  ''
              290  POP_TOP          

 L. 259       292  POP_BLOCK        
              294  POP_EXCEPT       
              296  CALL_FINALLY        324  'to 324'
              298  LOAD_CONST               None
              300  RETURN_VALUE     
            302_0  COME_FROM           278  '278'

 L. 266       302  LOAD_FAST                'queue_sem'
              304  LOAD_METHOD              release
              306  CALL_METHOD_0         0  ''
              308  POP_TOP          

 L. 267       310  LOAD_FAST                'onerror'
              312  LOAD_FAST                'e'
              314  LOAD_FAST                'obj'
              316  CALL_FUNCTION_2       2  ''
              318  POP_TOP          
              320  POP_BLOCK        
              322  BEGIN_FINALLY    
            324_0  COME_FROM           296  '296'
            324_1  COME_FROM           268  '268'
            324_2  COME_FROM_FINALLY   236  '236'
              324  LOAD_CONST               None
              326  STORE_FAST               'e'
              328  DELETE_FAST              'e'
              330  END_FINALLY      
              332  POP_EXCEPT       
              334  JUMP_BACK            64  'to 64'
            336_0  COME_FROM           226  '226'
              336  END_FINALLY      
              338  JUMP_BACK            64  'to 64'

Parse error at or near `POP_BLOCK' instruction at offset 128

    @staticmethod
    def _on_queue_feeder_error(e, obj):
        """
        Private API hook called when feeding data in the background thread
        raises an exception.  For overriding by concurrent.futures.
        """
        import traceback
        traceback.print_exc()


_sentinel = object()

class JoinableQueue(Queue):

    def __init__(self, maxsize=0, *, ctx):
        Queue.__init__(self, maxsize, ctx=ctx)
        self._unfinished_tasks = ctx.Semaphore(0)
        self._cond = ctx.Condition()

    def __getstate__(self):
        return Queue.__getstate__(self) + (self._cond, self._unfinished_tasks)

    def __setstate__(self, state):
        Queue.__setstate__(self, state[:-2])
        self._cond, self._unfinished_tasks = state[-2:]

    def put(self, obj, block=True, timeout=None):
        if self._closed:
            raise ValueError(f"Queue {self!r} is closed")
        if not self._sem.acquire(block, timeout):
            raise Full
        with self._notempty:
            with self._cond:
                if self._thread is None:
                    self._start_thread()
                self._buffer.append(obj)
                self._unfinished_tasks.release()
                self._notempty.notify()

    def task_done(self):
        with self._cond:
            if not self._unfinished_tasks.acquire(False):
                raise ValueError('task_done() called too many times')
            if self._unfinished_tasks._semlock._is_zero():
                self._cond.notify_all()

    def join(self):
        with self._cond:
            if not self._unfinished_tasks._semlock._is_zero():
                self._cond.wait()


class SimpleQueue(object):

    def __init__(self, *, ctx):
        self._reader, self._writer = connection.Pipe(duplex=False)
        self._rlock = ctx.Lock()
        self._poll = self._reader.poll
        if sys.platform == 'win32':
            self._wlock = None
        else:
            self._wlock = ctx.Lock()

    def empty(self):
        return not self._poll()

    def __getstate__(self):
        context.assert_spawning(self)
        return (
         self._reader, self._writer, self._rlock, self._wlock)

    def __setstate__(self, state):
        self._reader, self._writer, self._rlock, self._wlock = state
        self._poll = self._reader.poll

    def get(self):
        with self._rlock:
            res = self._reader.recv_bytes()
        return _ForkingPickler.loads(res)

    def put(self, obj):
        obj = _ForkingPickler.dumps(obj)
        if self._wlock is None:
            self._writer.send_bytes(obj)
        else:
            with self._wlock:
                self._writer.send_bytes(obj)