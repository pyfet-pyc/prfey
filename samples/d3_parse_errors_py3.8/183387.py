# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cffi\model.py
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

    def get_c_name(self, replace_with='', context='a C file', quals=0):
        result = self.c_name_with_marker
        assert result.count('&') == 1
        replace_with = replace_with.strip()
        if replace_with:
            if replace_with.startswith('*') and '&[' in result:
                replace_with = '(%s)' % replace_with
            elif replace_with[0] not in '[(':
                replace_with = ' ' + replace_with
        replace_with = qualify(quals, replace_with)
        result = result.replace('&', replace_with)
        if '$' in result:
            raise VerificationError("cannot generate '%s' in %s: unknown type name" % (
             self._get_c_name(), context))
        return result

    def _get_c_name(self):
        return self.c_name_with_marker.replace('&', '')

    def has_c_name(self):
        return '$' not in self._get_c_name()

    def is_integer_type(self):
        return False

    def get_cached_btype(self, ffi, finishlist, can_delay=False):
        try:
            BType = ffi._cached_btypes[self]
        except KeyError:
            BType = self.build_backend_type(ffi, finishlist)
            BType2 = ffi._cached_btypes.setdefault(self, BType)
            assert BType2 is BType
        else:
            return BType

    def __repr__(self):
        return '<%s>' % (self._get_c_name(),)

    def _get_items(self):
        return [(
         name, getattr(self, name)) for name in self._attrs_]


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

    def __init__(self, name):
        assert name in self.ALL_PRIMITIVE_TYPES
        self.name = name
        self.c_name_with_marker = name + '&'

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

    def __init__(self, args, result, ellipsis, abi=None):
        self.args = args
        self.result = result
        self.ellipsis = ellipsis
        self.abi = abi
        reprargs = [arg._get_c_name() for arg in self.args]
        if self.ellipsis:
            reprargs.append('...')
        reprargs = reprargs or ['void']
        replace_with = self._base_pattern % (', '.join(reprargs),)
        if abi is not None:
            replace_with = replace_with[:1] + abi + ' ' + replace_with[1:]
        self.c_name_with_marker = self.result.c_name_with_marker.replace('&', replace_with)


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

    def build_backend_type(self, ffi, finishlist):
        result = self.result.get_cached_btype(ffi, finishlist)
        args = []
        for tp in self.args:
            args.append(tp.get_cached_btype(ffi, finishlist))
        else:
            abi_args = ()
            if self.abi == '__stdcall' and not self.ellipsis:
                try:
                    abi_args = (
                     ffi._backend.FFI_STDCALL,)
                except AttributeError:
                    pass

                return global_cache(self, ffi, 'new_function_type', tuple(args), result, self.ellipsis, *abi_args)

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
        self.c_name_with_marker = totype.c_name_with_marker.replace('&', extra)

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

    def __init__(self, item, length):
        self.item = item
        self.length = length
        if length is None:
            brackets = '&[]'
        elif length == '...':
            brackets = '&[/*...*/]'
        else:
            brackets = '&[%s]' % length
        self.c_name_with_marker = self.item.c_name_with_marker.replace('&', brackets)

    def resolve_length(self, newlength):
        return ArrayType(self.item, newlength)

    def build_backend_type(self, ffi, finishlist):
        if self.length == '...':
            raise CDefError('cannot render the type %r: unknown length' % (
             self,))
        self.item.get_cached_btype(ffi, finishlist)
        BPtrItem = PointerType(self.item).get_cached_btype(ffi, finishlist)
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

    def get_official_name(self):
        assert self.c_name_with_marker.endswith('&')
        return self.c_name_with_marker[:-1]


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

    def anonymous_struct_fields(self):
        if self.fldtypes is not None:
            for name, type in zip(self.fldnames, self.fldtypes):
                if name == '':
                    if isinstance(type, StructOrUnion):
                        yield type

    def enumfields(self, expand_anonymous_struct_union=True):
        fldquals = self.fldquals
        if fldquals is None:
            fldquals = (0, ) * len(self.fldnames)
        for name, type, bitsize, quals in zip(self.fldnames, self.fldtypes, self.fldbitsize, fldquals):
            if name == '':
                if isinstance(type, StructOrUnion) and expand_anonymous_struct_union:
                    for result in type.enumfields():
                        yield result

                else:
                    yield (
                     name, type, bitsize, quals)

    def force_flatten(self):
        names = []
        types = []
        bitsizes = []
        fldquals = []
        for name, type, bitsize, quals in self.enumfields():
            names.append(name)
            types.append(type)
            bitsizes.append(bitsize)
            fldquals.append(quals)
        else:
            self.fldnames = tuple(names)
            self.fldtypes = tuple(types)
            self.fldbitsize = tuple(bitsizes)
            self.fldquals = tuple(fldquals)

    def get_cached_btype(self, ffi, finishlist, can_delay=False):
        BType = StructOrUnionOrEnum.get_cached_btype(self, ffi, finishlist, can_delay)
        if not can_delay:
            self.finish_backend_type(ffi, finishlist)
        return BType

    def finish_backend_type(self, ffi, finishlist):
        if self.completed:
            if self.completed != 2:
                raise NotImplementedError("recursive structure declaration for '%s'" % (
                 self.name,))
            return
        BType = ffi._cached_btypes[self]
        self.completed = 1
        if self.fldtypes is None:
            pass
        elif self.fixedlayout is None:
            fldtypes = [tp.get_cached_btype(ffi, finishlist) for tp in self.fldtypes]
            lst = list(zip(self.fldnames, fldtypes, self.fldbitsize))
            extra_flags = ()
            if self.packed:
                if self.packed == 1:
                    extra_flags = (8, )
                else:
                    extra_flags = (
                     0, self.packed)
            (ffi._backend.complete_struct_or_union)(BType, lst, self, -1, -1, *extra_flags)
        else:
            fldtypes = []
            fieldofs, fieldsize, totalsize, totalalignment = self.fixedlayout
            for i in range(len(self.fldnames)):
                fsize = fieldsize[i]
                ftype = self.fldtypes[i]
                if isinstance(ftype, ArrayType):
                    if ftype.length == '...':
                        BItemType = ftype.item.get_cached_btype(ffi, finishlist)
                        nlen, nrest = divmod(fsize, ffi.sizeof(BItemType))
                        if nrest != 0:
                            self._verification_error("field '%s.%s' has a bogus size?" % (
                             self.name, self.fldnames[i] or '{}'))
                        ftype = ftype.resolve_length(nlen)
                        self.fldtypes = self.fldtypes[:i] + (ftype,) + self.fldtypes[i + 1:]
                BFieldType = ftype.get_cached_btype(ffi, finishlist)
                if isinstance(ftype, ArrayType) and ftype.length is None:
                    assert fsize == 0
                else:
                    bitemsize = ffi.sizeof(BFieldType)
                    if bitemsize != fsize:
                        self._verification_error("field '%s.%s' is declared as %d bytes, but is really %d bytes" % (
                         self.name,
                         self.fldnames[i] or '{}',
                         bitemsize, fsize))
                fldtypes.append(BFieldType)
            else:
                lst = list(zip(self.fldnames, fldtypes, self.fldbitsize, fieldofs))
                ffi._backend.complete_struct_or_union(BType, lst, self, totalsize, totalalignment)

        self.completed = 2

    def _verification_error(self, msg):
        raise VerificationError(msg)

    def check_not_partial(self):
        if self.partial:
            if self.fixedlayout is None:
                raise VerificationMissing(self._get_c_name())

    def build_backend_type(self, ffi, finishlist):
        self.check_not_partial()
        finishlist.append(self)
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

    def force_the_name(self, forcename):
        StructOrUnionOrEnum.force_the_name(self, forcename)
        if self.forcename is None:
            name = self.get_official_name()
            self.forcename = '$' + name.replace(' ', '_')

    def check_not_partial(self):
        if self.partial:
            if not self.partial_resolved:
                raise VerificationMissing(self._get_c_name())

    def build_backend_type(self, ffi, finishlist):
        self.check_not_partial()
        base_btype = self.build_baseinttype(ffi, finishlist)
        return global_cache(self, ffi, 'new_enum_type', (self.get_official_name()),
          (self.enumerators),
          (self.enumvalues), base_btype,
          key=self)

    def build_baseinttype(self, ffi, finishlist):
        if self.baseinttype is not None:
            return self.baseinttype.get_cached_btype(ffi, finishlist)
        if self.enumvalues:
            smallest_value = min(self.enumvalues)
            largest_value = max(self.enumvalues)
        else:
            import warnings
            try:
                __warningregistry__.clear()
            except NameError:
                pass
            else:
                warnings.warn("%r has no values explicitly defined; guessing that it is equivalent to 'unsigned int'" % self._get_c_name())
                smallest_value = largest_value = 0
        if smallest_value < 0:
            sign = 1
            candidate1 = PrimitiveType('int')
            candidate2 = PrimitiveType('long')
        else:
            sign = 0
            candidate1 = PrimitiveType('unsigned int')
            candidate2 = PrimitiveType('unsigned long')
        btype1 = candidate1.get_cached_btype(ffi, finishlist)
        btype2 = candidate2.get_cached_btype(ffi, finishlist)
        size1 = ffi.sizeof(btype1)
        size2 = ffi.sizeof(btype2)
        if smallest_value >= -1 << 8 * size1 - 1:
            if largest_value < 1 << 8 * size1 - sign:
                return btype1
        if smallest_value >= -1 << 8 * size2 - 1:
            if largest_value < 1 << 8 * size2 - sign:
                return btype2
        raise CDefError("%s values don't all fit into either 'long' or 'unsigned long'" % self._get_c_name())


