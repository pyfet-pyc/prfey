# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\setuptools\depends.py
import sys, imp, marshal
from distutils.version import StrictVersion
from imp import PKG_DIRECTORY, PY_COMPILED, PY_SOURCE, PY_FROZEN
from .py33compat import Bytecode
__all__ = [
 'Require', 'find_module', 'get_module_constant', 'extract_constant']

class Require:
    __doc__ = 'A prerequisite to building or installing a distribution'

    def __init__(self, name, requested_version, module, homepage='', attribute=None, format=None):
        if format is None:
            if requested_version is not None:
                format = StrictVersion
        if format is not None:
            requested_version = format(requested_version)
            if attribute is None:
                attribute = '__version__'
        self.__dict__.update(locals())
        del self.self

    def full_name(self):
        """Return full package/distribution name, w/version"""
        if self.requested_version is not None:
            return '%s-%s' % (self.name, self.requested_version)
        return self.name

    def version_ok(self, version):
        """Is 'version' sufficiently up-to-date?"""
        return self.attribute is None or (self.format is None) or ((str(version) != 'unknown') and (version >= self.requested_version))

    def get_version--- This code section failed: ---

 L.  54         0  LOAD_FAST                'self'
                2  LOAD_ATTR                attribute
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    70  'to 70'

 L.  55        10  SETUP_FINALLY        48  'to 48'

 L.  56        12  LOAD_GLOBAL              find_module
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                module
               18  LOAD_FAST                'paths'
               20  CALL_FUNCTION_2       2  ''
               22  UNPACK_SEQUENCE_3     3 
               24  STORE_FAST               'f'
               26  STORE_FAST               'p'
               28  STORE_FAST               'i'

 L.  57        30  LOAD_FAST                'f'
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L.  58        34  LOAD_FAST                'f'
               36  LOAD_METHOD              close
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          
             42_0  COME_FROM            32  '32'

 L.  59        42  LOAD_FAST                'default'
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    10  '10'

 L.  60        48  DUP_TOP          
               50  LOAD_GLOBAL              ImportError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    68  'to 68'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  61        62  POP_EXCEPT       
               64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            54  '54'
               68  END_FINALLY      
             70_0  COME_FROM             8  '8'

 L.  63        70  LOAD_GLOBAL              get_module_constant
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                module
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                attribute
               80  LOAD_FAST                'default'
               82  LOAD_FAST                'paths'
               84  CALL_FUNCTION_4       4  ''
               86  STORE_FAST               'v'

 L.  65        88  LOAD_FAST                'v'
               90  LOAD_CONST               None
               92  COMPARE_OP               is-not
               94  POP_JUMP_IF_FALSE   124  'to 124'
               96  LOAD_FAST                'v'
               98  LOAD_FAST                'default'
              100  COMPARE_OP               is-not
              102  POP_JUMP_IF_FALSE   124  'to 124'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                format
              108  LOAD_CONST               None
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_FALSE   124  'to 124'

 L.  66       114  LOAD_FAST                'self'
              116  LOAD_METHOD              format
              118  LOAD_FAST                'v'
              120  CALL_METHOD_1         1  ''
              122  RETURN_VALUE     
            124_0  COME_FROM           112  '112'
            124_1  COME_FROM           102  '102'
            124_2  COME_FROM            94  '94'

 L.  68       124  LOAD_FAST                'v'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 64

    def is_present(self, paths=None):
        """Return true if dependency is present on 'paths'"""
        return self.get_version(paths) is not None

    def is_current(self, paths=None):
        """Return true if dependency is present and up-to-date on 'paths'"""
        version = self.get_version(paths)
        if version is None:
            return False
        return self.version_ok(version)


def find_module(module, paths=None):
    """Just like 'imp.find_module()', but with package support"""
    parts = module.split('.')
    while True:
        if parts:
            part = parts.pop(0)
            f, path, (suffix, mode, kind) = info = imp.find_module(part, paths)
            if kind == PKG_DIRECTORY:
                parts = parts or ['__init__']
                paths = [path]
            else:
                if parts:
                    raise ImportError("Can't find %r in %s" % (parts, module))

    return info


