# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: asyncio\coroutines.py
__all__ = ('coroutine', 'iscoroutinefunction', 'iscoroutine')
import collections.abc, functools, inspect, os, sys, traceback, types, warnings
from . import base_futures
from . import constants
from . import format_helpers
from .log import logger

def _is_debug_mode():
    return (sys.flags.dev_mode) or ((not sys.flags.ignore_environment) and (bool(os.environ.get('PYTHONASYNCIODEBUG'))))


_DEBUG = _is_debug_mode()

class CoroWrapper:

    def __init__(self, gen, func=None):
        if not inspect.isgenerator(gen):
            assert inspect.iscoroutine(gen), gen
        self.gen = gen
        self.func = func
        self._source_traceback = format_helpers.extract_stack(sys._getframe(1))
        self.__name__ = getattr(gen, '__name__', None)
        self.__qualname__ = getattr(gen, '__qualname__', None)

    def __repr__(self):
        coro_repr = _format_coroutine(self)
        if self._source_traceback:
            frame = self._source_traceback[(-1)]
            coro_repr += f", created at {frame[0]}:{frame[1]}"
        return f"<{self.__class__.__name__} {coro_repr}>"

    def __iter__(self):
        return self

    def __next__(self):
        return self.gen.send(None)

    def send(self, value):
        return self.gen.send(value)

    def throw(self, type, value=None, traceback=None):
        return self.gen.throw(type, value, traceback)

    def close(self):
        return self.gen.close()

    @property
    def gi_frame(self):
        return self.gen.gi_frame

    @property
    def gi_running(self):
        return self.gen.gi_running

    @property
    def gi_code(self):
        return self.gen.gi_code

    def __await__(self):
        return self

    @property
    def gi_yieldfrom(self):
        return self.gen.gi_yieldfrom

    def __del__(self):
        gen = getattr(self, 'gen', None)
        frame = getattr(gen, 'gi_frame', None)
        if frame is not None:
            if frame.f_lasti == -1:
                msg = f"{self!r} was never yielded from"
                tb = getattr(self, '_source_traceback', ())
                if tb:
                    tb = ''.join(traceback.format_list(tb))
                    msg += f"\nCoroutine object created at (most recent call last, truncated to {constants.DEBUG_STACK_DEPTH} last lines):\n"
                    msg += tb.rstrip()
                logger.error(msg)


def coroutine(func):
    """Decorator to mark coroutines.

    If the coroutine is not yielded from before it is destroyed,
    an error message is logged.
    """
    warnings.warn('"@coroutine" decorator is deprecated since Python 3.8, use "async def" instead', DeprecationWarning,
      stacklevel=2)
    if inspect.iscoroutinefunction(func):
        return func
    if inspect.isgeneratorfunction(func):
        coro = func
    else:

        @functools.wraps(func)
        def coro(*args, **kw):
            res = func(*args, **kw)
            if base_futures.isfuture(res) or inspect.isgenerator(res) or isinstance(res, CoroWrapper):
                res = yield from res
            else:
                try:
                    await_meth = res.__await__
                except AttributeError:
                    pass
                else:
                    if isinstance(res, collections.abc.Awaitable):
                        res = yield from await_meth()
            return res
            if False:
                yield None

    coro = types.coroutine(coro)
    if not _DEBUG:
        wrapper = coro
    else:

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            w = CoroWrapper(coro(*args, **kwds), func=func)
            if w._source_traceback:
                del w._source_traceback[-1]
            w.__name__ = getattr(func, '__name__', None)
            w.__qualname__ = getattr(func, '__qualname__', None)
            return w

    wrapper._is_coroutine = _is_coroutine
    return wrapper


_is_coroutine = object()

def iscoroutinefunction(func):
    """Return True if func is a decorated coroutine function."""
    return inspect.iscoroutinefunction(func) or getattr(func, '_is_coroutine', None) is _is_coroutine


_COROUTINE_TYPES = (
 types.CoroutineType, types.GeneratorType,
 collections.abc.Coroutine, CoroWrapper)
_iscoroutine_typecache = set()

def iscoroutine(obj):
    """Return True if obj is a coroutine object."""
    if type(obj) in _iscoroutine_typecache:
        return True
    if isinstance(obj, _COROUTINE_TYPES):
        if len(_iscoroutine_typecache) < 100:
            _iscoroutine_typecache.add(type(obj))
        return True
    return False


def _format_coroutine(coro):
    assert iscoroutine(coro)
    is_corowrapper = isinstance(coro, CoroWrapper)

    def get_name(coro):
        if is_corowrapper:
            return format_helpers._format_callback(coro.func, (), {})
        if hasattr(coro, '__qualname__') and coro.__qualname__:
            coro_name = coro.__qualname__
        elif hasattr(coro, '__name__') and coro.__name__:
            coro_name = coro.__name__
        else:
            coro_name = f"<{type(coro).__name__} without __name__>"
        return f"{coro_name}()"

    def is_running--- This code section failed: ---

 L. 216         0  SETUP_FINALLY        10  'to 10'

 L. 217         2  LOAD_FAST                'coro'
                4  LOAD_ATTR                cr_running
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L. 218        10  DUP_TOP          
               12  LOAD_GLOBAL              AttributeError
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    66  'to 66'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 219        24  SETUP_FINALLY        38  'to 38'

 L. 220        26  LOAD_FAST                'coro'
               28  LOAD_ATTR                gi_running
               30  POP_BLOCK        
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    24  '24'

 L. 221        38  DUP_TOP          
               40  LOAD_GLOBAL              AttributeError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    60  'to 60'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 222        52  POP_EXCEPT       
               54  POP_EXCEPT       
               56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            44  '44'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            16  '16'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'

Parse error at or near `ROT_FOUR' instruction at offset 32

    coro_code = None
    if hasattr(coro, 'cr_code') and coro.cr_code:
        coro_code = coro.cr_code
    elif hasattr(coro, 'gi_code'):
        if coro.gi_code:
            coro_code = coro.gi_code
    coro_name = get_name(coro)
    if not coro_code:
        if is_running(coro):
            return f"{coro_name} running"
        return coro_name
    coro_frame = None
    if hasattr(coro, 'gi_frame') and coro.gi_frame:
        coro_frame = coro.gi_frame
    elif hasattr(coro, 'cr_frame'):
        if coro.cr_frame:
            coro_frame = coro.cr_frame
    filename = coro_code.co_filename or '<empty co_filename>'
    lineno = 0
    if is_corowrapper:
        if coro.func is not None and not inspect.isgeneratorfunction(coro.func):
            source = format_helpers._get_function_source(coro.func)
            if source is not None:
                filename, lineno = source
            if coro_frame is None:
                coro_repr = f"{coro_name} done, defined at {filename}:{lineno}"
            else:
                coro_repr = f"{coro_name} running, defined at {filename}:{lineno}"
        elif coro_frame is not None:
            lineno = coro_frame.f_lineno
            coro_repr = f"{coro_name} running at {filename}:{lineno}"
        else:
            lineno = coro_code.co_firstlineno
            coro_repr = f"{coro_name} done, defined at {filename}:{lineno}"
        return coro_repr