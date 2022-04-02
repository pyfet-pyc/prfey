# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cffi\vengine_cpy.py
import sys, imp
from . import model
from .error import VerificationError

class VCPythonEngine(object):
    _class_key = 'x'
    _gen_python_module = True

    def __init__(self, verifier):
        self.verifier = verifier
        self.ffi = verifier.ffi
        self._struct_pending_verification = {}
        self._types_of_builtin_functions = {}

    def patch_extension_kwds(self, kwds):
        pass

    def find_module--- This code section failed: ---

 L.  23         0  SETUP_FINALLY        24  'to 24'

 L.  24         2  LOAD_GLOBAL              imp
                4  LOAD_METHOD              find_module
                6  LOAD_FAST                'module_name'
                8  LOAD_FAST                'path'
               10  CALL_METHOD_2         2  ''
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'f'
               16  STORE_FAST               'filename'
               18  STORE_FAST               'descr'
               20  POP_BLOCK        
               22  JUMP_FORWARD         44  'to 44'
             24_0  COME_FROM_FINALLY     0  '0'

 L.  25        24  DUP_TOP          
               26  LOAD_GLOBAL              ImportError
               28  <121>                42  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  26        36  POP_EXCEPT       
               38  LOAD_CONST               None
               40  RETURN_VALUE     
               42  <48>             
             44_0  COME_FROM            22  '22'

 L.  27        44  LOAD_FAST                'f'
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE    60  'to 60'

 L.  28        52  LOAD_FAST                'f'
               54  LOAD_METHOD              close
               56  CALL_METHOD_0         0  ''
               58  POP_TOP          
             60_0  COME_FROM            50  '50'

 L.  32        60  LOAD_FAST                'descr'
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  LOAD_FAST                'so_suffixes'
               68  <118>                 1  ''
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L.  33        72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'

 L.  34        76  LOAD_FAST                'filename'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 28

    def collect_types(self):
        self._typesdict = {}
        self._generate('collecttype')

    def _prnt(self, what=''):
        self._f.write(what + '\n')

    def _gettypenum(self, type):
        return self._typesdict[type]

    def _do_collect_type--- This code section failed: ---

 L.  48         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                PrimitiveType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    22  'to 22'

 L.  49        12  LOAD_FAST                'tp'
               14  LOAD_ATTR                name
               16  LOAD_STR                 'long double'
               18  COMPARE_OP               ==

 L.  48        20  POP_JUMP_IF_FALSE    52  'to 52'
             22_0  COME_FROM            10  '10'

 L.  50        22  LOAD_FAST                'tp'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _typesdict
               28  <118>                 1  ''

 L.  48        30  POP_JUMP_IF_FALSE    52  'to 52'

 L.  51        32  LOAD_GLOBAL              len
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _typesdict
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'num'

 L.  52        42  LOAD_FAST                'num'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _typesdict
               48  LOAD_FAST                'tp'
               50  STORE_SUBSCR     
             52_0  COME_FROM            30  '30'
             52_1  COME_FROM            20  '20'

Parse error at or near `<118>' instruction at offset 28

    def write_source_to_f(self):
        self.collect_types
        self._chained_list_constants = [
         '((void)lib,0)', '((void)lib,0)']
        prnt = self._prnt
        prnt(cffimod_header)
        prnt()
        prnt(self.verifier.preamble)
        prnt()
        self._generate('decl')
        self._generate_setup_custom
        prnt()
        prnt('static PyMethodDef _cffi_methods[] = {')
        self._generate('method')
        prnt('  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},')
        prnt('  {NULL, NULL, 0, NULL}    /* Sentinel */')
        prnt('};')
        prnt()
        modname = self.verifier.get_module_name
        constants = self._chained_list_constants[False]
        prnt('#if PY_MAJOR_VERSION >= 3')
        prnt()
        prnt('static struct PyModuleDef _cffi_module_def = {')
        prnt('  PyModuleDef_HEAD_INIT,')
        prnt('  "%s",' % modname)
        prnt('  NULL,')
        prnt('  -1,')
        prnt('  _cffi_methods,')
        prnt('  NULL, NULL, NULL, NULL')
        prnt('};')
        prnt()
        prnt('PyMODINIT_FUNC')
        prnt('PyInit_%s(void)' % modname)
        prnt('{')
        prnt('  PyObject *lib;')
        prnt('  lib = PyModule_Create(&_cffi_module_def);')
        prnt('  if (lib == NULL)')
        prnt('    return NULL;')
        prnt('  if (%s < 0 || _cffi_init() < 0) {' % (constants,))
        prnt('    Py_DECREF(lib);')
        prnt('    return NULL;')
        prnt('  }')
        prnt('  return lib;')
        prnt('}')
        prnt()
        prnt('#else')
        prnt()
        prnt('PyMODINIT_FUNC')
        prnt('init%s(void)' % modname)
        prnt('{')
        prnt('  PyObject *lib;')
        prnt('  lib = Py_InitModule("%s", _cffi_methods);' % modname)
        prnt('  if (lib == NULL)')
        prnt('    return;')
        prnt('  if (%s < 0 || _cffi_init() < 0)' % (constants,))
        prnt('    return;')
        prnt('  return;')
        prnt('}')
        prnt()
        prnt('#endif')

    def load_library--- This code section failed: ---

 L. 148         0  LOAD_GLOBAL              imp
                2  LOAD_METHOD              acquire_lock
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 149         8  SETUP_FINALLY       204  'to 204'

 L. 150        10  LOAD_GLOBAL              hasattr
               12  LOAD_GLOBAL              sys
               14  LOAD_STR                 'getdlopenflags'
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 151        20  LOAD_GLOBAL              sys
               22  LOAD_METHOD              getdlopenflags
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'previous_flags'
             28_0  COME_FROM            18  '18'

 L. 152        28  SETUP_FINALLY       170  'to 170'
               30  SETUP_FINALLY        86  'to 86'

 L. 153        32  LOAD_GLOBAL              hasattr
               34  LOAD_GLOBAL              sys
               36  LOAD_STR                 'setdlopenflags'
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    60  'to 60'
               42  LOAD_FAST                'flags'
               44  LOAD_CONST               None
               46  <117>                 1  ''
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L. 154        50  LOAD_GLOBAL              sys
               52  LOAD_METHOD              setdlopenflags
               54  LOAD_FAST                'flags'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
             60_0  COME_FROM            48  '48'
             60_1  COME_FROM            40  '40'

 L. 155        60  LOAD_GLOBAL              imp
               62  LOAD_METHOD              load_dynamic
               64  LOAD_DEREF               'self'
               66  LOAD_ATTR                verifier
               68  LOAD_METHOD              get_module_name
               70  CALL_METHOD_0         0  ''

 L. 156        72  LOAD_DEREF               'self'
               74  LOAD_ATTR                verifier
               76  LOAD_ATTR                modulefilename

 L. 155        78  CALL_METHOD_2         2  ''
               80  STORE_DEREF              'module'
               82  POP_BLOCK        
               84  JUMP_FORWARD        146  'to 146'
             86_0  COME_FROM_FINALLY    30  '30'

 L. 157        86  DUP_TOP          
               88  LOAD_GLOBAL              ImportError
               90  <121>               144  ''
               92  POP_TOP          
               94  STORE_FAST               'e'
               96  POP_TOP          
               98  SETUP_FINALLY       136  'to 136'

 L. 158       100  LOAD_STR                 'importing %r: %s'
              102  LOAD_DEREF               'self'
              104  LOAD_ATTR                verifier
              106  LOAD_ATTR                modulefilename
              108  LOAD_FAST                'e'
              110  BUILD_TUPLE_2         2 
              112  BINARY_MODULO    
              114  STORE_FAST               'error'

 L. 159       116  LOAD_GLOBAL              VerificationError
              118  LOAD_FAST                'error'
              120  CALL_FUNCTION_1       1  ''
              122  RAISE_VARARGS_1       1  'exception instance'
              124  POP_BLOCK        
              126  POP_EXCEPT       
              128  LOAD_CONST               None
              130  STORE_FAST               'e'
              132  DELETE_FAST              'e'
              134  JUMP_FORWARD        146  'to 146'
            136_0  COME_FROM_FINALLY    98  '98'
              136  LOAD_CONST               None
              138  STORE_FAST               'e'
              140  DELETE_FAST              'e'
              142  <48>             
              144  <48>             
            146_0  COME_FROM           134  '134'
            146_1  COME_FROM            84  '84'
              146  POP_BLOCK        

 L. 161       148  LOAD_GLOBAL              hasattr
              150  LOAD_GLOBAL              sys
              152  LOAD_STR                 'setdlopenflags'
              154  CALL_FUNCTION_2       2  ''
              156  POP_JUMP_IF_FALSE   192  'to 192'

 L. 162       158  LOAD_GLOBAL              sys
              160  LOAD_METHOD              setdlopenflags
              162  LOAD_FAST                'previous_flags'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
              168  JUMP_FORWARD        192  'to 192'
            170_0  COME_FROM_FINALLY    28  '28'

 L. 161       170  LOAD_GLOBAL              hasattr
              172  LOAD_GLOBAL              sys
              174  LOAD_STR                 'setdlopenflags'
              176  CALL_FUNCTION_2       2  ''
              178  POP_JUMP_IF_FALSE   190  'to 190'

 L. 162       180  LOAD_GLOBAL              sys
              182  LOAD_METHOD              setdlopenflags
              184  LOAD_FAST                'previous_flags'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
            190_0  COME_FROM           178  '178'
              190  <48>             
            192_0  COME_FROM           168  '168'
            192_1  COME_FROM           156  '156'
              192  POP_BLOCK        

 L. 164       194  LOAD_GLOBAL              imp
              196  LOAD_METHOD              release_lock
              198  CALL_METHOD_0         0  ''
              200  POP_TOP          
              202  JUMP_FORWARD        214  'to 214'
            204_0  COME_FROM_FINALLY     8  '8'
              204  LOAD_GLOBAL              imp
              206  LOAD_METHOD              release_lock
              208  CALL_METHOD_0         0  ''
              210  POP_TOP          
              212  <48>             
            214_0  COME_FROM           202  '202'

 L. 168       214  LOAD_DEREF               'self'
              216  LOAD_METHOD              _load
              218  LOAD_DEREF               'module'
              220  LOAD_STR                 'loading'
              222  CALL_METHOD_2         2  ''
              224  POP_TOP          

 L. 172       226  LOAD_GLOBAL              dict
              228  LOAD_LISTCOMP            '<code_object <listcomp>>'
              230  LOAD_STR                 'VCPythonEngine.load_library.<locals>.<listcomp>'
              232  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 173       234  LOAD_DEREF               'self'
              236  LOAD_ATTR                _typesdict
              238  LOAD_METHOD              items
              240  CALL_METHOD_0         0  ''

 L. 172       242  GET_ITER         
              244  CALL_FUNCTION_1       1  ''
              246  CALL_FUNCTION_1       1  ''
              248  STORE_DEREF              'revmapping'

 L. 174       250  LOAD_CLOSURE             'revmapping'
              252  BUILD_TUPLE_1         1 
              254  LOAD_LISTCOMP            '<code_object <listcomp>>'
              256  LOAD_STR                 'VCPythonEngine.load_library.<locals>.<listcomp>'
              258  MAKE_FUNCTION_8          'closure'
              260  LOAD_GLOBAL              range
              262  LOAD_GLOBAL              len
              264  LOAD_DEREF               'revmapping'
              266  CALL_FUNCTION_1       1  ''
              268  CALL_FUNCTION_1       1  ''
              270  GET_ITER         
              272  CALL_FUNCTION_1       1  ''
              274  STORE_FAST               'lst'

 L. 175       276  LOAD_GLOBAL              list
              278  LOAD_GLOBAL              map
              280  LOAD_DEREF               'self'
              282  LOAD_ATTR                ffi
              284  LOAD_ATTR                _get_cached_btype
              286  LOAD_FAST                'lst'
              288  CALL_FUNCTION_2       2  ''
              290  CALL_FUNCTION_1       1  ''
              292  STORE_FAST               'lst'

 L. 182       294  LOAD_BUILD_CLASS 
              296  LOAD_CLOSURE             'FFILibrary'
              298  LOAD_CLOSURE             'module'
              300  LOAD_CLOSURE             'self'
              302  BUILD_TUPLE_3         3 
              304  LOAD_CODE                <code_object FFILibrary>
              306  LOAD_STR                 'FFILibrary'
              308  MAKE_FUNCTION_8          'closure'
              310  LOAD_STR                 'FFILibrary'
              312  LOAD_GLOBAL              object
              314  CALL_FUNCTION_3       3  ''
              316  STORE_DEREF              'FFILibrary'

 L. 188       318  LOAD_DEREF               'FFILibrary'
              320  CALL_FUNCTION_0       0  ''
              322  STORE_FAST               'library'

 L. 189       324  LOAD_DEREF               'module'
              326  LOAD_METHOD              _cffi_setup
              328  LOAD_FAST                'lst'
              330  LOAD_GLOBAL              VerificationError
              332  LOAD_FAST                'library'
              334  CALL_METHOD_3         3  ''
          336_338  POP_JUMP_IF_FALSE   368  'to 368'

 L. 190       340  LOAD_CONST               0
              342  LOAD_CONST               None
              344  IMPORT_NAME              warnings
              346  STORE_FAST               'warnings'

 L. 191       348  LOAD_FAST                'warnings'
              350  LOAD_METHOD              warn
              352  LOAD_STR                 'reimporting %r might overwrite older definitions'

 L. 192       354  LOAD_DEREF               'self'
              356  LOAD_ATTR                verifier
              358  LOAD_METHOD              get_module_name
              360  CALL_METHOD_0         0  ''

 L. 191       362  BINARY_MODULO    
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          
            368_0  COME_FROM           336  '336'

 L. 198       368  LOAD_DEREF               'self'
              370  LOAD_ATTR                _load
              372  LOAD_DEREF               'module'
              374  LOAD_STR                 'loaded'
              376  LOAD_FAST                'library'
              378  LOAD_CONST               ('library',)
              380  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              382  POP_TOP          

 L. 199       384  LOAD_DEREF               'self'
              386  LOAD_ATTR                ffi
              388  LOAD_DEREF               'module'
              390  STORE_ATTR               _cffi_original_ffi

 L. 200       392  LOAD_DEREF               'self'
              394  LOAD_ATTR                _types_of_builtin_functions
              396  LOAD_DEREF               'module'
              398  STORE_ATTR               _cffi_types_of_builtin_funcs

 L. 201       400  LOAD_FAST                'library'
              402  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 46

    def _get_declarations(self):
        lst = [(key, tp) for key, (tp, qual) in self.ffi._parser._declarations.items]
        lst.sort
        return lst

    def _generate--- This code section failed: ---

 L. 210         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_declarations
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
                8  FOR_ITER            154  'to 154'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'name'
               14  STORE_FAST               'tp'

 L. 211        16  LOAD_FAST                'name'
               18  LOAD_METHOD              split
               20  LOAD_STR                 ' '
               22  LOAD_CONST               1
               24  CALL_METHOD_2         2  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'kind'
               30  STORE_FAST               'realname'

 L. 212        32  SETUP_FINALLY        56  'to 56'

 L. 213        34  LOAD_GLOBAL              getattr
               36  LOAD_FAST                'self'
               38  LOAD_STR                 '_generate_cpy_%s_%s'
               40  LOAD_FAST                'kind'

 L. 214        42  LOAD_FAST                'step_name'

 L. 213        44  BUILD_TUPLE_2         2 
               46  BINARY_MODULO    
               48  CALL_FUNCTION_2       2  ''
               50  STORE_FAST               'method'
               52  POP_BLOCK        
               54  JUMP_FORWARD         86  'to 86'
             56_0  COME_FROM_FINALLY    32  '32'

 L. 215        56  DUP_TOP          
               58  LOAD_GLOBAL              AttributeError
               60  <121>                84  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 216        68  LOAD_GLOBAL              VerificationError

 L. 217        70  LOAD_STR                 'not implemented in verify(): %r'
               72  LOAD_FAST                'name'
               74  BINARY_MODULO    

 L. 216        76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            54  '54'

 L. 218        86  SETUP_FINALLY       102  'to 102'

 L. 219        88  LOAD_FAST                'method'
               90  LOAD_FAST                'tp'
               92  LOAD_FAST                'realname'
               94  CALL_FUNCTION_2       2  ''
               96  POP_TOP          
               98  POP_BLOCK        
              100  JUMP_BACK             8  'to 8'
            102_0  COME_FROM_FINALLY    86  '86'

 L. 220       102  DUP_TOP          
              104  LOAD_GLOBAL              Exception
              106  <121>               150  ''
              108  POP_TOP          
              110  STORE_FAST               'e'
              112  POP_TOP          
              114  SETUP_FINALLY       142  'to 142'

 L. 221       116  LOAD_GLOBAL              model
              118  LOAD_METHOD              attach_exception_info
              120  LOAD_FAST                'e'
              122  LOAD_FAST                'name'
              124  CALL_METHOD_2         2  ''
              126  POP_TOP          

 L. 222       128  RAISE_VARARGS_0       0  'reraise'
              130  POP_BLOCK        
              132  POP_EXCEPT       
              134  LOAD_CONST               None
              136  STORE_FAST               'e'
              138  DELETE_FAST              'e'
              140  JUMP_BACK             8  'to 8'
            142_0  COME_FROM_FINALLY   114  '114'
              142  LOAD_CONST               None
              144  STORE_FAST               'e'
              146  DELETE_FAST              'e'
              148  <48>             
              150  <48>             
              152  JUMP_BACK             8  'to 8'

Parse error at or near `<121>' instruction at offset 60

    def _load--- This code section failed: ---

 L. 225         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_declarations
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
                8  FOR_ITER            128  'to 128'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'name'
               14  STORE_FAST               'tp'

 L. 226        16  LOAD_FAST                'name'
               18  LOAD_METHOD              split
               20  LOAD_STR                 ' '
               22  LOAD_CONST               1
               24  CALL_METHOD_2         2  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'kind'
               30  STORE_FAST               'realname'

 L. 227        32  LOAD_GLOBAL              getattr
               34  LOAD_FAST                'self'
               36  LOAD_STR                 '_%s_cpy_%s'
               38  LOAD_FAST                'step_name'
               40  LOAD_FAST                'kind'
               42  BUILD_TUPLE_2         2 
               44  BINARY_MODULO    
               46  CALL_FUNCTION_2       2  ''
               48  STORE_FAST               'method'

 L. 228        50  SETUP_FINALLY        76  'to 76'

 L. 229        52  LOAD_FAST                'method'
               54  LOAD_FAST                'tp'
               56  LOAD_FAST                'realname'
               58  LOAD_FAST                'module'
               60  BUILD_TUPLE_3         3 
               62  BUILD_MAP_0           0 
               64  LOAD_FAST                'kwds'
               66  <164>                 1  ''
               68  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               70  POP_TOP          
               72  POP_BLOCK        
               74  JUMP_BACK             8  'to 8'
             76_0  COME_FROM_FINALLY    50  '50'

 L. 230        76  DUP_TOP          
               78  LOAD_GLOBAL              Exception
               80  <121>               124  ''
               82  POP_TOP          
               84  STORE_FAST               'e'
               86  POP_TOP          
               88  SETUP_FINALLY       116  'to 116'

 L. 231        90  LOAD_GLOBAL              model
               92  LOAD_METHOD              attach_exception_info
               94  LOAD_FAST                'e'
               96  LOAD_FAST                'name'
               98  CALL_METHOD_2         2  ''
              100  POP_TOP          

 L. 232       102  RAISE_VARARGS_0       0  'reraise'
              104  POP_BLOCK        
              106  POP_EXCEPT       
              108  LOAD_CONST               None
              110  STORE_FAST               'e'
              112  DELETE_FAST              'e'
              114  JUMP_BACK             8  'to 8'
            116_0  COME_FROM_FINALLY    88  '88'
              116  LOAD_CONST               None
              118  STORE_FAST               'e'
              120  DELETE_FAST              'e'
              122  <48>             
              124  <48>             
              126  JUMP_BACK             8  'to 8'

