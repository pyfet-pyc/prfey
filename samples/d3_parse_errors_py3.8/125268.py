# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\core\numerictypes.py
r"""
numerictypes: Define the numeric type objects

This module is designed so "from numerictypes import \*" is safe.
Exported symbols include:

  Dictionary with all registered number types (including aliases):
    typeDict

  Type objects (not all will be available, depends on platform):
      see variable sctypes for which ones you have

    Bit-width names

    int8 int16 int32 int64 int128
    uint8 uint16 uint32 uint64 uint128
    float16 float32 float64 float96 float128 float256
    complex32 complex64 complex128 complex192 complex256 complex512
    datetime64 timedelta64

    c-based names

    bool_

    object_

    void, str_, unicode_

    byte, ubyte,
    short, ushort
    intc, uintc,
    intp, uintp,
    int_, uint,
    longlong, ulonglong,

    single, csingle,
    float_, complex_,
    longfloat, clongfloat,

   As part of the type-hierarchy:    xx -- is bit-width

   generic
     +-> bool_                                  (kind=b)
     +-> number
     |   +-> integer
     |   |   +-> signedinteger     (intxx)      (kind=i)
     |   |   |     byte
     |   |   |     short
     |   |   |     intc
     |   |   |     intp            int0
     |   |   |     int_
     |   |   |     longlong
     |   |   \-> unsignedinteger  (uintxx)     (kind=u)
     |   |         ubyte
     |   |         ushort
     |   |         uintc
     |   |         uintp           uint0
     |   |         uint_
     |   |         ulonglong
     |   +-> inexact
     |       +-> floating          (floatxx)    (kind=f)
     |       |     half
     |       |     single
     |       |     float_          (double)
     |       |     longfloat
     |       \-> complexfloating  (complexxx)  (kind=c)
     |             csingle         (singlecomplex)
     |             complex_        (cfloat, cdouble)
     |             clongfloat      (longcomplex)
     +-> flexible
     |   +-> character
     |   |     str_     (string_, bytes_)       (kind=S)    [Python 2]
     |   |     unicode_                         (kind=U)    [Python 2]
     |   |
     |   |     bytes_   (string_)               (kind=S)    [Python 3]
     |   |     str_     (unicode_)              (kind=U)    [Python 3]
     |   |
     |   \-> void                              (kind=V)
     \-> object_ (not used much)               (kind=O)

"""
import types as _types, numbers, warnings
from numpy.core.multiarray import typeinfo, ndarray, array, empty, dtype, datetime_data, datetime_as_string, busday_offset, busday_count, is_busday, busdaycalendar
from numpy.core.overrides import set_module
__all__ = [
 'sctypeDict', 'sctypeNA', 'typeDict', 'typeNA', 'sctypes',
 'ScalarType', 'obj2sctype', 'cast', 'nbytes', 'sctype2char',
 'maximum_sctype', 'issctype', 'typecodes', 'find_common_type',
 'issubdtype', 'datetime_data', 'datetime_as_string',
 'busday_offset', 'busday_count', 'is_busday', 'busdaycalendar']
from ._string_helpers import english_lower, english_upper, english_capitalize, LOWER_TABLE, UPPER_TABLE
from ._type_aliases import sctypeDict, sctypeNA, allTypes, bitname, sctypes, _concrete_types, _concrete_typeinfo, _bits_of
from ._dtype import _kind_name
from builtins import bool, int, float, complex, object, str, bytes
from numpy.compat import long, unicode
generic = allTypes['generic']
genericTypeRank = [
 'bool', 'int8', 'uint8', 'int16', 'uint16',
 'int32', 'uint32', 'int64', 'uint64', 'int128',
 'uint128', 'float16',
 'float32', 'float64', 'float80', 'float96', 'float128',
 'float256',
 'complex32', 'complex64', 'complex128', 'complex160',
 'complex192', 'complex256', 'complex512', 'object']

