# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\core\numeric.py
import functools, itertools, operator, sys, warnings, numbers, numpy as np
from . import multiarray
from .multiarray import _fastCopyAndTranspose as fastCopyAndTranspose, ALLOW_THREADS, BUFSIZE, CLIP, MAXDIMS, MAY_SHARE_BOUNDS, MAY_SHARE_EXACT, RAISE, WRAP, arange, array, broadcast, can_cast, compare_chararrays, concatenate, copyto, dot, dtype, empty, empty_like, flatiter, frombuffer, fromfile, fromiter, fromstring, inner, lexsort, matmul, may_share_memory, min_scalar_type, ndarray, nditer, nested_iters, promote_types, putmask, result_type, set_numeric_ops, shares_memory, vdot, where, zeros, normalize_axis_index
from . import overrides
from . import umath
from . import shape_base
from .overrides import set_module
from .umath import multiply, invert, sin, PINF, NAN
from . import numerictypes
from .numerictypes import longlong, intc, int_, float_, complex_, bool_
from ._exceptions import TooHardError, AxisError
from ._asarray import asarray, asanyarray
from ._ufunc_config import errstate
bitwise_not = invert
ufunc = type(sin)
newaxis = None
array_function_dispatch = functools.partial((overrides.array_function_dispatch),
  module='numpy')
__all__ = [
 'newaxis', 'ndarray', 'flatiter', 'nditer', 'nested_iters', 'ufunc',
 'arange', 'array', 'zeros', 'count_nonzero', 'empty', 'broadcast', 'dtype',
 'fromstring', 'fromfile', 'frombuffer', 'where',
 'argwhere', 'copyto', 'concatenate', 'fastCopyAndTranspose', 'lexsort',
 'set_numeric_ops', 'can_cast', 'promote_types', 'min_scalar_type',
 'result_type', 'isfortran', 'empty_like', 'zeros_like', 'ones_like',
 'correlate', 'convolve', 'inner', 'dot', 'outer', 'vdot', 'roll',
 'rollaxis', 'moveaxis', 'cross', 'tensordot', 'little_endian',
 'fromiter', 'array_equal', 'array_equiv', 'indices', 'fromfunction',
 'isclose', 'isscalar', 'binary_repr', 'base_repr', 'ones',
 'identity', 'allclose', 'compare_chararrays', 'putmask',
 'flatnonzero', 'Inf', 'inf', 'infty', 'Infinity', 'nan', 'NaN',
 'False_', 'True_', 'bitwise_not', 'CLIP', 'RAISE', 'WRAP', 'MAXDIMS',
 'BUFSIZE', 'ALLOW_THREADS', 'ComplexWarning', 'full', 'full_like',
 'matmul', 'shares_memory', 'may_share_memory', 'MAY_SHARE_BOUNDS',
 'MAY_SHARE_EXACT', 'TooHardError', 'AxisError']

@set_module('numpy')
class ComplexWarning(RuntimeWarning):
    __doc__ = '\n    The warning raised when casting a complex dtype to a real dtype.\n\n    As implemented, casting a complex number to a real discards its imaginary\n    part, but this behavior may not be what the user actually wants.\n\n    '


def _zeros_like_dispatcher(a, dtype=None, order=None, subok=None, shape=None):
    return (
     a,)


@array_function_dispatch(_zeros_like_dispatcher)
def zeros_like(a, dtype=None, order='K', subok=True, shape=None):
    """
    Return an array of zeros with the same shape and type as a given array.

    Parameters
    ----------
    a : array_like
        The shape and data-type of `a` define these same attributes of
        the returned array.
    dtype : data-type, optional
        Overrides the data type of the result.

        .. versionadded:: 1.6.0
    order : {'C', 'F', 'A', or 'K'}, optional
        Overrides the memory layout of the result. 'C' means C-order,
        'F' means F-order, 'A' means 'F' if `a` is Fortran contiguous,
        'C' otherwise. 'K' means match the layout of `a` as closely
        as possible.

        .. versionadded:: 1.6.0
    subok : bool, optional.
        If True, then the newly created array will use the sub-class
        type of 'a', otherwise it will be a base-class array. Defaults
        to True.
    shape : int or sequence of ints, optional.
        Overrides the shape of the result. If order='K' and the number of
        dimensions is unchanged, will try to keep order, otherwise,
        order='C' is implied.

        .. versionadded:: 1.17.0

    Returns
    -------
    out : ndarray
        Array of zeros with the same shape and type as `a`.

    See Also
    --------
    empty_like : Return an empty array with shape and type of input.
    ones_like : Return an array of ones with shape and type of input.
    full_like : Return a new array with shape of input filled with value.
    zeros : Return a new array setting values to zero.

    Examples
    --------
    >>> x = np.arange(6)
    >>> x = x.reshape((2, 3))
    >>> x
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.zeros_like(x)
    array([[0, 0, 0],
           [0, 0, 0]])

    >>> y = np.arange(3, dtype=float)
    >>> y
    array([0., 1., 2.])
    >>> np.zeros_like(y)
    array([0.,  0.,  0.])

    """
    res = empty_like(a, dtype=dtype, order=order, subok=subok, shape=shape)
    z = zeros(1, dtype=(res.dtype))
    multiarray.copyto(res, z, casting='unsafe')
    return res


@set_module('numpy')
def ones(shape, dtype=None, order='C'):
    """
    Return a new array of given shape and type, filled with ones.

    Parameters
    ----------
    shape : int or sequence of ints
        Shape of the new array, e.g., ``(2, 3)`` or ``2``.
    dtype : data-type, optional
        The desired data-type for the array, e.g., `numpy.int8`.  Default is
        `numpy.float64`.
    order : {'C', 'F'}, optional, default: C
        Whether to store multi-dimensional data in row-major
        (C-style) or column-major (Fortran-style) order in
        memory.

    Returns
    -------
    out : ndarray
        Array of ones with the given shape, dtype, and order.

    See Also
    --------
    ones_like : Return an array of ones with shape and type of input.
    empty : Return a new uninitialized array.
    zeros : Return a new array setting values to zero.
    full : Return a new array of given shape filled with value.

    Examples
    --------
    >>> np.ones(5)
    array([1., 1., 1., 1., 1.])

    >>> np.ones((5,), dtype=int)
    array([1, 1, 1, 1, 1])

    >>> np.ones((2, 1))
    array([[1.],
           [1.]])

    >>> s = (2,2)
    >>> np.ones(s)
    array([[1.,  1.],
           [1.,  1.]])

    """
    a = empty(shape, dtype, order)
    multiarray.copyto(a, 1, casting='unsafe')
    return a


def _ones_like_dispatcher(a, dtype=None, order=None, subok=None, shape=None):
    return (
     a,)


@array_function_dispatch(_ones_like_dispatcher)
def ones_like(a, dtype=None, order='K', subok=True, shape=None):
    """
    Return an array of ones with the same shape and type as a given array.

    Parameters
    ----------
    a : array_like
        The shape and data-type of `a` define these same attributes of
        the returned array.
    dtype : data-type, optional
        Overrides the data type of the result.

        .. versionadded:: 1.6.0
    order : {'C', 'F', 'A', or 'K'}, optional
        Overrides the memory layout of the result. 'C' means C-order,
        'F' means F-order, 'A' means 'F' if `a` is Fortran contiguous,
        'C' otherwise. 'K' means match the layout of `a` as closely
        as possible.

        .. versionadded:: 1.6.0
    subok : bool, optional.
        If True, then the newly created array will use the sub-class
        type of 'a', otherwise it will be a base-class array. Defaults
        to True.
    shape : int or sequence of ints, optional.
        Overrides the shape of the result. If order='K' and the number of
        dimensions is unchanged, will try to keep order, otherwise,
        order='C' is implied.

        .. versionadded:: 1.17.0

    Returns
    -------
    out : ndarray
        Array of ones with the same shape and type as `a`.

    See Also
    --------
    empty_like : Return an empty array with shape and type of input.
    zeros_like : Return an array of zeros with shape and type of input.
    full_like : Return a new array with shape of input filled with value.
    ones : Return a new array setting values to one.

    Examples
    --------
    >>> x = np.arange(6)
    >>> x = x.reshape((2, 3))
    >>> x
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.ones_like(x)
    array([[1, 1, 1],
           [1, 1, 1]])

    >>> y = np.arange(3, dtype=float)
    >>> y
    array([0., 1., 2.])
    >>> np.ones_like(y)
    array([1.,  1.,  1.])

    """
    res = empty_like(a, dtype=dtype, order=order, subok=subok, shape=shape)
    multiarray.copyto(res, 1, casting='unsafe')
    return res


@set_module('numpy')
def full(shape, fill_value, dtype=None, order='C'):
    """
    Return a new array of given shape and type, filled with `fill_value`.

    Parameters
    ----------
    shape : int or sequence of ints
        Shape of the new array, e.g., ``(2, 3)`` or ``2``.
    fill_value : scalar or array_like
        Fill value.
    dtype : data-type, optional
        The desired data-type for the array  The default, None, means
         `np.array(fill_value).dtype`.
    order : {'C', 'F'}, optional
        Whether to store multidimensional data in C- or Fortran-contiguous
        (row- or column-wise) order in memory.

    Returns
    -------
    out : ndarray
        Array of `fill_value` with the given shape, dtype, and order.

    See Also
    --------
    full_like : Return a new array with shape of input filled with value.
    empty : Return a new uninitialized array.
    ones : Return a new array setting values to one.
    zeros : Return a new array setting values to zero.

    Examples
    --------
    >>> np.full((2, 2), np.inf)
    array([[inf, inf],
           [inf, inf]])
    >>> np.full((2, 2), 10)
    array([[10, 10],
           [10, 10]])

    >>> np.full((2, 2), [1, 2])
    array([[1, 2],
           [1, 2]])

    """
    if dtype is None:
        dtype = array(fill_value).dtype
    a = empty(shape, dtype, order)
    multiarray.copyto(a, fill_value, casting='unsafe')
    return a


def _full_like_dispatcher(a, fill_value, dtype=None, order=None, subok=None, shape=None):
    return (
     a,)


