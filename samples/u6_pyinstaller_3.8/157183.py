# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\core\records.py
"""
Record Arrays
=============
Record arrays expose the fields of structured arrays as properties.

Most commonly, ndarrays contain elements of a single type, e.g. floats,
integers, bools etc.  However, it is possible for elements to be combinations
of these using structured types, such as::

  >>> a = np.array([(1, 2.0), (1, 2.0)], dtype=[('x', np.int64), ('y', np.float64)])
  >>> a
  array([(1, 2.), (1, 2.)], dtype=[('x', '<i8'), ('y', '<f8')])

Here, each element consists of two fields: x (and int), and y (a float).
This is known as a structured array.  The different fields are analogous
to columns in a spread-sheet.  The different fields can be accessed as
one would a dictionary::

  >>> a['x']
  array([1, 1])

  >>> a['y']
  array([2., 2.])

Record arrays allow us to access fields as properties::

  >>> ar = np.rec.array(a)

  >>> ar.x
  array([1, 1])

  >>> ar.y
  array([2., 2.])

"""
import os, warnings
from collections import Counter, OrderedDict
from . import numeric as sb
from . import numerictypes as nt
from numpy.compat import os_fspath, contextlib_nullcontext
from numpy.core.overrides import set_module
from .arrayprint import get_printoptions
__all__ = [
 'record', 'recarray', 'format_parser']
ndarray = sb.ndarray
_byteorderconv = {'b':'>', 
 'l':'<', 
 'n':'=', 
 'B':'>', 
 'L':'<', 
 'N':'=', 
 'S':'s', 
 's':'s', 
 '>':'>', 
 '<':'<', 
 '=':'=', 
 '|':'|', 
 'I':'|', 
 'i':'|'}
numfmt = nt.typeDict

class _OrderedCounter(Counter, OrderedDict):
    __doc__ = 'Counter that remembers the order elements are first encountered'

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return (
         self.__class__, (OrderedDict(self),))


def find_duplicate(list):
    """Find duplication in a list, return a list of duplicated elements"""
    return [item for item, counts in _OrderedCounter(list).items() if counts > 1]


@set_module('numpy')
class format_parser:
    __doc__ = "\n    Class to convert formats, names, titles description to a dtype.\n\n    After constructing the format_parser object, the dtype attribute is\n    the converted data-type:\n    ``dtype = format_parser(formats, names, titles).dtype``\n\n    Attributes\n    ----------\n    dtype : dtype\n        The converted data-type.\n\n    Parameters\n    ----------\n    formats : str or list of str\n        The format description, either specified as a string with\n        comma-separated format descriptions in the form ``'f8, i4, a5'``, or\n        a list of format description strings  in the form\n        ``['f8', 'i4', 'a5']``.\n    names : str or list/tuple of str\n        The field names, either specified as a comma-separated string in the\n        form ``'col1, col2, col3'``, or as a list or tuple of strings in the\n        form ``['col1', 'col2', 'col3']``.\n        An empty list can be used, in that case default field names\n        ('f0', 'f1', ...) are used.\n    titles : sequence\n        Sequence of title strings. An empty list can be used to leave titles\n        out.\n    aligned : bool, optional\n        If True, align the fields by padding as the C-compiler would.\n        Default is False.\n    byteorder : str, optional\n        If specified, all the fields will be changed to the\n        provided byte-order.  Otherwise, the default byte-order is\n        used. For all available string specifiers, see `dtype.newbyteorder`.\n\n    See Also\n    --------\n    dtype, typename, sctype2char\n\n    Examples\n    --------\n    >>> np.format_parser(['<f8', '<i4', '<a5'], ['col1', 'col2', 'col3'],\n    ...                  ['T1', 'T2', 'T3']).dtype\n    dtype([(('T1', 'col1'), '<f8'), (('T2', 'col2'), '<i4'), (('T3', 'col3'), 'S5')])\n\n    `names` and/or `titles` can be empty lists. If `titles` is an empty list,\n    titles will simply not appear. If `names` is empty, default field names\n    will be used.\n\n    >>> np.format_parser(['f8', 'i4', 'a5'], ['col1', 'col2', 'col3'],\n    ...                  []).dtype\n    dtype([('col1', '<f8'), ('col2', '<i4'), ('col3', '<S5')])\n    >>> np.format_parser(['<f8', '<i4', '<a5'], [], []).dtype\n    dtype([('f0', '<f8'), ('f1', '<i4'), ('f2', 'S5')])\n\n    "

    def __init__(self, formats, names, titles, aligned=False, byteorder=None):
        self._parseFormats(formats, aligned)
        self._setfieldnames(names, titles)
        self._createdtype(byteorder)

    def _parseFormats(self, formats, aligned=False):
        """ Parse the field formats """
        if formats is None:
            raise ValueError('Need formats argument')
        elif isinstance(formats, list):
            dtype = sb.dtype([(
             'f{}'.format(i), format_) for i, format_ in enumerate(formats)], aligned)
        else:
            dtype = sb.dtype(formats, aligned)
        fields = dtype.fields
        if fields is None:
            dtype = sb.dtype([('f1', dtype)], aligned)
            fields = dtype.fields
        keys = dtype.names
        self._f_formats = [fields[key][0] for key in keys]
        self._offsets = [fields[key][1] for key in keys]
        self._nfields = len(keys)

    def _setfieldnames(self, names, titles):
        """convert input field names into a list and assign to the _names
        attribute """
        if names:
            if type(names) in (list, tuple):
                pass
            elif isinstance(names, str):
                names = names.split(',')
            else:
                raise NameError('illegal input names %s' % repr(names))
            self._names = [n.strip() for n in names[:self._nfields]]
        else:
            self._names = []
        self._names += ['f%d' % i for i in range(len(self._names), self._nfields)]
        _dup = find_duplicate(self._names)
        if _dup:
            raise ValueError('Duplicate field names: %s' % _dup)
        elif titles:
            self._titles = [n.strip() for n in titles[:self._nfields]]
        else:
            self._titles = []
            titles = []
        if self._nfields > len(titles):
            self._titles += [None] * (self._nfields - len(titles))

    def _createdtype(self, byteorder):
        dtype = sb.dtype({'names':self._names, 
         'formats':self._f_formats, 
         'offsets':self._offsets, 
         'titles':self._titles})
        if byteorder is not None:
            byteorder = _byteorderconv[byteorder[0]]
            dtype = dtype.newbyteorder(byteorder)
        self.dtype = dtype


