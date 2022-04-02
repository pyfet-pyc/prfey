# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: contextlib.py
"""Utilities for with-statement contexts.  See PEP 343."""
import abc, sys, _collections_abc
from collections import deque
from functools import wraps
from types import MethodType
__all__ = [
 'asynccontextmanager', 'contextmanager', 'closing', 'nullcontext',
 'AbstractContextManager', 'AbstractAsyncContextManager',
 'AsyncExitStack', 'ContextDecorator', 'ExitStack',
 'redirect_stdout', 'redirect_stderr', 'suppress']

class AbstractContextManager(abc.ABC):
    __doc__ = 'An abstract base class for context managers.'

    def __enter__(self):
        """Return `self` upon entering the runtime context."""
        return self

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """Raise any exception triggered within the runtime context."""
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is AbstractContextManager:
            return _collections_abc._check_methods(C, '__enter__', '__exit__')
        return NotImplemented


class AbstractAsyncContextManager(abc.ABC):
    __doc__ = 'An abstract base class for asynchronous context managers.'

    async def __aenter__(self):
        """Return `self` upon entering the runtime context."""
        return self

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        """Raise any exception triggered within the runtime context."""
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is AbstractAsyncContextManager:
            return _collections_abc._check_methods(C, '__aenter__', '__aexit__')
        return NotImplemented


class ContextDecorator(object):
    __doc__ = 'A base class or mixin that enables context managers to work as decorators.'

    def _recreate_cm(self):
        """Return a recreated instance of self.

        Allows an otherwise one-shot context manager like
        _GeneratorContextManager to support use as
        a decorator via implicit recreation.

        This is a private interface just for _GeneratorContextManager.
        See issue #11647 for details.
        """
        return self

    def __call__(self, func):

        @wraps(func)
        def inner(*args, **kwds):
            with self._recreate_cm():
                return func(*args, **kwds)

        return inner


class _GeneratorContextManagerBase:
    __doc__ = 'Shared functionality for @contextmanager and @asynccontextmanager.'

    def __init__(self, func, args, kwds):
        self.gen = func(*args, **kwds)
        self.func, self.args, self.kwds = func, args, kwds
        doc = getattr(func, '__doc__', None)
        if doc is None:
            doc = type(self).__doc__
        self.__doc__ = doc


