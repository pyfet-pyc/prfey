# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\core\defchararray.py
"""
This module contains a set of functions for vectorized string
operations and methods.

.. note::
   The `chararray` class exists for backwards compatibility with
   Numarray, it is not recommended for new development. Starting from numpy
   1.4, if one needs arrays of strings, it is recommended to use arrays of
   `dtype` `object_`, `string_` or `unicode_`, and use the free functions
   in the `numpy.char` module for fast vectorized string operations.

Some methods will only be available if the corresponding string method is
available in your version of Python.

The preferred alias for `defchararray` is `numpy.char`.

"""
from __future__ import division, absolute_import, print_function
import functools, sys
from .numerictypes import string_, unicode_, integer, object_, bool_, character
from .numeric import ndarray, compare_chararrays
from .numeric import array as narray
from numpy.core.multiarray import _vec_string
from numpy.core.overrides import set_module
from numpy.core import overrides
from numpy.compat import asbytes, long
import numpy
__all__ = [
 'equal', 'not_equal', 'greater_equal', 'less_equal',
 'greater', 'less', 'str_len', 'add', 'multiply', 'mod', 'capitalize',
 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs',
 'find', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace',
 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition',
 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit',
 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase',
 'title', 'translate', 'upper', 'zfill', 'isnumeric', 'isdecimal',
 'array', 'asarray']
_globalvar = 0
if sys.version_info[0] >= 3:
    _unicode = str
    _bytes = bytes
else:
    _unicode = unicode
    _bytes = str
_len = len
array_function_dispatch = functools.partial((overrides.array_function_dispatch),
  module='numpy.char')

def _use_unicode(*args):
    """
    Helper function for determining the output type of some string
    operations.

    For an operation on two ndarrays, if at least one is unicode, the
    result should be unicode.
    """
    for x in args:
        if isinstance(x, _unicode) or issubclass(numpy.asarray(x).dtype.type, unicode_):
            return unicode_
        return string_


def _to_string_or_unicode_array(result):
    """
    Helper function to cast a result back into a string or unicode array
    if an object array must be used as an intermediary.
    """
    return numpy.asarray(result.tolist())


def _clean_args(*args):
    """
    Helper function for delegating arguments to Python string
    functions.

    Many of the Python string operations that have optional arguments
    do not use 'None' to indicate a default value.  In these cases,
    we need to remove all None arguments, and those following them.
    """
    newargs = []
    for chk in args:
        if chk is None:
            break
        newargs.append(chk)
    else:
        return newargs


def _get_num_chars(a):
    """
    Helper function that returns the number of characters per field in
    a string or unicode array.  This is to abstract out the fact that
    for a unicode array this is itemsize / 4.
    """
    if issubclass(a.dtype.type, unicode_):
        return a.itemsize // 4
    return a.itemsize


def _binary_op_dispatcher(x1, x2):
    return (
     x1, x2)


@array_function_dispatch(_binary_op_dispatcher)
def equal(x1, x2):
    """
    Return (x1 == x2) element-wise.

    Unlike `numpy.equal`, this comparison is performed by first
    stripping whitespace characters from the end of the string.  This
    behavior is provided for backward-compatibility with numarray.

    Parameters
    ----------
    x1, x2 : array_like of str or unicode
        Input arrays of the same shape.

    Returns
    -------
    out : ndarray or bool
        Output array of bools, or a single bool if x1 and x2 are scalars.

    See Also
    --------
    not_equal, greater_equal, less_equal, greater, less
    """
    return compare_chararrays(x1, x2, '==', True)


@array_function_dispatch(_binary_op_dispatcher)
def not_equal(x1, x2):
    """
    Return (x1 != x2) element-wise.

    Unlike `numpy.not_equal`, this comparison is performed by first
    stripping whitespace characters from the end of the string.  This
    behavior is provided for backward-compatibility with numarray.

    Parameters
    ----------
    x1, x2 : array_like of str or unicode
        Input arrays of the same shape.

    Returns
    -------
    out : ndarray or bool
        Output array of bools, or a single bool if x1 and x2 are scalars.

    See Also
    --------
    equal, greater_equal, less_equal, greater, less
    """
    return compare_chararrays(x1, x2, '!=', True)


@array_function_dispatch(_binary_op_dispatcher)
def greater_equal(x1, x2):
    """
    Return (x1 >= x2) element-wise.

    Unlike `numpy.greater_equal`, this comparison is performed by
    first stripping whitespace characters from the end of the string.
    This behavior is provided for backward-compatibility with
    numarray.

    Parameters
    ----------
    x1, x2 : array_like of str or unicode
        Input arrays of the same shape.

    Returns
    -------
    out : ndarray or bool
        Output array of bools, or a single bool if x1 and x2 are scalars.

    See Also
    --------
    equal, not_equal, less_equal, greater, less
    """
    return compare_chararrays(x1, x2, '>=', True)


@array_function_dispatch(_binary_op_dispatcher)
def less_equal(x1, x2):
    """
    Return (x1 <= x2) element-wise.

    Unlike `numpy.less_equal`, this comparison is performed by first
    stripping whitespace characters from the end of the string.  This
    behavior is provided for backward-compatibility with numarray.

    Parameters
    ----------
    x1, x2 : array_like of str or unicode
        Input arrays of the same shape.

    Returns
    -------
    out : ndarray or bool
        Output array of bools, or a single bool if x1 and x2 are scalars.

    See Also
    --------
    equal, not_equal, greater_equal, greater, less
    """
    return compare_chararrays(x1, x2, '<=', True)


@array_function_dispatch(_binary_op_dispatcher)
def greater(x1, x2):
    """
    Return (x1 > x2) element-wise.

    Unlike `numpy.greater`, this comparison is performed by first
    stripping whitespace characters from the end of the string.  This
    behavior is provided for backward-compatibility with numarray.

    Parameters
    ----------
    x1, x2 : array_like of str or unicode
        Input arrays of the same shape.

    Returns
    -------
    out : ndarray or bool
        Output array of bools, or a single bool if x1 and x2 are scalars.

    See Also
    --------
    equal, not_equal, greater_equal, less_equal, less
    """
    return compare_chararrays(x1, x2, '>', True)


@array_function_dispatch(_binary_op_dispatcher)
def less(x1, x2):
    """
    Return (x1 < x2) element-wise.

    Unlike `numpy.greater`, this comparison is performed by first
    stripping whitespace characters from the end of the string.  This
    behavior is provided for backward-compatibility with numarray.

    Parameters
    ----------
    x1, x2 : array_like of str or unicode
        Input arrays of the same shape.

    Returns
    -------
    out : ndarray or bool
        Output array of bools, or a single bool if x1 and x2 are scalars.

    See Also
    --------
    equal, not_equal, greater_equal, less_equal, greater
    """
    return compare_chararrays(x1, x2, '<', True)


def _unary_op_dispatcher(a):
    return (
     a,)


@array_function_dispatch(_unary_op_dispatcher)
def str_len(a):
    """
    Return len(a) element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    Returns
    -------
    out : ndarray
        Output array of integers

    See also
    --------
    __builtin__.len
    """
    return _vec_string(a, integer, '__len__')


@array_function_dispatch(_binary_op_dispatcher)
def add(x1, x2):
    """
    Return element-wise string concatenation for two arrays of str or unicode.

    Arrays `x1` and `x2` must have the same shape.

    Parameters
    ----------
    x1 : array_like of str or unicode
        Input array.
    x2 : array_like of str or unicode
        Input array.

    Returns
    -------
    add : ndarray
        Output array of `string_` or `unicode_`, depending on input types
        of the same shape as `x1` and `x2`.

    """
    arr1 = numpy.asarray(x1)
    arr2 = numpy.asarray(x2)
    out_size = _get_num_chars(arr1) + _get_num_chars(arr2)
    dtype = _use_unicode(arr1, arr2)
    return _vec_string(arr1, (dtype, out_size), '__add__', (arr2,))


def _multiply_dispatcher(a, i):
    return (
     a,)


@array_function_dispatch(_multiply_dispatcher)
def multiply(a, i):
    """
    Return (a * i), that is string multiple concatenation,
    element-wise.

    Values in `i` of less than 0 are treated as 0 (which yields an
    empty string).

    Parameters
    ----------
    a : array_like of str or unicode

    i : array_like of ints

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input types

    """
    a_arr = numpy.asarray(a)
    i_arr = numpy.asarray(i)
    if not issubclass(i_arr.dtype.type, integer):
        raise ValueError('Can only multiply by integers')
    out_size = _get_num_chars(a_arr) * max(long(i_arr.max()), 0)
    return _vec_string(a_arr, (a_arr.dtype.type, out_size), '__mul__', (i_arr,))


