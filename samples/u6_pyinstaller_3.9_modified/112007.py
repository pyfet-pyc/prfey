# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\monkey.py
"""
Monkey patching of distutils.
"""
import sys, distutils.filelist, platform, types, functools
from importlib import import_module
import inspect, setuptools
__all__ = []

def _get_mro(cls):
    """
    Returns the bases classes for cls sorted by the MRO.

    Works around an issue on Jython where inspect.getmro will not return all
    base classes if multiple classes share the same name. Instead, this
    function will return a tuple containing the class itself, and the contents
    of cls.__bases__. See https://github.com/pypa/setuptools/issues/1024.
    """
    if platform.python_implementation() == 'Jython':
        return (
         cls,) + cls.__bases__
    return inspect.getmro(cls)


def get_unpatched(item):
    lookup = get_unpatched_class if isinstance(item, type) else get_unpatched_function if isinstance(item, types.FunctionType) else (lambda item: None)
    return lookup(item)


def get_unpatched_class(cls):
    """Protect against re-patching the distutils if reloaded

    Also ensures that no other distutils extension monkeypatched the distutils
    first.
    """
    external_bases = (cls for cls in _get_mro(cls) if not cls.__module__.startswith('setuptools'))
    base = next(external_bases)
    if not base.__module__.startswith('distutils'):
        msg = 'distutils has already been patched by %r' % cls
        raise AssertionError(msg)
    return base


def patch_all--- This code section failed: ---

 L.  65         0  LOAD_GLOBAL              setuptools
                2  LOAD_ATTR                Command
                4  LOAD_GLOBAL              distutils
                6  LOAD_ATTR                core
                8  STORE_ATTR               Command

 L.  67        10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                version_info
               14  LOAD_CONST               (3, 5, 3)
               16  COMPARE_OP               <=
               18  STORE_FAST               'has_issue_12885'

 L.  69        20  LOAD_FAST                'has_issue_12885'
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L.  71        24  LOAD_GLOBAL              setuptools
               26  LOAD_ATTR                findall
               28  LOAD_GLOBAL              distutils
               30  LOAD_ATTR                filelist
               32  STORE_ATTR               findall
             34_0  COME_FROM            22  '22'

 L.  74        34  LOAD_GLOBAL              sys
               36  LOAD_ATTR                version_info
               38  LOAD_CONST               (2, 7, 13)
               40  COMPARE_OP               <
               42  JUMP_IF_TRUE_OR_POP    94  'to 94'

 L.  76        44  LOAD_CONST               (3, 4)
               46  LOAD_GLOBAL              sys
               48  LOAD_ATTR                version_info
               50  DUP_TOP          
               52  ROT_THREE        
               54  COMPARE_OP               <
               56  JUMP_IF_FALSE_OR_POP    64  'to 64'
               58  LOAD_CONST               (3, 4, 6)
               60  COMPARE_OP               <
               62  JUMP_FORWARD         68  'to 68'
             64_0  COME_FROM            56  '56'
               64  ROT_TWO          
               66  POP_TOP          
             68_0  COME_FROM            62  '62'

 L.  74        68  JUMP_IF_TRUE_OR_POP    94  'to 94'

 L.  78        70  LOAD_CONST               (3, 5)
               72  LOAD_GLOBAL              sys
               74  LOAD_ATTR                version_info
               76  DUP_TOP          
               78  ROT_THREE        
               80  COMPARE_OP               <
               82  JUMP_IF_FALSE_OR_POP    90  'to 90'
               84  LOAD_CONST               (3, 5, 3)
               86  COMPARE_OP               <=
             88_0  COME_FROM            68  '68'
             88_1  COME_FROM            42  '42'
               88  JUMP_FORWARD         94  'to 94'
             90_0  COME_FROM            82  '82'
               90  ROT_TWO          
               92  POP_TOP          
             94_0  COME_FROM            88  '88'

 L.  73        94  STORE_FAST               'needs_warehouse'

 L.  81        96  LOAD_FAST                'needs_warehouse'
               98  POP_JUMP_IF_FALSE   114  'to 114'

 L.  82       100  LOAD_STR                 'https://upload.pypi.org/legacy/'
              102  STORE_FAST               'warehouse'

 L.  83       104  LOAD_FAST                'warehouse'
              106  LOAD_GLOBAL              distutils
              108  LOAD_ATTR                config
              110  LOAD_ATTR                PyPIRCCommand
              112  STORE_ATTR               DEFAULT_REPOSITORY
            114_0  COME_FROM            98  '98'

 L.  85       114  LOAD_GLOBAL              _patch_distribution_metadata
              116  CALL_FUNCTION_0       0  ''
              118  POP_TOP          

 L.  88       120  LOAD_GLOBAL              distutils
              122  LOAD_ATTR                dist
              124  LOAD_GLOBAL              distutils
              126  LOAD_ATTR                core
              128  LOAD_GLOBAL              distutils
              130  LOAD_ATTR                cmd
              132  BUILD_TUPLE_3         3 
              134  GET_ITER         
              136  FOR_ITER            152  'to 152'
              138  STORE_FAST               'module'

 L.  89       140  LOAD_GLOBAL              setuptools
              142  LOAD_ATTR                dist
              144  LOAD_ATTR                Distribution
              146  LOAD_FAST                'module'
              148  STORE_ATTR               Distribution
              150  JUMP_BACK           136  'to 136'

 L.  92       152  LOAD_GLOBAL              setuptools
              154  LOAD_ATTR                extension
              156  LOAD_ATTR                Extension
              158  LOAD_GLOBAL              distutils
              160  LOAD_ATTR                core
              162  STORE_ATTR               Extension

 L.  93       164  LOAD_GLOBAL              setuptools
              166  LOAD_ATTR                extension
              168  LOAD_ATTR                Extension
              170  LOAD_GLOBAL              distutils
              172  LOAD_ATTR                extension
              174  STORE_ATTR               Extension

 L.  94       176  LOAD_STR                 'distutils.command.build_ext'
              178  LOAD_GLOBAL              sys
              180  LOAD_ATTR                modules
              182  <118>                 0  ''
              184  POP_JUMP_IF_FALSE   202  'to 202'

 L.  96       186  LOAD_GLOBAL              setuptools
              188  LOAD_ATTR                extension
              190  LOAD_ATTR                Extension

 L.  95       192  LOAD_GLOBAL              sys
              194  LOAD_ATTR                modules
              196  LOAD_STR                 'distutils.command.build_ext'
              198  BINARY_SUBSCR    
              200  STORE_ATTR               Extension
            202_0  COME_FROM           184  '184'

 L.  99       202  LOAD_GLOBAL              patch_for_msvc_specialized_compiler
              204  CALL_FUNCTION_0       0  ''
              206  POP_TOP          

