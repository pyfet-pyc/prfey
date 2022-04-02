# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\lib\_iotools.py
"""A collection of functions designed to help I/O with ascii files.

"""
__docformat__ = 'restructuredtext en'
import numpy as np
import numpy.core.numeric as nx
from numpy.compat import asbytes, asunicode

def _decode_line(line, encoding=None):
    """Decode bytes from binary input streams.

    Defaults to decoding from 'latin1'. That differs from the behavior of
    np.compat.asunicode that decodes from 'ascii'.

    Parameters
    ----------
    line : str or bytes
         Line to be decoded.
    encoding : str
         Encoding used to decode `line`.

    Returns
    -------
    decoded_line : unicode
         Unicode in Python 2, a str (unicode) in Python 3.

    """
    if type(line) is bytes:
        if encoding is None:
            encoding = 'latin1'
        line = line.decode(encoding)
    return line


def _is_string_like(obj):
    """
    Check whether obj behaves like a string.
    """
    try:
        obj + ''
    except (TypeError, ValueError):
        return False
    else:
        return True


def _is_bytes_like(obj):
    """
    Check whether obj behaves like a bytes object.
    """
    try:
        obj + b''
    except (TypeError, ValueError):
        return False
    else:
        return True


def has_nested_fields(ndtype):
    """
    Returns whether one or several fields of a dtype are nested.

    Parameters
    ----------
    ndtype : dtype
        Data-type of a structured array.

    Raises
    ------
    AttributeError
        If `ndtype` does not have a `names` attribute.

    Examples
    --------
    >>> dt = np.dtype([('name', 'S4'), ('x', float), ('y', float)])
    >>> np.lib._iotools.has_nested_fields(dt)
    False

    """
    for name in ndtype.names or ():
        if ndtype[name].names is not None:
            return True
        return False


def flatten_dtype(ndtype, flatten_base=False):
    """
    Unpack a structured data-type by collapsing nested fields and/or fields
    with a shape.

    Note that the field names are lost.

    Parameters
    ----------
    ndtype : dtype
        The datatype to collapse
    flatten_base : bool, optional
       If True, transform a field with a shape into several fields. Default is
       False.

    Examples
    --------
    >>> dt = np.dtype([('name', 'S4'), ('x', float), ('y', float),
    ...                ('block', int, (2, 3))])
    >>> np.lib._iotools.flatten_dtype(dt)
    [dtype('S4'), dtype('float64'), dtype('float64'), dtype('int64')]
    >>> np.lib._iotools.flatten_dtype(dt, flatten_base=True)
    [dtype('S4'),
     dtype('float64'),
     dtype('float64'),
     dtype('int64'),
     dtype('int64'),
     dtype('int64'),
     dtype('int64'),
     dtype('int64'),
     dtype('int64')]

    """
    names = ndtype.names
    if names is None:
        if flatten_base:
            return [
             ndtype.base] * int(np.prod(ndtype.shape))
        return [
         ndtype.base]
    types = []
    for field in names:
        info = ndtype.fields[field]
        flat_dt = flatten_dtype(info[0], flatten_base)
        types.extend(flat_dt)
    else:
        return types


