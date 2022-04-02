# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\depends.py
import sys, marshal, contextlib, dis
from distutils.version import StrictVersion
from ._imp import find_module, PY_COMPILED, PY_FROZEN, PY_SOURCE
from . import _imp
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
        return self.attribute is None or self.format is None or str(version) != 'unknown' and version >= self.requested_version

    def get_version--- This code section failed: ---

 L.  56         0  LOAD_FAST                'self'
                2  LOAD_ATTR                attribute
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    70  'to 70'

 L.  57        10  SETUP_FINALLY        48  'to 48'

 L.  58        12  LOAD_GLOBAL              find_module
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                module
               18  LOAD_FAST                'paths'
               20  CALL_FUNCTION_2       2  ''
               22  UNPACK_SEQUENCE_3     3 
               24  STORE_FAST               'f'
               26  STORE_FAST               'p'
               28  STORE_FAST               'i'

 L.  59        30  LOAD_FAST                'f'
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L.  60        34  LOAD_FAST                'f'
               36  LOAD_METHOD              close
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          
             42_0  COME_FROM            32  '32'

 L.  61        42  LOAD_FAST                'default'
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    10  '10'

 L.  62        48  DUP_TOP          
               50  LOAD_GLOBAL              ImportError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    68  'to 68'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  63        62  POP_EXCEPT       
               64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            54  '54'
               68  END_FINALLY      
             70_0  COME_FROM             8  '8'

 L.  65        70  LOAD_GLOBAL              get_module_constant
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                module
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                attribute
               80  LOAD_FAST                'default'
               82  LOAD_FAST                'paths'
               84  CALL_FUNCTION_4       4  ''
               86  STORE_FAST               'v'

 L.  67        88  LOAD_FAST                'v'
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

 L.  68       114  LOAD_FAST                'self'
              116  LOAD_METHOD              format
              118  LOAD_FAST                'v'
              120  CALL_METHOD_1         1  ''
              122  RETURN_VALUE     
            124_0  COME_FROM           112  '112'
            124_1  COME_FROM           102  '102'
            124_2  COME_FROM            94  '94'

 L.  70       124  LOAD_FAST                'v'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 58

    def is_present(self, paths=None):
        """Return true if dependency is present on 'paths'"""
        return self.get_version(paths) is not None

    def is_current(self, paths=None):
        """Return true if dependency is present and up-to-date on 'paths'"""
        version = self.get_version(paths)
        if version is None:
            return False
        return self.version_ok(version)


def maybe_close(f):

    @contextlib.contextmanager
    def empty():
        (yield)

    if not f:
        return empty()
    return contextlib.closing(f)


def get_module_constant--- This code section failed: ---

 L. 102         0  SETUP_FINALLY        32  'to 32'

 L. 103         2  LOAD_GLOBAL              find_module
                4  LOAD_FAST                'module'
                6  LOAD_FAST                'paths'
                8  CALL_FUNCTION_2       2  ''
               10  DUP_TOP          
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'f'
               16  STORE_FAST               'path'
               18  UNPACK_SEQUENCE_3     3 
               20  STORE_FAST               'suffix'
               22  STORE_FAST               'mode'
               24  STORE_FAST               'kind'
               26  STORE_FAST               'info'
               28  POP_BLOCK        
               30  JUMP_FORWARD         54  'to 54'
             32_0  COME_FROM_FINALLY     0  '0'

 L. 104        32  DUP_TOP          
               34  LOAD_GLOBAL              ImportError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    52  'to 52'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 106        46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            38  '38'
               52  END_FINALLY      
             54_0  COME_FROM            30  '30'

 L. 108        54  LOAD_GLOBAL              maybe_close
               56  LOAD_FAST                'f'
               58  CALL_FUNCTION_1       1  ''
               60  SETUP_WITH          184  'to 184'
               62  POP_TOP          

 L. 109        64  LOAD_FAST                'kind'
               66  LOAD_GLOBAL              PY_COMPILED
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    94  'to 94'

 L. 110        72  LOAD_FAST                'f'
               74  LOAD_METHOD              read
               76  LOAD_CONST               8
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 111        82  LOAD_GLOBAL              marshal
               84  LOAD_METHOD              load
               86  LOAD_FAST                'f'
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'code'
               92  JUMP_FORWARD        180  'to 180'
             94_0  COME_FROM            70  '70'

 L. 112        94  LOAD_FAST                'kind'
               96  LOAD_GLOBAL              PY_FROZEN
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   116  'to 116'

 L. 113       102  LOAD_GLOBAL              _imp
              104  LOAD_METHOD              get_frozen_object
              106  LOAD_FAST                'module'
              108  LOAD_FAST                'paths'
              110  CALL_METHOD_2         2  ''
              112  STORE_FAST               'code'
              114  JUMP_FORWARD        180  'to 180'
            116_0  COME_FROM           100  '100'

 L. 114       116  LOAD_FAST                'kind'
              118  LOAD_GLOBAL              PY_SOURCE
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   142  'to 142'

 L. 115       124  LOAD_GLOBAL              compile
              126  LOAD_FAST                'f'
              128  LOAD_METHOD              read
              130  CALL_METHOD_0         0  ''
              132  LOAD_FAST                'path'
              134  LOAD_STR                 'exec'
              136  CALL_FUNCTION_3       3  ''
              138  STORE_FAST               'code'
              140  JUMP_FORWARD        180  'to 180'
            142_0  COME_FROM           122  '122'

 L. 118       142  LOAD_GLOBAL              _imp
              144  LOAD_METHOD              get_module
              146  LOAD_FAST                'module'
              148  LOAD_FAST                'paths'
              150  LOAD_FAST                'info'
              152  CALL_METHOD_3         3  ''
              154  STORE_FAST               'imported'

 L. 119       156  LOAD_GLOBAL              getattr
              158  LOAD_FAST                'imported'
              160  LOAD_FAST                'symbol'
              162  LOAD_CONST               None
              164  CALL_FUNCTION_3       3  ''
              166  POP_BLOCK        
              168  ROT_TWO          
              170  BEGIN_FINALLY    
              172  WITH_CLEANUP_START
              174  WITH_CLEANUP_FINISH
              176  POP_FINALLY           0  ''
              178  RETURN_VALUE     
            180_0  COME_FROM           140  '140'
            180_1  COME_FROM           114  '114'
            180_2  COME_FROM            92  '92'
              180  POP_BLOCK        
              182  BEGIN_FINALLY    
            184_0  COME_FROM_WITH       60  '60'
              184  WITH_CLEANUP_START
              186  WITH_CLEANUP_FINISH
              188  END_FINALLY      

 L. 121       190  LOAD_GLOBAL              extract_constant
              192  LOAD_FAST                'code'
              194  LOAD_FAST                'symbol'
              196  LOAD_FAST                'default'
              198  CALL_FUNCTION_3       3  ''
              200  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 168


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
    for byte_code in dis.Bytecode(code):
        op = byte_code.opcode
        arg = byte_code.arg
        if op == LOAD_CONST:
            const = code.co_consts[arg]
        else:
            if arg == name_idx:
                if op == STORE_NAME or op == STORE_GLOBAL:
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