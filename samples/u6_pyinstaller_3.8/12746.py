# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\core\_asarray.py
"""
Functions in the ``as*array`` family that promote array-likes into arrays.

`require` fits this category despite its name not matching this pattern.
"""
from .overrides import array_function_dispatch, set_array_function_like_doc, set_module
from .multiarray import array
__all__ = [
 'asarray', 'asanyarray', 'ascontiguousarray', 'asfortranarray', 'require']

def _asarray_dispatcher(a, dtype=None, order=None, *, like=None):
    return (
     like,)


@set_array_function_like_doc
@set_module('numpy')
def asarray(a, dtype=None, order=None, *, like=None):
    """Convert the input to an array.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.  This
        includes lists, lists of tuples, tuples, tuples of tuples, tuples
        of lists and ndarrays.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F', 'A', 'K'}, optional
        Memory layout.  'A' and 'K' depend on the order of input array a.
        'C' row-major (C-style), 
        'F' column-major (Fortran-style) memory representation.
        'A' (any) means 'F' if `a` is Fortran contiguous, 'C' otherwise
        'K' (keep) preserve input order
        Defaults to 'C'.
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        Array interpretation of `a`.  No copy is performed if the input
        is already an ndarray with matching dtype and order.  If `a` is a
        subclass of ndarray, a base class ndarray is returned.

    See Also
    --------
    asanyarray : Similar function which passes through subclasses.
    ascontiguousarray : Convert input to a contiguous array.
    asfarray : Convert input to a floating point ndarray.
    asfortranarray : Convert input to an ndarray with column-major
                     memory order.
    asarray_chkfinite : Similar function which checks input for NaNs and Infs.
    fromiter : Create an array from an iterator.
    fromfunction : Construct an array by executing a function on grid
                   positions.

    Examples
    --------
    Convert a list into an array:

    >>> a = [1, 2]
    >>> np.asarray(a)
    array([1, 2])

    Existing arrays are not copied:

    >>> a = np.array([1, 2])
    >>> np.asarray(a) is a
    True

    If `dtype` is set, array is copied only if dtype does not match:

    >>> a = np.array([1, 2], dtype=np.float32)
    >>> np.asarray(a, dtype=np.float32) is a
    True
    >>> np.asarray(a, dtype=np.float64) is a
    False

    Contrary to `asanyarray`, ndarray subclasses are not passed through:

    >>> issubclass(np.recarray, np.ndarray)
    True
    >>> a = np.array([(1.0, 2), (3.0, 4)], dtype='f4,i4').view(np.recarray)
    >>> np.asarray(a) is a
    False
    >>> np.asanyarray(a) is a
    True

    """
    if like is not None:
        return _asarray_with_like(a, dtype=dtype, order=order, like=like)
    return array(a, dtype, copy=False, order=order)


_asarray_with_like = array_function_dispatch(_asarray_dispatcher)(asarray)

@set_array_function_like_doc
@set_module('numpy')
def asanyarray(a, dtype=None, order=None, *, like=None):
    """Convert the input to an ndarray, but pass ndarray subclasses through.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.  This
        includes scalars, lists, lists of tuples, tuples, tuples of tuples,
        tuples of lists, and ndarrays.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F', 'A', 'K'}, optional
        Memory layout.  'A' and 'K' depend on the order of input array a.
        'C' row-major (C-style), 
        'F' column-major (Fortran-style) memory representation.
        'A' (any) means 'F' if `a` is Fortran contiguous, 'C' otherwise
        'K' (keep) preserve input order
        Defaults to 'C'.
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray or an ndarray subclass
        Array interpretation of `a`.  If `a` is an ndarray or a subclass
        of ndarray, it is returned as-is and no copy is performed.

    See Also
    --------
    asarray : Similar function which always returns ndarrays.
    ascontiguousarray : Convert input to a contiguous array.
    asfarray : Convert input to a floating point ndarray.
    asfortranarray : Convert input to an ndarray with column-major
                     memory order.
    asarray_chkfinite : Similar function which checks input for NaNs and
                        Infs.
    fromiter : Create an array from an iterator.
    fromfunction : Construct an array by executing a function on grid
                   positions.

    Examples
    --------
    Convert a list into an array:

    >>> a = [1, 2]
    >>> np.asanyarray(a)
    array([1, 2])

    Instances of `ndarray` subclasses are passed through as-is:

    >>> a = np.array([(1.0, 2), (3.0, 4)], dtype='f4,i4').view(np.recarray)
    >>> np.asanyarray(a) is a
    True

    """
    if like is not None:
        return _asanyarray_with_like(a, dtype=dtype, order=order, like=like)
    return array(a, dtype, copy=False, order=order, subok=True)


