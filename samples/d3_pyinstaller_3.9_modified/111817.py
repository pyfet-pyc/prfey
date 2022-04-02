# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cffi\vengine_gen.py
import sys, os, types
from . import model
from .error import VerificationError

class VGenericEngine(object):
    _class_key = 'g'
    _gen_python_module = False

    def __init__(self, verifier):
        self.verifier = verifier
        self.ffi = verifier.ffi
        self.export_symbols = []
        self._struct_pending_verification = {}

    def patch_extension_kwds(self, kwds):
        kwds.setdefault('export_symbols', self.export_symbols)

    def find_module--- This code section failed: ---

 L.  28         0  LOAD_FAST                'so_suffixes'
                2  GET_ITER         
              4_0  COME_FROM            78  '78'
                4  FOR_ITER             80  'to 80'
                6  STORE_FAST               'so_suffix'

 L.  29         8  LOAD_FAST                'module_name'
               10  LOAD_FAST                'so_suffix'
               12  BINARY_ADD       
               14  STORE_FAST               'basename'

 L.  30        16  LOAD_FAST                'path'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L.  31        24  LOAD_GLOBAL              sys
               26  LOAD_ATTR                path
               28  STORE_FAST               'path'
             30_0  COME_FROM            22  '22'

 L.  32        30  LOAD_FAST                'path'
               32  GET_ITER         
             34_0  COME_FROM            76  '76'
             34_1  COME_FROM            62  '62'
               34  FOR_ITER             78  'to 78'
               36  STORE_FAST               'dirname'

 L.  33        38  LOAD_GLOBAL              os
               40  LOAD_ATTR                path
               42  LOAD_METHOD              join
               44  LOAD_FAST                'dirname'
               46  LOAD_FAST                'basename'
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'filename'

 L.  34        52  LOAD_GLOBAL              os
               54  LOAD_ATTR                path
               56  LOAD_METHOD              isfile
               58  LOAD_FAST                'filename'
               60  CALL_METHOD_1         1  ''
               62  POP_JUMP_IF_FALSE_BACK    34  'to 34'

 L.  35        64  LOAD_FAST                'filename'
               66  ROT_TWO          
               68  POP_TOP          
               70  ROT_TWO          
               72  POP_TOP          
               74  RETURN_VALUE     
               76  JUMP_BACK            34  'to 34'
             78_0  COME_FROM            34  '34'
               78  JUMP_BACK             4  'to 4'
             80_0  COME_FROM             4  '4'

Parse error at or near `<117>' instruction at offset 20

    def collect_types(self):
        pass

    def _prnt(self, what=''):
        self._f.write(what + '\n')

    def write_source_to_f(self):
        prnt = self._prnt
        prnt(cffimod_header)
        prnt(self.verifier.preamble)
        self._generate'decl'
        if sys.platform == 'win32':
            if sys.version_info >= (3, ):
                prefix = 'PyInit_'
            else:
                prefix = 'init'
            modname = self.verifier.get_module_name()
            prnt('void %s%s(void) { }\n' % (prefix, modname))

    def load_library(self, flags=0):
        backend = self.ffi._backend
        filename = os.path.join(os.curdir, self.verifier.modulefilename)
        module = backend.load_library(filename, flags)
        self._load(module, 'loading')

        class FFILibrary(types.ModuleType):
            _cffi_generic_module = module
            _cffi_ffi = self.ffi
            _cffi_dir = []

            def __dir__(self):
                return FFILibrary._cffi_dir

        library = FFILibrary('')
        self._load(module, 'loaded', library=library)
        return library

    def _get_declarations(self):
        lst = [(key, tp) for key, (tp, qual) in self.ffi._parser._declarations.items()]
        lst.sort()
        return lst

    def _generate--- This code section failed: ---

 L. 100         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_declarations
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
              8_0  COME_FROM           152  '152'
              8_1  COME_FROM           140  '140'
              8_2  COME_FROM           100  '100'
                8  FOR_ITER            154  'to 154'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'name'
               14  STORE_FAST               'tp'

 L. 101        16  LOAD_FAST                'name'
               18  LOAD_METHOD              split
               20  LOAD_STR                 ' '
               22  LOAD_CONST               1
               24  CALL_METHOD_2         2  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'kind'
               30  STORE_FAST               'realname'

 L. 102        32  SETUP_FINALLY        56  'to 56'

 L. 103        34  LOAD_GLOBAL              getattr
               36  LOAD_FAST                'self'
               38  LOAD_STR                 '_generate_gen_%s_%s'
               40  LOAD_FAST                'kind'

 L. 104        42  LOAD_FAST                'step_name'

 L. 103        44  BUILD_TUPLE_2         2 
               46  BINARY_MODULO    
               48  CALL_FUNCTION_2       2  ''
               50  STORE_FAST               'method'
               52  POP_BLOCK        
               54  JUMP_FORWARD         86  'to 86'
             56_0  COME_FROM_FINALLY    32  '32'

 L. 105        56  DUP_TOP          
               58  LOAD_GLOBAL              AttributeError
               60  <121>                84  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 106        68  LOAD_GLOBAL              VerificationError

 L. 107        70  LOAD_STR                 'not implemented in verify(): %r'
               72  LOAD_FAST                'name'
               74  BINARY_MODULO    

 L. 106        76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            54  '54'

 L. 108        86  SETUP_FINALLY       102  'to 102'

 L. 109        88  LOAD_FAST                'method'
               90  LOAD_FAST                'tp'
               92  LOAD_FAST                'realname'
               94  CALL_FUNCTION_2       2  ''
               96  POP_TOP          
               98  POP_BLOCK        
              100  JUMP_BACK             8  'to 8'
            102_0  COME_FROM_FINALLY    86  '86'

 L. 110       102  DUP_TOP          
              104  LOAD_GLOBAL              Exception
              106  <121>               150  ''
              108  POP_TOP          
              110  STORE_FAST               'e'
              112  POP_TOP          
              114  SETUP_FINALLY       142  'to 142'

 L. 111       116  LOAD_GLOBAL              model
              118  LOAD_METHOD              attach_exception_info
              120  LOAD_FAST                'e'
              122  LOAD_FAST                'name'
              124  CALL_METHOD_2         2  ''
              126  POP_TOP          

 L. 112       128  RAISE_VARARGS_0       0  'reraise'
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
            154_0  COME_FROM             8  '8'

Parse error at or near `<121>' instruction at offset 60

    def _load--- This code section failed: ---

 L. 115         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_declarations
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
              8_0  COME_FROM           126  '126'
              8_1  COME_FROM           114  '114'
              8_2  COME_FROM            74  '74'
                8  FOR_ITER            128  'to 128'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'name'
               14  STORE_FAST               'tp'

 L. 116        16  LOAD_FAST                'name'
               18  LOAD_METHOD              split
               20  LOAD_STR                 ' '
               22  LOAD_CONST               1
               24  CALL_METHOD_2         2  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'kind'
               30  STORE_FAST               'realname'

 L. 117        32  LOAD_GLOBAL              getattr
               34  LOAD_FAST                'self'
               36  LOAD_STR                 '_%s_gen_%s'
               38  LOAD_FAST                'step_name'
               40  LOAD_FAST                'kind'
               42  BUILD_TUPLE_2         2 
               44  BINARY_MODULO    
               46  CALL_FUNCTION_2       2  ''
               48  STORE_FAST               'method'

 L. 118        50  SETUP_FINALLY        76  'to 76'

 L. 119        52  LOAD_FAST                'method'
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

 L. 120        76  DUP_TOP          
               78  LOAD_GLOBAL              Exception
               80  <121>               124  ''
               82  POP_TOP          
               84  STORE_FAST               'e'
               86  POP_TOP          
               88  SETUP_FINALLY       116  'to 116'

 L. 121        90  LOAD_GLOBAL              model
               92  LOAD_METHOD              attach_exception_info
               94  LOAD_FAST                'e'
               96  LOAD_FAST                'name'
               98  CALL_METHOD_2         2  ''
              100  POP_TOP          

 L. 122       102  RAISE_VARARGS_0       0  'reraise'
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
            128_0  COME_FROM             8  '8'

