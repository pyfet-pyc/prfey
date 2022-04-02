# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: runpy.py
"""runpy.py - locating and running Python code using the module namespace

Provides support for locating and running Python scripts using the Python
module namespace instead of the native filesystem.

This allows Python code to play nicely with non-filesystem based PEP 302
importers when locating support scripts as well as when importing modules.
"""
import sys, importlib.machinery, importlib.util, io, types
from pkgutil import read_code, get_importer
__all__ = [
 'run_module', 'run_path']

class _TempModule(object):
    __doc__ = 'Temporarily replace a module in sys.modules with an empty namespace'

    def __init__(self, mod_name):
        self.mod_name = mod_name
        self.module = types.ModuleType(mod_name)
        self._saved_module = []

    def __enter__(self):
        mod_name = self.mod_name
        try:
            self._saved_module.append(sys.modules[mod_name])
        except KeyError:
            pass
        else:
            sys.modules[mod_name] = self.module
            return self

    def __exit__(self, *args):
        if self._saved_module:
            sys.modules[self.mod_name] = self._saved_module[0]
        else:
            del sys.modules[self.mod_name]
        self._saved_module = []


class _ModifiedArgv0(object):

    def __init__(self, value):
        self.value = value
        self._saved_value = self._sentinel = object()

    def __enter__(self):
        if self._saved_value is not self._sentinel:
            raise RuntimeError('Already preserving saved value')
        self._saved_value = sys.argv[0]
        sys.argv[0] = self.value

    def __exit__(self, *args):
        self.value = self._sentinel
        sys.argv[0] = self._saved_value


def _run_code(code, run_globals, init_globals=None, mod_name=None, mod_spec=None, pkg_name=None, script_name=None):
    """Helper to run code in nominated namespace"""
    if init_globals is not None:
        run_globals.update(init_globals)
    elif mod_spec is None:
        loader = None
        fname = script_name
        cached = None
    else:
        loader = mod_spec.loader
        fname = mod_spec.origin
        cached = mod_spec.cached
        if pkg_name is None:
            pkg_name = mod_spec.parent
    run_globals.update(__name__=mod_name, __file__=fname,
      __cached__=cached,
      __doc__=None,
      __loader__=loader,
      __package__=pkg_name,
      __spec__=mod_spec)
    exec(code, run_globals)
    return run_globals


def _run_module_code(code, init_globals=None, mod_name=None, mod_spec=None, pkg_name=None, script_name=None):
    """Helper to run code in new namespace with sys modified"""
    fname = script_name if mod_spec is None else mod_spec.origin
    with _TempModule(mod_name) as (temp_module):
        with _ModifiedArgv0(fname):
            mod_globals = temp_module.module.__dict__
            _run_code(code, mod_globals, init_globals, mod_name, mod_spec, pkg_name, script_name)
    return mod_globals.copy()


def _get_module_details(mod_name, error=ImportError):
    if mod_name.startswith('.'):
        raise error('Relative module names not supported')
    else:
        pkg_name, _, _ = mod_name.rpartition('.')
        if pkg_name:
            try:
                __import__(pkg_name)
            except ImportError as e:
                try:
                    if (e.name is None or e.name) != pkg_name:
                        if not pkg_name.startswith(e.name + '.'):
                            raise
                finally:
                    e = None
                    del e

            else:
                existing = sys.modules.get(mod_name)
                if existing is not None:
                    if not hasattr(existing, '__path__'):
                        from warnings import warn
                        msg = '{mod_name!r} found in sys.modules after import of package {pkg_name!r}, but prior to execution of {mod_name!r}; this may result in unpredictable behaviour'.format(mod_name=mod_name,
                          pkg_name=pkg_name)
                        warn(RuntimeWarning(msg))
        try:
            spec = importlib.util.find_spec(mod_name)
        except (ImportError, AttributeError, TypeError, ValueError) as ex:
            try:
                msg = 'Error while finding module specification for {!r} ({}: {})'
                raise error(msg.format(mod_name, type(ex).__name__, ex)) from ex
            finally:
                ex = None
                del ex

        else:
            if spec is None:
                raise error('No module named %s' % mod_name)
            if spec.submodule_search_locations is not None and not mod_name == '__main__':
                if mod_name.endswith('.__main__'):
                    raise error('Cannot use package as __main__ module')
                try:
                    pkg_main_name = mod_name + '.__main__'
                    return _get_module_details(pkg_main_name, error)
                            except error as e:
                    try:
                        if mod_name not in sys.modules:
                            raise
                        raise error('%s; %r is a package and cannot be directly executed' % (
                         e, mod_name))
                    finally:
                        e = None
                        del e

            loader = spec.loader
            if loader is None:
                raise error('%r is a namespace package and cannot be executed' % mod_name)
    try:
        code = loader.get_code(mod_name)
    except ImportError as e:
        try:
            raise error(format(e)) from e
        finally:
            e = None
            del e

    else:
        if code is None:
            raise error('No code object available for %s' % mod_name)
        return (
         mod_name, spec, code)