@array_function_dispatch(_full_like_dispatcher)
def full_like(a, fill_value, dtype=None, order='K', subok=True, shape=None):
    """
    Return a full array with the same shape and type as a given array.

    Parameters
    ----------
    a : array_like
        The shape and data-type of `a` define these same attributes of
        the returned array.
    fill_value : scalar
        Fill value.
    dtype : data-type, optional
        Overrides the data type of the result.
    order : {'C', 'F', 'A', or 'K'}, optional
        Overrides the memory layout of the result. 'C' means C-order,
        'F' means F-order, 'A' means 'F' if `a` is Fortran contiguous,
        'C' otherwise. 'K' means match the layout of `a` as closely
        as possible.
    subok : bool, optional.
        If True, then the newly created array will use the sub-class
        type of 'a', otherwise it will be a base-class array. Defaults
        to True.
    shape : int or sequence of ints, optional.
        Overrides the shape of the result. If order='K' and the number of
        dimensions is unchanged, will try to keep order, otherwise,
        order='C' is implied.

        .. versionadded:: 1.17.0

    Returns
    -------
    out : ndarray
        Array of `fill_value` with the same shape and type as `a`.

    See Also
    --------
    empty_like : Return an empty array with shape and type of input.
    ones_like : Return an array of ones with shape and type of input.
    zeros_like : Return an array of zeros with shape and type of input.
    full : Return a new array of given shape filled with value.

    Examples
    --------
    >>> x = np.arange(6, dtype=int)
    >>> np.full_like(x, 1)
    array([1, 1, 1, 1, 1, 1])
    >>> np.full_like(x, 0.1)
    array([0, 0, 0, 0, 0, 0])
    >>> np.full_like(x, 0.1, dtype=np.double)
    array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    >>> np.full_like(x, np.nan, dtype=np.double)
    array([nan, nan, nan, nan, nan, nan])

    >>> y = np.arange(6, dtype=np.double)
    >>> np.full_like(y, 0.1)
    array([0.1,  0.1,  0.1,  0.1,  0.1,  0.1])

    """
    res = empty_like(a, dtype=dtype, order=order, subok=subok, shape=shape)
    multiarray.copyto(res, fill_value, casting='unsafe')
    return res


def _count_nonzero_dispatcher(a, axis=None, *, keepdims=None):
    return (
     a,)


@array_function_dispatch(_count_nonzero_dispatcher)
def count_nonzero(a, axis=None, *, keepdims=False):
    """
    Counts the number of non-zero values in the array ``a``.

    The word "non-zero" is in reference to the Python 2.x
    built-in method ``__nonzero__()`` (renamed ``__bool__()``
    in Python 3.x) of Python objects that tests an object's
    "truthfulness". For example, any number is considered
    truthful if it is nonzero, whereas any string is considered
    truthful if it is not the empty string. Thus, this function
    (recursively) counts how many elements in ``a`` (and in
    sub-arrays thereof) have their ``__nonzero__()`` or ``__bool__()``
    method evaluated to ``True``.

    Parameters
    ----------
    a : array_like
        The array for which to count non-zeros.
    axis : int or tuple, optional
        Axis or tuple of axes along which to count non-zeros.
        Default is None, meaning that non-zeros will be counted
        along a flattened version of ``a``.

        .. versionadded:: 1.12.0

    keepdims : bool, optional
        If this is set to True, the axes that are counted are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        .. versionadded:: 1.19.0

    Returns
    -------
    count : int or array of int
        Number of non-zero values in the array along a given axis.
        Otherwise, the total number of non-zero values in the array
        is returned.

    See Also
    --------
    nonzero : Return the coordinates of all the non-zero values.

    Examples
    --------
    >>> np.count_nonzero(np.eye(4))
    4
    >>> a = np.array([[0, 1, 7, 0],
    ...               [3, 0, 2, 19]])
    >>> np.count_nonzero(a)
    5
    >>> np.count_nonzero(a, axis=0)
    array([1, 1, 2, 1])
    >>> np.count_nonzero(a, axis=1)
    array([2, 3])
    >>> np.count_nonzero(a, axis=1, keepdims=True)
    array([[2],
           [3]])
    """
    if axis is None:
        if not keepdims:
            return multiarray.count_nonzero(a)
    else:
        a = asanyarray(a)
        if np.issubdtype(a.dtype, np.character):
            a_bool = a != a.dtype.type()
        else:
            a_bool = a.astype((np.bool_), copy=False)
    return a_bool.sum(axis=axis, dtype=(np.intp), keepdims=keepdims)


@set_module('numpy')
def isfortran(a):
    """
    Check if the array is Fortran contiguous but *not* C contiguous.

    This function is obsolete and, because of changes due to relaxed stride
    checking, its return value for the same array may differ for versions
    of NumPy >= 1.10.0 and previous versions. If you only want to check if an
    array is Fortran contiguous use ``a.flags.f_contiguous`` instead.

    Parameters
    ----------
    a : ndarray
        Input array.

    Returns
    -------
    isfortran : bool
        Returns True if the array is Fortran contiguous but *not* C contiguous.

    Examples
    --------

    np.array allows to specify whether the array is written in C-contiguous
    order (last index varies the fastest), or FORTRAN-contiguous order in
    memory (first index varies the fastest).

    >>> a = np.array([[1, 2, 3], [4, 5, 6]], order='C')
    >>> a
    array([[1, 2, 3],
           [4, 5, 6]])
    >>> np.isfortran(a)
    False

    >>> b = np.array([[1, 2, 3], [4, 5, 6]], order='F')
    >>> b
    array([[1, 2, 3],
           [4, 5, 6]])
    >>> np.isfortran(b)
    True

    The transpose of a C-ordered array is a FORTRAN-ordered array.

    >>> a = np.array([[1, 2, 3], [4, 5, 6]], order='C')
    >>> a
    array([[1, 2, 3],
           [4, 5, 6]])
    >>> np.isfortran(a)
    False
    >>> b = a.T
    >>> b
    array([[1, 4],
           [2, 5],
           [3, 6]])
    >>> np.isfortran(b)
    True

    C-ordered arrays evaluate as False even if they are also FORTRAN-ordered.

    >>> np.isfortran(np.array([1, 2], order='F'))
    False

    """
    return a.flags.fnc


def _argwhere_dispatcher(a):
    return (
     a,)


@array_function_dispatch(_argwhere_dispatcher)
def argwhere(a):
    """
    Find the indices of array elements that are non-zero, grouped by element.

    Parameters
    ----------
    a : array_like
        Input data.

    Returns
    -------
    index_array : (N, a.ndim) ndarray
        Indices of elements that are non-zero. Indices are grouped by element.
        This array will have shape ``(N, a.ndim)`` where ``N`` is the number of
        non-zero items.

    See Also
    --------
    where, nonzero

    Notes
    -----
    ``np.argwhere(a)`` is almost the same as ``np.transpose(np.nonzero(a))``,
    but produces a result of the correct shape for a 0D array.

    The output of ``argwhere`` is not suitable for indexing arrays.
    For this purpose use ``nonzero(a)`` instead.

    Examples
    --------
    >>> x = np.arange(6).reshape(2,3)
    >>> x
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.argwhere(x>1)
    array([[0, 2],
           [1, 0],
           [1, 1],
           [1, 2]])

    """
    if np.ndim(a) == 0:
        a = shape_base.atleast_1d(a)
        return argwhere(a)[:, :0]
    return transpose(nonzero(a))


def _flatnonzero_dispatcher(a):
    return (
     a,)


@array_function_dispatch(_flatnonzero_dispatcher)
def flatnonzero(a):
    """
    Return indices that are non-zero in the flattened version of a.

    This is equivalent to np.nonzero(np.ravel(a))[0].

    Parameters
    ----------
    a : array_like
        Input data.

    Returns
    -------
    res : ndarray
        Output array, containing the indices of the elements of `a.ravel()`
        that are non-zero.

    See Also
    --------
    nonzero : Return the indices of the non-zero elements of the input array.
    ravel : Return a 1-D array containing the elements of the input array.

    Examples
    --------
    >>> x = np.arange(-2, 3)
    >>> x
    array([-2, -1,  0,  1,  2])
    >>> np.flatnonzero(x)
    array([0, 1, 3, 4])

    Use the indices of the non-zero elements as an index array to extract
    these elements:

    >>> x.ravel()[np.flatnonzero(x)]
    array([-2, -1,  1,  2])

    """
    return np.nonzero(np.ravel(a))[0]


_mode_from_name_dict = {'v':0, 
 's':1, 
 'f':2}

def _mode_from_name(mode):
    if isinstance(mode, str):
        return _mode_from_name_dict[mode.lower()[0]]
    return mode


def _correlate_dispatcher(a, v, mode=None):
    return (
     a, v)


@array_function_dispatch(_correlate_dispatcher)
def correlate(a, v, mode='valid'):
    """
    Cross-correlation of two 1-dimensional sequences.

    This function computes the correlation as generally defined in signal
    processing texts::

        c_{av}[k] = sum_n a[n+k] * conj(v[n])

    with a and v sequences being zero-padded where necessary and conj being
    the conjugate.

    Parameters
    ----------
    a, v : array_like
        Input sequences.
    mode : {'valid', 'same', 'full'}, optional
        Refer to the `convolve` docstring.  Note that the default
        is 'valid', unlike `convolve`, which uses 'full'.
    old_behavior : bool
        `old_behavior` was removed in NumPy 1.10. If you need the old
        behavior, use `multiarray.correlate`.

    Returns
    -------
    out : ndarray
        Discrete cross-correlation of `a` and `v`.

    See Also
    --------
    convolve : Discrete, linear convolution of two one-dimensional sequences.
    multiarray.correlate : Old, no conjugate, version of correlate.

    Notes
    -----
    The definition of correlation above is not unique and sometimes correlation
    may be defined differently. Another common definition is::

        c'_{av}[k] = sum_n a[n] conj(v[n+k])

    which is related to ``c_{av}[k]`` by ``c'_{av}[k] = c_{av}[-k]``.

    Examples
    --------
    >>> np.correlate([1, 2, 3], [0, 1, 0.5])
    array([3.5])
    >>> np.correlate([1, 2, 3], [0, 1, 0.5], "same")
    array([2. ,  3.5,  3. ])
    >>> np.correlate([1, 2, 3], [0, 1, 0.5], "full")
    array([0.5,  2. ,  3.5,  3. ,  0. ])

    Using complex sequences:

    >>> np.correlate([1+1j, 2, 3-1j], [0, 1, 0.5j], 'full')
    array([ 0.5-0.5j,  1.0+0.j ,  1.5-1.5j,  3.0-1.j ,  0.0+0.j ])

    Note that you get the time reversed, complex conjugated result
    when the two input sequences change places, i.e.,
    ``c_{va}[k] = c^{*}_{av}[-k]``:

    >>> np.correlate([0, 1, 0.5j], [1+1j, 2, 3-1j], 'full')
    array([ 0.0+0.j ,  3.0+1.j ,  1.5+1.5j,  1.0+0.j ,  0.5+0.5j])

    """
    mode = _mode_from_name(mode)
    return multiarray.correlate2(a, v, mode)


