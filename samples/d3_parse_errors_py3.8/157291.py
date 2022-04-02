# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\polynomial\polyutils.py
"""
Utility classes and functions for the polynomial modules.

This module provides: error and warning objects; a polynomial base class;
and some routines used in both the `polynomial` and `chebyshev` modules.

Error objects
-------------

.. autosummary::
   :toctree: generated/

   PolyError            base class for this sub-package's errors.
   PolyDomainError      raised when domains are mismatched.

Warning objects
---------------

.. autosummary::
   :toctree: generated/

   RankWarning  raised in least-squares fit for rank-deficient matrix.

Base class
----------

.. autosummary::
   :toctree: generated/

   PolyBase Obsolete base class for the polynomial classes. Do not use.

Functions
---------

.. autosummary::
   :toctree: generated/

   as_series    convert list of array_likes into 1-D arrays of common type.
   trimseq      remove trailing zeros.
   trimcoef     remove small trailing coefficients.
   getdomain    return the domain appropriate for a given set of abscissae.
   mapdomain    maps points between domains.
   mapparms     parameters of the linear map between domains.

"""
import operator, functools, warnings, numpy as np
__all__ = [
 'RankWarning', 'PolyError', 'PolyDomainError', 'as_series', 'trimseq',
 'trimcoef', 'getdomain', 'mapdomain', 'mapparms', 'PolyBase']

class RankWarning(UserWarning):
    __doc__ = 'Issued by chebfit when the design matrix is rank deficient.'


class PolyError(Exception):
    __doc__ = 'Base class for errors in this module.'


class PolyDomainError(PolyError):
    __doc__ = "Issued by the generic Poly class when two domains don't match.\n\n    This is raised when an binary operation is passed Poly objects with\n    different domains.\n\n    "


class PolyBase:
    __doc__ = '\n    Base class for all polynomial types.\n\n    Deprecated in numpy 1.9.0, use the abstract\n    ABCPolyBase class instead. Note that the latter\n    requires a number of virtual functions to be\n    implemented.\n\n    '


def trimseq(seq):
    """Remove small Poly series coefficients.

    Parameters
    ----------
    seq : sequence
        Sequence of Poly series coefficients. This routine fails for
        empty sequences.

    Returns
    -------
    series : sequence
        Subsequence with trailing zeros removed. If the resulting sequence
        would be empty, return the first element. The returned sequence may
        or may not be a view.

    Notes
    -----
    Do not lose the type info if the sequence contains unknown objects.

    """
    if len(seq) == 0:
        return seq
    for i in range(len(seq) - 1, -1, -1):
        if seq[i] != 0:
            break
    else:
        return seq[:i + 1]


def as_series(alist, trim=True):
    """
    Return argument as a list of 1-d arrays.

    The returned list contains array(s) of dtype double, complex double, or
    object.  A 1-d argument of shape ``(N,)`` is parsed into ``N`` arrays of
    size one; a 2-d argument of shape ``(M,N)`` is parsed into ``M`` arrays
    of size ``N`` (i.e., is "parsed by row"); and a higher dimensional array
    raises a Value Error if it is not first reshaped into either a 1-d or 2-d
    array.

    Parameters
    ----------
    alist : array_like
        A 1- or 2-d array_like
    trim : boolean, optional
        When True, trailing zeros are removed from the inputs.
        When False, the inputs are passed through intact.

    Returns
    -------
    [a1, a2,...] : list of 1-D arrays
        A copy of the input data as a list of 1-d arrays.

    Raises
    ------
    ValueError
        Raised when `as_series` cannot convert its input to 1-d arrays, or at
        least one of the resulting arrays is empty.

    Examples
    --------
    >>> from numpy.polynomial import polyutils as pu
    >>> a = np.arange(4)
    >>> pu.as_series(a)
    [array([0.]), array([1.]), array([2.]), array([3.])]
    >>> b = np.arange(6).reshape((2,3))
    >>> pu.as_series(b)
    [array([0., 1., 2.]), array([3., 4., 5.])]

    >>> pu.as_series((1, np.arange(3), np.arange(2, dtype=np.float16)))
    [array([1.]), array([0., 1., 2.]), array([0., 1.])]

    >>> pu.as_series([2, [1.1, 0.]])
    [array([2.]), array([1.1])]

    >>> pu.as_series([2, [1.1, 0.]], trim=False)
    [array([2.]), array([1.1, 0. ])]

    """
    arrays = [np.array(a, ndmin=1, copy=False) for a in alist]
    if min([a.size for a in arrays]) == 0:
        raise ValueError('Coefficient array is empty')
    if any((a.ndim != 1 for a in arrays)):
        raise ValueError('Coefficient array is not 1-d')
    if trim:
        arrays = [trimseq(a) for a in arrays]
    if any((a.dtype == np.dtype(object) for a in arrays)):
        ret = []
        for a in arrays:
            if a.dtype != np.dtype(object):
                tmp = np.empty((len(a)), dtype=(np.dtype(object)))
                tmp[:] = a[:]
                ret.append(tmp)
            else:
                ret.append(a.copy())

    else:
        try:
            dtype = (np.common_type)(*arrays)
        except Exception as e:
            try:
                raise ValueError('Coefficient arrays have no common type') from e
            finally:
                e = None
                del e

        else:
            ret = [np.array(a, copy=True, dtype=dtype) for a in arrays]
    return ret


