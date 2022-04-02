# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cffi\cffi_opcode.py
from .error import VerificationError

class CffiOp(object):

    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

    def as_c_expr--- This code section failed: ---

 L.   9         0  LOAD_FAST                'self'
                2  LOAD_ATTR                op
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    38  'to 38'

 L.  10        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                arg
               16  LOAD_GLOBAL              str
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'
               22  <74>             
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L.  11        26  LOAD_STR                 '(_cffi_opcode_t)(%s)'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                arg
               32  BUILD_TUPLE_1         1 
               34  BINARY_MODULO    
               36  RETURN_VALUE     
             38_0  COME_FROM             8  '8'

 L.  12        38  LOAD_GLOBAL              CLASS_NAME
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                op
               44  BINARY_SUBSCR    
               46  STORE_FAST               'classname'

 L.  13        48  LOAD_STR                 '_CFFI_OP(_CFFI_OP_%s, %s)'
               50  LOAD_FAST                'classname'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                arg
               56  BUILD_TUPLE_2         2 
               58  BINARY_MODULO    
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def as_python_bytes--- This code section failed: ---

 L.  16         0  LOAD_FAST                'self'
                2  LOAD_ATTR                op
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    62  'to 62'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                arg
               14  LOAD_METHOD              isdigit
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_FALSE    62  'to 62'

 L.  17        20  LOAD_GLOBAL              int
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                arg
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'value'

 L.  18        30  LOAD_FAST                'value'
               32  LOAD_CONST               2147483648
               34  COMPARE_OP               >=
               36  POP_JUMP_IF_FALSE    54  'to 54'

 L.  19        38  LOAD_GLOBAL              OverflowError
               40  LOAD_STR                 'cannot emit %r: limited to 2**31-1'

 L.  20        42  LOAD_FAST                'self'
               44  LOAD_ATTR                arg
               46  BUILD_TUPLE_1         1 

 L.  19        48  BINARY_MODULO    
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            36  '36'

 L.  21        54  LOAD_GLOBAL              format_four_bytes
               56  LOAD_FAST                'value'
               58  CALL_FUNCTION_1       1  ''
               60  RETURN_VALUE     
             62_0  COME_FROM            18  '18'
             62_1  COME_FROM             8  '8'

 L.  22        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                arg
               68  LOAD_GLOBAL              str
               70  CALL_FUNCTION_2       2  ''
               72  POP_JUMP_IF_FALSE    90  'to 90'

 L.  23        74  LOAD_GLOBAL              VerificationError
               76  LOAD_STR                 'cannot emit to Python: %r'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                arg
               82  BUILD_TUPLE_1         1 
               84  BINARY_MODULO    
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            72  '72'

 L.  24        90  LOAD_GLOBAL              format_four_bytes
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                arg
               96  LOAD_CONST               8
               98  BINARY_LSHIFT    
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                op
              104  BINARY_OR        
              106  CALL_FUNCTION_1       1  ''
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __str__(self):
        classname = CLASS_NAME.get(self.op, self.op)
        return '(%s %s)' % (classname, self.arg)


def format_four_bytes(num):
    return '\\x%02X\\x%02X\\x%02X\\x%02X' % (
     num >> 24 & 255,
     num >> 16 & 255,
     num >> 8 & 255,
     num & 255)


