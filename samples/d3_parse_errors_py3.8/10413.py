# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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
import atexit, os
from concurrent.futures import _base
import queue
from queue import Full
import multiprocessing as mp, multiprocessing.connection
from multiprocessing.queues import Queue
import threading, weakref
from functools import partial
import itertools, sys, traceback
_threads_wakeups = weakref.WeakKeyDictionary()
_global_shutdown = False

class _ThreadWakeup:

    def __init__(self):
        self._reader, self._writer = mp.Pipe(duplex=False)

    def close(self):
        self._writer.close()
        self._reader.close()

    def wakeup(self):
        self._writer.send_bytes(b'')

    def clear(self):
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

    def __init__(self, max_size=0, *, ctx, pending_work_items):
        self.pending_work_items = pending_work_items
        super().__init__(max_size, ctx=ctx)

    def _on_queue_feeder_error(self, e, obj):
        if isinstance(obj, _CallItem):
            tb = traceback.format_exception(type(e), e, e.__traceback__)
            e.__cause__ = _RemoteTraceback('\n"""\n{}"""'.format(''.join(tb)))
            work_item = self.pending_work_items.pop(obj.work_id, None)
            if work_item is not None:
                work_item.future.set_exception(e)
        else:
            super()._on_queue_feeder_error(e, obj)


def _get_chunks(*iterables, chunksize):
    """ Iterates over zip()ed iterables in chunks. """
    it = zip(*iterables)
    while True:
        chunk = tuple(itertools.islice(it, chunksize))
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


def _sendback_result(result_queue, work_id, result=None, exception=None):
    """Safely send back the given result or exception"""
    try:
        result_queue.put(_ResultItem(work_id, result=result, exception=exception))
    except BaseException as e:
        try:
            exc = _ExceptionWithTraceback(e, e.__traceback__)
            result_queue.put(_ResultItem(work_id, exception=exc))
        finally:
            e = None
            del e