class _GeneratorContextManager(_GeneratorContextManagerBase, AbstractContextManager, ContextDecorator):
    __doc__ = 'Helper for @contextmanager decorator.'

    def _recreate_cm(self):
        return self.__class__(self.func, self.args, self.kwds)

    def __enter__(self):
        del self.args
        del self.kwds
        del self.func
        try:
            return next(self.gen)
        except StopIteration:
            raise RuntimeError("generator didn't yield") from None

    def __exit__--- This code section failed: ---

 L. 118         0  LOAD_FAST                'type'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    56  'to 56'

 L. 119         8  SETUP_FINALLY        24  'to 24'

 L. 120        10  LOAD_GLOBAL              next
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                gen
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          
               20  POP_BLOCK        
               22  JUMP_FORWARD         46  'to 46'
             24_0  COME_FROM_FINALLY     8  '8'

 L. 121        24  DUP_TOP          
               26  LOAD_GLOBAL              StopIteration
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 122        38  POP_EXCEPT       
               40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      
             46_0  COME_FROM            22  '22'

 L. 124        46  LOAD_GLOBAL              RuntimeError
               48  LOAD_STR                 "generator didn't stop"
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
               54  JUMP_FORWARD        260  'to 260'
             56_0  COME_FROM             6  '6'

 L. 126        56  LOAD_FAST                'value'
               58  LOAD_CONST               None
               60  COMPARE_OP               is
               62  POP_JUMP_IF_FALSE    70  'to 70'

 L. 129        64  LOAD_FAST                'type'
               66  CALL_FUNCTION_0       0  ''
               68  STORE_FAST               'value'
             70_0  COME_FROM            62  '62'

 L. 130        70  SETUP_FINALLY        92  'to 92'

 L. 131        72  LOAD_FAST                'self'
               74  LOAD_ATTR                gen
               76  LOAD_METHOD              throw
               78  LOAD_FAST                'type'
               80  LOAD_FAST                'value'
               82  LOAD_FAST                'traceback'
               84  CALL_METHOD_3         3  ''
               86  POP_TOP          
               88  POP_BLOCK        
               90  JUMP_FORWARD        252  'to 252'
             92_0  COME_FROM_FINALLY    70  '70'

 L. 132        92  DUP_TOP          
               94  LOAD_GLOBAL              StopIteration
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   136  'to 136'
              100  POP_TOP          
              102  STORE_FAST               'exc'
              104  POP_TOP          
              106  SETUP_FINALLY       124  'to 124'

 L. 136       108  LOAD_FAST                'exc'
              110  LOAD_FAST                'value'
              112  COMPARE_OP               is-not
              114  ROT_FOUR         
              116  POP_BLOCK        
              118  POP_EXCEPT       
              120  CALL_FINALLY        124  'to 124'
              122  RETURN_VALUE     
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM_FINALLY   106  '106'
              124  LOAD_CONST               None
              126  STORE_FAST               'exc'
              128  DELETE_FAST              'exc'
              130  END_FINALLY      
              132  POP_EXCEPT       
              134  JUMP_FORWARD        252  'to 252'
            136_0  COME_FROM            98  '98'

 L. 137       136  DUP_TOP          
              138  LOAD_GLOBAL              RuntimeError
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   216  'to 216'
              144  POP_TOP          
              146  STORE_FAST               'exc'
              148  POP_TOP          
              150  SETUP_FINALLY       204  'to 204'

 L. 139       152  LOAD_FAST                'exc'
              154  LOAD_FAST                'value'
              156  COMPARE_OP               is
              158  POP_JUMP_IF_FALSE   170  'to 170'

 L. 140       160  POP_BLOCK        
              162  POP_EXCEPT       
              164  CALL_FINALLY        204  'to 204'
              166  LOAD_CONST               False
              168  RETURN_VALUE     
            170_0  COME_FROM           158  '158'

 L. 144       170  LOAD_FAST                'type'
              172  LOAD_GLOBAL              StopIteration
              174  COMPARE_OP               is
              176  POP_JUMP_IF_FALSE   198  'to 198'
              178  LOAD_FAST                'exc'
              180  LOAD_ATTR                __cause__
              182  LOAD_FAST                'value'
              184  COMPARE_OP               is
              186  POP_JUMP_IF_FALSE   198  'to 198'

 L. 145       188  POP_BLOCK        
              190  POP_EXCEPT       
              192  CALL_FINALLY        204  'to 204'
              194  LOAD_CONST               False
              196  RETURN_VALUE     
            198_0  COME_FROM           186  '186'
            198_1  COME_FROM           176  '176'

 L. 146       198  RAISE_VARARGS_0       0  'reraise'
              200  POP_BLOCK        
              202  BEGIN_FINALLY    
            204_0  COME_FROM           192  '192'
            204_1  COME_FROM           164  '164'
            204_2  COME_FROM_FINALLY   150  '150'
              204  LOAD_CONST               None
              206  STORE_FAST               'exc'
              208  DELETE_FAST              'exc'
              210  END_FINALLY      
              212  POP_EXCEPT       
              214  JUMP_FORWARD        252  'to 252'
            216_0  COME_FROM           142  '142'

 L. 147       216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 159       222  LOAD_GLOBAL              sys
              224  LOAD_METHOD              exc_info
              226  CALL_METHOD_0         0  ''
              228  LOAD_CONST               1
              230  BINARY_SUBSCR    
              232  LOAD_FAST                'value'
              234  COMPARE_OP               is
              236  POP_JUMP_IF_FALSE   244  'to 244'

 L. 160       238  POP_EXCEPT       
              240  LOAD_CONST               False
              242  RETURN_VALUE     
            244_0  COME_FROM           236  '236'

 L. 161       244  RAISE_VARARGS_0       0  'reraise'
              246  POP_EXCEPT       
              248  JUMP_FORWARD        252  'to 252'
              250  END_FINALLY      
            252_0  COME_FROM           248  '248'
            252_1  COME_FROM           214  '214'
            252_2  COME_FROM           134  '134'
            252_3  COME_FROM            90  '90'

 L. 162       252  LOAD_GLOBAL              RuntimeError
              254  LOAD_STR                 "generator didn't stop after throw()"
              256  CALL_FUNCTION_1       1  ''
              258  RAISE_VARARGS_1       1  'exception instance'
            260_0  COME_FROM            54  '54'

