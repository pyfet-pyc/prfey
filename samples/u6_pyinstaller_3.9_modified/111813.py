# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cffi\model.py
import types, weakref
from .lock import allocate_lock
from .error import CDefError, VerificationError, VerificationMissing
Q_CONST = 1
Q_RESTRICT = 2
Q_VOLATILE = 4

def qualify(quals, replace_with):
    if quals & Q_CONST:
        replace_with = ' const ' + replace_with.lstrip()
    if quals & Q_VOLATILE:
        replace_with = ' volatile ' + replace_with.lstrip()
    if quals & Q_RESTRICT:
        replace_with = ' __restrict ' + replace_with.lstrip()
    return replace_with


class BaseTypeByIdentity(object):
    is_array_type = False
    is_raw_function = False

    def get_c_name--- This code section failed: ---

 L.  30         0  LOAD_FAST                'self'
                2  LOAD_ATTR                c_name_with_marker
                4  STORE_FAST               'result'

 L.  31         6  LOAD_FAST                'result'
                8  LOAD_METHOD              count
               10  LOAD_STR                 '&'
               12  CALL_METHOD_1         1  ''
               14  LOAD_CONST               1
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_TRUE     24  'to 24'
               20  <74>             
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'

 L.  33        24  LOAD_FAST                'replace_with'
               26  LOAD_METHOD              strip
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'replace_with'

 L.  34        32  LOAD_FAST                'replace_with'
               34  POP_JUMP_IF_FALSE    84  'to 84'

 L.  35        36  LOAD_FAST                'replace_with'
               38  LOAD_METHOD              startswith
               40  LOAD_STR                 '*'
               42  CALL_METHOD_1         1  ''
               44  POP_JUMP_IF_FALSE    64  'to 64'
               46  LOAD_STR                 '&['
               48  LOAD_FAST                'result'
               50  <118>                 0  ''
               52  POP_JUMP_IF_FALSE    64  'to 64'

 L.  36        54  LOAD_STR                 '(%s)'
               56  LOAD_FAST                'replace_with'
               58  BINARY_MODULO    
               60  STORE_FAST               'replace_with'
               62  JUMP_FORWARD         84  'to 84'
             64_0  COME_FROM            52  '52'
             64_1  COME_FROM            44  '44'

 L.  37        64  LOAD_FAST                'replace_with'
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  LOAD_STR                 '[('
               72  <118>                 1  ''
               74  POP_JUMP_IF_FALSE    84  'to 84'

 L.  38        76  LOAD_STR                 ' '
               78  LOAD_FAST                'replace_with'
               80  BINARY_ADD       
               82  STORE_FAST               'replace_with'
             84_0  COME_FROM            74  '74'
             84_1  COME_FROM            62  '62'
             84_2  COME_FROM            34  '34'

 L.  39        84  LOAD_GLOBAL              qualify
               86  LOAD_FAST                'quals'
               88  LOAD_FAST                'replace_with'
               90  CALL_FUNCTION_2       2  ''
               92  STORE_FAST               'replace_with'

 L.  40        94  LOAD_FAST                'result'
               96  LOAD_METHOD              replace
               98  LOAD_STR                 '&'
              100  LOAD_FAST                'replace_with'
              102  CALL_METHOD_2         2  ''
              104  STORE_FAST               'result'

 L.  41       106  LOAD_STR                 '$'
              108  LOAD_FAST                'result'
              110  <118>                 0  ''
              112  POP_JUMP_IF_FALSE   134  'to 134'

 L.  42       114  LOAD_GLOBAL              VerificationError

 L.  43       116  LOAD_STR                 "cannot generate '%s' in %s: unknown type name"

 L.  44       118  LOAD_FAST                'self'
              120  LOAD_METHOD              _get_c_name
              122  CALL_METHOD_0         0  ''
              124  LOAD_FAST                'context'
              126  BUILD_TUPLE_2         2 

 L.  43       128  BINARY_MODULO    

 L.  42       130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           112  '112'

 L.  45       134  LOAD_FAST                'result'
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 20

    def _get_c_name(self):
        return self.c_name_with_marker.replace'&'''

    def has_c_name--- This code section failed: ---

 L.  51         0  LOAD_STR                 '$'
                2  LOAD_FAST                'self'
                4  LOAD_METHOD              _get_c_name
                6  CALL_METHOD_0         0  ''
                8  <118>                 1  ''
               10  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def is_integer_type(self):
        return False

    def get_cached_btype--- This code section failed: ---

 L.  57         0  SETUP_FINALLY        16  'to 16'

 L.  58         2  LOAD_FAST                'ffi'
                4  LOAD_ATTR                _cached_btypes
                6  LOAD_FAST                'self'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'BType'
               12  POP_BLOCK        
               14  JUMP_FORWARD         72  'to 72'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  59        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                70  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  60        28  LOAD_FAST                'self'
               30  LOAD_METHOD              build_backend_type
               32  LOAD_FAST                'ffi'
               34  LOAD_FAST                'finishlist'
               36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'BType'

 L.  61        40  LOAD_FAST                'ffi'
               42  LOAD_ATTR                _cached_btypes
               44  LOAD_METHOD              setdefault
               46  LOAD_FAST                'self'
               48  LOAD_FAST                'BType'
               50  CALL_METHOD_2         2  ''
               52  STORE_FAST               'BType2'

 L.  62        54  LOAD_FAST                'BType2'
               56  LOAD_FAST                'BType'
               58  <117>                 0  ''
               60  POP_JUMP_IF_TRUE     66  'to 66'
               62  <74>             
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            60  '60'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            14  '14'

 L.  63        72  LOAD_FAST                'BType'
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 20

    def __repr__(self):
        return '<%s>' % (self._get_c_name(),)

    def _get_items(self):
        return [(name, getattr(self, name)) for name in self._attrs_]


class BaseType(BaseTypeByIdentity):

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._get_items() == other._get_items()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.__class__, tuple(self._get_items())))


class VoidType(BaseType):
    _attrs_ = ()

    def __init__(self):
        self.c_name_with_marker = 'void&'

    def build_backend_type(self, ffi, finishlist):
        return global_cache(self, ffi, 'new_void_type')


void_type = VoidType()

class BasePrimitiveType(BaseType):

    def is_complex_type(self):
        return False


