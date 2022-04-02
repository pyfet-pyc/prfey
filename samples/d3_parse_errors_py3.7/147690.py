# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\ma\core.py
"""
numpy.ma : a package to handle missing or invalid values.

This package was initially written for numarray by Paul F. Dubois
at Lawrence Livermore National Laboratory.
In 2006, the package was completely rewritten by Pierre Gerard-Marchant
(University of Georgia) to make the MaskedArray class a subclass of ndarray,
and to improve support of structured arrays.

Copyright 1999, 2000, 2001 Regents of the University of California.
Released for unlimited redistribution.

* Adapted for numpy_core 2005 by Travis Oliphant and (mainly) Paul Dubois.
* Subclassing of the base `ndarray` 2006 by Pierre Gerard-Marchant
  (pgmdevlist_AT_gmail_DOT_com)
* Improvements suggested by Reggie Dugard (reggie_AT_merfinllc_DOT_com)

.. moduleauthor:: Pierre Gerard-Marchant

"""
import builtins, inspect, operator, warnings, textwrap, re
from functools import reduce
import numpy as np
import numpy.core.umath as umath
import numpy.core.numerictypes as ntypes
from numpy import ndarray, amax, amin, iscomplexobj, bool_, _NoValue
from numpy import array as narray
from numpy.lib.function_base import angle
from numpy.compat import getargspec, formatargspec, long, unicode, bytes
from numpy import expand_dims
from numpy.core.numeric import normalize_axis_tuple
from numpy.core._internal import recursive
from numpy.compat import pickle
__all__ = [
 'MAError', 'MaskError', 'MaskType', 'MaskedArray', 'abs', 'absolute',
 'add', 'all', 'allclose', 'allequal', 'alltrue', 'amax', 'amin',
 'angle', 'anom', 'anomalies', 'any', 'append', 'arange', 'arccos',
 'arccosh', 'arcsin', 'arcsinh', 'arctan', 'arctan2', 'arctanh',
 'argmax', 'argmin', 'argsort', 'around', 'array', 'asanyarray',
 'asarray', 'bitwise_and', 'bitwise_or', 'bitwise_xor', 'bool_', 'ceil',
 'choose', 'clip', 'common_fill_value', 'compress', 'compressed',
 'concatenate', 'conjugate', 'convolve', 'copy', 'correlate', 'cos', 'cosh',
 'count', 'cumprod', 'cumsum', 'default_fill_value', 'diag', 'diagonal',
 'diff', 'divide', 'empty', 'empty_like', 'equal', 'exp',
 'expand_dims', 'fabs', 'filled', 'fix_invalid', 'flatten_mask',
 'flatten_structured_array', 'floor', 'floor_divide', 'fmod',
 'frombuffer', 'fromflex', 'fromfunction', 'getdata', 'getmask',
 'getmaskarray', 'greater', 'greater_equal', 'harden_mask', 'hypot',
 'identity', 'ids', 'indices', 'inner', 'innerproduct', 'isMA',
 'isMaskedArray', 'is_mask', 'is_masked', 'isarray', 'left_shift',
 'less', 'less_equal', 'log', 'log10', 'log2',
 'logical_and', 'logical_not', 'logical_or', 'logical_xor', 'make_mask',
 'make_mask_descr', 'make_mask_none', 'mask_or', 'masked',
 'masked_array', 'masked_equal', 'masked_greater',
 'masked_greater_equal', 'masked_inside', 'masked_invalid',
 'masked_less', 'masked_less_equal', 'masked_not_equal',
 'masked_object', 'masked_outside', 'masked_print_option',
 'masked_singleton', 'masked_values', 'masked_where', 'max', 'maximum',
 'maximum_fill_value', 'mean', 'min', 'minimum', 'minimum_fill_value',
 'mod', 'multiply', 'mvoid', 'ndim', 'negative', 'nomask', 'nonzero',
 'not_equal', 'ones', 'outer', 'outerproduct', 'power', 'prod',
 'product', 'ptp', 'put', 'putmask', 'ravel', 'remainder',
 'repeat', 'reshape', 'resize', 'right_shift', 'round', 'round_',
 'set_fill_value', 'shape', 'sin', 'sinh', 'size', 'soften_mask',
 'sometrue', 'sort', 'sqrt', 'squeeze', 'std', 'subtract', 'sum',
 'swapaxes', 'take', 'tan', 'tanh', 'trace', 'transpose', 'true_divide',
 'var', 'where', 'zeros']
MaskType = np.bool_
nomask = MaskType(0)

class MaskedArrayFutureWarning(FutureWarning):
    pass


def _deprecate_argsort_axis(arr):
    """
    Adjust the axis passed to argsort, warning if necessary

    Parameters
    ----------
    arr
        The array which argsort was called on

    np.ma.argsort has a long-term bug where the default of the axis argument
    is wrong (gh-8701), which now must be kept for backwards compatibility.
    Thankfully, this only makes a difference when arrays are 2- or more-
    dimensional, so we only need a warning then.
    """
    if arr.ndim <= 1:
        return -1
    warnings.warn('In the future the default for argsort will be axis=-1, not the current None, to match its documentation and np.argsort. Explicitly pass -1 or None to silence this warning.',
      MaskedArrayFutureWarning,
      stacklevel=3)
    return


def doc_note(initialdoc, note):
    """
    Adds a Notes section to an existing docstring.

    """
    if initialdoc is None:
        return
    if note is None:
        return initialdoc
    notesplit = re.split('\\n\\s*?Notes\\n\\s*?-----', inspect.cleandoc(initialdoc))
    notedoc = '\n\nNotes\n-----\n%s\n' % inspect.cleandoc(note)
    return ''.join(notesplit[:1] + [notedoc] + notesplit[1:])


def get_object_signature(obj):
    """
    Get the signature from obj

    """
    try:
        sig = formatargspec(*getargspec(obj))
    except TypeError:
        sig = ''

    return sig


class MAError(Exception):
    __doc__ = '\n    Class for masked array related errors.\n\n    '


class MaskError(MAError):
    __doc__ = '\n    Class for mask related errors.\n\n    '


default_filler = {'b':True, 
 'c':complex(1e+20, 0.0), 
 'f':1e+20, 
 'i':999999, 
 'O':'?', 
 'S':'N/A', 
 'u':999999, 
 'V':'???', 
 'U':'N/A'}
for v in ('Y', 'M', 'W', 'D', 'h', 'm', 's', 'ms', 'us', 'ns', 'ps', 'fs', 'as'):
    default_filler['M8[' + v + ']'] = np.datetime64('NaT', v)
    default_filler['m8[' + v + ']'] = np.timedelta64('NaT', v)

float_types_list = [np.half, np.single, np.double, np.longdouble,
 np.csingle, np.cdouble, np.clongdouble]
max_filler = ntypes._minvals
max_filler.update([(k, -np.inf) for k in float_types_list[:4]])
max_filler.update([(k, complex(-np.inf, -np.inf)) for k in float_types_list[-3:]])
min_filler = ntypes._maxvals
min_filler.update([(k, +np.inf) for k in float_types_list[:4]])
min_filler.update([(k, complex(+np.inf, +np.inf)) for k in float_types_list[-3:]])
del float_types_list

def _recursive_fill_value(dtype, f):
    """
    Recursively produce a fill value for `dtype`, calling f on scalar dtypes
    """
    if dtype.names is not None:
        vals = tuple((_recursive_fill_value(dtype[name], f) for name in dtype.names))
        return np.array(vals, dtype=dtype)[()]
    if dtype.subdtype:
        subtype, shape = dtype.subdtype
        subval = _recursive_fill_value(subtype, f)
        return np.full(shape, subval)
    return f(dtype)


def _get_dtype_of(obj):
    """ Convert the argument for *_fill_value into a dtype """
    if isinstance(obj, np.dtype):
        return obj
    if hasattr(obj, 'dtype'):
        return obj.dtype
    return np.asanyarray(obj).dtype


def default_fill_value(obj):
    """
    Return the default fill value for the argument object.

    The default filling value depends on the datatype of the input
    array or the type of the input scalar:

       ========  ========
       datatype  default
       ========  ========
       bool      True
       int       999999
       float     1.e20
       complex   1.e20+0j
       object    '?'
       string    'N/A'
       ========  ========

    For structured types, a structured scalar is returned, with each field the
    default fill value for its type.

    For subarray types, the fill value is an array of the same size containing
    the default scalar fill value.

    Parameters
    ----------
    obj : ndarray, dtype or scalar
        The array data-type or scalar for which the default fill value
        is returned.

    Returns
    -------
    fill_value : scalar
        The default fill value.

    Examples
    --------
    >>> np.ma.default_fill_value(1)
    999999
    >>> np.ma.default_fill_value(np.array([1.1, 2., np.pi]))
    1e+20
    >>> np.ma.default_fill_value(np.dtype(complex))
    (1e+20+0j)

    """

    def _scalar_fill_value(dtype):
        if dtype.kind in 'Mm':
            return default_filler.get(dtype.str[1:], '?')
        return default_filler.get(dtype.kind, '?')

    dtype = _get_dtype_of(obj)
    return _recursive_fill_value(dtype, _scalar_fill_value)


def _extremum_fill_value(obj, extremum, extremum_name):

    def _scalar_fill_value(dtype):
        try:
            return extremum[dtype]
        except KeyError as e:
            try:
                raise TypeError(f"Unsuitable type {dtype} for calculating {extremum_name}.") from None
            finally:
                e = None
                del e

    dtype = _get_dtype_of(obj)
    return _recursive_fill_value(dtype, _scalar_fill_value)


def minimum_fill_value(obj):
    """
    Return the maximum value that can be represented by the dtype of an object.

    This function is useful for calculating a fill value suitable for
    taking the minimum of an array with a given dtype.

    Parameters
    ----------
    obj : ndarray, dtype or scalar
        An object that can be queried for it's numeric type.

    Returns
    -------
    val : scalar
        The maximum representable value.

    Raises
    ------
    TypeError
        If `obj` isn't a suitable numeric type.

    See Also
    --------
    maximum_fill_value : The inverse function.
    set_fill_value : Set the filling value of a masked array.
    MaskedArray.fill_value : Return current fill value.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.int8()
    >>> ma.minimum_fill_value(a)
    127
    >>> a = np.int32()
    >>> ma.minimum_fill_value(a)
    2147483647

    An array of numeric data can also be passed.

    >>> a = np.array([1, 2, 3], dtype=np.int8)
    >>> ma.minimum_fill_value(a)
    127
    >>> a = np.array([1, 2, 3], dtype=np.float32)
    >>> ma.minimum_fill_value(a)
    inf

    """
    return _extremum_fill_value(obj, min_filler, 'minimum')


def maximum_fill_value(obj):
    """
    Return the minimum value that can be represented by the dtype of an object.

    This function is useful for calculating a fill value suitable for
    taking the maximum of an array with a given dtype.

    Parameters
    ----------
    obj : ndarray, dtype or scalar
        An object that can be queried for it's numeric type.

    Returns
    -------
    val : scalar
        The minimum representable value.

    Raises
    ------
    TypeError
        If `obj` isn't a suitable numeric type.

    See Also
    --------
    minimum_fill_value : The inverse function.
    set_fill_value : Set the filling value of a masked array.
    MaskedArray.fill_value : Return current fill value.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.int8()
    >>> ma.maximum_fill_value(a)
    -128
    >>> a = np.int32()
    >>> ma.maximum_fill_value(a)
    -2147483648

    An array of numeric data can also be passed.

    >>> a = np.array([1, 2, 3], dtype=np.int8)
    >>> ma.maximum_fill_value(a)
    -128
    >>> a = np.array([1, 2, 3], dtype=np.float32)
    >>> ma.maximum_fill_value(a)
    -inf

    """
    return _extremum_fill_value(obj, max_filler, 'maximum')


def _recursive_set_fill_value(fillvalue, dt):
    """
    Create a fill value for a structured dtype.

    Parameters
    ----------
    fillvalue: scalar or array_like
        Scalar or array representing the fill value. If it is of shorter
        length than the number of fields in dt, it will be resized.
    dt: dtype
        The structured dtype for which to create the fill value.

    Returns
    -------
    val: tuple
        A tuple of values corresponding to the structured fill value.

    """
    fillvalue = np.resize(fillvalue, len(dt.names))
    output_value = []
    for fval, name in zip(fillvalue, dt.names):
        cdtype = dt[name]
        if cdtype.subdtype:
            cdtype = cdtype.subdtype[0]
        if cdtype.names is not None:
            output_value.append(tuple(_recursive_set_fill_value(fval, cdtype)))
        else:
            output_value.append(np.array(fval, dtype=cdtype).item())

    return tuple(output_value)


def _check_fill_value(fill_value, ndtype):
    """
    Private function validating the given `fill_value` for the given dtype.

    If fill_value is None, it is set to the default corresponding to the dtype.

    If fill_value is not None, its value is forced to the given dtype.

    The result is always a 0d array.

    """
    ndtype = np.dtype(ndtype)
    if fill_value is None:
        fill_value = default_fill_value(ndtype)
    else:
        pass
    if ndtype.names is not None:
        if isinstance(fill_value, (ndarray, np.void)):
            try:
                fill_value = np.array(fill_value, copy=False, dtype=ndtype)
            except ValueError as e:
                try:
                    err_msg = 'Unable to transform %s to dtype %s'
                    raise ValueError(err_msg % (fill_value, ndtype)) from e
                finally:
                    e = None
                    del e

        else:
            fill_value = np.asarray(fill_value, dtype=object)
            fill_value = np.array((_recursive_set_fill_value(fill_value, ndtype)), dtype=ndtype)
    elif isinstance(fill_value, str) and ndtype.char not in 'OSVU':
        err_msg = 'Cannot set fill value of string with array of dtype %s'
        raise TypeError(err_msg % ndtype)
    else:
        try:
            fill_value = np.array(fill_value, copy=False, dtype=ndtype)
        except (OverflowError, ValueError) as e:
            try:
                err_msg = 'Cannot convert fill_value %s to dtype %s'
                raise TypeError(err_msg % (fill_value, ndtype)) from e
            finally:
                e = None
                del e

    return np.array(fill_value)


def set_fill_value(a, fill_value):
    """
    Set the filling value of a, if a is a masked array.

    This function changes the fill value of the masked array `a` in place.
    If `a` is not a masked array, the function returns silently, without
    doing anything.

    Parameters
    ----------
    a : array_like
        Input array.
    fill_value : dtype
        Filling value. A consistency test is performed to make sure
        the value is compatible with the dtype of `a`.

    Returns
    -------
    None
        Nothing returned by this function.

    See Also
    --------
    maximum_fill_value : Return the default fill value for a dtype.
    MaskedArray.fill_value : Return current fill value.
    MaskedArray.set_fill_value : Equivalent method.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.arange(5)
    >>> a
    array([0, 1, 2, 3, 4])
    >>> a = ma.masked_where(a < 3, a)
    >>> a
    masked_array(data=[--, --, --, 3, 4],
                 mask=[ True,  True,  True, False, False],
           fill_value=999999)
    >>> ma.set_fill_value(a, -999)
    >>> a
    masked_array(data=[--, --, --, 3, 4],
                 mask=[ True,  True,  True, False, False],
           fill_value=-999)

    Nothing happens if `a` is not a masked array.

    >>> a = list(range(5))
    >>> a
    [0, 1, 2, 3, 4]
    >>> ma.set_fill_value(a, 100)
    >>> a
    [0, 1, 2, 3, 4]
    >>> a = np.arange(5)
    >>> a
    array([0, 1, 2, 3, 4])
    >>> ma.set_fill_value(a, 100)
    >>> a
    array([0, 1, 2, 3, 4])

    """
    if isinstance(a, MaskedArray):
        a.set_fill_value(fill_value)


def get_fill_value(a):
    """
    Return the filling value of a, if any.  Otherwise, returns the
    default filling value for that type.

    """
    if isinstance(a, MaskedArray):
        result = a.fill_value
    else:
        result = default_fill_value(a)
    return result


def common_fill_value(a, b):
    """
    Return the common filling value of two masked arrays, if any.

    If ``a.fill_value == b.fill_value``, return the fill value,
    otherwise return None.

    Parameters
    ----------
    a, b : MaskedArray
        The masked arrays for which to compare fill values.

    Returns
    -------
    fill_value : scalar or None
        The common fill value, or None.

    Examples
    --------
    >>> x = np.ma.array([0, 1.], fill_value=3)
    >>> y = np.ma.array([0, 1.], fill_value=3)
    >>> np.ma.common_fill_value(x, y)
    3.0

    """
    t1 = get_fill_value(a)
    t2 = get_fill_value(b)
    if t1 == t2:
        return t1


def filled(a, fill_value=None):
    """
    Return input as an array with masked data replaced by a fill value.

    If `a` is not a `MaskedArray`, `a` itself is returned.
    If `a` is a `MaskedArray` and `fill_value` is None, `fill_value` is set to
    ``a.fill_value``.

    Parameters
    ----------
    a : MaskedArray or array_like
        An input object.
    fill_value : array_like, optional.
        Can be scalar or non-scalar. If non-scalar, the
        resulting filled array should be broadcastable
        over input array. Default is None.

    Returns
    -------
    a : ndarray
        The filled array.

    See Also
    --------
    compressed

    Examples
    --------
    >>> x = np.ma.array(np.arange(9).reshape(3, 3), mask=[[1, 0, 0],
    ...                                                   [1, 0, 0],
    ...                                                   [0, 0, 0]])
    >>> x.filled()
    array([[999999,      1,      2],
           [999999,      4,      5],
           [     6,      7,      8]])
    >>> x.filled(fill_value=333)
    array([[333,   1,   2],
           [333,   4,   5],
           [  6,   7,   8]])
    >>> x.filled(fill_value=np.arange(3))
    array([[0, 1, 2],
           [0, 4, 5],
           [6, 7, 8]])

    """
    if hasattr(a, 'filled'):
        return a.filled(fill_value)
    if isinstance(a, ndarray):
        return a
    if isinstance(a, dict):
        return np.array(a, 'O')
    return np.array(a)


def get_masked_subclass(*arrays):
    """
    Return the youngest subclass of MaskedArray from a list of (masked) arrays.

    In case of siblings, the first listed takes over.

    """
    if len(arrays) == 1:
        arr = arrays[0]
        if isinstance(arr, MaskedArray):
            rcls = type(arr)
        else:
            rcls = MaskedArray
    else:
        arrcls = [type(a) for a in arrays]
        rcls = arrcls[0]
        if not issubclass(rcls, MaskedArray):
            rcls = MaskedArray
        for cls in arrcls[1:]:
            if issubclass(cls, rcls):
                rcls = cls

    if rcls.__name__ == 'MaskedConstant':
        return MaskedArray
    return rcls


def getdata(a, subok=True):
    """
    Return the data of a masked array as an ndarray.

    Return the data of `a` (if any) as an ndarray if `a` is a ``MaskedArray``,
    else return `a` as a ndarray or subclass (depending on `subok`) if not.

    Parameters
    ----------
    a : array_like
        Input ``MaskedArray``, alternatively a ndarray or a subclass thereof.
    subok : bool
        Whether to force the output to be a `pure` ndarray (False) or to
        return a subclass of ndarray if appropriate (True, default).

    See Also
    --------
    getmask : Return the mask of a masked array, or nomask.
    getmaskarray : Return the mask of a masked array, or full array of False.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = ma.masked_equal([[1,2],[3,4]], 2)
    >>> a
    masked_array(
      data=[[1, --],
            [3, 4]],
      mask=[[False,  True],
            [False, False]],
      fill_value=2)
    >>> ma.getdata(a)
    array([[1, 2],
           [3, 4]])

    Equivalently use the ``MaskedArray`` `data` attribute.

    >>> a.data
    array([[1, 2],
           [3, 4]])

    """
    try:
        data = a._data
    except AttributeError:
        data = np.array(a, copy=False, subok=subok)

    if not subok:
        return data.view(ndarray)
    return data


get_data = getdata

def fix_invalid(a, mask=nomask, copy=True, fill_value=None):
    """
    Return input with invalid data masked and replaced by a fill value.

    Invalid data means values of `nan`, `inf`, etc.

    Parameters
    ----------
    a : array_like
        Input array, a (subclass of) ndarray.
    mask : sequence, optional
        Mask. Must be convertible to an array of booleans with the same
        shape as `data`. True indicates a masked (i.e. invalid) data.
    copy : bool, optional
        Whether to use a copy of `a` (True) or to fix `a` in place (False).
        Default is True.
    fill_value : scalar, optional
        Value used for fixing invalid data. Default is None, in which case
        the ``a.fill_value`` is used.

    Returns
    -------
    b : MaskedArray
        The input array with invalid entries fixed.

    Notes
    -----
    A copy is performed by default.

    Examples
    --------
    >>> x = np.ma.array([1., -1, np.nan, np.inf], mask=[1] + [0]*3)
    >>> x
    masked_array(data=[--, -1.0, nan, inf],
                 mask=[ True, False, False, False],
           fill_value=1e+20)
    >>> np.ma.fix_invalid(x)
    masked_array(data=[--, -1.0, --, --],
                 mask=[ True, False,  True,  True],
           fill_value=1e+20)

    >>> fixed = np.ma.fix_invalid(x)
    >>> fixed.data
    array([ 1.e+00, -1.e+00,  1.e+20,  1.e+20])
    >>> x.data
    array([ 1., -1., nan, inf])

    """
    a = masked_array(a, copy=copy, mask=mask, subok=True)
    invalid = np.logical_not(np.isfinite(a._data))
    if not invalid.any():
        return a
    a._mask |= invalid
    if fill_value is None:
        fill_value = a.fill_value
    a._data[invalid] = fill_value
    return a


def is_string_or_list_of_strings(val):
    return (isinstance(val, str)) or ((isinstance(val, list)) and (val and builtins.all((isinstance(s, str) for s in val))))


ufunc_domain = {}
ufunc_fills = {}

class _DomainCheckInterval:
    __doc__ = '\n    Define a valid interval, so that :\n\n    ``domain_check_interval(a,b)(x) == True`` where\n    ``x < a`` or ``x > b``.\n\n    '

    def __init__(self, a, b):
        """domain_check_interval(a,b)(x) = true where x < a or y > b"""
        if a > b:
            a, b = b, a
        self.a = a
        self.b = b

    def __call__(self, x):
        """Execute the call behavior."""
        with np.errstate(invalid='ignore'):
            return umath.logical_or(umath.greater(x, self.b), umath.less(x, self.a))


class _DomainTan:
    __doc__ = '\n    Define a valid interval for the `tan` function, so that:\n\n    ``domain_tan(eps) = True`` where ``abs(cos(x)) < eps``\n\n    '

    def __init__(self, eps):
        """domain_tan(eps) = true where abs(cos(x)) < eps)"""
        self.eps = eps

    def __call__(self, x):
        """Executes the call behavior."""
        with np.errstate(invalid='ignore'):
            return umath.less(umath.absolute(umath.cos(x)), self.eps)


class _DomainSafeDivide:
    __doc__ = '\n    Define a domain for safe division.\n\n    '

    def __init__(self, tolerance=None):
        self.tolerance = tolerance

    def __call__(self, a, b):
        if self.tolerance is None:
            self.tolerance = np.finfo(float).tiny
        a, b = np.asarray(a), np.asarray(b)
        with np.errstate(invalid='ignore'):
            return umath.absolute(a) * self.tolerance >= umath.absolute(b)


class _DomainGreater:
    __doc__ = '\n    DomainGreater(v)(x) is True where x <= v.\n\n    '

    def __init__(self, critical_value):
        """DomainGreater(v)(x) = true where x <= v"""
        self.critical_value = critical_value

    def __call__(self, x):
        """Executes the call behavior."""
        with np.errstate(invalid='ignore'):
            return umath.less_equal(x, self.critical_value)


class _DomainGreaterEqual:
    __doc__ = '\n    DomainGreaterEqual(v)(x) is True where x < v.\n\n    '

    def __init__(self, critical_value):
        """DomainGreaterEqual(v)(x) = true where x < v"""
        self.critical_value = critical_value

    def __call__(self, x):
        """Executes the call behavior."""
        with np.errstate(invalid='ignore'):
            return umath.less(x, self.critical_value)


class _MaskedUFunc:

    def __init__(self, ufunc):
        self.f = ufunc
        self.__doc__ = ufunc.__doc__
        self.__name__ = ufunc.__name__

    def __str__(self):
        return f"Masked version of {self.f}"


class _MaskedUnaryOperation(_MaskedUFunc):
    __doc__ = '\n    Defines masked version of unary operations, where invalid values are\n    pre-masked.\n\n    Parameters\n    ----------\n    mufunc : callable\n        The function for which to define a masked version. Made available\n        as ``_MaskedUnaryOperation.f``.\n    fill : scalar, optional\n        Filling value, default is 0.\n    domain : class instance\n        Domain for the function. Should be one of the ``_Domain*``\n        classes. Default is None.\n\n    '

    def __init__(self, mufunc, fill=0, domain=None):
        super(_MaskedUnaryOperation, self).__init__(mufunc)
        self.fill = fill
        self.domain = domain
        ufunc_domain[mufunc] = domain
        ufunc_fills[mufunc] = fill

    def __call__(self, a, *args, **kwargs):
        """
        Execute the call behavior.

        """
        d = getdata(a)
        if self.domain is not None:
            with np.errstate(divide='ignore', invalid='ignore'):
                result = (self.f)(d, *args, **kwargs)
            m = ~umath.isfinite(result)
            m |= self.domain(d)
            m |= getmask(a)
        else:
            with np.errstate(divide='ignore', invalid='ignore'):
                result = (self.f)(d, *args, **kwargs)
            m = getmask(a)
        if not result.ndim:
            if m:
                return masked
            return result
        if m is not nomask:
            try:
                np.copyto(result, d, where=m)
            except TypeError:
                pass

            masked_result = result.view(get_masked_subclass(a))
            masked_result._mask = m
            masked_result._update_from(a)
            return masked_result


class _MaskedBinaryOperation(_MaskedUFunc):
    __doc__ = '\n    Define masked version of binary operations, where invalid\n    values are pre-masked.\n\n    Parameters\n    ----------\n    mbfunc : function\n        The function for which to define a masked version. Made available\n        as ``_MaskedBinaryOperation.f``.\n    domain : class instance\n        Default domain for the function. Should be one of the ``_Domain*``\n        classes. Default is None.\n    fillx : scalar, optional\n        Filling value for the first argument, default is 0.\n    filly : scalar, optional\n        Filling value for the second argument, default is 0.\n\n    '

    def __init__(self, mbfunc, fillx=0, filly=0):
        """
        abfunc(fillx, filly) must be defined.

        abfunc(x, filly) = x for all x to enable reduce.

        """
        super(_MaskedBinaryOperation, self).__init__(mbfunc)
        self.fillx = fillx
        self.filly = filly
        ufunc_domain[mbfunc] = None
        ufunc_fills[mbfunc] = (fillx, filly)

    def __call__(self, a, b, *args, **kwargs):
        """
        Execute the call behavior.

        """
        da, db = getdata(a), getdata(b)
        with np.errstate():
            np.seterr(divide='ignore', invalid='ignore')
            result = (self.f)(da, db, *args, **kwargs)
        ma, mb = getmask(a), getmask(b)
        if ma is nomask:
            if mb is nomask:
                m = nomask
            else:
                m = umath.logical_or(getmaskarray(a), mb)
        elif mb is nomask:
            m = umath.logical_or(ma, getmaskarray(b))
        else:
            m = umath.logical_or(ma, mb)
        if not result.ndim:
            if m:
                return masked
            return result
        if not m is not nomask or m.any():
            try:
                np.copyto(result, da, casting='unsafe', where=m)
            except Exception:
                pass

            masked_result = result.view(get_masked_subclass(a, b))
            masked_result._mask = m
            if isinstance(a, MaskedArray):
                masked_result._update_from(a)
            elif isinstance(b, MaskedArray):
                masked_result._update_from(b)
            return masked_result

    def reduce(self, target, axis=0, dtype=None):
        """
        Reduce `target` along the given `axis`.

        """
        tclass = get_masked_subclass(target)
        m = getmask(target)
        t = filled(target, self.filly)
        if t.shape == ():
            t = t.reshape(1)
            if m is not nomask:
                m = make_mask(m, copy=True)
                m.shape = (1, )
        if m is nomask:
            tr = self.f.reduce(t, axis)
            mr = nomask
        else:
            tr = self.f.reduce(t, axis, dtype=(dtype or t.dtype))
            mr = umath.logical_and.reduce(m, axis)
        if not tr.shape:
            if mr:
                return masked
            return tr
        masked_tr = tr.view(tclass)
        masked_tr._mask = mr
        return masked_tr

    def outer(self, a, b):
        """
        Return the function applied to the outer product of a and b.

        """
        da, db = getdata(a), getdata(b)
        d = self.f.outer(da, db)
        ma = getmask(a)
        mb = getmask(b)
        if ma is nomask and mb is nomask:
            m = nomask
        else:
            ma = getmaskarray(a)
            mb = getmaskarray(b)
            m = umath.logical_or.outer(ma, mb)
        if not m.ndim:
            if m:
                return masked
        if m is not nomask:
            np.copyto(d, da, where=m)
        if not d.shape:
            return d
        masked_d = d.view(get_masked_subclass(a, b))
        masked_d._mask = m
        return masked_d

    def accumulate(self, target, axis=0):
        """Accumulate `target` along `axis` after filling with y fill
        value.

        """
        tclass = get_masked_subclass(target)
        t = filled(target, self.filly)
        result = self.f.accumulate(t, axis)
        masked_result = result.view(tclass)
        return masked_result