Parse error at or near `POP_EXCEPT' instruction at offset 162


class _AsyncGeneratorContextManager(_GeneratorContextManagerBase, AbstractAsyncContextManager):
    __doc__ = 'Helper for @asynccontextmanager.'

    async def __aenter__(self):
        try:
            return await self.gen.__anext__()
        except StopAsyncIteration:
            raise RuntimeError("generator didn't yield") from None

    async def __aexit__--- This code section failed: ---

 L. 176         0  LOAD_FAST                'typ'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    62  'to 62'

 L. 177         8  SETUP_FINALLY        30  'to 30'

 L. 178        10  LOAD_FAST                'self'
               12  LOAD_ATTR                gen
               14  LOAD_METHOD              __anext__
               16  CALL_METHOD_0         0  ''
               18  GET_AWAITABLE    
               20  LOAD_CONST               None
               22  YIELD_FROM       
               24  POP_TOP          
               26  POP_BLOCK        
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM_FINALLY     8  '8'

 L. 179        30  DUP_TOP          
               32  LOAD_GLOBAL              StopAsyncIteration
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    50  'to 50'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 180        44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            36  '36'
               50  END_FINALLY      
             52_0  COME_FROM            28  '28'

 L. 182        52  LOAD_GLOBAL              RuntimeError
               54  LOAD_STR                 "generator didn't stop"
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
               60  JUMP_FORWARD        290  'to 290'
             62_0  COME_FROM             6  '6'

 L. 184        62  LOAD_FAST                'value'
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  POP_JUMP_IF_FALSE    76  'to 76'

 L. 185        70  LOAD_FAST                'typ'
               72  CALL_FUNCTION_0       0  ''
               74  STORE_FAST               'value'
             76_0  COME_FROM            68  '68'

 L. 188        76  SETUP_FINALLY       112  'to 112'

 L. 189        78  LOAD_FAST                'self'
               80  LOAD_ATTR                gen
               82  LOAD_METHOD              athrow
               84  LOAD_FAST                'typ'
               86  LOAD_FAST                'value'
               88  LOAD_FAST                'traceback'
               90  CALL_METHOD_3         3  ''
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  POP_TOP          

 L. 190       100  LOAD_GLOBAL              RuntimeError
              102  LOAD_STR                 "generator didn't stop after athrow()"
              104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
              108  POP_BLOCK        
              110  JUMP_FORWARD        290  'to 290'
            112_0  COME_FROM_FINALLY    76  '76'

 L. 191       112  DUP_TOP          
              114  LOAD_GLOBAL              StopAsyncIteration
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   156  'to 156'
              120  POP_TOP          
              122  STORE_FAST               'exc'
              124  POP_TOP          
              126  SETUP_FINALLY       144  'to 144'

 L. 192       128  LOAD_FAST                'exc'
              130  LOAD_FAST                'value'
              132  COMPARE_OP               is-not
              134  ROT_FOUR         
              136  POP_BLOCK        
              138  POP_EXCEPT       
              140  CALL_FINALLY        144  'to 144'
              142  RETURN_VALUE     
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM_FINALLY   126  '126'
              144  LOAD_CONST               None
              146  STORE_FAST               'exc'
              148  DELETE_FAST              'exc'
              150  END_FINALLY      
              152  POP_EXCEPT       
              154  JUMP_FORWARD        290  'to 290'
            156_0  COME_FROM           118  '118'

 L. 193       156  DUP_TOP          
              158  LOAD_GLOBAL              RuntimeError
              160  COMPARE_OP               exception-match
              162  POP_JUMP_IF_FALSE   242  'to 242'
              164  POP_TOP          
              166  STORE_FAST               'exc'
              168  POP_TOP          
              170  SETUP_FINALLY       230  'to 230'

 L. 194       172  LOAD_FAST                'exc'
              174  LOAD_FAST                'value'
              176  COMPARE_OP               is
              178  POP_JUMP_IF_FALSE   190  'to 190'

 L. 195       180  POP_BLOCK        
              182  POP_EXCEPT       
              184  CALL_FINALLY        230  'to 230'
              186  LOAD_CONST               False
              188  RETURN_VALUE     
            190_0  COME_FROM           178  '178'

 L. 202       190  LOAD_GLOBAL              isinstance
              192  LOAD_FAST                'value'
              194  LOAD_GLOBAL              StopIteration
              196  LOAD_GLOBAL              StopAsyncIteration
              198  BUILD_TUPLE_2         2 
              200  CALL_FUNCTION_2       2  ''
              202  POP_JUMP_IF_FALSE   224  'to 224'

 L. 203       204  LOAD_FAST                'exc'
              206  LOAD_ATTR                __cause__
              208  LOAD_FAST                'value'
              210  COMPARE_OP               is
              212  POP_JUMP_IF_FALSE   224  'to 224'

 L. 204       214  POP_BLOCK        
              216  POP_EXCEPT       
              218  CALL_FINALLY        230  'to 230'
              220  LOAD_CONST               False
              222  RETURN_VALUE     
            224_0  COME_FROM           212  '212'
            224_1  COME_FROM           202  '202'

 L. 205       224  RAISE_VARARGS_0       0  'reraise'
              226  POP_BLOCK        
              228  BEGIN_FINALLY    
            230_0  COME_FROM           218  '218'
            230_1  COME_FROM           184  '184'
            230_2  COME_FROM_FINALLY   170  '170'
              230  LOAD_CONST               None
              232  STORE_FAST               'exc'
              234  DELETE_FAST              'exc'
              236  END_FINALLY      
              238  POP_EXCEPT       
              240  JUMP_FORWARD        290  'to 290'
            242_0  COME_FROM           162  '162'

 L. 206       242  DUP_TOP          
              244  LOAD_GLOBAL              BaseException
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   288  'to 288'
              252  POP_TOP          
              254  STORE_FAST               'exc'
              256  POP_TOP          
              258  SETUP_FINALLY       276  'to 276'

 L. 207       260  LOAD_FAST                'exc'
              262  LOAD_FAST                'value'
              264  COMPARE_OP               is-not
          266_268  POP_JUMP_IF_FALSE   272  'to 272'

 L. 208       270  RAISE_VARARGS_0       0  'reraise'
            272_0  COME_FROM           266  '266'
              272  POP_BLOCK        
              274  BEGIN_FINALLY    
            276_0  COME_FROM_FINALLY   258  '258'
              276  LOAD_CONST               None
              278  STORE_FAST               'exc'
              280  DELETE_FAST              'exc'
              282  END_FINALLY      
              284  POP_EXCEPT       
              286  JUMP_FORWARD        290  'to 290'
            288_0  COME_FROM           248  '248'
              288  END_FINALLY      
            290_0  COME_FROM           286  '286'
            290_1  COME_FROM           240  '240'
            290_2  COME_FROM           154  '154'
            290_3  COME_FROM           110  '110'
            290_4  COME_FROM            60  '60'

Parse error at or near `POP_EXCEPT' instruction at offset 182


