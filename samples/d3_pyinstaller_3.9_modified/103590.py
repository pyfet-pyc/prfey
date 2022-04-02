# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multiprocessing\pool.py
__all__ = [
 'Pool', 'ThreadPool']
import collections, itertools, os, queue, threading, time, traceback, types, warnings
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
        return (
         rebuild_exc, (self.exc, self.tb))


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
                4  <117>                 1  ''
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
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 109        90  LOAD_FAST                'initializer'
               92  LOAD_FAST                'initargs'
               94  CALL_FUNCTION_EX      0  'positional arguments only'
               96  POP_TOP          
             98_0  COME_FROM            88  '88'

 L. 111        98  LOAD_CONST               0
              100  STORE_FAST               'completed'
            102_0  COME_FROM           446  '446'

 L. 112       102  LOAD_FAST                'maxtasks'
              104  LOAD_CONST               None
              106  <117>                 0  ''
              108  POP_JUMP_IF_TRUE    126  'to 126'
              110  LOAD_FAST                'maxtasks'
          112_114  POP_JUMP_IF_FALSE   448  'to 448'
              116  LOAD_FAST                'completed'
              118  LOAD_FAST                'maxtasks'
              120  COMPARE_OP               <
          122_124  POP_JUMP_IF_FALSE   448  'to 448'
            126_0  COME_FROM           108  '108'

 L. 113       126  SETUP_FINALLY       138  'to 138'

 L. 114       128  LOAD_FAST                'get'
              130  CALL_FUNCTION_0       0  ''
              132  STORE_FAST               'task'
              134  POP_BLOCK        
              136  JUMP_FORWARD        176  'to 176'
            138_0  COME_FROM_FINALLY   126  '126'

 L. 115       138  DUP_TOP          
              140  LOAD_GLOBAL              EOFError
              142  LOAD_GLOBAL              OSError
              144  BUILD_TUPLE_2         2 
              146  <121>               174  ''
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L. 116       154  LOAD_GLOBAL              util
              156  LOAD_METHOD              debug
              158  LOAD_STR                 'worker got EOFError or OSError -- exiting'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          

 L. 117       164  POP_EXCEPT       
          166_168  BREAK_LOOP          448  'to 448'
              170  POP_EXCEPT       
              172  JUMP_FORWARD        176  'to 176'
              174  <48>             
            176_0  COME_FROM           172  '172'
            176_1  COME_FROM           136  '136'

 L. 119       176  LOAD_FAST                'task'
              178  LOAD_CONST               None
              180  <117>                 0  ''
              182  POP_JUMP_IF_FALSE   198  'to 198'

 L. 120       184  LOAD_GLOBAL              util
              186  LOAD_METHOD              debug
              188  LOAD_STR                 'worker got sentinel -- exiting'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          

 L. 121   194_196  JUMP_FORWARD        448  'to 448'
            198_0  COME_FROM           182  '182'

 L. 123       198  LOAD_FAST                'task'
              200  UNPACK_SEQUENCE_5     5 
              202  STORE_FAST               'job'
              204  STORE_FAST               'i'
              206  STORE_FAST               'func'
              208  STORE_FAST               'args'
              210  STORE_FAST               'kwds'

 L. 124       212  SETUP_FINALLY       236  'to 236'

 L. 125       214  LOAD_CONST               True
              216  LOAD_FAST                'func'
              218  LOAD_FAST                'args'
              220  BUILD_MAP_0           0 
              222  LOAD_FAST                'kwds'
              224  <164>                 1  ''
              226  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              228  BUILD_TUPLE_2         2 
              230  STORE_FAST               'result'
              232  POP_BLOCK        
              234  JUMP_FORWARD        310  'to 310'
            236_0  COME_FROM_FINALLY   212  '212'

 L. 126       236  DUP_TOP          
              238  LOAD_GLOBAL              Exception
          240_242  <121>               308  ''
              244  POP_TOP          
              246  STORE_FAST               'e'
              248  POP_TOP          
              250  SETUP_FINALLY       300  'to 300'

 L. 127       252  LOAD_FAST                'wrap_exception'
          254_256  POP_JUMP_IF_FALSE   280  'to 280'
              258  LOAD_FAST                'func'
              260  LOAD_GLOBAL              _helper_reraises_exception
              262  <117>                 1  ''
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
              290  POP_EXCEPT       
              292  LOAD_CONST               None
              294  STORE_FAST               'e'
              296  DELETE_FAST              'e'
              298  JUMP_FORWARD        310  'to 310'
            300_0  COME_FROM_FINALLY   250  '250'
              300  LOAD_CONST               None
              302  STORE_FAST               'e'
              304  DELETE_FAST              'e'
              306  <48>             
              308  <48>             
            310_0  COME_FROM           298  '298'
            310_1  COME_FROM           234  '234'

 L. 130       310  SETUP_FINALLY       330  'to 330'

 L. 131       312  LOAD_FAST                'put'
              314  LOAD_FAST                'job'
              316  LOAD_FAST                'i'
              318  LOAD_FAST                'result'
              320  BUILD_TUPLE_3         3 
              322  CALL_FUNCTION_1       1  ''
              324  POP_TOP          
              326  POP_BLOCK        
              328  JUMP_FORWARD        414  'to 414'
            330_0  COME_FROM_FINALLY   310  '310'

 L. 132       330  DUP_TOP          
              332  LOAD_GLOBAL              Exception
          334_336  <121>               412  ''
              338  POP_TOP          
              340  STORE_FAST               'e'
              342  POP_TOP          
              344  SETUP_FINALLY       404  'to 404'

 L. 133       346  LOAD_GLOBAL              MaybeEncodingError
              348  LOAD_FAST                'e'
              350  LOAD_FAST                'result'
              352  LOAD_CONST               1
              354  BINARY_SUBSCR    
              356  CALL_FUNCTION_2       2  ''
              358  STORE_FAST               'wrapped'

 L. 134       360  LOAD_GLOBAL              util
              362  LOAD_METHOD              debug
              364  LOAD_STR                 'Possible encoding error while sending result: %s'

 L. 135       366  LOAD_FAST                'wrapped'

 L. 134       368  BINARY_MODULO    
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          

 L. 136       374  LOAD_FAST                'put'
              376  LOAD_FAST                'job'
              378  LOAD_FAST                'i'
              380  LOAD_CONST               False
              382  LOAD_FAST                'wrapped'
              384  BUILD_TUPLE_2         2 
              386  BUILD_TUPLE_3         3 
              388  CALL_FUNCTION_1       1  ''
              390  POP_TOP          
              392  POP_BLOCK        
              394  POP_EXCEPT       
              396  LOAD_CONST               None
              398  STORE_FAST               'e'
              400  DELETE_FAST              'e'
              402  JUMP_FORWARD        414  'to 414'
            404_0  COME_FROM_FINALLY   344  '344'
              404  LOAD_CONST               None
              406  STORE_FAST               'e'
              408  DELETE_FAST              'e'
              410  <48>             
              412  <48>             
            414_0  COME_FROM           402  '402'
            414_1  COME_FROM           328  '328'

 L. 138       414  LOAD_CONST               None
              416  DUP_TOP          
              418  STORE_FAST               'task'
              420  DUP_TOP          
              422  STORE_FAST               'job'
              424  DUP_TOP          
              426  STORE_FAST               'result'
              428  DUP_TOP          
              430  STORE_FAST               'func'
              432  DUP_TOP          
              434  STORE_FAST               'args'
              436  STORE_FAST               'kwds'

 L. 139       438  LOAD_FAST                'completed'
              440  LOAD_CONST               1
              442  INPLACE_ADD      
              444  STORE_FAST               'completed'
              446  JUMP_BACK           102  'to 102'
            448_0  COME_FROM           194  '194'
            448_1  COME_FROM           166  '166'
            448_2  COME_FROM           122  '122'
            448_3  COME_FROM           112  '112'

 L. 140       448  LOAD_GLOBAL              util
              450  LOAD_METHOD              debug
              452  LOAD_STR                 'worker exiting after %d tasks'
              454  LOAD_FAST                'completed'
              456  BINARY_MODULO    
              458  CALL_METHOD_1         1  ''
              460  POP_TOP          

Parse error at or near `None' instruction at offset -1


def _helper_reraises_exception(ex):
    """Pickle-able helper function for use by _guarded_task_generation."""
    raise ex


class _PoolCache(dict):
    __doc__ = '\n    Class that implements a cache for the Pool class that will notify\n    the pool management threads every time the cache is emptied. The\n    notification is done by the use of a queue that is provided when\n    instantiating the cache.\n    '

    def __init__--- This code section failed: ---

 L. 158         0  LOAD_FAST                'notifier'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               notifier

 L. 159         6  LOAD_GLOBAL              super
                8  CALL_FUNCTION_0       0  ''
               10  LOAD_ATTR                __init__
               12  LOAD_FAST                'args'
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwds'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  POP_TOP          

Parse error at or near `<164>' instruction at offset 18

    def __delitem__(self, item):
        super.__delitem__(item)
        if not self:
            self.notifier.put(None)