_asanyarray_with_like = array_function_dispatch(_asarray_dispatcher)(asanyarray)

def _asarray_contiguous_fortran_dispatcher(a, dtype=None, *, like=None):
    return (
     like,)


@set_array_function_like_doc
@set_module('numpy')
def ascontiguousarray(a, dtype=None, *, like=None):
    """
    Return a contiguous array (ndim >= 1) in memory (C order).

    Parameters
    ----------
    a : array_like
        Input array.
    dtype : str or dtype object, optional
        Data-type of returned array.
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        Contiguous array of same shape and content as `a`, with type `dtype`
        if specified.

    See Also
    --------
    asfortranarray : Convert input to an ndarray with column-major
                     memory order.
    require : Return an ndarray that satisfies requirements.
    ndarray.flags : Information about the memory layout of the array.

    Examples
    --------
    >>> x = np.arange(6).reshape(2,3)
    >>> np.ascontiguousarray(x, dtype=np.float32)
    array([[0., 1., 2.],
           [3., 4., 5.]], dtype=float32)
    >>> x.flags['C_CONTIGUOUS']
    True

    Note: This function returns an array with at least one-dimension (1-d) 
    so it will not preserve 0-d arrays.  

    """
    if like is not None:
        return _ascontiguousarray_with_like(a, dtype=dtype, like=like)
    return array(a, dtype, copy=False, order='C', ndmin=1)


_ascontiguousarray_with_like = array_function_dispatch(_asarray_contiguous_fortran_dispatcher)(ascontiguousarray)

@set_array_function_like_doc
@set_module('numpy')
def asfortranarray(a, dtype=None, *, like=None):
    """
    Return an array (ndim >= 1) laid out in Fortran order in memory.

    Parameters
    ----------
    a : array_like
        Input array.
    dtype : str or dtype object, optional
        By default, the data-type is inferred from the input data.
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        The input `a` in Fortran, or column-major, order.

    See Also
    --------
    ascontiguousarray : Convert input to a contiguous (C order) array.
    asanyarray : Convert input to an ndarray with either row or
        column-major memory order.
    require : Return an ndarray that satisfies requirements.
    ndarray.flags : Information about the memory layout of the array.

    Examples
    --------
    >>> x = np.arange(6).reshape(2,3)
    >>> y = np.asfortranarray(x)
    >>> x.flags['F_CONTIGUOUS']
    False
    >>> y.flags['F_CONTIGUOUS']
    True

    Note: This function returns an array with at least one-dimension (1-d) 
    so it will not preserve 0-d arrays.  

    """
    if like is not None:
        return _asfortranarray_with_like(a, dtype=dtype, like=like)
    return array(a, dtype, copy=False, order='F', ndmin=1)


_asfortranarray_with_like = array_function_dispatch(_asarray_contiguous_fortran_dispatcher)(asfortranarray)

def _require_dispatcher(a, dtype=None, requirements=None, *, like=None):
    return (
     like,)


