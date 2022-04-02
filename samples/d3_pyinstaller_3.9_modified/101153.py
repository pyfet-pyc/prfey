# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: concurrent\futures\process.py
"""Implements ProcessPoolExecutor.

The following diagram and text describe the data-flow through the system:

|======================= In-process =====================|== Out-of-process ==|

+----------+     +----------+       +--------+     +-----------+    +---------+
|          |  => | Work Ids |       |        |     | Call Q    |    | Process |
|          |     +----------+       |        |     +-----------+    |  Pool   |
|          |     | ...      |       |        |     | ...       |    +---------+
|          |     | 6        |    => |        |  => | 5, call() | => |         |
|          |     | 7        |       |        |     | ...       |    |         |
| Process  |     | ...      |       | Local  |     +-----------+    | Process |
|  Pool    |     +----------+       | Worker |                      |  #1..n  |
| Executor |                        | Thread |                      |         |
|          |     +----------- +     |        |     +-----------+    |         |
|          | <=> | Work Items | <=> |        | <=  | Result Q  | <= |         |
|          |     +------------+     |        |     +-----------+    |         |
|          |     | 6: call()  |     |        |     | ...       |    |         |
|          |     |    future  |     |        |     | 4, result |    |         |
|          |     | ...        |     |        |     | 3, except |    |         |
+----------+     +------------+     +--------+     +-----------+    +---------+

Executor.submit() called:
- creates a uniquely numbered _WorkItem and adds it to the "Work Items" dict
- adds the id of the _WorkItem to the "Work Ids" queue

Local worker thread:
- reads work ids from the "Work Ids" queue and looks up the corresponding
  WorkItem from the "Work Items" dict: if the work item has been cancelled then
  it is simply removed from the dict, otherwise it is repackaged as a
  _CallItem and put in the "Call Q". New _CallItems are put in the "Call Q"
  until "Call Q" is full. NOTE: the size of the "Call Q" is kept small because
  calls placed in the "Call Q" can no longer be cancelled with Future.cancel().
- reads _ResultItems from "Result Q", updates the future stored in the
  "Work Items" dict and deletes the dict entry

Process #1..n:
- reads _CallItems from "Call Q", executes the calls, and puts the resulting
  _ResultItems in "Result Q"
"""
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
import os
from concurrent.futures import _base
import queue, multiprocessing as mp, multiprocessing.connection
from multiprocessing.queues import Queue
import threading, weakref
from functools import partial
import itertools, sys, traceback
_threads_wakeups = weakref.WeakKeyDictionary()
_global_shutdown = False

class _ThreadWakeup:

    def __init__(self):
        self._closed = False
        self._reader, self._writer = mp.Pipe(duplex=False)

    def close(self):
        if not self._closed:
            self._closed = True
            self._writer.close()
            self._reader.close()

    def wakeup(self):
        if not self._closed:
            self._writer.send_bytes(b'')

    def clear(self):
        if not self._closed:
            while True:
                if self._reader.poll():
                    self._reader.recv_bytes()


def _python_exit():
    global _global_shutdown
    _global_shutdown = True
    items = list(_threads_wakeups.items())
    for _, thread_wakeup in items:
        thread_wakeup.wakeup()
    else:
        for t, _ in items:
            t.join()


threading._register_atexit(_python_exit)
EXTRA_QUEUED_CALLS = 1
_MAX_WINDOWS_WORKERS = 61

class _RemoteTraceback(Exception):

    def __init__(self, tb):
        self.tb = tb

    def __str__(self):
        return self.tb


class _ExceptionWithTraceback:

    def __init__(self, exc, tb):
        tb = traceback.format_exception(type(exc), exc, tb)
        tb = ''.join(tb)
        self.exc = exc
        self.tb = '\n"""\n%s"""' % tb

    def __reduce__(self):
        return (
         _rebuild_exc, (self.exc, self.tb))


def _rebuild_exc(exc, tb):
    exc.__cause__ = _RemoteTraceback(tb)
    return exc


class _WorkItem(object):

    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs


class _ResultItem(object):

    def __init__(self, work_id, exception=None, result=None):
        self.work_id = work_id
        self.exception = exception
        self.result = result


class _CallItem(object):

    def __init__(self, work_id, fn, args, kwargs):
        self.work_id = work_id
        self.fn = fn
        self.args = args
        self.kwargs = kwargs


class _SafeQueue(Queue):
    __doc__ = 'Safe Queue set exception to the future object linked to a job'

    def __init__(self, max_size=0, *, ctx, pending_work_items, shutdown_lock, thread_wakeup):
        self.pending_work_items = pending_work_items
        self.shutdown_lock = shutdown_lock
        self.thread_wakeup = thread_wakeup
        super().__init__(max_size, ctx=ctx)

    def _on_queue_feeder_error--- This code section failed: ---

 L. 168         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'obj'
                4  LOAD_GLOBAL              _CallItem
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE   138  'to 138'

 L. 169        10  LOAD_GLOBAL              traceback
               12  LOAD_METHOD              format_exception
               14  LOAD_GLOBAL              type
               16  LOAD_FAST                'e'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_FAST                'e'
               22  LOAD_FAST                'e'
               24  LOAD_ATTR                __traceback__
               26  CALL_METHOD_3         3  ''
               28  STORE_FAST               'tb'

 L. 170        30  LOAD_GLOBAL              _RemoteTraceback
               32  LOAD_STR                 '\n"""\n{}"""'
               34  LOAD_METHOD              format
               36  LOAD_STR                 ''
               38  LOAD_METHOD              join
               40  LOAD_FAST                'tb'
               42  CALL_METHOD_1         1  ''
               44  CALL_METHOD_1         1  ''
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_FAST                'e'
               50  STORE_ATTR               __cause__

 L. 171        52  LOAD_FAST                'self'
               54  LOAD_ATTR                pending_work_items
               56  LOAD_METHOD              pop
               58  LOAD_FAST                'obj'
               60  LOAD_ATTR                work_id
               62  LOAD_CONST               None
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'work_item'

 L. 172        68  LOAD_FAST                'self'
               70  LOAD_ATTR                shutdown_lock
               72  SETUP_WITH          100  'to 100'
               74  POP_TOP          

 L. 173        76  LOAD_FAST                'self'
               78  LOAD_ATTR                thread_wakeup
               80  LOAD_METHOD              wakeup
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          
               86  POP_BLOCK        
               88  LOAD_CONST               None
               90  DUP_TOP          
               92  DUP_TOP          
               94  CALL_FUNCTION_3       3  ''
               96  POP_TOP          
               98  JUMP_FORWARD        116  'to 116'
            100_0  COME_FROM_WITH       72  '72'
              100  <49>             
              102  POP_JUMP_IF_TRUE    106  'to 106'
              104  <48>             
            106_0  COME_FROM           102  '102'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          
              112  POP_EXCEPT       
              114  POP_TOP          
            116_0  COME_FROM            98  '98'

 L. 177       116  LOAD_FAST                'work_item'
              118  LOAD_CONST               None
              120  <117>                 1  ''
              122  POP_JUMP_IF_FALSE   152  'to 152'

 L. 178       124  LOAD_FAST                'work_item'
              126  LOAD_ATTR                future
              128  LOAD_METHOD              set_exception
              130  LOAD_FAST                'e'
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
              136  JUMP_FORWARD        152  'to 152'
            138_0  COME_FROM             8  '8'

 L. 180       138  LOAD_GLOBAL              super
              140  CALL_FUNCTION_0       0  ''
              142  LOAD_METHOD              _on_queue_feeder_error
              144  LOAD_FAST                'e'
              146  LOAD_FAST                'obj'
              148  CALL_METHOD_2         2  ''
              150  POP_TOP          
            152_0  COME_FROM           136  '136'
            152_1  COME_FROM           122  '122'