class LineSplitter:
    __doc__ = "\n    Object to split a string at a given delimiter or at given places.\n\n    Parameters\n    ----------\n    delimiter : str, int, or sequence of ints, optional\n        If a string, character used to delimit consecutive fields.\n        If an integer or a sequence of integers, width(s) of each field.\n    comments : str, optional\n        Character used to mark the beginning of a comment. Default is '#'.\n    autostrip : bool, optional\n        Whether to strip each individual field. Default is True.\n\n    "

    def autostrip(self, method):
        """
        Wrapper to strip each member of the output of `method`.

        Parameters
        ----------
        method : function
            Function that takes a single argument and returns a sequence of
            strings.

        Returns
        -------
        wrapped : function
            The result of wrapping `method`. `wrapped` takes a single input
            argument and returns a list of strings that are stripped of
            white-space.

        """
        return lambda input: [_.strip() for _ in method(input)]

    def __init__(self, delimiter=None, comments='#', autostrip=True, encoding=None):
        delimiter = _decode_line(delimiter)
        comments = _decode_line(comments)
        self.comments = comments
        if delimiter is None or isinstance(delimiter, str):
            delimiter = delimiter or None
            _handyman = self._delimited_splitter
        else:
            if hasattr(delimiter, '__iter__'):
                _handyman = self._variablewidth_splitter
                idx = np.cumsum([0] + list(delimiter))
                delimiter = [slice(i, j) for i, j in zip(idx[:-1], idx[1:])]
            else:
                if int(delimiter):
                    _handyman, delimiter = self._fixedwidth_splitter, int(delimiter)
                else:
                    _handyman, delimiter = self._delimited_splitter, None
        self.delimiter = delimiter
        if autostrip:
            self._handyman = self.autostrip(_handyman)
        else:
            self._handyman = _handyman
        self.encoding = encoding

    def _delimited_splitter(self, line):
        """Chop off comments, strip, and split at delimiter. """
        if self.comments is not None:
            line = line.split(self.comments)[0]
        else:
            line = line.strip(' \r\n')
            return line or []
        return line.split(self.delimiter)

    def _fixedwidth_splitter(self, line):
        if self.comments is not None:
            line = line.split(self.comments)[0]
        else:
            line = line.strip('\r\n')
            return line or []
        fixed = self.delimiter
        slices = [slice(i, i + fixed) for i in range(0, len(line), fixed)]
        return [line[s] for s in slices]

    def _variablewidth_splitter(self, line):
        if self.comments is not None:
            line = line.split(self.comments)[0]
        else:
            return line or []
        slices = self.delimiter
        return [line[s] for s in slices]

    def __call__(self, line):
        return self._handyman(_decode_line(line, self.encoding))