def contextmanager(func):
    """@contextmanager decorator.

    Typical usage:

        @contextmanager
        def some_generator(<arguments>):
            <setup>
            try:
                yield <value>
            finally:
                <cleanup>

    This makes this:

        with some_generator(<arguments>) as <variable>:
            <body>

    equivalent to this:

        <setup>
        try:
            <variable> = <value>
            <body>
        finally:
            <cleanup>
    """

    @wraps(func)
    def helper(*args, **kwds):
        return _GeneratorContextManager(func, args, kwds)

    return helper


def asynccontextmanager(func):
    """@asynccontextmanager decorator.

    Typical usage:

        @asynccontextmanager
        async def some_async_generator(<arguments>):
            <setup>
            try:
                yield <value>
            finally:
                <cleanup>

    This makes this:

        async with some_async_generator(<arguments>) as <variable>:
            <body>

    equivalent to this:

        <setup>
        try:
            <variable> = <value>
            <body>
        finally:
            <cleanup>
    """

    @wraps(func)
    def helper(*args, **kwds):
        return _AsyncGeneratorContextManager(func, args, kwds)

    return helper


class closing(AbstractContextManager):
    __doc__ = 'Context to automatically close something at the end of a block.\n\n    Code like this:\n\n        with closing(<module>.open(<arguments>)) as f:\n            <block>\n\n    is equivalent to this:\n\n        f = <module>.open(<arguments>)\n        try:\n            <block>\n        finally:\n            f.close()\n\n    '

    def __init__(self, thing):
        self.thing = thing

    def __enter__(self):
        return self.thing

    def __exit__(self, *exc_info):
        self.thing.close()


class _RedirectStream(AbstractContextManager):
    _stream = None

    def __init__(self, new_target):
        self._new_target = new_target
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(getattr(sys, self._stream))
        setattr(sys, self._stream, self._new_target)
        return self._new_target

    def __exit__(self, exctype, excinst, exctb):
        setattr(sys, self._stream, self._old_targets.pop())


class redirect_stdout(_RedirectStream):
    __doc__ = "Context manager for temporarily redirecting stdout to another file.\n\n        # How to send help() to stderr\n        with redirect_stdout(sys.stderr):\n            help(dir)\n\n        # How to write help() to a file\n        with open('help.txt', 'w') as f:\n            with redirect_stdout(f):\n                help(pow)\n    "
    _stream = 'stdout'


class redirect_stderr(_RedirectStream):
    __doc__ = 'Context manager for temporarily redirecting stderr to another file.'
    _stream = 'stderr'


