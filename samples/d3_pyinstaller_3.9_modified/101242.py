# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: importlib\_bootstrap.py
"""Core implementation of import.

This module is NOT meant to be directly imported! It has been designed such
that it can be bootstrapped into Python as the implementation of import. As
such it requires the injection of specific modules and attributes in order to
work. One should use importlib as the public-facing version of this module.

"""
_bootstrap_external = None

def _wrap(new, old):
    """Simple substitute for functools.update_wrapper."""
    for replace in ('__module__', '__name__', '__qualname__', '__doc__'):
        if hasattr(old, replace):
            setattr(new, replace, getattr(old, replace))
    else:
        new.__dict__.update(old.__dict__)


def _new_module(name):
    return type(sys)(name)


_module_locks = {}
_blocking_on = {}

class _DeadlockError(RuntimeError):
    pass


class _ModuleLock:
    __doc__ = 'A recursive lock implementation which is able to detect deadlocks\n    (e.g. thread 1 trying to take locks A then B, and thread 2 trying to\n    take locks B then A).\n    '

    def __init__(self, name):
        self.lock = _thread.allocate_lock()
        self.wakeup = _thread.allocate_lock()
        self.name = name
        self.owner = None
        self.count = 0
        self.waiters = 0

    def has_deadlock--- This code section failed: ---

 L.  68         0  LOAD_GLOBAL              _thread
                2  LOAD_METHOD              get_ident
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'me'

 L.  69         8  LOAD_FAST                'self'
               10  LOAD_ATTR                owner
               12  STORE_FAST               'tid'

 L.  70        14  LOAD_GLOBAL              set
               16  CALL_FUNCTION_0       0  ''
               18  STORE_FAST               'seen'
             20_0  COME_FROM            82  '82'

 L.  72        20  LOAD_GLOBAL              _blocking_on
               22  LOAD_METHOD              get
               24  LOAD_FAST                'tid'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'lock'

 L.  73        30  LOAD_FAST                'lock'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L.  74        38  LOAD_CONST               False
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'

 L.  75        42  LOAD_FAST                'lock'
               44  LOAD_ATTR                owner
               46  STORE_FAST               'tid'

 L.  76        48  LOAD_FAST                'tid'
               50  LOAD_FAST                'me'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L.  77        56  LOAD_CONST               True
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L.  78        60  LOAD_FAST                'tid'
               62  LOAD_FAST                'seen'
               64  <118>                 0  ''
               66  POP_JUMP_IF_FALSE    72  'to 72'

 L.  84        68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            66  '66'

 L.  85        72  LOAD_FAST                'seen'
               74  LOAD_METHOD              add
               76  LOAD_FAST                'tid'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  JUMP_BACK            20  'to 20'

Parse error at or near `<117>' instruction at offset 34

    def acquire--- This code section failed: ---

 L.  93         0  LOAD_GLOBAL              _thread
                2  LOAD_METHOD              get_ident
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'tid'

 L.  94         8  LOAD_FAST                'self'
               10  LOAD_GLOBAL              _blocking_on
               12  LOAD_FAST                'tid'
               14  STORE_SUBSCR     

 L.  95        16  SETUP_FINALLY       198  'to 198'
             18_0  COME_FROM           186  '186'

 L.  97        18  LOAD_FAST                'self'
               20  LOAD_ATTR                lock
               22  SETUP_WITH          150  'to 150'
               24  POP_TOP          

 L.  98        26  LOAD_FAST                'self'
               28  LOAD_ATTR                count
               30  LOAD_CONST               0
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_TRUE     46  'to 46'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                owner
               40  LOAD_FAST                'tid'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    90  'to 90'
             46_0  COME_FROM            34  '34'

 L.  99        46  LOAD_FAST                'tid'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               owner

 L. 100        52  LOAD_FAST                'self'
               54  DUP_TOP          
               56  LOAD_ATTR                count
               58  LOAD_CONST               1
               60  INPLACE_ADD      
               62  ROT_TWO          
               64  STORE_ATTR               count

 L. 101        66  POP_BLOCK        
               68  LOAD_CONST               None
               70  DUP_TOP          
               72  DUP_TOP          
               74  CALL_FUNCTION_3       3  ''
               76  POP_TOP          
               78  POP_BLOCK        

 L. 110        80  LOAD_GLOBAL              _blocking_on
               82  LOAD_FAST                'tid'
               84  DELETE_SUBSCR    

 L. 101        86  LOAD_CONST               True
               88  RETURN_VALUE     
             90_0  COME_FROM            44  '44'

 L. 102        90  LOAD_FAST                'self'
               92  LOAD_METHOD              has_deadlock
               94  CALL_METHOD_0         0  ''
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 103        98  LOAD_GLOBAL              _DeadlockError
              100  LOAD_STR                 'deadlock detected by %r'
              102  LOAD_FAST                'self'
              104  BINARY_MODULO    
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM            96  '96'

 L. 104       110  LOAD_FAST                'self'
              112  LOAD_ATTR                wakeup
              114  LOAD_METHOD              acquire
              116  LOAD_CONST               False
              118  CALL_METHOD_1         1  ''
              120  POP_JUMP_IF_FALSE   136  'to 136'

 L. 105       122  LOAD_FAST                'self'
              124  DUP_TOP          
              126  LOAD_ATTR                waiters
              128  LOAD_CONST               1
              130  INPLACE_ADD      
              132  ROT_TWO          
              134  STORE_ATTR               waiters
            136_0  COME_FROM           120  '120'
              136  POP_BLOCK        
              138  LOAD_CONST               None
              140  DUP_TOP          
              142  DUP_TOP          
              144  CALL_FUNCTION_3       3  ''
              146  POP_TOP          
              148  JUMP_FORWARD        166  'to 166'
            150_0  COME_FROM_WITH       22  '22'
              150  <49>             
              152  POP_JUMP_IF_TRUE    156  'to 156'
              154  <48>             
            156_0  COME_FROM           152  '152'
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          
              162  POP_EXCEPT       
              164  POP_TOP          
            166_0  COME_FROM           148  '148'

 L. 107       166  LOAD_FAST                'self'
              168  LOAD_ATTR                wakeup
              170  LOAD_METHOD              acquire
              172  CALL_METHOD_0         0  ''
              174  POP_TOP          

 L. 108       176  LOAD_FAST                'self'
              178  LOAD_ATTR                wakeup
              180  LOAD_METHOD              release
              182  CALL_METHOD_0         0  ''
              184  POP_TOP          
              186  JUMP_BACK            18  'to 18'
              188  POP_BLOCK        

 L. 110       190  LOAD_GLOBAL              _blocking_on
              192  LOAD_FAST                'tid'
              194  DELETE_SUBSCR    
              196  JUMP_FORWARD        206  'to 206'
            198_0  COME_FROM_FINALLY    16  '16'
              198  LOAD_GLOBAL              _blocking_on
              200  LOAD_FAST                'tid'
              202  DELETE_SUBSCR    
              204  <48>             
            206_0  COME_FROM           196  '196'

Parse error at or near `LOAD_CONST' instruction at offset 68

    def release--- This code section failed: ---

 L. 113         0  LOAD_GLOBAL              _thread
                2  LOAD_METHOD              get_ident
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'tid'

 L. 114         8  LOAD_FAST                'self'
               10  LOAD_ATTR                lock
               12  SETUP_WITH          122  'to 122'
               14  POP_TOP          

 L. 115        16  LOAD_FAST                'self'
               18  LOAD_ATTR                owner
               20  LOAD_FAST                'tid'
               22  COMPARE_OP               !=
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 116        26  LOAD_GLOBAL              RuntimeError
               28  LOAD_STR                 'cannot release un-acquired lock'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 117        34  LOAD_FAST                'self'
               36  LOAD_ATTR                count
               38  LOAD_CONST               0
               40  COMPARE_OP               >
               42  POP_JUMP_IF_TRUE     48  'to 48'
               44  <74>             
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'

 L. 118        48  LOAD_FAST                'self'
               50  DUP_TOP          
               52  LOAD_ATTR                count
               54  LOAD_CONST               1
               56  INPLACE_SUBTRACT 
               58  ROT_TWO          
               60  STORE_ATTR               count

 L. 119        62  LOAD_FAST                'self'
               64  LOAD_ATTR                count
               66  LOAD_CONST               0
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE   108  'to 108'

 L. 120        72  LOAD_CONST               None
               74  LOAD_FAST                'self'
               76  STORE_ATTR               owner

 L. 121        78  LOAD_FAST                'self'
               80  LOAD_ATTR                waiters
               82  POP_JUMP_IF_FALSE   108  'to 108'

 L. 122        84  LOAD_FAST                'self'
               86  DUP_TOP          
               88  LOAD_ATTR                waiters
               90  LOAD_CONST               1
               92  INPLACE_SUBTRACT 
               94  ROT_TWO          
               96  STORE_ATTR               waiters

 L. 123        98  LOAD_FAST                'self'
              100  LOAD_ATTR                wakeup
              102  LOAD_METHOD              release
              104  CALL_METHOD_0         0  ''
              106  POP_TOP          
            108_0  COME_FROM            82  '82'
            108_1  COME_FROM            70  '70'
              108  POP_BLOCK        
              110  LOAD_CONST               None
              112  DUP_TOP          
              114  DUP_TOP          
              116  CALL_FUNCTION_3       3  ''
              118  POP_TOP          
              120  JUMP_FORWARD        138  'to 138'
            122_0  COME_FROM_WITH       12  '12'
              122  <49>             
              124  POP_JUMP_IF_TRUE    128  'to 128'
              126  <48>             
            128_0  COME_FROM           124  '124'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          
              134  POP_EXCEPT       
              136  POP_TOP          
            138_0  COME_FROM           120  '120'

Parse error at or near `<74>' instruction at offset 44

    def __repr__(self):
        return '_ModuleLock({!r}) at {}'.format(self.name, id(self))


class _DummyModuleLock:
    __doc__ = 'A simple _ModuleLock equivalent for Python builds without\n    multi-threading support.'

    def __init__(self, name):
        self.name = name
        self.count = 0

    def acquire(self):
        self.count += 1
        return True

    def release(self):
        if self.count == 0:
            raise RuntimeError('cannot release un-acquired lock')
        self.count -= 1

    def __repr__(self):
        return '_DummyModuleLock({!r}) at {}'.format(self.name, id(self))


class _ModuleLockManager:

    def __init__(self, name):
        self._name = name
        self._lock = None

    def __enter__(self):
        self._lock = _get_module_lock(self._name)
        self._lock.acquire()

    def __exit__(self, *args, **kwargs):
        self._lock.release()


def _get_module_lock--- This code section failed: ---

 L. 172         0  LOAD_GLOBAL              _imp
                2  LOAD_METHOD              acquire_lock
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 173         8  SETUP_FINALLY       122  'to 122'

 L. 174        10  SETUP_FINALLY        26  'to 26'

 L. 175        12  LOAD_GLOBAL              _module_locks
               14  LOAD_FAST                'name'
               16  BINARY_SUBSCR    
               18  CALL_FUNCTION_0       0  ''
               20  STORE_FAST               'lock'
               22  POP_BLOCK        
               24  JUMP_FORWARD         48  'to 48'
             26_0  COME_FROM_FINALLY    10  '10'

 L. 176        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  <121>                46  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 177        38  LOAD_CONST               None
               40  STORE_FAST               'lock'
               42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            24  '24'

 L. 179        48  LOAD_FAST                'lock'
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE   110  'to 110'

 L. 180        56  LOAD_GLOBAL              _thread
               58  LOAD_CONST               None
               60  <117>                 0  ''
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L. 181        64  LOAD_GLOBAL              _DummyModuleLock
               66  LOAD_FAST                'name'
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'lock'
               72  JUMP_FORWARD         82  'to 82'
             74_0  COME_FROM            62  '62'

 L. 183        74  LOAD_GLOBAL              _ModuleLock
               76  LOAD_FAST                'name'
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'lock'
             82_0  COME_FROM            72  '72'

 L. 185        82  LOAD_FAST                'name'
               84  BUILD_TUPLE_1         1 
               86  LOAD_CODE                <code_object cb>
               88  LOAD_STR                 '_get_module_lock.<locals>.cb'
               90  MAKE_FUNCTION_1          'default'
               92  STORE_FAST               'cb'

 L. 196        94  LOAD_GLOBAL              _weakref
               96  LOAD_METHOD              ref
               98  LOAD_FAST                'lock'
              100  LOAD_FAST                'cb'
              102  CALL_METHOD_2         2  ''
              104  LOAD_GLOBAL              _module_locks
              106  LOAD_FAST                'name'
              108  STORE_SUBSCR     
            110_0  COME_FROM            54  '54'
              110  POP_BLOCK        

 L. 198       112  LOAD_GLOBAL              _imp
              114  LOAD_METHOD              release_lock
              116  CALL_METHOD_0         0  ''
              118  POP_TOP          
              120  JUMP_FORWARD        132  'to 132'
            122_0  COME_FROM_FINALLY     8  '8'
              122  LOAD_GLOBAL              _imp
              124  LOAD_METHOD              release_lock
              126  CALL_METHOD_0         0  ''
              128  POP_TOP          
              130  <48>             
            132_0  COME_FROM           120  '120'

 L. 200       132  LOAD_FAST                'lock'
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 30


def _lock_unlock_module--- This code section failed: ---

 L. 209         0  LOAD_GLOBAL              _get_module_lock
                2  LOAD_FAST                'name'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'lock'

 L. 210         8  SETUP_FINALLY        22  'to 22'

 L. 211        10  LOAD_FAST                'lock'
               12  LOAD_METHOD              acquire
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
               18  POP_BLOCK        
               20  JUMP_FORWARD         40  'to 40'
             22_0  COME_FROM_FINALLY     8  '8'

 L. 212        22  DUP_TOP          
               24  LOAD_GLOBAL              _DeadlockError
               26  <121>                38  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 215        34  POP_EXCEPT       
               36  JUMP_FORWARD         48  'to 48'
               38  <48>             
             40_0  COME_FROM            20  '20'

 L. 217        40  LOAD_FAST                'lock'
               42  LOAD_METHOD              release
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          
             48_0  COME_FROM            36  '36'

Parse error at or near `<121>' instruction at offset 26