def _convolve_dispatcher(a, v, mode=None):
    return (
     a, v)


@array_function_dispatch(_convolve_dispatcher)
def convolve(a, v, mode='full'):
    r"""
    Returns the discrete, linear convolution of two one-dimensional sequences.

    The convolution operator is often seen in signal processing, where it
    models the effect of a linear time-invariant system on a signal [1]_.  In
    probability theory, the sum of two independent random variables is
    distributed according to the convolution of their individual
    distributions.

    If `v` is longer than `a`, the arrays are swapped before computation.

    Parameters
    ----------
    a : (N,) array_like
        First one-dimensional input array.
    v : (M,) array_like
        Second one-dimensional input array.
    mode : {'full', 'valid', 'same'}, optional
        'full':
          By default, mode is 'full'.  This returns the convolution
          at each point of overlap, with an output shape of (N+M-1,). At
          the end-points of the convolution, the signals do not overlap
          completely, and boundary effects may be seen.

        'same':
          Mode 'same' returns output of length ``max(M, N)``.  Boundary
          effects are still visible.

        'valid':
          Mode 'valid' returns output of length
          ``max(M, N) - min(M, N) + 1``.  The convolution product is only given
          for points where the signals overlap completely.  Values outside
          the signal boundary have no effect.

    Returns
    -------
    out : ndarray
        Discrete, linear convolution of `a` and `v`.

    See Also
    --------
    scipy.signal.fftconvolve : Convolve two arrays using the Fast Fourier
                               Transform.
    scipy.linalg.toeplitz : Used to construct the convolution operator.
    polymul : Polynomial multiplication. Same output as convolve, but also
              accepts poly1d objects as input.

    Notes
    -----
    The discrete convolution operation is defined as

    .. math:: (a * v)[n] = \sum_{m = -\infty}^{\infty} a[m] v[n - m]

    It can be shown that a convolution :math:`x(t) * y(t)` in time/space
    is equivalent to the multiplication :math:`X(f) Y(f)` in the Fourier
    domain, after appropriate padding (padding is necessary to prevent
    circular convolution).  Since multiplication is more efficient (faster)
    than convolution, the function `scipy.signal.fftconvolve` exploits the
    FFT to calculate the convolution of large data-sets.

    References
    ----------
    .. [1] Wikipedia, "Convolution",
        https://en.wikipedia.org/wiki/Convolution

    Examples
    --------
    Note how the convolution operator flips the second array
    before "sliding" the two across one another:

    >>> np.convolve([1, 2, 3], [0, 1, 0.5])
    array([0. , 1. , 2.5, 4. , 1.5])

    Only return the middle values of the convolution.
    Contains boundary effects, where zeros are taken
    into account:

    >>> np.convolve([1,2,3],[0,1,0.5], 'same')
    array([1. ,  2.5,  4. ])

    The two arrays are of the same length, so there
    is only one position where they completely overlap:

    >>> np.convolve([1,2,3],[0,1,0.5], 'valid')
    array([2.5])

    """
    a, v = array(a, copy=False, ndmin=1), array(v, copy=False, ndmin=1)
    if len(v) > len(a):
        a, v = v, a
    if len(a) == 0:
        raise ValueError('a cannot be empty')
    if len(v) == 0:
        raise ValueError('v cannot be empty')
    mode = _mode_from_name(mode)
    return multiarray.correlate(a, v[::-1], mode)


def _outer_dispatcher(a, b, out=None):
    return (
     a, b, out)


@array_function_dispatch(_outer_dispatcher)
def outer(a, b, out=None):
    """
    Compute the outer product of two vectors.

    Given two vectors, ``a = [a0, a1, ..., aM]`` and
    ``b = [b0, b1, ..., bN]``,
    the outer product [1]_ is::

      [[a0*b0  a0*b1 ... a0*bN ]
       [a1*b0    .
       [ ...          .
       [aM*b0            aM*bN ]]

    Parameters
    ----------
    a : (M,) array_like
        First input vector.  Input is flattened if
        not already 1-dimensional.
    b : (N,) array_like
        Second input vector.  Input is flattened if
        not already 1-dimensional.
    out : (M, N) ndarray, optional
        A location where the result is stored

        .. versionadded:: 1.9.0

    Returns
    -------
    out : (M, N) ndarray
        ``out[i, j] = a[i] * b[j]``

    See also
    --------
    inner
    einsum : ``einsum('i,j->ij', a.ravel(), b.ravel())`` is the equivalent.
    ufunc.outer : A generalization to dimensions other than 1D and other
                  operations. ``np.multiply.outer(a.ravel(), b.ravel())``
                  is the equivalent.
    tensordot : ``np.tensordot(a.ravel(), b.ravel(), axes=((), ()))``
                is the equivalent.

    References
    ----------
    .. [1] : G. H. Golub and C. F. Van Loan, *Matrix Computations*, 3rd
             ed., Baltimore, MD, Johns Hopkins University Press, 1996,
             pg. 8.

    Examples
    --------
    Make a (*very* coarse) grid for computing a Mandelbrot set:

    >>> rl = np.outer(np.ones((5,)), np.linspace(-2, 2, 5))
    >>> rl
    array([[-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.],
           [-2., -1.,  0.,  1.,  2.]])
    >>> im = np.outer(1j*np.linspace(2, -2, 5), np.ones((5,)))
    >>> im
    array([[0.+2.j, 0.+2.j, 0.+2.j, 0.+2.j, 0.+2.j],
           [0.+1.j, 0.+1.j, 0.+1.j, 0.+1.j, 0.+1.j],
           [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
           [0.-1.j, 0.-1.j, 0.-1.j, 0.-1.j, 0.-1.j],
           [0.-2.j, 0.-2.j, 0.-2.j, 0.-2.j, 0.-2.j]])
    >>> grid = rl + im
    >>> grid
    array([[-2.+2.j, -1.+2.j,  0.+2.j,  1.+2.j,  2.+2.j],
           [-2.+1.j, -1.+1.j,  0.+1.j,  1.+1.j,  2.+1.j],
           [-2.+0.j, -1.+0.j,  0.+0.j,  1.+0.j,  2.+0.j],
           [-2.-1.j, -1.-1.j,  0.-1.j,  1.-1.j,  2.-1.j],
           [-2.-2.j, -1.-2.j,  0.-2.j,  1.-2.j,  2.-2.j]])

    An example using a "vector" of letters:

    >>> x = np.array(['a', 'b', 'c'], dtype=object)
    >>> np.outer(x, [1, 2, 3])
    array([['a', 'aa', 'aaa'],
           ['b', 'bb', 'bbb'],
           ['c', 'cc', 'ccc']], dtype=object)

    """
    a = asarray(a)
    b = asarray(b)
    return multiply(a.ravel()[:, newaxis], b.ravel()[newaxis, :], out)


def _tensordot_dispatcher(a, b, axes=None):
    return (
     a, b)


