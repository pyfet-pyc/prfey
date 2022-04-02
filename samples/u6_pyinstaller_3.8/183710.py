# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\core\_asarray.py
"""
Functions in the ``as*array`` family that promote array-likes into arrays.

`require` fits this category despite its name not matching this pattern.
"""
from __future__ import division, absolute_import, print_function
from .overrides import set_module
from .multiarray import array
__all__ = [
 'asarray', 'asanyarray', 'ascontiguousarray', 'asfortranarray', 'require']

@set_module('numpy')
def asarray(a, dtype=None, order=None):
    """Convert the input to an array.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.  This
        includes lists, lists of tuples, tuples, tuples of tuples, tuples
        of lists and ndarrays.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F'}, optional
        Whether to use row-major (C-style) or
        column-major (Fortran-style) memory representation.
        Defaults to 'C'.

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
    return array(a, dtype, copy=False, order=order)


@set_module('numpy')
def asanyarray(a, dtype=None, order=None):
    """Convert the input to an ndarray, but pass ndarray subclasses through.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.  This
        includes scalars, lists, lists of tuples, tuples, tuples of tuples,
        tuples of lists, and ndarrays.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F'}, optional
        Whether to use row-major (C-style) or column-major
        (Fortran-style) memory representation.  Defaults to 'C'.

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
    return array(a, dtype, copy=False, order=order, subok=True)


@set_module('numpy')
def ascontiguousarray(a, dtype=None):
    """
    Return a contiguous array (ndim >= 1) in memory (C order).

    Parameters
    ----------
    a : array_like
        Input array.
    dtype : str or dtype object, optional
        Data-type of returned array.

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
    return array(a, dtype, copy=False, order='C', ndmin=1)


@set_module('numpy')
def asfortranarray(a, dtype=None):
    """
    Return an array (ndim >= 1) laid out in Fortran order in memory.

    Parameters
    ----------
    a : array_like
        Input array.
    dtype : str or dtype object, optional
        By default, the data-type is inferred from the input data.

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
    return array(a, dtype, copy=False, order='F', ndmin=1)