Parse error at or near `<164>' instruction at offset 66

    def _generate_nothing(self, tp, name):
        pass

    def _loaded_noop(self, tp, name, module, **kwds):
        pass

    def _convert_funcarg_to_c(self, tp, fromvar, tovar, errcode):
        extraarg = ''
        if isinstancetpmodel.PrimitiveType:
            if tp.is_integer_type and tp.name != '_Bool':
                converter = '_cffi_to_c_int'
                extraarg = ', %s' % tp.name
            else:
                converter = '(%s)_cffi_to_c_%s' % (tp.get_c_name(''),
                 tp.name.replace' ''_')
            errvalue = '-1'
        else:
            if isinstancetpmodel.PointerType:
                self._convert_funcarg_to_c_ptr_or_array(tp, fromvar, tovar, errcode)
                return None
            elif isinstancetp(model.StructOrUnion, model.EnumType):
                self._prnt('  if (_cffi_to_c((char *)&%s, _cffi_type(%d), %s) < 0)' % (
                 tovar, self._gettypenum(tp), fromvar))
                self._prnt('    %s;' % errcode)
                return
                if isinstancetpmodel.FunctionPtrType:
                    converter = '(%s)_cffi_to_c_pointer' % tp.get_c_name('')
                    extraarg = ', _cffi_type(%d)' % self._gettypenum(tp)
                    errvalue = 'NULL'
            else:
                raise NotImplementedError(tp)
        self._prnt('  %s = %s(%s%s);' % (tovar, converter, fromvar, extraarg))
        self._prnt('  if (%s == (%s)%s && PyErr_Occurred())' % (
         tovar, tp.get_c_name(''), errvalue))
        self._prnt('    %s;' % errcode)

    def _extra_local_variables(self, tp, localvars, freelines):
        if isinstancetpmodel.PointerType:
            localvars.add('Py_ssize_t datasize')
            localvars.add('struct _cffi_freeme_s *large_args_free = NULL')
            freelines.add('if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);')

    def _convert_funcarg_to_c_ptr_or_array(self, tp, fromvar, tovar, errcode):
        self._prnt('  datasize = _cffi_prepare_pointer_call_argument(')
        self._prnt('      _cffi_type(%d), %s, (char **)&%s);' % (
         self._gettypenum(tp), fromvar, tovar))
        self._prnt('  if (datasize != 0) {')
        self._prnt('    %s = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;' % (
         tovar,))
        self._prnt('    if (_cffi_convert_array_argument(_cffi_type(%d), %s, (char **)&%s,' % (
         self._gettypenum(tp), fromvar, tovar))
        self._prnt('            datasize, &large_args_free) < 0)')
        self._prnt('      %s;' % errcode)
        self._prnt('  }')

    def _convert_expr_from_c--- This code section failed: ---

 L. 299         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                PrimitiveType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    96  'to 96'

 L. 300        12  LOAD_FAST                'tp'
               14  LOAD_METHOD              is_integer_type
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_FALSE    44  'to 44'
               20  LOAD_FAST                'tp'
               22  LOAD_ATTR                name
               24  LOAD_STR                 '_Bool'
               26  COMPARE_OP               !=
               28  POP_JUMP_IF_FALSE    44  'to 44'

 L. 301        30  LOAD_STR                 '_cffi_from_c_int(%s, %s)'
               32  LOAD_FAST                'var'
               34  LOAD_FAST                'tp'
               36  LOAD_ATTR                name
               38  BUILD_TUPLE_2         2 
               40  BINARY_MODULO    
               42  RETURN_VALUE     
             44_0  COME_FROM            28  '28'
             44_1  COME_FROM            18  '18'

 L. 302        44  LOAD_FAST                'tp'
               46  LOAD_ATTR                name
               48  LOAD_STR                 'long double'
               50  COMPARE_OP               !=
               52  POP_JUMP_IF_FALSE    76  'to 76'

 L. 303        54  LOAD_STR                 '_cffi_from_c_%s(%s)'
               56  LOAD_FAST                'tp'
               58  LOAD_ATTR                name
               60  LOAD_METHOD              replace
               62  LOAD_STR                 ' '
               64  LOAD_STR                 '_'
               66  CALL_METHOD_2         2  ''
               68  LOAD_FAST                'var'
               70  BUILD_TUPLE_2         2 
               72  BINARY_MODULO    
               74  RETURN_VALUE     
             76_0  COME_FROM            52  '52'

 L. 305        76  LOAD_STR                 '_cffi_from_c_deref((char *)&%s, _cffi_type(%d))'

 L. 306        78  LOAD_FAST                'var'
               80  LOAD_FAST                'self'
               82  LOAD_METHOD              _gettypenum
               84  LOAD_FAST                'tp'
               86  CALL_METHOD_1         1  ''

 L. 305        88  BUILD_TUPLE_2         2 
               90  BINARY_MODULO    
               92  RETURN_VALUE     
               94  JUMP_FORWARD        270  'to 270'
             96_0  COME_FROM            10  '10'

 L. 307        96  LOAD_GLOBAL              isinstance
               98  LOAD_FAST                'tp'
              100  LOAD_GLOBAL              model
              102  LOAD_ATTR                PointerType
              104  LOAD_GLOBAL              model
              106  LOAD_ATTR                FunctionPtrType
              108  BUILD_TUPLE_2         2 
              110  CALL_FUNCTION_2       2  ''
              112  POP_JUMP_IF_FALSE   132  'to 132'

 L. 308       114  LOAD_STR                 '_cffi_from_c_pointer((char *)%s, _cffi_type(%d))'

 L. 309       116  LOAD_FAST                'var'
              118  LOAD_FAST                'self'
              120  LOAD_METHOD              _gettypenum
              122  LOAD_FAST                'tp'
              124  CALL_METHOD_1         1  ''

 L. 308       126  BUILD_TUPLE_2         2 
              128  BINARY_MODULO    
              130  RETURN_VALUE     
            132_0  COME_FROM           112  '112'

 L. 310       132  LOAD_GLOBAL              isinstance
              134  LOAD_FAST                'tp'
              136  LOAD_GLOBAL              model
              138  LOAD_ATTR                ArrayType
              140  CALL_FUNCTION_2       2  ''
              142  POP_JUMP_IF_FALSE   170  'to 170'

 L. 311       144  LOAD_STR                 '_cffi_from_c_pointer((char *)%s, _cffi_type(%d))'

 L. 312       146  LOAD_FAST                'var'
              148  LOAD_FAST                'self'
              150  LOAD_METHOD              _gettypenum
              152  LOAD_GLOBAL              model
              154  LOAD_METHOD              PointerType
              156  LOAD_FAST                'tp'
              158  LOAD_ATTR                item
              160  CALL_METHOD_1         1  ''
              162  CALL_METHOD_1         1  ''

 L. 311       164  BUILD_TUPLE_2         2 
              166  BINARY_MODULO    
              168  RETURN_VALUE     
            170_0  COME_FROM           142  '142'

 L. 313       170  LOAD_GLOBAL              isinstance
              172  LOAD_FAST                'tp'
              174  LOAD_GLOBAL              model
              176  LOAD_ATTR                StructOrUnion
              178  CALL_FUNCTION_2       2  ''
              180  POP_JUMP_IF_FALSE   230  'to 230'

 L. 314       182  LOAD_FAST                'tp'
              184  LOAD_ATTR                fldnames
              186  LOAD_CONST               None
              188  <117>                 0  ''
              190  POP_JUMP_IF_FALSE   212  'to 212'

 L. 315       192  LOAD_GLOBAL              TypeError
              194  LOAD_STR                 "'%s' is used as %s, but is opaque"

 L. 316       196  LOAD_FAST                'tp'
              198  LOAD_METHOD              _get_c_name
              200  CALL_METHOD_0         0  ''
              202  LOAD_FAST                'context'

 L. 315       204  BUILD_TUPLE_2         2 
              206  BINARY_MODULO    
              208  CALL_FUNCTION_1       1  ''
              210  RAISE_VARARGS_1       1  'exception instance'
            212_0  COME_FROM           190  '190'

 L. 317       212  LOAD_STR                 '_cffi_from_c_struct((char *)&%s, _cffi_type(%d))'

 L. 318       214  LOAD_FAST                'var'
              216  LOAD_FAST                'self'
              218  LOAD_METHOD              _gettypenum
              220  LOAD_FAST                'tp'
              222  CALL_METHOD_1         1  ''

 L. 317       224  BUILD_TUPLE_2         2 
              226  BINARY_MODULO    
              228  RETURN_VALUE     
            230_0  COME_FROM           180  '180'

 L. 319       230  LOAD_GLOBAL              isinstance
              232  LOAD_FAST                'tp'
              234  LOAD_GLOBAL              model
              236  LOAD_ATTR                EnumType
              238  CALL_FUNCTION_2       2  ''
          240_242  POP_JUMP_IF_FALSE   262  'to 262'

 L. 320       244  LOAD_STR                 '_cffi_from_c_deref((char *)&%s, _cffi_type(%d))'

 L. 321       246  LOAD_FAST                'var'
              248  LOAD_FAST                'self'
              250  LOAD_METHOD              _gettypenum
              252  LOAD_FAST                'tp'
              254  CALL_METHOD_1         1  ''

 L. 320       256  BUILD_TUPLE_2         2 
              258  BINARY_MODULO    
              260  RETURN_VALUE     
            262_0  COME_FROM           240  '240'

 L. 323       262  LOAD_GLOBAL              NotImplementedError
              264  LOAD_FAST                'tp'
              266  CALL_FUNCTION_1       1  ''
              268  RAISE_VARARGS_1       1  'exception instance'
            270_0  COME_FROM            94  '94'

Parse error at or near `<117>' instruction at offset 188

    _generate_cpy_typedef_collecttype = _generate_nothing
    _generate_cpy_typedef_decl = _generate_nothing
    _generate_cpy_typedef_method = _generate_nothing
    _loading_cpy_typedef = _loaded_noop
    _loaded_cpy_typedef = _loaded_noop

    def _generate_cpy_function_collecttype--- This code section failed: ---

 L. 338         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                FunctionPtrType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 339        16  LOAD_FAST                'tp'
               18  LOAD_ATTR                ellipsis
               20  POP_JUMP_IF_FALSE    34  'to 34'

 L. 340        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _do_collect_type
               26  LOAD_FAST                'tp'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          
               32  JUMP_FORWARD         68  'to 68'
             34_0  COME_FROM            20  '20'

 L. 344        34  LOAD_FAST                'tp'
               36  LOAD_ATTR                args
               38  GET_ITER         
               40  FOR_ITER             56  'to 56'
               42  STORE_FAST               'type'

 L. 345        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _do_collect_type
               48  LOAD_FAST                'type'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
               54  JUMP_BACK            40  'to 40'

 L. 346        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _do_collect_type
               60  LOAD_FAST                'tp'
               62  LOAD_ATTR                result
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
             68_0  COME_FROM            32  '32'

