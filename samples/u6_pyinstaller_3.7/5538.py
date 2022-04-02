# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\linalg\linalg.py
"""Lite version of scipy.linalg.

Notes
-----
This module is a lite version of the linalg.py module in SciPy which
contains high-level Python interface to the LAPACK library.  The lite
version only accesses the following LAPACK functions: dgesv, zgesv,
dgeev, zgeev, dgesdd, zgesdd, dgelsd, zgelsd, dsyevd, zheevd, dgetrf,
zgetrf, dpotrf, zpotrf, dgeqrf, zgeqrf, zungqr, dorgqr.
"""
__all__ = [
 'matrix_power', 'solve', 'tensorsolve', 'tensorinv', 'inv',
 'cholesky', 'eigvals', 'eigvalsh', 'pinv', 'slogdet', 'det',
 'svd', 'eig', 'eigh', 'lstsq', 'norm', 'qr', 'cond', 'matrix_rank',
 'LinAlgError', 'multi_dot']
import functools, operator, warnings
from numpy.core import array, asarray, zeros, empty, empty_like, intc, single, double, csingle, cdouble, inexact, complexfloating, newaxis, all, Inf, dot, add, multiply, sqrt, fastCopyAndTranspose, sum, isfinite, finfo, errstate, geterrobj, moveaxis, amin, amax, product, abs, atleast_2d, intp, asanyarray, object_, matmul, swapaxes, divide, count_nonzero, isnan, sign, argsort, sort
from numpy.core.multiarray import normalize_axis_index
from numpy.core.overrides import set_module
from numpy.core import overrides
from numpy.lib.twodim_base import triu, eye
from numpy.linalg import lapack_lite, _umath_linalg
array_function_dispatch = functools.partial((overrides.array_function_dispatch),
  module='numpy.linalg')
fortran_int = intc

@set_module('numpy.linalg')
class LinAlgError(Exception):
    __doc__ = '\n    Generic Python-exception-derived object raised by linalg functions.\n\n    General purpose exception class, derived from Python\'s exception.Exception\n    class, programmatically raised in linalg functions when a Linear\n    Algebra-related condition would prevent further correct execution of the\n    function.\n\n    Parameters\n    ----------\n    None\n\n    Examples\n    --------\n    >>> from numpy import linalg as LA\n    >>> LA.inv(np.zeros((2,2)))\n    Traceback (most recent call last):\n      File "<stdin>", line 1, in <module>\n      File "...linalg.py", line 350,\n        in inv return wrap(solve(a, identity(a.shape[0], dtype=a.dtype)))\n      File "...linalg.py", line 249,\n        in solve\n        raise LinAlgError(\'Singular matrix\')\n    numpy.linalg.LinAlgError: Singular matrix\n\n    '


def _determine_error_states():
    errobj = geterrobj()
    bufsize = errobj[0]
    with errstate(invalid='call', over='ignore', divide='ignore',
      under='ignore'):
        invalid_call_errmask = geterrobj()[1]
    return [bufsize, invalid_call_errmask, None]


_linalg_error_extobj = _determine_error_states()
del _determine_error_states

def _raise_linalgerror_singular(err, flag):
    raise LinAlgError('Singular matrix')


def _raise_linalgerror_nonposdef(err, flag):
    raise LinAlgError('Matrix is not positive definite')


def _raise_linalgerror_eigenvalues_nonconvergence(err, flag):
    raise LinAlgError('Eigenvalues did not converge')


def _raise_linalgerror_svd_nonconvergence(err, flag):
    raise LinAlgError('SVD did not converge')


def _raise_linalgerror_lstsq(err, flag):
    raise LinAlgError('SVD did not converge in Linear Least Squares')


def get_linalg_error_extobj(callback):
    extobj = list(_linalg_error_extobj)
    extobj[2] = callback
    return extobj


def _makearray(a):
    new = asarray(a)
    wrap = getattr(a, '__array_prepare__', new.__array_wrap__)
    return (new, wrap)


def isComplexType(t):
    return issubclass(t, complexfloating)


_real_types_map = {single: single, 
 double: double, 
 csingle: single, 
 cdouble: double}
_complex_types_map = {single: csingle, 
 double: cdouble, 
 csingle: csingle, 
 cdouble: cdouble}

def _realType(t, default=double):
    return _real_types_map.get(t, default)


def _complexType(t, default=cdouble):
    return _complex_types_map.get(t, default)


def _linalgRealType(t):
    """Cast the type t to either double or cdouble."""
    return double


def _commonType(*arrays):
    result_type = single
    is_complex = False
    for a in arrays:
        if issubclass(a.dtype.type, inexact):
            if isComplexType(a.dtype.type):
                is_complex = True
            else:
                rt = _realType((a.dtype.type), default=None)
                if rt is None:
                    raise TypeError('array type %s is unsupported in linalg' % (
                     a.dtype.name,))
                else:
                    rt = double
            if rt is double:
                result_type = double

    if is_complex:
        t = cdouble
        result_type = _complex_types_map[result_type]
    else:
        t = double
    return (
     t, result_type)


_fastCT = fastCopyAndTranspose

def _to_native_byte_order(*arrays):
    ret = []
    for arr in arrays:
        if arr.dtype.byteorder not in ('=', '|'):
            ret.append(asarray(arr, dtype=(arr.dtype.newbyteorder('='))))
        else:
            ret.append(arr)

    if len(ret) == 1:
        return ret[0]
    return ret


def _fastCopyAndTranspose(type, *arrays):
    cast_arrays = ()
    for a in arrays:
        if a.dtype.type is type:
            cast_arrays = cast_arrays + (_fastCT(a),)
        else:
            cast_arrays = cast_arrays + (_fastCT(a.astype(type)),)

    if len(cast_arrays) == 1:
        return cast_arrays[0]
    return cast_arrays


def _assert_2d(*arrays):
    for a in arrays:
        if a.ndim != 2:
            raise LinAlgError('%d-dimensional array given. Array must be two-dimensional' % a.ndim)


def _assert_stacked_2d(*arrays):
    for a in arrays:
        if a.ndim < 2:
            raise LinAlgError('%d-dimensional array given. Array must be at least two-dimensional' % a.ndim)


def _assert_stacked_square(*arrays):
    for a in arrays:
        m, n = a.shape[-2:]
        if m != n:
            raise LinAlgError('Last 2 dimensions of the array must be square')


def _assert_finite(*arrays):
    for a in arrays:
        if not isfinite(a).all():
            raise LinAlgError('Array must not contain infs or NaNs')


def _is_empty_2d(arr):
    return arr.size == 0 and product(arr.shape[-2:]) == 0


def transpose(a):
    """
    Transpose each matrix in a stack of matrices.

    Unlike np.transpose, this only swaps the last two axes, rather than all of
    them

    Parameters
    ----------
    a : (...,M,N) array_like

    Returns
    -------
    aT : (...,N,M) ndarray
    """
    return swapaxes(a, -1, -2)


def _tensorsolve_dispatcher(a, b, axes=None):
    return (
     a, b)


@array_function_dispatch(_tensorsolve_dispatcher)
def tensorsolve(a, b, axes=None):
    """
    Solve the tensor equation ``a x = b`` for x.

    It is assumed that all indices of `x` are summed over in the product,
    together with the rightmost indices of `a`, as is done in, for example,
    ``tensordot(a, x, axes=b.ndim)``.

    Parameters
    ----------
    a : array_like
        Coefficient tensor, of shape ``b.shape + Q``. `Q`, a tuple, equals
        the shape of that sub-tensor of `a` consisting of the appropriate
        number of its rightmost indices, and must be such that
        ``prod(Q) == prod(b.shape)`` (in which sense `a` is said to be
        'square').
    b : array_like
        Right-hand tensor, which can be of any shape.
    axes : tuple of ints, optional
        Axes in `a` to reorder to the right, before inversion.
        If None (default), no reordering is done.

    Returns
    -------
    x : ndarray, shape Q

    Raises
    ------
    LinAlgError
        If `a` is singular or not 'square' (in the above sense).

    See Also
    --------
    numpy.tensordot, tensorinv, numpy.einsum

    Examples
    --------
    >>> a = np.eye(2*3*4)
    >>> a.shape = (2*3, 4, 2, 3, 4)
    >>> b = np.random.randn(2*3, 4)
    >>> x = np.linalg.tensorsolve(a, b)
    >>> x.shape
    (2, 3, 4)
    >>> np.allclose(np.tensordot(a, x, axes=3), b)
    True

    """
    a, wrap = _makearray(a)
    b = asarray(b)
    an = a.ndim
    if axes is not None:
        allaxes = list(range(0, an))
        for k in axes:
            allaxes.remove(k)
            allaxes.insert(an, k)

        a = a.transpose(allaxes)
    oldshape = a.shape[-(an - b.ndim):]
    prod = 1
    for k in oldshape:
        prod *= k

    a = a.reshape(-1, prod)
    b = b.ravel()
    res = wrap(solve(a, b))
    res.shape = oldshape
    return res


def _solve_dispatcher(a, b):
    return (
     a, b)


@array_function_dispatch(_solve_dispatcher)
def solve(a, b):
    """
    Solve a linear matrix equation, or system of linear scalar equations.

    Computes the "exact" solution, `x`, of the well-determined, i.e., full
    rank, linear matrix equation `ax = b`.

    Parameters
    ----------
    a : (..., M, M) array_like
        Coefficient matrix.
    b : {(..., M,), (..., M, K)}, array_like
        Ordinate or "dependent variable" values.

    Returns
    -------
    x : {(..., M,), (..., M, K)} ndarray
        Solution to the system a x = b.  Returned shape is identical to `b`.

    Raises
    ------
    LinAlgError
        If `a` is singular or not square.

    See Also
    --------
    scipy.linalg.solve : Similar function in SciPy.

    Notes
    -----

    .. versionadded:: 1.8.0

    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The solutions are computed using LAPACK routine ``_gesv``.

    `a` must be square and of full-rank, i.e., all rows (or, equivalently,
    columns) must be linearly independent; if either is not true, use
    `lstsq` for the least-squares best "solution" of the
    system/equation.

    References
    ----------
    .. [1] G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando,
           FL, Academic Press, Inc., 1980, pg. 22.

    Examples
    --------
    Solve the system of equations ``3 * x0 + x1 = 9`` and ``x0 + 2 * x1 = 8``:

    >>> a = np.array([[3,1], [1,2]])
    >>> b = np.array([9,8])
    >>> x = np.linalg.solve(a, b)
    >>> x
    array([2.,  3.])

    Check that the solution is correct:

    >>> np.allclose(np.dot(a, x), b)
    True

    """
    a, _ = _makearray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    b, wrap = _makearray(b)
    t, result_t = _commonType(a, b)
    if b.ndim == a.ndim - 1:
        gufunc = _umath_linalg.solve1
    else:
        gufunc = _umath_linalg.solve
    signature = 'DD->D' if isComplexType(t) else 'dd->d'
    extobj = get_linalg_error_extobj(_raise_linalgerror_singular)
    r = gufunc(a, b, signature=signature, extobj=extobj)
    return wrap(r.astype(result_t, copy=False))


def _tensorinv_dispatcher(a, ind=None):
    return (
     a,)


@array_function_dispatch(_tensorinv_dispatcher)
def tensorinv(a, ind=2):
    """
    Compute the 'inverse' of an N-dimensional array.

    The result is an inverse for `a` relative to the tensordot operation
    ``tensordot(a, b, ind)``, i. e., up to floating-point accuracy,
    ``tensordot(tensorinv(a), a, ind)`` is the "identity" tensor for the
    tensordot operation.

    Parameters
    ----------
    a : array_like
        Tensor to 'invert'. Its shape must be 'square', i. e.,
        ``prod(a.shape[:ind]) == prod(a.shape[ind:])``.
    ind : int, optional
        Number of first indices that are involved in the inverse sum.
        Must be a positive integer, default is 2.

    Returns
    -------
    b : ndarray
        `a`'s tensordot inverse, shape ``a.shape[ind:] + a.shape[:ind]``.

    Raises
    ------
    LinAlgError
        If `a` is singular or not 'square' (in the above sense).

    See Also
    --------
    numpy.tensordot, tensorsolve

    Examples
    --------
    >>> a = np.eye(4*6)
    >>> a.shape = (4, 6, 8, 3)
    >>> ainv = np.linalg.tensorinv(a, ind=2)
    >>> ainv.shape
    (8, 3, 4, 6)
    >>> b = np.random.randn(4, 6)
    >>> np.allclose(np.tensordot(ainv, b), np.linalg.tensorsolve(a, b))
    True

    >>> a = np.eye(4*6)
    >>> a.shape = (24, 8, 3)
    >>> ainv = np.linalg.tensorinv(a, ind=1)
    >>> ainv.shape
    (8, 3, 24)
    >>> b = np.random.randn(24)
    >>> np.allclose(np.tensordot(ainv, b, 1), np.linalg.tensorsolve(a, b))
    True

    """
    a = asarray(a)
    oldshape = a.shape
    prod = 1
    if ind > 0:
        invshape = oldshape[ind:] + oldshape[:ind]
        for k in oldshape[ind:]:
            prod *= k

    else:
        raise ValueError('Invalid ind argument.')
    a = a.reshape(prod, -1)
    ia = inv(a)
    return (ia.reshape)(*invshape)


