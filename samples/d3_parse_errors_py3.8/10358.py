# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\queues.py
__all__ = ('Queue', 'PriorityQueue', 'LifoQueue', 'QueueFull', 'QueueEmpty')
import collections, heapq, warnings
from . import events
from . import locks

class QueueEmpty(Exception):
    __doc__ = 'Raised when Queue.get_nowait() is called on an empty Queue.'


class QueueFull(Exception):
    __doc__ = 'Raised when the Queue.put_nowait() method is called on a full Queue.'


class Queue:
    __doc__ = 'A queue, useful for coordinating producer and consumer coroutines.\n\n    If maxsize is less than or equal to zero, the queue size is infinite. If it\n    is an integer greater than 0, then "await put()" will block when the\n    queue reaches maxsize, until an item is removed by get().\n\n    Unlike the standard library Queue, you can reliably know this Queue\'s size\n    with qsize(), since your single-threaded asyncio application won\'t be\n    interrupted between calling qsize() and doing an operation on the Queue.\n    '

    def __init__(self, maxsize=0, *, loop=None):
        if loop is None:
            self._loop = events.get_event_loop()
        else:
            self._loop = loop
            warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
              stacklevel=2)
        self._maxsize = maxsize
        self._getters = collections.deque()
        self._putters = collections.deque()
        self._unfinished_tasks = 0
        self._finished = locks.Event(loop=loop)
        self._finished.set()
        self._init(maxsize)

    def _init(self, maxsize):
        self._queue = collections.deque()

    def _get(self):
        return self._queue.popleft()

    def _put(self, item):
        self._queue.append(item)

    def _wakeup_next--- This code section failed: ---
              0_0  COME_FROM            32  '32'
              0_1  COME_FROM            18  '18'

 L.  67         0  LOAD_FAST                'waiters'
                2  POP_JUMP_IF_FALSE    34  'to 34'

 L.  68         4  LOAD_FAST                'waiters'
                6  LOAD_METHOD              popleft
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'waiter'

 L.  69        12  LOAD_FAST                'waiter'
               14  LOAD_METHOD              done
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_TRUE_BACK     0  'to 0'

 L.  70        20  LOAD_FAST                'waiter'
               22  LOAD_METHOD              set_result
               24  LOAD_CONST               None
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L.  71        30  JUMP_FORWARD         34  'to 34'
               32  JUMP_BACK             0  'to 0'
             34_0  COME_FROM            30  '30'
             34_1  COME_FROM             2  '2'