@array_function_dispatch(_tensordot_dispatcher)
def tensordot--- This code section failed: ---

 L.1045         0  SETUP_FINALLY        14  'to 14'

 L.1046         2  LOAD_GLOBAL              iter
                4  LOAD_FAST                'axes'
                6  CALL_FUNCTION_1       1  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         64  'to 64'
             14_0  COME_FROM_FINALLY     0  '0'

 L.1047        14  DUP_TOP          
               16  LOAD_GLOBAL              Exception
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    62  'to 62'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.1048        28  LOAD_GLOBAL              list
               30  LOAD_GLOBAL              range
               32  LOAD_FAST                'axes'
               34  UNARY_NEGATIVE   
               36  LOAD_CONST               0
               38  CALL_FUNCTION_2       2  ''
               40  CALL_FUNCTION_1       1  ''
               42  STORE_DEREF              'axes_a'

 L.1049        44  LOAD_GLOBAL              list
               46  LOAD_GLOBAL              range
               48  LOAD_CONST               0
               50  LOAD_FAST                'axes'
               52  CALL_FUNCTION_2       2  ''
               54  CALL_FUNCTION_1       1  ''
               56  STORE_DEREF              'axes_b'
               58  POP_EXCEPT       
               60  JUMP_FORWARD         72  'to 72'
             62_0  COME_FROM            20  '20'
               62  END_FINALLY      
             64_0  COME_FROM            12  '12'

 L.1051        64  LOAD_FAST                'axes'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_DEREF              'axes_a'
               70  STORE_DEREF              'axes_b'
             72_0  COME_FROM            60  '60'

 L.1052        72  SETUP_FINALLY        94  'to 94'

 L.1053        74  LOAD_GLOBAL              len
               76  LOAD_DEREF               'axes_a'
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'na'

 L.1054        82  LOAD_GLOBAL              list
               84  LOAD_DEREF               'axes_a'
               86  CALL_FUNCTION_1       1  ''
               88  STORE_DEREF              'axes_a'
               90  POP_BLOCK        
               92  JUMP_FORWARD        124  'to 124'
             94_0  COME_FROM_FINALLY    72  '72'

 L.1055        94  DUP_TOP          
               96  LOAD_GLOBAL              TypeError
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   122  'to 122'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L.1056       108  LOAD_DEREF               'axes_a'
              110  BUILD_LIST_1          1 
              112  STORE_DEREF              'axes_a'

 L.1057       114  LOAD_CONST               1
              116  STORE_FAST               'na'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           100  '100'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            92  '92'

 L.1058       124  SETUP_FINALLY       146  'to 146'

 L.1059       126  LOAD_GLOBAL              len
              128  LOAD_DEREF               'axes_b'
              130  CALL_FUNCTION_1       1  ''
              132  STORE_FAST               'nb'

 L.1060       134  LOAD_GLOBAL              list
              136  LOAD_DEREF               'axes_b'
              138  CALL_FUNCTION_1       1  ''
              140  STORE_DEREF              'axes_b'
              142  POP_BLOCK        
              144  JUMP_FORWARD        176  'to 176'
            146_0  COME_FROM_FINALLY   124  '124'

 L.1061       146  DUP_TOP          
              148  LOAD_GLOBAL              TypeError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   174  'to 174'
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L.1062       160  LOAD_DEREF               'axes_b'
              162  BUILD_LIST_1          1 
              164  STORE_DEREF              'axes_b'

 L.1063       166  LOAD_CONST               1
              168  STORE_FAST               'nb'
              170  POP_EXCEPT       
              172  JUMP_FORWARD        176  'to 176'
            174_0  COME_FROM           152  '152'
              174  END_FINALLY      
            176_0  COME_FROM           172  '172'
            176_1  COME_FROM           144  '144'

 L.1065       176  LOAD_GLOBAL              asarray
              178  LOAD_FAST                'a'
              180  CALL_FUNCTION_1       1  ''
              182  LOAD_GLOBAL              asarray
              184  LOAD_FAST                'b'
              186  CALL_FUNCTION_1       1  ''
              188  ROT_TWO          
              190  STORE_FAST               'a'
              192  STORE_FAST               'b'

 L.1066       194  LOAD_FAST                'a'
              196  LOAD_ATTR                shape
              198  STORE_DEREF              'as_'

 L.1067       200  LOAD_FAST                'a'
              202  LOAD_ATTR                ndim
              204  STORE_FAST               'nda'

 L.1068       206  LOAD_FAST                'b'
              208  LOAD_ATTR                shape
              210  STORE_DEREF              'bs'

 L.1069       212  LOAD_FAST                'b'
              214  LOAD_ATTR                ndim
              216  STORE_FAST               'ndb'

 L.1070       218  LOAD_CONST               True
              220  STORE_FAST               'equal'

 L.1071       222  LOAD_FAST                'na'
              224  LOAD_FAST                'nb'
              226  COMPARE_OP               !=
              228  POP_JUMP_IF_FALSE   236  'to 236'

 L.1072       230  LOAD_CONST               False
              232  STORE_FAST               'equal'
              234  JUMP_FORWARD        344  'to 344'
            236_0  COME_FROM           228  '228'

 L.1074       236  LOAD_GLOBAL              range
              238  LOAD_FAST                'na'
              240  CALL_FUNCTION_1       1  ''
              242  GET_ITER         
            244_0  COME_FROM           324  '324'
              244  FOR_ITER            344  'to 344'
              246  STORE_FAST               'k'

 L.1075       248  LOAD_DEREF               'as_'
              250  LOAD_DEREF               'axes_a'
              252  LOAD_FAST                'k'
              254  BINARY_SUBSCR    
              256  BINARY_SUBSCR    
              258  LOAD_DEREF               'bs'
              260  LOAD_DEREF               'axes_b'
              262  LOAD_FAST                'k'
              264  BINARY_SUBSCR    
              266  BINARY_SUBSCR    
              268  COMPARE_OP               !=
          270_272  POP_JUMP_IF_FALSE   284  'to 284'

 L.1076       274  LOAD_CONST               False
              276  STORE_FAST               'equal'

 L.1077       278  POP_TOP          
          280_282  JUMP_ABSOLUTE       344  'to 344'
            284_0  COME_FROM           270  '270'

 L.1078       284  LOAD_DEREF               'axes_a'
              286  LOAD_FAST                'k'
              288  BINARY_SUBSCR    
              290  LOAD_CONST               0
              292  COMPARE_OP               <
          294_296  POP_JUMP_IF_FALSE   314  'to 314'

 L.1079       298  LOAD_DEREF               'axes_a'
              300  LOAD_FAST                'k'
              302  DUP_TOP_TWO      
              304  BINARY_SUBSCR    
              306  LOAD_FAST                'nda'
              308  INPLACE_ADD      
              310  ROT_THREE        
              312  STORE_SUBSCR     
            314_0  COME_FROM           294  '294'

 L.1080       314  LOAD_DEREF               'axes_b'
              316  LOAD_FAST                'k'
              318  BINARY_SUBSCR    
              320  LOAD_CONST               0
              322  COMPARE_OP               <
              324  POP_JUMP_IF_FALSE   244  'to 244'

 L.1081       326  LOAD_DEREF               'axes_b'
              328  LOAD_FAST                'k'
              330  DUP_TOP_TWO      
              332  BINARY_SUBSCR    
              334  LOAD_FAST                'ndb'
              336  INPLACE_ADD      
              338  ROT_THREE        
              340  STORE_SUBSCR     
              342  JUMP_BACK           244  'to 244'
            344_0  COME_FROM           234  '234'

 L.1082       344  LOAD_FAST                'equal'
          346_348  POP_JUMP_IF_TRUE    358  'to 358'

 L.1083       350  LOAD_GLOBAL              ValueError
              352  LOAD_STR                 'shape-mismatch for sum'
              354  CALL_FUNCTION_1       1  ''
              356  RAISE_VARARGS_1       1  'exception instance'
            358_0  COME_FROM           346  '346'

 L.1087       358  LOAD_CLOSURE             'axes_a'
              360  BUILD_TUPLE_1         1 
              362  LOAD_LISTCOMP            '<code_object <listcomp>>'
              364  LOAD_STR                 'tensordot.<locals>.<listcomp>'
              366  MAKE_FUNCTION_8          'closure'
              368  LOAD_GLOBAL              range
              370  LOAD_FAST                'nda'
              372  CALL_FUNCTION_1       1  ''
              374  GET_ITER         
              376  CALL_FUNCTION_1       1  ''
              378  STORE_FAST               'notin'

 L.1088       380  LOAD_FAST                'notin'
              382  LOAD_DEREF               'axes_a'
              384  BINARY_ADD       
              386  STORE_FAST               'newaxes_a'

 L.1089       388  LOAD_CONST               1
              390  STORE_FAST               'N2'

 L.1090       392  LOAD_DEREF               'axes_a'
              394  GET_ITER         
              396  FOR_ITER            416  'to 416'
              398  STORE_FAST               'axis'

 L.1091       400  LOAD_FAST                'N2'
              402  LOAD_DEREF               'as_'
              404  LOAD_FAST                'axis'
              406  BINARY_SUBSCR    
              408  INPLACE_MULTIPLY 
              410  STORE_FAST               'N2'
          412_414  JUMP_BACK           396  'to 396'

 L.1092       416  LOAD_GLOBAL              int
              418  LOAD_GLOBAL              multiply
              420  LOAD_METHOD              reduce
              422  LOAD_CLOSURE             'as_'
              424  BUILD_TUPLE_1         1 
              426  LOAD_LISTCOMP            '<code_object <listcomp>>'
              428  LOAD_STR                 'tensordot.<locals>.<listcomp>'
              430  MAKE_FUNCTION_8          'closure'
              432  LOAD_FAST                'notin'
              434  GET_ITER         
              436  CALL_FUNCTION_1       1  ''
              438  CALL_METHOD_1         1  ''
              440  CALL_FUNCTION_1       1  ''
              442  LOAD_FAST                'N2'
              444  BUILD_TUPLE_2         2 
              446  STORE_FAST               'newshape_a'

 L.1093       448  LOAD_CLOSURE             'as_'
              450  BUILD_TUPLE_1         1 
              452  LOAD_LISTCOMP            '<code_object <listcomp>>'
              454  LOAD_STR                 'tensordot.<locals>.<listcomp>'
              456  MAKE_FUNCTION_8          'closure'
              458  LOAD_FAST                'notin'
              460  GET_ITER         
              462  CALL_FUNCTION_1       1  ''
              464  STORE_FAST               'olda'

 L.1095       466  LOAD_CLOSURE             'axes_b'
              468  BUILD_TUPLE_1         1 
              470  LOAD_LISTCOMP            '<code_object <listcomp>>'
              472  LOAD_STR                 'tensordot.<locals>.<listcomp>'
              474  MAKE_FUNCTION_8          'closure'
              476  LOAD_GLOBAL              range
              478  LOAD_FAST                'ndb'
              480  CALL_FUNCTION_1       1  ''
              482  GET_ITER         
              484  CALL_FUNCTION_1       1  ''
              486  STORE_FAST               'notin'

 L.1096       488  LOAD_DEREF               'axes_b'
              490  LOAD_FAST                'notin'
              492  BINARY_ADD       
              494  STORE_FAST               'newaxes_b'

 L.1097       496  LOAD_CONST               1
              498  STORE_FAST               'N2'

 L.1098       500  LOAD_DEREF               'axes_b'
              502  GET_ITER         
              504  FOR_ITER            524  'to 524'
              506  STORE_FAST               'axis'

 L.1099       508  LOAD_FAST                'N2'
              510  LOAD_DEREF               'bs'
              512  LOAD_FAST                'axis'
              514  BINARY_SUBSCR    
              516  INPLACE_MULTIPLY 
              518  STORE_FAST               'N2'
          520_522  JUMP_BACK           504  'to 504'

 L.1100       524  LOAD_FAST                'N2'
              526  LOAD_GLOBAL              int
              528  LOAD_GLOBAL              multiply
              530  LOAD_METHOD              reduce
              532  LOAD_CLOSURE             'bs'
              534  BUILD_TUPLE_1         1 
              536  LOAD_LISTCOMP            '<code_object <listcomp>>'
              538  LOAD_STR                 'tensordot.<locals>.<listcomp>'
              540  MAKE_FUNCTION_8          'closure'
              542  LOAD_FAST                'notin'
              544  GET_ITER         
              546  CALL_FUNCTION_1       1  ''
              548  CALL_METHOD_1         1  ''
              550  CALL_FUNCTION_1       1  ''
              552  BUILD_TUPLE_2         2 
              554  STORE_FAST               'newshape_b'

 L.1101       556  LOAD_CLOSURE             'bs'
              558  BUILD_TUPLE_1         1 
              560  LOAD_LISTCOMP            '<code_object <listcomp>>'
              562  LOAD_STR                 'tensordot.<locals>.<listcomp>'
              564  MAKE_FUNCTION_8          'closure'
              566  LOAD_FAST                'notin'
              568  GET_ITER         
              570  CALL_FUNCTION_1       1  ''
              572  STORE_FAST               'oldb'

 L.1103       574  LOAD_FAST                'a'
              576  LOAD_METHOD              transpose
              578  LOAD_FAST                'newaxes_a'
              580  CALL_METHOD_1         1  ''
              582  LOAD_METHOD              reshape
              584  LOAD_FAST                'newshape_a'
              586  CALL_METHOD_1         1  ''
              588  STORE_FAST               'at'

 L.1104       590  LOAD_FAST                'b'
              592  LOAD_METHOD              transpose
              594  LOAD_FAST                'newaxes_b'
              596  CALL_METHOD_1         1  ''
              598  LOAD_METHOD              reshape
              600  LOAD_FAST                'newshape_b'
              602  CALL_METHOD_1         1  ''
              604  STORE_FAST               'bt'

 L.1105       606  LOAD_GLOBAL              dot
              608  LOAD_FAST                'at'
              610  LOAD_FAST                'bt'
              612  CALL_FUNCTION_2       2  ''
              614  STORE_FAST               'res'

 L.1106       616  LOAD_FAST                'res'
              618  LOAD_METHOD              reshape
              620  LOAD_FAST                'olda'
              622  LOAD_FAST                'oldb'
              624  BINARY_ADD       
              626  CALL_METHOD_1         1  ''
              628  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 280_282