def _mod_dispatcher(a, values):
    return (
     a, values)


@array_function_dispatch(_mod_dispatcher)
def mod(a, values):
    """
    Return (a % i), that is pre-Python 2.6 string formatting
    (iterpolation), element-wise for a pair of array_likes of str
    or unicode.

    Parameters
    ----------
    a : array_like of str or unicode

    values : array_like of values
       These values will be element-wise interpolated into the string.

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input types

    See also
    --------
    str.__mod__

    """
    return _to_string_or_unicode_array(_vec_string(a, object_, '__mod__', (values,)))


@array_function_dispatch(_unary_op_dispatcher)
def capitalize(a):
    """
    Return a copy of `a` with only the first character of each element
    capitalized.

    Calls `str.capitalize` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like of str or unicode
        Input array of strings to capitalize.

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input
        types

    See also
    --------
    str.capitalize

    Examples
    --------
    >>> c = np.array(['a1b2','1b2a','b2a1','2a1b'],'S4'); c
    array(['a1b2', '1b2a', 'b2a1', '2a1b'],
        dtype='|S4')
    >>> np.char.capitalize(c)
    array(['A1b2', '1b2a', 'B2a1', '2a1b'],
        dtype='|S4')

    """
    a_arr = numpy.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'capitalize')


def _center_dispatcher(a, width, fillchar=None):
    return (
     a,)


@array_function_dispatch(_center_dispatcher)
def center(a, width, fillchar=' '):
    """
    Return a copy of `a` with its elements centered in a string of
    length `width`.

    Calls `str.center` element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    width : int
        The length of the resulting strings
    fillchar : str or unicode, optional
        The padding character to use (default is space).

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input
        types

    See also
    --------
    str.center

    """
    a_arr = numpy.asarray(a)
    width_arr = numpy.asarray(width)
    size = long(numpy.max(width_arr.flat))
    if numpy.issubdtype(a_arr.dtype, numpy.string_):
        fillchar = asbytes(fillchar)
    return _vec_string(a_arr, (a_arr.dtype.type, size), 'center', (width_arr, fillchar))


def _count_dispatcher(a, sub, start=None, end=None):
    return (
     a,)


@array_function_dispatch(_count_dispatcher)
def count(a, sub, start=0, end=None):
    """
    Returns an array with the number of non-overlapping occurrences of
    substring `sub` in the range [`start`, `end`].

    Calls `str.count` element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    sub : str or unicode
       The substring to search for.

    start, end : int, optional
       Optional arguments `start` and `end` are interpreted as slice
       notation to specify the range in which to count.

    Returns
    -------
    out : ndarray
        Output array of ints.

    See also
    --------
    str.count

    Examples
    --------
    >>> c = np.array(['aAaAaA', '  aA  ', 'abBABba'])
    >>> c
    array(['aAaAaA', '  aA  ', 'abBABba'], dtype='<U7')
    >>> np.char.count(c, 'A')
    array([3, 1, 1])
    >>> np.char.count(c, 'aA')
    array([3, 1, 0])
    >>> np.char.count(c, 'A', start=1, end=4)
    array([2, 1, 1])
    >>> np.char.count(c, 'A', start=1, end=3)
    array([1, 0, 0])

    """
    return _vec_string(a, integer, 'count', [sub, start] + _clean_args(end))


def _code_dispatcher(a, encoding=None, errors=None):
    return (
     a,)


@array_function_dispatch(_code_dispatcher)
def decode(a, encoding=None, errors=None):
    r"""
    Calls `str.decode` element-wise.

    The set of available codecs comes from the Python standard library,
    and may be extended at runtime.  For more information, see the
    :mod:`codecs` module.

    Parameters
    ----------
    a : array_like of str or unicode

    encoding : str, optional
       The name of an encoding

    errors : str, optional
       Specifies how to handle encoding errors

    Returns
    -------
    out : ndarray

    See also
    --------
    str.decode

    Notes
    -----
    The type of the result will depend on the encoding specified.

    Examples
    --------
    >>> c = np.array(['aAaAaA', '  aA  ', 'abBABba'])
    >>> c
    array(['aAaAaA', '  aA  ', 'abBABba'], dtype='<U7')
    >>> np.char.encode(c, encoding='cp037')
    array(['\x81\xc1\x81\xc1\x81\xc1', '@@\x81\xc1@@',
        '\x81\x82\xc2\xc1\xc2\x82\x81'],
        dtype='|S7')

    """
    return _to_string_or_unicode_array(_vec_string(a, object_, 'decode', _clean_args(encoding, errors)))


@array_function_dispatch(_code_dispatcher)
def encode(a, encoding=None, errors=None):
    """
    Calls `str.encode` element-wise.

    The set of available codecs comes from the Python standard library,
    and may be extended at runtime. For more information, see the codecs
    module.

    Parameters
    ----------
    a : array_like of str or unicode

    encoding : str, optional
       The name of an encoding

    errors : str, optional
       Specifies how to handle encoding errors

    Returns
    -------
    out : ndarray

    See also
    --------
    str.encode

    Notes
    -----
    The type of the result will depend on the encoding specified.

    """
    return _to_string_or_unicode_array(_vec_string(a, object_, 'encode', _clean_args(encoding, errors)))


def _endswith_dispatcher(a, suffix, start=None, end=None):
    return (
     a,)


@array_function_dispatch(_endswith_dispatcher)
def endswith(a, suffix, start=0, end=None):
    """
    Returns a boolean array which is `True` where the string element
    in `a` ends with `suffix`, otherwise `False`.

    Calls `str.endswith` element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    suffix : str

    start, end : int, optional
        With optional `start`, test beginning at that position. With
        optional `end`, stop comparing at that position.

    Returns
    -------
    out : ndarray
        Outputs an array of bools.

    See also
    --------
    str.endswith

    Examples
    --------
    >>> s = np.array(['foo', 'bar'])
    >>> s[0] = 'foo'
    >>> s[1] = 'bar'
    >>> s
    array(['foo', 'bar'], dtype='<U3')
    >>> np.char.endswith(s, 'ar')
    array([False,  True])
    >>> np.char.endswith(s, 'a', start=1, end=2)
    array([False,  True])

    """
    return _vec_string(a, bool_, 'endswith', [suffix, start] + _clean_args(end))


def _expandtabs_dispatcher(a, tabsize=None):
    return (
     a,)


@array_function_dispatch(_expandtabs_dispatcher)
def expandtabs(a, tabsize=8):
    """
    Return a copy of each string element where all tab characters are
    replaced by one or more spaces.

    Calls `str.expandtabs` element-wise.

    Return a copy of each string element where all tab characters are
    replaced by one or more spaces, depending on the current column
    and the given `tabsize`. The column number is reset to zero after
    each newline occurring in the string. This doesn't understand other
    non-printing characters or escape sequences.

    Parameters
    ----------
    a : array_like of str or unicode
        Input array
    tabsize : int, optional
        Replace tabs with `tabsize` number of spaces.  If not given defaults
        to 8 spaces.

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See also
    --------
    str.expandtabs

    """
    return _to_string_or_unicode_array(_vec_string(a, object_, 'expandtabs', (tabsize,)))


@array_function_dispatch(_count_dispatcher)
def find(a, sub, start=0, end=None):
    """
    For each element, return the lowest index in the string where
    substring `sub` is found.

    Calls `str.find` element-wise.

    For each element, return the lowest index in the string where
    substring `sub` is found, such that `sub` is contained in the
    range [`start`, `end`].

    Parameters
    ----------
    a : array_like of str or unicode

    sub : str or unicode

    start, end : int, optional
        Optional arguments `start` and `end` are interpreted as in
        slice notation.

    Returns
    -------
    out : ndarray or int
        Output array of ints.  Returns -1 if `sub` is not found.

    See also
    --------
    str.find

    """
    return _vec_string(a, integer, 'find', [sub, start] + _clean_args(end))


@array_function_dispatch(_count_dispatcher)
def index(a, sub, start=0, end=None):
    """
    Like `find`, but raises `ValueError` when the substring is not found.

    Calls `str.index` element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    sub : str or unicode

    start, end : int, optional

    Returns
    -------
    out : ndarray
        Output array of ints.  Returns -1 if `sub` is not found.

    See also
    --------
    find, str.find

    """
    return _vec_string(a, integer, 'index', [sub, start] + _clean_args(end))