class PrimitiveType(BasePrimitiveType):
    _attrs_ = ('name', )
    ALL_PRIMITIVE_TYPES = {'char':'c', 
     'short':'i', 
     'int':'i', 
     'long':'i', 
     'long long':'i', 
     'signed char':'i', 
     'unsigned char':'i', 
     'unsigned short':'i', 
     'unsigned int':'i', 
     'unsigned long':'i', 
     'unsigned long long':'i', 
     'float':'f', 
     'double':'f', 
     'long double':'f', 
     'float _Complex':'j', 
     'double _Complex':'j', 
     '_Bool':'i', 
     'wchar_t':'c', 
     'char16_t':'c', 
     'char32_t':'c', 
     'int8_t':'i', 
     'uint8_t':'i', 
     'int16_t':'i', 
     'uint16_t':'i', 
     'int32_t':'i', 
     'uint32_t':'i', 
     'int64_t':'i', 
     'uint64_t':'i', 
     'int_least8_t':'i', 
     'uint_least8_t':'i', 
     'int_least16_t':'i', 
     'uint_least16_t':'i', 
     'int_least32_t':'i', 
     'uint_least32_t':'i', 
     'int_least64_t':'i', 
     'uint_least64_t':'i', 
     'int_fast8_t':'i', 
     'uint_fast8_t':'i', 
     'int_fast16_t':'i', 
     'uint_fast16_t':'i', 
     'int_fast32_t':'i', 
     'uint_fast32_t':'i', 
     'int_fast64_t':'i', 
     'uint_fast64_t':'i', 
     'intptr_t':'i', 
     'uintptr_t':'i', 
     'intmax_t':'i', 
     'uintmax_t':'i', 
     'ptrdiff_t':'i', 
     'size_t':'i', 
     'ssize_t':'i'}

    def __init__--- This code section failed: ---

 L. 161         0  LOAD_FAST                'name'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                ALL_PRIMITIVE_TYPES
                6  <118>                 0  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 162        14  LOAD_FAST                'name'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               name

 L. 163        20  LOAD_FAST                'name'
               22  LOAD_STR                 '&'
               24  BINARY_ADD       
               26  LOAD_FAST                'self'
               28  STORE_ATTR               c_name_with_marker

Parse error at or near `None' instruction at offset -1

    def is_char_type(self):
        return self.ALL_PRIMITIVE_TYPES[self.name] == 'c'

    def is_integer_type(self):
        return self.ALL_PRIMITIVE_TYPES[self.name] == 'i'

    def is_float_type(self):
        return self.ALL_PRIMITIVE_TYPES[self.name] == 'f'

    def is_complex_type(self):
        return self.ALL_PRIMITIVE_TYPES[self.name] == 'j'

    def build_backend_type(self, ffi, finishlist):
        return global_cache(self, ffi, 'new_primitive_type', self.name)


class UnknownIntegerType(BasePrimitiveType):
    _attrs_ = ('name', )

    def __init__(self, name):
        self.name = name
        self.c_name_with_marker = name + '&'

    def is_integer_type(self):
        return True

    def build_backend_type(self, ffi, finishlist):
        raise NotImplementedError("integer type '%s' can only be used after compilation" % self.name)


class UnknownFloatType(BasePrimitiveType):
    _attrs_ = ('name', )

    def __init__(self, name):
        self.name = name
        self.c_name_with_marker = name + '&'

    def build_backend_type(self, ffi, finishlist):
        raise NotImplementedError("float type '%s' can only be used after compilation" % self.name)


class BaseFunctionType(BaseType):
    _attrs_ = ('args', 'result', 'ellipsis', 'abi')

    def __init__--- This code section failed: ---

 L. 208         0  LOAD_FAST                'args'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               args

 L. 209         6  LOAD_FAST                'result'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               result

 L. 210        12  LOAD_FAST                'ellipsis'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               ellipsis

 L. 211        18  LOAD_FAST                'abi'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               abi

 L. 213        24  LOAD_LISTCOMP            '<code_object <listcomp>>'
               26  LOAD_STR                 'BaseFunctionType.__init__.<locals>.<listcomp>'
               28  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                args
               34  GET_ITER         
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'reprargs'

 L. 214        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ellipsis
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 215        46  LOAD_FAST                'reprargs'
               48  LOAD_METHOD              append
               50  LOAD_STR                 '...'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            44  '44'

 L. 216        56  LOAD_FAST                'reprargs'
               58  JUMP_IF_TRUE_OR_POP    64  'to 64'
               60  LOAD_STR                 'void'
               62  BUILD_LIST_1          1 
             64_0  COME_FROM            58  '58'
               64  STORE_FAST               'reprargs'

 L. 217        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _base_pattern
               70  LOAD_STR                 ', '
               72  LOAD_METHOD              join
               74  LOAD_FAST                'reprargs'
               76  CALL_METHOD_1         1  ''
               78  BUILD_TUPLE_1         1 
               80  BINARY_MODULO    
               82  STORE_FAST               'replace_with'

 L. 218        84  LOAD_FAST                'abi'
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   124  'to 124'

 L. 219        92  LOAD_FAST                'replace_with'
               94  LOAD_CONST               None
               96  LOAD_CONST               1
               98  BUILD_SLICE_2         2 
              100  BINARY_SUBSCR    
              102  LOAD_FAST                'abi'
              104  BINARY_ADD       
              106  LOAD_STR                 ' '
              108  BINARY_ADD       
              110  LOAD_FAST                'replace_with'
              112  LOAD_CONST               1
              114  LOAD_CONST               None
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  BINARY_ADD       
              122  STORE_FAST               'replace_with'
            124_0  COME_FROM            90  '90'

 L. 221       124  LOAD_FAST                'self'
              126  LOAD_ATTR                result
              128  LOAD_ATTR                c_name_with_marker
              130  LOAD_METHOD              replace
              132  LOAD_STR                 '&'
              134  LOAD_FAST                'replace_with'
              136  CALL_METHOD_2         2  ''

 L. 220       138  LOAD_FAST                'self'
              140  STORE_ATTR               c_name_with_marker

Parse error at or near `<117>' instruction at offset 88


class RawFunctionType(BaseFunctionType):
    _base_pattern = '(&)(%s)'
    is_raw_function = True

    def build_backend_type(self, ffi, finishlist):
        raise CDefError('cannot render the type %r: it is a function type, not a pointer-to-function type' % (
         self,))

    def as_function_pointer(self):
        return FunctionPtrType(self.args, self.result, self.ellipsis, self.abi)


