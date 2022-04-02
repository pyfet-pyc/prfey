# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\core\_exceptions.py
"""
Various richly-typed exceptions, that also help us deal with string formatting
in python where it's easier.

By putting the formatting in `__str__`, we also avoid paying the cost for
users who silence the exceptions.
"""
from numpy.core.overrides import set_module

def _unpack_tuple(tup):
    if len(tup) == 1:
        return tup[0]
    return tup


def _display_as_base--- This code section failed: ---

 L.  27         0  LOAD_GLOBAL              issubclass
                2  LOAD_FAST                'cls'
                4  LOAD_GLOBAL              Exception
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L.  28        14  LOAD_FAST                'cls'
               16  LOAD_ATTR                __base__
               18  LOAD_ATTR                __name__
               20  LOAD_FAST                'cls'
               22  STORE_ATTR               __name__

 L.  29        24  LOAD_FAST                'cls'
               26  LOAD_ATTR                __base__
               28  LOAD_ATTR                __qualname__
               30  LOAD_FAST                'cls'
               32  STORE_ATTR               __qualname__

 L.  30        34  LOAD_GLOBAL              set_module
               36  LOAD_FAST                'cls'
               38  LOAD_ATTR                __base__
               40  LOAD_ATTR                __module__
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_FAST                'cls'
               46  CALL_FUNCTION_1       1  ''
               48  POP_TOP          

 L.  31        50  LOAD_FAST                'cls'
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class UFuncTypeError(TypeError):
    __doc__ = ' Base class for all ufunc exceptions '

    def __init__(self, ufunc):
        self.ufunc = ufunc


@_display_as_base
class _UFuncBinaryResolutionError(UFuncTypeError):
    __doc__ = ' Thrown when a binary resolution fails '

    def __init__--- This code section failed: ---

 L.  44         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __init__
                6  LOAD_FAST                'ufunc'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L.  45        12  LOAD_GLOBAL              tuple
               14  LOAD_FAST                'dtypes'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'self'
               20  STORE_ATTR               dtypes

 L.  46        22  LOAD_GLOBAL              len
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                dtypes
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               2
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_TRUE     40  'to 40'
               36  <74>             
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'

