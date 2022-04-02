# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\lib\stride_tricks.py
"""
Utilities that manipulate strides to achieve desirable effects.

An explanation of strides can be found in the "ndarray.rst" file in the
NumPy reference guide.

"""
import numpy as np
from numpy.core.overrides import array_function_dispatch
__all__ = [
 'broadcast_to', 'broadcast_arrays']

class DummyArray:
    __doc__ = 'Dummy object that just exists to hang __array_interface__ dictionaries\n    and possibly keep alive a reference to a base array.\n    '

    def __init__(self, interface, base=None):
        self.__array_interface__ = interface
        self.base = base


def _maybe_view_as_subclass--- This code section failed: ---

 L.  25         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'original_array'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              type
                8  LOAD_FAST                'new_array'
               10  CALL_FUNCTION_1       1  ''
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    48  'to 48'

 L.  28        16  LOAD_FAST                'new_array'
               18  LOAD_ATTR                view
               20  LOAD_GLOBAL              type
               22  LOAD_FAST                'original_array'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_CONST               ('type',)
               28  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               30  STORE_FAST               'new_array'

 L.  32        32  LOAD_FAST                'new_array'
               34  LOAD_ATTR                __array_finalize__
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L.  33        38  LOAD_FAST                'new_array'
               40  LOAD_METHOD              __array_finalize__
               42  LOAD_FAST                'original_array'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            36  '36'
             48_1  COME_FROM            14  '14'

 L.  34        48  LOAD_FAST                'new_array'
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def as_strided--- This code section failed: ---

 L.  94         0  LOAD_GLOBAL              np
                2  LOAD_ATTR                array
                4  LOAD_FAST                'x'
                6  LOAD_CONST               False
                8  LOAD_FAST                'subok'
               10  LOAD_CONST               ('copy', 'subok')
               12  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               14  STORE_FAST               'x'

 L.  95        16  LOAD_GLOBAL              dict
               18  LOAD_FAST                'x'
               20  LOAD_ATTR                __array_interface__
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'interface'

 L.  96        26  LOAD_FAST                'shape'
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L.  97        34  LOAD_GLOBAL              tuple
               36  LOAD_FAST                'shape'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_FAST                'interface'
               42  LOAD_STR                 'shape'
               44  STORE_SUBSCR     
             46_0  COME_FROM            32  '32'

 L.  98        46  LOAD_FAST                'strides'
               48  LOAD_CONST               None
               50  <117>                 1  ''
               52  POP_JUMP_IF_FALSE    66  'to 66'

 L.  99        54  LOAD_GLOBAL              tuple
               56  LOAD_FAST                'strides'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'interface'
               62  LOAD_STR                 'strides'
               64  STORE_SUBSCR     
             66_0  COME_FROM            52  '52'

 L. 101        66  LOAD_GLOBAL              np
               68  LOAD_METHOD              asarray
               70  LOAD_GLOBAL              DummyArray
               72  LOAD_FAST                'interface'
               74  LOAD_FAST                'x'
               76  LOAD_CONST               ('base',)
               78  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'array'

 L. 104        84  LOAD_FAST                'x'
               86  LOAD_ATTR                dtype
               88  LOAD_FAST                'array'
               90  STORE_ATTR               dtype

 L. 106        92  LOAD_GLOBAL              _maybe_view_as_subclass
               94  LOAD_FAST                'x'
               96  LOAD_FAST                'array'
               98  CALL_FUNCTION_2       2  ''
              100  STORE_FAST               'view'

 L. 108       102  LOAD_FAST                'view'
              104  LOAD_ATTR                flags
              106  LOAD_ATTR                writeable
              108  POP_JUMP_IF_FALSE   122  'to 122'
              110  LOAD_FAST                'writeable'
              112  POP_JUMP_IF_TRUE    122  'to 122'

 L. 109       114  LOAD_CONST               False
              116  LOAD_FAST                'view'
              118  LOAD_ATTR                flags
              120  STORE_ATTR               writeable
            122_0  COME_FROM           112  '112'
            122_1  COME_FROM           108  '108'

 L. 111       122  LOAD_FAST                'view'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 30