Parse error at or near `<164>' instruction at offset 66

    def _generate_nothing(self, tp, name):
        pass

    def _loaded_noop(self, tp, name, module, **kwds):
        pass

    _generate_gen_typedef_decl = _generate_nothing
    _loading_gen_typedef = _loaded_noop
    _loaded_gen_typedef = _loaded_noop

    def _generate_gen_function_decl--- This code section failed: ---

 L. 141         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                FunctionPtrType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 142        16  LOAD_FAST                'tp'
               18  LOAD_ATTR                ellipsis
               20  POP_JUMP_IF_FALSE    40  'to 40'

 L. 146        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _generate_gen_const
               26  LOAD_CONST               False
               28  LOAD_FAST                'name'
               30  LOAD_FAST                'tp'
               32  CALL_METHOD_3         3  ''
               34  POP_TOP          

 L. 147        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            20  '20'

 L. 148        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _prnt
               44  STORE_FAST               'prnt'

 L. 149        46  LOAD_GLOBAL              len
               48  LOAD_FAST                'tp'
               50  LOAD_ATTR                args
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'numargs'

 L. 150        56  BUILD_LIST_0          0 
               58  STORE_FAST               'argnames'

 L. 151        60  LOAD_GLOBAL              enumerate
               62  LOAD_FAST                'tp'
               64  LOAD_ATTR                args
               66  CALL_FUNCTION_1       1  ''
               68  GET_ITER         
             70_0  COME_FROM           116  '116'
               70  FOR_ITER            118  'to 118'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'i'
               76  STORE_FAST               'type'

 L. 152        78  LOAD_STR                 ''
               80  STORE_FAST               'indirection'

 L. 153        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'type'
               86  LOAD_GLOBAL              model
               88  LOAD_ATTR                StructOrUnion
               90  CALL_FUNCTION_2       2  ''
               92  POP_JUMP_IF_FALSE    98  'to 98'

 L. 154        94  LOAD_STR                 '*'
               96  STORE_FAST               'indirection'
             98_0  COME_FROM            92  '92'

 L. 155        98  LOAD_FAST                'argnames'
              100  LOAD_METHOD              append
              102  LOAD_STR                 '%sx%d'
              104  LOAD_FAST                'indirection'
              106  LOAD_FAST                'i'
              108  BUILD_TUPLE_2         2 
              110  BINARY_MODULO    
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  JUMP_BACK            70  'to 70'
            118_0  COME_FROM            70  '70'

 L. 156       118  LOAD_STR                 'argument of %s'
              120  LOAD_FAST                'name'
              122  BINARY_MODULO    
              124  STORE_DEREF              'context'

 L. 157       126  LOAD_CLOSURE             'context'
              128  BUILD_TUPLE_1         1 
              130  LOAD_LISTCOMP            '<code_object <listcomp>>'
              132  LOAD_STR                 'VGenericEngine._generate_gen_function_decl.<locals>.<listcomp>'
              134  MAKE_FUNCTION_8          'closure'

 L. 158       136  LOAD_GLOBAL              zip
              138  LOAD_FAST                'tp'
              140  LOAD_ATTR                args
              142  LOAD_FAST                'argnames'
              144  CALL_FUNCTION_2       2  ''

 L. 157       146  GET_ITER         
              148  CALL_FUNCTION_1       1  ''
              150  STORE_FAST               'arglist'

 L. 159       152  LOAD_FAST                'tp'
              154  LOAD_ATTR                result
              156  STORE_FAST               'tpresult'

 L. 160       158  LOAD_GLOBAL              isinstance
              160  LOAD_FAST                'tpresult'
              162  LOAD_GLOBAL              model
              164  LOAD_ATTR                StructOrUnion
              166  CALL_FUNCTION_2       2  ''
              168  POP_JUMP_IF_FALSE   196  'to 196'

 L. 161       170  LOAD_FAST                'arglist'
              172  LOAD_METHOD              insert
              174  LOAD_CONST               0
              176  LOAD_FAST                'tpresult'
              178  LOAD_METHOD              get_c_name
              180  LOAD_STR                 ' *r'
              182  LOAD_DEREF               'context'
              184  CALL_METHOD_2         2  ''
              186  CALL_METHOD_2         2  ''
              188  POP_TOP          

 L. 162       190  LOAD_GLOBAL              model
              192  LOAD_ATTR                void_type
              194  STORE_FAST               'tpresult'
            196_0  COME_FROM           168  '168'

 L. 163       196  LOAD_STR                 ', '
              198  LOAD_METHOD              join
              200  LOAD_FAST                'arglist'
              202  CALL_METHOD_1         1  ''
              204  JUMP_IF_TRUE_OR_POP   208  'to 208'
              206  LOAD_STR                 'void'
            208_0  COME_FROM           204  '204'
              208  STORE_FAST               'arglist'

 L. 164       210  LOAD_STR                 '_cffi_f_%s'
              212  LOAD_FAST                'name'
              214  BINARY_MODULO    
              216  STORE_FAST               'wrappername'

 L. 165       218  LOAD_FAST                'self'
              220  LOAD_ATTR                export_symbols
              222  LOAD_METHOD              append
              224  LOAD_FAST                'wrappername'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 166       230  LOAD_FAST                'tp'
              232  LOAD_ATTR                abi
              234  POP_JUMP_IF_FALSE   248  'to 248'

 L. 167       236  LOAD_FAST                'tp'
              238  LOAD_ATTR                abi
              240  LOAD_STR                 ' '
              242  BINARY_ADD       
              244  STORE_FAST               'abi'
              246  JUMP_FORWARD        252  'to 252'
            248_0  COME_FROM           234  '234'

 L. 169       248  LOAD_STR                 ''
              250  STORE_FAST               'abi'
            252_0  COME_FROM           246  '246'

 L. 170       252  LOAD_STR                 ' %s%s(%s)'
              254  LOAD_FAST                'abi'
              256  LOAD_FAST                'wrappername'
              258  LOAD_FAST                'arglist'
              260  BUILD_TUPLE_3         3 
              262  BINARY_MODULO    
              264  STORE_FAST               'funcdecl'

 L. 171       266  LOAD_STR                 'result of %s'
              268  LOAD_FAST                'name'
              270  BINARY_MODULO    
              272  STORE_DEREF              'context'

 L. 172       274  LOAD_FAST                'prnt'
              276  LOAD_FAST                'tpresult'
              278  LOAD_METHOD              get_c_name
              280  LOAD_FAST                'funcdecl'
              282  LOAD_DEREF               'context'
              284  CALL_METHOD_2         2  ''
              286  CALL_FUNCTION_1       1  ''
              288  POP_TOP          

 L. 173       290  LOAD_FAST                'prnt'
              292  LOAD_STR                 '{'
              294  CALL_FUNCTION_1       1  ''
              296  POP_TOP          

 L. 175       298  LOAD_GLOBAL              isinstance
              300  LOAD_FAST                'tp'
              302  LOAD_ATTR                result
              304  LOAD_GLOBAL              model
              306  LOAD_ATTR                StructOrUnion
              308  CALL_FUNCTION_2       2  ''
          310_312  POP_JUMP_IF_FALSE   320  'to 320'

 L. 176       314  LOAD_STR                 '*r = '
              316  STORE_FAST               'result_code'
              318  JUMP_FORWARD        346  'to 346'
            320_0  COME_FROM           310  '310'

 L. 177       320  LOAD_GLOBAL              isinstance
              322  LOAD_FAST                'tp'
              324  LOAD_ATTR                result
              326  LOAD_GLOBAL              model
              328  LOAD_ATTR                VoidType
              330  CALL_FUNCTION_2       2  ''
          332_334  POP_JUMP_IF_TRUE    342  'to 342'

 L. 178       336  LOAD_STR                 'return '
              338  STORE_FAST               'result_code'
              340  JUMP_FORWARD        346  'to 346'
            342_0  COME_FROM           332  '332'

 L. 180       342  LOAD_STR                 ''
              344  STORE_FAST               'result_code'
            346_0  COME_FROM           340  '340'
            346_1  COME_FROM           318  '318'

 L. 181       346  LOAD_FAST                'prnt'
              348  LOAD_STR                 '  %s%s(%s);'
              350  LOAD_FAST                'result_code'
              352  LOAD_FAST                'name'
              354  LOAD_STR                 ', '
              356  LOAD_METHOD              join
              358  LOAD_FAST                'argnames'
              360  CALL_METHOD_1         1  ''
              362  BUILD_TUPLE_3         3 
              364  BINARY_MODULO    
              366  CALL_FUNCTION_1       1  ''
              368  POP_TOP          

 L. 182       370  LOAD_FAST                'prnt'
              372  LOAD_STR                 '}'
              374  CALL_FUNCTION_1       1  ''
              376  POP_TOP          

 L. 183       378  LOAD_FAST                'prnt'
              380  CALL_FUNCTION_0       0  ''
              382  POP_TOP          

Parse error at or near `None' instruction at offset -1

    _loading_gen_function = _loaded_noop

    def _loaded_gen_function--- This code section failed: ---

 L. 188         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                FunctionPtrType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 189        16  LOAD_FAST                'tp'
               18  LOAD_ATTR                ellipsis
               20  POP_JUMP_IF_FALSE    42  'to 42'

 L. 190        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _load_constant
               26  LOAD_CONST               False
               28  LOAD_FAST                'tp'
               30  LOAD_FAST                'name'
               32  LOAD_FAST                'module'
               34  CALL_METHOD_4         4  ''
               36  STORE_FAST               'newfunction'
            38_40  JUMP_FORWARD        330  'to 330'
             42_0  COME_FROM            20  '20'

 L. 192        42  BUILD_LIST_0          0 
               44  STORE_FAST               'indirections'

 L. 193        46  LOAD_FAST                'tp'
               48  STORE_FAST               'base_tp'

 L. 194        50  LOAD_GLOBAL              any
               52  LOAD_GENEXPR             '<code_object <genexpr>>'
               54  LOAD_STR                 'VGenericEngine._loaded_gen_function.<locals>.<genexpr>'
               56  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               58  LOAD_FAST                'tp'
               60  LOAD_ATTR                args
               62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  CALL_FUNCTION_1       1  ''
               68  POP_JUMP_IF_TRUE     86  'to 86'

 L. 195        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'tp'
               74  LOAD_ATTR                result
               76  LOAD_GLOBAL              model
               78  LOAD_ATTR                StructOrUnion
               80  CALL_FUNCTION_2       2  ''

 L. 194     82_84  POP_JUMP_IF_FALSE   266  'to 266'
             86_0  COME_FROM            68  '68'

 L. 196        86  BUILD_LIST_0          0 
               88  STORE_FAST               'indirect_args'

 L. 197        90  LOAD_GLOBAL              enumerate
               92  LOAD_FAST                'tp'
               94  LOAD_ATTR                args
               96  CALL_FUNCTION_1       1  ''
               98  GET_ITER         
            100_0  COME_FROM           154  '154'
              100  FOR_ITER            156  'to 156'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'i'
              106  STORE_FAST               'typ'

 L. 198       108  LOAD_GLOBAL              isinstance
              110  LOAD_FAST                'typ'
              112  LOAD_GLOBAL              model
              114  LOAD_ATTR                StructOrUnion
              116  CALL_FUNCTION_2       2  ''
              118  POP_JUMP_IF_FALSE   144  'to 144'

 L. 199       120  LOAD_GLOBAL              model
              122  LOAD_METHOD              PointerType
              124  LOAD_FAST                'typ'
              126  CALL_METHOD_1         1  ''
              128  STORE_FAST               'typ'

 L. 200       130  LOAD_FAST                'indirections'
              132  LOAD_METHOD              append
              134  LOAD_FAST                'i'
              136  LOAD_FAST                'typ'
              138  BUILD_TUPLE_2         2 
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           118  '118'

 L. 201       144  LOAD_FAST                'indirect_args'
              146  LOAD_METHOD              append
              148  LOAD_FAST                'typ'
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
              154  JUMP_BACK           100  'to 100'
            156_0  COME_FROM           100  '100'

 L. 202       156  LOAD_FAST                'tp'
              158  LOAD_ATTR                result
              160  STORE_FAST               'indirect_result'

 L. 203       162  LOAD_GLOBAL              isinstance
              164  LOAD_FAST                'indirect_result'
              166  LOAD_GLOBAL              model
              168  LOAD_ATTR                StructOrUnion
              170  CALL_FUNCTION_2       2  ''
              172  POP_JUMP_IF_FALSE   246  'to 246'

 L. 204       174  LOAD_FAST                'indirect_result'
              176  LOAD_ATTR                fldtypes
              178  LOAD_CONST               None
              180  <117>                 0  ''
              182  POP_JUMP_IF_FALSE   202  'to 202'

 L. 205       184  LOAD_GLOBAL              TypeError
              186  LOAD_STR                 "'%s' is used as result type, but is opaque"

 L. 207       188  LOAD_FAST                'indirect_result'
              190  LOAD_METHOD              _get_c_name
              192  CALL_METHOD_0         0  ''

 L. 206       194  BUILD_TUPLE_1         1 

 L. 205       196  BINARY_MODULO    
              198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  'exception instance'
            202_0  COME_FROM           182  '182'

 L. 208       202  LOAD_GLOBAL              model
              204  LOAD_METHOD              PointerType
              206  LOAD_FAST                'indirect_result'
              208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'indirect_result'

 L. 209       212  LOAD_FAST                'indirect_args'
              214  LOAD_METHOD              insert
              216  LOAD_CONST               0
              218  LOAD_FAST                'indirect_result'
              220  CALL_METHOD_2         2  ''
              222  POP_TOP          

 L. 210       224  LOAD_FAST                'indirections'
              226  LOAD_METHOD              insert
              228  LOAD_CONST               0
              230  LOAD_STR                 'result'
              232  LOAD_FAST                'indirect_result'
              234  BUILD_TUPLE_2         2 
              236  CALL_METHOD_2         2  ''
              238  POP_TOP          

 L. 211       240  LOAD_GLOBAL              model
              242  LOAD_ATTR                void_type
              244  STORE_FAST               'indirect_result'
            246_0  COME_FROM           172  '172'

 L. 212       246  LOAD_GLOBAL              model
              248  LOAD_METHOD              FunctionPtrType
              250  LOAD_GLOBAL              tuple
              252  LOAD_FAST                'indirect_args'
              254  CALL_FUNCTION_1       1  ''

 L. 213       256  LOAD_FAST                'indirect_result'
              258  LOAD_FAST                'tp'
              260  LOAD_ATTR                ellipsis

 L. 212       262  CALL_METHOD_3         3  ''
              264  STORE_FAST               'tp'
            266_0  COME_FROM            82  '82'

 L. 214       266  LOAD_FAST                'self'
              268  LOAD_ATTR                ffi
              270  LOAD_METHOD              _get_cached_btype
              272  LOAD_FAST                'tp'
              274  CALL_METHOD_1         1  ''
              276  STORE_FAST               'BFunc'

 L. 215       278  LOAD_STR                 '_cffi_f_%s'
              280  LOAD_FAST                'name'
              282  BINARY_MODULO    
              284  STORE_FAST               'wrappername'

 L. 216       286  LOAD_FAST                'module'
              288  LOAD_METHOD              load_function
              290  LOAD_FAST                'BFunc'
              292  LOAD_FAST                'wrappername'
              294  CALL_METHOD_2         2  ''
              296  STORE_FAST               'newfunction'

 L. 217       298  LOAD_FAST                'indirections'
              300  GET_ITER         
            302_0  COME_FROM           326  '326'
              302  FOR_ITER            330  'to 330'
              304  UNPACK_SEQUENCE_2     2 
              306  STORE_FAST               'i'
              308  STORE_FAST               'typ'

 L. 218       310  LOAD_FAST                'self'
              312  LOAD_METHOD              _make_struct_wrapper
              314  LOAD_FAST                'newfunction'
              316  LOAD_FAST                'i'
              318  LOAD_FAST                'typ'

 L. 219       320  LOAD_FAST                'base_tp'

 L. 218       322  CALL_METHOD_4         4  ''
              324  STORE_FAST               'newfunction'
          326_328  JUMP_BACK           302  'to 302'
            330_0  COME_FROM           302  '302'
            330_1  COME_FROM            38  '38'

 L. 220       330  LOAD_GLOBAL              setattr
              332  LOAD_FAST                'library'
              334  LOAD_FAST                'name'
              336  LOAD_FAST                'newfunction'
              338  CALL_FUNCTION_3       3  ''
              340  POP_TOP          

 L. 221       342  LOAD_GLOBAL              type
              344  LOAD_FAST                'library'
              346  CALL_FUNCTION_1       1  ''
              348  LOAD_ATTR                _cffi_dir
              350  LOAD_METHOD              append
              352  LOAD_FAST                'name'
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _make_struct_wrapper(self, oldfunc, i, tp, base_tp):
        backend = self.ffi._backend
        BType = self.ffi._get_cached_btypetp
        if i == 'result':
            ffi = self.ffi

            def newfunc--- This code section failed: ---

 L. 229         0  LOAD_DEREF               'ffi'
                2  LOAD_METHOD              new
                4  LOAD_DEREF               'BType'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'res'

 L. 230        10  LOAD_DEREF               'oldfunc'
               12  LOAD_FAST                'res'
               14  BUILD_LIST_1          1 
               16  LOAD_FAST                'args'
               18  CALL_FINALLY         21  'to 21'
               20  WITH_CLEANUP_FINISH
               22  CALL_FUNCTION_EX      0  'positional arguments only'
               24  POP_TOP          

 L. 231        26  LOAD_FAST                'res'
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 18

        else:

            def newfunc(*args):
                args = args[:i] + (backend.newp(BType, args[i]),) + args[i + 1:]
                return oldfunc(*args)

        newfunc._cffi_base_type = base_tp
        return newfunc

    def _generate_gen_struct_decl--- This code section failed: ---

 L. 243         0  LOAD_FAST                'name'
                2  LOAD_FAST                'tp'
                4  LOAD_ATTR                name
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 244        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _generate_struct_or_union_decl
               18  LOAD_FAST                'tp'
               20  LOAD_STR                 'struct'
               22  LOAD_FAST                'name'
               24  CALL_METHOD_3         3  ''
               26  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _loading_gen_struct(self, tp, name, module):
        self._loading_struct_or_uniontp'struct'namemodule

    def _loaded_gen_struct(self, tp, name, module, **kwds):
        self._loaded_struct_or_uniontp

    def _generate_gen_union_decl--- This code section failed: ---

 L. 253         0  LOAD_FAST                'name'
                2  LOAD_FAST                'tp'
                4  LOAD_ATTR                name
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 254        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _generate_struct_or_union_decl
               18  LOAD_FAST                'tp'
               20  LOAD_STR                 'union'
               22  LOAD_FAST                'name'
               24  CALL_METHOD_3         3  ''
               26  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _loading_gen_union(self, tp, name, module):
        self._loading_struct_or_uniontp'union'namemodule

    def _loaded_gen_union(self, tp, name, module, **kwds):
        self._loaded_struct_or_uniontp

    def _generate_struct_or_union_decl--- This code section failed: ---

 L. 263         0  LOAD_FAST                'tp'
                2  LOAD_ATTR                fldnames
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 264        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 265        14  LOAD_STR                 '_cffi_check_%s_%s'
               16  LOAD_FAST                'prefix'
               18  LOAD_FAST                'name'
               20  BUILD_TUPLE_2         2 
               22  BINARY_MODULO    
               24  STORE_FAST               'checkfuncname'

 L. 266        26  LOAD_STR                 '_cffi_layout_%s_%s'
               28  LOAD_FAST                'prefix'
               30  LOAD_FAST                'name'
               32  BUILD_TUPLE_2         2 
               34  BINARY_MODULO    
               36  STORE_FAST               'layoutfuncname'

 L. 267        38  LOAD_STR                 '%s %s'
               40  LOAD_FAST                'prefix'
               42  LOAD_FAST                'name'
               44  BUILD_TUPLE_2         2 
               46  BINARY_MODULO    
               48  LOAD_METHOD              strip
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'cname'

 L. 269        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _prnt
               58  STORE_FAST               'prnt'

 L. 270        60  LOAD_FAST                'prnt'
               62  LOAD_STR                 'static void %s(%s *p)'
               64  LOAD_FAST                'checkfuncname'
               66  LOAD_FAST                'cname'
               68  BUILD_TUPLE_2         2 
               70  BINARY_MODULO    
               72  CALL_FUNCTION_1       1  ''
               74  POP_TOP          

 L. 271        76  LOAD_FAST                'prnt'
               78  LOAD_STR                 '{'
               80  CALL_FUNCTION_1       1  ''
               82  POP_TOP          

 L. 272        84  LOAD_FAST                'prnt'
               86  LOAD_STR                 '  /* only to generate compile-time warnings or errors */'
               88  CALL_FUNCTION_1       1  ''
               90  POP_TOP          

 L. 273        92  LOAD_FAST                'prnt'
               94  LOAD_STR                 '  (void)p;'
               96  CALL_FUNCTION_1       1  ''
               98  POP_TOP          

 L. 274       100  LOAD_FAST                'tp'
              102  LOAD_METHOD              enumfields
              104  CALL_METHOD_0         0  ''
              106  GET_ITER         
            108_0  COME_FROM           252  '252'
            108_1  COME_FROM           240  '240'
            108_2  COME_FROM           198  '198'
            108_3  COME_FROM           160  '160'
              108  FOR_ITER            254  'to 254'
              110  UNPACK_SEQUENCE_4     4 
              112  STORE_FAST               'fname'
              114  STORE_FAST               'ftype'
              116  STORE_FAST               'fbitsize'
              118  STORE_FAST               'fqual'

 L. 275       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'ftype'
              124  LOAD_GLOBAL              model
              126  LOAD_ATTR                PrimitiveType
              128  CALL_FUNCTION_2       2  ''
              130  POP_JUMP_IF_FALSE   140  'to 140'

 L. 276       132  LOAD_FAST                'ftype'
              134  LOAD_METHOD              is_integer_type
              136  CALL_METHOD_0         0  ''

 L. 275       138  POP_JUMP_IF_TRUE    148  'to 148'
            140_0  COME_FROM           130  '130'

 L. 276       140  LOAD_FAST                'fbitsize'
              142  LOAD_CONST               0
              144  COMPARE_OP               >=

 L. 275       146  POP_JUMP_IF_FALSE   162  'to 162'
            148_0  COME_FROM           138  '138'

 L. 278       148  LOAD_FAST                'prnt'
              150  LOAD_STR                 '  (void)((p->%s) << 1);'
              152  LOAD_FAST                'fname'
              154  BINARY_MODULO    
              156  CALL_FUNCTION_1       1  ''
              158  POP_TOP          
              160  JUMP_BACK           108  'to 108'
            162_0  COME_FROM           146  '146'

 L. 281       162  SETUP_FINALLY       200  'to 200'

 L. 282       164  LOAD_FAST                'prnt'
              166  LOAD_STR                 '  { %s = &p->%s; (void)tmp; }'

 L. 283       168  LOAD_FAST                'ftype'
              170  LOAD_ATTR                get_c_name
              172  LOAD_STR                 '*tmp'
              174  LOAD_STR                 'field %r'
              176  LOAD_FAST                'fname'
              178  BINARY_MODULO    
              180  LOAD_FAST                'fqual'
              182  LOAD_CONST               ('quals',)
              184  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 284       186  LOAD_FAST                'fname'

 L. 282       188  BUILD_TUPLE_2         2 
              190  BINARY_MODULO    
              192  CALL_FUNCTION_1       1  ''
              194  POP_TOP          
              196  POP_BLOCK        
              198  JUMP_BACK           108  'to 108'
            200_0  COME_FROM_FINALLY   162  '162'

 L. 285       200  DUP_TOP          
              202  LOAD_GLOBAL              VerificationError
              204  <121>               250  ''
              206  POP_TOP          
              208  STORE_FAST               'e'
              210  POP_TOP          
              212  SETUP_FINALLY       242  'to 242'

 L. 286       214  LOAD_FAST                'prnt'
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
            254_0  COME_FROM           108  '108'

 L. 287       254  LOAD_FAST                'prnt'
              256  LOAD_STR                 '}'
              258  CALL_FUNCTION_1       1  ''
              260  POP_TOP          

 L. 288       262  LOAD_FAST                'self'
              264  LOAD_ATTR                export_symbols
              266  LOAD_METHOD              append
              268  LOAD_FAST                'layoutfuncname'
              270  CALL_METHOD_1         1  ''
              272  POP_TOP          

 L. 289       274  LOAD_FAST                'prnt'
              276  LOAD_STR                 'intptr_t %s(intptr_t i)'
              278  LOAD_FAST                'layoutfuncname'
              280  BUILD_TUPLE_1         1 
              282  BINARY_MODULO    
              284  CALL_FUNCTION_1       1  ''
              286  POP_TOP          

 L. 290       288  LOAD_FAST                'prnt'
              290  LOAD_STR                 '{'
              292  CALL_FUNCTION_1       1  ''
              294  POP_TOP          

 L. 291       296  LOAD_FAST                'prnt'
              298  LOAD_STR                 '  struct _cffi_aligncheck { char x; %s y; };'
              300  LOAD_FAST                'cname'
              302  BINARY_MODULO    
              304  CALL_FUNCTION_1       1  ''
              306  POP_TOP          

 L. 292       308  LOAD_FAST                'prnt'
              310  LOAD_STR                 '  static intptr_t nums[] = {'
              312  CALL_FUNCTION_1       1  ''
              314  POP_TOP          

 L. 293       316  LOAD_FAST                'prnt'
              318  LOAD_STR                 '    sizeof(%s),'
              320  LOAD_FAST                'cname'
              322  BINARY_MODULO    
              324  CALL_FUNCTION_1       1  ''
              326  POP_TOP          

 L. 294       328  LOAD_FAST                'prnt'
              330  LOAD_STR                 '    offsetof(struct _cffi_aligncheck, y),'
              332  CALL_FUNCTION_1       1  ''
              334  POP_TOP          

 L. 295       336  LOAD_FAST                'tp'
              338  LOAD_METHOD              enumfields
              340  CALL_METHOD_0         0  ''
              342  GET_ITER         
            344_0  COME_FROM           446  '446'
            344_1  COME_FROM           428  '428'
            344_2  COME_FROM           366  '366'
              344  FOR_ITER            450  'to 450'
              346  UNPACK_SEQUENCE_4     4 
              348  STORE_FAST               'fname'
              350  STORE_FAST               'ftype'
              352  STORE_FAST               'fbitsize'
              354  STORE_FAST               'fqual'

 L. 296       356  LOAD_FAST                'fbitsize'
              358  LOAD_CONST               0
              360  COMPARE_OP               >=
          362_364  POP_JUMP_IF_FALSE   370  'to 370'

 L. 297   366_368  JUMP_BACK           344  'to 344'
            370_0  COME_FROM           362  '362'

 L. 298       370  LOAD_FAST                'prnt'
              372  LOAD_STR                 '    offsetof(%s, %s),'
              374  LOAD_FAST                'cname'
              376  LOAD_FAST                'fname'
              378  BUILD_TUPLE_2         2 
              380  BINARY_MODULO    
              382  CALL_FUNCTION_1       1  ''
              384  POP_TOP          

 L. 299       386  LOAD_GLOBAL              isinstance
              388  LOAD_FAST                'ftype'
              390  LOAD_GLOBAL              model
              392  LOAD_ATTR                ArrayType
              394  CALL_FUNCTION_2       2  ''
          396_398  POP_JUMP_IF_FALSE   430  'to 430'
              400  LOAD_FAST                'ftype'
              402  LOAD_ATTR                length
              404  LOAD_CONST               None
              406  <117>                 0  ''
          408_410  POP_JUMP_IF_FALSE   430  'to 430'

 L. 300       412  LOAD_FAST                'prnt'
              414  LOAD_STR                 '    0,  /* %s */'
              416  LOAD_FAST                'ftype'
              418  LOAD_METHOD              _get_c_name
              420  CALL_METHOD_0         0  ''
              422  BINARY_MODULO    
              424  CALL_FUNCTION_1       1  ''
              426  POP_TOP          
              428  JUMP_BACK           344  'to 344'
            430_0  COME_FROM           408  '408'
            430_1  COME_FROM           396  '396'

 L. 302       430  LOAD_FAST                'prnt'
              432  LOAD_STR                 '    sizeof(((%s *)0)->%s),'
              434  LOAD_FAST                'cname'
              436  LOAD_FAST                'fname'
              438  BUILD_TUPLE_2         2 
              440  BINARY_MODULO    
              442  CALL_FUNCTION_1       1  ''
              444  POP_TOP          
          446_448  JUMP_BACK           344  'to 344'
            450_0  COME_FROM           344  '344'

 L. 303       450  LOAD_FAST                'prnt'
              452  LOAD_STR                 '    -1'
              454  CALL_FUNCTION_1       1  ''
              456  POP_TOP          

 L. 304       458  LOAD_FAST                'prnt'
              460  LOAD_STR                 '  };'
              462  CALL_FUNCTION_1       1  ''
              464  POP_TOP          

 L. 305       466  LOAD_FAST                'prnt'
              468  LOAD_STR                 '  return nums[i];'
              470  CALL_FUNCTION_1       1  ''
              472  POP_TOP          

 L. 306       474  LOAD_FAST                'prnt'
              476  LOAD_STR                 '  /* the next line is not executed, but compiled */'
              478  CALL_FUNCTION_1       1  ''
              480  POP_TOP          

 L. 307       482  LOAD_FAST                'prnt'
              484  LOAD_STR                 '  %s(0);'
              486  LOAD_FAST                'checkfuncname'
              488  BUILD_TUPLE_1         1 
              490  BINARY_MODULO    
              492  CALL_FUNCTION_1       1  ''
              494  POP_TOP          

 L. 308       496  LOAD_FAST                'prnt'
              498  LOAD_STR                 '}'
              500  CALL_FUNCTION_1       1  ''
              502  POP_TOP          

 L. 309       504  LOAD_FAST                'prnt'
              506  CALL_FUNCTION_0       0  ''
              508  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _loading_struct_or_union--- This code section failed: ---

 L. 312         0  LOAD_FAST                'tp'
                2  LOAD_ATTR                fldnames
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 313        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 314        14  LOAD_STR                 '_cffi_layout_%s_%s'
               16  LOAD_FAST                'prefix'
               18  LOAD_FAST                'name'
               20  BUILD_TUPLE_2         2 
               22  BINARY_MODULO    
               24  STORE_FAST               'layoutfuncname'

 L. 316        26  LOAD_FAST                'self'
               28  LOAD_ATTR                ffi
               30  LOAD_METHOD              _typeof_locked
               32  LOAD_STR                 'intptr_t(*)(intptr_t)'
               34  CALL_METHOD_1         1  ''
               36  LOAD_CONST               0
               38  BINARY_SUBSCR    
               40  STORE_FAST               'BFunc'

 L. 317        42  LOAD_FAST                'module'
               44  LOAD_METHOD              load_function
               46  LOAD_FAST                'BFunc'
               48  LOAD_FAST                'layoutfuncname'
               50  CALL_METHOD_2         2  ''
               52  STORE_FAST               'function'

 L. 318        54  BUILD_LIST_0          0 
               56  STORE_FAST               'layout'

 L. 319        58  LOAD_CONST               0
               60  STORE_FAST               'num'
             62_0  COME_FROM            98  '98'

 L. 321        62  LOAD_FAST                'function'
               64  LOAD_FAST                'num'
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'x'

 L. 322        70  LOAD_FAST                'x'
               72  LOAD_CONST               0
               74  COMPARE_OP               <
               76  POP_JUMP_IF_FALSE    80  'to 80'
               78  JUMP_FORWARD        100  'to 100'
             80_0  COME_FROM            76  '76'

 L. 323        80  LOAD_FAST                'layout'
               82  LOAD_METHOD              append
               84  LOAD_FAST                'x'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L. 324        90  LOAD_FAST                'num'
               92  LOAD_CONST               1
               94  INPLACE_ADD      
               96  STORE_FAST               'num'
               98  JUMP_BACK            62  'to 62'
            100_0  COME_FROM            78  '78'

 L. 325       100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'tp'
              104  LOAD_GLOBAL              model
              106  LOAD_ATTR                StructOrUnion
              108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_FALSE   226  'to 226'
              112  LOAD_FAST                'tp'
              114  LOAD_ATTR                partial
              116  POP_JUMP_IF_FALSE   226  'to 226'

 L. 328       118  LOAD_FAST                'layout'
              120  LOAD_CONST               0
              122  BINARY_SUBSCR    
              124  STORE_FAST               'totalsize'

 L. 329       126  LOAD_FAST                'layout'
              128  LOAD_CONST               1
              130  BINARY_SUBSCR    
              132  STORE_FAST               'totalalignment'

 L. 330       134  LOAD_FAST                'layout'
              136  LOAD_CONST               2
              138  LOAD_CONST               None
              140  LOAD_CONST               2
              142  BUILD_SLICE_3         3 
              144  BINARY_SUBSCR    
              146  STORE_FAST               'fieldofs'

 L. 331       148  LOAD_FAST                'layout'
              150  LOAD_CONST               3
              152  LOAD_CONST               None
              154  LOAD_CONST               2
              156  BUILD_SLICE_3         3 
              158  BINARY_SUBSCR    
              160  STORE_FAST               'fieldsize'

 L. 332       162  LOAD_FAST                'tp'
              164  LOAD_METHOD              force_flatten
              166  CALL_METHOD_0         0  ''
              168  POP_TOP          

 L. 333       170  LOAD_GLOBAL              len
              172  LOAD_FAST                'fieldofs'
              174  CALL_FUNCTION_1       1  ''
              176  LOAD_GLOBAL              len
              178  LOAD_FAST                'fieldsize'
              180  CALL_FUNCTION_1       1  ''
              182  DUP_TOP          
              184  ROT_THREE        
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_FALSE   204  'to 204'
              190  LOAD_GLOBAL              len
              192  LOAD_FAST                'tp'
              194  LOAD_ATTR                fldnames
              196  CALL_FUNCTION_1       1  ''
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_TRUE    210  'to 210'
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           188  '188'
              204  POP_TOP          
            206_0  COME_FROM           202  '202'
              206  <74>             
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           200  '200'

 L. 334       210  LOAD_FAST                'fieldofs'
              212  LOAD_FAST                'fieldsize'
              214  LOAD_FAST                'totalsize'
              216  LOAD_FAST                'totalalignment'
              218  BUILD_TUPLE_4         4 
              220  LOAD_FAST                'tp'
              222  STORE_ATTR               fixedlayout
              224  JUMP_FORWARD        256  'to 256'
            226_0  COME_FROM           116  '116'
            226_1  COME_FROM           110  '110'

 L. 336       226  LOAD_STR                 '%s %s'
              228  LOAD_FAST                'prefix'
              230  LOAD_FAST                'name'
              232  BUILD_TUPLE_2         2 
              234  BINARY_MODULO    
              236  LOAD_METHOD              strip
              238  CALL_METHOD_0         0  ''
              240  STORE_FAST               'cname'

 L. 337       242  LOAD_FAST                'layout'
              244  LOAD_FAST                'cname'
              246  BUILD_TUPLE_2         2 
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                _struct_pending_verification
              252  LOAD_FAST                'tp'
              254  STORE_SUBSCR     
            256_0  COME_FROM           224  '224'

