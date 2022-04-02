# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\locks.py
"""Synchronization primitives."""
__all__ = ('Lock', 'Event', 'Condition', 'Semaphore', 'BoundedSemaphore')
import collections, warnings
from . import events
from . import exceptions

class _ContextManagerMixin:

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        self.release()


class Lock(_ContextManagerMixin):
    __doc__ = "Primitive lock objects.\n\n    A primitive lock is a synchronization primitive that is not owned\n    by a particular coroutine when locked.  A primitive lock is in one\n    of two states, 'locked' or 'unlocked'.\n\n    It is created in the unlocked state.  It has two basic methods,\n    acquire() and release().  When the state is unlocked, acquire()\n    changes the state to locked and returns immediately.  When the\n    state is locked, acquire() blocks until a call to release() in\n    another coroutine changes it to unlocked, then the acquire() call\n    resets it to locked and returns.  The release() method should only\n    be called in the locked state; it changes the state to unlocked\n    and returns immediately.  If an attempt is made to release an\n    unlocked lock, a RuntimeError will be raised.\n\n    When more than one coroutine is blocked in acquire() waiting for\n    the state to turn to unlocked, only one coroutine proceeds when a\n    release() call resets the state to unlocked; first coroutine which\n    is blocked in acquire() is being processed.\n\n    acquire() is a coroutine and should be called with 'await'.\n\n    Locks also support the asynchronous context management protocol.\n    'async with lock' statement should be used.\n\n    Usage:\n\n        lock = Lock()\n        ...\n        await lock.acquire()\n        try:\n            ...\n        finally:\n            lock.release()\n\n    Context manager usage:\n\n        lock = Lock()\n        ...\n        async with lock:\n             ...\n\n    Lock objects can be tested for locking state:\n\n        if not lock.locked():\n           await lock.acquire()\n        else:\n           # lock is acquired\n           ...\n\n    "

    def __init__--- This code section failed: ---

 L.  78         0  LOAD_CONST               None
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _waiters

 L.  79         6  LOAD_CONST               False
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _locked

 L.  80        12  LOAD_FAST                'loop'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L.  81        20  LOAD_GLOBAL              events
               22  LOAD_METHOD              get_event_loop
               24  CALL_METHOD_0         0  ''
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _loop
               30  JUMP_FORWARD         54  'to 54'
             32_0  COME_FROM            18  '18'

 L.  83        32  LOAD_FAST                'loop'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _loop

 L.  84        38  LOAD_GLOBAL              warnings
               40  LOAD_ATTR                warn
               42  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L.  86        44  LOAD_GLOBAL              DeprecationWarning
               46  LOAD_CONST               2

 L.  84        48  LOAD_CONST               ('stacklevel',)
               50  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               52  POP_TOP          
             54_0  COME_FROM            30  '30'