Parse error at or near `None' instruction at offset -1

    def _generate_cpy_function_decl--- This code section failed: ---

 L. 349         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                FunctionPtrType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 350        16  LOAD_FAST                'tp'
               18  LOAD_ATTR                ellipsis
               20  POP_JUMP_IF_FALSE    40  'to 40'

 L. 354        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _generate_cpy_const
               26  LOAD_CONST               False
               28  LOAD_FAST                'name'
               30  LOAD_FAST                'tp'
               32  CALL_METHOD_3         3  ''
               34  POP_TOP          

 L. 355        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            20  '20'

 L. 356        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _prnt
               44  STORE_FAST               'prnt'

 L. 357        46  LOAD_GLOBAL              len
               48  LOAD_FAST                'tp'
               50  LOAD_ATTR                args
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'numargs'

 L. 358        56  LOAD_FAST                'numargs'
               58  LOAD_CONST               0
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    70  'to 70'

 L. 359        64  LOAD_STR                 'noarg'
               66  STORE_FAST               'argname'
               68  JUMP_FORWARD         88  'to 88'
             70_0  COME_FROM            62  '62'

 L. 360        70  LOAD_FAST                'numargs'
               72  LOAD_CONST               1
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    84  'to 84'

 L. 361        78  LOAD_STR                 'arg0'
               80  STORE_FAST               'argname'
               82  JUMP_FORWARD         88  'to 88'
             84_0  COME_FROM            76  '76'

 L. 363        84  LOAD_STR                 'args'
               86  STORE_FAST               'argname'
             88_0  COME_FROM            82  '82'
             88_1  COME_FROM            68  '68'

 L. 364        88  LOAD_FAST                'prnt'
               90  LOAD_STR                 'static PyObject *'
               92  CALL_FUNCTION_1       1  ''
               94  POP_TOP          

 L. 365        96  LOAD_FAST                'prnt'
               98  LOAD_STR                 '_cffi_f_%s(PyObject *self, PyObject *%s)'
              100  LOAD_FAST                'name'
              102  LOAD_FAST                'argname'
              104  BUILD_TUPLE_2         2 
              106  BINARY_MODULO    
              108  CALL_FUNCTION_1       1  ''
              110  POP_TOP          

 L. 366       112  LOAD_FAST                'prnt'
              114  LOAD_STR                 '{'
              116  CALL_FUNCTION_1       1  ''
              118  POP_TOP          

 L. 368       120  LOAD_STR                 'argument of %s'
              122  LOAD_FAST                'name'
              124  BINARY_MODULO    
              126  STORE_FAST               'context'

 L. 369       128  LOAD_GLOBAL              enumerate
              130  LOAD_FAST                'tp'
              132  LOAD_ATTR                args
              134  CALL_FUNCTION_1       1  ''
              136  GET_ITER         
              138  FOR_ITER            172  'to 172'
              140  UNPACK_SEQUENCE_2     2 
              142  STORE_FAST               'i'
              144  STORE_FAST               'type'

 L. 370       146  LOAD_FAST                'prnt'
              148  LOAD_STR                 '  %s;'
              150  LOAD_FAST                'type'
              152  LOAD_METHOD              get_c_name
              154  LOAD_STR                 ' x%d'
              156  LOAD_FAST                'i'
              158  BINARY_MODULO    
              160  LOAD_FAST                'context'
              162  CALL_METHOD_2         2  ''
              164  BINARY_MODULO    
              166  CALL_FUNCTION_1       1  ''
              168  POP_TOP          
              170  JUMP_BACK           138  'to 138'

 L. 372       172  LOAD_GLOBAL              set
              174  CALL_FUNCTION_0       0  ''
              176  STORE_FAST               'localvars'

 L. 373       178  LOAD_GLOBAL              set
              180  CALL_FUNCTION_0       0  ''
              182  STORE_FAST               'freelines'

 L. 374       184  LOAD_FAST                'tp'
              186  LOAD_ATTR                args
              188  GET_ITER         
              190  FOR_ITER            210  'to 210'
              192  STORE_FAST               'type'

 L. 375       194  LOAD_FAST                'self'
              196  LOAD_METHOD              _extra_local_variables
              198  LOAD_FAST                'type'
              200  LOAD_FAST                'localvars'
              202  LOAD_FAST                'freelines'
              204  CALL_METHOD_3         3  ''
              206  POP_TOP          
              208  JUMP_BACK           190  'to 190'

 L. 376       210  LOAD_GLOBAL              sorted
              212  LOAD_FAST                'localvars'
              214  CALL_FUNCTION_1       1  ''
              216  GET_ITER         
              218  FOR_ITER            238  'to 238'
              220  STORE_FAST               'decl'

 L. 377       222  LOAD_FAST                'prnt'
              224  LOAD_STR                 '  %s;'
              226  LOAD_FAST                'decl'
              228  BUILD_TUPLE_1         1 
              230  BINARY_MODULO    
              232  CALL_FUNCTION_1       1  ''
              234  POP_TOP          
              236  JUMP_BACK           218  'to 218'

 L. 379       238  LOAD_GLOBAL              isinstance
              240  LOAD_FAST                'tp'
              242  LOAD_ATTR                result
              244  LOAD_GLOBAL              model
              246  LOAD_ATTR                VoidType
              248  CALL_FUNCTION_2       2  ''
          250_252  POP_JUMP_IF_TRUE    298  'to 298'

 L. 380       254  LOAD_STR                 'result = '
              256  STORE_FAST               'result_code'

 L. 381       258  LOAD_STR                 'result of %s'
              260  LOAD_FAST                'name'
              262  BINARY_MODULO    
              264  STORE_FAST               'context'

 L. 382       266  LOAD_FAST                'prnt'
              268  LOAD_STR                 '  %s;'
              270  LOAD_FAST                'tp'
              272  LOAD_ATTR                result
              274  LOAD_METHOD              get_c_name
              276  LOAD_STR                 ' result'
              278  LOAD_FAST                'context'
              280  CALL_METHOD_2         2  ''
              282  BINARY_MODULO    
              284  CALL_FUNCTION_1       1  ''
              286  POP_TOP          

 L. 383       288  LOAD_FAST                'prnt'
              290  LOAD_STR                 '  PyObject *pyresult;'
              292  CALL_FUNCTION_1       1  ''
              294  POP_TOP          
              296  JUMP_FORWARD        302  'to 302'
            298_0  COME_FROM           250  '250'

 L. 385       298  LOAD_STR                 ''
              300  STORE_FAST               'result_code'
            302_0  COME_FROM           296  '296'

 L. 387       302  LOAD_GLOBAL              len
              304  LOAD_FAST                'tp'
              306  LOAD_ATTR                args
              308  CALL_FUNCTION_1       1  ''
              310  LOAD_CONST               1
              312  COMPARE_OP               >
          314_316  POP_JUMP_IF_FALSE   408  'to 408'

 L. 388       318  LOAD_GLOBAL              range
              320  LOAD_GLOBAL              len
              322  LOAD_FAST                'tp'
              324  LOAD_ATTR                args
              326  CALL_FUNCTION_1       1  ''
              328  CALL_FUNCTION_1       1  ''
              330  STORE_FAST               'rng'

 L. 389       332  LOAD_FAST                'rng'
              334  GET_ITER         
              336  FOR_ITER            356  'to 356'
              338  STORE_FAST               'i'

 L. 390       340  LOAD_FAST                'prnt'
              342  LOAD_STR                 '  PyObject *arg%d;'
              344  LOAD_FAST                'i'
              346  BINARY_MODULO    
              348  CALL_FUNCTION_1       1  ''
              350  POP_TOP          
          352_354  JUMP_BACK           336  'to 336'

 L. 391       356  LOAD_FAST                'prnt'
              358  CALL_FUNCTION_0       0  ''
              360  POP_TOP          

 L. 392       362  LOAD_FAST                'prnt'
              364  LOAD_STR                 '  if (!PyArg_ParseTuple(args, "%s:%s", %s))'

 L. 393       366  LOAD_STR                 'O'
              368  LOAD_FAST                'numargs'
              370  BINARY_MULTIPLY  
              372  LOAD_FAST                'name'
              374  LOAD_STR                 ', '
              376  LOAD_METHOD              join
              378  LOAD_LISTCOMP            '<code_object <listcomp>>'
              380  LOAD_STR                 'VCPythonEngine._generate_cpy_function_decl.<locals>.<listcomp>'
              382  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              384  LOAD_FAST                'rng'
              386  GET_ITER         
              388  CALL_FUNCTION_1       1  ''
              390  CALL_METHOD_1         1  ''

 L. 392       392  BUILD_TUPLE_3         3 
              394  BINARY_MODULO    
              396  CALL_FUNCTION_1       1  ''
              398  POP_TOP          

 L. 394       400  LOAD_FAST                'prnt'
              402  LOAD_STR                 '    return NULL;'
              404  CALL_FUNCTION_1       1  ''
              406  POP_TOP          
            408_0  COME_FROM           314  '314'

 L. 395       408  LOAD_FAST                'prnt'
              410  CALL_FUNCTION_0       0  ''
              412  POP_TOP          

 L. 397       414  LOAD_GLOBAL              enumerate
              416  LOAD_FAST                'tp'
              418  LOAD_ATTR                args
              420  CALL_FUNCTION_1       1  ''
              422  GET_ITER         
              424  FOR_ITER            466  'to 466'
              426  UNPACK_SEQUENCE_2     2 
              428  STORE_FAST               'i'
              430  STORE_FAST               'type'

 L. 398       432  LOAD_FAST                'self'
              434  LOAD_METHOD              _convert_funcarg_to_c
              436  LOAD_FAST                'type'
              438  LOAD_STR                 'arg%d'
              440  LOAD_FAST                'i'
              442  BINARY_MODULO    
              444  LOAD_STR                 'x%d'
              446  LOAD_FAST                'i'
              448  BINARY_MODULO    

 L. 399       450  LOAD_STR                 'return NULL'

 L. 398       452  CALL_METHOD_4         4  ''
              454  POP_TOP          

 L. 400       456  LOAD_FAST                'prnt'
              458  CALL_FUNCTION_0       0  ''
              460  POP_TOP          
          462_464  JUMP_BACK           424  'to 424'

 L. 402       466  LOAD_FAST                'prnt'
              468  LOAD_STR                 '  Py_BEGIN_ALLOW_THREADS'
              470  CALL_FUNCTION_1       1  ''
              472  POP_TOP          

 L. 403       474  LOAD_FAST                'prnt'
              476  LOAD_STR                 '  _cffi_restore_errno();'
              478  CALL_FUNCTION_1       1  ''
              480  POP_TOP          

 L. 404       482  LOAD_FAST                'prnt'
              484  LOAD_STR                 '  { %s%s(%s); }'

 L. 405       486  LOAD_FAST                'result_code'
              488  LOAD_FAST                'name'

 L. 406       490  LOAD_STR                 ', '
              492  LOAD_METHOD              join
              494  LOAD_LISTCOMP            '<code_object <listcomp>>'
              496  LOAD_STR                 'VCPythonEngine._generate_cpy_function_decl.<locals>.<listcomp>'
              498  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              500  LOAD_GLOBAL              range
              502  LOAD_GLOBAL              len
              504  LOAD_FAST                'tp'
              506  LOAD_ATTR                args
              508  CALL_FUNCTION_1       1  ''
              510  CALL_FUNCTION_1       1  ''
              512  GET_ITER         
              514  CALL_FUNCTION_1       1  ''
              516  CALL_METHOD_1         1  ''

 L. 404       518  BUILD_TUPLE_3         3 
              520  BINARY_MODULO    
              522  CALL_FUNCTION_1       1  ''
              524  POP_TOP          

 L. 407       526  LOAD_FAST                'prnt'
              528  LOAD_STR                 '  _cffi_save_errno();'
              530  CALL_FUNCTION_1       1  ''
              532  POP_TOP          

 L. 408       534  LOAD_FAST                'prnt'
              536  LOAD_STR                 '  Py_END_ALLOW_THREADS'
              538  CALL_FUNCTION_1       1  ''
              540  POP_TOP          

 L. 409       542  LOAD_FAST                'prnt'
              544  CALL_FUNCTION_0       0  ''
              546  POP_TOP          

 L. 411       548  LOAD_FAST                'prnt'
              550  LOAD_STR                 '  (void)self; /* unused */'
              552  CALL_FUNCTION_1       1  ''
              554  POP_TOP          

 L. 412       556  LOAD_FAST                'numargs'
              558  LOAD_CONST               0
              560  COMPARE_OP               ==
          562_564  POP_JUMP_IF_FALSE   574  'to 574'

 L. 413       566  LOAD_FAST                'prnt'
              568  LOAD_STR                 '  (void)noarg; /* unused */'
              570  CALL_FUNCTION_1       1  ''
              572  POP_TOP          
            574_0  COME_FROM           562  '562'

 L. 414       574  LOAD_FAST                'result_code'
          576_578  POP_JUMP_IF_FALSE   638  'to 638'

 L. 415       580  LOAD_FAST                'prnt'
              582  LOAD_STR                 '  pyresult = %s;'

 L. 416       584  LOAD_FAST                'self'
              586  LOAD_METHOD              _convert_expr_from_c
              588  LOAD_FAST                'tp'
              590  LOAD_ATTR                result
              592  LOAD_STR                 'result'
              594  LOAD_STR                 'result type'
              596  CALL_METHOD_3         3  ''

 L. 415       598  BINARY_MODULO    
              600  CALL_FUNCTION_1       1  ''
              602  POP_TOP          

 L. 417       604  LOAD_FAST                'freelines'
              606  GET_ITER         
              608  FOR_ITER            628  'to 628'
              610  STORE_FAST               'freeline'

 L. 418       612  LOAD_FAST                'prnt'
              614  LOAD_STR                 '  '
              616  LOAD_FAST                'freeline'
              618  BINARY_ADD       
              620  CALL_FUNCTION_1       1  ''
              622  POP_TOP          
          624_626  JUMP_BACK           608  'to 608'

 L. 419       628  LOAD_FAST                'prnt'
              630  LOAD_STR                 '  return pyresult;'
              632  CALL_FUNCTION_1       1  ''
              634  POP_TOP          
              636  JUMP_FORWARD        678  'to 678'
            638_0  COME_FROM           576  '576'

 L. 421       638  LOAD_FAST                'freelines'
              640  GET_ITER         
              642  FOR_ITER            662  'to 662'
              644  STORE_FAST               'freeline'

 L. 422       646  LOAD_FAST                'prnt'
              648  LOAD_STR                 '  '
              650  LOAD_FAST                'freeline'
              652  BINARY_ADD       
              654  CALL_FUNCTION_1       1  ''
              656  POP_TOP          
          658_660  JUMP_BACK           642  'to 642'

 L. 423       662  LOAD_FAST                'prnt'
              664  LOAD_STR                 '  Py_INCREF(Py_None);'
              666  CALL_FUNCTION_1       1  ''
              668  POP_TOP          

 L. 424       670  LOAD_FAST                'prnt'
              672  LOAD_STR                 '  return Py_None;'
              674  CALL_FUNCTION_1       1  ''
              676  POP_TOP          
            678_0  COME_FROM           636  '636'

 L. 425       678  LOAD_FAST                'prnt'
              680  LOAD_STR                 '}'
              682  CALL_FUNCTION_1       1  ''
              684  POP_TOP          

 L. 426       686  LOAD_FAST                'prnt'
              688  CALL_FUNCTION_0       0  ''
              690  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _generate_cpy_function_method(self, tp, name):
        if tp.ellipsis:
            return
        else:
            numargs = len(tp.args)
            if numargs == 0:
                meth = 'METH_NOARGS'
            else:
                if numargs == 1:
                    meth = 'METH_O'
                else:
                    meth = 'METH_VARARGS'
        self._prnt('  {"%s", _cffi_f_%s, %s, NULL},' % (name, name, meth))

    _loading_cpy_function = _loaded_noop

    def _loaded_cpy_function(self, tp, name, module, library):
        if tp.ellipsis:
            return
        func = getattrmodulename
        setattr(library, name, func)
        self._types_of_builtin_functions[func] = tp

    _generate_cpy_struct_collecttype = _generate_nothing

    def _generate_cpy_struct_decl--- This code section failed: ---

 L. 454         0  LOAD_FAST                'name'
                2  LOAD_FAST                'tp'
                4  LOAD_ATTR                name
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 455        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _generate_struct_or_union_decl
               18  LOAD_FAST                'tp'
               20  LOAD_STR                 'struct'
               22  LOAD_FAST                'name'
               24  CALL_METHOD_3         3  ''
               26  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _generate_cpy_struct_method(self, tp, name):
        self._generate_struct_or_union_methodtp'struct'name

    def _loading_cpy_struct(self, tp, name, module):
        self._loading_struct_or_union(tp, 'struct', name, module)

    def _loaded_cpy_struct(self, tp, name, module, **kwds):
        self._loaded_struct_or_union(tp)

    _generate_cpy_union_collecttype = _generate_nothing

    def _generate_cpy_union_decl--- This code section failed: ---

 L. 465         0  LOAD_FAST                'name'
                2  LOAD_FAST                'tp'
                4  LOAD_ATTR                name
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 466        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _generate_struct_or_union_decl
               18  LOAD_FAST                'tp'
               20  LOAD_STR                 'union'
               22  LOAD_FAST                'name'
               24  CALL_METHOD_3         3  ''
               26  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _generate_cpy_union_method(self, tp, name):
        self._generate_struct_or_union_methodtp'union'name

    def _loading_cpy_union(self, tp, name, module):
        self._loading_struct_or_union(tp, 'union', name, module)

    def _loaded_cpy_union(self, tp, name, module, **kwds):
        self._loaded_struct_or_union(tp)

    def _generate_struct_or_union_decl--- This code section failed: ---

 L. 475         0  LOAD_FAST                'tp'
                2  LOAD_ATTR                fldnames
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 476        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 477        14  LOAD_STR                 '_cffi_check_%s_%s'
               16  LOAD_FAST                'prefix'
               18  LOAD_FAST                'name'
               20  BUILD_TUPLE_2         2 
               22  BINARY_MODULO    
               24  STORE_FAST               'checkfuncname'

 L. 478        26  LOAD_STR                 '_cffi_layout_%s_%s'
               28  LOAD_FAST                'prefix'
               30  LOAD_FAST                'name'
               32  BUILD_TUPLE_2         2 
               34  BINARY_MODULO    
               36  STORE_FAST               'layoutfuncname'

 L. 479        38  LOAD_STR                 '%s %s'
               40  LOAD_FAST                'prefix'
               42  LOAD_FAST                'name'
               44  BUILD_TUPLE_2         2 
               46  BINARY_MODULO    
               48  LOAD_METHOD              strip
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'cname'

 L. 481        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _prnt
               58  STORE_FAST               'prnt'

 L. 482        60  LOAD_FAST                'prnt'
               62  LOAD_STR                 'static void %s(%s *p)'
               64  LOAD_FAST                'checkfuncname'
               66  LOAD_FAST                'cname'
               68  BUILD_TUPLE_2         2 
               70  BINARY_MODULO    
               72  CALL_FUNCTION_1       1  ''
               74  POP_TOP          

 L. 483        76  LOAD_FAST                'prnt'
               78  LOAD_STR                 '{'
               80  CALL_FUNCTION_1       1  ''
               82  POP_TOP          

 L. 484        84  LOAD_FAST                'prnt'
               86  LOAD_STR                 '  /* only to generate compile-time warnings or errors */'
               88  CALL_FUNCTION_1       1  ''
               90  POP_TOP          

 L. 485        92  LOAD_FAST                'prnt'
               94  LOAD_STR                 '  (void)p;'
               96  CALL_FUNCTION_1       1  ''
               98  POP_TOP          

 L. 486       100  LOAD_FAST                'tp'
              102  LOAD_METHOD              enumfields
              104  CALL_METHOD_0         0  ''
              106  GET_ITER         
              108  FOR_ITER            254  'to 254'
              110  UNPACK_SEQUENCE_4     4 
              112  STORE_FAST               'fname'
              114  STORE_FAST               'ftype'
              116  STORE_FAST               'fbitsize'
              118  STORE_FAST               'fqual'

 L. 487       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'ftype'
              124  LOAD_GLOBAL              model
              126  LOAD_ATTR                PrimitiveType
              128  CALL_FUNCTION_2       2  ''
              130  POP_JUMP_IF_FALSE   140  'to 140'

 L. 488       132  LOAD_FAST                'ftype'
              134  LOAD_METHOD              is_integer_type
              136  CALL_METHOD_0         0  ''

 L. 487       138  POP_JUMP_IF_TRUE    148  'to 148'
            140_0  COME_FROM           130  '130'

 L. 488       140  LOAD_FAST                'fbitsize'
              142  LOAD_CONST               0
              144  COMPARE_OP               >=

 L. 487       146  POP_JUMP_IF_FALSE   162  'to 162'
            148_0  COME_FROM           138  '138'

 L. 490       148  LOAD_FAST                'prnt'
              150  LOAD_STR                 '  (void)((p->%s) << 1);'
              152  LOAD_FAST                'fname'
              154  BINARY_MODULO    
              156  CALL_FUNCTION_1       1  ''
              158  POP_TOP          
              160  JUMP_BACK           108  'to 108'
            162_0  COME_FROM           146  '146'

 L. 493       162  SETUP_FINALLY       200  'to 200'

 L. 494       164  LOAD_FAST                'prnt'
              166  LOAD_STR                 '  { %s = &p->%s; (void)tmp; }'

 L. 495       168  LOAD_FAST                'ftype'
              170  LOAD_ATTR                get_c_name
              172  LOAD_STR                 '*tmp'
              174  LOAD_STR                 'field %r'
              176  LOAD_FAST                'fname'
              178  BINARY_MODULO    
              180  LOAD_FAST                'fqual'
              182  LOAD_CONST               ('quals',)
              184  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 496       186  LOAD_FAST                'fname'

 L. 494       188  BUILD_TUPLE_2         2 
              190  BINARY_MODULO    
              192  CALL_FUNCTION_1       1  ''
              194  POP_TOP          
              196  POP_BLOCK        
              198  JUMP_BACK           108  'to 108'
            200_0  COME_FROM_FINALLY   162  '162'

 L. 497       200  DUP_TOP          
              202  LOAD_GLOBAL              VerificationError
              204  <121>               250  ''
              206  POP_TOP          
              208  STORE_FAST               'e'
              210  POP_TOP          
              212  SETUP_FINALLY       242  'to 242'

 L. 498       214  LOAD_FAST                'prnt'
              216  LOAD_STR                 '  /* %s */'
              218  LOAD_GLOBAL              str
              220  LOAD_FAST                'e'
              222  CALL_FUNCTION_1       1  ''
              224  BINARY_MODULO    
              226  CALL_FUNCTION_1       1  ''
              228  POP_TOP          
              230  POP_BLOCK        
              232  POP_EXCEPT       
              234  LOAD_CONST               None
              236  STORE_FAST               'e'
              238  DELETE_FAST              'e'
              240  JUMP_BACK           108  'to 108'
            242_0  COME_FROM_FINALLY   212  '212'
              242  LOAD_CONST               None
              244  STORE_FAST               'e'
              246  DELETE_FAST              'e'
              248  <48>             
              250  <48>             
              252  JUMP_BACK           108  'to 108'

 L. 499       254  LOAD_FAST                'prnt'
              256  LOAD_STR                 '}'
              258  CALL_FUNCTION_1       1  ''
              260  POP_TOP          

 L. 500       262  LOAD_FAST                'prnt'
              264  LOAD_STR                 'static PyObject *'
              266  CALL_FUNCTION_1       1  ''
              268  POP_TOP          

 L. 501       270  LOAD_FAST                'prnt'
              272  LOAD_STR                 '%s(PyObject *self, PyObject *noarg)'
              274  LOAD_FAST                'layoutfuncname'
              276  BUILD_TUPLE_1         1 
              278  BINARY_MODULO    
              280  CALL_FUNCTION_1       1  ''
              282  POP_TOP          

 L. 502       284  LOAD_FAST                'prnt'
              286  LOAD_STR                 '{'
              288  CALL_FUNCTION_1       1  ''
              290  POP_TOP          

 L. 503       292  LOAD_FAST                'prnt'
              294  LOAD_STR                 '  struct _cffi_aligncheck { char x; %s y; };'
              296  LOAD_FAST                'cname'
              298  BINARY_MODULO    
              300  CALL_FUNCTION_1       1  ''
              302  POP_TOP          

 L. 504       304  LOAD_FAST                'prnt'
              306  LOAD_STR                 '  static Py_ssize_t nums[] = {'
              308  CALL_FUNCTION_1       1  ''
              310  POP_TOP          

 L. 505       312  LOAD_FAST                'prnt'
              314  LOAD_STR                 '    sizeof(%s),'
              316  LOAD_FAST                'cname'
              318  BINARY_MODULO    
              320  CALL_FUNCTION_1       1  ''
              322  POP_TOP          

 L. 506       324  LOAD_FAST                'prnt'
              326  LOAD_STR                 '    offsetof(struct _cffi_aligncheck, y),'
              328  CALL_FUNCTION_1       1  ''
              330  POP_TOP          

 L. 507       332  LOAD_FAST                'tp'
              334  LOAD_METHOD              enumfields
              336  CALL_METHOD_0         0  ''
              338  GET_ITER         
              340  FOR_ITER            446  'to 446'
              342  UNPACK_SEQUENCE_4     4 
              344  STORE_FAST               'fname'
              346  STORE_FAST               'ftype'
              348  STORE_FAST               'fbitsize'
              350  STORE_FAST               'fqual'

 L. 508       352  LOAD_FAST                'fbitsize'
              354  LOAD_CONST               0
              356  COMPARE_OP               >=
          358_360  POP_JUMP_IF_FALSE   366  'to 366'

 L. 509   362_364  JUMP_BACK           340  'to 340'
            366_0  COME_FROM           358  '358'

 L. 510       366  LOAD_FAST                'prnt'
              368  LOAD_STR                 '    offsetof(%s, %s),'
              370  LOAD_FAST                'cname'
              372  LOAD_FAST                'fname'
              374  BUILD_TUPLE_2         2 
              376  BINARY_MODULO    
              378  CALL_FUNCTION_1       1  ''
              380  POP_TOP          

 L. 511       382  LOAD_GLOBAL              isinstance
              384  LOAD_FAST                'ftype'
              386  LOAD_GLOBAL              model
              388  LOAD_ATTR                ArrayType
              390  CALL_FUNCTION_2       2  ''
          392_394  POP_JUMP_IF_FALSE   426  'to 426'
              396  LOAD_FAST                'ftype'
              398  LOAD_ATTR                length
              400  LOAD_CONST               None
              402  <117>                 0  ''
          404_406  POP_JUMP_IF_FALSE   426  'to 426'

 L. 512       408  LOAD_FAST                'prnt'
              410  LOAD_STR                 '    0,  /* %s */'
              412  LOAD_FAST                'ftype'
              414  LOAD_METHOD              _get_c_name
              416  CALL_METHOD_0         0  ''
              418  BINARY_MODULO    
              420  CALL_FUNCTION_1       1  ''
              422  POP_TOP          
              424  JUMP_BACK           340  'to 340'
            426_0  COME_FROM           404  '404'
            426_1  COME_FROM           392  '392'

 L. 514       426  LOAD_FAST                'prnt'
              428  LOAD_STR                 '    sizeof(((%s *)0)->%s),'
              430  LOAD_FAST                'cname'
              432  LOAD_FAST                'fname'
              434  BUILD_TUPLE_2         2 
              436  BINARY_MODULO    
              438  CALL_FUNCTION_1       1  ''
              440  POP_TOP          
          442_444  JUMP_BACK           340  'to 340'

 L. 515       446  LOAD_FAST                'prnt'
              448  LOAD_STR                 '    -1'
              450  CALL_FUNCTION_1       1  ''
              452  POP_TOP          

 L. 516       454  LOAD_FAST                'prnt'
              456  LOAD_STR                 '  };'
              458  CALL_FUNCTION_1       1  ''
              460  POP_TOP          

 L. 517       462  LOAD_FAST                'prnt'
              464  LOAD_STR                 '  (void)self; /* unused */'
              466  CALL_FUNCTION_1       1  ''
              468  POP_TOP          

 L. 518       470  LOAD_FAST                'prnt'
              472  LOAD_STR                 '  (void)noarg; /* unused */'
              474  CALL_FUNCTION_1       1  ''
              476  POP_TOP          

 L. 519       478  LOAD_FAST                'prnt'
              480  LOAD_STR                 '  return _cffi_get_struct_layout(nums);'
              482  CALL_FUNCTION_1       1  ''
              484  POP_TOP          

 L. 520       486  LOAD_FAST                'prnt'
              488  LOAD_STR                 '  /* the next line is not executed, but compiled */'
              490  CALL_FUNCTION_1       1  ''
              492  POP_TOP          

 L. 521       494  LOAD_FAST                'prnt'
              496  LOAD_STR                 '  %s(0);'
              498  LOAD_FAST                'checkfuncname'
              500  BUILD_TUPLE_1         1 
              502  BINARY_MODULO    
              504  CALL_FUNCTION_1       1  ''
              506  POP_TOP          

 L. 522       508  LOAD_FAST                'prnt'
              510  LOAD_STR                 '}'
              512  CALL_FUNCTION_1       1  ''
              514  POP_TOP          

 L. 523       516  LOAD_FAST                'prnt'
              518  CALL_FUNCTION_0       0  ''
              520  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _generate_struct_or_union_method--- This code section failed: ---

 L. 526         0  LOAD_FAST                'tp'
                2  LOAD_ATTR                fldnames
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 527        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 528        14  LOAD_STR                 '_cffi_layout_%s_%s'
               16  LOAD_FAST                'prefix'
               18  LOAD_FAST                'name'
               20  BUILD_TUPLE_2         2 
               22  BINARY_MODULO    
               24  STORE_FAST               'layoutfuncname'

 L. 529        26  LOAD_FAST                'self'
               28  LOAD_METHOD              _prnt
               30  LOAD_STR                 '  {"%s", %s, METH_NOARGS, NULL},'
               32  LOAD_FAST                'layoutfuncname'

 L. 530        34  LOAD_FAST                'layoutfuncname'

 L. 529        36  BUILD_TUPLE_2         2 
               38  BINARY_MODULO    
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _loading_struct_or_union--- This code section failed: ---

 L. 533         0  LOAD_FAST                'tp'
                2  LOAD_ATTR                fldnames
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 534        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 535        14  LOAD_STR                 '_cffi_layout_%s_%s'
               16  LOAD_FAST                'prefix'
               18  LOAD_FAST                'name'
               20  BUILD_TUPLE_2         2 
               22  BINARY_MODULO    
               24  STORE_FAST               'layoutfuncname'

 L. 537        26  LOAD_GLOBAL              getattr
               28  LOAD_FAST                'module'
               30  LOAD_FAST                'layoutfuncname'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'function'

 L. 538        36  LOAD_FAST                'function'
               38  CALL_FUNCTION_0       0  ''
               40  STORE_FAST               'layout'

 L. 539        42  LOAD_GLOBAL              isinstance
               44  LOAD_FAST                'tp'
               46  LOAD_GLOBAL              model
               48  LOAD_ATTR                StructOrUnion
               50  CALL_FUNCTION_2       2  ''
               52  POP_JUMP_IF_FALSE   168  'to 168'
               54  LOAD_FAST                'tp'
               56  LOAD_ATTR                partial
               58  POP_JUMP_IF_FALSE   168  'to 168'

 L. 542        60  LOAD_FAST                'layout'
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  STORE_FAST               'totalsize'

 L. 543        68  LOAD_FAST                'layout'
               70  LOAD_CONST               1
               72  BINARY_SUBSCR    
               74  STORE_FAST               'totalalignment'

 L. 544        76  LOAD_FAST                'layout'
               78  LOAD_CONST               2
               80  LOAD_CONST               None
               82  LOAD_CONST               2
               84  BUILD_SLICE_3         3 
               86  BINARY_SUBSCR    
               88  STORE_FAST               'fieldofs'

 L. 545        90  LOAD_FAST                'layout'
               92  LOAD_CONST               3
               94  LOAD_CONST               None
               96  LOAD_CONST               2
               98  BUILD_SLICE_3         3 
              100  BINARY_SUBSCR    
              102  STORE_FAST               'fieldsize'

 L. 546       104  LOAD_FAST                'tp'
              106  LOAD_METHOD              force_flatten
              108  CALL_METHOD_0         0  ''
              110  POP_TOP          

 L. 547       112  LOAD_GLOBAL              len
              114  LOAD_FAST                'fieldofs'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_GLOBAL              len
              120  LOAD_FAST                'fieldsize'
              122  CALL_FUNCTION_1       1  ''
              124  DUP_TOP          
              126  ROT_THREE        
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   146  'to 146'
              132  LOAD_GLOBAL              len
              134  LOAD_FAST                'tp'
              136  LOAD_ATTR                fldnames
              138  CALL_FUNCTION_1       1  ''
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_TRUE    152  'to 152'
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           130  '130'
              146  POP_TOP          
            148_0  COME_FROM           144  '144'
              148  <74>             
              150  RAISE_VARARGS_1       1  'exception instance'
            152_0  COME_FROM           142  '142'

 L. 548       152  LOAD_FAST                'fieldofs'
              154  LOAD_FAST                'fieldsize'
              156  LOAD_FAST                'totalsize'
              158  LOAD_FAST                'totalalignment'
              160  BUILD_TUPLE_4         4 
              162  LOAD_FAST                'tp'
              164  STORE_ATTR               fixedlayout
              166  JUMP_FORWARD        198  'to 198'
            168_0  COME_FROM            58  '58'
            168_1  COME_FROM            52  '52'

 L. 550       168  LOAD_STR                 '%s %s'
              170  LOAD_FAST                'prefix'
              172  LOAD_FAST                'name'
              174  BUILD_TUPLE_2         2 
              176  BINARY_MODULO    
              178  LOAD_METHOD              strip
              180  CALL_METHOD_0         0  ''
              182  STORE_FAST               'cname'

 L. 551       184  LOAD_FAST                'layout'
              186  LOAD_FAST                'cname'
              188  BUILD_TUPLE_2         2 
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                _struct_pending_verification
              194  LOAD_FAST                'tp'
              196  STORE_SUBSCR     
            198_0  COME_FROM           166  '166'

Parse error at or near `None' instruction at offset -1

    def _loaded_struct_or_union--- This code section failed: ---

 L. 554         0  LOAD_FAST                'tp'
                2  LOAD_ATTR                fldnames
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 555        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 556        14  LOAD_FAST                'self'
               16  LOAD_ATTR                ffi
               18  LOAD_METHOD              _get_cached_btype
               20  LOAD_FAST                'tp'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L. 558        26  LOAD_FAST                'tp'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _struct_pending_verification
               32  <118>                 0  ''
            34_36  POP_JUMP_IF_FALSE   272  'to 272'

 L. 560        38  LOAD_CODE                <code_object check>
               40  LOAD_STR                 'VCPythonEngine._loaded_struct_or_union.<locals>.check'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               44  STORE_FAST               'check'

 L. 565        46  LOAD_FAST                'self'
               48  LOAD_ATTR                ffi
               50  STORE_FAST               'ffi'

 L. 566        52  LOAD_FAST                'ffi'
               54  LOAD_METHOD              _get_cached_btype
               56  LOAD_FAST                'tp'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'BStruct'

 L. 567        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _struct_pending_verification
               66  LOAD_METHOD              pop
               68  LOAD_FAST                'tp'
               70  CALL_METHOD_1         1  ''
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'layout'
               76  STORE_FAST               'cname'

 L. 568        78  LOAD_FAST                'check'
               80  LOAD_FAST                'layout'
               82  LOAD_CONST               0
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'ffi'
               88  LOAD_METHOD              sizeof
               90  LOAD_FAST                'BStruct'
               92  CALL_METHOD_1         1  ''
               94  LOAD_STR                 'wrong total size'
               96  CALL_FUNCTION_3       3  ''
               98  POP_TOP          

 L. 569       100  LOAD_FAST                'check'
              102  LOAD_FAST                'layout'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  LOAD_FAST                'ffi'
              110  LOAD_METHOD              alignof
              112  LOAD_FAST                'BStruct'
              114  CALL_METHOD_1         1  ''
              116  LOAD_STR                 'wrong total alignment'
              118  CALL_FUNCTION_3       3  ''
              120  POP_TOP          

 L. 570       122  LOAD_CONST               2
              124  STORE_FAST               'i'

 L. 571       126  LOAD_FAST                'tp'
              128  LOAD_METHOD              enumfields
              130  CALL_METHOD_0         0  ''
              132  GET_ITER         
              134  FOR_ITER            254  'to 254'
              136  UNPACK_SEQUENCE_4     4 
              138  STORE_FAST               'fname'
              140  STORE_FAST               'ftype'
              142  STORE_FAST               'fbitsize'
              144  STORE_FAST               'fqual'

 L. 572       146  LOAD_FAST                'fbitsize'
              148  LOAD_CONST               0
              150  COMPARE_OP               >=
              152  POP_JUMP_IF_FALSE   156  'to 156'

 L. 573       154  JUMP_BACK           134  'to 134'
            156_0  COME_FROM           152  '152'

 L. 574       156  LOAD_FAST                'check'
              158  LOAD_FAST                'layout'
              160  LOAD_FAST                'i'
              162  BINARY_SUBSCR    
              164  LOAD_FAST                'ffi'
              166  LOAD_METHOD              offsetof
              168  LOAD_FAST                'BStruct'
              170  LOAD_FAST                'fname'
              172  CALL_METHOD_2         2  ''

 L. 575       174  LOAD_STR                 'wrong offset for field %r'
              176  LOAD_FAST                'fname'
              178  BUILD_TUPLE_1         1 
              180  BINARY_MODULO    

 L. 574       182  CALL_FUNCTION_3       3  ''
              184  POP_TOP          

 L. 576       186  LOAD_FAST                'layout'
              188  LOAD_FAST                'i'
              190  LOAD_CONST               1
              192  BINARY_ADD       
              194  BINARY_SUBSCR    
              196  LOAD_CONST               0
              198  COMPARE_OP               !=
              200  POP_JUMP_IF_FALSE   244  'to 244'

 L. 577       202  LOAD_FAST                'ffi'
              204  LOAD_METHOD              _get_cached_btype
              206  LOAD_FAST                'ftype'
              208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'BField'

 L. 578       212  LOAD_FAST                'check'
              214  LOAD_FAST                'layout'
              216  LOAD_FAST                'i'
              218  LOAD_CONST               1
              220  BINARY_ADD       
              222  BINARY_SUBSCR    
              224  LOAD_FAST                'ffi'
              226  LOAD_METHOD              sizeof
              228  LOAD_FAST                'BField'
              230  CALL_METHOD_1         1  ''

 L. 579       232  LOAD_STR                 'wrong size for field %r'
              234  LOAD_FAST                'fname'
              236  BUILD_TUPLE_1         1 
              238  BINARY_MODULO    

 L. 578       240  CALL_FUNCTION_3       3  ''
              242  POP_TOP          
            244_0  COME_FROM           200  '200'

 L. 580       244  LOAD_FAST                'i'
              246  LOAD_CONST               2
              248  INPLACE_ADD      
              250  STORE_FAST               'i'
              252  JUMP_BACK           134  'to 134'

 L. 581       254  LOAD_FAST                'i'
              256  LOAD_GLOBAL              len
              258  LOAD_FAST                'layout'
              260  CALL_FUNCTION_1       1  ''
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_TRUE    272  'to 272'
              268  <74>             
              270  RAISE_VARARGS_1       1  'exception instance'
            272_0  COME_FROM           264  '264'
            272_1  COME_FROM            34  '34'

