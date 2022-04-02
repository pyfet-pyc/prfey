# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: importlib\util.py
"""Utility code for constructing importers, etc."""
from . import abc
from ._bootstrap import module_from_spec
from ._bootstrap import _resolve_name
from ._bootstrap import spec_from_loader
from ._bootstrap import _find_spec
from ._bootstrap_external import MAGIC_NUMBER
from ._bootstrap_external import _RAW_MAGIC_NUMBER
from ._bootstrap_external import cache_from_source
from ._bootstrap_external import decode_source
from ._bootstrap_external import source_from_cache
from ._bootstrap_external import spec_from_file_location
from contextlib import contextmanager
import _imp, functools, sys, types, warnings

def source_hash(source_bytes):
    """Return the hash of *source_bytes* as used in hash-based pyc files."""
    return _imp.source_hash(_RAW_MAGIC_NUMBER, source_bytes)


def resolve_name(name, package):
    """Resolve a relative module name to an absolute one."""
    if not name.startswith('.'):
        return name
    if not package:
        raise ImportError(f"no package specified for {repr(name)} (required for relative module names)")
    level = 0
    for character in name:
        if character != '.':
            break
        level += 1
    else:
        return _resolve_name(name[level:], package, level)


def _find_spec_from_path--- This code section failed: ---

 L.  57         0  LOAD_FAST                'name'
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                modules
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L.  58        10  LOAD_GLOBAL              _find_spec
               12  LOAD_FAST                'name'
               14  LOAD_FAST                'path'
               16  CALL_FUNCTION_2       2  ''
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L.  60        20  LOAD_GLOBAL              sys
               22  LOAD_ATTR                modules
               24  LOAD_FAST                'name'
               26  BINARY_SUBSCR    
               28  STORE_FAST               'module'

 L.  61        30  LOAD_FAST                'module'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L.  62        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'

 L.  63        42  SETUP_FINALLY        54  'to 54'

 L.  64        44  LOAD_FAST                'module'
               46  LOAD_ATTR                __spec__
               48  STORE_FAST               'spec'
               50  POP_BLOCK        
               52  JUMP_FORWARD         88  'to 88'
             54_0  COME_FROM_FINALLY    42  '42'

 L.  65        54  DUP_TOP          
               56  LOAD_GLOBAL              AttributeError
               58  <121>                86  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  66        66  LOAD_GLOBAL              ValueError
               68  LOAD_STR                 '{}.__spec__ is not set'
               70  LOAD_METHOD              format
               72  LOAD_FAST                'name'
               74  CALL_METHOD_1         1  ''
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_CONST               None
               80  RAISE_VARARGS_2       2  'exception instance with __cause__'
               82  POP_EXCEPT       
               84  JUMP_FORWARD        114  'to 114'
               86  <48>             
             88_0  COME_FROM            52  '52'

 L.  68        88  LOAD_FAST                'spec'
               90  LOAD_CONST               None
               92  <117>                 0  ''
               94  POP_JUMP_IF_FALSE   110  'to 110'

 L.  69        96  LOAD_GLOBAL              ValueError
               98  LOAD_STR                 '{}.__spec__ is None'
              100  LOAD_METHOD              format
              102  LOAD_FAST                'name'
              104  CALL_METHOD_1         1  ''
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM            94  '94'

 L.  70       110  LOAD_FAST                'spec'
              112  RETURN_VALUE     
            114_0  COME_FROM            84  '84'

