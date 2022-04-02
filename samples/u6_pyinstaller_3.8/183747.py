# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
            if self.compiler.compiler_type in ('msvc', 'intelw', 'intelemw') and not self.compiler.initialized:
                try:
                    self.compiler.initialize()
                except IOError:
                    e = get_exception()
                    msg = textwrap.dedent('                        Could not initialize compiler instance: do you have Visual Studio\n                        installed?  If you are trying to build with MinGW, please use "python setup.py\n                        build -c mingw32" instead.  If you have Visual Studio installed, check it is\n                        correctly installed, and the right version (VS 2008 for python 2.6, 2.7 and 3.2,\n                        VS 2010 for >= 3.3).\n\n                        Original exception was: %s, and the Compiler class was %s\n                        ============================================================================') % (
                     e, self.compiler.__class__.__name__)
                    print(textwrap.dedent('                        ============================================================================'))
                    raise distutils.errors.DistutilsPlatformError(msg)
                else:
                    from distutils import msvc9compiler
                    if msvc9compiler.get_build_version() >= 10:
                        for ldflags in (
                         self.compiler.ldflags_shared,
                         self.compiler.ldflags_shared_debug):
                            if '/MANIFEST' not in ldflags:
                                ldflags.append('/MANIFEST')

        self.fcompiler = isinstance(self.fcompiler, FCompiler) or new_fcompiler(compiler=(self.fcompiler), dry_run=(self.dry_run),
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
        return (src, obj)

    def _link(self, body, headers, include_dirs, libraries, library_dirs, lang):
        if self.compiler.compiler_type == 'msvc':
            libraries = (libraries or [])[:]
            library_dirs = (library_dirs or [])[:]
            if lang in ('f77', 'f90'):
                lang = 'c'
                if self.fcompiler:
                    for d in self.fcompiler.library_dirs or []:
                        if d.startswith('/usr/lib'):
                            try:
                                d = subprocess.check_output(['cygpath',
                                 '-w', d])
                            except (OSError, subprocess.CalledProcessError):
                                pass
                            else:
                                d = filepath_from_subprocess_output(d)
                        library_dirs.append(d)
                    else:
                        for libname in self.fcompiler.libraries or []:
                            if libname not in libraries:
                                libraries.append(libname)

            for libname in libraries:
                if libname.startswith('msvc'):
                    pass
                else:
                    fileexists = False
                    for libdir in library_dirs or []:
                        libfile = os.path.join(libdir, '%s.lib' % libname)
                        if os.path.isfile(libfile):
                            fileexists = True
                            break

                    if fileexists:
                        pass
                    else:
                        fileexists = False
                        for libdir in library_dirs:
                            libfile = os.path.join(libdir, 'lib%s.a' % libname)
                            if os.path.isfile(libfile):
                                libfile2 = os.path.join(libdir, '%s.lib' % libname)
                                copy_file(libfile, libfile2)
                                self.temp_files.append(libfile2)
                                fileexists = True
                                break
                            if fileexists:
                                pass
                            else:
                                log.warn('could not find library %r in directories %s' % (
                                 libname, library_dirs))

        else:
            if self.compiler.compiler_type == 'mingw32':
                generate_manifest(self)
            return self._wrap_method(old_config._link, lang, (
             body, headers, include_dirs,
             libraries, library_dirs, lang))

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
            140_0  COME_FROM            52  '52'

 L. 276       140  LOAD_GLOBAL              textwrap
              142  LOAD_METHOD              dedent
              144  LOAD_STR                 '\n            typedef %(type)s npy_check_sizeof_type;\n            int main (void)\n            {\n                static int test_array [1 - 2 * !(((long) (sizeof (npy_check_sizeof_type))) <= %(size)s)];\n                test_array [0] = 0\n\n                ;\n                return 0;\n            }\n            '
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'body'

 L. 291       150  LOAD_CONST               0
              152  STORE_FAST               'low'

 L. 292       154  LOAD_CONST               0
              156  STORE_FAST               'mid'

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

 L. 304       244  LOAD_FAST                'mid'
              246  STORE_FAST               'high'

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
        else:
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
                    if not (call_args and f in call_args and call_args[f]):
                        args = ''
                    else:
                        args = call_args[f]
                    body.append('  %s(%s);' % (f, args))
                else:
                    body.append('  %s;' % f)

        else:
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
                exe = os.path.join('.', exe)
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
            return (exitcode, output)


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