Parse error at or near `None' instruction at offset -1

    _generate_cpy_anonymous_collecttype = _generate_nothing

    def _generate_cpy_anonymous_decl(self, tp, name):
        if isinstancetpmodel.EnumType:
            self._generate_cpy_enum_decltpname''
        else:
            self._generate_struct_or_union_decltp''name

    def _generate_cpy_anonymous_method(self, tp, name):
        if not isinstancetpmodel.EnumType:
            self._generate_struct_or_union_methodtp''name

    def _loading_cpy_anonymous(self, tp, name, module):
        if isinstancetpmodel.EnumType:
            self._loading_cpy_enumtpnamemodule
        else:
            self._loading_struct_or_union(tp, '', name, module)

    def _loaded_cpy_anonymous--- This code section failed: ---

 L. 606         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                EnumType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    36  'to 36'

 L. 607        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _loaded_cpy_enum
               16  LOAD_FAST                'tp'
               18  LOAD_FAST                'name'
               20  LOAD_FAST                'module'
               22  BUILD_TUPLE_3         3 
               24  BUILD_MAP_0           0 
               26  LOAD_FAST                'kwds'
               28  <164>                 1  ''
               30  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               32  POP_TOP          
               34  JUMP_FORWARD         46  'to 46'
             36_0  COME_FROM            10  '10'

 L. 609        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _loaded_struct_or_union
               40  LOAD_FAST                'tp'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
             46_0  COME_FROM            34  '34'

Parse error at or near `<164>' instruction at offset 28

    def _generate_cpy_const--- This code section failed: ---

 L. 617         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _prnt
                4  STORE_FAST               'prnt'

 L. 618         6  LOAD_STR                 '_cffi_%s_%s'
                8  LOAD_FAST                'category'
               10  LOAD_FAST                'name'
               12  BUILD_TUPLE_2         2 
               14  BINARY_MODULO    
               16  STORE_FAST               'funcname'

 L. 619        18  LOAD_FAST                'prnt'
               20  LOAD_STR                 'static int %s(PyObject *lib)'
               22  LOAD_FAST                'funcname'
               24  BINARY_MODULO    
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          

 L. 620        30  LOAD_FAST                'prnt'
               32  LOAD_STR                 '{'
               34  CALL_FUNCTION_1       1  ''
               36  POP_TOP          

 L. 621        38  LOAD_FAST                'prnt'
               40  LOAD_STR                 '  PyObject *o;'
               42  CALL_FUNCTION_1       1  ''
               44  POP_TOP          

 L. 622        46  LOAD_FAST                'prnt'
               48  LOAD_STR                 '  int res;'
               50  CALL_FUNCTION_1       1  ''
               52  POP_TOP          

 L. 623        54  LOAD_FAST                'is_int'
               56  POP_JUMP_IF_TRUE     84  'to 84'

 L. 624        58  LOAD_FAST                'prnt'
               60  LOAD_STR                 '  %s;'
               62  LOAD_FAST                'vartp'
               64  JUMP_IF_TRUE_OR_POP    68  'to 68'
               66  LOAD_FAST                'tp'
             68_0  COME_FROM            64  '64'
               68  LOAD_METHOD              get_c_name
               70  LOAD_STR                 ' i'
               72  LOAD_FAST                'name'
               74  CALL_METHOD_2         2  ''
               76  BINARY_MODULO    
               78  CALL_FUNCTION_1       1  ''
               80  POP_TOP          
               82  JUMP_FORWARD         96  'to 96'
             84_0  COME_FROM            56  '56'

 L. 626        84  LOAD_FAST                'category'
               86  LOAD_STR                 'const'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_TRUE     96  'to 96'
               92  <74>             
               94  RAISE_VARARGS_1       1  'exception instance'
             96_0  COME_FROM            90  '90'
             96_1  COME_FROM            82  '82'

 L. 628        96  LOAD_FAST                'check_value'
               98  LOAD_CONST               None
              100  <117>                 1  ''
              102  POP_JUMP_IF_FALSE   116  'to 116'

 L. 629       104  LOAD_FAST                'self'
              106  LOAD_METHOD              _check_int_constant_value
              108  LOAD_FAST                'name'
              110  LOAD_FAST                'check_value'
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          
            116_0  COME_FROM           102  '102'

 L. 631       116  LOAD_FAST                'is_int'
              118  POP_JUMP_IF_TRUE    190  'to 190'

 L. 632       120  LOAD_FAST                'category'
              122  LOAD_STR                 'var'
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L. 633       128  LOAD_STR                 '&'
              130  LOAD_FAST                'name'
              132  BINARY_ADD       
              134  STORE_FAST               'realexpr'
              136  JUMP_FORWARD        142  'to 142'
            138_0  COME_FROM           126  '126'

 L. 635       138  LOAD_FAST                'name'
              140  STORE_FAST               'realexpr'
            142_0  COME_FROM           136  '136'

 L. 636       142  LOAD_FAST                'prnt'
              144  LOAD_STR                 '  i = (%s);'
              146  LOAD_FAST                'realexpr'
              148  BUILD_TUPLE_1         1 
              150  BINARY_MODULO    
              152  CALL_FUNCTION_1       1  ''
              154  POP_TOP          

 L. 637       156  LOAD_FAST                'prnt'
              158  LOAD_STR                 '  o = %s;'
              160  LOAD_FAST                'self'
              162  LOAD_METHOD              _convert_expr_from_c
              164  LOAD_FAST                'tp'
              166  LOAD_STR                 'i'

 L. 638       168  LOAD_STR                 'variable type'

 L. 637       170  CALL_METHOD_3         3  ''
              172  BUILD_TUPLE_1         1 
              174  BINARY_MODULO    
              176  CALL_FUNCTION_1       1  ''
              178  POP_TOP          

 L. 639       180  LOAD_FAST                'delayed'
              182  POP_JUMP_IF_TRUE    202  'to 202'
              184  <74>             
              186  RAISE_VARARGS_1       1  'exception instance'
              188  JUMP_FORWARD        202  'to 202'
            190_0  COME_FROM           118  '118'

 L. 641       190  LOAD_FAST                'prnt'
              192  LOAD_STR                 '  o = _cffi_from_c_int_const(%s);'
              194  LOAD_FAST                'name'
              196  BINARY_MODULO    
              198  CALL_FUNCTION_1       1  ''
              200  POP_TOP          
            202_0  COME_FROM           188  '188'
            202_1  COME_FROM           182  '182'

 L. 642       202  LOAD_FAST                'prnt'
              204  LOAD_STR                 '  if (o == NULL)'
              206  CALL_FUNCTION_1       1  ''
              208  POP_TOP          

 L. 643       210  LOAD_FAST                'prnt'
              212  LOAD_STR                 '    return -1;'
              214  CALL_FUNCTION_1       1  ''
              216  POP_TOP          

 L. 644       218  LOAD_FAST                'size_too'
          220_222  POP_JUMP_IF_FALSE   286  'to 286'

 L. 645       224  LOAD_FAST                'prnt'
              226  LOAD_STR                 '  {'
              228  CALL_FUNCTION_1       1  ''
              230  POP_TOP          

 L. 646       232  LOAD_FAST                'prnt'
              234  LOAD_STR                 '    PyObject *o1 = o;'
              236  CALL_FUNCTION_1       1  ''
              238  POP_TOP          

 L. 647       240  LOAD_FAST                'prnt'
              242  LOAD_STR                 '    o = Py_BuildValue("On", o1, (Py_ssize_t)sizeof(%s));'

 L. 648       244  LOAD_FAST                'name'
              246  BUILD_TUPLE_1         1 

 L. 647       248  BINARY_MODULO    
              250  CALL_FUNCTION_1       1  ''
              252  POP_TOP          

 L. 649       254  LOAD_FAST                'prnt'
              256  LOAD_STR                 '    Py_DECREF(o1);'
              258  CALL_FUNCTION_1       1  ''
              260  POP_TOP          

 L. 650       262  LOAD_FAST                'prnt'
              264  LOAD_STR                 '    if (o == NULL)'
              266  CALL_FUNCTION_1       1  ''
              268  POP_TOP          

 L. 651       270  LOAD_FAST                'prnt'
              272  LOAD_STR                 '      return -1;'
              274  CALL_FUNCTION_1       1  ''
              276  POP_TOP          

 L. 652       278  LOAD_FAST                'prnt'
              280  LOAD_STR                 '  }'
              282  CALL_FUNCTION_1       1  ''
              284  POP_TOP          
            286_0  COME_FROM           220  '220'

 L. 653       286  LOAD_FAST                'prnt'
              288  LOAD_STR                 '  res = PyObject_SetAttrString(lib, "%s", o);'
              290  LOAD_FAST                'name'
              292  BINARY_MODULO    
              294  CALL_FUNCTION_1       1  ''
              296  POP_TOP          

 L. 654       298  LOAD_FAST                'prnt'
              300  LOAD_STR                 '  Py_DECREF(o);'
              302  CALL_FUNCTION_1       1  ''
              304  POP_TOP          

 L. 655       306  LOAD_FAST                'prnt'
              308  LOAD_STR                 '  if (res < 0)'
              310  CALL_FUNCTION_1       1  ''
              312  POP_TOP          

 L. 656       314  LOAD_FAST                'prnt'
              316  LOAD_STR                 '    return -1;'
              318  CALL_FUNCTION_1       1  ''
              320  POP_TOP          

 L. 657       322  LOAD_FAST                'prnt'
              324  LOAD_STR                 '  return %s;'
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                _chained_list_constants
              330  LOAD_FAST                'delayed'
              332  BINARY_SUBSCR    
              334  BINARY_MODULO    
              336  CALL_FUNCTION_1       1  ''
              338  POP_TOP          

 L. 658       340  LOAD_FAST                'funcname'
              342  LOAD_STR                 '(lib)'
              344  BINARY_ADD       
              346  LOAD_FAST                'self'
              348  LOAD_ATTR                _chained_list_constants
              350  LOAD_FAST                'delayed'
              352  STORE_SUBSCR     

 L. 659       354  LOAD_FAST                'prnt'
              356  LOAD_STR                 '}'
              358  CALL_FUNCTION_1       1  ''
              360  POP_TOP          

 L. 660       362  LOAD_FAST                'prnt'
              364  CALL_FUNCTION_0       0  ''
              366  POP_TOP          