Parse error at or near `None' instruction at offset -1

    def _loaded_struct_or_union--- This code section failed: ---

 L. 340         0  LOAD_FAST                'tp'
                2  LOAD_ATTR                fldnames
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 341        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 342        14  LOAD_FAST                'self'
               16  LOAD_ATTR                ffi
               18  LOAD_METHOD              _get_cached_btype
               20  LOAD_FAST                'tp'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L. 344        26  LOAD_FAST                'tp'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _struct_pending_verification
               32  <118>                 0  ''
            34_36  POP_JUMP_IF_FALSE   272  'to 272'

 L. 346        38  LOAD_CODE                <code_object check>
               40  LOAD_STR                 'VGenericEngine._loaded_struct_or_union.<locals>.check'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               44  STORE_FAST               'check'

 L. 351        46  LOAD_FAST                'self'
               48  LOAD_ATTR                ffi
               50  STORE_FAST               'ffi'

 L. 352        52  LOAD_FAST                'ffi'
               54  LOAD_METHOD              _get_cached_btype
               56  LOAD_FAST                'tp'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'BStruct'

 L. 353        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _struct_pending_verification
               66  LOAD_METHOD              pop
               68  LOAD_FAST                'tp'
               70  CALL_METHOD_1         1  ''
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'layout'
               76  STORE_FAST               'cname'

 L. 354        78  LOAD_FAST                'check'
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

 L. 355       100  LOAD_FAST                'check'
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

 L. 356       122  LOAD_CONST               2
              124  STORE_FAST               'i'

 L. 357       126  LOAD_FAST                'tp'
              128  LOAD_METHOD              enumfields
              130  CALL_METHOD_0         0  ''
              132  GET_ITER         
            134_0  COME_FROM           252  '252'
            134_1  COME_FROM           154  '154'
              134  FOR_ITER            254  'to 254'
              136  UNPACK_SEQUENCE_4     4 
              138  STORE_FAST               'fname'
              140  STORE_FAST               'ftype'
              142  STORE_FAST               'fbitsize'
              144  STORE_FAST               'fqual'

 L. 358       146  LOAD_FAST                'fbitsize'
              148  LOAD_CONST               0
              150  COMPARE_OP               >=
              152  POP_JUMP_IF_FALSE   156  'to 156'

 L. 359       154  JUMP_BACK           134  'to 134'
            156_0  COME_FROM           152  '152'

 L. 360       156  LOAD_FAST                'check'
              158  LOAD_FAST                'layout'
              160  LOAD_FAST                'i'
              162  BINARY_SUBSCR    
              164  LOAD_FAST                'ffi'
              166  LOAD_METHOD              offsetof
              168  LOAD_FAST                'BStruct'
              170  LOAD_FAST                'fname'
              172  CALL_METHOD_2         2  ''

 L. 361       174  LOAD_STR                 'wrong offset for field %r'
              176  LOAD_FAST                'fname'
              178  BUILD_TUPLE_1         1 
              180  BINARY_MODULO    

 L. 360       182  CALL_FUNCTION_3       3  ''
              184  POP_TOP          

 L. 362       186  LOAD_FAST                'layout'
              188  LOAD_FAST                'i'
              190  LOAD_CONST               1
              192  BINARY_ADD       
              194  BINARY_SUBSCR    
              196  LOAD_CONST               0
              198  COMPARE_OP               !=
              200  POP_JUMP_IF_FALSE   244  'to 244'

 L. 363       202  LOAD_FAST                'ffi'
              204  LOAD_METHOD              _get_cached_btype
              206  LOAD_FAST                'ftype'
              208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'BField'

 L. 364       212  LOAD_FAST                'check'
              214  LOAD_FAST                'layout'
              216  LOAD_FAST                'i'
              218  LOAD_CONST               1
              220  BINARY_ADD       
              222  BINARY_SUBSCR    
              224  LOAD_FAST                'ffi'
              226  LOAD_METHOD              sizeof
              228  LOAD_FAST                'BField'
              230  CALL_METHOD_1         1  ''

 L. 365       232  LOAD_STR                 'wrong size for field %r'
              234  LOAD_FAST                'fname'
              236  BUILD_TUPLE_1         1 
              238  BINARY_MODULO    

 L. 364       240  CALL_FUNCTION_3       3  ''
              242  POP_TOP          
            244_0  COME_FROM           200  '200'

 L. 366       244  LOAD_FAST                'i'
              246  LOAD_CONST               2
              248  INPLACE_ADD      
              250  STORE_FAST               'i'
              252  JUMP_BACK           134  'to 134'
            254_0  COME_FROM           134  '134'

 L. 367       254  LOAD_FAST                'i'
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

    def _generate_gen_anonymous_decl(self, tp, name):
        if isinstancetpmodel.EnumType:
            self._generate_gen_enum_decltpname''
        else:
            self._generate_struct_or_union_decltp''name

    def _loading_gen_anonymous(self, tp, name, module):
        if isinstancetpmodel.EnumType:
            self._loading_gen_enumtpnamemodule''
        else:
            self._loading_struct_or_uniontp''namemodule

    def _loaded_gen_anonymous--- This code section failed: ---

 L. 386         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                EnumType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    36  'to 36'

 L. 387        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _loaded_gen_enum
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

 L. 389        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _loaded_struct_or_union
               40  LOAD_FAST                'tp'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
             46_0  COME_FROM            34  '34'

Parse error at or near `<164>' instruction at offset 28

    def _generate_gen_const--- This code section failed: ---

 L. 396         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _prnt
                4  STORE_FAST               'prnt'

 L. 397         6  LOAD_STR                 '_cffi_%s_%s'
                8  LOAD_FAST                'category'
               10  LOAD_FAST                'name'
               12  BUILD_TUPLE_2         2 
               14  BINARY_MODULO    
               16  STORE_FAST               'funcname'

 L. 398        18  LOAD_FAST                'self'
               20  LOAD_ATTR                export_symbols
               22  LOAD_METHOD              append
               24  LOAD_FAST                'funcname'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 399        30  LOAD_FAST                'check_value'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE   108  'to 108'

 L. 400        38  LOAD_FAST                'is_int'
               40  POP_JUMP_IF_TRUE     46  'to 46'
               42  <74>             
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            40  '40'

 L. 401        46  LOAD_FAST                'category'
               48  LOAD_STR                 'const'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_TRUE     58  'to 58'
               54  <74>             
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            52  '52'

 L. 402        58  LOAD_FAST                'prnt'
               60  LOAD_STR                 'int %s(char *out_error)'
               62  LOAD_FAST                'funcname'
               64  BINARY_MODULO    
               66  CALL_FUNCTION_1       1  ''
               68  POP_TOP          

 L. 403        70  LOAD_FAST                'prnt'
               72  LOAD_STR                 '{'
               74  CALL_FUNCTION_1       1  ''
               76  POP_TOP          

 L. 404        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _check_int_constant_value
               82  LOAD_FAST                'name'
               84  LOAD_FAST                'check_value'
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          

 L. 405        90  LOAD_FAST                'prnt'
               92  LOAD_STR                 '  return 0;'
               94  CALL_FUNCTION_1       1  ''
               96  POP_TOP          

 L. 406        98  LOAD_FAST                'prnt'
              100  LOAD_STR                 '}'
              102  CALL_FUNCTION_1       1  ''
              104  POP_TOP          
              106  JUMP_FORWARD        316  'to 316'
            108_0  COME_FROM            36  '36'

 L. 407       108  LOAD_FAST                'is_int'
              110  POP_JUMP_IF_FALSE   182  'to 182'

 L. 408       112  LOAD_FAST                'category'
              114  LOAD_STR                 'const'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_TRUE    124  'to 124'
              120  <74>             
              122  RAISE_VARARGS_1       1  'exception instance'
            124_0  COME_FROM           118  '118'

 L. 409       124  LOAD_FAST                'prnt'
              126  LOAD_STR                 'int %s(long long *out_value)'
              128  LOAD_FAST                'funcname'
              130  BINARY_MODULO    
              132  CALL_FUNCTION_1       1  ''
              134  POP_TOP          

 L. 410       136  LOAD_FAST                'prnt'
              138  LOAD_STR                 '{'
              140  CALL_FUNCTION_1       1  ''
              142  POP_TOP          

 L. 411       144  LOAD_FAST                'prnt'
              146  LOAD_STR                 '  *out_value = (long long)(%s);'
              148  LOAD_FAST                'name'
              150  BUILD_TUPLE_1         1 
              152  BINARY_MODULO    
              154  CALL_FUNCTION_1       1  ''
              156  POP_TOP          

 L. 412       158  LOAD_FAST                'prnt'
              160  LOAD_STR                 '  return (%s) <= 0;'
              162  LOAD_FAST                'name'
              164  BUILD_TUPLE_1         1 
              166  BINARY_MODULO    
              168  CALL_FUNCTION_1       1  ''
              170  POP_TOP          

 L. 413       172  LOAD_FAST                'prnt'
              174  LOAD_STR                 '}'
              176  CALL_FUNCTION_1       1  ''
              178  POP_TOP          
              180  JUMP_FORWARD        316  'to 316'
            182_0  COME_FROM           110  '110'

 L. 415       182  LOAD_FAST                'tp'
              184  LOAD_CONST               None
              186  <117>                 1  ''
              188  POP_JUMP_IF_TRUE    194  'to 194'
              190  <74>             
              192  RAISE_VARARGS_1       1  'exception instance'
            194_0  COME_FROM           188  '188'

 L. 416       194  LOAD_FAST                'check_value'
              196  LOAD_CONST               None
              198  <117>                 0  ''
              200  POP_JUMP_IF_TRUE    206  'to 206'
              202  <74>             
              204  RAISE_VARARGS_1       1  'exception instance'
            206_0  COME_FROM           200  '200'

 L. 417       206  LOAD_FAST                'category'
              208  LOAD_STR                 'var'
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   220  'to 220'

 L. 418       214  LOAD_STR                 '&'
              216  STORE_FAST               'ampersand'
              218  JUMP_FORWARD        224  'to 224'
            220_0  COME_FROM           212  '212'

 L. 420       220  LOAD_STR                 ''
              222  STORE_FAST               'ampersand'
            224_0  COME_FROM           218  '218'

 L. 421       224  LOAD_STR                 ''
              226  STORE_FAST               'extra'

 L. 422       228  LOAD_FAST                'category'
              230  LOAD_STR                 'const'
              232  COMPARE_OP               ==
          234_236  POP_JUMP_IF_FALSE   260  'to 260'
              238  LOAD_GLOBAL              isinstance
              240  LOAD_FAST                'tp'
              242  LOAD_GLOBAL              model
              244  LOAD_ATTR                StructOrUnion
              246  CALL_FUNCTION_2       2  ''
          248_250  POP_JUMP_IF_FALSE   260  'to 260'

 L. 423       252  LOAD_STR                 'const *'
              254  STORE_FAST               'extra'

 L. 424       256  LOAD_STR                 '&'
              258  STORE_FAST               'ampersand'
            260_0  COME_FROM           248  '248'
            260_1  COME_FROM           234  '234'

 L. 425       260  LOAD_FAST                'prnt'
              262  LOAD_FAST                'tp'
              264  LOAD_METHOD              get_c_name
              266  LOAD_STR                 ' %s%s(void)'
              268  LOAD_FAST                'extra'
              270  LOAD_FAST                'funcname'
              272  BUILD_TUPLE_2         2 
              274  BINARY_MODULO    
              276  LOAD_FAST                'name'
              278  CALL_METHOD_2         2  ''
              280  CALL_FUNCTION_1       1  ''
              282  POP_TOP          

 L. 426       284  LOAD_FAST                'prnt'
              286  LOAD_STR                 '{'
              288  CALL_FUNCTION_1       1  ''
              290  POP_TOP          

 L. 427       292  LOAD_FAST                'prnt'
              294  LOAD_STR                 '  return (%s%s);'
              296  LOAD_FAST                'ampersand'
              298  LOAD_FAST                'name'
              300  BUILD_TUPLE_2         2 
              302  BINARY_MODULO    
              304  CALL_FUNCTION_1       1  ''
              306  POP_TOP          

 L. 428       308  LOAD_FAST                'prnt'
              310  LOAD_STR                 '}'
              312  CALL_FUNCTION_1       1  ''
              314  POP_TOP          
            316_0  COME_FROM           180  '180'
            316_1  COME_FROM           106  '106'

 L. 429       316  LOAD_FAST                'prnt'
              318  CALL_FUNCTION_0       0  ''
              320  POP_TOP          