def trimcoef(c, tol=0):
    """
    Remove "small" "trailing" coefficients from a polynomial.

    "Small" means "small in absolute value" and is controlled by the
    parameter `tol`; "trailing" means highest order coefficient(s), e.g., in
    ``[0, 1, 1, 0, 0]`` (which represents ``0 + x + x**2 + 0*x**3 + 0*x**4``)
    both the 3-rd and 4-th order coefficients would be "trimmed."

    Parameters
    ----------
    c : array_like
        1-d array of coefficients, ordered from lowest order to highest.
    tol : number, optional
        Trailing (i.e., highest order) elements with absolute value less
        than or equal to `tol` (default value is zero) are removed.

    Returns
    -------
    trimmed : ndarray
        1-d array with trailing zeros removed.  If the resulting series
        would be empty, a series containing a single zero is returned.

    Raises
    ------
    ValueError
        If `tol` < 0

    See Also
    --------
    trimseq

    Examples
    --------
    >>> from numpy.polynomial import polyutils as pu
    >>> pu.trimcoef((0,0,3,0,5,0,0))
    array([0.,  0.,  3.,  0.,  5.])
    >>> pu.trimcoef((0,0,1e-3,0,1e-5,0,0),1e-3) # item == tol is trimmed
    array([0.])
    >>> i = complex(0,1) # works for complex
    >>> pu.trimcoef((3e-4,1e-3*(1-i),5e-4,2e-5*(1+i)), 1e-3)
    array([0.0003+0.j   , 0.001 -0.001j])

    """
    if tol < 0:
        raise ValueError('tol must be non-negative')
    c, = as_series([c])
    ind, = np.nonzero(np.abs(c) > tol)
    if len(ind) == 0:
        return c[:1] * 0
    return c[:ind[(-1)] + 1].copy()


def getdomain(x):
    """
    Return a domain suitable for given abscissae.

    Find a domain suitable for a polynomial or Chebyshev series
    defined at the values supplied.

    Parameters
    ----------
    x : array_like
        1-d array of abscissae whose domain will be determined.

    Returns
    -------
    domain : ndarray
        1-d array containing two values.  If the inputs are complex, then
        the two returned points are the lower left and upper right corners
        of the smallest rectangle (aligned with the axes) in the complex
        plane containing the points `x`. If the inputs are real, then the
        two points are the ends of the smallest interval containing the
        points `x`.

    See Also
    --------
    mapparms, mapdomain

    Examples
    --------
    >>> from numpy.polynomial import polyutils as pu
    >>> points = np.arange(4)**2 - 5; points
    array([-5, -4, -1,  4])
    >>> pu.getdomain(points)
    array([-5.,  4.])
    >>> c = np.exp(complex(0,1)*np.pi*np.arange(12)/6) # unit circle
    >>> pu.getdomain(c)
    array([-1.-1.j,  1.+1.j])

    """
    x, = as_series([x], trim=False)
    if x.dtype.char in np.typecodes['Complex']:
        rmin, rmax = x.real.min(), x.real.max()
        imin, imax = x.imag.min(), x.imag.max()
        return np.array((complex(rmin, imin), complex(rmax, imax)))
    return np.array((x.min(), x.max()))