Parse error at or near `<74>' instruction at offset 36

    def __str__--- This code section failed: ---

 L.  50         0  LOAD_STR                 'ufunc {!r} cannot use operands with types {!r} and {!r}'

 L.  49         2  LOAD_ATTR                format

 L.  52         4  LOAD_FAST                'self'
                6  LOAD_ATTR                ufunc
                8  LOAD_ATTR                __name__

 L.  49        10  BUILD_LIST_1          1 

 L.  52        12  LOAD_FAST                'self'
               14  LOAD_ATTR                dtypes

 L.  49        16  CALL_FINALLY         19  'to 19'
               18  WITH_CLEANUP_FINISH
               20  CALL_FUNCTION_EX      0  'positional arguments only'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 16


@_display_as_base
class _UFuncNoLoopError(UFuncTypeError):
    __doc__ = ' Thrown when a ufunc loop cannot be found '

    def __init__(self, ufunc, dtypes):
        super.__init__ufunc
        self.dtypes = tuple(dtypes)

    def __str__(self):
        return 'ufunc {!r} did not contain a loop with signature matching types {!r} -> {!r}'.format(self.ufunc.__name__, _unpack_tuple(self.dtypes[:self.ufunc.nin]), _unpack_tuple(self.dtypes[self.ufunc.nin:]))


@_display_as_base
class _UFuncCastingError(UFuncTypeError):

    def __init__(self, ufunc, casting, from_, to):
        super.__init__ufunc
        self.casting = casting
        self.from_ = from_
        self.to = to


@_display_as_base
class _UFuncInputCastingError(_UFuncCastingError):
    __doc__ = ' Thrown when a ufunc input cannot be casted '

    def __init__(self, ufunc, casting, from_, to, i):
        super.__init__(ufunc, casting, from_, to)
        self.in_i = i

    def __str__(self):
        i_str = '{} '.formatself.in_i if self.ufunc.nin != 1 else ''
        return 'Cannot cast ufunc {!r} input {}from {!r} to {!r} with casting rule {!r}'.format(self.ufunc.__name__, i_str, self.from_, self.to, self.casting)


@_display_as_base
class _UFuncOutputCastingError(_UFuncCastingError):
    __doc__ = ' Thrown when a ufunc output cannot be casted '

    def __init__(self, ufunc, casting, from_, to, i):
        super.__init__(ufunc, casting, from_, to)
        self.out_i = i

    def __str__(self):
        i_str = '{} '.formatself.out_i if self.ufunc.nout != 1 else ''
        return 'Cannot cast ufunc {!r} output {}from {!r} to {!r} with casting rule {!r}'.format(self.ufunc.__name__, i_str, self.from_, self.to, self.casting)


@set_module('numpy')
class TooHardError(RuntimeError):
    pass


@set_module('numpy')
class AxisError(ValueError, IndexError):
    __doc__ = ' Axis supplied was invalid. '

    def __init__--- This code section failed: ---

 L. 130         0  LOAD_FAST                'ndim'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'
                8  LOAD_FAST                'msg_prefix'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    22  'to 22'

 L. 131        16  LOAD_FAST                'axis'
               18  STORE_FAST               'msg'
               20  JUMP_FORWARD         54  'to 54'
             22_0  COME_FROM            14  '14'
             22_1  COME_FROM             6  '6'

 L. 135        22  LOAD_STR                 'axis {} is out of bounds for array of dimension {}'
               24  LOAD_METHOD              format

 L. 136        26  LOAD_FAST                'axis'
               28  LOAD_FAST                'ndim'

 L. 135        30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'msg'

 L. 137        34  LOAD_FAST                'msg_prefix'
               36  LOAD_CONST               None
               38  <117>                 1  ''
               40  POP_JUMP_IF_FALSE    54  'to 54'

 L. 138        42  LOAD_STR                 '{}: {}'
               44  LOAD_METHOD              format
               46  LOAD_FAST                'msg_prefix'
               48  LOAD_FAST                'msg'
               50  CALL_METHOD_2         2  ''
               52  STORE_FAST               'msg'
             54_0  COME_FROM            40  '40'
             54_1  COME_FROM            20  '20'

 L. 140        54  LOAD_GLOBAL              super
               56  LOAD_GLOBAL              AxisError
               58  LOAD_FAST                'self'
               60  CALL_FUNCTION_2       2  ''
               62  LOAD_METHOD              __init__
               64  LOAD_FAST                'msg'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

Parse error at or near `None' instruction at offset -1