@set_module('numpy')
def maximum_sctype(t):
    """
    Return the scalar type of highest precision of the same kind as the input.

    Parameters
    ----------
    t : dtype or dtype specifier
        The input data type. This can be a `dtype` object or an object that
        is convertible to a `dtype`.

    Returns
    -------
    out : dtype
        The highest precision data type of the same kind (`dtype.kind`) as `t`.

    See Also
    --------
    obj2sctype, mintypecode, sctype2char
    dtype

    Examples
    --------
    >>> np.maximum_sctype(int)
    <class 'numpy.int64'>
    >>> np.maximum_sctype(np.uint8)
    <class 'numpy.uint64'>
    >>> np.maximum_sctype(complex)
    <class 'numpy.complex256'> # may vary

    >>> np.maximum_sctype(str)
    <class 'numpy.str_'>

    >>> np.maximum_sctype('i2')
    <class 'numpy.int64'>
    >>> np.maximum_sctype('f4')
    <class 'numpy.float128'> # may vary

    """
    g = obj2sctype(t)
    if g is None:
        return t
    t = g
    base = _kind_name(dtype(t))
    if base in sctypes:
        return sctypes[base][(-1)]
    return t


@set_module('numpy')
def issctype--- This code section failed: ---

 L. 221         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'rep'
                4  LOAD_GLOBAL              type
                6  LOAD_GLOBAL              dtype
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     18  'to 18'

 L. 222        14  LOAD_CONST               False
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 223        18  SETUP_FINALLY        52  'to 52'

 L. 224        20  LOAD_GLOBAL              obj2sctype
               22  LOAD_FAST                'rep'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'res'

 L. 225        28  LOAD_FAST                'res'
               30  POP_JUMP_IF_FALSE    46  'to 46'
               32  LOAD_FAST                'res'
               34  LOAD_GLOBAL              object_
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L. 226        40  POP_BLOCK        
               42  LOAD_CONST               True
               44  RETURN_VALUE     
             46_0  COME_FROM            38  '38'
             46_1  COME_FROM            30  '30'

 L. 227        46  POP_BLOCK        
               48  LOAD_CONST               False
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    18  '18'

 L. 228        52  DUP_TOP          
               54  LOAD_GLOBAL              Exception
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    72  'to 72'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 229        66  POP_EXCEPT       
               68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            58  '58'
               72  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 42


@set_module('numpy')
def obj2sctype(rep, default=None):
    """
    Return the scalar dtype or NumPy equivalent of Python type of an object.

    Parameters
    ----------
    rep : any
        The object of which the type is returned.
    default : any, optional
        If given, this is returned for objects whose types can not be
        determined. If not given, None is returned for those objects.

    Returns
    -------
    dtype : dtype or Python type
        The data type of `rep`.

    See Also
    --------
    sctype2char, issctype, issubsctype, issubdtype, maximum_sctype

    Examples
    --------
    >>> np.obj2sctype(np.int32)
    <class 'numpy.int32'>
    >>> np.obj2sctype(np.array([1., 2.]))
    <class 'numpy.float64'>
    >>> np.obj2sctype(np.array([1.j]))
    <class 'numpy.complex128'>

    >>> np.obj2sctype(dict)
    <class 'numpy.object_'>
    >>> np.obj2sctype('string')

    >>> np.obj2sctype(1, default=list)
    <class 'list'>

    """
    if isinstancereptype:
        if issubclassrepgeneric:
            return rep
    if isinstancerepndarray:
        return rep.dtype.type
    try:
        res = dtype(rep)
    except Exception:
        return default
    else:
        return res.type


@set_module('numpy')
def issubclass_--- This code section failed: ---

 L. 322         0  SETUP_FINALLY        14  'to 14'

 L. 323         2  LOAD_GLOBAL              issubclass
                4  LOAD_FAST                'arg1'
                6  LOAD_FAST                'arg2'
                8  CALL_FUNCTION_2       2  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 324        14  DUP_TOP          
               16  LOAD_GLOBAL              TypeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 325        28  POP_EXCEPT       
               30  LOAD_CONST               False
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'
               34  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 30