def mapparms(old, new):
    """
    Linear map parameters between domains.

    Return the parameters of the linear map ``offset + scale*x`` that maps
    `old` to `new` such that ``old[i] -> new[i]``, ``i = 0, 1``.

    Parameters
    ----------
    old, new : array_like
        Domains. Each domain must (successfully) convert to a 1-d array
        containing precisely two values.

    Returns
    -------
    offset, scale : scalars
        The map ``L(x) = offset + scale*x`` maps the first domain to the
        second.

    See Also
    --------
    getdomain, mapdomain

    Notes
    -----
    Also works for complex numbers, and thus can be used to calculate the
    parameters required to map any line in the complex plane to any other
    line therein.

    Examples
    --------
    >>> from numpy.polynomial import polyutils as pu
    >>> pu.mapparms((-1,1),(-1,1))
    (0.0, 1.0)
    >>> pu.mapparms((1,-1),(-1,1))
    (-0.0, -1.0)
    >>> i = complex(0,1)
    >>> pu.mapparms((-i,-1),(1,i))
    ((1+1j), (1-0j))

    """
    oldlen = old[1] - old[0]
    newlen = new[1] - new[0]
    off = (old[1] * new[0] - old[0] * new[1]) / oldlen
    scl = newlen / oldlen
    return (
     off, scl)


def mapdomain(x, old, new):
    r"""
    Apply linear map to input points.

    The linear map ``offset + scale*x`` that maps the domain `old` to
    the domain `new` is applied to the points `x`.

    Parameters
    ----------
    x : array_like
        Points to be mapped. If `x` is a subtype of ndarray the subtype
        will be preserved.
    old, new : array_like
        The two domains that determine the map.  Each must (successfully)
        convert to 1-d arrays containing precisely two values.

    Returns
    -------
    x_out : ndarray
        Array of points of the same shape as `x`, after application of the
        linear map between the two domains.

    See Also
    --------
    getdomain, mapparms

    Notes
    -----
    Effectively, this implements:

    .. math ::
        x\_out = new[0] + m(x - old[0])

    where

    .. math ::
        m = \frac{new[1]-new[0]}{old[1]-old[0]}

    Examples
    --------
    >>> from numpy.polynomial import polyutils as pu
    >>> old_domain = (-1,1)
    >>> new_domain = (0,2*np.pi)
    >>> x = np.linspace(-1,1,6); x
    array([-1. , -0.6, -0.2,  0.2,  0.6,  1. ])
    >>> x_out = pu.mapdomain(x, old_domain, new_domain); x_out
    array([ 0.        ,  1.25663706,  2.51327412,  3.76991118,  5.02654825, # may vary
            6.28318531])
    >>> x - pu.mapdomain(x_out, new_domain, old_domain)
    array([0., 0., 0., 0., 0., 0.])

    Also works for complex numbers (and thus can be used to map any line in
    the complex plane to any other line therein).

    >>> i = complex(0,1)
    >>> old = (-1 - i, 1 + i)
    >>> new = (-1 + i, 1 - i)
    >>> z = np.linspace(old[0], old[1], 6); z
    array([-1. -1.j , -0.6-0.6j, -0.2-0.2j,  0.2+0.2j,  0.6+0.6j,  1. +1.j ])
    >>> new_z = pu.mapdomain(z, old, new); new_z
    array([-1.0+1.j , -0.6+0.6j, -0.2+0.2j,  0.2-0.2j,  0.6-0.6j,  1.0-1.j ]) # may vary

    """
    x = np.asanyarray(x)
    off, scl = mapparms(old, new)
    return off + scl * x


def _nth_slice(i, ndim):
    sl = [
     np.newaxis] * ndim
    sl[i] = slice(None)
    return tuple(sl)