class FunctionPtrType(BaseFunctionType):
    _base_pattern = '(*&)(%s)'

    def build_backend_type--- This code section failed: ---

 L. 243         0  LOAD_FAST                'self'
                2  LOAD_ATTR                result
                4  LOAD_METHOD              get_cached_btype
                6  LOAD_FAST                'ffi'
                8  LOAD_FAST                'finishlist'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'result'

 L. 244        14  BUILD_LIST_0          0 
               16  STORE_FAST               'args'

 L. 245        18  LOAD_FAST                'self'
               20  LOAD_ATTR                args
               22  GET_ITER         
               24  FOR_ITER             48  'to 48'
               26  STORE_FAST               'tp'

 L. 246        28  LOAD_FAST                'args'
               30  LOAD_METHOD              append
               32  LOAD_FAST                'tp'
               34  LOAD_METHOD              get_cached_btype
               36  LOAD_FAST                'ffi'
               38  LOAD_FAST                'finishlist'
               40  CALL_METHOD_2         2  ''
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
               46  JUMP_BACK            24  'to 24'

 L. 247        48  LOAD_CONST               ()
               50  STORE_FAST               'abi_args'

 L. 248        52  LOAD_FAST                'self'
               54  LOAD_ATTR                abi
               56  LOAD_STR                 '__stdcall'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE   102  'to 102'

 L. 249        62  LOAD_FAST                'self'
               64  LOAD_ATTR                ellipsis
               66  POP_JUMP_IF_TRUE    102  'to 102'

 L. 250        68  SETUP_FINALLY        84  'to 84'

 L. 251        70  LOAD_FAST                'ffi'
               72  LOAD_ATTR                _backend
               74  LOAD_ATTR                FFI_STDCALL
               76  BUILD_TUPLE_1         1 
               78  STORE_FAST               'abi_args'
               80  POP_BLOCK        
               82  JUMP_FORWARD        102  'to 102'
             84_0  COME_FROM_FINALLY    68  '68'

 L. 252        84  DUP_TOP          
               86  LOAD_GLOBAL              AttributeError
               88  <121>               100  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 253        96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
              100  <48>             
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            82  '82'
            102_2  COME_FROM            66  '66'
            102_3  COME_FROM            60  '60'

 L. 254       102  LOAD_GLOBAL              global_cache
              104  LOAD_FAST                'self'
              106  LOAD_FAST                'ffi'
              108  LOAD_STR                 'new_function_type'

 L. 255       110  LOAD_GLOBAL              tuple
              112  LOAD_FAST                'args'
              114  CALL_FUNCTION_1       1  ''
              116  LOAD_FAST                'result'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                ellipsis

 L. 254       122  BUILD_LIST_6          6 

 L. 255       124  LOAD_FAST                'abi_args'

 L. 254       126  CALL_FINALLY        129  'to 129'
              128  WITH_CLEANUP_FINISH
              130  CALL_FUNCTION_EX      0  'positional arguments only'
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 88

    def as_raw_function(self):
        return RawFunctionType(self.args, self.result, self.ellipsis, self.abi)


class PointerType(BaseType):
    _attrs_ = ('totype', 'quals')

    def __init__(self, totype, quals=0):
        self.totype = totype
        self.quals = quals
        extra = qualify(quals, ' *&')
        if totype.is_array_type:
            extra = '(%s)' % (extra.lstrip(),)
        self.c_name_with_marker = totype.c_name_with_marker.replace'&'extra

    def build_backend_type(self, ffi, finishlist):
        BItem = self.totype.get_cached_btype(ffi, finishlist, can_delay=True)
        return global_cache(self, ffi, 'new_pointer_type', BItem)


voidp_type = PointerType(void_type)

def ConstPointerType(totype):
    return PointerType(totype, Q_CONST)


const_voidp_type = ConstPointerType(void_type)

class NamedPointerType(PointerType):
    _attrs_ = ('totype', 'name')

    def __init__(self, totype, name, quals=0):
        PointerType.__init__(self, totype, quals)
        self.name = name
        self.c_name_with_marker = name + '&'


class ArrayType(BaseType):
    _attrs_ = ('item', 'length')
    is_array_type = True

    def __init__--- This code section failed: ---

 L. 298         0  LOAD_FAST                'item'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               item

 L. 299         6  LOAD_FAST                'length'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               length

 L. 301        12  LOAD_FAST                'length'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    26  'to 26'

 L. 302        20  LOAD_STR                 '&[]'
               22  STORE_FAST               'brackets'
               24  JUMP_FORWARD         48  'to 48'
             26_0  COME_FROM            18  '18'

 L. 303        26  LOAD_FAST                'length'
               28  LOAD_STR                 '...'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L. 304        34  LOAD_STR                 '&[/*...*/]'
               36  STORE_FAST               'brackets'
               38  JUMP_FORWARD         48  'to 48'
             40_0  COME_FROM            32  '32'

 L. 306        40  LOAD_STR                 '&[%s]'
               42  LOAD_FAST                'length'
               44  BINARY_MODULO    
               46  STORE_FAST               'brackets'
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            24  '24'

 L. 308        48  LOAD_FAST                'self'
               50  LOAD_ATTR                item
               52  LOAD_ATTR                c_name_with_marker
               54  LOAD_METHOD              replace
               56  LOAD_STR                 '&'
               58  LOAD_FAST                'brackets'
               60  CALL_METHOD_2         2  ''

 L. 307        62  LOAD_FAST                'self'
               64  STORE_ATTR               c_name_with_marker

