# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\core\overrides.py
"""Implementation of __array_function__ overrides from NEP-18."""
import collections, functools, os, textwrap
from numpy.core._multiarray_umath import add_docstring, implement_array_function, _get_implementing_args
from numpy.compat._inspect import getargspec
ARRAY_FUNCTION_ENABLED = bool(int(os.environ.get('NUMPY_EXPERIMENTAL_ARRAY_FUNCTION', 1)))
add_docstring(implement_array_function, "\n    Implement a function with checks for __array_function__ overrides.\n\n    All arguments are required, and can only be passed by position.\n\n    Arguments\n    ---------\n    implementation : function\n        Function that implements the operation on NumPy array without\n        overrides when called like ``implementation(*args, **kwargs)``.\n    public_api : function\n        Function exposed by NumPy's public API originally called like\n        ``public_api(*args, **kwargs)`` on which arguments are now being\n        checked.\n    relevant_args : iterable\n        Iterable of arguments to check for __array_function__ methods.\n    args : tuple\n        Arbitrary positional arguments originally passed into ``public_api``.\n    kwargs : dict\n        Arbitrary keyword arguments originally passed into ``public_api``.\n\n    Returns\n    -------\n    Result from calling ``implementation()`` or an ``__array_function__``\n    method, as appropriate.\n\n    Raises\n    ------\n    TypeError : if no implementation is found.\n    ")
add_docstring(_get_implementing_args, '\n    Collect arguments on which to call __array_function__.\n\n    Parameters\n    ----------\n    relevant_args : iterable of array-like\n        Iterable of possibly array-like arguments to check for\n        __array_function__ methods.\n\n    Returns\n    -------\n    Sequence of arguments with __array_function__ methods, in the order in\n    which they should be called.\n    ')
ArgSpec = collections.namedtuple('ArgSpec', 'args varargs keywords defaults')

def verify_matching_signatures--- This code section failed: ---

 L.  74         0  LOAD_GLOBAL              ArgSpec
                2  LOAD_GLOBAL              getargspec
                4  LOAD_FAST                'implementation'
                6  CALL_FUNCTION_1       1  ''
                8  CALL_FUNCTION_EX      0  'positional arguments only'
               10  STORE_FAST               'implementation_spec'

 L.  75        12  LOAD_GLOBAL              ArgSpec
               14  LOAD_GLOBAL              getargspec
               16  LOAD_FAST                'dispatcher'
               18  CALL_FUNCTION_1       1  ''
               20  CALL_FUNCTION_EX      0  'positional arguments only'
               22  STORE_FAST               'dispatcher_spec'

 L.  77        24  LOAD_FAST                'implementation_spec'
               26  LOAD_ATTR                args
               28  LOAD_FAST                'dispatcher_spec'
               30  LOAD_ATTR                args
               32  COMPARE_OP               !=
               34  POP_JUMP_IF_TRUE    110  'to 110'

 L.  78        36  LOAD_FAST                'implementation_spec'
               38  LOAD_ATTR                varargs
               40  LOAD_FAST                'dispatcher_spec'
               42  LOAD_ATTR                varargs
               44  COMPARE_OP               !=

 L.  77        46  POP_JUMP_IF_TRUE    110  'to 110'

 L.  79        48  LOAD_FAST                'implementation_spec'
               50  LOAD_ATTR                keywords
               52  LOAD_FAST                'dispatcher_spec'
               54  LOAD_ATTR                keywords
               56  COMPARE_OP               !=

 L.  77        58  POP_JUMP_IF_TRUE    110  'to 110'

 L.  80        60  LOAD_GLOBAL              bool
               62  LOAD_FAST                'implementation_spec'
               64  LOAD_ATTR                defaults
               66  CALL_FUNCTION_1       1  ''

 L.  81        68  LOAD_GLOBAL              bool
               70  LOAD_FAST                'dispatcher_spec'
               72  LOAD_ATTR                defaults
               74  CALL_FUNCTION_1       1  ''

 L.  80        76  COMPARE_OP               !=

 L.  77        78  POP_JUMP_IF_TRUE    110  'to 110'

 L.  82        80  LOAD_FAST                'implementation_spec'
               82  LOAD_ATTR                defaults
               84  LOAD_CONST               None
               86  COMPARE_OP               is-not

 L.  77        88  POP_JUMP_IF_FALSE   122  'to 122'

 L.  83        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'implementation_spec'
               94  LOAD_ATTR                defaults
               96  CALL_FUNCTION_1       1  ''

 L.  84        98  LOAD_GLOBAL              len
              100  LOAD_FAST                'dispatcher_spec'
              102  LOAD_ATTR                defaults
              104  CALL_FUNCTION_1       1  ''

 L.  83       106  COMPARE_OP               !=

 L.  77       108  POP_JUMP_IF_FALSE   122  'to 122'
            110_0  COME_FROM            78  '78'
            110_1  COME_FROM            58  '58'
            110_2  COME_FROM            46  '46'
            110_3  COME_FROM            34  '34'

 L.  85       110  LOAD_GLOBAL              RuntimeError
              112  LOAD_STR                 'implementation and dispatcher for %s have different function signatures'

 L.  86       114  LOAD_FAST                'implementation'

 L.  85       116  BINARY_MODULO    
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           108  '108'
            122_1  COME_FROM            88  '88'

 L.  88       122  LOAD_FAST                'implementation_spec'
              124  LOAD_ATTR                defaults
              126  LOAD_CONST               None
              128  COMPARE_OP               is-not
              130  POP_JUMP_IF_FALSE   160  'to 160'

 L.  89       132  LOAD_FAST                'dispatcher_spec'
              134  LOAD_ATTR                defaults
              136  LOAD_CONST               (None,)
              138  LOAD_GLOBAL              len
              140  LOAD_FAST                'dispatcher_spec'
              142  LOAD_ATTR                defaults
              144  CALL_FUNCTION_1       1  ''
              146  BINARY_MULTIPLY  
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L.  90       152  LOAD_GLOBAL              RuntimeError
              154  LOAD_STR                 'dispatcher functions can only use None for default argument values'
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
            160_0  COME_FROM           150  '150'
            160_1  COME_FROM           130  '130'