def _roll_dispatcher(a, shift, axis=None):
    return (
     a,)


@array_function_dispatch(_roll_dispatcher)
def roll(a, shift, axis=None):
    """
    Roll array elements along a given axis.

    Elements that roll beyond the last position are re-introduced at
    the first.

    Parameters
    ----------
    a : array_like
        Input array.
    shift : int or tuple of ints
        The number of places by which elements are shifted.  If a tuple,
        then `axis` must be a tuple of the same size, and each of the
        given axes is shifted by the corresponding number.  If an int
        while `axis` is a tuple of ints, then the same value is used for
        all given axes.
    axis : int or tuple of ints, optional
        Axis or axes along which elements are shifted.  By default, the
        array is flattened before shifting, after which the original
        shape is restored.

    Returns
    -------
    res : ndarray
        Output array, with the same shape as `a`.

    See Also
    --------
    rollaxis : Roll the specified axis backwards, until it lies in a
               given position.

    Notes
    -----
    .. versionadded:: 1.12.0

    Supports rolling over multiple dimensions simultaneously.

    Examples
    --------
    >>> x = np.arange(10)
    >>> np.roll(x, 2)
    array([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])
    >>> np.roll(x, -2)
    array([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])

    >>> x2 = np.reshape(x, (2,5))
    >>> x2
    array([[0, 1, 2, 3, 4],
           [5, 6, 7, 8, 9]])
    >>> np.roll(x2, 1)
    array([[9, 0, 1, 2, 3],
           [4, 5, 6, 7, 8]])
    >>> np.roll(x2, -1)
    array([[1, 2, 3, 4, 5],
           [6, 7, 8, 9, 0]])
    >>> np.roll(x2, 1, axis=0)
    array([[5, 6, 7, 8, 9],
           [0, 1, 2, 3, 4]])
    >>> np.roll(x2, -1, axis=0)
    array([[5, 6, 7, 8, 9],
           [0, 1, 2, 3, 4]])
    >>> np.roll(x2, 1, axis=1)
    array([[4, 0, 1, 2, 3],
           [9, 5, 6, 7, 8]])
    >>> np.roll(x2, -1, axis=1)
    array([[1, 2, 3, 4, 0],
           [6, 7, 8, 9, 5]])

    """
    a = asanyarray(a)
    if axis is None:
        return roll(a.ravel(), shift, 0).reshape(a.shape)
    axis = normalize_axis_tuple(axis, (a.ndim), allow_duplicate=True)
    broadcasted = broadcast(shift, axis)
    if broadcasted.ndim > 1:
        raise ValueError("'shift' and 'axis' should be scalars or 1D sequences")
    shifts = {0:ax for ax in range(a.ndim)}
    for sh, ax in broadcasted:
        shifts[ax] += sh
    else:
        rolls = [
         (
          (
           slice(None), slice(None)),)] * a.ndim
        for ax, offset in shifts.items():
            offset %= a.shape[ax] or 1
            if offset:
                rolls[ax] = ((slice(None, -offset), slice(offset, None)),
                 (
                  slice(-offset, None), slice(None, offset)))
            result = empty_like(a)
            for indices in (itertools.product)(*rolls):
                arr_index, res_index = zip(*indices)
                result[res_index] = a[arr_index]
            else:
                return result


def _rollaxis_dispatcher(a, axis, start=None):
    return (
     a,)


@array_function_dispatch(_rollaxis_dispatcher)
def rollaxis(a, axis, start=0):
    """
    Roll the specified axis backwards, until it lies in a given position.

    This function continues to be supported for backward compatibility, but you
    should prefer `moveaxis`. The `moveaxis` function was added in NumPy
    1.11.

    Parameters
    ----------
    a : ndarray
        Input array.
    axis : int
        The axis to be rolled. The positions of the other axes do not
        change relative to one another.
    start : int, optional
        When ``start <= axis``, the axis is rolled back until it lies in
        this position. When ``start > axis``, the axis is rolled until it
        lies before this position. The default, 0, results in a "complete"
        roll. The following table describes how negative values of ``start``
        are interpreted:

        .. table::
           :align: left

           +-------------------+----------------------+
           |     ``start``     | Normalized ``start`` |
           +===================+======================+
           | ``-(arr.ndim+1)`` | raise ``AxisError``  |
           +-------------------+----------------------+
           | ``-arr.ndim``     | 0                    |
           +-------------------+----------------------+
           | |vdots|           | |vdots|              |
           +-------------------+----------------------+
           | ``-1``            | ``arr.ndim-1``       |
           +-------------------+----------------------+
           | ``0``             | ``0``                |
           +-------------------+----------------------+
           | |vdots|           | |vdots|              |
           +-------------------+----------------------+
           | ``arr.ndim``      | ``arr.ndim``         |
           +-------------------+----------------------+
           | ``arr.ndim + 1``  | raise ``AxisError``  |
           +-------------------+----------------------+
           
        .. |vdots|   unicode:: U+22EE .. Vertical Ellipsis

    Returns
    -------
    res : ndarray
        For NumPy >= 1.10.0 a view of `a` is always returned. For earlier
        NumPy versions a view of `a` is returned only if the order of the
        axes is changed, otherwise the input array is returned.

    See Also
    --------
    moveaxis : Move array axes to new positions.
    roll : Roll the elements of an array by a number of positions along a
        given axis.

    Examples
    --------
    >>> a = np.ones((3,4,5,6))
    >>> np.rollaxis(a, 3, 1).shape
    (3, 6, 4, 5)
    >>> np.rollaxis(a, 2).shape
    (5, 3, 4, 6)
    >>> np.rollaxis(a, 1, 4).shape
    (3, 5, 6, 4)

    """
    n = a.ndim
    axis = normalize_axis_index(axis, n)
    if start < 0:
        start += n
    msg = "'%s' arg requires %d <= %s < %d, but %d was passed in"
    if not 0 <= start < n + 1:
        raise AxisError(msg % ('start', -n, 'start', n + 1, start))
    if axis < start:
        start -= 1
    if axis == start:
        return a[...]
    axes = list(range(0, n))
    axes.remove(axis)
    axes.insert(start, axis)
    return a.transpose(axes)


def normalize_axis_tuple(axis, ndim, argname=None, allow_duplicate=False):
    """
    Normalizes an axis argument into a tuple of non-negative integer axes.

    This handles shorthands such as ``1`` and converts them to ``(1,)``,
    as well as performing the handling of negative indices covered by
    `normalize_axis_index`.

    By default, this forbids axes from being specified multiple times.

    Used internally by multi-axis-checking logic.

    .. versionadded:: 1.13.0

    Parameters
    ----------
    axis : int, iterable of int
        The un-normalized index or indices of the axis.
    ndim : int
        The number of dimensions of the array that `axis` should be normalized
        against.
    argname : str, optional
        A prefix to put before the error message, typically the name of the
        argument.
    allow_duplicate : bool, optional
        If False, the default, disallow an axis from being specified twice.

    Returns
    -------
    normalized_axes : tuple of int
        The normalized axis index, such that `0 <= normalized_axis < ndim`

    Raises
    ------
    AxisError
        If any axis provided is out of range
    ValueError
        If an axis is repeated

    See also
    --------
    normalize_axis_index : normalizing a single scalar axis
    """
    if type(axis) not in (tuple, list):
        try:
            axis = [
             operator.index(axis)]
        except TypeError:
            pass
        else:
            axis = tuple([normalize_axis_index(ax, ndim, argname) for ax in axis])
            if not allow_duplicate:
                if len(set(axis)) != len(axis):
                    if argname:
                        raise ValueError('repeated axis in `{}` argument'.format(argname))
    else:
        raise ValueError('repeated axis')
    return axis


def _moveaxis_dispatcher(a, source, destination):
    return (
     a,)


@array_function_dispatch(_moveaxis_dispatcher)
def moveaxis(a, source, destination):
    """
    Move axes of an array to new positions.

    Other axes remain in their original order.

    .. versionadded:: 1.11.0

    Parameters
    ----------
    a : np.ndarray
        The array whose axes should be reordered.
    source : int or sequence of int
        Original positions of the axes to move. These must be unique.
    destination : int or sequence of int
        Destination positions for each of the original axes. These must also be
        unique.

    Returns
    -------
    result : np.ndarray
        Array with moved axes. This array is a view of the input array.

    See Also
    --------
    transpose: Permute the dimensions of an array.
    swapaxes: Interchange two axes of an array.

    Examples
    --------

    >>> x = np.zeros((3, 4, 5))
    >>> np.moveaxis(x, 0, -1).shape
    (4, 5, 3)
    >>> np.moveaxis(x, -1, 0).shape
    (5, 3, 4)

    These all achieve the same result:

    >>> np.transpose(x).shape
    (5, 4, 3)
    >>> np.swapaxes(x, 0, -1).shape
    (5, 4, 3)
    >>> np.moveaxis(x, [0, 1], [-1, -2]).shape
    (5, 4, 3)
    >>> np.moveaxis(x, [0, 1, 2], [-1, -2, -3]).shape
    (5, 4, 3)

    """
    try:
        transpose = a.transpose
    except AttributeError:
        a = asarray(a)
        transpose = a.transpose
    else:
        source = normalize_axis_tuple(source, a.ndim, 'source')
        destination = normalize_axis_tuple(destination, a.ndim, 'destination')
        if len(source) != len(destination):
            raise ValueError('`source` and `destination` arguments must have the same number of elements')
        order = [n for n in range(a.ndim) if n not in source]
        for dest, src in sorted(zip(destination, source)):
            order.insert(dest, src)
        else:
            result = transpose(order)
            return result


