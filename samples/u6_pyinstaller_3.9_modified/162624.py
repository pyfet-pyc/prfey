# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\core\_dtype_ctypes.py
"""
Conversion from ctypes to dtype.

In an ideal world, we could achieve this through the PEP3118 buffer protocol,
something like::

    def dtype_from_ctypes_type(t):
        # needed to ensure that the shape of `t` is within memoryview.format
        class DummyStruct(ctypes.Structure):
            _fields_ = [('a', t)]

        # empty to avoid memory allocation
        ctype_0 = (DummyStruct * 0)()
        mv = memoryview(ctype_0)

        # convert the struct, and slice back out the field
        return _dtype_from_pep3118(mv.format)['a']

Unfortunately, this fails because:

* ctypes cannot handle length-0 arrays with PEP3118 (bpo-32782)
* PEP3118 cannot represent unions, but both numpy and ctypes can
* ctypes cannot handle big-endian structs with PEP3118 (bpo-32780)
"""
import numpy as np

def _from_ctypes_array(t):
    return np.dtype((dtype_from_ctypes_type(t._type_), (t._length_,)))


def _from_ctypes_structure(t):
    for item in t._fields_:
        if len(item) > 2:
            raise TypeError('ctypes bitfields have no dtype equivalent')
        if hasattr(t, '_pack_'):
            import ctypes
            formats = []
            offsets = []
            names = []
            current_offset = 0
            for fname, ftyp in t._fields_:
                names.append(fname)
                formats.append(dtype_from_ctypes_type(ftyp))
                effective_pack = min(t._pack_, ctypes.alignment(ftyp))
                current_offset = (current_offset + effective_pack - 1) // effective_pack * effective_pack
                offsets.append(current_offset)
                current_offset += ctypes.sizeof(ftyp)
            else:
                return np.dtype(dict(formats=formats,
                  offsets=offsets,
                  names=names,
                  itemsize=(ctypes.sizeof(t))))

        fields = []
        for fname, ftyp in t._fields_:
            fields.append((fname, dtype_from_ctypes_type(ftyp)))
        else:
            return np.dtype(fields, align=True)


def _from_ctypes_scalar--- This code section failed: ---

 L.  75         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                't'
                4  LOAD_STR                 '__ctype_be__'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  LOAD_FAST                't'
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    32  'to 32'

 L.  76        16  LOAD_GLOBAL              np
               18  LOAD_METHOD              dtype
               20  LOAD_STR                 '>'
               22  LOAD_FAST                't'
               24  LOAD_ATTR                _type_
               26  BINARY_ADD       
               28  CALL_METHOD_1         1  ''
               30  RETURN_VALUE     
             32_0  COME_FROM            14  '14'

 L.  77        32  LOAD_GLOBAL              getattr
               34  LOAD_FAST                't'
               36  LOAD_STR                 '__ctype_le__'
               38  LOAD_CONST               None
               40  CALL_FUNCTION_3       3  ''
               42  LOAD_FAST                't'
               44  <117>                 0  ''
               46  POP_JUMP_IF_FALSE    64  'to 64'

 L.  78        48  LOAD_GLOBAL              np
               50  LOAD_METHOD              dtype
               52  LOAD_STR                 '<'
               54  LOAD_FAST                't'
               56  LOAD_ATTR                _type_
               58  BINARY_ADD       
               60  CALL_METHOD_1         1  ''
               62  RETURN_VALUE     
             64_0  COME_FROM            46  '46'

 L.  80        64  LOAD_GLOBAL              np
               66  LOAD_METHOD              dtype
               68  LOAD_FAST                't'
               70  LOAD_ATTR                _type_
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _from_ctypes_union(t):
    import ctypes
    formats = []
    offsets = []
    names = []
    for fname, ftyp in t._fields_:
        names.append(fname)
        formats.append(dtype_from_ctypes_type(ftyp))
        offsets.append(0)
    else:
        return np.dtype(dict(formats=formats,
          offsets=offsets,
          names=names,
          itemsize=(ctypes.sizeof(t))))


def dtype_from_ctypes_type(t):
    """
    Construct a dtype object from a ctypes type
    """
    import _ctypes
    if issubclass(t, _ctypes.Array):
        return _from_ctypes_array(t)
    elif issubclass(t, _ctypes._Pointer):
        raise TypeError('ctypes pointers have no dtype equivalent')
    else:
        if issubclass(t, _ctypes.Structure):
            return _from_ctypes_structure(t)
        if issubclass(t, _ctypes.Union):
            return _from_ctypes_union(t)
        if isinstance(getattrt'_type_'None, str):
            return _from_ctypes_scalar(t)
        raise NotImplementedError('Unknown ctypes type {}'.format(t.__name__))