Parse error at or near `None' instruction at offset -1


def find_spec--- This code section failed: ---

 L.  90         0  LOAD_FAST                'name'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '.'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'
               10  LOAD_GLOBAL              resolve_name
               12  LOAD_FAST                'name'
               14  LOAD_FAST                'package'
               16  CALL_FUNCTION_2       2  ''
               18  JUMP_FORWARD         22  'to 22'
             20_0  COME_FROM             8  '8'
               20  LOAD_FAST                'name'
             22_0  COME_FROM            18  '18'
               22  STORE_FAST               'fullname'

 L.  91        24  LOAD_FAST                'fullname'
               26  LOAD_GLOBAL              sys
               28  LOAD_ATTR                modules
               30  <118>                 1  ''
               32  POP_JUMP_IF_FALSE   156  'to 156'

 L.  92        34  LOAD_FAST                'fullname'
               36  LOAD_METHOD              rpartition
               38  LOAD_STR                 '.'
               40  CALL_METHOD_1         1  ''
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  STORE_FAST               'parent_name'

 L.  93        48  LOAD_FAST                'parent_name'
               50  POP_JUMP_IF_FALSE   142  'to 142'

 L.  94        52  LOAD_GLOBAL              __import__
               54  LOAD_FAST                'parent_name'
               56  LOAD_STR                 '__path__'
               58  BUILD_LIST_1          1 
               60  LOAD_CONST               ('fromlist',)
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  STORE_FAST               'parent'

 L.  95        66  SETUP_FINALLY        78  'to 78'

 L.  96        68  LOAD_FAST                'parent'
               70  LOAD_ATTR                __path__
               72  STORE_FAST               'parent_path'
               74  POP_BLOCK        
               76  JUMP_ABSOLUTE       146  'to 146'
             78_0  COME_FROM_FINALLY    66  '66'

 L.  97        78  DUP_TOP          
               80  LOAD_GLOBAL              AttributeError
               82  <121>               138  ''
               84  POP_TOP          
               86  STORE_FAST               'e'
               88  POP_TOP          
               90  SETUP_FINALLY       130  'to 130'

 L.  98        92  LOAD_GLOBAL              ModuleNotFoundError

 L.  99        94  LOAD_STR                 '__path__ attribute not found on '
               96  LOAD_FAST                'parent_name'
               98  FORMAT_VALUE          2  '!r'
              100  LOAD_STR                 ' while trying to find '

 L. 100       102  LOAD_FAST                'fullname'

 L.  99       104  FORMAT_VALUE          2  '!r'
              106  BUILD_STRING_4        4 

 L. 100       108  LOAD_FAST                'fullname'

 L.  98       110  LOAD_CONST               ('name',)
              112  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 100       114  LOAD_FAST                'e'

 L.  98       116  RAISE_VARARGS_2       2  'exception instance with __cause__'
              118  POP_BLOCK        
              120  POP_EXCEPT       
              122  LOAD_CONST               None
              124  STORE_FAST               'e'
              126  DELETE_FAST              'e'
              128  JUMP_ABSOLUTE       146  'to 146'
            130_0  COME_FROM_FINALLY    90  '90'
              130  LOAD_CONST               None
              132  STORE_FAST               'e'
              134  DELETE_FAST              'e'
              136  <48>             
              138  <48>             
              140  JUMP_FORWARD        146  'to 146'
            142_0  COME_FROM            50  '50'

 L. 102       142  LOAD_CONST               None
              144  STORE_FAST               'parent_path'
            146_0  COME_FROM           140  '140'

 L. 103       146  LOAD_GLOBAL              _find_spec
              148  LOAD_FAST                'fullname'
              150  LOAD_FAST                'parent_path'
              152  CALL_FUNCTION_2       2  ''
              154  RETURN_VALUE     
            156_0  COME_FROM            32  '32'

 L. 105       156  LOAD_GLOBAL              sys
              158  LOAD_ATTR                modules
              160  LOAD_FAST                'fullname'
              162  BINARY_SUBSCR    
              164  STORE_FAST               'module'

 L. 106       166  LOAD_FAST                'module'
              168  LOAD_CONST               None
              170  <117>                 0  ''
              172  POP_JUMP_IF_FALSE   178  'to 178'

 L. 107       174  LOAD_CONST               None
              176  RETURN_VALUE     
            178_0  COME_FROM           172  '172'

 L. 108       178  SETUP_FINALLY       190  'to 190'

 L. 109       180  LOAD_FAST                'module'
              182  LOAD_ATTR                __spec__
              184  STORE_FAST               'spec'
              186  POP_BLOCK        
              188  JUMP_FORWARD        224  'to 224'
            190_0  COME_FROM_FINALLY   178  '178'

 L. 110       190  DUP_TOP          
              192  LOAD_GLOBAL              AttributeError
              194  <121>               222  ''
              196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L. 111       202  LOAD_GLOBAL              ValueError
              204  LOAD_STR                 '{}.__spec__ is not set'
              206  LOAD_METHOD              format
              208  LOAD_FAST                'name'
              210  CALL_METHOD_1         1  ''
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_CONST               None
              216  RAISE_VARARGS_2       2  'exception instance with __cause__'
              218  POP_EXCEPT       
              220  JUMP_FORWARD        250  'to 250'
              222  <48>             
            224_0  COME_FROM           188  '188'

 L. 113       224  LOAD_FAST                'spec'
              226  LOAD_CONST               None
              228  <117>                 0  ''
              230  POP_JUMP_IF_FALSE   246  'to 246'

 L. 114       232  LOAD_GLOBAL              ValueError
              234  LOAD_STR                 '{}.__spec__ is None'
              236  LOAD_METHOD              format
              238  LOAD_FAST                'name'
              240  CALL_METHOD_1         1  ''
              242  CALL_FUNCTION_1       1  ''
              244  RAISE_VARARGS_1       1  'exception instance'
            246_0  COME_FROM           230  '230'

 L. 115       246  LOAD_FAST                'spec'
              248  RETURN_VALUE     
            250_0  COME_FROM           220  '220'

Parse error at or near `<118>' instruction at offset 30