class Pool(object):
    __doc__ = '\n    Class which supports an async version of applying functions to arguments.\n    '
    _wrap_exception = True

    @staticmethod
    def Process--- This code section failed: ---

 L. 181         0  LOAD_FAST                'ctx'
                2  LOAD_ATTR                Process
                4  LOAD_FAST                'args'
                6  BUILD_MAP_0           0 
                8  LOAD_FAST                'kwds'
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __init__--- This code section failed: ---

 L. 187         0  BUILD_LIST_0          0 
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _pool

 L. 188         6  LOAD_GLOBAL              INIT
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _state

 L. 190        12  LOAD_FAST                'context'
               14  JUMP_IF_TRUE_OR_POP    20  'to 20'
               16  LOAD_GLOBAL              get_context
               18  CALL_FUNCTION_0       0  ''
             20_0  COME_FROM            14  '14'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _ctx

 L. 191        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _setup_queues
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          

 L. 192        32  LOAD_GLOBAL              queue
               34  LOAD_METHOD              SimpleQueue
               36  CALL_METHOD_0         0  ''
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _taskqueue

 L. 196        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _ctx
               46  LOAD_METHOD              SimpleQueue
               48  CALL_METHOD_0         0  ''
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _change_notifier

 L. 197        54  LOAD_GLOBAL              _PoolCache
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _change_notifier
               60  LOAD_CONST               ('notifier',)
               62  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _cache

 L. 198        68  LOAD_FAST                'maxtasksperchild'
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _maxtasksperchild

 L. 199        74  LOAD_FAST                'initializer'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _initializer

 L. 200        80  LOAD_FAST                'initargs'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _initargs

 L. 202        86  LOAD_FAST                'processes'
               88  LOAD_CONST               None
               90  <117>                 0  ''
               92  POP_JUMP_IF_FALSE   106  'to 106'

 L. 203        94  LOAD_GLOBAL              os
               96  LOAD_METHOD              cpu_count
               98  CALL_METHOD_0         0  ''
              100  JUMP_IF_TRUE_OR_POP   104  'to 104'
              102  LOAD_CONST               1
            104_0  COME_FROM           100  '100'
              104  STORE_FAST               'processes'
            106_0  COME_FROM            92  '92'

 L. 204       106  LOAD_FAST                'processes'
              108  LOAD_CONST               1
              110  COMPARE_OP               <
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 205       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 'Number of processes must be at least 1'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'

 L. 207       122  LOAD_FAST                'initializer'
              124  LOAD_CONST               None
              126  <117>                 1  ''
              128  POP_JUMP_IF_FALSE   146  'to 146'
              130  LOAD_GLOBAL              callable
              132  LOAD_FAST                'initializer'
              134  CALL_FUNCTION_1       1  ''
              136  POP_JUMP_IF_TRUE    146  'to 146'

 L. 208       138  LOAD_GLOBAL              TypeError
              140  LOAD_STR                 'initializer must be a callable'
              142  CALL_FUNCTION_1       1  ''
              144  RAISE_VARARGS_1       1  'exception instance'
            146_0  COME_FROM           136  '136'
            146_1  COME_FROM           128  '128'

 L. 210       146  LOAD_FAST                'processes'
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _processes

 L. 211       152  SETUP_FINALLY       166  'to 166'

 L. 212       154  LOAD_FAST                'self'
              156  LOAD_METHOD              _repopulate_pool
              158  CALL_METHOD_0         0  ''
              160  POP_TOP          
              162  POP_BLOCK        
              164  JUMP_FORWARD        236  'to 236'
            166_0  COME_FROM_FINALLY   152  '152'

 L. 213       166  DUP_TOP          
              168  LOAD_GLOBAL              Exception
              170  <121>               234  ''
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 214       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _pool
              182  GET_ITER         
            184_0  COME_FROM           206  '206'
            184_1  COME_FROM           196  '196'
              184  FOR_ITER            208  'to 208'
              186  STORE_FAST               'p'

 L. 215       188  LOAD_FAST                'p'
              190  LOAD_ATTR                exitcode
              192  LOAD_CONST               None
              194  <117>                 0  ''
              196  POP_JUMP_IF_FALSE_BACK   184  'to 184'

 L. 216       198  LOAD_FAST                'p'
              200  LOAD_METHOD              terminate
              202  CALL_METHOD_0         0  ''
              204  POP_TOP          
              206  JUMP_BACK           184  'to 184'
            208_0  COME_FROM           184  '184'

 L. 217       208  LOAD_FAST                'self'
              210  LOAD_ATTR                _pool
              212  GET_ITER         
            214_0  COME_FROM           226  '226'
              214  FOR_ITER            228  'to 228'
              216  STORE_FAST               'p'

 L. 218       218  LOAD_FAST                'p'
              220  LOAD_METHOD              join
              222  CALL_METHOD_0         0  ''
              224  POP_TOP          
              226  JUMP_BACK           214  'to 214'
            228_0  COME_FROM           214  '214'

 L. 219       228  RAISE_VARARGS_0       0  'reraise'
              230  POP_EXCEPT       
              232  JUMP_FORWARD        236  'to 236'
              234  <48>             
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           164  '164'

 L. 221       236  LOAD_FAST                'self'
              238  LOAD_METHOD              _get_sentinels
              240  CALL_METHOD_0         0  ''
              242  STORE_FAST               'sentinels'

 L. 223       244  LOAD_GLOBAL              threading
              246  LOAD_ATTR                Thread

 L. 224       248  LOAD_GLOBAL              Pool
              250  LOAD_ATTR                _handle_workers

 L. 225       252  LOAD_FAST                'self'
              254  LOAD_ATTR                _cache
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                _taskqueue
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                _ctx
              264  LOAD_FAST                'self'
              266  LOAD_ATTR                Process

 L. 226       268  LOAD_FAST                'self'
              270  LOAD_ATTR                _processes
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                _pool
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                _inqueue
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                _outqueue

 L. 227       284  LOAD_FAST                'self'
              286  LOAD_ATTR                _initializer
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                _initargs
              292  LOAD_FAST                'self'
              294  LOAD_ATTR                _maxtasksperchild

 L. 228       296  LOAD_FAST                'self'
              298  LOAD_ATTR                _wrap_exception
              300  LOAD_FAST                'sentinels'
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                _change_notifier

 L. 225       306  BUILD_TUPLE_14       14 

 L. 223       308  LOAD_CONST               ('target', 'args')
              310  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              312  LOAD_FAST                'self'
              314  STORE_ATTR               _worker_handler

 L. 230       316  LOAD_CONST               True
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                _worker_handler
              322  STORE_ATTR               daemon

 L. 231       324  LOAD_GLOBAL              RUN
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                _worker_handler
              330  STORE_ATTR               _state

 L. 232       332  LOAD_FAST                'self'
              334  LOAD_ATTR                _worker_handler
              336  LOAD_METHOD              start
              338  CALL_METHOD_0         0  ''
              340  POP_TOP          

 L. 235       342  LOAD_GLOBAL              threading
              344  LOAD_ATTR                Thread

 L. 236       346  LOAD_GLOBAL              Pool
              348  LOAD_ATTR                _handle_tasks

 L. 237       350  LOAD_FAST                'self'
              352  LOAD_ATTR                _taskqueue
              354  LOAD_FAST                'self'
              356  LOAD_ATTR                _quick_put
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                _outqueue

 L. 238       362  LOAD_FAST                'self'
              364  LOAD_ATTR                _pool
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                _cache

 L. 237       370  BUILD_TUPLE_5         5 

 L. 235       372  LOAD_CONST               ('target', 'args')
              374  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              376  LOAD_FAST                'self'
              378  STORE_ATTR               _task_handler

 L. 240       380  LOAD_CONST               True
              382  LOAD_FAST                'self'
              384  LOAD_ATTR                _task_handler
              386  STORE_ATTR               daemon

 L. 241       388  LOAD_GLOBAL              RUN
              390  LOAD_FAST                'self'
              392  LOAD_ATTR                _task_handler
              394  STORE_ATTR               _state

 L. 242       396  LOAD_FAST                'self'
              398  LOAD_ATTR                _task_handler
              400  LOAD_METHOD              start
              402  CALL_METHOD_0         0  ''
              404  POP_TOP          

 L. 244       406  LOAD_GLOBAL              threading
              408  LOAD_ATTR                Thread

 L. 245       410  LOAD_GLOBAL              Pool
              412  LOAD_ATTR                _handle_results

 L. 246       414  LOAD_FAST                'self'
              416  LOAD_ATTR                _outqueue
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                _quick_get
              422  LOAD_FAST                'self'
              424  LOAD_ATTR                _cache
              426  BUILD_TUPLE_3         3 

 L. 244       428  LOAD_CONST               ('target', 'args')
              430  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              432  LOAD_FAST                'self'
              434  STORE_ATTR               _result_handler

 L. 248       436  LOAD_CONST               True
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                _result_handler
              442  STORE_ATTR               daemon

 L. 249       444  LOAD_GLOBAL              RUN
              446  LOAD_FAST                'self'
              448  LOAD_ATTR                _result_handler
              450  STORE_ATTR               _state

 L. 250       452  LOAD_FAST                'self'
              454  LOAD_ATTR                _result_handler
              456  LOAD_METHOD              start
              458  CALL_METHOD_0         0  ''
              460  POP_TOP          

 L. 252       462  LOAD_GLOBAL              util
              464  LOAD_ATTR                Finalize

 L. 253       466  LOAD_FAST                'self'
              468  LOAD_FAST                'self'
              470  LOAD_ATTR                _terminate_pool

 L. 254       472  LOAD_FAST                'self'
              474  LOAD_ATTR                _taskqueue
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                _inqueue
              480  LOAD_FAST                'self'
              482  LOAD_ATTR                _outqueue
              484  LOAD_FAST                'self'
              486  LOAD_ATTR                _pool

 L. 255       488  LOAD_FAST                'self'
              490  LOAD_ATTR                _change_notifier
              492  LOAD_FAST                'self'
              494  LOAD_ATTR                _worker_handler
              496  LOAD_FAST                'self'
              498  LOAD_ATTR                _task_handler

 L. 256       500  LOAD_FAST                'self'
              502  LOAD_ATTR                _result_handler
              504  LOAD_FAST                'self'
              506  LOAD_ATTR                _cache

 L. 254       508  BUILD_TUPLE_9         9 

 L. 257       510  LOAD_CONST               15

 L. 252       512  LOAD_CONST               ('args', 'exitpriority')
              514  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              516  LOAD_FAST                'self'
              518  STORE_ATTR               _terminate

 L. 259       520  LOAD_GLOBAL              RUN
              522  LOAD_FAST                'self'
              524  STORE_ATTR               _state