def unknown_type(name, structname=None):
    if structname is None:
        structname = '$%s' % name
    tp = StructType(structname, None, None, None)
    tp.force_the_name(name)
    tp.origin = 'unknown_type'
    return tp


def unknown_ptr_type(name, structname=None):
    if structname is None:
        structname = '$$%s' % name
    tp = StructType(structname, None, None, None)
    return NamedPointerType(tp, name)


global_lock = allocate_lock()
_typecache_cffi_backend = weakref.WeakValueDictionary()

def get_typecache(backend):
    if isinstance(backend, types.ModuleType):
        return _typecache_cffi_backend
    with global_lock:
        if not hasattr(type(backend), '__typecache'):
            type(backend).__typecache = weakref.WeakValueDictionary()
        return type(backend).__typecache


def global_cache--- This code section failed: ---

 L. 587         0  LOAD_FAST                'kwds'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'key'
                6  LOAD_FAST                'funcname'
                8  LOAD_FAST                'args'
               10  BUILD_TUPLE_2         2 
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'key'

 L. 588        16  LOAD_FAST                'kwds'
               18  POP_JUMP_IF_FALSE    24  'to 24'
               20  LOAD_GLOBAL              AssertionError
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'

 L. 589        24  SETUP_FINALLY        38  'to 38'

 L. 590        26  LOAD_FAST                'ffi'
               28  LOAD_ATTR                _typecache
               30  LOAD_FAST                'key'
               32  BINARY_SUBSCR    
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    24  '24'

 L. 591        38  DUP_TOP          
               40  LOAD_GLOBAL              KeyError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    56  'to 56'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 592        52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            44  '44'
               56  END_FINALLY      
             58_0  COME_FROM            54  '54'

 L. 593        58  SETUP_FINALLY        80  'to 80'

 L. 594        60  LOAD_GLOBAL              getattr
               62  LOAD_FAST                'ffi'
               64  LOAD_ATTR                _backend
               66  LOAD_FAST                'funcname'
               68  CALL_FUNCTION_2       2  ''
               70  LOAD_FAST                'args'
               72  CALL_FUNCTION_EX      0  'positional arguments only'
               74  STORE_FAST               'res'
               76  POP_BLOCK        
               78  JUMP_FORWARD        132  'to 132'
             80_0  COME_FROM_FINALLY    58  '58'

 L. 595        80  DUP_TOP          
               82  LOAD_GLOBAL              NotImplementedError
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   130  'to 130'
               88  POP_TOP          
               90  STORE_FAST               'e'
               92  POP_TOP          
               94  SETUP_FINALLY       118  'to 118'

 L. 596        96  LOAD_GLOBAL              NotImplementedError
               98  LOAD_STR                 '%s: %r: %s'
              100  LOAD_FAST                'funcname'
              102  LOAD_FAST                'srctype'
              104  LOAD_FAST                'e'
              106  BUILD_TUPLE_3         3 
              108  BINARY_MODULO    
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM_FINALLY    94  '94'
              118  LOAD_CONST               None
              120  STORE_FAST               'e'
              122  DELETE_FAST              'e'
              124  END_FINALLY      
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM            86  '86'
              130  END_FINALLY      
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM            78  '78'

 L. 600       132  LOAD_FAST                'ffi'
              134  LOAD_ATTR                _typecache
              136  STORE_FAST               'cache'

 L. 601       138  LOAD_GLOBAL              global_lock
              140  SETUP_WITH          206  'to 206'
              142  POP_TOP          

 L. 602       144  LOAD_FAST                'cache'
              146  LOAD_METHOD              get
              148  LOAD_FAST                'key'
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'res1'

 L. 603       154  LOAD_FAST                'res1'
              156  LOAD_CONST               None
              158  COMPARE_OP               is
              160  POP_JUMP_IF_FALSE   186  'to 186'

 L. 604       162  LOAD_FAST                'res'
              164  LOAD_FAST                'cache'
              166  LOAD_FAST                'key'
              168  STORE_SUBSCR     

 L. 605       170  LOAD_FAST                'res'
              172  POP_BLOCK        
              174  ROT_TWO          
              176  BEGIN_FINALLY    
              178  WITH_CLEANUP_START
              180  WITH_CLEANUP_FINISH
              182  POP_FINALLY           0  ''
              184  RETURN_VALUE     
            186_0  COME_FROM           160  '160'

 L. 607       186  LOAD_FAST                'res1'
              188  POP_BLOCK        
              190  ROT_TWO          
              192  BEGIN_FINALLY    
              194  WITH_CLEANUP_START
              196  WITH_CLEANUP_FINISH
              198  POP_FINALLY           0  ''
              200  RETURN_VALUE     
              202  POP_BLOCK        
              204  BEGIN_FINALLY    
            206_0  COME_FROM_WITH      140  '140'
              206  WITH_CLEANUP_START
              208  WITH_CLEANUP_FINISH
              210  END_FINALLY      

Parse error at or near `COME_FROM' instruction at offset 56_0


def pointer_cache(ffi, BType):
    return global_cache('?', ffi, 'new_pointer_type', BType)


def attach_exception_info(e, name):
    if e.args:
        if type(e.args[0]) is str:
            e.args = (
             '%s: %s' % (name, e.args[0]),) + e.args[1:]