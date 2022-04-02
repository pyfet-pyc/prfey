# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\thread_util.py
"""Utilities for multi-threading support."""
import threading
try:
    from time import monotonic as _time
except ImportError:
    from time import time as _time
else:
    import pymongo.monotonic as _time
    from pymongo.errors import ExceededMaxWaiters

    class Semaphore:

        def __init__(self, value=1):
            if value < 0:
                raise ValueError('semaphore initial value must be >= 0')
            self._cond = threading.Condition(threading.Lock())
            self._value = value

        def acquire--- This code section failed: ---

 L.  39         0  LOAD_FAST                'blocking'
                2  POP_JUMP_IF_TRUE     20  'to 20'
                4  LOAD_FAST                'timeout'
                6  LOAD_CONST               None
                8  COMPARE_OP               is-not
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  40        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 "can't specify timeout for non-blocking acquire"
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'
             20_1  COME_FROM             2  '2'

 L.  41        20  LOAD_CONST               False
               22  STORE_FAST               'rc'

 L.  42        24  LOAD_CONST               None
               26  STORE_FAST               'endtime'

 L.  43        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _cond
               32  LOAD_METHOD              acquire
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          
             38_0  COME_FROM           114  '114'

 L.  44        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _value
               42  LOAD_CONST               0
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE   116  'to 116'

 L.  45        48  LOAD_FAST                'blocking'
               50  POP_JUMP_IF_TRUE     54  'to 54'

 L.  46        52  JUMP_FORWARD        132  'to 132'
             54_0  COME_FROM            50  '50'

 L.  47        54  LOAD_FAST                'timeout'
               56  LOAD_CONST               None
               58  COMPARE_OP               is-not
               60  POP_JUMP_IF_FALSE   102  'to 102'

 L.  48        62  LOAD_FAST                'endtime'
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  POP_JUMP_IF_FALSE    82  'to 82'

 L.  49        70  LOAD_GLOBAL              _time
               72  CALL_FUNCTION_0       0  ''
               74  LOAD_FAST                'timeout'
               76  BINARY_ADD       
               78  STORE_FAST               'endtime'
               80  JUMP_FORWARD        102  'to 102'
             82_0  COME_FROM            68  '68'

 L.  51        82  LOAD_FAST                'endtime'
               84  LOAD_GLOBAL              _time
               86  CALL_FUNCTION_0       0  ''
               88  BINARY_SUBTRACT  
               90  STORE_FAST               'timeout'

 L.  52        92  LOAD_FAST                'timeout'
               94  LOAD_CONST               0
               96  COMPARE_OP               <=
               98  POP_JUMP_IF_FALSE   102  'to 102'

 L.  53       100  JUMP_FORWARD        132  'to 132'
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            80  '80'
            102_2  COME_FROM            60  '60'

 L.  54       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _cond
              106  LOAD_METHOD              wait
              108  LOAD_FAST                'timeout'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          
              114  JUMP_BACK            38  'to 38'
            116_0  COME_FROM            46  '46'

 L.  56       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _value
              120  LOAD_CONST               1
              122  BINARY_SUBTRACT  
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _value

 L.  57       128  LOAD_CONST               True
              130  STORE_FAST               'rc'
            132_0  COME_FROM           100  '100'
            132_1  COME_FROM            52  '52'

 L.  58       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _cond
              136  LOAD_METHOD              release
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          

 L.  59       142  LOAD_FAST                'rc'
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 144

        __enter__ = acquire

        def release(self):
            self._cond.acquire()
            self._value = self._value + 1
            self._cond.notify()
            self._cond.release()

        def __exit__(self, t, v, tb):
            self.release()

        @property
        def counter(self):
            return self._value


    class BoundedSemaphore(Semaphore):
        __doc__ = 'Semaphore that checks that # releases is <= # acquires'

        def __init__(self, value=1):
            Semaphore.__init__(self, value)
            self._initial_value = value

        def release(self):
            if self._value >= self._initial_value:
                raise ValueError('Semaphore released too many times')
            return Semaphore.release(self)


    class DummySemaphore(object):

        def __init__(self, value=None):
            pass

        def acquire(self, blocking=True, timeout=None):
            return True

        def release(self):
            pass


    class MaxWaitersBoundedSemaphore(object):

        def __init__(self, semaphore_class, value=1, max_waiters=1):
            self.waiter_semaphore = semaphore_class(max_waiters)
            self.semaphore = semaphore_class(value)

        def acquire(self, blocking=True, timeout=None):
            if not self.waiter_semaphore.acquire(False):
                raise ExceededMaxWaiters
            try:
                return self.semaphore.acquire(blocking, timeout)
            finally:
                self.waiter_semaphore.release()

        def __getattr__(self, name):
            return getattr(self.semaphore, name)


    class MaxWaitersBoundedSemaphoreThread(MaxWaitersBoundedSemaphore):

        def __init__(self, value=1, max_waiters=1):
            MaxWaitersBoundedSemaphore.__init__(self, BoundedSemaphore, value, max_waiters)


    def create_semaphore(max_size, max_waiters):
        if max_size is None:
            return DummySemaphore
        if max_waiters is None:
            return BoundedSemaphore(max_size)
        return MaxWaitersBoundedSemaphoreThread(max_size, max_waiters)