class suppress(AbstractContextManager):
    __doc__ = 'Context manager to suppress specified exceptions\n\n    After the exception is suppressed, execution proceeds with the next\n    statement following the with statement.\n\n         with suppress(FileNotFoundError):\n             os.remove(somefile)\n         # Execution still resumes here if the file was already removed\n    '

    def __init__(self, *exceptions):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exctype, excinst, exctb):
        return exctype is not None and issubclass(exctype, self._exceptions)


class _BaseExitStack:
    __doc__ = 'A base class for ExitStack and AsyncExitStack.'

    @staticmethod
    def _create_exit_wrapper(cm, cm_exit):
        return MethodType(cm_exit, cm)

    @staticmethod
    def _create_cb_wrapper(callback, *args, **kwds):

        def _exit_wrapper(exc_type, exc, tb):
            callback(*args, **kwds)

        return _exit_wrapper

    def __init__(self):
        self._exit_callbacks = deque

    def pop_all(self):
        """Preserve the context stack by transferring it to a new instance."""
        new_stack = type(self)
        new_stack._exit_callbacks = self._exit_callbacks
        self._exit_callbacks = deque
        return new_stack

    def push(self, exit):
        """Registers a callback with the standard __exit__ method signature.

        Can suppress exceptions the same way __exit__ method can.
        Also accepts any object with an __exit__ method (registering a call
        to the method instead of the object itself).
        """
        _cb_type = type(exit)
        try:
            exit_method = _cb_type.__exit__
        except AttributeError:
            self._push_exit_callback(exit)
        else:
            self._push_cm_exit(exit, exit_method)
        return exit

    def enter_context(self, cm):
        """Enters the supplied context manager.

        If successful, also pushes its __exit__ method as a callback and
        returns the result of the __enter__ method.
        """
        _cm_type = type(cm)
        _exit = _cm_type.__exit__
        result = _cm_type.__enter__(cm)
        self._push_cm_exit(cm, _exit)
        return result

    def callback(*args, **kwds):
        """Registers an arbitrary callback and arguments.

        Cannot suppress exceptions.
        """
        if len(args) >= 2:
            self, callback, *args = args
        elif not args:
            raise TypeError("descriptor 'callback' of '_BaseExitStack' object needs an argument")
        elif 'callback' in kwds:
            callback = kwds.pop('callback')
            self, *args = args
            import warnings
            warnings.warn("Passing 'callback' as keyword argument is deprecated", DeprecationWarning,
              stacklevel=2)
        else:
            raise TypeError('callback expected at least 1 positional argument, got %d' % (len(args) - 1))
        _exit_wrapper = (self._create_cb_wrapper)(callback, *args, **kwds)
        _exit_wrapper.__wrapped__ = callback
        self._push_exit_callback(_exit_wrapper)
        return callback

    callback.__text_signature__ = '($self, callback, /, *args, **kwds)'

    def _push_cm_exit(self, cm, cm_exit):
        """Helper to correctly register callbacks to __exit__ methods."""
        _exit_wrapper = self._create_exit_wrapper(cm, cm_exit)
        self._push_exit_callback(_exit_wrapper, True)

    def _push_exit_callback(self, callback, is_sync=True):
        self._exit_callbacks.append((is_sync, callback))