Parse error at or near `<117>' instruction at offset 16

    def length_is_unknown(self):
        return isinstance(self.length, str)

    def resolve_length(self, newlength):
        return ArrayType(self.item, newlength)

    def build_backend_type(self, ffi, finishlist):
        if self.length_is_unknown():
            raise CDefError('cannot render the type %r: unknown length' % (
             self,))
        self.item.get_cached_btypeffifinishlist
        BPtrItem = PointerType(self.item).get_cached_btypeffifinishlist
        return global_cache(self, ffi, 'new_array_type', BPtrItem, self.length)


char_array_type = ArrayType(PrimitiveType('char'), None)

class StructOrUnionOrEnum(BaseTypeByIdentity):
    _attrs_ = ('name', )
    forcename = None

    def build_c_name_with_marker(self):
        name = self.forcename or '%s %s' % (self.kind, self.name)
        self.c_name_with_marker = name + '&'

    def force_the_name(self, forcename):
        self.forcename = forcename
        self.build_c_name_with_marker()

    def get_official_name--- This code section failed: ---

 L. 340         0  LOAD_FAST                'self'
                2  LOAD_ATTR                c_name_with_marker
                4  LOAD_METHOD              endswith
                6  LOAD_STR                 '&'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 341        16  LOAD_FAST                'self'
               18  LOAD_ATTR                c_name_with_marker
               20  LOAD_CONST               None
               22  LOAD_CONST               -1
               24  BUILD_SLICE_2         2 
               26  BINARY_SUBSCR    
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class StructOrUnion(StructOrUnionOrEnum):
    fixedlayout = None
    completed = 0
    partial = False
    packed = 0

    def __init__(self, name, fldnames, fldtypes, fldbitsize, fldquals=None):
        self.name = name
        self.fldnames = fldnames
        self.fldtypes = fldtypes
        self.fldbitsize = fldbitsize
        self.fldquals = fldquals
        self.build_c_name_with_marker()

    def anonymous_struct_fields--- This code section failed: ---

 L. 359         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fldtypes
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    58  'to 58'

 L. 360        10  LOAD_GLOBAL              zip
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                fldnames
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                fldtypes
               20  CALL_FUNCTION_2       2  ''
               22  GET_ITER         
             24_0  COME_FROM            48  '48'
             24_1  COME_FROM            38  '38'
               24  FOR_ITER             58  'to 58'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'name'
               30  STORE_FAST               'type'

 L. 361        32  LOAD_FAST                'name'
               34  LOAD_STR                 ''
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    24  'to 24'
               40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'type'
               44  LOAD_GLOBAL              StructOrUnion
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    24  'to 24'

 L. 362        50  LOAD_FAST                'type'
               52  YIELD_VALUE      
               54  POP_TOP          
               56  JUMP_BACK            24  'to 24'
             58_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def enumfields--- This code section failed: ---

 L. 365         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fldquals
                4  STORE_FAST               'fldquals'

 L. 366         6  LOAD_FAST                'fldquals'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    28  'to 28'

 L. 367        14  LOAD_CONST               (0,)
               16  LOAD_GLOBAL              len
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                fldnames
               22  CALL_FUNCTION_1       1  ''
               24  BINARY_MULTIPLY  
               26  STORE_FAST               'fldquals'
             28_0  COME_FROM            12  '12'

 L. 368        28  LOAD_GLOBAL              zip
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                fldnames
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                fldtypes

 L. 369        38  LOAD_FAST                'self'
               40  LOAD_ATTR                fldbitsize
               42  LOAD_FAST                'fldquals'

 L. 368        44  CALL_FUNCTION_4       4  ''
               46  GET_ITER         
               48  FOR_ITER            120  'to 120'
               50  UNPACK_SEQUENCE_4     4 
               52  STORE_FAST               'name'
               54  STORE_FAST               'type'
               56  STORE_FAST               'bitsize'
               58  STORE_FAST               'quals'

 L. 370        60  LOAD_FAST                'name'
               62  LOAD_STR                 ''
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE   104  'to 104'
               68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'type'
               72  LOAD_GLOBAL              StructOrUnion
               74  CALL_FUNCTION_2       2  ''
               76  POP_JUMP_IF_FALSE   104  'to 104'

 L. 371        78  LOAD_FAST                'expand_anonymous_struct_union'

 L. 370        80  POP_JUMP_IF_FALSE   104  'to 104'

 L. 373        82  LOAD_FAST                'type'
               84  LOAD_METHOD              enumfields
               86  CALL_METHOD_0         0  ''
               88  GET_ITER         
               90  FOR_ITER            102  'to 102'
               92  STORE_FAST               'result'

 L. 374        94  LOAD_FAST                'result'
               96  YIELD_VALUE      
               98  POP_TOP          
              100  JUMP_BACK            90  'to 90'
              102  JUMP_BACK            48  'to 48'
            104_0  COME_FROM            80  '80'
            104_1  COME_FROM            76  '76'
            104_2  COME_FROM            66  '66'

 L. 376       104  LOAD_FAST                'name'
              106  LOAD_FAST                'type'
              108  LOAD_FAST                'bitsize'
              110  LOAD_FAST                'quals'
              112  BUILD_TUPLE_4         4 
              114  YIELD_VALUE      
              116  POP_TOP          
              118  JUMP_BACK            48  'to 48'

Parse error at or near `<117>' instruction at offset 10

    def force_flatten(self):
        names = []
        types = []
        bitsizes = []
        fldquals = []
        for name, type, bitsize, quals in self.enumfields():
            names.appendname
            types.appendtype
            bitsizes.appendbitsize
            fldquals.appendquals
        else:
            self.fldnames = tuple(names)
            self.fldtypes = tuple(types)
            self.fldbitsize = tuple(bitsizes)
            self.fldquals = tuple(fldquals)

    def get_cached_btype(self, ffi, finishlist, can_delay=False):
        BType = StructOrUnionOrEnum.get_cached_btype(self, ffi, finishlist, can_delay)
        if not can_delay:
            self.finish_backend_typeffifinishlist
        return BType

    def finish_backend_type--- This code section failed: ---

 L. 404         0  LOAD_FAST                'self'
                2  LOAD_ATTR                completed
                4  POP_JUMP_IF_FALSE    36  'to 36'

 L. 405         6  LOAD_FAST                'self'
                8  LOAD_ATTR                completed
               10  LOAD_CONST               2
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    32  'to 32'

 L. 406        16  LOAD_GLOBAL              NotImplementedError
               18  LOAD_STR                 "recursive structure declaration for '%s'"

 L. 407        20  LOAD_FAST                'self'
               22  LOAD_ATTR                name
               24  BUILD_TUPLE_1         1 

 L. 406        26  BINARY_MODULO    
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            14  '14'

 L. 408        32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM             4  '4'

 L. 409        36  LOAD_DEREF               'ffi'
               38  LOAD_ATTR                _cached_btypes
               40  LOAD_FAST                'self'
               42  BINARY_SUBSCR    
               44  STORE_FAST               'BType'

 L. 411        46  LOAD_CONST               1
               48  LOAD_FAST                'self'
               50  STORE_ATTR               completed

 L. 413        52  LOAD_FAST                'self'
               54  LOAD_ATTR                fldtypes
               56  LOAD_CONST               None
               58  <117>                 0  ''
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L. 414     62_64  JUMP_FORWARD        552  'to 552'
             66_0  COME_FROM            60  '60'

 L. 416        66  LOAD_FAST                'self'
               68  LOAD_ATTR                fixedlayout
               70  LOAD_CONST               None
               72  <117>                 0  ''
               74  POP_JUMP_IF_FALSE   186  'to 186'

 L. 417        76  LOAD_CLOSURE             'ffi'
               78  LOAD_CLOSURE             'finishlist'
               80  BUILD_TUPLE_2         2 
               82  LOAD_LISTCOMP            '<code_object <listcomp>>'
               84  LOAD_STR                 'StructOrUnion.finish_backend_type.<locals>.<listcomp>'
               86  MAKE_FUNCTION_8          'closure'

 L. 418        88  LOAD_FAST                'self'
               90  LOAD_ATTR                fldtypes

 L. 417        92  GET_ITER         
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'fldtypes'

 L. 419        98  LOAD_GLOBAL              list
              100  LOAD_GLOBAL              zip
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                fldnames
              106  LOAD_FAST                'fldtypes'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                fldbitsize
              112  CALL_FUNCTION_3       3  ''
              114  CALL_FUNCTION_1       1  ''
              116  STORE_FAST               'lst'

 L. 420       118  LOAD_CONST               ()
              120  STORE_FAST               'extra_flags'

 L. 421       122  LOAD_FAST                'self'
              124  LOAD_ATTR                packed
              126  POP_JUMP_IF_FALSE   154  'to 154'

 L. 422       128  LOAD_FAST                'self'
              130  LOAD_ATTR                packed
              132  LOAD_CONST               1
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   144  'to 144'

 L. 423       138  LOAD_CONST               (8,)
              140  STORE_FAST               'extra_flags'
              142  JUMP_FORWARD        154  'to 154'
            144_0  COME_FROM           136  '136'

 L. 425       144  LOAD_CONST               0
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                packed
              150  BUILD_TUPLE_2         2 
              152  STORE_FAST               'extra_flags'
            154_0  COME_FROM           142  '142'
            154_1  COME_FROM           126  '126'

 L. 426       154  LOAD_DEREF               'ffi'
              156  LOAD_ATTR                _backend
              158  LOAD_ATTR                complete_struct_or_union
              160  LOAD_FAST                'BType'
              162  LOAD_FAST                'lst'
              164  LOAD_FAST                'self'

 L. 427       166  LOAD_CONST               -1
              168  LOAD_CONST               -1

 L. 426       170  BUILD_LIST_5          5 

 L. 427       172  LOAD_FAST                'extra_flags'

 L. 426       174  CALL_FINALLY        177  'to 177'
              176  WITH_CLEANUP_FINISH
              178  CALL_FUNCTION_EX      0  'positional arguments only'
              180  POP_TOP          
          182_184  JUMP_FORWARD        552  'to 552'
            186_0  COME_FROM            74  '74'

 L. 430       186  BUILD_LIST_0          0 
              188  STORE_FAST               'fldtypes'

 L. 431       190  LOAD_FAST                'self'
              192  LOAD_ATTR                fixedlayout
              194  UNPACK_SEQUENCE_4     4 
              196  STORE_FAST               'fieldofs'
              198  STORE_FAST               'fieldsize'
              200  STORE_FAST               'totalsize'
              202  STORE_FAST               'totalalignment'

 L. 432       204  LOAD_GLOBAL              range
              206  LOAD_GLOBAL              len
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                fldnames
              212  CALL_FUNCTION_1       1  ''
              214  CALL_FUNCTION_1       1  ''
              216  GET_ITER         
          218_220  FOR_ITER            510  'to 510'
              222  STORE_FAST               'i'

 L. 433       224  LOAD_FAST                'fieldsize'
              226  LOAD_FAST                'i'
              228  BINARY_SUBSCR    
              230  STORE_FAST               'fsize'

 L. 434       232  LOAD_FAST                'self'
              234  LOAD_ATTR                fldtypes
              236  LOAD_FAST                'i'
              238  BINARY_SUBSCR    
              240  STORE_FAST               'ftype'

 L. 436       242  LOAD_GLOBAL              isinstance
              244  LOAD_FAST                'ftype'
              246  LOAD_GLOBAL              ArrayType
              248  CALL_FUNCTION_2       2  ''
          250_252  POP_JUMP_IF_FALSE   390  'to 390'
              254  LOAD_FAST                'ftype'
              256  LOAD_METHOD              length_is_unknown
              258  CALL_METHOD_0         0  ''
          260_262  POP_JUMP_IF_FALSE   390  'to 390'

 L. 438       264  LOAD_FAST                'ftype'
              266  LOAD_ATTR                item
              268  LOAD_METHOD              get_cached_btype
              270  LOAD_DEREF               'ffi'
              272  LOAD_DEREF               'finishlist'
              274  CALL_METHOD_2         2  ''
              276  STORE_FAST               'BItemType'

 L. 439       278  LOAD_GLOBAL              divmod
              280  LOAD_FAST                'fsize'
              282  LOAD_DEREF               'ffi'
              284  LOAD_METHOD              sizeof
              286  LOAD_FAST                'BItemType'
              288  CALL_METHOD_1         1  ''
              290  CALL_FUNCTION_2       2  ''
              292  UNPACK_SEQUENCE_2     2 
              294  STORE_FAST               'nlen'
              296  STORE_FAST               'nrest'

 L. 440       298  LOAD_FAST                'nrest'
              300  LOAD_CONST               0
              302  COMPARE_OP               !=
          304_306  POP_JUMP_IF_FALSE   340  'to 340'

 L. 441       308  LOAD_FAST                'self'
              310  LOAD_METHOD              _verification_error

 L. 442       312  LOAD_STR                 "field '%s.%s' has a bogus size?"

 L. 443       314  LOAD_FAST                'self'
              316  LOAD_ATTR                name
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                fldnames
              322  LOAD_FAST                'i'
              324  BINARY_SUBSCR    
          326_328  JUMP_IF_TRUE_OR_POP   332  'to 332'
              330  LOAD_STR                 '{}'
            332_0  COME_FROM           326  '326'

 L. 442       332  BUILD_TUPLE_2         2 
              334  BINARY_MODULO    

 L. 441       336  CALL_METHOD_1         1  ''
              338  POP_TOP          
            340_0  COME_FROM           304  '304'

 L. 444       340  LOAD_FAST                'ftype'
              342  LOAD_METHOD              resolve_length
              344  LOAD_FAST                'nlen'
              346  CALL_METHOD_1         1  ''
              348  STORE_FAST               'ftype'

 L. 445       350  LOAD_FAST                'self'
              352  LOAD_ATTR                fldtypes
              354  LOAD_CONST               None
              356  LOAD_FAST                'i'
              358  BUILD_SLICE_2         2 
              360  BINARY_SUBSCR    
              362  LOAD_FAST                'ftype'
              364  BUILD_TUPLE_1         1 
              366  BINARY_ADD       

 L. 446       368  LOAD_FAST                'self'
              370  LOAD_ATTR                fldtypes
              372  LOAD_FAST                'i'
              374  LOAD_CONST               1
              376  BINARY_ADD       
              378  LOAD_CONST               None
              380  BUILD_SLICE_2         2 
              382  BINARY_SUBSCR    

 L. 445       384  BINARY_ADD       
              386  LOAD_FAST                'self'
              388  STORE_ATTR               fldtypes
            390_0  COME_FROM           260  '260'
            390_1  COME_FROM           250  '250'

 L. 448       390  LOAD_FAST                'ftype'
              392  LOAD_METHOD              get_cached_btype
              394  LOAD_DEREF               'ffi'
              396  LOAD_DEREF               'finishlist'
              398  CALL_METHOD_2         2  ''
              400  STORE_FAST               'BFieldType'

 L. 449       402  LOAD_GLOBAL              isinstance
              404  LOAD_FAST                'ftype'
              406  LOAD_GLOBAL              ArrayType
              408  CALL_FUNCTION_2       2  ''
          410_412  POP_JUMP_IF_FALSE   442  'to 442'
              414  LOAD_FAST                'ftype'
              416  LOAD_ATTR                length
              418  LOAD_CONST               None
              420  <117>                 0  ''
          422_424  POP_JUMP_IF_FALSE   442  'to 442'

 L. 450       426  LOAD_FAST                'fsize'
              428  LOAD_CONST               0
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_TRUE    498  'to 498'
              436  <74>             
              438  RAISE_VARARGS_1       1  'exception instance'
              440  JUMP_FORWARD        498  'to 498'
            442_0  COME_FROM           422  '422'
            442_1  COME_FROM           410  '410'

 L. 452       442  LOAD_DEREF               'ffi'
              444  LOAD_METHOD              sizeof
              446  LOAD_FAST                'BFieldType'
              448  CALL_METHOD_1         1  ''
              450  STORE_FAST               'bitemsize'

 L. 453       452  LOAD_FAST                'bitemsize'
              454  LOAD_FAST                'fsize'
              456  COMPARE_OP               !=
          458_460  POP_JUMP_IF_FALSE   498  'to 498'

 L. 454       462  LOAD_FAST                'self'
              464  LOAD_METHOD              _verification_error

 L. 455       466  LOAD_STR                 "field '%s.%s' is declared as %d bytes, but is really %d bytes"

 L. 456       468  LOAD_FAST                'self'
              470  LOAD_ATTR                name

 L. 457       472  LOAD_FAST                'self'
              474  LOAD_ATTR                fldnames
              476  LOAD_FAST                'i'
              478  BINARY_SUBSCR    
          480_482  JUMP_IF_TRUE_OR_POP   486  'to 486'
              484  LOAD_STR                 '{}'
            486_0  COME_FROM           480  '480'

 L. 458       486  LOAD_FAST                'bitemsize'
              488  LOAD_FAST                'fsize'

 L. 456       490  BUILD_TUPLE_4         4 

 L. 455       492  BINARY_MODULO    

 L. 454       494  CALL_METHOD_1         1  ''
              496  POP_TOP          
            498_0  COME_FROM           458  '458'
            498_1  COME_FROM           440  '440'
            498_2  COME_FROM           432  '432'

 L. 459       498  LOAD_FAST                'fldtypes'
              500  LOAD_METHOD              append
              502  LOAD_FAST                'BFieldType'
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          
              508  JUMP_BACK           218  'to 218'

 L. 461       510  LOAD_GLOBAL              list
              512  LOAD_GLOBAL              zip
              514  LOAD_FAST                'self'
              516  LOAD_ATTR                fldnames
              518  LOAD_FAST                'fldtypes'
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                fldbitsize
              524  LOAD_FAST                'fieldofs'
              526  CALL_FUNCTION_4       4  ''
              528  CALL_FUNCTION_1       1  ''
              530  STORE_FAST               'lst'

 L. 462       532  LOAD_DEREF               'ffi'
              534  LOAD_ATTR                _backend
              536  LOAD_METHOD              complete_struct_or_union
              538  LOAD_FAST                'BType'
              540  LOAD_FAST                'lst'
              542  LOAD_FAST                'self'

 L. 463       544  LOAD_FAST                'totalsize'
              546  LOAD_FAST                'totalalignment'

 L. 462       548  CALL_METHOD_5         5  ''
              550  POP_TOP          
            552_0  COME_FROM           182  '182'
            552_1  COME_FROM            62  '62'

 L. 464       552  LOAD_CONST               2
              554  LOAD_FAST                'self'
              556  STORE_ATTR               completed