def _move_axis_to_0(a, axis):
    return moveaxis(a, axis, 0)


def _cross_dispatcher(a, b, axisa=None, axisb=None, axisc=None, axis=None):
    return (
     a, b)


@array_function_dispatch(_cross_dispatcher)
def cross(a, b, axisa=-1, axisb=-1, axisc=-1, axis=None):
    """
    Return the cross product of two (arrays of) vectors.

    The cross product of `a` and `b` in :math:`R^3` is a vector perpendicular
    to both `a` and `b`.  If `a` and `b` are arrays of vectors, the vectors
    are defined by the last axis of `a` and `b` by default, and these axes
    can have dimensions 2 or 3.  Where the dimension of either `a` or `b` is
    2, the third component of the input vector is assumed to be zero and the
    cross product calculated accordingly.  In cases where both input vectors
    have dimension 2, the z-component of the cross product is returned.

    Parameters
    ----------
    a : array_like
        Components of the first vector(s).
    b : array_like
        Components of the second vector(s).
    axisa : int, optional
        Axis of `a` that defines the vector(s).  By default, the last axis.
    axisb : int, optional
        Axis of `b` that defines the vector(s).  By default, the last axis.
    axisc : int, optional
        Axis of `c` containing the cross product vector(s).  Ignored if
        both input vectors have dimension 2, as the return is scalar.
        By default, the last axis.
    axis : int, optional
        If defined, the axis of `a`, `b` and `c` that defines the vector(s)
        and cross product(s).  Overrides `axisa`, `axisb` and `axisc`.

    Returns
    -------
    c : ndarray
        Vector cross product(s).

    Raises
    ------
    ValueError
        When the dimension of the vector(s) in `a` and/or `b` does not
        equal 2 or 3.

    See Also
    --------
    inner : Inner product
    outer : Outer product.
    ix_ : Construct index arrays.

    Notes
    -----
    .. versionadded:: 1.9.0

    Supports full broadcasting of the inputs.

    Examples
    --------
    Vector cross-product.

    >>> x = [1, 2, 3]
    >>> y = [4, 5, 6]
    >>> np.cross(x, y)
    array([-3,  6, -3])

    One vector with dimension 2.

    >>> x = [1, 2]
    >>> y = [4, 5, 6]
    >>> np.cross(x, y)
    array([12, -6, -3])

    Equivalently:

    >>> x = [1, 2, 0]
    >>> y = [4, 5, 6]
    >>> np.cross(x, y)
    array([12, -6, -3])

    Both vectors with dimension 2.

    >>> x = [1,2]
    >>> y = [4,5]
    >>> np.cross(x, y)
    array(-3)

    Multiple vector cross-products. Note that the direction of the cross
    product vector is defined by the `right-hand rule`.

    >>> x = np.array([[1,2,3], [4,5,6]])
    >>> y = np.array([[4,5,6], [1,2,3]])
    >>> np.cross(x, y)
    array([[-3,  6, -3],
           [ 3, -6,  3]])

    The orientation of `c` can be changed using the `axisc` keyword.

    >>> np.cross(x, y, axisc=0)
    array([[-3,  3],
           [ 6, -6],
           [-3,  3]])

    Change the vector definition of `x` and `y` using `axisa` and `axisb`.

    >>> x = np.array([[1,2,3], [4,5,6], [7, 8, 9]])
    >>> y = np.array([[7, 8, 9], [4,5,6], [1,2,3]])
    >>> np.cross(x, y)
    array([[ -6,  12,  -6],
           [  0,   0,   0],
           [  6, -12,   6]])
    >>> np.cross(x, y, axisa=0, axisb=0)
    array([[-24,  48, -24],
           [-30,  60, -30],
           [-36,  72, -36]])

    """
    if axis is not None:
        axisa, axisb, axisc = (
         axis,) * 3
    else:
        a = asarray(a)
        b = asarray(b)
        axisa = normalize_axis_index(axisa, (a.ndim), msg_prefix='axisa')
        axisb = normalize_axis_index(axisb, (b.ndim), msg_prefix='axisb')
        a = moveaxis(a, axisa, -1)
        b = moveaxis(b, axisb, -1)
        msg = 'incompatible dimensions for cross product\n(dimension must be 2 or 3)'
        if a.shape[(-1)] not in (2, 3) or b.shape[(-1)] not in (2, 3):
            raise ValueError(msg)
        shape = broadcast(a[(Ellipsis, 0)], b[(Ellipsis, 0)]).shape
        if a.shape[(-1)] == 3 or b.shape[(-1)] == 3:
            shape += (3, )
            axisc = normalize_axis_index(axisc, (len(shape)), msg_prefix='axisc')
        dtype = promote_types(a.dtype, b.dtype)
        cp = empty(shape, dtype)
        a0 = a[(Ellipsis, 0)]
        a1 = a[(Ellipsis, 1)]
        if a.shape[(-1)] == 3:
            a2 = a[(Ellipsis, 2)]
        b0 = b[(Ellipsis, 0)]
        b1 = b[(Ellipsis, 1)]
        if b.shape[(-1)] == 3:
            b2 = b[(Ellipsis, 2)]
        elif cp.ndim != 0:
            if cp.shape[(-1)] == 3:
                cp0 = cp[(Ellipsis, 0)]
                cp1 = cp[(Ellipsis, 1)]
                cp2 = cp[(Ellipsis, 2)]
            if a.shape[(-1)] == 2:
                if b.shape[(-1)] == 2:
                    multiply(a0, b1, out=cp)
                    cp -= a1 * b0
                    return cp
                assert b.shape[(-1)] == 3
                multiply(a1, b2, out=cp0)
                multiply(a0, b2, out=cp1)
                negative(cp1, out=cp1)
                multiply(a0, b1, out=cp2)
                cp2 -= a1 * b0
        else:
            assert a.shape[(-1)] == 3
            if b.shape[(-1)] == 3:
                multiply(a1, b2, out=cp0)
                tmp = array(a2 * b1)
                cp0 -= tmp
                multiply(a2, b0, out=cp1)
                multiply(a0, b2, out=tmp)
                cp1 -= tmp
                multiply(a0, b1, out=cp2)
                multiply(a1, b0, out=tmp)
                cp2 -= tmp
            else:
                assert b.shape[(-1)] == 2
            multiply(a2, b1, out=cp0)
            negative(cp0, out=cp0)
            multiply(a2, b0, out=cp1)
            multiply(a0, b1, out=cp2)
            cp2 -= a1 * b0
    return moveaxis(cp, -1, axisc)


little_endian = sys.byteorder == 'little'

@set_module('numpy')
def indices(dimensions, dtype=int, sparse=False):
    """
    Return an array representing the indices of a grid.

    Compute an array where the subarrays contain index values 0, 1, ...
    varying only along the corresponding axis.

    Parameters
    ----------
    dimensions : sequence of ints
        The shape of the grid.
    dtype : dtype, optional
        Data type of the result.
    sparse : boolean, optional
        Return a sparse representation of the grid instead of a dense
        representation. Default is False.

        .. versionadded:: 1.17

    Returns
    -------
    grid : one ndarray or tuple of ndarrays
        If sparse is False:
            Returns one array of grid indices,
            ``grid.shape = (len(dimensions),) + tuple(dimensions)``.
        If sparse is True:
            Returns a tuple of arrays, with
            ``grid[i].shape = (1, ..., 1, dimensions[i], 1, ..., 1)`` with
            dimensions[i] in the ith place

    See Also
    --------
    mgrid, ogrid, meshgrid

    Notes
    -----
    The output shape in the dense case is obtained by prepending the number
    of dimensions in front of the tuple of dimensions, i.e. if `dimensions`
    is a tuple ``(r0, ..., rN-1)`` of length ``N``, the output shape is
    ``(N, r0, ..., rN-1)``.

    The subarrays ``grid[k]`` contains the N-D array of indices along the
    ``k-th`` axis. Explicitly::

        grid[k, i0, i1, ..., iN-1] = ik

    Examples
    --------
    >>> grid = np.indices((2, 3))
    >>> grid.shape
    (2, 2, 3)
    >>> grid[0]        # row indices
    array([[0, 0, 0],
           [1, 1, 1]])
    >>> grid[1]        # column indices
    array([[0, 1, 2],
           [0, 1, 2]])

    The indices can be used as an index into an array.

    >>> x = np.arange(20).reshape(5, 4)
    >>> row, col = np.indices((2, 3))
    >>> x[row, col]
    array([[0, 1, 2],
           [4, 5, 6]])

    Note that it would be more straightforward in the above example to
    extract the required elements directly with ``x[:2, :3]``.

    If sparse is set to true, the grid will be returned in a sparse
    representation.

    >>> i, j = np.indices((2, 3), sparse=True)
    >>> i.shape
    (2, 1)
    >>> j.shape
    (1, 3)
    >>> i        # row indices
    array([[0],
           [1]])
    >>> j        # column indices
    array([[0, 1, 2]])

    """
    dimensions = tuple(dimensions)
    N = len(dimensions)
    shape = (1, ) * N
    if sparse:
        res = tuple()
    else:
        res = empty(((N,) + dimensions), dtype=dtype)
    for i, dim in enumerate(dimensions):
        idx = arange(dim, dtype=dtype).reshape(shape[:i] + (dim,) + shape[i + 1:])
        if sparse:
            res = res + (idx,)
        else:
            res[i] = idx
    else:
        return res