def _unary_dispatcher(a):
    return (
     a,)


@array_function_dispatch(_unary_dispatcher)
def inv(a):
    """
    Compute the (multiplicative) inverse of a matrix.

    Given a square matrix `a`, return the matrix `ainv` satisfying
    ``dot(a, ainv) = dot(ainv, a) = eye(a.shape[0])``.

    Parameters
    ----------
    a : (..., M, M) array_like
        Matrix to be inverted.

    Returns
    -------
    ainv : (..., M, M) ndarray or matrix
        (Multiplicative) inverse of the matrix `a`.

    Raises
    ------
    LinAlgError
        If `a` is not square or inversion fails.

    See Also
    --------
    scipy.linalg.inv : Similar function in SciPy.

    Notes
    -----

    .. versionadded:: 1.8.0

    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    Examples
    --------
    >>> from numpy.linalg import inv
    >>> a = np.array([[1., 2.], [3., 4.]])
    >>> ainv = inv(a)
    >>> np.allclose(np.dot(a, ainv), np.eye(2))
    True
    >>> np.allclose(np.dot(ainv, a), np.eye(2))
    True

    If a is a matrix object, then the return value is a matrix as well:

    >>> ainv = inv(np.matrix(a))
    >>> ainv
    matrix([[-2. ,  1. ],
            [ 1.5, -0.5]])

    Inverses of several matrices can be computed at once:

    >>> a = np.array([[[1., 2.], [3., 4.]], [[1, 3], [3, 5]]])
    >>> inv(a)
    array([[[-2.  ,  1.  ],
            [ 1.5 , -0.5 ]],
           [[-1.25,  0.75],
            [ 0.75, -0.25]]])

    """
    a, wrap = _makearray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)
    signature = 'D->D' if isComplexType(t) else 'd->d'
    extobj = get_linalg_error_extobj(_raise_linalgerror_singular)
    ainv = _umath_linalg.inv(a, signature=signature, extobj=extobj)
    return wrap(ainv.astype(result_t, copy=False))


def _matrix_power_dispatcher(a, n):
    return (
     a,)


@array_function_dispatch(_matrix_power_dispatcher)
def matrix_power(a, n):
    """
    Raise a square matrix to the (integer) power `n`.

    For positive integers `n`, the power is computed by repeated matrix
    squarings and matrix multiplications. If ``n == 0``, the identity matrix
    of the same shape as M is returned. If ``n < 0``, the inverse
    is computed and then raised to the ``abs(n)``.

    .. note:: Stacks of object matrices are not currently supported.

    Parameters
    ----------
    a : (..., M, M) array_like
        Matrix to be "powered".
    n : int
        The exponent can be any integer or long integer, positive,
        negative, or zero.

    Returns
    -------
    a**n : (..., M, M) ndarray or matrix object
        The return value is the same shape and type as `M`;
        if the exponent is positive or zero then the type of the
        elements is the same as those of `M`. If the exponent is
        negative the elements are floating-point.

    Raises
    ------
    LinAlgError
        For matrices that are not square or that (for negative powers) cannot
        be inverted numerically.

    Examples
    --------
    >>> from numpy.linalg import matrix_power
    >>> i = np.array([[0, 1], [-1, 0]]) # matrix equiv. of the imaginary unit
    >>> matrix_power(i, 3) # should = -i
    array([[ 0, -1],
           [ 1,  0]])
    >>> matrix_power(i, 0)
    array([[1, 0],
           [0, 1]])
    >>> matrix_power(i, -3) # should = 1/(-i) = i, but w/ f.p. elements
    array([[ 0.,  1.],
           [-1.,  0.]])

    Somewhat more sophisticated example

    >>> q = np.zeros((4, 4))
    >>> q[0:2, 0:2] = -i
    >>> q[2:4, 2:4] = i
    >>> q # one of the three quaternion units not equal to 1
    array([[ 0., -1.,  0.,  0.],
           [ 1.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  1.],
           [ 0.,  0., -1.,  0.]])
    >>> matrix_power(q, 2) # = -np.eye(4)
    array([[-1.,  0.,  0.,  0.],
           [ 0., -1.,  0.,  0.],
           [ 0.,  0., -1.,  0.],
           [ 0.,  0.,  0., -1.]])

    """
    a = asanyarray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    try:
        n = operator.index(n)
    except TypeError as e:
        try:
            raise TypeError('exponent must be an integer') from e
        finally:
            e = None
            del e

    if a.dtype != object:
        fmatmul = matmul
    else:
        if a.ndim == 2:
            fmatmul = dot
        else:
            raise NotImplementedError('matrix_power not supported for stacks of object arrays')
    if n == 0:
        a = empty_like(a)
        a[...] = eye((a.shape[(-2)]), dtype=(a.dtype))
        return a
    if n < 0:
        a = inv(a)
        n = abs(n)
    if n == 1:
        return a
    if n == 2:
        return fmatmul(a, a)
    if n == 3:
        return fmatmul(fmatmul(a, a), a)
    z = result = None
    while n > 0:
        z = a if z is None else fmatmul(z, z)
        n, bit = divmod(n, 2)
        if bit:
            result = z if result is None else fmatmul(result, z)

    return result


@array_function_dispatch(_unary_dispatcher)
def cholesky(a):
    r"""
    Cholesky decomposition.

    Return the Cholesky decomposition, `L * L.H`, of the square matrix `a`,
    where `L` is lower-triangular and .H is the conjugate transpose operator
    (which is the ordinary transpose if `a` is real-valued).  `a` must be
    Hermitian (symmetric if real-valued) and positive-definite. No
    checking is performed to verify whether `a` is Hermitian or not.
    In addition, only the lower-triangular and diagonal elements of `a`
    are used. Only `L` is actually returned.

    Parameters
    ----------
    a : (..., M, M) array_like
        Hermitian (symmetric if all elements are real), positive-definite
        input matrix.

    Returns
    -------
    L : (..., M, M) array_like
        Upper or lower-triangular Cholesky factor of `a`.  Returns a
        matrix object if `a` is a matrix object.

    Raises
    ------
    LinAlgError
       If the decomposition fails, for example, if `a` is not
       positive-definite.

    See Also
    --------
    scipy.linalg.cholesky : Similar function in SciPy.
    scipy.linalg.cholesky_banded : Cholesky decompose a banded Hermitian
                                   positive-definite matrix.
    scipy.linalg.cho_factor : Cholesky decomposition of a matrix, to use in
                              `scipy.linalg.cho_solve`.

    Notes
    -----

    .. versionadded:: 1.8.0

    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The Cholesky decomposition is often used as a fast way of solving

    .. math:: A \mathbf{x} = \mathbf{b}

    (when `A` is both Hermitian/symmetric and positive-definite).

    First, we solve for :math:`\mathbf{y}` in

    .. math:: L \mathbf{y} = \mathbf{b},

    and then for :math:`\mathbf{x}` in

    .. math:: L.H \mathbf{x} = \mathbf{y}.

    Examples
    --------
    >>> A = np.array([[1,-2j],[2j,5]])
    >>> A
    array([[ 1.+0.j, -0.-2.j],
           [ 0.+2.j,  5.+0.j]])
    >>> L = np.linalg.cholesky(A)
    >>> L
    array([[1.+0.j, 0.+0.j],
           [0.+2.j, 1.+0.j]])
    >>> np.dot(L, L.T.conj()) # verify that L * L.H = A
    array([[1.+0.j, 0.-2.j],
           [0.+2.j, 5.+0.j]])
    >>> A = [[1,-2j],[2j,5]] # what happens if A is only array_like?
    >>> np.linalg.cholesky(A) # an ndarray object is returned
    array([[1.+0.j, 0.+0.j],
           [0.+2.j, 1.+0.j]])
    >>> # But a matrix object is returned if A is a matrix object
    >>> np.linalg.cholesky(np.matrix(A))
    matrix([[ 1.+0.j,  0.+0.j],
            [ 0.+2.j,  1.+0.j]])

    """
    extobj = get_linalg_error_extobj(_raise_linalgerror_nonposdef)
    gufunc = _umath_linalg.cholesky_lo
    a, wrap = _makearray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)
    signature = 'D->D' if isComplexType(t) else 'd->d'
    r = gufunc(a, signature=signature, extobj=extobj)
    return wrap(r.astype(result_t, copy=False))


def _qr_dispatcher(a, mode=None):
    return (
     a,)


@array_function_dispatch(_qr_dispatcher)
def qr(a, mode='reduced'):
    """
    Compute the qr factorization of a matrix.

    Factor the matrix `a` as *qr*, where `q` is orthonormal and `r` is
    upper-triangular.

    Parameters
    ----------
    a : array_like, shape (M, N)
        Matrix to be factored.
    mode : {'reduced', 'complete', 'r', 'raw'}, optional
        If K = min(M, N), then

        * 'reduced'  : returns q, r with dimensions (M, K), (K, N) (default)
        * 'complete' : returns q, r with dimensions (M, M), (M, N)
        * 'r'        : returns r only with dimensions (K, N)
        * 'raw'      : returns h, tau with dimensions (N, M), (K,)

        The options 'reduced', 'complete, and 'raw' are new in numpy 1.8,
        see the notes for more information. The default is 'reduced', and to
        maintain backward compatibility with earlier versions of numpy both
        it and the old default 'full' can be omitted. Note that array h
        returned in 'raw' mode is transposed for calling Fortran. The
        'economic' mode is deprecated.  The modes 'full' and 'economic' may
        be passed using only the first letter for backwards compatibility,
        but all others must be spelled out. See the Notes for more
        explanation.

    Returns
    -------
    q : ndarray of float or complex, optional
        A matrix with orthonormal columns. When mode = 'complete' the
        result is an orthogonal/unitary matrix depending on whether or not
        a is real/complex. The determinant may be either +/- 1 in that
        case.
    r : ndarray of float or complex, optional
        The upper-triangular matrix.
    (h, tau) : ndarrays of np.double or np.cdouble, optional
        The array h contains the Householder reflectors that generate q
        along with r. The tau array contains scaling factors for the
        reflectors. In the deprecated  'economic' mode only h is returned.

    Raises
    ------
    LinAlgError
        If factoring fails.

    See Also
    --------
    scipy.linalg.qr : Similar function in SciPy.
    scipy.linalg.rq : Compute RQ decomposition of a matrix.

    Notes
    -----
    This is an interface to the LAPACK routines ``dgeqrf``, ``zgeqrf``,
    ``dorgqr``, and ``zungqr``.

    For more information on the qr factorization, see for example:
    https://en.wikipedia.org/wiki/QR_factorization

    Subclasses of `ndarray` are preserved except for the 'raw' mode. So if
    `a` is of type `matrix`, all the return values will be matrices too.

    New 'reduced', 'complete', and 'raw' options for mode were added in
    NumPy 1.8.0 and the old option 'full' was made an alias of 'reduced'.  In
    addition the options 'full' and 'economic' were deprecated.  Because
    'full' was the previous default and 'reduced' is the new default,
    backward compatibility can be maintained by letting `mode` default.
    The 'raw' option was added so that LAPACK routines that can multiply
    arrays by q using the Householder reflectors can be used. Note that in
    this case the returned arrays are of type np.double or np.cdouble and
    the h array is transposed to be FORTRAN compatible.  No routines using
    the 'raw' return are currently exposed by numpy, but some are available
    in lapack_lite and just await the necessary work.

    Examples
    --------
    >>> a = np.random.randn(9, 6)
    >>> q, r = np.linalg.qr(a)
    >>> np.allclose(a, np.dot(q, r))  # a does equal qr
    True
    >>> r2 = np.linalg.qr(a, mode='r')
    >>> np.allclose(r, r2)  # mode='r' returns the same r as mode='full'
    True

    Example illustrating a common use of `qr`: solving of least squares
    problems

    What are the least-squares-best `m` and `y0` in ``y = y0 + mx`` for
    the following data: {(0,1), (1,0), (1,2), (2,1)}. (Graph the points
    and you'll see that it should be y0 = 0, m = 1.)  The answer is provided
    by solving the over-determined matrix equation ``Ax = b``, where::

      A = array([[0, 1], [1, 1], [1, 1], [2, 1]])
      x = array([[y0], [m]])
      b = array([[1], [0], [2], [1]])

    If A = qr such that q is orthonormal (which is always possible via
    Gram-Schmidt), then ``x = inv(r) * (q.T) * b``.  (In numpy practice,
    however, we simply use `lstsq`.)

    >>> A = np.array([[0, 1], [1, 1], [1, 1], [2, 1]])
    >>> A
    array([[0, 1],
           [1, 1],
           [1, 1],
           [2, 1]])
    >>> b = np.array([1, 0, 2, 1])
    >>> q, r = np.linalg.qr(A)
    >>> p = np.dot(q.T, b)
    >>> np.dot(np.linalg.inv(r), p)
    array([  1.1e-16,   1.0e+00])

    """
    if mode not in ('reduced', 'complete', 'r', 'raw'):
        if mode in ('f', 'full'):
            msg = ''.join(("The 'full' option is deprecated in favor of 'reduced'.\n",
                           'For backward compatibility let mode default.'))
            warnings.warn(msg, DeprecationWarning, stacklevel=3)
            mode = 'reduced'
        else:
            if mode in ('e', 'economic'):
                msg = "The 'economic' option is deprecated."
                warnings.warn(msg, DeprecationWarning, stacklevel=3)
                mode = 'economic'
            else:
                raise ValueError("Unrecognized mode '%s'" % mode)
    else:
        a, wrap = _makearray(a)
        _assert_2d(a)
        m, n = a.shape
        t, result_t = _commonType(a)
        a = _fastCopyAndTranspose(t, a)
        a = _to_native_byte_order(a)
        mn = min(m, n)
        tau = zeros((mn,), t)
        if isComplexType(t):
            lapack_routine = lapack_lite.zgeqrf
            routine_name = 'zgeqrf'
        else:
            lapack_routine = lapack_lite.dgeqrf
            routine_name = 'dgeqrf'
        lwork = 1
        work = zeros((lwork,), t)
        results = lapack_routine(m, n, a, max(1, m), tau, work, -1, 0)
        if results['info'] != 0:
            raise LinAlgError('%s returns %d' % (routine_name, results['info']))
        lwork = max(1, n, int(abs(work[0])))
        work = zeros((lwork,), t)
        results = lapack_routine(m, n, a, max(1, m), tau, work, lwork, 0)
        if results['info'] != 0:
            raise LinAlgError('%s returns %d' % (routine_name, results['info']))
        if mode == 'r':
            r = _fastCopyAndTranspose(result_t, a[:, :mn])
            return wrap(triu(r))
        if mode == 'raw':
            return (
             a, tau)
        if mode == 'economic':
            if t != result_t:
                a = a.astype(result_t, copy=False)
            return wrap(a.T)
        if mode == 'complete':
            if m > n:
                mc = m
                q = empty((m, m), t)
            else:
                mc = mn
                q = empty((n, m), t)
            q[:n] = a
            if isComplexType(t):
                lapack_routine = lapack_lite.zungqr
                routine_name = 'zungqr'
        else:
            lapack_routine = lapack_lite.dorgqr
        routine_name = 'dorgqr'
    lwork = 1
    work = zeros((lwork,), t)
    results = lapack_routine(m, mc, mn, q, max(1, m), tau, work, -1, 0)
    if results['info'] != 0:
        raise LinAlgError('%s returns %d' % (routine_name, results['info']))
    lwork = max(1, n, int(abs(work[0])))
    work = zeros((lwork,), t)
    results = lapack_routine(m, mc, mn, q, max(1, m), tau, work, lwork, 0)
    if results['info'] != 0:
        raise LinAlgError('%s returns %d' % (routine_name, results['info']))
    q = _fastCopyAndTranspose(result_t, q[:mc])
    r = _fastCopyAndTranspose(result_t, a[:, :mc])
    return (
     wrap(q), wrap(triu(r)))