@set_module('numpy')
def issubsctype(arg1, arg2):
    """
    Determine if the first argument is a subclass of the second argument.

    Parameters
    ----------
    arg1, arg2 : dtype or dtype specifier
        Data-types.

    Returns
    -------
    out : bool
        The result.

    See Also
    --------
    issctype, issubdtype, obj2sctype

    Examples
    --------
    >>> np.issubsctype('S8', str)
    False
    >>> np.issubsctype(np.array([1]), int)
    True
    >>> np.issubsctype(np.array([1]), float)
    False

    """
    return issubclassobj2sctype(arg1)obj2sctype(arg2)


@set_module('numpy')
def issubdtype(arg1, arg2):
    """
    Returns True if first argument is a typecode lower/equal in type hierarchy.

    Parameters
    ----------
    arg1, arg2 : dtype_like
        dtype or string representing a typecode.

    Returns
    -------
    out : bool

    See Also
    --------
    issubsctype, issubclass_
    numpy.core.numerictypes : Overview of numpy type hierarchy.

    Examples
    --------
    >>> np.issubdtype('S1', np.string_)
    True
    >>> np.issubdtype(np.float64, np.float32)
    False

    """
    if not issubclass_arg1generic:
        arg1 = dtype(arg1).type
    if not issubclass_arg2generic:
        arg2 = dtype(arg2).type
    return issubclassarg1arg2


class _typedict(dict):
    __doc__ = '\n    Base object for a dictionary for look-up with any alias for an array dtype.\n\n    Instances of `_typedict` can not be used as dictionaries directly,\n    first they have to be populated.\n\n    '

    def __getitem__(self, obj):
        return dict.__getitem__(self, obj2sctype(obj))


nbytes = _typedict()
_alignment = _typedict()
_maxvals = _typedict()
_minvals = _typedict()

def _construct_lookups():
    for name, info in _concrete_typeinfo.items():
        obj = info.type
        nbytes[obj] = info.bits // 8
        _alignment[obj] = info.alignment
        if len(info) > 5:
            _maxvals[obj] = info.max
            _minvals[obj] = info.min
        else:
            _maxvals[obj] = None
            _minvals[obj] = None


_construct_lookups()

@set_module('numpy')
def sctype2char(sctype):
    """
    Return the string representation of a scalar dtype.

    Parameters
    ----------
    sctype : scalar dtype or object
        If a scalar dtype, the corresponding string character is
        returned. If an object, `sctype2char` tries to infer its scalar type
        and then return the corresponding string character.

    Returns
    -------
    typechar : str
        The string character corresponding to the scalar type.

    Raises
    ------
    ValueError
        If `sctype` is an object for which the type can not be inferred.

    See Also
    --------
    obj2sctype, issctype, issubsctype, mintypecode

    Examples
    --------
    >>> for sctype in [np.int32, np.double, np.complex_, np.string_, np.ndarray]:
    ...     print(np.sctype2char(sctype))
    l # may vary
    d
    D
    S
    O

    >>> x = np.array([1., 2-1.j])
    >>> np.sctype2char(x)
    'D'
    >>> np.sctype2char(list)
    'O'

    """
    sctype = obj2sctype(sctype)
    if sctype is None:
        raise ValueError('unrecognized type')
    if sctype not in _concrete_types:
        raise KeyError(sctype)
    return dtype(sctype).char


cast = _typedict()
for key in _concrete_types:
    cast[key] = lambda x, k=key: array(x, copy=False).astype(k)