@contextmanager
def _module_to_load--- This code section failed: ---

 L. 120         0  LOAD_FAST                'name'
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                modules
                6  <118>                 0  ''
                8  STORE_FAST               'is_reload'

 L. 122        10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                modules
               14  LOAD_METHOD              get
               16  LOAD_FAST                'name'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'module'

 L. 123        22  LOAD_FAST                'is_reload'
               24  POP_JUMP_IF_TRUE     54  'to 54'

 L. 127        26  LOAD_GLOBAL              type
               28  LOAD_GLOBAL              sys
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_FAST                'name'
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'module'

 L. 130        38  LOAD_CONST               True
               40  LOAD_FAST                'module'
               42  STORE_ATTR               __initializing__

 L. 131        44  LOAD_FAST                'module'
               46  LOAD_GLOBAL              sys
               48  LOAD_ATTR                modules
               50  LOAD_FAST                'name'
               52  STORE_SUBSCR     
             54_0  COME_FROM            24  '24'

 L. 132        54  SETUP_FINALLY       132  'to 132'
               56  SETUP_FINALLY        68  'to 68'

 L. 133        58  LOAD_FAST                'module'
               60  YIELD_VALUE      
               62  POP_TOP          
               64  POP_BLOCK        
               66  JUMP_FORWARD        122  'to 122'
             68_0  COME_FROM_FINALLY    56  '56'

 L. 134        68  DUP_TOP          
               70  LOAD_GLOBAL              Exception
               72  <121>               120  ''
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 135        80  LOAD_FAST                'is_reload'
               82  POP_JUMP_IF_TRUE    116  'to 116'

 L. 136        84  SETUP_FINALLY        98  'to 98'

 L. 137        86  LOAD_GLOBAL              sys
               88  LOAD_ATTR                modules
               90  LOAD_FAST                'name'
               92  DELETE_SUBSCR    
               94  POP_BLOCK        
               96  JUMP_FORWARD        116  'to 116'
             98_0  COME_FROM_FINALLY    84  '84'

 L. 138        98  DUP_TOP          
              100  LOAD_GLOBAL              KeyError
              102  <121>               114  ''
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 139       110  POP_EXCEPT       
              112  JUMP_FORWARD        116  'to 116'
              114  <48>             
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM            96  '96'
            116_2  COME_FROM            82  '82'
              116  POP_EXCEPT       
              118  JUMP_FORWARD        122  'to 122'
              120  <48>             
            122_0  COME_FROM           118  '118'
            122_1  COME_FROM            66  '66'
              122  POP_BLOCK        

 L. 141       124  LOAD_CONST               False
              126  LOAD_FAST                'module'
              128  STORE_ATTR               __initializing__
              130  JUMP_FORWARD        140  'to 140'
            132_0  COME_FROM_FINALLY    54  '54'
              132  LOAD_CONST               False
              134  LOAD_FAST                'module'
              136  STORE_ATTR               __initializing__
              138  <48>             
            140_0  COME_FROM           130  '130'

