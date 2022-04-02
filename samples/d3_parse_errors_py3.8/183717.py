# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\core\_type_aliases.py
"""
Due to compatibility, numpy has a very large number of different naming
conventions for the scalar types (those subclassing from `numpy.generic`).
This file produces a convoluted set of dictionaries mapping names to types,
and sometimes other mappings too.

.. data:: allTypes
    A dictionary of names to types that will be exposed as attributes through
    ``np.core.numerictypes.*``

.. data:: sctypeDict
    Similar to `allTypes`, but maps a broader set of aliases to their types.

.. data:: sctypeNA
    NumArray-compatible names for the scalar types. Contains not only
    ``name: type`` mappings, but ``char: name`` mappings too.

    .. deprecated:: 1.16

.. data:: sctypes
    A dictionary keyed by a "type group" string, providing a list of types
    under that group.

"""
import warnings, sys
from numpy.compat import unicode
from numpy._globals import VisibleDeprecationWarning
from numpy.core._string_helpers import english_lower, english_capitalize
from numpy.core.multiarray import typeinfo, dtype
from numpy.core._dtype import _kind_name
sctypeDict = {}

class TypeNADict(dict):

    def __getitem__(self, key):
        warnings.warn('sctypeNA and typeNA will be removed in v1.18 of numpy', VisibleDeprecationWarning,
          stacklevel=2)
        return dict.__getitem__(self, key)

    def get(self, key, default=None):
        warnings.warn('sctypeNA and typeNA will be removed in v1.18 of numpy', VisibleDeprecationWarning,
          stacklevel=2)
        return dict.get(self, key, default)


sctypeNA = TypeNADict()
allTypes = {}
_abstract_types = {}
_concrete_typeinfo = {}
for k, v in typeinfo.items():
    k = english_lower(k)
    if isinstance(v, type):
        _abstract_types[k] = v
    else:
        _concrete_typeinfo[k] = v