Parse error at or near `<117>' instruction at offset 58

    def _verification_error(self, msg):
        raise VerificationError(msg)

    def check_not_partial--- This code section failed: ---

 L. 470         0  LOAD_FAST                'self'
                2  LOAD_ATTR                partial
                4  POP_JUMP_IF_FALSE    28  'to 28'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                fixedlayout
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    28  'to 28'

 L. 471        16  LOAD_GLOBAL              VerificationMissing
               18  LOAD_FAST                'self'
               20  LOAD_METHOD              _get_c_name
               22  CALL_METHOD_0         0  ''
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            14  '14'
             28_1  COME_FROM             4  '4'

Parse error at or near `None' instruction at offset -1

    def build_backend_type(self, ffi, finishlist):
        self.check_not_partial()
        finishlist.appendself
        return global_cache(self, ffi, ('new_%s_type' % self.kind), (self.get_official_name()),
          key=self)


class StructType(StructOrUnion):
    kind = 'struct'


class UnionType(StructOrUnion):
    kind = 'union'


class EnumType(StructOrUnionOrEnum):
    kind = 'enum'
    partial = False
    partial_resolved = False

    def __init__(self, name, enumerators, enumvalues, baseinttype=None):
        self.name = name
        self.enumerators = enumerators
        self.enumvalues = enumvalues
        self.baseinttype = baseinttype
        self.build_c_name_with_marker()

    def force_the_name--- This code section failed: ---

 L. 502         0  LOAD_GLOBAL              StructOrUnionOrEnum
                2  LOAD_METHOD              force_the_name
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'forcename'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 503        12  LOAD_FAST                'self'
               14  LOAD_ATTR                forcename
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    48  'to 48'

 L. 504        22  LOAD_FAST                'self'
               24  LOAD_METHOD              get_official_name
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'name'

 L. 505        30  LOAD_STR                 '$'
               32  LOAD_FAST                'name'
               34  LOAD_METHOD              replace
               36  LOAD_STR                 ' '
               38  LOAD_STR                 '_'
               40  CALL_METHOD_2         2  ''
               42  BINARY_ADD       
               44  LOAD_FAST                'self'
               46  STORE_ATTR               forcename
             48_0  COME_FROM            20  '20'