def _vander_nd(vander_fs, points, degrees):
    r"""
    A generalization of the Vandermonde matrix for N dimensions

    The result is built by combining the results of 1d Vandermonde matrices,

    .. math::
        W[i_0, \ldots, i_M, j_0, \ldots, j_N] = \prod_{k=0}^N{V_k(x_k)[i_0, \ldots, i_M, j_k]}

    where

    .. math::
        N &= \texttt{len(points)} = \texttt{len(degrees)} = \texttt{len(vander\_fs)} \\
        M &= \texttt{points[k].ndim} \\
        V_k &= \texttt{vander\_fs[k]} \\
        x_k &= \texttt{points[k]} \\
        0 \le j_k &\le \texttt{degrees[k]}

    Expanding the one-dimensional :math:`V_k` functions gives:

    .. math::
        W[i_0, \ldots, i_M, j_0, \ldots, j_N] = \prod_{k=0}^N{B_{k, j_k}(x_k[i_0, \ldots, i_M])}

    where :math:`B_{k,m}` is the m'th basis of the polynomial construction used along
    dimension :math:`k`. For a regular polynomial, :math:`B_{k, m}(x) = P_m(x) = x^m`.

    Parameters
    ----------
    vander_fs : Sequence[function(array_like, int) -> ndarray]
        The 1d vander function to use for each axis, such as ``polyvander``
    points : Sequence[array_like]
        Arrays of point coordinates, all of the same shape. The dtypes
        will be converted to either float64 or complex128 depending on
        whether any of the elements are complex. Scalars are converted to
        1-D arrays.
        This must be the same length as `vander_fs`.
    degrees : Sequence[int]
        The maximum degree (inclusive) to use for each axis.
        This must be the same length as `vander_fs`.

    Returns
    -------
    vander_nd : ndarray
        An array of shape ``points[0].shape + tuple(d + 1 for d in degrees)``.
    """
    n_dims = len(vander_fs)
    if n_dims != len(points):
        raise ValueError(f"Expected {n_dims} dimensions of sample points, got {len(points)}")
    if n_dims != len(degrees):
        raise ValueError(f"Expected {n_dims} dimensions of degrees, got {len(degrees)}")
    if n_dims == 0:
        raise ValueError('Unable to guess a dtype or shape when no points are given')
    points = tuple(np.array((tuple(points)), copy=False) + 0.0)
    vander_arrays = (vander_fs[i](points[i], degrees[i])[((Ellipsis, ) + _nth_slice(i, n_dims))] for i in range(n_dims))
    return functools.reduce(operator.mul, vander_arrays)


def _vander_nd_flat(vander_fs, points, degrees):
    """
    Like `_vander_nd`, but flattens the last ``len(degrees)`` axes into a single axis

    Used to implement the public ``<type>vander<n>d`` functions.
    """
    v = _vander_nd(vander_fs, points, degrees)
    return v.reshape(v.shape[:-len(degrees)] + (-1, ))


def _fromroots(line_f, mul_f, roots):
    """
    Helper function used to implement the ``<type>fromroots`` functions.

    Parameters
    ----------
    line_f : function(float, float) -> ndarray
        The ``<type>line`` function, such as ``polyline``
    mul_f : function(array_like, array_like) -> ndarray
        The ``<type>mul`` function, such as ``polymul``
    roots :
        See the ``<type>fromroots`` functions for more detail
    """
    if len(roots) == 0:
        return np.ones(1)
    roots, = as_series([roots], trim=False)
    roots.sort()
    p = [line_f(-r, 1) for r in roots]
    n = len(p)
    while True:
        if n > 1:
            m, r = divmod(n, 2)
            tmp = [mul_f(p[i], p[(i + m)]) for i in range(m)]
            if r:
                tmp[0] = mul_f(tmp[0], p[(-1)])
            p = tmp
            n = m

    return p[0]


def _valnd(val_f, c, *args):
    """
    Helper function used to implement the ``<type>val<n>d`` functions.

    Parameters
    ----------
    val_f : function(array_like, array_like, tensor: bool) -> array_like
        The ``<type>val`` function, such as ``polyval``
    c, args :
        See the ``<type>val<n>d`` functions for more detail
    """
    args = [np.asanyarray(a) for a in args]
    shape0 = args[0].shape
    if not all((a.shape == shape0 for a in args[1:])):
        if len(args) == 3:
            raise ValueError('x, y, z are incompatible')
        elif len(args) == 2:
            raise ValueError('x, y are incompatible')
        else:
            raise ValueError('ordinates are incompatible')
    it = iter(args)
    x0 = next(it)
    c = val_f(x0, c)
    for xi in it:
        c = val_f(xi, c, tensor=False)
    else:
        return c


def _gridnd(val_f, c, *args):
    """
    Helper function used to implement the ``<type>grid<n>d`` functions.

    Parameters
    ----------
    val_f : function(array_like, array_like, tensor: bool) -> array_like
        The ``<type>val`` function, such as ``polyval``
    c, args :
        See the ``<type>grid<n>d`` functions for more detail
    """
    for xi in args:
        c = val_f(xi, c)
    else:
        return c