@array_function_dispatch(_unary_op_dispatcher)
def isalnum(a):
    """
    Returns true for each element if all characters in the string are
    alphanumeric and there is at least one character, false otherwise.

    Calls `str.isalnum` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like of str or unicode

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See also
    --------
    str.isalnum
    """
    return _vec_string(a, bool_, 'isalnum')


@array_function_dispatch(_unary_op_dispatcher)
def isalpha(a):
    """
    Returns true for each element if all characters in the string are
    alphabetic and there is at least one character, false otherwise.

    Calls `str.isalpha` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like of str or unicode

    Returns
    -------
    out : ndarray
        Output array of bools

    See also
    --------
    str.isalpha
    """
    return _vec_string(a, bool_, 'isalpha')


@array_function_dispatch(_unary_op_dispatcher)
def isdigit(a):
    """
    Returns true for each element if all characters in the string are
    digits and there is at least one character, false otherwise.

    Calls `str.isdigit` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like of str or unicode

    Returns
    -------
    out : ndarray
        Output array of bools

    See also
    --------
    str.isdigit
    """
    return _vec_string(a, bool_, 'isdigit')


@array_function_dispatch(_unary_op_dispatcher)
def islower(a):
    """
    Returns true for each element if all cased characters in the
    string are lowercase and there is at least one cased character,
    false otherwise.

    Calls `str.islower` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like of str or unicode

    Returns
    -------
    out : ndarray
        Output array of bools

    See also
    --------
    str.islower
    """
    return _vec_string(a, bool_, 'islower')


@array_function_dispatch(_unary_op_dispatcher)
def isspace(a):
    """
    Returns true for each element if there are only whitespace
    characters in the string and there is at least one character,
    false otherwise.

    Calls `str.isspace` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like of str or unicode

    Returns
    -------
    out : ndarray
        Output array of bools

    See also
    --------
    str.isspace
    """
    return _vec_string(a, bool_, 'isspace')


@array_function_dispatch(_unary_op_dispatcher)
def istitle(a):
    """
    Returns true for each element if the element is a titlecased
    string and there is at least one character, false otherwise.

    Call `str.istitle` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like of str or unicode

    Returns
    -------
    out : ndarray
        Output array of bools

    See also
    --------
    str.istitle
    """
    return _vec_string(a, bool_, 'istitle')


@array_function_dispatch(_unary_op_dispatcher)
def isupper(a):
    """
    Returns true for each element if all cased characters in the
    string are uppercase and there is at least one character, false
    otherwise.

    Call `str.isupper` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like of str or unicode

    Returns
    -------
    out : ndarray
        Output array of bools

    See also
    --------
    str.isupper
    """
    return _vec_string(a, bool_, 'isupper')


def _join_dispatcher(sep, seq):
    return (
     sep, seq)


@array_function_dispatch(_join_dispatcher)
def join(sep, seq):
    """
    Return a string which is the concatenation of the strings in the
    sequence `seq`.

    Calls `str.join` element-wise.

    Parameters
    ----------
    sep : array_like of str or unicode
    seq : array_like of str or unicode

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input types

    See also
    --------
    str.join
    """
    return _to_string_or_unicode_array(_vec_string(sep, object_, 'join', (seq,)))


def _just_dispatcher(a, width, fillchar=None):
    return (
     a,)


@array_function_dispatch(_just_dispatcher)
def ljust(a, width, fillchar=' '):
    """
    Return an array with the elements of `a` left-justified in a
    string of length `width`.

    Calls `str.ljust` element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    width : int
        The length of the resulting strings
    fillchar : str or unicode, optional
        The character to use for padding

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See also
    --------
    str.ljust

    """
    a_arr = numpy.asarray(a)
    width_arr = numpy.asarray(width)
    size = long(numpy.max(width_arr.flat))
    if numpy.issubdtype(a_arr.dtype, numpy.string_):
        fillchar = asbytes(fillchar)
    return _vec_string(a_arr, (a_arr.dtype.type, size), 'ljust', (width_arr, fillchar))


@array_function_dispatch(_unary_op_dispatcher)
def lower(a):
    """
    Return an array with the elements converted to lowercase.

    Call `str.lower` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like, {str, unicode}
        Input array.

    Returns
    -------
    out : ndarray, {str, unicode}
        Output array of str or unicode, depending on input type

    See also
    --------
    str.lower

    Examples
    --------
    >>> c = np.array(['A1B C', '1BCA', 'BCA1']); c
    array(['A1B C', '1BCA', 'BCA1'], dtype='<U5')
    >>> np.char.lower(c)
    array(['a1b c', '1bca', 'bca1'], dtype='<U5')

    """
    a_arr = numpy.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'lower')


def _strip_dispatcher(a, chars=None):
    return (
     a,)


@array_function_dispatch(_strip_dispatcher)
def lstrip(a, chars=None):
    """
    For each element in `a`, return a copy with the leading characters
    removed.

    Calls `str.lstrip` element-wise.

    Parameters
    ----------
    a : array-like, {str, unicode}
        Input array.

    chars : {str, unicode}, optional
        The `chars` argument is a string specifying the set of
        characters to be removed. If omitted or None, the `chars`
        argument defaults to removing whitespace. The `chars` argument
        is not a prefix; rather, all combinations of its values are
        stripped.

    Returns
    -------
    out : ndarray, {str, unicode}
        Output array of str or unicode, depending on input type

    See also
    --------
    str.lstrip

    Examples
    --------
    >>> c = np.array(['aAaAaA', '  aA  ', 'abBABba'])
    >>> c
    array(['aAaAaA', '  aA  ', 'abBABba'], dtype='<U7')

    The 'a' variable is unstripped from c[1] because whitespace leading.

    >>> np.char.lstrip(c, 'a')
    array(['AaAaA', '  aA  ', 'bBABba'], dtype='<U7')

    >>> np.char.lstrip(c, 'A') # leaves c unchanged
    array(['aAaAaA', '  aA  ', 'abBABba'], dtype='<U7')
    >>> (np.char.lstrip(c, ' ') == np.char.lstrip(c, '')).all()
    ... # XXX: is this a regression? This used to return True
    ... # np.char.lstrip(c,'') does not modify c at all.
    False
    >>> (np.char.lstrip(c, ' ') == np.char.lstrip(c, None)).all()
    True

    """
    a_arr = numpy.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'lstrip', (chars,))


def _partition_dispatcher(a, sep):
    return (
     a,)


@array_function_dispatch(_partition_dispatcher)
def partition(a, sep):
    """
    Partition each element in `a` around `sep`.

    Calls `str.partition` element-wise.

    For each element in `a`, split the element as the first
    occurrence of `sep`, and return 3 strings containing the part
    before the separator, the separator itself, and the part after
    the separator. If the separator is not found, return 3 strings
    containing the string itself, followed by two empty strings.

    Parameters
    ----------
    a : array_like, {str, unicode}
        Input array
    sep : {str, unicode}
        Separator to split each string element in `a`.

    Returns
    -------
    out : ndarray, {str, unicode}
        Output array of str or unicode, depending on input type.
        The output array will have an extra dimension with 3
        elements per input element.

    See also
    --------
    str.partition

    """
    return _to_string_or_unicode_array(_vec_string(a, object_, 'partition', (sep,)))


def _replace_dispatcher(a, old, new, count=None):
    return (
     a,)


@array_function_dispatch(_replace_dispatcher)
def replace(a, old, new, count=None):
    """
    For each element in `a`, return a copy of the string with all
    occurrences of substring `old` replaced by `new`.

    Calls `str.replace` element-wise.

    Parameters
    ----------
    a : array-like of str or unicode

    old, new : str or unicode

    count : int, optional
        If the optional argument `count` is given, only the first
        `count` occurrences are replaced.

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See also
    --------
    str.replace

    """
    return _to_string_or_unicode_array(_vec_string(a, object_, 'replace', [old, new] + _clean_args(count)))


@array_function_dispatch(_count_dispatcher)
def rfind(a, sub, start=0, end=None):
    """
    For each element in `a`, return the highest index in the string
    where substring `sub` is found, such that `sub` is contained
    within [`start`, `end`].

    Calls `str.rfind` element-wise.

    Parameters
    ----------
    a : array-like of str or unicode

    sub : str or unicode

    start, end : int, optional
        Optional arguments `start` and `end` are interpreted as in
        slice notation.

    Returns
    -------
    out : ndarray
       Output array of ints.  Return -1 on failure.

    See also
    --------
    str.rfind

    """
    return _vec_string(a, integer, 'rfind', [sub, start] + _clean_args(end))


