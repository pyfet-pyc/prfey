# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cffi\commontypes.py
import sys
from . import model
from .error import FFIError
COMMON_TYPES = {}
try:
    from _cffi_backend import _get_common_types
    _get_common_types(COMMON_TYPES)
except ImportError:
    pass
else:
    COMMON_TYPES['FILE'] = model.unknown_type('FILE', '_IO_FILE')
    COMMON_TYPES['bool'] = '_Bool'
for _type in model.PrimitiveType.ALL_PRIMITIVE_TYPES:
    if _type.endswith('_t'):
        COMMON_TYPES[_type] = _type
    del _type
    _CACHE = {}

    def resolve_common_type--- This code section failed: ---

 L.  26         0  SETUP_FINALLY        12  'to 12'

 L.  27         2  LOAD_GLOBAL              _CACHE
                4  LOAD_FAST                'commontype'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  28        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE   190  'to 190'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  29        26  LOAD_GLOBAL              COMMON_TYPES
               28  LOAD_METHOD              get
               30  LOAD_FAST                'commontype'
               32  LOAD_FAST                'commontype'
               34  CALL_METHOD_2         2  ''
               36  STORE_FAST               'cdecl'

 L.  30        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'cdecl'
               42  LOAD_GLOBAL              str
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_TRUE     60  'to 60'

 L.  31        48  LOAD_FAST                'cdecl'
               50  LOAD_CONST               0
               52  ROT_TWO          
               54  STORE_FAST               'result'
               56  STORE_FAST               'quals'
               58  JUMP_FORWARD        150  'to 150'
             60_0  COME_FROM            46  '46'

 L.  32        60  LOAD_FAST                'cdecl'
               62  LOAD_GLOBAL              model
               64  LOAD_ATTR                PrimitiveType
               66  LOAD_ATTR                ALL_PRIMITIVE_TYPES
               68  COMPARE_OP               in
               70  POP_JUMP_IF_FALSE    90  'to 90'

 L.  33        72  LOAD_GLOBAL              model
               74  LOAD_METHOD              PrimitiveType
               76  LOAD_FAST                'cdecl'
               78  CALL_METHOD_1         1  ''
               80  LOAD_CONST               0
               82  ROT_TWO          
               84  STORE_FAST               'result'
               86  STORE_FAST               'quals'
               88  JUMP_FORWARD        150  'to 150'
             90_0  COME_FROM            70  '70'

 L.  34        90  LOAD_FAST                'cdecl'
               92  LOAD_STR                 'set-unicode-needed'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   114  'to 114'

 L.  35        98  LOAD_GLOBAL              FFIError
              100  LOAD_STR                 'The Windows type %r is only available after you call ffi.set_unicode()'

 L.  36       102  LOAD_FAST                'commontype'
              104  BUILD_TUPLE_1         1 

 L.  35       106  BINARY_MODULO    
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
              112  JUMP_FORWARD        150  'to 150'
            114_0  COME_FROM            96  '96'

 L.  38       114  LOAD_FAST                'commontype'
              116  LOAD_FAST                'cdecl'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   136  'to 136'

 L.  39       122  LOAD_GLOBAL              FFIError

 L.  40       124  LOAD_STR                 'Unsupported type: %r.  Please look at http://cffi.readthedocs.io/en/latest/cdef.html#ffi-cdef-limitations and file an issue if you think this type should really be supported.'

 L.  43       126  LOAD_FAST                'commontype'
              128  BUILD_TUPLE_1         1 

 L.  40       130  BINARY_MODULO    

 L.  39       132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           120  '120'

 L.  44       136  LOAD_FAST                'parser'
              138  LOAD_METHOD              parse_type_and_quals
              140  LOAD_FAST                'cdecl'
              142  CALL_METHOD_1         1  ''
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_FAST               'result'
              148  STORE_FAST               'quals'
            150_0  COME_FROM           112  '112'
            150_1  COME_FROM            88  '88'
            150_2  COME_FROM            58  '58'

 L.  46       150  LOAD_GLOBAL              isinstance
              152  LOAD_FAST                'result'
              154  LOAD_GLOBAL              model
              156  LOAD_ATTR                BaseTypeByIdentity
              158  CALL_FUNCTION_2       2  ''
              160  POP_JUMP_IF_TRUE    166  'to 166'
              162  LOAD_ASSERT              AssertionError
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           160  '160'

 L.  47       166  LOAD_FAST                'result'
              168  LOAD_FAST                'quals'
              170  BUILD_TUPLE_2         2 
              172  LOAD_GLOBAL              _CACHE
              174  LOAD_FAST                'commontype'
              176  STORE_SUBSCR     

 L.  48       178  LOAD_FAST                'result'
              180  LOAD_FAST                'quals'
              182  BUILD_TUPLE_2         2 
              184  ROT_FOUR         
              186  POP_EXCEPT       
              188  RETURN_VALUE     
            190_0  COME_FROM            18  '18'
              190  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22


    def win_common_types():
        return {'UNICODE_STRING':model.StructType('_UNICODE_STRING', [
          'Length',
          'MaximumLength',
          'Buffer'], [
          model.PrimitiveType('unsigned short'),
          model.PrimitiveType('unsigned short'),
          model.PointerType(model.PrimitiveType('wchar_t'))], [
          -1, -1, -1]), 
         'PUNICODE_STRING':'UNICODE_STRING *', 
         'PCUNICODE_STRING':'const UNICODE_STRING *', 
         'TBYTE':'set-unicode-needed', 
         'TCHAR':'set-unicode-needed', 
         'LPCTSTR':'set-unicode-needed', 
         'PCTSTR':'set-unicode-needed', 
         'LPTSTR':'set-unicode-needed', 
         'PTSTR':'set-unicode-needed', 
         'PTBYTE':'set-unicode-needed', 
         'PTCHAR':'set-unicode-needed'}


    if sys.platform == 'win32':
        COMMON_TYPES.update(win_common_types())