def _div(mul_f, c1, c2):
    """
    Helper function used to implement the ``<type>div`` functions.

    Implementation uses repeated subtraction of c2 multiplied by the nth basis.
    For some polynomial types, a more efficient approach may be possible.

    Parameters
    ----------
    mul_f : function(array_like, array_like) -> array_like
        The ``<type>mul`` function, such as ``polymul``
    c1, c2 :
        See the ``<type>div`` functions for more detail
    """
    c1, c2 = as_series([c1, c2])
    if c2[(-1)] == 0:
        raise ZeroDivisionError()
    lc1 = len(c1)
    lc2 = len(c2)
    if lc1 < lc2:
        return (c1[:1] * 0, c1)
    if lc2 == 1:
        return (c1 / c2[(-1)], c1[:1] * 0)
    quo = np.empty((lc1 - lc2 + 1), dtype=(c1.dtype))
    rem = c1
    for i in range(lc1 - lc2, -1, -1):
        p = mul_f([0] * i + [1], c2)
        q = rem[(-1)] / p[(-1)]
        rem = rem[:-1] - q * p[:-1]
        quo[i] = q
    else:
        return (
         quo, trimseq(rem))


def _add(c1, c2):
    """ Helper function used to implement the ``<type>add`` functions. """
    c1, c2 = as_series([c1, c2])
    if len(c1) > len(c2):
        c1[:c2.size] += c2
        ret = c1
    else:
        c2[:c1.size] += c1
        ret = c2
    return trimseq(ret)


def _sub(c1, c2):
    """ Helper function used to implement the ``<type>sub`` functions. """
    c1, c2 = as_series([c1, c2])
    if len(c1) > len(c2):
        c1[:c2.size] -= c2
        ret = c1
    else:
        c2 = -c2
        c2[:c1.size] += c1
        ret = c2
    return trimseq(ret)


def _fit(vander_f, x, y, deg, rcond=None, full=False, w=None):
    """
    Helper function used to implement the ``<type>fit`` functions.

    Parameters
    ----------
    vander_f : function(array_like, int) -> ndarray
        The 1d vander function, such as ``polyvander``
    c1, c2 :
        See the ``<type>fit`` functions for more detail
    """
    x = np.asarray(x) + 0.0
    y = np.asarray(y) + 0.0
    deg = np.asarray(deg)
    if not deg.ndim > 1:
        if deg.dtype.kind not in 'iu' or (deg.size == 0):
            raise TypeError('deg must be an int or non-empty 1-D array of int')
        if deg.min() < 0:
            raise ValueError('expected deg >= 0')
        if x.ndim != 1:
            raise TypeError('expected 1D vector for x')
        if x.size == 0:
            raise TypeError('expected non-empty vector for x')
        if y.ndim < 1 or (y.ndim > 2):
            raise TypeError('expected 1D or 2D array for y')
        if len(x) != len(y):
            raise TypeError('expected x and y to have same length')
        if deg.ndim == 0:
            lmax = deg
            order = lmax + 1
            van = vander_f(x, lmax)
        else:
            deg = np.sort(deg)
            lmax = deg[(-1)]
            order = len(deg)
            van = vander_f(x, lmax)[:, deg]
        lhs = van.T
        rhs = y.T
        if w is not None:
            w = np.asarray(w) + 0.0
            if w.ndim != 1:
                raise TypeError('expected 1D vector for w')
            if len(x) != len(w):
                raise TypeError('expected x and w to have same length')
            lhs = lhs * w
            rhs = rhs * w
        if rcond is None:
            rcond = len(x) * np.finfo(x.dtype).eps
        if issubclass(lhs.dtype.type, np.complexfloating):
            scl = np.sqrt((np.square(lhs.real) + np.square(lhs.imag)).sum(1))
        else:
            scl = np.sqrt(np.square(lhs).sum(1))
        scl[scl == 0] = 1
        c, resids, rank, s = np.linalg.lstsq(lhs.T / scl, rhs.T, rcond)
        c = (c.T / scl).T
        if deg.ndim > 0:
            if c.ndim == 2:
                cc = np.zeros((lmax + 1, c.shape[1]), dtype=(c.dtype))
            else:
                cc = np.zeros((lmax + 1), dtype=(c.dtype))
            cc[deg] = c
            c = cc
        if rank != order:
            if not full:
                msg = 'The fit may be poorly conditioned'
                warnings.warn(msg, RankWarning, stacklevel=2)
            if full:
                return (c, [resids, rank, s, rcond])
        return c