Parse error at or near `<74>' instruction at offset 92

    def _generate_cpy_constant_collecttype(self, tp, name):
        is_int = isinstancetpmodel.PrimitiveType and tp.is_integer_type
        if not is_int:
            self._do_collect_type(tp)

    def _generate_cpy_constant_decl(self, tp, name):
        is_int = isinstancetpmodel.PrimitiveType and tp.is_integer_type
        self._generate_cpy_constis_intnametp

    _generate_cpy_constant_method = _generate_nothing
    _loading_cpy_constant = _loaded_noop
    _loaded_cpy_constant = _loaded_noop

    def _check_int_constant_value(self, name, value, err_prefix=''):
        prnt = self._prnt
        if value <= 0:
            prnt('  if ((%s) > 0 || (long)(%s) != %dL) {' % (
             name, name, value))
        else:
            prnt('  if ((%s) <= 0 || (unsigned long)(%s) != %dUL) {' % (
             name, name, value))
        prnt('    char buf[64];')
        prnt('    if ((%s) <= 0)' % name)
        prnt('        snprintf(buf, 63, "%%ld", (long)(%s));' % name)
        prnt('    else')
        prnt('        snprintf(buf, 63, "%%lu", (unsigned long)(%s));' % name)
        prnt('    PyErr_Format(_cffi_VerificationError,')
        prnt('                 "%s%s has the real value %s, not %s",')
        prnt('                 "%s", "%s", buf, "%d");' % (
         err_prefix, name, value))
        prnt('    return -1;')
        prnt('  }')

    def _enum_funcname(self, prefix, name):
        name = name.replace'$''___D_'
        return '_cffi_e_%s_%s' % (prefix, name)

    def _generate_cpy_enum_decl(self, tp, name, prefix='enum'):
        if tp.partial:
            for enumerator in tp.enumerators:
                self._generate_cpy_const(True, enumerator, delayed=False)
            else:
                return

        funcname = self._enum_funcnameprefixname
        prnt = self._prnt
        prnt('static int %s(PyObject *lib)' % funcname)
        prnt('{')
        for enumerator, enumvalue in ziptp.enumeratorstp.enumvalues:
            self._check_int_constant_valueenumeratorenumvalue('enum %s: ' % name)
        else:
            prnt('  return %s;' % self._chained_list_constants[True])
            self._chained_list_constants[True] = funcname + '(lib)'
            prnt('}')
            prnt()

    _generate_cpy_enum_collecttype = _generate_nothing
    _generate_cpy_enum_method = _generate_nothing

    def _loading_cpy_enum(self, tp, name, module):
        if tp.partial:
            enumvalues = [getattrmoduleenumerator for enumerator in tp.enumerators]
            tp.enumvalues = tuple(enumvalues)
            tp.partial_resolved = True

    def _loaded_cpy_enum(self, tp, name, module, library):
        for enumerator, enumvalue in ziptp.enumeratorstp.enumvalues:
            setattr(library, enumerator, enumvalue)

    def _generate_cpy_macro_decl(self, tp, name):
        if tp == '...':
            check_value = None
        else:
            check_value = tp
        self._generate_cpy_const(True, name, check_value=check_value)

    _generate_cpy_macro_collecttype = _generate_nothing
    _generate_cpy_macro_method = _generate_nothing
    _loading_cpy_macro = _loaded_noop
    _loaded_cpy_macro = _loaded_noop

    def _generate_cpy_variable_collecttype(self, tp, name):
        if isinstancetpmodel.ArrayType:
            tp_ptr = model.PointerType(tp.item)
        else:
            tp_ptr = model.PointerType(tp)
        self._do_collect_type(tp_ptr)

    def _generate_cpy_variable_decl(self, tp, name):
        if isinstancetpmodel.ArrayType:
            tp_ptr = model.PointerType(tp.item)
            self._generate_cpy_const(False, name, tp, vartp=tp_ptr, size_too=(tp.length_is_unknown))
        else:
            tp_ptr = model.PointerType(tp)
            self._generate_cpy_const(False, name, tp_ptr, category='var')

    _generate_cpy_variable_method = _generate_nothing
    _loading_cpy_variable = _loaded_noop

    def _loaded_cpy_variable--- This code section failed: ---

 L. 774         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'library'
                4  LOAD_FAST                'name'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'value'

 L. 775        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'tp'
               14  LOAD_GLOBAL              model
               16  LOAD_ATTR                ArrayType
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE   176  'to 176'

 L. 777        22  LOAD_FAST                'tp'
               24  LOAD_METHOD              length_is_unknown
               26  CALL_METHOD_0         0  ''
               28  POP_JUMP_IF_FALSE   124  'to 124'

 L. 778        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'value'
               34  LOAD_GLOBAL              tuple
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_TRUE     44  'to 44'
               40  <74>             
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            38  '38'

 L. 779        44  LOAD_FAST                'value'
               46  UNPACK_SEQUENCE_2     2 
               48  STORE_FAST               'value'
               50  STORE_FAST               'size'

 L. 780        52  LOAD_FAST                'self'
               54  LOAD_ATTR                ffi
               56  LOAD_METHOD              _get_cached_btype
               58  LOAD_FAST                'tp'
               60  LOAD_ATTR                item
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'BItemType'

 L. 781        66  LOAD_GLOBAL              divmod
               68  LOAD_FAST                'size'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                ffi
               74  LOAD_METHOD              sizeof
               76  LOAD_FAST                'BItemType'
               78  CALL_METHOD_1         1  ''
               80  CALL_FUNCTION_2       2  ''
               82  UNPACK_SEQUENCE_2     2 
               84  STORE_FAST               'length'
               86  STORE_FAST               'rest'

 L. 782        88  LOAD_FAST                'rest'
               90  LOAD_CONST               0
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   114  'to 114'

 L. 783        96  LOAD_GLOBAL              VerificationError

 L. 784        98  LOAD_STR                 'bad size: %r does not seem to be an array of %s'

 L. 785       100  LOAD_FAST                'name'
              102  LOAD_FAST                'tp'
              104  LOAD_ATTR                item
              106  BUILD_TUPLE_2         2 

 L. 784       108  BINARY_MODULO    

 L. 783       110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM            94  '94'

 L. 786       114  LOAD_FAST                'tp'
              116  LOAD_METHOD              resolve_length
              118  LOAD_FAST                'length'
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'tp'
            124_0  COME_FROM            28  '28'

 L. 789       124  LOAD_FAST                'tp'
              126  LOAD_ATTR                length
              128  LOAD_CONST               None
              130  <117>                 1  ''
              132  POP_JUMP_IF_FALSE   172  'to 172'

 L. 790       134  LOAD_FAST                'self'
              136  LOAD_ATTR                ffi
              138  LOAD_METHOD              _get_cached_btype
              140  LOAD_FAST                'tp'
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'BArray'

 L. 791       146  LOAD_FAST                'self'
              148  LOAD_ATTR                ffi
              150  LOAD_METHOD              cast
              152  LOAD_FAST                'BArray'
              154  LOAD_FAST                'value'
              156  CALL_METHOD_2         2  ''
              158  STORE_FAST               'value'

 L. 792       160  LOAD_GLOBAL              setattr
              162  LOAD_FAST                'library'
              164  LOAD_FAST                'name'
              166  LOAD_FAST                'value'
              168  CALL_FUNCTION_3       3  ''
              170  POP_TOP          
            172_0  COME_FROM           132  '132'

 L. 793       172  LOAD_CONST               None
              174  RETURN_VALUE     
            176_0  COME_FROM            20  '20'

 L. 796       176  LOAD_FAST                'value'
              178  STORE_DEREF              'ptr'

 L. 797       180  LOAD_GLOBAL              delattr
              182  LOAD_FAST                'library'
              184  LOAD_FAST                'name'
              186  CALL_FUNCTION_2       2  ''
              188  POP_TOP          

 L. 798       190  LOAD_CLOSURE             'ptr'
              192  BUILD_TUPLE_1         1 
              194  LOAD_CODE                <code_object getter>
              196  LOAD_STR                 'VCPythonEngine._loaded_cpy_variable.<locals>.getter'
              198  MAKE_FUNCTION_8          'closure'
              200  STORE_FAST               'getter'

 L. 800       202  LOAD_CLOSURE             'ptr'
              204  BUILD_TUPLE_1         1 
              206  LOAD_CODE                <code_object setter>
              208  LOAD_STR                 'VCPythonEngine._loaded_cpy_variable.<locals>.setter'
              210  MAKE_FUNCTION_8          'closure'
              212  STORE_FAST               'setter'

 L. 802       214  LOAD_GLOBAL              setattr
              216  LOAD_GLOBAL              type
              218  LOAD_FAST                'library'
              220  CALL_FUNCTION_1       1  ''
              222  LOAD_FAST                'name'
              224  LOAD_GLOBAL              property
              226  LOAD_FAST                'getter'
              228  LOAD_FAST                'setter'
              230  CALL_FUNCTION_2       2  ''
              232  CALL_FUNCTION_3       3  ''
              234  POP_TOP          

 L. 803       236  LOAD_GLOBAL              type
              238  LOAD_FAST                'library'
              240  CALL_FUNCTION_1       1  ''
              242  LOAD_ATTR                _cffi_dir
              244  LOAD_METHOD              append
              246  LOAD_FAST                'name'
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          

Parse error at or near `<74>' instruction at offset 40

    def _generate_setup_custom(self):
        prnt = self._prnt
        prnt('static int _cffi_setup_custom(PyObject *lib)')
        prnt('{')
        prnt('  return %s;' % self._chained_list_constants[True])
        prnt('}')