Parse error at or near `<117>' instruction at offset 18

    def check_not_partial(self):
        if self.partial:
            if not self.partial_resolved:
                raise VerificationMissing(self._get_c_name())

    def build_backend_type(self, ffi, finishlist):
        self.check_not_partial()
        base_btype = self.build_baseinttypeffifinishlist
        return global_cache(self, ffi, 'new_enum_type', (self.get_official_name()),
          (self.enumerators),
          (self.enumvalues), base_btype,
          key=self)

    def build_baseinttype--- This code section failed: ---

 L. 520         0  LOAD_FAST                'self'
                2  LOAD_ATTR                baseinttype
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 521        10  LOAD_FAST                'self'
               12  LOAD_ATTR                baseinttype
               14  LOAD_METHOD              get_cached_btype
               16  LOAD_FAST                'ffi'
               18  LOAD_FAST                'finishlist'
               20  CALL_METHOD_2         2  ''
               22  RETURN_VALUE     
             24_0  COME_FROM             8  '8'

 L. 523        24  LOAD_FAST                'self'
               26  LOAD_ATTR                enumvalues
               28  POP_JUMP_IF_FALSE    52  'to 52'

 L. 524        30  LOAD_GLOBAL              min
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                enumvalues
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'smallest_value'

 L. 525        40  LOAD_GLOBAL              max
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                enumvalues
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'largest_value'
               50  JUMP_FORWARD        118  'to 118'
             52_0  COME_FROM            28  '28'

 L. 527        52  LOAD_CONST               0
               54  LOAD_CONST               None
               56  IMPORT_NAME              warnings
               58  STORE_FAST               'warnings'

 L. 528        60  SETUP_FINALLY        74  'to 74'

 L. 532        62  LOAD_GLOBAL              __warningregistry__
               64  LOAD_METHOD              clear
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          
               70  POP_BLOCK        
               72  JUMP_FORWARD         92  'to 92'
             74_0  COME_FROM_FINALLY    60  '60'

 L. 533        74  DUP_TOP          
               76  LOAD_GLOBAL              NameError
               78  <121>                90  ''
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 534        86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
               90  <48>             
             92_0  COME_FROM            88  '88'
             92_1  COME_FROM            72  '72'

 L. 535        92  LOAD_FAST                'warnings'
               94  LOAD_METHOD              warn
               96  LOAD_STR                 "%r has no values explicitly defined; guessing that it is equivalent to 'unsigned int'"

 L. 537        98  LOAD_FAST                'self'
              100  LOAD_METHOD              _get_c_name
              102  CALL_METHOD_0         0  ''

 L. 535       104  BINARY_MODULO    
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 538       110  LOAD_CONST               0
              112  DUP_TOP          
              114  STORE_FAST               'smallest_value'
              116  STORE_FAST               'largest_value'
            118_0  COME_FROM            50  '50'

 L. 539       118  LOAD_FAST                'smallest_value'
              120  LOAD_CONST               0
              122  COMPARE_OP               <
              124  POP_JUMP_IF_FALSE   148  'to 148'

 L. 540       126  LOAD_CONST               1
              128  STORE_FAST               'sign'

 L. 541       130  LOAD_GLOBAL              PrimitiveType
              132  LOAD_STR                 'int'
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'candidate1'

 L. 542       138  LOAD_GLOBAL              PrimitiveType
              140  LOAD_STR                 'long'
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'candidate2'
              146  JUMP_FORWARD        168  'to 168'
            148_0  COME_FROM           124  '124'

 L. 544       148  LOAD_CONST               0
              150  STORE_FAST               'sign'

 L. 545       152  LOAD_GLOBAL              PrimitiveType
              154  LOAD_STR                 'unsigned int'
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'candidate1'

 L. 546       160  LOAD_GLOBAL              PrimitiveType
              162  LOAD_STR                 'unsigned long'
              164  CALL_FUNCTION_1       1  ''
              166  STORE_FAST               'candidate2'
            168_0  COME_FROM           146  '146'

 L. 547       168  LOAD_FAST                'candidate1'
              170  LOAD_METHOD              get_cached_btype
              172  LOAD_FAST                'ffi'
              174  LOAD_FAST                'finishlist'
              176  CALL_METHOD_2         2  ''
              178  STORE_FAST               'btype1'

 L. 548       180  LOAD_FAST                'candidate2'
              182  LOAD_METHOD              get_cached_btype
              184  LOAD_FAST                'ffi'
              186  LOAD_FAST                'finishlist'
              188  CALL_METHOD_2         2  ''
              190  STORE_FAST               'btype2'

 L. 549       192  LOAD_FAST                'ffi'
              194  LOAD_METHOD              sizeof
              196  LOAD_FAST                'btype1'
              198  CALL_METHOD_1         1  ''
              200  STORE_FAST               'size1'

 L. 550       202  LOAD_FAST                'ffi'
              204  LOAD_METHOD              sizeof
              206  LOAD_FAST                'btype2'
              208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'size2'

 L. 551       212  LOAD_FAST                'smallest_value'
              214  LOAD_CONST               -1
              216  LOAD_CONST               8
              218  LOAD_FAST                'size1'
              220  BINARY_MULTIPLY  
              222  LOAD_CONST               1
              224  BINARY_SUBTRACT  
              226  BINARY_LSHIFT    
              228  COMPARE_OP               >=
          230_232  POP_JUMP_IF_FALSE   260  'to 260'

 L. 552       234  LOAD_FAST                'largest_value'
              236  LOAD_CONST               1
              238  LOAD_CONST               8
              240  LOAD_FAST                'size1'
              242  BINARY_MULTIPLY  
              244  LOAD_FAST                'sign'
              246  BINARY_SUBTRACT  
              248  BINARY_LSHIFT    
              250  COMPARE_OP               <

 L. 551   252_254  POP_JUMP_IF_FALSE   260  'to 260'

 L. 553       256  LOAD_FAST                'btype1'
              258  RETURN_VALUE     
            260_0  COME_FROM           252  '252'
            260_1  COME_FROM           230  '230'

 L. 554       260  LOAD_FAST                'smallest_value'
              262  LOAD_CONST               -1
              264  LOAD_CONST               8
              266  LOAD_FAST                'size2'
              268  BINARY_MULTIPLY  
              270  LOAD_CONST               1
              272  BINARY_SUBTRACT  
              274  BINARY_LSHIFT    
              276  COMPARE_OP               >=
          278_280  POP_JUMP_IF_FALSE   308  'to 308'

 L. 555       282  LOAD_FAST                'largest_value'
              284  LOAD_CONST               1
              286  LOAD_CONST               8
              288  LOAD_FAST                'size2'
              290  BINARY_MULTIPLY  
              292  LOAD_FAST                'sign'
              294  BINARY_SUBTRACT  
              296  BINARY_LSHIFT    
              298  COMPARE_OP               <

 L. 554   300_302  POP_JUMP_IF_FALSE   308  'to 308'

 L. 556       304  LOAD_FAST                'btype2'
              306  RETURN_VALUE     
            308_0  COME_FROM           300  '300'
            308_1  COME_FROM           278  '278'

 L. 557       308  LOAD_GLOBAL              CDefError
              310  LOAD_STR                 "%s values don't all fit into either 'long' or 'unsigned long'"

 L. 558       312  LOAD_FAST                'self'
              314  LOAD_METHOD              _get_c_name
              316  CALL_METHOD_0         0  ''

 L. 557       318  BINARY_MODULO    
              320  CALL_FUNCTION_1       1  ''
              322  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `None' instruction at offset -1