Parse error at or near `JUMP_BACK' instruction at offset 32

    def __repr__(self):
        return f"<{type(self).__name__} at {id(self):#x} {self._format()}>"

    def __str__(self):
        return f"<{type(self).__name__} {self._format()}>"

    def _format(self):
        result = f"maxsize={self._maxsize!r}"
        if getattr(self, '_queue', None):
            result += f" _queue={list(self._queue)!r}"
        if self._getters:
            result += f" _getters[{len(self._getters)}]"
        if self._putters:
            result += f" _putters[{len(self._putters)}]"
        if self._unfinished_tasks:
            result += f" tasks={self._unfinished_tasks}"
        return result

    def qsize(self):
        """Number of items in the queue."""
        return len(self._queue)

    @property
    def maxsize(self):
        """Number of items allowed in the queue."""
        return self._maxsize

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return not self._queue

    def full(self):
        """Return True if there are maxsize items in the queue.

        Note: if the Queue was initialized with maxsize=0 (the default),
        then full() is never True.
        """
        if self._maxsize <= 0:
            return False
        return self.qsize() >= self._maxsize

    async def put--- This code section failed: ---
              0_0  COME_FROM           134  '134'
              0_1  COME_FROM           130  '130'
              0_2  COME_FROM            44  '44'

 L. 121         0  LOAD_FAST                'self'
                2  LOAD_METHOD              full
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE   136  'to 136'

 L. 122         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _loop
               12  LOAD_METHOD              create_future
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'putter'

 L. 123        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _putters
               22  LOAD_METHOD              append
               24  LOAD_FAST                'putter'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 124        30  SETUP_FINALLY        46  'to 46'

 L. 125        32  LOAD_FAST                'putter'
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_BACK             0  'to 0'
             46_0  COME_FROM_FINALLY    30  '30'

 L. 126        46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 127        52  LOAD_FAST                'putter'
               54  LOAD_METHOD              cancel
               56  CALL_METHOD_0         0  ''
               58  POP_TOP          

 L. 128        60  SETUP_FINALLY        78  'to 78'

 L. 130        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _putters
               66  LOAD_METHOD              remove
               68  LOAD_FAST                'putter'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  JUMP_FORWARD         98  'to 98'
             78_0  COME_FROM_FINALLY    60  '60'

 L. 131        78  DUP_TOP          
               80  LOAD_GLOBAL              ValueError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE    96  'to 96'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 134        92  POP_EXCEPT       
               94  BREAK_LOOP           98  'to 98'
             96_0  COME_FROM            84  '84'
               96  END_FINALLY      
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            76  '76'

 L. 135        98  LOAD_FAST                'self'
              100  LOAD_METHOD              full
              102  CALL_METHOD_0         0  ''
              104  POP_JUMP_IF_TRUE    126  'to 126'
              106  LOAD_FAST                'putter'
              108  LOAD_METHOD              cancelled
              110  CALL_METHOD_0         0  ''
              112  POP_JUMP_IF_TRUE    126  'to 126'

 L. 138       114  LOAD_FAST                'self'
              116  LOAD_METHOD              _wakeup_next
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _putters
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
            126_0  COME_FROM           112  '112'
            126_1  COME_FROM           104  '104'

 L. 139       126  RAISE_VARARGS_0       0  'reraise'
              128  POP_EXCEPT       
              130  JUMP_BACK             0  'to 0'
              132  END_FINALLY      
              134  JUMP_BACK             0  'to 0'
            136_0  COME_FROM             6  '6'

 L. 140       136  LOAD_FAST                'self'
              138  LOAD_METHOD              put_nowait
              140  LOAD_FAST                'item'
              142  CALL_METHOD_1         1  ''
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 96

    def put_nowait(self, item):
        """Put an item into the queue without blocking.

        If no free slot is immediately available, raise QueueFull.
        """
        if self.full():
            raise QueueFull
        self._put(item)
        self._unfinished_tasks += 1
        self._finished.clear()
        self._wakeup_next(self._getters)

    async def get--- This code section failed: ---
              0_0  COME_FROM           134  '134'
              0_1  COME_FROM           130  '130'
              0_2  COME_FROM            44  '44'

 L. 159         0  LOAD_FAST                'self'
                2  LOAD_METHOD              empty
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE   136  'to 136'

 L. 160         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _loop
               12  LOAD_METHOD              create_future
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'getter'

 L. 161        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _getters
               22  LOAD_METHOD              append
               24  LOAD_FAST                'getter'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 162        30  SETUP_FINALLY        46  'to 46'

 L. 163        32  LOAD_FAST                'getter'
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_BACK             0  'to 0'
             46_0  COME_FROM_FINALLY    30  '30'

 L. 164        46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 165        52  LOAD_FAST                'getter'
               54  LOAD_METHOD              cancel
               56  CALL_METHOD_0         0  ''
               58  POP_TOP          

 L. 166        60  SETUP_FINALLY        78  'to 78'

 L. 168        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _getters
               66  LOAD_METHOD              remove
               68  LOAD_FAST                'getter'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  JUMP_FORWARD         98  'to 98'
             78_0  COME_FROM_FINALLY    60  '60'

 L. 169        78  DUP_TOP          
               80  LOAD_GLOBAL              ValueError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE    96  'to 96'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 172        92  POP_EXCEPT       
               94  BREAK_LOOP           98  'to 98'
             96_0  COME_FROM            84  '84'
               96  END_FINALLY      
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            76  '76'

 L. 173        98  LOAD_FAST                'self'
              100  LOAD_METHOD              empty
              102  CALL_METHOD_0         0  ''
              104  POP_JUMP_IF_TRUE    126  'to 126'
              106  LOAD_FAST                'getter'
              108  LOAD_METHOD              cancelled
              110  CALL_METHOD_0         0  ''
              112  POP_JUMP_IF_TRUE    126  'to 126'

 L. 176       114  LOAD_FAST                'self'
              116  LOAD_METHOD              _wakeup_next
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _getters
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
            126_0  COME_FROM           112  '112'
            126_1  COME_FROM           104  '104'

 L. 177       126  RAISE_VARARGS_0       0  'reraise'
              128  POP_EXCEPT       
              130  JUMP_BACK             0  'to 0'
              132  END_FINALLY      
              134  JUMP_BACK             0  'to 0'
            136_0  COME_FROM             6  '6'

 L. 178       136  LOAD_FAST                'self'
              138  LOAD_METHOD              get_nowait
              140  CALL_METHOD_0         0  ''
              142  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 96

    def get_nowait(self):
        """Remove and return an item from the queue.

        Return an item if one is immediately available, else raise QueueEmpty.
        """
        if self.empty():
            raise QueueEmpty
        item = self._get()
        self._wakeup_next(self._putters)
        return item

    def task_done(self):
        """Indicate that a formerly enqueued task is complete.

        Used by queue consumers. For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items have
        been processed (meaning that a task_done() call was received for every
        item that had been put() into the queue).

        Raises ValueError if called more times than there were items placed in
        the queue.
        """
        if self._unfinished_tasks <= 0:
            raise ValueError('task_done() called too many times')
        self._unfinished_tasks -= 1
        if self._unfinished_tasks == 0:
            self._finished.set()

    async def join(self):
        """Block until all items in the queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer calls task_done() to
        indicate that the item was retrieved and all work on it is complete.
        When the count of unfinished tasks drops to zero, join() unblocks.
        """
        if self._unfinished_tasks > 0:
            await self._finished.wait()


class PriorityQueue(Queue):
    __doc__ = 'A subclass of Queue; retrieves entries in priority order (lowest first).\n\n    Entries are typically tuples of the form: (priority number, data).\n    '

    def _init(self, maxsize):
        self._queue = []

    def _put(self, item, heappush=heapq.heappush):
        heappush(self._queue, item)

    def _get(self, heappop=heapq.heappop):
        return heappop(self._queue)


class LifoQueue(Queue):
    __doc__ = 'A subclass of Queue that retrieves most recently added entries first.'

    def _init(self, maxsize):
        self._queue = []

    def _put(self, item):
        self._queue.append(item)

    def _get(self):
        return self._queue.pop()