Parse error at or near `<117>' instruction at offset 34

    def _generate_gen_constant_decl(self, tp, name):
        is_int = isinstancetpmodel.PrimitiveType and tp.is_integer_type()
        self._generate_gen_constis_intnametp

    _loading_gen_constant = _loaded_noop

    def _load_constant--- This code section failed: ---

 L. 438         0  LOAD_STR                 '_cffi_const_%s'
                2  LOAD_FAST                'name'
                4  BINARY_MODULO    
                6  STORE_FAST               'funcname'

 L. 439         8  LOAD_FAST                'check_value'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    42  'to 42'

 L. 440        16  LOAD_FAST                'is_int'
               18  POP_JUMP_IF_TRUE     24  'to 24'
               20  <74>             
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'

 L. 441        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _load_known_int_constant
               28  LOAD_FAST                'module'
               30  LOAD_FAST                'funcname'
               32  CALL_METHOD_2         2  ''
               34  POP_TOP          

 L. 442        36  LOAD_FAST                'check_value'
               38  STORE_FAST               'value'
               40  JUMP_FORWARD        276  'to 276'
             42_0  COME_FROM            14  '14'

 L. 443        42  LOAD_FAST                'is_int'
               44  POP_JUMP_IF_FALSE   176  'to 176'

 L. 444        46  LOAD_FAST                'self'
               48  LOAD_ATTR                ffi
               50  LOAD_METHOD              _typeof_locked
               52  LOAD_STR                 'long long*'
               54  CALL_METHOD_1         1  ''
               56  LOAD_CONST               0
               58  BINARY_SUBSCR    
               60  STORE_FAST               'BType'

 L. 445        62  LOAD_FAST                'self'
               64  LOAD_ATTR                ffi
               66  LOAD_METHOD              _typeof_locked
               68  LOAD_STR                 'int(*)(long long*)'
               70  CALL_METHOD_1         1  ''
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  STORE_FAST               'BFunc'

 L. 446        78  LOAD_FAST                'module'
               80  LOAD_METHOD              load_function
               82  LOAD_FAST                'BFunc'
               84  LOAD_FAST                'funcname'
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'function'

 L. 447        90  LOAD_FAST                'self'
               92  LOAD_ATTR                ffi
               94  LOAD_METHOD              new
               96  LOAD_FAST                'BType'
               98  CALL_METHOD_1         1  ''
              100  STORE_FAST               'p'

 L. 448       102  LOAD_FAST                'function'
              104  LOAD_FAST                'p'
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'negative'

 L. 449       110  LOAD_GLOBAL              int
              112  LOAD_FAST                'p'
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'value'

 L. 450       122  LOAD_FAST                'value'
              124  LOAD_CONST               0
              126  COMPARE_OP               <
              128  POP_JUMP_IF_FALSE   174  'to 174'
              130  LOAD_FAST                'negative'
              132  POP_JUMP_IF_TRUE    174  'to 174'

 L. 451       134  LOAD_FAST                'self'
              136  LOAD_ATTR                ffi
              138  LOAD_METHOD              _typeof_locked
              140  LOAD_STR                 'long long'
              142  CALL_METHOD_1         1  ''
              144  LOAD_CONST               0
              146  BINARY_SUBSCR    
              148  STORE_FAST               'BLongLong'

 L. 452       150  LOAD_FAST                'value'
              152  LOAD_CONST               1
              154  LOAD_CONST               8
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                ffi
              160  LOAD_METHOD              sizeof
              162  LOAD_FAST                'BLongLong'
              164  CALL_METHOD_1         1  ''
              166  BINARY_MULTIPLY  
              168  BINARY_LSHIFT    
              170  INPLACE_ADD      
              172  STORE_FAST               'value'
            174_0  COME_FROM           132  '132'
            174_1  COME_FROM           128  '128'
              174  JUMP_FORWARD        276  'to 276'
            176_0  COME_FROM            44  '44'

 L. 454       176  LOAD_FAST                'check_value'
              178  LOAD_CONST               None
              180  <117>                 0  ''
              182  POP_JUMP_IF_TRUE    188  'to 188'
              184  <74>             
              186  RAISE_VARARGS_1       1  'exception instance'
            188_0  COME_FROM           182  '182'

 L. 455       188  LOAD_STR                 '(*)(void)'
              190  STORE_FAST               'fntypeextra'

 L. 456       192  LOAD_GLOBAL              isinstance
              194  LOAD_FAST                'tp'
              196  LOAD_GLOBAL              model
              198  LOAD_ATTR                StructOrUnion
              200  CALL_FUNCTION_2       2  ''
              202  POP_JUMP_IF_FALSE   212  'to 212'

 L. 457       204  LOAD_STR                 '*'
              206  LOAD_FAST                'fntypeextra'
              208  BINARY_ADD       
              210  STORE_FAST               'fntypeextra'
            212_0  COME_FROM           202  '202'

 L. 458       212  LOAD_FAST                'self'
              214  LOAD_ATTR                ffi
              216  LOAD_METHOD              _typeof_locked
              218  LOAD_FAST                'tp'
              220  LOAD_METHOD              get_c_name
              222  LOAD_FAST                'fntypeextra'
              224  LOAD_FAST                'name'
              226  CALL_METHOD_2         2  ''
              228  CALL_METHOD_1         1  ''
              230  LOAD_CONST               0
              232  BINARY_SUBSCR    
              234  STORE_FAST               'BFunc'

 L. 459       236  LOAD_FAST                'module'
              238  LOAD_METHOD              load_function
              240  LOAD_FAST                'BFunc'
              242  LOAD_FAST                'funcname'
              244  CALL_METHOD_2         2  ''
              246  STORE_FAST               'function'

 L. 460       248  LOAD_FAST                'function'
              250  CALL_FUNCTION_0       0  ''
              252  STORE_FAST               'value'

 L. 461       254  LOAD_GLOBAL              isinstance
              256  LOAD_FAST                'tp'
              258  LOAD_GLOBAL              model
              260  LOAD_ATTR                StructOrUnion
              262  CALL_FUNCTION_2       2  ''
          264_266  POP_JUMP_IF_FALSE   276  'to 276'

 L. 462       268  LOAD_FAST                'value'
              270  LOAD_CONST               0
              272  BINARY_SUBSCR    
              274  STORE_FAST               'value'
            276_0  COME_FROM           264  '264'
            276_1  COME_FROM           174  '174'
            276_2  COME_FROM            40  '40'

 L. 463       276  LOAD_FAST                'value'
              278  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12

    def _loaded_gen_constant(self, tp, name, module, library):
        is_int = isinstancetpmodel.PrimitiveType and tp.is_integer_type()
        value = self._load_constantis_inttpnamemodule
        setattr(library, name, value)
        type(library)._cffi_dir.appendname

    def _check_int_constant_value(self, name, value):
        prnt = self._prnt
        if value <= 0:
            prnt('  if ((%s) > 0 || (long)(%s) != %dL) {' % (
             name, name, value))
        else:
            prnt('  if ((%s) <= 0 || (unsigned long)(%s) != %dUL) {' % (
             name, name, value))
        prnt('    char buf[64];')
        prnt('    if ((%s) <= 0)' % name)
        prnt('        sprintf(buf, "%%ld", (long)(%s));' % name)
        prnt('    else')
        prnt('        sprintf(buf, "%%lu", (unsigned long)(%s));' % name)
        prnt('    sprintf(out_error, "%s has the real value %s, not %s",')
        prnt('            "%s", buf, "%d");' % (name[:100], value))
        prnt('    return -1;')
        prnt('  }')

    def _load_known_int_constant(self, module, funcname):
        BType = self.ffi._typeof_locked'char[]'[0]
        BFunc = self.ffi._typeof_locked'int(*)(char*)'[0]
        function = module.load_function(BFunc, funcname)
        p = self.ffi.new(BType, 256)
        if function(p) < 0:
            error = self.ffi.stringp
            if sys.version_info >= (3, ):
                error = strerror'utf-8'
            raise VerificationError(error)

    def _enum_funcname(self, prefix, name):
        name = name.replace('$', '___D_')
        return '_cffi_e_%s_%s' % (prefix, name)

    def _generate_gen_enum_decl(self, tp, name, prefix='enum'):
        if tp.partial:
            for enumerator in tp.enumerators:
                self._generate_gen_const(True, enumerator)
            else:
                return

        funcname = self._enum_funcname(prefix, name)
        self.export_symbols.appendfuncname
        prnt = self._prnt
        prnt('int %s(char *out_error)' % funcname)
        prnt('{')
        for enumerator, enumvalue in ziptp.enumeratorstp.enumvalues:
            self._check_int_constant_value(enumerator, enumvalue)
        else:
            prnt('  return 0;')
            prnt('}')
            prnt

    def _loading_gen_enum(self, tp, name, module, prefix='enum'):
        if tp.partial:
            enumvalues = [self._load_constantTruetpenumeratormodule for enumerator in tp.enumerators]
            tp.enumvalues = tuple(enumvalues)
            tp.partial_resolved = True
        else:
            funcname = self._enum_funcname(prefix, name)
            self._load_known_int_constant(module, funcname)

    def _loaded_gen_enum(self, tp, name, module, library):
        for enumerator, enumvalue in ziptp.enumeratorstp.enumvalues:
            setattr(library, enumerator, enumvalue)
            type(library)._cffi_dir.appendenumerator

    def _generate_gen_macro_decl(self, tp, name):
        if tp == '...':
            check_value = None
        else:
            check_value = tp
        self._generate_gen_const(True, name, check_value=check_value)

    _loading_gen_macro = _loaded_noop

    def _loaded_gen_macro(self, tp, name, module, library):
        if tp == '...':
            check_value = None
        else:
            check_value = tp
        value = self._load_constant(True, tp, name, module, check_value=check_value)
        setattr(library, name, value)
        type(library)._cffi_dir.appendname

    def _generate_gen_variable_decl(self, tp, name):
        if isinstancetpmodel.ArrayType:
            if tp.length_is_unknown():
                prnt = self._prnt
                funcname = '_cffi_sizeof_%s' % (name,)
                self.export_symbols.appendfuncname
                prnt('size_t %s(void)' % funcname)
                prnt('{')
                prnt('  return sizeof(%s);' % (name,))
                prnt('}')
            tp_ptr = model.PointerTypetp.item
            self._generate_gen_constFalsenametp_ptr
        else:
            tp_ptr = model.PointerTypetp
            self._generate_gen_const(False, name, tp_ptr, category='var')

    _loading_gen_variable = _loaded_noop

    def _loaded_gen_variable--- This code section failed: ---

 L. 585         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                ArrayType
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE   232  'to 232'

 L. 587        12  LOAD_FAST                'tp'
               14  LOAD_METHOD              length_is_unknown
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_FALSE   136  'to 136'

 L. 588        20  LOAD_STR                 '_cffi_sizeof_%s'
               22  LOAD_FAST                'name'
               24  BUILD_TUPLE_1         1 
               26  BINARY_MODULO    
               28  STORE_FAST               'funcname'

 L. 589        30  LOAD_FAST                'self'
               32  LOAD_ATTR                ffi
               34  LOAD_METHOD              _typeof_locked
               36  LOAD_STR                 'size_t(*)(void)'
               38  CALL_METHOD_1         1  ''
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  STORE_FAST               'BFunc'

 L. 590        46  LOAD_FAST                'module'
               48  LOAD_METHOD              load_function
               50  LOAD_FAST                'BFunc'
               52  LOAD_FAST                'funcname'
               54  CALL_METHOD_2         2  ''
               56  STORE_FAST               'function'

 L. 591        58  LOAD_FAST                'function'
               60  CALL_FUNCTION_0       0  ''
               62  STORE_FAST               'size'

 L. 592        64  LOAD_FAST                'self'
               66  LOAD_ATTR                ffi
               68  LOAD_METHOD              _get_cached_btype
               70  LOAD_FAST                'tp'
               72  LOAD_ATTR                item
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'BItemType'

 L. 593        78  LOAD_GLOBAL              divmod
               80  LOAD_FAST                'size'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                ffi
               86  LOAD_METHOD              sizeof
               88  LOAD_FAST                'BItemType'
               90  CALL_METHOD_1         1  ''
               92  CALL_FUNCTION_2       2  ''
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'length'
               98  STORE_FAST               'rest'

 L. 594       100  LOAD_FAST                'rest'
              102  LOAD_CONST               0
              104  COMPARE_OP               !=
              106  POP_JUMP_IF_FALSE   126  'to 126'

 L. 595       108  LOAD_GLOBAL              VerificationError

 L. 596       110  LOAD_STR                 'bad size: %r does not seem to be an array of %s'

 L. 597       112  LOAD_FAST                'name'
              114  LOAD_FAST                'tp'
              116  LOAD_ATTR                item
              118  BUILD_TUPLE_2         2 

 L. 596       120  BINARY_MODULO    

 L. 595       122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM           106  '106'

 L. 598       126  LOAD_FAST                'tp'
              128  LOAD_METHOD              resolve_length
              130  LOAD_FAST                'length'
              132  CALL_METHOD_1         1  ''
              134  STORE_FAST               'tp'
            136_0  COME_FROM            18  '18'

 L. 599       136  LOAD_GLOBAL              model
              138  LOAD_METHOD              PointerType
              140  LOAD_FAST                'tp'
              142  LOAD_ATTR                item
              144  CALL_METHOD_1         1  ''
              146  STORE_FAST               'tp_ptr'

 L. 600       148  LOAD_FAST                'self'
              150  LOAD_METHOD              _load_constant
              152  LOAD_CONST               False
              154  LOAD_FAST                'tp_ptr'
              156  LOAD_FAST                'name'
              158  LOAD_FAST                'module'
              160  CALL_METHOD_4         4  ''
              162  STORE_FAST               'value'

 L. 603       164  LOAD_FAST                'tp'
              166  LOAD_ATTR                length
              168  LOAD_CONST               None
              170  <117>                 1  ''
              172  POP_JUMP_IF_FALSE   200  'to 200'

 L. 604       174  LOAD_FAST                'self'
              176  LOAD_ATTR                ffi
              178  LOAD_METHOD              _get_cached_btype
              180  LOAD_FAST                'tp'
              182  CALL_METHOD_1         1  ''
              184  STORE_FAST               'BArray'

 L. 605       186  LOAD_FAST                'self'
              188  LOAD_ATTR                ffi
              190  LOAD_METHOD              cast
              192  LOAD_FAST                'BArray'
              194  LOAD_FAST                'value'
              196  CALL_METHOD_2         2  ''
              198  STORE_FAST               'value'
            200_0  COME_FROM           172  '172'

 L. 606       200  LOAD_GLOBAL              setattr
              202  LOAD_FAST                'library'
              204  LOAD_FAST                'name'
              206  LOAD_FAST                'value'
              208  CALL_FUNCTION_3       3  ''
              210  POP_TOP          

 L. 607       212  LOAD_GLOBAL              type
              214  LOAD_FAST                'library'
              216  CALL_FUNCTION_1       1  ''
              218  LOAD_ATTR                _cffi_dir
              220  LOAD_METHOD              append
              222  LOAD_FAST                'name'
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          

 L. 608       228  LOAD_CONST               None
              230  RETURN_VALUE     
            232_0  COME_FROM            10  '10'

 L. 611       232  LOAD_STR                 '_cffi_var_%s'
              234  LOAD_FAST                'name'
              236  BINARY_MODULO    
              238  STORE_FAST               'funcname'

 L. 612       240  LOAD_FAST                'self'
              242  LOAD_ATTR                ffi
              244  LOAD_METHOD              _typeof_locked
              246  LOAD_FAST                'tp'
              248  LOAD_METHOD              get_c_name
              250  LOAD_STR                 '*(*)(void)'
              252  LOAD_FAST                'name'
              254  CALL_METHOD_2         2  ''
              256  CALL_METHOD_1         1  ''
              258  LOAD_CONST               0
              260  BINARY_SUBSCR    
              262  STORE_FAST               'BFunc'

 L. 613       264  LOAD_FAST                'module'
              266  LOAD_METHOD              load_function
              268  LOAD_FAST                'BFunc'
              270  LOAD_FAST                'funcname'
              272  CALL_METHOD_2         2  ''
              274  STORE_FAST               'function'

 L. 614       276  LOAD_FAST                'function'
              278  CALL_FUNCTION_0       0  ''
              280  STORE_DEREF              'ptr'

 L. 615       282  LOAD_CLOSURE             'ptr'
              284  BUILD_TUPLE_1         1 
              286  LOAD_CODE                <code_object getter>
              288  LOAD_STR                 'VGenericEngine._loaded_gen_variable.<locals>.getter'
              290  MAKE_FUNCTION_8          'closure'
              292  STORE_FAST               'getter'

 L. 617       294  LOAD_CLOSURE             'ptr'
              296  BUILD_TUPLE_1         1 
              298  LOAD_CODE                <code_object setter>
              300  LOAD_STR                 'VGenericEngine._loaded_gen_variable.<locals>.setter'
              302  MAKE_FUNCTION_8          'closure'
              304  STORE_FAST               'setter'

 L. 619       306  LOAD_GLOBAL              setattr
              308  LOAD_GLOBAL              type
              310  LOAD_FAST                'library'
              312  CALL_FUNCTION_1       1  ''
              314  LOAD_FAST                'name'
              316  LOAD_GLOBAL              property
              318  LOAD_FAST                'getter'
              320  LOAD_FAST                'setter'
              322  CALL_FUNCTION_2       2  ''
              324  CALL_FUNCTION_3       3  ''
              326  POP_TOP          

 L. 620       328  LOAD_GLOBAL              type
              330  LOAD_FAST                'library'
              332  CALL_FUNCTION_1       1  ''
              334  LOAD_ATTR                _cffi_dir
              336  LOAD_METHOD              append
              338  LOAD_FAST                'name'
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          

Parse error at or near `<117>' instruction at offset 170


