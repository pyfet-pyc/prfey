# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\core\overrides.py
"""Implementation of __array_function__ overrides from NEP-18."""
import collections, functools, os, textwrap
from numpy.core._multiarray_umath import add_docstring, implement_array_function, _get_implementing_args
from numpy.compat._inspect import getargspec
ARRAY_FUNCTION_ENABLED = bool(int(os.environ.get('NUMPY_EXPERIMENTAL_ARRAY_FUNCTION', 1)))
array_function_like_doc = 'like : array_like\n        Reference object to allow the creation of arrays which are not\n        NumPy arrays. If an array-like passed in as ``like`` supports\n        the ``__array_function__`` protocol, the result will be defined\n        by it. In this case, it ensures the creation of an array object\n        compatible with that passed in via this argument.\n\n        .. note::\n            The ``like`` keyword is an experimental feature pending on\n            acceptance of :ref:`NEP 35 <NEP35>`.'

def set_array_function_like_doc--- This code section failed: ---

 L.  29         0  LOAD_FAST                'public_api'
                2  LOAD_ATTR                __doc__
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L.  30        10  LOAD_FAST                'public_api'
               12  LOAD_ATTR                __doc__
               14  LOAD_METHOD              replace

 L.  31        16  LOAD_STR                 '${ARRAY_FUNCTION_LIKE}'

 L.  32        18  LOAD_GLOBAL              array_function_like_doc

 L.  30        20  CALL_METHOD_2         2  ''
               22  LOAD_FAST                'public_api'
               24  STORE_ATTR               __doc__
             26_0  COME_FROM             8  '8'

 L.  34        26  LOAD_FAST                'public_api'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


add_docstring(implement_array_function, "\n    Implement a function with checks for __array_function__ overrides.\n\n    All arguments are required, and can only be passed by position.\n\n    Parameters\n    ----------\n    implementation : function\n        Function that implements the operation on NumPy array without\n        overrides when called like ``implementation(*args, **kwargs)``.\n    public_api : function\n        Function exposed by NumPy's public API originally called like\n        ``public_api(*args, **kwargs)`` on which arguments are now being\n        checked.\n    relevant_args : iterable\n        Iterable of arguments to check for __array_function__ methods.\n    args : tuple\n        Arbitrary positional arguments originally passed into ``public_api``.\n    kwargs : dict\n        Arbitrary keyword arguments originally passed into ``public_api``.\n\n    Returns\n    -------\n    Result from calling ``implementation()`` or an ``__array_function__``\n    method, as appropriate.\n\n    Raises\n    ------\n    TypeError : if no implementation is found.\n    ")
add_docstring(_get_implementing_args, '\n    Collect arguments on which to call __array_function__.\n\n    Parameters\n    ----------\n    relevant_args : iterable of array-like\n        Iterable of possibly array-like arguments to check for\n        __array_function__ methods.\n\n    Returns\n    -------\n    Sequence of arguments with __array_function__ methods, in the order in\n    which they should be called.\n    ')
ArgSpec = collections.namedtuple('ArgSpec', 'args varargs keywords defaults')

