# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multiprocessing\context.py
import os, sys, threading
from . import process
from . import reduction
__all__ = ()

class ProcessError(Exception):
    pass


class BufferTooShort(ProcessError):
    pass


class TimeoutError(ProcessError):
    pass


class AuthenticationError(ProcessError):
    pass


class BaseContext(object):
    ProcessError = ProcessError
    BufferTooShort = BufferTooShort
    TimeoutError = TimeoutError
    AuthenticationError = AuthenticationError
    current_process = staticmethod(process.current_process)
    parent_process = staticmethod(process.parent_process)
    active_children = staticmethod(process.active_children)

    def cpu_count--- This code section failed: ---

 L.  43         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              cpu_count
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'num'

 L.  44         8  LOAD_FAST                'num'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L.  45        16  LOAD_GLOBAL              NotImplementedError
               18  LOAD_STR                 'cannot determine number of cpus'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
               24  JUMP_FORWARD         30  'to 30'
             26_0  COME_FROM            14  '14'

 L.  47        26  LOAD_FAST                'num'
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

Parse error at or near `<117>' instruction at offset 12

    def Manager(self):
        """Returns a manager associated with a running server process

        The managers methods such as `Lock()`, `Condition()` and `Queue()`
        can be used to create shared objects.
        """
        from .managers import SyncManager
        m = SyncManager(ctx=(self.get_context()))
        m.start()
        return m

    def Pipe(self, duplex=True):
        """Returns two connection object connected by a pipe"""
        from .connection import Pipe
        return Pipe(duplex)

    def Lock(self):
        """Returns a non-recursive lock object"""
        from .synchronize import Lock
        return Lock(ctx=(self.get_context()))

    def RLock(self):
        """Returns a recursive lock object"""
        from .synchronize import RLock
        return RLock(ctx=(self.get_context()))

    def Condition(self, lock=None):
        """Returns a condition object"""
        from .synchronize import Condition
        return Condition(lock, ctx=(self.get_context()))

    def Semaphore(self, value=1):
        """Returns a semaphore object"""
        from .synchronize import Semaphore
        return Semaphore(value, ctx=(self.get_context()))

    def BoundedSemaphore(self, value=1):
        """Returns a bounded semaphore object"""
        from .synchronize import BoundedSemaphore
        return BoundedSemaphore(value, ctx=(self.get_context()))

    def Event(self):
        """Returns an event object"""
        from .synchronize import Event
        return Event(ctx=(self.get_context()))

    def Barrier(self, parties, action=None, timeout=None):
        """Returns a barrier object"""
        from .synchronize import Barrier
        return Barrier(parties, action, timeout, ctx=(self.get_context()))

    def Queue(self, maxsize=0):
        """Returns a queue object"""
        from .queues import Queue
        return Queue(maxsize, ctx=(self.get_context()))

    def JoinableQueue(self, maxsize=0):
        """Returns a queue object"""
        from .queues import JoinableQueue
        return JoinableQueue(maxsize, ctx=(self.get_context()))

    def SimpleQueue(self):
        """Returns a queue object"""
        from .queues import SimpleQueue
        return SimpleQueue(ctx=(self.get_context()))

    def Pool(self, processes=None, initializer=None, initargs=(), maxtasksperchild=None):
        """Returns a process pool object"""
        from .pool import Pool
        return Pool(processes, initializer, initargs, maxtasksperchild, context=(self.get_context()))

    def RawValue--- This code section failed: ---

 L. 124         0  LOAD_CONST               1
                2  LOAD_CONST               ('RawValue',)
                4  IMPORT_NAME              sharedctypes
                6  IMPORT_FROM              RawValue
                8  STORE_FAST               'RawValue'
               10  POP_TOP          

 L. 125        12  LOAD_FAST                'RawValue'
               14  LOAD_FAST                'typecode_or_type'
               16  BUILD_LIST_1          1 
               18  LOAD_FAST                'args'
               20  CALL_FINALLY         23  'to 23'
               22  WITH_CLEANUP_FINISH
               24  CALL_FUNCTION_EX      0  'positional arguments only'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 20

    def RawArray(self, typecode_or_type, size_or_initializer):
        """Returns a shared array"""
        from .sharedctypes import RawArray
        return RawArray(typecode_or_type, size_or_initializer)

    def Value--- This code section failed: ---

 L. 134         0  LOAD_CONST               1
                2  LOAD_CONST               ('Value',)
                4  IMPORT_NAME              sharedctypes
                6  IMPORT_FROM              Value
                8  STORE_FAST               'Value'
               10  POP_TOP          

 L. 135        12  LOAD_FAST                'Value'
               14  LOAD_FAST                'typecode_or_type'
               16  BUILD_LIST_1          1 
               18  LOAD_FAST                'args'
               20  CALL_FINALLY         23  'to 23'
               22  WITH_CLEANUP_FINISH
               24  LOAD_FAST                'lock'

 L. 136        26  LOAD_FAST                'self'
               28  LOAD_METHOD              get_context
               30  CALL_METHOD_0         0  ''

 L. 135        32  LOAD_CONST               ('lock', 'ctx')
               34  BUILD_CONST_KEY_MAP_2     2 
               36  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 20

    def Array(self, typecode_or_type, size_or_initializer, *, lock=True):
        """Returns a synchronized shared array"""
        from .sharedctypes import Array
        return Array(typecode_or_type, size_or_initializer, lock=lock, ctx=(self.get_context()))

    def freeze_support(self):
        """Check whether this is a fake forked process in a frozen executable.
        If so then run code specified by commandline and exit.
        """
        if sys.platform == 'win32':
            if getattr(sys, 'frozen', False):
                from .spawn import freeze_support
                freeze_support()

    def get_logger(self):
        """Return package logger -- if it does not already exist then
        it is created.
        """
        from .util import get_logger
        return get_logger()

    def log_to_stderr(self, level=None):
        """Turn on logging and add a handler which prints to stderr"""
        from .util import log_to_stderr
        return log_to_stderr(level)

    def allow_connection_pickling(self):
        """Install support for sending connections and sockets
        between processes
        """
        from . import connection

    def set_executable(self, executable):
        """Sets the path to a python.exe or pythonw.exe binary used to run
        child processes instead of sys.executable when using the 'spawn'
        start method.  Useful for people embedding Python.
        """
        from .spawn import set_executable
        set_executable(executable)

    def set_forkserver_preload(self, module_names):
        """Set list of module names to try to load in forkserver process.
        This is really just a hint.
        """
        from .forkserver import set_forkserver_preload
        set_forkserver_preload(module_names)

    def get_context--- This code section failed: ---

 L. 188         0  LOAD_FAST                'method'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 189         8  LOAD_FAST                'self'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 190        12  SETUP_FINALLY        26  'to 26'

 L. 191        14  LOAD_GLOBAL              _concrete_contexts
               16  LOAD_FAST                'method'
               18  BINARY_SUBSCR    
               20  STORE_FAST               'ctx'
               22  POP_BLOCK        
               24  JUMP_FORWARD         58  'to 58'
             26_0  COME_FROM_FINALLY    12  '12'

 L. 192        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  <121>                56  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 193        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'cannot find context for %r'
               42  LOAD_FAST                'method'
               44  BINARY_MODULO    
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_CONST               None
               50  RAISE_VARARGS_2       2  'exception instance with __cause__'
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            24  '24'

 L. 194        58  LOAD_FAST                'ctx'
               60  LOAD_METHOD              _check_available
               62  CALL_METHOD_0         0  ''
               64  POP_TOP          

 L. 195        66  LOAD_FAST                'ctx'
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def get_start_method(self, allow_none=False):
        return self._name

    def set_start_method(self, method, force=False):
        raise ValueError('cannot set start method of concrete context')

    @property
    def reducer(self):
        """Controls how objects will be reduced to a form that can be
        shared with other processes."""
        return globals().get('reduction')

    @reducer.setter
    def reducer(self, reduction):
        globals()['reduction'] = reduction

    def _check_available(self):
        pass


class Process(process.BaseProcess):
    _start_method = None

    @staticmethod
    def _Popen(process_obj):
        return _default_context.get_context().Process._Popen(process_obj)


class DefaultContext(BaseContext):
    Process = Process

    def __init__(self, context):
        self._default_context = context
        self._actual_context = None

    def get_context--- This code section failed: ---

 L. 234         0  LOAD_FAST                'method'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    32  'to 32'

 L. 235         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _actual_context
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 236        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _default_context
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _actual_context
             26_0  COME_FROM            16  '16'

 L. 237        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _actual_context
               30  RETURN_VALUE     
             32_0  COME_FROM             6  '6'

 L. 239        32  LOAD_GLOBAL              super
               34  CALL_FUNCTION_0       0  ''
               36  LOAD_METHOD              get_context
               38  LOAD_FAST                'method'
               40  CALL_METHOD_1         1  ''
               42  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def set_start_method--- This code section failed: ---

 L. 242         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _actual_context
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'
               10  LOAD_FAST                'force'
               12  POP_JUMP_IF_TRUE     22  'to 22'

 L. 243        14  LOAD_GLOBAL              RuntimeError
               16  LOAD_STR                 'context has already been set'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'
             22_1  COME_FROM             8  '8'

 L. 244        22  LOAD_FAST                'method'
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    44  'to 44'
               30  LOAD_FAST                'force'
               32  POP_JUMP_IF_FALSE    44  'to 44'

 L. 245        34  LOAD_CONST               None
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _actual_context

 L. 246        40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            32  '32'
             44_1  COME_FROM            28  '28'

 L. 247        44  LOAD_FAST                'self'
               46  LOAD_METHOD              get_context
               48  LOAD_FAST                'method'
               50  CALL_METHOD_1         1  ''
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _actual_context

Parse error at or near `None' instruction at offset -1

    def get_start_method--- This code section failed: ---

 L. 250         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _actual_context
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 251        10  LOAD_FAST                'allow_none'
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 252        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 253        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _default_context
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _actual_context
             26_0  COME_FROM             8  '8'

 L. 254        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _actual_context
               30  LOAD_ATTR                _name
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def get_all_start_methods(self):
        if sys.platform == 'win32':
            return ['spawn']
        methods = ['spawn', 'fork'] if sys.platform == 'darwin' else ['fork', 'spawn']
        if reduction.HAVE_SEND_HANDLE:
            methods.append('forkserver')
        return methods