class _DomainedBinaryOperation(_MaskedUFunc):
    __doc__ = '\n    Define binary operations that have a domain, like divide.\n\n    They have no reduce, outer or accumulate.\n\n    Parameters\n    ----------\n    mbfunc : function\n        The function for which to define a masked version. Made available\n        as ``_DomainedBinaryOperation.f``.\n    domain : class instance\n        Default domain for the function. Should be one of the ``_Domain*``\n        classes.\n    fillx : scalar, optional\n        Filling value for the first argument, default is 0.\n    filly : scalar, optional\n        Filling value for the second argument, default is 0.\n\n    '

    def __init__(self, dbfunc, domain, fillx=0, filly=0):
        """abfunc(fillx, filly) must be defined.
           abfunc(x, filly) = x for all x to enable reduce.
        """
        super(_DomainedBinaryOperation, self).__init__(dbfunc)
        self.domain = domain
        self.fillx = fillx
        self.filly = filly
        ufunc_domain[dbfunc] = domain
        ufunc_fills[dbfunc] = (fillx, filly)

    def __call__(self, a, b, *args, **kwargs):
        """Execute the call behavior."""
        da, db = getdata(a), getdata(b)
        with np.errstate(divide='ignore', invalid='ignore'):
            result = (self.f)(da, db, *args, **kwargs)
        m = ~umath.isfinite(result)
        m |= getmask(a)
        m |= getmask(b)
        domain = ufunc_domain.get(self.f, None)
        if domain is not None:
            m |= domain(da, db)
        if not m.ndim:
            if m:
                return masked
            return result
        try:
            np.copyto(result, 0, casting='unsafe', where=m)
            masked_da = umath.multiply(m, da)
            if np.can_cast((masked_da.dtype), (result.dtype), casting='safe'):
                result += masked_da
        except Exception:
            pass

        masked_result = result.view(get_masked_subclass(a, b))
        masked_result._mask = m
        if isinstance(a, MaskedArray):
            masked_result._update_from(a)
        elif isinstance(b, MaskedArray):
            masked_result._update_from(b)
        return masked_result


exp = _MaskedUnaryOperation(umath.exp)
conjugate = _MaskedUnaryOperation(umath.conjugate)
sin = _MaskedUnaryOperation(umath.sin)
cos = _MaskedUnaryOperation(umath.cos)
arctan = _MaskedUnaryOperation(umath.arctan)
arcsinh = _MaskedUnaryOperation(umath.arcsinh)
sinh = _MaskedUnaryOperation(umath.sinh)
cosh = _MaskedUnaryOperation(umath.cosh)
tanh = _MaskedUnaryOperation(umath.tanh)
abs = absolute = _MaskedUnaryOperation(umath.absolute)
angle = _MaskedUnaryOperation(angle)
fabs = _MaskedUnaryOperation(umath.fabs)
negative = _MaskedUnaryOperation(umath.negative)
floor = _MaskedUnaryOperation(umath.floor)
ceil = _MaskedUnaryOperation(umath.ceil)
around = _MaskedUnaryOperation(np.round_)
logical_not = _MaskedUnaryOperation(umath.logical_not)
sqrt = _MaskedUnaryOperation(umath.sqrt, 0.0, _DomainGreaterEqual(0.0))
log = _MaskedUnaryOperation(umath.log, 1.0, _DomainGreater(0.0))
log2 = _MaskedUnaryOperation(umath.log2, 1.0, _DomainGreater(0.0))
log10 = _MaskedUnaryOperation(umath.log10, 1.0, _DomainGreater(0.0))
tan = _MaskedUnaryOperation(umath.tan, 0.0, _DomainTan(1e-35))
arcsin = _MaskedUnaryOperation(umath.arcsin, 0.0, _DomainCheckInterval(-1.0, 1.0))
arccos = _MaskedUnaryOperation(umath.arccos, 0.0, _DomainCheckInterval(-1.0, 1.0))
arccosh = _MaskedUnaryOperation(umath.arccosh, 1.0, _DomainGreaterEqual(1.0))
arctanh = _MaskedUnaryOperation(umath.arctanh, 0.0, _DomainCheckInterval(-0.999999999999999, 0.999999999999999))
add = _MaskedBinaryOperation(umath.add)
subtract = _MaskedBinaryOperation(umath.subtract)
multiply = _MaskedBinaryOperation(umath.multiply, 1, 1)
arctan2 = _MaskedBinaryOperation(umath.arctan2, 0.0, 1.0)
equal = _MaskedBinaryOperation(umath.equal)
equal.reduce = None
not_equal = _MaskedBinaryOperation(umath.not_equal)
not_equal.reduce = None
less_equal = _MaskedBinaryOperation(umath.less_equal)
less_equal.reduce = None
greater_equal = _MaskedBinaryOperation(umath.greater_equal)
greater_equal.reduce = None
less = _MaskedBinaryOperation(umath.less)
less.reduce = None
greater = _MaskedBinaryOperation(umath.greater)
greater.reduce = None
logical_and = _MaskedBinaryOperation(umath.logical_and)
alltrue = _MaskedBinaryOperation(umath.logical_and, 1, 1).reduce
logical_or = _MaskedBinaryOperation(umath.logical_or)
sometrue = logical_or.reduce
logical_xor = _MaskedBinaryOperation(umath.logical_xor)
bitwise_and = _MaskedBinaryOperation(umath.bitwise_and)
bitwise_or = _MaskedBinaryOperation(umath.bitwise_or)
bitwise_xor = _MaskedBinaryOperation(umath.bitwise_xor)
hypot = _MaskedBinaryOperation(umath.hypot)
divide = _DomainedBinaryOperation(umath.divide, _DomainSafeDivide(), 0, 1)
true_divide = _DomainedBinaryOperation(umath.true_divide, _DomainSafeDivide(), 0, 1)
floor_divide = _DomainedBinaryOperation(umath.floor_divide, _DomainSafeDivide(), 0, 1)
remainder = _DomainedBinaryOperation(umath.remainder, _DomainSafeDivide(), 0, 1)
fmod = _DomainedBinaryOperation(umath.fmod, _DomainSafeDivide(), 0, 1)
mod = _DomainedBinaryOperation(umath.mod, _DomainSafeDivide(), 0, 1)

def _replace_dtype_fields_recursive(dtype, primitive_dtype):
    """Private function allowing recursion in _replace_dtype_fields."""
    _recurse = _replace_dtype_fields_recursive
    if dtype.names is not None:
        descr = []
        for name in dtype.names:
            field = dtype.fields[name]
            if len(field) == 3:
                name = (field[(-1)], name)
            else:
                descr.append((name, _recurse(field[0], primitive_dtype)))

        new_dtype = np.dtype(descr)
    elif dtype.subdtype:
        descr = list(dtype.subdtype)
        descr[0] = _recurse(dtype.subdtype[0], primitive_dtype)
        new_dtype = np.dtype(tuple(descr))
    else:
        new_dtype = primitive_dtype
    if new_dtype == dtype:
        new_dtype = dtype
    return new_dtype


def _replace_dtype_fields(dtype, primitive_dtype):
    """
    Construct a dtype description list from a given dtype.

    Returns a new dtype object, with all fields and subtypes in the given type
    recursively replaced with `primitive_dtype`.

    Arguments are coerced to dtypes first.
    """
    dtype = np.dtype(dtype)
    primitive_dtype = np.dtype(primitive_dtype)
    return _replace_dtype_fields_recursive(dtype, primitive_dtype)


def make_mask_descr(ndtype):
    """
    Construct a dtype description list from a given dtype.

    Returns a new dtype object, with the type of all fields in `ndtype` to a
    boolean type. Field names are not altered.

    Parameters
    ----------
    ndtype : dtype
        The dtype to convert.

    Returns
    -------
    result : dtype
        A dtype that looks like `ndtype`, the type of all fields is boolean.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> dtype = np.dtype({'names':['foo', 'bar'],
    ...                   'formats':[np.float32, np.int64]})
    >>> dtype
    dtype([('foo', '<f4'), ('bar', '<i8')])
    >>> ma.make_mask_descr(dtype)
    dtype([('foo', '|b1'), ('bar', '|b1')])
    >>> ma.make_mask_descr(np.float32)
    dtype('bool')

    """
    return _replace_dtype_fields(ndtype, MaskType)


def getmask(a):
    """
    Return the mask of a masked array, or nomask.

    Return the mask of `a` as an ndarray if `a` is a `MaskedArray` and the
    mask is not `nomask`, else return `nomask`. To guarantee a full array
    of booleans of the same shape as a, use `getmaskarray`.

    Parameters
    ----------
    a : array_like
        Input `MaskedArray` for which the mask is required.

    See Also
    --------
    getdata : Return the data of a masked array as an ndarray.
    getmaskarray : Return the mask of a masked array, or full array of False.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = ma.masked_equal([[1,2],[3,4]], 2)
    >>> a
    masked_array(
      data=[[1, --],
            [3, 4]],
      mask=[[False,  True],
            [False, False]],
      fill_value=2)
    >>> ma.getmask(a)
    array([[False,  True],
           [False, False]])

    Equivalently use the `MaskedArray` `mask` attribute.

    >>> a.mask
    array([[False,  True],
           [False, False]])

    Result when mask == `nomask`

    >>> b = ma.masked_array([[1,2],[3,4]])
    >>> b
    masked_array(
      data=[[1, 2],
            [3, 4]],
      mask=False,
      fill_value=999999)
    >>> ma.nomask
    False
    >>> ma.getmask(b) == ma.nomask
    True
    >>> b.mask == ma.nomask
    True

    """
    return getattr(a, '_mask', nomask)


get_mask = getmask

def getmaskarray(arr):
    """
    Return the mask of a masked array, or full boolean array of False.

    Return the mask of `arr` as an ndarray if `arr` is a `MaskedArray` and
    the mask is not `nomask`, else return a full boolean array of False of
    the same shape as `arr`.

    Parameters
    ----------
    arr : array_like
        Input `MaskedArray` for which the mask is required.

    See Also
    --------
    getmask : Return the mask of a masked array, or nomask.
    getdata : Return the data of a masked array as an ndarray.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = ma.masked_equal([[1,2],[3,4]], 2)
    >>> a
    masked_array(
      data=[[1, --],
            [3, 4]],
      mask=[[False,  True],
            [False, False]],
      fill_value=2)
    >>> ma.getmaskarray(a)
    array([[False,  True],
           [False, False]])

    Result when mask == ``nomask``

    >>> b = ma.masked_array([[1,2],[3,4]])
    >>> b
    masked_array(
      data=[[1, 2],
            [3, 4]],
      mask=False,
      fill_value=999999)
    >>> ma.getmaskarray(b)
    array([[False, False],
           [False, False]])

    """
    mask = getmask(arr)
    if mask is nomask:
        mask = make_mask_none(np.shape(arr), getattr(arr, 'dtype', None))
    return mask


def is_mask(m):
    """
    Return True if m is a valid, standard mask.

    This function does not check the contents of the input, only that the
    type is MaskType. In particular, this function returns False if the
    mask has a flexible dtype.

    Parameters
    ----------
    m : array_like
        Array to test.

    Returns
    -------
    result : bool
        True if `m.dtype.type` is MaskType, False otherwise.

    See Also
    --------
    ma.isMaskedArray : Test whether input is an instance of MaskedArray.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> m = ma.masked_equal([0, 1, 0, 2, 3], 0)
    >>> m
    masked_array(data=[--, 1, --, 2, 3],
                 mask=[ True, False,  True, False, False],
           fill_value=0)
    >>> ma.is_mask(m)
    False
    >>> ma.is_mask(m.mask)
    True

    Input must be an ndarray (or have similar attributes)
    for it to be considered a valid mask.

    >>> m = [False, True, False]
    >>> ma.is_mask(m)
    False
    >>> m = np.array([False, True, False])
    >>> m
    array([False,  True, False])
    >>> ma.is_mask(m)
    True

    Arrays with complex dtypes don't return True.

    >>> dtype = np.dtype({'names':['monty', 'pithon'],
    ...                   'formats':[bool, bool]})
    >>> dtype
    dtype([('monty', '|b1'), ('pithon', '|b1')])
    >>> m = np.array([(True, False), (False, True), (True, False)],
    ...              dtype=dtype)
    >>> m
    array([( True, False), (False,  True), ( True, False)],
          dtype=[('monty', '?'), ('pithon', '?')])
    >>> ma.is_mask(m)
    False

    """
    try:
        return m.dtype.type is MaskType
    except AttributeError:
        return False


def _shrink_mask(m):
    """
    Shrink a mask to nomask if possible
    """
    if m.dtype.names is None:
        if not m.any():
            return nomask
        return m


def make_mask(m, copy=False, shrink=True, dtype=MaskType):
    """
    Create a boolean mask from an array.

    Return `m` as a boolean mask, creating a copy if necessary or requested.
    The function can accept any sequence that is convertible to integers,
    or ``nomask``.  Does not require that contents must be 0s and 1s, values
    of 0 are interpreted as False, everything else as True.

    Parameters
    ----------
    m : array_like
        Potential mask.
    copy : bool, optional
        Whether to return a copy of `m` (True) or `m` itself (False).
    shrink : bool, optional
        Whether to shrink `m` to ``nomask`` if all its values are False.
    dtype : dtype, optional
        Data-type of the output mask. By default, the output mask has a
        dtype of MaskType (bool). If the dtype is flexible, each field has
        a boolean dtype. This is ignored when `m` is ``nomask``, in which
        case ``nomask`` is always returned.

    Returns
    -------
    result : ndarray
        A boolean mask derived from `m`.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> m = [True, False, True, True]
    >>> ma.make_mask(m)
    array([ True, False,  True,  True])
    >>> m = [1, 0, 1, 1]
    >>> ma.make_mask(m)
    array([ True, False,  True,  True])
    >>> m = [1, 0, 2, -3]
    >>> ma.make_mask(m)
    array([ True, False,  True,  True])

    Effect of the `shrink` parameter.

    >>> m = np.zeros(4)
    >>> m
    array([0., 0., 0., 0.])
    >>> ma.make_mask(m)
    False
    >>> ma.make_mask(m, shrink=False)
    array([False, False, False, False])

    Using a flexible `dtype`.

    >>> m = [1, 0, 1, 1]
    >>> n = [0, 1, 0, 0]
    >>> arr = []
    >>> for man, mouse in zip(m, n):
    ...     arr.append((man, mouse))
    >>> arr
    [(1, 0), (0, 1), (1, 0), (1, 0)]
    >>> dtype = np.dtype({'names':['man', 'mouse'],
    ...                   'formats':[np.int64, np.int64]})
    >>> arr = np.array(arr, dtype=dtype)
    >>> arr
    array([(1, 0), (0, 1), (1, 0), (1, 0)],
          dtype=[('man', '<i8'), ('mouse', '<i8')])
    >>> ma.make_mask(arr, dtype=dtype)
    array([(True, False), (False, True), (True, False), (True, False)],
          dtype=[('man', '|b1'), ('mouse', '|b1')])

    """
    if m is nomask:
        return nomask
    dtype = make_mask_descr(dtype)
    if isinstance(m, ndarray):
        if m.dtype.fields:
            if dtype == np.bool_:
                return np.ones((m.shape), dtype=dtype)
    result = np.array((filled(m, True)), copy=copy, dtype=dtype, subok=True)
    if shrink:
        result = _shrink_mask(result)
    return result


def make_mask_none(newshape, dtype=None):
    """
    Return a boolean mask of the given shape, filled with False.

    This function returns a boolean ndarray with all entries False, that can
    be used in common mask manipulations. If a complex dtype is specified, the
    type of each field is converted to a boolean type.

    Parameters
    ----------
    newshape : tuple
        A tuple indicating the shape of the mask.
    dtype : {None, dtype}, optional
        If None, use a MaskType instance. Otherwise, use a new datatype with
        the same fields as `dtype`, converted to boolean types.

    Returns
    -------
    result : ndarray
        An ndarray of appropriate shape and dtype, filled with False.

    See Also
    --------
    make_mask : Create a boolean mask from an array.
    make_mask_descr : Construct a dtype description list from a given dtype.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> ma.make_mask_none((3,))
    array([False, False, False])

    Defining a more complex dtype.

    >>> dtype = np.dtype({'names':['foo', 'bar'],
    ...                   'formats':[np.float32, np.int64]})
    >>> dtype
    dtype([('foo', '<f4'), ('bar', '<i8')])
    >>> ma.make_mask_none((3,), dtype=dtype)
    array([(False, False), (False, False), (False, False)],
          dtype=[('foo', '|b1'), ('bar', '|b1')])

    """
    if dtype is None:
        result = np.zeros(newshape, dtype=MaskType)
    else:
        result = np.zeros(newshape, dtype=(make_mask_descr(dtype)))
    return result


def mask_or(m1, m2, copy=False, shrink=True):
    """
    Combine two masks with the ``logical_or`` operator.

    The result may be a view on `m1` or `m2` if the other is `nomask`
    (i.e. False).

    Parameters
    ----------
    m1, m2 : array_like
        Input masks.
    copy : bool, optional
        If copy is False and one of the inputs is `nomask`, return a view
        of the other input mask. Defaults to False.
    shrink : bool, optional
        Whether to shrink the output to `nomask` if all its values are
        False. Defaults to True.

    Returns
    -------
    mask : output mask
        The result masks values that are masked in either `m1` or `m2`.

    Raises
    ------
    ValueError
        If `m1` and `m2` have different flexible dtypes.

    Examples
    --------
    >>> m1 = np.ma.make_mask([0, 1, 1, 0])
    >>> m2 = np.ma.make_mask([1, 0, 0, 0])
    >>> np.ma.mask_or(m1, m2)
    array([ True,  True,  True, False])

    """

    @recursive
    def _recursive_mask_or(self, m1, m2, newmask):
        names = m1.dtype.names
        for name in names:
            current1 = m1[name]
            if current1.dtype.names is not None:
                self(current1, m2[name], newmask[name])
            else:
                umath.logical_or(current1, m2[name], newmask[name])

    if m1 is nomask or (m1 is False):
        dtype = getattr(m2, 'dtype', MaskType)
        return make_mask(m2, copy=copy, shrink=shrink, dtype=dtype)
    if m2 is nomask or (m2 is False):
        dtype = getattr(m1, 'dtype', MaskType)
        return make_mask(m1, copy=copy, shrink=shrink, dtype=dtype)
    if m1 is m2:
        if is_mask(m1):
            return m1
    dtype1, dtype2 = getattr(m1, 'dtype', None), getattr(m2, 'dtype', None)
    if dtype1 != dtype2:
        raise ValueError("Incompatible dtypes '%s'<>'%s'" % (dtype1, dtype2))
    if dtype1.names is not None:
        newmask = np.empty(np.broadcast(m1, m2).shape, dtype1)
        _recursive_mask_or(m1, m2, newmask)
        return newmask
    return make_mask((umath.logical_or(m1, m2)), copy=copy, shrink=shrink)


def flatten_mask(mask):
    """
    Returns a completely flattened version of the mask, where nested fields
    are collapsed.

    Parameters
    ----------
    mask : array_like
        Input array, which will be interpreted as booleans.

    Returns
    -------
    flattened_mask : ndarray of bools
        The flattened input.

    Examples
    --------
    >>> mask = np.array([0, 0, 1])
    >>> np.ma.flatten_mask(mask)
    array([False, False,  True])

    >>> mask = np.array([(0, 0), (0, 1)], dtype=[('a', bool), ('b', bool)])
    >>> np.ma.flatten_mask(mask)
    array([False, False, False,  True])

    >>> mdtype = [('a', bool), ('b', [('ba', bool), ('bb', bool)])]
    >>> mask = np.array([(0, (0, 0)), (0, (0, 1))], dtype=mdtype)
    >>> np.ma.flatten_mask(mask)
    array([False, False, False, False, False,  True])

    """

    def _flatmask(mask):
        """Flatten the mask and returns a (maybe nested) sequence of booleans."""
        mnames = mask.dtype.names
        if mnames is not None:
            return [flatten_mask(mask[name]) for name in mnames]
        return mask

    def _flatsequence(sequence):
        try:
            for element in sequence:
                if hasattr(element, '__iter__'):
                    yield from _flatsequence(element)
                else:
                    yield element

        except TypeError:
            yield sequence

    mask = np.asarray(mask)
    flattened = _flatsequence(_flatmask(mask))
    return np.array([_ for _ in flattened], dtype=bool)


def _check_mask_axis(mask, axis, keepdims=np._NoValue):
    """Check whether there are masked values along the given axis"""
    kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
    if mask is not nomask:
        return (mask.all)(axis=axis, **kwargs)
    return nomask


def masked_where(condition, a, copy=True):
    """
    Mask an array where a condition is met.

    Return `a` as an array masked where `condition` is True.
    Any masked values of `a` or `condition` are also masked in the output.

    Parameters
    ----------
    condition : array_like
        Masking condition.  When `condition` tests floating point values for
        equality, consider using ``masked_values`` instead.
    a : array_like
        Array to mask.
    copy : bool
        If True (default) make a copy of `a` in the result.  If False modify
        `a` in place and return a view.

    Returns
    -------
    result : MaskedArray
        The result of masking `a` where `condition` is True.

    See Also
    --------
    masked_values : Mask using floating point equality.
    masked_equal : Mask where equal to a given value.
    masked_not_equal : Mask where `not` equal to a given value.
    masked_less_equal : Mask where less than or equal to a given value.
    masked_greater_equal : Mask where greater than or equal to a given value.
    masked_less : Mask where less than a given value.
    masked_greater : Mask where greater than a given value.
    masked_inside : Mask inside a given interval.
    masked_outside : Mask outside a given interval.
    masked_invalid : Mask invalid values (NaNs or infs).

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.arange(4)
    >>> a
    array([0, 1, 2, 3])
    >>> ma.masked_where(a <= 2, a)
    masked_array(data=[--, --, --, 3],
                 mask=[ True,  True,  True, False],
           fill_value=999999)

    Mask array `b` conditional on `a`.

    >>> b = ['a', 'b', 'c', 'd']
    >>> ma.masked_where(a == 2, b)
    masked_array(data=['a', 'b', --, 'd'],
                 mask=[False, False,  True, False],
           fill_value='N/A',
                dtype='<U1')

    Effect of the `copy` argument.

    >>> c = ma.masked_where(a <= 2, a)
    >>> c
    masked_array(data=[--, --, --, 3],
                 mask=[ True,  True,  True, False],
           fill_value=999999)
    >>> c[0] = 99
    >>> c
    masked_array(data=[99, --, --, 3],
                 mask=[False,  True,  True, False],
           fill_value=999999)
    >>> a
    array([0, 1, 2, 3])
    >>> c = ma.masked_where(a <= 2, a, copy=False)
    >>> c[0] = 99
    >>> c
    masked_array(data=[99, --, --, 3],
                 mask=[False,  True,  True, False],
           fill_value=999999)
    >>> a
    array([99,  1,  2,  3])

    When `condition` or `a` contain masked values.

    >>> a = np.arange(4)
    >>> a = ma.masked_where(a == 2, a)
    >>> a
    masked_array(data=[0, 1, --, 3],
                 mask=[False, False,  True, False],
           fill_value=999999)
    >>> b = np.arange(4)
    >>> b = ma.masked_where(b == 0, b)
    >>> b
    masked_array(data=[--, 1, 2, 3],
                 mask=[ True, False, False, False],
           fill_value=999999)
    >>> ma.masked_where(a == 3, b)
    masked_array(data=[--, 1, --, --],
                 mask=[ True, False,  True,  True],
           fill_value=999999)

    """
    cond = make_mask(condition, shrink=False)
    a = np.array(a, copy=copy, subok=True)
    cshape, ashape = cond.shape, a.shape
    if cshape:
        if cshape != ashape:
            raise IndexError('Inconsistent shape between the condition and the input (got %s and %s)' % (
             cshape, ashape))
    if hasattr(a, '_mask'):
        cond = mask_or(cond, a._mask)
        cls = type(a)
    else:
        cls = MaskedArray
    result = a.view(cls)
    result.mask = _shrink_mask(cond)
    return result


def masked_greater(x, value, copy=True):
    """
    Mask an array where greater than a given value.

    This function is a shortcut to ``masked_where``, with
    `condition` = (x > value).

    See Also
    --------
    masked_where : Mask where a condition is met.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.arange(4)
    >>> a
    array([0, 1, 2, 3])
    >>> ma.masked_greater(a, 2)
    masked_array(data=[0, 1, 2, --],
                 mask=[False, False, False,  True],
           fill_value=999999)

    """
    return masked_where((greater(x, value)), x, copy=copy)


def masked_greater_equal(x, value, copy=True):
    """
    Mask an array where greater than or equal to a given value.

    This function is a shortcut to ``masked_where``, with
    `condition` = (x >= value).

    See Also
    --------
    masked_where : Mask where a condition is met.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.arange(4)
    >>> a
    array([0, 1, 2, 3])
    >>> ma.masked_greater_equal(a, 2)
    masked_array(data=[0, 1, --, --],
                 mask=[False, False,  True,  True],
           fill_value=999999)

    """
    return masked_where((greater_equal(x, value)), x, copy=copy)


def masked_less(x, value, copy=True):
    """
    Mask an array where less than a given value.

    This function is a shortcut to ``masked_where``, with
    `condition` = (x < value).

    See Also
    --------
    masked_where : Mask where a condition is met.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.arange(4)
    >>> a
    array([0, 1, 2, 3])
    >>> ma.masked_less(a, 2)
    masked_array(data=[--, --, 2, 3],
                 mask=[ True,  True, False, False],
           fill_value=999999)

    """
    return masked_where((less(x, value)), x, copy=copy)


def masked_less_equal(x, value, copy=True):
    """
    Mask an array where less than or equal to a given value.

    This function is a shortcut to ``masked_where``, with
    `condition` = (x <= value).

    See Also
    --------
    masked_where : Mask where a condition is met.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.arange(4)
    >>> a
    array([0, 1, 2, 3])
    >>> ma.masked_less_equal(a, 2)
    masked_array(data=[--, --, --, 3],
                 mask=[ True,  True,  True, False],
           fill_value=999999)

    """
    return masked_where((less_equal(x, value)), x, copy=copy)


def masked_not_equal(x, value, copy=True):
    """
    Mask an array where `not` equal to a given value.

    This function is a shortcut to ``masked_where``, with
    `condition` = (x != value).

    See Also
    --------
    masked_where : Mask where a condition is met.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.arange(4)
    >>> a
    array([0, 1, 2, 3])
    >>> ma.masked_not_equal(a, 2)
    masked_array(data=[--, --, 2, --],
                 mask=[ True,  True, False,  True],
           fill_value=999999)

    """
    return masked_where((not_equal(x, value)), x, copy=copy)


def masked_equal(x, value, copy=True):
    """
    Mask an array where equal to a given value.

    This function is a shortcut to ``masked_where``, with
    `condition` = (x == value).  For floating point arrays,
    consider using ``masked_values(x, value)``.

    See Also
    --------
    masked_where : Mask where a condition is met.
    masked_values : Mask using floating point equality.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.arange(4)
    >>> a
    array([0, 1, 2, 3])
    >>> ma.masked_equal(a, 2)
    masked_array(data=[0, 1, --, 3],
                 mask=[False, False,  True, False],
           fill_value=2)

    """
    output = masked_where((equal(x, value)), x, copy=copy)
    output.fill_value = value
    return output


def masked_inside(x, v1, v2, copy=True):
    """
    Mask an array inside a given interval.

    Shortcut to ``masked_where``, where `condition` is True for `x` inside
    the interval [v1,v2] (v1 <= x <= v2).  The boundaries `v1` and `v2`
    can be given in either order.

    See Also
    --------
    masked_where : Mask where a condition is met.

    Notes
    -----
    The array `x` is prefilled with its filling value.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> x = [0.31, 1.2, 0.01, 0.2, -0.4, -1.1]
    >>> ma.masked_inside(x, -0.3, 0.3)
    masked_array(data=[0.31, 1.2, --, --, -0.4, -1.1],
                 mask=[False, False,  True,  True, False, False],
           fill_value=1e+20)

    The order of `v1` and `v2` doesn't matter.

    >>> ma.masked_inside(x, 0.3, -0.3)
    masked_array(data=[0.31, 1.2, --, --, -0.4, -1.1],
                 mask=[False, False,  True,  True, False, False],
           fill_value=1e+20)

    """
    if v2 < v1:
        v1, v2 = v2, v1
    xf = filled(x)
    condition = (xf >= v1) & (xf <= v2)
    return masked_where(condition, x, copy=copy)


def masked_outside(x, v1, v2, copy=True):
    """
    Mask an array outside a given interval.

    Shortcut to ``masked_where``, where `condition` is True for `x` outside
    the interval [v1,v2] (x < v1)|(x > v2).
    The boundaries `v1` and `v2` can be given in either order.

    See Also
    --------
    masked_where : Mask where a condition is met.

    Notes
    -----
    The array `x` is prefilled with its filling value.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> x = [0.31, 1.2, 0.01, 0.2, -0.4, -1.1]
    >>> ma.masked_outside(x, -0.3, 0.3)
    masked_array(data=[--, --, 0.01, 0.2, --, --],
                 mask=[ True,  True, False, False,  True,  True],
           fill_value=1e+20)

    The order of `v1` and `v2` doesn't matter.

    >>> ma.masked_outside(x, 0.3, -0.3)
    masked_array(data=[--, --, 0.01, 0.2, --, --],
                 mask=[ True,  True, False, False,  True,  True],
           fill_value=1e+20)

    """
    if v2 < v1:
        v1, v2 = v2, v1
    xf = filled(x)
    condition = (xf < v1) | (xf > v2)
    return masked_where(condition, x, copy=copy)