Parse error at or near `<117>' instruction at offset 90

    def __del__--- This code section failed: ---

 L. 264         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _state
                4  LOAD_FAST                'RUN'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    58  'to 58'

 L. 265        10  LOAD_FAST                '_warn'
               12  LOAD_STR                 'unclosed running multiprocessing pool '
               14  LOAD_FAST                'self'
               16  FORMAT_VALUE          2  '!r'
               18  BUILD_STRING_2        2 

 L. 266        20  LOAD_GLOBAL              ResourceWarning
               22  LOAD_FAST                'self'

 L. 265        24  LOAD_CONST               ('source',)
               26  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               28  POP_TOP          

 L. 267        30  LOAD_GLOBAL              getattr
               32  LOAD_FAST                'self'
               34  LOAD_STR                 '_change_notifier'
               36  LOAD_CONST               None
               38  CALL_FUNCTION_3       3  ''
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    58  'to 58'

 L. 268        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _change_notifier
               50  LOAD_METHOD              put
               52  LOAD_CONST               None
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
             58_0  COME_FROM            44  '44'
             58_1  COME_FROM             8  '8'

Parse error at or near `<117>' instruction at offset 42

    def __repr__(self):
        cls = self.__class__
        return f"<{cls.__module__}.{cls.__qualname__} state={self._state} pool_size={len(self._pool)}>"

    def _get_sentinels--- This code section failed: ---

 L. 277         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _outqueue
                4  LOAD_ATTR                _reader
                6  BUILD_LIST_1          1 
                8  STORE_FAST               'task_queue_sentinels'

 L. 278        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _change_notifier
               14  LOAD_ATTR                _reader
               16  BUILD_LIST_1          1 
               18  STORE_FAST               'self_notifier_sentinels'

 L. 279        20  BUILD_LIST_0          0 
               22  LOAD_FAST                'task_queue_sentinels'
               24  CALL_FINALLY         27  'to 27'
               26  LOAD_FAST                'self_notifier_sentinels'
               28  CALL_FINALLY         31  'to 31'
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 24

    @staticmethod
    def _get_worker_sentinels(workers):
        return [worker.sentinel for worker in workers if hasattr(worker, 'sentinel')]

    @staticmethod
    def _join_exited_workers--- This code section failed: ---

 L. 291         0  LOAD_CONST               False
                2  STORE_FAST               'cleaned'

 L. 292         4  LOAD_GLOBAL              reversed
                6  LOAD_GLOBAL              range
                8  LOAD_GLOBAL              len
               10  LOAD_FAST                'pool'
               12  CALL_FUNCTION_1       1  ''
               14  CALL_FUNCTION_1       1  ''
               16  CALL_FUNCTION_1       1  ''
               18  GET_ITER         
             20_0  COME_FROM            74  '74'
             20_1  COME_FROM            40  '40'
               20  FOR_ITER             76  'to 76'
               22  STORE_FAST               'i'

 L. 293        24  LOAD_FAST                'pool'
               26  LOAD_FAST                'i'
               28  BINARY_SUBSCR    
               30  STORE_FAST               'worker'

 L. 294        32  LOAD_FAST                'worker'
               34  LOAD_ATTR                exitcode
               36  LOAD_CONST               None
               38  <117>                 1  ''
               40  POP_JUMP_IF_FALSE_BACK    20  'to 20'

 L. 296        42  LOAD_GLOBAL              util
               44  LOAD_METHOD              debug
               46  LOAD_STR                 'cleaning up worker %d'
               48  LOAD_FAST                'i'
               50  BINARY_MODULO    
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 297        56  LOAD_FAST                'worker'
               58  LOAD_METHOD              join
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          

 L. 298        64  LOAD_CONST               True
               66  STORE_FAST               'cleaned'

 L. 299        68  LOAD_FAST                'pool'
               70  LOAD_FAST                'i'
               72  DELETE_SUBSCR    
               74  JUMP_BACK            20  'to 20'
             76_0  COME_FROM            20  '20'

 L. 300        76  LOAD_FAST                'cleaned'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 38

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

    def _guarded_task_generation--- This code section failed: ---

 L. 386         0  SETUP_FINALLY        46  'to 46'

 L. 387         2  LOAD_CONST               -1
                4  STORE_FAST               'i'

 L. 388         6  LOAD_GLOBAL              enumerate
                8  LOAD_FAST                'iterable'
               10  CALL_FUNCTION_1       1  ''
               12  GET_ITER         
             14_0  COME_FROM            40  '40'
               14  FOR_ITER             42  'to 42'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'i'
               20  STORE_FAST               'x'

 L. 389        22  LOAD_FAST                'result_job'
               24  LOAD_FAST                'i'
               26  LOAD_FAST                'func'
               28  LOAD_FAST                'x'
               30  BUILD_TUPLE_1         1 
               32  BUILD_MAP_0           0 
               34  BUILD_TUPLE_5         5 
               36  YIELD_VALUE      
               38  POP_TOP          
               40  JUMP_BACK            14  'to 14'
             42_0  COME_FROM            14  '14'
               42  POP_BLOCK        
               44  JUMP_FORWARD        104  'to 104'
             46_0  COME_FROM_FINALLY     0  '0'

 L. 390        46  DUP_TOP          
               48  LOAD_GLOBAL              Exception
               50  <121>               102  ''
               52  POP_TOP          
               54  STORE_FAST               'e'
               56  POP_TOP          
               58  SETUP_FINALLY        94  'to 94'

 L. 391        60  LOAD_FAST                'result_job'
               62  LOAD_FAST                'i'
               64  LOAD_CONST               1
               66  BINARY_ADD       
               68  LOAD_GLOBAL              _helper_reraises_exception
               70  LOAD_FAST                'e'
               72  BUILD_TUPLE_1         1 
               74  BUILD_MAP_0           0 
               76  BUILD_TUPLE_5         5 
               78  YIELD_VALUE      
               80  POP_TOP          
               82  POP_BLOCK        
               84  POP_EXCEPT       
               86  LOAD_CONST               None
               88  STORE_FAST               'e'
               90  DELETE_FAST              'e'
               92  JUMP_FORWARD        104  'to 104'
             94_0  COME_FROM_FINALLY    58  '58'
               94  LOAD_CONST               None
               96  STORE_FAST               'e'
               98  DELETE_FAST              'e'
              100  <48>             
              102  <48>             
            104_0  COME_FROM            92  '92'
            104_1  COME_FROM            44  '44'