@array_function_dispatch(_unary_dispatcher)
def eigvals(a):
    """
    Compute the eigenvalues of a general matrix.

    Main difference between `eigvals` and `eig`: the eigenvectors aren't
    returned.

    Parameters
    ----------
    a : (..., M, M) array_like
        A complex- or real-valued matrix whose eigenvalues will be computed.

    Returns
    -------
    w : (..., M,) ndarray
        The eigenvalues, each repeated according to its multiplicity.
        They are not necessarily ordered, nor are they necessarily
        real for real matrices.

    Raises
    ------
    LinAlgError
        If the eigenvalue computation does not converge.

    See Also
    --------
    eig : eigenvalues and right eigenvectors of general arrays
    eigvalsh : eigenvalues of real symmetric or complex Hermitian
               (conjugate symmetric) arrays.
    eigh : eigenvalues and eigenvectors of real symmetric or complex
           Hermitian (conjugate symmetric) arrays.
    scipy.linalg.eigvals : Similar function in SciPy.

    Notes
    -----

    .. versionadded:: 1.8.0

    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    This is implemented using the ``_geev`` LAPACK routines which compute
    the eigenvalues and eigenvectors of general square arrays.

    Examples
    --------
    Illustration, using the fact that the eigenvalues of a diagonal matrix
    are its diagonal elements, that multiplying a matrix on the left
    by an orthogonal matrix, `Q`, and on the right by `Q.T` (the transpose
    of `Q`), preserves the eigenvalues of the "middle" matrix.  In other words,
    if `Q` is orthogonal, then ``Q * A * Q.T`` has the same eigenvalues as
    ``A``:

    >>> from numpy import linalg as LA
    >>> x = np.random.random()
    >>> Q = np.array([[np.cos(x), -np.sin(x)], [np.sin(x), np.cos(x)]])
    >>> LA.norm(Q[0, :]), LA.norm(Q[1, :]), np.dot(Q[0, :],Q[1, :])
    (1.0, 1.0, 0.0)

    Now multiply a diagonal matrix by ``Q`` on one side and by ``Q.T`` on the other:

    >>> D = np.diag((-1,1))
    >>> LA.eigvals(D)
    array([-1.,  1.])
    >>> A = np.dot(Q, D)
    >>> A = np.dot(A, Q.T)
    >>> LA.eigvals(A)
    array([ 1., -1.]) # random

    """
    a, wrap = _makearray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    _assert_finite(a)
    t, result_t = _commonType(a)
    extobj = get_linalg_error_extobj(_raise_linalgerror_eigenvalues_nonconvergence)
    signature = 'D->D' if isComplexType(t) else 'd->D'
    w = _umath_linalg.eigvals(a, signature=signature, extobj=extobj)
    if not isComplexType(t):
        if all(w.imag == 0):
            w = w.real
            result_t = _realType(result_t)
        else:
            result_t = _complexType(result_t)
    return w.astype(result_t, copy=False)


def _eigvalsh_dispatcher(a, UPLO=None):
    return (
     a,)


@array_function_dispatch(_eigvalsh_dispatcher)
def eigvalsh(a, UPLO='L'):
    """
    Compute the eigenvalues of a complex Hermitian or real symmetric matrix.

    Main difference from eigh: the eigenvectors are not computed.

    Parameters
    ----------
    a : (..., M, M) array_like
        A complex- or real-valued matrix whose eigenvalues are to be
        computed.
    UPLO : {'L', 'U'}, optional
        Specifies whether the calculation is done with the lower triangular
        part of `a` ('L', default) or the upper triangular part ('U').
        Irrespective of this value only the real parts of the diagonal will
        be considered in the computation to preserve the notion of a Hermitian
        matrix. It therefore follows that the imaginary part of the diagonal
        will always be treated as zero.

    Returns
    -------
    w : (..., M,) ndarray
        The eigenvalues in ascending order, each repeated according to
        its multiplicity.

    Raises
    ------
    LinAlgError
        If the eigenvalue computation does not converge.

    See Also
    --------
    eigh : eigenvalues and eigenvectors of real symmetric or complex Hermitian
           (conjugate symmetric) arrays.
    eigvals : eigenvalues of general real or complex arrays.
    eig : eigenvalues and right eigenvectors of general real or complex
          arrays.
    scipy.linalg.eigvalsh : Similar function in SciPy.

    Notes
    -----

    .. versionadded:: 1.8.0

    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The eigenvalues are computed using LAPACK routines ``_syevd``, ``_heevd``.

    Examples
    --------
    >>> from numpy import linalg as LA
    >>> a = np.array([[1, -2j], [2j, 5]])
    >>> LA.eigvalsh(a)
    array([ 0.17157288,  5.82842712]) # may vary

    >>> # demonstrate the treatment of the imaginary part of the diagonal
    >>> a = np.array([[5+2j, 9-2j], [0+2j, 2-1j]])
    >>> a
    array([[5.+2.j, 9.-2.j],
           [0.+2.j, 2.-1.j]])
    >>> # with UPLO='L' this is numerically equivalent to using LA.eigvals()
    >>> # with:
    >>> b = np.array([[5.+0.j, 0.-2.j], [0.+2.j, 2.-0.j]])
    >>> b
    array([[5.+0.j, 0.-2.j],
           [0.+2.j, 2.+0.j]])
    >>> wa = LA.eigvalsh(a)
    >>> wb = LA.eigvals(b)
    >>> wa; wb
    array([1., 6.])
    array([6.+0.j, 1.+0.j])

    """
    UPLO = UPLO.upper()
    if UPLO not in ('L', 'U'):
        raise ValueError("UPLO argument must be 'L' or 'U'")
    else:
        extobj = get_linalg_error_extobj(_raise_linalgerror_eigenvalues_nonconvergence)
        if UPLO == 'L':
            gufunc = _umath_linalg.eigvalsh_lo
        else:
            gufunc = _umath_linalg.eigvalsh_up
    a, wrap = _makearray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)
    signature = 'D->d' if isComplexType(t) else 'd->d'
    w = gufunc(a, signature=signature, extobj=extobj)
    return w.astype((_realType(result_t)), copy=False)


def _convertarray(a):
    t, result_t = _commonType(a)
    a = _fastCT(a.astype(t))
    return (a, t, result_t)


@array_function_dispatch(_unary_dispatcher)
def eig(a):
    r"""
    Compute the eigenvalues and right eigenvectors of a square array.

    Parameters
    ----------
    a : (..., M, M) array
        Matrices for which the eigenvalues and right eigenvectors will
        be computed

    Returns
    -------
    w : (..., M) array
        The eigenvalues, each repeated according to its multiplicity.
        The eigenvalues are not necessarily ordered. The resulting
        array will be of complex type, unless the imaginary part is
        zero in which case it will be cast to a real type. When `a`
        is real the resulting eigenvalues will be real (0 imaginary
        part) or occur in conjugate pairs

    v : (..., M, M) array
        The normalized (unit "length") eigenvectors, such that the
        column ``v[:,i]`` is the eigenvector corresponding to the
        eigenvalue ``w[i]``.

    Raises
    ------
    LinAlgError
        If the eigenvalue computation does not converge.

    See Also
    --------
    eigvals : eigenvalues of a non-symmetric array.
    eigh : eigenvalues and eigenvectors of a real symmetric or complex
           Hermitian (conjugate symmetric) array.
    eigvalsh : eigenvalues of a real symmetric or complex Hermitian
               (conjugate symmetric) array.
    scipy.linalg.eig : Similar function in SciPy that also solves the
                       generalized eigenvalue problem.
    scipy.linalg.schur : Best choice for unitary and other non-Hermitian
                         normal matrices.

    Notes
    -----

    .. versionadded:: 1.8.0

    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    This is implemented using the ``_geev`` LAPACK routines which compute
    the eigenvalues and eigenvectors of general square arrays.

    The number `w` is an eigenvalue of `a` if there exists a vector
    `v` such that ``a @ v = w * v``. Thus, the arrays `a`, `w`, and
    `v` satisfy the equations ``a @ v[:,i] = w[i] * v[:,i]``
    for :math:`i \in \{0,...,M-1\}`.

    The array `v` of eigenvectors may not be of maximum rank, that is, some
    of the columns may be linearly dependent, although round-off error may
    obscure that fact. If the eigenvalues are all different, then theoretically
    the eigenvectors are linearly independent and `a` can be diagonalized by
    a similarity transformation using `v`, i.e, ``inv(v) @ a @ v`` is diagonal.

    For non-Hermitian normal matrices the SciPy function `scipy.linalg.schur`
    is preferred because the matrix `v` is guaranteed to be unitary, which is
    not the case when using `eig`. The Schur factorization produces an
    upper triangular matrix rather than a diagonal matrix, but for normal
    matrices only the diagonal of the upper triangular matrix is needed, the
    rest is roundoff error.

    Finally, it is emphasized that `v` consists of the *right* (as in
    right-hand side) eigenvectors of `a`.  A vector `y` satisfying
    ``y.T @ a = z * y.T`` for some number `z` is called a *left*
    eigenvector of `a`, and, in general, the left and right eigenvectors
    of a matrix are not necessarily the (perhaps conjugate) transposes
    of each other.

    References
    ----------
    G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando, FL,
    Academic Press, Inc., 1980, Various pp.

    Examples
    --------
    >>> from numpy import linalg as LA

    (Almost) trivial example with real e-values and e-vectors.

    >>> w, v = LA.eig(np.diag((1, 2, 3)))
    >>> w; v
    array([1., 2., 3.])
    array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])

    Real matrix possessing complex e-values and e-vectors; note that the
    e-values are complex conjugates of each other.

    >>> w, v = LA.eig(np.array([[1, -1], [1, 1]]))
    >>> w; v
    array([1.+1.j, 1.-1.j])
    array([[0.70710678+0.j        , 0.70710678-0.j        ],
           [0.        -0.70710678j, 0.        +0.70710678j]])

    Complex-valued matrix with real e-values (but complex-valued e-vectors);
    note that ``a.conj().T == a``, i.e., `a` is Hermitian.

    >>> a = np.array([[1, 1j], [-1j, 1]])
    >>> w, v = LA.eig(a)
    >>> w; v
    array([2.+0.j, 0.+0.j])
    array([[ 0.        +0.70710678j,  0.70710678+0.j        ], # may vary
           [ 0.70710678+0.j        , -0.        +0.70710678j]])

    Be careful about round-off error!

    >>> a = np.array([[1 + 1e-9, 0], [0, 1 - 1e-9]])
    >>> # Theor. e-values are 1 +/- 1e-9
    >>> w, v = LA.eig(a)
    >>> w; v
    array([1., 1.])
    array([[1., 0.],
           [0., 1.]])

    """
    a, wrap = _makearray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    _assert_finite(a)
    t, result_t = _commonType(a)
    extobj = get_linalg_error_extobj(_raise_linalgerror_eigenvalues_nonconvergence)
    signature = 'D->DD' if isComplexType(t) else 'd->DD'
    w, vt = _umath_linalg.eig(a, signature=signature, extobj=extobj)
    if isComplexType(t) or all(w.imag == 0.0):
        w = w.real
        vt = vt.real
        result_t = _realType(result_t)
    else:
        result_t = _complexType(result_t)
    vt = vt.astype(result_t, copy=False)
    return (w.astype(result_t, copy=False), wrap(vt))


