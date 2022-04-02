# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\core\arrayprint.py
"""Array printing function

$Id: arrayprint.py,v 1.9 2005/09/13 13:58:44 teoliphant Exp $

"""
__all__ = [
 'array2string', 'array_str', 'array_repr', 'set_string_function',
 'set_printoptions', 'get_printoptions', 'printoptions',
 'format_float_positional', 'format_float_scientific']
__docformat__ = 'restructuredtext'
import functools, numbers
try:
    from _thread import get_ident
except ImportError:
    from _dummy_thread import get_ident
else:
    import numpy as np
    from . import numerictypes as _nt
    from .umath import absolute, isinf, isfinite, isnat
    from . import multiarray
    from .multiarray import array, dragon4_positional, dragon4_scientific, datetime_as_string, datetime_data, ndarray, set_legacy_print_mode
    from .fromnumeric import any
    from .numeric import concatenate, asarray, errstate
    from .numerictypes import longlong, intc, int_, float_, complex_, bool_, flexible
    from .overrides import array_function_dispatch, set_module
    import warnings, contextlib
    _format_options = {'edgeitems':3, 
     'threshold':1000, 
     'floatmode':'maxprec', 
     'precision':8, 
     'suppress':False, 
     'linewidth':75, 
     'nanstr':'nan', 
     'infstr':'inf', 
     'sign':'-', 
     'formatter':None, 
     'legacy':False}

    def _make_options_dict(precision=None, threshold=None, edgeitems=None, linewidth=None, suppress=None, nanstr=None, infstr=None, sign=None, formatter=None, floatmode=None, legacy=None):
        """ make a dictionary out of the non-None arguments, plus sanity checks """
        options = {v:k for k, v in locals().items() if v is not None if v is not None}
        if suppress is not None:
            options['suppress'] = bool(suppress)
        modes = ['fixed', 'unique', 'maxprec', 'maxprec_equal']
        if floatmode not in modes + [None]:
            raise ValueError('floatmode option must be one of ' + ', '.join(('"{}"'.format(m) for m in modes)))
        if sign not in (None, '-', '+', ' '):
            raise ValueError("sign option must be one of ' ', '+', or '-'")
        if legacy not in (None, False, '1.13'):
            warnings.warn("legacy printing option can currently only be '1.13' or `False`", stacklevel=3)
        if threshold is not None:
            if not isinstance(threshold, numbers.Number):
                raise TypeError('threshold must be numeric')
            if np.isnan(threshold):
                raise ValueError('threshold must be non-NAN, try sys.maxsize for untruncated representation')
        return options


    @set_module('numpy')
    def set_printoptions(precision=None, threshold=None, edgeitems=None, linewidth=None, suppress=None, nanstr=None, infstr=None, formatter=None, sign=None, floatmode=None, *, legacy=None):
        """
    Set printing options.

    These options determine the way floating point numbers, arrays and
    other NumPy objects are displayed.

    Parameters
    ----------
    precision : int or None, optional
        Number of digits of precision for floating point output (default 8).
        May be None if `floatmode` is not `fixed`, to print as many digits as
        necessary to uniquely specify the value.
    threshold : int, optional
        Total number of array elements which trigger summarization
        rather than full repr (default 1000).
        To always use the full repr without summarization, pass `sys.maxsize`.
    edgeitems : int, optional
        Number of array items in summary at beginning and end of
        each dimension (default 3).
    linewidth : int, optional
        The number of characters per line for the purpose of inserting
        line breaks (default 75).
    suppress : bool, optional
        If True, always print floating point numbers using fixed point
        notation, in which case numbers equal to zero in the current precision
        will print as zero.  If False, then scientific notation is used when
        absolute value of the smallest number is < 1e-4 or the ratio of the
        maximum absolute value to the minimum is > 1e3. The default is False.
    nanstr : str, optional
        String representation of floating point not-a-number (default nan).
    infstr : str, optional
        String representation of floating point infinity (default inf).
    sign : string, either '-', '+', or ' ', optional
        Controls printing of the sign of floating-point types. If '+', always
        print the sign of positive values. If ' ', always prints a space
        (whitespace character) in the sign position of positive values.  If
        '-', omit the sign character of positive values. (default '-')
    formatter : dict of callables, optional
        If not None, the keys should indicate the type(s) that the respective
        formatting function applies to.  Callables should return a string.
        Types that are not specified (by their corresponding keys) are handled
        by the default formatters.  Individual types for which a formatter
        can be set are:

        - 'bool'
        - 'int'
        - 'timedelta' : a `numpy.timedelta64`
        - 'datetime' : a `numpy.datetime64`
        - 'float'
        - 'longfloat' : 128-bit floats
        - 'complexfloat'
        - 'longcomplexfloat' : composed of two 128-bit floats
        - 'numpystr' : types `numpy.string_` and `numpy.unicode_`
        - 'object' : `np.object_` arrays
        - 'str' : all other strings

        Other keys that can be used to set a group of types at once are:

        - 'all' : sets all types
        - 'int_kind' : sets 'int'
        - 'float_kind' : sets 'float' and 'longfloat'
        - 'complex_kind' : sets 'complexfloat' and 'longcomplexfloat'
        - 'str_kind' : sets 'str' and 'numpystr'
    floatmode : str, optional
        Controls the interpretation of the `precision` option for
        floating-point types. Can take the following values
        (default maxprec_equal):

        * 'fixed': Always print exactly `precision` fractional digits,
                even if this would print more or fewer digits than
                necessary to specify the value uniquely.
        * 'unique': Print the minimum number of fractional digits necessary
                to represent each value uniquely. Different elements may
                have a different number of digits. The value of the
                `precision` option is ignored.
        * 'maxprec': Print at most `precision` fractional digits, but if
                an element can be uniquely represented with fewer digits
                only print it with that many.
        * 'maxprec_equal': Print at most `precision` fractional digits,
                but if every element in the array can be uniquely
                represented with an equal number of fewer digits, use that
                many digits for all elements.
    legacy : string or `False`, optional
        If set to the string `'1.13'` enables 1.13 legacy printing mode. This
        approximates numpy 1.13 print output by including a space in the sign
        position of floats and different behavior for 0d arrays. If set to
        `False`, disables legacy mode. Unrecognized strings will be ignored
        with a warning for forward compatibility.

        .. versionadded:: 1.14.0

    See Also
    --------
    get_printoptions, printoptions, set_string_function, array2string

    Notes
    -----
    `formatter` is always reset with a call to `set_printoptions`.

    Use `printoptions` as a context manager to set the values temporarily.

    Examples
    --------
    Floating point precision can be set:

    >>> np.set_printoptions(precision=4)
    >>> np.array([1.123456789])
    [1.1235]

    Long arrays can be summarised:

    >>> np.set_printoptions(threshold=5)
    >>> np.arange(10)
    array([0, 1, 2, ..., 7, 8, 9])

    Small results can be suppressed:

    >>> eps = np.finfo(float).eps
    >>> x = np.arange(4.)
    >>> x**2 - (x + eps)**2
    array([-4.9304e-32, -4.4409e-16,  0.0000e+00,  0.0000e+00])
    >>> np.set_printoptions(suppress=True)
    >>> x**2 - (x + eps)**2
    array([-0., -0.,  0.,  0.])

    A custom formatter can be used to display array elements as desired:

    >>> np.set_printoptions(formatter={'all':lambda x: 'int: '+str(-x)})
    >>> x = np.arange(3)
    >>> x
    array([int: 0, int: -1, int: -2])
    >>> np.set_printoptions()  # formatter gets reset
    >>> x
    array([0, 1, 2])

    To put back the default options, you can use:

    >>> np.set_printoptions(edgeitems=3, infstr='inf',
    ... linewidth=75, nanstr='nan', precision=8,
    ... suppress=False, threshold=1000, formatter=None)

    Also to temporarily override options, use `printoptions` as a context manager:

    >>> with np.printoptions(precision=2, suppress=True, threshold=5):
    ...     np.linspace(0, 10, 10)
    array([ 0.  ,  1.11,  2.22, ...,  7.78,  8.89, 10.  ])

    """
        opt = _make_options_dict(precision, threshold, edgeitems, linewidth, suppress, nanstr, infstr, sign, formatter, floatmode, legacy)
        opt['formatter'] = formatter
        _format_options.update(opt)
        if _format_options['legacy'] == '1.13':
            set_legacy_print_mode(113)
            _format_options['sign'] = '-'
        else:
            if _format_options['legacy'] is False:
                set_legacy_print_mode(0)


    @set_module('numpy')
    def get_printoptions():
        """
    Return the current print options.

    Returns
    -------
    print_opts : dict
        Dictionary of current print options with keys

          - precision : int
          - threshold : int
          - edgeitems : int
          - linewidth : int
          - suppress : bool
          - nanstr : str
          - infstr : str
          - formatter : dict of callables
          - sign : str

        For a full description of these options, see `set_printoptions`.

    See Also
    --------
    set_printoptions, printoptions, set_string_function

    """
        return _format_options.copy()


    @set_module('numpy')
    @contextlib.contextmanager
    def printoptions(*args, **kwargs):
        """Context manager for setting print options.

    Set print options for the scope of the `with` block, and restore the old
    options at the end. See `set_printoptions` for the full description of
    available options.

    Examples
    --------

    >>> from numpy.testing import assert_equal
    >>> with np.printoptions(precision=2):
    ...     np.array([2.0]) / 3
    array([0.67])

    The `as`-clause of the `with`-statement gives the current print options:

    >>> with np.printoptions(precision=2) as opts:
    ...      assert_equal(opts, np.get_printoptions())

    See Also
    --------
    set_printoptions, get_printoptions

    """
        opts = np.get_printoptions()
        try:
            (np.set_printoptions)(*args, **kwargs)
            (yield np.get_printoptions())
        finally:
            (np.set_printoptions)(**opts)


    def _leading_trailing(a, edgeitems, index=()):
        """
    Keep only the N-D corners (leading and trailing edges) of an array.

    Should be passed a base-class ndarray, since it makes no guarantees about
    preserving subclasses.
    """
        axis = len(index)
        if axis == a.ndim:
            return a[index]
        if a.shape[axis] > 2 * edgeitems:
            return concatenate((
             _leading_trailing(a, edgeitems, index + np.index_exp[:edgeitems]),
             _leading_trailing(a, edgeitems, index + np.index_exp[-edgeitems:])),
              axis=axis)
        return _leading_trailing(a, edgeitems, index + np.index_exp[:])


    def _object_format(o):
        """ Object arrays containing lists should be printed unambiguously """
        if type(o) is list:
            fmt = 'list({!r})'
        else:
            fmt = '{!r}'
        return fmt.format(o)


    def repr_format(x):
        return repr(x)


    def str_format(x):
        return str(x)


    def _get_formatdict(data, *, precision, floatmode, suppress, sign, legacy, formatter, **kwargs):
        formatdict = {'bool':lambda : BoolFormat(data), 
         'int':lambda : IntegerFormat(data), 
         'float':lambda : FloatingFormat(data,
           precision, floatmode, suppress, sign, legacy=legacy), 
         'longfloat':lambda : FloatingFormat(data,
           precision, floatmode, suppress, sign, legacy=legacy), 
         'complexfloat':lambda : ComplexFloatingFormat(data,
           precision, floatmode, suppress, sign, legacy=legacy), 
         'longcomplexfloat':lambda : ComplexFloatingFormat(data,
           precision, floatmode, suppress, sign, legacy=legacy), 
         'datetime':lambda : DatetimeFormat(data, legacy=legacy), 
         'timedelta':lambda : TimedeltaFormat(data), 
         'object':lambda : _object_format, 
         'void':lambda : str_format, 
         'numpystr':lambda : repr_format, 
         'str':lambda : str}

        def indirect(x):
            return lambda : x

        if formatter is not None:
            fkeys = [k for k in formatter.keys() if formatter[k] is not None]
            if 'all' in fkeys:
                for key in formatdict.keys():
                    formatdict[key] = indirect(formatter['all'])

            if 'int_kind' in fkeys:
                for key in ('int', ):
                    formatdict[key] = indirect(formatter['int_kind'])

            if 'float_kind' in fkeys:
                for key in ('float', 'longfloat'):
                    formatdict[key] = indirect(formatter['float_kind'])

            if 'complex_kind' in fkeys:
                for key in ('complexfloat', 'longcomplexfloat'):
                    formatdict[key] = indirect(formatter['complex_kind'])

            elif 'str_kind' in fkeys:
                for key in ('numpystr', 'str'):
                    formatdict[key] = indirect(formatter['str_kind'])

            else:
                for key in formatdict.keys():
                    if key in fkeys:
                        formatdict[key] = indirect(formatter[key])

        return formatdict


    def _get_format_function(data, **options):
        """
    find the right formatting function for the dtype_
    """
        dtype_ = data.dtype
        dtypeobj = dtype_.type
        formatdict = _get_formatdict(data, **options)
        if issubclass(dtypeobj, _nt.bool_):
            return formatdict['bool']()
        if issubclass(dtypeobj, _nt.integer):
            if issubclass(dtypeobj, _nt.timedelta64):
                return formatdict['timedelta']()
            return formatdict['int']()
        else:
            if issubclass(dtypeobj, _nt.floating):
                if issubclass(dtypeobj, _nt.longfloat):
                    return formatdict['longfloat']()
                return formatdict['float']()
            else:
                if issubclass(dtypeobj, _nt.complexfloating):
                    if issubclass(dtypeobj, _nt.clongfloat):
                        return formatdict['longcomplexfloat']()
                    return formatdict['complexfloat']()
                else:
                    if issubclass(dtypeobj, (_nt.unicode_, _nt.string_)):
                        return formatdict['numpystr']()
                        if issubclass(dtypeobj, _nt.datetime64):
                            return formatdict['datetime']()
                        if issubclass(dtypeobj, _nt.object_):
                            return formatdict['object']()
                        if issubclass(dtypeobj, _nt.void):
                            if dtype_.names is not None:
                                return (StructuredVoidFormat.from_data)(data, **options)
                            return formatdict['void']()
                    else:
                        return formatdict['numpystr']()


    def _recursive_guard(fillvalue='...'):
        """
    Like the python 3.2 reprlib.recursive_repr, but forwards *args and **kwargs

    Decorates a function such that if it calls itself with the same first
    argument, it returns `fillvalue` instead of recursing.

    Largely copied from reprlib.recursive_repr
    """

        def decorating_function(f):
            repr_running = set()

            @functools.wraps(f)
            def wrapper(self, *args, **kwargs):
                key = (id(self), get_ident())
                if key in repr_running:
                    return fillvalue
                repr_running.add(key)
                try:
                    return f(self, *args, **kwargs)
                finally:
                    repr_running.discard(key)

            return wrapper

        return decorating_function


    @_recursive_guard()
    def _array2string(a, options, separator=' ', prefix=''):
        data = asarray(a)
        if a.shape == ():
            a = data
        elif a.size > options['threshold']:
            summary_insert = '...'
            data = _leading_trailing(data, options['edgeitems'])
        else:
            summary_insert = ''
        format_function = _get_format_function(data, **options)
        next_line_prefix = ' '
        next_line_prefix += ' ' * len(prefix)
        lst = _formatArray(a, format_function, options['linewidth'], next_line_prefix, separator, options['edgeitems'], summary_insert, options['legacy'])
        return lst


    def _array2string_dispatcher(a, max_line_width=None, precision=None, suppress_small=None, separator=None, prefix=None, style=None, formatter=None, threshold=None, edgeitems=None, sign=None, floatmode=None, suffix=None, *, legacy=None):
        return (
         a,)


    @array_function_dispatch(_array2string_dispatcher, module='numpy')
    def array2string(a, max_line_width=None, precision=None, suppress_small=None, separator=' ', prefix='', style=np._NoValue, formatter=None, threshold=None, edgeitems=None, sign=None, floatmode=None, suffix='', *, legacy=None):
        """
    Return a string representation of an array.

    Parameters
    ----------
    a : array_like
        Input array.
    max_line_width : int, optional
        Inserts newlines if text is longer than `max_line_width`.
        Defaults to ``numpy.get_printoptions()['linewidth']``.
    precision : int or None, optional
        Floating point precision.
        Defaults to ``numpy.get_printoptions()['precision']``.
    suppress_small : bool, optional
        Represent numbers "very close" to zero as zero; default is False.
        Very close is defined by precision: if the precision is 8, e.g.,
        numbers smaller (in absolute value) than 5e-9 are represented as
        zero.
        Defaults to ``numpy.get_printoptions()['suppress']``.
    separator : str, optional
        Inserted between elements.
    prefix : str, optional
    suffix: str, optional
        The length of the prefix and suffix strings are used to respectively
        align and wrap the output. An array is typically printed as::

          prefix + array2string(a) + suffix

        The output is left-padded by the length of the prefix string, and
        wrapping is forced at the column ``max_line_width - len(suffix)``.
        It should be noted that the content of prefix and suffix strings are
        not included in the output.
    style : _NoValue, optional
        Has no effect, do not use.

        .. deprecated:: 1.14.0
    formatter : dict of callables, optional
        If not None, the keys should indicate the type(s) that the respective
        formatting function applies to.  Callables should return a string.
        Types that are not specified (by their corresponding keys) are handled
        by the default formatters.  Individual types for which a formatter
        can be set are:

        - 'bool'
        - 'int'
        - 'timedelta' : a `numpy.timedelta64`
        - 'datetime' : a `numpy.datetime64`
        - 'float'
        - 'longfloat' : 128-bit floats
        - 'complexfloat'
        - 'longcomplexfloat' : composed of two 128-bit floats
        - 'void' : type `numpy.void`
        - 'numpystr' : types `numpy.string_` and `numpy.unicode_`
        - 'str' : all other strings

        Other keys that can be used to set a group of types at once are:

        - 'all' : sets all types
        - 'int_kind' : sets 'int'
        - 'float_kind' : sets 'float' and 'longfloat'
        - 'complex_kind' : sets 'complexfloat' and 'longcomplexfloat'
        - 'str_kind' : sets 'str' and 'numpystr'
    threshold : int, optional
        Total number of array elements which trigger summarization
        rather than full repr.
        Defaults to ``numpy.get_printoptions()['threshold']``.
    edgeitems : int, optional
        Number of array items in summary at beginning and end of
        each dimension.
        Defaults to ``numpy.get_printoptions()['edgeitems']``.
    sign : string, either '-', '+', or ' ', optional
        Controls printing of the sign of floating-point types. If '+', always
        print the sign of positive values. If ' ', always prints a space
        (whitespace character) in the sign position of positive values.  If
        '-', omit the sign character of positive values.
        Defaults to ``numpy.get_printoptions()['sign']``.
    floatmode : str, optional
        Controls the interpretation of the `precision` option for
        floating-point types.
        Defaults to ``numpy.get_printoptions()['floatmode']``.
        Can take the following values:

        - 'fixed': Always print exactly `precision` fractional digits,
          even if this would print more or fewer digits than
          necessary to specify the value uniquely.
        - 'unique': Print the minimum number of fractional digits necessary
          to represent each value uniquely. Different elements may
          have a different number of digits.  The value of the
          `precision` option is ignored.
        - 'maxprec': Print at most `precision` fractional digits, but if
          an element can be uniquely represented with fewer digits
          only print it with that many.
        - 'maxprec_equal': Print at most `precision` fractional digits,
          but if every element in the array can be uniquely
          represented with an equal number of fewer digits, use that
          many digits for all elements.
    legacy : string or `False`, optional
        If set to the string `'1.13'` enables 1.13 legacy printing mode. This
        approximates numpy 1.13 print output by including a space in the sign
        position of floats and different behavior for 0d arrays. If set to
        `False`, disables legacy mode. Unrecognized strings will be ignored
        with a warning for forward compatibility.

        .. versionadded:: 1.14.0

    Returns
    -------
    array_str : str
        String representation of the array.

    Raises
    ------
    TypeError
        if a callable in `formatter` does not return a string.

    See Also
    --------
    array_str, array_repr, set_printoptions, get_printoptions

    Notes
    -----
    If a formatter is specified for a certain type, the `precision` keyword is
    ignored for that type.

    This is a very flexible function; `array_repr` and `array_str` are using
    `array2string` internally so keywords with the same name should work
    identically in all three functions.

    Examples
    --------
    >>> x = np.array([1e-16,1,2,3])
    >>> np.array2string(x, precision=2, separator=',',
    ...                       suppress_small=True)
    '[0.,1.,2.,3.]'

    >>> x  = np.arange(3.)
    >>> np.array2string(x, formatter={'float_kind':lambda x: "%.2f" % x})
    '[0.00 1.00 2.00]'

    >>> x  = np.arange(3)
    >>> np.array2string(x, formatter={'int':lambda x: hex(x)})
    '[0x0 0x1 0x2]'

    """
        overrides = _make_options_dict(precision, threshold, edgeitems, max_line_width, suppress_small, None, None, sign, formatter, floatmode, legacy)
        options = _format_options.copy()
        options.update(overrides)
        if options['legacy'] == '1.13':
            if style is np._NoValue:
                style = repr
            if a.shape == () and a.dtype.names is None:
                return style(a.item())
        elif style is not np._NoValue:
            warnings.warn("'style' argument is deprecated and no longer functional except in 1.13 'legacy' mode", DeprecationWarning,
              stacklevel=3)
        if options['legacy'] != '1.13':
            options['linewidth'] -= len(suffix)
        if a.size == 0:
            return '[]'
        return _array2string(a, options, separator, prefix)


    def _extendLine(s, line, word, line_width, next_line_prefix, legacy):
        needs_wrap = len(line) + len(word) > line_width
        if legacy != '1.13':
            s
            if len(line) <= len(next_line_prefix):
                needs_wrap = False
        if needs_wrap:
            s += line.rstrip() + '\n'
            line = next_line_prefix
        line += word
        return (s, line)


    def _formatArray(a, format_function, line_width, next_line_prefix, separator, edge_items, summary_insert, legacy):
        """formatArray is designed for two modes of operation:

    1. Full output

    2. Summarized output

    """

        def recurser(index, hanging_indent, curr_width):
            axis = len(index)
            axes_left = a.ndim - axis
            if axes_left == 0:
                return format_function(a[index])
            else:
                next_hanging_indent = hanging_indent + ' '
                if legacy == '1.13':
                    next_width = curr_width
                else:
                    next_width = curr_width - len(']')
                a_len = a.shape[axis]
                show_summary = summary_insert and 2 * edge_items < a_len
                if show_summary:
                    leading_items = edge_items
                    trailing_items = edge_items
                else:
                    leading_items = 0
                    trailing_items = a_len
                s = ''
                if axes_left == 1:
                    if legacy == '1.13':
                        elem_width = curr_width - len(separator.rstrip())
                    else:
                        elem_width = curr_width - max(len(separator.rstrip()), len(']'))
                    line = hanging_indent
                    for i in range(leading_items):
                        word = recurser(index + (i,), next_hanging_indent, next_width)
                        s, line = _extendLine(s, line, word, elem_width, hanging_indent, legacy)
                        line += separator
                    else:
                        if show_summary:
                            s, line = _extendLine(s, line, summary_insert, elem_width, hanging_indent, legacy)
                            if legacy == '1.13':
                                line += ', '
                            else:
                                line += separator
                        for i in range(trailing_items, 1, -1):
                            word = recurser(index + (-i,), next_hanging_indent, next_width)
                            s, line = _extendLine(s, line, word, elem_width, hanging_indent, legacy)
                            line += separator
                        else:
                            if legacy == '1.13':
                                elem_width = curr_width
                            word = recurser(index + (-1, ), next_hanging_indent, next_width)
                            s, line = _extendLine(s, line, word, elem_width, hanging_indent, legacy)
                            s += line

                else:
                    s = ''
                line_sep = separator.rstrip() + '\n' * (axes_left - 1)
                for i in range(leading_items):
                    nested = recurser(index + (i,), next_hanging_indent, next_width)
                    s += hanging_indent + nested + line_sep
                else:
                    if show_summary:
                        if legacy == '1.13':
                            s += hanging_indent + summary_insert + ', \n'
                        else:
                            s += hanging_indent + summary_insert + line_sep
                    for i in range(trailing_items, 1, -1):
                        nested = recurser(index + (-i,), next_hanging_indent, next_width)
                        s += hanging_indent + nested + line_sep
                    else:
                        nested = recurser(index + (-1, ), next_hanging_indent, next_width)
                        s += hanging_indent + nested

            s = '[' + s[len(hanging_indent):] + ']'
            return s

        try:
            return recurser(index=(), hanging_indent=next_line_prefix,
              curr_width=line_width)
        finally:
            recurser = None


    def _none_or_positive_arg(x, name):
        if x is None:
            return -1
        if x < 0:
            raise ValueError('{} must be >= 0'.format(name))
        return x


    class FloatingFormat:
        __doc__ = ' Formatter for subtypes of np.floating '

        def __init__(self, data, precision, floatmode, suppress_small, sign=False, *, legacy=None):
            if isinstance(sign, bool):
                sign = '+' if sign else '-'
            else:
                self._legacy = legacy
                if self._legacy == '1.13':
                    if data.shape != ():
                        if sign == '-':
                            sign = ' '
                self.floatmode = floatmode
                if floatmode == 'unique':
                    self.precision = None
                else:
                    self.precision = precision
            self.precision = _none_or_positive_arg(self.precision, 'precision')
            self.suppress_small = suppress_small
            self.sign = sign
            self.exp_format = False
            self.large_exponent = False
            self.fillFormat(data)

        def fillFormat--- This code section failed: ---

 L. 865         0  LOAD_FAST                'data'
                2  LOAD_GLOBAL              isfinite
                4  LOAD_FAST                'data'
                6  CALL_FUNCTION_1       1  ''
                8  BINARY_SUBSCR    
               10  STORE_FAST               'finite_vals'

 L. 868        12  LOAD_GLOBAL              absolute
               14  LOAD_FAST                'finite_vals'
               16  LOAD_FAST                'finite_vals'
               18  LOAD_CONST               0
               20  COMPARE_OP               !=
               22  BINARY_SUBSCR    
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'abs_non_zero'

 L. 869        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'abs_non_zero'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               0
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE   122  'to 122'

 L. 870        40  LOAD_GLOBAL              np
               42  LOAD_METHOD              max
               44  LOAD_FAST                'abs_non_zero'
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'max_val'

 L. 871        50  LOAD_GLOBAL              np
               52  LOAD_METHOD              min
               54  LOAD_FAST                'abs_non_zero'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'min_val'

 L. 872        60  LOAD_GLOBAL              errstate
               62  LOAD_STR                 'ignore'
               64  LOAD_CONST               ('over',)
               66  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               68  SETUP_WITH          116  'to 116'
               70  POP_TOP          

 L. 873        72  LOAD_FAST                'max_val'
               74  LOAD_CONST               100000000.0
               76  COMPARE_OP               >=
               78  POP_JUMP_IF_TRUE    106  'to 106'
               80  LOAD_DEREF               'self'
               82  LOAD_ATTR                suppress_small
               84  POP_JUMP_IF_TRUE    112  'to 112'

 L. 874        86  LOAD_FAST                'min_val'
               88  LOAD_CONST               0.0001
               90  COMPARE_OP               <

 L. 873        92  POP_JUMP_IF_TRUE    106  'to 106'

 L. 874        94  LOAD_FAST                'max_val'
               96  LOAD_FAST                'min_val'
               98  BINARY_TRUE_DIVIDE
              100  LOAD_CONST               1000.0
              102  COMPARE_OP               >

 L. 873       104  POP_JUMP_IF_FALSE   112  'to 112'
            106_0  COME_FROM            92  '92'
            106_1  COME_FROM            78  '78'

 L. 875       106  LOAD_CONST               True
              108  LOAD_DEREF               'self'
              110  STORE_ATTR               exp_format
            112_0  COME_FROM           104  '104'
            112_1  COME_FROM            84  '84'
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM_WITH       68  '68'
              116  WITH_CLEANUP_START
              118  WITH_CLEANUP_FINISH
              120  END_FINALLY      
            122_0  COME_FROM            38  '38'

 L. 878       122  LOAD_GLOBAL              len
              124  LOAD_FAST                'finite_vals'
              126  CALL_FUNCTION_1       1  ''
              128  LOAD_CONST               0
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   168  'to 168'

 L. 879       134  LOAD_CONST               0
              136  LOAD_DEREF               'self'
              138  STORE_ATTR               pad_left

 L. 880       140  LOAD_CONST               0
              142  LOAD_DEREF               'self'
              144  STORE_ATTR               pad_right

 L. 881       146  LOAD_STR                 '.'
              148  LOAD_DEREF               'self'
              150  STORE_ATTR               trim

 L. 882       152  LOAD_CONST               -1
              154  LOAD_DEREF               'self'
              156  STORE_ATTR               exp_size

 L. 883       158  LOAD_CONST               True
              160  LOAD_DEREF               'self'
              162  STORE_ATTR               unique
          164_166  JUMP_FORWARD        598  'to 598'
            168_0  COME_FROM           132  '132'

 L. 884       168  LOAD_DEREF               'self'
              170  LOAD_ATTR                exp_format
          172_174  POP_JUMP_IF_FALSE   396  'to 396'

 L. 885       176  LOAD_CONST               ('.', True)
              178  UNPACK_SEQUENCE_2     2 
              180  STORE_DEREF              'trim'
              182  STORE_DEREF              'unique'

 L. 886       184  LOAD_DEREF               'self'
              186  LOAD_ATTR                floatmode
              188  LOAD_STR                 'fixed'
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_TRUE    204  'to 204'
              194  LOAD_DEREF               'self'
              196  LOAD_ATTR                _legacy
              198  LOAD_STR                 '1.13'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   212  'to 212'
            204_0  COME_FROM           192  '192'

 L. 887       204  LOAD_CONST               ('k', False)
              206  UNPACK_SEQUENCE_2     2 
              208  STORE_DEREF              'trim'
              210  STORE_DEREF              'unique'
            212_0  COME_FROM           202  '202'

 L. 888       212  LOAD_CLOSURE             'self'
              214  LOAD_CLOSURE             'trim'
              216  LOAD_CLOSURE             'unique'
              218  BUILD_TUPLE_3         3 
              220  LOAD_GENEXPR             '<code_object <genexpr>>'
              222  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              224  MAKE_FUNCTION_8          'closure'

 L. 890       226  LOAD_FAST                'finite_vals'

 L. 888       228  GET_ITER         
              230  CALL_FUNCTION_1       1  ''
              232  STORE_FAST               'strs'

 L. 891       234  LOAD_GLOBAL              zip
              236  LOAD_GENEXPR             '<code_object <genexpr>>'
              238  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              240  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              242  LOAD_FAST                'strs'
              244  GET_ITER         
              246  CALL_FUNCTION_1       1  ''
              248  CALL_FUNCTION_EX      0  'positional arguments only'
              250  UNPACK_SEQUENCE_3     3 
              252  STORE_FAST               'frac_strs'
              254  STORE_FAST               '_'
              256  STORE_FAST               'exp_strs'

 L. 892       258  LOAD_GLOBAL              zip
              260  LOAD_GENEXPR             '<code_object <genexpr>>'
              262  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              264  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              266  LOAD_FAST                'frac_strs'
              268  GET_ITER         
              270  CALL_FUNCTION_1       1  ''
              272  CALL_FUNCTION_EX      0  'positional arguments only'
              274  UNPACK_SEQUENCE_2     2 
              276  STORE_FAST               'int_part'
              278  STORE_FAST               'frac_part'

 L. 893       280  LOAD_GLOBAL              max
              282  LOAD_GENEXPR             '<code_object <genexpr>>'
              284  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              286  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              288  LOAD_FAST                'exp_strs'
              290  GET_ITER         
              292  CALL_FUNCTION_1       1  ''
              294  CALL_FUNCTION_1       1  ''
              296  LOAD_CONST               1
              298  BINARY_SUBTRACT  
              300  LOAD_DEREF               'self'
              302  STORE_ATTR               exp_size

 L. 895       304  LOAD_STR                 'k'
              306  LOAD_DEREF               'self'
              308  STORE_ATTR               trim

 L. 896       310  LOAD_GLOBAL              max
              312  LOAD_GENEXPR             '<code_object <genexpr>>'
              314  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              316  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              318  LOAD_FAST                'frac_part'
              320  GET_ITER         
              322  CALL_FUNCTION_1       1  ''
              324  CALL_FUNCTION_1       1  ''
              326  LOAD_DEREF               'self'
              328  STORE_ATTR               precision

 L. 899       330  LOAD_DEREF               'self'
              332  LOAD_ATTR                _legacy
              334  LOAD_STR                 '1.13'
              336  COMPARE_OP               ==
          338_340  POP_JUMP_IF_FALSE   350  'to 350'

 L. 900       342  LOAD_CONST               3
              344  LOAD_DEREF               'self'
              346  STORE_ATTR               pad_left
              348  JUMP_FORWARD        370  'to 370'
            350_0  COME_FROM           338  '338'

 L. 903       350  LOAD_GLOBAL              max
              352  LOAD_GENEXPR             '<code_object <genexpr>>'
              354  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              356  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              358  LOAD_FAST                'int_part'
              360  GET_ITER         
              362  CALL_FUNCTION_1       1  ''
              364  CALL_FUNCTION_1       1  ''
              366  LOAD_DEREF               'self'
              368  STORE_ATTR               pad_left
            370_0  COME_FROM           348  '348'

 L. 905       370  LOAD_DEREF               'self'
              372  LOAD_ATTR                exp_size
              374  LOAD_CONST               2
              376  BINARY_ADD       
              378  LOAD_DEREF               'self'
              380  LOAD_ATTR                precision
              382  BINARY_ADD       
              384  LOAD_DEREF               'self'
              386  STORE_ATTR               pad_right

 L. 907       388  LOAD_CONST               False
              390  LOAD_DEREF               'self'
              392  STORE_ATTR               unique
              394  JUMP_FORWARD        598  'to 598'
            396_0  COME_FROM           172  '172'

 L. 910       396  LOAD_CONST               ('.', True)
              398  UNPACK_SEQUENCE_2     2 
              400  STORE_DEREF              'trim'
              402  STORE_DEREF              'unique'

 L. 911       404  LOAD_DEREF               'self'
              406  LOAD_ATTR                floatmode
              408  LOAD_STR                 'fixed'
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   424  'to 424'

 L. 912       416  LOAD_CONST               ('k', False)
              418  UNPACK_SEQUENCE_2     2 
              420  STORE_DEREF              'trim'
              422  STORE_DEREF              'unique'
            424_0  COME_FROM           412  '412'

 L. 913       424  LOAD_CLOSURE             'self'
              426  LOAD_CLOSURE             'trim'
              428  LOAD_CLOSURE             'unique'
              430  BUILD_TUPLE_3         3 
              432  LOAD_GENEXPR             '<code_object <genexpr>>'
              434  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              436  MAKE_FUNCTION_8          'closure'

 L. 917       438  LOAD_FAST                'finite_vals'

 L. 913       440  GET_ITER         
              442  CALL_FUNCTION_1       1  ''
              444  STORE_FAST               'strs'

 L. 918       446  LOAD_GLOBAL              zip
              448  LOAD_GENEXPR             '<code_object <genexpr>>'
              450  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              452  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              454  LOAD_FAST                'strs'
              456  GET_ITER         
              458  CALL_FUNCTION_1       1  ''
              460  CALL_FUNCTION_EX      0  'positional arguments only'
              462  UNPACK_SEQUENCE_2     2 
              464  STORE_FAST               'int_part'
              466  STORE_FAST               'frac_part'

 L. 919       468  LOAD_DEREF               'self'
              470  LOAD_ATTR                _legacy
              472  LOAD_STR                 '1.13'
              474  COMPARE_OP               ==
          476_478  POP_JUMP_IF_FALSE   506  'to 506'

 L. 920       480  LOAD_CONST               1
              482  LOAD_GLOBAL              max
              484  LOAD_GENEXPR             '<code_object <genexpr>>'
              486  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              488  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              490  LOAD_FAST                'int_part'
              492  GET_ITER         
              494  CALL_FUNCTION_1       1  ''
              496  CALL_FUNCTION_1       1  ''
              498  BINARY_ADD       
              500  LOAD_DEREF               'self'
              502  STORE_ATTR               pad_left
              504  JUMP_FORWARD        526  'to 526'
            506_0  COME_FROM           476  '476'

 L. 922       506  LOAD_GLOBAL              max
              508  LOAD_GENEXPR             '<code_object <genexpr>>'
              510  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              512  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              514  LOAD_FAST                'int_part'
              516  GET_ITER         
              518  CALL_FUNCTION_1       1  ''
              520  CALL_FUNCTION_1       1  ''
              522  LOAD_DEREF               'self'
              524  STORE_ATTR               pad_left
            526_0  COME_FROM           504  '504'

 L. 923       526  LOAD_GLOBAL              max
              528  LOAD_GENEXPR             '<code_object <genexpr>>'
              530  LOAD_STR                 'FloatingFormat.fillFormat.<locals>.<genexpr>'
              532  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              534  LOAD_FAST                'frac_part'
              536  GET_ITER         
              538  CALL_FUNCTION_1       1  ''
              540  CALL_FUNCTION_1       1  ''
              542  LOAD_DEREF               'self'
              544  STORE_ATTR               pad_right

 L. 924       546  LOAD_CONST               -1
              548  LOAD_DEREF               'self'
              550  STORE_ATTR               exp_size

 L. 926       552  LOAD_DEREF               'self'
              554  LOAD_ATTR                floatmode
              556  LOAD_CONST               ('fixed', 'maxprec_equal')
              558  COMPARE_OP               in
          560_562  POP_JUMP_IF_FALSE   586  'to 586'

 L. 927       564  LOAD_DEREF               'self'
              566  LOAD_ATTR                pad_right
              568  LOAD_DEREF               'self'
              570  STORE_ATTR               precision

 L. 928       572  LOAD_CONST               False
              574  LOAD_DEREF               'self'
              576  STORE_ATTR               unique

 L. 929       578  LOAD_STR                 'k'
              580  LOAD_DEREF               'self'
              582  STORE_ATTR               trim
              584  JUMP_FORWARD        598  'to 598'
            586_0  COME_FROM           560  '560'

 L. 931       586  LOAD_CONST               True
              588  LOAD_DEREF               'self'
              590  STORE_ATTR               unique

 L. 932       592  LOAD_STR                 '.'
              594  LOAD_DEREF               'self'
              596  STORE_ATTR               trim
            598_0  COME_FROM           584  '584'
            598_1  COME_FROM           394  '394'
            598_2  COME_FROM           164  '164'

 L. 934       598  LOAD_DEREF               'self'
              600  LOAD_ATTR                _legacy
              602  LOAD_STR                 '1.13'
              604  COMPARE_OP               !=
          606_608  POP_JUMP_IF_FALSE   652  'to 652'

 L. 936       610  LOAD_DEREF               'self'
              612  LOAD_ATTR                sign
              614  LOAD_STR                 ' '
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_FALSE   652  'to 652'
              622  LOAD_GLOBAL              any
              624  LOAD_GLOBAL              np
              626  LOAD_METHOD              signbit
              628  LOAD_FAST                'finite_vals'
              630  CALL_METHOD_1         1  ''
              632  CALL_FUNCTION_1       1  ''
          634_636  POP_JUMP_IF_TRUE    652  'to 652'

 L. 937       638  LOAD_DEREF               'self'
              640  DUP_TOP          
              642  LOAD_ATTR                pad_left
              644  LOAD_CONST               1
              646  INPLACE_ADD      
              648  ROT_TWO          
              650  STORE_ATTR               pad_left
            652_0  COME_FROM           634  '634'
            652_1  COME_FROM           618  '618'
            652_2  COME_FROM           606  '606'

 L. 940       652  LOAD_FAST                'data'
              654  LOAD_ATTR                size
              656  LOAD_FAST                'finite_vals'
              658  LOAD_ATTR                size
              660  COMPARE_OP               !=
          662_664  POP_JUMP_IF_FALSE   760  'to 760'

 L. 941       666  LOAD_DEREF               'self'
              668  LOAD_ATTR                sign
              670  LOAD_STR                 '-'
              672  COMPARE_OP               !=
          674_676  JUMP_IF_TRUE_OR_POP   696  'to 696'
              678  LOAD_GLOBAL              any
              680  LOAD_FAST                'data'
              682  LOAD_GLOBAL              isinf
              684  LOAD_FAST                'data'
              686  CALL_FUNCTION_1       1  ''
              688  BINARY_SUBSCR    
              690  LOAD_CONST               0
              692  COMPARE_OP               <
              694  CALL_FUNCTION_1       1  ''
            696_0  COME_FROM           674  '674'
              696  STORE_FAST               'neginf'

 L. 942       698  LOAD_GLOBAL              len
              700  LOAD_GLOBAL              _format_options
              702  LOAD_STR                 'nanstr'
              704  BINARY_SUBSCR    
              706  CALL_FUNCTION_1       1  ''
              708  STORE_FAST               'nanlen'

 L. 943       710  LOAD_GLOBAL              len
              712  LOAD_GLOBAL              _format_options
              714  LOAD_STR                 'infstr'
              716  BINARY_SUBSCR    
              718  CALL_FUNCTION_1       1  ''
              720  LOAD_FAST                'neginf'
              722  BINARY_ADD       
              724  STORE_FAST               'inflen'

 L. 944       726  LOAD_DEREF               'self'
              728  LOAD_ATTR                pad_right
              730  LOAD_CONST               1
              732  BINARY_ADD       
              734  STORE_FAST               'offset'

 L. 945       736  LOAD_GLOBAL              max
              738  LOAD_DEREF               'self'
              740  LOAD_ATTR                pad_left
              742  LOAD_FAST                'nanlen'
              744  LOAD_FAST                'offset'
              746  BINARY_SUBTRACT  
              748  LOAD_FAST                'inflen'
              750  LOAD_FAST                'offset'
              752  BINARY_SUBTRACT  
              754  CALL_FUNCTION_3       3  ''
              756  LOAD_DEREF               'self'
              758  STORE_ATTR               pad_left
            760_0  COME_FROM           662  '662'