Parse error at or near `<118>' instruction at offset 182


def _patch_distribution_metadata():
    """Patch write_pkg_file and read_pkg_file for higher metadata standards"""
    for attr in ('write_pkg_file', 'read_pkg_file', 'get_metadata_version'):
        new_val = getattr(setuptools.dist, attr)
        setattr(distutils.dist.DistributionMetadata, attr, new_val)


def patch_func(replacement, target_mod, func_name):
    """
    Patch func_name in target_mod with replacement

    Important - original must be resolved by name to avoid
    patching an already patched function.
    """
    original = getattr(target_mod, func_name)
    vars(replacement).setdefault('unpatched', original)
    setattr(target_mod, func_name, replacement)


def get_unpatched_function(candidate):
    return getattr(candidate, 'unpatched')


def patch_for_msvc_specialized_compiler--- This code section failed: ---

 L. 136         0  LOAD_GLOBAL              import_module
                2  LOAD_STR                 'setuptools.msvc'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_DEREF              'msvc'

 L. 138         8  LOAD_GLOBAL              platform
               10  LOAD_METHOD              system
               12  CALL_METHOD_0         0  ''
               14  LOAD_STR                 'Windows'
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 140        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 142        24  LOAD_CLOSURE             'msvc'
               26  BUILD_TUPLE_1         1 
               28  LOAD_CODE                <code_object patch_params>
               30  LOAD_STR                 'patch_for_msvc_specialized_compiler.<locals>.patch_params'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               'patch_params'

 L. 155        36  LOAD_GLOBAL              functools
               38  LOAD_METHOD              partial
               40  LOAD_FAST                'patch_params'
               42  LOAD_STR                 'distutils.msvc9compiler'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'msvc9'

 L. 158        48  LOAD_GLOBAL              functools
               50  LOAD_METHOD              partial
               52  LOAD_FAST                'patch_params'
               54  LOAD_STR                 'distutils._msvccompiler'
               56  CALL_METHOD_2         2  ''
               58  STORE_FAST               'msvc14'

 L. 160        60  SETUP_FINALLY        90  'to 90'

 L. 162        62  LOAD_GLOBAL              patch_func
               64  LOAD_FAST                'msvc9'
               66  LOAD_STR                 'find_vcvarsall'
               68  CALL_FUNCTION_1       1  ''
               70  CALL_FUNCTION_EX      0  'positional arguments only'
               72  POP_TOP          

 L. 163        74  LOAD_GLOBAL              patch_func
               76  LOAD_FAST                'msvc9'
               78  LOAD_STR                 'query_vcvarsall'
               80  CALL_FUNCTION_1       1  ''
               82  CALL_FUNCTION_EX      0  'positional arguments only'
               84  POP_TOP          
               86  POP_BLOCK        
               88  JUMP_FORWARD        108  'to 108'
             90_0  COME_FROM_FINALLY    60  '60'

 L. 164        90  DUP_TOP          
               92  LOAD_GLOBAL              ImportError
               94  <121>               106  ''
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 165       102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
              106  <48>             
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            88  '88'

 L. 167       108  SETUP_FINALLY       126  'to 126'

 L. 169       110  LOAD_GLOBAL              patch_func
              112  LOAD_FAST                'msvc14'
              114  LOAD_STR                 '_get_vc_env'
              116  CALL_FUNCTION_1       1  ''
              118  CALL_FUNCTION_EX      0  'positional arguments only'
              120  POP_TOP          
              122  POP_BLOCK        
              124  JUMP_FORWARD        144  'to 144'
            126_0  COME_FROM_FINALLY   108  '108'

 L. 170       126  DUP_TOP          
              128  LOAD_GLOBAL              ImportError
              130  <121>               142  ''
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 171       138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
              142  <48>             
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM           124  '124'

 L. 173       144  SETUP_FINALLY       162  'to 162'

 L. 175       146  LOAD_GLOBAL              patch_func
              148  LOAD_FAST                'msvc14'
              150  LOAD_STR                 'gen_lib_options'
              152  CALL_FUNCTION_1       1  ''
              154  CALL_FUNCTION_EX      0  'positional arguments only'
              156  POP_TOP          
              158  POP_BLOCK        
              160  JUMP_FORWARD        180  'to 180'
            162_0  COME_FROM_FINALLY   144  '144'

 L. 176       162  DUP_TOP          
              164  LOAD_GLOBAL              ImportError
              166  <121>               178  ''
              168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          

 L. 177       174  POP_EXCEPT       
              176  JUMP_FORWARD        180  'to 180'
              178  <48>             
            180_0  COME_FROM           176  '176'
            180_1  COME_FROM           160  '160'

Parse error at or near `<121>' instruction at offset 94