class NameValidator:
    __doc__ = '\n    Object to validate a list of strings to use as field names.\n\n    The strings are stripped of any non alphanumeric character, and spaces\n    are replaced by \'_\'. During instantiation, the user can define a list\n    of names to exclude, as well as a list of invalid characters. Names in\n    the exclusion list are appended a \'_\' character.\n\n    Once an instance has been created, it can be called with a list of\n    names, and a list of valid names will be created.  The `__call__`\n    method accepts an optional keyword "default" that sets the default name\n    in case of ambiguity. By default this is \'f\', so that names will\n    default to `f0`, `f1`, etc.\n\n    Parameters\n    ----------\n    excludelist : sequence, optional\n        A list of names to exclude. This list is appended to the default\n        list [\'return\', \'file\', \'print\']. Excluded names are appended an\n        underscore: for example, `file` becomes `file_` if supplied.\n    deletechars : str, optional\n        A string combining invalid characters that must be deleted from the\n        names.\n    case_sensitive : {True, False, \'upper\', \'lower\'}, optional\n        * If True, field names are case-sensitive.\n        * If False or \'upper\', field names are converted to upper case.\n        * If \'lower\', field names are converted to lower case.\n\n        The default value is True.\n    replace_space : \'_\', optional\n        Character(s) used in replacement of white spaces.\n\n    Notes\n    -----\n    Calling an instance of `NameValidator` is the same as calling its\n    method `validate`.\n\n    Examples\n    --------\n    >>> validator = np.lib._iotools.NameValidator()\n    >>> validator([\'file\', \'field2\', \'with space\', \'CaSe\'])\n    (\'file_\', \'field2\', \'with_space\', \'CaSe\')\n\n    >>> validator = np.lib._iotools.NameValidator(excludelist=[\'excl\'],\n    ...                                           deletechars=\'q\',\n    ...                                           case_sensitive=False)\n    >>> validator([\'excl\', \'field2\', \'no_q\', \'with space\', \'CaSe\'])\n    (\'EXCL\', \'FIELD2\', \'NO_Q\', \'WITH_SPACE\', \'CASE\')\n\n    '
    defaultexcludelist = [
     'return', 'file', 'print']
    defaultdeletechars = set("~!@#$%^&*()-=+~\\|]}[{';: /?.>,<")

    def __init__(self, excludelist=None, deletechars=None, case_sensitive=None, replace_space='_'):
        if excludelist is None:
            excludelist = []
        else:
            excludelist.extend(self.defaultexcludelist)
            self.excludelist = excludelist
            if deletechars is None:
                delete = self.defaultdeletechars
            else:
                delete = set(deletechars)
            delete.add('"')
            self.deletechars = delete
            if case_sensitive is None or case_sensitive is True:
                self.case_converter = lambda x: x
            else:
                if case_sensitive is False or case_sensitive.startswith('u'):
                    self.case_converter = lambda x: x.upper()
                else:
                    if case_sensitive.startswith('l'):
                        self.case_converter = lambda x: x.lower()
                    else:
                        msg = 'unrecognized case_sensitive value %s.' % case_sensitive
                        raise ValueError(msg)
        self.replace_space = replace_space

    def validate(self, names, defaultfmt='f%i', nbfields=None):
        """
        Validate a list of strings as field names for a structured array.

        Parameters
        ----------
        names : sequence of str
            Strings to be validated.
        defaultfmt : str, optional
            Default format string, used if validating a given string
            reduces its length to zero.
        nbfields : integer, optional
            Final number of validated names, used to expand or shrink the
            initial list of names.

        Returns
        -------
        validatednames : list of str
            The list of validated field names.

        Notes
        -----
        A `NameValidator` instance can be called directly, which is the
        same as calling `validate`. For examples, see `NameValidator`.

        """
        if names is None:
            if nbfields is None:
                return
            names = []
        else:
            if isinstance(names, str):
                names = [
                 names]
            if nbfields is not None:
                nbnames = len(names)
                if nbnames < nbfields:
                    names = list(names) + [''] * (nbfields - nbnames)
                else:
                    if nbnames > nbfields:
                        names = names[:nbfields]
        deletechars = self.deletechars
        excludelist = self.excludelist
        case_converter = self.case_converter
        replace_space = self.replace_space
        validatednames = []
        seen = dict()
        nbempty = 0
        for item in names:
            item = case_converter(item).strip()
            if replace_space:
                item = item.replace(' ', replace_space)
            item = ''.join([c for c in item if c not in deletechars])
            if item == '':
                item = defaultfmt % nbempty
                while item in names:
                    nbempty += 1
                    item = defaultfmt % nbempty

                nbempty += 1
            else:
                if item in excludelist:
                    item += '_'
                else:
                    cnt = seen.get(item, 0)
                    if cnt > 0:
                        validatednames.append(item + '_%d' % cnt)
                    else:
                        validatednames.append(item)
            seen[item] = cnt + 1
        else:
            return tuple(validatednames)

    def __call__(self, names, defaultfmt='f%i', nbfields=None):
        return self.validate(names, defaultfmt=defaultfmt, nbfields=nbfields)


def str2bool(value):
    """
    Tries to transform a string supposed to represent a boolean to a boolean.

    Parameters
    ----------
    value : str
        The string that is transformed to a boolean.

    Returns
    -------
    boolval : bool
        The boolean representation of `value`.

    Raises
    ------
    ValueError
        If the string is not 'True' or 'False' (case independent)

    Examples
    --------
    >>> np.lib._iotools.str2bool('TRUE')
    True
    >>> np.lib._iotools.str2bool('false')
    False

    """
    value = value.upper()
    if value == 'TRUE':
        return True
    if value == 'FALSE':
        return False
    raise ValueError('Invalid boolean')


class ConverterError(Exception):
    __doc__ = '\n    Exception raised when an error occurs in a converter for string values.\n\n    '