class record(nt.void):
    __doc__ = 'A data-type scalar that allows field access as attribute lookup.\n    '
    __name__ = 'record'
    __module__ = 'numpy'

    def __repr__(self):
        if get_printoptions()['legacy'] == '1.13':
            return self.__str__()
        return super(record, self).__repr__()

    def __str__(self):
        if get_printoptions()['legacy'] == '1.13':
            return str(self.item())
        return super(record, self).__str__()

    def __getattribute__--- This code section failed: ---

 L. 253         0  LOAD_FAST                'attr'
                2  LOAD_CONST               ('setfield', 'getfield', 'dtype')
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 254         8  LOAD_GLOBAL              nt
               10  LOAD_ATTR                void
               12  LOAD_METHOD              __getattribute__
               14  LOAD_FAST                'self'
               16  LOAD_FAST                'attr'
               18  CALL_METHOD_2         2  ''
               20  RETURN_VALUE     
             22_0  COME_FROM             6  '6'

 L. 255        22  SETUP_FINALLY        40  'to 40'

 L. 256        24  LOAD_GLOBAL              nt
               26  LOAD_ATTR                void
               28  LOAD_METHOD              __getattribute__
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'attr'
               34  CALL_METHOD_2         2  ''
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    22  '22'

 L. 257        40  DUP_TOP          
               42  LOAD_GLOBAL              AttributeError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    58  'to 58'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 258        54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            46  '46'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'

 L. 259        60  LOAD_GLOBAL              nt
               62  LOAD_ATTR                void
               64  LOAD_METHOD              __getattribute__
               66  LOAD_FAST                'self'
               68  LOAD_STR                 'dtype'
               70  CALL_METHOD_2         2  ''
               72  LOAD_ATTR                fields
               74  STORE_FAST               'fielddict'

 L. 260        76  LOAD_FAST                'fielddict'
               78  LOAD_METHOD              get
               80  LOAD_FAST                'attr'
               82  LOAD_CONST               None
               84  CALL_METHOD_2         2  ''
               86  STORE_FAST               'res'

 L. 261        88  LOAD_FAST                'res'
               90  POP_JUMP_IF_FALSE   178  'to 178'

 L. 262        92  LOAD_FAST                'self'
               94  LOAD_ATTR                getfield
               96  LOAD_FAST                'res'
               98  LOAD_CONST               None
              100  LOAD_CONST               2
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  CALL_FUNCTION_EX      0  'positional arguments only'
              108  STORE_FAST               'obj'

 L. 265       110  SETUP_FINALLY       122  'to 122'

 L. 266       112  LOAD_FAST                'obj'
              114  LOAD_ATTR                dtype
              116  STORE_FAST               'dt'
              118  POP_BLOCK        
              120  JUMP_FORWARD        146  'to 146'
            122_0  COME_FROM_FINALLY   110  '110'

 L. 267       122  DUP_TOP          
              124  LOAD_GLOBAL              AttributeError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   144  'to 144'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 269       136  LOAD_FAST                'obj'
              138  ROT_FOUR         
              140  POP_EXCEPT       
              142  RETURN_VALUE     
            144_0  COME_FROM           128  '128'
              144  END_FINALLY      
            146_0  COME_FROM           120  '120'

 L. 270       146  LOAD_FAST                'dt'
              148  LOAD_ATTR                names
              150  LOAD_CONST               None
              152  COMPARE_OP               is-not
              154  POP_JUMP_IF_FALSE   174  'to 174'

 L. 271       156  LOAD_FAST                'obj'
              158  LOAD_METHOD              view
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                __class__
              164  LOAD_FAST                'obj'
              166  LOAD_ATTR                dtype
              168  BUILD_TUPLE_2         2 
              170  CALL_METHOD_1         1  ''
              172  RETURN_VALUE     
            174_0  COME_FROM           154  '154'

 L. 272       174  LOAD_FAST                'obj'
              176  RETURN_VALUE     
            178_0  COME_FROM            90  '90'

 L. 274       178  LOAD_GLOBAL              AttributeError
              180  LOAD_STR                 "'record' object has no attribute '%s'"

 L. 275       182  LOAD_FAST                'attr'

 L. 274       184  BINARY_MODULO    
              186  CALL_FUNCTION_1       1  ''
              188  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 50

    def __setattr__(self, attr, val):
        if attr in ('setfield', 'getfield', 'dtype'):
            raise AttributeError("Cannot set '%s' attribute" % attr)
        fielddict = nt.void.__getattribute__(self, 'dtype').fields
        res = fielddict.get(attr, None)
        if res:
            return (self.setfield)(val, *res[:2])
        if getattr(self, attr, None):
            return nt.void.__setattr__(self, attr, val)
        raise AttributeError("'record' object has no attribute '%s'" % attr)

    def __getitem__(self, indx):
        obj = nt.void.__getitem__(self, indx)
        if isinstance(obj, nt.void):
            if obj.dtype.names is not None:
                return obj.view((self.__class__, obj.dtype))
        return obj

    def pprint(self):
        """Pretty-print all fields."""
        names = self.dtype.names
        maxlen = max((len(name) for name in names))
        fmt = '%% %ds: %%s' % maxlen
        rows = [fmt % (name, getattr(self, name)) for name in names]
        return '\n'.join(rows)