@array_function_dispatch(_count_dispatcher)
def rindex(a, sub, start=0, end=None):
    """
    Like `rfind`, but raises `ValueError` when the substring `sub` is
    not found.

    Calls `str.rindex` element-wise.

    Parameters
    ----------
    a : array-like of str or unicode

    sub : str or unicode

    start, end : int, optional

    Returns
    -------
    out : ndarray
       Output array of ints.

    See also
    --------
    rfind, str.rindex

    """
    return _vec_string(a, integer, 'rindex', [sub, start] + _clean_args(end))


@array_function_dispatch(_just_dispatcher)
def rjust(a, width, fillchar=' '):
    """
    Return an array with the elements of `a` right-justified in a
    string of length `width`.

    Calls `str.rjust` element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    width : int
        The length of the resulting strings
    fillchar : str or unicode, optional
        The character to use for padding

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See also
    --------
    str.rjust

    """
    a_arr = numpy.asarray(a)
    width_arr = numpy.asarray(width)
    size = long(numpy.max(width_arr.flat))
    if numpy.issubdtype(a_arr.dtype, numpy.string_):
        fillchar = asbytes(fillchar)
    return _vec_string(a_arr, (a_arr.dtype.type, size), 'rjust', (width_arr, fillchar))


@array_function_dispatch(_partition_dispatcher)
def rpartition(a, sep):
    """
    Partition (split) each element around the right-most separator.

    Calls `str.rpartition` element-wise.

    For each element in `a`, split the element as the last
    occurrence of `sep`, and return 3 strings containing the part
    before the separator, the separator itself, and the part after
    the separator. If the separator is not found, return 3 strings
    containing the string itself, followed by two empty strings.

    Parameters
    ----------
    a : array_like of str or unicode
        Input array
    sep : str or unicode
        Right-most separator to split each element in array.

    Returns
    -------
    out : ndarray
        Output array of string or unicode, depending on input
        type.  The output array will have an extra dimension with
        3 elements per input element.

    See also
    --------
    str.rpartition

    """
    return _to_string_or_unicode_array(_vec_string(a, object_, 'rpartition', (sep,)))


def _split_dispatcher(a, sep=None, maxsplit=None):
    return (
     a,)


@array_function_dispatch(_split_dispatcher)
def rsplit(a, sep=None, maxsplit=None):
    """
    For each element in `a`, return a list of the words in the
    string, using `sep` as the delimiter string.

    Calls `str.rsplit` element-wise.

    Except for splitting from the right, `rsplit`
    behaves like `split`.

    Parameters
    ----------
    a : array_like of str or unicode

    sep : str or unicode, optional
        If `sep` is not specified or None, any whitespace string
        is a separator.
    maxsplit : int, optional
        If `maxsplit` is given, at most `maxsplit` splits are done,
        the rightmost ones.

    Returns
    -------
    out : ndarray
       Array of list objects

    See also
    --------
    str.rsplit, split

    """
    return _vec_string(a, object_, 'rsplit', [sep] + _clean_args(maxsplit))


def _strip_dispatcher(a, chars=None):
    return (
     a,)


@array_function_dispatch(_strip_dispatcher)
def rstrip(a, chars=None):
    """
    For each element in `a`, return a copy with the trailing
    characters removed.

    Calls `str.rstrip` element-wise.

    Parameters
    ----------
    a : array-like of str or unicode

    chars : str or unicode, optional
       The `chars` argument is a string specifying the set of
       characters to be removed. If omitted or None, the `chars`
       argument defaults to removing whitespace. The `chars` argument
       is not a suffix; rather, all combinations of its values are
       stripped.

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See also
    --------
    str.rstrip

    Examples
    --------
    >>> c = np.array(['aAaAaA', 'abBABba'], dtype='S7'); c
    array(['aAaAaA', 'abBABba'],
        dtype='|S7')
    >>> np.char.rstrip(c, b'a')
    array(['aAaAaA', 'abBABb'],
        dtype='|S7')
    >>> np.char.rstrip(c, b'A')
    array(['aAaAa', 'abBABba'],
        dtype='|S7')

    """
    a_arr = numpy.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'rstrip', (chars,))


@array_function_dispatch(_split_dispatcher)
def split(a, sep=None, maxsplit=None):
    """
    For each element in `a`, return a list of the words in the
    string, using `sep` as the delimiter string.

    Calls `str.split` element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    sep : str or unicode, optional
       If `sep` is not specified or None, any whitespace string is a
       separator.

    maxsplit : int, optional
        If `maxsplit` is given, at most `maxsplit` splits are done.

    Returns
    -------
    out : ndarray
        Array of list objects

    See also
    --------
    str.split, rsplit

    """
    return _vec_string(a, object_, 'split', [sep] + _clean_args(maxsplit))


def _splitlines_dispatcher(a, keepends=None):
    return (
     a,)


@array_function_dispatch(_splitlines_dispatcher)
def splitlines(a, keepends=None):
    """
    For each element in `a`, return a list of the lines in the
    element, breaking at line boundaries.

    Calls `str.splitlines` element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    keepends : bool, optional
        Line breaks are not included in the resulting list unless
        keepends is given and true.

    Returns
    -------
    out : ndarray
        Array of list objects

    See also
    --------
    str.splitlines

    """
    return _vec_string(a, object_, 'splitlines', _clean_args(keepends))


def _startswith_dispatcher(a, prefix, start=None, end=None):
    return (
     a,)


@array_function_dispatch(_startswith_dispatcher)
def startswith(a, prefix, start=0, end=None):
    """
    Returns a boolean array which is `True` where the string element
    in `a` starts with `prefix`, otherwise `False`.

    Calls `str.startswith` element-wise.

    Parameters
    ----------
    a : array_like of str or unicode

    prefix : str

    start, end : int, optional
        With optional `start`, test beginning at that position. With
        optional `end`, stop comparing at that position.

    Returns
    -------
    out : ndarray
        Array of booleans

    See also
    --------
    str.startswith

    """
    return _vec_string(a, bool_, 'startswith', [prefix, start] + _clean_args(end))


@array_function_dispatch(_strip_dispatcher)
def strip(a, chars=None):
    """
    For each element in `a`, return a copy with the leading and
    trailing characters removed.

    Calls `str.strip` element-wise.

    Parameters
    ----------
    a : array-like of str or unicode

    chars : str or unicode, optional
       The `chars` argument is a string specifying the set of
       characters to be removed. If omitted or None, the `chars`
       argument defaults to removing whitespace. The `chars` argument
       is not a prefix or suffix; rather, all combinations of its
       values are stripped.

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See also
    --------
    str.strip

    Examples
    --------
    >>> c = np.array(['aAaAaA', '  aA  ', 'abBABba'])
    >>> c
    array(['aAaAaA', '  aA  ', 'abBABba'], dtype='<U7')
    >>> np.char.strip(c)
    array(['aAaAaA', 'aA', 'abBABba'], dtype='<U7')
    >>> np.char.strip(c, 'a') # 'a' unstripped from c[1] because whitespace leads
    array(['AaAaA', '  aA  ', 'bBABb'], dtype='<U7')
    >>> np.char.strip(c, 'A') # 'A' unstripped from c[1] because (unprinted) ws trails
    array(['aAaAa', '  aA  ', 'abBABba'], dtype='<U7')

    """
    a_arr = numpy.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'strip', _clean_args(chars))


@array_function_dispatch(_unary_op_dispatcher)
def swapcase(a):
    """
    Return element-wise a copy of the string with
    uppercase characters converted to lowercase and vice versa.

    Calls `str.swapcase` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like, {str, unicode}
        Input array.

    Returns
    -------
    out : ndarray, {str, unicode}
        Output array of str or unicode, depending on input type

    See also
    --------
    str.swapcase

    Examples
    --------
    >>> c=np.array(['a1B c','1b Ca','b Ca1','cA1b'],'S5'); c
    array(['a1B c', '1b Ca', 'b Ca1', 'cA1b'],
        dtype='|S5')
    >>> np.char.swapcase(c)
    array(['A1b C', '1B cA', 'B cA1', 'Ca1B'],
        dtype='|S5')

    """
    a_arr = numpy.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'swapcase')