Parse error at or near `<121>' instruction at offset 50

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

    def _map_async--- This code section failed: ---

 L. 473         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_running
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 474         8  LOAD_GLOBAL              hasattr
               10  LOAD_FAST                'iterable'
               12  LOAD_STR                 '__len__'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     26  'to 26'

 L. 475        18  LOAD_GLOBAL              list
               20  LOAD_FAST                'iterable'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'iterable'
             26_0  COME_FROM            16  '16'

 L. 477        26  LOAD_FAST                'chunksize'
               28  LOAD_CONST               None
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    74  'to 74'

 L. 478        34  LOAD_GLOBAL              divmod
               36  LOAD_GLOBAL              len
               38  LOAD_FAST                'iterable'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _pool
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               4
               52  BINARY_MULTIPLY  
               54  CALL_FUNCTION_2       2  ''
               56  UNPACK_SEQUENCE_2     2 
               58  STORE_FAST               'chunksize'
               60  STORE_FAST               'extra'

 L. 479        62  LOAD_FAST                'extra'
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 480        66  LOAD_FAST                'chunksize'
               68  LOAD_CONST               1
               70  INPLACE_ADD      
               72  STORE_FAST               'chunksize'
             74_0  COME_FROM            64  '64'
             74_1  COME_FROM            32  '32'

 L. 481        74  LOAD_GLOBAL              len
               76  LOAD_FAST                'iterable'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_CONST               0
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    90  'to 90'

 L. 482        86  LOAD_CONST               0
               88  STORE_FAST               'chunksize'
             90_0  COME_FROM            84  '84'

 L. 484        90  LOAD_GLOBAL              Pool
               92  LOAD_METHOD              _get_tasks
               94  LOAD_FAST                'func'
               96  LOAD_FAST                'iterable'
               98  LOAD_FAST                'chunksize'
              100  CALL_METHOD_3         3  ''
              102  STORE_FAST               'task_batches'

 L. 485       104  LOAD_GLOBAL              MapResult
              106  LOAD_FAST                'self'
              108  LOAD_FAST                'chunksize'
              110  LOAD_GLOBAL              len
              112  LOAD_FAST                'iterable'
              114  CALL_FUNCTION_1       1  ''
              116  LOAD_FAST                'callback'

 L. 486       118  LOAD_FAST                'error_callback'

 L. 485       120  LOAD_CONST               ('error_callback',)
              122  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              124  STORE_FAST               'result'

 L. 487       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _taskqueue
              130  LOAD_METHOD              put

 L. 489       132  LOAD_FAST                'self'
              134  LOAD_METHOD              _guarded_task_generation
              136  LOAD_FAST                'result'
              138  LOAD_ATTR                _job

 L. 490       140  LOAD_FAST                'mapper'

 L. 491       142  LOAD_FAST                'task_batches'

 L. 489       144  CALL_METHOD_3         3  ''

 L. 492       146  LOAD_CONST               None

 L. 488       148  BUILD_TUPLE_2         2 

 L. 487       150  CALL_METHOD_1         1  ''
              152  POP_TOP          

 L. 495       154  LOAD_FAST                'result'
              156  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 30

    @staticmethod
    def _wait_for_updates(sentinels, change_notifier, timeout=None):
        wait(sentinels, timeout=timeout)
        while True:
            change_notifier.empty() or change_notifier.get()

    @classmethod
    def _handle_workers--- This code section failed: ---

 L. 508         0  LOAD_GLOBAL              threading
                2  LOAD_METHOD              current_thread
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'thread'
              8_0  COME_FROM            90  '90'

 L. 512         8  LOAD_FAST                'thread'
               10  LOAD_ATTR                _state
               12  LOAD_GLOBAL              RUN
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_TRUE     32  'to 32'
               18  LOAD_FAST                'cache'
               20  POP_JUMP_IF_FALSE    92  'to 92'
               22  LOAD_FAST                'thread'
               24  LOAD_ATTR                _state
               26  LOAD_GLOBAL              TERMINATE
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    92  'to 92'
             32_0  COME_FROM            16  '16'

 L. 513        32  LOAD_FAST                'cls'
               34  LOAD_METHOD              _maintain_pool
               36  LOAD_FAST                'ctx'
               38  LOAD_FAST                'Process'
               40  LOAD_FAST                'processes'
               42  LOAD_FAST                'pool'
               44  LOAD_FAST                'inqueue'

 L. 514        46  LOAD_FAST                'outqueue'
               48  LOAD_FAST                'initializer'
               50  LOAD_FAST                'initargs'

 L. 515        52  LOAD_FAST                'maxtasksperchild'
               54  LOAD_FAST                'wrap_exception'

 L. 513        56  CALL_METHOD_10       10  ''
               58  POP_TOP          

 L. 517        60  BUILD_LIST_0          0 
               62  LOAD_FAST                'cls'
               64  LOAD_METHOD              _get_worker_sentinels
               66  LOAD_FAST                'pool'
               68  CALL_METHOD_1         1  ''
               70  CALL_FINALLY         73  'to 73'
               72  LOAD_FAST                'sentinels'
               74  CALL_FINALLY         77  'to 77'
               76  STORE_FAST               'current_sentinels'

 L. 519        78  LOAD_FAST                'cls'
               80  LOAD_METHOD              _wait_for_updates
               82  LOAD_FAST                'current_sentinels'
               84  LOAD_FAST                'change_notifier'
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          
               90  JUMP_BACK             8  'to 8'
             92_0  COME_FROM            30  '30'
             92_1  COME_FROM            20  '20'

 L. 521        92  LOAD_FAST                'taskqueue'
               94  LOAD_METHOD              put
               96  LOAD_CONST               None
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 522       102  LOAD_GLOBAL              util
              104  LOAD_METHOD              debug
              106  LOAD_STR                 'worker handler exiting'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 70

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
             20_0  COME_FROM           288  '288'
             20_1  COME_FROM           272  '272'
             20_2  COME_FROM           236  '236'
            20_22  FOR_ITER            290  'to 290'
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'taskseq'
               28  STORE_FAST               'set_length'

 L. 529        30  LOAD_CONST               None
               32  STORE_FAST               'task'

 L. 530        34  SETUP_FINALLY       274  'to 274'

 L. 532        36  LOAD_FAST                'taskseq'
               38  GET_ITER         
             40_0  COME_FROM           178  '178'
             40_1  COME_FROM           166  '166'
             40_2  COME_FROM            80  '80'
               40  FOR_ITER            180  'to 180'
               42  STORE_FAST               'task'

 L. 533        44  LOAD_FAST                'thread'
               46  LOAD_ATTR                _state
               48  LOAD_GLOBAL              RUN
               50  COMPARE_OP               !=
               52  POP_JUMP_IF_FALSE    68  'to 68'

 L. 534        54  LOAD_GLOBAL              util
               56  LOAD_METHOD              debug
               58  LOAD_STR                 'task handler found thread._state != RUN'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 535        64  POP_TOP          
               66  BREAK_LOOP          238  'to 238'
             68_0  COME_FROM            52  '52'

 L. 536        68  SETUP_FINALLY        82  'to 82'

 L. 537        70  LOAD_FAST                'put'
               72  LOAD_FAST                'task'
               74  CALL_FUNCTION_1       1  ''
               76  POP_TOP          
               78  POP_BLOCK        
               80  JUMP_BACK            40  'to 40'
             82_0  COME_FROM_FINALLY    68  '68'

 L. 538        82  DUP_TOP          
               84  LOAD_GLOBAL              Exception
               86  <121>               176  ''
               88  POP_TOP          
               90  STORE_FAST               'e'
               92  POP_TOP          
               94  SETUP_FINALLY       168  'to 168'

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
              136  JUMP_FORWARD        156  'to 156'
            138_0  COME_FROM_FINALLY   112  '112'

 L. 542       138  DUP_TOP          
              140  LOAD_GLOBAL              KeyError
              142  <121>               154  ''
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 543       150  POP_EXCEPT       
              152  BREAK_LOOP          156  'to 156'
              154  <48>             
            156_0  COME_FROM           152  '152'
            156_1  COME_FROM           136  '136'
              156  POP_BLOCK        
              158  POP_EXCEPT       
              160  LOAD_CONST               None
              162  STORE_FAST               'e'
              164  DELETE_FAST              'e'
              166  JUMP_BACK            40  'to 40'
            168_0  COME_FROM_FINALLY    94  '94'
              168  LOAD_CONST               None
              170  STORE_FAST               'e'
              172  DELETE_FAST              'e'
              174  <48>             
              176  <48>             
              178  JUMP_BACK            40  'to 40'
            180_0  COME_FROM            40  '40'

 L. 545       180  LOAD_FAST                'set_length'
              182  POP_JUMP_IF_FALSE   222  'to 222'

 L. 546       184  LOAD_GLOBAL              util
              186  LOAD_METHOD              debug
              188  LOAD_STR                 'doing set_length()'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          

 L. 547       194  LOAD_FAST                'task'
              196  POP_JUMP_IF_FALSE   206  'to 206'
              198  LOAD_FAST                'task'
              200  LOAD_CONST               1
              202  BINARY_SUBSCR    
              204  JUMP_FORWARD        208  'to 208'
            206_0  COME_FROM           196  '196'
              206  LOAD_CONST               -1
            208_0  COME_FROM           204  '204'
              208  STORE_FAST               'idx'

 L. 548       210  LOAD_FAST                'set_length'
              212  LOAD_FAST                'idx'
              214  LOAD_CONST               1
              216  BINARY_ADD       
              218  CALL_FUNCTION_1       1  ''
              220  POP_TOP          
            222_0  COME_FROM           182  '182'

 L. 549       222  POP_BLOCK        

 L. 552       224  LOAD_CONST               None
              226  DUP_TOP          
              228  STORE_FAST               'task'
              230  DUP_TOP          
              232  STORE_FAST               'taskseq'
              234  STORE_FAST               'job'

 L. 549       236  JUMP_BACK            20  'to 20'
            238_0  COME_FROM            66  '66'

 L. 550       238  POP_BLOCK        

 L. 552       240  LOAD_CONST               None
              242  DUP_TOP          
              244  STORE_FAST               'task'
              246  DUP_TOP          
              248  STORE_FAST               'taskseq'
              250  STORE_FAST               'job'

 L. 550       252  POP_TOP          
          254_256  JUMP_FORWARD        300  'to 300'
              258  POP_BLOCK        

 L. 552       260  LOAD_CONST               None
              262  DUP_TOP          
              264  STORE_FAST               'task'
              266  DUP_TOP          
              268  STORE_FAST               'taskseq'
              270  STORE_FAST               'job'
              272  JUMP_BACK            20  'to 20'
            274_0  COME_FROM_FINALLY    34  '34'
              274  LOAD_CONST               None
              276  DUP_TOP          
              278  STORE_FAST               'task'
              280  DUP_TOP          
              282  STORE_FAST               'taskseq'
              284  STORE_FAST               'job'
              286  <48>             
              288  JUMP_BACK            20  'to 20'
            290_0  COME_FROM            20  '20'

 L. 554       290  LOAD_GLOBAL              util
              292  LOAD_METHOD              debug
              294  LOAD_STR                 'task handler got sentinel'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
            300_0  COME_FROM           254  '254'

 L. 556       300  SETUP_FINALLY       356  'to 356'

 L. 558       302  LOAD_GLOBAL              util
              304  LOAD_METHOD              debug
              306  LOAD_STR                 'task handler sending sentinel to result handler'
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          

 L. 559       312  LOAD_FAST                'outqueue'
              314  LOAD_METHOD              put
              316  LOAD_CONST               None
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          

 L. 562       322  LOAD_GLOBAL              util
              324  LOAD_METHOD              debug
              326  LOAD_STR                 'task handler sending sentinel to workers'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          

 L. 563       332  LOAD_FAST                'pool'
              334  GET_ITER         
            336_0  COME_FROM           348  '348'
              336  FOR_ITER            352  'to 352'
              338  STORE_FAST               'p'

 L. 564       340  LOAD_FAST                'put'
              342  LOAD_CONST               None
              344  CALL_FUNCTION_1       1  ''
              346  POP_TOP          
          348_350  JUMP_BACK           336  'to 336'
            352_0  COME_FROM           336  '336'
              352  POP_BLOCK        
              354  JUMP_FORWARD        386  'to 386'
            356_0  COME_FROM_FINALLY   300  '300'

 L. 565       356  DUP_TOP          
              358  LOAD_GLOBAL              OSError
          360_362  <121>               384  ''
              364  POP_TOP          
              366  POP_TOP          
              368  POP_TOP          

 L. 566       370  LOAD_GLOBAL              util
              372  LOAD_METHOD              debug
              374  LOAD_STR                 'task handler got OSError when sending sentinels'
              376  CALL_METHOD_1         1  ''
              378  POP_TOP          
              380  POP_EXCEPT       
              382  JUMP_FORWARD        386  'to 386'
              384  <48>             
            386_0  COME_FROM           382  '382'
            386_1  COME_FROM           354  '354'

 L. 568       386  LOAD_GLOBAL              util
              388  LOAD_METHOD              debug
              390  LOAD_STR                 'task handler exiting'
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          

Parse error at or near `<121>' instruction at offset 86

    @staticmethod
    def _handle_results--- This code section failed: ---

 L. 572         0  LOAD_GLOBAL              threading
                2  LOAD_METHOD              current_thread
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'thread'
              8_0  COME_FROM           176  '176'

 L. 575         8  SETUP_FINALLY        20  'to 20'

 L. 576        10  LOAD_FAST                'get'
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'task'
               16  POP_BLOCK        
               18  JUMP_FORWARD         54  'to 54'
             20_0  COME_FROM_FINALLY     8  '8'

 L. 577        20  DUP_TOP          
               22  LOAD_GLOBAL              OSError
               24  LOAD_GLOBAL              EOFError
               26  BUILD_TUPLE_2         2 
               28  <121>                52  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 578        36  LOAD_GLOBAL              util
               38  LOAD_METHOD              debug
               40  LOAD_STR                 'result handler got EOFError/OSError -- exiting'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 579        46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  RETURN_VALUE     
               52  <48>             
             54_0  COME_FROM            18  '18'

 L. 581        54  LOAD_FAST                'thread'
               56  LOAD_ATTR                _state
               58  LOAD_GLOBAL              RUN
               60  COMPARE_OP               !=
               62  POP_JUMP_IF_FALSE    94  'to 94'

 L. 582        64  LOAD_FAST                'thread'
               66  LOAD_ATTR                _state
               68  LOAD_GLOBAL              TERMINATE
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_TRUE     82  'to 82'
               74  <74>             
               76  LOAD_STR                 'Thread not in TERMINATE'
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            72  '72'

 L. 583        82  LOAD_GLOBAL              util
               84  LOAD_METHOD              debug
               86  LOAD_STR                 'result handler found thread._state=TERMINATE'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L. 584        92  JUMP_FORWARD        178  'to 178'
             94_0  COME_FROM            62  '62'

 L. 586        94  LOAD_FAST                'task'
               96  LOAD_CONST               None
               98  <117>                 0  ''
              100  POP_JUMP_IF_FALSE   114  'to 114'

 L. 587       102  LOAD_GLOBAL              util
              104  LOAD_METHOD              debug
              106  LOAD_STR                 'result handler got sentinel'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 588       112  JUMP_FORWARD        178  'to 178'
            114_0  COME_FROM           100  '100'

 L. 590       114  LOAD_FAST                'task'
              116  UNPACK_SEQUENCE_3     3 
              118  STORE_FAST               'job'
              120  STORE_FAST               'i'
              122  STORE_FAST               'obj'

 L. 591       124  SETUP_FINALLY       146  'to 146'

 L. 592       126  LOAD_FAST                'cache'
              128  LOAD_FAST                'job'
              130  BINARY_SUBSCR    
              132  LOAD_METHOD              _set
              134  LOAD_FAST                'i'
              136  LOAD_FAST                'obj'
              138  CALL_METHOD_2         2  ''
              140  POP_TOP          
              142  POP_BLOCK        
              144  JUMP_FORWARD        164  'to 164'
            146_0  COME_FROM_FINALLY   124  '124'

 L. 593       146  DUP_TOP          
              148  LOAD_GLOBAL              KeyError
              150  <121>               162  ''
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 594       158  POP_EXCEPT       
              160  BREAK_LOOP          164  'to 164'
              162  <48>             
            164_0  COME_FROM           160  '160'
            164_1  COME_FROM           144  '144'

 L. 595       164  LOAD_CONST               None
              166  DUP_TOP          
              168  STORE_FAST               'task'
              170  DUP_TOP          
              172  STORE_FAST               'job'
              174  STORE_FAST               'obj'
              176  JUMP_BACK             8  'to 8'
            178_0  COME_FROM           328  '328'
            178_1  COME_FROM           262  '262'
            178_2  COME_FROM           112  '112'
            178_3  COME_FROM            92  '92'

 L. 597       178  LOAD_FAST                'cache'
          180_182  POP_JUMP_IF_FALSE   330  'to 330'
              184  LOAD_FAST                'thread'
              186  LOAD_ATTR                _state
              188  LOAD_GLOBAL              TERMINATE
              190  COMPARE_OP               !=
          192_194  POP_JUMP_IF_FALSE   330  'to 330'

 L. 598       196  SETUP_FINALLY       208  'to 208'

 L. 599       198  LOAD_FAST                'get'
              200  CALL_FUNCTION_0       0  ''
              202  STORE_FAST               'task'
              204  POP_BLOCK        
              206  JUMP_FORWARD        242  'to 242'
            208_0  COME_FROM_FINALLY   196  '196'

 L. 600       208  DUP_TOP          
              210  LOAD_GLOBAL              OSError
              212  LOAD_GLOBAL              EOFError
              214  BUILD_TUPLE_2         2 
              216  <121>               240  ''
              218  POP_TOP          
              220  POP_TOP          
              222  POP_TOP          

 L. 601       224  LOAD_GLOBAL              util
              226  LOAD_METHOD              debug
              228  LOAD_STR                 'result handler got EOFError/OSError -- exiting'
              230  CALL_METHOD_1         1  ''
              232  POP_TOP          

 L. 602       234  POP_EXCEPT       
              236  LOAD_CONST               None
              238  RETURN_VALUE     
              240  <48>             
            242_0  COME_FROM           206  '206'

 L. 604       242  LOAD_FAST                'task'
              244  LOAD_CONST               None
              246  <117>                 0  ''
          248_250  POP_JUMP_IF_FALSE   264  'to 264'

 L. 605       252  LOAD_GLOBAL              util
              254  LOAD_METHOD              debug
              256  LOAD_STR                 'result handler ignoring extra sentinel'
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          

 L. 606       262  JUMP_BACK           178  'to 178'
            264_0  COME_FROM           248  '248'

 L. 607       264  LOAD_FAST                'task'
              266  UNPACK_SEQUENCE_3     3 
              268  STORE_FAST               'job'
              270  STORE_FAST               'i'
              272  STORE_FAST               'obj'

 L. 608       274  SETUP_FINALLY       296  'to 296'

 L. 609       276  LOAD_FAST                'cache'
              278  LOAD_FAST                'job'
              280  BINARY_SUBSCR    
              282  LOAD_METHOD              _set
              284  LOAD_FAST                'i'
              286  LOAD_FAST                'obj'
              288  CALL_METHOD_2         2  ''
              290  POP_TOP          
              292  POP_BLOCK        
              294  JUMP_FORWARD        316  'to 316'
            296_0  COME_FROM_FINALLY   274  '274'

 L. 610       296  DUP_TOP          
              298  LOAD_GLOBAL              KeyError
          300_302  <121>               314  ''
              304  POP_TOP          
              306  POP_TOP          
              308  POP_TOP          

 L. 611       310  POP_EXCEPT       
              312  BREAK_LOOP          316  'to 316'
              314  <48>             
            316_0  COME_FROM           312  '312'
            316_1  COME_FROM           294  '294'

 L. 612       316  LOAD_CONST               None
              318  DUP_TOP          
              320  STORE_FAST               'task'
              322  DUP_TOP          
              324  STORE_FAST               'job'
              326  STORE_FAST               'obj'
              328  JUMP_BACK           178  'to 178'
            330_0  COME_FROM           192  '192'
            330_1  COME_FROM           180  '180'

 L. 614       330  LOAD_GLOBAL              hasattr
              332  LOAD_FAST                'outqueue'
              334  LOAD_STR                 '_reader'
              336  CALL_FUNCTION_2       2  ''
          338_340  POP_JUMP_IF_FALSE   422  'to 422'

 L. 615       342  LOAD_GLOBAL              util
              344  LOAD_METHOD              debug
              346  LOAD_STR                 'ensuring that outqueue is not full'
              348  CALL_METHOD_1         1  ''
              350  POP_TOP          

 L. 619       352  SETUP_FINALLY       398  'to 398'

 L. 620       354  LOAD_GLOBAL              range
              356  LOAD_CONST               10
              358  CALL_FUNCTION_1       1  ''
              360  GET_ITER         
            362_0  COME_FROM           390  '390'
              362  FOR_ITER            394  'to 394'
              364  STORE_FAST               'i'

 L. 621       366  LOAD_FAST                'outqueue'
              368  LOAD_ATTR                _reader
              370  LOAD_METHOD              poll
              372  CALL_METHOD_0         0  ''
          374_376  POP_JUMP_IF_TRUE    384  'to 384'

 L. 622       378  POP_TOP          
          380_382  BREAK_LOOP          394  'to 394'
            384_0  COME_FROM           374  '374'

 L. 623       384  LOAD_FAST                'get'
              386  CALL_FUNCTION_0       0  ''
              388  POP_TOP          
          390_392  JUMP_BACK           362  'to 362'
            394_0  COME_FROM           380  '380'
            394_1  COME_FROM           362  '362'
              394  POP_BLOCK        
              396  JUMP_FORWARD        422  'to 422'
            398_0  COME_FROM_FINALLY   352  '352'

 L. 624       398  DUP_TOP          
              400  LOAD_GLOBAL              OSError
              402  LOAD_GLOBAL              EOFError
              404  BUILD_TUPLE_2         2 
          406_408  <121>               420  ''
              410  POP_TOP          
              412  POP_TOP          
              414  POP_TOP          

 L. 625       416  POP_EXCEPT       
              418  BREAK_LOOP          422  'to 422'
              420  <48>             
            422_0  COME_FROM           418  '418'
            422_1  COME_FROM           396  '396'
            422_2  COME_FROM           338  '338'

 L. 627       422  LOAD_GLOBAL              util
              424  LOAD_METHOD              debug
              426  LOAD_STR                 'result handler exiting: len(cache)=%s, thread._state=%s'

 L. 628       428  LOAD_GLOBAL              len
              430  LOAD_FAST                'cache'
              432  CALL_FUNCTION_1       1  ''
              434  LOAD_FAST                'thread'
              436  LOAD_ATTR                _state

 L. 627       438  CALL_METHOD_3         3  ''
              440  POP_TOP          

