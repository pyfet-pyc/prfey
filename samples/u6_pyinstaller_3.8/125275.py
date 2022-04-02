# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\core\_dtype.py
"""
A place for code to be called from the implementation of np.dtype

String handling is much easier to do correctly in python.
"""
import numpy as np
_kind_to_stem = {'u':'uint', 
 'i':'int', 
 'c':'complex', 
 'f':'float', 
 'b':'bool', 
 'V':'void', 
 'O':'object', 
 'M':'datetime', 
 'm':'timedelta', 
 'S':'bytes', 
 'U':'str'}

def _kind_name--- This code section failed: ---

 L.  25         0  SETUP_FINALLY        14  'to 14'

 L.  26         2  LOAD_GLOBAL              _kind_to_stem
                4  LOAD_FAST                'dtype'
                6  LOAD_ATTR                kind
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  27        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    48  'to 48'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  28        28  LOAD_GLOBAL              RuntimeError

 L.  29        30  LOAD_STR                 'internal dtype error, unknown kind {!r}'
               32  LOAD_METHOD              format

 L.  30        34  LOAD_FAST                'dtype'
               36  LOAD_ATTR                kind

 L.  29        38  CALL_METHOD_1         1  ''

 L.  28        40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            20  '20'
               48  END_FINALLY      
             50_0  COME_FROM            46  '46'

