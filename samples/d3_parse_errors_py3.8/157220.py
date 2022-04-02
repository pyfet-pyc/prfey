# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\command\build_clib.py
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
from numpy.distutils.ccompiler_opt import new_ccompiler_opt
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
         ('warn-error', None, 'turn all warnings into errors (-Werror)'),
         ('cpu-baseline=', None, 'specify a list of enabled baseline CPU optimizations'),
         ('cpu-dispatch=', None, 'specify a list of dispatched CPU optimizations'),
         ('disable-optimization', None, 'disable CPU optimized code(dispatch,simd,fast...)')]
        boolean_options = old_build_clib.boolean_options + [
         'inplace', 'warn-error', 'disable-optimization']

        def initialize_options(self):
            old_build_clib.initialize_options(self)
            self.fcompiler = None
            self.inplace = 0
            self.parallel = None
            self.warn_error = None
            self.cpu_baseline = None
            self.cpu_dispatch = None
            self.disable_optimization = None

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
                                                                           'warn_error'), ('cpu_baseline',
                                                                                           'cpu_baseline'), ('cpu_dispatch',
                                                                                                             'cpu_dispatch'), ('disable_optimization',
                                                                                                                               'disable_optimization'))

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
                if not self.disable_optimization:
                    dispatch_hpath = os.path.join('numpy', 'distutils', 'include', 'npy_cpu_dispatch_config.h')
                    dispatch_hpath = os.path.join(self.get_finalized_command('build_src').build_src, dispatch_hpath)
                    opt_cache_path = os.path.abspath(os.path.join(self.build_temp, 'ccompiler_opt_cache_clib.py'))
                    self.compiler_opt = new_ccompiler_opt(compiler=(self.compiler),
                      dispatch_hpath=dispatch_hpath,
                      cpu_baseline=(self.cpu_baseline),
                      cpu_dispatch=(self.cpu_dispatch),
                      cache_path=opt_cache_path)
                    if not self.compiler_opt.is_cached():
                        log.info('Detected changes on compiler optimizations, force rebuilding')
                        self.force = True
                    import atexit

                    def report():
                        log.info('\n########### CLIB COMPILER OPTIMIZATION ###########')
                        log.info(self.compiler_opt.report(full=True))

                    atexit.register(report)
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

 L. 185         0  LOAD_FAST                'self'
                2  LOAD_ATTR                compiler
                4  STORE_FAST               'compiler'

 L. 186         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _f_compiler
               10  STORE_FAST               'fcompiler'

 L. 188        12  LOAD_FAST                'build_info'
               14  LOAD_METHOD              get
               16  LOAD_STR                 'sources'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'sources'

 L. 189        22  LOAD_FAST                'sources'
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_TRUE     38  'to 38'
               30  LOAD_GLOBAL              is_sequence
               32  LOAD_FAST                'sources'
               34  CALL_FUNCTION_1       1  ''
               36  POP_JUMP_IF_TRUE     50  'to 50'
             38_0  COME_FROM            28  '28'

 L. 190        38  LOAD_GLOBAL              DistutilsSetupError
               40  LOAD_STR                 "in 'libraries' option (library '%s'), 'sources' must be present and must be a list of source filenames"

 L. 192        42  LOAD_FAST                'lib_name'

 L. 190        44  BINARY_MODULO    
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            36  '36'

 L. 193        50  LOAD_GLOBAL              list
               52  LOAD_FAST                'sources'
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'sources'

 L. 196        58  LOAD_GLOBAL              filter_sources
               60  LOAD_FAST                'sources'
               62  CALL_FUNCTION_1       1  ''

 L. 195        64  UNPACK_SEQUENCE_4     4 
               66  STORE_DEREF              'c_sources'
               68  STORE_FAST               'cxx_sources'
               70  STORE_FAST               'f_sources'
               72  STORE_FAST               'fmodule_sources'

 L. 197        74  LOAD_FAST                'fmodule_sources'
               76  UNARY_NOT        
               78  UNARY_NOT        
               80  JUMP_IF_TRUE_OR_POP    96  'to 96'

 L. 198        82  LOAD_FAST                'build_info'
               84  LOAD_METHOD              get
               86  LOAD_STR                 'language'
               88  LOAD_STR                 'c'
               90  CALL_METHOD_2         2  ''
               92  LOAD_STR                 'f90'
               94  COMPARE_OP               ==
             96_0  COME_FROM            80  '80'

 L. 197        96  STORE_FAST               'requiref90'

 L. 201        98  BUILD_LIST_0          0 
              100  STORE_FAST               'source_languages'

 L. 202       102  LOAD_DEREF               'c_sources'
              104  POP_JUMP_IF_FALSE   116  'to 116'

 L. 203       106  LOAD_FAST                'source_languages'
              108  LOAD_METHOD              append
              110  LOAD_STR                 'c'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
            116_0  COME_FROM           104  '104'

 L. 204       116  LOAD_FAST                'cxx_sources'
              118  POP_JUMP_IF_FALSE   130  'to 130'

 L. 205       120  LOAD_FAST                'source_languages'
              122  LOAD_METHOD              append
              124  LOAD_STR                 'c++'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
            130_0  COME_FROM           118  '118'

 L. 206       130  LOAD_FAST                'requiref90'
              132  POP_JUMP_IF_FALSE   146  'to 146'

 L. 207       134  LOAD_FAST                'source_languages'
              136  LOAD_METHOD              append
              138  LOAD_STR                 'f90'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_FORWARD        160  'to 160'
            146_0  COME_FROM           132  '132'

 L. 208       146  LOAD_FAST                'f_sources'
              148  POP_JUMP_IF_FALSE   160  'to 160'

 L. 209       150  LOAD_FAST                'source_languages'
              152  LOAD_METHOD              append
              154  LOAD_STR                 'f77'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
            160_0  COME_FROM           148  '148'
            160_1  COME_FROM           144  '144'

 L. 210       160  LOAD_FAST                'source_languages'
              162  LOAD_FAST                'build_info'
              164  LOAD_STR                 'source_languages'
              166  STORE_SUBSCR     

 L. 212       168  LOAD_FAST                'compiler'
              170  LOAD_ATTR                library_filename
              172  LOAD_FAST                'lib_name'

 L. 213       174  LOAD_FAST                'self'
              176  LOAD_ATTR                build_clib

 L. 212       178  LOAD_CONST               ('output_dir',)
              180  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              182  STORE_FAST               'lib_file'

 L. 214       184  LOAD_FAST                'sources'
              186  LOAD_FAST                'build_info'
              188  LOAD_METHOD              get
              190  LOAD_STR                 'depends'
              192  BUILD_LIST_0          0 
              194  CALL_METHOD_2         2  ''
              196  BINARY_ADD       
              198  STORE_FAST               'depends'

 L. 215       200  LOAD_FAST                'self'
              202  LOAD_ATTR                force
              204  POP_JUMP_IF_TRUE    234  'to 234'
              206  LOAD_GLOBAL              newer_group
              208  LOAD_FAST                'depends'
              210  LOAD_FAST                'lib_file'
              212  LOAD_STR                 'newer'
              214  CALL_FUNCTION_3       3  ''
              216  POP_JUMP_IF_TRUE    234  'to 234'

 L. 216       218  LOAD_GLOBAL              log
              220  LOAD_METHOD              debug
              222  LOAD_STR                 "skipping '%s' library (up-to-date)"
              224  LOAD_FAST                'lib_name'
              226  CALL_METHOD_2         2  ''
              228  POP_TOP          

 L. 217       230  LOAD_CONST               None
              232  RETURN_VALUE     
            234_0  COME_FROM           216  '216'
            234_1  COME_FROM           204  '204'

 L. 219       234  LOAD_GLOBAL              log
              236  LOAD_METHOD              info
              238  LOAD_STR                 "building '%s' library"
              240  LOAD_FAST                'lib_name'
              242  CALL_METHOD_2         2  ''
              244  POP_TOP          

 L. 221       246  LOAD_FAST                'build_info'
              248  LOAD_METHOD              get
              250  LOAD_STR                 'config_fc'
              252  BUILD_MAP_0           0 
              254  CALL_METHOD_2         2  ''
              256  STORE_FAST               'config_fc'

 L. 222       258  LOAD_FAST                'fcompiler'
              260  LOAD_CONST               None
              262  COMPARE_OP               is-not
          264_266  POP_JUMP_IF_FALSE   382  'to 382'
              268  LOAD_FAST                'config_fc'
          270_272  POP_JUMP_IF_FALSE   382  'to 382'

 L. 223       274  LOAD_GLOBAL              log
              276  LOAD_METHOD              info
              278  LOAD_STR                 'using additional config_fc from setup script for fortran compiler: %s'

 L. 225       280  LOAD_FAST                'config_fc'
              282  BUILD_TUPLE_1         1 

 L. 223       284  BINARY_MODULO    
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

 L. 226       290  LOAD_CONST               0
              292  LOAD_CONST               ('new_fcompiler',)
              294  IMPORT_NAME_ATTR         numpy.distutils.fcompiler
              296  IMPORT_FROM              new_fcompiler
              298  STORE_FAST               'new_fcompiler'
              300  POP_TOP          

 L. 227       302  LOAD_FAST                'new_fcompiler'
              304  LOAD_FAST                'fcompiler'
              306  LOAD_ATTR                compiler_type

 L. 228       308  LOAD_FAST                'self'
              310  LOAD_ATTR                verbose

 L. 229       312  LOAD_FAST                'self'
              314  LOAD_ATTR                dry_run

 L. 230       316  LOAD_FAST                'self'
              318  LOAD_ATTR                force

 L. 231       320  LOAD_FAST                'requiref90'

 L. 232       322  LOAD_FAST                'self'
              324  LOAD_ATTR                compiler

 L. 227       326  LOAD_CONST               ('compiler', 'verbose', 'dry_run', 'force', 'requiref90', 'c_compiler')
              328  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              330  STORE_FAST               'fcompiler'

 L. 233       332  LOAD_FAST                'fcompiler'
              334  LOAD_CONST               None
              336  COMPARE_OP               is-not
          338_340  POP_JUMP_IF_FALSE   382  'to 382'

 L. 234       342  LOAD_FAST                'self'
              344  LOAD_ATTR                distribution
              346  STORE_FAST               'dist'

 L. 235       348  LOAD_FAST                'dist'
              350  LOAD_METHOD              get_option_dict
              352  LOAD_STR                 'config_fc'
              354  CALL_METHOD_1         1  ''
              356  LOAD_METHOD              copy
              358  CALL_METHOD_0         0  ''
              360  STORE_FAST               'base_config_fc'

 L. 236       362  LOAD_FAST                'base_config_fc'
              364  LOAD_METHOD              update
              366  LOAD_FAST                'config_fc'
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          

 L. 237       372  LOAD_FAST                'fcompiler'
              374  LOAD_METHOD              customize
              376  LOAD_FAST                'base_config_fc'
              378  CALL_METHOD_1         1  ''
              380  POP_TOP          
            382_0  COME_FROM           338  '338'
            382_1  COME_FROM           270  '270'
            382_2  COME_FROM           264  '264'

 L. 240       382  LOAD_FAST                'f_sources'
          384_386  POP_JUMP_IF_TRUE    394  'to 394'
              388  LOAD_FAST                'fmodule_sources'
          390_392  POP_JUMP_IF_FALSE   416  'to 416'
            394_0  COME_FROM           384  '384'
              394  LOAD_FAST                'fcompiler'
              396  LOAD_CONST               None
              398  COMPARE_OP               is
          400_402  POP_JUMP_IF_FALSE   416  'to 416'

 L. 241       404  LOAD_GLOBAL              DistutilsError
              406  LOAD_STR                 'library %s has Fortran sources but no Fortran compiler found'

 L. 242       408  LOAD_FAST                'lib_name'

 L. 241       410  BINARY_MODULO    
              412  CALL_FUNCTION_1       1  ''
              414  RAISE_VARARGS_1       1  'exception instance'
            416_0  COME_FROM           400  '400'
            416_1  COME_FROM           390  '390'

 L. 244       416  LOAD_FAST                'fcompiler'
              418  LOAD_CONST               None
              420  COMPARE_OP               is-not
          422_424  POP_JUMP_IF_FALSE   462  'to 462'

 L. 245       426  LOAD_FAST                'build_info'
              428  LOAD_METHOD              get

 L. 246       430  LOAD_STR                 'extra_f77_compile_args'

 L. 245       432  CALL_METHOD_1         1  ''
          434_436  JUMP_IF_TRUE_OR_POP   440  'to 440'

 L. 246       438  BUILD_LIST_0          0 
            440_0  COME_FROM           434  '434'

 L. 245       440  LOAD_FAST                'fcompiler'
              442  STORE_ATTR               extra_f77_compile_args

 L. 247       444  LOAD_FAST                'build_info'
              446  LOAD_METHOD              get

 L. 248       448  LOAD_STR                 'extra_f90_compile_args'

 L. 247       450  CALL_METHOD_1         1  ''
          452_454  JUMP_IF_TRUE_OR_POP   458  'to 458'

 L. 248       456  BUILD_LIST_0          0 
            458_0  COME_FROM           452  '452'

 L. 247       458  LOAD_FAST                'fcompiler'
              460  STORE_ATTR               extra_f90_compile_args
            462_0  COME_FROM           422  '422'

 L. 250       462  LOAD_FAST                'build_info'
              464  LOAD_METHOD              get
              466  LOAD_STR                 'macros'
              468  CALL_METHOD_1         1  ''
              470  STORE_FAST               'macros'

 L. 251       472  LOAD_FAST                'macros'
              474  LOAD_CONST               None
              476  COMPARE_OP               is
          478_480  POP_JUMP_IF_FALSE   486  'to 486'

 L. 252       482  BUILD_LIST_0          0 
              484  STORE_FAST               'macros'
            486_0  COME_FROM           478  '478'

 L. 253       486  LOAD_FAST                'build_info'
              488  LOAD_METHOD              get
              490  LOAD_STR                 'include_dirs'
              492  CALL_METHOD_1         1  ''
              494  STORE_FAST               'include_dirs'

 L. 254       496  LOAD_FAST                'include_dirs'
              498  LOAD_CONST               None
              500  COMPARE_OP               is
          502_504  POP_JUMP_IF_FALSE   510  'to 510'

 L. 255       506  BUILD_LIST_0          0 
              508  STORE_FAST               'include_dirs'
            510_0  COME_FROM           502  '502'

 L. 256       510  LOAD_FAST                'build_info'
              512  LOAD_METHOD              get
              514  LOAD_STR                 'extra_compiler_args'
              516  CALL_METHOD_1         1  ''
          518_520  JUMP_IF_TRUE_OR_POP   524  'to 524'
              522  BUILD_LIST_0          0 
            524_0  COME_FROM           518  '518'
              524  STORE_FAST               'extra_postargs'

 L. 258       526  LOAD_FAST                'include_dirs'
              528  LOAD_METHOD              extend
              530  LOAD_GLOBAL              get_numpy_include_dirs
              532  CALL_FUNCTION_0       0  ''
              534  CALL_METHOD_1         1  ''
              536  POP_TOP          

 L. 260       538  LOAD_FAST                'build_info'
              540  LOAD_METHOD              get
              542  LOAD_STR                 'module_dirs'
              544  CALL_METHOD_1         1  ''
          546_548  JUMP_IF_TRUE_OR_POP   552  'to 552'
              550  BUILD_LIST_0          0 
            552_0  COME_FROM           546  '546'
              552  STORE_FAST               'module_dirs'

 L. 261       554  LOAD_GLOBAL              os
              556  LOAD_ATTR                path
              558  LOAD_METHOD              dirname
              560  LOAD_FAST                'lib_file'
              562  CALL_METHOD_1         1  ''
              564  STORE_FAST               'module_build_dir'

 L. 262       566  LOAD_FAST                'requiref90'
          568_570  POP_JUMP_IF_FALSE   582  'to 582'

 L. 263       572  LOAD_FAST                'self'
              574  LOAD_METHOD              mkpath
              576  LOAD_FAST                'module_build_dir'
              578  CALL_METHOD_1         1  ''
              580  POP_TOP          
            582_0  COME_FROM           568  '568'

 L. 265       582  LOAD_FAST                'compiler'
              584  LOAD_ATTR                compiler_type
              586  LOAD_STR                 'msvc'
              588  COMPARE_OP               ==
          590_592  POP_JUMP_IF_FALSE   606  'to 606'

 L. 268       594  LOAD_DEREF               'c_sources'
              596  LOAD_FAST                'cxx_sources'
              598  INPLACE_ADD      
              600  STORE_DEREF              'c_sources'

 L. 269       602  BUILD_LIST_0          0 
              604  STORE_FAST               'cxx_sources'
            606_0  COME_FROM           590  '590'

 L. 273       606  BUILD_LIST_0          0 
              608  STORE_FAST               'copt_c_sources'

 L. 274       610  BUILD_LIST_0          0 
              612  STORE_FAST               'copt_baseline_flags'

 L. 275       614  BUILD_LIST_0          0 
              616  STORE_FAST               'copt_macros'

 L. 276       618  LOAD_FAST                'self'
              620  LOAD_ATTR                disable_optimization
          622_624  POP_JUMP_IF_TRUE    732  'to 732'

 L. 277       626  LOAD_FAST                'self'
              628  LOAD_METHOD              get_finalized_command
              630  LOAD_STR                 'build_src'
              632  CALL_METHOD_1         1  ''
              634  LOAD_ATTR                build_src
              636  STORE_FAST               'bsrc_dir'

 L. 278       638  LOAD_GLOBAL              os
              640  LOAD_ATTR                path
              642  LOAD_METHOD              join
              644  LOAD_STR                 'numpy'
              646  LOAD_STR                 'distutils'
              648  LOAD_STR                 'include'
              650  CALL_METHOD_3         3  ''
              652  STORE_FAST               'dispatch_hpath'

 L. 279       654  LOAD_GLOBAL              os
              656  LOAD_ATTR                path
              658  LOAD_METHOD              join
              660  LOAD_FAST                'bsrc_dir'
              662  LOAD_FAST                'dispatch_hpath'
              664  CALL_METHOD_2         2  ''
              666  STORE_FAST               'dispatch_hpath'

 L. 280       668  LOAD_FAST                'include_dirs'
              670  LOAD_METHOD              append
              672  LOAD_FAST                'dispatch_hpath'
              674  CALL_METHOD_1         1  ''
              676  POP_TOP          

 L. 282       678  LOAD_FAST                'self'
              680  LOAD_ATTR                inplace
          682_684  POP_JUMP_IF_FALSE   690  'to 690'
              686  LOAD_CONST               None
              688  JUMP_FORWARD        692  'to 692'
            690_0  COME_FROM           682  '682'
              690  LOAD_FAST                'bsrc_dir'
            692_0  COME_FROM           688  '688'
              692  STORE_FAST               'copt_build_src'

 L. 283       694  LOAD_CLOSURE             'c_sources'
              696  BUILD_TUPLE_1         1 
              698  LOAD_LISTCOMP            '<code_object <listcomp>>'
              700  LOAD_STR                 'build_clib.build_a_library.<locals>.<listcomp>'
              702  MAKE_FUNCTION_8          'closure'

 L. 285       704  LOAD_DEREF               'c_sources'
              706  LOAD_CONST               None
              708  LOAD_CONST               None
              710  BUILD_SLICE_2         2 
              712  BINARY_SUBSCR    

 L. 283       714  GET_ITER         
              716  CALL_FUNCTION_1       1  ''
              718  STORE_FAST               'copt_c_sources'

 L. 287       720  LOAD_FAST                'self'
              722  LOAD_ATTR                compiler_opt
              724  LOAD_METHOD              cpu_baseline_flags
              726  CALL_METHOD_0         0  ''
              728  STORE_FAST               'copt_baseline_flags'
              730  JUMP_FORWARD        742  'to 742'
            732_0  COME_FROM           622  '622'

 L. 289       732  LOAD_FAST                'copt_macros'
              734  LOAD_METHOD              append
              736  LOAD_CONST               ('NPY_DISABLE_OPTIMIZATION', 1)
              738  CALL_METHOD_1         1  ''
              740  POP_TOP          
            742_0  COME_FROM           730  '730'

 L. 291       742  BUILD_LIST_0          0 
              744  STORE_FAST               'objects'

 L. 292       746  LOAD_FAST                'copt_c_sources'
          748_750  POP_JUMP_IF_FALSE   800  'to 800'

 L. 293       752  LOAD_GLOBAL              log
              754  LOAD_METHOD              info
              756  LOAD_STR                 'compiling C dispatch-able sources'
              758  CALL_METHOD_1         1  ''
              760  POP_TOP          

 L. 294       762  LOAD_FAST                'objects'
              764  LOAD_FAST                'self'
              766  LOAD_ATTR                compiler_opt
              768  LOAD_ATTR                try_dispatch
              770  LOAD_FAST                'copt_c_sources'

 L. 295       772  LOAD_FAST                'self'
              774  LOAD_ATTR                build_temp

 L. 296       776  LOAD_FAST                'copt_build_src'

 L. 297       778  LOAD_FAST                'macros'
              780  LOAD_FAST                'copt_macros'
              782  BINARY_ADD       

 L. 298       784  LOAD_FAST                'include_dirs'

 L. 299       786  LOAD_FAST                'self'
              788  LOAD_ATTR                debug

 L. 300       790  LOAD_FAST                'extra_postargs'

 L. 294       792  LOAD_CONST               ('output_dir', 'src_dir', 'macros', 'include_dirs', 'debug', 'extra_postargs')
              794  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              796  INPLACE_ADD      
              798  STORE_FAST               'objects'
            800_0  COME_FROM           748  '748'

 L. 302       800  LOAD_DEREF               'c_sources'
          802_804  POP_JUMP_IF_FALSE   854  'to 854'

 L. 303       806  LOAD_GLOBAL              log
              808  LOAD_METHOD              info
              810  LOAD_STR                 'compiling C sources'
              812  CALL_METHOD_1         1  ''
              814  POP_TOP          

 L. 304       816  LOAD_FAST                'objects'
              818  LOAD_FAST                'compiler'
              820  LOAD_ATTR                compile
              822  LOAD_DEREF               'c_sources'

 L. 305       824  LOAD_FAST                'self'
              826  LOAD_ATTR                build_temp

 L. 306       828  LOAD_FAST                'macros'
              830  LOAD_FAST                'copt_macros'
              832  BINARY_ADD       

 L. 307       834  LOAD_FAST                'include_dirs'

 L. 308       836  LOAD_FAST                'self'
              838  LOAD_ATTR                debug

 L. 309       840  LOAD_FAST                'extra_postargs'
              842  LOAD_FAST                'copt_baseline_flags'
              844  BINARY_ADD       

 L. 304       846  LOAD_CONST               ('output_dir', 'macros', 'include_dirs', 'debug', 'extra_postargs')
              848  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              850  INPLACE_ADD      
              852  STORE_FAST               'objects'
            854_0  COME_FROM           802  '802'

 L. 311       854  LOAD_FAST                'cxx_sources'
          856_858  POP_JUMP_IF_FALSE   922  'to 922'

 L. 312       860  LOAD_GLOBAL              log
              862  LOAD_METHOD              info
              864  LOAD_STR                 'compiling C++ sources'
              866  CALL_METHOD_1         1  ''
              868  POP_TOP          

 L. 313       870  LOAD_FAST                'compiler'
              872  LOAD_METHOD              cxx_compiler
              874  CALL_METHOD_0         0  ''
              876  STORE_FAST               'cxx_compiler'

 L. 314       878  LOAD_FAST                'cxx_compiler'
              880  LOAD_ATTR                compile
              882  LOAD_FAST                'cxx_sources'

 L. 315       884  LOAD_FAST                'self'
              886  LOAD_ATTR                build_temp

 L. 316       888  LOAD_FAST                'macros'
              890  LOAD_FAST                'copt_macros'
              892  BINARY_ADD       

 L. 317       894  LOAD_FAST                'include_dirs'

 L. 318       896  LOAD_FAST                'self'
              898  LOAD_ATTR                debug

 L. 319       900  LOAD_FAST                'extra_postargs'
              902  LOAD_FAST                'copt_baseline_flags'
              904  BINARY_ADD       

 L. 314       906  LOAD_CONST               ('output_dir', 'macros', 'include_dirs', 'debug', 'extra_postargs')
              908  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              910  STORE_FAST               'cxx_objects'

 L. 320       912  LOAD_FAST                'objects'
              914  LOAD_METHOD              extend
              916  LOAD_FAST                'cxx_objects'
              918  CALL_METHOD_1         1  ''
              920  POP_TOP          
            922_0  COME_FROM           856  '856'

 L. 322       922  LOAD_FAST                'f_sources'
          924_926  POP_JUMP_IF_TRUE    934  'to 934'
              928  LOAD_FAST                'fmodule_sources'
          930_932  POP_JUMP_IF_FALSE  1254  'to 1254'
            934_0  COME_FROM           924  '924'

 L. 323       934  BUILD_LIST_0          0 
              936  STORE_FAST               'extra_postargs'

 L. 324       938  BUILD_LIST_0          0 
              940  STORE_FAST               'f_objects'

 L. 326       942  LOAD_FAST                'requiref90'
          944_946  POP_JUMP_IF_FALSE   984  'to 984'

 L. 327       948  LOAD_FAST                'fcompiler'
              950  LOAD_ATTR                module_dir_switch
              952  LOAD_CONST               None
              954  COMPARE_OP               is
          956_958  POP_JUMP_IF_FALSE   968  'to 968'

 L. 328       960  LOAD_GLOBAL              glob
              962  LOAD_STR                 '*.mod'
              964  CALL_FUNCTION_1       1  ''
              966  STORE_FAST               'existing_modules'
            968_0  COME_FROM           956  '956'

 L. 329       968  LOAD_FAST                'extra_postargs'
              970  LOAD_FAST                'fcompiler'
              972  LOAD_METHOD              module_options

 L. 330       974  LOAD_FAST                'module_dirs'

 L. 330       976  LOAD_FAST                'module_build_dir'

 L. 329       978  CALL_METHOD_2         2  ''
              980  INPLACE_ADD      
              982  STORE_FAST               'extra_postargs'
            984_0  COME_FROM           944  '944'

 L. 332       984  LOAD_FAST                'fmodule_sources'
          986_988  POP_JUMP_IF_FALSE  1030  'to 1030'

 L. 333       990  LOAD_GLOBAL              log
              992  LOAD_METHOD              info
              994  LOAD_STR                 'compiling Fortran 90 module sources'
              996  CALL_METHOD_1         1  ''
              998  POP_TOP          

 L. 334      1000  LOAD_FAST                'f_objects'
             1002  LOAD_FAST                'fcompiler'
             1004  LOAD_ATTR                compile
             1006  LOAD_FAST                'fmodule_sources'

 L. 335      1008  LOAD_FAST                'self'
             1010  LOAD_ATTR                build_temp

 L. 336      1012  LOAD_FAST                'macros'

 L. 337      1014  LOAD_FAST                'include_dirs'

 L. 338      1016  LOAD_FAST                'self'
             1018  LOAD_ATTR                debug

 L. 339      1020  LOAD_FAST                'extra_postargs'

 L. 334      1022  LOAD_CONST               ('output_dir', 'macros', 'include_dirs', 'debug', 'extra_postargs')
             1024  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1026  INPLACE_ADD      
             1028  STORE_FAST               'f_objects'
           1030_0  COME_FROM           986  '986'

 L. 341      1030  LOAD_FAST                'requiref90'
         1032_1034  POP_JUMP_IF_FALSE  1206  'to 1206'
             1036  LOAD_FAST                'self'
             1038  LOAD_ATTR                _f_compiler
             1040  LOAD_ATTR                module_dir_switch
             1042  LOAD_CONST               None
             1044  COMPARE_OP               is
         1046_1048  POP_JUMP_IF_FALSE  1206  'to 1206'

 L. 343      1050  LOAD_GLOBAL              glob
             1052  LOAD_STR                 '*.mod'
             1054  CALL_FUNCTION_1       1  ''
             1056  GET_ITER         
           1058_0  COME_FROM          1202  '1202'
           1058_1  COME_FROM          1198  '1198'
           1058_2  COME_FROM          1160  '1160'
           1058_3  COME_FROM          1116  '1116'
           1058_4  COME_FROM          1072  '1072'
             1058  FOR_ITER           1206  'to 1206'
             1060  STORE_FAST               'f'

 L. 344      1062  LOAD_FAST                'f'
             1064  LOAD_FAST                'existing_modules'
             1066  COMPARE_OP               in
         1068_1070  POP_JUMP_IF_FALSE  1076  'to 1076'

 L. 345  1072_1074  JUMP_BACK          1058  'to 1058'
           1076_0  COME_FROM          1068  '1068'

 L. 346      1076  LOAD_GLOBAL              os
             1078  LOAD_ATTR                path
             1080  LOAD_METHOD              join
             1082  LOAD_FAST                'module_build_dir'
             1084  LOAD_FAST                'f'
             1086  CALL_METHOD_2         2  ''
             1088  STORE_FAST               't'

 L. 347      1090  LOAD_GLOBAL              os
             1092  LOAD_ATTR                path
             1094  LOAD_METHOD              abspath
             1096  LOAD_FAST                'f'
             1098  CALL_METHOD_1         1  ''
             1100  LOAD_GLOBAL              os
             1102  LOAD_ATTR                path
             1104  LOAD_METHOD              abspath
             1106  LOAD_FAST                't'
             1108  CALL_METHOD_1         1  ''
             1110  COMPARE_OP               ==
         1112_1114  POP_JUMP_IF_FALSE  1120  'to 1120'

 L. 348  1116_1118  JUMP_BACK          1058  'to 1058'
           1120_0  COME_FROM          1112  '1112'

 L. 349      1120  LOAD_GLOBAL              os
             1122  LOAD_ATTR                path
             1124  LOAD_METHOD              isfile
             1126  LOAD_FAST                't'
             1128  CALL_METHOD_1         1  ''
         1130_1132  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 350      1134  LOAD_GLOBAL              os
             1136  LOAD_METHOD              remove
             1138  LOAD_FAST                't'
             1140  CALL_METHOD_1         1  ''
             1142  POP_TOP          
           1144_0  COME_FROM          1130  '1130'

 L. 351      1144  SETUP_FINALLY      1162  'to 1162'

 L. 352      1146  LOAD_FAST                'self'
             1148  LOAD_METHOD              move_file
             1150  LOAD_FAST                'f'
             1152  LOAD_FAST                'module_build_dir'
             1154  CALL_METHOD_2         2  ''
             1156  POP_TOP          
             1158  POP_BLOCK        
             1160  JUMP_BACK          1058  'to 1058'
           1162_0  COME_FROM_FINALLY  1144  '1144'

 L. 353      1162  DUP_TOP          
             1164  LOAD_GLOBAL              DistutilsFileError
             1166  COMPARE_OP               exception-match
         1168_1170  POP_JUMP_IF_FALSE  1200  'to 1200'
             1172  POP_TOP          
             1174  POP_TOP          
             1176  POP_TOP          

 L. 354      1178  LOAD_GLOBAL              log
             1180  LOAD_METHOD              warn
             1182  LOAD_STR                 'failed to move %r to %r'

 L. 355      1184  LOAD_FAST                'f'
             1186  LOAD_FAST                'module_build_dir'
             1188  BUILD_TUPLE_2         2 

 L. 354      1190  BINARY_MODULO    
             1192  CALL_METHOD_1         1  ''
             1194  POP_TOP          
             1196  POP_EXCEPT       
             1198  JUMP_BACK          1058  'to 1058'
           1200_0  COME_FROM          1168  '1168'
             1200  END_FINALLY      
         1202_1204  JUMP_BACK          1058  'to 1058'
           1206_0  COME_FROM          1058  '1058'
           1206_1  COME_FROM          1046  '1046'
           1206_2  COME_FROM          1032  '1032'

 L. 357      1206  LOAD_FAST                'f_sources'
         1208_1210  POP_JUMP_IF_FALSE  1258  'to 1258'

 L. 358      1212  LOAD_GLOBAL              log
             1214  LOAD_METHOD              info
             1216  LOAD_STR                 'compiling Fortran sources'
             1218  CALL_METHOD_1         1  ''
             1220  POP_TOP          

 L. 359      1222  LOAD_FAST                'f_objects'
             1224  LOAD_FAST                'fcompiler'
             1226  LOAD_ATTR                compile
             1228  LOAD_FAST                'f_sources'

 L. 360      1230  LOAD_FAST                'self'
             1232  LOAD_ATTR                build_temp

 L. 361      1234  LOAD_FAST                'macros'

 L. 362      1236  LOAD_FAST                'include_dirs'

 L. 363      1238  LOAD_FAST                'self'
             1240  LOAD_ATTR                debug

 L. 364      1242  LOAD_FAST                'extra_postargs'

 L. 359      1244  LOAD_CONST               ('output_dir', 'macros', 'include_dirs', 'debug', 'extra_postargs')
             1246  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1248  INPLACE_ADD      
             1250  STORE_FAST               'f_objects'
             1252  JUMP_FORWARD       1258  'to 1258'
           1254_0  COME_FROM           930  '930'

 L. 366      1254  BUILD_LIST_0          0 
             1256  STORE_FAST               'f_objects'
           1258_0  COME_FROM          1252  '1252'
           1258_1  COME_FROM          1208  '1208'

 L. 368      1258  LOAD_FAST                'f_objects'
         1260_1262  POP_JUMP_IF_FALSE  1458  'to 1458'
             1264  LOAD_FAST                'fcompiler'
             1266  LOAD_METHOD              can_ccompiler_link
             1268  LOAD_FAST                'compiler'
             1270  CALL_METHOD_1         1  ''
         1272_1274  POP_JUMP_IF_TRUE   1458  'to 1458'

 L. 372      1276  LOAD_GLOBAL              os
             1278  LOAD_ATTR                path
             1280  LOAD_METHOD              join
             1282  LOAD_FAST                'self'
             1284  LOAD_ATTR                build_clib

 L. 373      1286  LOAD_FAST                'lib_name'
             1288  LOAD_STR                 '.fobjects'
             1290  BINARY_ADD       

 L. 372      1292  CALL_METHOD_2         2  ''
             1294  STORE_FAST               'listfn'

 L. 374      1296  LOAD_GLOBAL              open
             1298  LOAD_FAST                'listfn'
             1300  LOAD_STR                 'w'
             1302  CALL_FUNCTION_2       2  ''
             1304  SETUP_WITH         1338  'to 1338'
             1306  STORE_FAST               'f'

 L. 375      1308  LOAD_FAST                'f'
             1310  LOAD_METHOD              write
             1312  LOAD_STR                 '\n'
             1314  LOAD_METHOD              join
             1316  LOAD_GENEXPR             '<code_object <genexpr>>'
             1318  LOAD_STR                 'build_clib.build_a_library.<locals>.<genexpr>'
             1320  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1322  LOAD_FAST                'f_objects'
             1324  GET_ITER         
             1326  CALL_FUNCTION_1       1  ''
             1328  CALL_METHOD_1         1  ''
             1330  CALL_METHOD_1         1  ''
             1332  POP_TOP          
             1334  POP_BLOCK        
             1336  BEGIN_FINALLY    
           1338_0  COME_FROM_WITH     1304  '1304'
             1338  WITH_CLEANUP_START
             1340  WITH_CLEANUP_FINISH
             1342  END_FINALLY      

 L. 377      1344  LOAD_GLOBAL              os
             1346  LOAD_ATTR                path
             1348  LOAD_METHOD              join
             1350  LOAD_FAST                'self'
             1352  LOAD_ATTR                build_clib

 L. 378      1354  LOAD_FAST                'lib_name'
             1356  LOAD_STR                 '.cobjects'
             1358  BINARY_ADD       

 L. 377      1360  CALL_METHOD_2         2  ''
             1362  STORE_FAST               'listfn'

 L. 379      1364  LOAD_GLOBAL              open
             1366  LOAD_FAST                'listfn'
             1368  LOAD_STR                 'w'
             1370  CALL_FUNCTION_2       2  ''
             1372  SETUP_WITH         1406  'to 1406'
             1374  STORE_FAST               'f'

 L. 380      1376  LOAD_FAST                'f'
             1378  LOAD_METHOD              write
             1380  LOAD_STR                 '\n'
             1382  LOAD_METHOD              join
             1384  LOAD_GENEXPR             '<code_object <genexpr>>'
             1386  LOAD_STR                 'build_clib.build_a_library.<locals>.<genexpr>'
             1388  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1390  LOAD_FAST                'objects'
             1392  GET_ITER         
             1394  CALL_FUNCTION_1       1  ''
             1396  CALL_METHOD_1         1  ''
             1398  CALL_METHOD_1         1  ''
             1400  POP_TOP          
             1402  POP_BLOCK        
             1404  BEGIN_FINALLY    
           1406_0  COME_FROM_WITH     1372  '1372'
             1406  WITH_CLEANUP_START
             1408  WITH_CLEANUP_FINISH
             1410  END_FINALLY      

 L. 383      1412  LOAD_GLOBAL              os
             1414  LOAD_ATTR                path
             1416  LOAD_METHOD              join
             1418  LOAD_FAST                'self'
             1420  LOAD_ATTR                build_clib

 L. 384      1422  LOAD_FAST                'lib_name'
             1424  LOAD_FAST                'compiler'
             1426  LOAD_ATTR                static_lib_extension
             1428  BINARY_ADD       

 L. 383      1430  CALL_METHOD_2         2  ''
             1432  STORE_FAST               'lib_fname'

 L. 385      1434  LOAD_GLOBAL              open
             1436  LOAD_FAST                'lib_fname'
             1438  LOAD_STR                 'wb'
             1440  CALL_FUNCTION_2       2  ''
             1442  SETUP_WITH         1450  'to 1450'
             1444  STORE_FAST               'f'

 L. 386      1446  POP_BLOCK        
             1448  BEGIN_FINALLY    
           1450_0  COME_FROM_WITH     1442  '1442'
             1450  WITH_CLEANUP_START
             1452  WITH_CLEANUP_FINISH
             1454  END_FINALLY      
             1456  JUMP_FORWARD       1490  'to 1490'
           1458_0  COME_FROM          1272  '1272'
           1458_1  COME_FROM          1260  '1260'

 L. 390      1458  LOAD_FAST                'objects'
             1460  LOAD_METHOD              extend
             1462  LOAD_FAST                'f_objects'
             1464  CALL_METHOD_1         1  ''
             1466  POP_TOP          

 L. 391      1468  LOAD_FAST                'compiler'
             1470  LOAD_ATTR                create_static_lib
             1472  LOAD_FAST                'objects'
             1474  LOAD_FAST                'lib_name'

 L. 392      1476  LOAD_FAST                'self'
             1478  LOAD_ATTR                build_clib

 L. 393      1480  LOAD_FAST                'self'
             1482  LOAD_ATTR                debug

 L. 391      1484  LOAD_CONST               ('output_dir', 'debug')
             1486  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1488  POP_TOP          
           1490_0  COME_FROM          1456  '1456'

 L. 396      1490  LOAD_FAST                'build_info'
             1492  LOAD_METHOD              get
             1494  LOAD_STR                 'libraries'
             1496  BUILD_LIST_0          0 
             1498  CALL_METHOD_2         2  ''
             1500  STORE_FAST               'clib_libraries'

 L. 397      1502  LOAD_FAST                'libraries'
             1504  GET_ITER         
           1506_0  COME_FROM          1542  '1542'
           1506_1  COME_FROM          1520  '1520'
             1506  FOR_ITER           1546  'to 1546'
             1508  UNPACK_SEQUENCE_2     2 
             1510  STORE_FAST               'lname'
             1512  STORE_FAST               'binfo'

 L. 398      1514  LOAD_FAST                'lname'
             1516  LOAD_FAST                'clib_libraries'
             1518  COMPARE_OP               in
         1520_1522  POP_JUMP_IF_FALSE_BACK  1506  'to 1506'

 L. 399      1524  LOAD_FAST                'clib_libraries'
             1526  LOAD_METHOD              extend
             1528  LOAD_FAST                'binfo'
             1530  LOAD_METHOD              get
             1532  LOAD_STR                 'libraries'
             1534  BUILD_LIST_0          0 
             1536  CALL_METHOD_2         2  ''
             1538  CALL_METHOD_1         1  ''
             1540  POP_TOP          
         1542_1544  JUMP_BACK          1506  'to 1506'
           1546_0  COME_FROM          1506  '1506'

 L. 400      1546  LOAD_FAST                'clib_libraries'
         1548_1550  POP_JUMP_IF_FALSE  1560  'to 1560'

 L. 401      1552  LOAD_FAST                'clib_libraries'
             1554  LOAD_FAST                'build_info'
             1556  LOAD_STR                 'libraries'
             1558  STORE_SUBSCR     
           1560_0  COME_FROM          1548  '1548'

Parse error at or near `BEGIN_FINALLY' instruction at offset 1448