@array_function_dispatch(_unary_op_dispatcher)
def title(a):
    """
    Return element-wise title cased version of string or unicode.

    Title case words start with uppercase characters, all remaining cased
    characters are lowercase.

    Calls `str.title` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like, {str, unicode}
        Input array.

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See also
    --------
    str.title

    Examples
    --------
    >>> c=np.array(['a1b c','1b ca','b ca1','ca1b'],'S5'); c
    array(['a1b c', '1b ca', 'b ca1', 'ca1b'],
        dtype='|S5')
    >>> np.char.title(c)
    array(['A1B C', '1B Ca', 'B Ca1', 'Ca1B'],
        dtype='|S5')

    """
    a_arr = numpy.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'title')


def _translate_dispatcher(a, table, deletechars=None):
    return (
     a,)


@array_function_dispatch(_translate_dispatcher)
def translate(a, table, deletechars=None):
    """
    For each element in `a`, return a copy of the string where all
    characters occurring in the optional argument `deletechars` are
    removed, and the remaining characters have been mapped through the
    given translation table.

    Calls `str.translate` element-wise.

    Parameters
    ----------
    a : array-like of str or unicode

    table : str of length 256

    deletechars : str

    Returns
    -------
    out : ndarray
        Output array of str or unicode, depending on input type

    See also
    --------
    str.translate

    """
    a_arr = numpy.asarray(a)
    if issubclass(a_arr.dtype.type, unicode_):
        return _vec_string(a_arr, a_arr.dtype, 'translate', (table,))
    return _vec_string(a_arr, a_arr.dtype, 'translate', [table] + _clean_args(deletechars))


@array_function_dispatch(_unary_op_dispatcher)
def upper(a):
    """
    Return an array with the elements converted to uppercase.

    Calls `str.upper` element-wise.

    For 8-bit strings, this method is locale-dependent.

    Parameters
    ----------
    a : array_like, {str, unicode}
        Input array.

    Returns
    -------
    out : ndarray, {str, unicode}
        Output array of str or unicode, depending on input type

    See also
    --------
    str.upper

    Examples
    --------
    >>> c = np.array(['a1b c', '1bca', 'bca1']); c
    array(['a1b c', '1bca', 'bca1'], dtype='<U5')
    >>> np.char.upper(c)
    array(['A1B C', '1BCA', 'BCA1'], dtype='<U5')

    """
    a_arr = numpy.asarray(a)
    return _vec_string(a_arr, a_arr.dtype, 'upper')


def _zfill_dispatcher(a, width):
    return (
     a,)


@array_function_dispatch(_zfill_dispatcher)
def zfill(a, width):
    """
    Return the numeric string left-filled with zeros

    Calls `str.zfill` element-wise.

    Parameters
    ----------
    a : array_like, {str, unicode}
        Input array.
    width : int
        Width of string to left-fill elements in `a`.

    Returns
    -------
    out : ndarray, {str, unicode}
        Output array of str or unicode, depending on input type

    See also
    --------
    str.zfill

    """
    a_arr = numpy.asarray(a)
    width_arr = numpy.asarray(width)
    size = long(numpy.max(width_arr.flat))
    return _vec_string(a_arr, (a_arr.dtype.type, size), 'zfill', (width_arr,))


@array_function_dispatch(_unary_op_dispatcher)
def isnumeric(a):
    """
    For each element, return True if there are only numeric
    characters in the element.

    Calls `unicode.isnumeric` element-wise.

    Numeric characters include digit characters, and all characters
    that have the Unicode numeric value property, e.g. ``U+2155,
    VULGAR FRACTION ONE FIFTH``.

    Parameters
    ----------
    a : array_like, unicode
        Input array.

    Returns
    -------
    out : ndarray, bool
        Array of booleans of same shape as `a`.

    See also
    --------
    unicode.isnumeric

    """
    if _use_unicode(a) != unicode_:
        raise TypeError('isnumeric is only available for Unicode strings and arrays')
    return _vec_string(a, bool_, 'isnumeric')


@array_function_dispatch(_unary_op_dispatcher)
def isdecimal(a):
    """
    For each element, return True if there are only decimal
    characters in the element.

    Calls `unicode.isdecimal` element-wise.

    Decimal characters include digit characters, and all characters
    that that can be used to form decimal-radix numbers,
    e.g. ``U+0660, ARABIC-INDIC DIGIT ZERO``.

    Parameters
    ----------
    a : array_like, unicode
        Input array.

    Returns
    -------
    out : ndarray, bool
        Array of booleans identical in shape to `a`.

    See also
    --------
    unicode.isdecimal

    """
    if _use_unicode(a) != unicode_:
        raise TypeError('isnumeric is only available for Unicode strings and arrays')
    return _vec_string(a, bool_, 'isdecimal')