Parse error at or near `BEGIN_FINALLY' instruction at offset 114

        def __call__--- This code section failed: ---

 L. 948         0  LOAD_GLOBAL              np
                2  LOAD_METHOD              isfinite
                4  LOAD_FAST                'x'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE    156  'to 156'

 L. 949        10  LOAD_GLOBAL              errstate
               12  LOAD_STR                 'ignore'
               14  LOAD_CONST               ('invalid',)
               16  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               18  SETUP_WITH          150  'to 150'
               20  POP_TOP          

 L. 950        22  LOAD_GLOBAL              np
               24  LOAD_METHOD              isnan
               26  LOAD_FAST                'x'
               28  CALL_METHOD_1         1  ''
               30  POP_JUMP_IF_FALSE    64  'to 64'

 L. 951        32  LOAD_FAST                'self'
               34  LOAD_ATTR                sign
               36  LOAD_STR                 '+'
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    46  'to 46'
               42  LOAD_STR                 '+'
               44  JUMP_FORWARD         48  'to 48'
             46_0  COME_FROM            40  '40'
               46  LOAD_STR                 ''
             48_0  COME_FROM            44  '44'
               48  STORE_FAST               'sign'

 L. 952        50  LOAD_FAST                'sign'
               52  LOAD_GLOBAL              _format_options
               54  LOAD_STR                 'nanstr'
               56  BINARY_SUBSCR    
               58  BINARY_ADD       
               60  STORE_FAST               'ret'
               62  JUMP_FORWARD        106  'to 106'
             64_0  COME_FROM            30  '30'

 L. 954        64  LOAD_FAST                'x'
               66  LOAD_CONST               0
               68  COMPARE_OP               <
               70  POP_JUMP_IF_FALSE    76  'to 76'
               72  LOAD_STR                 '-'
               74  JUMP_FORWARD         92  'to 92'
             76_0  COME_FROM            70  '70'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                sign
               80  LOAD_STR                 '+'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    90  'to 90'
               86  LOAD_STR                 '+'
               88  JUMP_FORWARD         92  'to 92'
             90_0  COME_FROM            84  '84'
               90  LOAD_STR                 ''
             92_0  COME_FROM            88  '88'
             92_1  COME_FROM            74  '74'
               92  STORE_FAST               'sign'

 L. 955        94  LOAD_FAST                'sign'
               96  LOAD_GLOBAL              _format_options
               98  LOAD_STR                 'infstr'
              100  BINARY_SUBSCR    
              102  BINARY_ADD       
              104  STORE_FAST               'ret'
            106_0  COME_FROM            62  '62'

 L. 956       106  LOAD_STR                 ' '
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                pad_left
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                pad_right
              116  BINARY_ADD       
              118  LOAD_CONST               1
              120  BINARY_ADD       
              122  LOAD_GLOBAL              len
              124  LOAD_FAST                'ret'
              126  CALL_FUNCTION_1       1  ''
              128  BINARY_SUBTRACT  
              130  BINARY_MULTIPLY  
              132  LOAD_FAST                'ret'
              134  BINARY_ADD       
              136  POP_BLOCK        
              138  ROT_TWO          
              140  BEGIN_FINALLY    
              142  WITH_CLEANUP_START
              144  WITH_CLEANUP_FINISH
              146  POP_FINALLY           0  ''
              148  RETURN_VALUE     
            150_0  COME_FROM_WITH       18  '18'
              150  WITH_CLEANUP_START
              152  WITH_CLEANUP_FINISH
              154  END_FINALLY      
            156_0  COME_FROM             8  '8'

 L. 958       156  LOAD_FAST                'self'
              158  LOAD_ATTR                exp_format
              160  POP_JUMP_IF_FALSE   200  'to 200'

 L. 959       162  LOAD_GLOBAL              dragon4_scientific
              164  LOAD_FAST                'x'

 L. 960       166  LOAD_FAST                'self'
              168  LOAD_ATTR                precision

 L. 961       170  LOAD_FAST                'self'
              172  LOAD_ATTR                unique

 L. 962       174  LOAD_FAST                'self'
              176  LOAD_ATTR                trim

 L. 963       178  LOAD_FAST                'self'
              180  LOAD_ATTR                sign
              182  LOAD_STR                 '+'
              184  COMPARE_OP               ==

 L. 964       186  LOAD_FAST                'self'
              188  LOAD_ATTR                pad_left

 L. 965       190  LOAD_FAST                'self'
              192  LOAD_ATTR                exp_size

 L. 959       194  LOAD_CONST               ('precision', 'unique', 'trim', 'sign', 'pad_left', 'exp_digits')
              196  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              198  RETURN_VALUE     
            200_0  COME_FROM           160  '160'

 L. 967       200  LOAD_GLOBAL              dragon4_positional
              202  LOAD_FAST                'x'

 L. 968       204  LOAD_FAST                'self'
              206  LOAD_ATTR                precision

 L. 969       208  LOAD_FAST                'self'
              210  LOAD_ATTR                unique

 L. 970       212  LOAD_CONST               True

 L. 971       214  LOAD_FAST                'self'
              216  LOAD_ATTR                trim

 L. 972       218  LOAD_FAST                'self'
              220  LOAD_ATTR                sign
              222  LOAD_STR                 '+'
              224  COMPARE_OP               ==

 L. 973       226  LOAD_FAST                'self'
              228  LOAD_ATTR                pad_left

 L. 974       230  LOAD_FAST                'self'
              232  LOAD_ATTR                pad_right

 L. 967       234  LOAD_CONST               ('precision', 'unique', 'fractional', 'trim', 'sign', 'pad_left', 'pad_right')
              236  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              238  RETURN_VALUE     

Parse error at or near `ROT_TWO' instruction at offset 138


    @set_module('numpy')
    def format_float_scientific(x, precision=None, unique=True, trim='k', sign=False, pad_left=None, exp_digits=None):
        """
    Format a floating-point scalar as a decimal string in scientific notation.

    Provides control over rounding, trimming and padding. Uses and assumes
    IEEE unbiased rounding. Uses the "Dragon4" algorithm.

    Parameters
    ----------
    x : python float or numpy floating scalar
        Value to format.
    precision : non-negative integer or None, optional
        Maximum number of digits to print. May be None if `unique` is
        `True`, but must be an integer if unique is `False`.
    unique : boolean, optional
        If `True`, use a digit-generation strategy which gives the shortest
        representation which uniquely identifies the floating-point number from
        other values of the same type, by judicious rounding. If `precision`
        was omitted, print all necessary digits, otherwise digit generation is
        cut off after `precision` digits and the remaining value is rounded.
        If `False`, digits are generated as if printing an infinite-precision
        value and stopping after `precision` digits, rounding the remaining
        value.
    trim : one of 'k', '.', '0', '-', optional
        Controls post-processing trimming of trailing digits, as follows:

        * 'k' : keep trailing zeros, keep decimal point (no trimming)
        * '.' : trim all trailing zeros, leave decimal point
        * '0' : trim all but the zero before the decimal point. Insert the
          zero if it is missing.
        * '-' : trim trailing zeros and any trailing decimal point
    sign : boolean, optional
        Whether to show the sign for positive values.
    pad_left : non-negative integer, optional
        Pad the left side of the string with whitespace until at least that
        many characters are to the left of the decimal point.
    exp_digits : non-negative integer, optional
        Pad the exponent with zeros until it contains at least this many digits.
        If omitted, the exponent will be at least 2 digits.

    Returns
    -------
    rep : string
        The string representation of the floating point value

    See Also
    --------
    format_float_positional

    Examples
    --------
    >>> np.format_float_scientific(np.float32(np.pi))
    '3.1415927e+00'
    >>> s = np.float32(1.23e24)
    >>> np.format_float_scientific(s, unique=False, precision=15)
    '1.230000071797338e+24'
    >>> np.format_float_scientific(s, exp_digits=4)
    '1.23e+0024'
    """
        precision = _none_or_positive_arg(precision, 'precision')
        pad_left = _none_or_positive_arg(pad_left, 'pad_left')
        exp_digits = _none_or_positive_arg(exp_digits, 'exp_digits')
        return dragon4_scientific(x, precision=precision, unique=unique, trim=trim,
          sign=sign,
          pad_left=pad_left,
          exp_digits=exp_digits)


    @set_module('numpy')
    def format_float_positional(x, precision=None, unique=True, fractional=True, trim='k', sign=False, pad_left=None, pad_right=None):
        """
    Format a floating-point scalar as a decimal string in positional notation.

    Provides control over rounding, trimming and padding. Uses and assumes
    IEEE unbiased rounding. Uses the "Dragon4" algorithm.

    Parameters
    ----------
    x : python float or numpy floating scalar
        Value to format.
    precision : non-negative integer or None, optional
        Maximum number of digits to print. May be None if `unique` is
        `True`, but must be an integer if unique is `False`.
    unique : boolean, optional
        If `True`, use a digit-generation strategy which gives the shortest
        representation which uniquely identifies the floating-point number from
        other values of the same type, by judicious rounding. If `precision`
        was omitted, print out all necessary digits, otherwise digit generation
        is cut off after `precision` digits and the remaining value is rounded.
        If `False`, digits are generated as if printing an infinite-precision
        value and stopping after `precision` digits, rounding the remaining
        value.
    fractional : boolean, optional
        If `True`, the cutoff of `precision` digits refers to the total number
        of digits after the decimal point, including leading zeros.
        If `False`, `precision` refers to the total number of significant
        digits, before or after the decimal point, ignoring leading zeros.
    trim : one of 'k', '.', '0', '-', optional
        Controls post-processing trimming of trailing digits, as follows:

        * 'k' : keep trailing zeros, keep decimal point (no trimming)
        * '.' : trim all trailing zeros, leave decimal point
        * '0' : trim all but the zero before the decimal point. Insert the
          zero if it is missing.
        * '-' : trim trailing zeros and any trailing decimal point
    sign : boolean, optional
        Whether to show the sign for positive values.
    pad_left : non-negative integer, optional
        Pad the left side of the string with whitespace until at least that
        many characters are to the left of the decimal point.
    pad_right : non-negative integer, optional
        Pad the right side of the string with whitespace until at least that
        many characters are to the right of the decimal point.

    Returns
    -------
    rep : string
        The string representation of the floating point value

    See Also
    --------
    format_float_scientific

    Examples
    --------
    >>> np.format_float_positional(np.float32(np.pi))
    '3.1415927'
    >>> np.format_float_positional(np.float16(np.pi))
    '3.14'
    >>> np.format_float_positional(np.float16(0.3))
    '0.3'
    >>> np.format_float_positional(np.float16(0.3), unique=False, precision=10)
    '0.3000488281'
    """
        precision = _none_or_positive_arg(precision, 'precision')
        pad_left = _none_or_positive_arg(pad_left, 'pad_left')
        pad_right = _none_or_positive_arg(pad_right, 'pad_right')
        return dragon4_positional(x, precision=precision, unique=unique, fractional=fractional,
          trim=trim,
          sign=sign,
          pad_left=pad_left,
          pad_right=pad_right)


    class IntegerFormat:

        def __init__(self, data):
            if data.size > 0:
                max_str_len = max(len(str(np.max(data))), len(str(np.min(data))))
            else:
                max_str_len = 0
            self.format = '%{}d'.format(max_str_len)

        def __call__(self, x):
            return self.format % x


    class BoolFormat:

        def __init__(self, data, **kwargs):
            self.truestr = ' True' if data.shape != () else 'True'

        def __call__(self, x):
            if x:
                return self.truestr
            return 'False'


    class ComplexFloatingFormat:
        __doc__ = ' Formatter for subtypes of np.complexfloating '

        def __init__(self, x, precision, floatmode, suppress_small, sign=False, *, legacy=None):
            if isinstance(sign, bool):
                sign = '+' if sign else '-'
            floatmode_real = floatmode_imag = floatmode
            if legacy == '1.13':
                floatmode_real = 'maxprec_equal'
                floatmode_imag = 'maxprec'
            self.real_format = FloatingFormat((x.real),
              precision, floatmode_real, suppress_small, sign=sign,
              legacy=legacy)
            self.imag_format = FloatingFormat((x.imag),
              precision, floatmode_imag, suppress_small, sign='+',
              legacy=legacy)

        def __call__(self, x):
            r = self.real_format(x.real)
            i = self.imag_format(x.imag)
            sp = len(i.rstrip())
            i = i[:sp] + 'j' + i[sp:]
            return r + i


    class _TimelikeFormat:

        def __init__(self, data):
            non_nat = data[(~isnat(data))]
            if len(non_nat) > 0:
                max_str_len = max(len(self._format_non_nat(np.max(non_nat))), len(self._format_non_nat(np.min(non_nat))))
            else:
                max_str_len = 0
            if len(non_nat) < data.size:
                max_str_len = max(max_str_len, 5)
            self._format = '%{}s'.format(max_str_len)
            self._nat = "'NaT'".rjust(max_str_len)

        def _format_non_nat(self, x):
            raise NotImplementedError

        def __call__(self, x):
            if isnat(x):
                return self._nat
            return self._format % self._format_non_nat(x)


    class DatetimeFormat(_TimelikeFormat):

        def __init__(self, x, unit=None, timezone=None, casting='same_kind', legacy=False):
            if unit is None:
                if x.dtype.kind == 'M':
                    unit = datetime_data(x.dtype)[0]
                else:
                    unit = 's'
            if timezone is None:
                timezone = 'naive'
            self.timezone = timezone
            self.unit = unit
            self.casting = casting
            self.legacy = legacy
            super(DatetimeFormat, self).__init__(x)

        def __call__(self, x):
            if self.legacy == '1.13':
                return self._format_non_nat(x)
            return super(DatetimeFormat, self).__call__(x)

        def _format_non_nat(self, x):
            return "'%s'" % datetime_as_string(x, unit=(self.unit),
              timezone=(self.timezone),
              casting=(self.casting))


    class TimedeltaFormat(_TimelikeFormat):

        def _format_non_nat(self, x):
            return str(x.astype('i8'))


    class SubArrayFormat:

        def __init__(self, format_function):
            self.format_function = format_function

        def __call__(self, arr):
            if arr.ndim <= 1:
                return '[' + ', '.join((self.format_function(a) for a in arr)) + ']'
            return '[' + ', '.join((self.__call__(a) for a in arr)) + ']'


    class StructuredVoidFormat:
        __doc__ = "\n    Formatter for structured np.void objects.\n\n    This does not work on structured alias types like np.dtype(('i4', 'i2,i2')),\n    as alias scalars lose their field information, and the implementation\n    relies upon np.void.__getitem__.\n    "

        def __init__(self, format_functions):
            self.format_functions = format_functions

        @classmethod
        def from_data(cls, data, **options):
            """
        This is a second way to initialize StructuredVoidFormat, using the raw data
        as input. Added to avoid changing the signature of __init__.
        """
            format_functions = []
            for field_name in data.dtype.names:
                format_function = _get_format_function((data[field_name]), **options)
                if data.dtype[field_name].shape != ():
                    format_function = SubArrayFormat(format_function)
                format_functions.append(format_function)
            else:
                return cls(format_functions)

        def __call__(self, x):
            str_fields = [format_function(field) for field, format_function in zip(x, self.format_functions)]
            if len(str_fields) == 1:
                return '({},)'.format(str_fields[0])
            return '({})'.format(', '.join(str_fields))


    def _void_scalar_repr(x):
        """
    Implements the repr for structured-void scalars. It is called from the
    scalartypes.c.src code, and is placed here because it uses the elementwise
    formatters defined above.
    """
        return (StructuredVoidFormat.from_data)((array(x)), **_format_options)(x)


    _typelessdata = [
     int_, float_, complex_, bool_]
    if issubclass(intc, int):
        _typelessdata.append(intc)
    if issubclass(longlong, int):
        _typelessdata.append(longlong)

    def dtype_is_implied(dtype):
        """
    Determine if the given dtype is implied by the representation of its values.

    Parameters
    ----------
    dtype : dtype
        Data type

    Returns
    -------
    implied : bool
        True if the dtype is implied by the representation of its values.

    Examples
    --------
    >>> np.core.arrayprint.dtype_is_implied(int)
    True
    >>> np.array([1, 2, 3], int)
    array([1, 2, 3])
    >>> np.core.arrayprint.dtype_is_implied(np.int8)
    False
    >>> np.array([1, 2, 3], np.int8)
    array([1, 2, 3], dtype=int8)
    """
        dtype = np.dtype(dtype)
        if _format_options['legacy'] == '1.13':
            if dtype.type == bool_:
                return False
        if dtype.names is not None:
            return False
        return dtype.type in _typelessdata


    def dtype_short_repr(dtype):
        """
    Convert a dtype to a short form which evaluates to the same dtype.

    The intent is roughly that the following holds

    >>> from numpy import *
    >>> dt = np.int64([1, 2]).dtype
    >>> assert eval(dtype_short_repr(dt)) == dt
    """
        if dtype.names is not None:
            return str(dtype)
        else:
            if issubclass(dtype.type, flexible):
                return "'%s'" % str(dtype)
            typename = dtype.name
            if typename:
                typename = typename[0].isalpha() and typename.isalnum() or repr(typename)
        return typename


    def _array_repr_implementation(arr, max_line_width=None, precision=None, suppress_small=None, array2string=array2string):
        """Internal version of array_repr() that allows overriding array2string."""
        if max_line_width is None:
            max_line_width = _format_options['linewidth']
        else:
            if type(arr) is not ndarray:
                class_name = type(arr).__name__
            else:
                class_name = 'array'
            skipdtype = dtype_is_implied(arr.dtype) and arr.size > 0
            prefix = class_name + '('
            suffix = ')' if skipdtype else ','
            if _format_options['legacy'] == '1.13' and arr.shape == ():
                if not arr.dtype.names:
                    lst = repr(arr.item())
                else:
                    if arr.size > 0 or arr.shape == (0, ):
                        lst = array2string(arr, max_line_width, precision, suppress_small, ', ',
                          prefix, suffix=suffix)
                    else:
                        lst = '[], shape=%s' % (repr(arr.shape),)
                arr_str = prefix + lst + suffix
                if skipdtype:
                    return arr_str
                dtype_str = 'dtype={})'.format(dtype_short_repr(arr.dtype))
                last_line_len = len(arr_str) - (arr_str.rfind('\n') + 1)
                spacer = ' '
                if _format_options['legacy'] == '1.13':
                    if issubclass(arr.dtype.type, flexible):
                        spacer = '\n' + ' ' * len(class_name + '(')
            elif last_line_len + len(dtype_str) + 1 > max_line_width:
                spacer = '\n' + ' ' * len(class_name + '(')
        return arr_str + spacer + dtype_str


    def _array_repr_dispatcher(arr, max_line_width=None, precision=None, suppress_small=None):
        return (
         arr,)


    @array_function_dispatch(_array_repr_dispatcher, module='numpy')
    def array_repr(arr, max_line_width=None, precision=None, suppress_small=None):
        """
    Return the string representation of an array.

    Parameters
    ----------
    arr : ndarray
        Input array.
    max_line_width : int, optional
        Inserts newlines if text is longer than `max_line_width`.
        Defaults to ``numpy.get_printoptions()['linewidth']``.
    precision : int, optional
        Floating point precision.
        Defaults to ``numpy.get_printoptions()['precision']``.
    suppress_small : bool, optional
        Represent numbers "very close" to zero as zero; default is False.
        Very close is defined by precision: if the precision is 8, e.g.,
        numbers smaller (in absolute value) than 5e-9 are represented as
        zero.
        Defaults to ``numpy.get_printoptions()['suppress']``.

    Returns
    -------
    string : str
      The string representation of an array.

    See Also
    --------
    array_str, array2string, set_printoptions

    Examples
    --------
    >>> np.array_repr(np.array([1,2]))
    'array([1, 2])'
    >>> np.array_repr(np.ma.array([0.]))
    'MaskedArray([0.])'
    >>> np.array_repr(np.array([], np.int32))
    'array([], dtype=int32)'

    >>> x = np.array([1e-6, 4e-7, 2, 3])
    >>> np.array_repr(x, precision=6, suppress_small=True)
    'array([0.000001,  0.      ,  2.      ,  3.      ])'

    """
        return _array_repr_implementation(arr, max_line_width, precision, suppress_small)


    @_recursive_guard()
    def _guarded_repr_or_str(v):
        if isinstance(v, bytes):
            return repr(v)
        return str(v)


    def _array_str_implementation(a, max_line_width=None, precision=None, suppress_small=None, array2string=array2string):
        """Internal version of array_str() that allows overriding array2string."""
        if _format_options['legacy'] == '1.13':
            if a.shape == ():
                if not a.dtype.names:
                    return str(a.item())
        if a.shape == ():
            return _guarded_repr_or_str(np.ndarray.__getitem__(a, ()))
        return array2string(a, max_line_width, precision, suppress_small, ' ', '')


    def _array_str_dispatcher(a, max_line_width=None, precision=None, suppress_small=None):
        return (
         a,)


    @array_function_dispatch(_array_str_dispatcher, module='numpy')
    def array_str(a, max_line_width=None, precision=None, suppress_small=None):
        """
    Return a string representation of the data in an array.

    The data in the array is returned as a single string.  This function is
    similar to `array_repr`, the difference being that `array_repr` also
    returns information on the kind of array and its data type.

    Parameters
    ----------
    a : ndarray
        Input array.
    max_line_width : int, optional
        Inserts newlines if text is longer than `max_line_width`.
        Defaults to ``numpy.get_printoptions()['linewidth']``.
    precision : int, optional
        Floating point precision.
        Defaults to ``numpy.get_printoptions()['precision']``.
    suppress_small : bool, optional
        Represent numbers "very close" to zero as zero; default is False.
        Very close is defined by precision: if the precision is 8, e.g.,
        numbers smaller (in absolute value) than 5e-9 are represented as
        zero.
        Defaults to ``numpy.get_printoptions()['suppress']``.

    See Also
    --------
    array2string, array_repr, set_printoptions

    Examples
    --------
    >>> np.array_str(np.arange(3))
    '[0 1 2]'

    """
        return _array_str_implementation(a, max_line_width, precision, suppress_small)


    _array2string_impl = getattr(array2string, '__wrapped__', array2string)
    _default_array_str = functools.partial(_array_str_implementation, array2string=_array2string_impl)
    _default_array_repr = functools.partial(_array_repr_implementation, array2string=_array2string_impl)

    def set_string_function(f, repr=True):
        """
    Set a Python function to be used when pretty printing arrays.

    Parameters
    ----------
    f : function or None
        Function to be used to pretty print arrays. The function should expect
        a single array argument and return a string of the representation of
        the array. If None, the function is reset to the default NumPy function
        to print arrays.
    repr : bool, optional
        If True (default), the function for pretty printing (``__repr__``)
        is set, if False the function that returns the default string
        representation (``__str__``) is set.

    See Also
    --------
    set_printoptions, get_printoptions

    Examples
    --------
    >>> def pprint(arr):
    ...     return 'HA! - What are you going to do now?'
    ...
    >>> np.set_string_function(pprint)
    >>> a = np.arange(10)
    >>> a
    HA! - What are you going to do now?
    >>> _ = a
    >>> # [0 1 2 3 4 5 6 7 8 9]

    We can reset the function to the default:

    >>> np.set_string_function(None)
    >>> a
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    `repr` affects either pretty printing or normal string representation.
    Note that ``__repr__`` is still affected by setting ``__str__``
    because the width of each array element in the returned string becomes
    equal to the length of the result of ``__str__()``.

    >>> x = np.arange(4)
    >>> np.set_string_function(lambda x:'random', repr=False)
    >>> x.__str__()
    'random'
    >>> x.__repr__()
    'array([0, 1, 2, 3])'

    """
        if f is None:
            if repr:
                return multiarray.set_string_function(_default_array_repr, 1)
            return multiarray.set_string_function(_default_array_str, 0)
        else:
            return multiarray.set_string_function(f, repr)


    set_string_function(_default_array_str, False)
    set_string_function(_default_array_repr, True)