Parse error at or near `DUP_TOP' instruction at offset 90


def _get_chunks(*iterables, chunksize):
    """ Iterates over zip()ed iterables in chunks. """
    it = zip(*iterables)
    while True:
        chunk = tuple(itertools.isliceitchunksize)
        if not chunk:
            return
        else:
            yield chunk


def _process_chunk(fn, chunk):
    """ Processes a chunk of an iterable passed to map.

    Runs the function passed to map() on a chunk of the
    iterable passed to map.

    This function is run in a separate process.

    """
    return [fn(*args) for args in chunk]


def _sendback_result--- This code section failed: ---

 L. 207         0  SETUP_FINALLY        26  'to 26'

 L. 208         2  LOAD_FAST                'result_queue'
                4  LOAD_METHOD              put
                6  LOAD_GLOBAL              _ResultItem
                8  LOAD_FAST                'work_id'
               10  LOAD_FAST                'result'

 L. 209        12  LOAD_FAST                'exception'

 L. 208        14  LOAD_CONST               ('result', 'exception')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  JUMP_FORWARD         92  'to 92'
             26_0  COME_FROM_FINALLY     0  '0'

 L. 210        26  DUP_TOP          
               28  LOAD_GLOBAL              BaseException
               30  <121>                90  ''
               32  POP_TOP          
               34  STORE_FAST               'e'
               36  POP_TOP          
               38  SETUP_FINALLY        82  'to 82'

 L. 211        40  LOAD_GLOBAL              _ExceptionWithTraceback
               42  LOAD_FAST                'e'
               44  LOAD_FAST                'e'
               46  LOAD_ATTR                __traceback__
               48  CALL_FUNCTION_2       2  ''
               50  STORE_FAST               'exc'

 L. 212        52  LOAD_FAST                'result_queue'
               54  LOAD_METHOD              put
               56  LOAD_GLOBAL              _ResultItem
               58  LOAD_FAST                'work_id'
               60  LOAD_FAST                'exc'
               62  LOAD_CONST               ('exception',)
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
               70  POP_BLOCK        
               72  POP_EXCEPT       
               74  LOAD_CONST               None
               76  STORE_FAST               'e'
               78  DELETE_FAST              'e'
               80  JUMP_FORWARD         92  'to 92'
             82_0  COME_FROM_FINALLY    38  '38'
               82  LOAD_CONST               None
               84  STORE_FAST               'e'
               86  DELETE_FAST              'e'
               88  <48>             
               90  <48>             
             92_0  COME_FROM            80  '80'
             92_1  COME_FROM            24  '24'

Parse error at or near `<121>' instruction at offset 30