OP_PRIMITIVE = 1
OP_POINTER = 3
OP_ARRAY = 5
OP_OPEN_ARRAY = 7
OP_STRUCT_UNION = 9
OP_ENUM = 11
OP_FUNCTION = 13
OP_FUNCTION_END = 15
OP_NOOP = 17
OP_BITFIELD = 19
OP_TYPENAME = 21
OP_CPYTHON_BLTN_V = 23
OP_CPYTHON_BLTN_N = 25
OP_CPYTHON_BLTN_O = 27
OP_CONSTANT = 29
OP_CONSTANT_INT = 31
OP_GLOBAL_VAR = 33
OP_DLOPEN_FUNC = 35
OP_DLOPEN_CONST = 37
OP_GLOBAL_VAR_F = 39
OP_EXTERN_PYTHON = 41
PRIM_VOID = 0
PRIM_BOOL = 1
PRIM_CHAR = 2
PRIM_SCHAR = 3
PRIM_UCHAR = 4
PRIM_SHORT = 5
PRIM_USHORT = 6
PRIM_INT = 7
PRIM_UINT = 8
PRIM_LONG = 9
PRIM_ULONG = 10
PRIM_LONGLONG = 11
PRIM_ULONGLONG = 12
PRIM_FLOAT = 13
PRIM_DOUBLE = 14
PRIM_LONGDOUBLE = 15
PRIM_WCHAR = 16
PRIM_INT8 = 17
PRIM_UINT8 = 18
PRIM_INT16 = 19
PRIM_UINT16 = 20
PRIM_INT32 = 21
PRIM_UINT32 = 22
PRIM_INT64 = 23
PRIM_UINT64 = 24
PRIM_INTPTR = 25
PRIM_UINTPTR = 26
PRIM_PTRDIFF = 27
PRIM_SIZE = 28
PRIM_SSIZE = 29
PRIM_INT_LEAST8 = 30
PRIM_UINT_LEAST8 = 31
PRIM_INT_LEAST16 = 32
PRIM_UINT_LEAST16 = 33
PRIM_INT_LEAST32 = 34
PRIM_UINT_LEAST32 = 35
PRIM_INT_LEAST64 = 36
PRIM_UINT_LEAST64 = 37
PRIM_INT_FAST8 = 38
PRIM_UINT_FAST8 = 39
PRIM_INT_FAST16 = 40
PRIM_UINT_FAST16 = 41
PRIM_INT_FAST32 = 42
PRIM_UINT_FAST32 = 43
PRIM_INT_FAST64 = 44
PRIM_UINT_FAST64 = 45
PRIM_INTMAX = 46
PRIM_UINTMAX = 47
PRIM_FLOATCOMPLEX = 48
PRIM_DOUBLECOMPLEX = 49
PRIM_CHAR16 = 50
PRIM_CHAR32 = 51
_NUM_PRIM = 52
_UNKNOWN_PRIM = -1
_UNKNOWN_FLOAT_PRIM = -2
_UNKNOWN_LONG_DOUBLE = -3
_IO_FILE_STRUCT = -1
PRIMITIVE_TO_INDEX = {'char':PRIM_CHAR, 
 'short':PRIM_SHORT, 
 'int':PRIM_INT, 
 'long':PRIM_LONG, 
 'long long':PRIM_LONGLONG, 
 'signed char':PRIM_SCHAR, 
 'unsigned char':PRIM_UCHAR, 
 'unsigned short':PRIM_USHORT, 
 'unsigned int':PRIM_UINT, 
 'unsigned long':PRIM_ULONG, 
 'unsigned long long':PRIM_ULONGLONG, 
 'float':PRIM_FLOAT, 
 'double':PRIM_DOUBLE, 
 'long double':PRIM_LONGDOUBLE, 
 'float _Complex':PRIM_FLOATCOMPLEX, 
 'double _Complex':PRIM_DOUBLECOMPLEX, 
 '_Bool':PRIM_BOOL, 
 'wchar_t':PRIM_WCHAR, 
 'char16_t':PRIM_CHAR16, 
 'char32_t':PRIM_CHAR32, 
 'int8_t':PRIM_INT8, 
 'uint8_t':PRIM_UINT8, 
 'int16_t':PRIM_INT16, 
 'uint16_t':PRIM_UINT16, 
 'int32_t':PRIM_INT32, 
 'uint32_t':PRIM_UINT32, 
 'int64_t':PRIM_INT64, 
 'uint64_t':PRIM_UINT64, 
 'intptr_t':PRIM_INTPTR, 
 'uintptr_t':PRIM_UINTPTR, 
 'ptrdiff_t':PRIM_PTRDIFF, 
 'size_t':PRIM_SIZE, 
 'ssize_t':PRIM_SSIZE, 
 'int_least8_t':PRIM_INT_LEAST8, 
 'uint_least8_t':PRIM_UINT_LEAST8, 
 'int_least16_t':PRIM_INT_LEAST16, 
 'uint_least16_t':PRIM_UINT_LEAST16, 
 'int_least32_t':PRIM_INT_LEAST32, 
 'uint_least32_t':PRIM_UINT_LEAST32, 
 'int_least64_t':PRIM_INT_LEAST64, 
 'uint_least64_t':PRIM_UINT_LEAST64, 
 'int_fast8_t':PRIM_INT_FAST8, 
 'uint_fast8_t':PRIM_UINT_FAST8, 
 'int_fast16_t':PRIM_INT_FAST16, 
 'uint_fast16_t':PRIM_UINT_FAST16, 
 'int_fast32_t':PRIM_INT_FAST32, 
 'uint_fast32_t':PRIM_UINT_FAST32, 
 'int_fast64_t':PRIM_INT_FAST64, 
 'uint_fast64_t':PRIM_UINT_FAST64, 
 'intmax_t':PRIM_INTMAX, 
 'uintmax_t':PRIM_UINTMAX}
F_UNION = 1
F_CHECK_FIELDS = 2
F_PACKED = 4
F_EXTERNAL = 8
F_OPAQUE = 16
G_FLAGS = dict([('_CFFI_' + _key, globals()[_key]) for _key in ('F_UNION', 'F_CHECK_FIELDS',
                                                                'F_PACKED', 'F_EXTERNAL',
                                                                'F_OPAQUE')])
CLASS_NAME = {}
for _name, _value in list(globals().items()):
    if _name.startswith('OP_'):
        if isinstance(_value, int):
            CLASS_NAME[_value] = _name[3:]