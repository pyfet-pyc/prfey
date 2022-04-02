# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
from __future__ import division, absolute_import, print_function
import sys, os, warnings
from collections import Counter, OrderedDict
from . import numeric as sb
from . import numerictypes as nt
from numpy.compat import isfileobj, bytes, long, unicode, os_fspath, contextlib_nullcontext
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
class format_parser(object):
    __doc__ = "\n    Class to convert formats, names, titles description to a dtype.\n\n    After constructing the format_parser object, the dtype attribute is\n    the converted data-type:\n    ``dtype = format_parser(formats, names, titles).dtype``\n\n    Attributes\n    ----------\n    dtype : dtype\n        The converted data-type.\n\n    Parameters\n    ----------\n    formats : str or list of str\n        The format description, either specified as a string with\n        comma-separated format descriptions in the form ``'f8, i4, a5'``, or\n        a list of format description strings  in the form\n        ``['f8', 'i4', 'a5']``.\n    names : str or list/tuple of str\n        The field names, either specified as a comma-separated string in the\n        form ``'col1, col2, col3'``, or as a list or tuple of strings in the\n        form ``['col1', 'col2', 'col3']``.\n        An empty list can be used, in that case default field names\n        ('f0', 'f1', ...) are used.\n    titles : sequence\n        Sequence of title strings. An empty list can be used to leave titles\n        out.\n    aligned : bool, optional\n        If True, align the fields by padding as the C-compiler would.\n        Default is False.\n    byteorder : str, optional\n        If specified, all the fields will be changed to the\n        provided byte-order.  Otherwise, the default byte-order is\n        used. For all available string specifiers, see `dtype.newbyteorder`.\n\n    See Also\n    --------\n    dtype, typename, sctype2char\n\n    Examples\n    --------\n    >>> np.format_parser(['<f8', '<i4', '<a5'], ['col1', 'col2', 'col3'],\n    ...                  ['T1', 'T2', 'T3']).dtype\n    dtype([(('T1', 'col1'), '<f8'), (('T2', 'col2'), '<i4'), (('T3', 'col3'), 'S5')])\n\n    `names` and/or `titles` can be empty lists. If `titles` is an empty list,\n    titles will simply not appear. If `names` is empty, default field names\n    will be used.\n\n    >>> np.format_parser(['f8', 'i4', 'a5'], ['col1', 'col2', 'col3'],\n    ...                  []).dtype\n    dtype([('col1', '<f8'), ('col2', '<i4'), ('col3', '<S5')])\n    >>> np.format_parser(['<f8', '<i4', '<a5'], [], []).dtype\n    dtype([('f0', '<f8'), ('f1', '<i4'), ('f2', 'S5')])\n\n    "

    def __init__(self, formats, names, titles, aligned=False, byteorder=None):
        self._parseFormats(formats, aligned)
        self._setfieldnames(names, titles)
        self._createdescr(byteorder)
        self.dtype = self._descr

    def _parseFormats(self, formats, aligned=False):
        """ Parse the field formats """
        if formats is None:
            raise ValueError('Need formats argument')
        if isinstance(formats, list):
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
            elif isinstance(names, (str, unicode)):
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
        if titles:
            self._titles = [n.strip() for n in titles[:self._nfields]]
        else:
            self._titles = []
            titles = []
        if self._nfields > len(titles):
            self._titles += [None] * (self._nfields - len(titles))

    def _createdescr(self, byteorder):
        descr = sb.dtype({'names':self._names,  'formats':self._f_formats, 
         'offsets':self._offsets, 
         'titles':self._titles})
        if byteorder is not None:
            byteorder = _byteorderconv[byteorder[0]]
            descr = descr.newbyteorder(byteorder)
        self._descr = descr


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

 L. 254         0  LOAD_FAST                'attr'
                2  LOAD_CONST               ('setfield', 'getfield', 'dtype')
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 255         8  LOAD_GLOBAL              nt
               10  LOAD_ATTR                void
               12  LOAD_METHOD              __getattribute__
               14  LOAD_FAST                'self'
               16  LOAD_FAST                'attr'
               18  CALL_METHOD_2         2  ''
               20  RETURN_VALUE     
             22_0  COME_FROM             6  '6'

 L. 256        22  SETUP_FINALLY        40  'to 40'

 L. 257        24  LOAD_GLOBAL              nt
               26  LOAD_ATTR                void
               28  LOAD_METHOD              __getattribute__
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'attr'
               34  CALL_METHOD_2         2  ''
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    22  '22'

 L. 258        40  DUP_TOP          
               42  LOAD_GLOBAL              AttributeError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    58  'to 58'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 259        54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            46  '46'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'

 L. 260        60  LOAD_GLOBAL              nt
               62  LOAD_ATTR                void
               64  LOAD_METHOD              __getattribute__
               66  LOAD_FAST                'self'
               68  LOAD_STR                 'dtype'
               70  CALL_METHOD_2         2  ''
               72  LOAD_ATTR                fields
               74  STORE_FAST               'fielddict'

 L. 261        76  LOAD_FAST                'fielddict'
               78  LOAD_METHOD              get
               80  LOAD_FAST                'attr'
               82  LOAD_CONST               None
               84  CALL_METHOD_2         2  ''
               86  STORE_FAST               'res'

 L. 262        88  LOAD_FAST                'res'
               90  POP_JUMP_IF_FALSE   178  'to 178'

 L. 263        92  LOAD_FAST                'self'
               94  LOAD_ATTR                getfield
               96  LOAD_FAST                'res'
               98  LOAD_CONST               None
              100  LOAD_CONST               2
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  CALL_FUNCTION_EX      0  'positional arguments only'
              108  STORE_FAST               'obj'

 L. 266       110  SETUP_FINALLY       122  'to 122'

 L. 267       112  LOAD_FAST                'obj'
              114  LOAD_ATTR                dtype
              116  STORE_FAST               'dt'
              118  POP_BLOCK        
              120  JUMP_FORWARD        146  'to 146'
            122_0  COME_FROM_FINALLY   110  '110'

 L. 268       122  DUP_TOP          
              124  LOAD_GLOBAL              AttributeError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   144  'to 144'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 270       136  LOAD_FAST                'obj'
              138  ROT_FOUR         
              140  POP_EXCEPT       
              142  RETURN_VALUE     
            144_0  COME_FROM           128  '128'
              144  END_FINALLY      
            146_0  COME_FROM           120  '120'

 L. 271       146  LOAD_FAST                'dt'
              148  LOAD_ATTR                names
              150  LOAD_CONST               None
              152  COMPARE_OP               is-not
              154  POP_JUMP_IF_FALSE   174  'to 174'

 L. 272       156  LOAD_FAST                'obj'
              158  LOAD_METHOD              view
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                __class__
              164  LOAD_FAST                'obj'
              166  LOAD_ATTR                dtype
              168  BUILD_TUPLE_2         2 
              170  CALL_METHOD_1         1  ''
              172  RETURN_VALUE     
            174_0  COME_FROM           154  '154'

 L. 273       174  LOAD_FAST                'obj'
              176  RETURN_VALUE     
            178_0  COME_FROM            90  '90'

 L. 275       178  LOAD_GLOBAL              AttributeError
              180  LOAD_STR                 "'record' object has no attribute '%s'"

 L. 276       182  LOAD_FAST                'attr'

 L. 275       184  BINARY_MODULO    
              186  CALL_FUNCTION_1       1  ''
              188  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `COME_FROM' instruction at offset 58_0

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
    __doc__ = "Construct an ndarray that allows field access using attributes.\n\n    Arrays may have a data-types containing fields, analogous\n    to columns in a spread sheet.  An example is ``[(x, int), (y, float)]``,\n    where each entry in the array is a pair of ``(int, float)``.  Normally,\n    these attributes are accessed using dictionary lookups such as ``arr['x']``\n    and ``arr['y']``.  Record arrays allow the fields to be accessed as members\n    of the array, using ``arr.x`` and ``arr.y``.\n\n    Parameters\n    ----------\n    shape : tuple\n        Shape of output array.\n    dtype : data-type, optional\n        The desired data-type.  By default, the data-type is determined\n        from `formats`, `names`, `titles`, `aligned` and `byteorder`.\n    formats : list of data-types, optional\n        A list containing the data-types for the different columns, e.g.\n        ``['i4', 'f8', 'i4']``.  `formats` does *not* support the new\n        convention of using types directly, i.e. ``(int, float, int)``.\n        Note that `formats` must be a list, not a tuple.\n        Given that `formats` is somewhat limited, we recommend specifying\n        `dtype` instead.\n    names : tuple of str, optional\n        The name of each column, e.g. ``('x', 'y', 'z')``.\n    buf : buffer, optional\n        By default, a new array is created of the given shape and data-type.\n        If `buf` is specified and is an object exposing the buffer interface,\n        the array will use the memory from the existing buffer.  In this case,\n        the `offset` and `strides` keywords are available.\n\n    Other Parameters\n    ----------------\n    titles : tuple of str, optional\n        Aliases for column names.  For example, if `names` were\n        ``('x', 'y', 'z')`` and `titles` is\n        ``('x_coordinate', 'y_coordinate', 'z_coordinate')``, then\n        ``arr['x']`` is equivalent to both ``arr.x`` and ``arr.x_coordinate``.\n    byteorder : {'<', '>', '='}, optional\n        Byte-order for all fields.\n    aligned : bool, optional\n        Align the fields in memory as the C-compiler would.\n    strides : tuple of ints, optional\n        Buffer (`buf`) is interpreted according to these strides (strides\n        define how many bytes each array element, row, column, etc.\n        occupy in memory).\n    offset : int, optional\n        Start reading buffer (`buf`) from this offset onwards.\n    order : {'C', 'F'}, optional\n        Row-major (C-style) or column-major (Fortran-style) order.\n\n    Returns\n    -------\n    rec : recarray\n        Empty array of the given shape and type.\n\n    See Also\n    --------\n    rec.fromrecords : Construct a record array from data.\n    record : fundamental data-type for `recarray`.\n    format_parser : determine a data-type from formats, names, titles.\n\n    Notes\n    -----\n    This constructor can be compared to ``empty``: it creates a new record\n    array but does not fill it with data.  To create a record array from data,\n    use one of the following methods:\n\n    1. Create a standard ndarray and convert it to a record array,\n       using ``arr.view(np.recarray)``\n    2. Use the `buf` keyword.\n    3. Use `np.rec.fromrecords`.\n\n    Examples\n    --------\n    Create an array with two fields, ``x`` and ``y``:\n\n    >>> x = np.array([(1.0, 2), (3.0, 4)], dtype=[('x', '<f8'), ('y', '<i8')])\n    >>> x\n    array([(1., 2), (3., 4)], dtype=[('x', '<f8'), ('y', '<i8')])\n\n    >>> x['x']\n    array([1., 3.])\n\n    View the array as a record array:\n\n    >>> x = x.view(np.recarray)\n\n    >>> x.x\n    array([1., 3.])\n\n    >>> x.y\n    array([2, 4])\n\n    Create a new, empty record array:\n\n    >>> np.recarray((2,),\n    ... dtype=[('x', int), ('y', float), ('z', int)]) #doctest: +SKIP\n    rec.array([(-1073741821, 1.2249118382103472e-301, 24547520),\n           (3471280, 1.2134086255804012e-316, 0)],\n          dtype=[('x', '<i4'), ('y', '<f8'), ('z', '<i4')])\n\n    "
    __name__ = 'recarray'
    __module__ = 'numpy'

    def __new__(subtype, shape, dtype=None, buf=None, offset=0, strides=None, formats=None, names=None, titles=None, byteorder=None, aligned=False, order='C'):
        if dtype is not None:
            descr = sb.dtype(dtype)
        else:
            descr = format_parser(formats, names, titles, aligned, byteorder)._descr
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

 L. 456         0  SETUP_FINALLY        16  'to 16'

 L. 457         2  LOAD_GLOBAL              object
                4  LOAD_METHOD              __getattribute__
                6  LOAD_FAST                'self'
                8  LOAD_FAST                'attr'
               10  CALL_METHOD_2         2  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 458        16  DUP_TOP          
               18  LOAD_GLOBAL              AttributeError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    34  'to 34'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 459        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
             34_0  COME_FROM            22  '22'
               34  END_FINALLY      
             36_0  COME_FROM            32  '32'

 L. 462        36  LOAD_GLOBAL              ndarray
               38  LOAD_METHOD              __getattribute__
               40  LOAD_FAST                'self'
               42  LOAD_STR                 'dtype'
               44  CALL_METHOD_2         2  ''
               46  LOAD_ATTR                fields
               48  STORE_FAST               'fielddict'

 L. 463        50  SETUP_FINALLY        72  'to 72'

 L. 464        52  LOAD_FAST                'fielddict'
               54  LOAD_FAST                'attr'
               56  BINARY_SUBSCR    
               58  LOAD_CONST               None
               60  LOAD_CONST               2
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  STORE_FAST               'res'
               68  POP_BLOCK        
               70  JUMP_FORWARD        108  'to 108'
             72_0  COME_FROM_FINALLY    50  '50'

 L. 465        72  DUP_TOP          
               74  LOAD_GLOBAL              TypeError
               76  LOAD_GLOBAL              KeyError
               78  BUILD_TUPLE_2         2 
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   106  'to 106'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 466        90  LOAD_GLOBAL              AttributeError
               92  LOAD_STR                 'recarray has no attribute %s'
               94  LOAD_FAST                'attr'
               96  BINARY_MODULO    
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            82  '82'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            70  '70'

 L. 467       108  LOAD_FAST                'self'
              110  LOAD_ATTR                getfield
              112  LOAD_FAST                'res'
              114  CALL_FUNCTION_EX      0  'positional arguments only'
              116  STORE_FAST               'obj'

 L. 475       118  LOAD_FAST                'obj'
              120  LOAD_ATTR                dtype
              122  LOAD_ATTR                names
              124  LOAD_CONST               None
              126  COMPARE_OP               is-not
              128  POP_JUMP_IF_FALSE   172  'to 172'

 L. 476       130  LOAD_GLOBAL              issubclass
              132  LOAD_FAST                'obj'
              134  LOAD_ATTR                dtype
              136  LOAD_ATTR                type
              138  LOAD_GLOBAL              nt
              140  LOAD_ATTR                void
              142  CALL_FUNCTION_2       2  ''
              144  POP_JUMP_IF_FALSE   168  'to 168'

 L. 477       146  LOAD_FAST                'obj'
              148  LOAD_ATTR                view
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                dtype
              154  LOAD_ATTR                type
              156  LOAD_FAST                'obj'
              158  LOAD_ATTR                dtype
              160  BUILD_TUPLE_2         2 
              162  LOAD_CONST               ('dtype',)
              164  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              166  RETURN_VALUE     
            168_0  COME_FROM           144  '144'

 L. 478       168  LOAD_FAST                'obj'
              170  RETURN_VALUE     
            172_0  COME_FROM           128  '128'

 L. 480       172  LOAD_FAST                'obj'
              174  LOAD_METHOD              view
              176  LOAD_GLOBAL              ndarray
              178  CALL_METHOD_1         1  ''
              180  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 34_0

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
                    except (TypeError, KeyError):
                        raise AttributeError('record array has no attribute %s' % attr)
                    else:
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
        if self.dtype.type is record or not issubclass(self.dtype.type, nt.void):
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


def fromarrays(arrayList, dtype=None, shape=None, formats=None, names=None, titles=None, aligned=False, byteorder=None):
    """ create a record array from a (flat) list of arrays

    >>> x1=np.array([1,2,3,4])
    >>> x2=np.array(['a','dd','xyz','12'])
    >>> x3=np.array([1.1,2,3,4])
    >>> r = np.core.records.fromarrays([x1,x2,x3],names='a,b,c')
    >>> print(r[1])
    (2, 'dd', 2.0) # may vary
    >>> x1[1]=34
    >>> r.a
    array([1, 2, 3, 4])
    """
    arrayList = [sb.asarray(x) for x in arrayList]
    if shape is None or (shape == 0):
        shape = arrayList[0].shape
    if isinstance(shape, int):
        shape = (
         shape,)
    if formats is None:
        if dtype is None:
            formats = []
            for obj in arrayList:
                formats.append(obj.dtype)
            else:
                if dtype is not None:
                    descr = sb.dtype(dtype)
                    _names = descr.names
                else:
                    parsed = format_parser(formats, names, titles, aligned, byteorder)
                    _names = parsed._names
                    descr = parsed._descr
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
    else:
        _array = recarray(shape, descr)
        for i in range(len(arrayList)):
            _array[_names[i]] = arrayList[i]
        else:
            return _array


def fromrecords(recList, dtype=None, shape=None, formats=None, names=None, titles=None, aligned=False, byteorder=None):
    """ create a recarray from a list of records in text form

        The data in the same field can be heterogeneous, they will be promoted
        to the highest data type.  This method is intended for creating
        smaller record arrays.  If used to create large array without formats
        defined

        r=fromrecords([(2,3.,'abc')]*100000)

        it can be slow.

        If formats is None, then this will auto-detect formats. Use list of
        tuples rather than list of lists for faster processing.

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
    if dtype is not None:
        descr = sb.dtype((record, dtype))
    else:
        descr = format_parser(formats, names, titles, aligned, byteorder)._descr
    try:
        retval = sb.array(recList, dtype=descr)
    except (TypeError, ValueError):
        if shape is None or (shape == 0):
            shape = len(recList)
        if isinstance(shape, (int, long)):
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
    """ create a (read-only) record array from binary data contained in
    a string"""
    if dtype is None:
        if formats is None:
            raise TypeError("fromstring() needs a 'dtype' or 'formats' argument")
    if dtype is not None:
        descr = sb.dtype(dtype)
    else:
        descr = format_parser(formats, names, titles, aligned, byteorder)._descr
    itemsize = descr.itemsize
    if not shape is None:
        if shape == 0 or (shape == -1):
            shape = (len(datastring) - offset) // itemsize
        _array = recarray(shape, descr, buf=datastring, offset=offset)
        return _array


def get_remaining_size(fd):
    try:
        fn = fd.fileno()
    except AttributeError:
        return os.path.getsize(fd.name) - fd.tell()
    else:
        st = os.fstat(fn)
        size = st.st_size - fd.tell()
        return size


def fromfile(fd, dtype=None, shape=None, offset=0, formats=None, names=None, titles=None, aligned=False, byteorder=None):
    """Create an array from binary file data

    If file is a string or a path-like object then that file is opened,
    else it is assumed to be a file object. The file object must
    support random access (i.e. it must have tell and seek methods).

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
    if shape is None or shape == 0:
        shape = (-1, )
    elif isinstance(shape, (int, long)):
        shape = (
         shape,)
    if isfileobj(fd):
        ctx = contextlib_nullcontext(fd)
    else:
        ctx = open(os_fspath(fd), 'rb')
    with ctx as fd:
        if offset > 0:
            fd.seek(offset, 1)
        size = get_remaining_size(fd)
        if dtype is not None:
            descr = sb.dtype(dtype)
        else:
            descr = format_parser(formats, names, titles, aligned, byteorder)._descr
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
    """Construct a record array from a wide-variety of objects.
    """
    if isinstance(obj, (type(None), str)) or (isfileobj(obj)):
        if formats is None:
            if dtype is None:
                raise ValueError('Must define formats (or dtype) if object is None, string, or an open file')
    kwds = {}
    if dtype is not None:
        dtype = sb.dtype(dtype)
    elif formats is not None:
        dtype = format_parser(formats, names, titles, aligned, byteorder)._descr
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
        if isfileobj(obj):
            return fromfile(obj, dtype=dtype, shape=shape, offset=offset)
        if isinstance(obj, ndarray):
            if dtype is not None and obj.dtype != dtype:
                new = obj.view(dtype)
            else:
                new = obj
            if copy:
                new = new.copy()
            return new.view(recarray)
        interface = getattr(obj, '__array_interface__', None)
        if not (interface is None or isinstance(interface, dict)):
            raise ValueError('Unknown input type')
        obj = sb.array(obj)
        if dtype is not None:
            if obj.dtype != dtype:
                obj = obj.view(dtype)
        return obj.view(recarray)