cffimod_header = '\n#include <Python.h>\n#include <stddef.h>\n\n/* this block of #ifs should be kept exactly identical between\n   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py\n   and cffi/_cffi_include.h */\n#if defined(_MSC_VER)\n# include <malloc.h>   /* for alloca() */\n# if _MSC_VER < 1600   /* MSVC < 2010 */\n   typedef __int8 int8_t;\n   typedef __int16 int16_t;\n   typedef __int32 int32_t;\n   typedef __int64 int64_t;\n   typedef unsigned __int8 uint8_t;\n   typedef unsigned __int16 uint16_t;\n   typedef unsigned __int32 uint32_t;\n   typedef unsigned __int64 uint64_t;\n   typedef __int8 int_least8_t;\n   typedef __int16 int_least16_t;\n   typedef __int32 int_least32_t;\n   typedef __int64 int_least64_t;\n   typedef unsigned __int8 uint_least8_t;\n   typedef unsigned __int16 uint_least16_t;\n   typedef unsigned __int32 uint_least32_t;\n   typedef unsigned __int64 uint_least64_t;\n   typedef __int8 int_fast8_t;\n   typedef __int16 int_fast16_t;\n   typedef __int32 int_fast32_t;\n   typedef __int64 int_fast64_t;\n   typedef unsigned __int8 uint_fast8_t;\n   typedef unsigned __int16 uint_fast16_t;\n   typedef unsigned __int32 uint_fast32_t;\n   typedef unsigned __int64 uint_fast64_t;\n   typedef __int64 intmax_t;\n   typedef unsigned __int64 uintmax_t;\n# else\n#  include <stdint.h>\n# endif\n# if _MSC_VER < 1800   /* MSVC < 2013 */\n#  ifndef __cplusplus\n    typedef unsigned char _Bool;\n#  endif\n# endif\n#else\n# include <stdint.h>\n# if (defined (__SVR4) && defined (__sun)) || defined(_AIX) || defined(__hpux)\n#  include <alloca.h>\n# endif\n#endif\n\n#if PY_MAJOR_VERSION < 3\n# undef PyCapsule_CheckExact\n# undef PyCapsule_GetPointer\n# define PyCapsule_CheckExact(capsule) (PyCObject_Check(capsule))\n# define PyCapsule_GetPointer(capsule, name) \\\n    (PyCObject_AsVoidPtr(capsule))\n#endif\n\n#if PY_MAJOR_VERSION >= 3\n# define PyInt_FromLong PyLong_FromLong\n#endif\n\n#define _cffi_from_c_double PyFloat_FromDouble\n#define _cffi_from_c_float PyFloat_FromDouble\n#define _cffi_from_c_long PyInt_FromLong\n#define _cffi_from_c_ulong PyLong_FromUnsignedLong\n#define _cffi_from_c_longlong PyLong_FromLongLong\n#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong\n#define _cffi_from_c__Bool PyBool_FromLong\n\n#define _cffi_to_c_double PyFloat_AsDouble\n#define _cffi_to_c_float PyFloat_AsDouble\n\n#define _cffi_from_c_int_const(x)                                        \\\n    (((x) > 0) ?                                                         \\\n        ((unsigned long long)(x) <= (unsigned long long)LONG_MAX) ?      \\\n            PyInt_FromLong((long)(x)) :                                  \\\n            PyLong_FromUnsignedLongLong((unsigned long long)(x)) :       \\\n        ((long long)(x) >= (long long)LONG_MIN) ?                        \\\n            PyInt_FromLong((long)(x)) :                                  \\\n            PyLong_FromLongLong((long long)(x)))\n\n#define _cffi_from_c_int(x, type)                                        \\\n    (((type)-1) > 0 ? /* unsigned */                                     \\\n        (sizeof(type) < sizeof(long) ?                                   \\\n            PyInt_FromLong((long)x) :                                    \\\n         sizeof(type) == sizeof(long) ?                                  \\\n            PyLong_FromUnsignedLong((unsigned long)x) :                  \\\n            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \\\n        (sizeof(type) <= sizeof(long) ?                                  \\\n            PyInt_FromLong((long)x) :                                    \\\n            PyLong_FromLongLong((long long)x)))\n\n#define _cffi_to_c_int(o, type)                                          \\\n    ((type)(                                                             \\\n     sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \\\n                                         : (type)_cffi_to_c_i8(o)) :     \\\n     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \\\n                                         : (type)_cffi_to_c_i16(o)) :    \\\n     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \\\n                                         : (type)_cffi_to_c_i32(o)) :    \\\n     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \\\n                                         : (type)_cffi_to_c_i64(o)) :    \\\n     (Py_FatalError("unsupported size for type " #type), (type)0)))\n\n#define _cffi_to_c_i8                                                    \\\n                 ((int(*)(PyObject *))_cffi_exports[1])\n#define _cffi_to_c_u8                                                    \\\n                 ((int(*)(PyObject *))_cffi_exports[2])\n#define _cffi_to_c_i16                                                   \\\n                 ((int(*)(PyObject *))_cffi_exports[3])\n#define _cffi_to_c_u16                                                   \\\n                 ((int(*)(PyObject *))_cffi_exports[4])\n#define _cffi_to_c_i32                                                   \\\n                 ((int(*)(PyObject *))_cffi_exports[5])\n#define _cffi_to_c_u32                                                   \\\n                 ((unsigned int(*)(PyObject *))_cffi_exports[6])\n#define _cffi_to_c_i64                                                   \\\n                 ((long long(*)(PyObject *))_cffi_exports[7])\n#define _cffi_to_c_u64                                                   \\\n                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])\n#define _cffi_to_c_char                                                  \\\n                 ((int(*)(PyObject *))_cffi_exports[9])\n#define _cffi_from_c_pointer                                             \\\n    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])\n#define _cffi_to_c_pointer                                               \\\n    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])\n#define _cffi_get_struct_layout                                          \\\n    ((PyObject *(*)(Py_ssize_t[]))_cffi_exports[12])\n#define _cffi_restore_errno                                              \\\n    ((void(*)(void))_cffi_exports[13])\n#define _cffi_save_errno                                                 \\\n    ((void(*)(void))_cffi_exports[14])\n#define _cffi_from_c_char                                                \\\n    ((PyObject *(*)(char))_cffi_exports[15])\n#define _cffi_from_c_deref                                               \\\n    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])\n#define _cffi_to_c                                                       \\\n    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])\n#define _cffi_from_c_struct                                              \\\n    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])\n#define _cffi_to_c_wchar_t                                               \\\n    ((wchar_t(*)(PyObject *))_cffi_exports[19])\n#define _cffi_from_c_wchar_t                                             \\\n    ((PyObject *(*)(wchar_t))_cffi_exports[20])\n#define _cffi_to_c_long_double                                           \\\n    ((long double(*)(PyObject *))_cffi_exports[21])\n#define _cffi_to_c__Bool                                                 \\\n    ((_Bool(*)(PyObject *))_cffi_exports[22])\n#define _cffi_prepare_pointer_call_argument                              \\\n    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])\n#define _cffi_convert_array_from_object                                  \\\n    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])\n#define _CFFI_NUM_EXPORTS 25\n\ntypedef struct _ctypedescr CTypeDescrObject;\n\nstatic void *_cffi_exports[_CFFI_NUM_EXPORTS];\nstatic PyObject *_cffi_types, *_cffi_VerificationError;\n\nstatic int _cffi_setup_custom(PyObject *lib);   /* forward */\n\nstatic PyObject *_cffi_setup(PyObject *self, PyObject *args)\n{\n    PyObject *library;\n    int was_alive = (_cffi_types != NULL);\n    (void)self; /* unused */\n    if (!PyArg_ParseTuple(args, "OOO", &_cffi_types, &_cffi_VerificationError,\n                                       &library))\n        return NULL;\n    Py_INCREF(_cffi_types);\n    Py_INCREF(_cffi_VerificationError);\n    if (_cffi_setup_custom(library) < 0)\n        return NULL;\n    return PyBool_FromLong(was_alive);\n}\n\nunion _cffi_union_alignment_u {\n    unsigned char m_char;\n    unsigned short m_short;\n    unsigned int m_int;\n    unsigned long m_long;\n    unsigned long long m_longlong;\n    float m_float;\n    double m_double;\n    long double m_longdouble;\n};\n\nstruct _cffi_freeme_s {\n    struct _cffi_freeme_s *next;\n    union _cffi_union_alignment_u alignment;\n};\n\n#ifdef __GNUC__\n  __attribute__((unused))\n#endif\nstatic int _cffi_convert_array_argument(CTypeDescrObject *ctptr, PyObject *arg,\n                                        char **output_data, Py_ssize_t datasize,\n                                        struct _cffi_freeme_s **freeme)\n{\n    char *p;\n    if (datasize < 0)\n        return -1;\n\n    p = *output_data;\n    if (p == NULL) {\n        struct _cffi_freeme_s *fp = (struct _cffi_freeme_s *)PyObject_Malloc(\n            offsetof(struct _cffi_freeme_s, alignment) + (size_t)datasize);\n        if (fp == NULL)\n            return -1;\n        fp->next = *freeme;\n        *freeme = fp;\n        p = *output_data = (char *)&fp->alignment;\n    }\n    memset((void *)p, 0, (size_t)datasize);\n    return _cffi_convert_array_from_object(p, ctptr, arg);\n}\n\n#ifdef __GNUC__\n  __attribute__((unused))\n#endif\nstatic void _cffi_free_array_arguments(struct _cffi_freeme_s *freeme)\n{\n    do {\n        void *p = (void *)freeme;\n        freeme = freeme->next;\n        PyObject_Free(p);\n    } while (freeme != NULL);\n}\n\nstatic int _cffi_init(void)\n{\n    PyObject *module, *c_api_object = NULL;\n\n    module = PyImport_ImportModule("_cffi_backend");\n    if (module == NULL)\n        goto failure;\n\n    c_api_object = PyObject_GetAttrString(module, "_C_API");\n    if (c_api_object == NULL)\n        goto failure;\n    if (!PyCapsule_CheckExact(c_api_object)) {\n        PyErr_SetNone(PyExc_ImportError);\n        goto failure;\n    }\n    memcpy(_cffi_exports, PyCapsule_GetPointer(c_api_object, "cffi"),\n           _CFFI_NUM_EXPORTS * sizeof(void *));\n\n    Py_DECREF(module);\n    Py_DECREF(c_api_object);\n    return 0;\n\n  failure:\n    Py_XDECREF(module);\n    Py_XDECREF(c_api_object);\n    return -1;\n}\n\n#define _cffi_type(num) ((CTypeDescrObject *)PyList_GET_ITEM(_cffi_types, num))\n\n/**********/\n'