Parse error at or near `None' instruction at offset -1


def set_package(fxn):
    """Set __package__ on the returned module.

    This function is deprecated.

    """

    @functools.wraps(fxn)
    def set_package_wrapper--- This code section failed: ---

 L. 152         0  LOAD_GLOBAL              warnings
                2  LOAD_ATTR                warn
                4  LOAD_STR                 'The import system now takes care of this automatically.'

 L. 153         6  LOAD_GLOBAL              DeprecationWarning
                8  LOAD_CONST               2

 L. 152        10  LOAD_CONST               ('stacklevel',)
               12  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               14  POP_TOP          

 L. 154        16  LOAD_DEREF               'fxn'
               18  LOAD_FAST                'args'
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kwargs'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  STORE_FAST               'module'

 L. 155        30  LOAD_GLOBAL              getattr
               32  LOAD_FAST                'module'
               34  LOAD_STR                 '__package__'
               36  LOAD_CONST               None
               38  CALL_FUNCTION_3       3  ''
               40  LOAD_CONST               None
               42  <117>                 0  ''
               44  POP_JUMP_IF_FALSE    82  'to 82'

 L. 156        46  LOAD_FAST                'module'
               48  LOAD_ATTR                __name__
               50  LOAD_FAST                'module'
               52  STORE_ATTR               __package__

 L. 157        54  LOAD_GLOBAL              hasattr
               56  LOAD_FAST                'module'
               58  LOAD_STR                 '__path__'
               60  CALL_FUNCTION_2       2  ''
               62  POP_JUMP_IF_TRUE     82  'to 82'

 L. 158        64  LOAD_FAST                'module'
               66  LOAD_ATTR                __package__
               68  LOAD_METHOD              rpartition
               70  LOAD_STR                 '.'
               72  CALL_METHOD_1         1  ''
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'module'
               80  STORE_ATTR               __package__
             82_0  COME_FROM            62  '62'
             82_1  COME_FROM            44  '44'

 L. 159        82  LOAD_FAST                'module'
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 24

    return set_package_wrapper


def set_loader(fxn):
    """Set __loader__ on the returned module.

    This function is deprecated.

    """

    @functools.wraps(fxn)
    def set_loader_wrapper--- This code section failed: ---

 L. 171         0  LOAD_GLOBAL              warnings
                2  LOAD_ATTR                warn
                4  LOAD_STR                 'The import system now takes care of this automatically.'

 L. 172         6  LOAD_GLOBAL              DeprecationWarning
                8  LOAD_CONST               2

 L. 171        10  LOAD_CONST               ('stacklevel',)
               12  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               14  POP_TOP          

 L. 173        16  LOAD_DEREF               'fxn'
               18  LOAD_FAST                'self'
               20  BUILD_LIST_1          1 
               22  LOAD_FAST                'args'
               24  CALL_FINALLY         27  'to 27'
               26  WITH_CLEANUP_FINISH
               28  BUILD_MAP_0           0 
               30  LOAD_FAST                'kwargs'
               32  <164>                 1  ''
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  STORE_FAST               'module'

 L. 174        38  LOAD_GLOBAL              getattr
               40  LOAD_FAST                'module'
               42  LOAD_STR                 '__loader__'
               44  LOAD_CONST               None
               46  CALL_FUNCTION_3       3  ''
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    60  'to 60'

 L. 175        54  LOAD_FAST                'self'
               56  LOAD_FAST                'module'
               58  STORE_ATTR               __loader__
             60_0  COME_FROM            52  '52'

 L. 176        60  LOAD_FAST                'module'
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 24

    return set_loader_wrapper


def module_for_loader(fxn):
    """Decorator to handle selecting the proper module for loaders.

    The decorated function is passed the module to use instead of the module
    name. The module passed in to the function is either from sys.modules if
    it already exists or is a new module. If the module is new, then __name__
    is set the first argument to the method, __loader__ is set to self, and
    __package__ is set accordingly (if self.is_package() is defined) will be set
    before it is passed to the decorated function (if self.is_package() does
    not work for the module it will be set post-load).

    If an exception is raised and the decorator created the module it is
    subsequently removed from sys.modules.

    The decorator assumes that the decorated function takes the module name as
    the second argument.

    """
    warnings.warn('The import system now takes care of this automatically.', DeprecationWarning,
      stacklevel=2)

    @functools.wraps(fxn)
    def module_for_loader_wrapper--- This code section failed: ---

 L. 202         0  LOAD_GLOBAL              _module_to_load
                2  LOAD_FAST                'fullname'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH          120  'to 120'
                8  STORE_FAST               'module'

 L. 203        10  LOAD_FAST                'self'
               12  LOAD_FAST                'module'
               14  STORE_ATTR               __loader__

 L. 204        16  SETUP_FINALLY        32  'to 32'

 L. 205        18  LOAD_FAST                'self'
               20  LOAD_METHOD              is_package
               22  LOAD_FAST                'fullname'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'is_package'
               28  POP_BLOCK        
               30  JUMP_FORWARD         54  'to 54'
             32_0  COME_FROM_FINALLY    16  '16'

 L. 206        32  DUP_TOP          
               34  LOAD_GLOBAL              ImportError
               36  LOAD_GLOBAL              AttributeError
               38  BUILD_TUPLE_2         2 
               40  <121>                52  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 207        48  POP_EXCEPT       
               50  JUMP_FORWARD         82  'to 82'
               52  <48>             
             54_0  COME_FROM            30  '30'

 L. 209        54  LOAD_FAST                'is_package'
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 210        58  LOAD_FAST                'fullname'
               60  LOAD_FAST                'module'
               62  STORE_ATTR               __package__
               64  JUMP_FORWARD         82  'to 82'
             66_0  COME_FROM            56  '56'

 L. 212        66  LOAD_FAST                'fullname'
               68  LOAD_METHOD              rpartition
               70  LOAD_STR                 '.'
               72  CALL_METHOD_1         1  ''
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'module'
               80  STORE_ATTR               __package__
             82_0  COME_FROM            64  '64'
             82_1  COME_FROM            50  '50'

 L. 214        82  LOAD_DEREF               'fxn'
               84  LOAD_FAST                'self'
               86  LOAD_FAST                'module'
               88  BUILD_LIST_2          2 
               90  LOAD_FAST                'args'
               92  CALL_FINALLY         95  'to 95'
               94  WITH_CLEANUP_FINISH
               96  BUILD_MAP_0           0 
               98  LOAD_FAST                'kwargs'
              100  <164>                 1  ''
              102  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              104  POP_BLOCK        
              106  ROT_TWO          
              108  LOAD_CONST               None
              110  DUP_TOP          
              112  DUP_TOP          
              114  CALL_FUNCTION_3       3  ''
              116  POP_TOP          
              118  RETURN_VALUE     
            120_0  COME_FROM_WITH        6  '6'
              120  <49>             
              122  POP_JUMP_IF_TRUE    126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          
              132  POP_EXCEPT       
              134  POP_TOP          

Parse error at or near `<121>' instruction at offset 40

    return module_for_loader_wrapper