class ConverterLockError(ConverterError):
    __doc__ = '\n    Exception raised when an attempt is made to upgrade a locked converter.\n\n    '


class ConversionWarning(UserWarning):
    __doc__ = '\n    Warning issued when a string converter has a problem.\n\n    Notes\n    -----\n    In `genfromtxt` a `ConversionWarning` is issued if raising exceptions\n    is explicitly suppressed with the "invalid_raise" keyword.\n\n    '


class StringConverter:
    __doc__ = '\n    Factory class for function transforming a string into another object\n    (int, float).\n\n    After initialization, an instance can be called to transform a string\n    into another object. If the string is recognized as representing a\n    missing value, a default value is returned.\n\n    Attributes\n    ----------\n    func : function\n        Function used for the conversion.\n    default : any\n        Default value to return when the input corresponds to a missing\n        value.\n    type : type\n        Type of the output.\n    _status : int\n        Integer representing the order of the conversion.\n    _mapper : sequence of tuples\n        Sequence of tuples (dtype, function, default value) to evaluate in\n        order.\n    _locked : bool\n        Holds `locked` parameter.\n\n    Parameters\n    ----------\n    dtype_or_func : {None, dtype, function}, optional\n        If a `dtype`, specifies the input data type, used to define a basic\n        function and a default value for missing data. For example, when\n        `dtype` is float, the `func` attribute is set to `float` and the\n        default value to `np.nan`.  If a function, this function is used to\n        convert a string to another object. In this case, it is recommended\n        to give an associated default value as input.\n    default : any, optional\n        Value to return by default, that is, when the string to be\n        converted is flagged as missing. If not given, `StringConverter`\n        tries to supply a reasonable default value.\n    missing_values : {None, sequence of str}, optional\n        ``None`` or sequence of strings indicating a missing value. If ``None``\n        then missing values are indicated by empty entries. The default is\n        ``None``.\n    locked : bool, optional\n        Whether the StringConverter should be locked to prevent automatic\n        upgrade or not. Default is False.\n\n    '
    _mapper = [
     (
      nx.bool_, str2bool, False),
     (
      nx.int_, int, -1)]
    if nx.dtype(nx.int_).itemsize < nx.dtype(nx.int64).itemsize:
        _mapper.append((nx.int64, int, -1))
    _mapper.extend([(nx.float64, float, nx.nan),
     (
      nx.complex128, complex, nx.nan + complex(0.0, 0.0)),
     (
      nx.longdouble, nx.longdouble, nx.nan),
     (
      nx.integer, int, -1),
     (
      nx.floating, float, nx.nan),
     (
      nx.complexfloating, complex, nx.nan + complex(0.0, 0.0)),
     (
      nx.unicode_, asunicode, '???'),
     (
      nx.string_, asbytes, '???')])

    @classmethod
    def _getdtype(cls, val):
        """Returns the dtype of the input variable."""
        return np.array(val).dtype

    @classmethod
    def _getsubdtype(cls, val):
        """Returns the type of the dtype of the input variable."""
        return np.array(val).dtype.type

    @classmethod
    def _dtypeortype(cls, dtype):
        """Returns dtype for datetime64 and type of dtype otherwise."""
        if dtype.type == np.datetime64:
            return dtype
        return dtype.type

    @classmethod
    def upgrade_mapper(cls, func, default=None):
        """
        Upgrade the mapper of a StringConverter by adding a new function and
        its corresponding default.

        The input function (or sequence of functions) and its associated
        default value (if any) is inserted in penultimate position of the
        mapper.  The corresponding type is estimated from the dtype of the
        default value.

        Parameters
        ----------
        func : var
            Function, or sequence of functions

        Examples
        --------
        >>> import dateutil.parser
        >>> import datetime
        >>> dateparser = dateutil.parser.parse
        >>> defaultdate = datetime.date(2000, 1, 1)
        >>> StringConverter.upgrade_mapper(dateparser, default=defaultdate)
        """
        if hasattr(func, '__call__'):
            cls._mapper.insert(-1, (cls._getsubdtype(default), func, default))
            return None
        if hasattr(func, '__iter__'):
            if isinstance(func[0], (tuple, list)):
                for _ in func:
                    cls._mapper.insert(-1, _)
                else:
                    return

            elif default is None:
                default = [
                 None] * len(func)
            else:
                default = list(default)
                default.append([None] * (len(func) - len(default)))
            for fct, dft in zip(func, default):
                cls._mapper.insert(-1, (cls._getsubdtype(dft), fct, dft))

    @classmethod
    def _find_map_entry(cls, dtype):
        for i, (deftype, func, default_def) in enumerate(cls._mapper):
            if dtype.type == deftype:
                return (
                 i, (deftype, func, default_def))
        else:
            for i, (deftype, func, default_def) in enumerate(cls._mapper):
                if np.issubdtype(dtype.type, deftype):
                    return (
                     i, (deftype, func, default_def))
            else:
                raise LookupError

    def __init__(self, dtype_or_func=None, default=None, missing_values=None, locked=False):
        self._locked = bool(locked)
        if dtype_or_func is None:
            self.func = str2bool
            self._status = 0
            self.default = default or False
            dtype = np.dtype('bool')
        else:
            try:
                self.func = None
                dtype = np.dtype(dtype_or_func)
            except TypeError:
                if not hasattr(dtype_or_func, '__call__'):
                    errmsg = "The input argument `dtype` is neither a function nor a dtype (got '%s' instead)"
                    raise TypeError(errmsg % type(dtype_or_func))
                self.func = dtype_or_func
                if default is None:
                    try:
                        default = self.func('0')
                    except ValueError:
                        default = None

                dtype = self._getdtype(default)
            else:
                try:
                    self._status, (_, func, default_def) = self._find_map_entry(dtype)
                except LookupError:
                    self.default = default
                    _, func, _ = self._mapper[(-1)]
                    self._status = 0
                else:
                    if default is None:
                        self.default = default_def
                    else:
                        self.default = default
                    if self.func == self._mapper[1][1]:
                        if issubclass(dtype.type, np.uint64):
                            self.func = np.uint64
                        else:
                            if issubclass(dtype.type, np.int64):
                                self.func = np.int64
                            else:
                                self.func = lambda x: int(float(x))
                    elif missing_values is None:
                        self.missing_values = {
                         ''}
                    else:
                        if isinstance(missing_values, str):
                            missing_values = missing_values.split(',')
                        self.missing_values = set(list(missing_values) + [''])
                    self._callingfunction = self._strict_call
                    self.type = self._dtypeortype(dtype)
                    self._checked = False
                    self._initial_default = default

    def _loose_call--- This code section failed: ---

 L. 672         0  SETUP_FINALLY        14  'to 14'

 L. 673         2  LOAD_FAST                'self'
                4  LOAD_METHOD              func
                6  LOAD_FAST                'value'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 674        14  DUP_TOP          
               16  LOAD_GLOBAL              ValueError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    38  'to 38'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 675        28  LOAD_FAST                'self'
               30  LOAD_ATTR                default
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
             38_0  COME_FROM            20  '20'
               38  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24

    def _strict_call--- This code section failed: ---

 L. 678         0  SETUP_FINALLY        74  'to 74'

 L. 681         2  LOAD_FAST                'self'
                4  LOAD_METHOD              func
                6  LOAD_FAST                'value'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'new_value'

 L. 686        12  LOAD_FAST                'self'
               14  LOAD_ATTR                func
               16  LOAD_GLOBAL              int
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    68  'to 68'

 L. 687        22  SETUP_FINALLY        44  'to 44'

 L. 688        24  LOAD_GLOBAL              np
               26  LOAD_ATTR                array
               28  LOAD_FAST                'value'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                type
               34  LOAD_CONST               ('dtype',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD         68  'to 68'
             44_0  COME_FROM_FINALLY    22  '22'

 L. 689        44  DUP_TOP          
               46  LOAD_GLOBAL              OverflowError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    66  'to 66'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 690        58  LOAD_GLOBAL              ValueError
               60  RAISE_VARARGS_1       1  'exception instance'
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            50  '50'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            42  '42'
             68_2  COME_FROM            20  '20'

 L. 693        68  LOAD_FAST                'new_value'
               70  POP_BLOCK        
               72  RETURN_VALUE     
             74_0  COME_FROM_FINALLY     0  '0'

 L. 695        74  DUP_TOP          
               76  LOAD_GLOBAL              ValueError
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   140  'to 140'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 696        88  LOAD_FAST                'value'
               90  LOAD_METHOD              strip
               92  CALL_METHOD_0         0  ''
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                missing_values
               98  COMPARE_OP               in
              100  POP_JUMP_IF_FALSE   124  'to 124'

 L. 697       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _status
              106  POP_JUMP_IF_TRUE    114  'to 114'

 L. 698       108  LOAD_CONST               False
              110  LOAD_FAST                'self'
              112  STORE_ATTR               _checked
            114_0  COME_FROM           106  '106'

 L. 699       114  LOAD_FAST                'self'
              116  LOAD_ATTR                default
              118  ROT_FOUR         
              120  POP_EXCEPT       
              122  RETURN_VALUE     
            124_0  COME_FROM           100  '100'

 L. 700       124  LOAD_GLOBAL              ValueError
              126  LOAD_STR                 "Cannot convert string '%s'"
              128  LOAD_FAST                'value'
              130  BINARY_MODULO    
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM            80  '80'
              140  END_FINALLY      
            142_0  COME_FROM           138  '138'

Parse error at or near `POP_TOP' instruction at offset 84

    def __call__(self, value):
        return self._callingfunction(value)

    def _do_upgrade(self):
        if self._locked:
            errmsg = 'Converter is locked and cannot be upgraded'
            raise ConverterLockError(errmsg)
        else:
            _statusmax = len(self._mapper)
            _status = self._status
            if _status == _statusmax:
                errmsg = 'Could not find a valid conversion function'
                raise ConverterError(errmsg)
            else:
                if _status < _statusmax - 1:
                    _status += 1
            self.type, self.func, default = self._mapper[_status]
            self._status = _status
            if self._initial_default is not None:
                self.default = self._initial_default
            else:
                self.default = default

    def upgrade--- This code section failed: ---

 L. 746         0  LOAD_CONST               True
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _checked

 L. 747         6  SETUP_FINALLY        20  'to 20'

 L. 748         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _strict_call
               12  LOAD_FAST                'value'
               14  CALL_METHOD_1         1  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     6  '6'

 L. 749        20  DUP_TOP          
               22  LOAD_GLOBAL              ValueError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    56  'to 56'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 750        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _do_upgrade
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 751        42  LOAD_FAST                'self'
               44  LOAD_METHOD              upgrade
               46  LOAD_FAST                'value'
               48  CALL_METHOD_1         1  ''
               50  ROT_FOUR         
               52  POP_EXCEPT       
               54  RETURN_VALUE     
             56_0  COME_FROM            26  '26'
               56  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 30

    def iterupgrade(self, value):
        self._checked = True
        if not hasattr(value, '__iter__'):
            value = (
             value,)
        _strict_call = self._strict_call
        try:
            for _m in value:
                _strict_call(_m)

        except ValueError:
            self._do_upgrade()
            self.iterupgrade(value)

    def update(self, func, default=None, testing_value=None, missing_values='', locked=False):
        """
        Set StringConverter attributes directly.

        Parameters
        ----------
        func : function
            Conversion function.
        default : any, optional
            Value to return by default, that is, when the string to be
            converted is flagged as missing. If not given,
            `StringConverter` tries to supply a reasonable default value.
        testing_value : str, optional
            A string representing a standard input value of the converter.
            This string is used to help defining a reasonable default
            value.
        missing_values : {sequence of str, None}, optional
            Sequence of strings indicating a missing value. If ``None``, then
            the existing `missing_values` are cleared. The default is `''`.
        locked : bool, optional
            Whether the StringConverter should be locked to prevent
            automatic upgrade or not. Default is False.

        Notes
        -----
        `update` takes the same parameters as the constructor of
        `StringConverter`, except that `func` does not accept a `dtype`
        whereas `dtype_or_func` in the constructor does.

        """
        self.func = func
        self._locked = locked
        if default is not None:
            self.default = default
            self.type = self._dtypeortype(self._getdtype(default))
        else:
            try:
                tester = func(testing_value or '1')
            except (TypeError, ValueError):
                tester = None
            else:
                self.type = self._dtypeortype(self._getdtype(tester))
            if missing_values is None:
                self.missing_values = set()
            else:
                if not np.iterable(missing_values):
                    missing_values = [
                     missing_values]
                if not all((isinstance(v, str) for v in missing_values)):
                    raise TypeError('missing_values must be strings or unicode')
                self.missing_values.update(missing_values)


def easy_dtype(ndtype, names=None, defaultfmt='f%i', **validationargs):
    """
    Convenience function to create a `np.dtype` object.

    The function processes the input `dtype` and matches it with the given
    names.

    Parameters
    ----------
    ndtype : var
        Definition of the dtype. Can be any string or dictionary recognized
        by the `np.dtype` function, or a sequence of types.
    names : str or sequence, optional
        Sequence of strings to use as field names for a structured dtype.
        For convenience, `names` can be a string of a comma-separated list
        of names.
    defaultfmt : str, optional
        Format string used to define missing names, such as ``"f%i"``
        (default) or ``"fields_%02i"``.
    validationargs : optional
        A series of optional arguments used to initialize a
        `NameValidator`.

    Examples
    --------
    >>> np.lib._iotools.easy_dtype(float)
    dtype('float64')
    >>> np.lib._iotools.easy_dtype("i4, f8")
    dtype([('f0', '<i4'), ('f1', '<f8')])
    >>> np.lib._iotools.easy_dtype("i4, f8", defaultfmt="field_%03i")
    dtype([('field_000', '<i4'), ('field_001', '<f8')])

    >>> np.lib._iotools.easy_dtype((int, float, float), names="a,b,c")
    dtype([('a', '<i8'), ('b', '<f8'), ('c', '<f8')])
    >>> np.lib._iotools.easy_dtype(float, names="a,b,c")
    dtype([('a', '<f8'), ('b', '<f8'), ('c', '<f8')])

    """
    try:
        ndtype = np.dtype(ndtype)
    except TypeError:
        validate = NameValidator(**validationargs)
        nbfields = len(ndtype)
        if names is None:
            names = [
             ''] * len(ndtype)
        else:
            if isinstance(names, str):
                names = names.split(',')
        names = validate(names, nbfields=nbfields, defaultfmt=defaultfmt)
        ndtype = np.dtype(dict(formats=ndtype, names=names))
    else:
        if names is not None:
            validate = NameValidator(**validationargs)
            if isinstance(names, str):
                names = names.split(',')
            elif ndtype.names is None:
                formats = tuple([ndtype.type] * len(names))
                names = validate(names, defaultfmt=defaultfmt)
                ndtype = np.dtype(list(zip(names, formats)))
            else:
                ndtype.names = validate(names, nbfields=(len(ndtype.names)), defaultfmt=defaultfmt)
        else:
            if ndtype.names is not None:
                validate = NameValidator(**validationargs)
                numbered_names = tuple(('f%i' % i for i in range(len(ndtype.names))))
                if ndtype.names == numbered_names and defaultfmt != 'f%i':
                    ndtype.names = validate(([''] * len(ndtype.names)), defaultfmt=defaultfmt)
                else:
                    ndtype.names = validate((ndtype.names), defaultfmt=defaultfmt)
            return ndtype