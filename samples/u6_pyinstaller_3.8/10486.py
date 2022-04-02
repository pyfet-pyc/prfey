# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: importlib\__init__.py
"""A pure Python implementation of import."""
__all__ = ['__import__', 'import_module', 'invalidate_caches', 'reload']
import _imp, sys
try:
    import _frozen_importlib as _bootstrap
except ImportError:
    from . import _bootstrap
    _bootstrap._setup(sys, _imp)
else:
    _bootstrap.__name__ = 'importlib._bootstrap'
    _bootstrap.__package__ = 'importlib'
    try:
        _bootstrap.__file__ = __file__.replace('__init__.py', '_bootstrap.py')
    except NameError:
        pass
    else:
        sys.modules['importlib._bootstrap'] = _bootstrap
    try:
        import _frozen_importlib_external as _bootstrap_external
    except ImportError:
        from . import _bootstrap_external
        _bootstrap_external._setup(_bootstrap)
        _bootstrap._bootstrap_external = _bootstrap_external
    else:
        _bootstrap_external.__name__ = 'importlib._bootstrap_external'
        _bootstrap_external.__package__ = 'importlib'
        try:
            _bootstrap_external.__file__ = __file__.replace('__init__.py', '_bootstrap_external.py')
        except NameError:
            pass
        else:
            sys.modules['importlib._bootstrap_external'] = _bootstrap_external
        _pack_uint32 = _bootstrap_external._pack_uint32
        _unpack_uint32 = _bootstrap_external._unpack_uint32
        import types, warnings
        from ._bootstrap import __import__

        def invalidate_caches():
            """Call the invalidate_caches() method on all meta path finders stored in
    sys.meta_path (where implemented)."""
            for finder in sys.meta_path:
                if hasattr(finder, 'invalidate_caches'):
                    finder.invalidate_caches()


        def find_loader(name, path=None):
            """Return the loader for the specified module.

    This is a backward-compatible wrapper around find_spec().

    This function is deprecated in favor of importlib.util.find_spec().

    """
            warnings.warn('Deprecated since Python 3.4. Use importlib.util.find_spec() instead.', DeprecationWarning,
              stacklevel=2)
            try:
                loader = sys.modules[name].__loader__
                if loader is None:
                    raise ValueError('{}.__loader__ is None'.format(name))
                else:
                    return loader
            except KeyError:
                pass
            except AttributeError:
                raise ValueError('{}.__loader__ is not set'.format(name)) from None
            else:
                spec = _bootstrap._find_spec(name, path)
                if spec is None:
                    return
                if spec.loader is None:
                    if spec.submodule_search_locations is None:
                        raise ImportError(('spec for {} missing loader'.format(name)), name=name)
                    raise ImportError('namespace packages do not have loaders', name=name)
                return spec.loader


        def import_module--- This code section failed: ---

 L. 117         0  LOAD_CONST               0
                2  STORE_FAST               'level'

 L. 118         4  LOAD_FAST                'name'
                6  LOAD_METHOD              startswith
                8  LOAD_STR                 '.'
               10  CALL_METHOD_1         1  ''
               12  POP_JUMP_IF_FALSE    66  'to 66'

 L. 119        14  LOAD_FAST                'package'
               16  POP_JUMP_IF_TRUE     36  'to 36'

 L. 120        18  LOAD_STR                 "the 'package' argument is required to perform a relative import for {!r}"
               20  STORE_FAST               'msg'

 L. 122        22  LOAD_GLOBAL              TypeError
               24  LOAD_FAST                'msg'
               26  LOAD_METHOD              format
               28  LOAD_FAST                'name'
               30  CALL_METHOD_1         1  ''
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            16  '16'

 L. 123        36  LOAD_FAST                'name'
               38  GET_ITER         
               40  FOR_ITER             66  'to 66'
               42  STORE_FAST               'character'

 L. 124        44  LOAD_FAST                'character'
               46  LOAD_STR                 '.'
               48  COMPARE_OP               !=
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L. 125        52  POP_TOP          
               54  JUMP_ABSOLUTE        66  'to 66'
             56_0  COME_FROM            50  '50'

 L. 126        56  LOAD_FAST                'level'
               58  LOAD_CONST               1
               60  INPLACE_ADD      
               62  STORE_FAST               'level'
               64  JUMP_BACK            40  'to 40'
             66_0  COME_FROM            12  '12'

 L. 127        66  LOAD_GLOBAL              _bootstrap
               68  LOAD_METHOD              _gcd_import
               70  LOAD_FAST                'name'
               72  LOAD_FAST                'level'
               74  LOAD_CONST               None
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  LOAD_FAST                'package'
               82  LOAD_FAST                'level'
               84  CALL_METHOD_3         3  ''
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 56_0


        _RELOADING = {}

        def reload--- This code section failed: ---

 L. 139         0  LOAD_FAST                'module'
                2  POP_JUMP_IF_FALSE    16  'to 16'
                4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'module'
                8  LOAD_GLOBAL              types
               10  LOAD_ATTR                ModuleType
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     24  'to 24'
             16_0  COME_FROM             2  '2'

 L. 140        16  LOAD_GLOBAL              TypeError
               18  LOAD_STR                 'reload() argument must be a module'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 141        24  SETUP_FINALLY        38  'to 38'

 L. 142        26  LOAD_FAST                'module'
               28  LOAD_ATTR                __spec__
               30  LOAD_ATTR                name
               32  STORE_FAST               'name'
               34  POP_BLOCK        
               36  JUMP_FORWARD         64  'to 64'
             38_0  COME_FROM_FINALLY    24  '24'

 L. 143        38  DUP_TOP          
               40  LOAD_GLOBAL              AttributeError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    62  'to 62'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 144        52  LOAD_FAST                'module'
               54  LOAD_ATTR                __name__
               56  STORE_FAST               'name'
               58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            44  '44'
               62  END_FINALLY      
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            36  '36'

 L. 146        64  LOAD_GLOBAL              sys
               66  LOAD_ATTR                modules
               68  LOAD_METHOD              get
               70  LOAD_FAST                'name'
               72  CALL_METHOD_1         1  ''
               74  LOAD_FAST                'module'
               76  COMPARE_OP               is-not
               78  POP_JUMP_IF_FALSE   102  'to 102'

 L. 147        80  LOAD_STR                 'module {} not in sys.modules'
               82  STORE_FAST               'msg'

 L. 148        84  LOAD_GLOBAL              ImportError
               86  LOAD_FAST                'msg'
               88  LOAD_METHOD              format
               90  LOAD_FAST                'name'
               92  CALL_METHOD_1         1  ''
               94  LOAD_FAST                'name'
               96  LOAD_CONST               ('name',)
               98  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            78  '78'

 L. 149       102  LOAD_FAST                'name'
              104  LOAD_GLOBAL              _RELOADING
              106  COMPARE_OP               in
              108  POP_JUMP_IF_FALSE   118  'to 118'

 L. 150       110  LOAD_GLOBAL              _RELOADING
              112  LOAD_FAST                'name'
              114  BINARY_SUBSCR    
              116  RETURN_VALUE     
            118_0  COME_FROM           108  '108'

 L. 151       118  LOAD_FAST                'module'
              120  LOAD_GLOBAL              _RELOADING
              122  LOAD_FAST                'name'
              124  STORE_SUBSCR     

 L. 152       126  SETUP_FINALLY       296  'to 296'

 L. 153       128  LOAD_FAST                'name'
              130  LOAD_METHOD              rpartition
              132  LOAD_STR                 '.'
              134  CALL_METHOD_1         1  ''
              136  LOAD_CONST               0
              138  BINARY_SUBSCR    
              140  STORE_FAST               'parent_name'

 L. 154       142  LOAD_FAST                'parent_name'
              144  POP_JUMP_IF_FALSE   214  'to 214'

 L. 155       146  SETUP_FINALLY       162  'to 162'

 L. 156       148  LOAD_GLOBAL              sys
              150  LOAD_ATTR                modules
              152  LOAD_FAST                'parent_name'
              154  BINARY_SUBSCR    
              156  STORE_FAST               'parent'
              158  POP_BLOCK        
              160  JUMP_FORWARD        206  'to 206'
            162_0  COME_FROM_FINALLY   146  '146'

 L. 157       162  DUP_TOP          
              164  LOAD_GLOBAL              KeyError
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   204  'to 204'
              170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L. 158       176  LOAD_STR                 'parent {!r} not in sys.modules'
              178  STORE_FAST               'msg'

 L. 159       180  LOAD_GLOBAL              ImportError
              182  LOAD_FAST                'msg'
              184  LOAD_METHOD              format
              186  LOAD_FAST                'parent_name'
              188  CALL_METHOD_1         1  ''

 L. 160       190  LOAD_FAST                'parent_name'

 L. 159       192  LOAD_CONST               ('name',)
              194  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 160       196  LOAD_CONST               None

 L. 159       198  RAISE_VARARGS_2       2  'exception instance with __cause__'
              200  POP_EXCEPT       
              202  JUMP_ABSOLUTE       218  'to 218'
            204_0  COME_FROM           168  '168'
              204  END_FINALLY      
            206_0  COME_FROM           160  '160'

 L. 162       206  LOAD_FAST                'parent'
              208  LOAD_ATTR                __path__
              210  STORE_FAST               'pkgpath'
              212  JUMP_FORWARD        218  'to 218'
            214_0  COME_FROM           144  '144'

 L. 164       214  LOAD_CONST               None
              216  STORE_FAST               'pkgpath'
            218_0  COME_FROM           212  '212'

 L. 165       218  LOAD_FAST                'module'
              220  STORE_FAST               'target'

 L. 166       222  LOAD_GLOBAL              _bootstrap
              224  LOAD_METHOD              _find_spec
              226  LOAD_FAST                'name'
              228  LOAD_FAST                'pkgpath'
              230  LOAD_FAST                'target'
              232  CALL_METHOD_3         3  ''
              234  DUP_TOP          
              236  STORE_FAST               'spec'
              238  LOAD_FAST                'module'
              240  STORE_ATTR               __spec__

 L. 167       242  LOAD_FAST                'spec'
              244  LOAD_CONST               None
              246  COMPARE_OP               is
          248_250  POP_JUMP_IF_FALSE   270  'to 270'

 L. 168       252  LOAD_GLOBAL              ModuleNotFoundError
              254  LOAD_STR                 'spec not found for the module '
              256  LOAD_FAST                'name'
              258  FORMAT_VALUE          2  '!r'
              260  BUILD_STRING_2        2 
              262  LOAD_FAST                'name'
              264  LOAD_CONST               ('name',)
              266  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              268  RAISE_VARARGS_1       1  'exception instance'
            270_0  COME_FROM           248  '248'

 L. 169       270  LOAD_GLOBAL              _bootstrap
              272  LOAD_METHOD              _exec
              274  LOAD_FAST                'spec'
              276  LOAD_FAST                'module'
              278  CALL_METHOD_2         2  ''
              280  POP_TOP          

 L. 171       282  LOAD_GLOBAL              sys
              284  LOAD_ATTR                modules
              286  LOAD_FAST                'name'
              288  BINARY_SUBSCR    
              290  POP_BLOCK        
              292  CALL_FINALLY        296  'to 296'
              294  RETURN_VALUE     
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM_FINALLY   126  '126'

 L. 173       296  SETUP_FINALLY       308  'to 308'

 L. 174       298  LOAD_GLOBAL              _RELOADING
              300  LOAD_FAST                'name'
              302  DELETE_SUBSCR    
              304  POP_BLOCK        
              306  JUMP_FORWARD        330  'to 330'
            308_0  COME_FROM_FINALLY   296  '296'

 L. 175       308  DUP_TOP          
              310  LOAD_GLOBAL              KeyError
              312  COMPARE_OP               exception-match
          314_316  POP_JUMP_IF_FALSE   328  'to 328'
              318  POP_TOP          
              320  POP_TOP          
              322  POP_TOP          

 L. 176       324  POP_EXCEPT       
              326  JUMP_FORWARD        330  'to 330'
            328_0  COME_FROM           314  '314'
              328  END_FINALLY      
            330_0  COME_FROM           326  '326'
            330_1  COME_FROM           306  '306'
              330  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 292