else:
    _concrete_types = {v.type for k, v in _concrete_typeinfo.items()}

    def _bits_of(obj):
        try:
            info = next((v for v in _concrete_typeinfo.values() if v.type is obj))
        except StopIteration:
            if obj in _abstract_types.values():
                raise ValueError('Cannot count the bits of an abstract type')
            return dtype(obj).itemsize * 8
        else:
            return info.bits


    def bitname(obj):
        """Return a bit-width name for a given type object"""
        bits = _bits_of(obj)
        dt = dtype(obj)
        char = dt.kind
        base = _kind_name(dt)
        if base == 'object':
            bits = 0
        if bits != 0:
            char = '%s%d' % (char, bits // 8)
        return (
         base, bits, char)


    def _add_types():
        for name, info in _concrete_typeinfo.items():
            allTypes[name] = info.type
            sctypeDict[name] = info.type
            sctypeDict[info.char] = info.type
            sctypeDict[info.num] = info.type
        else:
            for name, cls in _abstract_types.items():
                allTypes[name] = cls


    _add_types()
    _int_ctypes = [
     'long', 'longlong', 'int', 'short', 'byte']
    _uint_ctypes = list(('u' + t for t in _int_ctypes))

    def _add_aliases--- This code section failed: ---

 L. 116         0  LOAD_GLOBAL              _concrete_typeinfo
                2  LOAD_METHOD              items
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
              8_0  COME_FROM           218  '218'
              8_1  COME_FROM            78  '78'
              8_2  COME_FROM            32  '32'
              8_3  COME_FROM            22  '22'
                8  FOR_ITER            220  'to 220'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'name'
               14  STORE_FAST               'info'

 L. 118        16  LOAD_FAST                'name'
               18  LOAD_GLOBAL              _int_ctypes
               20  COMPARE_OP               in
               22  POP_JUMP_IF_TRUE_BACK     8  'to 8'
               24  LOAD_FAST                'name'
               26  LOAD_GLOBAL              _uint_ctypes
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE    34  'to 34'

 L. 119        32  JUMP_BACK             8  'to 8'
             34_0  COME_FROM            30  '30'

 L. 122        34  LOAD_GLOBAL              bitname
               36  LOAD_FAST                'info'
               38  LOAD_ATTR                type
               40  CALL_FUNCTION_1       1  ''
               42  UNPACK_SEQUENCE_3     3 
               44  STORE_FAST               'base'
               46  STORE_FAST               'bit'
               48  STORE_FAST               'char'

 L. 124        50  LOAD_STR                 '%s%d'
               52  LOAD_FAST                'base'
               54  LOAD_FAST                'bit'
               56  BUILD_TUPLE_2         2 
               58  BINARY_MODULO    
               60  STORE_FAST               'myname'

 L. 128        62  LOAD_FAST                'name'
               64  LOAD_CONST               ('longdouble', 'clongdouble')
               66  COMPARE_OP               in
               68  POP_JUMP_IF_FALSE    80  'to 80'
               70  LOAD_FAST                'myname'
               72  LOAD_GLOBAL              allTypes
               74  COMPARE_OP               in
               76  POP_JUMP_IF_FALSE    80  'to 80'

 L. 129        78  JUMP_BACK             8  'to 8'
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            68  '68'

 L. 131        80  LOAD_GLOBAL              english_capitalize
               82  LOAD_FAST                'base'
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               'base_capitalize'

 L. 132        88  LOAD_FAST                'base'
               90  LOAD_STR                 'complex'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   114  'to 114'

 L. 133        96  LOAD_STR                 '%s%d'
               98  LOAD_FAST                'base_capitalize'
              100  LOAD_FAST                'bit'
              102  LOAD_CONST               2
              104  BINARY_FLOOR_DIVIDE
              106  BUILD_TUPLE_2         2 
              108  BINARY_MODULO    
              110  STORE_FAST               'na_name'
              112  JUMP_FORWARD        140  'to 140'
            114_0  COME_FROM            94  '94'

 L. 134       114  LOAD_FAST                'base'
              116  LOAD_STR                 'bool'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   128  'to 128'

 L. 135       122  LOAD_FAST                'base_capitalize'
              124  STORE_FAST               'na_name'
              126  JUMP_FORWARD        140  'to 140'
            128_0  COME_FROM           120  '120'

 L. 137       128  LOAD_STR                 '%s%d'
              130  LOAD_FAST                'base_capitalize'
              132  LOAD_FAST                'bit'
              134  BUILD_TUPLE_2         2 
              136  BINARY_MODULO    
              138  STORE_FAST               'na_name'
            140_0  COME_FROM           126  '126'
            140_1  COME_FROM           112  '112'

 L. 139       140  LOAD_FAST                'info'
              142  LOAD_ATTR                type
              144  LOAD_GLOBAL              allTypes
              146  LOAD_FAST                'myname'
              148  STORE_SUBSCR     

 L. 142       150  LOAD_FAST                'info'
              152  LOAD_ATTR                type
              154  LOAD_GLOBAL              sctypeDict
              156  LOAD_FAST                'myname'
              158  STORE_SUBSCR     

 L. 143       160  LOAD_FAST                'info'
              162  LOAD_ATTR                type
              164  LOAD_GLOBAL              sctypeDict
              166  LOAD_FAST                'na_name'
              168  STORE_SUBSCR     

 L. 146       170  LOAD_FAST                'info'
              172  LOAD_ATTR                type
              174  LOAD_GLOBAL              sctypeNA
              176  LOAD_FAST                'na_name'
              178  STORE_SUBSCR     

 L. 147       180  LOAD_FAST                'na_name'
              182  LOAD_GLOBAL              sctypeNA
              184  LOAD_FAST                'info'
              186  LOAD_ATTR                type
              188  STORE_SUBSCR     

 L. 148       190  LOAD_FAST                'na_name'
              192  LOAD_GLOBAL              sctypeNA
              194  LOAD_FAST                'info'
              196  LOAD_ATTR                char
              198  STORE_SUBSCR     

 L. 150       200  LOAD_FAST                'info'
              202  LOAD_ATTR                type
              204  LOAD_GLOBAL              sctypeDict
              206  LOAD_FAST                'char'
              208  STORE_SUBSCR     

 L. 151       210  LOAD_FAST                'na_name'
              212  LOAD_GLOBAL              sctypeNA
              214  LOAD_FAST                'char'
              216  STORE_SUBSCR     
              218  JUMP_BACK             8  'to 8'
            220_0  COME_FROM             8  '8'

Parse error at or near `JUMP_BACK' instruction at offset 218


    _add_aliases()

    def _add_integer_aliases():
        seen_bits = set()
        for i_ctype, u_ctype in zip(_int_ctypes, _uint_ctypes):
            i_info = _concrete_typeinfo[i_ctype]
            u_info = _concrete_typeinfo[u_ctype]
            bits = i_info.bits
            for info, charname, intname, Intname in (
             (
              i_info, 'i%d' % (bits // 8,), 'int%d' % bits, 'Int%d' % bits),
             (
              u_info, 'u%d' % (bits // 8,), 'uint%d' % bits, 'UInt%d' % bits)):
                if bits not in seen_bits:
                    allTypes[intname] = info.type
                    sctypeDict[intname] = info.type
                    sctypeDict[Intname] = info.type
                    sctypeDict[charname] = info.type
                    sctypeNA[Intname] = info.type
                    sctypeNA[charname] = info.type
                else:
                    sctypeNA[info.type] = Intname
                    sctypeNA[info.char] = Intname
            else:
                seen_bits.add(bits)


    _add_integer_aliases()
    void = allTypes['void']

    def _set_up_aliases():
        type_pairs = [
         ('complex_', 'cdouble'),
         ('int0', 'intp'),
         ('uint0', 'uintp'),
         ('single', 'float'),
         ('csingle', 'cfloat'),
         ('singlecomplex', 'cfloat'),
         ('float_', 'double'),
         ('intc', 'int'),
         ('uintc', 'uint'),
         ('int_', 'long'),
         ('uint', 'ulong'),
         ('cfloat', 'cdouble'),
         ('longfloat', 'longdouble'),
         ('clongfloat', 'clongdouble'),
         ('longcomplex', 'clongdouble'),
         ('bool_', 'bool'),
         ('bytes_', 'string'),
         ('string_', 'string'),
         ('unicode_', 'unicode'),
         ('object_', 'object')]
        if sys.version_info[0] >= 3:
            type_pairs.extend([('str_', 'unicode')])
        else:
            type_pairs.extend([('str_', 'string')])
        for alias, t in type_pairs:
            allTypes[alias] = allTypes[t]
            sctypeDict[alias] = sctypeDict[t]
        else:
            to_remove = [
             'ulong', 'object', 'int', 'float',
             'complex', 'bool', 'string', 'datetime', 'timedelta']
            if sys.version_info[0] >= 3:
                to_remove.extend(['bytes', 'str'])
            else:
                to_remove.extend(['unicode', 'long'])
            for t in to_remove:
                try:
                    del allTypes[t]
                    del sctypeDict[t]
                except KeyError:
                    pass


    _set_up_aliases()
    sctypes = {'int':[],  'uint':[],  'float':[],  'complex':[],  'others':[
      bool, object, bytes, unicode, void]}

    def _add_array_type(typename, bits):
        try:
            t = allTypes[('%s%d' % (typename, bits))]
        except KeyError:
            pass
        else:
            sctypes[typename].append(t)


    def _set_array_types():
        ibytes = [1, 2, 4, 8, 16, 32, 64]
        fbytes = [2, 4, 8, 10, 12, 16, 32, 64]
        for bytes in ibytes:
            bits = 8 * bytes
            _add_array_type('int', bits)
            _add_array_type('uint', bits)
        else:
            for bytes in fbytes:
                bits = 8 * bytes
                _add_array_type('float', bits)
                _add_array_type('complex', 2 * bits)
            else:
                _gi = dtype('p')
                if _gi.type not in sctypes['int']:
                    indx = 0
                    sz = _gi.itemsize
                    _lst = sctypes['int']
                    while indx < len(_lst):
                        if sz >= _lst[indx](0).itemsize:
                            indx += 1

                    sctypes['int'].insert(indx, _gi.type)
                    sctypes['uint'].insert(indx, dtype('P').type)


    _set_array_types()
    _toadd = [
     'int', 'float', 'complex', 'bool', 'object']
    if sys.version_info[0] >= 3:
        _toadd.extend(['str', 'bytes', ('a', 'bytes_')])
    else:
        _toadd.extend(['string', ('str', 'string_'), 'unicode', ('a', 'string_')])
    for name in _toadd:
        if isinstance(name, tuple):
            sctypeDict[name[0]] = allTypes[name[1]]
        else:
            sctypeDict[name] = allTypes[('%s_' % name)]
    else:
        del _toadd
        del name