def unknown_type--- This code section failed: ---

 L. 561         0  LOAD_FAST                'structname'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 562         8  LOAD_STR                 '$%s'
               10  LOAD_FAST                'name'
               12  BINARY_MODULO    
               14  STORE_FAST               'structname'
             16_0  COME_FROM             6  '6'

 L. 563        16  LOAD_GLOBAL              StructType
               18  LOAD_FAST                'structname'
               20  LOAD_CONST               None
               22  LOAD_CONST               None
               24  LOAD_CONST               None
               26  CALL_FUNCTION_4       4  ''
               28  STORE_FAST               'tp'

 L. 564        30  LOAD_FAST                'tp'
               32  LOAD_METHOD              force_the_name
               34  LOAD_FAST                'name'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 565        40  LOAD_STR                 'unknown_type'
               42  LOAD_FAST                'tp'
               44  STORE_ATTR               origin

 L. 566        46  LOAD_FAST                'tp'
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def unknown_ptr_type--- This code section failed: ---

 L. 569         0  LOAD_FAST                'structname'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 570         8  LOAD_STR                 '$$%s'
               10  LOAD_FAST                'name'
               12  BINARY_MODULO    
               14  STORE_FAST               'structname'
             16_0  COME_FROM             6  '6'

 L. 571        16  LOAD_GLOBAL              StructType
               18  LOAD_FAST                'structname'
               20  LOAD_CONST               None
               22  LOAD_CONST               None
               24  LOAD_CONST               None
               26  CALL_FUNCTION_4       4  ''
               28  STORE_FAST               'tp'

 L. 572        30  LOAD_GLOBAL              NamedPointerType
               32  LOAD_FAST                'tp'
               34  LOAD_FAST                'name'
               36  CALL_FUNCTION_2       2  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


global_lock = allocate_lock()
_typecache_cffi_backend = weakref.WeakValueDictionary()

