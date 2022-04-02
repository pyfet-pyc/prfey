# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\command\config.py
from __future__ import division, absolute_import, print_function
import os, signal, warnings, sys, subprocess, textwrap
import distutils.command.config as old_config
from distutils.command.config import LANG_EXT
from distutils import log
from distutils.file_util import copy_file
from distutils.ccompiler import CompileError, LinkError
import distutils
from numpy.distutils.exec_command import filepath_from_subprocess_output
from numpy.distutils.mingw32ccompiler import generate_manifest
from numpy.distutils.command.autodist import check_gcc_function_attribute, check_gcc_function_attribute_with_intrinsics, check_gcc_variable_attribute, check_inline, check_restrict, check_compiler_gcc4
from numpy.distutils.compat import get_exception
LANG_EXT['f77'] = '.f'
LANG_EXT['f90'] = '.f90'

class config(old_config):
    old_config.user_options += [
     ('fcompiler=', None, 'specify the Fortran compiler type')]

    def initialize_options(self):
        self.fcompiler = None
        old_config.initialize_options(self)

    def _check_compiler(self):
        old_config._check_compiler(self)
        from numpy.distutils.fcompiler import FCompiler, new_fcompiler
        if sys.platform == 'win32':
            if self.compiler.compiler_type in ('msvc', 'intelw', 'intelemw'):
                if not self.compiler.initialized:
                    try:
                        self.compiler.initialize()
                    except IOError:
                        e = get_exception()
                        msg = textwrap.dedent('                        Could not initialize compiler instance: do you have Visual Studio\n                        installed?  If you are trying to build with MinGW, please use "python setup.py\n                        build -c mingw32" instead.  If you have Visual Studio installed, check it is\n                        correctly installed, and the right version (VS 2008 for python 2.6, 2.7 and 3.2,\n                        VS 2010 for >= 3.3).\n\n                        Original exception was: %s, and the Compiler class was %s\n                        ============================================================================') % (
                         e, self.compiler.__class__.__name__)
                        print(textwrap.dedent('                        ============================================================================'))
                        raise distutils.errors.DistutilsPlatformError(msg)

                from distutils import msvc9compiler
                if msvc9compiler.get_build_version() >= 10:
                    for ldflags in (
                     self.compiler.ldflags_shared,
                     self.compiler.ldflags_shared_debug):
                        if '/MANIFEST' not in ldflags:
                            ldflags.append('/MANIFEST')
                    else:
                        if not isinstance(self.fcompiler, FCompiler):
                            self.fcompiler = new_fcompiler(compiler=(self.fcompiler), dry_run=(self.dry_run),
                              force=1,
                              c_compiler=(self.compiler))
                            if self.fcompiler is not None:
                                self.fcompiler.customize(self.distribution)
                                if self.fcompiler.get_version():
                                    self.fcompiler.customize_cmd(self)
                                    self.fcompiler.show_customization()

    def _wrap_method(self, mth, lang, args):
        from distutils.ccompiler import CompileError
        from distutils.errors import DistutilsExecError
        save_compiler = self.compiler
        if lang in ('f77', 'f90'):
            self.compiler = self.fcompiler
        try:
            ret = mth(*(self,) + args)
        except (DistutilsExecError, CompileError):
            str(get_exception())
            self.compiler = save_compiler
            raise CompileError
        else:
            self.compiler = save_compiler
            return ret

    def _compile(self, body, headers, include_dirs, lang):
        src, obj = self._wrap_method(old_config._compile, lang, (
         body, headers, include_dirs, lang))
        self.temp_files.append(obj + '.d')
        return (
         src, obj)

    def _link--- This code section failed: ---

 L. 117         0  LOAD_FAST                'self'
                2  LOAD_ATTR                compiler
                4  LOAD_ATTR                compiler_type
                6  LOAD_STR                 'msvc'
                8  COMPARE_OP               ==
            10_12  POP_JUMP_IF_FALSE   408  'to 408'

 L. 118        14  LOAD_FAST                'libraries'
               16  JUMP_IF_TRUE_OR_POP    20  'to 20'
               18  BUILD_LIST_0          0 
             20_0  COME_FROM            16  '16'
               20  LOAD_CONST               None
               22  LOAD_CONST               None
               24  BUILD_SLICE_2         2 
               26  BINARY_SUBSCR    
               28  STORE_FAST               'libraries'

 L. 119        30  LOAD_FAST                'library_dirs'
               32  JUMP_IF_TRUE_OR_POP    36  'to 36'
               34  BUILD_LIST_0          0 
             36_0  COME_FROM            32  '32'
               36  LOAD_CONST               None
               38  LOAD_CONST               None
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  STORE_FAST               'library_dirs'

 L. 120        46  LOAD_FAST                'lang'
               48  LOAD_CONST               ('f77', 'f90')
               50  COMPARE_OP               in
               52  POP_JUMP_IF_FALSE   194  'to 194'

 L. 121        54  LOAD_STR                 'c'
               56  STORE_FAST               'lang'

 L. 122        58  LOAD_FAST                'self'
               60  LOAD_ATTR                fcompiler
               62  POP_JUMP_IF_FALSE   194  'to 194'

 L. 123        64  LOAD_FAST                'self'
               66  LOAD_ATTR                fcompiler
               68  LOAD_ATTR                library_dirs
               70  JUMP_IF_TRUE_OR_POP    74  'to 74'
               72  BUILD_LIST_0          0 
             74_0  COME_FROM            70  '70'
               74  GET_ITER         
             76_0  COME_FROM           156  '156'
               76  FOR_ITER            158  'to 158'
               78  STORE_FAST               'd'

 L. 126        80  LOAD_FAST                'd'
               82  LOAD_METHOD              startswith
               84  LOAD_STR                 '/usr/lib'
               86  CALL_METHOD_1         1  ''
               88  POP_JUMP_IF_FALSE   146  'to 146'

 L. 127        90  SETUP_FINALLY       112  'to 112'

 L. 128        92  LOAD_GLOBAL              subprocess
               94  LOAD_METHOD              check_output
               96  LOAD_STR                 'cygpath'

 L. 129        98  LOAD_STR                 '-w'

 L. 129       100  LOAD_FAST                'd'

 L. 128       102  BUILD_LIST_3          3 
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'd'
              108  POP_BLOCK        
              110  JUMP_FORWARD        138  'to 138'
            112_0  COME_FROM_FINALLY    90  '90'

 L. 130       112  DUP_TOP          
              114  LOAD_GLOBAL              OSError
              116  LOAD_GLOBAL              subprocess
              118  LOAD_ATTR                CalledProcessError
              120  BUILD_TUPLE_2         2 
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   136  'to 136'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 131       132  POP_EXCEPT       
              134  BREAK_LOOP          146  'to 146'
            136_0  COME_FROM           124  '124'
              136  END_FINALLY      
            138_0  COME_FROM           110  '110'

 L. 133       138  LOAD_GLOBAL              filepath_from_subprocess_output
              140  LOAD_FAST                'd'
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'd'
            146_0  COME_FROM           134  '134'
            146_1  COME_FROM            88  '88'

 L. 134       146  LOAD_FAST                'library_dirs'
              148  LOAD_METHOD              append
              150  LOAD_FAST                'd'
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          
              156  JUMP_BACK            76  'to 76'
            158_0  COME_FROM            76  '76'

 L. 135       158  LOAD_FAST                'self'
              160  LOAD_ATTR                fcompiler
              162  LOAD_ATTR                libraries
              164  JUMP_IF_TRUE_OR_POP   168  'to 168'
              166  BUILD_LIST_0          0 
            168_0  COME_FROM           164  '164'
              168  GET_ITER         
            170_0  COME_FROM           192  '192'
            170_1  COME_FROM           180  '180'
              170  FOR_ITER            194  'to 194'
              172  STORE_FAST               'libname'

 L. 136       174  LOAD_FAST                'libname'
              176  LOAD_FAST                'libraries'
              178  COMPARE_OP               not-in
              180  POP_JUMP_IF_FALSE_BACK   170  'to 170'

 L. 137       182  LOAD_FAST                'libraries'
              184  LOAD_METHOD              append
              186  LOAD_FAST                'libname'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          
              192  JUMP_BACK           170  'to 170'
            194_0  COME_FROM           170  '170'
            194_1  COME_FROM            62  '62'
            194_2  COME_FROM            52  '52'

 L. 138       194  LOAD_FAST                'libraries'
              196  GET_ITER         
            198_0  COME_FROM           404  '404'
            198_1  COME_FROM           384  '384'
            198_2  COME_FROM           278  '278'
            198_3  COME_FROM           212  '212'
              198  FOR_ITER            406  'to 406'
              200  STORE_FAST               'libname'

 L. 139       202  LOAD_FAST                'libname'
              204  LOAD_METHOD              startswith
              206  LOAD_STR                 'msvc'
              208  CALL_METHOD_1         1  ''
              210  POP_JUMP_IF_FALSE   214  'to 214'

 L. 139       212  JUMP_BACK           198  'to 198'
            214_0  COME_FROM           210  '210'

 L. 140       214  LOAD_CONST               False
              216  STORE_FAST               'fileexists'

 L. 141       218  LOAD_FAST                'library_dirs'
              220  JUMP_IF_TRUE_OR_POP   224  'to 224'
              222  BUILD_LIST_0          0 
            224_0  COME_FROM           220  '220'
              224  GET_ITER         
            226_0  COME_FROM           270  '270'
            226_1  COME_FROM           258  '258'
              226  FOR_ITER            272  'to 272'
              228  STORE_FAST               'libdir'

 L. 142       230  LOAD_GLOBAL              os
              232  LOAD_ATTR                path
              234  LOAD_METHOD              join
              236  LOAD_FAST                'libdir'
              238  LOAD_STR                 '%s.lib'
              240  LOAD_FAST                'libname'
              242  BINARY_MODULO    
              244  CALL_METHOD_2         2  ''
              246  STORE_FAST               'libfile'

 L. 143       248  LOAD_GLOBAL              os
              250  LOAD_ATTR                path
              252  LOAD_METHOD              isfile
              254  LOAD_FAST                'libfile'
              256  CALL_METHOD_1         1  ''
              258  POP_JUMP_IF_FALSE_BACK   226  'to 226'

 L. 144       260  LOAD_CONST               True
              262  STORE_FAST               'fileexists'

 L. 145       264  POP_TOP          
          266_268  BREAK_LOOP          272  'to 272'
              270  JUMP_BACK           226  'to 226'
            272_0  COME_FROM           266  '266'
            272_1  COME_FROM           226  '226'

 L. 146       272  LOAD_FAST                'fileexists'
          274_276  POP_JUMP_IF_FALSE   280  'to 280'

 L. 146       278  JUMP_BACK           198  'to 198'
            280_0  COME_FROM           274  '274'

 L. 148       280  LOAD_CONST               False
              282  STORE_FAST               'fileexists'

 L. 149       284  LOAD_FAST                'library_dirs'
              286  GET_ITER         
            288_0  COME_FROM           374  '374'
            288_1  COME_FROM           320  '320'
              288  FOR_ITER            378  'to 378'
              290  STORE_FAST               'libdir'

 L. 150       292  LOAD_GLOBAL              os
              294  LOAD_ATTR                path
              296  LOAD_METHOD              join
              298  LOAD_FAST                'libdir'
              300  LOAD_STR                 'lib%s.a'
              302  LOAD_FAST                'libname'
              304  BINARY_MODULO    
              306  CALL_METHOD_2         2  ''
              308  STORE_FAST               'libfile'

 L. 151       310  LOAD_GLOBAL              os
              312  LOAD_ATTR                path
              314  LOAD_METHOD              isfile
              316  LOAD_FAST                'libfile'
              318  CALL_METHOD_1         1  ''
          320_322  POP_JUMP_IF_FALSE_BACK   288  'to 288'

 L. 154       324  LOAD_GLOBAL              os
              326  LOAD_ATTR                path
              328  LOAD_METHOD              join
              330  LOAD_FAST                'libdir'
              332  LOAD_STR                 '%s.lib'
              334  LOAD_FAST                'libname'
              336  BINARY_MODULO    
              338  CALL_METHOD_2         2  ''
              340  STORE_FAST               'libfile2'

 L. 155       342  LOAD_GLOBAL              copy_file
              344  LOAD_FAST                'libfile'
              346  LOAD_FAST                'libfile2'
              348  CALL_FUNCTION_2       2  ''
              350  POP_TOP          

 L. 156       352  LOAD_FAST                'self'
              354  LOAD_ATTR                temp_files
              356  LOAD_METHOD              append
              358  LOAD_FAST                'libfile2'
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          

 L. 157       364  LOAD_CONST               True
              366  STORE_FAST               'fileexists'

 L. 158       368  POP_TOP          
          370_372  BREAK_LOOP          378  'to 378'
          374_376  JUMP_BACK           288  'to 288'
            378_0  COME_FROM           370  '370'
            378_1  COME_FROM           288  '288'

 L. 159       378  LOAD_FAST                'fileexists'
          380_382  POP_JUMP_IF_FALSE   386  'to 386'

 L. 159       384  JUMP_BACK           198  'to 198'
            386_0  COME_FROM           380  '380'

 L. 160       386  LOAD_GLOBAL              log
              388  LOAD_METHOD              warn
              390  LOAD_STR                 'could not find library %r in directories %s'

 L. 161       392  LOAD_FAST                'libname'
              394  LOAD_FAST                'library_dirs'
              396  BUILD_TUPLE_2         2 

 L. 160       398  BINARY_MODULO    
              400  CALL_METHOD_1         1  ''
              402  POP_TOP          
              404  JUMP_BACK           198  'to 198'
            406_0  COME_FROM           198  '198'
              406  JUMP_FORWARD        430  'to 430'
            408_0  COME_FROM            10  '10'

 L. 162       408  LOAD_FAST                'self'
              410  LOAD_ATTR                compiler
              412  LOAD_ATTR                compiler_type
              414  LOAD_STR                 'mingw32'
              416  COMPARE_OP               ==
          418_420  POP_JUMP_IF_FALSE   430  'to 430'

 L. 163       422  LOAD_GLOBAL              generate_manifest
              424  LOAD_FAST                'self'
              426  CALL_FUNCTION_1       1  ''
              428  POP_TOP          
            430_0  COME_FROM           418  '418'
            430_1  COME_FROM           406  '406'

 L. 164       430  LOAD_FAST                'self'
              432  LOAD_METHOD              _wrap_method
              434  LOAD_GLOBAL              old_config
              436  LOAD_ATTR                _link
              438  LOAD_FAST                'lang'

 L. 165       440  LOAD_FAST                'body'
              442  LOAD_FAST                'headers'
              444  LOAD_FAST                'include_dirs'

 L. 166       446  LOAD_FAST                'libraries'

 L. 166       448  LOAD_FAST                'library_dirs'

 L. 166       450  LOAD_FAST                'lang'

 L. 165       452  BUILD_TUPLE_6         6 

 L. 164       454  CALL_METHOD_3         3  ''
              456  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 136

    def check_header(self, header, include_dirs=None, library_dirs=None, lang='c'):
        self._check_compiler()
        return self.try_compile('/* we need a dummy line to make distutils happy */', [
         header], include_dirs)

    def check_decl(self, symbol, headers=None, include_dirs=None):
        self._check_compiler()
        body = textwrap.dedent('\n            int main(void)\n            {\n            #ifndef %s\n                (void) %s;\n            #endif\n                ;\n                return 0;\n            }') % (
         symbol, symbol)
        return self.try_compile(body, headers, include_dirs)

    def check_macro_true(self, symbol, headers=None, include_dirs=None):
        self._check_compiler()
        body = textwrap.dedent('\n            int main(void)\n            {\n            #if %s\n            #else\n            #error false or undefined macro\n            #endif\n                ;\n                return 0;\n            }') % (
         symbol,)
        return self.try_compile(body, headers, include_dirs)

    def check_type(self, type_name, headers=None, include_dirs=None, library_dirs=None):
        """Check type availability. Return True if the type can be compiled,
        False otherwise"""
        self._check_compiler()
        body = textwrap.dedent('\n            int main(void) {\n              if ((%(name)s *) 0)\n                return 0;\n              if (sizeof (%(name)s))\n                return 0;\n            }\n            ') % {'name': type_name}
        st = False
        try:
            try:
                self._compile(body % {'type': type_name}, headers, include_dirs, 'c')
                st = True
            except distutils.errors.CompileError:
                st = False

        finally:
            self._clean()

        return st

    def check_type_size--- This code section failed: ---

 L. 236         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_compiler
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 239         8  LOAD_GLOBAL              textwrap
               10  LOAD_METHOD              dedent
               12  LOAD_STR                 '\n            typedef %(type)s npy_check_sizeof_type;\n            int main (void)\n            {\n                static int test_array [1 - 2 * !(((long) (sizeof (npy_check_sizeof_type))) >= 0)];\n                test_array [0] = 0\n\n                ;\n                return 0;\n            }\n            '
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'body'

 L. 250        18  LOAD_FAST                'self'
               20  LOAD_METHOD              _compile
               22  LOAD_FAST                'body'
               24  LOAD_STR                 'type'
               26  LOAD_FAST                'type_name'
               28  BUILD_MAP_1           1 
               30  BINARY_MODULO    

 L. 251        32  LOAD_FAST                'headers'

 L. 251        34  LOAD_FAST                'include_dirs'

 L. 251        36  LOAD_STR                 'c'

 L. 250        38  CALL_METHOD_4         4  ''
               40  POP_TOP          

 L. 252        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _clean
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          

 L. 254        50  LOAD_FAST                'expected'
               52  POP_JUMP_IF_FALSE   140  'to 140'

 L. 255        54  LOAD_GLOBAL              textwrap
               56  LOAD_METHOD              dedent
               58  LOAD_STR                 '\n                typedef %(type)s npy_check_sizeof_type;\n                int main (void)\n                {\n                    static int test_array [1 - 2 * !(((long) (sizeof (npy_check_sizeof_type))) == %(size)s)];\n                    test_array [0] = 0\n\n                    ;\n                    return 0;\n                }\n                '
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'body'

 L. 266        64  LOAD_FAST                'expected'
               66  GET_ITER         
             68_0  COME_FROM           138  '138'
             68_1  COME_FROM           134  '134'
               68  FOR_ITER            140  'to 140'
               70  STORE_FAST               'size'

 L. 267        72  SETUP_FINALLY       118  'to 118'

 L. 268        74  LOAD_FAST                'self'
               76  LOAD_METHOD              _compile
               78  LOAD_FAST                'body'
               80  LOAD_FAST                'type_name'
               82  LOAD_FAST                'size'
               84  LOAD_CONST               ('type', 'size')
               86  BUILD_CONST_KEY_MAP_2     2 
               88  BINARY_MODULO    

 L. 269        90  LOAD_FAST                'headers'

 L. 269        92  LOAD_FAST                'include_dirs'

 L. 269        94  LOAD_STR                 'c'

 L. 268        96  CALL_METHOD_4         4  ''
               98  POP_TOP          

 L. 270       100  LOAD_FAST                'self'
              102  LOAD_METHOD              _clean
              104  CALL_METHOD_0         0  ''
              106  POP_TOP          

 L. 271       108  LOAD_FAST                'size'
              110  POP_BLOCK        
              112  ROT_TWO          
              114  POP_TOP          
              116  RETURN_VALUE     
            118_0  COME_FROM_FINALLY    72  '72'

 L. 272       118  DUP_TOP          
              120  LOAD_GLOBAL              CompileError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   136  'to 136'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 273       132  POP_EXCEPT       
              134  JUMP_BACK            68  'to 68'
            136_0  COME_FROM           124  '124'
              136  END_FINALLY      
              138  JUMP_BACK            68  'to 68'
            140_0  COME_FROM            68  '68'
            140_1  COME_FROM            52  '52'

 L. 276       140  LOAD_GLOBAL              textwrap
              142  LOAD_METHOD              dedent
              144  LOAD_STR                 '\n            typedef %(type)s npy_check_sizeof_type;\n            int main (void)\n            {\n                static int test_array [1 - 2 * !(((long) (sizeof (npy_check_sizeof_type))) <= %(size)s)];\n                test_array [0] = 0\n\n                ;\n                return 0;\n            }\n            '
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'body'

 L. 291       150  LOAD_CONST               0
              152  STORE_FAST               'low'

 L. 292       154  LOAD_CONST               0
              156  STORE_FAST               'mid'
            158_0  COME_FROM           242  '242'
            158_1  COME_FROM           238  '238'
            158_2  COME_FROM           200  '200'

 L. 294       158  SETUP_FINALLY       202  'to 202'

 L. 295       160  LOAD_FAST                'self'
              162  LOAD_METHOD              _compile
              164  LOAD_FAST                'body'
              166  LOAD_FAST                'type_name'
              168  LOAD_FAST                'mid'
              170  LOAD_CONST               ('type', 'size')
              172  BUILD_CONST_KEY_MAP_2     2 
              174  BINARY_MODULO    

 L. 296       176  LOAD_FAST                'headers'

 L. 296       178  LOAD_FAST                'include_dirs'

 L. 296       180  LOAD_STR                 'c'

 L. 295       182  CALL_METHOD_4         4  ''
              184  POP_TOP          

 L. 297       186  LOAD_FAST                'self'
              188  LOAD_METHOD              _clean
              190  CALL_METHOD_0         0  ''
              192  POP_TOP          

 L. 298       194  POP_BLOCK        
              196  BREAK_LOOP          244  'to 244'
              198  POP_BLOCK        
              200  JUMP_BACK           158  'to 158'
            202_0  COME_FROM_FINALLY   158  '158'

 L. 299       202  DUP_TOP          
              204  LOAD_GLOBAL              CompileError
              206  COMPARE_OP               exception-match
              208  POP_JUMP_IF_FALSE   240  'to 240'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L. 301       216  LOAD_FAST                'mid'
              218  LOAD_CONST               1
              220  BINARY_ADD       
              222  STORE_FAST               'low'

 L. 302       224  LOAD_CONST               2
              226  LOAD_FAST                'mid'
              228  BINARY_MULTIPLY  
              230  LOAD_CONST               1
              232  BINARY_ADD       
              234  STORE_FAST               'mid'
              236  POP_EXCEPT       
              238  JUMP_BACK           158  'to 158'
            240_0  COME_FROM           208  '208'
              240  END_FINALLY      
              242  JUMP_BACK           158  'to 158'
            244_0  COME_FROM           196  '196'

 L. 304       244  LOAD_FAST                'mid'
              246  STORE_FAST               'high'
            248_0  COME_FROM           348  '348'
            248_1  COME_FROM           344  '344'
            248_2  COME_FROM           316  '316'

 L. 306       248  LOAD_FAST                'low'
              250  LOAD_FAST                'high'
              252  COMPARE_OP               !=
          254_256  POP_JUMP_IF_FALSE   350  'to 350'

 L. 307       258  LOAD_FAST                'high'
              260  LOAD_FAST                'low'
              262  BINARY_SUBTRACT  
              264  LOAD_CONST               2
              266  BINARY_FLOOR_DIVIDE
              268  LOAD_FAST                'low'
              270  BINARY_ADD       
              272  STORE_FAST               'mid'

 L. 308       274  SETUP_FINALLY       318  'to 318'

 L. 309       276  LOAD_FAST                'self'
              278  LOAD_METHOD              _compile
              280  LOAD_FAST                'body'
              282  LOAD_FAST                'type_name'
              284  LOAD_FAST                'mid'
              286  LOAD_CONST               ('type', 'size')
              288  BUILD_CONST_KEY_MAP_2     2 
              290  BINARY_MODULO    

 L. 310       292  LOAD_FAST                'headers'

 L. 310       294  LOAD_FAST                'include_dirs'

 L. 310       296  LOAD_STR                 'c'

 L. 309       298  CALL_METHOD_4         4  ''
              300  POP_TOP          

 L. 311       302  LOAD_FAST                'self'
              304  LOAD_METHOD              _clean
              306  CALL_METHOD_0         0  ''
              308  POP_TOP          

 L. 312       310  LOAD_FAST                'mid'
              312  STORE_FAST               'high'
              314  POP_BLOCK        
              316  JUMP_BACK           248  'to 248'
            318_0  COME_FROM_FINALLY   274  '274'

 L. 313       318  DUP_TOP          
              320  LOAD_GLOBAL              CompileError
              322  COMPARE_OP               exception-match
          324_326  POP_JUMP_IF_FALSE   346  'to 346'
              328  POP_TOP          
              330  POP_TOP          
              332  POP_TOP          

 L. 314       334  LOAD_FAST                'mid'
              336  LOAD_CONST               1
              338  BINARY_ADD       
              340  STORE_FAST               'low'
              342  POP_EXCEPT       
              344  JUMP_BACK           248  'to 248'
            346_0  COME_FROM           324  '324'
              346  END_FINALLY      
              348  JUMP_BACK           248  'to 248'
            350_0  COME_FROM           254  '254'

 L. 315       350  LOAD_FAST                'low'
              352  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 112

    def check_func(self, func, headers=None, include_dirs=None, libraries=None, library_dirs=None, decl=False, call=False, call_args=None):
        self._check_compiler()
        body = []
        if decl:
            if type(decl) == str:
                body.append(decl)
            else:
                body.append('int %s (void);' % func)
        body.append('#ifdef _MSC_VER')
        body.append('#pragma function(%s)' % func)
        body.append('#endif')
        body.append('int main (void) {')
        if call:
            if call_args is None:
                call_args = ''
            body.append('  %s(%s);' % (func, call_args))
        else:
            body.append('  %s;' % func)
        body.append('  return 0;')
        body.append('}')
        body = '\n'.join(body) + '\n'
        return self.try_link(body, headers, include_dirs, libraries, library_dirs)

    def check_funcs_once(self, funcs, headers=None, include_dirs=None, libraries=None, library_dirs=None, decl=False, call=False, call_args=None):
        """Check a list of functions at once.

        This is useful to speed up things, since all the functions in the funcs
        list will be put in one compilation unit.

        Arguments
        ---------
        funcs : seq
            list of functions to test
        include_dirs : seq
            list of header paths
        libraries : seq
            list of libraries to link the code snippet to
        library_dirs : seq
            list of library paths
        decl : dict
            for every (key, value), the declaration in the value will be
            used for function in key. If a function is not in the
            dictionary, no declaration will be used.
        call : dict
            for every item (f, value), if the value is True, a call will be
            done to the function f.
        """
        self._check_compiler()
        body = []
        if decl:
            for f, v in decl.items():
                if v:
                    body.append('int %s (void);' % f)

        body.append('#ifdef _MSC_VER')
        for func in funcs:
            body.append('#pragma function(%s)' % func)
        else:
            body.append('#endif')
            body.append('int main (void) {')
            if call:
                for f in funcs:
                    if f in call and call[f]:
                        if call_args:
                            if not (f in call_args and call_args[f]):
                                args = ''
                            else:
                                args = call_args[f]
                            body.append('  %s(%s);' % (f, args))
                    else:
                        body.append('  %s;' % f)

            else:
                pass
            for f in funcs:
                body.append('  %s;' % f)
            else:
                body.append('  return 0;')
                body.append('}')
                body = '\n'.join(body) + '\n'
                return self.try_link(body, headers, include_dirs, libraries, library_dirs)

    def check_inline(self):
        """Return the inline keyword recognized by the compiler, empty string
        otherwise."""
        return check_inline(self)

    def check_restrict(self):
        """Return the restrict keyword recognized by the compiler, empty string
        otherwise."""
        return check_restrict(self)

    def check_compiler_gcc4(self):
        """Return True if the C compiler is gcc >= 4."""
        return check_compiler_gcc4(self)

    def check_gcc_function_attribute(self, attribute, name):
        return check_gcc_function_attribute(self, attribute, name)

    def check_gcc_function_attribute_with_intrinsics(self, attribute, name, code, include):
        return check_gcc_function_attribute_with_intrinsics(self, attribute, name, code, include)

    def check_gcc_variable_attribute(self, attribute):
        return check_gcc_variable_attribute(self, attribute)

    def get_output(self, body, headers=None, include_dirs=None, libraries=None, library_dirs=None, lang='c', use_tee=None):
        """Try to compile, link to an executable, and run a program
        built from 'body' and 'headers'. Returns the exit status code
        of the program and its output.
        """
        warnings.warn('\n+++++++++++++++++++++++++++++++++++++++++++++++++\nUsage of get_output is deprecated: please do not \nuse it anymore, and avoid configuration checks \ninvolving running executable on the target machine.\n+++++++++++++++++++++++++++++++++++++++++++++++++\n', DeprecationWarning,
          stacklevel=2)
        self._check_compiler()
        exitcode, output = (255, '')
        try:
            grabber = GrabStdout()
            try:
                src, obj, exe = self._link(body, headers, include_dirs, libraries, library_dirs, lang)
                grabber.restore()
            except Exception:
                output = grabber.data
                grabber.restore()
                raise
            else:
                exe = os.path.join'.'exe
                try:
                    output = subprocess.check_output([exe], cwd='.')
                except subprocess.CalledProcessError as exc:
                    try:
                        exitstatus = exc.returncode
                        output = ''
                    finally:
                        exc = None
                        del exc

                except OSError:
                    exitstatus = 127
                    output = ''
                else:
                    output = filepath_from_subprocess_output(output)
                if hasattr(os, 'WEXITSTATUS'):
                    exitcode = os.WEXITSTATUS(exitstatus)
                    if os.WIFSIGNALED(exitstatus):
                        sig = os.WTERMSIG(exitstatus)
                        log.error('subprocess exited with signal %d' % (sig,))
                        if sig == signal.SIGINT:
                            raise KeyboardInterrupt
                else:
                    exitcode = exitstatus
                log.info('success!')
        except (CompileError, LinkError):
            log.info('failure.')
        else:
            self._clean()
            return (
             exitcode, output)


class GrabStdout(object):

    def __init__(self):
        self.sys_stdout = sys.stdout
        self.data = ''
        sys.stdout = self

    def write(self, data):
        self.sys_stdout.write(data)
        self.data += data

    def flush(self):
        self.sys_stdout.flush()

    def restore(self):
        sys.stdout = self.sys_stdout