@set_module('numpy')
class chararray(ndarray):
    __doc__ = '\n    chararray(shape, itemsize=1, unicode=False, buffer=None, offset=0,\n              strides=None, order=None)\n\n    Provides a convenient view on arrays of string and unicode values.\n\n    .. note::\n       The `chararray` class exists for backwards compatibility with\n       Numarray, it is not recommended for new development. Starting from numpy\n       1.4, if one needs arrays of strings, it is recommended to use arrays of\n       `dtype` `object_`, `string_` or `unicode_`, and use the free functions\n       in the `numpy.char` module for fast vectorized string operations.\n\n    Versus a regular NumPy array of type `str` or `unicode`, this\n    class adds the following functionality:\n\n      1) values automatically have whitespace removed from the end\n         when indexed\n\n      2) comparison operators automatically remove whitespace from the\n         end when comparing values\n\n      3) vectorized string operations are provided as methods\n         (e.g. `.endswith`) and infix operators (e.g. ``"+", "*", "%"``)\n\n    chararrays should be created using `numpy.char.array` or\n    `numpy.char.asarray`, rather than this constructor directly.\n\n    This constructor creates the array, using `buffer` (with `offset`\n    and `strides`) if it is not ``None``. If `buffer` is ``None``, then\n    constructs a new array with `strides` in "C order", unless both\n    ``len(shape) >= 2`` and ``order=\'F\'``, in which case `strides`\n    is in "Fortran order".\n\n    Methods\n    -------\n    astype\n    argsort\n    copy\n    count\n    decode\n    dump\n    dumps\n    encode\n    endswith\n    expandtabs\n    fill\n    find\n    flatten\n    getfield\n    index\n    isalnum\n    isalpha\n    isdecimal\n    isdigit\n    islower\n    isnumeric\n    isspace\n    istitle\n    isupper\n    item\n    join\n    ljust\n    lower\n    lstrip\n    nonzero\n    put\n    ravel\n    repeat\n    replace\n    reshape\n    resize\n    rfind\n    rindex\n    rjust\n    rsplit\n    rstrip\n    searchsorted\n    setfield\n    setflags\n    sort\n    split\n    splitlines\n    squeeze\n    startswith\n    strip\n    swapaxes\n    swapcase\n    take\n    title\n    tofile\n    tolist\n    tostring\n    translate\n    transpose\n    upper\n    view\n    zfill\n\n    Parameters\n    ----------\n    shape : tuple\n        Shape of the array.\n    itemsize : int, optional\n        Length of each array element, in number of characters. Default is 1.\n    unicode : bool, optional\n        Are the array elements of type unicode (True) or string (False).\n        Default is False.\n    buffer : int, optional\n        Memory address of the start of the array data.  Default is None,\n        in which case a new array is created.\n    offset : int, optional\n        Fixed stride displacement from the beginning of an axis?\n        Default is 0. Needs to be >=0.\n    strides : array_like of ints, optional\n        Strides for the array (see `ndarray.strides` for full description).\n        Default is None.\n    order : {\'C\', \'F\'}, optional\n        The order in which the array data is stored in memory: \'C\' ->\n        "row major" order (the default), \'F\' -> "column major"\n        (Fortran) order.\n\n    Examples\n    --------\n    >>> charar = np.chararray((3, 3))\n    >>> charar[:] = \'a\'\n    >>> charar\n    chararray([[b\'a\', b\'a\', b\'a\'],\n               [b\'a\', b\'a\', b\'a\'],\n               [b\'a\', b\'a\', b\'a\']], dtype=\'|S1\')\n\n    >>> charar = np.chararray(charar.shape, itemsize=5)\n    >>> charar[:] = \'abc\'\n    >>> charar\n    chararray([[b\'abc\', b\'abc\', b\'abc\'],\n               [b\'abc\', b\'abc\', b\'abc\'],\n               [b\'abc\', b\'abc\', b\'abc\']], dtype=\'|S5\')\n\n    '

    def __new__(subtype, shape, itemsize=1, unicode=False, buffer=None, offset=0, strides=None, order='C'):
        global _globalvar
        if unicode:
            dtype = unicode_
        else:
            dtype = string_
        itemsize = long(itemsize)
        if sys.version_info[0] >= 3:
            if isinstance(buffer, _unicode):
                filler = buffer
                buffer = None
            else:
                filler = None
        else:
            _globalvar = 1
            if buffer is None:
                self = ndarray.__new__(subtype, shape, (dtype, itemsize), order=order)
            else:
                self = ndarray.__new__(subtype, shape, (dtype, itemsize), buffer=buffer,
                  offset=offset,
                  strides=strides,
                  order=order)
        if filler is not None:
            self[...] = filler
        _globalvar = 0
        return self

    def __array_finalize__(self, obj):
        if not _globalvar:
            if self.dtype.char not in 'SUbc':
                raise ValueError('Can only create a chararray from string data.')

    def __getitem__(self, obj):
        val = ndarray.__getitem__(self, obj)
        if isinstance(val, character):
            temp = val.rstrip()
            if _len(temp) == 0:
                val = ''
            else:
                val = temp
        return val

    def __eq__(self, other):
        """
        Return (self == other) element-wise.

        See also
        --------
        equal
        """
        return equal(self, other)

    def __ne__(self, other):
        """
        Return (self != other) element-wise.

        See also
        --------
        not_equal
        """
        return not_equal(self, other)

    def __ge__(self, other):
        """
        Return (self >= other) element-wise.

        See also
        --------
        greater_equal
        """
        return greater_equal(self, other)

    def __le__(self, other):
        """
        Return (self <= other) element-wise.

        See also
        --------
        less_equal
        """
        return less_equal(self, other)

    def __gt__(self, other):
        """
        Return (self > other) element-wise.

        See also
        --------
        greater
        """
        return greater(self, other)

    def __lt__(self, other):
        """
        Return (self < other) element-wise.

        See also
        --------
        less
        """
        return less(self, other)

    def __add__(self, other):
        """
        Return (self + other), that is string concatenation,
        element-wise for a pair of array_likes of str or unicode.

        See also
        --------
        add
        """
        return asarray(add(self, other))

    def __radd__(self, other):
        """
        Return (other + self), that is string concatenation,
        element-wise for a pair of array_likes of `string_` or `unicode_`.

        See also
        --------
        add
        """
        return asarray(add(numpy.asarray(other), self))

    def __mul__(self, i):
        """
        Return (self * i), that is string multiple concatenation,
        element-wise.

        See also
        --------
        multiply
        """
        return asarray(multiply(self, i))

    def __rmul__(self, i):
        """
        Return (self * i), that is string multiple concatenation,
        element-wise.

        See also
        --------
        multiply
        """
        return asarray(multiply(self, i))

    def __mod__(self, i):
        """
        Return (self % i), that is pre-Python 2.6 string formatting
        (iterpolation), element-wise for a pair of array_likes of `string_`
        or `unicode_`.

        See also
        --------
        mod
        """
        return asarray(mod(self, i))

    def __rmod__(self, other):
        return NotImplemented

    def argsort(self, axis=-1, kind=None, order=None):
        """
        Return the indices that sort the array lexicographically.

        For full documentation see `numpy.argsort`, for which this method is
        in fact merely a "thin wrapper."

        Examples
        --------
        >>> c = np.array(['a1b c', '1b ca', 'b ca1', 'Ca1b'], 'S5')
        >>> c = c.view(np.chararray); c
        chararray(['a1b c', '1b ca', 'b ca1', 'Ca1b'],
              dtype='|S5')
        >>> c[c.argsort()]
        chararray(['1b ca', 'Ca1b', 'a1b c', 'b ca1'],
              dtype='|S5')

        """
        return self.__array__().argsort(axis, kind, order)

    argsort.__doc__ = ndarray.argsort.__doc__

    def capitalize(self):
        """
        Return a copy of `self` with only the first character of each element
        capitalized.

        See also
        --------
        char.capitalize

        """
        return asarray(capitalize(self))

    def center(self, width, fillchar=' '):
        """
        Return a copy of `self` with its elements centered in a
        string of length `width`.

        See also
        --------
        center
        """
        return asarray(center(self, width, fillchar))

    def count(self, sub, start=0, end=None):
        """
        Returns an array with the number of non-overlapping occurrences of
        substring `sub` in the range [`start`, `end`].

        See also
        --------
        char.count

        """
        return count(self, sub, start, end)

    def decode(self, encoding=None, errors=None):
        """
        Calls `str.decode` element-wise.

        See also
        --------
        char.decode

        """
        return decode(self, encoding, errors)

    def encode(self, encoding=None, errors=None):
        """
        Calls `str.encode` element-wise.

        See also
        --------
        char.encode

        """
        return encode(self, encoding, errors)

    def endswith(self, suffix, start=0, end=None):
        """
        Returns a boolean array which is `True` where the string element
        in `self` ends with `suffix`, otherwise `False`.

        See also
        --------
        char.endswith

        """
        return endswith(self, suffix, start, end)

    def expandtabs(self, tabsize=8):
        """
        Return a copy of each string element where all tab characters are
        replaced by one or more spaces.

        See also
        --------
        char.expandtabs

        """
        return asarray(expandtabs(self, tabsize))

    def find(self, sub, start=0, end=None):
        """
        For each element, return the lowest index in the string where
        substring `sub` is found.

        See also
        --------
        char.find

        """
        return find(self, sub, start, end)

    def index(self, sub, start=0, end=None):
        """
        Like `find`, but raises `ValueError` when the substring is not found.

        See also
        --------
        char.index

        """
        return index(self, sub, start, end)

    def isalnum(self):
        """
        Returns true for each element if all characters in the string
        are alphanumeric and there is at least one character, false
        otherwise.

        See also
        --------
        char.isalnum

        """
        return isalnum(self)

    def isalpha(self):
        """
        Returns true for each element if all characters in the string
        are alphabetic and there is at least one character, false
        otherwise.

        See also
        --------
        char.isalpha

        """
        return isalpha(self)

    def isdigit(self):
        """
        Returns true for each element if all characters in the string are
        digits and there is at least one character, false otherwise.

        See also
        --------
        char.isdigit

        """
        return isdigit(self)

    def islower(self):
        """
        Returns true for each element if all cased characters in the
        string are lowercase and there is at least one cased character,
        false otherwise.

        See also
        --------
        char.islower

        """
        return islower(self)

    def isspace(self):
        """
        Returns true for each element if there are only whitespace
        characters in the string and there is at least one character,
        false otherwise.

        See also
        --------
        char.isspace

        """
        return isspace(self)

    def istitle(self):
        """
        Returns true for each element if the element is a titlecased
        string and there is at least one character, false otherwise.

        See also
        --------
        char.istitle

        """
        return istitle(self)

    def isupper(self):
        """
        Returns true for each element if all cased characters in the
        string are uppercase and there is at least one character, false
        otherwise.

        See also
        --------
        char.isupper

        """
        return isupper(self)

    def join(self, seq):
        """
        Return a string which is the concatenation of the strings in the
        sequence `seq`.

        See also
        --------
        char.join

        """
        return join(self, seq)

    def ljust(self, width, fillchar=' '):
        """
        Return an array with the elements of `self` left-justified in a
        string of length `width`.

        See also
        --------
        char.ljust

        """
        return asarray(ljust(self, width, fillchar))

    def lower(self):
        """
        Return an array with the elements of `self` converted to
        lowercase.

        See also
        --------
        char.lower

        """
        return asarray(lower(self))

    def lstrip(self, chars=None):
        """
        For each element in `self`, return a copy with the leading characters
        removed.

        See also
        --------
        char.lstrip

        """
        return asarray(lstrip(self, chars))

    def partition(self, sep):
        """
        Partition each element in `self` around `sep`.

        See also
        --------
        partition
        """
        return asarray(partition(self, sep))

    def replace(self, old, new, count=None):
        """
        For each element in `self`, return a copy of the string with all
        occurrences of substring `old` replaced by `new`.

        See also
        --------
        char.replace

        """
        return asarray(replace(self, old, new, count))

    def rfind(self, sub, start=0, end=None):
        """
        For each element in `self`, return the highest index in the string
        where substring `sub` is found, such that `sub` is contained
        within [`start`, `end`].

        See also
        --------
        char.rfind

        """
        return rfind(self, sub, start, end)

    def rindex(self, sub, start=0, end=None):
        """
        Like `rfind`, but raises `ValueError` when the substring `sub` is
        not found.

        See also
        --------
        char.rindex

        """
        return rindex(self, sub, start, end)

    def rjust(self, width, fillchar=' '):
        """
        Return an array with the elements of `self`
        right-justified in a string of length `width`.

        See also
        --------
        char.rjust

        """
        return asarray(rjust(self, width, fillchar))

    def rpartition(self, sep):
        """
        Partition each element in `self` around `sep`.

        See also
        --------
        rpartition
        """
        return asarray(rpartition(self, sep))

    def rsplit(self, sep=None, maxsplit=None):
        """
        For each element in `self`, return a list of the words in
        the string, using `sep` as the delimiter string.

        See also
        --------
        char.rsplit

        """
        return rsplit(self, sep, maxsplit)

    def rstrip(self, chars=None):
        """
        For each element in `self`, return a copy with the trailing
        characters removed.

        See also
        --------
        char.rstrip

        """
        return asarray(rstrip(self, chars))

    def split(self, sep=None, maxsplit=None):
        """
        For each element in `self`, return a list of the words in the
        string, using `sep` as the delimiter string.

        See also
        --------
        char.split

        """
        return split(self, sep, maxsplit)

    def splitlines(self, keepends=None):
        """
        For each element in `self`, return a list of the lines in the
        element, breaking at line boundaries.

        See also
        --------
        char.splitlines

        """
        return splitlines(self, keepends)

    def startswith(self, prefix, start=0, end=None):
        """
        Returns a boolean array which is `True` where the string element
        in `self` starts with `prefix`, otherwise `False`.

        See also
        --------
        char.startswith

        """
        return startswith(self, prefix, start, end)

    def strip(self, chars=None):
        """
        For each element in `self`, return a copy with the leading and
        trailing characters removed.

        See also
        --------
        char.strip

        """
        return asarray(strip(self, chars))

    def swapcase(self):
        """
        For each element in `self`, return a copy of the string with
        uppercase characters converted to lowercase and vice versa.

        See also
        --------
        char.swapcase

        """
        return asarray(swapcase(self))

    def title(self):
        """
        For each element in `self`, return a titlecased version of the
        string: words start with uppercase characters, all remaining cased
        characters are lowercase.

        See also
        --------
        char.title

        """
        return asarray(title(self))

    def translate(self, table, deletechars=None):
        """
        For each element in `self`, return a copy of the string where
        all characters occurring in the optional argument
        `deletechars` are removed, and the remaining characters have
        been mapped through the given translation table.

        See also
        --------
        char.translate

        """
        return asarray(translate(self, table, deletechars))

    def upper(self):
        """
        Return an array with the elements of `self` converted to
        uppercase.

        See also
        --------
        char.upper

        """
        return asarray(upper(self))

    def zfill(self, width):
        """
        Return the numeric string left-filled with zeros in a string of
        length `width`.

        See also
        --------
        char.zfill

        """
        return asarray(zfill(self, width))

    def isnumeric(self):
        """
        For each element in `self`, return True if there are only
        numeric characters in the element.

        See also
        --------
        char.isnumeric

        """
        return isnumeric(self)

    def isdecimal(self):
        """
        For each element in `self`, return True if there are only
        decimal characters in the element.

        See also
        --------
        char.isdecimal

        """
        return isdecimal(self)