class recarray(ndarray):
    __doc__ = "Construct an ndarray that allows field access using attributes.\n\n    Arrays may have a data-types containing fields, analogous\n    to columns in a spread sheet.  An example is ``[(x, int), (y, float)]``,\n    where each entry in the array is a pair of ``(int, float)``.  Normally,\n    these attributes are accessed using dictionary lookups such as ``arr['x']``\n    and ``arr['y']``.  Record arrays allow the fields to be accessed as members\n    of the array, using ``arr.x`` and ``arr.y``.\n\n    Parameters\n    ----------\n    shape : tuple\n        Shape of output array.\n    dtype : data-type, optional\n        The desired data-type.  By default, the data-type is determined\n        from `formats`, `names`, `titles`, `aligned` and `byteorder`.\n    formats : list of data-types, optional\n        A list containing the data-types for the different columns, e.g.\n        ``['i4', 'f8', 'i4']``.  `formats` does *not* support the new\n        convention of using types directly, i.e. ``(int, float, int)``.\n        Note that `formats` must be a list, not a tuple.\n        Given that `formats` is somewhat limited, we recommend specifying\n        `dtype` instead.\n    names : tuple of str, optional\n        The name of each column, e.g. ``('x', 'y', 'z')``.\n    buf : buffer, optional\n        By default, a new array is created of the given shape and data-type.\n        If `buf` is specified and is an object exposing the buffer interface,\n        the array will use the memory from the existing buffer.  In this case,\n        the `offset` and `strides` keywords are available.\n\n    Other Parameters\n    ----------------\n    titles : tuple of str, optional\n        Aliases for column names.  For example, if `names` were\n        ``('x', 'y', 'z')`` and `titles` is\n        ``('x_coordinate', 'y_coordinate', 'z_coordinate')``, then\n        ``arr['x']`` is equivalent to both ``arr.x`` and ``arr.x_coordinate``.\n    byteorder : {'<', '>', '='}, optional\n        Byte-order for all fields.\n    aligned : bool, optional\n        Align the fields in memory as the C-compiler would.\n    strides : tuple of ints, optional\n        Buffer (`buf`) is interpreted according to these strides (strides\n        define how many bytes each array element, row, column, etc.\n        occupy in memory).\n    offset : int, optional\n        Start reading buffer (`buf`) from this offset onwards.\n    order : {'C', 'F'}, optional\n        Row-major (C-style) or column-major (Fortran-style) order.\n\n    Returns\n    -------\n    rec : recarray\n        Empty array of the given shape and type.\n\n    See Also\n    --------\n    core.records.fromrecords : Construct a record array from data.\n    record : fundamental data-type for `recarray`.\n    format_parser : determine a data-type from formats, names, titles.\n\n    Notes\n    -----\n    This constructor can be compared to ``empty``: it creates a new record\n    array but does not fill it with data.  To create a record array from data,\n    use one of the following methods:\n\n    1. Create a standard ndarray and convert it to a record array,\n       using ``arr.view(np.recarray)``\n    2. Use the `buf` keyword.\n    3. Use `np.rec.fromrecords`.\n\n    Examples\n    --------\n    Create an array with two fields, ``x`` and ``y``:\n\n    >>> x = np.array([(1.0, 2), (3.0, 4)], dtype=[('x', '<f8'), ('y', '<i8')])\n    >>> x\n    array([(1., 2), (3., 4)], dtype=[('x', '<f8'), ('y', '<i8')])\n\n    >>> x['x']\n    array([1., 3.])\n\n    View the array as a record array:\n\n    >>> x = x.view(np.recarray)\n\n    >>> x.x\n    array([1., 3.])\n\n    >>> x.y\n    array([2, 4])\n\n    Create a new, empty record array:\n\n    >>> np.recarray((2,),\n    ... dtype=[('x', int), ('y', float), ('z', int)]) #doctest: +SKIP\n    rec.array([(-1073741821, 1.2249118382103472e-301, 24547520),\n           (3471280, 1.2134086255804012e-316, 0)],\n          dtype=[('x', '<i4'), ('y', '<f8'), ('z', '<i4')])\n\n    "
    __name__ = 'recarray'
    __module__ = 'numpy'

    def __new__(subtype, shape, dtype=None, buf=None, offset=0, strides=None, formats=None, names=None, titles=None, byteorder=None, aligned=False, order='C'):
        if dtype is not None:
            descr = sb.dtype(dtype)
        else:
            descr = format_parser(formats, names, titles, aligned, byteorder).dtype
        if buf is None:
            self = ndarray.__new__(subtype, shape, (record, descr), order=order)
        else:
            self = ndarray.__new__(subtype, shape, (record, descr), buffer=buf,
              offset=offset,
              strides=strides,
              order=order)
        return self

    def __array_finalize__(self, obj):
        if self.dtype.type is not record:
            if self.dtype.names is not None:
                self.dtype = self.dtype

    def __getattribute__--- This code section failed: ---

 L. 455         0  SETUP_FINALLY        16  'to 16'

 L. 456         2  LOAD_GLOBAL              object
                4  LOAD_METHOD              __getattribute__
                6  LOAD_FAST                'self'
                8  LOAD_FAST                'attr'
               10  CALL_METHOD_2         2  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 457        16  DUP_TOP          
               18  LOAD_GLOBAL              AttributeError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    34  'to 34'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 458        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
             34_0  COME_FROM            22  '22'
               34  END_FINALLY      
             36_0  COME_FROM            32  '32'

 L. 461        36  LOAD_GLOBAL              ndarray
               38  LOAD_METHOD              __getattribute__
               40  LOAD_FAST                'self'
               42  LOAD_STR                 'dtype'
               44  CALL_METHOD_2         2  ''
               46  LOAD_ATTR                fields
               48  STORE_FAST               'fielddict'

 L. 462        50  SETUP_FINALLY        72  'to 72'

 L. 463        52  LOAD_FAST                'fielddict'
               54  LOAD_FAST                'attr'
               56  BINARY_SUBSCR    
               58  LOAD_CONST               None
               60  LOAD_CONST               2
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  STORE_FAST               'res'
               68  POP_BLOCK        
               70  JUMP_FORWARD        124  'to 124'
             72_0  COME_FROM_FINALLY    50  '50'

 L. 464        72  DUP_TOP          
               74  LOAD_GLOBAL              TypeError
               76  LOAD_GLOBAL              KeyError
               78  BUILD_TUPLE_2         2 
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   122  'to 122'
               84  POP_TOP          
               86  STORE_FAST               'e'
               88  POP_TOP          
               90  SETUP_FINALLY       110  'to 110'

 L. 465        92  LOAD_GLOBAL              AttributeError
               94  LOAD_STR                 'recarray has no attribute %s'
               96  LOAD_FAST                'attr'
               98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_FAST                'e'
              104  RAISE_VARARGS_2       2  'exception instance with __cause__'
              106  POP_BLOCK        
              108  BEGIN_FINALLY    
            110_0  COME_FROM_FINALLY    90  '90'
              110  LOAD_CONST               None
              112  STORE_FAST               'e'
              114  DELETE_FAST              'e'
              116  END_FINALLY      
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM            82  '82'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            70  '70'

 L. 466       124  LOAD_FAST                'self'
              126  LOAD_ATTR                getfield
              128  LOAD_FAST                'res'
              130  CALL_FUNCTION_EX      0  'positional arguments only'
              132  STORE_FAST               'obj'

 L. 474       134  LOAD_FAST                'obj'
              136  LOAD_ATTR                dtype
              138  LOAD_ATTR                names
              140  LOAD_CONST               None
              142  COMPARE_OP               is-not
              144  POP_JUMP_IF_FALSE   188  'to 188'

 L. 475       146  LOAD_GLOBAL              issubclass
              148  LOAD_FAST                'obj'
              150  LOAD_ATTR                dtype
              152  LOAD_ATTR                type
              154  LOAD_GLOBAL              nt
              156  LOAD_ATTR                void
              158  CALL_FUNCTION_2       2  ''
              160  POP_JUMP_IF_FALSE   184  'to 184'

 L. 476       162  LOAD_FAST                'obj'
              164  LOAD_ATTR                view
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                dtype
              170  LOAD_ATTR                type
              172  LOAD_FAST                'obj'
              174  LOAD_ATTR                dtype
              176  BUILD_TUPLE_2         2 
              178  LOAD_CONST               ('dtype',)
              180  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              182  RETURN_VALUE     
            184_0  COME_FROM           160  '160'

 L. 477       184  LOAD_FAST                'obj'
              186  RETURN_VALUE     
            188_0  COME_FROM           144  '144'

 L. 479       188  LOAD_FAST                'obj'
              190  LOAD_METHOD              view
              192  LOAD_GLOBAL              ndarray
              194  CALL_METHOD_1         1  ''
              196  RETURN_VALUE     

