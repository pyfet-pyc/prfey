# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: concurrent\futures\thread.py
"""Implements ThreadPoolExecutor."""
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
from concurrent.futures import _base
import itertools, queue, threading, types, weakref, os
_threads_queues = weakref.WeakKeyDictionary()
_shutdown = False
_global_shutdown_lock = threading.Lock()

def _python_exit--- This code section failed: ---

 L.  25         0  LOAD_GLOBAL              _global_shutdown_lock
                2  SETUP_WITH           24  'to 24'
                4  POP_TOP          

 L.  26         6  LOAD_CONST               True
                8  STORE_GLOBAL             _shutdown
               10  POP_BLOCK        
               12  LOAD_CONST               None
               14  DUP_TOP          
               16  DUP_TOP          
               18  CALL_FUNCTION_3       3  ''
               20  POP_TOP          
               22  JUMP_FORWARD         40  'to 40'
             24_0  COME_FROM_WITH        2  '2'
               24  <49>             
               26  POP_JUMP_IF_TRUE     30  'to 30'
               28  <48>             
             30_0  COME_FROM            26  '26'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          
               36  POP_EXCEPT       
               38  POP_TOP          
             40_0  COME_FROM            22  '22'

 L.  27        40  LOAD_GLOBAL              list
               42  LOAD_GLOBAL              _threads_queues
               44  LOAD_METHOD              items
               46  CALL_METHOD_0         0  ''
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'items'

 L.  28        52  LOAD_FAST                'items'
               54  GET_ITER         
             56_0  COME_FROM            74  '74'
               56  FOR_ITER             76  'to 76'
               58  UNPACK_SEQUENCE_2     2 
               60  STORE_FAST               't'
               62  STORE_FAST               'q'

 L.  29        64  LOAD_FAST                'q'
               66  LOAD_METHOD              put
               68  LOAD_CONST               None
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  JUMP_BACK            56  'to 56'
             76_0  COME_FROM            56  '56'

 L.  30        76  LOAD_FAST                'items'
               78  GET_ITER         
             80_0  COME_FROM            96  '96'
               80  FOR_ITER             98  'to 98'
               82  UNPACK_SEQUENCE_2     2 
               84  STORE_FAST               't'
               86  STORE_FAST               'q'

 L.  31        88  LOAD_FAST                't'
               90  LOAD_METHOD              join
               92  CALL_METHOD_0         0  ''
               94  POP_TOP          
               96  JUMP_BACK            80  'to 80'
             98_0  COME_FROM            80  '80'

Parse error at or near `DUP_TOP' instruction at offset 14


threading._register_atexit(_python_exit)

class _WorkItem(object):

    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run--- This code section failed: ---

 L.  48         0  LOAD_FAST                'self'
                2  LOAD_ATTR                future
                4  LOAD_METHOD              set_running_or_notify_cancel
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L.  49        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  51        14  SETUP_FINALLY        40  'to 40'

 L.  52        16  LOAD_FAST                'self'
               18  LOAD_ATTR                fn
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                args
               24  BUILD_MAP_0           0 
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                kwargs
               30  <164>                 1  ''
               32  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               34  STORE_FAST               'result'
               36  POP_BLOCK        
               38  JUMP_FORWARD         92  'to 92'
             40_0  COME_FROM_FINALLY    14  '14'

 L.  53        40  DUP_TOP          
               42  LOAD_GLOBAL              BaseException
               44  <121>                90  ''
               46  POP_TOP          
               48  STORE_FAST               'exc'
               50  POP_TOP          
               52  SETUP_FINALLY        82  'to 82'

 L.  54        54  LOAD_FAST                'self'
               56  LOAD_ATTR                future
               58  LOAD_METHOD              set_exception
               60  LOAD_FAST                'exc'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L.  56        66  LOAD_CONST               None
               68  STORE_FAST               'self'
               70  POP_BLOCK        
               72  POP_EXCEPT       
               74  LOAD_CONST               None
               76  STORE_FAST               'exc'
               78  DELETE_FAST              'exc'
               80  JUMP_FORWARD        104  'to 104'
             82_0  COME_FROM_FINALLY    52  '52'
               82  LOAD_CONST               None
               84  STORE_FAST               'exc'
               86  DELETE_FAST              'exc'
               88  <48>             
               90  <48>             
             92_0  COME_FROM            38  '38'

 L.  58        92  LOAD_FAST                'self'
               94  LOAD_ATTR                future
               96  LOAD_METHOD              set_result
               98  LOAD_FAST                'result'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
            104_0  COME_FROM            80  '80'

Parse error at or near `<164>' instruction at offset 30

    __class_getitem__ = classmethod(types.GenericAlias)