def verify_matching_signatures--- This code section failed: ---

 L.  95         0  LOAD_GLOBAL              ArgSpec
                2  LOAD_GLOBAL              getargspec
                4  LOAD_FAST                'implementation'
                6  CALL_FUNCTION_1       1  ''
                8  CALL_FUNCTION_EX      0  'positional arguments only'
               10  STORE_FAST               'implementation_spec'

 L.  96        12  LOAD_GLOBAL              ArgSpec
               14  LOAD_GLOBAL              getargspec
               16  LOAD_FAST                'dispatcher'
               18  CALL_FUNCTION_1       1  ''
               20  CALL_FUNCTION_EX      0  'positional arguments only'
               22  STORE_FAST               'dispatcher_spec'

 L.  98        24  LOAD_FAST                'implementation_spec'
               26  LOAD_ATTR                args
               28  LOAD_FAST                'dispatcher_spec'
               30  LOAD_ATTR                args
               32  COMPARE_OP               !=
               34  POP_JUMP_IF_TRUE    110  'to 110'

 L.  99        36  LOAD_FAST                'implementation_spec'
               38  LOAD_ATTR                varargs
               40  LOAD_FAST                'dispatcher_spec'
               42  LOAD_ATTR                varargs
               44  COMPARE_OP               !=

 L.  98        46  POP_JUMP_IF_TRUE    110  'to 110'

 L. 100        48  LOAD_FAST                'implementation_spec'
               50  LOAD_ATTR                keywords
               52  LOAD_FAST                'dispatcher_spec'
               54  LOAD_ATTR                keywords
               56  COMPARE_OP               !=

 L.  98        58  POP_JUMP_IF_TRUE    110  'to 110'

 L. 101        60  LOAD_GLOBAL              bool
               62  LOAD_FAST                'implementation_spec'
               64  LOAD_ATTR                defaults
               66  CALL_FUNCTION_1       1  ''

 L. 102        68  LOAD_GLOBAL              bool
               70  LOAD_FAST                'dispatcher_spec'
               72  LOAD_ATTR                defaults
               74  CALL_FUNCTION_1       1  ''

 L. 101        76  COMPARE_OP               !=

 L.  98        78  POP_JUMP_IF_TRUE    110  'to 110'

 L. 103        80  LOAD_FAST                'implementation_spec'
               82  LOAD_ATTR                defaults
               84  LOAD_CONST               None
               86  <117>                 1  ''

 L.  98        88  POP_JUMP_IF_FALSE   122  'to 122'

 L. 104        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'implementation_spec'
               94  LOAD_ATTR                defaults
               96  CALL_FUNCTION_1       1  ''

 L. 105        98  LOAD_GLOBAL              len
              100  LOAD_FAST                'dispatcher_spec'
              102  LOAD_ATTR                defaults
              104  CALL_FUNCTION_1       1  ''

 L. 104       106  COMPARE_OP               !=

 L.  98       108  POP_JUMP_IF_FALSE   122  'to 122'
            110_0  COME_FROM            78  '78'
            110_1  COME_FROM            58  '58'
            110_2  COME_FROM            46  '46'
            110_3  COME_FROM            34  '34'

 L. 106       110  LOAD_GLOBAL              RuntimeError
              112  LOAD_STR                 'implementation and dispatcher for %s have different function signatures'

 L. 107       114  LOAD_FAST                'implementation'

 L. 106       116  BINARY_MODULO    
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           108  '108'
            122_1  COME_FROM            88  '88'

 L. 109       122  LOAD_FAST                'implementation_spec'
              124  LOAD_ATTR                defaults
              126  LOAD_CONST               None
              128  <117>                 1  ''
              130  POP_JUMP_IF_FALSE   160  'to 160'

 L. 110       132  LOAD_FAST                'dispatcher_spec'
              134  LOAD_ATTR                defaults
              136  LOAD_CONST               (None,)
              138  LOAD_GLOBAL              len
              140  LOAD_FAST                'dispatcher_spec'
              142  LOAD_ATTR                defaults
              144  CALL_FUNCTION_1       1  ''
              146  BINARY_MULTIPLY  
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L. 111       152  LOAD_GLOBAL              RuntimeError
              154  LOAD_STR                 'dispatcher functions can only use None for default argument values'
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
            160_0  COME_FROM           150  '150'
            160_1  COME_FROM           130  '130'