def masked_object(x, value, copy=True, shrink=True):
    """
    Mask the array `x` where the data are exactly equal to value.

    This function is similar to `masked_values`, but only suitable
    for object arrays: for floating point, use `masked_values` instead.

    Parameters
    ----------
    x : array_like
        Array to mask
    value : object
        Comparison value
    copy : {True, False}, optional
        Whether to return a copy of `x`.
    shrink : {True, False}, optional
        Whether to collapse a mask full of False to nomask

    Returns
    -------
    result : MaskedArray
        The result of masking `x` where equal to `value`.

    See Also
    --------
    masked_where : Mask where a condition is met.
    masked_equal : Mask where equal to a given value (integers).
    masked_values : Mask using floating point equality.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> food = np.array(['green_eggs', 'ham'], dtype=object)
    >>> # don't eat spoiled food
    >>> eat = ma.masked_object(food, 'green_eggs')
    >>> eat
    masked_array(data=[--, 'ham'],
                 mask=[ True, False],
           fill_value='green_eggs',
                dtype=object)
    >>> # plain ol` ham is boring
    >>> fresh_food = np.array(['cheese', 'ham', 'pineapple'], dtype=object)
    >>> eat = ma.masked_object(fresh_food, 'green_eggs')
    >>> eat
    masked_array(data=['cheese', 'ham', 'pineapple'],
                 mask=False,
           fill_value='green_eggs',
                dtype=object)

    Note that `mask` is set to ``nomask`` if possible.

    >>> eat
    masked_array(data=['cheese', 'ham', 'pineapple'],
                 mask=False,
           fill_value='green_eggs',
                dtype=object)

    """
    if isMaskedArray(x):
        condition = umath.equal(x._data, value)
        mask = x._mask
    else:
        condition = umath.equal(np.asarray(x), value)
        mask = nomask
    mask = mask_or(mask, make_mask(condition, shrink=shrink))
    return masked_array(x, mask=mask, copy=copy, fill_value=value)


def masked_values(x, value, rtol=1e-05, atol=1e-08, copy=True, shrink=True):
    """
    Mask using floating point equality.

    Return a MaskedArray, masked where the data in array `x` are approximately
    equal to `value`, determined using `isclose`. The default tolerances for
    `masked_values` are the same as those for `isclose`.

    For integer types, exact equality is used, in the same way as
    `masked_equal`.

    The fill_value is set to `value` and the mask is set to ``nomask`` if
    possible.

    Parameters
    ----------
    x : array_like
        Array to mask.
    value : float
        Masking value.
    rtol, atol : float, optional
        Tolerance parameters passed on to `isclose`
    copy : bool, optional
        Whether to return a copy of `x`.
    shrink : bool, optional
        Whether to collapse a mask full of False to ``nomask``.

    Returns
    -------
    result : MaskedArray
        The result of masking `x` where approximately equal to `value`.

    See Also
    --------
    masked_where : Mask where a condition is met.
    masked_equal : Mask where equal to a given value (integers).

    Examples
    --------
    >>> import numpy.ma as ma
    >>> x = np.array([1, 1.1, 2, 1.1, 3])
    >>> ma.masked_values(x, 1.1)
    masked_array(data=[1.0, --, 2.0, --, 3.0],
                 mask=[False,  True, False,  True, False],
           fill_value=1.1)

    Note that `mask` is set to ``nomask`` if possible.

    >>> ma.masked_values(x, 1.5)
    masked_array(data=[1. , 1.1, 2. , 1.1, 3. ],
                 mask=False,
           fill_value=1.5)

    For integers, the fill value will be different in general to the
    result of ``masked_equal``.

    >>> x = np.arange(5)
    >>> x
    array([0, 1, 2, 3, 4])
    >>> ma.masked_values(x, 2)
    masked_array(data=[0, 1, --, 3, 4],
                 mask=[False, False,  True, False, False],
           fill_value=2)
    >>> ma.masked_equal(x, 2)
    masked_array(data=[0, 1, --, 3, 4],
                 mask=[False, False,  True, False, False],
           fill_value=2)

    """
    xnew = filled(x, value)
    if np.issubdtype(xnew.dtype, np.floating):
        mask = np.isclose(xnew, value, atol=atol, rtol=rtol)
    else:
        mask = umath.equal(xnew, value)
    ret = masked_array(xnew, mask=mask, copy=copy, fill_value=value)
    if shrink:
        ret.shrink_mask()
    return ret


def masked_invalid(a, copy=True):
    """
    Mask an array where invalid values occur (NaNs or infs).

    This function is a shortcut to ``masked_where``, with
    `condition` = ~(np.isfinite(a)). Any pre-existing mask is conserved.
    Only applies to arrays with a dtype where NaNs or infs make sense
    (i.e. floating point types), but accepts any array_like object.

    See Also
    --------
    masked_where : Mask where a condition is met.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.arange(5, dtype=float)
    >>> a[2] = np.NaN
    >>> a[3] = np.PINF
    >>> a
    array([ 0.,  1., nan, inf,  4.])
    >>> ma.masked_invalid(a)
    masked_array(data=[0.0, 1.0, --, --, 4.0],
                 mask=[False, False,  True,  True, False],
           fill_value=1e+20)

    """
    a = np.array(a, copy=copy, subok=True)
    mask = getattr(a, '_mask', None)
    if mask is not None:
        condition = ~np.isfinite(getdata(a))
        if mask is not nomask:
            condition |= mask
        cls = type(a)
    else:
        condition = ~np.isfinite(a)
        cls = MaskedArray
    result = a.view(cls)
    result._mask = condition
    return result


class _MaskedPrintOption:
    __doc__ = '\n    Handle the string used to represent missing data in a masked array.\n\n    '

    def __init__(self, display):
        """
        Create the masked_print_option object.

        """
        self._display = display
        self._enabled = True

    def display(self):
        """
        Display the string to print for masked values.

        """
        return self._display

    def set_display(self, s):
        """
        Set the string to print for masked values.

        """
        self._display = s

    def enabled(self):
        """
        Is the use of the display value enabled?

        """
        return self._enabled

    def enable(self, shrink=1):
        """
        Set the enabling shrink to `shrink`.

        """
        self._enabled = shrink

    def __str__(self):
        return str(self._display)

    __repr__ = __str__


masked_print_option = _MaskedPrintOption('--')

def _recursive_printoption(result, mask, printopt):
    """
    Puts printoptions in result where mask is True.

    Private function allowing for recursion

    """
    names = result.dtype.names
    if names is not None:
        for name in names:
            curdata = result[name]
            curmask = mask[name]
            _recursive_printoption(curdata, curmask, printopt)

    else:
        np.copyto(result, printopt, where=mask)


_legacy_print_templates = dict(long_std=(textwrap.dedent('        masked_%(name)s(data =\n         %(data)s,\n        %(nlen)s        mask =\n         %(mask)s,\n        %(nlen)s  fill_value = %(fill)s)\n        ')),
  long_flx=(textwrap.dedent('        masked_%(name)s(data =\n         %(data)s,\n        %(nlen)s        mask =\n         %(mask)s,\n        %(nlen)s  fill_value = %(fill)s,\n        %(nlen)s       dtype = %(dtype)s)\n        ')),
  short_std=(textwrap.dedent('        masked_%(name)s(data = %(data)s,\n        %(nlen)s        mask = %(mask)s,\n        %(nlen)s  fill_value = %(fill)s)\n        ')),
  short_flx=(textwrap.dedent('        masked_%(name)s(data = %(data)s,\n        %(nlen)s        mask = %(mask)s,\n        %(nlen)s  fill_value = %(fill)s,\n        %(nlen)s       dtype = %(dtype)s)\n        ')))

def _recursive_filled(a, mask, fill_value):
    """
    Recursively fill `a` with `fill_value`.

    """
    names = a.dtype.names
    for name in names:
        current = a[name]
        if current.dtype.names is not None:
            _recursive_filled(current, mask[name], fill_value[name])
        else:
            np.copyto(current, (fill_value[name]), where=(mask[name]))


def flatten_structured_array(a):
    """
    Flatten a structured array.

    The data type of the output is chosen such that it can represent all of the
    (nested) fields.

    Parameters
    ----------
    a : structured array

    Returns
    -------
    output : masked array or ndarray
        A flattened masked array if the input is a masked array, otherwise a
        standard ndarray.

    Examples
    --------
    >>> ndtype = [('a', int), ('b', float)]
    >>> a = np.array([(1, 1), (2, 2)], dtype=ndtype)
    >>> np.ma.flatten_structured_array(a)
    array([[1., 1.],
           [2., 2.]])

    """

    def flatten_sequence(iterable):
        for elm in iter(iterable):
            if hasattr(elm, '__iter__'):
                yield from flatten_sequence(elm)
            else:
                yield elm

    a = np.asanyarray(a)
    inishape = a.shape
    a = a.ravel()
    if isinstance(a, MaskedArray):
        out = np.array([tuple(flatten_sequence(d.item())) for d in a._data])
        out = out.view(MaskedArray)
        out._mask = np.array([tuple(flatten_sequence(d.item())) for d in getmaskarray(a)])
    else:
        out = np.array([tuple(flatten_sequence(d.item())) for d in a])
    if len(inishape) > 1:
        newshape = list(out.shape)
        newshape[0] = inishape
        out.shape = tuple(flatten_sequence(newshape))
    return out


def _arraymethod(funcname, onmask=True):
    """
    Return a class method wrapper around a basic array method.

    Creates a class method which returns a masked array, where the new
    ``_data`` array is the output of the corresponding basic method called
    on the original ``_data``.

    If `onmask` is True, the new mask is the output of the method called
    on the initial mask. Otherwise, the new mask is just a reference
    to the initial mask.

    Parameters
    ----------
    funcname : str
        Name of the function to apply on data.
    onmask : bool
        Whether the mask must be processed also (True) or left
        alone (False). Default is True. Make available as `_onmask`
        attribute.

    Returns
    -------
    method : instancemethod
        Class method wrapper of the specified basic array method.

    """

    def wrapped_method(self, *args, **params):
        result = (getattr(self._data, funcname))(*args, **params)
        result = result.view(type(self))
        result._update_from(self)
        mask = self._mask
        if not onmask:
            result.__setmask__(mask)
        elif mask is not nomask:
            result._mask = (getattr(mask, funcname))(*args, **params)
        return result

    methdoc = getattr(ndarray, funcname, None) or getattr(np, funcname, None)
    if methdoc is not None:
        wrapped_method.__doc__ = methdoc.__doc__
    wrapped_method.__name__ = funcname
    return wrapped_method


class MaskedIterator:
    __doc__ = "\n    Flat iterator object to iterate over masked arrays.\n\n    A `MaskedIterator` iterator is returned by ``x.flat`` for any masked array\n    `x`. It allows iterating over the array as if it were a 1-D array,\n    either in a for-loop or by calling its `next` method.\n\n    Iteration is done in C-contiguous style, with the last index varying the\n    fastest. The iterator can also be indexed using basic slicing or\n    advanced indexing.\n\n    See Also\n    --------\n    MaskedArray.flat : Return a flat iterator over an array.\n    MaskedArray.flatten : Returns a flattened copy of an array.\n\n    Notes\n    -----\n    `MaskedIterator` is not exported by the `ma` module. Instead of\n    instantiating a `MaskedIterator` directly, use `MaskedArray.flat`.\n\n    Examples\n    --------\n    >>> x = np.ma.array(arange(6).reshape(2, 3))\n    >>> fl = x.flat\n    >>> type(fl)\n    <class 'numpy.ma.core.MaskedIterator'>\n    >>> for item in fl:\n    ...     print(item)\n    ...\n    0\n    1\n    2\n    3\n    4\n    5\n\n    Extracting more than a single element b indexing the `MaskedIterator`\n    returns a masked array:\n\n    >>> fl[2:4]\n    masked_array(data = [2 3],\n                 mask = False,\n           fill_value = 999999)\n\n    "

    def __init__(self, ma):
        self.ma = ma
        self.dataiter = ma._data.flat
        if ma._mask is nomask:
            self.maskiter = None
        else:
            self.maskiter = ma._mask.flat

    def __iter__(self):
        return self

    def __getitem__(self, indx):
        result = self.dataiter.__getitem__(indx).view(type(self.ma))
        if self.maskiter is not None:
            _mask = self.maskiter.__getitem__(indx)
            if isinstance(_mask, ndarray):
                _mask.shape = result.shape
                result._mask = _mask
            else:
                if isinstance(_mask, np.void):
                    return mvoid(result, mask=_mask, hardmask=(self.ma._hardmask))
                if _mask:
                    return masked
        return result

    def __setitem__(self, index, value):
        self.dataiter[index] = getdata(value)
        if self.maskiter is not None:
            self.maskiter[index] = getmaskarray(value)

    def __next__(self):
        """
        Return the next value, or raise StopIteration.

        Examples
        --------
        >>> x = np.ma.array([3, 2], mask=[0, 1])
        >>> fl = x.flat
        >>> next(fl)
        3
        >>> next(fl)
        masked
        >>> next(fl)
        Traceback (most recent call last):
          ...
        StopIteration

        """
        d = next(self.dataiter)
        if self.maskiter is not None:
            m = next(self.maskiter)
            if isinstance(m, np.void):
                return mvoid(d, mask=m, hardmask=(self.ma._hardmask))
            if m:
                return masked
        return d