@set_array_function_like_doc
@set_module('numpy')
def require--- This code section failed: ---

 L. 365         0  LOAD_FAST                'like'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 366         8  LOAD_GLOBAL              _require_with_like

 L. 367        10  LOAD_FAST                'a'

 L. 368        12  LOAD_FAST                'dtype'

 L. 369        14  LOAD_FAST                'requirements'

 L. 370        16  LOAD_FAST                'like'

 L. 366        18  LOAD_CONST               ('dtype', 'requirements', 'like')
               20  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               22  RETURN_VALUE     
             24_0  COME_FROM             6  '6'

 L. 373        24  LOAD_STR                 'C'
               26  LOAD_STR                 'C'
               28  LOAD_STR                 'C'

 L. 374        30  LOAD_STR                 'F'

 L. 374        32  LOAD_STR                 'F'

 L. 374        34  LOAD_STR                 'F'

 L. 375        36  LOAD_STR                 'A'

 L. 375        38  LOAD_STR                 'A'

 L. 376        40  LOAD_STR                 'W'

 L. 376        42  LOAD_STR                 'W'

 L. 377        44  LOAD_STR                 'O'

 L. 377        46  LOAD_STR                 'O'

 L. 378        48  LOAD_STR                 'E'

 L. 378        50  LOAD_STR                 'E'

 L. 373        52  LOAD_CONST               ('C', 'C_CONTIGUOUS', 'CONTIGUOUS', 'F', 'F_CONTIGUOUS', 'FORTRAN', 'A', 'ALIGNED', 'W', 'WRITEABLE', 'O', 'OWNDATA', 'E', 'ENSUREARRAY')
               54  BUILD_CONST_KEY_MAP_14    14 
               56  STORE_DEREF              'possible_flags'

 L. 379        58  LOAD_FAST                'requirements'
               60  POP_JUMP_IF_TRUE     74  'to 74'

 L. 380        62  LOAD_GLOBAL              asanyarray
               64  LOAD_FAST                'a'
               66  LOAD_FAST                'dtype'
               68  LOAD_CONST               ('dtype',)
               70  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               72  RETURN_VALUE     
             74_0  COME_FROM            60  '60'

 L. 382        74  LOAD_CLOSURE             'possible_flags'
               76  BUILD_TUPLE_1         1 
               78  LOAD_SETCOMP             '<code_object <setcomp>>'
               80  LOAD_STR                 'require.<locals>.<setcomp>'
               82  MAKE_FUNCTION_8          'closure'
               84  LOAD_FAST                'requirements'
               86  GET_ITER         
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'requirements'

 L. 384        92  LOAD_STR                 'E'
               94  LOAD_FAST                'requirements'
               96  COMPARE_OP               in
               98  POP_JUMP_IF_FALSE   116  'to 116'

 L. 385       100  LOAD_FAST                'requirements'
              102  LOAD_METHOD              remove
              104  LOAD_STR                 'E'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 386       110  LOAD_CONST               False
              112  STORE_FAST               'subok'
              114  JUMP_FORWARD        120  'to 120'
            116_0  COME_FROM            98  '98'

 L. 388       116  LOAD_CONST               True
              118  STORE_FAST               'subok'
            120_0  COME_FROM           114  '114'

 L. 390       120  LOAD_STR                 'A'
              122  STORE_FAST               'order'

 L. 391       124  LOAD_FAST                'requirements'
              126  LOAD_STR                 'C'
              128  LOAD_STR                 'F'
              130  BUILD_SET_2           2 
              132  COMPARE_OP               >=
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L. 392       136  LOAD_GLOBAL              ValueError
              138  LOAD_STR                 'Cannot specify both "C" and "F" order'
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
              144  JUMP_FORWARD        192  'to 192'
            146_0  COME_FROM           134  '134'

 L. 393       146  LOAD_STR                 'F'
              148  LOAD_FAST                'requirements'
              150  COMPARE_OP               in
              152  POP_JUMP_IF_FALSE   170  'to 170'

 L. 394       154  LOAD_STR                 'F'
              156  STORE_FAST               'order'

 L. 395       158  LOAD_FAST                'requirements'
              160  LOAD_METHOD              remove
              162  LOAD_STR                 'F'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
              168  JUMP_FORWARD        192  'to 192'
            170_0  COME_FROM           152  '152'

 L. 396       170  LOAD_STR                 'C'
              172  LOAD_FAST                'requirements'
              174  COMPARE_OP               in
              176  POP_JUMP_IF_FALSE   192  'to 192'

 L. 397       178  LOAD_STR                 'C'
              180  STORE_FAST               'order'

 L. 398       182  LOAD_FAST                'requirements'
              184  LOAD_METHOD              remove
              186  LOAD_STR                 'C'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          
            192_0  COME_FROM           176  '176'
            192_1  COME_FROM           168  '168'
            192_2  COME_FROM           144  '144'

 L. 400       192  LOAD_GLOBAL              array
              194  LOAD_FAST                'a'
              196  LOAD_FAST                'dtype'
              198  LOAD_FAST                'order'
              200  LOAD_CONST               False
              202  LOAD_FAST                'subok'
              204  LOAD_CONST               ('dtype', 'order', 'copy', 'subok')
              206  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              208  STORE_FAST               'arr'

 L. 402       210  LOAD_FAST                'requirements'
              212  GET_ITER         
            214_0  COME_FROM           226  '226'
              214  FOR_ITER            244  'to 244'
              216  STORE_FAST               'prop'

 L. 403       218  LOAD_FAST                'arr'
              220  LOAD_ATTR                flags
              222  LOAD_FAST                'prop'
              224  BINARY_SUBSCR    
              226  POP_JUMP_IF_TRUE    214  'to 214'

 L. 404       228  LOAD_FAST                'arr'
              230  LOAD_METHOD              copy
              232  LOAD_FAST                'order'
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               'arr'

 L. 405       238  POP_TOP          
              240  BREAK_LOOP          244  'to 244'
              242  JUMP_BACK           214  'to 214'

 L. 406       244  LOAD_FAST                'arr'
              246  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 78


_require_with_like = array_function_dispatch(_require_dispatcher)(require)