def get_typecache--- This code section failed: ---

 L. 582         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'backend'
                4  LOAD_GLOBAL              types
                6  LOAD_ATTR                ModuleType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 583        12  LOAD_GLOBAL              _typecache_cffi_backend
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 584        16  LOAD_GLOBAL              global_lock
               18  SETUP_WITH           74  'to 74'
               20  POP_TOP          

 L. 585        22  LOAD_GLOBAL              hasattr
               24  LOAD_GLOBAL              type
               26  LOAD_FAST                'backend'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_STR                 '__typecache'
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_TRUE     50  'to 50'

 L. 586        36  LOAD_GLOBAL              weakref
               38  LOAD_METHOD              WeakValueDictionary
               40  CALL_METHOD_0         0  ''
               42  LOAD_GLOBAL              type
               44  LOAD_FAST                'backend'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_ATTR               __typecache
             50_0  COME_FROM            34  '34'

 L. 587        50  LOAD_GLOBAL              type
               52  LOAD_FAST                'backend'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_ATTR                __typecache
               58  POP_BLOCK        
               60  ROT_TWO          
               62  LOAD_CONST               None
               64  DUP_TOP          
               66  DUP_TOP          
               68  CALL_FUNCTION_3       3  ''
               70  POP_TOP          
               72  RETURN_VALUE     
             74_0  COME_FROM_WITH       18  '18'
               74  <49>             
               76  POP_JUMP_IF_TRUE     80  'to 80'
               78  <48>             
             80_0  COME_FROM            76  '76'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          
               86  POP_EXCEPT       
               88  POP_TOP          

Parse error at or near `ROT_TWO' instruction at offset 60


def global_cache--- This code section failed: ---

 L. 590         0  LOAD_FAST                'kwds'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'key'
                6  LOAD_FAST                'funcname'
                8  LOAD_FAST                'args'
               10  BUILD_TUPLE_2         2 
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'key'

 L. 591        16  LOAD_FAST                'kwds'
               18  POP_JUMP_IF_FALSE    24  'to 24'
               20  <74>             
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'

 L. 592        24  SETUP_FINALLY        38  'to 38'

 L. 593        26  LOAD_FAST                'ffi'
               28  LOAD_ATTR                _typecache
               30  LOAD_FAST                'key'
               32  BINARY_SUBSCR    
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    24  '24'

 L. 594        38  DUP_TOP          
               40  LOAD_GLOBAL              KeyError
               42  <121>                54  ''
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 595        50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
               54  <48>             
             56_0  COME_FROM            52  '52'

 L. 596        56  SETUP_FINALLY        78  'to 78'

 L. 597        58  LOAD_GLOBAL              getattr
               60  LOAD_FAST                'ffi'
               62  LOAD_ATTR                _backend
               64  LOAD_FAST                'funcname'
               66  CALL_FUNCTION_2       2  ''
               68  LOAD_FAST                'args'
               70  CALL_FUNCTION_EX      0  'positional arguments only'
               72  STORE_FAST               'res'
               74  POP_BLOCK        
               76  JUMP_FORWARD        132  'to 132'
             78_0  COME_FROM_FINALLY    56  '56'

 L. 598        78  DUP_TOP          
               80  LOAD_GLOBAL              NotImplementedError
               82  <121>               130  ''
               84  POP_TOP          
               86  STORE_FAST               'e'
               88  POP_TOP          
               90  SETUP_FINALLY       122  'to 122'

 L. 599        92  LOAD_GLOBAL              NotImplementedError
               94  LOAD_STR                 '%s: %r: %s'
               96  LOAD_FAST                'funcname'
               98  LOAD_FAST                'srctype'
              100  LOAD_FAST                'e'
              102  BUILD_TUPLE_3         3 
              104  BINARY_MODULO    
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
              110  POP_BLOCK        
              112  POP_EXCEPT       
              114  LOAD_CONST               None
              116  STORE_FAST               'e'
              118  DELETE_FAST              'e'
              120  JUMP_FORWARD        132  'to 132'
            122_0  COME_FROM_FINALLY    90  '90'
              122  LOAD_CONST               None
              124  STORE_FAST               'e'
              126  DELETE_FAST              'e'
              128  <48>             
              130  <48>             
            132_0  COME_FROM           120  '120'
            132_1  COME_FROM            76  '76'

 L. 603       132  LOAD_FAST                'ffi'
              134  LOAD_ATTR                _typecache
              136  STORE_FAST               'cache'

 L. 604       138  LOAD_GLOBAL              global_lock
              140  SETUP_WITH          220  'to 220'
              142  POP_TOP          

 L. 605       144  LOAD_FAST                'cache'
              146  LOAD_METHOD              get
              148  LOAD_FAST                'key'
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'res1'

 L. 606       154  LOAD_FAST                'res1'
              156  LOAD_CONST               None
              158  <117>                 0  ''
              160  POP_JUMP_IF_FALSE   188  'to 188'

 L. 607       162  LOAD_FAST                'res'
              164  LOAD_FAST                'cache'
              166  LOAD_FAST                'key'
              168  STORE_SUBSCR     

 L. 608       170  LOAD_FAST                'res'
              172  POP_BLOCK        
              174  ROT_TWO          
              176  LOAD_CONST               None
              178  DUP_TOP          
              180  DUP_TOP          
              182  CALL_FUNCTION_3       3  ''
              184  POP_TOP          
              186  RETURN_VALUE     
            188_0  COME_FROM           160  '160'

 L. 610       188  LOAD_FAST                'res1'
              190  POP_BLOCK        
              192  ROT_TWO          
              194  LOAD_CONST               None
              196  DUP_TOP          
              198  DUP_TOP          
              200  CALL_FUNCTION_3       3  ''
              202  POP_TOP          
              204  RETURN_VALUE     
              206  POP_BLOCK        
              208  LOAD_CONST               None
              210  DUP_TOP          
              212  DUP_TOP          
              214  CALL_FUNCTION_3       3  ''
              216  POP_TOP          
              218  JUMP_FORWARD        236  'to 236'
            220_0  COME_FROM_WITH      140  '140'
              220  <49>             
              222  POP_JUMP_IF_TRUE    226  'to 226'
              224  <48>             
            226_0  COME_FROM           222  '222'
              226  POP_TOP          
              228  POP_TOP          
              230  POP_TOP          
              232  POP_EXCEPT       
              234  POP_TOP          
            236_0  COME_FROM           218  '218'

Parse error at or near `<74>' instruction at offset 20


def pointer_cache(ffi, BType):
    return global_cache('?', ffi, 'new_pointer_type', BType)


def attach_exception_info--- This code section failed: ---

 L. 616         0  LOAD_FAST                'e'
                2  LOAD_ATTR                args
                4  POP_JUMP_IF_FALSE    60  'to 60'
                6  LOAD_GLOBAL              type
                8  LOAD_FAST                'e'
               10  LOAD_ATTR                args
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_GLOBAL              str
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    60  'to 60'

 L. 617        24  LOAD_STR                 '%s: %s'
               26  LOAD_FAST                'name'
               28  LOAD_FAST                'e'
               30  LOAD_ATTR                args
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  BUILD_TUPLE_2         2 
               38  BINARY_MODULO    
               40  BUILD_TUPLE_1         1 
               42  LOAD_FAST                'e'
               44  LOAD_ATTR                args
               46  LOAD_CONST               1
               48  LOAD_CONST               None
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    
               54  BINARY_ADD       
               56  LOAD_FAST                'e'
               58  STORE_ATTR               args
             60_0  COME_FROM            22  '22'
             60_1  COME_FROM             4  '4'

Parse error at or near `None' instruction at offset -1