@_display_as_base
class _ArrayMemoryError(MemoryError):
    __doc__ = ' Thrown when an array cannot be allocated'

    def __init__(self, shape, dtype):
        self.shape = shape
        self.dtype = dtype

    @property
    def _total_size(self):
        num_bytes = self.dtype.itemsize
        for dim in self.shape:
            num_bytes *= dim
        else:
            return num_bytes

    @staticmethod
    def _size_to_string--- This code section failed: ---

 L. 162         0  LOAD_CONST               10
                2  STORE_FAST               'LOG2_STEP'

 L. 163         4  LOAD_CONST               1024
                6  STORE_FAST               'STEP'

 L. 164         8  BUILD_LIST_0          0 
               10  LOAD_CONST               ('bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB')
               12  CALL_FINALLY         15  'to 15'
               14  STORE_FAST               'units'

 L. 166        16  LOAD_GLOBAL              max
               18  LOAD_FAST                'num_bytes'
               20  LOAD_METHOD              bit_length
               22  CALL_METHOD_0         0  ''
               24  LOAD_CONST               1
               26  BINARY_SUBTRACT  
               28  LOAD_CONST               1
               30  CALL_FUNCTION_2       2  ''
               32  LOAD_FAST                'LOG2_STEP'
               34  BINARY_FLOOR_DIVIDE
               36  STORE_FAST               'unit_i'

 L. 167        38  LOAD_CONST               1
               40  LOAD_FAST                'unit_i'
               42  LOAD_FAST                'LOG2_STEP'
               44  BINARY_MULTIPLY  
               46  BINARY_LSHIFT    
               48  STORE_FAST               'unit_val'

 L. 168        50  LOAD_FAST                'num_bytes'
               52  LOAD_FAST                'unit_val'
               54  BINARY_TRUE_DIVIDE
               56  STORE_FAST               'n_units'

 L. 169        58  DELETE_FAST              'unit_val'

 L. 172        60  LOAD_GLOBAL              round
               62  LOAD_FAST                'n_units'
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_FAST                'STEP'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    88  'to 88'

 L. 173        72  LOAD_FAST                'unit_i'
               74  LOAD_CONST               1
               76  INPLACE_ADD      
               78  STORE_FAST               'unit_i'

 L. 174        80  LOAD_FAST                'n_units'
               82  LOAD_FAST                'STEP'
               84  INPLACE_TRUE_DIVIDE
               86  STORE_FAST               'n_units'
             88_0  COME_FROM            70  '70'

 L. 177        88  LOAD_FAST                'unit_i'
               90  LOAD_GLOBAL              len
               92  LOAD_FAST                'units'
               94  CALL_FUNCTION_1       1  ''
               96  COMPARE_OP               >=
               98  POP_JUMP_IF_FALSE   136  'to 136'

 L. 178       100  LOAD_GLOBAL              len
              102  LOAD_FAST                'units'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_CONST               1
              108  BINARY_SUBTRACT  
              110  STORE_FAST               'new_unit_i'

 L. 179       112  LOAD_FAST                'n_units'
              114  LOAD_CONST               1
              116  LOAD_FAST                'unit_i'
              118  LOAD_FAST                'new_unit_i'
              120  BINARY_SUBTRACT  
              122  LOAD_FAST                'LOG2_STEP'
              124  BINARY_MULTIPLY  
              126  BINARY_LSHIFT    
              128  INPLACE_MULTIPLY 
              130  STORE_FAST               'n_units'

 L. 180       132  LOAD_FAST                'new_unit_i'
              134  STORE_FAST               'unit_i'
            136_0  COME_FROM            98  '98'

 L. 182       136  LOAD_FAST                'units'
              138  LOAD_FAST                'unit_i'
              140  BINARY_SUBSCR    
              142  STORE_FAST               'unit_name'

 L. 184       144  LOAD_FAST                'unit_i'
              146  LOAD_CONST               0
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   164  'to 164'

 L. 186       152  LOAD_STR                 '{:.0f} {}'
              154  LOAD_METHOD              format
              156  LOAD_FAST                'n_units'
              158  LOAD_FAST                'unit_name'
              160  CALL_METHOD_2         2  ''
              162  RETURN_VALUE     
            164_0  COME_FROM           150  '150'

 L. 187       164  LOAD_GLOBAL              round
              166  LOAD_FAST                'n_units'
              168  CALL_FUNCTION_1       1  ''
              170  LOAD_CONST               1000
              172  COMPARE_OP               <
              174  POP_JUMP_IF_FALSE   188  'to 188'

 L. 189       176  LOAD_STR                 '{:#.3g} {}'
              178  LOAD_METHOD              format
              180  LOAD_FAST                'n_units'
              182  LOAD_FAST                'unit_name'
              184  CALL_METHOD_2         2  ''
              186  RETURN_VALUE     
            188_0  COME_FROM           174  '174'

 L. 192       188  LOAD_STR                 '{:#.0f} {}'
              190  LOAD_METHOD              format
              192  LOAD_FAST                'n_units'
              194  LOAD_FAST                'unit_name'
              196  CALL_METHOD_2         2  ''
              198  RETURN_VALUE     

Parse error at or near `CALL_FINALLY' instruction at offset 12

    def __str__(self):
        size_str = self._size_to_stringself._total_size
        return 'Unable to allocate {} for an array with shape {} and data type {}'.format(size_str, self.shape, self.dtype)