else:
    try:
        ScalarType = [
         _types.IntType, _types.FloatType, _types.ComplexType,
         _types.LongType, _types.BooleanType,
         _types.StringType, _types.UnicodeType, _types.BufferType]
    except AttributeError:
        ScalarType = [
         int, float, complex, int, bool, bytes, str, memoryview]
    else:
        ScalarType.extend(_concrete_types)
        ScalarType = tuple(ScalarType)
        for key in allTypes:
            globals()[key] = allTypes[key]
            __all__.append(key)
        else:
            del key
            typecodes = {'Character':'c', 
             'Integer':'bhilqp', 
             'UnsignedInteger':'BHILQP', 
             'Float':'efdg', 
             'Complex':'FDG', 
             'AllInteger':'bBhHiIlLqQpP', 
             'AllFloat':'efdgFDG', 
             'Datetime':'Mm', 
             'All':'?bhilqpBHILQPefdgFDGSUVOMm'}
            typeDict = sctypeDict
            typeNA = sctypeNA
            _kind_list = [
             'b', 'u', 'i', 'f', 'c', 'S', 'U', 'V', 'O', 'M', 'm']
            __test_types = '?' + typecodes['AllInteger'][:-2] + typecodes['AllFloat'] + 'O'
            __len_test_types = len(__test_types)

            def _find_common_coerce(a, b):
                if a > b:
                    return a
                try:
                    thisind = __test_types.index(a.char)
                except ValueError:
                    return
                else:
                    return _can_coerce_all([a, b], start=thisind)


            def _can_coerce_all(dtypelist, start=0):
                N = len(dtypelist)
                if N == 0:
                    return
                if N == 1:
                    return dtypelist[0]
                thisind = start
                while True:
                    if thisind < __len_test_types:
                        newdtype = dtype(__test_types[thisind])
                        numcoerce = len([x for x in dtypelist if newdtype >= x])
                        if numcoerce == N:
                            return newdtype
                        thisind += 1


            def _register_types():
                numbers.Integral.register(integer)
                numbers.Complex.register(inexact)
                numbers.Real.register(floating)
                numbers.Number.register(number)


            _register_types()

            @set_module('numpy')
            def find_common_type(array_types, scalar_types):
                """
    Determine common type following standard coercion rules.

    Parameters
    ----------
    array_types : sequence
        A list of dtypes or dtype convertible objects representing arrays.
    scalar_types : sequence
        A list of dtypes or dtype convertible objects representing scalars.

    Returns
    -------
    datatype : dtype
        The common data type, which is the maximum of `array_types` ignoring
        `scalar_types`, unless the maximum of `scalar_types` is of a
        different kind (`dtype.kind`). If the kind is not understood, then
        None is returned.

    See Also
    --------
    dtype, common_type, can_cast, mintypecode

    Examples
    --------
    >>> np.find_common_type([], [np.int64, np.float32, complex])
    dtype('complex128')
    >>> np.find_common_type([np.int64, np.float32], [])
    dtype('float64')

    The standard casting rules ensure that a scalar cannot up-cast an
    array unless the scalar is of a fundamentally different kind of data
    (i.e. under a different hierarchy in the data type hierarchy) then
    the array:

    >>> np.find_common_type([np.float32], [np.int64, np.float64])
    dtype('float32')

    Complex is of a different type, so it up-casts the float in the
    `array_types` argument:

    >>> np.find_common_type([np.float32], [complex])
    dtype('complex128')

    Type specifier strings are convertible to dtypes and can therefore
    be used instead of dtypes:

    >>> np.find_common_type(['f4', 'f4', 'i4'], ['c8'])
    dtype('complex128')

    """
                array_types = [dtype(x) for x in array_types]
                scalar_types = [dtype(x) for x in scalar_types]
                maxa = _can_coerce_all(array_types)
                maxsc = _can_coerce_all(scalar_types)
                if maxa is None:
                    return maxsc
                if maxsc is None:
                    return maxa
                try:
                    index_a = _kind_list.index(maxa.kind)
                    index_sc = _kind_list.index(maxsc.kind)
                except ValueError:
                    return
                else:
                    if index_sc > index_a:
                        return _find_common_coercemaxscmaxa
                    return maxa