Parse error at or near `<117>' instruction at offset 86


def set_module(module):
    """Decorator for overriding __module__ on a function or class.

    Example usage::

        @set_module('numpy')
        def example():
            pass

        assert example.__module__ == 'numpy'
    """

    def decorator--- This code section failed: ---

 L. 127         0  LOAD_DEREF               'module'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 128         8  LOAD_DEREF               'module'
               10  LOAD_FAST                'func'
               12  STORE_ATTR               __module__
             14_0  COME_FROM             6  '6'

 L. 129        14  LOAD_FAST                'func'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

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

        def decorator--- This code section failed: ---

 L. 180         0  LOAD_DEREF               'docs_from_dispatcher'
                2  POP_JUMP_IF_FALSE    16  'to 16'

 L. 181         4  LOAD_GLOBAL              add_docstring
                6  LOAD_FAST                'implementation'
                8  LOAD_DEREF               'dispatcher'
               10  LOAD_ATTR                __doc__
               12  CALL_FUNCTION_2       2  ''
               14  POP_TOP          
             16_0  COME_FROM             2  '2'

 L. 182        16  LOAD_DEREF               'module'
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 183        24  LOAD_DEREF               'module'
               26  LOAD_FAST                'implementation'
               28  STORE_ATTR               __module__
             30_0  COME_FROM            22  '22'

 L. 184        30  LOAD_FAST                'implementation'
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 20

        return decorator

    def decorator--- This code section failed: ---

 L. 188         0  LOAD_DEREF               'verify'
                2  POP_JUMP_IF_FALSE    14  'to 14'

 L. 189         4  LOAD_GLOBAL              verify_matching_signatures
                6  LOAD_FAST                'implementation'
                8  LOAD_DEREF               'dispatcher'
               10  CALL_FUNCTION_2       2  ''
               12  POP_TOP          
             14_0  COME_FROM             2  '2'

 L. 191        14  LOAD_DEREF               'docs_from_dispatcher'
               16  POP_JUMP_IF_FALSE    30  'to 30'

 L. 192        18  LOAD_GLOBAL              add_docstring
               20  LOAD_FAST                'implementation'
               22  LOAD_DEREF               'dispatcher'
               24  LOAD_ATTR                __doc__
               26  CALL_FUNCTION_2       2  ''
               28  POP_TOP          
             30_0  COME_FROM            16  '16'

 L. 199        30  LOAD_GLOBAL              _wrapped_func_source
               32  LOAD_ATTR                format
               34  LOAD_FAST                'implementation'
               36  LOAD_ATTR                __name__
               38  LOAD_CONST               ('name',)
               40  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               42  STORE_FAST               'source'

 L. 201        44  LOAD_GLOBAL              compile

 L. 202        46  LOAD_FAST                'source'
               48  LOAD_STR                 '<__array_function__ internals>'
               50  LOAD_STR                 'exec'

 L. 201        52  LOAD_CONST               ('filename', 'mode')
               54  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               56  STORE_FAST               'source_object'

 L. 204        58  LOAD_FAST                'implementation'

 L. 205        60  LOAD_DEREF               'dispatcher'

 L. 206        62  LOAD_GLOBAL              functools

 L. 207        64  LOAD_GLOBAL              implement_array_function

 L. 203        66  LOAD_CONST               ('implementation', 'dispatcher', 'functools', 'implement_array_function')
               68  BUILD_CONST_KEY_MAP_4     4 
               70  STORE_FAST               'scope'

 L. 209        72  LOAD_GLOBAL              exec
               74  LOAD_FAST                'source_object'
               76  LOAD_FAST                'scope'
               78  CALL_FUNCTION_2       2  ''
               80  POP_TOP          

 L. 211        82  LOAD_FAST                'scope'
               84  LOAD_FAST                'implementation'
               86  LOAD_ATTR                __name__
               88  BINARY_SUBSCR    
               90  STORE_FAST               'public_api'

 L. 213        92  LOAD_DEREF               'module'
               94  LOAD_CONST               None
               96  <117>                 1  ''
               98  POP_JUMP_IF_FALSE   106  'to 106'

 L. 214       100  LOAD_DEREF               'module'
              102  LOAD_FAST                'public_api'
              104  STORE_ATTR               __module__
            106_0  COME_FROM            98  '98'

 L. 216       106  LOAD_FAST                'implementation'
              108  LOAD_FAST                'public_api'
              110  STORE_ATTR               _implementation

 L. 218       112  LOAD_FAST                'public_api'
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 96

    return decorator


def array_function_from_dispatcher(implementation, module=None, verify=True, docs_from_dispatcher=True):
    """Like array_function_dispatcher, but with function arguments flipped."""

    def decorator(dispatcher):
        return array_function_dispatch(dispatcher,
          module, verify=verify, docs_from_dispatcher=docs_from_dispatcher)(implementation)

    return decorator