Parse error at or near `<117>' instruction at offset 16

    def __repr__(self):
        res = super().__repr__()
        extra = 'locked' if self._locked else 'unlocked'
        if self._waiters:
            extra = f"{extra}, waiters:{len(self._waiters)}"
        return f"<{res[1:-1]} [{extra}]>"

    def locked(self):
        """Return True if lock is acquired."""
        return self._locked

    async def acquire--- This code section failed: ---

 L. 105         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _locked
                4  POP_JUMP_IF_TRUE     46  'to 46'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _waiters
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_TRUE     36  'to 36'

 L. 106        16  LOAD_GLOBAL              all
               18  LOAD_GENEXPR             '<code_object <genexpr>>'
               20  LOAD_STR                 'Lock.acquire.<locals>.<genexpr>'
               22  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _waiters
               28  GET_ITER         
               30  CALL_FUNCTION_1       1  ''
               32  CALL_FUNCTION_1       1  ''

 L. 105        34  POP_JUMP_IF_FALSE    46  'to 46'
             36_0  COME_FROM            14  '14'

 L. 107        36  LOAD_CONST               True
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _locked

 L. 108        42  LOAD_CONST               True
               44  RETURN_VALUE     
             46_0  COME_FROM            34  '34'
             46_1  COME_FROM             4  '4'

 L. 110        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _waiters
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    66  'to 66'

 L. 111        56  LOAD_GLOBAL              collections
               58  LOAD_METHOD              deque
               60  CALL_METHOD_0         0  ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _waiters
             66_0  COME_FROM            54  '54'

 L. 112        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _loop
               70  LOAD_METHOD              create_future
               72  CALL_METHOD_0         0  ''
               74  STORE_FAST               'fut'

 L. 113        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _waiters
               80  LOAD_METHOD              append
               82  LOAD_FAST                'fut'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 118        88  SETUP_FINALLY       136  'to 136'

 L. 119        90  SETUP_FINALLY       118  'to 118'

 L. 120        92  LOAD_FAST                'fut'
               94  GET_AWAITABLE    
               96  LOAD_CONST               None
               98  YIELD_FROM       
              100  POP_TOP          
              102  POP_BLOCK        

 L. 122       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _waiters
              108  LOAD_METHOD              remove
              110  LOAD_FAST                'fut'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  JUMP_FORWARD        132  'to 132'
            118_0  COME_FROM_FINALLY    90  '90'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _waiters
              122  LOAD_METHOD              remove
              124  LOAD_FAST                'fut'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
              130  <48>             
            132_0  COME_FROM           116  '116'
              132  POP_BLOCK        
              134  JUMP_FORWARD        172  'to 172'
            136_0  COME_FROM_FINALLY    88  '88'

 L. 123       136  DUP_TOP          
              138  LOAD_GLOBAL              exceptions
              140  LOAD_ATTR                CancelledError
              142  <121>               170  ''
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 124       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _locked
              154  POP_JUMP_IF_TRUE    164  'to 164'

 L. 125       156  LOAD_FAST                'self'
              158  LOAD_METHOD              _wake_up_first
              160  CALL_METHOD_0         0  ''
              162  POP_TOP          
            164_0  COME_FROM           154  '154'

 L. 126       164  RAISE_VARARGS_0       0  'reraise'
              166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
              170  <48>             
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM           134  '134'

 L. 128       172  LOAD_CONST               True
              174  LOAD_FAST                'self'
              176  STORE_ATTR               _locked

 L. 129       178  LOAD_CONST               True
              180  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def release(self):
        """Release a lock.

        When the lock is locked, reset it to unlocked, and return.
        If any other coroutines are blocked waiting for the lock to become
        unlocked, allow exactly one of them to proceed.

        When invoked on an unlocked lock, a RuntimeError is raised.

        There is no return value.
        """
        if self._locked:
            self._locked = False
            self._wake_up_first()
        else:
            raise RuntimeError('Lock is not acquired.')

    def _wake_up_first--- This code section failed: ---

 L. 150         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _waiters
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 151         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 152        10  SETUP_FINALLY        30  'to 30'

 L. 153        12  LOAD_GLOBAL              next
               14  LOAD_GLOBAL              iter
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _waiters
               20  CALL_FUNCTION_1       1  ''
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'fut'
               26  POP_BLOCK        
               28  JUMP_FORWARD         50  'to 50'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 154        30  DUP_TOP          
               32  LOAD_GLOBAL              StopIteration
               34  <121>                48  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 155        42  POP_EXCEPT       
               44  LOAD_CONST               None
               46  RETURN_VALUE     
               48  <48>             
             50_0  COME_FROM            28  '28'

 L. 160        50  LOAD_FAST                'fut'
               52  LOAD_METHOD              done
               54  CALL_METHOD_0         0  ''
               56  POP_JUMP_IF_TRUE     68  'to 68'

 L. 161        58  LOAD_FAST                'fut'
               60  LOAD_METHOD              set_result
               62  LOAD_CONST               True
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
             68_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 34


class Event:
    __doc__ = 'Asynchronous equivalent to threading.Event.\n\n    Class implementing event objects. An event manages a flag that can be set\n    to true with the set() method and reset to false with the clear() method.\n    The wait() method blocks until the flag is true. The flag is initially\n    false.\n    '

    def __init__--- This code section failed: ---

 L. 174         0  LOAD_GLOBAL              collections
                2  LOAD_METHOD              deque
                4  CALL_METHOD_0         0  ''
                6  LOAD_FAST                'self'
                8  STORE_ATTR               _waiters

 L. 175        10  LOAD_CONST               False
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _value

 L. 176        16  LOAD_FAST                'loop'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    36  'to 36'

 L. 177        24  LOAD_GLOBAL              events
               26  LOAD_METHOD              get_event_loop
               28  CALL_METHOD_0         0  ''
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _loop
               34  JUMP_FORWARD         58  'to 58'
             36_0  COME_FROM            22  '22'

 L. 179        36  LOAD_FAST                'loop'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _loop

 L. 180        42  LOAD_GLOBAL              warnings
               44  LOAD_ATTR                warn
               46  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L. 182        48  LOAD_GLOBAL              DeprecationWarning
               50  LOAD_CONST               2

 L. 180        52  LOAD_CONST               ('stacklevel',)
               54  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               56  POP_TOP          
             58_0  COME_FROM            34  '34'

Parse error at or near `<117>' instruction at offset 20

    def __repr__(self):
        res = super().__repr__()
        extra = 'set' if self._value else 'unset'
        if self._waiters:
            extra = f"{extra}, waiters:{len(self._waiters)}"
        return f"<{res[1:-1]} [{extra}]>"

    def is_set(self):
        """Return True if and only if the internal flag is true."""
        return self._value

    def set(self):
        """Set the internal flag to true. All coroutines waiting for it to
        become true are awakened. Coroutine that call wait() once the flag is
        true will not block at all.
        """
        if not self._value:
            self._value = True
            for fut in self._waiters:
                if not fut.done():
                    fut.set_resultTrue

    def clear(self):
        """Reset the internal flag to false. Subsequently, coroutines calling
        wait() will block until set() is called to set the internal flag
        to true again."""
        self._value = False

    async def wait--- This code section failed: ---

 L. 220         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _value
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 221         6  LOAD_CONST               True
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 223        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _loop
               14  LOAD_METHOD              create_future
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'fut'

 L. 224        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _waiters
               24  LOAD_METHOD              append
               26  LOAD_FAST                'fut'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 225        32  SETUP_FINALLY        62  'to 62'

 L. 226        34  LOAD_FAST                'fut'
               36  GET_AWAITABLE    
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  POP_TOP          

 L. 227        44  POP_BLOCK        

 L. 229        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _waiters
               50  LOAD_METHOD              remove
               52  LOAD_FAST                'fut'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 227        58  LOAD_CONST               True
               60  RETURN_VALUE     
             62_0  COME_FROM_FINALLY    32  '32'

 L. 229        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _waiters
               66  LOAD_METHOD              remove
               68  LOAD_FAST                'fut'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  <48>             