class MaskedArray(ndarray):
    __doc__ = "\n    An array class with possibly masked values.\n\n    Masked values of True exclude the corresponding element from any\n    computation.\n\n    Construction::\n\n      x = MaskedArray(data, mask=nomask, dtype=None, copy=False, subok=True,\n                      ndmin=0, fill_value=None, keep_mask=True, hard_mask=None,\n                      shrink=True, order=None)\n\n    Parameters\n    ----------\n    data : array_like\n        Input data.\n    mask : sequence, optional\n        Mask. Must be convertible to an array of booleans with the same\n        shape as `data`. True indicates a masked (i.e. invalid) data.\n    dtype : dtype, optional\n        Data type of the output.\n        If `dtype` is None, the type of the data argument (``data.dtype``)\n        is used. If `dtype` is not None and different from ``data.dtype``,\n        a copy is performed.\n    copy : bool, optional\n        Whether to copy the input data (True), or to use a reference instead.\n        Default is False.\n    subok : bool, optional\n        Whether to return a subclass of `MaskedArray` if possible (True) or a\n        plain `MaskedArray`. Default is True.\n    ndmin : int, optional\n        Minimum number of dimensions. Default is 0.\n    fill_value : scalar, optional\n        Value used to fill in the masked values when necessary.\n        If None, a default based on the data-type is used.\n    keep_mask : bool, optional\n        Whether to combine `mask` with the mask of the input data, if any\n        (True), or to use only `mask` for the output (False). Default is True.\n    hard_mask : bool, optional\n        Whether to use a hard mask or not. With a hard mask, masked values\n        cannot be unmasked. Default is False.\n    shrink : bool, optional\n        Whether to force compression of an empty mask. Default is True.\n    order : {'C', 'F', 'A'}, optional\n        Specify the order of the array.  If order is 'C', then the array\n        will be in C-contiguous order (last-index varies the fastest).\n        If order is 'F', then the returned array will be in\n        Fortran-contiguous order (first-index varies the fastest).\n        If order is 'A' (default), then the returned array may be\n        in any order (either C-, Fortran-contiguous, or even discontiguous),\n        unless a copy is required, in which case it will be C-contiguous.\n\n    Examples\n    --------\n\n    The ``mask`` can be initialized with an array of boolean values\n    with the same shape as ``data``.\n\n    >>> data = np.arange(6).reshape((2, 3))\n    >>> np.ma.MaskedArray(data, mask=[[False, True, False],\n    ...                               [False, False, True]])\n    masked_array(\n      data=[[0, --, 2],\n            [3, 4, --]],\n      mask=[[False,  True, False],\n            [False, False,  True]],\n      fill_value=999999)\n\n    Alternatively, the ``mask`` can be initialized to homogeneous boolean\n    array with the same shape as ``data`` by passing in a scalar\n    boolean value:\n\n    >>> np.ma.MaskedArray(data, mask=False)\n    masked_array(\n      data=[[0, 1, 2],\n            [3, 4, 5]],\n      mask=[[False, False, False],\n            [False, False, False]],\n      fill_value=999999)\n\n    >>> np.ma.MaskedArray(data, mask=True)\n    masked_array(\n      data=[[--, --, --],\n            [--, --, --]],\n      mask=[[ True,  True,  True],\n            [ True,  True,  True]],\n      fill_value=999999,\n      dtype=int64)\n\n    .. note::\n        The recommended practice for initializing ``mask`` with a scalar\n        boolean value is to use ``True``/``False`` rather than\n        ``np.True_``/``np.False_``. The reason is :attr:`nomask`\n        is represented internally as ``np.False_``.\n\n        >>> np.False_ is np.ma.nomask\n        True\n\n    "
    __array_priority__ = 15
    _defaultmask = nomask
    _defaulthardmask = False
    _baseclass = ndarray
    _print_width = 100
    _print_width_1d = 1500

    def __new__--- This code section failed: ---

 L.2825         0  LOAD_GLOBAL              np
                2  LOAD_ATTR                array
                4  LOAD_FAST                'data'
                6  LOAD_FAST                'dtype'
                8  LOAD_FAST                'copy'

 L.2826        10  LOAD_FAST                'order'
               12  LOAD_CONST               True
               14  LOAD_FAST                'ndmin'
               16  LOAD_CONST               ('dtype', 'copy', 'order', 'subok', 'ndmin')
               18  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               20  STORE_DEREF              '_data'

 L.2827        22  LOAD_GLOBAL              getattr
               24  LOAD_FAST                'data'
               26  LOAD_STR                 '_baseclass'
               28  LOAD_GLOBAL              type
               30  LOAD_DEREF               '_data'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  CALL_FUNCTION_3       3  '3 positional arguments'
               36  STORE_FAST               '_baseclass'

 L.2829        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'data'
               42  LOAD_GLOBAL              MaskedArray
               44  CALL_FUNCTION_2       2  '2 positional arguments'
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  LOAD_FAST                'data'
               50  LOAD_ATTR                shape
               52  LOAD_DEREF               '_data'
               54  LOAD_ATTR                shape
               56  COMPARE_OP               !=
               58  POP_JUMP_IF_FALSE    64  'to 64'

 L.2830        60  LOAD_CONST               True
               62  STORE_FAST               'copy'
             64_0  COME_FROM            58  '58'
             64_1  COME_FROM            46  '46'

 L.2835        64  LOAD_GLOBAL              isinstance
               66  LOAD_FAST                'data'
               68  LOAD_FAST                'cls'
               70  CALL_FUNCTION_2       2  '2 positional arguments'
               72  POP_JUMP_IF_FALSE   106  'to 106'
               74  LOAD_FAST                'subok'
               76  POP_JUMP_IF_FALSE   106  'to 106'
               78  LOAD_GLOBAL              isinstance
               80  LOAD_FAST                'data'
               82  LOAD_GLOBAL              MaskedConstant
               84  CALL_FUNCTION_2       2  '2 positional arguments'
               86  POP_JUMP_IF_TRUE    106  'to 106'

 L.2836        88  LOAD_GLOBAL              ndarray
               90  LOAD_METHOD              view
               92  LOAD_DEREF               '_data'
               94  LOAD_GLOBAL              type
               96  LOAD_FAST                'data'
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  CALL_METHOD_2         2  '2 positional arguments'
              102  STORE_DEREF              '_data'
              104  JUMP_FORWARD        118  'to 118'
            106_0  COME_FROM            86  '86'
            106_1  COME_FROM            76  '76'
            106_2  COME_FROM            72  '72'

 L.2838       106  LOAD_GLOBAL              ndarray
              108  LOAD_METHOD              view
              110  LOAD_DEREF               '_data'
              112  LOAD_FAST                'cls'
              114  CALL_METHOD_2         2  '2 positional arguments'
              116  STORE_DEREF              '_data'
            118_0  COME_FROM           104  '104'

 L.2840       118  LOAD_GLOBAL              hasattr
              120  LOAD_FAST                'data'
              122  LOAD_STR                 '_mask'
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  POP_JUMP_IF_FALSE   150  'to 150'
              128  LOAD_GLOBAL              isinstance
              130  LOAD_FAST                'data'
              132  LOAD_GLOBAL              ndarray
              134  CALL_FUNCTION_2       2  '2 positional arguments'
              136  POP_JUMP_IF_TRUE    150  'to 150'

 L.2841       138  LOAD_FAST                'data'
              140  LOAD_ATTR                _mask
              142  LOAD_DEREF               '_data'
              144  STORE_ATTR               _mask

 L.2843       146  LOAD_CONST               True
              148  STORE_FAST               '_sharedmask'
            150_0  COME_FROM           136  '136'
            150_1  COME_FROM           126  '126'

 L.2846       150  LOAD_GLOBAL              make_mask_descr
              152  LOAD_DEREF               '_data'
              154  LOAD_ATTR                dtype
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  STORE_DEREF              'mdtype'

 L.2848       160  LOAD_FAST                'mask'
              162  LOAD_GLOBAL              nomask
              164  COMPARE_OP               is
          166_168  POP_JUMP_IF_FALSE   370  'to 370'

 L.2851       170  LOAD_FAST                'keep_mask'
              172  POP_JUMP_IF_TRUE    206  'to 206'

 L.2853       174  LOAD_FAST                'shrink'
              176  POP_JUMP_IF_FALSE   186  'to 186'

 L.2854       178  LOAD_GLOBAL              nomask
              180  LOAD_DEREF               '_data'
              182  STORE_ATTR               _mask
              184  JUMP_FORWARD        204  'to 204'
            186_0  COME_FROM           176  '176'

 L.2857       186  LOAD_GLOBAL              np
              188  LOAD_ATTR                zeros
              190  LOAD_DEREF               '_data'
              192  LOAD_ATTR                shape
              194  LOAD_DEREF               'mdtype'
              196  LOAD_CONST               ('dtype',)
              198  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              200  LOAD_DEREF               '_data'
              202  STORE_ATTR               _mask
            204_0  COME_FROM           184  '184'
              204  JUMP_FORWARD        734  'to 734'
            206_0  COME_FROM           172  '172'

 L.2859       206  LOAD_GLOBAL              isinstance
              208  LOAD_FAST                'data'
              210  LOAD_GLOBAL              tuple
              212  LOAD_GLOBAL              list
              214  BUILD_TUPLE_2         2 
              216  CALL_FUNCTION_2       2  '2 positional arguments'
          218_220  POP_JUMP_IF_FALSE   316  'to 316'

 L.2860       222  SETUP_EXCEPT        256  'to 256'

 L.2862       224  LOAD_GLOBAL              np
              226  LOAD_ATTR                array

 L.2863       228  LOAD_CLOSURE             '_data'
              230  BUILD_TUPLE_1         1 
              232  LOAD_LISTCOMP            '<code_object <listcomp>>'
              234  LOAD_STR                 'MaskedArray.__new__.<locals>.<listcomp>'
              236  MAKE_FUNCTION_8          'closure'

 L.2864       238  LOAD_FAST                'data'
              240  GET_ITER         
              242  CALL_FUNCTION_1       1  '1 positional argument'
              244  LOAD_DEREF               'mdtype'
              246  LOAD_CONST               ('dtype',)
              248  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              250  STORE_FAST               'mask'
              252  POP_BLOCK        
              254  JUMP_FORWARD        282  'to 282'
            256_0  COME_FROM_EXCEPT    222  '222'

 L.2865       256  DUP_TOP          
              258  LOAD_GLOBAL              ValueError
              260  COMPARE_OP               exception-match
          262_264  POP_JUMP_IF_FALSE   280  'to 280'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L.2867       272  LOAD_GLOBAL              nomask
              274  STORE_FAST               'mask'
              276  POP_EXCEPT       
              278  JUMP_FORWARD        282  'to 282'
            280_0  COME_FROM           262  '262'
              280  END_FINALLY      
            282_0  COME_FROM           278  '278'
            282_1  COME_FROM           254  '254'

 L.2869       282  LOAD_DEREF               'mdtype'
              284  LOAD_GLOBAL              MaskType
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   366  'to 366'
              292  LOAD_FAST                'mask'
              294  LOAD_METHOD              any
              296  CALL_METHOD_0         0  '0 positional arguments'
          298_300  POP_JUMP_IF_FALSE   366  'to 366'

 L.2870       302  LOAD_FAST                'mask'
              304  LOAD_DEREF               '_data'
              306  STORE_ATTR               _mask

 L.2871       308  LOAD_CONST               False
              310  LOAD_DEREF               '_data'
              312  STORE_ATTR               _sharedmask
              314  JUMP_FORWARD        734  'to 734'
            316_0  COME_FROM           218  '218'

 L.2873       316  LOAD_FAST                'copy'
              318  UNARY_NOT        
              320  LOAD_DEREF               '_data'
              322  STORE_ATTR               _sharedmask

 L.2874       324  LOAD_FAST                'copy'
          326_328  POP_JUMP_IF_FALSE   734  'to 734'

 L.2875       330  LOAD_DEREF               '_data'
              332  LOAD_ATTR                _mask
              334  LOAD_METHOD              copy
              336  CALL_METHOD_0         0  '0 positional arguments'
              338  LOAD_DEREF               '_data'
              340  STORE_ATTR               _mask

 L.2877       342  LOAD_GLOBAL              getmask
              344  LOAD_FAST                'data'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  LOAD_GLOBAL              nomask
              350  COMPARE_OP               is-not
          352_354  POP_JUMP_IF_FALSE   734  'to 734'

 L.2878       356  LOAD_FAST                'data'
              358  LOAD_ATTR                shape
              360  LOAD_FAST                'data'
              362  LOAD_ATTR                _mask
              364  STORE_ATTR               shape
            366_0  COME_FROM           298  '298'
            366_1  COME_FROM           288  '288'
          366_368  JUMP_FORWARD        734  'to 734'
            370_0  COME_FROM           166  '166'

 L.2882       370  LOAD_FAST                'mask'
              372  LOAD_CONST               True
              374  COMPARE_OP               is
          376_378  POP_JUMP_IF_FALSE   408  'to 408'
              380  LOAD_DEREF               'mdtype'
              382  LOAD_GLOBAL              MaskType
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   408  'to 408'

 L.2883       390  LOAD_GLOBAL              np
              392  LOAD_ATTR                ones
              394  LOAD_DEREF               '_data'
              396  LOAD_ATTR                shape
              398  LOAD_DEREF               'mdtype'
              400  LOAD_CONST               ('dtype',)
              402  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              404  STORE_FAST               'mask'
              406  JUMP_FORWARD        518  'to 518'
            408_0  COME_FROM           386  '386'
            408_1  COME_FROM           376  '376'

 L.2884       408  LOAD_FAST                'mask'
              410  LOAD_CONST               False
              412  COMPARE_OP               is
          414_416  POP_JUMP_IF_FALSE   446  'to 446'
              418  LOAD_DEREF               'mdtype'
              420  LOAD_GLOBAL              MaskType
              422  COMPARE_OP               ==
          424_426  POP_JUMP_IF_FALSE   446  'to 446'

 L.2885       428  LOAD_GLOBAL              np
              430  LOAD_ATTR                zeros
              432  LOAD_DEREF               '_data'
              434  LOAD_ATTR                shape
              436  LOAD_DEREF               'mdtype'
              438  LOAD_CONST               ('dtype',)
              440  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              442  STORE_FAST               'mask'
              444  JUMP_FORWARD        518  'to 518'
            446_0  COME_FROM           424  '424'
            446_1  COME_FROM           414  '414'

 L.2888       446  SETUP_EXCEPT        468  'to 468'

 L.2889       448  LOAD_GLOBAL              np
              450  LOAD_ATTR                array
              452  LOAD_FAST                'mask'
              454  LOAD_FAST                'copy'
              456  LOAD_DEREF               'mdtype'
              458  LOAD_CONST               ('copy', 'dtype')
              460  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              462  STORE_FAST               'mask'
              464  POP_BLOCK        
              466  JUMP_FORWARD        518  'to 518'
            468_0  COME_FROM_EXCEPT    446  '446'

 L.2891       468  DUP_TOP          
              470  LOAD_GLOBAL              TypeError
              472  COMPARE_OP               exception-match
          474_476  POP_JUMP_IF_FALSE   516  'to 516'
              478  POP_TOP          
              480  POP_TOP          
              482  POP_TOP          

 L.2892       484  LOAD_GLOBAL              np
              486  LOAD_ATTR                array
              488  LOAD_CLOSURE             'mdtype'
              490  BUILD_TUPLE_1         1 
              492  LOAD_LISTCOMP            '<code_object <listcomp>>'
              494  LOAD_STR                 'MaskedArray.__new__.<locals>.<listcomp>'
              496  MAKE_FUNCTION_8          'closure'
              498  LOAD_FAST                'mask'
              500  GET_ITER         
              502  CALL_FUNCTION_1       1  '1 positional argument'

 L.2893       504  LOAD_DEREF               'mdtype'
              506  LOAD_CONST               ('dtype',)
              508  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              510  STORE_FAST               'mask'
              512  POP_EXCEPT       
              514  JUMP_FORWARD        518  'to 518'
            516_0  COME_FROM           474  '474'
              516  END_FINALLY      
            518_0  COME_FROM           514  '514'
            518_1  COME_FROM           466  '466'
            518_2  COME_FROM           444  '444'
            518_3  COME_FROM           406  '406'

 L.2895       518  LOAD_FAST                'mask'
              520  LOAD_ATTR                shape
              522  LOAD_DEREF               '_data'
              524  LOAD_ATTR                shape
              526  COMPARE_OP               !=
          528_530  POP_JUMP_IF_FALSE   622  'to 622'

 L.2896       532  LOAD_DEREF               '_data'
              534  LOAD_ATTR                size
              536  LOAD_FAST                'mask'
              538  LOAD_ATTR                size
              540  ROT_TWO          
              542  STORE_FAST               'nd'
              544  STORE_FAST               'nm'

 L.2897       546  LOAD_FAST                'nm'
              548  LOAD_CONST               1
              550  COMPARE_OP               ==
          552_554  POP_JUMP_IF_FALSE   572  'to 572'

 L.2898       556  LOAD_GLOBAL              np
              558  LOAD_METHOD              resize
              560  LOAD_FAST                'mask'
              562  LOAD_DEREF               '_data'
              564  LOAD_ATTR                shape
              566  CALL_METHOD_2         2  '2 positional arguments'
              568  STORE_FAST               'mask'
              570  JUMP_FORWARD        618  'to 618'
            572_0  COME_FROM           552  '552'

 L.2899       572  LOAD_FAST                'nm'
              574  LOAD_FAST                'nd'
              576  COMPARE_OP               ==
          578_580  POP_JUMP_IF_FALSE   598  'to 598'

 L.2900       582  LOAD_GLOBAL              np
              584  LOAD_METHOD              reshape
              586  LOAD_FAST                'mask'
              588  LOAD_DEREF               '_data'
              590  LOAD_ATTR                shape
              592  CALL_METHOD_2         2  '2 positional arguments'
              594  STORE_FAST               'mask'
              596  JUMP_FORWARD        618  'to 618'
            598_0  COME_FROM           578  '578'

 L.2902       598  LOAD_STR                 'Mask and data not compatible: data size is %i, mask size is %i.'
              600  STORE_FAST               'msg'

 L.2904       602  LOAD_GLOBAL              MaskError
              604  LOAD_FAST                'msg'
              606  LOAD_FAST                'nd'
              608  LOAD_FAST                'nm'
              610  BUILD_TUPLE_2         2 
              612  BINARY_MODULO    
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  RAISE_VARARGS_1       1  'exception instance'
            618_0  COME_FROM           596  '596'
            618_1  COME_FROM           570  '570'

 L.2905       618  LOAD_CONST               True
              620  STORE_FAST               'copy'
            622_0  COME_FROM           528  '528'

 L.2907       622  LOAD_DEREF               '_data'
              624  LOAD_ATTR                _mask
              626  LOAD_GLOBAL              nomask
              628  COMPARE_OP               is
          630_632  POP_JUMP_IF_FALSE   650  'to 650'

 L.2908       634  LOAD_FAST                'mask'
              636  LOAD_DEREF               '_data'
              638  STORE_ATTR               _mask

 L.2909       640  LOAD_FAST                'copy'
              642  UNARY_NOT        
              644  LOAD_DEREF               '_data'
              646  STORE_ATTR               _sharedmask
              648  JUMP_FORWARD        734  'to 734'
            650_0  COME_FROM           630  '630'

 L.2911       650  LOAD_FAST                'keep_mask'
          652_654  POP_JUMP_IF_TRUE    672  'to 672'

 L.2912       656  LOAD_FAST                'mask'
              658  LOAD_DEREF               '_data'
              660  STORE_ATTR               _mask

 L.2913       662  LOAD_FAST                'copy'
              664  UNARY_NOT        
              666  LOAD_DEREF               '_data'
              668  STORE_ATTR               _sharedmask
              670  JUMP_FORWARD        734  'to 734'
            672_0  COME_FROM           652  '652'

 L.2915       672  LOAD_DEREF               '_data'
              674  LOAD_ATTR                dtype
              676  LOAD_ATTR                names
              678  LOAD_CONST               None
              680  COMPARE_OP               is-not
          682_684  POP_JUMP_IF_FALSE   712  'to 712'

 L.2916       686  LOAD_CLOSURE             '_recursive_or'
              688  BUILD_TUPLE_1         1 
              690  LOAD_CODE                <code_object _recursive_or>
              692  LOAD_STR                 'MaskedArray.__new__.<locals>._recursive_or'
              694  MAKE_FUNCTION_8          'closure'
              696  STORE_DEREF              '_recursive_or'

 L.2925       698  LOAD_DEREF               '_recursive_or'
              700  LOAD_DEREF               '_data'
              702  LOAD_ATTR                _mask
              704  LOAD_FAST                'mask'
              706  CALL_FUNCTION_2       2  '2 positional arguments'
              708  POP_TOP          
              710  JUMP_FORWARD        728  'to 728'
            712_0  COME_FROM           682  '682'

 L.2927       712  LOAD_GLOBAL              np
              714  LOAD_METHOD              logical_or
              716  LOAD_FAST                'mask'
              718  LOAD_DEREF               '_data'
              720  LOAD_ATTR                _mask
              722  CALL_METHOD_2         2  '2 positional arguments'
              724  LOAD_DEREF               '_data'
              726  STORE_ATTR               _mask
            728_0  COME_FROM           710  '710'

 L.2928       728  LOAD_CONST               False
              730  LOAD_DEREF               '_data'
              732  STORE_ATTR               _sharedmask
            734_0  COME_FROM           670  '670'
            734_1  COME_FROM           648  '648'
            734_2  COME_FROM           366  '366'
            734_3  COME_FROM           352  '352'
            734_4  COME_FROM           326  '326'
            734_5  COME_FROM           314  '314'
            734_6  COME_FROM           204  '204'

 L.2930       734  LOAD_FAST                'fill_value'
              736  LOAD_CONST               None
              738  COMPARE_OP               is
          740_742  POP_JUMP_IF_FALSE   756  'to 756'

 L.2931       744  LOAD_GLOBAL              getattr
              746  LOAD_FAST                'data'
              748  LOAD_STR                 '_fill_value'
              750  LOAD_CONST               None
              752  CALL_FUNCTION_3       3  '3 positional arguments'
              754  STORE_FAST               'fill_value'
            756_0  COME_FROM           740  '740'

 L.2933       756  LOAD_FAST                'fill_value'
              758  LOAD_CONST               None
              760  COMPARE_OP               is-not
          762_764  POP_JUMP_IF_FALSE   780  'to 780'

 L.2934       766  LOAD_GLOBAL              _check_fill_value
              768  LOAD_FAST                'fill_value'
              770  LOAD_DEREF               '_data'
              772  LOAD_ATTR                dtype
              774  CALL_FUNCTION_2       2  '2 positional arguments'
              776  LOAD_DEREF               '_data'
              778  STORE_ATTR               _fill_value
            780_0  COME_FROM           762  '762'

 L.2936       780  LOAD_FAST                'hard_mask'
              782  LOAD_CONST               None
              784  COMPARE_OP               is
          786_788  POP_JUMP_IF_FALSE   806  'to 806'

 L.2937       790  LOAD_GLOBAL              getattr
              792  LOAD_FAST                'data'
              794  LOAD_STR                 '_hardmask'
              796  LOAD_CONST               False
              798  CALL_FUNCTION_3       3  '3 positional arguments'
              800  LOAD_DEREF               '_data'
              802  STORE_ATTR               _hardmask
              804  JUMP_FORWARD        812  'to 812'
            806_0  COME_FROM           786  '786'

 L.2939       806  LOAD_FAST                'hard_mask'
              808  LOAD_DEREF               '_data'
              810  STORE_ATTR               _hardmask
            812_0  COME_FROM           804  '804'

 L.2940       812  LOAD_FAST                '_baseclass'
              814  LOAD_DEREF               '_data'
              816  STORE_ATTR               _baseclass

 L.2941       818  LOAD_DEREF               '_data'
              820  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 734

    def _update_from(self, obj):
        """
        Copies some attributes of obj to self.

        """
        if isinstance(obj, ndarray):
            _baseclass = type(obj)
        else:
            _baseclass = ndarray
        _optinfo = {}
        _optinfo.update(getattr(obj, '_optinfo', {}))
        _optinfo.update(getattr(obj, '_basedict', {}))
        if not isinstance(obj, MaskedArray):
            _optinfo.update(getattr(obj, '__dict__', {}))
        _dict = dict(_fill_value=(getattr(obj, '_fill_value', None)), _hardmask=(getattr(obj, '_hardmask', False)),
          _sharedmask=(getattr(obj, '_sharedmask', False)),
          _isfield=(getattr(obj, '_isfield', False)),
          _baseclass=(getattr(obj, '_baseclass', _baseclass)),
          _optinfo=_optinfo,
          _basedict=_optinfo)
        self.__dict__.update(_dict)
        self.__dict__.update(_optinfo)

    def __array_finalize__(self, obj):
        """
        Finalizes the masked array.

        """
        self._update_from(obj)
        if isinstance(obj, ndarray):
            if obj.dtype.names is not None:
                _mask = getmaskarray(obj)
            else:
                _mask = getmask(obj)
            if _mask is not nomask and obj.__array_interface__['data'][0] != self.__array_interface__['data'][0]:
                if self.dtype == obj.dtype:
                    _mask_dtype = _mask.dtype
                else:
                    _mask_dtype = make_mask_descr(self.dtype)
                if self.flags.c_contiguous:
                    order = 'C'
                elif self.flags.f_contiguous:
                    order = 'F'
                else:
                    order = 'K'
                _mask = _mask.astype(_mask_dtype, order)
            else:
                _mask = _mask.view()
        else:
            _mask = nomask
        self._mask = _mask
        if self._mask is not nomask:
            try:
                self._mask.shape = self.shape
            except ValueError:
                self._mask = nomask
            except (TypeError, AttributeError):
                pass

        if self._fill_value is not None:
            self._fill_value = _check_fill_value(self._fill_value, self.dtype)
        elif self.dtype.names is not None:
            self._fill_value = _check_fill_value(None, self.dtype)

    def __array_wrap__(self, obj, context=None):
        """
        Special hook for ufuncs.

        Wraps the numpy array and sets the mask according to context.

        """
        if obj is self:
            result = obj
        else:
            result = obj.view(type(self))
            result._update_from(self)
        if context is not None:
            result._mask = result._mask.copy()
            func, args, out_i = context
            input_args = args[:func.nin]
            m = reduce(mask_or, [getmaskarray(arg) for arg in input_args])
            domain = ufunc_domain.get(func, None)
            if domain is not None:
                with np.errstate(divide='ignore', invalid='ignore'):
                    d = filled(domain(*input_args), True)
                if d.any():
                    try:
                        fill_value = ufunc_fills[func][(-1)]
                    except TypeError:
                        fill_value = ufunc_fills[func]
                    except KeyError:
                        fill_value = self.fill_value

                    np.copyto(result, fill_value, where=d)
                    if m is nomask:
                        m = d
                    else:
                        m = m | d
            if result is not self:
                if result.shape == ():
                    if m:
                        return masked
            result._mask = m
            result._sharedmask = False
        return result

    def view(self, dtype=None, type=None, fill_value=None):
        """
        Return a view of the MaskedArray data.

        Parameters
        ----------
        dtype : data-type or ndarray sub-class, optional
            Data-type descriptor of the returned view, e.g., float32 or int16.
            The default, None, results in the view having the same data-type
            as `a`. As with ``ndarray.view``, dtype can also be specified as
            an ndarray sub-class, which then specifies the type of the
            returned object (this is equivalent to setting the ``type``
            parameter).
        type : Python type, optional
            Type of the returned view, either ndarray or a subclass.  The
            default None results in type preservation.
        fill_value : scalar, optional
            The value to use for invalid entries (None by default).
            If None, then this argument is inferred from the passed `dtype`, or
            in its absence the original array, as discussed in the notes below.

        See Also
        --------
        numpy.ndarray.view : Equivalent method on ndarray object.

        Notes
        -----

        ``a.view()`` is used two different ways:

        ``a.view(some_dtype)`` or ``a.view(dtype=some_dtype)`` constructs a view
        of the array's memory with a different data-type.  This can cause a
        reinterpretation of the bytes of memory.

        ``a.view(ndarray_subclass)`` or ``a.view(type=ndarray_subclass)`` just
        returns an instance of `ndarray_subclass` that looks at the same array
        (same shape, dtype, etc.)  This does not cause a reinterpretation of the
        memory.

        If `fill_value` is not specified, but `dtype` is specified (and is not
        an ndarray sub-class), the `fill_value` of the MaskedArray will be
        reset. If neither `fill_value` nor `dtype` are specified (or if
        `dtype` is an ndarray sub-class), then the fill value is preserved.
        Finally, if `fill_value` is specified, but `dtype` is not, the fill
        value is set to the specified value.

        For ``a.view(some_dtype)``, if ``some_dtype`` has a different number of
        bytes per entry than the previous dtype (for example, converting a
        regular array to a structured array), then the behavior of the view
        cannot be predicted just from the superficial appearance of ``a`` (shown
        by ``print(a)``). It also depends on exactly how ``a`` is stored in
        memory. Therefore if ``a`` is C-ordered versus fortran-ordered, versus
        defined as a slice or transpose, etc., the view may give different
        results.
        """
        if dtype is None:
            if type is None:
                output = ndarray.view(self)
            else:
                output = ndarray.view(self, type)
        elif type is None:
            try:
                if issubclass(dtype, ndarray):
                    output = ndarray.view(self, dtype)
                    dtype = None
                else:
                    output = ndarray.view(self, dtype)
            except TypeError:
                output = ndarray.view(self, dtype)

        else:
            output = ndarray.view(self, dtype, type)
        if getmask(output) is not nomask:
            output._mask = output._mask.view()
        if getattr(output, '_fill_value', None) is not None:
            if fill_value is None:
                if dtype is None:
                    pass
                else:
                    output._fill_value = None
            else:
                output.fill_value = fill_value
        return output

    def __getitem__--- This code section failed: ---

 L.3220         0  LOAD_FAST                'self'
                2  LOAD_ATTR                data
                4  LOAD_FAST                'indx'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'dout'

 L.3221        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _mask
               14  STORE_FAST               '_mask'

 L.3223        16  LOAD_CODE                <code_object _is_scalar>
               18  LOAD_STR                 'MaskedArray.__getitem__.<locals>._is_scalar'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  STORE_FAST               '_is_scalar'

 L.3226        24  LOAD_CODE                <code_object _scalar_heuristic>
               26  LOAD_STR                 'MaskedArray.__getitem__.<locals>._scalar_heuristic'
               28  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               30  STORE_FAST               '_scalar_heuristic'

 L.3249        32  LOAD_FAST                '_mask'
               34  LOAD_GLOBAL              nomask
               36  COMPARE_OP               is-not
               38  POP_JUMP_IF_FALSE    58  'to 58'

 L.3252        40  LOAD_FAST                '_mask'
               42  LOAD_FAST                'indx'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'mout'

 L.3253        48  LOAD_FAST                '_is_scalar'
               50  LOAD_FAST                'mout'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  STORE_FAST               'scalar_expected'
               56  JUMP_FORWARD         98  'to 98'
             58_0  COME_FROM            38  '38'

 L.3257        58  LOAD_GLOBAL              nomask
               60  STORE_FAST               'mout'

 L.3258        62  LOAD_FAST                '_scalar_heuristic'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                data
               68  LOAD_FAST                'dout'
               70  CALL_FUNCTION_2       2  '2 positional arguments'
               72  STORE_FAST               'scalar_expected'

 L.3259        74  LOAD_FAST                'scalar_expected'
               76  LOAD_CONST               None
               78  COMPARE_OP               is
               80  POP_JUMP_IF_FALSE    98  'to 98'

 L.3263        82  LOAD_FAST                '_is_scalar'
               84  LOAD_GLOBAL              getmaskarray
               86  LOAD_FAST                'self'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  LOAD_FAST                'indx'
               92  BINARY_SUBSCR    
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  STORE_FAST               'scalar_expected'
             98_0  COME_FROM            80  '80'
             98_1  COME_FROM            56  '56'

 L.3266        98  LOAD_FAST                'scalar_expected'
              100  POP_JUMP_IF_FALSE   200  'to 200'

 L.3268       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'dout'
              106  LOAD_GLOBAL              np
              108  LOAD_ATTR                void
              110  CALL_FUNCTION_2       2  '2 positional arguments'
              112  POP_JUMP_IF_FALSE   130  'to 130'

 L.3272       114  LOAD_GLOBAL              mvoid
              116  LOAD_FAST                'dout'
              118  LOAD_FAST                'mout'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _hardmask
              124  LOAD_CONST               ('mask', 'hardmask')
              126  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              128  RETURN_VALUE     
            130_0  COME_FROM           112  '112'

 L.3275       130  LOAD_FAST                'self'
              132  LOAD_ATTR                dtype
              134  LOAD_ATTR                type
              136  LOAD_GLOBAL              np
              138  LOAD_ATTR                object_
              140  COMPARE_OP               is
              142  POP_JUMP_IF_FALSE   186  'to 186'

 L.3276       144  LOAD_GLOBAL              isinstance
              146  LOAD_FAST                'dout'
              148  LOAD_GLOBAL              np
              150  LOAD_ATTR                ndarray
              152  CALL_FUNCTION_2       2  '2 positional arguments'
              154  POP_JUMP_IF_FALSE   186  'to 186'

 L.3277       156  LOAD_FAST                'dout'
              158  LOAD_GLOBAL              masked
              160  COMPARE_OP               is-not
              162  POP_JUMP_IF_FALSE   186  'to 186'

 L.3279       164  LOAD_FAST                'mout'
              166  POP_JUMP_IF_FALSE   180  'to 180'

 L.3280       168  LOAD_GLOBAL              MaskedArray
              170  LOAD_FAST                'dout'
              172  LOAD_CONST               True
              174  LOAD_CONST               ('mask',)
              176  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              178  RETURN_VALUE     
            180_0  COME_FROM           166  '166'

 L.3282       180  LOAD_FAST                'dout'
              182  RETURN_VALUE     
              184  JUMP_FORWARD        198  'to 198'
            186_0  COME_FROM           162  '162'
            186_1  COME_FROM           154  '154'
            186_2  COME_FROM           142  '142'

 L.3286       186  LOAD_FAST                'mout'
              188  POP_JUMP_IF_FALSE   194  'to 194'

 L.3287       190  LOAD_GLOBAL              masked
              192  RETURN_VALUE     
            194_0  COME_FROM           188  '188'

 L.3289       194  LOAD_FAST                'dout'
              196  RETURN_VALUE     
            198_0  COME_FROM           184  '184'
              198  JUMP_FORWARD        416  'to 416'
            200_0  COME_FROM           100  '100'

 L.3292       200  LOAD_FAST                'dout'
              202  LOAD_METHOD              view
              204  LOAD_GLOBAL              type
              206  LOAD_FAST                'self'
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  STORE_FAST               'dout'

 L.3294       214  LOAD_FAST                'dout'
              216  LOAD_METHOD              _update_from
              218  LOAD_FAST                'self'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  POP_TOP          

 L.3296       224  LOAD_GLOBAL              is_string_or_list_of_strings
              226  LOAD_FAST                'indx'
              228  CALL_FUNCTION_1       1  '1 positional argument'
          230_232  POP_JUMP_IF_FALSE   386  'to 386'

 L.3297       234  LOAD_FAST                'self'
              236  LOAD_ATTR                _fill_value
              238  LOAD_CONST               None
              240  COMPARE_OP               is-not
          242_244  POP_JUMP_IF_FALSE   380  'to 380'

 L.3298       246  LOAD_FAST                'self'
              248  LOAD_ATTR                _fill_value
              250  LOAD_FAST                'indx'
              252  BINARY_SUBSCR    
              254  LOAD_FAST                'dout'
              256  STORE_ATTR               _fill_value

 L.3302       258  LOAD_GLOBAL              isinstance
              260  LOAD_FAST                'dout'
              262  LOAD_ATTR                _fill_value
              264  LOAD_GLOBAL              np
              266  LOAD_ATTR                ndarray
              268  CALL_FUNCTION_2       2  '2 positional arguments'
          270_272  POP_JUMP_IF_TRUE    282  'to 282'

 L.3303       274  LOAD_GLOBAL              RuntimeError
              276  LOAD_STR                 'Internal NumPy error.'
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  RAISE_VARARGS_1       1  'exception instance'
            282_0  COME_FROM           270  '270'

 L.3312       282  LOAD_FAST                'dout'
              284  LOAD_ATTR                _fill_value
              286  LOAD_ATTR                ndim
              288  LOAD_CONST               0
              290  COMPARE_OP               >
          292_294  POP_JUMP_IF_FALSE   380  'to 380'

 L.3313       296  LOAD_FAST                'dout'
              298  LOAD_ATTR                _fill_value

 L.3314       300  LOAD_FAST                'dout'
              302  LOAD_ATTR                _fill_value
              304  LOAD_ATTR                flat
              306  LOAD_CONST               0
              308  BINARY_SUBSCR    
              310  COMPARE_OP               ==
              312  LOAD_METHOD              all
              314  CALL_METHOD_0         0  '0 positional arguments'
          316_318  POP_JUMP_IF_TRUE    354  'to 354'

 L.3315       320  LOAD_GLOBAL              warnings
              322  LOAD_ATTR                warn

 L.3316       324  LOAD_STR                 'Upon accessing multidimensional field '
              326  LOAD_FAST                'indx'
              328  FORMAT_VALUE          1  '!s'
              330  LOAD_STR                 ', need to keep dimensionality of fill_value at 0. Discarding heterogeneous fill_value and setting all to '
              332  LOAD_FAST                'dout'
              334  LOAD_ATTR                _fill_value
              336  LOAD_CONST               0
              338  BINARY_SUBSCR    
              340  FORMAT_VALUE          1  '!s'
              342  LOAD_STR                 '.'
              344  BUILD_STRING_5        5 

 L.3321       346  LOAD_CONST               2
              348  LOAD_CONST               ('stacklevel',)
              350  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              352  POP_TOP          
            354_0  COME_FROM           316  '316'

 L.3325       354  LOAD_FAST                'dout'
              356  LOAD_ATTR                _fill_value
              358  LOAD_ATTR                flat
              360  LOAD_CONST               0
              362  LOAD_CONST               1
              364  BUILD_SLICE_2         2 
              366  BINARY_SUBSCR    
              368  LOAD_ATTR                squeeze
              370  LOAD_CONST               0
              372  LOAD_CONST               ('axis',)
              374  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              376  LOAD_FAST                'dout'
              378  STORE_ATTR               _fill_value
            380_0  COME_FROM           292  '292'
            380_1  COME_FROM           242  '242'

 L.3326       380  LOAD_CONST               True
              382  LOAD_FAST                'dout'
              384  STORE_ATTR               _isfield
            386_0  COME_FROM           230  '230'

 L.3328       386  LOAD_FAST                'mout'
              388  LOAD_GLOBAL              nomask
              390  COMPARE_OP               is-not
          392_394  POP_JUMP_IF_FALSE   416  'to 416'

 L.3330       396  LOAD_GLOBAL              reshape
              398  LOAD_FAST                'mout'
              400  LOAD_FAST                'dout'
              402  LOAD_ATTR                shape
              404  CALL_FUNCTION_2       2  '2 positional arguments'
              406  LOAD_FAST                'dout'
              408  STORE_ATTR               _mask

 L.3331       410  LOAD_CONST               True
              412  LOAD_FAST                'dout'
              414  STORE_ATTR               _sharedmask
            416_0  COME_FROM           392  '392'
            416_1  COME_FROM           198  '198'

 L.3333       416  LOAD_FAST                'dout'
              418  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 198

    def __setitem__(self, indx, value):
        """
        x.__setitem__(i, y) <==> x[i]=y

        Set item described by index. If value is masked, masks those
        locations.

        """
        if self is masked:
            raise MaskError('Cannot alter the masked element.')
        _data = self._data
        _mask = self._mask
        if isinstance(indx, str):
            _data[indx] = value
            if _mask is nomask:
                self._mask = _mask = make_mask_none(self.shape, self.dtype)
            _mask[indx] = getmask(value)
            return
        _dtype = _data.dtype
        if value is masked:
            if _mask is nomask:
                _mask = self._mask = make_mask_none(self.shape, _dtype)
            if _dtype.names is not None:
                _mask[indx] = tuple([True] * len(_dtype.names))
            else:
                _mask[indx] = True
            return
        dval = getattr(value, '_data', value)
        mval = getmask(value)
        if _dtype.names is not None:
            if mval is nomask:
                mval = tuple([False] * len(_dtype.names))
        if _mask is nomask:
            _data[indx] = dval
            if mval is not nomask:
                _mask = self._mask = make_mask_none(self.shape, _dtype)
                _mask[indx] = mval
        elif not self._hardmask:
            _data[indx] = dval
            _mask[indx] = mval
        elif hasattr(indx, 'dtype') and indx.dtype == MaskType:
            indx = indx * umath.logical_not(_mask)
            _data[indx] = dval
        else:
            if _dtype.names is not None:
                err_msg = "Flexible 'hard' masks are not yet supported."
                raise NotImplementedError(err_msg)
            mindx = mask_or((_mask[indx]), mval, copy=True)
            dindx = self._data[indx]
            if dindx.size > 1:
                np.copyto(dindx, dval, where=(~mindx))
            elif mindx is nomask:
                dindx = dval
            _data[indx] = dindx
            _mask[indx] = mindx

    @property
    def dtype(self):
        return super(MaskedArray, self).dtype

    @dtype.setter
    def dtype(self, dtype):
        super(MaskedArray, type(self)).dtype.__set__(self, dtype)
        if self._mask is not nomask:
            self._mask = self._mask.view(make_mask_descr(dtype), ndarray)
            try:
                self._mask.shape = self.shape
            except (AttributeError, TypeError):
                pass

    @property
    def shape(self):
        return super(MaskedArray, self).shape

    @shape.setter
    def shape(self, shape):
        super(MaskedArray, type(self)).shape.__set__(self, shape)
        if getmask(self) is not nomask:
            self._mask.shape = self.shape

    def __setmask__(self, mask, copy=False):
        """
        Set the mask.

        """
        idtype = self.dtype
        current_mask = self._mask
        if mask is masked:
            mask = True
        if current_mask is nomask:
            if mask is nomask:
                return
            current_mask = self._mask = make_mask_none(self.shape, idtype)
        if idtype.names is None:
            if self._hardmask:
                current_mask |= mask
            elif isinstance(mask, (int, float, np.bool_, np.number)):
                current_mask[...] = mask
            else:
                current_mask.flat = mask
        else:
            mdtype = current_mask.dtype
            mask = np.array(mask, copy=False)
            if not mask.ndim:
                if mask.dtype.kind == 'b':
                    mask = np.array((tuple([mask.item()] * len(mdtype))), dtype=mdtype)
                else:
                    mask = mask.astype(mdtype)
            else:
                try:
                    mask = np.array(mask, copy=copy, dtype=mdtype)
                except TypeError:
                    mask = np.array([tuple([m] * len(mdtype)) for m in mask], dtype=mdtype)

            if self._hardmask:
                for n in idtype.names:
                    current_mask[n] |= mask[n]

            elif isinstance(mask, (int, float, np.bool_, np.number)):
                current_mask[...] = mask
            else:
                current_mask.flat = mask
        if current_mask.shape:
            current_mask.shape = self.shape

    _set_mask = __setmask__

    @property
    def mask(self):
        """ Current mask. """
        return self._mask.view()

    @mask.setter
    def mask(self, value):
        self.__setmask__(value)

    @property
    def recordmask(self):
        """
        Get or set the mask of the array if it has no named fields. For
        structured arrays, returns a ndarray of booleans where entries are
        ``True`` if **all** the fields are masked, ``False`` otherwise:

        >>> x = np.ma.array([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        ...         mask=[(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
        ...        dtype=[('a', int), ('b', int)])
        >>> x.recordmask
        array([False, False,  True, False, False])
        """
        _mask = self._mask.view(ndarray)
        if _mask.dtype.names is None:
            return _mask
        return np.all((flatten_structured_array(_mask)), axis=(-1))

    @recordmask.setter
    def recordmask(self, mask):
        raise NotImplementedError('Coming soon: setting the mask per records!')

    def harden_mask(self):
        """
        Force the mask to hard.

        Whether the mask of a masked array is hard or soft is determined by
        its `~ma.MaskedArray.hardmask` property. `harden_mask` sets
        `~ma.MaskedArray.hardmask` to ``True``.

        See Also
        --------
        ma.MaskedArray.hardmask

        """
        self._hardmask = True
        return self

    def soften_mask(self):
        """
        Force the mask to soft.

        Whether the mask of a masked array is hard or soft is determined by
        its `~ma.MaskedArray.hardmask` property. `soften_mask` sets
        `~ma.MaskedArray.hardmask` to ``False``.

        See Also
        --------
        ma.MaskedArray.hardmask

        """
        self._hardmask = False
        return self

    @property
    def hardmask(self):
        """ Hardness of the mask """
        return self._hardmask

    def unshare_mask(self):
        """
        Copy the mask and set the sharedmask flag to False.

        Whether the mask is shared between masked arrays can be seen from
        the `sharedmask` property. `unshare_mask` ensures the mask is not shared.
        A copy of the mask is only made if it was shared.

        See Also
        --------
        sharedmask

        """
        if self._sharedmask:
            self._mask = self._mask.copy()
            self._sharedmask = False
        return self

    @property
    def sharedmask(self):
        """ Share status of the mask (read-only). """
        return self._sharedmask

    def shrink_mask(self):
        """
        Reduce a mask to nomask when possible.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> x = np.ma.array([[1,2 ], [3, 4]], mask=[0]*4)
        >>> x.mask
        array([[False, False],
               [False, False]])
        >>> x.shrink_mask()
        masked_array(
          data=[[1, 2],
                [3, 4]],
          mask=False,
          fill_value=999999)
        >>> x.mask
        False

        """
        self._mask = _shrink_mask(self._mask)
        return self

    @property
    def baseclass(self):
        """ Class of the underlying data (read-only). """
        return self._baseclass

    def _get_data(self):
        """
        Returns the underlying data, as a view of the masked array.

        If the underlying data is a subclass of :class:`numpy.ndarray`, it is
        returned as such.

        >>> x = np.ma.array(np.matrix([[1, 2], [3, 4]]), mask=[[0, 1], [1, 0]])
        >>> x.data
        matrix([[1, 2],
                [3, 4]])

        The type of the data can be accessed through the :attr:`baseclass`
        attribute.
        """
        return ndarray.view(self, self._baseclass)

    _data = property(fget=_get_data)
    data = property(fget=_get_data)

    @property
    def flat(self):
        """ Return a flat iterator, or set a flattened version of self to value. """
        return MaskedIterator(self)

    @flat.setter
    def flat(self, value):
        y = self.ravel()
        y[:] = value

    @property
    def fill_value(self):
        """
        The filling value of the masked array is a scalar. When setting, None
        will set to a default based on the data type.

        Examples
        --------
        >>> for dt in [np.int32, np.int64, np.float64, np.complex128]:
        ...     np.ma.array([0, 1], dtype=dt).get_fill_value()
        ...
        999999
        999999
        1e+20
        (1e+20+0j)

        >>> x = np.ma.array([0, 1.], fill_value=-np.inf)
        >>> x.fill_value
        -inf
        >>> x.fill_value = np.pi
        >>> x.fill_value
        3.1415926535897931 # may vary

        Reset to default:

        >>> x.fill_value = None
        >>> x.fill_value
        1e+20

        """
        if self._fill_value is None:
            self._fill_value = _check_fill_value(None, self.dtype)
        if isinstance(self._fill_value, ndarray):
            return self._fill_value[()]
        return self._fill_value

    @fill_value.setter
    def fill_value(self, value=None):
        target = _check_fill_value(value, self.dtype)
        if not target.ndim == 0:
            warnings.warn('Non-scalar arrays for the fill value are deprecated. Use arrays with scalar values instead. The filled function still supports any array as `fill_value`.',
              DeprecationWarning,
              stacklevel=2)
        _fill_value = self._fill_value
        if _fill_value is None:
            self._fill_value = target
        else:
            _fill_value[()] = target

    get_fill_value = fill_value.fget
    set_fill_value = fill_value.fset

    def filled(self, fill_value=None):
        """
        Return a copy of self, with masked values filled with a given value.
        **However**, if there are no masked values to fill, self will be
        returned instead as an ndarray.

        Parameters
        ----------
        fill_value : array_like, optional
            The value to use for invalid entries. Can be scalar or non-scalar.
            If non-scalar, the resulting ndarray must be broadcastable over
            input array. Default is None, in which case, the `fill_value`
            attribute of the array is used instead.

        Returns
        -------
        filled_array : ndarray
            A copy of ``self`` with invalid entries replaced by *fill_value*
            (be it the function argument or the attribute of ``self``), or
            ``self`` itself as an ndarray if there are no invalid entries to
            be replaced.

        Notes
        -----
        The result is **not** a MaskedArray!

        Examples
        --------
        >>> x = np.ma.array([1,2,3,4,5], mask=[0,0,1,0,1], fill_value=-999)
        >>> x.filled()
        array([   1,    2, -999,    4, -999])
        >>> x.filled(fill_value=1000)
        array([   1,    2, 1000,    4, 1000])
        >>> type(x.filled())
        <class 'numpy.ndarray'>

        Subclassing is preserved. This means that if, e.g., the data part of
        the masked array is a recarray, `filled` returns a recarray:

        >>> x = np.array([(-1, 2), (-3, 4)], dtype='i8,i8').view(np.recarray)
        >>> m = np.ma.array(x, mask=[(True, False), (False, True)])
        >>> m.filled()
        rec.array([(999999,      2), (    -3, 999999)],
                  dtype=[('f0', '<i8'), ('f1', '<i8')])
        """
        m = self._mask
        if m is nomask:
            return self._data
        if fill_value is None:
            fill_value = self.fill_value
        else:
            fill_value = _check_fill_value(fill_value, self.dtype)
        if self is masked_singleton:
            return np.asanyarray(fill_value)
        if m.dtype.names is not None:
            result = self._data.copy('K')
            _recursive_filled(result, self._mask, fill_value)
        else:
            if not m.any():
                return self._data
            result = self._data.copy('K')
            try:
                np.copyto(result, fill_value, where=m)
            except (TypeError, AttributeError):
                fill_value = narray(fill_value, dtype=object)
                d = result.astype(object)
                result = np.choose(m, (d, fill_value))
            except IndexError:
                if self._data.shape:
                    raise
                elif m:
                    result = np.array(fill_value, dtype=(self.dtype))
                else:
                    result = self._data

        return result

    def compressed(self):
        """
        Return all the non-masked data as a 1-D array.

        Returns
        -------
        data : ndarray
            A new `ndarray` holding the non-masked data is returned.

        Notes
        -----
        The result is **not** a MaskedArray!

        Examples
        --------
        >>> x = np.ma.array(np.arange(5), mask=[0]*2 + [1]*3)
        >>> x.compressed()
        array([0, 1])
        >>> type(x.compressed())
        <class 'numpy.ndarray'>

        """
        data = ndarray.ravel(self._data)
        if self._mask is not nomask:
            data = data.compress(np.logical_not(ndarray.ravel(self._mask)))
        return data

    def compress(self, condition, axis=None, out=None):
        """
        Return `a` where condition is ``True``.

        If condition is a `~ma.MaskedArray`, missing values are considered
        as ``False``.

        Parameters
        ----------
        condition : var
            Boolean 1-d array selecting which entries to return. If len(condition)
            is less than the size of a along the axis, then output is truncated
            to length of condition array.
        axis : {None, int}, optional
            Axis along which the operation must be performed.
        out : {None, ndarray}, optional
            Alternative output array in which to place the result. It must have
            the same shape as the expected output but the type will be cast if
            necessary.

        Returns
        -------
        result : MaskedArray
            A :class:`~ma.MaskedArray` object.

        Notes
        -----
        Please note the difference with :meth:`compressed` !
        The output of :meth:`compress` has a mask, the output of
        :meth:`compressed` does not.

        Examples
        --------
        >>> x = np.ma.array([[1,2,3],[4,5,6],[7,8,9]], mask=[0] + [1,0]*4)
        >>> x
        masked_array(
          data=[[1, --, 3],
                [--, 5, --],
                [7, --, 9]],
          mask=[[False,  True, False],
                [ True, False,  True],
                [False,  True, False]],
          fill_value=999999)
        >>> x.compress([1, 0, 1])
        masked_array(data=[1, 3],
                     mask=[False, False],
               fill_value=999999)

        >>> x.compress([1, 0, 1], axis=1)
        masked_array(
          data=[[1, 3],
                [--, --],
                [7, 9]],
          mask=[[False, False],
                [ True,  True],
                [False, False]],
          fill_value=999999)

        """
        _data, _mask = self._data, self._mask
        condition = np.array(condition, copy=False, subok=False)
        _new = _data.compress(condition, axis=axis, out=out).view(type(self))
        _new._update_from(self)
        if _mask is not nomask:
            _new._mask = _mask.compress(condition, axis=axis)
        return _new

    def _insert_masked_print(self):
        """
        Replace masked values with masked_print_option, casting all innermost
        dtypes to object.
        """
        if masked_print_option.enabled():
            mask = self._mask
            if mask is nomask:
                res = self._data
            else:
                data = self._data
                print_width = self._print_width if self.ndim > 1 else self._print_width_1d
                for axis in range(self.ndim):
                    if data.shape[axis] > print_width:
                        ind = print_width // 2
                        arr = np.split(data, (ind, -ind), axis=axis)
                        data = np.concatenate((arr[0], arr[2]), axis=axis)
                        arr = np.split(mask, (ind, -ind), axis=axis)
                        mask = np.concatenate((arr[0], arr[2]), axis=axis)

                rdtype = _replace_dtype_fields(self.dtype, 'O')
                res = data.astype(rdtype)
                _recursive_printoption(res, mask, masked_print_option)
        else:
            res = self.filled(self.fill_value)
        return res

    def __str__(self):
        return str(self._insert_masked_print())

    def __repr__(self):
        """
        Literal string representation.

        """
        if self._baseclass is np.ndarray:
            name = 'array'
        else:
            name = self._baseclass.__name__
        if np.get_printoptions()['legacy'] == '1.13':
            is_long = self.ndim > 1
            parameters = dict(name=name,
              nlen=(' ' * len(name)),
              data=(str(self)),
              mask=(str(self._mask)),
              fill=(str(self.fill_value)),
              dtype=(str(self.dtype)))
            is_structured = bool(self.dtype.names)
            key = '{}_{}'.format('long' if is_long else 'short', 'flx' if is_structured else 'std')
            return _legacy_print_templates[key] % parameters
        prefix = f"masked_{name}("
        dtype_needed = not np.core.arrayprint.dtype_is_implied(self.dtype) or np.all(self.mask) or self.size == 0
        keys = [
         'data', 'mask', 'fill_value']
        if dtype_needed:
            keys.append('dtype')
        is_one_row = builtins.all((dim == 1 for dim in self.shape[:-1]))
        min_indent = 2
        if is_one_row:
            indents = {}
            indents[keys[0]] = prefix
            for k in keys[1:]:
                n = builtins.max(min_indent, len(prefix + keys[0]) - len(k))
                indents[k] = ' ' * n

            prefix = ''
        else:
            indents = {k:' ' * min_indent for k in keys}
            prefix = prefix + '\n'
        reprs = {}
        reprs['data'] = np.array2string((self._insert_masked_print()),
          separator=', ',
          prefix=(indents['data'] + 'data='),
          suffix=',')
        reprs['mask'] = np.array2string((self._mask),
          separator=', ',
          prefix=(indents['mask'] + 'mask='),
          suffix=',')
        reprs['fill_value'] = repr(self.fill_value)
        if dtype_needed:
            reprs['dtype'] = np.core.arrayprint.dtype_short_repr(self.dtype)
        result = ',\n'.join(('{}{}={}'.format(indents[k], k, reprs[k]) for k in keys))
        return prefix + result + ')'

    def _delegate_binop(self, other):
        if isinstance(other, type(self)):
            return False
        array_ufunc = getattr(other, '__array_ufunc__', False)
        if array_ufunc is False:
            other_priority = getattr(other, '__array_priority__', -1000000)
            return self.__array_priority__ < other_priority
        return array_ufunc is None

    def _comparison(self, other, compare):
        """Compare self with other using operator.eq or operator.ne.

        When either of the elements is masked, the result is masked as well,
        but the underlying boolean data are still set, with self and other
        considered equal if both are masked, and unequal otherwise.

        For structured arrays, all fields are combined, with masked values
        ignored. The result is masked if all fields were masked, with self
        and other considered equal only if both were fully masked.
        """
        omask = getmask(other)
        smask = self.mask
        mask = mask_or(smask, omask, copy=True)
        odata = getdata(other)
        if mask.dtype.names is not None:
            broadcast_shape = np.broadcast(self, odata).shape
            sbroadcast = np.broadcast_to(self, broadcast_shape, subok=True)
            sbroadcast._mask = mask
            sdata = sbroadcast.filled(odata)
            mask = mask == np.ones((), mask.dtype)
        else:
            sdata = self.data
        check = compare(sdata, odata)
        if isinstance(check, (np.bool_, bool)):
            if mask:
                return masked
            return check
        if mask is not nomask:
            check = np.where(mask, compare(smask, omask), check)
            if mask.shape != check.shape:
                mask = np.broadcast_to(mask, check.shape).copy()
        check = check.view(type(self))
        check._update_from(self)
        check._mask = mask
        if check._fill_value is not None:
            try:
                fill = _check_fill_value(check._fill_value, np.bool_)
            except (TypeError, ValueError):
                fill = _check_fill_value(None, np.bool_)

            check._fill_value = fill
        return check

    def __eq__(self, other):
        """Check whether other equals self elementwise.

        When either of the elements is masked, the result is masked as well,
        but the underlying boolean data are still set, with self and other
        considered equal if both are masked, and unequal otherwise.

        For structured arrays, all fields are combined, with masked values
        ignored. The result is masked if all fields were masked, with self
        and other considered equal only if both were fully masked.
        """
        return self._comparison(other, operator.eq)

    def __ne__(self, other):
        """Check whether other does not equal self elementwise.

        When either of the elements is masked, the result is masked as well,
        but the underlying boolean data are still set, with self and other
        considered equal if both are masked, and unequal otherwise.

        For structured arrays, all fields are combined, with masked values
        ignored. The result is masked if all fields were masked, with self
        and other considered equal only if both were fully masked.
        """
        return self._comparison(other, operator.ne)

    def __add__(self, other):
        """
        Add self to other, and return a new masked array.

        """
        if self._delegate_binop(other):
            return NotImplemented
        return add(self, other)

    def __radd__(self, other):
        """
        Add other to self, and return a new masked array.

        """
        return add(other, self)

    def __sub__(self, other):
        """
        Subtract other from self, and return a new masked array.

        """
        if self._delegate_binop(other):
            return NotImplemented
        return subtract(self, other)

    def __rsub__(self, other):
        """
        Subtract self from other, and return a new masked array.

        """
        return subtract(other, self)

    def __mul__(self, other):
        """Multiply self by other, and return a new masked array."""
        if self._delegate_binop(other):
            return NotImplemented
        return multiply(self, other)

    def __rmul__(self, other):
        """
        Multiply other by self, and return a new masked array.

        """
        return multiply(other, self)

    def __div__(self, other):
        """
        Divide other into self, and return a new masked array.

        """
        if self._delegate_binop(other):
            return NotImplemented
        return divide(self, other)

    def __truediv__(self, other):
        """
        Divide other into self, and return a new masked array.

        """
        if self._delegate_binop(other):
            return NotImplemented
        return true_divide(self, other)

    def __rtruediv__(self, other):
        """
        Divide self into other, and return a new masked array.

        """
        return true_divide(other, self)

    def __floordiv__(self, other):
        """
        Divide other into self, and return a new masked array.

        """
        if self._delegate_binop(other):
            return NotImplemented
        return floor_divide(self, other)

    def __rfloordiv__(self, other):
        """
        Divide self into other, and return a new masked array.

        """
        return floor_divide(other, self)

    def __pow__(self, other):
        """
        Raise self to the power other, masking the potential NaNs/Infs

        """
        if self._delegate_binop(other):
            return NotImplemented
        return power(self, other)

    def __rpow__(self, other):
        """
        Raise other to the power self, masking the potential NaNs/Infs

        """
        return power(other, self)

    def __iadd__(self, other):
        """
        Add other to self in-place.

        """
        m = getmask(other)
        if self._mask is nomask:
            if not m is not nomask or m.any():
                self._mask = make_mask_none(self.shape, self.dtype)
                self._mask += m
        elif m is not nomask:
            self._mask += m
        self._data.__iadd__(np.where(self._mask, self.dtype.type(0), getdata(other)))
        return self

    def __isub__(self, other):
        """
        Subtract other from self in-place.

        """
        m = getmask(other)
        if self._mask is nomask:
            if not m is not nomask or m.any():
                self._mask = make_mask_none(self.shape, self.dtype)
                self._mask += m
        elif m is not nomask:
            self._mask += m
        self._data.__isub__(np.where(self._mask, self.dtype.type(0), getdata(other)))
        return self

    def __imul__(self, other):
        """
        Multiply self by other in-place.

        """
        m = getmask(other)
        if self._mask is nomask:
            if not m is not nomask or m.any():
                self._mask = make_mask_none(self.shape, self.dtype)
                self._mask += m
        elif m is not nomask:
            self._mask += m
        self._data.__imul__(np.where(self._mask, self.dtype.type(1), getdata(other)))
        return self

    def __idiv__(self, other):
        """
        Divide self by other in-place.

        """
        other_data = getdata(other)
        dom_mask = _DomainSafeDivide().__call__(self._data, other_data)
        other_mask = getmask(other)
        new_mask = mask_or(other_mask, dom_mask)
        if dom_mask.any():
            _, fval = ufunc_fills[np.divide]
            other_data = np.where(dom_mask, fval, other_data)
        self._mask |= new_mask
        self._data.__idiv__(np.where(self._mask, self.dtype.type(1), other_data))
        return self

    def __ifloordiv__(self, other):
        """
        Floor divide self by other in-place.

        """
        other_data = getdata(other)
        dom_mask = _DomainSafeDivide().__call__(self._data, other_data)
        other_mask = getmask(other)
        new_mask = mask_or(other_mask, dom_mask)
        if dom_mask.any():
            _, fval = ufunc_fills[np.floor_divide]
            other_data = np.where(dom_mask, fval, other_data)
        self._mask |= new_mask
        self._data.__ifloordiv__(np.where(self._mask, self.dtype.type(1), other_data))
        return self

    def __itruediv__(self, other):
        """
        True divide self by other in-place.

        """
        other_data = getdata(other)
        dom_mask = _DomainSafeDivide().__call__(self._data, other_data)
        other_mask = getmask(other)
        new_mask = mask_or(other_mask, dom_mask)
        if dom_mask.any():
            _, fval = ufunc_fills[np.true_divide]
            other_data = np.where(dom_mask, fval, other_data)
        self._mask |= new_mask
        self._data.__itruediv__(np.where(self._mask, self.dtype.type(1), other_data))
        return self

    def __ipow__(self, other):
        """
        Raise self to the power other, in place.

        """
        other_data = getdata(other)
        other_mask = getmask(other)
        with np.errstate(divide='ignore', invalid='ignore'):
            self._data.__ipow__(np.where(self._mask, self.dtype.type(1), other_data))
        invalid = np.logical_not(np.isfinite(self._data))
        if invalid.any():
            if self._mask is not nomask:
                self._mask |= invalid
            else:
                self._mask = invalid
            np.copyto((self._data), (self.fill_value), where=invalid)
        new_mask = mask_or(other_mask, invalid)
        self._mask = mask_or(self._mask, new_mask)
        return self

    def __float__(self):
        """
        Convert to float.

        """
        if self.size > 1:
            raise TypeError('Only length-1 arrays can be converted to Python scalars')
        elif self._mask:
            warnings.warn('Warning: converting a masked element to nan.', stacklevel=2)
            return np.nan
        return float(self.item())

    def __int__(self):
        """
        Convert to int.

        """
        if self.size > 1:
            raise TypeError('Only length-1 arrays can be converted to Python scalars')
        elif self._mask:
            raise MaskError('Cannot convert masked element to a Python int.')
        return int(self.item())

    @property
    def imag(self):
        """
        The imaginary part of the masked array.

        This property is a view on the imaginary part of this `MaskedArray`.

        See Also
        --------
        real

        Examples
        --------
        >>> x = np.ma.array([1+1.j, -2j, 3.45+1.6j], mask=[False, True, False])
        >>> x.imag
        masked_array(data=[1.0, --, 1.6],
                     mask=[False,  True, False],
               fill_value=1e+20)

        """
        result = self._data.imag.view(type(self))
        result.__setmask__(self._mask)
        return result

    get_imag = imag.fget

    @property
    def real(self):
        """
        The real part of the masked array.

        This property is a view on the real part of this `MaskedArray`.

        See Also
        --------
        imag

        Examples
        --------
        >>> x = np.ma.array([1+1.j, -2j, 3.45+1.6j], mask=[False, True, False])
        >>> x.real
        masked_array(data=[1.0, --, 3.45],
                     mask=[False,  True, False],
               fill_value=1e+20)

        """
        result = self._data.real.view(type(self))
        result.__setmask__(self._mask)
        return result

    get_real = real.fget

    def count(self, axis=None, keepdims=np._NoValue):
        """
        Count the non-masked elements of the array along the given axis.

        Parameters
        ----------
        axis : None or int or tuple of ints, optional
            Axis or axes along which the count is performed.
            The default, None, performs the count over all
            the dimensions of the input array. `axis` may be negative, in
            which case it counts from the last to the first axis.

            .. versionadded:: 1.10.0

            If this is a tuple of ints, the count is performed on multiple
            axes, instead of a single axis or all the axes as before.
        keepdims : bool, optional
            If this is set to True, the axes which are reduced are left
            in the result as dimensions with size one. With this option,
            the result will broadcast correctly against the array.

        Returns
        -------
        result : ndarray or scalar
            An array with the same shape as the input array, with the specified
            axis removed. If the array is a 0-d array, or if `axis` is None, a
            scalar is returned.

        See Also
        --------
        ma.count_masked : Count masked elements in array or along a given axis.

        Examples
        --------
        >>> import numpy.ma as ma
        >>> a = ma.arange(6).reshape((2, 3))
        >>> a[1, :] = ma.masked
        >>> a
        masked_array(
          data=[[0, 1, 2],
                [--, --, --]],
          mask=[[False, False, False],
                [ True,  True,  True]],
          fill_value=999999)
        >>> a.count()
        3

        When the `axis` keyword is specified an array of appropriate size is
        returned.

        >>> a.count(axis=0)
        array([1, 1, 1])
        >>> a.count(axis=1)
        array([3, 0])

        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        m = self._mask
        if isinstance(self.data, np.matrix):
            if m is nomask:
                m = np.zeros((self.shape), dtype=(np.bool_))
            m = m.view(type(self.data))
        if m is nomask:
            if self.shape == ():
                if axis not in (None, 0):
                    raise np.AxisError(axis=axis, ndim=(self.ndim))
                return 1
            if axis is None:
                if kwargs.get('keepdims', False):
                    return np.array((self.size), dtype=(np.intp), ndmin=(self.ndim))
                return self.size
            axes = normalize_axis_tuple(axis, self.ndim)
            items = 1
            for ax in axes:
                items *= self.shape[ax]

            if kwargs.get('keepdims', False):
                out_dims = list(self.shape)
                for a in axes:
                    out_dims[a] = 1

            else:
                out_dims = [d for n, d in enumerate(self.shape) if n not in axes]
            return np.full(out_dims, items, dtype=(np.intp))
        if self is masked:
            return 0
        return ((~m).sum)(axis=axis, dtype=np.intp, **kwargs)

    def ravel(self, order='C'):
        """
        Returns a 1D version of self, as a view.

        Parameters
        ----------
        order : {'C', 'F', 'A', 'K'}, optional
            The elements of `a` are read using this index order. 'C' means to
            index the elements in C-like order, with the last axis index
            changing fastest, back to the first axis index changing slowest.
            'F' means to index the elements in Fortran-like index order, with
            the first index changing fastest, and the last index changing
            slowest. Note that the 'C' and 'F' options take no account of the
            memory layout of the underlying array, and only refer to the order
            of axis indexing.  'A' means to read the elements in Fortran-like
            index order if `m` is Fortran *contiguous* in memory, C-like order
            otherwise.  'K' means to read the elements in the order they occur
            in memory, except for reversing the data when strides are negative.
            By default, 'C' index order is used.

        Returns
        -------
        MaskedArray
            Output view is of shape ``(self.size,)`` (or
            ``(np.ma.product(self.shape),)``).

        Examples
        --------
        >>> x = np.ma.array([[1,2,3],[4,5,6],[7,8,9]], mask=[0] + [1,0]*4)
        >>> x
        masked_array(
          data=[[1, --, 3],
                [--, 5, --],
                [7, --, 9]],
          mask=[[False,  True, False],
                [ True, False,  True],
                [False,  True, False]],
          fill_value=999999)
        >>> x.ravel()
        masked_array(data=[1, --, 3, --, 5, --, 7, --, 9],
                     mask=[False,  True, False,  True, False,  True, False,  True,
                           False],
               fill_value=999999)

        """
        r = ndarray.ravel((self._data), order=order).view(type(self))
        r._update_from(self)
        if self._mask is not nomask:
            r._mask = ndarray.ravel((self._mask), order=order).reshape(r.shape)
        else:
            r._mask = nomask
        return r

    def reshape(self, *s, **kwargs):
        """
        Give a new shape to the array without changing its data.

        Returns a masked array containing the same data, but with a new shape.
        The result is a view on the original array; if this is not possible, a
        ValueError is raised.

        Parameters
        ----------
        shape : int or tuple of ints
            The new shape should be compatible with the original shape. If an
            integer is supplied, then the result will be a 1-D array of that
            length.
        order : {'C', 'F'}, optional
            Determines whether the array data should be viewed as in C
            (row-major) or FORTRAN (column-major) order.

        Returns
        -------
        reshaped_array : array
            A new view on the array.

        See Also
        --------
        reshape : Equivalent function in the masked array module.
        numpy.ndarray.reshape : Equivalent method on ndarray object.
        numpy.reshape : Equivalent function in the NumPy module.

        Notes
        -----
        The reshaping operation cannot guarantee that a copy will not be made,
        to modify the shape in place, use ``a.shape = s``

        Examples
        --------
        >>> x = np.ma.array([[1,2],[3,4]], mask=[1,0,0,1])
        >>> x
        masked_array(
          data=[[--, 2],
                [3, --]],
          mask=[[ True, False],
                [False,  True]],
          fill_value=999999)
        >>> x = x.reshape((4,1))
        >>> x
        masked_array(
          data=[[--],
                [2],
                [3],
                [--]],
          mask=[[ True],
                [False],
                [False],
                [ True]],
          fill_value=999999)

        """
        kwargs.update(order=(kwargs.get('order', 'C')))
        result = (self._data.reshape)(*s, **kwargs).view(type(self))
        result._update_from(self)
        mask = self._mask
        if mask is not nomask:
            result._mask = (mask.reshape)(*s, **kwargs)
        return result

    def resize(self, newshape, refcheck=True, order=False):
        """
        .. warning::

            This method does nothing, except raise a ValueError exception. A
            masked array does not own its data and therefore cannot safely be
            resized in place. Use the `numpy.ma.resize` function instead.

        This method is difficult to implement safely and may be deprecated in
        future releases of NumPy.

        """
        errmsg = 'A masked array does not own its data and therefore cannot be resized.\nUse the numpy.ma.resize function instead.'
        raise ValueError(errmsg)

    def put(self, indices, values, mode='raise'):
        """
        Set storage-indexed locations to corresponding values.

        Sets self._data.flat[n] = values[n] for each n in indices.
        If `values` is shorter than `indices` then it will repeat.
        If `values` has some masked values, the initial mask is updated
        in consequence, else the corresponding values are unmasked.

        Parameters
        ----------
        indices : 1-D array_like
            Target indices, interpreted as integers.
        values : array_like
            Values to place in self._data copy at target indices.
        mode : {'raise', 'wrap', 'clip'}, optional
            Specifies how out-of-bounds indices will behave.
            'raise' : raise an error.
            'wrap' : wrap around.
            'clip' : clip to the range.

        Notes
        -----
        `values` can be a scalar or length 1 array.

        Examples
        --------
        >>> x = np.ma.array([[1,2,3],[4,5,6],[7,8,9]], mask=[0] + [1,0]*4)
        >>> x
        masked_array(
          data=[[1, --, 3],
                [--, 5, --],
                [7, --, 9]],
          mask=[[False,  True, False],
                [ True, False,  True],
                [False,  True, False]],
          fill_value=999999)
        >>> x.put([0,4,8],[10,20,30])
        >>> x
        masked_array(
          data=[[10, --, 3],
                [--, 20, --],
                [7, --, 30]],
          mask=[[False,  True, False],
                [ True, False,  True],
                [False,  True, False]],
          fill_value=999999)

        >>> x.put(4,999)
        >>> x
        masked_array(
          data=[[10, --, 3],
                [--, 999, --],
                [7, --, 30]],
          mask=[[False,  True, False],
                [ True, False,  True],
                [False,  True, False]],
          fill_value=999999)

        """
        if self._hardmask:
            if self._mask is not nomask:
                mask = self._mask[indices]
                indices = narray(indices, copy=False)
                values = narray(values, copy=False, subok=True)
                values.resize(indices.shape)
                indices = indices[(~mask)]
                values = values[(~mask)]
        self._data.put(indices, values, mode=mode)
        if self._mask is nomask:
            if getmask(values) is nomask:
                return
        m = getmaskarray(self)
        if getmask(values) is nomask:
            m.put(indices, False, mode=mode)
        else:
            m.put(indices, (values._mask), mode=mode)
        m = make_mask(m, copy=False, shrink=True)
        self._mask = m

    def ids(self):
        """
        Return the addresses of the data and mask areas.

        Parameters
        ----------
        None

        Examples
        --------
        >>> x = np.ma.array([1, 2, 3], mask=[0, 1, 1])
        >>> x.ids()
        (166670640, 166659832) # may vary

        If the array has no mask, the address of `nomask` is returned. This address
        is typically not close to the data in memory:

        >>> x = np.ma.array([1, 2, 3])
        >>> x.ids()
        (166691080, 3083169284) # may vary

        """
        if self._mask is nomask:
            return (self.ctypes.data, id(nomask))
        return (self.ctypes.data, self._mask.ctypes.data)

    def iscontiguous(self):
        """
        Return a boolean indicating whether the data is contiguous.

        Parameters
        ----------
        None

        Examples
        --------
        >>> x = np.ma.array([1, 2, 3])
        >>> x.iscontiguous()
        True

        `iscontiguous` returns one of the flags of the masked array:

        >>> x.flags
          C_CONTIGUOUS : True
          F_CONTIGUOUS : True
          OWNDATA : False
          WRITEABLE : True
          ALIGNED : True
          WRITEBACKIFCOPY : False
          UPDATEIFCOPY : False

        """
        return self.flags['CONTIGUOUS']

    def all(self, axis=None, out=None, keepdims=np._NoValue):
        """
        Returns True if all elements evaluate to True.

        The output array is masked where all the values along the given axis
        are masked: if the output would have been a scalar and that all the
        values are masked, then the output is `masked`.

        Refer to `numpy.all` for full documentation.

        See Also
        --------
        numpy.ndarray.all : corresponding function for ndarrays
        numpy.all : equivalent function

        Examples
        --------
        >>> np.ma.array([1,2,3]).all()
        True
        >>> a = np.ma.array([1,2,3], mask=True)
        >>> (a.all() is np.ma.masked)
        True

        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        mask = _check_mask_axis((self._mask), axis, **kwargs)
        if out is None:
            d = (self.filled(True).all)(axis=axis, **kwargs).view(type(self))
            if d.ndim:
                d.__setmask__(mask)
            elif mask:
                return masked
            return d
        (self.filled(True).all)(axis=axis, out=out, **kwargs)
        if isinstance(out, MaskedArray):
            if out.ndim or (mask):
                out.__setmask__(mask)
            return out

    def any(self, axis=None, out=None, keepdims=np._NoValue):
        """
        Returns True if any of the elements of `a` evaluate to True.

        Masked values are considered as False during computation.

        Refer to `numpy.any` for full documentation.

        See Also
        --------
        numpy.ndarray.any : corresponding function for ndarrays
        numpy.any : equivalent function

        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        mask = _check_mask_axis((self._mask), axis, **kwargs)
        if out is None:
            d = (self.filled(False).any)(axis=axis, **kwargs).view(type(self))
            if d.ndim:
                d.__setmask__(mask)
            elif mask:
                d = masked
            return d
        (self.filled(False).any)(axis=axis, out=out, **kwargs)
        if isinstance(out, MaskedArray):
            if out.ndim or (mask):
                out.__setmask__(mask)
            return out

    def nonzero(self):
        """
        Return the indices of unmasked elements that are not zero.

        Returns a tuple of arrays, one for each dimension, containing the
        indices of the non-zero elements in that dimension. The corresponding
        non-zero values can be obtained with::

            a[a.nonzero()]

        To group the indices by element, rather than dimension, use
        instead::

            np.transpose(a.nonzero())

        The result of this is always a 2d array, with a row for each non-zero
        element.

        Parameters
        ----------
        None

        Returns
        -------
        tuple_of_arrays : tuple
            Indices of elements that are non-zero.

        See Also
        --------
        numpy.nonzero :
            Function operating on ndarrays.
        flatnonzero :
            Return indices that are non-zero in the flattened version of the input
            array.
        numpy.ndarray.nonzero :
            Equivalent ndarray method.
        count_nonzero :
            Counts the number of non-zero elements in the input array.

        Examples
        --------
        >>> import numpy.ma as ma
        >>> x = ma.array(np.eye(3))
        >>> x
        masked_array(
          data=[[1., 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]],
          mask=False,
          fill_value=1e+20)
        >>> x.nonzero()
        (array([0, 1, 2]), array([0, 1, 2]))

        Masked elements are ignored.

        >>> x[1, 1] = ma.masked
        >>> x
        masked_array(
          data=[[1.0, 0.0, 0.0],
                [0.0, --, 0.0],
                [0.0, 0.0, 1.0]],
          mask=[[False, False, False],
                [False,  True, False],
                [False, False, False]],
          fill_value=1e+20)
        >>> x.nonzero()
        (array([0, 2]), array([0, 2]))

        Indices can also be grouped by element.

        >>> np.transpose(x.nonzero())
        array([[0, 0],
               [2, 2]])

        A common use for ``nonzero`` is to find the indices of an array, where
        a condition is True.  Given an array `a`, the condition `a` > 3 is a
        boolean array and since False is interpreted as 0, ma.nonzero(a > 3)
        yields the indices of the `a` where the condition is true.

        >>> a = ma.array([[1,2,3],[4,5,6],[7,8,9]])
        >>> a > 3
        masked_array(
          data=[[False, False, False],
                [ True,  True,  True],
                [ True,  True,  True]],
          mask=False,
          fill_value=True)
        >>> ma.nonzero(a > 3)
        (array([1, 1, 1, 2, 2, 2]), array([0, 1, 2, 0, 1, 2]))

        The ``nonzero`` method of the condition array can also be called.

        >>> (a > 3).nonzero()
        (array([1, 1, 1, 2, 2, 2]), array([0, 1, 2, 0, 1, 2]))

        """
        return narray((self.filled(0)), copy=False).nonzero()

    def trace(self, offset=0, axis1=0, axis2=1, dtype=None, out=None):
        """
        (this docstring should be overwritten)
        """
        m = self._mask
        if m is nomask:
            result = super(MaskedArray, self).trace(offset=offset, axis1=axis1, axis2=axis2,
              out=out)
            return result.astype(dtype)
        D = self.diagonal(offset=offset, axis1=axis1, axis2=axis2)
        return D.astype(dtype).filled(0).sum(axis=(-1), out=out)

    trace.__doc__ = ndarray.trace.__doc__

    def dot(self, b, out=None, strict=False):
        """
        a.dot(b, out=None)

        Masked dot product of two arrays. Note that `out` and `strict` are
        located in different positions than in `ma.dot`. In order to
        maintain compatibility with the functional version, it is
        recommended that the optional arguments be treated as keyword only.
        At some point that may be mandatory.

        .. versionadded:: 1.10.0

        Parameters
        ----------
        b : masked_array_like
            Inputs array.
        out : masked_array, optional
            Output argument. This must have the exact kind that would be
            returned if it was not used. In particular, it must have the
            right type, must be C-contiguous, and its dtype must be the
            dtype that would be returned for `ma.dot(a,b)`. This is a
            performance feature. Therefore, if these conditions are not
            met, an exception is raised, instead of attempting to be
            flexible.
        strict : bool, optional
            Whether masked data are propagated (True) or set to 0 (False)
            for the computation. Default is False.  Propagating the mask
            means that if a masked value appears in a row or column, the
            whole row or column is considered masked.

            .. versionadded:: 1.10.2

        See Also
        --------
        numpy.ma.dot : equivalent function

        """
        return dot(self, b, out=out, strict=strict)

    def sum(self, axis=None, dtype=None, out=None, keepdims=np._NoValue):
        """
        Return the sum of the array elements over the given axis.

        Masked elements are set to 0 internally.

        Refer to `numpy.sum` for full documentation.

        See Also
        --------
        numpy.ndarray.sum : corresponding function for ndarrays
        numpy.sum : equivalent function

        Examples
        --------
        >>> x = np.ma.array([[1,2,3],[4,5,6],[7,8,9]], mask=[0] + [1,0]*4)
        >>> x
        masked_array(
          data=[[1, --, 3],
                [--, 5, --],
                [7, --, 9]],
          mask=[[False,  True, False],
                [ True, False,  True],
                [False,  True, False]],
          fill_value=999999)
        >>> x.sum()
        25
        >>> x.sum(axis=1)
        masked_array(data=[4, 5, 16],
                     mask=[False, False, False],
               fill_value=999999)
        >>> x.sum(axis=0)
        masked_array(data=[8, 5, 12],
                     mask=[False, False, False],
               fill_value=999999)
        >>> print(type(x.sum(axis=0, dtype=np.int64)[0]))
        <class 'numpy.int64'>

        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        _mask = self._mask
        newmask = _check_mask_axis(_mask, axis, **kwargs)
        if out is None:
            result = (self.filled(0).sum)(axis, dtype=dtype, **kwargs)
            rndim = getattr(result, 'ndim', 0)
            if rndim:
                result = result.view(type(self))
                result.__setmask__(newmask)
            elif newmask:
                result = masked
            return result
        result = (self.filled(0).sum)(axis, dtype=dtype, out=out, **kwargs)
        if isinstance(out, MaskedArray):
            outmask = getmask(out)
            if outmask is nomask:
                outmask = out._mask = make_mask_none(out.shape)
            outmask.flat = newmask
        return out

    def cumsum(self, axis=None, dtype=None, out=None):
        """
        Return the cumulative sum of the array elements over the given axis.

        Masked values are set to 0 internally during the computation.
        However, their position is saved, and the result will be masked at
        the same locations.

        Refer to `numpy.cumsum` for full documentation.

        Notes
        -----
        The mask is lost if `out` is not a valid :class:`ma.MaskedArray` !

        Arithmetic is modular when using integer types, and no error is
        raised on overflow.

        See Also
        --------
        numpy.ndarray.cumsum : corresponding function for ndarrays
        numpy.cumsum : equivalent function

        Examples
        --------
        >>> marr = np.ma.array(np.arange(10), mask=[0,0,0,1,1,1,0,0,0,0])
        >>> marr.cumsum()
        masked_array(data=[0, 1, 3, --, --, --, 9, 16, 24, 33],
                     mask=[False, False, False,  True,  True,  True, False, False,
                           False, False],
               fill_value=999999)

        """
        result = self.filled(0).cumsum(axis=axis, dtype=dtype, out=out)
        if out is not None:
            if isinstance(out, MaskedArray):
                out.__setmask__(self.mask)
            return out
        result = result.view(type(self))
        result.__setmask__(self._mask)
        return result

    def prod(self, axis=None, dtype=None, out=None, keepdims=np._NoValue):
        """
        Return the product of the array elements over the given axis.

        Masked elements are set to 1 internally for computation.

        Refer to `numpy.prod` for full documentation.

        Notes
        -----
        Arithmetic is modular when using integer types, and no error is raised
        on overflow.

        See Also
        --------
        numpy.ndarray.prod : corresponding function for ndarrays
        numpy.prod : equivalent function
        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        _mask = self._mask
        newmask = _check_mask_axis(_mask, axis, **kwargs)
        if out is None:
            result = (self.filled(1).prod)(axis, dtype=dtype, **kwargs)
            rndim = getattr(result, 'ndim', 0)
            if rndim:
                result = result.view(type(self))
                result.__setmask__(newmask)
            elif newmask:
                result = masked
            return result
        result = (self.filled(1).prod)(axis, dtype=dtype, out=out, **kwargs)
        if isinstance(out, MaskedArray):
            outmask = getmask(out)
            if outmask is nomask:
                outmask = out._mask = make_mask_none(out.shape)
            outmask.flat = newmask
        return out

    product = prod

    def cumprod(self, axis=None, dtype=None, out=None):
        """
        Return the cumulative product of the array elements over the given axis.

        Masked values are set to 1 internally during the computation.
        However, their position is saved, and the result will be masked at
        the same locations.

        Refer to `numpy.cumprod` for full documentation.

        Notes
        -----
        The mask is lost if `out` is not a valid MaskedArray !

        Arithmetic is modular when using integer types, and no error is
        raised on overflow.

        See Also
        --------
        numpy.ndarray.cumprod : corresponding function for ndarrays
        numpy.cumprod : equivalent function
        """
        result = self.filled(1).cumprod(axis=axis, dtype=dtype, out=out)
        if out is not None:
            if isinstance(out, MaskedArray):
                out.__setmask__(self._mask)
            return out
        result = result.view(type(self))
        result.__setmask__(self._mask)
        return result

    def mean(self, axis=None, dtype=None, out=None, keepdims=np._NoValue):
        """
        Returns the average of the array elements along given axis.

        Masked entries are ignored, and result elements which are not
        finite will be masked.

        Refer to `numpy.mean` for full documentation.

        See Also
        --------
        numpy.ndarray.mean : corresponding function for ndarrays
        numpy.mean : Equivalent function
        numpy.ma.average: Weighted average.

        Examples
        --------
        >>> a = np.ma.array([1,2,3], mask=[False, False, True])
        >>> a
        masked_array(data=[1, 2, --],
                     mask=[False, False,  True],
               fill_value=999999)
        >>> a.mean()
        1.5

        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        if self._mask is nomask:
            result = (super(MaskedArray, self).mean)(axis=axis, dtype=dtype, **kwargs)[()]
        else:
            dsum = (self.sum)(axis=axis, dtype=dtype, **kwargs)
            cnt = (self.count)(axis=axis, **kwargs)
            if cnt.shape == () and cnt == 0:
                result = masked
            else:
                result = dsum * 1.0 / cnt
        if out is not None:
            out.flat = result
            if isinstance(out, MaskedArray):
                outmask = getmask(out)
                if outmask is nomask:
                    outmask = out._mask = make_mask_none(out.shape)
                outmask.flat = getmask(result)
            return out
        return result

    def anom(self, axis=None, dtype=None):
        """
        Compute the anomalies (deviations from the arithmetic mean)
        along the given axis.

        Returns an array of anomalies, with the same shape as the input and
        where the arithmetic mean is computed along the given axis.

        Parameters
        ----------
        axis : int, optional
            Axis over which the anomalies are taken.
            The default is to use the mean of the flattened array as reference.
        dtype : dtype, optional
            Type to use in computing the variance. For arrays of integer type
             the default is float32; for arrays of float types it is the same as
             the array type.

        See Also
        --------
        mean : Compute the mean of the array.

        Examples
        --------
        >>> a = np.ma.array([1,2,3])
        >>> a.anom()
        masked_array(data=[-1.,  0.,  1.],
                     mask=False,
               fill_value=1e+20)

        """
        m = self.mean(axis, dtype)
        if m is masked:
            return m
        if not axis:
            return self - m
        return self - expand_dims(m, axis)

    def var(self, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue):
        """
        Returns the variance of the array elements along given axis.

        Masked entries are ignored, and result elements which are not
        finite will be masked.

        Refer to `numpy.var` for full documentation.

        See Also
        --------
        numpy.ndarray.var : corresponding function for ndarrays
        numpy.var : Equivalent function
        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        if self._mask is nomask:
            ret = (super(MaskedArray, self).var)(axis=axis, dtype=dtype, out=out, ddof=ddof, **kwargs)[()]
            if out is not None:
                if isinstance(out, MaskedArray):
                    out.__setmask__(nomask)
                return out
            return ret
        cnt = (self.count)(axis=axis, **kwargs) - ddof
        danom = self - self.mean(axis, dtype, keepdims=True)
        if iscomplexobj(self):
            danom = umath.absolute(danom) ** 2
        else:
            danom *= danom
        dvar = divide((danom.sum)(axis, **kwargs), cnt).view(type(self))
        if dvar.ndim:
            dvar._mask = mask_or((self._mask.all)(axis, **kwargs), cnt <= 0)
            dvar._update_from(self)
        elif getmask(dvar):
            dvar = masked
            if out is not None:
                if isinstance(out, MaskedArray):
                    out.flat = 0
                    out.__setmask__(True)
                elif out.dtype.kind in 'biu':
                    errmsg = 'Masked data information would be lost in one or more location.'
                    raise MaskError(errmsg)
                else:
                    out.flat = np.nan
                return out
        if out is not None:
            out.flat = dvar
            if isinstance(out, MaskedArray):
                out.__setmask__(dvar.mask)
            return out
        return dvar

    var.__doc__ = np.var.__doc__

    def std(self, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue):
        """
        Returns the standard deviation of the array elements along given axis.

        Masked entries are ignored.

        Refer to `numpy.std` for full documentation.

        See Also
        --------
        numpy.ndarray.std : corresponding function for ndarrays
        numpy.std : Equivalent function
        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        dvar = (self.var)(axis, dtype, out, ddof, **kwargs)
        if dvar is not masked:
            if out is not None:
                np.power(out, 0.5, out=out, casting='unsafe')
                return out
            dvar = sqrt(dvar)
        return dvar

    def round(self, decimals=0, out=None):
        """
        Return each element rounded to the given number of decimals.

        Refer to `numpy.around` for full documentation.

        See Also
        --------
        numpy.ndarray.round : corresponding function for ndarrays
        numpy.around : equivalent function
        """
        result = self._data.round(decimals=decimals, out=out).view(type(self))
        if result.ndim > 0:
            result._mask = self._mask
            result._update_from(self)
        elif self._mask:
            result = masked
        if out is None:
            return result
        if isinstance(out, MaskedArray):
            out.__setmask__(self._mask)
        return out

    def argsort(self, axis=np._NoValue, kind=None, order=None, endwith=True, fill_value=None):
        """
        Return an ndarray of indices that sort the array along the
        specified axis.  Masked values are filled beforehand to
        `fill_value`.

        Parameters
        ----------
        axis : int, optional
            Axis along which to sort. If None, the default, the flattened array
            is used.

            ..  versionchanged:: 1.13.0
                Previously, the default was documented to be -1, but that was
                in error. At some future date, the default will change to -1, as
                originally intended.
                Until then, the axis should be given explicitly when
                ``arr.ndim > 1``, to avoid a FutureWarning.
        kind : {'quicksort', 'mergesort', 'heapsort', 'stable'}, optional
            The sorting algorithm used.
        order : list, optional
            When `a` is an array with fields defined, this argument specifies
            which fields to compare first, second, etc.  Not all fields need be
            specified.
        endwith : {True, False}, optional
            Whether missing values (if any) should be treated as the largest values
            (True) or the smallest values (False)
            When the array contains unmasked values at the same extremes of the
            datatype, the ordering of these values and the masked values is
            undefined.
        fill_value : {var}, optional
            Value used internally for the masked values.
            If ``fill_value`` is not None, it supersedes ``endwith``.

        Returns
        -------
        index_array : ndarray, int
            Array of indices that sort `a` along the specified axis.
            In other words, ``a[index_array]`` yields a sorted `a`.

        See Also
        --------
        ma.MaskedArray.sort : Describes sorting algorithms used.
        lexsort : Indirect stable sort with multiple keys.
        numpy.ndarray.sort : Inplace sort.

        Notes
        -----
        See `sort` for notes on the different sorting algorithms.

        Examples
        --------
        >>> a = np.ma.array([3,2,1], mask=[False, False, True])
        >>> a
        masked_array(data=[3, 2, --],
                     mask=[False, False,  True],
               fill_value=999999)
        >>> a.argsort()
        array([1, 0, 2])

        """
        if axis is np._NoValue:
            axis = _deprecate_argsort_axis(self)
        if fill_value is None:
            if endwith:
                if np.issubdtype(self.dtype, np.floating):
                    fill_value = np.nan
                else:
                    fill_value = minimum_fill_value(self)
            else:
                fill_value = maximum_fill_value(self)
        filled = self.filled(fill_value)
        return filled.argsort(axis=axis, kind=kind, order=order)

    def argmin(self, axis=None, fill_value=None, out=None):
        """
        Return array of indices to the minimum values along the given axis.

        Parameters
        ----------
        axis : {None, integer}
            If None, the index is into the flattened array, otherwise along
            the specified axis
        fill_value : {var}, optional
            Value used to fill in the masked values.  If None, the output of
            minimum_fill_value(self._data) is used instead.
        out : {None, array}, optional
            Array into which the result can be placed. Its type is preserved
            and it must be of the right shape to hold the output.

        Returns
        -------
        ndarray or scalar
            If multi-dimension input, returns a new ndarray of indices to the
            minimum values along the given axis.  Otherwise, returns a scalar
            of index to the minimum values along the given axis.

        Examples
        --------
        >>> x = np.ma.array(np.arange(4), mask=[1,1,0,0])
        >>> x.shape = (2,2)
        >>> x
        masked_array(
          data=[[--, --],
                [2, 3]],
          mask=[[ True,  True],
                [False, False]],
          fill_value=999999)
        >>> x.argmin(axis=0, fill_value=-1)
        array([0, 0])
        >>> x.argmin(axis=0, fill_value=9)
        array([1, 1])

        """
        if fill_value is None:
            fill_value = minimum_fill_value(self)
        d = self.filled(fill_value).view(ndarray)
        return d.argmin(axis, out=out)

    def argmax(self, axis=None, fill_value=None, out=None):
        """
        Returns array of indices of the maximum values along the given axis.
        Masked values are treated as if they had the value fill_value.

        Parameters
        ----------
        axis : {None, integer}
            If None, the index is into the flattened array, otherwise along
            the specified axis
        fill_value : {var}, optional
            Value used to fill in the masked values.  If None, the output of
            maximum_fill_value(self._data) is used instead.
        out : {None, array}, optional
            Array into which the result can be placed. Its type is preserved
            and it must be of the right shape to hold the output.

        Returns
        -------
        index_array : {integer_array}

        Examples
        --------
        >>> a = np.arange(6).reshape(2,3)
        >>> a.argmax()
        5
        >>> a.argmax(0)
        array([1, 1, 1])
        >>> a.argmax(1)
        array([2, 2])

        """
        if fill_value is None:
            fill_value = maximum_fill_value(self._data)
        d = self.filled(fill_value).view(ndarray)
        return d.argmax(axis, out=out)

    def sort(self, axis=-1, kind=None, order=None, endwith=True, fill_value=None):
        """
        Sort the array, in-place

        Parameters
        ----------
        a : array_like
            Array to be sorted.
        axis : int, optional
            Axis along which to sort. If None, the array is flattened before
            sorting. The default is -1, which sorts along the last axis.
        kind : {'quicksort', 'mergesort', 'heapsort', 'stable'}, optional
            The sorting algorithm used.
        order : list, optional
            When `a` is a structured array, this argument specifies which fields
            to compare first, second, and so on.  This list does not need to
            include all of the fields.
        endwith : {True, False}, optional
            Whether missing values (if any) should be treated as the largest values
            (True) or the smallest values (False)
            When the array contains unmasked values sorting at the same extremes of the
            datatype, the ordering of these values and the masked values is
            undefined.
        fill_value : {var}, optional
            Value used internally for the masked values.
            If ``fill_value`` is not None, it supersedes ``endwith``.

        Returns
        -------
        sorted_array : ndarray
            Array of the same type and shape as `a`.

        See Also
        --------
        numpy.ndarray.sort : Method to sort an array in-place.
        argsort : Indirect sort.
        lexsort : Indirect stable sort on multiple keys.
        searchsorted : Find elements in a sorted array.

        Notes
        -----
        See ``sort`` for notes on the different sorting algorithms.

        Examples
        --------
        >>> a = np.ma.array([1, 2, 5, 4, 3],mask=[0, 1, 0, 1, 0])
        >>> # Default
        >>> a.sort()
        >>> a
        masked_array(data=[1, 3, 5, --, --],
                     mask=[False, False, False,  True,  True],
               fill_value=999999)

        >>> a = np.ma.array([1, 2, 5, 4, 3],mask=[0, 1, 0, 1, 0])
        >>> # Put missing values in the front
        >>> a.sort(endwith=False)
        >>> a
        masked_array(data=[--, --, 1, 3, 5],
                     mask=[ True,  True, False, False, False],
               fill_value=999999)

        >>> a = np.ma.array([1, 2, 5, 4, 3],mask=[0, 1, 0, 1, 0])
        >>> # fill_value takes over endwith
        >>> a.sort(endwith=False, fill_value=3)
        >>> a
        masked_array(data=[1, --, --, 3, 5],
                     mask=[False,  True,  True, False, False],
               fill_value=999999)

        """
        if self._mask is nomask:
            ndarray.sort(self, axis=axis, kind=kind, order=order)
            return
        if self is masked:
            return
        sidx = self.argsort(axis=axis, kind=kind, order=order, fill_value=fill_value,
          endwith=endwith)
        self[...] = np.take_along_axis(self, sidx, axis=axis)

    def min(self, axis=None, out=None, fill_value=None, keepdims=np._NoValue):
        """
        Return the minimum along a given axis.

        Parameters
        ----------
        axis : {None, int}, optional
            Axis along which to operate.  By default, ``axis`` is None and the
            flattened input is used.
        out : array_like, optional
            Alternative output array in which to place the result.  Must be of
            the same shape and buffer length as the expected output.
        fill_value : {var}, optional
            Value used to fill in the masked values.
            If None, use the output of `minimum_fill_value`.
        keepdims : bool, optional
            If this is set to True, the axes which are reduced are left
            in the result as dimensions with size one. With this option,
            the result will broadcast correctly against the array.

        Returns
        -------
        amin : array_like
            New array holding the result.
            If ``out`` was specified, ``out`` is returned.

        See Also
        --------
        ma.minimum_fill_value
            Returns the minimum filling value for a given datatype.

        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        _mask = self._mask
        newmask = _check_mask_axis(_mask, axis, **kwargs)
        if fill_value is None:
            fill_value = minimum_fill_value(self)
        if out is None:
            result = (self.filled(fill_value).min)(axis=axis, 
             out=out, **kwargs).view(type(self))
            if result.ndim:
                result.__setmask__(newmask)
                if newmask.ndim:
                    np.copyto(result, (result.fill_value), where=newmask)
            elif newmask:
                result = masked
            return result
        result = (self.filled(fill_value).min)(axis=axis, out=out, **kwargs)
        if isinstance(out, MaskedArray):
            outmask = getmask(out)
            if outmask is nomask:
                outmask = out._mask = make_mask_none(out.shape)
            outmask.flat = newmask
        else:
            if out.dtype.kind in 'biu':
                errmsg = 'Masked data information would be lost in one or more location.'
                raise MaskError(errmsg)
            np.copyto(out, (np.nan), where=newmask)
        return out

    def mini(self, axis=None):
        """
        Return the array minimum along the specified axis.

        .. deprecated:: 1.13.0
           This function is identical to both:

            * ``self.min(keepdims=True, axis=axis).squeeze(axis=axis)``
            * ``np.ma.minimum.reduce(self, axis=axis)``

           Typically though, ``self.min(axis=axis)`` is sufficient.

        Parameters
        ----------
        axis : int, optional
            The axis along which to find the minima. Default is None, in which case
            the minimum value in the whole array is returned.

        Returns
        -------
        min : scalar or MaskedArray
            If `axis` is None, the result is a scalar. Otherwise, if `axis` is
            given and the array is at least 2-D, the result is a masked array with
            dimension one smaller than the array on which `mini` is called.

        Examples
        --------
        >>> x = np.ma.array(np.arange(6), mask=[0 ,1, 0, 0, 0 ,1]).reshape(3, 2)
        >>> x
        masked_array(
          data=[[0, --],
                [2, 3],
                [4, --]],
          mask=[[False,  True],
                [False, False],
                [False,  True]],
          fill_value=999999)
        >>> x.mini()
        masked_array(data=0,
                     mask=False,
               fill_value=999999)
        >>> x.mini(axis=0)
        masked_array(data=[0, 3],
                     mask=[False, False],
               fill_value=999999)
        >>> x.mini(axis=1)
        masked_array(data=[0, 2, 4],
                     mask=[False, False, False],
               fill_value=999999)

        There is a small difference between `mini` and `min`:

        >>> x[:,1].mini(axis=0)
        masked_array(data=3,
                     mask=False,
               fill_value=999999)
        >>> x[:,1].min(axis=0)
        3
        """
        warnings.warn('`mini` is deprecated; use the `min` method or `np.ma.minimum.reduce instead.',
          DeprecationWarning,
          stacklevel=2)
        return minimum.reduce(self, axis)

    def max(self, axis=None, out=None, fill_value=None, keepdims=np._NoValue):
        """
        Return the maximum along a given axis.

        Parameters
        ----------
        axis : {None, int}, optional
            Axis along which to operate.  By default, ``axis`` is None and the
            flattened input is used.
        out : array_like, optional
            Alternative output array in which to place the result.  Must
            be of the same shape and buffer length as the expected output.
        fill_value : {var}, optional
            Value used to fill in the masked values.
            If None, use the output of maximum_fill_value().
        keepdims : bool, optional
            If this is set to True, the axes which are reduced are left
            in the result as dimensions with size one. With this option,
            the result will broadcast correctly against the array.

        Returns
        -------
        amax : array_like
            New array holding the result.
            If ``out`` was specified, ``out`` is returned.

        See Also
        --------
        ma.maximum_fill_value
            Returns the maximum filling value for a given datatype.

        """
        kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
        _mask = self._mask
        newmask = _check_mask_axis(_mask, axis, **kwargs)
        if fill_value is None:
            fill_value = maximum_fill_value(self)
        if out is None:
            result = (self.filled(fill_value).max)(axis=axis, 
             out=out, **kwargs).view(type(self))
            if result.ndim:
                result.__setmask__(newmask)
                if newmask.ndim:
                    np.copyto(result, (result.fill_value), where=newmask)
            elif newmask:
                result = masked
            return result
        result = (self.filled(fill_value).max)(axis=axis, out=out, **kwargs)
        if isinstance(out, MaskedArray):
            outmask = getmask(out)
            if outmask is nomask:
                outmask = out._mask = make_mask_none(out.shape)
            outmask.flat = newmask
        else:
            if out.dtype.kind in 'biu':
                errmsg = 'Masked data information would be lost in one or more location.'
                raise MaskError(errmsg)
            np.copyto(out, (np.nan), where=newmask)
        return out

    def ptp(self, axis=None, out=None, fill_value=None, keepdims=False):
        """
        Return (maximum - minimum) along the given dimension
        (i.e. peak-to-peak value).

        .. warning::
            `ptp` preserves the data type of the array. This means the
            return value for an input of signed integers with n bits
            (e.g. `np.int8`, `np.int16`, etc) is also a signed integer
            with n bits.  In that case, peak-to-peak values greater than
            ``2**(n-1)-1`` will be returned as negative values. An example
            with a work-around is shown below.

        Parameters
        ----------
        axis : {None, int}, optional
            Axis along which to find the peaks.  If None (default) the
            flattened array is used.
        out : {None, array_like}, optional
            Alternative output array in which to place the result. It must
            have the same shape and buffer length as the expected output
            but the type will be cast if necessary.
        fill_value : {var}, optional
            Value used to fill in the masked values.
        keepdims : bool, optional
            If this is set to True, the axes which are reduced are left
            in the result as dimensions with size one. With this option,
            the result will broadcast correctly against the array.

        Returns
        -------
        ptp : ndarray.
            A new array holding the result, unless ``out`` was
            specified, in which case a reference to ``out`` is returned.

        Examples
        --------
        >>> x = np.ma.MaskedArray([[4, 9, 2, 10],
        ...                        [6, 9, 7, 12]])

        >>> x.ptp(axis=1)
        masked_array(data=[8, 6],
                     mask=False,
               fill_value=999999)

        >>> x.ptp(axis=0)
        masked_array(data=[2, 0, 5, 2],
                     mask=False,
               fill_value=999999)

        >>> x.ptp()
        10

        This example shows that a negative value can be returned when
        the input is an array of signed integers.

        >>> y = np.ma.MaskedArray([[1, 127],
        ...                        [0, 127],
        ...                        [-1, 127],
        ...                        [-2, 127]], dtype=np.int8)
        >>> y.ptp(axis=1)
        masked_array(data=[ 126,  127, -128, -127],
                     mask=False,
               fill_value=999999,
                    dtype=int8)

        A work-around is to use the `view()` method to view the result as
        unsigned integers with the same bit width:

        >>> y.ptp(axis=1).view(np.uint8)
        masked_array(data=[126, 127, 128, 129],
                     mask=False,
               fill_value=999999,
                    dtype=uint8)
        """
        if out is None:
            result = self.max(axis=axis, fill_value=fill_value, keepdims=keepdims)
            result -= self.min(axis=axis, fill_value=fill_value, keepdims=keepdims)
            return result
        out.flat = self.max(axis=axis, out=out, fill_value=fill_value, keepdims=keepdims)
        min_value = self.min(axis=axis, fill_value=fill_value, keepdims=keepdims)
        np.subtract(out, min_value, out=out, casting='unsafe')
        return out

    def partition(self, *args, **kwargs):
        warnings.warn(f"Warning: 'partition' will ignore the 'mask' of the {self.__class__.__name__}.", stacklevel=2)
        return (super(MaskedArray, self).partition)(*args, **kwargs)

    def argpartition(self, *args, **kwargs):
        warnings.warn(f"Warning: 'argpartition' will ignore the 'mask' of the {self.__class__.__name__}.", stacklevel=2)
        return (super(MaskedArray, self).argpartition)(*args, **kwargs)

    def take(self, indices, axis=None, out=None, mode='raise'):
        """
        """
        _data, _mask = self._data, self._mask
        cls = type(self)
        maskindices = getmask(indices)
        if maskindices is not nomask:
            indices = indices.filled(0)
        if out is None:
            out = _data.take(indices, axis=axis, mode=mode)[...].view(cls)
        else:
            np.take(_data, indices, axis=axis, mode=mode, out=out)
        if isinstance(out, MaskedArray):
            if _mask is nomask:
                outmask = maskindices
            else:
                outmask = _mask.take(indices, axis=axis, mode=mode)
                outmask |= maskindices
            out.__setmask__(outmask)
        return out[()]

    copy = _arraymethod('copy')
    diagonal = _arraymethod('diagonal')
    flatten = _arraymethod('flatten')
    repeat = _arraymethod('repeat')
    squeeze = _arraymethod('squeeze')
    swapaxes = _arraymethod('swapaxes')
    T = property(fget=(lambda self: self.transpose()))
    transpose = _arraymethod('transpose')

    def tolist(self, fill_value=None):
        """
        Return the data portion of the masked array as a hierarchical Python list.

        Data items are converted to the nearest compatible Python type.
        Masked values are converted to `fill_value`. If `fill_value` is None,
        the corresponding entries in the output list will be ``None``.

        Parameters
        ----------
        fill_value : scalar, optional
            The value to use for invalid entries. Default is None.

        Returns
        -------
        result : list
            The Python list representation of the masked array.

        Examples
        --------
        >>> x = np.ma.array([[1,2,3], [4,5,6], [7,8,9]], mask=[0] + [1,0]*4)
        >>> x.tolist()
        [[1, None, 3], [None, 5, None], [7, None, 9]]
        >>> x.tolist(-999)
        [[1, -999, 3], [-999, 5, -999], [7, -999, 9]]

        """
        _mask = self._mask
        if _mask is nomask:
            return self._data.tolist()
        if fill_value is not None:
            return self.filled(fill_value).tolist()
        names = self.dtype.names
        if names:
            result = self._data.astype([(_, object) for _ in names])
            for n in names:
                result[n][_mask[n]] = None

            return result.tolist()
        if _mask is nomask:
            return [None]
        inishape = self.shape
        result = np.array((self._data.ravel()), dtype=object)
        result[_mask.ravel()] = None
        result.shape = inishape
        return result.tolist()

    def tostring(self, fill_value=None, order='C'):
        r"""
        A compatibility alias for `tobytes`, with exactly the same behavior.

        Despite its name, it returns `bytes` not `str`\ s.

        .. deprecated:: 1.19.0
        """
        warnings.warn('tostring() is deprecated. Use tobytes() instead.',
          DeprecationWarning,
          stacklevel=2)
        return self.tobytes(fill_value, order=order)

    def tobytes(self, fill_value=None, order='C'):
        r"""
        Return the array data as a string containing the raw bytes in the array.

        The array is filled with a fill value before the string conversion.

        .. versionadded:: 1.9.0

        Parameters
        ----------
        fill_value : scalar, optional
            Value used to fill in the masked values. Default is None, in which
            case `MaskedArray.fill_value` is used.
        order : {'C','F','A'}, optional
            Order of the data item in the copy. Default is 'C'.

            - 'C'   -- C order (row major).
            - 'F'   -- Fortran order (column major).
            - 'A'   -- Any, current order of array.
            - None  -- Same as 'A'.

        See Also
        --------
        numpy.ndarray.tobytes
        tolist, tofile

        Notes
        -----
        As for `ndarray.tobytes`, information about the shape, dtype, etc.,
        but also about `fill_value`, will be lost.

        Examples
        --------
        >>> x = np.ma.array(np.array([[1, 2], [3, 4]]), mask=[[0, 1], [1, 0]])
        >>> x.tobytes()
        b'\x01\x00\x00\x00\x00\x00\x00\x00?B\x0f\x00\x00\x00\x00\x00?B\x0f\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00'

        """
        return self.filled(fill_value).tobytes(order=order)

    def tofile(self, fid, sep='', format='%s'):
        """
        Save a masked array to a file in binary format.

        .. warning::
          This function is not implemented yet.

        Raises
        ------
        NotImplementedError
            When `tofile` is called.

        """
        raise NotImplementedError('MaskedArray.tofile() not implemented yet.')

    def toflex(self):
        """
        Transforms a masked array into a flexible-type array.

        The flexible type array that is returned will have two fields:

        * the ``_data`` field stores the ``_data`` part of the array.
        * the ``_mask`` field stores the ``_mask`` part of the array.

        Parameters
        ----------
        None

        Returns
        -------
        record : ndarray
            A new flexible-type `ndarray` with two fields: the first element
            containing a value, the second element containing the corresponding
            mask boolean. The returned record shape matches self.shape.

        Notes
        -----
        A side-effect of transforming a masked array into a flexible `ndarray` is
        that meta information (``fill_value``, ...) will be lost.

        Examples
        --------
        >>> x = np.ma.array([[1,2,3],[4,5,6],[7,8,9]], mask=[0] + [1,0]*4)
        >>> x
        masked_array(
          data=[[1, --, 3],
                [--, 5, --],
                [7, --, 9]],
          mask=[[False,  True, False],
                [ True, False,  True],
                [False,  True, False]],
          fill_value=999999)
        >>> x.toflex()
        array([[(1, False), (2,  True), (3, False)],
               [(4,  True), (5, False), (6,  True)],
               [(7, False), (8,  True), (9, False)]],
              dtype=[('_data', '<i8'), ('_mask', '?')])

        """
        ddtype = self.dtype
        _mask = self._mask
        if _mask is None:
            _mask = make_mask_none(self.shape, ddtype)
        mdtype = self._mask.dtype
        record = np.ndarray(shape=(self.shape), dtype=[
         (
          '_data', ddtype), ('_mask', mdtype)])
        record['_data'] = self._data
        record['_mask'] = self._mask
        return record

    torecords = toflex

    def __getstate__(self):
        cf = 'CF'[self.flags.fnc]
        data_state = super(MaskedArray, self).__reduce__()[2]
        return data_state + (getmaskarray(self).tobytes(cf), self._fill_value)

    def __setstate__(self, state):
        _, shp, typ, isf, raw, msk, flv = state
        super(MaskedArray, self).__setstate__((shp, typ, isf, raw))
        self._mask.__setstate__((shp, make_mask_descr(typ), isf, msk))
        self.fill_value = flv

    def __reduce__(self):
        """Return a 3-tuple for pickling a MaskedArray.

        """
        return (
         _mareconstruct,
         (
          self.__class__, self._baseclass, (0, ), 'b'),
         self.__getstate__())

    def __deepcopy__(self, memo=None):
        from copy import deepcopy
        copied = MaskedArray.__new__((type(self)), self, copy=True)
        if memo is None:
            memo = {}
        memo[id(self)] = copied
        for k, v in self.__dict__.items():
            copied.__dict__[k] = deepcopy(v, memo)

        return copied


def _mareconstruct(subtype, baseclass, baseshape, basetype):
    """Internal function that builds a new MaskedArray from the
    information stored in a pickle.

    """
    _data = ndarray.__new__(baseclass, baseshape, basetype)
    _mask = ndarray.__new__(ndarray, baseshape, make_mask_descr(basetype))
    return subtype.__new__(subtype, _data, mask=_mask, dtype=basetype)


class mvoid(MaskedArray):
    __doc__ = "\n    Fake a 'void' object to use for masked array with structured dtypes.\n    "

    def __new__(self, data, mask=nomask, dtype=None, fill_value=None, hardmask=False, copy=False, subok=True):
        _data = np.array(data, copy=copy, subok=subok, dtype=dtype)
        _data = _data.view(self)
        _data._hardmask = hardmask
        if mask is not nomask:
            if isinstance(mask, np.void):
                _data._mask = mask
            else:
                try:
                    _data._mask = np.void(mask)
                except TypeError:
                    mdtype = make_mask_descr(dtype)
                    _data._mask = np.array(mask, dtype=mdtype)[()]

            if fill_value is not None:
                _data.fill_value = fill_value
            return _data

    @property
    def _data(self):
        return super(mvoid, self)._data[()]

    def __getitem__(self, indx):
        """
        Get the index.

        """
        m = self._mask
        if isinstance(m[indx], ndarray):
            return masked_array(data=(self._data[indx]),
              mask=(m[indx]),
              fill_value=(self._fill_value[indx]),
              hard_mask=(self._hardmask))
        if m is not nomask:
            if m[indx]:
                return masked
        return self._data[indx]

    def __setitem__(self, indx, value):
        self._data[indx] = value
        if self._hardmask:
            self._mask[indx] |= getattr(value, '_mask', False)
        else:
            self._mask[indx] = getattr(value, '_mask', False)

    def __str__(self):
        m = self._mask
        if m is nomask:
            return str(self._data)
        rdtype = _replace_dtype_fields(self._data.dtype, 'O')
        data_arr = super(mvoid, self)._data
        res = data_arr.astype(rdtype)
        _recursive_printoption(res, self._mask, masked_print_option)
        return str(res)

    __repr__ = __str__

    def __iter__(self):
        """Defines an iterator for mvoid"""
        _data, _mask = self._data, self._mask
        if _mask is nomask:
            yield from _data
        else:
            for d, m in zip(_data, _mask):
                if m:
                    yield masked
                else:
                    yield d

    def __len__(self):
        return self._data.__len__()

    def filled(self, fill_value=None):
        """
        Return a copy with masked fields filled with a given value.

        Parameters
        ----------
        fill_value : array_like, optional
            The value to use for invalid entries. Can be scalar or
            non-scalar. If latter is the case, the filled array should
            be broadcastable over input array. Default is None, in
            which case the `fill_value` attribute is used instead.

        Returns
        -------
        filled_void
            A `np.void` object

        See Also
        --------
        MaskedArray.filled

        """
        return asarray(self).filled(fill_value)[()]

    def tolist(self):
        """
    Transforms the mvoid object into a tuple.

    Masked fields are replaced by None.

    Returns
    -------
    returned_tuple
        Tuple of fields
        """
        _mask = self._mask
        if _mask is nomask:
            return self._data.tolist()
        result = []
        for d, m in zip(self._data, self._mask):
            if m:
                result.append(None)
            else:
                result.append(d.item())

        return tuple(result)


def isMaskedArray(x):
    """
    Test whether input is an instance of MaskedArray.

    This function returns True if `x` is an instance of MaskedArray
    and returns False otherwise.  Any object is accepted as input.

    Parameters
    ----------
    x : object
        Object to test.

    Returns
    -------
    result : bool
        True if `x` is a MaskedArray.

    See Also
    --------
    isMA : Alias to isMaskedArray.
    isarray : Alias to isMaskedArray.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.eye(3, 3)
    >>> a
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])
    >>> m = ma.masked_values(a, 0)
    >>> m
    masked_array(
      data=[[1.0, --, --],
            [--, 1.0, --],
            [--, --, 1.0]],
      mask=[[False,  True,  True],
            [ True, False,  True],
            [ True,  True, False]],
      fill_value=0.0)
    >>> ma.isMaskedArray(a)
    False
    >>> ma.isMaskedArray(m)
    True
    >>> ma.isMaskedArray([0, 1, 2])
    False

    """
    return isinstance(x, MaskedArray)


isarray = isMaskedArray
isMA = isMaskedArray

class MaskedConstant(MaskedArray):
    _MaskedConstant__singleton = None

    @classmethod
    def __has_singleton(cls):
        return cls._MaskedConstant__singleton is not None and type(cls._MaskedConstant__singleton) is cls

    def __new__(cls):
        if not cls._MaskedConstant__has_singleton():
            data = np.array(0.0)
            mask = np.array(True)
            data.flags.writeable = False
            mask.flags.writeable = False
            cls._MaskedConstant__singleton = MaskedArray(data, mask=mask).view(cls)
        return cls._MaskedConstant__singleton

    def __array_finalize__(self, obj):
        if not self._MaskedConstant__has_singleton():
            return super(MaskedConstant, self).__array_finalize__(obj)
        if self is self._MaskedConstant__singleton:
            pass
        else:
            self.__class__ = MaskedArray
            MaskedArray.__array_finalize__(self, obj)

    def __array_prepare__(self, obj, context=None):
        return self.view(MaskedArray).__array_prepare__(obj, context)

    def __array_wrap__(self, obj, context=None):
        return self.view(MaskedArray).__array_wrap__(obj, context)

    def __str__(self):
        return str(masked_print_option._display)

    def __repr__(self):
        if self is MaskedConstant._MaskedConstant__singleton:
            return 'masked'
        return object.__repr__(self)

    def __format__(self, format_spec):
        try:
            return object.__format__(self, format_spec)
        except TypeError:
            warnings.warn('Format strings passed to MaskedConstant are ignored, but in future may error or produce different behavior',
              FutureWarning,
              stacklevel=2)
            return object.__format__(self, '')

    def __reduce__(self):
        """Override of MaskedArray's __reduce__.
        """
        return (
         self.__class__, ())

    def __iop__(self, other):
        return self

    __iadd__ = __isub__ = __imul__ = __ifloordiv__ = __itruediv__ = __ipow__ = __iop__
    del __iop__

    def copy(self, *args, **kwargs):
        """ Copy is a no-op on the maskedconstant, as it is a scalar """
        return self

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __setattr__(self, attr, value):
        if not self._MaskedConstant__has_singleton():
            return super(MaskedConstant, self).__setattr__(attr, value)
        if self is self._MaskedConstant__singleton:
            raise AttributeError(f"attributes of {self!r} are not writeable")
        else:
            return super(MaskedConstant, self).__setattr__(attr, value)


masked = masked_singleton = MaskedConstant()
masked_array = MaskedArray

def array(data, dtype=None, copy=False, order=None, mask=nomask, fill_value=None, keep_mask=True, hard_mask=False, shrink=True, subok=True, ndmin=0):
    """
    Shortcut to MaskedArray.

    The options are in a different order for convenience and backwards
    compatibility.

    """
    return MaskedArray(data, mask=mask, dtype=dtype, copy=copy, subok=subok,
      keep_mask=keep_mask,
      hard_mask=hard_mask,
      fill_value=fill_value,
      ndmin=ndmin,
      shrink=shrink,
      order=order)


array.__doc__ = masked_array.__doc__

def is_masked(x):
    """
    Determine whether input has masked values.

    Accepts any object as input, but always returns False unless the
    input is a MaskedArray containing masked values.

    Parameters
    ----------
    x : array_like
        Array to check for masked values.

    Returns
    -------
    result : bool
        True if `x` is a MaskedArray with masked values, False otherwise.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> x = ma.masked_equal([0, 1, 0, 2, 3], 0)
    >>> x
    masked_array(data=[--, 1, --, 2, 3],
                 mask=[ True, False,  True, False, False],
           fill_value=0)
    >>> ma.is_masked(x)
    True
    >>> x = ma.masked_equal([0, 1, 0, 2, 3], 42)
    >>> x
    masked_array(data=[0, 1, 0, 2, 3],
                 mask=False,
           fill_value=42)
    >>> ma.is_masked(x)
    False

    Always returns False if `x` isn't a MaskedArray.

    >>> x = [False, True, False]
    >>> ma.is_masked(x)
    False
    >>> x = 'a string'
    >>> ma.is_masked(x)
    False

    """
    m = getmask(x)
    if m is nomask:
        return False
    if m.any():
        return True
    return False


class _extrema_operation(_MaskedUFunc):
    __doc__ = '\n    Generic class for maximum/minimum functions.\n\n    .. note::\n      This is the base class for `_maximum_operation` and\n      `_minimum_operation`.\n\n    '

    def __init__(self, ufunc, compare, fill_value):
        super(_extrema_operation, self).__init__(ufunc)
        self.compare = compare
        self.fill_value_func = fill_value

    def __call__(self, a, b=None):
        """Executes the call behavior."""
        if b is None:
            warnings.warn(f"Single-argument form of np.ma.{self.__name__} is deprecated. Use np.ma.{self.__name__}.reduce instead.",
              DeprecationWarning,
              stacklevel=2)
            return self.reduce(a)
        return where(self.compare(a, b), a, b)

    def reduce(self, target, axis=np._NoValue):
        """Reduce target along the given axis."""
        target = narray(target, copy=False, subok=True)
        m = getmask(target)
        if axis is np._NoValue:
            if target.ndim > 1:
                warnings.warn(f"In the future the default for ma.{self.__name__}.reduce will be axis=0, not the current None, to match np.{self.__name__}.reduce. Explicitly pass 0 or None to silence this warning.",
                  MaskedArrayFutureWarning,
                  stacklevel=2)
                axis = None
        if axis is not np._NoValue:
            kwargs = dict(axis=axis)
        else:
            kwargs = dict()
        if m is nomask:
            t = (self.f.reduce)(target, **kwargs)
        else:
            target = target.filled(self.fill_value_func(target)).view(type(target))
            t = (self.f.reduce)(target, **kwargs)
            m = (umath.logical_and.reduce)(m, **kwargs)
            if hasattr(t, '_mask'):
                t._mask = m
            elif m:
                t = masked
        return t

    def outer(self, a, b):
        """Return the function applied to the outer product of a and b."""
        ma = getmask(a)
        mb = getmask(b)
        if ma is nomask and mb is nomask:
            m = nomask
        else:
            ma = getmaskarray(a)
            mb = getmaskarray(b)
            m = logical_or.outer(ma, mb)
        result = self.f.outer(filled(a), filled(b))
        if not isinstance(result, MaskedArray):
            result = result.view(MaskedArray)
        result._mask = m
        return result


def min(obj, axis=None, out=None, fill_value=None, keepdims=np._NoValue):
    kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
    try:
        return (obj.min)(axis=axis, fill_value=fill_value, out=out, **kwargs)
    except (AttributeError, TypeError):
        return (asanyarray(obj).min)(axis=axis, fill_value=fill_value, out=out, **kwargs)


min.__doc__ = MaskedArray.min.__doc__

def max(obj, axis=None, out=None, fill_value=None, keepdims=np._NoValue):
    kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
    try:
        return (obj.max)(axis=axis, fill_value=fill_value, out=out, **kwargs)
    except (AttributeError, TypeError):
        return (asanyarray(obj).max)(axis=axis, fill_value=fill_value, out=out, **kwargs)


max.__doc__ = MaskedArray.max.__doc__

def ptp(obj, axis=None, out=None, fill_value=None, keepdims=np._NoValue):
    kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}
    try:
        return (obj.ptp)(axis, out=out, fill_value=fill_value, **kwargs)
    except (AttributeError, TypeError):
        return (asanyarray(obj).ptp)(axis=axis, fill_value=fill_value, out=out, **kwargs)


ptp.__doc__ = MaskedArray.ptp.__doc__

class _frommethod:
    __doc__ = '\n    Define functions from existing MaskedArray methods.\n\n    Parameters\n    ----------\n    methodname : str\n        Name of the method to transform.\n\n    '

    def __init__(self, methodname, reversed=False):
        self.__name__ = methodname
        self.__doc__ = self.getdoc()
        self.reversed = reversed

    def getdoc(self):
        """Return the doc of the function (from the doc of the method)."""
        meth = getattr(MaskedArray, self.__name__, None) or getattr(np, self.__name__, None)
        signature = self.__name__ + get_object_signature(meth)
        if meth is not None:
            doc = '    %s\n%s' % (
             signature, getattr(meth, '__doc__', None))
            return doc

    def __call__(self, a, *args, **params):
        if self.reversed:
            args = list(args)
            a, args[0] = args[0], a
        marr = asanyarray(a)
        method_name = self.__name__
        method = getattr(type(marr), method_name, None)
        if method is None:
            method = getattr(np, method_name)
        return method(marr, *args, **params)


all = _frommethod('all')
anomalies = anom = _frommethod('anom')
any = _frommethod('any')
compress = _frommethod('compress', reversed=True)
cumprod = _frommethod('cumprod')
cumsum = _frommethod('cumsum')
copy = _frommethod('copy')
diagonal = _frommethod('diagonal')
harden_mask = _frommethod('harden_mask')
ids = _frommethod('ids')
maximum = _extrema_operation(umath.maximum, greater, maximum_fill_value)
mean = _frommethod('mean')
minimum = _extrema_operation(umath.minimum, less, minimum_fill_value)
nonzero = _frommethod('nonzero')
prod = _frommethod('prod')
product = _frommethod('prod')
ravel = _frommethod('ravel')
repeat = _frommethod('repeat')
shrink_mask = _frommethod('shrink_mask')
soften_mask = _frommethod('soften_mask')
std = _frommethod('std')
sum = _frommethod('sum')
swapaxes = _frommethod('swapaxes')
trace = _frommethod('trace')
var = _frommethod('var')
count = _frommethod('count')

def take(a, indices, axis=None, out=None, mode='raise'):
    """
    """
    a = masked_array(a)
    return a.take(indices, axis=axis, out=out, mode=mode)


def power(a, b, third=None):
    """
    Returns element-wise base array raised to power from second array.

    This is the masked array version of `numpy.power`. For details see
    `numpy.power`.

    See Also
    --------
    numpy.power

    Notes
    -----
    The *out* argument to `numpy.power` is not supported, `third` has to be
    None.

    """
    if third is not None:
        raise MaskError('3-argument power not supported.')
    ma = getmask(a)
    mb = getmask(b)
    m = mask_or(ma, mb)
    fa = getdata(a)
    fb = getdata(b)
    if isinstance(a, MaskedArray):
        basetype = type(a)
    else:
        basetype = MaskedArray
    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.where(m, fa, umath.power(fa, fb)).view(basetype)
    result._update_from(a)
    invalid = np.logical_not(np.isfinite(result.view(ndarray)))
    if m is not nomask:
        if not result.ndim:
            return masked
        result._mask = np.logical_or(m, invalid)
    if invalid.any():
        if not result.ndim:
            return masked
        if result._mask is nomask:
            result._mask = invalid
        result._data[invalid] = result.fill_value
    return result


argmin = _frommethod('argmin')
argmax = _frommethod('argmax')

def argsort(a, axis=np._NoValue, kind=None, order=None, endwith=True, fill_value=None):
    """Function version of the eponymous method."""
    a = np.asanyarray(a)
    if axis is np._NoValue:
        axis = _deprecate_argsort_axis(a)
    if isinstance(a, MaskedArray):
        return a.argsort(axis=axis, kind=kind, order=order, endwith=endwith,
          fill_value=fill_value)
    return a.argsort(axis=axis, kind=kind, order=order)


argsort.__doc__ = MaskedArray.argsort.__doc__

def sort(a, axis=-1, kind=None, order=None, endwith=True, fill_value=None):
    """
    Return a sorted copy of the masked array.

    Equivalent to creating a copy of the array
    and applying the  MaskedArray ``sort()`` method.

    Refer to ``MaskedArray.sort`` for the full documentation

    See Also
    --------
    MaskedArray.sort : equivalent method
    """
    a = np.array(a, copy=True, subok=True)
    if axis is None:
        a = a.flatten()
        axis = 0
    if isinstance(a, MaskedArray):
        a.sort(axis=axis, kind=kind, order=order, endwith=endwith,
          fill_value=fill_value)
    else:
        a.sort(axis=axis, kind=kind, order=order)
    return a


def compressed(x):
    """
    Return all the non-masked data as a 1-D array.

    This function is equivalent to calling the "compressed" method of a
    `ma.MaskedArray`, see `ma.MaskedArray.compressed` for details.

    See Also
    --------
    ma.MaskedArray.compressed
        Equivalent method.

    """
    return asanyarray(x).compressed()


def concatenate(arrays, axis=0):
    """
    Concatenate a sequence of arrays along the given axis.

    Parameters
    ----------
    arrays : sequence of array_like
        The arrays must have the same shape, except in the dimension
        corresponding to `axis` (the first, by default).
    axis : int, optional
        The axis along which the arrays will be joined. Default is 0.

    Returns
    -------
    result : MaskedArray
        The concatenated array with any masked entries preserved.

    See Also
    --------
    numpy.concatenate : Equivalent function in the top-level NumPy module.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = ma.arange(3)
    >>> a[1] = ma.masked
    >>> b = ma.arange(2, 5)
    >>> a
    masked_array(data=[0, --, 2],
                 mask=[False,  True, False],
           fill_value=999999)
    >>> b
    masked_array(data=[2, 3, 4],
                 mask=False,
           fill_value=999999)
    >>> ma.concatenate([a, b])
    masked_array(data=[0, --, 2, 2, 3, 4],
                 mask=[False,  True, False, False, False, False],
           fill_value=999999)

    """
    d = np.concatenate([getdata(a) for a in arrays], axis)
    rcls = get_masked_subclass(*arrays)
    data = d.view(rcls)
    for x in arrays:
        if getmask(x) is not nomask:
            break
    else:
        return data
    dm = np.concatenate([getmaskarray(a) for a in arrays], axis)
    dm = dm.reshape(d.shape)
    data._mask = _shrink_mask(dm)
    return data


def diag(v, k=0):
    """
    Extract a diagonal or construct a diagonal array.

    This function is the equivalent of `numpy.diag` that takes masked
    values into account, see `numpy.diag` for details.

    See Also
    --------
    numpy.diag : Equivalent function for ndarrays.

    """
    output = np.diag(v, k).view(MaskedArray)
    if getmask(v) is not nomask:
        output._mask = np.diag(v._mask, k)
    return output


def left_shift(a, n):
    """
    Shift the bits of an integer to the left.

    This is the masked array version of `numpy.left_shift`, for details
    see that function.

    See Also
    --------
    numpy.left_shift

    """
    m = getmask(a)
    if m is nomask:
        d = umath.left_shift(filled(a), n)
        return masked_array(d)
    d = umath.left_shift(filled(a, 0), n)
    return masked_array(d, mask=m)


def right_shift(a, n):
    """
    Shift the bits of an integer to the right.

    This is the masked array version of `numpy.right_shift`, for details
    see that function.

    See Also
    --------
    numpy.right_shift

    """
    m = getmask(a)
    if m is nomask:
        d = umath.right_shift(filled(a), n)
        return masked_array(d)
    d = umath.right_shift(filled(a, 0), n)
    return masked_array(d, mask=m)


def put(a, indices, values, mode='raise'):
    """
    Set storage-indexed locations to corresponding values.

    This function is equivalent to `MaskedArray.put`, see that method
    for details.

    See Also
    --------
    MaskedArray.put

    """
    try:
        return a.put(indices, values, mode=mode)
    except AttributeError:
        return narray(a, copy=False).put(indices, values, mode=mode)


def putmask(a, mask, values):
    """
    Changes elements of an array based on conditional and input values.

    This is the masked array version of `numpy.putmask`, for details see
    `numpy.putmask`.

    See Also
    --------
    numpy.putmask

    Notes
    -----
    Using a masked array as `values` will **not** transform a `ndarray` into
    a `MaskedArray`.

    """
    if not isinstance(a, MaskedArray):
        a = a.view(MaskedArray)
    valdata, valmask = getdata(values), getmask(values)
    if getmask(a) is nomask:
        if valmask is not nomask:
            a._sharedmask = True
            a._mask = make_mask_none(a.shape, a.dtype)
            np.copyto((a._mask), valmask, where=mask)
    elif a._hardmask:
        if valmask is not nomask:
            m = a._mask.copy()
            np.copyto(m, valmask, where=mask)
            a.mask |= m
    else:
        if valmask is nomask:
            valmask = getmaskarray(values)
        np.copyto((a._mask), valmask, where=mask)
    np.copyto((a._data), valdata, where=mask)


def transpose(a, axes=None):
    """
    Permute the dimensions of an array.

    This function is exactly equivalent to `numpy.transpose`.

    See Also
    --------
    numpy.transpose : Equivalent function in top-level NumPy module.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> x = ma.arange(4).reshape((2,2))
    >>> x[1, 1] = ma.masked
    >>> x
    masked_array(
      data=[[0, 1],
            [2, --]],
      mask=[[False, False],
            [False,  True]],
      fill_value=999999)

    >>> ma.transpose(x)
    masked_array(
      data=[[0, 2],
            [1, --]],
      mask=[[False, False],
            [False,  True]],
      fill_value=999999)
    """
    try:
        return a.transpose(axes)
    except AttributeError:
        return narray(a, copy=False).transpose(axes).view(MaskedArray)


def reshape(a, new_shape, order='C'):
    """
    Returns an array containing the same data with a new shape.

    Refer to `MaskedArray.reshape` for full documentation.

    See Also
    --------
    MaskedArray.reshape : equivalent function

    """
    try:
        return a.reshape(new_shape, order=order)
    except AttributeError:
        _tmp = narray(a, copy=False).reshape(new_shape, order=order)
        return _tmp.view(MaskedArray)


def resize(x, new_shape):
    """
    Return a new masked array with the specified size and shape.

    This is the masked equivalent of the `numpy.resize` function. The new
    array is filled with repeated copies of `x` (in the order that the
    data are stored in memory). If `x` is masked, the new array will be
    masked, and the new mask will be a repetition of the old one.

    See Also
    --------
    numpy.resize : Equivalent function in the top level NumPy module.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = ma.array([[1, 2] ,[3, 4]])
    >>> a[0, 1] = ma.masked
    >>> a
    masked_array(
      data=[[1, --],
            [3, 4]],
      mask=[[False,  True],
            [False, False]],
      fill_value=999999)
    >>> np.resize(a, (3, 3))
    masked_array(
      data=[[1, 2, 3],
            [4, 1, 2],
            [3, 4, 1]],
      mask=False,
      fill_value=999999)
    >>> ma.resize(a, (3, 3))
    masked_array(
      data=[[1, --, 3],
            [4, 1, --],
            [3, 4, 1]],
      mask=[[False,  True, False],
            [False, False,  True],
            [False, False, False]],
      fill_value=999999)

    A MaskedArray is always returned, regardless of the input type.

    >>> a = np.array([[1, 2] ,[3, 4]])
    >>> ma.resize(a, (3, 3))
    masked_array(
      data=[[1, 2, 3],
            [4, 1, 2],
            [3, 4, 1]],
      mask=False,
      fill_value=999999)

    """
    m = getmask(x)
    if m is not nomask:
        m = np.resize(m, new_shape)
    result = np.resize(x, new_shape).view(get_masked_subclass(x))
    if result.ndim:
        result._mask = m
    return result


def ndim(obj):
    """
    maskedarray version of the numpy function.

    """
    return np.ndim(getdata(obj))


ndim.__doc__ = np.ndim.__doc__

def shape(obj):
    """maskedarray version of the numpy function."""
    return np.shape(getdata(obj))


shape.__doc__ = np.shape.__doc__

def size(obj, axis=None):
    """maskedarray version of the numpy function."""
    return np.size(getdata(obj), axis)


size.__doc__ = np.size.__doc__

def where(condition, x=_NoValue, y=_NoValue):
    """
    Return a masked array with elements from `x` or `y`, depending on condition.

    .. note::
        When only `condition` is provided, this function is identical to
        `nonzero`. The rest of this documentation covers only the case where
        all three arguments are provided.

    Parameters
    ----------
    condition : array_like, bool
        Where True, yield `x`, otherwise yield `y`.
    x, y : array_like, optional
        Values from which to choose. `x`, `y` and `condition` need to be
        broadcastable to some shape.

    Returns
    -------
    out : MaskedArray
        An masked array with `masked` elements where the condition is masked,
        elements from `x` where `condition` is True, and elements from `y`
        elsewhere.

    See Also
    --------
    numpy.where : Equivalent function in the top-level NumPy module.
    nonzero : The function that is called when x and y are omitted

    Examples
    --------
    >>> x = np.ma.array(np.arange(9.).reshape(3, 3), mask=[[0, 1, 0],
    ...                                                    [1, 0, 1],
    ...                                                    [0, 1, 0]])
    >>> x
    masked_array(
      data=[[0.0, --, 2.0],
            [--, 4.0, --],
            [6.0, --, 8.0]],
      mask=[[False,  True, False],
            [ True, False,  True],
            [False,  True, False]],
      fill_value=1e+20)
    >>> np.ma.where(x > 5, x, -3.1416)
    masked_array(
      data=[[-3.1416, --, -3.1416],
            [--, -3.1416, --],
            [6.0, --, 8.0]],
      mask=[[False,  True, False],
            [ True, False,  True],
            [False,  True, False]],
      fill_value=1e+20)

    """
    missing = (
     x is _NoValue, y is _NoValue).count(True)
    if missing == 1:
        raise ValueError("Must provide both 'x' and 'y' or neither.")
    if missing == 2:
        return nonzero(condition)
    cf = filled(condition, False)
    xd = getdata(x)
    yd = getdata(y)
    cm = getmaskarray(condition)
    xm = getmaskarray(x)
    ym = getmaskarray(y)
    if x is masked and y is not masked:
        xd = np.zeros((), dtype=(yd.dtype))
        xm = np.ones((), dtype=(ym.dtype))
    elif y is masked:
        if x is not masked:
            yd = np.zeros((), dtype=(xd.dtype))
            ym = np.ones((), dtype=(xm.dtype))
    data = np.where(cf, xd, yd)
    mask = np.where(cf, xm, ym)
    mask = np.where(cm, np.ones((), dtype=(mask.dtype)), mask)
    mask = _shrink_mask(mask)
    return masked_array(data, mask=mask)


def choose(indices, choices, out=None, mode='raise'):
    """
    Use an index array to construct a new array from a set of choices.

    Given an array of integers and a set of n choice arrays, this method
    will create a new array that merges each of the choice arrays.  Where a
    value in `a` is i, the new array will have the value that choices[i]
    contains in the same place.

    Parameters
    ----------
    a : ndarray of ints
        This array must contain integers in ``[0, n-1]``, where n is the
        number of choices.
    choices : sequence of arrays
        Choice arrays. The index array and all of the choices should be
        broadcastable to the same shape.
    out : array, optional
        If provided, the result will be inserted into this array. It should
        be of the appropriate shape and `dtype`.
    mode : {'raise', 'wrap', 'clip'}, optional
        Specifies how out-of-bounds indices will behave.

        * 'raise' : raise an error
        * 'wrap' : wrap around
        * 'clip' : clip to the range

    Returns
    -------
    merged_array : array

    See Also
    --------
    choose : equivalent function

    Examples
    --------
    >>> choice = np.array([[1,1,1], [2,2,2], [3,3,3]])
    >>> a = np.array([2, 1, 0])
    >>> np.ma.choose(a, choice)
    masked_array(data=[3, 2, 1],
                 mask=False,
           fill_value=999999)

    """

    def fmask(x):
        """Returns the filled array, or True if masked."""
        if x is masked:
            return True
        return filled(x)

    def nmask(x):
        """Returns the mask, True if ``masked``, False if ``nomask``."""
        if x is masked:
            return True
        return getmask(x)

    c = filled(indices, 0)
    masks = [nmask(x) for x in choices]
    data = [fmask(x) for x in choices]
    outputmask = np.choose(c, masks, mode=mode)
    outputmask = make_mask((mask_or(outputmask, getmask(indices))), copy=False,
      shrink=True)
    d = np.choose(c, data, mode=mode, out=out).view(MaskedArray)
    if out is not None:
        if isinstance(out, MaskedArray):
            out.__setmask__(outputmask)
        return out
    d.__setmask__(outputmask)
    return d


def round_(a, decimals=0, out=None):
    """
    Return a copy of a, rounded to 'decimals' places.

    When 'decimals' is negative, it specifies the number of positions
    to the left of the decimal point.  The real and imaginary parts of
    complex numbers are rounded separately. Nothing is done if the
    array is not of float type and 'decimals' is greater than or equal
    to 0.

    Parameters
    ----------
    decimals : int
        Number of decimals to round to. May be negative.
    out : array_like
        Existing array to use for output.
        If not given, returns a default copy of a.

    Notes
    -----
    If out is given and does not have a mask attribute, the mask of a
    is lost!

    """
    if out is None:
        return np.round_(a, decimals, out)
    np.round_(getdata(a), decimals, out)
    if hasattr(out, '_mask'):
        out._mask = getmask(a)
    return out


round = round_

def mask_rowcols(a, axis=None):
    """
    Mask rows and/or columns of a 2D array that contain masked values.

    Mask whole rows and/or columns of a 2D array that contain
    masked values.  The masking behavior is selected using the
    `axis` parameter.

      - If `axis` is None, rows *and* columns are masked.
      - If `axis` is 0, only rows are masked.
      - If `axis` is 1 or -1, only columns are masked.

    Parameters
    ----------
    a : array_like, MaskedArray
        The array to mask.  If not a MaskedArray instance (or if no array
        elements are masked).  The result is a MaskedArray with `mask` set
        to `nomask` (False). Must be a 2D array.
    axis : int, optional
        Axis along which to perform the operation. If None, applies to a
        flattened version of the array.

    Returns
    -------
    a : MaskedArray
        A modified version of the input array, masked depending on the value
        of the `axis` parameter.

    Raises
    ------
    NotImplementedError
        If input array `a` is not 2D.

    See Also
    --------
    mask_rows : Mask rows of a 2D array that contain masked values.
    mask_cols : Mask cols of a 2D array that contain masked values.
    masked_where : Mask where a condition is met.

    Notes
    -----
    The input array's mask is modified by this function.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = np.zeros((3, 3), dtype=int)
    >>> a[1, 1] = 1
    >>> a
    array([[0, 0, 0],
           [0, 1, 0],
           [0, 0, 0]])
    >>> a = ma.masked_equal(a, 1)
    >>> a
    masked_array(
      data=[[0, 0, 0],
            [0, --, 0],
            [0, 0, 0]],
      mask=[[False, False, False],
            [False,  True, False],
            [False, False, False]],
      fill_value=1)
    >>> ma.mask_rowcols(a)
    masked_array(
      data=[[0, --, 0],
            [--, --, --],
            [0, --, 0]],
      mask=[[False,  True, False],
            [ True,  True,  True],
            [False,  True, False]],
      fill_value=1)

    """
    a = array(a, subok=False)
    if a.ndim != 2:
        raise NotImplementedError('mask_rowcols works for 2D arrays only.')
    m = getmask(a)
    if not (m is nomask or m.any()):
        return a
    maskedval = m.nonzero()
    a._mask = a._mask.copy()
    if not axis:
        a[np.unique(maskedval[0])] = masked
    if axis in (None, 1, -1):
        a[:, np.unique(maskedval[1])] = masked
    return a


def dot(a, b, strict=False, out=None):
    """
    Return the dot product of two arrays.

    This function is the equivalent of `numpy.dot` that takes masked values
    into account. Note that `strict` and `out` are in different position
    than in the method version. In order to maintain compatibility with the
    corresponding method, it is recommended that the optional arguments be
    treated as keyword only.  At some point that may be mandatory.

    .. note::
      Works only with 2-D arrays at the moment.

    Parameters
    ----------
    a, b : masked_array_like
        Inputs arrays.
    strict : bool, optional
        Whether masked data are propagated (True) or set to 0 (False) for
        the computation. Default is False.  Propagating the mask means that
        if a masked value appears in a row or column, the whole row or
        column is considered masked.
    out : masked_array, optional
        Output argument. This must have the exact kind that would be returned
        if it was not used. In particular, it must have the right type, must be
        C-contiguous, and its dtype must be the dtype that would be returned
        for `dot(a,b)`. This is a performance feature. Therefore, if these
        conditions are not met, an exception is raised, instead of attempting
        to be flexible.

        .. versionadded:: 1.10.2

    See Also
    --------
    numpy.dot : Equivalent function for ndarrays.

    Examples
    --------
    >>> a = np.ma.array([[1, 2, 3], [4, 5, 6]], mask=[[1, 0, 0], [0, 0, 0]])
    >>> b = np.ma.array([[1, 2], [3, 4], [5, 6]], mask=[[1, 0], [0, 0], [0, 0]])
    >>> np.ma.dot(a, b)
    masked_array(
      data=[[21, 26],
            [45, 64]],
      mask=[[False, False],
            [False, False]],
      fill_value=999999)
    >>> np.ma.dot(a, b, strict=True)
    masked_array(
      data=[[--, --],
            [--, 64]],
      mask=[[ True,  True],
            [ True, False]],
      fill_value=999999)

    """
    if strict:
        if a.ndim == 2:
            if b.ndim == 2:
                a = mask_rowcols(a, 0)
                b = mask_rowcols(b, 1)
    am = ~getmaskarray(a)
    bm = ~getmaskarray(b)
    if out is None:
        d = np.dot(filled(a, 0), filled(b, 0))
        m = ~np.dot(am, bm)
        if d.ndim == 0:
            d = np.asarray(d)
        r = d.view(get_masked_subclass(a, b))
        r.__setmask__(m)
        return r
    d = np.dot(filled(a, 0), filled(b, 0), out._data)
    if out.mask.shape != d.shape:
        out._mask = np.empty(d.shape, MaskType)
    np.dot(am, bm, out._mask)
    np.logical_not(out._mask, out._mask)
    return out


def inner(a, b):
    """
    Returns the inner product of a and b for arrays of floating point types.

    Like the generic NumPy equivalent the product sum is over the last dimension
    of a and b. The first argument is not conjugated.

    """
    fa = filled(a, 0)
    fb = filled(b, 0)
    if fa.ndim == 0:
        fa.shape = (1, )
    if fb.ndim == 0:
        fb.shape = (1, )
    return np.inner(fa, fb).view(MaskedArray)


inner.__doc__ = doc_note(np.inner.__doc__, 'Masked values are replaced by 0.')
innerproduct = inner

def outer(a, b):
    """maskedarray version of the numpy function."""
    fa = filled(a, 0).ravel()
    fb = filled(b, 0).ravel()
    d = np.outer(fa, fb)
    ma = getmask(a)
    mb = getmask(b)
    if ma is nomask:
        if mb is nomask:
            return masked_array(d)
    ma = getmaskarray(a)
    mb = getmaskarray(b)
    m = make_mask((1 - np.outer(1 - ma, 1 - mb)), copy=False)
    return masked_array(d, mask=m)


outer.__doc__ = doc_note(np.outer.__doc__, 'Masked values are replaced by 0.')
outerproduct = outer

def _convolve_or_correlate(f, a, v, mode, propagate_mask):
    """
    Helper function for ma.correlate and ma.convolve
    """
    if propagate_mask:
        mask = f((getmaskarray(a)), np.ones((np.shape(v)), dtype=bool), mode=mode) | f(np.ones((np.shape(a)), dtype=bool), (getmaskarray(v)), mode=mode)
        data = f((getdata(a)), (getdata(v)), mode=mode)
    else:
        mask = ~f(~getmaskarray(a), ~getmaskarray(v))
        data = f((filled(a, 0)), (filled(v, 0)), mode=mode)
    return masked_array(data, mask=mask)


def correlate(a, v, mode='valid', propagate_mask=True):
    """
    Cross-correlation of two 1-dimensional sequences.

    Parameters
    ----------
    a, v : array_like
        Input sequences.
    mode : {'valid', 'same', 'full'}, optional
        Refer to the `np.convolve` docstring.  Note that the default
        is 'valid', unlike `convolve`, which uses 'full'.
    propagate_mask : bool
        If True, then a result element is masked if any masked element contributes towards it.
        If False, then a result element is only masked if no non-masked element
        contribute towards it

    Returns
    -------
    out : MaskedArray
        Discrete cross-correlation of `a` and `v`.

    See Also
    --------
    numpy.correlate : Equivalent function in the top-level NumPy module.
    """
    return _convolve_or_correlate(np.correlate, a, v, mode, propagate_mask)


def convolve(a, v, mode='full', propagate_mask=True):
    """
    Returns the discrete, linear convolution of two one-dimensional sequences.

    Parameters
    ----------
    a, v : array_like
        Input sequences.
    mode : {'valid', 'same', 'full'}, optional
        Refer to the `np.convolve` docstring.
    propagate_mask : bool
        If True, then if any masked element is included in the sum for a result
        element, then the result is masked.
        If False, then the result element is only masked if no non-masked cells
        contribute towards it

    Returns
    -------
    out : MaskedArray
        Discrete, linear convolution of `a` and `v`.

    See Also
    --------
    numpy.convolve : Equivalent function in the top-level NumPy module.
    """
    return _convolve_or_correlate(np.convolve, a, v, mode, propagate_mask)


def allequal(a, b, fill_value=True):
    """
    Return True if all entries of a and b are equal, using
    fill_value as a truth value where either or both are masked.

    Parameters
    ----------
    a, b : array_like
        Input arrays to compare.
    fill_value : bool, optional
        Whether masked values in a or b are considered equal (True) or not
        (False).

    Returns
    -------
    y : bool
        Returns True if the two arrays are equal within the given
        tolerance, False otherwise. If either array contains NaN,
        then False is returned.

    See Also
    --------
    all, any
    numpy.ma.allclose

    Examples
    --------
    >>> a = np.ma.array([1e10, 1e-7, 42.0], mask=[0, 0, 1])
    >>> a
    masked_array(data=[10000000000.0, 1e-07, --],
                 mask=[False, False,  True],
           fill_value=1e+20)

    >>> b = np.array([1e10, 1e-7, -42.0])
    >>> b
    array([  1.00000000e+10,   1.00000000e-07,  -4.20000000e+01])
    >>> np.ma.allequal(a, b, fill_value=False)
    False
    >>> np.ma.allequal(a, b)
    True

    """
    m = mask_or(getmask(a), getmask(b))
    if m is nomask:
        x = getdata(a)
        y = getdata(b)
        d = umath.equal(x, y)
        return d.all()
    if fill_value:
        x = getdata(a)
        y = getdata(b)
        d = umath.equal(x, y)
        dm = array(d, mask=m, copy=False)
        return dm.filled(True).all(None)
    return False


def allclose(a, b, masked_equal=True, rtol=1e-05, atol=1e-08):
    """
    Returns True if two arrays are element-wise equal within a tolerance.

    This function is equivalent to `allclose` except that masked values
    are treated as equal (default) or unequal, depending on the `masked_equal`
    argument.

    Parameters
    ----------
    a, b : array_like
        Input arrays to compare.
    masked_equal : bool, optional
        Whether masked values in `a` and `b` are considered equal (True) or not
        (False). They are considered equal by default.
    rtol : float, optional
        Relative tolerance. The relative difference is equal to ``rtol * b``.
        Default is 1e-5.
    atol : float, optional
        Absolute tolerance. The absolute difference is equal to `atol`.
        Default is 1e-8.

    Returns
    -------
    y : bool
        Returns True if the two arrays are equal within the given
        tolerance, False otherwise. If either array contains NaN, then
        False is returned.

    See Also
    --------
    all, any
    numpy.allclose : the non-masked `allclose`.

    Notes
    -----
    If the following equation is element-wise True, then `allclose` returns
    True::

      absolute(`a` - `b`) <= (`atol` + `rtol` * absolute(`b`))

    Return True if all elements of `a` and `b` are equal subject to
    given tolerances.

    Examples
    --------
    >>> a = np.ma.array([1e10, 1e-7, 42.0], mask=[0, 0, 1])
    >>> a
    masked_array(data=[10000000000.0, 1e-07, --],
                 mask=[False, False,  True],
           fill_value=1e+20)
    >>> b = np.ma.array([1e10, 1e-8, -42.0], mask=[0, 0, 1])
    >>> np.ma.allclose(a, b)
    False

    >>> a = np.ma.array([1e10, 1e-8, 42.0], mask=[0, 0, 1])
    >>> b = np.ma.array([1.00001e10, 1e-9, -42.0], mask=[0, 0, 1])
    >>> np.ma.allclose(a, b)
    True
    >>> np.ma.allclose(a, b, masked_equal=False)
    False

    Masked values are not compared directly.

    >>> a = np.ma.array([1e10, 1e-8, 42.0], mask=[0, 0, 1])
    >>> b = np.ma.array([1.00001e10, 1e-9, 42.0], mask=[0, 0, 1])
    >>> np.ma.allclose(a, b)
    True
    >>> np.ma.allclose(a, b, masked_equal=False)
    False

    """
    x = masked_array(a, copy=False)
    y = masked_array(b, copy=False)
    if y.dtype.kind != 'm':
        dtype = np.result_type(y, 1.0)
        if y.dtype != dtype:
            y = masked_array(y, dtype=dtype, copy=False)
    m = mask_or(getmask(x), getmask(y))
    xinf = np.isinf(masked_array(x, copy=False, mask=m)).filled(False)
    if not np.all(xinf == filled(np.isinf(y), False)):
        return False
    if not np.any(xinf):
        d = filled(less_equal(absolute(x - y), atol + rtol * absolute(y)), masked_equal)
        return np.all(d)
    if not np.all(filled(x[xinf] == y[xinf], masked_equal)):
        return False
    x = x[(~xinf)]
    y = y[(~xinf)]
    d = filled(less_equal(absolute(x - y), atol + rtol * absolute(y)), masked_equal)
    return np.all(d)


def asarray(a, dtype=None, order=None):
    """
    Convert the input to a masked array of the given data-type.

    No copy is performed if the input is already an `ndarray`. If `a` is
    a subclass of `MaskedArray`, a base class `MaskedArray` is returned.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to a masked array. This
        includes lists, lists of tuples, tuples, tuples of tuples, tuples
        of lists, ndarrays and masked arrays.
    dtype : dtype, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F'}, optional
        Whether to use row-major ('C') or column-major ('FORTRAN') memory
        representation.  Default is 'C'.

    Returns
    -------
    out : MaskedArray
        Masked array interpretation of `a`.

    See Also
    --------
    asanyarray : Similar to `asarray`, but conserves subclasses.

    Examples
    --------
    >>> x = np.arange(10.).reshape(2, 5)
    >>> x
    array([[0., 1., 2., 3., 4.],
           [5., 6., 7., 8., 9.]])
    >>> np.ma.asarray(x)
    masked_array(
      data=[[0., 1., 2., 3., 4.],
            [5., 6., 7., 8., 9.]],
      mask=False,
      fill_value=1e+20)
    >>> type(np.ma.asarray(x))
    <class 'numpy.ma.core.MaskedArray'>

    """
    order = order or 'C'
    return masked_array(a, dtype=dtype, copy=False, keep_mask=True, subok=False,
      order=order)


def asanyarray(a, dtype=None):
    """
    Convert the input to a masked array, conserving subclasses.

    If `a` is a subclass of `MaskedArray`, its class is conserved.
    No copy is performed if the input is already an `ndarray`.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.
    dtype : dtype, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F'}, optional
        Whether to use row-major ('C') or column-major ('FORTRAN') memory
        representation.  Default is 'C'.

    Returns
    -------
    out : MaskedArray
        MaskedArray interpretation of `a`.

    See Also
    --------
    asarray : Similar to `asanyarray`, but does not conserve subclass.

    Examples
    --------
    >>> x = np.arange(10.).reshape(2, 5)
    >>> x
    array([[0., 1., 2., 3., 4.],
           [5., 6., 7., 8., 9.]])
    >>> np.ma.asanyarray(x)
    masked_array(
      data=[[0., 1., 2., 3., 4.],
            [5., 6., 7., 8., 9.]],
      mask=False,
      fill_value=1e+20)
    >>> type(np.ma.asanyarray(x))
    <class 'numpy.ma.core.MaskedArray'>

    """
    if isinstance(a, MaskedArray):
        if dtype is None or (dtype == a.dtype):
            return a
        return masked_array(a, dtype=dtype, copy=False, keep_mask=True, subok=True)


def _pickle_warn(method):
    warnings.warn(f"np.ma.{method} is deprecated, use pickle.{method} instead",
      DeprecationWarning,
      stacklevel=3)


def fromfile(file, dtype=float, count=-1, sep=''):
    raise NotImplementedError('fromfile() not yet implemented for a MaskedArray.')


def fromflex(fxarray):
    """
    Build a masked array from a suitable flexible-type array.

    The input array has to have a data-type with ``_data`` and ``_mask``
    fields. This type of array is output by `MaskedArray.toflex`.

    Parameters
    ----------
    fxarray : ndarray
        The structured input array, containing ``_data`` and ``_mask``
        fields. If present, other fields are discarded.

    Returns
    -------
    result : MaskedArray
        The constructed masked array.

    See Also
    --------
    MaskedArray.toflex : Build a flexible-type array from a masked array.

    Examples
    --------
    >>> x = np.ma.array(np.arange(9).reshape(3, 3), mask=[0] + [1, 0] * 4)
    >>> rec = x.toflex()
    >>> rec
    array([[(0, False), (1,  True), (2, False)],
           [(3,  True), (4, False), (5,  True)],
           [(6, False), (7,  True), (8, False)]],
          dtype=[('_data', '<i8'), ('_mask', '?')])
    >>> x2 = np.ma.fromflex(rec)
    >>> x2
    masked_array(
      data=[[0, --, 2],
            [--, 4, --],
            [6, --, 8]],
      mask=[[False,  True, False],
            [ True, False,  True],
            [False,  True, False]],
      fill_value=999999)

    Extra fields can be present in the structured array but are discarded:

    >>> dt = [('_data', '<i4'), ('_mask', '|b1'), ('field3', '<f4')]
    >>> rec2 = np.zeros((2, 2), dtype=dt)
    >>> rec2
    array([[(0, False, 0.), (0, False, 0.)],
           [(0, False, 0.), (0, False, 0.)]],
          dtype=[('_data', '<i4'), ('_mask', '?'), ('field3', '<f4')])
    >>> y = np.ma.fromflex(rec2)
    >>> y
    masked_array(
      data=[[0, 0],
            [0, 0]],
      mask=[[False, False],
            [False, False]],
      fill_value=999999,
      dtype=int32)

    """
    return masked_array((fxarray['_data']), mask=(fxarray['_mask']))


class _convert2ma:
    __doc__ = '\n    Convert functions from numpy to numpy.ma.\n\n    Parameters\n    ----------\n        _methodname : string\n            Name of the method to transform.\n\n    '
    __doc__ = None

    def __init__(self, funcname, params=None):
        self._func = getattr(np, funcname)
        self.__doc__ = self.getdoc()
        self._extras = params or {}

    def getdoc(self):
        """Return the doc of the function (from the doc of the method)."""
        doc = getattr(self._func, '__doc__', None)
        sig = get_object_signature(self._func)
        if doc:
            if sig:
                sig = '%s%s\n' % (self._func.__name__, sig)
            doc = sig + doc
        return doc

    def __call__(self, *args, **params):
        _extras = self._extras
        common_params = set(params).intersection(_extras)
        for p in common_params:
            _extras[p] = params.pop(p)

        result = (self._func.__call__)(*args, **params).view(MaskedArray)
        if 'fill_value' in common_params:
            result.fill_value = _extras.get('fill_value', None)
        if 'hardmask' in common_params:
            result._hardmask = bool(_extras.get('hard_mask', False))
        return result


arange = _convert2ma('arange', params=dict(fill_value=None, hardmask=False))
clip = np.clip
diff = np.diff
empty = _convert2ma('empty', params=dict(fill_value=None, hardmask=False))
empty_like = _convert2ma('empty_like')
frombuffer = _convert2ma('frombuffer')
fromfunction = _convert2ma('fromfunction')
identity = _convert2ma('identity',
  params=dict(fill_value=None, hardmask=False))
indices = np.indices
ones = _convert2ma('ones', params=dict(fill_value=None, hardmask=False))
ones_like = np.ones_like
squeeze = np.squeeze
zeros = _convert2ma('zeros', params=dict(fill_value=None, hardmask=False))
zeros_like = np.zeros_like

def append(a, b, axis=None):
    """Append values to the end of an array.

    .. versionadded:: 1.9.0

    Parameters
    ----------
    a : array_like
        Values are appended to a copy of this array.
    b : array_like
        These values are appended to a copy of `a`.  It must be of the
        correct shape (the same shape as `a`, excluding `axis`).  If `axis`
        is not specified, `b` can be any shape and will be flattened
        before use.
    axis : int, optional
        The axis along which `v` are appended.  If `axis` is not given,
        both `a` and `b` are flattened before use.

    Returns
    -------
    append : MaskedArray
        A copy of `a` with `b` appended to `axis`.  Note that `append`
        does not occur in-place: a new array is allocated and filled.  If
        `axis` is None, the result is a flattened array.

    See Also
    --------
    numpy.append : Equivalent function in the top-level NumPy module.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> a = ma.masked_values([1, 2, 3], 2)
    >>> b = ma.masked_values([[4, 5, 6], [7, 8, 9]], 7)
    >>> ma.append(a, b)
    masked_array(data=[1, --, 3, 4, 5, 6, --, 8, 9],
                 mask=[False,  True, False, False, False, False,  True, False,
                       False],
           fill_value=999999)
    """
    return concatenate([a, b], axis)