def get_module_constant--- This code section failed: ---

 L. 108         0  SETUP_FINALLY        28  'to 28'

 L. 109         2  LOAD_GLOBAL              find_module
                4  LOAD_FAST                'module'
                6  LOAD_FAST                'paths'
                8  CALL_FUNCTION_2       2  ''
               10  UNPACK_SEQUENCE_3     3 
               12  STORE_FAST               'f'
               14  STORE_FAST               'path'
               16  UNPACK_SEQUENCE_3     3 
               18  STORE_FAST               'suffix'
               20  STORE_FAST               'mode'
               22  STORE_FAST               'kind'
               24  POP_BLOCK        
               26  JUMP_FORWARD         50  'to 50'
             28_0  COME_FROM_FINALLY     0  '0'

 L. 110        28  DUP_TOP          
               30  LOAD_GLOBAL              ImportError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    48  'to 48'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 112        42  POP_EXCEPT       
               44  LOAD_CONST               None
               46  RETURN_VALUE     
             48_0  COME_FROM            34  '34'
               48  END_FINALLY      
             50_0  COME_FROM            26  '26'

 L. 114        50  SETUP_FINALLY       186  'to 186'

 L. 115        52  LOAD_FAST                'kind'
               54  LOAD_GLOBAL              PY_COMPILED
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    82  'to 82'

 L. 116        60  LOAD_FAST                'f'
               62  LOAD_METHOD              read
               64  LOAD_CONST               8
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L. 117        70  LOAD_GLOBAL              marshal
               72  LOAD_METHOD              load
               74  LOAD_FAST                'f'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'code'
               80  JUMP_FORWARD        182  'to 182'
             82_0  COME_FROM            58  '58'

 L. 118        82  LOAD_FAST                'kind'
               84  LOAD_GLOBAL              PY_FROZEN
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   102  'to 102'

 L. 119        90  LOAD_GLOBAL              imp
               92  LOAD_METHOD              get_frozen_object
               94  LOAD_FAST                'module'
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'code'
              100  JUMP_FORWARD        182  'to 182'
            102_0  COME_FROM            88  '88'

 L. 120       102  LOAD_FAST                'kind'
              104  LOAD_GLOBAL              PY_SOURCE
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   128  'to 128'

 L. 121       110  LOAD_GLOBAL              compile
              112  LOAD_FAST                'f'
              114  LOAD_METHOD              read
              116  CALL_METHOD_0         0  ''
              118  LOAD_FAST                'path'
              120  LOAD_STR                 'exec'
              122  CALL_FUNCTION_3       3  ''
              124  STORE_FAST               'code'
              126  JUMP_FORWARD        182  'to 182'
            128_0  COME_FROM           108  '108'

 L. 124       128  LOAD_FAST                'module'
              130  LOAD_GLOBAL              sys
              132  LOAD_ATTR                modules
              134  COMPARE_OP               not-in
              136  POP_JUMP_IF_FALSE   160  'to 160'

 L. 125       138  LOAD_GLOBAL              imp
              140  LOAD_METHOD              load_module
              142  LOAD_FAST                'module'
              144  LOAD_FAST                'f'
              146  LOAD_FAST                'path'
              148  LOAD_FAST                'suffix'
              150  LOAD_FAST                'mode'
              152  LOAD_FAST                'kind'
              154  BUILD_TUPLE_3         3 
              156  CALL_METHOD_4         4  ''
              158  POP_TOP          
            160_0  COME_FROM           136  '136'

 L. 126       160  LOAD_GLOBAL              getattr
              162  LOAD_GLOBAL              sys
              164  LOAD_ATTR                modules
              166  LOAD_FAST                'module'
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'symbol'
              172  LOAD_CONST               None
              174  CALL_FUNCTION_3       3  ''
              176  POP_BLOCK        
              178  CALL_FINALLY        186  'to 186'
              180  RETURN_VALUE     
            182_0  COME_FROM           126  '126'
            182_1  COME_FROM           100  '100'
            182_2  COME_FROM            80  '80'
              182  POP_BLOCK        
              184  BEGIN_FINALLY    
            186_0  COME_FROM           178  '178'
            186_1  COME_FROM_FINALLY    50  '50'

 L. 129       186  LOAD_FAST                'f'
              188  POP_JUMP_IF_FALSE   198  'to 198'

 L. 130       190  LOAD_FAST                'f'
              192  LOAD_METHOD              close
              194  CALL_METHOD_0         0  ''
              196  POP_TOP          
            198_0  COME_FROM           188  '188'
              198  END_FINALLY      

 L. 132       200  LOAD_GLOBAL              extract_constant
              202  LOAD_FAST                'code'
              204  LOAD_FAST                'symbol'
              206  LOAD_FAST                'default'
              208  CALL_FUNCTION_3       3  ''
              210  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 178


def extract_constant(code, symbol, default=-1):
    """Extract the constant value of 'symbol' from 'code'

    If the name 'symbol' is bound to a constant value by the Python code
    object 'code', return that value.  If 'symbol' is bound to an expression,
    return 'default'.  Otherwise, return 'None'.

    Return value is based on the first assignment to 'symbol'.  'symbol' must
    be a global, or at least a non-"fast" local in the code block.  That is,
    only 'STORE_NAME' and 'STORE_GLOBAL' opcodes are checked, and 'symbol'
    must be present in 'code.co_names'.
    """
    if symbol not in code.co_names:
        return
    name_idx = list(code.co_names).index(symbol)
    STORE_NAME = 90
    STORE_GLOBAL = 97
    LOAD_CONST = 100
    const = default
    for byte_code in Bytecode(code):
        op = byte_code.opcode
        arg = byte_code.arg
        if op == LOAD_CONST:
            const = code.co_consts[arg]
        else:
            if arg == name_idx:
                if op == STORE_NAME or (op == STORE_GLOBAL):
                    return const
                const = default


def _update_globals():
    """
    Patch the globals to remove the objects not available on some platforms.

    XXX it'd be better to test assertions about bytecode instead.
    """
    if not sys.platform.startswith('java'):
        if sys.platform != 'cli':
            return
    incompatible = ('extract_constant', 'get_module_constant')
    for name in incompatible:
        del globals()[name]
        __all__.remove(name)


_update_globals()