def _process_worker--- This code section failed: ---

 L. 224         0  LOAD_FAST                'initializer'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    60  'to 60'

 L. 225         8  SETUP_FINALLY        22  'to 22'

 L. 226        10  LOAD_FAST                'initializer'
               12  LOAD_FAST                'initargs'
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  POP_TOP          
               18  POP_BLOCK        
               20  JUMP_FORWARD         60  'to 60'
             22_0  COME_FROM_FINALLY     8  '8'

 L. 227        22  DUP_TOP          
               24  LOAD_GLOBAL              BaseException
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    58  'to 58'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 228        36  LOAD_GLOBAL              _base
               38  LOAD_ATTR                LOGGER
               40  LOAD_ATTR                critical
               42  LOAD_STR                 'Exception in initializer:'
               44  LOAD_CONST               True
               46  LOAD_CONST               ('exc_info',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  POP_TOP          

 L. 231        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            28  '28'
               58  END_FINALLY      
             60_0  COME_FROM           202  '202'
             60_1  COME_FROM            20  '20'
             60_2  COME_FROM             6  '6'

 L. 233        60  LOAD_FAST                'call_queue'
               62  LOAD_ATTR                get
               64  LOAD_CONST               True
               66  LOAD_CONST               ('block',)
               68  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               70  STORE_FAST               'call_item'

 L. 234        72  LOAD_FAST                'call_item'
               74  LOAD_CONST               None
               76  COMPARE_OP               is
               78  POP_JUMP_IF_FALSE    98  'to 98'

 L. 236        80  LOAD_FAST                'result_queue'
               82  LOAD_METHOD              put
               84  LOAD_GLOBAL              os
               86  LOAD_METHOD              getpid
               88  CALL_METHOD_0         0  ''
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 237        94  LOAD_CONST               None
               96  RETURN_VALUE     
             98_0  COME_FROM            78  '78'

 L. 238        98  SETUP_FINALLY       120  'to 120'

 L. 239       100  LOAD_FAST                'call_item'
              102  LOAD_ATTR                fn
              104  LOAD_FAST                'call_item'
              106  LOAD_ATTR                args
              108  LOAD_FAST                'call_item'
              110  LOAD_ATTR                kwargs
              112  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              114  STORE_FAST               'r'
              116  POP_BLOCK        
              118  JUMP_FORWARD        182  'to 182'
            120_0  COME_FROM_FINALLY    98  '98'

 L. 240       120  DUP_TOP          
              122  LOAD_GLOBAL              BaseException
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   180  'to 180'
              128  POP_TOP          
              130  STORE_FAST               'e'
              132  POP_TOP          
              134  SETUP_FINALLY       168  'to 168'

 L. 241       136  LOAD_GLOBAL              _ExceptionWithTraceback
              138  LOAD_FAST                'e'
              140  LOAD_FAST                'e'
              142  LOAD_ATTR                __traceback__
              144  CALL_FUNCTION_2       2  ''
              146  STORE_FAST               'exc'

 L. 242       148  LOAD_GLOBAL              _sendback_result
              150  LOAD_FAST                'result_queue'
              152  LOAD_FAST                'call_item'
              154  LOAD_ATTR                work_id
              156  LOAD_FAST                'exc'
              158  LOAD_CONST               ('exception',)
              160  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              162  POP_TOP          
              164  POP_BLOCK        
              166  BEGIN_FINALLY    
            168_0  COME_FROM_FINALLY   134  '134'
              168  LOAD_CONST               None
              170  STORE_FAST               'e'
              172  DELETE_FAST              'e'
              174  END_FINALLY      
              176  POP_EXCEPT       
              178  JUMP_FORWARD        200  'to 200'
            180_0  COME_FROM           126  '126'
              180  END_FINALLY      
            182_0  COME_FROM           118  '118'

 L. 244       182  LOAD_GLOBAL              _sendback_result
              184  LOAD_FAST                'result_queue'
              186  LOAD_FAST                'call_item'
              188  LOAD_ATTR                work_id
              190  LOAD_FAST                'r'
              192  LOAD_CONST               ('result',)
              194  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              196  POP_TOP          

 L. 245       198  DELETE_FAST              'r'
            200_0  COME_FROM           178  '178'

 L. 249       200  DELETE_FAST              'call_item'
              202  JUMP_BACK            60  'to 60'

Parse error at or near `LOAD_CONST' instruction at offset 54


def _add_call_item_to_queue(pending_work_items, work_ids, call_queue):
    """Fills call_queue with _WorkItems from pending_work_items.

    This function never blocks.

    Args:
        pending_work_items: A dict mapping work ids to _WorkItems e.g.
            {5: <_WorkItem...>, 6: <_WorkItem...>, ...}
        work_ids: A queue.Queue of work ids e.g. Queue([5, 6, ...]). Work ids
            are consumed and the corresponding _WorkItems from
            pending_work_items are transformed into _CallItems and put in
            call_queue.
        call_queue: A multiprocessing.Queue that will be filled with _CallItems
            derived from _WorkItems.
    """
    while True:
        while True:
            if call_queue.full():
                return
            else:
                try:
                    work_id = work_ids.get(block=False)
                except queue.Empty:
                    return
                else:
                    work_item = pending_work_items[work_id]
                    if work_item.future.set_running_or_notify_cancel():
                        call_queue.put((_CallItem(work_id, work_item.fn, work_item.args, work_item.kwargs)),
                          block=True)

        del pending_work_items[work_id]
        continue


def _queue_management_worker--- This code section failed: ---

 L. 318         0  LOAD_CONST               None
                2  STORE_DEREF              'executor'

 L. 320         4  LOAD_CLOSURE             'executor'
                6  BUILD_TUPLE_1         1 
                8  LOAD_CODE                <code_object shutting_down>
               10  LOAD_STR                 '_queue_management_worker.<locals>.shutting_down'
               12  MAKE_FUNCTION_8          'closure'
               14  STORE_FAST               'shutting_down'

 L. 324        16  LOAD_CLOSURE             'call_queue'
               18  LOAD_CLOSURE             'processes'
               20  BUILD_TUPLE_2         2 
               22  LOAD_CODE                <code_object shutdown_worker>
               24  LOAD_STR                 '_queue_management_worker.<locals>.shutdown_worker'
               26  MAKE_FUNCTION_8          'closure'
               28  STORE_FAST               'shutdown_worker'

 L. 347        30  LOAD_FAST                'result_queue'
               32  LOAD_ATTR                _reader
               34  STORE_FAST               'result_reader'

 L. 348        36  LOAD_FAST                'thread_wakeup'
               38  LOAD_ATTR                _reader
               40  STORE_FAST               'wakeup_reader'

 L. 349        42  LOAD_FAST                'result_reader'
               44  LOAD_FAST                'wakeup_reader'
               46  BUILD_LIST_2          2 
               48  STORE_FAST               'readers'
             50_0  COME_FROM           580  '580'

 L. 352        50  LOAD_GLOBAL              _add_call_item_to_queue
               52  LOAD_FAST                'pending_work_items'

 L. 353        54  LOAD_FAST                'work_ids_queue'

 L. 354        56  LOAD_DEREF               'call_queue'

 L. 352        58  CALL_FUNCTION_3       3  ''
               60  POP_TOP          

 L. 361        62  LOAD_LISTCOMP            '<code_object <listcomp>>'
               64  LOAD_STR                 '_queue_management_worker.<locals>.<listcomp>'
               66  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               68  LOAD_DEREF               'processes'
               70  LOAD_METHOD              values
               72  CALL_METHOD_0         0  ''
               74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'worker_sentinels'

 L. 362        80  LOAD_GLOBAL              mp
               82  LOAD_ATTR                connection
               84  LOAD_METHOD              wait
               86  LOAD_FAST                'readers'
               88  LOAD_FAST                'worker_sentinels'
               90  BINARY_ADD       
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'ready'

 L. 364        96  LOAD_CONST               None
               98  STORE_FAST               'cause'

 L. 365       100  LOAD_CONST               True
              102  STORE_FAST               'is_broken'

 L. 366       104  LOAD_FAST                'result_reader'
              106  LOAD_FAST                'ready'
              108  COMPARE_OP               in
              110  POP_JUMP_IF_FALSE   186  'to 186'

 L. 367       112  SETUP_FINALLY       130  'to 130'

 L. 368       114  LOAD_FAST                'result_reader'
              116  LOAD_METHOD              recv
              118  CALL_METHOD_0         0  ''
              120  STORE_FAST               'result_item'

 L. 369       122  LOAD_CONST               False
              124  STORE_FAST               'is_broken'
              126  POP_BLOCK        
              128  JUMP_FORWARD        202  'to 202'
            130_0  COME_FROM_FINALLY   112  '112'

 L. 370       130  DUP_TOP          
              132  LOAD_GLOBAL              BaseException
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   182  'to 182'
              138  POP_TOP          
              140  STORE_FAST               'e'
              142  POP_TOP          
              144  SETUP_FINALLY       170  'to 170'

 L. 371       146  LOAD_GLOBAL              traceback
              148  LOAD_METHOD              format_exception
              150  LOAD_GLOBAL              type
              152  LOAD_FAST                'e'
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_FAST                'e'
              158  LOAD_FAST                'e'
              160  LOAD_ATTR                __traceback__
              162  CALL_METHOD_3         3  ''
              164  STORE_FAST               'cause'
              166  POP_BLOCK        
              168  BEGIN_FINALLY    
            170_0  COME_FROM_FINALLY   144  '144'
              170  LOAD_CONST               None
              172  STORE_FAST               'e'
              174  DELETE_FAST              'e'
              176  END_FINALLY      
              178  POP_EXCEPT       
              180  JUMP_FORWARD        202  'to 202'
            182_0  COME_FROM           136  '136'
              182  END_FINALLY      
              184  JUMP_FORWARD        202  'to 202'
            186_0  COME_FROM           110  '110'

 L. 373       186  LOAD_FAST                'wakeup_reader'
              188  LOAD_FAST                'ready'
              190  COMPARE_OP               in
              192  POP_JUMP_IF_FALSE   202  'to 202'

 L. 374       194  LOAD_CONST               False
              196  STORE_FAST               'is_broken'

 L. 375       198  LOAD_CONST               None
              200  STORE_FAST               'result_item'
            202_0  COME_FROM           192  '192'
            202_1  COME_FROM           184  '184'
            202_2  COME_FROM           180  '180'
            202_3  COME_FROM           128  '128'

 L. 376       202  LOAD_FAST                'thread_wakeup'
              204  LOAD_METHOD              clear
              206  CALL_METHOD_0         0  ''
              208  POP_TOP          

 L. 377       210  LOAD_FAST                'is_broken'
          212_214  POP_JUMP_IF_FALSE   364  'to 364'

 L. 379       216  LOAD_FAST                'executor_reference'
              218  CALL_FUNCTION_0       0  ''
              220  STORE_DEREF              'executor'

 L. 380       222  LOAD_DEREF               'executor'
              224  LOAD_CONST               None
              226  COMPARE_OP               is-not
              228  POP_JUMP_IF_FALSE   246  'to 246'

 L. 381       230  LOAD_STR                 'A child process terminated abruptly, the process pool is not usable anymore'
              232  LOAD_DEREF               'executor'
              234  STORE_ATTR               _broken

 L. 384       236  LOAD_CONST               True
              238  LOAD_DEREF               'executor'
              240  STORE_ATTR               _shutdown_thread

 L. 385       242  LOAD_CONST               None
              244  STORE_DEREF              'executor'
            246_0  COME_FROM           228  '228'

 L. 386       246  LOAD_GLOBAL              BrokenProcessPool
              248  LOAD_STR                 'A process in the process pool was terminated abruptly while the future was running or pending.'
              250  CALL_FUNCTION_1       1  ''
              252  STORE_FAST               'bpe'

 L. 389       254  LOAD_FAST                'cause'
              256  LOAD_CONST               None
              258  COMPARE_OP               is-not
          260_262  POP_JUMP_IF_FALSE   288  'to 288'

 L. 390       264  LOAD_GLOBAL              _RemoteTraceback

 L. 391       266  LOAD_STR                 "\n'''\n"
              268  LOAD_STR                 ''
              270  LOAD_METHOD              join
              272  LOAD_FAST                'cause'
              274  CALL_METHOD_1         1  ''
              276  FORMAT_VALUE          0  ''
              278  LOAD_STR                 "'''"
              280  BUILD_STRING_3        3 

 L. 390       282  CALL_FUNCTION_1       1  ''
              284  LOAD_FAST                'bpe'
              286  STORE_ATTR               __cause__
            288_0  COME_FROM           260  '260'

 L. 393       288  LOAD_FAST                'pending_work_items'
              290  LOAD_METHOD              items
              292  CALL_METHOD_0         0  ''
              294  GET_ITER         
            296_0  COME_FROM           318  '318'
              296  FOR_ITER            322  'to 322'
              298  UNPACK_SEQUENCE_2     2 
              300  STORE_FAST               'work_id'
              302  STORE_FAST               'work_item'

 L. 394       304  LOAD_FAST                'work_item'
              306  LOAD_ATTR                future
              308  LOAD_METHOD              set_exception
              310  LOAD_FAST                'bpe'
              312  CALL_METHOD_1         1  ''
              314  POP_TOP          

 L. 396       316  DELETE_FAST              'work_item'
          318_320  JUMP_BACK           296  'to 296'
            322_0  COME_FROM           296  '296'

 L. 397       322  LOAD_FAST                'pending_work_items'
              324  LOAD_METHOD              clear
              326  CALL_METHOD_0         0  ''
              328  POP_TOP          

 L. 400       330  LOAD_DEREF               'processes'
              332  LOAD_METHOD              values
              334  CALL_METHOD_0         0  ''
              336  GET_ITER         
            338_0  COME_FROM           350  '350'
              338  FOR_ITER            354  'to 354'
              340  STORE_FAST               'p'

 L. 401       342  LOAD_FAST                'p'
              344  LOAD_METHOD              terminate
              346  CALL_METHOD_0         0  ''
              348  POP_TOP          
          350_352  JUMP_BACK           338  'to 338'
            354_0  COME_FROM           338  '338'

 L. 402       354  LOAD_FAST                'shutdown_worker'
              356  CALL_FUNCTION_0       0  ''
              358  POP_TOP          

 L. 403       360  LOAD_CONST               None
              362  RETURN_VALUE     
            364_0  COME_FROM           212  '212'

 L. 404       364  LOAD_GLOBAL              isinstance
              366  LOAD_FAST                'result_item'
              368  LOAD_GLOBAL              int
              370  CALL_FUNCTION_2       2  ''
          372_374  POP_JUMP_IF_FALSE   424  'to 424'

 L. 407       376  LOAD_FAST                'shutting_down'
              378  CALL_FUNCTION_0       0  ''
          380_382  POP_JUMP_IF_TRUE    388  'to 388'
              384  LOAD_ASSERT              AssertionError
              386  RAISE_VARARGS_1       1  'exception instance'
            388_0  COME_FROM           380  '380'

 L. 408       388  LOAD_DEREF               'processes'
              390  LOAD_METHOD              pop
              392  LOAD_FAST                'result_item'
              394  CALL_METHOD_1         1  ''
              396  STORE_FAST               'p'

 L. 409       398  LOAD_FAST                'p'
              400  LOAD_METHOD              join
              402  CALL_METHOD_0         0  ''
              404  POP_TOP          

 L. 410       406  LOAD_DEREF               'processes'
          408_410  POP_JUMP_IF_TRUE    500  'to 500'

 L. 411       412  LOAD_FAST                'shutdown_worker'
              414  CALL_FUNCTION_0       0  ''
              416  POP_TOP          

 L. 412       418  LOAD_CONST               None
              420  RETURN_VALUE     
              422  JUMP_FORWARD        500  'to 500'
            424_0  COME_FROM           372  '372'

 L. 413       424  LOAD_FAST                'result_item'
              426  LOAD_CONST               None
              428  COMPARE_OP               is-not
          430_432  POP_JUMP_IF_FALSE   500  'to 500'

 L. 414       434  LOAD_FAST                'pending_work_items'
              436  LOAD_METHOD              pop
              438  LOAD_FAST                'result_item'
              440  LOAD_ATTR                work_id
              442  LOAD_CONST               None
              444  CALL_METHOD_2         2  ''
              446  STORE_FAST               'work_item'

 L. 416       448  LOAD_FAST                'work_item'
              450  LOAD_CONST               None
              452  COMPARE_OP               is-not
          454_456  POP_JUMP_IF_FALSE   498  'to 498'

 L. 417       458  LOAD_FAST                'result_item'
              460  LOAD_ATTR                exception
          462_464  POP_JUMP_IF_FALSE   482  'to 482'

 L. 418       466  LOAD_FAST                'work_item'
              468  LOAD_ATTR                future
              470  LOAD_METHOD              set_exception
              472  LOAD_FAST                'result_item'
              474  LOAD_ATTR                exception
              476  CALL_METHOD_1         1  ''
              478  POP_TOP          
              480  JUMP_FORWARD        496  'to 496'
            482_0  COME_FROM           462  '462'

 L. 420       482  LOAD_FAST                'work_item'
              484  LOAD_ATTR                future
              486  LOAD_METHOD              set_result
              488  LOAD_FAST                'result_item'
              490  LOAD_ATTR                result
              492  CALL_METHOD_1         1  ''
              494  POP_TOP          
            496_0  COME_FROM           480  '480'

 L. 422       496  DELETE_FAST              'work_item'
            498_0  COME_FROM           454  '454'

 L. 424       498  DELETE_FAST              'result_item'
            500_0  COME_FROM           430  '430'
            500_1  COME_FROM           422  '422'
            500_2  COME_FROM           408  '408'

 L. 427       500  LOAD_FAST                'executor_reference'
              502  CALL_FUNCTION_0       0  ''
              504  STORE_DEREF              'executor'

 L. 432       506  LOAD_FAST                'shutting_down'
              508  CALL_FUNCTION_0       0  ''
          510_512  POP_JUMP_IF_FALSE   576  'to 576'

 L. 433       514  SETUP_FINALLY       554  'to 554'

 L. 436       516  LOAD_DEREF               'executor'
              518  LOAD_CONST               None
              520  COMPARE_OP               is-not
          522_524  POP_JUMP_IF_FALSE   532  'to 532'

 L. 437       526  LOAD_CONST               True
              528  LOAD_DEREF               'executor'
              530  STORE_ATTR               _shutdown_thread
            532_0  COME_FROM           522  '522'

 L. 440       532  LOAD_FAST                'pending_work_items'
          534_536  POP_JUMP_IF_TRUE    550  'to 550'

 L. 441       538  LOAD_FAST                'shutdown_worker'
              540  CALL_FUNCTION_0       0  ''
              542  POP_TOP          

 L. 442       544  POP_BLOCK        
              546  LOAD_CONST               None
              548  RETURN_VALUE     
            550_0  COME_FROM           534  '534'
              550  POP_BLOCK        
              552  JUMP_FORWARD        576  'to 576'
            554_0  COME_FROM_FINALLY   514  '514'

 L. 443       554  DUP_TOP          
              556  LOAD_GLOBAL              Full
              558  COMPARE_OP               exception-match
          560_562  POP_JUMP_IF_FALSE   574  'to 574'
              564  POP_TOP          
              566  POP_TOP          
              568  POP_TOP          

 L. 446       570  POP_EXCEPT       
              572  BREAK_LOOP          576  'to 576'
            574_0  COME_FROM           560  '560'
              574  END_FINALLY      
            576_0  COME_FROM           572  '572'
            576_1  COME_FROM           552  '552'
            576_2  COME_FROM           510  '510'

 L. 447       576  LOAD_CONST               None
              578  STORE_DEREF              'executor'
              580  JUMP_BACK            50  'to 50'

Parse error at or near `COME_FROM' instruction at offset 550_0


_system_limits_checked = False
_system_limited = None

def _check_system_limits():
    global _system_limited
    global _system_limits_checked
    if _system_limits_checked:
        if _system_limited:
            raise NotImplementedError(_system_limited)
    _system_limits_checked = True
    try:
        nsems_max = os.sysconf('SC_SEM_NSEMS_MAX')
    except (AttributeError, ValueError):
        return
    else:
        if nsems_max == -1:
            return
        if nsems_max >= 256:
            return
        _system_limited = 'system provides too few semaphores (%d available, 256 necessary)' % nsems_max
        raise NotImplementedError(_system_limited)


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

    def __init__(self, max_workers=None, mp_context=None, initializer=None, initargs=()):
        """Initializes a new ProcessPoolExecutor instance.

        Args:
            max_workers: The maximum number of processes that can be used to
                execute the given calls. If None or not given then as many
                worker processes will be created as the machine has processors.
            mp_context: A multiprocessing context to launch the workers. This
                object should provide SimpleQueue, Queue and Process.
            initializer: A callable used to initialize worker processes.
            initargs: A tuple of arguments to pass to the initializer.
        """
        _check_system_limits()
        if max_workers is None:
            self._max_workers = os.cpu_count() or 1
            if sys.platform == 'win32':
                self._max_workers = min(_MAX_WINDOWS_WORKERS, self._max_workers)
        else:
            if max_workers <= 0:
                raise ValueError('max_workers must be greater than 0')
            elif sys.platform == 'win32':
                if max_workers > _MAX_WINDOWS_WORKERS:
                    raise ValueError(f"max_workers must be <= {_MAX_WINDOWS_WORKERS}")
            self._max_workers = max_workers
        if mp_context is None:
            mp_context = mp.get_context()
        self._mp_context = mp_context
        if initializer is not None:
            if not callable(initializer):
                raise TypeError('initializer must be a callable')
        self._initializer = initializer
        self._initargs = initargs
        self._queue_management_thread = None
        self._processes = {}
        self._shutdown_thread = False
        self._shutdown_lock = threading.Lock()
        self._broken = False
        self._queue_count = 0
        self._pending_work_items = {}
        queue_size = self._max_workers + EXTRA_QUEUED_CALLS
        self._call_queue = _SafeQueue(max_size=queue_size,
          ctx=(self._mp_context),
          pending_work_items=(self._pending_work_items))
        self._call_queue._ignore_epipe = True
        self._result_queue = mp_context.SimpleQueue()
        self._work_ids = queue.Queue()
        self._queue_management_thread_wakeup = _ThreadWakeup()

    def _start_queue_management_thread(self):
        if self._queue_management_thread is None:

            def weakref_cb(_, thread_wakeup=self._queue_management_thread_wakeup):
                mp.util.debug('Executor collected: triggering callback for QueueManager wakeup')
                thread_wakeup.wakeup()

            self._adjust_process_count()
            self._queue_management_thread = threading.Thread(target=_queue_management_worker,
              args=(
             weakref.ref(self, weakref_cb),
             self._processes,
             self._pending_work_items,
             self._work_ids,
             self._call_queue,
             self._result_queue,
             self._queue_management_thread_wakeup),
              name='QueueManagerThread')
            self._queue_management_thread.daemon = True
            self._queue_management_thread.start()
            _threads_wakeups[self._queue_management_thread] = self._queue_management_thread_wakeup

    def _adjust_process_count(self):
        for _ in range(len(self._processes), self._max_workers):
            p = self._mp_context.Process(target=_process_worker,
              args=(
             self._call_queue,
             self._result_queue,
             self._initializer,
             self._initargs))
            p.start()
            self._processes[p.pid] = p

    def submit(*args, **kwargs):
        if len(args) >= 2:
            self, fn, *args = args
        elif not args:
            raise TypeError("descriptor 'submit' of 'ProcessPoolExecutor' object needs an argument")
        elif 'fn' in kwargs:
            fn = kwargs.pop('fn')
            self, *args = args
            import warnings
            warnings.warn("Passing 'fn' as keyword argument is deprecated", DeprecationWarning,
              stacklevel=2)
        else:
            raise TypeError('submit expected at least 1 positional argument, got %d' % (len(args) - 1))
        with self._shutdown_lock:
            if self._broken:
                raise BrokenProcessPool(self._broken)
            if self._shutdown_thread:
                raise RuntimeError('cannot schedule new futures after shutdown')
            if _global_shutdown:
                raise RuntimeError('cannot schedule new futures after interpreter shutdown')
            f = _base.Future()
            w = _WorkItem(f, fn, args, kwargs)
            self._pending_work_items[self._queue_count] = w
            self._work_ids.put(self._queue_count)
            self._queue_count += 1
            self._queue_management_thread_wakeup.wakeup()
            self._start_queue_management_thread()
            return f

    submit.__text_signature__ = _base.Executor.submit.__text_signature__
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

    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown_thread = True
        if self._queue_management_thread:
            self._queue_management_thread_wakeup.wakeup()
            if wait:
                self._queue_management_thread.join()
        self._queue_management_thread = None
        if self._call_queue is not None:
            self._call_queue.close()
            if wait:
                self._call_queue.join_thread()
            self._call_queue = None
        self._result_queue = None
        self._processes = None
        if self._queue_management_thread_wakeup:
            self._queue_management_thread_wakeup.close()
            self._queue_management_thread_wakeup = None

    shutdown.__doc__ = _base.Executor.shutdown.__doc__


atexit.register(_python_exit)