@array_function_dispatch(_eigvalsh_dispatcher)
def eigh(a, UPLO='L'):
    """
    Return the eigenvalues and eigenvectors of a complex Hermitian
    (conjugate symmetric) or a real symmetric matrix.

    Returns two objects, a 1-D array containing the eigenvalues of `a`, and
    a 2-D square array or matrix (depending on the input type) of the
    corresponding eigenvectors (in columns).

    Parameters
    ----------
    a : (..., M, M) array
        Hermitian or real symmetric matrices whose eigenvalues and
        eigenvectors are to be computed.
    UPLO : {'L', 'U'}, optional
        Specifies whether the calculation is done with the lower triangular
        part of `a` ('L', default) or the upper triangular part ('U').
        Irrespective of this value only the real parts of the diagonal will
        be considered in the computation to preserve the notion of a Hermitian
        matrix. It therefore follows that the imaginary part of the diagonal
        will always be treated as zero.

    Returns
    -------
    w : (..., M) ndarray
        The eigenvalues in ascending order, each repeated according to
        its multiplicity.
    v : {(..., M, M) ndarray, (..., M, M) matrix}
        The column ``v[:, i]`` is the normalized eigenvector corresponding
        to the eigenvalue ``w[i]``.  Will return a matrix object if `a` is
        a matrix object.

    Raises
    ------
    LinAlgError
        If the eigenvalue computation does not converge.

    See Also
    --------
    eigvalsh : eigenvalues of real symmetric or complex Hermitian
               (conjugate symmetric) arrays.
    eig : eigenvalues and right eigenvectors for non-symmetric arrays.
    eigvals : eigenvalues of non-symmetric arrays.
    scipy.linalg.eigh : Similar function in SciPy (but also solves the
                        generalized eigenvalue problem).

    Notes
    -----

    .. versionadded:: 1.8.0

    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The eigenvalues/eigenvectors are computed using LAPACK routines ``_syevd``,
    ``_heevd``.

    The eigenvalues of real symmetric or complex Hermitian matrices are
    always real. [1]_ The array `v` of (column) eigenvectors is unitary
    and `a`, `w`, and `v` satisfy the equations
    ``dot(a, v[:, i]) = w[i] * v[:, i]``.

    References
    ----------
    .. [1] G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando,
           FL, Academic Press, Inc., 1980, pg. 222.

    Examples
    --------
    >>> from numpy import linalg as LA
    >>> a = np.array([[1, -2j], [2j, 5]])
    >>> a
    array([[ 1.+0.j, -0.-2.j],
           [ 0.+2.j,  5.+0.j]])
    >>> w, v = LA.eigh(a)
    >>> w; v
    array([0.17157288, 5.82842712])
    array([[-0.92387953+0.j        , -0.38268343+0.j        ], # may vary
           [ 0.        +0.38268343j,  0.        -0.92387953j]])

    >>> np.dot(a, v[:, 0]) - w[0] * v[:, 0] # verify 1st e-val/vec pair
    array([5.55111512e-17+0.0000000e+00j, 0.00000000e+00+1.2490009e-16j])
    >>> np.dot(a, v[:, 1]) - w[1] * v[:, 1] # verify 2nd e-val/vec pair
    array([0.+0.j, 0.+0.j])

    >>> A = np.matrix(a) # what happens if input is a matrix object
    >>> A
    matrix([[ 1.+0.j, -0.-2.j],
            [ 0.+2.j,  5.+0.j]])
    >>> w, v = LA.eigh(A)
    >>> w; v
    array([0.17157288, 5.82842712])
    matrix([[-0.92387953+0.j        , -0.38268343+0.j        ], # may vary
            [ 0.        +0.38268343j,  0.        -0.92387953j]])

    >>> # demonstrate the treatment of the imaginary part of the diagonal
    >>> a = np.array([[5+2j, 9-2j], [0+2j, 2-1j]])
    >>> a
    array([[5.+2.j, 9.-2.j],
           [0.+2.j, 2.-1.j]])
    >>> # with UPLO='L' this is numerically equivalent to using LA.eig() with:
    >>> b = np.array([[5.+0.j, 0.-2.j], [0.+2.j, 2.-0.j]])
    >>> b
    array([[5.+0.j, 0.-2.j],
           [0.+2.j, 2.+0.j]])
    >>> wa, va = LA.eigh(a)
    >>> wb, vb = LA.eig(b)
    >>> wa; wb
    array([1., 6.])
    array([6.+0.j, 1.+0.j])
    >>> va; vb
    array([[-0.4472136 +0.j        , -0.89442719+0.j        ], # may vary
           [ 0.        +0.89442719j,  0.        -0.4472136j ]])
    array([[ 0.89442719+0.j       , -0.        +0.4472136j],
           [-0.        +0.4472136j,  0.89442719+0.j       ]])
    """
    UPLO = UPLO.upper()
    if UPLO not in ('L', 'U'):
        raise ValueError("UPLO argument must be 'L' or 'U'")
    else:
        a, wrap = _makearray(a)
        _assert_stacked_2d(a)
        _assert_stacked_square(a)
        t, result_t = _commonType(a)
        extobj = get_linalg_error_extobj(_raise_linalgerror_eigenvalues_nonconvergence)
        if UPLO == 'L':
            gufunc = _umath_linalg.eigh_lo
        else:
            gufunc = _umath_linalg.eigh_up
    signature = 'D->dD' if isComplexType(t) else 'd->dd'
    w, vt = gufunc(a, signature=signature, extobj=extobj)
    w = w.astype((_realType(result_t)), copy=False)
    vt = vt.astype(result_t, copy=False)
    return (w, wrap(vt))


def _svd_dispatcher(a, full_matrices=None, compute_uv=None, hermitian=None):
    return (
     a,)


@array_function_dispatch(_svd_dispatcher)
def svd(a, full_matrices=True, compute_uv=True, hermitian=False):
    r"""
    Singular Value Decomposition.

    When `a` is a 2D array, it is factorized as ``u @ np.diag(s) @ vh
    = (u * s) @ vh``, where `u` and `vh` are 2D unitary arrays and `s` is a 1D
    array of `a`'s singular values. When `a` is higher-dimensional, SVD is
    applied in stacked mode as explained below.

    Parameters
    ----------
    a : (..., M, N) array_like
        A real or complex array with ``a.ndim >= 2``.
    full_matrices : bool, optional
        If True (default), `u` and `vh` have the shapes ``(..., M, M)`` and
        ``(..., N, N)``, respectively.  Otherwise, the shapes are
        ``(..., M, K)`` and ``(..., K, N)``, respectively, where
        ``K = min(M, N)``.
    compute_uv : bool, optional
        Whether or not to compute `u` and `vh` in addition to `s`.  True
        by default.
    hermitian : bool, optional
        If True, `a` is assumed to be Hermitian (symmetric if real-valued),
        enabling a more efficient method for finding singular values.
        Defaults to False.

        .. versionadded:: 1.17.0

    Returns
    -------
    u : { (..., M, M), (..., M, K) } array
        Unitary array(s). The first ``a.ndim - 2`` dimensions have the same
        size as those of the input `a`. The size of the last two dimensions
        depends on the value of `full_matrices`. Only returned when
        `compute_uv` is True.
    s : (..., K) array
        Vector(s) with the singular values, within each vector sorted in
        descending order. The first ``a.ndim - 2`` dimensions have the same
        size as those of the input `a`.
    vh : { (..., N, N), (..., K, N) } array
        Unitary array(s). The first ``a.ndim - 2`` dimensions have the same
        size as those of the input `a`. The size of the last two dimensions
        depends on the value of `full_matrices`. Only returned when
        `compute_uv` is True.

    Raises
    ------
    LinAlgError
        If SVD computation does not converge.

    See Also
    --------
    scipy.linalg.svd : Similar function in SciPy.
    scipy.linalg.svdvals : Compute singular values of a matrix.

    Notes
    -----

    .. versionchanged:: 1.8.0
       Broadcasting rules apply, see the `numpy.linalg` documentation for
       details.

    The decomposition is performed using LAPACK routine ``_gesdd``.

    SVD is usually described for the factorization of a 2D matrix :math:`A`.
    The higher-dimensional case will be discussed below. In the 2D case, SVD is
    written as :math:`A = U S V^H`, where :math:`A = a`, :math:`U= u`,
    :math:`S= \mathtt{np.diag}(s)` and :math:`V^H = vh`. The 1D array `s`
    contains the singular values of `a` and `u` and `vh` are unitary. The rows
    of `vh` are the eigenvectors of :math:`A^H A` and the columns of `u` are
    the eigenvectors of :math:`A A^H`. In both cases the corresponding
    (possibly non-zero) eigenvalues are given by ``s**2``.

    If `a` has more than two dimensions, then broadcasting rules apply, as
    explained in :ref:`routines.linalg-broadcasting`. This means that SVD is
    working in "stacked" mode: it iterates over all indices of the first
    ``a.ndim - 2`` dimensions and for each combination SVD is applied to the
    last two indices. The matrix `a` can be reconstructed from the
    decomposition with either ``(u * s[..., None, :]) @ vh`` or
    ``u @ (s[..., None] * vh)``. (The ``@`` operator can be replaced by the
    function ``np.matmul`` for python versions below 3.5.)

    If `a` is a ``matrix`` object (as opposed to an ``ndarray``), then so are
    all the return values.

    Examples
    --------
    >>> a = np.random.randn(9, 6) + 1j*np.random.randn(9, 6)
    >>> b = np.random.randn(2, 7, 8, 3) + 1j*np.random.randn(2, 7, 8, 3)

    Reconstruction based on full SVD, 2D case:

    >>> u, s, vh = np.linalg.svd(a, full_matrices=True)
    >>> u.shape, s.shape, vh.shape
    ((9, 9), (6,), (6, 6))
    >>> np.allclose(a, np.dot(u[:, :6] * s, vh))
    True
    >>> smat = np.zeros((9, 6), dtype=complex)
    >>> smat[:6, :6] = np.diag(s)
    >>> np.allclose(a, np.dot(u, np.dot(smat, vh)))
    True

    Reconstruction based on reduced SVD, 2D case:

    >>> u, s, vh = np.linalg.svd(a, full_matrices=False)
    >>> u.shape, s.shape, vh.shape
    ((9, 6), (6,), (6, 6))
    >>> np.allclose(a, np.dot(u * s, vh))
    True
    >>> smat = np.diag(s)
    >>> np.allclose(a, np.dot(u, np.dot(smat, vh)))
    True

    Reconstruction based on full SVD, 4D case:

    >>> u, s, vh = np.linalg.svd(b, full_matrices=True)
    >>> u.shape, s.shape, vh.shape
    ((2, 7, 8, 8), (2, 7, 3), (2, 7, 3, 3))
    >>> np.allclose(b, np.matmul(u[..., :3] * s[..., None, :], vh))
    True
    >>> np.allclose(b, np.matmul(u[..., :3], s[..., None] * vh))
    True

    Reconstruction based on reduced SVD, 4D case:

    >>> u, s, vh = np.linalg.svd(b, full_matrices=False)
    >>> u.shape, s.shape, vh.shape
    ((2, 7, 8, 3), (2, 7, 3), (2, 7, 3, 3))
    >>> np.allclose(b, np.matmul(u * s[..., None, :], vh))
    True
    >>> np.allclose(b, np.matmul(u, s[..., None] * vh))
    True

    """
    import numpy as _nx
    a, wrap = _makearray(a)
    if hermitian:
        if compute_uv:
            s, u = eigh(a)
            sgn = sign(s)
            s = abs(s)
            sidx = argsort(s)[..., ::-1]
            sgn = _nx.take_along_axis(sgn, sidx, axis=(-1))
            s = _nx.take_along_axis(s, sidx, axis=(-1))
            u = _nx.take_along_axis(u, (sidx[..., None, :]), axis=(-1))
            vt = transpose(u * sgn[..., None, :]).conjugate()
            return (wrap(u), s, wrap(vt))
        s = eigvalsh(a)
        s = s[..., ::-1]
        s = abs(s)
        return sort(s)[..., ::-1]
    _assert_stacked_2d(a)
    t, result_t = _commonType(a)
    extobj = get_linalg_error_extobj(_raise_linalgerror_svd_nonconvergence)
    m, n = a.shape[-2:]
    if compute_uv:
        if full_matrices:
            if m < n:
                gufunc = _umath_linalg.svd_m_f
            else:
                gufunc = _umath_linalg.svd_n_f
        elif m < n:
            gufunc = _umath_linalg.svd_m_s
        else:
            gufunc = _umath_linalg.svd_n_s
    else:
        signature = 'D->DdD' if isComplexType(t) else 'd->ddd'
        u, s, vh = gufunc(a, signature=signature, extobj=extobj)
        u = u.astype(result_t, copy=False)
        s = s.astype((_realType(result_t)), copy=False)
        vh = vh.astype(result_t, copy=False)
        return (wrap(u), s, wrap(vh))
        if m < n:
            gufunc = _umath_linalg.svd_m
        else:
            gufunc = _umath_linalg.svd_n
    signature = 'D->d' if isComplexType(t) else 'd->d'
    s = gufunc(a, signature=signature, extobj=extobj)
    s = s.astype((_realType(result_t)), copy=False)
    return s