Parse error at or near `LOAD_FAST' instruction at offset 46


class Condition(_ContextManagerMixin):
    __doc__ = 'Asynchronous equivalent to threading.Condition.\n\n    This class implements condition variable objects. A condition variable\n    allows one or more coroutines to wait until they are notified by another\n    coroutine.\n\n    A new Lock object is created and used as the underlying lock.\n    '

    def __init__--- This code section failed: ---

 L. 243         0  LOAD_FAST                'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 244         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _loop
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM             6  '6'

 L. 246        20  LOAD_FAST                'loop'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _loop

 L. 247        26  LOAD_GLOBAL              warnings
               28  LOAD_ATTR                warn
               30  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L. 249        32  LOAD_GLOBAL              DeprecationWarning
               34  LOAD_CONST               2

 L. 247        36  LOAD_CONST               ('stacklevel',)
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  POP_TOP          
             42_0  COME_FROM            18  '18'

 L. 251        42  LOAD_FAST                'lock'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L. 252        50  LOAD_GLOBAL              Lock
               52  LOAD_FAST                'loop'
               54  LOAD_CONST               ('loop',)
               56  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               58  STORE_FAST               'lock'
               60  JUMP_FORWARD         82  'to 82'
             62_0  COME_FROM            48  '48'

 L. 253        62  LOAD_FAST                'lock'
               64  LOAD_ATTR                _loop
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _loop
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    82  'to 82'

 L. 254        74  LOAD_GLOBAL              ValueError
               76  LOAD_STR                 'loop argument must agree with lock'
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            72  '72'
             82_1  COME_FROM            60  '60'

 L. 256        82  LOAD_FAST                'lock'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _lock

 L. 258        88  LOAD_FAST                'lock'
               90  LOAD_ATTR                locked
               92  LOAD_FAST                'self'
               94  STORE_ATTR               locked

 L. 259        96  LOAD_FAST                'lock'
               98  LOAD_ATTR                acquire
              100  LOAD_FAST                'self'
              102  STORE_ATTR               acquire

 L. 260       104  LOAD_FAST                'lock'
              106  LOAD_ATTR                release
              108  LOAD_FAST                'self'
              110  STORE_ATTR               release

 L. 262       112  LOAD_GLOBAL              collections
              114  LOAD_METHOD              deque
              116  CALL_METHOD_0         0  ''
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _waiters

Parse error at or near `None' instruction at offset -1

    def __repr__(self):
        res = super().__repr__()
        extra = 'locked' if self.locked() else 'unlocked'
        if self._waiters:
            extra = f"{extra}, waiters:{len(self._waiters)}"
        return f"<{res[1:-1]} [{extra}]>"

    async def wait--- This code section failed: ---

 L. 282         0  LOAD_FAST                'self'
                2  LOAD_METHOD              locked
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L. 283         8  LOAD_GLOBAL              RuntimeError
               10  LOAD_STR                 'cannot wait on un-acquired lock'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 285        16  LOAD_FAST                'self'
               18  LOAD_METHOD              release
               20  CALL_METHOD_0         0  ''
               22  POP_TOP          

 L. 286        24  SETUP_FINALLY       226  'to 226'

 L. 287        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _loop
               30  LOAD_METHOD              create_future
               32  CALL_METHOD_0         0  ''
               34  STORE_FAST               'fut'

 L. 288        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _waiters
               40  LOAD_METHOD              append
               42  LOAD_FAST                'fut'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 289        48  SETUP_FINALLY       144  'to 144'

 L. 290        50  LOAD_FAST                'fut'
               52  GET_AWAITABLE    
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  POP_TOP          

 L. 291        60  POP_BLOCK        

 L. 293        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _waiters
               66  LOAD_METHOD              remove
               68  LOAD_FAST                'fut'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          

 L. 291        74  POP_BLOCK        

 L. 297        76  LOAD_CONST               False
               78  STORE_FAST               'cancelled'

 L. 299        80  SETUP_FINALLY       104  'to 104'

 L. 300        82  LOAD_FAST                'self'
               84  LOAD_METHOD              acquire
               86  CALL_METHOD_0         0  ''
               88  GET_AWAITABLE    
               90  LOAD_CONST               None
               92  YIELD_FROM       
               94  POP_TOP          

 L. 301        96  POP_BLOCK        
               98  BREAK_LOOP          130  'to 130'
              100  POP_BLOCK        
              102  JUMP_BACK            80  'to 80'
            104_0  COME_FROM_FINALLY    80  '80'

 L. 302       104  DUP_TOP          
              106  LOAD_GLOBAL              exceptions
              108  LOAD_ATTR                CancelledError
              110  <121>               126  ''
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 303       118  LOAD_CONST               True
              120  STORE_FAST               'cancelled'
              122  POP_EXCEPT       
              124  JUMP_BACK            80  'to 80'
              126  <48>             
              128  JUMP_BACK            80  'to 80'

 L. 305       130  LOAD_FAST                'cancelled'
              132  POP_JUMP_IF_FALSE   140  'to 140'

 L. 306       134  LOAD_GLOBAL              exceptions
              136  LOAD_ATTR                CancelledError
              138  RAISE_VARARGS_1       1  'exception instance'
            140_0  COME_FROM           132  '132'

 L. 291       140  LOAD_CONST               True
              142  RETURN_VALUE     
            144_0  COME_FROM_FINALLY    48  '48'

 L. 293       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _waiters
              148  LOAD_METHOD              remove
              150  LOAD_FAST                'fut'
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          
              156  <48>             
              158  POP_BLOCK        

 L. 297       160  LOAD_CONST               False
              162  STORE_FAST               'cancelled'

 L. 299       164  SETUP_FINALLY       188  'to 188'

 L. 300       166  LOAD_FAST                'self'
              168  LOAD_METHOD              acquire
              170  CALL_METHOD_0         0  ''
              172  GET_AWAITABLE    
              174  LOAD_CONST               None
              176  YIELD_FROM       
              178  POP_TOP          

 L. 301       180  POP_BLOCK        
              182  BREAK_LOOP          214  'to 214'
              184  POP_BLOCK        
              186  JUMP_BACK           164  'to 164'
            188_0  COME_FROM_FINALLY   164  '164'

 L. 302       188  DUP_TOP          
              190  LOAD_GLOBAL              exceptions
              192  LOAD_ATTR                CancelledError
              194  <121>               210  ''
              196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L. 303       202  LOAD_CONST               True
              204  STORE_FAST               'cancelled'
              206  POP_EXCEPT       
              208  JUMP_BACK           164  'to 164'
              210  <48>             
              212  JUMP_BACK           164  'to 164'

 L. 305       214  LOAD_FAST                'cancelled'
              216  POP_JUMP_IF_FALSE   224  'to 224'

 L. 306       218  LOAD_GLOBAL              exceptions
              220  LOAD_ATTR                CancelledError
              222  RAISE_VARARGS_1       1  'exception instance'
            224_0  COME_FROM           216  '216'
              224  JUMP_FORWARD        298  'to 298'
            226_0  COME_FROM_FINALLY    24  '24'

 L. 297       226  LOAD_CONST               False
              228  STORE_FAST               'cancelled'

 L. 299       230  SETUP_FINALLY       256  'to 256'

 L. 300       232  LOAD_FAST                'self'
              234  LOAD_METHOD              acquire
              236  CALL_METHOD_0         0  ''
              238  GET_AWAITABLE    
              240  LOAD_CONST               None
              242  YIELD_FROM       
              244  POP_TOP          

 L. 301       246  POP_BLOCK        
          248_250  BREAK_LOOP          284  'to 284'
              252  POP_BLOCK        
              254  JUMP_BACK           230  'to 230'
            256_0  COME_FROM_FINALLY   230  '230'

 L. 302       256  DUP_TOP          
              258  LOAD_GLOBAL              exceptions
              260  LOAD_ATTR                CancelledError
          262_264  <121>               280  ''
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L. 303       272  LOAD_CONST               True
              274  STORE_FAST               'cancelled'
              276  POP_EXCEPT       
              278  JUMP_BACK           230  'to 230'
              280  <48>             
              282  JUMP_BACK           230  'to 230'

 L. 305       284  LOAD_FAST                'cancelled'
          286_288  POP_JUMP_IF_FALSE   296  'to 296'

 L. 306       290  LOAD_GLOBAL              exceptions
              292  LOAD_ATTR                CancelledError
              294  RAISE_VARARGS_1       1  'exception instance'
            296_0  COME_FROM           286  '286'
              296  <48>             
            298_0  COME_FROM           224  '224'

