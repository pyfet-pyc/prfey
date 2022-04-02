# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
        return self.attribute is None or (self.format is None) or ((str(version) != 'unknown') and (version >= self.requested_version))

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


def maybe_close(f):

    @contextlib.contextmanager
    def empty():
        yield

    if not f:
        return empty()
    return contextlib.closing(f)


def get_module_constant(module, symbol, default=-1, paths=None):
    """Find 'module' by searching 'paths', and extract 'symbol'

    Return 'None' if 'module' does not exist on 'paths', or it does not define
    'symbol'.  If the module defines 'symbol' as a constant, return the
    constant.  Otherwise, return 'default'."""
    try:
        f, path, (suffix, mode, kind) = info = find_module(module, paths)
    except ImportError:
        return
    else:
        with maybe_close(f):
            if kind == PY_COMPILED:
                f.read(8)
                code = marshal.load(f)
            elif kind == PY_FROZEN:
                code = _imp.get_frozen_object(module, paths)
            elif kind == PY_SOURCE:
                code = compile(f.read, path, 'exec')
            else:
                imported = _imp.get_module(module, paths, info)
                return getattr(imported, symbol, None)
        return extract_constant(code, symbol, default)


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