Parse error at or near `<121>' instruction at offset 28

    @staticmethod
    def _get_tasks(func, it, size):
        it = iter(it)
        while True:
            x = tuple(itertools.islice(it, size))
            if not x:
                return
            else:
                yield (
                 func, x)

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
        self._terminate()

    def join--- This code section failed: ---

 L. 657         0  LOAD_GLOBAL              util
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'joining pool'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 658        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _state
               14  LOAD_GLOBAL              RUN
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    30  'to 30'

 L. 659        20  LOAD_GLOBAL              ValueError
               22  LOAD_STR                 'Pool is still running'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM            18  '18'

 L. 660        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _state
               34  LOAD_GLOBAL              CLOSE
               36  LOAD_GLOBAL              TERMINATE
               38  BUILD_TUPLE_2         2 
               40  <118>                 1  ''
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 661        44  LOAD_GLOBAL              ValueError
               46  LOAD_STR                 'In unknown state'
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            42  '42'
             52_1  COME_FROM            28  '28'

 L. 662        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _worker_handler
               56  LOAD_METHOD              join
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          

 L. 663        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _task_handler
               66  LOAD_METHOD              join
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          

 L. 664        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _result_handler
               76  LOAD_METHOD              join
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          

 L. 665        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _pool
               86  GET_ITER         
             88_0  COME_FROM           100  '100'
               88  FOR_ITER            102  'to 102'
               90  STORE_FAST               'p'

 L. 666        92  LOAD_FAST                'p'
               94  LOAD_METHOD              join
               96  CALL_METHOD_0         0  ''
               98  POP_TOP          
              100  JUMP_BACK            88  'to 88'
            102_0  COME_FROM            88  '88'

Parse error at or near `<118>' instruction at offset 40

    @staticmethod
    def _help_stuff_finish(inqueue, task_handler, size):
        util.debug('removing tasks from inqueue until task handler finished')
        inqueue._rlock.acquire()
        while task_handler.is_alive():
            if inqueue._reader.poll():
                inqueue._reader.recv()
                time.sleep(0)

    @classmethod
    def _terminate_pool--- This code section failed: ---

 L. 681         0  LOAD_GLOBAL              util
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'finalizing pool'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 686        10  LOAD_GLOBAL              TERMINATE
               12  LOAD_FAST                'worker_handler'
               14  STORE_ATTR               _state

 L. 687        16  LOAD_FAST                'change_notifier'
               18  LOAD_METHOD              put
               20  LOAD_CONST               None
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L. 689        26  LOAD_GLOBAL              TERMINATE
               28  LOAD_FAST                'task_handler'
               30  STORE_ATTR               _state

 L. 691        32  LOAD_GLOBAL              util
               34  LOAD_METHOD              debug
               36  LOAD_STR                 'helping task handler/workers to finish'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 692        42  LOAD_FAST                'cls'
               44  LOAD_METHOD              _help_stuff_finish
               46  LOAD_FAST                'inqueue'
               48  LOAD_FAST                'task_handler'
               50  LOAD_GLOBAL              len
               52  LOAD_FAST                'pool'
               54  CALL_FUNCTION_1       1  ''
               56  CALL_METHOD_3         3  ''
               58  POP_TOP          

 L. 694        60  LOAD_FAST                'result_handler'
               62  LOAD_METHOD              is_alive
               64  CALL_METHOD_0         0  ''
               66  POP_JUMP_IF_TRUE     88  'to 88'
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'cache'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_CONST               0
               76  COMPARE_OP               !=
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L. 695        80  LOAD_GLOBAL              AssertionError

 L. 696        82  LOAD_STR                 'Cannot have cache with result_hander not alive'

 L. 695        84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            78  '78'
             88_1  COME_FROM            66  '66'

 L. 698        88  LOAD_GLOBAL              TERMINATE
               90  LOAD_FAST                'result_handler'
               92  STORE_ATTR               _state

 L. 699        94  LOAD_FAST                'change_notifier'
               96  LOAD_METHOD              put
               98  LOAD_CONST               None
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          

 L. 700       104  LOAD_FAST                'outqueue'
              106  LOAD_METHOD              put
              108  LOAD_CONST               None
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 704       114  LOAD_GLOBAL              util
              116  LOAD_METHOD              debug
              118  LOAD_STR                 'joining worker handler'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L. 705       124  LOAD_GLOBAL              threading
              126  LOAD_METHOD              current_thread
              128  CALL_METHOD_0         0  ''
              130  LOAD_FAST                'worker_handler'
              132  <117>                 1  ''
              134  POP_JUMP_IF_FALSE   144  'to 144'

 L. 706       136  LOAD_FAST                'worker_handler'
              138  LOAD_METHOD              join
              140  CALL_METHOD_0         0  ''
              142  POP_TOP          
            144_0  COME_FROM           134  '134'

 L. 709       144  LOAD_FAST                'pool'
              146  POP_JUMP_IF_FALSE   200  'to 200'
              148  LOAD_GLOBAL              hasattr
              150  LOAD_FAST                'pool'
              152  LOAD_CONST               0
              154  BINARY_SUBSCR    
              156  LOAD_STR                 'terminate'
              158  CALL_FUNCTION_2       2  ''
              160  POP_JUMP_IF_FALSE   200  'to 200'

 L. 710       162  LOAD_GLOBAL              util
              164  LOAD_METHOD              debug
              166  LOAD_STR                 'terminating workers'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 711       172  LOAD_FAST                'pool'
              174  GET_ITER         
            176_0  COME_FROM           198  '198'
            176_1  COME_FROM           188  '188'
              176  FOR_ITER            200  'to 200'
              178  STORE_FAST               'p'

 L. 712       180  LOAD_FAST                'p'
              182  LOAD_ATTR                exitcode
              184  LOAD_CONST               None
              186  <117>                 0  ''
              188  POP_JUMP_IF_FALSE_BACK   176  'to 176'

 L. 713       190  LOAD_FAST                'p'
              192  LOAD_METHOD              terminate
              194  CALL_METHOD_0         0  ''
              196  POP_TOP          
              198  JUMP_BACK           176  'to 176'
            200_0  COME_FROM           176  '176'
            200_1  COME_FROM           160  '160'
            200_2  COME_FROM           146  '146'

 L. 715       200  LOAD_GLOBAL              util
              202  LOAD_METHOD              debug
              204  LOAD_STR                 'joining task handler'
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          

 L. 716       210  LOAD_GLOBAL              threading
              212  LOAD_METHOD              current_thread
              214  CALL_METHOD_0         0  ''
              216  LOAD_FAST                'task_handler'
              218  <117>                 1  ''
              220  POP_JUMP_IF_FALSE   230  'to 230'

 L. 717       222  LOAD_FAST                'task_handler'
              224  LOAD_METHOD              join
              226  CALL_METHOD_0         0  ''
              228  POP_TOP          
            230_0  COME_FROM           220  '220'

 L. 719       230  LOAD_GLOBAL              util
              232  LOAD_METHOD              debug
              234  LOAD_STR                 'joining result handler'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L. 720       240  LOAD_GLOBAL              threading
              242  LOAD_METHOD              current_thread
              244  CALL_METHOD_0         0  ''
              246  LOAD_FAST                'result_handler'
              248  <117>                 1  ''
          250_252  POP_JUMP_IF_FALSE   262  'to 262'

 L. 721       254  LOAD_FAST                'result_handler'
              256  LOAD_METHOD              join
              258  CALL_METHOD_0         0  ''
              260  POP_TOP          
            262_0  COME_FROM           250  '250'

 L. 723       262  LOAD_FAST                'pool'
          264_266  POP_JUMP_IF_FALSE   340  'to 340'
              268  LOAD_GLOBAL              hasattr
              270  LOAD_FAST                'pool'
              272  LOAD_CONST               0
              274  BINARY_SUBSCR    
              276  LOAD_STR                 'terminate'
              278  CALL_FUNCTION_2       2  ''
          280_282  POP_JUMP_IF_FALSE   340  'to 340'

 L. 724       284  LOAD_GLOBAL              util
              286  LOAD_METHOD              debug
              288  LOAD_STR                 'joining pool workers'
              290  CALL_METHOD_1         1  ''
              292  POP_TOP          

 L. 725       294  LOAD_FAST                'pool'
              296  GET_ITER         
            298_0  COME_FROM           336  '336'
            298_1  COME_FROM           308  '308'
              298  FOR_ITER            340  'to 340'
              300  STORE_FAST               'p'

 L. 726       302  LOAD_FAST                'p'
              304  LOAD_METHOD              is_alive
              306  CALL_METHOD_0         0  ''
          308_310  POP_JUMP_IF_FALSE_BACK   298  'to 298'

 L. 728       312  LOAD_GLOBAL              util
              314  LOAD_METHOD              debug
              316  LOAD_STR                 'cleaning up worker %d'
              318  LOAD_FAST                'p'
              320  LOAD_ATTR                pid
              322  BINARY_MODULO    
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          

 L. 729       328  LOAD_FAST                'p'
              330  LOAD_METHOD              join
              332  CALL_METHOD_0         0  ''
              334  POP_TOP          
          336_338  JUMP_BACK           298  'to 298'
            340_0  COME_FROM           298  '298'
            340_1  COME_FROM           280  '280'
            340_2  COME_FROM           264  '264'