def _cond_dispatcher(x, p=None):
    return (
     x,)


@array_function_dispatch(_cond_dispatcher)
def cond(x, p=None):
    """
    Compute the condition number of a matrix.

    This function is capable of returning the condition number using
    one of seven different norms, depending on the value of `p` (see
    Parameters below).

    Parameters
    ----------
    x : (..., M, N) array_like
        The matrix whose condition number is sought.
    p : {None, 1, -1, 2, -2, inf, -inf, 'fro'}, optional
        Order of the norm:

        =====  ============================
        p      norm for matrices
        =====  ============================
        None   2-norm, computed directly using the ``SVD``
        'fro'  Frobenius norm
        inf    max(sum(abs(x), axis=1))
        -inf   min(sum(abs(x), axis=1))
        1      max(sum(abs(x), axis=0))
        -1     min(sum(abs(x), axis=0))
        2      2-norm (largest sing. value)
        -2     smallest singular value
        =====  ============================

        inf means the numpy.inf object, and the Frobenius norm is
        the root-of-sum-of-squares norm.

    Returns
    -------
    c : {float, inf}
        The condition number of the matrix. May be infinite.

    See Also
    --------
    numpy.linalg.norm

    Notes
    -----
    The condition number of `x` is defined as the norm of `x` times the
    norm of the inverse of `x` [1]_; the norm can be the usual L2-norm
    (root-of-sum-of-squares) or one of a number of other matrix norms.

    References
    ----------
    .. [1] G. Strang, *Linear Algebra and Its Applications*, Orlando, FL,
           Academic Press, Inc., 1980, pg. 285.

    Examples
    --------
    >>> from numpy import linalg as LA
    >>> a = np.array([[1, 0, -1], [0, 1, 0], [1, 0, 1]])
    >>> a
    array([[ 1,  0, -1],
           [ 0,  1,  0],
           [ 1,  0,  1]])
    >>> LA.cond(a)
    1.4142135623730951
    >>> LA.cond(a, 'fro')
    3.1622776601683795
    >>> LA.cond(a, np.inf)
    2.0
    >>> LA.cond(a, -np.inf)
    1.0
    >>> LA.cond(a, 1)
    2.0
    >>> LA.cond(a, -1)
    1.0
    >>> LA.cond(a, 2)
    1.4142135623730951
    >>> LA.cond(a, -2)
    0.70710678118654746 # may vary
    >>> min(LA.svd(a, compute_uv=False))*min(LA.svd(LA.inv(a), compute_uv=False))
    0.70710678118654746 # may vary

    """
    x = asarray(x)
    if _is_empty_2d(x):
        raise LinAlgError('cond is not defined on empty arrays')
    if not p is None:
        if p == 2 or p == -2:
            s = svd(x, compute_uv=False)
            with errstate(all='ignore'):
                if p == -2:
                    r = s[(Ellipsis, -1)] / s[(Ellipsis, 0)]
                else:
                    r = s[(Ellipsis, 0)] / s[(Ellipsis, -1)]
    else:
        _assert_stacked_2d(x)
        _assert_stacked_square(x)
        t, result_t = _commonType(x)
        signature = 'D->D' if isComplexType(t) else 'd->d'
        with errstate(all='ignore'):
            invx = _umath_linalg.inv(x, signature=signature)
            r = norm(x, p, axis=(-2, -1)) * norm(invx, p, axis=(-2, -1))
        r = r.astype(result_t, copy=False)
    r = asarray(r)
    nan_mask = isnan(r)
    if nan_mask.any():
        nan_mask &= ~isnan(x).any(axis=(-2, -1))
        if r.ndim > 0:
            r[nan_mask] = Inf
        else:
            if nan_mask:
                r[()] = Inf
    if r.ndim == 0:
        r = r[()]
    return r


def _matrix_rank_dispatcher(M, tol=None, hermitian=None):
    return (
     M,)


@array_function_dispatch(_matrix_rank_dispatcher)
def matrix_rank(M, tol=None, hermitian=False):
    """
    Return matrix rank of array using SVD method

    Rank of the array is the number of singular values of the array that are
    greater than `tol`.

    .. versionchanged:: 1.14
       Can now operate on stacks of matrices

    Parameters
    ----------
    M : {(M,), (..., M, N)} array_like
        Input vector or stack of matrices.
    tol : (...) array_like, float, optional
        Threshold below which SVD values are considered zero. If `tol` is
        None, and ``S`` is an array with singular values for `M`, and
        ``eps`` is the epsilon value for datatype of ``S``, then `tol` is
        set to ``S.max() * max(M.shape) * eps``.

        .. versionchanged:: 1.14
           Broadcasted against the stack of matrices
    hermitian : bool, optional
        If True, `M` is assumed to be Hermitian (symmetric if real-valued),
        enabling a more efficient method for finding singular values.
        Defaults to False.

        .. versionadded:: 1.14

    Returns
    -------
    rank : (...) array_like
        Rank of M.

    Notes
    -----
    The default threshold to detect rank deficiency is a test on the magnitude
    of the singular values of `M`.  By default, we identify singular values less
    than ``S.max() * max(M.shape) * eps`` as indicating rank deficiency (with
    the symbols defined above). This is the algorithm MATLAB uses [1].  It also
    appears in *Numerical recipes* in the discussion of SVD solutions for linear
    least squares [2].

    This default threshold is designed to detect rank deficiency accounting for
    the numerical errors of the SVD computation.  Imagine that there is a column
    in `M` that is an exact (in floating point) linear combination of other
    columns in `M`. Computing the SVD on `M` will not produce a singular value
    exactly equal to 0 in general: any difference of the smallest SVD value from
    0 will be caused by numerical imprecision in the calculation of the SVD.
    Our threshold for small SVD values takes this numerical imprecision into
    account, and the default threshold will detect such numerical rank
    deficiency.  The threshold may declare a matrix `M` rank deficient even if
    the linear combination of some columns of `M` is not exactly equal to
    another column of `M` but only numerically very close to another column of
    `M`.

    We chose our default threshold because it is in wide use.  Other thresholds
    are possible.  For example, elsewhere in the 2007 edition of *Numerical
    recipes* there is an alternative threshold of ``S.max() *
    np.finfo(M.dtype).eps / 2. * np.sqrt(m + n + 1.)``. The authors describe
    this threshold as being based on "expected roundoff error" (p 71).

    The thresholds above deal with floating point roundoff error in the
    calculation of the SVD.  However, you may have more information about the
    sources of error in `M` that would make you consider other tolerance values
    to detect *effective* rank deficiency.  The most useful measure of the
    tolerance depends on the operations you intend to use on your matrix.  For
    example, if your data come from uncertain measurements with uncertainties
    greater than floating point epsilon, choosing a tolerance near that
    uncertainty may be preferable.  The tolerance may be absolute if the
    uncertainties are absolute rather than relative.

    References
    ----------
    .. [1] MATLAB reference documention, "Rank"
           https://www.mathworks.com/help/techdoc/ref/rank.html
    .. [2] W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery,
           "Numerical Recipes (3rd edition)", Cambridge University Press, 2007,
           page 795.

    Examples
    --------
    >>> from numpy.linalg import matrix_rank
    >>> matrix_rank(np.eye(4)) # Full rank matrix
    4
    >>> I=np.eye(4); I[-1,-1] = 0. # rank deficient matrix
    >>> matrix_rank(I)
    3
    >>> matrix_rank(np.ones((4,))) # 1 dimension - rank 1 unless all 0
    1
    >>> matrix_rank(np.zeros((4,)))
    0
    """
    M = asarray(M)
    if M.ndim < 2:
        return int(not all(M == 0))
    else:
        S = svd(M, compute_uv=False, hermitian=hermitian)
        if tol is None:
            tol = S.max(axis=(-1), keepdims=True) * max(M.shape[-2:]) * finfo(S.dtype).eps
        else:
            tol = asarray(tol)[(..., newaxis)]
    return count_nonzero((S > tol), axis=(-1))


def _pinv_dispatcher(a, rcond=None, hermitian=None):
    return (
     a,)


@array_function_dispatch(_pinv_dispatcher)
def pinv(a, rcond=1e-15, hermitian=False):
    r"""
    Compute the (Moore-Penrose) pseudo-inverse of a matrix.

    Calculate the generalized inverse of a matrix using its
    singular-value decomposition (SVD) and including all
    *large* singular values.

    .. versionchanged:: 1.14
       Can now operate on stacks of matrices

    Parameters
    ----------
    a : (..., M, N) array_like
        Matrix or stack of matrices to be pseudo-inverted.
    rcond : (...) array_like of float
        Cutoff for small singular values.
        Singular values less than or equal to
        ``rcond * largest_singular_value`` are set to zero.
        Broadcasts against the stack of matrices.
    hermitian : bool, optional
        If True, `a` is assumed to be Hermitian (symmetric if real-valued),
        enabling a more efficient method for finding singular values.
        Defaults to False.

        .. versionadded:: 1.17.0

    Returns
    -------
    B : (..., N, M) ndarray
        The pseudo-inverse of `a`. If `a` is a `matrix` instance, then so
        is `B`.

    Raises
    ------
    LinAlgError
        If the SVD computation does not converge.

    See Also
    --------
    scipy.linalg.pinv : Similar function in SciPy.
    scipy.linalg.pinv2 : Similar function in SciPy (SVD-based).
    scipy.linalg.pinvh : Compute the (Moore-Penrose) pseudo-inverse of a
                         Hermitian matrix.

    Notes
    -----
    The pseudo-inverse of a matrix A, denoted :math:`A^+`, is
    defined as: "the matrix that 'solves' [the least-squares problem]
    :math:`Ax = b`," i.e., if :math:`\bar{x}` is said solution, then
    :math:`A^+` is that matrix such that :math:`\bar{x} = A^+b`.

    It can be shown that if :math:`Q_1 \Sigma Q_2^T = A` is the singular
    value decomposition of A, then
    :math:`A^+ = Q_2 \Sigma^+ Q_1^T`, where :math:`Q_{1,2}` are
    orthogonal matrices, :math:`\Sigma` is a diagonal matrix consisting
    of A's so-called singular values, (followed, typically, by
    zeros), and then :math:`\Sigma^+` is simply the diagonal matrix
    consisting of the reciprocals of A's singular values
    (again, followed by zeros). [1]_

    References
    ----------
    .. [1] G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando,
           FL, Academic Press, Inc., 1980, pp. 139-142.

    Examples
    --------
    The following example checks that ``a * a+ * a == a`` and
    ``a+ * a * a+ == a+``:

    >>> a = np.random.randn(9, 6)
    >>> B = np.linalg.pinv(a)
    >>> np.allclose(a, np.dot(a, np.dot(B, a)))
    True
    >>> np.allclose(B, np.dot(B, np.dot(a, B)))
    True

    """
    a, wrap = _makearray(a)
    rcond = asarray(rcond)
    if _is_empty_2d(a):
        m, n = a.shape[-2:]
        res = empty((a.shape[:-2] + (n, m)), dtype=(a.dtype))
        return wrap(res)
    a = a.conjugate()
    u, s, vt = svd(a, full_matrices=False, hermitian=hermitian)
    cutoff = rcond[(..., newaxis)] * amax(s, axis=(-1), keepdims=True)
    large = s > cutoff
    s = divide(1, s, where=large, out=s)
    s[~large] = 0
    res = matmul(transpose(vt), multiply(s[(..., newaxis)], transpose(u)))
    return wrap(res)