class _Error(Exception):
    __doc__ = 'Error that _run_module_as_main() should report without a traceback'


def _run_module_as_main(mod_name, alter_argv=True):
    """Runs the designated module in the __main__ namespace

       Note that the executed module will have full access to the
       __main__ namespace. If this is not desirable, the run_module()
       function should be used to run the module code in a fresh namespace.

       At the very least, these variables in __main__ will be overwritten:
           __name__
           __file__
           __cached__
           __loader__
           __package__
    """
    try:
        if alter_argv or mod_name != '__main__':
            mod_name, mod_spec, code = _get_module_details(mod_name, _Error)
        else:
            mod_name, mod_spec, code = _get_main_module_details(_Error)
    except _Error as exc:
        try:
            msg = '%s: %s' % (sys.executable, exc)
            sys.exit(msg)
        finally:
            exc = None
            del exc

    else:
        main_globals = sys.modules['__main__'].__dict__
        if alter_argv:
            sys.argv[0] = mod_spec.origin
        return _run_code(code, main_globals, None, '__main__', mod_spec)


def run_module(mod_name, init_globals=None, run_name=None, alter_sys=False):
    """Execute a module's code without importing it

       Returns the resulting top level namespace dictionary
    """
    mod_name, mod_spec, code = _get_module_details(mod_name)
    if run_name is None:
        run_name = mod_name
    if alter_sys:
        return _run_module_code(code, init_globals, run_name, mod_spec)
    return _run_code(code, {}, init_globals, run_name, mod_spec)


def _get_main_module_details--- This code section failed: ---

 L. 216         0  LOAD_STR                 '__main__'
                2  STORE_FAST               'main_name'

 L. 217         4  LOAD_GLOBAL              sys
                6  LOAD_ATTR                modules
                8  LOAD_FAST                'main_name'
               10  BINARY_SUBSCR    
               12  STORE_FAST               'saved_main'

 L. 218        14  LOAD_GLOBAL              sys
               16  LOAD_ATTR                modules
               18  LOAD_FAST                'main_name'
               20  DELETE_SUBSCR    

 L. 219        22  SETUP_FINALLY       116  'to 116'
               24  SETUP_FINALLY        40  'to 40'

 L. 220        26  LOAD_GLOBAL              _get_module_details
               28  LOAD_FAST                'main_name'
               30  CALL_FUNCTION_1       1  ''
               32  POP_BLOCK        
               34  POP_BLOCK        
               36  CALL_FINALLY        116  'to 116'
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    24  '24'

 L. 221        40  DUP_TOP          
               42  LOAD_GLOBAL              ImportError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE   110  'to 110'
               48  POP_TOP          
               50  STORE_FAST               'exc'
               52  POP_TOP          
               54  SETUP_FINALLY        98  'to 98'

 L. 222        56  LOAD_FAST                'main_name'
               58  LOAD_GLOBAL              str
               60  LOAD_FAST                'exc'
               62  CALL_FUNCTION_1       1  ''
               64  COMPARE_OP               in
               66  POP_JUMP_IF_FALSE    92  'to 92'

 L. 223        68  LOAD_FAST                'error'
               70  LOAD_STR                 "can't find %r module in %r"

 L. 224        72  LOAD_FAST                'main_name'
               74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                path
               78  LOAD_CONST               0
               80  BINARY_SUBSCR    
               82  BUILD_TUPLE_2         2 

 L. 223        84  BINARY_MODULO    
               86  CALL_FUNCTION_1       1  ''

 L. 224        88  LOAD_FAST                'exc'

 L. 223        90  RAISE_VARARGS_2       2  'exception instance with __cause__'
             92_0  COME_FROM            66  '66'

 L. 225        92  RAISE_VARARGS_0       0  'reraise'
               94  POP_BLOCK        
               96  BEGIN_FINALLY    
             98_0  COME_FROM_FINALLY    54  '54'
               98  LOAD_CONST               None
              100  STORE_FAST               'exc'
              102  DELETE_FAST              'exc'
              104  END_FINALLY      
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM            46  '46'
              110  END_FINALLY      
            112_0  COME_FROM           108  '108'
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM            36  '36'
            116_1  COME_FROM_FINALLY    22  '22'

 L. 227       116  LOAD_FAST                'saved_main'
              118  LOAD_GLOBAL              sys
              120  LOAD_ATTR                modules
              122  LOAD_FAST                'main_name'
              124  STORE_SUBSCR     
              126  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 34