class _LazyModule(types.ModuleType):
    __doc__ = 'A subclass of the module type which triggers loading upon attribute access.'

    def __getattribute__--- This code section failed: ---

 L. 228         0  LOAD_GLOBAL              types
                2  LOAD_ATTR                ModuleType
                4  LOAD_FAST                'self'
                6  STORE_ATTR               __class__

 L. 231         8  LOAD_FAST                'self'
               10  LOAD_ATTR                __spec__
               12  LOAD_ATTR                name
               14  STORE_FAST               'original_name'

 L. 234        16  LOAD_FAST                'self'
               18  LOAD_ATTR                __spec__
               20  LOAD_ATTR                loader_state
               22  LOAD_STR                 '__dict__'
               24  BINARY_SUBSCR    
               26  STORE_FAST               'attrs_then'

 L. 235        28  LOAD_FAST                'self'
               30  LOAD_ATTR                __spec__
               32  LOAD_ATTR                loader_state
               34  LOAD_STR                 '__class__'
               36  BINARY_SUBSCR    
               38  STORE_FAST               'original_type'

 L. 236        40  LOAD_FAST                'self'
               42  LOAD_ATTR                __dict__
               44  STORE_FAST               'attrs_now'

 L. 237        46  BUILD_MAP_0           0 
               48  STORE_FAST               'attrs_updated'

 L. 238        50  LOAD_FAST                'attrs_now'
               52  LOAD_METHOD              items
               54  CALL_METHOD_0         0  ''
               56  GET_ITER         
             58_0  COME_FROM           106  '106'
               58  FOR_ITER            118  'to 118'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'key'
               64  STORE_FAST               'value'

 L. 241        66  LOAD_FAST                'key'
               68  LOAD_FAST                'attrs_then'
               70  <118>                 1  ''
               72  POP_JUMP_IF_FALSE    84  'to 84'

 L. 242        74  LOAD_FAST                'value'
               76  LOAD_FAST                'attrs_updated'
               78  LOAD_FAST                'key'
               80  STORE_SUBSCR     
               82  JUMP_BACK            58  'to 58'
             84_0  COME_FROM            72  '72'

 L. 243        84  LOAD_GLOBAL              id
               86  LOAD_FAST                'attrs_now'
               88  LOAD_FAST                'key'
               90  BINARY_SUBSCR    
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_GLOBAL              id
               96  LOAD_FAST                'attrs_then'
               98  LOAD_FAST                'key'
              100  BINARY_SUBSCR    
              102  CALL_FUNCTION_1       1  ''
              104  COMPARE_OP               !=
              106  POP_JUMP_IF_FALSE    58  'to 58'

 L. 244       108  LOAD_FAST                'value'
              110  LOAD_FAST                'attrs_updated'
              112  LOAD_FAST                'key'
              114  STORE_SUBSCR     
              116  JUMP_BACK            58  'to 58'

 L. 245       118  LOAD_FAST                'self'
              120  LOAD_ATTR                __spec__
              122  LOAD_ATTR                loader
              124  LOAD_METHOD              exec_module
              126  LOAD_FAST                'self'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L. 248       132  LOAD_FAST                'original_name'
              134  LOAD_GLOBAL              sys
              136  LOAD_ATTR                modules
              138  <118>                 0  ''
              140  POP_JUMP_IF_FALSE   180  'to 180'

 L. 249       142  LOAD_GLOBAL              id
              144  LOAD_FAST                'self'
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_GLOBAL              id
              150  LOAD_GLOBAL              sys
              152  LOAD_ATTR                modules
              154  LOAD_FAST                'original_name'
              156  BINARY_SUBSCR    
              158  CALL_FUNCTION_1       1  ''
              160  COMPARE_OP               !=
              162  POP_JUMP_IF_FALSE   180  'to 180'

 L. 250       164  LOAD_GLOBAL              ValueError
              166  LOAD_STR                 'module object for '
              168  LOAD_FAST                'original_name'
              170  FORMAT_VALUE          2  '!r'
              172  LOAD_STR                 ' substituted in sys.modules during a lazy load'
              174  BUILD_STRING_3        3 
              176  CALL_FUNCTION_1       1  ''
              178  RAISE_VARARGS_1       1  'exception instance'
            180_0  COME_FROM           162  '162'
            180_1  COME_FROM           140  '140'

 L. 255       180  LOAD_FAST                'self'
              182  LOAD_ATTR                __dict__
              184  LOAD_METHOD              update
              186  LOAD_FAST                'attrs_updated'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L. 256       192  LOAD_GLOBAL              getattr
              194  LOAD_FAST                'self'
              196  LOAD_FAST                'attr'
              198  CALL_FUNCTION_2       2  ''
              200  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 70

    def __delattr__(self, attr):
        """Trigger the load and then perform the deletion."""
        self.__getattribute__(attr)
        delattrselfattr


class LazyLoader(abc.Loader):
    __doc__ = 'A loader that creates a module which defers loading until attribute access.'

    @staticmethod
    def __check_eager_loader(loader):
        if not hasattrloader'exec_module':
            raise TypeError('loader must define exec_module()')

    @classmethod
    def factory(cls, loader):
        """Construct a callable which returns the eager loader made lazy."""
        cls._LazyLoader__check_eager_loader(loader)
        return --- This code section failed: ---

 L. 279         0  LOAD_DEREF               'cls'
                2  LOAD_DEREF               'loader'
                4  LOAD_FAST                'args'
                6  BUILD_MAP_0           0 
                8  LOAD_FAST                'kwargs'
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  CALL_FUNCTION_1       1  ''
               16  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1

    def __init__(self, loader):
        self._LazyLoader__check_eager_loader(loader)
        self.loader = loader

    def create_module(self, spec):
        return self.loader.create_module(spec)

    def exec_module(self, module):
        """Make the module load lazily."""
        module.__spec__.loader = self.loader
        module.__loader__ = self.loader
        loader_state = {}
        loader_state['__dict__'] = module.__dict__.copy
        loader_state['__class__'] = module.__class__
        module.__spec__.loader_state = loader_state
        module.__class__ = _LazyModule