Parse error at or near `POP_TOP' instruction at offset 24


def __str__(dtype):
    if dtype.fields is not None:
        return _struct_str(dtype, include_align=True)
    else:
        if dtype.subdtype:
            return _subarray_str(dtype)
        return issubclass(dtype.type, np.flexible) or dtype.isnative or dtype.str
    return dtype.name


def __repr__(dtype):
    arg_str = _construction_repr(dtype, include_align=False)
    if dtype.isalignedstruct:
        arg_str = arg_str + ', align=True'
    return 'dtype({})'.formatarg_str


def _unpack_field(dtype, offset, title=None):
    """
    Helper function to normalize the items in dtype.fields.

    Call as:

    dtype, offset, title = _unpack_field(*dtype.fields[name])
    """
    return (
     dtype, offset, title)


def _isunsized(dtype):
    return dtype.itemsize == 0


def _construction_repr(dtype, include_align=False, short=False):
    """
    Creates a string repr of the dtype, excluding the 'dtype()' part
    surrounding the object. This object may be a string, a list, or
    a dict depending on the nature of the dtype. This
    is the object passed as the first parameter to the dtype
    constructor, and if no additional constructor parameters are
    given, will reproduce the exact memory layout.

    Parameters
    ----------
    short : bool
        If true, this creates a shorter repr using 'kind' and 'itemsize', instead
        of the longer type name.

    include_align : bool
        If true, this includes the 'align=True' parameter
        inside the struct dtype construction dict when needed. Use this flag
        if you want a proper repr string without the 'dtype()' part around it.

        If false, this does not preserve the
        'align=True' parameter or sticky NPY_ALIGNED_STRUCT flag for
        struct arrays like the regular repr does, because the 'align'
        flag is not part of first dtype constructor parameter. This
        mode is intended for a full 'repr', where the 'align=True' is
        provided as the second parameter.
    """
    if dtype.fields is not None:
        return _struct_str(dtype, include_align=include_align)
    if dtype.subdtype:
        return _subarray_str(dtype)
    return _scalar_str(dtype, short=short)


def _scalar_str(dtype, short):
    byteorder = _byte_order_str(dtype)
    if dtype.type == np.bool_:
        if short:
            return "'?'"
        return "'bool'"
    else:
        if dtype.type == np.object_:
            return "'O'"
            if dtype.type == np.string_:
                if _isunsized(dtype):
                    return "'S'"
                return "'S%d'" % dtype.itemsize
        elif dtype.type == np.unicode_:
            if _isunsized(dtype):
                return "'%sU'" % byteorder
            return "'%sU%d'" % (byteorder, dtype.itemsize / 4)
        else:
            if issubclass(dtype.type, np.void):
                if _isunsized(dtype):
                    return "'V'"
                return "'V%d'" % dtype.itemsize
            else:
                if dtype.type == np.datetime64:
                    return "'%sM8%s'" % (byteorder, _datetime_metadata_str(dtype))
                    if dtype.type == np.timedelta64:
                        return "'%sm8%s'" % (byteorder, _datetime_metadata_str(dtype))
                elif np.issubdtype(dtype, np.number) and not short:
                    if dtype.byteorder not in ('=', '|'):
                        return "'%s%c%d'" % (byteorder, dtype.kind, dtype.itemsize)
                    return "'%s%d'" % (_kind_name(dtype), 8 * dtype.itemsize)
                else:
                    if dtype.isbuiltin == 2:
                        return dtype.type.__name__
                    raise RuntimeError('Internal error: NumPy dtype unrecognized type number')


def _byte_order_str(dtype):
    """ Normalize byteorder to '<' or '>' """
    swapped = np.dtypeint.newbyteorder's'
    native = swapped.newbyteorder's'
    byteorder = dtype.byteorder
    if byteorder == '=':
        return native.byteorder
    if byteorder == 's':
        return swapped.byteorder
    if byteorder == '|':
        return ''
    return byteorder


def _datetime_metadata_str(dtype):
    unit, count = np.datetime_datadtype
    if unit == 'generic':
        return ''
    if count == 1:
        return '[{}]'.formatunit
    return '[{}{}]'.format(count, unit)


def _struct_dict_str(dtype, includealignedflag):
    names = dtype.names
    fld_dtypes = []
    offsets = []
    titles = []
    for name in names:
        fld_dtype, offset, title = _unpack_field(*dtype.fields[name])
        fld_dtypes.appendfld_dtype
        offsets.appendoffset
        titles.appendtitle
    else:
        ret = "{'names':["
        ret += ','.join(repr(name) for name in names)
        ret += "], 'formats':["
        ret += ','.join(_construction_repr(fld_dtype, short=True) for fld_dtype in fld_dtypes)
        ret += "], 'offsets':["
        ret += ','.join('%d' % offset for offset in offsets)
        if any((title is not None for title in titles)):
            ret += "], 'titles':["
            ret += ','.join(repr(title) for title in titles)
        ret += "], 'itemsize':%d" % dtype.itemsize
        if includealignedflag and dtype.isalignedstruct:
            ret += ", 'aligned':True}"
        else:
            ret += '}'
        return ret


def _is_packed(dtype):
    """
    Checks whether the structured data type in 'dtype'
    has a simple layout, where all the fields are in order,
    and follow each other with no alignment padding.

    When this returns true, the dtype can be reconstructed
    from a list of the field names and dtypes with no additional
    dtype parameters.

    Duplicates the C `is_dtype_struct_simple_unaligned_layout` function.
    """
    total_offset = 0
    for name in dtype.names:
        fld_dtype, fld_offset, title = _unpack_field(*dtype.fields[name])
        if fld_offset != total_offset:
            return False
            total_offset += fld_dtype.itemsize
    else:
        if total_offset != dtype.itemsize:
            return False
        return True


def _struct_list_str(dtype):
    items = []
    for name in dtype.names:
        fld_dtype, fld_offset, title = _unpack_field(*dtype.fields[name])
        item = '('
        if title is not None:
            item += '({!r}, {!r}), '.format(title, name)
        else:
            item += '{!r}, '.formatname
        if fld_dtype.subdtype is not None:
            base, shape = fld_dtype.subdtype
            item += '{}, {}'.format(_construction_repr(base, short=True), shape)
        else:
            item += _construction_repr(fld_dtype, short=True)
        item += ')'
        items.appenditem
    else:
        return '[' + ', '.joinitems + ']'


def _struct_str(dtype, include_align):
    if not (include_align and dtype.isalignedstruct):
        if _is_packed(dtype):
            sub = _struct_list_str(dtype)
        else:
            sub = _struct_dict_str(dtype, include_align)
    if dtype.type != np.void:
        return '({t.__module__}.{t.__name__}, {f})'.format(t=(dtype.type), f=sub)
    return sub


def _subarray_str(dtype):
    base, shape = dtype.subdtype
    return '({}, {})'.format(_construction_repr(base, short=True), shape)


def _name_includes_bit_suffix(dtype):
    if dtype.type == np.object_:
        return False
    else:
        if dtype.type == np.bool_:
            return False
        if np.issubdtype(dtype, np.flexible) and _isunsized(dtype):
            return False
    return True


def _name_get(dtype):
    if dtype.isbuiltin == 2:
        return dtype.type.__name__
    elif issubclass(dtype.type, np.void):
        name = dtype.type.__name__
    else:
        name = _kind_name(dtype)
    if _name_includes_bit_suffix(dtype):
        name += '{}'.format(dtype.itemsize * 8)
    if dtype.type in (np.datetime64, np.timedelta64):
        name += _datetime_metadata_str(dtype)
    return name