@set_module('numpy')
def require--- This code section failed: ---

 L. 291         0  LOAD_STR                 'C'
                2  LOAD_STR                 'C'
                4  LOAD_STR                 'C'

 L. 292         6  LOAD_STR                 'F'

 L. 292         8  LOAD_STR                 'F'

 L. 292        10  LOAD_STR                 'F'

 L. 293        12  LOAD_STR                 'A'

 L. 293        14  LOAD_STR                 'A'

 L. 294        16  LOAD_STR                 'W'

 L. 294        18  LOAD_STR                 'W'

 L. 295        20  LOAD_STR                 'O'

 L. 295        22  LOAD_STR                 'O'

 L. 296        24  LOAD_STR                 'E'

 L. 296        26  LOAD_STR                 'E'

 L. 291        28  LOAD_CONST               ('C', 'C_CONTIGUOUS', 'CONTIGUOUS', 'F', 'F_CONTIGUOUS', 'FORTRAN', 'A', 'ALIGNED', 'W', 'WRITEABLE', 'O', 'OWNDATA', 'E', 'ENSUREARRAY')
               30  BUILD_CONST_KEY_MAP_14    14 
               32  STORE_DEREF              'possible_flags'

 L. 297        34  LOAD_FAST                'requirements'
               36  POP_JUMP_IF_TRUE     50  'to 50'

 L. 298        38  LOAD_GLOBAL              asanyarray
               40  LOAD_FAST                'a'
               42  LOAD_FAST                'dtype'
               44  LOAD_CONST               ('dtype',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  RETURN_VALUE     
             50_0  COME_FROM            36  '36'

 L. 300        50  LOAD_CLOSURE             'possible_flags'
               52  BUILD_TUPLE_1         1 
               54  LOAD_SETCOMP             '<code_object <setcomp>>'
               56  LOAD_STR                 'require.<locals>.<setcomp>'
               58  MAKE_FUNCTION_8          'closure'
               60  LOAD_FAST                'requirements'
               62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'requirements'

 L. 302        68  LOAD_STR                 'E'
               70  LOAD_FAST                'requirements'
               72  COMPARE_OP               in
               74  POP_JUMP_IF_FALSE    92  'to 92'

 L. 303        76  LOAD_FAST                'requirements'
               78  LOAD_METHOD              remove
               80  LOAD_STR                 'E'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L. 304        86  LOAD_CONST               False
               88  STORE_FAST               'subok'
               90  JUMP_FORWARD         96  'to 96'
             92_0  COME_FROM            74  '74'

 L. 306        92  LOAD_CONST               True
               94  STORE_FAST               'subok'
             96_0  COME_FROM            90  '90'

 L. 308        96  LOAD_STR                 'A'
               98  STORE_FAST               'order'

 L. 309       100  LOAD_FAST                'requirements'
              102  LOAD_STR                 'C'
              104  LOAD_STR                 'F'
              106  BUILD_SET_2           2 
              108  COMPARE_OP               >=
              110  POP_JUMP_IF_FALSE   122  'to 122'

 L. 310       112  LOAD_GLOBAL              ValueError
              114  LOAD_STR                 'Cannot specify both "C" and "F" order'
              116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
              120  JUMP_FORWARD        168  'to 168'
            122_0  COME_FROM           110  '110'

 L. 311       122  LOAD_STR                 'F'
              124  LOAD_FAST                'requirements'
              126  COMPARE_OP               in
              128  POP_JUMP_IF_FALSE   146  'to 146'

 L. 312       130  LOAD_STR                 'F'
              132  STORE_FAST               'order'

 L. 313       134  LOAD_FAST                'requirements'
              136  LOAD_METHOD              remove
              138  LOAD_STR                 'F'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_FORWARD        168  'to 168'
            146_0  COME_FROM           128  '128'

 L. 314       146  LOAD_STR                 'C'
              148  LOAD_FAST                'requirements'
              150  COMPARE_OP               in
              152  POP_JUMP_IF_FALSE   168  'to 168'

 L. 315       154  LOAD_STR                 'C'
              156  STORE_FAST               'order'

 L. 316       158  LOAD_FAST                'requirements'
              160  LOAD_METHOD              remove
              162  LOAD_STR                 'C'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
            168_0  COME_FROM           152  '152'
            168_1  COME_FROM           144  '144'
            168_2  COME_FROM           120  '120'

 L. 318       168  LOAD_GLOBAL              array
              170  LOAD_FAST                'a'
              172  LOAD_FAST                'dtype'
              174  LOAD_FAST                'order'
              176  LOAD_CONST               False
              178  LOAD_FAST                'subok'
              180  LOAD_CONST               ('dtype', 'order', 'copy', 'subok')
              182  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              184  STORE_FAST               'arr'

 L. 320       186  LOAD_FAST                'requirements'
              188  GET_ITER         
            190_0  COME_FROM           202  '202'
              190  FOR_ITER            220  'to 220'
              192  STORE_FAST               'prop'

 L. 321       194  LOAD_FAST                'arr'
              196  LOAD_ATTR                flags
              198  LOAD_FAST                'prop'
              200  BINARY_SUBSCR    
              202  POP_JUMP_IF_TRUE    190  'to 190'

 L. 322       204  LOAD_FAST                'arr'
              206  LOAD_METHOD              copy
              208  LOAD_FAST                'order'
              210  CALL_METHOD_1         1  ''
              212  STORE_FAST               'arr'

 L. 323       214  POP_TOP          
              216  BREAK_LOOP          220  'to 220'
              218  JUMP_BACK           190  'to 190'

 L. 324       220  LOAD_FAST                'arr'
              222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 54