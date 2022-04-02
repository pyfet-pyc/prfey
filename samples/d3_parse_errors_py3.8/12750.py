# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\core\_internal.py
"""
A place for internal code

Some things are more easily handled Python.

"""
import ast, re, sys, platform
from .multiarray import dtype, array, ndarray
try:
    import ctypes
except ImportError:
    ctypes = None
else:
    IS_PYPY = platform.python_implementation() == 'PyPy'
    if sys.byteorder == 'little':
        _nbo = '<'
    else:
        _nbo = '>'

    def _makenames_list--- This code section failed: ---

 L.  26         0  BUILD_LIST_0          0 
                2  STORE_FAST               'allfields'

 L.  28         4  LOAD_FAST                'adict'
                6  LOAD_METHOD              items
                8  CALL_METHOD_0         0  ''
               10  GET_ITER         
             12_0  COME_FROM           160  '160'
             12_1  COME_FROM            74  '74'
               12  FOR_ITER            162  'to 162'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'fname'
               18  STORE_FAST               'obj'

 L.  29        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'obj'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'n'

 L.  30        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'obj'
               32  LOAD_GLOBAL              tuple
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    46  'to 46'
               38  LOAD_FAST                'n'
               40  LOAD_CONST               (2, 3)
               42  COMPARE_OP               not-in
               44  POP_JUMP_IF_FALSE    54  'to 54'
             46_0  COME_FROM            36  '36'

 L.  31        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'entry not a 2- or 3- tuple'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L.  32        54  LOAD_FAST                'n'
               56  LOAD_CONST               2
               58  COMPARE_OP               >
               60  POP_JUMP_IF_FALSE    76  'to 76'
               62  LOAD_FAST                'obj'
               64  LOAD_CONST               2
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'fname'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    76  'to 76'

 L.  33        74  JUMP_BACK            12  'to 12'
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            60  '60'

 L.  34        76  LOAD_GLOBAL              int
               78  LOAD_FAST                'obj'
               80  LOAD_CONST               1
               82  BINARY_SUBSCR    
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               'num'

 L.  35        88  LOAD_FAST                'num'
               90  LOAD_CONST               0
               92  COMPARE_OP               <
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L.  36        96  LOAD_GLOBAL              ValueError
               98  LOAD_STR                 'invalid offset.'
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            94  '94'

 L.  37       104  LOAD_GLOBAL              dtype
              106  LOAD_FAST                'obj'
              108  LOAD_CONST               0
              110  BINARY_SUBSCR    
              112  LOAD_FAST                'align'
              114  LOAD_CONST               ('align',)
              116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              118  STORE_FAST               'format'

 L.  38       120  LOAD_FAST                'n'
              122  LOAD_CONST               2
              124  COMPARE_OP               >
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L.  39       128  LOAD_FAST                'obj'
              130  LOAD_CONST               2
              132  BINARY_SUBSCR    
              134  STORE_FAST               'title'
              136  JUMP_FORWARD        142  'to 142'
            138_0  COME_FROM           126  '126'

 L.  41       138  LOAD_CONST               None
              140  STORE_FAST               'title'
            142_0  COME_FROM           136  '136'

 L.  42       142  LOAD_FAST                'allfields'
              144  LOAD_METHOD              append
              146  LOAD_FAST                'fname'
              148  LOAD_FAST                'format'
              150  LOAD_FAST                'num'
              152  LOAD_FAST                'title'
              154  BUILD_TUPLE_4         4 
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
              160  JUMP_BACK            12  'to 12'
            162_0  COME_FROM            12  '12'

 L.  44       162  LOAD_FAST                'allfields'
              164  LOAD_ATTR                sort
              166  LOAD_LAMBDA              '<code_object <lambda>>'
              168  LOAD_STR                 '_makenames_list.<locals>.<lambda>'
              170  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              172  LOAD_CONST               ('key',)
              174  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              176  POP_TOP          

 L.  45       178  LOAD_LISTCOMP            '<code_object <listcomp>>'
              180  LOAD_STR                 '_makenames_list.<locals>.<listcomp>'
              182  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              184  LOAD_FAST                'allfields'
              186  GET_ITER         
              188  CALL_FUNCTION_1       1  ''
              190  STORE_FAST               'names'

 L.  46       192  LOAD_LISTCOMP            '<code_object <listcomp>>'
              194  LOAD_STR                 '_makenames_list.<locals>.<listcomp>'
              196  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              198  LOAD_FAST                'allfields'
              200  GET_ITER         
              202  CALL_FUNCTION_1       1  ''
              204  STORE_FAST               'formats'

 L.  47       206  LOAD_LISTCOMP            '<code_object <listcomp>>'
              208  LOAD_STR                 '_makenames_list.<locals>.<listcomp>'
              210  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              212  LOAD_FAST                'allfields'
              214  GET_ITER         
              216  CALL_FUNCTION_1       1  ''
              218  STORE_FAST               'offsets'

 L.  48       220  LOAD_LISTCOMP            '<code_object <listcomp>>'
              222  LOAD_STR                 '_makenames_list.<locals>.<listcomp>'
              224  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              226  LOAD_FAST                'allfields'
              228  GET_ITER         
              230  CALL_FUNCTION_1       1  ''
              232  STORE_FAST               'titles'

 L.  50       234  LOAD_FAST                'names'
              236  LOAD_FAST                'formats'
              238  LOAD_FAST                'offsets'
              240  LOAD_FAST                'titles'
              242  BUILD_TUPLE_4         4 
              244  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 162


    def _usefields(adict, align):
        try:
            names = adict[(-1)]
        except KeyError:
            names = None
        else:
            if names is None:
                names, formats, offsets, titles = _makenames_list(adict, align)
            else:
                formats = []
                offsets = []
                titles = []
                for name in names:
                    res = adict[name]
                    formats.append(res[0])
                    offsets.append(res[1])
                    if len(res) > 2:
                        titles.append(res[2])
                    else:
                        titles.append(None)
                else:
                    return dtype({'names':names,  'formats':formats, 
                     'offsets':offsets, 
                     'titles':titles}, align)


    def _array_descr(descriptor):
        fields = descriptor.fields
        if fields is None:
            subdtype = descriptor.subdtype
            if subdtype is None:
                if descriptor.metadata is None:
                    return descriptor.str
                new = descriptor.metadata.copy()
                if new:
                    return (descriptor.str, new)
                return descriptor.str
            else:
                return (
                 _array_descr(subdtype[0]), subdtype[1])
        names = descriptor.names
        ordered_fields = [fields[x] + (x,) for x in names]
        result = []
        offset = 0
        for field in ordered_fields:
            if field[1] > offset:
                num = field[1] - offset
                result.append(('', f"|V{num}"))
                offset += num
            elif field[1] < offset:
                raise ValueError('dtype.descr is not defined for types with overlapping or out-of-order fields')
            if len(field) > 3:
                name = (
                 field[2], field[3])
            else:
                name = field[2]
            if field[0].subdtype:
                tup = (
                 name, _array_descr(field[0].subdtype[0]),
                 field[0].subdtype[1])
            else:
                tup = (
                 name, _array_descr(field[0]))
            offset += field[0].itemsize
            result.append(tup)
        else:
            if descriptor.itemsize > offset:
                num = descriptor.itemsize - offset
                result.append(('', f"|V{num}"))
            return result


    def _reconstruct(subtype, shape, dtype):
        return ndarray.__new__(subtype, shape, dtype)


    format_re = re.compile('(?P<order1>[<>|=]?)(?P<repeats> *[(]?[ ,0-9]*[)]? *)(?P<order2>[<>|=]?)(?P<dtype>[A-Za-z0-9.?]*(?:\\[[a-zA-Z0-9,.]+\\])?)')
    sep_re = re.compile('\\s*,\\s*')
    space_re = re.compile('\\s+$')
    _convorder = {'=': _nbo}

    def _commastring(astr):
        startindex = 0
        result = []
        while True:
            if startindex < len(astr):
                mo = format_re.match(astr, pos=startindex)
                try:
                    order1, repeats, order2, dtype = mo.groups()
                except (TypeError, AttributeError):
                    raise ValueError(f'format number {len(result) + 1} of "{astr}" is not recognized') from None
                else:
                    startindex = mo.end()
                    if startindex < len(astr):
                        if space_re.match(astr, pos=startindex):
                            startindex = len(astr)
                        else:
                            mo = sep_re.match(astr, pos=startindex)
                            if not mo:
                                raise ValueError('format number %d of "%s" is not recognized' % (
                                 len(result) + 1, astr))
                            startindex = mo.end()
                    if order2 == '':
                        order = order1
                    elif order1 == '':
                        order = order2
                    else:
                        order1 = _convorder.get(order1, order1)
                        order2 = _convorder.get(order2, order2)
                        if order1 != order2:
                            raise ValueError('inconsistent byte-order specification %s and %s' % (
                             order1, order2))
                        order = order1
                    if order in ('|', '=', _nbo):
                        order = ''
                    dtype = order + dtype
                    if repeats == '':
                        newitem = dtype
                    else:
                        newitem = (
                         dtype, ast.literal_eval(repeats))
                    result.append(newitem)

        return result


    class dummy_ctype:

        def __init__(self, cls):
            self._cls = cls

        def __mul__(self, other):
            return self

        def __call__(self, *other):
            return self._cls(other)

        def __eq__(self, other):
            return self._cls == other._cls

        def __ne__(self, other):
            return self._cls != other._cls


    def _getintp_ctype():
        val = _getintp_ctype.cache
        if val is not None:
            return val
        if ctypes is None:
            import numpy as np
            val = dummy_ctype(np.intp)
        else:
            char = dtype('p').char
            if char == 'i':
                val = ctypes.c_int
            elif char == 'l':
                val = ctypes.c_long
            elif char == 'q':
                val = ctypes.c_longlong
            else:
                val = ctypes.c_long
        _getintp_ctype.cache = val
        return val


    _getintp_ctype.cache = None

    class _missing_ctypes:

        def cast(self, num, obj):
            return num.value

        class c_void_p:

            def __init__(self, ptr):
                self.value = ptr


    class _ctypes:

        def __init__(self, array, ptr=None):
            self._arr = array
            if ctypes:
                self._ctypes = ctypes
                self._data = self._ctypes.c_void_p(ptr)
            else:
                self._ctypes = _missing_ctypes()
                self._data = self._ctypes.c_void_p(ptr)
                self._data._objects = array
            if self._arr.ndim == 0:
                self._zerod = True
            else:
                self._zerod = False

        def data_as(self, obj):
            """
        Return the data pointer cast to a particular c-types object.
        For example, calling ``self._as_parameter_`` is equivalent to
        ``self.data_as(ctypes.c_void_p)``. Perhaps you want to use the data as a
        pointer to a ctypes array of floating-point data:
        ``self.data_as(ctypes.POINTER(ctypes.c_double))``.

        The returned pointer will keep a reference to the array.
        """
            ptr = self._ctypes.cast(self._data, obj)
            ptr._arr = self._arr
            return ptr

        def shape_as(self, obj):
            """
        Return the shape tuple as an array of some other c-types
        type. For example: ``self.shape_as(ctypes.c_short)``.
        """
            if self._zerod:
                return
            return (obj * self._arr.ndim)(*self._arr.shape)

        def strides_as(self, obj):
            """
        Return the strides tuple as an array of some other
        c-types type. For example: ``self.strides_as(ctypes.c_longlong)``.
        """
            if self._zerod:
                return
            return (obj * self._arr.ndim)(*self._arr.strides)

        @property
        def data(self):
            """
        A pointer to the memory area of the array as a Python integer.
        This memory area may contain data that is not aligned, or not in correct
        byte-order. The memory area may not even be writeable. The array
        flags and data-type of this array should be respected when passing this
        attribute to arbitrary C-code to avoid trouble that can include Python
        crashing. User Beware! The value of this attribute is exactly the same
        as ``self._array_interface_['data'][0]``.

        Note that unlike ``data_as``, a reference will not be kept to the array:
        code like ``ctypes.c_void_p((a + b).ctypes.data)`` will result in a
        pointer to a deallocated array, and should be spelt
        ``(a + b).ctypes.data_as(ctypes.c_void_p)``
        """
            return self._data.value

        @property
        def shape(self):
            """
        (c_intp*self.ndim): A ctypes array of length self.ndim where
        the basetype is the C-integer corresponding to ``dtype('p')`` on this
        platform. This base-type could be `ctypes.c_int`, `ctypes.c_long`, or
        `ctypes.c_longlong` depending on the platform.
        The c_intp type is defined accordingly in `numpy.ctypeslib`.
        The ctypes array contains the shape of the underlying array.
        """
            return self.shape_as(_getintp_ctype())

        @property
        def strides(self):
            """
        (c_intp*self.ndim): A ctypes array of length self.ndim where
        the basetype is the same as for the shape attribute. This ctypes array
        contains the strides information from the underlying array. This strides
        information is important for showing how many bytes must be jumped to
        get to the next element in the array.
        """
            return self.strides_as(_getintp_ctype())

        @property
        def _as_parameter_(self):
            """
        Overrides the ctypes semi-magic method

        Enables `c_func(some_array.ctypes)`
        """
            return self.data_as(ctypes.c_void_p)

        get_data = data.fget
        get_shape = shape.fget
        get_strides = strides.fget
        get_as_parameter = _as_parameter_.fget


    def _newnames(datatype, order):
        """
    Given a datatype and an order object, return a new names tuple, with the
    order indicated
    """
        oldnames = datatype.names
        nameslist = list(oldnames)
        if isinstance(order, str):
            order = [
             order]
        seen = set()
        if isinstance(order, (list, tuple)):
            for name in order:
                try:
                    nameslist.remove(name)
                except ValueError:
                    if name in seen:
                        raise ValueError(f"duplicate field name: {name}") from None
                    else:
                        raise ValueError(f"unknown field name: {name}") from None
                else:
                    seen.add(name)
            else:
                return tuple(list(order) + nameslist)

        raise ValueError(f"unsupported order value: {order}")


    def _copy_fields(ary):
        """Return copy of structured array with padding between fields removed.

    Parameters
    ----------
    ary : ndarray
       Structured array from which to remove padding bytes

    Returns
    -------
    ary_copy : ndarray
       Copy of ary with padding bytes removed
    """
        dt = ary.dtype
        copy_dtype = {'names':dt.names,  'formats':[dt.fields[name][0] for name in dt.names]}
        return array(ary, dtype=copy_dtype, copy=True)


    def _getfield_is_safe(oldtype, newtype, offset):
        """ Checks safety of getfield for object arrays.

    As in _view_is_safe, we need to check that memory containing objects is not
    reinterpreted as a non-object datatype and vice versa.

    Parameters
    ----------
    oldtype : data-type
        Data type of the original ndarray.
    newtype : data-type
        Data type of the field being accessed by ndarray.getfield
    offset : int
        Offset of the field being accessed by ndarray.getfield

    Raises
    ------
    TypeError
        If the field access is invalid

    """
        if newtype.hasobject or (oldtype.hasobject):
            if offset == 0:
                if newtype == oldtype:
                    return
        if oldtype.names is not None:
            for name in oldtype.names:
                if oldtype.fields[name][1] == offset:
                    if oldtype.fields[name][0] == newtype:
                        return None
            else:
                raise TypeError('Cannot get/set field of an object array')


    def _view_is_safe(oldtype, newtype):
        """ Checks safety of a view involving object arrays, for example when
    doing::

        np.zeros(10, dtype=oldtype).view(newtype)

    Parameters
    ----------
    oldtype : data-type
        Data type of original ndarray
    newtype : data-type
        Data type of the view

    Raises
    ------
    TypeError
        If the new type is incompatible with the old type.

    """
        if oldtype == newtype:
            return
        if newtype.hasobject or (oldtype.hasobject):
            raise TypeError('Cannot change data-type for object array.')


    _pep3118_native_map = {'?':'?', 
     'c':'S1', 
     'b':'b', 
     'B':'B', 
     'h':'h', 
     'H':'H', 
     'i':'i', 
     'I':'I', 
     'l':'l', 
     'L':'L', 
     'q':'q', 
     'Q':'Q', 
     'e':'e', 
     'f':'f', 
     'd':'d', 
     'g':'g', 
     'Zf':'F', 
     'Zd':'D', 
     'Zg':'G', 
     's':'S', 
     'w':'U', 
     'O':'O', 
     'x':'V'}
    _pep3118_native_typechars = ''.join(_pep3118_native_map.keys())
    _pep3118_standard_map = {'?':'?', 
     'c':'S1', 
     'b':'b', 
     'B':'B', 
     'h':'i2', 
     'H':'u2', 
     'i':'i4', 
     'I':'u4', 
     'l':'i4', 
     'L':'u4', 
     'q':'i8', 
     'Q':'u8', 
     'e':'f2', 
     'f':'f', 
     'd':'d', 
     'Zf':'F', 
     'Zd':'D', 
     's':'S', 
     'w':'U', 
     'O':'O', 
     'x':'V'}
    _pep3118_standard_typechars = ''.join(_pep3118_standard_map.keys())
    _pep3118_unsupported_map = {'u':'UCS-2 strings', 
     '&':'pointers', 
     't':'bitfields', 
     'X':'function pointers'}

    class _Stream:

        def __init__(self, s):
            self.s = s
            self.byteorder = '@'

        def advance(self, n):
            res = self.s[:n]
            self.s = self.s[n:]
            return res

        def consume(self, c):
            if self.s[:len(c)] == c:
                self.advance(len(c))
                return True
            return False

        def consume_until(self, c):
            if callable(c):
                i = 0
                while True:
                    if i < len(self.s):
                        i = (c(self.s[i]) or i) + 1

                return self.advance(i)
            i = self.s.index(c)
            res = self.advance(i)
            self.advance(len(c))
            return res

        @property
        def next(self):
            return self.s[0]

        def __bool__(self):
            return bool(self.s)


    def _dtype_from_pep3118(spec):
        stream = _Stream(spec)
        dtype, align = __dtype_from_pep3118(stream, is_subdtype=False)
        return dtype


    def __dtype_from_pep3118(stream, is_subdtype):
        field_spec = dict(names=[], formats=[], offsets=[], itemsize=0)
        offset = 0
        common_alignment = 1
        is_padding = False
        while True:
            if stream:
                value = None
                if stream.consume('}'):
                    pass
                else:
                    shape = None
                    if stream.consume('('):
                        shape = stream.consume_until(')')
                        shape = tuple(map(int, shape.split(',')))
                    if stream.next in ('@', '=', '<', '>', '^', '!'):
                        byteorder = stream.advance(1)
                        if byteorder == '!':
                            byteorder = '>'
                        stream.byteorder = byteorder
                    if stream.byteorder in ('@', '^'):
                        type_map = _pep3118_native_map
                        type_map_chars = _pep3118_native_typechars
                    else:
                        type_map = _pep3118_standard_map
                        type_map_chars = _pep3118_standard_typechars
                    itemsize_str = stream.consume_until(lambda c: not c.isdigit())
                    if itemsize_str:
                        itemsize = int(itemsize_str)
                    else:
                        itemsize = 1
                    is_padding = False
                    if stream.consume('T{'):
                        value, align = __dtype_from_pep3118(stream,
                          is_subdtype=True)
                    elif stream.next in type_map_chars:
                        if stream.next == 'Z':
                            typechar = stream.advance(2)
                        else:
                            typechar = stream.advance(1)
                        is_padding = typechar == 'x'
                        dtypechar = type_map[typechar]
                        if dtypechar in 'USV':
                            dtypechar += '%d' % itemsize
                            itemsize = 1
                        numpy_byteorder = {'@':'=', 
                         '^':'='}.get(stream.byteorder, stream.byteorder)
                        value = dtype(numpy_byteorder + dtypechar)
                        align = value.alignment
                    elif stream.next in _pep3118_unsupported_map:
                        desc = _pep3118_unsupported_map[stream.next]
                        raise NotImplementedError('Unrepresentable PEP 3118 data type {!r} ({})'.format(stream.next, desc))
                    else:
                        raise ValueError('Unknown PEP 3118 data type specifier %r' % stream.s)
                    extra_offset = 0
                    if stream.byteorder == '@':
                        start_padding = -offset % align
                        intra_padding = -value.itemsize % align
                        offset += start_padding
                        if not intra_padding != 0 and (itemsize > 1 or shape) is not None or _prod(shape) > 1:
                            value = _add_trailing_padding(value, intra_padding)
                        else:
                            extra_offset += intra_padding
                        common_alignment = _lcm(align, common_alignment)
                    if itemsize != 1:
                        value = dtype((value, (itemsize,)))
                    if shape is not None:
                        value = dtype((value, shape))
                    if stream.consume(':'):
                        name = stream.consume_until(':')
                    else:
                        name = None
                    if not (is_padding and name is None):
                        if name is not None:
                            if name in field_spec['names']:
                                raise RuntimeError(f"Duplicate field name '{name}' in PEP3118 format")
                        field_spec['names'].append(name)
                        field_spec['formats'].append(value)
                        field_spec['offsets'].append(offset)
                    offset += value.itemsize
                    offset += extra_offset
                    field_spec['itemsize'] = offset

        if stream.byteorder == '@':
            field_spec['itemsize'] += -offset % common_alignment
        if field_spec['names'] == [None]:
            if field_spec['offsets'][0] == 0:
                if field_spec['itemsize'] == field_spec['formats'][0].itemsize and not is_subdtype:
                    ret = field_spec['formats'][0]
                else:
                    _fix_names(field_spec)
                    ret = dtype(field_spec)
            return (
             ret, common_alignment)


    def _fix_names(field_spec):
        """ Replace names which are None with the next unused f%d name """
        names = field_spec['names']
        for i, name in enumerate(names):
            if name is not None:
                pass
            else:
                j = 0
                while True:
                    name = f"f{j}"
                    if name not in names:
                        pass
                    else:
                        j = j + 1

                names[i] = name


    def _add_trailing_padding(value, padding):
        """Inject the specified number of padding bytes at the end of a dtype"""
        if value.fields is None:
            field_spec = dict(names=[
             'f0'],
              formats=[
             value],
              offsets=[
             0],
              itemsize=(value.itemsize))
        else:
            fields = value.fields
            names = value.names
            field_spec = dict(names=names,
              formats=[fields[name][0] for name in names],
              offsets=[fields[name][1] for name in names],
              itemsize=(value.itemsize))
        field_spec['itemsize'] += padding
        return dtype(field_spec)


    def _prod(a):
        p = 1
        for x in a:
            p *= x
        else:
            return p


    def _gcd(a, b):
        """Calculate the greatest common divisor of a and b"""
        while True:
            if b:
                a, b = b, a % b

        return a


    def _lcm(a, b):
        return a // _gcd(a, b) * b


    def array_ufunc_errmsg_formatter(dummy, ufunc, method, *inputs, **kwargs):
        """ Format the error message for when __array_ufunc__ gives up. """
        args_string = ', '.join(['{!r}'.format(arg) for arg in inputs] + ['{}={!r}'.format(k, v) for k, v in kwargs.items()])
        args = inputs + kwargs.get('out', ())
        types_string = ', '.join((repr(type(arg).__name__) for arg in args))
        return 'operand type(s) all returned NotImplemented from __array_ufunc__({!r}, {!r}, {}): {}'.format(ufunc, method, args_string, types_string)


    def array_function_errmsg_formatter(public_api, types):
        """ Format the error message for when __array_ufunc__ gives up. """
        func_name = '{}.{}'.format(public_api.__module__, public_api.__name__)
        return "no implementation found for '{}' on types that implement __array_function__: {}".format(func_name, list(types))


    def _ufunc_doc_signature_formatter(ufunc):
        """
    Builds a signature string which resembles PEP 457

    This is used to construct the first line of the docstring
    """
        if ufunc.nin == 1:
            in_args = 'x'
        else:
            in_args = ', '.join((f"x{i + 1}" for i in range(ufunc.nin)))
        if ufunc.nout == 0:
            out_args = ', /, out=()'
        elif ufunc.nout == 1:
            out_args = ', /, out=None'
        else:
            out_args = '[, {positional}], / [, out={default}]'.format(positional=(', '.join(('out{}'.format(i + 1) for i in range(ufunc.nout)))),
              default=(repr((None, ) * ufunc.nout)))
        kwargs = ", casting='same_kind', order='K', dtype=None, subok=True[, signature, extobj]"
        if ufunc.signature is None:
            kwargs = ', where=True' + kwargs
        return '{name}({in_args}{out_args}, *{kwargs})'.format(name=(ufunc.__name__),
          in_args=in_args,
          out_args=out_args,
          kwargs=kwargs)


    def npy_ctypes_check--- This code section failed: ---

 L. 829         0  SETUP_FINALLY        40  'to 40'

 L. 832         2  LOAD_GLOBAL              IS_PYPY
                4  POP_JUMP_IF_FALSE    18  'to 18'

 L. 834         6  LOAD_FAST                'cls'
                8  LOAD_ATTR                __mro__
               10  LOAD_CONST               -3
               12  BINARY_SUBSCR    
               14  STORE_FAST               'ctype_base'
               16  JUMP_FORWARD         28  'to 28'
             18_0  COME_FROM             4  '4'

 L. 837        18  LOAD_FAST                'cls'
               20  LOAD_ATTR                __mro__
               22  LOAD_CONST               -2
               24  BINARY_SUBSCR    
               26  STORE_FAST               'ctype_base'
             28_0  COME_FROM            16  '16'

 L. 839        28  LOAD_STR                 '_ctypes'
               30  LOAD_FAST                'ctype_base'
               32  LOAD_ATTR                __module__
               34  COMPARE_OP               in
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY     0  '0'

 L. 840        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    60  'to 60'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 841        54  POP_EXCEPT       
               56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            46  '46'
               60  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 56


    class recursive:
        __doc__ = '\n    A decorator class for recursive nested functions.\n    Naive recursive nested functions hold a reference to themselves:\n\n    def outer(*args):\n        def stringify_leaky(arg0, *arg1):\n            if len(arg1) > 0:\n                return stringify_leaky(*arg1)  # <- HERE\n            return str(arg0)\n        stringify_leaky(*args)\n\n    This design pattern creates a reference cycle that is difficult for a\n    garbage collector to resolve. The decorator class prevents the\n    cycle by passing the nested function in as an argument `self`:\n\n    def outer(*args):\n        @recursive\n        def stringify(self, arg0, *arg1):\n            if len(arg1) > 0:\n                return self(*arg1)\n            return str(arg0)\n        stringify(*args)\n\n    '

        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            return (self.func)(self, *args, **kwargs)