Parse error at or near `<117>' instruction at offset 132

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

    __class_getitem__ = classmethod(types.GenericAlias)


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

    def next--- This code section failed: ---

 L. 851         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cond
                4  SETUP_WITH          156  'to 156'
                6  POP_TOP          

 L. 852         8  SETUP_FINALLY        24  'to 24'

 L. 853        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _items
               14  LOAD_METHOD              popleft
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'item'
               20  POP_BLOCK        
               22  JUMP_FORWARD        142  'to 142'
             24_0  COME_FROM_FINALLY     8  '8'

 L. 854        24  DUP_TOP          
               26  LOAD_GLOBAL              IndexError
               28  <121>               140  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 855        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _index
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _length
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L. 856        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _pool

 L. 857        54  LOAD_GLOBAL              StopIteration
               56  LOAD_CONST               None
               58  RAISE_VARARGS_2       2  'exception instance with __cause__'
             60_0  COME_FROM            46  '46'

 L. 858        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _cond
               64  LOAD_METHOD              wait
               66  LOAD_FAST                'timeout'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 859        72  SETUP_FINALLY        88  'to 88'

 L. 860        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _items
               78  LOAD_METHOD              popleft
               80  CALL_METHOD_0         0  ''
               82  STORE_FAST               'item'
               84  POP_BLOCK        
               86  JUMP_FORWARD        136  'to 136'
             88_0  COME_FROM_FINALLY    72  '72'

 L. 861        88  DUP_TOP          
               90  LOAD_GLOBAL              IndexError
               92  <121>               134  ''
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 862       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _index
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _length
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   124  'to 124'

 L. 863       112  LOAD_CONST               None
              114  LOAD_FAST                'self'
              116  STORE_ATTR               _pool

 L. 864       118  LOAD_GLOBAL              StopIteration
              120  LOAD_CONST               None
              122  RAISE_VARARGS_2       2  'exception instance with __cause__'
            124_0  COME_FROM           110  '110'

 L. 865       124  LOAD_GLOBAL              TimeoutError
              126  LOAD_CONST               None
              128  RAISE_VARARGS_2       2  'exception instance with __cause__'
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
              134  <48>             
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM            86  '86'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
              140  <48>             
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM            22  '22'
              142  POP_BLOCK        
              144  LOAD_CONST               None
              146  DUP_TOP          
              148  DUP_TOP          
              150  CALL_FUNCTION_3       3  ''
              152  POP_TOP          
              154  JUMP_FORWARD        172  'to 172'
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
            172_0  COME_FROM           154  '154'

 L. 867       172  LOAD_FAST                'item'
              174  UNPACK_SEQUENCE_2     2 
              176  STORE_FAST               'success'
              178  STORE_FAST               'value'

 L. 868       180  LOAD_FAST                'success'
              182  POP_JUMP_IF_FALSE   188  'to 188'

 L. 869       184  LOAD_FAST                'value'
              186  RETURN_VALUE     
            188_0  COME_FROM           182  '182'

 L. 870       188  LOAD_FAST                'value'
              190  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 28

    __next__ = next

    def _set--- This code section failed: ---

 L. 875         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cond
                4  SETUP_WITH          162  'to 162'
                6  POP_TOP          

 L. 876         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _index
               12  LOAD_FAST                'i'
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE   110  'to 110'

 L. 877        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _items
               22  LOAD_METHOD              append
               24  LOAD_FAST                'obj'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 878        30  LOAD_FAST                'self'
               32  DUP_TOP          
               34  LOAD_ATTR                _index
               36  LOAD_CONST               1
               38  INPLACE_ADD      
               40  ROT_TWO          
               42  STORE_ATTR               _index
             44_0  COME_FROM            96  '96'

 L. 879        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _index
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _unsorted
               52  <118>                 0  ''
               54  POP_JUMP_IF_FALSE    98  'to 98'

 L. 880        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _unsorted
               60  LOAD_METHOD              pop
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _index
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'obj'

 L. 881        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _items
               74  LOAD_METHOD              append
               76  LOAD_FAST                'obj'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 882        82  LOAD_FAST                'self'
               84  DUP_TOP          
               86  LOAD_ATTR                _index
               88  LOAD_CONST               1
               90  INPLACE_ADD      
               92  ROT_TWO          
               94  STORE_ATTR               _index
               96  JUMP_BACK            44  'to 44'
             98_0  COME_FROM            54  '54'

 L. 883        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _cond
              102  LOAD_METHOD              notify
              104  CALL_METHOD_0         0  ''
              106  POP_TOP          
              108  JUMP_FORWARD        120  'to 120'
            110_0  COME_FROM            16  '16'

 L. 885       110  LOAD_FAST                'obj'
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _unsorted
              116  LOAD_FAST                'i'
              118  STORE_SUBSCR     
            120_0  COME_FROM           108  '108'

 L. 887       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _index
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _length
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   148  'to 148'

 L. 888       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _cache
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _job
              140  DELETE_SUBSCR    

 L. 889       142  LOAD_CONST               None
              144  LOAD_FAST                'self'
              146  STORE_ATTR               _pool
            148_0  COME_FROM           130  '130'
              148  POP_BLOCK        
              150  LOAD_CONST               None
              152  DUP_TOP          
              154  DUP_TOP          
              156  CALL_FUNCTION_3       3  ''
              158  POP_TOP          
              160  JUMP_FORWARD        178  'to 178'
            162_0  COME_FROM_WITH        4  '4'
              162  <49>             
              164  POP_JUMP_IF_TRUE    168  'to 168'
              166  <48>             
            168_0  COME_FROM           164  '164'
              168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          
              174  POP_EXCEPT       
              176  POP_TOP          
            178_0  COME_FROM           160  '160'

Parse error at or near `<118>' instruction at offset 52

    def _set_length--- This code section failed: ---

 L. 892         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cond
                4  SETUP_WITH           66  'to 66'
                6  POP_TOP          

 L. 893         8  LOAD_FAST                'length'
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _length

 L. 894        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _index
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _length
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    52  'to 52'

 L. 895        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _cond
               30  LOAD_METHOD              notify
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          

 L. 896        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _cache
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _job
               44  DELETE_SUBSCR    

 L. 897        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _pool
             52_0  COME_FROM            24  '24'
               52  POP_BLOCK        
               54  LOAD_CONST               None
               56  DUP_TOP          
               58  DUP_TOP          
               60  CALL_FUNCTION_3       3  ''
               62  POP_TOP          
               64  JUMP_FORWARD         82  'to 82'
             66_0  COME_FROM_WITH        4  '4'
               66  <49>             
               68  POP_JUMP_IF_TRUE     72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          
               78  POP_EXCEPT       
               80  POP_TOP          
             82_0  COME_FROM            64  '64'