cffimod_header = '\n#include <stdio.h>\n#include <stddef.h>\n#include <stdarg.h>\n#include <errno.h>\n#include <sys/types.h>   /* XXX for ssize_t on some platforms */\n\n/* this block of #ifs should be kept exactly identical between\n   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py\n   and cffi/_cffi_include.h */\n#if defined(_MSC_VER)\n# include <malloc.h>   /* for alloca() */\n# if _MSC_VER < 1600   /* MSVC < 2010 */\n   typedef __int8 int8_t;\n   typedef __int16 int16_t;\n   typedef __int32 int32_t;\n   typedef __int64 int64_t;\n   typedef unsigned __int8 uint8_t;\n   typedef unsigned __int16 uint16_t;\n   typedef unsigned __int32 uint32_t;\n   typedef unsigned __int64 uint64_t;\n   typedef __int8 int_least8_t;\n   typedef __int16 int_least16_t;\n   typedef __int32 int_least32_t;\n   typedef __int64 int_least64_t;\n   typedef unsigned __int8 uint_least8_t;\n   typedef unsigned __int16 uint_least16_t;\n   typedef unsigned __int32 uint_least32_t;\n   typedef unsigned __int64 uint_least64_t;\n   typedef __int8 int_fast8_t;\n   typedef __int16 int_fast16_t;\n   typedef __int32 int_fast32_t;\n   typedef __int64 int_fast64_t;\n   typedef unsigned __int8 uint_fast8_t;\n   typedef unsigned __int16 uint_fast16_t;\n   typedef unsigned __int32 uint_fast32_t;\n   typedef unsigned __int64 uint_fast64_t;\n   typedef __int64 intmax_t;\n   typedef unsigned __int64 uintmax_t;\n# else\n#  include <stdint.h>\n# endif\n# if _MSC_VER < 1800   /* MSVC < 2013 */\n#  ifndef __cplusplus\n    typedef unsigned char _Bool;\n#  endif\n# endif\n#else\n# include <stdint.h>\n# if (defined (__SVR4) && defined (__sun)) || defined(_AIX) || defined(__hpux)\n#  include <alloca.h>\n# endif\n#endif\n'