def _process_worker--- This code section failed: ---

 L. 228         0  LOAD_FAST                'initializer'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    58  'to 58'

 L. 229         8  SETUP_FINALLY        22  'to 22'

 L. 230        10  LOAD_FAST                'initializer'
               12  LOAD_FAST                'initargs'
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  POP_TOP          
               18  POP_BLOCK        
               20  JUMP_FORWARD         58  'to 58'
             22_0  COME_FROM_FINALLY     8  '8'

 L. 231        22  DUP_TOP          
               24  LOAD_GLOBAL              BaseException
               26  <121>                56  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 232        34  LOAD_GLOBAL              _base
               36  LOAD_ATTR                LOGGER
               38  LOAD_ATTR                critical
               40  LOAD_STR                 'Exception in initializer:'
               42  LOAD_CONST               True
               44  LOAD_CONST               ('exc_info',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  POP_TOP          

 L. 235        50  POP_EXCEPT       
               52  LOAD_CONST               None
               54  RETURN_VALUE     
               56  <48>             
             58_0  COME_FROM           206  '206'
             58_1  COME_FROM            20  '20'
             58_2  COME_FROM             6  '6'

 L. 237        58  LOAD_FAST                'call_queue'
               60  LOAD_ATTR                get
               62  LOAD_CONST               True
               64  LOAD_CONST               ('block',)
               66  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               68  STORE_FAST               'call_item'

 L. 238        70  LOAD_FAST                'call_item'
               72  LOAD_CONST               None
               74  <117>                 0  ''
               76  POP_JUMP_IF_FALSE    96  'to 96'

 L. 240        78  LOAD_FAST                'result_queue'
               80  LOAD_METHOD              put
               82  LOAD_GLOBAL              os
               84  LOAD_METHOD              getpid
               86  CALL_METHOD_0         0  ''
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L. 241        92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            76  '76'

 L. 242        96  SETUP_FINALLY       122  'to 122'

 L. 243        98  LOAD_FAST                'call_item'
              100  LOAD_ATTR                fn
              102  LOAD_FAST                'call_item'
              104  LOAD_ATTR                args
              106  BUILD_MAP_0           0 
              108  LOAD_FAST                'call_item'
              110  LOAD_ATTR                kwargs
              112  <164>                 1  ''
              114  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              116  STORE_FAST               'r'
              118  POP_BLOCK        
              120  JUMP_FORWARD        186  'to 186'
            122_0  COME_FROM_FINALLY    96  '96'

 L. 244       122  DUP_TOP          
              124  LOAD_GLOBAL              BaseException
              126  <121>               184  ''
              128  POP_TOP          
              130  STORE_FAST               'e'
              132  POP_TOP          
              134  SETUP_FINALLY       176  'to 176'

 L. 245       136  LOAD_GLOBAL              _ExceptionWithTraceback
              138  LOAD_FAST                'e'
              140  LOAD_FAST                'e'
              142  LOAD_ATTR                __traceback__
              144  CALL_FUNCTION_2       2  ''
              146  STORE_FAST               'exc'

 L. 246       148  LOAD_GLOBAL              _sendback_result
              150  LOAD_FAST                'result_queue'
              152  LOAD_FAST                'call_item'
              154  LOAD_ATTR                work_id
              156  LOAD_FAST                'exc'
              158  LOAD_CONST               ('exception',)
              160  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              162  POP_TOP          
              164  POP_BLOCK        
              166  POP_EXCEPT       
              168  LOAD_CONST               None
              170  STORE_FAST               'e'
              172  DELETE_FAST              'e'
              174  JUMP_FORWARD        204  'to 204'
            176_0  COME_FROM_FINALLY   134  '134'
              176  LOAD_CONST               None
              178  STORE_FAST               'e'
              180  DELETE_FAST              'e'
              182  <48>             
              184  <48>             
            186_0  COME_FROM           120  '120'

 L. 248       186  LOAD_GLOBAL              _sendback_result
              188  LOAD_FAST                'result_queue'
              190  LOAD_FAST                'call_item'
              192  LOAD_ATTR                work_id
              194  LOAD_FAST                'r'
              196  LOAD_CONST               ('result',)
              198  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              200  POP_TOP          

 L. 249       202  DELETE_FAST              'r'
            204_0  COME_FROM           174  '174'

 L. 253       204  DELETE_FAST              'call_item'
              206  JUMP_BACK            58  'to 58'

Parse error at or near `None' instruction at offset -1


class _ExecutorManagerThread(threading.Thread):
    __doc__ = 'Manages the communication between this process and the worker processes.\n\n    The manager is run in a local thread.\n\n    Args:\n        executor: A reference to the ProcessPoolExecutor that owns\n            this thread. A weakref will be own by the manager as well as\n            references to internal objects used to introspect the state of\n            the executor.\n    '

    def __init__(self, executor):
        self.thread_wakeup = executor._executor_manager_thread_wakeup
        self.shutdown_lock = executor._shutdown_lock

        def weakref_cb--- This code section failed: ---

 L. 285         0  LOAD_GLOBAL              mp
                2  LOAD_ATTR                util
                4  LOAD_METHOD              debug
                6  LOAD_STR                 'Executor collected: triggering callback for QueueManager wakeup'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 287        12  LOAD_FAST                'shutdown_lock'
               14  SETUP_WITH           40  'to 40'
               16  POP_TOP          

 L. 288        18  LOAD_FAST                'thread_wakeup'
               20  LOAD_METHOD              wakeup
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
               26  POP_BLOCK        
               28  LOAD_CONST               None
               30  DUP_TOP          
               32  DUP_TOP          
               34  CALL_FUNCTION_3       3  ''
               36  POP_TOP          
               38  JUMP_FORWARD         56  'to 56'
             40_0  COME_FROM_WITH       14  '14'
               40  <49>             
               42  POP_JUMP_IF_TRUE     46  'to 46'
               44  <48>             
             46_0  COME_FROM            42  '42'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          
               52  POP_EXCEPT       
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

Parse error at or near `DUP_TOP' instruction at offset 30

        self.executor_reference = weakref.refexecutorweakref_cb
        self.processes = executor._processes
        self.call_queue = executor._call_queue
        self.result_queue = executor._result_queue
        self.work_ids_queue = executor._work_ids
        self.pending_work_items = executor._pending_work_items
        super().__init__()

    def run--- This code section failed: ---
              0_0  COME_FROM           122  '122'
              0_1  COME_FROM           108  '108'
              0_2  COME_FROM            94  '94'

 L. 315         0  LOAD_FAST                'self'
                2  LOAD_METHOD              add_call_item_to_queue
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 317         8  LOAD_FAST                'self'
               10  LOAD_METHOD              wait_result_broken_or_wakeup
               12  CALL_METHOD_0         0  ''
               14  UNPACK_SEQUENCE_3     3 
               16  STORE_FAST               'result_item'
               18  STORE_FAST               'is_broken'
               20  STORE_FAST               'cause'

 L. 319        22  LOAD_FAST                'is_broken'
               24  POP_JUMP_IF_FALSE    40  'to 40'

 L. 320        26  LOAD_FAST                'self'
               28  LOAD_METHOD              terminate_broken
               30  LOAD_FAST                'cause'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 321        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            24  '24'

 L. 322        40  LOAD_FAST                'result_item'
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    88  'to 88'

 L. 323        48  LOAD_FAST                'self'
               50  LOAD_METHOD              process_result_item
               52  LOAD_FAST                'result_item'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 326        58  DELETE_FAST              'result_item'

 L. 329        60  LOAD_FAST                'self'
               62  LOAD_METHOD              executor_reference
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'executor'

 L. 330        68  LOAD_FAST                'executor'
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_FALSE    86  'to 86'

 L. 331        76  LOAD_FAST                'executor'
               78  LOAD_ATTR                _idle_worker_semaphore
               80  LOAD_METHOD              release
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          
             86_0  COME_FROM            74  '74'

 L. 332        86  DELETE_FAST              'executor'
             88_0  COME_FROM            46  '46'

 L. 334        88  LOAD_FAST                'self'
               90  LOAD_METHOD              is_shutting_down
               92  CALL_METHOD_0         0  ''
               94  POP_JUMP_IF_FALSE_BACK     0  'to 0'

 L. 335        96  LOAD_FAST                'self'
               98  LOAD_METHOD              flag_executor_shutting_down
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          

 L. 339       104  LOAD_FAST                'self'
              106  LOAD_ATTR                pending_work_items
              108  POP_JUMP_IF_TRUE_BACK     0  'to 0'

 L. 340       110  LOAD_FAST                'self'
              112  LOAD_METHOD              join_executor_internals
              114  CALL_METHOD_0         0  ''
              116  POP_TOP          

 L. 341       118  LOAD_CONST               None
              120  RETURN_VALUE     
              122  JUMP_BACK             0  'to 0'

Parse error at or near `<117>' instruction at offset 44

    def add_call_item_to_queue--- This code section failed: ---
              0_0  COME_FROM           120  '120'
              0_1  COME_FROM           118  '118'
              0_2  COME_FROM           108  '108'

 L. 347         0  LOAD_FAST                'self'
                2  LOAD_ATTR                call_queue
                4  LOAD_METHOD              full
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 348        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 349        14  SETUP_FINALLY        34  'to 34'

 L. 350        16  LOAD_FAST                'self'
               18  LOAD_ATTR                work_ids_queue
               20  LOAD_ATTR                get
               22  LOAD_CONST               False
               24  LOAD_CONST               ('block',)
               26  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               28  STORE_FAST               'work_id'
               30  POP_BLOCK        
               32  JUMP_FORWARD         56  'to 56'
             34_0  COME_FROM_FINALLY    14  '14'

 L. 351        34  DUP_TOP          
               36  LOAD_GLOBAL              queue
               38  LOAD_ATTR                Empty
               40  <121>                54  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 352        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
               54  <48>             
             56_0  COME_FROM            32  '32'

 L. 354        56  LOAD_FAST                'self'
               58  LOAD_ATTR                pending_work_items
               60  LOAD_FAST                'work_id'
               62  BINARY_SUBSCR    
               64  STORE_FAST               'work_item'

 L. 356        66  LOAD_FAST                'work_item'
               68  LOAD_ATTR                future
               70  LOAD_METHOD              set_running_or_notify_cancel
               72  CALL_METHOD_0         0  ''
               74  POP_JUMP_IF_FALSE   110  'to 110'

 L. 357        76  LOAD_FAST                'self'
               78  LOAD_ATTR                call_queue
               80  LOAD_ATTR                put
               82  LOAD_GLOBAL              _CallItem
               84  LOAD_FAST                'work_id'

 L. 358        86  LOAD_FAST                'work_item'
               88  LOAD_ATTR                fn

 L. 359        90  LOAD_FAST                'work_item'
               92  LOAD_ATTR                args

 L. 360        94  LOAD_FAST                'work_item'
               96  LOAD_ATTR                kwargs

 L. 357        98  CALL_FUNCTION_4       4  ''

 L. 361       100  LOAD_CONST               True

 L. 357       102  LOAD_CONST               ('block',)
              104  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              106  POP_TOP          
              108  JUMP_BACK             0  'to 0'
            110_0  COME_FROM            74  '74'

 L. 363       110  LOAD_FAST                'self'
              112  LOAD_ATTR                pending_work_items
              114  LOAD_FAST                'work_id'
              116  DELETE_SUBSCR    

 L. 364       118  CONTINUE              0  'to 0'
              120  JUMP_BACK             0  'to 0'

Parse error at or near `<121>' instruction at offset 40

    def wait_result_broken_or_wakeup--- This code section failed: ---

 L. 372         0  LOAD_FAST                'self'
                2  LOAD_ATTR                result_queue
                4  LOAD_ATTR                _reader
                6  STORE_FAST               'result_reader'

 L. 373         8  LOAD_FAST                'self'
               10  LOAD_ATTR                thread_wakeup
               12  LOAD_ATTR                _closed
               14  POP_JUMP_IF_FALSE    20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 374        20  LOAD_FAST                'self'
               22  LOAD_ATTR                thread_wakeup
               24  LOAD_ATTR                _reader
               26  STORE_FAST               'wakeup_reader'

 L. 375        28  LOAD_FAST                'result_reader'
               30  LOAD_FAST                'wakeup_reader'
               32  BUILD_LIST_2          2 
               34  STORE_FAST               'readers'

 L. 376        36  LOAD_LISTCOMP            '<code_object <listcomp>>'
               38  LOAD_STR                 '_ExecutorManagerThread.wait_result_broken_or_wakeup.<locals>.<listcomp>'
               40  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                processes
               46  LOAD_METHOD              values
               48  CALL_METHOD_0         0  ''
               50  GET_ITER         
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'worker_sentinels'

 L. 377        56  LOAD_GLOBAL              mp
               58  LOAD_ATTR                connection
               60  LOAD_METHOD              wait
               62  LOAD_FAST                'readers'
               64  LOAD_FAST                'worker_sentinels'
               66  BINARY_ADD       
               68  CALL_METHOD_1         1  ''
               70  STORE_FAST               'ready'

 L. 379        72  LOAD_CONST               None
               74  STORE_FAST               'cause'

 L. 380        76  LOAD_CONST               True
               78  STORE_FAST               'is_broken'

 L. 381        80  LOAD_CONST               None
               82  STORE_FAST               'result_item'

 L. 382        84  LOAD_FAST                'result_reader'
               86  LOAD_FAST                'ready'
               88  <118>                 0  ''
               90  POP_JUMP_IF_FALSE   168  'to 168'

 L. 383        92  SETUP_FINALLY       110  'to 110'

 L. 384        94  LOAD_FAST                'result_reader'
               96  LOAD_METHOD              recv
               98  CALL_METHOD_0         0  ''
              100  STORE_FAST               'result_item'

 L. 385       102  LOAD_CONST               False
              104  STORE_FAST               'is_broken'
              106  POP_BLOCK        
              108  JUMP_FORWARD        180  'to 180'
            110_0  COME_FROM_FINALLY    92  '92'

 L. 386       110  DUP_TOP          
              112  LOAD_GLOBAL              BaseException
              114  <121>               164  ''
              116  POP_TOP          
              118  STORE_FAST               'e'
              120  POP_TOP          
              122  SETUP_FINALLY       156  'to 156'

 L. 387       124  LOAD_GLOBAL              traceback
              126  LOAD_METHOD              format_exception
              128  LOAD_GLOBAL              type
              130  LOAD_FAST                'e'
              132  CALL_FUNCTION_1       1  ''
              134  LOAD_FAST                'e'
              136  LOAD_FAST                'e'
              138  LOAD_ATTR                __traceback__
              140  CALL_METHOD_3         3  ''
              142  STORE_FAST               'cause'
              144  POP_BLOCK        
              146  POP_EXCEPT       
              148  LOAD_CONST               None
              150  STORE_FAST               'e'
              152  DELETE_FAST              'e'
              154  JUMP_FORWARD        180  'to 180'
            156_0  COME_FROM_FINALLY   122  '122'
              156  LOAD_CONST               None
              158  STORE_FAST               'e'
              160  DELETE_FAST              'e'
              162  <48>             
              164  <48>             
              166  JUMP_FORWARD        180  'to 180'
            168_0  COME_FROM            90  '90'

 L. 389       168  LOAD_FAST                'wakeup_reader'
              170  LOAD_FAST                'ready'
              172  <118>                 0  ''
              174  POP_JUMP_IF_FALSE   180  'to 180'

 L. 390       176  LOAD_CONST               False
              178  STORE_FAST               'is_broken'
            180_0  COME_FROM           174  '174'
            180_1  COME_FROM           166  '166'
            180_2  COME_FROM           154  '154'
            180_3  COME_FROM           108  '108'

 L. 392       180  LOAD_FAST                'self'
              182  LOAD_ATTR                shutdown_lock
              184  SETUP_WITH          212  'to 212'
              186  POP_TOP          

 L. 393       188  LOAD_FAST                'self'
              190  LOAD_ATTR                thread_wakeup
              192  LOAD_METHOD              clear
              194  CALL_METHOD_0         0  ''
              196  POP_TOP          
              198  POP_BLOCK        
              200  LOAD_CONST               None
              202  DUP_TOP          
              204  DUP_TOP          
              206  CALL_FUNCTION_3       3  ''
              208  POP_TOP          
              210  JUMP_FORWARD        228  'to 228'
            212_0  COME_FROM_WITH      184  '184'
              212  <49>             
              214  POP_JUMP_IF_TRUE    218  'to 218'
              216  <48>             
            218_0  COME_FROM           214  '214'
              218  POP_TOP          
              220  POP_TOP          
              222  POP_TOP          
              224  POP_EXCEPT       
              226  POP_TOP          
            228_0  COME_FROM           210  '210'

 L. 395       228  LOAD_FAST                'result_item'
              230  LOAD_FAST                'is_broken'
              232  LOAD_FAST                'cause'
              234  BUILD_TUPLE_3         3 
              236  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 16

    def process_result_item--- This code section failed: ---

 L. 401         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'result_item'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    62  'to 62'

 L. 404        10  LOAD_FAST                'self'
               12  LOAD_METHOD              is_shutting_down
               14  CALL_METHOD_0         0  ''
               16  POP_JUMP_IF_TRUE     22  'to 22'
               18  <74>             
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            16  '16'

 L. 405        22  LOAD_FAST                'self'
               24  LOAD_ATTR                processes
               26  LOAD_METHOD              pop
               28  LOAD_FAST                'result_item'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'p'

 L. 406        34  LOAD_FAST                'p'
               36  LOAD_METHOD              join
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 407        42  LOAD_FAST                'self'
               44  LOAD_ATTR                processes
               46  POP_JUMP_IF_TRUE    122  'to 122'

 L. 408        48  LOAD_FAST                'self'
               50  LOAD_METHOD              join_executor_internals
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          

 L. 409        56  LOAD_CONST               None
               58  RETURN_VALUE     
               60  JUMP_FORWARD        122  'to 122'
             62_0  COME_FROM             8  '8'

 L. 412        62  LOAD_FAST                'self'
               64  LOAD_ATTR                pending_work_items
               66  LOAD_METHOD              pop
               68  LOAD_FAST                'result_item'
               70  LOAD_ATTR                work_id
               72  LOAD_CONST               None
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'work_item'

 L. 414        78  LOAD_FAST                'work_item'
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   122  'to 122'

 L. 415        86  LOAD_FAST                'result_item'
               88  LOAD_ATTR                exception
               90  POP_JUMP_IF_FALSE   108  'to 108'

 L. 416        92  LOAD_FAST                'work_item'
               94  LOAD_ATTR                future
               96  LOAD_METHOD              set_exception
               98  LOAD_FAST                'result_item'
              100  LOAD_ATTR                exception
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
              106  JUMP_FORWARD        122  'to 122'
            108_0  COME_FROM            90  '90'

 L. 418       108  LOAD_FAST                'work_item'
              110  LOAD_ATTR                future
              112  LOAD_METHOD              set_result
              114  LOAD_FAST                'result_item'
              116  LOAD_ATTR                result
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
            122_0  COME_FROM           106  '106'
            122_1  COME_FROM            84  '84'
            122_2  COME_FROM            60  '60'
            122_3  COME_FROM            46  '46'

Parse error at or near `<74>' instruction at offset 18

    def is_shutting_down--- This code section failed: ---

 L. 422         0  LOAD_FAST                'self'
                2  LOAD_METHOD              executor_reference
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'executor'

 L. 427         8  LOAD_GLOBAL              _global_shutdown
               10  JUMP_IF_TRUE_OR_POP    24  'to 24'
               12  LOAD_FAST                'executor'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  JUMP_IF_TRUE_OR_POP    24  'to 24'

 L. 428        20  LOAD_FAST                'executor'
               22  LOAD_ATTR                _shutdown_thread
             24_0  COME_FROM            18  '18'
             24_1  COME_FROM            10  '10'

 L. 427        24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def terminate_broken--- This code section failed: ---

 L. 436         0  LOAD_FAST                'self'
                2  LOAD_METHOD              executor_reference
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'executor'

 L. 437         8  LOAD_FAST                'executor'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    32  'to 32'

 L. 438        16  LOAD_STR                 'A child process terminated abruptly, the process pool is not usable anymore'
               18  LOAD_FAST                'executor'
               20  STORE_ATTR               _broken

 L. 441        22  LOAD_CONST               True
               24  LOAD_FAST                'executor'
               26  STORE_ATTR               _shutdown_thread

 L. 442        28  LOAD_CONST               None
               30  STORE_FAST               'executor'
             32_0  COME_FROM            14  '14'

 L. 446        32  LOAD_GLOBAL              BrokenProcessPool
               34  LOAD_STR                 'A process in the process pool was terminated abruptly while the future was running or pending.'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'bpe'

 L. 449        40  LOAD_FAST                'cause'
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    72  'to 72'

 L. 450        48  LOAD_GLOBAL              _RemoteTraceback

 L. 451        50  LOAD_STR                 "\n'''\n"
               52  LOAD_STR                 ''
               54  LOAD_METHOD              join
               56  LOAD_FAST                'cause'
               58  CALL_METHOD_1         1  ''
               60  FORMAT_VALUE          0  ''
               62  LOAD_STR                 "'''"
               64  BUILD_STRING_3        3 

 L. 450        66  CALL_FUNCTION_1       1  ''
               68  LOAD_FAST                'bpe'
               70  STORE_ATTR               __cause__
             72_0  COME_FROM            46  '46'

 L. 454        72  LOAD_FAST                'self'
               74  LOAD_ATTR                pending_work_items
               76  LOAD_METHOD              items
               78  CALL_METHOD_0         0  ''
               80  GET_ITER         
             82_0  COME_FROM           104  '104'
               82  FOR_ITER            106  'to 106'
               84  UNPACK_SEQUENCE_2     2 
               86  STORE_FAST               'work_id'
               88  STORE_FAST               'work_item'

 L. 455        90  LOAD_FAST                'work_item'
               92  LOAD_ATTR                future
               94  LOAD_METHOD              set_exception
               96  LOAD_FAST                'bpe'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 457       102  DELETE_FAST              'work_item'
              104  JUMP_BACK            82  'to 82'
            106_0  COME_FROM            82  '82'

 L. 458       106  LOAD_FAST                'self'
              108  LOAD_ATTR                pending_work_items
              110  LOAD_METHOD              clear
              112  CALL_METHOD_0         0  ''
              114  POP_TOP          

 L. 462       116  LOAD_FAST                'self'
              118  LOAD_ATTR                processes
              120  LOAD_METHOD              values
              122  CALL_METHOD_0         0  ''
              124  GET_ITER         
            126_0  COME_FROM           138  '138'
              126  FOR_ITER            140  'to 140'
              128  STORE_FAST               'p'

 L. 463       130  LOAD_FAST                'p'
              132  LOAD_METHOD              terminate
              134  CALL_METHOD_0         0  ''
              136  POP_TOP          
              138  JUMP_BACK           126  'to 126'
            140_0  COME_FROM           126  '126'

 L. 466       140  LOAD_FAST                'self'
              142  LOAD_METHOD              join_executor_internals
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          

Parse error at or near `<117>' instruction at offset 12

    def flag_executor_shutting_down--- This code section failed: ---

 L. 471         0  LOAD_FAST                'self'
                2  LOAD_METHOD              executor_reference
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'executor'

 L. 472         8  LOAD_FAST                'executor'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE   124  'to 124'

 L. 473        16  LOAD_CONST               True
               18  LOAD_FAST                'executor'
               20  STORE_ATTR               _shutdown_thread

 L. 475        22  LOAD_FAST                'executor'
               24  LOAD_ATTR                _cancel_pending_futures
               26  POP_JUMP_IF_FALSE   124  'to 124'

 L. 478        28  BUILD_MAP_0           0 
               30  STORE_FAST               'new_pending_work_items'

 L. 479        32  LOAD_FAST                'self'
               34  LOAD_ATTR                pending_work_items
               36  LOAD_METHOD              items
               38  CALL_METHOD_0         0  ''
               40  GET_ITER         
             42_0  COME_FROM            68  '68'
             42_1  COME_FROM            58  '58'
               42  FOR_ITER             70  'to 70'
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'work_id'
               48  STORE_FAST               'work_item'

 L. 480        50  LOAD_FAST                'work_item'
               52  LOAD_ATTR                future
               54  LOAD_METHOD              cancel
               56  CALL_METHOD_0         0  ''
               58  POP_JUMP_IF_TRUE_BACK    42  'to 42'

 L. 481        60  LOAD_FAST                'work_item'
               62  LOAD_FAST                'new_pending_work_items'
               64  LOAD_FAST                'work_id'
               66  STORE_SUBSCR     
               68  JUMP_BACK            42  'to 42'
             70_0  COME_FROM            42  '42'

 L. 482        70  LOAD_FAST                'new_pending_work_items'
               72  LOAD_FAST                'self'
               74  STORE_ATTR               pending_work_items
             76_0  COME_FROM           116  '116'
             76_1  COME_FROM           112  '112'
             76_2  COME_FROM            90  '90'

 L. 486        76  SETUP_FINALLY        92  'to 92'

 L. 487        78  LOAD_FAST                'self'
               80  LOAD_ATTR                work_ids_queue
               82  LOAD_METHOD              get_nowait
               84  CALL_METHOD_0         0  ''
               86  POP_TOP          
               88  POP_BLOCK        
               90  JUMP_BACK            76  'to 76'
             92_0  COME_FROM_FINALLY    76  '76'

 L. 488        92  DUP_TOP          
               94  LOAD_GLOBAL              queue
               96  LOAD_ATTR                Empty
               98  <121>               114  ''
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 489       106  POP_EXCEPT       
              108  BREAK_LOOP          118  'to 118'
              110  POP_EXCEPT       
              112  JUMP_BACK            76  'to 76'
              114  <48>             
              116  JUMP_BACK            76  'to 76'
            118_0  COME_FROM           108  '108'

 L. 492       118  LOAD_CONST               False
              120  LOAD_FAST                'executor'
              122  STORE_ATTR               _cancel_pending_futures
            124_0  COME_FROM            26  '26'
            124_1  COME_FROM            14  '14'

Parse error at or near `<117>' instruction at offset 12

    def shutdown_workers--- This code section failed: ---

 L. 495         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_n_children_alive
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'n_children_to_stop'

 L. 496         8  LOAD_CONST               0
               10  STORE_FAST               'n_sentinels_sent'
             12_0  COME_FROM           102  '102'
             12_1  COME_FROM            92  '92'

 L. 499        12  LOAD_FAST                'n_sentinels_sent'
               14  LOAD_FAST                'n_children_to_stop'
               16  COMPARE_OP               <
               18  POP_JUMP_IF_FALSE   104  'to 104'

 L. 500        20  LOAD_FAST                'self'
               22  LOAD_METHOD              get_n_children_alive
               24  CALL_METHOD_0         0  ''
               26  LOAD_CONST               0
               28  COMPARE_OP               >

 L. 499        30  POP_JUMP_IF_FALSE   104  'to 104'

 L. 501        32  LOAD_GLOBAL              range
               34  LOAD_FAST                'n_children_to_stop'
               36  LOAD_FAST                'n_sentinels_sent'
               38  BINARY_SUBTRACT  
               40  CALL_FUNCTION_1       1  ''
               42  GET_ITER         
             44_0  COME_FROM           100  '100'
             44_1  COME_FROM            96  '96'
             44_2  COME_FROM            72  '72'
               44  FOR_ITER            102  'to 102'
               46  STORE_FAST               'i'

 L. 502        48  SETUP_FINALLY        74  'to 74'

 L. 503        50  LOAD_FAST                'self'
               52  LOAD_ATTR                call_queue
               54  LOAD_METHOD              put_nowait
               56  LOAD_CONST               None
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 504        62  LOAD_FAST                'n_sentinels_sent'
               64  LOAD_CONST               1
               66  INPLACE_ADD      
               68  STORE_FAST               'n_sentinels_sent'
               70  POP_BLOCK        
               72  JUMP_BACK            44  'to 44'
             74_0  COME_FROM_FINALLY    48  '48'

 L. 505        74  DUP_TOP          
               76  LOAD_GLOBAL              queue
               78  LOAD_ATTR                Full
               80  <121>                98  ''
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 506        88  POP_EXCEPT       
               90  POP_TOP          
               92  JUMP_BACK            12  'to 12'
               94  POP_EXCEPT       
               96  JUMP_BACK            44  'to 44'
               98  <48>             
              100  JUMP_BACK            44  'to 44'
            102_0  COME_FROM            44  '44'
              102  JUMP_BACK            12  'to 12'
            104_0  COME_FROM            30  '30'
            104_1  COME_FROM            18  '18'

Parse error at or near `<121>' instruction at offset 80

    def join_executor_internals--- This code section failed: ---

 L. 509         0  LOAD_FAST                'self'
                2  LOAD_METHOD              shutdown_workers
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 511         8  LOAD_FAST                'self'
               10  LOAD_ATTR                call_queue
               12  LOAD_METHOD              close
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          

 L. 512        18  LOAD_FAST                'self'
               20  LOAD_ATTR                call_queue
               22  LOAD_METHOD              join_thread
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          

 L. 513        28  LOAD_FAST                'self'
               30  LOAD_ATTR                shutdown_lock
               32  SETUP_WITH           60  'to 60'
               34  POP_TOP          

 L. 514        36  LOAD_FAST                'self'
               38  LOAD_ATTR                thread_wakeup
               40  LOAD_METHOD              close
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  LOAD_CONST               None
               50  DUP_TOP          
               52  DUP_TOP          
               54  CALL_FUNCTION_3       3  ''
               56  POP_TOP          
               58  JUMP_FORWARD         76  'to 76'
             60_0  COME_FROM_WITH       32  '32'
               60  <49>             
               62  POP_JUMP_IF_TRUE     66  'to 66'
               64  <48>             
             66_0  COME_FROM            62  '62'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          
               72  POP_EXCEPT       
               74  POP_TOP          
             76_0  COME_FROM            58  '58'

 L. 517        76  LOAD_FAST                'self'
               78  LOAD_ATTR                processes
               80  LOAD_METHOD              values
               82  CALL_METHOD_0         0  ''
               84  GET_ITER         
             86_0  COME_FROM            98  '98'
               86  FOR_ITER            100  'to 100'
               88  STORE_FAST               'p'

 L. 518        90  LOAD_FAST                'p'
               92  LOAD_METHOD              join
               94  CALL_METHOD_0         0  ''
               96  POP_TOP          
               98  JUMP_BACK            86  'to 86'
            100_0  COME_FROM            86  '86'

Parse error at or near `DUP_TOP' instruction at offset 50

    def get_n_children_alive(self):
        return sum((p.is_alive() for p in self.processes.values()))


_system_limits_checked = False
_system_limited = None

def _check_system_limits--- This code section failed: ---

 L. 531         0  LOAD_GLOBAL              _system_limits_checked
                2  POP_JUMP_IF_FALSE    16  'to 16'

 L. 532         4  LOAD_GLOBAL              _system_limited
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 533         8  LOAD_GLOBAL              NotImplementedError
               10  LOAD_GLOBAL              _system_limited
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'
             16_1  COME_FROM             2  '2'

 L. 534        16  LOAD_CONST               True
               18  STORE_GLOBAL             _system_limits_checked

 L. 535        20  SETUP_FINALLY        36  'to 36'

 L. 536        22  LOAD_GLOBAL              os
               24  LOAD_METHOD              sysconf
               26  LOAD_STR                 'SC_SEM_NSEMS_MAX'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'nsems_max'
               32  POP_BLOCK        
               34  JUMP_FORWARD         60  'to 60'
             36_0  COME_FROM_FINALLY    20  '20'

 L. 537        36  DUP_TOP          
               38  LOAD_GLOBAL              AttributeError
               40  LOAD_GLOBAL              ValueError
               42  BUILD_TUPLE_2         2 
               44  <121>                58  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 539        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
               58  <48>             
             60_0  COME_FROM            34  '34'

 L. 540        60  LOAD_FAST                'nsems_max'
               62  LOAD_CONST               -1
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    72  'to 72'

 L. 543        68  LOAD_CONST               None
               70  RETURN_VALUE     
             72_0  COME_FROM            66  '66'

 L. 544        72  LOAD_FAST                'nsems_max'
               74  LOAD_CONST               256
               76  COMPARE_OP               >=
               78  POP_JUMP_IF_FALSE    84  'to 84'

 L. 547        80  LOAD_CONST               None
               82  RETURN_VALUE     
             84_0  COME_FROM            78  '78'

 L. 548        84  LOAD_STR                 'system provides too few semaphores (%d available, 256 necessary)'

 L. 549        86  LOAD_FAST                'nsems_max'

 L. 548        88  BINARY_MODULO    
               90  STORE_GLOBAL             _system_limited

 L. 550        92  LOAD_GLOBAL              NotImplementedError
               94  LOAD_GLOBAL              _system_limited
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 44


def _chain_from_iterable_of_lists(iterable):
    """
    Specialized implementation of itertools.chain.from_iterable.
    Each item in *iterable* should be a list.  This function is
    careful not to keep references to yielded objects.
    """
    for element in iterable:
        element.reverse()
        while True:
            if element:
                yield element.pop()


class BrokenProcessPool(_base.BrokenExecutor):
    __doc__ = '\n    Raised when a process in a ProcessPoolExecutor terminated abruptly\n    while a future was in the running state.\n    '


class ProcessPoolExecutor(_base.Executor):

    def __init__--- This code section failed: ---

 L. 586         0  LOAD_GLOBAL              _check_system_limits
                2  CALL_FUNCTION_0       0  ''
                4  POP_TOP          

 L. 588         6  LOAD_FAST                'max_workers'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    54  'to 54'

 L. 589        14  LOAD_GLOBAL              os
               16  LOAD_METHOD              cpu_count
               18  CALL_METHOD_0         0  ''
               20  JUMP_IF_TRUE_OR_POP    24  'to 24'
               22  LOAD_CONST               1
             24_0  COME_FROM            20  '20'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _max_workers

 L. 590        28  LOAD_GLOBAL              sys
               30  LOAD_ATTR                platform
               32  LOAD_STR                 'win32'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE   110  'to 110'

 L. 591        38  LOAD_GLOBAL              min
               40  LOAD_GLOBAL              _MAX_WINDOWS_WORKERS

 L. 592        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _max_workers

 L. 591        46  CALL_FUNCTION_2       2  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _max_workers
               52  JUMP_FORWARD        110  'to 110'
             54_0  COME_FROM            12  '12'

 L. 594        54  LOAD_FAST                'max_workers'
               56  LOAD_CONST               0
               58  COMPARE_OP               <=
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L. 595        62  LOAD_GLOBAL              ValueError
               64  LOAD_STR                 'max_workers must be greater than 0'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
               70  JUMP_FORWARD        104  'to 104'
             72_0  COME_FROM            60  '60'

 L. 596        72  LOAD_GLOBAL              sys
               74  LOAD_ATTR                platform
               76  LOAD_STR                 'win32'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   104  'to 104'

 L. 597        82  LOAD_FAST                'max_workers'
               84  LOAD_GLOBAL              _MAX_WINDOWS_WORKERS
               86  COMPARE_OP               >

 L. 596        88  POP_JUMP_IF_FALSE   104  'to 104'

 L. 598        90  LOAD_GLOBAL              ValueError

 L. 599        92  LOAD_STR                 'max_workers must be <= '
               94  LOAD_GLOBAL              _MAX_WINDOWS_WORKERS
               96  FORMAT_VALUE          0  ''
               98  BUILD_STRING_2        2 

 L. 598       100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            88  '88'
            104_1  COME_FROM            80  '80'
            104_2  COME_FROM            70  '70'

 L. 601       104  LOAD_FAST                'max_workers'
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _max_workers
            110_0  COME_FROM            52  '52'
            110_1  COME_FROM            36  '36'

 L. 603       110  LOAD_FAST                'mp_context'
              112  LOAD_CONST               None
              114  <117>                 0  ''
              116  POP_JUMP_IF_FALSE   126  'to 126'

 L. 604       118  LOAD_GLOBAL              mp
              120  LOAD_METHOD              get_context
              122  CALL_METHOD_0         0  ''
              124  STORE_FAST               'mp_context'
            126_0  COME_FROM           116  '116'

 L. 605       126  LOAD_FAST                'mp_context'
              128  LOAD_FAST                'self'
              130  STORE_ATTR               _mp_context

 L. 607       132  LOAD_FAST                'initializer'
              134  LOAD_CONST               None
              136  <117>                 1  ''
              138  POP_JUMP_IF_FALSE   156  'to 156'
              140  LOAD_GLOBAL              callable
              142  LOAD_FAST                'initializer'
              144  CALL_FUNCTION_1       1  ''
              146  POP_JUMP_IF_TRUE    156  'to 156'

 L. 608       148  LOAD_GLOBAL              TypeError
              150  LOAD_STR                 'initializer must be a callable'
              152  CALL_FUNCTION_1       1  ''
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           146  '146'
            156_1  COME_FROM           138  '138'

 L. 609       156  LOAD_FAST                'initializer'
              158  LOAD_FAST                'self'
              160  STORE_ATTR               _initializer

 L. 610       162  LOAD_FAST                'initargs'
              164  LOAD_FAST                'self'
              166  STORE_ATTR               _initargs

 L. 613       168  LOAD_CONST               None
              170  LOAD_FAST                'self'
              172  STORE_ATTR               _executor_manager_thread

 L. 616       174  BUILD_MAP_0           0 
              176  LOAD_FAST                'self'
              178  STORE_ATTR               _processes

 L. 619       180  LOAD_CONST               False
              182  LOAD_FAST                'self'
              184  STORE_ATTR               _shutdown_thread

 L. 620       186  LOAD_GLOBAL              threading
              188  LOAD_METHOD              Lock
              190  CALL_METHOD_0         0  ''
              192  LOAD_FAST                'self'
              194  STORE_ATTR               _shutdown_lock

 L. 621       196  LOAD_GLOBAL              threading
              198  LOAD_METHOD              Semaphore
              200  LOAD_CONST               0
              202  CALL_METHOD_1         1  ''
              204  LOAD_FAST                'self'
              206  STORE_ATTR               _idle_worker_semaphore

 L. 622       208  LOAD_CONST               False
              210  LOAD_FAST                'self'
              212  STORE_ATTR               _broken

 L. 623       214  LOAD_CONST               0
              216  LOAD_FAST                'self'
              218  STORE_ATTR               _queue_count

 L. 624       220  BUILD_MAP_0           0 
              222  LOAD_FAST                'self'
              224  STORE_ATTR               _pending_work_items

 L. 625       226  LOAD_CONST               False
              228  LOAD_FAST                'self'
              230  STORE_ATTR               _cancel_pending_futures

 L. 635       232  LOAD_GLOBAL              _ThreadWakeup
              234  CALL_FUNCTION_0       0  ''
              236  LOAD_FAST                'self'
              238  STORE_ATTR               _executor_manager_thread_wakeup

 L. 641       240  LOAD_FAST                'self'
              242  LOAD_ATTR                _max_workers
              244  LOAD_GLOBAL              EXTRA_QUEUED_CALLS
              246  BINARY_ADD       
              248  STORE_FAST               'queue_size'

 L. 642       250  LOAD_GLOBAL              _SafeQueue

 L. 643       252  LOAD_FAST                'queue_size'
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                _mp_context

 L. 644       258  LOAD_FAST                'self'
              260  LOAD_ATTR                _pending_work_items

 L. 645       262  LOAD_FAST                'self'
              264  LOAD_ATTR                _shutdown_lock

 L. 646       266  LOAD_FAST                'self'
              268  LOAD_ATTR                _executor_manager_thread_wakeup

 L. 642       270  LOAD_CONST               ('max_size', 'ctx', 'pending_work_items', 'shutdown_lock', 'thread_wakeup')
              272  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              274  LOAD_FAST                'self'
              276  STORE_ATTR               _call_queue

 L. 650       278  LOAD_CONST               True
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                _call_queue
              284  STORE_ATTR               _ignore_epipe

 L. 651       286  LOAD_FAST                'mp_context'
              288  LOAD_METHOD              SimpleQueue
              290  CALL_METHOD_0         0  ''
              292  LOAD_FAST                'self'
              294  STORE_ATTR               _result_queue

 L. 652       296  LOAD_GLOBAL              queue
              298  LOAD_METHOD              Queue
              300  CALL_METHOD_0         0  ''
              302  LOAD_FAST                'self'
              304  STORE_ATTR               _work_ids

Parse error at or near `<117>' instruction at offset 10

    def _start_executor_manager_thread--- This code section failed: ---

 L. 655         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _executor_manager_thread
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    42  'to 42'

 L. 657        10  LOAD_GLOBAL              _ExecutorManagerThread
               12  LOAD_FAST                'self'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _executor_manager_thread

 L. 658        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _executor_manager_thread
               24  LOAD_METHOD              start
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          

 L. 660        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _executor_manager_thread_wakeup

 L. 659        34  LOAD_GLOBAL              _threads_wakeups
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _executor_manager_thread
               40  STORE_SUBSCR     
             42_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def _adjust_process_count(self):
        if self._idle_worker_semaphore.acquire(blocking=False):
            return
        process_count = len(self._processes)
        if process_count < self._max_workers:
            p = self._mp_context.Process(target=_process_worker,
              args=(
             self._call_queue,
             self._result_queue,
             self._initializer,
             self._initargs))
            p.start()
            self._processes[p.pid] = p

    def submit--- This code section failed: ---

 L. 679         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _shutdown_lock
                4  SETUP_WITH          156  'to 156'
                6  POP_TOP          

 L. 680         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _broken
               12  POP_JUMP_IF_FALSE    24  'to 24'

 L. 681        14  LOAD_GLOBAL              BrokenProcessPool
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _broken
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            12  '12'

 L. 682        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _shutdown_thread
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 683        30  LOAD_GLOBAL              RuntimeError
               32  LOAD_STR                 'cannot schedule new futures after shutdown'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 684        38  LOAD_GLOBAL              _global_shutdown
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L. 685        42  LOAD_GLOBAL              RuntimeError
               44  LOAD_STR                 'cannot schedule new futures after interpreter shutdown'
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            40  '40'

 L. 688        50  LOAD_GLOBAL              _base
               52  LOAD_METHOD              Future
               54  CALL_METHOD_0         0  ''
               56  STORE_FAST               'f'

 L. 689        58  LOAD_GLOBAL              _WorkItem
               60  LOAD_FAST                'f'
               62  LOAD_FAST                'fn'
               64  LOAD_FAST                'args'
               66  LOAD_FAST                'kwargs'
               68  CALL_FUNCTION_4       4  ''
               70  STORE_FAST               'w'

 L. 691        72  LOAD_FAST                'w'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _pending_work_items
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _queue_count
               82  STORE_SUBSCR     

 L. 692        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _work_ids
               88  LOAD_METHOD              put
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _queue_count
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 693        98  LOAD_FAST                'self'
              100  DUP_TOP          
              102  LOAD_ATTR                _queue_count
              104  LOAD_CONST               1
              106  INPLACE_ADD      
              108  ROT_TWO          
              110  STORE_ATTR               _queue_count

 L. 695       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _executor_manager_thread_wakeup
              116  LOAD_METHOD              wakeup
              118  CALL_METHOD_0         0  ''
              120  POP_TOP          

 L. 697       122  LOAD_FAST                'self'
              124  LOAD_METHOD              _adjust_process_count
              126  CALL_METHOD_0         0  ''
              128  POP_TOP          

 L. 698       130  LOAD_FAST                'self'
              132  LOAD_METHOD              _start_executor_manager_thread
              134  CALL_METHOD_0         0  ''
              136  POP_TOP          

 L. 699       138  LOAD_FAST                'f'
              140  POP_BLOCK        
              142  ROT_TWO          
              144  LOAD_CONST               None
              146  DUP_TOP          
              148  DUP_TOP          
              150  CALL_FUNCTION_3       3  ''
              152  POP_TOP          
              154  RETURN_VALUE     
            156_0  COME_FROM_WITH        4  '4'
              156  <49>             
              158  POP_JUMP_IF_TRUE    162  'to 162'
              160  <48>             
            162_0  COME_FROM           158  '158'
              162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          
              168  POP_EXCEPT       
              170  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 144

    submit.__doc__ = _base.Executor.submit.__doc__

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        """Returns an iterator equivalent to map(fn, iter).

        Args:
            fn: A callable that will take as many arguments as there are
                passed iterables.
            timeout: The maximum number of seconds to wait. If None, then there
                is no limit on the wait time.
            chunksize: If greater than one, the iterables will be chopped into
                chunks of size chunksize and submitted to the process pool.
                If set to one, the items in the list will be sent one at a time.

        Returns:
            An iterator equivalent to: map(func, *iterables) but the calls may
            be evaluated out-of-order.

        Raises:
            TimeoutError: If the entire result iterator could not be generated
                before the given timeout.
            Exception: If fn(*args) raises for any values.
        """
        if chunksize < 1:
            raise ValueError('chunksize must be >= 1.')
        results = super().map((partial(_process_chunk, fn)), _get_chunks(*iterables, **{'chunksize': chunksize}),
          timeout=timeout)
        return _chain_from_iterable_of_lists(results)

    def shutdown--- This code section failed: ---

 L. 732         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _shutdown_lock
                4  SETUP_WITH           54  'to 54'
                6  POP_TOP          

 L. 733         8  LOAD_FAST                'cancel_futures'
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _cancel_pending_futures

 L. 734        14  LOAD_CONST               True
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _shutdown_thread

 L. 735        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _executor_manager_thread_wakeup
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    40  'to 40'

 L. 737        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _executor_manager_thread_wakeup
               34  LOAD_METHOD              wakeup
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          
             40_0  COME_FROM            28  '28'
               40  POP_BLOCK        
               42  LOAD_CONST               None
               44  DUP_TOP          
               46  DUP_TOP          
               48  CALL_FUNCTION_3       3  ''
               50  POP_TOP          
               52  JUMP_FORWARD         70  'to 70'
             54_0  COME_FROM_WITH        4  '4'
               54  <49>             
               56  POP_JUMP_IF_TRUE     60  'to 60'
               58  <48>             
             60_0  COME_FROM            56  '56'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          
               66  POP_EXCEPT       
               68  POP_TOP          
             70_0  COME_FROM            52  '52'

 L. 739        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _executor_manager_thread
               74  LOAD_CONST               None
               76  <117>                 1  ''
               78  POP_JUMP_IF_FALSE    94  'to 94'
               80  LOAD_FAST                'wait'
               82  POP_JUMP_IF_FALSE    94  'to 94'

 L. 740        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _executor_manager_thread
               88  LOAD_METHOD              join
               90  CALL_METHOD_0         0  ''
               92  POP_TOP          
             94_0  COME_FROM            82  '82'
             94_1  COME_FROM            78  '78'

 L. 743        94  LOAD_CONST               None
               96  LOAD_FAST                'self'
               98  STORE_ATTR               _executor_manager_thread

 L. 744       100  LOAD_CONST               None
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _call_queue

 L. 745       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _result_queue
              110  LOAD_CONST               None
              112  <117>                 1  ''
              114  POP_JUMP_IF_FALSE   130  'to 130'
              116  LOAD_FAST                'wait'
              118  POP_JUMP_IF_FALSE   130  'to 130'

 L. 746       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _result_queue
              124  LOAD_METHOD              close
              126  CALL_METHOD_0         0  ''
              128  POP_TOP          
            130_0  COME_FROM           118  '118'
            130_1  COME_FROM           114  '114'

 L. 747       130  LOAD_CONST               None
              132  LOAD_FAST                'self'
              134  STORE_ATTR               _result_queue

 L. 748       136  LOAD_CONST               None
              138  LOAD_FAST                'self'
              140  STORE_ATTR               _processes

 L. 749       142  LOAD_CONST               None
              144  LOAD_FAST                'self'
              146  STORE_ATTR               _executor_manager_thread_wakeup

Parse error at or near `<117>' instruction at offset 26

    shutdown.__doc__ = _base.Executor.shutdown.__doc__


# global _system_limited ## Warning: Unused global
# global _system_limits_checked ## Warning: Unused global