def _call_with_frames_removed--- This code section failed: ---

 L. 228         0  LOAD_FAST                'f'
                2  LOAD_FAST                'args'
                4  BUILD_MAP_0           0 
                6  LOAD_FAST                'kwds'
                8  <164>                 1  ''
               10  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               12  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _verbose_message(message, *args, verbosity=1):
    """Print the message to stderr if -v/PYTHONVERBOSE is turned on."""
    if sys.flags.verbose >= verbosity:
        if not message.startswith(('#', 'import ')):
            message = '# ' + message
        print((message.format)(*args), file=(sys.stderr))


def _requires_builtin(fxn):
    """Decorator to verify the named module is built-in."""

    def _requires_builtin_wrapper--- This code section failed: ---

 L. 242         0  LOAD_FAST                'fullname'
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                builtin_module_names
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 243        10  LOAD_GLOBAL              ImportError
               12  LOAD_STR                 '{!r} is not a built-in module'
               14  LOAD_METHOD              format
               16  LOAD_FAST                'fullname'
               18  CALL_METHOD_1         1  ''

 L. 244        20  LOAD_FAST                'fullname'

 L. 243        22  LOAD_CONST               ('name',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM             8  '8'

 L. 245        28  LOAD_DEREF               'fxn'
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'fullname'
               34  CALL_FUNCTION_2       2  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    _wrap(_requires_builtin_wrapper, fxn)
    return _requires_builtin_wrapper


def _requires_frozen(fxn):
    """Decorator to verify the named module is frozen."""

    def _requires_frozen_wrapper(self, fullname):
        if not _imp.is_frozen(fullname):
            raise ImportError(('{!r} is not a frozen module'.format(fullname)), name=fullname)
        return fxn(self, fullname)

    _wrap(_requires_frozen_wrapper, fxn)
    return _requires_frozen_wrapper


def _load_module_shim--- This code section failed: ---

 L. 268         0  LOAD_GLOBAL              spec_from_loader
                2  LOAD_FAST                'fullname'
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'spec'

 L. 269        10  LOAD_FAST                'fullname'
               12  LOAD_GLOBAL              sys
               14  LOAD_ATTR                modules
               16  <118>                 0  ''
               18  POP_JUMP_IF_FALSE    50  'to 50'

 L. 270        20  LOAD_GLOBAL              sys
               22  LOAD_ATTR                modules
               24  LOAD_FAST                'fullname'
               26  BINARY_SUBSCR    
               28  STORE_FAST               'module'

 L. 271        30  LOAD_GLOBAL              _exec
               32  LOAD_FAST                'spec'
               34  LOAD_FAST                'module'
               36  CALL_FUNCTION_2       2  ''
               38  POP_TOP          

 L. 272        40  LOAD_GLOBAL              sys
               42  LOAD_ATTR                modules
               44  LOAD_FAST                'fullname'
               46  BINARY_SUBSCR    
               48  RETURN_VALUE     
             50_0  COME_FROM            18  '18'

 L. 274        50  LOAD_GLOBAL              _load
               52  LOAD_FAST                'spec'
               54  CALL_FUNCTION_1       1  ''
               56  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 16


def _module_repr--- This code section failed: ---

 L. 280         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'module'
                4  LOAD_STR                 '__loader__'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'loader'

 L. 281        12  LOAD_GLOBAL              hasattr
               14  LOAD_FAST                'loader'
               16  LOAD_STR                 'module_repr'
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    54  'to 54'

 L. 285        22  SETUP_FINALLY        36  'to 36'

 L. 286        24  LOAD_FAST                'loader'
               26  LOAD_METHOD              module_repr
               28  LOAD_FAST                'module'
               30  CALL_METHOD_1         1  ''
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    22  '22'

 L. 287        36  DUP_TOP          
               38  LOAD_GLOBAL              Exception
               40  <121>                52  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 288        48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
               52  <48>             
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM            20  '20'

 L. 289        54  SETUP_FINALLY        66  'to 66'

 L. 290        56  LOAD_FAST                'module'
               58  LOAD_ATTR                __spec__
               60  STORE_FAST               'spec'
               62  POP_BLOCK        
               64  JUMP_FORWARD         84  'to 84'
             66_0  COME_FROM_FINALLY    54  '54'

 L. 291        66  DUP_TOP          
               68  LOAD_GLOBAL              AttributeError
               70  <121>                82  ''
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 292        78  POP_EXCEPT       
               80  JUMP_FORWARD        100  'to 100'
               82  <48>             
             84_0  COME_FROM            64  '64'

 L. 294        84  LOAD_FAST                'spec'
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 295        92  LOAD_GLOBAL              _module_repr_from_spec
               94  LOAD_FAST                'spec'
               96  CALL_FUNCTION_1       1  ''
               98  RETURN_VALUE     
            100_0  COME_FROM            90  '90'
            100_1  COME_FROM            80  '80'

 L. 299       100  SETUP_FINALLY       112  'to 112'

 L. 300       102  LOAD_FAST                'module'
              104  LOAD_ATTR                __name__
              106  STORE_FAST               'name'
              108  POP_BLOCK        
              110  JUMP_FORWARD        134  'to 134'
            112_0  COME_FROM_FINALLY   100  '100'

 L. 301       112  DUP_TOP          
              114  LOAD_GLOBAL              AttributeError
              116  <121>               132  ''
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 302       124  LOAD_STR                 '?'
              126  STORE_FAST               'name'
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
              132  <48>             
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM           110  '110'

 L. 303       134  SETUP_FINALLY       146  'to 146'

 L. 304       136  LOAD_FAST                'module'
              138  LOAD_ATTR                __file__
              140  STORE_FAST               'filename'
              142  POP_BLOCK        
              144  JUMP_FORWARD        202  'to 202'
            146_0  COME_FROM_FINALLY   134  '134'

 L. 305       146  DUP_TOP          
              148  LOAD_GLOBAL              AttributeError
              150  <121>               200  ''
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 306       158  LOAD_FAST                'loader'
              160  LOAD_CONST               None
              162  <117>                 0  ''
              164  POP_JUMP_IF_FALSE   180  'to 180'

 L. 307       166  LOAD_STR                 '<module {!r}>'
              168  LOAD_METHOD              format
              170  LOAD_FAST                'name'
              172  CALL_METHOD_1         1  ''
              174  ROT_FOUR         
              176  POP_EXCEPT       
              178  RETURN_VALUE     
            180_0  COME_FROM           164  '164'

 L. 309       180  LOAD_STR                 '<module {!r} ({!r})>'
              182  LOAD_METHOD              format
              184  LOAD_FAST                'name'
              186  LOAD_FAST                'loader'
              188  CALL_METHOD_2         2  ''
              190  ROT_FOUR         
              192  POP_EXCEPT       
              194  RETURN_VALUE     
              196  POP_EXCEPT       
              198  JUMP_FORWARD        214  'to 214'
              200  <48>             
            202_0  COME_FROM           144  '144'

 L. 311       202  LOAD_STR                 '<module {!r} from {!r}>'
              204  LOAD_METHOD              format
              206  LOAD_FAST                'name'
              208  LOAD_FAST                'filename'
              210  CALL_METHOD_2         2  ''
              212  RETURN_VALUE     
            214_0  COME_FROM           198  '198'

Parse error at or near `<121>' instruction at offset 40


class ModuleSpec:
    __doc__ = 'The specification for a module, used for loading.\n\n    A module\'s spec is the source for information about the module.  For\n    data associated with the module, including source, use the spec\'s\n    loader.\n\n    `name` is the absolute name of the module.  `loader` is the loader\n    to use when loading the module.  `parent` is the name of the\n    package the module is in.  The parent is derived from the name.\n\n    `is_package` determines if the module is considered a package or\n    not.  On modules this is reflected by the `__path__` attribute.\n\n    `origin` is the specific location used by the loader from which to\n    load the module, if that information is available.  When filename is\n    set, origin will match.\n\n    `has_location` indicates that a spec\'s "origin" reflects a location.\n    When this is True, `__file__` attribute of the module is set.\n\n    `cached` is the location of the cached bytecode file, if any.  It\n    corresponds to the `__cached__` attribute.\n\n    `submodule_search_locations` is the sequence of path entries to\n    search when importing submodules.  If set, is_package should be\n    True--and False otherwise.\n\n    Packages are simply modules that (may) have submodules.  If a spec\n    has a non-None value in `submodule_search_locations`, the import\n    system will consider modules loaded from the spec as packages.\n\n    Only finders (see importlib.abc.MetaPathFinder and\n    importlib.abc.PathEntryFinder) should modify ModuleSpec instances.\n\n    '

    def __init__(self, name, loader, *, origin=None, loader_state=None, is_package=None):
        self.name = name
        self.loader = loader
        self.origin = origin
        self.loader_state = loader_state
        self.submodule_search_locations = [] if is_package else None
        self._set_fileattr = False
        self._cached = None

    def __repr__--- This code section failed: ---

 L. 364         0  LOAD_STR                 'name={!r}'
                2  LOAD_METHOD              format
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                name
                8  CALL_METHOD_1         1  ''

 L. 365        10  LOAD_STR                 'loader={!r}'
               12  LOAD_METHOD              format
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                loader
               18  CALL_METHOD_1         1  ''

 L. 364        20  BUILD_LIST_2          2 
               22  STORE_FAST               'args'

 L. 366        24  LOAD_FAST                'self'
               26  LOAD_ATTR                origin
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    52  'to 52'

 L. 367        34  LOAD_FAST                'args'
               36  LOAD_METHOD              append
               38  LOAD_STR                 'origin={!r}'
               40  LOAD_METHOD              format
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                origin
               46  CALL_METHOD_1         1  ''
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
             52_0  COME_FROM            32  '32'

 L. 368        52  LOAD_FAST                'self'
               54  LOAD_ATTR                submodule_search_locations
               56  LOAD_CONST               None
               58  <117>                 1  ''
               60  POP_JUMP_IF_FALSE    80  'to 80'

 L. 369        62  LOAD_FAST                'args'
               64  LOAD_METHOD              append
               66  LOAD_STR                 'submodule_search_locations={}'
               68  LOAD_METHOD              format

 L. 370        70  LOAD_FAST                'self'
               72  LOAD_ATTR                submodule_search_locations

 L. 369        74  CALL_METHOD_1         1  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
             80_0  COME_FROM            60  '60'

 L. 371        80  LOAD_STR                 '{}({})'
               82  LOAD_METHOD              format
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                __class__
               88  LOAD_ATTR                __name__
               90  LOAD_STR                 ', '
               92  LOAD_METHOD              join
               94  LOAD_FAST                'args'
               96  CALL_METHOD_1         1  ''
               98  CALL_METHOD_2         2  ''
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 30

    def __eq__--- This code section failed: ---

 L. 374         0  LOAD_FAST                'self'
                2  LOAD_ATTR                submodule_search_locations
                4  STORE_FAST               'smsl'

 L. 375         6  SETUP_FINALLY        80  'to 80'

 L. 376         8  LOAD_FAST                'self'
               10  LOAD_ATTR                name
               12  LOAD_FAST                'other'
               14  LOAD_ATTR                name
               16  COMPARE_OP               ==
               18  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 377        20  LOAD_FAST                'self'
               22  LOAD_ATTR                loader
               24  LOAD_FAST                'other'
               26  LOAD_ATTR                loader
               28  COMPARE_OP               ==

 L. 376        30  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 378        32  LOAD_FAST                'self'
               34  LOAD_ATTR                origin
               36  LOAD_FAST                'other'
               38  LOAD_ATTR                origin
               40  COMPARE_OP               ==

 L. 376        42  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 379        44  LOAD_FAST                'smsl'
               46  LOAD_FAST                'other'
               48  LOAD_ATTR                submodule_search_locations
               50  COMPARE_OP               ==

 L. 376        52  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 380        54  LOAD_FAST                'self'
               56  LOAD_ATTR                cached
               58  LOAD_FAST                'other'
               60  LOAD_ATTR                cached
               62  COMPARE_OP               ==

 L. 376        64  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 381        66  LOAD_FAST                'self'
               68  LOAD_ATTR                has_location
               70  LOAD_FAST                'other'
               72  LOAD_ATTR                has_location
               74  COMPARE_OP               ==
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            52  '52'
             76_2  COME_FROM            42  '42'
             76_3  COME_FROM            30  '30'
             76_4  COME_FROM            18  '18'

 L. 376        76  POP_BLOCK        
               78  RETURN_VALUE     
             80_0  COME_FROM_FINALLY     6  '6'

 L. 382        80  DUP_TOP          
               82  LOAD_GLOBAL              AttributeError
               84  <121>               100  ''
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 383        92  LOAD_GLOBAL              NotImplemented
               94  ROT_FOUR         
               96  POP_EXCEPT       
               98  RETURN_VALUE     
              100  <48>             

Parse error at or near `<121>' instruction at offset 84

    @property
    def cached--- This code section failed: ---

 L. 387         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cached
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    52  'to 52'

 L. 388        10  LOAD_FAST                'self'
               12  LOAD_ATTR                origin
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    52  'to 52'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _set_fileattr
               24  POP_JUMP_IF_FALSE    52  'to 52'

 L. 389        26  LOAD_GLOBAL              _bootstrap_external
               28  LOAD_CONST               None
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 390        34  LOAD_GLOBAL              NotImplementedError
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            32  '32'

 L. 391        38  LOAD_GLOBAL              _bootstrap_external
               40  LOAD_METHOD              _get_cached
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                origin
               46  CALL_METHOD_1         1  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _cached
             52_0  COME_FROM            24  '24'
             52_1  COME_FROM            18  '18'
             52_2  COME_FROM             8  '8'

 L. 392        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _cached
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @cached.setter
    def cached(self, cached):
        self._cached = cached

    @property
    def parent--- This code section failed: ---

 L. 401         0  LOAD_FAST                'self'
                2  LOAD_ATTR                submodule_search_locations
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 402        10  LOAD_FAST                'self'
               12  LOAD_ATTR                name
               14  LOAD_METHOD              rpartition
               16  LOAD_STR                 '.'
               18  CALL_METHOD_1         1  ''
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  RETURN_VALUE     
             26_0  COME_FROM             8  '8'

 L. 404        26  LOAD_FAST                'self'
               28  LOAD_ATTR                name
               30  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    @property
    def has_location(self):
        return self._set_fileattr

    @has_location.setter
    def has_location(self, value):
        self._set_fileattr = bool(value)


def spec_from_loader--- This code section failed: ---

 L. 417         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'loader'
                4  LOAD_STR                 'get_filename'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    74  'to 74'

 L. 418        10  LOAD_GLOBAL              _bootstrap_external
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 419        18  LOAD_GLOBAL              NotImplementedError
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            16  '16'

 L. 420        22  LOAD_GLOBAL              _bootstrap_external
               24  LOAD_ATTR                spec_from_file_location
               26  STORE_FAST               'spec_from_file_location'

 L. 422        28  LOAD_FAST                'is_package'
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    48  'to 48'

 L. 423        36  LOAD_FAST                'spec_from_file_location'
               38  LOAD_FAST                'name'
               40  LOAD_FAST                'loader'
               42  LOAD_CONST               ('loader',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  RETURN_VALUE     
             48_0  COME_FROM            34  '34'

 L. 424        48  LOAD_FAST                'is_package'
               50  POP_JUMP_IF_FALSE    56  'to 56'
               52  BUILD_LIST_0          0 
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            50  '50'
               56  LOAD_CONST               None
             58_0  COME_FROM            54  '54'
               58  STORE_FAST               'search'

 L. 425        60  LOAD_FAST                'spec_from_file_location'
               62  LOAD_FAST                'name'
               64  LOAD_FAST                'loader'

 L. 426        66  LOAD_FAST                'search'

 L. 425        68  LOAD_CONST               ('loader', 'submodule_search_locations')
               70  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               72  RETURN_VALUE     
             74_0  COME_FROM             8  '8'

 L. 428        74  LOAD_FAST                'is_package'
               76  LOAD_CONST               None
               78  <117>                 0  ''
               80  POP_JUMP_IF_FALSE   136  'to 136'

 L. 429        82  LOAD_GLOBAL              hasattr
               84  LOAD_FAST                'loader'
               86  LOAD_STR                 'is_package'
               88  CALL_FUNCTION_2       2  ''
               90  POP_JUMP_IF_FALSE   132  'to 132'

 L. 430        92  SETUP_FINALLY       108  'to 108'

 L. 431        94  LOAD_FAST                'loader'
               96  LOAD_METHOD              is_package
               98  LOAD_FAST                'name'
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'is_package'
              104  POP_BLOCK        
              106  JUMP_FORWARD        136  'to 136'
            108_0  COME_FROM_FINALLY    92  '92'

 L. 432       108  DUP_TOP          
              110  LOAD_GLOBAL              ImportError
              112  <121>               128  ''
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 433       120  LOAD_CONST               None
              122  STORE_FAST               'is_package'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        136  'to 136'
              128  <48>             
              130  JUMP_FORWARD        136  'to 136'
            132_0  COME_FROM            90  '90'

 L. 436       132  LOAD_CONST               False
              134  STORE_FAST               'is_package'
            136_0  COME_FROM           130  '130'
            136_1  COME_FROM           126  '126'
            136_2  COME_FROM           106  '106'
            136_3  COME_FROM            80  '80'

 L. 438       136  LOAD_GLOBAL              ModuleSpec
              138  LOAD_FAST                'name'
              140  LOAD_FAST                'loader'
              142  LOAD_FAST                'origin'
              144  LOAD_FAST                'is_package'
              146  LOAD_CONST               ('origin', 'is_package')
              148  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


def _spec_from_module--- This code section failed: ---

 L. 443         0  SETUP_FINALLY        12  'to 12'

 L. 444         2  LOAD_FAST                'module'
                4  LOAD_ATTR                __spec__
                6  STORE_FAST               'spec'
                8  POP_BLOCK        
               10  JUMP_FORWARD         30  'to 30'
             12_0  COME_FROM_FINALLY     0  '0'

 L. 445        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  <121>                28  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 446        24  POP_EXCEPT       
               26  JUMP_FORWARD         42  'to 42'
               28  <48>             
             30_0  COME_FROM            10  '10'

 L. 448        30  LOAD_FAST                'spec'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 449        38  LOAD_FAST                'spec'
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'
             42_1  COME_FROM            26  '26'

 L. 451        42  LOAD_FAST                'module'
               44  LOAD_ATTR                __name__
               46  STORE_FAST               'name'

 L. 452        48  LOAD_FAST                'loader'
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    86  'to 86'

 L. 453        56  SETUP_FINALLY        68  'to 68'

 L. 454        58  LOAD_FAST                'module'
               60  LOAD_ATTR                __loader__
               62  STORE_FAST               'loader'
               64  POP_BLOCK        
               66  JUMP_FORWARD         86  'to 86'
             68_0  COME_FROM_FINALLY    56  '56'

 L. 455        68  DUP_TOP          
               70  LOAD_GLOBAL              AttributeError
               72  <121>                84  ''
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 457        80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            66  '66'
             86_2  COME_FROM            54  '54'

 L. 458        86  SETUP_FINALLY        98  'to 98'

 L. 459        88  LOAD_FAST                'module'
               90  LOAD_ATTR                __file__
               92  STORE_FAST               'location'
               94  POP_BLOCK        
               96  JUMP_FORWARD        120  'to 120'
             98_0  COME_FROM_FINALLY    86  '86'

 L. 460        98  DUP_TOP          
              100  LOAD_GLOBAL              AttributeError
              102  <121>               118  ''
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 461       110  LOAD_CONST               None
              112  STORE_FAST               'location'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
              118  <48>             
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            96  '96'

 L. 462       120  LOAD_FAST                'origin'
              122  LOAD_CONST               None
              124  <117>                 0  ''
              126  POP_JUMP_IF_FALSE   176  'to 176'

 L. 463       128  LOAD_FAST                'location'
              130  LOAD_CONST               None
              132  <117>                 0  ''
              134  POP_JUMP_IF_FALSE   172  'to 172'

 L. 464       136  SETUP_FINALLY       148  'to 148'

 L. 465       138  LOAD_FAST                'loader'
              140  LOAD_ATTR                _ORIGIN
              142  STORE_FAST               'origin'
              144  POP_BLOCK        
              146  JUMP_FORWARD        176  'to 176'
            148_0  COME_FROM_FINALLY   136  '136'

 L. 466       148  DUP_TOP          
              150  LOAD_GLOBAL              AttributeError
              152  <121>               168  ''
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L. 467       160  LOAD_CONST               None
              162  STORE_FAST               'origin'
              164  POP_EXCEPT       
              166  JUMP_FORWARD        176  'to 176'
              168  <48>             
              170  JUMP_FORWARD        176  'to 176'
            172_0  COME_FROM           134  '134'

 L. 469       172  LOAD_FAST                'location'
              174  STORE_FAST               'origin'
            176_0  COME_FROM           170  '170'
            176_1  COME_FROM           166  '166'
            176_2  COME_FROM           146  '146'
            176_3  COME_FROM           126  '126'

 L. 470       176  SETUP_FINALLY       188  'to 188'

 L. 471       178  LOAD_FAST                'module'
              180  LOAD_ATTR                __cached__
              182  STORE_FAST               'cached'
              184  POP_BLOCK        
              186  JUMP_FORWARD        210  'to 210'
            188_0  COME_FROM_FINALLY   176  '176'

 L. 472       188  DUP_TOP          
              190  LOAD_GLOBAL              AttributeError
              192  <121>               208  ''
              194  POP_TOP          
              196  POP_TOP          
              198  POP_TOP          

 L. 473       200  LOAD_CONST               None
              202  STORE_FAST               'cached'
              204  POP_EXCEPT       
              206  JUMP_FORWARD        210  'to 210'
              208  <48>             
            210_0  COME_FROM           206  '206'
            210_1  COME_FROM           186  '186'

 L. 474       210  SETUP_FINALLY       226  'to 226'

 L. 475       212  LOAD_GLOBAL              list
              214  LOAD_FAST                'module'
              216  LOAD_ATTR                __path__
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'submodule_search_locations'
              222  POP_BLOCK        
              224  JUMP_FORWARD        248  'to 248'
            226_0  COME_FROM_FINALLY   210  '210'

 L. 476       226  DUP_TOP          
              228  LOAD_GLOBAL              AttributeError
              230  <121>               246  ''
              232  POP_TOP          
              234  POP_TOP          
              236  POP_TOP          

 L. 477       238  LOAD_CONST               None
              240  STORE_FAST               'submodule_search_locations'
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
              246  <48>             
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           224  '224'

 L. 479       248  LOAD_GLOBAL              ModuleSpec
              250  LOAD_FAST                'name'
              252  LOAD_FAST                'loader'
              254  LOAD_FAST                'origin'
              256  LOAD_CONST               ('origin',)
              258  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              260  STORE_FAST               'spec'

 L. 480       262  LOAD_FAST                'location'
              264  LOAD_CONST               None
              266  <117>                 0  ''
          268_270  POP_JUMP_IF_FALSE   276  'to 276'
              272  LOAD_CONST               False
              274  JUMP_FORWARD        278  'to 278'
            276_0  COME_FROM           268  '268'
              276  LOAD_CONST               True
            278_0  COME_FROM           274  '274'
              278  LOAD_FAST                'spec'
              280  STORE_ATTR               _set_fileattr

 L. 481       282  LOAD_FAST                'cached'
              284  LOAD_FAST                'spec'
              286  STORE_ATTR               cached

 L. 482       288  LOAD_FAST                'submodule_search_locations'
              290  LOAD_FAST                'spec'
              292  STORE_ATTR               submodule_search_locations

 L. 483       294  LOAD_FAST                'spec'
              296  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 16


def _init_module_attrs--- This code section failed: ---

 L. 490         0  LOAD_FAST                'override'
                2  POP_JUMP_IF_TRUE     20  'to 20'
                4  LOAD_GLOBAL              getattr
                6  LOAD_FAST                'module'
                8  LOAD_STR                 '__name__'
               10  LOAD_CONST               None
               12  CALL_FUNCTION_3       3  ''
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    52  'to 52'
             20_0  COME_FROM             2  '2'

 L. 491        20  SETUP_FINALLY        34  'to 34'

 L. 492        22  LOAD_FAST                'spec'
               24  LOAD_ATTR                name
               26  LOAD_FAST                'module'
               28  STORE_ATTR               __name__
               30  POP_BLOCK        
               32  JUMP_FORWARD         52  'to 52'
             34_0  COME_FROM_FINALLY    20  '20'

 L. 493        34  DUP_TOP          
               36  LOAD_GLOBAL              AttributeError
               38  <121>                50  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 494        46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM            32  '32'
             52_2  COME_FROM            18  '18'

 L. 496        52  LOAD_FAST                'override'
               54  POP_JUMP_IF_TRUE     72  'to 72'
               56  LOAD_GLOBAL              getattr
               58  LOAD_FAST                'module'
               60  LOAD_STR                 '__loader__'
               62  LOAD_CONST               None
               64  CALL_FUNCTION_3       3  ''
               66  LOAD_CONST               None
               68  <117>                 0  ''
               70  POP_JUMP_IF_FALSE   174  'to 174'
             72_0  COME_FROM            54  '54'

 L. 497        72  LOAD_FAST                'spec'
               74  LOAD_ATTR                loader
               76  STORE_FAST               'loader'

 L. 498        78  LOAD_FAST                'loader'
               80  LOAD_CONST               None
               82  <117>                 0  ''
               84  POP_JUMP_IF_FALSE   144  'to 144'

 L. 500        86  LOAD_FAST                'spec'
               88  LOAD_ATTR                submodule_search_locations
               90  LOAD_CONST               None
               92  <117>                 1  ''
               94  POP_JUMP_IF_FALSE   144  'to 144'

 L. 501        96  LOAD_GLOBAL              _bootstrap_external
               98  LOAD_CONST               None
              100  <117>                 0  ''
              102  POP_JUMP_IF_FALSE   108  'to 108'

 L. 502       104  LOAD_GLOBAL              NotImplementedError
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM           102  '102'

 L. 503       108  LOAD_GLOBAL              _bootstrap_external
              110  LOAD_ATTR                _NamespaceLoader
              112  STORE_FAST               '_NamespaceLoader'

 L. 505       114  LOAD_FAST                '_NamespaceLoader'
              116  LOAD_METHOD              __new__
              118  LOAD_FAST                '_NamespaceLoader'
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'loader'

 L. 506       124  LOAD_FAST                'spec'
              126  LOAD_ATTR                submodule_search_locations
              128  LOAD_FAST                'loader'
              130  STORE_ATTR               _path

 L. 507       132  LOAD_FAST                'loader'
              134  LOAD_FAST                'spec'
              136  STORE_ATTR               loader

 L. 518       138  LOAD_CONST               None
              140  LOAD_FAST                'module'
              142  STORE_ATTR               __file__
            144_0  COME_FROM            94  '94'
            144_1  COME_FROM            84  '84'

 L. 519       144  SETUP_FINALLY       156  'to 156'

 L. 520       146  LOAD_FAST                'loader'
              148  LOAD_FAST                'module'
              150  STORE_ATTR               __loader__
              152  POP_BLOCK        
              154  JUMP_FORWARD        174  'to 174'
            156_0  COME_FROM_FINALLY   144  '144'

 L. 521       156  DUP_TOP          
              158  LOAD_GLOBAL              AttributeError
              160  <121>               172  ''
              162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          

 L. 522       168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
              172  <48>             
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           154  '154'
            174_2  COME_FROM            70  '70'

 L. 524       174  LOAD_FAST                'override'
              176  POP_JUMP_IF_TRUE    194  'to 194'
              178  LOAD_GLOBAL              getattr
              180  LOAD_FAST                'module'
              182  LOAD_STR                 '__package__'
              184  LOAD_CONST               None
              186  CALL_FUNCTION_3       3  ''
              188  LOAD_CONST               None
              190  <117>                 0  ''
              192  POP_JUMP_IF_FALSE   226  'to 226'
            194_0  COME_FROM           176  '176'

 L. 525       194  SETUP_FINALLY       208  'to 208'

 L. 526       196  LOAD_FAST                'spec'
              198  LOAD_ATTR                parent
              200  LOAD_FAST                'module'
              202  STORE_ATTR               __package__
              204  POP_BLOCK        
              206  JUMP_FORWARD        226  'to 226'
            208_0  COME_FROM_FINALLY   194  '194'

 L. 527       208  DUP_TOP          
              210  LOAD_GLOBAL              AttributeError
              212  <121>               224  ''
              214  POP_TOP          
              216  POP_TOP          
              218  POP_TOP          

 L. 528       220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
              224  <48>             
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           206  '206'
            226_2  COME_FROM           192  '192'

 L. 530       226  SETUP_FINALLY       238  'to 238'

 L. 531       228  LOAD_FAST                'spec'
              230  LOAD_FAST                'module'
              232  STORE_ATTR               __spec__
              234  POP_BLOCK        
              236  JUMP_FORWARD        256  'to 256'
            238_0  COME_FROM_FINALLY   226  '226'

 L. 532       238  DUP_TOP          
              240  LOAD_GLOBAL              AttributeError
              242  <121>               254  ''
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          

 L. 533       250  POP_EXCEPT       
              252  JUMP_FORWARD        256  'to 256'
              254  <48>             
            256_0  COME_FROM           252  '252'
            256_1  COME_FROM           236  '236'

 L. 535       256  LOAD_FAST                'override'
          258_260  POP_JUMP_IF_TRUE    280  'to 280'
              262  LOAD_GLOBAL              getattr
              264  LOAD_FAST                'module'
              266  LOAD_STR                 '__path__'
              268  LOAD_CONST               None
              270  CALL_FUNCTION_3       3  ''
              272  LOAD_CONST               None
              274  <117>                 0  ''
          276_278  POP_JUMP_IF_FALSE   326  'to 326'
            280_0  COME_FROM           258  '258'

 L. 536       280  LOAD_FAST                'spec'
              282  LOAD_ATTR                submodule_search_locations
              284  LOAD_CONST               None
              286  <117>                 1  ''
          288_290  POP_JUMP_IF_FALSE   326  'to 326'

 L. 537       292  SETUP_FINALLY       306  'to 306'

 L. 538       294  LOAD_FAST                'spec'
              296  LOAD_ATTR                submodule_search_locations
              298  LOAD_FAST                'module'
              300  STORE_ATTR               __path__
              302  POP_BLOCK        
              304  JUMP_FORWARD        326  'to 326'
            306_0  COME_FROM_FINALLY   292  '292'

 L. 539       306  DUP_TOP          
              308  LOAD_GLOBAL              AttributeError
          310_312  <121>               324  ''
              314  POP_TOP          
              316  POP_TOP          
              318  POP_TOP          

 L. 540       320  POP_EXCEPT       
              322  JUMP_FORWARD        326  'to 326'
              324  <48>             
            326_0  COME_FROM           322  '322'
            326_1  COME_FROM           304  '304'
            326_2  COME_FROM           288  '288'
            326_3  COME_FROM           276  '276'

 L. 542       326  LOAD_FAST                'spec'
              328  LOAD_ATTR                has_location
          330_332  POP_JUMP_IF_FALSE   462  'to 462'

 L. 543       334  LOAD_FAST                'override'
          336_338  POP_JUMP_IF_TRUE    358  'to 358'
              340  LOAD_GLOBAL              getattr
              342  LOAD_FAST                'module'
              344  LOAD_STR                 '__file__'
              346  LOAD_CONST               None
              348  CALL_FUNCTION_3       3  ''
              350  LOAD_CONST               None
              352  <117>                 0  ''
          354_356  POP_JUMP_IF_FALSE   392  'to 392'
            358_0  COME_FROM           336  '336'

 L. 544       358  SETUP_FINALLY       372  'to 372'

 L. 545       360  LOAD_FAST                'spec'
              362  LOAD_ATTR                origin
              364  LOAD_FAST                'module'
              366  STORE_ATTR               __file__
              368  POP_BLOCK        
              370  JUMP_FORWARD        392  'to 392'
            372_0  COME_FROM_FINALLY   358  '358'

 L. 546       372  DUP_TOP          
              374  LOAD_GLOBAL              AttributeError
          376_378  <121>               390  ''
              380  POP_TOP          
              382  POP_TOP          
              384  POP_TOP          

 L. 547       386  POP_EXCEPT       
              388  JUMP_FORWARD        392  'to 392'
              390  <48>             
            392_0  COME_FROM           388  '388'
            392_1  COME_FROM           370  '370'
            392_2  COME_FROM           354  '354'

 L. 549       392  LOAD_FAST                'override'
          394_396  POP_JUMP_IF_TRUE    416  'to 416'
              398  LOAD_GLOBAL              getattr
              400  LOAD_FAST                'module'
              402  LOAD_STR                 '__cached__'
              404  LOAD_CONST               None
              406  CALL_FUNCTION_3       3  ''
              408  LOAD_CONST               None
              410  <117>                 0  ''
          412_414  POP_JUMP_IF_FALSE   462  'to 462'
            416_0  COME_FROM           394  '394'

 L. 550       416  LOAD_FAST                'spec'
              418  LOAD_ATTR                cached
              420  LOAD_CONST               None
              422  <117>                 1  ''
          424_426  POP_JUMP_IF_FALSE   462  'to 462'

 L. 551       428  SETUP_FINALLY       442  'to 442'

 L. 552       430  LOAD_FAST                'spec'
              432  LOAD_ATTR                cached
              434  LOAD_FAST                'module'
              436  STORE_ATTR               __cached__
              438  POP_BLOCK        
              440  JUMP_FORWARD        462  'to 462'
            442_0  COME_FROM_FINALLY   428  '428'

 L. 553       442  DUP_TOP          
              444  LOAD_GLOBAL              AttributeError
          446_448  <121>               460  ''
              450  POP_TOP          
              452  POP_TOP          
              454  POP_TOP          

 L. 554       456  POP_EXCEPT       
              458  JUMP_FORWARD        462  'to 462'
              460  <48>             
            462_0  COME_FROM           458  '458'
            462_1  COME_FROM           440  '440'
            462_2  COME_FROM           424  '424'
            462_3  COME_FROM           412  '412'
            462_4  COME_FROM           330  '330'

 L. 555       462  LOAD_FAST                'module'
              464  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def module_from_spec--- This code section failed: ---

 L. 561         0  LOAD_CONST               None
                2  STORE_FAST               'module'

 L. 562         4  LOAD_GLOBAL              hasattr
                6  LOAD_FAST                'spec'
                8  LOAD_ATTR                loader
               10  LOAD_STR                 'create_module'
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_FALSE    30  'to 30'

 L. 565        16  LOAD_FAST                'spec'
               18  LOAD_ATTR                loader
               20  LOAD_METHOD              create_module
               22  LOAD_FAST                'spec'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'module'
               28  JUMP_FORWARD         50  'to 50'
             30_0  COME_FROM            14  '14'

 L. 566        30  LOAD_GLOBAL              hasattr
               32  LOAD_FAST                'spec'
               34  LOAD_ATTR                loader
               36  LOAD_STR                 'exec_module'
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L. 567        42  LOAD_GLOBAL              ImportError
               44  LOAD_STR                 'loaders that define exec_module() must also define create_module()'
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            40  '40'
             50_1  COME_FROM            28  '28'

 L. 569        50  LOAD_FAST                'module'
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L. 570        58  LOAD_GLOBAL              _new_module
               60  LOAD_FAST                'spec'
               62  LOAD_ATTR                name
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'module'
             68_0  COME_FROM            56  '56'

 L. 571        68  LOAD_GLOBAL              _init_module_attrs
               70  LOAD_FAST                'spec'
               72  LOAD_FAST                'module'
               74  CALL_FUNCTION_2       2  ''
               76  POP_TOP          

 L. 572        78  LOAD_FAST                'module'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 54


def _module_repr_from_spec--- This code section failed: ---

 L. 578         0  LOAD_FAST                'spec'
                2  LOAD_ATTR                name
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'
               10  LOAD_STR                 '?'
               12  JUMP_FORWARD         18  'to 18'
             14_0  COME_FROM             8  '8'
               14  LOAD_FAST                'spec'
               16  LOAD_ATTR                name
             18_0  COME_FROM            12  '12'
               18  STORE_FAST               'name'

 L. 579        20  LOAD_FAST                'spec'
               22  LOAD_ATTR                origin
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    66  'to 66'

 L. 580        30  LOAD_FAST                'spec'
               32  LOAD_ATTR                loader
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    50  'to 50'

 L. 581        40  LOAD_STR                 '<module {!r}>'
               42  LOAD_METHOD              format
               44  LOAD_FAST                'name'
               46  CALL_METHOD_1         1  ''
               48  RETURN_VALUE     
             50_0  COME_FROM            38  '38'

 L. 583        50  LOAD_STR                 '<module {!r} ({!r})>'
               52  LOAD_METHOD              format
               54  LOAD_FAST                'name'
               56  LOAD_FAST                'spec'
               58  LOAD_ATTR                loader
               60  CALL_METHOD_2         2  ''
               62  RETURN_VALUE     
               64  JUMP_FORWARD        102  'to 102'
             66_0  COME_FROM            28  '28'

 L. 585        66  LOAD_FAST                'spec'
               68  LOAD_ATTR                has_location
               70  POP_JUMP_IF_FALSE    86  'to 86'

 L. 586        72  LOAD_STR                 '<module {!r} from {!r}>'
               74  LOAD_METHOD              format
               76  LOAD_FAST                'name'
               78  LOAD_FAST                'spec'
               80  LOAD_ATTR                origin
               82  CALL_METHOD_2         2  ''
               84  RETURN_VALUE     
             86_0  COME_FROM            70  '70'

 L. 588        86  LOAD_STR                 '<module {!r} ({})>'
               88  LOAD_METHOD              format
               90  LOAD_FAST                'spec'
               92  LOAD_ATTR                name
               94  LOAD_FAST                'spec'
               96  LOAD_ATTR                origin
               98  CALL_METHOD_2         2  ''
              100  RETURN_VALUE     
            102_0  COME_FROM            64  '64'

Parse error at or near `None' instruction at offset -1


def _exec--- This code section failed: ---

 L. 594         0  LOAD_FAST                'spec'
                2  LOAD_ATTR                name
                4  STORE_FAST               'name'

 L. 595         6  LOAD_GLOBAL              _ModuleLockManager
                8  LOAD_FAST                'name'
               10  CALL_FUNCTION_1       1  ''
               12  SETUP_WITH          230  'to 230'
               14  POP_TOP          

 L. 596        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                modules
               20  LOAD_METHOD              get
               22  LOAD_FAST                'name'
               24  CALL_METHOD_1         1  ''
               26  LOAD_FAST                'module'
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    54  'to 54'

 L. 597        32  LOAD_STR                 'module {!r} not in sys.modules'
               34  LOAD_METHOD              format
               36  LOAD_FAST                'name'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'msg'

 L. 598        42  LOAD_GLOBAL              ImportError
               44  LOAD_FAST                'msg'
               46  LOAD_FAST                'name'
               48  LOAD_CONST               ('name',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            30  '30'

 L. 599        54  SETUP_FINALLY       188  'to 188'

 L. 600        56  LOAD_FAST                'spec'
               58  LOAD_ATTR                loader
               60  LOAD_CONST               None
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE   106  'to 106'

 L. 601        66  LOAD_FAST                'spec'
               68  LOAD_ATTR                submodule_search_locations
               70  LOAD_CONST               None
               72  <117>                 0  ''
               74  POP_JUMP_IF_FALSE    90  'to 90'

 L. 602        76  LOAD_GLOBAL              ImportError
               78  LOAD_STR                 'missing loader'
               80  LOAD_FAST                'spec'
               82  LOAD_ATTR                name
               84  LOAD_CONST               ('name',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            74  '74'

 L. 604        90  LOAD_GLOBAL              _init_module_attrs
               92  LOAD_FAST                'spec'
               94  LOAD_FAST                'module'
               96  LOAD_CONST               True
               98  LOAD_CONST               ('override',)
              100  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              102  POP_TOP          
              104  JUMP_FORWARD        158  'to 158'
            106_0  COME_FROM            64  '64'

 L. 606       106  LOAD_GLOBAL              _init_module_attrs
              108  LOAD_FAST                'spec'
              110  LOAD_FAST                'module'
              112  LOAD_CONST               True
              114  LOAD_CONST               ('override',)
              116  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              118  POP_TOP          

 L. 607       120  LOAD_GLOBAL              hasattr
              122  LOAD_FAST                'spec'
              124  LOAD_ATTR                loader
              126  LOAD_STR                 'exec_module'
              128  CALL_FUNCTION_2       2  ''
              130  POP_JUMP_IF_TRUE    146  'to 146'

 L. 611       132  LOAD_FAST                'spec'
              134  LOAD_ATTR                loader
              136  LOAD_METHOD              load_module
              138  LOAD_FAST                'name'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_FORWARD        158  'to 158'
            146_0  COME_FROM           130  '130'

 L. 613       146  LOAD_FAST                'spec'
              148  LOAD_ATTR                loader
              150  LOAD_METHOD              exec_module
              152  LOAD_FAST                'module'
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
            158_0  COME_FROM           144  '144'
            158_1  COME_FROM           104  '104'
              158  POP_BLOCK        

 L. 617       160  LOAD_GLOBAL              sys
              162  LOAD_ATTR                modules
              164  LOAD_METHOD              pop
              166  LOAD_FAST                'spec'
              168  LOAD_ATTR                name
              170  CALL_METHOD_1         1  ''
              172  STORE_FAST               'module'

 L. 618       174  LOAD_FAST                'module'
              176  LOAD_GLOBAL              sys
              178  LOAD_ATTR                modules
              180  LOAD_FAST                'spec'
              182  LOAD_ATTR                name
              184  STORE_SUBSCR     
              186  JUMP_FORWARD        216  'to 216'
            188_0  COME_FROM_FINALLY    54  '54'

 L. 617       188  LOAD_GLOBAL              sys
              190  LOAD_ATTR                modules
              192  LOAD_METHOD              pop
              194  LOAD_FAST                'spec'
              196  LOAD_ATTR                name
              198  CALL_METHOD_1         1  ''
              200  STORE_FAST               'module'

 L. 618       202  LOAD_FAST                'module'
              204  LOAD_GLOBAL              sys
              206  LOAD_ATTR                modules
              208  LOAD_FAST                'spec'
              210  LOAD_ATTR                name
              212  STORE_SUBSCR     
              214  <48>             
            216_0  COME_FROM           186  '186'
              216  POP_BLOCK        
              218  LOAD_CONST               None
              220  DUP_TOP          
              222  DUP_TOP          
              224  CALL_FUNCTION_3       3  ''
              226  POP_TOP          
              228  JUMP_FORWARD        246  'to 246'
            230_0  COME_FROM_WITH       12  '12'
              230  <49>             
              232  POP_JUMP_IF_TRUE    236  'to 236'
              234  <48>             
            236_0  COME_FROM           232  '232'
              236  POP_TOP          
              238  POP_TOP          
              240  POP_TOP          
              242  POP_EXCEPT       
              244  POP_TOP          
            246_0  COME_FROM           228  '228'

 L. 619       246  LOAD_FAST                'module'
              248  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28


def _load_backward_compatible--- This code section failed: ---

 L. 626         0  SETUP_FINALLY        20  'to 20'

 L. 627         2  LOAD_FAST                'spec'
                4  LOAD_ATTR                loader
                6  LOAD_METHOD              load_module
                8  LOAD_FAST                'spec'
               10  LOAD_ATTR                name
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          
               16  POP_BLOCK        
               18  JUMP_FORWARD         72  'to 72'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 628        20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 629        26  LOAD_FAST                'spec'
               28  LOAD_ATTR                name
               30  LOAD_GLOBAL              sys
               32  LOAD_ATTR                modules
               34  <118>                 0  ''
               36  POP_JUMP_IF_FALSE    64  'to 64'

 L. 630        38  LOAD_GLOBAL              sys
               40  LOAD_ATTR                modules
               42  LOAD_METHOD              pop
               44  LOAD_FAST                'spec'
               46  LOAD_ATTR                name
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'module'

 L. 631        52  LOAD_FAST                'module'
               54  LOAD_GLOBAL              sys
               56  LOAD_ATTR                modules
               58  LOAD_FAST                'spec'
               60  LOAD_ATTR                name
               62  STORE_SUBSCR     
             64_0  COME_FROM            36  '36'

 L. 632        64  RAISE_VARARGS_0       0  'reraise'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            18  '18'

 L. 635        72  LOAD_GLOBAL              sys
               74  LOAD_ATTR                modules
               76  LOAD_METHOD              pop
               78  LOAD_FAST                'spec'
               80  LOAD_ATTR                name
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'module'

 L. 636        86  LOAD_FAST                'module'
               88  LOAD_GLOBAL              sys
               90  LOAD_ATTR                modules
               92  LOAD_FAST                'spec'
               94  LOAD_ATTR                name
               96  STORE_SUBSCR     

 L. 637        98  LOAD_GLOBAL              getattr
              100  LOAD_FAST                'module'
              102  LOAD_STR                 '__loader__'
              104  LOAD_CONST               None
              106  CALL_FUNCTION_3       3  ''
              108  LOAD_CONST               None
              110  <117>                 0  ''
              112  POP_JUMP_IF_FALSE   146  'to 146'

 L. 638       114  SETUP_FINALLY       128  'to 128'

 L. 639       116  LOAD_FAST                'spec'
              118  LOAD_ATTR                loader
              120  LOAD_FAST                'module'
              122  STORE_ATTR               __loader__
              124  POP_BLOCK        
              126  JUMP_FORWARD        146  'to 146'
            128_0  COME_FROM_FINALLY   114  '114'

 L. 640       128  DUP_TOP          
              130  LOAD_GLOBAL              AttributeError
              132  <121>               144  ''
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 641       140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
              144  <48>             
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM           126  '126'
            146_2  COME_FROM           112  '112'

 L. 642       146  LOAD_GLOBAL              getattr
              148  LOAD_FAST                'module'
              150  LOAD_STR                 '__package__'
              152  LOAD_CONST               None
              154  CALL_FUNCTION_3       3  ''
              156  LOAD_CONST               None
              158  <117>                 0  ''
              160  POP_JUMP_IF_FALSE   222  'to 222'

 L. 643       162  SETUP_FINALLY       204  'to 204'

 L. 647       164  LOAD_FAST                'module'
              166  LOAD_ATTR                __name__
              168  LOAD_FAST                'module'
              170  STORE_ATTR               __package__

 L. 648       172  LOAD_GLOBAL              hasattr
              174  LOAD_FAST                'module'
              176  LOAD_STR                 '__path__'
              178  CALL_FUNCTION_2       2  ''
              180  POP_JUMP_IF_TRUE    200  'to 200'

 L. 649       182  LOAD_FAST                'spec'
              184  LOAD_ATTR                name
              186  LOAD_METHOD              rpartition
              188  LOAD_STR                 '.'
              190  CALL_METHOD_1         1  ''
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  LOAD_FAST                'module'
              198  STORE_ATTR               __package__
            200_0  COME_FROM           180  '180'
              200  POP_BLOCK        
              202  JUMP_FORWARD        222  'to 222'
            204_0  COME_FROM_FINALLY   162  '162'

 L. 650       204  DUP_TOP          
              206  LOAD_GLOBAL              AttributeError
              208  <121>               220  ''
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L. 651       216  POP_EXCEPT       
              218  JUMP_FORWARD        222  'to 222'
              220  <48>             
            222_0  COME_FROM           218  '218'
            222_1  COME_FROM           202  '202'
            222_2  COME_FROM           160  '160'

 L. 652       222  LOAD_GLOBAL              getattr
              224  LOAD_FAST                'module'
              226  LOAD_STR                 '__spec__'
              228  LOAD_CONST               None
              230  CALL_FUNCTION_3       3  ''
              232  LOAD_CONST               None
              234  <117>                 0  ''
          236_238  POP_JUMP_IF_FALSE   272  'to 272'

 L. 653       240  SETUP_FINALLY       252  'to 252'

 L. 654       242  LOAD_FAST                'spec'
              244  LOAD_FAST                'module'
              246  STORE_ATTR               __spec__
              248  POP_BLOCK        
              250  JUMP_FORWARD        272  'to 272'
            252_0  COME_FROM_FINALLY   240  '240'

 L. 655       252  DUP_TOP          
              254  LOAD_GLOBAL              AttributeError
          256_258  <121>               270  ''
              260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          

 L. 656       266  POP_EXCEPT       
              268  JUMP_FORWARD        272  'to 272'
              270  <48>             
            272_0  COME_FROM           268  '268'
            272_1  COME_FROM           250  '250'
            272_2  COME_FROM           236  '236'

 L. 657       272  LOAD_FAST                'module'
              274  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 34


def _load_unlocked--- This code section failed: ---

 L. 661         0  LOAD_FAST                'spec'
                2  LOAD_ATTR                loader
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    30  'to 30'

 L. 663        10  LOAD_GLOBAL              hasattr
               12  LOAD_FAST                'spec'
               14  LOAD_ATTR                loader
               16  LOAD_STR                 'exec_module'
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     30  'to 30'

 L. 664        22  LOAD_GLOBAL              _load_backward_compatible
               24  LOAD_FAST                'spec'
               26  CALL_FUNCTION_1       1  ''
               28  RETURN_VALUE     
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM             8  '8'

 L. 666        30  LOAD_GLOBAL              module_from_spec
               32  LOAD_FAST                'spec'
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'module'

 L. 671        38  LOAD_CONST               True
               40  LOAD_FAST                'spec'
               42  STORE_ATTR               _initializing

 L. 672        44  SETUP_FINALLY       212  'to 212'

 L. 673        46  LOAD_FAST                'module'
               48  LOAD_GLOBAL              sys
               50  LOAD_ATTR                modules
               52  LOAD_FAST                'spec'
               54  LOAD_ATTR                name
               56  STORE_SUBSCR     

 L. 674        58  SETUP_FINALLY       112  'to 112'

 L. 675        60  LOAD_FAST                'spec'
               62  LOAD_ATTR                loader
               64  LOAD_CONST               None
               66  <117>                 0  ''
               68  POP_JUMP_IF_FALSE    96  'to 96'

 L. 676        70  LOAD_FAST                'spec'
               72  LOAD_ATTR                submodule_search_locations
               74  LOAD_CONST               None
               76  <117>                 0  ''
               78  POP_JUMP_IF_FALSE   108  'to 108'

 L. 677        80  LOAD_GLOBAL              ImportError
               82  LOAD_STR                 'missing loader'
               84  LOAD_FAST                'spec'
               86  LOAD_ATTR                name
               88  LOAD_CONST               ('name',)
               90  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               92  RAISE_VARARGS_1       1  'exception instance'
               94  JUMP_FORWARD        108  'to 108'
             96_0  COME_FROM            68  '68'

 L. 680        96  LOAD_FAST                'spec'
               98  LOAD_ATTR                loader
              100  LOAD_METHOD              exec_module
              102  LOAD_FAST                'module'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
            108_0  COME_FROM            94  '94'
            108_1  COME_FROM            78  '78'
              108  POP_BLOCK        
              110  JUMP_FORWARD        160  'to 160'
            112_0  COME_FROM_FINALLY    58  '58'

 L. 681       112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 682       118  SETUP_FINALLY       134  'to 134'

 L. 683       120  LOAD_GLOBAL              sys
              122  LOAD_ATTR                modules
              124  LOAD_FAST                'spec'
              126  LOAD_ATTR                name
              128  DELETE_SUBSCR    
              130  POP_BLOCK        
              132  JUMP_FORWARD        152  'to 152'
            134_0  COME_FROM_FINALLY   118  '118'

 L. 684       134  DUP_TOP          
              136  LOAD_GLOBAL              KeyError
              138  <121>               150  ''
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 685       146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
              150  <48>             
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           132  '132'

 L. 686       152  RAISE_VARARGS_0       0  'reraise'
              154  POP_EXCEPT       
              156  JUMP_FORWARD        160  'to 160'
              158  <48>             
            160_0  COME_FROM           156  '156'
            160_1  COME_FROM           110  '110'

 L. 691       160  LOAD_GLOBAL              sys
              162  LOAD_ATTR                modules
              164  LOAD_METHOD              pop
              166  LOAD_FAST                'spec'
              168  LOAD_ATTR                name
              170  CALL_METHOD_1         1  ''
              172  STORE_FAST               'module'

 L. 692       174  LOAD_FAST                'module'
              176  LOAD_GLOBAL              sys
              178  LOAD_ATTR                modules
              180  LOAD_FAST                'spec'
              182  LOAD_ATTR                name
              184  STORE_SUBSCR     

 L. 693       186  LOAD_GLOBAL              _verbose_message
              188  LOAD_STR                 'import {!r} # {!r}'
              190  LOAD_FAST                'spec'
              192  LOAD_ATTR                name
              194  LOAD_FAST                'spec'
              196  LOAD_ATTR                loader
              198  CALL_FUNCTION_3       3  ''
              200  POP_TOP          
              202  POP_BLOCK        

 L. 695       204  LOAD_CONST               False
              206  LOAD_FAST                'spec'
              208  STORE_ATTR               _initializing
              210  JUMP_FORWARD        220  'to 220'
            212_0  COME_FROM_FINALLY    44  '44'
              212  LOAD_CONST               False
              214  LOAD_FAST                'spec'
              216  STORE_ATTR               _initializing
              218  <48>             
            220_0  COME_FROM           210  '210'

 L. 697       220  LOAD_FAST                'module'
              222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _load--- This code section failed: ---

 L. 710         0  LOAD_GLOBAL              _ModuleLockManager
                2  LOAD_FAST                'spec'
                4  LOAD_ATTR                name
                6  CALL_FUNCTION_1       1  ''
                8  SETUP_WITH           34  'to 34'
               10  POP_TOP          

 L. 711        12  LOAD_GLOBAL              _load_unlocked
               14  LOAD_FAST                'spec'
               16  CALL_FUNCTION_1       1  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  LOAD_CONST               None
               24  DUP_TOP          
               26  DUP_TOP          
               28  CALL_FUNCTION_3       3  ''
               30  POP_TOP          
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        8  '8'
               34  <49>             
               36  POP_JUMP_IF_TRUE     40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          
               46  POP_EXCEPT       
               48  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 22


class BuiltinImporter:
    __doc__ = 'Meta path import for built-in modules.\n\n    All methods are either class or static methods to avoid the need to\n    instantiate the class.\n\n    '
    _ORIGIN = 'built-in'

    @staticmethod
    def module_repr(module):
        """Return repr for the module.

        The method is deprecated.  The import machinery does the job itself.

        """
        return f"<module {module.__name__!r} ({BuiltinImporter._ORIGIN})>"

    @classmethod
    def find_spec--- This code section failed: ---

 L. 738         0  LOAD_FAST                'path'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 739         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 740        12  LOAD_GLOBAL              _imp
               14  LOAD_METHOD              is_builtin
               16  LOAD_FAST                'fullname'
               18  CALL_METHOD_1         1  ''
               20  POP_JUMP_IF_FALSE    38  'to 38'

 L. 741        22  LOAD_GLOBAL              spec_from_loader
               24  LOAD_FAST                'fullname'
               26  LOAD_FAST                'cls'
               28  LOAD_FAST                'cls'
               30  LOAD_ATTR                _ORIGIN
               32  LOAD_CONST               ('origin',)
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  RETURN_VALUE     
             38_0  COME_FROM            20  '20'

 L. 743        38  LOAD_CONST               None
               40  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    @classmethod
    def find_module--- This code section failed: ---

 L. 754         0  LOAD_FAST                'cls'
                2  LOAD_METHOD              find_spec
                4  LOAD_FAST                'fullname'
                6  LOAD_FAST                'path'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'spec'

 L. 755        12  LOAD_FAST                'spec'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    26  'to 26'
               20  LOAD_FAST                'spec'
               22  LOAD_ATTR                loader
               24  RETURN_VALUE     
             26_0  COME_FROM            18  '18'

Parse error at or near `<117>' instruction at offset 16

    @classmethod
    def create_module--- This code section failed: ---

 L. 760         0  LOAD_FAST                'spec'
                2  LOAD_ATTR                name
                4  LOAD_GLOBAL              sys
                6  LOAD_ATTR                builtin_module_names
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    34  'to 34'

 L. 761        12  LOAD_GLOBAL              ImportError
               14  LOAD_STR                 '{!r} is not a built-in module'
               16  LOAD_METHOD              format
               18  LOAD_FAST                'spec'
               20  LOAD_ATTR                name
               22  CALL_METHOD_1         1  ''

 L. 762        24  LOAD_FAST                'spec'
               26  LOAD_ATTR                name

 L. 761        28  LOAD_CONST               ('name',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            10  '10'

 L. 763        34  LOAD_GLOBAL              _call_with_frames_removed
               36  LOAD_GLOBAL              _imp
               38  LOAD_ATTR                create_builtin
               40  LOAD_FAST                'spec'
               42  CALL_FUNCTION_2       2  ''
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def exec_module(self, module):
        """Exec a built-in module"""
        _call_with_frames_removed(_imp.exec_builtin, module)

    @classmethod
    @_requires_builtin
    def get_code(cls, fullname):
        """Return None as built-in modules do not have code objects."""
        pass

    @classmethod
    @_requires_builtin
    def get_source(cls, fullname):
        """Return None as built-in modules do not have source code."""
        pass

    @classmethod
    @_requires_builtin
    def is_package(cls, fullname):
        """Return False as built-in modules are never packages."""
        return False

    load_module = classmethod(_load_module_shim)


class FrozenImporter:
    __doc__ = 'Meta path import for frozen modules.\n\n    All methods are either class or static methods to avoid the need to\n    instantiate the class.\n\n    '
    _ORIGIN = 'frozen'

    @staticmethod
    def module_repr(m):
        """Return repr for the module.

        The method is deprecated.  The import machinery does the job itself.

        """
        return '<module {!r} ({})>'.format(m.__name__, FrozenImporter._ORIGIN)

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if _imp.is_frozen(fullname):
            return spec_from_loader(fullname, cls, origin=(cls._ORIGIN))
        return

    @classmethod
    def find_module(cls, fullname, path=None):
        """Find a frozen module.

        This method is deprecated.  Use find_spec() instead.

        """
        if _imp.is_frozen(fullname):
            return cls

    @classmethod
    def create_module(cls, spec):
        """Use default semantics for module creation."""
        pass

    @staticmethod
    def exec_module(module):
        name = module.__spec__.name
        if not _imp.is_frozen(name):
            raise ImportError(('{!r} is not a frozen module'.format(name)), name=name)
        code = _call_with_frames_removed(_imp.get_frozen_object, name)
        exec(code, module.__dict__)

    @classmethod
    def load_module(cls, fullname):
        """Load a frozen module.

        This method is deprecated.  Use exec_module() instead.

        """
        return _load_module_shim(cls, fullname)

    @classmethod
    @_requires_frozen
    def get_code(cls, fullname):
        """Return the code object for the frozen module."""
        return _imp.get_frozen_object(fullname)

    @classmethod
    @_requires_frozen
    def get_source(cls, fullname):
        """Return None as frozen modules do not have source code."""
        pass

    @classmethod
    @_requires_frozen
    def is_package(cls, fullname):
        """Return True if the frozen module is a package."""
        return _imp.is_frozen_package(fullname)


class _ImportLockContext:
    __doc__ = 'Context manager for the import lock.'

    def __enter__(self):
        """Acquire the import lock."""
        _imp.acquire_lock()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Release the import lock regardless of any raised exceptions."""
        _imp.release_lock()


def _resolve_name(name, package, level):
    """Resolve a relative module name to an absolute one."""
    bits = package.rsplit('.', level - 1)
    if len(bits) < level:
        raise ImportError('attempted relative import beyond top-level package')
    base = bits[0]
    if name:
        return '{}.{}'.format(base, name)
    return base


def _find_spec_legacy--- This code section failed: ---

 L. 895         0  LOAD_FAST                'finder'
                2  LOAD_METHOD              find_module
                4  LOAD_FAST                'name'
                6  LOAD_FAST                'path'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'loader'

 L. 896        12  LOAD_FAST                'loader'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 897        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 898        24  LOAD_GLOBAL              spec_from_loader
               26  LOAD_FAST                'name'
               28  LOAD_FAST                'loader'
               30  CALL_FUNCTION_2       2  ''
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16


def _find_spec--- This code section failed: ---

 L. 903         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                meta_path
                4  STORE_FAST               'meta_path'

 L. 904         6  LOAD_FAST                'meta_path'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 906        14  LOAD_GLOBAL              ImportError
               16  LOAD_STR                 'sys.meta_path is None, Python is likely shutting down'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'

 L. 909        22  LOAD_FAST                'meta_path'
               24  POP_JUMP_IF_TRUE     38  'to 38'

 L. 910        26  LOAD_GLOBAL              _warnings
               28  LOAD_METHOD              warn
               30  LOAD_STR                 'sys.meta_path is empty'
               32  LOAD_GLOBAL              ImportWarning
               34  CALL_METHOD_2         2  ''
               36  POP_TOP          
             38_0  COME_FROM            24  '24'

 L. 915        38  LOAD_FAST                'name'
               40  LOAD_GLOBAL              sys
               42  LOAD_ATTR                modules
               44  <118>                 0  ''
               46  STORE_FAST               'is_reload'

 L. 916        48  LOAD_FAST                'meta_path'
               50  GET_ITER         
             52_0  COME_FROM           282  '282'
             52_1  COME_FROM           272  '272'
             52_2  COME_FROM           178  '178'
             52_3  COME_FROM           122  '122'
               52  FOR_ITER            284  'to 284'
               54  STORE_FAST               'finder'

 L. 917        56  LOAD_GLOBAL              _ImportLockContext
               58  CALL_FUNCTION_0       0  ''
               60  SETUP_WITH          156  'to 156'
               62  POP_TOP          

 L. 918        64  SETUP_FINALLY        76  'to 76'

 L. 919        66  LOAD_FAST                'finder'
               68  LOAD_ATTR                find_spec
               70  STORE_FAST               'find_spec'
               72  POP_BLOCK        
               74  JUMP_FORWARD        130  'to 130'
             76_0  COME_FROM_FINALLY    64  '64'

 L. 920        76  DUP_TOP          
               78  LOAD_GLOBAL              AttributeError
               80  <121>               128  ''
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 921        88  LOAD_GLOBAL              _find_spec_legacy
               90  LOAD_FAST                'finder'
               92  LOAD_FAST                'name'
               94  LOAD_FAST                'path'
               96  CALL_FUNCTION_3       3  ''
               98  STORE_FAST               'spec'

 L. 922       100  LOAD_FAST                'spec'
              102  LOAD_CONST               None
              104  <117>                 0  ''
              106  POP_JUMP_IF_FALSE   124  'to 124'

 L. 923       108  POP_EXCEPT       
              110  POP_BLOCK        
              112  LOAD_CONST               None
              114  DUP_TOP          
              116  DUP_TOP          
              118  CALL_FUNCTION_3       3  ''
              120  POP_TOP          
              122  JUMP_BACK            52  'to 52'
            124_0  COME_FROM           106  '106'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        142  'to 142'
              128  <48>             
            130_0  COME_FROM            74  '74'

 L. 925       130  LOAD_FAST                'find_spec'
              132  LOAD_FAST                'name'
              134  LOAD_FAST                'path'
              136  LOAD_FAST                'target'
              138  CALL_FUNCTION_3       3  ''
              140  STORE_FAST               'spec'
            142_0  COME_FROM           126  '126'
              142  POP_BLOCK        
              144  LOAD_CONST               None
              146  DUP_TOP          
              148  DUP_TOP          
              150  CALL_FUNCTION_3       3  ''
              152  POP_TOP          
              154  JUMP_FORWARD        172  'to 172'
            156_0  COME_FROM_WITH       60  '60'
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

 L. 926       172  LOAD_FAST                'spec'
              174  LOAD_CONST               None
              176  <117>                 1  ''
              178  POP_JUMP_IF_FALSE_BACK    52  'to 52'

 L. 928       180  LOAD_FAST                'is_reload'
          182_184  POP_JUMP_IF_TRUE    274  'to 274'
              186  LOAD_FAST                'name'
              188  LOAD_GLOBAL              sys
              190  LOAD_ATTR                modules
              192  <118>                 0  ''
          194_196  POP_JUMP_IF_FALSE   274  'to 274'

 L. 929       198  LOAD_GLOBAL              sys
              200  LOAD_ATTR                modules
              202  LOAD_FAST                'name'
              204  BINARY_SUBSCR    
              206  STORE_FAST               'module'

 L. 930       208  SETUP_FINALLY       220  'to 220'

 L. 931       210  LOAD_FAST                'module'
              212  LOAD_ATTR                __spec__
              214  STORE_FAST               '__spec__'
              216  POP_BLOCK        
              218  JUMP_FORWARD        246  'to 246'
            220_0  COME_FROM_FINALLY   208  '208'

 L. 932       220  DUP_TOP          
              222  LOAD_GLOBAL              AttributeError
              224  <121>               244  ''
              226  POP_TOP          
              228  POP_TOP          
              230  POP_TOP          

 L. 936       232  LOAD_FAST                'spec'
              234  ROT_FOUR         
              236  POP_EXCEPT       
              238  ROT_TWO          
              240  POP_TOP          
              242  RETURN_VALUE     
              244  <48>             
            246_0  COME_FROM           218  '218'

 L. 938       246  LOAD_FAST                '__spec__'
              248  LOAD_CONST               None
              250  <117>                 0  ''
          252_254  POP_JUMP_IF_FALSE   264  'to 264'

 L. 939       256  LOAD_FAST                'spec'
              258  ROT_TWO          
              260  POP_TOP          
              262  RETURN_VALUE     
            264_0  COME_FROM           252  '252'

 L. 941       264  LOAD_FAST                '__spec__'
              266  ROT_TWO          
              268  POP_TOP          
              270  RETURN_VALUE     
              272  JUMP_BACK            52  'to 52'
            274_0  COME_FROM           194  '194'
            274_1  COME_FROM           182  '182'

 L. 943       274  LOAD_FAST                'spec'
              276  ROT_TWO          
              278  POP_TOP          
              280  RETURN_VALUE     
              282  JUMP_BACK            52  'to 52'
            284_0  COME_FROM            52  '52'

Parse error at or near `<117>' instruction at offset 10


def _sanity_check(name, package, level):
    """Verify arguments are "sane"."""
    if not isinstance(name, str):
        raise TypeError('module name must be str, not {}'.format(type(name)))
    if level < 0:
        raise ValueError('level must be >= 0')
    if level > 0:
        if not isinstance(package, str):
            raise TypeError('__package__ not set to a string')
        elif not package:
            raise ImportError('attempted relative import with no known parent package')
        if not name:
            if level == 0:
                raise ValueError('Empty module name')


_ERR_MSG_PREFIX = 'No module named '
_ERR_MSG = _ERR_MSG_PREFIX + '{!r}'

def _find_and_load_unlocked--- This code section failed: ---

 L. 968         0  LOAD_CONST               None
                2  STORE_FAST               'path'

 L. 969         4  LOAD_FAST                'name'
                6  LOAD_METHOD              rpartition
                8  LOAD_STR                 '.'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'parent'

 L. 970        18  LOAD_FAST                'parent'
               20  POP_JUMP_IF_FALSE   132  'to 132'

 L. 971        22  LOAD_FAST                'parent'
               24  LOAD_GLOBAL              sys
               26  LOAD_ATTR                modules
               28  <118>                 1  ''
               30  POP_JUMP_IF_FALSE    42  'to 42'

 L. 972        32  LOAD_GLOBAL              _call_with_frames_removed
               34  LOAD_FAST                'import_'
               36  LOAD_FAST                'parent'
               38  CALL_FUNCTION_2       2  ''
               40  POP_TOP          
             42_0  COME_FROM            30  '30'

 L. 974        42  LOAD_FAST                'name'
               44  LOAD_GLOBAL              sys
               46  LOAD_ATTR                modules
               48  <118>                 0  ''
               50  POP_JUMP_IF_FALSE    62  'to 62'

 L. 975        52  LOAD_GLOBAL              sys
               54  LOAD_ATTR                modules
               56  LOAD_FAST                'name'
               58  BINARY_SUBSCR    
               60  RETURN_VALUE     
             62_0  COME_FROM            50  '50'

 L. 976        62  LOAD_GLOBAL              sys
               64  LOAD_ATTR                modules
               66  LOAD_FAST                'parent'
               68  BINARY_SUBSCR    
               70  STORE_FAST               'parent_module'

 L. 977        72  SETUP_FINALLY        84  'to 84'

 L. 978        74  LOAD_FAST                'parent_module'
               76  LOAD_ATTR                __path__
               78  STORE_FAST               'path'
               80  POP_BLOCK        
               82  JUMP_FORWARD        132  'to 132'
             84_0  COME_FROM_FINALLY    72  '72'

 L. 979        84  DUP_TOP          
               86  LOAD_GLOBAL              AttributeError
               88  <121>               130  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 980        96  LOAD_GLOBAL              _ERR_MSG
               98  LOAD_STR                 '; {!r} is not a package'
              100  BINARY_ADD       
              102  LOAD_METHOD              format
              104  LOAD_FAST                'name'
              106  LOAD_FAST                'parent'
              108  CALL_METHOD_2         2  ''
              110  STORE_FAST               'msg'

 L. 981       112  LOAD_GLOBAL              ModuleNotFoundError
              114  LOAD_FAST                'msg'
              116  LOAD_FAST                'name'
              118  LOAD_CONST               ('name',)
              120  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              122  LOAD_CONST               None
              124  RAISE_VARARGS_2       2  'exception instance with __cause__'
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
              130  <48>             
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM            82  '82'
            132_2  COME_FROM            20  '20'

 L. 982       132  LOAD_GLOBAL              _find_spec
              134  LOAD_FAST                'name'
              136  LOAD_FAST                'path'
              138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'spec'

 L. 983       142  LOAD_FAST                'spec'
              144  LOAD_CONST               None
              146  <117>                 0  ''
              148  POP_JUMP_IF_FALSE   170  'to 170'

 L. 984       150  LOAD_GLOBAL              ModuleNotFoundError
              152  LOAD_GLOBAL              _ERR_MSG
              154  LOAD_METHOD              format
              156  LOAD_FAST                'name'
              158  CALL_METHOD_1         1  ''
              160  LOAD_FAST                'name'
              162  LOAD_CONST               ('name',)
              164  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              166  RAISE_VARARGS_1       1  'exception instance'
              168  JUMP_FORWARD        178  'to 178'
            170_0  COME_FROM           148  '148'

 L. 986       170  LOAD_GLOBAL              _load_unlocked
              172  LOAD_FAST                'spec'
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'module'
            178_0  COME_FROM           168  '168'

 L. 987       178  LOAD_FAST                'parent'
          180_182  POP_JUMP_IF_FALSE   274  'to 274'

 L. 989       184  LOAD_GLOBAL              sys
              186  LOAD_ATTR                modules
              188  LOAD_FAST                'parent'
              190  BINARY_SUBSCR    
              192  STORE_FAST               'parent_module'

 L. 990       194  LOAD_FAST                'name'
              196  LOAD_METHOD              rpartition
              198  LOAD_STR                 '.'
              200  CALL_METHOD_1         1  ''
              202  LOAD_CONST               2
              204  BINARY_SUBSCR    
              206  STORE_FAST               'child'

 L. 991       208  SETUP_FINALLY       226  'to 226'

 L. 992       210  LOAD_GLOBAL              setattr
              212  LOAD_FAST                'parent_module'
              214  LOAD_FAST                'child'
              216  LOAD_FAST                'module'
              218  CALL_FUNCTION_3       3  ''
              220  POP_TOP          
              222  POP_BLOCK        
              224  JUMP_FORWARD        274  'to 274'
            226_0  COME_FROM_FINALLY   208  '208'

 L. 993       226  DUP_TOP          
              228  LOAD_GLOBAL              AttributeError
          230_232  <121>               272  ''
              234  POP_TOP          
              236  POP_TOP          
              238  POP_TOP          

 L. 994       240  LOAD_STR                 'Cannot set an attribute on '
              242  LOAD_FAST                'parent'
              244  FORMAT_VALUE          2  '!r'
              246  LOAD_STR                 ' for child module '
              248  LOAD_FAST                'child'
              250  FORMAT_VALUE          2  '!r'
              252  BUILD_STRING_4        4 
              254  STORE_FAST               'msg'

 L. 995       256  LOAD_GLOBAL              _warnings
              258  LOAD_METHOD              warn
              260  LOAD_FAST                'msg'
              262  LOAD_GLOBAL              ImportWarning
              264  CALL_METHOD_2         2  ''
              266  POP_TOP          
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
              272  <48>             
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           224  '224'
            274_2  COME_FROM           180  '180'

 L. 996       274  LOAD_FAST                'module'
              276  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 28


_NEEDS_LOADING = object()

def _find_and_load--- This code section failed: ---

 L.1004         0  LOAD_GLOBAL              _ModuleLockManager
                2  LOAD_FAST                'name'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           70  'to 70'
                8  POP_TOP          

 L.1005        10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                modules
               14  LOAD_METHOD              get
               16  LOAD_FAST                'name'
               18  LOAD_GLOBAL              _NEEDS_LOADING
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'module'

 L.1006        24  LOAD_FAST                'module'
               26  LOAD_GLOBAL              _NEEDS_LOADING
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    56  'to 56'

 L.1007        32  LOAD_GLOBAL              _find_and_load_unlocked
               34  LOAD_FAST                'name'
               36  LOAD_FAST                'import_'
               38  CALL_FUNCTION_2       2  ''
               40  POP_BLOCK        
               42  ROT_TWO          
               44  LOAD_CONST               None
               46  DUP_TOP          
               48  DUP_TOP          
               50  CALL_FUNCTION_3       3  ''
               52  POP_TOP          
               54  RETURN_VALUE     
             56_0  COME_FROM            30  '30'
               56  POP_BLOCK        
               58  LOAD_CONST               None
               60  DUP_TOP          
               62  DUP_TOP          
               64  CALL_FUNCTION_3       3  ''
               66  POP_TOP          
               68  JUMP_FORWARD         86  'to 86'
             70_0  COME_FROM_WITH        6  '6'
               70  <49>             
               72  POP_JUMP_IF_TRUE     76  'to 76'
               74  <48>             
             76_0  COME_FROM            72  '72'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          
               82  POP_EXCEPT       
               84  POP_TOP          
             86_0  COME_FROM            68  '68'

 L.1009        86  LOAD_FAST                'module'
               88  LOAD_CONST               None
               90  <117>                 0  ''
               92  POP_JUMP_IF_FALSE   116  'to 116'

 L.1010        94  LOAD_STR                 'import of {} halted; None in sys.modules'
               96  LOAD_METHOD              format

 L.1011        98  LOAD_FAST                'name'

 L.1010       100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'message'

 L.1012       104  LOAD_GLOBAL              ModuleNotFoundError
              106  LOAD_FAST                'message'
              108  LOAD_FAST                'name'
              110  LOAD_CONST               ('name',)
              112  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM            92  '92'

 L.1014       116  LOAD_GLOBAL              _lock_unlock_module
              118  LOAD_FAST                'name'
              120  CALL_FUNCTION_1       1  ''
              122  POP_TOP          

 L.1015       124  LOAD_FAST                'module'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28


def _gcd_import(name, package=None, level=0):
    """Import and return the module based on its name, the package the call is
    being made from, and the level adjustment.

    This function represents the greatest common denominator of functionality
    between import_module and __import__. This includes setting __package__ if
    the loader did not.

    """
    _sanity_check(name, package, level)
    if level > 0:
        name = _resolve_name(name, package, level)
    return _find_and_load(name, _gcd_import)


def _handle_fromlist--- This code section failed: ---

 L.1043         0  LOAD_FAST                'fromlist'
                2  GET_ITER         
              4_0  COME_FROM           226  '226'
              4_1  COME_FROM           214  '214'
              4_2  COME_FROM           200  '200'
              4_3  COME_FROM           146  '146'
              4_4  COME_FROM           116  '116'
              4_5  COME_FROM           106  '106'
              4_6  COME_FROM            64  '64'
                4  FOR_ITER            228  'to 228'
                6  STORE_FAST               'x'

 L.1044         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'x'
               12  LOAD_GLOBAL              str
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     66  'to 66'

 L.1045        18  LOAD_FAST                'recursive'
               20  POP_JUMP_IF_FALSE    34  'to 34'

 L.1046        22  LOAD_FAST                'module'
               24  LOAD_ATTR                __name__
               26  LOAD_STR                 '.__all__'
               28  BINARY_ADD       
               30  STORE_FAST               'where'
               32  JUMP_FORWARD         38  'to 38'
             34_0  COME_FROM            20  '20'

 L.1048        34  LOAD_STR                 "``from list''"
               36  STORE_FAST               'where'
             38_0  COME_FROM            32  '32'

 L.1049        38  LOAD_GLOBAL              TypeError
               40  LOAD_STR                 'Item in '
               42  LOAD_FAST                'where'
               44  FORMAT_VALUE          0  ''
               46  LOAD_STR                 ' must be str, not '

 L.1050        48  LOAD_GLOBAL              type
               50  LOAD_FAST                'x'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_ATTR                __name__

 L.1049        56  FORMAT_VALUE          0  ''
               58  BUILD_STRING_4        4 
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
               64  JUMP_BACK             4  'to 4'
             66_0  COME_FROM            16  '16'

 L.1051        66  LOAD_FAST                'x'
               68  LOAD_STR                 '*'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE   108  'to 108'

 L.1052        74  LOAD_FAST                'recursive'
               76  POP_JUMP_IF_TRUE    226  'to 226'
               78  LOAD_GLOBAL              hasattr
               80  LOAD_FAST                'module'
               82  LOAD_STR                 '__all__'
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   226  'to 226'

 L.1053        88  LOAD_GLOBAL              _handle_fromlist
               90  LOAD_FAST                'module'
               92  LOAD_FAST                'module'
               94  LOAD_ATTR                __all__
               96  LOAD_FAST                'import_'

 L.1054        98  LOAD_CONST               True

 L.1053       100  LOAD_CONST               ('recursive',)
              102  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              104  POP_TOP          
              106  JUMP_BACK             4  'to 4'
            108_0  COME_FROM            72  '72'

 L.1055       108  LOAD_GLOBAL              hasattr
              110  LOAD_FAST                'module'
              112  LOAD_FAST                'x'
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_TRUE_BACK     4  'to 4'

 L.1056       118  LOAD_STR                 '{}.{}'
              120  LOAD_METHOD              format
              122  LOAD_FAST                'module'
              124  LOAD_ATTR                __name__
              126  LOAD_FAST                'x'
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'from_name'

 L.1057       132  SETUP_FINALLY       148  'to 148'

 L.1058       134  LOAD_GLOBAL              _call_with_frames_removed
              136  LOAD_FAST                'import_'
              138  LOAD_FAST                'from_name'
              140  CALL_FUNCTION_2       2  ''
              142  POP_TOP          
              144  POP_BLOCK        
              146  JUMP_BACK             4  'to 4'
            148_0  COME_FROM_FINALLY   132  '132'

 L.1059       148  DUP_TOP          
              150  LOAD_GLOBAL              ModuleNotFoundError
              152  <121>               224  ''
              154  POP_TOP          
              156  STORE_FAST               'exc'
              158  POP_TOP          
              160  SETUP_FINALLY       216  'to 216'

 L.1063       162  LOAD_FAST                'exc'
              164  LOAD_ATTR                name
              166  LOAD_FAST                'from_name'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   202  'to 202'

 L.1064       172  LOAD_GLOBAL              sys
              174  LOAD_ATTR                modules
              176  LOAD_METHOD              get
              178  LOAD_FAST                'from_name'
              180  LOAD_GLOBAL              _NEEDS_LOADING
              182  CALL_METHOD_2         2  ''
              184  LOAD_CONST               None
              186  <117>                 1  ''

 L.1063       188  POP_JUMP_IF_FALSE   202  'to 202'

 L.1065       190  POP_BLOCK        
              192  POP_EXCEPT       
              194  LOAD_CONST               None
              196  STORE_FAST               'exc'
              198  DELETE_FAST              'exc'
              200  JUMP_BACK             4  'to 4'
            202_0  COME_FROM           188  '188'
            202_1  COME_FROM           170  '170'

 L.1066       202  RAISE_VARARGS_0       0  'reraise'
              204  POP_BLOCK        
              206  POP_EXCEPT       
              208  LOAD_CONST               None
              210  STORE_FAST               'exc'
              212  DELETE_FAST              'exc'
              214  JUMP_BACK             4  'to 4'
            216_0  COME_FROM_FINALLY   160  '160'
              216  LOAD_CONST               None
              218  STORE_FAST               'exc'
              220  DELETE_FAST              'exc'
              222  <48>             
              224  <48>             
            226_0  COME_FROM            86  '86'
            226_1  COME_FROM            76  '76'
              226  JUMP_BACK             4  'to 4'
            228_0  COME_FROM             4  '4'

 L.1067       228  LOAD_FAST                'module'
              230  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 152


def _calc___package__--- This code section failed: ---

 L.1077         0  LOAD_FAST                'globals'
                2  LOAD_METHOD              get
                4  LOAD_STR                 '__package__'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'package'

 L.1078        10  LOAD_FAST                'globals'
               12  LOAD_METHOD              get
               14  LOAD_STR                 '__spec__'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'spec'

 L.1079        20  LOAD_FAST                'package'
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    82  'to 82'

 L.1080        28  LOAD_FAST                'spec'
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    78  'to 78'
               36  LOAD_FAST                'package'
               38  LOAD_FAST                'spec'
               40  LOAD_ATTR                parent
               42  COMPARE_OP               !=
               44  POP_JUMP_IF_FALSE    78  'to 78'

 L.1081        46  LOAD_GLOBAL              _warnings
               48  LOAD_ATTR                warn
               50  LOAD_STR                 '__package__ != __spec__.parent ('

 L.1082        52  LOAD_FAST                'package'

 L.1081        54  FORMAT_VALUE          2  '!r'
               56  LOAD_STR                 ' != '

 L.1082        58  LOAD_FAST                'spec'
               60  LOAD_ATTR                parent

 L.1081        62  FORMAT_VALUE          2  '!r'
               64  LOAD_STR                 ')'
               66  BUILD_STRING_5        5 

 L.1083        68  LOAD_GLOBAL              ImportWarning
               70  LOAD_CONST               3

 L.1081        72  LOAD_CONST               ('stacklevel',)
               74  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               76  POP_TOP          
             78_0  COME_FROM            44  '44'
             78_1  COME_FROM            34  '34'

 L.1084        78  LOAD_FAST                'package'
               80  RETURN_VALUE     
             82_0  COME_FROM            26  '26'

 L.1085        82  LOAD_FAST                'spec'
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE    96  'to 96'

 L.1086        90  LOAD_FAST                'spec'
               92  LOAD_ATTR                parent
               94  RETURN_VALUE     
             96_0  COME_FROM            88  '88'

 L.1088        96  LOAD_GLOBAL              _warnings
               98  LOAD_ATTR                warn
              100  LOAD_STR                 "can't resolve package from __spec__ or __package__, falling back on __name__ and __path__"

 L.1090       102  LOAD_GLOBAL              ImportWarning
              104  LOAD_CONST               3

 L.1088       106  LOAD_CONST               ('stacklevel',)
              108  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              110  POP_TOP          

 L.1091       112  LOAD_FAST                'globals'
              114  LOAD_STR                 '__name__'
              116  BINARY_SUBSCR    
              118  STORE_FAST               'package'

 L.1092       120  LOAD_STR                 '__path__'
              122  LOAD_FAST                'globals'
              124  <118>                 1  ''
              126  POP_JUMP_IF_FALSE   142  'to 142'

 L.1093       128  LOAD_FAST                'package'
              130  LOAD_METHOD              rpartition
              132  LOAD_STR                 '.'
              134  CALL_METHOD_1         1  ''
              136  LOAD_CONST               0
              138  BINARY_SUBSCR    
              140  STORE_FAST               'package'
            142_0  COME_FROM           126  '126'

 L.1094       142  LOAD_FAST                'package'
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24


def __import__--- This code section failed: ---

 L.1108         0  LOAD_FAST                'level'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.1109         8  LOAD_GLOBAL              _gcd_import
               10  LOAD_FAST                'name'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'module'
               16  JUMP_FORWARD         54  'to 54'
             18_0  COME_FROM             6  '6'

 L.1111        18  LOAD_FAST                'globals'
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_FALSE    30  'to 30'
               26  LOAD_FAST                'globals'
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            24  '24'
               30  BUILD_MAP_0           0 
             32_0  COME_FROM            28  '28'
               32  STORE_FAST               'globals_'

 L.1112        34  LOAD_GLOBAL              _calc___package__
               36  LOAD_FAST                'globals_'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'package'

 L.1113        42  LOAD_GLOBAL              _gcd_import
               44  LOAD_FAST                'name'
               46  LOAD_FAST                'package'
               48  LOAD_FAST                'level'
               50  CALL_FUNCTION_3       3  ''
               52  STORE_FAST               'module'
             54_0  COME_FROM            16  '16'

 L.1114        54  LOAD_FAST                'fromlist'
               56  POP_JUMP_IF_TRUE    150  'to 150'

 L.1117        58  LOAD_FAST                'level'
               60  LOAD_CONST               0
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    84  'to 84'

 L.1118        66  LOAD_GLOBAL              _gcd_import
               68  LOAD_FAST                'name'
               70  LOAD_METHOD              partition
               72  LOAD_STR                 '.'
               74  CALL_METHOD_1         1  ''
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  CALL_FUNCTION_1       1  ''
               82  RETURN_VALUE     
             84_0  COME_FROM            64  '64'

 L.1119        84  LOAD_FAST                'name'
               86  POP_JUMP_IF_TRUE     92  'to 92'

 L.1120        88  LOAD_FAST                'module'
               90  RETURN_VALUE     
             92_0  COME_FROM            86  '86'

 L.1124        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'name'
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_GLOBAL              len
              100  LOAD_FAST                'name'
              102  LOAD_METHOD              partition
              104  LOAD_STR                 '.'
              106  CALL_METHOD_1         1  ''
              108  LOAD_CONST               0
              110  BINARY_SUBSCR    
              112  CALL_FUNCTION_1       1  ''
              114  BINARY_SUBTRACT  
              116  STORE_FAST               'cut_off'

 L.1127       118  LOAD_GLOBAL              sys
              120  LOAD_ATTR                modules
              122  LOAD_FAST                'module'
              124  LOAD_ATTR                __name__
              126  LOAD_CONST               None
              128  LOAD_GLOBAL              len
              130  LOAD_FAST                'module'
              132  LOAD_ATTR                __name__
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_FAST                'cut_off'
              138  BINARY_SUBTRACT  
              140  BUILD_SLICE_2         2 
              142  BINARY_SUBSCR    
              144  BINARY_SUBSCR    
              146  RETURN_VALUE     
              148  JUMP_FORWARD        176  'to 176'
            150_0  COME_FROM            56  '56'

 L.1128       150  LOAD_GLOBAL              hasattr
              152  LOAD_FAST                'module'
              154  LOAD_STR                 '__path__'
              156  CALL_FUNCTION_2       2  ''
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L.1129       160  LOAD_GLOBAL              _handle_fromlist
              162  LOAD_FAST                'module'
              164  LOAD_FAST                'fromlist'
              166  LOAD_GLOBAL              _gcd_import
              168  CALL_FUNCTION_3       3  ''
              170  RETURN_VALUE     
            172_0  COME_FROM           158  '158'

 L.1131       172  LOAD_FAST                'module'
              174  RETURN_VALUE     
            176_0  COME_FROM           148  '148'

Parse error at or near `<117>' instruction at offset 22


def _builtin_from_name--- This code section failed: ---

 L.1135         0  LOAD_GLOBAL              BuiltinImporter
                2  LOAD_METHOD              find_spec
                4  LOAD_FAST                'name'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'spec'

 L.1136        10  LOAD_FAST                'spec'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    30  'to 30'

 L.1137        18  LOAD_GLOBAL              ImportError
               20  LOAD_STR                 'no built-in module named '
               22  LOAD_FAST                'name'
               24  BINARY_ADD       
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'

 L.1138        30  LOAD_GLOBAL              _load_unlocked
               32  LOAD_FAST                'spec'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


def _setup--- This code section failed: ---

 L.1150         0  LOAD_FAST                '_imp_module'
                2  STORE_GLOBAL             _imp

 L.1151         4  LOAD_FAST                'sys_module'
                6  STORE_GLOBAL             sys

 L.1154         8  LOAD_GLOBAL              type
               10  LOAD_GLOBAL              sys
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'module_type'

 L.1155        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                modules
               20  LOAD_METHOD              items
               22  CALL_METHOD_0         0  ''
               24  GET_ITER         
             26_0  COME_FROM            98  '98'
             26_1  COME_FROM            76  '76'
             26_2  COME_FROM            68  '68'
             26_3  COME_FROM            42  '42'
               26  FOR_ITER            100  'to 100'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'name'
               32  STORE_FAST               'module'

 L.1156        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'module'
               38  LOAD_FAST                'module_type'
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L.1157        44  LOAD_FAST                'name'
               46  LOAD_GLOBAL              sys
               48  LOAD_ATTR                builtin_module_names
               50  <118>                 0  ''
               52  POP_JUMP_IF_FALSE    60  'to 60'

 L.1158        54  LOAD_GLOBAL              BuiltinImporter
               56  STORE_FAST               'loader'
               58  JUMP_FORWARD         78  'to 78'
             60_0  COME_FROM            52  '52'

 L.1159        60  LOAD_GLOBAL              _imp
               62  LOAD_METHOD              is_frozen
               64  LOAD_FAST                'name'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L.1160        70  LOAD_GLOBAL              FrozenImporter
               72  STORE_FAST               'loader'
               74  JUMP_FORWARD         78  'to 78'

 L.1162        76  JUMP_BACK            26  'to 26'
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            58  '58'

 L.1163        78  LOAD_GLOBAL              _spec_from_module
               80  LOAD_FAST                'module'
               82  LOAD_FAST                'loader'
               84  CALL_FUNCTION_2       2  ''
               86  STORE_FAST               'spec'

 L.1164        88  LOAD_GLOBAL              _init_module_attrs
               90  LOAD_FAST                'spec'
               92  LOAD_FAST                'module'
               94  CALL_FUNCTION_2       2  ''
               96  POP_TOP          
               98  JUMP_BACK            26  'to 26'
            100_0  COME_FROM            26  '26'

 L.1167       100  LOAD_GLOBAL              sys
              102  LOAD_ATTR                modules
              104  LOAD_GLOBAL              __name__
              106  BINARY_SUBSCR    
              108  STORE_FAST               'self_module'

 L.1168       110  LOAD_CONST               ('_thread', '_warnings', '_weakref')
              112  GET_ITER         
            114_0  COME_FROM           160  '160'
              114  FOR_ITER            162  'to 162'
              116  STORE_FAST               'builtin_name'

 L.1169       118  LOAD_FAST                'builtin_name'
              120  LOAD_GLOBAL              sys
              122  LOAD_ATTR                modules
              124  <118>                 1  ''
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L.1170       128  LOAD_GLOBAL              _builtin_from_name
              130  LOAD_FAST                'builtin_name'
              132  CALL_FUNCTION_1       1  ''
              134  STORE_FAST               'builtin_module'
              136  JUMP_FORWARD        148  'to 148'
            138_0  COME_FROM           126  '126'

 L.1172       138  LOAD_GLOBAL              sys
              140  LOAD_ATTR                modules
              142  LOAD_FAST                'builtin_name'
              144  BINARY_SUBSCR    
              146  STORE_FAST               'builtin_module'
            148_0  COME_FROM           136  '136'

 L.1173       148  LOAD_GLOBAL              setattr
              150  LOAD_FAST                'self_module'
              152  LOAD_FAST                'builtin_name'
              154  LOAD_FAST                'builtin_module'
              156  CALL_FUNCTION_3       3  ''
              158  POP_TOP          
              160  JUMP_BACK           114  'to 114'
            162_0  COME_FROM           114  '114'

Parse error at or near `<118>' instruction at offset 50


def _install(sys_module, _imp_module):
    """Install importers for builtin and frozen modules"""
    _setup(sys_module, _imp_module)
    sys.meta_path.append(BuiltinImporter)
    sys.meta_path.append(FrozenImporter)


def _install_external_importers():
    """Install importers that require external filesystem access"""
    global _bootstrap_external
    import _frozen_importlib_external
    _bootstrap_external = _frozen_importlib_external
    _frozen_importlib_external._install(sys.modules[__name__])