def _broadcast_to--- This code section failed: ---

 L. 115         0  LOAD_GLOBAL              np
                2  LOAD_METHOD              iterable
                4  LOAD_FAST                'shape'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'
               10  LOAD_GLOBAL              tuple
               12  LOAD_FAST                'shape'
               14  CALL_FUNCTION_1       1  ''
               16  JUMP_FORWARD         22  'to 22'
             18_0  COME_FROM             8  '8'
               18  LOAD_FAST                'shape'
               20  BUILD_TUPLE_1         1 
             22_0  COME_FROM            16  '16'
               22  STORE_FAST               'shape'

 L. 116        24  LOAD_GLOBAL              np
               26  LOAD_ATTR                array
               28  LOAD_FAST                'array'
               30  LOAD_CONST               False
               32  LOAD_FAST                'subok'
               34  LOAD_CONST               ('copy', 'subok')
               36  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               38  STORE_FAST               'array'

 L. 117        40  LOAD_FAST                'shape'
               42  POP_JUMP_IF_TRUE     58  'to 58'
               44  LOAD_FAST                'array'
               46  LOAD_ATTR                shape
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L. 118        50  LOAD_GLOBAL              ValueError
               52  LOAD_STR                 'cannot broadcast a non-scalar to a scalar array'
               54  CALL_FUNCTION_1       1  ''
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            48  '48'
             58_1  COME_FROM            42  '42'

 L. 119        58  LOAD_GLOBAL              any
               60  LOAD_GENEXPR             '<code_object <genexpr>>'
               62  LOAD_STR                 '_broadcast_to.<locals>.<genexpr>'
               64  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               66  LOAD_FAST                'shape'
               68  GET_ITER         
               70  CALL_FUNCTION_1       1  ''
               72  CALL_FUNCTION_1       1  ''
               74  POP_JUMP_IF_FALSE    84  'to 84'

 L. 120        76  LOAD_GLOBAL              ValueError
               78  LOAD_STR                 'all elements of broadcast shape must be non-negative'
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            74  '74'

 L. 122        84  BUILD_LIST_0          0 
               86  STORE_FAST               'extras'

 L. 123        88  LOAD_GLOBAL              np
               90  LOAD_ATTR                nditer

 L. 124        92  LOAD_FAST                'array'
               94  BUILD_TUPLE_1         1 
               96  BUILD_LIST_0          0 
               98  LOAD_CONST               ('multi_index', 'refs_ok', 'zerosize_ok')
              100  CALL_FINALLY        103  'to 103'
              102  LOAD_FAST                'extras'
              104  BINARY_ADD       

 L. 125       106  LOAD_STR                 'readonly'
              108  BUILD_LIST_1          1 
              110  LOAD_FAST                'shape'
              112  LOAD_STR                 'C'

 L. 123       114  LOAD_CONST               ('flags', 'op_flags', 'itershape', 'order')
              116  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              118  STORE_FAST               'it'

 L. 126       120  LOAD_FAST                'it'
              122  SETUP_WITH          150  'to 150'
              124  POP_TOP          

 L. 128       126  LOAD_FAST                'it'
              128  LOAD_ATTR                itviews
              130  LOAD_CONST               0
              132  BINARY_SUBSCR    
              134  STORE_FAST               'broadcast'
              136  POP_BLOCK        
              138  LOAD_CONST               None
              140  DUP_TOP          
              142  DUP_TOP          
              144  CALL_FUNCTION_3       3  ''
              146  POP_TOP          
              148  JUMP_FORWARD        166  'to 166'
            150_0  COME_FROM_WITH      122  '122'
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

 L. 129       166  LOAD_GLOBAL              _maybe_view_as_subclass
              168  LOAD_FAST                'array'
              170  LOAD_FAST                'broadcast'
              172  CALL_FUNCTION_2       2  ''
              174  STORE_FAST               'result'

 L. 131       176  LOAD_FAST                'readonly'
              178  POP_JUMP_IF_TRUE    204  'to 204'
              180  LOAD_FAST                'array'
              182  LOAD_ATTR                flags
              184  LOAD_ATTR                _writeable_no_warn
              186  POP_JUMP_IF_FALSE   204  'to 204'

 L. 132       188  LOAD_CONST               True
              190  LOAD_FAST                'result'
              192  LOAD_ATTR                flags
              194  STORE_ATTR               writeable

 L. 133       196  LOAD_CONST               True
              198  LOAD_FAST                'result'
              200  LOAD_ATTR                flags
              202  STORE_ATTR               _warn_on_write
            204_0  COME_FROM           186  '186'
            204_1  COME_FROM           178  '178'

 L. 134       204  LOAD_FAST                'result'
              206  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 100


def _broadcast_to_dispatcher(array, shape, subok=None):
    return (
     array,)