@array_function_dispatch(_unary_dispatcher)
def slogdet(a):
    """
    Compute the sign and (natural) logarithm of the determinant of an array.

    If an array has a very small or very large determinant, then a call to
    `det` may overflow or underflow. This routine is more robust against such
    issues, because it computes the logarithm of the determinant rather than
    the determinant itself.

    Parameters
    ----------
    a : (..., M, M) array_like
        Input array, has to be a square 2-D array.

    Returns
    -------
    sign : (...) array_like
        A number representing the sign of the determinant. For a real matrix,
        this is 1, 0, or -1. For a complex matrix, this is a complex number
        with absolute value 1 (i.e., it is on the unit circle), or else 0.
    logdet : (...) array_like
        The natural log of the absolute value of the determinant.

    If the determinant is zero, then `sign` will be 0 and `logdet` will be
    -Inf. In all cases, the determinant is equal to ``sign * np.exp(logdet)``.

    See Also
    --------
    det

    Notes
    -----

    .. versionadded:: 1.8.0

    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    .. versionadded:: 1.6.0

    The determinant is computed via LU factorization using the LAPACK
    routine ``z/dgetrf``.

    Examples
    --------
    The determinant of a 2-D array ``[[a, b], [c, d]]`` is ``ad - bc``:

    >>> a = np.array([[1, 2], [3, 4]])
    >>> (sign, logdet) = np.linalg.slogdet(a)
    >>> (sign, logdet)
    (-1, 0.69314718055994529) # may vary
    >>> sign * np.exp(logdet)
    -2.0

    Computing log-determinants for a stack of matrices:

    >>> a = np.array([ [[1, 2], [3, 4]], [[1, 2], [2, 1]], [[1, 3], [3, 1]] ])
    >>> a.shape
    (3, 2, 2)
    >>> sign, logdet = np.linalg.slogdet(a)
    >>> (sign, logdet)
    (array([-1., -1., -1.]), array([ 0.69314718,  1.09861229,  2.07944154]))
    >>> sign * np.exp(logdet)
    array([-2., -3., -8.])

    This routine succeeds where ordinary `det` does not:

    >>> np.linalg.det(np.eye(500) * 0.1)
    0.0
    >>> np.linalg.slogdet(np.eye(500) * 0.1)
    (1, -1151.2925464970228)

    """
    a = asarray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)
    real_t = _realType(result_t)
    signature = 'D->Dd' if isComplexType(t) else 'd->dd'
    sign, logdet = _umath_linalg.slogdet(a, signature=signature)
    sign = sign.astype(result_t, copy=False)
    logdet = logdet.astype(real_t, copy=False)
    return (sign, logdet)


@array_function_dispatch(_unary_dispatcher)
def det(a):
    """
    Compute the determinant of an array.

    Parameters
    ----------
    a : (..., M, M) array_like
        Input array to compute determinants for.

    Returns
    -------
    det : (...) array_like
        Determinant of `a`.

    See Also
    --------
    slogdet : Another way to represent the determinant, more suitable
      for large matrices where underflow/overflow may occur.
    scipy.linalg.det : Similar function in SciPy.

    Notes
    -----

    .. versionadded:: 1.8.0

    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The determinant is computed via LU factorization using the LAPACK
    routine ``z/dgetrf``.

    Examples
    --------
    The determinant of a 2-D array [[a, b], [c, d]] is ad - bc:

    >>> a = np.array([[1, 2], [3, 4]])
    >>> np.linalg.det(a)
    -2.0 # may vary

    Computing determinants for a stack of matrices:

    >>> a = np.array([ [[1, 2], [3, 4]], [[1, 2], [2, 1]], [[1, 3], [3, 1]] ])
    >>> a.shape
    (3, 2, 2)
    >>> np.linalg.det(a)
    array([-2., -3., -8.])

    """
    a = asarray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)
    signature = 'D->D' if isComplexType(t) else 'd->d'
    r = _umath_linalg.det(a, signature=signature)
    r = r.astype(result_t, copy=False)
    return r


def _lstsq_dispatcher(a, b, rcond=None):
    return (
     a, b)


@array_function_dispatch(_lstsq_dispatcher)
def lstsq(a, b, rcond='warn'):
    """
    Return the least-squares solution to a linear matrix equation.

    Computes the vector x that approximatively solves the equation
    ``a @ x = b``. The equation may be under-, well-, or over-determined
    (i.e., the number of linearly independent rows of `a` can be less than,
    equal to, or greater than its number of linearly independent columns).
    If `a` is square and of full rank, then `x` (but for round-off error)
    is the "exact" solution of the equation. Else, `x` minimizes the
    Euclidean 2-norm :math:`|| b - a x ||`.

    Parameters
    ----------
    a : (M, N) array_like
        "Coefficient" matrix.
    b : {(M,), (M, K)} array_like
        Ordinate or "dependent variable" values. If `b` is two-dimensional,
        the least-squares solution is calculated for each of the `K` columns
        of `b`.
    rcond : float, optional
        Cut-off ratio for small singular values of `a`.
        For the purposes of rank determination, singular values are treated
        as zero if they are smaller than `rcond` times the largest singular
        value of `a`.

        .. versionchanged:: 1.14.0
           If not set, a FutureWarning is given. The previous default
           of ``-1`` will use the machine precision as `rcond` parameter,
           the new default will use the machine precision times `max(M, N)`.
           To silence the warning and use the new default, use ``rcond=None``,
           to keep using the old behavior, use ``rcond=-1``.

    Returns
    -------
    x : {(N,), (N, K)} ndarray
        Least-squares solution. If `b` is two-dimensional,
        the solutions are in the `K` columns of `x`.
    residuals : {(1,), (K,), (0,)} ndarray
        Sums of residuals; squared Euclidean 2-norm for each column in
        ``b - a*x``.
        If the rank of `a` is < N or M <= N, this is an empty array.
        If `b` is 1-dimensional, this is a (1,) shape array.
        Otherwise the shape is (K,).
    rank : int
        Rank of matrix `a`.
    s : (min(M, N),) ndarray
        Singular values of `a`.

    Raises
    ------
    LinAlgError
        If computation does not converge.

    See Also
    --------
    scipy.linalg.lstsq : Similar function in SciPy.

    Notes
    -----
    If `b` is a matrix, then all array results are returned as matrices.

    Examples
    --------
    Fit a line, ``y = mx + c``, through some noisy data-points:

    >>> x = np.array([0, 1, 2, 3])
    >>> y = np.array([-1, 0.2, 0.9, 2.1])

    By examining the coefficients, we see that the line should have a
    gradient of roughly 1 and cut the y-axis at, more or less, -1.

    We can rewrite the line equation as ``y = Ap``, where ``A = [[x 1]]``
    and ``p = [[m], [c]]``.  Now use `lstsq` to solve for `p`:

    >>> A = np.vstack([x, np.ones(len(x))]).T
    >>> A
    array([[ 0.,  1.],
           [ 1.,  1.],
           [ 2.,  1.],
           [ 3.,  1.]])

    >>> m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    >>> m, c
    (1.0 -0.95) # may vary

    Plot the data along with the fitted line:

    >>> import matplotlib.pyplot as plt
    >>> _ = plt.plot(x, y, 'o', label='Original data', markersize=10)
    >>> _ = plt.plot(x, m*x + c, 'r', label='Fitted line')
    >>> _ = plt.legend()
    >>> plt.show()

    """
    a, _ = _makearray(a)
    b, wrap = _makearray(b)
    is_1d = b.ndim == 1
    if is_1d:
        b = b[:, newaxis]
    else:
        _assert_2d(a, b)
        m, n = a.shape[-2:]
        m2, n_rhs = b.shape[-2:]
        if m != m2:
            raise LinAlgError('Incompatible dimensions')
        t, result_t = _commonType(a, b)
        real_t = _linalgRealType(t)
        result_real_t = _realType(result_t)
        if rcond == 'warn':
            warnings.warn('`rcond` parameter will change to the default of machine precision times ``max(M, N)`` where M and N are the input matrix dimensions.\nTo use the future default and silence this warning we advise to pass `rcond=None`, to keep using the old, explicitly pass `rcond=-1`.', FutureWarning,
              stacklevel=3)
            rcond = -1
        if rcond is None:
            rcond = finfo(t).eps * max(n, m)
        if m <= n:
            gufunc = _umath_linalg.lstsq_m
        else:
            gufunc = _umath_linalg.lstsq_n
    signature = 'DDd->Ddid' if isComplexType(t) else 'ddd->ddid'
    extobj = get_linalg_error_extobj(_raise_linalgerror_lstsq)
    if n_rhs == 0:
        b = zeros((b.shape[:-2] + (m, n_rhs + 1)), dtype=(b.dtype))
    x, resids, rank, s = gufunc(a, b, rcond, signature=signature, extobj=extobj)
    if m == 0:
        x[...] = 0
    if n_rhs == 0:
        x = x[..., :n_rhs]
        resids = resids[..., :n_rhs]
    if is_1d:
        x = x.squeeze(axis=(-1))
    if rank != n or m <= n:
        resids = array([], result_real_t)
    s = s.astype(result_real_t, copy=False)
    resids = resids.astype(result_real_t, copy=False)
    x = x.astype(result_t, copy=True)
    return (wrap(x), wrap(resids), rank, s)


def _multi_svd_norm(x, row_axis, col_axis, op):
    """Compute a function of the singular values of the 2-D matrices in `x`.

    This is a private utility function used by `numpy.linalg.norm()`.

    Parameters
    ----------
    x : ndarray
    row_axis, col_axis : int
        The axes of `x` that hold the 2-D matrices.
    op : callable
        This should be either numpy.amin or `numpy.amax` or `numpy.sum`.

    Returns
    -------
    result : float or ndarray
        If `x` is 2-D, the return values is a float.
        Otherwise, it is an array with ``x.ndim - 2`` dimensions.
        The return values are either the minimum or maximum or sum of the
        singular values of the matrices, depending on whether `op`
        is `numpy.amin` or `numpy.amax` or `numpy.sum`.

    """
    y = moveaxis(x, (row_axis, col_axis), (-2, -1))
    result = op(svd(y, compute_uv=False), axis=(-1))
    return result


def _norm_dispatcher(x, ord=None, axis=None, keepdims=None):
    return (
     x,)