Parse error at or near `DUP_TOP' instruction at offset 56


class IMapUnorderedIterator(IMapIterator):

    def _set--- This code section failed: ---

 L. 906         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cond
                4  SETUP_WITH           86  'to 86'
                6  POP_TOP          

 L. 907         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _items
               12  LOAD_METHOD              append
               14  LOAD_FAST                'obj'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L. 908        20  LOAD_FAST                'self'
               22  DUP_TOP          
               24  LOAD_ATTR                _index
               26  LOAD_CONST               1
               28  INPLACE_ADD      
               30  ROT_TWO          
               32  STORE_ATTR               _index

 L. 909        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _cond
               38  LOAD_METHOD              notify
               40  CALL_METHOD_0         0  ''
               42  POP_TOP          

 L. 910        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _index
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _length
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    72  'to 72'

 L. 911        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _cache
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _job
               64  DELETE_SUBSCR    

 L. 912        66  LOAD_CONST               None
               68  LOAD_FAST                'self'
               70  STORE_ATTR               _pool
             72_0  COME_FROM            54  '54'
               72  POP_BLOCK        
               74  LOAD_CONST               None
               76  DUP_TOP          
               78  DUP_TOP          
               80  CALL_FUNCTION_3       3  ''
               82  POP_TOP          
               84  JUMP_FORWARD        102  'to 102'
             86_0  COME_FROM_WITH        4  '4'
               86  <49>             
               88  POP_JUMP_IF_TRUE     92  'to 92'
               90  <48>             
             92_0  COME_FROM            88  '88'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          
               98  POP_EXCEPT       
              100  POP_TOP          
            102_0  COME_FROM            84  '84'

Parse error at or near `DUP_TOP' instruction at offset 76


