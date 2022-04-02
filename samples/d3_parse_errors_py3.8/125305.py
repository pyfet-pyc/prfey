# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\distutils\command\build_clib.py
""" Modified version of build_clib that handles fortran source files.
"""
import os
from glob import glob
import shutil
import distutils.command.build_clib as old_build_clib
from distutils.errors import DistutilsSetupError, DistutilsError, DistutilsFileError
from numpy.distutils import log
from distutils.dep_util import newer_group
from numpy.distutils.misc_util import filter_sources, get_lib_source_files, get_numpy_include_dirs, has_cxx_sources, has_f_sources, is_sequence
_l = old_build_clib.user_options
for _i in range(len(_l)):
    if _l[_i][0] in ('build-clib', 'build-temp'):
        _l[_i] = (
         _l[_i][0] + '=',) + _l[_i][1:]
else:

    class build_clib(old_build_clib):
        description = 'build C/C++/F libraries used by Python extensions'
        user_options = old_build_clib.user_options + [
         ('fcompiler=', None, 'specify the Fortran compiler type'),
         ('inplace', 'i', 'Build in-place'),
         ('parallel=', 'j', 'number of parallel jobs'),
         ('warn-error', None, 'turn all warnings into errors (-Werror)')]
        boolean_options = old_build_clib.boolean_options + ['inplace', 'warn-error']

        def initialize_options(self):
            old_build_clib.initialize_options(self)
            self.fcompiler = None
            self.inplace = 0
            self.parallel = None
            self.warn_error = None

        def finalize_options(self):
            if self.parallel:
                try:
                    self.parallel = int(self.parallel)
                except ValueError as e:
                    try:
                        raise ValueError('--parallel/-j argument must be an integer') from e
                    finally:
                        e = None
                        del e

            old_build_clib.finalize_options(self)
            self.set_undefined_options('build', ('parallel', 'parallel'), ('warn_error',
                                                                           'warn_error'))

        def have_f_sources(self):
            for lib_name, build_info in self.libraries:
                if has_f_sources(build_info.get('sources', [])):
                    return True
            else:
                return False

        def have_cxx_sources(self):
            for lib_name, build_info in self.libraries:
                if has_cxx_sources(build_info.get('sources', [])):
                    return True
            else:
                return False

        def run(self):
            if not self.libraries:
                return
            languages = []
            self.run_command('build_src')
            for lib_name, build_info in self.libraries:
                l = build_info.get('language', None)
                if l:
                    if l not in languages:
                        languages.append(l)
            else:
                from distutils.ccompiler import new_compiler
                self.compiler = new_compiler(compiler=(self.compiler), dry_run=(self.dry_run),
                  force=(self.force))
                self.compiler.customize((self.distribution), need_cxx=(self.have_cxx_sources()))
                if self.warn_error:
                    self.compiler.compiler.append('-Werror')
                    self.compiler.compiler_so.append('-Werror')
                libraries = self.libraries
                self.libraries = None
                self.compiler.customize_cmd(self)
                self.libraries = libraries
                self.compiler.show_customization()
                if self.have_f_sources():
                    from numpy.distutils.fcompiler import new_fcompiler
                    self._f_compiler = new_fcompiler(compiler=(self.fcompiler), verbose=(self.verbose),
                      dry_run=(self.dry_run),
                      force=(self.force),
                      requiref90=('f90' in languages),
                      c_compiler=(self.compiler))
                    if self._f_compiler is not None:
                        self._f_compiler.customize(self.distribution)
                        libraries = self.libraries
                        self.libraries = None
                        self._f_compiler.customize_cmd(self)
                        self.libraries = libraries
                        self._f_compiler.show_customization()
                else:
                    self._f_compiler = None
                self.build_libraries(self.libraries)
                if self.inplace:
                    for l in self.distribution.installed_libraries:
                        libname = self.compiler.library_filename(l.name)
                        source = os.path.join(self.build_clib, libname)
                        target = os.path.join(l.target_dir, libname)
                        self.mkpath(l.target_dir)
                        shutil.copy(source, target)

        def get_source_files(self):
            self.check_library_list(self.libraries)
            filenames = []
            for lib in self.libraries:
                filenames.extend(get_lib_source_files(lib))
            else:
                return filenames

        def build_libraries(self, libraries):
            for lib_name, build_info in libraries:
                self.build_a_library(build_info, lib_name, libraries)

        def build_a_library--- This code section failed: ---

 L. 148         0  LOAD_FAST                'self'
                2  LOAD_ATTR                compiler
                4  STORE_FAST               'compiler'

 L. 149         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _f_compiler
               10  STORE_FAST               'fcompiler'

 L. 151        12  LOAD_FAST                'build_info'
               14  LOAD_METHOD              get
               16  LOAD_STR                 'sources'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'sources'

 L. 152        22  LOAD_FAST                'sources'
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_TRUE     38  'to 38'
               30  LOAD_GLOBAL              is_sequence
               32  LOAD_FAST                'sources'
               34  CALL_FUNCTION_1       1  ''
               36  POP_JUMP_IF_TRUE     50  'to 50'
             38_0  COME_FROM            28  '28'

 L. 153        38  LOAD_GLOBAL              DistutilsSetupError
               40  LOAD_STR                 "in 'libraries' option (library '%s'), 'sources' must be present and must be a list of source filenames"

 L. 155        42  LOAD_FAST                'lib_name'

 L. 153        44  BINARY_MODULO    
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            36  '36'

 L. 156        50  LOAD_GLOBAL              list
               52  LOAD_FAST                'sources'
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'sources'

 L. 159        58  LOAD_GLOBAL              filter_sources
               60  LOAD_FAST                'sources'
               62  CALL_FUNCTION_1       1  ''

 L. 158        64  UNPACK_SEQUENCE_4     4 
               66  STORE_FAST               'c_sources'
               68  STORE_FAST               'cxx_sources'
               70  STORE_FAST               'f_sources'
               72  STORE_FAST               'fmodule_sources'

 L. 160        74  LOAD_FAST                'fmodule_sources'
               76  UNARY_NOT        
               78  UNARY_NOT        
               80  JUMP_IF_TRUE_OR_POP    96  'to 96'

 L. 161        82  LOAD_FAST                'build_info'
               84  LOAD_METHOD              get
               86  LOAD_STR                 'language'
               88  LOAD_STR                 'c'
               90  CALL_METHOD_2         2  ''
               92  LOAD_STR                 'f90'
               94  COMPARE_OP               ==
             96_0  COME_FROM            80  '80'

 L. 160        96  STORE_FAST               'requiref90'

 L. 164        98  BUILD_LIST_0          0 
              100  STORE_FAST               'source_languages'

 L. 165       102  LOAD_FAST                'c_sources'
              104  POP_JUMP_IF_FALSE   116  'to 116'

 L. 166       106  LOAD_FAST                'source_languages'
              108  LOAD_METHOD              append
              110  LOAD_STR                 'c'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
            116_0  COME_FROM           104  '104'

 L. 167       116  LOAD_FAST                'cxx_sources'
              118  POP_JUMP_IF_FALSE   130  'to 130'

 L. 168       120  LOAD_FAST                'source_languages'
              122  LOAD_METHOD              append
              124  LOAD_STR                 'c++'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
            130_0  COME_FROM           118  '118'

 L. 169       130  LOAD_FAST                'requiref90'
              132  POP_JUMP_IF_FALSE   146  'to 146'

 L. 170       134  LOAD_FAST                'source_languages'
              136  LOAD_METHOD              append
              138  LOAD_STR                 'f90'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_FORWARD        160  'to 160'
            146_0  COME_FROM           132  '132'

 L. 171       146  LOAD_FAST                'f_sources'
              148  POP_JUMP_IF_FALSE   160  'to 160'

 L. 172       150  LOAD_FAST                'source_languages'
              152  LOAD_METHOD              append
              154  LOAD_STR                 'f77'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
            160_0  COME_FROM           148  '148'
            160_1  COME_FROM           144  '144'

 L. 173       160  LOAD_FAST                'source_languages'
              162  LOAD_FAST                'build_info'
              164  LOAD_STR                 'source_languages'
              166  STORE_SUBSCR     

 L. 175       168  LOAD_FAST                'compiler'
              170  LOAD_ATTR                library_filename
              172  LOAD_FAST                'lib_name'

 L. 176       174  LOAD_FAST                'self'
              176  LOAD_ATTR                build_clib

 L. 175       178  LOAD_CONST               ('output_dir',)
              180  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              182  STORE_FAST               'lib_file'

 L. 177       184  LOAD_FAST                'sources'
              186  LOAD_FAST                'build_info'
              188  LOAD_METHOD              get
              190  LOAD_STR                 'depends'
              192  BUILD_LIST_0          0 
              194  CALL_METHOD_2         2  ''
              196  BINARY_ADD       
              198  STORE_FAST               'depends'

 L. 178       200  LOAD_FAST                'self'
              202  LOAD_ATTR                force
              204  POP_JUMP_IF_TRUE    234  'to 234'
              206  LOAD_GLOBAL              newer_group
              208  LOAD_FAST                'depends'
              210  LOAD_FAST                'lib_file'
              212  LOAD_STR                 'newer'
              214  CALL_FUNCTION_3       3  ''
              216  POP_JUMP_IF_TRUE    234  'to 234'

 L. 179       218  LOAD_GLOBAL              log
              220  LOAD_METHOD              debug
              222  LOAD_STR                 "skipping '%s' library (up-to-date)"
              224  LOAD_FAST                'lib_name'
              226  CALL_METHOD_2         2  ''
              228  POP_TOP          

 L. 180       230  LOAD_CONST               None
              232  RETURN_VALUE     
            234_0  COME_FROM           216  '216'
            234_1  COME_FROM           204  '204'

 L. 182       234  LOAD_GLOBAL              log
              236  LOAD_METHOD              info
              238  LOAD_STR                 "building '%s' library"
              240  LOAD_FAST                'lib_name'
              242  CALL_METHOD_2         2  ''
              244  POP_TOP          

 L. 184       246  LOAD_FAST                'build_info'
              248  LOAD_METHOD              get
              250  LOAD_STR                 'config_fc'
              252  BUILD_MAP_0           0 
              254  CALL_METHOD_2         2  ''
              256  STORE_FAST               'config_fc'

 L. 185       258  LOAD_FAST                'fcompiler'
              260  LOAD_CONST               None
              262  COMPARE_OP               is-not
          264_266  POP_JUMP_IF_FALSE   382  'to 382'
              268  LOAD_FAST                'config_fc'
          270_272  POP_JUMP_IF_FALSE   382  'to 382'

 L. 186       274  LOAD_GLOBAL              log
              276  LOAD_METHOD              info
              278  LOAD_STR                 'using additional config_fc from setup script for fortran compiler: %s'

 L. 188       280  LOAD_FAST                'config_fc'
              282  BUILD_TUPLE_1         1 

 L. 186       284  BINARY_MODULO    
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

 L. 189       290  LOAD_CONST               0
              292  LOAD_CONST               ('new_fcompiler',)
              294  IMPORT_NAME_ATTR         numpy.distutils.fcompiler
              296  IMPORT_FROM              new_fcompiler
              298  STORE_FAST               'new_fcompiler'
              300  POP_TOP          

 L. 190       302  LOAD_FAST                'new_fcompiler'
              304  LOAD_FAST                'fcompiler'
              306  LOAD_ATTR                compiler_type

 L. 191       308  LOAD_FAST                'self'
              310  LOAD_ATTR                verbose

 L. 192       312  LOAD_FAST                'self'
              314  LOAD_ATTR                dry_run

 L. 193       316  LOAD_FAST                'self'
              318  LOAD_ATTR                force

 L. 194       320  LOAD_FAST                'requiref90'

 L. 195       322  LOAD_FAST                'self'
              324  LOAD_ATTR                compiler

 L. 190       326  LOAD_CONST               ('compiler', 'verbose', 'dry_run', 'force', 'requiref90', 'c_compiler')
              328  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              330  STORE_FAST               'fcompiler'

 L. 196       332  LOAD_FAST                'fcompiler'
              334  LOAD_CONST               None
              336  COMPARE_OP               is-not
          338_340  POP_JUMP_IF_FALSE   382  'to 382'

 L. 197       342  LOAD_FAST                'self'
              344  LOAD_ATTR                distribution
              346  STORE_FAST               'dist'

 L. 198       348  LOAD_FAST                'dist'
              350  LOAD_METHOD              get_option_dict
              352  LOAD_STR                 'config_fc'
              354  CALL_METHOD_1         1  ''
              356  LOAD_METHOD              copy
              358  CALL_METHOD_0         0  ''
              360  STORE_FAST               'base_config_fc'

 L. 199       362  LOAD_FAST                'base_config_fc'
              364  LOAD_METHOD              update
              366  LOAD_FAST                'config_fc'
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          

 L. 200       372  LOAD_FAST                'fcompiler'
              374  LOAD_METHOD              customize
              376  LOAD_FAST                'base_config_fc'
              378  CALL_METHOD_1         1  ''
              380  POP_TOP          
            382_0  COME_FROM           338  '338'
            382_1  COME_FROM           270  '270'
            382_2  COME_FROM           264  '264'

 L. 203       382  LOAD_FAST                'f_sources'
          384_386  POP_JUMP_IF_TRUE    394  'to 394'
              388  LOAD_FAST                'fmodule_sources'
          390_392  POP_JUMP_IF_FALSE   416  'to 416'
            394_0  COME_FROM           384  '384'
              394  LOAD_FAST                'fcompiler'
              396  LOAD_CONST               None
              398  COMPARE_OP               is
          400_402  POP_JUMP_IF_FALSE   416  'to 416'

 L. 204       404  LOAD_GLOBAL              DistutilsError
              406  LOAD_STR                 'library %s has Fortran sources but no Fortran compiler found'

 L. 205       408  LOAD_FAST                'lib_name'

 L. 204       410  BINARY_MODULO    
              412  CALL_FUNCTION_1       1  ''
              414  RAISE_VARARGS_1       1  'exception instance'
            416_0  COME_FROM           400  '400'
            416_1  COME_FROM           390  '390'

 L. 207       416  LOAD_FAST                'fcompiler'
              418  LOAD_CONST               None
              420  COMPARE_OP               is-not
          422_424  POP_JUMP_IF_FALSE   462  'to 462'

 L. 208       426  LOAD_FAST                'build_info'
              428  LOAD_METHOD              get

 L. 209       430  LOAD_STR                 'extra_f77_compile_args'

 L. 208       432  CALL_METHOD_1         1  ''
          434_436  JUMP_IF_TRUE_OR_POP   440  'to 440'

 L. 209       438  BUILD_LIST_0          0 
            440_0  COME_FROM           434  '434'

 L. 208       440  LOAD_FAST                'fcompiler'
              442  STORE_ATTR               extra_f77_compile_args

 L. 210       444  LOAD_FAST                'build_info'
              446  LOAD_METHOD              get

 L. 211       448  LOAD_STR                 'extra_f90_compile_args'

 L. 210       450  CALL_METHOD_1         1  ''
          452_454  JUMP_IF_TRUE_OR_POP   458  'to 458'

 L. 211       456  BUILD_LIST_0          0 
            458_0  COME_FROM           452  '452'

 L. 210       458  LOAD_FAST                'fcompiler'
              460  STORE_ATTR               extra_f90_compile_args
            462_0  COME_FROM           422  '422'

 L. 213       462  LOAD_FAST                'build_info'
              464  LOAD_METHOD              get
              466  LOAD_STR                 'macros'
              468  CALL_METHOD_1         1  ''
              470  STORE_FAST               'macros'

 L. 214       472  LOAD_FAST                'build_info'
              474  LOAD_METHOD              get
              476  LOAD_STR                 'include_dirs'
              478  CALL_METHOD_1         1  ''
              480  STORE_FAST               'include_dirs'

 L. 215       482  LOAD_FAST                'include_dirs'
              484  LOAD_CONST               None
              486  COMPARE_OP               is
          488_490  POP_JUMP_IF_FALSE   496  'to 496'

 L. 216       492  BUILD_LIST_0          0 
              494  STORE_FAST               'include_dirs'
            496_0  COME_FROM           488  '488'

 L. 217       496  LOAD_FAST                'build_info'
              498  LOAD_METHOD              get
              500  LOAD_STR                 'extra_compiler_args'
              502  CALL_METHOD_1         1  ''
          504_506  JUMP_IF_TRUE_OR_POP   510  'to 510'
              508  BUILD_LIST_0          0 
            510_0  COME_FROM           504  '504'
              510  STORE_FAST               'extra_postargs'

 L. 219       512  LOAD_FAST                'include_dirs'
              514  LOAD_METHOD              extend
              516  LOAD_GLOBAL              get_numpy_include_dirs
              518  CALL_FUNCTION_0       0  ''
              520  CALL_METHOD_1         1  ''
              522  POP_TOP          

 L. 221       524  LOAD_FAST                'build_info'
              526  LOAD_METHOD              get
              528  LOAD_STR                 'module_dirs'
              530  CALL_METHOD_1         1  ''
          532_534  JUMP_IF_TRUE_OR_POP   538  'to 538'
              536  BUILD_LIST_0          0 
            538_0  COME_FROM           532  '532'
              538  STORE_FAST               'module_dirs'

 L. 222       540  LOAD_GLOBAL              os
              542  LOAD_ATTR                path
              544  LOAD_METHOD              dirname
              546  LOAD_FAST                'lib_file'
              548  CALL_METHOD_1         1  ''
              550  STORE_FAST               'module_build_dir'

 L. 223       552  LOAD_FAST                'requiref90'
          554_556  POP_JUMP_IF_FALSE   568  'to 568'

 L. 224       558  LOAD_FAST                'self'
              560  LOAD_METHOD              mkpath
              562  LOAD_FAST                'module_build_dir'
              564  CALL_METHOD_1         1  ''
              566  POP_TOP          
            568_0  COME_FROM           554  '554'

 L. 226       568  LOAD_FAST                'compiler'
              570  LOAD_ATTR                compiler_type
              572  LOAD_STR                 'msvc'
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   592  'to 592'

 L. 229       580  LOAD_FAST                'c_sources'
              582  LOAD_FAST                'cxx_sources'
              584  INPLACE_ADD      
              586  STORE_FAST               'c_sources'

 L. 230       588  BUILD_LIST_0          0 
              590  STORE_FAST               'cxx_sources'
            592_0  COME_FROM           576  '576'

 L. 232       592  BUILD_LIST_0          0 
              594  STORE_FAST               'objects'

 L. 233       596  LOAD_FAST                'c_sources'
          598_600  POP_JUMP_IF_FALSE   638  'to 638'

 L. 234       602  LOAD_GLOBAL              log
              604  LOAD_METHOD              info
              606  LOAD_STR                 'compiling C sources'
              608  CALL_METHOD_1         1  ''
              610  POP_TOP          

 L. 235       612  LOAD_FAST                'compiler'
              614  LOAD_ATTR                compile
              616  LOAD_FAST                'c_sources'

 L. 236       618  LOAD_FAST                'self'
              620  LOAD_ATTR                build_temp

 L. 237       622  LOAD_FAST                'macros'

 L. 238       624  LOAD_FAST                'include_dirs'

 L. 239       626  LOAD_FAST                'self'
              628  LOAD_ATTR                debug

 L. 240       630  LOAD_FAST                'extra_postargs'

 L. 235       632  LOAD_CONST               ('output_dir', 'macros', 'include_dirs', 'debug', 'extra_postargs')
              634  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              636  STORE_FAST               'objects'
            638_0  COME_FROM           598  '598'

 L. 242       638  LOAD_FAST                'cxx_sources'
          640_642  POP_JUMP_IF_FALSE   698  'to 698'

 L. 243       644  LOAD_GLOBAL              log
              646  LOAD_METHOD              info
              648  LOAD_STR                 'compiling C++ sources'
              650  CALL_METHOD_1         1  ''
              652  POP_TOP          

 L. 244       654  LOAD_FAST                'compiler'
              656  LOAD_METHOD              cxx_compiler
              658  CALL_METHOD_0         0  ''
              660  STORE_FAST               'cxx_compiler'

 L. 245       662  LOAD_FAST                'cxx_compiler'
              664  LOAD_ATTR                compile
              666  LOAD_FAST                'cxx_sources'

 L. 246       668  LOAD_FAST                'self'
              670  LOAD_ATTR                build_temp

 L. 247       672  LOAD_FAST                'macros'

 L. 248       674  LOAD_FAST                'include_dirs'

 L. 249       676  LOAD_FAST                'self'
              678  LOAD_ATTR                debug

 L. 250       680  LOAD_FAST                'extra_postargs'

 L. 245       682  LOAD_CONST               ('output_dir', 'macros', 'include_dirs', 'debug', 'extra_postargs')
              684  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              686  STORE_FAST               'cxx_objects'

 L. 251       688  LOAD_FAST                'objects'
              690  LOAD_METHOD              extend
              692  LOAD_FAST                'cxx_objects'
              694  CALL_METHOD_1         1  ''
              696  POP_TOP          
            698_0  COME_FROM           640  '640'

 L. 253       698  LOAD_FAST                'f_sources'
          700_702  POP_JUMP_IF_TRUE    710  'to 710'
              704  LOAD_FAST                'fmodule_sources'
          706_708  POP_JUMP_IF_FALSE  1030  'to 1030'
            710_0  COME_FROM           700  '700'

 L. 254       710  BUILD_LIST_0          0 
              712  STORE_FAST               'extra_postargs'

 L. 255       714  BUILD_LIST_0          0 
              716  STORE_FAST               'f_objects'

 L. 257       718  LOAD_FAST                'requiref90'
          720_722  POP_JUMP_IF_FALSE   760  'to 760'

 L. 258       724  LOAD_FAST                'fcompiler'
              726  LOAD_ATTR                module_dir_switch
              728  LOAD_CONST               None
              730  COMPARE_OP               is
          732_734  POP_JUMP_IF_FALSE   744  'to 744'

 L. 259       736  LOAD_GLOBAL              glob
              738  LOAD_STR                 '*.mod'
              740  CALL_FUNCTION_1       1  ''
              742  STORE_FAST               'existing_modules'
            744_0  COME_FROM           732  '732'

 L. 260       744  LOAD_FAST                'extra_postargs'
              746  LOAD_FAST                'fcompiler'
              748  LOAD_METHOD              module_options

 L. 261       750  LOAD_FAST                'module_dirs'

 L. 261       752  LOAD_FAST                'module_build_dir'

 L. 260       754  CALL_METHOD_2         2  ''
              756  INPLACE_ADD      
              758  STORE_FAST               'extra_postargs'
            760_0  COME_FROM           720  '720'

 L. 263       760  LOAD_FAST                'fmodule_sources'
          762_764  POP_JUMP_IF_FALSE   806  'to 806'

 L. 264       766  LOAD_GLOBAL              log
              768  LOAD_METHOD              info
              770  LOAD_STR                 'compiling Fortran 90 module sources'
              772  CALL_METHOD_1         1  ''
              774  POP_TOP          

 L. 265       776  LOAD_FAST                'f_objects'
              778  LOAD_FAST                'fcompiler'
              780  LOAD_ATTR                compile
              782  LOAD_FAST                'fmodule_sources'

 L. 266       784  LOAD_FAST                'self'
              786  LOAD_ATTR                build_temp

 L. 267       788  LOAD_FAST                'macros'

 L. 268       790  LOAD_FAST                'include_dirs'

 L. 269       792  LOAD_FAST                'self'
              794  LOAD_ATTR                debug

 L. 270       796  LOAD_FAST                'extra_postargs'

 L. 265       798  LOAD_CONST               ('output_dir', 'macros', 'include_dirs', 'debug', 'extra_postargs')
              800  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              802  INPLACE_ADD      
              804  STORE_FAST               'f_objects'
            806_0  COME_FROM           762  '762'

 L. 272       806  LOAD_FAST                'requiref90'
          808_810  POP_JUMP_IF_FALSE   982  'to 982'
              812  LOAD_FAST                'self'
              814  LOAD_ATTR                _f_compiler
              816  LOAD_ATTR                module_dir_switch
              818  LOAD_CONST               None
              820  COMPARE_OP               is
          822_824  POP_JUMP_IF_FALSE   982  'to 982'

 L. 274       826  LOAD_GLOBAL              glob
              828  LOAD_STR                 '*.mod'
              830  CALL_FUNCTION_1       1  ''
              832  GET_ITER         
            834_0  COME_FROM           978  '978'
            834_1  COME_FROM           974  '974'
            834_2  COME_FROM           936  '936'
            834_3  COME_FROM           892  '892'
            834_4  COME_FROM           848  '848'
              834  FOR_ITER            982  'to 982'
              836  STORE_FAST               'f'

 L. 275       838  LOAD_FAST                'f'
              840  LOAD_FAST                'existing_modules'
              842  COMPARE_OP               in
          844_846  POP_JUMP_IF_FALSE   852  'to 852'

 L. 276   848_850  JUMP_BACK           834  'to 834'
            852_0  COME_FROM           844  '844'

 L. 277       852  LOAD_GLOBAL              os
              854  LOAD_ATTR                path
              856  LOAD_METHOD              join
              858  LOAD_FAST                'module_build_dir'
              860  LOAD_FAST                'f'
              862  CALL_METHOD_2         2  ''
              864  STORE_FAST               't'

 L. 278       866  LOAD_GLOBAL              os
              868  LOAD_ATTR                path
              870  LOAD_METHOD              abspath
              872  LOAD_FAST                'f'
              874  CALL_METHOD_1         1  ''
              876  LOAD_GLOBAL              os
              878  LOAD_ATTR                path
              880  LOAD_METHOD              abspath
              882  LOAD_FAST                't'
              884  CALL_METHOD_1         1  ''
              886  COMPARE_OP               ==
          888_890  POP_JUMP_IF_FALSE   896  'to 896'

 L. 279   892_894  JUMP_BACK           834  'to 834'
            896_0  COME_FROM           888  '888'

 L. 280       896  LOAD_GLOBAL              os
              898  LOAD_ATTR                path
              900  LOAD_METHOD              isfile
              902  LOAD_FAST                't'
              904  CALL_METHOD_1         1  ''
          906_908  POP_JUMP_IF_FALSE   920  'to 920'

 L. 281       910  LOAD_GLOBAL              os
              912  LOAD_METHOD              remove
              914  LOAD_FAST                't'
              916  CALL_METHOD_1         1  ''
              918  POP_TOP          
            920_0  COME_FROM           906  '906'

 L. 282       920  SETUP_FINALLY       938  'to 938'

 L. 283       922  LOAD_FAST                'self'
              924  LOAD_METHOD              move_file
              926  LOAD_FAST                'f'
              928  LOAD_FAST                'module_build_dir'
              930  CALL_METHOD_2         2  ''
              932  POP_TOP          
              934  POP_BLOCK        
              936  JUMP_BACK           834  'to 834'
            938_0  COME_FROM_FINALLY   920  '920'

 L. 284       938  DUP_TOP          
              940  LOAD_GLOBAL              DistutilsFileError
              942  COMPARE_OP               exception-match
          944_946  POP_JUMP_IF_FALSE   976  'to 976'
              948  POP_TOP          
              950  POP_TOP          
              952  POP_TOP          

 L. 285       954  LOAD_GLOBAL              log
              956  LOAD_METHOD              warn
              958  LOAD_STR                 'failed to move %r to %r'

 L. 286       960  LOAD_FAST                'f'
              962  LOAD_FAST                'module_build_dir'
              964  BUILD_TUPLE_2         2 

 L. 285       966  BINARY_MODULO    
              968  CALL_METHOD_1         1  ''
              970  POP_TOP          
              972  POP_EXCEPT       
              974  JUMP_BACK           834  'to 834'
            976_0  COME_FROM           944  '944'
              976  END_FINALLY      
          978_980  JUMP_BACK           834  'to 834'
            982_0  COME_FROM           834  '834'
            982_1  COME_FROM           822  '822'
            982_2  COME_FROM           808  '808'

 L. 288       982  LOAD_FAST                'f_sources'
          984_986  POP_JUMP_IF_FALSE  1034  'to 1034'

 L. 289       988  LOAD_GLOBAL              log
              990  LOAD_METHOD              info
              992  LOAD_STR                 'compiling Fortran sources'
              994  CALL_METHOD_1         1  ''
              996  POP_TOP          

 L. 290       998  LOAD_FAST                'f_objects'
             1000  LOAD_FAST                'fcompiler'
             1002  LOAD_ATTR                compile
             1004  LOAD_FAST                'f_sources'

 L. 291      1006  LOAD_FAST                'self'
             1008  LOAD_ATTR                build_temp

 L. 292      1010  LOAD_FAST                'macros'

 L. 293      1012  LOAD_FAST                'include_dirs'

 L. 294      1014  LOAD_FAST                'self'
             1016  LOAD_ATTR                debug

 L. 295      1018  LOAD_FAST                'extra_postargs'

 L. 290      1020  LOAD_CONST               ('output_dir', 'macros', 'include_dirs', 'debug', 'extra_postargs')
             1022  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1024  INPLACE_ADD      
             1026  STORE_FAST               'f_objects'
             1028  JUMP_FORWARD       1034  'to 1034'
           1030_0  COME_FROM           706  '706'

 L. 297      1030  BUILD_LIST_0          0 
             1032  STORE_FAST               'f_objects'
           1034_0  COME_FROM          1028  '1028'
           1034_1  COME_FROM           984  '984'

 L. 299      1034  LOAD_FAST                'f_objects'
         1036_1038  POP_JUMP_IF_FALSE  1234  'to 1234'
             1040  LOAD_FAST                'fcompiler'
             1042  LOAD_METHOD              can_ccompiler_link
             1044  LOAD_FAST                'compiler'
             1046  CALL_METHOD_1         1  ''
         1048_1050  POP_JUMP_IF_TRUE   1234  'to 1234'

 L. 303      1052  LOAD_GLOBAL              os
             1054  LOAD_ATTR                path
             1056  LOAD_METHOD              join
             1058  LOAD_FAST                'self'
             1060  LOAD_ATTR                build_clib

 L. 304      1062  LOAD_FAST                'lib_name'
             1064  LOAD_STR                 '.fobjects'
             1066  BINARY_ADD       

 L. 303      1068  CALL_METHOD_2         2  ''
             1070  STORE_FAST               'listfn'

 L. 305      1072  LOAD_GLOBAL              open
             1074  LOAD_FAST                'listfn'
             1076  LOAD_STR                 'w'
             1078  CALL_FUNCTION_2       2  ''
             1080  SETUP_WITH         1114  'to 1114'
             1082  STORE_FAST               'f'

 L. 306      1084  LOAD_FAST                'f'
             1086  LOAD_METHOD              write
             1088  LOAD_STR                 '\n'
             1090  LOAD_METHOD              join
             1092  LOAD_GENEXPR             '<code_object <genexpr>>'
             1094  LOAD_STR                 'build_clib.build_a_library.<locals>.<genexpr>'
             1096  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1098  LOAD_FAST                'f_objects'
             1100  GET_ITER         
             1102  CALL_FUNCTION_1       1  ''
             1104  CALL_METHOD_1         1  ''
             1106  CALL_METHOD_1         1  ''
             1108  POP_TOP          
             1110  POP_BLOCK        
             1112  BEGIN_FINALLY    
           1114_0  COME_FROM_WITH     1080  '1080'
             1114  WITH_CLEANUP_START
             1116  WITH_CLEANUP_FINISH
             1118  END_FINALLY      

 L. 308      1120  LOAD_GLOBAL              os
             1122  LOAD_ATTR                path
             1124  LOAD_METHOD              join
             1126  LOAD_FAST                'self'
             1128  LOAD_ATTR                build_clib

 L. 309      1130  LOAD_FAST                'lib_name'
             1132  LOAD_STR                 '.cobjects'
             1134  BINARY_ADD       

 L. 308      1136  CALL_METHOD_2         2  ''
             1138  STORE_FAST               'listfn'

 L. 310      1140  LOAD_GLOBAL              open
             1142  LOAD_FAST                'listfn'
             1144  LOAD_STR                 'w'
             1146  CALL_FUNCTION_2       2  ''
             1148  SETUP_WITH         1182  'to 1182'
             1150  STORE_FAST               'f'

 L. 311      1152  LOAD_FAST                'f'
             1154  LOAD_METHOD              write
             1156  LOAD_STR                 '\n'
             1158  LOAD_METHOD              join
             1160  LOAD_GENEXPR             '<code_object <genexpr>>'
             1162  LOAD_STR                 'build_clib.build_a_library.<locals>.<genexpr>'
             1164  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1166  LOAD_FAST                'objects'
             1168  GET_ITER         
             1170  CALL_FUNCTION_1       1  ''
             1172  CALL_METHOD_1         1  ''
             1174  CALL_METHOD_1         1  ''
             1176  POP_TOP          
             1178  POP_BLOCK        
             1180  BEGIN_FINALLY    
           1182_0  COME_FROM_WITH     1148  '1148'
             1182  WITH_CLEANUP_START
             1184  WITH_CLEANUP_FINISH
             1186  END_FINALLY      

 L. 314      1188  LOAD_GLOBAL              os
             1190  LOAD_ATTR                path
             1192  LOAD_METHOD              join
             1194  LOAD_FAST                'self'
             1196  LOAD_ATTR                build_clib

 L. 315      1198  LOAD_FAST                'lib_name'
             1200  LOAD_FAST                'compiler'
             1202  LOAD_ATTR                static_lib_extension
             1204  BINARY_ADD       

 L. 314      1206  CALL_METHOD_2         2  ''
             1208  STORE_FAST               'lib_fname'

 L. 316      1210  LOAD_GLOBAL              open
             1212  LOAD_FAST                'lib_fname'
             1214  LOAD_STR                 'wb'
             1216  CALL_FUNCTION_2       2  ''
             1218  SETUP_WITH         1226  'to 1226'
             1220  STORE_FAST               'f'

 L. 317      1222  POP_BLOCK        
             1224  BEGIN_FINALLY    
           1226_0  COME_FROM_WITH     1218  '1218'
             1226  WITH_CLEANUP_START
             1228  WITH_CLEANUP_FINISH
             1230  END_FINALLY      
             1232  JUMP_FORWARD       1266  'to 1266'
           1234_0  COME_FROM          1048  '1048'
           1234_1  COME_FROM          1036  '1036'

 L. 321      1234  LOAD_FAST                'objects'
             1236  LOAD_METHOD              extend
             1238  LOAD_FAST                'f_objects'
             1240  CALL_METHOD_1         1  ''
             1242  POP_TOP          

 L. 322      1244  LOAD_FAST                'compiler'
             1246  LOAD_ATTR                create_static_lib
             1248  LOAD_FAST                'objects'
             1250  LOAD_FAST                'lib_name'

 L. 323      1252  LOAD_FAST                'self'
             1254  LOAD_ATTR                build_clib

 L. 324      1256  LOAD_FAST                'self'
             1258  LOAD_ATTR                debug

 L. 322      1260  LOAD_CONST               ('output_dir', 'debug')
             1262  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1264  POP_TOP          
           1266_0  COME_FROM          1232  '1232'

 L. 327      1266  LOAD_FAST                'build_info'
             1268  LOAD_METHOD              get
             1270  LOAD_STR                 'libraries'
             1272  BUILD_LIST_0          0 
             1274  CALL_METHOD_2         2  ''
             1276  STORE_FAST               'clib_libraries'

 L. 328      1278  LOAD_FAST                'libraries'
             1280  GET_ITER         
           1282_0  COME_FROM          1318  '1318'
           1282_1  COME_FROM          1296  '1296'
             1282  FOR_ITER           1322  'to 1322'
             1284  UNPACK_SEQUENCE_2     2 
             1286  STORE_FAST               'lname'
             1288  STORE_FAST               'binfo'

 L. 329      1290  LOAD_FAST                'lname'
             1292  LOAD_FAST                'clib_libraries'
             1294  COMPARE_OP               in
         1296_1298  POP_JUMP_IF_FALSE_BACK  1282  'to 1282'

 L. 330      1300  LOAD_FAST                'clib_libraries'
             1302  LOAD_METHOD              extend
             1304  LOAD_FAST                'binfo'
             1306  LOAD_METHOD              get
             1308  LOAD_STR                 'libraries'
             1310  BUILD_LIST_0          0 
             1312  CALL_METHOD_2         2  ''
             1314  CALL_METHOD_1         1  ''
             1316  POP_TOP          
         1318_1320  JUMP_BACK          1282  'to 1282'
           1322_0  COME_FROM          1282  '1282'

 L. 331      1322  LOAD_FAST                'clib_libraries'
         1324_1326  POP_JUMP_IF_FALSE  1336  'to 1336'

 L. 332      1328  LOAD_FAST                'clib_libraries'
             1330  LOAD_FAST                'build_info'
             1332  LOAD_STR                 'libraries'
             1334  STORE_SUBSCR     
           1336_0  COME_FROM          1324  '1324'

Parse error at or near `BEGIN_FINALLY' instruction at offset 1224