@array_function_dispatch(_norm_dispatcher)
def norm--- This code section failed: ---

 L.2514         0  LOAD_GLOBAL              asarray
                2  LOAD_FAST                'x'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'x'

 L.2516         8  LOAD_GLOBAL              issubclass
               10  LOAD_FAST                'x'
               12  LOAD_ATTR                dtype
               14  LOAD_ATTR                type
               16  LOAD_GLOBAL              inexact
               18  LOAD_GLOBAL              object_
               20  BUILD_TUPLE_2         2 
               22  CALL_FUNCTION_2       2  '2 positional arguments'
               24  POP_JUMP_IF_TRUE     36  'to 36'

 L.2517        26  LOAD_FAST                'x'
               28  LOAD_METHOD              astype
               30  LOAD_GLOBAL              float
               32  CALL_METHOD_1         1  '1 positional argument'
               34  STORE_FAST               'x'
             36_0  COME_FROM            24  '24'

 L.2520        36  LOAD_FAST                'axis'
               38  LOAD_CONST               None
               40  COMPARE_OP               is
               42  POP_JUMP_IF_FALSE   186  'to 186'

 L.2521        44  LOAD_FAST                'x'
               46  LOAD_ATTR                ndim
               48  STORE_FAST               'ndim'

 L.2522        50  LOAD_FAST                'ord'
               52  LOAD_CONST               None
               54  COMPARE_OP               is
               56  POP_JUMP_IF_TRUE     90  'to 90'

 L.2523        58  LOAD_FAST                'ord'
               60  LOAD_CONST               ('f', 'fro')
               62  COMPARE_OP               in
               64  POP_JUMP_IF_FALSE    74  'to 74'
               66  LOAD_FAST                'ndim'
               68  LOAD_CONST               2
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_TRUE     90  'to 90'
             74_0  COME_FROM            64  '64'

 L.2524        74  LOAD_FAST                'ord'
               76  LOAD_CONST               2
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   186  'to 186'
               82  LOAD_FAST                'ndim'
               84  LOAD_CONST               1
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   186  'to 186'
             90_0  COME_FROM            72  '72'
             90_1  COME_FROM            56  '56'

 L.2526        90  LOAD_FAST                'x'
               92  LOAD_ATTR                ravel
               94  LOAD_STR                 'K'
               96  LOAD_CONST               ('order',)
               98  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              100  STORE_FAST               'x'

 L.2527       102  LOAD_GLOBAL              isComplexType
              104  LOAD_FAST                'x'
              106  LOAD_ATTR                dtype
              108  LOAD_ATTR                type
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  POP_JUMP_IF_FALSE   144  'to 144'

 L.2528       114  LOAD_GLOBAL              dot
              116  LOAD_FAST                'x'
              118  LOAD_ATTR                real
              120  LOAD_FAST                'x'
              122  LOAD_ATTR                real
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  LOAD_GLOBAL              dot
              128  LOAD_FAST                'x'
              130  LOAD_ATTR                imag
              132  LOAD_FAST                'x'
              134  LOAD_ATTR                imag
              136  CALL_FUNCTION_2       2  '2 positional arguments'
              138  BINARY_ADD       
              140  STORE_FAST               'sqnorm'
              142  JUMP_FORWARD        154  'to 154'
            144_0  COME_FROM           112  '112'

 L.2530       144  LOAD_GLOBAL              dot
              146  LOAD_FAST                'x'
              148  LOAD_FAST                'x'
              150  CALL_FUNCTION_2       2  '2 positional arguments'
              152  STORE_FAST               'sqnorm'
            154_0  COME_FROM           142  '142'

 L.2531       154  LOAD_GLOBAL              sqrt
              156  LOAD_FAST                'sqnorm'
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  STORE_FAST               'ret'

 L.2532       162  LOAD_FAST                'keepdims'
              164  POP_JUMP_IF_FALSE   182  'to 182'

 L.2533       166  LOAD_FAST                'ret'
              168  LOAD_METHOD              reshape
              170  LOAD_FAST                'ndim'
              172  LOAD_CONST               1
              174  BUILD_LIST_1          1 
              176  BINARY_MULTIPLY  
              178  CALL_METHOD_1         1  '1 positional argument'
              180  STORE_FAST               'ret'
            182_0  COME_FROM           164  '164'

 L.2534       182  LOAD_FAST                'ret'
              184  RETURN_VALUE     
            186_0  COME_FROM            88  '88'
            186_1  COME_FROM            80  '80'
            186_2  COME_FROM            42  '42'

 L.2537       186  LOAD_FAST                'x'
              188  LOAD_ATTR                ndim
              190  STORE_FAST               'nd'

 L.2538       192  LOAD_FAST                'axis'
              194  LOAD_CONST               None
              196  COMPARE_OP               is
              198  POP_JUMP_IF_FALSE   214  'to 214'

 L.2539       200  LOAD_GLOBAL              tuple
              202  LOAD_GLOBAL              range
              204  LOAD_FAST                'nd'
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  STORE_FAST               'axis'
              212  JUMP_FORWARD        292  'to 292'
            214_0  COME_FROM           198  '198'

 L.2540       214  LOAD_GLOBAL              isinstance
              216  LOAD_FAST                'axis'
              218  LOAD_GLOBAL              tuple
              220  CALL_FUNCTION_2       2  '2 positional arguments'
          222_224  POP_JUMP_IF_TRUE    292  'to 292'

 L.2541       226  SETUP_EXCEPT        240  'to 240'

 L.2542       228  LOAD_GLOBAL              int
              230  LOAD_FAST                'axis'
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  STORE_FAST               'axis'
              236  POP_BLOCK        
              238  JUMP_FORWARD        286  'to 286'
            240_0  COME_FROM_EXCEPT    226  '226'

 L.2543       240  DUP_TOP          
              242  LOAD_GLOBAL              Exception
              244  COMPARE_OP               exception-match
          246_248  POP_JUMP_IF_FALSE   284  'to 284'
              250  POP_TOP          
              252  STORE_FAST               'e'
              254  POP_TOP          
              256  SETUP_FINALLY       272  'to 272'

 L.2544       258  LOAD_GLOBAL              TypeError
              260  LOAD_STR                 "'axis' must be None, an integer or a tuple of integers"
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  LOAD_FAST                'e'
              266  RAISE_VARARGS_2       2  'exception instance with __cause__'
              268  POP_BLOCK        
              270  LOAD_CONST               None
            272_0  COME_FROM_FINALLY   256  '256'
              272  LOAD_CONST               None
              274  STORE_FAST               'e'
              276  DELETE_FAST              'e'
              278  END_FINALLY      
              280  POP_EXCEPT       
              282  JUMP_FORWARD        286  'to 286'
            284_0  COME_FROM           246  '246'
              284  END_FINALLY      
            286_0  COME_FROM           282  '282'
            286_1  COME_FROM           238  '238'

 L.2545       286  LOAD_FAST                'axis'
              288  BUILD_TUPLE_1         1 
              290  STORE_FAST               'axis'
            292_0  COME_FROM           222  '222'
            292_1  COME_FROM           212  '212'

 L.2547       292  LOAD_GLOBAL              len
              294  LOAD_FAST                'axis'
              296  CALL_FUNCTION_1       1  '1 positional argument'
              298  LOAD_CONST               1
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   568  'to 568'

 L.2548       306  LOAD_FAST                'ord'
              308  LOAD_GLOBAL              Inf
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   334  'to 334'

 L.2549       316  LOAD_GLOBAL              abs
              318  LOAD_FAST                'x'
              320  CALL_FUNCTION_1       1  '1 positional argument'
              322  LOAD_ATTR                max
              324  LOAD_FAST                'axis'
              326  LOAD_FAST                'keepdims'
              328  LOAD_CONST               ('axis', 'keepdims')
              330  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              332  RETURN_VALUE     
            334_0  COME_FROM           312  '312'

 L.2550       334  LOAD_FAST                'ord'
              336  LOAD_GLOBAL              Inf
              338  UNARY_NEGATIVE   
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   364  'to 364'

 L.2551       346  LOAD_GLOBAL              abs
              348  LOAD_FAST                'x'
              350  CALL_FUNCTION_1       1  '1 positional argument'
              352  LOAD_ATTR                min
              354  LOAD_FAST                'axis'
              356  LOAD_FAST                'keepdims'
              358  LOAD_CONST               ('axis', 'keepdims')
              360  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              362  RETURN_VALUE     
            364_0  COME_FROM           342  '342'

 L.2552       364  LOAD_FAST                'ord'
              366  LOAD_CONST               0
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   402  'to 402'

 L.2554       374  LOAD_FAST                'x'
              376  LOAD_CONST               0
              378  COMPARE_OP               !=
              380  LOAD_METHOD              astype
              382  LOAD_FAST                'x'
              384  LOAD_ATTR                real
              386  LOAD_ATTR                dtype
              388  CALL_METHOD_1         1  '1 positional argument'
              390  LOAD_ATTR                sum
              392  LOAD_FAST                'axis'
              394  LOAD_FAST                'keepdims'
              396  LOAD_CONST               ('axis', 'keepdims')
              398  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              400  RETURN_VALUE     
            402_0  COME_FROM           370  '370'

 L.2555       402  LOAD_FAST                'ord'
              404  LOAD_CONST               1
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   432  'to 432'

 L.2557       412  LOAD_GLOBAL              add
              414  LOAD_ATTR                reduce
              416  LOAD_GLOBAL              abs
              418  LOAD_FAST                'x'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  LOAD_FAST                'axis'
              424  LOAD_FAST                'keepdims'
              426  LOAD_CONST               ('axis', 'keepdims')
              428  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              430  RETURN_VALUE     
            432_0  COME_FROM           408  '408'

 L.2558       432  LOAD_FAST                'ord'
              434  LOAD_CONST               None
              436  COMPARE_OP               is
          438_440  POP_JUMP_IF_TRUE    452  'to 452'
              442  LOAD_FAST                'ord'
              444  LOAD_CONST               2
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_FALSE   486  'to 486'
            452_0  COME_FROM           438  '438'

 L.2560       452  LOAD_FAST                'x'
              454  LOAD_METHOD              conj
              456  CALL_METHOD_0         0  '0 positional arguments'
              458  LOAD_FAST                'x'
              460  BINARY_MULTIPLY  
              462  LOAD_ATTR                real
              464  STORE_FAST               's'

 L.2561       466  LOAD_GLOBAL              sqrt
              468  LOAD_GLOBAL              add
              470  LOAD_ATTR                reduce
              472  LOAD_FAST                's'
              474  LOAD_FAST                'axis'
              476  LOAD_FAST                'keepdims'
              478  LOAD_CONST               ('axis', 'keepdims')
              480  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  RETURN_VALUE     
            486_0  COME_FROM           448  '448'

 L.2564       486  LOAD_GLOBAL              isinstance
              488  LOAD_FAST                'ord'
              490  LOAD_GLOBAL              str
              492  CALL_FUNCTION_2       2  '2 positional arguments'
          494_496  POP_JUMP_IF_FALSE   516  'to 516'

 L.2565       498  LOAD_GLOBAL              ValueError
              500  LOAD_STR                 "Invalid norm order '"
              502  LOAD_FAST                'ord'
              504  FORMAT_VALUE          0  ''
              506  LOAD_STR                 "' for vectors"
              508  BUILD_STRING_3        3 
              510  CALL_FUNCTION_1       1  '1 positional argument'
              512  RAISE_VARARGS_1       1  'exception instance'
              514  JUMP_FORWARD       1046  'to 1046'
            516_0  COME_FROM           494  '494'

 L.2567       516  LOAD_GLOBAL              abs
              518  LOAD_FAST                'x'
              520  CALL_FUNCTION_1       1  '1 positional argument'
              522  STORE_FAST               'absx'

 L.2568       524  LOAD_FAST                'absx'
              526  LOAD_FAST                'ord'
              528  INPLACE_POWER    
              530  STORE_FAST               'absx'

 L.2569       532  LOAD_GLOBAL              add
              534  LOAD_ATTR                reduce
              536  LOAD_FAST                'absx'
              538  LOAD_FAST                'axis'
              540  LOAD_FAST                'keepdims'
              542  LOAD_CONST               ('axis', 'keepdims')
              544  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              546  STORE_FAST               'ret'

 L.2570       548  LOAD_FAST                'ret'
              550  LOAD_CONST               1
              552  LOAD_FAST                'ord'
              554  BINARY_TRUE_DIVIDE
              556  INPLACE_POWER    
              558  STORE_FAST               'ret'

 L.2571       560  LOAD_FAST                'ret'
              562  RETURN_VALUE     
          564_566  JUMP_FORWARD       1046  'to 1046'
            568_0  COME_FROM           302  '302'

 L.2572       568  LOAD_GLOBAL              len
              570  LOAD_FAST                'axis'
              572  CALL_FUNCTION_1       1  '1 positional argument'
              574  LOAD_CONST               2
              576  COMPARE_OP               ==
          578_580  POP_JUMP_IF_FALSE  1038  'to 1038'

 L.2573       582  LOAD_FAST                'axis'
              584  UNPACK_SEQUENCE_2     2 
              586  STORE_FAST               'row_axis'
              588  STORE_FAST               'col_axis'

 L.2574       590  LOAD_GLOBAL              normalize_axis_index
              592  LOAD_FAST                'row_axis'
              594  LOAD_FAST                'nd'
              596  CALL_FUNCTION_2       2  '2 positional arguments'
              598  STORE_FAST               'row_axis'

 L.2575       600  LOAD_GLOBAL              normalize_axis_index
              602  LOAD_FAST                'col_axis'
              604  LOAD_FAST                'nd'
              606  CALL_FUNCTION_2       2  '2 positional arguments'
              608  STORE_FAST               'col_axis'

 L.2576       610  LOAD_FAST                'row_axis'
              612  LOAD_FAST                'col_axis'
              614  COMPARE_OP               ==
          616_618  POP_JUMP_IF_FALSE   628  'to 628'

 L.2577       620  LOAD_GLOBAL              ValueError
              622  LOAD_STR                 'Duplicate axes given.'
              624  CALL_FUNCTION_1       1  '1 positional argument'
              626  RAISE_VARARGS_1       1  'exception instance'
            628_0  COME_FROM           616  '616'

 L.2578       628  LOAD_FAST                'ord'
              630  LOAD_CONST               2
              632  COMPARE_OP               ==
          634_636  POP_JUMP_IF_FALSE   656  'to 656'

 L.2579       638  LOAD_GLOBAL              _multi_svd_norm
              640  LOAD_FAST                'x'
              642  LOAD_FAST                'row_axis'
              644  LOAD_FAST                'col_axis'
              646  LOAD_GLOBAL              amax
              648  CALL_FUNCTION_4       4  '4 positional arguments'
              650  STORE_FAST               'ret'
          652_654  JUMP_FORWARD        984  'to 984'
            656_0  COME_FROM           634  '634'

 L.2580       656  LOAD_FAST                'ord'
              658  LOAD_CONST               -2
              660  COMPARE_OP               ==
          662_664  POP_JUMP_IF_FALSE   684  'to 684'

 L.2581       666  LOAD_GLOBAL              _multi_svd_norm
              668  LOAD_FAST                'x'
              670  LOAD_FAST                'row_axis'
              672  LOAD_FAST                'col_axis'
              674  LOAD_GLOBAL              amin
              676  CALL_FUNCTION_4       4  '4 positional arguments'
              678  STORE_FAST               'ret'
          680_682  JUMP_FORWARD        984  'to 984'
            684_0  COME_FROM           662  '662'

 L.2582       684  LOAD_FAST                'ord'
              686  LOAD_CONST               1
              688  COMPARE_OP               ==
          690_692  POP_JUMP_IF_FALSE   740  'to 740'

 L.2583       694  LOAD_FAST                'col_axis'
              696  LOAD_FAST                'row_axis'
              698  COMPARE_OP               >
          700_702  POP_JUMP_IF_FALSE   712  'to 712'

 L.2584       704  LOAD_FAST                'col_axis'
              706  LOAD_CONST               1
              708  INPLACE_SUBTRACT 
              710  STORE_FAST               'col_axis'
            712_0  COME_FROM           700  '700'

 L.2585       712  LOAD_GLOBAL              add
              714  LOAD_ATTR                reduce
              716  LOAD_GLOBAL              abs
              718  LOAD_FAST                'x'
              720  CALL_FUNCTION_1       1  '1 positional argument'
              722  LOAD_FAST                'row_axis'
              724  LOAD_CONST               ('axis',)
              726  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              728  LOAD_ATTR                max
              730  LOAD_FAST                'col_axis'
              732  LOAD_CONST               ('axis',)
              734  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              736  STORE_FAST               'ret'
              738  JUMP_FORWARD        984  'to 984'
            740_0  COME_FROM           690  '690'

 L.2586       740  LOAD_FAST                'ord'
              742  LOAD_GLOBAL              Inf
              744  COMPARE_OP               ==
          746_748  POP_JUMP_IF_FALSE   796  'to 796'

 L.2587       750  LOAD_FAST                'row_axis'
              752  LOAD_FAST                'col_axis'
              754  COMPARE_OP               >
          756_758  POP_JUMP_IF_FALSE   768  'to 768'

 L.2588       760  LOAD_FAST                'row_axis'
              762  LOAD_CONST               1
              764  INPLACE_SUBTRACT 
              766  STORE_FAST               'row_axis'
            768_0  COME_FROM           756  '756'

 L.2589       768  LOAD_GLOBAL              add
              770  LOAD_ATTR                reduce
              772  LOAD_GLOBAL              abs
              774  LOAD_FAST                'x'
              776  CALL_FUNCTION_1       1  '1 positional argument'
              778  LOAD_FAST                'col_axis'
              780  LOAD_CONST               ('axis',)
              782  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              784  LOAD_ATTR                max
              786  LOAD_FAST                'row_axis'
              788  LOAD_CONST               ('axis',)
              790  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              792  STORE_FAST               'ret'
              794  JUMP_FORWARD        984  'to 984'
            796_0  COME_FROM           746  '746'

 L.2590       796  LOAD_FAST                'ord'
              798  LOAD_CONST               -1
              800  COMPARE_OP               ==
          802_804  POP_JUMP_IF_FALSE   852  'to 852'

 L.2591       806  LOAD_FAST                'col_axis'
              808  LOAD_FAST                'row_axis'
              810  COMPARE_OP               >
          812_814  POP_JUMP_IF_FALSE   824  'to 824'

 L.2592       816  LOAD_FAST                'col_axis'
              818  LOAD_CONST               1
              820  INPLACE_SUBTRACT 
              822  STORE_FAST               'col_axis'
            824_0  COME_FROM           812  '812'

 L.2593       824  LOAD_GLOBAL              add
              826  LOAD_ATTR                reduce
              828  LOAD_GLOBAL              abs
              830  LOAD_FAST                'x'
              832  CALL_FUNCTION_1       1  '1 positional argument'
              834  LOAD_FAST                'row_axis'
              836  LOAD_CONST               ('axis',)
              838  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              840  LOAD_ATTR                min
              842  LOAD_FAST                'col_axis'
              844  LOAD_CONST               ('axis',)
              846  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              848  STORE_FAST               'ret'
              850  JUMP_FORWARD        984  'to 984'
            852_0  COME_FROM           802  '802'

 L.2594       852  LOAD_FAST                'ord'
              854  LOAD_GLOBAL              Inf
              856  UNARY_NEGATIVE   
              858  COMPARE_OP               ==
          860_862  POP_JUMP_IF_FALSE   910  'to 910'

 L.2595       864  LOAD_FAST                'row_axis'
              866  LOAD_FAST                'col_axis'
              868  COMPARE_OP               >
          870_872  POP_JUMP_IF_FALSE   882  'to 882'

 L.2596       874  LOAD_FAST                'row_axis'
              876  LOAD_CONST               1
              878  INPLACE_SUBTRACT 
              880  STORE_FAST               'row_axis'
            882_0  COME_FROM           870  '870'

 L.2597       882  LOAD_GLOBAL              add
              884  LOAD_ATTR                reduce
              886  LOAD_GLOBAL              abs
              888  LOAD_FAST                'x'
              890  CALL_FUNCTION_1       1  '1 positional argument'
              892  LOAD_FAST                'col_axis'
              894  LOAD_CONST               ('axis',)
              896  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              898  LOAD_ATTR                min
              900  LOAD_FAST                'row_axis'
              902  LOAD_CONST               ('axis',)
              904  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              906  STORE_FAST               'ret'
              908  JUMP_FORWARD        984  'to 984'
            910_0  COME_FROM           860  '860'

 L.2598       910  LOAD_FAST                'ord'
              912  LOAD_CONST               (None, 'fro', 'f')
              914  COMPARE_OP               in
          916_918  POP_JUMP_IF_FALSE   950  'to 950'

 L.2599       920  LOAD_GLOBAL              sqrt
              922  LOAD_GLOBAL              add
              924  LOAD_ATTR                reduce
              926  LOAD_FAST                'x'
              928  LOAD_METHOD              conj
              930  CALL_METHOD_0         0  '0 positional arguments'
              932  LOAD_FAST                'x'
              934  BINARY_MULTIPLY  
              936  LOAD_ATTR                real
              938  LOAD_FAST                'axis'
              940  LOAD_CONST               ('axis',)
              942  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              944  CALL_FUNCTION_1       1  '1 positional argument'
              946  STORE_FAST               'ret'
              948  JUMP_FORWARD        984  'to 984'
            950_0  COME_FROM           916  '916'

 L.2600       950  LOAD_FAST                'ord'
              952  LOAD_STR                 'nuc'
              954  COMPARE_OP               ==
          956_958  POP_JUMP_IF_FALSE   976  'to 976'

 L.2601       960  LOAD_GLOBAL              _multi_svd_norm
              962  LOAD_FAST                'x'
              964  LOAD_FAST                'row_axis'
              966  LOAD_FAST                'col_axis'
              968  LOAD_GLOBAL              sum
              970  CALL_FUNCTION_4       4  '4 positional arguments'
              972  STORE_FAST               'ret'
              974  JUMP_FORWARD        984  'to 984'
            976_0  COME_FROM           956  '956'

 L.2603       976  LOAD_GLOBAL              ValueError
              978  LOAD_STR                 'Invalid norm order for matrices.'
              980  CALL_FUNCTION_1       1  '1 positional argument'
              982  RAISE_VARARGS_1       1  'exception instance'
            984_0  COME_FROM           974  '974'
            984_1  COME_FROM           948  '948'
            984_2  COME_FROM           908  '908'
            984_3  COME_FROM           850  '850'
            984_4  COME_FROM           794  '794'
            984_5  COME_FROM           738  '738'
            984_6  COME_FROM           680  '680'
            984_7  COME_FROM           652  '652'

 L.2604       984  LOAD_FAST                'keepdims'
          986_988  POP_JUMP_IF_FALSE  1034  'to 1034'

 L.2605       990  LOAD_GLOBAL              list
              992  LOAD_FAST                'x'
            994_0  COME_FROM           514  '514'
              994  LOAD_ATTR                shape
              996  CALL_FUNCTION_1       1  '1 positional argument'
              998  STORE_FAST               'ret_shape'

 L.2606      1000  LOAD_CONST               1
             1002  LOAD_FAST                'ret_shape'
             1004  LOAD_FAST                'axis'
             1006  LOAD_CONST               0
             1008  BINARY_SUBSCR    
             1010  STORE_SUBSCR     

 L.2607      1012  LOAD_CONST               1
             1014  LOAD_FAST                'ret_shape'
             1016  LOAD_FAST                'axis'
             1018  LOAD_CONST               1
             1020  BINARY_SUBSCR    
             1022  STORE_SUBSCR     

 L.2608      1024  LOAD_FAST                'ret'
             1026  LOAD_METHOD              reshape
             1028  LOAD_FAST                'ret_shape'
             1030  CALL_METHOD_1         1  '1 positional argument'
             1032  STORE_FAST               'ret'
           1034_0  COME_FROM           986  '986'

 L.2609      1034  LOAD_FAST                'ret'
             1036  RETURN_VALUE     
           1038_0  COME_FROM           578  '578'

 L.2611      1038  LOAD_GLOBAL              ValueError
             1040  LOAD_STR                 'Improper number of dimensions to norm.'
             1042  CALL_FUNCTION_1       1  '1 positional argument'
             1044  RAISE_VARARGS_1       1  'exception instance'
           1046_0  COME_FROM           564  '564'