Parse error at or near `LOAD_FAST' instruction at offset 62

    async def wait_for(self, predicate):
        """Wait until a predicate becomes true.

        The predicate should be a callable which result will be
        interpreted as a boolean value.  The final predicate value is
        the return value.
        """
        result = predicate()
        while not result:
            await self.wait()
            result = predicate()

        return result

    def notify(self, n=1):
        """By default, wake up one coroutine waiting on this condition, if any.
        If the calling coroutine has not acquired the lock when this method
        is called, a RuntimeError is raised.

        This method wakes up at most n of the coroutines waiting for the
        condition variable; it is a no-op if no coroutines are waiting.

        Note: an awakened coroutine does not actually return from its
        wait() call until it can reacquire the lock. Since notify() does
        not release the lock, its caller should.
        """
        if not self.locked():
            raise RuntimeError('cannot notify on un-acquired lock')
        idx = 0
        for fut in self._waiters:
            if idx >= n:
                break
            if not fut.done():
                idx += 1
                fut.set_resultFalse

    def notify_all(self):
        """Wake up all threads waiting on this condition. This method acts
        like notify(), but wakes up all waiting threads instead of one. If the
        calling thread has not acquired the lock when this method is called,
        a RuntimeError is raised.
        """
        self.notifylen(self._waiters)


class Semaphore(_ContextManagerMixin):
    __doc__ = 'A Semaphore implementation.\n\n    A semaphore manages an internal counter which is decremented by each\n    acquire() call and incremented by each release() call. The counter\n    can never go below zero; when acquire() finds that it is zero, it blocks,\n    waiting until some other thread calls release().\n\n    Semaphores also support the context management protocol.\n\n    The optional argument gives the initial value for the internal\n    counter; it defaults to 1. If the value given is less than 0,\n    ValueError is raised.\n    '

    def __init__--- This code section failed: ---

 L. 370         0  LOAD_FAST                'value'
                2  LOAD_CONST               0
                4  COMPARE_OP               <
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 371         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Semaphore initial value must be >= 0'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 372        16  LOAD_FAST                'value'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _value

 L. 373        22  LOAD_GLOBAL              collections
               24  LOAD_METHOD              deque
               26  CALL_METHOD_0         0  ''
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _waiters

 L. 374        32  LOAD_FAST                'loop'
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 375        40  LOAD_GLOBAL              events
               42  LOAD_METHOD              get_event_loop
               44  CALL_METHOD_0         0  ''
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _loop
               50  JUMP_FORWARD         74  'to 74'
             52_0  COME_FROM            38  '38'

 L. 377        52  LOAD_FAST                'loop'
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _loop

 L. 378        58  LOAD_GLOBAL              warnings
               60  LOAD_ATTR                warn
               62  LOAD_STR                 'The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.'

 L. 380        64  LOAD_GLOBAL              DeprecationWarning
               66  LOAD_CONST               2

 L. 378        68  LOAD_CONST               ('stacklevel',)
               70  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               72  POP_TOP          
             74_0  COME_FROM            50  '50'

Parse error at or near `<117>' instruction at offset 36

    def __repr__(self):
        res = super().__repr__()
        extra = 'locked' if self.locked() else f"unlocked, value:{self._value}"
        if self._waiters:
            extra = f"{extra}, waiters:{len(self._waiters)}"
        return f"<{res[1:-1]} [{extra}]>"

    def _wake_up_next(self):
        while self._waiters:
            waiter = self._waiters.popleft()
            if not waiter.done():
                waiter.set_resultNone
                return None

    def locked(self):
        """Returns True if semaphore can not be acquired immediately."""
        return self._value == 0

    async def acquire--- This code section failed: ---

 L. 409         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _value
                4  LOAD_CONST               0
                6  COMPARE_OP               <=
                8  POP_JUMP_IF_FALSE    98  'to 98'

 L. 410        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _loop
               14  LOAD_METHOD              create_future
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'fut'

 L. 411        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _waiters
               24  LOAD_METHOD              append
               26  LOAD_FAST                'fut'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 412        32  SETUP_FINALLY        48  'to 48'

 L. 413        34  LOAD_FAST                'fut'
               36  GET_AWAITABLE    
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  POP_TOP          
               44  POP_BLOCK        
               46  JUMP_BACK             0  'to 0'
             48_0  COME_FROM_FINALLY    32  '32'

 L. 414        48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 416        54  LOAD_FAST                'fut'
               56  LOAD_METHOD              cancel
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          

 L. 417        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _value
               66  LOAD_CONST               0
               68  COMPARE_OP               >
               70  POP_JUMP_IF_FALSE    88  'to 88'
               72  LOAD_FAST                'fut'
               74  LOAD_METHOD              cancelled
               76  CALL_METHOD_0         0  ''
               78  POP_JUMP_IF_TRUE     88  'to 88'

 L. 418        80  LOAD_FAST                'self'
               82  LOAD_METHOD              _wake_up_next
               84  CALL_METHOD_0         0  ''
               86  POP_TOP          
             88_0  COME_FROM            78  '78'
             88_1  COME_FROM            70  '70'

 L. 419        88  RAISE_VARARGS_0       0  'reraise'
               90  POP_EXCEPT       
               92  JUMP_BACK             0  'to 0'
               94  <48>             
               96  JUMP_BACK             0  'to 0'
             98_0  COME_FROM             8  '8'

 L. 420        98  LOAD_FAST                'self'
              100  DUP_TOP          
              102  LOAD_ATTR                _value
              104  LOAD_CONST               1
              106  INPLACE_SUBTRACT 
              108  ROT_TWO          
              110  STORE_ATTR               _value

 L. 421       112  LOAD_CONST               True
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<48>' instruction at offset 94

    def release(self):
        """Release a semaphore, incrementing the internal counter by one.
        When it was zero on entry and another coroutine is waiting for it to
        become larger than zero again, wake up that coroutine.
        """
        self._value += 1
        self._wake_up_next()


class BoundedSemaphore(Semaphore):
    __doc__ = 'A bounded semaphore implementation.\n\n    This raises ValueError in release() if it would increase the value\n    above the initial value.\n    '

    def __init__(self, value=1, *, loop=None):
        if loop:
            warnings.warn('The loop argument is deprecated since Python 3.8, and scheduled for removal in Python 3.10.', DeprecationWarning,
              stacklevel=2)
        self._bound_value = value
        super().__init__(value, loop=loop)

    def release(self):
        if self._value >= self._bound_value:
            raise ValueError('BoundedSemaphore released too many times')
        super().release()