Parse error at or near `COME_FROM' instruction at offset 160_0


def set_module(module):
    """Decorator for overriding __module__ on a function or class.

    Example usage::

        @set_module('numpy')
        def example():
            pass

        assert example.__module__ == 'numpy'
    """

    def decorator(func):
        if module is not None:
            func.__module__ = module
        return func

    return decorator


_wrapped_func_source = textwrap.dedent('\n    @functools.wraps(implementation)\n    def {name}(*args, **kwargs):\n        relevant_args = dispatcher(*args, **kwargs)\n        return implement_array_function(\n            implementation, {name}, relevant_args, args, kwargs)\n    ')

def array_function_dispatch(dispatcher, module=None, verify=True, docs_from_dispatcher=False):
    """Decorator for adding dispatch with the __array_function__ protocol.

    See NEP-18 for example usage.

    Parameters
    ----------
    dispatcher : callable
        Function that when called like ``dispatcher(*args, **kwargs)`` with
        arguments from the NumPy function call returns an iterable of
        array-like arguments to check for ``__array_function__``.
    module : str, optional
        __module__ attribute to set on new function, e.g., ``module='numpy'``.
        By default, module is copied from the decorated function.
    verify : bool, optional
        If True, verify the that the signature of the dispatcher and decorated
        function signatures match exactly: all required and optional arguments
        should appear in order with the same names, but the default values for
        all optional arguments should be ``None``. Only disable verification
        if the dispatcher's signature needs to deviate for some particular
        reason, e.g., because the function has a signature like
        ``func(*args, **kwargs)``.
    docs_from_dispatcher : bool, optional
        If True, copy docs from the dispatcher function onto the dispatched
        function, rather than from the implementation. This is useful for
        functions defined in C, which otherwise don't have docstrings.

    Returns
    -------
    Function suitable for decorating the implementation of a NumPy function.
    """
    if not ARRAY_FUNCTION_ENABLED:

        def decorator(implementation):
            if docs_from_dispatcher:
                add_docstring(implementation, dispatcher.__doc__)
            if module is not None:
                implementation.__module__ = module
            return implementation

        return decorator

    def decorator(implementation):
        if verify:
            verify_matching_signatures(implementation, dispatcher)
        if docs_from_dispatcher:
            add_docstring(implementation, dispatcher.__doc__)
        source = _wrapped_func_source.format(name=(implementation.__name__))
        source_object = compile(source,
          filename='<__array_function__ internals>', mode='exec')
        scope = {'implementation':implementation, 
         'dispatcher':dispatcher, 
         'functools':functools, 
         'implement_array_function':implement_array_function}
        exec(source_object, scope)
        public_api = scope[implementation.__name__]
        if module is not None:
            public_api.__module__ = module
        public_api._implementation = implementation
        return public_api

    return decorator


def array_function_from_dispatcher(implementation, module=None, verify=True, docs_from_dispatcher=True):
    """Like array_function_dispatcher, but with function arguments flipped."""

    def decorator(dispatcher):
        return array_function_dispatch(dispatcher,
          module, verify=verify, docs_from_dispatcher=docs_from_dispatcher)(implementation)

    return decorator