Parse error at or near `COME_FROM' instruction at offset 994_0


def _multidot_dispatcher(arrays, *, out=None):
    yield from arrays
    yield out


@array_function_dispatch(_multidot_dispatcher)
def multi_dot(arrays, *, out=None):
    """
    Compute the dot product of two or more arrays in a single function call,
    while automatically selecting the fastest evaluation order.

    `multi_dot` chains `numpy.dot` and uses optimal parenthesization
    of the matrices [1]_ [2]_. Depending on the shapes of the matrices,
    this can speed up the multiplication a lot.

    If the first argument is 1-D it is treated as a row vector.
    If the last argument is 1-D it is treated as a column vector.
    The other arguments must be 2-D.

    Think of `multi_dot` as::

        def multi_dot(arrays): return functools.reduce(np.dot, arrays)

    Parameters
    ----------
    arrays : sequence of array_like
        If the first argument is 1-D it is treated as row vector.
        If the last argument is 1-D it is treated as column vector.
        The other arguments must be 2-D.
    out : ndarray, optional
        Output argument. This must have the exact kind that would be returned
        if it was not used. In particular, it must have the right type, must be
        C-contiguous, and its dtype must be the dtype that would be returned
        for `dot(a, b)`. This is a performance feature. Therefore, if these
        conditions are not met, an exception is raised, instead of attempting
        to be flexible.

        .. versionadded:: 1.19.0

    Returns
    -------
    output : ndarray
        Returns the dot product of the supplied arrays.

    See Also
    --------
    dot : dot multiplication with two arguments.

    References
    ----------

    .. [1] Cormen, "Introduction to Algorithms", Chapter 15.2, p. 370-378
    .. [2] https://en.wikipedia.org/wiki/Matrix_chain_multiplication

    Examples
    --------
    `multi_dot` allows you to write::

    >>> from numpy.linalg import multi_dot
    >>> # Prepare some data
    >>> A = np.random.random((10000, 100))
    >>> B = np.random.random((100, 1000))
    >>> C = np.random.random((1000, 5))
    >>> D = np.random.random((5, 333))
    >>> # the actual dot multiplication
    >>> _ = multi_dot([A, B, C, D])

    instead of::

    >>> _ = np.dot(np.dot(np.dot(A, B), C), D)
    >>> # or
    >>> _ = A.dot(B).dot(C).dot(D)

    Notes
    -----
    The cost for a matrix multiplication can be calculated with the
    following function::

        def cost(A, B):
            return A.shape[0] * A.shape[1] * B.shape[1]

    Assume we have three matrices
    :math:`A_{10x100}, B_{100x5}, C_{5x50}`.

    The costs for the two different parenthesizations are as follows::

        cost((AB)C) = 10*100*5 + 10*5*50   = 5000 + 2500   = 7500
        cost(A(BC)) = 10*100*50 + 100*5*50 = 50000 + 25000 = 75000

    """
    n = len(arrays)
    if n < 2:
        raise ValueError('Expecting at least two arrays.')
    else:
        if n == 2:
            return dot((arrays[0]), (arrays[1]), out=out)
        else:
            arrays = [asanyarray(a) for a in arrays]
            ndim_first, ndim_last = arrays[0].ndim, arrays[(-1)].ndim
            if arrays[0].ndim == 1:
                arrays[0] = atleast_2d(arrays[0])
            if arrays[(-1)].ndim == 1:
                arrays[-1] = atleast_2d(arrays[(-1)]).T
            _assert_2d(*arrays)
            if n == 3:
                result = _multi_dot_three((arrays[0]), (arrays[1]), (arrays[2]), out=out)
            else:
                order = _multi_dot_matrix_chain_order(arrays)
            result = _multi_dot(arrays, order, 0, (n - 1), out=out)
        if ndim_first == 1:
            if ndim_last == 1:
                return result[(0, 0)]
        if ndim_first == 1 or ndim_last == 1:
            return result.ravel()
        return result


def _multi_dot_three(A, B, C, out=None):
    """
    Find the best order for three arrays and do the multiplication.

    For three arguments `_multi_dot_three` is approximately 15 times faster
    than `_multi_dot_matrix_chain_order`

    """
    a0, a1b0 = A.shape
    b1c0, c1 = C.shape
    cost1 = a0 * b1c0 * (a1b0 + c1)
    cost2 = a1b0 * c1 * (a0 + b1c0)
    if cost1 < cost2:
        return dot((dot(A, B)), C, out=out)
    return dot(A, (dot(B, C)), out=out)


def _multi_dot_matrix_chain_order(arrays, return_costs=False):
    """
    Return a np.array that encodes the optimal order of mutiplications.

    The optimal order array is then used by `_multi_dot()` to do the
    multiplication.

    Also return the cost matrix if `return_costs` is `True`

    The implementation CLOSELY follows Cormen, "Introduction to Algorithms",
    Chapter 15.2, p. 370-378.  Note that Cormen uses 1-based indices.

        cost[i, j] = min([
            cost[prefix] + cost[suffix] + cost_mult(prefix, suffix)
            for k in range(i, j)])

    """
    n = len(arrays)
    p = [a.shape[0] for a in arrays] + [arrays[(-1)].shape[1]]
    m = zeros((n, n), dtype=double)
    s = empty((n, n), dtype=intp)
    for l in range(1, n):
        for i in range(n - l):
            j = i + l
            m[(i, j)] = Inf
            for k in range(i, j):
                q = m[(i, k)] + m[(k + 1, j)] + p[i] * p[(k + 1)] * p[(j + 1)]
                if q < m[(i, j)]:
                    m[(i, j)] = q
                    s[(i, j)] = k

    if return_costs:
        return (s, m)
    return s


def _multi_dot(arrays, order, i, j, out=None):
    """Actually do the multiplication with the given order."""
    if i == j:
        assert out is None
        return arrays[i]
    return dot((_multi_dotarraysorderiorder[(i, j)]), (_multi_dotarraysorder(order[(i, j)] + 1)j),
      out=out)