@set_module('numpy')
def fromfunction(function, shape, *, dtype=float, **kwargs):
    """
    Construct an array by executing a function over each coordinate.

    The resulting array therefore has a value ``fn(x, y, z)`` at
    coordinate ``(x, y, z)``.

    Parameters
    ----------
    function : callable
        The function is called with N parameters, where N is the rank of
        `shape`.  Each parameter represents the coordinates of the array
        varying along a specific axis.  For example, if `shape`
        were ``(2, 2)``, then the parameters would be
        ``array([[0, 0], [1, 1]])`` and ``array([[0, 1], [0, 1]])``
    shape : (N,) tuple of ints
        Shape of the output array, which also determines the shape of
        the coordinate arrays passed to `function`.
    dtype : data-type, optional
        Data-type of the coordinate arrays passed to `function`.
        By default, `dtype` is float.

    Returns
    -------
    fromfunction : any
        The result of the call to `function` is passed back directly.
        Therefore the shape of `fromfunction` is completely determined by
        `function`.  If `function` returns a scalar value, the shape of
        `fromfunction` would not match the `shape` parameter.

    See Also
    --------
    indices, meshgrid

    Notes
    -----
    Keywords other than `dtype` are passed to `function`.

    Examples
    --------
    >>> np.fromfunction(lambda i, j: i == j, (3, 3), dtype=int)
    array([[ True, False, False],
           [False,  True, False],
           [False, False,  True]])

    >>> np.fromfunction(lambda i, j: i + j, (3, 3), dtype=int)
    array([[0, 1, 2],
           [1, 2, 3],
           [2, 3, 4]])

    """
    args = indices(shape, dtype=dtype)
    return function(*args, **kwargs)


def _frombuffer(buf, dtype, shape, order):
    return frombuffer(buf, dtype=dtype).reshape(shape, order=order)


@set_module('numpy')
def isscalar(element):
    """
    Returns True if the type of `element` is a scalar type.

    Parameters
    ----------
    element : any
        Input argument, can be of any type and shape.

    Returns
    -------
    val : bool
        True if `element` is a scalar type, False if it is not.

    See Also
    --------
    ndim : Get the number of dimensions of an array

    Notes
    -----
    If you need a stricter way to identify a *numerical* scalar, use
    ``isinstance(x, numbers.Number)``, as that returns ``False`` for most
    non-numerical elements such as strings.

    In most cases ``np.ndim(x) == 0`` should be used instead of this function,
    as that will also return true for 0d arrays. This is how numpy overloads
    functions in the style of the ``dx`` arguments to `gradient` and the ``bins``
    argument to `histogram`. Some key differences:

    +--------------------------------------+---------------+-------------------+
    | x                                    |``isscalar(x)``|``np.ndim(x) == 0``|
    +======================================+===============+===================+
    | PEP 3141 numeric objects (including  | ``True``      | ``True``          |
    | builtins)                            |               |                   |
    +--------------------------------------+---------------+-------------------+
    | builtin string and buffer objects    | ``True``      | ``True``          |
    +--------------------------------------+---------------+-------------------+
    | other builtin objects, like          | ``False``     | ``True``          |
    | `pathlib.Path`, `Exception`,         |               |                   |
    | the result of `re.compile`           |               |                   |
    +--------------------------------------+---------------+-------------------+
    | third-party objects like             | ``False``     | ``True``          |
    | `matplotlib.figure.Figure`           |               |                   |
    +--------------------------------------+---------------+-------------------+
    | zero-dimensional numpy arrays        | ``False``     | ``True``          |
    +--------------------------------------+---------------+-------------------+
    | other numpy arrays                   | ``False``     | ``False``         |
    +--------------------------------------+---------------+-------------------+
    | `list`, `tuple`, and other sequence  | ``False``     | ``False``         |
    | objects                              |               |                   |
    +--------------------------------------+---------------+-------------------+

    Examples
    --------
    >>> np.isscalar(3.1)
    True
    >>> np.isscalar(np.array(3.1))
    False
    >>> np.isscalar([3.1])
    False
    >>> np.isscalar(False)
    True
    >>> np.isscalar('numpy')
    True

    NumPy supports PEP 3141 numbers:

    >>> from fractions import Fraction
    >>> np.isscalar(Fraction(5, 17))
    True
    >>> from numbers import Number
    >>> np.isscalar(Number())
    True

    """
    return isinstance(element, generic) or type(element) in ScalarType or isinstance(element, numbers.Number)


@set_module('numpy')
def binary_repr(num, width=None):
    """
    Return the binary representation of the input number as a string.

    For negative numbers, if width is not given, a minus sign is added to the
    front. If width is given, the two's complement of the number is
    returned, with respect to that width.

    In a two's-complement system negative numbers are represented by the two's
    complement of the absolute value. This is the most common method of
    representing signed integers on computers [1]_. A N-bit two's-complement
    system can represent every integer in the range
    :math:`-2^{N-1}` to :math:`+2^{N-1}-1`.

    Parameters
    ----------
    num : int
        Only an integer decimal number can be used.
    width : int, optional
        The length of the returned string if `num` is positive, or the length
        of the two's complement if `num` is negative, provided that `width` is
        at least a sufficient number of bits for `num` to be represented in the
        designated form.

        If the `width` value is insufficient, it will be ignored, and `num` will
        be returned in binary (`num` > 0) or two's complement (`num` < 0) form
        with its width equal to the minimum number of bits needed to represent
        the number in the designated form. This behavior is deprecated and will
        later raise an error.

        .. deprecated:: 1.12.0

    Returns
    -------
    bin : str
        Binary representation of `num` or two's complement of `num`.

    See Also
    --------
    base_repr: Return a string representation of a number in the given base
               system.
    bin: Python's built-in binary representation generator of an integer.

    Notes
    -----
    `binary_repr` is equivalent to using `base_repr` with base 2, but about 25x
    faster.

    References
    ----------
    .. [1] Wikipedia, "Two's complement",
        https://en.wikipedia.org/wiki/Two's_complement

    Examples
    --------
    >>> np.binary_repr(3)
    '11'
    >>> np.binary_repr(-3)
    '-11'
    >>> np.binary_repr(3, width=4)
    '0011'

    The two's complement is returned when the input number is negative and
    width is specified:

    >>> np.binary_repr(-3, width=3)
    '101'
    >>> np.binary_repr(-3, width=5)
    '11101'

    """

    def warn_if_insufficient(width, binwidth):
        if width is not None:
            if width < binwidth:
                warnings.warn('Insufficient bit width provided. This behavior will raise an error in the future.',
                  DeprecationWarning,
                  stacklevel=3)

    num = operator.index(num)
    if num == 0:
        return '0' * (width or 1)
    if num > 0:
        binary = bin(num)[2:]
        binwidth = len(binary)
        outwidth = binwidth if width is None else max(binwidth, width)
        warn_if_insufficient(width, binwidth)
        return binary.zfill(outwidth)
    if width is None:
        return '-' + bin(-num)[2:]
    poswidth = len(bin(-num)[2:])
    if 2 ** (poswidth - 1) == -num:
        poswidth -= 1
    twocomp = 2 ** (poswidth + 1) + num
    binary = bin(twocomp)[2:]
    binwidth = len(binary)
    outwidth = max(binwidth, width)
    warn_if_insufficient(width, binwidth)
    return '1' * (outwidth - binwidth) + binary


@set_module('numpy')
def base_repr(number, base=2, padding=0):
    """
    Return a string representation of a number in the given base system.

    Parameters
    ----------
    number : int
        The value to convert. Positive and negative values are handled.
    base : int, optional
        Convert `number` to the `base` number system. The valid range is 2-36,
        the default value is 2.
    padding : int, optional
        Number of zeros padded on the left. Default is 0 (no padding).

    Returns
    -------
    out : str
        String representation of `number` in `base` system.

    See Also
    --------
    binary_repr : Faster version of `base_repr` for base 2.

    Examples
    --------
    >>> np.base_repr(5)
    '101'
    >>> np.base_repr(6, 5)
    '11'
    >>> np.base_repr(7, base=5, padding=3)
    '00012'

    >>> np.base_repr(10, base=16)
    'A'
    >>> np.base_repr(32, base=16)
    '20'

    """
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if base > len(digits):
        raise ValueError('Bases greater than 36 not handled in base_repr.')
    else:
        if base < 2:
            raise ValueError('Bases less than 2 not handled in base_repr.')
        else:
            num = abs(number)
            res = []
            while True:
                if num:
                    res.append(digits[(num % base)])
                    num //= base

        if padding:
            res.append('0' * padding)
        if number < 0:
            res.append('-')
        return ''.join(reversed(res or '0'))


def _maketup(descr, val):
    dt = dtype(descr)
    fields = dt.fields
    if fields is None:
        return val
    res = [_maketup(fields[name][0], val) for name in dt.names]
    return tuple(res)


@set_module('numpy')
def identity(n, dtype=None):
    """
    Return the identity array.

    The identity array is a square array with ones on
    the main diagonal.

    Parameters
    ----------
    n : int
        Number of rows (and columns) in `n` x `n` output.
    dtype : data-type, optional
        Data-type of the output.  Defaults to ``float``.

    Returns
    -------
    out : ndarray
        `n` x `n` array with its main diagonal set to one,
        and all other elements 0.

    Examples
    --------
    >>> np.identity(3)
    array([[1.,  0.,  0.],
           [0.,  1.,  0.],
           [0.,  0.,  1.]])

    """
    from numpy import eye
    return eye(n, dtype=dtype)


def _allclose_dispatcher(a, b, rtol=None, atol=None, equal_nan=None):
    return (
     a, b)