Parse error at or near `POP_TOP' instruction at offset 26

    def __setattr__(self, attr, val):
        if attr == 'dtype':
            if issubclass(val.type, nt.void):
                if val.names is not None:
                    val = sb.dtype((record, val))
        newattr = attr not in self.__dict__
        try:
            ret = object.__setattr__(self, attr, val)
        except Exception:
            fielddict = ndarray.__getattribute__(self, 'dtype').fields or {}
            if attr not in fielddict:
                raise
        else:
            fielddict = ndarray.__getattribute__(self, 'dtype').fields or {}
            if attr not in fielddict:
                return ret
                if newattr:
                    try:
                        object.__delattr__(self, attr)
                    except Exception:
                        return ret

            else:
                try:
                    res = fielddict[attr][:2]
                except (TypeError, KeyError) as e:
                    try:
                        raise AttributeError('record array has no attribute %s' % attr) from e
                    finally:
                        e = None
                        del e

            return (self.setfield)(val, *res)

    def __getitem__(self, indx):
        obj = super(recarray, self).__getitem__(indx)
        if isinstance(obj, ndarray):
            if obj.dtype.names is not None:
                obj = obj.view(type(self))
                if issubclass(obj.dtype.type, nt.void):
                    return obj.view(dtype=(self.dtype.type, obj.dtype))
                return obj
            return obj.view(type=ndarray)
        else:
            return obj

    def __repr__(self):
        repr_dtype = self.dtype
        if not self.dtype.type is record:
            if not issubclass(self.dtype.type, nt.void):
                if repr_dtype.type is record:
                    repr_dtype = sb.dtype((nt.void, repr_dtype))
                prefix = 'rec.array('
                fmt = 'rec.array(%s,%sdtype=%s)'
        else:
            prefix = 'array('
            fmt = 'array(%s,%sdtype=%s).view(numpy.recarray)'
        if self.size > 0 or self.shape == (0, ):
            lst = sb.array2string(self,
              separator=', ', prefix=prefix, suffix=',')
        else:
            lst = '[], shape=%s' % (repr(self.shape),)
        lf = '\n' + ' ' * len(prefix)
        if get_printoptions()['legacy'] == '1.13':
            lf = ' ' + lf
        return fmt % (lst, lf, repr_dtype)

    def field(self, attr, val=None):
        if isinstance(attr, int):
            names = ndarray.__getattribute__(self, 'dtype').names
            attr = names[attr]
        fielddict = ndarray.__getattribute__(self, 'dtype').fields
        res = fielddict[attr][:2]
        if val is None:
            obj = (self.getfield)(*res)
            if obj.dtype.names is not None:
                return obj
            return obj.view(ndarray)
        return (self.setfield)(val, *res)


def _deprecate_shape_0_as_None(shape):
    if shape == 0:
        warnings.warn('Passing `shape=0` to have the shape be inferred is deprecated, and in future will be equivalent to `shape=(0,)`. To infer the shape and suppress this warning, pass `shape=None` instead.',
          FutureWarning,
          stacklevel=3)
        return
    return shape


def fromarrays(arrayList, dtype=None, shape=None, formats=None, names=None, titles=None, aligned=False, byteorder=None):
    """Create a record array from a (flat) list of arrays

    Parameters
    ----------
    arrayList : list or tuple
        List of array-like objects (such as lists, tuples,
        and ndarrays).
    dtype : data-type, optional
        valid dtype for all arrays
    shape : int or tuple of ints, optional
        Shape of the resulting array. If not provided, inferred from
        ``arrayList[0]``.
    formats, names, titles, aligned, byteorder :
        If `dtype` is ``None``, these arguments are passed to
        `numpy.format_parser` to construct a dtype. See that function for
        detailed documentation.

    Returns
    -------
    np.recarray
        Record array consisting of given arrayList columns.

    Examples
    --------
    >>> x1=np.array([1,2,3,4])
    >>> x2=np.array(['a','dd','xyz','12'])
    >>> x3=np.array([1.1,2,3,4])
    >>> r = np.core.records.fromarrays([x1,x2,x3],names='a,b,c')
    >>> print(r[1])
    (2, 'dd', 2.0) # may vary
    >>> x1[1]=34
    >>> r.a
    array([1, 2, 3, 4])

    >>> x1 = np.array([1, 2, 3, 4])
    >>> x2 = np.array(['a', 'dd', 'xyz', '12'])
    >>> x3 = np.array([1.1, 2, 3,4])
    >>> r = np.core.records.fromarrays(
    ...     [x1, x2, x3],
    ...     dtype=np.dtype([('a', np.int32), ('b', 'S3'), ('c', np.float32)]))
    >>> r
    rec.array([(1, b'a', 1.1), (2, b'dd', 2. ), (3, b'xyz', 3. ),
               (4, b'12', 4. )],
              dtype=[('a', '<i4'), ('b', 'S3'), ('c', '<f4')])
    """
    arrayList = [sb.asarray(x) for x in arrayList]
    shape = _deprecate_shape_0_as_None(shape)
    if shape is None:
        shape = arrayList[0].shape
    else:
        if isinstance(shape, int):
            shape = (
             shape,)
        else:
            if formats is None:
                if dtype is None:
                    formats = [obj.dtype for obj in arrayList]
            if dtype is not None:
                descr = sb.dtype(dtype)
            else:
                descr = format_parser(formats, names, titles, aligned, byteorder).dtype
        _names = descr.names
        if len(descr) != len(arrayList):
            raise ValueError('mismatch between the number of fields and the number of arrays')
        d0 = descr[0].shape
        nn = len(d0)
        if nn > 0:
            shape = shape[:-nn]
        for k, obj in enumerate(arrayList):
            nn = descr[k].ndim
            testshape = obj.shape[:obj.ndim - nn]
            if testshape != shape:
                raise ValueError('array-shape mismatch in array %d' % k)
            _array = recarray(shape, descr)
            for i in range(len(arrayList)):
                _array[_names[i]] = arrayList[i]
            else:
                return _array


def fromrecords(recList, dtype=None, shape=None, formats=None, names=None, titles=None, aligned=False, byteorder=None):
    """Create a recarray from a list of records in text form.

    Parameters
    ----------
    recList : sequence
        data in the same field may be heterogeneous - they will be promoted
        to the highest data type.
    dtype : data-type, optional
        valid dtype for all arrays
    shape : int or tuple of ints, optional
        shape of each array.
    formats, names, titles, aligned, byteorder :
        If `dtype` is ``None``, these arguments are passed to
        `numpy.format_parser` to construct a dtype. See that function for
        detailed documentation.

        If both `formats` and `dtype` are None, then this will auto-detect
        formats. Use list of tuples rather than list of lists for faster
        processing.

    Returns
    -------
    np.recarray
        record array consisting of given recList rows.

    Examples
    --------
    >>> r=np.core.records.fromrecords([(456,'dbe',1.2),(2,'de',1.3)],
    ... names='col1,col2,col3')
    >>> print(r[0])
    (456, 'dbe', 1.2)
    >>> r.col1
    array([456,   2])
    >>> r.col2
    array(['dbe', 'de'], dtype='<U3')
    >>> import pickle
    >>> pickle.loads(pickle.dumps(r))
    rec.array([(456, 'dbe', 1.2), (  2, 'de', 1.3)],
              dtype=[('col1', '<i8'), ('col2', '<U3'), ('col3', '<f8')])
    """
    if formats is None:
        if dtype is None:
            obj = sb.array(recList, dtype=object)
            arrlist = [sb.array(obj[(..., i)].tolist()) for i in range(obj.shape[(-1)])]
            return fromarrays(arrlist, formats=formats, shape=shape, names=names, titles=titles,
              aligned=aligned,
              byteorder=byteorder)
    elif dtype is not None:
        descr = sb.dtype((record, dtype))
    else:
        descr = format_parser(formats, names, titles, aligned, byteorder).dtype
    try:
        retval = sb.array(recList, dtype=descr)
    except (TypeError, ValueError):
        shape = _deprecate_shape_0_as_None(shape)
        if shape is None:
            shape = len(recList)
        if isinstance(shape, int):
            shape = (
             shape,)
        if len(shape) > 1:
            raise ValueError('Can only deal with 1-d array.')
        _array = recarray(shape, descr)
        for k in range(_array.size):
            _array[k] = tuple(recList[k])
        else:
            warnings.warn('fromrecords expected a list of tuples, may have received a list of lists instead. In the future that will raise an error',
              FutureWarning,
              stacklevel=2)

        return _array
    else:
        if shape is not None:
            if retval.shape != shape:
                retval.shape = shape
        res = retval.view(recarray)
        return res


def fromstring(datastring, dtype=None, shape=None, offset=0, formats=None, names=None, titles=None, aligned=False, byteorder=None):
    r"""Create a record array from binary data

    Note that despite the name of this function it does not accept `str`
    instances.

    Parameters
    ----------
    datastring : bytes-like
        Buffer of binary data
    dtype : data-type, optional
        Valid dtype for all arrays
    shape : int or tuple of ints, optional
        Shape of each array.
    offset : int, optional
        Position in the buffer to start reading from.
    formats, names, titles, aligned, byteorder :
        If `dtype` is ``None``, these arguments are passed to
        `numpy.format_parser` to construct a dtype. See that function for
        detailed documentation.

    Returns
    -------
    np.recarray
        Record array view into the data in datastring. This will be readonly
        if `datastring` is readonly.

    See Also
    --------
    numpy.frombuffer

    Examples
    --------
    >>> a = b'\x01\x02\x03abc'
    >>> np.core.records.fromstring(a, dtype='u1,u1,u1,S3')
    rec.array([(1, 2, 3, b'abc')],
            dtype=[('f0', 'u1'), ('f1', 'u1'), ('f2', 'u1'), ('f3', 'S3')])

    >>> grades_dtype = [('Name', (np.str_, 10)), ('Marks', np.float64),
    ...                 ('GradeLevel', np.int32)]
    >>> grades_array = np.array([('Sam', 33.3, 3), ('Mike', 44.4, 5),
    ...                         ('Aadi', 66.6, 6)], dtype=grades_dtype)
    >>> np.core.records.fromstring(grades_array.tobytes(), dtype=grades_dtype)
    rec.array([('Sam', 33.3, 3), ('Mike', 44.4, 5), ('Aadi', 66.6, 6)],
            dtype=[('Name', '<U10'), ('Marks', '<f8'), ('GradeLevel', '<i4')])

    >>> s = '\x01\x02\x03abc'
    >>> np.core.records.fromstring(s, dtype='u1,u1,u1,S3')
    Traceback (most recent call last)
       ...
    TypeError: a bytes-like object is required, not 'str'
    """
    if dtype is None:
        if formats is None:
            raise TypeError("fromstring() needs a 'dtype' or 'formats' argument")
    elif dtype is not None:
        descr = sb.dtype(dtype)
    else:
        descr = format_parser(formats, names, titles, aligned, byteorder).dtype
    itemsize = descr.itemsize
    shape = _deprecate_shape_0_as_None(shape)
    if shape in (None, -1):
        shape = (len(datastring) - offset) // itemsize
    _array = recarray(shape, descr, buf=datastring, offset=offset)
    return _array


def get_remaining_size--- This code section failed: ---

 L. 850         0  LOAD_FAST                'fd'
                2  LOAD_METHOD              tell
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'pos'

 L. 851         8  SETUP_FINALLY        38  'to 38'

 L. 852        10  LOAD_FAST                'fd'
               12  LOAD_METHOD              seek
               14  LOAD_CONST               0
               16  LOAD_CONST               2
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          

 L. 853        22  LOAD_FAST                'fd'
               24  LOAD_METHOD              tell
               26  CALL_METHOD_0         0  ''
               28  LOAD_FAST                'pos'
               30  BINARY_SUBTRACT  
               32  POP_BLOCK        
               34  CALL_FINALLY         38  'to 38'
               36  RETURN_VALUE     
             38_0  COME_FROM            34  '34'
             38_1  COME_FROM_FINALLY     8  '8'

 L. 855        38  LOAD_FAST                'fd'
               40  LOAD_METHOD              seek
               42  LOAD_FAST                'pos'
               44  LOAD_CONST               0
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          
               50  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 34


def fromfile(fd, dtype=None, shape=None, offset=0, formats=None, names=None, titles=None, aligned=False, byteorder=None):
    """Create an array from binary file data

    Parameters
    ----------
    fd : str or file type
        If file is a string or a path-like object then that file is opened,
        else it is assumed to be a file object. The file object must
        support random access (i.e. it must have tell and seek methods).
    dtype : data-type, optional
        valid dtype for all arrays
    shape : int or tuple of ints, optional
        shape of each array.
    offset : int, optional
        Position in the file to start reading from.
    formats, names, titles, aligned, byteorder :
        If `dtype` is ``None``, these arguments are passed to
        `numpy.format_parser` to construct a dtype. See that function for
        detailed documentation

    Returns
    -------
    np.recarray
        record array consisting of data enclosed in file.

    Examples
    --------
    >>> from tempfile import TemporaryFile
    >>> a = np.empty(10,dtype='f8,i4,a5')
    >>> a[5] = (0.5,10,'abcde')
    >>>
    >>> fd=TemporaryFile()
    >>> a = a.newbyteorder('<')
    >>> a.tofile(fd)
    >>>
    >>> _ = fd.seek(0)
    >>> r=np.core.records.fromfile(fd, formats='f8,i4,a5', shape=10,
    ... byteorder='<')
    >>> print(r[5])
    (0.5, 10, 'abcde')
    >>> r.shape
    (10,)
    """
    if dtype is None:
        if formats is None:
            raise TypeError("fromfile() needs a 'dtype' or 'formats' argument")
    shape = _deprecate_shape_0_as_None(shape)
    if shape is None:
        shape = (-1, )
    else:
        if isinstance(shape, int):
            shape = (
             shape,)
        elif hasattr(fd, 'readinto'):
            ctx = contextlib_nullcontext(fd)
        else:
            ctx = open(os_fspath(fd), 'rb')
        with ctx as (fd):
            if offset > 0:
                fd.seek(offset, 1)
            else:
                size = get_remaining_size(fd)
                if dtype is not None:
                    descr = sb.dtype(dtype)
                else:
                    descr = format_parser(formats, names, titles, aligned, byteorder).dtype
            itemsize = descr.itemsize
            shapeprod = sb.array(shape).prod(dtype=(nt.intp))
            shapesize = shapeprod * itemsize
            if shapesize < 0:
                shape = list(shape)
                shape[shape.index(-1)] = size // -shapesize
                shape = tuple(shape)
                shapeprod = sb.array(shape).prod(dtype=(nt.intp))
            nbytes = shapeprod * itemsize
            if nbytes > size:
                raise ValueError('Not enough bytes left in file for specified shape and type')
            _array = recarray(shape, descr)
            nbytesread = fd.readinto(_array.data)
            if nbytesread != nbytes:
                raise IOError("Didn't read as many bytes as expected")
        return _array


def array(obj, dtype=None, shape=None, offset=0, strides=None, formats=None, names=None, titles=None, aligned=False, byteorder=None, copy=True):
    """
    Construct a record array from a wide-variety of objects.

    A general-purpose record array constructor that dispatches to the
    appropriate `recarray` creation function based on the inputs (see Notes).

    Parameters
    ----------
    obj: any
        Input object. See Notes for details on how various input types are
        treated.
    dtype: data-type, optional
        Valid dtype for array.
    shape: int or tuple of ints, optional
        Shape of each array.
    offset: int, optional
        Position in the file or buffer to start reading from.
    strides: tuple of ints, optional
        Buffer (`buf`) is interpreted according to these strides (strides
        define how many bytes each array element, row, column, etc.
        occupy in memory).
    formats, names, titles, aligned, byteorder :
        If `dtype` is ``None``, these arguments are passed to
        `numpy.format_parser` to construct a dtype. See that function for
        detailed documentation.
    copy: bool, optional
        Whether to copy the input object (True), or to use a reference instead.
        This option only applies when the input is an ndarray or recarray.
        Defaults to True.

    Returns
    -------
    np.recarray
        Record array created from the specified object.

    Notes
    -----
    If `obj` is ``None``, then call the `~numpy.recarray` constructor. If
    `obj` is a string, then call the `fromstring` constructor. If `obj` is a
    list or a tuple, then if the first object is an `~numpy.ndarray`, call
    `fromarrays`, otherwise call `fromrecords`. If `obj` is a
    `~numpy.recarray`, then make a copy of the data in the recarray
    (if ``copy=True``) and use the new formats, names, and titles. If `obj`
    is a file, then call `fromfile`. Finally, if obj is an `ndarray`, then
    return ``obj.view(recarray)``, making a copy of the data if ``copy=True``.

    Examples
    --------
    >>> a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    array([[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]])

    >>> np.core.records.array(a)
    rec.array([[1, 2, 3],
               [4, 5, 6],
               [7, 8, 9]],
        dtype=int32)

    >>> b = [(1, 1), (2, 4), (3, 9)]
    >>> c = np.core.records.array(b, formats = ['i2', 'f2'], names = ('x', 'y'))
    >>> c
    rec.array([(1, 1.0), (2, 4.0), (3, 9.0)],
              dtype=[('x', '<i2'), ('y', '<f2')])

    >>> c.x
    rec.array([1, 2, 3], dtype=int16)

    >>> c.y
    rec.array([ 1.0,  4.0,  9.0], dtype=float16)

    >>> r = np.rec.array(['abc','def'], names=['col1','col2'])
    >>> print(r.col1)
    abc

    >>> r.col1
    array('abc', dtype='<U3')

    >>> r.col2
    array('def', dtype='<U3')
    """
    if isinstance(obj, (type(None), str)) or hasattr(obj, 'readinto'):
        if formats is None:
            if dtype is None:
                raise ValueError('Must define formats (or dtype) if object is None, string, or an open file')
        else:
            kwds = {}
            if dtype is not None:
                dtype = sb.dtype(dtype)
            else:
                if formats is not None:
                    dtype = format_parser(formats, names, titles, aligned, byteorder).dtype
                else:
                    kwds = {'formats':formats, 
                     'names':names, 
                     'titles':titles, 
                     'aligned':aligned, 
                     'byteorder':byteorder}
        if obj is None:
            if shape is None:
                raise ValueError('Must define a shape if obj is None')
            return recarray(shape, dtype, buf=obj, offset=offset, strides=strides)
        if isinstance(obj, bytes):
            return fromstring(obj, dtype, shape=shape, offset=offset, **kwds)
        if isinstance(obj, (list, tuple)):
            if isinstance(obj[0], (tuple, list)):
                return fromrecords(obj, dtype=dtype, shape=shape, **kwds)
            return fromarrays(obj, dtype=dtype, shape=shape, **kwds)
    else:
        if isinstance(obj, recarray):
            if dtype is not None and obj.dtype != dtype:
                new = obj.view(dtype)
            else:
                new = obj
            if copy:
                new = new.copy()
            return new
            if hasattr(obj, 'readinto'):
                return fromfile(obj, dtype=dtype, shape=shape, offset=offset)
                if isinstance(obj, ndarray):
                    if dtype is not None and obj.dtype != dtype:
                        new = obj.view(dtype)
            else:
                new = obj
            if copy:
                new = new.copy()
        else:
            return new.view(recarray)
            interface = getattr(obj, '__array_interface__', None)
            if not (interface is None or isinstance(interface, dict)):
                raise ValueError('Unknown input type')
            obj = sb.array(obj)
            if dtype is not None and obj.dtype != dtype:
                obj = obj.view(dtype)
        return obj.view(recarray)