class ExitStack(_BaseExitStack, AbstractContextManager):
    __doc__ = 'Context manager for dynamic management of a stack of exit callbacks.\n\n    For example:\n        with ExitStack() as stack:\n            files = [stack.enter_context(open(fname)) for fname in filenames]\n            # All opened files will automatically be closed at the end of\n            # the with statement, even if attempts to open files later\n            # in the list raise an exception.\n    '

    def __enter__(self):
        return self

    def __exit__--- This code section failed: ---

 L. 483         0  LOAD_FAST                'exc_details'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  LOAD_CONST               None
                8  COMPARE_OP               is-not
               10  STORE_FAST               'received_exc'

 L. 487        12  LOAD_GLOBAL              sys
               14  LOAD_METHOD              exc_info
               16  CALL_METHOD_0         0  ''
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  STORE_DEREF              'frame_exc'

 L. 488        24  LOAD_CLOSURE             'frame_exc'
               26  BUILD_TUPLE_1         1 
               28  LOAD_CODE                <code_object _fix_exception_context>
               30  LOAD_STR                 'ExitStack.__exit__.<locals>._fix_exception_context'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               '_fix_exception_context'

 L. 504        36  LOAD_CONST               False
               38  STORE_FAST               'suppressed_exc'

 L. 505        40  LOAD_CONST               False
               42  STORE_FAST               'pending_raise'
             44_0  COME_FROM           144  '144'
             44_1  COME_FROM           140  '140'
             44_2  COME_FROM            96  '96'

 L. 506        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _exit_callbacks
               48  POP_JUMP_IF_FALSE   146  'to 146'

 L. 507        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _exit_callbacks
               54  LOAD_METHOD              pop
               56  CALL_METHOD_0         0  ''
               58  UNPACK_SEQUENCE_2     2 
               60  STORE_FAST               'is_sync'
               62  STORE_FAST               'cb'

 L. 508        64  LOAD_FAST                'is_sync'
               66  POP_JUMP_IF_TRUE     72  'to 72'
               68  LOAD_ASSERT              AssertionError
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            66  '66'

 L. 509        72  SETUP_FINALLY        98  'to 98'

 L. 510        74  LOAD_FAST                'cb'
               76  LOAD_FAST                'exc_details'
               78  CALL_FUNCTION_EX      0  'positional arguments only'
               80  POP_JUMP_IF_FALSE    94  'to 94'

 L. 511        82  LOAD_CONST               True
               84  STORE_FAST               'suppressed_exc'

 L. 512        86  LOAD_CONST               False
               88  STORE_FAST               'pending_raise'

 L. 513        90  LOAD_CONST               (None, None, None)
               92  STORE_FAST               'exc_details'
             94_0  COME_FROM            80  '80'
               94  POP_BLOCK        
               96  JUMP_BACK            44  'to 44'
             98_0  COME_FROM_FINALLY    72  '72'

 L. 514        98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 515       104  LOAD_GLOBAL              sys
              106  LOAD_METHOD              exc_info
              108  CALL_METHOD_0         0  ''
              110  STORE_FAST               'new_exc_details'

 L. 517       112  LOAD_FAST                '_fix_exception_context'
              114  LOAD_FAST                'new_exc_details'
              116  LOAD_CONST               1
              118  BINARY_SUBSCR    
              120  LOAD_FAST                'exc_details'
              122  LOAD_CONST               1
              124  BINARY_SUBSCR    
              126  CALL_FUNCTION_2       2  ''
              128  POP_TOP          

 L. 518       130  LOAD_CONST               True
              132  STORE_FAST               'pending_raise'

 L. 519       134  LOAD_FAST                'new_exc_details'
              136  STORE_FAST               'exc_details'
              138  POP_EXCEPT       
              140  JUMP_BACK            44  'to 44'
              142  END_FINALLY      
              144  JUMP_BACK            44  'to 44'
            146_0  COME_FROM            48  '48'

 L. 520       146  LOAD_FAST                'pending_raise'
              148  POP_JUMP_IF_FALSE   206  'to 206'

 L. 521       150  SETUP_FINALLY       174  'to 174'

 L. 524       152  LOAD_FAST                'exc_details'
              154  LOAD_CONST               1
              156  BINARY_SUBSCR    
              158  LOAD_ATTR                __context__
              160  STORE_FAST               'fixed_ctx'

 L. 525       162  LOAD_FAST                'exc_details'
              164  LOAD_CONST               1
              166  BINARY_SUBSCR    
              168  RAISE_VARARGS_1       1  'exception instance'
              170  POP_BLOCK        
              172  JUMP_FORWARD        206  'to 206'
            174_0  COME_FROM_FINALLY   150  '150'

 L. 526       174  DUP_TOP          
              176  LOAD_GLOBAL              BaseException
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   204  'to 204'
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          

 L. 527       188  LOAD_FAST                'fixed_ctx'
              190  LOAD_FAST                'exc_details'
              192  LOAD_CONST               1
              194  BINARY_SUBSCR    
              196  STORE_ATTR               __context__

 L. 528       198  RAISE_VARARGS_0       0  'reraise'
              200  POP_EXCEPT       
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           180  '180'
              204  END_FINALLY      
            206_0  COME_FROM           202  '202'
            206_1  COME_FROM           172  '172'
            206_2  COME_FROM           148  '148'

 L. 529       206  LOAD_FAST                'received_exc'
              208  JUMP_IF_FALSE_OR_POP   212  'to 212'
              210  LOAD_FAST                'suppressed_exc'
            212_0  COME_FROM           208  '208'
              212  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 140

    def close(self):
        """Immediately unwind the context stack."""
        self.__exit__(None, None, None)