@array_function_dispatch(_allclose_dispatcher)
def allclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False):
    """
    Returns True if two arrays are element-wise equal within a tolerance.

    The tolerance values are positive, typically very small numbers.  The
    relative difference (`rtol` * abs(`b`)) and the absolute difference
    `atol` are added together to compare against the absolute difference
    between `a` and `b`.

    NaNs are treated as equal if they are in the same place and if
    ``equal_nan=True``.  Infs are treated as equal if they are in the same
    place and of the same sign in both arrays.

    Parameters
    ----------
    a, b : array_like
        Input arrays to compare.
    rtol : float
        The relative tolerance parameter (see Notes).
    atol : float
        The absolute tolerance parameter (see Notes).
    equal_nan : bool
        Whether to compare NaN's as equal.  If True, NaN's in `a` will be
        considered equal to NaN's in `b` in the output array.

        .. versionadded:: 1.10.0

    Returns
    -------
    allclose : bool
        Returns True if the two arrays are equal within the given
        tolerance; False otherwise.

    See Also
    --------
    isclose, all, any, equal

    Notes
    -----
    If the following equation is element-wise True, then allclose returns
    True.

     absolute(`a` - `b`) <= (`atol` + `rtol` * absolute(`b`))

    The above equation is not symmetric in `a` and `b`, so that
    ``allclose(a, b)`` might be different from ``allclose(b, a)`` in
    some rare cases.

    The comparison of `a` and `b` uses standard broadcasting, which
    means that `a` and `b` need not have the same shape in order for
    ``allclose(a, b)`` to evaluate to True.  The same is true for
    `equal` but not `array_equal`.

    Examples
    --------
    >>> np.allclose([1e10,1e-7], [1.00001e10,1e-8])
    False
    >>> np.allclose([1e10,1e-8], [1.00001e10,1e-9])
    True
    >>> np.allclose([1e10,1e-8], [1.0001e10,1e-9])
    False
    >>> np.allclose([1.0, np.nan], [1.0, np.nan])
    False
    >>> np.allclose([1.0, np.nan], [1.0, np.nan], equal_nan=True)
    True

    """
    res = all(isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan))
    return bool(res)


def _isclose_dispatcher(a, b, rtol=None, atol=None, equal_nan=None):
    return (
     a, b)


@array_function_dispatch(_isclose_dispatcher)
def isclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False):
    """
    Returns a boolean array where two arrays are element-wise equal within a
    tolerance.

    The tolerance values are positive, typically very small numbers.  The
    relative difference (`rtol` * abs(`b`)) and the absolute difference
    `atol` are added together to compare against the absolute difference
    between `a` and `b`.

    .. warning:: The default `atol` is not appropriate for comparing numbers
                 that are much smaller than one (see Notes).

    Parameters
    ----------
    a, b : array_like
        Input arrays to compare.
    rtol : float
        The relative tolerance parameter (see Notes).
    atol : float
        The absolute tolerance parameter (see Notes).
    equal_nan : bool
        Whether to compare NaN's as equal.  If True, NaN's in `a` will be
        considered equal to NaN's in `b` in the output array.

    Returns
    -------
    y : array_like
        Returns a boolean array of where `a` and `b` are equal within the
        given tolerance. If both `a` and `b` are scalars, returns a single
        boolean value.

    See Also
    --------
    allclose

    Notes
    -----
    .. versionadded:: 1.7.0

    For finite values, isclose uses the following equation to test whether
    two floating point values are equivalent.

     absolute(`a` - `b`) <= (`atol` + `rtol` * absolute(`b`))

    Unlike the built-in `math.isclose`, the above equation is not symmetric
    in `a` and `b` -- it assumes `b` is the reference value -- so that
    `isclose(a, b)` might be different from `isclose(b, a)`. Furthermore,
    the default value of atol is not zero, and is used to determine what
    small values should be considered close to zero. The default value is
    appropriate for expected values of order unity: if the expected values
    are significantly smaller than one, it can result in false positives.
    `atol` should be carefully selected for the use case at hand. A zero value
    for `atol` will result in `False` if either `a` or `b` is zero.

    Examples
    --------
    >>> np.isclose([1e10,1e-7], [1.00001e10,1e-8])
    array([ True, False])
    >>> np.isclose([1e10,1e-8], [1.00001e10,1e-9])
    array([ True, True])
    >>> np.isclose([1e10,1e-8], [1.0001e10,1e-9])
    array([False,  True])
    >>> np.isclose([1.0, np.nan], [1.0, np.nan])
    array([ True, False])
    >>> np.isclose([1.0, np.nan], [1.0, np.nan], equal_nan=True)
    array([ True, True])
    >>> np.isclose([1e-8, 1e-7], [0.0, 0.0])
    array([ True, False])
    >>> np.isclose([1e-100, 1e-7], [0.0, 0.0], atol=0.0)
    array([False, False])
    >>> np.isclose([1e-10, 1e-10], [1e-20, 0.0])
    array([ True,  True])
    >>> np.isclose([1e-10, 1e-10], [1e-20, 0.999999e-10], atol=0.0)
    array([False,  True])
    """

    def within_tol--- This code section failed: ---

 L.2275         0  LOAD_GLOBAL              errstate
                2  LOAD_STR                 'ignore'
                4  LOAD_CONST               ('invalid',)
                6  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
                8  SETUP_WITH           54  'to 54'
               10  POP_TOP          

 L.2276        12  LOAD_GLOBAL              less_equal
               14  LOAD_GLOBAL              abs
               16  LOAD_FAST                'x'
               18  LOAD_FAST                'y'
               20  BINARY_SUBTRACT  
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_FAST                'atol'
               26  LOAD_FAST                'rtol'
               28  LOAD_GLOBAL              abs
               30  LOAD_FAST                'y'
               32  CALL_FUNCTION_1       1  ''
               34  BINARY_MULTIPLY  
               36  BINARY_ADD       
               38  CALL_FUNCTION_2       2  ''
               40  POP_BLOCK        
               42  ROT_TWO          
               44  BEGIN_FINALLY    
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  POP_FINALLY           0  ''
               52  RETURN_VALUE     
             54_0  COME_FROM_WITH        8  '8'
               54  WITH_CLEANUP_START
               56  WITH_CLEANUP_FINISH
               58  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 42

    x = asanyarray(a)
    y = asanyarray(b)
    dt = multiarray.result_type(y, 1.0)
    y = array(y, dtype=dt, copy=False, subok=True)
    xfin = isfinite(x)
    yfin = isfinite(y)
    if all(xfin):
        if all(yfin):
            return within_tol(x, y, atol, rtol)
    finite = xfin & yfin
    cond = zeros_like(finite, subok=True)
    x = x * ones_like(cond)
    y = y * ones_like(cond)
    cond[finite] = within_tol(x[finite], y[finite], atol, rtol)
    cond[~finite] = x[(~finite)] == y[(~finite)]
    if equal_nan:
        both_nan = isnan(x) & isnan(y)
        cond[both_nan] = both_nan[both_nan]
    return cond[()]


def _array_equal_dispatcher(a1, a2, equal_nan=None):
    return (
     a1, a2)


@array_function_dispatch(_array_equal_dispatcher)
def array_equal(a1, a2, equal_nan=False):
    """
    True if two arrays have the same shape and elements, False otherwise.

    Parameters
    ----------
    a1, a2 : array_like
        Input arrays.
    equal_nan : bool
        Whether to compare NaN's as equal. If the dtype of a1 and a2 is
        complex, values will be considered equal if either the real or the
        imaginary component of a given value is ``nan``.

        .. versionadded:: 1.19.0

    Returns
    -------
    b : bool
        Returns True if the arrays are equal.

    See Also
    --------
    allclose: Returns True if two arrays are element-wise equal within a
              tolerance.
    array_equiv: Returns True if input arrays are shape consistent and all
                 elements equal.

    Examples
    --------
    >>> np.array_equal([1, 2], [1, 2])
    True
    >>> np.array_equal(np.array([1, 2]), np.array([1, 2]))
    True
    >>> np.array_equal([1, 2], [1, 2, 3])
    False
    >>> np.array_equal([1, 2], [1, 4])
    False
    >>> a = np.array([1, np.nan])
    >>> np.array_equal(a, a)
    False
    >>> np.array_equal(a, a, equal_nan=True)
    True

    When ``equal_nan`` is True, complex values with nan components are
    considered equal if either the real *or* the imaginary components are nan.

    >>> a = np.array([1 + 1j])
    >>> b = a.copy()
    >>> a.real = np.nan
    >>> b.imag = np.nan
    >>> np.array_equal(a, b, equal_nan=True)
    True
    """
    try:
        a1, a2 = asarray(a1), asarray(a2)
    except Exception:
        return False
    else:
        if a1.shape != a2.shape:
            return False
        else:
            if not equal_nan:
                return bool(asarray(a1 == a2).all())
            a1nan, a2nan = isnan(a1), isnan(a2)
            return (a1nan == a2nan).all() or False
        return bool(asarray(a1[(~a1nan)] == a2[(~a1nan)]).all())


def _array_equiv_dispatcher(a1, a2):
    return (
     a1, a2)


@array_function_dispatch(_array_equiv_dispatcher)
def array_equiv(a1, a2):
    """
    Returns True if input arrays are shape consistent and all elements equal.

    Shape consistent means they are either the same shape, or one input array
    can be broadcasted to create the same shape as the other one.

    Parameters
    ----------
    a1, a2 : array_like
        Input arrays.

    Returns
    -------
    out : bool
        True if equivalent, False otherwise.

    Examples
    --------
    >>> np.array_equiv([1, 2], [1, 2])
    True
    >>> np.array_equiv([1, 2], [1, 3])
    False

    Showing the shape equivalence:

    >>> np.array_equiv([1, 2], [[1, 2], [1, 2]])
    True
    >>> np.array_equiv([1, 2], [[1, 2, 1, 2], [1, 2, 1, 2]])
    False

    >>> np.array_equiv([1, 2], [[1, 2], [1, 3]])
    False

    """
    try:
        a1, a2 = asarray(a1), asarray(a2)
    except Exception:
        return False
    else:
        try:
            multiarray.broadcast(a1, a2)
        except Exception:
            return False
        else:
            return bool(asarray(a1 == a2).all())


Inf = inf = infty = Infinity = PINF
nan = NaN = NAN
False_ = bool_(False)
True_ = bool_(True)

def extend_all(module):
    existing = set(__all__)
    mall = getattr(module, '__all__')
    for a in mall:
        if a not in existing:
            __all__.append(a)


from .umath import *
from .numerictypes import *
from . import fromnumeric
from .fromnumeric import *
from . import arrayprint
from .arrayprint import *
from . import _asarray
from ._asarray import *
from . import _ufunc_config
from ._ufunc_config import *
extend_all(fromnumeric)
extend_all(umath)
extend_all(numerictypes)
extend_all(arrayprint)
extend_all(_asarray)
extend_all(_ufunc_config)