def _worker--- This code section failed: ---

 L.  64         0  LOAD_FAST                'initializer'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    80  'to 80'

 L.  65         8  SETUP_FINALLY        22  'to 22'

 L.  66        10  LOAD_FAST                'initializer'
               12  LOAD_FAST                'initargs'
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  POP_TOP          
               18  POP_BLOCK        
               20  JUMP_FORWARD         80  'to 80'
             22_0  COME_FROM_FINALLY     8  '8'

 L.  67        22  DUP_TOP          
               24  LOAD_GLOBAL              BaseException
               26  <121>                78  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  68        34  LOAD_GLOBAL              _base
               36  LOAD_ATTR                LOGGER
               38  LOAD_ATTR                critical
               40  LOAD_STR                 'Exception in initializer:'
               42  LOAD_CONST               True
               44  LOAD_CONST               ('exc_info',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  POP_TOP          

 L.  69        50  LOAD_FAST                'executor_reference'
               52  CALL_FUNCTION_0       0  ''
               54  STORE_FAST               'executor'

 L.  70        56  LOAD_FAST                'executor'
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L.  71        64  LOAD_FAST                'executor'
               66  LOAD_METHOD              _initializer_failed
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          
             72_0  COME_FROM            62  '62'

 L.  72        72  POP_EXCEPT       
               74  LOAD_CONST               None
               76  RETURN_VALUE     
               78  <48>             
             80_0  COME_FROM            20  '20'
             80_1  COME_FROM             6  '6'

 L.  73        80  SETUP_FINALLY       202  'to 202'
             82_0  COME_FROM           196  '196'
             82_1  COME_FROM           138  '138'

 L.  75        82  LOAD_FAST                'work_queue'
               84  LOAD_ATTR                get
               86  LOAD_CONST               True
               88  LOAD_CONST               ('block',)
               90  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               92  STORE_FAST               'work_item'

 L.  76        94  LOAD_FAST                'work_item'
               96  LOAD_CONST               None
               98  <117>                 1  ''
              100  POP_JUMP_IF_FALSE   140  'to 140'

 L.  77       102  LOAD_FAST                'work_item'
              104  LOAD_METHOD              run
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          

 L.  79       110  DELETE_FAST              'work_item'

 L.  82       112  LOAD_FAST                'executor_reference'
              114  CALL_FUNCTION_0       0  ''
              116  STORE_FAST               'executor'

 L.  83       118  LOAD_FAST                'executor'
              120  LOAD_CONST               None
              122  <117>                 1  ''
              124  POP_JUMP_IF_FALSE   136  'to 136'

 L.  84       126  LOAD_FAST                'executor'
              128  LOAD_ATTR                _idle_semaphore
              130  LOAD_METHOD              release
              132  CALL_METHOD_0         0  ''
              134  POP_TOP          
            136_0  COME_FROM           124  '124'

 L.  85       136  DELETE_FAST              'executor'

 L.  86       138  JUMP_BACK            82  'to 82'
            140_0  COME_FROM           100  '100'

 L.  88       140  LOAD_FAST                'executor_reference'
              142  CALL_FUNCTION_0       0  ''
              144  STORE_FAST               'executor'

 L.  93       146  LOAD_GLOBAL              _shutdown
              148  POP_JUMP_IF_TRUE    164  'to 164'
              150  LOAD_FAST                'executor'
              152  LOAD_CONST               None
              154  <117>                 0  ''
              156  POP_JUMP_IF_TRUE    164  'to 164'
              158  LOAD_FAST                'executor'
              160  LOAD_ATTR                _shutdown
              162  POP_JUMP_IF_FALSE   194  'to 194'
            164_0  COME_FROM           156  '156'
            164_1  COME_FROM           148  '148'

 L.  96       164  LOAD_FAST                'executor'
              166  LOAD_CONST               None
              168  <117>                 1  ''
              170  POP_JUMP_IF_FALSE   178  'to 178'

 L.  97       172  LOAD_CONST               True
              174  LOAD_FAST                'executor'
              176  STORE_ATTR               _shutdown
            178_0  COME_FROM           170  '170'

 L.  99       178  LOAD_FAST                'work_queue'
              180  LOAD_METHOD              put
              182  LOAD_CONST               None
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 100       188  POP_BLOCK        
              190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           162  '162'

 L. 101       194  DELETE_FAST              'executor'
              196  JUMP_BACK            82  'to 82'
              198  POP_BLOCK        
              200  JUMP_FORWARD        236  'to 236'
            202_0  COME_FROM_FINALLY    80  '80'

 L. 102       202  DUP_TOP          
              204  LOAD_GLOBAL              BaseException
              206  <121>               234  ''
              208  POP_TOP          
              210  POP_TOP          
              212  POP_TOP          

 L. 103       214  LOAD_GLOBAL              _base
              216  LOAD_ATTR                LOGGER
              218  LOAD_ATTR                critical
              220  LOAD_STR                 'Exception in worker'
              222  LOAD_CONST               True
              224  LOAD_CONST               ('exc_info',)
              226  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              228  POP_TOP          
              230  POP_EXCEPT       
              232  JUMP_FORWARD        236  'to 236'
              234  <48>             
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           200  '200'

Parse error at or near `None' instruction at offset -1


class BrokenThreadPool(_base.BrokenExecutor):
    __doc__ = '\n    Raised when a worker thread in a ThreadPoolExecutor failed initializing.\n    '


class ThreadPoolExecutor(_base.Executor):
    _counter = itertools.count().__next__

    def __init__--- This code section failed: ---

 L. 128         0  LOAD_FAST                'max_workers'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    30  'to 30'

 L. 136         8  LOAD_GLOBAL              min
               10  LOAD_CONST               32
               12  LOAD_GLOBAL              os
               14  LOAD_METHOD              cpu_count
               16  CALL_METHOD_0         0  ''
               18  JUMP_IF_TRUE_OR_POP    22  'to 22'
               20  LOAD_CONST               1
             22_0  COME_FROM            18  '18'
               22  LOAD_CONST               4
               24  BINARY_ADD       
               26  CALL_FUNCTION_2       2  ''
               28  STORE_FAST               'max_workers'
             30_0  COME_FROM             6  '6'

 L. 137        30  LOAD_FAST                'max_workers'
               32  LOAD_CONST               0
               34  COMPARE_OP               <=
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 138        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'max_workers must be greater than 0'
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L. 140        46  LOAD_FAST                'initializer'
               48  LOAD_CONST               None
               50  <117>                 1  ''
               52  POP_JUMP_IF_FALSE    70  'to 70'
               54  LOAD_GLOBAL              callable
               56  LOAD_FAST                'initializer'
               58  CALL_FUNCTION_1       1  ''
               60  POP_JUMP_IF_TRUE     70  'to 70'

 L. 141        62  LOAD_GLOBAL              TypeError
               64  LOAD_STR                 'initializer must be a callable'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            60  '60'
             70_1  COME_FROM            52  '52'

 L. 143        70  LOAD_FAST                'max_workers'
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _max_workers

 L. 144        76  LOAD_GLOBAL              queue
               78  LOAD_METHOD              SimpleQueue
               80  CALL_METHOD_0         0  ''
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _work_queue

 L. 145        86  LOAD_GLOBAL              threading
               88  LOAD_METHOD              Semaphore
               90  LOAD_CONST               0
               92  CALL_METHOD_1         1  ''
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _idle_semaphore

 L. 146        98  LOAD_GLOBAL              set
              100  CALL_FUNCTION_0       0  ''
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _threads

 L. 147       106  LOAD_CONST               False
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _broken

 L. 148       112  LOAD_CONST               False
              114  LOAD_FAST                'self'
              116  STORE_ATTR               _shutdown

 L. 149       118  LOAD_GLOBAL              threading
              120  LOAD_METHOD              Lock
              122  CALL_METHOD_0         0  ''
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _shutdown_lock

 L. 150       128  LOAD_FAST                'thread_name_prefix'
              130  JUMP_IF_TRUE_OR_POP   142  'to 142'

 L. 151       132  LOAD_STR                 'ThreadPoolExecutor-%d'
              134  LOAD_FAST                'self'
              136  LOAD_METHOD              _counter
              138  CALL_METHOD_0         0  ''
              140  BINARY_MODULO    
            142_0  COME_FROM           130  '130'

 L. 150       142  LOAD_FAST                'self'
              144  STORE_ATTR               _thread_name_prefix

 L. 152       146  LOAD_FAST                'initializer'
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _initializer

 L. 153       152  LOAD_FAST                'initargs'
              154  LOAD_FAST                'self'
              156  STORE_ATTR               _initargs

Parse error at or near `None' instruction at offset -1

    def submit--- This code section failed: ---

 L. 156         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _shutdown_lock
                4  SETUP_WITH          160  'to 160'
                6  POP_TOP          
                8  LOAD_GLOBAL              _global_shutdown_lock
               10  SETUP_WITH          130  'to 130'
               12  POP_TOP          

 L. 157        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _broken
               18  POP_JUMP_IF_FALSE    30  'to 30'

 L. 158        20  LOAD_GLOBAL              BrokenThreadPool
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _broken
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            18  '18'

 L. 160        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _shutdown
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 161        36  LOAD_GLOBAL              RuntimeError
               38  LOAD_STR                 'cannot schedule new futures after shutdown'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L. 162        44  LOAD_GLOBAL              _shutdown
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 163        48  LOAD_GLOBAL              RuntimeError
               50  LOAD_STR                 'cannot schedule new futures after interpreter shutdown'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L. 166        56  LOAD_GLOBAL              _base
               58  LOAD_METHOD              Future
               60  CALL_METHOD_0         0  ''
               62  STORE_FAST               'f'

 L. 167        64  LOAD_GLOBAL              _WorkItem
               66  LOAD_FAST                'f'
               68  LOAD_FAST                'fn'
               70  LOAD_FAST                'args'
               72  LOAD_FAST                'kwargs'
               74  CALL_FUNCTION_4       4  ''
               76  STORE_FAST               'w'

 L. 169        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _work_queue
               82  LOAD_METHOD              put
               84  LOAD_FAST                'w'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L. 170        90  LOAD_FAST                'self'
               92  LOAD_METHOD              _adjust_thread_count
               94  CALL_METHOD_0         0  ''
               96  POP_TOP          

 L. 171        98  LOAD_FAST                'f'
              100  POP_BLOCK        
              102  ROT_TWO          
              104  LOAD_CONST               None
              106  DUP_TOP          
              108  DUP_TOP          
              110  CALL_FUNCTION_3       3  ''
              112  POP_TOP          
              114  POP_BLOCK        
              116  ROT_TWO          
              118  LOAD_CONST               None
              120  DUP_TOP          
              122  DUP_TOP          
              124  CALL_FUNCTION_3       3  ''
              126  POP_TOP          
              128  RETURN_VALUE     
            130_0  COME_FROM_WITH       10  '10'
              130  <49>             
              132  POP_JUMP_IF_TRUE    136  'to 136'
              134  <48>             
            136_0  COME_FROM           132  '132'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          
              142  POP_EXCEPT       
              144  POP_TOP          
              146  POP_BLOCK        
              148  LOAD_CONST               None
              150  DUP_TOP          
              152  DUP_TOP          
              154  CALL_FUNCTION_3       3  ''
              156  POP_TOP          
              158  JUMP_FORWARD        176  'to 176'
            160_0  COME_FROM_WITH        4  '4'
              160  <49>             
              162  POP_JUMP_IF_TRUE    166  'to 166'
              164  <48>             
            166_0  COME_FROM           162  '162'
              166  POP_TOP          
              168  POP_TOP          
              170  POP_TOP          
              172  POP_EXCEPT       
              174  POP_TOP          
            176_0  COME_FROM           158  '158'

Parse error at or near `LOAD_CONST' instruction at offset 104

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
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue

    def _initializer_failed--- This code section failed: ---

 L. 198         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _shutdown_lock
                4  SETUP_WITH           96  'to 96'
                6  POP_TOP          

 L. 199         8  LOAD_STR                 'A thread initializer failed, the thread pool is not usable anymore'
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _broken
             14_0  COME_FROM            80  '80'
             14_1  COME_FROM            60  '60'

 L. 203        14  SETUP_FINALLY        30  'to 30'

 L. 204        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _work_queue
               20  LOAD_METHOD              get_nowait
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'work_item'
               26  POP_BLOCK        
               28  JUMP_FORWARD         54  'to 54'
             30_0  COME_FROM_FINALLY    14  '14'

 L. 205        30  DUP_TOP          
               32  LOAD_GLOBAL              queue
               34  LOAD_ATTR                Empty
               36  <121>                52  ''
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 206        44  POP_EXCEPT       
               46  BREAK_LOOP           82  'to 82'
               48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
               52  <48>             
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM            28  '28'

 L. 207        54  LOAD_FAST                'work_item'
               56  LOAD_CONST               None
               58  <117>                 1  ''
               60  POP_JUMP_IF_FALSE_BACK    14  'to 14'

 L. 208        62  LOAD_FAST                'work_item'
               64  LOAD_ATTR                future
               66  LOAD_METHOD              set_exception
               68  LOAD_GLOBAL              BrokenThreadPool
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _broken
               74  CALL_FUNCTION_1       1  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  JUMP_BACK            14  'to 14'
             82_0  COME_FROM            46  '46'
               82  POP_BLOCK        
               84  LOAD_CONST               None
               86  DUP_TOP          
               88  DUP_TOP          
               90  CALL_FUNCTION_3       3  ''
               92  POP_TOP          
               94  JUMP_FORWARD        112  'to 112'
             96_0  COME_FROM_WITH        4  '4'
               96  <49>             
               98  POP_JUMP_IF_TRUE    102  'to 102'
              100  <48>             
            102_0  COME_FROM            98  '98'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          
              108  POP_EXCEPT       
              110  POP_TOP          
            112_0  COME_FROM            94  '94'

Parse error at or near `<121>' instruction at offset 36

    def shutdown--- This code section failed: ---

 L. 211         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _shutdown_lock
                4  SETUP_WITH          104  'to 104'
                6  POP_TOP          

 L. 212         8  LOAD_CONST               True
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _shutdown

 L. 213        14  LOAD_FAST                'cancel_futures'
               16  POP_JUMP_IF_FALSE    78  'to 78'
             18_0  COME_FROM            76  '76'
             18_1  COME_FROM            64  '64'

 L. 217        18  SETUP_FINALLY        34  'to 34'

 L. 218        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _work_queue
               24  LOAD_METHOD              get_nowait
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'work_item'
               30  POP_BLOCK        
               32  JUMP_FORWARD         58  'to 58'
             34_0  COME_FROM_FINALLY    18  '18'

 L. 219        34  DUP_TOP          
               36  LOAD_GLOBAL              queue
               38  LOAD_ATTR                Empty
               40  <121>                56  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 220        48  POP_EXCEPT       
               50  BREAK_LOOP           78  'to 78'
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            32  '32'

 L. 221        58  LOAD_FAST                'work_item'
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L. 222        66  LOAD_FAST                'work_item'
               68  LOAD_ATTR                future
               70  LOAD_METHOD              cancel
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          
               76  JUMP_BACK            18  'to 18'
             78_0  COME_FROM            50  '50'
             78_1  COME_FROM            16  '16'

 L. 226        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _work_queue
               82  LOAD_METHOD              put
               84  LOAD_CONST               None
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
               90  POP_BLOCK        
               92  LOAD_CONST               None
               94  DUP_TOP          
               96  DUP_TOP          
               98  CALL_FUNCTION_3       3  ''
              100  POP_TOP          
              102  JUMP_FORWARD        120  'to 120'
            104_0  COME_FROM_WITH        4  '4'
              104  <49>             
              106  POP_JUMP_IF_TRUE    110  'to 110'
              108  <48>             
            110_0  COME_FROM           106  '106'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          
              116  POP_EXCEPT       
              118  POP_TOP          
            120_0  COME_FROM           102  '102'

 L. 227       120  LOAD_FAST                'wait'
              122  POP_JUMP_IF_FALSE   144  'to 144'

 L. 228       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _threads
              128  GET_ITER         
            130_0  COME_FROM           142  '142'
              130  FOR_ITER            144  'to 144'
              132  STORE_FAST               't'

 L. 229       134  LOAD_FAST                't'
              136  LOAD_METHOD              join
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          
              142  JUMP_BACK           130  'to 130'
            144_0  COME_FROM           130  '130'
            144_1  COME_FROM           122  '122'

Parse error at or near `<121>' instruction at offset 40

    shutdown.__doc__ = _base.Executor.shutdown.__doc__


# global _shutdown ## Warning: Unused global