def array--- This code section failed: ---

 L.2680         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'obj'
                4  LOAD_GLOBAL              _bytes
                6  LOAD_GLOBAL              _unicode
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE   132  'to 132'

 L.2681        14  LOAD_FAST                'unicode'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    42  'to 42'

 L.2682        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'obj'
               26  LOAD_GLOBAL              _unicode
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    38  'to 38'

 L.2683        32  LOAD_CONST               True
               34  STORE_FAST               'unicode'
               36  JUMP_FORWARD         42  'to 42'
             38_0  COME_FROM            30  '30'

 L.2685        38  LOAD_CONST               False
               40  STORE_FAST               'unicode'
             42_0  COME_FROM            36  '36'
             42_1  COME_FROM            20  '20'

 L.2687        42  LOAD_FAST                'itemsize'
               44  LOAD_CONST               None
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L.2688        50  LOAD_GLOBAL              _len
               52  LOAD_FAST                'obj'
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'itemsize'
             58_0  COME_FROM            48  '48'

 L.2689        58  LOAD_GLOBAL              _len
               60  LOAD_FAST                'obj'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_FAST                'itemsize'
               66  BINARY_FLOOR_DIVIDE
               68  STORE_FAST               'shape'

 L.2691        70  LOAD_FAST                'unicode'
               72  POP_JUMP_IF_FALSE   106  'to 106'

 L.2692        74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                maxunicode
               78  LOAD_CONST               65535
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE    96  'to 96'

 L.2702        84  LOAD_FAST                'obj'
               86  LOAD_METHOD              encode
               88  LOAD_STR                 'utf_32'
               90  CALL_METHOD_1         1  ''
               92  STORE_FAST               'obj'
               94  JUMP_ABSOLUTE       114  'to 114'
             96_0  COME_FROM            82  '82'

 L.2704        96  LOAD_GLOBAL              _unicode
               98  LOAD_FAST                'obj'
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'obj'
              104  JUMP_FORWARD        114  'to 114'
            106_0  COME_FROM            72  '72'

 L.2708       106  LOAD_GLOBAL              _bytes
              108  LOAD_FAST                'obj'
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'obj'
            114_0  COME_FROM           104  '104'

 L.2710       114  LOAD_GLOBAL              chararray
              116  LOAD_FAST                'shape'
              118  LOAD_FAST                'itemsize'
              120  LOAD_FAST                'unicode'

 L.2711       122  LOAD_FAST                'obj'

 L.2711       124  LOAD_FAST                'order'

 L.2710       126  LOAD_CONST               ('itemsize', 'unicode', 'buffer', 'order')
              128  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              130  RETURN_VALUE     
            132_0  COME_FROM            12  '12'

 L.2713       132  LOAD_GLOBAL              isinstance
              134  LOAD_FAST                'obj'
              136  LOAD_GLOBAL              list
              138  LOAD_GLOBAL              tuple
              140  BUILD_TUPLE_2         2 
              142  CALL_FUNCTION_2       2  ''
              144  POP_JUMP_IF_FALSE   156  'to 156'

 L.2714       146  LOAD_GLOBAL              numpy
              148  LOAD_METHOD              asarray
              150  LOAD_FAST                'obj'
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               'obj'
            156_0  COME_FROM           144  '144'

 L.2716       156  LOAD_GLOBAL              isinstance
              158  LOAD_FAST                'obj'
              160  LOAD_GLOBAL              ndarray
              162  CALL_FUNCTION_2       2  ''
          164_166  POP_JUMP_IF_FALSE   392  'to 392'
              168  LOAD_GLOBAL              issubclass
              170  LOAD_FAST                'obj'
              172  LOAD_ATTR                dtype
              174  LOAD_ATTR                type
              176  LOAD_GLOBAL              character
              178  CALL_FUNCTION_2       2  ''
          180_182  POP_JUMP_IF_FALSE   392  'to 392'

 L.2719       184  LOAD_GLOBAL              isinstance
              186  LOAD_FAST                'obj'
              188  LOAD_GLOBAL              chararray
              190  CALL_FUNCTION_2       2  ''
              192  POP_JUMP_IF_TRUE    204  'to 204'

 L.2720       194  LOAD_FAST                'obj'
              196  LOAD_METHOD              view
              198  LOAD_GLOBAL              chararray
              200  CALL_METHOD_1         1  ''
              202  STORE_FAST               'obj'
            204_0  COME_FROM           192  '192'

 L.2722       204  LOAD_FAST                'itemsize'
              206  LOAD_CONST               None
              208  COMPARE_OP               is
              210  POP_JUMP_IF_FALSE   240  'to 240'

 L.2723       212  LOAD_FAST                'obj'
              214  LOAD_ATTR                itemsize
              216  STORE_FAST               'itemsize'

 L.2727       218  LOAD_GLOBAL              issubclass
              220  LOAD_FAST                'obj'
              222  LOAD_ATTR                dtype
              224  LOAD_ATTR                type
              226  LOAD_GLOBAL              unicode_
              228  CALL_FUNCTION_2       2  ''
              230  POP_JUMP_IF_FALSE   240  'to 240'

 L.2728       232  LOAD_FAST                'itemsize'
              234  LOAD_CONST               4
              236  INPLACE_FLOOR_DIVIDE
              238  STORE_FAST               'itemsize'
            240_0  COME_FROM           230  '230'
            240_1  COME_FROM           210  '210'

 L.2730       240  LOAD_FAST                'unicode'
              242  LOAD_CONST               None
              244  COMPARE_OP               is
          246_248  POP_JUMP_IF_FALSE   276  'to 276'

 L.2731       250  LOAD_GLOBAL              issubclass
              252  LOAD_FAST                'obj'
              254  LOAD_ATTR                dtype
              256  LOAD_ATTR                type
              258  LOAD_GLOBAL              unicode_
              260  CALL_FUNCTION_2       2  ''
          262_264  POP_JUMP_IF_FALSE   272  'to 272'

 L.2732       266  LOAD_CONST               True
              268  STORE_FAST               'unicode'
              270  JUMP_FORWARD        276  'to 276'
            272_0  COME_FROM           262  '262'

 L.2734       272  LOAD_CONST               False
              274  STORE_FAST               'unicode'
            276_0  COME_FROM           270  '270'
            276_1  COME_FROM           246  '246'

 L.2736       276  LOAD_FAST                'unicode'
          278_280  POP_JUMP_IF_FALSE   288  'to 288'

 L.2737       282  LOAD_GLOBAL              unicode_
              284  STORE_FAST               'dtype'
              286  JUMP_FORWARD        292  'to 292'
            288_0  COME_FROM           278  '278'

 L.2739       288  LOAD_GLOBAL              string_
              290  STORE_FAST               'dtype'
            292_0  COME_FROM           286  '286'

 L.2741       292  LOAD_FAST                'order'
              294  LOAD_CONST               None
              296  COMPARE_OP               is-not
          298_300  POP_JUMP_IF_FALSE   316  'to 316'

 L.2742       302  LOAD_GLOBAL              numpy
              304  LOAD_ATTR                asarray
              306  LOAD_FAST                'obj'
              308  LOAD_FAST                'order'
              310  LOAD_CONST               ('order',)
              312  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              314  STORE_FAST               'obj'
            316_0  COME_FROM           298  '298'

 L.2743       316  LOAD_FAST                'copy'
          318_320  POP_JUMP_IF_TRUE    370  'to 370'

 L.2744       322  LOAD_FAST                'itemsize'
              324  LOAD_FAST                'obj'
              326  LOAD_ATTR                itemsize
              328  COMPARE_OP               !=

 L.2743   330_332  POP_JUMP_IF_TRUE    370  'to 370'

 L.2745       334  LOAD_FAST                'unicode'

 L.2743   336_338  POP_JUMP_IF_TRUE    352  'to 352'

 L.2745       340  LOAD_GLOBAL              isinstance
              342  LOAD_FAST                'obj'
              344  LOAD_GLOBAL              unicode_
              346  CALL_FUNCTION_2       2  ''

 L.2743   348_350  POP_JUMP_IF_TRUE    370  'to 370'
            352_0  COME_FROM           336  '336'

 L.2746       352  LOAD_FAST                'unicode'

 L.2743   354_356  POP_JUMP_IF_FALSE   388  'to 388'

 L.2746       358  LOAD_GLOBAL              isinstance
              360  LOAD_FAST                'obj'
              362  LOAD_GLOBAL              string_
              364  CALL_FUNCTION_2       2  ''

 L.2743   366_368  POP_JUMP_IF_FALSE   388  'to 388'
            370_0  COME_FROM           348  '348'
            370_1  COME_FROM           330  '330'
            370_2  COME_FROM           318  '318'

 L.2747       370  LOAD_FAST                'obj'
              372  LOAD_METHOD              astype
              374  LOAD_FAST                'dtype'
              376  LOAD_GLOBAL              long
              378  LOAD_FAST                'itemsize'
              380  CALL_FUNCTION_1       1  ''
              382  BUILD_TUPLE_2         2 
              384  CALL_METHOD_1         1  ''
              386  STORE_FAST               'obj'
            388_0  COME_FROM           366  '366'
            388_1  COME_FROM           354  '354'

 L.2748       388  LOAD_FAST                'obj'
              390  RETURN_VALUE     
            392_0  COME_FROM           180  '180'
            392_1  COME_FROM           164  '164'

 L.2750       392  LOAD_GLOBAL              isinstance
              394  LOAD_FAST                'obj'
              396  LOAD_GLOBAL              ndarray
              398  CALL_FUNCTION_2       2  ''
          400_402  POP_JUMP_IF_FALSE   438  'to 438'
              404  LOAD_GLOBAL              issubclass
              406  LOAD_FAST                'obj'
              408  LOAD_ATTR                dtype
              410  LOAD_ATTR                type
              412  LOAD_GLOBAL              object
              414  CALL_FUNCTION_2       2  ''
          416_418  POP_JUMP_IF_FALSE   438  'to 438'

 L.2751       420  LOAD_FAST                'itemsize'
              422  LOAD_CONST               None
              424  COMPARE_OP               is
          426_428  POP_JUMP_IF_FALSE   438  'to 438'

 L.2755       430  LOAD_FAST                'obj'
              432  LOAD_METHOD              tolist
              434  CALL_METHOD_0         0  ''
              436  STORE_FAST               'obj'
            438_0  COME_FROM           426  '426'
            438_1  COME_FROM           416  '416'
            438_2  COME_FROM           400  '400'

 L.2758       438  LOAD_FAST                'unicode'
          440_442  POP_JUMP_IF_FALSE   450  'to 450'

 L.2759       444  LOAD_GLOBAL              unicode_
              446  STORE_FAST               'dtype'
              448  JUMP_FORWARD        454  'to 454'
            450_0  COME_FROM           440  '440'

 L.2761       450  LOAD_GLOBAL              string_
              452  STORE_FAST               'dtype'
            454_0  COME_FROM           448  '448'

 L.2763       454  LOAD_FAST                'itemsize'
              456  LOAD_CONST               None
              458  COMPARE_OP               is
          460_462  POP_JUMP_IF_FALSE   482  'to 482'

 L.2764       464  LOAD_GLOBAL              narray
              466  LOAD_FAST                'obj'
              468  LOAD_FAST                'dtype'
              470  LOAD_FAST                'order'
              472  LOAD_CONST               True
              474  LOAD_CONST               ('dtype', 'order', 'subok')
              476  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              478  STORE_FAST               'val'
              480  JUMP_FORWARD        502  'to 502'
            482_0  COME_FROM           460  '460'

 L.2766       482  LOAD_GLOBAL              narray
              484  LOAD_FAST                'obj'
              486  LOAD_FAST                'dtype'
              488  LOAD_FAST                'itemsize'
              490  BUILD_TUPLE_2         2 
              492  LOAD_FAST                'order'
              494  LOAD_CONST               True
              496  LOAD_CONST               ('dtype', 'order', 'subok')
              498  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              500  STORE_FAST               'val'
            502_0  COME_FROM           480  '480'

 L.2767       502  LOAD_FAST                'val'
              504  LOAD_METHOD              view
              506  LOAD_GLOBAL              chararray
              508  CALL_METHOD_1         1  ''
              510  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 510


