# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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

    def __init__--- This code section failed: ---

 L.  34         0  LOAD_FAST                'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  35         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _loop
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM             6  '6'

 L.  37        20  LOAD_FAST                'loop'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _loop

 L.  38        26  LOAD_GLOBAL              warnings
               28  LOAD_ATTR                warn
               30  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L.  40        32  LOAD_GLOBAL              DeprecationWarning
               34  LOAD_CONST               2

 L.  38        36  LOAD_CONST               ('stacklevel',)
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  POP_TOP          
             42_0  COME_FROM            18  '18'

 L.  41        42  LOAD_FAST                'maxsize'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _maxsize

 L.  44        48  LOAD_GLOBAL              collections
               50  LOAD_METHOD              deque
               52  CALL_METHOD_0         0  ''
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _getters

 L.  46        58  LOAD_GLOBAL              collections
               60  LOAD_METHOD              deque
               62  CALL_METHOD_0         0  ''
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _putters

 L.  47        68  LOAD_CONST               0
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _unfinished_tasks

 L.  48        74  LOAD_GLOBAL              locks
               76  LOAD_ATTR                Event
               78  LOAD_FAST                'loop'
               80  LOAD_CONST               ('loop',)
               82  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _finished

 L.  49        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _finished
               92  LOAD_METHOD              set
               94  CALL_METHOD_0         0  ''
               96  POP_TOP          

 L.  50        98  LOAD_FAST                'self'
              100  LOAD_METHOD              _init
              102  LOAD_FAST                'maxsize'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _init(self, maxsize):
        self._queue = collections.deque

    def _get(self):
        return self._queue.popleft

    def _put(self, item):
        self._queue.appenditem

    def _wakeup_next(self, waiters):
        while waiters:
            waiter = waiters.popleft
            if not waiter.done:
                waiter.set_resultNone
                break

    def __repr__(self):
        return f"<{type(self).__name__} at {id(self):#x} {self._format}>"

    def __str__(self):
        return f"<{type(self).__name__} {self._format}>"

    def __class_getitem__(cls, type):
        return cls

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
        return self.qsize >= self._maxsize

    async def put--- This code section failed: ---

 L. 124         0  LOAD_FAST                'self'
                2  LOAD_METHOD              full
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE   134  'to 134'

 L. 125         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _loop
               12  LOAD_METHOD              create_future
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'putter'

 L. 126        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _putters
               22  LOAD_METHOD              append
               24  LOAD_FAST                'putter'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 127        30  SETUP_FINALLY        46  'to 46'

 L. 128        32  LOAD_FAST                'putter'
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_BACK             0  'to 0'
             46_0  COME_FROM_FINALLY    30  '30'

 L. 129        46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 130        52  LOAD_FAST                'putter'
               54  LOAD_METHOD              cancel
               56  CALL_METHOD_0         0  ''
               58  POP_TOP          

 L. 131        60  SETUP_FINALLY        78  'to 78'

 L. 133        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _putters
               66  LOAD_METHOD              remove
               68  LOAD_FAST                'putter'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  JUMP_FORWARD         96  'to 96'
             78_0  COME_FROM_FINALLY    60  '60'

 L. 134        78  DUP_TOP          
               80  LOAD_GLOBAL              ValueError
               82  <121>                94  ''
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 137        90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
               94  <48>             
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            76  '76'

 L. 138        96  LOAD_FAST                'self'
               98  LOAD_METHOD              full
              100  CALL_METHOD_0         0  ''
              102  POP_JUMP_IF_TRUE    124  'to 124'
              104  LOAD_FAST                'putter'
              106  LOAD_METHOD              cancelled
              108  CALL_METHOD_0         0  ''
              110  POP_JUMP_IF_TRUE    124  'to 124'

 L. 141       112  LOAD_FAST                'self'
              114  LOAD_METHOD              _wakeup_next
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _putters
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
            124_0  COME_FROM           110  '110'
            124_1  COME_FROM           102  '102'

 L. 142       124  RAISE_VARARGS_0       0  'reraise'
              126  POP_EXCEPT       
              128  JUMP_BACK             0  'to 0'
              130  <48>             
              132  JUMP_BACK             0  'to 0'
            134_0  COME_FROM             6  '6'

 L. 143       134  LOAD_FAST                'self'
              136  LOAD_METHOD              put_nowait
              138  LOAD_FAST                'item'
              140  CALL_METHOD_1         1  ''
              142  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 82

    def put_nowait(self, item):
        """Put an item into the queue without blocking.

        If no free slot is immediately available, raise QueueFull.
        """
        if self.full:
            raise QueueFull
        self._putitem
        self._unfinished_tasks += 1
        self._finished.clear
        self._wakeup_nextself._getters

    async def get--- This code section failed: ---

 L. 162         0  LOAD_FAST                'self'
                2  LOAD_METHOD              empty
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE   134  'to 134'

 L. 163         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _loop
               12  LOAD_METHOD              create_future
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'getter'

 L. 164        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _getters
               22  LOAD_METHOD              append
               24  LOAD_FAST                'getter'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 165        30  SETUP_FINALLY        46  'to 46'

 L. 166        32  LOAD_FAST                'getter'
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_BACK             0  'to 0'
             46_0  COME_FROM_FINALLY    30  '30'

 L. 167        46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 168        52  LOAD_FAST                'getter'
               54  LOAD_METHOD              cancel
               56  CALL_METHOD_0         0  ''
               58  POP_TOP          

 L. 169        60  SETUP_FINALLY        78  'to 78'

 L. 171        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _getters
               66  LOAD_METHOD              remove
               68  LOAD_FAST                'getter'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  JUMP_FORWARD         96  'to 96'
             78_0  COME_FROM_FINALLY    60  '60'

 L. 172        78  DUP_TOP          
               80  LOAD_GLOBAL              ValueError
               82  <121>                94  ''
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 175        90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
               94  <48>             
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            76  '76'

 L. 176        96  LOAD_FAST                'self'
               98  LOAD_METHOD              empty
              100  CALL_METHOD_0         0  ''
              102  POP_JUMP_IF_TRUE    124  'to 124'
              104  LOAD_FAST                'getter'
              106  LOAD_METHOD              cancelled
              108  CALL_METHOD_0         0  ''
              110  POP_JUMP_IF_TRUE    124  'to 124'

 L. 179       112  LOAD_FAST                'self'
              114  LOAD_METHOD              _wakeup_next
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _getters
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
            124_0  COME_FROM           110  '110'
            124_1  COME_FROM           102  '102'

 L. 180       124  RAISE_VARARGS_0       0  'reraise'
              126  POP_EXCEPT       
              128  JUMP_BACK             0  'to 0'
              130  <48>             
              132  JUMP_BACK             0  'to 0'
            134_0  COME_FROM             6  '6'

 L. 181       134  LOAD_FAST                'self'
              136  LOAD_METHOD              get_nowait
              138  CALL_METHOD_0         0  ''
              140  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 82

    def get_nowait(self):
        """Remove and return an item from the queue.

        Return an item if one is immediately available, else raise QueueEmpty.
        """
        if self.empty:
            raise QueueEmpty
        item = self._get
        self._wakeup_nextself._putters
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
            self._finished.set

    async def join(self):
        """Block until all items in the queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer calls task_done() to
        indicate that the item was retrieved and all work on it is complete.
        When the count of unfinished tasks drops to zero, join() unblocks.
        """
        if self._unfinished_tasks > 0:
            await self._finished.wait


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
        self._queue.appenditem

    def _get(self):
        return self._queue.pop