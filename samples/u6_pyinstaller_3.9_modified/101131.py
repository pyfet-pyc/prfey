# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\format_helpers.py
import functools, inspect, reprlib, sys, traceback
from . import constants

def _get_function_source(func):
    func = inspect.unwrap(func)
    if inspect.isfunction(func):
        code = func.__code__
        return (code.co_filename, code.co_firstlineno)
    if isinstance(func, functools.partial):
        return _get_function_source(func.func)
    if isinstance(func, functools.partialmethod):
        return _get_function_source(func.func)


def _format_callback_source(func, args):
    func_repr = _format_callback(func, args, None)
    source = _get_function_source(func)
    if source:
        func_repr += f" at {source[0]}:{source[1]}"
    return func_repr


def _format_args_and_kwargs(args, kwargs):
    """Format function arguments and keyword arguments.

    Special case for a single parameter: ('hello',) is formatted as ('hello').
    """
    items = []
    if args:
        items.extend((reprlib.repr(arg) for arg in args))
    if kwargs:
        items.extend((f"{k}={reprlib.repr(v)}" for k, v in kwargs.items()))
    return '({})'.format(', '.join(items))


def _format_callback(func, args, kwargs, suffix=''):
    if isinstance(func, functools.partial):
        suffix = _format_args_and_kwargs(args, kwargs) + suffix
        return _format_callback(func.func, func.args, func.keywords, suffix)
    if hasattr(func, '__qualname__') and func.__qualname__:
        func_repr = func.__qualname__
    else:
        if hasattr(func, '__name__') and func.__name__:
            func_repr = func.__name__
        else:
            func_repr = repr(func)
    func_repr += _format_args_and_kwargs(args, kwargs)
    if suffix:
        func_repr += suffix
    return func_repr


def extract_stack--- This code section failed: ---

 L.  66         0  LOAD_FAST                'f'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  67         8  LOAD_GLOBAL              sys
               10  LOAD_METHOD              _getframe
               12  CALL_METHOD_0         0  ''
               14  LOAD_ATTR                f_back
               16  STORE_FAST               'f'
             18_0  COME_FROM             6  '6'

 L.  68        18  LOAD_FAST                'limit'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L.  71        26  LOAD_GLOBAL              constants
               28  LOAD_ATTR                DEBUG_STACK_DEPTH
               30  STORE_FAST               'limit'
             32_0  COME_FROM            24  '24'

 L.  72        32  LOAD_GLOBAL              traceback
               34  LOAD_ATTR                StackSummary
               36  LOAD_ATTR                extract
               38  LOAD_GLOBAL              traceback
               40  LOAD_METHOD              walk_stack
               42  LOAD_FAST                'f'
               44  CALL_METHOD_1         1  ''

 L.  73        46  LOAD_FAST                'limit'

 L.  74        48  LOAD_CONST               False

 L.  72        50  LOAD_CONST               ('limit', 'lookup_lines')
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  STORE_FAST               'stack'

 L.  75        56  LOAD_FAST                'stack'
               58  LOAD_METHOD              reverse
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          

 L.  76        64  LOAD_FAST                'stack'
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1