def asarray(obj, itemsize=None, unicode=None, order=None):
    """
    Convert the input to a `chararray`, copying the data only if
    necessary.

    Versus a regular NumPy array of type `str` or `unicode`, this
    class adds the following functionality:

      1) values automatically have whitespace removed from the end
         when indexed

      2) comparison operators automatically remove whitespace from the
         end when comparing values

      3) vectorized string operations are provided as methods
         (e.g. `str.endswith`) and infix operators (e.g. ``+``, ``*``,``%``)

    Parameters
    ----------
    obj : array of str or unicode-like

    itemsize : int, optional
        `itemsize` is the number of characters per scalar in the
        resulting array.  If `itemsize` is None, and `obj` is an
        object array or a Python list, the `itemsize` will be
        automatically determined.  If `itemsize` is provided and `obj`
        is of type str or unicode, then the `obj` string will be
        chunked into `itemsize` pieces.

    unicode : bool, optional
        When true, the resulting `chararray` can contain Unicode
        characters, when false only 8-bit characters.  If unicode is
        None and `obj` is one of the following:

          - a `chararray`,
          - an ndarray of type `str` or 'unicode`
          - a Python str or unicode object,

        then the unicode setting of the output array will be
        automatically determined.

    order : {'C', 'F'}, optional
        Specify the order of the array.  If order is 'C' (default), then the
        array will be in C-contiguous order (last-index varies the
        fastest).  If order is 'F', then the returned array
        will be in Fortran-contiguous order (first-index varies the
        fastest).
    """
    return array(obj, itemsize, copy=False, unicode=unicode,
      order=order)