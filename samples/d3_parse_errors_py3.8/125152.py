# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\command\config.py
"""distutils.command.config

Implements the Distutils 'config' command, a (mostly) empty command class
that exists mainly to be sub-classed by specific module distributions and
applications.  The idea is that while every "config" command is different,
at least they're all named the same, and users always see "config" in the
list of standard commands.  Also, this is a good place to put common
configure-like tasks: "try to compile this C code", or "figure out where
this header file lives".
"""
import os, re
from distutils.core import Command
from distutils.errors import DistutilsExecError
from distutils.sysconfig import customize_compiler
from distutils import log
LANG_EXT = {'c':'.c', 
 'c++':'.cxx'}

class config(Command):
    description = 'prepare to build'
    user_options = [
     ('compiler=', None, 'specify the compiler type'),
     ('cc=', None, 'specify the compiler executable'),
     ('include-dirs=', 'I', 'list of directories to search for header files'),
     ('define=', 'D', 'C preprocessor macros to define'),
     ('undef=', 'U', 'C preprocessor macros to undefine'),
     ('libraries=', 'l', 'external C libraries to link with'),
     ('library-dirs=', 'L', 'directories to search for external C libraries'),
     ('noisy', None, 'show every action (compile, link, run, ...) taken'),
     ('dump-source', None, 'dump generated source files before attempting to compile them')]

    def initialize_options(self):
        self.compiler = None
        self.cc = None
        self.include_dirs = None
        self.libraries = None
        self.library_dirs = None
        self.noisy = 1
        self.dump_source = 1
        self.temp_files = []

    def finalize_options(self):
        if self.include_dirs is None:
            self.include_dirs = self.distribution.include_dirs or []
        elif isinstance(self.include_dirs, str):
            self.include_dirs = self.include_dirs.split(os.pathsep)
        if self.libraries is None:
            self.libraries = []
        elif isinstance(self.libraries, str):
            self.libraries = [
             self.libraries]
        if self.library_dirs is None:
            self.library_dirs = []
        elif isinstance(self.library_dirs, str):
            self.library_dirs = self.library_dirs.split(os.pathsep)

    def run(self):
        pass

    def _check_compiler(self):
        """Check that 'self.compiler' really is a CCompiler object;
        if not, make it one.
        """
        from distutils.ccompiler import CCompiler, new_compiler
        if not isinstance(self.compiler, CCompiler):
            self.compiler = new_compiler(compiler=(self.compiler), dry_run=(self.dry_run),
              force=1)
            customize_compiler(self.compiler)
            if self.include_dirs:
                self.compiler.set_include_dirs(self.include_dirs)
            if self.libraries:
                self.compiler.set_libraries(self.libraries)
            if self.library_dirs:
                self.compiler.set_library_dirs(self.library_dirs)

    def _gen_temp_sourcefile(self, body, headers, lang):
        filename = '_configtest' + LANG_EXT[lang]
        with open(filename, 'w') as file:
            if headers:
                for header in headers:
                    file.write('#include <%s>\n' % header)
                else:
                    file.write('\n')

            file.write(body)
            if body[(-1)] != '\n':
                file.write('\n')
        return filename

    def _preprocess(self, body, headers, include_dirs, lang):
        src = self._gen_temp_sourcefile(body, headers, lang)
        out = '_configtest.i'
        self.temp_files.extend([src, out])
        self.compiler.preprocess(src, out, include_dirs=include_dirs)
        return (
         src, out)

    def _compile(self, body, headers, include_dirs, lang):
        src = self._gen_temp_sourcefile(body, headers, lang)
        if self.dump_source:
            dump_file(src, "compiling '%s':" % src)
        obj, = self.compiler.object_filenames([src])
        self.temp_files.extend([src, obj])
        self.compiler.compile([src], include_dirs=include_dirs)
        return (
         src, obj)

    def _link(self, body, headers, include_dirs, libraries, library_dirs, lang):
        src, obj = self._compile(body, headers, include_dirs, lang)
        prog = os.path.splitext(os.path.basename(src))[0]
        self.compiler.link_executable([obj], prog, libraries=libraries,
          library_dirs=library_dirs,
          target_lang=lang)
        if self.compiler.exe_extension is not None:
            prog = prog + self.compiler.exe_extension
        self.temp_files.append(prog)
        return (
         src, obj, prog)

    def _clean(self, *filenames):
        if not filenames:
            filenames = self.temp_files
            self.temp_files = []
        log.info('removing: %s', ' '.join(filenames))
        for filename in filenames:
            try:
                os.remove(filename)
            except OSError:
                pass

    def try_cpp(self, body=None, headers=None, include_dirs=None, lang='c'):
        """Construct a source file from 'body' (a string containing lines
        of C/C++ code) and 'headers' (a list of header files to include)
        and run it through the preprocessor.  Return true if the
        preprocessor succeeded, false if there were any errors.
        ('body' probably isn't of much use, but what the heck.)
        """
        from distutils.ccompiler import CompileError
        self._check_compiler()
        ok = True
        try:
            self._preprocess(body, headers, include_dirs, lang)
        except CompileError:
            ok = False
        else:
            self._clean()
            return ok

    def search_cpp--- This code section failed: ---

 L. 199         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_compiler
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 200         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _preprocess
               12  LOAD_FAST                'body'
               14  LOAD_FAST                'headers'
               16  LOAD_FAST                'include_dirs'
               18  LOAD_FAST                'lang'
               20  CALL_METHOD_4         4  ''
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'src'
               26  STORE_FAST               'out'

 L. 202        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'pattern'
               32  LOAD_GLOBAL              str
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L. 203        38  LOAD_GLOBAL              re
               40  LOAD_METHOD              compile
               42  LOAD_FAST                'pattern'
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'pattern'
             48_0  COME_FROM            36  '36'

 L. 205        48  LOAD_GLOBAL              open
               50  LOAD_FAST                'out'
               52  CALL_FUNCTION_1       1  ''
               54  SETUP_WITH          102  'to 102'
               56  STORE_FAST               'file'

 L. 206        58  LOAD_CONST               False
               60  STORE_FAST               'match'
             62_0  COME_FROM            96  '96'
             62_1  COME_FROM            88  '88'

 L. 208        62  LOAD_FAST                'file'
               64  LOAD_METHOD              readline
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'line'

 L. 209        70  LOAD_FAST                'line'
               72  LOAD_STR                 ''
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    80  'to 80'

 L. 210        78  JUMP_FORWARD         98  'to 98'
             80_0  COME_FROM            76  '76'

 L. 211        80  LOAD_FAST                'pattern'
               82  LOAD_METHOD              search
               84  LOAD_FAST                'line'
               86  CALL_METHOD_1         1  ''
               88  POP_JUMP_IF_FALSE_BACK    62  'to 62'

 L. 212        90  LOAD_CONST               True
               92  STORE_FAST               'match'

 L. 213        94  JUMP_FORWARD         98  'to 98'
               96  JUMP_BACK            62  'to 62'
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            78  '78'
               98  POP_BLOCK        
              100  BEGIN_FINALLY    
            102_0  COME_FROM_WITH       54  '54'
              102  WITH_CLEANUP_START
              104  WITH_CLEANUP_FINISH
              106  END_FINALLY      

 L. 215       108  LOAD_FAST                'self'
              110  LOAD_METHOD              _clean
              112  CALL_METHOD_0         0  ''
              114  POP_TOP          

 L. 216       116  LOAD_FAST                'match'
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 96

    def try_compile(self, body, headers=None, include_dirs=None, lang='c'):
        """Try to compile a source file built from 'body' and 'headers'.
        Return true on success, false otherwise.
        """
        from distutils.ccompiler import CompileError
        self._check_compiler()
        try:
            self._compile(body, headers, include_dirs, lang)
            ok = True
        except CompileError:
            ok = False
        else:
            log.info(ok and 'success!' or 'failure.')
            self._clean()
            return ok

    def try_link(self, body, headers=None, include_dirs=None, libraries=None, library_dirs=None, lang='c'):
        """Try to compile and link a source file, built from 'body' and
        'headers', to executable form.  Return true on success, false
        otherwise.
        """
        from distutils.ccompiler import CompileError, LinkError
        self._check_compiler()
        try:
            self._link(body, headers, include_dirs, libraries, library_dirs, lang)
            ok = True
        except (CompileError, LinkError):
            ok = False
        else:
            log.info(ok and 'success!' or 'failure.')
            self._clean()
            return ok

    def try_run(self, body, headers=None, include_dirs=None, libraries=None, library_dirs=None, lang='c'):
        """Try to compile, link to an executable, and run a program
        built from 'body' and 'headers'.  Return true on success, false
        otherwise.
        """
        from distutils.ccompiler import CompileError, LinkError
        self._check_compiler()
        try:
            src, obj, exe = self._link(body, headers, include_dirs, libraries, library_dirs, lang)
            self.spawn([exe])
            ok = True
        except (CompileError, LinkError, DistutilsExecError):
            ok = False
        else:
            log.info(ok and 'success!' or 'failure.')
            self._clean()
            return ok

    def check_func(self, func, headers=None, include_dirs=None, libraries=None, library_dirs=None, decl=0, call=0):
        """Determine if function 'func' is available by constructing a
        source file that refers to 'func', and compiles and links it.
        If everything succeeds, returns true; otherwise returns false.

        The constructed source file starts out by including the header
        files listed in 'headers'.  If 'decl' is true, it then declares
        'func' (as "int func()"); you probably shouldn't supply 'headers'
        and set 'decl' true in the same call, or you might get errors about
        a conflicting declarations for 'func'.  Finally, the constructed
        'main()' function either references 'func' or (if 'call' is true)
        calls it.  'libraries' and 'library_dirs' are used when
        linking.
        """
        self._check_compiler()
        body = []
        if decl:
            body.append('int %s ();' % func)
        body.append('int main () {')
        if call:
            body.append('  %s();' % func)
        else:
            body.append('  %s;' % func)
        body.append('}')
        body = '\n'.join(body) + '\n'
        return self.try_link(body, headers, include_dirs, libraries, library_dirs)

    def check_lib(self, library, library_dirs=None, headers=None, include_dirs=None, other_libraries=[]):
        """Determine if 'library' is available to be linked against,
        without actually checking that any particular symbols are provided
        by it.  'headers' will be used in constructing the source file to
        be compiled, but the only effect of this is to check if all the
        header files listed are available.  Any libraries listed in
        'other_libraries' will be included in the link, in case 'library'
        has symbols that depend on other libraries.
        """
        self._check_compiler()
        return self.try_link('int main (void) { }', headers, include_dirs, [
         library] + other_libraries, library_dirs)

    def check_header(self, header, include_dirs=None, library_dirs=None, lang='c'):
        """Determine if the system header file named by 'header_file'
        exists and can be found by the preprocessor; return true if so,
        false otherwise.
        """
        return self.try_cpp(body='/* No body */', headers=[header], include_dirs=include_dirs)


def dump_file(filename, head=None):
    """Dumps a file content into log.info.

    If head is not None, will be dumped before the file content.
    """
    if head is None:
        log.info('%s', filename)
    else:
        log.info(head)
    file = open(filename)
    try:
        log.info(file.read())
    finally:
        file.close()