@array_function_dispatch(_broadcast_to_dispatcher, module='numpy')
def broadcast_to(array, shape, subok=False):
    """Broadcast an array to a new shape.

    Parameters
    ----------
    array : array_like
        The array to broadcast.
    shape : tuple
        The shape of the desired array.
    subok : bool, optional
        If True, then sub-classes will be passed-through, otherwise
        the returned array will be forced to be a base-class array (default).

    Returns
    -------
    broadcast : array
        A readonly view on the original array with the given shape. It is
        typically not contiguous. Furthermore, more than one element of a
        broadcasted array may refer to a single memory location.

    Raises
    ------
    ValueError
        If the array is not compatible with the new shape according to NumPy's
        broadcasting rules.

    Notes
    -----
    .. versionadded:: 1.10.0

    Examples
    --------
    >>> x = np.array([1, 2, 3])
    >>> np.broadcast_to(x, (3, 3))
    array([[1, 2, 3],
           [1, 2, 3],
           [1, 2, 3]])
    """
    return _broadcast_to(array, shape, subok=subok, readonly=True)


def _broadcast_shape--- This code section failed: ---

 L. 189         0  LOAD_GLOBAL              np
                2  LOAD_ATTR                broadcast
                4  LOAD_FAST                'args'
                6  LOAD_CONST               None
                8  LOAD_CONST               32
               10  BUILD_SLICE_2         2 
               12  BINARY_SUBSCR    
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  STORE_FAST               'b'

 L. 191        18  LOAD_GLOBAL              range
               20  LOAD_CONST               32
               22  LOAD_GLOBAL              len
               24  LOAD_FAST                'args'
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_CONST               31
               30  CALL_FUNCTION_3       3  ''
               32  GET_ITER         
             34_0  COME_FROM            80  '80'
               34  FOR_ITER             82  'to 82'
               36  STORE_FAST               'pos'

 L. 195        38  LOAD_GLOBAL              broadcast_to
               40  LOAD_CONST               0
               42  LOAD_FAST                'b'
               44  LOAD_ATTR                shape
               46  CALL_FUNCTION_2       2  ''
               48  STORE_FAST               'b'

 L. 196        50  LOAD_GLOBAL              np
               52  LOAD_ATTR                broadcast
               54  LOAD_FAST                'b'
               56  BUILD_LIST_1          1 
               58  LOAD_FAST                'args'
               60  LOAD_FAST                'pos'
               62  LOAD_FAST                'pos'
               64  LOAD_CONST               31
               66  BINARY_ADD       
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  CALL_FINALLY         75  'to 75'
               74  WITH_CLEANUP_FINISH
               76  CALL_FUNCTION_EX      0  'positional arguments only'
               78  STORE_FAST               'b'
               80  JUMP_BACK            34  'to 34'
             82_0  COME_FROM            34  '34'

 L. 197        82  LOAD_FAST                'b'
               84  LOAD_ATTR                shape
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 72


def _broadcast_arrays_dispatcher(*args, subok=None):
    return args


@array_function_dispatch(_broadcast_arrays_dispatcher, module='numpy')
def broadcast_arrays(*args, subok=False):
    """
    Broadcast any number of arrays against each other.

    Parameters
    ----------
    `*args` : array_likes
        The arrays to broadcast.

    subok : bool, optional
        If True, then sub-classes will be passed-through, otherwise
        the returned arrays will be forced to be a base-class array (default).

    Returns
    -------
    broadcasted : list of arrays
        These arrays are views on the original arrays.  They are typically
        not contiguous.  Furthermore, more than one element of a
        broadcasted array may refer to a single memory location. If you need
        to write to the arrays, make copies first. While you can set the
        ``writable`` flag True, writing to a single output value may end up
        changing more than one location in the output array.

        .. deprecated:: 1.17
            The output is currently marked so that if written to, a deprecation
            warning will be emitted. A future version will set the
            ``writable`` flag False so writing to it will raise an error.

    Examples
    --------
    >>> x = np.array([[1,2,3]])
    >>> y = np.array([[4],[5]])
    >>> np.broadcast_arrays(x, y)
    [array([[1, 2, 3],
           [1, 2, 3]]), array([[4, 4, 4],
           [5, 5, 5]])]

    Here is a useful idiom for getting contiguous copies instead of
    non-contiguous views.

    >>> [np.array(a) for a in np.broadcast_arrays(x, y)]
    [array([[1, 2, 3],
           [1, 2, 3]]), array([[4, 4, 4],
           [5, 5, 5]])]

    """
    args = [np.array(_m, copy=False, subok=subok) for _m in args]
    shape = _broadcast_shape(*args)
    if all((array.shape == shape for array in args)):
        return args
    return [_broadcast_to(array, shape, subok=subok, readonly=False) for array in args]