class ThreadPool(Pool):
    _wrap_exception = False

    @staticmethod
    def Process--- This code section failed: ---

 L. 923         0  LOAD_CONST               1
                2  LOAD_CONST               ('Process',)
                4  IMPORT_NAME              dummy
                6  IMPORT_FROM              Process
                8  STORE_FAST               'Process'
               10  POP_TOP          

 L. 924        12  LOAD_FAST                'Process'
               14  LOAD_FAST                'args'
               16  BUILD_MAP_0           0 
               18  LOAD_FAST                'kwds'
               20  <164>                 1  ''
               22  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 20

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
    def _help_stuff_finish--- This code section failed: ---

 L. 945         0  SETUP_FINALLY        20  'to 20'
              2_0  COME_FROM            14  '14'

 L. 947         2  LOAD_FAST                'inqueue'
                4  LOAD_ATTR                get
                6  LOAD_CONST               False
                8  LOAD_CONST               ('block',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_TOP          
               14  JUMP_BACK             2  'to 2'
               16  POP_BLOCK        
               18  JUMP_FORWARD         40  'to 40'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 948        20  DUP_TOP          
               22  LOAD_GLOBAL              queue
               24  LOAD_ATTR                Empty
               26  <121>                38  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 949        34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'
             40_1  COME_FROM            18  '18'

 L. 950        40  LOAD_GLOBAL              range
               42  LOAD_FAST                'size'
               44  CALL_FUNCTION_1       1  ''
               46  GET_ITER         
             48_0  COME_FROM            62  '62'
               48  FOR_ITER             64  'to 64'
               50  STORE_FAST               'i'

 L. 951        52  LOAD_FAST                'inqueue'
               54  LOAD_METHOD              put
               56  LOAD_CONST               None
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  JUMP_BACK            48  'to 48'
             64_0  COME_FROM            48  '48'

Parse error at or near `<121>' instruction at offset 26

    def _wait_for_updates(self, sentinels, change_notifier, timeout):
        time.sleep(timeout)