def _get_code_from_file(run_name, fname):
    with io.open_code(fname) as (f):
        code = read_code(f)
    if code is None:
        with io.open_code(fname) as (f):
            code = compile(f.read(), fname, 'exec')
    return (
     code, fname)


def run_path--- This code section failed: ---

 L. 250         0  LOAD_FAST                'run_name'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 251         8  LOAD_STR                 '<run_path>'
               10  STORE_FAST               'run_name'
             12_0  COME_FROM             6  '6'

 L. 252        12  LOAD_FAST                'run_name'
               14  LOAD_METHOD              rpartition
               16  LOAD_STR                 '.'
               18  CALL_METHOD_1         1  ''
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  STORE_FAST               'pkg_name'

 L. 253        26  LOAD_GLOBAL              get_importer
               28  LOAD_FAST                'path_name'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'importer'

 L. 255        34  LOAD_CONST               False
               36  STORE_FAST               'is_NullImporter'

 L. 256        38  LOAD_GLOBAL              type
               40  LOAD_FAST                'importer'
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_ATTR                __module__
               46  LOAD_STR                 'imp'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    70  'to 70'

 L. 257        52  LOAD_GLOBAL              type
               54  LOAD_FAST                'importer'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_ATTR                __name__
               60  LOAD_STR                 'NullImporter'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    70  'to 70'

 L. 258        66  LOAD_CONST               True
               68  STORE_FAST               'is_NullImporter'
             70_0  COME_FROM            64  '64'
             70_1  COME_FROM            50  '50'

 L. 259        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'importer'
               74  LOAD_GLOBAL              type
               76  LOAD_CONST               None
               78  CALL_FUNCTION_1       1  ''
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_TRUE     88  'to 88'
               84  LOAD_FAST                'is_NullImporter'
               86  POP_JUMP_IF_FALSE   120  'to 120'
             88_0  COME_FROM            82  '82'

 L. 262        88  LOAD_GLOBAL              _get_code_from_file
               90  LOAD_FAST                'run_name'
               92  LOAD_FAST                'path_name'
               94  CALL_FUNCTION_2       2  ''
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'code'
              100  STORE_FAST               'fname'

 L. 263       102  LOAD_GLOBAL              _run_module_code
              104  LOAD_FAST                'code'
              106  LOAD_FAST                'init_globals'
              108  LOAD_FAST                'run_name'

 L. 264       110  LOAD_FAST                'pkg_name'

 L. 264       112  LOAD_FAST                'fname'

 L. 263       114  LOAD_CONST               ('pkg_name', 'script_name')
              116  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              118  RETURN_VALUE     
            120_0  COME_FROM            86  '86'

 L. 268       120  LOAD_GLOBAL              sys
              122  LOAD_ATTR                path
              124  LOAD_METHOD              insert
              126  LOAD_CONST               0
              128  LOAD_FAST                'path_name'
              130  CALL_METHOD_2         2  ''
              132  POP_TOP          

 L. 269       134  SETUP_FINALLY       246  'to 246'

 L. 276       136  LOAD_GLOBAL              _get_main_module_details
              138  CALL_FUNCTION_0       0  ''
              140  UNPACK_SEQUENCE_3     3 
              142  STORE_FAST               'mod_name'
              144  STORE_FAST               'mod_spec'
              146  STORE_FAST               'code'

 L. 277       148  LOAD_GLOBAL              _TempModule
              150  LOAD_FAST                'run_name'
              152  CALL_FUNCTION_1       1  ''
              154  SETUP_WITH          236  'to 236'
              156  STORE_FAST               'temp_module'

 L. 278       158  LOAD_GLOBAL              _ModifiedArgv0
              160  LOAD_FAST                'path_name'
              162  CALL_FUNCTION_1       1  ''

 L. 277       164  SETUP_WITH          226  'to 226'
              166  POP_TOP          

 L. 279       168  LOAD_FAST                'temp_module'
              170  LOAD_ATTR                module
              172  LOAD_ATTR                __dict__
              174  STORE_FAST               'mod_globals'

 L. 280       176  LOAD_GLOBAL              _run_code
              178  LOAD_FAST                'code'
              180  LOAD_FAST                'mod_globals'
              182  LOAD_FAST                'init_globals'

 L. 281       184  LOAD_FAST                'run_name'

 L. 281       186  LOAD_FAST                'mod_spec'

 L. 281       188  LOAD_FAST                'pkg_name'

 L. 280       190  CALL_FUNCTION_6       6  ''
              192  LOAD_METHOD              copy
              194  CALL_METHOD_0         0  ''
              196  POP_BLOCK        
              198  ROT_TWO          
              200  BEGIN_FINALLY    
              202  WITH_CLEANUP_START
              204  WITH_CLEANUP_FINISH
              206  POP_FINALLY           0  ''
              208  POP_BLOCK        
              210  ROT_TWO          
              212  BEGIN_FINALLY    
              214  WITH_CLEANUP_START
              216  WITH_CLEANUP_FINISH
              218  POP_FINALLY           0  ''
              220  POP_BLOCK        
              222  CALL_FINALLY        246  'to 246'
              224  RETURN_VALUE     
            226_0  COME_FROM_WITH      164  '164'
              226  WITH_CLEANUP_START
              228  WITH_CLEANUP_FINISH
              230  END_FINALLY      
              232  POP_BLOCK        
              234  BEGIN_FINALLY    
            236_0  COME_FROM_WITH      154  '154'
              236  WITH_CLEANUP_START
              238  WITH_CLEANUP_FINISH
              240  END_FINALLY      
              242  POP_BLOCK        
              244  BEGIN_FINALLY    
            246_0  COME_FROM           222  '222'
            246_1  COME_FROM_FINALLY   134  '134'

 L. 283       246  SETUP_FINALLY       264  'to 264'

 L. 284       248  LOAD_GLOBAL              sys
              250  LOAD_ATTR                path
              252  LOAD_METHOD              remove
              254  LOAD_FAST                'path_name'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          
              260  POP_BLOCK        
              262  JUMP_FORWARD        286  'to 286'
            264_0  COME_FROM_FINALLY   246  '246'

 L. 285       264  DUP_TOP          
              266  LOAD_GLOBAL              ValueError
              268  COMPARE_OP               exception-match
          270_272  POP_JUMP_IF_FALSE   284  'to 284'
              274  POP_TOP          
              276  POP_TOP          
              278  POP_TOP          

 L. 286       280  POP_EXCEPT       
              282  JUMP_FORWARD        286  'to 286'
            284_0  COME_FROM           270  '270'
              284  END_FINALLY      
            286_0  COME_FROM           282  '282'
            286_1  COME_FROM           262  '262'
              286  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 198


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No module specified for execution', file=(sys.stderr))
    else:
        del sys.argv[0]
        _run_module_as_main(sys.argv[0])