if sys.platform != 'win32':

    class ForkProcess(process.BaseProcess):
        _start_method = 'fork'

        @staticmethod
        def _Popen(process_obj):
            from .popen_fork import Popen
            return Popen(process_obj)


    class SpawnProcess(process.BaseProcess):
        _start_method = 'spawn'

        @staticmethod
        def _Popen(process_obj):
            from .popen_spawn_posix import Popen
            return Popen(process_obj)


    class ForkServerProcess(process.BaseProcess):
        _start_method = 'forkserver'

        @staticmethod
        def _Popen(process_obj):
            from .popen_forkserver import Popen
            return Popen(process_obj)


    class ForkContext(BaseContext):
        _name = 'fork'
        Process = ForkProcess


    class SpawnContext(BaseContext):
        _name = 'spawn'
        Process = SpawnProcess


    class ForkServerContext(BaseContext):
        _name = 'forkserver'
        Process = ForkServerProcess

        def _check_available(self):
            if not reduction.HAVE_SEND_HANDLE:
                raise ValueError('forkserver start method not available')


    _concrete_contexts = {'fork':ForkContext(), 
     'spawn':SpawnContext(), 
     'forkserver':ForkServerContext()}
    if sys.platform == 'darwin':
        _default_context = DefaultContext(_concrete_contexts['spawn'])
    else:
        _default_context = DefaultContext(_concrete_contexts['fork'])
else:

    class SpawnProcess(process.BaseProcess):
        _start_method = 'spawn'

        @staticmethod
        def _Popen(process_obj):
            from .popen_spawn_win32 import Popen
            return Popen(process_obj)


    class SpawnContext(BaseContext):
        _name = 'spawn'
        Process = SpawnProcess


    _concrete_contexts = {'spawn': SpawnContext()}
    _default_context = DefaultContext(_concrete_contexts['spawn'])

def _force_start_method(method):
    _default_context._actual_context = _concrete_contexts[method]


_tls = threading.local()

def get_spawning_popen():
    return getattr(_tls, 'spawning_popen', None)


def set_spawning_popen(popen):
    _tls.spawning_popen = popen


def assert_spawning--- This code section failed: ---

 L. 358         0  LOAD_GLOBAL              get_spawning_popen
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 359        10  LOAD_GLOBAL              RuntimeError

 L. 360        12  LOAD_STR                 '%s objects should only be shared between processes through inheritance'

 L. 361        14  LOAD_GLOBAL              type
               16  LOAD_FAST                'obj'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_ATTR                __name__

 L. 360        22  BINARY_MODULO    

 L. 359        24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1