def _pow(mul_f, c, pow, maxpower):
    """
    Helper function used to implement the ``<type>pow`` functions.

    Parameters
    ----------
    vander_f : function(array_like, int) -> ndarray
        The 1d vander function, such as ``polyvander``
    pow, maxpower :
        See the ``<type>pow`` functions for more detail
    mul_f : function(array_like, array_like) -> ndarray
        The ``<type>mul`` function, such as ``polymul``
    """
    c, = as_series([c])
    power = int(pow)
    if power != pow or power < 0:
        raise ValueError('Power must be a non-negative integer.')
    elif maxpower is not None and power > maxpower:
        raise ValueError('Power is too large')
    else:
        if power == 0:
            return np.array([1], dtype=(c.dtype))
        if power == 1:
            return c
        prd = c
        for i in range(2, power + 1):
            prd = mul_f(prd, c)
        else:
            return prd


def _deprecate_as_int--- This code section failed: ---

 L. 778         0  SETUP_FINALLY        14  'to 14'

 L. 779         2  LOAD_GLOBAL              operator
                4  LOAD_METHOD              index
                6  LOAD_FAST                'x'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 780        14  DUP_TOP          
               16  LOAD_GLOBAL              TypeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE   140  'to 140'
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY       128  'to 128'

 L. 782        30  SETUP_FINALLY        44  'to 44'

 L. 783        32  LOAD_GLOBAL              int
               34  LOAD_FAST                'x'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'ix'
               40  POP_BLOCK        
               42  JUMP_FORWARD         64  'to 64'
             44_0  COME_FROM_FINALLY    30  '30'

 L. 784        44  DUP_TOP          
               46  LOAD_GLOBAL              TypeError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    62  'to 62'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 785        58  POP_EXCEPT       
               60  JUMP_FORWARD        108  'to 108'
             62_0  COME_FROM            50  '50'
               62  END_FINALLY      
             64_0  COME_FROM            42  '42'

 L. 787        64  LOAD_FAST                'ix'
               66  LOAD_FAST                'x'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE   108  'to 108'

 L. 788        72  LOAD_GLOBAL              warnings
               74  LOAD_ATTR                warn

 L. 789        76  LOAD_STR                 'In future, this will raise TypeError, as '
               78  LOAD_FAST                'desc'
               80  FORMAT_VALUE          0  ''
               82  LOAD_STR                 ' will need to be an integer not just an integral float.'
               84  BUILD_STRING_3        3 

 L. 791        86  LOAD_GLOBAL              DeprecationWarning

 L. 792        88  LOAD_CONST               3

 L. 788        90  LOAD_CONST               ('stacklevel',)
               92  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               94  POP_TOP          

 L. 794        96  LOAD_FAST                'ix'
               98  ROT_FOUR         
              100  POP_BLOCK        
              102  POP_EXCEPT       
              104  CALL_FINALLY        128  'to 128'
              106  RETURN_VALUE     
            108_0  COME_FROM            70  '70'
            108_1  COME_FROM            60  '60'

 L. 796       108  LOAD_GLOBAL              TypeError
              110  LOAD_FAST                'desc'
              112  FORMAT_VALUE          0  ''
              114  LOAD_STR                 ' must be an integer'
              116  BUILD_STRING_2        2 
              118  CALL_FUNCTION_1       1  ''
              120  LOAD_FAST                'e'
              122  RAISE_VARARGS_2       2  'exception instance with __cause__'
              124  POP_BLOCK        
              126  BEGIN_FINALLY    
            128_0  COME_FROM           104  '104'
            128_1  COME_FROM_FINALLY    28  '28'
              128  LOAD_CONST               None
              130  STORE_FAST               'e'
              132  DELETE_FAST              'e'
              134  END_FINALLY      
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM            20  '20'
              140  END_FINALLY      
            142_0  COME_FROM           138  '138'

Parse error at or near `POP_BLOCK' instruction at offset 100