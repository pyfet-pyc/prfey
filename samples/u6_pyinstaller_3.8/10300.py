# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: queue.py
"""A multi-producer, multi-consumer queue."""
import threading
from collections import deque
from heapq import heappush, heappop
from time import monotonic as time
try:
    from _queue import SimpleQueue
except ImportError:
    SimpleQueue = None
else:
    __all__ = [
     'Empty', 'Full', 'Queue', 'PriorityQueue', 'LifoQueue', 'SimpleQueue']
    try:
        from _queue import Empty
    except ImportError:

        class Empty(Exception):
            __doc__ = 'Exception raised by Queue.get(block=0)/get_nowait().'


    else:

        class Full(Exception):
            __doc__ = 'Exception raised by Queue.put(block=0)/put_nowait().'


        class Queue:
            __doc__ = 'Create a queue object with a given maximum size.\n\n    If maxsize is <= 0, the queue size is infinite.\n    '

            def __init__(self, maxsize=0):
                self.maxsize = maxsize
                self._init(maxsize)
                self.mutex = threading.Lock()
                self.not_empty = threading.Condition(self.mutex)
                self.not_full = threading.Condition(self.mutex)
                self.all_tasks_done = threading.Condition(self.mutex)
                self.unfinished_tasks = 0

            def task_done(self):
                """Indicate that a formerly enqueued task is complete.

        Used by Queue consumer threads.  For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items
        have been processed (meaning that a task_done() call was received
        for every item that had been put() into the queue).

        Raises a ValueError if called more times than there were items
        placed in the queue.
        """
                with self.all_tasks_done:
                    unfinished = self.unfinished_tasks - 1
                    if unfinished <= 0:
                        if unfinished < 0:
                            raise ValueError('task_done() called too many times')
                        self.all_tasks_done.notify_all()
                    self.unfinished_tasks = unfinished

            def join(self):
                """Blocks until all items in the Queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer thread calls task_done()
        to indicate the item was retrieved and all work on it is complete.

        When the count of unfinished tasks drops to zero, join() unblocks.
        """
                with self.all_tasks_done:
                    while self.unfinished_tasks:
                        self.all_tasks_done.wait()

            def qsize--- This code section failed: ---

 L.  93         0  LOAD_FAST                'self'
                2  LOAD_ATTR                mutex
                4  SETUP_WITH           28  'to 28'
                6  POP_TOP          

 L.  94         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _qsize
               12  CALL_METHOD_0         0  ''
               14  POP_BLOCK        
               16  ROT_TWO          
               18  BEGIN_FINALLY    
               20  WITH_CLEANUP_START
               22  WITH_CLEANUP_FINISH
               24  POP_FINALLY           0  ''
               26  RETURN_VALUE     
             28_0  COME_FROM_WITH        4  '4'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 16

            def empty--- This code section failed: ---

 L. 107         0  LOAD_FAST                'self'
                2  LOAD_ATTR                mutex
                4  SETUP_WITH           30  'to 30'
                6  POP_TOP          

 L. 108         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _qsize
               12  CALL_METHOD_0         0  ''
               14  UNARY_NOT        
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

            def full--- This code section failed: ---

 L. 118         0  LOAD_FAST                'self'
                2  LOAD_ATTR                mutex
                4  SETUP_WITH           50  'to 50'
                6  POP_TOP          

 L. 119         8  LOAD_CONST               0
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                maxsize
               14  DUP_TOP          
               16  ROT_THREE        
               18  COMPARE_OP               <
               20  JUMP_IF_FALSE_OR_POP    32  'to 32'
               22  LOAD_FAST                'self'
               24  LOAD_METHOD              _qsize
               26  CALL_METHOD_0         0  ''
               28  COMPARE_OP               <=
               30  JUMP_FORWARD         36  'to 36'
             32_0  COME_FROM            20  '20'
               32  ROT_TWO          
               34  POP_TOP          
             36_0  COME_FROM            30  '30'
               36  POP_BLOCK        
               38  ROT_TWO          
               40  BEGIN_FINALLY    
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  RETURN_VALUE     
             50_0  COME_FROM_WITH        4  '4'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 38

            def put(self, item, block=True, timeout=None):
                """Put an item into the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until a free slot is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Full exception if no free slot was available within that time.
        Otherwise ('block' is false), put an item on the queue if a free slot
        is immediately available, else raise the Full exception ('timeout'
        is ignored in that case).
        """
                with self.not_full:
                    if self.maxsize > 0 and (block or self._qsize()) >= self.maxsize:
                        raise Full
                    else:
                        if timeout is None:
                            while True:
                                if self._qsize() >= self.maxsize:
                                    self.not_full.wait()

                        else:
                            if timeout < 0:
                                raise ValueError("'timeout' must be a non-negative number")
                            else:
                                endtime = time() + timeout
                                while self._qsize() >= self.maxsize:
                                    remaining = endtime - time()
                                    if remaining <= 0.0:
                                        raise Full
                                    self.not_full.wait(remaining)

                                self._put(item)
                                self.unfinished_tasks += 1
                                self.not_empty.notify()

            def get--- This code section failed: ---

 L. 164         0  LOAD_FAST                'self'
                2  LOAD_ATTR                not_empty
                4  SETUP_WITH          162  'to 162'
                6  POP_TOP          

 L. 165         8  LOAD_FAST                'block'
               10  POP_JUMP_IF_TRUE     26  'to 26'

 L. 166        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _qsize
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_TRUE    128  'to 128'

 L. 167        20  LOAD_GLOBAL              Empty
               22  RAISE_VARARGS_1       1  'exception instance'
               24  JUMP_FORWARD        128  'to 128'
             26_0  COME_FROM            10  '10'

 L. 168        26  LOAD_FAST                'timeout'
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    56  'to 56'

 L. 169        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _qsize
               38  CALL_METHOD_0         0  ''
               40  POP_JUMP_IF_TRUE    128  'to 128'

 L. 170        42  LOAD_FAST                'self'
               44  LOAD_ATTR                not_empty
               46  LOAD_METHOD              wait
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
               52  JUMP_BACK            34  'to 34'
               54  JUMP_FORWARD        128  'to 128'
             56_0  COME_FROM            32  '32'

 L. 171        56  LOAD_FAST                'timeout'
               58  LOAD_CONST               0
               60  COMPARE_OP               <
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L. 172        64  LOAD_GLOBAL              ValueError
               66  LOAD_STR                 "'timeout' must be a non-negative number"
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
               72  JUMP_FORWARD        128  'to 128'
             74_0  COME_FROM            62  '62'

 L. 174        74  LOAD_GLOBAL              time
               76  CALL_FUNCTION_0       0  ''
               78  LOAD_FAST                'timeout'
               80  BINARY_ADD       
               82  STORE_FAST               'endtime'

 L. 175        84  LOAD_FAST                'self'
               86  LOAD_METHOD              _qsize
               88  CALL_METHOD_0         0  ''
               90  POP_JUMP_IF_TRUE    128  'to 128'

 L. 176        92  LOAD_FAST                'endtime'
               94  LOAD_GLOBAL              time
               96  CALL_FUNCTION_0       0  ''
               98  BINARY_SUBTRACT  
              100  STORE_FAST               'remaining'

 L. 177       102  LOAD_FAST                'remaining'
              104  LOAD_CONST               0.0
              106  COMPARE_OP               <=
              108  POP_JUMP_IF_FALSE   114  'to 114'

 L. 178       110  LOAD_GLOBAL              Empty
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           108  '108'

 L. 179       114  LOAD_FAST                'self'
              116  LOAD_ATTR                not_empty
              118  LOAD_METHOD              wait
              120  LOAD_FAST                'remaining'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
              126  JUMP_BACK            84  'to 84'
            128_0  COME_FROM            90  '90'
            128_1  COME_FROM            72  '72'
            128_2  COME_FROM            54  '54'
            128_3  COME_FROM            40  '40'
            128_4  COME_FROM            24  '24'
            128_5  COME_FROM            18  '18'

 L. 180       128  LOAD_FAST                'self'
              130  LOAD_METHOD              _get
              132  CALL_METHOD_0         0  ''
              134  STORE_FAST               'item'

 L. 181       136  LOAD_FAST                'self'
              138  LOAD_ATTR                not_full
              140  LOAD_METHOD              notify
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          

 L. 182       146  LOAD_FAST                'item'
              148  POP_BLOCK        
              150  ROT_TWO          
              152  BEGIN_FINALLY    
              154  WITH_CLEANUP_START
              156  WITH_CLEANUP_FINISH
              158  POP_FINALLY           0  ''
              160  RETURN_VALUE     
            162_0  COME_FROM_WITH        4  '4'
              162  WITH_CLEANUP_START
              164  WITH_CLEANUP_FINISH
              166  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 150

            def put_nowait(self, item):
                """Put an item into the queue without blocking.

        Only enqueue the item if a free slot is immediately available.
        Otherwise raise the Full exception.
        """
                return self.put(item, block=False)

            def get_nowait(self):
                """Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available. Otherwise
        raise the Empty exception.
        """
                return self.get(block=False)

            def _init(self, maxsize):
                self.queue = deque()

            def _qsize(self):
                return len(self.queue)

            def _put(self, item):
                self.queue.append(item)

            def _get(self):
                return self.queue.popleft()


        class PriorityQueue(Queue):
            __doc__ = 'Variant of Queue that retrieves open entries in priority order (lowest first).\n\n    Entries are typically tuples of the form:  (priority number, data).\n    '

            def _init(self, maxsize):
                self.queue = []

            def _qsize(self):
                return len(self.queue)

            def _put(self, item):
                heappush(self.queue, item)

            def _get(self):
                return heappop(self.queue)


        class LifoQueue(Queue):
            __doc__ = 'Variant of Queue that retrieves most recently added entries first.'

            def _init(self, maxsize):
                self.queue = []

            def _qsize(self):
                return len(self.queue)

            def _put(self, item):
                self.queue.append(item)

            def _get(self):
                return self.queue.pop()


        class _PySimpleQueue:
            __doc__ = 'Simple, unbounded FIFO queue.\n\n    This pure Python implementation is not reentrant.\n    '

            def __init__(self):
                self._queue = deque()
                self._count = threading.Semaphore(0)

            def put(self, item, block=True, timeout=None):
                """Put the item on the queue.

        The optional 'block' and 'timeout' arguments are ignored, as this method
        never blocks.  They are provided for compatibility with the Queue class.
        """
                self._queue.append(item)
                self._count.release()

            def get(self, block=True, timeout=None):
                """Remove and return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
                if timeout is not None:
                    if timeout < 0:
                        raise ValueError("'timeout' must be a non-negative number")
                if not self._count.acquire(block, timeout):
                    raise Empty
                return self._queue.popleft()

            def put_nowait(self, item):
                """Put an item into the queue without blocking.

        This is exactly equivalent to `put(item)` and is only provided
        for compatibility with the Queue class.
        """
                return self.put(item, block=False)

            def get_nowait(self):
                """Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available. Otherwise
        raise the Empty exception.
        """
                return self.get(block=False)

            def empty(self):
                """Return True if the queue is empty, False otherwise (not reliable!)."""
                return len(self._queue) == 0

            def qsize(self):
                """Return the approximate size of the queue (not reliable!)."""
                return len(self._queue)


        if SimpleQueue is None:
            SimpleQueue = _PySimpleQueue