class AsyncExitStack(_BaseExitStack, AbstractAsyncContextManager):
    __doc__ = 'Async context manager for dynamic management of a stack of exit\n    callbacks.\n\n    For example:\n        async with AsyncExitStack() as stack:\n            connections = [await stack.enter_async_context(get_connection())\n                for i in range(5)]\n            # All opened connections will automatically be released at the\n            # end of the async with statement, even if attempts to open a\n            # connection later in the list raise an exception.\n    '

    @staticmethod
    def _create_async_exit_wrapper(cm, cm_exit):
        return MethodType(cm_exit, cm)

    @staticmethod
    def _create_async_cb_wrapper(callback, *args, **kwds):

        async def _exit_wrapper(exc_type, exc, tb):
            await callback(*args, **kwds)

        return _exit_wrapper

    async def enter_async_context(self, cm):
        """Enters the supplied async context manager.

        If successful, also pushes its __aexit__ method as a callback and
        returns the result of the __aenter__ method.
        """
        _cm_type = type(cm)
        _exit = _cm_type.__aexit__
        result = await _cm_type.__aenter__(cm)
        self._push_async_cm_exit(cm, _exit)
        return result

    def push_async_exit(self, exit):
        """Registers a coroutine function with the standard __aexit__ method
        signature.

        Can suppress exceptions the same way __aexit__ method can.
        Also accepts any object with an __aexit__ method (registering a call
        to the method instead of the object itself).
        """
        _cb_type = type(exit)
        try:
            exit_method = _cb_type.__aexit__
        except AttributeError:
            self._push_exit_callback(exit, False)
        else:
            self._push_async_cm_exit(exit, exit_method)
        return exit

    def push_async_callback(*args, **kwds):
        """Registers an arbitrary coroutine function and arguments.

        Cannot suppress exceptions.
        """
        if len(args) >= 2:
            self, callback, *args = args
        elif not args:
            raise TypeError("descriptor 'push_async_callback' of 'AsyncExitStack' object needs an argument")
        elif 'callback' in kwds:
            callback = kwds.pop('callback')
            self, *args = args
            import warnings
            warnings.warn("Passing 'callback' as keyword argument is deprecated", DeprecationWarning,
              stacklevel=2)
        else:
            raise TypeError('push_async_callback expected at least 1 positional argument, got %d' % (len(args) - 1))
        _exit_wrapper = (self._create_async_cb_wrapper)(callback, *args, **kwds)
        _exit_wrapper.__wrapped__ = callback
        self._push_exit_callback(_exit_wrapper, False)
        return callback

    push_async_callback.__text_signature__ = '($self, callback, /, *args, **kwds)'

    async def aclose(self):
        """Immediately unwind the context stack."""
        await self.__aexit__(None, None, None)

    def _push_async_cm_exit(self, cm, cm_exit):
        """Helper to correctly register coroutine function to __aexit__
        method."""
        _exit_wrapper = self._create_async_exit_wrapper(cm, cm_exit)
        self._push_exit_callback(_exit_wrapper, False)

    async def __aenter__(self):
        return self

    async def __aexit__--- This code section failed: ---

 L. 633         0  LOAD_FAST                'exc_details'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  LOAD_CONST               None
                8  COMPARE_OP               is-not
               10  STORE_FAST               'received_exc'

 L. 637        12  LOAD_GLOBAL              sys
               14  LOAD_METHOD              exc_info
               16  CALL_METHOD_0         0  ''
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  STORE_DEREF              'frame_exc'

 L. 638        24  LOAD_CLOSURE             'frame_exc'
               26  BUILD_TUPLE_1         1 
               28  LOAD_CODE                <code_object _fix_exception_context>
               30  LOAD_STR                 'AsyncExitStack.__aexit__.<locals>._fix_exception_context'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               '_fix_exception_context'

 L. 654        36  LOAD_CONST               False
               38  STORE_FAST               'suppressed_exc'

 L. 655        40  LOAD_CONST               False
               42  STORE_FAST               'pending_raise'
             44_0  COME_FROM           160  '160'
             44_1  COME_FROM           156  '156'
             44_2  COME_FROM           112  '112'

 L. 656        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _exit_callbacks
               48  POP_JUMP_IF_FALSE   162  'to 162'

 L. 657        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _exit_callbacks
               54  LOAD_METHOD              pop
               56  CALL_METHOD_0         0  ''
               58  UNPACK_SEQUENCE_2     2 
               60  STORE_FAST               'is_sync'
               62  STORE_FAST               'cb'

 L. 658        64  SETUP_FINALLY       114  'to 114'

 L. 659        66  LOAD_FAST                'is_sync'
               68  POP_JUMP_IF_FALSE    80  'to 80'

 L. 660        70  LOAD_FAST                'cb'
               72  LOAD_FAST                'exc_details'
               74  CALL_FUNCTION_EX      0  'positional arguments only'
               76  STORE_FAST               'cb_suppress'
               78  JUMP_FORWARD         94  'to 94'
             80_0  COME_FROM            68  '68'

 L. 662        80  LOAD_FAST                'cb'
               82  LOAD_FAST                'exc_details'
               84  CALL_FUNCTION_EX      0  'positional arguments only'
               86  GET_AWAITABLE    
               88  LOAD_CONST               None
               90  YIELD_FROM       
               92  STORE_FAST               'cb_suppress'
             94_0  COME_FROM            78  '78'

 L. 664        94  LOAD_FAST                'cb_suppress'
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 665        98  LOAD_CONST               True
              100  STORE_FAST               'suppressed_exc'

 L. 666       102  LOAD_CONST               False
              104  STORE_FAST               'pending_raise'

 L. 667       106  LOAD_CONST               (None, None, None)
              108  STORE_FAST               'exc_details'
            110_0  COME_FROM            96  '96'
              110  POP_BLOCK        
              112  JUMP_BACK            44  'to 44'
            114_0  COME_FROM_FINALLY    64  '64'

 L. 668       114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 669       120  LOAD_GLOBAL              sys
              122  LOAD_METHOD              exc_info
              124  CALL_METHOD_0         0  ''
              126  STORE_FAST               'new_exc_details'

 L. 671       128  LOAD_FAST                '_fix_exception_context'
              130  LOAD_FAST                'new_exc_details'
              132  LOAD_CONST               1
              134  BINARY_SUBSCR    
              136  LOAD_FAST                'exc_details'
              138  LOAD_CONST               1
              140  BINARY_SUBSCR    
              142  CALL_FUNCTION_2       2  ''
              144  POP_TOP          

 L. 672       146  LOAD_CONST               True
              148  STORE_FAST               'pending_raise'

 L. 673       150  LOAD_FAST                'new_exc_details'
              152  STORE_FAST               'exc_details'
              154  POP_EXCEPT       
              156  JUMP_BACK            44  'to 44'
              158  END_FINALLY      
              160  JUMP_BACK            44  'to 44'
            162_0  COME_FROM            48  '48'

 L. 674       162  LOAD_FAST                'pending_raise'
              164  POP_JUMP_IF_FALSE   222  'to 222'

 L. 675       166  SETUP_FINALLY       190  'to 190'

 L. 678       168  LOAD_FAST                'exc_details'
              170  LOAD_CONST               1
              172  BINARY_SUBSCR    
              174  LOAD_ATTR                __context__
              176  STORE_FAST               'fixed_ctx'

 L. 679       178  LOAD_FAST                'exc_details'
              180  LOAD_CONST               1
              182  BINARY_SUBSCR    
              184  RAISE_VARARGS_1       1  'exception instance'
              186  POP_BLOCK        
              188  JUMP_FORWARD        222  'to 222'
            190_0  COME_FROM_FINALLY   166  '166'

 L. 680       190  DUP_TOP          
              192  LOAD_GLOBAL              BaseException
              194  COMPARE_OP               exception-match
              196  POP_JUMP_IF_FALSE   220  'to 220'
              198  POP_TOP          
              200  POP_TOP          
              202  POP_TOP          

 L. 681       204  LOAD_FAST                'fixed_ctx'
              206  LOAD_FAST                'exc_details'
              208  LOAD_CONST               1
              210  BINARY_SUBSCR    
              212  STORE_ATTR               __context__

 L. 682       214  RAISE_VARARGS_0       0  'reraise'
              216  POP_EXCEPT       
              218  JUMP_FORWARD        222  'to 222'
            220_0  COME_FROM           196  '196'
              220  END_FINALLY      
            222_0  COME_FROM           218  '218'
            222_1  COME_FROM           188  '188'
            222_2  COME_FROM           164  '164'

 L. 683       222  LOAD_FAST                'received_exc'
              224  JUMP_IF_FALSE_OR_POP   228  'to 228'
              226  LOAD_FAST                'suppressed_exc'
            228_0  COME_FROM           224  '224'
              228  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 156


class nullcontext(AbstractContextManager):
    __doc__ = 'Context manager that does no additional processing.\n\n    Used as a stand-in for a normal context manager, when a particular\n    block of code is only sometimes used with a normal context manager:\n\n    cm = optional_cm if condition else nullcontext()\n    with cm:\n        # Perform operation, using optional_cm if condition is True\n    '

    def __init__(self, enter_result=None):
        self.enter_result = enter_result

    def __enter__(self):
        return self.enter_result

    def __exit__(self, *excinfo):
        pass